#!/usr/bin/env python3
"""Inventory every workbook's per-sheet, per-year coverage - the gap audit.

WHY THIS EXISTS, AND WHAT IT IS NOT
-----------------------------------
`verify_workbook.py` checks a workbook is CONSISTENT with itself, and
`check_builds_current.py` checks a workbook is current with the script that
builds it. Neither can see the third axis: a workbook that is self-consistent,
freshly built, and simply MISSING data - an empty FY2025 column, an RWA
Breakdown that stops in 2023, a KM1 sheet that was never added. That gap is
invisible to both instruments and is what this script reports.

It was written against `bank_probs.txt`, a hand-written list of 72 such gaps
the user spotted by reading the workbooks. A hand-read list is a SAMPLE - it
finds what someone happened to notice. This is the census. Expect it to find
gaps the list missed and to contradict some entries on it; both are useful.

WHAT COUNTS AS A GAP - AND THE THING THIS SCRIPT CANNOT TELL YOU
----------------------------------------------------------------
An empty cell here means "this workbook has no figure". It does NOT mean the
bank failed to publish one. Those are different claims and only the second is
a defect worth chasing:

  (a) the bank never disclosed it            -> correct as-is, needs no work
  (b) the bank disclosed it and we missed it -> a real gap, go and get it
  (c) the bank has since published a newer
      edition than we cite                   -> a real gap, refresh it

This script CANNOT distinguish them - that needs the documents. It reports
shape, and shape only. Treat every line as a question, never as a verdict.

WHAT A CELL IS CLASSIFIED ON (changed 2026-09-18, GA-020)
---------------------------------------------------------
SHAPE decides whether a cell is a value; the phrase list only names the kind
of non-value. In that order:

    numeric                     -> data
    all dash characters         -> data      (the bank PRINTED a dash: it is
                                              saying "does not apply to us",
                                              which is neither silence nor a
                                              measured zero - user, 2026-09-18)
    matches NOT_DISCLOSED_RE    -> not_disclosed
    contains a digit            -> data      ('18.7%', '1,234' - CLAUDE.md:
                                              strings are valid cell values)
    anything else               -> not_disclosed, and the phrase is REPORTED

Before this, the phrase list was the whole test and everything unmatched fell
through to `data`, so 181 cells across 12 banks saying "Not required (SDDT)",
"Not presented", "Not separately disclosed" were counted as FIGURES. Alpha
Bank London's CET1 Ratio read as seven years of data holding none; Union
Bancaire Privee's Cash Flow Statement as fifty-three.

The fix is deliberately NOT a longer phrase list. That list always trails the
authors - three successive widenings in one afternoon each left cases out.
Unmatched phrasings are printed under ABSENCES CLASSIFIED BY SHAPE so they
stay visible; a real figure appearing there means the shape test is wrong.

AND WHERE THE EXPLANATION LIVES IS NOT WHERE THE GRID IS
--------------------------------------------------------
A sheet may explain an absence in its SUBTITLE or a row label instead of in
the year cells. Every wholly-empty Cash Flow Statement in this corpus does
exactly that, citing an FRS 101/102 or IAS 7 exemption - so a per-cell reading
called them unexplained gaps while the reason sat one row above the header.
Those columns are now marked `x` and reported apart as closures, not gaps.
This moved 14 workbooks out of the empty-column list (52 -> 38).

The three states the WORK is organised around - FOUND / NEVER PUBLISHED /
UNREACHED TODAY - still have no representation here. `n` conflates the last
two: "Not available today, no copy retrievable" matches NOT_DISCLOSED_RE and
so a limit on OUR reach is filed as a fact about the bank. That is GA-020 and
is NOT fixed by this change.

A wholly-empty year column is called out separately because it is the one
shape that is a defect whatever the cause: per the user's instruction of
2026-09-17, a year for which a sheet holds nothing at all should not carry a
header on that sheet (Alrayan's KM1 FY2021/FY2020 being the named example).

Usage:
    python3 scripts/audit_gaps.py                  # whole corpus, summary
    python3 scripts/audit_gaps.py --tsv            # one row per sheet-year
    python3 scripts/audit_gaps.py --bank ALRAYAN   # one bank, verbose
    python3 scripts/audit_gaps.py --json out.json  # machine-readable
"""

import argparse
import glob
import json
import os
import re
import sys

import openpyxl

BANKS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "banks")

HEADER_ROW = 3

# Sheets whose shape is "one column per year", which is the only shape this
# audit can read. Statement of Changes in Equity is deliberately absent: it is
# a chronological roll-forward (equity-component columns x movement rows), so
# its columns are not years and a year-coverage question is meaningless there.
YEAR_COLUMN_SHEETS = [
    "Balance Sheet",
    "Profit & Loss",
    "Cash Flow Statement",
    "Asset Quality",
    "KM1 Key Metrics",
    "CET1 Capital",
    "CET1 Ratio",
    "Tier 1 Capital",
    "Tier 1 Ratio",
    "Total Capital",
    "Total Capital Ratio",
    "Total RWAs",
    "RWA Breakdown",
    "Leverage Ratio",
    "LCR",
    "NSFR",
    "MREL Ratio",
    "Interim Pillar 3",
]

# A cell holding one of these is a STATEMENT ABOUT ABSENCE, not a figure. It
# must not be counted as data (it would hide the gap) nor as blank (it would
# invent one - the bank was asked and the answer was recorded). Counted apart.
#
# THIS LIST IS NOT THE CLASSIFIER, AND MUST NOT BE TREATED AS ONE. It decides
# only WHICH KIND of non-value a cell holds; whether a cell is a value at all
# is decided by SHAPE below. Until 2026-09-18 this regex was the whole test,
# with everything unmatched falling through to `data` - so 174 cells across 11
# banks saying "Not required (SDDT)", "Not presented" or "Not separately
# disclosed" were counted as FIGURES. Widening the phrase list is not the fix
# and never will be: the list always trails the authors. See GA-020.
NOT_DISCLOSED_RE = re.compile(
    r"not\s+(publicly\s+)?(disclosed|published|available|applicable|reported)"
    r"|no\s+(pillar\s*3|km1)"
    r"|^n/?a$",
    re.I,
)

# A PRINTED DASH IS PUBLISHED CONTENT, NOT AN ABSENCE. The user decided this
# explicitly on 2026-09-18 and CLAUDE.md carries it: a dash is the bank saying
# "this does not apply to us", which is a different statement from silence and
# from a measured zero. Chetwood's KM1 prints all three on adjacent rows of one
# table. 267 dash-only cells across 24 banks depend on this carve-out; without
# it the shape test below would reclassify every one of them as a non-value and
# silently reverse that decision.
DASH_CHARS = {"-", "‐", "‑", "‒", "–", "—", "−"}

# A sheet may explain an absence in its SUBTITLE or in a row label, rather than
# in the year cells - which is what every wholly-empty Cash Flow Statement in
# this corpus does (13 banks, ~101 sheet-years, all citing an FRS 101/102 or
# IAS 7 exemption). Those year columns hold nothing, so a per-cell reading
# reports them as unexplained gaps; the explanation is one row above, outside
# the year grid entirely. Deliberately wide - it decides only whether a sheet
# says ANYTHING about why it is empty.
EXPLAINS_RE = re.compile(
    r"\bnot\b[^.;]{0,30}?\b(disclos\w*|publish\w*|present\w*|applicable|available"
    r"|report\w*|used|broken|split|shown|stated|given|provided|separat\w*|prepar\w*"
    r"|required|computed|located|filed)"
    r"|\bno\b[^.;]{0,40}?\b(statement|disclosure|pillar\s*3|km1|edition|document"
    r"|figure|breakdown|template|cash\s*flow)"
    r"|exempt\w*|FRS\s*10[12]|FRS\s*1\b|IAS\s*7"
    r"|template not used|does not (publish|disclose|prepare)",
    re.I,
)

YEAR_RE = re.compile(r"\bFY(\d{4})\b")


def _is_dash(v):
    """True when a cell's entire content is dash characters.

    Matches on EVERY character rather than exact equality, so '--' counts as
    the printed dash it plainly is. One such cell exists (Punjab National
    International); an exact-membership test classified it as an absence while
    treating the 26 single dashes in the same workbook as content, which is the
    same figure being read two ways inside one sheet.
    """
    if not isinstance(v, str):
        return False
    s = v.strip()
    return bool(s) and all(ch in DASH_CHARS for ch in s)


def _year_of(label):
    """Pull the year out of a header cell.

    Headers are written several ways across the corpus - 'FY2025',
    "FY2025 (£'000)", 'FY2025 (£m)' - and at least one bank carries a spanning
    label like 'FY2022-FY2023'. Take the LAST year mentioned, so a span is
    attributed to the year it ends in rather than silently dropped.
    """
    if label is None:
        return None
    hits = YEAR_RE.findall(str(label))
    return int(hits[-1]) if hits else None


def audit_workbook(path):
    name = os.path.basename(path).replace(" FINANCIALS.xlsx", "")
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    result = {
        "bank": name,
        "sheets": wb.sheetnames,
        "n_sheets": len(wb.sheetnames),
        "has_km1": "KM1 Key Metrics" in wb.sheetnames,
        "has_rwa_breakdown": "RWA Breakdown" in wb.sheetnames,
        "has_interim": "Interim Pillar 3" in wb.sheetnames,
        "coverage": {},
        "missing_sheets": [],
        # Sheets whose year grid is wholly empty but which SAY WHY in their
        # subtitle or a row label. Their columns are not unexplained gaps.
        "explained_sheets": {},
        # Phrasings caught by the shape test but not by NOT_DISCLOSED_RE.
        # Surfaced rather than swallowed: a genuine figure landing here would
        # mean the shape test is wrong, and that must be visible.
        "unphrased_absences": {},
    }

    for sheet in YEAR_COLUMN_SHEETS:
        if sheet not in wb.sheetnames:
            # Interim Pillar 3 and KM1 are legitimately optional; the rest are
            # the 18-sheet baseline and their absence is itself a finding.
            if sheet not in ("Interim Pillar 3",):
                result["missing_sheets"].append(sheet)
            continue

        ws = wb[sheet]
        rows = list(ws.iter_rows(values_only=True))
        if len(rows) < HEADER_ROW:
            result["coverage"][sheet] = {}
            continue

        header = rows[HEADER_ROW - 1]
        years = {}  # col index -> year
        for ci, cell in enumerate(header):
            y = _year_of(cell)
            if y is not None and ci > 0:
                years[ci] = y
        if not years:
            result["coverage"][sheet] = {}
            continue

        counts = {y: {"data": 0, "not_disclosed": 0} for y in years.values()}
        for r in rows[HEADER_ROW:]:
            # The source-citation cell is a merged block in column A with
            # nothing beside it; it is not a data row and must not be read as
            # one. Rows whose column A is empty are section spacers.
            for ci, y in years.items():
                if ci >= len(r):
                    continue
                v = r[ci]
                if v is None or (isinstance(v, str) and not v.strip()):
                    continue
                # CLASSIFY ON SHAPE FIRST, PHRASE SECOND. The question "is this
                # a value?" is answered by what the cell looks like; the phrase
                # list only names the kind of non-value. Order matters: a dash
                # is published content and is tested before anything else.
                if isinstance(v, (int, float)):
                    counts[y]["data"] += 1
                elif _is_dash(v):
                    counts[y]["data"] += 1          # the bank printed a dash
                elif NOT_DISCLOSED_RE.search(str(v)):
                    counts[y]["not_disclosed"] += 1
                elif re.search(r"\d", str(v)):
                    # A figure stored as a string - "18.7%", "1,234", "£2.5m".
                    # CLAUDE.md: numbers and strings are both valid cell values.
                    counts[y]["data"] += 1
                else:
                    # Prose with no digit in it is not a figure, whatever it
                    # says. Previously this fell through to `data`.
                    counts[y]["not_disclosed"] += 1
                    result["unphrased_absences"][str(v).strip()[:60]] = (
                        result["unphrased_absences"].get(str(v).strip()[:60], 0) + 1)
        result["coverage"][sheet] = {
            str(y): counts[y] for y in sorted(counts, reverse=True)
        }

        # Does this sheet explain itself outside the year grid? Only asked when
        # the grid is wholly empty, because that is the only case where the
        # per-cell reading has nothing to go on. Column A of EVERY row is read,
        # from row 1 - the subtitle sits ABOVE the header row and is the place
        # these sheets most often put the reason.
        if not any(c["data"] or c["not_disclosed"] for c in counts.values()):
            prose = " ".join(
                str(r[0]) for r in rows if r and r[0] not in (None, "")
            )
            if EXPLAINS_RE.search(prose):
                result["explained_sheets"][sheet] = sorted(
                    counts, reverse=True)

    wb.close()

    # --- derived flags -----------------------------------------------------
    all_years = set()
    for cov in result["coverage"].values():
        all_years.update(int(y) for y in cov)
    result["years"] = sorted(all_years, reverse=True)
    result["latest_year"] = max(all_years) if all_years else None

    # An empty column on a sheet that explains itself is NOT the same finding
    # as an empty column on a sheet that says nothing. Reported apart so a
    # closure is never counted as a gap, and a gap never hides inside a
    # closure. `empty_year_columns` keeps its meaning: UNEXPLAINED emptiness.
    empty_cols, explained_cols = [], []
    for sheet, cov in result["coverage"].items():
        for y, c in cov.items():
            if c["data"] == 0 and c["not_disclosed"] == 0:
                if sheet in result["explained_sheets"]:
                    explained_cols.append((sheet, int(y)))
                else:
                    empty_cols.append((sheet, int(y)))
    result["empty_year_columns"] = sorted(empty_cols, key=lambda t: (t[0], -t[1]))
    result["explained_empty_year_columns"] = sorted(
        explained_cols, key=lambda t: (t[0], -t[1]))

    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bank", help="substring of one bank name")
    ap.add_argument("--tsv", action="store_true")
    ap.add_argument("--json", metavar="PATH")
    ap.add_argument("--min-year", type=int, default=2025,
                    help="flag workbooks whose latest year is below this")
    args = ap.parse_args()

    paths = sorted(glob.glob(os.path.join(BANKS_DIR, "*FINANCIALS.xlsx")))
    if args.bank:
        needle = args.bank.upper()
        paths = [p for p in paths if needle in os.path.basename(p).upper()]
    if not paths:
        print("no workbooks matched", file=sys.stderr)
        return 1

    results = []
    for p in paths:
        try:
            results.append(audit_workbook(p))
        except Exception as exc:  # a workbook that cannot be opened is itself a finding
            print(f"!! {os.path.basename(p)}: {type(exc).__name__}: {exc}", file=sys.stderr)

    if args.json:
        with open(args.json, "w") as fh:
            json.dump(results, fh, indent=1)
        print(f"wrote {args.json} ({len(results)} workbooks)")

    if args.tsv:
        print("bank\tsheet\tyear\tdata_cells\tnot_disclosed_cells")
        for r in results:
            for sheet, cov in r["coverage"].items():
                for y, c in cov.items():
                    print(f"{r['bank']}\t{sheet}\t{y}\t{c['data']}\t{c['not_disclosed']}")
        return 0

    if args.bank and len(results) == 1:
        r = results[0]
        print(f"{r['bank']} - {r['n_sheets']} sheets, years {r['years']}")
        if r["missing_sheets"]:
            print(f"  MISSING SHEETS: {', '.join(r['missing_sheets'])}")
        for sheet, cov in r["coverage"].items():
            explained = sheet in r["explained_sheets"]
            bits = []
            for y, c in cov.items():
                if c["data"]:
                    mark = "."
                elif c["not_disclosed"]:
                    mark = "n"
                elif explained:
                    mark = "x"
                else:
                    mark = "_"
                bits.append(f"{y}{mark}")
            print(f"  {sheet:<24} {' '.join(bits)}")
        print("\n  key: . = has figures   n = 'not disclosed' recorded in a cell"
              "\n       x = grid empty, but the SHEET explains why (subtitle or row label)"
              "\n       _ = EMPTY and unexplained - the only mark that is a question")
        if r["unphrased_absences"]:
            print("\n  absence phrasings not in NOT_DISCLOSED_RE, classified by shape:")
            for phrase, n in sorted(r["unphrased_absences"].items(),
                                    key=lambda kv: -kv[1]):
                print(f"    {n:4}  {phrase!r}")
        return 0

    # corpus summary
    no_km1 = [r["bank"] for r in results if not r["has_km1"]]
    stale = [(r["bank"], r["latest_year"]) for r in results
             if r["latest_year"] is not None and r["latest_year"] < args.min_year]
    empties = [r for r in results if r["empty_year_columns"]]
    missing = [r for r in results if r["missing_sheets"]]

    print(f"=== gap audit: {len(results)} workbooks ===\n")
    print(f"NO KM1 SHEET ({len(no_km1)}):")
    for b in no_km1:
        print(f"    {b}")
    print(f"\nLATEST YEAR BELOW FY{args.min_year} ({len(stale)}):")
    for b, y in sorted(stale, key=lambda t: t[1]):
        print(f"    FY{y}  {b}")
    print(f"\nMISSING BASELINE SHEETS ({len(missing)}):")
    for r in missing:
        print(f"    {r['bank']}: {', '.join(r['missing_sheets'])}")
    print(f"\nWHOLLY EMPTY YEAR COLUMNS - UNEXPLAINED ({len(empties)} workbooks):")
    for r in empties:
        by_sheet = {}
        for sheet, y in r["empty_year_columns"]:
            by_sheet.setdefault(sheet, []).append(y)
        parts = [f"{s} [{', '.join(str(y) for y in sorted(ys, reverse=True))}]"
                 for s, ys in sorted(by_sheet.items())]
        print(f"    {r['bank']}: {'; '.join(parts)}")

    explained = [r for r in results if r.get("explained_empty_year_columns")]
    n_exp = sum(len(r["explained_empty_year_columns"]) for r in explained)
    print(f"\nEMPTY BUT EXPLAINED ON THE SHEET ({len(explained)} workbooks, "
          f"{n_exp} sheet-years) - closures, NOT gaps:")
    for r in explained:
        by_sheet = {}
        for sheet, y in r["explained_empty_year_columns"]:
            by_sheet.setdefault(sheet, []).append(y)
        parts = [f"{s} x{len(ys)}" for s, ys in sorted(by_sheet.items())]
        print(f"    {r['bank']}: {'; '.join(parts)}")

    unphrased = {}
    for r in results:
        for phrase, n in r["unphrased_absences"].items():
            unphrased[phrase] = unphrased.get(phrase, 0) + n
    if unphrased:
        total = sum(unphrased.values())
        print(f"\nABSENCES CLASSIFIED BY SHAPE, NOT BY PHRASE ({total} cells) -"
              "\n  these were counted as FIGURES before 2026-09-18. A real"
              "\n  figure appearing in this list means the shape test is wrong:")
        for phrase, n in sorted(unphrased.items(), key=lambda kv: -kv[1])[:20]:
            print(f"    {n:4}  {phrase!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
