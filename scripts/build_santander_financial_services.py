import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

AR2025 = "https://assets.santandermedia.com/adobe/assets/urn:aaid:aem:3af8ccd7-5ee0-4196-9577-83a30558e64c/original/as/02536CCAA25SantanderFinancialServicesPlc.pdf"
AR2023 = "https://assets.santandermedia.com/adobe/assets/urn:aaid:aem:8da5f087-d631-4188-9c9c-9671410070c5/original/as/sfs_annual_report_2023.pdf"
AR2022 = "https://assets.santandermedia.com/adobe/assets/urn:aaid:aem:f15fea69-5780-484a-bb22-ce42b29eeac3/original/as/santander_financial_services_plc_2022_annual_report.pdf"
AR2021 = "https://assets.santandermedia.com/adobe/assets/urn:aaid:aem:58592004-0ef9-4156-9df8-367908fc81a9/original/as/sfs_2021_annual_report.pdf"

# Added 2026-09-15. The AR* URLs above are Adobe AEM asset links keyed by opaque
# GUID; these are the same documents on Santander's own public site under stable,
# human-readable paths, and they are what the 2026-09-15 re-verification actually
# read. The FY2024 report was not previously cited at all - FY2024 had been taken
# from the FY2025 report's comparative column - and the FY2020 report is the
# primary source for the FY2021 LCR/liquidity comparatives.
AR2024_SANT = "https://www.santander.co.uk/assets/s3fs-public/documents/Santander%20Financial%20Services%20plc%202024%20Annual%20Report.pdf"
AR2023_SANT = "https://www.santander.co.uk/assets/s3fs-public/documents/sfs_annual_report_2023.pdf"
AR2022_SANT = "https://www.santander.co.uk/assets/s3fs-public/documents/santander_financial_services_plc_2022_annual_report.pdf"
AR2021_SANT = "https://www.santander.co.uk/assets/s3fs-public/documents/sfs_2021_annual_report.pdf"
AR2020_SANT = "https://www.santander.co.uk/assets/s3fs-public/documents/sfs_2020_annual_report.pdf"

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
    f"FY2021: SFS 2021 Annual Report, Risk review p.39 - {AR2021}\n"
    f"FY2024 (primary, added 2026-09-15): SFS 2024 Annual Report, Risk review p.38-39 "
    f"'Regulatory capital resources (audited)' - {AR2024_SANT}\n"
    f"FY2020 (context for the FY2021 comparative): SFS 2020 Annual Report - {AR2020_SANT}\n\n"
    "TEXT-LAYER RE-VERIFICATION 2026-09-15: all five SFS Annual Reports for FY2020-FY2024 were "
    "independently re-downloaded from santander.co.uk as full text-layer PDFs and the regulatory "
    "capital table re-extracted from each. Every capital figure on these sheets reconciles "
    "exactly, and each year is corroborated twice because each report carries the prior year as "
    "a comparative: CET1 capital FY2021 293 (FY2021 and FY2022 reports), FY2022 256 (FY2022 and "
    "FY2023 reports), FY2023 288 (FY2023 and FY2024 reports), FY2024 266 (FY2024 report). "
    "AT1 capital is 50 in FY2022-FY2024 and nil in FY2021, and Total regulatory capital equals "
    "CET1 + AT1 in every single year, confirming no Tier 2 instruments exist - which is why the "
    "Tier 1 Capital and Total Capital sheets carry identical figures. That identity is read off "
    "the disclosed rows, not assumed.\n\n"
    "RATIOS, RWA AND LEVERAGE - PROVEN ABSENT, not an unresearched gap. The 2026-09-15 pass "
    "searched the full extracted text of all five reports for any capital ratio, risk-weighted "
    "asset figure or leverage ratio at this entity's level and found none. The 'Regulatory "
    "capital resources (audited)' table is the entity's only capital disclosure and it contains "
    "five rows only: CET1 capital before regulatory adjustments, CET1 regulatory adjustments, "
    "CET1 capital, AT1 capital, Total regulatory capital. There is no denominator anywhere in "
    "the document, so no ratio can be sourced and none may be derived - deriving RWA from "
    "capital divided by a ratio is barred by project convention, and here there is not even a "
    "ratio to divide by. The only percentages the reports attach to capital are the 7% CET1 "
    "trigger written into the terms of the AT1 securities and the auditors' 0.5%-of-total-assets "
    "materiality threshold; neither is a disclosed capital ratio. Santander's site hosts no "
    "FY2025 SFS report under any tested filename, and an unfiltered Wayback CDX sweep of "
    "santander.co.uk returns SFS annual reports for FY2019-FY2024 only.\n\n" + ENTITY_NOTE
)

# ---------------------------------------------------------------
# KM1 Key Metrics (KM1-026, 2026-09-16)
#
# FINDING: SFS publishes no standalone Pillar 3 document and no KM1 template
# for the entity. Its Annual Reports do contain selected prudential disclosures
# (including regulatory capital, LCR and NSFR); they are not a full Pillar 3
# disclosure. This distinction is supported below, including the check of the
# PARENT's Pillar 3 that this project has twice been caught skipping.
# ---------------------------------------------------------------
ACRMD_2025_URL = "https://www.santander.co.uk/assets/s3fs-public/documents/2025SantanderUKACRMD.pdf"
ACRMD_2024_URL = "https://www.santander.co.uk/assets/s3fs-public/documents/ACRMD%20FINAL_Dec%2024.pdf"

KM1_SOURCES = (
    "Sources - checked 2026-09-16 for KM1-026:\n"
    f"SFS Annual Report 2025 (Risk review; 'Key metrics' headings at credit-risk and capital-risk) - {AR2025}\n"
    f"SFS Annual Report 2024 - {AR2024_SANT}\n"
    f"SFS Annual Report 2023 - {AR2023_SANT}\n"
    f"SFS Annual Report 2022 - {AR2022_SANT}\n"
    f"SFS Annual Report 2021 - {AR2021_SANT}\n"
    f"PARENT'S Pillar 3: Santander UK Group Holdings plc / Santander UK plc Additional Capital and Risk "
    f"Management Disclosures (ACRMD), 31 December 2025 - {ACRMD_2025_URL}\n"
    f"and 31 December 2024 - {ACRMD_2024_URL} (the 2023, 2022, 2021 and 2020 editions were checked the same "
    "way).\n\n"
    "NO STANDALONE PILLAR 3 DOCUMENT OR KM1 EXISTS FOR THIS ENTITY, ON THREE INDEPENDENT CHECKS.\n"
    "SCOPE CLARIFICATION: SFS's Annual Reports do contain selected entity-level prudential disclosures, "
    "including an audited regulatory-capital table and LCR/NSFR figures. The FY2024 report (Risk review, "
    "printed pp.36-38) gives CET1 capital £266m, AT1 £50m and total regulatory capital £316m for FY2024, "
    "and LCR 186% / NSFR 149%; it does not give a KM1 template, RWA breakdown or standalone capital-ratio "
    "figures. It says CRD IV exposure measurement is covered by Banco Santander's Pillar 3 report. The "
    "presence of these selected disclosures is why the claim below is limited to absence of a standalone "
    "Pillar 3 publication/KM1, not absence of all Pillar 3-related information.\n"
    "(1) SFS PUBLISHES NO STANDALONE PILLAR 3 DOCUMENT. Its own investor page - santander.co.uk > About "
    "Santander > Investor relations > Santander Financial Services plc - lists Annual Reports only, one per "
    "year, 2021 through 2025, and nothing else. The FY2025 report is the newest document of any kind there.\n"
    "(2) NO ANNUAL REPORT CONTAINS THE TEMPLATE. All five reports (FY2021-FY2025) were downloaded fresh and "
    "searched case-insensitively across their full text layers. 'KM1', 'key metrics template', 'leverage "
    "ratio' and 'risk-weighted assets' return ZERO hits in every one of the five. Those zeroes are facts about "
    "the documents rather than a failed extraction: the same searches return 84-89 hits for 'capital' in each "
    "report, and the regulatory-capital table itself extracts cleanly (it is the source of the CET1 Capital, "
    "Tier 1 Capital and Total Capital sheets). The phrase 'Key metrics' does appear twice in each report, but "
    "neither occurrence is a table of figures: one heads a prose glossary of credit-risk terms (ECL, Stages "
    "1-3, Stage 3 ratio, Expected Loss) and the other is a single sentence in the capital-risk section - 'The "
    "main metrics we use to measure capital risk are CET1 capital ratio, and total regulatory capital'. Each "
    "report carries only 2-6 embedded images (logos and small charts), so no table is hiding in a bitmap.\n"
    "(3) THE PARENT'S PILLAR 3 CARRIES NO SFS BLOCK EITHER - checked explicitly, because a UK subsidiary's "
    "numbers normally live in its parent's Pillar 3 rather than in a document of its own. All six ACRMD "
    "editions (FY2020-FY2025) were searched for 'Santander Financial Services', 'Abbey National Treasury' and "
    "'SFS'. The full entity name returns ZERO hits in every edition; 'SFS' appears only inside one narrative "
    "sentence about liquidity governance ('We monitor and manage liquidity risk for the Santander UK plc group "
    "and SFS separately'), with no figures attached. Again the extraction is demonstrably rich - the FY2025 "
    "edition returns 286 hits for 'capital', 59 for 'cet1' and 66 for 'leverage ratio' - so the zero is about "
    "the document. Each ACRMD prints the KM1 template exactly twice, for two entities that are NOT this one: "
    "Part 1 for the Santander UK Group Holdings plc group and Part 2 for the Santander UK plc (RFB) group.\n"
    "WHY, STRUCTURALLY. SFS sits OUTSIDE the ring-fence, in the Non-RFB Sub-Group alongside Santander UK Group "
    "Holdings plc and Santander Equity Investments Limited (FY2025 report, Risk review, capital-risk section: "
    "the three were party to a Non-RFB Sub-Group Capital Support Deed dated 3 December 2024 and were permitted "
    "by the PRA to form a core UK group). Its individual disclosures are made through the consolidated group "
    "rather than separately: the FY2025 report states, under Risk measurement, 'We apply Banco Santander's "
    "approach to capital measurement and risk management for CRD IV. For more on the CRD IV risk measurement "
    "of our exposures, see Banco Santander's Pillar 3 report.' That is the bank's own explanation of why it "
    "prints no template of its own.\n"
    "NOT AN SDDT EXEMPTION. The PRA consolidated waivers list records five entries for Santander Financial "
    "Services plc (FRN 146003) - Capital Buffers rules CA.BU.5.1-5.5, Core Large Exposures under CRR Articles "
    "113(6) and 429a(1), an IRB model permission and a resolution-assessment modification. None is a "
    "Disclosure (CRR) waiver and none is the SDDT Regime Rule 3.1 opt-in, so the absence here is a "
    "consolidated-group disclosure arrangement, not a regulatory exemption from disclosing.\n"
    "ONE CHECK COULD NOT BE COMPLETED AND IS RECORDED AS BLOCKED, NOT AS AN ABSENCE. Banco Santander SA's own "
    "group Pillar 3 report - the document SFS's Risk review points to - could not be retrieved this session: "
    "santander.com's Pillar 3 page renders its document list client-side and returned 'No results found' to "
    "every server-side fetch, and three plausible direct PDF paths all returned HTTP 404 with Content-Type "
    "text/html. That is a statement about our reach, not about the document. It does not weaken the finding "
    "above, because Banco Santander's group Pillar 3 is a consolidated report for the Spanish group in euros: "
    "a UK sub-subsidiary's own KM1 template would not be in it, and the immediate UK parent's Pillar 3, which "
    "is where UK Disclosure (CRR) would put one, has been checked in full and does not carry it.\n"
    "LATEST-EDITION CHECK 2026-09-16, on santander.co.uk's own investor-relations pages rather than this "
    "project's cited URLs: newest SFS Annual Report = FY2025 (31 December 2025), which is already this "
    "workbook's newest year; newest parent ACRMD = 31 December 2025, plus interim 2026 half-yearly and Q1-26 "
    "editions that do not constitute a new full year. Nothing newer to transcribe.\n\n"
    + ENTITY_NOTE
)

bw.add_km1_sheet(
    title="Santander Financial Services plc - KM1 Key Metrics",
    subtitle="No standalone Pillar 3/KM1 published. SFS Annual Reports contain selected prudential data, but neither its own "
             "Annual Reports nor its parent's Pillar 3 (the Santander UK ACRMD) contains a KM1 key-metrics "
             "template for this entity. See the source note for the three checks behind that statement.",
    rows=[
        ("DATA", "UK KM1 template - no standalone SFS Pillar 3/KM1 publication",
         {y: f"Not published – no standalone SFS Pillar 3/KM1; SFS {y} annual report has no KM1 and the parent's "
             "ACRMD prints KM1 only for Santander UK Group Holdings and the RFB group; see note"
          for y in YEARS}),
    ],
    sources_text=KM1_SOURCES,
    first_col_width=64,
    source_height=300,
)


# GA-020 (2026-09-19): bare cells reclassified NOT PUBLISHED on evidence. All five SFS
# annual reports (FY2021-FY2025) were re-downloaded today (%PDF) and their text layers probed:
# 'tier 1 ratio' 0, 'total capital ratio' 0, 'mrel'/'eligible liabilities'/'loss-absorbing' 0 in
# every one; 'risk-weighted' occurs only in "exposures are risk-weighted at 0%" (core UK group
# permission) and 'leverage' only in "leverage exposure measure" narrative - no RWA or leverage
# ratio figure. 'CET1 capital ratio' occurs only in the capital-risk sentence naming it as a
# metric and in an AT1 write-down trigger clause; the regulatory capital table (e.g. FY2025
# Risk review, 'Regulatory capital resources') prints amounts only. ~85 'capital' hits each
# (positive control). No standalone SFS Pillar 3/KM1 exists (KM1_SOURCES); selected prudential
# disclosures are in the Annual Reports. Not SDDT (PRA waivers register).
def _sfs_np(what):
    return {y: f"Not published – SFS {y} annual report prints no {what} (capital table gives amounts "
               "only); selected prudential disclosures appear in the Annual Report, but no standalone "
               "SFS Pillar 3/KM1 is published; see note" for y in YEARS}


def metric(name, unit, data, note=None):
    bw.add_metric_sheet(name, unit, data, CAPITAL_SOURCES, note=note, first_col_width=52, source_height=170)

metric("CET1 Capital", "£m", [("CET1 capital", {"FY2025": 249, "FY2024": 266, "FY2023": 288, "FY2022": 256, "FY2021": 293})])
metric("CET1 Ratio", "%", [("CET1 capital ratio", _sfs_np("CET1 ratio"))], "The SFS reports disclose CET1 capital amounts but do not disclose a standalone CET1 percentage or RWA in the reviewed reports. No ratio is inferred from other Santander entities.")
metric("Tier 1 Capital", "£m", [("Tier 1 capital", {"FY2025": 299, "FY2024": 316, "FY2023": 338, "FY2022": 306, "FY2021": 293})])
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", _sfs_np("Tier 1 ratio"))])
metric("Total Capital", "£m", [("Total regulatory capital", {"FY2025": 299, "FY2024": 316, "FY2023": 338, "FY2022": 306, "FY2021": 293})])
metric("Total Capital Ratio", "%", [("Total capital ratio", _sfs_np("total capital ratio"))])
metric("Total RWAs", "£m", [("Total risk-weighted assets", _sfs_np("RWA figure"))])

bw.add_rwa_breakdown_sheet(
    title="Santander Financial Services plc — RWA Breakdown",
    subtitle="Standalone company basis. Not publicly disclosed.",
    rows=[("DATA", "RWA breakdown by risk category", _sfs_np("RWA figure or breakdown"))],
    sources_text=(
        "Sources - reviewed SFS Annual Reports FY2021-FY2025 (see Total RWAs sheet for the same document list).\n\n"
        "SFS's own risk review states it relies on Banco Santander's group Pillar 3 report for CRD IV risk "
        "measurement of its exposures and does not publish its own standalone RWA figure or risk-category "
        "breakdown (UK OV1 template) at the SFS entity level in any of the reviewed reports - confirmed via direct "
        "reading of the Capital Risk section of each report, not an access gap. Santander UK Group Holdings plc's "
        "own disclosures are a different regulatory entity and were not substituted.\n\n"
        "RE-VERIFIED 2026-09-12 (independent re-check): the FY2025 Annual Report was re-downloaded and read "
        "directly. Its Capital Risk section states verbatim: 'We apply Banco Santander's approach to capital "
        "measurement and risk management for CRD IV. For more on the CRD IV risk measurement of our exposures, "
        "see Banco Santander's Pillar 3 report.' The report gives CET1 capital as a GBP amount (FY2025 GBP249m, "
        "FY2024 GBP266m - already on the CET1 Capital sheet) but no RWA figure anywhere, which is why every "
        "RWA-denominated ratio (CET1/Tier 1/Total Capital Ratio) and the RWA breakdown are absent: SFS's "
        "risk-weighted exposures are measured and published only within Banco Santander's group Pillar 3, never "
        "at SFS entity level. This is a structural consequence of the group's disclosure architecture, not a "
        "document this project failed to obtain. Entity-level LCR and NSFR ARE disclosed and are captured on "
        "their own sheets - SFS states its liquidity risk 'is monitored and managed separately from the rest of "
        "the Santander UK group', which is why those two exist at entity level while the capital ratios do "
        "not.\n\n" + ENTITY_NOTE
    ),
    first_col_width=54, source_height=190, unit_suffix="",
)

UNAVAILABLE = "Not publicly disclosed at SFS standalone level"
bw.add_not_disclosed_metric_sheets(
    ["Leverage Ratio"], CAPITAL_SOURCES,
    statements={"Leverage Ratio": _sfs_np("leverage ratio")},
    per_note={"Leverage Ratio": "The reviewed SFS annual reports do not provide this metric for the SFS standalone/company basis. Santander UK Group Holdings disclosures are a different regulatory entity and were not substituted."},
)

LIQ_SOURCES = (
    "Sources - SFS own liquidity-risk review, £bn for LCR components and percentages for ratios:\n"
    f"FY2025/FY2024: SFS 2025 Annual Report, Risk review p.37 - {AR2025}\n"
    f"FY2023/FY2022: SFS 2023 Annual Report, Risk review p.37 - {AR2023}\n"
    f"FY2022/FY2021: SFS 2022 Annual Report, Risk review p.37 - {AR2022}\n"
    f"FY2021: SFS 2021 Annual Report, Risk review p.37 - {AR2021}\n"
    f"FY2024 (primary, added 2026-09-15): SFS 2024 Annual Report, Risk review p.36-37 - {AR2024_SANT}\n\n"
    "BASIS WARNING - THESE ARE POINT-IN-TIME RATIOS, NOT 12-MONTH AVERAGES. SFS does not publish "
    "a UK KM1 template. The figure captured here is the row the reports label 'Eligible liquidity "
    "pool as a percentage of anticipated net cash flows', measured at the 31 December balance "
    "sheet date. Most banks in this project whose LCR comes from a Pillar 3 KM1 table are "
    "reporting a 12-month average instead, and the two bases can diverge very widely - "
    "divergences of 89 to 470 percentage points have been found elsewhere in this dataset. Do "
    "not rank or trend SFS's LCR directly against a KM1-sourced LCR without noting the "
    "difference. SFS's own reports show how large the gap can be within a single entity: the "
    "FY2021 report's table prints the LCR measure at 206% (2021) and 165% (2020) beside an LRA "
    "stress measure of 184% and 168% for the same two dates.\n\n"
    "RE-VERIFICATION 2026-09-15: re-extracted from text-layer PDFs of the FY2020-FY2024 reports. "
    "Every LCR and NSFR value below FY2025 is confirmed by two independent reports, since each "
    "year's figure reappears as the following year's comparative - LCR FY2021 206%, FY2022 218%, "
    "FY2023 240%, FY2024 186%; NSFR FY2021 137%, FY2022 127%, FY2023 142%, FY2024 149%. The "
    "FY2021 NSFR is genuine and deliberately retained: the UK NSFR requirement only took effect "
    "on 1 January 2022, and across this project pre-2022 NSFR blanks are treated as structural, "
    "but SFS chose to monitor and publish the ratio a year early and its FY2021 report states "
    "the figure outright ('At 31 December 2021, the SFS NSFR was 137%'), corroborated by the "
    "FY2022 report's comparative.\n\n" + ENTITY_NOTE
)
bw.add_metric_sheet("LCR", "£bn / %", [("Eligible liquidity pool", {"FY2025": 3.5, "FY2024": 3.5, "FY2023": 2.6, "FY2022": 2.7, "FY2021": 2.8}), ("Net stress outflows", {"FY2025": -1.5, "FY2024": -1.9, "FY2023": -1.1, "FY2022": -1.3, "FY2021": -1.4}), ("Eligible liquidity pool as percentage of anticipated net cash flows", {"FY2025": "227%", "FY2024": "186%", "FY2023": "240%", "FY2022": "218%", "FY2021": "206%"})], LIQ_SOURCES, note="LCR is presented in the SFS risk review as the eligible liquidity pool divided by anticipated/net stress cash outflows; the underlying table is in £bn and rounded.", first_col_width=58, source_height=180)
bw.add_metric_sheet("NSFR", "%", [("NSFR ratio", {"FY2025": "148%", "FY2024": "149%", "FY2023": "142%", "FY2022": "127%", "FY2021": "137%"})], LIQ_SOURCES, note="NSFR was described by SFS as implemented from 1 January 2022, but the 2021 report nevertheless states the SFS NSFR at 31 December 2021; values are reproduced as reported.", first_col_width=58, source_height=180)
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], CAPITAL_SOURCES,
    statements={"MREL Ratio": _sfs_np("MREL figure")},
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
