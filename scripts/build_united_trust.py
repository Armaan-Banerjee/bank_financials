import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# TODO: adjust YEARS/YEAR_LABEL once the entity's actual fiscal year-end and
# available history are confirmed (most recent first). Use YEAR_LABEL only if
# a year needs a suffix/footnote (entity change, transition period, etc.) -
# otherwise the default (year key == its own label) is fine, drop this dict.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

# TODO: fill in every source document URL actually used, one constant per
# document (annual report and/or Pillar 3 report, per year or per multi-year
# document as applicable). Keep names descriptive, e.g. AR2025_URL, P3_2025_URL.
AR2025_URL = ""
P3_2025_URL = ""

# TODO: any entity-structure/basis/complication notes go here as a constant,
# then get interpolated into CASH_FLOW_SOURCES and/or individual metric notes
# (see build_clydesdale.py for the pattern - ENTITY_NOTE, NATIONWIDE_NOTE, etc.)
ENTITY_NOTE = (
    ""
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are United Trust Bank Limited's own consolidated cash flow statement:\n"
    # TODO: one "FYxxxx: <document>, p.<page> (<statement name>) - <url>\n" line per year
    + ENTITY_NOTE
)


def p3_sources():
    # TODO: mirror build_clydesdale.py's p3_sources() pattern - one line per
    # year citing the exact Pillar 3 document/page/table/URL used. Parameterize
    # with page-number kwargs if the same helper is reused across metrics with
    # differing page numbers per metric.
    return (
        "Sources - United Trust Bank Limited Pillar 3 basis:\n"
    )


bw = BankWorkbook(bank_name="United Trust Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="3C6E47")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
# TODO: fill in real rows. Each tuple is (kind, label, {year: value}):
#   "SECTION" - a bold divider row, label only, values={}
#   "DATA"    - a normal line item
#   "TOTAL"   - a bolded subtotal/total (bold across every column)
# Leave a year out of the dict (rather than 0) when that year's report didn't
# disclose that line. Preserve each year's own as-reported line items/labels
# rather than forcing every year into identical rows - see build_clydesdale.py.
rows = [
    ("SECTION", "Operating activities", {}),
    ("TOTAL", "Net cash from/(used in) operating activities", {}),
    ("SECTION", "Investing activities", {}),
    ("TOTAL", "Net cash from/(used in) investing activities", {}),
    ("SECTION", "Financing activities", {}),
    ("TOTAL", "Net cash from/(used in) financing activities", {}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {}),
]

bw.add_cash_flow_sheet(
    title="United Trust Bank Limited — Consolidated Cash Flow Statement",
    subtitle="TODO basis/unit description",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=70,
    source_height=150,
    unit_suffix=" (£m)",  # TODO: confirm unit (£m / £'000) matches the source
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=110)


# TODO: one metric(...) call per sheet - CET1 Capital, CET1 Ratio, Tier 1 Capital,
# Tier 1 Ratio, Total Capital, Total Capital Ratio, Total RWAs, Leverage Ratio,
# LCR, NSFR, MREL Ratio. Use add_not_disclosed_metric_sheets(...) or a
# "Not disclosed" row for anything genuinely unavailable - never guess.
metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {})],
    p3_sources(),
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {}),
        ("Net cash from/(used in) investing activities", {}),
        ("Net cash from/(used in) financing activities", {}),
        ("Cash and cash equivalents at end of year", {}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {}),
        ("Tier 1 Ratio", {}),
        ("Total Capital Ratio", {}),
        ("Leverage Ratio", {}),
        ("LCR", {}),
        ("NSFR", {}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/UNITED TRUST FINANCIALS.xlsx")
