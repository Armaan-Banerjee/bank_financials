"""Recompute Pillar 3 coverage after the gap-filling batches.

Mirrors the classification used throughout this session:
  - MREL excluded from headline coverage (structural: only UK resolution
    entities have an MREL requirement, ~130 of 145 banks legitimately have none)
  - year strings carry annotations ("FY2025 (y/e 30 Jun 25)"), so always
    regex-extract the FY prefix rather than comparing exact strings
  - the "spine" is the years a bank has real Balance Sheet data for
"""
import re
import sqlite3
from collections import defaultdict

DB = "/Users/armaan/code/katalysis/research/insights.db"

P3 = ["CET1 Capital", "CET1 Ratio", "Tier 1 Capital", "Tier 1 Ratio",
      "Total Capital", "Total Capital Ratio", "Total RWAs",
      "Leverage Ratio", "LCR", "NSFR"]

BLANK = ("", "-", "n/a", "not publicly disclosed",
         "not applicable", "not disclosed")

# "Not applicable" is NOT a gap: it's the project's explicit marker for a year
# that structurally cannot have the metric (pre-licence / pre-incorporation
# years, MREL for a non-resolution entity). Those cells are already resolved
# and can never be filled, so they leave the denominator entirely rather than
# counting as filled - counting them either way distorts the rate. Contrast
# "not publicly disclosed", which IS a real coverage limitation: the figure
# exists at the bank, it just isn't published.
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

# Spine: years each bank actually reports (real Balance Sheet data).
spine = defaultdict(set)
for frn, year, raw in cur.execute(
        "SELECT frn, year, value_raw FROM annual_metrics WHERE sheet='Balance Sheet'"):
    f = fy(year)
    if f and have(raw):
        spine[frn].add(f)

# Last 5 reported years per bank.
window = {frn: sorted(ys, key=lambda y: -int(y[2:]))[:5] for frn, ys in spine.items()}

# What's present per (frn, sheet, year).
present = defaultdict(set)
na = defaultdict(set)
for frn, sheet, year, raw in cur.execute(
        "SELECT frn, sheet, year, value_raw FROM annual_metrics WHERE sheet IN (%s)"
        % ",".join("?" * len(P3)), P3):
    f = fy(year)
    if not f:
        continue
    if have(raw):
        present[(frn, sheet)].add(f)
    elif inapplicable(raw):
        na[(frn, sheet)].add(f)

names = dict(cur.execute("SELECT frn, canonical_name FROM banks"))

filled = total = inapplicable_cells = 0
by_metric = defaultdict(lambda: [0, 0])   # sheet -> [filled, total]
by_year = defaultdict(lambda: [0, 0])
gaps = defaultdict(list)                  # frn -> [(sheet, year)]

for frn, years in window.items():
    if not years:
        continue
    for sheet in P3:
        for y in years:
            if y in na.get((frn, sheet), ()):
                inapplicable_cells += 1
                continue
            total += 1
            by_metric[sheet][1] += 1
            by_year[y][1] += 1
            if y in present.get((frn, sheet), ()):
                filled += 1
                by_metric[sheet][0] += 1
                by_year[y][0] += 1
            else:
                gaps[frn].append((sheet, y))

print(f"Banks with a reported spine: {len(window)}")
print(f"Pillar 3 coverage (MREL excluded): {filled}/{total} = {100*filled/total:.1f}%")
print(f"Open cells: {total-filled}")
print(f"Excluded as structurally inapplicable: {inapplicable_cells}\n")

print("By metric:")
for sheet in P3:
    f, t = by_metric[sheet]
    print(f"  {sheet:22} {f:5}/{t:<5} {100*f/t:5.1f}%   gap {t-f}")

print("\nBy year:")
for y in sorted(by_year, key=lambda y: -int(y[2:])):
    f, t = by_year[y]
    print(f"  {y}  {f:5}/{t:<5} {100*f/t:5.1f}%   gap {t-f}")

print("\nTop 15 banks by open cells:")
for frn, gs in sorted(gaps.items(), key=lambda kv: -len(kv[1]))[:15]:
    print(f"  {names.get(frn, frn)[:44]:46} {len(gs):3}")

# NSFR FY2021-and-earlier, now understood as structural (PRA PS17/21).
nsfr_pre22 = sum(1 for frn, gs in gaps.items()
                 for s, y in gs if s == "NSFR" and int(y[2:]) <= 2021)
nsfr_22 = sum(1 for frn, gs in gaps.items()
              for s, y in gs if s == "NSFR" and int(y[2:]) == 2022)
print(f"\nNSFR gaps FY2021 or earlier (structural, PRA PS17/21): {nsfr_pre22}")
print(f"NSFR gaps FY2022 (often structural - 4-quarter-average rule): {nsfr_22}")
print(f"Open cells excluding structural pre-2022 NSFR: {total-filled-nsfr_pre22}")

# ---- adjusted view: strip cells already proved structural ----
ENTITY_BASIS = ["Rathbones", "Standard Chartered Bank", "Nomura Bank International",
                "Santander Financial Services", "J.P. Morgan Europe"]
structural = 0
for frn, gs in gaps.items():
    nm = names.get(frn, "")
    is_entity = any(k.lower() in nm.lower() for k in ENTITY_BASIS)
    for s, y in gs:
        if is_entity or (s == "NSFR" and int(y[2:]) <= 2021):
            structural += 1
adj_total = total - structural
print(f"\n--- adjusted (entity-basis banks + pre-2022 NSFR removed) ---")
print(f"Structural cells removed: {structural}")
print(f"Adjusted coverage: {filled}/{adj_total} = {100*filled/adj_total:.1f}%")
print(f"Genuinely open: {adj_total-filled}")
