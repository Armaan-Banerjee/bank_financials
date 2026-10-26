#!/usr/bin/env python3
"""Cross-check thebanks.eu's reported Total Assets against ours.

    /usr/bin/python3 research/profitability/thebanks_eu/extract_wayback.py
    /usr/bin/python3 research/profitability/thebanks_eu/crosscheck_inputs.py

RUN ORDER MATTERS, in that exact sequence. This script APPENDS its section to
wayback_extract_report.md, while `extract_wayback.py` rewrites that file from
scratch — so running the extractor afterwards silently discards this section.
Always run this one second.

WHAT THIS IS FOR. The Wayback captures carry thebanks.eu's own transcription
of Total Assets and Annual Profit for 100 bank-years. That is an INDEPENDENT
reading of the same primary documents we transcribed, and no existing check
axis compares our inputs against an outside source at all - `verify_workbook`
asks whether two of OUR transcriptions agree, not whether either is right.

WHAT A DIVERGENCE IS NOT. It is not an error in our figure. thebanks.eu is
known to mix bases: the README's trap 5 records it reporting Lloyds' GROUP
consolidated profit over BANK-only denominators. A divergence is a LEAD, to be
settled against the document, exactly like a `check_ratio_ties` break.

UNITS ARE THE WHOLE DIFFICULTY and this script refuses rather than guesses.
Our figures come in 16 different unit strings, including "conv. from USD"
variants, and thebanks.eu reports mln/bln in GBP or USD. A ratio only cancels
its unit if both sides share it, so any pair whose units are not confidently
comparable is SKIPPED and counted, never coerced. An earlier inline version of
this comparison lost the pound sign to shell quoting, fell through every unit
branch, and reported Havin Bank as diverging by a factor of a million - the
absurdity is what exposed it, which is a poor substitute for refusing.
"""

import collections
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
# HERE is research/profitability/thebanks_eu, so the repo root is three up.
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
WAYBACK = os.path.join(HERE, "wayback_returns.jsonl")
REPORT = os.path.join(HERE, "wayback_extract_report.md")

THOUSANDS = ("'000", "000s", "'000s")
MILLIONS = ("m",)


def ours_to_millions(value, unit):
    """Return the figure in millions of its OWN currency, or None if unsure."""
    try:
        x = float(str(value).replace(",", ""))
    except (TypeError, ValueError):
        return None, "unparseable"
    u = (unit or "").strip()
    if not u:
        return None, "no unit"
    if "conv." in u:
        # A converted figure is ours-after-FX; comparing it to the site's
        # native-currency number compares two different conversions.
        return None, "converted (FX)"
    if any(t in u for t in THOUSANDS):
        return x / 1000.0, None
    if u in ("£m", "$m") or u.startswith("£m") or u.startswith("$m"):
        return x, None
    if u == "£":
        return x / 1e6, None
    return None, "unrecognised unit %r" % u


def site_to_millions(block):
    try:
        x = float(str(block["value"]).replace(",", ""))
    except (TypeError, ValueError, KeyError):
        return None
    return x * 1000.0 if block.get("scale") == "bln" else x


def main():
    csv_path = None
    for name in sorted(os.listdir(os.path.join(ROOT, "research")), reverse=True):
        if name.startswith("UK_banks_profitability_") and name.endswith(".csv"):
            csv_path = os.path.join(ROOT, "research", name)
            break
    rows = list(csv.DictReader(open(csv_path, encoding="utf-8")))
    ours = {(r["bank"], r["year"]): r for r in rows}

    seen = {}
    skipped = collections.Counter()
    for line in open(WAYBACK, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        bank, year = rec.get("bank"), rec.get("year")
        block = (rec.get("site_inputs") or {}).get("total_assets")
        if not bank or not block or (bank, year) not in ours:
            continue
        if block.get("currency") != "GBP":
            skipped["site not GBP"] += 1
            continue
        row = ours[(bank, year)]
        if not row["total_assets"]:
            skipped["no figure of ours"] += 1
            continue
        mine, why = ours_to_millions(row["total_assets"], row["unit"])
        if mine is None:
            skipped[why] += 1
            continue
        theirs = site_to_millions(block)
        if theirs is None or not mine:
            skipped["unparseable"] += 1
            continue
        # One row per (bank, year); duplicate captures of the same page agree.
        seen[(bank, year)] = (theirs, mine, theirs / mine, row["unit"])

    pairs = sorted(seen.items(), key=lambda kv: -abs(kv[1][2] - 1))
    within2 = sum(1 for _, v in pairs if abs(v[2] - 1) <= 0.02)
    within10 = sum(1 for _, v in pairs if abs(v[2] - 1) <= 0.10)

    with open(REPORT, "a", encoding="utf-8") as fh:
        w = fh.write
        w("\n## Cross-check: thebanks.eu Total Assets vs ours\n\n")
        w("An INDEPENDENT reading of the same documents. No existing axis compares\n")
        w("our inputs against an outside source — `verify_workbook.py` only asks\n")
        w("whether two of our own transcriptions agree.\n\n")
        w("| | count |\n|---|---|\n")
        w("| comparable bank-years | **%d** |\n" % len(pairs))
        w("| agree within 2%% | %d |\n" % within2)
        w("| agree within 10%% | %d |\n" % within10)
        w("| **diverge by more than 10%%** | **%d** |\n" % (len(pairs) - within10))
        w("\nSkipped rather than coerced (a ratio cancels its unit only if both sides\n")
        w("share it): %s\n\n"
          % ", ".join("%s %d" % (k, v) for k, v in sorted(skipped.items())))
        if len(pairs) - within10:
            w("### Divergences over 10%% — LEADS, not errors\n\n")
            w("thebanks.eu is documented as mixing bases (README trap 5: Group profit\n")
            w("over Bank-only denominators for Lloyds), so a gap here is as likely to\n")
            w("be their perimeter as our transcription. Settle each against the document.\n\n")
            w("| bank | year | thebanks.eu (m) | ours (m) | theirs/ours | our unit |\n")
            w("|---|---|---|---|---|---|\n")
            for (b, y), (t, m, r, u) in pairs:
                if abs(r - 1) > 0.10:
                    w("| %s | %s | %.1f | %.1f | %.3f | %s |\n" % (b, y, t, m, r, u))
            w("\n")

    print("comparable: %d | within 2%%: %d | within 10%%: %d | diverging: %d"
          % (len(pairs), within2, within10, len(pairs) - within10))
    print("skipped: %s" % dict(skipped))
    for (b, y), (t, m, r, u) in pairs:
        if abs(r - 1) > 0.10:
            print("  LEAD %-34s %s theirs %.1f ours %.1f ratio %.3f  unit %s"
                  % (b, y, t, m, r, u))
    print("appended to %s" % os.path.relpath(REPORT, ROOT))


if __name__ == "__main__":
    main()
