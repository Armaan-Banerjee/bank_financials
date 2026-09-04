import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2021_URL = "https://cdn.craft.cloud/019db931-b985-7148-ac09-8f1d1e20d1a6/assets/content/hampden/content/Hampden-Co-Annual-Report-2021.pdf"
AR2022_URL = "https://cdn.craft.cloud/019db931-b985-7148-ac09-8f1d1e20d1a6/assets/content/hampden/content/Hampden-Co-2022-Annual-Report-and-Financial-Statements.pdf"
AR2023_URL = "https://cdn.craft.cloud/019db931-b985-7148-ac09-8f1d1e20d1a6/assets/content/hampden/content/Hampden-Co-Annual-Report-and-Financial-Statements-2023.pdf"
AR2024_URL = "https://cdn.craft.cloud/019db931-b985-7148-ac09-8f1d1e20d1a6/assets/content/hampden/content/Hampden-Bank-Annual-Report-and-Financial-Statements-2024.pdf"
AR2025_URL = "https://cdn.craft.cloud/019db931-b985-7148-ac09-8f1d1e20d1a6/assets/content/hampden/content/Hampden_Bank_Annual_Report_2025_2026-06-09-100801_cggc.pdf"

P3_2021_URL = "https://hampdenandco.com/content/hampden/content/Hampden-Co-plc-2021-Pillar-3-Disclosures-FINAL.pdf"
P3_2022_URL = "https://hampdenandco.com/content/hampden/content/Hampden-Co-2022-Pillar-3-Disclosures.pdf"
P3_2023_URL = "https://cdn.craft.cloud/019db931-b985-7148-ac09-8f1d1e20d1a6/assets/content/hampden/content/Hampden-Co-plc-2023-Pillar-3-Disclosures.pdf"

ENTITY_NOTE = (
    "Hampden & Co Plc (Companies House SC386922, FRN 606934) is a small Edinburgh-based private/relationship "
    "banking group; it began trading as 'Hampden Bank' during 2025/2026 but the legal entity name and company "
    "number are unchanged - confirmed via the entity's own 'about us' page. The cash flow statement's presentation "
    "structure genuinely changes mid-series: FY2021-FY2022 present operating activities as a single reconciliation "
    "block; FY2023 onward split it into a 'Cash generated from operations' subtotal followed by a separate "
    "'Changes in operating assets and liabilities' block and a final operating subtotal (with 'Tax paid' appearing "
    "as its own line from FY2024). Each year is kept on its own as-disclosed structure rather than forced into a "
    "single row set. All comparative-year figures cross-checked against each year's own originally-published "
    "report - no restatements found anywhere in the 5-year window."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Hampden & Co Plc's own Statement of Cash Flows, as filed with Companies House:\n"
    f"FY2025: Hampden Bank Annual Report and Financial Statements 2025, p.49 (Statement of cash flows) - {AR2025_URL}\n"
    f"FY2024: Hampden Bank Annual Report and Financial Statements 2024, p.51 (Statement of cash flows) - {AR2024_URL}\n"
    f"FY2023: Hampden & Co Plc Annual Report and Financial Statements 2023, p.44 (Statement of cash flows) - {AR2023_URL}\n"
    f"FY2022: Hampden & Co Plc Annual Report and Financial Statements 2022, p.45 (Statement of cash flows) - {AR2022_URL}\n"
    f"FY2021: Hampden & Co Plc Annual Report and Financial Statements 2021, p.56 (Statement of cash flows) - {AR2021_URL}\n"
    + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - Hampden & Co Plc Pillar 3 Disclosures (Article 447/UK KM1 Key Metrics table unless noted):\n"
        f"FY2023/FY2022: Pillar 3 Disclosures for the year ended 31 December 2023, p.5-6 (UK KM1 Key metrics table) - {P3_2023_URL}\n"
        f"FY2021: Pillar 3 Disclosures for the year ended 31 December 2021 (pre-KM1 format), p.15 'Table 4: Capital resources' "
        f"and p.18 leverage ratio and p.26 'Table 15: Liquidity coverage ratio' - {P3_2021_URL}\n"
        "FY2024/FY2025: no standalone Pillar 3 document was found published for either year (last located Pillar 3 disclosure "
        "covers FY2023) - Total Capital Ratio only is sourced from each year's own Annual Report Key Performance Indicators "
        f"table instead (FY2024 AR p.7, FY2025 AR p.11) - {AR2024_URL} / {AR2025_URL}. All other metrics are not publicly "
        "disclosed for FY2024/FY2025."
    )


bw = BankWorkbook(bank_name="Hampden & Co Plc", years=YEARS, year_label=YEAR_LABEL, header_color="32ADB6")

STATEMENTS_SOURCES = (
    "Sources - all figures are Hampden & Co Plc's own Statement of Financial Position / Statement of "
    "Comprehensive Income / Statement of Changes in Equity, as filed with Companies House:\n"
    f"FY2025: Hampden Bank Annual Report and Financial Statements 2025, p.46-48 - {AR2025_URL}\n"
    f"FY2024: Hampden Bank Annual Report and Financial Statements 2024, p.48-50 - {AR2024_URL}\n"
    f"FY2023: Hampden & Co Plc Annual Report and Financial Statements 2023, p.41-43 - {AR2023_URL}\n"
    f"FY2022: Hampden & Co Plc Annual Report and Financial Statements 2022, p.42-44 - {AR2022_URL}\n"
    f"FY2021: Hampden & Co Plc Annual Report and Financial Statements 2021, p.53-55 - {AR2021_URL}\n"
    + ENTITY_NOTE
    + " Debt securities and the FY2022 hedge-accounting-related lines (Fair value adjustment for hedged risk, "
    "Derivative financial instruments, Deferred tax asset, Current tax liabilities) genuinely did not exist as "
    "separate balance sheet lines before FY2022 (the Bank started using interest rate hedges and holding debt "
    "securities that year) - left blank for FY2021 rather than assumed nil, except where that year's own report "
    "explicitly shows a dash ('-'), which is transcribed as a disclosed nil (0)."
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {
        "FY2025": 60397, "FY2024": 52771, "FY2023": 104956, "FY2022": 172477, "FY2021": 139948,
    }),
    ("DATA", "Loans and advances to banks", {
        "FY2025": 137120, "FY2024": 203664, "FY2023": 274523, "FY2022": 241254, "FY2021": 189686,
    }),
    ("DATA", "Debt securities", {
        "FY2025": 362399, "FY2024": 224751, "FY2023": 67066, "FY2022": 0,
    }),
    ("DATA", "Loans and advances to clients", {
        "FY2025": 639581, "FY2024": 585893, "FY2023": 487624, "FY2022": 447675, "FY2021": 422160,
    }),
    ("DATA", "Fair value adjustment for hedged risk on loans and advances to clients", {
        "FY2025": 607, "FY2024": -175, "FY2023": 759, "FY2022": -256, "FY2021": 0,
    }),
    ("DATA", "Derivative financial instruments", {
        "FY2025": 413, "FY2024": 1016, "FY2023": 1083, "FY2022": 1867, "FY2021": 0,
    }),
    ("DATA", "Deferred tax asset", {
        "FY2025": 3823, "FY2024": 5605, "FY2023": 4315, "FY2022": 4819, "FY2021": 0,
    }),
    ("DATA", "Prepayments and accrued income", {
        "FY2025": 2334, "FY2024": 1063, "FY2023": 623, "FY2022": 1118, "FY2021": 913,
    }),
    ("DATA", "Other assets", {
        "FY2025": 558, "FY2024": 508, "FY2023": 513, "FY2022": 2372, "FY2021": 212,
    }),
    ("DATA", "Property, plant and equipment", {
        "FY2025": 1370, "FY2024": 570, "FY2023": 176, "FY2022": 143, "FY2021": 85,
    }),
    ("DATA", "Right-of-use assets", {
        "FY2025": 8051, "FY2024": 4439, "FY2023": 589, "FY2022": 714, "FY2021": 1139,
    }),
    ("DATA", "Intangible assets", {
        "FY2025": 10396, "FY2024": 9197, "FY2023": 3936, "FY2022": 2302, "FY2021": 2038,
    }),
    ("TOTAL", "Total assets", {
        "FY2025": 1227049, "FY2024": 1089302, "FY2023": 946163, "FY2022": 874485, "FY2021": 756181,
    }),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from clients", {
        "FY2025": 1123743, "FY2024": 990720, "FY2023": 857506, "FY2022": 796049, "FY2021": 695590,
    }),
    ("DATA", "Derivative financial instruments (liability)", {
        "FY2025": 788, "FY2024": 436, "FY2023": 1194, "FY2022": 838, "FY2021": 0,
    }),
    ("DATA", "Current tax liabilities", {
        "FY2025": 72, "FY2024": 22, "FY2023": 532, "FY2022": 0,
    }),
    ("DATA", "Accruals and deferred income", {
        "FY2025": 2530, "FY2024": 3472, "FY2023": 3447, "FY2022": 3440, "FY2021": 2014,
    }),
    ("DATA", "Lease liabilities", {
        "FY2025": 7565, "FY2024": 3940, "FY2023": 574, "FY2022": 756, "FY2021": 1134,
    }),
    ("DATA", "Other liabilities", {
        "FY2025": 24, "FY2024": 87, "FY2023": 21, "FY2022": 174, "FY2021": 18,
    }),
    ("DATA", "Provisions", {
        "FY2025": 291, "FY2024": 517, "FY2023": 465, "FY2022": 376, "FY2021": 123,
    }),
    ("TOTAL", "Total liabilities", {
        "FY2025": 1135013, "FY2024": 999194, "FY2023": 863739, "FY2022": 801633, "FY2021": 698879,
    }),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {
        "FY2025": 4726, "FY2024": 4726, "FY2023": 4726, "FY2022": 4623, "FY2021": 4223,
    }),
    ("DATA", "Share premium account", {
        "FY2025": 25865, "FY2024": 25865, "FY2023": 25865, "FY2022": 24001, "FY2021": 16555,
    }),
    ("DATA", "Retained earnings", {
        "FY2025": 61445, "FY2024": 59517, "FY2023": 51833, "FY2022": 44228, "FY2021": 36524,
    }),
    ("TOTAL", "Total equity", {
        "FY2025": 92036, "FY2024": 90108, "FY2023": 82424, "FY2022": 72852, "FY2021": 57302,
    }),
    ("TOTAL", "Total liabilities and equity", {
        "FY2025": 1227049, "FY2024": 1089302, "FY2023": 946163, "FY2022": 874485, "FY2021": 756181,
    }),
]

bw.add_balance_sheet_sheet(
    title="Hampden & Co Plc — Statement of Financial Position",
    subtitle="Company-only statement, as filed with Companies House",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=70,
    source_height=190,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
is_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable and similar income", {
        "FY2025": 54016, "FY2024": 53961, "FY2023": 45265, "FY2022": 22882, "FY2021": 12542,
    }),
    ("DATA", "Interest payable and similar charges", {
        "FY2025": -24738, "FY2024": -25613, "FY2023": -16096, "FY2022": -2821, "FY2021": -868,
    }),
    ("TOTAL", "Net interest income", {
        "FY2025": 29278, "FY2024": 28348, "FY2023": 29169, "FY2022": 20061, "FY2021": 11674,
    }),
    ("DATA", "Non-interest income", {
        "FY2025": 1152, "FY2024": 1055, "FY2023": 1043, "FY2022": 906, "FY2021": 758,
    }),
    ("DATA", "Income from currency operations", {
        "FY2025": 1144, "FY2024": 1124, "FY2023": 1278, "FY2022": 1069, "FY2021": 775,
    }),
    ("DATA", "Net (losses)/gains from derivatives and hedge accounting", {
        "FY2025": -111, "FY2024": -203, "FY2023": -303, "FY2022": 820, "FY2021": 0,
    }),
    ("TOTAL", "Total income", {
        "FY2025": 31463, "FY2024": 30324, "FY2023": 31187, "FY2022": 22856, "FY2021": 13207,
    }),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Administrative expenses", {
        "FY2025": -21945, "FY2024": -20873, "FY2023": -20903, "FY2022": -19837, "FY2021": -15006,
    }),
    ("DATA", "Depreciation and amortisation", {
        "FY2025": -2672, "FY2024": -1258, "FY2023": -1038, "FY2022": -945, "FY2021": -1176,
    }),
    ("TOTAL", "Operating expenses", {
        "FY2025": -24617, "FY2024": -22131, "FY2023": -21941, "FY2022": -20782, "FY2021": -16182,
    }),
    ("TOTAL", "Operating profit/(loss) before impairment losses", {
        "FY2025": 6846, "FY2024": 8193, "FY2023": 9246, "FY2022": 2074, "FY2021": -2975,
    }),
    ("DATA", "Impairment credit/(charge) on loans and advances to clients", {
        "FY2025": 107, "FY2024": -12, "FY2023": -103, "FY2022": -29, "FY2021": 5,
    }),
    ("TOTAL", "Profit/(loss) before tax", {
        "FY2025": 6953, "FY2024": 8181, "FY2023": 9143, "FY2022": 2045, "FY2021": -2970,
    }),
    ("DATA", "Tax (expense)/income", {
        "FY2025": -1964, "FY2024": 930, "FY2023": -1036, "FY2022": 4819, "FY2021": 0,
    }),
    ("TOTAL", "Profit/(loss) for the year and total comprehensive profit/(loss)", {
        "FY2025": 4989, "FY2024": 9111, "FY2023": 8107, "FY2022": 6864, "FY2021": -2970,
    }),
]

bw.add_income_statement_sheet(
    title="Hampden & Co Plc — Statement of Comprehensive Income",
    subtitle="Company-only statement, as filed with Companies House",
    rows=is_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=70,
    source_height=190,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
eq_headers = ["Share capital", "Share premium account", "Retained earnings", "Total equity"]
eq_rows = [
    ("TOTAL", "At 1 January 2021", (3823, 9064, 38452, 51339)),
    ("DATA", "Loss for the year and total comprehensive loss", (None, None, -2970, -2970)),
    ("DATA", "Issue of share capital", (400, 7600, None, 8000)),
    ("DATA", "Direct share issue costs", (None, -109, None, -109)),
    ("DATA", "Equity settled share-based payments", (None, None, 1042, 1042)),
    ("TOTAL", "At 31 December 2021", (4223, 16555, 36524, 57302)),
    ("DATA", "Profit for the year and total comprehensive profit", (None, None, 6864, 6864)),
    ("DATA", "Issue of share capital", (400, 7600, None, 8000)),
    ("DATA", "Direct share issue costs", (None, -154, None, -154)),
    ("DATA", "Equity settled share-based payments", (None, None, 840, 840)),
    ("TOTAL", "At 31 December 2022", (4623, 24001, 44228, 72852)),
    ("DATA", "Profit for the year and total comprehensive profit", (None, None, 8107, 8107)),
    ("DATA", "Issue of share capital", (103, 1956, None, 2059)),
    ("DATA", "Direct share issue costs", (None, -92, None, -92)),
    ("DATA", "Equity settled share-based payments", (None, None, 186, 186)),
    ("DATA", "Cancellation of share options", (None, None, -688, -688)),
    ("TOTAL", "At 31 December 2023", (4726, 25865, 51833, 82424)),
    ("DATA", "Profit for the year and total comprehensive profit", (None, None, 9111, 9111)),
    ("DATA", "Dividends", (None, None, -1512, -1512)),
    ("DATA", "Equity settled share-based payments", (None, None, 176, 176)),
    ("DATA", "Dividend equivalent on share options", (None, None, -91, -91)),
    ("TOTAL", "At 31 December 2024", (4726, 25865, 59517, 90108)),
    ("DATA", "Profit for the year and total comprehensive profit", (None, None, 4989, 4989)),
    ("DATA", "Dividends", (None, None, -3024, -3024)),
    ("DATA", "Equity settled share-based payments", (None, None, 145, 145)),
    ("DATA", "Dividend equivalent on share options", (None, None, -182, -182)),
    ("TOTAL", "At 31 December 2025", (4726, 25865, 61445, 92036)),
]

bw.add_equity_changes_sheet(
    title="Hampden & Co Plc — Statement of Changes in Equity",
    subtitle="Company-only statement, as filed with Companies House — read chronologically, oldest to newest",
    headers=eq_headers,
    rows=eq_rows,
    sources_text=(
        STATEMENTS_SOURCES
        + " Equity reconciliation ladder: every year's closing balance ties exactly to both the next year's own "
        "reported opening balance and that year's own Balance Sheet Total equity - zero plug rows needed anywhere "
        "in this 5-year window."
    ),
    first_col_width=52,
    source_height=190,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {
        "FY2025": 6953, "FY2024": 8181, "FY2023": 9143, "FY2022": 2045, "FY2021": -2970,
    }),
    ("DATA", "Net losses/(gains) from derivatives and hedge accounting", {
        "FY2025": 111, "FY2024": 203, "FY2023": 303, "FY2022": -820,
    }),
    ("DATA", "Depreciation and amortisation", {
        "FY2025": 2672, "FY2024": 1258, "FY2023": 1038, "FY2022": 945, "FY2021": 1176,
    }),
    ("DATA", "Equity settled share-based payments", {
        "FY2025": 145, "FY2024": 176, "FY2023": 186, "FY2022": 840, "FY2021": 1042,
    }),
    ("DATA", "Dividend equivalent on share options", {
        "FY2025": -182, "FY2024": -91,
    }),
    ("DATA", "Cancellation of share options", {
        "FY2023": -688,
    }),
    ("DATA", "Impairment (credit)/charge for the year", {
        "FY2025": -107, "FY2024": 12, "FY2023": 103, "FY2022": 29, "FY2021": -5,
    }),
    ("DATA", "(Increase) in prepayments and accrued income", {
        "FY2021": -185,
    }),
    ("DATA", "Increase/(decrease) in accruals and deferred income", {
        "FY2021": 353,
    }),
    ("DATA", "(Increase) in loans and advances to clients and banks", {
        "FY2021": -132311,
    }),
    ("DATA", "Increase in deposits by clients and banks", {
        "FY2021": 194668,
    }),
    ("DATA", "Decrease in other assets", {
        "FY2021": 3,
    }),
    ("DATA", "(Decrease)/increase in other liabilities and provisions", {
        "FY2021": -22,
    }),
    ("DATA", "Elimination of foreign exchange differences", {
        "FY2022": 8, "FY2021": -9,
    }),
    ("TOTAL", "Cash generated from/(used in) operations", {
        "FY2025": 9592, "FY2024": 9739, "FY2023": 10085,
    }),
    ("SECTION", "Changes in operating assets and liabilities", {}),
    ("DATA", "Increase/(decrease) in prepayments and accrued income", {
        "FY2025": -1271, "FY2024": -441, "FY2023": 421, "FY2022": -205,
    }),
    ("DATA", "Increase/(decrease) in accruals and deferred income", {
        "FY2025": -942, "FY2024": 25, "FY2023": 6, "FY2022": 1560,
    }),
    ("DATA", "Decrease/(increase) in loans and advances to clients and banks", {
        "FY2025": 34430, "FY2024": -57243, "FY2023": -93474, "FY2022": -43506,
    }),
    ("DATA", "Increase in deposits from clients/by clients and banks", {
        "FY2025": 133690, "FY2024": 134544, "FY2023": 67050, "FY2022": 90941,
    }),
    ("DATA", "(Increase)/decrease in other assets", {
        "FY2025": -49, "FY2024": 5, "FY2023": 1859, "FY2022": -2160,
    }),
    ("DATA", "(Decrease)/increase in other liabilities and provisions", {
        "FY2025": -285, "FY2024": 117, "FY2023": -56, "FY2022": 405,
    }),
    ("TOTAL", "Cash generated from/(used in) operating activities", {
        "FY2025": 175165, "FY2024": 86746, "FY2023": -14109,
    }),
    ("DATA", "Tax paid/(income tax received)", {
        "FY2025": -131, "FY2024": -870, "FY2021": 0,
    }),
    ("TOTAL", "Net cash from/(used in) operating activities", {
        "FY2025": 175034, "FY2024": 85876, "FY2023": -14109, "FY2022": 50082, "FY2021": 61740,
    }),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of debt securities", {
        "FY2025": -853557, "FY2024": -414862, "FY2023": -67066,
    }),
    ("DATA", "Sales and maturities of debt securities", {
        "FY2025": 715908, "FY2024": 257177,
    }),
    ("DATA", "Purchase of property, plant and equipment", {
        "FY2025": -1848, "FY2024": -902, "FY2023": -77, "FY2022": -86,
    }),
    ("DATA", "Purchases/development of intangible assets", {
        "FY2025": -2736, "FY2024": -5995, "FY2023": -2184, "FY2022": -891, "FY2021": -1145,
    }),
    ("TOTAL", "Net cash from/(used in) investing activities", {
        "FY2025": -142233, "FY2024": -164582, "FY2023": -69327, "FY2022": -977, "FY2021": -1145,
    }),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Repayment of lease liabilities", {
        "FY2025": -74, "FY2024": -500, "FY2023": -427, "FY2022": -378, "FY2021": -445,
    }),
    ("DATA", "Proceeds from issue of shares", {
        "FY2023": 2059, "FY2022": 8000, "FY2021": 8000,
    }),
    ("DATA", "Direct costs of share issuance", {
        "FY2023": -92, "FY2022": -154, "FY2021": -109,
    }),
    ("DATA", "Equity dividends paid", {
        "FY2025": -3024, "FY2024": -1512,
    }),
    ("TOTAL", "Net cash from/(used in) financing activities", {
        "FY2025": -3098, "FY2024": -2012, "FY2023": 1540, "FY2022": 7468, "FY2021": 7446,
    }),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {
        "FY2025": 29703, "FY2024": -80718, "FY2023": -81896, "FY2022": 56573, "FY2021": 68041,
    }),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {
        "FY2025": 125315, "FY2024": 207363, "FY2023": 294851, "FY2022": 228768, "FY2021": 160960,
    }),
    ("DATA", "Effects of foreign exchange rate changes on cash and cash equivalents", {
        "FY2025": -667, "FY2024": -1330, "FY2023": -5592, "FY2022": 9510, "FY2021": -233,
    }),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {
        "FY2025": 154351, "FY2024": 125315, "FY2023": 207363, "FY2022": 294851, "FY2021": 228768,
    }),
]

bw.add_cash_flow_sheet(
    title="Hampden & Co Plc — Statement of Cash Flows",
    subtitle="Company-only statement, as filed with Companies House",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=70,
    source_height=170,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
aq_rows = [
    ("SECTION", "Loans and advances to clients, gross carrying amount by IFRS 9 stage", {}),
    ("DATA", "Stage 1", {
        "FY2025": 609002, "FY2024": 562580, "FY2023": 471836, "FY2022": 432518, "FY2021": 402514,
    }),
    ("DATA", "Stage 2", {
        "FY2025": 12202, "FY2024": 17094, "FY2023": 13154, "FY2022": 15223, "FY2021": 19690,
    }),
    ("DATA", "Stage 3", {
        "FY2025": 18589, "FY2024": 6534, "FY2023": 2939, "FY2022": 128, "FY2021": 124,
    }),
    ("TOTAL", "Gross loans and advances to clients", {
        "FY2025": 639793, "FY2024": 586208, "FY2023": 487929, "FY2022": 447869, "FY2021": 422328,
    }),
    ("SECTION", "Impairment allowances by IFRS 9 stage", {}),
    ("DATA", "Stage 1", {
        "FY2025": -115, "FY2024": -102, "FY2023": -67, "FY2022": -111, "FY2021": -106,
    }),
    ("DATA", "Stage 2", {
        "FY2025": -56, "FY2024": -164, "FY2023": -218, "FY2022": -67, "FY2021": -56,
    }),
    ("DATA", "Stage 3", {
        "FY2025": -41, "FY2024": -49, "FY2023": -20, "FY2022": -16, "FY2021": -6,
    }),
    ("TOTAL", "Total impairment allowances", {
        "FY2025": -212, "FY2024": -315, "FY2023": -305, "FY2022": -194, "FY2021": -168,
    }),
    ("SECTION", "Loans and advances to clients, net carrying amount by IFRS 9 stage", {}),
    ("DATA", "Stage 1", {
        "FY2025": 608887, "FY2024": 562478, "FY2023": 471769, "FY2022": 432407, "FY2021": 402408,
    }),
    ("DATA", "Stage 2", {
        "FY2025": 12146, "FY2024": 16930, "FY2023": 12936, "FY2022": 15156, "FY2021": 19634,
    }),
    ("DATA", "Stage 3", {
        "FY2025": 18548, "FY2024": 6485, "FY2023": 2919, "FY2022": 112, "FY2021": 118,
    }),
    ("TOTAL", "Net loans and advances to clients", {
        "FY2025": 639581, "FY2024": 585893, "FY2023": 487624, "FY2022": 447675, "FY2021": 422160,
    }),
    ("SECTION", "Coverage ratios (each year's own disclosed figure)", {}),
    ("DATA", "Stage 3 coverage ratio", {
        "FY2025": "0.221%", "FY2024": "0.750%", "FY2023": "0.680%", "FY2022": "12.500%", "FY2021": "4.839%",
    }),
    ("DATA", "Total coverage ratio", {
        "FY2025": "0.033%", "FY2024": "0.054%", "FY2023": "0.063%", "FY2022": "0.043%", "FY2021": "0.040%",
    }),
]

bw.add_asset_quality_sheet(
    title="Hampden & Co Plc — Asset Quality",
    subtitle="Loans and advances to clients by IFRS 9 stage, as disclosed in the Bank's own impairment note",
    rows=aq_rows,
    sources_text=(
        "Sources - Hampden & Co Plc's own Note 13 'Impairment of loans and advances to clients' (Note 12 in "
        "FY2021's Annual Report), 'Impairments by stage' table:\n"
        f"FY2025/FY2024: Hampden Bank Annual Report and Financial Statements 2025, p.61 - {AR2025_URL}\n"
        f"FY2023/FY2022: Hampden & Co Plc Annual Report and Financial Statements 2023, p.57 - {AR2023_URL}\n"
        f"FY2021: Hampden & Co Plc Annual Report and Financial Statements 2021, p.72 - {AR2021_URL}\n"
        "Net loans and advances to clients ties exactly to the Balance Sheet's own 'Loans and advances to "
        "clients' line for every year. The Bank does not disclose gross/net exposure by product type separately "
        "from this IFRS 9 stage split - all lending is presented as a single 'loans and advances to clients' "
        "category."
    ),
    first_col_width=56,
    source_height=170,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=130)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {
        "FY2023": 74173, "FY2022": 65731, "FY2021": 55264,
    })],
    p3_sources(),
    note="No Additional Tier 1 or Tier 2 capital any year - CET1 = Tier 1 = Total Capital throughout. "
         "Not disclosed for FY2024/FY2025 (no standalone Pillar 3 document located for either year).",
)

metric(
    "CET1 Ratio", "%",
    [("Common Equity Tier 1 (CET1) ratio", {
        "FY2023": "20.53%", "FY2022": "20.77%", "FY2021": "19%",
    })],
    p3_sources(),
    note="Not disclosed for FY2024/FY2025 (no standalone Pillar 3 document located for either year); "
         "only the aggregate Total Capital Ratio is given in those years' own Annual Reports.",
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {
        "FY2023": 74173, "FY2022": 65731, "FY2021": 55264,
    })],
    p3_sources(),
    note="No AT1 capital any year - Tier 1 = CET1 = Total Capital throughout. Not disclosed for FY2024/FY2025.",
)

metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 ratio", {
        "FY2023": "20.53%", "FY2022": "20.77%", "FY2021": "19%",
    })],
    p3_sources(),
    note="Not disclosed for FY2024/FY2025 (no standalone Pillar 3 document located for either year).",
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {
        "FY2023": 74173, "FY2022": 65731, "FY2021": 55264,
    })],
    p3_sources(),
    note="Not disclosed in £'000 terms for FY2024/FY2025 - only the ratio (below) is given.",
)

metric(
    "Total Capital Ratio", "%",
    [("Total capital ratio", {
        "FY2025": "17%", "FY2024": "17%", "FY2023": "20.53%", "FY2022": "20.77%", "FY2021": "19%",
    })],
    p3_sources(),
    note="FY2024/FY2025 sourced from each year's own Annual Report Key Performance Indicators table (the only "
         "capital metric given there) rather than a standalone Pillar 3 document - none was found published for "
         "either year.",
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted exposure amount", {
        "FY2023": 361317, "FY2022": 316422, "FY2021": 285422,
    })],
    p3_sources(),
    note="Not disclosed for FY2024/FY2025 (no standalone Pillar 3 document located for either year).",
)

rwa_rows = [
    ("DATA", "Credit risk (excluding CCR)", {
        "FY2023": 317736, "FY2022": 284658, "FY2021": 269622,
    }),
    ("DATA", "Counterparty credit risk (CCR)", {
        "FY2023": 1549, "FY2022": 2826,
    }),
    ("DATA", "Of which credit valuation adjustment (CVA)", {
        "FY2023": 738, "FY2022": 1750,
    }),
    ("DATA", "Of which other CCR", {
        "FY2023": 811, "FY2022": 1076,
    }),
    ("DATA", "Market risk (FX)", {
        "FY2021": 0,
    }),
    ("DATA", "Operational risk", {
        "FY2023": 42032, "FY2022": 28938, "FY2021": 15800,
    }),
    ("TOTAL", "Total risk-weighted exposure amount", {
        "FY2023": 361317, "FY2022": 316422, "FY2021": 285422,
    }),
]

bw.add_rwa_breakdown_sheet(
    title="Hampden & Co Plc — RWA Breakdown",
    subtitle="Pillar 1 risk weighted exposure amounts by risk category",
    rows=rwa_rows,
    sources_text=(
        "Sources - Hampden & Co Plc Pillar 3 Disclosures:\n"
        f"FY2023/FY2022: Table UK OV1 'Overview of risk weighted exposure amounts', Pillar 3 Disclosures for the "
        f"year ended 31 December 2023, p.16 - {P3_2023_URL}\n"
        f"FY2021: Table 6 'Pillar 1 capital requirement' and Table 7 'Risk weighted assets and Pillar 1 credit "
        f"risk capital requirement by exposure class', Pillar 3 Disclosures for the year ended 31 December 2021, "
        f"p.16 - {P3_2021_URL}. FY2021's Operational risk RWA (15,800) is derived from the disclosed capital "
        "requirement (1,264) divided by 8%, since only the capital requirement (not the RWA itself) is stated "
        "under this pre-UK-KM1-format disclosure; FY2021 also does not separately disclose a CCR/CVA split (not "
        "itemised in this basis) - left blank rather than assumed zero, unlike Market risk which the document "
        "explicitly states is nil.\n"
        "Not disclosed for FY2024/FY2025 (no standalone Pillar 3 document located for either year, consistent "
        "with the pre-existing Total RWAs sheet). Every year's Total ties exactly to the pre-existing Total RWAs "
        "metric sheet."
    ),
    first_col_width=52,
    source_height=190,
    unit_suffix=" (£'000)",
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio (excluding claims on central banks, FY2022-FY2023)", {
        "FY2023": "8.36%", "FY2022": "8.72%",
    }),
     ("Leverage ratio (FY2021 basis, as originally disclosed)", {
        "FY2021": "7%",
    })],
    p3_sources(),
    note="FY2021's pre-UK-KM1-format disclosure does not specify whether central-bank claims are excluded - shown "
         "on its own row rather than merged with the later, explicitly-labelled basis. Not disclosed for "
         "FY2024/FY2025.",
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio (12-month average)", {
        "FY2023": "262%", "FY2022": "213%",
    }),
     ("Liquidity Coverage Ratio (point-in-time, FY2021 basis)", {
        "FY2021": "180%",
    })],
    p3_sources(),
    note="FY2021's disclosure predates the UK KM1 format and does not state an averaging basis (later years use "
         "a 12-month average per KM1) - shown on its own row rather than assumed equivalent. Not disclosed for "
         "FY2024/FY2025.",
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio (4-quarter average)", {
        "FY2023": "186%", "FY2022": "186%",
    })],
    p3_sources(),
    note="Not disclosed for FY2021 - the Bank's own FY2021 Pillar 3 report contains no NSFR section at all, "
         "consistent with the UK's NSFR reporting requirement only commencing during 2022 for firms of this size "
         "(the same commencement pattern already seen at Ghana International Bank). Not disclosed for "
         "FY2024/FY2025.",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={
        "MREL Ratio": "Not publicly disclosed for any year - no MREL-related content appears in any Pillar 3 "
                       "document reviewed (FY2021-FY2023); Hampden & Co Plc does not appear to be a UK "
                       "resolution entity subject to a standalone MREL requirement.",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {
            "FY2025": 1227049, "FY2024": 1089302, "FY2023": 946163, "FY2022": 874485, "FY2021": 756181,
        }),
        ("Loans and advances to clients", {
            "FY2025": 639581, "FY2024": 585893, "FY2023": 487624, "FY2022": 447675, "FY2021": 422160,
        }),
        ("Deposits from clients", {
            "FY2025": 1123743, "FY2024": 990720, "FY2023": 857506, "FY2022": 796049, "FY2021": 695590,
        }),
        ("Total equity", {
            "FY2025": 92036, "FY2024": 90108, "FY2023": 82424, "FY2022": 72852, "FY2021": 57302,
        }),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total income", {
            "FY2025": 31463, "FY2024": 30324, "FY2023": 31187, "FY2022": 22856, "FY2021": 13207,
        }),
        ("Operating expenses", {
            "FY2025": -24617, "FY2024": -22131, "FY2023": -21941, "FY2022": -20782, "FY2021": -16182,
        }),
        ("Profit/(loss) for the year", {
            "FY2025": 4989, "FY2024": 9111, "FY2023": 8107, "FY2022": 6864, "FY2021": -2970,
        }),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {
            "FY2025": 90108, "FY2024": 82424, "FY2023": 72852, "FY2022": 57302, "FY2021": 51339,
        }),
        ("Profit/(loss) for the year", {
            "FY2025": 4989, "FY2024": 9111, "FY2023": 8107, "FY2022": 6864, "FY2021": -2970,
        }),
        ("Other equity movements, net", {
            "FY2025": -3061, "FY2024": -1427, "FY2023": 1465, "FY2022": 8686, "FY2021": 8933,
        }),
        ("Closing equity", {
            "FY2025": 92036, "FY2024": 90108, "FY2023": 82424, "FY2022": 72852, "FY2021": 57302,
        }),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {
            "FY2025": 175034, "FY2024": 85876, "FY2023": -14109, "FY2022": 50082, "FY2021": 61740,
        }),
        ("Net cash from/(used in) investing activities", {
            "FY2025": -142233, "FY2024": -164582, "FY2023": -69327, "FY2022": -977, "FY2021": -1145,
        }),
        ("Net cash from/(used in) financing activities", {
            "FY2025": -3098, "FY2024": -2012, "FY2023": 1540, "FY2022": 7468, "FY2021": 7446,
        }),
        ("Cash and cash equivalents at end of year", {
            "FY2025": 154351, "FY2024": 125315, "FY2023": 207363, "FY2022": 294851, "FY2021": 228768,
        }),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {
            "FY2023": "20.53%", "FY2022": "20.77%", "FY2021": "19%",
        }),
        ("Tier 1 Ratio", {
            "FY2023": "20.53%", "FY2022": "20.77%", "FY2021": "19%",
        }),
        ("Total Capital Ratio", {
            "FY2025": "17%", "FY2024": "17%", "FY2023": "20.53%", "FY2022": "20.77%", "FY2021": "19%",
        }),
        ("LCR", {
            "FY2023": "262%", "FY2022": "213%", "FY2021": "180%",
        }),
        ("NSFR", {
            "FY2023": "186%", "FY2022": "186%",
        }),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. FY2024/FY2025 ratios other than Total Capital Ratio "
         "are blank - no standalone Pillar 3 document was found published for either year.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/HAMPDEN & CO FINANCIALS.xlsx")
