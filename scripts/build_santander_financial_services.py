import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

AR2025 = "https://assets.santandermedia.com/adobe/assets/urn:aaid:aem:3af8ccd7-5ee0-4196-9577-83a30558e64c/original/as/02536CCAA25SantanderFinancialServicesPlc.pdf"
AR2023 = "https://assets.santandermedia.com/adobe/assets/urn:aaid:aem:8da5f087-d631-4188-9c9c-9671410070c5/original/as/sfs_annual_report_2023.pdf"
AR2022 = "https://assets.santandermedia.com/adobe/assets/urn:aaid:aem:f15fea69-5780-484a-bb22-ce42b29eeac3/original/as/santander_financial_services_plc_2022_annual_report.pdf"
AR2021 = "https://assets.santandermedia.com/adobe/assets/urn:aaid:aem:58592004-0ef9-4156-9df8-367908fc81a9/original/as/sfs_2021_annual_report.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Santander Financial Services plc (company 02338548, FRN 146003) is the legal entity covered. "
    "It operates in the UK, Jersey and the Isle of Man and is a subsidiary of Santander UK Group Holdings plc. "
    "The Company's accounts are prepared on an individual-company basis: SFS is exempt from preparing group accounts "
    "under section 400 of the Companies Act 2006. Figures below therefore use SFS standalone/company basis throughout; "
    "Santander UK plc, Santander UK Group Holdings plc and Banco Santander SA figures are not substituted."
)

CASH_SOURCES = (
    "Sources - Santander Financial Services plc own audited Cash Flow Statement, £m:\n"
    f"FY2025 and FY2024: SFS 2025 Annual Report, Cash Flow Statement (printed p.48/49) - {AR2025}\n"
    f"FY2023 and FY2022: SFS 2023 Annual Report, Cash Flow Statement (printed p.49) - {AR2023}\n"
    f"FY2022 and FY2021: SFS 2022 Annual Report, Cash Flow Statement (printed p.48) - {AR2022}\n"
    f"FY2021: SFS 2021 Annual Report, Cash Flow Statement (printed p.48) - {AR2021}\n\n"
    "The 2022 report's 2021 comparative agrees with the 2021 report. The 2023 report's 2022 comparative is used for "
    "the FY2022 column, and the 2025 report's 2024 comparative is used for FY2024. FY2025 accounting-policy change "
    "to IFRS 9 hedge accounting did not impact the statement of financial position or income statement and comparatives "
    "were not restated.\n\n" + ENTITY_NOTE
)

rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {"FY2025": 28, "FY2024": -23, "FY2023": -3, "FY2022": 36, "FY2021": 24}),
    ("SECTION", "Adjustments for non-cash items included in profit", {}),
    ("DATA", "Depreciation and amortisation", {"FY2025": 3, "FY2024": 3, "FY2023": 2, "FY2022": 1, "FY2021": 3}),
    ("DATA", "Provisions for other liabilities and charges", {"FY2025": 3, "FY2023": 2, "FY2022": 2, "FY2021": 2}),
    ("DATA", "Impairment losses", {"FY2024": 17, "FY2023": 1, "FY2022": 1}),
    ("DATA", "Corporation tax credit", {"FY2021": -2}),
    ("DATA", "Other non-cash items", {"FY2025": 2, "FY2024": 1, "FY2023": 3, "FY2022": 1}),
    ("TOTAL", "Non-cash items included in profit", {"FY2025": 8, "FY2024": 21, "FY2023": 8, "FY2022": 5, "FY2021": 3}),
    ("SECTION", "Net change in operating assets and liabilities", {}),
    ("DATA", "Cash and balances at central banks", {"FY2024": 17, "FY2023": 1, "FY2022": -1, "FY2021": 1}),
    ("DATA", "Derivative assets", {"FY2025": 3, "FY2024": -17, "FY2023": 2, "FY2022": 14, "FY2021": 12}),
    ("DATA", "Other financial assets at fair value through profit or loss", {"FY2025": -3, "FY2024": 30, "FY2023": -14, "FY2022": 146, "FY2021": 54}),
    ("DATA", "Loans and advances to banks and customers", {"FY2025": 165, "FY2024": 353, "FY2023": 307, "FY2022": -650, "FY2021": 40}),
    ("DATA", "Other assets", {"FY2024": -1, "FY2023": -2, "FY2022": -2}),
    ("DATA", "Deposits by banks and customers", {"FY2025": -103, "FY2024": 568, "FY2023": -443, "FY2022": 576, "FY2021": -40}),
    ("DATA", "Derivative liabilities", {"FY2025": 10, "FY2024": -56, "FY2023": 12, "FY2022": -181, "FY2021": -71}),
    ("DATA", "Other liabilities", {"FY2025": -21, "FY2024": -3, "FY2023": 16, "FY2022": 3, "FY2021": 1}),
    ("TOTAL", "Net change in operating assets and liabilities", {"FY2025": 51, "FY2024": 891, "FY2023": -121, "FY2022": -95, "FY2021": -3}),
    ("SECTION", "Corporation taxes", {}),
    ("DATA", "Corporation taxes (paid)/received", {"FY2025": -19, "FY2024": 9, "FY2023": -3, "FY2022": 7, "FY2021": -7}),
    ("TOTAL", "Net cash flows from operating activities", {"FY2025": 68, "FY2024": 898, "FY2023": -119, "FY2022": -47, "FY2021": 20}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Investments in other entities", {"FY2022": -3}),
    ("DATA", "Purchase of property, plant and equipment and intangible assets", {"FY2025": -5, "FY2024": -4, "FY2023": -13, "FY2022": -8, "FY2021": -3}),
    ("DATA", "Proceeds from sale of property, plant and equipment and intangible assets", {"FY2025": 1}),
    ("TOTAL", "Net cash flows from investing activities", {"FY2025": -4, "FY2024": -4, "FY2023": -13, "FY2022": -11, "FY2021": -3}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Issue of other equity instruments", {"FY2022": 50}),
    ("DATA", "Dividends paid on ordinary shares", {"FY2025": -12, "FY2024": -2, "FY2023": -4, "FY2022": -65, "FY2021": -8}),
    ("DATA", "Dividends paid on preference shares and other equity instruments", {"FY2025": -5, "FY2024": -4, "FY2023": -5}),
    ("DATA", "Principal elements of lease payments", {"FY2025": -1, "FY2024": -1, "FY2021": -1}),
    ("TOTAL", "Net cash flows from financing activities", {"FY2025": -18, "FY2024": -7, "FY2023": -9, "FY2022": -15, "FY2021": -9}),
    ("TOTAL", "Change in cash and cash equivalents", {"FY2025": 46, "FY2024": 887, "FY2023": -141, "FY2022": -73, "FY2021": 8}),
    ("DATA", "Cash and cash equivalents at beginning of the year", {"FY2025": 3204, "FY2024": 2318, "FY2023": 2460, "FY2022": 2532, "FY2021": 2524}),
    ("DATA", "Effects of exchange rate changes on cash and cash equivalents", {"FY2024": -1, "FY2023": -1, "FY2022": 1, "FY2021": 0}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2025": 3250, "FY2024": 3204, "FY2023": 2318, "FY2022": 2460, "FY2021": 2532}),
    ("SECTION", "Cash and cash equivalents consist of", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 3223, "FY2024": 3186, "FY2023": 2308, "FY2022": 2445, "FY2021": 2355}),
    ("DATA", "Less: restricted balances", {"FY2023": -17, "FY2022": -18, "FY2021": -17}),
    ("DATA", "Other cash equivalents", {"FY2025": 27, "FY2024": 18, "FY2023": 27, "FY2022": 33, "FY2021": 194}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2025": 3250, "FY2024": 3204, "FY2023": 2318, "FY2022": 2460, "FY2021": 2532}),
]

STATEMENT_SOURCES = (
    "Sources - Santander Financial Services plc own audited Balance Sheet / Income Statement / Statement of Changes "
    "in Equity, £m:\n"
    f"FY2025 and FY2024: SFS 2025 Annual Report, primary financial statements (printed p.46/47/49) - {AR2025}\n"
    f"FY2023 and FY2022: SFS 2023 Annual Report, primary financial statements (printed p.47/48/50) - {AR2023}\n"
    f"FY2022 and FY2021: SFS 2022 Annual Report, primary financial statements (printed p.46/47/49) - {AR2022}\n"
    f"FY2021: SFS 2021 Annual Report, primary financial statements (printed p.46/47/49) - {AR2021}\n\n"
    "Each year's own originally-published column is used throughout (not a later comparative), except FY2024, which "
    "has no standalone SFS annual report of its own and is taken from the 2025 report's 2024 comparative column - "
    "cross-checked and found to agree exactly where both are available. PRESENTATION NOTE: the Income Statement's "
    "OCI/comprehensive-income lines use 1-decimal-place £m; the Statement of Changes in Equity rounds the same "
    "movements to whole £m - both are reproduced exactly as SFS itself presents them, so the two sheets' OCI/total "
    "comprehensive income figures for the same year differ by rounding only (e.g. FY2025: £26.4m on the Income "
    "Statement vs £26m on the equity roll-forward). 'Other equity instruments' (AT1-style capital) was first issued "
    "in FY2022 and 'Cash flow hedging' reserve first appears from FY2023 - blank cells before each existed, not a "
    "disclosure gap. 'Interests in other entities' only appears as its own Balance Sheet line FY2022-FY2023. Fee and "
    "commission income/expense were only split into separate lines from FY2022 onward; FY2021's own report discloses "
    "only the combined 'Net fee and commission expense' line.\n\n" + ENTITY_NOTE
)

BS_ROWS = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 3223, "FY2024": 3186, "FY2023": 2308, "FY2022": 2445, "FY2021": 2355}),
    ("DATA", "Derivative financial instruments", {"FY2025": 24, "FY2024": 27, "FY2023": 10, "FY2022": 13, "FY2021": 27}),
    ("DATA", "Other financial assets at fair value through profit or loss", {"FY2025": 282, "FY2024": 279, "FY2023": 309, "FY2022": 296, "FY2021": 441}),
    ("DATA", "Loans and advances to banks", {"FY2025": 38, "FY2024": 18, "FY2023": 92, "FY2022": 57, "FY2021": 227}),
    ("DATA", "Loans and advances to customers", {"FY2025": 3373, "FY2024": 3546, "FY2023": 3834, "FY2022": 4180, "FY2021": 3521}),
    ("DATA", "Interests in other entities", {"FY2023": 3, "FY2022": 3}),
    ("DATA", "Macro hedge of interest rate risk", {"FY2025": 1, "FY2024": 1, "FY2023": 2}),
    ("DATA", "Property, plant and equipment", {"FY2025": 22, "FY2024": 21, "FY2023": 19, "FY2022": 13, "FY2021": 7}),
    ("DATA", "Current tax assets", {"FY2025": 8, "FY2023": 3}),
    ("DATA", "Deferred tax assets", {"FY2025": 2, "FY2024": 3, "FY2023": 4, "FY2022": 5, "FY2021": 6}),
    ("DATA", "Other assets", {"FY2025": 4, "FY2024": 6, "FY2023": 6, "FY2022": 5, "FY2021": 5}),
    ("TOTAL", "Total assets", {"FY2025": 6977, "FY2024": 7087, "FY2023": 6590, "FY2022": 7017, "FY2021": 6589}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2025": 26, "FY2024": 14, "FY2023": 2, "FY2022": 4, "FY2021": 31}),
    ("DATA", "Deposits by customers", {"FY2025": 6585, "FY2024": 6707, "FY2023": 6152, "FY2022": 6575, "FY2021": 5969}),
    ("DATA", "Derivative financial instruments", {"FY2025": 23, "FY2024": 13, "FY2023": 69, "FY2022": 56, "FY2021": 237}),
    ("DATA", "Other liabilities", {"FY2025": 9, "FY2024": 9, "FY2023": 9, "FY2022": 14, "FY2021": 10}),
    ("DATA", "Provisions", {"FY2025": 5, "FY2024": 16, "FY2023": 3, "FY2022": 2, "FY2021": 2}),
    ("DATA", "Current tax liabilities", {"FY2024": 8, "FY2022": 15, "FY2021": 14}),
    ("TOTAL", "Total liabilities", {"FY2025": 6648, "FY2024": 6767, "FY2023": 6235, "FY2022": 6666, "FY2021": 6263}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 250, "FY2024": 250, "FY2023": 250, "FY2022": 250, "FY2021": 250}),
    ("DATA", "Other equity instruments", {"FY2025": 50, "FY2024": 50, "FY2023": 50, "FY2022": 50}),
    ("DATA", "Other reserves (cash flow hedging)", {"FY2025": 1, "FY2024": -2, "FY2023": 1}),
    ("DATA", "Retained earnings", {"FY2025": 28, "FY2024": 22, "FY2023": 54, "FY2022": 51, "FY2021": 76}),
    ("TOTAL", "Total equity", {"FY2025": 329, "FY2024": 320, "FY2023": 355, "FY2022": 351, "FY2021": 326}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 6977, "FY2024": 7087, "FY2023": 6590, "FY2022": 7017, "FY2021": 6589}),
]

IS_ROWS = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest and similar income", {"FY2025": 268.0, "FY2024": 280.7, "FY2023": 235.1, "FY2022": 111.6, "FY2021": 67.4}),
    ("DATA", "Interest expense and similar charges", {"FY2025": -224.8, "FY2024": -268.3, "FY2023": -225.8, "FY2022": -62.4, "FY2021": -16.4}),
    ("TOTAL", "Net interest income", {"FY2025": 43.2, "FY2024": 12.4, "FY2023": 9.3, "FY2022": 49.2, "FY2021": 51.0}),
    ("DATA", "Fee and commission income", {"FY2025": 5.5, "FY2024": 1.9, "FY2023": 2.1, "FY2022": 1.9}),
    ("DATA", "Fee and commission expense", {"FY2025": -5.8, "FY2024": -7.6, "FY2023": -8.6, "FY2022": -8.4}),
    ("TOTAL", "Net fee and commission expense", {"FY2025": -0.3, "FY2024": -5.7, "FY2023": -6.5, "FY2022": -6.5, "FY2021": -6.9}),
    ("DATA", "Other operating income", {"FY2025": 10.4, "FY2024": 11.5, "FY2023": 21.6, "FY2022": 18.9, "FY2021": 5.5}),
    ("TOTAL", "Total operating income", {"FY2025": 53.3, "FY2024": 18.2, "FY2023": 24.4, "FY2022": 61.6, "FY2021": 49.6}),
    ("SECTION", "Impairment, provisions and expenses", {}),
    ("DATA", "Operating expenses before credit impairment charges, provisions and charges", {"FY2025": -23.1, "FY2024": -24.7, "FY2023": -25.1, "FY2022": -23.6, "FY2021": -23.1}),
    ("DATA", "Credit impairment charges/(release)", {"FY2025": 0.1, "FY2024": 0.2, "FY2023": -0.6, "FY2022": -0.7, "FY2021": -0.1}),
    ("DATA", "Provisions for other liabilities and charges", {"FY2025": -2.7, "FY2024": -16.7, "FY2023": -1.7, "FY2022": -1.6, "FY2021": -2.1}),
    ("TOTAL", "Total credit impairment charges, provisions and charges", {"FY2025": -2.6, "FY2024": -16.5, "FY2023": -2.3, "FY2022": -2.3, "FY2021": -2.2}),
    ("TOTAL", "Profit/(loss) before tax", {"FY2025": 27.6, "FY2024": -23.0, "FY2023": -3.0, "FY2022": 35.7, "FY2021": 24.3}),
    ("DATA", "Tax charge/(credit)", {"FY2025": -4.2, "FY2024": -3.4, "FY2023": 15.0, "FY2022": 4.0, "FY2021": 2.4}),
    ("TOTAL", "Profit/(loss) after tax", {"FY2025": 23.4, "FY2024": -26.4, "FY2023": 12.0, "FY2022": 39.7, "FY2021": 26.7}),
    ("SECTION", "Other comprehensive income/(expense)", {}),
    ("DATA", "Cash flow hedges - effective portion of changes in fair value", {"FY2025": 4.5, "FY2024": -4.4, "FY2023": 1.4}),
    ("DATA", "Cash flow hedges - income statement transfers", {"FY2025": -0.6, "FY2024": 1.5}),
    ("DATA", "Cash flow hedges - taxation", {"FY2025": -0.8, "FY2024": 0.5}),
    ("DATA", "Currency translation on foreign operations", {"FY2025": -0.1}),
    ("TOTAL", "Total other comprehensive income/(expense), net of tax", {"FY2025": 3.0, "FY2024": -2.4, "FY2023": 1.4}),
    ("TOTAL", "Total comprehensive income/(expense)", {"FY2025": 26.4, "FY2024": -28.8, "FY2023": 13.4, "FY2022": 39.7, "FY2021": 26.7}),
]

EQ_HEADERS = ["Share capital", "Other equity instruments", "Cash flow hedging reserve", "Retained earnings", "Total equity"]
EQ_ROWS = [
    ("TOTAL", "At 1 January 2021", (250, None, None, 57, 307)),
    ("DATA", "Profit after tax", (None, None, None, 27, 27)),
    ("TOTAL", "Total comprehensive income", (None, None, None, 27, 27)),
    ("DATA", "Dividends on ordinary shares", (None, None, None, -8, -8)),
    ("TOTAL", "At 31 December 2021 / 1 January 2022", (250, None, None, 76, 326)),
    ("DATA", "Issue of other equity instruments", (None, 50, None, None, 50)),
    ("DATA", "Profit after tax", (None, None, None, 40, 40)),
    ("TOTAL", "Total comprehensive income", (None, None, None, 40, 40)),
    ("DATA", "Dividends on ordinary shares", (None, None, None, -65, -65)),
    ("TOTAL", "At 31 December 2022 / 1 January 2023", (250, 50, 0, 51, 351)),
    ("DATA", "Profit after tax", (None, None, None, 12, 12)),
    ("DATA", "Other comprehensive income - cash flow hedges, net of tax", (None, None, 1, None, 1)),
    ("TOTAL", "Total comprehensive income", (None, None, 1, 12, 13)),
    ("DATA", "Dividends on ordinary shares", (None, None, None, -4, -4)),
    ("DATA", "Dividends on other equity instruments", (None, None, None, -5, -5)),
    ("TOTAL", "At 31 December 2023 / 1 January 2024", (250, 50, 1, 54, 355)),
    ("DATA", "Loss after tax", (None, None, None, -26, -26)),
    ("DATA", "Other comprehensive expense - cash flow hedges, net of tax", (None, None, -3, None, -3)),
    ("TOTAL", "Total comprehensive expense", (None, None, -3, -26, -29)),
    ("DATA", "Dividends on ordinary shares", (None, None, None, -2, -2)),
    ("DATA", "Dividends on other equity instruments", (None, None, None, -4, -4)),
    ("TOTAL", "At 31 December 2024 / 1 January 2025", (250, 50, -2, 22, 320)),
    ("DATA", "Profit after tax", (None, None, None, 23, 23)),
    ("DATA", "Other comprehensive income - cash flow hedges, net of tax", (None, None, 3, None, 3)),
    ("TOTAL", "Total comprehensive income", (None, None, 3, 23, 26)),
    ("DATA", "Dividends on ordinary shares", (None, None, None, -12, -12)),
    ("DATA", "Dividends on other equity instruments", (None, None, None, -5, -5)),
    ("TOTAL", "At 31 December 2025", (250, 50, 1, 28, 329)),
]

bw = BankWorkbook(bank_name="Santander Financial Services plc", years=YEARS, header_color="EC0000")
bw.add_balance_sheet_sheet(
    title="Santander Financial Services plc — Balance Sheet",
    subtitle="Standalone company basis, £m. See source note for entity and comparative-column conventions.",
    rows=BS_ROWS, sources_text=STATEMENT_SOURCES, first_col_width=72, source_height=280, unit_suffix=" (£m)",
)
bw.add_income_statement_sheet(
    title="Santander Financial Services plc — Profit & Loss",
    subtitle="Standalone company basis, £m. See source note for entity and comparative-column conventions.",
    rows=IS_ROWS, sources_text=STATEMENT_SOURCES, first_col_width=72, source_height=280, unit_suffix=" (£m)",
)
bw.add_equity_changes_sheet(
    title="Santander Financial Services plc — Statement of Changes in Equity",
    subtitle="Standalone company basis, £m, chronological roll-forward. See source note for entity and comparative-column conventions.",
    headers=EQ_HEADERS, rows=EQ_ROWS, sources_text=STATEMENT_SOURCES, first_col_width=46, source_height=280,
)
bw.add_cash_flow_sheet(
    title="Santander Financial Services plc — Cash Flow Statement",
    subtitle="Standalone company basis, £m. See source note for entity and comparative-column conventions.",
    rows=rows, sources_text=CASH_SOURCES, first_col_width=72, source_height=260, unit_suffix=" (£m)",
)

AQ_SOURCES = (
    "Sources - Santander Financial Services plc own audited Credit quality note, £m:\n"
    f"FY2025 and FY2024 (gross exposure by product and by IFRS 9 stage): SFS 2025 Annual Report, Risk review, "
    f"Credit quality (printed p.31/32) - {AR2025}\n"
    f"FY2023 and FY2022 (gross exposure by product and by IFRS 9 stage): SFS 2023 Annual Report, Risk review, "
    f"Credit quality (printed p.31/32) - {AR2023}\n"
    f"FY2021 (gross exposure by product only, no IFRS 9 stage split disclosed that year): SFS 2021 Annual Report, "
    f"Risk review, 'Our maximum and net exposure to credit risk' (printed p.28) - {AR2021}\n\n"
    "FY2022's by-stage figures are only available from the 2023 report's 2022 comparative column - the 2022 report "
    "itself (and the 2021 report) present credit risk in a different, non-IFRS-9-stage table format ('maximum "
    "exposure' by gross/net amounts, not by stage), so no earlier-published stage split exists for FY2022 or FY2021. "
    "FY2021's own report additionally rounds to the nearest £0.1bn rather than £1m, and shows loss allowances as nil "
    "at that rounding - so no FY2021 ECL/stage/ratio figures are populated; this is a genuine disclosure-format gap, "
    "not an estimate. 'Total ECL' is disclosed by SFS as a single per-stage total across the whole loan book, not "
    "broken out by product - the ECL rows below reproduce that structure exactly. Asset quality ratios are derived: "
    "ECL coverage ratio = Total ECL / Total gross loans (by-stage total); Stage 3 (NPL) ratio = Stage 3 gross loans / "
    "Total gross loans; Stage 3 coverage ratio = Stage 3 ECL / Stage 3 gross loans.\n\n" + ENTITY_NOTE
)

AQ_ROWS = [
    ("SECTION", "Gross loans and advances to customers, by product", {}),
    ("DATA", "Crown Dependencies", {"FY2025": 1456, "FY2024": 1333, "FY2023": 1256, "FY2022": 1144, "FY2021": 700}),
    ("DATA", "UK residential mortgages", {"FY2025": 1734, "FY2024": 2015, "FY2023": 2380, "FY2022": 2824, "FY2021": 2600}),
    ("DATA", "Other", {"FY2025": 183, "FY2024": 199, "FY2023": 200, "FY2022": 212, "FY2021": 200}),
    ("TOTAL", "Total gross loans and advances to customers", {"FY2025": 3373, "FY2024": 3547, "FY2023": 3836, "FY2022": 4180, "FY2021": 3500}),
    ("SECTION", "Gross loans and advances to customers, by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (performing)", {"FY2025": 3184, "FY2024": 3330, "FY2023": 3542, "FY2022": 4020}),
    ("DATA", "Stage 2 (underperforming)", {"FY2025": 172, "FY2024": 204, "FY2023": 285, "FY2022": 155}),
    ("DATA", "Stage 3 (credit-impaired)", {"FY2025": 17, "FY2024": 13, "FY2023": 9, "FY2022": 5}),
    ("TOTAL", "Total gross loans and advances to customers (by stage)", {"FY2025": 3373, "FY2024": 3547, "FY2023": 3836, "FY2022": 4180}),
    ("SECTION", "ECL allowance, by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (performing)", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": -1}),
    ("DATA", "Stage 2 (underperforming)", {"FY2025": 0, "FY2024": 0, "FY2023": -1, "FY2022": -1}),
    ("DATA", "Stage 3 (credit-impaired)", {"FY2025": -1, "FY2024": -1, "FY2023": -1, "FY2022": 0}),
    ("TOTAL", "Total ECL allowance", {"FY2025": -1, "FY2024": -1, "FY2023": -2, "FY2022": -2}),
    ("SECTION", "Asset quality ratios", {}),
    ("DATA", "ECL coverage ratio (Total ECL / Total gross loans)", {"FY2025": "0.03%", "FY2024": "0.03%", "FY2023": "0.05%", "FY2022": "0.05%"}),
    ("DATA", "Stage 3 (NPL) ratio (Stage 3 gross loans / Total gross loans)", {"FY2025": "0.50%", "FY2024": "0.37%", "FY2023": "0.23%", "FY2022": "0.12%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 ECL / Stage 3 gross loans)", {"FY2025": "5.88%", "FY2024": "7.69%", "FY2023": "11.11%", "FY2022": "0.00%"}),
]
bw.add_asset_quality_sheet(
    title="Santander Financial Services plc — Asset Quality / Credit Risk Disclosures",
    subtitle="Standalone company basis, £m. See source note for entity and IFRS 9 stage-disclosure conventions.",
    rows=AQ_ROWS, sources_text=AQ_SOURCES, first_col_width=64, source_height=260, unit_suffix=" (£m)",
)

CAPITAL_SOURCES = (
    "Sources - Santander Financial Services plc own audited regulatory-capital tables in its Annual Reports, £m:\n"
    f"FY2025/FY2024: SFS 2025 Annual Report, Risk review p.39 - {AR2025}\n"
    f"FY2023/FY2022: SFS 2023 Annual Report, Risk review p.39 - {AR2023}\n"
    f"FY2022/FY2021: SFS 2022 Annual Report, Risk review p.39 - {AR2022}\n"
    f"FY2021: SFS 2021 Annual Report, Risk review p.39 - {AR2021}\n\n" + ENTITY_NOTE
)

def metric(name, unit, data, note=None):
    bw.add_metric_sheet(name, unit, data, CAPITAL_SOURCES, note=note, first_col_width=52, source_height=170)

metric("CET1 Capital", "£m", [("CET1 capital", {"FY2025": 249, "FY2024": 266, "FY2023": 288, "FY2022": 256, "FY2021": 293})])
metric("CET1 Ratio", "%", [("CET1 capital ratio", {y: "Not publicly disclosed" for y in YEARS})], "The SFS reports disclose CET1 capital amounts but do not disclose a standalone CET1 percentage or RWA in the reviewed reports. No ratio is inferred from other Santander entities.")
metric("Tier 1 Capital", "£m", [("Tier 1 capital", {"FY2025": 299, "FY2024": 316, "FY2023": 338, "FY2022": 306, "FY2021": 293})])
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", {y: "Not publicly disclosed" for y in YEARS})])
metric("Total Capital", "£m", [("Total regulatory capital", {"FY2025": 299, "FY2024": 316, "FY2023": 338, "FY2022": 306, "FY2021": 293})])
metric("Total Capital Ratio", "%", [("Total capital ratio", {y: "Not publicly disclosed" for y in YEARS})])
metric("Total RWAs", "£m", [("Total risk-weighted assets", {y: "Not publicly disclosed" for y in YEARS})])

bw.add_rwa_breakdown_sheet(
    title="Santander Financial Services plc — RWA Breakdown",
    subtitle="Standalone company basis. Not publicly disclosed.",
    rows=[("DATA", "RWA breakdown by risk category", {y: "Not publicly disclosed" for y in YEARS})],
    sources_text=(
        "Sources - reviewed SFS Annual Reports FY2021-FY2025 (see Total RWAs sheet for the same document list).\n\n"
        "SFS's own risk review states it relies on Banco Santander's group Pillar 3 report for CRD IV risk "
        "measurement of its exposures and does not publish its own standalone RWA figure or risk-category "
        "breakdown (UK OV1 template) at the SFS entity level in any of the reviewed reports - confirmed via direct "
        "reading of the Capital Risk section of each report, not an access gap. Santander UK Group Holdings plc's "
        "own disclosures are a different regulatory entity and were not substituted.\n\n" + ENTITY_NOTE
    ),
    first_col_width=54, source_height=190, unit_suffix="",
)

UNAVAILABLE = "Not publicly disclosed at SFS standalone level"
bw.add_not_disclosed_metric_sheets(
    ["Leverage Ratio"], CAPITAL_SOURCES,
    per_note={"Leverage Ratio": "The reviewed SFS annual reports do not provide this metric for the SFS standalone/company basis. Santander UK Group Holdings disclosures are a different regulatory entity and were not substituted."},
)

LIQ_SOURCES = (
    "Sources - SFS own liquidity-risk review, £bn for LCR components and percentages for ratios:\n"
    f"FY2025/FY2024: SFS 2025 Annual Report, Risk review p.37 - {AR2025}\n"
    f"FY2023/FY2022: SFS 2023 Annual Report, Risk review p.37 - {AR2023}\n"
    f"FY2022/FY2021: SFS 2022 Annual Report, Risk review p.37 - {AR2022}\n"
    f"FY2021: SFS 2021 Annual Report, Risk review p.37 - {AR2021}\n\n" + ENTITY_NOTE
)
bw.add_metric_sheet("LCR", "£bn / %", [("Eligible liquidity pool", {"FY2025": 3.5, "FY2024": 3.5, "FY2023": 2.6, "FY2022": 2.7, "FY2021": 2.8}), ("Net stress outflows", {"FY2025": -1.5, "FY2024": -1.9, "FY2023": -1.1, "FY2022": -1.3, "FY2021": -1.4}), ("Eligible liquidity pool as percentage of anticipated net cash flows", {"FY2025": "227%", "FY2024": "186%", "FY2023": "240%", "FY2022": "218%", "FY2021": "206%"})], LIQ_SOURCES, note="LCR is presented in the SFS risk review as the eligible liquidity pool divided by anticipated/net stress cash outflows; the underlying table is in £bn and rounded.", first_col_width=58, source_height=180)
bw.add_metric_sheet("NSFR", "%", [("NSFR ratio", {"FY2025": "148%", "FY2024": "149%", "FY2023": "142%", "FY2022": "127%", "FY2021": "137%"})], LIQ_SOURCES, note="NSFR was described by SFS as implemented from 1 January 2022, but the 2021 report nevertheless states the SFS NSFR at 31 December 2021; values are reproduced as reported.", first_col_width=58, source_height=180)
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], CAPITAL_SOURCES,
    per_note={"MREL Ratio": "The reviewed SFS annual reports do not provide this metric for the SFS standalone/company basis. Santander UK Group Holdings disclosures are a different regulatory entity and were not substituted."},
)

bw.add_overview_sheet(
    cash_flow_totals=[("Net cash flows from operating activities", {"FY2025": 68, "FY2024": 898, "FY2023": -119, "FY2022": -47, "FY2021": 20}), ("Net cash flows from investing activities", {"FY2025": -4, "FY2024": -4, "FY2023": -13, "FY2022": -11, "FY2021": -3}), ("Net cash flows from financing activities", {"FY2025": -18, "FY2024": -7, "FY2023": -9, "FY2022": -15, "FY2021": -9}), ("Cash and cash equivalents at end of year", {"FY2025": 3250, "FY2024": 3204, "FY2023": 2318, "FY2022": 2460, "FY2021": 2532})],
    cash_flow_unit="£m", ratios=[("LCR", {"FY2025": "227%", "FY2024": "186%", "FY2023": "240%", "FY2022": "218%", "FY2021": "206%"}), ("NSFR", {"FY2025": "148%", "FY2024": "149%", "FY2023": "142%", "FY2022": "127%", "FY2021": "137%"})],
    balance_sheet_totals=[("Total assets", {"FY2025": 6977, "FY2024": 7087, "FY2023": 6590, "FY2022": 7017, "FY2021": 6589}), ("Loans and advances to customers", {"FY2025": 3373, "FY2024": 3546, "FY2023": 3834, "FY2022": 4180, "FY2021": 3521}), ("Deposits by customers", {"FY2025": 6585, "FY2024": 6707, "FY2023": 6152, "FY2022": 6575, "FY2021": 5969}), ("Total equity", {"FY2025": 329, "FY2024": 320, "FY2023": 355, "FY2022": 351, "FY2021": 326})],
    balance_sheet_unit="£m",
    income_statement_totals=[("Total operating income", {"FY2025": 53.3, "FY2024": 18.2, "FY2023": 24.4, "FY2022": 61.6, "FY2021": 49.6}), ("Operating expenses before credit impairment charges, provisions and charges", {"FY2025": -23.1, "FY2024": -24.7, "FY2023": -25.1, "FY2022": -23.6, "FY2021": -23.1}), ("Profit/(loss) after tax", {"FY2025": 23.4, "FY2024": -26.4, "FY2023": 12.0, "FY2022": 39.7, "FY2021": 26.7})],
    income_statement_unit="£m",
    equity_changes_totals=[("Opening equity", {"FY2025": 320, "FY2024": 355, "FY2023": 351, "FY2022": 326, "FY2021": 307}), ("Total comprehensive income/(expense) for the year", {"FY2025": 26, "FY2024": -29, "FY2023": 13, "FY2022": 40, "FY2021": 27}), ("Other equity movements, net", {"FY2025": -17, "FY2024": -6, "FY2023": -9, "FY2022": -15, "FY2021": -8}), ("Closing equity", {"FY2025": 329, "FY2024": 320, "FY2023": 355, "FY2022": 351, "FY2021": 326})],
    equity_changes_unit="£m",
    note=ENTITY_NOTE + " All unavailable standalone regulatory ratios remain blank/not disclosed on their detail sheets."
)

bw.save("/Users/armaan/code/katalysis/banks/SANTANDER FINANCIAL SERVICES FINANCIALS.xlsx")
