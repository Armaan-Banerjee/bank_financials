import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# PILLAR-3-ONLY WORKBOOK: Bank Mandiri (Europe) Limited (company 03793679, FRN 204424)
# is a qualifying entity under FRS 101 and takes the "presentation of a cash-flow
# statement" (IAS 7) disclosure exemption every year - explicitly stated in Note 1.4
# "Disclosure Exemptions" of its FY2025 Annual Report, deferring to the accounts of
# its parent, PT Bank Mandiri (Persero) Tbk. Confirmed as a standing feature by
# checking both the FY2020 filing (earliest available, filed 2021) and the FY2025
# filing (most recent) - no Contents-page entry for a cash flow statement in either,
# 5 years apart. Follows the BNY Mellon International / ABC International Bank
# precedent: 13-sheet structure, Cash Flow Statement sheet documents the exemption
# instead of line items, Overview sheet omits the cash-flow chart.
#
# The Bank's functional currency is US Dollars (Note 1.2). No dedicated Pillar 3
# document exists - the only capital/liquidity disclosures found are a narrative
# paragraph + "Key Performance Indicator" table in the Strategic Report of each
# Annual Report, giving only a combined Total Capital Ratio (labelled "Capital
# Adequacy Ratio", Own Funds / Total RWA - no separate CET1/Tier 1 breakdown exists
# anywhere), LCR, NSFR, and total "regulatory capital resources" (Own Funds, $m).
# This KPI table format was only introduced from the FY2023 Annual Report onward
# (FY2022's own report has a KPI table with no capital/liquidity rows, and no
# capital/liquidity narrative was found in its Strategic Report or Directors'
# Report) - FY2022's figures come from FY2023's own comparative column instead.
# FY2021 could not be found in any source checked (FY2022 filing has no numeric
# capital/liquidity disclosure at all) - left blank, not estimated.

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, calendar year-end (31 December)
YEAR_LABEL = {y: y for y in YEARS}

# ---------------------------------------------------------------
# FX conversion (functional currency USD; converting to £ per this project's
# established FX methodology - see build_zenith.py / build_smbc.py precedent).
# Only point-in-time (stock) figures need conversion here - there's no cash flow
# statement, so no average/flow rate is needed.
# Rates are Bank of England GBP/USD spot via poundsterlinglive.com's published
# archive, £1 = $X, same table used throughout this project's USD-reporting banks.
# ---------------------------------------------------------------
FX_SPOT = {
    "FY2021": 1.3728,  # 31 Dec 2021
    "FY2022": 1.2097,  # 30 Dec 2022 (31st was a Saturday)
    "FY2023": 1.2732,  # 29 Dec 2023 (31st was a Sunday)
    "FY2024": 1.2515,  # 31 Dec 2024
    "FY2025": 1.3448,  # 31 Dec 2025
}

# Calendar-year average GBP/USD spot rate (£1 = $X), computed from the daily
# Bank of England spot series published at poundsterlinglive.com's historical
# archive (~250 trading days per year averaged) - used for flow figures
# (P&L, equity movements) per this project's established FX methodology
# (see build_smbc.py precedent: spot for stocks, average for flows).
FX_AVG = {
    "FY2021": 1.3756,
    "FY2022": 1.2365,
    "FY2023": 1.2434,
    "FY2024": 1.2780,
    "FY2025": 1.3183,
}


def stock(usd):
    """Point-in-time (capital/RWA/balance sheet) figures, £'000, at that year's period-end spot rate."""
    return {y: round(v / FX_SPOT[y] / 1000, 0) for y, v in usd.items()}


def flow(usd):
    """Flow (P&L/equity-movement) figures, £'000, at that year's calendar-year average rate."""
    return {y: round(v / FX_AVG[y] / 1000, 0) for y, v in usd.items()}


FY2025_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/03793679/filing-history/MzUyODU0NjIyMmFkaXF6a2N4/document?format=pdf&download=0"
FY2024_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/03793679/filing-history/MzQ2ODc4NDgyMGFkaXF6a2N4/document?format=pdf&download=0"
FY2023_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/03793679/filing-history/MzQyNjk5Njk1M2FkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "ENTITY NOTE: Bank Mandiri (Europe) Limited (company 03793679, FRN 204424, incorporated 22 June 1999 as "
    "'Exitmode Limited', renamed 26 July 1999) is a wholly-owned UK subsidiary of PT Bank Mandiri (Persero) Tbk, "
    "Indonesia's largest bank by assets. All figures below are on the Bank's own entity-level basis - it has no "
    "subsidiaries of its own."
)

EXEMPTION_NOTE = (
    "FRS 101 CASH-FLOW EXEMPTION: the FY2025 Annual Report states (Note 1.4, Disclosure Exemptions): \"As permitted "
    "by FRS 101, the Company has taken advantage of the disclosure exemptions available under that standard "
    "concerning the presentation of comparative information in respect of certain assets, presentation of a "
    "cash-flow statement, standards not yet effective, impairment of assets and related party transactions between "
    "two or more wholly owned members of the group. Where required, equivalent disclosures are given in the "
    "accounts of PT Bank Mandiri (Persero) Tbk\", and explicitly lists 'IAS 7 Statement of Cash Flows and related "
    f"notes' among the exemptions applied - Bank Mandiri (Europe) Limited Annual Report FY2025, p.24-25 - "
    f"{FY2025_AR_URL}. No Statement of Cash Flows appears in the Contents page of either the FY2020 (earliest "
    "available Companies House filing) or FY2025 (most recent) accounts, confirming this is a standing structural "
    "feature across the entity's history, not a one-off. Per the project's established policy for this exemption "
    "(see The Bank of New York Mellon (International) Limited / ABC International Bank plc), this workbook is "
    "built as a PILLAR-3-ONLY variant: the capital/liquidity metrics that are disclosed are populated below, but no "
    "cash flow figures exist to show. See the Overview sheet for the equivalent treatment there."
)

CASH_FLOW_SOURCES = ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE

NOT_DISCLOSED_NOTE = (
    "No dedicated Pillar 3 document is published by this entity - the only capital/liquidity disclosures found are "
    "a narrative paragraph and Key Performance Indicator table in each Annual Report's Strategic Report, which give "
    "only a single combined Total Capital Ratio (no CET1/Tier 1 breakdown), LCR, and NSFR. This metric is not "
    "disclosed in any form found in any of the 4 Annual Reports (FY2022-FY2025) or the FY2020 filing checked."
)


def p3_sources(extra=""):
    return (
        "Sources - Bank Mandiri (Europe) Limited (figures reported in US Dollars, converted to £ at the Bank of "
        "England GBP/USD spot rate as at each fiscal year-end - see FX conversion note below; % ratios shown "
        "exactly as reported, not converted):\n"
        f"FY2025 & FY2024: Bank Mandiri (Europe) Limited Annual Report FY2025, Strategic Report \"Key Performance "
        f"Indicator\" table, p.6 - {FY2025_AR_URL}\n"
        f"FY2024 (as originally reported) & FY2023: Bank Mandiri (Europe) Limited Annual Report FY2024, Strategic "
        f"Report \"Key Performance Indicator\" table, p.6 - {FY2024_AR_URL}\n"
        f"FY2023 (as originally reported) & FY2022: Bank Mandiri (Europe) Limited Annual Report FY2023, Strategic "
        f"Report \"Key Performance Indicator\" table, p.6 - {FY2023_AR_URL}\n"
        "FX rates (£1 = $X, Bank of England spot via poundsterlinglive.com): 31 Dec 2022 1.2097; 29 Dec 2023 "
        "1.2732 (31st was a Sunday); 31 Dec 2024 1.2515; 31 Dec 2025 1.3448.\n"
        + (extra + "\n" if extra else "")
        + "FY2022's Total Capital Ratio/LCR/NSFR are sourced from the FY2023 Annual Report's own comparative column "
          "- the FY2022 Annual Report's own KPI table and Strategic Report do not include these figures at all "
          "(this KPI format was only introduced from the FY2023 report onward). FY2021 could not be found in any "
          "form (numeric or narrative) in the FY2022 Annual Report - left blank, not estimated."
    )


bw = BankWorkbook(bank_name="Bank Mandiri (Europe) Limited", years=YEARS, year_label=YEAR_LABEL, header_color="8B0000")

# ---------------------------------------------------------------
# ST- wayfinder map rollout (batch ST-011): Balance Sheet, Profit & Loss,
# Statement of Changes in Equity, Asset Quality, RWA Breakdown.
#
# All 5 years (FY2021-FY2025) were sourced by visually transcribing this
# entity's own scanned/image-only Companies House statutory accounts filings
# (fy2025.pdf, fy2024.pdf, fy2023.pdf, fy2022.pdf - all confirmed image-only
# via pdf_tools.py scan, 0 text blocks per page) via pdf_tools.py render +
# visual reading, per the project's established OCR/visual-transcription
# approach for scanned filings. FY2025's own report gives FY2025/FY2024;
# FY2024's own report gives FY2024/FY2023 (used to cross-check FY2024, which
# matched exactly); FY2023's own report gives FY2023/FY2022 (cross-checked
# FY2023, matched exactly); FY2022's own report gives FY2022/FY2021
# (cross-checked FY2022, matched exactly). Figures reported in US$'000
# (entity's functional currency), converted to £'000 at Bank of England
# GBP/USD spot rate for point-in-time (balance sheet, equity closing/opening
# balances) figures and calendar-year average rate for flow (P&L, equity
# in-year movement) figures - see FX_SPOT/FX_AVG/stock()/flow() above and
# the SMBC Bank International precedent this follows.
ST_ENTITY_NOTE = ENTITY_NOTE + (
    "\n\nAll years (FY2021-FY2025) sourced from this entity's own Companies House statutory accounts filings "
    "(all scanned/image-only PDFs - no text layer - visually transcribed page-by-page): Annual Report FY2025 "
    f"(Profit and Loss Account p.20, Statement of Comprehensive Income p.21, Balance Sheet p.22, Statement of "
    f"Changes in Equity p.23) - {FY2025_AR_URL}; Annual Report FY2024 (same page layout, FY2024/FY2023 columns) "
    f"- {FY2024_AR_URL}; Annual Report FY2023 (same page layout, FY2023/FY2022 columns) - {FY2023_AR_URL}; "
    "Annual Report FY2022 (Profit and Loss Account p.18, Statement of Comprehensive Income p.19, Balance Sheet "
    "p.20, Statement of Changes in Equity p.21, FY2022/FY2021 columns) - Companies House filing history, company "
    "03793679, accounts made up to 31 December 2022. Each year's own comparative column was cross-checked against "
    "the following year's report where both exist - all matched exactly, no discrepancies found.\n\n"
    "FX conversion: £1 = $X, Bank of England spot via poundsterlinglive.com. Spot rates (period-end, used for "
    "balance sheet and equity opening/closing balances): 31 Dec 2021 1.3728; 31 Dec 2022 1.2097 (30 Dec, 31st was "
    "a Saturday); 31 Dec 2023 1.2732 (29 Dec, 31st was a Sunday); 31 Dec 2024 1.2515; 31 Dec 2025 1.3448. Average "
    "rates (calendar-year mean of ~250 daily spot quotes, used for P&L and in-year equity movements): FY2021 "
    "1.3756; FY2022 1.2365; FY2023 1.2434; FY2024 1.2780; FY2025 1.3183."
)

BALANCE_SHEET_USD = {
    "Cash and cash equivalent": {"FY2025": 3_622_000, "FY2024": 14_000_000, "FY2023": 17_781_000, "FY2022": 30_448_000, "FY2021": 31_508_000},
    "Loan and advances to banks": {"FY2025": 29_404_000, "FY2024": 30_509_000, "FY2023": 34_531_000, "FY2022": 37_011_000, "FY2021": 19_985_000},
    "Loan and advances to customers": {"FY2025": 131_430_000, "FY2024": 88_010_000, "FY2023": 87_428_000, "FY2022": 74_065_000, "FY2021": 59_912_000},
    "Debt securities": {"FY2025": 132_298_000, "FY2024": 128_310_000, "FY2023": 118_990_000, "FY2022": 99_423_000, "FY2021": 71_107_000},
    "Tangible fixed assets": {"FY2025": 14_000, "FY2024": 14_000, "FY2023": 2_000, "FY2022": 6_000, "FY2021": 15_000},
    "Intangible fixed assets": {"FY2025": 179_000, "FY2024": 187_000, "FY2023": 3_000, "FY2022": 3_000, "FY2021": 16_000},
    "Right of use assets": {"FY2025": 106_000, "FY2024": 235_000, "FY2023": 381_000, "FY2022": 499_000, "FY2021": 37_000},
    "Other assets, prepayments and accrued income": {"FY2025": 1_296_000, "FY2024": 507_000, "FY2023": 448_000, "FY2022": 442_000, "FY2021": 776_000},
    "Total assets": {"FY2025": 298_349_000, "FY2024": 261_772_000, "FY2023": 259_564_000, "FY2022": 241_897_000, "FY2021": 183_356_000},
    "Deposit from banks": {"FY2025": 236_320_000, "FY2024": 201_729_000, "FY2023": 189_826_000, "FY2022": 172_796_000, "FY2021": 113_533_000},
    "Customer accounts": {"FY2025": 4_190_000, "FY2024": 4_298_000, "FY2023": 15_674_000, "FY2022": 17_526_000, "FY2021": 15_862_000},
    "Other liabilities, accruals and deferred income": {"FY2025": 953_000, "FY2024": 1_150_000, "FY2023": 1_234_000, "FY2022": 1_195_000, "FY2021": 1_279_000},
    "Lease liability": {"FY2025": 106_000, "FY2024": 235_000, "FY2023": 381_000, "FY2022": 499_000, "FY2021": 37_000},
    "Current tax liability": {"FY2025": 296_000, "FY2024": 106_000, "FY2023": 126_000, "FY2022": 167_000, "FY2021": 69_000},
    "Deferred tax liability": {"FY2022": 0, "FY2021": 87_000},  # nil FY2023-25; blank FY2022 shown as "-" (nil) in source
    "Total liabilities excluding shareholders' funds": {"FY2025": 241_865_000, "FY2024": 207_518_000, "FY2023": 207_241_000, "FY2022": 192_183_000, "FY2021": 130_867_000},
    "Called up share capital": {"FY2025": 49_000_000, "FY2024": 49_000_000, "FY2023": 49_000_000, "FY2022": 49_000_000, "FY2021": 49_000_000},
    "Capital reserve": {"FY2025": 11_496_000, "FY2024": 11_496_000, "FY2023": 11_496_000, "FY2022": 11_496_000, "FY2021": 11_496_000},
    "Revaluation reserve": {"FY2025": 637_000, "FY2024": -317_000, "FY2023": -1_189_000, "FY2022": -2_959_000, "FY2021": 425_000},
    "Profit and loss account": {"FY2025": -4_649_000, "FY2024": -5_925_000, "FY2023": -6_984_000, "FY2022": -7_823_000, "FY2021": -8_432_000},
    "Total shareholders' funds": {"FY2025": 56_484_000, "FY2024": 54_254_000, "FY2023": 52_323_000, "FY2022": 49_714_000, "FY2021": 52_489_000},
    "Total liabilities and shareholders' funds": {"FY2025": 298_349_000, "FY2024": 261_772_000, "FY2023": 259_564_000, "FY2022": 241_897_000, "FY2021": 183_356_000},
}
BS = {k: stock(v) for k, v in BALANCE_SHEET_USD.items()}

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalent", BS["Cash and cash equivalent"]),
    ("DATA", "Loan and advances to banks", BS["Loan and advances to banks"]),
    ("DATA", "Loan and advances to customers", BS["Loan and advances to customers"]),
    ("DATA", "Debt securities", BS["Debt securities"]),
    ("DATA", "Tangible fixed assets", BS["Tangible fixed assets"]),
    ("DATA", "Intangible fixed assets", BS["Intangible fixed assets"]),
    ("DATA", "Right of use assets", BS["Right of use assets"]),
    ("DATA", "Other assets, prepayments and accrued income", BS["Other assets, prepayments and accrued income"]),
    ("TOTAL", "Total assets", BS["Total assets"]),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposit from banks", BS["Deposit from banks"]),
    ("DATA", "Customer accounts", BS["Customer accounts"]),
    ("DATA", "Other liabilities, accruals and deferred income", BS["Other liabilities, accruals and deferred income"]),
    ("DATA", "Lease liability", BS["Lease liability"]),
    ("DATA", "Current tax liability", BS["Current tax liability"]),
    ("DATA", "Deferred tax liability", BS["Deferred tax liability"]),
    ("TOTAL", "Total liabilities excluding shareholders' funds", BS["Total liabilities excluding shareholders' funds"]),
    ("SECTION", "Shareholders' funds", {}),
    ("DATA", "Called up share capital", BS["Called up share capital"]),
    ("DATA", "Capital reserve", BS["Capital reserve"]),
    ("DATA", "Revaluation reserve", BS["Revaluation reserve"]),
    ("DATA", "Profit and loss account", BS["Profit and loss account"]),
    ("TOTAL", "Total shareholders' funds — equity interests", BS["Total shareholders' funds"]),
    ("TOTAL", "Total liabilities and shareholders' funds", BS["Total liabilities and shareholders' funds"]),
]

BALANCE_SHEET_SOURCES = (
    "Sources — Bank Mandiri (Europe) Limited's own Balance Sheet, converted from USD to £'000 at the Bank of "
    "England GBP/USD spot rate as at each fiscal year-end (point-in-time figures — see FX conversion note below):\n"
    + ST_ENTITY_NOTE
)

bw.add_balance_sheet_sheet(
    title="Bank Mandiri (Europe) Limited — Balance Sheet",
    subtitle="£'000, converted from USD — see source note for FX methodology and rates used. Entity-level basis (no subsidiaries).",
    rows=balance_sheet_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=52,
    source_height=260,
)

INCOME_STATEMENT_USD = {
    "Interest receivable": {"FY2025": 13_124_000, "FY2024": 13_430_000, "FY2023": 11_175_000, "FY2022": 6_198_000, "FY2021": 4_431_000},
    "Interest payable": {"FY2025": -8_080_000, "FY2024": -8_683_000, "FY2023": -6_790_000, "FY2022": -2_546_000, "FY2021": -928_000},
    "Net interest income": {"FY2025": 5_044_000, "FY2024": 4_747_000, "FY2023": 4_385_000, "FY2022": 3_652_000, "FY2021": 3_503_000},
    "Fees and commissions receivable": {"FY2025": 311_000, "FY2024": 446_000, "FY2023": 243_000, "FY2022": 205_000, "FY2021": 246_000},
    "Other operating income": {"FY2025": 461_000, "FY2024": 184_000, "FY2023": 378_000, "FY2022": 472_000, "FY2021": 90_000},
    "Total operating income": {"FY2025": 5_816_000, "FY2024": 5_377_000, "FY2023": 5_006_000, "FY2022": 4_329_000, "FY2021": 3_839_000},
    "Administrative expenses": {"FY2025": -4_072_000, "FY2024": -3_963_000, "FY2023": -3_328_000, "FY2022": -3_269_000, "FY2021": -3_012_000},
    "Depreciation and amortisation": {"FY2025": -199_000, "FY2024": -183_000, "FY2023": -150_000, "FY2022": -168_000, "FY2021": -230_000},
    "Loan impairment losses — write-back/(charge)": {"FY2025": 27_000, "FY2024": 22_000, "FY2023": -427_000, "FY2022": -116_000, "FY2021": -123_000},
    "Profit on ordinary activities before tax": {"FY2025": 1_572_000, "FY2024": 1_253_000, "FY2023": 1_101_000, "FY2022": 776_000, "FY2021": 474_000},
    "Taxation (charge)/credit": {"FY2025": -296_000, "FY2024": -194_000, "FY2023": -262_000, "FY2022": -167_000, "FY2021": -98_000},
    "Profit on ordinary activities after tax": {"FY2025": 1_276_000, "FY2024": 1_059_000, "FY2023": 839_000, "FY2022": 609_000, "FY2021": 376_000},
    "Change in fair value of investments measured at FVOCI": {"FY2025": 954_000, "FY2024": 872_000, "FY2023": 1_770_000, "FY2022": -3_384_000, "FY2021": -938_000},
    "Deferred tax credit on FVTOCI financial instruments": {"FY2021": 178_000},  # nil/not disclosed other years
    "Effects of changes in tax rate": {"FY2021": -34_000},  # nil/not disclosed other years
    "Total comprehensive income/(loss) for the period": {"FY2025": 2_230_000, "FY2024": 1_931_000, "FY2023": 2_609_000, "FY2022": -2_775_000, "FY2021": -418_000},
}
IS_USD = INCOME_STATEMENT_USD
IS = {k: flow(v) for k, v in IS_USD.items()}

income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable", IS["Interest receivable"]),
    ("DATA", "Interest payable", IS["Interest payable"]),
    ("TOTAL", "Net interest income", IS["Net interest income"]),
    ("DATA", "Fees and commissions receivable", IS["Fees and commissions receivable"]),
    ("DATA", "Other operating income", IS["Other operating income"]),
    ("TOTAL", "Total operating income", IS["Total operating income"]),
    ("SECTION", "Expenses", {}),
    ("DATA", "Administrative expenses", IS["Administrative expenses"]),
    ("DATA", "Depreciation and amortisation", IS["Depreciation and amortisation"]),
    ("DATA", "Loan impairment losses — write-back/(charge)", IS["Loan impairment losses — write-back/(charge)"]),
    ("TOTAL", "Profit on ordinary activities before tax", IS["Profit on ordinary activities before tax"]),
    ("DATA", "Taxation (charge)/credit", IS["Taxation (charge)/credit"]),
    ("TOTAL", "Profit on ordinary activities after tax", IS["Profit on ordinary activities after tax"]),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Change in fair value of investments measured at FVOCI", IS["Change in fair value of investments measured at FVOCI"]),
    ("DATA", "Deferred tax credit on FVTOCI financial instruments", IS["Deferred tax credit on FVTOCI financial instruments"]),
    ("DATA", "Effects of changes in tax rate", IS["Effects of changes in tax rate"]),
    ("TOTAL", "Total comprehensive income/(loss) for the period", IS["Total comprehensive income/(loss) for the period"]),
]

INCOME_STATEMENT_SOURCES = (
    "Sources — Bank Mandiri (Europe) Limited's own Profit and Loss Account and Statement of Comprehensive Income, "
    "converted from USD to £'000 at the Bank of England GBP/USD calendar-year average spot rate (flow figures — "
    "see FX conversion note below):\n"
    + ST_ENTITY_NOTE
    + "\n\nFY2022 and FY2021's OCI detail (deferred tax credit on FVTOCI, effects of tax rate changes) is disclosed "
      "only for FY2021 in the FY2022 Annual Report's own comparative column — FY2022's own OCI detail below the "
      "fair-value-change line was reported as nil/not itemised. Total comprehensive income/(loss) is the one row "
      "genuinely comparable and populated across all 5 years."
)

bw.add_income_statement_sheet(
    title="Bank Mandiri (Europe) Limited — Profit and Loss Account and Statement of Comprehensive Income",
    subtitle="£'000, converted from USD — see source note for FX methodology and rates used. Entity-level basis (no subsidiaries).",
    rows=income_statement_rows,
    sources_text=INCOME_STATEMENT_SOURCES,
    first_col_width=58,
    source_height=280,
)

EQUITY_HEADERS = ["Share capital", "Capital reserve", "Revaluation reserve", "Profit and loss account", "Total shareholders' funds"]

# Build each movement row directly in £'000 (inputs are US$'000), using spot rate for balance rows
# (opening/closing — point-in-time) and average rate for movement rows
# (in-year flows), consistent with BS/IS above.
def bal(usd_thousands, year):
    return tuple(round(v / FX_SPOT[year], 0) if v is not None else None for v in usd_thousands)

def mov(usd_thousands, year):
    return tuple(round(v / FX_AVG[year], 0) if v is not None else None for v in usd_thousands)

# Opening ("At 1 January Y") rows are the SAME point in time as the prior
# year's "At 31 December" row (31 December Y-1) - both must therefore use
# that same 31-December spot rate (FX_SPOT["FY"+str(Y-1)]), not year Y's own
# rate, or the roll-forward would show a false discontinuity purely from an
# FX-rate mismatch. Caught and fixed this exact bug before finalizing.
#
# Even with that fix, opening (prior year's spot rate) + this year's
# movements (this year's AVERAGE rate) does not exactly equal closing (this
# year's own spot rate) in £ terms, even though it does exactly in $ terms -
# because three different GBP/USD rates are in play across one year's
# block. This is a real currency-translation artifact (the same phenomenon
# SMBC Bank International's Cash Flow Statement handles with an explicit
# "Effect of GBP/USD translation" line - see build_smbc.py), not a data
# error. An explicit "FX translation effect on equity, net" row (Total
# column only - there is no currency-translation-reserve component in this
# entity's own accounts to attribute it to) absorbs the gap so opening +
# movements + this line = closing exactly, each year.
FX_TRANSLATION_EFFECT = {"FY2022": 5105, "FY2023": -2099, "FY2024": 744, "FY2025": -3041}  # closing - opening - Total comprehensive income, £'000, per year

equity_changes_rows = [
    ("TOTAL", "At 1 January 2022", bal((49000, 11496, 425, -8432, 52489), "FY2021")),
    ("DATA", "Decrease in fair value of debt securities", mov((None, None, -3384, None, -3384), "FY2022")),
    ("DATA", "Profit for the year", mov((None, None, None, 609, 609), "FY2022")),
    ("DATA", "FX translation effect on equity, net (£'000, see FX conversion note)", (None, None, None, None, FX_TRANSLATION_EFFECT["FY2022"])),
    ("TOTAL", "At 31 December 2022", bal((49000, 11496, -2959, -7823, 49714), "FY2022")),
    ("TOTAL", "At 1 January 2023", bal((49000, 11496, -2959, -7823, 49714), "FY2022")),
    ("DATA", "Increase in fair value of debt securities", mov((None, None, 1770, None, 1770), "FY2023")),
    ("DATA", "Profit for the year", mov((None, None, None, 839, 839), "FY2023")),
    ("DATA", "FX translation effect on equity, net (£'000, see FX conversion note)", (None, None, None, None, FX_TRANSLATION_EFFECT["FY2023"])),
    ("TOTAL", "At 31 December 2023", bal((49000, 11496, -1189, -6984, 52323), "FY2023")),
    ("TOTAL", "At 1 January 2024", bal((49000, 11496, -1189, -6984, 52323), "FY2023")),
    ("DATA", "Increase in fair value of debt securities", mov((None, None, 872, None, 872), "FY2024")),
    ("DATA", "Profit for the year", mov((None, None, None, 1059, 1059), "FY2024")),
    ("DATA", "FX translation effect on equity, net (£'000, see FX conversion note)", (None, None, None, None, FX_TRANSLATION_EFFECT["FY2024"])),
    ("TOTAL", "At 31 December 2024", bal((49000, 11496, -317, -5925, 54254), "FY2024")),
    ("TOTAL", "At 1 January 2025", bal((49000, 11496, -317, -5925, 54254), "FY2024")),
    ("DATA", "Increase in fair value of debt securities", mov((None, None, 954, None, 954), "FY2025")),
    ("DATA", "Profit for the year", mov((None, None, None, 1276, 1276), "FY2025")),
    ("DATA", "FX translation effect on equity, net (£'000, see FX conversion note)", (None, None, None, None, FX_TRANSLATION_EFFECT["FY2025"])),
    ("TOTAL", "At 31 December 2025", bal((49000, 11496, 637, -4649, 56484), "FY2025")),
]

EQUITY_CHANGES_SOURCES = (
    "Sources — Bank Mandiri (Europe) Limited's own Statement of Change in Equity, converted from USD to £'000 "
    "(balance/opening/closing rows at that date's spot rate; movement rows at that year's average rate — see FX "
    "conversion note below):\n"
    + ST_ENTITY_NOTE
    + "\n\nFY2021's opening balance (1 January 2021) was not located this session — the FY2021 movements "
      "(profit £376k, FVOCI change $(938)k, deferred tax credit $178k, tax-rate-change effect $(34)k, giving total "
      "comprehensive loss $(418)k per that year's own Statement of Comprehensive Income) are disclosed via the "
      "FY2022 Annual Report's comparative column, but the FY2022 report does not itself show a 1 January 2021 "
      "opening equity roll-forward row — only the FY2021 P&L/OCI flows and the 31 December 2021 closing balance "
      "(= 1 January 2022 opening balance, £52,489k / $52,489k, shown above) are available without the FY2021 "
      "Annual Report itself, which was not sourced this session. This sheet therefore begins at 1 January 2022, "
      "not 1 January 2021 — a narrower start than the Balance Sheet/P&L sheets' FY2021 column, which come "
      "straight off each report's own comparative column and don't need an opening equity bridge.\n\n"
      "FX TRANSLATION EFFECT: each year's opening balance is converted at the PRIOR year-end's spot rate (the same "
      "point in time as that row, so opening always exactly equals the prior year's closing row); each year's "
      "movement rows (FVOCI change, profit) are converted at that year's AVERAGE rate, consistent with the "
      "Profit & Loss sheet; each year's closing balance is converted at that year's OWN year-end spot rate. Because "
      "three different GBP/USD rates are used within one year's block, opening + movements does not exactly equal "
      "closing in £ terms even though it does exactly in $ terms (Bank Mandiri Europe's underlying accounts have "
      "no currency-translation-reserve component to attribute this to, unlike a genuine multi-currency group). The "
      "explicit 'FX translation effect on equity, net' row absorbs this gap so the roll-forward ties exactly every "
      "year — it is a pure artefact of £ conversion, not a real equity movement, the same treatment SMBC Bank "
      "International plc's Cash Flow Statement sheet uses for its analogous 'Effect of GBP/USD translation' line."
)

bw.add_equity_changes_sheet(
    title="Bank Mandiri (Europe) Limited — Statement of Change in Equity",
    subtitle="£'000, converted from USD — see source note for FX methodology and rates used. Chronological, oldest to newest. Starts 1 January 2022 — see source note.",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQUITY_CHANGES_SOURCES,
    first_col_width=32,
    source_height=280,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (exemption note in place of line items)
# ---------------------------------------------------------------
rows = [
    ("SECTION", "No Statement of Cash Flows is published by this entity in any year", {}),
    ("DATA", "See the note below for the FRS 101 exemption this entity relies on every year, and why this "
             "workbook is built as a Pillar-3-only variant.", {}),
]

bw.add_cash_flow_sheet(
    title="Bank Mandiri (Europe) Limited — Cash Flow Statement",
    subtitle="Not applicable — this entity takes the FRS 101 cash-flow-statement disclosure exemption every year. See source note below.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=300,
    unit_suffix="",
)

# ---------------------------------------------------------------
# Asset Quality (loans and advances to customers by credit quality + ECL)
# ---------------------------------------------------------------
# Only FY2025 and FY2024 Annual Reports contain a "Credit quality per class
# of financial assets" note (Note 23.5, Credit Risk) breaking loans and
# advances to customers into rating buckets with a 12-month ECL column -
# this note format was not located in the FY2023/FY2022/FY2021 filings
# checked (their equivalent notes cover lease/share-capital/pensions/fair-
# value at the same note numbers instead - the credit-quality-per-class
# table appears to be a later addition to this entity's disclosure). No
# Stage 1/2/3 lifetime-ECL split is disclosed in any year checked - every
# row in the note carries only a "12-mo ECL" column, consistent with this
# entity never disclosing a non-performing/Stage 3 loan figure anywhere
# (its whole book appears to be treated as Stage 1/performing).
ASSET_QUALITY_USD = {
    "Sub-investment grade (rated below Baa3 by Moody's) — gross": {"FY2025": 4_814_000},
    "Sub-investment grade (rated below Baa3 by Moody's) — 12-mo ECL": {"FY2025": -57_000},
    "Unrated — gross": {"FY2025": 127_274_000, "FY2024": 88_401_000},
    "Unrated — 12-mo ECL": {"FY2025": -601_000, "FY2024": -391_000},
    "Total gross loans and advances to customers": {"FY2025": 132_088_000, "FY2024": 88_401_000},
    "Total 12-mo ECL allowance": {"FY2025": -658_000, "FY2024": -391_000},
    "Total net loans and advances to customers": {"FY2025": 131_430_000, "FY2024": 88_010_000},
}
AQ = {k: stock(v) for k, v in ASSET_QUALITY_USD.items()}
ECL_COVERAGE = {"FY2025": "0.50%", "FY2024": "0.44%"}  # 658/132,088; 391/88,401 - not directly disclosed, calculated here

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, by credit quality (Note 23.5)", {}),
    ("DATA", "Sub-investment grade (rated below Baa3 by Moody's) — gross", AQ["Sub-investment grade (rated below Baa3 by Moody's) — gross"]),
    ("DATA", "Sub-investment grade (rated below Baa3 by Moody's) — 12-mo ECL", AQ["Sub-investment grade (rated below Baa3 by Moody's) — 12-mo ECL"]),
    ("DATA", "Unrated — gross", AQ["Unrated — gross"]),
    ("DATA", "Unrated — 12-mo ECL", AQ["Unrated — 12-mo ECL"]),
    ("TOTAL", "Total gross loans and advances to customers", AQ["Total gross loans and advances to customers"]),
    ("DATA", "Total 12-mo ECL allowance", AQ["Total 12-mo ECL allowance"]),
    ("TOTAL", "Total net loans and advances to customers", AQ["Total net loans and advances to customers"]),
    ("SECTION", "Ratios (calculated)", {}),
    ("DATA", "ECL coverage ratio (12-mo ECL allowance ÷ gross loans)", ECL_COVERAGE),
]

ASSET_QUALITY_SOURCES = (
    "Sources — Bank Mandiri (Europe) Limited's own \"Credit quality per class of financial assets\" note (Note "
    "23.5, Credit Risk), Loans and advances to customers rows only, converted from USD to £'000 at each "
    "year-end's Bank of England GBP/USD spot rate (see FX conversion note below): FY2025 & FY2024 — Bank Mandiri "
    f"(Europe) Limited Annual Report FY2025, Note 23.5 Credit Risk, p.48-49 — {FY2025_AR_URL}.\n\n"
    "FY2023, FY2022 and FY2021: this credit-quality-per-class-of-financial-assets table was NOT found in the "
    "FY2023, FY2022, or FY2021 Annual Reports checked (their financial-risk-management notes are structured "
    "differently and do not include an equivalent loans-and-advances credit-quality breakdown) — left blank "
    "rather than estimated. No Stage 1/2/3 IFRS 9 staging split (only an aggregate/12-month ECL figure) is "
    "disclosed for any year — this entity does not appear to disclose a non-performing or Stage 3 loan balance "
    "anywhere in any of the 4 reports checked, so no NPL/Stage 3 ratio is presented here. The ECL coverage ratio "
    "row is CALCULATED (12-mo ECL allowance ÷ gross loans), not directly disclosed.\n\n"
    + ENTITY_NOTE
)

bw.add_asset_quality_sheet(
    title="Bank Mandiri (Europe) Limited — Asset Quality",
    subtitle="£'000, converted from USD — see source note for FX methodology, rates used, and years covered.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=64,
    source_height=280,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=170)


TOTAL_CAPITAL_USD = {"FY2025": 56_400_000, "FY2024": 54_300_000, "FY2023": 52_300_000, "FY2022": 49_710_000}
CAR = {"FY2025": "33.59%", "FY2024": "42.90%", "FY2023": "34.30%", "FY2022": "34.09%"}
# Calculated: Own Funds / CAR - no separate RWA figure is directly disclosed anywhere.
RWA_USD = {"FY2025": 167_907_000, "FY2024": 126_573_000, "FY2023": 152_478_000, "FY2022": 145_820_000}

# Sheet order matches the project-wide standard (CET1 Capital/Ratio, Tier 1 Capital/Ratio,
# Total Capital/Ratio, Total RWAs, Leverage Ratio, LCR, NSFR, MREL Ratio) even though this
# entity only discloses the Total Capital/RWA/LCR/NSFR metrics.
bw.add_not_disclosed_metric_sheets(
    ["CET1 Capital", "CET1 Ratio", "Tier 1 Capital", "Tier 1 Ratio"],
    p3_sources(),
    per_note={m: NOT_DISCLOSED_NOTE for m in ["CET1 Capital", "CET1 Ratio", "Tier 1 Capital", "Tier 1 Ratio"]},
)

metric(
    "Total Capital", "£'000 (conv. from USD)",
    [("Regulatory capital resources (\"Own Funds\")", stock(TOTAL_CAPITAL_USD))],
    p3_sources(),
    note="No CET1/Tier 1 breakdown is disclosed anywhere in the source - only this single combined 'regulatory "
         "capital resources' figure. See CET1 Capital / Tier 1 Capital sheets.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Capital Adequacy Ratio / Total Capital Ratio (Own Funds / Total Risk Weighted Asset)", CAR)],
    p3_sources(),
)

metric(
    "Total RWAs", "£'000 (conv. from USD)",
    [("Total risk-weighted assets", stock(RWA_USD))],
    p3_sources(),
    note="CALCULATED, not directly disclosed - derived as regulatory capital resources ÷ Total Capital Ratio for "
         "each year. No RWA figure appears in any source checked.",
)

RWA_BREAKDOWN_SOURCES = (
    "No dedicated Pillar 3 document, and no UK OV1-style RWA-by-exposure-class breakdown, is published by this "
    "entity — the only RWA figure available (even the single aggregate Total RWAs figure on the 'Total RWAs' "
    "sheet) is itself CALCULATED, not directly disclosed (see that sheet's note). With no directly disclosed "
    "aggregate RWA figure to begin with, a category-level split cannot exist. Checked all 4 Annual Reports "
    "(FY2022-FY2025) and the FY2020 Companies House filing — no exposure-class RWA table found in any.\n\n"
    + ENTITY_NOTE
)

bw.add_not_disclosed_metric_sheets(
    ["RWA Breakdown"], RWA_BREAKDOWN_SOURCES, per_note={"RWA Breakdown": RWA_BREAKDOWN_SOURCES},
)

bw.add_not_disclosed_metric_sheets(
    ["Leverage Ratio"], p3_sources(), per_note={"Leverage Ratio": NOT_DISCLOSED_NOTE},
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio (%)", {"FY2025": "446.89%", "FY2024": "382%", "FY2023": "264.29%", "FY2022": "147.59%"})],
    p3_sources(),
    note="No £/$ breakdown (HQLA, net cash outflows) is disclosed anywhere - only the ratio itself. FY2025 shown to "
         "2 d.p. as stated in the Strategic Report narrative (446.89%); the report's own KPI table rounds this to 447%.",
)

metric(
    "NSFR", "%",
    [("Net Stable Fund Ratio (%)", {"FY2025": "121.85%", "FY2024": "142%", "FY2023": "131.85%", "FY2022": "143.26%"})],
    p3_sources(),
    note="No £/$ breakdown (available/required stable funding) is disclosed anywhere - only the ratio itself. "
         "FY2025 shown to 2 d.p. as stated in the Strategic Report narrative (121.85%); the report's own KPI table "
         "rounds this to 122%.",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources(), per_note={"MREL Ratio": NOT_DISCLOSED_NOTE},
)

# ---------------------------------------------------------------
# Overview sheet (Pillar-3-only: no cash-flow chart)
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit=None,
    balance_sheet_totals=[
        ("Total assets", BS["Total assets"]),
        ("Loan and advances to customers", BS["Loan and advances to customers"]),
        ("Customer accounts", BS["Customer accounts"]),
        ("Total shareholders' funds", BS["Total shareholders' funds"]),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total operating income", IS["Total operating income"]),
        ("Administrative expenses", IS["Administrative expenses"]),
        ("Profit on ordinary activities after tax", IS["Profit on ordinary activities after tax"]),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        # Each opening balance is 31-Dec-(Y-1)'s figure, converted at THAT
        # date's spot rate (FX_SPOT["FY"+str(Y-1)]) - same fix as the
        # Statement of Change in Equity sheet's "At 1 January" rows above.
        ("Opening shareholders' funds", {"FY2025": bal((54254,), "FY2024")[0], "FY2024": bal((52323,), "FY2023")[0], "FY2023": bal((49714,), "FY2022")[0], "FY2022": bal((52489,), "FY2021")[0]}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": flow({"FY2025": 2_230_000})["FY2025"], "FY2024": flow({"FY2024": 1_931_000})["FY2024"], "FY2023": flow({"FY2023": 2_609_000})["FY2023"], "FY2022": flow({"FY2022": -2_775_000})["FY2022"], "FY2021": flow({"FY2021": -418_000})["FY2021"]}),
        # Pure FX-translation artefact of converting opening/movements/closing at 3 different
        # GBP/USD rates within one year - see the Statement of Change in Equity sheet's source
        # note. Not a real equity movement; absorbs the gap so this bridge ties exactly.
        ("Other equity movements, net (FX translation effect — see Statement of Change in Equity)", {y: v for y, v in FX_TRANSLATION_EFFECT.items()}),
        ("Closing shareholders' funds", BS["Total shareholders' funds"]),
    ],
    equity_changes_unit="£'000",
    ratios=[
        ("Total Capital Ratio", CAR),
        ("LCR", {"FY2025": "446.89%", "FY2024": "382%", "FY2023": "264.29%", "FY2022": "147.59%"}),
        ("NSFR", {"FY2025": "121.85%", "FY2024": "142%", "FY2023": "131.85%", "FY2022": "143.26%"}),
    ],
    note="This entity takes the FRS 101 cash-flow-statement exemption every year (see the Cash Flow Statement "
         "sheet), so no cash flow summary or chart is shown here. No dedicated Pillar 3 document is published by "
         "this entity; only a combined Total Capital Ratio (no CET1/Tier 1 breakdown), LCR, and NSFR are "
         "disclosed, in each Annual Report's Strategic Report — Total RWAs and RWA Breakdown are calculated/not "
         "disclosed respectively, see those sheets. FY2021 not available for the ratio trend chart — see each "
         "Pillar 3 sheet's own source citation. Opening shareholders' funds is not available for FY2021 — see the "
         "Statement of Change in Equity sheet's source note.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BANK MANDIRI EUROPE FINANCIALS.xlsx")
