import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {year: year for year in YEARS}

COMPANY_NO = "01772585"
AR_URLS = {
    "FY2025": f"https://find-and-update.company-information.service.gov.uk/company/{COMPANY_NO}/filing-history/MzUyNzI0MDUzNGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2024": f"https://find-and-update.company-information.service.gov.uk/company/{COMPANY_NO}/filing-history/MzQ3MTYzOTk3NmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2023": f"https://find-and-update.company-information.service.gov.uk/company/{COMPANY_NO}/filing-history/MzQyNjY3NDIyNmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2022": f"https://find-and-update.company-information.service.gov.uk/company/{COMPANY_NO}/filing-history/MzM4NDYyNTMxMWFkaXF6a2N4/document?format=pdf&download=0",
    "FY2021": f"https://find-and-update.company-information.service.gov.uk/company/{COMPANY_NO}/filing-history/MzM0MzE4NDc0N2FkaXF6a2N4/document?format=pdf&download=0",
}

ENTITY_NOTE = (
    "Marks and Spencer Financial Services plc (trading as M&S Bank) is the PRA-authorised entity in the bank list, "
    "FRN 151427, Companies House company 01772585. The statutory accounts are entity-only accounts, in £'000. "
    "The company changed its registered name to Marks and Spencer Financial Services Limited in June 2026; the "
    "five source filings used here were filed under the historical plc name.\n\n"
    "The accounts state that separate Pillar 3 disclosures are not required because the Entity is included in the "
    "consolidated Pillar 3 disclosures of HSBC UK Bank plc. Accordingly, this workbook uses the Entity's own annual "
    "capital-management figures where disclosed and does not substitute HSBC UK group figures."
)


def source(year, page, detail):
    return f"Marks and Spencer Financial Services plc Annual Report and Financial Statements {year}, p.{page}, {detail} - {AR_URLS[year]}"


CASH_FLOW_SOURCES = (
    "Sources - Marks and Spencer Financial Services plc entity-only Statement of Cash Flows, £'000:\n"
    + "\n".join(
        source(year, 21 if year == "FY2021" else 20 if year in ("FY2022", "FY2023") else 21 if year == "FY2024" else 22,
               "Statement of cash flows")
        for year in YEARS
    )
    + "\n\n"
    + ENTITY_NOTE
    + "\n\nPresentation note: the reports present changes in operating assets and liabilities as aggregate lines, "
      "so those lines are retained rather than reverse-engineering their underlying loan/deposit components."
)


bw = BankWorkbook(
    bank_name="Marks and Spencer Financial Services plc",
    years=YEARS,
    year_label=YEAR_LABEL,
    header_color="A50034",
)


cash_rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {"FY2025": 9608, "FY2024": 51896, "FY2023": 55021, "FY2022": 38013, "FY2021": 115795}),
    ("DATA", "Non-cash items included in profit before tax", {"FY2025": 23182, "FY2024": -19285, "FY2023": -35967, "FY2022": 15787, "FY2021": -175023}),
    ("DATA", "Change in operating assets", {"FY2025": -583961, "FY2024": -274436, "FY2023": -113098, "FY2022": -354722, "FY2021": 664424}),
    ("DATA", "Change in operating liabilities", {"FY2025": -27505, "FY2024": -42313, "FY2023": -57669, "FY2022": -170561, "FY2021": -1082413}),
    ("DATA", "Tax paid/(credit received)", {"FY2025": -10663, "FY2024": -9999, "FY2023": -7801, "FY2022": -13322, "FY2021": 708}),
    ("TOTAL", "Net cash used in operating activities", {"FY2025": -589339, "FY2024": -294137, "FY2023": -159514, "FY2022": -484805, "FY2021": -476509}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": 0, "FY2024": -71, "FY2023": -253, "FY2022": -204, "FY2021": -176}),
    ("DATA", "Purchase of intangible assets", {"FY2025": -3937, "FY2024": -4404, "FY2023": -6115, "FY2022": -7442, "FY2021": -3443}),
    ("DATA", "Proceeds from sale of property, plant and equipment", {"FY2024": 447}),
    ("DATA", "Adjustment of leases", {"FY2024": 0, "FY2023": -1228, "FY2022": -2787, "FY2021": 2137}),
    ("TOTAL", "Net cash used in investing activities", {"FY2025": -3937, "FY2024": -4028, "FY2023": -7596, "FY2022": -10433, "FY2021": -1482}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Proceeds from borrowings", {"FY2025": 499000, "FY2024": 407000, "FY2023": 155000, "FY2022": 210000, "FY2021": 149967}),
    ("DATA", "Issue of ordinary share capital", {"FY2025": 30000}),
    ("DATA", "Repayment of other equity instruments", {"FY2025": -49000}),
    ("DATA", "Issue of other equity instruments", {"FY2025": 39547}),
    ("DATA", "Subordinated liabilities repaid", {"FY2024": -16017}),
    ("DATA", "Dividends", {"FY2025": -16932, "FY2024": -19226, "FY2023": -11000, "FY2022": -27000}),
    ("DATA", "Distribution on other equity instruments (AT1)", {"FY2025": -5003, "FY2024": -5003, "FY2023": -5003, "FY2022": -5003, "FY2021": -5003}),
    ("TOTAL", "Net cash generated from financing activities", {"FY2025": 497612, "FY2024": 366754, "FY2023": 138997, "FY2022": 177997, "FY2021": 144964}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -95661, "FY2024": 68589, "FY2023": -28113, "FY2022": -317241, "FY2021": -333027}),
    ("DATA", "Cash and cash equivalents brought forward", {"FY2025": 190223, "FY2024": 121634, "FY2023": 149747, "FY2022": 466988, "FY2021": 800015}),
    ("TOTAL", "Cash and cash equivalents carried forward", {"FY2025": 94562, "FY2024": 190223, "FY2023": 121634, "FY2022": 149747, "FY2021": 466988}),
]

bw.add_cash_flow_sheet(
    title="Marks and Spencer Financial Services plc — Statement of Cash Flows",
    subtitle="Entity-only figures, £'000. See source note at bottom.",
    rows=cash_rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=64,
    source_height=190,
    unit_suffix=" (£'000)",
)


PAGES = {"FY2021": 10, "FY2022": 9, "FY2023": 9, "FY2024": 10, "FY2025": 12}


def metric(name, unit, rows_data, detail, note=None):
    sources = "Sources - entity-only capital management disclosures:\n" + "\n".join(
        source(year, PAGES[year], "Capital management / calculation of actual capital") for year in YEARS
    ) + "\n\n" + ENTITY_NOTE
    bw.add_metric_sheet(name, unit, rows_data, sources, note=note, first_col_width=48, source_height=170)


metric("CET1 Capital", "£'000", [("Common equity tier 1 capital", {"FY2025": 443918, "FY2024": 402910, "FY2023": 395366, "FY2022": 396478, "FY2021": 389044})], "CET1 capital")
metric("CET1 Ratio", "% of RWA", [("Common equity tier 1 ratio", {"FY2025": "13.86%", "FY2024": "13.59%", "FY2023": "14.28%", "FY2022": "15.12%", "FY2021": "16.60%"})], "CET1 ratio")
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", {"FY2025": 503465, "FY2024": 471910, "FY2023": 464366, "FY2022": 465478, "FY2021": 458044})], "Tier 1 capital")
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {"FY2025": "15.72%", "FY2024": "15.92%", "FY2023": "16.78%", "FY2022": "17.76%", "FY2021": "19.54%"})], "Tier 1 ratio")
metric("Total Capital", "£'000", [("Total regulatory capital", {"FY2025": 589922, "FY2024": 557332, "FY2023": 568127, "FY2022": 567767, "FY2021": 563755})], "Total regulatory capital")
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2025": "18.42%", "FY2024": "18.80%", "FY2023": "20.52%", "FY2022": "21.66%", "FY2021": "24.05%"})], "Total capital ratio")
metric("Total RWAs", "£'000", [("Total risk-weighted assets", {"FY2025": 3202921, "FY2024": 2964326, "FY2023": 2768029, "FY2022": 2621405, "FY2021": 2343898})], "Total risk-weighted assets")

not_disclosed = ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"]
NOT_DISCLOSED_SOURCES = (
    "Sources - entity-only annual accounts reviewed for this metric:\n"
    + "\n".join(
        source(year, PAGES[year], "Capital management / calculation of actual capital; no standalone metric disclosed")
        for year in YEARS
    )
    + "\n\n"
    + ENTITY_NOTE
    + "\n\nThe entity's accounts do not disclose a standalone leverage ratio, LCR, NSFR or MREL ratio. "
      "HSBC UK Bank plc consolidated Pillar 3 disclosures are not substituted because they are group-level figures."
)
for name in not_disclosed:
    bw.add_metric_sheet(
        name,
        None,
        [(name, {y: "Not publicly disclosed" for y in YEARS})],
        NOT_DISCLOSED_SOURCES,
        note="Not separately disclosed for Marks and Spencer Financial Services plc; HSBC UK consolidated Pillar 3 figures are not entity-level.",
    )


bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash used in operating activities", {"FY2025": -589339, "FY2024": -294137, "FY2023": -159514, "FY2022": -484805, "FY2021": -476509}),
        ("Net cash used in investing activities", {"FY2025": -3937, "FY2024": -4028, "FY2023": -7596, "FY2022": -10433, "FY2021": -1482}),
        ("Net cash generated from financing activities", {"FY2025": 497612, "FY2024": 366754, "FY2023": 138997, "FY2022": 177997, "FY2021": 144964}),
        ("Cash and cash equivalents carried forward", {"FY2025": 94562, "FY2024": 190223, "FY2023": 121634, "FY2022": 149747, "FY2021": 466988}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 ratio", {"FY2025": 13.86, "FY2024": 13.59, "FY2023": 14.28, "FY2022": 15.12, "FY2021": 16.60}),
        ("Total capital ratio", {"FY2025": 18.42, "FY2024": 18.80, "FY2023": 20.52, "FY2022": 21.66, "FY2021": 24.05}),
    ],
    note="Entity-only annual capital-management figures. Separate Pillar 3 disclosures are not required because the entity is included in HSBC UK Bank plc's consolidated Pillar 3 disclosures; group figures are not substituted here.",
)


bw.save("/Users/armaan/code/katalysis/banks/MARKS AND SPENCER FINANCIAL SERVICES FINANCIALS.xlsx")
