import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

# Companies House filings for Monument Bank Limited (company 10921940).
AR25_URL = "https://find-and-update.company-information.service.gov.uk/company/10921940/filing-history/MzQ3Njc0NjA3MmFkaXF6a2N4/document?download=0&format=pdf"
AR24_URL = "https://find-and-update.company-information.service.gov.uk/company/10921940/filing-history/MzQzNjUxODg2NmFkaXF6a2N4/document?download=0&format=pdf"
AR23_URL = "https://find-and-update.company-information.service.gov.uk/company/10921940/filing-history/MzM5NDQyODAwN2FkaXF6a2N4/document?download=0&format=pdf"
AR22_URL = "https://find-and-update.company-information.service.gov.uk/company/10921940/filing-history/MzM1Mjc4MTU2M2FkaXF6a2N4/document?download=0&format=pdf"

ENTITY_NOTE = (
    "ENTITY/BASIS NOTE: Monument Bank Limited (Companies House 10921940; FRN 849724; "
    "LEI 213800OLF8OE1I3HVY91) is the matched legal entity in Banks List 2608.xlsx. "
    "Cash flows are the Company/standalone figures in £'000. The latest available filing "
    "is the report for the year ended 31 December 2024; FY2025 is blank because no FY2025 "
    "accounts were available in the Companies House filing history reviewed. The accounts "
    "are scanned filings and were OCR-processed and cross-checked against rendered pages. "
    "Blank cells mean not publicly disclosed, not zero."
)

CASH_SOURCES = (
    "Sources - Monument Bank Limited Company/standalone cash flows, £'000:\n"
    f"FY2024 & FY2023: Financial Statements for the year ended 31 December 2024, pp.74-75 (Company columns) - {AR25_URL}\n"
    f"FY2023 & FY2022: Financial Statements for the year ended 31 December 2023, p.35 (Company figures; FY2022 comparative) - {AR24_URL}\n"
    f"FY2022 & FY2021: Financial Statements for the year ended 31 December 2022, p.29 - {AR23_URL}\n"
    f"FY2021: Financial Statements for the year ended 31 December 2021, p.25 - {AR22_URL}\n\n"
    + ENTITY_NOTE
)

P3_SOURCES = (
    "Sources - Monument Bank Limited annual regulatory KPIs and risk disclosures:\n"
    f"FY2024 & FY2023: Financial Statements for the year ended 31 December 2024, pp.11-12 and 74 - {AR25_URL}\n"
    f"FY2023 & FY2022: Financial Statements for the year ended 31 December 2023, pp.8-9 and 60-61 - {AR24_URL}\n"
    f"FY2022 & FY2021: Financial Statements for the year ended 31 December 2022, pp.10 and 51 - {AR23_URL}\n"
    f"FY2021: Financial Statements for the year ended 31 December 2021, pp.9 and 41 - {AR22_URL}\n\n"
    "The reports do not provide a complete UK KM1 table for every year. Only explicitly disclosed "
    "entity-level values are populated; unavailable capital components and ratios remain blank."
)

bw = BankWorkbook(bank_name="Monument Bank Limited", years=YEARS, header_color="5B2C6F")

rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Loss for the financial year", {"FY2024": -13086, "FY2023": -19360, "FY2022": -12709.555, "FY2021": -9973.318}),
    ("DATA", "Amortisation charges", {"FY2024": 3538, "FY2023": 2793.918, "FY2022": 2175.212, "FY2021": 128.659}),
    ("DATA", "Depreciation charges", {"FY2024": 95, "FY2023": 69.739, "FY2022": 57.660, "FY2021": 28.517}),
    ("DATA", "Impairment charge on loans and advances to customers", {"FY2024": 79, "FY2023": 82.581, "FY2022": 101.980, "FY2021": 2.664}),
    ("DATA", "Employee share scheme charge", {"FY2024": 1389, "FY2023": 608.050, "FY2022": 718.696, "FY2021": 613.561}),
    ("DATA", "Increase in loans and advances to customers", {"FY2024": -34229, "FY2023": -46400.642, "FY2022": -92714.010, "FY2021": -761.749}),
    ("DATA", "Increase in customer deposits", {"FY2024": 4079222, "FY2023": 842843.947, "FY2022": 145564.821, "FY2021": 2093.036}),
    ("DATA", "Increase in other assets", {"FY2024": -54, "FY2023": -1418.529, "FY2022": -112.616, "FY2021": -688.421}),
    ("DATA", "Increase/(decrease) in other liabilities", {"FY2024": 1465, "FY2023": -256.431, "FY2022": 332.370, "FY2021": -206.864}),
    ("DATA", "Decrease/(increase) in derivative financial instruments", {"FY2024": -642, "FY2023": 2331.057, "FY2022": -2576.137}),
    ("DATA", "Decrease/(increase) in treasury bills", {"FY2024": 130102, "FY2023": -130101.590}),
    ("DATA", "Increase in debt securities", {"FY2024": -843959, "FY2023": -373373.722}),
    ("TOTAL", "Net cash from/(used in) operating activities", {"FY2024": 3323920, "FY2023": 277818.774, "FY2022": 40838.421, "FY2021": -8763.915}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Expenditure on internally generated intangible assets", {"FY2024": -4507, "FY2023": -3417.546, "FY2022": -3256.064, "FY2021": -8307.109}),
    ("DATA", "Purchase of tangible fixed assets", {"FY2024": -192, "FY2023": -72.485, "FY2022": -78.582, "FY2021": -139.569}),
    ("DATA", "Purchase of financial investments", {"FY2022": -242.496, "FY2021": -10300}),
    ("TOTAL", "Net cash used in investing activities", {"FY2024": -4699, "FY2023": -3490.041, "FY2022": -3577.142, "FY2021": -18746.678}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Share issuance", {"FY2024": 31183, "FY2023": 23233.150, "FY2022": 1728.142, "FY2021": 25561.125}),
    ("DATA", "Cost of share issuance", {"FY2024": -2687, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Cash inflows from shares to be issued", {"FY2024": 48, "FY2023": 13980.144, "FY2022": 2796, "FY2021": 724.816}),
    ("TOTAL", "Net cash from financing activities", {"FY2024": 28544, "FY2023": 37213.294, "FY2022": 4524.142, "FY2021": 26285.941}),
    ("TOTAL", "Increase/(decrease) in cash and cash equivalents", {"FY2024": 3347765, "FY2023": 311542.027, "FY2022": 41785.421, "FY2021": -1224.652}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2024": 377215, "FY2023": 65673.758, "FY2022": 23888.337, "FY2021": 25112.989}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2024": 3724980, "FY2023": 377215.785, "FY2022": 65673.758, "FY2021": 23888.337}),
]

bw.add_cash_flow_sheet(
    title="Monument Bank Limited - Company Cash Flow Statement",
    subtitle="Company/standalone basis, £'000; 31 December year-end. FY2025 not yet filed.",
    rows=rows, sources_text=CASH_SOURCES, first_col_width=68, source_height=240,
    unit_suffix=" (£'000)",
)

def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, P3_SOURCES, note=note, first_col_width=56, source_height=180)

def vals(data):
    return {y: data.get(y) for y in YEARS}

metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", vals({"FY2024": 56324, "FY2023": 28035.733, "FY2022": 21299.969, "FY2021": 32643.538}))])
metric("CET1 Ratio", "%", [("Common Equity Tier 1 (CET1) ratio", vals({"FY2024": "20%", "FY2023": "22%"}))], "The annual reports disclose CET1 capital and, from 2023 onward, the CET1 ratio; earlier ratios were not separately disclosed.")
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", vals({}))], "No standalone Tier 1 capital amount was separately disclosed in the reports reviewed.")
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", vals({}))], "No standalone Tier 1 ratio was separately disclosed in the reports reviewed.")
metric("Total Capital", "£'000", [("Total capital", vals({}))], "No standalone total capital amount was separately disclosed in the reports reviewed.")
metric("Total Capital Ratio", "%", [("Total capital ratio", vals({"FY2022": "44%", "FY2021": "529%"}))], "The 2023 report states 44% for FY2022 and the 2024 report does not repeat a total capital ratio for FY2023/FY2024; FY2021 is reported as 529%.")
metric("Total RWAs", "£'000", [("Total risk-weighted assets", vals({"FY2024": 281756, "FY2023": 126528}))], "Total RWAs were disclosed in the 2024 report’s regulatory metrics table; earlier totals were not separately disclosed.")
metric("Leverage Ratio", "%", [("Leverage ratio", vals({"FY2024": "3.9%", "FY2023": "4.1%"}))])
metric("LCR", "%", [("Liquidity coverage ratio", vals({"FY2024": "589%", "FY2023": "1,093%", "FY2022": "10,128%", "FY2021": "2,861,111,111%"}))], "FY2021’s unusually high percentage is reproduced exactly as printed in the 2021 accounts; it is not normalised or inferred.")
metric("NSFR", "%", [("Net stable funding ratio", vals({"FY2024": "560%", "FY2023": "228%"}))], "NSFR was disclosed in the FY2024 report’s regulatory metrics table; no earlier standalone figure was located.")
metric("MREL Ratio", None, [("MREL ratio", vals({}))], "No quantitative MREL ratio was located in the official annual reports reviewed.")

def row_values(label):
    return next(values for kind, name, values in rows if name == label)

bw.add_overview_sheet(
    cash_flow_totals=[(label, row_values(label)) for label in [
        "Net cash from/(used in) operating activities",
        "Net cash used in investing activities",
        "Net cash from financing activities",
        "Cash and cash equivalents at end of year",
    ]],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", vals({"FY2024": "20%", "FY2023": "22%"})),
        ("Total Capital Ratio", vals({"FY2022": "44%", "FY2021": "529%"})),
        ("Leverage Ratio", vals({"FY2024": "3.9%", "FY2023": "4.1%"})),
        ("LCR", vals({"FY2024": "589%", "FY2023": "1,093%", "FY2022": "10,128%", "FY2021": "2,861,111,111%"})),
        ("NSFR", vals({"FY2024": "560%", "FY2023": "228%"})),
    ],
    note="Monument Bank Limited standalone/Company basis. FY2025 is blank because the latest available Companies House accounts cover 31 December 2024. Pillar 3 sheets contain only explicitly disclosed annual regulatory values; blank cells mean not disclosed.",
)

bw.save("/Users/armaan/code/katalysis/banks/MONUMENT BANK FINANCIALS.xlsx")
