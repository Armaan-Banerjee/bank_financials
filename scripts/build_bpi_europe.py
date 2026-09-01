import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# PILLAR-3-ONLY WORKBOOK: Bank of the Philippine Islands (Europe) PLC (company
# 05888535, FRN 455378) is a qualifying entity under FRS 102 and takes the
# Section 7 "Statement of Cash Flows" disclosure exemption every year - the
# FY2025 Annual Report's Note 3(c) "Exemptions for qualifying entities under
# FRS 102" states this explicitly: the Bank is wholly-owned by BPI (Bank of the
# Philippine Islands), which publishes a consolidated Cash Flow Statement. The
# FY2025 Independent Auditor's Report confirms the audited primary statements
# comprise only the Profit and Loss Account, the Balance Sheet, and the
# Statement of Movement in Shareholder's Funds - no cash flow statement.
# Follows the BNY Mellon International / ABC International Bank / Bank Mandiri
# (Europe) precedent: 13-sheet structure, Cash Flow Statement sheet documents
# the exemption instead of line items, Overview sheet omits the cash-flow chart.
#
# NOT the same entity as Philippine National Bank (Europe) Plc (company
# 02939223, SKIPPED earlier in this project) - different parent group (Bank of
# the Philippine Islands vs. Philippine National Bank) despite similar naming;
# confirmed independently via Companies House.
#
# GENUINE MID-SERIES FUNCTIONAL CURRENCY CHANGE: the Bank changed its
# functional/presentation currency from GBP to USD during FY2023 (the FY2023
# Annual Report's Strategic Report states the change caused a one-time $1.16m
# FX trading loss, and the FY2023 accounts' capital table is explicitly labelled
# "Restated" for the FY2022 comparative). FY2021 and FY2022's own originally-
# published figures are in GBP (no conversion needed); FY2023-FY2025 are in USD
# and are converted to £ per this project's established FX methodology. This is
# a different pattern from every prior FX case in this project (which are all
# single-currency-throughout) - only PART of the window needs conversion.

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, calendar year-end (31 December)
YEAR_LABEL = {y: y for y in YEARS}

# ---------------------------------------------------------------
# FX conversion - ONLY for FY2023-FY2025 (the USD-reporting years). FY2021 and
# FY2022 are the Bank's own originally-published £ figures, used as-is.
# Rates are Bank of England GBP/USD spot via poundsterlinglive.com's published
# archive, £1 = $X - same rate table used throughout this project's USD banks.
# ---------------------------------------------------------------
FX_SPOT = {
    "FY2023": 1.2732,  # 29 Dec 2023 (31st was a Sunday)
    "FY2024": 1.2515,  # 31 Dec 2024
    "FY2025": 1.3448,  # 31 Dec 2025
}


def stock(usd_by_year):
    """Point-in-time (capital/RWA) USD figures for FY2023-FY2025, £'000 at that
    year's period-end spot rate. Pass GBP-native FY2021/FY2022 figures separately."""
    return {y: round(v / FX_SPOT[y] / 1000, 0) for y, v in usd_by_year.items()}


FY2025_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/05888535/filing-history/MzUyMDczNTAwM2FkaXF6a2N4/document?format=pdf&download=0"
FY2023_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/05888535/filing-history/MzQyNjQ2OTQ5OGFkaXF6a2N4/document?format=pdf&download=0"
FY2022_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/05888535/filing-history/MzM3NzAxNzg2OGFkaXF6a2N4/document?format=pdf&download=0"
FY2021_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/05888535/filing-history/MzMzNzI1NDc5M2FkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "ENTITY NOTE: Bank of the Philippine Islands (Europe) PLC (\"BPI Europe\", company 05888535, FRN 455378, "
    "incorporated 27 July 2006) is a wholly-owned UK subsidiary of Bank of the Philippine Islands (BPI), one of "
    "the Philippines' largest banks. NOT the same entity as Philippine National Bank (Europe) Plc (company "
    "02939223, a different Philippine bank group's UK subsidiary, skipped earlier in this project) - confirmed "
    "via Companies House, no relationship between the two."
)

EXEMPTION_NOTE = (
    "FRS 102 CASH-FLOW EXEMPTION: the FY2025 Annual Report's Note 3(c) \"Exemptions for qualifying entities under "
    "FRS 102\" states: \"In preparing these financial statements, BPI Europe has taken advantage of the disclosure "
    "exemption on the requirement of Section 7 Statement of Cash Flows, as permitted by FRS 102... The Bank is "
    "wholly-owned by BPI, a bank incorporated in the Republic of the Philippines and which publishes a "
    "consolidated Cash Flow Statement, Balance Sheet, and Income Statement\" - "
    f"Bank of the Philippine Islands (Europe) PLC Annual Report FY2025, Note 3(c), p.38 - {FY2025_AR_URL}. The "
    "Independent Auditor's Report (p.25) confirms the audited primary statements comprise only the Profit and "
    "Loss Account, the Balance Sheet, and the Statement of Movement in Shareholder's Funds. Per the project's "
    "established policy for this exemption, this workbook is built as a PILLAR-3-ONLY variant: the capital/"
    "liquidity metrics that are disclosed are populated below, but no cash flow figures exist to show."
)

CASH_FLOW_SOURCES = ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE

CURRENCY_NOTE = (
    "CURRENCY: the Bank changed its functional/presentation currency from GBP to USD during FY2023 (confirmed in "
    "the FY2023 Annual Report's Strategic Report and its capital table's \"Restated\" FY2022 comparative). FY2021 "
    "and FY2022 monetary figures below are the Bank's own originally-published £ figures (Companies House filings "
    "for those years, in GBP) - not converted. FY2023-FY2025 are originally reported in USD and are converted to "
    "£ at the Bank of England GBP/USD spot rate as at each fiscal year-end (29 Dec 2023 1.2732 - 31st was a "
    "Sunday; 31 Dec 2024 1.2515; 31 Dec 2025 1.3448). % ratios are shown exactly as reported in either currency, "
    "never converted (dimensionless)."
)


def p3_sources(extra=""):
    return (
        "Sources - Bank of the Philippine Islands (Europe) PLC, Strategic Report \"Capital Resources\"/\"Liquidity "
        "Resources\" narrative and the Notes' \"Capital Adequacy\" components table, from each year's own Annual "
        "Report filed at Companies House (all 5 filings fully scanned/image-only, OCR'd):\n"
        f"FY2025 & FY2024: Annual Report FY2025, Strategic Report p.7, Note 21 components table p.9-10 - {FY2025_AR_URL}\n"
        f"FY2023 & FY2022 (restated): Annual Report FY2023, Strategic Report p.7-8, components table p.9-10 - {FY2023_AR_URL}\n"
        f"FY2022 (as originally reported, £) & FY2021: Annual Report FY2022, Strategic Report p.5-6, components table p.7 - {FY2022_AR_URL}\n"
        f"FY2021 (as originally reported, £) & FY2020: Annual Report FY2021, Strategic Report p.5-6, components table p.7 - {FY2021_AR_URL}\n"
        + (extra + "\n" if extra else "")
        + CURRENCY_NOTE
    )


NOT_DISCLOSED_NOTE = (
    "No dedicated Pillar 3 document is published by this entity - all capital/liquidity figures come from each "
    "Annual Report's own Strategic Report narrative and Notes. This metric is not disclosed in any of the 5 "
    "Annual Reports checked (FY2021-FY2025)."
)

bw = BankWorkbook(bank_name="Bank of the Philippine Islands (Europe) PLC", years=YEARS, year_label=YEAR_LABEL, header_color="0057B7")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (exemption note in place of line items)
# ---------------------------------------------------------------
rows = [
    ("SECTION", "No Statement of Cash Flows is published by this entity in any year", {}),
    ("DATA", "See the note below for the FRS 102 exemption this entity relies on every year, and why this "
             "workbook is built as a Pillar-3-only variant.", {}),
]

bw.add_cash_flow_sheet(
    title="Bank of the Philippine Islands (Europe) PLC — Cash Flow Statement",
    subtitle="Not applicable — this entity takes the FRS 102 cash-flow-statement disclosure exemption every year. See source note below.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=320,
    unit_suffix="",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=190)


# Own Funds = Tier 1 Capital = CET1 Capital every year (no AT1/Tier 2 instruments)
OWN_FUNDS_USD = {"FY2025": 122_218_000, "FY2024": 121_886_000, "FY2023": 121_737_000}
OWN_FUNDS_GBP = stock(OWN_FUNDS_USD)
OWN_FUNDS_GBP.update({"FY2022": 101_839, "FY2021": 101_528})  # £'000, as originally reported

CAPITAL_RATIO = {"FY2025": "56.29%", "FY2024": "61.59%", "FY2023": "68.24%", "FY2022": "60.19%", "FY2021": "76.79%"}

CRWA_USD = {"FY2025": 202_285_000, "FY2024": 183_493_000, "FY2023": 163_978_000}
MRWA_USD = {"FY2025": 8_513_000, "FY2024": 8_688_000, "FY2023": 8_665_000}
ORWA_USD = {"FY2025": 6_325_000, "FY2024": 5_725_000, "FY2023": 5_750_000}
TOTAL_RWA_USD = {"FY2025": 217_123_000, "FY2024": 197_906_000, "FY2023": 178_393_000}

CRWA_GBP = stock(CRWA_USD); CRWA_GBP.update({"FY2022": 152_940, "FY2021": 119_123})
MRWA_GBP = stock(MRWA_USD); MRWA_GBP.update({"FY2022": 11_838, "FY2021": 8_938})
ORWA_GBP = stock(ORWA_USD); ORWA_GBP.update({"FY2022": 4_400, "FY2021": 4_150})
TOTAL_RWA_GBP = stock(TOTAL_RWA_USD); TOTAL_RWA_GBP.update({"FY2022": 169_178, "FY2021": 132_211})

LCR = {"FY2025": "206%", "FY2024": "329%", "FY2023": "410%", "FY2022": "166%", "FY2021": "224%"}
NSFR = {"FY2025": "154%", "FY2024": "163%", "FY2023": "117%", "FY2022": "119%"}  # FY2021: see note below
LEVERAGE = {"FY2025": "51.22%", "FY2024": "58.71%", "FY2023": "64.62%"}  # FY2022/FY2021: not disclosed

metric("CET1 Capital", "£'000 (FY2021-22 £ native, FY2023-25 conv. from USD)",
       [("Common Equity Tier 1 (CET1) Capital", OWN_FUNDS_GBP)], p3_sources())

metric("CET1 Ratio", "% of Total Risk Exposure Amount",
       [("CET1 Capital Ratio", CAPITAL_RATIO)], p3_sources(),
       note="CET1 = Tier 1 = Total Capital every year - the Bank holds no AT1 or Tier 2 instruments.")

metric("Tier 1 Capital", "£'000 (FY2021-22 £ native, FY2023-25 conv. from USD)",
       [("Tier 1 Capital", OWN_FUNDS_GBP)], p3_sources())

metric("Tier 1 Ratio", "% of Total Risk Exposure Amount",
       [("Tier 1 Capital Ratio", CAPITAL_RATIO)], p3_sources())

metric("Total Capital", "£'000 (FY2021-22 £ native, FY2023-25 conv. from USD)",
       [("Own Funds / Total Capital", OWN_FUNDS_GBP)], p3_sources())

metric("Total Capital Ratio", "% of Total Risk Exposure Amount",
       [("Total Capital Ratio", CAPITAL_RATIO)], p3_sources())

metric("Total RWAs", "£'000 (FY2021-22 £ native, FY2023-25 conv. from USD)",
       [
           ("Total Credit Risk-Weighted Assets (CRWA)", CRWA_GBP),
           ("Total Market Risk-Weighted Assets (MRWA)", MRWA_GBP),
           ("Total Operational Risk-Weighted Assets (ORWA)", ORWA_GBP),
           ("Total Risk Exposure Amount", TOTAL_RWA_GBP),
       ], p3_sources())

metric("Leverage Ratio", "%", [("Leverage Ratio", LEVERAGE)], p3_sources(),
       note="Not disclosed for FY2021/FY2022 in either Annual Report - left blank, not estimated.")

metric("LCR", "%", [("Liquidity Coverage Ratio (LCR)", LCR)], p3_sources(),
       note="No £/$ HQLA/outflow breakdown is disclosed anywhere - only the ratio itself.")

metric("NSFR", "%", [("Net Stable Funding Ratio (NSFR)", NSFR)], p3_sources(),
       note="FY2021: not disclosed - the FY2021 and FY2022 Annual Reports both describe the Bank securing "
            "long-term borrowings \"to comply with the requirements of Net Stable Funding Ratio (NSFR), ahead "
            "of its full implementation in 2022\", i.e. NSFR was not yet a tracked/reported metric for FY2021.")

bw.add_not_disclosed_metric_sheets(["MREL Ratio"], p3_sources(), per_note={"MREL Ratio": NOT_DISCLOSED_NOTE})

# ---------------------------------------------------------------
# Overview sheet (Pillar-3-only: no cash-flow chart)
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("Total Capital Ratio", CAPITAL_RATIO),
        ("LCR", LCR),
        ("NSFR", NSFR),
    ],
    note="This is a PILLAR-3-ONLY workbook: BPI Europe takes the FRS 102 cash-flow-statement exemption every year "
         "(see the Cash Flow Statement sheet), so no cash flow summary or chart is shown here. Also note a genuine "
         "mid-series functional-currency change (GBP through FY2022, USD from FY2023) - monetary (£'000) figures "
         "on the capital/RWA sheets are on a mixed native/converted basis across the window; see each sheet's own "
         "source note and the CURRENCY note there for the exact treatment. % ratios are unaffected by the "
         "currency change.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BANK OF THE PHILIPPINE ISLANDS EUROPE FINANCIALS.xlsx")
