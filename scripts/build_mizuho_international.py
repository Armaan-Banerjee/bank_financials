import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


# Mizuho International plc (company 01203696, FRN 119256), confirmed against
# Banks List 2608.xlsx and Companies House.  The reports present consolidated
# Mizuho International plc Group figures in GBP millions.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

AR = {
    "FY2025": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/6949753a5e4af5e79887a666_MIzuho_MHI_Annual_Report_2025.pdf",
    "FY2024": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/686301edbbd3ea24c5c8059f_mizuho_annual_report_2024_final_v02.pdf",
    "FY2023": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/6863021624e9468651ae2fbd_mizuho_annual_report_2023_final_02.pdf",
    "FY2022": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/686302389cf6e01446043fd2_2022-mizuho-international-plc-annual-report.pdf",
    "FY2021": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/686302637f7fc2c72f2e2f59_2021-mizuho-international-plc-annual-report.pdf",
}
P3 = {
    "FY2025": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/6a903f20d82fcd0100158b9f_MHI%20consolidated%20Pillar%203%20disclosure%202025.pdf",
    "FY2024": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/6864747a2fb833ca68387b1e_mhi-consolidated-pillar-3-disclosure-2024-final.pdf",
    "FY2023": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/68647496be5f9b72fe43c3f9_mhi-consolidated-pillar-3-disclosure-2023-final.pdf",
    "FY2022": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/686474abd90349ac917e208a_2022-mhi-consolidated-pillar-3-disclosure.pdf",
    "FY2021": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/6864754eb71eb72dcfb8ec06_2021-mizuho-international-plc-pillar-3-disclosure.pdf",
}

ENTITY_NOTE = (
    "ENTITY NOTE: Mizuho International plc (company 01203696, FRN 119256; LEI "
    "213800HZ54TG54H2KV03) is the legal entity in Banks List 2608.xlsx. "
    "Companies House confirms the active UK public company. Figures are the "
    "consolidated Mizuho International plc Group basis used in the official reports, "
    "in £ millions. The company accounts use the FRS 102 exemption from preparing a "
    "separate company cash-flow statement."
)

CF = {
    "Profit / (loss) before tax": {"FY2025": 5.8, "FY2024": 15.0, "FY2023": -10.4, "FY2022": -37.6, "FY2021": 43.8},
    "Non-cash items included in profit / (loss) before tax": {"FY2025": -30.0, "FY2024": -23.0, "FY2023": -6.3, "FY2022": 12.6, "FY2021": 23.3},
    "Provision for liabilities": {"FY2025": 0.1, "FY2024": -0.9, "FY2023": 0.9, "FY2022": -0.2, "FY2021": -0.4},
    "Movement in Other Comprehensive Income": {"FY2025": -0.5, "FY2024": -0.4, "FY2023": -0.1, "FY2022": -0.4, "FY2021": -0.5},
    "Change in operating assets": {"FY2025": 846.1, "FY2024": 2479.7, "FY2023": -5424.2, "FY2022": -3613.0, "FY2021": 6374.7},
    "Change in operating liabilities": {"FY2025": -938.8, "FY2024": -2313.4, "FY2023": 5456.5, "FY2022": 4012.7, "FY2021": -6952.2},
    "Interest paid": {"FY2025": -93.3, "FY2024": -92.7, "FY2023": -0.1, "FY2022": -0.2, "FY2021": -1.3},
    "Interest received": {"FY2025": 124.2, "FY2024": 139.8, "FY2023": 11.0, "FY2022": 14.4, "FY2021": 16.4},
    "Tax (paid) / received": {"FY2025": -6.1, "FY2024": 12.6, "FY2023": -2.0, "FY2022": -3.4, "FY2021": 10.5},
    "Net cash flows from operating activities": {"FY2025": -92.5, "FY2024": 216.7, "FY2023": 25.3, "FY2022": 384.9, "FY2021": -485.7},
    "Net investment in shares in group undertakings": {"FY2025": -1.4, "FY2024": -0.1, "FY2023": -0.5, "FY2022": -2.0, "FY2021": -0.1},
    "Dividends from investment in shares in group undertakings": {"FY2025": 0.4, "FY2024": 0.2, "FY2023": 0.3, "FY2022": 0.7, "FY2021": 0.4},
    "Purchase of intangible assets": {"FY2025": -43.8, "FY2024": -27.2, "FY2023": -28.7, "FY2022": -25.3, "FY2021": -21.8},
    "Purchase of tangible assets": {"FY2025": -5.2, "FY2024": -5.8, "FY2023": -2.7, "FY2022": -6.4, "FY2021": -3.6},
    "Net cash flows used in investing activities": {"FY2025": -50.0, "FY2024": -32.9, "FY2023": -31.6, "FY2022": -33.0, "FY2021": -25.1},
    "Net repayment from debt securities in issue": {"FY2025": -101.5, "FY2024": -221.2, "FY2023": -139.6, "FY2022": -87.8, "FY2021": 75.6},
    "Net repayment of subordinated liabilities": {"FY2022": -45.0},
    "Proceeds from the issuance of equity": {"FY2025": 45.0},
    "Net cash flows from / (used in) financing activities": {"FY2025": -56.5, "FY2024": -221.2, "FY2023": -139.6, "FY2022": -132.8, "FY2021": 75.6},
    "Net (decrease) / increase in cash and cash equivalents": {"FY2025": -199.0, "FY2024": -37.4, "FY2023": -145.9, "FY2022": 219.1, "FY2021": -435.2},
    "Effects of exchange rates on cash and cash equivalents": {"FY2025": -0.9, "FY2024": -4.2, "FY2023": 4.3, "FY2022": 2.2, "FY2021": -6.6},
    "Cash and cash equivalents at beginning of the period": {"FY2025": 375.6, "FY2024": 417.2, "FY2023": 558.8, "FY2022": 337.5, "FY2021": 779.3},
    "Cash and cash equivalents at the end of the period": {"FY2025": 175.7, "FY2024": 375.6, "FY2023": 417.2, "FY2022": 558.8, "FY2021": 337.5},
}

ROWS = [("SECTION", "Operating activities", {})]
for label in list(CF)[:10]:
    ROWS.append(("TOTAL" if label == "Net cash flows from operating activities" else "DATA", label, CF[label]))
ROWS.append(("SECTION", "Investing activities", {}))
for label in list(CF)[10:15]:
    ROWS.append(("TOTAL" if label == "Net cash flows used in investing activities" else "DATA", label, CF[label]))
ROWS.append(("SECTION", "Financing activities", {}))
for label in list(CF)[15:19]:
    ROWS.append(("TOTAL" if label == "Net cash flows from / (used in) financing activities" else "DATA", label, CF[label]))
for label in list(CF)[19:]:
    ROWS.append(("TOTAL" if "cash equivalents" in label else "DATA", label, CF[label]))

def sources():
    return ENTITY_NOTE + "\n\nOfficial sources — Mizuho International plc Annual Reports: " + "; ".join(f"{y}: {u}" for y, u in AR.items())

def p3_sources():
    return ENTITY_NOTE + "\n\nOfficial Mizuho International plc Pillar 3 disclosures: " + "; ".join(f"{y}: {u}" for y, u in P3.items())

STATEMENTS_SOURCES = (
    sources()
    + "\n\nBalance Sheet/P&L/Equity figures are the Consolidated Mizuho International plc Group basis "
      "(distinct from the Company-only basis also shown in each Annual Report). FY2025/FY2024: Annual "
      "Report 2025, Consolidated Statement of Comprehensive Income and Consolidated Statement of "
      "Financial Position p.88-89, Consolidated Statement of Changes in Equity p.90-91. FY2023/FY2022: "
      "Annual Report 2024, same statements p.86-89. FY2021: Annual Report 2022, Consolidated Statement "
      "of Comprehensive Income p.84-85, Consolidated Statement of Financial Position and Consolidated "
      "Statement of Changes in Equity p.86, 88."
)

bw = BankWorkbook("Mizuho International plc", YEARS, header_color="7A3E9D")

# ---------------------------------------------------------------
# Balance Sheet - equity reconciliation ladder step 1: built first so each
# year's own Total Equity is the independent check value for the equity
# sheet below. All 5 years tie exactly.
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 115.5, "FY2024": 328.5, "FY2023": 370.4, "FY2022": 481.0, "FY2021": 227.5}),
    ("DATA", "Loans and advances to banks", {"FY2025": 60.2, "FY2024": 47.1, "FY2023": 46.8, "FY2022": 77.8, "FY2021": 110.0}),
    ("DATA", "Reverse repurchase agreements with banks", {"FY2025": 4055.8, "FY2024": 5131.0, "FY2023": 5841.9, "FY2022": 3854.3, "FY2021": 2107.5}),
    ("DATA", "Reverse repurchase agreements with customers", {"FY2025": 4587.1, "FY2024": 3059.6, "FY2023": 2303.5, "FY2022": 5417.0, "FY2021": 4288.6}),
    ("DATA", "Debt and other fixed income securities", {"FY2025": 5644.9, "FY2024": 5463.7, "FY2023": 5087.2, "FY2022": 4772.0, "FY2021": 4261.9}),
    ("DATA", "Equity shares", {"FY2025": 2.6, "FY2024": 4.3, "FY2023": 6.1, "FY2022": 3.5, "FY2021": 1.8}),
    ("DATA", "Derivative assets", {"FY2025": 8520.1, "FY2024": 9707.7, "FY2023": 13072.6, "FY2022": 6443.1, "FY2021": 6513.8}),
    ("DATA", "Shares in group undertakings", {"FY2025": 17.6, "FY2024": 13.2, "FY2023": 9.9, "FY2022": 8.1, "FY2021": 6.8}),
    ("DATA", "Intangible assets", {"FY2025": 96.3, "FY2024": 76.7, "FY2023": 73.7, "FY2022": 66.2, "FY2021": 63.2}),
    ("DATA", "Tangible fixed assets", {"FY2025": 25.1, "FY2024": 27.1, "FY2023": 27.3, "FY2022": 29.0, "FY2021": 27.0}),
    ("DATA", "Other assets", {"FY2025": 559.8, "FY2024": 897.9, "FY2023": 449.5, "FY2022": 832.2, "FY2021": 517.6}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 229.9, "FY2024": 177.1, "FY2023": 90.0, "FY2022": 74.7, "FY2021": 82.7}),
    ("TOTAL", "Total Assets", {"FY2025": 23914.9, "FY2024": 24933.9, "FY2023": 27378.9, "FY2022": 22058.9, "FY2021": 18208.4}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2025": 678.7, "FY2024": 519.1, "FY2023": 292.1, "FY2022": 1153.3, "FY2021": 285.5}),
    ("DATA", "Customer accounts", {"FY2025": 473.5, "FY2024": 707.5, "FY2023": 897.9, "FY2022": 295.7, "FY2021": 228.6}),
    ("DATA", "Repurchase agreements with banks", {"FY2025": 4580.9, "FY2024": 3769.7, "FY2023": 1675.3, "FY2022": 1775.5, "FY2021": 1984.1}),
    ("DATA", "Repurchase agreements with customers", {"FY2025": 4078.0, "FY2024": 3425.7, "FY2023": 5231.3, "FY2022": 5799.8, "FY2021": 3133.7}),
    ("DATA", "Debt securities in issue", {"FY2025": 1292.3, "FY2024": 1395.0, "FY2023": 1616.5, "FY2022": 1760.1, "FY2021": 1851.6}),
    ("DATA", "Short trading positions", {"FY2025": 2889.1, "FY2024": 3925.7, "FY2023": 3418.7, "FY2022": 3560.9, "FY2021": 3072.9}),
    ("DATA", "Derivative liabilities", {"FY2025": 8548.4, "FY2024": 9603.3, "FY2023": 12833.5, "FY2022": 6422.7, "FY2021": 6481.2}),
    ("DATA", "Other liabilities", {"FY2025": 365.8, "FY2024": 651.2, "FY2023": 581.4, "FY2022": 452.1, "FY2021": 225.3}),
    ("DATA", "Accruals and deferred income", {"FY2025": 234.5, "FY2024": 212.9, "FY2023": 120.5, "FY2022": 123.3, "FY2021": 155.4}),
    ("DATA", "Provisions for liabilities", {"FY2025": 0.2, "FY2024": 3.1, "FY2023": 4.0, "FY2022": 3.1, "FY2021": 3.3}),
    ("DATA", "Subordinated liabilities", {"FY2021": 45.2}),
    ("TOTAL", "Total Liabilities", {"FY2025": 23141.4, "FY2024": 24213.2, "FY2023": 26671.2, "FY2022": 21346.5, "FY2021": 17466.8}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 754.9, "FY2024": 709.9, "FY2023": 709.9, "FY2022": 709.9, "FY2021": 709.9}),
    ("DATA", "Share premium account", {"FY2025": 15.6, "FY2024": 15.6, "FY2023": 15.6, "FY2022": 15.6, "FY2021": 15.6}),
    ("DATA", "Pension reserve", {"FY2025": -7.1, "FY2024": -6.8, "FY2023": -6.5, "FY2022": -6.2, "FY2021": -5.9}),
    ("DATA", "Other reserves", {"FY2025": -0.8, "FY2024": -0.6, "FY2023": -0.4, "FY2022": -0.5, "FY2021": -0.4}),
    ("DATA", "Profit and loss account", {"FY2025": 10.9, "FY2024": 2.6, "FY2023": -10.9, "FY2022": -6.4, "FY2021": 22.4}),
    ("TOTAL", "Total Equity", {"FY2025": 773.5, "FY2024": 720.7, "FY2023": 707.7, "FY2022": 712.4, "FY2021": 741.6}),
    ("TOTAL", "Total Liabilities and Equity", {"FY2025": 23914.9, "FY2024": 24933.9, "FY2023": 27378.9, "FY2022": 22058.9, "FY2021": 18208.4}),
]
bw.add_balance_sheet_sheet(
    title="Mizuho International plc — Balance Sheet",
    subtitle="Consolidated Group basis. £m. FY2021 shows a genuine structural difference from later years: a "
              "standalone 'Subordinated liabilities' line (£45.2m), fully repaid during FY2022 (see the Cash Flow "
              "Statement's 'Net repayment of subordinated liabilities' row) and absent from FY2022 onward.",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=72,
    source_height=240,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable", {"FY2025": 28.4, "FY2024": 33.3, "FY2023": 18.2, "FY2022": 7.5, "FY2021": 4.0}),
    ("DATA", "Interest payable", {"FY2025": -105.7, "FY2024": -103.3, "FY2023": -38.7, "FY2022": -4.0, "FY2021": -5.4}),
    ("TOTAL", "Net interest income/(expense)", {"FY2025": -77.3, "FY2024": -70.0, "FY2023": -20.5, "FY2022": 3.5, "FY2021": -1.4}),
    ("DATA", "Fees and commissions receivable", {"FY2025": 198.7, "FY2024": 178.8, "FY2023": 132.1, "FY2022": 175.6, "FY2021": 182.4}),
    ("DATA", "Fees and commissions payable", {"FY2025": -76.0, "FY2024": -71.9, "FY2023": -53.4, "FY2022": -91.3, "FY2021": -99.5}),
    ("TOTAL", "Net fees and commissions", {"FY2025": 122.7, "FY2024": 106.9, "FY2023": 78.7, "FY2022": 84.3, "FY2021": 82.9}),
    ("DATA", "Dealing profit", {"FY2025": 175.1, "FY2024": 204.9, "FY2023": 130.7, "FY2022": 77.1, "FY2021": 183.1}),
    ("DATA", "Other operating income", {"FY2025": 152.9, "FY2024": 2.3, "FY2023": 5.5, "FY2022": 1.4, "FY2021": 0.5}),
    ("TOTAL", "Net income from operations", {"FY2025": 373.4, "FY2024": 244.1, "FY2023": 194.4, "FY2022": 166.3, "FY2021": 265.1}),
    ("DATA", "Administrative expenses", {"FY2025": -338.6, "FY2024": -200.7, "FY2023": -178.3, "FY2022": -178.5, "FY2021": -192.0}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -28.9, "FY2024": -29.3, "FY2023": -25.6, "FY2022": -25.4, "FY2021": -29.5}),
    ("DATA", "Provisions for liabilities", {"FY2025": -0.1, "FY2024": 0.9, "FY2023": -0.9, "FY2021": 0.2}),
    ("TOTAL", "Operating expenses", {"FY2025": -367.6, "FY2024": -229.1, "FY2023": -204.8, "FY2022": -203.9, "FY2021": -221.3}),
    ("TOTAL", "Profit/(loss) on ordinary activities before taxation", {"FY2025": 5.8, "FY2024": 15.0, "FY2023": -10.4, "FY2022": -37.6, "FY2021": 43.8}),
    ("DATA", "Tax credit/(charge) on profit/(loss) on ordinary activities", {"FY2025": 1.4, "FY2024": -1.5, "FY2023": 5.9, "FY2022": 8.8, "FY2021": -1.0}),
    ("TOTAL", "Profit/(loss) for the year", {"FY2025": 7.2, "FY2024": 13.5, "FY2023": -4.5, "FY2022": -28.8, "FY2021": 42.8}),
    ("SECTION", "Other comprehensive income/(loss)", {}),
    ("DATA", "Re-measurement losses from defined benefit scheme", {"FY2025": -0.3, "FY2024": -0.3, "FY2023": -0.3, "FY2022": -0.3}),
    ("DATA", "FX translation gain/(loss) relating to net investment in subsidiary", {"FY2025": -0.2, "FY2024": -0.2, "FY2023": 0.1, "FY2022": -0.1, "FY2021": -0.4}),
    ("TOTAL", "Total comprehensive income/(loss) for the year", {"FY2025": 6.7, "FY2024": 13.0, "FY2023": -4.7, "FY2022": -29.2, "FY2021": 42.4}),
]
bw.add_income_statement_sheet(
    title="Mizuho International plc — Profit & Loss",
    subtitle="Consolidated Group basis. £m. Re-measurement losses from defined benefit scheme were nil (not "
              "disclosed as a line) in FY2021; Provisions for liabilities was nil in FY2021 Company statement "
              "terms and is shown blank for FY2021 Consolidated as the report discloses no separate figure.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=240,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - per-year reconciliation ladder confirmed:
# every year's own closing balance ties exactly to both the next year's own
# opening balance and that year's own Balance Sheet Total Equity. Zero plug
# rows needed anywhere across all 5 years. Ladder's mandated scan of each
# year's equity note caught the FY2025 capital injection, equity
# contribution, and transfer-to-P&L rows arising from the sub-lease
# termination described in the source's own explanatory note.
# ---------------------------------------------------------------
equity_headers = ["Share capital", "Share premium account", "Pension reserve", "Other reserves",
                   "Profit and loss account", "Total equity"]
equity_rows = [
    ("TOTAL", "At 1 April 2020 (FY2021 opening)", (709.9, 15.6, -5.9, 0, -20.4, 699.2)),
    ("DATA", "Profit for the year", (None, None, None, None, 42.8, 42.8)),
    ("DATA", "Other comprehensive income/(loss)", (None, None, None, -0.4, None, -0.4)),
    ("TOTAL", "At 31 March 2021 (FY2021 closing)", (709.9, 15.6, -5.9, -0.4, 22.4, 741.6)),
    ("DATA", "Loss for the year", (None, None, None, None, -28.8, -28.8)),
    ("DATA", "Other comprehensive income/(loss)", (None, None, -0.3, -0.1, None, -0.4)),
    ("TOTAL", "At 31 March 2022 (FY2022 closing)", (709.9, 15.6, -6.2, -0.5, -6.4, 712.4)),
    ("DATA", "Loss for the year", (None, None, None, None, -4.5, -4.5)),
    ("DATA", "Other comprehensive income/(loss)", (None, None, -0.3, 0.1, None, -0.2)),
    ("TOTAL", "At 31 March 2023 (FY2023 closing)", (709.9, 15.6, -6.5, -0.4, -10.9, 707.7)),
    ("DATA", "Profit for the year", (None, None, None, None, 13.5, 13.5)),
    ("DATA", "Other comprehensive income/(loss)", (None, None, -0.3, -0.2, None, -0.5)),
    ("TOTAL", "At 31 March 2024 (FY2024 closing)", (709.9, 15.6, -6.8, -0.6, 2.6, 720.7)),
    ("DATA", "Profit for the year", (None, None, None, None, 7.2, 7.2)),
    ("DATA", "Capital injection", (45.0, None, None, None, None, 45.0)),
    ("DATA", "Equity contribution", (None, None, None, 1.1, None, 1.1)),
    ("DATA", "Transfer to profit and loss account", (None, None, None, -1.1, 1.1, None)),
    ("DATA", "Other comprehensive income/(loss)", (None, None, -0.3, -0.2, None, -0.5)),
    ("TOTAL", "At 31 March 2025 (FY2025 closing)", (754.9, 15.6, -7.1, -0.8, 10.9, 773.5)),
]
bw.add_equity_changes_sheet(
    title="Mizuho International plc — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, Consolidated Group basis. £m. Equity reconciliation "
              "ladder confirmed: every year's own closing balance ties exactly to both the next year's own opening "
              "balance and that year's own Balance Sheet Total Equity - zero plug rows needed anywhere across all "
              "5 years. FY2025's Capital injection/Equity contribution/Transfer-to-P&L rows relate to a capital "
              "raise and the release of a net dilapidation provision following termination of the Company's "
              "sub-lease, per the source's own explanatory note.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
)

bw.add_cash_flow_sheet("Mizuho International plc — Consolidated Statement of Cash Flows", "Consolidated Group basis, £ millions", ROWS, sources(), first_col_width=66, source_height=220, unit_suffix=" (£m)")

# ---------------------------------------------------------------
# Asset Quality - Mizuho is a wholesale/markets subsidiary (loans and
# advances to customers is a minor balance sheet line, e.g. £60.2m of
# £23,914.9m total assets in FY2025); its Pillar 3 disclosures do not
# publish an IFRS 9 stage split. Substituted with the Pillar 3 credit-risk
# exposures by credit quality step table (Table 23), the closest available
# disclosure of counterparty/credit risk quality across the book.
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Credit risk exposures by credit quality step (standardised approach), net of CRM", {}),
    ("DATA", "Credit quality step 1", {"FY2025": 158.3, "FY2024": 368.5, "FY2023": 403.5, "FY2022": 531.4, "FY2021": 303.7}),
    ("DATA", "Credit quality step 2", {"FY2025": 102.2, "FY2024": 72.2, "FY2023": 57.5, "FY2022": 29.7, "FY2021": 31.3}),
    ("DATA", "Credit quality step 3", {"FY2025": 0.0, "FY2024": 57.8, "FY2023": 56.2, "FY2022": 20.4}),
    ("DATA", "Credit quality step 4", {}),
    ("DATA", "Credit quality step 5", {"FY2025": 17.7, "FY2024": 13.2, "FY2023": 9.9, "FY2022": 8.1, "FY2021": 6.9}),
    ("DATA", "Credit quality step 6", {"FY2025": 1.1, "FY2024": 4.0, "FY2023": 3.9, "FY2022": 2.5, "FY2021": 1.7}),
    ("DATA", "Unrated", {"FY2025": 96.5, "FY2024": 70.1, "FY2023": 78.4, "FY2022": 70.5, "FY2021": 64.7}),
    ("TOTAL", "Total net credit exposure", {"FY2025": 375.8, "FY2024": 585.7, "FY2023": 609.5, "FY2022": 662.7, "FY2021": 408.2}),
    ("DATA", "Memo: Total gross credit exposure (before CRM)", {"FY2025": 420.8, "FY2024": 665.7, "FY2023": 681.1, "FY2022": 725.0, "FY2021": 437.9}),
    ("DATA", "Credit risk RWAs (excluding CCR)", {"FY2025": 150.5, "FY2024": 148.4, "FY2023": 140.1, "FY2022": 108.2, "FY2021": 92.8}),
    ("DATA", "Credit risk RWA density (RWAs / net credit exposure)", {"FY2025": "40.05%", "FY2024": "25.34%", "FY2023": "22.99%", "FY2022": "16.33%", "FY2021": "22.73%"}),
]
bw.add_asset_quality_sheet(
    title="Mizuho International plc — Asset Quality",
    subtitle="Pillar 3 credit risk exposures by credit quality step (Table 23), standardised approach, £m — "
              "substitutes for an IFRS 9 stage split, which this Group does not disclose (it runs no material "
              "customer lending book).",
    rows=asset_quality_rows,
    sources_text=p3_sources() + "\n\nTable 23 'Credit risk exposures and RWAs by credit quality step', section 8.3 'Analysis of credit risk exposures', in each year's own Pillar 3 disclosure document listed above.",
    first_col_width=74,
    source_height=240,
    unit_suffix=" (£m)",
)

def metric(name, unit, values, note=None):
    bw.add_metric_sheet(name, unit, [(name, values)], p3_sources(), note=note, first_col_width=48, source_height=220)

metric("CET1 Capital", "£ millions", {"FY2025": 670.5, "FY2024": 637.4, "FY2023": 627.7, "FY2022": 640.8, "FY2021": 675.6}, "FY2025 Annual Report states regulatory capital consists solely of Tier 1 capital; treated as CET1 for this metric because no Tier 2 capital is reported.")
metric("CET1 Ratio", "%", {"FY2025": "20.0%", "FY2024": "22.8%", "FY2023": "28.0%", "FY2022": "31.14%", "FY2021": "31.12%"})
metric("Tier 1 Capital", "£ millions", {"FY2025": 670.5, "FY2024": 637.4, "FY2023": 627.7, "FY2022": 640.8, "FY2021": 675.6})
metric("Tier 1 Ratio", "%", {"FY2025": "20.0%", "FY2024": "22.84%", "FY2023": "28.00%", "FY2022": "31.14%", "FY2021": "31.12%"})
metric("Total Capital", "£ millions", {"FY2025": 670.5, "FY2024": 637.4, "FY2023": 627.7, "FY2022": 640.8, "FY2021": 711.6})
metric("Total Capital Ratio", "%", {"FY2025": "20.0%", "FY2024": "22.84%", "FY2023": "28.00%", "FY2022": "31.14%", "FY2021": "32.78%"})
metric("Total RWAs", "£ millions", {"FY2025": 3353.2, "FY2024": 2790.7, "FY2023": 2241.7, "FY2022": 2057.9, "FY2021": 2171.0})

# RWA Breakdown - Pillar 3 UK OV1 template, placed right after Total RWAs
# per the locked sheet order. All 5 available years tie exactly to the
# Total RWAs figure above (each year's own disclosed Total row used
# directly, not a recomputed sum - individual risk-type rows carry £0.1-
# 0.2m source rounding artifacts against that Total, consistent with the
# pattern seen across other banks in this rollout).
rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 150.5, "FY2024": 148.4, "FY2023": 140.1, "FY2022": 108.2, "FY2021": 92.8}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 682.4, "FY2024": 638.9, "FY2023": 530.6, "FY2022": 357.3, "FY2021": 259.6}),
    ("DATA", "Settlement risk", {"FY2025": 0.0, "FY2024": 0.2, "FY2023": 0.1, "FY2022": 0.2, "FY2021": 0.1}),
    ("DATA", "Position, foreign exchange and commodities risks (Market risk)", {"FY2025": 2014.2, "FY2024": 1626.8, "FY2023": 1166.8, "FY2022": 1224.3, "FY2021": 1445.4}),
    ("DATA", "Large exposures", {"FY2023": 14.6}),
    ("DATA", "Operational risk", {"FY2025": 506.1, "FY2024": 376.6, "FY2023": 389.6, "FY2022": 368.1, "FY2021": 373.3}),
    ("TOTAL", "Total", {"FY2025": 3353.2, "FY2024": 2790.7, "FY2023": 2241.7, "FY2022": 2057.9, "FY2021": 2171.0}),
]
bw.add_rwa_breakdown_sheet(
    title="Mizuho International plc — RWA Breakdown",
    subtitle="Consolidated Group basis, Pillar 3 'UK OV1 - Overview of risk weighted exposure amounts' template "
              "(Table 10, only non-nil rows shown per the source document's own convention), £m. "
              "'Large exposures' (row 22a of the PRA template) only appears as a non-nil row in the FY2023 report.",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources() + "\n\nTable 10 'RWAs and Pillar 1 capital requirements', section 6.1, in each year's own Pillar 3 disclosure document listed above.",
    first_col_width=76,
    source_height=220,
    unit_suffix=" (£m)",
)
metric("Leverage Ratio", "%", {"FY2025": "4.2%", "FY2024": "4.07%", "FY2023": "4.24%", "FY2022": "4.07%", "FY2021": "4.75%"})
metric("LCR", "%", {"FY2025": "268.7%", "FY2024": "250.39%", "FY2023": "302.67%", "FY2022": "364.04%", "FY2021": "303.00%"})
metric("NSFR", "%", {"FY2025": "122.5%", "FY2024": "128.67%", "FY2023": "140.66%", "FY2022": "177.71%"}, "NSFR was not disclosed in the 2021 report; 2025 is from the Annual Report KPI section.")
metric("MREL Ratio", "%", {}, "MREL ratio was not numerically disclosed in the official annual/Pillar 3 reports checked.")

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total Assets", {"FY2025": 23914.9, "FY2024": 24933.9, "FY2023": 27378.9, "FY2022": 22058.9, "FY2021": 18208.4}),
        ("Reverse repurchase agreements with customers", {"FY2025": 4587.1, "FY2024": 3059.6, "FY2023": 2303.5, "FY2022": 5417.0, "FY2021": 4288.6}),
        ("Derivative assets", {"FY2025": 8520.1, "FY2024": 9707.7, "FY2023": 13072.6, "FY2022": 6443.1, "FY2021": 6513.8}),
        ("Total Equity", {"FY2025": 773.5, "FY2024": 720.7, "FY2023": 707.7, "FY2022": 712.4, "FY2021": 741.6}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Net income from operations", {"FY2025": 373.4, "FY2024": 244.1, "FY2023": 194.4, "FY2022": 166.3, "FY2021": 265.1}),
        ("Operating expenses", {"FY2025": -367.6, "FY2024": -229.1, "FY2023": -204.8, "FY2022": -203.9, "FY2021": -221.3}),
        ("Profit/(loss) for the year", {"FY2025": 7.2, "FY2024": 13.5, "FY2023": -4.5, "FY2022": -28.8, "FY2021": 42.8}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 720.7, "FY2024": 707.7, "FY2023": 712.4, "FY2022": 741.6, "FY2021": 699.2}),
        ("Profit/(loss) for the year", {"FY2025": 7.2, "FY2024": 13.5, "FY2023": -4.5, "FY2022": -28.8, "FY2021": 42.8}),
        ("Other equity movements, net", {"FY2025": 45.6, "FY2024": -0.5, "FY2023": -0.2, "FY2022": -0.4, "FY2021": -0.4}),
        ("Closing equity", {"FY2025": 773.5, "FY2024": 720.7, "FY2023": 707.7, "FY2022": 712.4, "FY2021": 741.6}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[("Net cash flow from operating activities", CF["Net cash flows from operating activities"]), ("Net cash flows used in investing activities", CF["Net cash flows used in investing activities"]), ("Cash and cash equivalents at end of period", CF["Cash and cash equivalents at the end of the period"])],
    cash_flow_unit="£m",
    ratios=[("CET1 Ratio", {"FY2025": "20.0%", "FY2024": "22.8%", "FY2023": "28.0%", "FY2022": "31.14%", "FY2021": "31.12%"}), ("Leverage Ratio", {"FY2025": "4.2%", "FY2024": "4.07%", "FY2023": "4.24%", "FY2022": "4.07%", "FY2021": "4.75%"})],
    note="Annual consolidated Group data.",
)

bw.save("/Users/armaan/code/katalysis/banks/MIZUHO INTERNATIONAL FINANCIALS.xlsx")
