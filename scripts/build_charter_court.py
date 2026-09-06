import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

BASE = "https://find-and-update.company-information.service.gov.uk/company/06749498/filing-history"
AR2025_URL = BASE + "/MzUxNjgzMTY2OWFkaXF6a2N4/document?format=pdf&download=0"  # filed 23 Apr 2026, covers FY2025/FY2024
AR2024_URL = BASE + "/MzQ2MzY3MjYwMmFkaXF6a2N4/document?format=pdf&download=0"  # filed 23 Apr 2025, covers FY2024/FY2023
AR2023_URL = BASE + "/MzQxOTgyMzYzMWFkaXF6a2N4/document?format=pdf&download=0"  # filed 30 Apr 2024, covers FY2023/FY2022
AR2022_URL = BASE + "/MzM3NjA1NDU0NWFkaXF6a2N4/document?format=pdf&download=0"  # filed 18 Apr 2023, covers FY2022/FY2021
AR2021_URL = BASE + "/MzMzNTQwMDY5MWFkaXF6a2N4/document?format=pdf&download=0"  # filed 07 Apr 2022, covers FY2021/FY2020

ENTITY_NOTE = (
    "Charter Court Financial Services Limited (company 06749498) trades under the Charter "
    "Savings Bank, Precise Mortgages and Exact Mortgage Experts brands - a UK specialist "
    "mortgage lender. Its parent was CCFSG Holdings Limited (formerly Charter Court Financial "
    "Services Group PLC, merged with OneSavings Bank plc in 2019) until 22 September 2025, when "
    "the Company was transferred directly to OneSavings Bank plc; the ultimate parent throughout "
    "is OSB GROUP PLC. All 5 Companies House filings used were fully scanned/image-only, "
    "transcribed via page rendering. Each year's own originally-published Statement of Cash "
    "Flows is used as that year's column (not a later restated comparative) - the full chain "
    "ties exactly (each year's closing balance = the next year's opening balance) across all 5 "
    "years. FY2022's own Annual Report discloses a voluntary restatement of its FY2021 "
    "comparative (reclassifying £73.3m of cash collateral/margin on interest rate swaps from "
    "financing to operating activities, plus a presentation gross-up of fair-value-hedge and "
    "derivative movements) - FY2021's own originally-published figures are used here regardless, "
    "per this project's convention, so this workbook's FY2021 column will not tie to the "
    "restated FY2021 comparative shown in the FY2022 report."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Charter Court Financial Services Limited's own Statement of Cash "
    "Flows, from each year's own originally-filed Companies House accounts (not a later "
    "restated comparative):\n"
    f"FY2025: Full accounts made up to 31 Dec 2025, p.69 (Statement of Cash Flows) - {AR2025_URL}\n"
    f"FY2024: Full accounts made up to 31 Dec 2024, p.68 (Statement of Cash Flows) - {AR2024_URL}\n"
    f"FY2023: Full accounts made up to 31 Dec 2023, p.56 (Statement of Cash Flows) - {AR2023_URL}\n"
    f"FY2022: Full accounts made up to 31 Dec 2022, p.50 (Statement of Cash Flows) - {AR2022_URL}\n"
    f"FY2021: Full accounts made up to 31 Dec 2021, p.51 (Statement of Cash Flows) - {AR2021_URL}\n"
    + ENTITY_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - Charter Court Financial Services Limited's own Strategic Report narrative "
        "(no standalone Pillar 3 document or KM1 template found at this entity level; the "
        "Directors' Report explicitly refers readers to \"the OSBG annual report and accounts\" "
        "for further capital/risk detail):\n"
        f"FY2025/FY2024: Full accounts to 31 Dec 2025, p.44 (KPIs table, CET1 only) - {AR2025_URL}\n"
        f"FY2023/FY2022: Full accounts to 31 Dec 2023, p.19 (Solvency Risk narrative) - {AR2023_URL}\n"
        + ("\n" + extra if extra else "")
    )


bw = BankWorkbook(bank_name="Charter Court Financial Services Limited", years=YEARS, year_label=YEAR_LABEL, header_color="C83584")

STATEMENTS_SOURCES = (
    "Sources - Charter Court Financial Services Limited's own Statement of Financial Position / "
    "Statement of Comprehensive Income / Statement of Changes in Equity, from each year's own "
    "originally-filed Companies House accounts (not a later restated comparative):\n"
    f"FY2025: Full accounts made up to 31 Dec 2025, pp.66-68 - {AR2025_URL}\n"
    f"FY2024: Full accounts made up to 31 Dec 2025, pp.66-68 (FY2024 own comparative column) - {AR2025_URL}\n"
    f"FY2023: Full accounts made up to 31 Dec 2023, pp.53-55 - {AR2023_URL}\n"
    f"FY2022: Full accounts made up to 31 Dec 2023, pp.53-55 (FY2022 own comparative column) - {AR2023_URL}\n"
    f"FY2021: Full accounts made up to 31 Dec 2021, pp.48-50 - {AR2021_URL}\n"
    + ENTITY_NOTE
    + "\n\nPRESENTATION NOTE: FY2025's equity statement shows two separate 'Coupon paid on AT1 "
    "securities' rows in the same year (one nil, one -£4.0m) because the AT1 instrument in issue "
    "changed mid-year - the old AT1 was redeemed (-£53.3m total, of which -£53.2m against Other "
    "equity instruments and -£0.1m against Retained earnings) and a new one issued (+£60.0m gross, "
    "less £0.5m transaction costs), reconciling to the cash flow statement's narrower 'Issuance of "
    "AT1 securities' (£59.5m net of costs) and 'Redemption of AT1 securities' (-£53.3m) lines - not "
    "an error, both rows are reproduced as the Company's own source table shows them. FY2021's "
    "equity statement uses a differently-labelled 'Additional Tier 1 securities' column (vs FY2022+'s "
    "'Other equity instruments') for the same underlying instrument, issued that year (+£60.0m)."
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Loans and advances to credit institutions", {"FY2025": 2890.4, "FY2024": 2081.5, "FY2023": 1570.0, "FY2022": 1632.0, "FY2021": 1269.1}),
    ("DATA", "Investment securities", {"FY2025": 1181.3, "FY2024": 905.7, "FY2023": 225.5, "FY2022": 202.3, "FY2021": 477.8}),
    ("DATA", "Loans and advances to customers", {"FY2025": 9346.1, "FY2024": 9785.5, "FY2023": 11229.3, "FY2022": 10260.9, "FY2021": 8789.3}),
    ("DATA", "Fair value adjustments on hedged assets", {"FY2025": 6.0, "FY2024": -79.0, "FY2023": -151.7, "FY2022": -375.5, "FY2021": -68.4}),
    ("DATA", "Derivative assets", {"FY2025": 22.8, "FY2024": 84.1, "FY2023": 234.0, "FY2022": 447.2, "FY2021": 86.9}),
    ("DATA", "Other assets", {"FY2025": 7.5, "FY2024": 4.7, "FY2023": 9.2, "FY2022": 3.8, "FY2021": 4.5}),
    ("DATA", "Current taxation asset", {"FY2025": 0.8, "FY2024": 9.7, "FY2023": 7.4, "FY2022": 0.1, "FY2021": 0.4}),
    ("DATA", "Deferred taxation asset", {"FY2025": 0, "FY2024": 0.7, "FY2023": 4.0, "FY2022": 5.2}),
    ("DATA", "Property, plant and equipment", {"FY2025": 2.1, "FY2024": 4.2, "FY2023": 5.7, "FY2022": 7.1, "FY2021": 8.1}),
    ("DATA", "Intangible assets", {"FY2025": 0, "FY2024": 0.4, "FY2023": 1.4, "FY2022": 2.9, "FY2021": 4.2}),
    ("TOTAL", "Total assets", {"FY2025": 13457.0, "FY2024": 12797.5, "FY2023": 13134.8, "FY2022": 12186.0, "FY2021": 10571.9}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Amounts owed to credit institutions", {"FY2025": 801.7, "FY2024": 311.6, "FY2023": 1556.7, "FY2022": 2524.3, "FY2021": 1900.8}),
    ("DATA", "Amounts owed to retail depositors", {"FY2025": 10162.8, "FY2024": 10294.9, "FY2023": 9880.1, "FY2022": 8623.1, "FY2021": 7785.4}),
    ("DATA", "Fair value adjustments on hedged liabilities", {"FY2025": -0.3, "FY2024": -3.8, "FY2023": 10.1, "FY2022": -20.7, "FY2021": -8.6}),
    ("DATA", "Amounts owed to other customers", {"FY2025": 458.5, "FY2024": 104.9, "FY2023": 62.8, "FY2022": 112.6, "FY2021": 86.8}),
    ("DATA", "Derivative liabilities", {"FY2025": 43.2, "FY2024": 26.2, "FY2023": 75.9, "FY2022": 42.8, "FY2021": 11.3}),
    ("DATA", "Lease liabilities", {"FY2025": 1.7, "FY2024": 3.6, "FY2023": 4.5, "FY2022": 5.2, "FY2021": 5.6}),
    ("DATA", "Other liabilities", {"FY2025": 7.6, "FY2024": 15.4, "FY2023": 31.4, "FY2022": 4.6, "FY2021": 5.5}),
    ("DATA", "Provisions", {"FY2025": 0, "FY2024": 0.3, "FY2023": 0.1, "FY2022": 0, "FY2021": 0.1}),
    ("DATA", "Deferred taxation liability", {"FY2025": 0.1, "FY2021": 4.4}),
    ("DATA", "Deemed loan liability", {"FY2025": 930.8, "FY2024": 855.3, "FY2023": 501.5, "FY2022": 0}),
    ("DATA", "Senior notes", {"FY2025": 176.9, "FY2024": 259.3, "FY2023": 82.4, "FY2022": 0}),
    ("DATA", "Subordinated liabilities", {"FY2025": 104.3, "FY2024": 104.3, "FY2023": 104.3, "FY2022": 0}),
    ("TOTAL", "Total liabilities", {"FY2025": 12687.3, "FY2024": 11972.0, "FY2023": 12309.8, "FY2022": 11291.9, "FY2021": 9791.3}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 2.9, "FY2024": 2.9, "FY2023": 2.9, "FY2022": 2.9, "FY2021": 2.9}),
    ("DATA", "Share premium", {"FY2025": 67.3, "FY2024": 67.3, "FY2023": 67.3, "FY2022": 67.3, "FY2021": 67.3}),
    ("DATA", "FVOCI reserve", {"FY2025": -1.0, "FY2024": -2.6, "FY2023": -1.1, "FY2022": 16.6, "FY2021": 18.5}),
    ("DATA", "Other equity instruments / AT1 securities", {"FY2025": 66.8, "FY2024": 60.0, "FY2023": 60.0, "FY2022": 60.0, "FY2021": 60.0}),
    ("DATA", "Retained earnings", {"FY2025": 633.7, "FY2024": 697.9, "FY2023": 695.9, "FY2022": 747.3, "FY2021": 631.9}),
    ("TOTAL", "Total equity", {"FY2025": 769.7, "FY2024": 825.5, "FY2023": 825.0, "FY2022": 894.1, "FY2021": 780.6}),
    ("TOTAL", "Total equity and liabilities", {"FY2025": 13457.0, "FY2024": 12797.5, "FY2023": 13134.8, "FY2022": 12186.0, "FY2021": 10571.9}),
]

bw.add_balance_sheet_sheet(
    title="Charter Court Financial Services Limited — Balance Sheet",
    subtitle="Entity (Company) basis, £m. See source note at bottom.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=90,
    source_height=340,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable and similar income", {"FY2025": 784.4, "FY2024": 922.6, "FY2023": 731.9, "FY2022": 465.3, "FY2021": 300.8}),
    ("DATA", "Interest payable and similar charges", {"FY2025": -527.0, "FY2024": -635.6, "FY2023": -498.7, "FY2022": -161.8, "FY2021": -70.8}),
    ("TOTAL", "Net interest income", {"FY2025": 257.4, "FY2024": 287.0, "FY2023": 233.2, "FY2022": 303.5, "FY2021": 230.0}),
    ("DATA", "Fair value (losses)/gains on financial instruments", {"FY2025": -7.1, "FY2024": 2.9, "FY2023": -20.3, "FY2022": 42.2, "FY2021": 11.9}),
    ("DATA", "Gain/(loss) on sale of financial instruments/assets", {"FY2025": -1.2, "FY2021": 2.4}),
    ("DATA", "Other operating income", {"FY2025": 5.2, "FY2024": 3.3, "FY2023": 1.4, "FY2022": 2.2, "FY2021": 1.6}),
    ("TOTAL", "Total income", {"FY2025": 254.3, "FY2024": 290.8, "FY2023": 214.3, "FY2022": 347.9, "FY2021": 245.9}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Administrative expenses", {"FY2025": -108.5, "FY2024": -109.3, "FY2023": -101.9, "FY2022": -75.2, "FY2021": -65.7}),
    ("DATA", "Decrease/(increase) in provisions", {"FY2025": 0, "FY2024": 0.1, "FY2023": -0.1, "FY2021": 0.1}),
    ("DATA", "Impairment of financial assets / credit to impairment", {"FY2025": 3.4, "FY2024": 9.6, "FY2023": -7.0, "FY2022": -8.6, "FY2021": 8.1}),
    ("DATA", "Integration costs", {"FY2023": 0, "FY2022": -0.8, "FY2021": -1.0}),
    ("TOTAL", "Profit before taxation", {"FY2025": 149.2, "FY2024": 191.2, "FY2023": 105.3, "FY2022": 263.3, "FY2021": 187.4}),
    ("DATA", "Taxation", {"FY2025": -39.4, "FY2024": -50.7, "FY2023": -28.2, "FY2022": -69.1, "FY2021": -49.5}),
    ("TOTAL", "Profit for the year", {"FY2025": 109.8, "FY2024": 140.5, "FY2023": 77.1, "FY2022": 194.2, "FY2021": 137.9}),
    ("SECTION", "Other comprehensive income/(expense)", {}),
    ("DATA", "Fair value changes on debt instruments at FVOCI, arising in the year", {"FY2025": 2.3, "FY2024": 2.1, "FY2023": -16.4, "FY2022": -11.4, "FY2021": 16.9}),
    ("DATA", "Tax on items in other comprehensive income/(expense)", {"FY2025": -0.7, "FY2024": -3.6, "FY2023": -1.3, "FY2022": 9.5, "FY2021": -0.8}),
    ("TOTAL", "Other comprehensive income/(expense)", {"FY2025": 1.6, "FY2024": -1.5, "FY2023": -17.7, "FY2022": -1.9, "FY2021": 16.1}),
    ("TOTAL", "Total comprehensive income for the year", {"FY2025": 111.4, "FY2024": 139.0, "FY2023": 59.4, "FY2022": 192.3, "FY2021": 154.0}),
]

bw.add_income_statement_sheet(
    title="Charter Court Financial Services Limited — Profit & Loss",
    subtitle="Entity (Company) basis, £m. Results derived wholly from continuing operations. See source note at bottom.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=90,
    source_height=340,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
equity_headers = ["Share capital", "Share premium", "FVOCI reserve", "Other equity instruments / AT1", "Retained earnings", "Total"]
equity_rows = [
    ("TOTAL", "At 1 January 2021 (=31 Dec 2020)", (2.9, 67.3, 15.2, None, 421.2, 506.6)),
    ("DATA", "Profit for the year", (None, None, None, None, 137.9, 137.9)),
    ("DATA", "Other comprehensive income", (None, None, 16.9, None, None, 16.9)),
    ("DATA", "Tax recognised in equity", (None, None, -0.8, None, None, -0.8)),
    ("DATA", "Issuance of Additional Tier 1 securities", (None, None, None, 60.0, None, 60.0)),
    ("TOTAL", "At 31 December 2021", (2.9, 67.3, 18.5, 60.0, 631.9, 780.6)),
    ("DATA", "Profit for the year", (None, None, None, None, 194.2, 194.2)),
    ("DATA", "Other comprehensive expense", (None, None, -11.4, None, None, -11.4)),
    ("DATA", "Tax recognised in equity", (None, None, 9.5, None, None, 9.5)),
    ("DATA", "Coupon paid on Additional Tier 1 (AT1) securities", (None, None, None, None, -3.6, -3.6)),
    ("DATA", "Dividends paid", (None, None, None, None, -75.2, -75.2)),
    ("TOTAL", "At 31 December 2022", (2.9, 67.3, 16.6, 60.0, 747.3, 894.1)),
    ("DATA", "Profit for the year", (None, None, None, None, 77.1, 77.1)),
    ("DATA", "Other comprehensive expense", (None, None, -16.4, None, None, -16.4)),
    ("DATA", "Tax recognised in equity", (None, None, -1.3, None, None, -1.3)),
    ("DATA", "Coupon paid on AT1 securities", (None, None, None, None, -3.6, -3.6)),
    ("DATA", "Dividends paid", (None, None, None, None, -124.9, -124.9)),
    ("TOTAL", "At 31 December 2023", (2.9, 67.3, -1.1, 60.0, 695.9, 825.0)),
    ("DATA", "Profit for the year", (None, None, None, None, 140.5, 140.5)),
    ("DATA", "Other comprehensive income", (None, None, 2.1, None, None, 2.1)),
    ("DATA", "Tax recognised in equity", (None, None, -3.6, None, None, -3.6)),
    ("DATA", "Coupon paid on Additional Tier 1 (AT1) securities", (None, None, None, None, -3.6, -3.6)),
    ("DATA", "Dividends paid", (None, None, None, None, -134.9, -134.9)),
    ("TOTAL", "At 31 December 2024", (2.9, 67.3, -2.6, 60.0, 697.9, 825.5)),
    ("DATA", "Profit for the year", (None, None, None, None, 109.8, 109.8)),
    ("DATA", "Other comprehensive income", (None, None, 2.3, None, None, 2.3)),
    ("DATA", "Tax recognised in equity", (None, None, -0.7, None, None, -0.7)),
    ("DATA", "Coupon paid on AT1 securities (old instrument, nil in year)", (None, None, None, None, None, None)),
    ("DATA", "Redemption of AT1 securities", (None, None, None, -53.2, -0.1, -53.3)),
    ("DATA", "Issuance of AT1 securities", (None, None, None, 60.0, None, 60.0)),
    ("DATA", "Transaction costs on issuance of AT1 securities", (None, None, None, None, -0.5, -0.5)),
    ("DATA", "Coupon paid on AT1 securities (new instrument)", (None, None, None, None, -4.0, -4.0)),
    ("DATA", "Dividends paid", (None, None, None, None, -169.4, -169.4)),
    ("TOTAL", "At 31 December 2025", (2.9, 67.3, -1.0, 66.8, 633.7, 769.7)),
]

bw.add_equity_changes_sheet(
    title="Charter Court Financial Services Limited — Statement of Changes in Equity",
    subtitle="Entity (Company) basis, £m, chronological (oldest to newest). See source note at bottom.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=58,
    source_height=340,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before taxation", {"FY2025": 149.2, "FY2024": 191.2, "FY2023": 105.3, "FY2022": 263.3, "FY2021": 187.4}),
    ("DATA", "Adjustments for non-cash and other items", {"FY2025": 26.6, "FY2024": 93.9, "FY2023": 117.7, "FY2022": -1.1, "FY2021": 127.1}),
    ("DATA", "Changes in operating assets and liabilities", {"FY2025": 581.9, "FY2024": 1103.6, "FY2023": 92.0, "FY2022": -388.0, "FY2021": -254.9}),
    ("TOTAL", "Cash generated from/(used in) operating activities", {"FY2025": 757.7, "FY2024": 1388.7, "FY2023": 315.0, "FY2022": -125.8, "FY2021": 59.6}),
    ("DATA", "Provisions paid", {"FY2025": -0.3}),
    ("DATA", "Net tax paid", {"FY2025": -40.0, "FY2024": -53.3, "FY2023": -35.9, "FY2022": -69.3, "FY2021": -47.1}),
    ("TOTAL", "Net cash generated from/(used in) operating activities", {"FY2025": 717.4, "FY2024": 1335.4, "FY2023": 279.1, "FY2022": -195.1, "FY2021": 12.5}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Sales of loans and advances to customers", {"FY2021": 0}),
    ("DATA", "Maturity and sales of investment securities", {"FY2025": 256.3, "FY2024": 360.3, "FY2023": 49.5, "FY2022": 215.3, "FY2021": 535.8}),
    ("DATA", "Purchases of investment securities", {"FY2025": -526.9, "FY2024": -251.4, "FY2023": -72.2, "FY2022": -40.2, "FY2021": -452.5}),
    ("DATA", "Interest received on investment securities", {"FY2025": 51.3, "FY2024": 18.3, "FY2023": 11.8, "FY2022": 5.1}),
    ("DATA", "Purchases of property, plant and equipment and intangible assets", {"FY2025": -0.1, "FY2024": -0.2, "FY2023": -0.1, "FY2022": -0.6, "FY2021": -1.8}),
    ("TOTAL", "Net cash from investing activities", {"FY2025": -219.4, "FY2024": 127.0, "FY2023": -11.0, "FY2022": 179.6, "FY2021": 81.5}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Financing received", {"FY2025": 1174.2, "FY2024": 1170.9, "FY2023": 731.3, "FY2022": 309.5, "FY2021": 1899.5}),
    ("DATA", "Financing repaid", {"FY2025": -644.1, "FY2024": -1777.5, "FY2023": -804.9, "FY2022": -2.5, "FY2021": -1667.9}),
    ("DATA", "Interest paid on financing", {"FY2025": -64.3, "FY2024": -127.1, "FY2023": -92.2, "FY2022": -15.4, "FY2021": -1.8}),
    ("DATA", "Coupon paid on AT1 securities", {"FY2024": -3.6, "FY2023": -3.6, "FY2022": -3.6}),
    ("DATA", "Redemption of AT1 securities", {"FY2025": -53.3}),
    ("DATA", "Issuance of AT1 securities", {"FY2025": 59.5, "FY2021": 60.0}),
    ("DATA", "Dividends paid", {"FY2025": -169.4, "FY2024": -134.9, "FY2023": -124.9, "FY2022": -75.2}),
    ("DATA", "Net swap interest paid on subordinated liabilities and senior notes", {"FY2024": -2.3}),
    ("DATA", "Net swap interest paid on structural hedge", {"FY2024": -1.2}),
    ("DATA", "Repayments of principal portion of lease liabilities", {"FY2025": -7.6, "FY2024": -0.9, "FY2023": -1.0, "FY2022": -1.0, "FY2021": -1.0}),
    ("TOTAL", "Net cash from/(used in) financing activities", {"FY2025": 295.0, "FY2024": -876.6, "FY2023": -295.3, "FY2022": 211.8, "FY2021": 288.8}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 793.0, "FY2024": 585.8, "FY2023": -27.2, "FY2022": 196.3, "FY2021": 382.8}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {"FY2025": 2037.8, "FY2024": 1452.0, "FY2023": 1479.2, "FY2022": 1282.9, "FY2021": 900.1}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2025": 2830.8, "FY2024": 2037.8, "FY2023": 1452.0, "FY2022": 1479.2, "FY2021": 1282.9}),
]

bw.add_cash_flow_sheet(
    title="Charter Court Financial Services Limited — Statement of Cash Flows",
    subtitle="Entity (Company) basis, £m. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=280,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
ASSET_QUALITY_SOURCES = (
    "Sources - Note 'Loans and advances to customers' and Note 'Expected credit losses' (residential "
    "mortgages held at amortised cost only - the FVOCI-held mortgage book, a smaller separate "
    "portfolio, uses a different loss-recognition basis and is excluded here for consistency), £m:\n"
    f"FY2025/FY2024: Full accounts made up to 31 Dec 2025, pp.97,99 (Notes 15-16) - {AR2025_URL}\n"
    f"FY2023/FY2022: Full accounts made up to 31 Dec 2023, pp.82,87 (Notes 15-16) - {AR2023_URL}\n"
    f"FY2021: Full accounts made up to 31 Dec 2021, pp.79,83 (Notes 16-17) - {AR2021_URL}\n"
    + ENTITY_NOTE
    + "\n\nRatios calculated here from the disclosed stage-level figures (not separately stated by the "
    "Company): NPL ratio = (Stage 3 + Stage 3 POCI) gross / Total gross; Stage 3 coverage = Stage 3 "
    "ECL / Stage 3 gross (POCI excluded from the coverage denominator, consistent with how Stage 3 "
    "coverage is conventionally calculated across this project); Total coverage = Total ECL / Total "
    "gross."
)

asset_quality_rows = [
    ("SECTION", "Gross carrying amount by IFRS 9 stage (held at amortised cost)", {}),
    ("DATA", "Stage 1", {"FY2025": 7316.6, "FY2024": 7043.3, "FY2023": 8435.4, "FY2022": 7319.8, "FY2021": 6570.3}),
    ("DATA", "Stage 2", {"FY2025": 1580.5, "FY2024": 2121.4, "FY2023": 2129.8, "FY2022": 2053.4, "FY2021": 1157.5}),
    ("DATA", "Stage 3", {"FY2025": 301.6, "FY2024": 298.2, "FY2023": 216.1, "FY2022": 162.7, "FY2021": 114.8}),
    ("DATA", "Stage 3 (POCI)", {"FY2025": 0.3, "FY2024": 0.5, "FY2023": 1.1, "FY2022": 1.0, "FY2021": 1.3}),
    ("TOTAL", "Total gross carrying amount", {"FY2025": 9199.0, "FY2024": 9463.4, "FY2023": 10782.4, "FY2022": 9536.9, "FY2021": 7843.9}),
    ("SECTION", "Expected credit loss (ECL) provision by stage", {}),
    ("DATA", "Stage 1", {"FY2025": 1.1, "FY2024": 1.9, "FY2023": 6.1, "FY2022": 1.2, "FY2021": 2.4}),
    ("DATA", "Stage 2", {"FY2025": 5.1, "FY2024": 9.4, "FY2023": 15.8, "FY2022": 15.8, "FY2021": 10.2}),
    ("DATA", "Stage 3", {"FY2025": 12.6, "FY2024": 13.7, "FY2023": 12.6, "FY2022": 9.2, "FY2021": 5.2}),
    ("DATA", "Stage 3 (POCI)", {"FY2025": 0, "FY2024": 0.1, "FY2023": 0, "FY2022": 0.1, "FY2021": 0.1}),
    ("TOTAL", "Total ECL provision", {"FY2025": 18.8, "FY2024": 25.1, "FY2023": 34.5, "FY2022": 26.3, "FY2021": 17.9}),
    ("TOTAL", "Net carrying amount (Total gross - Total ECL)", {"FY2025": 9180.2, "FY2024": 9438.3, "FY2023": 10747.9, "FY2022": 9510.6, "FY2021": 7826.0}),
    ("SECTION", "Asset quality ratios", {}),
    ("DATA", "Total coverage ratio (Total ECL / Total gross)", {"FY2025": "0.20%", "FY2024": "0.27%", "FY2023": "0.32%", "FY2022": "0.28%", "FY2021": "0.23%"}),
    ("DATA", "NPL ratio ((Stage 3 + POCI) gross / Total gross)", {"FY2025": "3.28%", "FY2024": "3.16%", "FY2023": "2.01%", "FY2022": "1.72%", "FY2021": "1.48%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 ECL / Stage 3 gross)", {"FY2025": "4.18%", "FY2024": "4.59%", "FY2023": "5.83%", "FY2022": "5.65%", "FY2021": "4.53%"}),
]

bw.add_asset_quality_sheet(
    title="Charter Court Financial Services Limited — Asset Quality",
    subtitle="Entity (Company) basis, £m (ratios as calculated). See source note at bottom.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=88,
    source_height=280,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
NOT_DISCLOSED_NOTE = (
    "Not publicly disclosed at the Charter Court Financial Services Limited entity level in any "
    "of the 5 Annual Reports reviewed - the Directors' Report explicitly defers to \"the OSBG "
    "annual report and accounts\" for further capital/risk detail, and no standalone Pillar 3 "
    "document or KM1 template for this entity was found."
)


def metric(name, unit, rows_data, note=None, extra_source=""):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(extra_source), note=note, first_col_width=44, source_height=150)


# Sheet order matches the project-wide standard: CET1 Capital, CET1 Ratio, Tier 1
# Capital, Tier 1 Ratio, Total Capital, Total Capital Ratio, Total RWAs, Leverage
# Ratio, LCR, NSFR, MREL Ratio - even though this entity only discloses 3 of them.
bw.add_not_disclosed_metric_sheets(
    ["CET1 Capital"], p3_sources(), per_note={"CET1 Capital": NOT_DISCLOSED_NOTE},
)

metric(
    "CET1 Ratio", "%",
    [("Common Equity Tier 1 (CET1) ratio, under CRD IV", {"FY2025": "16.2%", "FY2024": "17.8%", "FY2023": "15.8%", "FY2022": "18.8%"})],
    note="FY2025/FY2024 from the Annual Report's own KPI table (FY2024 shown as that report's own "
         "comparative). FY2023 from the Strategic Report's own Solvency Risk narrative (FY2022 shown "
         "as that report's own comparative). FY2021 not located within this build's research budget - "
         "left blank rather than guessed, not confirmed absent.",
)

bw.add_not_disclosed_metric_sheets(
    ["Tier 1 Capital", "Tier 1 Ratio"], p3_sources(),
    per_note={"Tier 1 Capital": NOT_DISCLOSED_NOTE, "Tier 1 Ratio": NOT_DISCLOSED_NOTE},
)

bw.add_not_disclosed_metric_sheets(
    ["Total Capital"], p3_sources(), per_note={"Total Capital": NOT_DISCLOSED_NOTE},
)

metric(
    "Total Capital Ratio", "%",
    [("Total capital ratio, under CRD IV", {"FY2023": "19.2%", "FY2022": "20.2%"})],
    note=NOT_DISCLOSED_NOTE + " FY2023/FY2022 are the exception, from the Strategic Report's own "
         "Solvency Risk narrative (FY2022 shown as FY2023's report's own comparative). FY2025/FY2024/"
         "FY2021 not found - the later KPI table format only carries CET1, and FY2021 wasn't located "
         "within this build's research budget.",
)

bw.add_not_disclosed_metric_sheets(
    ["Total RWAs"], p3_sources(), per_note={"Total RWAs": NOT_DISCLOSED_NOTE},
)

bw.add_rwa_breakdown_sheet(
    title="Charter Court Financial Services Limited — RWA Breakdown",
    subtitle="Not publicly disclosed. See source note at bottom.",
    rows=[("DATA", "Not publicly disclosed", {})],
    sources_text=p3_sources() + "\n\n" + NOT_DISCLOSED_NOTE,
    first_col_width=54,
    source_height=280,
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio, under CRD IV", {"FY2023": "6.9%", "FY2022": "7.9%"})],
    note=NOT_DISCLOSED_NOTE + " FY2023/FY2022 are the exception, from the Strategic Report's own "
         "Solvency Risk narrative (FY2022 shown as FY2023's report's own comparative). FY2025/FY2024/"
         "FY2021 not found within this build's research budget.",
)

bw.add_not_disclosed_metric_sheets(
    ["LCR", "NSFR", "MREL Ratio"], p3_sources(),
    per_note={m: NOT_DISCLOSED_NOTE for m in ["LCR", "NSFR", "MREL Ratio"]},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 13457.0, "FY2024": 12797.5, "FY2023": 13134.8, "FY2022": 12186.0, "FY2021": 10571.9}),
        ("Loans and advances to customers", {"FY2025": 9346.1, "FY2024": 9785.5, "FY2023": 11229.3, "FY2022": 10260.9, "FY2021": 8789.3}),
        ("Amounts owed to retail depositors", {"FY2025": 10162.8, "FY2024": 10294.9, "FY2023": 9880.1, "FY2022": 8623.1, "FY2021": 7785.4}),
        ("Total equity", {"FY2025": 769.7, "FY2024": 825.5, "FY2023": 825.0, "FY2022": 894.1, "FY2021": 780.6}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total income", {"FY2025": 254.3, "FY2024": 290.8, "FY2023": 214.3, "FY2022": 347.9, "FY2021": 245.9}),
        ("Administrative expenses", {"FY2025": -108.5, "FY2024": -109.3, "FY2023": -101.9, "FY2022": -75.2, "FY2021": -65.7}),
        ("Profit for the year", {"FY2025": 109.8, "FY2024": 140.5, "FY2023": 77.1, "FY2022": 194.2, "FY2021": 137.9}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 825.5, "FY2024": 825.0, "FY2023": 894.1, "FY2022": 780.6}),
        ("Total comprehensive income for the year", {"FY2025": 111.4, "FY2024": 139.0, "FY2023": 59.4, "FY2022": 192.3, "FY2021": 154.0}),
        ("Other equity movements, net", {"FY2025": -167.2, "FY2024": -138.5, "FY2023": -128.5, "FY2022": -78.8}),
        ("Closing equity", {"FY2025": 769.7, "FY2024": 825.5, "FY2023": 825.0, "FY2022": 894.1, "FY2021": 780.6}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 717.4, "FY2024": 1335.4, "FY2023": 279.1, "FY2022": -195.1, "FY2021": 12.5}),
        ("Net cash from investing activities", {"FY2025": -219.4, "FY2024": 127.0, "FY2023": -11.0, "FY2022": 179.6, "FY2021": 81.5}),
        ("Net cash from/(used in) financing activities", {"FY2025": 295.0, "FY2024": -876.6, "FY2023": -295.3, "FY2022": 211.8, "FY2021": 288.8}),
        ("Cash and cash equivalents at end of year", {"FY2025": 2830.8, "FY2024": 2037.8, "FY2023": 1452.0, "FY2022": 1479.2, "FY2021": 1282.9}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "16.2%", "FY2024": "17.8%", "FY2023": "15.8%", "FY2022": "18.8%"}),
        ("Total Capital Ratio", {"FY2023": "19.2%", "FY2022": "20.2%"}),
        ("Leverage Ratio", {"FY2023": "6.9%", "FY2022": "7.9%"}),
    ],
    note="LCR/NSFR/MREL/Tier 1 metrics omitted from this chart - not disclosed at this entity level "
         "in any year (see the individual sheets). Figures are duplicated from the detail sheets for "
         "at-a-glance trend viewing; see each sheet's own source citation for the underlying "
         "document/page.",
)

bw.save("/Users/armaan/code/katalysis/banks/CHARTER COURT FINANCIAL SERVICES FINANCIALS.xlsx")
