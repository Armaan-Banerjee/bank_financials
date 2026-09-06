import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Full 5 years of cash flow AND Pillar 3 coverage FY2021-FY2025. No FRS 101/102
# cash-flow exemption at all - clean, active, well-documented UK subsidiary of
# Bank of Beirut SAL (Lebanon), unaffected in its own filings by the parent
# jurisdiction's banking crisis (confirmed active Companies House status,
# unqualified audit opinions, no going-concern language in any of the 5 reports).
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2017"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

CH_URL = "https://find-and-update.company-information.service.gov.uk/company/04406777"
AR2025_URL = "https://www.bankofbeirut.co.uk/Content/uploads/AnnualReport/Annual_Report_and_Financial_Statements_2025_-_for_publishing.pdf"
AR2024_URL = "https://www.bankofbeirut.co.uk/Content/Uploads/AnnualReport/Annual%20Report%20and%20Financial%20Statements%202024%20-%20Final%20-%20for%20publishing250506021233950~.pdf"
AR2023_URL = "https://www.bankofbeirut.co.uk/Content/Uploads/AnnualReport/Annual%20Report%20and%20Financial%20Statements%202023%20-%20for%20publishing240429124230700~.pdf"
AR2021_URL = "https://www.bankofbeirut.co.uk/Content/uploads/AnnualReport/Bank_of_beirut_UK_Annual_Report_-_2021_.pdf"
AR2017_URL = "https://www.bankofbeirut.co.uk/content/uploads/AnnualReport/bankofbeirut-uk2017-annualreport180614103530638~.pdf"
P3_2025_URL = "https://www.bankofbeirut.co.uk/Content/uploads/PillarDisclosure/Bank_of_Beirut_UK_Ltd_-_Pillar_III_Disclosures_-_31_December_2025.pdf"
P3_2024_URL = "https://www.bankofbeirut.co.uk/Content/uploads/Announcement/bob-disclosures3-2024.pdf"
P3_2023_URL = "https://www.bankofbeirut.co.uk/Content/uploads/Announcement/Bank_of_Beirut_UK_Ltd_-_Pillar_III_Disclosures_-_31_December_2023.pdf"
P3_2022_URL = "https://www.bankofbeirut.co.uk/Content/uploads/Announcement/Bank_of_Beirut_UK_Ltd_-_Pillar_III_Disclosures_-_31DEC2022_-_Final.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Bank of Beirut (UK) Ltd (FRN 219523, Companies House 04406777, matches Banks List 2608.xlsx "
    "exactly) is a UK-incorporated subsidiary of Bank of Beirut SAL (Lebanon). Despite Lebanon's severe banking-"
    "sector crisis since 2019, this UK entity remains Active at Companies House with unqualified audit opinions "
    "and no going-concern qualification in any of the 5 Annual Reports reviewed (FY2021-FY2025) - the parent's "
    "distress has not visibly affected this subsidiary's own filings or capital position. Reports in GBP "
    "throughout, no FX conversion needed."
)

CASH_FLOW_SOURCES = (
    "Sources - Bank of Beirut (UK) Ltd's own Cash Flow Statement, converted from £ to £'000s (rounded), all years:\n"
    f"FY2025/FY2024: Annual Report and Financial Statements 2025, p.33 - {AR2025_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.34 - {AR2023_URL}\n"
    f"FY2022: sourced from the Annual Report and Financial Statements 2023's own FY2022 comparative column, p.34 - "
    f"{AR2023_URL}\n"
    f"FY2021: Annual Report & Financial Statements 2021, p.31 - {AR2021_URL}\n"
    "GENUINE UNRESOLVED PRESENTATIONAL BREAK: FY2024's own report (Annual Report 2024, p.34/p.33 Balance Sheet) "
    "states 'Cash and balances at banks' at FY2024 year-end as £139,856,747, matching FY2023's own year-end "
    "figure of £97,312,901 as that year's opening balance - fully self-consistent. But the FY2025 report's own "
    "FY2024 comparative restates BOTH the FY2024 balance-sheet cash figure and the cash-flow opening balance to "
    "£276,517,994 - a £136.7m increase. Tracing this: the FY2025 report's FY2024 comparative 'Placements with "
    "banks' balance-sheet line also drops from its FY2024-report-original £139,666,071 to a restated £3,004,824 "
    "in the same amount as the cash increase (£139,666,071 - £3,004,824 = £136,661,247, matching the cash "
    "increase to the pound). This is evidence of a genuine reclassification - most of 'Placements with banks' "
    "moved into 'Cash and balances at banks' from FY2025 onward, with FY2024 restated for comparability - not an "
    "error. Per this project's convention, each column below keeps ITS OWN report's originally-published figures "
    "(FY2024 = £139,857k as originally stated, FY2025's own opening balance = £276,518k as its own report "
    "states) rather than force-blending the two; the reconciling difference is fully explained above, unlike the "
    "unexplained gap left at Arab Bank Europe.\n"
    "One immaterial £1k rounding artifact in the FY2021 report's own tail chain (kept as printed).\n\n"
    + ENTITY_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - Bank of Beirut (UK) Ltd's own Pillar 3 Disclosures, £m capital amounts / % ratios, all years:\n"
        f"FY2025: Pillar 3 Disclosures - 31 December 2025, s.3.6 Key Metrics (UK KM1 template) - {P3_2025_URL}\n"
        f"FY2024: Pillar 3 Disclosures - 31 December 2024, s.3.6 Key Metrics (UK KM1 template) - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures - 31 December 2023, s.4.2 Key Metrics (UK KM1 template) - {P3_2023_URL}\n"
        f"FY2022: sourced from the FY2023 Pillar 3 Disclosures' own FY2022 KM1 comparative column - {P3_2023_URL}. "
        f"Capital £ figures independently cross-checked against the FY2022 Pillar 3 Disclosures' own 5-year ICAAP "
        f"summary table (s.4.1) - {P3_2022_URL} - and match to the pound (CET1 £103,161,031 both sources); that "
        f"document's TREA is on a different ICAAP basis (£314.6m) vs the KM1/COREP basis used here (£317.6m), a "
        f"~1% difference, KM1 basis used throughout for consistency with FY2023 onward.\n"
        f"FY2021: calculated from the FY2022 Pillar 3 Disclosures' own 5-year ICAAP summary table (s.4.1), which "
        f"predates this bank's adoption of the KM1 template - {P3_2022_URL}. CET1 = Own Funds Capital Resources "
        f"less Eligible Tier II Capital; ratios = £ amount / Total Risk Exposure Amount (Memo line), consistent "
        f"with this project's convention of calculating a ratio from disclosed £ figures where no % is directly "
        f"stated (see Bank of Ireland UK). No Leverage/LCR/NSFR/MREL numeric figures exist in this pre-KM1 "
        f"document (narrative KPI list only, no values) - left blank rather than guessed.\n"
        "No document at any year mentions MREL.\n"
        + (extra + "\n" if extra else "")
        + "\n" + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="Bank of Beirut (UK) Ltd", years=YEARS, year_label=YEAR_LABEL, header_color="6B4226")

STATEMENT_SOURCES = (
    "Sources - Bank of Beirut (UK) Ltd's own Balance Sheet / Income Statement / Statement of Changes in "
    "Equity, converted from £ to £'000s (rounded to nearest £'000), all years:\n"
    f"FY2025/FY2024: Annual Report and Financial Statements 2025, Income Statement p.29, Statement of Other "
    f"Comprehensive Income p.30, Balance Sheet p.31, Statement of Changes in Equity p.32 - {AR2025_URL}\n"
    f"FY2023/FY2022: Annual Report and Financial Statements 2023, Income Statement p.30, Statement of Other "
    f"Comprehensive Income p.31, Balance Sheet p.32, Statement of Changes in Equity p.33 (FY2022 is that "
    f"report's own FY2022 comparative column) - {AR2023_URL}\n"
    f"FY2021: Annual Report & Financial Statements 2021, Income Statement/OCI p.28, Balance Sheet p.29, "
    f"Statement of Changes in Equity p.30 - {AR2021_URL}\n"
    "PRESENTATIONAL BREAK: FY2021's Balance Sheet carries 'Debt securities at amortised cost' and 'Financial "
    "assets at FVTOCI' as separate lines; FY2022 onward consolidates everything into a single 'Financial "
    "assets at amortised cost' line - a genuine reclassification of the investment portfolio, not merged here "
    "(each year's own report structure kept). FY2021 and FY2023's own Balance Sheets carry no 'Derivative "
    "assets/liabilities' line (nil that year); FY2022/FY2024 do.\n"
    "ROUNDING ARTIFACT: FY2021's Statement of Changes in Equity's own Profit-for-year (£1,419,884 -> £1,420k) "
    "and OCI-for-year (£10,501 -> £11k) rows sum to £1,431k against that year's own reported Total "
    "comprehensive income of £1,430,385 (-> £1,430k) - a £1k rounding artifact from independently rounding "
    "each component to the nearest £'000, not a source-document error (the underlying unrounded figures tie "
    "exactly: 1,419,884 + 10,501 = 1,430,385).\n"
    "FY2025's and FY2023's own Balance Sheet Total assets figures (£502,093,745 -> £502,094k; £367,528,644 -> "
    "£367,529k) are each £1k more than Total liabilities + Total equity independently rounded (£379,117k + "
    "£122,976k = £502,093k; £252,533k + £114,995k = £367,528k) - same rounding-artifact class as above, not "
    "an imbalance in the source (both years' unrounded figures tie exactly).\n\n"
    + ENTITY_NOTE
)

# ---------------------------------------------------------------
# Sheet 0a: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at banks", {"FY2025": 254772, "FY2024": 276518, "FY2023": 97313, "FY2022": 97866, "FY2021": 134557}),
    ("DATA", "Placements with banks", {"FY2025": 3554, "FY2024": 3005, "FY2023": 84957, "FY2022": 85207, "FY2021": 90779}),
    ("DATA", "Loans and advances to customers", {"FY2025": 144331, "FY2024": 121491, "FY2023": 121214, "FY2022": 161651, "FY2021": 128986}),
    ("DATA", "Customers' acceptances", {"FY2025": 3581, "FY2024": 1783, "FY2023": 4492, "FY2022": 4089, "FY2021": 8186}),
    ("DATA", "Financial assets at amortised cost", {"FY2025": 68899, "FY2024": 57046, "FY2023": 38551, "FY2022": 35784}),
    ("DATA", "Debt securities at amortised cost", {}),
    ("DATA", "Financial assets at FVTOCI", {"FY2021": 26631}),
    ("DATA", "Derivative assets", {"FY2023": 47}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 1892, "FY2024": 1554, "FY2023": 1057, "FY2022": 1161, "FY2021": 983}),
    ("DATA", "Current tax assets", {"FY2025": 1241, "FY2024": 406}),
    ("DATA", "Land and Buildings", {"FY2025": 18289, "FY2024": 18449, "FY2023": 18583, "FY2022": 18649, "FY2021": 18800}),
    ("DATA", "Right-of-use lease assets", {"FY2025": 345, "FY2024": 419, "FY2023": 531, "FY2022": 608, "FY2021": 731}),
    ("DATA", "Property and equipment", {"FY2025": 631, "FY2024": 778, "FY2023": 699, "FY2022": 855, "FY2021": 384}),
    ("DATA", "Intangible assets", {"FY2025": 4559, "FY2024": 1322, "FY2023": 83, "FY2022": 133, "FY2021": 204}),
    ("TOTAL", "Total assets", {"FY2025": 502094, "FY2024": 482771, "FY2023": 367529, "FY2022": 406004, "FY2021": 410239}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2025": 187647, "FY2024": 162269, "FY2023": 89116, "FY2022": 80596, "FY2021": 88810}),
    ("DATA", "Customer accounts", {"FY2025": 167175, "FY2024": 167963, "FY2023": 137387, "FY2022": 175446, "FY2021": 173317}),
    ("DATA", "Acceptances payable", {"FY2025": 3587, "FY2024": 1797, "FY2023": 4498, "FY2022": 4098, "FY2021": 8218}),
    ("DATA", "Derivative liabilities", {"FY2024": 145, "FY2022": 17}),
    ("DATA", "Accruals and deferred income", {"FY2025": 316, "FY2024": 663, "FY2023": 833, "FY2022": 530, "FY2021": 560}),
    ("DATA", "Lease liabilities", {"FY2025": 388, "FY2024": 479, "FY2023": 588, "FY2022": 655, "FY2021": 765}),
    ("DATA", "Other liabilities", {"FY2025": 3341, "FY2024": 12280, "FY2023": 1886, "FY2022": 1954, "FY2021": 1655}),
    ("DATA", "Current tax liability", {"FY2025": 47, "FY2024": 56, "FY2023": 1386, "FY2022": 417, "FY2021": 132}),
    ("DATA", "Deferred tax liability", {"FY2025": 1970, "FY2024": 1121, "FY2023": 699, "FY2022": 657, "FY2021": 450}),
    ("DATA", "Subordinated loan", {"FY2025": 14646, "FY2024": 15784, "FY2023": 16141, "FY2022": 33549, "FY2021": 31424}),
    ("TOTAL", "Total liabilities", {"FY2025": 379117, "FY2024": 362557, "FY2023": 252533, "FY2022": 297920, "FY2021": 305331}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 34150, "FY2024": 34150, "FY2023": 34150, "FY2022": 34150, "FY2021": 34150}),
    ("DATA", "Retained earnings", {"FY2025": 88826, "FY2024": 86064, "FY2023": 80845, "FY2022": 73934, "FY2021": 70758}),
    ("TOTAL", "Total equity", {"FY2025": 122976, "FY2024": 120214, "FY2023": 114995, "FY2022": 108084, "FY2021": 104908}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 502094, "FY2024": 482771, "FY2023": 367529, "FY2022": 406004, "FY2021": 410239}),
]

bw.add_balance_sheet_sheet(
    title="Bank of Beirut (UK) Ltd — Balance Sheet",
    subtitle="Entity-level basis, £'000s (converted from source £). Full 5 years.",
    rows=balance_sheet_rows,
    sources_text=STATEMENT_SOURCES,
    first_col_width=52,
    source_height=280,
)

# ---------------------------------------------------------------
# Sheet 0b: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 22273, "FY2024": 23830, "FY2023": 20688, "FY2022": 11195, "FY2021": 6286}),
    ("DATA", "Interest expense", {"FY2025": -6352, "FY2024": -5875, "FY2023": -4270, "FY2022": -2956, "FY2021": -2676}),
    ("TOTAL", "Net interest income", {"FY2025": 15921, "FY2024": 17955, "FY2023": 16418, "FY2022": 8239, "FY2021": 3610}),
    ("DATA", "Fees and commission income (net)", {"FY2025": 7359, "FY2024": 6186, "FY2023": 6476, "FY2022": 8211, "FY2021": 7427}),
    ("DATA", "Foreign exchange income", {"FY2025": 952, "FY2024": 888, "FY2023": 1041, "FY2022": 880, "FY2021": 588}),
    ("TOTAL", "Total non-interest income", {"FY2025": 8311, "FY2024": 7073, "FY2023": 7517, "FY2022": 9090, "FY2021": 8015}),
    ("TOTAL", "Total income", {"FY2025": 24232, "FY2024": 25029, "FY2023": 23935, "FY2022": 17329, "FY2021": 11625}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Administrative expenses", {"FY2025": -14398, "FY2024": -12234, "FY2023": -11303, "FY2022": -9666, "FY2021": -9127}),
    ("DATA", "Finance cost", {"FY2025": -23, "FY2024": -83, "FY2023": -32, "FY2022": -38, "FY2021": -43}),
    ("DATA", "Net impairment (losses)/reversal on financial assets", {"FY2025": 368, "FY2024": 241, "FY2023": -736, "FY2022": -2669, "FY2021": -297}),
    ("TOTAL", "Profit before taxation", {"FY2025": 10177, "FY2024": 12953, "FY2023": 11864, "FY2022": 4956, "FY2021": 2157}),
    ("DATA", "Taxation", {"FY2025": -2581, "FY2024": -3283, "FY2023": -2838, "FY2022": -980, "FY2021": -737}),
    ("DATA", "Discontinued operations (Frankfurt Branch)", {"FY2023": -127}),
    ("TOTAL", "Profit for the year", {"FY2025": 7597, "FY2024": 9670, "FY2023": 8899, "FY2022": 3976, "FY2021": 1420}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Financial assets at FVOCI - gains arising during the year", {"FY2022": 3, "FY2021": 13}),
    ("DATA", "Income tax relating to items that may be reclassified", {"FY2022": -1, "FY2021": -2}),
    ("TOTAL", "Other comprehensive income for the year, net of tax", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 2, "FY2021": 11}),
    ("TOTAL", "Total comprehensive income for the year", {"FY2025": 7597, "FY2024": 9670, "FY2023": 8899, "FY2022": 3978, "FY2021": 1430}),
]

bw.add_income_statement_sheet(
    title="Bank of Beirut (UK) Ltd — Profit & Loss",
    subtitle="Entity-level basis, £'000s (converted from source £). Full 5 years.",
    rows=income_statement_rows,
    sources_text=STATEMENT_SOURCES,
    first_col_width=58,
    source_height=280,
)

# ---------------------------------------------------------------
# Sheet 0c: Statement of Changes in Equity
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Called up share capital", "Retained earnings", "Total equity"]
equity_changes_rows = [
    ("DATA", "As at 1 January 2021", (34150, 69328, 103478)),
    ("DATA", "Profit for the year", (0, 1420, 1420)),
    ("DATA", "Other comprehensive income for the year", (0, 11, 11)),
    ("TOTAL", "As at 31 December 2021", (34150, 70758, 104908)),
    ("DATA", "Dividend paid", (0, -802, -802)),
    ("DATA", "Profit for the year", (0, 3976, 3976)),
    ("DATA", "Other comprehensive income for the year", (0, 2, 2)),
    ("TOTAL", "As at 31 December 2022", (34150, 73934, 108084)),
    ("DATA", "Dividend paid", (0, -1988, -1988)),
    ("DATA", "Profit for the year", (0, 8899, 8899)),
    ("TOTAL", "As at 31 December 2023", (34150, 80845, 114995)),
    ("DATA", "Other adjustment", (0, -1, -1)),
    ("DATA", "Dividend paid", (0, -4450, -4450)),
    ("DATA", "Profit for the year", (0, 9670, 9670)),
    ("TOTAL", "As at 31 December 2024", (34150, 86064, 120214)),
    ("DATA", "Dividend paid", (0, -4835, -4835)),
    ("DATA", "Profit for the year", (0, 7597, 7597)),
    ("TOTAL", "As at 31 December 2025", (34150, 88826, 122976)),
]

bw.add_equity_changes_sheet(
    title="Bank of Beirut (UK) Ltd — Statement of Changes in Equity",
    subtitle="Entity-level basis, £'000s (converted from source £), chronological. Full 5 years, 1 Jan 2021 - 31 Dec 2025.",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=STATEMENT_SOURCES,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit for the year", {"FY2025": 7597, "FY2024": 9670, "FY2023": 8899, "FY2022": 3976, "FY2021": 1420}),
    ("DATA", "Taxation", {"FY2025": 2586, "FY2024": 3283, "FY2023": 2838, "FY2022": 980, "FY2021": 737}),
    ("DATA", "Treasury Bills discount and interest", {"FY2025": -233, "FY2024": -277, "FY2023": 594, "FY2022": 0}),
    ("DATA", "Depreciation and amortisation", {"FY2025": 1004, "FY2024": 834, "FY2023": 750, "FY2022": 642, "FY2021": 809}),
    ("DATA", "Impairment reversal/(losses) on financial assets", {"FY2025": -368, "FY2024": -241, "FY2023": 736, "FY2022": 2669, "FY2021": 297}),
    ("DATA", "Finance cost on lease liabilities", {"FY2025": 23, "FY2024": 83, "FY2023": 32, "FY2022": 38, "FY2021": 43}),
    ("DATA", "Interest income", {"FY2025": -22273, "FY2024": -23830}),
    ("DATA", "Interest expense", {"FY2025": 6352, "FY2024": 5875}),
    ("TOTAL", "Operating cash flows before movements in working capital", {"FY2025": -5312, "FY2024": -4603, "FY2023": 13849, "FY2022": 8304, "FY2021": 3306}),
    ("DATA", "Increase/(Decrease) in prepayments and accrued income", {"FY2025": -337, "FY2024": -497, "FY2023": 104, "FY2022": -178, "FY2021": -181}),
    ("DATA", "(Decrease)/Increase in accruals and deferred income", {"FY2025": -347, "FY2024": -170, "FY2023": 303, "FY2022": -31, "FY2021": 263}),
    ("DATA", "Net Increase/(Decrease) in loans and advances to banks and customers", {"FY2025": -24435, "FY2024": -54985, "FY2023": 39905, "FY2022": -27093, "FY2021": 24313}),
    ("DATA", "(Decrease)/Increase in deposits by banks and customer accounts", {"FY2025": 24806, "FY2024": 103729, "FY2023": -29538, "FY2022": -6085, "FY2021": -11002}),
    ("DATA", "(Decrease)/Increase in other liabilities", {"FY2025": -8938, "FY2024": 10394, "FY2023": -69, "FY2022": 299, "FY2021": -1363}),
    ("DATA", "Net (Decrease)/Increase in derivative financial instruments", {"FY2025": -145, "FY2024": 192, "FY2023": -65, "FY2022": 17}),
    ("DATA", "Interest income received", {"FY2025": 23318, "FY2024": 23628}),
    ("DATA", "Interest expense paid", {"FY2025": -6569, "FY2024": -6056}),
    ("DATA", "Corporation tax paid", {"FY2025": -2571, "FY2024": -4710, "FY2023": -1828, "FY2022": -356, "FY2021": -295}),
    ("TOTAL", "Net cash (used in)/generated from operating activities", {"FY2025": -529, "FY2024": 121755, "FY2023": 22662, "FY2022": -25122, "FY2021": 15041}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property, equipment and intangible assets", {"FY2025": -3860, "FY2024": -1906, "FY2023": -355, "FY2022": -769, "FY2021": -128}),
    ("DATA", "Proceeds on maturity of treasury bills and other eligible bills", {"FY2025": 340419, "FY2024": 107809, "FY2023": 43930, "FY2022": 39572, "FY2021": 30077}),
    ("DATA", "Purchase of treasury bills and other eligible bills", {"FY2025": -355953, "FY2024": -125744, "FY2023": -49034, "FY2022": -45974, "FY2021": -29631}),
    ("TOTAL", "Net cash (used in)/generated from investing activities", {"FY2025": -19394, "FY2024": -19841, "FY2023": -5459, "FY2022": -7171, "FY2021": 318}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Lease payments under Finance Lease", {"FY2025": -156, "FY2024": -136, "FY2023": -148, "FY2022": -141, "FY2021": -148}),
    ("DATA", "Subordinated loan redemption", {"FY2023": -17408}),
    ("DATA", "Dividend paid", {"FY2025": -4835, "FY2024": -4450, "FY2023": -1988, "FY2022": -802}),
    ("TOTAL", "Net cash (used in)/generated from financing activities", {"FY2025": -4991, "FY2024": -4586, "FY2023": -19544, "FY2022": -944, "FY2021": -148}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -24915, "FY2024": 42879, "FY2023": -2340, "FY2022": -33237, "FY2021": 15211}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {"FY2025": 276518, "FY2024": 97313, "FY2023": 97866, "FY2022": 134557, "FY2021": 118590}),
    ("DATA", "Effect of exchange rate changes on cash and cash equivalents", {"FY2025": 3169, "FY2024": -335, "FY2023": 1787, "FY2022": -3454, "FY2021": 755}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2025": 254772, "FY2024": 139857, "FY2023": 97313, "FY2022": 97866, "FY2021": 134557}),
]

bw.add_cash_flow_sheet(
    title="Bank of Beirut (UK) Ltd — Cash Flow Statement",
    subtitle="Entity-level basis, £'000s (converted from source £). Full 5 years, no cash-flow exemption.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=300,
    unit_suffix=" (£'000s)",
)

# ---------------------------------------------------------------
# Sheet 2: Asset Quality / Credit Risk Disclosures
# ---------------------------------------------------------------
ASSET_QUALITY_SOURCES = (
    "Sources - Bank of Beirut (UK) Ltd's own IFRS 9 credit risk note (loans and advances to customers), "
    "£'000s (converted from source £, rounded), all years:\n"
    f"FY2025/FY2024: Annual Report and Financial Statements 2025, Note 28.1 Credit risk - {AR2025_URL}\n"
    f"FY2023/FY2022: Annual Report and Financial Statements 2023, Note 30.1 Credit risk - {AR2023_URL}\n"
    f"FY2021: Annual Report & Financial Statements 2021, Note 30.1 Credit risk - {AR2021_URL}\n"
    "No by-product loan breakdown exists in any year's notes - only the IFRS 9 stage view (all lending is to "
    "customers as a single class; the Bank does not sub-segment by retail/corporate/sector in its published "
    "financial statements). Ratios are calculated from each year's own unrounded £ figures, not from the "
    "rounded £'000s shown here, to avoid compounding rounding error.\n"
    "IMMATERIAL RECONCILING DIFFERENCE: each year's Total gross carrying amount below is £90k-£150k (~0.1%) "
    "higher than that year's Balance Sheet 'Loans and advances to customers' net-of-ECL figure would suggest "
    "(Total gross - Total ECL allowance) - most likely accrued interest or fee adjustments not captured in "
    "the credit-risk note's gross carrying table; both source tables are self-consistent within themselves, "
    "this is a genuine small gap between two notes in the Bank's own reports, not a transcription error here.\n\n"
    + ENTITY_NOTE
)

asset_quality_rows = [
    ("SECTION", "Loan book by IFRS 9 stage (gross carrying amount)", {}),
    ("DATA", "Stage 1 (12-month ECL)", {"FY2025": 142128, "FY2024": 119370, "FY2023": 114296, "FY2022": 159945, "FY2021": 118696}),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {"FY2025": 2024, "FY2024": 1587, "FY2023": 7063, "FY2022": 2050, "FY2021": 8389}),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired)", {"FY2025": 6562, "FY2024": 10543, "FY2023": 9952, "FY2022": 9795, "FY2021": 8438}),
    ("TOTAL", "Total gross loans and advances to customers", {"FY2025": 150714, "FY2024": 131500, "FY2023": 131311, "FY2022": 171790, "FY2021": 135523}),
    ("SECTION", "Loss allowance (ECL) by stage", {}),
    ("DATA", "Stage 1 allowance", {"FY2025": 676, "FY2024": 347, "FY2023": 391, "FY2022": 696, "FY2021": 417}),
    ("DATA", "Stage 2 allowance", {"FY2025": 42, "FY2024": 69, "FY2023": 84, "FY2022": 268, "FY2021": 301}),
    ("DATA", "Stage 3 allowance", {"FY2025": 5812, "FY2024": 9688, "FY2023": 9740, "FY2022": 9340, "FY2021": 5960}),
    ("TOTAL", "Total loss allowance", {"FY2025": 6530, "FY2024": 10103, "FY2023": 10215, "FY2022": 10303, "FY2021": 6678}),
    ("SECTION", "Asset quality ratios", {}),
    ("DATA", "ECL coverage ratio (Total allowance / Total gross loans)", {"FY2025": "4.33%", "FY2024": "7.68%", "FY2023": "7.78%", "FY2022": "6.00%", "FY2021": "4.93%"}),
    ("DATA", "Stage 3 / NPL ratio (Stage 3 gross / Total gross loans)", {"FY2025": "4.35%", "FY2024": "8.02%", "FY2023": "7.58%", "FY2022": "5.70%", "FY2021": "6.23%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 allowance / Stage 3 gross)", {"FY2025": "88.57%", "FY2024": "91.89%", "FY2023": "97.87%", "FY2022": "95.35%", "FY2021": "70.65%"}),
]

bw.add_asset_quality_sheet(
    title="Bank of Beirut (UK) Ltd — Asset Quality / Credit Risk Disclosures",
    subtitle="Entity-level basis, £'000s (converted from source £). Full 5 years.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=62,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else "", rows_data, sources_text,
                         note=note, first_col_width=52, source_height=220)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 110.6, "FY2024": 109.0, "FY2023": 105.8, "FY2022": 103.2, "FY2021": 104.0})],
    p3_sources(),
    note="FY2021 is calculated (Own Funds less Eligible Tier II Capital from the pre-KM1 ICAAP table) - see source note.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("CET1 ratio", {"FY2025": "37.49%", "FY2024": "43.57%", "FY2023": "42.56%", "FY2022": "32.49%", "FY2021": "35.14%"})],
    p3_sources(),
    note="FY2021 is calculated (CET1 £ / Total Risk Exposure Amount £, pre-KM1 ICAAP basis) rather than directly disclosed as a percentage.",
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 110.6, "FY2024": 109.0, "FY2023": 105.8, "FY2022": 103.2, "FY2021": 104.0})],
    p3_sources(),
    note="Tier 1 = CET1 every year (no AT1 instruments ever issued).",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "37.49%", "FY2024": "43.57%", "FY2023": "42.56%", "FY2022": "32.49%", "FY2021": "35.14%"})],
    p3_sources(),
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 123.6, "FY2024": 124.9, "FY2023": 121.5, "FY2022": 133.8, "FY2021": 134.6})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "41.93%", "FY2024": "49.95%", "FY2023": "48.87%", "FY2022": "42.14%", "FY2021": "45.50%"})],
    p3_sources(),
    note="FY2021 is calculated (Total Capital £ / Total Risk Exposure Amount £, pre-KM1 ICAAP basis).",
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted exposure amount", {"FY2025": 294.9, "FY2024": 250.1, "FY2023": 248.5, "FY2022": 317.6, "FY2021": 295.9})],
    p3_sources(),
    note="FY2022 (£317.6m) is on the KM1/COREP basis; the same year's ICAAP-basis figure in the FY2022 Pillar 3 "
         "document's own 5-year table is £314.6m - a ~1% methodology difference, KM1 used for consistency with "
         "FY2023 onward. FY2021 (£295.9m) is on the older ICAAP basis only (no KM1 equivalent exists for that year).",
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - Bank of Beirut (UK) Ltd's own Pillar 3 Disclosures, £'000s, all years:\n"
    f"FY2025: Pillar 3 Disclosures - 31 December 2025, s.3.6 Key Metrics (UK KM1) - {P3_2025_URL}\n"
    f"FY2024: Pillar 3 Disclosures - 31 December 2024, s.3.6 Key Metrics (UK KM1) - {P3_2024_URL}\n"
    f"FY2023: Pillar 3 Disclosures - 31 December 2023, s.4.2 Key Metrics (UK KM1) - {P3_2023_URL}\n"
    f"FY2022: FY2023 Pillar 3 Disclosures' own FY2022 KM1 comparative column - {P3_2023_URL}\n"
    f"FY2021: FY2022 Pillar 3 Disclosures' own 5-year ICAAP summary table (s.4.1), pre-KM1 basis - {P3_2022_URL}\n"
    "NOT PUBLICLY DISCLOSED (category split): checked all 4 available Pillar 3 Disclosures (FY2022-FY2025) "
    "directly for a UK OV1-style risk-category breakdown (credit risk / counterparty credit risk / "
    "securitisation / market risk / operational risk) - none exists in any year. Each report's 'Risk-Weighted "
    "Exposure Amounts' section is KM1-only (a single aggregate Total RWA figure), consistent with a bank of "
    "this size. Only the Total row below is populated (ties exactly to the Total RWAs sheet).\n\n"
    + ENTITY_NOTE
)

rwa_breakdown_rows = [
    ("SECTION", "RWA by risk category", {}),
    ("DATA", "Not publicly disclosed (see sources - KM1-only Pillar 3 report, no UK OV1 category breakdown)", {}),
    ("TOTAL", "Total risk-weighted exposure amount", {"FY2025": 294900, "FY2024": 250100, "FY2023": 248500, "FY2022": 317600, "FY2021": 295900}),
]

bw.add_rwa_breakdown_sheet(
    title="Bank of Beirut (UK) Ltd — RWA Breakdown",
    subtitle="Entity-level basis, £'000s. Full 5 years. Category split not publicly disclosed - see sources.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=68,
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio excluding claims on central banks", {"FY2025": "20.42%", "FY2024": "21.19%", "FY2023": "26.38%", "FY2022": "22.88%"})],
    p3_sources(),
    note="Not disclosed for FY2021 - the pre-KM1 Pillar 3 document lists Leverage Ratio as a tracked KPI but "
         "states no numeric value for any year in that edition.",
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio", {"FY2025": "316.67%", "FY2024": "335.52%", "FY2023": "390.70%", "FY2022": "468.51%"})],
    p3_sources(),
    note="Not disclosed for FY2021 - see Leverage Ratio sheet note (same pre-KM1 document limitation).",
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio", {"FY2025": "310.42%", "FY2024": "325.22%", "FY2023": "371.19%", "FY2022": "417.71%"})],
    p3_sources(),
    note="Not disclosed for FY2021 - see Leverage Ratio sheet note (same pre-KM1 document limitation).",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={
        "MREL Ratio": "MREL is not mentioned anywhere in any of the 5 Pillar 3 Disclosures reviewed (searched "
                      "directly, no hits any year) - consistent with a bank of this size not being its own "
                      "resolution entity under the Bank of England's MREL framework.",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 502094, "FY2024": 482771, "FY2023": 367529, "FY2022": 406004, "FY2021": 410239}),
        ("Loans and advances to customers", {"FY2025": 144331, "FY2024": 121491, "FY2023": 121214, "FY2022": 161651, "FY2021": 128986}),
        ("Customer accounts", {"FY2025": 167175, "FY2024": 167963, "FY2023": 137387, "FY2022": 175446, "FY2021": 173317}),
        ("Total equity", {"FY2025": 122976, "FY2024": 120214, "FY2023": 114995, "FY2022": 108084, "FY2021": 104908}),
    ],
    balance_sheet_unit="£'000s",
    income_statement_totals=[
        ("Total income", {"FY2025": 24232, "FY2024": 25029, "FY2023": 23935, "FY2022": 17329, "FY2021": 11625}),
        ("Administrative expenses", {"FY2025": -14398, "FY2024": -12234, "FY2023": -11303, "FY2022": -9666, "FY2021": -9127}),
        ("Profit for the year", {"FY2025": 7597, "FY2024": 9670, "FY2023": 8899, "FY2022": 3976, "FY2021": 1420}),
    ],
    income_statement_unit="£'000s",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 120214, "FY2024": 114995, "FY2023": 108084, "FY2022": 104908, "FY2021": 103478}),
        ("Total comprehensive income for the year", {"FY2025": 7597, "FY2024": 9670, "FY2023": 8899, "FY2022": 3978, "FY2021": 1430}),
        ("Other movements, net", {"FY2025": -4835, "FY2024": -4451, "FY2023": -1988, "FY2022": -802, "FY2021": 0}),
        ("Closing equity", {"FY2025": 122976, "FY2024": 120214, "FY2023": 114995, "FY2022": 108084, "FY2021": 104908}),
    ],
    equity_changes_unit="£'000s",
    cash_flow_totals=[
        ("Net cash (used in)/generated from operating activities", {"FY2025": -529, "FY2024": 121755, "FY2023": 22662, "FY2022": -25122, "FY2021": 15041}),
        ("Net cash (used in)/generated from investing activities", {"FY2025": -19394, "FY2024": -19841, "FY2023": -5459, "FY2022": -7171, "FY2021": 318}),
        ("Net cash (used in)/generated from financing activities", {"FY2025": -4991, "FY2024": -4586, "FY2023": -19544, "FY2022": -944, "FY2021": -148}),
        ("Cash and cash equivalents at end of year", {"FY2025": 254772, "FY2024": 139857, "FY2023": 97313, "FY2022": 97866, "FY2021": 134557}),
    ],
    cash_flow_unit="£'000s",
    ratios=[
        ("CET1 Ratio", {"FY2025": "37.49%", "FY2024": "43.57%", "FY2023": "42.56%", "FY2022": "32.49%", "FY2021": "35.14%"}),
        ("Tier 1 Ratio", {"FY2025": "37.49%", "FY2024": "43.57%", "FY2023": "42.56%", "FY2022": "32.49%", "FY2021": "35.14%"}),
        ("Total Capital Ratio", {"FY2025": "41.93%", "FY2024": "49.95%", "FY2023": "48.87%", "FY2022": "42.14%", "FY2021": "45.50%"}),
        ("Leverage Ratio", {"FY2025": "20.42%", "FY2024": "21.19%", "FY2023": "26.38%", "FY2022": "22.88%"}),
        ("LCR", {"FY2025": "316.67%", "FY2024": "335.52%", "FY2023": "390.70%", "FY2022": "468.51%"}),
        ("NSFR", {"FY2025": "310.42%", "FY2024": "325.22%", "FY2023": "371.19%", "FY2022": "417.71%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. Leverage/LCR/NSFR are blank for FY2021 (pre-KM1 "
         "disclosure with no numeric values published that year). Cash flow FY2024-FY2025 has a genuine, fully "
         "explained (not guessed) presentational break - see the Cash Flow Statement sheet's source note. "
         "Balance Sheet/P&L/Statement of Changes in Equity headline blocks added per the project's spend/risk "
         "lens: 'Loans and advances to customers' and 'Customer accounts' as the capital-allocation view, "
         "'Administrative expenses' as the operating-cost view.",
)

# FY2017 extension from the Bank's own Report and Financial Statements 2017
# (pp.23-27), rounded from £ to £'000. No pre-KM1 Pillar 3 metrics are
# inferred; those regulatory columns remain blank for FY2017.
_fy17 = {
    "Balance Sheet": {
        "Cash and balances at banks": 105686, "Placements with banks": 181949,
        "Loans and advances to customers": 178336, "Customers' acceptances": 8425,
        "Total assets": 520774, "Deposits by banks": 306972,
        "Customer accounts": 92397, "Acceptances payable": 8425,
        "Derivative liabilities": 16, "Accruals and deferred income": 312,
        "Other liabilities": 13, "Current tax liability": 1014,
        "Deferred tax liability": 39, "Subordinated loan": 14827,
        "Total liabilities": 424170, "Called up share capital": 34150,
        "Retained earnings": 62454, "Total equity": 96604,
        "Total liabilities and equity": 520774,
    },
    "Profit & Loss": {
        "Interest income": 10879, "Interest expense": -3579,
        "Net interest income": 7301, "Fees and commission income (net)": 10179,
        "Foreign exchange income": 539, "Total non-interest income": 10718,
        "Total income": 18018, "Administrative expenses": -8149,
        "Net impairment (losses)/reversal on financial assets": -500,
        "Profit before taxation": 9369, "Taxation": -1943,
        "Profit for the year": 7426,
        "Financial assets at FVOCI - gains arising during the year": -6,
        "Other comprehensive income for the year, net of tax": 29,
        "Total comprehensive income for the year": 7455,
    },
    "Cash Flow Statement": {
        "Profit before taxation": 9369,
        "Cash generated from operations": 29272,
        "Corporation tax paid": -1782,
        "Net cash generated by operating activities": 27491,
        "Net cash (used in) / generated from investing activities": -17090,
        "Net cash flow from/(used in) financing activities": 0,
        "Net increase in cash and cash equivalents": 10400,
        "Cash and cash equivalents at the beginning of the year": 96052,
        "Cash and cash equivalents at the end of the year": 105686,
    },
}
for _sheet, _values in _fy17.items():
    _ws = bw.wb[_sheet]
    _labels = {str(_ws.cell(r, 1).value).strip(): r for r in range(4, _ws.max_row + 1)}
    _col = 1 + YEARS.index("FY2017") + 1
    for _label, _value in _values.items():
        if _label in _labels:
            _ws.cell(_labels[_label], _col, _value)

bw.save("/Users/armaan/code/katalysis/banks/BANK OF BEIRUT UK FINANCIALS.xlsx")
print("Saved.")
