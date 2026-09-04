import sys, os

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first

AR25_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/financial-results-and-reports/2025/TSB-Bank-ARA-2025.pdf"
AR24_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/financial-results-and-reports/2024/TSB-Bank-ARA-2024.pdf"
AR23_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/financial-results-and-reports/2023/TSB-Bank-2023.pdf"
AR21_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/financial-results-and-reports/2021/tsb-bank-ara-2021.pdf"

P3_25_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/rns/tsb-large-subsidiary-disclosure-2025.pdf"
P3_24_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/rns/TSB-Large-subsidiary-Disclosure-2024.pdf"
P3_23_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/rns/TSB-large-subsidiary-disclosure-2023.pdf"
P3_22_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/rns/TSB-Large-subsidiary-Disclosure-2022.pdf"
P3_21_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/rns/TSB-Large-Subsidiary-Disclosure-2021.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: TSB Bank plc (Companies House SC095237) is the entity on the PRA register; its own Annual "
    "Report and Accounts (consolidated 'Bank (Consolidated)' column used throughout) is used for the cash flow "
    "statement. TSB Banking Group plc's only direct subsidiary is TSB Bank plc, so 'TSB Banking Group plc' "
    "consolidated Pillar 3 disclosures (published under that name, as TSB is a 'large subsidiary' of Banco "
    "Sabadell for CRR Article 13 purposes) are effectively the same consolidation scope and are used for all "
    "Pillar 3 metric sheets.\n"
    "CONTEXT: TSB was owned by Banco de Sabadell, S.A. (Spain) throughout FY2021-FY2025. Santander UK plc agreed "
    "to acquire TSB in July 2025 and completed the acquisition on 30 April 2026 (after this workbook's FY2025 "
    "year-end) - so all 5 years of data here reflect the Sabadell-owned period; TSB's board ceased dividend "
    "payments to Sabadell following the announcement per TSB's FY2025 Pillar 3 disclosure."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are TSB Bank plc, Bank (Consolidated) basis, £ million.\n"
    f"FY2025 & FY2024: TSB Bank plc Annual Report and Accounts 2025, p.49 and p.106 (Cash flow statements and "
    f"note 32) - {AR25_URL}\n"
    f"FY2023 & FY2022 (restated): TSB Bank plc Annual Report and Accounts 2023, p.33-34 and p.83-84 (Cash flow "
    f"statements and note 32) - {AR23_URL}\n"
    f"FY2021: TSB Bank plc Annual Report and Accounts 2021, p.29 and p.78 (Cash flow statements and note 31) "
    f"- {AR21_URL}\n\n" + ENTITY_NOTE + "\n\n"
    "RESTATEMENT NOTE: The 2023 Annual Report restated FY2022 (and earlier) to include on-demand loans and "
    "advances to credit institutions within cash and cash equivalents; this added £56.1m to the FY2021 closing "
    "cash position and £159.2m to the FY2022 opening position on a comparative basis, but FY2021's own Annual "
    "Report was never itself restated. As a result, FY2021's closing cash and cash equivalents (£4,851.1m, as "
    "originally reported) does not exactly tie to FY2022's opening balance shown here (£4,907.2m, restated) - a "
    "known £56.1m definitional break at that one boundary, not a data error. FY2022 onward reconciles exactly. "
    "The 2023 Annual Report also reclassified a derivatives/hedge-accounting fair value line from 'change in "
    "operating assets and liabilities' into 'non-cash and other items' from FY2023 onward; FY2021 and FY2022 keep "
    "their original as-reported classification for that line (see the two separate rows below).\n\n"
    "PRESENTATION NOTE: Line items were relabelled and reorganised across these 5 years as TSB's funding mix "
    "evolved (e.g. 'Issue of debt securities in issue' in FY2021 became separate covered bond/senior "
    "unsecured/securitisation/AT1 lines by FY2024-25; a repurchase-agreements financing line appeared only in "
    "FY2022-23). Blank cells indicate that year's report did not disclose or did not have that specific line; "
    "'0' indicates the report explicitly showed a nil ('-') value. The 'Change in operating assets and "
    "liabilities' and 'Non-cash and other items' rows are TSB's own audited primary-statement subtotals; the "
    "rows above each are the supporting breakdown from the cash flow note."
)


def p3_sources(page_km1, table_km1="Table 1: Key metrics (KM1)"):
    return (
        "Sources - TSB Banking Group plc consolidated Pillar 3 basis (see entity note on Cash Flow Statement "
        "sheet):\n"
        f"FY2025: TSB Banking Group plc Large Subsidiary Disclosures, as at 31 December 2025, p.6 ({table_km1}) "
        f"- {P3_25_URL}\n"
        f"FY2024: TSB Banking Group plc Large Subsidiary Disclosures, as at 31 December 2024, p.6 (Table 1a: Key "
        f"metrics (KM1)) - {P3_24_URL}\n"
        f"FY2023: TSB Banking Group plc Large Subsidiary Disclosures 2023, p.6 (Table 1a: Key metrics (KM1)) "
        f"- {P3_23_URL}\n"
        f"FY2022: TSB Banking Group plc Large Subsidiary Disclosures 2022, p.6 (Table 1a: Key metrics (KM1)) "
        f"- {P3_22_URL}\n"
        f"FY2021: TSB Banking Group plc Large Subsidiary Disclosures 2021, p.5 (Table 1: Key metrics (KM1 / IFRS "
        f"9-FL)) - {P3_21_URL}"
    )


bw = BankWorkbook(bank_name="TSB Bank plc", years=YEARS, header_color="002D5B")

# ---------------------------------------------------------------
# Statement sources - TSB Bank plc, Bank (Consolidated) basis, £ million,
# each year's own Annual Report figures, independently cross-checked against
# the adjacent report's comparative column - ties exactly across all 5 years
# for Total assets/Total liabilities/Total equity, Profit for the year, and
# Total comprehensive income. Zero undocumented plug rows anywhere.
# ---------------------------------------------------------------
STATEMENTS_SOURCES = (
    "Sources - TSB Bank plc, Bank (Consolidated) basis, £ million:\n"
    f"FY2025 & FY2024: TSB Bank plc Annual Report and Accounts 2025, p.46 (Balance sheets), p.47 (Consolidated "
    f"statement of comprehensive income), p.48 (Statements of changes in equity) - {AR25_URL}\n"
    f"FY2023 & FY2022: TSB Bank plc Annual Report and Accounts 2023, p.30 (Balance sheets), p.31 (Consolidated "
    f"statement of comprehensive income), p.32 (Statements of changes in equity) - {AR23_URL}\n"
    f"FY2021: TSB Bank plc Annual Report and Accounts 2021, p.26 (Balance sheets), p.27 (Consolidated statement "
    f"of comprehensive income), p.28 (Statements of changes in equity); FY2021's closing equity ties exactly to "
    f"AR2023's own 'Balance at 1 January 2022' comparative - {AR21_URL}\n\n" + ENTITY_NOTE + "\n\n"
    "PRESENTATION NOTE: Balance sheet - 'Loans and advances to credit institutions' is shown as a standalone line "
    "from FY2025 only; FY2021-FY2024 combine it with central bank placements as 'Loans and advances to central "
    "banks and credit institutions' (same figures reused here). 'Other equity instruments' (Additional Tier 1) "
    "first appears FY2024, following TSB's first AT1 issuance that year (see Cash Flow Statement financing "
    "activities). Income statement - FY2024/FY2025 itemise 'Gains on derecognition of financial assets/liabilities' "
    "lines that differ from FY2021-FY2023's own line items (e.g. FVOCI derecognition gains only shown FY2021-23); "
    "each year's own as-published structure is preserved rather than forced into a common format."
)

# ---------------------------------------------------------------
# Balance Sheet - equity reconciliation ladder step 1: built first so each
# year's own Total equity is the independent check value for the equity
# sheet below.
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash, cash balances at central banks and other demand deposits", {"FY2025": 4202.1, "FY2024": 4823.8, "FY2023": 5897.3, "FY2022": 5238.8, "FY2021": 4851.1}),
    ("DATA", "Debt securities at amortised cost", {"FY2025": 1986.4, "FY2024": 1982.5, "FY2023": 2124.2, "FY2022": 1951.6, "FY2021": 2166.7}),
    ("DATA", "Loans and advances to customers", {"FY2025": 36268.4, "FY2024": 36330.9, "FY2023": 36245.9, "FY2022": 38050.0, "FY2021": 37383.8}),
    ("DATA", "Loans and advances to central banks and credit institutions", {"FY2025": 305.2, "FY2024": 277.8, "FY2023": 328.0, "FY2022": 303.5, "FY2021": 199.7}),
    ("DATA", "Reverse repurchase agreement", {"FY2025": 62.0, "FY2024": 0}),
    ("DATA", "Other advances", {"FY2025": 66.9, "FY2024": 130.2, "FY2023": 209.6, "FY2022": 703.2, "FY2021": 80.7}),
    ("DATA", "Debt securities at fair value through other comprehensive income", {"FY2025": 440.2, "FY2024": 328.6, "FY2023": 356.6, "FY2022": 509.5, "FY2021": 1069.0}),
    ("DATA", "Derivative financial assets not in hedge accounting relationships", {"FY2025": 362.4, "FY2024": 667.6, "FY2023": 822.9, "FY2022": 1158.7, "FY2021": 168.4}),
    ("DATA", "Hedging derivative financial assets", {"FY2025": 1149.2, "FY2024": 1274.3, "FY2023": 1346.9, "FY2022": 1565.9, "FY2021": 244.5}),
    ("DATA", "Fair value adjustments for portfolio hedged risk", {"FY2025": 4.5, "FY2024": -170.9, "FY2023": -154.9, "FY2022": -542.8, "FY2021": -109.3}),
    ("DATA", "Property and equipment", {"FY2025": 215.1, "FY2024": 233.9, "FY2023": 253.5, "FY2022": 287.5, "FY2021": 300.3}),
    ("DATA", "Intangible assets", {"FY2025": 123.4, "FY2024": 109.9, "FY2023": 86.1, "FY2022": 75.6, "FY2021": 72.1}),
    ("DATA", "Deferred tax asset", {"FY2025": 6.1, "FY2024": 8.1, "FY2023": 43.2, "FY2022": 64.5, "FY2021": 122.6}),
    ("DATA", "Other assets", {"FY2025": 89.6, "FY2024": 102.4, "FY2023": 93.6, "FY2022": 83.6, "FY2021": 156.0}),
    ("TOTAL", "Total assets", {"FY2025": 45281.5, "FY2024": 46099.1, "FY2023": 47652.9, "FY2022": 49449.6, "FY2021": 46705.6}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer deposits", {"FY2025": 35209.0, "FY2024": 35051.2, "FY2023": 34764.3, "FY2022": 36338.2, "FY2021": 35951.9}),
    ("DATA", "Borrowings from central banks", {"FY2025": 598.9, "FY2024": 1406.9, "FY2023": 4057.9, "FY2022": 5538.3, "FY2021": 5501.6}),
    ("DATA", "Debt securities in issue", {"FY2025": 4869.3, "FY2024": 4583.2, "FY2023": 3664.1, "FY2022": 1955.5, "FY2021": 2199.1}),
    ("DATA", "Repurchase agreements", {"FY2023": 0, "FY2022": 360.0}),
    ("DATA", "Subordinated liabilities", {"FY2025": 297.8, "FY2024": 285.9, "FY2023": 277.7, "FY2022": 265.4, "FY2021": 291.8}),
    ("DATA", "Lease liabilities", {"FY2025": 107.8, "FY2024": 120.7, "FY2023": 125.0, "FY2022": 145.9, "FY2021": 163.5}),
    ("DATA", "Other financial liabilities", {"FY2025": 1080.6, "FY2024": 1184.6, "FY2023": 1222.4, "FY2022": 1320.1, "FY2021": 193.6}),
    ("DATA", "Derivative financial liabilities not in hedge accounting relationships", {"FY2025": 456.7, "FY2024": 824.2, "FY2023": 982.1, "FY2022": 1252.4, "FY2021": 156.5}),
    ("DATA", "Hedging derivative financial liabilities", {"FY2025": 99.4, "FY2024": 143.6, "FY2023": 318.7, "FY2022": 301.5, "FY2021": 136.8}),
    ("DATA", "Fair value adjustments for portfolio hedged risk", {"FY2025": 12.3, "FY2024": -134.7, "FY2023": -85.5, "FY2022": -321.3, "FY2021": -63.6}),
    ("DATA", "Provisions", {"FY2025": 22.2, "FY2024": 39.8, "FY2023": 75.2, "FY2022": 125.0, "FY2021": 110.2}),
    ("DATA", "Other liabilities", {"FY2025": 189.5, "FY2024": 473.0, "FY2023": 296.4, "FY2022": 238.8, "FY2021": 197.8}),
    ("TOTAL", "Total liabilities", {"FY2025": 42943.5, "FY2024": 43978.4, "FY2023": 45698.3, "FY2022": 47519.8, "FY2021": 44839.2}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 79.4, "FY2024": 79.4, "FY2023": 79.4, "FY2022": 79.4, "FY2021": 79.4}),
    ("DATA", "Share premium", {"FY2025": 195.6, "FY2024": 195.6, "FY2023": 195.6, "FY2022": 195.6, "FY2021": 195.6}),
    ("DATA", "Other equity instruments", {"FY2025": 250.0, "FY2024": 250.0}),
    ("DATA", "Merger reserve / Other reserves", {"FY2025": 412.8, "FY2024": 412.8, "FY2023": 412.8, "FY2022": 412.8, "FY2021": 412.8}),
    ("DATA", "Retained profits", {"FY2025": 1398.4, "FY2024": 1164.9, "FY2023": 1261.1, "FY2022": 1207.7, "FY2021": 1174.1}),
    ("DATA", "Fair value reserve", {"FY2025": -6.2, "FY2024": -8.0, "FY2023": -6.5, "FY2022": -6.1, "FY2021": 11.1}),
    ("DATA", "Cash flow hedging reserve", {"FY2025": 8.0, "FY2024": 26.0, "FY2023": 12.2, "FY2022": 40.4, "FY2021": -6.6}),
    ("TOTAL", "Total equity", {"FY2025": 2338.0, "FY2024": 2120.7, "FY2023": 1954.6, "FY2022": 1929.8, "FY2021": 1866.4}),
    ("TOTAL", "Total equity and liabilities", {"FY2025": 45281.5, "FY2024": 46099.1, "FY2023": 47652.9, "FY2022": 49449.6, "FY2021": 46705.6}),
]

bw.add_balance_sheet_sheet(
    title="TSB Bank plc — Consolidated Balance Sheet",
    subtitle="Bank (Consolidated) basis, £ million. Total equity ties exactly to the Statement of Changes in "
              "Equity sheet for every year.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=230,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Profit & Loss (Consolidated Statement of Comprehensive Income)
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Interest and similar income", {}),
    ("DATA", "Interest income calculated using the effective interest method", {"FY2025": 1846.4, "FY2024": 1803.9, "FY2023": 1573.5, "FY2022": 1123.0, "FY2021": 946.4}),
    ("DATA", "Other interest income", {"FY2025": 129.3, "FY2024": 273.5, "FY2023": 368.6, "FY2022": 108.7, "FY2021": -35.0}),
    ("TOTAL", "Total interest and similar income", {"FY2025": 1975.7, "FY2024": 2077.4, "FY2023": 1942.1, "FY2022": 1231.7, "FY2021": 911.4}),
    ("DATA", "Interest and similar expense", {"FY2025": -920.1, "FY2024": -1093.0, "FY2023": -920.1, "FY2022": -250.0, "FY2021": -42.5}),
    ("TOTAL", "Net interest income", {"FY2025": 1055.6, "FY2024": 984.4, "FY2023": 1022.0, "FY2022": 981.7, "FY2021": 868.9}),
    ("DATA", "Fee and commission income", {"FY2025": 114.1, "FY2024": 124.7, "FY2023": 129.2, "FY2022": 135.5, "FY2021": 121.8}),
    ("DATA", "Fee and commission expense", {"FY2025": -37.4, "FY2024": -34.0, "FY2023": -21.2, "FY2022": -21.3, "FY2021": -18.2}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 76.7, "FY2024": 90.7, "FY2023": 108.0, "FY2022": 114.2, "FY2021": 103.6}),
    ("SECTION", "Other income", {}),
    ("DATA", "Gains on derecognition of financial assets measured at amortised cost", {"FY2025": 2.8}),
    ("DATA", "Gains on derecognition of financial assets measured at FVOCI", {"FY2023": 4.3, "FY2022": 6.3, "FY2021": 7.0}),
    ("DATA", "Losses on derecognition of financial liabilities measured at amortised cost", {"FY2023": -1.0}),
    ("DATA", "Gains/(losses) on derivative financial instruments at fair value through profit or loss", {"FY2025": 40.5, "FY2024": 57.6, "FY2023": 11.2, "FY2022": -8.1}),
    ("DATA", "Losses on derivative financial assets at fair value through profit or loss", {"FY2021": -2.5}),
    ("DATA", "(Losses)/gains from hedge accounting", {"FY2025": -34.2, "FY2024": -30.1, "FY2023": -2.2, "FY2022": 4.2, "FY2021": -2.4}),
    ("DATA", "Gains/(losses) on derecognition of non-financial assets/liabilities", {"FY2025": 0.5, "FY2024": -2.3, "FY2023": -0.1, "FY2022": 0.6, "FY2021": -2.6}),
    ("DATA", "Other operating income", {"FY2025": 30.4, "FY2024": 36.7, "FY2023": 14.5, "FY2022": 6.6, "FY2021": 10.9}),
    ("TOTAL", "Other income", {"FY2025": 116.7, "FY2024": 152.6, "FY2023": 134.7, "FY2022": 123.8, "FY2021": 114.0}),
    ("TOTAL", "Total income", {"FY2025": 1172.3, "FY2024": 1137.0, "FY2023": 1156.7, "FY2022": 1105.5, "FY2021": 982.9}),
    ("DATA", "Total operating expenses", {"FY2025": -785.9, "FY2024": -821.8, "FY2023": -852.9, "FY2022": -869.5, "FY2021": -827.3}),
    ("TOTAL", "Operating profit/(loss) before impairment losses and taxation", {"FY2025": 386.4, "FY2024": 315.2, "FY2023": 303.8, "FY2022": 236.0, "FY2021": 155.6}),
    ("DATA", "Impairment losses on financial assets at amortised cost", {"FY2025": -51.2, "FY2024": -31.9, "FY2023": -71.8, "FY2022": -57.7, "FY2021": -2.6}),
    ("DATA", "Impairment credit/(losses) on loan commitments", {"FY2025": 4.2, "FY2024": 1.8, "FY2023": 3.5, "FY2022": 2.8, "FY2021": 2.5}),
    ("TOTAL", "Total impairment losses", {"FY2025": -47.0, "FY2024": -30.1, "FY2023": -68.3, "FY2022": -54.9, "FY2021": -0.1}),
    ("TOTAL", "Profit/(loss) before taxation", {"FY2025": 339.4, "FY2024": 285.1, "FY2023": 235.5, "FY2022": 181.1, "FY2021": 155.5}),
    ("DATA", "Taxation", {"FY2025": -88.3, "FY2024": -81.3, "FY2023": -62.1, "FY2022": -80.5, "FY2021": -27.1}),
    ("TOTAL", "Profit/(loss) for the year", {"FY2025": 251.1, "FY2024": 203.8, "FY2023": 173.4, "FY2022": 100.6, "FY2021": 128.4}),
    ("SECTION", "Other comprehensive income/(loss), net of taxation", {}),
    ("DATA", "Change in fair value reserve", {"FY2025": 1.8, "FY2024": -1.5, "FY2023": -0.4, "FY2022": -17.2, "FY2021": -0.5}),
    ("DATA", "Change in cash flow hedging reserve", {"FY2025": -18.0, "FY2024": 13.8, "FY2023": -28.2, "FY2022": 47.0, "FY2021": 13.6}),
    ("TOTAL", "Other comprehensive income/(losses) for the year, net of taxation", {"FY2025": -16.2, "FY2024": 12.3, "FY2023": -28.6, "FY2022": 29.8, "FY2021": 13.1}),
    ("TOTAL", "Total comprehensive income/(loss) for the year", {"FY2025": 234.9, "FY2024": 216.1, "FY2023": 144.8, "FY2022": 130.4, "FY2021": 141.5}),
]

bw.add_income_statement_sheet(
    title="TSB Bank plc — Consolidated Statement of Comprehensive Income",
    subtitle="Bank (Consolidated) basis, £ million. 'Total comprehensive income/(loss) for the year' ties exactly "
              "to Profit for the year + Other comprehensive income for every year.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=230,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - equity reconciliation ladder steps 2-3:
# built year-by-year, confirmed against next year's opening AND that year's
# own Balance Sheet Total equity above (all 5 years tie exactly, including
# the FY2024 AT1 issuance and FY2025 AT1 distribution - two easy-to-skip
# movement categories deliberately checked for). Zero undocumented plug rows.
# ---------------------------------------------------------------
EQUITY_HEADERS = [
    "Share capital", "Share premium", "Other equity instruments", "Merger reserve",
    "Fair value reserve", "Cash flow hedging reserve", "Retained profit", "Total equity",
]

equity_rows = [
    ("TOTAL", "Balance at 1 January 2021", (79.4, 195.6, None, 412.8, 11.6, -20.2, 1045.7, 1724.9)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, 128.4, 128.4)),
    ("DATA", "Change in fair value reserve", (None, None, None, None, -0.5, None, None, -0.5)),
    ("DATA", "Change in cash flow hedging reserve", (None, None, None, None, None, 13.6, None, 13.6)),
    ("TOTAL", "Balance at 31 December 2021", (79.4, 195.6, None, 412.8, 11.1, -6.6, 1174.1, 1866.4)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, 100.6, 100.6)),
    ("DATA", "Change in fair value reserve", (None, None, None, None, -17.2, None, None, -17.2)),
    ("DATA", "Change in cash flow hedging reserve", (None, None, None, None, None, 47.0, None, 47.0)),
    ("DATA", "Dividend paid", (None, None, None, None, None, None, -67.0, -67.0)),
    ("TOTAL", "Balance at 31 December 2022", (79.4, 195.6, None, 412.8, -6.1, 40.4, 1207.7, 1929.8)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, 173.4, 173.4)),
    ("DATA", "Change in fair value reserve", (None, None, None, None, -0.4, None, None, -0.4)),
    ("DATA", "Change in cash flow hedging reserve", (None, None, None, None, None, -28.2, None, -28.2)),
    ("DATA", "Dividend paid", (None, None, None, None, None, None, -120.0, -120.0)),
    ("TOTAL", "Balance at 31 December 2023", (79.4, 195.6, None, 412.8, -6.5, 12.2, 1261.1, 1954.6)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, 203.8, 203.8)),
    ("DATA", "Change in fair value reserve", (None, None, None, None, -1.5, None, None, -1.5)),
    ("DATA", "Change in cash flow hedging reserve", (None, None, None, None, None, 13.8, None, 13.8)),
    ("DATA", "Issue of Additional Tier 1 Securities", (None, None, 250.0, None, None, None, None, 250.0)),
    ("DATA", "Dividends paid on ordinary shares", (None, None, None, None, None, None, -300.0, -300.0)),
    ("TOTAL", "Balance at 31 December 2024", (79.4, 195.6, 250.0, 412.8, -8.0, 26.0, 1164.9, 2120.7)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, 251.1, 251.1)),
    ("DATA", "Change in fair value reserve", (None, None, None, None, 1.8, None, None, 1.8)),
    ("DATA", "Change in cash flow hedging reserve", (None, None, None, None, None, -18.0, None, -18.0)),
    ("DATA", "Distributions on other equity instruments", (None, None, None, None, None, None, -17.6, -17.6)),
    ("TOTAL", "Balance at 31 December 2025", (79.4, 195.6, 250.0, 412.8, -6.2, 8.0, 1398.4, 2338.0)),
]

bw.add_equity_changes_sheet(
    title="TSB Bank plc — Statement of Changes in Equity",
    subtitle="Bank (Consolidated) basis, £ million, chronological (oldest to newest). Each year's closing Total "
              "equity ties exactly to that year's own Balance Sheet Total equity and to the next year's opening "
              "balance - zero undocumented plug rows across all 5 years.",
    headers=EQUITY_HEADERS,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=50,
    source_height=230,
)

# ---------------------------------------------------------------
# Sheet: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    (
        "DATA",
        "Profit/(loss) before taxation",
        {
            "FY2025": 339.4,
            "FY2024": 285.1,
            "FY2023": 235.5,
            "FY2022": 181.1,
            "FY2021": 155.5,
        },
    ),
    ("DATA", "Decrease in loans to central banks", {"FY2025": 0, "FY2024": 136.0}),
    (
        "DATA",
        "Increase in loans to central banks (FY2021 presentation)",
        {"FY2021": -22.7},
    ),
    ("DATA", "(Increase)/decrease in loans to credit institutions", {"FY2021": -12.8}),
    (
        "DATA",
        "Decrease/(increase) in loans and advances to customers",
        {
            "FY2025": -1.4,
            "FY2024": -124.6,
            "FY2023": 1719.2,
            "FY2022": -722.5,
            "FY2021": -4070.2,
        },
    ),
    (
        "DATA",
        "Increase in reverse repurchase agreements",
        {"FY2025": -62.0, "FY2024": 0},
    ),
    (
        "DATA",
        "Decrease in reverse purchase agreements (FY2021 presentation)",
        {"FY2021": 0},
    ),
    (
        "DATA",
        "Decrease/(increase) in other advances",
        {
            "FY2025": 63.3,
            "FY2024": 79.3,
            "FY2023": 493.6,
            "FY2022": -622.6,
            "FY2021": 136.8,
        },
    ),
    (
        "DATA",
        "Net change in derivative financial instruments and FV adjustments for portfolio hedged risk (within operating assets/liabilities - FY2021/22 as originally presented)",
        {"FY2022": -63.1, "FY2021": -147.6},
    ),
    (
        "DATA",
        "Decrease/(increase) in other assets",
        {"FY2025": 11.2, "FY2024": 2.0, "FY2023": -6.5, "FY2022": 72.4, "FY2021": 18.6},
    ),
    (
        "DATA",
        "(Decrease)/increase in deposits from credit institutions (FY2021 presentation)",
        {"FY2021": 0},
    ),
    (
        "DATA",
        "Increase/(decrease) in customer deposits",
        {
            "FY2025": 176.0,
            "FY2024": 280.8,
            "FY2023": -1666.5,
            "FY2022": 357.0,
            "FY2021": 1591.2,
        },
    ),
    (
        "DATA",
        "(Decrease)/increase in other financial liabilities",
        {
            "FY2025": -148.8,
            "FY2024": -91.9,
            "FY2023": -156.4,
            "FY2022": 1126.5,
            "FY2021": 141.9,
        },
    ),
    (
        "DATA",
        "(Decrease)/increase in provisions",
        {
            "FY2025": -13.4,
            "FY2024": -33.5,
            "FY2023": -46.5,
            "FY2022": 17.6,
            "FY2021": -40.4,
        },
    ),
    (
        "DATA",
        "Increase/(decrease) in other liabilities",
        {
            "FY2025": 16.4,
            "FY2024": -3.3,
            "FY2023": -11.6,
            "FY2022": -25.4,
            "FY2021": 0.7,
        },
    ),
    (
        "TOTAL",
        "Change in operating assets and liabilities (as reported)",
        {
            "FY2025": 41.3,
            "FY2024": 244.8,
            "FY2023": 333.6,
            "FY2022": 202.3,
            "FY2021": -2404.5,
        },
    ),
    (
        "DATA",
        "Interest expense on financing activities",
        {"FY2025": 291.1, "FY2024": 402.3, "FY2023": 398.8, "FY2022": 160.0},
    ),
    (
        "DATA",
        "Interest income on investing activities",
        {"FY2025": -63.4, "FY2024": -63.2, "FY2023": -60.0, "FY2022": -33.2},
    ),
    (
        "DATA",
        "Net change in derivative financial instruments and FV adjustments for portfolio hedged risk (within non-cash items - FY2023 onward presentation)",
        {"FY2025": 127.1, "FY2024": 259.6, "FY2023": 147.6},
    ),
    (
        "DATA",
        "Depreciation and amortisation",
        {
            "FY2025": 63.4,
            "FY2024": 72.5,
            "FY2023": 67.0,
            "FY2022": 66.0,
            "FY2021": 70.2,
        },
    ),
    (
        "DATA",
        "Net movement in allowance for credit impairment losses",
        {"FY2025": -8.9, "FY2024": -31.7},
    ),
    (
        "DATA",
        "Impairment losses on loans and advances to customers (FY2021-23 presentation)",
        {"FY2023": 13.8, "FY2022": 57.8, "FY2021": 2.6},
    ),
    ("DATA", "Exchange differences", {"FY2021": 0}),
    (
        "DATA",
        "Other non-cash items",
        {
            "FY2025": -48.8,
            "FY2024": -115.5,
            "FY2023": 97.4,
            "FY2022": -64.2,
            "FY2021": 39.2,
        },
    ),
    (
        "TOTAL",
        "Non-cash and other items (as reported)",
        {
            "FY2025": 360.5,
            "FY2024": 524.0,
            "FY2023": 664.6,
            "FY2022": 247.4,
            "FY2021": 112.0,
        },
    ),
    (
        "DATA",
        "Taxation paid",
        {
            "FY2025": -78.8,
            "FY2024": -57.0,
            "FY2023": -33.0,
            "FY2022": -34.4,
            "FY2021": -8.7,
        },
    ),
    (
        "TOTAL",
        "Net cash (used in)/provided by operating activities",
        {
            "FY2025": 662.4,
            "FY2024": 996.9,
            "FY2023": 1200.7,
            "FY2022": 596.4,
            "FY2021": -2145.7,
        },
    ),
    ("SECTION", "Cash flows from investing activities", {}),
    (
        "DATA",
        "Purchase of property and equipment",
        {
            "FY2025": -18.3,
            "FY2024": -22.2,
            "FY2023": -20.2,
            "FY2022": -36.8,
            "FY2021": -44.5,
        },
    ),
    (
        "DATA",
        "Purchase and development of intangible assets",
        {
            "FY2025": -38.4,
            "FY2024": -41.8,
            "FY2023": -28.0,
            "FY2022": -17.5,
            "FY2021": -30.3,
        },
    ),
    (
        "DATA",
        "Purchase of debt securities",
        {
            "FY2025": -247.4,
            "FY2024": -124.7,
            "FY2023": -219.8,
            "FY2022": -580.1,
            "FY2021": -1324.5,
        },
    ),
    (
        "DATA",
        "Sale of debt securities",
        {"FY2024": 0, "FY2023": 252.6, "FY2022": 442.6, "FY2021": 500.9},
    ),
    (
        "DATA",
        "Proceeds from maturing investments",
        {
            "FY2025": 169.3,
            "FY2024": 141.7,
            "FY2023": 39.3,
            "FY2022": 67.0,
            "FY2021": 23.0,
        },
    ),
    (
        "DATA",
        "Interest received on debt securities",
        {
            "FY2025": 67.6,
            "FY2024": 68.1,
            "FY2023": 64.6,
            "FY2022": 44.5,
            "FY2021": 36.3,
        },
    ),
    (
        "TOTAL",
        "Net cash (used in)/provided by investing activities",
        {
            "FY2025": -67.2,
            "FY2024": 21.1,
            "FY2023": 88.5,
            "FY2022": -80.3,
            "FY2021": -839.1,
        },
    ),
    ("SECTION", "Cash flows from financing activities", {}),
    (
        "DATA",
        "Additional borrowings from central banks",
        {"FY2025": 5.0, "FY2024": 0, "FY2023": 5.0, "FY2022": 510.0, "FY2021": 5500.0},
    ),
    (
        "DATA",
        "Repayment of borrowing from central banks",
        {
            "FY2025": -797.0,
            "FY2024": -2620.0,
            "FY2023": -1500.0,
            "FY2022": -510.0,
            "FY2021": -3065.0,
        },
    ),
    (
        "DATA",
        "Interest paid on borrowings from central banks",
        {
            "FY2025": -46.2,
            "FY2024": -177.1,
            "FY2023": -191.7,
            "FY2022": -57.3,
            "FY2021": -7.8,
        },
    ),
    (
        "DATA",
        "Issue of covered bonds",
        {"FY2025": 495.5, "FY2024": 926.1, "FY2023": 1750.0, "FY2022": 0},
    ),
    ("DATA", "Repayment of covered bonds", {"FY2025": 0, "FY2024": -500.0}),
    ("DATA", "Buyback of covered bonds", {"FY2023": -251.0, "FY2022": -500.0}),
    (
        "DATA",
        "Interest paid on covered bonds",
        {"FY2025": -143.2, "FY2024": -144.4, "FY2023": -120.1, "FY2022": -29.5},
    ),
    ("DATA", "Issue of securitisation notes", {"FY2025": 0, "FY2024": 498.3}),
    ("DATA", "Repayment of securitisation notes", {"FY2025": -20.0, "FY2024": -5.0}),
    (
        "DATA",
        "Interest paid on securitisation notes",
        {"FY2025": -24.2, "FY2024": -11.8},
    ),
    ("DATA", "Issue of Additional Tier 1 securities", {"FY2025": 0, "FY2024": 249.7}),
    (
        "DATA",
        "Issue of senior unsecured debt securities",
        {"FY2024": 0, "FY2023": 200.0, "FY2022": 700.0},
    ),
    (
        "DATA",
        "Repayment of senior unsecured debt securities",
        {"FY2025": -250.0, "FY2024": 0, "FY2023": 0, "FY2022": -450.0},
    ),
    (
        "DATA",
        "Interest paid on senior unsecured debt securities",
        {"FY2025": -65.3, "FY2024": -72.4, "FY2023": -51.1, "FY2022": -15.8},
    ),
    (
        "DATA",
        "Issue of debt securities in issue (FY2021 presentation)",
        {"FY2021": 500.0},
    ),
    (
        "DATA",
        "Interest paid on debt securities in issue (FY2021 presentation)",
        {"FY2021": -21.0},
    ),
    ("DATA", "Issue of subordinated liabilities", {"FY2021": 300.0}),
    ("DATA", "Repayment of subordinated liabilities", {"FY2021": -385.0}),
    (
        "DATA",
        "Interest paid on subordinated liabilities",
        {
            "FY2025": -10.3,
            "FY2024": -10.3,
            "FY2023": -10.3,
            "FY2022": -10.3,
            "FY2021": -18.8,
        },
    ),
    (
        "DATA",
        "(Repayment)/issue of repurchase agreements",
        {"FY2023": -359.9, "FY2022": 359.9},
    ),
    (
        "DATA",
        "Interest paid on repurchase agreements",
        {"FY2023": -1.0, "FY2022": -2.6},
    ),
    ("DATA", "Net securitisation funding (FY2021 presentation)", {"FY2021": 0}),
    (
        "DATA",
        "Lease payments",
        {
            "FY2025": -16.2,
            "FY2024": -18.8,
            "FY2023": -17.8,
            "FY2022": -19.7,
            "FY2021": -22.8,
        },
    ),
    (
        "DATA",
        "Distributions on other equity instruments",
        {"FY2025": -17.6, "FY2024": 0},
    ),
    (
        "DATA",
        "Dividends paid",
        {"FY2025": -300.0, "FY2024": -120.0, "FY2023": -50.0, "FY2022": 0},
    ),
    (
        "TOTAL",
        "Net cash (used in)/provided by financing activities",
        {
            "FY2025": -1189.5,
            "FY2024": -2005.7,
            "FY2023": -597.9,
            "FY2022": -25.3,
            "FY2021": 2779.6,
        },
    ),
    (
        "TOTAL",
        "Change in cash and cash equivalents",
        {
            "FY2025": -594.3,
            "FY2024": -987.7,
            "FY2023": 691.3,
            "FY2022": 490.8,
            "FY2021": -205.2,
        },
    ),
    (
        "DATA",
        "Cash and cash equivalents at 1 January",
        {
            "FY2025": 5101.6,
            "FY2024": 6089.3,
            "FY2023": 5398.0,
            "FY2022": 4907.2,
            "FY2021": 5056.3,
        },
    ),
    (
        "TOTAL",
        "Cash and cash equivalents at 31 December",
        {
            "FY2025": 4507.3,
            "FY2024": 5101.6,
            "FY2023": 6089.3,
            "FY2022": 5398.0,
            "FY2021": 4851.1,
        },
    ),
]

bw.add_cash_flow_sheet(
    title="TSB Bank plc — Consolidated Cash Flow Statement",
    subtitle="Bank (Consolidated) basis, £ million unless stated. See source note at bottom (incl. an FY2021/FY2022 restatement break).",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=80,
    source_height=220,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Asset Quality - loan book by IFRS 9 stage. FY2022-FY2025 sourced from the
# 'Sensitivity to alternative economic scenario weightings' note's weighted
# gross customer lending balances/ECL table; FY2021 sourced from the fuller
# 'Reconciliation of movements in gross customer balances and allowances for
# credit impairment losses' table (a differently-scoped disclosure - see
# source note). Neither table ties exactly to the Balance Sheet's narrower
# 'Loans and advances to customers' net line (a documented, genuine
# cross-statement presentation difference, not forced to tie).
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Gross customer lending balances by IFRS 9 stage (weighted forecast)", {}),
    ("DATA", "Stage 1", {"FY2025": 33038.7, "FY2024": 33151.6, "FY2023": 32115.9, "FY2022": 33737.1, "FY2021": 34280.5}),
    ("DATA", "Stage 2", {"FY2025": 2738.6, "FY2024": 2697.2, "FY2023": 3684.9, "FY2022": 3866.8, "FY2021": 2583.9}),
    ("DATA", "Stage 3 (non-performing)", {"FY2025": 525.7, "FY2024": 528.2, "FY2023": 508.1, "FY2022": 472.1, "FY2021": 502.4}),
    ("DATA", "POCI (purchased or originated credit impaired)", {"FY2025": 73.2, "FY2024": 84.1, "FY2023": 94.9, "FY2022": 109.3, "FY2021": 124.8}),
    ("TOTAL", "Total gross customer lending balances", {"FY2025": 36376.2, "FY2024": 36461.1, "FY2023": 36403.8, "FY2022": 38185.3, "FY2021": 37491.6}),
    ("SECTION", "Allowance for credit losses and credit impairment provisions", {}),
    ("DATA", "Stage 1", {"FY2025": 34.1, "FY2024": 50.2, "FY2023": 60.5, "FY2022": 42.5, "FY2021": 59.0}),
    ("DATA", "Stage 2", {"FY2025": 52.4, "FY2024": 57.7, "FY2023": 80.9, "FY2022": 103.2, "FY2021": 74.4}),
    ("DATA", "Stage 3", {"FY2025": 86.5, "FY2024": 80.0, "FY2023": 79.8, "FY2022": 65.5, "FY2021": 55.4}),
    ("DATA", "POCI", {"FY2025": 2.6, "FY2024": 0.8, "FY2023": 1.0, "FY2022": 0.7, "FY2021": 0.8}),
    ("TOTAL", "Total allowance for credit losses and credit impairment provisions", {"FY2025": 175.6, "FY2024": 188.7, "FY2023": 222.2, "FY2022": 211.9, "FY2021": 189.6}),
    ("SECTION", "Derived ratios", {}),
    ("DATA", "NPL ratio (Stage 3 gross / Total gross customer lending)", {"FY2025": "1.45%", "FY2024": "1.45%", "FY2023": "1.40%", "FY2022": "1.24%", "FY2021": "1.34%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 allowance / Stage 3 gross)", {"FY2025": "16.45%", "FY2024": "15.15%", "FY2023": "15.71%", "FY2022": "13.87%", "FY2021": "11.03%"}),
    ("DATA", "Total coverage ratio (Total allowance / Total gross)", {"FY2025": "0.48%", "FY2024": "0.52%", "FY2023": "0.61%", "FY2022": "0.55%", "FY2021": "0.51%"}),
]

bw.add_asset_quality_sheet(
    title="TSB Bank plc — Asset Quality",
    subtitle="Bank and Company, £ million. See source note for why this doesn't tie exactly to the Balance Sheet's "
              "Loans and advances to customers line, and for a FY2021 vs FY2022-25 disclosure-basis difference.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - Bank and Company basis, £ million:\n"
        f"FY2025: TSB Bank plc Annual Report and Accounts 2025, p.62 (Note 8, 'Sensitivity to alternative economic "
        f"scenario weightings', weighted column) - {AR25_URL}\n"
        f"FY2024: TSB Bank plc Annual Report and Accounts 2025, p.63 (Note 8, FY2024 comparative, weighted column) "
        f"- {AR25_URL}\n"
        f"FY2023: TSB Bank plc Annual Report and Accounts 2023, p.45 (Note 8, weighted column) - {AR23_URL}\n"
        f"FY2022: TSB Bank plc Annual Report and Accounts 2023, p.46 (Note 8, FY2022 comparative, weighted column) "
        f"- {AR23_URL}\n"
        f"FY2021: TSB Bank plc Annual Report and Accounts 2021, p.54 ('Reconciliation of movements in gross "
        f"customer balances and allowances for credit impairment losses', at 31 December 2021 closing row) "
        f"- {AR21_URL}\n\n"
        "PRESENTATION NOTE: FY2022-FY2025 use the 'Sensitivity to alternative economic scenario weightings' note's "
        "weighted-forecast gross lending/ECL table (a narrower disclosure scope than the full 'Reconciliation of "
        "movements' table, which TSB stopped publishing after the 2021 Annual Report). FY2021 uses that older, "
        "fuller reconciliation table instead - a genuine disclosure-format change, not a data error. Neither "
        "table's Total gross/Total allowance figures tie exactly to the Balance Sheet's 'Loans and advances to "
        "customers' net line (a ~£58m-£82m gap across all 5 years, consistent in direction and rough magnitude, "
        "most likely reflecting a scope difference such as loan commitment provisions or accrued interest treated "
        "differently between the two disclosures) - reproduced faithfully from each source rather than forced to "
        "tie.\n\n" + ENTITY_NOTE
    ),
    first_col_width=64,
    source_height=260,
    unit_suffix=" (£m)",
)


# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(
        name,
        unit,
        rows_data,
        sources_text,
        note=note,
        first_col_width=52,
        source_height=120,
    )


metric(
    "CET1 Capital",
    "£'000",
    [
        (
            "Common Equity Tier 1 (CET1) capital",
            {
                "FY2025": 1949276,
                "FY2024": 1738133,
                "FY2023": 1842646,
                "FY2022": 1791545,
                "FY2021": 1724002,
            },
        )
    ],
    p3_sources("6"),
)

metric(
    "CET1 Ratio",
    "% of RWA",
    [
        (
            "Common Equity Tier 1 (CET1) ratio",
            {
                "FY2025": "16.74%",
                "FY2024": "15.45%",
                "FY2023": "16.7%",
                "FY2022": "17.2%",
                "FY2021": "15.9%",
            },
        )
    ],
    p3_sources("6"),
)

metric(
    "Tier 1 Capital",
    "£'000",
    [
        (
            "Tier 1 capital",
            {
                "FY2025": 2198973,
                "FY2024": 1987837,
                "FY2023": 1842646,
                "FY2022": 1791545,
                "FY2021": 1724002,
            },
        )
    ],
    p3_sources("6"),
    note="Equal to CET1 capital through FY2023 - TSB held no Additional Tier 1 (AT1) capital until it issued "
    "£249.7m of AT1 securities during FY2024 (see the Cash Flow Statement sheet), which is why Tier 1 "
    "capital first exceeds CET1 capital from FY2024 onward.",
)

metric(
    "Tier 1 Ratio",
    "% of RWA",
    [
        (
            "Tier 1 ratio",
            {
                "FY2025": "18.88%",
                "FY2024": "17.67%",
                "FY2023": "16.7%",
                "FY2022": "17.2%",
                "FY2021": "15.9%",
            },
        )
    ],
    p3_sources("6"),
)

metric(
    "Total Capital",
    "£'000",
    [
        (
            "Total capital",
            {
                "FY2025": 2498973,
                "FY2024": 2287837,
                "FY2023": 2167829,
                "FY2022": 2109761,
                "FY2021": 2024002,
            },
        )
    ],
    p3_sources("6"),
)

metric(
    "Total Capital Ratio",
    "% of RWA",
    [
        (
            "Total capital ratio",
            {
                "FY2025": "21.46%",
                "FY2024": "20.33%",
                "FY2023": "19.6%",
                "FY2022": "20.2%",
                "FY2021": "18.7%",
            },
        )
    ],
    p3_sources("6"),
)

metric(
    "Total RWAs",
    "£'000",
    [
        (
            "Total risk-weighted exposure amount",
            {
                "FY2025": 11646331,
                "FY2024": 11250820,
                "FY2023": 11052751,
                "FY2022": 10442066,
                "FY2021": 10851867,
            },
        )
    ],
    p3_sources("6"),
)

# ---------------------------------------------------------------
# RWA Breakdown - Pillar 3 UK OV1 template. All 5 years sourced from TSB
# Banking Group plc's own Large Subsidiary Disclosures (own-year figures
# cross-checked against the adjacent year's comparative column, which agrees
# exactly in every case). All 5 years tie exactly to the Total RWAs metric
# above.
# ---------------------------------------------------------------
rwa_breakdown_rows = [
    ("SECTION", "RWA by risk category (Pillar 3 UK OV1 template)", {}),
    ("DATA", "Credit risk (excluding counterparty credit risk)", {"FY2025": 9802107, "FY2024": 9417095, "FY2023": 9285021, "FY2022": 8781922, "FY2021": 9375601}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 34637, "FY2024": 44008, "FY2023": 47113, "FY2022": 107036, "FY2021": 17276}),
    ("DATA", "Operational risk", {"FY2025": 1725340, "FY2024": 1710925, "FY2023": 1633140, "FY2022": 1475213, "FY2021": 1400010}),
    ("DATA", "Amounts below the thresholds for deduction (subject to 250% risk weight)", {"FY2025": 84247, "FY2024": 78792, "FY2023": 87477, "FY2022": 77895, "FY2021": 58980}),
    ("TOTAL", "Total RWAs", {"FY2025": 11646331, "FY2024": 11250820, "FY2023": 11052751, "FY2022": 10442066, "FY2021": 10851867}),
]

bw.add_rwa_breakdown_sheet(
    title="TSB Bank plc — RWA Breakdown",
    subtitle="TSB Banking Group plc consolidated Pillar 3 basis, £'000. The 4 category rows sum exactly to Total "
              "RWAs for every year.",
    rows=rwa_breakdown_rows,
    sources_text=(
        "Sources - TSB Banking Group plc consolidated Pillar 3 basis, UK OV1: Overview of risk-weighted exposure "
        "amounts (see entity note on Cash Flow Statement sheet):\n"
        f"FY2025: TSB Banking Group plc Large Subsidiary Disclosures, as at 31 December 2025, p.10 (Table 4: OV1) "
        f"- {P3_25_URL}\n"
        f"FY2024: TSB Banking Group plc Large Subsidiary Disclosures, as at 31 December 2024, p.12 (Table 5: OV1; "
        f"independently cross-checked against the FY2025 disclosure's own FY2024 comparative column, which agrees "
        f"exactly) - {P3_24_URL}\n"
        f"FY2023: TSB Banking Group plc Large Subsidiary Disclosures, as at 31 December 2024, p.12 (Table 5: OV1, "
        f"FY2023 comparative column) - {P3_24_URL}\n"
        f"FY2022: TSB Banking Group plc Large Subsidiary Disclosures 2022, p.12 (Table 5: OV1) - {P3_22_URL}\n"
        f"FY2021: TSB Banking Group plc Large Subsidiary Disclosures 2021, p.11 (Table 5: OV1; independently "
        f"cross-checked against the 2022 disclosure's own FY2021 comparative column, which agrees exactly) "
        f"- {P3_21_URL}"
    ),
    first_col_width=64,
    source_height=220,
    unit_suffix=" (£'000)",
)

metric(
    "Leverage Ratio",
    "£'000 / %",
    [
        (
            "Leverage ratio total exposure measure excluding claims on central banks",
            {
                "FY2025": 40220383,
                "FY2024": 40126116,
                "FY2023": 40338726,
                "FY2022": 42544451,
                "FY2021": 42569754,
            },
        ),
        (
            "Leverage ratio excluding claims on central banks (%)",
            {
                "FY2025": "5.47%",
                "FY2024": "4.95%",
                "FY2023": "4.57%",
                "FY2022": "4.2%",
                "FY2021": "4.0%",
            },
        ),
        (
            "Leverage ratio total exposure measure including claims on central banks (FY2021 as originally reported, pre-2022 PRA methodology)",
            {"FY2021": 47412008},
        ),
        (
            "Leverage ratio including claims on central banks (%) (FY2021 as originally reported, pre-2022 PRA methodology)",
            {"FY2021": "3.6%"},
        ),
    ],
    p3_sources("6"),
    note="From the PRA Rulebook change effective January 2022, TSB's leverage ratio is calculated excluding "
    "central bank claims; FY2021 figures on that basis (42,569,754 / 4.0%) are a restatement published "
    "as the FY2021 comparator in the FY2022 disclosure, not TSB's own FY2021 report - which itself reported "
    "on the pre-2022 basis including central bank claims (47,412,008 / 3.6%, kept on its own row).",
)

metric(
    "LCR",
    "£'000 / %",
    [
        (
            "Total high-quality liquid assets (HQLA) (weighted value - average)",
            {
                "FY2025": 6476199,
                "FY2024": 6921589,
                "FY2023": 7371627,
                "FY2022": 6788964,
                "FY2021": 6441563,
            },
        ),
        (
            "Cash outflows - total weighted value",
            {
                "FY2025": 3765659,
                "FY2024": 4056488,
                "FY2023": 4134068,
                "FY2022": 4326960,
                "FY2021": 4123393,
            },
        ),
        (
            "Cash inflows - total weighted value",
            {
                "FY2025": 250510,
                "FY2024": 230451,
                "FY2023": 218878,
                "FY2022": 260513,
                "FY2021": 202253,
            },
        ),
        (
            "Total net cash outflows (adjusted value)",
            {
                "FY2025": 3515149,
                "FY2024": 3826038,
                "FY2023": 3915190,
                "FY2022": 4066447,
                "FY2021": 3921140,
            },
        ),
        (
            "Liquidity Coverage Ratio (%)",
            {
                "FY2025": "185%",
                "FY2024": "182%",
                "FY2023": "188%",
                "FY2022": "168%",
                "FY2021": "165%",
            },
        ),
    ],
    p3_sources("6"),
    note="LCR is a twelve-month simple average per TSB's disclosed methodology.",
)

metric(
    "NSFR",
    "£'000 / %",
    [
        (
            "Total available stable funding",
            {
                "FY2025": 40945691,
                "FY2024": 42119435,
                "FY2023": 42368266,
                "FY2022": 42774578,
            },
        ),
        (
            "Total required stable funding",
            {
                "FY2025": 26999917,
                "FY2024": 27582817,
                "FY2023": 27601540,
                "FY2022": 28845131,
            },
        ),
        (
            "Net Stable Funding Ratio (%)",
            {
                "FY2025": "152%",
                "FY2024": "153%",
                "FY2023": "154%",
                "FY2022": "148%",
                "FY2021": "Not disclosed",
            },
        ),
    ],
    p3_sources("6"),
    note="NSFR is a four-quarter simple average per TSB's disclosed methodology. Not disclosed for FY2021: the "
    "PRA's averaging methodology for NSFR was only introduced from 1 January 2022, so no FY2021 comparative "
    "was reported (confirmed explicitly in the FY2022 disclosure). Separately, the FY2024 disclosure's own "
    "FY2023 comparator shows NSFR as 153% rather than the 154% in TSB's own FY2023 disclosure used here - a "
    "1 percentage point drift, most likely rounding/methodology refinement between report vintages rather "
    "than an error; both are reproduced faithfully from their respective source documents.",
)

MREL_SOURCES = (
    "Sources - TSB Banking Group plc consolidated Pillar 3 basis, Section 4.4 'Minimum requirement for own funds "
    "and eligible liabilities (MREL)' (see entity note on Cash Flow Statement sheet):\n"
    f"FY2025: TSB Banking Group plc Large Subsidiary Disclosures, as at 31 December 2025, p.13 - {P3_25_URL}\n"
    f"FY2024: TSB Banking Group plc Large Subsidiary Disclosures, as at 31 December 2024, p.16 - {P3_24_URL}\n"
    f"FY2023: TSB Banking Group plc Large Subsidiary Disclosures 2023, p.16 - {P3_23_URL}\n"
    f"FY2022: TSB Banking Group plc Large Subsidiary Disclosures 2022, p.17 - {P3_22_URL}\n"
    f"FY2021: TSB Banking Group plc Large Subsidiary Disclosures 2021, p.14 - {P3_21_URL}"
)

metric(
    "MREL Ratio",
    "%",
    [
        (
            "MREL ratio",
            {
                "FY2025": "27.04%",
                "FY2024": "28.33%",
                "FY2023": "27.8%",
                "FY2022": "26.9%",
                "FY2021": "22.8%",
            },
        ),
        (
            "Internal MREL requirement (TSB is a UK subsidiary of Banco Sabadell; not a resolution entity in its own right)",
            {
                "FY2025": "23.58%",
                "FY2024": "24.03%",
                "FY2023": "18.4%",
                "FY2022": "16.2%",
                "FY2021": "16.2%",
            },
        ),
    ],
    MREL_SOURCES,
    note="TSB is subject to an internal MREL requirement (not external/resolution-entity MREL) as a UK subsidiary "
    "of Banco Sabadell. The requirement shown is TSB's disclosed internal MREL requirement each year - basis "
    "changed from 'excluding regulatory stress buffers' (FY2021-23) to an all-in figure 'including regulatory "
    "stress buffers' (FY2024-25), per TSB's own wording each year; TSB's MREL ratio exceeded its requirement "
    "in every year shown.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 45281.5, "FY2024": 46099.1, "FY2023": 47652.9, "FY2022": 49449.6, "FY2021": 46705.6}),
        ("Loans and advances to customers", {"FY2025": 36268.4, "FY2024": 36330.9, "FY2023": 36245.9, "FY2022": 38050.0, "FY2021": 37383.8}),
        ("Customer deposits", {"FY2025": 35209.0, "FY2024": 35051.2, "FY2023": 34764.3, "FY2022": 36338.2, "FY2021": 35951.9}),
        ("Total equity", {"FY2025": 2338.0, "FY2024": 2120.7, "FY2023": 1954.6, "FY2022": 1929.8, "FY2021": 1866.4}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total income", {"FY2025": 1172.3, "FY2024": 1137.0, "FY2023": 1156.7, "FY2022": 1105.5, "FY2021": 982.9}),
        ("Total operating expenses", {"FY2025": -785.9, "FY2024": -821.8, "FY2023": -852.9, "FY2022": -869.5, "FY2021": -827.3}),
        ("Profit/(loss) for the year", {"FY2025": 251.1, "FY2024": 203.8, "FY2023": 173.4, "FY2022": 100.6, "FY2021": 128.4}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 2120.7, "FY2024": 1954.6, "FY2023": 1929.8, "FY2022": 1866.4, "FY2021": 1724.9}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": 234.9, "FY2024": 216.1, "FY2023": 144.8, "FY2022": 130.4, "FY2021": 141.5}),
        ("Other equity movements, net", {"FY2025": -17.6, "FY2024": -50.0, "FY2023": -120.0, "FY2022": -67.0, "FY2021": 0}),
        ("Closing equity", {"FY2025": 2338.0, "FY2024": 2120.7, "FY2023": 1954.6, "FY2022": 1929.8, "FY2021": 1866.4}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash (used in)/provided by operating activities", {"FY2025": 662.4, "FY2024": 996.9, "FY2023": 1200.7, "FY2022": 596.4, "FY2021": -2145.7}),
        ("Net cash (used in)/provided by investing activities", {"FY2025": -67.2, "FY2024": 21.1, "FY2023": 88.5, "FY2022": -80.3, "FY2021": -839.1}),
        ("Net cash (used in)/provided by financing activities", {"FY2025": -1189.5, "FY2024": -2005.7, "FY2023": -597.9, "FY2022": -25.3, "FY2021": 2779.6}),
        ("Cash and cash equivalents at 31 December", {"FY2025": 4507.3, "FY2024": 5101.6, "FY2023": 6089.3, "FY2022": 5398.0, "FY2021": 4851.1}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "16.74%", "FY2024": "15.45%", "FY2023": "16.7%", "FY2022": "17.2%", "FY2021": "15.9%"}),
        ("Tier 1 Ratio", {"FY2025": "18.88%", "FY2024": "17.67%", "FY2023": "16.7%", "FY2022": "17.2%", "FY2021": "15.9%"}),
        ("Total Capital Ratio", {"FY2025": "21.46%", "FY2024": "20.33%", "FY2023": "19.6%", "FY2022": "20.2%", "FY2021": "18.7%"}),
        ("Leverage Ratio", {"FY2025": "5.47%", "FY2024": "4.95%", "FY2023": "4.57%", "FY2022": "4.2%", "FY2021": "4.0%"}),
        ("LCR", {"FY2025": "185%", "FY2024": "182%", "FY2023": "188%", "FY2022": "168%", "FY2021": "165%"}),
        ("NSFR", {"FY2025": "152%", "FY2024": "153%", "FY2023": "154%", "FY2022": "148%", "FY2021": "Not disclosed"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
    "citation for the underlying document/page. Tier 1 capital first exceeds CET1 from FY2024 onward following "
    "TSB's first AT1 issuance that year. Leverage ratio shown on the 'excluding claims on central banks' basis "
    "for comparability across years (FY2021 was originally reported on the pre-2022 'including' basis - see "
    "Leverage Ratio sheet).",
)

bw.save("/Users/armaan/code/katalysis/banks/TSB FINANCIALS.xlsx")
