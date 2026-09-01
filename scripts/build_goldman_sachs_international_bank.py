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

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
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
bw.add_overview_sheet(
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
