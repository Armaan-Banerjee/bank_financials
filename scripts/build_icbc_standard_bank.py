import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first

AR25_URL = "https://v.icbc.com.cn/userfiles/resources/icbc/haiwai/standardbank/download/2023/consolidatedannualreport2025.pdf"
AR23_URL = "https://v.icbc.com.cn/userfiles/resources/icbc/haiwai/standardbank/download/2023/2023annualreportyasuo.pdf"
AR21_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/StandardBank/Download/2022/Consolidated_Annual_Report_2021.pdf"

P3_25_URL = "https://v.icbc.com.cn/userfiles/resources/icbc/haiwai/standardbank/download/2023/2025pillar3disclosures.pdf"
P3_23_URL = "https://v.icbc.com.cn/userfiles/resources/icbc/haiwai/standardbank/download/2023/2023pillar3.pdf"
P3_21_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/StandardBank/Download/2022/2021_Pillar_3_document.pdf"

CASH_FLOW_SOURCES = (
    "Sources — all figures are ICBC Standard Bank Plc consolidated (Group) statement of cash flows, $m:\n"
    f"FY2025 & FY2024: ICBC Standard Bank Consolidated Annual Report 2025, p.68 (Consolidated Statement of Cash Flows) — {AR25_URL}\n"
    f"FY2023 & FY2022: ICBC Standard Bank Consolidated Annual Report 2023, p.65 (11. Consolidated statement of cash flows) — {AR23_URL}\n"
    f"FY2021: ICBC Standard Bank Consolidated Annual Report 2021, p.65 (10. Consolidated statement of cash flows) — {AR21_URL}\n"
    "Note: presentation granularity changed across report vintages. FY2025/FY2024 report a single 'Non-cash items "
    "included in profit before tax' adjustment and disclose interest received/paid only in a footnote; FY2023/FY2022 "
    "separately reconcile 'Net interest income' and show 'Interest received'/'Interest paid' as distinct lines within "
    "operating activities; FY2021 additionally itemises several one-off non-cash adjustments (equity-settled share-based "
    "payments, impairments, restructuring/commodity-inventory provisions) not repeated in later years. Blank cells "
    "indicate that year's report did not disclose that specific line; all section totals (cash flows from operating/"
    "investing/financing activities, and cash and cash equivalents at start/end of year) reconcile exactly year-on-year "
    "across all 5 years."
)

def p3_sources(page_25="5", page_23="5", page_21_capital="23", page_21_leverage="87", page_21_lcr="28"):
    return (
        "Sources — ICBC Standard Bank Plc (ICBCS Group) consolidated (Pillar 3) basis:\n"
        f"FY2025 & FY2024: ICBC Standard Bank Pillar 3 Disclosures 2025, p.{page_25} (UK KM1 - Key metrics template) — {P3_25_URL}\n"
        f"FY2023 & FY2022: ICBC Standard Bank Pillar 3 Disclosures 2023, p.{page_23} (UK KM1 - Key metrics template) — {P3_23_URL}\n"
        f"FY2021: ICBC Standard Bank Pillar 3 Disclosures 2021, p.{page_21_capital} (Table 5: ICBCS - Capital Resources), "
        f"p.{page_21_leverage} (Annex D: Leverage Ratio Common Disclosure Template), "
        f"p.{page_21_lcr} (Table 8: Average Consolidated Liquidity Coverage Ratio for ICBCS Group) — {P3_21_URL}"
    )

bw = BankWorkbook(bank_name="ICBC Standard Bank Plc", years=YEARS, header_color="C1272D")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Reconciliation of profit before tax to net cash flows from operating activities", {}),
    ("DATA", "Profit before taxation", {"FY2025": 280.9, "FY2024": 187.0, "FY2023": 210.6, "FY2022": 375.5, "FY2021": 120.7}),
    ("DATA", "Non-cash items included in profit before tax (as reported)", {"FY2025": -4.5, "FY2024": -48.1}),
    ("DATA", "Net interest income (as reported)", {"FY2023": -153.9, "FY2022": -98.5, "FY2021": -112.0}),
    ("DATA", "Amortisation of intangible assets", {"FY2025": 6.5, "FY2024": 8.7, "FY2023": 9.6, "FY2022": 11.0, "FY2021": 11.2}),
    ("DATA", "Depreciation of property and equipment", {"FY2025": 12.5, "FY2024": 14.8, "FY2023": 17.5, "FY2022": 18.2, "FY2021": 17.9}),
    ("DATA", "Non-cash flow movements on fair value hedges", {"FY2025": 2.3, "FY2024": -2.8, "FY2023": -2.2, "FY2022": 0.9, "FY2021": 0}),
    ("DATA", "Incentive charges / cash-settled incentive payments", {"FY2025": 93.1, "FY2024": 69.4, "FY2023": 72.9, "FY2022": 64.6, "FY2021": 10.4}),
    ("DATA", "Equity-settled share-based payments", {"FY2021": -0.3}),
    ("DATA", "Net credit impairment charges/(recoveries)", {"FY2025": 15.0, "FY2024": 2.7, "FY2023": -50.2, "FY2022": 60.8, "FY2021": -2.8}),
    ("DATA", "Impairment of property and equipment", {"FY2021": -0.9}),
    ("DATA", "Impairment of intangible assets", {"FY2021": 0}),
    ("DATA", "Provisions for commodity inventory intermediation costs", {"FY2021": -7.0}),
    ("DATA", "Restructuring provisions", {"FY2021": -5.3}),
    ("DATA", "Provisions for leave pay", {"FY2025": -0.1, "FY2024": 0.3, "FY2023": 0.3, "FY2022": -1.4, "FY2021": -0.3}),
    ("TOTAL", "Subtotal after non-cash adjustments", {"FY2025": 405.7, "FY2024": 232.0, "FY2023": 104.6, "FY2022": 431.1, "FY2021": 31.6}),
    ("SECTION", "Changes in operating funds", {}),
    ("DATA", "(Increase)/decrease in income-earning assets", {"FY2025": -8294.0, "FY2024": -2780.4, "FY2023": -4382.4, "FY2022": 2981.5, "FY2021": 1974.8}),
    ("DATA", "Increase/(decrease) in interest bearing and non-interest bearing liabilities", {"FY2025": 6161.5, "FY2024": 2706.7, "FY2023": 1994.6, "FY2022": -4589.9, "FY2021": 154.2}),
    ("TOTAL", "Changes in operating funds (subtotal)", {"FY2025": -2132.5, "FY2024": -73.7, "FY2023": -2387.8, "FY2022": -1608.4, "FY2021": 2129.0}),
    ("DATA", "Interest received (as reported)", {"FY2023": 505.7, "FY2022": 244.1, "FY2021": 146.2}),
    ("DATA", "Interest paid (as reported)", {"FY2023": -336.2, "FY2022": -149.5, "FY2021": -24.0}),
    ("DATA", "Corporation and withholding tax paid", {"FY2025": -53.5, "FY2024": -30.2, "FY2023": -37.0, "FY2022": -54.6, "FY2021": -27.0}),
    ("TOTAL", "Cash flows (used in)/from operating activities", {"FY2025": -1780.3, "FY2024": 128.1, "FY2023": -2150.7, "FY2022": -1137.3, "FY2021": 2255.8}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Capital expenditure on intangible assets", {"FY2025": -5.0, "FY2024": -11.5, "FY2023": -5.1, "FY2022": -11.4, "FY2021": -9.4}),
    ("DATA", "Capital expenditure on property and equipment", {"FY2025": -13.0, "FY2024": -4.9, "FY2023": -1.8, "FY2022": -4.1, "FY2021": -3.1}),
    ("TOTAL", "Cash flows used in investing activities", {"FY2025": -18.0, "FY2024": -16.4, "FY2023": -6.9, "FY2022": -15.5, "FY2021": -12.5}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Proceeds from issuance of subordinated debt", {"FY2024": 100.0, "FY2022": 150.0}),
    ("DATA", "Repayment of subordinated debt", {"FY2024": -100.0, "FY2022": -150.0}),
    ("DATA", "Dividend payment on ordinary share capital", {"FY2025": -41.8, "FY2024": -49.9}),
    ("DATA", "Coupon payment on other equity instruments", {"FY2025": -12.4, "FY2024": -12.2, "FY2023": -12.2, "FY2022": -12.2, "FY2021": -12.2}),
    ("DATA", "Principal payments on leasehold liabilities", {"FY2025": -9.4, "FY2024": -8.5, "FY2023": -10.4, "FY2022": -9.7, "FY2021": -12.5}),
    ("TOTAL", "Cash flows used in financing activities", {"FY2025": -63.6, "FY2024": -70.6, "FY2023": -22.6, "FY2022": -21.9, "FY2021": -24.7}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -1861.9, "FY2024": 41.1, "FY2023": -2180.2, "FY2022": -1174.7, "FY2021": 2218.6}),
    ("DATA", "Effects of exchange rate changes on cash and cash equivalents", {"FY2025": 2.5, "FY2024": -23.5, "FY2023": -65.8, "FY2022": 42.6, "FY2021": -2.5}),
    ("DATA", "Cash and cash equivalents at beginning of the year", {"FY2025": 2762.0, "FY2024": 2744.4, "FY2023": 4990.4, "FY2022": 6122.5, "FY2021": 3906.4}),
    ("TOTAL", "Cash and cash equivalents at end of the year", {"FY2025": 902.6, "FY2024": 2762.0, "FY2023": 2744.4, "FY2022": 4990.4, "FY2021": 6122.5}),
]

bw.add_cash_flow_sheet(
    title="ICBC Standard Bank Plc — Consolidated Statement of Cash Flows",
    subtitle="ICBC Standard Bank Group (consolidated basis), $m unless stated",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=72,
    source_height=110,
    unit_suffix=" ($m)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Consolidated basis, {unit}" if unit else "Consolidated basis",
                         rows_data, sources_text, note=note, first_col_width=48, source_height=100)

metric(
    "CET1 Capital", "$m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 1819.5, "FY2024": 1676.1, "FY2023": 1629.1, "FY2022": 1454.6, "FY2021": 1148.4})],
    p3_sources(),
    note="FY2021 figure is 'Total Common Equity Tier I' from Table 5 (Capital Resources), the transitional-basis "
         "equivalent of the UK KM1 template row used from FY2022 onward.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "12.2%", "FY2024": "14.6%", "FY2023": "16.9%", "FY2022": "15.7%", "FY2021": "13.47%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "$m",
    [("Tier 1 capital", {"FY2025": 1979.5, "FY2024": 1836.1, "FY2023": 1789.1, "FY2022": 1614.6, "FY2021": 1308.4})],
    p3_sources(),
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "13.3%", "FY2024": "16.0%", "FY2023": "18.5%", "FY2022": "17.5%", "FY2021": "15.35%"})],
    p3_sources(),
    note="FY2021 figure is 'Tier 1 Risk Asset Ratio' from Table 5, the transitional-basis equivalent of the later "
         "UK KM1 template row.",
)

metric(
    "Total Capital", "$m",
    [("Total capital", {"FY2025": 2229.5, "FY2024": 2086.1, "FY2023": 2039.1, "FY2022": 1864.6, "FY2021": 1558.4})],
    p3_sources(),
    note="FY2021 figure is 'Total eligible capital' from Table 5, the transitional-basis equivalent of the later "
         "UK KM1 template row.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "15.0%", "FY2024": "18.1%", "FY2023": "21.1%", "FY2022": "20.2%", "FY2021": "18.28%"})],
    p3_sources(),
    note="FY2021 figure is 'Capital Adequacy ratio' from Table 5, the transitional-basis equivalent of the later "
         "UK KM1 template row.",
)

metric(
    "Total RWAs", "$m",
    [("Total risk-weighted exposure amount", {"FY2025": 14902.7, "FY2024": 11500.1, "FY2023": 9653.2, "FY2022": 9251.0, "FY2021": 8526.3})],
    p3_sources(),
)

metric(
    "Leverage Ratio", "$m / %",
    [
        ("Total exposure measure excluding claims on central banks ($m)", {"FY2025": 35294.7, "FY2024": 26624.0, "FY2023": 23301.0, "FY2022": 20958.2, "FY2021": 25680}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "5.6%", "FY2024": "6.9%", "FY2023": "7.7%", "FY2022": "7.7%", "FY2021": "5.09%"}),
    ],
    p3_sources(),
    note="FY2021 uses the CRR Leverage Ratio Common Disclosure Template's 'Total leverage ratio exposures' and "
         "'Leverage ratio' rows (Annex D) — the pre-'excluding central banks' presentation format used before the "
         "later UK KM1 template split the exposure measure basis.",
)

metric(
    "LCR", "$m / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value (average) ($m)", {"FY2025": 5294.2, "FY2024": 5216.2, "FY2023": 5704.2, "FY2022": 6280.5, "FY2021": 5027}),
        ("Total net cash outflows, adjusted value ($m)", {"FY2025": 2777.2, "FY2024": 2422.5, "FY2023": 3561.5, "FY2022": 2926.2, "FY2021": 2425}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "197.3%", "FY2024": "226.7%", "FY2023": "165.3%", "FY2022": "206.0%", "FY2021": "207%"}),
    ],
    p3_sources(),
    note="LCR figures are averages of month-end observations over the 12 months preceding each year-end. FY2021 "
         "figures are the 31 December 2021 quarter-end column of Table 8 (Average Consolidated LCR for ICBCS Group), "
         "the same consolidated-Group basis used by the later UK KM1 template rows.",
)

metric(
    "NSFR", "$m / %",
    [
        ("Total available stable funding ($m)", {"FY2025": 9393.0, "FY2024": 8348.6, "FY2023": 7963.4, "FY2022": 8417.6}),
        ("Total required stable funding ($m)", {"FY2025": 7736.7, "FY2024": 6118.4, "FY2023": 4462.0, "FY2022": 5266.3}),
        ("Net Stable Funding Ratio (%)", {"FY2025": "122.8%", "FY2024": "136.4%", "FY2023": "183.3%", "FY2022": "163.8%", "FY2021": "Not disclosed"}),
    ],
    p3_sources(),
    note="NSFR was not a UK Pillar 3 disclosure requirement as at FY2021 (the UK NSFR regime took effect from "
         "1 January 2022), so no FY2021 figures are available. Balances are averages of the four quarter-ends "
         "preceding each year-end.",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})],
    p3_sources(),
    note="No MREL disclosure appears in any of the five ICBC Standard Bank Pillar 3 Disclosures reports reviewed "
         "(2021-2025) — ICBC Standard Bank Plc is not itself a resolution entity subject to a standalone MREL "
         "requirement.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Cash flows (used in)/from operating activities", {"FY2025": -1780.3, "FY2024": 128.1, "FY2023": -2150.7, "FY2022": -1137.3, "FY2021": 2255.8}),
        ("Cash flows used in investing activities", {"FY2025": -18.0, "FY2024": -16.4, "FY2023": -6.9, "FY2022": -15.5, "FY2021": -12.5}),
        ("Cash flows used in financing activities", {"FY2025": -63.6, "FY2024": -70.6, "FY2023": -22.6, "FY2022": -21.9, "FY2021": -24.7}),
        ("Cash and cash equivalents at end of the year", {"FY2025": 902.6, "FY2024": 2762.0, "FY2023": 2744.4, "FY2022": 4990.4, "FY2021": 6122.5}),
    ],
    cash_flow_unit="$m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "12.2%", "FY2024": "14.6%", "FY2023": "16.9%", "FY2022": "15.7%", "FY2021": "13.47%"}),
        ("Tier 1 Ratio", {"FY2025": "13.3%", "FY2024": "16.0%", "FY2023": "18.5%", "FY2022": "17.5%", "FY2021": "15.35%"}),
        ("Total Capital Ratio", {"FY2025": "15.0%", "FY2024": "18.1%", "FY2023": "21.1%", "FY2022": "20.2%", "FY2021": "18.28%"}),
        ("Leverage Ratio", {"FY2025": "5.6%", "FY2024": "6.9%", "FY2023": "7.7%", "FY2022": "7.7%", "FY2021": "5.09%"}),
        ("LCR", {"FY2025": "197.3%", "FY2024": "226.7%", "FY2023": "165.3%", "FY2022": "206.0%", "FY2021": "207%"}),
        ("NSFR", {"FY2025": "122.8%", "FY2024": "136.4%", "FY2023": "183.3%", "FY2022": "163.8%", "FY2021": "Not disclosed"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. All amounts are in USD ($m), the reporting currency used "
         "throughout ICBC Standard Bank Plc's Annual Reports and Pillar 3 Disclosures.",
)

bw.save("/Users/armaan/code/katalysis/banks/ICBC STANDARD BANK PLC FINANCIALS.xlsx")
