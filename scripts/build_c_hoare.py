import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2026", "FY2025", "FY2024", "FY2023", "FY2022"]  # most recent first, y/e 31 March
YEAR_LABEL = {y: y for y in YEARS}

AR2026_URL = "https://www.hoaresbank.co.uk/files/2026-06/Financial_Report_2026.pdf"
AR2025_URL = "https://www.hoaresbank.co.uk/files/2025-07/Financial_Report_2025.pdf"
AR2024_URL = "https://www.hoaresbank.co.uk/files/2024-06/Financial_Report_2024.pdf"
AR2023_URL = "https://www.hoaresbank.co.uk/files/2023-07/Financial_Report_2023.pdf"
AR2022_URL = "https://www.hoaresbank.co.uk/files/2022-07/Annual_Report_2022.pdf"

P3_2025_URL = "https://www.hoaresbank.co.uk/files/2025-07/Pillar_3_Disclosure_2025.pdf"
P3_2023_URL = "https://www.hoaresbank.co.uk/files/2023-07/Pillar_3_Disclosure_2023.pdf"

ENTITY_NOTE = (
    "C. Hoare & Co. (company 00240822, FRN 122093) is a private unlimited company - Britain's oldest "
    "privately-owned bank, founded 1672, owned by the Hoare family. Despite the unlimited-company legal "
    "form, it voluntarily publishes full audited Consolidated (Group) accounts and Pillar 3 disclosures every "
    "year on its own site (hoaresbank.co.uk/financial-reports), all text-native, no OCR needed, 0 WebSearch "
    "calls used (all sourcing via WebFetch against the bank's own site and Companies House). Fiscal year-end "
    "31 March. Every figure below is each year's own originally-published report - not a later restated "
    "comparative. FY2025's report introduced a new 'Effect of exchange rate changes' line splitting out what "
    "FY2024's own report folded into a single net-change figure; FY2024's own presentation (no separate FX "
    "line) is preserved here rather than using FY2025's restated split. FY2024's own printed 'Net decrease in "
    "cash and cash equivalents' (164,034) is £1k off from summing its own three section totals (164,033) - an "
    "immaterial rounding artifact in the source document itself, kept as printed. FY2026 Pillar 3 has not yet "
    "been published (the bank's Pillar 3 editions consistently lag the Annual Report by several months) - "
    "left blank, not estimated."
)

CASH_FLOW_SOURCES = (
    "Sources - C. Hoare & Co.'s own Consolidated Cash Flow Statement, each year from its own year's Financial "
    "Report (not a later comparative):\n"
    f"FY2026: Financial Report 2026, p.53 (Consolidated Cash Flow Statement) - {AR2026_URL}\n"
    f"FY2025: Financial Report 2025, p.39 (Consolidated Cash Flow Statement) - {AR2025_URL}\n"
    f"FY2024: Financial Report 2024, p.41 (Consolidated Cash Flow Statement) - {AR2024_URL}\n"
    f"FY2023: Financial Report 2023, p.37 (Consolidated Cash Flow Statement) - {AR2023_URL}\n"
    f"FY2022: Annual Report 2022, p.36 (Consolidated Cash Flow Statement) - {AR2022_URL}\n"
    "The face of the statement itself gives operating cash flow as a single pre-tax total (with a detailed "
    "profit/adjustments/working-capital breakdown in a separate Notes to the Cash Flow Statement note) - that "
    "single total is transcribed here as one DATA line rather than the full note-level breakdown, to keep row "
    "structure consistent across all 5 years.\n"
    + ENTITY_NOTE
)


def p3_sources(page):
    return (
        "Sources - C. Hoare & Co. Pillar 3 Disclosures, Appendix 1 (Own Funds Disclosure template, UK KM1 "
        "basis), solo-consolidated basis:\n"
        f"FY2025/FY2024: Pillar 3 Disclosures 2025, p.{page.get('recent','15')} - {P3_2025_URL}\n"
        f"FY2023/FY2022: Pillar 3 Disclosures 2023, p.{page.get('older','26')} - {P3_2023_URL}\n"
        "FY2026: not yet published as of this build - left blank, not estimated.\n"
        + ENTITY_NOTE
    )


PAGES = {"recent": "15", "older": "26"}

bw = BankWorkbook(bank_name="C. Hoare & Co.", years=YEARS, year_label=YEAR_LABEL, header_color="6F1D1B")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Net cash from/(used in) operating activities (before tax)", {
        "FY2026": 87472, "FY2025": 333415, "FY2024": -94951, "FY2023": -418678, "FY2022": 1121381}),
    ("DATA", "Taxation paid", {
        "FY2026": -12154, "FY2025": -11881, "FY2024": -15618, "FY2023": -17355, "FY2022": -4932}),
    ("TOTAL", "Net cash from/(used in) operating activities", {
        "FY2026": 75318, "FY2025": 321534, "FY2024": -110569, "FY2023": -436033, "FY2022": 1116449}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of investment securities", {
        "FY2026": -1648567, "FY2025": -779143, "FY2024": -1648464, "FY2023": -1562892, "FY2022": -3121342}),
    ("DATA", "Sale and maturity of investment securities", {
        "FY2026": 1064233, "FY2025": 684225, "FY2024": 1614146, "FY2023": 1640306, "FY2022": 2122564}),
    ("DATA", "Purchase of bulk annuity policy", {"FY2025": -278, "FY2024": -7191}),
    ("DATA", "Purchase of intangible assets", {
        "FY2026": -16598, "FY2025": -23130, "FY2024": -9220, "FY2023": -8427, "FY2022": -10853}),
    ("DATA", "Purchase of tangible fixed assets", {
        "FY2026": -5725, "FY2025": -6425, "FY2024": -2671, "FY2023": -4318, "FY2022": -350}),
    ("DATA", "Purchase of heritage assets", {"FY2026": -192, "FY2025": -9, "FY2024": -58, "FY2023": -53}),
    ("DATA", "Proceeds from sale of subsidiary", {"FY2025": 745}),
    ("TOTAL", "Net cash from/(used in) investing activities", {
        "FY2026": -606849, "FY2025": -124015, "FY2024": -53458, "FY2023": 64616, "FY2022": -1009981}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividend paid", {"FY2026": -6, "FY2025": -6, "FY2024": -6, "FY2023": -6, "FY2022": -6}),
    ("TOTAL", "Net cash from/(used in) financing activities", {
        "FY2026": -6, "FY2025": -6, "FY2024": -6, "FY2023": -6, "FY2022": -6}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {
        "FY2026": -531537, "FY2025": 197513, "FY2024": -164034, "FY2023": -371423, "FY2022": 106462}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {
        "FY2026": 1580850, "FY2025": 1382976, "FY2024": 1547010, "FY2023": 1918433, "FY2022": 1811971}),
    ("DATA", "Effect of exchange rate changes", {"FY2026": -12, "FY2025": 361}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {
        "FY2026": 1049301, "FY2025": 1580850, "FY2024": 1382976, "FY2023": 1547010, "FY2022": 1918433}),
    ("SECTION", "Cash and cash equivalents comprise", {}),
    ("DATA", "Cash at bank and in hand", {
        "FY2026": 896317, "FY2025": 1548443, "FY2024": 1345322, "FY2023": 1452949, "FY2022": 1843378}),
    ("DATA", "Short term deposits", {
        "FY2026": 152984, "FY2025": 32407, "FY2024": 37654, "FY2023": 94061, "FY2022": 75055}),
    ("TOTAL", "Cash and cash equivalents", {
        "FY2026": 1049301, "FY2025": 1580850, "FY2024": 1382976, "FY2023": 1547010, "FY2022": 1918433}),
]

bw.add_cash_flow_sheet(
    title="C. Hoare & Co. — Consolidated Cash Flow Statement",
    subtitle="Consolidated Group basis, £'000. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(PAGES), note=note, first_col_width=48, source_height=170)


metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", {
    "FY2025": 526455, "FY2024": 483235, "FY2023": 428543, "FY2022": 381989})])

metric("CET1 Ratio", "%", [("Common Equity Tier 1 ratio", {
    "FY2025": "23.00%", "FY2024": "23.11%", "FY2023": "21.44%", "FY2022": "20.96%"})])

metric("Tier 1 Capital", "£'000 (= CET1 capital; no AT1 instruments)", [("Tier 1 capital", {
    "FY2025": 526455, "FY2024": 483235, "FY2023": 428543, "FY2022": 381989})])

metric("Tier 1 Ratio", "%", [("Tier 1 ratio", {
    "FY2025": "23.00%", "FY2024": "23.11%", "FY2023": "21.44%", "FY2022": "20.96%"})])

metric("Total Capital", "£'000", [("Total capital", {
    "FY2025": 531333, "FY2024": 488113, "FY2023": 433856, "FY2022": 386392})])

metric("Total Capital Ratio", "%", [("Total capital ratio", {
    "FY2025": "23.21%", "FY2024": "23.34%", "FY2023": "21.72%", "FY2022": "21.20%"})])

metric("Total RWAs", "£'000", [("Total risk-weighted exposure amount", {
    "FY2025": 2289414, "FY2024": 2091044, "FY2023": 1997896, "FY2022": 1822244})])

metric("Leverage Ratio", "%, excluding claims on central banks", [("Leverage ratio excluding claims on central banks", {
    "FY2025": "9.29%", "FY2024": "7.61%", "FY2023": "6.96%", "FY2022": "6.61%"})],
    note="Consistently disclosed on the same 'excluding claims on central banks' basis every year shown - no "
         "mid-series methodology break, unlike several other banks in this project.")

metric("LCR", "%, 12-month rolling average of month-end positions", [("Liquidity coverage ratio", {
    "FY2025": "341%", "FY2024": "308%", "FY2023": "273%", "FY2022": "272%"})])

metric("NSFR", "%, 4-quarter rolling average of quarter-end positions", [("NSFR ratio", {
    "FY2025": "250%", "FY2024": "246%", "FY2023": "256%", "FY2022": "269%"})])

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources(PAGES),
    per_note={"MREL Ratio": "Not found in either Pillar 3 document reviewed (2025 or 2023 edition) - no MREL "
                             "row exists in this bank's Own Funds Disclosure template at all, and no separate "
                             "qualitative statement was found either."},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {
            "FY2026": 75318, "FY2025": 321534, "FY2024": -110569, "FY2023": -436033, "FY2022": 1116449}),
        ("Net cash from/(used in) investing activities", {
            "FY2026": -606849, "FY2025": -124015, "FY2024": -53458, "FY2023": 64616, "FY2022": -1009981}),
        ("Net cash from/(used in) financing activities", {
            "FY2026": -6, "FY2025": -6, "FY2024": -6, "FY2023": -6, "FY2022": -6}),
        ("Cash and cash equivalents at end of year", {
            "FY2026": 1049301, "FY2025": 1580850, "FY2024": 1382976, "FY2023": 1547010, "FY2022": 1918433}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "23.00%", "FY2024": "23.11%", "FY2023": "21.44%", "FY2022": "20.96%"}),
        ("Tier 1 Ratio", {"FY2025": "23.00%", "FY2024": "23.11%", "FY2023": "21.44%", "FY2022": "20.96%"}),
        ("Total Capital Ratio", {"FY2025": "23.21%", "FY2024": "23.34%", "FY2023": "21.72%", "FY2022": "21.20%"}),
        ("Leverage Ratio", {"FY2025": "9.29%", "FY2024": "7.61%", "FY2023": "6.96%", "FY2022": "6.61%"}),
        ("LCR", {"FY2025": "341%", "FY2024": "308%", "FY2023": "273%", "FY2022": "272%"}),
        ("NSFR", {"FY2025": "250%", "FY2024": "246%", "FY2023": "256%", "FY2022": "269%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. FY2026 Pillar 3 ratios not yet published.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/C HOARE AND CO FINANCIALS.xlsx")
