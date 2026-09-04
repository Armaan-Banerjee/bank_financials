import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first

# Companies House annual accounts filings (company 05321714, formerly BMCE Bank
# International Plc / MediCapital Bank Plc). All filings are fully scanned
# (image-only) - every figure below was OCR'd/read visually and cross-checked
# against the adjoining year's own comparative column.
AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/05321714/filing-history/MzUxODk4NzcyM2FkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/05321714/filing-history/MzQzODczNDQ5OWFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/05321714/filing-history/MzM5NDE3NzEwN2FkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/05321714/filing-history/MzM1NDAwMjc2N2FkaXF6a2N4/document?format=pdf&download=0"

# Standalone Pillar 3 disclosures, found on the Bank's own site
# (bankofafricaunitedkingdom.co.uk/finances.html) - text-native PDFs, no OCR
# needed. No FY2021 or FY2025 edition exists (site's earliest is FY2022; FY2025
# not yet published).
P3_2022_URL = "https://www.bankofafricaunitedkingdom.co.uk/pdfs/finances/BOA_UK_Pillar_III_2022.pdf"
P3_2023_URL = "https://www.bankofafricaunitedkingdom.co.uk/pdfs/finances/Pillar3-Disclosures-2023.pdf"
P3_2024_URL = "https://www.bankofafricaunitedkingdom.co.uk/pdfs/finances/Pillar3-Disclosures-2024.pdf"
BOA_FINANCES_URL = "https://www.bankofafricaunitedkingdom.co.uk/finances.html"

ENTITY_NOTE = (
    "Entity: BANK OF AFRICA United Kingdom Plc (FRN 454750, company 05321714, formerly "
    "BMCE Bank International Plc / MediCapital Bank Plc), a UK-incorporated subsidiary of "
    "Bank of Africa S.A. (Morocco). Reports in GBP; no FX conversion needed. Does NOT take "
    "the FRS 101/102 cash-flow-statement exemption - a full Statement of Cash Flows exists "
    "every year. All 5 Companies House filings used are fully scanned/image-only; every "
    "figure was read from the rendered page image and cross-checked against the following "
    "year's own comparative column (all ties confirmed exact across the full 5-year chain: "
    "FY2021 closing = FY2022 opening = 87,968; FY2022 closing = FY2023 opening = 68,544; "
    "FY2023 closing = FY2024 opening = 54,575; FY2024 closing = FY2025 opening = 51,070).\n\n"
    "DATA QUALITY NOTE - genuine restatement, distinct from an arithmetic-error correction: "
    "the FY2023 Annual Report restates FY2022's comparative Statement of Changes in Equity "
    "(loss for the year (GBP3,839k) as originally reported in the FY2022 Annual Report vs. "
    "(GBP4,556k) restated; closing equity GBP75,751k vs. GBP75,034k restated) and, within the "
    "Cash Flow Statement itself, restates two line items within operating activities (Change "
    "in operating liabilities GBP(35,633)k original vs. GBP(35,509)k restated; Other non-cash "
    "items GBP(5,399)k vs. GBP(5,512)k restated) - the operating-activities TOTAL is "
    "unaffected (GBP(27,463)k both times) and the closing cash balance is unaffected. The "
    "FY2022 Independent Auditor's Report itself references 'prior year adjustments and "
    "ongoing regulatory investigation' as an audit risk factor, consistent with this being a "
    "genuine, disclosed restatement rather than a transcription error on our part. This "
    "workbook uses each year's own originally-reported cash flow figures as the primary "
    "column (project convention), with the restatement noted here rather than silently "
    "blended in."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Bank of Africa United Kingdom Plc's own Statement of Cash "
    "Flows, GBP'000:\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements 2025, p.42 (Statement of Cash Flows) - {AR2025_URL}\n"
    f"FY2023 (& FY2022 restated comparative, see note): Annual Report and Financial Statements 2023, p.43 (Statement of cash flows) - {AR2023_URL}\n"
    f"FY2022 (originally reported, used as primary column): Annual Report and Financial Statements 2022, p.42 (Statement of cash flows) - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2022, p.42 (Statement of cash flows, FY2021 comparative column) - {AR2022_URL}\n\n"
    + ENTITY_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - Bank of Africa United Kingdom Plc, own entity-level Pillar 3 disclosures "
        "(KM1 Key Metrics), GBP'000 unless stated:\n"
        f"FY2024: Pillar 3 Disclosures 2024, p.6 (Key Metrics) and p.20 (composition of capital resources table) - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures 2023, p.6 (Key Metrics) and p.20 (composition of capital resources table) - {P3_2023_URL}\n"
        f"FY2022: Pillar 3 Disclosures 2022, p.17 (composition of capital resources table, as originally published) - {P3_2022_URL}\n"
        f"FY2021: Pillar 3 Disclosures 2022, p.17 (composition of capital resources table, FY2021 comparative column) - {P3_2022_URL}\n"
        f"FY2025: no Pillar 3 edition published yet (as of this build) - Annual Report and Financial Statements 2025, p.23 (Capital Management) - {AR2025_URL}"
        + extra
    )


bw = BankWorkbook(bank_name="Bank of Africa United Kingdom Plc", years=YEARS, header_color="3D5A80")

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
BALANCE_SHEET_PRESENTATION_NOTE = (
    "PRESENTATION NOTE: FY2025/FY2024 (Annual Report 2025) split Property, Plant and Equipment "
    "and Right-of-use Assets, and Goodwill and Other intangible assets, into separate lines; "
    "FY2023 (Annual Report 2023) and FY2022/FY2021 (Annual Report 2022) combine each of those "
    "pairs into a single 'Property, Plant and Equipment and Right-of-use Assets' line and a "
    "single 'Goodwill and other intangible assets' line - reproduced here as originally "
    "disclosed rather than artificially split. FY2023-2025 include a 'Provisions' line "
    "(introduced FY2023); FY2021-2022 have none. FY2025's Balance Sheet folds Collateral held "
    "with third parties into Other assets (same convention as the other statement sheets in "
    "this workbook)."
)
BALANCE_SHEET_SOURCES = (
    "Sources - Bank of Africa United Kingdom Plc's own Statement of Financial Position, GBP'000:\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements 2025, p.40 - {AR2025_URL}\n"
    f"FY2023 (& FY2022 restated comparative, not used - see note): Annual Report and Financial Statements 2023, p.41 - {AR2023_URL}\n"
    f"FY2022 (originally reported, used as primary column): Annual Report and Financial Statements 2022, p.40 - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2022, p.40 (FY2021 comparative column) - {AR2022_URL}\n\n"
    + BALANCE_SHEET_PRESENTATION_NOTE + "\n\n" + ENTITY_NOTE
)

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances with central banks", {"FY2025": 3145, "FY2024": 15397, "FY2023": 27447, "FY2022": 45655, "FY2021": 43395}),
    ("DATA", "Due from banks", {"FY2025": 112586, "FY2024": 66588, "FY2023": 40848, "FY2022": 90560, "FY2021": 121178}),
    ("DATA", "Derivative assets", {"FY2025": 993, "FY2024": 546, "FY2023": 766, "FY2022": 42, "FY2021": 89}),
    ("DATA", "Loans and advances to customers", {"FY2025": 41952, "FY2024": 28985, "FY2023": 28332, "FY2022": 148285, "FY2021": 162016}),
    ("DATA", "Financial investments - Amortised Cost", {"FY2025": 66165, "FY2024": 80814, "FY2023": 82889, "FY2022": 89665, "FY2021": 87687}),
    ("DATA", "Financial investments - FVOCI", {"FY2025": 63507, "FY2024": 57583, "FY2023": 37667, "FY2022": 43949, "FY2021": 52020}),
    ("DATA", "Property, Plant and Equipment", {"FY2025": 476, "FY2024": 578}),
    ("DATA", "Right-of-use Assets", {"FY2025": 1192, "FY2024": 1366}),
    ("DATA", "Property, Plant and Equipment and Right-of-use Assets", {"FY2023": 1885, "FY2022": 1496, "FY2021": 2517}),
    ("DATA", "Goodwill", {"FY2025": 8766, "FY2024": 8304}),
    ("DATA", "Other intangible assets", {"FY2025": 4969, "FY2024": 4941}),
    ("DATA", "Goodwill and other intangible assets", {"FY2023": 12787, "FY2022": 11561, "FY2021": 9802}),
    ("DATA", "Deferred tax assets", {"FY2025": 12597, "FY2024": 13428, "FY2023": 8822, "FY2022": 8781, "FY2021": 8191}),
    ("DATA", "Other assets", {"FY2025": 12616, "FY2024": 13002, "FY2023": 12998, "FY2022": 12396, "FY2021": 9791}),
    ("TOTAL", "Total assets", {"FY2025": 328964, "FY2024": 291532, "FY2023": 254441, "FY2022": 452390, "FY2021": 496686}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Due to banks", {"FY2025": 149668, "FY2024": 153081, "FY2023": 120940, "FY2022": 289489, "FY2021": 297704}),
    ("DATA", "Derivative liabilities", {"FY2025": 26, "FY2024": 868, "FY2023": 69, "FY2022": 502, "FY2021": 25}),
    ("DATA", "Due to customers", {"FY2025": 84367, "FY2024": 44717, "FY2023": 42227, "FY2022": 59541, "FY2021": 92028}),
    ("DATA", "Other liabilities", {"FY2025": 8317, "FY2024": 9171, "FY2023": 9623, "FY2022": 11254, "FY2021": 9316}),
    ("DATA", "Provisions", {"FY2025": 334, "FY2024": 700, "FY2023": 500}),
    ("DATA", "Subordinated debt", {"FY2025": 15623, "FY2024": 14824, "FY2023": 15556, "FY2022": 15853, "FY2021": 15032}),
    ("TOTAL", "Total liabilities", {"FY2025": 258335, "FY2024": 223361, "FY2023": 188915, "FY2022": 376639, "FY2021": 414105}),
    ("SECTION", "Equity attributable to equity holders", {}),
    ("DATA", "Share capital", {"FY2025": 102173, "FY2024": 102173, "FY2023": 102173, "FY2022": 102173, "FY2021": 102173}),
    ("DATA", "Other reserves", {"FY2025": -1303, "FY2024": -1488, "FY2023": -2354, "FY2022": -6845, "FY2021": -3854}),
    ("DATA", "Accumulated losses", {"FY2025": -30241, "FY2024": -32514, "FY2023": -34293, "FY2022": -19577, "FY2021": -15738}),
    ("TOTAL", "Total equity", {"FY2025": 70629, "FY2024": 68171, "FY2023": 65526, "FY2022": 75751, "FY2021": 82581}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 328964, "FY2024": 291532, "FY2023": 254441, "FY2022": 452390, "FY2021": 496686}),
]

bw.add_balance_sheet_sheet(
    title="Bank of Africa United Kingdom Plc — Statement of Financial Position",
    subtitle="Entity-level (solo) basis, as reported in each year's own Annual Report",
    rows=balance_sheet_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=64,
    source_height=220,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
INCOME_STATEMENT_PRESENTATION_NOTE = (
    "PRESENTATION NOTE: FY2025/FY2024 (Annual Report 2025) reach 'Net operating income' via "
    "Net interest income + Net fee and commission income + Net trading income (no separate "
    "'Other operating income' line), then 'Total operating expenses' followed by a 'Net "
    "impairment gain/(loss)' line to reach Profit/(Loss) before tax. FY2023 (Annual Report "
    "2023) and FY2022/FY2021 (Annual Report 2022) additionally disclose a separate 'Other "
    "operating income' line feeding into Net operating income, then 'Total operating expenses "
    "before impairment losses' followed by 'Net impairment (losses)/recoveries' to reach the "
    "same (Loss)/Profit before tax subtotal - economically the same structure, reproduced as "
    "originally labelled each year. 'Redundancy cost' is a one-off line only disclosed in "
    "FY2023."
)
INCOME_STATEMENT_SOURCES = (
    "Sources - Bank of Africa United Kingdom Plc's own Statement of Profit or Loss, GBP'000:\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements 2025, p.38 - {AR2025_URL}\n"
    f"FY2023 (& FY2022 restated comparative, not used - see note): Annual Report and Financial Statements 2023, p.39 - {AR2023_URL}\n"
    f"FY2022 (originally reported, used as primary column): Annual Report and Financial Statements 2022, p.38 - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2022, p.38 (FY2021 comparative column) - {AR2022_URL}\n\n"
    + INCOME_STATEMENT_PRESENTATION_NOTE + "\n\n" + ENTITY_NOTE
)

income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest and similar income", {"FY2025": 12676, "FY2024": 12402, "FY2023": 17701, "FY2022": 21817, "FY2021": 21793}),
    ("DATA", "Interest expense and similar charges", {"FY2025": -5587, "FY2024": -6728, "FY2023": -10927, "FY2022": -6747, "FY2021": -3212}),
    ("TOTAL", "Net interest income", {"FY2025": 7089, "FY2024": 5674, "FY2023": 6774, "FY2022": 15070, "FY2021": 18581}),
    ("DATA", "Fee and commission income", {"FY2025": 3193, "FY2024": 3678, "FY2023": 3691, "FY2022": 3034, "FY2021": 3193}),
    ("DATA", "Fee and commission expense", {"FY2025": -958, "FY2024": -1332, "FY2023": -2532, "FY2022": -1632, "FY2021": -1526}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 2235, "FY2024": 2346, "FY2023": 1159, "FY2022": 1402, "FY2021": 1667}),
    ("DATA", "Net trading income/(expense)", {"FY2025": 716, "FY2024": 578, "FY2023": -4039, "FY2022": 3000, "FY2021": 4298}),
    ("DATA", "Other operating income", {"FY2023": 284, "FY2022": 33, "FY2021": 51}),
    ("TOTAL", "Net operating income", {"FY2025": 10040, "FY2024": 8598, "FY2023": 4178, "FY2022": 19505, "FY2021": 24597}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Personnel expenses", {"FY2025": -7191, "FY2024": -7054, "FY2023": -8648, "FY2022": -10282, "FY2021": -8982}),
    ("DATA", "Redundancy cost", {"FY2023": -765}),
    ("DATA", "Depreciation on property, plant and equipment", {"FY2025": -180, "FY2024": -111}),
    ("DATA", "Depreciation on right-of-use assets", {"FY2025": -211, "FY2024": -658}),
    ("DATA", "Depreciation of property, plant and equipment; and right-of-use assets", {"FY2023": -976, "FY2022": -1244, "FY2021": -1236}),
    ("DATA", "Amortisation of intangible assets", {"FY2025": -826, "FY2024": -730, "FY2023": -459, "FY2022": -461, "FY2021": -653}),
    ("DATA", "Other operating expenses", {"FY2025": -2251, "FY2024": -6351, "FY2023": -6814, "FY2022": -7471, "FY2021": -7018}),
    ("TOTAL", "Total operating expenses", {"FY2025": -10659, "FY2024": -14904, "FY2023": -17662, "FY2022": -19458, "FY2021": -17889}),
    ("DATA", "Net impairment gain/(losses)", {"FY2025": 3723, "FY2024": 3482, "FY2023": -420, "FY2022": -5325, "FY2021": -1648}),
    ("TOTAL", "Profit/(Loss) before tax", {"FY2025": 3104, "FY2024": -2824, "FY2023": -13904, "FY2022": -5278, "FY2021": 5060}),
    ("DATA", "Taxation credit/(expense)", {"FY2025": -831, "FY2024": 4603, "FY2023": -95, "FY2022": 1439, "FY2021": 622}),
    ("TOTAL", "Profit/(Loss) for the year", {"FY2025": 2273, "FY2024": 1779, "FY2023": -13999, "FY2022": -3839, "FY2021": 5682}),
]

bw.add_income_statement_sheet(
    title="Bank of Africa United Kingdom Plc — Statement of Profit or Loss",
    subtitle="Entity-level (solo) basis, as reported in each year's own Annual Report",
    rows=income_statement_rows,
    sources_text=INCOME_STATEMENT_SOURCES,
    first_col_width=68,
    source_height=220,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Share capital", "Other reserves", "Accumulated losses", "Total equity"]
EQUITY_CHANGES_SOURCES = (
    "Sources - Bank of Africa United Kingdom Plc's own Statement of Changes in Equity, GBP'000:\n"
    f"1 Jan 2021 - 31 Dec 2022 (originally reported): Annual Report and Financial Statements 2022, p.41 - {AR2022_URL}\n"
    f"1 Jan 2023 - 31 Dec 2023 (opening balance restated - see note): Annual Report and Financial Statements 2023, p.42 - {AR2023_URL}\n"
    f"1 Jan 2024 - 31 Dec 2025: Annual Report and Financial Statements 2025, p.41 - {AR2025_URL}\n\n"
    "DATA QUALITY NOTE - genuine restatement break, same one already documented on the Cash "
    "Flow Statement sheet: the FY2022 Annual Report's own closing balance at 31 December 2022 "
    "was Share capital 102,173 / Other reserves (6,845) / Accumulated losses (19,577) / Total "
    "75,751 (loss for the year (3,839)). The FY2023 Annual Report's own opening balance at 1 "
    "January 2023 restates this to Accumulated losses (20,294) / Total 75,034 (loss for the "
    "year restated to (4,556)), consistent with the FY2022 Independent Auditor's Report's own "
    "reference to 'prior year adjustments and ongoing regulatory investigation'. This workbook "
    "shows both: the FY2021-2022 rows follow the originally-reported chain (project "
    "convention - each year's own primary report), and the FY2023 opening row uses the FY2023 "
    "Annual Report's own restated opening balance (since that is the actual starting point of "
    "its own statement) - the £717k break between the two 'Balance at 31 Dec 2022 / 1 Jan "
    "2023' rows is the restatement, not a transcription error.\n\n" + ENTITY_NOTE
)

equity_changes_rows = [
    ("TOTAL", "Balance as at 1 January 2021", (102173, 1625, -21420, 82378)),
    ("DATA", "Profit for the year", (None, None, 5682, 5682)),
    ("DATA", "Other comprehensive income", (None, -5479, None, -5479)),
    ("TOTAL", "Balance as at 31 December 2021", (102173, -3854, -15738, 82581)),
    ("TOTAL", "Balance as at 1 January 2022", (102173, -3854, -15738, 82581)),
    ("DATA", "Loss for the year", (None, None, -3839, -3839)),
    ("DATA", "Other comprehensive income", (None, -2991, None, -2991)),
    ("TOTAL", "Balance as at 31 December 2022 (as originally reported)", (102173, -6845, -19577, 75751)),
    ("TOTAL", "Balance as at 1 January 2023 (restated - see note)", (102173, -6845, -20294, 75034)),
    ("DATA", "Loss for the year", (None, None, -13999, -13999)),
    ("DATA", "Other comprehensive income", (None, 4491, None, 4491)),
    ("TOTAL", "Balance as at 31 December 2023", (102173, -2354, -34293, 65526)),
    ("TOTAL", "Balance as at 1 January 2024", (102173, -2354, -34293, 65526)),
    ("DATA", "Profit for the year", (None, None, 1779, 1779)),
    ("DATA", "Other comprehensive income", (None, 866, None, 866)),
    ("TOTAL", "Balance as at 31 December 2024", (102173, -1488, -32514, 68171)),
    ("TOTAL", "Balance as at 1 January 2025", (102173, -1488, -32514, 68171)),
    ("DATA", "Profit for the year", (None, None, 2273, 2273)),
    ("DATA", "Other comprehensive income", (None, 185, None, 185)),
    ("TOTAL", "Balance as at 31 December 2025", (102173, -1303, -30241, 70629)),
]

bw.add_equity_changes_sheet(
    title="Bank of Africa United Kingdom Plc — Statement of Changes in Equity",
    subtitle="Entity-level (solo) basis, chronological, 1 January 2021 - 31 December 2025",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQUITY_CHANGES_SOURCES,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from continuing operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {"FY2025": 3104, "FY2024": -2824, "FY2023": -13904, "FY2022": -5278, "FY2021": 5060}),
    ("DATA", "Net interest income", {"FY2025": -7089, "FY2024": -5674, "FY2023": -6774, "FY2022": -15070, "FY2021": -18581}),
    ("DATA", "Interest received", {"FY2025": 13028, "FY2024": 12048, "FY2023": 20919, "FY2022": 19859, "FY2021": 27104}),
    ("DATA", "Interest paid", {"FY2025": -6175, "FY2024": -6777, "FY2023": -10607, "FY2022": -7197, "FY2021": -4236}),
    ("DATA", "Change in operating assets", {"FY2025": -54573, "FY2024": -17912, "FY2023": 170939, "FY2022": 21084, "FY2021": 35264}),
    ("DATA", "Change in operating liabilities", {"FY2025": 34977, "FY2024": 33274, "FY2023": -189466, "FY2022": -35633, "FY2021": 14726}),
    ("DATA", "Other (non-cash) items included in profit before tax", {"FY2025": -7125, "FY2024": -1465, "FY2023": 18778, "FY2022": -5399, "FY2021": 1625}),
    ("DATA", "Corporation tax", {"FY2023": 0, "FY2022": 171, "FY2021": -868}),
    ("TOTAL", "Net cash flows from/(used in) operating activities", {"FY2025": -23853, "FY2024": 10670, "FY2023": -10115, "FY2022": -27463, "FY2021": 60094}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Purchase of financial investments", {"FY2025": -53189, "FY2024": -44212, "FY2023": -7685, "FY2022": -6272, "FY2021": -82228}),
    ("DATA", "Proceeds from sales of financial investments", {"FY2025": 64477, "FY2024": 32257, "FY2023": 8036, "FY2022": 17338, "FY2021": 39068}),
    ("DATA", "Purchase of Property, Plant and Equipment (and Right-of-use Assets)", {"FY2025": -22, "FY2024": -470, "FY2023": -1550, "FY2022": -233, "FY2021": -66}),
    ("DATA", "Purchase of intangible assets", {"FY2025": -877, "FY2024": -1569, "FY2023": -1858, "FY2022": -1744, "FY2021": -745}),
    ("TOTAL", "Net cash flows from/(used in) investing activities", {"FY2025": 10389, "FY2024": -13994, "FY2023": -3057, "FY2022": 9089, "FY2021": -43971}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Repayment of lease principal", {"FY2025": -89, "FY2024": -181, "FY2023": -797, "FY2022": -1050, "FY2021": -944}),
    ("TOTAL", "Net cash flows from/(used in) financing activities", {"FY2025": -89, "FY2024": -181, "FY2023": -797, "FY2022": -1050, "FY2021": -944}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": -13553, "FY2024": -3505, "FY2023": -13969, "FY2022": -19424, "FY2021": 15179}),
    ("DATA", "Cash and cash equivalents as at 1 January", {"FY2025": 51070, "FY2024": 54575, "FY2023": 68544, "FY2022": 87968, "FY2021": 72789}),
    ("TOTAL", "Cash and cash equivalents as at 31 December", {"FY2025": 37517, "FY2024": 51070, "FY2023": 54575, "FY2022": 68544, "FY2021": 87968}),
]

bw.add_cash_flow_sheet(
    title="Bank of Africa United Kingdom Plc — Statement of Cash Flows",
    subtitle="Entity-level (solo) basis, as reported in each year's own Annual Report",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=70,
    source_height=210,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
ASSET_QUALITY_PRESENTATION_NOTE = (
    "PRESENTATION NOTE: BOA UK's Loans and advances to customers note (Note 16 in every year's "
    "Annual Report) discloses only a single IFRS 9 stage breakdown - no by-product/by-sector "
    "split. Gross carrying amount FY2025 (42,440) + FY2024 (34,168) + FY2023 (33,745) + FY2022 "
    "(154,905) + FY2021 (168,272) and Carrying amount figures all tie exactly to the Balance "
    "Sheet's own 'Loans and advances to customers' line for each year."
)
ASSET_QUALITY_SOURCES = (
    "Sources - Bank of Africa United Kingdom Plc's own Loans and advances to customers note "
    "(Note 16), GBP'000:\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements 2025, p.65 - {AR2025_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.67 - {AR2023_URL}\n"
    f"FY2022 (originally reported, used as primary column): Annual Report and Financial Statements 2022, p.66 - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2022, p.66 (FY2021 comparative column) - {AR2022_URL}\n\n"
    + ASSET_QUALITY_PRESENTATION_NOTE + "\n\n" + ENTITY_NOTE
)

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers by IFRS 9 stage - gross carrying amount", {}),
    ("DATA", "Stage 1 - 12 months ECL", {"FY2025": 39023, "FY2024": 25334, "FY2023": 20047, "FY2022": 138815, "FY2021": 152521}),
    ("DATA", "Stage 2 - Lifetime ECL", {"FY2025": 678, "FY2024": 3938, "FY2023": 6350, "FY2022": 7799, "FY2021": 0}),
    ("DATA", "Stage 3 - Non performing - Lifetime ECL", {"FY2025": 2739, "FY2024": 4896, "FY2023": 7348, "FY2022": 8291, "FY2021": 15751}),
    ("TOTAL", "Total gross carrying amount", {"FY2025": 42440, "FY2024": 34168, "FY2023": 33745, "FY2022": 154905, "FY2021": 168272}),
    ("SECTION", "Loss allowance by IFRS 9 stage", {}),
    ("DATA", "Stage 1 - 12 months ECL", {"FY2025": -49, "FY2024": -51, "FY2023": -106, "FY2022": -568, "FY2021": -837}),
    ("DATA", "Stage 2 - Lifetime ECL", {"FY2025": -29, "FY2024": -236, "FY2023": -114, "FY2022": -127, "FY2021": 0}),
    ("DATA", "Stage 3 - Non performing - Lifetime ECL", {"FY2025": -410, "FY2024": -4896, "FY2023": -5193, "FY2022": -5925, "FY2021": -5419}),
    ("TOTAL", "Total loss allowance", {"FY2025": -488, "FY2024": -5183, "FY2023": -5413, "FY2022": -6620, "FY2021": -6256}),
    ("SECTION", "Carrying amount", {}),
    ("TOTAL", "Loans and advances to customers (carrying amount)", {"FY2025": 41952, "FY2024": 28985, "FY2023": 28332, "FY2022": 148285, "FY2021": 162016}),
    ("SECTION", "Derived ratios", {}),
    ("DATA", "ECL coverage ratio (total loss allowance / total gross)", {"FY2025": "1.15%", "FY2024": "15.17%", "FY2023": "16.04%", "FY2022": "4.27%", "FY2021": "3.72%"}),
    ("DATA", "Stage 3 / NPL ratio (Stage 3 gross / total gross)", {"FY2025": "6.45%", "FY2024": "14.33%", "FY2023": "21.78%", "FY2022": "5.35%", "FY2021": "9.36%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 allowance / Stage 3 gross)", {"FY2025": "14.97%", "FY2024": "100.00%", "FY2023": "70.68%", "FY2022": "71.46%", "FY2021": "34.40%"}),
]

bw.add_asset_quality_sheet(
    title="Bank of Africa United Kingdom Plc — Asset Quality / Credit Risk Disclosures",
    subtitle="Loans and advances to customers by IFRS 9 stage, entity-level (solo) basis",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=64,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=130)


RESTATEMENT_NOTE = (
    "FY2022 shown here as originally published in the Pillar 3 Disclosures 2022 (Tier 1 "
    "GBP55,465k, Own funds GBP71,130k, RWA GBP453,124k, Total Capital Ratio 15.70%). The "
    "Pillar 3 Disclosures 2023's FY2022 comparative restates this to Tier 1 GBP54,760k, Own "
    "funds GBP70,425k, RWA GBP453,125k, Total Capital Ratio 15.54% - the same restatement "
    "documented on the Cash Flow Statement sheet, consistent with the FY2022 Annual Report's "
    "own auditor's report flagging 'prior year adjustments and ongoing regulatory "
    "investigation'."
)

metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital (= Tier 1 capital; wholly CET1, no AT1 instruments)",
      {"FY2025": 41047, "FY2024": 45680, "FY2023": 44826, "FY2022": 55465, "FY2021": 59466})],
    p3_sources(), note=RESTATEMENT_NOTE,
)

metric(
    "CET1 Ratio", "%",
    [("CET1 Ratio (= Tier 1 Capital Ratio)",
      {"FY2025": "17.46%", "FY2024": "19.65%", "FY2023": "17.75%", "FY2022": "12.24%", "FY2021": "12.36%"})],
    p3_sources(), note=RESTATEMENT_NOTE,
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 Capital",
      {"FY2025": 41047, "FY2024": 45680, "FY2023": 44826, "FY2022": 55465, "FY2021": 59466})],
    p3_sources(), note=RESTATEMENT_NOTE,
)

metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 Capital Ratio",
      {"FY2025": "17.46%", "FY2024": "19.65%", "FY2023": "17.75%", "FY2022": "12.24%", "FY2021": "12.36%"})],
    p3_sources(), note=RESTATEMENT_NOTE,
)

metric(
    "Total Capital", "£'000",
    [("Total Capital / Own Funds (Tier 1 + Tier 2)",
      {"FY2025": 56485, "FY2024": 60323, "FY2023": 60197, "FY2022": 71130, "FY2021": 74498})],
    p3_sources(), note=RESTATEMENT_NOTE,
)

metric(
    "Total Capital Ratio", "%",
    [("Total Capital Ratio (Solvency Ratio)",
      {"FY2025": "24.03%", "FY2024": "25.95%", "FY2023": "23.83%", "FY2022": "15.70%", "FY2021": "15.49%"})],
    p3_sources(), note=RESTATEMENT_NOTE,
)

metric(
    "Total RWAs", "£'000",
    [("Total Risk Weighted Assets (Credit RWA)",
      {"FY2025": 235076, "FY2024": 232412, "FY2023": 252608, "FY2022": 453124, "FY2021": 480918})],
    p3_sources(),
)

RWA_BREAKDOWN_PRESENTATION_NOTE = (
    "PRESENTATION NOTE: FY2025 category breakdown not available - no FY2025 Pillar 3 "
    "disclosure has been published yet (same gap already noted on the Total RWAs and other "
    "Pillar 3 sheets), so only the aggregate Total RWA figure exists for that year and it is "
    "not repeated on this sheet. FY2023's category breakdown (Credit risk 167,168 + CCR 447 + "
    "Market risk 45,736 + Operational risk 39,255 = 252,606) is £2k below the Total RWAs "
    "sheet's own FY2023 total of 252,608 - both figures are transcribed exactly as each "
    "source document states them; not reconciled further. FY2022 and FY2021 totals tie exactly "
    "to the Total RWAs sheet (453,124 and 480,918 respectively)."
)
RWA_BREAKDOWN_SOURCES = (
    "Sources - Bank of Africa United Kingdom Plc's own Pillar 3 Disclosures, 'Overview of Risk "
    "Weighted Assets and Minimum Capital Required under Pillar 1' table, GBP'000:\n"
    f"FY2024 (& FY2023 comparative): Pillar 3 Disclosures 2024, p.22 - {P3_2024_URL}\n"
    f"FY2023 (used as primary column): Pillar 3 Disclosures 2023, p.22 - {P3_2023_URL}\n"
    f"FY2022 (used as primary column, & FY2021 comparative): Pillar 3 Disclosures 2022, p.18-19 - {P3_2022_URL}\n\n"
    + RWA_BREAKDOWN_PRESENTATION_NOTE
)

rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding counterparty credit risk)", {"FY2024": 194090, "FY2023": 167168, "FY2022": 345166, "FY2021": 238172}),
    ("DATA", "Counterparty credit risk (of which CVA)", {"FY2024": 1442, "FY2023": 447, "FY2022": 246, "FY2021": 350}),
    ("DATA", "Market risk", {"FY2024": 7152, "FY2023": 45736, "FY2022": 67257, "FY2021": 206395}),
    ("DATA", "Operational risk", {"FY2024": 29727, "FY2023": 39255, "FY2022": 40455, "FY2021": 36001}),
    ("TOTAL", "Total RWA", {"FY2024": 232412, "FY2023": 252606, "FY2022": 453124, "FY2021": 480918}),
]

bw.add_rwa_breakdown_sheet(
    title="Bank of Africa United Kingdom Plc — RWA Breakdown",
    subtitle="Overview of Risk Weighted Assets under Pillar 1, entity-level (solo) basis",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=54,
)

metric(
    "Leverage Ratio", "%",
    [("Leverage Ratio",
      {"FY2024": "17.67%", "FY2023": "20.66%", "FY2022": "13.98%", "FY2021": "11.51%"})],
    p3_sources(
        "\n\nFY2025 leverage ratio not found - no Pillar 3 edition published yet and the "
        "FY2025 Annual Report's Strategic Report does not state a leverage ratio; left blank "
        "rather than guessed."
    ),
    note="No FY2025 figure - see source note.",
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio",
      {"FY2025": "212%", "FY2024": "207%", "FY2023": "351%", "FY2022": "207%", "FY2021": "203%"})],
    p3_sources(
        "\n\nBASIS NOTE: FY2021-FY2024 are point-in-time (31 December) LCR from each year's "
        "own Pillar 3 KM1 disclosure (FY2024's 207% independently verified by reconstructing "
        "the LCR composition table: HQLA GBP54,641k / net cash outflows GBP26,427k = 206.75% "
        "≈ 207%). FY2025 (212%) is instead the *average LCR throughout the year* as stated "
        "in the FY2025 Annual Report's 'Liquidity and funding' section (no Pillar 3 edition "
        "exists yet for FY2025) - the FY2025 Annual Report separately states FY2024's average "
        "LCR as 228%, a different basis to the 207% point-in-time figure used for FY2024 "
        "above, kept for consistency with every other year in this row. Same "
        "spot-vs-average distinction documented across this project (e.g. ALRAYAN Bank)."
    ),
    note="FY2025 is an average-throughout-year figure (Annual Report); all other years are "
         "point-in-time at 31 December (Pillar 3 KM1) - see source note.",
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio",
      {"FY2025": "173%", "FY2024": "146%"})],
    p3_sources(
        "\n\nNSFR is not quantified in any Pillar 3 KM1 disclosure found (FY2022-FY2024 "
        "editions mention only that the Bank 'monitors net stable funding ratio' "
        "qualitatively). FY2024 and FY2025 figures instead come from the FY2025 Annual "
        "Report's 'Liquidity and funding' narrative. FY2021-FY2023 not found anywhere - left "
        "blank rather than guessed (plausible given the UK NSFR requirement only took effect "
        "from 1 January 2022)."
    ),
    note="FY2021-FY2023 not publicly disclosed - see source note.",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    "No MREL disclosure found in any Annual Report or Pillar 3 document for any year - no "
    "numeric ratio and no qualitative exemption statement either. BOA UK is a small, "
    "non-systemic entity; plausibly below the Bank of England's MREL-setting threshold, but "
    "left as not disclosed rather than assumed. Official Bank of Africa UK financial reports "
    f"and Pillar 3 disclosures archive reviewed: {BOA_FINANCES_URL}. The available official "
    f"Pillar 3 reports are also cited directly above (2022: {P3_2022_URL}; 2023: "
    f"{P3_2023_URL}; 2024: {P3_2024_URL}).",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 328964, "FY2024": 291532, "FY2023": 254441, "FY2022": 452390, "FY2021": 496686}),
        ("Loans and advances to customers", {"FY2025": 41952, "FY2024": 28985, "FY2023": 28332, "FY2022": 148285, "FY2021": 162016}),
        ("Due to customers", {"FY2025": 84367, "FY2024": 44717, "FY2023": 42227, "FY2022": 59541, "FY2021": 92028}),
        ("Total equity", {"FY2025": 70629, "FY2024": 68171, "FY2023": 65526, "FY2022": 75751, "FY2021": 82581}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net operating income", {"FY2025": 10040, "FY2024": 8598, "FY2023": 4178, "FY2022": 19505, "FY2021": 24597}),
        ("Total operating expenses", {"FY2025": -10659, "FY2024": -14904, "FY2023": -17662, "FY2022": -19458, "FY2021": -17889}),
        ("Profit/(Loss) for the year", {"FY2025": 2273, "FY2024": 1779, "FY2023": -13999, "FY2022": -3839, "FY2021": 5682}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 68171, "FY2024": 65526, "FY2023": 75034, "FY2022": 82581, "FY2021": 82378}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": 2458, "FY2024": 2645, "FY2023": -9508, "FY2022": -6830, "FY2021": 203}),
        ("Other equity movements, net", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
        ("Closing equity", {"FY2025": 70629, "FY2024": 68171, "FY2023": 65526, "FY2022": 75751, "FY2021": 82581}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash flows from/(used in) operating activities", {"FY2025": -23853, "FY2024": 10670, "FY2023": -10115, "FY2022": -27463, "FY2021": 60094}),
        ("Net cash flows from/(used in) investing activities", {"FY2025": 10389, "FY2024": -13994, "FY2023": -3057, "FY2022": 9089, "FY2021": -43971}),
        ("Net cash flows from/(used in) financing activities", {"FY2025": -89, "FY2024": -181, "FY2023": -797, "FY2022": -1050, "FY2021": -944}),
        ("Cash and cash equivalents as at 31 December", {"FY2025": 37517, "FY2024": 51070, "FY2023": 54575, "FY2022": 68544, "FY2021": 87968}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "17.46%", "FY2024": "19.65%", "FY2023": "17.75%", "FY2022": "12.24%", "FY2021": "12.36%"}),
        ("Total Capital Ratio", {"FY2025": "24.03%", "FY2024": "25.95%", "FY2023": "23.83%", "FY2022": "15.70%", "FY2021": "15.49%"}),
        ("Leverage Ratio", {"FY2024": "17.67%", "FY2023": "20.66%", "FY2022": "13.98%", "FY2021": "11.51%"}),
        ("LCR", {"FY2025": "212%", "FY2024": "207%", "FY2023": "351%", "FY2022": "207%", "FY2021": "203%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page, and the Cash Flow Statement sheet's source note "
         "for a genuine FY2022 restatement affecting several sheets in this workbook.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BANK OF AFRICA UK FINANCIALS.xlsx")
print("Saved.")
