import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://ccbank.co.uk/wp-content/uploads/2026/04/Cambridge__Counties-Bank_Annual-Report_2025.pdf"
AR2024_URL = "https://ccbank.co.uk/wp-content/uploads/2025/05/86395_CCB-2024-Annual-Report-web.pdf"
AR2022_URL = "https://ccbank.co.uk/wp-content/uploads/2023/06/CCB_Annual-Report_2022.pdf"

P3_2024_URL = "https://ccbank.co.uk/wp-content/uploads/2025/05/Pillar-3-report-CCB-2024.docx"
P3_2023_URL = "https://ccbank.co.uk/wp-content/uploads/2024/05/Pillar-3-report-2023-Cambridge-Counties-Bank.docx"
P3_2022_URL = "https://ccbank.co.uk/wp-content/uploads/2023/05/Pillar-3-Disclosure2022.pdf"
P3_2021_URL = "https://ccbank.co.uk/wp-content/uploads/2022/06/CCB_Pillar-3-2021.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Cambridge & Counties Bank Limited (company 07972522, FRN 579415), a UK SME/commercial-property "
    "lender jointly owned by Trinity Hall (a Cambridge University college) and Cambridgeshire County Council as "
    "Administering Authority of the Cambridgeshire Local Government Pension Fund. The Bank has no subsidiaries, so "
    "all figures below are the Bank's own entity-level (not consolidated) results - there is no Group/solo basis "
    "question for this bank. No FRS cash-flow exemption is taken - a full Statement of Cash Flows is published "
    "every year. Cash flow figures for FY2021-FY2025 are internally consistent to the pound across every source "
    "document checked (each year cross-verified against its appearance as the following year's comparative "
    "column). The 2023 and 2024 Pillar 3 disclosures are published as .docx files (not PDF) with the Key Metrics "
    "table embedded as an image rather than as text/a real table - extracted by rendering the embedded image."
)

RWA_RESTATEMENT_NOTE = (
    "RWA CAVEAT: FY2022's own Pillar 3 report states Total RWA of £787,621k. FY2023's Pillar 3 report's own "
    "'31-Dec-22' comparative column instead shows £728,379k for the same date - a figure that exactly matches "
    "what FY2022's own report separately states as FY2021's RWA, suggesting the FY2023 report's comparative "
    "column was populated in error (a copy of the prior-prior year) rather than reflecting a genuine restatement. "
    "FY2022's own originally-published figure (£787,621k) is used here, per this project's standing convention of "
    "using each year's own originally-published figures - flagged prominently since the coincidence is unusual "
    "enough to be worth checking against the primary source again if precision matters."
)

LEVERAGE_NOTE = (
    "LEVERAGE CAVEAT: FY2021's own Pillar 3 report states a leverage ratio total exposure measure of £1,298,463k "
    "(ratio 12.90%). FY2022's report's FY2021 comparative instead shows £1,298,284k (ratio 12.83%) - a small "
    "(£179k / 0.07pp) discrepancy, plausibly a minor restatement or rounding difference rather than an error. "
    "FY2021's own originally-published figures are used here, per project convention."
)

LCR_NOTE = (
    "LCR CAVEAT: the formal Pillar 3/KM1 template figures (used for FY2021-FY2024 below) are themselves labelled "
    "'Average of 12 months'. The FY2025 Annual Report's own narrative separately states the Bank's FY2024 LCR as "
    "521%, materially different from the FY2024 Pillar 3 KM1 table's 605% for the same year - two different "
    "figures for what should be the same average-basis metric, not reconciled anywhere in the source documents. "
    "The formal Pillar 3 KM1 figures are used throughout FY2021-FY2024 for internal consistency across this "
    "workbook series; FY2025 (no standalone Pillar 3 document published yet) falls back to the Annual Report's "
    "own narrative figure of 587%, on a basis that may not be directly comparable to the KM1 years - flagged."
)

CASH_FLOW_SOURCES = (
    "Sources - Cambridge & Counties Bank Limited's own Statement of Cash Flows (Bank-only basis, no subsidiaries):\n"
    f"FY2025: Annual Report 2025, p.58 (own year) - {AR2025_URL}\n"
    f"FY2024: Annual Report 2024, p.82 (own year); cross-checked against Annual Report 2025's FY2024 comparative "
    f"column, p.58 (exact match) - {AR2024_URL}\n"
    f"FY2023: Annual Report 2024, p.82 (FY2023 comparative column) - {AR2024_URL}\n"
    f"FY2022: Annual Report 2022 (accounts to 31 Dec 2022), p.86 (own year) - {AR2022_URL}\n"
    f"FY2021: Annual Report 2022, p.86 (FY2021 comparative column) - {AR2022_URL}\n"
    "LABEL NOTE: both the FY2024 and FY2025 Annual Reports mislabel the financing-activities subtotal row as "
    "'Net cash (used in) investing activities' (should read 'financing') - a recurring caption typo in the Bank's "
    "own template across at least two years; the figure is correctly placed under the Financing Activities section "
    "here regardless of the source's mislabelled caption.\n"
    "PRESENTATION NOTE: FY2021-FY2024 show two running subtotals within operating activities (adjustments-for "
    "subtotal, then a working-capital-changes subtotal) before the final operating total; FY2025's presentation "
    "drops both intermediate subtotals and lists all line items in one unbroken block - both years' totals "
    "reconcile exactly against their own line items either way; FY2025's missing subtotal cells are a genuine "
    "presentation change, not a gap.\n"
    "DATA QUALITY NOTE: Annual Report 2024's own printed working-capital-changes subtotal for FY2024 reads "
    "£(21,140)k, but this does not match the sum of its own seven component line items, which total £(22,140)k - "
    "a £1,000k discrepancy. £(22,140)k is used here instead, since it is the figure that reconciles exactly to "
    "the report's own final 'Net cash generated from operating activities' total of £13,542k (£35,682k + "
    "£(22,140)k = £13,542k, matching exactly; £35,682k + £(21,140)k = £14,542k, which does not match the printed "
    "final total). The FY2023 comparative column in the same table is internally consistent and required no "
    "correction.\n"
    + ENTITY_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - Cambridge & Counties Bank Limited Pillar 3 Disclosures (entity-level, no subsidiaries):\n"
        f"FY2025: Annual Report 2025 Strategic Report 'Capital'/'Loans and liquid assets' sections, p.22-23 (no "
        f"standalone Pillar 3 document published yet for FY2025) - {AR2025_URL}\n"
        f"FY2024: Pillar 3 Disclosures 2024, Table 1: Key metrics (own year, 31-Dec-24 column) - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures 2023, Table 1: Key metrics (own year, 31-Dec-23 column) - {P3_2023_URL}\n"
        f"FY2022: Pillar 3 Disclosures 2022, Table 1: Key metrics, p.18 (own year, 31-Dec-22 column) - {P3_2022_URL}\n"
        f"FY2021: Pillar 3 Disclosures 2021, 'Own funds disclosure' table p.38 and 'Table LRCom' p.40 (own year, "
        f"2021 column) - {P3_2021_URL}\n"
        + (extra + "\n" if extra else "")
    )


bw = BankWorkbook(bank_name="Cambridge & Counties Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="390062")

STATEMENTS_SOURCES = (
    "Sources - Cambridge & Counties Bank Limited's own Income Statement / Balance Sheet / Statement of Changes "
    "in Equity (Bank-only basis, no subsidiaries):\n"
    f"FY2025: Annual Report 2025, pp.55-57 (own year) - {AR2025_URL}\n"
    f"FY2024: Annual Report 2025, pp.55-57 (FY2024 comparative column); cross-checked against Annual Report "
    f"2024's own FY2024 figures, p.80-81 (exact match) - {AR2025_URL}\n"
    f"FY2023: Annual Report 2024, pp.80-81 (FY2023 comparative column) - {AR2024_URL}\n"
    f"FY2022: Annual Report 2022 (accounts to 31 Dec 2022), pp.85-86 (own year) - {AR2022_URL}\n"
    f"FY2021: Annual Report 2022, pp.85-86 (FY2021 comparative column) - {AR2022_URL}\n"
    + ENTITY_NOTE
)

ASSET_QUALITY_SOURCES = (
    "Sources - Cambridge & Counties Bank Limited's own Note 15 (Loans and advances to customers) and Note 16 "
    "(Allowance for impairment losses):\n"
    f"FY2025/FY2024: Annual Report 2025, p.66-67 - {AR2025_URL}\n"
    f"FY2023: Annual Report 2024, Note 16 (Allowance for impairment losses), p.47's 'Gross loan balances by "
    f"Stage 2023' table, 'Closing Balance at 31 December 2023' row - {AR2024_URL}\n"
    f"FY2022/FY2021: Annual Report 2022, pp.48-49 - {AR2022_URL}\n"
    "Gross/net loan figures per the Balance Sheet above; the loan loss provision is disclosed by full IFRS 9 "
    "stage (Stage 1/2/3) in every year's own Note 16 - shown as negative (a deduction from gross loans). The "
    "loan loss provision credit/(charge) for the year is the P&L's own 'Impairment release/(losses) on loans "
    "and advances to customers' line.\n"
    + ENTITY_NOTE
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - Cambridge & Counties Bank Limited's own Pillar 3 Disclosures, Table 2 ('Overview of risk weighted "
    "exposure amounts'):\n"
    f"FY2024: Pillar 3 Disclosures 2024 (own year, 31-Dec-24 column) - {P3_2024_URL}\n"
    f"FY2023: Pillar 3 Disclosures 2023 (own year, 31-Dec-23 column) - {P3_2023_URL}\n"
    f"FY2022: Pillar 3 Disclosures 2022, p.19 (own year, 31-Dec-22 column) - {P3_2022_URL}\n"
    f"FY2021: Pillar 3 Disclosures 2022, p.19 (31-Dec-21 comparative column) - {P3_2022_URL}\n"
    "FY2025: not publicly disclosed - no standalone Pillar 3 document has been published yet for FY2025 (same "
    "gap as the other Pillar 3 metric sheets this year).\n"
    "Table 2 in the 2023/2024 Pillar 3 Disclosures is a .docx-embedded image (not text/a real table) - extracted "
    "by rendering the embedded image. All 4 years' Total row ties exactly to the Total RWAs sheet's own figure "
    "for that year.\n"
    + ENTITY_NOTE
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 282554, "FY2024": 292850, "FY2023": 302473, "FY2022": 286680, "FY2021": 240158}),
    ("DATA", "Loans and advances to banks", {"FY2025": 11034, "FY2024": 12139, "FY2023": 10420, "FY2022": 13931, "FY2021": 12293}),
    ("DATA", "Debt securities", {"FY2025": 151065, "FY2024": 65137, "FY2023": 47409, "FY2022": 30412, "FY2021": 37137}),
    ("DATA", "Loans and advances to customers", {"FY2025": 1446075, "FY2024": 1204444, "FY2023": 1083278, "FY2022": 1037710, "FY2021": 977834}),
    ("DATA", "Derivative financial assets", {"FY2025": 0, "FY2024": 149, "FY2023": 0}),
    ("DATA", "Other assets and prepayments", {"FY2025": 1534, "FY2024": 1443, "FY2023": 2526, "FY2022": 2573, "FY2021": 2091}),
    ("DATA", "Property, plant and equipment", {"FY2025": 1398, "FY2024": 1700, "FY2023": 2026, "FY2022": 2366, "FY2021": 2587}),
    ("DATA", "Intangible assets", {"FY2025": 3089, "FY2024": 2277, "FY2023": 1869, "FY2022": 1774, "FY2021": 1589}),
    ("DATA", "Current tax asset", {"FY2025": 1276, "FY2024": 689, "FY2023": 0, "FY2022": 0, "FY2021": 407}),
    ("DATA", "Deferred tax asset", {"FY2025": 608, "FY2024": 907, "FY2023": 721, "FY2022": 1099, "FY2021": 775}),
    ("TOTAL", "Total assets", {"FY2025": 1898633, "FY2024": 1581735, "FY2023": 1450722, "FY2022": 1376545, "FY2021": 1274871}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customers' accounts", {"FY2025": 1633601, "FY2024": 1271824, "FY2023": 1155224, "FY2022": 1103256, "FY2021": 1025520}),
    ("DATA", "Central Bank facilities", {"FY2025": 0, "FY2024": 55000, "FY2023": 65000, "FY2022": 78000, "FY2021": 78000}),
    ("DATA", "Subordinated debt liability", {"FY2025": 4840, "FY2024": 4800, "FY2023": 4751}),
    ("DATA", "Derivative financial liabilities", {"FY2025": 3087, "FY2024": 0, "FY2023": 652, "FY2022": 1010, "FY2021": 254}),
    ("DATA", "Provisions", {"FY2025": 0, "FY2024": 750}),
    ("DATA", "Other liabilities and accruals", {"FY2025": 8462, "FY2024": 9277, "FY2023": 9628, "FY2022": 9107, "FY2021": 7280}),
    ("DATA", "Current tax liability", {"FY2025": 0, "FY2024": 0, "FY2023": 689, "FY2022": 326, "FY2021": 0}),
    ("TOTAL", "Total liabilities", {"FY2025": 1649990, "FY2024": 1341651, "FY2023": 1235944, "FY2022": 1191699, "FY2021": 1111054}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 44955, "FY2024": 44955, "FY2023": 44955, "FY2022": 44955, "FY2021": 44955}),
    ("DATA", "Contingent convertible loan notes", {"FY2025": 22900, "FY2024": 22900, "FY2023": 22900, "FY2022": 22900, "FY2021": 22900}),
    ("DATA", "Fair value through other comprehensive income reserve", {"FY2025": 77, "FY2024": -274, "FY2023": -376, "FY2022": -1209, "FY2021": -475}),
    ("DATA", "Retained earnings", {"FY2025": 180711, "FY2024": 172503, "FY2023": 147299, "FY2022": 118200, "FY2021": 96437}),
    ("TOTAL", "Total equity", {"FY2025": 248643, "FY2024": 240084, "FY2023": 214778, "FY2022": 184846, "FY2021": 163817}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 1898633, "FY2024": 1581735, "FY2023": 1450722, "FY2022": 1376545, "FY2021": 1274871}),
]

bw.add_balance_sheet_sheet(
    title="Cambridge & Counties Bank Limited — Balance Sheet",
    subtitle="Bank-only basis (no subsidiaries), £'000. See source note at bottom.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=88,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income calculated using the effective interest rate", {"FY2025": 130181, "FY2024": 128313, "FY2023": 116023, "FY2022": 75977, "FY2021": 55335}),
    ("DATA", "Interest expense", {"FY2025": -59341, "FY2024": -54838, "FY2023": -40172, "FY2022": -16753, "FY2021": -10408}),
    ("TOTAL", "Net interest income", {"FY2025": 70840, "FY2024": 73475, "FY2023": 75851, "FY2022": 59224, "FY2021": 44927}),
    ("DATA", "Other income", {"FY2025": 376, "FY2024": 126, "FY2023": 553, "FY2022": 28, "FY2021": 23}),
    ("TOTAL", "Total operating income", {"FY2025": 71216, "FY2024": 73601, "FY2023": 76404, "FY2022": 59252, "FY2021": 44950}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Administrative expenses", {"FY2025": -32390, "FY2024": -31772, "FY2023": -27287, "FY2022": -25034, "FY2021": -21965}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -1122, "FY2024": -1077, "FY2023": -944, "FY2022": -906, "FY2021": -971}),
    ("TOTAL", "Operating profit before impairment losses", {"FY2025": 37704, "FY2024": 40752, "FY2023": 48173, "FY2022": 33312, "FY2021": 22014}),
    ("DATA", "Impairment release/(losses) on loans and advances to customers", {"FY2025": 1967, "FY2024": -4932, "FY2023": -7263, "FY2022": -4773, "FY2021": -3524}),
    ("TOTAL", "Profit before tax", {"FY2025": 39671, "FY2024": 35820, "FY2023": 40910, "FY2022": 28539, "FY2021": 18490}),
    ("DATA", "Taxation charge", {"FY2025": -9179, "FY2024": -8157, "FY2023": -9620, "FY2022": -5337, "FY2021": -3024}),
    ("TOTAL", "Profit after tax", {"FY2025": 30492, "FY2024": 27663, "FY2023": 31290, "FY2022": 23202, "FY2021": 15466}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Fair value movements taken to reserves", {"FY2025": 455, "FY2024": 150, "FY2023": 1111, "FY2022": -1233, "FY2021": -411}),
    ("DATA", "Taxation", {"FY2025": -104, "FY2024": -48, "FY2023": -278, "FY2022": 499, "FY2021": -90}),
    ("TOTAL", "Total other comprehensive income/(expense), net of tax", {"FY2025": 351, "FY2024": 102, "FY2023": 833, "FY2022": -734, "FY2021": -501}),
    ("TOTAL", "Total comprehensive income attributable to owners of the Bank", {"FY2025": 30843, "FY2024": 27765, "FY2023": 32123, "FY2022": 22468, "FY2021": 14965}),
]

bw.add_income_statement_sheet(
    title="Cambridge & Counties Bank Limited — Profit & Loss",
    subtitle="Bank-only basis (no subsidiaries), £'000. All profit for the year arises from continuing "
              "operations. See source note at bottom.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=88,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
equity_headers = ["Share capital", "Contingent convertible loan notes", "FVOCI reserve", "Retained earnings", "Total"]
equity_rows = [
    ("TOTAL", "At 1 January 2021", (44955, 22900, 26, 82254, 150135)),
    ("DATA", "Profit for the year", (None, None, None, 15466, 15466)),
    ("DATA", "Other comprehensive expense", (None, None, -501, None, -501)),
    ("DATA", "Total comprehensive income for the period (FY2021)", (None, None, -501, 15466, 14965)),
    ("DATA", "Convertible loan note interest", (None, None, None, -1283, -1283)),
    ("TOTAL", "At 31 December 2021", (44955, 22900, -475, 96437, 163817)),
    ("DATA", "Total comprehensive income for the period (FY2022)", (None, None, -734, 23202, 22468)),
    ("DATA", "Convertible loan note interest", (None, None, None, -1439, -1439)),
    ("TOTAL", "At 31 December 2022", (44955, 22900, -1209, 118200, 184846)),
    ("DATA", "Total comprehensive income for the period (FY2023)", (None, None, 833, 31290, 32123)),
    ("DATA", "Convertible loan note interest", (None, None, None, -2191, -2191)),
    ("TOTAL", "At 31 December 2023", (44955, 22900, -376, 147299, 214778)),
    ("DATA", "Total comprehensive income for the period (FY2024)", (None, None, 102, 27663, 27765)),
    ("DATA", "Convertible loan note interest", (None, None, None, -2459, -2459)),
    ("TOTAL", "At 31 December 2024", (44955, 22900, -274, 172503, 240084)),
    ("DATA", "Total comprehensive income for the period (FY2025)", (None, None, 351, 30492, 30843)),
    ("DATA", "Dividend paid", (None, None, None, -20000, -20000)),
    ("DATA", "Convertible loan note interest", (None, None, None, -2284, -2284)),
    ("TOTAL", "At 31 December 2025", (44955, 22900, 77, 180711, 248643)),
]

bw.add_equity_changes_sheet(
    title="Cambridge & Counties Bank Limited — Statement of Changes in Equity",
    subtitle="Bank-only basis (no subsidiaries), £'000, chronological (oldest to newest). All totals reconcile "
              "exactly, no plug rows needed (real audited data). See source note at bottom.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=58,
    source_height=260,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit after tax", {"FY2025": 30492, "FY2024": 27663, "FY2023": 31290, "FY2022": 23202, "FY2021": 15466}),
    ("DATA", "Subordinated debt liability interest and fee accrual", {"FY2025": 40, "FY2024": 196, "FY2023": 147}),
    ("DATA", "Depreciation, amortisation and (loss)/gain on disposals", {"FY2025": 1122, "FY2024": 1077, "FY2023": 944, "FY2022": 906, "FY2021": 971}),
    ("DATA", "(Decrease)/increase in allowance for impairment losses", {"FY2025": -9644, "FY2024": -1654, "FY2023": 5849}),
    ("DATA", "Taxation charge", {"FY2025": 9179, "FY2024": 8157, "FY2023": 9620, "FY2022": 5337, "FY2021": 3024}),
    ("DATA", "Other non-cash items", {"FY2025": 597, "FY2024": 243, "FY2023": -112}),
    ("TOTAL", "Cash flows from operating activities before changes in working capital", {"FY2024": 35682, "FY2023": 47738, "FY2022": 29445, "FY2021": 19461}),
    ("SECTION", "Net increase/(decrease) in other assets/liabilities", {}),
    ("DATA", "Net (increase)/decrease in loans and advances to customers", {"FY2025": -228708, "FY2024": -119661, "FY2023": -51418, "FY2022": -59876, "FY2021": -149454}),
    ("DATA", "Net increase/(decrease) in customers' accounts", {"FY2025": 361462, "FY2024": 116329, "FY2023": 51968, "FY2022": 77736, "FY2021": 108305}),
    ("DATA", "Net (decrease)/increase in central bank facilities", {"FY2025": -55000, "FY2024": -10000, "FY2023": -13000, "FY2022": 0, "FY2021": 78000}),
    ("DATA", "Net (increase)/decrease in derivatives", {"FY2025": -57, "FY2024": -475, "FY2023": -358, "FY2022": 756, "FY2021": 262}),
    ("DATA", "Net (decrease)/increase in value of debt securities", {"FY2022": 336, "FY2021": 591}),
    ("DATA", "Net (decrease)/increase in other liabilities and provisions", {"FY2025": -1565, "FY2024": 399, "FY2023": 520, "FY2022": 1827, "FY2021": 371}),
    ("DATA", "Net (increase)/decrease in other assets and prepayments", {"FY2025": -91, "FY2024": 1083, "FY2023": 46, "FY2022": -482, "FY2021": -661}),
    ("DATA", "Income tax paid", {"FY2025": -9572, "FY2024": -9815, "FY2023": -9154, "FY2022": -4428, "FY2021": -3050}),
    ("TOTAL", "Net increase/(decrease) in operating assets and liabilities", {"FY2024": -22140, "FY2023": -21396, "FY2022": 15869, "FY2021": 34364}),
    ("TOTAL", "Net cash generated from operating activities", {"FY2025": 98255, "FY2024": 13542, "FY2023": 26342, "FY2022": 45314, "FY2021": 53825}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Proceeds from debt securities sales/maturity", {"FY2025": 21594, "FY2024": 6609, "FY2023": 20000, "FY2022": 10000, "FY2021": 7000}),
    ("DATA", "Acquisition of debt securities", {"FY2025": -107335, "FY2024": -24437, "FY2023": -35774, "FY2022": -4845, "FY2021": -7094}),
    ("DATA", "Acquisition of property, plant & equipment and intangible assets", {"FY2025": -1631, "FY2024": -1159, "FY2023": -700, "FY2022": -870, "FY2021": -646}),
    ("TOTAL", "Net cash (used in)/generated from investing activities", {"FY2025": -87372, "FY2024": -18987, "FY2023": -16474, "FY2022": 4285, "FY2021": -740}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividend paid", {"FY2025": -20000}),
    ("DATA", "Issue of subordinated debt liability", {"FY2024": 0, "FY2023": 4604}),
    ("DATA", "Convertible loan note interest paid", {"FY2025": -2284, "FY2024": -2459, "FY2023": -2191, "FY2022": -1439, "FY2021": -1283}),
    ("TOTAL", "Net cash (used in)/generated from financing activities", {"FY2025": -22284, "FY2024": -2459, "FY2023": 2413, "FY2022": -1439, "FY2021": -1283}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -11401, "FY2024": -7904, "FY2023": 12282, "FY2022": 48160, "FY2021": 51802}),
    ("DATA", "Cash and cash equivalents at 1 January", {"FY2025": 304989, "FY2024": 312893, "FY2023": 300611, "FY2022": 252451, "FY2021": 200649}),
    ("TOTAL", "Cash and cash equivalents at 31 December", {"FY2025": 293588, "FY2024": 304989, "FY2023": 312893, "FY2022": 300611, "FY2021": 252451}),
]

bw.add_cash_flow_sheet(
    title="Cambridge & Counties Bank Limited — Statement of Cash Flows",
    subtitle="Bank-only basis (no subsidiaries), £'000. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loan book", {}),
    ("DATA", "Gross loans and advances", {"FY2025": 1454424, "FY2024": 1225716, "FY2023": 1106055, "FY2022": 1054638, "FY2021": 992600}),
    ("DATA", "Loans and advances to customers, net", {"FY2025": 1446075, "FY2024": 1204444, "FY2023": 1083278, "FY2022": 1037710, "FY2021": 977834}),
    ("SECTION", "Loan loss provision, by IFRS 9 stage", {}),
    ("DATA", "Stage 1: subject to 12-month ECL", {"FY2025": -3559, "FY2024": -2645, "FY2023": -3288, "FY2022": -3082, "FY2021": -2836}),
    ("DATA", "Stage 2: subject to lifetime ECL", {"FY2025": -3366, "FY2024": -8208, "FY2023": -8907, "FY2022": -8283, "FY2021": -5954}),
    ("DATA", "Stage 3: subject to lifetime ECL", {"FY2025": -4554, "FY2024": -10270, "FY2023": -10582, "FY2022": -5563, "FY2021": -5976}),
    ("TOTAL", "Total loan loss provision", {"FY2025": -11479, "FY2024": -21123, "FY2023": -22777, "FY2022": -16928, "FY2021": -14766}),
    ("DATA", "Loan loss provision credit/(charge) for the year", {"FY2025": 1967, "FY2024": -4932, "FY2023": -7263, "FY2022": -4773, "FY2021": -3524}),
]

bw.add_asset_quality_sheet(
    title="Cambridge & Counties Bank Limited — Asset Quality",
    subtitle="Bank-only basis (no subsidiaries), £'000. Full IFRS 9 stage split disclosed every year, "
              "including FY2023's gross loan figure (found on a follow-up pass; ties exactly to net + provision). "
              "See source note at bottom.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=88,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=180)


CET1_CAPITAL = {"FY2025": 218496, "FY2024": 213247, "FY2023": 190817, "FY2022": 163071, "FY2021": 144655}
TIER1_CAPITAL = {"FY2025": 242394, "FY2024": 236147, "FY2023": 213717, "FY2022": 185972, "FY2021": 167555}
TOTAL_CAPITAL = {"FY2025": 246946, "FY2024": 241147, "FY2023": 218717, "FY2022": 185972, "FY2021": 167555}
TOTAL_RWA = {"FY2025": 1138000, "FY2024": 980319, "FY2023": 841556, "FY2022": 787621, "FY2021": 728379}

CET1_RATIO = {"FY2025": "19.2%", "FY2024": "21.75%", "FY2023": "22.67%", "FY2022": "20.70%", "FY2021": "19.86%"}
TIER1_RATIO = {"FY2025": "21.3%", "FY2024": "24.09%", "FY2023": "25.40%", "FY2022": "23.61%", "FY2021": "23.00%"}
TOTAL_CAPITAL_RATIO = {"FY2025": "21.7%", "FY2024": "24.60%", "FY2023": "25.99%", "FY2022": "23.61%", "FY2021": "23.00%"}

CALC_NOTE_2025 = (
    "FY2025: no standalone Pillar 3 document has been published yet - CALCULATED from the Annual Report 2025's own "
    "disclosed RWA (£1,138m) and ratio (see Overview/Strategic Report), not directly disclosed as a £ figure "
    "anywhere in the source. FY2021-FY2024 are directly disclosed, not calculated."
)

metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", CET1_CAPITAL)], p3_sources(), note=CALC_NOTE_2025)
metric("CET1 Ratio", "%", [("Common Equity Tier 1 ratio", CET1_RATIO)], p3_sources())
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", TIER1_CAPITAL)], p3_sources(), note=CALC_NOTE_2025)
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", TIER1_RATIO)], p3_sources())
metric(
    "Total Capital", "£'000", [("Total capital", TOTAL_CAPITAL)], p3_sources(),
    note=CALC_NOTE_2025 + " Total Capital = Tier 1 capital alone for FY2021/FY2022 (no Tier 2 instruments held); "
                          "Tier 2 capital (£5m subordinated debt from British Business Bank Investments) was first "
                          "issued during FY2023, explaining the step-up between Tier 1 and Total Capital from that "
                          "year onward.",
)
metric("Total Capital Ratio", "%", [("Total capital ratio", TOTAL_CAPITAL_RATIO)], p3_sources())
metric("Total RWAs", "£'000", [("Total risk-weighted exposure amount", TOTAL_RWA)], p3_sources(RWA_RESTATEMENT_NOTE))

rwa_breakdown_rows = [
    ("SECTION", "RWA by risk category", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2024": 846780, "FY2023": 728547, "FY2022": 690434, "FY2021": 640391}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2024": 2753, "FY2023": 130, "FY2022": 232, "FY2021": 46}),
    ("DATA", "Securitisation exposures in the non-trading book", {"FY2024": 0, "FY2023": 0, "FY2022": 7991, "FY2021": 9158}),
    ("DATA", "Operational risk", {"FY2024": 130786, "FY2023": 112879, "FY2022": 88964, "FY2021": 78784}),
    ("DATA", "Amounts below the thresholds for deduction", {"FY2024": 2267, "FY2023": 1801, "FY2022": 2749, "FY2021": 1984}),
    ("TOTAL", "Total RWAs", {"FY2024": 980319, "FY2023": 841556, "FY2022": 787621, "FY2021": 728379}),
]

bw.add_rwa_breakdown_sheet(
    title="Cambridge & Counties Bank Limited — RWA Breakdown",
    subtitle="Bank-only basis (no subsidiaries), £'000. FY2025 not publicly disclosed (no standalone Pillar 3 "
              "document published yet). See source note at bottom.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=58,
    source_height=280,
    unit_suffix=" (£'000)",
)

metric(
    "Leverage Ratio", "£'000 exposure / %",
    [
        ("Leverage ratio total exposure measure", {"FY2024": 1605041, "FY2023": 1435897, "FY2022": 1335869, "FY2021": 1298463}),
        ("Leverage ratio (%)", {"FY2024": "14.71%", "FY2023": "14.88%", "FY2022": "13.92%", "FY2021": "12.90%"}),
    ],
    p3_sources(LEVERAGE_NOTE),
    note="FY2025 not publicly disclosed (no standalone Pillar 3 document published yet for FY2025, and the Annual "
         "Report's own Strategic Report narrative does not state a leverage ratio figure).",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA)", {"FY2024": 345604, "FY2023": 296975, "FY2022": 265556, "FY2021": 275200}),
        ("Total net cash outflows", {"FY2024": 57137, "FY2023": 47570, "FY2022": 84394, "FY2021": 95900}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "587%", "FY2024": "605%", "FY2023": "519%", "FY2022": "315%", "FY2021": "287%"}),
    ],
    p3_sources(LCR_NOTE),
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding", {"FY2024": 1303092, "FY2023": 1190919, "FY2022": 1104235}),
        ("Total required stable funding", {"FY2024": 960390, "FY2023": 873031, "FY2022": 842391}),
        ("Net Stable Funding Ratio (%)", {"FY2024": "136%", "FY2023": "136%", "FY2022": "131%"}),
    ],
    p3_sources(),
    note="FY2021 and FY2025 not publicly disclosed - the UK NSFR requirement only took effect for periods "
         "starting after 1 Jan 2022 (FY2021's Pillar 3 report has no NSFR section at all), and no standalone "
         "Pillar 3 document has been published yet for FY2025.",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={"MREL Ratio": "Not found in any of the 5 years' Annual Reports or Pillar 3 disclosures reviewed - "
                             "no numeric ratio, and no explicit exemption statement either; the Bank's balance "
                             "sheet scale is consistent with sitting below the threshold at which MREL applies."},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 1898633, "FY2024": 1581735, "FY2023": 1450722, "FY2022": 1376545, "FY2021": 1274871}),
        ("Loans and advances to customers", {"FY2025": 1446075, "FY2024": 1204444, "FY2023": 1083278, "FY2022": 1037710, "FY2021": 977834}),
        ("Customers' accounts", {"FY2025": 1633601, "FY2024": 1271824, "FY2023": 1155224, "FY2022": 1103256, "FY2021": 1025520}),
        ("Total equity", {"FY2025": 248643, "FY2024": 240084, "FY2023": 214778, "FY2022": 184846, "FY2021": 163817}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total operating income", {"FY2025": 71216, "FY2024": 73601, "FY2023": 76404, "FY2022": 59252, "FY2021": 44950}),
        ("Administrative expenses", {"FY2025": -32390, "FY2024": -31772, "FY2023": -27287, "FY2022": -25034, "FY2021": -21965}),
        ("Profit after tax", {"FY2025": 30492, "FY2024": 27663, "FY2023": 31290, "FY2022": 23202, "FY2021": 15466}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 240084, "FY2024": 214778, "FY2023": 184846, "FY2022": 163817}),
        ("Total comprehensive income for the year", {"FY2025": 30843, "FY2024": 27765, "FY2023": 32123, "FY2022": 22468, "FY2021": 14965}),
        ("Other equity movements, net", {"FY2025": -22284, "FY2024": -2459, "FY2023": -2191, "FY2022": -1439, "FY2021": -1283}),
        ("Closing equity", {"FY2025": 248643, "FY2024": 240084, "FY2023": 214778, "FY2022": 184846, "FY2021": 163817}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash generated from operating activities", {"FY2025": 98255, "FY2024": 13542, "FY2023": 26342, "FY2022": 45314, "FY2021": 53825}),
        ("Net cash (used in)/generated from investing activities", {"FY2025": -87372, "FY2024": -18987, "FY2023": -16474, "FY2022": 4285, "FY2021": -740}),
        ("Net cash (used in)/generated from financing activities", {"FY2025": -22284, "FY2024": -2459, "FY2023": 2413, "FY2022": -1439, "FY2021": -1283}),
        ("Cash and cash equivalents at 31 December", {"FY2025": 293588, "FY2024": 304989, "FY2023": 312893, "FY2022": 300611, "FY2021": 252451}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Tier 1 Ratio", TIER1_RATIO),
        ("Total Capital Ratio", TOTAL_CAPITAL_RATIO),
        ("Leverage Ratio", {"FY2024": "14.71%", "FY2023": "14.88%", "FY2022": "13.92%", "FY2021": "12.90%"}),
        ("LCR", {"FY2025": "587%", "FY2024": "605%", "FY2023": "519%", "FY2022": "315%", "FY2021": "287%"}),
        ("NSFR", {"FY2024": "136%", "FY2023": "136%", "FY2022": "131%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. See the RWA and Leverage caveats on the Total RWAs "
         "and Leverage Ratio sheets before treating year-on-year moves in those two series as fully comparable.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/CAMBRIDGE AND COUNTIES BANK FINANCIALS.xlsx")
