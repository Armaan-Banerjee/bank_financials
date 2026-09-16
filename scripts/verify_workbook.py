"""
Generic post-build sanity checker for a "<BANK> FINANCIALS.xlsx" workbook -
so every bank build doesn't need its own hand-written openpyxl verification
snippet. Structural checks work on ANY bank because they key off font
styling (bold = TOTAL/SECTION, per bank_workbook.py's own conventions), not
label text - so they don't need per-bank tuning.

Usage:
    python3 verify_workbook.py "banks/<BANK> FINANCIALS.xlsx"

Checks performed:
    1. Sheet list + count. Base shape is 13 (Overview, Cash Flow Statement,
       11 Pillar 3 sheets). The expected count is COMPUTED from what is
       actually present rather than assumed, so one checker serves workbooks
       at different stages of two rollouts: base, plus however many of the 5
       ST- statement sheets exist (Balance Sheet, Profit & Loss, Statement of
       Changes in Equity, Asset Quality, RWA Breakdown - see
       wayfinder/statements/map.md, now complete for all 145 banks), plus 1
       for an auxiliary "Interim Pillar 3" sheet where the bank publishes a
       half-year Pillar 3 (13 banks do), plus 1 for a "KM1 Key Metrics" sheet
       (the KM1- rollout, still in progress). A workbook may therefore
       legitimately have anywhere from 18 to 20 sheets today. Also asserts
       the KM1 sheet's locked placement: immediately before "CET1 Capital".
    2. Overview sheet chart count - expected is derived the same way: 1 bar
       chart per money block sheet present (Balance Sheet/Profit & Loss/
       Statement of Changes in Equity/Cash Flow Statement) + 1 ratios line
       chart if any Pillar 3 metric sheet is present. This is a heuristic
       (a block's totals could have been passed empty even if its sheet
       exists) so a mismatch is printed as informational, not asserted.
    3. For every statement sheet sharing the standard SECTION/DATA*/TOTAL
       year-column block shape from bank_workbook.py's `_add_statement_sheet`
       - Cash Flow Statement, Balance Sheet, Profit & Loss, Asset Quality,
       RWA Breakdown - verify every contiguous run of plain DATA rows
       immediately followed by a bold TOTAL row sums to that TOTAL, per year
       column. This is a fully generic structural check - it doesn't know or
       care what the rows are called, so it runs unchanged whichever of the
       5 sheets are present in a given workbook. (Statement of Changes in
       Equity is deliberately excluded: it's a chronological roll-forward,
       not this year-column shape.) Originally only ran against Cash Flow
       Statement (this check predates the other 4 ST- sheets) - widened
       2026-09-08 after a bug sweep found it was the exact class of check
       that would have caught this project's real Close Brothers/Aldermore
       double-counting bug had it run against a Balance Sheet or Asset
       Quality sheet.
    4. Prints every TOTAL row's values per year, so the "tail" reconciliation
       (net change / opening / closing, which varies bank-to-bank - e.g. extra
       FX lines) can be eyeballed quickly rather than re-deriving it by hand.
    5. Where the workbook has a "KM1 Key Metrics" sheet (the KM1- wayfinder
       map, see wayfinder/km1/map.md), cross-checks it against the 11
       single-metric Pillar 3 sheets. KM1 rows 1-7, 14, 17 and 20 restate
       figures that those sheets also carry, transcribed separately from the
       same source table, so a disagreement is usually a transcription slip.
       It caught a real GBP175k error in Monzo's FY2026 balance sheet on its
       first run.

       A reported disagreement is NOT automatically a bug. It is either a
       transcription error, or a genuine divergence - a different disclosed
       basis, a restated comparative, point-in-time vs average LCR - which
       belongs in the sheet note, naming both figures and both editions.
       Never silence one by editing a figure so the two sides agree.

       Unit handling is the fiddly part, because the two sheet types declare
       units in different places. A metric sheet has ONE unit for the whole
       sheet, on its own row above the header, usually beside the reporting
       basis ("Bank solo basis, GBPm"). A KM1 sheet cannot: it is the one
       sheet that mixes GBP'000 amounts and % ratios down a single column, so
       it declares units per ROW - in the row label, or once on the section
       divider above a block ("Available own funds (amounts, GBP million)").
       Resolution order for a KM1 cell is row label, then section divider,
       then column header, then as-printed. It deliberately never falls back
       to a sheet-level unit: the cell in that position on a KM1 sheet holds
       a prose note, and prose lies - Bank of Beirut's reads "Amounts in
       plain pounds - NOT GBP'000 or GBPm", which a substring search reads as
       GBPm and then scales every amount by a million.

       Two classes are deliberately excluded rather than compared. Rows whose
       label declares more than one unit (Cynergy prints FY2023 in GBP'000
       beside FY2022/FY2021 in plain pounds) have a per-COLUMN unit that one
       row scale cannot express - they are reported as "NOT cross-checked,
       check by eye". And fully-loaded twins ("Tier 1 capital as if IFRS 9
       transitional arrangements had not been applied", four of which HSBC UK
       prints) are a different disclosure from the transitional figure the
       metric sheets carry, so matching them manufactures a disagreement out
       of two correct numbers.

This does NOT replace judgment for anything label-dependent or bank-specific
(e.g. an FX translation plug row, a duplicate "comprise" breakdown section) -
it flags what it can verify unambiguously and prints the rest for a human/
fork to check by eye.
"""

import os
import re
import sys

import openpyxl

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import PILLAR3_SHEET_NAMES


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    path = sys.argv[1]
    wb = openpyxl.load_workbook(path, data_only=True)

    print("=== Sheets ===")
    print(f"{len(wb.sheetnames)} sheets: {wb.sheetnames}")
    has_interim = "Interim Pillar 3" in wb.sheetnames
    st_sheet_names = [
        "Balance Sheet",
        "Profit & Loss",
        "Statement of Changes in Equity",
        "Asset Quality",
        "RWA Breakdown",
    ]
    st_sheets_present = [n for n in st_sheet_names if n in wb.sheetnames]
    # KM1 rollout (see wayfinder/km1/map.md): the bank's own published UK KM1
    # template, optional per bank while the rollout is in progress.
    has_km1 = "KM1 Key Metrics" in wb.sheetnames
    expected_sheets = (
        13 + len(st_sheets_present) + (1 if has_interim else 0) + (1 if has_km1 else 0)
    )
    if len(wb.sheetnames) != expected_sheets:
        print(
            f"  !! expected {expected_sheets} sheets "
            f"(13 base + {len(st_sheets_present)} ST- sheets {st_sheets_present} "
            f"+ {1 if has_interim else 0} interim + {1 if has_km1 else 0} KM1), "
            f"got {len(wb.sheetnames)}"
        )
    if has_km1:
        km1_idx = wb.sheetnames.index("KM1 Key Metrics")
        # Locked placement: immediately before the first Pillar 3 metric sheet.
        if wb.sheetnames[km1_idx + 1 : km1_idx + 2] != ["CET1 Capital"]:
            print(
                "  !! 'KM1 Key Metrics' must sit immediately before 'CET1 Capital'; "
                f"it is followed by {wb.sheetnames[km1_idx + 1 : km1_idx + 2]}"
            )
        check_km1_against_metric_sheets(wb)

    if has_interim:
        interim = wb["Interim Pillar 3"]
        expected_headers = [
            "Period",
            "Disclosure type",
            "Metric",
            "Value",
            "Unit",
            "Basis",
            "Source document",
            "Page / table",
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
                if any(
                    interim.cell(row=r, column=c).value in (None, "")
                    for c in (1, 2, 3, 7, 8)
                ):
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
            wide_headers = [
                interim.cell(row=4, column=c).value
                for c in range(1, interim.max_column + 1)
            ]
            if len(wide_headers) < 4 or wide_headers[:3] != ["Metric", "Unit", "Basis"]:
                print(f"Headers: {headers}")
                print(
                    f"  !! expected long headers {expected_headers} or wide headers beginning with Metric/Unit/Basis"
                )
            else:
                period_count = len(wide_headers) - 3
                metric_rows = 0
                value_cells = 0
                value_links = 0
                source_register_row = next(
                    (
                        r
                        for r in range(5, interim.max_row + 1)
                        if interim.cell(row=r, column=1).value == "Source register"
                    ),
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
                    register_header = [
                        interim.cell(row=source_register_row + 1, column=c).value
                        for c in range(1, 5)
                    ]
                    if register_header != [
                        "Period",
                        "Disclosure type",
                        "Source document",
                        "Page / table",
                    ]:
                        print(
                            f"  !! invalid source-register headers: {register_header}"
                        )
                    for r in range(source_register_row + 2, interim.max_row + 1):
                        if interim.cell(row=r, column=1).value in (None, ""):
                            break
                        register_rows += 1
                        if interim.cell(row=r, column=3).hyperlink:
                            register_links += 1
                print(
                    f"Format: wide; metrics: {metric_rows}; periods: {period_count}; populated values: {value_cells}; value hyperlinks: {value_links}; source rows: {register_rows}; source hyperlinks: {register_links}"
                )
                if not metric_rows or not period_count:
                    print(
                        "  !! wide Interim Pillar 3 sheet contains no metric/period matrix"
                    )
                if not source_register_row or not register_rows:
                    print(
                        "  !! wide Interim Pillar 3 sheet contains no source register"
                    )

    if "Overview" in wb.sheetnames:
        ov = wb["Overview"]
        n_charts = len(ov._charts)
        money_block_sheets = [
            "Balance Sheet",
            "Profit & Loss",
            "Statement of Changes in Equity",
            "Cash Flow Statement",
        ]
        expected_bar_charts = sum(1 for n in money_block_sheets if n in wb.sheetnames)
        pillar3_present = any(n in wb.sheetnames for n in PILLAR3_SHEET_NAMES)
        expected_charts = expected_bar_charts + (1 if pillar3_present else 0)
        print(
            f"\n=== Overview charts ===\n{n_charts} charts (heuristic expectation: {expected_charts} "
            f"= {expected_bar_charts} money-block bar chart(s) + {1 if pillar3_present else 0} ratios line chart)"
        )
        if n_charts != expected_charts:
            print(
                "  (informational, not necessarily wrong - a block's totals could have been passed empty "
                "even with its sheet present)"
            )

    # Sheets sharing the standard SECTION/DATA*/TOTAL year-column block shape
    # from bank_workbook.py's `_add_statement_sheet` - Statement of Changes
    # in Equity is deliberately excluded (chronological roll-forward, not
    # this shape).
    reconciliation_sheet_names = [
        "Cash Flow Statement",
        "Balance Sheet",
        "Profit & Loss",
        "Asset Quality",
        "RWA Breakdown",
    ]
    any_reconciliation_sheet = any(n in wb.sheetnames for n in reconciliation_sheet_names)
    if not any_reconciliation_sheet:
        print(
            "\nNo statement sheet with the standard SECTION/DATA/TOTAL shape found - "
            "skipping reconciliation checks."
        )
        return
    for sheet_name in reconciliation_sheet_names:
        if sheet_name in wb.sheetnames:
            check_statement_sheet(wb[sheet_name], sheet_name)


# KM1 template row number -> the Pillar 3 metric sheet that must carry the
# same figure. Only rows with an unambiguous one-to-one metric sheet are
# listed; buffer and SREP rows have no metric sheet of their own.
#
# Each entry also carries the words the row's own label must contain. Banks
# mis-number rows - Bank of China (UK) prints template row 16 as "6" in every
# edition - so a row number alone is not enough to say what a row is. If the
# label disagrees with the number, the number is not trusted.
KM1_ROW_TO_METRIC_SHEET = {
    "1": ("CET1 Capital", ("common equity tier 1", "cet1")),
    "2": ("Tier 1 Capital", ("tier 1 capital",)),
    # "capital" alone was too loose to be a disagreement detector here. Banks
    # that filed under the EARLIER EU/EBA KM1 template number their rows
    # differently: Santander UK's FY2021 and FY2020 ACRMDs print "3  Tier 1
    # capital" (that template's row 3), which contains "capital" and so was
    # matched to the Total Capital sheet and reported as a 1,816m disagreement
    # between two correct figures. The words below identify row 3 of the UK
    # template without claiming a Tier 1 or CET1 row.
    "3": ("Total Capital", ("total capital", "total regulatory capital", "total own funds")),
    # "rwea" is needed as well as "rwa": the UK template's own term is Risk
    # Weighted Exposure Amount, and banks that print row 4 as "Total RWEAs"
    # (Secure Trust Bank, FY2025-FY2022) matched none of the other three
    # tokens - "rwa" is not a substring of "rweas" - so those cells were
    # silently not cross-checked rather than reported as disagreeing. A row
    # NUMBERED 4 whose label says RWEA is unambiguously the total.
    "4": ("Total RWAs", ("risk-weight", "risk weight", "rwa", "rwea")),
    "5": ("CET1 Ratio", ("ratio",)),
    "6": ("Tier 1 Ratio", ("ratio",)),
    "7": ("Total Capital Ratio", ("ratio",)),
    "14": ("Leverage Ratio", ("leverage",)),
    "17": ("LCR", ("liquidity coverage", "lcr")),
    "20": ("NSFR", ("nsfr", "net stable funding")),
}


def _sheet_header_row(ws):
    for r in range(1, 6):
        vals = [ws.cell(row=r, column=c).value for c in range(1, ws.max_column + 1)]
        if sum(1 for v in vals if v not in (None, "")) > 1:
            return r
    return None


def _year_key(label):
    """'FY2025 (£'000)' -> 'FY2025'. Year labels carry the unit (and sometimes
    an entity tag like '(MBHG)'), which differs between sheets, so match on the
    FY token alone."""
    if not isinstance(label, str):
        return None
    m = re.search(r"FY\d{4}", label)
    return m.group(0) if m else None


# Banks abbreviate "million" every way there is: "£m", "£'m", "$ m", "£ mn",
# "£ mil", "£ millions". FCE Bank writes "£ mil", which a bare `m\b` misses
# because the word boundary lands after "mil", not after "m". The abbreviation
# is the bank's choice and the checker has to read all of them - rewording a
# delivered sheet to suit the parser would be normalising the source.
_MILLION_RE = r"[£$€]\s*'?m(?:n|m|il|illion)?s?\b|\bmillions?\b"
_THOUSAND_RE = r"[£$€]\s*'?k\b|\bthousands?\b"


def _unit_scale(label):
    """Multiplier that converts a cell carrying this label to units of 1. KM1
    is usually in £'000 while a metric sheet may be in £m (or vice versa), so a
    like-for-like comparison has to normalise first.

    Returns None when the label carries no unit token at all, so callers can
    fall back to another place on the sheet rather than assuming units of 1.
    """
    if not isinstance(label, str):
        return None
    low = label.lower()
    if re.search(r"bn\b|billion", low):
        return 1e9
    # "£m", "£'m", "$ m", "£ mil", "£ million", "(amounts, £ million)".
    if re.search(_MILLION_RE, low):
        return 1e6
    if "'000" in low or "000s" in low or re.search(_THOUSAND_RE, low):
        return 1e3
    # An EXPLICIT bare-currency declaration means as-printed, and is different
    # from saying nothing at all. Plain pounds has no scale token, so without
    # this a block published in single pounds could not declare itself, and
    # would inherit a scale from whatever block precedes it. C. Hoare prints
    # its FY2022 edition in single pounds and later editions in £'000.
    if re.search(r"\(\s*[£$€]\s*[,)]|\bin\s+[£$€]\b|\b(single|plain)\s+pounds\b", low):
        return 1.0
    return None


def _distinct_unit_tokens(label):
    """How many DIFFERENT unit scales one label declares. Cynergy's KM1 prints
    FY2023 in £'000 beside FY2022/FY2021 in plain pounds and says so in the row
    label ("[FY2023 £'000; FY2022/FY2021 £]"); the unit is then per-COLUMN and
    a single row scale cannot express it, so the comparison must be skipped
    rather than guessed at."""
    if not isinstance(label, str):
        return 0
    low = label.lower()
    # A label that names specific YEARS beside a unit is spelling out that the
    # unit changes per column - Cynergy's "[FY2023 £'000; FY2022/FY2021 £]".
    # One row scale cannot express that, whether or not the two units it names
    # both parse as scale tokens (plain pounds has no token at all).
    if re.search(r"fy\s?\d{4}", low) and re.search(r"[£$€]|\bmillions?\b|'000", low):
        return 2
    found = set()
    if re.search(r"bn\b|billion", low):
        found.add(1e9)
    if re.search(_MILLION_RE, low):
        found.add(1e6)
    if "'000" in low or "000s" in low or re.search(_THOUSAND_RE, low):
        found.add(1e3)
    return len(found)


def _sheet_unit_scale(ws, header_row):
    """A metric sheet declares its unit on its own row, between the title and
    the column header, and usually pairs it with the reporting basis - "£m",
    "Bank solo basis, £m", "Consolidated (Group) basis, £'000". Read it there.

    Only valid for a METRIC sheet. A KM1 sheet has no sheet-level unit by
    design (see wayfinder/km1/map.md: it is the one sheet that mixes £'000
    amounts and % ratios down a single column), so its equivalent cell holds a
    prose note instead - and prose lies. Bank of Beirut's reads "Amounts in
    plain pounds (£) - NOT £'000 or £m", which a substring search reads as £m
    and then scales every amount on the sheet by a million.
    """
    for r in range(1, (header_row or 3)):
        s = _unit_scale(ws.cell(row=r, column=1).value)
        if s is not None:
            return s
    return 1.0


def _km1_section_scale(ws, row, header_row):
    """Walk UP to the nearest preceding SECTION divider and read its unit.

    A KM1 sheet mixes units down one column, so it cannot declare one unit for
    the whole sheet - but banks don't always repeat the unit on every row
    either. Citibank UK puts it on the section divider once ("Available own
    funds (amounts, £ million)") and leaves the rows beneath it bare ("1
    Common Equity Tier 1 (CET1) capital"). A divider is a row with a label and
    no values in the year columns.
    """
    for r in range(row - 1, (header_row or 1), -1):
        lab = ws.cell(row=r, column=1).value
        if not isinstance(lab, str) or not lab.strip():
            continue
        is_divider = all(
            ws.cell(row=r, column=c).value in (None, "")
            for c in range(2, ws.max_column + 1)
        )
        if not is_divider:
            continue
        # Take the nearest preceding divider that says ANYTHING about units,
        # walking past ones that are silent. Guaranty Trust declares "Available
        # Own Funds (Amounts in GBP '000')" once and leaves its later dividers
        # ("Risk-Weighted Exposure Amount") bare, so its RWA row depends on
        # reaching back past a silent divider.
        #
        # The risk in walking is that a unit leaks downward across caption
        # blocks in a two-unit sheet (rule 17). That is why an explicit bare-
        # currency declaration counts as a declaration of scale 1 in
        # _unit_scale: a plain-pounds block can then stop the walk on its own
        # divider. A block whose rows each carry their own unit - which is the
        # more robust way to build one - never reaches this function at all.
        s = _unit_scale(lab)
        if s is not None:
            return s
    return None


def _km1_row_scale(ws, row, col, header_row):
    """Resolve the unit for ONE KM1 cell, in the order the sheets actually use
    it: the row label ("1  CET1 capital (£'000)"), then the section divider
    above it, then the column header, then any sheet-level unit row."""
    for v in (
        ws.cell(row=row, column=1).value,
        ws.cell(row=header_row, column=col).value if header_row else None,
    ):
        s = _unit_scale(v)
        if s is not None:
            return s
    s = _km1_section_scale(ws, row, header_row)
    if s is not None:
        return s
    # Deliberately NOT _sheet_unit_scale: a KM1 sheet has no sheet-level unit,
    # only a prose note that would be misread. Undeclared means as-printed.
    return 1.0


def _numeric(v):
    """Coerce a cell to a float for comparison. Ratios are stored as printed
    strings ('15.45%', '14.5 %', '1,057.8%'); text like 'Not publicly
    disclosed' returns None."""
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        s = v.strip().replace(",", "").replace(" ", "")
        pct = s.endswith("%")
        if pct:
            s = s[:-1]
        try:
            return float(s)
        except ValueError:
            return None
    return None


# Some banks print the KM1 template with no row numbers at all (Europe Arab
# Bank heads it "Key metrics" and numbers nothing), so the row-number lookup
# above finds nothing. Fall back to matching the row's own label.
KM1_LABEL_TO_METRIC_SHEET = [
    ("common equity tier 1 ratio", "CET1 Ratio"),
    ("common equity tier 1 (cet1) ratio", "CET1 Ratio"),
    ("common equity tier 1 (cet1) capital", "CET1 Capital"),
    ("tier 1 ratio", "Tier 1 Ratio"),
    ("tier 1 capital", "Tier 1 Capital"),
    ("total capital ratio", "Total Capital Ratio"),
    ("total capital", "Total Capital"),
    ("total risk-weighted exposure amount", "Total RWAs"),
    ("total rwa", "Total RWAs"),
    ("leverage ratio excluding claims on central banks", "Leverage Ratio"),
    ("liquidity coverage ratio", "LCR"),
    ("nsfr ratio", "NSFR"),
    # Griffin and GTBank UK spell row 20 out in full instead of "NSFR ratio".
    ("net stable funding ratio", "NSFR"),
]


def _normalise_km1_label(label):
    """Lower-case a KM1 row label and strip the punctuation banks sprinkle
    through it, so the prefix table above matches on words. GTBank UK prints
    'Common Equity Tier 1 ("CET1") capital' with quotation marks round the
    abbreviation and Griffin prints 'Net stable funding ratio' in sentence
    case; neither matched before. Double spaces are collapsed too, since some
    banks pad the label out to align a column."""
    low = label.strip().lower().rstrip(":")
    for ch in ('"', "“", "”", "'", "‘", "’"):
        low = low.replace(ch, "")
    return " ".join(low.split())


def _metric_sheet_for(label):
    """Which Pillar 3 metric sheet, if any, must carry this KM1 row's figure.
    Prefers the template row number; falls back to the label for the banks
    that print the template unnumbered."""
    low = _normalise_km1_label(label)
    # The template carries FULLY-LOADED twins of several rows ("Tier 1 capital
    # as if IFRS 9 transitional arrangements had not been applied"). They are a
    # different disclosure from the transitional figure the metric sheets
    # carry, and HSBC UK prints four of them, so matching them to the plain
    # sheet manufactures a disagreement out of two correct numbers.
    if re.search(r"as if|had not been applied|fully[- ]loaded|pre[- ]ifrs", low):
        return None
    parts = label.split()
    if parts:
        by_num = KM1_ROW_TO_METRIC_SHEET.get(parts[0])
        if by_num:
            sheet, keywords = by_num
            if any(k in low for k in keywords):
                return sheet
            # Number and label disagree: the number is wrong (or belongs to a
            # row this mapping does not cover). Fall through to the label.
    # Longest prefix wins, so "tier 1 ratio" never shadows "total capital ratio".
    best = None
    for prefix, sheet in KM1_LABEL_TO_METRIC_SHEET:
        if low.startswith(prefix) and (best is None or len(prefix) > best[0]):
            best = (len(prefix), sheet)
    return best[1] if best else None


def _currency(*texts):
    """'EUR'/'GBP'/'USD' if any of these strings names one, else None. A KM1
    sheet left in the bank's reporting currency cannot be compared cell-for-
    cell against metric sheets converted to sterling.

    EARLIEST MENTION WINS, not a fixed EUR>USD>GBP priority. The texts are
    passed most-specific-first (a unit header, then the subtitle, then row
    labels), and a unit header names the sheet's own currency before it names
    any other: Goldman Sachs International Bank's metric sheets are headed
    "£m (conv. from USD)", which is a sterling sheet whose provenance happens
    to mention dollars. Under a fixed priority that header read as USD and the
    GBP-vs-USD break went undetected, so every amount row was compared across
    a currency break and reported as a mismatch."""
    blob = " ".join(t for t in texts if isinstance(t, str))
    first = None
    for ccy, tokens in (("EUR", ("€", "EUR")), ("USD", ("$", "USD")), ("GBP", ("£", "GBP"))):
        for tok in tokens:
            i = blob.find(tok)
            if i != -1 and (first is None or i < first[0]):
                first = (i, ccy)
    return first[1] if first else None


def _decimals(v):
    """Decimal places as PRINTED ('14.2%' -> 1, '14.15%' -> 2, '523%' -> 0)."""
    s = str(v).strip().replace(",", "").replace(" ", "").rstrip("%")
    return len(s.split(".")[1]) if "." in s else 0


def check_km1_against_metric_sheets(wb):
    """Every figure the KM1 sheet carries for rows 1-7, 14, 17 and 20 also
    appears on a dedicated Pillar 3 metric sheet in the same workbook. They are
    transcribed separately, from the same source table, so a disagreement is
    almost always a transcription slip in one of the two."""
    ws = wb["KM1 Key Metrics"]
    hr = _sheet_header_row(ws)
    if hr is None:
        print("\nCouldn't locate the KM1 header row - skipping KM1 cross-check.")
        return
    km1_years = {}  # column index -> FY token. The scale is per-ROW, not per
    # column: a KM1 column mixes £'000 amounts and % ratios, so the unit lives
    # in the row label and is resolved inside the row loop below.
    for c in range(2, ws.max_column + 1):
        fy = _year_key(ws.cell(row=hr, column=c).value)
        if fy:
            km1_years[c] = fy

    print("\n=== KM1 vs Pillar 3 metric sheets ===")
    checks = mismatches = 0
    skipped_mixed_unit = []
    for r in range(hr + 1, ws.max_row + 1):
        label = ws.cell(row=r, column=1).value
        if not isinstance(label, str):
            continue
        rownum = label.split()[0] if label.split() else ""
        sheet_name = _metric_sheet_for(label)
        if sheet_name is None or sheet_name not in wb.sheetnames:
            continue
        # Per-COLUMN units (Cynergy: FY2023 in £'000, FY2022/FY2021 in plain
        # pounds) can't be resolved by a single row scale. Say so and move on,
        # rather than emitting disagreements that are pure unit artefacts.
        if _distinct_unit_tokens(label) > 1:
            skipped_mixed_unit.append(f"{label.split('[')[0].strip()[:56]!r} ({sheet_name})")
            continue
        mws = wb[sheet_name]
        mhr = _sheet_header_row(mws)
        if mhr is None:
            continue
        # A metric sheet is in one unit throughout, declared on its unit row.
        m_sheet_scale = _sheet_unit_scale(mws, mhr)
        m_cols = {}
        for c in range(2, mws.max_column + 1):
            fy = _year_key(mws.cell(row=mhr, column=c).value)
            if fy:
                hdr_scale = _unit_scale(mws.cell(row=mhr, column=c).value)
                m_cols[fy] = (c, hdr_scale if hdr_scale is not None else m_sheet_scale)
        # A metric sheet may carry several bases (e.g. Leverage Ratio
        # excluding vs including central bank claims). A KM1 figure matching
        # ANY of them is fine; only "matches none" is worth reporting.
        # Real data rows only. A metric sheet also carries a note row and a
        # merged source-citation row, both long prose in column 1 with nothing
        # in the year columns - and a citation that happens to quote a figure
        # in another currency would otherwise poison the currency check below.
        m_rows = [
            mr
            for mr in range(mhr + 1, mws.max_row + 1)
            if isinstance(mws.cell(row=mr, column=1).value, str)
            and mws.cell(row=mr, column=1).value.strip()
            and any(
                mws.cell(row=mr, column=cc).value not in (None, "")
                for cc in range(2, mws.max_column + 1)
            )
        ]
        for c, fy in km1_years.items():
            kv = _numeric(ws.cell(row=r, column=c).value)
            if kv is None or fy not in m_cols:
                continue
            km1_scale = _km1_row_scale(ws, r, c, hr)
            mc, m_scale = m_cols[fy]
            is_ratio = "Ratio" in sheet_name or sheet_name in ("LCR", "NSFR")
            if not is_ratio:
                # A KM1 sheet left in the bank's reporting currency (Europe
                # Arab Bank's is in EUR; ICBC London's in USD) cannot be
                # compared against metric sheets converted to sterling. Ratios
                # are currency-free and still get checked.
                km1_ccy = _currency(label, ws.cell(row=hr, column=c).value, ws.cell(row=1, column=1).value,
                                    ws.cell(row=2, column=1).value)
                m_ccy = _currency(
                    mws.cell(row=mhr, column=mc).value,
                    mws.cell(row=2, column=1).value,
                    *[mws.cell(row=mr, column=1).value for mr in m_rows],
                )
                if km1_ccy and m_ccy and km1_ccy != m_ccy:
                    continue
            candidates = []
            for mr in m_rows:
                mv = _numeric(mws.cell(row=mr, column=mc).value)
                if mv is not None:
                    candidates.append(mv if is_ratio else mv * m_scale)
            if not candidates:
                continue
            checks += 1
            target = kv if is_ratio else kv * km1_scale
            if is_ratio:
                # Banks print the same ratio to different precisions in
                # different editions (Monzo's FY2023 leverage ratio is
                # "14.2%" in the FY2023 report and "14.15%" restated in the
                # FY2024 one). Allow half a unit of the coarser printing, so
                # rounding differences pass and digit slips still fire.
                printed = [ws.cell(row=r, column=c).value] + [
                    mws.cell(row=mr, column=mc).value for mr in m_rows
                ]
                dps = [
                    _decimals(p) for p in printed if _numeric(p) is not None
                ]
                tol = 0.5 * (10 ** -min(dps)) if dps else 0.005
            else:
                tol = max(abs(target) * 0.001, 1.0)
            if not any(abs(target - cand) <= tol for cand in candidates):
                mismatches += 1
                # Unnumbered templates have no row number to quote, so name
                # the row by its label instead.
                who = rownum if rownum in KM1_ROW_TO_METRIC_SHEET else f"{label[:44]!r}"
                print(
                    f"  !! KM1 row {who} {fy}: {ws.cell(row=r, column=c).value!r} "
                    f"disagrees with '{sheet_name}' "
                    f"{[mws.cell(row=mr, column=mc).value for mr in m_rows]}"
                )
    if mismatches == 0:
        print(f"  {checks} KM1 cells cross-checked against metric sheets (all agree)")
    else:
        print(
            f"  {checks} KM1 cells cross-checked, {mismatches} disagree - see above. "
            "A different disclosed basis (e.g. leverage including central bank claims, "
            "point-in-time vs average LCR) is a legitimate reason; a digit slip is not."
        )
    if skipped_mixed_unit:
        print(
            f"  {len(skipped_mixed_unit)} row(s) NOT cross-checked - the row declares more "
            "than one unit, so the unit is per-column and a single row scale cannot "
            "express it. Check these by eye: " + "; ".join(skipped_mixed_unit)
        )


def check_statement_sheet(ws, sheet_name):
    """Run the generic DATA-block -> TOTAL reconciliation check (and print
    every TOTAL row for manual tail-chain review) against one statement
    sheet sharing the standard SECTION/DATA*/TOTAL year-column shape."""
    # Locate the header row (first row with >1 non-empty cell after the title/subtitle)
    header_row = None
    for r in range(1, 6):
        vals = [ws.cell(row=r, column=c).value for c in range(1, ws.max_column + 1)]
        if sum(1 for v in vals if v not in (None, "")) > 1:
            header_row = r
            break
    if header_row is None:
        print(f"\nCouldn't locate the header row for {sheet_name!r} - skipping reconciliation checks.")
        return
    ncols = ws.max_column
    years = [ws.cell(row=header_row, column=c).value for c in range(2, ncols + 1)]
    print(f"\n=== {sheet_name} structure (header row {header_row}) ===")
    print("Years:", years)

    def is_bold(row, col):
        cell = ws.cell(row=row, column=col)
        return bool(cell.font and cell.font.bold)

    def row_kind(r):
        a_bold = is_bold(r, 1)
        if not a_bold:
            return "DATA" if ws.cell(row=r, column=1).value else "BLANK"
        # bold col A: SECTION has no data-column values written; TOTAL does
        any_data = any(
            ws.cell(row=r, column=c).value is not None for c in range(2, ncols + 1)
        )
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
                    col_vals = [ws.cell(row=dr, column=ci).value for dr in run]
                    # Text cells ("Not publicly disclosed", "n/a", a ratio
                    # printed as a string) are legitimate values, not numbers
                    # to add up. A column carrying any of them - in the block
                    # or in the TOTAL row - simply isn't reconcilable, so skip
                    # it rather than crash or report a bogus mismatch.
                    if isinstance(total_v, str) or any(
                        isinstance(v, str) for v in col_vals
                    ):
                        continue
                    # A wholly blank block under a disclosed TOTAL is the
                    # bank disclosing the total but not the split (e.g.
                    # Allica's FY2020 ECL: total 40, no IFRS 9 stage
                    # breakdown published). Nothing to reconcile against.
                    if all(v is None for v in col_vals):
                        continue
                    data_sum = sum((v or 0) for v in col_vals)
                    if total_v is not None and abs((total_v or 0) - data_sum) > 0.05:
                        ok = False
                        mismatches.append((y, data_sum, total_v))
                if ok:
                    checks_passed += 1
                else:
                    print(
                        f"    !! block {run}->row {r} does NOT reconcile: {mismatches}"
                    )
            run = []

    print(f"\n=== {sheet_name} block reconciliation summary ===")
    print(
        f"{checks_passed}/{checks_run} DATA-block -> TOTAL checks passed"
        f"{' (all clean)' if checks_passed == checks_run else '  !! see mismatches above'}"
    )
    print(
        "\nReview the TOTAL rows above by eye for the tail chain (net change / "
        "opening / closing, incl. any FX or other adjustment lines) - that part "
        "is bank-specific and isn't auto-verified."
    )


if __name__ == "__main__":
    main()
