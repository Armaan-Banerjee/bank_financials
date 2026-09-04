import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

# All 5 years sourced from Companies House filings (fully scanned/image-only,
# 0 text blocks per page) - the bank's registered site (www.kingdombank.co.uk)
# is an unrelated expired/parked domain; the real site is www.kingdom.bank.
CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/04346834/filing-history"
FY2025_URL = f"{CH_BASE}/MzUzMjA2MDkzOWFkaXF6a2N4/document?format=pdf&download=0"
FY2024_URL = f"{CH_BASE}/MzQ3Mjc3MDk4N2FkaXF6a2N4/document?format=pdf&download=0"
FY2023_URL = f"{CH_BASE}/MzQyNzk5NjY3OGFkaXF6a2N4/document?format=pdf&download=0"
FY2022_URL = f"{CH_BASE}/MzM3Nzc1Mzk0NWFkaXF6a2N4/document?format=pdf&download=0"
FY2021_URL = f"{CH_BASE}/MzM0MzYxNTEyM2FkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "Entity: Kingdom Bank Limited, company 04346834 (formerly Kingdom Banking Limited), FRN 400972 - "
    "confirmed via Banks List 2608.xlsx and Companies House, no identity ambiguity. A small specialist "
    "bank providing mortgages, savings and insurance broking to UK churches, Christian charities and "
    "individuals in Christian ministry; parent/ultimate controlling party is Lamb's Passage Holding "
    "Limited (LPHL), whose investor group includes Stewardship Services (UKET) Limited. Solo/Bank basis "
    "throughout - no group consolidation applies. All 5 years' filings on Companies House are fully "
    "scanned/image-only (0 extractable text on every page); the bank's registered-looking domain "
    "www.kingdombank.co.uk is an unrelated expired/parked domain (a GoDaddy-style parking page) - its "
    "real site is www.kingdom.bank, which hosts only the FY2025 Annual Report and no standalone Pillar 3 "
    "disclosures."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Kingdom Bank Limited's own Statement of cash flows, £'000, Bank/solo basis "
    "(Companies House filings, all fully scanned):\n"
    f"FY2025 (own) & FY2024 (comparative, cross-checked against FY2024's own report): Annual Report & "
    "Accounts 2025, p.38 (Statement of cash flows) - " + FY2025_URL + "\n"
    f"FY2024 (own): Annual Report & Accounts 2024 - " + FY2024_URL + "\n"
    f"FY2023 (own) & FY2022 (comparative): Annual Report & Accounts 2023, p.39 (Statement of cash flows) - " + FY2023_URL + "\n"
    f"FY2022 (own): Annual Report & Accounts 2022 - " + FY2022_URL + "\n"
    f"FY2021 (own) & FY2020 comparative (not used): Annual Report & Accounts 2021, p.33 (Statement of cash "
    "flows) - " + FY2021_URL + "\n"
    + ENTITY_NOTE + "\n"
    "Every year-end closing balance ties exactly to the following year's opening balance across all 5 years "
    "(FY2021 closing £20,030k = FY2022 opening; FY2022 closing £24,861k = FY2023 opening; FY2023 closing "
    "£35,058k = FY2024 opening; FY2024 closing £39,791k = FY2025 opening) - no restatements found."
)

STATEMENTS_SOURCES = (
    "Sources - Kingdom Bank Limited's own Statement of financial position / Income statement / Statement of "
    "changes in equity, £'000, Bank/solo basis (Companies House filings, all fully scanned/image-only):\n"
    f"FY2025 & FY2024: Annual Report & Accounts 2025, p.35 (Income statement), p.36 (Statement of financial "
    "position), p.37 (Statement of changes in equity) - " + FY2025_URL + "\n"
    f"FY2024 (own): Annual Report & Accounts 2024 - " + FY2024_URL + "\n"
    f"FY2023 & FY2022: Annual Report & Accounts 2023, p.36 (Income statement), p.37 (Statement of financial "
    "position), p.38 (Statement of changes in equity) - " + FY2023_URL + "\n"
    f"FY2022 (own): Annual Report & Accounts 2022, p.40 (Income statement), p.42 (Statement of financial "
    "position) - " + FY2022_URL + "\n"
    f"FY2021: Annual Report & Accounts 2021, p.29 (Income statement), p.31 (Statement of financial position), "
    "p.32 (Statement of changes in equity) - " + FY2021_URL + "\n"
    + ENTITY_NOTE + "\n"
    "PRESENTATION NOTES: (1) FY2021-FY2022 do not disclose separate 'Prepayments and accrued income' or "
    "'Accruals and deferred income' lines - FY2021/FY2022's own 'Other assets' and 'Other liabilities' totals "
    "bundle what FY2023 onward splits into two lines each; each year's own labelling is followed as published, "
    "not forced into a common template. (2) FY2021's income statement includes a one-off 'Profit on sale of "
    "investment property' line (£634k) and used the subtotal label 'Operating income' rather than 'Total net "
    "income' (introduced from FY2023) - same calculation, different label. (3) FY2021's own equity statement "
    "carried a £172k Revaluation reserve (from a historical operating-property revaluation) that was "
    "transferred to the Profit and loss account and fully extinguished during FY2021 upon reclassification of "
    "that property - a genuine one-off equity movement, not a plug. (4) FY2021's loan-book note used the label "
    "'Charity mortgages' where FY2022 onward uses 'Organisational mortgages' for the same category, and "
    "FY2021/FY2020 additionally had a small 'Fully secured lending to other group companies' sub-category "
    "(nil in FY2021, £269k in FY2020) not present from FY2022 onward."
)

ASSET_QUALITY_SOURCES = (
    "Sources - Kingdom Bank Limited's own Note 12 'Loans and advances to customers' (Advances to customers by "
    "product, part a; Loan loss provision movement, part c), £'000, Bank/solo basis (Companies House filings, "
    "all fully scanned/image-only):\n"
    f"FY2025 & FY2024: Annual Report & Accounts 2025, p.51-52 - " + FY2025_URL + "\n"
    f"FY2024 (own): Annual Report & Accounts 2024 - " + FY2024_URL + "\n"
    f"FY2023 & FY2022: Annual Report & Accounts 2023, p.53-54 - " + FY2023_URL + "\n"
    f"FY2022 (own): Annual Report & Accounts 2022 - " + FY2022_URL + "\n"
    f"FY2021: Annual Report & Accounts 2021, p.48-49 - " + FY2021_URL + "\n"
    + ENTITY_NOTE + "\n"
    "No IFRS 9 stage (1/2/3) split is disclosed in any year - this entity applies FRS 102, not IFRS 9, and "
    "reports a single collective/IBNR loan loss provision instead; the 'Of which collective/IBNR provision' "
    "split shown here (where disclosed) is the closest equivalent breakdown. FY2021's own note does not "
    "disclose an IBNR sub-split at all (introduced from FY2022 onward) - left blank for FY2021, not assumed "
    "zero."
)


def p3_sources():
    return (
        "Sources - Kingdom Bank Limited, Bank/solo basis, £'000 (from each year's own audited Statement of "
        "financial position and Strategic Report):\n"
        f"FY2025 & FY2024: Annual Report & Accounts 2025, p.10 (Capital) and p.36 (Statement of financial "
        "position) - " + FY2025_URL + "\n"
        f"FY2023 & FY2022: Annual Report & Accounts 2023, p.10 (Capital) and p.37 (Statement of financial "
        "position) - " + FY2023_URL + "\n"
        f"FY2021: Annual Report & Accounts 2021, p.31 (Statement of financial position) - " + FY2021_URL + "\n"
        + "No standalone Pillar 3/KM1 disclosure document was found on the bank's own site (www.kingdom.bank) "
        "or via Companies House - each Annual Report's 'Capital' section states only that 'the Bank's "
        "regulatory capital consists of shareholders' funds (\"Core Equity Tier 1\") and subordinated "
        "liabilities (\"Tier 2\")' with £m totals, and no year discloses Total RWAs or any capital/liquidity "
        "ratio (%) figure. This is consistent with the PRA's Small Domestic Deposit Taker (SDDT) thin-"
        "disclosure pattern already seen at Cynergy Bank Plc/DF Capital Bank Limited in this project."
    )


NOT_DISCLOSED_NOTE = (
    "Not publicly disclosed. Kingdom Bank's Annual Reports state only narrative £m totals for shareholders' "
    "funds (CET1) and subordinated liabilities (Tier 2) in the 'Capital' section of the Strategic Report - "
    "no Total RWAs or any capital/liquidity ratio (%) figure is given in any of the 5 years reviewed, and no "
    "standalone Pillar 3 document exists on the bank's own site or via Companies House. See the CET1 "
    "Capital/Total Capital sheets' source note for the SDDT-regime context that plausibly explains this."
)

TIER1_NOTE = (
    "Kingdom Bank's own Annual Reports state regulatory capital consists only of shareholders' funds "
    "(\"Core Equity Tier 1\") and subordinated liabilities (\"Tier 2\") - no Additional Tier 1 instruments "
    "are in issue in any year reviewed, so Tier 1 Capital equals CET1 Capital exactly. See the CET1 Capital "
    "sheet for the same figures and source."
)

RWA_NOT_DISCLOSED_NOTE = (
    "Not publicly disclosed. No Total RWAs figure is disclosed by Kingdom Bank in any of the 5 years "
    "reviewed (see the Total RWAs sheet's source note), so no RWA-by-risk-category breakdown exists either - "
    "no standalone Pillar 3 document was located on the bank's own site or via Companies House."
)

bw = BankWorkbook(bank_name="Kingdom Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="7A1F2B")

# ---------------------------------------------------------------
# Sheet 1: Balance Sheet - built first per the equity reconciliation
# ladder so each year's own Total equity is an independent check value.
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 38497, "FY2024": 38548, "FY2023": 34064, "FY2022": 23032, "FY2021": 10087}),
    ("DATA", "Loans and advances to banks", {"FY2025": 1217, "FY2024": 1243, "FY2023": 994, "FY2022": 1829, "FY2021": 10795}),
    ("DATA", "Loans and advances to customers", {"FY2025": 118242, "FY2024": 97733, "FY2023": 77532, "FY2022": 63291, "FY2021": 53795}),
    ("DATA", "Investment property", {"FY2025": 650}),
    ("DATA", "Intangible fixed assets", {"FY2025": 18, "FY2024": 39, "FY2023": 75, "FY2022": 76, "FY2021": 83}),
    ("DATA", "Tangible fixed assets", {"FY2025": 171, "FY2024": 174, "FY2023": 192, "FY2022": 230, "FY2021": 268}),
    ("DATA", "Other assets", {"FY2025": 23, "FY2024": 63, "FY2023": 37, "FY2022": 481, "FY2021": 347}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 1056, "FY2024": 662, "FY2023": 571}),
    ("DATA", "Deferred tax assets", {"FY2025": 297, "FY2024": 30, "FY2023": 44, "FY2022": 83, "FY2021": 166}),
    ("TOTAL", "Total assets", {"FY2025": 160171, "FY2024": 138492, "FY2023": 113509, "FY2022": 89022, "FY2021": 75541}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer accounts", {"FY2025": 141758, "FY2024": 121269, "FY2023": 102091, "FY2022": 78452, "FY2021": 66668}),
    ("DATA", "Other liabilities", {"FY2025": 616, "FY2024": 448, "FY2023": 438, "FY2022": 517, "FY2021": 661}),
    ("DATA", "Accruals and deferred income", {"FY2025": 1289, "FY2024": 563, "FY2023": 404}),
    ("DATA", "Subordinated liabilities", {"FY2025": 700, "FY2024": 700, "FY2023": 700, "FY2022": 700, "FY2021": 761}),
    ("TOTAL", "Total liabilities", {"FY2025": 144363, "FY2024": 122980, "FY2023": 103633, "FY2022": 79669, "FY2021": 68090}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 13237, "FY2024": 12067, "FY2023": 6667, "FY2022": 6667, "FY2021": 4867}),
    ("DATA", "Profit and loss account", {"FY2025": 2571, "FY2024": 3445, "FY2023": 3209, "FY2022": 2686, "FY2021": 2584}),
    ("TOTAL", "Total shareholders' funds", {"FY2025": 15808, "FY2024": 15512, "FY2023": 9876, "FY2022": 9353, "FY2021": 7451}),
    ("TOTAL", "Total liabilities and total shareholders' funds", {"FY2025": 160171, "FY2024": 138492, "FY2023": 113509, "FY2022": 89022, "FY2021": 75541}),
]

bw.add_balance_sheet_sheet(
    title="Kingdom Bank Limited — Balance Sheet",
    subtitle="Statement of financial position, Bank/solo basis, £'000. See source note at bottom.",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=320,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet 2: Profit & Loss
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable", {"FY2025": 8637, "FY2024": 7828, "FY2023": 6003, "FY2022": 3144, "FY2021": 2419}),
    ("DATA", "Interest payable", {"FY2025": -2942, "FY2024": -3207, "FY2023": -2193, "FY2022": -454, "FY2021": -345}),
    ("TOTAL", "Net interest income", {"FY2025": 5695, "FY2024": 4621, "FY2023": 3810, "FY2022": 2690, "FY2021": 2074}),
    ("DATA", "Insurance commission income", {"FY2025": 666, "FY2024": 576, "FY2023": 543, "FY2022": 482, "FY2021": 419}),
    ("DATA", "Other operating income", {"FY2025": 43, "FY2024": 8, "FY2023": 7, "FY2022": 3, "FY2021": 117}),
    ("TOTAL", "Total net income (FY2021-FY2022's own equivalent subtotal is labelled 'Operating income' - same calculation)",
     {"FY2025": 6404, "FY2024": 5205, "FY2023": 4360, "FY2022": 3175, "FY2021": 2610}),
    ("DATA", "Administrative expenses", {"FY2025": -7241, "FY2024": -4776, "FY2023": -3597, "FY2022": -2953, "FY2021": -2437}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -67, "FY2024": -79, "FY2023": -86, "FY2022": -85, "FY2021": -80}),
    ("DATA", "Profit on sale of investment property", {"FY2022": 0, "FY2021": 634}),
    ("DATA", "Movement in loan loss provision", {"FY2025": -158, "FY2024": -9, "FY2023": -12, "FY2022": -9, "FY2021": -24}),
    ("TOTAL", "(Loss)/profit on ordinary activities before taxation", {"FY2025": -1062, "FY2024": 341, "FY2023": 665, "FY2022": 128, "FY2021": 703}),
    ("DATA", "Tax credit/(charge) on (loss)/profit", {"FY2025": 258, "FY2024": -62, "FY2023": -142, "FY2022": -26, "FY2021": -23}),
    ("TOTAL", "(Loss)/profit and total comprehensive income for the financial year", {"FY2025": -804, "FY2024": 279, "FY2023": 523, "FY2022": 102, "FY2021": 680}),
]

bw.add_income_statement_sheet(
    title="Kingdom Bank Limited — Profit & Loss",
    subtitle="Income statement, Bank/solo basis, £'000. All results arise from continuing operations, attributable to the "
              "owners of the Bank, every year. See source note at bottom.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=90,
    source_height=320,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet 3: Statement of Changes in Equity - per-year reconciliation
# ladder confirmed: every year's own closing balance ties exactly to
# both the next year's own opening balance and that year's own Balance
# Sheet Total shareholders' funds. Zero plug rows needed anywhere
# across all 5 years. Ladder's mandated scan caught one genuine
# easy-to-skip movement: FY2021's Revaluation reserve transfer.
# ---------------------------------------------------------------
equity_headers = ["Called up share capital", "Profit and loss account", "Revaluation reserve", "Total shareholders' funds"]
equity_rows = [
    ("TOTAL", "Balance as at 1 January 2021", (4867, 1732, 172, 6771)),
    ("DATA", "Profit for the financial year", (None, 680, None, 680)),
    ("DATA", "Transfer of revaluation reserve to profit and loss reserve upon reclassification of operating property", (None, 172, -172, None)),
    ("TOTAL", "Balance as at 31 December 2021 (FY2021 closing)", (4867, 2584, 0, 7451)),
    ("DATA", "Profit for the financial year", (None, 102, None, 102)),
    ("DATA", "Share allotment", (1800, None, None, 1800)),
    ("TOTAL", "Balance as at 31 December 2022 (FY2022 closing)", (6667, 2686, 0, 9353)),
    ("DATA", "Profit for the financial year", (None, 523, None, 523)),
    ("TOTAL", "Balance as at 31 December 2023 (FY2023 closing)", (6667, 3209, 0, 9876)),
    ("DATA", "Profit for the financial year", (None, 279, None, 279)),
    ("DATA", "Share allotment", (5400, None, None, 5400)),
    ("DATA", "Dividends paid", (None, -43, None, -43)),
    ("TOTAL", "Balance as at 31 December 2024 (FY2024 closing)", (12067, 3445, 0, 15512)),
    ("DATA", "Loss for the financial year", (None, -804, None, -804)),
    ("DATA", "Share allotment", (1170, None, None, 1170)),
    ("DATA", "Dividends paid", (None, -70, None, -70)),
    ("TOTAL", "Balance as at 31 December 2025 (FY2025 closing)", (13237, 2571, 0, 15808)),
]

bw.add_equity_changes_sheet(
    title="Kingdom Bank Limited — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest. Equity reconciliation ladder confirmed: every year's own "
              "closing balance ties exactly to both the next year's own opening balance and that year's own Balance "
              "Sheet Total shareholders' funds - zero plug rows needed anywhere across all 5 years. £'000. The "
              "Revaluation reserve column is fully extinguished from FY2021 onward (see FY2021's transfer row) and "
              "shown as 0, not blank, for FY2022-FY2025 to make the reconciliation explicit.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
)

# ---------------------------------------------------------------
# Sheet 4: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Net cash (used in)/generated from operating activities excluding tax", {"FY2025": -1079, "FY2024": -481, "FY2023": 10255, "FY2022": 3157, "FY2021": -630}),
    ("DATA", "Taxation paid", {"FY2025": -55, "FY2024": -102, "FY2023": -11, "FY2022": -25}),
    ("TOTAL", "Net cash (used in)/generated from operating activities", {"FY2025": -1134, "FY2024": -583, "FY2023": 10244, "FY2022": 3132, "FY2021": -630}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of intangible assets", {"FY2025": 0, "FY2024": 0, "FY2023": -23, "FY2022": -16, "FY2021": -47}),
    ("DATA", "Purchase of tangible assets", {"FY2025": -43, "FY2024": -41, "FY2023": -24, "FY2022": -24, "FY2021": -197}),
    ("DATA", "Sale of investment property", {"FY2021": 2013}),
    ("TOTAL", "Net cash (used in)/generated from investing activities", {"FY2025": -43, "FY2024": -41, "FY2023": -47, "FY2022": -40, "FY2021": 1769}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Repayment of subordinated liabilities", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": -61, "FY2021": -670}),
    ("DATA", "Share allotment", {"FY2025": 1170, "FY2024": 5400, "FY2023": 0, "FY2022": 1800, "FY2021": 0}),
    ("DATA", "Dividends paid", {"FY2025": -70, "FY2024": -43}),
    ("TOTAL", "Net cash generated from/(used in) financing activities", {"FY2025": 1100, "FY2024": 5357, "FY2023": 0, "FY2022": 1739, "FY2021": -670}),
    ("TOTAL", "Net movement in cash and cash equivalents", {"FY2025": -77, "FY2024": 4733, "FY2023": 10197, "FY2022": 4831, "FY2021": 469}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {"FY2025": 39791, "FY2024": 35058, "FY2023": 24861, "FY2022": 20030, "FY2021": 19561}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2025": 39714, "FY2024": 39791, "FY2023": 35058, "FY2022": 24861, "FY2021": 20030}),
]

bw.add_cash_flow_sheet(
    title="Kingdom Bank Limited — Statement of Cash Flows",
    subtitle="Bank/solo basis, £'000. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=68,
    source_height=200,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet 5: Asset Quality - loan book by product (Note 12a) plus loan
# loss provision movement, incl. collective/IBNR split where disclosed
# (Note 12c). No IFRS 9 stage split exists - FRS 102 entity, not IFRS 9.
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, gross", {}),
    ("DATA", "Organisational/Charity mortgages (FY2021's own label: 'Charity mortgages')", {"FY2025": 98455, "FY2024": 79806, "FY2023": 60628, "FY2022": 48320, "FY2021": 42846}),
    ("DATA", "Personal mortgages", {"FY2025": 19897, "FY2024": 18049, "FY2023": 17017, "FY2022": 15086, "FY2021": 11063}),
    ("DATA", "Fully secured lending to other group companies (FY2021/FY2020 only)", {"FY2021": 0}),
    ("DATA", "Unsecured personal loans", {"FY2025": 89, "FY2024": 72, "FY2023": 72, "FY2022": 58, "FY2021": 50}),
    ("TOTAL", "Gross advances to customers", {"FY2025": 118441, "FY2024": 97927, "FY2023": 77717, "FY2022": 63464, "FY2021": 53959}),
    ("DATA", "Less: loan loss provision", {"FY2025": -199, "FY2024": -194, "FY2023": -185, "FY2022": -173, "FY2021": -164}),
    ("TOTAL", "Net advances to customers", {"FY2025": 118242, "FY2024": 97733, "FY2023": 77532, "FY2022": 63291, "FY2021": 53795}),
    ("DATA", "Loan loss provision coverage (% of gross advances)", {
        "FY2025": "0.17%", "FY2024": "0.20%", "FY2023": "0.24%", "FY2022": "0.27%", "FY2021": "0.30%",
    }),
    ("SECTION", "Loan loss provision movement (Note 12c)", {}),
    ("DATA", "Balance at 1 January", {"FY2025": 194, "FY2024": 185, "FY2023": 173, "FY2022": 164, "FY2021": 324}),
    ("DATA", "Charge for the year", {"FY2025": 160, "FY2024": 11, "FY2023": 13, "FY2022": 10, "FY2021": 26}),
    ("DATA", "Utilised during the year", {"FY2025": -153, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": -184}),
    ("DATA", "Released during the year", {"FY2025": -2, "FY2024": -2, "FY2023": -1, "FY2022": -1, "FY2021": -2}),
    ("TOTAL", "Balance at 31 December", {"FY2025": 199, "FY2024": 194, "FY2023": 185, "FY2022": 173, "FY2021": 164}),
    ("DATA", "Of which: collective/IBNR provision (not disclosed for FY2021 - sub-split introduced FY2022 onward)",
     {"FY2025": 156, "FY2024": 148, "FY2023": 137, "FY2022": 124}),
]

bw.add_asset_quality_sheet(
    title="Kingdom Bank Limited — Asset Quality",
    subtitle="Loan book by product (Note 12a) and loan loss provision movement (Note 12c), Bank/solo basis, £'000. No "
              "IFRS 9 stage 1/2/3 split is disclosed in any year - this entity applies FRS 102, not IFRS 9. See source "
              "note at bottom.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=100,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------

def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, f"Bank/solo basis, {unit}" if unit else "Bank/solo basis",
                         rows_data, p3_sources(), note=note, first_col_width=52, source_height=190)


CET1_VALUES = {"FY2025": 15808, "FY2024": 15512, "FY2023": 9876, "FY2022": 9353, "FY2021": 7451}
TIER2_VALUES = {"FY2025": 700, "FY2024": 700, "FY2023": 700, "FY2022": 700, "FY2021": 761}
TOTAL_CAPITAL_VALUES = {y: CET1_VALUES[y] + TIER2_VALUES[y] for y in YEARS}

metric(
    "CET1 Capital", "£'000",
    [("Shareholders' funds (Core Equity Tier 1)", CET1_VALUES)],
)

bw.add_not_disclosed_metric_sheets(
    ["CET1 Ratio"], p3_sources(), per_note={"CET1 Ratio": NOT_DISCLOSED_NOTE},
)

metric(
    "Tier 1 Capital", "£'000",
    [("Shareholders' funds (Core Equity Tier 1)", CET1_VALUES)],
    note=TIER1_NOTE,
)

bw.add_not_disclosed_metric_sheets(
    ["Tier 1 Ratio"], p3_sources(), per_note={"Tier 1 Ratio": NOT_DISCLOSED_NOTE},
)

metric(
    "Total Capital", "£'000",
    [
        ("Shareholders' funds (Core Equity Tier 1)", CET1_VALUES),
        ("Subordinated liabilities (Tier 2)", TIER2_VALUES),
        ("Total regulatory capital (CET1 + Tier 2)", TOTAL_CAPITAL_VALUES),
    ],
)

bw.add_not_disclosed_metric_sheets(
    ["Total Capital Ratio", "Total RWAs"],
    p3_sources(),
    per_note={m: NOT_DISCLOSED_NOTE for m in ["Total Capital Ratio", "Total RWAs"]},
)

# RWA Breakdown - placed immediately after Total RWAs, before Leverage
# Ratio, per the locked sheet order. Not publicly disclosed (no RWA
# figure exists in any form for this bank - see Total RWAs sheet).
bw.add_rwa_breakdown_sheet(
    title="Kingdom Bank Limited — RWA Breakdown",
    subtitle="Bank/solo basis. Not publicly disclosed - see source note.",
    rows=[("DATA", "Not publicly disclosed", {})],
    sources_text=p3_sources() + "\n\n" + RWA_NOT_DISCLOSED_NOTE,
    first_col_width=54,
    source_height=190,
)

bw.add_not_disclosed_metric_sheets(
    ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"],
    p3_sources(),
    per_note={m: NOT_DISCLOSED_NOTE for m in ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"]},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 160171, "FY2024": 138492, "FY2023": 113509, "FY2022": 89022, "FY2021": 75541}),
        ("Loans and advances to customers", {"FY2025": 118242, "FY2024": 97733, "FY2023": 77532, "FY2022": 63291, "FY2021": 53795}),
        ("Customer accounts", {"FY2025": 141758, "FY2024": 121269, "FY2023": 102091, "FY2022": 78452, "FY2021": 66668}),
        ("Total shareholders' funds", {"FY2025": 15808, "FY2024": 15512, "FY2023": 9876, "FY2022": 9353, "FY2021": 7451}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total net income", {"FY2025": 6404, "FY2024": 5205, "FY2023": 4360, "FY2022": 3175, "FY2021": 2610}),
        ("Administrative expenses", {"FY2025": -7241, "FY2024": -4776, "FY2023": -3597, "FY2022": -2953, "FY2021": -2437}),
        ("(Loss)/profit for the financial year", {"FY2025": -804, "FY2024": 279, "FY2023": 523, "FY2022": 102, "FY2021": 680}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening total shareholders' funds", {"FY2025": 15512, "FY2024": 9876, "FY2023": 9353, "FY2022": 7451, "FY2021": 6771}),
        ("(Loss)/profit for the financial year", {"FY2025": -804, "FY2024": 279, "FY2023": 523, "FY2022": 102, "FY2021": 680}),
        ("Other equity movements, net", {"FY2025": 1100, "FY2024": 5357, "FY2023": 0, "FY2022": 1800, "FY2021": 0}),
        ("Closing total shareholders' funds", {"FY2025": 15808, "FY2024": 15512, "FY2023": 9876, "FY2022": 9353, "FY2021": 7451}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash flow from/(used in) operating activities", {"FY2025": -1134, "FY2024": -583, "FY2023": 10244, "FY2022": 3132, "FY2021": -630}),
        ("Net cash flow from/(used in) investing activities", {"FY2025": -43, "FY2024": -41, "FY2023": -47, "FY2022": -40, "FY2021": 1769}),
        ("Net cash flow from/(used in) financing activities", {"FY2025": 1100, "FY2024": 5357, "FY2023": 0, "FY2022": 1739, "FY2021": -670}),
        ("Cash and cash equivalents at end of year", {"FY2025": 39714, "FY2024": 39791, "FY2023": 35058, "FY2022": 24861, "FY2021": 20030}),
    ],
    cash_flow_unit="£'000",
    ratios=[],
    note="No Pillar 3 ratio-type metrics (CET1/Tier 1/Total Capital Ratio, Leverage Ratio, LCR, NSFR, MREL "
         "Ratio) or Total RWAs are disclosed by Kingdom Bank in any of the 5 years reviewed, so no ratios "
         "chart is shown here - see each individual Pillar 3 sheet. CET1 Capital, Tier 1 Capital and Total "
         "Capital (£'000) are disclosed for all 5 years on their own sheets. Balance Sheet, Profit & Loss, "
         "Statement of Changes in Equity and Cash Flow figures are duplicated from their own sheets for "
         "at-a-glance trend viewing - how the bank is using its money (steady growth in loans and advances to "
         "churches/charities/individuals, funded by customer deposits) and the risk it is taking with it (a "
         "small, consistently sub-0.3%-of-gross-advances loan loss provision).",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/KINGDOM BANK FINANCIALS.xlsx")
