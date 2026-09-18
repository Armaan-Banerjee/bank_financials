import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Bank Saderat Plc (company 01126618, FRN 204488) - UK subsidiary of Bank
# Saderat Iran. Reports in EUR (its functional currency, confirmed on the
# Statement of Changes in Equity/Cash Flows) - converted to £ using the same
# methodology as Arab Bank Europe Plc (the project's other EUR-reporting
# bank), reusing that bank's FX rate table extended by one year for FY2025.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019"]  # most recent first

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
AR2020_URL = (
    "https://find-and-update.company-information.service.gov.uk/company/01126618/"
    "filing-history/MzI5OTI5MzU3NGFkaXF6a2N4/document?format=pdf&download=0"
)
AR2019_URL = (
    "https://find-and-update.company-information.service.gov.uk/company/01126618/"
    "filing-history/MzI2MzQzNDY1MmFkaXF6a2N4/document?format=pdf&download=0"
)

# Standalone Pillar 3 disclosures. The Bank DOES publish these - a "Basel
# Disclosures Archive" page on its own live site carries every edition from 2010
# to 2023. Earlier passes on this bank recorded "no standalone Pillar 3 document
# was found"; that was wrong, and the archive page is linked from the site's own
# top-level navigation. Newest edition is 2023: FY2024 and FY2025 have not been
# published (checked 2026-09-15, see P3_ARCHIVE_NOTE).
P3_ARCHIVE_URL = "https://www.saderat-plc.com/Basel_Disclosures.htm"
P3_2023_URL = "https://www.saderat-plc.com/Reports/Pillar%203%20Disclosures%202023.pdf"
P3_2022_URL = "https://www.saderat-plc.com/Reports/Pillar%203%20%20%20disclosures%202022.pdf"
P3_2021_URL = "https://www.saderat-plc.com/Reports/Pillar%203%20disclosures%202021.pdf"
P3_2020_URL = "https://www.saderat-plc.com/Reports/Pillar%203%20%20%20disclosures%202020%20ver%207.pdf"
P3_2019_URL = "https://www.saderat-plc.com/Reports/Basel%20III%20Pillar%203%20Disclosures%202019.pdf"

# ---------------------------------------------------------------
# FX conversion: rates in market convention "£1 = €X" (Bank of England GBP/EUR
# spot reference rate). Reuses the FY2020-FY2024 rates already established for
# Arab Bank Europe Plc (same official BoE series, same 31 December year-end),
# extended with FY2025 (spot confirmed via poundsterlinglive.com's BoE
# archive; average is a rough mid-month-sample estimate, full daily series
# wasn't practical to extract - flagged as approximate in FX_NOTE).
FX_RATES = {
    "FY2018": {"period_end": 1.1133},
    "FY2019": {"period_end": 1.1757, "average": 1.1405},
    "FY2020": {"period_end": 1.1118},
    "FY2021": {"period_end": 1.1907, "average": 1.1628},
    "FY2022": {"period_end": 1.1277, "average": 1.1717},
    "FY2023": {"period_end": 1.1539, "average": 1.1520},
    "FY2024": {"period_end": 1.2099, "average": 1.1824},
    "FY2025": {"period_end": 1.1454, "average": 1.168},
}
FX_RATES["FY2020"]["average"] = 1.1250
PRIOR_YEAR = {"FY2019": "FY2018", "FY2020": "FY2019", "FY2021": "FY2020", "FY2022": "FY2021", "FY2023": "FY2022", "FY2024": "FY2023", "FY2025": "FY2024"}


def gbp_m_spot(eur_by_year):
    """Convert a {year: €} dict to £m using that year's OWN period-end spot rate (stocks)."""
    return {y: (None if v is None else round(v / FX_RATES[y]["period_end"] / 1_000_000, 2)) for y, v in eur_by_year.items()}


def gbp_m_spot_prior(eur_by_year):
    """Convert a {year: €} dict to £m using the PRIOR year's period-end spot rate
    (for opening cash balances, which are last year's closing balance)."""
    return {y: (None if v is None else round(v / FX_RATES[PRIOR_YEAR[y]]["period_end"] / 1_000_000, 2)) for y, v in eur_by_year.items()}


def gbp_m_avg(eur_by_year):
    """Convert a {year: €} dict to £m using that year's average rate (flows)."""
    return {y: (None if v is None else round(v / FX_RATES[y]["average"] / 1_000_000, 2)) for y, v in eur_by_year.items()}


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
    "CAPITAL RATIO CAVEAT (SUBSTANTIALLY RESOLVED 2026-09-15 - this bank DOES publish Pillar 3 disclosures): the "
    "Bank's own Annual Reports give a 'Capital Cover' percentage every year, and earlier passes used it as the "
    "CET1/Tier 1/Total Capital Ratio series while flagging that it is not a conventional CET1/RWA ratio. That "
    "flag was right and the reason is now confirmed: 'Capital Cover' measures capital against the Bank's total "
    "capital REQUIREMENT (Pillar 1 plus a Pillar 2A add-on), not against the risk exposure amount, which is why "
    "it reads in the 300s where the CRR ratio reads in the 80s-90s for the same year. The genuine CRR ratios and "
    "the risk exposure amounts they divide into are now carried for FY2019-FY2023, transcribed from the Bank's "
    "own standalone Pillar 3 disclosures, which are published on its live website and had simply not been found "
    "by earlier passes (see the detailed correction note on the Total RWAs and RWA Breakdown sheets). The ratio "
    "sheets therefore now carry TWO labelled rows - the CRR ratio, comparable with every other bank in this "
    "project, and the Bank's own Capital Cover metric, retained because it is the only measure available for all "
    "seven years. FY2024 has neither a Pillar 3 edition nor a disclosed risk exposure amount, so its CRR row is "
    "blank; FY2025's CRR ratio comes from the Annual Report's own narrative. No RWA is back-solved from a ratio "
    "in any year. One caveat specific to FY2019: the 2019 edition prints a CET1 ratio (81.0%) different from its "
    "Tier 1 and total capital ratios (84.4%) despite nil Tier 2, so those sheets' FY2019 cells differ from each "
    "other - as printed, and explained in full on each ratio sheet's own note.\n\n"
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
    f"FY2022/FY2021: Full accounts made up to 31 December 2022, p.24 (Statement of Cash Flows) - {AR2022_URL}\n"
    f"FY2020/FY2019: FY2020 accounts p.20 and FY2019 accounts p.18 - {AR2020_URL} / {AR2019_URL}. "
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
        f"FY2022/FY2021: Full accounts made up to 31 December 2022, p.{page['FY2022']} - {AR2022_URL}\n"
        f"FY2020/FY2019: own Capital management Note 15, FY2020 p.35 and FY2019 p.35 - {AR2020_URL} / {AR2019_URL}\n"
        f"FY2019-FY2023 CRR capital ratios and risk exposure amounts: each year's own standalone Pillar 3 "
        f"disclosure, from the Bank's Basel Disclosures Archive - {P3_ARCHIVE_URL} (see the detailed source note "
        f"on the Total RWAs and RWA Breakdown sheets, including the FY2019 CET1-ratio caveat)"
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
    f"FY2022/FY2021: Full accounts made up to 31 December 2022, pp.21-23 - {AR2022_URL}\n"
    f"FY2020: Full accounts made up to 31 December 2020, pp.17-19 - {AR2020_URL}\n"
    f"FY2019: Full accounts made up to 31 December 2019, pp.15-17 - {AR2019_URL}\n\n"
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
BS_CASH = {"FY2025": 1679132, "FY2024": 1741636, "FY2023": 1707223, "FY2022": 1690155, "FY2021": 1740004, "FY2020": 1616050, "FY2019": 1724643}
BS_LOANS_BANKS = {"FY2025": 199786057, "FY2024": 209345595, "FY2023": 196726056, "FY2022": 192267152, "FY2021": 188430847, "FY2020": 186486070, "FY2019": 187385290}
BS_LOANS_CUSTOMERS = {"FY2025": 10327206, "FY2024": 1852583, "FY2023": 11906292, "FY2022": 14025951, "FY2021": 17529843, "FY2020": 23194499, "FY2019": 23622973}
BS_TANGIBLE_FA = {"FY2025": 11905141, "FY2024": 12045264, "FY2023": 12198950, "FY2022": 12345892, "FY2021": 12304894, "FY2020": 12381659, "FY2019": 12478397}
BS_INTANGIBLE_FA = {"FY2025": 174875, "FY2024": 261390, "FY2023": 342715, "FY2022": 431434, "FY2021": 621177}
BS_OTHER_ASSETS = {"FY2025": 638242, "FY2024": 668048, "FY2023": 36508, "FY2022": 418946, "FY2021": 303728, "FY2020": 124729, "FY2019": 33565}
BS_INTANGIBLE_FA.update({"FY2020": 0, "FY2019": 0})
BS_DEFERRED_TAX_ASSET = {"FY2025": 62654, "FY2024": 59638, "FY2020": 63119, "FY2019": 62180}
BS_PREPAYMENTS = {"FY2025": 1462160, "FY2024": 1096657, "FY2023": 1079507, "FY2022": 1100167, "FY2021": 1070309, "FY2020": 275634, "FY2019": 218557}
BS_TOTAL_ASSETS = {"FY2025": 226035467, "FY2024": 227070811, "FY2023": 223997250, "FY2022": 222279687, "FY2021": 221900802, "FY2020": 224516310, "FY2019": 225525605}

BS_DEPOSITS_BANKS = {"FY2025": 22179542, "FY2024": 23734019, "FY2023": 23195849, "FY2022": 23197516, "FY2021": 23349246, "FY2020": 27673592, "FY2019": 29185063}
BS_CUSTOMER_ACCOUNTS = {"FY2025": 3331704, "FY2024": 3535622, "FY2023": 3409112, "FY2022": 3468029, "FY2021": 3452199, "FY2020": 3271385, "FY2019": 3505884}
BS_DEFERRED_TAX_LIAB = {"FY2023": 23426, "FY2022": 63649, "FY2021": 37764}
BS_OTHER_LIABILITIES = {"FY2025": 1017433, "FY2024": 3710072, "FY2023": 2899488, "FY2022": 2329932, "FY2021": 2463658, "FY2020": 1777596, "FY2019": 1732767}
BS_ACCRUALS_DEFERRED_INCOME = {"FY2025": 3239462}
BS_TOTAL_LIABILITIES = {"FY2025": 29768141, "FY2024": 30979713, "FY2023": 29527874, "FY2022": 29059126, "FY2021": 29302867, "FY2020": 32722574, "FY2019": 34423714}

BS_SHARE_CAPITAL = {y: 183219924 for y in YEARS}
BS_GEN_BANKING_RESERVE = {y: 6000000 for y in YEARS}
BS_RETAINED_EARNINGS = {"FY2025": 7047402, "FY2024": 6871174, "FY2023": 5249451, "FY2022": 4000637, "FY2021": 3378011, "FY2020": 2573812, "FY2019": 1881967}
BS_TOTAL_EQUITY = {"FY2025": 196267326, "FY2024": 196091098, "FY2023": 194469375, "FY2022": 193220561, "FY2021": 192597935, "FY2020": 191793736, "FY2019": 191101891}

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
IS_INTEREST_INCOME = {"FY2025": 4570218, "FY2024": 6733396, "FY2023": 5505485, "FY2022": 4752833, "FY2021": 5150072, "FY2020": 4691851, "FY2019": 4201434}
IS_INTEREST_EXPENSE = {"FY2025": -55745, "FY2024": -61203, "FY2023": -39920, "FY2022": -33454, "FY2021": -31616, "FY2020": -41527, "FY2019": -61451}
IS_NET_INTEREST_INCOME = {"FY2025": 4514473, "FY2024": 6672193, "FY2023": 5465565, "FY2022": 4719379, "FY2021": 5118456, "FY2020": 4650324, "FY2019": 4139983}
IS_FEES_RECEIVABLE = {"FY2025": 32106, "FY2024": 20243, "FY2023": 65058, "FY2022": 20526, "FY2021": 19749, "FY2020": 7535, "FY2019": 58382}
IS_OTHER_OPERATING = {"FY2025": -84557, "FY2024": -50385, "FY2023": -148108, "FY2022": 65380, "FY2021": 57771, "FY2020": -55427, "FY2019": 14167}
IS_OPERATING_INCOME = {"FY2025": 4462023, "FY2024": 6642051, "FY2023": 5382515, "FY2022": 4805285, "FY2021": 5195976, "FY2020": 4596479, "FY2019": 4208448}
IS_ADMIN_EXPENSES = {"FY2025": -3098500, "FY2024": -3329844, "FY2023": -3175665, "FY2022": -3238959, "FY2021": -3752083, "FY2020": -3013972, "FY2019": -3653179}
IS_DEPRECIATION = {"FY2025": -228391, "FY2024": -235012, "FY2023": -235661, "FY2022": -224464, "FY2021": -158258, "FY2020": -107851, "FY2019": -108286}
IS_NET_OPERATING_INCOME = {"FY2025": 1135132, "FY2024": 3077195, "FY2023": 1971189}
IS_NET_OPERATING_INCOME.update({"FY2020": None, "FY2019": None})
IS_PROVISIONS = {"FY2025": -965654, "FY2024": -786269, "FY2023": -308056, "FY2022": -542170, "FY2021": -308848, "FY2020": -596849, "FY2019": 35897}
IS_PROFIT_BEFORE_TAX = {"FY2025": 169477, "FY2024": 2290926, "FY2023": 1663133, "FY2022": 799692, "FY2021": 976787, "FY2020": 877808, "FY2019": 482880}
IS_TAX = {"FY2025": 6751, "FY2024": -669203, "FY2023": -414320, "FY2022": -177066, "FY2021": -172589, "FY2020": -185962, "FY2019": -111853}
IS_PROFIT_AFTER_TAX = {"FY2025": 176228, "FY2024": 1621723, "FY2023": 1248813, "FY2022": 622626, "FY2021": 804198, "FY2020": 691846, "FY2019": 371027}
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
    ("2019-01-01", "opening", {"cap": 183219924, "reserve": 6000000, "retained": 1510940, "total": 190730864}),
    ("FY2019", "profit", {"cap": 0, "reserve": 0, "retained": 371027, "total": 371027}),
    ("2019-12-31", "closing", {"cap": 183219924, "reserve": 6000000, "retained": 1881967, "total": 191101891}),
    ("FY2020", "profit", {"cap": 0, "reserve": 0, "retained": 691846, "total": 691846}),
    ("2020-12-31", "closing", {"cap": 183219924, "reserve": 6000000, "retained": 2573812, "total": 191793736}),
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
    "2019-01-01": FX_RATES["FY2018"]["period_end"] if "FY2018" in FX_RATES else FX_RATES["FY2019"]["period_end"],
    "2019-12-31": FX_RATES["FY2019"]["period_end"],
    "2020-12-31": FX_RATES["FY2020"]["period_end"],
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
CASH_FROM_OPERATIONS = {"FY2025": -70787294, "FY2024": 25102237, "FY2023": 30246049, "FY2022": 27068225, "FY2021": 668390, "FY2020": 45889, "FY2019": 213286}
TAXATION_PAID = {"FY2025": -164923, "FY2024": -450593, "FY2023": -126529, "FY2022": -180691, "FY2021": -59573, "FY2020": -122886, "FY2019": -164458}
NET_OPERATING = {"FY2025": -70952217, "FY2024": 24651644, "FY2023": 30119520, "FY2022": 26887534, "FY2021": 608817, "FY2020": -76997, "FY2019": 48828}

# Investing: explicitly nil (stated as "-") FY2023-FY2025 per the Bank's own presentation; a genuine
# purchase of tangible fixed assets appears only in FY2021/FY2022.
PURCHASE_FIXED_ASSETS = {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": -175719, "FY2021": -621432, "FY2020": -11112, "FY2019": -2056}
NET_INVESTING = {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": -175719, "FY2021": -621432, "FY2020": -11112, "FY2019": -2056}

NET_CHANGE = {"FY2025": -70952217, "FY2024": 24651644, "FY2023": 30119520, "FY2022": 26711816, "FY2021": -12615, "FY2020": -88109, "FY2019": 46772}
CASH_BEGIN = {"FY2025": 204773258, "FY2024": 180121614, "FY2023": 150002094, "FY2022": 123290279, "FY2021": 123302894, "FY2020": 1724643, "FY2019": 1657214}
CASH_END = {"FY2025": 133821041, "FY2024": 204773258, "FY2023": 180121614, "FY2022": 150002094, "FY2021": 123290279, "FY2020": 1616050, "FY2019": 1724643}

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
AQ_MATURITY_3M = {"FY2025": 11406356, "FY2024": 10681209, "FY2023": 17026526, "FY2022": 14496029, "FY2021": 13523362, "FY2020": 16180724, "FY2019": 13278277}
AQ_MATURITY_1Y = {"FY2025": 0, "FY2024": 896129, "FY2023": 2623410, "FY2022": 2324700, "FY2021": 2324701, "FY2020": 3220830, "FY2019": 1792258}
AQ_MATURITY_5Y = {"FY2025": 10657868, "FY2024": 298710, "FY2023": 1493549, "FY2022": 5545530, "FY2021": 9597512, "FY2020": 41558526, "FY2019": 15376776}
AQ_GROSS_LOANS = {y: AQ_MATURITY_3M[y] + AQ_MATURITY_1Y[y] + AQ_MATURITY_5Y[y] for y in YEARS}
AQ_ALLOWANCE = {"FY2025": 11737018, "FY2024": 10023465, "FY2023": 9237194, "FY2022": 7917439, "FY2021": 7375271, "FY2020": 7765581, "FY2019": 6824338}
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
        f"FY2022/FY2021: Full accounts made up to 31 December 2022, pp.30,37 - {AR2022_URL}\n"
        f"FY2020/FY2019: own Notes 9-11, FY2020 pp.25-26 and FY2019 p.24 - {AR2020_URL} / {AR2019_URL}\n\n"
        + ENTITY_NOTE + "\n\n" + FX_NOTE
    ),
    first_col_width=70,
    source_height=380,
    unit_suffix=" (£m, conv. from EUR)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
RATIO_PAGES = {"FY2025": "13-14", "FY2024": "13-14", "FY2022": "9", "FY2020": "35", "FY2019": "35"}

CAPITAL_BASE = {"FY2025": 196228824, "FY2024": 196287187, "FY2023": 194469375, "FY2022": 193220561, "FY2021": 192597935, "FY2020": 191793736, "FY2019": 191101891}
CAPITAL_COVER = {"FY2025": "331%", "FY2024": "349%", "FY2023": "325%", "FY2022": "339%", "FY2021": "313%", "FY2020": "330%", "FY2019": "324%"}
LCR_ALL_CCY = {"FY2025": "477%", "FY2024": "331%", "FY2023": "334%", "FY2022": "368%", "FY2021": "376%"}

# The genuine CRR ratio (own funds / total risk exposure amount), as printed.
# FY2021-FY2023 from each year's own Pillar 3 disclosure, section 4.3 "Capital
# Buffers"; FY2025 from the Annual Report's own narrative. The Bank holds no AT1
# or Tier 2 ("The Bank does not hold any Tier 2 or Tier 3 Capital"), so CET1 =
# Tier 1 = Total Capital and one printed ratio serves all three sheets - the
# FY2021 Pillar 3 states this explicitly by printing all three at 83.57%.
# FY2024 CORRECTED 2026-09-18. This block previously said FY2024 was blank because
# "its Annual Report gives only the Capital Cover chart". That was WRONG, and the
# reason it went unnoticed is instructive: the FY2024 Annual Report is an image-only
# scan (61 pages, 61 characters extractable - one form feed per page and no text
# layer), so every text search of it returns zero and an earlier pass reasonably but
# mistakenly read that zero as "the document does not say it". After OCR the report
# states, in the Strategic Report at PDF p.12 of 60 under "Share capital and
# regulatory capital base" (confirmed by reading a 200 DPI render of that page, not
# by trusting the OCR): "The CET1 capital ratio to the total risk exposure is
# 92.33%." That is the same sentence, in the same section, that already sources
# FY2025's 88.70%. FY2024 is therefore populated on the same basis as FY2025.
# This does NOT give FY2024 a total risk exposure amount - see the Total RWAs sheet.
# FY2019 and FY2020 added 2026-09-15 from the 2019 and 2020 Pillar 3 editions
# on the same archive page (the earlier pass read only the 2021-2023 files).
# FY2020 prints all three ratios at 83.44%, like FY2021-FY2023. FY2019 is the
# one year where the three DIVERGE - see FY2019_RATIO_NOTE - so the three ratio
# sheets take three separate dicts rather than one shared CRR_RATIO.
CRR_RATIO = {"FY2025": "88.70%", "FY2024": "92.33%", "FY2023": "86.62%", "FY2022": "90.31%",
             "FY2021": "83.57%", "FY2020": "83.44%"}
CRR_RATIO_CET1 = dict(CRR_RATIO, **{"FY2019": "81.0%"})
CRR_RATIO_TIER1 = dict(CRR_RATIO, **{"FY2019": "84.4%"})
CRR_RATIO_TOTAL = dict(CRR_RATIO, **{"FY2019": "84.4%"})

# Total risk exposure amount, €'000 as printed in each year's Pillar 3.
# Components foot exactly to the total in all five years.
P3_RWA_CREDIT_EUR = {"FY2023": 214136000, "FY2022": 204055000, "FY2021": 220810000, "FY2020": 220485000, "FY2019": 216933000}
P3_RWA_FX_EUR = {"FY2023": 765000, "FY2022": 748000, "FY2021": 722000, "FY2020": 655000, "FY2019": 1088000}
P3_RWA_OP_EUR = {"FY2023": 9615000, "FY2022": 9124000, "FY2021": 8934000, "FY2020": 8715000, "FY2019": 8288000}
P3_RWA_TOTAL_EUR = {"FY2023": 224516000, "FY2022": 213927000, "FY2021": 230466000, "FY2020": 229855000, "FY2019": 226309000}

capital_base_gbp = gbp_m_spot(CAPITAL_BASE)


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, p3_sources(RATIO_PAGES), note=note, first_col_width=48, source_height=260)


CAPITAL_COVER_NOTE = (
    "TWO ROWS, TWO DIFFERENT MEASURES - read the labels before comparing.\n"
    "ROW 1 is the genuine CRR ratio (own funds divided by the total risk exposure amount), the measure every "
    "other bank in this project reports on these sheets. FY2019-FY2023 are transcribed from each year's own "
    "standalone Pillar 3 disclosure, 'Capital Requirement, Resources & Ratios' table (and its section 4.3 "
    "'Capital Buffers' restatement, where the edition has one); FY2025 is from the Annual Report's own "
    "narrative ('The CET1 capital ratio to the total risk exposure is 88.70%'). Each Pillar 3 ratio reconciles "
    "against that same document's own capital and total-risk-exposure figures: FY2023 194,469/224,516 = 86.62%, "
    "FY2021 192,598/230,466 = 83.57% and FY2020 191,794/229,855 = 83.44% reproduce the printed values exactly, "
    "FY2022 193,221/213,927 = 90.32% against a printed 90.31% (a 0.01pp rounding difference inside the Bank's "
    "own figures; the printed value is carried, nothing is back-solved). FY2024 was blank here until "
    "2026-09-18 and is now 92.33%, taken from the FY2024 Annual Report's own narrative ('The CET1 capital "
    "ratio to the total risk exposure is 92.33%', Strategic Report, PDF p.12 of 60) - the identical sentence "
    "in the identical section that already sources FY2025. It had been missed because that report is an "
    "image-only scan with no text layer, so every text search of it returned zero; the sentence is legible "
    "only after OCR, and was confirmed against a 200 DPI render of the page rather than trusted from OCR. "
    "There is still NO Pillar 3 edition for FY2024, so this ratio has no published denominator to tie to - "
    "see the Total RWAs sheet.\n"
    "THE FY2024 REPORT PRINTS CAPITAL COVER THREE TIMES, AT THREE DIFFERENT VALUES, AND THAT IS THE BANK'S "
    "OWN INCONSISTENCY, NOT A TRANSCRIPTION CHOICE: the Capital Cover chart on PDF p.13 reads 349%, the "
    "narrative beneath it says the cover 'has increased from 325% in 2023 to 347% in the year 2024', and the "
    "Strategic Report on p.12 says 'a capital cover of 346.77%'. Row 2 carries 349%, the CHART value, because "
    "the chart is the series every other year on this sheet is transcribed from (FY2023 325%, FY2022 339%, "
    "and so on) - so the row stays internally comparable across years. The other two values are recorded here "
    "rather than reconciled away. The same report likewise prints two different capital bases - EUR196,091,098 "
    "as shareholders' funds and net assets, and EUR196,287,187 as 'the Bank's capital base' - and the CET1 "
    "Capital sheet carries the latter, which is the one the Bank labels as its capital base.\n"
    "FY2019 IS THE ONE YEAR WHERE THE THREE RATIO SHEETS DIFFER, AND THAT IS AS PRINTED. The 2019 Pillar 3's "
    "ratio table gives a CET1 capital ratio of 81.0% but a Tier 1 capital ratio and total capital ratio of "
    "84.4%, even though the same table shows Tier 2 capital as nil - so on the CRR definitions all three should "
    "be identical, as they are in every other year. Reconstructing both: 191,102/226,309 = 84.44%, matching the "
    "Tier 1 and total figures; 183,220/226,309 = 80.96%, matching the CET1 figure - i.e. the printed CET1 ratio "
    "appears to have been computed on SHARE CAPITAL ALONE (EUR183,220k), excluding the general banking risk "
    "reserve and profit and loss account that the same table includes in CET1 capital. The 2020 edition does "
    "not repeat this: it prints all three at 83.44% on the full CET1 base. The figures are carried here exactly "
    "as printed in each sheet's own line and NOT restated to 84.4%, per this project's transcribe-as-reported "
    "convention - but treat FY2019's CET1 Ratio cell as the Bank's own presentation quirk rather than a real "
    "3.4pp gap between its CET1 and Tier 1 ratios.\n"
    "ROW 2 is the Bank's own 'Capital Cover' percentage, disclosed every year as a Strategic Report chart. It "
    "is NOT a CET1/RWA ratio - it measures capital against the Bank's total capital REQUIREMENT (Pillar 1 plus "
    "a Pillar 2A add-on), which is why it reads in the 300s while the CRR ratio reads in the 80s-90s for the "
    "same year. It is retained because it is the only measure available for all seven years and was the series "
    "these sheets previously carried; it must not be compared with other banks' ratio sheets.\n"
    "Capital = CET1 = Tier 1 = Total Capital throughout, per the Bank's own statement that it holds no Tier 2 "
    "or Tier 3 capital, so one printed ratio serves all three sheets - the FY2021 Pillar 3 confirms this by "
    "printing the CET1, Tier 1 and Total capital ratios all at 83.57%.\n"
    "UNRESOLVED, RECORDED NOT SILENTLY CORRECTED: the FY2025 Annual Report's narrative (p.14, confirmed by "
    "page-image reading at 450 dpi) states a capital cover of 333.16%, where the Capital Cover row carries "
    "331% for FY2025 sourced from the Strategic Report chart. Charts and narrative may legitimately differ in "
    "rounding or vintage within the same filing, and the chart itself was not re-read at image level this "
    "session, so the existing 331% is left untouched and the discrepancy is flagged here instead."
)

P3_SOURCES_NOTE = (
    "PRIOR CLAIM CORRECTED (2026-09-15): earlier passes on this bank recorded that \"no standalone Pillar 3 "
    "document was found\" and attributed the absence to correspondent-banking/website constraints. That was "
    "wrong. Bank Saderat Plc publishes a 'Basel Disclosures Archive' page, linked from the top-level navigation "
    f"of its own live site ({P3_ARCHIVE_URL}), carrying every Pillar 3 edition from 2010 to 2023 as downloadable "
    "PDFs with full text layers. The FY2019-FY2023 editions were downloaded and read directly:\n"
    f"FY2023: Bank Saderat PLC Pillar 3 disclosures 2023, p.12 (capital and risk exposure table) and p.13 "
    f"(section 4.3 'Capital Buffers', ratio table) - {P3_2023_URL}\n"
    f"FY2022: Bank Saderat PLC Pillar 3 disclosures 2022, p.12 and section 4.3 - {P3_2022_URL}\n"
    f"FY2021: Bank Saderat PLC Pillar 3 disclosures 2021, capital resources/capital ratios table and section 4.3 "
    f"- {P3_2021_URL}\n"
    f"FY2020: Bank Saderat PLC Pillar 3 disclosures 2020 (ver 7), pp.14-15, 'Capital Requirement, Resources & "
    f"Ratios' table and section 4.3 - {P3_2020_URL}\n"
    f"FY2019: Bank Saderat PLC Basel III Pillar 3 Disclosures 2019, pp.6-7, 'Capital Requirement, Resources & "
    f"Ratios' table - {P3_2019_URL}\n"
    "FY2019 AND FY2020 ADDED 2026-09-15, CORRECTING A SECOND CLAIM ON THIS BANK. The pass that found the "
    "archive read only the 2021-2023 files and left a note here saying FY2019/FY2020 had no Pillar 3 edition. "
    "The archive page links both directly - 'Basel III Pillar 3 Disclosures 2019.pdf' and 'Pillar 3   "
    "disclosures 2020 ver 7.pdf' - and both return HTTP 200 with a full text layer. What is genuinely absent is "
    "only FY2024/FY2025, the years after the archive stops.\n"
    "VALIDATION: each Pillar 3's own funds figure reproduces the CAPITAL_BASE figure already carried on the CET1 "
    "Capital sheet from the statutory accounts, to the euro (FY2023 EUR194,469k vs 194,469,375; FY2022 "
    "EUR193,221k vs 193,220,561; FY2021 EUR192,598k vs 192,597,935; FY2020 EUR191,794k vs 191,793,736; FY2019 "
    "EUR191,102k vs 191,101,891) - independent confirmation of entity and year before any new figure was "
    "accepted. The risk-type components foot exactly to the printed total in all five years (FY2023 "
    "214,136+765+9,615 = 224,516; FY2022 204,055+748+9,124 = 213,927; FY2021 220,810+722+8,934 = 230,466; "
    "FY2020 220,485+655+8,715 = 229,855; FY2019 216,933+1,088+8,288 = 226,309).\n"
    "ONE INTERNAL INCONSISTENCY IN THE 2020 EDITION, RECORDED NOT CORRECTED: its section 8 operational-risk "
    "table derives an operational risk exposure of EUR7,839k (three-year average income EUR4,181k x 15% = "
    "EUR627k capital, / 8%), while its capital table on p.14 - the source used here - carries EUR8,715k with a "
    "capital requirement of EUR697k. Only the p.14 figure foots to that document's own printed total risk "
    "exposure amount of EUR229,855k, which in turn reproduces the printed 83.44% ratio against the known "
    "capital base, so the p.14 figure is the one carried. The 2019 edition has no such conflict.\n"
    "TAXONOMY: the Bank presents its risk exposure amount as credit risk / FX risk / operational risk, not as a "
    "UK OV1 template, so the RWA Breakdown sheet follows the Bank's own three-way presentation rather than "
    "mapping it onto OV1 categories it does not use.\n"
    "FY2024 AND FY2025 ARE GENUINELY UNPUBLISHED, not unsourced: the archive page's newest entry is the 2023 "
    "edition, and eight filename permutations for 2024/2025 all return HTTP 404 from the same /Reports/ path "
    "that serves the 2023 file with HTTP 200 (checked 2026-09-15). Leverage Ratio, LCR and NSFR are absent from "
    "all five Pillar 3 editions as well - a case-insensitive search for 'leverage', 'liquidity coverage', "
    "'LCR', 'net stable funding' and 'NSFR' across the full text of each returns no match - so those sheets "
    "remain on their existing Annual Report basis or blank. The LCR sheet's FY2019/FY2020 cells therefore stay "
    "blank: the Pillar 3 editions for those years do not carry the ratio, and the FY2021 edition prints no "
    "2020 comparative for it either."
)

# EVIDENCE BEHIND THIS NOTE, re-established 2026-09-16.
#
# The previous wording enumerated only "no leverage, LCR or NSFR figures" yet
# was reused verbatim for the MREL Ratio sheet, so the MREL claim rested on a
# search that never included the term MREL. That is the shared-constant trap:
# one sentence, four sheets, and only three of the four metrics actually
# checked. (Now map rule 14 in wayfinder/km1/map.md.)
#
# Re-checked by searching the full text of TEN primary documents - all five
# standalone Pillar 3 editions (FY2019-FY2023) and all five Annual Reports on
# file. Every one verified as a real PDF first (HTTP 200, application/pdf,
# %PDF magic bytes). The Annual Reports are scanned image-only - pdftotext
# returns 37-63 characters from a 1.4-2.9 MB file - so they were searched via
# the OCR sidecars in research/ocr_text/ instead; the FY2019 sidecar did not
# exist and was produced for this check.
#
# "mrel", "minimum requirement for own funds" and "loss-absorb" all return
# ZERO across all ten documents. Per map rule 15, a zero only counts once the
# extraction is shown to be rich: these run 47-114 hits for "capital", 49-118
# for "ratio", 53-89 for "pillar" in the Pillar 3 set, and 13-51 for
# "liquidity" in the reports. So the absence is a fact about the documents,
# not about our tooling.
NOT_DISCLOSED_NOTE = (
    "Not disclosed in the Bank's own Annual Reports, and absent from its standalone Pillar 3 disclosures for "
    "FY2021-FY2023 (which do exist - see the Total RWAs and RWA Breakdown sheets - but contain no leverage, LCR, "
    "NSFR or MREL figures). Verified 2026-09-16 by full-text search of all five Pillar 3 editions (FY2019-FY2023) "
    "and all five Annual Reports; the Annual Reports are scanned image-only, so they were searched via OCR rather "
    "than by text extraction, which returns almost nothing from them. The Strategic Report's capital/liquidity "
    "disclosure is limited to the 'Capital Cover' and Liquidity Coverage Ratio charts plus the CET1 capital base "
    "figure (see the other Pillar 3 sheets)."
)

# ---------------------------------------------------------------
# KM1 Key Metrics - NOT APPLICABLE. This bank DOES publish Pillar 3
# disclosures - a continuous annual series back to 2008 on its own Reports
# page - but none of them contains the UK KM1 key-metrics template. That is a
# different statement from "publishes no Pillar 3", and the distinction is the
# point of this sheet.
#
# THE TEST APPLIED: a table is the KM1 template if it carries the template's
# ROW SET, whatever it is titled and whether or not its rows are numbered.
# Some banks print the template headed only "Key metrics" with no numbers at
# all, and those count. Bank Saderat's capital disclosure fails the test on
# every count: it is a single-column bespoke narrative table of the Bank's own
# design (share capital / general reserve / reserves / CET1 / Tier 1 / total
# own funds, then a Pillar 1 and Pillar 2A build-up by risk type, then a
# buffer stack), with no template row numbers, no rows 5-7 capital-ratio
# block, no UK 7a-7d SREP rows, no UK 11a, and no rows 15-20 for LCR or NSFR.
# Mapping it onto KM1 row numbers would invent a correspondence the Bank never
# published.
# ---------------------------------------------------------------
KM1_SOURCES = (
    "Sources — none. Bank Saderat PLC publishes Pillar 3 disclosures, but no edition contains the UK KM1 "
    "key-metrics template, so there is nothing to reproduce on this sheet.\n\n"
    "Latest-edition check, 2026-09-16: the Bank's own Reports index at https://www.saderat-plc.com/Reports "
    "was read directly. It lists a continuous Pillar 3 series — Basel II editions for 2010–2015, Basel III "
    "for 2016–2019, and untitled-series editions for 2020, 2021, 2022 and 2023. THE NEWEST IS 2023; there is "
    "no 2024 or 2025 Pillar 3 document, which is why those years are blank or Annual-Report-sourced on the "
    "metric sheets. Checked, none newer.\n\n"
    "WHY THIS IS 'NO KM1' RATHER THAN 'NO PILLAR 3'. The FY2020–FY2023 editions were downloaded and read "
    "(HTTP 200, Content-Type application/pdf, %PDF magic bytes verified). Each carries a capital disclosure "
    "of the Bank's own design: a single undated column listing share capital, general reserve, reserves, "
    "CET1 capital, Tier 1 capital and total own funds; then risk-weighted assets split into credit, FX and "
    "operational risk; then a Pillar 1 minimum and a long Pillar 2A add-on build-up by risk type "
    "(settlement/residual, market, concentration by single name/country/sector, operational, IRRBB, sanction "
    "risk, payment risk, and financial risk due to climate change); then a buffer stack (capital "
    "conservation, PRA buffer, countercyclical) and the Bank's own 'Capital Cover' measure.\n\n"
    "That is a genuine Pillar 3 capital disclosure, and every figure this workbook takes from it is on the "
    "individual metric sheets. But it is NOT the KM1 template: it has no template row numbers, no capital-"
    "ratio block in rows 5-7 form, no UK 7a-7d SREP rows, no UK 11a overall capital requirement row, and no "
    "rows 15-20 for LCR or NSFR. The string 'KM1' appears nowhere in any edition, and neither do the "
    "template's own row captions.\n\n"
    "The test this project applies is the ROW SET, not the title and not the numbering — a bank that prints "
    "the template headed merely 'Key metrics', with no row numbers, still has a KM1 (Allica and Europe Arab "
    "Bank both do). Bank Saderat's table fails that test on every count, so mapping it onto KM1 row numbers "
    "would assert a correspondence the Bank never published. Nothing has been reconstructed here."
)

bw.add_km1_sheet(
    title="Bank Saderat PLC — KM1 Key Metrics",
    subtitle="Not applicable — the Bank publishes Pillar 3 disclosures (a continuous series back to 2010, "
             "newest edition 2023) but none of them contains the UK KM1 key-metrics template. Its capital "
             "disclosure is a bespoke single-column table of the Bank's own design, which is a different "
             "thing; see the source note below for the test applied and the individual Pillar 3 metric "
             "sheets for what that table does disclose.",
    rows=[
        ("DATA", "UK KM1 key-metrics template", {y: "Not used in any Pillar 3 edition" for y in YEARS}),
    ],
    sources_text=KM1_SOURCES,
    first_col_width=48,
    source_height=300,
)

metric("CET1 Capital", "£m (Bank's disclosed capital base, consisting of CET1 Capital)",
       [("Common Equity Tier 1 (CET1) capital", capital_base_gbp)])

metric("CET1 Ratio", "%",
       [("CET1 capital ratio (CRR: own funds / total risk exposure amount)", CRR_RATIO_CET1),
        ("Capital Cover (Bank's own metric - NOT a CRR ratio)", CAPITAL_COVER)],
       note=CAPITAL_COVER_NOTE)

metric("Tier 1 Capital", "£m (= CET1 Capital; no AT1 instruments)", [("Tier 1 capital", capital_base_gbp)])

metric("Tier 1 Ratio", "%",
       [("Tier 1 capital ratio (CRR: own funds / total risk exposure amount)", CRR_RATIO_TIER1),
        ("Capital Cover (Bank's own metric - NOT a CRR ratio)", CAPITAL_COVER)],
       note=CAPITAL_COVER_NOTE)

metric("Total Capital", "£m (= CET1 Capital; no Tier 2 instruments)", [("Total capital", capital_base_gbp)])

metric("Total Capital Ratio", "%",
       [("Total capital ratio (CRR: own funds / total risk exposure amount)", CRR_RATIO_TOTAL),
        ("Capital Cover (Bank's own metric - NOT a CRR ratio)", CAPITAL_COVER)],
       note=CAPITAL_COVER_NOTE)

# GAP-FILL (2026-09-18): FY2024 and FY2025 previously carried NO cell on the Total
# RWAs or RWA Breakdown sheets, so four sheet-years read as blank to audit_gaps.py.
# The finding is now stated IN the columns. Separate display dicts are used so the
# numeric series feeding other sheets stays numeric.
# THE NEGATIVE WAS RE-ESTABLISHED FROM TWO INDEPENDENT SIDES ON 2026-09-18:
#   (1) No Pillar 3 edition exists for FY2024 or FY2025. The Bank's OWN live index,
#       https://www.saderat-plc.com/Basel_Disclosures.htm, was fetched today and
#       lists Pillar 3 editions for 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016,
#       2015, 2013, 2011 and 2010 - the newest is 2023. Wayback CDX agrees. NOTE THE
#       FETCH: plain curl and curl --http1.1 both returned HTTP 403; only a browser
#       User-Agent PLUS an Accept header got HTTP 200. A 403 here is a live host
#       refusing the client, NOT evidence that the page or the documents are absent,
#       and an earlier pass that stopped at the 403 would have recorded the wrong
#       reason for the same gap.
#   (2) Neither Annual Report prints a risk-weighted-asset amount. Both are
#       image-only scans (FY2024 61pp/61 chars, FY2025 63pp/63 chars - i.e. one
#       form feed per page and NO text layer at all), so they were OCR'd before
#       being searched; a text search of the raw PDFs returns zero for every term
#       including ones known to be present, which is an instrument limit and not a
#       fact about the documents. After OCR, each report gives only a capital
#       amount, a Capital Cover percentage and a CET1-to-total-risk-exposure ratio.
# DELIBERATELY NOT BACK-SOLVED. FY2024 prints CET1 of EUR196,091,098 and a CET1
# ratio of 92.33%; FY2025 prints EUR196,228,824 and 88.70%. Dividing one by the
# other would manufacture a total risk exposure amount for both years. That is
# exactly the derivation this project forbids, and the resulting figure would be
# indistinguishable in the sheet from one the Bank actually published.
RWA_NOT_PUBLISHED = ("Not published - no Pillar 3 edition for this year; the Annual Report prints no risk "
                     "exposure amount (not derived from capital/ratio)")
RWA_TOTAL_DISPLAY = dict(gbp_m_spot(P3_RWA_TOTAL_EUR),
                         **{"FY2025": RWA_NOT_PUBLISHED, "FY2024": RWA_NOT_PUBLISHED})
RWA_CREDIT_DISPLAY = dict(gbp_m_spot(P3_RWA_CREDIT_EUR),
                          **{"FY2025": RWA_NOT_PUBLISHED, "FY2024": RWA_NOT_PUBLISHED})
# Every component row carries the statement, not just credit risk and the total.
# A column where only some rows speak would read as though the silent rows were a
# separate finding - e.g. that FX risk specifically was nil or not applicable in
# FY2024/FY2025 - when in fact the whole three-way split is missing for the one
# reason: there is no Pillar 3 edition for either year to split.
RWA_FX_DISPLAY = dict(gbp_m_spot(P3_RWA_FX_EUR),
                      **{"FY2025": RWA_NOT_PUBLISHED, "FY2024": RWA_NOT_PUBLISHED})
RWA_OP_DISPLAY = dict(gbp_m_spot(P3_RWA_OP_EUR),
                      **{"FY2025": RWA_NOT_PUBLISHED, "FY2024": RWA_NOT_PUBLISHED})

metric("Total RWAs", "£m (converted from €'000 at each year's own period-end spot rate)",
       [("Total risk exposure amount", RWA_TOTAL_DISPLAY)],
       note="FY2019-FY2023 are the total risk exposure amount printed in each year's own standalone Pillar 3 "
            "disclosure (EUR '000, converted to £m at that year's period-end spot rate per this workbook's FX "
            "convention): FY2023 EUR224,516k, FY2022 EUR213,927k, FY2021 EUR230,466k, FY2020 EUR229,855k, "
            "FY2019 EUR226,309k. Each reconciles against that document's own capital figure and printed capital "
            "ratio (see the CET1 Ratio sheet), and each year's Pillar 3 capital amount reproduces the "
            "statutory-accounts capital base on the CET1 Capital sheet to the euro - which is what confirms "
            "these are the same entity and basis. FY2019 and FY2020 were added 2026-09-15 from the 2019 and "
            "2020 Pillar 3 editions, which the earlier pass on this bank had recorded as non-existent; they are "
            "linked from the same archive page as the others (see the RWA Breakdown sheet's note). FY2024 and "
            "FY2025 carry an explicit statement in place of a figure, re-verified 2026-09-18 from both sides: "
            "the Bank's OWN live Basel disclosures index (fetched that day - plain curl returns HTTP 403, only "
            "a browser User-Agent plus an Accept header returns 200, so a 403 here means a host refusing the "
            "client and NOT a missing page) still lists nothing newer than the 2023 edition; and both Annual "
            "Reports, which are image-only scans with no text layer and had to be OCR'd before they could be "
            "searched at all, disclose no risk exposure amount anywhere. NOT back-solved from the printed CET1 "
            "ratios (FY2024 92.33% on CET1 of EUR196,091,098; FY2025 88.70% on EUR196,228,824), even though "
            "dividing one by the other would yield a number for both years - a derived denominator would sit in "
            "this column indistinguishable from one the Bank actually published.")

bw.add_rwa_breakdown_sheet(
    title="Bank Saderat Plc — RWA Breakdown",
    subtitle="FY2019-FY2023 from each year's own Pillar 3 disclosure (EUR '000 converted to £m at period-end "
             "spot). FY2024/FY2025 state the reason for the absence in place of figures - see note below.",
    rows=[
        ("SECTION", "Risk exposure amount by risk type (Bank's own Pillar 3 presentation)", {}),
        ("DATA", "Credit risk (risk weighted assets)", RWA_CREDIT_DISPLAY),
        ("DATA", "Foreign exchange (FX) risk", RWA_FX_DISPLAY),
        ("DATA", "Operational risk", RWA_OP_DISPLAY),
        ("TOTAL", "Total risk exposure amount", RWA_TOTAL_DISPLAY),
    ],
    sources_text=p3_sources(RATIO_PAGES) + "\n\n" + P3_SOURCES_NOTE,
    first_col_width=54,
    source_height=300,
    unit_suffix=" (£m)",
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
OPENING_KEY = {"FY2019": "2019-01-01", "FY2020": "2019-12-31", "FY2021": "2021-01-01", "FY2022": "2021-12-31", "FY2023": "2022-12-31", "FY2024": "2023-12-31", "FY2025": "2024-12-31"}
CLOSING_KEY = {"FY2019": "2019-12-31", "FY2020": "2020-12-31", "FY2021": "2021-12-31", "FY2022": "2022-12-31", "FY2023": "2023-12-31", "FY2024": "2024-12-31", "FY2025": "2025-12-31"}
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
        ("CET1 Ratio", CRR_RATIO_CET1),
        ("Tier 1 Ratio", CRR_RATIO_TIER1),
        ("Total Capital Ratio", CRR_RATIO_TOTAL),
        ("LCR", LCR_ALL_CCY),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing. ALL £ figures in this "
         "workbook are converted from Bank Saderat Plc's native EUR reporting - see the Cash Flow Statement "
         "sheet's source note for the full FX methodology and rates used. Ratios (%) are shown exactly as "
         "reported in EUR and were not converted. CHANGED 2026-09-15: the CET1/Tier 1/Total Capital Ratio rows "
         "now carry the genuine CRR ratio (own funds / total risk exposure amount), transcribed from the Bank's "
         "own Pillar 3 disclosures for FY2019-FY2023 and from the Annual Report narrative for FY2025. They "
         "previously carried the Bank's 'Capital Cover' metric, which reads in the 300s because it measures "
         "capital against the capital REQUIREMENT rather than against risk exposure, and so was not comparable "
         "with any other bank in this project; Capital Cover is still shown, labelled, as the second row on each "
         "ratio detail sheet. FY2024 is blank here because no Pillar 3 edition exists for it - it is not zero, "
         "and its Capital Cover of 349% is on the detail sheets. FY2019's CET1 cell (81.0%) differs from its "
         "Tier 1/Total cells (84.4%) because the 2019 Pillar 3 prints them that way - see the ratio sheets' "
         "note. FY2025 was also materially affected by UK 'snapback' sanctions from 29 "
         "September 2025 - see ENTITY_NOTE. Leverage Ratio, NSFR and MREL Ratio are not publicly disclosed for "
         "this entity and are omitted from this chart.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BANK SADERAT FINANCIALS.xlsx")
