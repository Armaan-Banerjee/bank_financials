#!/usr/bin/env python3
"""How many profitability metrics can we ACTUALLY get, per year, per source.

    /usr/bin/python3 research/profitability/coverage_ceiling.py

Writes research/profitability/coverage_ceiling_<date>.md.

The gap report answers "what is missing from the deliverable". This answers a
different question: **what do we already hold, whether or not it is wired in.**
Those diverge sharply, because three collected sources reach no deliverable
column yet - the full thebanks.eu collection, the Wayback extraction, and five
aggregator banks dropped on a name mismatch.

TWO RULES THIS FILE OBEYS, both of them the project's own:

1. **The union is reported per source AND as a union, never as one merged
   number pretending to be one measure.** A computed ratio, the bank's own
   published figure on its own definition, and an aggregator's arithmetic are
   three different claims about the world. "We can get a return for this
   bank-year" is a real and useful statement; "the return is X" is not, unless
   you say whose.
2. **A ceiling is not a promise.** Everything counted here is already on disk.
   Nothing is projected from what a bank "probably" publishes.

ROE-family vs ROA-family: published measures carry 66 different labels, so they
are bucketed by what the DENOMINATOR is - anything naming assets is ROA-family,
anything naming equity (including tangible equity and RoTE) is ROE-family. A
label that names neither is counted in neither, and listed.
"""

import collections
import csv
import datetime
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
YEARS = ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025"]

STORE = os.path.join(HERE, "published_returns.jsonl")
AGG_WIRED = os.path.join(HERE, "agent_findings", "thebanks_eu.jsonl")
AGG_FULL = os.path.join(HERE, "thebanks_eu", "thebanks_eu_returns_with_archives.jsonl")
AGG_WAYBACK = os.path.join(HERE, "thebanks_eu", "wayback_returns.jsonl")

# Aggregator names that match no project bank. The entity each states is in the
# aggregator file and resolves unambiguously; see gaps_*.md.
AGG_ALIASES = {
    "HAMPSHIRE TRUST": "HAMPSHIRE TRUST BANK",
    "HSBC UK BANK": "HSBC UK BANK PLC",
    "NATWEST": "NATIONAL WESTMINSTER BANK PLC",
    "OAKNORTH": "OAKNORTH BANK",
    "SANTANDER UK": "SANTANDER",
}

# The bare abbreviations must be matched explicitly: `rote` does not match
# "ROE", so a label that is simply "ROE" fell into neither family on the first
# run. Tier 1 capital, capital employed, the net loan book and "return on
# investment" are deliberately left in NEITHER family - Tier 1 capital is not
# equity and ROCE is not ROE, so bucketing them would assert an equivalence
# the labels do not support.
ASSET_RE = re.compile(r"asset|\broa\b", re.I)
EQUITY_RE = re.compile(r"equity|\brote\b|\broe\b|shareholders|owner|funds", re.I)


def load_jsonl(path):
    out = []
    if not os.path.exists(path):
        return out
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        if "_schema" in rec and "bank" not in rec:
            continue
        out.append(rec)
    return out


def family(measure):
    if not measure:
        return None
    if ASSET_RE.search(measure):
        return "ROA"
    if EQUITY_RE.search(measure):
        return "ROE"
    return None


def main():
    csv_path = None
    for name in sorted(os.listdir(os.path.join(ROOT, "research")), reverse=True):
        if name.startswith("UK_banks_profitability_") and name.endswith(".csv"):
            csv_path = os.path.join(ROOT, "research", name)
            break
    rows = list(csv.DictReader(open(csv_path, encoding="utf-8")))
    banks = sorted({r["bank"] for r in rows})
    nbanks = len(banks)
    by = {(r["bank"], r["year"]): r for r in rows}

    # --- source sets, each a set of (bank, year) -----------------------------
    S = collections.defaultdict(set)

    for r in rows:
        k = (r["bank"], r["year"])
        if r["roe_pct_avg_equity"]:
            S["computed ROE (average equity)"].add(k)
        if r["roe_pct_year_end"]:
            S["computed ROE (year-end)"].add(k)
        if r["roa_pct_avg_assets"]:
            S["computed ROA (average assets)"].add(k)
        if r["roa_pct_year_end"]:
            S["computed ROA (year-end)"].add(k)
        if r["desk_research_roe_pct"]:
            S["prior desk research (ROE)"].add(k)
        if r["aggregator_roe_pct"] or r["aggregator_roa_pct"]:
            S["aggregator IN the deliverable"].add(k)

    unbucketed = collections.Counter()
    for r in load_jsonl(STORE):
        if r.get("publishes_none") or r.get("excluded"):
            continue
        k = (r.get("bank"), r.get("year"))
        if k[1] not in YEARS:
            continue
        fam = family(r.get("measure"))
        if fam == "ROE":
            S["bank's own published (ROE-family)"].add(k)
        elif fam == "ROA":
            S["bank's own published (ROA-family)"].add(k)
        else:
            unbucketed[r.get("measure")] += 1
        S["bank's own published (any)"].add(k)

    def numeric(raw):
        try:
            float(str(raw).replace("%", "").replace(",", "").strip())
            return True
        except (TypeError, ValueError):
            return False

    # aggregator, three files, names normalised through the alias table
    def agg_add(label, recs, roe_key, roa_key, bank_key="bank", year_key="year"):
        for r in recs:
            b = str(r.get(bank_key) or "").strip().upper()
            b = AGG_ALIASES.get(b, b)
            y = str(r.get(year_key) or "").strip()
            if not y.startswith("FY"):
                y = "FY" + y if re.fullmatch(r"\d{4}", y) else ""
            if b not in banks or y not in YEARS:
                continue
            if numeric(r.get(roe_key)) or numeric(r.get(roa_key)):
                S[label].add((b, y))

    # A VALUE MUST BE A NUMBER. This file uses the string "not found" as a
    # sentinel, and treating non-empty as present counted Streambank FY2022 as
    # covered when nothing was ever found for it - which inflated the reported
    # ceiling by one bank-year and, worse, moved Streambank FY2022 out of the
    # unreachable list. The build script was right and this script was wrong.
    for r in load_jsonl(AGG_WIRED):
        b = str(r.get("bank") or "").strip().upper()
        b = AGG_ALIASES.get(b, b)
        y = str(r.get("year") or "").strip()
        y = y if y.startswith("FY") else ("FY" + y if re.fullmatch(r"\d{4}", y) else "")
        if b in banks and y in YEARS and numeric(r.get("value")):
            S["aggregator: original file + name fixes"].add((b, y))

    agg_add("aggregator: full collection", load_jsonl(AGG_FULL), "roe_pct", "roa_pct")
    agg_add("aggregator: Wayback extraction", load_jsonl(AGG_WAYBACK), "roe_pct", "roa_pct")

    S["aggregator: ALL sources combined"] = (
        S["aggregator: original file + name fixes"]
        | S["aggregator: full collection"]
        | S["aggregator: Wayback extraction"])

    S["ANY computed ratio"] = (S["computed ROE (average equity)"]
                               | S["computed ROE (year-end)"]
                               | S["computed ROA (average assets)"]
                               | S["computed ROA (year-end)"])
    S["ANY return, ANY source"] = (S["ANY computed ratio"]
                                   | S["bank's own published (any)"]
                                   | S["aggregator: ALL sources combined"]
                                   | S["prior desk research (ROE)"])

    order = [
        "computed ROE (average equity)",
        "computed ROE (year-end)",
        "computed ROA (average assets)",
        "computed ROA (year-end)",
        "ANY computed ratio",
        "bank's own published (ROE-family)",
        "bank's own published (ROA-family)",
        "bank's own published (any)",
        "prior desk research (ROE)",
        "aggregator IN the deliverable",
        "aggregator: original file + name fixes",
        "aggregator: full collection",
        "aggregator: Wayback extraction",
        "aggregator: ALL sources combined",
        "ANY return, ANY source",
    ]

    date = datetime.date.today().isoformat()
    out = os.path.join(HERE, "coverage_ceiling_%s.md" % date)
    w = open(out, "w", encoding="utf-8").write

    w("# What we can actually get — coverage ceiling, %s\n\n" % date)
    w("Banks = **%d**; years FY2021-FY2025; %d bank-years.\n"
      % (nbanks, nbanks * len(YEARS)))
    w("Source: `%s` plus every collected file in this directory.\n\n"
      % os.path.basename(csv_path))
    w("**Counts are banks per year, out of %d.** Each source is reported\n" % nbanks)
    w("separately as well as in the union: a computed ratio, the bank's own figure\n")
    w("on its own definition, and an aggregator's arithmetic are three different\n")
    w("claims, and the union says only that SOME return is obtainable — never that\n")
    w("they agree or are interchangeable.\n\n")

    w("| Source | %s | total |\n" % " | ".join(YEARS))
    w("|---%s|---|\n" % ("|---" * len(YEARS)))
    for label in order:
        counts = [len({b for b, y in S[label] if y == yr}) for yr in YEARS]
        emph = "**" if label.startswith(("ANY", "aggregator: ALL")) else ""
        w("| %s%s%s | %s | %d |\n"
          % (emph, label, emph,
             " | ".join("%s%d%s" % (emph, c, emph) for c in counts), sum(counts)))
    w("\n")

    # what the unexploited sources would add
    w("## What is collected but NOT yet in the deliverable\n\n")
    gained = S["aggregator: ALL sources combined"] - S["aggregator IN the deliverable"]
    w("| | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 | total |\n")
    w("|---|---|---|---|---|---|---|\n")
    for label, st in (
        ("aggregator bank-years in the deliverable now", S["aggregator IN the deliverable"]),
        ("aggregator bank-years we actually hold", S["aggregator: ALL sources combined"]),
        ("**gain from wiring them in**", gained),
    ):
        counts = [len({b for b, y in st if y == yr}) for yr in YEARS]
        w("| %s | %s | %d |\n" % (label, " | ".join(str(c) for c in counts), sum(counts)))
    w("\n")

    # the hard floor: bank-years no source can reach
    unreachable = [(b, y) for b in banks for y in YEARS
                   if (b, y) not in S["ANY return, ANY source"]]
    w("## Bank-years NO source can reach\n\n")
    w("**%d of %d.** These are the real floor.\n\n" % (len(unreachable), nbanks * len(YEARS)))
    per_year = collections.Counter(y for _, y in unreachable)
    w("| year | unreachable |\n|---|---|\n")
    for y in YEARS:
        w("| %s | %d |\n" % (y, per_year[y]))
    w("\n")
    if unreachable:
        w("| bank | year | why (deliverable's own gap reason) |\n|---|---|---|\n")
        for b, y in sorted(unreachable):
            reason = (by.get((b, y), {}).get("gap_reason") or "").strip()
            w("| %s | %s | %s |\n" % (b, y, reason[:90] or "—"))
        w("\n")

    if unbucketed:
        w("## Published measures in neither family\n\n")
        w("Counted in the 'any' row but in neither ROE nor ROA, because the label\n")
        w("names neither denominator:\n\n")
        for m, n in unbucketed.most_common():
            w("- %r (%d)\n" % (m, n))
        w("\n")

    w("## Reading this\n\n")
    w("- **The computed year-end rows are the strongest coverage we have** and the\n")
    w("  average-basis rows are not a worse version of them: an average denominator\n")
    w("  needs the prior year, so FY2021 cannot have one. Where both exist they are\n")
    w("  different measures, not different qualities of the same measure.\n")
    w("- **The aggregator rows are the big movable number.** Only FY2024 reaches the\n")
    w("  deliverable today; the collection and the Wayback extraction cover FY2022\n")
    w("  and FY2023 as well, and five banks are lost purely to a name mismatch.\n")
    w("- **The own-published rows will not approach the computed rows** and should\n")
    w("  not be expected to: 66 banks publish no return at all, which is a finding.\n")
    w("  The ceiling there is roughly 72 banks, not 145.\n")

    print("wrote %s" % os.path.relpath(out, ROOT))
    for label in ("ANY computed ratio", "bank's own published (any)",
                  "aggregator: ALL sources combined", "ANY return, ANY source"):
        counts = [len({b for b, y in S[label] if y == yr}) for yr in YEARS]
        print("  %-36s %s  total %d" % (label, counts, sum(counts)))
    print("  unreachable bank-years: %d" % len(unreachable))


if __name__ == "__main__":
    main()
