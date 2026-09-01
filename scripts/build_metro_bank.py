import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

AR_2021 = "https://www.metrobankonline.co.uk/globalassets/documents/customer_documents/intermediaries/metro-bank-annual-report-2021.pdf"
AR_2022 = "https://www.metrobankonline.co.uk/globalassets/documents/customer_documents/business-and-commercial/metro-bank-annual-report-and-accounts-2022.pdf.pdf"
AR_2023 = "https://www.metrobankonline.co.uk/globalassets/documents/customer_documents/business-and-commercial/metro-bank-plc-annual-report-2023.pdf"
AR_2024 = "https://www.metrobankonline.co.uk/globalassets/documents/customer_documents/personal/metro-bank-annual-report-2024.pdf"
AR_2025 = "https://www.metrobankonline.co.uk/globalassets/documents/investor_documents/metro-bank---annual-report-2025.pdf"
P3_2021 = "https://www.metrobankonline.co.uk/globalassets/documents/customer_documents/intermediaries/metro-bank-pillar-3-disclosure-2021.pdf"
P3_H1_2022 = "https://www.metrobankonline.co.uk/globalassets/documents/customer_documents/business-and-commercial/pillar-3-disclosure---h1-2022.pdf"
P3_H1_2023 = "https://www.metrobankonline.co.uk/globalassets/documents/customer_documents/personal/pillar-3-disclosure-h1-2023.pdf"
P3_H1_2024 = "https://www.metrobankonline.co.uk/globalassets/documents/customer_documents/intermediaries/pillar-3-disclosure-h1-2024.pdf"
P3_H1_2025 = "https://www.metrobankonline.co.uk/globalassets/h1-2025-pillar-3-final.pdf"
P3_2022 = "https://www.metrobankonline.co.uk/globalassets/documents/customer_documents/business-and-commercial/pillar-3-disclosure-2022.pdf"
P3_2023 = "https://www.metrobankonline.co.uk/globalassets/pillar-3-disclosure-2023.pdf"
P3_2024 = "https://www.metrobankonline.co.uk/globalassets/pillar-3-2024.pdf"
P3_2025 = "https://www.metrobankonline.co.uk/globalassets/documents/investor_documents/pillar-3---2025-final.pdf"

ENTITY_NOTE = (
    "ENTITY/BASIS NOTE: Metro Bank PLC (Companies House 06419578; FRN 488982; LEI "
    "213800X5WU57YL9GPK89) is the matched legal entity in Banks List 2608.xlsx. "
    "FY2021-FY2023 cash flows are the Company/standalone figures from Metro Bank PLC "
    "accounts. Metro Bank PLC used an individual consolidation method for prudential "
    "reporting in 2021-2022. On 19 May 2023 Metro Bank Holdings PLC became the ultimate "
    "holding company; FY2023-FY2025 Pillar 3 disclosures are subsequently for Holdings "
    "and its subsidiaries, not standalone Metro Bank PLC. FY2024-FY2025 standalone Metro "
    "Bank PLC accounts/cash flows were not located in the reviewed official archive and "
    "are left blank rather than substituted with Holdings figures."
)

CASH_SOURCES = (
    "Sources - Metro Bank PLC Company/standalone cash flows, £m:\n"
    f"FY2023 & FY2022: Metro Bank PLC Annual Report 2023, p.147 (Company cash flow statement) - {AR_2023}\n"
    f"FY2022 & FY2021: Metro Bank PLC Annual Report and Accounts 2022, p.185 (Company column) - {AR_2022}\n"
    f"FY2021: Metro Bank PLC Annual Report and Accounts 2021, p.165 (Company column) - {AR_2021}\n\n"
    + ENTITY_NOTE
)

P3_SOURCES = (
    "Sources - Metro Bank regulatory key metrics:\n"
    f"FY2025: Metro Bank Holdings PLC Pillar 3 Disclosure 2025, p.10 - {P3_2025}\n"
    f"FY2024: Metro Bank Holdings PLC Pillar 3 Disclosure 2024, p.12 - {P3_2024}\n"
    f"FY2023: Metro Bank Holdings PLC Pillar 3 Disclosure 2023, p.12 - {P3_2023}\n"
    f"FY2022: Metro Bank PLC Pillar 3 Disclosure 2022, p.10 - {P3_2022}\n"
    f"FY2021: Metro Bank PLC Pillar 3 Disclosure 2021, p.4 - {P3_2021}\n\n"
    + ENTITY_NOTE
)

bw = BankWorkbook(bank_name="Metro Bank PLC", years=YEARS, year_label=YEAR_LABEL, header_color="00695C")

cash_rows = [
    ("SECTION", "Reconciliation of profit/(loss) before tax to net cash flows from operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {"FY2023": 46, "FY2022": -71, "FY2021": -245}),
    ("DATA", "Adjustments for non-cash items", {"FY2023": -376, "FY2022": -259, "FY2021": -132}),
    ("DATA", "Interest received", {"FY2023": 834, "FY2022": 538, "FY2021": 394}),
    ("DATA", "Interest paid", {"FY2023": -370, "FY2022": -124, "FY2021": -126}),
    ("DATA", "Changes in other operating assets", {"FY2023": 729, "FY2022": -842, "FY2021": 2613}),
    ("DATA", "Changes in other operating liabilities", {"FY2023": -251, "FY2022": -409, "FY2021": 370}),
    ("TOTAL", "Net cash inflows/(outflows) from operating activities", {"FY2023": 612, "FY2022": -1167, "FY2021": 2874}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Sales of investment securities", {"FY2023": 1870, "FY2022": 857, "FY2021": 1269}),
    ("DATA", "Purchase of investment securities", {"FY2023": -816, "FY2022": -1206, "FY2021": -3438}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2023": -12, "FY2022": -29, "FY2021": -41}),
    ("DATA", "Purchase and development of intangible assets", {"FY2023": -26, "FY2022": -24, "FY2021": -64}),
    ("DATA", "Dividends received from subsidiaries", {"FY2023": 12}),
    ("TOTAL", "Net cash inflows/(outflows) from investing activities", {"FY2023": 1028, "FY2022": -402, "FY2021": -2274}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Repayment of capital elements of leases", {"FY2023": -23, "FY2022": -25, "FY2021": -27}),
    ("DATA", "Issuance of new shares", {"FY2023": 144}),
    ("DATA", "Issuance of medium-term notes/subordinated debt (net of costs)", {"FY2023": 175}),
    ("TOTAL", "Net cash inflows/(outflows) from financing activities", {"FY2023": 296, "FY2022": -25, "FY2021": -27}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2023": 1936, "FY2022": -1594, "FY2021": 573}),
    ("DATA", "Cash and cash equivalents at start of year", {"FY2023": 1953, "FY2022": 3547, "FY2021": 2974}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2023": 3889, "FY2022": 1953, "FY2021": 3547}),
]

bw.add_cash_flow_sheet(
    title="Metro Bank PLC - Company Cash Flow Statement",
    subtitle="Company/standalone basis, £m; 31 December year-end. FY2024-FY2025 standalone accounts not located.",
    rows=cash_rows, sources_text=CASH_SOURCES, first_col_width=72, source_height=220, unit_suffix=" (£m)",
)


def vals(data):
    return {y: data.get(y) for y in YEARS}


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, P3_SOURCES, note=note, first_col_width=56, source_height=190)


metric("CET1 Capital", "£m", [("Common Equity Tier 1 (CET1) capital", vals({"FY2025": 826, "FY2024": 937, "FY2023": 813, "FY2022": 819, "FY2021": 936}))],
       "FY2023-FY2025 are Holdings Group figures following the May 2023 holding-company insertion; FY2021-FY2022 are Metro Bank PLC consolidated prudential figures.")
metric("CET1 Ratio", "%", [("Common Equity Tier 1 ratio", vals({"FY2025": "12.8%", "FY2024": "12.9%", "FY2023": "10.4%", "FY2022": "10.3%", "FY2021": "12.6%"}))])
metric("Tier 1 Capital", "£m", [("Tier 1 capital", vals({"FY2025": 1068, "FY2024": 937, "FY2023": 813, "FY2022": 819, "FY2021": 936}))])
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", vals({"FY2025": "16.6%", "FY2024": "12.9%", "FY2023": "10.4%", "FY2022": "10.3%", "FY2021": "12.6%"}))])
metric("Total Capital", "£m", [("Total capital", vals({"FY2025": 1218, "FY2024": 1087, "FY2023": 1030, "FY2022": 1069, "FY2021": 1184}))])
metric("Total Capital Ratio", "%", [("Total capital ratio", vals({"FY2025": "18.9%", "FY2024": "15.0%", "FY2023": "13.2%", "FY2022": "13.4%", "FY2021": "15.9%"}))])
metric("Total RWAs", "£m", [("Total risk-weighted exposure amount", vals({"FY2025": 6437, "FY2024": 7239, "FY2023": 7802, "FY2022": 7990, "FY2021": 7454}))])
metric("Leverage Ratio", "£m / %", [
    ("Total exposure measure excluding claims on central banks", vals({"FY2025": 13560, "FY2024": 17185, "FY2023": 18550, "FY2022": 19348, "FY2021": 17869})),
    ("Leverage ratio excluding claims on central banks", vals({"FY2025": "7.9%", "FY2024": "5.5%", "FY2023": "4.4%", "FY2022": "4.2%", "FY2021": "5.2%"})),
], note="The 2023-2025 figures are Holdings Group figures; 2021-2022 are the Metro Bank PLC prudential perimeter. The 2021-2022 disclosures restate the leverage measure to exclude central-bank claims for comparability.")
metric("LCR", "£m / %", [
    ("Total high-quality liquid assets (HQLA), weighted value - average", vals({"FY2025": 6289, "FY2024": 6509, "FY2023": 5063, "FY2022": 6051, "FY2021": 6900})),
    ("Total net cash outflows, adjusted value", vals({"FY2025": 1689, "FY2024": 2037, "FY2023": 2310, "FY2022": 2465, "FY2021": 2169})),
    ("Liquidity Coverage Ratio", vals({"FY2025": "427%", "FY2024": "319%", "FY2023": "219%", "FY2022": "246%", "FY2021": "281%"})),
], note="The source tables disclose HQLA/net outflow components on different reporting bases across years; the headline ratios are reproduced as reported. Basis changes after the holding-company insertion are described on the Cash Flow Statement and source note.")
metric("NSFR", "£m / %", [
    ("Total available stable funding", vals({"FY2025": 14465, "FY2024": 18361, "FY2023": 18564, "FY2022": 18903})),
    ("Total required stable funding", vals({"FY2025": 8560, "FY2024": 12512, "FY2023": 13790, "FY2022": 13225})),
    ("Net stable funding ratio", vals({"FY2025": "169%", "FY2024": "147%", "FY2023": "135%", "FY2022": "143%"})),
], note="NSFR disclosures were required from 1 January 2023; FY2021 is blank. FY2023-FY2025 are Holdings Group figures after the restructure.")
metric("MREL Ratio", "%", [("MREL ratio", vals({"FY2021": "20.5%", "FY2022": "Not disclosed", "FY2023": "Not disclosed", "FY2024": "Not disclosed", "FY2025": "Not disclosed"}))],
       "The 2021 Pillar 3 report discloses 20.5%. No quantitative MREL ratio was located in the later KM1 tables reviewed; the 2022-2025 cells are therefore not publicly disclosed rather than zero.")


INTERIM_HEADERS = ["Period", "Disclosure type", "Metric", "Value", "Unit", "Basis", "Source document", "Page / table"]
INTERIM_METRICS = [
    ("CET1 capital", [1052, 816], "£m"),
    ("Tier 1 capital", [1052, 816], "£m"),
    ("Total capital", [1301, 1065], "£m"),
    ("Total risk-weighted exposure amount", [7563, 7702], "£m"),
    ("CET1 ratio", ["13.9%", "10.6%"], "%"),
    ("Tier 1 ratio", ["13.9%", "10.6%"], "%"),
    ("Total capital ratio", ["17.2%", "13.8%"], "%"),
    ("Total exposure measure excluding claims on central banks", [16909, 18809], "£m"),
    ("Leverage ratio excluding claims on central banks", ["6.2%", "4.3%"], "%"),
    ("Total HQLA, weighted value - average", [None, 6687], "£m"),
    ("Total net cash outflows, adjusted value", [None, 2374], "£m"),
    ("Liquidity coverage ratio", [None, "282%"], "%"),
    ("Total available stable funding", ["Not yet required", "Not disclosed"], "£m"),
    ("Total required stable funding", ["Not yet required", "Not disclosed"], "£m"),
    ("NSFR ratio", ["Not yet required", "Not disclosed"], "%"),
    ("MREL ratio", ["Not disclosed", "Not disclosed"], "%"),
]
interim_rows = []
for period, values, source, page in [
    ("30 Jun 2021", 0, P3_H1_2022, "3, UK KM1"),
    ("30 Jun 2022", 1, P3_H1_2022, "3, UK KM1"),
]:
    for metric_name, metric_values, unit in INTERIM_METRICS:
        interim_rows.append([period, "H1 Pillar 3 disclosure", metric_name, metric_values[values], unit, "Metro Bank PLC consolidated basis", source, page])
for period, source in [("30 Jun 2023", P3_H1_2023), ("30 Jun 2024", P3_H1_2024), ("30 Jun 2025", P3_H1_2025)]:
    interim_rows.append([period, "H1 Pillar 3 disclosure", "All Metro Bank PLC entity-level interim metrics", "Not separately disclosed", "n/a", "Metro Bank Holdings PLC group disclosure after 19 May 2023 restructure", source, "Basis note"])

bw.add_wide_interim_sheet(
    "Interim Pillar 3", rows=interim_rows,
    hyperlink_cells={(i, 6): row[6] for i, row in enumerate(interim_rows)},
    title="Metro Bank PLC - Interim Pillar 3 Disclosures",
    subtitle="Entity-level Metro Bank PLC basis where available; later Holdings Group disclosures are not substituted.",
    note="H1 2021 and H1 2022 use the official Metro Bank PLC consolidated UK KM1 table. From 19 May 2023 the ultimate holding company changed to Metro Bank Holdings PLC; H1 2023-H1 2025 official disclosures are Holdings Group figures and do not provide a defensible standalone Metro Bank PLC series, so those periods are explicitly recorded as not separately disclosed.",
)


def cash_value(label):
    return next(v for kind, name, v in cash_rows if name == label)


bw.add_overview_sheet(
    cash_flow_totals=[(label, cash_value(label)) for label in [
        "Net cash inflows/(outflows) from operating activities",
        "Net cash inflows/(outflows) from investing activities",
        "Net cash inflows/(outflows) from financing activities",
        "Cash and cash equivalents at end of year",
    ]],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", vals({"FY2025": "12.8%", "FY2024": "12.9%", "FY2023": "10.4%", "FY2022": "10.3%", "FY2021": "12.6%"})),
        ("Total Capital Ratio", vals({"FY2025": "18.9%", "FY2024": "15.0%", "FY2023": "13.2%", "FY2022": "13.4%", "FY2021": "15.9%"})),
        ("Leverage Ratio", vals({"FY2025": "7.9%", "FY2024": "5.5%", "FY2023": "4.4%", "FY2022": "4.2%", "FY2021": "5.2%"})),
        ("LCR", vals({"FY2025": "427%", "FY2024": "319%", "FY2023": "219%", "FY2022": "246%", "FY2021": "281%"})),
        ("NSFR", vals({"FY2025": "169%", "FY2024": "147%", "FY2023": "135%", "FY2022": "143%"})),
    ],
    note="Metro Bank PLC entity basis. FY2024-FY2025 company cash-flow data is blank because the reviewed official reports are Holdings PLC reports rather than standalone Metro Bank PLC accounts. Regulatory figures change from Metro Bank PLC consolidated basis to Holdings Group basis after the 19 May 2023 restructure; see the metric and interim-sheet notes.",
)

bw.save("/Users/armaan/code/katalysis/banks/METRO BANK FINANCIALS.xlsx")
