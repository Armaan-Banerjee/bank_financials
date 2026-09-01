import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# SMBC Bank International plc reports in USD (its functional currency) - this
# workbook converts every $ figure to £ at the user's request. See FX_NOTE
# below for the full methodology; ratios are never converted (see FX_NOTE).
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first

AR2021_URL = "https://web.archive.org/web/20240612221125/https://www.smbcgroup.com/emea/images/SMBC/media/SMBC/pdf/disclosures/smbcbi-annual-report-2021.pdf"
AR2022_URL = "https://www.smbcgroup.com/emea/getmedia/efb562ee-627d-41c9-823a-b157f879892f/Annual-Report-and-Financial-Statements-2022-(SMBC-BI).pdf"
AR2023_URL = "https://www.smbcgroup.com/emea/getmedia/1784eaa0-0924-4cd7-a4e4-1613b6cb015f/Annual-Report-and-Financial-Statements-2023-(SMBC-BI).pdf"
AR2024_URL = "https://www.smbcgroup.com/emea/getmedia/1c52fee7-2c0d-4378-b571-bd45d5f6ea9f/PDF-Annual-report-(SMBC-BI).pdf"
AR2025_URL = "https://www.smbcgroup.com/emea/getmedia/28eec268-62ab-4d64-b597-02b7f918c767/smbcbi-annual-report-2025.pdf"

P3_2021_URL = "https://www.smbcgroup.com/emea/getmedia/c956424b-468e-4f29-9650-a4c792a720c3/Pillar-3-Interim-Disclosure-March-2021-(SMBC-BI).pdf"
P3_2022_URL = "https://web.archive.org/web/20240712094621/https://www.smbcgroup.com/emea/images/SMBC/media/Notices-Reporting/Corporate%20Disclosures/smbcbi-pillar3-2022.pdf"
P3_2023_URL = "https://www.smbcgroup.com/emea/getmedia/352315cf-7a34-42d7-9cb1-3082d16539f3/Pillar-3-Interim-Disclosure-March-2023-(SMBC-BI).pdf"
P3_2024_URL = "https://www.smbcgroup.com/emea/getmedia/7690b9ee-bae2-4fc1-bba5-0422a250f84c/Pillar-3-Interim-Disclosure-March-2024-(SMBC-BI).pdf"
P3_2025_URL = "https://www.smbcgroup.com/emea/getmedia/2418d0a0-de22-497a-9a9a-4ca69ade9f94/Pillar-3-annual-disclosure-(SMBC-BI-%E2%80%93-31-March-2025).pdf"

# ---------------------------------------------------------------
# FX conversion: GBP-per-1-USD is NOT what these are - these are GBP/USD
# quotes in the market convention "£1 = $X" (Bank of England spot rate,
# sterling into US dollar). To convert a $ amount to £: gbp = usd / rate.
# Source: Bank of England daily reference rates, via poundsterlinglive.com's
# published archive of the official BoE series
# (https://www.poundsterlinglive.com/bank-of-england-spot/historical-spot-exchange-rates/gbp/GBP-to-USD-<year>).
# "period_end" = spot rate on the fiscal year-end date (31 March each year;
# FY2021's *opening* balance needs 31 Mar 2020's rate too, included below).
# "average" = simple arithmetic mean of the 12 month-end spot rates falling
# within that fiscal year (1 April - 31 March) - a standard simplified proxy
# for a true daily average, used because the source's daily series does not
# expose a ready-made period-average figure.
FX_RATES = {
    "FY2020": {"period_end": 1.2403},  # 31 Mar 2020 only - needed for FY2021's opening cash balance
    "FY2021": {"period_end": 1.3796, "average": 1.3193},
    "FY2022": {"period_end": 1.3162, "average": 1.3617},
    "FY2023": {"period_end": 1.2364, "average": 1.2043},
    "FY2024": {"period_end": 1.2632, "average": 1.2581},
    "FY2025": {"period_end": 1.2910, "average": 1.2775},
}
PRIOR_YEAR = {"FY2021": "FY2020", "FY2022": "FY2021", "FY2023": "FY2022", "FY2024": "FY2023", "FY2025": "FY2024"}


def gbp_spot(usd_by_year):
    """Convert a {year: $m} dict to £m using that year's OWN period-end spot rate (stocks)."""
    return {y: round(v / FX_RATES[y]["period_end"], 1) for y, v in usd_by_year.items()}


def gbp_spot_prior(usd_by_year):
    """Convert a {year: $m} dict to £m using the PRIOR year's period-end spot rate
    (for opening cash balances, which are last year's closing balance)."""
    return {y: round(v / FX_RATES[PRIOR_YEAR[y]]["period_end"], 1) for y, v in usd_by_year.items()}


def gbp_avg(usd_by_year):
    """Convert a {year: $m} dict to £m using that year's average rate (flows)."""
    return {y: round(v / FX_RATES[y]["average"], 1) for y, v in usd_by_year.items()}


FX_NOTE = (
    "FX CONVERSION NOTE: SMBC Bank International plc reports in US Dollars (its functional currency, per its own "
    "Annual Report). This workbook converts every $ amount to £ at the user's request - conversion was necessary "
    "because every other workbook in this series is £-denominated and SMBC BI does not itself publish £ figures. "
    "Methodology: point-in-time/balance figures (capital, RWA, leverage exposure, HQLA, cash balances) use the "
    "Bank of England GBP/USD SPOT rate as at that fiscal year-end (31 March); flow figures (every cash flow "
    "statement line item) use the AVERAGE of the 12 month-end spot rates over that fiscal year (1 April-31 March), "
    "since a true daily average was not practically obtainable - both from Bank of England daily reference rates "
    "via poundsterlinglive.com's published archive. Rates used (£1 = $X): 31 Mar 2020 spot 1.2403 (FY2021 opening "
    "cash only); FY2021 spot 1.3796 / average 1.3193; FY2022 spot 1.3162 / average 1.3617; FY2023 spot 1.2364 / "
    "average 1.2043; FY2024 spot 1.2632 / average 1.2581; FY2025 spot 1.2910 / average 1.2775. All % ratios (CET1/"
    "Tier 1/Total Capital/Leverage/LCR/NSFR ratios) are shown EXACTLY as reported in USD and were NOT converted - "
    "a ratio is dimensionless and currency-invariant since both its numerator and denominator would move by the "
    "same factor. Because stocks and flows are converted at different rates (standard practice for translating "
    "foreign-currency financial statements), the cash flow statement includes an explicit 'Effect of GBP/USD "
    "translation' reconciling line so opening + all flows + this line = closing exactly in £ terms - this line is "
    "purely an artefact of £ translation and has no bearing on the Bank's underlying USD results."
)

ENTITY_NOTE = (
    "ENTITY NOTE: SMBC Bank International plc (SMBC BI), FRN 223304, is a wholesale bank headquartered in London "
    "and a wholly-owned subsidiary of Sumitomo Mitsui Banking Corporation (SMBC), itself part of Sumitomo Mitsui "
    "Financial Group (Japan). It was incorporated in 2003 as Sumitomo Mitsui Banking Corporation Europe Limited and "
    "renamed/re-registered as a public limited company in 2020. On 7 October 2024, SMBC BI completed a project "
    "transferring the securities business of SMBC Nikko Capital Markets Limited (a portfolio of debt securities and "
    "other fixed income assets) to itself, and opened a branch in the Abu Dhabi Global Market - this accounts for "
    "new FY2025 cash flow line items (trading portfolio assets/liabilities, repurchase agreements) not present in "
    "earlier years, and for part of the FY2025 RWA increase. Figures are on SMBC Bank International plc's own "
    "(entity-level) basis throughout, both for cash flow and Pillar 3."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are SMBC Bank International plc's own Statement of cash flows, converted from USD to "
    "£m (see FX conversion note below):\n"
    f"FY2025: SMBC BI Annual report and financial statements, year ended 31 March 2025, p.72 (Statement of cash "
    f"flows) - {AR2025_URL}\n"
    f"FY2024: SMBC BI Annual report and financial statements, year ended 31 March 2024, p.85 (Statement of cash "
    f"flows) - {AR2024_URL}\n"
    f"FY2023: SMBC BI Annual report and financial statements, year ended 31 March 2023, p.90 (Statement of cash "
    f"flows) - {AR2023_URL}\n"
    f"FY2022: SMBC BI Annual report and financial statements, year ended 31 March 2022, p.87 (Statement of cash "
    f"flows) - {AR2022_URL}\n"
    f"FY2021: SMBC BI Annual report & financial statements, year ended 31 March 2021, p.75 (Statement of cash "
    f"flows) - {AR2021_URL}\n"
    "Each year's own report was used for its own column (not a restated comparative); every year's own figure was "
    "cross-checked against its appearance as the comparative column in the following year's report and matched "
    "exactly in all cases, so there are no presentation-basis restatements to flag across vintages (only new line "
    "items appearing from FY2025 onward - see entity note). Note: FY2025's operating/investing/financing subtotals "
    "sum to £1,785.5m against a directly-converted net change of £1,785.4m - a £0.1m rounding artefact from "
    "rounding each £ line independently to 1 decimal place before summing, not a data error; the full statement "
    "still ties exactly end-to-end via the net change, FX and translation-effect lines.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE
)


def p3_sources(page):
    return (
        "Sources - SMBC Bank International plc's own Basel III Pillar 3 Disclosures, converted from USD to £m "
        f"where a $ amount (see FX conversion note on the Cash Flow Statement sheet; % ratios are unconverted):\n"
        f"FY2025: Table 2.1 KM1 - Key metrics, p.{page['FY2025']} - {P3_2025_URL}\n"
        f"FY2024: Table 1 KM1 - Key metrics, p.{page['FY2024']} - {P3_2024_URL}\n"
        f"FY2023: Table 1 KM1 - Key metrics, p.{page['FY2023']} - {P3_2023_URL}\n"
        f"FY2022: Table 1 KM1 Key metrics, p.{page['FY2022']} - {P3_2022_URL}\n"
        f"FY2021: 2.1 Key metrics dashboard, p.{page['FY2021']} - {P3_2021_URL}"
    )


bw = BankWorkbook(bank_name="SMBC Bank International plc", years=YEARS, header_color="1B6B3C")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (raw USD figures, converted at build time)
# ---------------------------------------------------------------
PROFIT_BEFORE_TAX = {"FY2025": 483.6, "FY2024": 535.6, "FY2023": 340.3, "FY2022": 180.8, "FY2021": 333.1}
IMPAIRMENT_LOSS = {"FY2025": 28.3, "FY2024": 27.2, "FY2023": 47.7, "FY2022": 95.8, "FY2021": 8.6}
LOSS_ON_DISPOSAL = {"FY2025": 83.7}
UNREALISED_FX = {"FY2025": -239.2, "FY2024": -161.3, "FY2023": -1076.0, "FY2022": -1121.7, "FY2021": 1698.8}
DEPRECIATION = {"FY2025": 62.1, "FY2024": 55.6, "FY2023": 51.9, "FY2022": 42.7, "FY2021": 40.8}
CHG_LOANS_BANKS = {"FY2025": -35.0, "FY2024": -276.4, "FY2023": 736.4, "FY2022": -197.8, "FY2021": 8.9}
CHG_LOANS_CUSTOMERS = {"FY2025": -1292.4, "FY2024": -321.5, "FY2023": 2255.5, "FY2022": 856.4, "FY2021": 1943.4}
CHG_REVERSE_REPO = {"FY2025": -15373.7, "FY2024": -443.5, "FY2023": -69.0, "FY2022": 534.8, "FY2021": -230.2}
CHG_DERIVATIVES = {"FY2025": 358.0, "FY2024": -139.5, "FY2023": -100.5, "FY2022": -80.9, "FY2021": 123.5}
CHG_OTHER_ASSETS = {"FY2025": -698.8, "FY2024": 162.5, "FY2023": -214.0, "FY2022": -200.7, "FY2021": 341.6}
CHG_DEPOSITS_BANKS = {"FY2025": 7630.1, "FY2024": -4082.8, "FY2023": -1387.4, "FY2022": 2550.6, "FY2021": -1854.8}
CHG_CUSTOMER_ACCOUNTS = {"FY2025": -149.1, "FY2024": 1157.2, "FY2023": -1085.1, "FY2022": -2565.1, "FY2021": -5329.7}
CHG_OTHER_LIABILITIES = {"FY2025": 145.4, "FY2024": 99.4, "FY2023": 245.9, "FY2022": 107.6, "FY2021": -324.4}
CHG_TRADING_ASSETS = {"FY2025": -1497.7}
CHG_TRADING_LIABILITIES = {"FY2025": 294.3}
CHG_REPO_BORROWING = {"FY2025": 12669.1}
TAXES_PAID = {"FY2025": -130.3, "FY2024": -122.8, "FY2023": -91.6, "FY2022": -92.1, "FY2021": -50.5}
NET_OPERATING = {"FY2025": 2338.4, "FY2024": -3510.3, "FY2023": -350.7, "FY2022": 110.4, "FY2021": -3290.9}

PURCHASE_SECURITIES = {"FY2025": -3186.0, "FY2024": -2849.6, "FY2023": -1025.2, "FY2022": -1669.1, "FY2021": -1137.0}
PROCEEDS_SECURITIES = {"FY2025": 3107.4, "FY2024": 3217.3, "FY2023": 992.4, "FY2022": 1145.9, "FY2021": 1269.1}
PURCHASE_INTANGIBLES = {"FY2025": -65.7, "FY2024": -34.5, "FY2023": -24.5, "FY2022": -21.0, "FY2021": -20.9}
PROCEEDS_INTANGIBLES = {"FY2021": 0.2}
PURCHASE_PPE = {"FY2025": -6.6, "FY2024": -24.0, "FY2023": -37.1, "FY2022": -64.1, "FY2021": -199.1}
PROCEEDS_PPE = {"FY2025": 0.5, "FY2021": 15.1}
NET_INVESTING = {"FY2025": -150.4, "FY2024": 309.2, "FY2023": -94.4, "FY2022": -608.3, "FY2021": -72.6}

LEASE_PAYMENTS = {"FY2025": -17.2, "FY2024": -8.3, "FY2023": -5.3, "FY2022": -18.9, "FY2021": -19.0}
PROCEEDS_DEBT_SECURITIES = {"FY2025": 1012.0, "FY2024": 901.9, "FY2023": 1048.7, "FY2022": 976.0, "FY2021": 853.6}
REPAYMENT_DEBT_SECURITIES = {"FY2025": -901.9, "FY2024": -1048.7, "FY2023": -976.0, "FY2022": -853.6, "FY2021": 0}
NET_FINANCING = {"FY2025": 92.9, "FY2024": -155.1, "FY2023": 67.4, "FY2022": 103.5, "FY2021": 834.6}

NET_CHANGE = {"FY2025": 2280.9, "FY2024": -3356.2, "FY2023": -377.7, "FY2022": -394.4, "FY2021": -2528.9}
FX_EFFECT = {"FY2025": 214.3, "FY2024": 159.5, "FY2023": 1020.9, "FY2022": 1157.1, "FY2021": -1824.8}
CASH_BEGIN = {"FY2025": 22798.8, "FY2024": 25995.5, "FY2023": 25352.3, "FY2022": 24589.6, "FY2021": 28943.3}
CASH_END = {"FY2025": 25294.0, "FY2024": 22798.8, "FY2023": 25995.5, "FY2022": 25352.3, "FY2021": 24589.6}

# Reconciling line: with stocks at spot and flows at average, opening + net
# change (avg) + FX effect (avg) will not exactly equal closing (spot) in
# GBP terms - see FX_NOTE. This line absorbs that rate-differential exactly.
cash_begin_gbp = gbp_spot_prior(CASH_BEGIN)
cash_end_gbp = gbp_spot(CASH_END)
net_change_gbp = gbp_avg(NET_CHANGE)
fx_effect_gbp = gbp_avg(FX_EFFECT)
GBP_TRANSLATION_EFFECT = {
    y: round(cash_end_gbp[y] - cash_begin_gbp[y] - net_change_gbp[y] - fx_effect_gbp[y], 1)
    for y in YEARS
}

rows = [
    ("SECTION", "Reconciliation of profit before tax to net cash flows from operating activities", {}),
    ("DATA", "Profit for the year before tax", gbp_avg(PROFIT_BEFORE_TAX)),
    ("DATA", "Net impairment loss on financial assets", gbp_avg(IMPAIRMENT_LOSS)),
    ("DATA", "Net losses from disposal of financial assets at amortised cost", gbp_avg(LOSS_ON_DISPOSAL)),
    ("DATA", "Unrealised exchange movements on non operating assets and liabilities", gbp_avg(UNREALISED_FX)),
    ("DATA", "Depreciation and amortisation", gbp_avg(DEPRECIATION)),
    ("SECTION", "Changes in operating assets and liabilities", {}),
    ("DATA", "Changes in loans and advances to banks", gbp_avg(CHG_LOANS_BANKS)),
    ("DATA", "Changes in loans and advances to customers", gbp_avg(CHG_LOANS_CUSTOMERS)),
    ("DATA", "Changes in reverse repurchase agreements", gbp_avg(CHG_REVERSE_REPO)),
    ("DATA", "Changes in derivative financial instruments", gbp_avg(CHG_DERIVATIVES)),
    ("DATA", "Changes in other assets", gbp_avg(CHG_OTHER_ASSETS)),
    ("DATA", "Changes in deposits by banks", gbp_avg(CHG_DEPOSITS_BANKS)),
    ("DATA", "Changes in customer accounts", gbp_avg(CHG_CUSTOMER_ACCOUNTS)),
    ("DATA", "Changes in other liabilities", gbp_avg(CHG_OTHER_LIABILITIES)),
    ("DATA", "Net decrease/(increase) in trading portfolio assets", gbp_avg(CHG_TRADING_ASSETS)),
    ("DATA", "Net increase in trading portfolio liabilities", gbp_avg(CHG_TRADING_LIABILITIES)),
    ("DATA", "Net increase in repurchase agreements and other similar secured borrowing", gbp_avg(CHG_REPO_BORROWING)),
    ("DATA", "Taxes paid", gbp_avg(TAXES_PAID)),
    ("TOTAL", "Net cash from/(used in) operating activities", gbp_avg(NET_OPERATING)),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of investment securities", gbp_avg(PURCHASE_SECURITIES)),
    ("DATA", "Proceeds from sale or redemption of investment securities", gbp_avg(PROCEEDS_SECURITIES)),
    ("DATA", "Purchase of intangible assets", gbp_avg(PURCHASE_INTANGIBLES)),
    ("DATA", "Proceeds from the sale of intangible assets", gbp_avg(PROCEEDS_INTANGIBLES)),
    ("DATA", "Purchase of property and equipment", gbp_avg(PURCHASE_PPE)),
    ("DATA", "Proceeds from sale of property and equipment", gbp_avg(PROCEEDS_PPE)),
    ("TOTAL", "Net cash from/(used in) investing activities", gbp_avg(NET_INVESTING)),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Payment of lease liabilities", gbp_avg(LEASE_PAYMENTS)),
    ("DATA", "Proceeds from issue of debt securities", gbp_avg(PROCEEDS_DEBT_SECURITIES)),
    ("DATA", "Repayment of debt securities", gbp_avg(REPAYMENT_DEBT_SECURITIES)),
    ("TOTAL", "Net cash from/(used in) financing activities", gbp_avg(NET_FINANCING)),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", net_change_gbp),
    ("DATA", "Exchange differences in respect of cash and cash equivalents (USD)", fx_effect_gbp),
    ("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", GBP_TRANSLATION_EFFECT),
    ("DATA", "Cash and cash equivalents at start of the year", cash_begin_gbp),
    ("TOTAL", "Cash and cash equivalents at 31 March", cash_end_gbp),
]

bw.add_cash_flow_sheet(
    title="SMBC Bank International plc — Consolidated Cash Flow Statement",
    subtitle="£m, converted from USD - see source note at bottom for FX methodology and rates used.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=76,
    source_height=340,
    unit_suffix=" (£m, conv. from USD)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
CET1_CAPITAL = {"FY2025": 5786, "FY2024": 5477, "FY2023": 5083, "FY2022": 4887, "FY2021": 4787.9}
TIER1_CAPITAL = dict(CET1_CAPITAL)   # identical every year - no AT1 instruments
TOTAL_CAPITAL = dict(CET1_CAPITAL)   # identical every year - no Tier 2 instruments either
TOTAL_RWA = {"FY2025": 33891, "FY2024": 28122, "FY2023": 28579, "FY2022": 29941, "FY2021": 28662.1}
LEV_EXPOSURE = {"FY2025": 57267, "FY2024": 37072, "FY2023": 36713, "FY2022": 39509, "FY2021": 62531.4}
LCR_HQLA = {"FY2025": 25359, "FY2024": 25071, "FY2023": 27770, "FY2022": 27160, "FY2021": 25266.0}
LCR_OUTFLOWS = {"FY2025": 15835, "FY2024": 16110, "FY2023": 19094, "FY2022": 20036, "FY2021": 17426.3}
NSFR_ASF = {"FY2025": 22673, "FY2024": 23986, "FY2023": 23984, "FY2022": 23643, "FY2021": 27000.0}
NSFR_RSF = {"FY2025": 17827, "FY2024": 16912, "FY2023": 16839, "FY2022": 17713, "FY2021": 19923.0}

RATIO_PAGES = {"FY2025": "5-6", "FY2024": "5-6", "FY2023": "7-8", "FY2022": "6-7", "FY2021": "6"}


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, f"SMBC BI basis, {unit}" if unit else "SMBC BI basis",
                         rows_data, p3_sources(RATIO_PAGES), note=note,
                         first_col_width=46, source_height=130)


metric("CET1 Capital", "£m (conv. from USD)", [("Common Equity Tier 1 (CET1) capital", gbp_spot(CET1_CAPITAL))])

metric("CET1 Ratio", "% of RWA", [
    ("Common Equity Tier 1 (CET1) ratio", {"FY2025": "17.1%", "FY2024": "19.5%", "FY2023": "17.8%", "FY2022": "16.3%", "FY2021": "16.7%"}),
])

metric("Tier 1 Capital", "£m (conv. from USD)", [("Tier 1 capital", gbp_spot(TIER1_CAPITAL))],
       note="Equal to CET1 capital in every year shown - SMBC BI holds no Additional Tier 1 (AT1) instruments.")

metric("Tier 1 Ratio", "% of RWA", [
    ("Tier 1 ratio", {"FY2025": "17.1%", "FY2024": "19.5%", "FY2023": "17.8%", "FY2022": "16.3%", "FY2021": "16.7%"}),
])

metric("Total Capital", "£m (conv. from USD)", [("Total capital", gbp_spot(TOTAL_CAPITAL))],
       note="Equal to CET1/Tier 1 capital in every year shown - SMBC BI holds no Tier 2 instruments either.")

metric("Total Capital Ratio", "% of RWA", [
    ("Total capital ratio", {"FY2025": "17.1%", "FY2024": "19.5%", "FY2023": "17.8%", "FY2022": "16.3%", "FY2021": "16.7%"}),
])

metric("Total RWAs", "£m (conv. from USD)", [("Total risk weighted exposure amount", gbp_spot(TOTAL_RWA))])

metric("Leverage Ratio", "£m (conv. from USD) / %", [
    ("Total exposure measure excluding claims on central banks", gbp_spot(LEV_EXPOSURE)),
    ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "10.1%", "FY2024": "14.8%", "FY2023": "13.8%", "FY2022": "12.4%", "FY2021": "7.7%"}),
    ("Leverage ratio including claims on central banks (%)", {"FY2025": "7.0%", "FY2024": "9.2%", "FY2023": "8.2%"}),
], note="FY2021 and FY2022 disclosed a single Basel III leverage ratio (7.7% / 12.4%) that does NOT exclude central "
        "bank claims - the 'excluding claims on central banks' UK framework was introduced only from the FY2022 "
        "report onward per that report's own commentary ('this was primarily due to the exclusion of qualifying "
        "claims on central banks from the leverage ratio exposures under the UK leverage ratio framework'). FY2021's "
        "and FY2022's figures are shown on the 'excluding' row for continuity, but are not on a like-for-like basis "
        "with FY2023 onward; no 'including claims on central banks' variant is separately disclosed for those two "
        "years.")

metric("LCR", "£m (conv. from USD) / %", [
    ("Total high quality liquid assets (HQLA), weighted value (average)", gbp_spot(LCR_HQLA)),
    ("Total net cash outflows (adjusted value)", gbp_spot(LCR_OUTFLOWS)),
    ("Liquidity coverage ratio (%)", {"FY2025": "160.1%", "FY2024": "155.6%", "FY2023": "145.4%", "FY2022": "136%", "FY2021": "145.0%"}),
])

metric("NSFR", "£m (conv. from USD) / %", [
    ("Total available stable funding", gbp_spot(NSFR_ASF)),
    ("Total required stable funding", gbp_spot(NSFR_RSF)),
    ("NSFR ratio (%)", {"FY2025": "127.2%", "FY2024": "141.8%", "FY2023": "142.4%", "FY2022": "133.5%", "FY2021": "135.5%"}),
])

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(RATIO_PAGES),
    per_note={"MREL Ratio": "No MREL disclosure of any kind (numeric or qualitative) appears in any of the 5 "
                             "years' Pillar 3 disclosures - SMBC BI does not appear to be subject to a disclosed "
                             "MREL requirement."},
)

# ---------------------------------------------------------------
# Interim Pillar 3 disclosures
# ---------------------------------------------------------------
# SMBC BI's financial year ends in March.  The official EMEA archive provides
# entity-level KM1 disclosures for June, September and December 2022-2025;
# March is the annual reporting point already represented by the metric sheets
# above.  Values below remain in SMBC BI's native USD millions because the
# interim source documents do not provide a defensible common GBP conversion
# basis for the three month-end dates.  Annual sheets retain their established
# GBP conversion methodology.
INTERIM_PERIODS = [
    ("2025 Q4", "Q4", "SMBC-BI-Pillar-3-Dec-25-v3.pdf", "Table 1: KM1, PDF p.5",
     "https://www.smbcgroup.com/emea/getmedia/0d5f0926-6436-48ef-a708-377fa7898591/SMBC-BI-Pillar-3-Dec-25-v3.pdf"),
    ("2025 Q3", "Q3", "SMBC-BI-Pillar-3-Sept-25.pdf", "Table 2.1: KM1, PDF p.5",
     "https://www.smbcgroup.com/emea/getmedia/bd6c0013-d139-4ba1-913c-96bbd44efe1f/SMBC-BI-Pillar-3-Sept-25.pdf"),
    ("2025 H1", "H1", "SMBC-BI-Pillar-3-June-25.pdf", "Table 1: KM1, PDF p.5",
     "https://www.smbcgroup.com/emea/getmedia/97fab1b7-9060-4cfe-93c7-09d3172181ac/SMBC-BI-Pillar-3-June-25.pdf"),
    ("2024 Q4", "Q4", "Pillar-3-Interim-Disclosure-December-2024-(SMBC-BI).pdf", "Table 1: KM1, PDF p.5",
     "https://www.smbcgroup.com/emea/getmedia/478b7c2d-76e0-4c07-b727-b00757a4636d/Pillar-3-Interim-Disclosure-December-2024-(SMBC-BI).pdf"),
    ("2024 Q3", "Q3", "Pillar-3-Interim-Disclosure-September-2024-(SMBC-BI).pdf", "Table 1: KM1, PDF p.5",
     "https://www.smbcgroup.com/emea/getmedia/7c046ae7-c39b-4e3a-83b6-789e9c0d305e/Pillar-3-Interim-Disclosure-September-2024-(SMBC-BI).pdf"),
    ("2024 H1", "H1", "Pillar-3-Interim-Disclosure-June-2024-(SMBC-BI).pdf", "Table 1: KM1, PDF p.5",
     "https://www.smbcgroup.com/emea/getmedia/5808b03a-874f-4d90-a062-10d94d98c9d8/Pillar-3-Interim-Disclosure-June-2024-(SMBC-BI).pdf"),
    ("2023 Q4", "Q4", "Pillar-3-Interim-Disclosure-December-2023-(SMBC-BI).pdf", "Table 1: KM1, PDF p.5",
     "https://www.smbcgroup.com/emea/getmedia/8c626609-cec1-44a5-b08b-227189f7e287/Pillar-3-Interim-Disclosure-December-2023-(SMBC-BI).pdf"),
    ("2023 Q3", "Q3", "Pillar-3-Interim-Disclosure-September-2023-(SMBC-BI).pdf", "Table 1: KM1, PDF p.4",
     "https://www.smbcgroup.com/emea/getmedia/e2329270-9c6b-4707-be71-48a96b030b7b/Pillar-3-Interim-Disclosure-September-2023-(SMBC-BI).pdf"),
    ("2023 H1", "H1", "Pillar-3-Interim-Disclosure-June-2023-(SMBC-BI).pdf", "Table 1: KM1, PDF p.5",
     "https://www.smbcgroup.com/emea/getmedia/db3289f7-2020-4cfe-835c-4b0ef5eac4aa/Pillar-3-Interim-Disclosure-June-2023-(SMBC-BI).pdf"),
    ("2022 Q4", "Q4", "Pillar-3-Interim-Disclosure-December-2022-(SMBC-BI).pdf", "Table 1: KM1, PDF p.5",
     "https://www.smbcgroup.com/emea/getmedia/ee8d7d6b-5d17-4d82-9bd8-d52369fa4e45/Pillar-3-Interim-Disclosure-December-2022-(SMBC-BI).pdf"),
    ("2022 Q3", "Q3", "Pillar-3-Interim-Disclosure-September-2022-(SMBC-BI).pdf", "Table 1: KM1, PDF p.4",
     "https://www.smbcgroup.com/emea/getmedia/cd804340-56b8-4410-8bab-2b2f733729cd/Pillar-3-Interim-Disclosure-September-2022-(SMBC-BI).pdf"),
    ("2022 H1", "H1", "Pillar-3-Interim-Disclosure-June-2022-(SMBC-BI).pdf", "Table 1: KM1, PDF p.5",
     "https://www.smbcgroup.com/emea/getmedia/4490ceb5-1ff3-4cfb-84ac-93a8049d8cb5/Pillar-3-Interim-Disclosure-June-2022-(SMBC-BI).pdf"),
]

# Most-recent-first and aligned with INTERIM_PERIODS above.  All amount rows
# are USDm; ratios are percentage points as reported.
INTERIM_VALUES = {
    "CET1 Capital": [5761, 5771, 5780, 5450, 5465, 5469, 5077, 5084, 5077, 4878, 4871, 4864],
    "Tier 1 Capital": [5761, 5771, 5780, 5450, 5465, 5469, 5077, 5084, 5077, 4878, 4871, 4864],
    "Total Capital": [5761, 5771, 5780, 5450, 5465, 5469, 5077, 5084, 5077, 4878, 4871, 4864],
    "Total RWAs": [34723, 32117, 34299, 32113, 30156, 28591, 31432, 29061, 29791, 28657, 27759, 28233],
    "CET1 Ratio": ["16.6%", "18.0%", "16.9%", "17.0%", "18.1%", "19.1%", "16.2%", "17.5%", "17.0%", "17.0%", "17.5%", "17.2%"],
    "Tier 1 Ratio": ["16.6%", "18.0%", "16.9%", "17.0%", "18.1%", "19.1%", "16.2%", "17.5%", "17.0%", "17.0%", "17.5%", "17.2%"],
    "Total Capital Ratio": ["16.6%", "18.0%", "16.9%", "17.0%", "18.1%", "19.1%", "16.2%", "17.5%", "17.0%", "17.0%", "17.5%", "17.2%"],
    "Leverage Exposure": [74964, 64993, 63790, 59429, 40131, 36189, 42439, 37292, 36456, 38261, 42903, 38634],
    "Leverage Ratio": ["7.7%", "8.9%", "9.1%", "9.2%", "13.6%", "15.1%", "12.0%", "13.6%", "13.9%", "12.7%", "11.4%", "12.6%"],
    "LCR HQLA": [28993, 27479, 26296, 24939, 25369, 25342, 26810, 25074, 22986, 28599, 26812, 27846],
    "LCR Net Outflows": [19099, 18026, 16850, 15384, 15651, 15855, 16971, 16237, 15301, 19175, 16934, 19730],
    "LCR Ratio": ["151.8%", "152.4%", "156.1%", "162.1%", "162.1%", "159.8%", "158.0%", "154.4%", "150.2%", "149.1%", "158.3%", "141.1%"],
    "NSFR ASF": [26054, 24586, 23735, 22805, 23060, 23516, 23890, 23965, 23210, 24228, 24965, 22865],
    "NSFR RSF": [20317, 19844, 19020, 16987, 16693, 16735, 16939, 16870, 16613, 17256, 16274, 17191],
    "NSFR Ratio": ["128.2%", "123.9%", "124.8%", "134.3%", "138.1%", "140.5%", "141.0%", "142.1%", "139.7%", "140.4%", "153.4%", "133.0%"],
}

interim_headers = ["Period", "Disclosure type", "Metric", "Value", "Unit", "Basis", "Source document", "Page / table"]
interim_rows = []
interim_hyperlinks = {}
for metric_name, values in INTERIM_VALUES.items():
    unit = "%" if "Ratio" in metric_name else "USDm"
    if metric_name in {"Leverage Exposure", "LCR HQLA", "LCR Net Outflows", "NSFR ASF", "NSFR RSF"}:
        unit = "USDm"
    for idx, (period, disclosure_type, document, page, url) in enumerate(INTERIM_PERIODS):
        interim_rows.append((period, disclosure_type, metric_name, values[idx], unit,
                             "SMBC Bank International plc entity-level; native USD reporting",
                             document, page))
        interim_hyperlinks[(len(interim_rows) - 1, 6)] = url

bw.add_wide_interim_sheet(
    "Interim Pillar 3",
    headers=interim_headers,
    rows=interim_rows,
    title="SMBC Bank International plc — Interim Pillar 3",
    subtitle="Entity-level KM1 observations for non-annual quarter ends; amounts are native USDm and ratios are as reported.",
    note="The March year-end observations remain on the annual metric sheets. The official archive provides June, September and December disclosures for 2022-2025. Direct source-document hyperlinks are attached to every row. Interim amounts are intentionally not converted to GBP because a common, documented month-end conversion series is not part of the source methodology used for the annual workbook.",
    widths=[14, 16, 24, 14, 10, 48, 58, 25],
    hyperlink_cells=interim_hyperlinks,
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", gbp_avg(NET_OPERATING)),
        ("Net cash from/(used in) investing activities", gbp_avg(NET_INVESTING)),
        ("Net cash from/(used in) financing activities", gbp_avg(NET_FINANCING)),
        ("Cash and cash equivalents at 31 March", cash_end_gbp),
    ],
    cash_flow_unit="£m (conv. from USD)",
    ratios=[
        ("CET1 Ratio", {"FY2025": "17.1%", "FY2024": "19.5%", "FY2023": "17.8%", "FY2022": "16.3%", "FY2021": "16.7%"}),
        ("Tier 1 Ratio", {"FY2025": "17.1%", "FY2024": "19.5%", "FY2023": "17.8%", "FY2022": "16.3%", "FY2021": "16.7%"}),
        ("Total Capital Ratio", {"FY2025": "17.1%", "FY2024": "19.5%", "FY2023": "17.8%", "FY2022": "16.3%", "FY2021": "16.7%"}),
        ("Leverage Ratio", {"FY2025": "10.1%", "FY2024": "14.8%", "FY2023": "13.8%", "FY2022": "12.4%", "FY2021": "7.7%"}),
        ("LCR", {"FY2025": "160.1%", "FY2024": "155.6%", "FY2023": "145.4%", "FY2022": "136%", "FY2021": "145.0%"}),
        ("NSFR", {"FY2025": "127.2%", "FY2024": "141.8%", "FY2023": "142.4%", "FY2022": "133.5%", "FY2021": "135.5%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing. ALL £ figures in this "
         "workbook are converted from SMBC Bank International plc's native USD reporting - see the Cash Flow "
         "Statement sheet's source note for the full FX methodology and exact rates used. Ratios (%) are shown "
         "exactly as reported in USD and were not converted.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/SMBC FINANCIALS.xlsx")
