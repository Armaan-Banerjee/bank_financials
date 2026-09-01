import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, calendar year-end
YEAR_LABEL = {y: y for y in YEARS}

# Bank of England GBP/USD rates via poundsterlinglive.com's published archive,
# reusing the exact table already established for Zenith Bank UK (same 31
# December calendar year-end, so identical rate set applies).
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


def flow(usd_m, year):
    """Flow figures (cash flow statement lines) - converted at the year's AVERAGE rate."""
    return round(usd_m / FX_AVG[year], 1)


def stock(usd_m, year):
    """Point-in-time figures (balances, capital, RWA) - converted at that year-end's SPOT rate."""
    return round(usd_m / FX_SPOT[year], 1)


AR_URLS = {
    "FY2025": "https://find-and-update.company-information.service.gov.uk/company/02500199/filing-history/MzUxNDA4Njk0M2FkaXF6a2N4/document?format=pdf&download=0",
    "FY2023": "https://find-and-update.company-information.service.gov.uk/company/02500199/filing-history/MzQxNzkxNzIxNWFkaXF6a2N4/document?format=pdf&download=0",
    "FY2021": "https://find-and-update.company-information.service.gov.uk/company/02500199/filing-history/MzMzMjg3NzIzMGFkaXF6a2N4/document?format=pdf&download=0",
}

ENTITY_NOTE = (
    "Credit Suisse International (CSI, company 02500199, FRN 146702) is the UK derivatives/structured-products "
    "trading entity within the former Credit Suisse group - a DISTINCT legal entity from 'Credit Suisse (UK) "
    "Limited' (the deposit-taking bank, built separately in this same batch). Following Credit Suisse's 2023 "
    "collapse and rescue by UBS Group AG, CSI remains an active, separately-reporting UK entity (registered "
    "office moved to UBS's 5 Broadgate address 2 Jan 2026) but is in an explicit, disclosed CONTROLLED WIND-DOWN: "
    "its own FY2025 KPI table states 'Profitability and Risk Weighted Assets (RWA) are reviewed to ensure a "
    "controlled wind-down in a capital efficient manner.' Total assets collapsed from $244.5bn (FY2021) to "
    "$5.65bn (FY2025) - a 97.7% reduction - as client business was progressively transferred to other UBS Group "
    "entities via Part VII transfers. FY2025 also separately reports a $(397)m pre-tax loss from Discontinued "
    "Operations, on top of continuing operations. All figures are converted from CSI's reporting currency (USD) "
    "to GBP using the Bank of England's published GBP/USD spot rate (point-in-time/balance figures) or average "
    "rate over the fiscal year (flow figures) - see the FX conversion methodology note below. All %-ratios are "
    "shown exactly as disclosed, not converted (dimensionless)."
)

FX_METHOD_NOTE = (
    "FX conversion: point-in-time figures (cash balances, Tier 1 capital, RWA) converted at the Bank of England "
    "GBP/USD SPOT rate as at each fiscal year-end; flow figures (every cash flow statement line item) converted "
    "at the AVERAGE rate over that fiscal year. Rates used (£1 = $X): 31 Dec 2020 spot 1.3661 (FY2021 opening "
    "cash only); FY2021 spot 1.3521 / average 1.3752; FY2022 spot 1.2097 / average 1.2362; FY2023 spot 1.2732 / "
    "average 1.2439; FY2024 spot 1.2515 / average 1.2782; FY2025 spot 1.3448 / average 1.3193 - same table "
    "already established for Zenith Bank UK (identical 31 December year-end). Converting stocks and flows at "
    "different rates means the statement doesn't tie in GBP by itself - an 'Effect of GBP/USD translation' line "
    "is included, computed programmatically as the balancing figure (never hardcoded), labelled clearly as a "
    "translation artefact with no bearing on CSI's actual results."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Credit Suisse International's own Consolidated Statement of Cash Flows (Group "
    "and Bank basis - identical for this entity in every year checked), converted from USD to GBP (see FX note "
    "below):\n"
    f"FY2025/FY2024: Annual Report for the Year Ended 31 December 2025, p.46 (filed at Companies House "
    f"12 Apr 2026) - {AR_URLS['FY2025']}\n"
    f"FY2023/FY2022: Annual Report for the Year Ended 31 December 2023, p.47 (filed 20 Apr 2024) - "
    f"{AR_URLS['FY2023']}\n"
    f"FY2021: Annual Report for the Year Ended 31 December 2021, p.55 (filed 16 Mar 2022) - {AR_URLS['FY2021']}\n"
    + ENTITY_NOTE + "\n\n" + FX_METHOD_NOTE
)


def p3_sources():
    return (
        "Sources - Credit Suisse International capital/RWA basis: the FY2025 Annual Report's own 'Key "
        "Performance Indicators' table (p.6), which discloses Risk Weighted Assets, Tier 1 capital, and Tier 1 "
        "capital ratio for all 5 years (2021-2025) as at each year-end - "
        f"{AR_URLS['FY2025']}. This report explicitly states 'Pillar 3 disclosures required under the Capital "
        "Requirements Regulation (CRR) can be found separately at http://www.ubs.com' - a standalone CSI Pillar "
        "3 document was not locatable this session (the UBS regulatory-disclosures URL pattern returned 404, "
        "and the session's WebSearch quota was already exhausted by parallel forks) - revisit if this bank is "
        "ever rebuilt. Converted from USD to GBP using the same FX methodology as the Cash Flow Statement sheet "
        "(SPOT rate at each year-end); % ratios shown exactly as disclosed, not converted.\n" + FX_METHOD_NOTE
    )


bw = BankWorkbook(bank_name="Credit Suisse International", years=YEARS, year_label=YEAR_LABEL, header_color="50B633")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
NET_OPERATING_USD = {"FY2025": 7865, "FY2024": 8673, "FY2023": 11387, "FY2022": 21276, "FY2021": -14340}
NET_INVESTING_USD = {"FY2025": 4, "FY2024": 1, "FY2023": -26, "FY2022": -165, "FY2021": -180}
NET_FINANCING_USD = {"FY2025": -9493, "FY2024": -10409, "FY2023": -11749, "FY2022": -18419, "FY2021": 10043}
OPENING_CASH_USD = {"FY2025": 1840, "FY2024": 3596, "FY2023": 3883, "FY2022": 5792, "FY2021": 5792}
OPENING_CASH_RATE_YEAR = {"FY2025": "FY2024", "FY2024": "FY2023", "FY2023": "FY2022", "FY2022": "FY2021", "FY2021": "FY2020"}
CLOSING_CASH_USD = {"FY2025": 357, "FY2024": 1840, "FY2023": 3596, "FY2022": 3883, "FY2021": 5792}

net_operating = {y: flow(v, y) for y, v in NET_OPERATING_USD.items()}
net_investing = {y: flow(v, y) for y, v in NET_INVESTING_USD.items()}
net_financing = {y: flow(v, y) for y, v in NET_FINANCING_USD.items()}
opening_cash = {y: stock(v, OPENING_CASH_RATE_YEAR[y]) for y, v in OPENING_CASH_USD.items()}
closing_cash = {y: stock(v, y) for y, v in CLOSING_CASH_USD.items()}
net_change = {y: round(net_operating[y] + net_investing[y] + net_financing[y], 1) for y in YEARS}
fx_plug = {y: round((closing_cash[y] - opening_cash[y]) - net_change[y], 1) for y in YEARS}

rows = [
    ("SECTION", "Operating activities", {}),
    ("TOTAL", "Net cash generated from/(used in) operating activities", net_operating),
    ("SECTION", "Investing activities", {}),
    ("TOTAL", "Net cash generated from/(used in) investing activities", net_investing),
    ("SECTION", "Financing activities", {}),
    ("TOTAL", "Net cash generated from/(used in) financing activities", net_financing),
    ("TOTAL", "Net change in cash and cash equivalents (before FX translation)", net_change),
    ("DATA", "Effect of GBP/USD translation (see FX methodology note - not a real cash flow)", fx_plug),
    ("DATA", "Cash and cash equivalents at beginning of period", opening_cash),
    ("TOTAL", "Cash and cash equivalents at end of period", closing_cash),
]

bw.add_cash_flow_sheet(
    title="Credit Suisse International — Consolidated Cash Flow Statement",
    subtitle="£m, converted from USD - see source note at bottom for FX methodology and rates used.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=320,
    unit_suffix=" (£m, conv. from USD)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=56, source_height=190)


TIER1_USD = {"FY2025": 3014, "FY2024": 6883, "FY2023": 13889, "FY2022": 15809, "FY2021": 15022}
TIER1_RATIO = {"FY2025": "146.9%", "FY2024": "62.9%", "FY2023": "40.0%", "FY2022": "26.0%", "FY2021": "24.0%"}
RWA_USD = {"FY2025": 2052, "FY2024": 10951, "FY2023": 34698, "FY2022": 60646, "FY2021": 62643}

tier1_gbp = {y: stock(v, y) for y, v in TIER1_USD.items()}
rwa_gbp = {y: stock(v, y) for y, v in RWA_USD.items()}

AT1_NOTE = (
    "CET1 is NOT separately disclosed anywhere in the source - only a combined 'Tier 1 capital' figure and "
    "ratio are given. The Statement of Changes in Equity shows Additional Tier 1 (AT1) instruments of $1,200m "
    "outstanding at 31 Dec 2022 and 31 Dec 2023 only (issued during FY2022, repatriated during FY2024) - so "
    "CET1 = Tier 1 for FY2021/FY2024/FY2025 (confirmed zero AT1 those years), but CET1 < Tier 1 for FY2022/"
    "FY2023 by an unknown regulatory-capital amount (the $1,200m accounting carrying value of the AT1 "
    "instrument itself isn't necessarily identical to its CRR-recognised capital amount) - left blank rather "
    "than guessed for those two years."
)

metric(
    "CET1 Capital", "£m (conv. from USD) - see note",
    [("Common Equity Tier 1 (CET1) capital", {y: tier1_gbp[y] for y in ["FY2025", "FY2024", "FY2021"]})],
    note=AT1_NOTE,
)
metric(
    "CET1 Ratio", "% - see note",
    [("CET1 Ratio", {y: TIER1_RATIO[y] for y in ["FY2025", "FY2024", "FY2021"]})],
    note=AT1_NOTE,
)
metric(
    "Tier 1 Capital", "£m (conv. from USD)",
    [("Tier 1 capital", tier1_gbp)],
)
metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 capital ratio", TIER1_RATIO)],
)
bw.add_not_disclosed_metric_sheets(
    ["Total Capital", "Total Capital Ratio"],
    p3_sources(),
    per_note={
        "Total Capital": "Not publicly disclosed - only Tier 1 capital is given in the source; no Tier 2 "
                          "instrument or Total Capital figure/ratio appears anywhere in the 5 Annual Reports "
                          "reviewed, and the standalone Pillar 3 document (referenced at ubs.com) was not "
                          "locatable this session.",
        "Total Capital Ratio": "Not publicly disclosed - see Total Capital sheet note.",
    },
)
metric(
    "Total RWAs", "£m (conv. from USD)",
    [("Risk Weighted Assets", rwa_gbp)],
)
bw.add_not_disclosed_metric_sheets(
    ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"],
    p3_sources(),
    per_note={m: "Not publicly disclosed in the Annual Report itself. A standalone CSI Pillar 3 document is "
                 "explicitly referenced (at ubs.com) but was not locatable this session (404 on the guessed URL "
                 "pattern; WebSearch quota already exhausted) - revisit if this bank is ever rebuilt."
              for m in ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"]},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash generated from/(used in) operating activities", net_operating),
        ("Net cash generated from/(used in) investing activities", net_investing),
        ("Net cash generated from/(used in) financing activities", net_financing),
        ("Cash and cash equivalents at end of period", closing_cash),
    ],
    cash_flow_unit="£m (conv. from USD)",
    ratios=[
        ("Tier 1 Ratio", TIER1_RATIO),
    ],
    note="CSI is in an explicit, disclosed controlled wind-down following the 2023 Credit Suisse/UBS "
         "combination - total assets fell 97.7% from FY2021 to FY2025. Figures converted from USD to GBP; see "
         "the Cash Flow Statement sheet's source note for the full FX methodology. Figures are duplicated from "
         "the detail sheets for at-a-glance trend viewing; see each sheet's own source citation for the "
         "underlying document/page.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/CREDIT SUISSE INTERNATIONAL FINANCIALS.xlsx")
