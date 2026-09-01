import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/01448919/filing-history/MzUyMjY1MjQyNWFkaXF6a2N4/document?download=0&format=pdf"
AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/01448919/filing-history/MzQ3MzI5ODI4OWFkaXF6a2N4/document?download=0&format=pdf"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/01448919/filing-history/MzQyMjI5MjUwM2FkaXF6a2N4/document?download=0&format=pdf"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/01448919/filing-history/MzM4MTE3NjI0OGFkaXF6a2N4/document?download=0&format=pdf"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/01448919/filing-history/MzM0MjM1MjU5OWFkaXF6a2N4/document?download=0&format=pdf"
PILLAR_URL = "https://www.rathbones.com/sites/rathbones.com/files/results_and_presentations/files/31_december_2024_pillar_3_disclosures.pdf"

ENTITY_NOTE = (
    "Entity: Rathbones Investment Management Limited (FRN 116316, company 01448919), formerly "
    "Rathbone Investment Management Limited until 7 December 2022. The Company is a wholly-owned "
    "subsidiary of Rathbones Group Plc and prepares entity-only IFRS financial statements under the "
    "Companies Act 2006 Section 400 exemption from consolidated accounts. Figures are GBP'000. "
    "The Company is an investment and wealth-management business, not the consolidated Rathbones Group.\n\n"
    "Pillar 3 metrics are not substituted from Rathbones Group Plc: the official 2024 Pillar 3 report "
    "states that disclosures are consolidated and that no large subsidiary meets the definition requiring "
    "individual disclosure. Accordingly, entity-level CET1, Tier 1, Total Capital, RWA, leverage, LCR, "
    "NSFR and MREL figures are not publicly disclosed in the Company's accounts. The 2021 own-account "
    "closing cash (£1,530,445k) does not equal the 2022 account's comparative opening cash (£1,527,887k); "
    "both source-presented figures are retained and the difference is not inferred or forced."
)

CASH_SOURCES = (
    "Sources - Rathbones Investment Management Limited statutory Statement of cash flows, GBP'000. "
    "Each year's own column was checked against the next year's comparative column where available.\n"
    f"FY2025 and FY2024 comparative: Annual report and financial statements 2025, p.25 - {AR2025_URL}\n"
    f"FY2024 and FY2023 comparative: Annual report and financial statements 2024, p.28 - {AR2024_URL}\n"
    f"FY2023 and FY2022 comparative: Annual report and financial statements 2023, p.29 - {AR2023_URL}\n"
    f"FY2022 and FY2021 comparative: Annual report and financial statements 2022, p.29 - {AR2022_URL}\n"
    f"FY2021: Annual report and financial statements 2021, p.29 - {AR2021_URL}\n\n"
    + ENTITY_NOTE
)

rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax", {"FY2025":111473,"FY2024":21167,"FY2023":63864,"FY2022":49174,"FY2021":75198}),
    ("DATA", "Change in fair value through profit or loss", {"FY2024":19,"FY2023":-958,"FY2022":-588}),
    ("DATA", "Net charge for provisions", {"FY2025":6493,"FY2024":1962,"FY2023":1914,"FY2022":150,"FY2021":1436}),
    ("DATA", "Net interest income", {"FY2025":-83158,"FY2024":-56469,"FY2023":-49638,"FY2022":-22576,"FY2021":-6657}),
    ("DATA", "Impairment losses on financial instruments", {"FY2025":4,"FY2024":17,"FY2023":-7,"FY2022":-39,"FY2021":-727}),
    ("DATA", "Profit on disposal of property, plant and equipment", {"FY2023":0,"FY2022":0,"FY2021":67}),
    ("DATA", "Depreciation and amortisation", {"FY2025":43690,"FY2024":23492,"FY2023":22843,"FY2022":22072,"FY2021":23966}),
    ("DATA", "Impairment in investment in subsidiary", {"FY2025":43888}),
    ("DATA", "Foreign exchange movements", {"FY2025":3025,"FY2024":-1012,"FY2023":3433,"FY2022":-7078,"FY2021":-519}),
    ("DATA", "Interest paid", {"FY2025":-74032,"FY2024":-81871,"FY2023":-67542,"FY2022":-19438,"FY2021":-1300}),
    ("DATA", "Interest received", {"FY2025":150214,"FY2024":137180,"FY2023":93817,"FY2022":31519,"FY2021":-10470}),
    ("DATA", "Net (increase)/decrease in loans and advances to banks and customers", {"FY2025":-81775,"FY2024":21867,"FY2023":87017,"FY2022":7357,"FY2021":-38715}),
    ("DATA", "Net (increase)/decrease in settlement balance debtors", {"FY2025":-9406,"FY2024":3800,"FY2023":-19223,"FY2022":9006,"FY2021":14260}),
    ("DATA", "Net increase/(decrease) in prepayments, accrued income and other assets", {"FY2025":-57400,"FY2024":-41320,"FY2023":21727,"FY2022":-13828,"FY2021":-364}),
    ("DATA", "Net increase/(decrease) in amounts due to customers and deposits by banks", {"FY2025":938715,"FY2024":172629,"FY2023":-251998,"FY2022":231254,"FY2021":-260531}),
    ("DATA", "Net increase/(decrease) in settlement balance creditors", {"FY2025":15921,"FY2024":5283,"FY2023":10914,"FY2022":3910,"FY2021":-27472}),
    ("DATA", "Net increase/(decrease) in accruals, deferred income, provisions and other liabilities", {"FY2025":14555,"FY2024":3739,"FY2023":-239,"FY2022":-2741,"FY2021":2395}),
    ("DATA", "Tax paid", {"FY2025":-34027,"FY2024":-10227,"FY2023":-15392,"FY2022":-11426,"FY2021":-19676}),
    ("TOTAL", "Net cash inflow/(outflow) from operating activities", {"FY2025":988180,"FY2024":200256,"FY2023":-99468,"FY2022":276728,"FY2021":-249109}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Cash acquired on acquisition of subsidiaries", {"FY2025":46460}),
    ("DATA", "Acquisition of investment in subsidiary undertaking", {"FY2021":0}),
    ("DATA", "Purchase of property, plant and equipment and intangible assets", {"FY2025":-16629,"FY2024":-20925,"FY2023":-6521,"FY2022":-8561,"FY2021":-17275}),
    ("DATA", "Proceeds from sale of equity securities", {"FY2024":1162,"FY2023":2922}),
    ("DATA", "Purchase of investment securities", {"FY2025":-2690119,"FY2024":-2027961,"FY2023":-2059899,"FY2022":-1259979,"FY2021":-930728}),
    ("DATA", "Proceeds from sale and redemption of investment securities", {"FY2025":2101020,"FY2024":2045349,"FY2023":1807092,"FY2022":983481,"FY2021":821100}),
    ("TOTAL", "Net cash used in investing activities", {"FY2025":-559268,"FY2024":-2375,"FY2023":-256406,"FY2022":-285059,"FY2021":-126903}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividends paid", {"FY2025":-69000,"FY2024":-27000,"FY2023":-50000,"FY2022":-35000,"FY2021":-55000}),
    ("DATA", "Payment of lease liabilities", {"FY2022":-81,"FY2021":-90}),
    ("TOTAL", "Net cash used in financing activities", {"FY2025":-69000,"FY2024":-27000,"FY2023":-50000,"FY2022":-35081,"FY2021":-55090}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025":359912,"FY2024":170881,"FY2023":-405874,"FY2022":-43412,"FY2021":-431102}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {"FY2025":1249482,"FY2024":1078601,"FY2023":1484475,"FY2022":1527887,"FY2021":1961547}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2025":1609394,"FY2024":1249482,"FY2023":1078601,"FY2022":1484475,"FY2021":1530445}),
]

bw = BankWorkbook(bank_name="Rathbones Investment Management Limited", years=YEARS, year_label=None, header_color="6B3F8C")
bw.add_cash_flow_sheet(title="Rathbones Investment Management Limited — Cash Flow Statement", subtitle="Entity basis, £'000. All figures transcribed from the Company's statutory accounts.", rows=rows, sources_text=CASH_SOURCES, first_col_width=86, source_height=330, unit_suffix=" (£'000)")

NOT_DISCLOSED = "Not publicly disclosed at Rathbones Investment Management Limited entity level. Rathbones Group Plc's official Pillar 3 reports are consolidated and state that no large subsidiary meets the definition requiring individual disclosure; group metrics must not be substituted for this Company's metrics. See the source note."
bw.add_not_disclosed_metric_sheets(["CET1 Capital", "CET1 Ratio", "Tier 1 Capital", "Tier 1 Ratio", "Total Capital", "Total Capital Ratio", "Total RWAs", "Leverage Ratio", "LCR", "NSFR", "MREL Ratio"], CASH_SOURCES, per_note={m: NOT_DISCLOSED for m in ["CET1 Capital", "CET1 Ratio", "Tier 1 Capital", "Tier 1 Ratio", "Total Capital", "Total Capital Ratio", "Total RWAs", "Leverage Ratio", "LCR", "NSFR", "MREL Ratio"]})

bw.add_overview_sheet(cash_flow_totals=[("Net cash inflow/(outflow) from operating activities", {"FY2025":988180,"FY2024":200256,"FY2023":-99468,"FY2022":276728,"FY2021":-249109}), ("Net cash used in investing activities", {"FY2025":-559268,"FY2024":-2375,"FY2023":-256406,"FY2022":-285059,"FY2021":-126903}), ("Cash and cash equivalents at the end of the year", {"FY2025":1609394,"FY2024":1249482,"FY2023":1078601,"FY2022":1484475,"FY2021":1530445})], cash_flow_unit=" (£'000)", ratios=[("CET1 Ratio", {})])
bw.save("/Users/armaan/code/katalysis/banks/RATHBONES INVESTMENT MANAGEMENT FINANCIALS.xlsx")
