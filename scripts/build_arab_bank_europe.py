import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Arab Bank Europe Plc (Companies House / trading name "Europe Arab Bank plc",
# company 05575857, FRN 446951) reports in EUR (its functional currency) - this
# workbook converts every € figure to £ at the established FX methodology (see
# FX_NOTE below). Only FY2021-FY2024 could be sourced (FY2025 Annual Report and
# any Pillar 3 document are unobtainable - see ENTITY_NOTE); ratios are never
# converted.
YEARS = ["FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first

AR2022_URL = (
    "https://web.archive.org/web/20240714135652/"
    "https://www.eabplc.com/downloads/202304_EABAnnualReport_v7_144ppi.pdf"
)
AR2024_URL = (
    "https://web.archive.org/web/20250805183352/"
    "https://www.eabplc.com/downloads/202502_EABAnnualReport_v3.pdf"
)

# ---------------------------------------------------------------
# FX conversion: rates in market convention "£1 = €X" (Bank of England GBP/EUR
# spot reference rate). To convert a € amount to £: gbp = eur / rate.
# Source: Bank of England daily reference rates, via poundsterlinglive.com's
# published archive of the official BoE series
# (https://www.poundsterlinglive.com/bank-of-england-spot/historical-spot-exchange-rates/gbp/gbp-to-eur-<year>).
# "period_end" = spot rate on 31 December each year (or the last trading day
# if 31 Dec fell on a weekend); FY2021's *opening* balance needs 31 Dec 2020's
# rate too, included below. "average" = simple arithmetic mean of the daily
# reference rates across that calendar year.
FX_RATES = {
    "FY2020": {"period_end": 1.1118},  # 31 Dec 2020 only - needed for FY2021's opening cash balance
    "FY2021": {"period_end": 1.1907, "average": 1.1628},
    "FY2022": {"period_end": 1.1277, "average": 1.1717},
    "FY2023": {"period_end": 1.1539, "average": 1.1520},
    "FY2024": {"period_end": 1.2099, "average": 1.1824},
}
PRIOR_YEAR = {"FY2021": "FY2020", "FY2022": "FY2021", "FY2023": "FY2022", "FY2024": "FY2023"}


def gbp_spot(eur_by_year):
    """Convert a {year: €'000} dict to £'000 using that year's OWN period-end spot rate (stocks)."""
    return {y: round(v / FX_RATES[y]["period_end"], 1) for y, v in eur_by_year.items()}


def gbp_spot_prior(eur_by_year):
    """Convert a {year: €'000} dict to £'000 using the PRIOR year's period-end spot rate
    (for opening cash balances, which are last year's closing balance)."""
    return {y: round(v / FX_RATES[PRIOR_YEAR[y]]["period_end"], 1) for y, v in eur_by_year.items()}


def gbp_avg(eur_by_year):
    """Convert a {year: €'000} dict to £'000 using that year's average rate (flows)."""
    return {y: round(v / FX_RATES[y]["average"], 1) for y, v in eur_by_year.items()}


FX_NOTE = (
    "FX CONVERSION NOTE: Arab Bank Europe Plc (trading/registered as \"Europe Arab Bank plc\") reports in Euros "
    "(its functional currency, per its own Annual Report) - this is the first EUR-reporting workbook in this "
    "series. Converted to £ following the same methodology used for this project's earlier USD-reporting banks "
    "(SMBC BI, Zenith, UBA UK, Access Bank UK, Union Bank of India UK): point-in-time/balance figures use the "
    "Bank of England GBP/EUR SPOT rate as at that fiscal year-end (31 December); flow figures (every cash flow "
    "statement line item) use the AVERAGE of the daily spot rates over that calendar year - both from Bank of "
    "England daily reference rates via poundsterlinglive.com's published archive. Rates used (£1 = €X): 31 Dec "
    "2020 spot 1.1118 (FY2021 opening cash only); FY2021 spot 1.1907 / average 1.1628; FY2022 spot 1.1277 / "
    "average 1.1717; FY2023 spot 1.1539 / average 1.1520; FY2024 spot 1.2099 / average 1.1824. All % ratios (CET1/"
    "Total Capital ratios - see ENTITY_NOTE for why this is all that's disclosed) are shown EXACTLY as reported "
    "in EUR and were NOT converted - a ratio is dimensionless and currency-invariant. Because stocks and flows "
    "are converted at different rates (standard practice for translating foreign-currency financial statements), "
    "a programmatically-computed 'Effect of GBP/EUR translation' reconciling line is included so opening + all "
    "flows + this line = closing exactly in £ terms."
)

ENTITY_NOTE = (
    "ENTITY NOTE: Arab Bank Europe Plc, FRN 446951, company 05575857 (incorporated 2005, trades and files "
    "financial statements under the name \"Europe Arab Bank plc\" - the PRA list's word order is reversed vs. "
    "Companies House/FCA register, confirmed as the same entity via FRN and company number match, not a guess). "
    "Wholly-owned subsidiary of Arab Bank plc (Jordan); UNLIKE many single-foreign-parent subsidiaries in this "
    "series, it does NOT take the FRS 101/102 cash-flow-statement exemption - a full Cash Flow Statement is "
    "published every year. eabplc.com's TLS configuration rejects every automated fetch attempted (both direct "
    "and via Wayback-triggered re-crawl), so sourcing relied entirely on Wayback Machine snapshots already in the "
    "archive; only the FY2022 Annual Report (giving FY2021+FY2022) and the FY2024 Annual Report (giving "
    "FY2023+FY2024) were found archived - the FY2021, FY2023, and FY2025 standalone Annual Reports, and every "
    "standalone Pillar 3 document (only a generic 'Pillar3.pdf' was found archived, and that download was itself "
    "truncated/corrupted on every retry attempted), were not obtainable. FY2025 is therefore excluded entirely "
    "(Companies House confirms a FY2025 filing exists, filed 10 May 2026, but no accessible copy was found). "
    "Pillar 3 disclosure is consequently very thin: only two ratios (Capital adequacy/Total Capital ratio, "
    "Common Equity Tier 1 ratio) are ever stated, and only as headline percentages in the Annual Report's own "
    "'Other Key Performance Indicators' table (note 37 does not add any £/€ breakdown - CET1/Total Capital "
    "amounts, RWA, leverage, LCR, NSFR and MREL are not disclosed anywhere in the sourced documents) - the same "
    "narrative-KPI-only pattern seen at AIB Group (UK) and Bank of Ireland (UK). A genuine, undocumented cash "
    "bridge gap exists between FY2022's closing balance (per the FY2022 Annual Report, €158,856k) and FY2023's "
    "opening balance (per the FY2024 Annual Report's own comparative column, €538,633k) - the FY2023 Annual "
    "Report itself, which would show what happened during that year, was not obtainable. The FY2023 column shows "
    "a 'Loss on disposal of subsidiary' (€3,294k) and 'Disposal of subsidiaries' (€25,342k) line item not present "
    "in any other year, consistent with a subsidiary disposal/deconsolidation event during FY2023, but this does "
    "not come close to explaining the full €379,777k gap - left unbridged and flagged rather than silently forced "
    "to reconcile."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Arab Bank Europe Plc's (Europe Arab Bank plc's) own Cash Flow Statement, converted "
    "from EUR to £'000 (see FX conversion note below):\n"
    f"FY2024/FY2023: Europe Arab Bank plc Annual Report and Financial Statements 2024, p.31 (Cash Flow Statement) "
    f"- {AR2024_URL}\n"
    f"FY2022/FY2021: Europe Arab Bank plc Annual Report and Financial Statements 2022, p.30 (Cash Flow Statement) "
    f"- {AR2022_URL}\n"
    "Each pair's own report was used for both its own year and its comparative column. FY2023/FY2024 use a "
    "materially different note structure to FY2021/FY2022 (new lines: trading gains on securities/derivatives, "
    "gain on lease modification, FX adjustments on ECL/ROU, loss on disposal of subsidiary/disposal of "
    "subsidiaries) - a genuine presentation evolution, not a gap; blank cells mark a line item that doesn't apply "
    "to that year's presentation, section TOTALs are unaffected and fully comparable.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE
)


def p3_sources(page):
    return (
        "Sources - Arab Bank Europe Plc's (Europe Arab Bank plc's) own Annual Report, 'Other Key Performance "
        "Indicators' table (% ratios only - see ENTITY_NOTE on the Cash Flow Statement sheet for why no £/€ "
        "breakdown, RWA, leverage, LCR, NSFR, or MREL figure could be sourced):\n"
        f"FY2024/FY2023: Annual Report and Financial Statements 2024, p.{page['FY2024']} - {AR2024_URL}\n"
        f"FY2022/FY2021: Annual Report and Financial Statements 2022, p.{page['FY2022']} - {AR2022_URL}"
    )


bw = BankWorkbook(bank_name="Arab Bank Europe Plc", years=YEARS, header_color="355070")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (raw EUR '000 figures, converted at build time)
# ---------------------------------------------------------------
PROFIT_ADJ = {"FY2024": 19444, "FY2023": 12873, "FY2022": 12416, "FY2021": 402}
DEPRECIATION = {"FY2024": 3228, "FY2023": 2990, "FY2022": 1564, "FY2021": 1361}
IMPAIRMENT_LOSS = {"FY2024": 5378, "FY2023": 4608, "FY2022": 4500, "FY2021": 1567}
LOSS_ON_DISPOSAL_FA = {"FY2022": 0, "FY2021": 1056}
LOSS_ON_DISPOSAL_SUB = {"FY2023": 3294}
FX_LOSS_SUBORDINATED = {"FY2024": 7620, "FY2023": -4128, "FY2022": 7053, "FY2021": 7784}
INTEREST_EXP_LEASE = {"FY2024": 411, "FY2023": 505, "FY2022": 379, "FY2021": 46}
TRADING_GAINS = {"FY2024": -1334, "FY2023": -456}
GAIN_LEASE_MOD = {"FY2023": -398}
FX_ADJ_ECL = {"FY2024": 1757, "FY2023": -2328}
FX_ADJ_ROU = {"FY2024": -340}
OPERATING_ADJ_SUBTOTAL = {"FY2024": 36164, "FY2023": 16960, "FY2022": 25912, "FY2021": 12216}

CHG_LOANS_CUSTOMERS = {"FY2024": -99312, "FY2023": -88176, "FY2022": 76970, "FY2021": -31138}
CHG_LOANS_BANKS = {"FY2022": 23398, "FY2021": 207372}
CHG_FVTPL_DERIVATIVES = {"FY2024": -1689, "FY2023": 14110, "FY2022": -19270, "FY2021": 123184}
CHG_FVOCI = {"FY2022": -42644, "FY2021": -86081}
CHG_AMORTISED_COST_INVESTMENTS = {"FY2022": 47594, "FY2021": -86211}
CHG_OTHER_ASSETS = {"FY2024": -4068, "FY2023": -1829, "FY2022": -2717, "FY2021": -6137}
CHG_ASSETS_SUBTOTAL = {"FY2024": -105069, "FY2023": -75895, "FY2022": 83331, "FY2021": 120989}

CHG_CUSTOMER_DEPOSITS = {"FY2024": 231252, "FY2023": -27011, "FY2022": 86445, "FY2021": 75042}
CHG_FUNDS_FROM_BANKS = {"FY2024": -9181, "FY2023": 98566, "FY2022": -218828, "FY2021": -166377}
CHG_OTHER_LIABILITIES = {"FY2024": -768, "FY2023": 4667, "FY2022": 13392, "FY2021": -159}
CHG_LIABILITIES_SUBTOTAL = {"FY2024": 221302, "FY2023": 76222, "FY2022": -118990, "FY2021": -91494}

TAXES_PAID = {"FY2024": -2289, "FY2023": 0, "FY2022": 0, "FY2021": 0}
INTEREST_PAID_LEASE = {"FY2022": -379, "FY2021": -46}
NET_OPERATING = {"FY2024": 150109, "FY2023": 17287, "FY2022": -10126, "FY2021": 41665}

CHG_FVOCI_INVESTING = {"FY2024": -33386, "FY2023": 27277}
CHG_AMORTISED_COST_INVESTING = {"FY2024": -79759, "FY2023": 21229}
ACQUISITION_PPE = {"FY2024": -3251, "FY2023": -2410, "FY2022": -3848, "FY2021": -1674}
DISPOSAL_SUBSIDIARIES = {"FY2023": 25342}
INVESTMENT_IN_SUBSIDIARIES = {"FY2022": 0, "FY2021": 0}
NET_INVESTING = {"FY2024": -116396, "FY2023": 71438, "FY2022": -3848, "FY2021": -1674}

PAYMENT_LEASE_LIABILITIES = {"FY2024": -1178, "FY2023": -803, "FY2022": -1344, "FY2021": -1335}
NET_FINANCING = {"FY2024": -1178, "FY2023": -803, "FY2022": -1344, "FY2021": -1335}

NET_CHANGE = {"FY2024": 32535, "FY2023": 87922, "FY2022": -15318, "FY2021": 38656}
CASH_BEGIN = {"FY2024": 626555, "FY2023": 538633, "FY2022": 174174, "FY2021": 135518}
CASH_END = {"FY2024": 659090, "FY2023": 626555, "FY2022": 158856, "FY2021": 174174}

cash_begin_gbp = gbp_spot_prior(CASH_BEGIN)
cash_end_gbp = gbp_spot(CASH_END)
net_change_gbp = gbp_avg(NET_CHANGE)
# Reconciling line absorbing the spot-vs-average rate differential exactly (see FX_NOTE).
# NOTE: FY2023's translation line also absorbs the genuine, undocumented €379,777k cash-bridge
# gap described in ENTITY_NOTE (FY2022 closing vs FY2023 opening don't reconcile in EUR either) -
# flagged prominently there rather than silently smoothed over.
GBP_TRANSLATION_EFFECT = {
    y: round(cash_end_gbp[y] - cash_begin_gbp[y] - net_change_gbp[y], 1)
    for y in YEARS
}

rows = [
    ("SECTION", "Reconciliation of profit before tax to net cash flows from operating activities", {}),
    ("DATA", "Profit before tax", gbp_avg(PROFIT_ADJ)),
    ("DATA", "Depreciation", gbp_avg(DEPRECIATION)),
    ("DATA", "Impairment loss expense", gbp_avg(IMPAIRMENT_LOSS)),
    ("DATA", "Loss on disposal/write-off of fixed assets", gbp_avg(LOSS_ON_DISPOSAL_FA)),
    ("DATA", "Loss on disposal of subsidiary", gbp_avg(LOSS_ON_DISPOSAL_SUB)),
    ("DATA", "Net foreign exchange loss/(gain) on subordinated liability", gbp_avg(FX_LOSS_SUBORDINATED)),
    ("DATA", "Interest expense on lease liabilities", gbp_avg(INTEREST_EXP_LEASE)),
    ("DATA", "Trading gains on securities and derivatives", gbp_avg(TRADING_GAINS)),
    ("DATA", "Gain on lease modification", gbp_avg(GAIN_LEASE_MOD)),
    ("DATA", "FX adjustments on expected credit losses", gbp_avg(FX_ADJ_ECL)),
    ("DATA", "FX adjustments on right-of-use assets", gbp_avg(FX_ADJ_ROU)),
    ("TOTAL", "Profit before tax, adjusted for non-cash items - subtotal", gbp_avg(OPERATING_ADJ_SUBTOTAL)),
    ("SECTION", "Decrease/(Increase) in operating and other assets", {}),
    ("DATA", "Loans advanced to customers", gbp_avg(CHG_LOANS_CUSTOMERS)),
    ("DATA", "Loans advanced to banks", gbp_avg(CHG_LOANS_BANKS)),
    ("DATA", "Fair value through profit or loss and derivatives", gbp_avg(CHG_FVTPL_DERIVATIVES)),
    ("DATA", "Fair value through other comprehensive income", gbp_avg(CHG_FVOCI)),
    ("DATA", "Financial investments at amortised cost", gbp_avg(CHG_AMORTISED_COST_INVESTMENTS)),
    ("DATA", "Other assets", gbp_avg(CHG_OTHER_ASSETS)),
    ("TOTAL", "Decrease/(Increase) in operating and other assets - subtotal", gbp_avg(CHG_ASSETS_SUBTOTAL)),
    ("SECTION", "(Decrease)/Increase in operating and other liabilities", {}),
    ("DATA", "Customer deposits", gbp_avg(CHG_CUSTOMER_DEPOSITS)),
    ("DATA", "Funds received from banks", gbp_avg(CHG_FUNDS_FROM_BANKS)),
    ("DATA", "Other liabilities and retirement benefit liabilities", gbp_avg(CHG_OTHER_LIABILITIES)),
    ("TOTAL", "(Decrease)/Increase in operating and other liabilities - subtotal", gbp_avg(CHG_LIABILITIES_SUBTOTAL)),
    ("DATA", "Income taxes paid", gbp_avg(TAXES_PAID)),
    ("DATA", "Interest paid on lease liabilities", gbp_avg(INTEREST_PAID_LEASE)),
    ("TOTAL", "Net cash (outflows)/inflows from operating activities", gbp_avg(NET_OPERATING)),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Fair value through other comprehensive income (investing)", gbp_avg(CHG_FVOCI_INVESTING)),
    ("DATA", "Financial investments at amortised cost (investing)", gbp_avg(CHG_AMORTISED_COST_INVESTING)),
    ("DATA", "Acquisition of property, plant and equipment", gbp_avg(ACQUISITION_PPE)),
    ("DATA", "Disposal of subsidiaries", gbp_avg(DISPOSAL_SUBSIDIARIES)),
    ("DATA", "Investment in subsidiaries", gbp_avg(INVESTMENT_IN_SUBSIDIARIES)),
    ("TOTAL", "Net cash (outflows)/inflows from investing activities", gbp_avg(NET_INVESTING)),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Payment of lease liabilities", gbp_avg(PAYMENT_LEASE_LIABILITIES)),
    ("TOTAL", "Net cash outflows from financing activities", gbp_avg(NET_FINANCING)),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", net_change_gbp),
    ("DATA", "Effect of GBP/EUR translation (£ conversion artefact - see FX note; FY2023 also absorbs an "
             "undocumented cash-bridge gap, see ENTITY_NOTE)", GBP_TRANSLATION_EFFECT),
    ("DATA", "Cash and cash equivalents at 1 January", cash_begin_gbp),
    ("TOTAL", "Cash and cash equivalents at 31 December", cash_end_gbp),
]

bw.add_cash_flow_sheet(
    title="Arab Bank Europe Plc — Cash Flow Statement",
    subtitle="£'000, converted from EUR - see source note at bottom for FX methodology and rates used.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=80,
    source_height=380,
    unit_suffix=" (£'000, conv. from EUR)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets - only two ratios disclosed anywhere (see ENTITY_NOTE)
# ---------------------------------------------------------------
RATIO_PAGES = {"FY2024": "6", "FY2022": "9"}

TOTAL_CAPITAL_RATIO = {"FY2024": "23%", "FY2023": "24%", "FY2022": "23%", "FY2021": "22%"}
CET1_RATIO = {"FY2024": "16%", "FY2023": "17%", "FY2022": "16%", "FY2021": "16%"}


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, f"Entity-level basis, {unit}" if unit else "Entity-level basis",
                         rows_data, p3_sources(RATIO_PAGES), note=note,
                         first_col_width=46, source_height=140)


NOT_DISCLOSED_NOTE = (
    "Not disclosed in any of the two sourced Annual Reports (FY2021/FY2022 or FY2023/FY2024) - the Bank's only "
    "capital/liquidity disclosure is the 'Other Key Performance Indicators' table's two headline ratios (Capital "
    "adequacy ratio, Common Equity Tier 1 ratio). No standalone Pillar 3 document was obtainable (see ENTITY_NOTE "
    "on the Cash Flow Statement sheet) and no other figure for this metric appears anywhere in either report."
)

metric("CET1 Capital", None, [("Common Equity Tier 1 (CET1) capital (£'000)", {y: "Not publicly disclosed" for y in YEARS})],
       note=NOT_DISCLOSED_NOTE)

metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 (CET1) ratio", CET1_RATIO)])

metric("Tier 1 Capital", None, [("Tier 1 capital (£'000)", {y: "Not publicly disclosed" for y in YEARS})],
       note=NOT_DISCLOSED_NOTE)

metric("Tier 1 Ratio", None, [("Tier 1 ratio", {y: "Not publicly disclosed" for y in YEARS})],
       note=NOT_DISCLOSED_NOTE + " Note: the KPI table's 'Capital adequacy ratio' is Total Capital, not Tier 1 - "
                                  "not substituted here since that would misrepresent a different metric.")

metric("Total Capital", None, [("Total capital (£'000)", {y: "Not publicly disclosed" for y in YEARS})],
       note=NOT_DISCLOSED_NOTE)

metric("Total Capital Ratio", "% of RWA", [("Capital adequacy (Total Capital) ratio", TOTAL_CAPITAL_RATIO)])

metric("Total RWAs", None, [("Total risk-weighted assets (£'000)", {y: "Not publicly disclosed" for y in YEARS})],
       note=NOT_DISCLOSED_NOTE)

bw.add_not_disclosed_metric_sheets(
    ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"],
    p3_sources(RATIO_PAGES),
    per_note={
        "Leverage Ratio": NOT_DISCLOSED_NOTE,
        "LCR": NOT_DISCLOSED_NOTE,
        "NSFR": NOT_DISCLOSED_NOTE,
        "MREL Ratio": NOT_DISCLOSED_NOTE,
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash (outflows)/inflows from operating activities", gbp_avg(NET_OPERATING)),
        ("Net cash (outflows)/inflows from investing activities", gbp_avg(NET_INVESTING)),
        ("Net cash outflows from financing activities", gbp_avg(NET_FINANCING)),
        ("Cash and cash equivalents at 31 December", cash_end_gbp),
    ],
    cash_flow_unit="£'000 (conv. from EUR)",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Total Capital Ratio", TOTAL_CAPITAL_RATIO),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing. ALL £ figures in this "
         "workbook are converted from Arab Bank Europe Plc's (Europe Arab Bank plc's) native EUR reporting - see "
         "the Cash Flow Statement sheet's source note for the full FX methodology and exact rates used. Ratios "
         "(%) are shown exactly as reported in EUR and were not converted. Only 2 of the usual 6 headline ratios "
         "are plotted here (CET1 Ratio, Total Capital Ratio) - Tier 1 Ratio, Leverage Ratio, LCR and NSFR are not "
         "publicly disclosed for this entity, see the individual Pillar 3 sheets and ENTITY_NOTE for why. FY2025 "
         "is excluded entirely (no accessible Annual Report found - see ENTITY_NOTE).",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/ARAB BANK EUROPE FINANCIALS.xlsx")
