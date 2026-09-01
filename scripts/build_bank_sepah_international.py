import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, y/e 31 March
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/04189598/filing-history/MzQ3Mzg4ODM0MGFkaXF6a2N4/document?format=pdf&download=0"
AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/04189598/filing-history/MzQyOTk1Mjg2NmFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/04189598/filing-history/MzM1MTIwNTQ2MGFkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "Bank Sepah International Plc (FRN 208019, company 04189598) is a wholly-owned UK subsidiary of Bank Sepah "
    "(Iran). Confirmed a going concern: Companies House status Active, accounts filed every year through FY2025 "
    "(y/e 31 March), no insolvency/administration notices. The Managing Director's Statement in the FY2025 Annual "
    "Report (signed 27 June 2025) states 'there are currently no UN, EU or UK sanctions against Bank Sepah "
    "International Plc' as at that date, though US OFAC sanctions on Iranian entities since 2018 severely restrict "
    "its business (SWIFT access suspended Nov 2018) - this predates the UK 'snapback' sanctions on Iran-linked "
    "entities that took effect 29 September 2025 (which affected Bank Saderat Plc, built earlier in this project); "
    "the FY2025 accounts (the most recent filed) do not reflect any post-September-2025 development. Does NOT take "
    "the FRS 101/102 cash-flow exemption - full Statement of Cash Flows every year. Reports in EUR (majority of "
    "assets/liabilities are Euro-denominated per the Strategic Report), converted to GBP here for consistency with "
    "every other workbook in this project."
)

# GBP/EUR conversion rates as disclosed in the Bank's own FY2025 Annual Report's 5-year "Performance Summary" table
# (Strategic Report, p.5) - "Year-end exchange rate - EURO/GBP" and "Average exchange rate - EURO/GBP", i.e. GBP per
# EUR 1. Used directly rather than re-derived from Bank of England data, since the entity discloses its own rates.
YEAR_END_RATE = {"FY2025": 0.8354, "FY2024": 0.8548, "FY2023": 0.8782, "FY2022": 0.8459, "FY2021": 0.8520}
AVG_RATE = {"FY2025": 0.8418, "FY2024": 0.8636, "FY2023": 0.8645, "FY2022": 0.8366, "FY2021": 0.8911}
FX_NOTE = (
    "FX conversion methodology: point-in-time/balance figures (capital, RWA, cash balances) converted at the "
    "Bank's own disclosed EUR/GBP year-end rate; cash-flow figures converted at its own disclosed EUR/GBP average "
    "rate (both from the FY2025 Annual Report's 5-year Performance Summary table, p.5). Ratios are not converted "
    "(dimensionless). The 'Effect of GBP/EUR translation' line in the Cash Flow Statement is computed "
    "programmatically from the actual converted figures (opening + net change + entity's own FX line + this plug = "
    "closing, exactly) - see this project's established FX conversion methodology (first used for SMBC Bank "
    "International plc)."
)

CASH_FLOW_SOURCES = (
    "Sources - Bank Sepah International Plc's own Statement of Cash Flows (Companies House filings):\n"
    f"FY2025/FY2024: Full accounts to 31 March 2025, p.28 - {AR2025_URL}\n"
    f"FY2023: Full accounts to 31 March 2024's own FY2023 comparative column, p.30 - {AR2024_URL}\n"
    f"FY2022/FY2021: Full accounts to 31 March 2022, p.26 - {AR2022_URL}\n"
    "All 3 filings are fully scanned/image-only (0 text blocks/page) - rendered and read visually, cross-checked "
    "where years overlap between filings (FY2024 figures match exactly between the FY2024 and FY2025 accounts).\n"
    + ENTITY_NOTE + "\n" + FX_NOTE
)


def p3_sources():
    return (
        "Sources - Bank Sepah International Plc's own 'Performance Summary' 5-year table, Strategic Report p.5, "
        f"FY2025 Annual Report - {AR2025_URL}. CET1 = Tier 1 = Total Capital every year (no AT1/Tier 2 instruments "
        "mentioned; the Bank discloses a single 'Total capital to total risk-weighted assets' ratio, identical to "
        "'Tier 1 capital to total risk-weighted assets' every year). No Pillar 3/KM1-format document, no leverage "
        "ratio, LCR, NSFR or MREL figure found anywhere in the Annual Report - the Bank states its (unaudited) "
        "Pillar 3 disclosures are published separately at www.banksepah.co.uk, but that site's TLS certificate has "
        "expired and could not be fetched.\n" + FX_NOTE
    )


bw = BankWorkbook(bank_name="Bank Sepah International Plc", years=YEARS, year_label=YEAR_LABEL, header_color="444444")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
# Source figures (EUR '000), from the Bank's own Statement of Cash Flows, cross-checked across overlapping filings.
OPERATING_EUR = {"FY2025": -7597, "FY2024": 5217, "FY2023": -51049, "FY2022": 18042, "FY2021": 2189}
INVESTING_EUR = {"FY2025": 1137, "FY2024": -2122, "FY2023": -122, "FY2022": -515, "FY2021": -499}
NET_CHANGE_EUR = {"FY2025": -6460, "FY2024": 3105, "FY2023": -51171, "FY2022": 17208, "FY2021": 1690}
FX_EUR = {"FY2025": -106, "FY2024": -44, "FY2023": -264, "FY2022": 36, "FY2021": -259}
OPENING_EUR = {"FY2025": 156069, "FY2024": 153018, "FY2023": 204453, "FY2022": 187209, "FY2021": 185778}
CLOSING_EUR = {"FY2025": 149503, "FY2024": 156069, "FY2023": 153018, "FY2022": 204453, "FY2021": 187209}


def flow(eur):
    # eur values are already in EUR '000, so v * rate gives GBP '000 directly.
    return {y: round(v * AVG_RATE[y], 1) for y, v in eur.items()}


def stock(eur):
    return {y: round(v * YEAR_END_RATE[y], 1) for y, v in eur.items()}


OPERATING_GBP = flow(OPERATING_EUR)
INVESTING_GBP = flow(INVESTING_EUR)
NET_CHANGE_GBP = flow(NET_CHANGE_EUR)
FX_GBP = flow(FX_EUR)
CLOSING_GBP = stock(CLOSING_EUR)

# Opening balance: converted at the SAME year's year-end rate applied to the prior year's own EUR closing figure
# (i.e. it equals the prior year's own closing GBP figure exactly) - FY2021's opening has no available FY2020 rate
# and is deliberately left blank rather than sourcing an unverified rate (same convention as Access Bank UK's FY2020).
OPENING_GBP = {
    "FY2025": CLOSING_GBP["FY2024"],
    "FY2024": CLOSING_GBP["FY2023"],
    "FY2023": CLOSING_GBP["FY2022"],
    "FY2022": CLOSING_GBP["FY2021"],
}

# Translation plug computed programmatically (never hardcoded) so it can't hide a conversion bug.
TRANSLATION_PLUG = {
    y: round(CLOSING_GBP[y] - OPENING_GBP[y] - NET_CHANGE_GBP[y] - FX_GBP[y], 1)
    for y in YEARS if y in OPENING_GBP
}

rows = [
    ("SECTION", "Operating activities", {}),
    ("TOTAL", "Net cash from/(used in) operating activities", OPERATING_GBP),
    ("SECTION", "Investing activities", {}),
    ("TOTAL", "Net cash from/(used in) investing activities", INVESTING_GBP),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", NET_CHANGE_GBP),
    ("DATA", "Foreign currency exchange (loss)/gain (Bank's own, EUR functional currency)", FX_GBP),
    ("DATA", "Effect of GBP/EUR translation (this workbook's own conversion, not in the source)", TRANSLATION_PLUG),
    ("DATA", "Cash and cash equivalents at the beginning of the year", OPENING_GBP),
    ("TOTAL", "Cash and cash equivalents at the end of the year", CLOSING_GBP),
]

bw.add_cash_flow_sheet(
    title="Bank Sepah International Plc — Statement of Cash Flows",
    subtitle="Entity-level basis, reports in EUR, converted to GBP - see source note below for methodology",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=260,
    unit_suffix=" (£'000, conv. from EUR)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=52, source_height=170)


# Total capital resources (EUR m), = CET1 = Tier 1 = Total Capital (no AT1/Tier 2 disclosed)
CAPITAL_EUR_M = {"FY2025": 173, "FY2024": 172, "FY2023": 172, "FY2022": 170, "FY2021": 169}
CAPITAL_RATIO = {"FY2025": "102.7%", "FY2024": "91.8%", "FY2023": "81.5%", "FY2022": "67.5%", "FY2021": "61.2%"}
CAPITAL_GBP_M = {y: round(v * YEAR_END_RATE[y], 1) for y, v in CAPITAL_EUR_M.items()}

# RWA calculated (not directly disclosed) = capital resources / ratio, in EUR m, then converted
RWA_EUR_M = {y: round(CAPITAL_EUR_M[y] / (float(CAPITAL_RATIO[y].rstrip('%')) / 100), 1) for y in YEARS}
RWA_GBP_M = {y: round(v * YEAR_END_RATE[y], 1) for y, v in RWA_EUR_M.items()}

CAPITAL_NOTE = "CET1 = Tier 1 = Total Capital every year - the Bank discloses only a single combined capital figure, no AT1/Tier 2 instruments mentioned anywhere in the Annual Report."
RATIO_NOTE = "The Bank discloses one 'Total capital / Tier 1 capital to total risk-weighted assets' ratio (identical each year, confirming no AT1/Tier 2) - used for CET1/Tier1/Total Capital Ratio alike."
RWA_NOTE = "CALCULATED, not directly disclosed - derived as capital resources (EUR) ÷ the disclosed capital ratio for each year, then converted to GBP at the year-end rate."
NOT_DISCLOSED_NOTE = "Not publicly disclosed - no figure found in the FY2021-FY2025 Annual Reports. The Bank states its (unaudited) Pillar 3 disclosures are published separately at www.banksepah.co.uk, but that site's TLS certificate has expired and could not be fetched to check."

metric("CET1 Capital", "£m (conv. from EUR)", [("Common Equity Tier 1 (CET1) capital", CAPITAL_GBP_M)], note=CAPITAL_NOTE)
metric("CET1 Ratio", "%", [("CET1 to total risk-weighted assets", CAPITAL_RATIO)], note=RATIO_NOTE)
metric("Tier 1 Capital", "£m (conv. from EUR)", [("Tier 1 capital", CAPITAL_GBP_M)], note=CAPITAL_NOTE)
metric("Tier 1 Ratio", "%", [("Tier 1 capital to total risk-weighted assets", CAPITAL_RATIO)], note=RATIO_NOTE)
metric("Total Capital", "£m (conv. from EUR)", [("Total capital resources", CAPITAL_GBP_M)], note=CAPITAL_NOTE)
metric("Total Capital Ratio", "%", [("Total capital to total risk-weighted assets", CAPITAL_RATIO)], note=RATIO_NOTE)
metric("Total RWAs", "£m (conv. from EUR)", [("Total risk-weighted assets", RWA_GBP_M)], note=RWA_NOTE)

bw.add_not_disclosed_metric_sheets(
    ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"],
    p3_sources(),
    per_note={m: NOT_DISCLOSED_NOTE for m in ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"]},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", OPERATING_GBP),
        ("Net cash from/(used in) investing activities", INVESTING_GBP),
        ("Cash and cash equivalents at end of year", CLOSING_GBP),
    ],
    cash_flow_unit="£'000 (conv. from EUR)",
    ratios=[
        ("CET1 Ratio", CAPITAL_RATIO),
        ("Tier 1 Ratio", CAPITAL_RATIO),
        ("Total Capital Ratio", CAPITAL_RATIO),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. All capital ratios are identical every year (no "
         "AT1/Tier 2 capital) so all three lines overlap on the chart.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BANK SEPAH INTERNATIONAL FINANCIALS.xlsx")
