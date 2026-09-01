import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, all 12mo to 31 Dec
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2025/annual/pdfs/hsbc-bank-plc/260225-annual-report-and-accounts-2025.pdf"
AR2024_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2024/annual/pdfs/hsbc-bank-plc/250219-annual-report-and-accounts-2024.pdf"
AR2023_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2023/annual/pdfs/hsbc-bank-plc/240221-annual-report-and-accounts-2023.pdf"
AR2022_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2022/annual/pdfs/hsbc-bank-plc/230221-annual-report-and-accounts-2022.pdf"
AR2021_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2021/annual/pdfs/hsbc-bank-plc/220222-annual-report-and-accounts-2021.pdf"

P32025_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2025/annual/pdfs/hsbc-bank-plc/260225-pillar-3-disclosures-at-31-december-2025.pdf"
P32024_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2024/annual/pdfs/hsbc-bank-plc/250219-pillar-3-disclosures-at-31-december-2024.pdf"
P32023_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2023/annual/pdfs/hsbc-bank-plc/240221-pillar-3-disclosures-31-december-2023.pdf"
P32022_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2022/annual/pdfs/hsbc-bank-plc/230221-pillar-3-disclosures-31-december-2022.pdf"
P32021_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2021/annual/pdfs/hsbc-bank-plc/220222-pillar-3-disclosures-at-31-december-2021.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: HSBC Bank plc (Companies House 00014259, FRN 114216) is HSBC's legacy UK/international "
    "non-ring-fenced banking entity - confirmed distinct from HSBC UK Bank plc (FRN 765112, the ring-fenced "
    "retail bank created 2018 under UK ring-fencing reform, not attempted in this project as of this build), "
    "HSBC Holdings plc (the ultimate listed parent, out of scope), and HSBC Innovation Bank Limited (FRN "
    "543146, the former Silicon Valley Bank UK, built separately in this same batch - see 'HSBC INNOVATION "
    "BANK FINANCIALS.xlsx'). All figures below are HSBC Bank plc's own entity-level Consolidated (i.e. HSBC "
    "Bank plc and its own subsidiaries, not the wider HSBC Holdings plc Group) statements, sourced directly "
    "from HSBC Bank plc's own Annual Report and Accounts and Pillar 3 Disclosures, published on hsbc.com's "
    "investor-relations 'Subsidiaries' reporting archive (a company-house style lookup was blocked at the DNS "
    "level in this session; hsbc.com itself was fully reachable). Both a 2023 IFRS 17 'Insurance Contracts' "
    "adoption and a late-2022 change to how non-financial-institution subsidiary investments are measured "
    "triggered real, source-disclosed restatements of prior-year comparatives - per this project's convention, "
    "every year below uses that year's own originally-published figures, not a later restated comparative; "
    "both restatements are individually noted where they bite."
)

CASH_FLOW_NOTE = (
    "CASH FLOW NOTE: figures are £m (this is one of the largest entities in this project by balance sheet "
    "size; £'000 would be unwieldy). The full opening-to-closing cash chain reconciles exactly year-to-year "
    "using each year's own originally-published figures (FY2021 closing £140,923m = FY2022 opening; FY2022 "
    "closing £189,907m = FY2023 opening; FY2023 closing £177,037m = FY2024 opening; FY2024 closing £162,928m "
    "= FY2025 opening) despite the IFRS 17 restatement below only affecting the 'Profit/(loss) before tax' "
    "and adjustment-line presentation for FY2022, not the underlying cash totals. One row's label was "
    "corrected between reports for the same figure: FY2022's own Annual Report labelled the £628m financing "
    "line 'redemption of preference shares and other equity instruments' (a positive value, inconsistent with "
    "'redemption'), which the FY2023 Annual Report's FY2022 comparative column relabels 'issue of ordinary "
    "share capital and other equity instruments' - matching the £628m 'Capital securities issued during the "
    "period' shown in FY2022's own statement of changes in equity. The corrected label and FY2022's own "
    "originally-published £628m value are both used here."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are HSBC Bank plc's own Consolidated Statement of Cash Flows, £m, from each year's "
    "own Annual Report and Accounts (each year's own originally-published figures, not a later restated "
    "comparative):\n"
    f"FY2025: HSBC Bank plc Annual Report and Accounts 2025, p.95 (Consolidated statement of cash flows) - {AR2025_URL}\n"
    f"FY2024: HSBC Bank plc Annual Report and Accounts 2024, p.121 (Consolidated statement of cash flows) - {AR2024_URL}\n"
    f"FY2023: HSBC Bank plc Annual Report and Accounts 2023, p.112-113 (Consolidated statement of cash flows) - {AR2023_URL}\n"
    f"FY2022: HSBC Bank plc Annual Report and Accounts 2022, p.117 (Consolidated statement of cash flows) - {AR2022_URL}\n"
    f"FY2021: HSBC Bank plc Annual Report and Accounts 2021, p.111 (Consolidated statement of cash flows) - {AR2021_URL}\n\n"
    + CASH_FLOW_NOTE + "\n\n" + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - HSBC Bank plc's own entity-level Pillar 3 Disclosures, Table 1 'Key metrics (KM1/IFRS9-FL)' "
        "(FY2022-FY2025) or the equivalent 'Comparison of own funds, capital and leverage ratios' / 'Overview "
        "of RWAs' tables (FY2021, which pre-dates the KM1 template), each year's own originally-published "
        "figures at 31 December:\n"
        f"FY2025: HSBC Bank plc Pillar 3 Disclosures at 31 December 2025, p.3 - {P32025_URL}\n"
        f"FY2024: HSBC Bank plc Pillar 3 Disclosures at 31 December 2024, p.3 - {P32024_URL}\n"
        f"FY2023: HSBC Bank plc Pillar 3 Disclosures at 31 December 2023, p.4 - {P32023_URL}\n"
        f"FY2022: HSBC Bank plc Pillar 3 Disclosures at 31 December 2022, p.2 - {P32022_URL}\n"
        f"FY2021: HSBC Bank plc Pillar 3 Disclosures at 31 December 2021, p.2-3 (Tables 1 and 2) - {P32021_URL}\n\n"
        + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="HSBC Bank plc", years=YEARS, year_label=YEAR_LABEL, header_color="8602AA")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {"FY2025": -119, "FY2024": 2068, "FY2023": 2152, "FY2022": -959, "FY2021": 1023}),
    ("DATA", "Depreciation, amortisation and impairment", {"FY2025": 558, "FY2024": 148, "FY2023": 61, "FY2022": 128, "FY2021": 174}),
    ("DATA", "Net loss/(gain) from investing activities", {"FY2025": 1098, "FY2024": 83, "FY2023": -66, "FY2022": 2002, "FY2021": -62}),
    ("DATA", "Share of (profit)/loss in associates and joint ventures", {"FY2025": -61, "FY2024": -18, "FY2023": 43, "FY2022": 30, "FY2021": -191}),
    ("DATA", "Change in expected credit losses gross of recoveries and other credit impairment charges", {"FY2025": 154, "FY2024": 165, "FY2023": 161, "FY2022": 253, "FY2021": -171}),
    ("DATA", "Provisions including pensions", {"FY2025": 1184, "FY2024": 78, "FY2023": 132, "FY2022": 192, "FY2021": 104}),
    ("DATA", "Share-based payment expense", {"FY2025": 81, "FY2024": 61, "FY2023": 58, "FY2022": 46, "FY2021": 96}),
    ("DATA", "Other non-cash items included in (loss)/profit before tax", {"FY2025": -155, "FY2024": -180, "FY2023": -165, "FY2022": -242, "FY2021": -198}),
    ("DATA", "Elimination of exchange differences", {"FY2025": -3416, "FY2024": 4883, "FY2023": 4426, "FY2022": -6714, "FY2021": 4926}),
    ("DATA", "- change in net trading securities and derivatives", {"FY2025": -16933, "FY2024": -13266, "FY2023": -15528, "FY2022": -6213, "FY2021": 8157}),
    ("DATA", "- change in loans and advances to banks and customers", {"FY2025": -3077, "FY2024": -455, "FY2023": 4245, "FY2022": -2717, "FY2021": 11149}),
    ("DATA", "- change in reverse repurchase agreements - non-trading", {"FY2025": -13896, "FY2024": 9341, "FY2023": -13531, "FY2022": 6251, "FY2021": 9538}),
    ("DATA", "- change in financial assets designated and otherwise mandatorily measured at fair value", {"FY2025": -3139, "FY2024": -1954, "FY2023": -3296, "FY2022": 2729, "FY2021": -2429}),
    ("DATA", "- change in other assets", {"FY2025": -3313, "FY2024": 4734, "FY2023": -5707, "FY2022": -7329, "FY2021": 10924}),
    ("DATA", "- change in deposits by banks and customer accounts", {"FY2025": 23219, "FY2024": 14113, "FY2023": 7548, "FY2022": 19835, "FY2021": 7940}),
    ("DATA", "- change in repurchase agreements - non-trading", {"FY2025": 6374, "FY2024": -13813, "FY2023": 20516, "FY2022": 5641, "FY2021": -7643}),
    ("DATA", "- change in debt securities in issue", {"FY2025": -6638, "FY2024": 6018, "FY2023": 6175, "FY2022": -1060, "FY2021": -7943}),
    ("DATA", "- change in financial liabilities designated at fair value", {"FY2025": 5234, "FY2024": 4937, "FY2023": 4042, "FY2022": -1822, "FY2021": -7191}),
    ("DATA", "- change in other liabilities", {"FY2025": 3534, "FY2024": -10026, "FY2023": -7506, "FY2022": 21297, "FY2021": -12295}),
    ("DATA", "- dividend received from associates", {"FY2025": 18, "FY2023": 15, "FY2022": 7}),
    ("DATA", "- contributions paid to defined benefit plans", {"FY2025": -28, "FY2024": -20, "FY2023": -5, "FY2022": -10, "FY2021": -24}),
    ("DATA", "- tax received/(paid)", {"FY2025": 92, "FY2024": -1088, "FY2023": -140, "FY2022": 845, "FY2021": -581}),
    ("TOTAL", "Changes in operating assets and liabilities - subtotal", {"FY2025": -8553, "FY2024": -1479, "FY2023": -3172, "FY2022": 37454, "FY2021": 9602}),
    ("TOTAL", "Net cash from operating activities", {"FY2025": -9229, "FY2024": 5809, "FY2023": 3630, "FY2022": 32190, "FY2021": 15303}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of financial investments", {"FY2025": -45055, "FY2024": -32587, "FY2023": -26586, "FY2022": -13227, "FY2021": -18890}),
    ("DATA", "Proceeds from the sale and maturity of financial investments", {"FY2025": 33969, "FY2024": 23272, "FY2023": 15497, "FY2022": 20490, "FY2021": 25027}),
    ("DATA", "Net cash flows from the purchase and sale of property, plant and equipment", {"FY2025": -18, "FY2024": -16, "FY2023": -31, "FY2022": -20, "FY2021": 52}),
    ("DATA", "Net investment in intangible assets", {"FY2025": -393, "FY2024": -149, "FY2023": -125, "FY2022": -28, "FY2021": -45}),
    ("DATA", "Net cash outflow from investment in associates and acquisition of businesses and subsidiaries", {"FY2025": -25, "FY2024": -955, "FY2023": -1161, "FY2022": -29, "FY2021": -85}),
    ("DATA", "Net cash flow on disposal of subsidiaries, businesses, associates and joint ventures", {"FY2025": 39, "FY2024": -8631, "FY2023": -394, "FY2021": 0}),
    ("TOTAL", "Net cash from investing activities", {"FY2025": -11483, "FY2024": -19066, "FY2023": -12800, "FY2022": 7186, "FY2021": 6059}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Issue of ordinary share capital and other equity instruments", {"FY2025": 276, "FY2024": 2782, "FY2023": 584, "FY2022": 628}),
    ("DATA", "Redemption of other equity instruments", {"FY2024": -213, "FY2021": 0}),
    ("DATA", "Subordinated loan capital issued", {"FY2025": 2702, "FY2024": 2777, "FY2023": 3246, "FY2022": 3111, "FY2021": 10466}),
    ("DATA", "Subordinated loan capital repaid", {"FY2025": -1277, "FY2024": -474, "FY2023": -2693, "FY2022": -2248, "FY2021": -10902}),
    ("DATA", "Dividends to the parent company", {"FY2025": -1951, "FY2024": -535, "FY2023": -961, "FY2022": -1052, "FY2021": -194}),
    ("DATA", "Funds received from the parent company", {"FY2022": 1465}),
    ("DATA", "Dividends paid to non-controlling interests", {"FY2025": -16, "FY2024": -11, "FY2023": -7, "FY2022": -2, "FY2021": -1}),
    ("TOTAL", "Net cash from financing activities", {"FY2025": -266, "FY2024": 4326, "FY2023": 169, "FY2022": 1902, "FY2021": -631}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": -20978, "FY2024": -8931, "FY2023": -9001, "FY2022": 41278, "FY2021": 20731}),
    ("DATA", "Cash and cash equivalents at 1 Jan", {"FY2025": 162928, "FY2024": 177037, "FY2023": 189907, "FY2022": 140923, "FY2021": 125304}),
    ("DATA", "Exchange difference in respect of cash and cash equivalents", {"FY2025": 4949, "FY2024": -5178, "FY2023": -3869, "FY2022": 7706, "FY2021": -5112}),
    ("TOTAL", "Cash and cash equivalents at 31 Dec", {"FY2025": 146899, "FY2024": 162928, "FY2023": 177037, "FY2022": 189907, "FY2021": 140923}),
]

bw.add_cash_flow_sheet(
    title="HSBC Bank plc — Consolidated Cash Flow Statement",
    subtitle="HSBC Bank plc consolidated (entity-level, not the wider HSBC Holdings plc Group), £m. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=82,
    source_height=280,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=48, source_height=190)


metric(
    "CET1 Capital", "£m",
    [("Common equity tier 1 (CET1) capital", {"FY2025": 20063, "FY2024": 21896, "FY2023": 19230, "FY2022": 19184, "FY2021": 18007})],
)

metric(
    "CET1 Ratio", "% of RWA",
    [("CET1 ratio", {"FY2025": "17.9%", "FY2024": "19.5%", "FY2023": "17.9%", "FY2022": "16.8%", "FY2021": "17.3%"})],
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 24272, "FY2024": 25828, "FY2023": 23124, "FY2022": 23077, "FY2021": 21869})],
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "21.6%", "FY2024": "23.0%", "FY2023": "21.5%", "FY2022": "20.2%", "FY2021": "21.0%"})],
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 41473, "FY2024": 41306, "FY2023": 37131, "FY2022": 36187, "FY2021": 33036})],
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "36.9%", "FY2024": "36.8%", "FY2023": "34.6%", "FY2022": "31.7%", "FY2021": "31.7%"})],
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted assets", {"FY2025": 112340, "FY2024": 112251, "FY2023": 107449, "FY2022": 114171, "FY2021": 104314})],
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio", {"FY2025": "4.5%", "FY2024": "5.5%", "FY2023": "5.1%", "FY2022": "5.5%", "FY2021": "4.1%"})],
    note="A genuine basis change: FY2021 is disclosed on the Capital Requirements Regulation basis (total "
         "leverage ratio exposure £535,562m, ratio 4.1%). From FY2022 onward, HSBC Bank plc switched to the "
         "CRR II end-point basis 'excluding claims on central banks' (a narrower exposure measure) - FY2022's "
         "own report shows this new-basis figure (exposure £417,587m, ratio 5.5%) with no FY2021 comparative on "
         "the same basis, so FY2021 above is left on its own originally-disclosed (different) basis rather than "
         "forced onto the newer definition.",
)

metric(
    "LCR", "%, 12-month average",
    [("Liquidity coverage ratio", {"FY2025": "148%", "FY2024": "148%", "FY2023": "148%", "FY2022": "143.1%"})],
    note="Not disclosed for FY2021: HSBC Bank plc's own FY2021 Pillar 3 Disclosures pre-date the KM1 template "
         "and PRA's entity-level LCR/NSFR disclosure requirement, which 'came into effect on 1 January 2022' "
         "per the FY2022 Pillar 3 Disclosures' own footnote - confirmed genuinely absent, not an access gap. "
         "Reported on a 12-month rolling average basis (this project's standard convention).",
)

metric(
    "NSFR", "%, average of preceding 4 quarters",
    [("Net stable funding ratio", {"FY2025": "114%", "FY2024": "115%", "FY2023": "116%", "FY2022": "115.4%"})],
    note="Not disclosed for FY2021 - same reason as the LCR sheet (pre-dates the PRA's entity-level NSFR "
         "disclosure requirement, effective 1 January 2022).",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={
        "MREL Ratio": "No MREL figure or mention appears anywhere in any of HSBC Bank plc's own Pillar 3 "
                      "Disclosures FY2021-FY2025 - HSBC Bank plc is not itself a resolution entity under the "
                      "Bank of England's Single Point of Entry resolution strategy for the HSBC group (that "
                      "role sits with HSBC Holdings plc at the top of the group), so no entity-level MREL "
                      "requirement or ratio applies here - the same pattern as RBS plc/Coutts & Company's "
                      "relationship to the wider NatWest Group.",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from operating activities", {"FY2025": -9229, "FY2024": 5809, "FY2023": 3630, "FY2022": 32190, "FY2021": 15303}),
        ("Net cash from investing activities", {"FY2025": -11483, "FY2024": -19066, "FY2023": -12800, "FY2022": 7186, "FY2021": 6059}),
        ("Net cash from financing activities", {"FY2025": -266, "FY2024": 4326, "FY2023": 169, "FY2022": 1902, "FY2021": -631}),
        ("Cash and cash equivalents at 31 Dec", {"FY2025": 146899, "FY2024": 162928, "FY2023": 177037, "FY2022": 189907, "FY2021": 140923}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "17.9%", "FY2024": "19.5%", "FY2023": "17.9%", "FY2022": "16.8%", "FY2021": "17.3%"}),
        ("Tier 1 Ratio", {"FY2025": "21.6%", "FY2024": "23.0%", "FY2023": "21.5%", "FY2022": "20.2%", "FY2021": "21.0%"}),
        ("Total Capital Ratio", {"FY2025": "36.9%", "FY2024": "36.8%", "FY2023": "34.6%", "FY2022": "31.7%", "FY2021": "31.7%"}),
        ("Leverage Ratio", {"FY2025": "4.5%", "FY2024": "5.5%", "FY2023": "5.1%", "FY2022": "5.5%", "FY2021": "4.1%"}),
        ("LCR", {"FY2025": "148%", "FY2024": "148%", "FY2023": "148%", "FY2022": "143.1%"}),
        ("NSFR", {"FY2025": "114%", "FY2024": "115%", "FY2023": "116%", "FY2022": "115.4%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. MREL is not shown here (not disclosed at this "
         "entity level - see that sheet). The Leverage Ratio's FY2021 figure is on a different basis than "
         "FY2022-FY2025 - see the Leverage Ratio sheet's note.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/HSBC BANK PLC FINANCIALS.xlsx")
