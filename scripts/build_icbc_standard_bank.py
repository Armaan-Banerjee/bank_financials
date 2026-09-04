import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first

AR25_URL = "https://v.icbc.com.cn/userfiles/resources/icbc/haiwai/standardbank/download/2023/consolidatedannualreport2025.pdf"
AR23_URL = "https://v.icbc.com.cn/userfiles/resources/icbc/haiwai/standardbank/download/2023/2023annualreportyasuo.pdf"
AR21_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/StandardBank/Download/2022/Consolidated_Annual_Report_2021.pdf"

P3_25_URL = "https://v.icbc.com.cn/userfiles/resources/icbc/haiwai/standardbank/download/2023/2025pillar3disclosures.pdf"
P3_23_URL = "https://v.icbc.com.cn/userfiles/resources/icbc/haiwai/standardbank/download/2023/2023pillar3.pdf"
P3_21_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/StandardBank/Download/2022/2021_Pillar_3_document.pdf"

CASH_FLOW_SOURCES = (
    "Sources — all figures are ICBC Standard Bank Plc consolidated (Group) statement of cash flows, $m:\n"
    f"FY2025 & FY2024: ICBC Standard Bank Consolidated Annual Report 2025, p.68 (Consolidated Statement of Cash Flows) — {AR25_URL}\n"
    f"FY2023 & FY2022: ICBC Standard Bank Consolidated Annual Report 2023, p.65 (11. Consolidated statement of cash flows) — {AR23_URL}\n"
    f"FY2021: ICBC Standard Bank Consolidated Annual Report 2021, p.65 (10. Consolidated statement of cash flows) — {AR21_URL}\n"
    "Note: presentation granularity changed across report vintages. FY2025/FY2024 report a single 'Non-cash items "
    "included in profit before tax' adjustment and disclose interest received/paid only in a footnote; FY2023/FY2022 "
    "separately reconcile 'Net interest income' and show 'Interest received'/'Interest paid' as distinct lines within "
    "operating activities; FY2021 additionally itemises several one-off non-cash adjustments (equity-settled share-based "
    "payments, impairments, restructuring/commodity-inventory provisions) not repeated in later years. Blank cells "
    "indicate that year's report did not disclose that specific line; all section totals (cash flows from operating/"
    "investing/financing activities, and cash and cash equivalents at start/end of year) reconcile exactly year-on-year "
    "across all 5 years."
)

def p3_sources(page_25="5", page_23="5", page_21_capital="23", page_21_leverage="87", page_21_lcr="28"):
    return (
        "Sources — ICBC Standard Bank Plc (ICBCS Group) consolidated (Pillar 3) basis:\n"
        f"FY2025 & FY2024: ICBC Standard Bank Pillar 3 Disclosures 2025, p.{page_25} (UK KM1 - Key metrics template) — {P3_25_URL}\n"
        f"FY2023 & FY2022: ICBC Standard Bank Pillar 3 Disclosures 2023, p.{page_23} (UK KM1 - Key metrics template) — {P3_23_URL}\n"
        f"FY2021: ICBC Standard Bank Pillar 3 Disclosures 2021, p.{page_21_capital} (Table 5: ICBCS - Capital Resources), "
        f"p.{page_21_leverage} (Annex D: Leverage Ratio Common Disclosure Template), "
        f"p.{page_21_lcr} (Table 8: Average Consolidated Liquidity Coverage Ratio for ICBCS Group) — {P3_21_URL}"
    )

bw = BankWorkbook(bank_name="ICBC Standard Bank Plc", years=YEARS, header_color="C1272D")

STATEMENTS_ENTITY_NOTE = (
    "All figures are ICBC Standard Bank Plc consolidated (Group) basis, $m unless stated, each year's own "
    "originally-published figures (not a later restated comparative). ICBCS is jointly owned by Industrial and "
    "Commercial Bank of China Limited (60%) and Standard Bank Group Limited (40%)."
)

# ---------------------------------------------------------------
# Sheet 1: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances with central banks", {"FY2025": 764.5, "FY2024": 2674.1, "FY2023": 2635.9, "FY2022": 4856.1, "FY2021": 6056.5}),
    ("DATA", "Due from banks and other financial institutions", {"FY2025": 5438.2, "FY2024": 3727.2, "FY2023": 2248.4, "FY2022": 2182.3, "FY2021": 2306.7}),
    ("DATA", "Financial assets held for trading", {"FY2025": 1413.4, "FY2024": 1211.9, "FY2023": 1278.5, "FY2022": 702.7, "FY2021": 2455.7}),
    ("DATA", "Non-trading financial assets at fair value through profit or loss", {"FY2025": 1017.6, "FY2024": 689.0, "FY2023": 2856.6, "FY2022": 2193.7, "FY2021": 1972.1}),
    ("DATA", "Derivative financial assets", {"FY2025": 8686.4, "FY2024": 3911.2, "FY2023": 3383.2, "FY2022": 4968.0, "FY2021": 4392.1}),
    ("DATA", "Reverse repurchase agreements", {"FY2025": 4987.3, "FY2024": 3526.8, "FY2023": 2936.0, "FY2022": 2614.6, "FY2021": 2287.8}),
    ("DATA", "Loans and advances to customers", {"FY2025": 1828.0, "FY2024": 1303.0, "FY2023": 771.3, "FY2022": 818.6, "FY2021": 1608.7}),
    ("DATA", "Financial investments", {"FY2025": 3721.7, "FY2024": 3176.9, "FY2023": 2052.8, "FY2022": 1293.4, "FY2021": 925.5}),
    ("DATA", "Property and equipment", {"FY2025": 70.8, "FY2024": 70.3, "FY2023": 66.9, "FY2022": 34.6, "FY2021": 47.4}),
    ("DATA", "Current tax assets", {"FY2025": 10.9, "FY2024": 7.6, "FY2023": 11.8, "FY2022": 5.5, "FY2021": 3.5}),
    ("DATA", "Deferred tax assets", {"FY2025": 13.7, "FY2024": 13.3, "FY2023": 8.0, "FY2022": 0.6, "FY2021": 0.7}),
    ("DATA", "Other assets (incl. non-financial commodities inventory held for trading)", {"FY2025": 9848.2, "FY2024": 6289.1, "FY2023": 4997.7, "FY2022": 2957.2, "FY2021": 4211.8}),
    ("TOTAL", "Total assets", {"FY2025": 37800.7, "FY2024": 26600.4, "FY2023": 23247.1, "FY2022": 22627.3, "FY2021": 26268.5}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Financial liabilities held for trading", {"FY2025": 1876.9, "FY2024": 938.0, "FY2023": 1634.7, "FY2022": 1295.2, "FY2021": 1566.5}),
    ("DATA", "Non-trading financial liabilities at fair value through profit or loss", {"FY2025": 7342.6, "FY2024": 6975.3, "FY2023": 3744.0, "FY2022": 2951.2, "FY2021": 2099.9}),
    ("DATA", "Derivative financial liabilities", {"FY2025": 7368.4, "FY2024": 4194.9, "FY2023": 3782.3, "FY2022": 5352.8, "FY2021": 5050.7}),
    ("DATA", "Due to banks and other financial institutions", {"FY2025": 7761.1, "FY2024": 4731.3, "FY2023": 6553.2, "FY2022": 6221.9, "FY2021": 11646.5}),
    ("DATA", "Repurchase agreements", {"FY2025": 1079.1, "FY2024": 1080.4, "FY2023": 853.1, "FY2022": 530.1, "FY2021": 693.6}),
    ("DATA", "Due to customers", {"FY2025": 2386.8, "FY2024": 1431.0, "FY2023": 1077.1, "FY2022": 1736.5, "FY2021": 1235.8}),
    ("DATA", "Current tax liabilities", {"FY2025": 3.2, "FY2024": 0.8, "FY2023": 2.4, "FY2022": 3.5, "FY2021": 1.9}),
    ("DATA", "Subordinated debt", {"FY2025": 251.9, "FY2024": 248.6, "FY2023": 247.6, "FY2022": 245.4, "FY2021": 250.8}),
    ("DATA", "Other liabilities (incl. precious metal payables)", {"FY2025": 7599.3, "FY2024": 5056.4, "FY2023": 3481.8, "FY2022": 2608.7, "FY2021": 2352.8}),
    ("TOTAL", "Total liabilities", {"FY2025": 35669.3, "FY2024": 24656.7, "FY2023": 21376.2, "FY2022": 20945.3, "FY2021": 24898.5}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital (and share premium pre-FY2021 restructure)", {"FY2025": 1083.5, "FY2024": 1083.5, "FY2023": 1083.5, "FY2022": 1083.5, "FY2021": 1083.5}),
    ("DATA", "Other equity instruments", {"FY2025": 160.0, "FY2024": 160.0, "FY2023": 160.0, "FY2022": 160.0, "FY2021": 160.0}),
    ("DATA", "Reserves", {"FY2025": 887.9, "FY2024": 700.2, "FY2023": 627.4, "FY2022": 438.5, "FY2021": 126.5}),
    ("TOTAL", "Total equity (attributable to ordinary shareholders)", {"FY2025": 2131.4, "FY2024": 1943.7, "FY2023": 1870.9, "FY2022": 1682.0, "FY2021": 1370.0}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 37800.7, "FY2024": 26600.4, "FY2023": 23247.1, "FY2022": 22627.3, "FY2021": 26268.5}),
]

BALANCE_SHEET_SOURCES = (
    f"Sources — {STATEMENTS_ENTITY_NOTE}\n"
    f"FY2025 & FY2024: ICBC Standard Bank Consolidated Annual Report 2025, p.64 (Consolidated balance sheet) — {AR25_URL}\n"
    f"FY2023 & FY2022: ICBC Standard Bank Consolidated Annual Report 2023, p.61 (7. Consolidated balance sheet) — {AR23_URL}\n"
    f"FY2021: ICBC Standard Bank Consolidated Annual Report 2021, p.61 (6. Consolidated balance sheet) — {AR21_URL}\n"
    "Note: an 'Ordinary share premium' line ($996.0m at FY2020) was eliminated via a June 2021 share premium "
    "restructure (cancelled and transferred to retained earnings) - by FY2021 year-end onward, share capital and "
    "premium are a single, fully-merged line."
)

bw.add_balance_sheet_sheet(
    title="ICBC Standard Bank Plc — Consolidated Balance Sheet",
    subtitle="ICBC Standard Bank Group (consolidated basis), $m unless stated",
    rows=balance_sheet_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=68,
    source_height=110,
    unit_suffix=" ($m)",
)

# ---------------------------------------------------------------
# Sheet 2: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 730.8, "FY2024": 613.4, "FY2023": 524.7, "FY2022": 254.8, "FY2021": 135.1}),
    ("DATA", "Interest expense", {"FY2025": -482.7, "FY2024": -449.5, "FY2023": -370.8, "FY2022": -156.3, "FY2021": -23.1}),
    ("TOTAL", "Net interest income", {"FY2025": 248.1, "FY2024": 163.9, "FY2023": 153.9, "FY2022": 98.5, "FY2021": 112.0}),
    ("DATA", "Fees and commission income", {"FY2025": 81.3, "FY2024": 68.9, "FY2023": 65.7, "FY2022": 43.2, "FY2021": 52.0}),
    ("DATA", "Fees and commission expenses", {"FY2025": -27.1, "FY2024": -24.8, "FY2023": -27.1, "FY2022": -17.8, "FY2021": -19.1}),
    ("TOTAL", "Net fees and commission", {"FY2025": 54.2, "FY2024": 44.1, "FY2023": 38.6, "FY2022": 25.4, "FY2021": 32.9}),
    ("DATA", "Net trading revenue", {"FY2025": 351.7, "FY2024": 257.0, "FY2023": 314.0, "FY2022": 400.6, "FY2021": 260.6}),
    ("DATA", "Net gain on non-trading financial assets/liabilities at fair value through profit or loss", {"FY2025": 85.8, "FY2024": 107.1, "FY2023": 51.5, "FY2022": 51.7, "FY2021": 48.3}),
    ("DATA", "Recoveries/(losses) on commodity inventory intermediation", {"FY2022": 233.7, "FY2021": 8.8}),
    ("DATA", "Recoveries on commodity reverse repurchase agreements", {"FY2021": 3.4}),
    ("TOTAL", "Non-interest revenue", {"FY2025": 491.7, "FY2024": 408.2, "FY2023": 404.1, "FY2022": 711.4, "FY2021": 354.0}),
    ("TOTAL", "Total operating income", {"FY2025": 739.8, "FY2024": 572.1, "FY2023": 558.0, "FY2022": 809.9, "FY2021": 466.0}),
    ("DATA", "Credit impairment charges/(recoveries)", {"FY2025": -15.0, "FY2024": -2.7, "FY2023": 50.2, "FY2022": -60.8, "FY2021": 2.8}),
    ("TOTAL", "Income after credit impairments", {"FY2025": 724.8, "FY2024": 569.4, "FY2023": 608.2, "FY2022": 749.1, "FY2021": 468.8}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Staff costs", {"FY2025": -279.2, "FY2024": -248.5, "FY2023": -247.8, "FY2022": -223.9, "FY2021": -216.1}),
    ("DATA", "Other operating expenses", {"FY2025": -156.8, "FY2024": -130.8, "FY2023": -145.9, "FY2022": -147.9, "FY2021": -127.7}),
    ("DATA", "Restructuring costs and other impairments", {"FY2021": 1.4}),
    ("DATA", "Indirect taxation", {"FY2025": -7.9, "FY2024": -3.1, "FY2023": -3.9, "FY2022": -1.8, "FY2021": -5.7}),
    ("TOTAL", "Operating expenses", {"FY2025": -443.9, "FY2024": -382.4, "FY2023": -397.6, "FY2022": -373.6, "FY2021": -348.1}),
    ("TOTAL", "Profit before taxation", {"FY2025": 280.9, "FY2024": 187.0, "FY2023": 210.6, "FY2022": 375.5, "FY2021": 120.7}),
    ("DATA", "Income tax charge", {"FY2025": -56.0, "FY2024": -30.5, "FY2023": -23.5, "FY2022": -58.4, "FY2021": -22.1}),
    ("TOTAL", "Profit attributable to equity shareholders", {"FY2025": 224.9, "FY2024": 156.5, "FY2023": 187.1, "FY2022": 317.1, "FY2021": 98.6}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Foreign currency translation reserve", {"FY2025": 1.3, "FY2024": -0.7, "FY2023": -0.7, "FY2022": -2.6, "FY2021": 0.8}),
    ("DATA", "Cash flow hedging reserve, net", {"FY2025": 15.6, "FY2024": -22.8, "FY2023": 13.5, "FY2022": 13.1, "FY2021": -19.3}),
    ("DATA", "Changes in fair value of debt instruments measured at FVOCI", {"FY2025": 0.1, "FY2024": 0.9, "FY2023": 0.9, "FY2022": -2.5, "FY2021": 0.6}),
    ("DATA", "Gains/(losses) attributable to own credit risk", {"FY2025": 0.0, "FY2024": 1.0, "FY2023": 0.3, "FY2022": -0.9, "FY2021": -0.1}),
    ("TOTAL", "Other comprehensive income/(losses) for the year", {"FY2025": 17.0, "FY2024": -21.6, "FY2023": 14.0, "FY2022": 7.1, "FY2021": -17.9}),
    ("TOTAL", "Total comprehensive income attributable to equity shareholders", {"FY2025": 241.9, "FY2024": 134.9, "FY2023": 201.1, "FY2022": 324.2, "FY2021": 80.7}),
]

INCOME_STATEMENT_SOURCES = (
    f"Sources — {STATEMENTS_ENTITY_NOTE}\n"
    f"FY2025 & FY2024: ICBC Standard Bank Consolidated Annual Report 2025, p.65 (Consolidated income statement) and p.66 (Consolidated statement of comprehensive income) — {AR25_URL}\n"
    f"FY2023 & FY2022: ICBC Standard Bank Consolidated Annual Report 2023, p.62-63 (8-9. Consolidated income statement / statement of comprehensive income) — {AR23_URL}\n"
    f"FY2021: ICBC Standard Bank Consolidated Annual Report 2021, p.62-63 (7-8. Consolidated income statement / statement of comprehensive income) — {AR21_URL}\n"
    "Note: 'Recoveries/(losses) on commodity inventory intermediation' and 'Recoveries on commodity reverse "
    "repurchase agreements' are one-off lines that only appear in the FY2021/FY2022 income statement structure "
    "(and 'Restructuring costs and other impairments' only in FY2021) - blank cells indicate that year's report did "
    "not disclose that specific line, not a genuine zero. FY2021's 'Other comprehensive income/(losses) for the "
    "year' ($(17.9)m) is derived (Total comprehensive income less Profit for the year) since that year's report "
    "does not show an explicit OCI subtotal row - the disclosed OCI component lines sum to $(18.0)m, a $0.1m "
    "rounding difference reproduced as disclosed, not forced to match."
)

bw.add_income_statement_sheet(
    title="ICBC Standard Bank Plc — Consolidated Income Statement",
    subtitle="ICBC Standard Bank Group (consolidated basis), $m unless stated",
    rows=income_statement_rows,
    sources_text=INCOME_STATEMENT_SOURCES,
    first_col_width=76,
    source_height=130,
    unit_suffix=" ($m)",
)

# ---------------------------------------------------------------
# Sheet 3: Statement of Changes in Equity
# ---------------------------------------------------------------
EQUITY_HEADERS = [
    "Share capital (and premium pre-restructure)",
    "Other equity instruments",
    "Cash flow hedging reserve",
    "FVOCI reserve",
    "FX translation reserve",
    "Net investment hedge reserve",
    "Own credit reserve",
    "Retained earnings",
    "Total equity",
]

equity_rows = [
    ("TOTAL", "Balance at 1 January 2021 (FY2021's own opening)", (2079.5, 160.0, 14.2, 0.9, -0.7, -1.7, -0.3, -950.4, 1301.5)),
    ("DATA", "Total comprehensive gains/(losses) for the year", (None, None, -19.3, 0.6, 0.8, None, -0.1, 98.6, 80.7)),
    ("DATA", "Share premium restructure (cancellation of share premium, transferred to retained earnings)", (-996.0, None, None, None, None, None, None, 996.0, 0.0)),
    ("DATA", "Coupon payment on other equity instruments", (None, None, None, None, None, None, None, -12.2, -12.2)),
    ("TOTAL", "Balance at 31 December 2021 (FY2021 close = FY2022 opening)", (1083.5, 160.0, -5.1, 1.5, 0.1, -1.7, -0.4, 132.1, 1370.0)),
    ("DATA", "Total comprehensive gains/(losses) for the year", (None, None, 13.1, -2.5, -2.6, None, -0.9, 317.1, 324.2)),
    ("DATA", "Coupon payment on other equity instruments", (None, None, None, None, None, None, None, -12.2, -12.2)),
    ("TOTAL", "Balance at 31 December 2022 (FY2022 close = FY2023 opening)", (1083.5, 160.0, 8.0, -1.0, -2.5, -1.7, -1.3, 437.0, 1682.0)),
    ("DATA", "Total comprehensive gains/(losses) for the year", (None, None, 13.5, 0.9, -0.7, None, 0.3, 187.1, 201.1)),
    ("DATA", "Coupon payment on other equity instruments", (None, None, None, None, None, None, None, -12.2, -12.2)),
    ("TOTAL", "Balance at 31 December 2023 (FY2023 close = FY2024 opening)", (1083.5, 160.0, 21.5, -0.1, -3.2, -1.7, -1.0, 611.9, 1870.9)),
    ("DATA", "Total comprehensive gains/(losses) for the year", (None, None, -22.8, 0.9, -0.7, None, 1.0, 156.5, 134.9)),
    ("DATA", "Dividend payment on ordinary share capital", (None, None, None, None, None, None, None, -49.9, -49.9)),
    ("DATA", "Coupon payment on other equity instruments", (None, None, None, None, None, None, None, -12.2, -12.2)),
    ("TOTAL", "Balance at 31 December 2024 (FY2024 close = FY2025 opening)", (1083.5, 160.0, -1.3, 0.8, -3.9, -1.7, 0.0, 706.3, 1943.7)),
    ("DATA", "Total comprehensive gains for the year", (None, None, 15.6, 0.1, 1.3, None, 0.0, 224.9, 241.9)),
    ("DATA", "Dividend payment on ordinary share capital", (None, None, None, None, None, None, None, -41.8, -41.8)),
    ("DATA", "Coupon payment on other equity instruments", (None, None, None, None, None, None, None, -12.4, -12.4)),
    ("TOTAL", "Balance at 31 December 2025 (FY2025 close)", (1083.5, 160.0, 14.3, 0.9, -2.6, -1.7, 0.0, 877.0, 2131.4)),
]

EQUITY_SOURCES = (
    f"Sources — {STATEMENTS_ENTITY_NOTE}\n"
    f"FY2025 & FY2024 movements: ICBC Standard Bank Consolidated Annual Report 2025, p.67 (Consolidated statement of changes in shareholders' equity) — {AR25_URL}\n"
    f"FY2023 & FY2022 movements: ICBC Standard Bank Consolidated Annual Report 2023, p.64 (10. Consolidated statement of changes in shareholders' equity) — {AR23_URL}\n"
    f"FY2021 movements: ICBC Standard Bank Consolidated Annual Report 2021, p.64 (9. Consolidated statement of changes in shareholders' equity) — {AR21_URL}\n"
    "Reconciliation ladder confirmed: every year's own closing balance ties exactly to both the next year's own "
    "opening balance and that year's own Balance Sheet Total equity - zero plug rows needed anywhere across all "
    "5 years. The June 2021 share premium restructure (cancellation of the $996.0m share premium account, "
    "transferred to retained earnings) is shown as an explicit, net-zero movement row rather than absorbed "
    "silently. 'Own credit reserve' genuinely nets to $0.0m from FY2024 year-end onward (shown as '-' in the "
    "Bank's own tables), not a blank/inapplicable cell."
)

bw.add_equity_changes_sheet(
    title="ICBC Standard Bank Plc — Consolidated Statement of Changes in Equity",
    subtitle="ICBC Standard Bank Group (consolidated basis), $m, chronological roll-forward",
    headers=EQUITY_HEADERS,
    rows=equity_rows,
    sources_text=EQUITY_SOURCES,
    first_col_width=58,
    source_height=140,
)

# ---------------------------------------------------------------
# Sheet 4: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Reconciliation of profit before tax to net cash flows from operating activities", {}),
    ("DATA", "Profit before taxation", {"FY2025": 280.9, "FY2024": 187.0, "FY2023": 210.6, "FY2022": 375.5, "FY2021": 120.7}),
    ("DATA", "Non-cash items included in profit before tax (as reported)", {"FY2025": -4.5, "FY2024": -48.1}),
    ("DATA", "Net interest income (as reported)", {"FY2023": -153.9, "FY2022": -98.5, "FY2021": -112.0}),
    ("DATA", "Amortisation of intangible assets", {"FY2025": 6.5, "FY2024": 8.7, "FY2023": 9.6, "FY2022": 11.0, "FY2021": 11.2}),
    ("DATA", "Depreciation of property and equipment", {"FY2025": 12.5, "FY2024": 14.8, "FY2023": 17.5, "FY2022": 18.2, "FY2021": 17.9}),
    ("DATA", "Non-cash flow movements on fair value hedges", {"FY2025": 2.3, "FY2024": -2.8, "FY2023": -2.2, "FY2022": 0.9, "FY2021": 0}),
    ("DATA", "Incentive charges / cash-settled incentive payments", {"FY2025": 93.1, "FY2024": 69.4, "FY2023": 72.9, "FY2022": 64.6, "FY2021": 10.4}),
    ("DATA", "Equity-settled share-based payments", {"FY2021": -0.3}),
    ("DATA", "Net credit impairment charges/(recoveries)", {"FY2025": 15.0, "FY2024": 2.7, "FY2023": -50.2, "FY2022": 60.8, "FY2021": -2.8}),
    ("DATA", "Impairment of property and equipment", {"FY2021": -0.9}),
    ("DATA", "Impairment of intangible assets", {"FY2021": 0}),
    ("DATA", "Provisions for commodity inventory intermediation costs", {"FY2021": -7.0}),
    ("DATA", "Restructuring provisions", {"FY2021": -5.3}),
    ("DATA", "Provisions for leave pay", {"FY2025": -0.1, "FY2024": 0.3, "FY2023": 0.3, "FY2022": -1.4, "FY2021": -0.3}),
    ("TOTAL", "Subtotal after non-cash adjustments", {"FY2025": 405.7, "FY2024": 232.0, "FY2023": 104.6, "FY2022": 431.1, "FY2021": 31.6}),
    ("SECTION", "Changes in operating funds", {}),
    ("DATA", "(Increase)/decrease in income-earning assets", {"FY2025": -8294.0, "FY2024": -2780.4, "FY2023": -4382.4, "FY2022": 2981.5, "FY2021": 1974.8}),
    ("DATA", "Increase/(decrease) in interest bearing and non-interest bearing liabilities", {"FY2025": 6161.5, "FY2024": 2706.7, "FY2023": 1994.6, "FY2022": -4589.9, "FY2021": 154.2}),
    ("TOTAL", "Changes in operating funds (subtotal)", {"FY2025": -2132.5, "FY2024": -73.7, "FY2023": -2387.8, "FY2022": -1608.4, "FY2021": 2129.0}),
    ("DATA", "Interest received (as reported)", {"FY2023": 505.7, "FY2022": 244.1, "FY2021": 146.2}),
    ("DATA", "Interest paid (as reported)", {"FY2023": -336.2, "FY2022": -149.5, "FY2021": -24.0}),
    ("DATA", "Corporation and withholding tax paid", {"FY2025": -53.5, "FY2024": -30.2, "FY2023": -37.0, "FY2022": -54.6, "FY2021": -27.0}),
    ("TOTAL", "Cash flows (used in)/from operating activities", {"FY2025": -1780.3, "FY2024": 128.1, "FY2023": -2150.7, "FY2022": -1137.3, "FY2021": 2255.8}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Capital expenditure on intangible assets", {"FY2025": -5.0, "FY2024": -11.5, "FY2023": -5.1, "FY2022": -11.4, "FY2021": -9.4}),
    ("DATA", "Capital expenditure on property and equipment", {"FY2025": -13.0, "FY2024": -4.9, "FY2023": -1.8, "FY2022": -4.1, "FY2021": -3.1}),
    ("TOTAL", "Cash flows used in investing activities", {"FY2025": -18.0, "FY2024": -16.4, "FY2023": -6.9, "FY2022": -15.5, "FY2021": -12.5}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Proceeds from issuance of subordinated debt", {"FY2024": 100.0, "FY2022": 150.0}),
    ("DATA", "Repayment of subordinated debt", {"FY2024": -100.0, "FY2022": -150.0}),
    ("DATA", "Dividend payment on ordinary share capital", {"FY2025": -41.8, "FY2024": -49.9}),
    ("DATA", "Coupon payment on other equity instruments", {"FY2025": -12.4, "FY2024": -12.2, "FY2023": -12.2, "FY2022": -12.2, "FY2021": -12.2}),
    ("DATA", "Principal payments on leasehold liabilities", {"FY2025": -9.4, "FY2024": -8.5, "FY2023": -10.4, "FY2022": -9.7, "FY2021": -12.5}),
    ("TOTAL", "Cash flows used in financing activities", {"FY2025": -63.6, "FY2024": -70.6, "FY2023": -22.6, "FY2022": -21.9, "FY2021": -24.7}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -1861.9, "FY2024": 41.1, "FY2023": -2180.2, "FY2022": -1174.7, "FY2021": 2218.6}),
    ("DATA", "Effects of exchange rate changes on cash and cash equivalents", {"FY2025": 2.5, "FY2024": -23.5, "FY2023": -65.8, "FY2022": 42.6, "FY2021": -2.5}),
    ("DATA", "Cash and cash equivalents at beginning of the year", {"FY2025": 2762.0, "FY2024": 2744.4, "FY2023": 4990.4, "FY2022": 6122.5, "FY2021": 3906.4}),
    ("TOTAL", "Cash and cash equivalents at end of the year", {"FY2025": 902.6, "FY2024": 2762.0, "FY2023": 2744.4, "FY2022": 4990.4, "FY2021": 6122.5}),
]

bw.add_cash_flow_sheet(
    title="ICBC Standard Bank Plc — Consolidated Statement of Cash Flows",
    subtitle="ICBC Standard Bank Group (consolidated basis), $m unless stated",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=72,
    source_height=110,
    unit_suffix=" ($m)",
)

# ---------------------------------------------------------------
# Sheet 5: Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Gross balances subject to the three-stage ECL model", {}),
    ("DATA", "Stage 1 (12-month ECL)", {"FY2025": 13357.1, "FY2024": 11465.1, "FY2023": 9323.6, "FY2022": 10617.5, "FY2021": 11586.6}),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {"FY2025": 38.3, "FY2024": 0.0, "FY2023": 0.0, "FY2022": 9.8, "FY2021": 66.8}),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired)", {"FY2025": 0.0, "FY2024": 0.0, "FY2023": 0.0, "FY2022": 28.3}),
    ("DATA", "Purchased or originated credit-impaired (POCI)", {"FY2025": 5.7, "FY2024": 5.3, "FY2023": 10.8, "FY2022": 95.1}),
    ("TOTAL", "Total gross balances subject to ECL", {"FY2025": 13401.1, "FY2024": 11470.4, "FY2023": 9334.4, "FY2022": 10750.7, "FY2021": 11653.4}),
    ("SECTION", "Credit loss allowance, by stage (year-end balance)", {}),
    ("DATA", "Stage 1 (12-month ECL)", {"FY2025": -25.4, "FY2024": -15.9, "FY2023": -13.2, "FY2022": -7.3, "FY2021": -5.0}),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {"FY2025": -4.0, "FY2024": 0.0, "FY2023": 0.0, "FY2022": -3.8, "FY2021": -0.3}),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired)", {"FY2025": 0.0, "FY2024": 0.0, "FY2023": 0.0, "FY2022": -4.1, "FY2021": 0.0}),
    ("DATA", "Purchased or originated credit-impaired (POCI)", {"FY2025": -5.3, "FY2024": -3.5, "FY2023": -3.6, "FY2022": -51.4}),
    ("TOTAL", "Total credit loss allowance", {"FY2025": -34.7, "FY2024": -19.4, "FY2023": -16.8, "FY2022": -66.6, "FY2021": -5.3}),
    ("SECTION", "Derived coverage ratio", {}),
    ("DATA", "Total credit loss allowance / total gross balances subject to ECL", {"FY2025": "0.26%", "FY2024": "0.17%", "FY2023": "0.18%", "FY2022": "0.62%", "FY2021": "0.05%"}),
]

ASSET_QUALITY_SOURCES = (
    f"Sources — {STATEMENTS_ENTITY_NOTE}\n"
    f"FY2025 & FY2024: ICBC Standard Bank Consolidated Annual Report 2025, p.159-160 (Note 37.4 Credit risk - Analysis of gross balances/Movements in credit loss allowances) — {AR25_URL}\n"
    f"FY2023 & FY2022: ICBC Standard Bank Consolidated Annual Report 2023, p.147-148 (Note 37 Risk management - same tables) — {AR23_URL}\n"
    f"FY2021: ICBC Standard Bank Consolidated Annual Report 2021, p.143-144 (Note 37 Risk management - same tables) — {AR21_URL}\n"
    "Note: coverage is across the Group's entire ECL-model population (cash, interbank placements, reverse repos, "
    "loans and advances, financial investments, commitments/guarantees) - not restricted to customer loans, since "
    "that is how the Group's own credit-risk note is structured. FY2021's own disclosure does not break out a "
    "separate POCI column (leave blank, not zero) or a distinct 'Sub-standard/Doubtful/Loss' Stage 3 sub-split; "
    "FY2021 Stage 3 total is genuinely nil. The derived coverage ratio (total allowance / total gross balances) is "
    "computed here for a comparable cross-year signal, not itself a disclosed figure."
)

bw.add_asset_quality_sheet(
    title="ICBC Standard Bank Plc — Asset Quality",
    subtitle="ICBC Standard Bank Group (consolidated basis), $m unless stated",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=68,
    source_height=140,
    unit_suffix=" ($m)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Consolidated basis, {unit}" if unit else "Consolidated basis",
                         rows_data, sources_text, note=note, first_col_width=48, source_height=100)

metric(
    "CET1 Capital", "$m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 1819.5, "FY2024": 1676.1, "FY2023": 1629.1, "FY2022": 1454.6, "FY2021": 1148.4})],
    p3_sources(),
    note="FY2021 figure is 'Total Common Equity Tier I' from Table 5 (Capital Resources), the transitional-basis "
         "equivalent of the UK KM1 template row used from FY2022 onward.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "12.2%", "FY2024": "14.6%", "FY2023": "16.9%", "FY2022": "15.7%", "FY2021": "13.47%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "$m",
    [("Tier 1 capital", {"FY2025": 1979.5, "FY2024": 1836.1, "FY2023": 1789.1, "FY2022": 1614.6, "FY2021": 1308.4})],
    p3_sources(),
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "13.3%", "FY2024": "16.0%", "FY2023": "18.5%", "FY2022": "17.5%", "FY2021": "15.35%"})],
    p3_sources(),
    note="FY2021 figure is 'Tier 1 Risk Asset Ratio' from Table 5, the transitional-basis equivalent of the later "
         "UK KM1 template row.",
)

metric(
    "Total Capital", "$m",
    [("Total capital", {"FY2025": 2229.5, "FY2024": 2086.1, "FY2023": 2039.1, "FY2022": 1864.6, "FY2021": 1558.4})],
    p3_sources(),
    note="FY2021 figure is 'Total eligible capital' from Table 5, the transitional-basis equivalent of the later "
         "UK KM1 template row.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "15.0%", "FY2024": "18.1%", "FY2023": "21.1%", "FY2022": "20.2%", "FY2021": "18.28%"})],
    p3_sources(),
    note="FY2021 figure is 'Capital Adequacy ratio' from Table 5, the transitional-basis equivalent of the later "
         "UK KM1 template row.",
)

metric(
    "Total RWAs", "$m",
    [("Total risk-weighted exposure amount", {"FY2025": 14902.7, "FY2024": 11500.1, "FY2023": 9653.2, "FY2022": 9251.0, "FY2021": 8526.3})],
    p3_sources(),
)

# ---------------------------------------------------------------
# RWA Breakdown (placed right after Total RWAs, itself a Pillar 3 disclosure)
# ---------------------------------------------------------------
rwa_breakdown_rows = [
    ("SECTION", "Risk-weighted exposure amounts by category", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 3495.0, "FY2024": 2736.3, "FY2023": 2692.2, "FY2022": 1770.9}),
    ("DATA", "Credit risk, counterparty credit risk and dilution risk, combined (FY2021's older disclosure format only - not separable into the components above; derived from Table 6's capital requirement ÷8%)", {"FY2021": 3830.0}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 5023.6, "FY2024": 2843.7, "FY2023": 2109.9, "FY2022": 1854.0}),
    ("DATA", "Of which credit valuation adjustment (CVA)", {"FY2025": 460.4, "FY2024": 276.0, "FY2023": 219.9, "FY2022": 243.4, "FY2021": 193.75}),
    ("DATA", "Settlement risk", {"FY2025": 0.2, "FY2024": 0.6, "FY2023": 0.1, "FY2022": 24.9, "FY2021": 2.5}),
    ("DATA", "Securitisation exposures in the non-trading book", {"FY2025": 0.0, "FY2024": 0.0, "FY2023": 0.0, "FY2022": 0.0}),
    ("DATA", "Market risk (position, foreign exchange and commodities)", {"FY2025": 4799.2, "FY2024": 4464.4, "FY2023": 3475.5, "FY2022": 4277.5, "FY2021": 3681.25}),
    ("DATA", "Operational risk", {"FY2025": 1402.4, "FY2024": 1455.1, "FY2023": 1375.5, "FY2022": 1323.7, "FY2021": 818.75}),
    ("DATA", "Amounts below thresholds for deduction (subject to 250% risk weight, for information)", {"FY2025": 4.9, "FY2024": 3.0, "FY2023": 5.4, "FY2022": 1.5}),
    ("TOTAL", "Total risk-weighted exposure amount", {"FY2025": 14902.7, "FY2024": 11500.1, "FY2023": 9653.2, "FY2022": 9251.0, "FY2021": 8526.3}),
]

RWA_BREAKDOWN_SOURCES = (
    f"Sources — {STATEMENTS_ENTITY_NOTE}\n"
    f"FY2025 & FY2024: ICBC Standard Bank Pillar 3 Disclosures 2025, p.6 (UK OV1 - Overview of risk-weighted exposure amounts) — {P3_25_URL}\n"
    f"FY2023 & FY2022: ICBC Standard Bank Pillar 3 Disclosures 2023, p.6-7 (UK OV1) — {P3_23_URL}\n"
    f"FY2021: ICBC Standard Bank Pillar 3 Disclosures 2021, p.24 (Table 6: ICBCS - Capital Requirements, pre-UK-OV1 format) — {P3_21_URL}\n"
    "Note: FY2021's Pillar 3 document predates the UK OV1 template and combines credit, counterparty credit and "
    "dilution risk into one 'standardised approach' capital-requirement line, so it cannot be split into 'Credit "
    "risk (excluding CCR)' and 'Counterparty credit risk (CCR)' the way later years' disclosures are - shown as its "
    "own combined line instead of blended into either category. All FY2021 category figures are derived "
    "(disclosed capital requirement ÷ 8%, the standard CRR conversion), not directly disclosed as RWA amounts; "
    "they sum to $8,526.25m, which rounds to the disclosed Total RWA of $8,526.3m. FY2021's document has no "
    "'Securitisation exposures' or 'Amounts below thresholds for deduction' line at all (genuinely not disclosed "
    "in that format, left blank rather than assumed zero)."
)

bw.add_rwa_breakdown_sheet(
    title="ICBC Standard Bank Plc — RWA Breakdown",
    subtitle="ICBC Standard Bank Group (consolidated basis), $m",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=88,
    source_height=150,
    unit_suffix=" ($m)",
)

metric(
    "Leverage Ratio", "$m / %",
    [
        ("Total exposure measure excluding claims on central banks ($m)", {"FY2025": 35294.7, "FY2024": 26624.0, "FY2023": 23301.0, "FY2022": 20958.2, "FY2021": 25680}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "5.6%", "FY2024": "6.9%", "FY2023": "7.7%", "FY2022": "7.7%", "FY2021": "5.09%"}),
    ],
    p3_sources(),
    note="FY2021 uses the CRR Leverage Ratio Common Disclosure Template's 'Total leverage ratio exposures' and "
         "'Leverage ratio' rows (Annex D) — the pre-'excluding central banks' presentation format used before the "
         "later UK KM1 template split the exposure measure basis.",
)

metric(
    "LCR", "$m / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value (average) ($m)", {"FY2025": 5294.2, "FY2024": 5216.2, "FY2023": 5704.2, "FY2022": 6280.5, "FY2021": 5027}),
        ("Total net cash outflows, adjusted value ($m)", {"FY2025": 2777.2, "FY2024": 2422.5, "FY2023": 3561.5, "FY2022": 2926.2, "FY2021": 2425}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "197.3%", "FY2024": "226.7%", "FY2023": "165.3%", "FY2022": "206.0%", "FY2021": "207%"}),
    ],
    p3_sources(),
    note="LCR figures are averages of month-end observations over the 12 months preceding each year-end. FY2021 "
         "figures are the 31 December 2021 quarter-end column of Table 8 (Average Consolidated LCR for ICBCS Group), "
         "the same consolidated-Group basis used by the later UK KM1 template rows.",
)

metric(
    "NSFR", "$m / %",
    [
        ("Total available stable funding ($m)", {"FY2025": 9393.0, "FY2024": 8348.6, "FY2023": 7963.4, "FY2022": 8417.6}),
        ("Total required stable funding ($m)", {"FY2025": 7736.7, "FY2024": 6118.4, "FY2023": 4462.0, "FY2022": 5266.3}),
        ("Net Stable Funding Ratio (%)", {"FY2025": "122.8%", "FY2024": "136.4%", "FY2023": "183.3%", "FY2022": "163.8%", "FY2021": "Not disclosed"}),
    ],
    p3_sources(),
    note="NSFR was not a UK Pillar 3 disclosure requirement as at FY2021 (the UK NSFR regime took effect from "
         "1 January 2022), so no FY2021 figures are available. Balances are averages of the four quarter-ends "
         "preceding each year-end.",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})],
    p3_sources(),
    note="No MREL disclosure appears in any of the five ICBC Standard Bank Pillar 3 Disclosures reports reviewed "
         "(2021-2025) — ICBC Standard Bank Plc is not itself a resolution entity subject to a standalone MREL "
         "requirement.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 37800.7, "FY2024": 26600.4, "FY2023": 23247.1, "FY2022": 22627.3, "FY2021": 26268.5}),
        ("Loans and advances to customers", {"FY2025": 1828.0, "FY2024": 1303.0, "FY2023": 771.3, "FY2022": 818.6, "FY2021": 1608.7}),
        ("Total liabilities", {"FY2025": 35669.3, "FY2024": 24656.7, "FY2023": 21376.2, "FY2022": 20945.3, "FY2021": 24898.5}),
        ("Total equity", {"FY2025": 2131.4, "FY2024": 1943.7, "FY2023": 1870.9, "FY2022": 1682.0, "FY2021": 1370.0}),
    ],
    balance_sheet_unit="$m",
    income_statement_totals=[
        ("Total operating income", {"FY2025": 739.8, "FY2024": 572.1, "FY2023": 558.0, "FY2022": 809.9, "FY2021": 466.0}),
        ("Operating expenses", {"FY2025": -443.9, "FY2024": -382.4, "FY2023": -397.6, "FY2022": -373.6, "FY2021": -348.1}),
        ("Profit attributable to equity shareholders", {"FY2025": 224.9, "FY2024": 156.5, "FY2023": 187.1, "FY2022": 317.1, "FY2021": 98.6}),
    ],
    income_statement_unit="$m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 1943.7, "FY2024": 1870.9, "FY2023": 1682.0, "FY2022": 1370.0, "FY2021": 1301.5}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": 241.9, "FY2024": 134.9, "FY2023": 201.1, "FY2022": 324.2, "FY2021": 80.7}),
        ("Other equity movements, net", {"FY2025": -54.2, "FY2024": -62.1, "FY2023": -12.2, "FY2022": -12.2, "FY2021": -12.2}),
    ],
    equity_changes_unit="$m",
    cash_flow_totals=[
        ("Cash flows (used in)/from operating activities", {"FY2025": -1780.3, "FY2024": 128.1, "FY2023": -2150.7, "FY2022": -1137.3, "FY2021": 2255.8}),
        ("Cash flows used in investing activities", {"FY2025": -18.0, "FY2024": -16.4, "FY2023": -6.9, "FY2022": -15.5, "FY2021": -12.5}),
        ("Cash flows used in financing activities", {"FY2025": -63.6, "FY2024": -70.6, "FY2023": -22.6, "FY2022": -21.9, "FY2021": -24.7}),
        ("Cash and cash equivalents at end of the year", {"FY2025": 902.6, "FY2024": 2762.0, "FY2023": 2744.4, "FY2022": 4990.4, "FY2021": 6122.5}),
    ],
    cash_flow_unit="$m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "12.2%", "FY2024": "14.6%", "FY2023": "16.9%", "FY2022": "15.7%", "FY2021": "13.47%"}),
        ("Tier 1 Ratio", {"FY2025": "13.3%", "FY2024": "16.0%", "FY2023": "18.5%", "FY2022": "17.5%", "FY2021": "15.35%"}),
        ("Total Capital Ratio", {"FY2025": "15.0%", "FY2024": "18.1%", "FY2023": "21.1%", "FY2022": "20.2%", "FY2021": "18.28%"}),
        ("Leverage Ratio", {"FY2025": "5.6%", "FY2024": "6.9%", "FY2023": "7.7%", "FY2022": "7.7%", "FY2021": "5.09%"}),
        ("LCR", {"FY2025": "197.3%", "FY2024": "226.7%", "FY2023": "165.3%", "FY2022": "206.0%", "FY2021": "207%"}),
        ("NSFR", {"FY2025": "122.8%", "FY2024": "136.4%", "FY2023": "183.3%", "FY2022": "163.8%", "FY2021": "Not disclosed"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. All amounts are in USD ($m), the reporting currency used "
         "throughout ICBC Standard Bank Plc's Annual Reports and Pillar 3 Disclosures.",
)

bw.save("/Users/armaan/code/katalysis/banks/ICBC STANDARD BANK PLC FINANCIALS.xlsx")
