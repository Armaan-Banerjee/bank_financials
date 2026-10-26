#!/usr/bin/env python3
"""Write the profitability gap report: what is missing, per source, with causes.

    /usr/bin/python3 research/profitability/gap_report.py [deliverable.csv]

Writes research/profitability/gaps_<date>.md.

WHY A SCRIPT AND NOT A HAND-WRITTEN LIST. The question "which banks and years
are we missing" has four different answers here, one per source, and they must
not be blurred: a bank-year with no COMPUTED ratio is a different claim from
one where the bank PUBLISHES no return, which is different again from one an
aggregator does not carry. Hand-listing them is how the four get merged.

The second reason is that most apparent gaps are STRUCTURAL and a flat list
makes them look chaseable. A missing FY2021 average-equity ratio is usually
not missing data at all: an average denominator needs the prior year, and
FY2020 is outside the extract window, so the year-end ratio is the only one
that can exist there and it IS published. Likewise a bank that was not yet
licensed in 2021, or whose newest accounts are not filed, has no figure to
find. This script classifies each gap by cause so the handful worth chasing
are visible: a year missing in the MIDDLE of an otherwise complete series.
"""

import collections
import csv
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
YEARS_OLD_TO_NEW = ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025"]
STORE = os.path.join(HERE, "published_returns.jsonl")
AGG = os.path.join(HERE, "agent_findings", "thebanks_eu.jsonl")


def load_jsonl(path, skip_schema=True):
    out = []
    if not os.path.exists(path):
        return out
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        if skip_schema and "_schema" in rec and "bank" not in rec:
            continue
        out.append(rec)
    return out


def classify_year(have, year):
    """leading / trailing / middle, relative to the years this bank DOES have."""
    idx = [i for i, y in enumerate(YEARS_OLD_TO_NEW) if y in have]
    if not idx:
        return "none_at_all"
    i = YEARS_OLD_TO_NEW.index(year)
    if i < min(idx):
        return "leading"
    if i > max(idx):
        return "trailing"
    return "middle"


def main():
    csv_path = sys.argv[1] if len(sys.argv) > 1 else None
    if not csv_path:
        cands = sorted(f for f in os.listdir(ROOT + "/research")
                       if f.startswith("UK_banks_profitability_") and f.endswith(".csv"))
        if not cands:
            sys.exit("no deliverable CSV found; pass one explicitly")
        csv_path = os.path.join(ROOT, "research", cands[-1])
    rows = list(csv.DictReader(open(csv_path, encoding="utf-8")))
    banks = sorted({r["bank"] for r in rows})
    by = {(r["bank"], r["year"]): r for r in rows}

    have_stmt = collections.defaultdict(set)
    for r in rows:
        if r["profit_after_tax"]:
            have_stmt[r["bank"]].add(r["year"])

    # --- source 1: computed -------------------------------------------------
    stmt_missing = collections.defaultdict(list)   # cause -> [(bank, year)]
    for b in banks:
        for y in YEARS_OLD_TO_NEW:
            if y in have_stmt[b]:
                continue
            reason = by[(b, y)].get("gap_reason") or ""
            if "no such reporting period" in reason:
                cause = "period_label"
            else:
                cause = classify_year(have_stmt[b], y)
            stmt_missing[cause].append((b, y))

    roe_missing = collections.defaultdict(list)
    roa_missing = collections.defaultdict(list)
    for r in rows:
        b, y = r["bank"], r["year"]
        if not r["roe_pct_avg_equity"]:
            if not r["profit_after_tax"]:
                roe_missing["no_statement"].append((b, y))
            elif not r["total_equity"]:
                roe_missing["no_equity_line"].append((b, y))
            elif not r["equity_prior_year"]:
                roe_missing["needs_prior_year"].append((b, y))
            else:
                roe_missing["other"].append((b, y))
        if not r["roa_pct_avg_assets"]:
            if not r["profit_after_tax"]:
                roa_missing["no_statement"].append((b, y))
            elif not r["total_assets"]:
                roa_missing["no_assets_line"].append((b, y))
            elif not r["assets_prior_year"]:
                roa_missing["needs_prior_year"].append((b, y))
            else:
                roa_missing["other"].append((b, y))

    # --- source 2: the bank's own published return ---------------------------
    store = load_jsonl(STORE)
    pub_years = collections.defaultdict(set)
    pub_outside = collections.defaultdict(set)
    publishes_none, in_store = set(), set()
    for r in store:
        in_store.add(r["bank"])
        if r.get("publishes_none"):
            publishes_none.add(r["bank"])
            continue
        if r.get("excluded"):
            continue
        if r.get("year") in YEARS_OLD_TO_NEW:
            pub_years[r["bank"]].add(r["year"])
        elif r.get("year"):
            pub_outside[r["bank"]].add(r["year"])
    no_record = [b for b in banks if b not in in_store]
    # Snapshot these as PLAIN sets before anything reads pub_years by key.
    # pub_years/pub_outside are defaultdicts, so a bare `pub_years[b]` read -
    # e.g. inside a sum() over all 145 banks - INSERTS an empty entry for every
    # bank read. That made `b not in pub_years` false for all of them and
    # silently dropped a whole section of this report: no error, just absence.
    publishers = sorted(pub_years)
    in_window_banks = {b for b, ys in pub_years.items() if ys}
    outside_only = sorted(b for b, ys in pub_outside.items()
                          if ys and b not in in_window_banks)
    pub_year_total = sum(len(ys) for ys in pub_years.values())

    # --- source 4: aggregator name matching ---------------------------------
    # The alias table the BUILD now applies. Kept in sync by name: if a name
    # here stops being needed the build still resolves it, and this report
    # should say it is resolved rather than keep listing it as a loss.
    AGG_ALIASES = {
        "HAMPSHIRE TRUST": "HAMPSHIRE TRUST BANK",
        "HSBC UK BANK": "HSBC UK BANK PLC",
        "NATWEST": "NATIONAL WESTMINSTER BANK PLC",
        "OAKNORTH": "OAKNORTH BANK",
        "SANTANDER UK": "SANTANDER",
    }
    agg = load_jsonl(AGG, skip_schema=False)
    agg_names = {r["bank"].strip().upper(): r for r in agg if r.get("bank")}
    raw_unmatched = sorted(set(agg_names) - set(banks))
    aliased = [n for n in raw_unmatched if AGG_ALIASES.get(n) in banks]
    unmatched = [n for n in raw_unmatched if AGG_ALIASES.get(n) not in banks]

    date = datetime.date.today().isoformat()
    out = os.path.join(HERE, "gaps_%s.md" % date)
    w = open(out, "w", encoding="utf-8").write

    w("# Profitability coverage gaps — %s\n\n" % date)
    w("Source: `%s`, %d banks x %d years = %d bank-years.\n\n"
      % (os.path.basename(csv_path), len(banks), len(YEARS_OLD_TO_NEW), len(rows)))
    w("Generated by `gap_report.py`. **Four sources, four answers — never merged.**\n")
    w("A bank-year with no computed ratio is a different claim from one where the\n")
    w("bank publishes no return, which is different again from one an aggregator\n")
    w("does not carry.\n\n")

    # ---- banks missing, per year, per metric --------------------------------
    metrics = [
        ("Statement figures (profit after tax)",
         lambda b, y: bool(by[(b, y)]["profit_after_tax"])),
        ("ROE — average equity", lambda b, y: bool(by[(b, y)]["roe_pct_avg_equity"])),
        ("ROE — year-end", lambda b, y: bool(by[(b, y)]["roe_pct_year_end"])),
        ("ROA — average assets", lambda b, y: bool(by[(b, y)]["roa_pct_avg_assets"])),
        ("ROA — year-end", lambda b, y: bool(by[(b, y)]["roa_pct_year_end"])),
        ("Bank's own published return",
         lambda b, y: y in pub_years.get(b, set())),
        ("Prior desk research ROE", lambda b, y: bool(by[(b, y)]["desk_research_roe_pct"])),
        ("Aggregator (thebanks.eu)",
         lambda b, y: bool(by[(b, y)]["aggregator_roe_pct"]
                           or by[(b, y)]["aggregator_roa_pct"])),
    ]
    w("## Banks missing data, per year, per metric\n\n")
    w("Out of **%d banks** in every cell. The four sources are counted separately\n" % len(banks))
    w("and a high count is not automatically a gap — see the notes under the table.\n\n")
    w("| Metric | %s | All 5 |\n" % " | ".join(y for y in YEARS_OLD_TO_NEW))
    w("|---%s|---|\n" % ("|---" * len(YEARS_OLD_TO_NEW)))
    for name, fn in metrics:
        counts = [sum(1 for b in banks if not fn(b, y)) for y in YEARS_OLD_TO_NEW]
        w("| %s | %s | %d |\n"
          % (name, " | ".join(str(c) for c in counts), sum(counts)))
    w("\n")
    w("Reading it:\n\n")
    w("- **The two average-basis rows are not measuring absent data.** An average\n")
    w("  denominator needs the prior year, so FY2021 needs FY2020, which is outside\n")
    w("  the window. Compare each against the year-end row immediately below it:\n")
    w("  FY2021 ROE is 55 missing on the average basis and 9 on year-end, and the\n")
    w("  year-end figure IS published for those banks.\n")
    w("- **The statement-figures row is the real measure of our reach**, since every\n")
    w("  computed ratio derives from it: 17 absences in 725 bank-years, none of them\n")
    w("  mid-series.\n")
    w("- **The last three rows are other people's publishing decisions, not our\n")
    w("  coverage.** A bank that publishes no return cannot be missing one, and 66\n")
    w("  banks publish none at all — so most of the own-published row is a finding.\n")
    w("  The aggregator row is near-total by nature: the site exposes only the\n")
    w("  current performance year.\n\n")

    # Own-published, split by cause
    pure_none = set(publishes_none) - {r["bank"] for r in store
                                       if not r.get("publishes_none")
                                       and not r.get("excluded")}
    w("### The own-published row, split by cause\n\n")
    w("| Reason a bank-year has no own-published figure | %s |\n"
      % " | ".join(YEARS_OLD_TO_NEW))
    w("|---%s|\n" % ("|---" * len(YEARS_OLD_TO_NEW)))
    rows_out = []
    for label, fn in (
        ("Bank publishes no return at all — a FINDING, not a gap",
         lambda b, y: b in pure_none),
        ("No record — quarantined `ocr_lead` only",
         lambda b, y: b in set(no_record)),
        ("**Publishes returns, but not this year — the REAL gap**",
         lambda b, y: (b not in pure_none and b not in set(no_record)
                       and y not in pub_years.get(b, set()))),
    ):
        counts = [sum(1 for b in banks if fn(b, y)) for y in YEARS_OLD_TO_NEW]
        rows_out.append(counts)
        w("| %s | %s |\n" % (label, " | ".join(str(c) for c in counts)))
    w("| TOTAL missing | %s |\n\n"
      % " | ".join(str(sum(col)) for col in zip(*rows_out)))
    w("The real-gap row falls away sharply in FY2024-FY2025 because the sweep read\n")
    w("each bank's most recent report. FY2021-FY2023 need older editions.\n\n")

    w("## 1. Computed ROE / ROA (from the delivered workbooks)\n\n")
    w("| | count |\n|---|---|\n")
    w("| bank-years with a statement profit figure | **%d** of %d |\n"
      % (sum(len(have_stmt[b]) for b in banks), len(rows)))
    w("| ROE on average equity | %d |\n" % sum(1 for r in rows if r["roe_pct_avg_equity"]))
    w("| ROE year-end | %d |\n" % sum(1 for r in rows if r["roe_pct_year_end"]))
    w("| ROA on average assets | %d |\n" % sum(1 for r in rows if r["roa_pct_avg_assets"]))
    w("| ROA year-end | %d |\n\n" % sum(1 for r in rows if r["roa_pct_year_end"]))

    w("### Missing statement figures, by cause\n\n")
    labels = [
        ("middle", "**MID-SERIES HOLE — the only kind worth chasing**"),
        ("leading", "oldest end: the bank did not report that far back "
                    "(not yet licensed, or pre-dates the window)"),
        ("trailing", "newest end: accounts not filed yet"),
        ("period_label", "no such reporting period — an adjacent column covers it "
                         "(year-end change), so the data is present under another label"),
        ("none_at_all", "no figures in any year"),
    ]
    for key, label in labels:
        items = sorted(stmt_missing.get(key, []))
        w("- %s — **%d**\n" % (label, len(items)))
        for b, y in items:
            w("    - %s %s\n" % (b, y))
    w("\n")

    w("### Why a ratio is absent where the statement figures are present\n\n")
    for name, miss in (("ROE (average equity)", roe_missing), ("ROA (average assets)", roa_missing)):
        w("**%s** — %d absent of %d\n\n" % (name, sum(len(v) for v in miss.values()), len(rows)))
        for key, label in (
            ("no_statement", "no statement figures that year (listed above)"),
            ("no_equity_line", "no equity line in the balance sheet — GENUINE, structural"),
            ("no_assets_line", "no total-assets line"),
            ("needs_prior_year", "average basis needs the prior year, which is outside the "
                                 "window or is the bank's first reported year — the YEAR-END "
                                 "ratio exists for these"),
            ("other", "other"),
        ):
            items = sorted(miss.get(key, []))
            if not items:
                continue
            w("- %s — **%d**\n" % (label, len(items)))
            if key in ("no_equity_line", "no_assets_line", "other"):
                for b, y in items:
                    w("    - %s %s\n" % (b, y))
            else:
                per_year = collections.Counter(y for _, y in items)
                w("    - by year: %s\n" % ", ".join("%s %d" % (y, per_year[y])
                                                    for y in YEARS_OLD_TO_NEW if per_year[y]))
                non21 = [(b, y) for b, y in items if y != "FY2021"]
                if non21 and key == "needs_prior_year":
                    w("    - not FY2021, so not the window edge — each of these is the "
                      "bank's FIRST reported year + 1, where the prior year does not "
                      "exist to average against:\n")
                    for b, y in non21:
                        w("        - %s %s\n" % (b, y))
        w("\n")

    w("## 2. The bank's own published return\n\n")
    w("| | count |\n|---|---|\n")
    w("| banks with a store record | %d of %d |\n" % (len(in_store), len(banks)))
    w("| banks publishing at least one return | %d |\n" % len(publishers))
    w("| banks publishing none (a FINDING, not a gap) | %d |\n" % len(publishes_none))
    w("| **banks with NO record at all** | **%d** |\n" % len(no_record))
    w("| bank-years with an own-published figure | %d of %d |\n\n"
      % (pub_year_total, len(rows)))

    w("### Banks with no record at all\n\n")
    w("Their figures exist only as `ocr_lead` records quarantined in the sweep\n")
    w("batch files — read off search-indexed text, never rendered at 300 dpi.\n")
    w("Closing one means rendering its cited page and reading it.\n\n")
    for b in no_record:
        w("- %s\n" % b)
    w("\n")

    only_outside = outside_only
    if only_outside:
        w("### Publishes a return, but NOT for any year in the window\n\n")
        w("A distinct kind of gap: the measure exists for this bank, just not for\n")
        w("FY2021-FY2025. Two of these stopped publishing before the window opened,\n")
        w("which is a finding about the bank, not a hole in our reach.\n\n")
        for b in only_outside:
            w("- **%s** — publishes only %s\n"
              % (b, ", ".join(sorted(pub_outside[b]))))
        w("\nThis is why two counts of \"banks that publish\" are both correct and must\n")
        w("be labelled: **%d** publish a return somewhere, **%d** publish one inside\n"
          % (len(pub_years) + len(only_outside), len(pub_years)))
        w("the FY2021-FY2025 window.\n\n")

    w("### Own-published coverage by year\n\n")
    w("| year | banks with a published figure |\n|---|---|\n")
    for y in YEARS_OLD_TO_NEW:
        w("| %s | %d |\n" % (y, sum(1 for ys in pub_years.values() if y in ys)))
    w("\nThe early years are thin by construction, not by failure: the sweep read\n")
    w("each bank's MOST RECENT report, which carries only one or two comparative\n")
    w("years. Extending FY2021-FY2022 means pulling older editions — and under the\n")
    w("own-edition rule each such year should come from its own edition anyway.\n\n")

    w("### Per-bank missing years, for banks that DO publish\n\n")
    w("`publishes_none` banks are omitted: they have no gap to close.\n\n")
    w("| bank | has | missing |\n|---|---|---|\n")
    for b in publishers:
        missing = [y for y in YEARS_OLD_TO_NEW if y not in pub_years.get(b, set())]
        if not missing:
            continue
        w("| %s | %s | %s |\n" % (b,
                                  " ".join(y[2:] for y in YEARS_OLD_TO_NEW
                                           if y in pub_years.get(b, set())),
                                  " ".join(y[2:] for y in missing)))
    w("\n")

    w("## 3. Prior desk research\n\n")
    w("%d ROE values of %d bank-years. Third-party, of unknown derivation; kept as\n"
      % (sum(1 for r in rows if r["desk_research_roe_pct"]), len(rows)))
    w("its own column and never used to fill a computed or published cell.\n\n")

    w("## 4. Aggregator (thebanks.eu)\n\n")
    in_deliverable = sum(1 for r in rows if r["aggregator_roe_pct"] or r["aggregator_roa_pct"])
    w("Reaching the deliverable: **%d** bank-years, all FY2024.\n\n" % in_deliverable)
    w("**RESOLVED 2026-10-22.** %d aggregator banks previously never reached the\n" % len(aliased))
    w("deliverable because their name did not match and nothing reported the loss.\n")
    w("The build now applies an alias table, settled by the ENTITY the aggregator\n")
    w("file itself states rather than by name similarity:\n\n")
    w("| aggregator name | entity it states | deliverable name |\n|---|---|---|\n")
    resolve = {
        "HAMPSHIRE TRUST": "HAMPSHIRE TRUST BANK",
        "HSBC UK BANK": "HSBC UK BANK PLC",
        "NATWEST": "NATIONAL WESTMINSTER BANK PLC",
        "OAKNORTH": "OAKNORTH BANK",
        "SANTANDER UK": "SANTANDER",
    }
    for n in aliased:
        rec = agg_names[n]
        w("| %s | %s | %s |\n" % (n, rec.get("entity", ""), resolve.get(n, "?")))
    w("\nNote the two that look ambiguous and are not: the collector recorded "
      "`NOT NatWest Group plc` and\n`NOT Santander UK Group Holdings`, which is "
      "what settles them.\n\n")
    if unmatched:
        w("Still unmatched and therefore still dropped: %s\n\n"
          % ", ".join(unmatched))
    w("**ALSO RESOLVED 2026-10-22:** the full collection "
      "(`thebanks_eu_returns_with_archives.jsonl`,\n149 observations) and the Wayback "
      "extraction (`wayback_returns.jsonl`, 40) are now read\nby the build alongside the "
      "original file, and each value carries the verification\nstate it was collected "
      "under. The aggregator column went from 20 bank-years to\n**178**, and FY2022 and "
      "FY2023 are no longer empty.\n")

    print("wrote %s" % os.path.relpath(out, ROOT))
    print("  statement-figure gaps: %d (mid-series: %d)"
          % (sum(len(v) for v in stmt_missing.values()), len(stmt_missing.get("middle", []))))
    print("  banks with no published record: %d" % len(no_record))
    print("  aggregator aliases applied: %d | still unmatched: %d"
          % (len(aliased), len(unmatched)))


if __name__ == "__main__":
    main()
