import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first

AR2021_URL = "https://pic.bankofchina.com/bocappd/uk/202303/P020230331590070165221.pdf"
AR2022_URL = "https://pic.bankofchina.com/bocappd/uk/202403/P020240315379765805794.pdf"
AR2023_URL = "https://pic.bankofchina.com/bocappd/uk/202405/P020240508355110735895.pdf"
AR2024_URL = "https://pic.bankofchina.com/bocappd/uk/202507/P020250718380377744220.pdf"
AR2025_URL = "https://pic.bankofchina.com/bocappd/uk/202605/P020260506389809417235.pdf"

P3_2021_URL = "https://www.bankofchina.com/uk/aboutus/ab5/202303/P020230315381669571541.pdf"
P3_2022_URL = "https://www.bankofchina.com/uk/aboutus/ab5/202310/P020231026347190320350.pdf"
P3_2023_URL = "https://www.bankofchina.com/uk/aboutus/ab5/202410/P020241008402737321677.pdf"
P3_2024_URL = "https://www.bankofchina.com/uk/aboutus/ab5/202507/P020250718380587744231.pdf"
P3_2025_URL = "https://pic.bankofchina.com/bocappd/uk/202607/P020260716391457618567.pdf"

ENTITY_NOTE = (
    "Entity note: Bank of China (UK) Limited (company 06193060, FRN 467410) is a wholly-owned UK subsidiary of "
    "Bank of China Limited (state-owned). It does not take the FRS 101/102 cash-flow-statement exemption - a full "
    "Statement of Cash Flows is published every year. All figures are the Bank's own solo entity basis throughout."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Bank of China (UK) Limited's own Statement of Cash Flows, £'000, as published on "
    "the Bank's own site (each year's own originally-published report, not a later restated comparative):\n"
    f"FY2025: Annual Report and Financial Statements for the year ended 31 December 2025, p.51-52 - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements for the year ended 31 December 2024, p.52-53 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements for the year ended 31 December 2023, p.52-53 - {AR2023_URL}\n"
    f"FY2022: Financial Statements for the year ended 31 December 2022, p.40 - {AR2022_URL}\n"
    f"FY2021: Financial Statements for the year ended 31 December 2021, p.37 - {AR2021_URL}\n"
    "Restatement note: FY2023's own report marks its FY2022 comparative column 'Restated' and shows different "
    "figures (e.g. operating activities -£17,138k, closing cash £687,013k) to FY2022's own originally-published "
    "report (operating activities +£22,570k, closing cash £657,656k). This workbook uses each year's own "
    "originally-published figures as the primary column (project convention), which creates a genuine, disclosed "
    "£29,357k gap between FY2022's own closing balance and FY2023's own opening balance - flagged here rather "
    "than silently blended or force-reconciled. The underlying cause of the restatement is not explained in "
    "either source.\n"
    "Presentation notes: FY2021-FY2023 include small 'Exchange rate movements on plant and equipment/on equity' "
    "lines not present in FY2024/FY2025's statements. FY2022 alone shows a one-off Tier 2-to-AT1 capital "
    "replacement (subordinated debt of £60,000k repaid, an equal Additional Tier 1 instrument issued, both under "
    "financing activities). FY2025's own report split 'Change in financial assets at amortised cost/fair value' "
    "into two lines (the government-bond component shown separately) and separated lease-liability cash flows "
    "into principal and interest portions for the first time - both are FY2025-only presentational changes with "
    "no net impact on any section total. FY2025's own supplementary 'cash and cash equivalents comprise' note "
    "totals £1,073,245k (£157k less than the statement's own £1,073,402k closing balance), a gap matching the "
    "same page's separately-shown expected-credit-loss allowance of £157k - the statement's own total is used as "
    "the primary closing-balance figure here. FY2022's own report does not break out a separate 'Interest paid "
    "on Additional Tier 1 instrument' line (the AT1 instrument was only issued in June 2022); FY2023's restated "
    "FY2022 comparative does show one (£1,759k), consistent with the broader FY2022 restatement noted above - "
    "not included here since it wasn't part of FY2022's own originally-published statement.\n"
    + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - Bank of China (UK) Limited Pillar 3 disclosures (UK KM1 Key Metrics template from FY2022 "
        "onward; FY2021's own document is narrative/ratio-only and predates the KM1 template), £'000 unless "
        "stated:\n"
        f"FY2025 & FY2024 comparative: Pillar 3 Disclosure 31 December 2025, p.15 (UK KM1) - {P3_2025_URL}\n"
        f"FY2024 (own year) & FY2023 comparative: Pillar 3 Disclosures 31 December 2024, p.16 (UK KM1) - {P3_2024_URL}\n"
        f"FY2023 (own year) & FY2022 comparative: Pillar 3 disclosures 31 December 2023, p.14 (UK KM1) - {P3_2023_URL}\n"
        f"FY2022 (own year) & FY2021 comparative: Pillar 3 Disclosures 2022, p.14 (UK KM1) - {P3_2022_URL}\n"
        f"FY2021 (own year, narrative/ratio-only - no KM1 template yet): Pillar 3 Disclosures 2021, p.12-14, 24 - {P3_2021_URL}\n"
        "FY2021 note: the Bank's own FY2021 Pillar 3 document states CET1/Total Capital as rounded £275m/£335m "
        "and gives no £-breakdown for leverage exposure, LCR HQLA/outflow, or NSFR (NSFR was not yet a formal "
        "disclosure). The precise FY2021 figures used on those sheets (CET1/Tier 1 £275,164k, Total Capital "
        "£335,164k, leverage exposure £2,431,869k, LCR HQLA £527,697k/outflow £294,774k, NSFR £1,438,026k/"
        "£950,742k) are taken from the FY2022 Pillar 3 document's FY2021 comparative column instead, since it is "
        "the more complete disclosure - all overlapping ratios (CET1 24.6%, Total Capital 29.9%, Leverage 11.3%, "
        "LCR 179.0%) match the FY2021 document's own narrative figures exactly.\n"
        + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="Bank of China (UK) Limited", years=YEARS, header_color="B22222")

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
AR2024_OWN_NOTE = (
    "FY2024's own primary source is its own report (AR2024_URL), not AR2025's comparative column - both are "
    "identical figures (verified), no restatement."
)

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 982512, "FY2024": 975201, "FY2023": 687070, "FY2022": 657656, "FY2021": 716133}),
    ("DATA", "Government bonds", {"FY2025": 142529, "FY2024": 144495, "FY2023": 118328, "FY2022": 44264}),
    ("DATA", "Loans and advances to banks", {"FY2025": 90733, "FY2024": 73658, "FY2023": 86477, "FY2022": 29357, "FY2021": 69065}),
    ("DATA", "Loans and advances to customers", {"FY2025": 810985, "FY2024": 941507, "FY2023": 990763, "FY2022": 1122459, "FY2021": 1194653}),
    ("DATA", "Derivative financial instruments", {"FY2025": 2504, "FY2024": 4667, "FY2023": 5506, "FY2022": 7702, "FY2021": 11}),
    ("DATA", "Prepayments, accrued income and other assets", {"FY2025": 156554, "FY2024": 138246, "FY2023": 130581, "FY2022": 351967, "FY2021": 87868}),
    ("DATA", "Financial assets at fair value through profit and loss", {"FY2025": 71293, "FY2024": 30150, "FY2023": 47445, "FY2022": 60514, "FY2021": 64659}),
    ("DATA", "Current tax asset", {"FY2025": 4582, "FY2024": 2934, "FY2023": 637, "FY2022": 2351, "FY2021": 5979}),
    ("DATA", "Deferred tax assets", {"FY2025": 289, "FY2024": 406, "FY2023": 359, "FY2022": 1280, "FY2021": 1283}),
    ("DATA", "Property, plant and equipment", {"FY2025": 11573, "FY2024": 11419, "FY2023": 11902, "FY2022": 12769, "FY2021": 11167}),
    ("DATA", "Intangible assets", {"FY2025": 887, "FY2024": 636, "FY2023": 305, "FY2022": 274, "FY2021": 362}),
    ("TOTAL", "Total assets", {"FY2025": 2274441, "FY2024": 2323319, "FY2023": 2079373, "FY2022": 2290593, "FY2021": 2151180}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks", {"FY2025": 511961, "FY2024": 493256, "FY2023": 369590, "FY2022": 539387, "FY2021": 396254}),
    ("DATA", "Deposits from customers", {"FY2025": 1304816, "FY2024": 1355529, "FY2023": 1223068, "FY2022": 1291150, "FY2021": 1333523}),
    ("DATA", "Derivative financial instruments", {"FY2025": 289, "FY2024": 2, "FY2023": 3, "FY2022": 13, "FY2021": 5280}),
    ("DATA", "Other liabilities", {"FY2025": 39574, "FY2024": 37473, "FY2023": 38352, "FY2022": 50379, "FY2021": 43571}),
    ("DATA", "Accruals and deferred income", {"FY2025": 18650, "FY2024": 23257, "FY2023": 15017, "FY2022": 7720, "FY2021": 5657}),
    ("DATA", "Impairment provision on off balance sheet products", {"FY2025": 138, "FY2024": 58, "FY2023": 54, "FY2022": 51, "FY2021": 119}),
    ("DATA", "Subordinated liabilities", {"FY2021": 60000}),
    ("TOTAL", "Total liabilities", {"FY2025": 1875428, "FY2024": 1909575, "FY2023": 1646084, "FY2022": 1888700, "FY2021": 1844404}),
    ("SECTION", "Equity", {}),
    ("DATA", "Authorised and called up share capital", {"FY2025": 250000, "FY2024": 250000, "FY2023": 250000, "FY2022": 250000, "FY2021": 250000}),
    ("DATA", "Other equity instruments (Additional Tier 1)", {"FY2025": 60000, "FY2024": 60000, "FY2023": 60000, "FY2022": 60000}),
    ("DATA", "Retained earnings", {"FY2025": 89013, "FY2024": 103744, "FY2023": 123289, "FY2022": 91893, "FY2021": 56776}),
    ("TOTAL", "Total shareholders' equity", {"FY2025": 399013, "FY2024": 413744, "FY2023": 433289, "FY2022": 401893, "FY2021": 306776}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 2274441, "FY2024": 2323319, "FY2023": 2079373, "FY2022": 2290593, "FY2021": 2151180}),
]

BALANCE_SHEET_SOURCES = (
    "Sources - Bank of China (UK) Limited's own Statement of Financial Position (Bank/solo basis - no group "
    "accounts prepared, Companies Act 2006 s.401 exemption), £'000, each year's own originally-published report:\n"
    f"FY2025: Annual Report 2025, p.49 - {AR2025_URL}\n"
    f"FY2024: Annual Report 2024, p.49 - {AR2024_URL} ({AR2024_OWN_NOTE})\n"
    f"FY2023: Annual Report 2023, p.50 - {AR2023_URL}\n"
    f"FY2022: Financial Statements 2022, p.38 - {AR2022_URL}\n"
    f"FY2021: Financial Statements 2021, p.35 - {AR2021_URL}\n"
    "Presentation notes: 'Government bonds' only appears as its own line from FY2022 onward (no separate line "
    "existed pre-2022 - blank for FY2021, not zero). 'Subordinated liabilities' (£60,000k, FY2021) was repaid "
    "and replaced by an equal £60,000k Additional Tier 1 instrument in June 2022 - both nil/blank in the years "
    "they don't apply. 'Investment in subsidiary companies' is nil every year and omitted as a row. FY2021's "
    "own report's Statement of Changes in Equity states closing retained earnings as £56,706k, £70k less than "
    "the Balance Sheet's own £56,776k for the same date - the Balance Sheet's single 'Retained earnings' line "
    "appears to combine the SOCE's separate retained-earnings and FX-translation-reserve columns (£56,706k + "
    "£70k = £56,776k); total equity ties out exactly either way (£306,776k).\n"
    + ENTITY_NOTE
)

bw.add_balance_sheet_sheet(
    title="Bank of China (UK) Limited — Statement of Financial Position",
    subtitle="Bank of China (UK) Limited (solo entity basis), £'000",
    rows=balance_sheet_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=68,
    source_height=200,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 110123, "FY2024": 128817, "FY2023": 121217, "FY2022": 62661, "FY2021": 36936}),
    ("DATA", "Interest expense", {"FY2025": -53024, "FY2024": -57415, "FY2023": -40422, "FY2022": -13239, "FY2021": -3650}),
    ("TOTAL", "Net interest income", {"FY2025": 57099, "FY2024": 71402, "FY2023": 80795, "FY2022": 49422, "FY2021": 33286}),
    ("DATA", "Fee and commission income", {"FY2025": 3399, "FY2024": 3228, "FY2023": 3378, "FY2022": 3955, "FY2021": 4294}),
    ("DATA", "Fee and commission expense", {"FY2025": -1462, "FY2024": -1481, "FY2023": -1692, "FY2022": -1694, "FY2021": -1319}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 1937, "FY2024": 1747, "FY2023": 1686, "FY2022": 2261, "FY2021": 2975}),
    ("DATA", "Net fair value gain/(loss) on financial instruments", {"FY2025": 3431, "FY2024": 4711, "FY2023": 9119, "FY2022": 148, "FY2021": 1923}),
    ("DATA", "Foreign exchange gain", {"FY2025": 2388, "FY2024": 2295, "FY2023": 386, "FY2022": 4916, "FY2021": 2590}),
    ("DATA", "Net other operating income", {"FY2025": 123435, "FY2024": 107108, "FY2023": 114199, "FY2022": 93633, "FY2021": 83274}),
    ("TOTAL", "Non-interest income", {"FY2025": 129254, "FY2024": 114114, "FY2023": 123704, "FY2022": 98697, "FY2021": 87787}),
    ("TOTAL", "Total income", {"FY2025": 188290, "FY2024": 187263, "FY2023": 206185, "FY2022": 150380, "FY2021": 124048}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Staff costs", {"FY2025": -86079, "FY2024": -72194, "FY2023": -68058, "FY2022": -59208, "FY2021": -50154}),
    ("DATA", "Other expenses", {"FY2025": -10029, "FY2024": -9735, "FY2023": -9543, "FY2022": -9818, "FY2021": -8924}),
    ("DATA", "Depreciation of plant and equipment", {"FY2025": -1870, "FY2024": -1540, "FY2023": -1572, "FY2022": -1462, "FY2021": -1802}),
    ("DATA", "Amortisation of intangible assets", {"FY2025": -161, "FY2024": -104, "FY2023": -52, "FY2022": -271, "FY2021": -237}),
    ("DATA", "Credit/(provision) for expected credit losses", {"FY2025": 217, "FY2024": 3953, "FY2023": 11235, "FY2022": 11526, "FY2021": -23665}),
    ("TOTAL", "Profit before income tax", {"FY2025": 90368, "FY2024": 107643, "FY2023": 138195, "FY2022": 91147, "FY2021": 39266}),
    ("DATA", "Income tax expense", {"FY2025": -21437, "FY2024": -23726, "FY2023": -34982, "FY2022": -22583, "FY2021": -7788}),
    ("TOTAL", "Profit for the year", {"FY2025": 68931, "FY2024": 83917, "FY2023": 103213, "FY2022": 68564, "FY2021": 31478}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Foreign currency translation", {"FY2025": 80, "FY2023": -2, "FY2022": 12, "FY2021": 134}),
    ("TOTAL", "Other comprehensive income/(expense) for the year", {"FY2025": 80, "FY2024": 0, "FY2023": -2, "FY2022": 12, "FY2021": 134}),
    ("TOTAL", "Total comprehensive income for the year", {"FY2025": 69011, "FY2024": 83917, "FY2023": 103211, "FY2022": 68576, "FY2021": 31612}),
]

INCOME_STATEMENT_SOURCES = (
    "Sources - Bank of China (UK) Limited's own Income Statement / Statement of Comprehensive Income (Bank/solo "
    "basis), £'000, each year's own originally-published report:\n"
    f"FY2025: Annual Report 2025, p.47-48 - {AR2025_URL}\n"
    f"FY2024: Annual Report 2024, p.48-49 - {AR2024_URL} ({AR2024_OWN_NOTE})\n"
    f"FY2023: Annual Report 2023, p.48-49 - {AR2023_URL}\n"
    f"FY2022: Financial Statements 2022, p.36-37 - {AR2022_URL}\n"
    f"FY2021: Financial Statements 2021, p.33-34 - {AR2021_URL}\n"
    "Profit before income tax ties exactly to the Cash Flow Statement's own 'Profit before income tax' row for "
    "every year, cross-checked as a reconciliation.\n"
    + ENTITY_NOTE
)

bw.add_income_statement_sheet(
    title="Bank of China (UK) Limited — Income Statement and Statement of Comprehensive Income",
    subtitle="Bank of China (UK) Limited (solo entity basis), £'000",
    rows=income_statement_rows,
    sources_text=INCOME_STATEMENT_SOURCES,
    first_col_width=68,
    source_height=180,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Issued share capital", "Other equity instruments", "Retained earnings", "Foreign currency translation reserve", "Total"]

equity_changes_rows = [
    ("DATA", "As at 1 January 2021", (250000, 0, 92228, -64, 342164)),
    ("DATA", "Profit for the financial year", (0, 0, 31478, 0, 31478)),
    ("DATA", "Foreign exchange and other", (0, 0, 0, 134, 134)),
    ("TOTAL", "Total comprehensive income", (0, 0, 31478, 134, 31612)),
    ("DATA", "Dividend paid", (0, 0, -67000, 0, -67000)),
    ("TOTAL", "As at 31 December 2021", (250000, 0, 56706, 70, 306776)),
    ("DATA", "Additional Tier 1 capital issued", (0, 60000, 0, 0, 60000)),
    ("DATA", "Profit for the financial year", (0, 0, 68564, 0, 68564)),
    ("DATA", "Foreign exchange and other", (0, 0, 0, 12, 12)),
    ("TOTAL", "Total comprehensive income", (0, 0, 68564, 12, 68576)),
    ("DATA", "Dividend paid", (0, 0, -33459, 0, -33459)),
    ("TOTAL", "As at 31 December 2022", (250000, 60000, 91811, 82, 401893)),
    ("DATA", "Profit for the financial year", (0, 0, 103213, 0, 103213)),
    ("DATA", "Foreign exchange and other", (0, 0, 0, -2, -2)),
    ("TOTAL", "Total comprehensive income", (0, 0, 103213, -2, 103211)),
    ("DATA", "Dividend paid", (0, 0, -71815, 0, -71815)),
    ("TOTAL", "As at 31 December 2023", (250000, 60000, 123209, 80, 433289)),
    ("DATA", "Profit for the financial year", (0, 0, 83917, 0, 83917)),
    ("TOTAL", "Total comprehensive income", (0, 0, 83917, 0, 83917)),
    ("DATA", "Dividend paid", (0, 0, -103462, 0, -103462)),
    ("TOTAL", "As at 31 December 2024", (250000, 60000, 103664, 80, 413744)),
    ("DATA", "Profit for the financial year", (0, 0, 68931, 0, 68931)),
    ("DATA", "Transfer", (0, 0, 80, -80, 0)),
    ("TOTAL", "Total comprehensive income", (0, 0, 69011, 0, 69011)),
    ("DATA", "Dividend paid", (0, 0, -83662, 0, -83662)),
    ("TOTAL", "As at 31 December 2025", (250000, 60000, 89013, 0, 399013)),
]

EQUITY_CHANGES_SOURCES = (
    "Sources - Bank of China (UK) Limited's own Statement of Changes in Equity (Bank/solo basis), £'000, "
    "chronological roll-forward reconstructed from each year's own originally-published report:\n"
    f"2021 movements: Financial Statements 2021, p.36 - {AR2021_URL}\n"
    f"2022 movements: Financial Statements 2022, p.39 - {AR2022_URL}\n"
    f"2023 movements: Annual Report 2023, p.51 - {AR2023_URL}\n"
    f"2024 movements: Annual Report 2024, p.50 - {AR2024_URL} ({AR2024_OWN_NOTE})\n"
    f"2025 movements: Annual Report 2025, p.50 - {AR2025_URL}\n"
    "Note: the 'Dividend paid' row in this statement (which includes both ordinary share dividends and Additional "
    "Tier 1 coupon/interest payments to the parent) differs from the Cash Flow Statement's separately-split "
    "'Dividend paid'/'Interest paid on Additional Tier 1 instrument' lines - e.g. FY2025's £83,662k here vs "
    "£78,700k + £4,962k = £83,662k on the Cash Flow Statement (ties out exactly once combined; genuinely two "
    "different presentations of the same total, not a discrepancy).\n"
    + ENTITY_NOTE
)

bw.add_equity_changes_sheet(
    title="Bank of China (UK) Limited — Statement of Changes in Equity",
    subtitle="Bank of China (UK) Limited (solo entity basis), £'000, chronological",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQUITY_CHANGES_SOURCES,
    first_col_width=42,
    source_height=190,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit before income tax", {"FY2025": 90368, "FY2024": 107644, "FY2023": 138195, "FY2022": 91147, "FY2021": 39266}),
    ("DATA", "Depreciation and amortisation of plant and equipment and intangible assets", {"FY2025": 2031, "FY2024": 1644, "FY2023": 1624, "FY2022": 1733, "FY2021": 2039}),
    ("DATA", "Net (credit)/loss for expected credit losses", {"FY2025": -297, "FY2024": -3958, "FY2023": -11237, "FY2022": -11526, "FY2021": 23665}),
    ("DATA", "Exchange rate movements on plant and equipment", {"FY2021": -1}),
    ("DATA", "Exchange rate movements on equity", {"FY2023": -1, "FY2022": 12, "FY2021": 135}),
    ("DATA", "Net fair value (gain)/loss on financial instruments", {"FY2025": -1895, "FY2024": -1310, "FY2023": -7446, "FY2022": 10358, "FY2021": 2656}),
    ("SECTION", "Changes in operating assets and liabilities", {}),
    ("DATA", "Change in derivative financial instruments assets", {"FY2025": 2163, "FY2024": 839, "FY2023": 2196, "FY2022": -7691, "FY2021": -8}),
    ("DATA", "Change in loans and advances to banks", {"FY2022": 39708, "FY2021": 41381}),
    ("DATA", "Change in loans and advances to customers", {"FY2025": 130992, "FY2024": 53197, "FY2023": 142977, "FY2022": 83721, "FY2021": -79736}),
    ("DATA", "Change in financial assets at amortised cost/fair value", {"FY2025": -39251, "FY2024": 16787, "FY2023": 20515, "FY2022": -6213, "FY2021": 10167}),
    ("DATA", "Change in financial assets at amortised cost - Government bonds", {"FY2025": 2147}),
    ("DATA", "Change in other assets", {"FY2025": -18315, "FY2024": -7665, "FY2023": 221384, "FY2022": -264099, "FY2021": -9099}),
    ("DATA", "Change in derivative financial instruments liabilities", {"FY2025": 287, "FY2024": 1, "FY2023": -10, "FY2022": -5267, "FY2021": -3484}),
    ("DATA", "Change in deposits from banks", {"FY2025": 18705, "FY2024": 123666, "FY2023": -169797, "FY2022": 143133, "FY2021": 176876}),
    ("DATA", "Change in deposits from customers", {"FY2025": -50713, "FY2024": 132461, "FY2023": -68081, "FY2022": -42374, "FY2021": 117876}),
    ("DATA", "Change in other liabilities and provisions", {"FY2025": -2001, "FY2024": 7855, "FY2023": -4681, "FY2022": 8883, "FY2021": 1456}),
    ("DATA", "Income taxes paid", {"FY2025": -22969, "FY2024": -26070, "FY2023": -32346, "FY2022": -18955, "FY2021": -18895}),
    ("TOTAL", "Net cash generated from operating activities", {"FY2025": 111252, "FY2024": 405091, "FY2023": 233292, "FY2022": 22570, "FY2021": 304294}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Acquisition of government bonds", {"FY2025": -78477, "FY2024": -36107, "FY2023": -74108, "FY2022": -44264}),
    ("DATA", "Proceeds from government bonds", {"FY2025": 78289, "FY2024": 11775}),
    ("DATA", "Acquisition of property, plant and equipment", {"FY2025": -2120, "FY2024": -1086, "FY2023": -745, "FY2022": -3086, "FY2021": -1349}),
    ("DATA", "Acquisition of intangible assets", {"FY2025": -412, "FY2024": -435, "FY2023": -83, "FY2022": -183, "FY2021": -86}),
    ("DATA", "Proceeds from disposal of property, plant and equipment", {"FY2025": 97, "FY2024": 27, "FY2023": 40, "FY2022": 22, "FY2021": 272}),
    ("DATA", "Proceeds from disposal of intangible assets", {"FY2021": 16}),
    ("TOTAL", "Net cash from/(used in) investing activities", {"FY2025": -2623, "FY2024": -25826, "FY2023": -74896, "FY2022": -47511, "FY2021": -1147}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Repayment of subordinated debt", {"FY2022": -60000}),
    ("DATA", "Issuance of Additional Tier 1 instrument", {"FY2022": 60000}),
    ("DATA", "Dividend paid", {"FY2025": -78700, "FY2024": -98100, "FY2023": -66800, "FY2022": -33459, "FY2021": -67000}),
    ("DATA", "Interest paid on Additional Tier 1 instrument", {"FY2025": -4962, "FY2024": -5362, "FY2023": -5015}),
    ("DATA", "Repayment of principal portion of lease liabilities", {"FY2025": -722, "FY2024": -491, "FY2023": -47, "FY2022": -77, "FY2021": -1393}),
    ("DATA", "Repayment of interest portion of lease liabilities", {"FY2025": 298}),
    ("TOTAL", "Net cash used in financing activities", {"FY2025": -84086, "FY2024": -103953, "FY2023": -71862, "FY2022": -33536, "FY2021": -68393}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 24543, "FY2024": 275312, "FY2023": 86534, "FY2022": -58477, "FY2021": 234754}),
    ("DATA", "Cash and cash equivalents at beginning of period", {"FY2025": 1048859, "FY2024": 773547, "FY2023": 687013, "FY2022": 716133, "FY2021": 481379}),
    ("TOTAL", "Cash and cash equivalents at end of period", {"FY2025": 1073402, "FY2024": 1048859, "FY2023": 773547, "FY2022": 657656, "FY2021": 716133}),
]

bw.add_cash_flow_sheet(
    title="Bank of China (UK) Limited — Statement of Cash Flows",
    subtitle="Bank of China (UK) Limited (solo entity basis), £'000",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=72,
    source_height=210,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Gross carrying amount by product", {}),
    ("DATA", "Wholesale loans", {"FY2025": 2162, "FY2024": 2242, "FY2023": 2352, "FY2022": 2535, "FY2021": 4806}),
    ("DATA", "Housing loans", {"FY2025": 895, "FY2024": 1117, "FY2023": 2279, "FY2022": 2417, "FY2021": 2607}),
    ("DATA", "Syndicated loans", {"FY2025": 194775, "FY2024": 238983, "FY2023": 173584, "FY2022": 155931, "FY2021": 183604}),
    ("DATA", "Factoring financing", {"FY2025": 1898, "FY2024": 2185, "FY2023": 4840, "FY2022": 4219, "FY2021": 7892}),
    ("DATA", "Credit cards", {"FY2025": 343, "FY2024": 382, "FY2023": 501, "FY2022": 401, "FY2021": 449}),
    ("DATA", "Mortgage loans", {"FY2025": 611782, "FY2024": 697619, "FY2023": 812348, "FY2022": 973424, "FY2021": 1035418}),
    ("DATA", "Financing order", {"FY2024": 319, "FY2023": 140, "FY2022": 92, "FY2021": 1960}),
    ("TOTAL", "Total gross carrying amount", {"FY2025": 811855, "FY2024": 942847, "FY2023": 996044, "FY2022": 1139019, "FY2021": 1236736}),
    ("SECTION", "Gross carrying amount by IFRS 9 stage", {}),
    ("DATA", "Stage 1: 12-month ECL", {"FY2025": 755256, "FY2024": 838850, "FY2023": 875144, "FY2022": 932381, "FY2021": 1161138}),
    ("DATA", "Stage 2: Lifetime ECL, not credit-impaired", {"FY2025": 52230, "FY2024": 99518, "FY2023": 117365, "FY2022": 133805, "FY2021": 23529}),
    ("DATA", "Stage 3: Lifetime ECL, credit-impaired", {"FY2025": 4369, "FY2024": 4479, "FY2023": 3535, "FY2022": 72833, "FY2021": 52069}),
    ("TOTAL", "Total gross carrying amount (by stage)", {"FY2025": 811855, "FY2024": 942847, "FY2023": 996044, "FY2022": 1139019, "FY2021": 1236736}),
    ("SECTION", "Reconciliation to Balance Sheet", {}),
    ("DATA", "Net carrying value (Balance Sheet's Loans and advances to customers)", {"FY2025": 810985, "FY2024": 941507, "FY2023": 990763, "FY2022": 1122459, "FY2021": 1194653}),
    ("DATA", "Implied total ECL allowance (gross − net)", {"FY2025": 870, "FY2024": 1340, "FY2023": 5281, "FY2022": 16560, "FY2021": 42083}),
    ("SECTION", "Asset quality ratios", {}),
    ("DATA", "ECL coverage ratio (implied allowance / gross carrying amount)", {"FY2025": "0.11%", "FY2024": "0.14%", "FY2023": "0.53%", "FY2022": "1.45%", "FY2021": "3.40%"}),
    ("DATA", "Stage 3 / NPL ratio (Stage 3 gross / total gross carrying amount)", {"FY2025": "0.54%", "FY2024": "0.48%", "FY2023": "0.35%", "FY2022": "6.39%", "FY2021": "4.21%"}),
]

ASSET_QUALITY_SOURCES = (
    "Sources - Note 6(a) 'Analysis of risk concentration in the financial position' (Global/Europe/US/UK/UK "
    "Retail x Stage 1/2/3 geographic table), Bank/solo basis, £'000. By-product and by-stage figures here are "
    "summed from that table's 'Loans and advances to customers' product rows (Wholesale/Housing/Syndicated/"
    "Factoring/Credit Cards/Mortgage/Financing Order) across all geography columns - both groupings tie exactly "
    "to each other and to the same total for every year (verified):\n"
    f"FY2025: Annual Report 2025, p.77 - {AR2025_URL}\n"
    f"FY2024: Annual Report 2025's own FY2024 comparative column, p.78 (figures independently cross-checked "
    "against AR2024's own Balance Sheet net-loans figure) - {AR2025_URL}\n"
    f"FY2023: Annual Report 2023, p.80 - {AR2023_URL}\n"
    f"FY2022: Annual Report 2023's own FY2022 comparative column, p.81 - {AR2023_URL}\n"
    f"FY2021: Financial Statements 2021, p.67 - {AR2021_URL}\n"
    "'Implied total ECL allowance' is not separately disclosed by product/stage anywhere in these documents - it "
    "is the residual gap between this note's gross carrying total and the Balance Sheet's own net carrying "
    "value, so it captures the whole-portfolio allowance only (not split by stage), hence no separate Stage 3 "
    "coverage ratio is shown here (would require a stage-level allowance split that isn't disclosed). FY2021's "
    "large ECL gap (£42,083k, 3.40% coverage) is consistent with that year's Cash Flow Statement, which shows "
    "the largest single-year 'Net loss for expected credit losses' charge (£23,665k) in the whole 5-year series. "
    "FY2022's elevated Stage 3/NPL ratio (6.39%, mostly Syndicated loans) fell sharply by FY2023 (0.35%) - both "
    "years' own source tables, not smoothed or averaged.\n"
    + ENTITY_NOTE
)

bw.add_asset_quality_sheet(
    title="Bank of China (UK) Limited — Asset Quality / Credit Risk Disclosures",
    subtitle="Bank of China (UK) Limited (solo entity basis), £'000 (ratios as calculated)",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=68,
    source_height=270,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=46, source_height=170)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 274521, "FY2024": 274294, "FY2023": 275056, "FY2022": 275000, "FY2021": 275164})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 ratio", {"FY2025": "27.2%", "FY2024": "24.8%", "FY2023": "26.8%", "FY2022": "23.4%", "FY2021": "24.6%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2025": 334521, "FY2024": 334294, "FY2023": 335056, "FY2022": 335000, "FY2021": 275164})],
    p3_sources(),
    note="Equal to CET1 capital at FY2021 (no AT1 instruments in issue that year). A £60m Additional Tier 1 "
         "instrument was issued in June 2022, replacing an equal amount of Tier 2 subordinated debt.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "33.2%", "FY2024": "30.2%", "FY2023": "32.7%", "FY2022": "28.5%", "FY2021": "24.6%"})],
    p3_sources(),
    note="FY2021 not separately stated as a percentage in the source; numerically equal to the stated CET1 ratio "
         "since Tier 1 capital equalled CET1 capital exactly that year (no AT1 in issue).",
)

metric(
    "Total Capital", "£'000",
    [("Total regulatory capital", {"FY2025": 334521, "FY2024": 334294, "FY2023": 335056, "FY2022": 335000, "FY2021": 335164})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "33.2%", "FY2024": "30.2%", "FY2023": "32.7%", "FY2022": "28.5%", "FY2021": "29.9%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted assets (RWA)", {"FY2025": 1008110, "FY2024": 1106898, "FY2023": 1024452, "FY2022": 1176625, "FY2021": 1119380})],
    p3_sources(),
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - Bank of China (UK) Limited's UK KM1 Key Metrics tables (same 5 Pillar 3 documents as the Total "
    "RWAs sheet):\n"
    f"FY2025 & FY2024 comparative: Pillar 3 Disclosure 31 December 2025, p.15 - {P3_2025_URL}\n"
    f"FY2023-FY2021: see p3_sources() citations on the Total RWAs sheet.\n\n"
    "NOT DISCLOSED (category breakdown): none of the 5 Pillar 3 documents contains a UK OV1 'Overview of risk "
    "weighted exposure amounts' table breaking RWA down by risk category (credit/market/operational/CVA) - "
    "confirmed by reading the FY2025 document's own table of contents and KM1 template in full. Only the single "
    "aggregate Total RWA figure exists for every year (see the Total RWAs sheet, which this sheet's Total row "
    "ties out to exactly)."
)

bw.add_rwa_breakdown_sheet(
    title="Bank of China (UK) Limited — RWA Breakdown",
    subtitle="Bank of China (UK) Limited (solo entity basis), £'000",
    rows=[
        ("DATA", "Not publicly disclosed — category breakdown", {y: "Not publicly disclosed" for y in YEARS}),
        ("TOTAL", "Total risk exposure amount", {"FY2025": 1008110, "FY2024": 1106898, "FY2023": 1024452, "FY2022": 1176625, "FY2021": 1119380}),
    ],
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=58,
    source_height=170,
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Total Basel III leverage ratio exposure measure", {"FY2025": 1373968, "FY2024": 1462346, "FY2023": 1473437, "FY2022": 1814024, "FY2021": 2431869}),
        ("Basel III leverage ratio (%)", {"FY2025": "24.4%", "FY2024": "22.9%", "FY2023": "22.7%", "FY2022": "18.5%", "FY2021": "11.3%"}),
    ],
    p3_sources(),
    note="FY2021's 11.3% is on an older/broader exposure-measure basis (pre-dates the KM1 'excluding claims on "
         "central banks' framework used from FY2022 onward) - not directly comparable to later years, kept on "
         "its own row per project convention.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA)", {"FY2025": 1007375, "FY2024": 1014087, "FY2023": 677646, "FY2022": 545654, "FY2021": 527697}),
        ("Total net cash outflow", {"FY2025": 310866, "FY2024": 272240, "FY2023": 174967, "FY2022": 299877, "FY2021": 294774}),
        ("LCR ratio (%)", {"FY2025": "324.1%", "FY2024": "372.5%", "FY2023": "387.3%", "FY2022": "182.0%", "FY2021": "179.0%"}),
    ],
    p3_sources(),
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding", {"FY2025": 1389486, "FY2024": 1630136, "FY2023": 1289845, "FY2022": 1463448, "FY2021": 1438026}),
        ("Total required stable funding", {"FY2025": 714820, "FY2024": 752941, "FY2023": 959234, "FY2022": 1209361, "FY2021": 950742}),
        ("NSFR ratio (%)", {"FY2025": "194.4%", "FY2024": "216.5%", "FY2023": "134.5%", "FY2022": "121.0%", "FY2021": "151.3%"}),
    ],
    p3_sources(),
    note="FY2021's own Pillar 3 document does not disclose an NSFR figure at all (the UK NSFR regime's formal KM1 "
         "disclosure only started from FY2022) - the FY2021 figures here are taken from the FY2022 Pillar 3 "
         "document's FY2021 comparative column instead, the only source where they appear.",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not disclosed" for y in YEARS})],
    p3_sources(),
    note="No MREL disclosure found in any of the 5 available Pillar 3 documents (FY2021-FY2025).",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 2274441, "FY2024": 2323319, "FY2023": 2079373, "FY2022": 2290593, "FY2021": 2151180}),
        ("Loans and advances to customers", {"FY2025": 810985, "FY2024": 941507, "FY2023": 990763, "FY2022": 1122459, "FY2021": 1194653}),
        ("Deposits from customers", {"FY2025": 1304816, "FY2024": 1355529, "FY2023": 1223068, "FY2022": 1291150, "FY2021": 1333523}),
        ("Total shareholders' equity", {"FY2025": 399013, "FY2024": 413744, "FY2023": 433289, "FY2022": 401893, "FY2021": 306776}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total income", {"FY2025": 188290, "FY2024": 187263, "FY2023": 206185, "FY2022": 150380, "FY2021": 124048}),
        ("Staff costs", {"FY2025": -86079, "FY2024": -72194, "FY2023": -68058, "FY2022": -59208, "FY2021": -50154}),
        ("Profit for the year", {"FY2025": 68931, "FY2024": 83917, "FY2023": 103213, "FY2022": 68564, "FY2021": 31478}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 413744, "FY2024": 433289, "FY2023": 401893, "FY2022": 306776, "FY2021": 342164}),
        ("Total comprehensive income", {"FY2025": 69011, "FY2024": 83917, "FY2023": 103211, "FY2022": 68576, "FY2021": 31612}),
        ("Other movements, net (AT1 issued / dividends)", {"FY2025": -83662, "FY2024": -103462, "FY2023": -71815, "FY2022": 26541, "FY2021": -67000}),
        ("Closing equity", {"FY2025": 399013, "FY2024": 413744, "FY2023": 433289, "FY2022": 401893, "FY2021": 306776}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash generated from operating activities", {"FY2025": 111252, "FY2024": 405091, "FY2023": 233292, "FY2022": 22570, "FY2021": 304294}),
        ("Net cash from/(used in) investing activities", {"FY2025": -2623, "FY2024": -25826, "FY2023": -74896, "FY2022": -47511, "FY2021": -1147}),
        ("Net cash used in financing activities", {"FY2025": -84086, "FY2024": -103953, "FY2023": -71862, "FY2022": -33536, "FY2021": -68393}),
        ("Cash and cash equivalents at end of period", {"FY2025": 1073402, "FY2024": 1048859, "FY2023": 773547, "FY2022": 657656, "FY2021": 716133}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "27.2%", "FY2024": "24.8%", "FY2023": "26.8%", "FY2022": "23.4%", "FY2021": "24.6%"}),
        ("Tier 1 Ratio", {"FY2025": "33.2%", "FY2024": "30.2%", "FY2023": "32.7%", "FY2022": "28.5%", "FY2021": "24.6%"}),
        ("Total Capital Ratio", {"FY2025": "33.2%", "FY2024": "30.2%", "FY2023": "32.7%", "FY2022": "28.5%", "FY2021": "29.9%"}),
        ("Leverage Ratio", {"FY2025": "24.4%", "FY2024": "22.9%", "FY2023": "22.7%", "FY2022": "18.5%", "FY2021": "11.3%"}),
        ("LCR", {"FY2025": "324.1%", "FY2024": "372.5%", "FY2023": "387.3%", "FY2022": "182.0%", "FY2021": "179.0%"}),
        ("NSFR", {"FY2025": "194.4%", "FY2024": "216.5%", "FY2023": "134.5%", "FY2022": "121.0%", "FY2021": "151.3%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. See the Cash Flow Statement sheet's source note for "
         "a disclosed restatement gap between FY2022's and FY2023's own reports.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BANK OF CHINA UK FINANCIALS.xlsx")
