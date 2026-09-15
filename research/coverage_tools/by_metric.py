"""Per-metric breakdown: which banks are missing which metric, and for which years.

Same conventions as coverage.py: MREL excluded, FY prefix regex-extracted from
annotated year strings, spine = years with real Balance Sheet data, window =
last 5 reported years. RWA Breakdown is included because it's a distinct sheet,
but it's evaluated differently: it either exists for a year or it doesn't.
"""
import json
import re
import sqlite3
from collections import defaultdict

DB = "/Users/armaan/code/katalysis/research/insights.db"
OUT = "/Users/armaan/code/katalysis/research/coverage_tools/by_metric.json"

P3 = ["CET1 Capital", "CET1 Ratio", "Tier 1 Capital", "Tier 1 Ratio",
      "Total Capital", "Total Capital Ratio", "Total RWAs",
      "Leverage Ratio", "LCR", "NSFR"]
BLANK = ("", "-", "n/a", "not publicly disclosed",
         "not applicable", "not disclosed")

# See coverage.py: "Not applicable" marks a year that structurally cannot carry
# the metric (pre-licence years, MREL for a non-resolution entity). Listing
# those as gaps sends agents to chase cells that can never be filled, so they
# are dropped from the register entirely.
NOT_APPLICABLE = ("not applicable", "n/a")


def fy(y):
    m = re.match(r"(FY\d{4})", y or "")
    return m.group(1) if m else None


def have(v):
    return v is not None and str(v).strip().lower() not in BLANK


def inapplicable(v):
    return v is not None and str(v).strip().lower() in NOT_APPLICABLE


con = sqlite3.connect(DB)
cur = con.cursor()
names = dict(cur.execute("SELECT frn, canonical_name FROM banks"))

spine = defaultdict(set)
for frn, year, raw in cur.execute(
        "SELECT frn, year, value_raw FROM annual_metrics WHERE sheet='Balance Sheet'"):
    f = fy(year)
    if f and have(raw):
        spine[frn].add(f)
window = {frn: sorted(ys, key=lambda y: -int(y[2:]))[:5] for frn, ys in spine.items()}

present = defaultdict(set)
na = defaultdict(set)
for frn, sheet, year, raw in cur.execute(
        "SELECT frn, sheet, year, value_raw FROM annual_metrics "
        "WHERE sheet IN (%s)" % ",".join("?" * (len(P3) + 1)), P3 + ["RWA Breakdown"]):
    f = fy(year)
    if not f:
        continue
    if have(raw):
        present[(frn, sheet)].add(f)
    elif inapplicable(raw):
        na[(frn, sheet)].add(f)

report = {}
for sheet in P3 + ["RWA Breakdown"]:
    banks = []
    for frn, years in window.items():
        if not years:
            continue
        held = present.get((frn, sheet), set())
        skip = na.get((frn, sheet), set())
        miss = [y for y in years if y not in held and y not in skip]
        if miss:
            # Every year this bank HAS disclosed the metric, including years
            # outside its 5-year window - that history is what distinguishes a
            # sourcing miss from a bank that genuinely never discloses.
            ever = sorted(held, key=lambda y: -int(y[2:]))
            banks.append({
                "bank": names.get(frn, frn),
                "missing": miss,
                "ever": ever,
                "n": len(miss),
                # "never disclosed" is judged against the years that COULD
                # carry the metric, not the raw 5-year window.
                "all5": len(miss) == len([y for y in years if y not in skip]),
            })
    banks.sort(key=lambda b: (-b["n"], b["bank"]))
    report[sheet] = banks

with open(OUT, "w") as fh:
    json.dump(report, fh, indent=1)

print(f"{'METRIC':22} {'banks':>6} {'cells':>6} {'all-5':>6}")
print("-" * 44)
for sheet, banks in report.items():
    print(f"{sheet:22} {len(banks):6} {sum(b['n'] for b in banks):6} "
          f"{sum(1 for b in banks if b['all5']):6}")
print(f"\nwritten: {OUT}")
