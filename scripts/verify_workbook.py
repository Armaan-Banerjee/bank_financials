"""
Generic post-build sanity checker for a "<BANK> FINANCIALS.xlsx" workbook -
so every bank build doesn't need its own hand-written openpyxl verification
snippet. Structural checks work on ANY bank because they key off font
styling (bold = TOTAL/SECTION, per bank_workbook.py's own conventions), not
label text - so they don't need per-bank tuning.

Usage:
    python3 verify_workbook.py "banks/<BANK> FINANCIALS.xlsx"

Checks performed:
    1. Sheet list + count (expect 13: Overview, Cash Flow Statement, 11 Pillar 3
       sheets; 14 when an auxiliary "Interim Pillar 3" sheet is present)
    2. Overview sheet chart count (expect 2)
    3. Cash Flow Statement: for every contiguous run of plain DATA rows that is
       immediately followed by a bold TOTAL row (the standard SECTION/DATA*/TOTAL
       block shape from add_cash_flow_sheet), verify the DATA rows sum to that
       TOTAL, per year column. This is a fully generic structural check - it
       doesn't know or care what the rows are called.
    4. Prints every TOTAL row's values per year, so the "tail" reconciliation
       (net change / opening / closing, which varies bank-to-bank - e.g. extra
       FX lines) can be eyeballed quickly rather than re-deriving it by hand.

This does NOT replace judgment for anything label-dependent or bank-specific
(e.g. an FX translation plug row, a duplicate "comprise" breakdown section) -
it flags what it can verify unambiguously and prints the rest for a human/
fork to check by eye.
"""
import sys

import openpyxl


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    path = sys.argv[1]
    wb = openpyxl.load_workbook(path, data_only=True)

    print("=== Sheets ===")
    print(f"{len(wb.sheetnames)} sheets: {wb.sheetnames}")
    has_interim = "Interim Pillar 3" in wb.sheetnames
    expected_sheets = 14 if has_interim else 13
    if len(wb.sheetnames) != expected_sheets:
        print(f"  !! expected {expected_sheets} sheets, got {len(wb.sheetnames)}")

    if has_interim:
        interim = wb["Interim Pillar 3"]
        expected_headers = [
            "Period", "Disclosure type", "Metric", "Value", "Unit",
            "Basis", "Source document", "Page / table",
        ]
        headers = [interim.cell(row=4, column=c).value for c in range(1, 9)]
        print("\n=== Interim Pillar 3 structure ===")
        if headers == expected_headers:
            print(f"Format: long; headers: {headers}")
            data_rows = 0
            missing_fields = []
            hyperlink_count = 0
            for r in range(5, interim.max_row + 1):
                # The helper's merged note row has no value in column B; data rows
                # always have a disclosure type there.
                if interim.cell(row=r, column=2).value in (None, ""):
                    break
                data_rows += 1
                if any(interim.cell(row=r, column=c).value in (None, "") for c in (1, 2, 3, 7, 8)):
                    missing_fields.append(r)
                if interim.cell(row=r, column=7).hyperlink:
                    hyperlink_count += 1
            print(f"Data rows: {data_rows}; source hyperlinks: {hyperlink_count}")
            if not data_rows:
                print("  !! Interim Pillar 3 sheet contains no data rows")
            if missing_fields:
                print(f"  !! required fields missing on rows: {missing_fields}")
        else:
            # Wide-format check - previously nested INSIDE the long-format
            # `if headers == expected_headers:` branch above, so it never
            # ran for any real workbook (every interim sheet built since the
            # 2026-08-29 "wide interim-layout conversion" uses this format,
            # not the long one) - confirmed empirically: the verifier printed
            # nothing at all under "Interim Pillar 3 structure" for every
            # wide-format workbook. Made a real `else` sibling instead, and
            # `wide_headers` is now only referenced in the branch where it's
            # actually assigned (it used to be read unconditionally right
            # after an `if missing_fields: ... else: wide_headers = ...`,
            # which would raise UnboundLocalError on any long-format sheet
            # with a missing field).
            wide_headers = [interim.cell(row=4, column=c).value for c in range(1, interim.max_column + 1)]
            if len(wide_headers) < 4 or wide_headers[:3] != ["Metric", "Unit", "Basis"]:
                print(f"Headers: {headers}")
                print(f"  !! expected long headers {expected_headers} or wide headers beginning with Metric/Unit/Basis")
            else:
                period_count = len(wide_headers) - 3
                metric_rows = 0
                value_cells = 0
                value_links = 0
                source_register_row = next(
                    (r for r in range(5, interim.max_row + 1)
                     if interim.cell(row=r, column=1).value == "Source register"),
                    None,
                )
                metric_end = source_register_row or interim.max_row + 1
                for r in range(5, metric_end):
                    if interim.cell(row=r, column=1).value in (None, ""):
                        continue
                    metric_rows += 1
                    for c in range(4, interim.max_column + 1):
                        cell = interim.cell(row=r, column=c)
                        if cell.value not in (None, ""):
                            value_cells += 1
                            if cell.hyperlink:
                                value_links += 1
                register_links = 0
                register_rows = 0
                if source_register_row:
                    register_header = [interim.cell(row=source_register_row + 1, column=c).value for c in range(1, 5)]
                    if register_header != ["Period", "Disclosure type", "Source document", "Page / table"]:
                        print(f"  !! invalid source-register headers: {register_header}")
                    for r in range(source_register_row + 2, interim.max_row + 1):
                        if interim.cell(row=r, column=1).value in (None, ""):
                            break
                        register_rows += 1
                        if interim.cell(row=r, column=3).hyperlink:
                            register_links += 1
                print(f"Format: wide; metrics: {metric_rows}; periods: {period_count}; populated values: {value_cells}; value hyperlinks: {value_links}; source rows: {register_rows}; source hyperlinks: {register_links}")
                if not metric_rows or not period_count:
                    print("  !! wide Interim Pillar 3 sheet contains no metric/period matrix")
                if not source_register_row or not register_rows:
                    print("  !! wide Interim Pillar 3 sheet contains no source register")

    if "Overview" in wb.sheetnames:
        ov = wb["Overview"]
        n_charts = len(ov._charts)
        print(f"\n=== Overview charts ===\n{n_charts} charts")
        if n_charts != 2:
            print("  !! expected 2 charts (cash flow bar + ratios line)")

    if "Cash Flow Statement" not in wb.sheetnames:
        print("\nNo 'Cash Flow Statement' sheet found - skipping reconciliation checks.")
        return
    ws = wb["Cash Flow Statement"]

    # Locate the header row (first row with >1 non-empty cell after the title/subtitle)
    header_row = None
    for r in range(1, 6):
        vals = [ws.cell(row=r, column=c).value for c in range(1, ws.max_column + 1)]
        if sum(1 for v in vals if v not in (None, "")) > 1:
            header_row = r
            break
    if header_row is None:
        print("\nCouldn't locate the header row - skipping reconciliation checks.")
        return
    ncols = ws.max_column
    years = [ws.cell(row=header_row, column=c).value for c in range(2, ncols + 1)]
    print(f"\n=== Cash Flow Statement structure (header row {header_row}) ===")
    print("Years:", years)

    def is_bold(row, col):
        cell = ws.cell(row=row, column=col)
        return bool(cell.font and cell.font.bold)

    def row_kind(r):
        a_bold = is_bold(r, 1)
        b_val = ws.cell(row=r, column=2).value
        if not a_bold:
            return "DATA" if ws.cell(row=r, column=1).value else "BLANK"
        # bold col A: SECTION has no data-column values written; TOTAL does
        any_data = any(ws.cell(row=r, column=c).value is not None for c in range(2, ncols + 1))
        return "TOTAL" if any_data else "SECTION"

    # find the last populated row before the (merged) source-citation cell
    last_row = header_row
    for r in range(header_row + 1, ws.max_row + 1):
        if ws.cell(row=r, column=1).value in (None, ""):
            break
        last_row = r

    print("\n=== TOTAL rows (for manual/tail reconciliation) ===")
    totals = []
    run = []  # pending DATA rows since the last SECTION/TOTAL
    block_start_r = None
    checks_run = 0
    checks_passed = 0
    for r in range(header_row + 1, last_row + 1):
        kind = row_kind(r)
        label = ws.cell(row=r, column=1).value
        if kind == "SECTION":
            run = []
        elif kind == "DATA":
            run.append(r)
        elif kind == "TOTAL":
            vals = [ws.cell(row=r, column=c).value for c in range(2, ncols + 1)]
            totals.append((label, vals))
            print(f"  row {r}: {label!r} -> {vals}")
            if run:
                checks_run += 1
                ok = True
                mismatches = []
                for ci, y in enumerate(years, start=2):
                    total_v = ws.cell(row=r, column=ci).value
                    data_sum = sum(
                        (ws.cell(row=dr, column=ci).value or 0) for dr in run
                    )
                    if total_v is not None and abs((total_v or 0) - data_sum) > 0.05:
                        ok = False
                        mismatches.append((y, data_sum, total_v))
                if ok:
                    checks_passed += 1
                else:
                    print(f"    !! block {run}->row {r} does NOT reconcile: {mismatches}")
            run = []

    print(f"\n=== Block reconciliation summary ===")
    print(f"{checks_passed}/{checks_run} DATA-block -> TOTAL checks passed"
          f"{' (all clean)' if checks_passed == checks_run else '  !! see mismatches above'}")
    print("\nReview the TOTAL rows above by eye for the tail chain (net change / "
          "opening / closing, incl. any FX or other adjustment lines) - that part "
          "is bank-specific and isn't auto-verified.")


if __name__ == "__main__":
    main()
