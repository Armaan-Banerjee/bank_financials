import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first

CH_URL = "https://find-and-update.company-information.service.gov.uk/company/00185070/filing-history"
AR25_URL = "https://find-and-update.company-information.service.gov.uk/company/00185070/filing-history/MzUyMzkyMTM5MGFkaXF6a2N4/document?format=pdf&download=0"
AR24_URL = "https://find-and-update.company-information.service.gov.uk/company/00185070/filing-history/MzQ2NDAyMTQ4MGFkaXF6a2N4/document?format=pdf&download=0"
AR22_URL = "https://find-and-update.company-information.service.gov.uk/company/00185070/filing-history/MzM3OTU0ODM0NWFkaXF6a2N4/document?format=pdf&download=0"

CASH_FLOW_SOURCES = (
    "Sources — Alpha Bank London Limited (FRN 135327, company 00185070) own Statement of Cash Flows, £000's:\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements 31 December 2025, p.25-26 (Statement of Cash Flows) — {AR25_URL}\n"
    f"FY2023 & FY2024 (cross-checked): Annual Report and Financial Statements 31 December 2024, p.26-27 (Statement of Cash Flows) — {AR24_URL}\n"
    f"FY2022 & FY2021: Annual Report and Financial Statements 31 December 2022, p.22-23 (Statement of Cash Flows) — {AR22_URL}\n"
    "Filed accounts at Companies House are fully scanned/image-only (no text layer) for all 5 years — figures "
    "transcribed via OCR (tesseract) then manually cross-checked against a rendered page image. All figures GBP "
    "throughout (no FX conversion needed).\n"
    "PRESENTATION NOTE: the source restructures this statement across the 5 years. FY2021-FY2024 report an "
    "'adjustments' block (incl. accrued interest income/expense removed from profit) feeding an unlabelled interim "
    "subtotal, then separate blocks for changes in operating assets and operating liabilities, then a block adding "
    "back actual CASH interest received/paid, then tax paid, before the final 'Net cash flows used in operating "
    "activities' total. FY2025 drops both the interim subtotal and the separate cash-interest block entirely (cash "
    "interest is folded directly into the asset/liability movement figures) — cells left blank for FY2025 where "
    "FY2021-FY2024 show a value are genuinely not broken out that year, not a data gap. Section TOTALs (assets "
    "change, liabilities change, investing, financing, and the final operating/net-change/closing-balance figures) "
    "are fully consistent and comparable across all 5 years — verified by hand line-by-line; see "
    "scripts/verify_workbook.py's own docstring re: its known limitation on multi-block tail reconciliation, which "
    "applies here (it will only cleanly auto-check the asset-change and liability-change blocks).\n"
    "Two immaterial (£1k) accrued-vs-cash timing differences exist between the operating-adjustments block's accrued "
    "interest figures and the financing section's actual cash-paid interest figures for FY2023 (£669k accrued vs "
    "£668k paid) and FY2021 (£161k accrued vs £162k paid) — normal accrual/cash timing, not an error, both used "
    "exactly as each section states them.\n"
    "FY2023 investing-activities section: component lines sum to £16,147k but the source's own printed total reads "
    "£16,148k — an immaterial £1k rounding artifact in the original filing, kept as printed (not force-corrected)."
)

def p3_sources():
    return (
        "Sources — Alpha Bank London Limited's own Annual Report (no standalone Pillar 3 document is published; "
        "the Bank is below the threshold requiring one, disclosing capital/liquidity KPIs and a capital breakdown "
        "note within the Annual Report itself):\n"
        f"FY2025 & FY2024: Annual Report 2025, p.6 (Key Performance Indicators) and p.67 Note 34.7 (Capital "
        f"management, Regulatory analysis) — {AR25_URL}\n"
        f"FY2024 & FY2023: Annual Report 2024, p.6 (Key Performance Indicators) and p.68 Note 34.7 (Capital "
        f"management, Regulatory analysis) — {AR24_URL}\n"
        f"FY2022 & FY2021: Annual Report 2022, p.65 Note 34.6 (Capital management, Regulatory analysis) — {AR22_URL}\n"
        f"Companies House filing history — {CH_URL}\n"
        "DATA QUALITY NOTE: the FY2024 Annual Report's own Key Performance Indicators table (p.6) shows a "
        "'Total regulatory capital' line of £68.4m (FY2024) / £66.0m (FY2023) that does NOT match the same report's "
        "own Note 34.7 'Total regulatory capital' figure of £77,015k / £67,916k for the identical years. Comparing "
        "the KPI-table figures against Total Equity (share capital + retained earnings + FVTOCI reserve, i.e. "
        "Tier 1 before the intangible-assets deduction) shows they match almost exactly — the FY2025 Annual Report "
        "itself confirms this by renaming that same KPI line to 'Total equity' and dropping the 'Total regulatory "
        "capital' label entirely. This is treated as a labelling fix made in the FY2025 report rather than an "
        "arithmetic error: Note 34.7's fully itemised, internally-consistent regulatory-capital build-up (used "
        "throughout this workbook) is the correct regulatory figure in every year."
    )

bw = BankWorkbook(bank_name="Alpha Bank London Limited", years=YEARS, header_color="1D3557")

ENTITY_NOTE = (
    "Alpha Bank London Limited (FRN 135327, company 00185070) prepares entity-only accounts - no group/"
    "consolidated statements are produced. All figures below are on that entity-level basis, consistent with "
    "the Cash Flow Statement and Pillar 3 sheets."
)

BALANCE_SHEET_SOURCES = (
    "Sources — Alpha Bank London Limited's own Statement of Financial Position, £000's:\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements 31 December 2025, p.23 (Statement of Financial "
    f"Position) — {AR25_URL}\n"
    f"FY2023 (cross-checked against FY2024 & FY2023 comparative): Annual Report and Financial Statements 31 "
    f"December 2024, p.24 — {AR24_URL}\n"
    f"FY2022 & FY2021: Annual Report and Financial Statements 31 December 2022, p.20 — {AR22_URL}\n"
    "Filed accounts at Companies House are fully scanned/image-only (no text layer) for all 5 years - figures "
    "transcribed via pdf_tools.py render+visual read of each statement page, cross-checked against the adjacent "
    "year's comparative column where available. All figures GBP throughout.\n"
    f"{ENTITY_NOTE}\n"
    "PRESENTATION NOTE: 'Cash and cash equivalents' (FY2025) is labelled 'Cash and due from credit institutions' "
    "in FY2024-FY2021 - same line, relabelled; both are shown under this sheet's 'Cash and cash equivalents' "
    "label. All TOTAL rows (Total assets/Total liabilities/Total equity/Total liabilities and equity) tie out "
    "exactly for every year."
)

INCOME_STATEMENT_SOURCES = (
    "Sources — Alpha Bank London Limited's own Statement of Profit or Loss and Statement of Comprehensive "
    "Income, £000's:\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements 31 December 2025, p.22 — {AR25_URL}\n"
    f"FY2023 (cross-checked against FY2024 & FY2023 comparative): Annual Report and Financial Statements 31 "
    f"December 2024, p.23 — {AR24_URL}\n"
    f"FY2022 & FY2021: Annual Report and Financial Statements 31 December 2022, p.19 — {AR22_URL}\n"
    "Filed accounts at Companies House are fully scanned/image-only (no text layer) for all 5 years - figures "
    "transcribed via pdf_tools.py render+visual read of each statement page.\n"
    f"{ENTITY_NOTE}\n"
    "'Net trading income/(expense)' is presented as a positive figure some years and negative in others exactly "
    "as printed in the source (a genuine swing between net trading gains and losses year to year, not a sign "
    "error). All TOTAL rows tie out exactly for every year; 'Total comprehensive income for the year, net of "
    "tax' also ties to the Statement of Changes in Equity's own 'Total comprehensive income' movement row for "
    "every year."
)

EQUITY_CHANGES_SOURCES = (
    "Sources — Alpha Bank London Limited's own Statement of Changes in Equity, £000's, chronological (1 January "
    "2021 to 31 December 2025):\n"
    f"FY2025 & FY2024 movements: Annual Report and Financial Statements 31 December 2025, p.24 — {AR25_URL}\n"
    f"FY2023 movements (cross-checked against FY2024 & FY2023 comparative): Annual Report and Financial "
    f"Statements 31 December 2024, p.25 — {AR24_URL}\n"
    f"FY2022 & FY2021 movements: Annual Report and Financial Statements 31 December 2022, p.21 — {AR22_URL}\n"
    "Filed accounts at Companies House are fully scanned/image-only (no text layer) for all 5 years - figures "
    "transcribed via pdf_tools.py render+visual read of each statement page.\n"
    f"{ENTITY_NOTE}\n"
    "Equity components are Share capital, Retained earnings, and a Fair value reserve (FVTOCI debt-instrument "
    "movements) - no other reserve types exist across the 5 years. All 'Balance as at' rows tie out exactly to "
    "the Balance Sheet sheet's own Total equity figure for the matching year-end."
)

ASSET_QUALITY_SOURCES = (
    "Sources — Alpha Bank London Limited's own Note 19 (Loans and advances to customers) and Note 34.3 (Credit "
    "risk) IFRS 9 loss-allowance-by-stage disclosures, £000's:\n"
    f"FY2025 & FY2024 (by-product breakdown, gross/ECL/carrying): Annual Report and Financial Statements 31 "
    f"December 2025, p.45 — {AR25_URL}\n"
    f"FY2023 (cross-checked against FY2024 & FY2023 comparative): Annual Report and Financial Statements 31 "
    f"December 2024, p.46 — {AR24_URL}\n"
    f"FY2022 & FY2021: Annual Report and Financial Statements 31 December 2022, p.44 — {AR22_URL}\n"
    f"FY2025 & FY2024 loss-allowance-by-IFRS-9-stage roll-forward (Loans and advances to customers): Annual "
    f"Report and Financial Statements 31 December 2025, p.57 — {AR25_URL}\n"
    "Filed accounts at Companies House are fully scanned/image-only (no text layer) for all 5 years - figures "
    "transcribed via pdf_tools.py render+visual read of each note page.\n"
    f"{ENTITY_NOTE}\n"
    "DISCLOSURE GRANULARITY NOTE: the by-product split (Retail = Mortgage + Consumer lending; Corporate lending) "
    "with gross carrying amount/ECL allowance/net carrying amount is disclosed for all 5 years. The £-value "
    "by-IFRS-9-Stage-1/2/3 GROSS EXPOSURE breakdown is not disclosed in any year reviewed - only the loss "
    "ALLOWANCE (not the underlying exposure) is broken out by stage, and only for FY2025/FY2024 (a stage-level "
    "table for FY2023/FY2022/FY2021 was not located in the sections reviewed). This is an extremely low-credit-"
    "risk book (ECL allowance is £3k-£432k against £325m-£454m of gross lending across the 5 years, reflecting "
    "that 'almost 100%' of lending is fully collateralised per the source's own Note 34.3.4) - Stage 2/3 "
    "allowances are consistently nil or near-nil. No NPL/non-performing-exposure £ or % figure is separately "
    "disclosed in any year; a coverage ratio (ECL allowance ÷ gross lending) is shown below instead, calculated "
    "from the disclosed totals."
)

def _cov_ratio(ecl, gross):
    return f"{abs(ecl) / gross * 100:.2f}%"

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents", {"FY2025": 44211, "FY2024": 36967, "FY2023": 40658, "FY2022": 38160, "FY2021": 80857}),
    ("DATA", "Derivative financial instruments", {"FY2025": 263, "FY2024": 2868, "FY2023": 345, "FY2022": 3261}),
    ("DATA", "Investment securities", {"FY2025": 39897, "FY2024": 42230, "FY2023": 78097, "FY2022": 92051, "FY2021": 85647}),
    ("DATA", "Loans and advances to customers", {"FY2025": 454489, "FY2024": 397459, "FY2023": 330090, "FY2022": 325461, "FY2021": 357822}),
    ("DATA", "Property and equipment", {"FY2025": 1020, "FY2024": 1987, "FY2023": 2861, "FY2022": 3804, "FY2021": 4787}),
    ("DATA", "Intangible assets", {"FY2025": 3021, "FY2024": 1367, "FY2023": 87, "FY2022": 69, "FY2021": 116}),
    ("DATA", "Current tax assets", {"FY2025": 584, "FY2024": 402, "FY2023": 110, "FY2022": 14, "FY2021": 52}),
    ("DATA", "Deferred tax assets", {"FY2025": 611, "FY2023": 28, "FY2022": 50}),
    ("DATA", "Other assets", {"FY2025": 3220, "FY2024": 1856, "FY2023": 799, "FY2022": 1002, "FY2021": 1215}),
    ("TOTAL", "Total assets", {"FY2025": 547316, "FY2024": 485136, "FY2023": 453075, "FY2022": 463872, "FY2021": 530496}),

    ("SECTION", "Liabilities", {}),
    ("DATA", "Due to banks", {"FY2025": 7300, "FY2024": 1962, "FY2023": 201, "FY2022": 6388, "FY2021": 30194}),
    ("DATA", "Derivative financial instruments", {"FY2025": 793, "FY2024": 899, "FY2023": 1724, "FY2022": 1843, "FY2021": 2502}),
    ("DATA", "Due to customers", {"FY2025": 454928, "FY2024": 397172, "FY2023": 370324, "FY2022": 380738, "FY2021": 424160}),
    ("DATA", "Subordinated debt", {"FY2025": 10004, "FY2024": 10004, "FY2023": 10006, "FY2022": 10003, "FY2021": 10001}),
    ("DATA", "Deferred tax liabilities", {"FY2025": 616, "FY2024": 251, "FY2023": 16, "FY2022": 16, "FY2021": 64}),
    ("DATA", "Lease liabilities", {"FY2025": 1138, "FY2024": 1996, "FY2023": 2811, "FY2022": 3611, "FY2021": 4385}),
    ("DATA", "Provisions", {"FY2025": 1, "FY2023": 1, "FY2021": 6}),
    ("DATA", "Other liabilities", {"FY2025": 4987, "FY2024": 4470, "FY2023": 1989, "FY2022": 1739, "FY2021": 2814}),
    ("TOTAL", "Total liabilities", {"FY2025": 479767, "FY2024": 416754, "FY2023": 387072, "FY2022": 404338, "FY2021": 474126}),

    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 30000, "FY2024": 30000, "FY2023": 30000, "FY2022": 30000, "FY2021": 30000}),
    ("DATA", "Retained earnings", {"FY2025": 37540, "FY2024": 38360, "FY2023": 36005, "FY2022": 29685, "FY2021": 26318}),
    ("DATA", "Fair value reserve", {"FY2025": 9, "FY2024": 22, "FY2023": -2, "FY2022": -151, "FY2021": 52}),
    ("TOTAL", "Total equity", {"FY2025": 67549, "FY2024": 68382, "FY2023": 66003, "FY2022": 59534, "FY2021": 56370}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 547316, "FY2024": 485136, "FY2023": 453075, "FY2022": 463872, "FY2021": 530496}),
]

income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest and similar income", {"FY2025": 40745, "FY2024": 41240, "FY2023": 36264, "FY2022": 19333, "FY2021": 13080}),
    ("DATA", "Interest expense and similar charges", {"FY2025": -20860, "FY2024": -20382, "FY2023": -15359, "FY2022": -4329, "FY2021": -2107}),
    ("TOTAL", "Net interest income", {"FY2025": 19885, "FY2024": 20858, "FY2023": 20905, "FY2022": 15004, "FY2021": 10973}),
    ("DATA", "Fees and commission income", {"FY2025": 1162, "FY2024": 1284, "FY2023": 1126, "FY2022": 1557, "FY2021": 2446}),
    ("DATA", "Net trading income/(expense)", {"FY2025": 374, "FY2024": 60, "FY2023": -67, "FY2022": -340, "FY2021": -98}),
    ("DATA", "Other operating (expense)/income", {"FY2025": -35, "FY2024": 97, "FY2023": 36, "FY2022": 120, "FY2021": 143}),
    ("DATA", "Net loss from derecognition of financial assets measured at FVTOCI", {"FY2025": 0, "FY2024": -34, "FY2023": -82, "FY2022": -41, "FY2021": -38}),
    ("TOTAL", "Operating income", {"FY2025": 21386, "FY2024": 22265, "FY2023": 21918, "FY2022": 16300, "FY2021": 13426}),

    ("SECTION", "Operating expenses", {}),
    ("DATA", "Staff costs", {"FY2025": -11526, "FY2024": -9688, "FY2023": -8892, "FY2022": -7845, "FY2021": -7176}),
    ("DATA", "General administrative expenses", {"FY2025": -9699, "FY2024": -8415, "FY2023": -3886, "FY2022": -3512, "FY2021": -3462}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -1230, "FY2024": -1006, "FY2023": -1044, "FY2022": -1039, "FY2021": -1028}),
    ("TOTAL", "Operating expenses", {"FY2025": -22455, "FY2024": -19109, "FY2023": -13822, "FY2022": -12396, "FY2021": -11666}),

    ("DATA", "Reversal of impairment/(provision) for credit losses", {"FY2025": 3, "FY2024": 7, "FY2023": 171, "FY2022": 256, "FY2021": 108}),
    ("TOTAL", "(Loss)/Profit before tax", {"FY2025": -1066, "FY2024": 3163, "FY2023": 8267, "FY2022": 4160, "FY2021": 1868}),
    ("DATA", "Income tax (expense)/credit", {"FY2025": 246, "FY2024": -808, "FY2023": -1947, "FY2022": -793, "FY2021": -364}),
    ("TOTAL", "(Loss)/Profit after tax", {"FY2025": -820, "FY2024": 2355, "FY2023": 6320, "FY2022": 3367, "FY2021": 1504}),

    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Fair value movement of debt instruments at FVTOCI", {"FY2025": -1, "FY2024": -5, "FY2023": 70, "FY2022": -247, "FY2021": 56}),
    ("DATA", "Allowance for ECL movement of debt instruments at FVTOCI", {"FY2025": -12, "FY2024": -5, "FY2023": -3, "FY2022": 3, "FY2021": -13}),
    ("DATA", "Amounts reclassified to profit or loss for debt instruments measured at FVTOCI", {"FY2025": 0, "FY2024": 34, "FY2023": 82, "FY2022": 41, "FY2021": 38}),
    ("TOTAL", "Other comprehensive (expense)/income", {"FY2025": -13, "FY2024": 24, "FY2023": 149, "FY2022": -203, "FY2021": 81}),
    ("TOTAL", "Total comprehensive income for the year, net of tax", {"FY2025": -833, "FY2024": 2379, "FY2023": 6469, "FY2022": 3164, "FY2021": 1585}),
]

EQUITY_HEADERS = ["Share capital", "Retained earnings", "Fair value reserve", "Total equity"]
equity_changes_rows = [
    ("TOTAL", "Balance as at 1 January 2021", (30000, 24814, -29, 54785)),
    ("DATA", "Profit after tax", (None, 1504, None, 1504)),
    ("DATA", "Other comprehensive income for the year", (None, None, 81, 81)),
    ("TOTAL", "Total comprehensive income for the year", (None, 1504, 81, 1585)),
    ("TOTAL", "Balance attributable to the owner as at 31 December 2021", (30000, 26318, 52, 56370)),

    ("TOTAL", "Balance as at 1 January 2022", (30000, 26318, 52, 56370)),
    ("DATA", "Profit after tax", (None, 3367, None, 3367)),
    ("DATA", "Other comprehensive expense for the year", (None, None, -203, -203)),
    ("TOTAL", "Total comprehensive income for the year", (None, 3367, -203, 3164)),
    ("TOTAL", "Balance attributable to the owner as at 31 December 2022", (30000, 29685, -151, 59534)),

    ("TOTAL", "Balance as at 1 January 2023", (30000, 29685, -151, 59534)),
    ("DATA", "Profit after tax", (None, 6320, None, 6320)),
    ("DATA", "Other comprehensive income for the year", (None, None, 149, 149)),
    ("TOTAL", "Total comprehensive income for the year", (None, 6320, 149, 6469)),
    ("TOTAL", "Balance attributable to the owner as at 31 December 2023", (30000, 36005, -2, 66003)),

    ("TOTAL", "Balance as at 1 January 2024", (30000, 36005, -2, 66003)),
    ("DATA", "Profit after tax", (None, 2355, None, 2355)),
    ("DATA", "Other comprehensive income for the year", (None, None, 24, 24)),
    ("TOTAL", "Total comprehensive income for the year", (None, 2355, 24, 2379)),
    ("TOTAL", "Balance attributable to the owner as at 31 December 2024", (30000, 38360, 22, 68382)),

    ("TOTAL", "Balance as at 1 January 2025", (30000, 38360, 22, 68382)),
    ("DATA", "(Loss) after tax", (None, -820, None, -820)),
    ("DATA", "Other comprehensive expense for the year", (None, None, -13, -13)),
    ("TOTAL", "Total comprehensive income for the year", (None, -820, -13, -833)),
    ("TOTAL", "Balance attributable to the owner as at 31 December 2025", (30000, 37540, 9, 67549)),
]

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers by product — gross carrying amount", {}),
    ("DATA", "Mortgage lending", {"FY2025": 21626, "FY2024": 22798, "FY2023": 24460, "FY2022": 24842, "FY2021": 28943}),
    ("DATA", "Consumer lending", {"FY2025": 13088, "FY2024": 11055, "FY2023": 5891, "FY2022": 5459, "FY2021": 6608}),
    ("TOTAL", "Retail lending (gross)", {"FY2025": 34714, "FY2024": 33853, "FY2023": 30351, "FY2022": 30301, "FY2021": 35551}),
    ("DATA", "Corporate lending (gross)", {"FY2025": 419778, "FY2024": 363615, "FY2023": 299749, "FY2022": 295339, "FY2021": 322703}),
    ("TOTAL", "Total lending (gross carrying amount)", {"FY2025": 454492, "FY2024": 397468, "FY2023": 330100, "FY2022": 325640, "FY2021": 358254}),

    ("SECTION", "ECL allowance by product", {}),
    ("DATA", "Retail lending ECL allowance", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": -385}),
    ("DATA", "Corporate lending ECL allowance", {"FY2025": -3, "FY2024": -9, "FY2023": -10, "FY2022": -179, "FY2021": -47}),
    ("TOTAL", "Total ECL allowance", {"FY2025": -3, "FY2024": -9, "FY2023": -10, "FY2022": -179, "FY2021": -432}),
    ("TOTAL", "Total lending (net carrying amount)", {"FY2025": 454489, "FY2024": 397459, "FY2023": 330090, "FY2022": 325461, "FY2021": 357822}),

    ("SECTION", "ECL allowance by IFRS 9 stage — Loans and advances to customers (closing balance; gross exposure by stage not separately disclosed)", {}),
    ("DATA", "Stage 1 (12-month ECL)", {"FY2025": -2, "FY2024": -9}),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {"FY2025": -1, "FY2024": 0}),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired)", {"FY2025": 0, "FY2024": 0}),
    ("TOTAL", "Total ECL allowance by stage", {"FY2025": -3, "FY2024": -9}),

    ("SECTION", "Derived ratios", {}),
    ("DATA", "ECL coverage ratio (Total ECL allowance ÷ Total gross lending)",
     {y: _cov_ratio(v, g) for y, v, g in [
         ("FY2025", 3, 454492), ("FY2024", 9, 397468), ("FY2023", 10, 330100),
         ("FY2022", 179, 325640), ("FY2021", 432, 358254),
     ]}),
]

RWA_BREAKDOWN_SOURCES = (
    "Sources — Alpha Bank London Limited's own Note 34.7 (Capital management, Regulatory analysis) and the "
    f"Annual Report's Key Performance Indicators table:\n{AR25_URL}\n{AR24_URL}\n{AR22_URL}\n"
    "NOT PUBLICLY DISCLOSED: as noted on the Total RWAs sheet, this bank does not publish a standalone Pillar 3 "
    "document or a UK OV1-style risk-weighted-exposure-by-category table in any of the 5 Annual Reports reviewed "
    "(confirmed by reading Note 34.7 in full, p.67 of the 2025 Annual Report and the equivalent pages of the "
    "2024/2022 Annual Reports — it discloses only the aggregate Tier 1/Tier 2/Total regulatory capital build-up, "
    "not a risk-category RWA split). Total RWAs (a single aggregate figure) is calculated on the Total RWAs "
    "sheet from Total Capital ÷ Capital adequacy ratio, per that sheet's own note; no further breakdown by "
    "credit/market/operational risk is available for any year."
)
rwa_breakdown_rows = [
    ("DATA", "RWA category breakdown", {y: "Not publicly disclosed" for y in YEARS}),
]

bw.add_balance_sheet_sheet(
    title="Alpha Bank London Limited — Statement of Financial Position",
    subtitle="Entity-level basis, £000's, as at 31 December, FY2021-FY2025",
    rows=balance_sheet_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    unit_suffix=" (£'000)",
)

bw.add_income_statement_sheet(
    title="Alpha Bank London Limited — Statement of Profit or Loss and Other Comprehensive Income",
    subtitle="Entity-level basis, £000's, FY2021-FY2025",
    rows=income_statement_rows,
    sources_text=INCOME_STATEMENT_SOURCES,
    unit_suffix=" (£'000)",
)

bw.add_equity_changes_sheet(
    title="Alpha Bank London Limited — Statement of Changes in Equity",
    subtitle="Entity-level basis, £000's, chronological, 1 January 2021 - 31 December 2025",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQUITY_CHANGES_SOURCES,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "(Loss)/profit before tax", {"FY2025": -1066, "FY2024": 3163, "FY2023": 8267, "FY2022": 4160, "FY2021": 1868}),
    ("DATA", "Interest income on investment securities", {"FY2025": -1367, "FY2024": -2894, "FY2023": -4042, "FY2022": -630, "FY2021": 248}),
    ("DATA", "Interest income on loans and advances to customers (accrued)", {"FY2024": -29603, "FY2023": -25319, "FY2022": -16874, "FY2021": -12771}),
    ("DATA", "Interest expense on due to banks (accrued)", {"FY2024": 0, "FY2023": 624, "FY2022": 2316, "FY2021": 1484}),
    ("DATA", "Interest expense on due to customers (accrued)", {"FY2024": 7547, "FY2023": 7383, "FY2022": 355, "FY2021": 144}),
    ("DATA", "Interest expense on debt securities in issue and other borrowed funds", {"FY2025": 690, "FY2024": 726, "FY2023": 669, "FY2022": 340, "FY2021": 207}),
    ("DATA", "Interest expense on lease liabilities", {"FY2025": 54, "FY2024": 139, "FY2023": 185, "FY2022": 138, "FY2021": 161}),
    ("DATA", "Gain/(loss) on forward revaluation of FX transactions", {"FY2025": -374, "FY2024": -60, "FY2023": 67, "FY2022": 340, "FY2021": 98}),
    ("DATA", "Gain on foreign exchange", {"FY2025": 49, "FY2024": -100, "FY2023": -96, "FY2022": -120, "FY2021": -143}),
    ("DATA", "(Loss)/gain from derecognition of investment securities", {"FY2025": -1, "FY2024": 28, "FY2023": 152, "FY2022": -206, "FY2021": 94}),
    ("DATA", "Movement in ECL allowance on investment securities", {"FY2025": 0, "FY2024": -5, "FY2023": -3, "FY2022": 3, "FY2021": -13}),
    ("DATA", "Movement in ECL allowance on loans and advances to customers", {"FY2025": 2, "FY2024": -1, "FY2023": -168, "FY2022": -254, "FY2021": -92}),
    ("DATA", "Movement in ECL allowance on undrawn commitments", {"FY2025": 1, "FY2024": -1}),
    ("DATA", "Depreciation and amortisation", {"FY2025": 1230, "FY2024": 992, "FY2023": 1044, "FY2022": 1039, "FY2021": 1028}),
    ("DATA", "Provision", {"FY2023": 1, "FY2022": 0, "FY2021": 6}),
    ("TOTAL", "Cash flows before changes in operating assets/liabilities (as reported; not broken out FY2025)", {"FY2024": -20069, "FY2023": -11236, "FY2022": -9393, "FY2021": -7681}),

    ("SECTION", "Net increase/(decrease) in assets relating to operating activities", {}),
    ("DATA", "Derivative financial instruments", {"FY2025": 2605, "FY2024": -2523, "FY2023": 2916, "FY2022": -3261, "FY2021": 452}),
    ("DATA", "Investment securities", {"FY2025": 447, "FY2024": 8164, "FY2023": 1729, "FY2022": -5211, "FY2021": -3265}),
    ("DATA", "Loans and advances to customers", {"FY2025": -57033, "FY2024": -67368, "FY2023": -4461, "FY2022": 32615, "FY2021": -20115}),
    ("DATA", "Other assets", {"FY2025": -1364, "FY2024": -1057, "FY2023": 203, "FY2022": 213, "FY2021": 61}),
    ("TOTAL", "Total change in operating assets", {"FY2025": -55345, "FY2024": -62784, "FY2023": 387, "FY2022": 24356, "FY2021": -22867}),

    ("SECTION", "Net increase/(decrease) in liabilities relating to operating activities", {}),
    ("DATA", "Derivative financial instruments", {"FY2025": -106, "FY2024": -825, "FY2023": -119, "FY2022": -659, "FY2021": 523}),
    ("DATA", "Due to banks", {"FY2025": 5337, "FY2024": 1761, "FY2023": -6187, "FY2022": -23806, "FY2021": 27128}),
    ("DATA", "Due to customers", {"FY2025": 57757, "FY2024": 26848, "FY2023": -10414, "FY2022": -43423, "FY2021": -91738}),
    ("DATA", "Other borrowed funds", {"FY2025": 0, "FY2024": -2, "FY2023": 3, "FY2022": 2, "FY2021": 1}),
    ("DATA", "Other liabilities", {"FY2025": 517, "FY2024": 2481, "FY2023": 250, "FY2022": -1075, "FY2021": 1209}),
    ("TOTAL", "Total change in operating liabilities", {"FY2025": 63505, "FY2024": 30263, "FY2023": -16467, "FY2022": -68961, "FY2021": -62877}),

    ("SECTION", "Cash interest received/(paid) reconciliation (as reported; not broken out FY2025)", {}),
    ("DATA", "Interest income on loans and advances to customers (cash received)", {"FY2024": 29603, "FY2023": 25319, "FY2022": 16874, "FY2021": 12771}),
    ("DATA", "Interest expense on due to banks (cash paid)", {"FY2024": 0, "FY2023": -624, "FY2022": -2316, "FY2021": -1484}),
    ("DATA", "Interest expense on due to customers (cash paid)", {"FY2024": -7547, "FY2023": -7383, "FY2022": -355, "FY2021": -144}),
    ("TOTAL", "Total cash interest reconciliation", {"FY2024": 22056, "FY2023": 17312, "FY2022": 14203, "FY2021": 11143}),

    ("DATA", "Income tax paid", {"FY2025": -182, "FY2024": -836, "FY2023": -2022, "FY2022": -805, "FY2021": -482}),
    ("TOTAL", "Net cash flows used in operating activities", {"FY2025": 7196, "FY2024": -31370, "FY2023": -12026, "FY2022": -40650, "FY2021": -82764}),

    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Acquisition of investment securities", {"FY2025": -102879, "FY2024": -32554, "FY2023": -44562, "FY2022": -97105, "FY2021": -62157}),
    ("DATA", "Disposal/maturity of investment securities", {"FY2025": 104753, "FY2024": 60257, "FY2023": 56786, "FY2022": 95910, "FY2021": 129499}),
    ("DATA", "Interest income/(expense) on investment securities", {"FY2025": 1367, "FY2024": 2894, "FY2023": 4042, "FY2022": 630, "FY2021": -248}),
    ("DATA", "Acquisition of fixed assets (including intangibles)", {"FY2025": -1916, "FY2024": -1398, "FY2023": -119, "FY2022": -9, "FY2021": -189}),
    ("TOTAL", "Net cash flows from investing activities", {"FY2025": 1325, "FY2024": 29199, "FY2023": 16148, "FY2022": -574, "FY2021": 66905}),

    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Repayment of lease liabilities", {"FY2025": -858, "FY2024": -815, "FY2023": -800, "FY2022": -775, "FY2021": -725}),
    ("DATA", "Interest paid on other borrowed funds", {"FY2025": -690, "FY2024": -726, "FY2023": -668, "FY2022": -340, "FY2021": -207}),
    ("DATA", "Interest paid on lease liabilities", {"FY2025": -54, "FY2024": -139, "FY2023": -185, "FY2022": -138, "FY2021": -162}),
    ("TOTAL", "Net cash flows used in financing activities", {"FY2025": -1602, "FY2024": -1680, "FY2023": -1653, "FY2022": -1253, "FY2021": -1094}),

    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 6919, "FY2024": -3851, "FY2023": 2469, "FY2022": -42477, "FY2021": -16953}),
    ("DATA", "Cash and cash equivalents at beginning of the year", {"FY2025": 36967, "FY2024": 40658, "FY2023": 38160, "FY2022": 80857, "FY2021": 97765}),
    ("DATA", "Net effect of foreign exchange fluctuations", {"FY2025": 325, "FY2024": 160, "FY2023": 29, "FY2022": -220, "FY2021": 45}),
    ("TOTAL", "Cash and cash equivalents at end of the year", {"FY2025": 44211, "FY2024": 36967, "FY2023": 40658, "FY2022": 38160, "FY2021": 80857}),
]

bw.add_cash_flow_sheet(
    title="Alpha Bank London Limited — Cash Flow Statement",
    subtitle="Entity-level basis, £000's, FY2021-FY2025",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    unit_suffix=" (£'000)",
)

bw.add_asset_quality_sheet(
    title="Alpha Bank London Limited — Asset Quality / Credit Risk Disclosures",
    subtitle="Entity-level basis, £000's, FY2021-FY2025",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Entity-level basis, {unit}" if unit else "Entity-level basis",
                         rows_data, sources_text, note=note, first_col_width=46, source_height=110)

metric(
    "CET1 Capital", "£000's",
    [("Common Equity Tier 1 (CET1) capital = Total Tier 1 capital (no AT1 instruments)",
      {"FY2025": 64528, "FY2024": 67015, "FY2023": 65916, "FY2022": 59465, "FY2021": 56254})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("CET1 ratio", {y: "Not separately disclosed" for y in YEARS})],
    p3_sources(),
    note="The source discloses only a single combined 'Capital adequacy ratio' (see Total Capital Ratio sheet), "
         "not separately-stated CET1/Tier 1/Total Capital ratios. Since Tier 2 capital (subordinated debt) is a "
         "material part of total regulatory capital in every year, a CET1-only ratio would differ measurably from "
         "the disclosed combined ratio — left blank rather than assume which capital measure the disclosed ratio "
         "uses.",
)

metric(
    "Tier 1 Capital", "£000's",
    [("Tier 1 capital (share capital, retained earnings, FVTOCI reserve, less intangible assets)",
      {"FY2025": 64528, "FY2024": 67015, "FY2023": 65916, "FY2022": 59465, "FY2021": 56254})],
    p3_sources(),
    note="No AT1 instruments in any year — Tier 1 = CET1.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {y: "Not separately disclosed" for y in YEARS})],
    p3_sources(),
    note="Same basis issue as the CET1 Ratio sheet — only a single combined 'Capital adequacy ratio' is disclosed.",
)

metric(
    "Total Capital", "£000's",
    [("Total regulatory capital (Tier 1 + Tier 2)",
      {"FY2025": 74528, "FY2024": 77015, "FY2023": 67916, "FY2022": 63465, "FY2021": 62254})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Capital adequacy ratio (as disclosed; source does not specify whether the numerator is Total Capital or "
      "Tier 1 only — treated as Total Capital ratio per standard Basel/PRA usage of this exact term)",
      {"FY2025": "20%", "FY2024": "23%", "FY2023": "25%"})],
    p3_sources(),
    note="Not disclosed at all for FY2021/FY2022 — the Annual Report's KPI table for those years lists only "
         "Profit before tax, Total equity, and Return on equity; the Capital adequacy/LCR/Leverage ratio KPI trio "
         "was introduced from the FY2023 report onward.",
)

metric(
    "Total RWAs", "£000's",
    [("Total risk-weighted assets (calculated: Total Capital ÷ Capital adequacy ratio, as reported)",
      {"FY2025": 372640, "FY2024": 334848, "FY2023": 271664})],
    p3_sources(),
    note="Not directly disclosed any year — calculated from the two most literal disclosed figures for the years "
         "the capital adequacy ratio exists (FY2023-FY2025). Not calculable for FY2021/FY2022 since no ratio is "
         "disclosed for those years either.",
)

bw.add_rwa_breakdown_sheet(
    title="Alpha Bank London Limited — RWA Breakdown",
    subtitle="Entity-level basis, FY2021-FY2025",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    unit_suffix="",
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio", {"FY2025": "11%", "FY2024": "13%", "FY2023": "13%"})],
    p3_sources(),
    note="Not disclosed for FY2021/FY2022 (same KPI-table introduction timing as the Total Capital Ratio sheet). "
         "No exposure-measure £ figure is disclosed alongside the ratio in any year.",
)

metric(
    "LCR", "%",
    [("Liquidity coverage ratio", {"FY2025": "310%", "FY2024": "323%", "FY2023": "349%"})],
    p3_sources(),
    note="Not disclosed for FY2021/FY2022 (same KPI-table introduction timing as the other ratio sheets).",
)

bw.add_not_disclosed_metric_sheets(
    ["NSFR", "MREL Ratio"],
    p3_sources(),
    per_note={
        "NSFR": "Not disclosed in any of the 5 years reviewed — no NSFR figure or qualitative statement found in "
                "any Annual Report, including the years the LCR/leverage/capital-adequacy KPI trio was introduced.",
        "MREL Ratio": "Not disclosed in any of the 5 years reviewed, and no explicit exemption statement found "
                      "either — plausibly reflects the Bank's small balance sheet size sitting below the threshold "
                      "requiring a stated MREL requirement, but this is not confirmed by the source.",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 547316, "FY2024": 485136, "FY2023": 453075, "FY2022": 463872, "FY2021": 530496}),
        ("Loans and advances to customers", {"FY2025": 454489, "FY2024": 397459, "FY2023": 330090, "FY2022": 325461, "FY2021": 357822}),
        ("Due to customers", {"FY2025": 454928, "FY2024": 397172, "FY2023": 370324, "FY2022": 380738, "FY2021": 424160}),
        ("Total equity", {"FY2025": 67549, "FY2024": 68382, "FY2023": 66003, "FY2022": 59534, "FY2021": 56370}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Operating income", {"FY2025": 21386, "FY2024": 22265, "FY2023": 21918, "FY2022": 16300, "FY2021": 13426}),
        ("Operating expenses", {"FY2025": -22455, "FY2024": -19109, "FY2023": -13822, "FY2022": -12396, "FY2021": -11666}),
        ("(Loss)/Profit after tax", {"FY2025": -820, "FY2024": 2355, "FY2023": 6320, "FY2022": 3367, "FY2021": 1504}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 68382, "FY2024": 66003, "FY2023": 59534, "FY2022": 56370, "FY2021": 54785}),
        ("Total comprehensive income for the year", {"FY2025": -833, "FY2024": 2379, "FY2023": 6469, "FY2022": 3164, "FY2021": 1585}),
        ("Closing equity", {"FY2025": 67549, "FY2024": 68382, "FY2023": 66003, "FY2022": 59534, "FY2021": 56370}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from operating activities", {"FY2025": 7196, "FY2024": -31370, "FY2023": -12026, "FY2022": -40650, "FY2021": -82764}),
        ("Net cash from investing activities", {"FY2025": 1325, "FY2024": 29199, "FY2023": 16148, "FY2022": -574, "FY2021": 66905}),
        ("Net cash from financing activities", {"FY2025": -1602, "FY2024": -1680, "FY2023": -1653, "FY2022": -1253, "FY2021": -1094}),
        ("Cash and cash equivalents at end of year", {"FY2025": 44211, "FY2024": 36967, "FY2023": 40658, "FY2022": 38160, "FY2021": 80857}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("Total Capital Ratio", {"FY2025": "20%", "FY2024": "23%", "FY2023": "25%"}),
        ("Leverage Ratio", {"FY2025": "11%", "FY2024": "13%", "FY2023": "13%"}),
        ("LCR", {"FY2025": "310%", "FY2024": "323%", "FY2023": "349%"}),
    ],
    note="CET1/Tier 1 ratios not shown here — only a single combined 'Capital adequacy ratio' is disclosed by this "
         "bank (see the Total Capital Ratio sheet's note). No ratios of any kind disclosed for FY2021/FY2022. "
         "Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page.",
)

bw.save("/Users/armaan/code/katalysis/banks/ALPHA BANK LONDON FINANCIALS.xlsx")
print("Saved ALPHA BANK LONDON FINANCIALS.xlsx")
