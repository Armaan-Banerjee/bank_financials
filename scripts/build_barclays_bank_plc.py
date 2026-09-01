import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first

CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/01026167/filing-history"
AR25_URL = f"{CH_BASE}/MzUyMzkyMDY5MmFkaXF6a2N4/document?format=pdf&download=0"
AR24_URL = f"{CH_BASE}/MzQ2OTM2NDcwM2FkaXF6a2N4/document?format=pdf&download=0"
AR22_URL = f"{CH_BASE}/MzM4Mjg0NjA2M2FkaXF6a2N4/document?format=pdf&download=0"

CASH_FLOW_SOURCES = (
    "Sources — Barclays Bank PLC (the non ring-fenced bank; company no. 01026167) consolidated cash flow "
    "statement, £m, as filed with Companies House:\n"
    f"FY2025, FY2024 & FY2023: Barclays Bank PLC Annual Report 2025 (Group accounts made up to 31 Dec 2025, "
    f"filed 02 Jun 2026), p.289 (Consolidated cash flow statement) — {AR25_URL}\n"
    f"FY2022 & FY2021: Barclays Bank PLC Annual Report 2022 (Group accounts made up to 31 Dec 2022, filed 21 "
    f"Jun 2023), p.171 (Consolidated cash flow statement) — {AR22_URL}\n"
    "Note: FY2021 figures are presented on a restated basis — Barclays Bank PLC restated its FY2021 results "
    "(including litigation and conduct charges) to reflect the impact of the 2022 Over-issuance of Securities "
    "matter in the US; see Note 1a (Restatement of financial statements) in the FY2022 Annual Report. FY2022 "
    "and FY2023 totals are cross-checked and consistent across the FY2022/FY2024/FY2025 Annual Report vintages."
)

def p3_sources(note_extra=""):
    return (
        "Sources — Barclays Bank PLC solo-consolidated capital/liquidity disclosures, from the 'Treasury and "
        "Capital risk' section of the Risk review, as filed with Companies House:\n"
        f"FY2025 & FY2024: Barclays Bank PLC Annual Report 2025, p.231-233 (Capital risk / Liquidity risk) — {AR25_URL}\n"
        f"FY2023: Barclays Bank PLC Annual Report 2024, p.213-222 (Liquidity risk / Capital risk) — {AR24_URL}\n"
        f"FY2022 & FY2021: Barclays Bank PLC Annual Report 2022, p.115-126 (Liquidity risk / Capital risk) — {AR22_URL}"
        + note_extra
    )

bw = BankWorkbook(bank_name="Barclays Bank PLC", years=YEARS, header_color="7B241C")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Reconciliation of profit before tax to net cash flows from operating activities", {}),
    ("DATA", "Profit before tax", {"FY2025": 5943, "FY2024": 4747, "FY2023": 4223, "FY2022": 4867, "FY2021": 5418}),
    ("SECTION", "Adjustment for non-cash items", {}),
    ("DATA", "Credit impairment charges/(releases)", {"FY2025": 1866, "FY2024": 1617, "FY2023": 1578, "FY2022": 933, "FY2021": -277}),
    ("DATA", "Depreciation, amortisation and impairment of property, plant, equipment and intangibles", {"FY2025": 362, "FY2024": 356, "FY2023": 489, "FY2022": 483, "FY2021": 683}),
    ("DATA", "Provisions and pension charges / other provisions", {"FY2025": 268, "FY2024": 195, "FY2023": 63, "FY2022": 1188, "FY2021": 85}),
    ("DATA", "Net loss/(profit) on disposal of investments and property, plant and equipment", {"FY2025": 13, "FY2024": 9, "FY2023": 7, "FY2022": 8, "FY2021": 12}),
    ("DATA", "Other non-cash movements including exchange rate movements", {"FY2025": 4863, "FY2024": 1835, "FY2023": 7567, "FY2022": -13491, "FY2021": 1968}),
    ("SECTION", "Changes in operating assets and liabilities", {}),
    ("DATA", "Net decrease/(increase) in cash collateral and settlement balances", {"FY2025": 2252, "FY2024": 2060, "FY2023": 31, "FY2022": -1078, "FY2021": 3633}),
    ("DATA", "Net (increase)/decrease in loans and advances at amortised cost", {"FY2025": -7782, "FY2024": -2556, "FY2023": 8313, "FY2022": -30617, "FY2021": -7190}),
    ("DATA", "Net increase/(decrease) in reverse repurchase agreements and other similar secured lending", {"FY2025": -14269, "FY2024": -2290, "FY2023": -378, "FY2022": 2452, "FY2021": 5804}),
    ("DATA", "Net increase in deposits at amortised cost", {"FY2025": 25375, "FY2024": 17578, "FY2023": 10219, "FY2022": 28751, "FY2021": 18132}),
    ("DATA", "Net increase/(decrease) in debt securities in issue", {"FY2025": 21426, "FY2024": -9850, "FY2023": -14359, "FY2022": 11624, "FY2021": 18965}),
    ("DATA", "Net (decrease)/increase in repurchase agreements and other similar secured borrowing", {"FY2025": -10746, "FY2024": 843, "FY2023": 16589, "FY2022": -804, "FY2021": 2326}),
    ("DATA", "Net decrease/(increase) in derivative financial instruments", {"FY2025": 1590, "FY2024": -6794, "FY2023": 7539, "FY2022": -8002, "FY2021": -3655}),
    ("DATA", "Net (increase)/decrease in trading portfolio assets", {"FY2025": -23499, "FY2024": 8322, "FY2023": -40795, "FY2022": 13100, "FY2021": -19207}),
    ("DATA", "Net increase/(decrease) in trading portfolio liabilities", {"FY2025": 647, "FY2024": -1579, "FY2023": -14699, "FY2022": 19169, "FY2021": 7152}),
    ("DATA", "Net increase/(decrease) in financial assets and liabilities at fair value through the income statement", {"FY2025": 20593, "FY2024": -6415, "FY2023": 33410, "FY2022": -1978, "FY2021": -14960}),
    ("DATA", "Net increase in other assets", {"FY2025": -167, "FY2024": -3962, "FY2023": -1301, "FY2022": -3311, "FY2021": -2235}),
    ("DATA", "Net decrease/increase in other liabilities", {"FY2025": -384, "FY2024": -1440, "FY2023": -1864, "FY2022": 1834, "FY2021": 2082}),
    ("DATA", "Corporate income tax paid", {"FY2025": -248, "FY2024": -685, "FY2023": -265, "FY2022": -144, "FY2021": -1239}),
    ("TOTAL", "Net cash from operating activities", {"FY2025": 28103, "FY2024": 1991, "FY2023": 16367, "FY2022": 24984, "FY2021": 17497}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of debt securities at amortised cost", {"FY2025": -15658, "FY2024": -27617, "FY2023": -14901, "FY2022": -20014, "FY2021": -6931}),
    ("DATA", "Proceeds from redemption or sale of debt securities at amortised cost", {"FY2025": 9828, "FY2024": 16922, "FY2023": 2681, "FY2022": 12925, "FY2021": 2424}),
    ("DATA", "Purchase of financial assets at fair value through other comprehensive income", {"FY2025": -29747, "FY2024": -52347, "FY2023": -50254, "FY2022": -43139, "FY2021": -44058}),
    ("DATA", "Proceeds from sale or redemption of financial assets at fair value through other comprehensive income", {"FY2025": 38246, "FY2024": 51803, "FY2023": 44126, "FY2022": 42157, "FY2021": 47601}),
    ("DATA", "Purchase of property, plant and equipment and investment in intangibles", {"FY2025": -574, "FY2024": -512, "FY2023": -439, "FY2022": -540, "FY2021": -758}),
    ("DATA", "Acquisition of business", {"FY2025": 0, "FY2024": -232}),
    ("DATA", "Disposal of subsidiaries and associates, net of cash disposed", {"FY2022": 0, "FY2021": 65}),
    ("DATA", "Other cash flows associated with investing activities", {"FY2024": 2749, "FY2022": 0, "FY2021": 4}),
    ("TOTAL", "Net cash from investing activities", {"FY2025": 2095, "FY2024": -9234, "FY2023": -18787, "FY2022": -8611, "FY2021": -1653}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividends paid and other coupon payments on equity instruments", {"FY2025": -3385, "FY2024": -2615, "FY2023": -2196, "FY2022": -963, "FY2021": -1452}),
    ("DATA", "Issuance of subordinated liabilities", {"FY2025": 9808, "FY2024": 11222, "FY2023": 5986, "FY2022": 15381, "FY2021": 9099}),
    ("DATA", "Redemption of subordinated liabilities", {"FY2025": -5665, "FY2024": -5067, "FY2023": -7431, "FY2022": -8367, "FY2021": -7241}),
    ("DATA", "Issue of shares and other equity instruments", {"FY2025": 2770, "FY2024": 970, "FY2023": 2499, "FY2022": 3134, "FY2021": 1072}),
    ("DATA", "Repurchase of shares and other equity instruments", {"FY2025": -2198, "FY2024": -2131, "FY2023": -2425, "FY2022": -2136, "FY2021": 0}),
    ("DATA", "Capital contribution", {"FY2022": 750}),
    ("DATA", "Vesting of employee share schemes", {"FY2025": -530, "FY2024": -448, "FY2023": -442, "FY2022": -413, "FY2021": -356}),
    ("TOTAL", "Net cash from financing activities", {"FY2025": 800, "FY2024": 1931, "FY2023": -4009, "FY2022": 7386, "FY2021": 1122}),
    ("DATA", "Effect of exchange rates on cash and cash equivalents", {"FY2025": -1740, "FY2024": -2405, "FY2023": -5013, "FY2022": 10235, "FY2021": -4231}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 29258, "FY2024": -7717, "FY2023": -11442, "FY2022": 33994, "FY2021": 12735}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 200695, "FY2024": 208412, "FY2023": 219854, "FY2022": 185860, "FY2021": 173125}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 229953, "FY2024": 200695, "FY2023": 208412, "FY2022": 219854, "FY2021": 185860}),
    ("SECTION", "Cash and cash equivalents at end of year comprise", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 208544, "FY2024": 180365, "FY2023": 189686, "FY2022": 202142, "FY2021": 169085}),
    ("DATA", "Loans and advances to banks with original maturity of three months or less", {"FY2025": 7802, "FY2024": 7758, "FY2023": 7117, "FY2022": 6229, "FY2021": 6473}),
    ("DATA", "Cash collateral balances with central banks with original maturity of three months or less", {"FY2025": 11625, "FY2024": 11025, "FY2023": 10325, "FY2022": 10625, "FY2021": 9690}),
    ("DATA", "Treasury and other eligible bills with original maturity of three months or less", {"FY2025": 1982, "FY2024": 1547, "FY2023": 1284, "FY2022": 858, "FY2021": 612}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 229953, "FY2024": 200695, "FY2023": 208412, "FY2022": 219854, "FY2021": 185860}),
]

bw.add_cash_flow_sheet(
    title="Barclays Bank PLC — Consolidated Cash Flow Statement",
    subtitle="Barclays Bank PLC Group (consolidated basis), £m unless stated",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=72,
    source_height=100,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 / capital metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Solo-consolidated basis, {unit}" if unit else "Solo-consolidated basis",
                         rows_data, sources_text, note=note, first_col_width=44, source_height=100)

metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 28177, "FY2024": 26995, "FY2023": 25470, "FY2022": 25907, "FY2021": 23928})],
    p3_sources(),
    note="FY2021 figure is restated (Over-issuance of Securities matter); see Note 1a in the FY2022 Annual Report.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "12.7%", "FY2024": "12.1%", "FY2023": "12.1%", "FY2022": "12.7%", "FY2021": "12.9%"})],
    p3_sources(),
    note="FY2021 figure is restated (Over-issuance of Securities matter); see Note 1a in the FY2022 Annual Report.",
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 (T1) capital", {"FY2025": 35848, "FY2024": 33787, "FY2023": 33864, "FY2022": 34139, "FY2021": 32395})],
    p3_sources(),
    note="FY2021 figure is restated (Over-issuance of Securities matter); see Note 1a in the FY2022 Annual Report.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 (T1) ratio", {"FY2025": "16.1%", "FY2024": "15.1%", "FY2023": "16.0%", "FY2022": "16.7%", "FY2021": "17.5%"})],
    p3_sources(),
    note="FY2021 figure is restated (Over-issuance of Securities matter); see Note 1a in the FY2022 Annual Report.",
)

metric(
    "Total Capital", "£m",
    [("Total regulatory capital", {"FY2025": 42129, "FY2024": 40444, "FY2023": 40530, "FY2022": 42321, "FY2021": 37954})],
    p3_sources(),
    note="FY2021 figure is restated (Over-issuance of Securities matter); see Note 1a in the FY2022 Annual Report.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total regulatory capital ratio", {"FY2025": "19.0%", "FY2024": "18.1%", "FY2023": "19.2%", "FY2022": "20.8%", "FY2021": "20.5%"})],
    p3_sources(),
    note="FY2021 figure is restated (Over-issuance of Securities matter); see Note 1a in the FY2022 Annual Report.",
)

metric(
    "Total RWAs", "£m",
    [("Total risk weighted assets (RWAs)", {"FY2025": 222247, "FY2024": 223648, "FY2023": 211193, "FY2022": 203833, "FY2021": 185467})],
    p3_sources(),
    note="FY2021 figure is restated (Over-issuance of Securities matter); see Note 1a in the FY2022 Annual Report. "
         "FY2024 comparative in the FY2025 Annual Report is calculated applying UK CRR transitional arrangements "
         "(IFRS 9 transitional relief and grandfathering of certain capital instruments), which ceased to apply "
         "from 1 January/29 June 2025.",
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("UK leverage ratio (%)", {"FY2025": "5.8%", "FY2024": "5.8%", "FY2023": "6.0%", "FY2022": "4.6%", "FY2021": "3.7%"}),
        ("Tier 1 (T1) capital used in leverage calculation (£m)", {"FY2025": 56465, "FY2024": 54713, "FY2023": 55560, "FY2022": 34139, "FY2021": 32395}),
        ("UK leverage exposure (£m)", {"FY2025": 980935, "FY2024": 946809, "FY2023": 924826, "FY2022": 742730, "FY2021": 883371}),
    ],
    p3_sources(),
    note="Basis changes across the period: FY2021 is a CRR leverage ratio (Barclays Bank PLC was not subject to "
         "the UK leverage framework until 1 January 2022; the UK-framework equivalent was disclosed as 4.1%, "
         "£767.6bn exposure). FY2022 is a UK leverage ratio on a solo-consolidated basis. From FY2023 onward, "
         "leverage minimum requirements — and the disclosed ratio — moved to a Barclays Bank PLC sub-consolidated "
         "basis (PRA approval granted 20 December 2022, effective 1 January 2023). These bases are not directly "
         "comparable year-on-year.",
)

metric(
    "LCR", "£bn / %",
    [
        ("Barclays Bank PLC DoLSub Liquidity Pool (£bn)", {"FY2025": 229.9, "FY2024": 179.3, "FY2023": 176, "FY2022": 191, "FY2021": 167}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "149.7%", "FY2024": "147.9%", "FY2023": "151%", "FY2022": "148%", "FY2021": "140%"}),
    ],
    p3_sources(),
    note="LCR is an average of the last 12 spot month-end ratios for the Barclays Bank PLC Domestic Liquidity "
         "Sub-Group (DoLSub, comprising Barclays Bank PLC and Barclays Capital Securities Limited). Barclays "
         "prospectively changed its methodology for calculating net stress outflows on secured financing "
         "transactions from June 2025; the FY2025 Annual Report re-presents FY2024 on the new basis (147.9%, "
         "used here for comparability) — the FY2024 Annual Report originally reported FY2024 LCR as 157% "
         "(FY2023 comparator in that report: 151%, unchanged).",
)

metric(
    "NSFR", "£bn / %",
    [
        ("Total Available Stable Funding (£bn)", {"FY2025": 381, "FY2024": 372, "FY2023": 339}),
        ("Total Required Stable Funding (£bn)", {"FY2025": 337, "FY2024": 333, "FY2023": 308}),
        ("Net Stable Funding Ratio (%)", {"FY2025": "113%", "FY2024": "112%", "FY2023": "110%", "FY2022": "108%", "FY2021": "Not publicly disclosed"}),
    ],
    p3_sources(),
    note="NSFR is an average of the last four spot quarter-end ratios. It was not a UK regulatory requirement "
         "as at FY2021 (the UK NSFR regime took effect from 1 January 2022), so no FY2021 figure is available. "
         "Available/Required Stable Funding £bn breakdown was not located for FY2022 within the reviewed pages "
         "(only the ratio, 108%, was disclosed there); the ratio alone is reported for that year.",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={
        "MREL Ratio": "MREL (Minimum Requirement for own funds and Eligible Liabilities) is set and disclosed "
                      "at the Barclays PLC resolution-group level, not for Barclays Bank PLC as an individual "
                      "operating subsidiary. No MREL ratio for Barclays Bank PLC specifically was found in its "
                      "Annual Reports for FY2021-FY2025.",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from operating activities", {"FY2025": 28103, "FY2024": 1991, "FY2023": 16367, "FY2022": 24984, "FY2021": 17497}),
        ("Net cash from investing activities", {"FY2025": 2095, "FY2024": -9234, "FY2023": -18787, "FY2022": -8611, "FY2021": -1653}),
        ("Net cash from financing activities", {"FY2025": 800, "FY2024": 1931, "FY2023": -4009, "FY2022": 7386, "FY2021": 1122}),
        ("Cash and cash equivalents at end of year", {"FY2025": 229953, "FY2024": 200695, "FY2023": 208412, "FY2022": 219854, "FY2021": 185860}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "12.7%", "FY2024": "12.1%", "FY2023": "12.1%", "FY2022": "12.7%", "FY2021": "12.9%"}),
        ("Tier 1 Ratio", {"FY2025": "16.1%", "FY2024": "15.1%", "FY2023": "16.0%", "FY2022": "16.7%", "FY2021": "17.5%"}),
        ("Total Capital Ratio", {"FY2025": "19.0%", "FY2024": "18.1%", "FY2023": "19.2%", "FY2022": "20.8%", "FY2021": "20.5%"}),
        ("Leverage Ratio", {"FY2025": "5.8%", "FY2024": "5.8%", "FY2023": "6.0%", "FY2022": "4.6%", "FY2021": "3.7%"}),
        ("LCR", {"FY2025": "149.7%", "FY2024": "147.9%", "FY2023": "151%", "FY2022": "148%", "FY2021": "140%"}),
        ("NSFR", {"FY2025": "113%", "FY2024": "112%", "FY2023": "110%", "FY2022": "108%", "FY2021": "Not publicly disclosed"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. FY2021 capital figures are restated (Over-issuance "
         "of Securities matter). Leverage ratio basis changes year-on-year (see Leverage Ratio sheet).",
)

bw.save("/Users/armaan/code/katalysis/banks/BARCLAYS BANK PLC FINANCIALS.xlsx")
