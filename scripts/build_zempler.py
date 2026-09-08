import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Zempler Bank Limited's first Pillar 3 report covered FY2022 (it only received
# its full banking licence in 2021), so the 5-year window here is FY2022-FY2026
# (year end 31 March each year) rather than the usual FY2021-FY2025 - there is
# no FY2021 Pillar 3 disclosure to pair with a cash flow column.
YEARS = ["FY2026", "FY2025", "FY2024", "FY2023", "FY2022"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2026_URL = "https://www.zemplerbank.com/media/yqkhclip/annual-report-2026-final.pdf"
AR2025_URL = "https://www.zemplerbank.com/media/5qxdezfu/annual-report-2025-final.pdf"
AR2023_URL = "https://www.zemplerbank.com/media/x5sbu2bc/annual-report-2023-010923.pdf"

P3_2026_URL = "https://www.zemplerbank.com/media/hfllow3d/pillar-3-fy2025-26-final.pdf"
P3_2024_URL = "https://www.zemplerbank.com/media/mszljzed/pillar-3-fy2023-24.pdf"
P3_2023_URL = "https://www.zemplerbank.com/media/f3vjwqov/pillar-3-fy2022-23.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Zempler Bank Limited (FRN 671140, company number 04947027) is a UK-domestic challenger bank - "
    "not a foreign subsidiary, so there was no reason to expect (and none was found) the FRS 101/102 cash-flow-"
    "statement exemption that blocked ICICI/PNBE/Citibank UK/State Bank of India UK. The company traded as "
    "'Cashplus Bank' under the legal name 'Advanced Payment Solutions Limited' through the FY2023 annual report; "
    "it was renamed 'Zempler Bank Limited' in July 2024 (FY2024/FY2025/FY2026 reports use the new name). Same "
    "company number throughout - this is a rename, not a different entity. FY2023's own annual report also notes "
    "that 'the Group no longer exists as at 31 March 2023' (a prior group restructuring), so the cash flow "
    "statement is presented on a Company-only basis for FY2023 and its FY2022 comparative, which this workbook "
    "uses for both years - there is no consolidated/Group-basis alternative available for FY2022-FY2023."
)

DATA_QUALITY_NOTE = (
    "DATA QUALITY NOTE - two apparent arithmetic errors were found in Zempler's own published, audited annual "
    "reports and are flagged here rather than silently smoothed over: "
    "(1) FY2025's own operating-activities line items (as printed) sum to £75,870k, not the £75,570k the source "
    "states as 'Net cash flow generated from operating activities' - a £300k gap in one of the individual "
    "components. The £75,570k TOTAL is used here (not the £75,870k component sum) because it is independently "
    "corroborated: operating + investing + financing (75,570 - 92,016 - 491) ties exactly to the source's own "
    "stated 'Net (decrease)/increase in cash and cash equivalent' of -£16,937k. The individual FY2025 operating "
    f"line items are transcribed exactly as printed in the source ({AR2025_URL}, p.64-66) despite this discrepancy. "
    "(2) FY2026's financing activities: the source prints 'Proceeds from issue of ordinary shares' £1,232k and "
    "'Interest paid' (£492k), which sum to +£740k, but the source's own 'Net cash used in financing activities' "
    "subtotal is printed as (£740k) - the opposite sign. +£740k is used here (not the printed -£740k) because it "
    "is the only figure consistent with both its own two components (1,232-492=740) and the overall cash bridge "
    f"(80,642 operating - 53,638 investing + 740 = 27,744, matching the source's own stated net increase in cash "
    f"exactly) - {AR2026_URL}, p.65-67."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Zempler Bank Limited's own (Company-only) cash flow statement, £'000:\n"
    f"FY2026: Zempler Bank Annual Report 2026, p.65-67 (Cash Flow Statement) - {AR2026_URL}\n"
    f"FY2025: Zempler Bank Annual Report 2025, p.64-66 (Cash Flow Statement) - {AR2025_URL}\n"
    f"FY2024 (restated): Zempler Bank Annual Report 2025, p.64-66 (Cash Flow Statement, restated comparative "
    f"column) - {AR2025_URL} - the restatement (see Note 38 in that report) reclassified some operating-section "
    "line items but did NOT change the operating/investing/financing TOTALS, which are identical to the "
    "originally-reported FY2024 figures.\n"
    f"FY2023: Annual Report and Financial Statements (Cashplus Bank / Advanced Payment Solutions Limited) for the "
    f"year ended 31 March 2023, p.56 (Cash Flow Statement) - {AR2023_URL}\n"
    f"FY2022 (restated to Company-only basis): Annual Report and Financial Statements for the year ended 31 March "
    f"2023, p.56 (Cash Flow Statement, comparative column) - {AR2023_URL}\n"
    "Blank cells indicate that year's report did not disclose that specific line item (e.g. prepayments/accrued "
    "income was only split out from FY2024 onward; tangible and intangible asset purchases were combined through "
    "FY2023 and split from FY2024). Section totals and cash/cash equivalents figures chain exactly year-to-year "
    "(each year's closing balance equals the next year's opening balance) across all 5 years.\n\n"
    + ENTITY_NOTE + "\n\n" + DATA_QUALITY_NOTE
)


P3_SOURCE_LINES = {
    "FY2026": f"FY2026: Zempler Bank Pillar 3 Disclosures for the year ended 31 March 2026, p.53-54 - {P3_2026_URL}",
    "FY2025": f"FY2025: Zempler Bank Pillar 3 Disclosures for the year ended 31 March 2026 (FY2025 comparative column), p.53-54 - {P3_2026_URL}",
    "FY2024": f"FY2024: Zempler Bank Pillar 3 Disclosures for the year ended 31 March 2024, p.51-52 - {P3_2024_URL}",
    "FY2023": f"FY2023: Pillar 3 Disclosures for the year ended 31 March 2023 (Cashplus Bank), p.40 - {P3_2023_URL}",
    "FY2022": f"FY2022: Pillar 3 Disclosures for the year ended 31 March 2023 (Cashplus Bank, FY2022 comparative column), p.40 - {P3_2023_URL}",
}

P3_SOURCES = (
    "Sources - Zempler Bank Limited's own entity-level Table 14: Key Metrics (KM1), £'000:\n"
    + "\n".join(P3_SOURCE_LINES[y] for y in YEARS)
)

bw = BankWorkbook(bank_name="Zempler Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="8A5A00")

STATEMENTS_SOURCES = (
    "Sources - Zempler Bank Limited's own (Company-only) statements, £'000:\n"
    f"FY2026: Zempler Bank Annual Report 2026, p.60-63 (Statement of Comprehensive Income / Statement of Financial "
    f"Position) - {AR2026_URL}\n"
    f"FY2025: Zempler Bank Annual Report 2026, p.60-63 (FY2025 comparative column) - {AR2026_URL} (matches AR2025's "
    f"own FY2025 column exactly)\n"
    f"FY2024 (restated): Zempler Bank Annual Report 2025, p.59-62 (restated comparative column) - {AR2025_URL} - "
    "the FY2025 report's own Note 38 (prior year restatement) reclassified some Balance Sheet line items (moving "
    "£1,841k from Other assets to a reduction in Customer deposits, and splitting Prepayments/Accrued income and "
    "Deferred income out of Other assets/Other liabilities) and some P&L line items (moving £2,520k/£113k between "
    "Fee income, Other income and Administrative expenses) - Profit for the year, Total comprehensive income, and "
    "Net assets/Total equity are IDENTICAL under both the originally-reported and restated FY2024 figures, so this "
    "restatement does not affect either bottom line. FY2024's own originally-published Annual Report (published "
    "before the July 2024 rename) was not separately located this session - the restated comparative is used "
    "throughout for consistency with the pre-existing Cash Flow Statement sheet, which already uses this same "
    "convention for FY2024 (see that sheet's own source note). Note: the restated Balance Sheet's own 'Other "
    "liabilities'/'Accruals and deferred income' split as printed in the primary statement (£37,321k/£5,796k) does "
    "not exactly match the figures implied by Note 38's own reconciliation table (£36,701k/£5,796k) - a small "
    "(~£620k) internal inconsistency in the source document itself; the primary statement's own printed figures "
    "are used here, not the reconciliation note's.\n"
    f"FY2023: Annual Report and Financial Statements (Cashplus Bank / Advanced Payment Solutions Limited) for the "
    f"year ended 31 March 2023, p.53-56 (Statement of Comprehensive Income / Statement of Financial Position / "
    f"Statement of Changes in Equity) - {AR2023_URL}\n"
    f"FY2022 (restated to Company-only basis): same document, p.53-56 (comparative column) - {AR2023_URL}\n"
    "Presentation note: FY2024-FY2026 use a 'Total operating income / Net operating income' P&L structure "
    "(splitting Interest and Fee income/expense into separate net subtotals); FY2022-FY2023 use the same structure "
    "but without a 'Loss on derivatives' line (introduced FY2024). The Balance Sheet's asset-side structure also "
    "changed: FY2022-FY2023 combine several lines into 'Other assets' (Deferred tax, Prepayments and accrued "
    "income, Derivative financial assets) that are shown separately from FY2024 onward - blank cells for those "
    "specific lines reflect items not separately disclosed that year, not zero balances. 'Tangible fixed assets / "
    "Property, plant and equipment' is its own distinct line in the FY2023 Annual Report's own Statement of "
    "Financial Position for both FY2023 (£3,528k) and its FY2022 comparative (£4,141k restated) - not combined "
    "into Other assets - and both years' Total assets figures already include it. "
    "All TOTAL rows (Total assets/liabilities/equity, Profit before/after taxation, Total comprehensive income) tie "
    "exactly across Balance Sheet <-> Equity Statement <-> P&L for every year, including a zero-plug-row equity "
    "roll-forward chaining from the 31 March 2021 opening balance through to 31 March 2026.\n"
    "'Total investment securities' is broken down into Treasury bills / UK government issued gilts / SSA "
    "(Sovereign, Supranational, Agency) bonds / Unamortised interest and discount, per each annual report's own "
    "'Investment securities' note (continued) table: Note 10 (p.91) of the FY2026 Annual Report for FY2026/FY2025 "
    f"({AR2026_URL}); Note 10 (p.91) of the FY2025 Annual Report for FY2024 ({AR2025_URL}); Note 11 of the FY2023 "
    f"Annual Report for FY2023/FY2022 ({AR2023_URL}). Each annual report's note also states 'All investment "
    "securities are held at amortised cost' for every year shown - there is no FVOCI/FVTPL/mark-to-market leg to "
    "this book across FY2022-FY2026. The SSA Bonds category was first disclosed in FY2025 (nil in FY2022-FY2024); "
    "Treasury bills were nil in FY2022. Sub-rows sum exactly to 'Total investment securities' each year.\n\n"
    + ENTITY_NOTE
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at banks", {"FY2026": 396832, "FY2025": 369088, "FY2024": 386025, "FY2023": 380533, "FY2022": 325327}),
    ("DATA", "Total investment securities", {"FY2026": 332687, "FY2025": 266859, "FY2024": 167073, "FY2023": 129949, "FY2022": 125196}),
    ("DATA", "Treasury bills - investment securities at amortised cost", {"FY2026": 60000, "FY2025": 69368, "FY2024": 75354, "FY2023": 61045, "FY2022": 0}),
    ("DATA", "UK government issued gilts - investment securities at amortised cost", {"FY2026": 135000, "FY2025": 125000, "FY2024": 95000, "FY2023": 70000, "FY2022": 125000}),
    ("DATA", "SSA (Sovereign, Supranational, Agency) bonds - investment securities at amortised cost", {"FY2026": 140000, "FY2025": 75000, "FY2024": 0, "FY2023": 0, "FY2022": 0}),
    ("DATA", "Unamortised interest and discount on investment securities", {"FY2026": -2313, "FY2025": -2509, "FY2024": -3281, "FY2023": -1096, "FY2022": 196}),
    ("DATA", "Derivative financial assets", {"FY2025": 0, "FY2024": 137}),
    ("DATA", "Loans and advances to customers", {"FY2026": 35122, "FY2025": 25452, "FY2024": 28225, "FY2023": 22593, "FY2022": 21779}),
    ("DATA", "Deferred tax", {"FY2026": 1781, "FY2025": 3051, "FY2024": 4730}),
    ("DATA", "Intangible assets", {"FY2026": 4420, "FY2025": 5827, "FY2024": 5986, "FY2023": 4520, "FY2022": 2591}),
    ("DATA", "Tangible fixed assets / Property, plant and equipment", {"FY2026": 1247, "FY2025": 2177, "FY2024": 3112, "FY2023": 3528, "FY2022": 4141}),
    ("DATA", "Other assets", {"FY2026": 6199, "FY2025": 7480, "FY2024": 19172, "FY2023": 16932, "FY2022": 14891}),
    ("DATA", "Prepayments and accrued income", {"FY2026": 1870, "FY2025": 1989, "FY2024": 2292}),
    ("TOTAL", "Total assets", {"FY2026": 780158, "FY2025": 681923, "FY2024": 616752, "FY2023": 558055, "FY2022": 493925}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer deposits", {"FY2026": 713291, "FY2025": 624600, "FY2024": 542169, "FY2023": 511463, "FY2022": 452500}),
    ("DATA", "Debt securities and borrowing", {"FY2026": 3000, "FY2025": 3000, "FY2024": 3000, "FY2023": 3000, "FY2022": 3000}),
    ("DATA", "Other liabilities", {"FY2026": 21719, "FY2025": 16520, "FY2024": 37321}),
    ("DATA", "Other liabilities and accruals (combined, as reported)", {"FY2023": 18386, "FY2022": 16364}),
    ("DATA", "Accruals and deferred income", {"FY2026": 5357, "FY2025": 5024, "FY2024": 5796}),
    ("DATA", "Deferred income", {"FY2023": 2238, "FY2022": 5443}),
    ("TOTAL", "Total liabilities", {"FY2026": 743367, "FY2025": 649144, "FY2024": 588286, "FY2023": 535087, "FY2022": 477307}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2026": 11, "FY2025": 9, "FY2024": 9, "FY2023": 9, "FY2022": 9}),
    ("DATA", "Share premium account", {"FY2026": 44565, "FY2025": 43335, "FY2024": 43335, "FY2023": 43321, "FY2022": 43321}),
    ("DATA", "Other reserves", {"FY2026": 0, "FY2025": 4880, "FY2024": 3993, "FY2023": 3247, "FY2022": 2349}),
    ("DATA", "Accumulated losses", {"FY2026": -7785, "FY2025": -15445, "FY2024": -18871, "FY2023": -23609, "FY2022": -29061}),
    ("TOTAL", "Total equity", {"FY2026": 36791, "FY2025": 32779, "FY2024": 28466, "FY2023": 22968, "FY2022": 16618}),
    ("TOTAL", "Total liabilities and equity", {"FY2026": 780158, "FY2025": 681923, "FY2024": 616752, "FY2023": 558055, "FY2022": 493925}),
]

bw.add_balance_sheet_sheet(
    title="Zempler Bank Limited — Statement of Financial Position",
    subtitle="Company (non-consolidated) basis, £'000.",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=64,
    source_height=380,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2026": 36810, "FY2025": 36899, "FY2024": 33911, "FY2023": 16925, "FY2022": 7358}),
    ("DATA", "Interest expense", {"FY2026": -2131, "FY2025": -2178, "FY2024": -2020, "FY2023": -1845, "FY2022": -1987}),
    ("TOTAL", "Net interest income", {"FY2026": 34679, "FY2025": 34721, "FY2024": 31891, "FY2023": 15080, "FY2022": 5371}),
    ("DATA", "Fee and commission income", {"FY2026": 31161, "FY2025": 31282, "FY2024": 33776, "FY2023": 34990, "FY2022": 33756}),
    ("DATA", "Fee and commission expense", {"FY2026": -8165, "FY2025": -7993, "FY2024": -8627, "FY2023": -7652, "FY2022": -6654}),
    ("TOTAL", "Net fee and commission income", {"FY2026": 22996, "FY2025": 23289, "FY2024": 25149, "FY2023": 27338, "FY2022": 27102}),
    ("TOTAL", "Total operating income", {"FY2026": 57675, "FY2025": 58010, "FY2024": 57040, "FY2023": 42418, "FY2022": 32473}),
    ("DATA", "Other income", {"FY2026": 1184, "FY2025": 2118, "FY2024": 2809, "FY2023": 3047, "FY2022": 1203}),
    ("DATA", "Loss on derivatives", {"FY2026": 0, "FY2025": -121, "FY2024": -278}),
    ("DATA", "Impairment charges and charge-offs", {"FY2026": -6527, "FY2025": -3771, "FY2024": -6559, "FY2023": -4426, "FY2022": -3147}),
    ("TOTAL", "Net operating income", {"FY2026": 52332, "FY2025": 56236, "FY2024": 53012, "FY2023": 41039, "FY2022": 30529}),
    ("DATA", "Administrative expenses", {"FY2026": -48107, "FY2025": -51019, "FY2024": -49721, "FY2023": -37796, "FY2022": -32632}),
    ("TOTAL", "Profit/(loss) before taxation", {"FY2026": 4225, "FY2025": 5217, "FY2024": 3291, "FY2023": 3243, "FY2022": -2103}),
    ("DATA", "Taxation charge/(credit)", {"FY2026": -1445, "FY2025": -1791, "FY2024": 1447, "FY2023": 2209, "FY2022": 0}),
    ("TOTAL", "Profit/(loss) after taxation", {"FY2026": 2780, "FY2025": 3426, "FY2024": 4738, "FY2023": 5452, "FY2022": -2103}),
    ("TOTAL", "Total comprehensive income/(loss)", {"FY2026": 2780, "FY2025": 3426, "FY2024": 4738, "FY2023": 5452, "FY2022": -2103}),
]

bw.add_income_statement_sheet(
    title="Zempler Bank Limited — Statement of Comprehensive Income",
    subtitle="Company (non-consolidated) basis, £'000. No other comprehensive income in any year shown.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=64,
    source_height=380,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
equity_headers = ["Share capital", "Share premium account", "Other reserves", "Retained earnings", "Total"]
equity_rows = [
    ("TOTAL", "Balance at 31 March 2021", (9, 41060, 1673, -26958, 15784)),
    ("DATA", "Issue of shares", (0, 2261, 0, 0, 2261)),
    ("DATA", "Loss for the period", (0, 0, 0, -2103, -2103)),
    ("DATA", "Fair value of shares allocated to employees", (0, 0, 676, 0, 676)),
    ("TOTAL", "Balance at 31 March 2022", (9, 43321, 2349, -29061, 16618)),
    ("DATA", "Issue of shares", (0, 0, 0, 0, 0)),
    ("DATA", "Profit for the period", (0, 0, 0, 5452, 5452)),
    ("DATA", "Fair value of shares allocated to employees", (0, 0, 898, 0, 898)),
    ("TOTAL", "Balance at 31 March 2023", (9, 43321, 3247, -23609, 22968)),
    ("DATA", "Issue of shares", (0, 14, 0, 0, 14)),
    ("DATA", "Total comprehensive profit for the period", (0, 0, 0, 4738, 4738)),
    ("DATA", "Employee share based payments", (0, 0, 746, 0, 746)),
    ("TOTAL", "Balance at 31 March 2024", (9, 43335, 3993, -18871, 28466)),
    ("DATA", "Issue of shares", (0, 0, 0, 0, 0)),
    ("DATA", "Total comprehensive profit for the period", (0, 0, 0, 3426, 3426)),
    ("DATA", "Employee share-based payments", (0, 0, 887, 0, 887)),
    ("TOTAL", "Balance at 31 March 2025", (9, 43335, 4880, -15445, 32779)),
    ("DATA", "Settlement of employee share scheme", (2, 1230, 0, 0, 1232)),
    ("DATA", "Total comprehensive profit for the period", (0, 0, 0, 2780, 2780)),
    ("DATA", "Transfer on exercise of share option", (0, 0, -4880, 4880, 0)),
    ("TOTAL", "Balance at 31 March 2026", (11, 44565, 0, -7785, 36791)),
]

bw.add_equity_changes_sheet(
    title="Zempler Bank Limited — Statement of Changes in Equity",
    subtitle="Company (non-consolidated) basis, £'000. Chronological, oldest to newest. Zero undocumented plug "
              "rows - ties exactly to the Balance Sheet's own Total equity every year.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=56,
    source_height=380,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) for the financial year before taxation", {"FY2026": 4225, "FY2025": 5217, "FY2024": 3291, "FY2023": 3243, "FY2022": -2103}),
    ("DATA", "Corporation tax paid", {"FY2023": 0, "FY2022": 0}),
    ("DATA", "Interest income from non-operating activities", {"FY2026": -12548, "FY2025": -9944, "FY2024": -5584, "FY2023": -1392, "FY2022": 289}),
    ("DATA", "Amortisation and depreciation / write offs", {"FY2026": 2991, "FY2025": 2987, "FY2024": 2326, "FY2023": 1427, "FY2022": 1754}),
    ("DATA", "Loss on disposal of tangible and intangible assets", {"FY2023": 619}),
    ("DATA", "Changes in fair value of derivatives", {"FY2025": 137, "FY2024": -137}),
    ("DATA", "Share based payment charge", {"FY2025": 887, "FY2024": 746, "FY2023": 898, "FY2022": 676}),
    ("DATA", "Amortisation of discount/premium for investment securities", {"FY2026": 196, "FY2025": 772, "FY2024": -2185, "FY2023": -1292, "FY2022": 196}),
    ("DATA", "Net increase/(decrease) in loans and advances to customers", {"FY2026": -9670, "FY2025": 2773, "FY2024": -5012, "FY2023": -814, "FY2022": -4593}),
    ("DATA", "Net decrease/(increase) in other assets", {"FY2026": 1281, "FY2025": 11992, "FY2024": -10054, "FY2023": 168, "FY2022": 1193}),
    ("DATA", "Net decrease in prepayments and accrued income", {"FY2026": 119, "FY2025": 303, "FY2024": 285}),
    ("DATA", "Net increase/(decrease) in customer deposits", {"FY2026": 88691, "FY2025": 82431, "FY2024": 32660, "FY2023": 58963, "FY2022": -7662}),
    ("DATA", "Net increase/(decrease) in other liabilities", {"FY2026": 5024, "FY2025": -20913, "FY2024": 20030, "FY2023": 2022, "FY2022": 1464}),
    ("DATA", "Net increase/(decrease) in deferred income", {"FY2026": 333, "FY2025": -772, "FY2024": 1843, "FY2023": -3205, "FY2022": 3071}),
    ("TOTAL", "Net cash flow generated from/(used in) operating activities", {"FY2026": 80642, "FY2025": 75570, "FY2024": 38209, "FY2023": 60637, "FY2022": -5715}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of tangible and intangible assets (combined, as reported)", {"FY2023": -3362, "FY2022": -6206}),
    ("DATA", "Purchase of intangible assets", {"FY2026": -593, "FY2025": -1712, "FY2024": -2753}),
    ("DATA", "Purchase of tangible fixed assets", {"FY2026": -61, "FY2025": -181, "FY2024": -623}),
    ("DATA", "Purchase of investment securities", {"FY2026": -287687, "FY2025": -316715, "FY2024": -242450, "FY2023": -134949, "FY2022": -1155196}),
    ("DATA", "Sale/maturity/disposal of investment securities", {"FY2026": 221859, "FY2025": 216929, "FY2024": 205326, "FY2023": 130196, "FY2022": 1460883}),
    ("DATA", "Interest received on investment securities", {"FY2026": 12844, "FY2025": 9663, "FY2024": 8262, "FY2023": 3148, "FY2022": -25}),
    ("TOTAL", "Net cash from/(used in) investing activities", {"FY2026": -53638, "FY2025": -92016, "FY2024": -32238, "FY2023": -4967, "FY2022": 299456}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Proceeds from issue of ordinary shares", {"FY2026": 1232, "FY2024": 14, "FY2022": 2261}),
    ("DATA", "Interest paid", {"FY2026": -492, "FY2025": -491, "FY2024": -493, "FY2023": -464, "FY2022": -478}),
    ("TOTAL", "Net cash from/(used in) financing activities", {"FY2026": 740, "FY2025": -491, "FY2024": -479, "FY2023": -464, "FY2022": 1783}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2026": 27744, "FY2025": -16937, "FY2024": 5492, "FY2023": 55206, "FY2022": 295524}),
    ("DATA", "Cash and cash equivalents at beginning of period", {"FY2026": 369088, "FY2025": 386025, "FY2024": 380533, "FY2023": 325327, "FY2022": 29803}),
    ("TOTAL", "Cash and cash equivalents at end of period", {"FY2026": 396832, "FY2025": 369088, "FY2024": 386025, "FY2023": 380533, "FY2022": 325327}),
]

bw.add_cash_flow_sheet(
    title="Zempler Bank Limited — Cash Flow Statement",
    subtitle="Company basis (see entity note), £'000. FY2026 financing subtotal and FY2025 operating subtotal are "
              "adjusted from the source's own printed figures - see DATA QUALITY NOTE at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=68,
    source_height=320,
    unit_suffix=" (£'000)",
)

ASSET_QUALITY_SOURCES = (
    "Sources - Zempler Bank Limited's own Note 27 'Credit Risk Management' (Credit quality by IFRS 9 stage), "
    "£'000:\n"
    f"FY2026: Zempler Bank Annual Report 2026, p.117-118 (Credit quality as at 31 March 2026) - {AR2026_URL}\n"
    f"FY2025: Zempler Bank Annual Report 2026, p.118 (FY2025 comparative column) - {AR2026_URL} (matches AR2025's "
    f"own FY2025 table exactly)\n"
    f"FY2024: Zempler Bank Annual Report 2025, p.118 (Credit quality as at 31 March 2024) - {AR2025_URL}\n"
    f"FY2023: Annual Report and Financial Statements (Cashplus Bank) for the year ended 31 March 2023, p.92 "
    f"(Credit quality as at 31 March 2023) - {AR2023_URL}\n"
    f"FY2022 (restated - the effective interest rate adjustment was added as a restatement per that report's own "
    f"Note 34): same document, p.92 (Credit quality as at 31 March 2022) - {AR2023_URL}\n"
    "Figures shown are 'provisions on loans and advances to customer' only (excluding undrawn-commitment "
    "provisions, which are disclosed separately in the source and are not part of the Balance Sheet's loans "
    "line). Note: FY2023/FY2022's Net loans and advances to customers per this note (£22,573k/£21,759k) is ~£20k "
    "below the Balance Sheet's own loans and advances line (£22,593k/£21,779k) in both years - a small, "
    "consistent gap in the source's own tables, not a transcription error; FY2024-FY2026 tie exactly."
)

def _npl(gross_s3, gross_total):
    return f"{gross_s3 / gross_total * 100:.2f}%"

aq_rows = [
    ("SECTION", "Gross loans and advances to customers by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (performing)", {"FY2026": 30138, "FY2025": 20693, "FY2024": 23438, "FY2023": 17540, "FY2022": 16493}),
    ("DATA", "Stage 2 (underperforming)", {"FY2026": 4356, "FY2025": 3136, "FY2024": 3898, "FY2023": 3529, "FY2022": 3275}),
    ("DATA", "Stage 3 (non-performing)", {"FY2026": 7154, "FY2025": 6325, "FY2024": 6896, "FY2023": 5933, "FY2022": 7143}),
    ("TOTAL", "Total gross loans and advances to customers", {"FY2026": 41648, "FY2025": 30154, "FY2024": 34232, "FY2023": 27002, "FY2022": 26911}),
    ("DATA", "Effective interest rate adjustment", {"FY2026": 542, "FY2025": 74, "FY2024": 418, "FY2023": 371, "FY2022": 285}),
    ("SECTION", "Impairment provision (ECL) by IFRS 9 stage", {}),
    ("DATA", "Stage 1 provision", {"FY2026": 1808, "FY2025": 984, "FY2024": 1314, "FY2023": 1144, "FY2022": 712}),
    ("DATA", "Stage 2 provision", {"FY2026": 1601, "FY2025": 858, "FY2024": 1086, "FY2023": 918, "FY2022": 972}),
    ("DATA", "Stage 3 provision", {"FY2026": 3659, "FY2025": 2934, "FY2024": 4025, "FY2023": 2738, "FY2022": 3753}),
    ("TOTAL", "Total impairment provision", {"FY2026": 7068, "FY2025": 4776, "FY2024": 6425, "FY2023": 4800, "FY2022": 5437}),
    ("TOTAL", "Net loans and advances to customers", {"FY2026": 35122, "FY2025": 25452, "FY2024": 28225, "FY2023": 22573, "FY2022": 21759}),
    ("SECTION", "Derived / disclosed ratios", {}),
    ("DATA", "NPL ratio (Stage 3 gross / Total gross)", {"FY2026": _npl(7154, 41648), "FY2025": _npl(6325, 30154), "FY2024": _npl(6896, 34232), "FY2023": _npl(5933, 27002), "FY2022": _npl(7143, 26911)}),
    ("DATA", "Coverage ratio - Stage 1", {"FY2026": "6.00%", "FY2025": "4.76%", "FY2024": "5.61%", "FY2023": "6.52%", "FY2022": "4.32%"}),
    ("DATA", "Coverage ratio - Stage 2", {"FY2026": "36.75%", "FY2025": "27.36%", "FY2024": "27.86%", "FY2023": "26.01%", "FY2022": "29.68%"}),
    ("DATA", "Coverage ratio - Stage 3", {"FY2026": "51.15%", "FY2025": "46.39%", "FY2024": "58.37%", "FY2023": "46.15%", "FY2022": "52.54%"}),
    ("DATA", "Coverage ratio - Total", {"FY2026": "16.97%", "FY2025": "15.84%", "FY2024": "18.77%", "FY2023": "17.78%", "FY2022": "20.20%"}),
]

bw.add_asset_quality_sheet(
    title="Zempler Bank Limited — Asset Quality",
    subtitle="Company (non-consolidated) basis, £'000.",
    rows=aq_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=64,
    source_height=240,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, P3_SOURCES, note=note, first_col_width=44, source_height=140)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 capital", {"FY2026": 30728, "FY2025": 24728, "FY2024": 19877, "FY2023": 17672, "FY2022": 16115})],
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 ratio", {"FY2026": "21.74%", "FY2025": "19.32%", "FY2024": "15.57%", "FY2023": "18.17%", "FY2022": "14.79%"})],
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2026": 30728, "FY2025": 24728, "FY2024": 19877, "FY2023": 17672, "FY2022": 16115})],
    note="Equal to CET1 capital in every year shown - Zempler holds no Additional Tier 1 (AT1) instruments.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2026": "21.74%", "FY2025": "19.32%", "FY2024": "15.57%", "FY2023": "18.17%", "FY2022": "14.79%"})],
    note="Equal to the CET1 ratio in every year shown - Zempler holds no Additional Tier 1 (AT1) instruments.",
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2026": 31755, "FY2025": 26354, "FY2024": 22103, "FY2023": 20465, "FY2022": 18343})],
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2026": "22.47%", "FY2025": "20.59%", "FY2024": "17.31%", "FY2023": "21.04%", "FY2022": "16.83%"})],
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted assets", {"FY2026": 141317, "FY2025": 127987, "FY2024": 127670, "FY2023": 97282, "FY2022": 108982})],
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - Zempler Bank Limited's own Table 1: Overview of Risk Weighted Exposure Amounts (OV1), £'000:\n"
    f"FY2026/FY2025: Zempler Bank Pillar 3 Disclosures for the year ended 31 March 2026, p.28 - {P3_2026_URL}\n"
    f"FY2024/FY2023: Zempler Bank Pillar 3 Disclosures for the year ended 31 March 2024, p.26 - {P3_2024_URL}\n"
    f"FY2022: Pillar 3 Disclosures for the year ended 31 March 2023 (Cashplus Bank, FY2022 comparative column), "
    f"p.20 - {P3_2023_URL} - this year's own OV1 table has no Counterparty Credit Risk (CCR) line (pre-dates its "
    "introduction), so that row is blank rather than zero for FY2022.\n"
    "All 5 years' category rows sum exactly to that year's own Total RWAs figure on the Total RWAs sheet."
)

bw.add_rwa_breakdown_sheet(
    title="Zempler Bank Limited — RWA Breakdown",
    subtitle="Company (non-consolidated) basis, £'000.",
    rows=[
        ("SECTION", "Risk-weighted exposure amounts", {}),
        ("DATA", "Credit Risk", {"FY2026": 33364, "FY2025": 29569, "FY2024": 42858, "FY2023": 34818, "FY2022": 36075}),
        ("DATA", "Counterparty Credit Risk (CCR)", {"FY2026": 0, "FY2025": 0, "FY2024": 780, "FY2023": 0}),
        ("DATA", "of which: Credit valuation adjustment (CVA)", {"FY2024": 299, "FY2023": 0}),
        ("DATA", "of which: other CCR", {"FY2024": 481, "FY2023": 0}),
        ("DATA", "Market Risk", {"FY2026": 0, "FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 353}),
        ("DATA", "Operational Risk", {"FY2026": 107953, "FY2025": 98418, "FY2024": 84032, "FY2023": 62464, "FY2022": 72554}),
        ("TOTAL", "Total Risk-weighted Assets", {"FY2026": 141317, "FY2025": 127987, "FY2024": 127670, "FY2023": 97282, "FY2022": 108982}),
    ],
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=54,
    source_height=180,
    unit_suffix=" (£'000)",
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Leverage ratio total exposure measure", {"FY2026": 383737, "FY2025": 310657, "FY2024": 238194, "FY2023": 181803, "FY2022": 177724}),
        ("Leverage ratio (%)", {"FY2026": "7.99%", "FY2025": "7.96%", "FY2024": "8.34%", "FY2023": "9.72%", "FY2022": "9.07%"}),
    ],
    note="Zempler's Pillar 3 reports do not distinguish an 'excluding/including claims on central banks' basis - a "
         "single leverage ratio definition is used throughout.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA)", {"FY2026": 672041, "FY2025": 593599, "FY2024": 499336, "FY2023": 465257, "FY2022": 443570}),
        ("Total net cash outflows", {"FY2026": 60635, "FY2025": 68646, "FY2024": 55908, "FY2023": 53002, "FY2022": 45275}),
        ("Liquidity Coverage Ratio (%)", {"FY2026": "1108%", "FY2025": "865%", "FY2024": "893%", "FY2023": "878%", "FY2022": "980%"}),
    ],
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding", {"FY2026": 700696, "FY2025": 606213, "FY2024": 539411, "FY2023": 498682, "FY2022": 435465}),
        ("Total required stable funding", {"FY2026": 84273, "FY2025": 75978, "FY2024": 67565, "FY2023": 45238, "FY2022": 38105}),
        ("NSFR ratio (%)", {"FY2026": "831%", "FY2025": "798%", "FY2024": "798%", "FY2023": "1102%", "FY2022": "1143%"}),
    ],
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not applicable" for y in YEARS})],
    note="Per Zempler's FY2026 Pillar 3 Disclosures: 'MREL is set annually by the Bank of England on a case-by-case "
         "basis. In line with its preferred resolution strategy for Zempler, the Bank of England does not "
         "currently require any additional MREL to be held by the bank over and above its minimum Pillar 1 and "
         "Pillar 2A requirements.' No numeric MREL disclosure exists in any year's Pillar 3 report (no KM2 template "
         "is presented), consistent with this qualitative statement.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2026": 780158, "FY2025": 681923, "FY2024": 616752, "FY2023": 558055, "FY2022": 493925}),
        ("Loans and advances to customers", {"FY2026": 35122, "FY2025": 25452, "FY2024": 28225, "FY2023": 22593, "FY2022": 21779}),
        ("Customer deposits", {"FY2026": 713291, "FY2025": 624600, "FY2024": 542169, "FY2023": 511463, "FY2022": 452500}),
        ("Total equity", {"FY2026": 36791, "FY2025": 32779, "FY2024": 28466, "FY2023": 22968, "FY2022": 16618}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total operating income", {"FY2026": 57675, "FY2025": 58010, "FY2024": 57040, "FY2023": 42418, "FY2022": 32473}),
        ("Administrative expenses", {"FY2026": -48107, "FY2025": -51019, "FY2024": -49721, "FY2023": -37796, "FY2022": -32632}),
        ("Profit/(loss) after taxation", {"FY2026": 2780, "FY2025": 3426, "FY2024": 4738, "FY2023": 5452, "FY2022": -2103}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2026": 32779, "FY2025": 28466, "FY2024": 22968, "FY2023": 16618, "FY2022": 15784}),
        ("Total comprehensive income/(loss) for the year", {"FY2026": 2780, "FY2025": 3426, "FY2024": 4738, "FY2023": 5452, "FY2022": -2103}),
        ("Other equity movements, net", {"FY2026": 1232, "FY2025": 887, "FY2024": 760, "FY2023": 898, "FY2022": 2937}),
        ("Closing equity", {"FY2026": 36791, "FY2025": 32779, "FY2024": 28466, "FY2023": 22968, "FY2022": 16618}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2026": 80642, "FY2025": 75570, "FY2024": 38209, "FY2023": 60637, "FY2022": -5715}),
        ("Net cash from/(used in) investing activities", {"FY2026": -53638, "FY2025": -92016, "FY2024": -32238, "FY2023": -4967, "FY2022": 299456}),
        ("Net cash from/(used in) financing activities", {"FY2026": 740, "FY2025": -491, "FY2024": -479, "FY2023": -464, "FY2022": 1783}),
        ("Cash and cash equivalents at end of period", {"FY2026": 396832, "FY2025": 369088, "FY2024": 386025, "FY2023": 380533, "FY2022": 325327}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2026": "21.74%", "FY2025": "19.32%", "FY2024": "15.57%", "FY2023": "18.17%", "FY2022": "14.79%"}),
        ("Tier 1 Ratio", {"FY2026": "21.74%", "FY2025": "19.32%", "FY2024": "15.57%", "FY2023": "18.17%", "FY2022": "14.79%"}),
        ("Total Capital Ratio", {"FY2026": "22.47%", "FY2025": "20.59%", "FY2024": "17.31%", "FY2023": "21.04%", "FY2022": "16.83%"}),
        ("Leverage Ratio", {"FY2026": "7.99%", "FY2025": "7.96%", "FY2024": "8.34%", "FY2023": "9.72%", "FY2022": "9.07%"}),
        ("LCR", {"FY2026": "1108%", "FY2025": "865%", "FY2024": "893%", "FY2023": "878%", "FY2022": "980%"}),
        ("NSFR", {"FY2026": "831%", "FY2025": "798%", "FY2024": "798%", "FY2023": "1102%", "FY2022": "1143%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. This workbook covers FY2022-FY2026 (not the usual FY2021-"
         "FY2025) since Zempler's first Pillar 3 disclosure covered FY2022 - it did not hold a full banking "
         "licence before 2021. See the Cash Flow Statement sheet's DATA QUALITY NOTE re: two apparent arithmetic "
         "errors found in the bank's own published FY2025/FY2026 annual reports.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/ZEMPLER FINANCIALS.xlsx")
