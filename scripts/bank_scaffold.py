"""
Generate a new scripts/build_<slug>.py skeleton for a bank workbook, so each
new bank starts from a filled-in template instead of retyping the same
imports/YEARS/metric()/add_overview_sheet boilerplate every time.

Usage:
    python3 bank_scaffold.py <slug> "<Bank Legal Name>" "<XLSX STUB>" [hex_color] [--interim]

    slug        - short lowercase identifier, e.g. "zopa" -> writes build_zopa.py
    Bank Legal Name - passed to BankWorkbook(bank_name=...), e.g. "Zopa Bank Limited"
    XLSX STUB   - short name used in the output filename: "<XLSX STUB> FINANCIALS.xlsx"
                  (match this project's existing short-name convention, e.g. "ZOPA",
                  "BANK OF IRELAND UK" - not necessarily the full legal name)
    hex_color   - optional 6-digit hex header color. If omitted, picks the first
                  color from a fixed palette that isn't already used by any
                  existing build_*.py in this directory.
    --interim   - optional flag to include an empty Interim Pillar 3 sheet
                  placeholder using BankWorkbook.add_long_form_sheet().

Example:
    python3 bank_scaffold.py zopa "Zopa Bank Limited" "ZOPA"
"""
import os
import re
import sys

SCRIPTS_DIR = os.path.dirname(__file__)

PALETTE = [
    "1B4332", "5C2751", "8A5A00", "2A3E5C", "6E2C00", "0B4F6C", "7A0C2E",
    "3C6E47", "4A1E4D", "805B10", "1E5631", "9C3D54", "264653", "5A3E85",
    "7C4A03", "285943", "4B2E39", "0F5B78", "6B4226", "3D5A80",
]


def used_colors():
    used = set()
    for fn in os.listdir(SCRIPTS_DIR):
        if fn.startswith("build_") and fn.endswith(".py"):
            with open(os.path.join(SCRIPTS_DIR, fn)) as f:
                text = f.read()
            for m in re.finditer(r'header_color="([0-9A-Fa-f]{6})"', text):
                used.add(m.group(1).upper())
    return used


def pick_color():
    used = used_colors()
    for c in PALETTE:
        if c not in used:
            return c
    # Palette exhausted (this project now has more banks than PALETTE has
    # colors) - generate further colors deterministically rather than always
    # returning the same hardcoded fallback, which caused a real collision
    # once two scripts both hit this branch (build_bank_sepah_international.py
    # and an early attempt at build_c_hoare.py both got "444444").
    import hashlib
    n = 0
    while True:
        digest = hashlib.sha256(f"katalysis-bank-color-{n}".encode()).hexdigest()
        c = digest[:6].upper()
        r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
        luminance = 0.299 * r + 0.587 * g + 0.114 * b
        # header text is always white (see bank_workbook.py's header_font) -
        # reject anything too light to keep it readable, not just unique.
        if c not in used and c not in PALETTE and luminance < 140:
            return c
        n += 1


TEMPLATE = '''import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# TODO: adjust YEARS/YEAR_LABEL once the entity's actual fiscal year-end and
# available history are confirmed (most recent first). Use YEAR_LABEL only if
# a year needs a suffix/footnote (entity change, transition period, etc.) -
# otherwise the default (year key == its own label) is fine, drop this dict.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {{y: y for y in YEARS}}

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
    "Sources - all figures are {bank_name}'s own consolidated cash flow statement:\\n"
    # TODO: one "FYxxxx: <document>, p.<page> (<statement name>) - <url>\\n" line per year
    + ENTITY_NOTE
)


def p3_sources():
    # TODO: mirror build_clydesdale.py's p3_sources() pattern - one line per
    # year citing the exact Pillar 3 document/page/table/URL used. Parameterize
    # with page-number kwargs if the same helper is reused across metrics with
    # differing page numbers per metric.
    return (
        "Sources - {bank_name} Pillar 3 basis:\\n"
    )


bw = BankWorkbook(bank_name="{bank_name}", years=YEARS, year_label=YEAR_LABEL, header_color="{color}")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
# TODO: fill in real rows. Each tuple is (kind, label, {{year: value}}):
#   "SECTION" - a bold divider row, label only, values={{}}
#   "DATA"    - a normal line item
#   "TOTAL"   - a bolded subtotal/total (bold across every column)
# Leave a year out of the dict (rather than 0) when that year's report didn't
# disclose that line. Preserve each year's own as-reported line items/labels
# rather than forcing every year into identical rows - see build_clydesdale.py.
rows = [
    ("SECTION", "Operating activities", {{}}),
    ("TOTAL", "Net cash from/(used in) operating activities", {{}}),
    ("SECTION", "Investing activities", {{}}),
    ("TOTAL", "Net cash from/(used in) investing activities", {{}}),
    ("SECTION", "Financing activities", {{}}),
    ("TOTAL", "Net cash from/(used in) financing activities", {{}}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {{}}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {{}}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {{}}),
]

bw.add_cash_flow_sheet(
    title="{bank_name} — Consolidated Cash Flow Statement",
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
    bw.add_metric_sheet(name, f"{{unit}}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=110)


# TODO: one metric(...) call per sheet - CET1 Capital, CET1 Ratio, Tier 1 Capital,
# Tier 1 Ratio, Total Capital, Total Capital Ratio, Total RWAs, Leverage Ratio,
# LCR, NSFR, MREL Ratio. Use add_not_disclosed_metric_sheets(...) or a
# "Not disclosed" row for anything genuinely unavailable - never guess.
metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {{}})],
    p3_sources(),
)

# ---------------------------------------------------------------
{interim_block}
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {{}}),
        ("Net cash from/(used in) investing activities", {{}}),
        ("Net cash from/(used in) financing activities", {{}}),
        ("Cash and cash equivalents at end of year", {{}}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {{}}),
        ("Tier 1 Ratio", {{}}),
        ("Total Capital Ratio", {{}}),
        ("Leverage Ratio", {{}}),
        ("LCR", {{}}),
        ("NSFR", {{}}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/{xlsx_stub} FINANCIALS.xlsx")
'''


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)
    slug, bank_name, xlsx_stub = sys.argv[1], sys.argv[2], sys.argv[3]
    extra_args = sys.argv[4:]
    interim = "--interim" in extra_args
    color_args = [arg for arg in extra_args if arg != "--interim"]
    color = color_args[0] if color_args else pick_color()

    out_path = os.path.join(SCRIPTS_DIR, f"build_{slug}.py")
    if os.path.exists(out_path):
        print(f"Refusing to overwrite existing {out_path}")
        sys.exit(1)

    interim_block = ""
    if interim:
        interim_block = '''# ---------------------------------------------------------------
# Optional interim Pillar 3 observations
# ---------------------------------------------------------------
# Fill INTERIM_ROWS with one list per observation. Keep the annual metric
# sheets above unchanged; use this long-form sheet for Q1/H1/Q3 periods.
INTERIM_HEADERS = ["Period", "Disclosure type", "Metric", "Value", "Unit", "Basis", "Source document", "Page / table"]
INTERIM_ROWS = []
bw.add_long_form_sheet(
    name="Interim Pillar 3",
    headers=INTERIM_HEADERS,
    rows=INTERIM_ROWS,
    note="TODO: document the reporting periods, entity basis, and source gaps.",
    widths=[14, 16, 24, 14, 10, 36, 52, 18],
)

'''
    content = TEMPLATE.format(
        bank_name=bank_name,
        xlsx_stub=xlsx_stub,
        color=color,
        interim_block=interim_block,
    )
    with open(out_path, "w") as f:
        f.write(content)
    print(f"Wrote {out_path} (header_color={color})")


if __name__ == "__main__":
    main()
