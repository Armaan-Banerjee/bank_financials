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
# ST- rollout (batch ST-012): Balance Sheet, P&L, Statement of Changes in
# Equity, Asset Quality, RWA Breakdown. Sourced from the same 3 Companies
# House filings already cited above (AR2025_URL/AR2024_URL/AR2022_URL), all
# scanned/image-only - transcribed via pdf_tools.py render + visual read.
# Same EUR->£ FX methodology as the Cash Flow Statement (see FX_NOTE):
# balance-sheet/equity snapshots at that period's own spot rate, P&L/
# movement figures at that period's average rate.
# ---------------------------------------------------------------
STATEMENTS_SOURCES = (
    "Sources - Bank Saderat Plc's own Statement of Comprehensive Income / Statement of Financial Position / "
    "Statement of Changes in Equity, converted from EUR to £ (see FX conversion note below):\n"
    f"FY2025/FY2024: Full accounts made up to 31 December 2025, pp.29-31 - {AR2025_URL}\n"
    f"FY2024/FY2023: Full accounts made up to 31 December 2024, pp.27-29 - {AR2024_URL} (FY2024's own primary "
    f"report used per project convention, in preference to the FY2025 report's FY2024 comparative column, which "
    f"reclassifies the Other liabilities/Deferred tax liability lines differently - see PRESENTATION_NOTE)\n"
    f"FY2022/FY2021: Full accounts made up to 31 December 2022, pp.21-23 - {AR2022_URL}\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE
)

PRESENTATION_NOTE = (
    "PRESENTATION NOTE: this Bank's own statement formats changed between the FY2021/22 report and the FY2023-25 "
    "reports. P&L: FY2021/22 has no 'Net operating Income' subtotal (Depreciation and Provisions are both "
    "deducted together, straight from Operating Income, to reach Profit before Taxation) and labels 'Other "
    "operating income' as a positive line, vs. FY2023-25's 'Other operating loss' (negative) plus a separate "
    "'Net operating Income' subtotal before Provisions - both structures are reproduced as disclosed, with the "
    "FY2021/22 'Net operating income' cell left blank rather than back-calculated. Balance Sheet: 'Deferred tax "
    "assets' only appears as its own line FY2024-25 (nil/absent FY2021-23); FY2021-23's own reports show a single "
    "'Deferred Tax Liability' line, which FY2025's own report restructures (for FY2025/24) into two lines, "
    "'Other liabilities and Payables' + 'Accruals and Deferred Income' - FY2024's own primary report (used here, "
    "not FY2025's restated comparative) still uses a single undifferentiated 'Other liabilities' line, so FY2024's "
    "'Accruals and deferred income' cell is left blank rather than split. Both totals are unaffected by these "
    "reclassifications and tie out exactly in every year."
)

# ---------------------------------------------------------------
# Balance Sheet (EUR, raw units - converted at each year's own period-end spot rate)
# ---------------------------------------------------------------
BS_CASH = {"FY2025": 1679132, "FY2024": 1741636, "FY2023": 1707223, "FY2022": 1690155, "FY2021": 1740004}
BS_LOANS_BANKS = {"FY2025": 199786057, "FY2024": 209345595, "FY2023": 196726056, "FY2022": 192267152, "FY2021": 188430847}
BS_LOANS_CUSTOMERS = {"FY2025": 10327206, "FY2024": 1852583, "FY2023": 11906292, "FY2022": 14025951, "FY2021": 17529843}
BS_TANGIBLE_FA = {"FY2025": 11905141, "FY2024": 12045264, "FY2023": 12198950, "FY2022": 12345892, "FY2021": 12304894}
BS_INTANGIBLE_FA = {"FY2025": 174875, "FY2024": 261390, "FY2023": 342715, "FY2022": 431434, "FY2021": 621177}
BS_OTHER_ASSETS = {"FY2025": 638242, "FY2024": 668048, "FY2023": 36508, "FY2022": 418946, "FY2021": 303728}
BS_DEFERRED_TAX_ASSET = {"FY2025": 62654, "FY2024": 59638}
BS_PREPAYMENTS = {"FY2025": 1462160, "FY2024": 1096657, "FY2023": 1079507, "FY2022": 1100167, "FY2021": 1070309}
BS_TOTAL_ASSETS = {"FY2025": 226035467, "FY2024": 227070811, "FY2023": 223997250, "FY2022": 222279687, "FY2021": 221900802}

BS_DEPOSITS_BANKS = {"FY2025": 22179542, "FY2024": 23734019, "FY2023": 23195849, "FY2022": 23197516, "FY2021": 23349246}
BS_CUSTOMER_ACCOUNTS = {"FY2025": 3331704, "FY2024": 3535622, "FY2023": 3409112, "FY2022": 3468029, "FY2021": 3452199}
BS_DEFERRED_TAX_LIAB = {"FY2023": 23426, "FY2022": 63649, "FY2021": 37764}
BS_OTHER_LIABILITIES = {"FY2025": 1017433, "FY2024": 3710072, "FY2023": 2899488, "FY2022": 2329932, "FY2021": 2463658}
BS_ACCRUALS_DEFERRED_INCOME = {"FY2025": 3239462}
BS_TOTAL_LIABILITIES = {"FY2025": 29768141, "FY2024": 30979713, "FY2023": 29527874, "FY2022": 29059126, "FY2021": 29302867}

BS_SHARE_CAPITAL = {y: 183219924 for y in YEARS}
BS_GEN_BANKING_RESERVE = {y: 6000000 for y in YEARS}
BS_RETAINED_EARNINGS = {"FY2025": 7047402, "FY2024": 6871174, "FY2023": 5249451, "FY2022": 4000637, "FY2021": 3378011}
BS_TOTAL_EQUITY = {"FY2025": 196267326, "FY2024": 196091098, "FY2023": 194469375, "FY2022": 193220561, "FY2021": 192597935}

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", gbp_m_spot(BS_CASH)),
    ("DATA", "Loans and advances to banks", gbp_m_spot(BS_LOANS_BANKS)),
    ("DATA", "Loans and advances to customers", gbp_m_spot(BS_LOANS_CUSTOMERS)),
    ("DATA", "Tangible fixed assets", gbp_m_spot(BS_TANGIBLE_FA)),
    ("DATA", "Intangible fixed assets", gbp_m_spot(BS_INTANGIBLE_FA)),
    ("DATA", "Other assets", gbp_m_spot(BS_OTHER_ASSETS)),
    ("DATA", "Deferred tax assets", gbp_m_spot(BS_DEFERRED_TAX_ASSET)),
    ("DATA", "Prepayments and accrued income", gbp_m_spot(BS_PREPAYMENTS)),
    ("TOTAL", "Total assets", gbp_m_spot(BS_TOTAL_ASSETS)),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", gbp_m_spot(BS_DEPOSITS_BANKS)),
    ("DATA", "Customer accounts", gbp_m_spot(BS_CUSTOMER_ACCOUNTS)),
    ("DATA", "Deferred tax liability", gbp_m_spot(BS_DEFERRED_TAX_LIAB)),
    ("DATA", "Other liabilities (and payables)", gbp_m_spot(BS_OTHER_LIABILITIES)),
    ("DATA", "Accruals and deferred income", gbp_m_spot(BS_ACCRUALS_DEFERRED_INCOME)),
    ("TOTAL", "Total liabilities", gbp_m_spot(BS_TOTAL_LIABILITIES)),
    ("SECTION", "Shareholders' funds", {}),
    ("DATA", "Called up share capital", gbp_m_spot(BS_SHARE_CAPITAL)),
    ("DATA", "General banking risk reserve", gbp_m_spot(BS_GEN_BANKING_RESERVE)),
    ("DATA", "Retained earnings", gbp_m_spot(BS_RETAINED_EARNINGS)),
    ("TOTAL", "Total equity (Shareholders' funds)", gbp_m_spot(BS_TOTAL_EQUITY)),
    ("TOTAL", "Total liabilities and equity", gbp_m_spot({y: BS_TOTAL_LIABILITIES[y] + BS_TOTAL_EQUITY[y] for y in YEARS})),
]

bw.add_balance_sheet_sheet(
    title="Bank Saderat Plc — Statement of Financial Position",
    subtitle="£m, converted from EUR - see source note at bottom for FX methodology and rates used.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + PRESENTATION_NOTE,
    first_col_width=60,
    source_height=460,
    unit_suffix=" (£m, conv. from EUR)",
)

# ---------------------------------------------------------------
# Profit & Loss (EUR, raw units - flow figures converted at each year's average rate)
# ---------------------------------------------------------------
IS_INTEREST_INCOME = {"FY2025": 4570218, "FY2024": 6733396, "FY2023": 5505485, "FY2022": 4752833, "FY2021": 5150072}
IS_INTEREST_EXPENSE = {"FY2025": -55745, "FY2024": -61203, "FY2023": -39920, "FY2022": -33454, "FY2021": -31616}
IS_NET_INTEREST_INCOME = {"FY2025": 4514473, "FY2024": 6672193, "FY2023": 5465565, "FY2022": 4719379, "FY2021": 5118456}
IS_FEES_RECEIVABLE = {"FY2025": 32106, "FY2024": 20243, "FY2023": 65058, "FY2022": 20526, "FY2021": 19749}
IS_OTHER_OPERATING = {"FY2025": -84557, "FY2024": -50385, "FY2023": -148108, "FY2022": 65380, "FY2021": 57771}
IS_OPERATING_INCOME = {"FY2025": 4462023, "FY2024": 6642051, "FY2023": 5382515, "FY2022": 4805285, "FY2021": 5195976}
IS_ADMIN_EXPENSES = {"FY2025": -3098500, "FY2024": -3329844, "FY2023": -3175665, "FY2022": -3238959, "FY2021": -3752083}
IS_DEPRECIATION = {"FY2025": -228391, "FY2024": -235012, "FY2023": -235661, "FY2022": -224464, "FY2021": -158258}
IS_NET_OPERATING_INCOME = {"FY2025": 1135132, "FY2024": 3077195, "FY2023": 1971189}
IS_PROVISIONS = {"FY2025": -965654, "FY2024": -786269, "FY2023": -308056, "FY2022": -542170, "FY2021": -308848}
IS_PROFIT_BEFORE_TAX = {"FY2025": 169477, "FY2024": 2290926, "FY2023": 1663133, "FY2022": 799692, "FY2021": 976787}
IS_TAX = {"FY2025": 6751, "FY2024": -669203, "FY2023": -414320, "FY2022": -177066, "FY2021": -172589}
IS_PROFIT_AFTER_TAX = {"FY2025": 176228, "FY2024": 1621723, "FY2023": 1248813, "FY2022": 622626, "FY2021": 804198}
IS_OCI = {y: 0 for y in YEARS}
IS_TOTAL_COMPREHENSIVE = dict(IS_PROFIT_AFTER_TAX)

income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable and similar income", gbp_m_avg(IS_INTEREST_INCOME)),
    ("DATA", "Interest payable and similar expenses", gbp_m_avg(IS_INTEREST_EXPENSE)),
    ("TOTAL", "Net interest income", gbp_m_avg(IS_NET_INTEREST_INCOME)),
    ("DATA", "Fees and commissions receivable", gbp_m_avg(IS_FEES_RECEIVABLE)),
    ("DATA", "Other operating income/(loss)", gbp_m_avg(IS_OTHER_OPERATING)),
    ("TOTAL", "Operating income/profit", gbp_m_avg(IS_OPERATING_INCOME)),
    ("DATA", "Administrative expenses", gbp_m_avg(IS_ADMIN_EXPENSES)),
    ("DATA", "Depreciation & amortisation", gbp_m_avg(IS_DEPRECIATION)),
    ("TOTAL", "Net operating income", gbp_m_avg(IS_NET_OPERATING_INCOME)),
    ("DATA", "Provisions for the year", gbp_m_avg(IS_PROVISIONS)),
    ("TOTAL", "Profit before taxation", gbp_m_avg(IS_PROFIT_BEFORE_TAX)),
    ("DATA", "Tax on profit", gbp_m_avg(IS_TAX)),
    ("TOTAL", "Profit after taxation", gbp_m_avg(IS_PROFIT_AFTER_TAX)),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Other comprehensive income", gbp_m_avg(IS_OCI)),
    ("TOTAL", "Total comprehensive income for the year", gbp_m_avg(IS_TOTAL_COMPREHENSIVE)),
]

bw.add_income_statement_sheet(
    title="Bank Saderat Plc — Statement of Comprehensive Income",
    subtitle="£m, converted from EUR - see source note at bottom for FX methodology and rates used.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + PRESENTATION_NOTE,
    first_col_width=60,
    source_height=460,
    unit_suffix=" (£m, conv. from EUR)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity (chronological; each snapshot converted at
# its own period-end spot rate, each year's profit at that year's average
# rate - an "FX translation effect" plug row absorbs the resulting gap per
# component column, same treatment as the Cash Flow Statement's GBP_TRANSLATION_EFFECT
# line and as used for Bank Mandiri Europe (ST-011) - since Called up share
# capital/General banking risk reserve are EUR-constant but get revalued at
# each period's own spot rate, most of the "effect" is this revaluation, not
# a real economic movement.
# ---------------------------------------------------------------
EQUITY_EUR = [
    ("2021-01-01", "opening", {"cap": 183219924, "reserve": 6000000, "retained": 2573813, "total": 191793737}),
    ("FY2021", "profit", {"cap": 0, "reserve": 0, "retained": 804198, "total": 804198}),
    ("2021-12-31", "closing", {"cap": 183219924, "reserve": 6000000, "retained": 3378011, "total": 192597935}),
    ("FY2022", "profit", {"cap": 0, "reserve": 0, "retained": 622626, "total": 622626}),
    ("2022-12-31", "closing", {"cap": 183219924, "reserve": 6000000, "retained": 4000637, "total": 193220561}),
    ("FY2023", "profit", {"cap": 0, "reserve": 0, "retained": 1248813, "total": 1248813}),
    ("2023-12-31", "closing", {"cap": 183219924, "reserve": 6000000, "retained": 5249451, "total": 194469375}),
    ("FY2024", "profit", {"cap": 0, "reserve": 0, "retained": 1621723, "total": 1621723}),
    ("2024-12-31", "closing", {"cap": 183219924, "reserve": 6000000, "retained": 6871174, "total": 196091098}),
    ("FY2025", "profit", {"cap": 0, "reserve": 0, "retained": 176228, "total": 176228}),
    ("2025-12-31", "closing", {"cap": 183219924, "reserve": 6000000, "retained": 7047402, "total": 196267326}),
]
# Note: the FY2024 report's own comparative opening balance at 1 Jan 2023/
# 31 Dec 2022 (194,469,375 becomes the 2023-12-31 closing above) matches; a
# tiny €1 rounding gap exists between the FY2022 report's own 31 Dec 2022
# closing total (193,220,561) and other internal sums - immaterial, not
# adjusted.

SNAPSHOT_SPOT = {
    "2021-01-01": FX_RATES["FY2020"]["period_end"],
    "2021-12-31": FX_RATES["FY2021"]["period_end"],
    "2022-12-31": FX_RATES["FY2022"]["period_end"],
    "2023-12-31": FX_RATES["FY2023"]["period_end"],
    "2024-12-31": FX_RATES["FY2024"]["period_end"],
    "2025-12-31": FX_RATES["FY2025"]["period_end"],
}


def _to_gbp_m(eur, rate):
    return round(eur / rate / 1_000_000, 2)


equity_gbp = {}
for key, kind, comps in EQUITY_EUR:
    if kind == "profit":
        rate = FX_RATES[key]["average"]
    else:
        rate = SNAPSHOT_SPOT[key]
    equity_gbp[key] = {c: _to_gbp_m(v, rate) for c, v in comps.items()}

equity_changes_rows = []
prior_key = None
for key, kind, comps in EQUITY_EUR:
    g = equity_gbp[key]
    if kind == "opening":
        label = "At 1 January 2021"
        equity_changes_rows.append(("TOTAL", label, (g["cap"], g["reserve"], g["retained"], g["total"])))
    elif kind == "profit":
        label = f"Profit and total comprehensive income for the year ({key})"
        equity_changes_rows.append(("DATA", label, (None, None, g["retained"], g["total"])))
    else:  # closing
        # Find the immediately preceding opening/closing and profit rows to compute the plug.
        idx = [k for k, *_ in EQUITY_EUR].index(key)
        opening_key = EQUITY_EUR[idx - 2][0]
        profit_key = EQUITY_EUR[idx - 1][0]
        plug = {
            c: round(g[c] - equity_gbp[opening_key][c] - equity_gbp[profit_key].get(c, 0), 2)
            for c in ("cap", "reserve", "retained", "total")
        }
        if any(abs(v) > 0.005 for v in plug.values()):
            equity_changes_rows.append((
                "DATA", "FX translation effect on equity, net",
                (plug["cap"], plug["reserve"], plug["retained"], plug["total"]),
            ))
        label = f"At {key[8:10]} {['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][int(key[5:7])-1]}. {key[:4]}"
        equity_changes_rows.append(("TOTAL", label, (g["cap"], g["reserve"], g["retained"], g["total"])))
    prior_key = key

bw.add_equity_changes_sheet(
    title="Bank Saderat Plc — Statement of Changes in Equity",
    subtitle="£m, converted from EUR - see source note at bottom for FX methodology; an 'FX translation effect' "
              "row is included since equity components that are EUR-constant still shift in £ terms because each "
              "snapshot is converted at that period's own spot rate.",
    headers=["Called up share capital", "General banking risk reserve", "Retained earnings", "Total"],
    rows=equity_changes_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + PRESENTATION_NOTE + "\n\nNote: 'Total' £m figures are converted "
                 "independently from the raw EUR total (not summed from the rounded component columns), so a "
                 "~£0.01m rounding gap vs. summing the displayed component cells, or vs. the Balance Sheet's own "
                 "Total equity row, is expected and immaterial.",
    first_col_width=52,
    source_height=460,
)

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
# Asset Quality: loans and advances to customers, gross/net + allowance
# (the Bank's own Note 10/11 - no by-product or IFRS 9 stage split is
# disclosed at all, so remaining-maturity is used as the loan-book breakdown
# instead, per the "use what's actually disclosed" convention). Impaired/
# not-impaired split only located for FY2021/FY2022 (Note 15.7-15.8 in the
# AR2022 report) - FY2023-25 don't carry an equivalent note in the sections
# reviewed, so those cells are left blank rather than estimated.
# ---------------------------------------------------------------
AQ_MATURITY_3M = {"FY2025": 11406356, "FY2024": 10681209, "FY2023": 17026526, "FY2022": 14496029, "FY2021": 13523362}
AQ_MATURITY_1Y = {"FY2025": 0, "FY2024": 896129, "FY2023": 2623410, "FY2022": 2324700, "FY2021": 2324701}
AQ_MATURITY_5Y = {"FY2025": 10657868, "FY2024": 298710, "FY2023": 1493549, "FY2022": 5545530, "FY2021": 9597512}
AQ_GROSS_LOANS = {y: AQ_MATURITY_3M[y] + AQ_MATURITY_1Y[y] + AQ_MATURITY_5Y[y] for y in YEARS}
AQ_ALLOWANCE = {"FY2025": 11737018, "FY2024": 10023465, "FY2023": 9237194, "FY2022": 7917439, "FY2021": 7375271}
AQ_INTEREST_SUSPENSE = {"FY2022": 422869, "FY2021": 540461}
AQ_NET_LOANS = {y: AQ_GROSS_LOANS[y] - AQ_ALLOWANCE[y] - AQ_INTEREST_SUSPENSE.get(y, 0) for y in YEARS}
AQ_IMPAIRED = {"FY2022": 7866000, "FY2021": 7645000}
AQ_NOT_IMPAIRED = {"FY2022": 6160000, "FY2021": 9885000}  # exposure total minus impaired (per Note 15.8, €000s->€)

AQ_COVERAGE_RATIO = {y: f"{AQ_ALLOWANCE[y] / AQ_GROSS_LOANS[y] * 100:.1f}%" for y in YEARS}
AQ_IMPAIRED_RATIO = {y: f"{AQ_IMPAIRED[y] / (AQ_IMPAIRED[y] + AQ_NOT_IMPAIRED[y]) * 100:.1f}%" for y in AQ_IMPAIRED}

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, by remaining maturity", {}),
    ("DATA", "Three months or less", gbp_m_spot(AQ_MATURITY_3M)),
    ("DATA", "One year or less but over three months", gbp_m_spot(AQ_MATURITY_1Y)),
    ("DATA", "Five years or less but over one year", gbp_m_spot(AQ_MATURITY_5Y)),
    ("TOTAL", "Gross loans and advances to customers", gbp_m_spot(AQ_GROSS_LOANS)),
    ("DATA", "Less: allowance for losses", gbp_m_spot({y: -AQ_ALLOWANCE[y] for y in YEARS})),
    ("DATA", "Less: interest suspended", gbp_m_spot({y: -v for y, v in AQ_INTEREST_SUSPENSE.items()})),
    ("TOTAL", "Net loans and advances to customers", gbp_m_spot(AQ_NET_LOANS)),
    ("SECTION", "Impaired / not impaired split (FY2021-FY2022 only - not disclosed at this granularity FY2023-25)", {}),
    ("DATA", "Impaired exposure", gbp_m_spot(AQ_IMPAIRED)),
    ("DATA", "Neither past due nor impaired / past due not impaired", gbp_m_spot(AQ_NOT_IMPAIRED)),
    ("DATA", "Allowance coverage ratio (allowance / gross loans)", AQ_COVERAGE_RATIO),
    ("DATA", "Impaired exposure ratio (impaired / total exposure)", AQ_IMPAIRED_RATIO),
]

bw.add_asset_quality_sheet(
    title="Bank Saderat Plc — Asset Quality / Credit Risk Disclosures",
    subtitle="£m, converted from EUR. The Bank does not disclose an IFRS 9 stage or by-product loan-book split - "
              "remaining-maturity (its own actual disclosure) is used as the breakdown instead.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - Bank Saderat Plc's own Note 10 (Loans and advances to customers) and Note 15.7/15.8 (impaired "
        "loans and advances, FY2021/FY2022 only):\n"
        f"FY2025/FY2024: Full accounts made up to 31 December 2025, p.48 - {AR2025_URL}\n"
        f"FY2024/FY2023: Full accounts made up to 31 December 2024, p.44 - {AR2024_URL}\n"
        f"FY2022/FY2021: Full accounts made up to 31 December 2022, pp.30,37 - {AR2022_URL}\n\n"
        + ENTITY_NOTE + "\n\n" + FX_NOTE
    ),
    first_col_width=70,
    source_height=380,
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

bw.add_rwa_breakdown_sheet(
    title="Bank Saderat Plc — RWA Breakdown",
    subtitle="Not publicly disclosed - see note below.",
    rows=[("DATA", "RWA by risk category (UK OV1)", {y: "Not publicly disclosed" for y in YEARS})],
    sources_text=p3_sources(RATIO_PAGES) + "\n\n" + NOT_DISCLOSED_NOTE,
    first_col_width=54,
    source_height=200,
)

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
OPENING_KEY = {"FY2021": "2021-01-01", "FY2022": "2021-12-31", "FY2023": "2022-12-31", "FY2024": "2023-12-31", "FY2025": "2024-12-31"}
CLOSING_KEY = {"FY2021": "2021-12-31", "FY2022": "2022-12-31", "FY2023": "2023-12-31", "FY2024": "2024-12-31", "FY2025": "2025-12-31"}
eq_opening = {y: equity_gbp[OPENING_KEY[y]]["total"] for y in YEARS}
eq_tci = {y: equity_gbp[y]["total"] for y in YEARS}
eq_closing = {y: equity_gbp[CLOSING_KEY[y]]["total"] for y in YEARS}
eq_other = {y: round(eq_closing[y] - eq_opening[y] - eq_tci[y], 2) for y in YEARS}

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", gbp_m_spot(BS_TOTAL_ASSETS)),
        ("Loans and advances to customers", gbp_m_spot(BS_LOANS_CUSTOMERS)),
        ("Customer accounts", gbp_m_spot(BS_CUSTOMER_ACCOUNTS)),
        ("Total equity", gbp_m_spot(BS_TOTAL_EQUITY)),
    ],
    balance_sheet_unit="£m (conv. from EUR)",
    income_statement_totals=[
        ("Net interest income", gbp_m_avg(IS_NET_INTEREST_INCOME)),
        ("Administrative expenses", gbp_m_avg(IS_ADMIN_EXPENSES)),
        ("Profit/(loss) after taxation", gbp_m_avg(IS_PROFIT_AFTER_TAX)),
    ],
    income_statement_unit="£m (conv. from EUR)",
    equity_changes_totals=[
        ("Opening equity", eq_opening),
        ("Total comprehensive income for the year", eq_tci),
        ("Other movements, net (FX translation effect)", eq_other),
        ("Closing equity", eq_closing),
    ],
    equity_changes_unit="£m (conv. from EUR)",
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
