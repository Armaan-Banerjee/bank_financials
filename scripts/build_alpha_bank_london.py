import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019"]  # most recent first

CH_URL = "https://find-and-update.company-information.service.gov.uk/company/00185070/filing-history"
AR25_URL = "https://find-and-update.company-information.service.gov.uk/company/00185070/filing-history/MzUyMzkyMTM5MGFkaXF6a2N4/document?format=pdf&download=0"
AR24_URL = "https://find-and-update.company-information.service.gov.uk/company/00185070/filing-history/MzQ2NDAyMTQ4MGFkaXF6a2N4/document?format=pdf&download=0"
AR22_URL = "https://find-and-update.company-information.service.gov.uk/company/00185070/filing-history/MzM3OTU0ODM0NWFkaXF6a2N4/document?format=pdf&download=0"
AR20_URL = "https://www.alphabanklondon.co.uk/sites/default/files/2025-10/ABL-Financial-Statements-2020.pdf"
AR19_URL = "https://alphabanklondon.co.uk/wp-content/uploads/2020/05/ABL-Financial-Statements-2019-1.pdf"
# ADDED 2026-09-15: the FY2021 statements as a standalone primary source. Until now
# FY2021 was taken only from the FY2022 report's comparative column; this is the
# FY2021 report itself, and it is a full text-layer PDF, so Note 34.6 could be read
# by search rather than by eye. The bank's live Drupal host returns HTTP 403 to
# every non-browser request regardless of user-agent or header set, so this cites
# the Wayback capture, which serves the file intact.
AR21_URL = (
    "https://web.archive.org/web/20260118042750id_/https://www.alphabanklondon.co.uk/"
    "sites/default/files/2025-10/ABL%20Financial%20Statements%202021%20Final%20contents%20page%20fixed.pdf"
)

CASH_FLOW_SOURCES = (
    "Sources — Alpha Bank London Limited (FRN 135327, company 00185070) own Statement of Cash Flows, £000's:\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements 31 December 2025, p.25-26 (Statement of Cash Flows) — {AR25_URL}\n"
    f"FY2023 & FY2024 (cross-checked): Annual Report and Financial Statements 31 December 2024, p.26-27 (Statement of Cash Flows) — {AR24_URL}\n"
    f"FY2022 & FY2021: Annual Report and Financial Statements 31 December 2022, p.22-23 (Statement of Cash Flows) — {AR22_URL}\n"
    f"FY2020 & FY2019: Annual Report and Financial Statements 31 December 2020, p.23-24 (Statement of Cash Flows) — {AR20_URL}\n"
    "FY2019 is also the prior-year comparative in the FY2020 report. Figures are directly transcribed from the Bank's own searchable PDF archive; no Companies House copy is used for these two years.\n"
    "Filed accounts at Companies House are fully scanned/image-only for FY2021-FY2025 — figures "
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
    "are fully consistent and comparable across all 7 years — verified by hand line-by-line; see "
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
        f"FY2020 & FY2019: Annual Report 2020, p.67 Note 33.6 (Capital management, Regulatory analysis) — {AR20_URL}\n"
        f"FY2021 & FY2020 (standalone primary source, added 2026-09-15): Annual Report 2021, p.68 Note 34 "
        f"'Capital management — Regulatory analysis' — {AR21_URL}\n"
        f"Companies House filing history — {CH_URL}\n"
        "INDEPENDENT RE-VERIFICATION 2026-09-15: the FY2021 report was obtained as a text-layer PDF and its "
        "regulatory-capital note re-extracted from scratch, without reference to the figures already in this "
        "script. It prints, in £000's for 2021 and 2020: Share capital 30,000 / 30,000; Retained earnings "
        "26,318 / 24,814; FVTOCI reserve 52 / (29); Intangible assets (116) / -; Total Tier 1 capital 56,254 / "
        "54,785; Subordinated debt (excluding accrued interest) 6,000 / 8,000; Total Tier 2 capital 6,000 / "
        "8,000; Total Tier 1 and Tier 2 capital 62,254 / 62,785; Total regulatory capital 62,254 / 62,785. Both "
        "columns foot exactly and every figure matches what this script already carried for FY2021 and FY2020, "
        "so those years are now confirmed against the original report rather than resting on the following "
        "year's comparative alone. The note also confirms the Tier 1 build-up contains no AT1 instrument of any "
        "kind, which is the basis for treating CET1 and Tier 1 as equal throughout.\n"
        "MACHINE-VERIFIED ABSENCE OF AN RWA DENOMINATOR: a full-text search of the FY2021 report for "
        "'risk-weighted', 'RWA', 'capital requirement' and 'Pillar 1' returns only narrative — the sentence "
        "explaining that the PRA's Individual Capital Guidance 'is expressed as a percentage of total capital to "
        "total risk-weighted assets together with a capital planning buffer'. No RWA amount is printed. This "
        "matters because it independently closes the last route to a CRR ratio for these years: the Bank's own "
        "'Capital adequacy ratio' KPI (shareholders' funds ÷ RWA) does not appear in the FY2021 report at all, "
        "confirming that KPI was introduced only from the FY2023 report, and with no published RWA there is no "
        "denominator from which a CET1, Tier 1 or Total Capital ratio could be sourced. Deriving RWA by dividing "
        "shareholders' funds by that KPI would be back-solving and is barred by project convention.\n"
        "NO-PILLAR-3 EVIDENCE (established 2026-09-15; the claim above was previously asserted without a stated "
        "check): a Wayback Machine CDX scan of the whole alphabanklondon.co.uk domain, unfiltered by path and "
        "covering both generations of the site (the pre-2025 WordPress /wp-content/uploads/ tree and the current "
        "Drupal /sites/default/files/ tree), returns 39 distinct PDFs ever captured. Not one is a Pillar 3 "
        "disclosure: the set is 8 Annual Report editions (FY2018-FY2023), tariff and key-information sheets, FSCS "
        "leaflets, terms of business, a GDPR privacy notice and a fraud-warning client letter. So the absence is "
        "an evidenced absence rather than an unfound document. Note also that the Bank's own Note 34.7 "
        "'Regulatory analysis (unaudited)' was re-read in full this session and contains ONLY the capital "
        "build-up (Tier 1 components, Tier 2 subordinated debt, and the two totals) — it carries no "
        "risk-weighted-asset amount, no OV1-equivalent table and no capital ratio.\n"
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
    f"FY2020 & FY2019: Annual Report and Financial Statements 31 December 2020, p.21 — {AR20_URL}\n"
    "FY2019 is the FY2020 report's comparative. The Bank's own searchable archive PDF is used for both years. "
    "Companies House copies are used only for the FY2021-FY2025 OCR work — figures "
    "transcribed via pdf_tools.py render+visual read of each statement page, cross-checked against the adjacent "
    "year's comparative column where available. All figures GBP throughout.\n"
    f"{ENTITY_NOTE}\n"
    "PRESENTATION NOTE: 'Cash and cash equivalents' (FY2025) is labelled 'Cash and due from credit institutions' "
    "in FY2024-FY2019 - same line, relabelled; both are shown under this sheet's 'Cash and cash equivalents' "
    "label. All TOTAL rows (Total assets/Total liabilities/Total equity/Total liabilities and equity) tie out "
    "exactly for every year.\n"
    "INVESTMENT SECURITIES COMPOSITION: Note 18 'Investment securities' (rendered/read visually via "
    "pdf_tools.py, since the FY2025/FY2024/FY2022 Companies House filings are fully scanned/image-only) discloses "
    "the entire balance as a single line, 'Measured at FVTOCI', for every year reviewed - there is no further "
    "£-value split by measurement basis (100% FVTOCI/mark-to-market; no amortised-cost or FVTPL holdings in any "
    "year) or by issuer type. FY2025: Note 18, p.44 - " + AR25_URL + " (FY2025: £39,897k; FY2024 comparative: "
    "£42,230k). FY2023: Note 18, p.45 - " + AR24_URL + " (FY2024: £42,230k; FY2023 comparative: £78,097k). "
    "FY2022 & FY2021: Note 18, p.43 - " + AR22_URL + " (FY2022: £92,051k; FY2021 comparative: £85,647k). "
    "FY2020 & FY2019: Note 18, p.45 - " + AR20_URL + " (FY2020: £149,729k; FY2019 comparative: £174,633k). "
    "The line item's own label changes over time: FY2019-FY2020 it reads 'Multilateral development bank bonds' "
    "only (100% supranational); FY2021-FY2025 it reads 'Multilateral development bank bonds and sovereign debt' "
    "- the FY2022 report's Note 18 adds two qualitative (non-£-split) paragraphs stating the sovereign portion "
    "pays 0%-2.25% p.a. and matures Apr-Jun 2023, while the multilateral development bank portion pays "
    "3.7924%-5.1747% p.a. and matures 2023-2026, but does not give a £ amount for either sub-component in any "
    "year - so no reconciling sub-row split is possible; the single row is relabelled in place instead. The "
    "'sovereign debt' wording is not confirmed to mean UK gilts specifically (no country/currency is stated for "
    "it), so it is not classified as 'UK Government' in this workbook."
)

INCOME_STATEMENT_SOURCES = (
    "Sources — Alpha Bank London Limited's own Statement of Profit or Loss and Statement of Comprehensive "
    "Income, £000's:\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements 31 December 2025, p.22 — {AR25_URL}\n"
    f"FY2023 (cross-checked against FY2024 & FY2023 comparative): Annual Report and Financial Statements 31 "
    f"December 2024, p.23 — {AR24_URL}\n"
    f"FY2022 & FY2021: Annual Report and Financial Statements 31 December 2022, p.19 — {AR22_URL}\n"
    f"FY2020 & FY2019: Annual Report and Financial Statements 31 December 2020, p.20 — {AR20_URL}\n"
    "FY2019 is the FY2020 report's comparative. The Bank's own searchable archive PDF is used for both years. "
    "Companies House copies are used only for the FY2021-FY2025 OCR work — figures "
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
    "2019 to 31 December 2025):\n"
    f"FY2025 & FY2024 movements: Annual Report and Financial Statements 31 December 2025, p.24 — {AR25_URL}\n"
    f"FY2023 movements (cross-checked against FY2024 & FY2023 comparative): Annual Report and Financial "
    f"Statements 31 December 2024, p.25 — {AR24_URL}\n"
    f"FY2022 & FY2021 movements: Annual Report and Financial Statements 31 December 2022, p.21 — {AR22_URL}\n"
    f"FY2020 & FY2019 movements: Annual Report and Financial Statements 31 December 2020, p.22 — {AR20_URL}\n"
    "FY2019 is the FY2020 report's comparative. The Bank's own searchable archive PDF is used for both years. "
    "Companies House copies are used only for the FY2021-FY2025 OCR work — figures "
    "transcribed via pdf_tools.py render+visual read of each statement page.\n"
    f"{ENTITY_NOTE}\n"
    "Equity components are Share capital, Retained earnings, and a Fair value reserve (FVTOCI debt-instrument "
    "movements) - no other reserve types exist across the 7 years. All 'Balance as at' rows tie out exactly to "
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
    f"FY2020 & FY2019: Annual Report and Financial Statements 31 December 2020, p.45 — {AR20_URL}\n"
    f"FY2025 & FY2024 loss-allowance-by-IFRS-9-stage roll-forward (Loans and advances to customers): Annual "
    f"Report and Financial Statements 31 December 2025, p.57 — {AR25_URL}\n"
    "FY2019 is the FY2020 report's comparative. The Bank's own searchable archive PDF is used for both years. "
    "Companies House copies are used only for the FY2021-FY2025 OCR work — figures "
    "transcribed via pdf_tools.py render+visual read of each note page.\n"
    f"{ENTITY_NOTE}\n"
    "DISCLOSURE GRANULARITY NOTE: the by-product split (Retail = Mortgage + Consumer lending; Corporate lending) "
    "with gross carrying amount/ECL allowance/net carrying amount is disclosed for all 7 years. The £-value "
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
    ("DATA", "Cash and cash equivalents", {"FY2025": 44211, "FY2024": 36967, "FY2023": 40658, "FY2022": 38160, "FY2021": 80857, "FY2020": 97765, "FY2019": 106249}),
    ("DATA", "Derivative financial instruments", {"FY2025": 263, "FY2024": 2868, "FY2023": 345, "FY2022": 3261, "FY2020": 452, "FY2019": 213}),
    ("DATA", "Investment securities - Multilateral development bank & sovereign debt bonds, all at FVTOCI (mark-to-market)", {"FY2025": 39897, "FY2024": 42230, "FY2023": 78097, "FY2022": 92051, "FY2021": 85647, "FY2020": 149729, "FY2019": 174633}),
    ("DATA", "Loans and advances to customers", {"FY2025": 454489, "FY2024": 397459, "FY2023": 330090, "FY2022": 325461, "FY2021": 357822, "FY2020": 337615, "FY2019": 339047}),
    ("DATA", "Property and equipment", {"FY2025": 1020, "FY2024": 1987, "FY2023": 2861, "FY2022": 3804, "FY2021": 4787, "FY2020": 5743, "FY2019": 6596}),
    ("DATA", "Intangible assets", {"FY2025": 3021, "FY2024": 1367, "FY2023": 87, "FY2022": 69, "FY2021": 116, "FY2019": 15}),
    ("DATA", "Current tax assets", {"FY2025": 584, "FY2024": 402, "FY2023": 110, "FY2022": 14, "FY2021": 52}),
    ("DATA", "Deferred tax assets", {"FY2025": 611, "FY2023": 28, "FY2022": 50}),
    ("DATA", "Other assets", {"FY2025": 3220, "FY2024": 1856, "FY2023": 799, "FY2022": 1002, "FY2021": 1215, "FY2020": 1276, "FY2019": 1011}),
    ("TOTAL", "Total assets", {"FY2025": 547316, "FY2024": 485136, "FY2023": 453075, "FY2022": 463872, "FY2021": 530496, "FY2020": 592579, "FY2019": 627764}),

    ("SECTION", "Liabilities", {}),
    ("DATA", "Due to banks", {"FY2025": 7300, "FY2024": 1962, "FY2023": 201, "FY2022": 6388, "FY2021": 30194, "FY2020": 3065, "FY2019": 2408}),
    ("DATA", "Derivative financial instruments", {"FY2025": 793, "FY2024": 899, "FY2023": 1724, "FY2022": 1843, "FY2021": 2502, "FY2020": 1979, "FY2019": 3272}),
    ("DATA", "Due to customers", {"FY2025": 454928, "FY2024": 397172, "FY2023": 370324, "FY2022": 380738, "FY2021": 424160, "FY2020": 515898, "FY2019": 551341}),
    ("DATA", "Subordinated debt", {"FY2025": 10004, "FY2024": 10004, "FY2023": 10006, "FY2022": 10003, "FY2021": 10001, "FY2020": 10001, "FY2019": 10002}),
    ("DATA", "Deferred tax liabilities", {"FY2025": 616, "FY2024": 251, "FY2023": 16, "FY2022": 16, "FY2021": 64, "FY2020": 59, "FY2019": 81}),
    ("DATA", "Lease liabilities", {"FY2025": 1138, "FY2024": 1996, "FY2023": 2811, "FY2022": 3611, "FY2021": 4385, "FY2020": 5110, "FY2019": 5444}),
    ("DATA", "Provisions", {"FY2025": 1, "FY2023": 1, "FY2021": 6}),
    ("DATA", "Other liabilities", {"FY2025": 4987, "FY2024": 4470, "FY2023": 1989, "FY2022": 1739, "FY2021": 2814, "FY2020": 1611, "FY2019": 1340}),
    ("TOTAL", "Total liabilities", {"FY2025": 479767, "FY2024": 416754, "FY2023": 387072, "FY2022": 404338, "FY2021": 474126, "FY2020": 537794, "FY2019": 574313}),

    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 30000, "FY2024": 30000, "FY2023": 30000, "FY2022": 30000, "FY2021": 30000, "FY2020": 30000, "FY2019": 30000}),
    ("DATA", "Retained earnings", {"FY2025": 37540, "FY2024": 38360, "FY2023": 36005, "FY2022": 29685, "FY2021": 26318, "FY2020": 24814, "FY2019": 23510}),
    ("DATA", "Fair value reserve", {"FY2025": 9, "FY2024": 22, "FY2023": -2, "FY2022": -151, "FY2021": 52, "FY2020": -29, "FY2019": -59}),
    ("TOTAL", "Total equity", {"FY2025": 67549, "FY2024": 68382, "FY2023": 66003, "FY2022": 59534, "FY2021": 56370, "FY2020": 54785, "FY2019": 53451}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 547316, "FY2024": 485136, "FY2023": 453075, "FY2022": 463872, "FY2021": 530496, "FY2020": 592579, "FY2019": 627764}),
]

income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest and similar income", {"FY2025": 40745, "FY2024": 41240, "FY2023": 36264, "FY2022": 19333, "FY2021": 13080, "FY2020": 13062, "FY2019": 16827}),
    ("DATA", "Interest expense and similar charges", {"FY2025": -20860, "FY2024": -20382, "FY2023": -15359, "FY2022": -4329, "FY2021": -2107, "FY2020": -3073, "FY2019": -5048}),
    ("TOTAL", "Net interest income", {"FY2025": 19885, "FY2024": 20858, "FY2023": 20905, "FY2022": 15004, "FY2021": 10973, "FY2020": 9989, "FY2019": 11779}),
    ("DATA", "Fees and commission income", {"FY2025": 1162, "FY2024": 1284, "FY2023": 1126, "FY2022": 1557, "FY2021": 2446, "FY2020": 2250, "FY2019": 2108}),
    ("DATA", "Net trading income/(expense)", {"FY2025": 374, "FY2024": 60, "FY2023": -67, "FY2022": -340, "FY2021": -98, "FY2020": -21, "FY2019": 43}),
    ("DATA", "Other operating (expense)/income", {"FY2025": -35, "FY2024": 97, "FY2023": 36, "FY2022": 120, "FY2021": 143, "FY2020": 236, "FY2019": 171}),
    ("DATA", "Net loss from derecognition of financial assets measured at FVTOCI", {"FY2025": 0, "FY2024": -34, "FY2023": -82, "FY2022": -41, "FY2021": -38, "FY2020": 0, "FY2019": 54}),
    ("TOTAL", "Operating income", {"FY2025": 21386, "FY2024": 22265, "FY2023": 21918, "FY2022": 16300, "FY2021": 13426, "FY2020": 12454, "FY2019": 14155}),

    ("SECTION", "Operating expenses", {}),
    ("DATA", "Staff costs", {"FY2025": -11526, "FY2024": -9688, "FY2023": -8892, "FY2022": -7845, "FY2021": -7176, "FY2020": -6981, "FY2019": -6085}),
    ("DATA", "General administrative expenses", {"FY2025": -9699, "FY2024": -8415, "FY2023": -3886, "FY2022": -3512, "FY2021": -3462, "FY2020": -3118, "FY2019": -3952}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -1230, "FY2024": -1006, "FY2023": -1044, "FY2022": -1039, "FY2021": -1028, "FY2020": -866, "FY2019": -977}),
    ("TOTAL", "Operating expenses", {"FY2025": -22455, "FY2024": -19109, "FY2023": -13822, "FY2022": -12396, "FY2021": -11666, "FY2020": -10965, "FY2019": -11014}),

    ("DATA", "Reversal of impairment/(provision) for credit losses", {"FY2025": 3, "FY2024": 7, "FY2023": 171, "FY2022": 256, "FY2021": 108, "FY2020": -32, "FY2019": -8}),
    ("TOTAL", "(Loss)/Profit before tax", {"FY2025": -1066, "FY2024": 3163, "FY2023": 8267, "FY2022": 4160, "FY2021": 1868, "FY2020": 1457, "FY2019": 3133}),
    ("DATA", "Income tax (expense)/credit", {"FY2025": 246, "FY2024": -808, "FY2023": -1947, "FY2022": -793, "FY2021": -364, "FY2020": -153, "FY2019": -538}),
    ("TOTAL", "(Loss)/Profit after tax", {"FY2025": -820, "FY2024": 2355, "FY2023": 6320, "FY2022": 3367, "FY2021": 1504, "FY2020": 1304, "FY2019": 2595}),

    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Fair value movement of debt instruments at FVTOCI", {"FY2025": -1, "FY2024": -5, "FY2023": 70, "FY2022": -247, "FY2021": 56, "FY2020": 37, "FY2019": 274}),
    ("DATA", "Allowance for ECL movement of debt instruments at FVTOCI", {"FY2025": -12, "FY2024": -5, "FY2023": -3, "FY2022": 3, "FY2021": -13, "FY2020": -7, "FY2019": -3}),
    ("DATA", "Amounts reclassified to profit or loss for debt instruments measured at FVTOCI", {"FY2025": 0, "FY2024": 34, "FY2023": 82, "FY2022": 41, "FY2021": 38, "FY2020": 0, "FY2019": 54}),
    ("TOTAL", "Other comprehensive (expense)/income", {"FY2025": -13, "FY2024": 24, "FY2023": 149, "FY2022": -203, "FY2021": 81, "FY2020": 30, "FY2019": 325}),
    ("TOTAL", "Total comprehensive income for the year, net of tax", {"FY2025": -833, "FY2024": 2379, "FY2023": 6469, "FY2022": 3164, "FY2021": 1585, "FY2020": 1334, "FY2019": 2920}),
]

EQUITY_HEADERS = ["Share capital", "Retained earnings", "Fair value reserve", "Total equity"]
equity_changes_rows = [
    ("TOTAL", "Balance as at 1 January 2019", (30000, 20915, -384, 50531)),
    ("DATA", "Profit after tax", (None, 2595, None, 2595)),
    ("DATA", "Other comprehensive income for the year", (None, None, 325, 325)),
    ("TOTAL", "Total comprehensive income for the year", (None, 2595, 325, 2920)),
    ("TOTAL", "Balance attributable to the owner as at 31 December 2019", (30000, 23510, -59, 53451)),

    ("TOTAL", "Balance as at 1 January 2020", (30000, 23510, -59, 53451)),
    ("DATA", "Profit after tax", (None, 1304, None, 1304)),
    ("DATA", "Other comprehensive income for the year", (None, None, 30, 30)),
    ("TOTAL", "Total comprehensive income for the year", (None, 1304, 30, 1334)),
    ("TOTAL", "Balance attributable to the owner as at 31 December 2020", (30000, 24814, -29, 54785)),

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
    ("DATA", "Mortgage lending", {"FY2025": 21626, "FY2024": 22798, "FY2023": 24460, "FY2022": 24842, "FY2021": 28943, "FY2020": 23719, "FY2019": 21272}),
    ("DATA", "Consumer lending", {"FY2025": 13088, "FY2024": 11055, "FY2023": 5891, "FY2022": 5459, "FY2021": 6608, "FY2020": 6294, "FY2019": 7698}),
    ("TOTAL", "Retail lending (gross)", {"FY2025": 34714, "FY2024": 33853, "FY2023": 30351, "FY2022": 30301, "FY2021": 35551, "FY2020": 30013, "FY2019": 28970}),
    ("DATA", "Corporate lending (gross)", {"FY2025": 419778, "FY2024": 363615, "FY2023": 299749, "FY2022": 295339, "FY2021": 322703, "FY2020": 308160, "FY2019": 310573}),
    ("TOTAL", "Total lending (gross carrying amount)", {"FY2025": 454492, "FY2024": 397468, "FY2023": 330100, "FY2022": 325640, "FY2021": 358254, "FY2020": 338173, "FY2019": 339543}),

    ("SECTION", "ECL allowance by product", {}),
    ("DATA", "Retail lending ECL allowance", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": -385, "FY2020": -531, "FY2019": -479}),
    ("DATA", "Corporate lending ECL allowance", {"FY2025": -3, "FY2024": -9, "FY2023": -10, "FY2022": -179, "FY2021": -47, "FY2020": -27, "FY2019": -17}),
    ("TOTAL", "Total ECL allowance", {"FY2025": -3, "FY2024": -9, "FY2023": -10, "FY2022": -179, "FY2021": -432, "FY2020": -558, "FY2019": -496}),
    ("TOTAL", "Total lending (net carrying amount)", {"FY2025": 454489, "FY2024": 397459, "FY2023": 330090, "FY2022": 325461, "FY2021": 357822, "FY2020": 337615, "FY2019": 339047}),

    ("SECTION", "ECL allowance by IFRS 9 stage — Loans and advances to customers (closing balance; gross exposure by stage not separately disclosed)", {}),
    ("DATA", "Stage 1 (12-month ECL)", {"FY2025": -2, "FY2024": -9}),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {"FY2025": -1, "FY2024": 0}),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired)", {"FY2025": 0, "FY2024": 0}),
    ("TOTAL", "Total ECL allowance by stage", {"FY2025": -3, "FY2024": -9}),

    ("SECTION", "Derived ratios", {}),
    ("DATA", "ECL coverage ratio (Total ECL allowance ÷ Total gross lending)",
     {y: _cov_ratio(v, g) for y, v, g in [
         ("FY2025", 3, 454492), ("FY2024", 9, 397468), ("FY2023", 10, 330100),
         ("FY2022", 179, 325640), ("FY2021", 432, 358254), ("FY2020", 558, 338173),
         ("FY2019", 496, 339543),
     ]}),
]

RWA_BREAKDOWN_SOURCES = (
    "Sources — Alpha Bank London Limited's own Note 34.7 (Capital management, Regulatory analysis) and the "
    f"Annual Report's Key Performance Indicators table:\n{AR25_URL}\n{AR24_URL}\n{AR22_URL}\n{AR20_URL}\n"
    "NOT PUBLICLY DISCLOSED: as noted on the Total RWAs sheet, this bank does not publish a standalone Pillar 3 "
    "document or a UK OV1-style risk-weighted-exposure-by-category table in any of the 7 Annual Reports reviewed "
    "(confirmed by reading Note 34.7 in full, p.67 of the 2025 Annual Report and the equivalent pages of the "
    "2024/2022 Annual Reports — it discloses only the aggregate Tier 1/Tier 2/Total regulatory capital build-up, "
    "not a risk-category RWA split). Total RWAs (a single aggregate figure) is calculated on the Total RWAs "
    "sheet from Total Capital ÷ Capital adequacy ratio, per that sheet's own note; no further breakdown by "
    "credit/market/operational risk is available for any year.\n\n"
    "RE-VERIFIED 2026-09-12: independently re-downloaded and OCR'd the live FY2025 Annual Report "
    "(a scanned, no-text-layer PDF) directly from Companies House and re-read Note 34.7 in full "
    "(pp.66-67) - confirmed it still contains only the Tier 1/Tier 2 regulatory-capital build-up "
    "table shown above, with no risk-weighted-assets figure or category split anywhere on that page "
    "or the surrounding notes. No standalone Pillar 3 document was found on the bank's own site or "
    "in the Wayback Machine archive. The non-disclosure is confirmed current."
)
rwa_breakdown_rows = [
    ("DATA", "RWA category breakdown", {y: "Not publicly disclosed" for y in YEARS}),
]

bw.add_balance_sheet_sheet(
    title="Alpha Bank London Limited — Statement of Financial Position",
    subtitle="Entity-level basis, £000's, as at 31 December, FY2019-FY2025",
    rows=balance_sheet_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    unit_suffix=" (£'000)",
)

bw.add_income_statement_sheet(
    title="Alpha Bank London Limited — Statement of Profit or Loss and Other Comprehensive Income",
    subtitle="Entity-level basis, £000's, FY2019-FY2025",
    rows=income_statement_rows,
    sources_text=INCOME_STATEMENT_SOURCES,
    unit_suffix=" (£'000)",
)

bw.add_equity_changes_sheet(
    title="Alpha Bank London Limited — Statement of Changes in Equity",
    subtitle="Entity-level basis, £000's, chronological, 1 January 2019 - 31 December 2025",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQUITY_CHANGES_SOURCES,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "(Loss)/profit before tax", {"FY2025": -1066, "FY2024": 3163, "FY2023": 8267, "FY2022": 4160, "FY2021": 1868, "FY2020": 1457, "FY2019": 3133}),
    ("DATA", "Interest income on investment securities", {"FY2025": -1367, "FY2024": -2894, "FY2023": -4042, "FY2022": -630, "FY2021": 248, "FY2020": -648, "FY2019": -1945}),
    ("DATA", "Interest income on loans and advances to customers (accrued)", {"FY2024": -29603, "FY2023": -25319, "FY2022": -16874, "FY2021": -12771, "FY2020": -12955, "FY2019": -13967}),
    ("DATA", "Interest expense on due to banks (accrued)", {"FY2024": 0, "FY2023": 624, "FY2022": 2316, "FY2021": 1484, "FY2020": 1887, "FY2019": 2750}),
    ("DATA", "Interest expense on due to customers (accrued)", {"FY2024": 7547, "FY2023": 7383, "FY2022": 355, "FY2021": 144, "FY2020": 1122, "FY2019": 2009}),
    ("DATA", "Interest expense on debt securities in issue and other borrowed funds", {"FY2025": 690, "FY2024": 726, "FY2023": 669, "FY2022": 340, "FY2021": 207, "FY2020": 240, "FY2019": 283}),
    ("DATA", "Interest expense on lease liabilities", {"FY2025": 54, "FY2024": 139, "FY2023": 185, "FY2022": 138, "FY2021": 161, "FY2020": 149, "FY2019": 131}),
    ("DATA", "Gain/(loss) on forward revaluation of FX transactions", {"FY2025": -374, "FY2024": -60, "FY2023": 67, "FY2022": 340, "FY2021": 98, "FY2020": 21, "FY2019": -42}),
    ("DATA", "Gain on foreign exchange", {"FY2025": 49, "FY2024": -100, "FY2023": -96, "FY2022": -120, "FY2021": -143, "FY2020": -167, "FY2019": -161}),
    ("DATA", "(Loss)/gain from derecognition of investment securities", {"FY2025": -1, "FY2024": 28, "FY2023": 152, "FY2022": -206, "FY2021": 94, "FY2020": 0, "FY2019": -54}),
    ("DATA", "Movement in ECL allowance on investment securities", {"FY2025": 0, "FY2024": -5, "FY2023": -3, "FY2022": 3, "FY2021": -13, "FY2020": -7, "FY2019": -3}),
    ("DATA", "Movement in ECL allowance on loans and advances to customers", {"FY2025": 2, "FY2024": -1, "FY2023": -168, "FY2022": -254, "FY2021": -92, "FY2020": 32, "FY2019": 11}),
    ("DATA", "Movement in ECL allowance on undrawn commitments", {"FY2025": 1, "FY2024": -1}),
    ("DATA", "Depreciation and amortisation", {"FY2025": 1230, "FY2024": 992, "FY2023": 1044, "FY2022": 1039, "FY2021": 1028, "FY2020": 1009, "FY2019": 1150}),
    ("DATA", "Provision", {"FY2023": 1, "FY2022": 0, "FY2021": 6, "FY2020": 109, "FY2019": 0}),
    ("TOTAL", "Cash flows before changes in operating assets/liabilities (as reported; not broken out FY2025)", {"FY2024": -20069, "FY2023": -11236, "FY2022": -9393, "FY2021": -7681, "FY2020": -7751, "FY2019": -6705}),

    ("SECTION", "Net increase/(decrease) in assets relating to operating activities", {}),
    ("DATA", "Derivative financial instruments", {"FY2025": 2605, "FY2024": -2523, "FY2023": 2916, "FY2022": -3261, "FY2021": 452, "FY2020": -239, "FY2019": 1141}),
    ("DATA", "Investment securities", {"FY2025": 447, "FY2024": 8164, "FY2023": 1729, "FY2022": -5211, "FY2021": -3265, "FY2020": -1748, "FY2019": 12240}),
    ("DATA", "Loans and advances to customers", {"FY2025": -57033, "FY2024": -67368, "FY2023": -4461, "FY2022": 32615, "FY2021": -20115, "FY2020": 1433, "FY2019": -49640}),
    ("DATA", "Right-of-use assets", {"FY2019": -4892}),
    ("DATA", "Other assets", {"FY2025": -1364, "FY2024": -1057, "FY2023": 203, "FY2022": 213, "FY2021": 61, "FY2020": -266, "FY2019": 38}),
    ("TOTAL", "Total change in operating assets", {"FY2025": -55345, "FY2024": -62784, "FY2023": 387, "FY2022": 24356, "FY2021": -22867, "FY2020": -821, "FY2019": -41113}),

    ("SECTION", "Net increase/(decrease) in liabilities relating to operating activities", {}),
    ("DATA", "Derivative financial instruments", {"FY2025": -106, "FY2024": -825, "FY2023": -119, "FY2022": -659, "FY2021": 523, "FY2020": -1293, "FY2019": 3150}),
    ("DATA", "Due to banks", {"FY2025": 5337, "FY2024": 1761, "FY2023": -6187, "FY2022": -23806, "FY2021": 27128, "FY2020": 657, "FY2019": -1426}),
    ("DATA", "Due to customers", {"FY2025": 57757, "FY2024": 26848, "FY2023": -10414, "FY2022": -43423, "FY2021": -91738, "FY2020": -35443, "FY2019": -226829}),
    ("DATA", "Other borrowed funds", {"FY2025": 0, "FY2024": -2, "FY2023": 3, "FY2022": 2, "FY2021": 1, "FY2020": -1, "FY2019": -1}),
    ("DATA", "Lease liabilities", {"FY2019": 5831}),
    ("DATA", "Other liabilities", {"FY2025": 517, "FY2024": 2481, "FY2023": 250, "FY2022": -1075, "FY2021": 1209, "FY2020": 160, "FY2019": -640}),
    ("TOTAL", "Total change in operating liabilities", {"FY2025": 63505, "FY2024": 30263, "FY2023": -16467, "FY2022": -68961, "FY2021": -62877, "FY2020": -35920, "FY2019": -219915}),

    ("SECTION", "Cash interest received/(paid) reconciliation (as reported; not broken out FY2025)", {}),
    ("DATA", "Interest income on loans and advances to customers (cash received)", {"FY2024": 29603, "FY2023": 25319, "FY2022": 16874, "FY2021": 12771, "FY2020": 12955, "FY2019": 13967}),
    ("DATA", "Interest expense on due to banks (cash paid)", {"FY2024": 0, "FY2023": -624, "FY2022": -2316, "FY2021": -1484, "FY2020": -1887, "FY2019": -2750}),
    ("DATA", "Interest expense on due to customers (cash paid)", {"FY2024": -7547, "FY2023": -7383, "FY2022": -355, "FY2021": -144, "FY2020": -1122, "FY2019": -2009}),
    ("TOTAL", "Total cash interest reconciliation", {"FY2024": 22056, "FY2023": 17312, "FY2022": 14203, "FY2021": 11143, "FY2020": 9946, "FY2019": 9208}),

    ("DATA", "Income tax paid", {"FY2025": -182, "FY2024": -836, "FY2023": -2022, "FY2022": -805, "FY2021": -482, "FY2020": -528, "FY2019": -540}),
    ("TOTAL", "Net cash flows used in operating activities", {"FY2025": 7196, "FY2024": -31370, "FY2023": -12026, "FY2022": -40650, "FY2021": -82764, "FY2020": -35072, "FY2019": -259065}),

    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Acquisition of investment securities", {"FY2025": -102879, "FY2024": -32554, "FY2023": -44562, "FY2022": -97105, "FY2021": -62157, "FY2020": -21746, "FY2019": -16260}),
    ("DATA", "Disposal/maturity of investment securities", {"FY2025": 104753, "FY2024": 60257, "FY2023": 56786, "FY2022": 95910, "FY2021": 129499, "FY2020": 48405, "FY2019": 236957}),
    ("DATA", "Interest income/(expense) on investment securities", {"FY2025": 1367, "FY2024": 2894, "FY2023": 4042, "FY2022": 630, "FY2021": -248, "FY2020": 648, "FY2019": 1945}),
    ("DATA", "Acquisition of fixed assets (including intangibles)", {"FY2025": -1916, "FY2024": -1398, "FY2023": -119, "FY2022": -9, "FY2021": -189, "FY2020": -141, "FY2019": -72}),
    ("DATA", "Proceeds from disposal of fixed assets", {"FY2019": 1}),
    ("TOTAL", "Net cash flows from investing activities", {"FY2025": 1325, "FY2024": 29199, "FY2023": 16148, "FY2022": -574, "FY2021": 66905, "FY2020": 27166, "FY2019": 222571}),

    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Repayment of lease liabilities", {"FY2025": -858, "FY2024": -815, "FY2023": -800, "FY2022": -775, "FY2021": -725, "FY2020": -334, "FY2019": -387}),
    ("DATA", "Interest paid on other borrowed funds", {"FY2025": -690, "FY2024": -726, "FY2023": -668, "FY2022": -340, "FY2021": -207, "FY2020": -240, "FY2019": -283}),
    ("DATA", "Interest paid on lease liabilities", {"FY2025": -54, "FY2024": -139, "FY2023": -185, "FY2022": -138, "FY2021": -162, "FY2020": -149, "FY2019": -131}),
    ("TOTAL", "Net cash flows used in financing activities", {"FY2025": -1602, "FY2024": -1680, "FY2023": -1653, "FY2022": -1253, "FY2021": -1094, "FY2020": -723, "FY2019": -801}),

    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 6919, "FY2024": -3851, "FY2023": 2469, "FY2022": -42477, "FY2021": -16953, "FY2020": -8629, "FY2019": -37295}),
    ("DATA", "Cash and cash equivalents at beginning of the year", {"FY2025": 36967, "FY2024": 40658, "FY2023": 38160, "FY2022": 80857, "FY2021": 97765, "FY2020": 106249, "FY2019": 143364}),
    ("DATA", "Net effect of foreign exchange fluctuations", {"FY2025": 325, "FY2024": 160, "FY2023": 29, "FY2022": -220, "FY2021": 45, "FY2020": 145, "FY2019": 180}),
    ("TOTAL", "Cash and cash equivalents at end of the year", {"FY2025": 44211, "FY2024": 36967, "FY2023": 40658, "FY2022": 38160, "FY2021": 80857, "FY2020": 97765, "FY2019": 106249}),
]

bw.add_cash_flow_sheet(
    title="Alpha Bank London Limited — Cash Flow Statement",
    subtitle="Entity-level basis, £000's, FY2019-FY2025",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    unit_suffix=" (£'000)",
)

bw.add_asset_quality_sheet(
    title="Alpha Bank London Limited — Asset Quality / Credit Risk Disclosures",
    subtitle="Entity-level basis, £000's, FY2019-FY2025",
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
      {"FY2025": 64528, "FY2024": 67015, "FY2023": 65916, "FY2022": 59465, "FY2021": 56254, "FY2020": 54785, "FY2019": 53436})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("CET1 ratio", {y: "Not separately disclosed" for y in YEARS})],
    p3_sources(),
    note="The source discloses only a single 'Capital adequacy ratio' (see Total Capital Ratio sheet), not "
         "separately-stated CET1/Tier 1/Total Capital ratios, and as of 2026-09-15 that ratio is known NOT to be a "
         "CRR capital ratio at all: the Annual Report defines its numerator as the Bank's shareholders' funds, "
         "i.e. Total equity before the intangible-assets deduction and excluding the £10,000k of Tier 2 "
         "subordinated debt. It therefore cannot be reused as a CET1 ratio. A true CET1 ratio is not computable "
         "either, since the Bank discloses no RWA denominator in any year (see the Total RWAs sheet) — left blank "
         "rather than estimated.",
)

metric(
    "Tier 1 Capital", "£000's",
    [("Tier 1 capital (share capital, retained earnings, FVTOCI reserve, less intangible assets)",
      {"FY2025": 64528, "FY2024": 67015, "FY2023": 65916, "FY2022": 59465, "FY2021": 56254, "FY2020": 54785, "FY2019": 53436})],
    p3_sources(),
    note="No AT1 instruments in any year — Tier 1 = CET1.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {y: "Not separately disclosed" for y in YEARS})],
    p3_sources(),
    note="Same basis issue as the CET1 Ratio sheet — the only ratio disclosed is the Bank's own 'Capital adequacy "
         "ratio', whose numerator is shareholders' funds rather than any CRR capital measure, and no RWA "
         "denominator is disclosed in any year from which a Tier 1 ratio could be computed.",
)

metric(
    "Total Capital", "£000's",
    [("Total regulatory capital (Tier 1 + Tier 2)",
      {"FY2025": 74528, "FY2024": 77015, "FY2023": 67916, "FY2022": 63465, "FY2021": 62254, "FY2020": 62785, "FY2019": 63436})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Memo: Bank's own 'Capital adequacy ratio' = shareholders' funds ÷ RWA (NOT a CRR total capital ratio)",
      {"FY2025": "20%", "FY2024": "23%", "FY2023": "25%"})],
    p3_sources(),
    note="BASIS CORRECTED 2026-09-15. This row was previously labelled as the Total Capital ratio on the stated "
         "grounds that the 'source does not specify whether the numerator is Total Capital or Tier 1 only'. The "
         "source does specify: 'Capital adequacy ratio is a measure of capital strength and calculated by dividing "
         "the Bank's shareholders funds by its risk weighted assets' (FY2025 Annual Report p.6; the FY2024 report "
         "uses the identical sentence). Shareholders' funds is Total equity — share capital + retained earnings + "
         "FVTOCI reserve — which is neither the CRR Total Capital measure (it excludes the £10,000k Tier 2 "
         "subordinated debt) nor CET1 (it is struck before the intangible-assets deduction: £3,021k at FY2025). "
         "The figure is genuine and correctly sourced, so it is kept, but as an explicitly-labelled memo row on "
         "the Bank's own definition rather than as a CRR total capital ratio. The true CRR ratio is not "
         "derivable, because no RWA denominator is disclosed — see the Total RWAs sheet. Not disclosed at all for "
         "FY2019-FY2022: the Annual Report KPI table for those years lists only Profit before tax, Total equity "
         "and Return on equity; the Capital adequacy/LCR/Leverage ratio KPI trio was introduced from the FY2023 "
         "report onward.",
)

metric(
    "Total RWAs", "£000's",
    [("Total risk-weighted assets", {y: "Not publicly disclosed" for y in YEARS})],
    p3_sources(),
    note="CORRECTED 2026-09-15 — this sheet previously carried £372,640k/£334,848k/£271,664k for "
         "FY2025/FY2024/FY2023, back-solved as Total regulatory capital ÷ Capital adequacy ratio. Those figures "
         "have been withdrawn: no risk-weighted asset amount is disclosed by this Bank in any year, and the "
         "back-solve was unsound on two independent grounds. (1) WRONG NUMERATOR: the Annual Report defines the "
         "ratio explicitly — 'Capital adequacy ratio is a measure of capital strength and calculated by dividing "
         "the Bank's shareholders funds by its risk weighted assets' (FY2025 Annual Report p.6, identical wording "
         "in the FY2024 report) — so the numerator is shareholders' funds/Total equity (£67,549k FY2025, £68,382k "
         "FY2024, £66,003k FY2023), NOT the Note 34.7 Total regulatory capital of £74,528k/£77,015k/£67,916k that "
         "the old calculation divided. The old figures therefore overstated RWA by roughly 10% even on their own "
         "logic. (2) INSUFFICIENT PRECISION: the ratio is published to two significant figures ('20%', '23%', "
         "'25%'), so even with the correct numerator the implied FY2025 RWA spans roughly £329.5m-£346.4m — a "
         "±2.5% band that cannot honestly be presented as a disclosed figure. This also aligns the sheet with the "
         "treatment applied elsewhere in this project (Ghana International, Weatherbys, SBI (UK), Nomura, Havin), "
         "where back-solved RWAs are refused rather than published.",
)

bw.add_rwa_breakdown_sheet(
    title="Alpha Bank London Limited — RWA Breakdown",
    subtitle="Entity-level basis, FY2019-FY2025",
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
        ("Total assets", {"FY2025": 547316, "FY2024": 485136, "FY2023": 453075, "FY2022": 463872, "FY2021": 530496, "FY2020": 592579, "FY2019": 627764}),
        ("Loans and advances to customers", {"FY2025": 454489, "FY2024": 397459, "FY2023": 330090, "FY2022": 325461, "FY2021": 357822, "FY2020": 337615, "FY2019": 339047}),
        ("Due to customers", {"FY2025": 454928, "FY2024": 397172, "FY2023": 370324, "FY2022": 380738, "FY2021": 424160, "FY2020": 515898, "FY2019": 551341}),
        ("Total equity", {"FY2025": 67549, "FY2024": 68382, "FY2023": 66003, "FY2022": 59534, "FY2021": 56370, "FY2020": 54785, "FY2019": 53451}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Operating income", {"FY2025": 21386, "FY2024": 22265, "FY2023": 21918, "FY2022": 16300, "FY2021": 13426, "FY2020": 12454, "FY2019": 14155}),
        ("Operating expenses", {"FY2025": -22455, "FY2024": -19109, "FY2023": -13822, "FY2022": -12396, "FY2021": -11666, "FY2020": -10965, "FY2019": -11014}),
        ("(Loss)/Profit after tax", {"FY2025": -820, "FY2024": 2355, "FY2023": 6320, "FY2022": 3367, "FY2021": 1504, "FY2020": 1304, "FY2019": 2595}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 68382, "FY2024": 66003, "FY2023": 59534, "FY2022": 56370, "FY2021": 54785, "FY2020": 53451, "FY2019": 50531}),
        ("Total comprehensive income for the year", {"FY2025": -833, "FY2024": 2379, "FY2023": 6469, "FY2022": 3164, "FY2021": 1585, "FY2020": 1334, "FY2019": 2920}),
        ("Closing equity", {"FY2025": 67549, "FY2024": 68382, "FY2023": 66003, "FY2022": 59534, "FY2021": 56370, "FY2020": 54785, "FY2019": 53451}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from operating activities", {"FY2025": 7196, "FY2024": -31370, "FY2023": -12026, "FY2022": -40650, "FY2021": -82764, "FY2020": -35072, "FY2019": -259065}),
        ("Net cash from investing activities", {"FY2025": 1325, "FY2024": 29199, "FY2023": 16148, "FY2022": -574, "FY2021": 66905, "FY2020": 27166, "FY2019": 222571}),
        ("Net cash from financing activities", {"FY2025": -1602, "FY2024": -1680, "FY2023": -1653, "FY2022": -1253, "FY2021": -1094, "FY2020": -723, "FY2019": -801}),
        ("Cash and cash equivalents at end of year", {"FY2025": 44211, "FY2024": 36967, "FY2023": 40658, "FY2022": 38160, "FY2021": 80857, "FY2020": 97765, "FY2019": 106249}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("Capital adequacy ratio (Bank's own definition — not a CRR ratio)",
         {"FY2025": "20%", "FY2024": "23%", "FY2023": "25%"}),
        ("Leverage Ratio", {"FY2025": "11%", "FY2024": "13%", "FY2023": "13%"}),
        ("LCR", {"FY2025": "310%", "FY2024": "323%", "FY2023": "349%"}),
    ],
    note="No CRR capital ratio (CET1, Tier 1 or Total Capital) is disclosed by this bank in any year. The single "
         "ratio shown above is the Bank's own 'Capital adequacy ratio', which the Annual Report defines as "
         "shareholders' funds divided by risk-weighted assets — a numerator that excludes the £10,000k Tier 2 "
         "subordinated debt and is struck before the intangible-assets deduction, so it is neither a Total Capital "
         "nor a CET1 ratio; see the Total Capital Ratio sheet's note. No ratios of any kind are disclosed for "
         "FY2019-FY2022, and no RWA amount is disclosed in any year. Figures are duplicated from the detail sheets "
         "for at-a-glance trend viewing; see each sheet's own source citation for the underlying document/page.",
)

bw.save("/Users/armaan/code/katalysis/banks/ALPHA BANK LONDON FINANCIALS.xlsx")
print("Saved ALPHA BANK LONDON FINANCIALS.xlsx")
