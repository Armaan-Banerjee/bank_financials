#!/usr/bin/env python3
"""Fifth check axis: does the Overview sheet agree with the sheets it summarises?

The Overview is a HAND-COPIED DUPLICATE. Every build script passes
`balance_sheet_totals=[...]`, `income_statement_totals=[...]` and so on to
add_overview_sheet() as literal dicts, separate from the `rows` that build the
detail sheets. Nothing has ever compared the two, so the copy can silently
diverge from its source - and it does:

  - Access Bank UK prints an FY2019 heading on four Overview blocks with no
    figure under any of them, while its Balance Sheet carries 22 populated
    FY2019 cells.
  - Starling's Overview Balance Sheet block skips FY2019 entirely while
    carrying FY2018 and FY2017 either side of it.

None of the four existing axes can see this. verify_workbook.py checks a
workbook against ITSELF but never compares the Overview to the detail sheets.
audit_gaps.py counts cells per sheet and so reports the Overview's emptiness
and the Balance Sheet's fullness as two unrelated facts. check_builds_current
checks staleness; check_ratio_ties divides single-metric sheets.

REPORTS LEADS, NOT VERDICTS, like the other axes. A coverage break can be
(a) the Overview genuinely lagging a later-filled sheet, (b) a curated omission
someone made deliberately (a year on a different basis, say), or (c) this
script's own label matching falling short. A value break can be a copy error on
either side, a unit difference between the block heading and the sheet, or a
deliberately different figure (an Overview "Total income" summarising a sheet
that splits revenue across two presentations). Only the documents and the sheet
notes separate them.

KNOWN LIMITS, stated so nobody reads past them:
  - The Statement of Changes in Equity detail sheet is CHRONOLOGICAL, not
    year-columned, so its block gets no coverage comparison. Its figures are
    therefore unchecked here.
  - Value ties are only attempted where the Overview label and the detail-sheet
    row label match EXACTLY (case- and whitespace-insensitive). Curated labels
    like "Total income / Revenue" match nothing and are skipped. The `compared`
    and `skipped` counts in the summary are part of the result: a run that
    skips heavily is reporting its own reach, not a clean corpus.
  - Only NUMERIC cells count as data on either side. A "Not published yet - ..."
    or "Not applicable - ..." statement is deliberately NOT treated as a figure,
    so a year that carries only such a statement reads as empty here. That is
    intended: those are recorded absences, not values.
  - A year column at the NEWEST end that is empty everywhere is usually CORRECT
    (the period has not been reported yet) and this script does not flag it.
    Only a block that is empty where its own detail sheet has figures is
    reported.

Usage:
    python3 scripts/check_overview_ties.py            # whole corpus
    python3 scripts/check_overview_ties.py STARLING   # one bank (substring)
"""
import glob
import os
import re
import sys

import openpyxl

FY = re.compile(r"FY(\d{4})")

# Overview block title prefix -> the detail sheet it duplicates.
# "Statement of Changes in Equity" is deliberately absent: that sheet is a
# chronological roll-forward with no year columns to compare against.
BLOCK_TO_SHEET = {
    "balance sheet summary": "Balance Sheet",
    "profit & loss summary": "Profit & Loss",
    "cash flow summary": "Cash Flow Statement",
}

# The ratios block names its rows after the single-metric sheets directly.
PILLAR3_BLOCK = "pillar 3 key metrics"

TOL = 0.005  # relative tolerance for a value tie (0.5%), to absorb rounding


def fy(v):
    m = FY.search(str(v)) if v is not None else None
    return int(m.group(1)) if m else None


def norm(label):
    return re.sub(r"\s+", " ", str(label)).strip().lower()


def num(v):
    if isinstance(v, (int, float)):
        return float(v)
    if v is None:
        return None
    s = str(v).strip().replace(",", "").replace("£", "").replace("$", "")
    s = s.replace("%", "")
    if s.startswith("(") and s.endswith(")"):
        s = "-" + s[1:-1]
    try:
        return float(s)
    except ValueError:
        return None


def year_cols(header):
    """{column index: year} for the CONTIGUOUS run of FY columns only.

    This matters: add_overview_sheet writes an auxiliary CHART DATA region far
    to the right of the display table (Starling's Overview runs to column 76),
    repeating the same year labels in oldest-first order with their own values.
    Taking every FY-labelled column in the header row swallows that region and
    maps chart numbers onto the wrong rows - NSFR values landing on 'Total
    assets', for one. Stopping at the first gap after the first year column
    keeps the visible table and nothing else.
    """
    cols, started = {}, False
    for i, v in enumerate(header):
        if i == 0:
            continue
        y = fy(v)
        if y is not None:
            cols[i] = y
            started = True
        elif started:
            break
    return cols


def header_row(ws, limit=8):
    """(row index, values) of the first row carrying >=2 FY labels."""
    for r in range(1, min(ws.max_row, limit) + 1):
        vals = [c.value for c in ws[r]]
        if len(year_cols(vals)) >= 2:
            return r, vals
    return None, None


def sheet_table(ws):
    """(year -> has numeric data, {normalised label: {year: value}})."""
    hr, hdr = header_row(ws)
    if hr is None:
        return {}, {}
    cols = year_cols(hdr)
    has = {y: False for y in cols.values()}
    labels = {}
    for row in ws.iter_rows(min_row=hr + 1, values_only=True):
        if not row or row[0] is None or not str(row[0]).strip():
            continue
        key = norm(row[0])
        for i, y in cols.items():
            if i >= len(row):
                continue
            if isinstance(row[i], (int, float)):
                has[y] = True
            if row[i] is not None and str(row[i]).strip():
                labels.setdefault(key, {})[y] = row[i]
    return has, labels


def overview_blocks(ws):
    """[(title, {year: has numeric}, {normalised label: {year: value}})]"""
    rows = list(ws.iter_rows(min_row=1, values_only=True))
    out = []
    for n, row in enumerate(rows):
        if not row or row[0] is None:
            continue
        if norm(row[0]) != "line item" or len(year_cols(row)) < 2:
            continue
        cols = year_cols(row)
        title = ""
        for back in range(n - 1, max(-1, n - 4), -1):
            if rows[back] and rows[back][0] and str(rows[back][0]).strip():
                title = str(rows[back][0]).strip()
                break
        has = {y: False for y in cols.values()}
        labels = {}
        for r2 in rows[n + 1:]:
            if not r2 or r2[0] is None or not str(r2[0]).strip():
                continue
            key = norm(r2[0])
            if key == "line item" or key.startswith("note:"):
                break
            for i, y in cols.items():
                if i >= len(r2):
                    continue
                if isinstance(r2[i], (int, float)):
                    has[y] = True
                if r2[i] is not None and str(r2[i]).strip():
                    labels.setdefault(key, {})[y] = r2[i]
        out.append((title, has, labels))
    return out


def main():
    want = sys.argv[1].upper() if len(sys.argv) > 1 else None
    lag, ahead, valbreak = [], [], []
    banks = compared = skipped_lbl = 0

    for path in sorted(glob.glob("banks/*FINANCIALS.xlsx")):
        base = os.path.basename(path)
        if base.startswith("~$"):
            continue
        bank = base.replace(" FINANCIALS.xlsx", "")
        if want and want not in bank.upper():
            continue
        try:
            wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        except Exception as exc:
            print(f"!! {bank}: {type(exc).__name__}: {exc}")
            continue
        if "Overview" not in wb.sheetnames:
            wb.close()
            continue
        banks += 1
        cache = {}

        def detail(name):
            if name not in cache:
                cache[name] = sheet_table(wb[name]) if name in wb.sheetnames else ({}, {})
            return cache[name]

        for title, has, labels in overview_blocks(wb["Overview"]):
            tl = norm(title)

            if tl.startswith(PILLAR3_BLOCK):
                for key, years in labels.items():
                    sheet = next((s for s in wb.sheetnames if norm(s) == key), None)
                    if sheet is None:
                        skipped_lbl += 1
                        continue
                    _, srows = detail(sheet)
                    # Take the first cell in each year that is PRINTED AS A
                    # PERCENTAGE, not simply the sheet's first row: on the
                    # Leverage Ratio, LCR and NSFR sheets the first row is the
                    # exposure/HQLA/funding measure, so a first-row rule
                    # compares a ratio against a £'000 amount.
                    flat = {}
                    for yrs in srows.values():
                        for y, v in yrs.items():
                            if "%" in str(v) and y not in flat:
                                flat[y] = v
                    for y, ov in years.items():
                        a, b = num(ov), num(flat.get(y))
                        if a is None or b is None:
                            skipped_lbl += 1
                            continue
                        compared += 1
                        if abs(a - b) > max(abs(b) * TOL, 1e-9):
                            valbreak.append((bank, title, key, y, ov, flat.get(y)))
                continue

            skey = next((k for k in BLOCK_TO_SHEET if tl.startswith(k)), None)
            if skey is None:
                continue
            sname = BLOCK_TO_SHEET[skey]
            shas, srows = detail(sname)

            for y in sorted(has, reverse=True):
                if y not in shas:
                    continue
                if not has[y] and shas[y]:
                    lag.append((bank, title, sname, y))
                elif has[y] and not shas[y]:
                    ahead.append((bank, title, sname, y))

            for key, years in labels.items():
                if key not in srows:
                    skipped_lbl += 1
                    continue
                for y, ov in years.items():
                    a, b = num(ov), num(srows[key].get(y))
                    if a is None or b is None:
                        skipped_lbl += 1
                        continue
                    compared += 1
                    if abs(a - b) > max(abs(b) * TOL, 1e-9):
                        valbreak.append((bank, title, key, y, ov, srows[key].get(y)))
        wb.close()

    print(f"scanned {banks} Overview sheet(s)\n")

    print(f"A. Overview block EMPTY where its own detail sheet has figures  "
          f"({len(lag)} block-year(s))")
    if lag:
        print(f"   {'bank':<36} {'year':<7} {'Overview block':<34} vs sheet")
        for bank, title, sname, y in sorted(lag, key=lambda r: (r[0], -r[3])):
            print(f"   {bank:<36} FY{y}   {title[:34]:<34} {sname}")
    print()

    print(f"B. Overview block has a figure where the detail sheet has none  "
          f"({len(ahead)} block-year(s))")
    if ahead:
        print(f"   {'bank':<36} {'year':<7} {'Overview block':<34} vs sheet")
        for bank, title, sname, y in sorted(ahead, key=lambda r: (r[0], -r[3])):
            print(f"   {bank:<36} FY{y}   {title[:34]:<34} {sname}")
    print()

    print(f"C. Label matched but the VALUE differs  ({len(valbreak)} cell(s))")
    if valbreak:
        print(f"   {'bank':<30} {'year':<7} {'row':<34} {'Overview':>16} {'sheet':>16}")
        for bank, title, key, y, ov, sv in sorted(valbreak, key=lambda r: (r[0], -r[3])):
            print(f"   {bank:<30} FY{y}   {key[:34]:<34} {str(ov):>16} {str(sv):>16}")
    print()

    print(f"reach: {compared} value comparison(s) made, {skipped_lbl} skipped "
          f"(label not matched, or non-numeric on one side)")
    return 1 if (lag or ahead or valbreak) else 0


if __name__ == "__main__":
    sys.exit(main())
