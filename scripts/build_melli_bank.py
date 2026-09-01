import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/04152338/filing-history/MzUyNjMyOTE4OGFkaXF6a2N4/document?download=0&format=pdf"
AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/04152338/filing-history/MzQ3MDI0ODU4NWFkaXF6a2N4/document?download=0&format=pdf"
AR2023_URL = "https://vpr.hkma.gov.hk/statics/assets/doc/100273/ar_23/ar_23_eng.pdf"
AR2022_URL = "https://vpr.hkma.gov.hk/statics/assets/doc/100273/ar_22/ar_22_eng.pdf"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/04152338/filing-history/MzM0MzE1NzIzOWFkaXF6a2N4/document?download=0&format=pdf"

ENTITY_NOTE = (
    "ENTITY AND REPORTING BASIS: Melli Bank plc (company 04152338, FRN 207380, LEI "
    "213800BC4TEGCCQH9V07) is an active UK public limited company and PRA-authorised bank, "
    "incorporated in England and Wales. Companies House identifies the registered office as "
    "98a Kensington High Street, London W8 4SG and the latest accounts as made up to 31 December "
    "2025. The Bank's functional and reporting currency is EUR; amounts are therefore retained in "
    "EUR thousands/millions, consistent with the source accounts. The figures are standalone Melli "
    "Bank plc entity figures, not Bank Melli Iran group figures."
)

CASH_FLOW_SOURCES = (
    "Sources - Melli Bank plc entity-level Statements of Cash Flows:\n"
    f"FY2024: Annual Report and Accounts 2024, p.24 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Accounts 2023, p.24 - {AR2023_URL}\n"
    f"FY2022: Annual Report and Accounts 2023 comparative column, p.24 - {AR2023_URL}\n"
    "FY2021: not disclosed. The Annual Report 2021, accounting policy (p.23), states that the "
    "Company used the FRS 102 cash-flow exemption because it was consolidated with Bank Melli Iran.\n"
    f"FY2025: the Companies House filing is listed, but the PDF was not retrievable in this run - {AR2025_URL}\n\n"
    + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - Melli Bank plc entity-level regulatory KPI and capital disclosures:\n"
        f"FY2024/FY2023: Annual Report and Accounts 2024, KPI p.9 and capital management p.49 - {AR2024_URL}\n"
        f"FY2023/FY2022/FY2021: Annual Report and Accounts 2023, KPI p.9 and capital management p.49 - {AR2023_URL}\n"
        f"FY2021 comparative context: Annual Report 2021, KPI p.8 and capital management p.46 - {AR2021_URL}\n"
        f"FY2025: the Companies House filing is listed, but the PDF was not retrievable in this run - {AR2025_URL}\n"
        "The 2022-2024 reports state that Pillar 3 disclosure is available on request; no public current "
        "Pillar 3/KM1 document or defensible entity-level interim series was located."
    )


bw = BankWorkbook(
    bank_name="Melli Bank plc",
    years=YEARS,
    year_label=YEAR_LABEL,
    header_color="6E4B3A",
)

# Source cash-flow figures are EUR '000. FY2021 is blank because the 2021
# accounts expressly claim the FRS 102 qualifying-entity exemption.
OPERATING = {"FY2024": 13753, "FY2023": -27408, "FY2022": -52056}
INVESTING = {"FY2024": -664, "FY2023": -258, "FY2022": -47}
NET_CHANGE = {"FY2024": 13089, "FY2023": -27666, "FY2022": -52103}
OPENING = {"FY2024": 39289, "FY2023": 66955, "FY2022": 119058}
CLOSING = {"FY2024": 52378, "FY2023": 39289, "FY2022": 66955}

cash_rows = [
    ("SECTION", "Operating activities", {}),
    ("TOTAL", "Net cash from operating activities", OPERATING),
    ("SECTION", "Investing activities", {}),
    ("TOTAL", "Net cash from investing activities", INVESTING),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", NET_CHANGE),
    ("DATA", "Cash and cash equivalents at the beginning of the period", OPENING),
    ("TOTAL", "Cash and cash equivalents at the end of the period", CLOSING),
]

bw.add_cash_flow_sheet(
    title="Melli Bank plc — Statement of Cash Flows",
    subtitle="Entity-level basis, EUR '000; FY2021 unavailable under FRS 102 exemption and FY2025 source PDF not retrievable",
    rows=cash_rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=270,
    unit_suffix=" (EUR '000)",
)


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(
        name,
        unit,
        rows_data,
        p3_sources(),
        note=note,
        first_col_width=58,
        source_height=250,
    )


ELIGIBLE_CAPITAL = {
    "FY2024": 258360,
    "FY2023": 256049,
    "FY2022": 255912,
    "FY2021": 255099,
}
RWA = {"FY2024": 466000, "FY2023": 498000, "FY2022": 423000, "FY2021": 399000}
CAPITAL_RATIO = {"FY2024": "55%", "FY2023": "51%", "FY2022": "60%", "FY2021": "64%"}
LCR = {"FY2024": "697%", "FY2023": "529%", "FY2022": "617%"}

CAPITAL_NOTE = (
    "Eligible regulatory capital is 100% CET1 in the disclosed KPI/capital-management tables; "
    "the same disclosed amount is therefore shown for CET1, Tier 1 and Total Capital. Values are EUR '000."
)
RATIO_NOTE = "The Bank discloses a single Total Capital Ratio and states all capital is CET1; the ratio is shown as the CET1, Tier 1 and Total Capital ratio."
RWA_NOTE = "Total Risk Exposure Amount is the directly disclosed regulatory KPI, shown in EUR '000 (source table reports EUR millions)."
GAP_NOTE = (
    "Not publicly disclosed for this entity/year in the reviewed official source set. The Bank's reports state that "
    "Pillar 3 disclosure is available on request; no public current KM1 document was located. FY2025 is also blank "
    "because the listed Companies House PDF was not retrievable in this run."
)

metric("CET1 Capital", "EUR '000", [("Common Equity Tier 1 / eligible regulatory capital", ELIGIBLE_CAPITAL)], note=CAPITAL_NOTE)
metric("CET1 Ratio", "%", [("CET1 capital ratio", CAPITAL_RATIO)], note=RATIO_NOTE)
metric("Tier 1 Capital", "EUR '000", [("Tier 1 / eligible regulatory capital", ELIGIBLE_CAPITAL)], note=CAPITAL_NOTE)
metric("Tier 1 Ratio", "%", [("Tier 1 capital ratio", CAPITAL_RATIO)], note=RATIO_NOTE)
metric("Total Capital", "EUR '000", [("Total regulatory capital / eligible capital", ELIGIBLE_CAPITAL)], note=CAPITAL_NOTE)
metric("Total Capital Ratio", "%", [("Total capital ratio", CAPITAL_RATIO)], note=RATIO_NOTE)
metric("Total RWAs", "EUR '000", [("Total risk exposure amount", RWA)], note=RWA_NOTE)
metric("Leverage Ratio", "%", [("Leverage ratio", {})], note=GAP_NOTE)
metric("LCR", "%", [("Liquidity Coverage Ratio", LCR)], note="Directly disclosed in the KPI table for FY2022-FY2024; no FY2021 or FY2025 value was located.")
bw.add_not_disclosed_metric_sheets(
    ["NSFR", "MREL Ratio"],
    p3_sources(),
    per_note={"NSFR": GAP_NOTE, "MREL Ratio": GAP_NOTE},
)

bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from operating activities", OPERATING),
        ("Net cash from investing activities", INVESTING),
        ("Cash and cash equivalents at end of year", CLOSING),
    ],
    cash_flow_unit="EUR '000",
    ratios=[("CET1 Ratio", CAPITAL_RATIO), ("LCR", LCR)],
    note="FY2021 cash flow is unavailable under the FRS 102 exemption. FY2025 values remain blank pending retrieval of the listed Companies House accounts PDF.",
)

bw.save("/Users/armaan/code/katalysis/banks/MELLI BANK FINANCIALS.xlsx")
