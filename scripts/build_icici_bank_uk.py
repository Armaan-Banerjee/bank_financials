import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

P3_URLS = {
    "FY2025": "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/basel-pillar-3-disclosures-FY2024-25.pdf",
    "FY2024": "https://www.icicibank.co.uk/content/dam/icicibank/india/managed-assets/docs/pdf/basel-pillar-3-disclosures-FY2023-24.pdf",
    "FY2023": "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/icici-bank-uk-plc-pillar-3-disclosures-FY2022-23.pdf",
    "FY2022": "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/ICICI-Bank-UK-Plc-Pillar3-disclosures-FY2021-22.pdf",
}

AR2025_URL = "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/financial-report-uk-FY2025.pdf"
AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/04663024/filing-history/MzQzNDA3NTE5MmFkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/04663024/filing-history/MzM5Mjc5MzA4M2FkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/04663024/filing-history/MzM0NjUxNzQwNmFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/04663024/filing-history/MzMwMTQ3NjY0OGFkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "ENTITY NOTE: ICICI Bank UK Plc (Companies House 04663024, FRN 223268, LEI "
    "2138002XB6T14IGKGU43) is the UK-incorporated PRA-authorised bank entity. "
    "Companies House confirms it is an active public limited company, incorporated "
    "11 February 2003, with accounts filed through 31 March 2025. The official Basel "
    "disclosures identify the reporting entity as ICICI Bank UK PLC and present the "
    "UK KM1 data on a standalone Bank basis in USD millions. No parent-group figures "
    "have been substituted."
)

EXEMPTION_NOTE = (
    "FRS 101 CASH-FLOW EXEMPTION: ICICI Bank UK Plc applies the FRS 101 reduced-"
    "disclosure framework and does not prepare a separate Statement of Cash Flows. "
    "This is therefore a Pillar-3-only workbook; the Cash Flow Statement sheet is "
    "retained to document the exemption rather than substituting parent-group cash flows. "
    f"Official supporting source: ICICI Bank UK PLC Strategic report, Directors' report "
    f"and financial statements for the year ended 31 March 2025, cash-flow exemptions "
    f"section (c) - {AR2025_URL}"
)


STATEMENTS_ENTITY_NOTE = (
    "STATEMENTS ENTITY NOTE: the Bank's Balance Sheet, Profit & Loss, Statement of Changes "
    "in Equity, Asset Quality, and RWA Breakdown sheets are presented in USD (the Bank's own "
    "and sole primary reporting currency in every source document reviewed - each Annual "
    "Report and Pillar 3 disclosure gives only an unaudited INR 'convenience translation' "
    "alongside the USD primary figures; no GBP figures are published anywhere by this Bank). "
    "Kept in USD throughout (not converted to £) for consistency with the workbook's own "
    "pre-existing Pillar 3 metric sheets, which are also USD million. "
    + ENTITY_NOTE
)

STATEMENTS_SOURCES = (
    "Sources - ICICI Bank UK Plc's own Annual Reports (Companies House filings, text-native):\n"
    f"FY2025/FY2024: Annual Report and Accounts, year ended 31 March 2025, Profit and loss "
    f"account/Statement of other comprehensive income/Balance sheet/Statement of change in "
    f"equity, pp.36-39 - {AR2025_URL}\n"
    f"FY2023 (own): Annual Report and Accounts, year ended 31 March 2023, pp.38-41 - {AR2023_URL}\n"
    f"FY2022 (own): Annual Report and Accounts, year ended 31 March 2022, pp.39-42 - {AR2022_URL}\n"
    f"FY2021 (own): Annual Report and Accounts, year ended 31 March 2021, pp.35-38 - {AR2021_URL}\n"
    "PRESENTATION NOTES: each year's own originally-published figures are used throughout "
    "(not later restated comparatives), except for the Statement of Changes in Equity where a "
    "genuine, Bank-disclosed prior period adjustment is shown explicitly (see that sheet's own "
    "note). Line items renamed/regrouped across years without changing the underlying figure "
    "are shown on a consistent row (e.g. FY2021-2023's 'Cash and cash equivalents' = FY2024-25's "
    "'Cash and Balances at Central Banks'; FY2021-2024's single 'Investment securities other "
    "than Government/Treasury securities' line = FY2025's 'Debt Securities' + 'Equity shares' "
    "combined, since FY2025 was the only year to break these out separately). P&L uses 'Total "
    "revenue' (FY2021-2023) and 'Net Income' (FY2024-2025) interchangeably for the same "
    "subtotal concept (sum of net interest income plus fee/FX/trading income) - shown on one "
    "row. Balance Sheet: FY2025 has no separate 'Bonds and medium term notes' line (present "
    "FY2021-2024, nil in FY2024) - left blank for FY2025, not force-merged into another line; "
    "FY2025 has no separate 'Deposits by banks' comparator issue (FY2024 explicitly nil, shown "
    "as 0)."
    "\n\n" + STATEMENTS_ENTITY_NOTE
)


def p3_sources():
    lines = [
        "Sources - ICICI Bank UK Plc Basel III Pillar 3 disclosures, UK KM1 Key Metrics template (standalone Bank basis, USD million):"
    ]
    for year in YEARS:
        if year in P3_URLS:
            lines.append(f"{year}: official ICICI Bank UK Pillar 3 disclosure, pp.7–8 - {P3_URLS[year]}")
        else:
            lines.append(
                f"{year}: 31 March 2021 comparative in the official ICICI Bank UK Pillar 3 disclosure, pp.7–8 - {P3_URLS['FY2022']}"
            )
    lines.append(ENTITY_NOTE)
    return "\n".join(lines)


bw = BankWorkbook(bank_name="ICICI Bank UK Plc", years=YEARS, header_color="2A5D67")

BS_ROWS = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents / Cash and Balances at Central Banks", {"FY2025": 403868, "FY2024": 219629, "FY2023": 352907, "FY2022": 336706, "FY2021": 733560}),
    ("DATA", "Investment in Treasury Bills / Government Securities", {"FY2025": 140589, "FY2024": 146509, "FY2023": 206357, "FY2022": 154441, "FY2021": 125760}),
    ("DATA", "Loans and advances to banks", {"FY2025": 339561, "FY2024": 355557, "FY2023": 190371, "FY2022": 141379, "FY2021": 52372}),
    ("DATA", "Loans and advances to customers", {"FY2025": 964471, "FY2024": 888857, "FY2023": 899505, "FY2022": 1182895, "FY2021": 1522138}),
    ("DATA", "Investment securities other than Government/Treasury securities (FY2025: Debt Securities + Equity shares combined)", {"FY2025": 535052, "FY2024": 551784, "FY2023": 431819, "FY2022": 366804, "FY2021": 412986}),
    ("DATA", "Derivative financial instruments", {"FY2025": 22995, "FY2024": 23710, "FY2023": 48189, "FY2022": 20096, "FY2021": 49181}),
    ("DATA", "Tangible & intangible fixed assets", {"FY2025": 2447, "FY2024": 2350, "FY2023": 2348, "FY2022": 2690, "FY2021": 3549}),
    ("DATA", "Other assets", {"FY2025": 11331, "FY2024": 13339, "FY2023": 9221, "FY2022": 27383, "FY2021": 46158}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 1299, "FY2024": 1525, "FY2023": 1343, "FY2022": 9579, "FY2021": 11050}),
    ("TOTAL", "Total assets", {"FY2025": 2421613, "FY2024": 2203260, "FY2023": 2142060, "FY2022": 2241973, "FY2021": 2956754}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2025": 27169, "FY2024": 0, "FY2023": 32456, "FY2022": 28850, "FY2021": 65315}),
    ("DATA", "Customer accounts", {"FY2025": 1901625, "FY2024": 1668596, "FY2023": 1617438, "FY2022": 1541957, "FY2021": 1957458}),
    ("DATA", "Bonds and medium term notes", {"FY2024": 0, "FY2023": 25122, "FY2022": 146358, "FY2021": 197852}),
    ("DATA", "Derivative financial instruments", {"FY2025": 16587, "FY2024": 19191, "FY2023": 28483, "FY2022": 18208, "FY2021": 40360}),
    ("DATA", "Other liabilities", {"FY2025": 28627, "FY2024": 24163, "FY2023": 37868, "FY2022": 15546, "FY2021": 19620}),
    ("DATA", "Accruals and deferred income", {"FY2025": 11671, "FY2024": 11078, "FY2023": 9734, "FY2022": 13680, "FY2021": 14139}),
    ("DATA", "Subordinated debt", {"FY2025": 50568, "FY2024": 50028, "FY2023": 72616, "FY2022": 72954, "FY2021": 76116}),
    ("DATA", "Repurchase Agreements", {"FY2025": 33425, "FY2024": 92735, "FY2023": 0, "FY2022": 88548, "FY2021": 79153}),
    ("TOTAL", "Total Liabilities", {"FY2025": 2069672, "FY2024": 1865791, "FY2023": 1823717, "FY2022": 1926101, "FY2021": 2450013}),
    ("SECTION", "Shareholders' funds", {}),
    ("DATA", "Issued share capital", {"FY2025": 220095, "FY2024": 220095, "FY2023": 220095, "FY2022": 220095, "FY2021": 420095}),
    ("DATA", "Capital contribution", {"FY2025": 12208, "FY2024": 12208, "FY2023": 12208, "FY2022": 12194, "FY2021": 12108}),
    ("DATA", "Retained earnings", {"FY2025": 117423, "FY2024": 103595, "FY2023": 86086, "FY2022": 83076, "FY2021": 72175}),
    ("DATA", "Available for sale reserve", {"FY2025": 2215, "FY2024": 1571, "FY2023": -46, "FY2022": 507, "FY2021": 2363}),
    ("TOTAL", "Total Equity", {"FY2025": 351941, "FY2024": 337469, "FY2023": 318343, "FY2022": 315872, "FY2021": 506741}),
    ("TOTAL", "Total Equity and Liabilities", {"FY2025": 2421613, "FY2024": 2203260, "FY2023": 2142060, "FY2022": 2241973, "FY2021": 2956754}),
]

bw.add_balance_sheet_sheet(
    title="ICICI Bank UK Plc — Statement of Financial Position",
    subtitle="Bank (standalone), USD'000, each year's own originally-published figures. See source note at bottom.",
    rows=BS_ROWS,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=70,
    source_height=220,
    unit_suffix=" (USD'000)",
)

PL_ROWS = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income and similar income", {"FY2025": 124272, "FY2024": 123959, "FY2023": 76554, "FY2022": 54766, "FY2021": 82846}),
    ("DATA", "Interest expense", {"FY2025": -58391, "FY2024": -57300, "FY2023": -23910, "FY2022": -14268, "FY2021": -31939}),
    ("TOTAL", "Net interest income", {"FY2025": 65881, "FY2024": 66659, "FY2023": 52644, "FY2022": 40498, "FY2021": 50907}),
    ("DATA", "Fees and commissions receivable", {"FY2025": 8656, "FY2024": 7399, "FY2023": 6785, "FY2022": 7352, "FY2021": 6461}),
    ("DATA", "Foreign exchange revaluation gains", {"FY2025": 8918, "FY2024": 8389, "FY2023": 6343, "FY2022": 5786, "FY2021": 6376}),
    ("DATA", "Income/(loss) on financial instruments at fair value through P&L", {"FY2025": 1238, "FY2024": -17, "FY2023": 1095, "FY2022": 461, "FY2021": -157}),
    ("DATA", "Profit/(loss) on sale of financial assets", {"FY2025": 2601, "FY2024": 3221, "FY2023": -7094, "FY2022": 66, "FY2021": -1336}),
    ("DATA", "Other operating income", {"FY2025": 28, "FY2024": 40, "FY2023": 279, "FY2022": 294, "FY2021": 326}),
    ("TOTAL", "Total revenue / Net Income", {"FY2025": 87322, "FY2024": 85691, "FY2023": 60052, "FY2022": 54457, "FY2021": 62577}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Administrative expenses", {"FY2025": -51266, "FY2024": -46758, "FY2023": -37348, "FY2022": -38960, "FY2021": -35531}),
    ("DATA", "Depreciation", {"FY2025": -786, "FY2024": -709, "FY2023": -956, "FY2022": -1229, "FY2021": -1157}),
    ("DATA", "Impairment on investment securities", {"FY2025": -27, "FY2024": -23, "FY2023": -79, "FY2022": -20, "FY2021": 49}),
    ("DATA", "Impairment on loans and advances", {"FY2025": -3207, "FY2024": -7145, "FY2023": -5867, "FY2022": -2906, "FY2021": -8414}),
    ("TOTAL", "Profit on ordinary activities before tax", {"FY2025": 32036, "FY2024": 31056, "FY2023": 15802, "FY2022": 11342, "FY2021": 17524}),
    ("DATA", "Taxation on ordinary activities", {"FY2025": -5208, "FY2024": -2279, "FY2023": -2792, "FY2022": -441, "FY2021": -2732}),
    ("TOTAL", "Profit for the year", {"FY2025": 26828, "FY2024": 28777, "FY2023": 13010, "FY2022": 10901, "FY2021": 14792}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Movement in valuation of available for sale debt securities, net of tax", {"FY2025": 644, "FY2024": 1617, "FY2023": -553, "FY2022": -1856, "FY2021": 38143}),
    ("TOTAL", "Total comprehensive income for the year", {"FY2025": 27472, "FY2024": 30394, "FY2023": 12457, "FY2022": 9045, "FY2021": 52935}),
]

bw.add_income_statement_sheet(
    title="ICICI Bank UK Plc — Profit and Loss Account",
    subtitle="Bank (standalone), USD'000, each year's own originally-published figures. See source note at bottom.",
    rows=PL_ROWS,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=70,
    source_height=220,
    unit_suffix=" (USD'000)",
)

EQUITY_HEADERS = ["Issued share capital", "Retained earnings", "Available for sale reserve", "Capital contribution", "Total equity"]
EQUITY_ROWS = [
    ("TOTAL", "Balance as at 1 April 2020 (FY2021's own opening)", (420095, 57383, -35780, 11634, 453332)),
    ("DATA", "Capital contribution (share-based payments), FY2021", (None, None, None, 474, 474)),
    ("DATA", "Profit for the year, FY2021", (None, 14792, None, None, 14792)),
    ("DATA", "Movement in valuation of AFS debt securities, net of tax, FY2021", (None, None, 38143, None, 38143)),
    ("TOTAL", "Balance as at 31 March 2021 / 1 April 2021", (420095, 72175, 2363, 12108, 506741)),
    ("DATA", "Capital contribution (share-based payments), FY2022", (None, None, None, 86, 86)),
    ("DATA", "Profit for the year, FY2022", (None, 10901, None, None, 10901)),
    ("DATA", "Movement in valuation of AFS debt securities, net of tax, FY2022", (None, None, -1856, None, -1856)),
    ("DATA", "Capital reduction, FY2022", (-200000, None, None, None, -200000)),
    ("TOTAL", "Balance as at 31 March 2022 / 1 April 2022", (220095, 83076, 507, 12194, 315872)),
    ("DATA", "Capital contribution (share-based payments), FY2023", (None, None, None, 14, 14)),
    ("DATA", "Profit for the year, FY2023", (None, 13010, None, None, 13010)),
    ("DATA", "Movement in valuation of AFS debt securities, net of tax, FY2023", (None, None, -553, None, -553)),
    ("DATA", "Dividends paid, FY2023", (None, -10000, None, None, -10000)),
    ("TOTAL", "Balance as at 31 March 2023 (as originally reported in the FY2023 Annual Report)", (220095, 86086, -46, 12208, 318343)),
    ("DATA", "Prior period adjustment (disclosed only in the FY2024 Annual Report, restating the 1 April 2022 opening retained earnings - see source note)", (None, -1268, None, None, -1268)),
    ("TOTAL", "Restated balance as at 1 April 2023 (per the FY2024 Annual Report)", (220095, 84818, -46, 12208, 317075)),
    ("DATA", "Profit for the year, FY2024", (None, 28777, None, None, 28777)),
    ("DATA", "Movement in valuation of AFS debt securities, net of tax, FY2024", (None, None, 1617, None, 1617)),
    ("DATA", "Dividends paid, FY2024", (None, -10000, None, None, -10000)),
    ("TOTAL", "Balance as at 31 March 2024 / 1 April 2024", (220095, 103595, 1571, 12208, 337469)),
    ("DATA", "Profit for the year, FY2025", (None, 26828, None, None, 26828)),
    ("DATA", "Movement in valuation of AFS debt securities, net of tax, FY2025", (None, None, 644, None, 644)),
    ("DATA", "Dividends paid, FY2025", (None, -13000, None, None, -13000)),
    ("TOTAL", "Closing shareholders' funds as at 31 March 2025", (220095, 117423, 2215, 12208, 351941)),
]

bw.add_equity_changes_sheet(
    title="ICICI Bank UK Plc — Statement of Changes in Equity",
    subtitle=(
        "USD'000, chronological, oldest to newest. Equity reconciliation ladder confirmed: each year's "
        "own closing balance ties exactly to both the next year's own opening balance and that year's own "
        "Balance Sheet Total equity, EXCEPT the FY2023 close, which is bridged by an explicit Prior period "
        "adjustment row - the FY2024 Annual Report discloses a $1,268k restatement to the 1 April 2022 "
        "opening retained earnings (not explained further in that filing) that cascades through to a "
        "different 1 April 2023 opening figure ($317,075k) than the FY2023 Annual Report's own originally-"
        "published 31 March 2023 closing figure ($318,343k). Both figures are genuine, Bank-disclosed "
        "numbers from their respective reports - shown explicitly, not force-reconciled."
    ),
    headers=EQUITY_HEADERS,
    rows=EQUITY_ROWS,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=70,
    source_height=220,
)

bw.add_cash_flow_sheet(
    title="ICICI Bank UK Plc — Cash Flow Statement",
    subtitle="Not applicable — FRS 101 cash-flow-statement exemption applies for the periods covered.",
    rows=[("SECTION", "Not applicable", {}), ("DATA", EXEMPTION_NOTE, {})],
    sources_text=EXEMPTION_NOTE + "\n\n" + ENTITY_NOTE,
    first_col_width=105,
    source_height=180,
    unit_suffix="",
)


AQ_ROWS = [
    ("SECTION", "Loans and advances to customers, by credit risk category", {}),
    ("DATA", "Neither past due nor impaired", {"FY2025": 965499, "FY2024": 837804, "FY2023": 864553, "FY2022": 1098791, "FY2021": 1465451}),
    ("DATA", "Past due not impaired", {"FY2025": 0, "FY2024": 43847, "FY2023": 3833, "FY2022": 69855, "FY2021": 40536}),
    ("DATA", "Impaired", {"FY2025": 8035, "FY2024": 13901, "FY2023": 75966, "FY2022": 54999, "FY2021": 55208}),
    ("DATA", "Impairment & collective allowances", {"FY2025": -9063, "FY2024": -6695, "FY2023": -44847, "FY2022": -40750, "FY2021": -39057}),
    ("TOTAL", "Total loans and advances to customers (net)", {"FY2025": 964471, "FY2024": 888857, "FY2023": 899505, "FY2022": 1182895, "FY2021": 1522138}),
    ("DATA", "Impaired ratio (Impaired / gross loans)", {"FY2025": "0.83%", "FY2024": "1.55%", "FY2023": "8.04%", "FY2022": "4.49%", "FY2021": "3.54%"}),
    ("DATA", "Coverage ratio (Impairment & collective allowances / Impaired)", {"FY2025": "112.79%", "FY2024": "48.16%", "FY2023": "59.03%", "FY2022": "74.09%", "FY2021": "70.75%"}),
]

bw.add_asset_quality_sheet(
    title="ICICI Bank UK Plc — Asset Quality",
    subtitle=(
        "Bank (standalone), USD'000. No IFRS 9 Stage 1/2/3 split disclosed - the Bank's own Note 19 "
        "'Potential credit risk on financial instruments' breaks the loan book into 'Neither past due nor "
        "impaired' / 'Past due not impaired' / 'Impaired' instead, confirmed by reading each year's own "
        "note in full. FY2025's 'Past due not impaired' is explicitly disclosed as NIL, not blank/missing. "
        "See source note at bottom."
    ),
    rows=AQ_ROWS,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=75,
    source_height=220,
    unit_suffix=" (USD'000)",
)


def metric(name, unit, rows, note=None):
    bw.add_metric_sheet(
        name, unit, rows, p3_sources(), note=note, first_col_width=58, source_height=155
    )


metric("CET1 Capital", "USD million", [("Common Equity Tier 1 (CET1) capital", {"FY2025": 322.9, "FY2024": 311.3, "FY2023": 295.4, "FY2022": 293.0, "FY2021": 493.9})])
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "19.57%", "FY2024": "20.14%", "FY2023": "21.54%", "FY2022": "17.79%", "FY2021": "23.80%"})])
metric("Tier 1 Capital", "USD million", [("Tier 1 capital", {"FY2025": 322.9, "FY2024": 311.3, "FY2023": 295.4, "FY2022": 293.0, "FY2021": 493.9})])
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {"FY2025": "19.57%", "FY2024": "20.14%", "FY2023": "21.54%", "FY2022": "17.79%", "FY2021": "23.80%"})])
metric("Total Capital", "USD million", [("Total capital", {"FY2025": 372.9, "FY2024": 361.3, "FY2023": 371.9, "FY2022": 378.0, "FY2021": 586.7})])
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2025": "22.60%", "FY2024": "23.37%", "FY2023": "27.12%", "FY2022": "22.96%", "FY2021": "28.27%"})])
metric("Total RWAs", "USD million", [("Total risk-weighted exposure amount", {"FY2025": 1649.7, "FY2024": 1546.2, "FY2023": 1371.5, "FY2022": 1646.7, "FY2021": 2075.1})])

RWA_ROWS = [
    ("SECTION", "UK OV1: Overview of risk weighted exposure amounts", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 1487.3, "FY2024": 1397.2, "FY2023": 1221.6, "FY2022": 1491.1, "FY2021": 1865.8}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 16.0, "FY2024": 21.5, "FY2023": 34.0, "FY2022": 32.1, "FY2021": 54.4}),
    ("DATA", "Securitisation exposures in the non-trading book", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 12.5}),
    ("DATA", "Position, foreign exchange and commodities risk (Market risk)", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Operational risk", {"FY2025": 146.4, "FY2024": 127.5, "FY2023": 115.9, "FY2022": 123.5, "FY2021": 142.4}),
    ("DATA", "Amounts below thresholds for deduction (subject to 250% risk weight)", {"FY2025": 4.6, "FY2024": 15.0, "FY2023": 17.6, "FY2022": 22.0, "FY2021": 21.8}),
    ("TOTAL", "Total RWA", {"FY2025": 1649.7, "FY2024": 1546.2, "FY2023": 1371.5, "FY2022": 1646.7, "FY2021": 2075.1}),
]

bw.add_rwa_breakdown_sheet(
    title="ICICI Bank UK Plc — RWA Breakdown",
    subtitle="Bank (standalone), USD million. UK OV1 template - source: official Basel III Pillar 3 Disclosures. See source note at bottom.",
    rows=RWA_ROWS,
    sources_text=p3_sources(),
    first_col_width=68,
    source_height=200,
    unit_suffix=" (USD million)",
)

metric(
    "Leverage Ratio",
    "USD million / %",
    [
        ("Total exposure measure excluding claims on central banks", {"FY2025": 2276.7, "FY2024": 2086.8, "FY2023": 1914.3, "FY2022": 2085.6}),
        ("Leverage ratio excluding claims on central banks", {"FY2025": "14.18%", "FY2024": "14.92%", "FY2023": "15.43%", "FY2022": "14.05%"}),
    ],
    note="The FY2021 comparative was not disclosed in the FY2022 UK KM1 leverage rows and is left blank rather than substituted.",
)
metric("LCR", "%", [("Liquidity coverage ratio", {"FY2025": "190.08%", "FY2024": "240.20%", "FY2023": "226.83%", "FY2022": "226.90%"})], note="The FY2021 comparative was not disclosed in the FY2022 UK KM1 LCR rows and is left blank rather than substituted.")
metric("NSFR", "%", [("Net stable funding ratio", {"FY2025": "151.03%", "FY2024": "159.20%", "FY2023": "147.72%", "FY2022": "141.69%"})], note="The FY2021 comparative was not disclosed in the FY2022 UK KM1 NSFR rows and is left blank rather than substituted.")
bw.add_not_disclosed_metric_sheets(["MREL Ratio"], p3_sources(), per_note={"MREL Ratio": "No MREL ratio appears in the official ICICI Bank UK Basel disclosures reviewed for FY2021–FY2025; no figure has been inferred."})

bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit=None,
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 2421613, "FY2024": 2203260, "FY2023": 2142060, "FY2022": 2241973, "FY2021": 2956754}),
        ("Loans and advances to customers", {"FY2025": 964471, "FY2024": 888857, "FY2023": 899505, "FY2022": 1182895, "FY2021": 1522138}),
        ("Customer accounts", {"FY2025": 1901625, "FY2024": 1668596, "FY2023": 1617438, "FY2022": 1541957, "FY2021": 1957458}),
        ("Total Equity", {"FY2025": 351941, "FY2024": 337469, "FY2023": 318343, "FY2022": 315872, "FY2021": 506741}),
    ],
    balance_sheet_unit="USD'000",
    income_statement_totals=[
        ("Total revenue / Net Income", {"FY2025": 87322, "FY2024": 85691, "FY2023": 60052, "FY2022": 54457, "FY2021": 62577}),
        ("Administrative expenses", {"FY2025": -51266, "FY2024": -46758, "FY2023": -37348, "FY2022": -38960, "FY2021": -35531}),
        ("Profit for the year", {"FY2025": 26828, "FY2024": 28777, "FY2023": 13010, "FY2022": 10901, "FY2021": 14792}),
    ],
    income_statement_unit="USD'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 337469, "FY2024": 317075, "FY2023": 315872, "FY2022": 506741, "FY2021": 453332}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": 27472, "FY2024": 30394, "FY2023": 12457, "FY2022": 9045, "FY2021": 52935}),
        ("Closing equity", {"FY2025": 351941, "FY2024": 337469, "FY2023": 318343, "FY2022": 315872, "FY2021": 506741}),
    ],
    equity_changes_unit="USD'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "19.57%", "FY2024": "20.14%", "FY2023": "21.54%", "FY2022": "17.79%", "FY2021": "23.80%"}),
        ("Tier 1 Ratio", {"FY2025": "19.57%", "FY2024": "20.14%", "FY2023": "21.54%", "FY2022": "17.79%", "FY2021": "23.80%"}),
        ("Total Capital Ratio", {"FY2025": "22.60%", "FY2024": "23.37%", "FY2023": "27.12%", "FY2022": "22.96%", "FY2021": "28.27%"}),
        ("Leverage Ratio", {"FY2025": "14.18%", "FY2024": "14.92%", "FY2023": "15.43%", "FY2022": "14.05%"}),
        ("LCR", {"FY2025": "190.08%", "FY2024": "240.20%", "FY2023": "226.83%", "FY2022": "226.90%"}),
        ("NSFR", {"FY2025": "151.03%", "FY2024": "159.20%", "FY2023": "147.72%", "FY2022": "141.69%"}),
    ],
    note="ICICI Bank UK Plc's FRS 101 cash-flow exemption means no cash-flow summary or chart is shown (5 blocks total: Balance Sheet, P&L, Equity, and Ratios - no Cash Flow block). All statement figures are Bank-standalone USD, kept in the Bank's own native reporting currency (not converted to £) for consistency with the pre-existing Pillar 3 sheets, which are also USD. FY2026 is available from the official archive but excluded to retain the project's FY2021–FY2025 window.",
)

bw.save("/Users/armaan/code/katalysis/banks/ICICI BANK UK FINANCIALS.xlsx")
