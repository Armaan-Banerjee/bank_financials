import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first

# Companies House annual accounts filings (company 00383032). All 4 filings
# used are fully scanned (image-only) - every figure below was read visually
# from the rendered page image and cross-checked against the adjoining year's
# own comparative column.
AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/00383032/filing-history/MzUxODk5NjMzM2FkaXF6a2N4/document?format=pdf&download=0"
AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/00383032/filing-history/MzQ2NDYzNjU4OGFkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/00383032/filing-history/MzQyMDI4MDMwNWFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/00383032/filing-history/MzMzODQ2NDUzMWFkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "Entity: Cater Allen Limited (FRN 178737, company 00383032), a UK private bank, wholly "
    "owned by Santander Private Banking UK Limited, itself a wholly-owned subsidiary of "
    "Santander UK plc (ultimate UK parent: Santander UK Group Holdings plc; ultimate parent: "
    "Banco Santander SA). Reports in GBP; no FX conversion needed.\n\n"
    "GENUINELY NEW PATTERN - exemption newly adopted in the FINAL year of this workbook's "
    "window, not from the start: FY2021-FY2024 all have a full, audited Statement of Cash "
    "Flows (confirmed directly from each year's own filing - the FY2024 filing, approved 24 "
    "April 2025, includes a complete Cash Flow Statement for both FY2024 and its FY2023 "
    "comparative). Only the FY2025 filing (approved 23 April 2026) newly invokes the FRS 101 "
    "exemption for IAS 7 'Statement of cash flows' - its Basis of Preparation note states the "
    "financial statements 'are presented with the benefit of the disclosure exemptions "
    "permitted by FRS 101 with regards to: IAS 7, Statement of cash flows... standards not yet "
    "effective', and no cash flow statement (for FY2025 OR its FY2024 comparative) appears "
    "anywhere in that filing. This is a mirror-image of Tandem Bank/AIB Group UK/Atom Bank's "
    "'exemption kicks in partway through the window' pattern - here it only blocks the LAST "
    "year rather than the earlier years, so FY2021-FY2024 are built as a normal full cash flow "
    "statement and only FY2025 is left blank with this note.\n\n"
    "PRESENTATION FORMAT NOTE: FY2021's own filing discloses only a single aggregate operating "
    "cash flow figure (no trading-activities/working-capital breakdown, no investing/financing "
    "sections) - this is the source's own presentation for that year, not a gap. FY2022-FY2024 "
    "(sourced from the FY2023 and FY2024 filings, whose comparative/current columns cross-"
    "check exactly) use a fuller breakdown. Blank cells on the more granular rows for FY2021 "
    "reflect this genuine presentation difference; the year's one available total is placed on "
    "the 'Net cash (used in)/generated from operating activities' row.\n\n"
    "Full opening-to-closing chain cross-checked and ties exactly across all 4 years with cash "
    "flow data: FY2021 closing (5,128,808) = FY2022 opening; FY2022 closing (5,671,848) = "
    "FY2023 opening; FY2023 closing (5,383,852) = FY2024 opening; FY2024 closing = 5,540,507, "
    "matching the FY2024 Balance Sheet's own 'Loans and advances to banks' figure exactly."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Cater Allen Limited's own Cash Flow Statement, GBP'000:\n"
    f"FY2021: Annual Report and Financial Statements 2021, p.14 (Cash Flow Statement) and p.35 "
    f"(Note 24, reconciliation) - {AR2021_URL}\n"
    f"FY2022 (restated comparative, used as primary column per project convention): Annual "
    f"Report and Financial Statements 2023, p.26 (Cash Flow Statement, 2022 restated column) - {AR2023_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.26 (Cash Flow Statement) - {AR2023_URL}\n"
    f"FY2024: Annual Report and Financial Statements 2024, p.27 (Cash Flow Statement) - {AR2024_URL}\n"
    f"FY2025: Not applicable - FRS 101 cash-flow exemption newly taken this year. Annual Report "
    f"and Financial Statements 2025, p.29 (Note 1, Basis of preparation) - {AR2025_URL}\n\n"
    + ENTITY_NOTE
)

rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax", {"FY2024": 168882, "FY2023": 169529, "FY2022": 67307}),
    ("DATA", "Effect of foreign exchange rates on loans and advances to banks",
     {"FY2024": -81, "FY2023": 3545, "FY2022": -10493}),
    ("DATA", "Amortisation of intangible assets", {"FY2024": 2771, "FY2023": 2905, "FY2022": 2905}),
    ("DATA", "Impairment reversal", {"FY2022": -35}),
    ("TOTAL", "Net cash flow from trading activities", {"FY2024": 171572, "FY2023": 175979, "FY2022": 59684}),
    ("DATA", "Decrease in loans and advances to customers", {"FY2022": 35}),
    ("DATA", "Decrease/(increase) in other assets", {"FY2024": 3044, "FY2023": -2207, "FY2022": -10406}),
    ("DATA", "Increase/(decrease) in customer accounts", {"FY2024": 135483, "FY2023": -348801, "FY2022": 782202}),
    ("DATA", "Increase/(decrease) in deposits by banks", {"FY2024": 2820, "FY2023": 2577, "FY2022": -1348}),
    ("DATA", "Increase in amounts due to other group companies", {"FY2024": 1736, "FY2023": 2073, "FY2022": 4061}),
    ("DATA", "(Decrease)/increase in other liabilities", {"FY2024": -9420, "FY2023": 4491, "FY2022": 8942}),
    ("DATA", "Settlement to Santander UK plc in respect of Corporation Tax",
     {"FY2024": -47048, "FY2023": -18170, "FY2022": -10623}),
    ("TOTAL", "Net cash (used in)/generated from operating activities",
     {"FY2024": 258187, "FY2023": -184058, "FY2022": 832547, "FY2021": -200379}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Intangible asset work in progress", {"FY2023": -393}),
    ("TOTAL", "Cash used in investing activities", {"FY2024": 0, "FY2023": -393, "FY2022": 0}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividend paid", {"FY2024": -100000, "FY2023": -100000, "FY2022": -300000}),
    ("TOTAL", "Cash used in financing activities", {"FY2024": -100000, "FY2023": -100000, "FY2022": -300000}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents",
     {"FY2024": 158187, "FY2023": -284451, "FY2022": 532547, "FY2021": -200379}),
    ("DATA", "Effect of foreign exchange rates", {"FY2024": -1532, "FY2023": -3545, "FY2022": 10493}),
    ("DATA", "Opening cash and cash equivalents",
     {"FY2024": 5383852, "FY2023": 5671848, "FY2022": 5128808, "FY2021": 5329187}),
    ("TOTAL", "Closing cash and cash equivalents",
     {"FY2024": 5540507, "FY2023": 5383852, "FY2022": 5671848, "FY2021": 5128808}),
]

bw = BankWorkbook(bank_name="Cater Allen Limited", years=YEARS, year_label=None, header_color="1A5276")

bw.add_cash_flow_sheet(
    title="Cater Allen Limited — Cash Flow Statement",
    subtitle="Entity basis, £'000. FY2025 not applicable — FRS 101 cash-flow exemption newly taken. See source note below.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=320,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 / capital metric sheets
# ---------------------------------------------------------------
CET1_CAPITAL = {"FY2025": 217373, "FY2024": 246095, "FY2023": 220848, "FY2022": 268414}
CET1_RATIO = {"FY2025": "78.20%", "FY2024": "98.74%", "FY2023": "122.8%", "FY2022": "246.5%"}
RWA_CALC = {"FY2025": 277971, "FY2024": 249235, "FY2023": 179844, "FY2022": 108890}

NOT_DISCLOSED_NOTE = (
    "Not publicly disclosed. Cater Allen's Annual Report discloses only CET1 capital ratio and "
    "Total Tier 1 Capital/Total Capital Resources (identical, since no AT1/Tier 2 instruments "
    "exist) via its Strategic Report KPI table and Capital risk note - no Leverage Ratio, LCR, "
    "NSFR, or MREL figures are disclosed at this entity level in any of the 4 years reviewed. "
    "No standalone Pillar 3 document exists; liquidity/capital management is described only "
    "narratively (managed centrally with Santander UK plc as part of the RFB Domestic "
    "Liquidity Sub-Group and the RFB Sub-Group Capital Support Deed)."
)

CAPITAL_SOURCES = (
    "Sources - Cater Allen Limited's own Annual Report, Strategic Report KPI table and Risk "
    "Review 'Capital risk' section (Capital table), GBP'000 except ratios:\n"
    f"FY2025: Annual Report and Financial Statements 2025, p.2 (KPIs) and p.12 (Capital) - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements 2024, p.2 (KPIs) and p.13 (Capital) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.2 (KPIs) and p.15 (Capital) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2023, p.2 (KPI comparative) and p.15 "
    f"(Capital table 2022 comparative) - {AR2023_URL}\n\n"
    "CET1 Capital = Tier 1 Capital = Total Capital every year - the Company's Tier 1 capital "
    "consists of shareholders' equity, share premium and audited prior-year profits (adjusted "
    "for foreseeable charges/dividends); no AT1 or Tier 2 instruments exist. FY2021 is "
    "genuinely not disclosed - the FY2021 Annual Report's KPI table and financial-statement "
    "notes predate this project's window's capital-ratio disclosure format and contain no "
    "capital-adequacy figures of any kind."
)


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, CAPITAL_SOURCES, note=note, first_col_width=52, source_height=220)


metric("CET1 Capital", "£'000", [("Total Capital Resources (= CET1 Capital)", CET1_CAPITAL)])
metric("CET1 Ratio", "%", [("CET1 capital ratio", CET1_RATIO)])
metric("Tier 1 Capital", "£'000 (= CET1 Capital; no AT1 instruments)", [("Total Tier 1 Capital Resources", CET1_CAPITAL)])
metric("Tier 1 Ratio", "%", [("CET1 capital ratio (= Tier 1 Ratio; no AT1 instruments)", CET1_RATIO)])
metric("Total Capital", "£'000 (= CET1 Capital; no Tier 2 instruments)", [("Total Capital Resources", CET1_CAPITAL)])
metric("Total Capital Ratio", "%", [("CET1 capital ratio (= Total Capital Ratio; no AT1/Tier 2 instruments)", CET1_RATIO)])
metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted assets", RWA_CALC)],
    note="CALCULATED, not directly disclosed - derived as Total Capital Resources ÷ CET1 "
         "capital ratio for each year. No RWA figure appears in any source reviewed.",
)

bw.add_not_disclosed_metric_sheets(
    ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"],
    CAPITAL_SOURCES,
    per_note={m: NOT_DISCLOSED_NOTE for m in ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"]},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash (used in)/generated from operating activities",
         {"FY2024": 258187, "FY2023": -184058, "FY2022": 832547, "FY2021": -200379}),
        ("Cash used in investing activities", {"FY2024": 0, "FY2023": -393, "FY2022": 0}),
        ("Closing cash and cash equivalents",
         {"FY2024": 5540507, "FY2023": 5383852, "FY2022": 5671848, "FY2021": 5128808}),
    ],
    cash_flow_unit=" (£'000)",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Total Capital Ratio", CET1_RATIO),
    ],
)

bw.save("/Users/armaan/code/katalysis/banks/CATER ALLEN FINANCIALS.xlsx")
