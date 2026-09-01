import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/00036695/filing-history"
AR2025_URL = CH_BASE + "/MzUyMTA2MDcwMGFkaXF6a2N4/document?format=pdf&download=0"  # FY2025 accounts (FY2025+FY2024)
AR2023_URL = CH_BASE + "/MzQyMDgzOTQ5OWFkaXF6a2N4/document?format=pdf&download=0"  # FY2023 accounts (FY2023+FY2022)
AR2022_URL = CH_BASE + "/MzM4NTMwNzEyMGFkaXF6a2N4/document?format=pdf&download=0"  # FY2022 accounts (FY2022+FY2021)

ENTITY_NOTE = (
    "Coutts & Company (company 00036695, FRN 122287) is a wholly-owned subsidiary of NatWest Group plc, "
    "part of the ring-fenced NatWest Holdings (NWH) Group sub-group. All figures are Coutts & Company's own "
    "entity-level financial statements/disclosures, not the wider NatWest Group. A private unlimited company - "
    "voluntarily files full audited accounts at Companies House despite the unlimited-company form (which "
    "would otherwise exempt it from public filing), same as C. Hoare & Co. elsewhere in this project.\n\n"
    "BASIS CHANGE: the FY2022 Annual Report states its financial statements 'are prepared on a standalone "
    "basis for Coutts. Previously these were prepared on a consolidated basis for Coutts and its "
    "subsidiaries.' The FY2021 figures used here are as shown in the FY2022 report's own comparative column "
    "(the only source available for FY2021) - it isn't confirmed whether that comparative was itself restated "
    "onto the new standalone basis or retains the original consolidated FY2021 basis. Flagged, not resolved.\n\n"
    "In September 2022 Coutts acquired the 'Adam & Company' private-banking business from The Royal Bank of "
    "Scotland plc (a Part VII-style transfer) - RBS plc is a separate entity already built in this project; "
    "that acquisition is the source-side counterpart of this project's earlier RBS plc entity-identity finding."
)

CASH_FLOW_SOURCES = (
    "Sources - Coutts & Company's own Cash Flow Statement, from its audited Companies House filings:\n"
    f"FY2025/FY2024: Annual Report and Accounts 2025, p.56 - {AR2025_URL}\n"
    f"FY2023/FY2022 (summary presentation): Annual Report and Accounts 2023, p.53 - {AR2023_URL}\n"
    f"FY2022/FY2021 (detailed presentation, used for the itemized operating-activities breakdown and as the "
    f"source for FY2021): Annual Report and Accounts 2022, p.56 - {AR2022_URL}\n\n"
    "FY2021/FY2022 use a more detailed operating-activities presentation (a 'Net cash flows from trading "
    "activities' subtotal, then an itemized 'Changes in operating assets and liabilities' breakdown) than "
    "FY2023-FY2025's simpler 3-line 'Adjustments for' presentation - both feed the same-labelled 'Changes in "
    "operating assets and liabilities' total line; FY2023-FY2025 state it as a single figure with no "
    "breakdown. Full opening-to-closing cash chain reconciles exactly across all 5 years, cross-checked "
    "against each year's appearance as the following year's comparative in every case.\n\n" + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - Coutts & Company's own 'Risk and capital management' section, Companies House filings:\n"
        f"FY2025/FY2024: Annual Report and Accounts 2025, p.30 - {AR2025_URL}\n"
        f"FY2023/FY2022 (capital): Annual Report and Accounts 2023, p.30 - {AR2023_URL}\n"
        f"FY2022/FY2021 (capital): Annual Report and Accounts 2022, p.34 - {AR2022_URL}\n\n"
        "LCR/NSFR/MREL are NOT disclosed at Coutts's own entity level in any year - the FY2025 report states "
        "explicitly: 'Disclosures relating to these metrics... are completed at UK DoLSub level and published "
        "in the... NatWest Holdings Group Annual Report and Accounts. Under the UK DoLSub waiver NWB Plc, RBS "
        "plc and Coutts are permitted to manage liquidity on a consolidated sub-group basis rather than "
        "individually at the entity level.' Only the regulatory minimum requirement (100%/100%) is stated, "
        "never an achieved value - this matches the RBS plc build's precedent elsewhere in this project "
        "(RBS plc + NatWest Bank plc + Coutts share one DoLSub liquidity disclosure). MREL is mentioned only "
        "as a defined concept, with no ratio ever stated for Coutts specifically.\n\n" + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="Coutts & Company", years=YEARS, year_label=YEAR_LABEL, header_color="8444FC")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Operating profit before tax", {"FY2025": 346, "FY2024": 262, "FY2023": 381, "FY2022": 358, "FY2021": 241}),
    ("DATA", "Non-cash and other items (FY2023-FY2025 summary presentation)", {"FY2025": 81, "FY2024": 39, "FY2023": 61}),
    ("DATA", "Depreciation and amortisation (FY2021-FY2022 detailed presentation)", {"FY2022": 21, "FY2021": 19}),
    ("DATA", "Impairment losses/(releases) (FY2021-FY2022 detailed presentation)", {"FY2022": 31, "FY2021": -57}),
    ("DATA", "Other non-cash items (FY2021-FY2022 detailed presentation)", {"FY2022": 8, "FY2021": 3}),
    ("DATA", "Provision releases (FY2021-FY2022 detailed presentation)", {"FY2022": -1, "FY2021": -3}),
    ("DATA", "Elimination of foreign exchange differences (FY2021-FY2022 detailed presentation)", {"FY2022": -11, "FY2021": 30}),
    ("DATA", "Interest payable on debt securities in issue and subordinated liabilities (FY2021-FY2022 detailed presentation)", {"FY2022": 23, "FY2021": 12}),
    ("DATA", "Dividends receivable from subsidiaries (FY2021-FY2022 detailed presentation)", {"FY2022": -8, "FY2021": -15}),
    ("TOTAL", "Net cash flows from trading activities (FY2021-FY2022 subtotal; no equivalent line FY2023-FY2025)", {"FY2022": 421, "FY2021": 230}),
    ("DATA", "(Increase)/decrease in derivative assets", {"FY2022": -18, "FY2021": 15}),
    ("DATA", "Decrease in loans to banks", {"FY2022": 5, "FY2021": 49}),
    ("DATA", "Increase in loans to customers", {"FY2022": -944, "FY2021": -1449}),
    ("DATA", "Decrease in amounts due from holding companies and fellow subsidiaries", {"FY2022": 2234, "FY2021": 9513}),
    ("DATA", "Increase in other assets", {"FY2022": -4, "FY2021": -2}),
    ("DATA", "Decrease in bank deposits", {"FY2022": -2, "FY2021": -2}),
    ("DATA", "Increase in customer deposits", {"FY2022": 1847, "FY2021": 6829}),
    ("DATA", "Increase in amounts due to holding companies and fellow subsidiaries", {"FY2022": 2680, "FY2021": 1360}),
    ("DATA", "Increase/(decrease) in derivative liabilities", {"FY2022": 22, "FY2021": -16}),
    ("DATA", "Increase in other liabilities", {"FY2022": 1, "FY2021": 5}),
    ("TOTAL", "Changes in operating assets and liabilities", {"FY2025": -1841, "FY2024": 7767, "FY2023": 2095, "FY2022": 5821, "FY2021": 16302}),
    ("DATA", "Income taxes paid", {"FY2025": -89, "FY2024": -55, "FY2023": -192, "FY2022": 0, "FY2021": -71}),
    ("TOTAL", "Net cash flows from operating activities", {"FY2025": -1503, "FY2024": 8013, "FY2023": 2345, "FY2022": 6242, "FY2021": 16461}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -2, "FY2024": -9, "FY2023": -2, "FY2022": -3, "FY2021": -4}),
    ("DATA", "Sale of property, plant and equipment", {"FY2022": 0, "FY2021": 3}),
    ("DATA", "Cash expenditure on / purchase of intangible assets", {"FY2025": -9, "FY2024": -10, "FY2023": -22, "FY2022": -28, "FY2021": -27}),
    ("DATA", "Sale of intangible assets", {"FY2022": 0, "FY2021": 1}),
    ("DATA", "Purchase of net assets and liabilities", {"FY2023": 0, "FY2022": -270, "FY2021": 0}),
    ("DATA", "Dividends received from subsidiaries", {"FY2025": 33, "FY2024": 28, "FY2023": 60, "FY2022": 8, "FY2021": 15}),
    ("TOTAL", "Net cash flows from investing activities", {"FY2025": 22, "FY2024": 9, "FY2023": 36, "FY2022": -293, "FY2021": -12}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Issue of debt securities in issue", {"FY2025": 0, "FY2024": 260, "FY2023": 0, "FY2022": 50, "FY2021": 252}),
    ("DATA", "Redemption of debt securities in issue", {"FY2025": 0, "FY2024": -260, "FY2023": -50, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Issue of paid-in equity", {"FY2023": 0, "FY2022": 240, "FY2021": 0}),
    ("DATA", "Redemption of paid-in equity", {"FY2023": -35, "FY2022": -167, "FY2021": 0}),
    ("DATA", "Issue of subordinated liabilities", {"FY2023": 300, "FY2022": 0}),
    ("DATA", "Redemption of subordinated liabilities", {"FY2023": -266, "FY2022": 0}),
    ("DATA", "Interest paid on subordinated liabilities and debt securities in issue", {"FY2025": -45, "FY2024": -44, "FY2023": -55, "FY2022": -21, "FY2021": -12}),
    ("DATA", "Paid-in equity dividends paid", {"FY2025": -26, "FY2024": -28, "FY2023": -31, "FY2022": -16, "FY2021": -12}),
    ("DATA", "Dividends paid", {"FY2025": -187, "FY2024": -289, "FY2023": -210, "FY2022": -225, "FY2021": -105}),
    ("TOTAL", "Net cash flows from financing activities", {"FY2025": -258, "FY2024": -361, "FY2023": -347, "FY2022": -139, "FY2021": 123}),
    ("DATA", "Effects of exchange rate changes on cash and cash equivalents", {"FY2025": -1, "FY2024": 0, "FY2023": -1, "FY2022": 24, "FY2021": -38}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -1740, "FY2024": 7661, "FY2023": 2033, "FY2022": 5834, "FY2021": 16534}),
    ("DATA", "Cash and cash equivalents at 1 January", {"FY2025": 44222, "FY2024": 36561, "FY2023": 34528, "FY2022": 28694, "FY2021": 12160}),
    ("TOTAL", "Cash and cash equivalents at 31 December", {"FY2025": 42482, "FY2024": 44222, "FY2023": 36561, "FY2022": 34528, "FY2021": 28694}),
]

bw.add_cash_flow_sheet(
    title="Coutts & Company — Cash Flow Statement",
    subtitle="Entity-level basis, £m. Presentation varies by year - see source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=95,
    source_height=280,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 / capital metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=44, source_height=170)


CET1_CAPITAL = {"FY2025": 1248, "FY2024": 1192, "FY2023": 1199, "FY2022": 1260, "FY2021": 1235}
CET1_RATIO = {"FY2025": "11.4%", "FY2024": "11.3%", "FY2023": "11.3%", "FY2022": "11.8%", "FY2021": "11.9%"}
TIER1_CAPITAL = {"FY2025": 1488, "FY2024": 1432, "FY2023": 1439, "FY2022": 1535, "FY2021": 1437}
TIER1_RATIO = {"FY2025": "13.5%", "FY2024": "13.6%", "FY2023": "13.6%", "FY2022": "14.3%", "FY2021": "13.9%"}
TOTAL_CAPITAL = {"FY2025": 1788, "FY2024": 1732, "FY2023": 1739, "FY2022": 1790, "FY2021": 1703}
TOTAL_CAPITAL_RATIO = {"FY2025": "16.3%", "FY2024": "16.4%", "FY2023": "16.4%", "FY2022": "16.7%", "FY2021": "16.4%"}
TOTAL_RWA = {"FY2025": 10982, "FY2024": 10564, "FY2023": 10591, "FY2022": 10722, "FY2021": 10367}
LEVERAGE_RATIO = {"FY2025": "7.6%", "FY2024": "7.5%", "FY2023": "7.4%", "FY2022": "7.7%"}

NOT_DISCLOSED_LIQ_NOTE = (
    "Not publicly disclosed at Coutts's own entity level in any year - managed and disclosed only at the "
    "UK DoLSub sub-group level (NatWest Bank Plc + RBS plc + Coutts). See the sheet's source note for the "
    "exact quoted basis."
)
NOT_DISCLOSED_MREL_NOTE = (
    "Not publicly disclosed for any year - MREL is defined in the Annual Report's own glossary of capital "
    "concepts, but no MREL ratio for Coutts specifically is ever stated."
)

metric("CET1 Capital", "£m", [("Common Equity Tier 1 (CET1) capital", CET1_CAPITAL)])
metric("CET1 Ratio", "%", [("CET1 ratio", CET1_RATIO)])
metric("Tier 1 Capital", "£m", [("Tier 1 capital", TIER1_CAPITAL)])
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", TIER1_RATIO)])
metric("Total Capital", "£m", [("Total regulatory capital", TOTAL_CAPITAL)])
metric("Total Capital Ratio", "%", [("Total capital ratio", TOTAL_CAPITAL_RATIO)])
metric("Total RWAs", "£m", [("Total risk-weighted assets", TOTAL_RWA)])
metric(
    "Leverage Ratio", "%", [("UK leverage ratio", LEVERAGE_RATIO)],
    note="FY2021 not disclosed - the FY2022 Annual Report (the only source for FY2021) does not include a "
         "leverage ratio table at all; the leverage-ratio disclosure only begins from the FY2023 report "
         "onward (shown there with a FY2022 comparative, used for the FY2022 column here).",
)

bw.add_not_disclosed_metric_sheets(
    ["LCR", "NSFR"], p3_sources(), per_note={"LCR": NOT_DISCLOSED_LIQ_NOTE, "NSFR": NOT_DISCLOSED_LIQ_NOTE},
)
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources(), per_note={"MREL Ratio": NOT_DISCLOSED_MREL_NOTE},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash flows from operating activities", {"FY2025": -1503, "FY2024": 8013, "FY2023": 2345, "FY2022": 6242, "FY2021": 16461}),
        ("Net cash flows from investing activities", {"FY2025": 22, "FY2024": 9, "FY2023": 36, "FY2022": -293, "FY2021": -12}),
        ("Net cash flows from financing activities", {"FY2025": -258, "FY2024": -361, "FY2023": -347, "FY2022": -139, "FY2021": 123}),
        ("Cash and cash equivalents at 31 December", {"FY2025": 42482, "FY2024": 44222, "FY2023": 36561, "FY2022": 34528, "FY2021": 28694}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Tier 1 Ratio", TIER1_RATIO),
        ("Total Capital Ratio", TOTAL_CAPITAL_RATIO),
        ("Leverage Ratio", LEVERAGE_RATIO),
    ],
    note="LCR/NSFR/MREL omitted from this chart - not disclosed at Coutts's own entity level in any year "
         "(see the individual sheets). Figures are duplicated from the detail sheets for at-a-glance trend "
         "viewing; see each sheet's own source citation for the underlying document/page.",
)

bw.save("/Users/armaan/code/katalysis/banks/COUTTS FINANCIALS.xlsx")
