import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first

AR2025_URL = "https://www.ghanabank.co.uk/app/uploads/2026/04/GHIB-ANNUAL-REPORT-2025-2-page-view.pdf"
AR2024_URL = "https://www.ghanabank.co.uk/app/uploads/2025/04/GHIB-ANNUAL-REPORT-2024.pdf"
AR2022_URL = "https://www.ghanabank.co.uk/app/uploads/2023/03/GHIB-Annual-Report-and-Financial-Statements-2022-.pdf"

P3_2024_URL = "https://www.ghanabank.co.uk/app/uploads/2025/11/GHIB-2024-Pillar-3-Disclosures.pdf"
P3_2023_URL = "https://www.ghanabank.co.uk/app/uploads/2024/11/GHIB-2023-Pillar-3-Disclosures.pdf"
P3_2022_URL = "https://www.ghanabank.co.uk/app/uploads/2023/09/GHIB-2022-Pillar-3-Disclosures.pdf"
P3_2021_URL = "https://www.ghanabank.co.uk/app/uploads/2022/10/GHIB-2021-Pillar-3-Disclosures.pdf"

CASH_FLOW_NOTE = (
    "Note: FY2023/FY2024/FY2025 statements include an additional adjustment line, 'Net interest "
    "income and other non-cash items', not present in the FY2021/FY2022 presentation - this is a "
    "genuine year-on-year presentation change by the Bank, not a missing figure; the blank cells for "
    "FY2021/FY2022 reflect that this split simply wasn't disclosed that way in those years' accounts. "
    "Section totals (net cash from operating/investing/financing activities, cash and cash equivalents) "
    "are consistent and comparable across all 5 years."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Ghana International Bank Plc's own Statement of Cash Flow, £:\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements 2025, p.76 (Statement of Cash Flow) - {AR2025_URL}\n"
    f"FY2024 & FY2023: Annual Report and Financial Statements 2024, p.82 (Statement of cash flow) - {AR2024_URL}\n"
    f"FY2022 & FY2021: Annual Report and Financial Statements 2022, p.49 (Statement of cash flow) - {AR2022_URL}\n"
    "(FY2022 report is a scanned/image-only Companies House filing with no text layer - transcribed "
    "by direct visual reading of the rendered page.)\n"
    + CASH_FLOW_NOTE
)


def p3_sources(page="4-5"):
    return (
        "Sources - Ghana International Bank Plc Pillar 3 Disclosures, Table 1: Key Metrics ratios:\n"
        f"FY2024: Pillar 3 Disclosures 31 December 2024, p.{page} - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures 31 December 2023, p.5 - {P3_2023_URL}\n"
        f"FY2022: Pillar 3 Disclosures 31 December 2022, p.4 - {P3_2022_URL}\n"
        f"FY2021: Pillar 3 Disclosures 31 December 2021, p.4 - {P3_2021_URL}\n"
        "FY2025 not yet published as of this workbook's build date (Pillar 3 reports historically follow "
        "the Annual Report by several months - e.g. the FY2024 Pillar 3 report was published in "
        "November 2025, ~7 months after the FY2024 Annual Report)."
    )


NSFR_NOTE = (
    "NSFR only reported from FY2022 onward - the Bank states comparable figures for earlier periods "
    "are not available because the NSFR rules introduced under CRR2 only commenced on 1 January 2022."
)
NO_AT1_NOTE = "No Additional Tier 1 or Tier 2 instruments disclosed any year - Tier 1/Total Capital equal CET1 Capital throughout."

bw = BankWorkbook(bank_name="Ghana International Bank Plc", years=YEARS, header_color="619578")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit/(loss) before taxation", {
        "FY2025": 7026619, "FY2024": 5836762, "FY2023": 4258102, "FY2022": -10119946, "FY2021": -12470381}),
    ("DATA", "Foreign currency income - Translation of assets & liabilities", {
        "FY2025": -856667, "FY2024": -748521, "FY2023": -525892, "FY2022": -661420, "FY2021": -297613}),
    ("DATA", "Depreciation and amortisation", {
        "FY2025": 3318426, "FY2024": 2383646, "FY2023": 2277366, "FY2022": 1682232, "FY2021": 1258265}),
    ("DATA", "Lease finance charge", {
        "FY2025": 168908, "FY2024": 165240, "FY2023": 140727, "FY2022": 159254, "FY2021": 168528}),
    ("DATA", "(Reversal of provisions)/provisions for credit losses", {
        "FY2025": -82778, "FY2024": 408819, "FY2023": -1024498, "FY2022": 1986487, "FY2021": 1090971}),
    ("DATA", "Gain on disposal of fixed asset", {"FY2025": -5164, "FY2022": -4404, "FY2021": -7648}),
    ("DATA", "Net interest income and other non-cash items", {
        "FY2025": -5354639, "FY2024": 6709610, "FY2023": -790883}),
    ("DATA", "Decrease/(increase) in loans and advances to banks and customers", {
        "FY2025": -102290341, "FY2024": -79379510, "FY2023": -8318223, "FY2022": 37516914, "FY2021": -40250490}),
    ("DATA", "Decrease/(increase) in government and other securities", {
        "FY2025": -56902275, "FY2024": -246603941, "FY2023": 52729216, "FY2022": -82184444, "FY2021": -23355251}),
    ("DATA", "Decrease/(increase) in prepayments and other receivables", {
        "FY2025": 1097161, "FY2024": -2393680, "FY2023": -488671, "FY2022": 43806, "FY2021": -919472}),
    ("DATA", "Increase/(decrease) in deposits by banks and customers", {
        "FY2025": 91632232, "FY2024": 247285853, "FY2023": -90180843, "FY2022": 79813107, "FY2021": 43175607}),
    ("DATA", "Increase/(decrease) in other liabilities", {
        "FY2025": -40316, "FY2024": 382531, "FY2023": -323153, "FY2022": 866972, "FY2021": 252000}),
    ("DATA", "Increase/(decrease) in accruals and deferred income", {
        "FY2025": 1430553, "FY2024": 1574625, "FY2023": 1816917, "FY2022": 955575, "FY2021": -647350}),
    ("DATA", "Income taxes refunded", {"FY2025": 0, "FY2024": 945584}),
    ("DATA", "Foreign income taxes paid", {"FY2025": -198914, "FY2024": -38468}),
    ("TOTAL", "Net cash generated from/(used in) operating activities", {
        "FY2025": -61057195, "FY2024": -63471450, "FY2023": -40429835, "FY2022": 30054133, "FY2021": -32002834}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment", {
        "FY2025": -578036, "FY2024": -478827, "FY2023": -303289, "FY2022": -786227, "FY2021": -800543}),
    ("DATA", "Purchase of intangible assets", {
        "FY2025": -1992939, "FY2024": -2751634, "FY2023": -1914732, "FY2022": -3455929, "FY2021": -1585110}),
    ("DATA", "Proceeds from sale of fixed asset", {"FY2025": 5164, "FY2022": 4404, "FY2021": 7648}),
    ("TOTAL", "Net cash used in investing activities", {
        "FY2025": -2565811, "FY2024": -3230461, "FY2023": -2218021, "FY2022": -4237752, "FY2021": -2378005}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Dividends paid", {"FY2025": -847741, "FY2024": -622459}),
    ("DATA", "Net increase in term financing", {"FY2025": 19945689, "FY2024": 14377227}),
    ("DATA", "Proceeds from an equity share issue (net of issuance cost)", {"FY2022": 49952714}),
    ("DATA", "Repayment of lease liabilities", {
        "FY2025": -848145, "FY2024": -1157028, "FY2023": -874791, "FY2022": -915051, "FY2021": -849159}),
    ("TOTAL", "Net cash generated from/(used in) financing activities", {
        "FY2025": 18249803, "FY2024": 12597740, "FY2023": -874791, "FY2022": 49037663, "FY2021": -849159}),
    ("TOTAL", "(Decrease)/increase in cash and cash equivalents", {
        "FY2025": -45373203, "FY2024": -54104171, "FY2023": -43522647, "FY2022": 74854044, "FY2021": -35229998}),
    ("DATA", "Effect of exchange rate changes on cash and cash equivalents", {
        "FY2025": 89985, "FY2024": 108502, "FY2023": 112750, "FY2022": 162049, "FY2021": 71416}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {
        "FY2025": -45283218, "FY2024": -53995669, "FY2023": -43409897, "FY2022": 75016093, "FY2021": -35158582}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {
        "FY2025": 376370085, "FY2024": 430365754, "FY2023": 473775651, "FY2022": 398759558, "FY2021": 433918140}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {
        "FY2025": 331086867, "FY2024": 376370085, "FY2023": 430365754, "FY2022": 473775651, "FY2021": 398759558}),
]

bw.add_cash_flow_sheet(
    title="Ghana International Bank Plc — Statement of Cash Flow",
    subtitle="Company basis (GHIB has no subsidiaries or branches), £. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=85,
    source_height=210,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None, page="4-5"):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(page), note=note, first_col_width=48, source_height=170)


CET1_CAPITAL = {"FY2024": 156657, "FY2023": 153053, "FY2022": 152019, "FY2021": 120301}
TOTAL_RWA = {"FY2024": 700374, "FY2023": 493080, "FY2022": 537708, "FY2021": 450231}
CET1_RATIO = {"FY2024": "22.37%", "FY2023": "31.04%", "FY2022": "28.27%", "FY2021": "26.72%"}
LEVERAGE_RATIO = {"FY2024": "14.66%", "FY2023": "25.88%", "FY2022": "23.86%", "FY2021": "15.20%"}
LCR = {"FY2024": "256.31%", "FY2023": "370.09%", "FY2022": "409.87%", "FY2021": "378.34%"}
NSFR = {"FY2024": "255.98%", "FY2023": "273.27%", "FY2022": "292.79%"}

metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", CET1_CAPITAL)])
metric("CET1 Ratio", "%", [("Common Equity Tier 1 ratio", CET1_RATIO)])
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", CET1_CAPITAL)], note=NO_AT1_NOTE)
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", CET1_RATIO)], note=NO_AT1_NOTE)
metric("Total Capital", "£'000", [("Total capital", CET1_CAPITAL)], note=NO_AT1_NOTE)
metric("Total Capital Ratio", "%", [("Total capital ratio", CET1_RATIO)], note=NO_AT1_NOTE)
metric("Total RWAs", "£'000", [("Total risk-weighted exposure amount", TOTAL_RWA)])
metric("Leverage Ratio", "%", [("Leverage ratio excluding claims on central banks", LEVERAGE_RATIO)])
metric("LCR", "%", [("Liquidity coverage ratio", LCR)])
metric("NSFR", "%", [("Net Stable Funding Ratio", NSFR)], note=NSFR_NOTE)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources(),
    per_note={"MREL Ratio": "Not publicly disclosed any year - GHIB is not a UK resolution entity subject to MREL."},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash generated from/(used in) operating activities", {
            "FY2025": -61057195, "FY2024": -63471450, "FY2023": -40429835, "FY2022": 30054133, "FY2021": -32002834}),
        ("Net cash used in investing activities", {
            "FY2025": -2565811, "FY2024": -3230461, "FY2023": -2218021, "FY2022": -4237752, "FY2021": -2378005}),
        ("Net cash generated from/(used in) financing activities", {
            "FY2025": 18249803, "FY2024": 12597740, "FY2023": -874791, "FY2022": 49037663, "FY2021": -849159}),
        ("Cash and cash equivalents at the end of the year", {
            "FY2025": 331086867, "FY2024": 376370085, "FY2023": 430365754, "FY2022": 473775651, "FY2021": 398759558}),
    ],
    cash_flow_unit="£",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Leverage Ratio", LEVERAGE_RATIO),
        ("LCR", LCR),
        ("NSFR", NSFR),
    ],
    note="GHIB is a UK-incorporated PLC (registered England & Wales no. 03468216, a subsidiary of the "
         "Government of Ghana) that reports in GBP throughout - no currency conversion applied. Pillar 3 "
         "figures are not yet available for FY2025 (see the Pillar 3 sheets' own source notes). Figures "
         "are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/GHANA INTERNATIONAL BANK FINANCIALS.xlsx")
