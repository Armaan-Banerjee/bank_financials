import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Bank Saderat Plc (company 01126618, FRN 204488) - UK subsidiary of Bank
# Saderat Iran. Reports in EUR (its functional currency, confirmed on the
# Statement of Changes in Equity/Cash Flows) - converted to £ using the same
# methodology as Arab Bank Europe Plc (the project's other EUR-reporting
# bank), reusing that bank's FX rate table extended by one year for FY2025.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first

AR2024_URL = (
    "https://find-and-update.company-information.service.gov.uk/company/01126618/"
    "filing-history/MzQ2MzQ4MDU2OWFkaXF6a2N4/document?format=pdf&download=0"
)
AR2022_URL = (
    "https://find-and-update.company-information.service.gov.uk/company/01126618/"
    "filing-history/MzM3Nzc2OTA1NGFkaXF6a2N4/document?format=pdf&download=0"
)
AR2025_URL = (
    "https://find-and-update.company-information.service.gov.uk/company/01126618/"
    "filing-history/MzUyNzI0MjU2MGFkaXF6a2N4/document?format=pdf&download=0"
)

# ---------------------------------------------------------------
# FX conversion: rates in market convention "£1 = €X" (Bank of England GBP/EUR
# spot reference rate). Reuses the FY2020-FY2024 rates already established for
# Arab Bank Europe Plc (same official BoE series, same 31 December year-end),
# extended with FY2025 (spot confirmed via poundsterlinglive.com's BoE
# archive; average is a rough mid-month-sample estimate, full daily series
# wasn't practical to extract - flagged as approximate in FX_NOTE).
FX_RATES = {
    "FY2020": {"period_end": 1.1118},
    "FY2021": {"period_end": 1.1907, "average": 1.1628},
    "FY2022": {"period_end": 1.1277, "average": 1.1717},
    "FY2023": {"period_end": 1.1539, "average": 1.1520},
    "FY2024": {"period_end": 1.2099, "average": 1.1824},
    "FY2025": {"period_end": 1.1454, "average": 1.168},
}
PRIOR_YEAR = {"FY2021": "FY2020", "FY2022": "FY2021", "FY2023": "FY2022", "FY2024": "FY2023", "FY2025": "FY2024"}


def gbp_m_spot(eur_by_year):
    """Convert a {year: €} dict to £m using that year's OWN period-end spot rate (stocks)."""
    return {y: round(v / FX_RATES[y]["period_end"] / 1_000_000, 2) for y, v in eur_by_year.items()}


def gbp_m_spot_prior(eur_by_year):
    """Convert a {year: €} dict to £m using the PRIOR year's period-end spot rate
    (for opening cash balances, which are last year's closing balance)."""
    return {y: round(v / FX_RATES[PRIOR_YEAR[y]]["period_end"] / 1_000_000, 2) for y, v in eur_by_year.items()}


def gbp_m_avg(eur_by_year):
    """Convert a {year: €} dict to £m using that year's average rate (flows)."""
    return {y: round(v / FX_RATES[y]["average"] / 1_000_000, 2) for y, v in eur_by_year.items()}


FX_NOTE = (
    "FX CONVERSION NOTE: Bank Saderat Plc reports in Euros (its functional currency) - the second EUR-reporting "
    "workbook in this series after Arab Bank Europe Plc, using the identical methodology and (for FY2020-FY2024) "
    "the identical Bank of England GBP/EUR reference rates: point-in-time/balance figures use the SPOT rate as at "
    "that fiscal year-end (31 December); flow figures use the AVERAGE rate over that calendar year. Rates used "
    "(£1 = €X): 31 Dec 2020 spot 1.1118 (FY2021 opening cash only); FY2021 spot 1.1907 / avg 1.1628; FY2022 spot "
    "1.1277 / avg 1.1717; FY2023 spot 1.1539 / avg 1.1520; FY2024 spot 1.2099 / avg 1.1824; FY2025 spot 1.1454 "
    "(confirmed, poundsterlinglive.com BoE archive) / avg ~1.168 (approximate - a mid-month sample average, not "
    "a full daily-series mean, since extracting the complete 2025 daily series wasn't practical; flagged here "
    "rather than presented as precise). All % ratios (Capital Cover, LCR - see ENTITY_NOTE) are shown EXACTLY as "
    "reported in EUR and were NOT converted - a ratio is dimensionless and currency-invariant. Because stocks and "
    "flows are converted at different rates, a programmatically-computed 'Effect of GBP/EUR translation' "
    "reconciling line is included so opening + all flows + this line = closing exactly in £ terms."
)

ENTITY_NOTE = (
    "ENTITY NOTE: Bank Saderat Plc, FRN 204488, company 01126618 (incorporated 1973 as Iran Overseas Investment "
    "Bank, renamed 2002), wholly-owned UK subsidiary of Bank Saderat Iran. The Bank operated under EU sanctions "
    "until October 2016 and has faced correspondent-banking/SWIFT access difficulties since a second round of "
    "OFAC sanctions in 2018, but remains an active, going-concern entity throughout the period covered here - "
    "Companies House confirms Active status with accounts filed every year through FY2025 (filed 25 Jun 2026), "
    "and does NOT take the FRS 101/102 cash-flow-statement exemption (a full Statement of Cash Flows is published "
    "every year). IMPORTANT: the UK imposed 'snapback' sanctions affecting the Bank's business activities from "
    "29 September 2025 (mid-way through FY2025) - the Bank's own FY2025 Annual Report states the relevant "
    "authorities have granted licenses permitting it to continue essential operations and ordinary-course "
    "payments, so this is NOT treated as a going-concern/skip situation (contrast VTB Capital plc elsewhere in "
    "this project, which IS in insolvency administration), but it materially affects FY2025's figures - operating "
    "cash flow swings to a large outflow (see Cash Flow Statement) and interest income fell sharply. Flagged "
    "prominently here since it's a genuinely new, still-unfolding development, not a historical footnote.\n\n"
    "CAPITAL RATIO CAVEAT: the Bank's own disclosures give a 'Capital Cover' percentage every year (used below as "
    "the CET1/Tier 1/Total Capital Ratio series, since capital = CET1 = Tier 1 = Total Capital per the Bank's own "
    "description - no AT1/Tier 2 instruments) - but this does NOT appear to be a conventional CET1/RWA-style ratio "
    "as disclosed by every other bank in this project. The FY2025 Annual Report separately states 'the CET1 "
    "capital ratio to the total risk exposure is 88.70%' - a very different figure from the 331% 'Capital Cover' "
    "value for the same year, implying 'Capital Cover' uses a different denominator (plausibly capital versus the "
    "Bank's Total Capital Requirement including a Pillar 2A add-on, not capital versus RWA). The 88.70% figure is "
    "only disclosed for FY2025 (no equivalent figure found for FY2021-FY2024), so 'Capital Cover' was used "
    "throughout for a consistent 5-year series - readers should treat this bank's ratio row as NOT directly "
    "comparable to other banks' CET1/Tier1/Total Capital Ratio sheets in this project. Total RWAs is left 'Not "
    "publicly disclosed' rather than calculated from either figure, since which one (if either) 'Capital Cover' "
    "actually divides into isn't confirmed.\n\n"
    "LIQUIDITY RATIO CAVEAT: the Bank's LCR disclosure is genuinely inconsistent across filing vintages - each "
    "year's OWN report is used as the primary figure below (project convention), but later reports' comparative "
    "columns for the SAME years show materially different values: FY2022 368% (own report) vs. 328% (per the "
    "FY2024 report's comparative); FY2023 334% (own report) vs. 375% (per the FY2025 report's comparative); "
    "FY2024 331% (own report) vs. 323% (per the FY2025 report's comparative). This is a larger and more persistent "
    "cross-vintage discrepancy than the single-instance restatements seen elsewhere in this project (e.g. Bank of "
    "Ceylon, BNY Mellon) - plausibly reflecting a genuinely unstable LCR calculation methodology at this bank "
    "(new core banking/regulatory reporting software went live during this period) rather than a one-off "
    "correction. The FY2024/FY2025 reports also separately break LCR out by currency (GBP: 582-674%; EUR: "
    "158-212%) - the 'All currencies' figure is used here as the single comparable metric, consistent with every "
    "other bank in this project."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Bank Saderat Plc's own Statement of Cash Flows, converted from EUR to £m (see FX "
    "conversion note below):\n"
    f"FY2025/FY2024 (2024 comparative confirmed unchanged): Full accounts made up to 31 December 2025, p.32 "
    f"(Statement of Cash Flows) - {AR2025_URL}\n"
    f"FY2024/FY2023: Full accounts made up to 31 December 2024, p.30 (Statement of Cash Flows) - {AR2024_URL}\n"
    f"FY2022/FY2021: Full accounts made up to 31 December 2022, p.24 (Statement of Cash Flows) - {AR2022_URL}. "
    f"Note: this filing states 'The 2021 cash flow stands amended' - the FY2021 column here is that amended "
    f"figure, not the original FY2021 filing's figure (not separately sourced).\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE
)


def p3_sources(page):
    return (
        "Sources - Bank Saderat Plc's own Annual Report, Strategic Report 'Key performance indicators' / 'Share "
        "capital and regulatory capital base' sections (see ENTITY_NOTE on the Cash Flow Statement sheet for "
        "important caveats on how these ratios are defined and their cross-vintage consistency):\n"
        f"FY2025: Full accounts made up to 31 December 2025, p.{page['FY2025']} - {AR2025_URL}\n"
        f"FY2024/FY2023: Full accounts made up to 31 December 2024, p.{page['FY2024']} - {AR2024_URL}\n"
        f"FY2022/FY2021: Full accounts made up to 31 December 2022, p.{page['FY2022']} - {AR2022_URL}"
    )


bw = BankWorkbook(bank_name="Bank Saderat Plc", years=YEARS, header_color="2F4538")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (raw EUR figures, converted to £m at build time)
# ---------------------------------------------------------------
CASH_FROM_OPERATIONS = {"FY2025": -70787294, "FY2024": 25102237, "FY2023": 30246049, "FY2022": 27068225, "FY2021": 668390}
TAXATION_PAID = {"FY2025": -164923, "FY2024": -450593, "FY2023": -126529, "FY2022": -180691, "FY2021": -59573}
NET_OPERATING = {"FY2025": -70952217, "FY2024": 24651644, "FY2023": 30119520, "FY2022": 26887534, "FY2021": 608817}

# Investing: explicitly nil (stated as "-") FY2023-FY2025 per the Bank's own presentation; a genuine
# purchase of tangible fixed assets appears only in FY2021/FY2022.
PURCHASE_FIXED_ASSETS = {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": -175719, "FY2021": -621432}
NET_INVESTING = {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": -175719, "FY2021": -621432}

NET_CHANGE = {"FY2025": -70952217, "FY2024": 24651644, "FY2023": 30119520, "FY2022": 26711816, "FY2021": -12615}
CASH_BEGIN = {"FY2025": 204773258, "FY2024": 180121614, "FY2023": 150002094, "FY2022": 123290279, "FY2021": 123302894}
CASH_END = {"FY2025": 133821041, "FY2024": 204773258, "FY2023": 180121614, "FY2022": 150002094, "FY2021": 123290279}

cash_begin_gbp = gbp_m_spot_prior(CASH_BEGIN)
cash_end_gbp = gbp_m_spot(CASH_END)
net_change_gbp = gbp_m_avg(NET_CHANGE)
# Reconciling line absorbing the spot-vs-average rate differential exactly (see FX_NOTE).
GBP_TRANSLATION_EFFECT = {
    y: round(cash_end_gbp[y] - cash_begin_gbp[y] - net_change_gbp[y], 2)
    for y in YEARS
}

rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Cash flow from operations (note 22)", gbp_m_avg(CASH_FROM_OPERATIONS)),
    ("DATA", "Taxation paid", gbp_m_avg(TAXATION_PAID)),
    ("TOTAL", "Net cash generated from/(used in) operating activities", gbp_m_avg(NET_OPERATING)),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of tangible fixed assets (note 12)", gbp_m_avg(PURCHASE_FIXED_ASSETS)),
    ("TOTAL", "Net cash used in investing activities", gbp_m_avg(NET_INVESTING)),
    ("TOTAL", "Increase/(decrease) in cash and cash equivalents", net_change_gbp),
    ("DATA", "Effect of GBP/EUR translation (£ conversion artefact - see FX note)", GBP_TRANSLATION_EFFECT),
    ("DATA", "Cash and cash equivalents at the beginning of the year", cash_begin_gbp),
    ("TOTAL", "Cash and cash equivalents at year-end", cash_end_gbp),
]

bw.add_cash_flow_sheet(
    title="Bank Saderat Plc — Statement of Cash Flows",
    subtitle="£m, converted from EUR - see source note at bottom for FX methodology and rates used. No "
              "Financing Activities section - none is presented in any of the Bank's own source statements.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=80,
    source_height=420,
    unit_suffix=" (£m, conv. from EUR)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
RATIO_PAGES = {"FY2025": "13-14", "FY2024": "13-14", "FY2022": "9"}

CAPITAL_BASE = {"FY2025": 196228824, "FY2024": 196287187, "FY2023": 194469375, "FY2022": 193220561, "FY2021": 192597935}
CAPITAL_COVER = {"FY2025": "331%", "FY2024": "349%", "FY2023": "325%", "FY2022": "339%", "FY2021": "313%"}
LCR_ALL_CCY = {"FY2025": "477%", "FY2024": "331%", "FY2023": "334%", "FY2022": "368%", "FY2021": "376%"}

capital_base_gbp = gbp_m_spot(CAPITAL_BASE)


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, p3_sources(RATIO_PAGES), note=note, first_col_width=48, source_height=260)


CAPITAL_COVER_NOTE = (
    "This is the Bank's own 'Capital Cover' metric (disclosed every year as a chart in the Strategic Report), "
    "used here for CET1/Tier 1/Total Capital Ratio since capital = CET1 = Tier 1 = Total Capital per the Bank's "
    "own description (no AT1/Tier 2 instruments). See the CAPITAL RATIO CAVEAT in the Cash Flow Statement sheet's "
    "ENTITY_NOTE - this figure does not appear to be a conventional CET1/RWA ratio like other banks in this "
    "project (the FY2025 report separately states a genuine CET1-to-total-risk-exposure ratio of 88.70%, only "
    "disclosed for that one year)."
)

NOT_DISCLOSED_NOTE = (
    "Not disclosed anywhere in the Bank's own Annual Reports - no standalone Pillar 3 document was found "
    "(correspondent-banking/website constraints, see ENTITY_NOTE), and the Strategic Report's capital/liquidity "
    "disclosure is limited to the 'Capital Cover' and Liquidity Coverage Ratio charts plus the CET1 capital base "
    "figure (see the other Pillar 3 sheets)."
)

metric("CET1 Capital", "£m (Bank's disclosed capital base, consisting of CET1 Capital)",
       [("Common Equity Tier 1 (CET1) capital", capital_base_gbp)])

metric("CET1 Ratio", "%", [("Capital Cover", CAPITAL_COVER)], note=CAPITAL_COVER_NOTE)

metric("Tier 1 Capital", "£m (= CET1 Capital; no AT1 instruments)", [("Tier 1 capital", capital_base_gbp)])

metric("Tier 1 Ratio", "%", [("Capital Cover", CAPITAL_COVER)], note=CAPITAL_COVER_NOTE)

metric("Total Capital", "£m (= CET1 Capital; no Tier 2 instruments)", [("Total capital", capital_base_gbp)])

metric("Total Capital Ratio", "%", [("Capital Cover", CAPITAL_COVER)], note=CAPITAL_COVER_NOTE)

metric("Total RWAs", None, [("Total risk-weighted assets", {y: "Not publicly disclosed" for y in YEARS})],
       note=NOT_DISCLOSED_NOTE + " Not calculated from Capital Cover either, since which denominator that "
                                  "metric actually uses isn't confirmed - see CAPITAL RATIO CAVEAT.")

bw.add_not_disclosed_metric_sheets(
    ["Leverage Ratio"], p3_sources(RATIO_PAGES), per_note={"Leverage Ratio": NOT_DISCLOSED_NOTE},
)

metric("LCR", "%, all currencies", [("Liquidity Coverage Ratio", LCR_ALL_CCY)],
       note="See LIQUIDITY RATIO CAVEAT in the Cash Flow Statement sheet's ENTITY_NOTE - this bank's LCR series "
            "shows real cross-vintage inconsistency; each year's own originally-reported figure is used here.")

bw.add_not_disclosed_metric_sheets(
    ["NSFR", "MREL Ratio"],
    p3_sources(RATIO_PAGES),
    per_note={m: NOT_DISCLOSED_NOTE for m in ["NSFR", "MREL Ratio"]},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash generated from/(used in) operating activities", gbp_m_avg(NET_OPERATING)),
        ("Net cash used in investing activities", gbp_m_avg(NET_INVESTING)),
        ("Cash and cash equivalents at year-end", cash_end_gbp),
    ],
    cash_flow_unit="£m (conv. from EUR)",
    ratios=[
        ("CET1 Ratio", CAPITAL_COVER),
        ("Tier 1 Ratio", CAPITAL_COVER),
        ("Total Capital Ratio", CAPITAL_COVER),
        ("LCR", LCR_ALL_CCY),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing. ALL £ figures in this "
         "workbook are converted from Bank Saderat Plc's native EUR reporting - see the Cash Flow Statement "
         "sheet's source note for the full FX methodology and rates used. Ratios (%) are shown exactly as "
         "reported in EUR and were not converted. IMPORTANT: the CET1/Tier1/Total Capital Ratio row uses the "
         "Bank's own 'Capital Cover' metric, which is NOT confirmed to be a conventional CET1/RWA-style ratio - "
         "see the CAPITAL RATIO CAVEAT on the Cash Flow Statement sheet before comparing this bank's ratios to "
         "others in this project. FY2025 was also materially affected by UK 'snapback' sanctions from 29 "
         "September 2025 - see ENTITY_NOTE. Leverage Ratio, NSFR and MREL Ratio are not publicly disclosed for "
         "this entity and are omitted from this chart.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BANK SADERAT FINANCIALS.xlsx")
