import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# PILLAR-3-ONLY WORKBOOK: Bank of the Philippine Islands (Europe) PLC (company
# 05888535, FRN 455378) is a qualifying entity under FRS 102 and takes the
# Section 7 "Statement of Cash Flows" disclosure exemption every year - the
# FY2025 Annual Report's Note 3(c) "Exemptions for qualifying entities under
# FRS 102" states this explicitly: the Bank is wholly-owned by BPI (Bank of the
# Philippine Islands), which publishes a consolidated Cash Flow Statement. The
# FY2025 Independent Auditor's Report confirms the audited primary statements
# comprise only the Profit and Loss Account, the Balance Sheet, and the
# Statement of Movement in Shareholder's Funds - no cash flow statement.
# Follows the BNY Mellon International / ABC International Bank / Bank Mandiri
# (Europe) precedent: 13-sheet structure, Cash Flow Statement sheet documents
# the exemption instead of line items, Overview sheet omits the cash-flow chart.
#
# NOT the same entity as Philippine National Bank (Europe) Plc (company
# 02939223, SKIPPED earlier in this project) - different parent group (Bank of
# the Philippine Islands vs. Philippine National Bank) despite similar naming;
# confirmed independently via Companies House.
#
# GENUINE MID-SERIES FUNCTIONAL CURRENCY CHANGE: the Bank changed its
# functional/presentation currency from GBP to USD during FY2023 (the FY2023
# Annual Report's Strategic Report states the change caused a one-time $1.16m
# FX trading loss, and the FY2023 accounts' capital table is explicitly labelled
# "Restated" for the FY2022 comparative). FY2021 and FY2022's own originally-
# published figures are in GBP (no conversion needed); FY2023-FY2025 are in USD
# and are converted to £ per this project's established FX methodology. This is
# a different pattern from every prior FX case in this project (which are all
# single-currency-throughout) - only PART of the window needs conversion.

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, calendar year-end (31 December)
YEAR_LABEL = {y: y for y in YEARS}

# ---------------------------------------------------------------
# FX conversion - ONLY for FY2023-FY2025 (the USD-reporting years). FY2021 and
# FY2022 are the Bank's own originally-published £ figures, used as-is.
# Rates are Bank of England GBP/USD spot via poundsterlinglive.com's published
# archive, £1 = $X - same rate table used throughout this project's USD banks.
# ---------------------------------------------------------------
FX_SPOT = {
    "FY2023": 1.2732,  # 29 Dec 2023 (31st was a Sunday)
    "FY2024": 1.2515,  # 31 Dec 2024
    "FY2025": 1.3448,  # 31 Dec 2025
}


def stock(usd_by_year):
    """Point-in-time (capital/RWA) USD figures for FY2023-FY2025, £'000 at that
    year's period-end spot rate. Pass GBP-native FY2021/FY2022 figures separately."""
    return {y: round(v / FX_SPOT[y] / 1000, 0) for y, v in usd_by_year.items()}


FY2025_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/05888535/filing-history/MzUyMDczNTAwM2FkaXF6a2N4/document?format=pdf&download=0"
FY2023_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/05888535/filing-history/MzQyNjQ2OTQ5OGFkaXF6a2N4/document?format=pdf&download=0"
FY2022_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/05888535/filing-history/MzM3NzAxNzg2OGFkaXF6a2N4/document?format=pdf&download=0"
FY2021_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/05888535/filing-history/MzMzNzI1NDc5M2FkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "ENTITY NOTE: Bank of the Philippine Islands (Europe) PLC (\"BPI Europe\", company 05888535, FRN 455378, "
    "incorporated 27 July 2006) is a wholly-owned UK subsidiary of Bank of the Philippine Islands (BPI), one of "
    "the Philippines' largest banks. NOT the same entity as Philippine National Bank (Europe) Plc (company "
    "02939223, a different Philippine bank group's UK subsidiary, skipped earlier in this project) - confirmed "
    "via Companies House, no relationship between the two."
)

EXEMPTION_NOTE = (
    "FRS 102 CASH-FLOW EXEMPTION: the FY2025 Annual Report's Note 3(c) \"Exemptions for qualifying entities under "
    "FRS 102\" states: \"In preparing these financial statements, BPI Europe has taken advantage of the disclosure "
    "exemption on the requirement of Section 7 Statement of Cash Flows, as permitted by FRS 102... The Bank is "
    "wholly-owned by BPI, a bank incorporated in the Republic of the Philippines and which publishes a "
    "consolidated Cash Flow Statement, Balance Sheet, and Income Statement\" - "
    f"Bank of the Philippine Islands (Europe) PLC Annual Report FY2025, Note 3(c), p.38 - {FY2025_AR_URL}. The "
    "Independent Auditor's Report (p.25) confirms the audited primary statements comprise only the Profit and "
    "Loss Account, the Balance Sheet, and the Statement of Movement in Shareholder's Funds. Per the project's "
    "established policy for this exemption, this workbook is built as a PILLAR-3-ONLY variant: the capital/"
    "liquidity metrics that are disclosed are populated below, but no cash flow figures exist to show."
)

CASH_FLOW_SOURCES = ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE

CURRENCY_NOTE = (
    "CURRENCY: the Bank changed its functional/presentation currency from GBP to USD during FY2023 (confirmed in "
    "the FY2023 Annual Report's Strategic Report and its capital table's \"Restated\" FY2022 comparative). FY2021 "
    "and FY2022 monetary figures below are the Bank's own originally-published £ figures (Companies House filings "
    "for those years, in GBP) - not converted. FY2023-FY2025 are originally reported in USD and are converted to "
    "£ at the Bank of England GBP/USD spot rate as at each fiscal year-end (29 Dec 2023 1.2732 - 31st was a "
    "Sunday; 31 Dec 2024 1.2515; 31 Dec 2025 1.3448). % ratios are shown exactly as reported in either currency, "
    "never converted (dimensionless)."
)


def p3_sources(extra=""):
    return (
        "Sources - Bank of the Philippine Islands (Europe) PLC, Strategic Report \"Capital Resources\"/\"Liquidity "
        "Resources\" narrative and the Notes' \"Capital Adequacy\" components table, from each year's own Annual "
        "Report filed at Companies House (all 5 filings fully scanned/image-only, OCR'd):\n"
        f"FY2025 & FY2024: Annual Report FY2025, Strategic Report p.7, Note 21 components table p.9-10 - {FY2025_AR_URL}\n"
        f"FY2023 & FY2022 (restated): Annual Report FY2023, Strategic Report p.7-8, components table p.9-10 - {FY2023_AR_URL}\n"
        f"FY2022 (as originally reported, £) & FY2021: Annual Report FY2022, Strategic Report p.5-6, components table p.7 - {FY2022_AR_URL}\n"
        f"FY2021 (as originally reported, £) & FY2020: Annual Report FY2021, Strategic Report p.5-6, components table p.7 - {FY2021_AR_URL}\n"
        + (extra + "\n" if extra else "")
        + CURRENCY_NOTE
    )


NOT_DISCLOSED_NOTE = (
    "No dedicated Pillar 3 document is published by this entity - all capital/liquidity figures come from each "
    "Annual Report's own Strategic Report narrative and Notes. This metric is not disclosed in any of the 5 "
    "Annual Reports checked (FY2021-FY2025)."
)

bw = BankWorkbook(bank_name="Bank of the Philippine Islands (Europe) PLC", years=YEARS, year_label=YEAR_LABEL, header_color="0057B7")

# ---------------------------------------------------------------
# ST- new sheets: Balance Sheet / P&L / Statement of Changes in Equity /
# Asset Quality / RWA Breakdown. Sourced from the same 3 Annual Reports
# already cited above (FY2025 AR gives FY2025+FY2024; FY2023 AR gives
# FY2023 own-year; FY2022 AR gives FY2022+FY2021, both £ native). FY2023-25
# are originally reported in USD (own report, own year) and converted to £
# at that year's own period-end spot rate (same FX_SPOT table and stock()
# helper already used for the capital/RWA sheets above) - applied here to
# BOTH stock (Balance Sheet, Equity) and flow (P&L) figures for internal
# sheet-to-sheet consistency, since no separate period-average rate table
# exists for this entity; flagged as an approximation, not a true average.
# ---------------------------------------------------------------
BS_PL_SOURCES = (
    ENTITY_NOTE + "\n\n" +
    "Sources - Bank of the Philippine Islands (Europe) PLC, Balance Sheet / Profit and Loss Account / Statement "
    "of Movement in Shareholder's Funds, from each year's own Annual Report filed at Companies House (all 3 "
    "filings fully scanned/image-only, visually transcribed):\n"
    f"FY2025 & FY2024: Annual Report FY2025, pp.35-37 - {FY2025_AR_URL}\n"
    f"FY2023: Annual Report FY2023, pp.28-30 - {FY2023_AR_URL}\n"
    f"FY2022 & FY2021: Annual Report FY2022, pp.26-28 (both years shown as primary/comparative in that one "
    f"report) - {FY2022_AR_URL}\n"
    + CURRENCY_NOTE + " The same period-end spot rate is applied here to P&L (flow) figures as an approximation, "
    "since no separate period-average GBP/USD rate table exists for this entity."
)

def gbp(usd_by_year):
    return {y: round(v / FX_SPOT[y]) for y, v in usd_by_year.items()}

# --- Balance Sheet ---------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash", {**gbp({"FY2025": 4042, "FY2024": 5029, "FY2023": 10}), "FY2022": 680, "FY2021": 4443}),
    ("DATA", "Loans and advances to banks", {**gbp({"FY2025": 10226245, "FY2024": 2725089, "FY2023": 3736215}), "FY2022": 10590380, "FY2021": 8215760}),
    ("DATA", "Loans and advances to customers", {**gbp({"FY2025": 121682050, "FY2024": 73129828, "FY2023": 74751736}), "FY2022": 84804657, "FY2021": 43461929}),
    ("DATA", "Amounts due from group undertakings", {**gbp({"FY2025": 13472, "FY2024": 19057, "FY2023": 39521}), "FY2022": 23882, "FY2021": 9094569}),
    ("DATA", "Investment in securities", {**gbp({"FY2025": 151146088, "FY2024": 151772387, "FY2023": 121881874}), "FY2022": 89860760, "FY2021": 98421761}),
    ("DATA", "Derivative assets", {**gbp({"FY2025": 315365, "FY2024": 395392, "FY2023": 17192}), "FY2022": 1524834, "FY2021": 336406}),
    ("DATA", "Tangible fixed assets", {**gbp({"FY2025": 108352, "FY2024": 139257, "FY2023": 130877}), "FY2022": 42965, "FY2021": 75625}),
    ("DATA", "Deferred tax asset", {**gbp({"FY2025": 148706, "FY2024": 451474, "FY2023": 254694})}),
    ("DATA", "Other assets", {**gbp({"FY2025": 247527, "FY2024": 226234, "FY2023": 220331}), "FY2022": 301688, "FY2021": 304722}),
    ("TOTAL", "Total assets", {**gbp({"FY2025": 283891847, "FY2024": 228863747, "FY2023": 201032450}), "FY2022": 187149846, "FY2021": 159915215}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from customers", {**gbp({"FY2025": 142032600, "FY2024": 88970695, "FY2023": 1696057}), "FY2022": 1180161, "FY2021": 1291370}),
    ("DATA", "Bank borrowings", {**gbp({"FY2025": 5005375, "FY2024": 1790256, "FY2023": 61998461}), "FY2022": 67708294, "FY2021": 42276046}),
    ("DATA", "Amounts due to group undertakings", {**gbp({"FY2025": 13716745, "FY2024": 15306531, "FY2023": 14088060}), "FY2022": 14274996, "FY2021": 10915712}),
    ("DATA", "Amounts due to other banks", {"FY2022": 1120704, "FY2021": 2020426}),
    ("DATA", "Derivative liabilities", {**gbp({"FY2025": 475266, "FY2024": 1061512, "FY2023": 853975}), "FY2022": 661433, "FY2021": 1114662}),
    ("DATA", "Deferred tax liability", {"FY2022": 193}),
    ("DATA", "Other liabilities", {**gbp({"FY2025": 443968, "FY2024": 449537, "FY2023": 510335}), "FY2022": 320976, "FY2021": 395657}),
    ("TOTAL", "Total liabilities", {**gbp({"FY2025": 161673954, "FY2024": 107578531, "FY2023": 79146888}), "FY2022": 85266757, "FY2021": 58013873}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {**gbp({"FY2025": 120390000, "FY2024": 120390000, "FY2023": 120390000}), "FY2022": 100000000, "FY2021": 100000000}),
    ("DATA", "Profit and loss account", {**gbp({"FY2025": 1827893, "FY2024": 895216, "FY2023": 1495562}), "FY2022": 1883089, "FY2021": 1901342}),
    ("TOTAL", "Total shareholder's funds", {**gbp({"FY2025": 122217893, "FY2024": 121285216, "FY2023": 121885562}), "FY2022": 101883089, "FY2021": 101901342}),
]

bw.add_balance_sheet_sheet(
    title="Bank of the Philippine Islands (Europe) PLC — Consolidated Statement of Financial Position",
    subtitle="£-equivalent, whole pounds (FY2021-22 £ native, FY2023-25 converted from USD at period-end spot)",
    rows=balance_sheet_rows,
    sources_text=BS_PL_SOURCES,
    first_col_width=46,
    source_height=210,
    unit_suffix=" (£)",
)

# --- Profit & Loss -----------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable and similar income", {**gbp({"FY2025": 11283426, "FY2024": 8343493, "FY2023": 8749221}), "FY2022": 4823824, "FY2021": 1977005}),
    ("DATA", "Interest payable and similar charges", {**gbp({"FY2025": -6228718, "FY2024": -4641394, "FY2023": -5116017}), "FY2022": -1887599, "FY2021": -341865}),
    ("TOTAL", "Net interest income", {**gbp({"FY2025": 5054708, "FY2024": 3702099, "FY2023": 3633204}), "FY2022": 2936225, "FY2021": 1635140}),
    ("DATA", "Fees and commission income", {**gbp({"FY2025": 41562, "FY2024": 141289, "FY2023": 22362}), "FY2022": 91623, "FY2021": 44019}),
    ("DATA", "Foreign exchange gain/(loss)", {**gbp({"FY2025": -420330, "FY2024": 127927, "FY2023": -760974}), "FY2022": -68042, "FY2021": 636230}),
    ("DATA", "Gain/(loss) on sale/FV of investments", {**gbp({"FY2025": 1066619, "FY2024": 504529, "FY2023": 71503}), "FY2022": -506419, "FY2021": 267358}),
    ("DATA", "Loss on sale of syndicated loan", {**gbp({"FY2023": -383713})}),
    ("DATA", "Other operating income/(loss)", {**gbp({"FY2025": 3231, "FY2024": 17758, "FY2023": 2226}), "FY2022": 2855, "FY2021": -5172}),
    ("TOTAL", "Operating income", {**gbp({"FY2025": 5745790, "FY2024": 4493602, "FY2023": 2584608}), "FY2022": 2456242, "FY2021": 2577575}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Administrative expenses", {**gbp({"FY2025": -4345837, "FY2024": -3610660, "FY2023": -3550817}), "FY2022": -2344707, "FY2021": -2029872}),
    ("DATA", "Depreciation", {**gbp({"FY2025": -32989, "FY2024": -30774, "FY2023": -44436}), "FY2022": -45850, "FY2021": -44704}),
    ("DATA", "Impairment charges", {**gbp({"FY2025": -131519, "FY2024": -1649293, "FY2023": -15771}), "FY2022": -82437, "FY2021": -50172}),
    ("TOTAL", "Profit/(loss) on ordinary activities before taxation", {**gbp({"FY2025": 1235445, "FY2024": -797125, "FY2023": -1026416}), "FY2022": -16752, "FY2021": 452827}),
    ("DATA", "Income tax (charge)/credit", {**gbp({"FY2025": -302768, "FY2024": 196779, "FY2023": 254927}), "FY2022": -1635, "FY2021": -79972}),
    ("TOTAL", "Profit/(loss) for the financial year", {**gbp({"FY2025": 932677, "FY2024": -600346, "FY2023": -771489}), "FY2022": -18387, "FY2021": 372855}),
]

bw.add_income_statement_sheet(
    title="Bank of the Philippine Islands (Europe) PLC — Consolidated Statement of Comprehensive Income",
    subtitle="£-equivalent, whole pounds (FY2021-22 £ native, FY2023-25 converted from USD at period-end spot); "
             "no separate OCI - the Bank has no comprehensive income/expense beyond the P&L result each year.",
    rows=income_statement_rows,
    sources_text=BS_PL_SOURCES,
    first_col_width=52,
    source_height=210,
    unit_suffix=" (£)",
)

# --- Statement of Changes in Equity (chronological) ---------------------
EQUITY_HEADERS = ["Called up share capital", "Profit and loss account", "Total shareholder's funds"]
equity_changes_rows = [
    ("TOTAL", "Balance as at 1 January 2021", (40000000, 1528487, 41528487)),
    ("DATA", "Additional share capital", (60000000, 0, 60000000)),
    ("DATA", "Profit for the year", (0, 372855, 372855)),
    ("TOTAL", "Balance as at 31 December 2021", (100000000, 1901342, 101901342)),
    ("DATA", "Loss for the year", (0, -18387, -18387)),
    ("DATA", "Prior period adjustment", (0, 134, 134)),
    ("TOTAL", "Balance as at 31 December 2022", (100000000, 1883089, 101883089)),
    ("DATA", "FX translation effect (GBP->USD functional currency change), net", (-5442978, -102496, -5545474)),
    ("DATA", "Loss for the year", (0, -605945, -605945)),
    ("TOTAL", "Balance as at 31 December 2023", (94557022, 1174648, 95731670)),
    ("DATA", "FX retranslation of USD balances at period-end spot, net", (1639542, 20367, 1659909)),
    ("DATA", "Loss for the year", (0, -479701, -479701)),
    ("TOTAL", "Balance as at 31 December 2024", (96196564, 715314, 96911879)),
    ("DATA", "FX retranslation of USD balances at period-end spot, net", (-6673958, -49627, -6723585)),
    ("DATA", "Profit for the year", (0, 693543, 693543)),
    ("TOTAL", "Balance as at 31 December 2025", (89522606, 1359230, 90881836)),
]

EQUITY_SOURCES = (
    BS_PL_SOURCES + "\n\n"
    "EQUITY-SHEET-SPECIFIC NOTE: FY2021-22 rows are the Bank's own originally-published £ figures (no "
    "conversion). The Bank changed its functional/presentation currency from GBP to USD during FY2023; rather "
    "than force a single continuous £ or $ figure through that boundary, the two 'FX translation effect'/'FX "
    "retranslation' rows are plug figures that make each year's £-equivalent closing balance tie exactly to that "
    "year's own Annual Report (itself USD, converted at that year's period-end spot rate) - they are not a "
    "disclosed line item, they are this workbook's own reconciling entry, shown explicitly rather than hidden. "
    "Note the 'Called up share capital' column moves every USD year purely from FX retranslation - the "
    "underlying $120,390,000 balance itself has been unchanged since FY2023."
)

bw.add_equity_changes_sheet(
    title="Bank of the Philippine Islands (Europe) PLC — Statement of Changes in Equity",
    subtitle="£-equivalent, whole pounds, chronological (FY2021-22 £ native, FY2023-25 converted from USD at period-end spot)",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQUITY_SOURCES,
)

# --- Asset Quality -------------------------------------------------------
ASSET_QUALITY_SOURCES = (
    ENTITY_NOTE + "\n\n" +
    "Sources - Bank of the Philippine Islands (Europe) PLC, \"Loans and advances to customers\" note "
    "(Note 14 in the FY2025 AR, Note 12 in the FY2023 AR, Note 11 in the FY2022 AR) and its \"Impairment "
    "Charge\"/\"Movement in provision for impairment\" note, from each year's own Annual Report:\n"
    f"FY2025 & FY2024: Annual Report FY2025, Notes 13-14, pp.48-49 - {FY2025_AR_URL}\n"
    f"FY2023: Annual Report FY2023, Note 12, p.40 - {FY2023_AR_URL}\n"
    f"FY2022 & FY2021: Annual Report FY2022, Note 11, p.38 - {FY2022_AR_URL}\n"
    + CURRENCY_NOTE + "\n\n"
    "NO IFRS 9 STAGE BREAKDOWN: this entity applies a simple FRS 102 impairment model (a single collective "
    "provision across the performing loan book, plus occasional specific provisions - see the FY2025 Auditor's "
    "Report's Key Audit Matter: \"the loan portfolio is performing, and no specific provision has been "
    "assessed\"). No Stage 1/2/3 staging table is disclosed in any of the 5 years checked, so this sheet shows "
    "the loan book by product plus the collective/specific provision split instead. NOTE: the FY2025 AR's "
    "impairment-movement note (Note 13) no longer breaks the provision into Collective/Specific columns - only a "
    "single combined \"Provision for impairment\" figure is disclosed for FY2025/FY2024 (the Total provision row "
    "below is populated for those years; the Collective/Specific split rows are left blank rather than assumed)."
)

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, by product", {}),
    ("DATA", "Corporate loans", {**gbp({"FY2025": 121823428, "FY2024": 73139687, "FY2023": 74975584}), "FY2022": 84977493, "FY2021": 43552328}),
    ("DATA", "Other retail loans", {**gbp({"FY2025": 1, "FY2024": 1, "FY2023": 1}), "FY2022": 1, "FY2021": 1}),
    ("TOTAL", "Gross loans and advances to customers", {**gbp({"FY2025": 121823429, "FY2024": 73139688, "FY2023": 74975585}), "FY2022": 84977494, "FY2021": 43552329}),
    ("SECTION", "Provision for impairment", {}),
    ("DATA", "Collective provision", {**gbp({"FY2023": -223848}), "FY2022": -172836, "FY2021": -90399}),
    ("DATA", "Specific provision", {**gbp({"FY2023": -1}), "FY2022": -1, "FY2021": -1}),
    ("TOTAL", "Total provision for impairment", {**gbp({"FY2025": -141379, "FY2024": -9860, "FY2023": -223849}), "FY2022": -172837, "FY2021": -90400}),
    ("TOTAL", "Net loans and advances to customers", {**gbp({"FY2025": 121682050, "FY2024": 73129828, "FY2023": 74751736}), "FY2022": 84804657, "FY2021": 43461929}),
    ("SECTION", "Ratio", {}),
    ("DATA", "Provision coverage (total provision / gross loans)", {"FY2025": "0.12%", "FY2024": "0.01%", "FY2023": "0.30%", "FY2022": "0.20%", "FY2021": "0.21%"}),
]

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (exemption note in place of line items)
# ---------------------------------------------------------------
rows = [
    ("SECTION", "No Statement of Cash Flows is published by this entity in any year", {}),
    ("DATA", "See the note below for the FRS 102 exemption this entity relies on every year, and why this "
             "workbook is built as a Pillar-3-only variant.", {}),
]

bw.add_cash_flow_sheet(
    title="Bank of the Philippine Islands (Europe) PLC — Cash Flow Statement",
    subtitle="Not applicable — this entity takes the FRS 102 cash-flow-statement disclosure exemption every year. See source note below.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=320,
    unit_suffix=" (£'000)",
)

bw.add_asset_quality_sheet(
    title="Bank of the Philippine Islands (Europe) PLC — Asset Quality / Credit Risk Disclosures",
    subtitle="£-equivalent, whole pounds (FY2021-22 £ native, FY2023-25 converted from USD at period-end spot); "
             "no IFRS 9 stage-level breakdown is disclosed - see source note",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=52,
    source_height=260,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=190)


# Own Funds = Tier 1 Capital = CET1 Capital every year (no AT1/Tier 2 instruments)
OWN_FUNDS_USD = {"FY2025": 122_218_000, "FY2024": 121_886_000, "FY2023": 121_737_000}
OWN_FUNDS_GBP = stock(OWN_FUNDS_USD)
OWN_FUNDS_GBP.update({"FY2022": 101_839, "FY2021": 101_528})  # £'000, as originally reported

CAPITAL_RATIO = {"FY2025": "56.29%", "FY2024": "61.59%", "FY2023": "68.24%", "FY2022": "60.19%", "FY2021": "76.79%"}

CRWA_USD = {"FY2025": 202_285_000, "FY2024": 183_493_000, "FY2023": 163_978_000}
MRWA_USD = {"FY2025": 8_513_000, "FY2024": 8_688_000, "FY2023": 8_665_000}
ORWA_USD = {"FY2025": 6_325_000, "FY2024": 5_725_000, "FY2023": 5_750_000}
TOTAL_RWA_USD = {"FY2025": 217_123_000, "FY2024": 197_906_000, "FY2023": 178_393_000}

CRWA_GBP = stock(CRWA_USD); CRWA_GBP.update({"FY2022": 152_940, "FY2021": 119_123})
MRWA_GBP = stock(MRWA_USD); MRWA_GBP.update({"FY2022": 11_838, "FY2021": 8_938})
ORWA_GBP = stock(ORWA_USD); ORWA_GBP.update({"FY2022": 4_400, "FY2021": 4_150})
TOTAL_RWA_GBP = stock(TOTAL_RWA_USD); TOTAL_RWA_GBP.update({"FY2022": 169_178, "FY2021": 132_211})

LCR = {"FY2025": "206%", "FY2024": "329%", "FY2023": "410%", "FY2022": "166%", "FY2021": "224%"}
NSFR = {"FY2025": "154%", "FY2024": "163%", "FY2023": "117%", "FY2022": "119%"}  # FY2021: see note below
LEVERAGE = {"FY2025": "51.22%", "FY2024": "58.71%", "FY2023": "64.62%"}  # FY2022/FY2021: not disclosed

# ---------------------------------------------------------------
# KM1 Key Metrics - NOT APPLICABLE. This entity publishes no Pillar 3
# document and therefore no KM1 template. Documented rather than omitted, so
# the absence is a finding rather than a gap.
#
# The evidence is positive, not the result of a search that came up empty:
# the entity has no website of its own (bpieurope.com and bpieurope.co.uk do
# not resolve to it - the .com belongs to an unrelated plastics company, and
# the only PDFs Wayback holds for either host are that company's product
# sheets), so Companies House is the entity's complete public record, and all
# five FY2021-FY2025 filings there were read: each contains only the Annual
# Report, with capital and liquidity figures in the Strategic Report narrative
# and the Capital Adequacy note. No Pillar 3 document has ever been filed.
#
# THE DECOY: the Philippine parent, Bank of the Philippine Islands, publishes
# extensive Basel III disclosures under BSP rules. Those are a different legal
# entity, a different consolidation and a different regulator, and under this
# project's entity-basis rule they must never be used here. Note also that
# this bank is NOT Philippine National Bank (Europe) Plc, a separate
# PRA-authorised entity with a similar name and a different parent.
# ---------------------------------------------------------------
KM1_SOURCES = (
    "Sources — none. Bank of the Philippine Islands (Europe) PLC publishes NO Pillar 3 disclosure, and "
    "therefore no UK KM1 key-metrics template, for any year in this workbook.\n\n"
    "Evidence, re-checked 2026-09-16:\n"
    "• The entity has no website of its own. bpieurope.co.uk does not resolve; bpieurope.com resolves to an "
    "unrelated plastics manufacturer, and the only PDFs the Wayback Machine holds for that host are its "
    "product certificates. There is therefore no investor or regulatory-disclosures page to check, and no "
    "blocked host behind which a document could be hiding.\n"
    "• Companies House (company 05888535) is consequently the entity's complete public record. All five "
    "FY2021–FY2025 filings were read: each is an Annual Report only. No Pillar 3 document has ever been "
    "filed, and no key-metrics table of any kind appears in any of them.\n"
    "• Every capital and liquidity figure in this workbook comes instead from each Annual Report's own "
    "Strategic Report 'Capital Resources' / 'Liquidity Resources' narrative and the Capital Adequacy note, "
    "as cited on the individual Pillar 3 metric sheets.\n\n"
    "DO NOT SUBSTITUTE THE PARENT. Bank of the Philippine Islands publishes extensive Basel III disclosures "
    "under Bangko Sentral ng Pilipinas rules. That is a different legal entity, a different consolidation and "
    "a different regulator; using it here would breach the entity-basis rule this workbook follows "
    "throughout. Separately, this bank is NOT Philippine National Bank (Europe) Plc (company 02939223), a "
    "distinct PRA-authorised entity with a similar name and a different parent group.\n\n"
    "The Annual Report figures are deliberately NOT reassembled into a KM1 shape here. This sheet reproduces "
    "a published template; a table built from an annual report would look like one without being one, and its "
    "row 4 in particular would not be the total risk exposure amount the PRA template defines."
)

bw.add_km1_sheet(
    title="Bank of the Philippine Islands (Europe) PLC — KM1 Key Metrics",
    subtitle="Not applicable — this entity publishes no Pillar 3 disclosure, and so no UK KM1 key-metrics "
             "template, in any year. The absence is documented rather than left blank; the entity has no "
             "website, so its Companies House filings are its complete public record and all five were "
             "checked. The Philippine parent's Basel III disclosures are a different entity and are "
             "deliberately not used.",
    rows=[
        ("DATA", "UK KM1 key-metrics template", {y: "Not published by this entity" for y in YEARS}),
    ],
    sources_text=KM1_SOURCES,
    first_col_width=46,
    source_height=280,
)

metric("CET1 Capital", "£'000 (FY2021-22 £ native, FY2023-25 conv. from USD)",
       [("Common Equity Tier 1 (CET1) Capital", OWN_FUNDS_GBP)], p3_sources())

metric("CET1 Ratio", "% of Total Risk Exposure Amount",
       [("CET1 Capital Ratio", CAPITAL_RATIO)], p3_sources(),
       note="CET1 = Tier 1 = Total Capital every year - the Bank holds no AT1 or Tier 2 instruments.")

metric("Tier 1 Capital", "£'000 (FY2021-22 £ native, FY2023-25 conv. from USD)",
       [("Tier 1 Capital", OWN_FUNDS_GBP)], p3_sources())

metric("Tier 1 Ratio", "% of Total Risk Exposure Amount",
       [("Tier 1 Capital Ratio", CAPITAL_RATIO)], p3_sources())

metric("Total Capital", "£'000 (FY2021-22 £ native, FY2023-25 conv. from USD)",
       [("Own Funds / Total Capital", OWN_FUNDS_GBP)], p3_sources())

metric("Total Capital Ratio", "% of Total Risk Exposure Amount",
       [("Total Capital Ratio", CAPITAL_RATIO)], p3_sources())

metric("Total RWAs", "£'000 (FY2021-22 £ native, FY2023-25 conv. from USD)",
       [
           ("Total Credit Risk-Weighted Assets (CRWA)", CRWA_GBP),
           ("Total Market Risk-Weighted Assets (MRWA)", MRWA_GBP),
           ("Total Operational Risk-Weighted Assets (ORWA)", ORWA_GBP),
           ("Total Risk Exposure Amount", TOTAL_RWA_GBP),
       ], p3_sources())

rwa_breakdown_rows = [
    ("DATA", "Total Credit Risk-Weighted Assets (CRWA)", CRWA_GBP),
    ("DATA", "Total Market Risk-Weighted Assets (MRWA)", MRWA_GBP),
    ("DATA", "Total Operational Risk-Weighted Assets (ORWA)", ORWA_GBP),
    ("TOTAL", "Total Risk Exposure Amount", TOTAL_RWA_GBP),
]
bw.add_rwa_breakdown_sheet(
    title="Bank of the Philippine Islands (Europe) PLC — RWA Breakdown",
    subtitle="£'000-equivalent (FY2021-22 £ native, FY2023-25 conv. from USD) — reuses the same CRWA/MRWA/ORWA "
             "components already broken out on the Total RWAs sheet",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources(),
    first_col_width=52,
    source_height=190,
    unit_suffix=" (£'000)",
)

metric("Leverage Ratio", "%", [("Leverage Ratio", LEVERAGE)], p3_sources(),
       note="Not disclosed for FY2021/FY2022 in either Annual Report - left blank, not estimated.")

metric("LCR", "%", [("Liquidity Coverage Ratio (LCR)", LCR)], p3_sources(),
       note="No £/$ HQLA/outflow breakdown is disclosed anywhere - only the ratio itself.")

metric("NSFR", "%", [("Net Stable Funding Ratio (NSFR)", NSFR)], p3_sources(),
       note="FY2021: not disclosed - the FY2021 and FY2022 Annual Reports both describe the Bank securing "
            "long-term borrowings \"to comply with the requirements of Net Stable Funding Ratio (NSFR), ahead "
            "of its full implementation in 2022\", i.e. NSFR was not yet a tracked/reported metric for FY2021.")

# GA-020 (2026-09-19): all five Companies House accounts FY2021-FY2025 (image-only;
# FY2024's own filing, 57pp, filed 12 May 2025, id MzQ2NTc1OTE5MmFkaXF6a2N4, was
# fetched as well) OCR'd in full at 150dpi: 0 hits for MREL / eligible
# liabilities / loss absorbing (positive control 60-66 'capital' hits each).
# The entity publishes no Pillar 3 (see KM1 note: no website; CH filings are its
# complete public record).
BPI_MREL = {y: ("Not published – no MREL figure or statement in this year's Companies House accounts (all pages "
                "OCR'd 2026-09-19); the entity publishes no Pillar 3") for y in YEARS}
bw.add_not_disclosed_metric_sheets(["MREL Ratio"], p3_sources(), per_note={"MREL Ratio": NOT_DISCLOSED_NOTE},
                                   statements={"MREL Ratio": BPI_MREL})

# ---------------------------------------------------------------
# Overview sheet (Pillar-3-only: no cash-flow chart)
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("Total Capital Ratio", CAPITAL_RATIO),
        ("LCR", LCR),
        ("NSFR", NSFR),
    ],
    balance_sheet_totals=[
        ("Total assets", {**gbp({"FY2025": 283891847, "FY2024": 228863747, "FY2023": 201032450}), "FY2022": 187149846, "FY2021": 159915215}),
        ("Loans and advances to customers", {**gbp({"FY2025": 121682050, "FY2024": 73129828, "FY2023": 74751736}), "FY2022": 84804657, "FY2021": 43461929}),
        ("Deposits from customers", {**gbp({"FY2025": 142032600, "FY2024": 88970695, "FY2023": 1696057}), "FY2022": 1180161, "FY2021": 1291370}),
        ("Total shareholder's funds", {**gbp({"FY2025": 122217893, "FY2024": 121285216, "FY2023": 121885562}), "FY2022": 101883089, "FY2021": 101901342}),
    ],
    # UNIT (corrected 2026-09-16, research/RESUME_fx_scale_sweep.md): these three
    # Overview blocks carry WHOLE POUNDS, copied cell-for-cell from the Balance
    # Sheet / Profit & Loss / Statement of Changes in Equity sheets, whose own
    # subtitles say "£-equivalent, whole pounds". They were labelled "£'000-
    # equivalent", a 1000x overstatement to any reader and to scripts/insights/
    # (extract_metrics.py parses this label and the in040/in041/build_deliverable
    # consumers scale by it). The FIGURES are right; only the labels were wrong,
    # so only the labels changed. NB the Pillar 3 metric sheets and the RWA
    # Breakdown really ARE £'000 - this workbook genuinely mixes the two scales,
    # which is why each label has to be stated separately and correctly.
    balance_sheet_unit="£-equivalent, whole pounds",
    income_statement_totals=[
        ("Operating income", {**gbp({"FY2025": 5745790, "FY2024": 4493602, "FY2023": 2584608}), "FY2022": 2456242, "FY2021": 2577575}),
        ("Total operating expense", {**gbp({"FY2025": -4510345, "FY2024": -5290727, "FY2023": -3611024}), "FY2022": -2472994, "FY2021": -2124748}),
        ("Profit/(loss) for the year", {**gbp({"FY2025": 932677, "FY2024": -600346, "FY2023": -771489}), "FY2022": -18387, "FY2021": 372855}),
    ],
    income_statement_unit="£-equivalent, whole pounds",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 96911879, "FY2024": 95731670, "FY2023": 101883089, "FY2022": 101901342, "FY2021": 41528487}),
        ("Total comprehensive income", {"FY2025": 693543, "FY2024": -479701, "FY2023": -605945, "FY2022": -18387, "FY2021": 372855}),
        ("Other equity movements, net", {"FY2025": -6723585, "FY2024": 1659909, "FY2023": -5545474, "FY2022": 134, "FY2021": 60000000}),
        ("Closing equity", {**gbp({"FY2025": 122217893, "FY2024": 121285216, "FY2023": 121885562}), "FY2022": 101883089, "FY2021": 101901342}),
    ],
    equity_changes_unit="£-equivalent, whole pounds (native/converted per year - see Statement of Changes in Equity sheet)",
    note="This is a PILLAR-3-ONLY workbook: BPI Europe takes the FRS 102 cash-flow-statement exemption every year "
         "(see the Cash Flow Statement sheet), so no cash flow summary or chart is shown here. Also note a genuine "
         "mid-series functional-currency change (GBP through FY2022, USD from FY2023) - monetary figures on the "
         "capital/RWA sheets and on the Balance Sheet/P&L/Equity/Asset Quality sheets are on a mixed "
         "native/converted basis across the window; see each sheet's own source note and the CURRENCY note there "
         "for the exact treatment. UNIT WARNING: this workbook uses TWO scales, and each sheet states its own. "
         "The Balance Sheet, Profit & Loss, Statement of Changes in Equity and Asset Quality sheets - and the "
         "three blocks above, which are copies of them - are in WHOLE POUNDS. The Pillar 3 capital/RWA sheets "
         "and the RWA Breakdown are in £'000. Until 2026-09-16 the three blocks above were mislabelled "
         "\"£'000-equivalent\" while carrying whole-pound values; the labels were corrected and no figure was "
         "changed.The Equity block's 'Other equity movements, net' line absorbs both real equity "
         "events (e.g. FY2021's £60m share issuance) and the FX retranslation plugs documented on the Statement "
         "of Changes in Equity sheet - see that sheet for the breakdown. % ratios are unaffected by the currency "
         "change.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BANK OF THE PHILIPPINE ISLANDS EUROPE FINANCIALS.xlsx")
