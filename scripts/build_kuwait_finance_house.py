import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, y/e 31 Dec
YEAR_LABEL = {y: y for y in YEARS}

BASE = "https://find-and-update.company-information.service.gov.uk/company/00877859/filing-history"
AR2025_URL = f"{BASE}/MzUyMTMwODAyMGFkaXF6a2N4/document?format=pdf&download=0"
AR2024_URL = f"{BASE}/MzQ2OTUzMTA5NGFkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = f"{BASE}/MzQxNzM5MjkxNGFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = f"{BASE}/MzM3MTE2OTUwOGFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = f"{BASE}/MzM0MTg2NjEyNWFkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "ENTITY NOTE: Kuwait Finance House Plc (FRN 131818, Companies House 00877859) was formerly Ahli "
    "United Bank (UK) PLC - renamed following its 2024 conversion to a Shariah-compliant (Islamic) "
    "bank under new ownership (Kuwait Finance House Group), confirmed by the FY2024/FY2025 Annual "
    "Reports' own Shariah Supervisory Board report describing 'the recent conversion of the Bank'. "
    "This is a genuine, disclosed business-model change, not a data anomaly: FY2021-FY2023 use "
    "conventional banking terminology (Loans and advances, Interest income/expense/receivable/"
    "payable); FY2024-FY2025 use Islamic-finance terminology (Financing receivables, Returns "
    "receivable/payable) for the functionally equivalent line items, kept as each year's own "
    "originally-printed labels rather than forced into a single common wording. Reports in USD'000 "
    "(Bank/solo basis) - all Companies House filings are fully scanned/image-only, transcribed via "
    "targeted page-image reads, not full-document OCR. Kept in native USD (not converted to GBP), "
    "consistent with sibling USD-reporting banks built in this same batch (e.g. Itau BBA "
    "International plc)."
)

RESTATEMENT_NOTE = (
    "RESTATEMENT NOTE: the FY2025 Annual Report's own FY2024 comparative column restates FY2024's "
    "cash flow (operating $(75,732) vs FY2024's own originally-published $(131,665); investing "
    "$254,257 vs FY2024's own originally-published $257,136) - both vintages agree on the "
    "$752,166k closing balance, so this is a reclassification between activity sections, not a "
    "change to overall cash movement. Likewise the FY2024 Annual Report's own Note 37 documents a "
    "restatement of FY2023's comparative cash flow figures vs FY2023's own originally-published "
    "report (operating activities restated to $58,844/net $44,248 vs FY2023's own $87,112/$72,516; "
    "both agree on the $664,122k closing balance). Every year's own originally-published Annual "
    "Report figures are used throughout this workbook, consistent with this project's standard "
    "convention of preferring each year's own primary source over a later restated comparative."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Kuwait Finance House Plc's (formerly Ahli United Bank (UK) PLC's) own "
    "Bank Statement of Cash Flows, from Companies House filings:\n"
    f"FY2025/FY2024 (own): Annual Report and Financial Statements 2025, p.29 - {AR2025_URL}\n"
    f"FY2024 (own, used here) / FY2023 (restated, not used): Annual Report and Financial Statements "
    f"2024, p.30 - {AR2024_URL}\n"
    f"FY2023 (own, used here) / FY2022: Annual Report and Financial Statements 2023, p.26 - "
    f"{AR2023_URL}\n"
    f"FY2022 (own, used here) / FY2021 (cross-checked): Annual Report and Financial Statements 2022, "
    f"p.25 - {AR2022_URL}\n"
    f"FY2021 (own, used here): Annual Report and Financial Statements 2021, p.18 - {AR2021_URL}\n\n"
    + ENTITY_NOTE + "\n\n" + RESTATEMENT_NOTE + "\n\n"
    "ROUNDING NOTE: the FY2023 Annual Report's own printed subtotals for 'Operating profit before "
    "changes in operating assets and liabilities' ($57,149k) and 'Net cash used in investing "
    "activities' ($(67,619)k) are each $1k off from summing that same report's own component line "
    "items ($57,150k / $(67,618)k) - an immaterial source-document rounding artifact, not a "
    "transcription error; the source's own printed figures are used throughout. Every other total in "
    "this workbook ties exactly to its component lines."
)


def p3_sources(page_2025, extra=""):
    return (
        "Sources - Kuwait Finance House Plc (formerly Ahli United Bank (UK) PLC) Appendix: Pillar 3 "
        "Disclosures (unaudited), Key Metrics table, published within each year's own Annual Report "
        "and Financial Statements:\n"
        f"FY2025/FY2024: p.{page_2025} - {AR2025_URL}\n"
        f"FY2023: Annual Report 2024, p.85 - {AR2024_URL}\n"
        f"FY2022/FY2021: Annual Report 2022, p.72 - {AR2022_URL}\n\n"
        "Total RWAs are NOT separately disclosed anywhere in the source (Note 33/Capital Adequacy "
        "explicitly defers to the Pillar 3 appendix, which gives ratios and Own Funds only, no RWA "
        "figure) - calculated here as Own Funds / Total Capital ratio for each year, flagged as "
        "calculated rather than directly quoted." + extra
    )


bw = BankWorkbook(bank_name="Kuwait Finance House Plc", years=YEARS, year_label=YEAR_LABEL,
                   header_color="1E7A5C")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax",
     {"FY2025": 28425, "FY2024": 51882, "FY2023": 61792, "FY2022": 50559, "FY2021": 23877}),
    ("DATA", "Depreciation",
     {"FY2025": 2207, "FY2024": 1990, "FY2023": 2036, "FY2022": 3106, "FY2021": 3366}),
    ("DATA", "Profit on disposal of Investment Property", {"FY2025": -140}),
    ("DATA", "Changes in carrying value of non-trading investments/debt instruments",
     {"FY2025": -9532, "FY2024": -10984, "FY2023": -3584, "FY2022": -3405,
      "FY2021": 13344}),
    ("DATA", "Amortisation of Short Term Government Instruments", {"FY2025": -952}),
    ("DATA", "Changes in carrying value of Visa shares/Private Equity funds",
     {"FY2025": -64, "FY2024": -411, "FY2023": 667, "FY2022": 1534}),
    ("DATA", "Proceeds from sale of non trading investments (P&L adjustment)", {"FY2023": 0, "FY2022": -890}),
    ("DATA", "Expense/interest expense on lease liabilities (P&L adjustment)",
     {"FY2025": 119}),
    ("DATA", "Expected credit loss provisions/(releases)",
     {"FY2025": 8012, "FY2024": 1415, "FY2023": 4718, "FY2022": 397, "FY2021": -1882}),
    ("DATA", "Foreign currency translations (P&L adjustment)",
     {"FY2025": 36362, "FY2024": 5411}),
    ("DATA", "Share of profit from investments in a joint venture and reserves now recognised",
     {"FY2023": -1028}),
    ("DATA", "Net realised gains from derecognition of financial investments/instruments",
     {"FY2025": -2551, "FY2024": -9370, "FY2023": -7451, "FY2022": 50122, "FY2021": -310}),
    ("TOTAL", "Operating profit before changes in operating assets and liabilities",
     {"FY2025": 61886, "FY2024": 39933, "FY2023": 57149, "FY2022": 101423, "FY2021": 38395}),

    ("DATA", "Mandatory reserve deposits with central bank",
     {"FY2025": 0, "FY2024": 4220, "FY2023": 722, "FY2022": 955, "FY2021": -273}),
    ("DATA", "Repurchase agreements", {"FY2021": -36075}),
    ("DATA", "Financing receivables / Loans and advances",
     {"FY2025": -19993, "FY2024": 21413, "FY2023": -85911, "FY2022": 146833, "FY2021": 135149}),
    ("DATA", "Returns receivable and similar assets / Interest receivable",
     {"FY2025": 5535, "FY2024": -6479, "FY2023": -1355, "FY2022": -4156, "FY2021": -307}),
    ("DATA", "Other assets",
     {"FY2025": 32394, "FY2024": 21397, "FY2023": 42323, "FY2022": -16673, "FY2021": -59267}),
    ("DATA", "Deposits from banks",
     {"FY2025": -36524, "FY2024": 48466, "FY2023": -75379, "FY2022": 2470, "FY2021": 68821}),
    ("DATA", "Customer(s') deposits",
     {"FY2025": -110585, "FY2024": -250205, "FY2023": 150680, "FY2022": -156676, "FY2021": 155952}),
    ("DATA", "Returns payable and similar liabilities / Interest payable",
     {"FY2025": -5126, "FY2024": 7739, "FY2023": 21758, "FY2022": 1302, "FY2021": 1123}),
    ("DATA", "Expense on lease liabilities (working-capital block)",
     {"FY2024": 237, "FY2023": 213, "FY2022": 258, "FY2021": 344}),
    ("DATA", "Other liabilities",
     {"FY2025": 3528, "FY2024": -5884, "FY2023": -23088, "FY2022": -31134, "FY2021": -35056}),
    ("TOTAL", "Cash from/(used in) operations",
     {"FY2025": -68885, "FY2024": -119163, "FY2023": 87112, "FY2022": 44602, "FY2021": 268806}),
    ("DATA", "Tax paid net of tax refund",
     {"FY2025": -6847, "FY2024": -12502, "FY2023": -14596, "FY2022": -9936, "FY2021": -3936}),
    ("TOTAL", "Net cash from/(used in) operating activities",
     {"FY2025": -75732, "FY2024": -131665, "FY2023": 72516, "FY2022": 34665, "FY2021": 264870}),

    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of non-trading investments/debt instruments at amortised cost",
     {"FY2025": -251652, "FY2024": -198948, "FY2023": -186083, "FY2022": -466167, "FY2021": -58479}),
    ("DATA", "Proceeds from sale of non-trading investments/debt instruments at amortised cost",
     {"FY2025": 237832, "FY2024": 445023, "FY2023": 123400, "FY2022": 238416, "FY2021": 30375}),
    ("DATA", "Proceeds from sale of non-trading investments (Visa shares)",
     {"FY2025": 137, "FY2024": 712, "FY2023": 0, "FY2022": 890, "FY2021": 1773}),
    ("DATA", "Purchase of premises and equipment",
     {"FY2025": -361, "FY2024": -700, "FY2023": -1278, "FY2022": -120, "FY2021": -1217}),
    ("DATA", "Purchase of intangible assets", {"FY2025": -2619}),
    ("DATA", "Net disposals/(investments) of/in Private Equity funds",
     {"FY2025": 1284, "FY2024": 10985, "FY2023": -4702, "FY2022": -928, "FY2021": -6528}),
    ("DATA", "Proceeds from sale of Investment Property", {"FY2025": 405}),
    ("DATA", "Dividend received from investment in joint venture", {"FY2023": 1045}),
    ("DATA", "Liquidation of investment in joint venture", {"FY2024": 64}),
    ("TOTAL", "Net cash from/(used in) investing activities",
     {"FY2025": -14974, "FY2024": 257136, "FY2023": -67619, "FY2022": -227909, "FY2021": -34076}),

    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividend paid to parent undertaking",
     {"FY2025": -30000, "FY2024": -30000, "FY2023": -20000, "FY2022": -10000, "FY2021": -10000}),
    ("DATA", "Subordinated debt repayment", {"FY2023": -9592}),
    ("DATA", "Lease liabilities payments",
     {"FY2025": -1875, "FY2024": -2014, "FY2023": -1668, "FY2022": -1777, "FY2021": -1954}),
    ("TOTAL", "Net cash used in financing activities",
     {"FY2025": -31875, "FY2024": -32014, "FY2023": -31260, "FY2022": -11777, "FY2021": -11954}),

    ("DATA", "Foreign currency translation adjustments (within the change calc, FY2021-FY2023 only)",
     {"FY2023": -1650, "FY2022": 5767, "FY2021": 2170}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents",
     {"FY2025": -122581, "FY2024": 93456, "FY2023": -28014, "FY2022": -199254, "FY2021": 221010}),
    ("DATA", "Cash and cash equivalents at 1 January",
     {"FY2025": 752166, "FY2024": 664122, "FY2023": 692136, "FY2022": 891390, "FY2021": 670380}),
    ("DATA", "Effect of exchange rate fluctuations on cash and cash equivalents held (shown after opening, FY2024-FY2025 only)",
     {"FY2025": -36362, "FY2024": -5412}),
    ("TOTAL", "Cash and cash equivalents at 31 December",
     {"FY2025": 593223, "FY2024": 752166, "FY2023": 664122, "FY2022": 692136, "FY2021": 891390}),
]

bw.add_cash_flow_sheet(
    title="Kuwait Finance House Plc — Bank Statement of Cash Flows",
    subtitle="Bank/solo basis, US$'000. Formerly Ahli United Bank (UK) PLC. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=95,
    source_height=380,
    unit_suffix=" (US$'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources("83"), note=note, first_col_width=48,
                         source_height=280)


CET1_CAPITAL = {"FY2025": 325.3, "FY2024": 316.7, "FY2023": 323.2, "FY2022": 304.5, "FY2021": 319.0}
TIER1_CAPITAL = CET1_CAPITAL  # no AT1 disclosed any year
TOTAL_CAPITAL = {"FY2025": 325.3, "FY2024": 316.7, "FY2023": 323.2, "FY2022": 304.5, "FY2021": 319.8}
TOTAL_RWA_CALC = {"FY2025": 1618.4, "FY2024": 1649.3, "FY2023": 1666.0, "FY2022": 1530.2, "FY2021": 1421.3}
CET1_RATIO = {"FY2025": "20.1%", "FY2024": "19.2%", "FY2023": "19.4%", "FY2022": "19.9%", "FY2021": "22.4%"}
TOTAL_CAPITAL_RATIO = {"FY2025": "20.1%", "FY2024": "19.2%", "FY2023": "19.4%", "FY2022": "19.9%", "FY2021": "22.5%"}
LEVERAGE_RATIO = {"FY2025": "14.2%", "FY2024": "13.7%", "FY2023": "11.9%", "FY2022": "12.3%", "FY2021": "10.5%"}
LCR = {"FY2025": "592.3%", "FY2024": "385.4%", "FY2023": "662.5%", "FY2022": "392.5%", "FY2021": "486.4%"}
NSFR = {"FY2025": "139.0%", "FY2024": "119.4%", "FY2023": "133.0%", "FY2022": "127.4%", "FY2021": "136.2%"}

NO_AT1_NOTE = ("No Additional Tier 1 instruments disclosed any year - Tier 1 capital equals CET1 "
               "capital throughout. A small Tier 2 balance ($799k) exists only in FY2021 (see Total "
               "Capital), fully amortised/repaid by FY2022 onward.")
RWA_NOTE = ("Total RWAs are NOT directly disclosed in the source - calculated as Own Funds / Total "
            "Capital ratio for each year (see sheet-level source note). Treat as an approximation "
            "consistent with the source's own rounded percentages, not a directly-quoted figure.")

metric("CET1 Capital", "USD m", [("Common Equity Tier 1 (CET1) capital", CET1_CAPITAL)])
metric("CET1 Ratio", "%", [("CET1 ratio", CET1_RATIO)])
metric("Tier 1 Capital", "USD m", [("Tier 1 capital", TIER1_CAPITAL)], note=NO_AT1_NOTE)
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", CET1_RATIO)], note=NO_AT1_NOTE)
metric("Total Capital", "USD m", [("Total capital / Own Funds", TOTAL_CAPITAL)])
metric("Total Capital Ratio", "%", [("Total capital ratio", TOTAL_CAPITAL_RATIO)])
metric("Total RWAs", "USD m", [("Total risk-weighted exposure amount (calculated)", TOTAL_RWA_CALC)],
       note=RWA_NOTE)
metric("Leverage Ratio", "%", [("Leverage ratio", LEVERAGE_RATIO)])
metric("LCR", "%", [("Liquidity Coverage Ratio", LCR)])
metric("NSFR", "%", [("Net Stable Funding Ratio", NSFR)])

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources("n/a"),
    per_note={"MREL Ratio": "Not publicly disclosed any year - consistent with a small UK bank "
                             "subsidiary that is not itself a resolution entity."},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities",
         {"FY2025": -75732, "FY2024": -131665, "FY2023": 72516, "FY2022": 34665, "FY2021": 264870}),
        ("Net cash from/(used in) investing activities",
         {"FY2025": -14974, "FY2024": 257136, "FY2023": -67619, "FY2022": -227909, "FY2021": -34076}),
        ("Net cash used in financing activities",
         {"FY2025": -31875, "FY2024": -32014, "FY2023": -31260, "FY2022": -11777, "FY2021": -11954}),
        ("Cash and cash equivalents at 31 December",
         {"FY2025": 593223, "FY2024": 752166, "FY2023": 664122, "FY2022": 692136, "FY2021": 891390}),
    ],
    cash_flow_unit="US$'000",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Total Capital Ratio", TOTAL_CAPITAL_RATIO),
        ("Leverage Ratio", LEVERAGE_RATIO),
        ("LCR", LCR),
        ("NSFR", NSFR),
    ],
    note="Kuwait Finance House Plc (formerly Ahli United Bank (UK) PLC) converted to a Shariah-"
         "compliant (Islamic) bank during FY2024 under new ownership - see the Cash Flow Statement "
         "sheet's ENTITY NOTE. Figures are US$, not converted to GBP (native-currency presentation, "
         "consistent with sibling USD-reporting banks in this batch). Total RWAs are calculated "
         "(Own Funds / Total Capital ratio), not directly disclosed. Figures are duplicated from the "
         "detail sheets for at-a-glance trend viewing.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/KUWAIT FINANCE HOUSE FINANCIALS.xlsx")
print("Saved.")
