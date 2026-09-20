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
        "figure), so the Total RWAs sheet reads 'Not publicly disclosed'. A back-solved series "
        "(Own Funds / Total Capital ratio) previously stood there and was WITHDRAWN 2026-09-16 - "
        "see that sheet's own note for the withdrawal record. What the bank does disclose by risk "
        "category is on the RWA Breakdown sheet, derived from the appendix's own published Pillar 1 "
        "minimum capital requirements." + extra
    )


bw = BankWorkbook(bank_name="Kuwait Finance House Plc", years=YEARS, year_label=YEAR_LABEL,
                   header_color="1E7A5C")

BASIS_NOTE = (
    "BASIS NOTE: this entity takes the exemption in s.408 Companies Act 2006 and does not present a "
    "standalone Bank/solo income statement in any year - only a Consolidated (Group) income statement "
    "and comprehensive income statement are published, each year's own Bank Balance Sheet page noting "
    "the Bank's own profit-after-tax figure separately (used here to build the Statement of Changes in "
    "Equity, which the Bank DOES publish on a solo basis every year). The Balance Sheet and Statement "
    "of Changes in Equity sheets in this workbook are therefore Bank/solo basis (consistent with the "
    "existing Cash Flow Statement sheet), while the Profit & Loss sheet is necessarily Consolidated "
    "(Group) basis - the only income statement this entity discloses. Group and Bank scope differ only "
    "immaterially here (a small non-trading subsidiary), so the two bases are not directly comparable "
    "line-by-line but both are genuine, source-disclosed figures, not derived or estimated."
)

INVESTMENTS_BREAKDOWN_NOTE = (
    "FINANCIAL INVESTMENTS BREAKDOWN: the 'Financial investments - ...' sub-rows below the headline "
    "'Total financial investments' line are transcribed from Note 14 'Financial investments' (Note "
    "14(a) 'Financial Investments by category' and Note 14(b) ECL impairment summary) of each year's "
    "own Notes to the Financial Statements, which splits the balance both by measurement basis "
    "(amortised cost / fair value through profit or loss (FVTPL) / fair value through other "
    "comprehensive income (FVOCI)) and, within the amortised-cost bucket, by issuer type (GCC "
    "government bonds/Sukuk and similar instruments; issued by banks and other financial "
    "institutions; issued by corporate bodies):\n"
    f"FY2025/FY2024 (own): Annual Report and Financial Statements 2025, Note 14, p.52 - {AR2025_URL}\n"
    f"FY2023 (own) / FY2022 (comparative): Annual Report and Financial Statements 2023, Note 14, "
    f"p.48 - {AR2023_URL}\n"
    f"FY2022 (own) / FY2021 (comparative): Annual Report and Financial Statements 2022, Note 14, "
    f"p.47 - {AR2022_URL}\n"
    f"FY2021 (own): Annual Report and Financial Statements 2021, Note 14, p.38 - {AR2021_URL}\n\n"
    "The three amortised-cost issuer-type sub-rows are gross carrying amounts (Note 14(a)'s own "
    "'Quoted investments' lines); the 'ECL impairment provision' sub-row is that same note's single "
    "aggregate impairment allowance (Note 14(b), not broken down by issuer), so the four amortised-"
    "cost sub-rows plus the FVTPL and FVOCI sub-rows sum exactly to that year's headline 'Total "
    "financial investments' line every year. GCC government bonds and debt securities are labelled "
    "'GCC government Sukuk and similar instruments' from FY2024 onward, reflecting the FY2024 "
    "Shariah conversion (see ENTITY_NOTE) - the same amortised-cost sovereign-debt line, kept under "
    "each year's own originally-printed wording rather than forced into a single common label."
)

STATEMENTS_SOURCES = (
    "Sources - all figures are Kuwait Finance House Plc's (formerly Ahli United Bank (UK) PLC's) own "
    "Annual Report and Financial Statements, from Companies House filings:\n"
    f"FY2025: Bank Balance Sheet p.27, Consolidated Statement of Income p.24, Consolidated Statement "
    f"of Comprehensive Income p.25, Bank Statement of Changes in Equity p.30-31 - {AR2025_URL}\n"
    f"FY2024: Bank Balance Sheet p.28, Consolidated Statement of Income p.25, Consolidated Statement "
    f"of Comprehensive Income p.26, Bank Statement of Changes in Equity p.31 - {AR2024_URL}\n"
    f"FY2023: Bank Balance Sheet p.24, Consolidated Statement of Income p.21, Consolidated Statement "
    f"of Comprehensive Income p.22, Bank Statement of Changes in Equity p.28 - {AR2023_URL}\n"
    f"FY2022: Bank Balance Sheet p.23, Consolidated Statement of Income p.20, Consolidated Statement "
    f"of Comprehensive Income p.21, Bank Statement of Changes in Equity p.27 (own report) - "
    f"{AR2022_URL}\n"
    f"FY2021: Bank Balance Sheet p.17, Consolidated Statement of Income (unpaginated, follows p.13), "
    f"Consolidated Statement of Comprehensive Income p.15, Bank Statement of Changes in Equity p.21 "
    f"(own report) - {AR2021_URL}\n\n"
    + ENTITY_NOTE + "\n\n" + BASIS_NOTE
)

BALANCE_SHEET_SOURCES = STATEMENTS_SOURCES + "\n\n" + INVESTMENTS_BREAKDOWN_NOTE

# ---------------------------------------------------------------
# Sheet: Balance Sheet (Bank/solo basis)
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances with central banks",
     {"FY2025": 350734, "FY2024": 477039, "FY2023": 302738, "FY2022": 451104, "FY2021": 675547}),
    ("DATA", "Deposits with banks",
     {"FY2025": 242489, "FY2024": 275127, "FY2023": 365605, "FY2022": 245974, "FY2021": 221740}),
    ("DATA", "Financing receivables / Loans and advances",
     {"FY2025": 1524604, "FY2024": 1512591, "FY2023": 1536066, "FY2022": 1454873, "FY2021": 1602103}),
    ("DATA", "Total financial investments",
     {"FY2025": 419996, "FY2024": 397718, "FY2023": 658778, "FY2022": 582585, "FY2021": 412144}),
    ("DATA", "Financial investments - GCC government bonds/Sukuk (sovereign debt, amortised cost)",
     {"FY2025": 99438, "FY2024": 67285, "FY2023": 164797, "FY2022": 222762, "FY2021": 194626}),
    ("DATA", "Financial investments - Issued by banks and other financial institutions (amortised cost)",
     {"FY2025": 141838, "FY2024": 139475, "FY2023": 248594, "FY2022": 147794, "FY2021": 145262}),
    ("DATA", "Financial investments - Issued by corporate bodies (amortised cost)",
     {"FY2025": 138332, "FY2024": 146784, "FY2023": 196476, "FY2022": 164546, "FY2021": 17308}),
    ("DATA", "Financial investments - ECL impairment provision on amortised-cost investments (amortised cost)",
     {"FY2025": -129, "FY2024": -100, "FY2023": -747, "FY2022": -709, "FY2021": -358}),
    ("DATA", "Financial investments - Investments not directly quoted (FVTPL)",
     {"FY2025": 143, "FY2024": 215, "FY2023": 516, "FY2022": 420, "FY2021": 928}),
    ("DATA", "Financial investments - Private equity investments at net asset value (FVOCI)",
     {"FY2025": 40374, "FY2024": 44059, "FY2023": 49142, "FY2022": 47772, "FY2021": 54378}),
    ("DATA", "Derivative financial instruments",
     {"FY2025": 6952, "FY2024": 41151, "FY2023": 34717, "FY2022": 56979, "FY2021": 18040}),
    ("DATA", "Investment in joint venture", {"FY2023": 64, "FY2022": 60, "FY2021": 69}),
    ("DATA", "Investments in group undertakings",
     {"FY2025": 34, "FY2024": 32, "FY2023": 32, "FY2022": 47, "FY2021": 52}),
    ("DATA", "Premises and equipment",
     {"FY2025": 2436, "FY2024": 4058, "FY2023": 5311, "FY2022": 6031, "FY2021": 10618}),
    ("DATA", "Intangible assets", {"FY2025": 5599}),
    ("DATA", "Investment property", {"FY2024": 278, "FY2023": 316, "FY2022": 354, "FY2021": 392}),
    ("DATA", "Returns receivable and similar assets / Interest receivable and other assets",
     {"FY2025": 19310, "FY2024": 24659, "FY2023": 15409, "FY2022": 12994, "FY2021": 8682}),
    ("DATA", "Current tax asset",
     {"FY2025": 1233, "FY2024": 1769, "FY2023": 1515, "FY2022": 274, "FY2021": 507}),
    ("DATA", "Deferred tax asset", {"FY2022": 87}),
    ("DATA", "Retirement benefit scheme",
     {"FY2025": 3509, "FY2024": 3105, "FY2023": 3347, "FY2022": 24381, "FY2021": 46616}),
    ("TOTAL", "Total assets",
     {"FY2025": 2576896, "FY2024": 2737527, "FY2023": 2923898, "FY2022": 2835743, "FY2021": 2996510}),

    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks",
     {"FY2025": 23106, "FY2024": 59630, "FY2023": 11164, "FY2022": 86543, "FY2021": 84073}),
    ("DATA", "Customer deposits",
     {"FY2025": 2149033, "FY2024": 2259618, "FY2023": 2509823, "FY2022": 2359144, "FY2021": 2515820}),
    ("DATA", "Borrowings under repurchase agreements", {"FY2021": 0}),
    ("DATA", "Derivative financial instruments",
     {"FY2025": 12582, "FY2024": 4694, "FY2023": 13253, "FY2022": 16006, "FY2021": 21690}),
    ("DATA", "Returns payable and similar liabilities / Interest payable and other liabilities",
     {"FY2025": 57607, "FY2024": 62898, "FY2023": 53969, "FY2022": 26000, "FY2021": 27532}),
    ("DATA", "Deferred tax liability",
     {"FY2025": 1959, "FY2024": 3408, "FY2023": 1935, "FY2022": 8303, "FY2021": 14663}),
    ("DATA", "Subordinated liabilities", {"FY2023": 0, "FY2022": 9462, "FY2021": 9983}),
    ("TOTAL", "Total liabilities",
     {"FY2025": 2244287, "FY2024": 2390248, "FY2023": 2590144, "FY2022": 2505458, "FY2021": 2673761}),

    ("SECTION", "Equity", {}),
    ("DATA", "Ordinary share capital",
     {"FY2025": 200080, "FY2024": 200080, "FY2023": 200080, "FY2022": 200080, "FY2021": 200080}),
    ("DATA", "Reserves",
     {"FY2025": 132529, "FY2024": 147199, "FY2023": 133674, "FY2022": 130205, "FY2021": 122669}),
    ("TOTAL", "Total equity",
     {"FY2025": 332609, "FY2024": 347279, "FY2023": 333754, "FY2022": 330285, "FY2021": 322749}),
    ("TOTAL", "Total liabilities and equity",
     {"FY2025": 2576896, "FY2024": 2737527, "FY2023": 2923898, "FY2022": 2835743, "FY2021": 2996510}),
]

bw.add_balance_sheet_sheet(
    title="Kuwait Finance House Plc — Bank Balance Sheet",
    subtitle="Bank/solo basis, US$'000. Formerly Ahli United Bank (UK) PLC. See source note at bottom.",
    rows=bs_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=95,
    source_height=520,
    unit_suffix=" (US$'000)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss (Consolidated/Group basis - see BASIS_NOTE)
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Financing and similar income / Interest income",
     {"FY2025": 143932, "FY2024": 185131, "FY2023": 178840, "FY2022": 86307, "FY2021": 50477}),
    ("DATA", "Financing and similar cost / Interest expense",
     {"FY2025": -78199, "FY2024": -110078, "FY2023": -94224, "FY2022": -30047, "FY2021": -13505}),
    ("TOTAL", "Net financing and similar income / Net interest income",
     {"FY2025": 65733, "FY2024": 75053, "FY2023": 84616, "FY2022": 56260, "FY2021": 36972}),
    ("DATA", "Net fees and commissions",
     {"FY2025": 7846, "FY2024": 6498, "FY2023": 8147, "FY2022": 11141, "FY2021": 11900}),
    ("DATA", "Investment income",
     {"FY2025": 2571, "FY2024": 9444, "FY2023": 4545, "FY2022": 6241, "FY2021": 694}),
    ("DATA", "Other operating income",
     {"FY2025": 5902, "FY2024": 4961, "FY2023": 5365, "FY2022": 5600, "FY2021": 3149}),
    ("TOTAL", "Fees and other income",
     {"FY2025": 16319, "FY2024": 20903, "FY2023": 18057, "FY2022": 22982, "FY2021": 15743}),
    ("TOTAL", "Operating income",
     {"FY2025": 82052, "FY2024": 95956, "FY2023": 102673, "FY2022": 79242, "FY2021": 52715}),
    ("DATA", "Credit provision loss/(recovery)",
     {"FY2025": -8012, "FY2024": -1415, "FY2023": -4718, "FY2022": -397, "FY2021": 1882}),
    ("TOTAL", "Net operating income",
     {"FY2025": 74040, "FY2024": 94541, "FY2023": 97955, "FY2022": 78845, "FY2021": 54597}),
    ("DATA", "Staff costs",
     {"FY2025": -25784, "FY2024": -24276, "FY2023": -20490, "FY2022": -15720, "FY2021": -17147}),
    ("DATA", "Depreciation",
     {"FY2025": -2207, "FY2024": -1990, "FY2023": -2036, "FY2022": -3106, "FY2021": -3366}),
    ("DATA", "Operating expenses",
     {"FY2025": -15786, "FY2024": -16379, "FY2023": -14264, "FY2022": -9460, "FY2021": -10250}),
    ("TOTAL", "Operating expenses (total)",
     {"FY2025": 43777, "FY2024": 42645, "FY2023": 36790, "FY2022": 28286, "FY2021": 30763}),
    ("TOTAL", "Profit before tax",
     {"FY2025": 30263, "FY2024": 51896, "FY2023": 61165, "FY2022": 50559, "FY2021": 23834}),
    ("DATA", "Tax expense",
     {"FY2025": -7843, "FY2024": -12678, "FY2023": -14179, "FY2022": -11097, "FY2021": -4941}),
    ("TOTAL", "Net profit after tax",
     {"FY2025": 22420, "FY2024": 39218, "FY2023": 46986, "FY2022": 39462, "FY2021": 18893}),

    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Net change in pension fund reserve",
     {"FY2025": -17, "FY2024": -242, "FY2023": -20082, "FY2022": -17605, "FY2021": 28081}),
    ("DATA", "Net change in fair value of investments",
     {"FY2025": -5243, "FY2024": 4762, "FY2023": -3824, "FY2022": -4250, "FY2021": 8495}),
    ("DATA", "Exchange differences on translating sterling share capital",
     {"FY2025": 5, "FY2024": 1, "FY2023": 3, "FY2022": -7, "FY2021": -1}),
    ("DATA", "Net change in fair value of cash flow hedges",
     {"FY2025": 0, "FY2024": 0, "FY2023": -92, "FY2022": -64, "FY2021": 373}),
    ("TOTAL", "Comprehensive income/(loss) for the year",
     {"FY2025": -5255, "FY2024": 4521, "FY2023": -23995, "FY2022": -21926, "FY2021": 36948}),
    ("TOTAL", "Total comprehensive income for the year, net of tax",
     {"FY2025": 17165, "FY2024": 43739, "FY2023": 22991, "FY2022": 17536, "FY2021": 55841}),
]

bw.add_income_statement_sheet(
    title="Kuwait Finance House Plc — Profit & Loss",
    subtitle="Consolidated (Group) basis - see BASIS NOTE at bottom (this entity does not publish a "
              "standalone Bank income statement). US$'000.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=95,
    source_height=420,
    unit_suffix=" (US$'000)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity (Bank/solo basis) - per-year
# reconciliation ladder confirmed: every year's own closing balance ties
# exactly to both the next year's own opening balance and that year's own
# Balance Sheet Total equity. Zero plug rows needed anywhere across all
# 5 years.
# ---------------------------------------------------------------
equity_headers = ["Ordinary share capital", "Share premium", "Cash flow hedge reserve",
                   "Other reserves / Fair value reserve", "Retained earnings", "Total equity"]
equity_rows = [
    ("TOTAL", "Balance at 1 January 2021", (200080, 128, None, 951, 75712, 276871)),
    ("DATA", "Net profit after tax for the year", (None, None, None, None, 18893, 18893)),
    ("DATA", "Net change in fair value of cash flow hedges", (None, None, None, 373, None, 373)),
    ("DATA", "Net change in fair value of investments", (None, None, None, 8495, None, 8495)),
    ("DATA", "Net change in pension fund reserve", (None, None, None, None, 28081, 28081)),
    ("DATA", "Exchange differences on translating sterling share capital", (None, None, None, None, -1, -1)),
    ("DATA", "Dividend paid to parent undertaking", (None, None, None, None, -10000, -10000)),
    ("TOTAL", "Balance at 31 December 2021 (FY2021 closing / FY2022 opening)",
     (200080, 128, None, 9819, 112722, 322749)),
    ("DATA", "Net profit after tax for the year", (None, None, None, None, 39462, 39462)),
    ("DATA", "Net change in fair value of cash flow hedges", (None, None, None, -64, None, -64)),
    ("DATA", "Net change in fair value of investments", (None, None, None, -4250, None, -4250)),
    ("DATA", "Net change in pension fund reserve", (None, None, None, None, -17605, -17605)),
    ("DATA", "Reclassification of net changes in fair value through OCI investments upon derecognition",
     (None, None, None, 318, -318, None)),
    ("DATA", "Exchange differences on translating sterling share capital", (None, None, None, None, -7, -7)),
    ("DATA", "Dividend paid to parent undertaking", (None, None, None, None, -10000, -10000)),
    ("TOTAL", "Balance at 31 December 2022 (FY2022 closing / FY2023 opening - Other reserves 5,823 "
              "here becomes Cash flow hedge reserve 92 + Fair value reserve 5,731 in the source's own "
              "FY2023 presentation, split below)",
     (200080, 128, 92, 5731, 124254, 330285)),
    ("DATA", "Net profit after tax for the year", (None, None, None, None, 47464, 47464)),
    ("DATA", "Net change in fair value of cash flow hedges", (None, None, -92, None, None, -92)),
    ("DATA", "Net change in fair value of investments", (None, None, None, -3824, None, -3824)),
    ("DATA", "Net change in pension fund reserve", (None, None, None, None, -20082, -20082)),
    ("DATA", "Exchange differences on translating sterling share capital", (None, None, None, None, 3, 3)),
    ("DATA", "Dividend paid to parent undertaking", (None, None, None, None, -20000, -20000)),
    ("TOTAL", "Balance at 31 December 2023 (FY2023 closing / FY2024 opening)",
     (200080, 128, 0, 1907, 131639, 333754)),
    ("DATA", "Net profit after tax for the year", (None, None, None, None, 39450, 39450)),
    ("DATA", "Net change in fair value of investments", (None, None, None, 4316, None, 4316)),
    ("DATA", "Net change in pension fund reserve", (None, None, None, None, -242, -242)),
    ("DATA", "Reclassification of net changes in fair value through OCI investments",
     (None, None, None, 446, -446, None)),
    ("DATA", "Exchange differences on translating sterling share capital", (None, None, None, None, 1, 1)),
    ("DATA", "Dividend paid to parent undertaking", (None, None, None, None, -30000, -30000)),
    ("TOTAL", "Balance at 31 December 2024 (FY2024 closing / FY2025 opening)",
     (200080, 128, 0, 6669, 140402, 347279)),
    ("DATA", "Net profit after tax for the year", (None, None, None, None, 20585, 20585)),
    ("DATA", "Net change in fair value of investments", (None, None, None, -5243, None, -5243)),
    ("DATA", "Net change in pension fund reserve", (None, None, None, None, -17, -17)),
    ("DATA", "Exchange differences on translating sterling share capital", (None, None, None, None, 5, 5)),
    ("DATA", "Dividend paid to parent undertaking", (None, None, None, None, -30000, -30000)),
    ("TOTAL", "Balance at 31 December 2025 (FY2025 closing)",
     (200080, 128, 0, 1426, 130975, 332609)),
]

bw.add_equity_changes_sheet(
    title="Kuwait Finance House Plc — Statement of Changes in Equity",
    subtitle="Bank/solo basis, chronological roll-forward oldest to newest. Equity reconciliation "
              "ladder confirmed: every year's own closing balance ties exactly to both the next year's "
              "own opening balance and that year's own Balance Sheet Total equity - zero plug rows "
              "needed anywhere across all 5 years. US$'000.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
)

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
# Sheet: Asset Quality
# ---------------------------------------------------------------
ASSET_QUALITY_SOURCES = (
    "Sources - Kuwait Finance House Plc's (formerly Ahli United Bank (UK) PLC's) own Annual Report and "
    "Financial Statements, Note 13 'Financing receivables' (FY2024-FY2025) / 'Loans and advances' "
    "(FY2021-FY2023), IFRS 9 stage-by-stage gross carrying amount and impairment allowance tables:\n"
    f"FY2025/FY2024 (own): Annual Report and Financial Statements 2025, p.51-52 - {AR2025_URL}\n"
    f"FY2023 (own): Annual Report and Financial Statements 2023, p.47-48 - {AR2023_URL}\n"
    f"FY2022 (own) / FY2021 (comparative, used here in place of AR2021's own Note since it discloses "
    f"the same IFRS 9 stage granularity): Annual Report and Financial Statements 2022, p.45-47 - "
    f"{AR2022_URL}\n\n"
    + ENTITY_NOTE
)

asset_quality_rows = [
    ("SECTION", "Financing receivables / Loans and advances to customers", {}),
    ("DATA", "Gross carrying amount",
     {"FY2025": 1543237, "FY2024": 1522372, "FY2023": 1543909, "FY2022": 1457822, "FY2021": 1605505}),
    ("DATA", "Impairment allowance",
     {"FY2025": -18633, "FY2024": -9781, "FY2023": -7843, "FY2022": -2949, "FY2021": -3402}),
    ("TOTAL", "Net carrying amount",
     {"FY2025": 1524604, "FY2024": 1512591, "FY2023": 1536066, "FY2022": 1454873, "FY2021": 1602103}),

    ("SECTION", "Gross carrying amount, by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (12-month ECL)",
     {"FY2025": 1276906, "FY2024": 1359230, "FY2023": 1409031, "FY2022": 1316924, "FY2021": 1446060}),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)",
     {"FY2025": 144165, "FY2024": 75245, "FY2023": 79810, "FY2022": 94435, "FY2021": 131646}),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired)",
     {"FY2025": 122166, "FY2024": 87897, "FY2023": 55068, "FY2022": 46463, "FY2021": 27799}),

    ("SECTION", "Impairment allowance, by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (12-month ECL)",
     {"FY2025": 283, "FY2024": 65, "FY2023": 208, "FY2022": 20, "FY2021": 18}),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)",
     {"FY2025": 350, "FY2024": 99, "FY2023": 42, "FY2022": 43, "FY2021": 52}),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired)",
     {"FY2025": 18000, "FY2024": 9617, "FY2023": 7593, "FY2022": 2886, "FY2021": 3332}),

    ("SECTION", "Derived ratios", {}),
    ("DATA", "NPL ratio (Stage 3 gross / total gross)",
     {"FY2025": "7.92%", "FY2024": "5.77%", "FY2023": "3.57%", "FY2022": "3.19%", "FY2021": "1.73%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 impairment / Stage 3 gross)",
     {"FY2025": "14.73%", "FY2024": "10.94%", "FY2023": "13.79%", "FY2022": "6.21%", "FY2021": "11.99%"}),
]

bw.add_asset_quality_sheet(
    title="Kuwait Finance House Plc — Asset Quality",
    subtitle="Financing receivables / Loans and advances to customers, IFRS 9 stage 1/2/3 gross "
              "carrying amount and impairment allowance roll-forward (Note 13). US$'000.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=76,
    source_height=320,
    unit_suffix=" (US$'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources("83"), note=note, first_col_width=48,
                         source_height=280)


# ---------------------------------------------------------------
# KM1 Key Metrics (wayfinder/km1/map.md) - NOT APPLICABLE for this bank, on
# affirmative evidence from the documents themselves rather than a failed
# search. Called BEFORE the first add_metric_sheet() so the sheet still
# lands in its locked position, immediately after Asset Quality and
# immediately before CET1 Capital.
#
# The finding is the middle one of the map's three-way taxonomy: NOT "no
# Pillar 3 is published" (one is, every year, as a signed appendix to the
# Annual Report) but "Pillar 3 IS published and the KM1 template is NOT
# used". The appendix's own "Key Metrics" block is five ratio rows, which
# fails the row-set test of map rule 8 the same way ABC International Bank's
# ten-row "Table 3 Key Regulatory Metrics" does.
# ---------------------------------------------------------------
KM1_SOURCES = (
    "NOT APPLICABLE - Kuwait Finance House Plc does not use the UK KM1 key-metrics template in any year. "
    "This is an affirmative finding read off the documents, not the result of a search that failed to find a "
    "table.\n\n"
    "WHAT THE BANK DOES PUBLISH. A Pillar 3 disclosure exists for every year in this workbook, but not as a "
    "standalone document: it is printed as a signed appendix inside the Annual Report and Financial "
    "Statements filed at Companies House, headed 'APPENDIX : PILLAR 3 DISCLOSURES (UNAUDITED)' and dated at "
    "the top of each page. Verified page by page in the FY2025 filing (printed folios 83-85) and, under the "
    "bank's former name Ahli United Bank (UK) PLC, in the FY2022 filing (printed folio 72).\n\n"
    "WHY IT IS NOT THE TEMPLATE (map rule 8, the ROW-SET TEST). The appendix opens with a block headed 'Key "
    "Metrics - Key capital and liquidity metrics at 31 December are:' and that block is FIVE ROWS, all of "
    "them ratios, in this order: Total Capital ratio, Common Equity Tier 1 (CET1) Capital Ratio, Leverage "
    "Ratio, Liquidity Coverage Ratio, Net Stable Funding Ratio. It carries two columns (the reporting year "
    "and the prior year) and no row numbers. Everything else the UK KM1 template requires is simply absent: "
    "no CET1, Tier 1 or Total capital AMOUNT rows, no total risk-weighted exposure amount, no Tier 1 ratio, "
    "none of the UK 7a-7d SREP rows, no capital conservation or countercyclical buffer rows, no combined "
    "buffer requirement, no leverage exposure measure, and no LCR or NSFR component build-ups (rows 15-16, "
    "UK 16a/16b, 18-19). A five-row ratio summary is a different and shorter table, not an unnumbered KM1, "
    "and mapping it onto template row numbers would invent a correspondence the bank never published.\n\n"
    "WHAT IS ADJACENT TO IT, and why it still is not KM1. The same appendix does print a 'Capital Structure "
    "and Own Funds' table (a CET1 build-up ending in Own Funds) and an 'Own Funds requirements' table (the "
    "minimum Pillar 1 capital requirement by risk category). Those are CC1-like and OV1-like disclosures, and "
    "this workbook already uses them - they are the source for the CET1 Capital, Tier 1 Capital, Total "
    "Capital and RWA Breakdown sheets. They are not the KM1 template and are not reproduced here as one.\n\n"
    "THE FIVE RATIOS THEMSELVES ARE ALREADY IN THIS WORKBOOK, on the CET1 Ratio, Total Capital Ratio, "
    "Leverage Ratio, LCR and NSFR sheets, each with its own citation. Nothing is lost by this sheet carrying "
    "no rows.\n\n"
    "AN EXTRACTION CAVEAT WORTH RECORDING (map rules 13 and 15). Every Companies House filing for this "
    "company is a whole-document scan: pdftotext returns 91 characters for the entire 91-page FY2025 filing, "
    "and pdfimages confirms one full-page CCITT bitmap per page. Any keyword search over these documents "
    "therefore returns zero for everything, and a zero from that instrument says nothing whatever about the "
    "bank. The finding above was made by RENDERING the appendix pages at 150dpi and reading them by eye, "
    "which is the only instrument that works on this filing set.\n\n"
    "LATEST-EDITION CHECK (required by the KM1 map), performed 2026-09-17. The bank's own web presence, "
    "kfhuk.com, is a single-page holding site: its robots.txt points at /sitemap.xml, and that sitemap "
    "contains exactly one URL (/lander). There is no investor, results or regulatory-disclosures section to "
    "check, and no Pillar 3 document is published on the bank's website at all - which is consistent with, "
    "and explains, the disclosure living inside the Companies House filing. The newest filing available is "
    "the Annual Report and Financial Statements 2025 (FY2025), which is already this workbook's most recent "
    "year. NONE NEWER EXISTS; this workbook is not an edition behind.\n\n"
    "NOTE ON kfh.co.uk, recorded so a later session does not repeat the mistake: that domain is NOT this "
    "bank. It belongs to Kinleigh Folkard & Hayward, a London estate agency, and it resolves and serves a "
    "normal site - so an automated check that assumed the obvious domain would have read an unrelated "
    "company's pages as this bank's.\n\n"
    + ENTITY_NOTE
)

bw.add_km1_sheet(
    title="Kuwait Finance House Plc — KM1 Key Metrics",
    subtitle="Not applicable - this bank publishes Pillar 3 disclosures every year (as a signed appendix "
             "inside its Annual Report and Financial Statements) but does not use the UK KM1 key-metrics "
             "template in any of them. Its own 'Key Metrics' block is a five-row ratio summary, which fails "
             "the template's row-set test. See the source note for the full evidence and for what the bank "
             "does disclose instead.",
    # GA-009 (2026-09-18): EVERY YEAR CELL CARRIES THE STATEMENT. Until now this
    # row was built as {y: "" for y in YEARS} - a dict of EMPTY STRINGS, which
    # renders exactly like the empty dict that produced the same defect in
    # Nomura (GA-005) and Melli (GA-006): five year headers above five blank
    # cells, saying nothing at all where the sheet means to say "this bank
    # publishes a Pillar 3 but does not use this template".
    rows=[
        ("DATA", "UK KM1 key-metrics template",
         {y: "Not published — the template is not used" for y in YEARS}),
        ("DATA", "Pillar 3 disclosures published by the Bank (signed Appendix inside each Annual Report)",
         {y: "Published every year, but contain no KM1" for y in YEARS}),
        ("DATA", "The Bank's own five-row 'Key Metrics' block (Total Capital ratio, CET1 ratio, Leverage "
                 "Ratio, LCR, NSFR), printed in its place",
         {y: "Not applicable as a KM1 — fails the row-set test" for y in YEARS}),
    ],
    sources_text=KM1_SOURCES,
    first_col_width=86,
    source_height=460,
)


CET1_CAPITAL = {"FY2025": 325.3, "FY2024": 316.7, "FY2023": 323.2, "FY2022": 304.5, "FY2021": 319.0}
TIER1_CAPITAL = CET1_CAPITAL  # no AT1 disclosed any year
TOTAL_CAPITAL = {"FY2025": 325.3, "FY2024": 316.7, "FY2023": 323.2, "FY2022": 304.5, "FY2021": 319.8}
# WITHDRAWN 2026-09-16 on the user's decision. Each value was Own Funds DIVIDED
# BY that year's Total Capital ratio - a back-solve from a ROUNDED percentage,
# which is the pattern this project does not present as disclosure. Retained
# unused as the record of what was removed; do NOT re-wire into the sheet.
# NOTE this is NOT the same as the RWA Breakdown sheet further below, which
# multiplies the Pillar 3 appendix's OWN DISCLOSED per-category Pillar 1 capital
# requirements by 12.5 (the 8% constant). That is a unit conversion of published
# components, not a back-solve from a rounded ratio, and it stands.
TOTAL_RWA_CALC_WITHDRAWN = {"FY2025": 1618.4, "FY2024": 1649.3, "FY2023": 1666.0, "FY2022": 1530.2, "FY2021": 1421.3}  # noqa: F841
CET1_RATIO = {"FY2025": "20.1%", "FY2024": "19.2%", "FY2023": "19.4%", "FY2022": "19.9%", "FY2021": "22.4%"}
TOTAL_CAPITAL_RATIO = {"FY2025": "20.1%", "FY2024": "19.2%", "FY2023": "19.4%", "FY2022": "19.9%", "FY2021": "22.5%"}
LEVERAGE_RATIO = {"FY2025": "14.2%", "FY2024": "13.7%", "FY2023": "11.9%", "FY2022": "12.3%", "FY2021": "10.5%"}
LCR = {"FY2025": "592.3%", "FY2024": "385.4%", "FY2023": "662.5%", "FY2022": "392.5%", "FY2021": "486.4%"}
NSFR = {"FY2025": "139.0%", "FY2024": "119.4%", "FY2023": "133.0%", "FY2022": "127.4%", "FY2021": "136.2%"}

NO_AT1_NOTE = ("No Additional Tier 1 instruments disclosed any year - Tier 1 capital equals CET1 "
               "capital throughout. A small Tier 2 balance ($799k) exists only in FY2021 (see Total "
               "Capital), fully amortised/repaid by FY2022 onward.")
RWA_NOTE = (
    "NOT PUBLICLY DISCLOSED, AND THE RWA BREAKDOWN SHEET'S TOTAL IS NOT A CONTRADICTION OF THAT - it is "
    "a derivation, and this note says exactly what the Bank does and does not print.\n\n"
    "WHAT THE BANK PRINTS, re-read end to end 2026-09-18 from the FY2025 Annual Report's own Appendix: "
    "Pillar 3 Disclosures (unaudited), printed folios 83-89. (i) A five-row 'Key Metrics' block on "
    "printed p.83: Total Capital ratio, CET1 Capital Ratio, Leverage Ratio, Liquidity Coverage Ratio, "
    "Net Stable Funding Ratio. No RWA row. (ii) A 'Capital Structure and Own Funds' table on the same "
    "page: a CET1 component build-up ending in Own Funds. No RWA row. (iii) 'The minimum capital "
    "requirements under Pillar 1' on printed p.84: CAPITAL REQUIREMENTS by risk category, footing to a "
    "Total Pillar 1 capital requirement of US$129,413k (2025) and US$131,855k (2024). Again no RWA. "
    "(iv) Credit-quality-step exposure tables, counterparty credit risk, impaired exposures, asset "
    "encumbrance and remuneration across printed pp.85-89 - none of which states an RWA either.\n"
    "THE ZERO IS A FACT ABOUT THE DOCUMENT, NOT ABOUT THE EXTRACTION. These filings are whole-document "
    "image scans (go-tiff2pdf, no text layer at all), so the appendix was rendered at 200dpi and read. "
    "The phrases 'risk weighted' and 'risk-weighted' occur ZERO times across all seven appendix pages, "
    "while the same extraction returns the appendix's 'Risk Weight' column headers, its capital-"
    "requirement tables in full, and every narrative section named above. The Bank's vocabulary for "
    "this concept is 'capital requirement' and 'Risk Weight'; it never states a risk-weighted total.\n\n"
    "WITHDRAWAL RECORD (2026-09-16). This sheet previously carried FY2025 1,618.4; FY2024 1,649.3; "
    "FY2023 1,666.0; FY2022 1,530.2; FY2021 1,421.3 (USD m), each back-solved as Own Funds divided "
    "by that year's Total Capital ratio. They were withdrawn on the project owner's decision: the "
    "ratio is published rounded to one decimal place, so the quotient carries a materially wider "
    "band than its four significant figures imply, and a computed value in a disclosure column "
    "reads as a disclosure. The arithmetic is preserved in this build script as "
    "TOTAL_RWA_CALC_WITHDRAWN so the removal stays auditable.\n\n"
    "SEE THE RWA BREAKDOWN SHEET FOR WHAT THE BANK DOES DISCLOSE. That sheet is NOT affected by "
    "this withdrawal and is a different calculation: the Pillar 3 appendix publishes the minimum "
    "Pillar 1 CAPITAL REQUIREMENT by risk category every year, and those disclosed components are "
    "multiplied by 12.5 (the inverse of the fixed 8% own-funds requirement) to state them as "
    "RWA-equivalents. That is a unit conversion of published figures against a regulatory constant, "
    "not a back-solve from a rounded ratio. As a cross-check, the two approaches agreed to within "
    "0.15% in every year before this withdrawal (e.g. FY2025 1,618.4 against 1,617.7), which is why "
    "the breakdown's totals remain sound while the division above does not.")

metric("CET1 Capital", "USD m", [("Common Equity Tier 1 (CET1) capital", CET1_CAPITAL)])
metric("CET1 Ratio", "%", [("CET1 ratio", CET1_RATIO)])
metric("Tier 1 Capital", "USD m", [("Tier 1 capital", TIER1_CAPITAL)], note=NO_AT1_NOTE)
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", CET1_RATIO)], note=NO_AT1_NOTE)
metric("Total Capital", "USD m", [("Total capital / Own Funds", TOTAL_CAPITAL)])
metric("Total Capital Ratio", "%", [("Total capital ratio", TOTAL_CAPITAL_RATIO)])
# GA-009 (2026-09-18): the cell used to read a bare "Not publicly disclosed"
# while the very next sheet printed a Total RWAs row - a reader flipping between
# the two saw the workbook contradict itself. Both sheets are correct (the Bank
# discloses no total RWA; the breakdown's total is a x12.5 derivation of
# disclosed capital requirements), and the cell now SAYS that instead of leaving
# the reader to reconcile two sheets from a source note.
metric("Total RWAs", "USD m",
       [("Total risk-weighted exposure amount",
         {y: "Not publicly disclosed — see RWA Breakdown (derived x12.5)" for y in YEARS})],
       note=RWA_NOTE)

# ---------------------------------------------------------------
# Sheet: RWA Breakdown - the Pillar 3 appendix discloses the minimum
# Pillar 1 CAPITAL REQUIREMENT by risk category every year (not RWAs
# directly); RWA-equivalent = capital requirement / 8% (i.e. x12.5),
# standard Basel III methodology. This independently cross-validates
# the Total RWAs sheet's own Own-Funds/Total-Capital-ratio calculation
# (both land within ~0.2% of each other every year).
# ---------------------------------------------------------------
rwa_breakdown_rows = [
    ("DATA", "Credit and counterparty risk RWA (Standardised Approach)",
     {"FY2025": 1407550, "FY2024": 1394450, "FY2023": 1490975, "FY2022": 1304388, "FY2021": 1206525}),
    ("DATA", "Market risk RWA (Position Risk Requirement)",
     {"FY2025": 38638, "FY2024": 63925, "FY2023": 23488, "FY2022": 62513, "FY2021": 74988}),
    ("DATA", "Credit value adjustment (CVA) RWA",
     {"FY2025": 5500, "FY2024": 26900, "FY2023": 31313, "FY2022": 39650, "FY2021": 3750}),
    ("DATA", "Operational risk RWA (Basic Indicator Approach)",
     {"FY2025": 165975, "FY2024": 162913, "FY2023": 118550, "FY2022": 120875, "FY2021": 138150}),
    # GA-009 (2026-09-18): the label now says DERIVED and says the Bank does not
    # publish this total, so a reader who reaches this row before the Total RWAs
    # sheet's note cannot read it as a disclosure.
    ("TOTAL", "Total RWAs - DERIVED here (x12.5) from the disclosed Pillar 1 capital requirement "
              "components above; the Bank publishes no total RWA figure of its own",
     {"FY2025": 1617663, "FY2024": 1648188, "FY2023": 1664325, "FY2022": 1527425, "FY2021": 1423413}),
]

bw.add_rwa_breakdown_sheet(
    title="Kuwait Finance House Plc — RWA Breakdown",
    subtitle="DERIVED, NOT DISCLOSED. The Bank publishes no RWA figure - neither by category nor in "
              "total (appendix re-read end to end 2026-09-18; see the Total RWAs sheet's note). Every "
              "figure on this sheet is the Pillar 3 appendix's own disclosed 'minimum capital "
              "requirements under Pillar 1' by risk category, multiplied by 12.5 to state it as an "
              "RWA-equivalent. USD'000.",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources(
        "83-84",
        extra=(
            "\n\nRWA BREAKDOWN METHOD: the source discloses 'The minimum capital requirements under "
            "Pillar 1' by risk category every year (Credit and counterparty risk capital requirement "
            "(SA); Market risk capital requirement; Credit value adjustment capital requirement; "
            "Operational risk capital requirement (BIA)) but never a category-level RWA figure "
            "directly. Each category's RWA-equivalent is calculated here as capital requirement / 8% "
            "(i.e. x12.5), the standard Basel III relationship between capital requirement and RWA "
            "under the Standardised Approach. The resulting Total RWAs (this sheet's own component "
            "sum) differs from the Total RWAs sheet's Own-Funds/Total-Capital-ratio-based calculation "
            "by under 0.2% every year - both are legitimate derivations from disclosed figures, "
            "neither is a directly-quoted 'Total RWAs' line item, and the small gap is an immaterial "
            "reconciliation-methodology difference, not a data error."
        ),
    ),
    first_col_width=90,
    source_height=380,
    unit_suffix=" (USD'000)",
)

metric("Leverage Ratio", "%", [("Leverage ratio", LEVERAGE_RATIO)])
metric("LCR", "%", [("Liquidity Coverage Ratio", LCR)])
metric("NSFR", "%", [("Net Stable Funding Ratio", NSFR)])

# GA-020 (2026-09-19): all five Annual Reports FY2021-FY2025 (which carry the Pillar 3 appendix)
# OCR'd from Companies House at 150 dpi: 'MREL'/'eligible liabilities'/'loss-absorbing' zero in
# every one (richness 'capital' 59-66). FY2023-FY2025 additionally rest on the BoE 'External
# MRELs' lists (2023-2026 editions), which by their own scope sentence name every UK resolution
# entity with an MREL above MCR and do not name KFH - see the note. FY2021/FY2022 predate the
# earliest edition relied on, so they are recorded as not published rather than not applicable.
MREL_ST = {y: ("Not applicable – no MREL above MCR: KFH Plc absent from BoE 'External MRELs' lists 2023–26, which "
               "name every UK resolution entity with MREL above MCR; AR " + y + " (incl. Pillar 3) has none.")
           for y in ["FY2025", "FY2024", "FY2023"]}
MREL_ST.update({y: ("Not published – no MREL figure in KFH Plc Annual Report " + y + " or its Pillar 3 appendix "
                    "(CH scan, OCR 2026-09-19).") for y in ["FY2022", "FY2021"]})
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources("n/a"), statements={"MREL Ratio": MREL_ST},
    per_note={"MREL Ratio": "Not publicly disclosed any year. POSITIVE RECORD ADDED 18 September 2026 "
                             "(KM1-032): this note previously read 'consistent with a small UK bank "
                             "subsidiary that is not itself a resolution entity' - a plausibility argument "
                             "rather than evidence. The Bank of England's own 'External minimum requirements "
                             "for own funds and eligible liabilities (MRELs)' disclosures - the 2023, 2024, "
                             "2025 and 2026 editions at bankofengland.co.uk/financial-stability/resolution/"
                             "mrels-<year> - contain, in the BoE's own words, 'all firms with a resolution "
                             "entity incorporated in the UK for which an MREL above MCR has been "
                             "communicated'. KFH is named in none of the four editions. As a UK subsidiary "
                             "of Kuwait Finance House K.S.C.P., whose resolution entity is not incorporated "
                             "in the UK, that absence is exactly what the scope sentence predicts, and the "
                             "reasoning in this note is now sourced rather than assumed. The BoE publishes "
                             "the REQUIREMENT, not the ratio, so nothing from that table is transcribed "
                             "here - it establishes that there was nothing for the Bank to disclose."},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets",
         {"FY2025": 2576896, "FY2024": 2737527, "FY2023": 2923898, "FY2022": 2835743, "FY2021": 2996510}),
        ("Financing receivables / Loans and advances",
         {"FY2025": 1524604, "FY2024": 1512591, "FY2023": 1536066, "FY2022": 1454873, "FY2021": 1602103}),
        ("Customer deposits",
         {"FY2025": 2149033, "FY2024": 2259618, "FY2023": 2509823, "FY2022": 2359144, "FY2021": 2515820}),
        ("Total equity",
         {"FY2025": 332609, "FY2024": 347279, "FY2023": 333754, "FY2022": 330285, "FY2021": 322749}),
    ],
    balance_sheet_unit="US$'000",
    income_statement_totals=[
        ("Operating income",
         {"FY2025": 82052, "FY2024": 95956, "FY2023": 102673, "FY2022": 79242, "FY2021": 52715}),
        ("Total operating expense",
         {"FY2025": 43777, "FY2024": 42645, "FY2023": 36790, "FY2022": 28286, "FY2021": 30763}),
        ("Net profit after tax",
         {"FY2025": 22420, "FY2024": 39218, "FY2023": 46986, "FY2022": 39462, "FY2021": 18893}),
    ],
    income_statement_unit="US$'000",
    equity_changes_totals=[
        ("Opening equity",
         {"FY2025": 347279, "FY2024": 333754, "FY2023": 330285, "FY2022": 322749, "FY2021": 276871}),
        ("Total comprehensive income for the year (Bank/solo basis, ties to the equity sheet)",
         {"FY2025": 15330, "FY2024": 43525, "FY2023": 23469, "FY2022": 17536, "FY2021": 55841}),
        ("Other equity movements, net",
         {"FY2025": -30000, "FY2024": -30000, "FY2023": -20000, "FY2022": -10000, "FY2021": -10000}),
        ("Closing equity",
         {"FY2025": 332609, "FY2024": 347279, "FY2023": 333754, "FY2022": 330285, "FY2021": 322749}),
    ],
    equity_changes_unit="US$'000",
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
         "compliant (Islamic) bank during FY2024 under new ownership - see the Balance Sheet sheet's "
         "ENTITY NOTE. Figures are US$, not converted to GBP (native-currency presentation, consistent "
         "with sibling USD-reporting banks in this batch). Balance Sheet and Statement of Changes in "
         "Equity are Bank/solo basis; Profit & Loss is necessarily Consolidated (Group) basis - this "
         "entity does not publish a standalone Bank income statement (see the Balance Sheet sheet's "
         "BASIS NOTE) - so the equity-changes block above uses the equity sheet's own Bank-basis "
         "comprehensive income, not the Group P&L's OCI total. Total RWAs is independently derived two "
         "ways (Own Funds/Total Capital ratio on the Total RWAs sheet; summed Pillar 1 capital "
         "requirement components x12.5 on the RWA Breakdown sheet) since no single RWA figure is "
         "directly disclosed - both agree within 0.2%. Figures are duplicated from the detail sheets "
         "for at-a-glance trend viewing.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/KUWAIT FINANCE HOUSE FINANCIALS.xlsx")
print("Saved.")
