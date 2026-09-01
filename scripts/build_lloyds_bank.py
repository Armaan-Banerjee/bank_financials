import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
AR_URLS = {
    "FY2025": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2025/q4/2025-lb-annual-report.pdf",
    "FY2024": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2024/q4/2024-lb-annual-report.pdf",
    "FY2023": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2023/q4/2023-lb-annual-report.pdf",
    "FY2022": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2022/full-year/2022-lb-annual-report.pdf",
    "FY2021": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2021/full-year/2021-lb-annual-report.pdf",
}
P3_URLS = {
    "FY2025": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2025/q4/2025-lb-fy-pillar-3.pdf",
    "FY2024": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2024/q4/2024-lb-fy-pillar-3.pdf",
    "FY2023": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2023/q4/2023-lb-fy-pillar-3.pdf",
    "FY2022": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2022/full-year/2022-lb-fy-pillar3.pdf",
    "FY2021": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2021/full-year/2021-lb-fy-pillar3.pdf",
}
CH_URL = "https://find-and-update.company-information.service.gov.uk/company/00002065"

ENTITY_NOTE = (
    "Entity: Lloyds Bank plc, company number 00002065, FRN 119278, LEI "
    "H7FNTJ4851HG0EXQ1Z70. Companies House confirms the active bank company. "
    "Pillar 3 figures are Lloyds Bank plc Group consolidated prudential figures, "
    "not Lloyds Banking Group plc or Bank of Scotland plc."
)


def annual_sources(kind):
    pages = {"FY2025": 79, "FY2024": 81, "FY2023": 82, "FY2022": 82, "FY2021": 82}
    urls = AR_URLS if kind == "annual" else P3_URLS
    label = "Annual Report and Accounts" if kind == "annual" else "Year-End Pillar 3 disclosure"
    return "\n".join([f"{y}: Lloyds Bank plc {label}, p.{pages[y]} — {urls[y]}" for y in YEARS] + [ENTITY_NOTE, f"Companies House — {CH_URL}"])


bw = BankWorkbook("Lloyds Bank plc", YEARS, header_color="005A8D")

cash_rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax", {"FY2025": 5472, "FY2024": 4688, "FY2023": 7056, "FY2022": 6094, "FY2021": 5785}),
    ("DATA", "Change in operating assets", {"FY2025": -22432, "FY2024": -21996, "FY2023": 8923, "FY2022": -2900, "FY2021": 5174}),
    ("DATA", "Change in operating liabilities", {"FY2025": 15414, "FY2024": 4470, "FY2023": -15325, "FY2022": 16894, "FY2021": 8110}),
    ("DATA", "Non-cash and other items", {"FY2025": 5889, "FY2024": 6051, "FY2023": 4818, "FY2022": -129, "FY2021": -661}),
    ("DATA", "Tax paid/(refunded), net", {"FY2025": -2157, "FY2024": -462, "FY2023": -1357, "FY2022": -649, "FY2021": -715}),
    ("TOTAL", "Net cash provided by/(used in) operating activities", {"FY2025": 2186, "FY2024": -7249, "FY2023": 4115, "FY2022": 19310, "FY2021": 17693}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of financial assets", {"FY2025": -19761, "FY2024": -10508, "FY2023": -10303, "FY2022": -7953, "FY2021": -8885}),
    ("DATA", "Proceeds from sale and maturity of financial assets", {"FY2025": 14296, "FY2024": 7053, "FY2023": 5289, "FY2022": 11041, "FY2021": 8134}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -4454, "FY2024": -3693, "FY2023": -3489, "FY2022": -3704, "FY2021": -3102}),
    ("DATA", "Proceeds from sale of property, plant and equipment", {"FY2025": 1528, "FY2024": 1183, "FY2023": 979, "FY2022": 871, "FY2021": 1028}),
    ("TOTAL", "Net cash used in investing activities", {"FY2025": -9635, "FY2024": -7203, "FY2023": -9290, "FY2022": 255, "FY2021": -2828}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividends and distributions paid", {"FY2025": -2810, "FY2024": -4353, "FY2023": -5034, "FY2022": -582, "FY2021": -3244}),
    ("DATA", "Issue of subordinated liabilities and other equity", {"FY2025": 3261, "FY2024": 1554, "FY2023": 1415, "FY2022": 837, "FY2021": 3262}),
    ("DATA", "Repayments/redemptions of capital instruments", {"FY2025": -2671, "FY2024": -500, "FY2023": -251, "FY2022": -2216, "FY2021": -3745}),
    ("DATA", "Net borrowings from/(repayments to) parent", {"FY2025": 992, "FY2024": 1415, "FY2023": 1011, "FY2022": 1852, "FY2021": -4353}),
    ("TOTAL", "Net cash used in financing activities", {"FY2025": -1807, "FY2024": -2251, "FY2023": -3444, "FY2022": -406, "FY2021": -10526}),
    ("DATA", "Effects of exchange rate changes", {"FY2025": 143, "FY2024": -123, "FY2023": -44, "FY2022": 82, "FY2021": -1}),
    ("TOTAL", "Change in cash and cash equivalents", {"FY2025": -9113, "FY2024": -16826, "FY2023": -8663, "FY2022": 19241, "FY2021": 4338}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 49712, "FY2024": 66538, "FY2023": 75201, "FY2022": 55960, "FY2021": 51622}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 40599, "FY2024": 49712, "FY2023": 66538, "FY2022": 75201, "FY2021": 55960}),
]
bw.add_cash_flow_sheet("Lloyds Bank plc — Cash Flow Statement", "Lloyds Bank plc Group consolidated basis, £m.", cash_rows, annual_sources("annual"), first_col_width=66, unit_suffix=" (£m)")


ANNUAL = {
    "CET1 Capital": [26468, 25610, 26220, 25926, 26904],
    "CET1 Ratio": ["13.6%", "13.7%", "14.4%", "14.8%", "16.7%"],
    "Tier 1 Capital": [31835, 31305, 31238, 30194, 31853],
    "Tier 1 Ratio": ["16.4%", "16.7%", "17.1%", "17.3%", "19.7%"],
    "Total Capital": [38995, 37214, 37402, 35815, 37909],
    "Total Capital Ratio": ["20.1%", "19.9%", "20.5%", "20.5%", "23.5%"],
    "Total RWAs": [194300, 186996, 182560, 174902, 161576],
    "Leverage Ratio": ["5.2%", "5.4%", "5.6%", "5.4%", "5.3%"],
    "LCR": ["135%", "137%", "133%", "136%", "126%"],
    "NSFR": ["119%", "124%", "126%", None, None],
}
for name, values in ANNUAL.items():
    unit = "%" if "Ratio" in name or name in {"LCR", "NSFR"} else "£m"
    row = [(name, {y: v for y, v in zip(YEARS, values) if v is not None})]
    note = "Figures are Group consolidated. 2021/2022 NSFR was not separately disclosed in the reviewed year-end KM1 extracts." if name == "NSFR" else None
    bw.add_metric_sheet(name, unit, row, annual_sources("p3"), note=note, first_col_width=58)
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    annual_sources("p3"),
    per_note={"MREL Ratio": "A numeric MREL ratio for Lloyds Bank plc Group was not disclosed in the reviewed Lloyds Bank plc year-end reports; parent-level or instrument data is not substituted."},
)


INTERIM_URLS = {
    "2025-Q1": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2025/q1/2025-lb-q1-pillar-3.pdf",
    "2025-H1": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2025/q2/2025-lb-hy-pillar-3.pdf",
    "2025-Q3": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2025/q3/2025-lb-q3-pillar-3.pdf",
    "2024-Q1": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2024/q1/2024-lb-q1-pillar-3.pdf",
    "2024-H1": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2024/q2/2024-lb-hy-pillar-3.pdf",
    "2024-Q3": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2024/q3/2024-lb-q3-pillar-3.pdf",
    "2023-Q1": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2023/q1/2023-lb-q1-pillar-3.pdf",
    "2023-H1": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2023/q2/2023-lb-hy-pillar-3.pdf",
    "2023-Q3": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2023/q3/2023-lb-q3-pillar-3.pdf",
    "2022-Q1": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2022/q1/2022-lb-q1-pillar-3.pdf",
    "2022-H1": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2022/half-year/2022-lb-hy-pillar-3.pdf",
    "2022-Q3": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2022/q3/2022-lb-q3-pillar-3.pdf",
    "2021-Q1": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2021/q1/2021-lb-q1-ims-pillar-3.pdf",
    "2021-H1": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2021/half-year/2021-lb-hy-pillar-3.pdf",
    "2021-Q3": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2021/q3/2021-lb-q3-pillar-3.pdf",
}
INTERIM_VALUES = {
    "2025-Q1": [26052, 32497, 38044, 190951, "13.6%", "17.0%", "19.9%", 588776, "5.5%", "137%", "123%"],
    "2025-H1": [26094, 31852, 38926, 191291, "13.6%", "16.7%", "20.3%", 593908, "5.4%", "136%", "122%"],
    "2025-Q3": [25926, 30532, 37739, 190570, "13.6%", "16.0%", "19.8%", 606659, "5.0%", "136%", "121%"],
    "2024-Q1": [26243, 31261, 37081, 184304, "14.2%", "17.0%", "20.1%", 569835, "5.5%", "134%", "126%"],
    "2024-H1": [25038, 30056, 35681, 183949, "13.6%", "16.3%", "19.4%", 574932, "5.2%", "134%", "125%"],
    "2024-Q3": [25197, 30625, 36684, 184910, "13.6%", "16.6%", "19.8%", 582214, "5.3%", "135%", "124%"],
    "2023-Q1": [26246, 31264, 37074, 174916, "15.0%", "17.9%", "21.2%", 551508, "5.7%", "134%", "127%"],
    "2023-H1": [26354, 31372, 37035, 178534, "14.8%", "17.6%", "20.7%", 551063, "5.7%", "133%", "127%"],
    "2023-Q3": [25709, 30728, 36967, 180311, "14.3%", "17.0%", "20.5%", 561710, "5.5%", "133%", "126%"],
    "2022-Q1": [25399, 29667, 35015, 175416, "14.5%", "16.9%", "20.0%", 576845, "5.1%", "131%", None],
    "2022-H1": [26456, 30724, 35920, 173784, "15.2%", "17.7%", "20.7%", 572127, "5.4%", "134%", None],
    "2022-Q3": [25944, 30212, 35297, 173192, "15.0%", "17.4%", "20.4%", 575772, "5.2%", "138%", None],
    "2021-Q1": [27069, 33684, 40149, 168215, "16.1%", "20.0%", "23.9%", 584853, "5.6%", "124%", None],
    "2021-H1": [26960, 31909, 38362, 167190, "16.1%", "19.1%", "22.9%", 587248, "5.3%", "122%", None],
    "2021-Q3": [26749, 31698, 37149, 166677, "16.0%", "19.0%", "22.3%", 591233, "5.2%", "121%", None],
}
INTERIM_METRICS = [
    ("CET1 capital", "£m"), ("Tier 1 capital", "£m"), ("Total capital", "£m"),
    ("Total risk-weighted exposure amount", "£m"), ("CET1 ratio", "%"),
    ("Tier 1 ratio", "%"), ("Total capital ratio", "%"),
    ("Total exposure measure excluding claims on central banks", "£m"),
    ("Leverage ratio excluding claims on central banks", "%"),
    ("Average liquidity coverage ratio", "%"), ("Average net stable funding ratio", "%"),
]
interim_rows, interim_links = [], {}
for period, values in INTERIM_VALUES.items():
    for idx, ((metric_name, unit), value) in enumerate(zip(INTERIM_METRICS, values)):
        if value is None:
            continue
        i = len(interim_rows)
        interim_rows.append([period, "Quarterly/interim Pillar 3 disclosure", metric_name, value, unit, "Lloyds Bank plc Group consolidated basis", f"Lloyds Bank plc {period} Pillar 3 disclosure", "KM1, pp.4–6"])
        interim_links[(i, 6)] = INTERIM_URLS[period]
# The wide helper uses field 7 as the source URL.  The legacy long-form rows
# retain the same eight fields, with the source label replaced here by the
# already-defined period-specific official URL that was formerly supplied via
# ``interim_links``.
wide_interim_rows = [
    row[:6] + [INTERIM_URLS[row[0]], row[7]] for row in interim_rows
]
bw.add_wide_interim_sheet(
    "Interim Pillar 3",
    rows=wide_interim_rows,
    hyperlink_cells={(i, 6): row[6] for i, row in enumerate(wide_interim_rows)},
    subtitle="Quarterly and half-year KM1 disclosures, 2021–2025",
    note="Official Lloyds Bank plc reports publish limited Pillar 3 disclosures at interim quarter ends and half-year. 2021–2025 observations are consolidated Lloyds Bank plc Group figures; no values are substituted from Lloyds Banking Group plc or Bank of Scotland plc. NSFR was not disclosed in the reviewed 2021–2022 interim KM1 extracts.",
)
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 2186, "FY2024": -7249, "FY2023": 4115, "FY2022": 19310, "FY2021": 17693}),
        ("Net cash from/(used in) investing activities", {"FY2025": -9635, "FY2024": -7203, "FY2023": -9290, "FY2022": 255, "FY2021": -2828}),
        ("Net cash from/(used in) financing activities", {"FY2025": -1807, "FY2024": -2251, "FY2023": -3444, "FY2022": -406, "FY2021": -10526}),
        ("Cash and cash equivalents at end of year", {"FY2025": 40599, "FY2024": 49712, "FY2023": 66538, "FY2022": 75201, "FY2021": 55960}),
    ], cash_flow_unit="£m",
    ratios=[("CET1 Ratio", {y: v for y, v in zip(YEARS, ANNUAL["CET1 Ratio"])}), ("Tier 1 Ratio", {y: v for y, v in zip(YEARS, ANNUAL["Tier 1 Ratio"])}), ("Total Capital Ratio", {y: v for y, v in zip(YEARS, ANNUAL["Total Capital Ratio"])}), ("Leverage Ratio", {y: v for y, v in zip(YEARS, ANNUAL["Leverage Ratio"])}), ("LCR", {y: v for y, v in zip(YEARS, ANNUAL["LCR"])})],
    note="Annual figures are consolidated Lloyds Bank plc Group metrics; interim observations are on the Interim Pillar 3 sheet.")

bw.save("/Users/armaan/code/katalysis/banks/LLOYDS BANK FINANCIALS.xlsx")
