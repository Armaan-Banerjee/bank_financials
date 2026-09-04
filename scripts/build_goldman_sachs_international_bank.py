import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, calendar year-end (31 December)
YEAR_LABEL = {y: y for y in YEARS}

# Bank of England GBP/USD rates via poundsterlinglive.com's published archive,
# reusing the exact table already established for Zenith Bank UK / Credit
# Suisse International (same 31 December calendar year-end).
FX_SPOT = {
    "FY2020": 1.3661,  # 31 Dec 2020 - only used for FY2021's opening cash balance
    "FY2021": 1.3521,  # 31 Dec 2021
    "FY2022": 1.2097,  # 30 Dec 2022 (31st was a Saturday)
    "FY2023": 1.2732,  # 29 Dec 2023 (31st was a Sunday)
    "FY2024": 1.2515,  # 31 Dec 2024
    "FY2025": 1.3448,  # 31 Dec 2025
}
FX_AVG = {
    "FY2021": 1.3752,
    "FY2022": 1.2362,
    "FY2023": 1.2439,
    "FY2024": 1.2782,
    "FY2025": 1.3193,
}
PREV_YEAR = {"FY2021": "FY2020", "FY2022": "FY2021", "FY2023": "FY2022", "FY2024": "FY2023", "FY2025": "FY2024"}


def flow(usd_m, year):
    """Flow figures (cash flow statement lines) - converted at the year's AVERAGE rate, £m."""
    return round(usd_m / FX_AVG[year], 1)


def stock(usd_m, year):
    """Point-in-time figures (balances, capital) - converted at that year-end's SPOT rate, £m."""
    return round(usd_m / FX_SPOT[year], 1)


AA_2025_URL = "https://find-and-update.company-information.service.gov.uk/company/01122503/filing-history/MzUxNzc2NzE5OGFkaXF6a2N4/document?format=pdf&download=0"
AA_2023_URL = "https://find-and-update.company-information.service.gov.uk/company/01122503/filing-history/MzQxOTg0MjAwMGFkaXF6a2N4/document?format=pdf&download=0"
AA_2021_URL = "https://find-and-update.company-information.service.gov.uk/company/01122503/filing-history/MzMzODY3Mzc0NGFkaXF6a2N4/document?format=pdf&download=0"
P3_2025_URL = "https://www.goldmansachs.com/disclosures/gsguk-q4-2025-pillar-3.pdf/"
P3_2024_URL = "https://www.goldmansachs.com/disclosures/gsguk-q4-2024-pillar-3.pdf/"
P3_2023_URL = "https://www.goldmansachs.com/disclosures/gsguk-q4-2023-pillar-3.pdf/"
P3_2022_URL = "https://www.goldmansachs.com/disclosures/gsguk-q4-2022-pillar-3.pdf/"
P3_2021_URL = "https://www.goldmansachs.com/disclosures/gsguk-q4-2021-pillar-3.pdf/"

ENTITY_NOTE = (
    "Goldman Sachs International Bank (GSIB, company 01122503, FRN 124659) is a PRA-authorised UK unlimited "
    "company, wholly-owned by Goldman Sachs Group UK Limited (GSG UK) and ultimately by The Goldman Sachs "
    "Group, Inc. (US) - a DISTINCT legal entity from Goldman Sachs International (GSI, company 02263951, the "
    "UK broker-dealer, not a bank) and from Goldman Sachs Bank Europe SE. All figures are GSIB's own entity-"
    "level disclosure, converted from its reporting currency (USD) to GBP using the Bank of England's published "
    "GBP/USD spot rate (point-in-time/balance figures) or average rate over the fiscal year (flow figures) - "
    "see the FX conversion methodology note below."
)

PILLAR3_NOTE = (
    "PILLAR 3 STRUCTURE: GSIB's own Annual Report states every year (Note 1, 'Basel III Pillar 3 Disclosures'): "
    "\"The bank is included in the consolidated Pillar 3 disclosures of GSG UK, as required by the U.K. capital "
    "framework\". GSIB does not publish a separate standalone Pillar 3 report, but the official GSG UK Q4 Pillar 3 "
    "disclosures explicitly provide GSIB columns/tables alongside GSGUK and GSI. The GSIB breakout is used here "
    "rather than substituting GSGUK consolidated figures. FY2021 GSIB capital, ratios, RWA, leverage and LCR are "
    "available; FY2022-FY2025 also provide GSIB NSFR. No GSIB-specific numeric MREL value is shown in the reviewed "
    "reports, so MREL remains explicitly unavailable."
)

FX_METHOD_NOTE = (
    "FX conversion: point-in-time figures (cash balances, capital) converted at the Bank of England GBP/USD "
    "SPOT rate as at each fiscal year-end; flow figures (cash flow statement lines) converted at the AVERAGE "
    "rate over that fiscal year. Rates used (£1 = $X): 31 Dec 2020 spot 1.3661 (FY2021 opening cash only); "
    "FY2021 spot 1.3521 / average 1.3752; FY2022 spot 1.2097 / average 1.2362; FY2023 spot 1.2732 / average "
    "1.2439; FY2024 spot 1.2515 / average 1.2782; FY2025 spot 1.3448 / average 1.3193 - same table already "
    "established for Zenith Bank UK / Credit Suisse International (identical 31 December year-end). Converting "
    "stocks and flows at different rates means the statement doesn't tie in GBP by itself - an 'Effect of GBP/"
    "USD translation' line is included, computed programmatically as the balancing figure (never hardcoded), "
    "labelled clearly as a translation artefact with no bearing on GSIB's actual USD results."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Goldman Sachs International Bank's own Statement of Cash Flows, converted from "
    "USD to GBP (see FX note below):\n"
    f"FY2025/FY2024: Annual Report for the Financial Year Ended December 31, 2025, p.23 (filed at Companies "
    f"House 26 Apr 2026) - {AA_2025_URL}\n"
    f"FY2023/FY2022: Annual Report for the Financial Year Ended December 31, 2023, p.23 (filed 29 Apr 2024) - "
    f"{AA_2023_URL}\n"
    f"FY2021: Annual Report for the Financial Period Ended December 31, 2021, p.22 (filed 9 May 2022) - "
    f"{AA_2021_URL}\n"
    + ENTITY_NOTE + "\n\n" + FX_METHOD_NOTE
)


def p3_sources():
    return (
        "Sources - official Goldman Sachs Group UK Limited Q4 Pillar 3 Disclosures. The reports present explicit "
        "GSIB columns/tables for the metrics used here (USD millions and percentages):\n"
        f"FY2025: Table 1 / pp.15-16 - {P3_2025_URL}\n"
        f"FY2024: Table 1 / pp.14-15 - {P3_2024_URL}\n"
        f"FY2023: Table 1 / pp.14-16 - {P3_2023_URL}\n"
        f"FY2022: Table 1 / pp.14-15 - {P3_2022_URL}\n"
        f"FY2021: Table 2 / p.16, RWA Table 8 / p.20, LCR Table 39 / p.53, leverage Table 40 / p.54 - {P3_2021_URL}\n"
        + ENTITY_NOTE + "\n\n" + PILLAR3_NOTE + "\n\n" + FX_METHOD_NOTE
    )


bw = BankWorkbook(bank_name="Goldman Sachs International Bank", years=YEARS, year_label=YEAR_LABEL, header_color="B651C8")

STATEMENTS_SOURCES_NOTE = (
    "Sources - Goldman Sachs International Bank's own Balance Sheet / Income Statement / Statement of "
    "Comprehensive Income / Statement of Changes in Equity (entity-level, converted from USD to GBP - see FX "
    "note below), each year's own originally-published figures (not a later year's restated comparative):\n"
    f"FY2025/FY2024: Annual Report for the Financial Year Ended December 31, 2025, pp.20-22 (filed at Companies "
    f"House 26 Apr 2026) - {AA_2025_URL}\n"
    f"FY2023/FY2022: Annual Report for the Financial Year Ended December 31, 2023, pp.20-22 (filed 29 Apr 2024) "
    f"- {AA_2023_URL}\n"
    f"FY2021: Annual Report for the Financial Period Ended December 31, 2021, pp.19-21 (filed 9 May 2022) - "
    f"{AA_2021_URL}\n"
    + ENTITY_NOTE + "\n\n" + FX_METHOD_NOTE
)

# ---------------------------------------------------------------
# Balance Sheet
# ---------------------------------------------------------------
BS_ROWS_USD = [
    ("SECTION", "Assets", None),
    ("DATA", "Cash and cash equivalents", {"FY2025": 8460, "FY2024": 11978, "FY2023": 19932, "FY2022": 18455, "FY2021": 9901}),
    ("DATA", "Collateralised agreements", {"FY2025": 77833, "FY2024": 58191, "FY2023": 52139, "FY2022": 37489, "FY2021": 55190}),
    ("DATA", "Customer and other receivables", {"FY2025": 1538, "FY2024": 2554, "FY2023": 916, "FY2022": 209, "FY2021": 292}),
    ("DATA", "Trading assets", {"FY2025": 3863, "FY2024": 3263, "FY2023": 5214, "FY2022": 5367, "FY2021": 3227}),
    ("DATA", "Loans", {"FY2025": 8839, "FY2024": 8134, "FY2023": 8075, "FY2022": 9109, "FY2021": 11800}),
    ("DATA", "Investments", {"FY2025": 9495, "FY2024": 5471, "FY2023": 3168, "FY2022": 4078, "FY2021": 5080}),
    ("DATA", "Other assets", {"FY2025": 119, "FY2024": 192, "FY2023": 405, "FY2022": 2273, "FY2021": 1032}),
    ("TOTAL", "Total assets", {"FY2025": 110147, "FY2024": 89783, "FY2023": 89849, "FY2022": 76980, "FY2021": 86522}),
    ("SECTION", "Liabilities", None),
    ("DATA", "Collateralised financings", {"FY2025": 1898, "FY2024": 596, "FY2023": 41, "FY2022": 301, "FY2021": 234}),
    ("DATA", "Customer and other payables", {"FY2025": 212, "FY2024": 583, "FY2023": 772, "FY2022": 764, "FY2021": 252}),
    ("DATA", "Trading liabilities", {"FY2025": 3295, "FY2024": 2995, "FY2023": 1636, "FY2022": 1604, "FY2021": 826}),
    ("DATA", "Deposits", {"FY2025": 97472, "FY2024": 78793, "FY2023": 81061, "FY2022": 67841, "FY2021": 79635}),
    ("DATA", "Unsecured borrowings", {"FY2025": 1968, "FY2024": 2105, "FY2023": 2128, "FY2022": 2827, "FY2021": 1896}),
    ("DATA", "Other liabilities", {"FY2025": 227, "FY2024": 223, "FY2023": 193, "FY2022": 169, "FY2021": 176}),
    ("TOTAL", "Total liabilities", {"FY2025": 105072, "FY2024": 85295, "FY2023": 85831, "FY2022": 73506, "FY2021": 83019}),
    ("SECTION", "Shareholder's equity", None),
    ("DATA", "Share capital", {"FY2025": 63, "FY2024": 63, "FY2023": 63, "FY2022": 63, "FY2021": 63}),
    ("DATA", "Share premium account", {"FY2025": 2094, "FY2024": 2094, "FY2023": 2094, "FY2022": 2094, "FY2021": 2094}),
    ("DATA", "Retained earnings", {"FY2025": 3090, "FY2024": 2602, "FY2023": 2144, "FY2022": 1638, "FY2021": 1420}),
    ("DATA", "Accumulated other comprehensive income", {"FY2025": -172, "FY2024": -271, "FY2023": -283, "FY2022": -321, "FY2021": -74}),
    ("TOTAL", "Total shareholder's equity", {"FY2025": 5075, "FY2024": 4488, "FY2023": 4018, "FY2022": 3474, "FY2021": 3503}),
    ("TOTAL", "Total liabilities and shareholder's equity", {"FY2025": 110147, "FY2024": 89783, "FY2023": 89849, "FY2022": 76980, "FY2021": 86522}),
]
balance_sheet_rows = [
    (kind, label, ({} if values is None else {y: stock(v, y) for y, v in values.items()}))
    for kind, label, values in BS_ROWS_USD
]

bw.add_balance_sheet_sheet(
    title="Goldman Sachs International Bank — Balance Sheet",
    subtitle="£m, converted from USD - see source note at bottom for FX methodology and rates used.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES_NOTE,
    first_col_width=90,
    source_height=320,
    unit_suffix=" (£m, conv. from USD)",
)

# ---------------------------------------------------------------
# Profit & Loss (Income Statement / Statement of Comprehensive Income)
# ---------------------------------------------------------------
PL_ROWS_USD = [
    ("SECTION", "Income", None),
    ("DATA", "Interest income - financial instruments at FVTPL", {"FY2025": 1395, "FY2024": 1350, "FY2023": 2626, "FY2022": 1070, "FY2021": 346}),
    ("DATA", "Interest income - financial instruments at FVOCI", {"FY2025": 101, "FY2024": 29, "FY2023": 10, "FY2022": 10, "FY2021": 6}),
    ("DATA", "Interest income - financial instruments at amortised cost", {"FY2025": 2823, "FY2024": 3542, "FY2023": 1789, "FY2022": 641, "FY2021": 340}),
    ("DATA", "Interest expense - financial instruments at FVTPL", {"FY2025": -1152, "FY2024": -1137, "FY2023": -1407, "FY2022": -445, "FY2021": -101}),
    ("DATA", "Interest expense - financial instruments at amortised cost", {"FY2025": -2729, "FY2024": -3423, "FY2023": -2254, "FY2022": -699, "FY2021": -217}),
    ("TOTAL", "Net interest income", {"FY2025": 438, "FY2024": 361, "FY2023": 764, "FY2022": 577, "FY2021": 374}),
    ("DATA", "Gains/(losses) - financial instruments at FVTPL", {"FY2025": 340, "FY2024": 333, "FY2023": 9, "FY2022": -82, "FY2021": -75}),
    ("DATA", "Gains - financial instruments at FVOCI", {"FY2025": 3, "FY2023": 0}),
    ("DATA", "Fees and commissions", {"FY2025": 86, "FY2024": 72, "FY2023": 75, "FY2022": 51, "FY2021": 102}),
    ("TOTAL", "Non-interest income/(losses)", {"FY2025": 429, "FY2024": 405, "FY2023": 84, "FY2022": -31, "FY2021": 27}),
    ("TOTAL", "Net revenues", {"FY2025": 867, "FY2024": 766, "FY2023": 848, "FY2022": 546, "FY2021": 401}),
    ("DATA", "Impairments on financial instruments", {"FY2025": 21, "FY2024": 50, "FY2023": 11, "FY2022": -94, "FY2021": 89}),
    ("DATA", "Operating expenses", {"FY2025": -209, "FY2024": -175, "FY2023": -160, "FY2022": -176, "FY2021": -207}),
    ("TOTAL", "Profit before taxation", {"FY2025": 679, "FY2024": 641, "FY2023": 699, "FY2022": 276, "FY2021": 283}),
    ("DATA", "Income tax expense", {"FY2025": -191, "FY2024": -183, "FY2023": -193, "FY2022": -58, "FY2021": -82}),
    ("TOTAL", "Profit for the financial year", {"FY2025": 488, "FY2024": 458, "FY2023": 506, "FY2022": 218, "FY2021": 201}),
    ("SECTION", "Other comprehensive income/(loss)", None),
    ("DATA", "Debt valuation adjustment", {"FY2024": -5, "FY2023": -6, "FY2022": 22, "FY2021": 14}),
    ("DATA", "UK deferred tax on items not reclassified", {"FY2024": 1, "FY2023": 2, "FY2022": -6, "FY2021": -4}),
    ("TOTAL", "Total items not reclassified subsequently to P&L", {"FY2024": -4, "FY2023": -4, "FY2022": 16, "FY2021": 10}),
    ("DATA", "Translation losses and net investment hedges", {"FY2025": -1, "FY2024": -2, "FY2023": -2, "FY2022": -3, "FY2021": 1}),
    ("DATA", "Gains/(losses) - financial instruments at FVOCI", {"FY2025": 139, "FY2024": 25, "FY2023": 61, "FY2022": -363, "FY2021": -95}),
    ("DATA", "UK deferred tax on items reclassified", {"FY2025": -39, "FY2024": -7, "FY2023": -17, "FY2022": 103, "FY2021": 25}),
    ("TOTAL", "Total items reclassified subsequently to P&L", {"FY2025": 99, "FY2024": 16, "FY2023": 42, "FY2022": -263, "FY2021": -69}),
    ("TOTAL", "Other comprehensive income/(loss) for the year, net of tax", {"FY2025": 99, "FY2024": 12, "FY2023": 38, "FY2022": -247, "FY2021": -59}),
    ("TOTAL", "Total comprehensive income/(loss) for the financial year", {"FY2025": 587, "FY2024": 470, "FY2023": 544, "FY2022": -29, "FY2021": 142}),
]
income_statement_rows = [
    (kind, label, ({} if values is None else {y: flow(v, y) for y, v in values.items()}))
    for kind, label, values in PL_ROWS_USD
]

bw.add_income_statement_sheet(
    title="Goldman Sachs International Bank — Income Statement / Statement of Comprehensive Income",
    subtitle="£m, converted from USD - see source note at bottom for FX methodology and rates used.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES_NOTE + "\n\nPRESENTATION NOTE: FY2025's Statement of Comprehensive Income "
    "discloses gains from financial instruments at FVOCI as its own OCI line under 'items that will be "
    "reclassified' (£139m) - shown here in the Income line; FY2024/FY2023/FY2022/FY2021 show the equivalent as "
    "the same OCI line, consistent presentation across all 5 years. No standalone Gains-at-FVOCI Income-statement "
    "line is disclosed for FY2024/FY2022/FY2021 (nil/immaterial per the source table) - left blank rather than "
    "guessed.",
    first_col_width=90,
    source_height=340,
    unit_suffix=" (£m, conv. from USD)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - built year-by-year per the map's
# per-year reconciliation ladder: verified in USD first (every closing
# balance ties exactly to both the next year's own opening balance and
# that year's own Balance Sheet Total shareholder's equity, with ZERO
# plug rows needed in USD - genuinely a clean roll-forward). An "FX
# translation effect on equity, net" row (Total column only, computed
# as the balancing figure) is still needed for the GBP presentation,
# since opening/movement/closing convert at 3 different point-in-time
# rates - same treatment as Credit Suisse International/Bank Mandiri
# Europe/Bank Saderat.
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Share capital", "Share premium", "Retained earnings", "AOCI", "Total"]
EQUITY_ROWS_USD = [
    ("TOTAL", "At 1 January 2021", [63, 2094, 1219, -15, 3361], "spot", "FY2020"),
    ("DATA", "Profit for the financial period (FY2021)", [None, None, 201, None, 201], "avg", "FY2021"),
    ("DATA", "Other comprehensive loss (FY2021)", [None, None, None, -59, -59], "avg", "FY2021"),
    ("TOTAL", "Total comprehensive income for the period (FY2021)", [None, None, 201, -59, 142], "avg", "FY2021"),
    ("DATA", "FX translation effect on equity, net (FY2021)", [None, None, None, None, None], "plug", "FY2021"),
    ("TOTAL", "At 31 December 2021", [63, 2094, 1420, -74, 3503], "spot", "FY2021"),

    ("DATA", "Profit for the financial year (FY2022)", [None, None, 218, None, 218], "avg", "FY2022"),
    ("DATA", "Other comprehensive loss (FY2022)", [None, None, None, -247, -247], "avg", "FY2022"),
    ("TOTAL", "Total comprehensive income for the year (FY2022)", [None, None, 218, -247, -29], "avg", "FY2022"),
    ("DATA", "Share-based payments (FY2022)", [None, None, 1, None, 1], "avg", "FY2022"),
    ("DATA", "Management recharge related to share-based payments (FY2022)", [None, None, -1, None, -1], "avg", "FY2022"),
    ("DATA", "FX translation effect on equity, net (FY2022)", [None, None, None, None, None], "plug", "FY2022"),
    ("TOTAL", "At 31 December 2022", [63, 2094, 1638, -321, 3474], "spot", "FY2022"),

    ("DATA", "Profit for the financial year (FY2023)", [None, None, 506, None, 506], "avg", "FY2023"),
    ("DATA", "Other comprehensive gains (FY2023)", [None, None, None, 38, 38], "avg", "FY2023"),
    ("TOTAL", "Total comprehensive income for the year (FY2023)", [None, None, 506, 38, 544], "avg", "FY2023"),
    ("DATA", "Share-based payments (FY2023)", [None, None, 2, None, 2], "avg", "FY2023"),
    ("DATA", "Management recharge related to share-based payments (FY2023)", [None, None, -2, None, -2], "avg", "FY2023"),
    ("DATA", "FX translation effect on equity, net (FY2023)", [None, None, None, None, None], "plug", "FY2023"),
    ("TOTAL", "At 31 December 2023", [63, 2094, 2144, -283, 4018], "spot", "FY2023"),

    ("DATA", "Profit for the financial year (FY2024)", [None, None, 458, None, 458], "avg", "FY2024"),
    ("DATA", "Other comprehensive income (FY2024)", [None, None, None, 12, 12], "avg", "FY2024"),
    ("TOTAL", "Total comprehensive income for the year (FY2024)", [None, None, 458, 12, 470], "avg", "FY2024"),
    ("DATA", "Share-based payments (FY2024)", [None, None, 2, None, 2], "avg", "FY2024"),
    ("DATA", "Management recharge related to share-based payments (FY2024)", [None, None, -2, None, -2], "avg", "FY2024"),
    ("DATA", "FX translation effect on equity, net (FY2024)", [None, None, None, None, None], "plug", "FY2024"),
    ("TOTAL", "At 31 December 2024", [63, 2094, 2602, -271, 4488], "spot", "FY2024"),

    ("DATA", "Profit for the financial year (FY2025)", [None, None, 488, None, 488], "avg", "FY2025"),
    ("DATA", "Other comprehensive income (FY2025)", [None, None, None, 99, 99], "avg", "FY2025"),
    ("TOTAL", "Total comprehensive income for the year (FY2025)", [None, None, 488, 99, 587], "avg", "FY2025"),
    ("DATA", "Share-based payments (FY2025)", [None, None, 2, None, 2], "avg", "FY2025"),
    ("DATA", "Management recharge related to share-based payments (FY2025)", [None, None, -2, None, -2], "avg", "FY2025"),
    ("DATA", "FX translation effect on equity, net (FY2025)", [None, None, None, None, None], "plug", "FY2025"),
    ("TOTAL", "At 31 December 2025", [63, 2094, 3090, -172, 5075], "spot", "FY2025"),
]
# FX translation plug values (£m) - computed as: closing (spot) - opening (spot, prior year-end) -
# sum of that year's movements (average rate). Independently derived and cross-checked to make each
# year's roll-forward tie exactly - see map.md's Notes for the method. Every year ties EXACTLY in USD
# (zero USD plug needed) - these plugs exist purely because GBP conversion uses 3 different rates.
FX_PLUG_GBP = {
    "FY2021": round((stock(3503, "FY2021") - stock(3361, "FY2020")) - flow(142, "FY2021"), 1),
    "FY2022": round((stock(3474, "FY2022") - stock(3503, "FY2021")) - flow(-29, "FY2022") - flow(1, "FY2022") - flow(-1, "FY2022"), 1),
    "FY2023": round((stock(4018, "FY2023") - stock(3474, "FY2022")) - flow(544, "FY2023") - flow(2, "FY2023") - flow(-2, "FY2023"), 1),
    "FY2024": round((stock(4488, "FY2024") - stock(4018, "FY2023")) - flow(470, "FY2024") - flow(2, "FY2024") - flow(-2, "FY2024"), 1),
    "FY2025": round((stock(5075, "FY2025") - stock(4488, "FY2024")) - flow(587, "FY2025") - flow(2, "FY2025") - flow(-2, "FY2025"), 1),
}

equity_changes_rows = []
for kind, label, vals, rtype, ry in EQUITY_ROWS_USD:
    if rtype == "plug":
        row_vals = [None] * (len(EQUITY_HEADERS) - 1) + [FX_PLUG_GBP[ry]]
    else:
        rate = FX_SPOT[ry] if rtype == "spot" else FX_AVG[ry]
        row_vals = [None if v is None else round(v / rate, 1) for v in vals]
    equity_changes_rows.append((kind, label, row_vals))

EQUITY_SOURCES = (
    STATEMENTS_SOURCES_NOTE + "\n\n"
    "FX METHODOLOGY FOR THIS SHEET: opening balances converted at the prior year-end's spot rate, movement "
    "lines at that year's average rate, closing balances at that year-end's spot rate - the same convention "
    "used throughout this workbook. Converting stocks and flows at 3 different rates within one year means the "
    "roll-forward doesn't tie exactly in GBP even though it ties exactly in USD (independently verified against "
    "each year's own source table before conversion - every year's closing balance ties to both the Balance "
    "Sheet's own Total shareholder's equity and the next year's own opening balance, with zero USD plug needed) "
    "- an explicit 'FX translation effect on equity, net' row (Total column only, computed as the balancing "
    "figure) is included each year, same treatment as this workbook's own Cash Flow Statement's 'Effect of "
    "GBP/USD translation' line."
)

bw.add_equity_changes_sheet(
    title="Goldman Sachs International Bank — Statement of Changes in Equity",
    subtitle="£m, converted from USD - chronological, oldest to newest. See source note for FX methodology.",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQUITY_SOURCES,
    first_col_width=56,
    source_height=340,
)

# ---------------------------------------------------------------
# Sheet: Cash Flow Statement
# ---------------------------------------------------------------
NET_OPERATING_USD = {"FY2025": 275, "FY2024": -5248, "FY2023": 178, "FY2022": 8107, "FY2021": 2354}
NET_INVESTING_USD = {"FY2025": -3950, "FY2024": -2214, "FY2023": 994, "FY2022": 669, "FY2021": -2178}
NET_FINANCING_USD = {"FY2025": -57, "FY2024": -73, "FY2023": -71, "FY2022": -39, "FY2021": -29}
NET_CHANGE_USD = {"FY2025": -3732, "FY2024": -7535, "FY2023": 1101, "FY2022": 8737, "FY2021": 147}
FX_REPORTED_USD = {"FY2025": 200, "FY2024": -420, "FY2023": 376, "FY2022": -183, "FY2021": -328}
OPENING_CASH_USD = {"FY2025": 11977, "FY2024": 19932, "FY2023": 18455, "FY2022": 9901, "FY2021": 10082}
CLOSING_CASH_USD = {"FY2025": 8445, "FY2024": 11977, "FY2023": 19932, "FY2022": 18455, "FY2021": 9901}

net_operating = {y: flow(v, y) for y, v in NET_OPERATING_USD.items()}
net_investing = {y: flow(v, y) for y, v in NET_INVESTING_USD.items()}
net_financing = {y: flow(v, y) for y, v in NET_FINANCING_USD.items()}
net_change = {y: flow(v, y) for y, v in NET_CHANGE_USD.items()}
fx_reported = {y: flow(v, y) for y, v in FX_REPORTED_USD.items()}
opening_cash = {y: stock(v, PREV_YEAR[y]) for y, v in OPENING_CASH_USD.items()}
closing_cash = {y: stock(v, y) for y, v in CLOSING_CASH_USD.items()}

# £ translation plug (see FX_METHOD_NOTE): stocks (opening/closing) and flows
# (everything else) are converted at different rates, so the £ statement needs
# an explicit reconciling line to tie exactly. Computed programmatically as the
# balancing figure, never hardcoded.
fx_plug = {
    y: round(closing_cash[y] - opening_cash[y] - net_change[y] - fx_reported[y], 1)
    for y in YEARS
}

rows = [
    ("SECTION", "Operating activities", {}),
    ("TOTAL", "Net cash from/(used in) operating activities", net_operating),
    ("SECTION", "Investing activities", {}),
    ("TOTAL", "Net cash used in/(from) investing activities", net_investing),
    ("SECTION", "Financing activities", {}),
    ("TOTAL", "Net cash used in financing activities", net_financing),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", net_change),
    ("DATA", "Cash and cash equivalents, beginning balance", opening_cash),
    ("DATA", "Foreign exchange gains/(losses) on cash and cash equivalents (as reported, USD)", fx_reported),
    ("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", fx_plug),
    ("TOTAL", "Cash and cash equivalents, ending balance", closing_cash),
]

bw.add_cash_flow_sheet(
    title="Goldman Sachs International Bank — Statement of Cash Flows",
    subtitle="£m, converted from USD - see source note at bottom for FX methodology and rates used.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=340,
    unit_suffix=" (£m, conv. from USD)",
)

# ---------------------------------------------------------------
# Asset Quality - GSIB's own Note "Loans" gives a product-level Bank
# loans / Mortgage-backed loans split (both already net of impairment)
# plus a single aggregate impairment allowance figure each year - no
# IFRS 9 Stage 1/2/3 table is published for this entity (confirmed by
# reading the Loans note and Note 29 Financial Risk Management in full
# across all 3 Annual Reports; GSIB's balance sheet is dominated by
# collateralised agreements/trading exposures, not a traditional stage-
# split loan book). Gross loans and a coverage ratio are derived from
# the net + allowance figures actually disclosed, not guessed.
# ---------------------------------------------------------------
BANK_LOANS_NET_USD = {"FY2025": 4133, "FY2024": 3077, "FY2023": 3623, "FY2022": 4330, "FY2021": 10644}
MORTGAGE_LOANS_NET_USD = {"FY2025": 4706, "FY2024": 5057, "FY2023": 4452, "FY2022": 4779, "FY2021": 1156}
TOTAL_LOANS_NET_USD = {"FY2025": 8839, "FY2024": 8134, "FY2023": 8075, "FY2022": 9109, "FY2021": 11800}
LOANS_ALLOWANCE_USD = {"FY2025": 45, "FY2024": 64, "FY2023": 108, "FY2022": 108, "FY2021": 51}
TOTAL_LOANS_GROSS_USD = {y: TOTAL_LOANS_NET_USD[y] + LOANS_ALLOWANCE_USD[y] for y in YEARS}
COVERAGE_RATIO = {y: f"{100 * LOANS_ALLOWANCE_USD[y] / TOTAL_LOANS_GROSS_USD[y]:.2f}%" for y in YEARS}

asset_quality_rows_usd = [
    ("DATA", "Bank loans (net of impairment allowance)", BANK_LOANS_NET_USD),
    ("DATA", "Mortgage-backed loans (net of impairment allowance)", MORTGAGE_LOANS_NET_USD),
    ("TOTAL", "Total loans, net of impairment allowance", TOTAL_LOANS_NET_USD),
    ("DATA", "Impairment allowance", LOANS_ALLOWANCE_USD),
    ("TOTAL", "Total loans, gross (derived: net + allowance)", TOTAL_LOANS_GROSS_USD),
]
asset_quality_rows = [
    (kind, label, {y: stock(v, y) for y, v in values.items()})
    for kind, label, values in asset_quality_rows_usd
] + [("DATA", "Impairment allowance / gross loans coverage ratio (derived)", COVERAGE_RATIO)]

ASSET_QUALITY_SOURCES = (
    "Sources - Goldman Sachs International Bank's own Note 'Loans' (product-level net figures and aggregate "
    "impairment allowance), converted from USD to GBP (see FX note below):\n"
    f"FY2025/FY2024: Annual Report for the Financial Year Ended December 31, 2025, p.36 - {AA_2025_URL}\n"
    f"FY2023/FY2022: Annual Report for the Financial Year Ended December 31, 2023, p.36 - {AA_2023_URL}\n"
    f"FY2021: Annual Report for the Financial Period Ended December 31, 2021, p.36 - {AA_2021_URL}\n"
    "No IFRS 9 Stage 1/2/3 or credit-quality-by-rating table is published for this entity in any of the 3 "
    "Annual Reports checked (confirmed by reading the Loans note and Note 'Financial Risk Management and "
    "Capital Management' in full) - GSIB's balance sheet is dominated by collateralised agreements and trading "
    "exposures, not a traditional stage-split loan book (same structural pattern as Credit Suisse International, "
    "built earlier in this rollout). Gross loans and the coverage ratio are derived from the net-of-allowance "
    "product figures plus the aggregate impairment allowance actually disclosed, not from a source table.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_METHOD_NOTE
)
bw.add_asset_quality_sheet(
    title="Goldman Sachs International Bank — Asset Quality",
    subtitle="£m, converted from USD - product-level net loans + aggregate impairment allowance (no IFRS 9 stage table published - see note).",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=90,
    source_height=320,
    unit_suffix=" (£m, conv. from USD)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=56, source_height=260)


# GSIB-specific annual December values from the official GSG UK Q4 Pillar 3
# disclosures. Amounts are reported in USD millions and converted at the
# year-end spot rate used elsewhere in this workbook.
CET1_USD = {"FY2025": 4945, "FY2024": 4336, "FY2023": 3934, "FY2022": 3409, "FY2021": 3412}
TIER1_USD = {"FY2025": 4945, "FY2024": 4336, "FY2023": 3934, "FY2022": 3409, "FY2021": 3412}
TOTAL_CAPITAL_USD = {"FY2025": 5771, "FY2024": 5162, "FY2023": 4760, "FY2022": 4237, "FY2021": 4238}
TOTAL_RWA_USD = {"FY2025": 19936, "FY2024": 17767, "FY2023": 16546, "FY2022": 15674, "FY2021": 17262}
LEVERAGE_EXPOSURE_USD = {"FY2025": 58928, "FY2024": 48965, "FY2023": 53470, "FY2022": 49383, "FY2021": 53247}

CET1_RATIO = {"FY2025": "24.81%", "FY2024": "24.41%", "FY2023": "23.77%", "FY2022": "21.75%", "FY2021": "19.8%"}
TIER1_RATIO = {"FY2025": "24.81%", "FY2024": "24.41%", "FY2023": "23.77%", "FY2022": "21.75%", "FY2021": "19.8%"}
TOTAL_CAPITAL_RATIO = {"FY2025": "28.96%", "FY2024": "29.06%", "FY2023": "28.77%", "FY2022": "27.03%", "FY2021": "24.5%"}
LEVERAGE_RATIO = {"FY2025": "8.39%", "FY2024": "8.86%", "FY2023": "7.36%", "FY2022": "6.87%", "FY2021": "6.4%"}

LCR_HQLA_USD = {"FY2025": 32924, "FY2024": 31716, "FY2023": 28379, "FY2022": 20000, "FY2021": 17889}
LCR_OUTFLOWS_USD = {"FY2025": 27998, "FY2024": 27382, "FY2023": 25109, "FY2022": 19375}
LCR_INFLOWS_USD = {"FY2025": 6754, "FY2024": 7171, "FY2023": 6255, "FY2022": 6867}
LCR_NET_OUTFLOWS_USD = {"FY2025": 21244, "FY2024": 20210, "FY2023": 18855, "FY2022": 12506, "FY2021": 12199}
LCR_RATIO = {"FY2025": "155.57%", "FY2024": "158%", "FY2023": "151%", "FY2022": "161%", "FY2021": "147%"}

NSFR_AVAILABLE_USD = {"FY2025": 52125, "FY2024": 47029, "FY2023": 46071, "FY2022": 45775}
NSFR_REQUIRED_USD = {"FY2025": 40480, "FY2024": 27270, "FY2023": 26631, "FY2022": 30642}
NSFR_RATIO = {"FY2025": "130.01%", "FY2024": "173%", "FY2023": "173%", "FY2022": "151%", "FY2021": "Not publicly disclosed"}

cet1_gbp = {y: stock(v, y) for y, v in CET1_USD.items()}
tier1_gbp = {y: stock(v, y) for y, v in TIER1_USD.items()}
total_capital_gbp = {y: stock(v, y) for y, v in TOTAL_CAPITAL_USD.items()}
total_rwa_gbp = {y: stock(v, y) for y, v in TOTAL_RWA_USD.items()}
leverage_exposure_gbp = {y: stock(v, y) for y, v in LEVERAGE_EXPOSURE_USD.items()}

NO_AT1_NOTE = (
    "The GSIB columns report equal CET1 and Tier 1 capital in each annual observation; no separate Additional Tier 1 "
    "capital is shown for GSIB in the annual key-metrics tables."
)

metric("CET1 Capital", "£m (conv. from USD)", [("Common Equity Tier 1 (CET1) capital", cet1_gbp)], note=NO_AT1_NOTE)
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 (CET1) ratio", CET1_RATIO)])
metric("Tier 1 Capital", "£m (conv. from USD)", [("Tier 1 capital", tier1_gbp)], note=NO_AT1_NOTE)
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", TIER1_RATIO)])
metric("Total Capital", "£m (conv. from USD)", [("Total capital", total_capital_gbp)])
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", TOTAL_CAPITAL_RATIO)])
metric("Total RWAs", "£m (conv. from USD)", [("Total risk-weighted exposure amount", total_rwa_gbp)])

# ---------------------------------------------------------------
# RWA Breakdown - GSIB's own entity-level RWA-by-category table (UK OV1
# template) from the official GSG UK Q4 Pillar 3 disclosures. Each
# year's GSIB Total ties exactly to the Total RWAs metric sheet above.
# FY2021's document uses slightly different row numbering/labels to
# FY2022-2025 (an older table version, "Table 8" vs "Table 5") and has
# no "Amounts below the thresholds for deduction" line at all - left
# blank for FY2021 rather than guessed, not force-matched to later years.
# ---------------------------------------------------------------
RWA_CREDIT_RISK_USD = {"FY2025": 13774, "FY2024": 12897, "FY2023": 12312, "FY2022": 11869, "FY2021": 11675}
RWA_CCR_USD = {"FY2025": 958, "FY2024": 841, "FY2023": 874, "FY2022": 494, "FY2021": 1028}
RWA_SETTLEMENT_USD = {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 6}
RWA_SECURITISATION_USD = {"FY2025": 456, "FY2024": 390, "FY2023": 434, "FY2022": 415, "FY2021": 1207}
RWA_MARKET_USD = {"FY2025": 3308, "FY2024": 2396, "FY2023": 1899, "FY2022": 2058, "FY2021": 2521}
RWA_OPERATIONAL_USD = {"FY2025": 1440, "FY2024": 1243, "FY2023": 1027, "FY2022": 838, "FY2021": 825}
RWA_BELOW_THRESHOLD_USD = {"FY2025": 156, "FY2024": 253, "FY2023": 270, "FY2022": 0}

rwa_breakdown_rows_usd = [
    ("DATA", "Credit risk (excluding CCR)", RWA_CREDIT_RISK_USD),
    ("DATA", "Counterparty credit risk (CCR)", RWA_CCR_USD),
    ("DATA", "Settlement risk", RWA_SETTLEMENT_USD),
    ("DATA", "Securitisation exposures in the non-trading/banking book", RWA_SECURITISATION_USD),
    ("DATA", "Market risk (position, FX and commodities)", RWA_MARKET_USD),
    ("DATA", "Operational risk", RWA_OPERATIONAL_USD),
    ("DATA", "Amounts below the thresholds for deduction (250% risk weight)", RWA_BELOW_THRESHOLD_USD),
    ("TOTAL", "Total RWAs", TOTAL_RWA_USD),
]
rwa_breakdown_rows = [
    (kind, label, {y: stock(v, y) for y, v in values.items()})
    for kind, label, values in rwa_breakdown_rows_usd
]
RWA_BREAKDOWN_SOURCES = (
    "Sources - GSIB's own RWA-by-category breakdown from the official Goldman Sachs Group UK Limited Q4 Pillar "
    "3 Disclosures (GSIB columns/tables, UK OV1 template), converted from USD to GBP (see FX note below):\n"
    f"FY2025: Table 5 (\"Overview of RWAs\"), GSIB table, p.20 - {P3_2025_URL}\n"
    f"FY2024: Table 5, GSIB table, p.20 - {P3_2024_URL}\n"
    f"FY2023: Table 5, GSIB table, p.20 - {P3_2023_URL}\n"
    f"FY2022: Table 5, GSIB table, p.19 - {P3_2022_URL}\n"
    f"FY2021: Table 8 (\"Overview of RWAs\"), GSIB table, p.20 - {P3_2021_URL}\n"
    "FY2021's document uses an older table version (\"Table 8\" vs \"Table 5\" in later years) with slightly "
    "different row numbering and no \"Amounts below the thresholds for deduction\" line at all - left blank for "
    "FY2021 rather than guessed. Each year's GSIB Total ties exactly to this workbook's Total RWAs metric sheet.\n\n"
    + ENTITY_NOTE + "\n\n" + PILLAR3_NOTE + "\n\n" + FX_METHOD_NOTE
)
bw.add_rwa_breakdown_sheet(
    title="Goldman Sachs International Bank — RWA Breakdown",
    subtitle="£m, converted from USD - GSIB entity-level breakdown (UK OV1 template) - see source note for FX methodology.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=90,
    source_height=320,
    unit_suffix=" (£m, conv. from USD)",
)

metric("Leverage Ratio", "£m (conv. from USD) / %", [
    ("Leverage ratio total exposure measure", leverage_exposure_gbp),
    ("Leverage ratio", LEVERAGE_RATIO),
])
metric("LCR", "£m (conv. from USD) / %", [
    ("Total high-quality liquid assets (HQLA) (weighted value - average)", {y: stock(v, y) for y, v in LCR_HQLA_USD.items()}),
    ("Cash outflows - total weighted value", {**{y: stock(v, y) for y, v in LCR_OUTFLOWS_USD.items()}, "FY2021": "Not publicly disclosed"}),
    ("Cash inflows - total weighted value", {**{y: stock(v, y) for y, v in LCR_INFLOWS_USD.items()}, "FY2021": "Not publicly disclosed"}),
    ("Total net cash outflows (adjusted value)", {y: stock(v, y) for y, v in LCR_NET_OUTFLOWS_USD.items()}),
    ("Liquidity coverage ratio", LCR_RATIO),
], note="FY2021 source reports the GSIB LCR summary as liquidity buffer and total net cash outflows; separate cash-inflow and cash-outflow rows were not reported in that table.")
metric("NSFR", "£m (conv. from USD) / %", [
    ("Total available stable funding", {**{y: stock(v, y) for y, v in NSFR_AVAILABLE_USD.items()}, "FY2021": "Not publicly disclosed"}),
    ("Total required stable funding", {**{y: stock(v, y) for y, v in NSFR_REQUIRED_USD.items()}, "FY2021": "Not publicly disclosed"}),
    ("NSFR ratio", NSFR_RATIO),
], note="The FY2021 Q4 report does not show a GSIB NSFR table; FY2022-FY2025 values are taken from the GSIB columns in Table 1.")
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={"MREL Ratio": "No GSIB-specific numeric MREL value is shown in the reviewed official GSG UK Q4 Pillar 3 disclosures; GSGUK MREL figures are not substituted."},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bs_by_label = {label: values for _, label, values in balance_sheet_rows}
is_by_label = {label: values for _, label, values in income_statement_rows}

OPENING_EQUITY_GBP = {y: stock(v, py) for y, v, py in [
    ("FY2021", 3361, "FY2020"), ("FY2022", 3503, "FY2021"), ("FY2023", 3474, "FY2022"),
    ("FY2024", 4018, "FY2023"), ("FY2025", 4488, "FY2024"),
]}
CLOSING_EQUITY_GBP = {y: stock(v, y) for y, v in [
    ("FY2021", 3503), ("FY2022", 3474), ("FY2023", 4018), ("FY2024", 4488), ("FY2025", 5075),
]}
TOTAL_COMPREHENSIVE_GBP = {y: flow(v, y) for y, v in [
    ("FY2021", 142), ("FY2022", -29), ("FY2023", 544), ("FY2024", 470), ("FY2025", 587),
]}
OTHER_EQUITY_MOVEMENTS_GBP = {
    y: round(CLOSING_EQUITY_GBP[y] - OPENING_EQUITY_GBP[y] - TOTAL_COMPREHENSIVE_GBP[y], 1) for y in YEARS
}

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", bs_by_label["Total assets"]),
        ("Loans", bs_by_label["Loans"]),
        ("Deposits", bs_by_label["Deposits"]),
        ("Total shareholder's equity", bs_by_label["Total shareholder's equity"]),
    ],
    balance_sheet_unit="£m (conv. from USD)",
    income_statement_totals=[
        ("Net revenues", is_by_label["Net revenues"]),
        ("Operating expenses", is_by_label["Operating expenses"]),
        ("Profit for the financial year", is_by_label["Profit for the financial year"]),
    ],
    income_statement_unit="£m (conv. from USD)",
    equity_changes_totals=[
        ("Opening equity", OPENING_EQUITY_GBP),
        ("Total comprehensive income/(loss) for the year", TOTAL_COMPREHENSIVE_GBP),
        ("Other equity movements, net", OTHER_EQUITY_MOVEMENTS_GBP),
        ("Closing equity", CLOSING_EQUITY_GBP),
    ],
    equity_changes_unit="£m (conv. from USD)",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", net_operating),
        ("Net cash used in/(from) investing activities", net_investing),
        ("Net cash used in financing activities", net_financing),
        ("Cash and cash equivalents, ending balance", closing_cash),
    ],
    cash_flow_unit="£m (conv. from USD)",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Tier 1 Ratio", TIER1_RATIO),
        ("Total Capital Ratio", TOTAL_CAPITAL_RATIO),
        ("Leverage Ratio", LEVERAGE_RATIO),
        ("LCR", LCR_RATIO),
        ("NSFR", NSFR_RATIO),
    ],
    note="The official GSG UK Q4 Pillar 3 disclosures provide explicit GSIB entity columns/tables for capital, ratios, "
         "RWA, leverage, LCR and (from FY2022) NSFR. No GSIB-specific numeric MREL value is shown, so MREL remains "
         "unavailable. All USD amounts are converted to GBP using the established FX methodology; percentages are "
         "retained as reported. See each metric sheet for official source URLs and table/page references.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/GOLDMAN SACHS INTERNATIONAL BANK FINANCIALS.xlsx")
