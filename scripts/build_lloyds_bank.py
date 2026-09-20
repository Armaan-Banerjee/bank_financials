import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017"]
AR_URLS = {
    "FY2025": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2025/q4/2025-lb-annual-report.pdf",
    "FY2024": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2024/q4/2024-lb-annual-report.pdf",
    "FY2023": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2023/q4/2023-lb-annual-report.pdf",
    "FY2022": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2022/full-year/2022-lb-annual-report.pdf",
    "FY2021": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2021/full-year/2021-lb-annual-report.pdf",
    "FY2020": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2020/2020-lb-annual-report.pdf",
    "FY2019": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2019/2019-lb-annual-report.pdf",
    "FY2018": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2018/2018-lb-annual-report.pdf",
}
P3_URLS = {
    "FY2025": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2025/q4/2025-lb-fy-pillar-3.pdf",
    "FY2024": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2024/q4/2024-lb-fy-pillar-3.pdf",
    "FY2023": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2023/q4/2023-lb-fy-pillar-3.pdf",
    "FY2022": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2022/full-year/2022-lb-fy-pillar3.pdf",
    "FY2021": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2021/full-year/2021-lb-fy-pillar3.pdf",
    "FY2020": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2020/2020-lb-fy-pillar-3.pdf",
    "FY2019": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2019/2019-lb-pillar-3-report.pdf",
}
CH_URL = "https://find-and-update.company-information.service.gov.uk/company/00002065"
AR2017_URL = "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2017/2017-lb-annual-report-v2.pdf"

ENTITY_NOTE = (
    "Entity: Lloyds Bank plc, company number 00002065, FRN 119278, LEI "
    "H7FNTJ4851HG0EXQ1Z70. Companies House confirms the active bank company. "
    "Pillar 3 figures are Lloyds Bank plc Group consolidated prudential figures, "
    "not Lloyds Banking Group plc or Bank of Scotland plc."
)


def annual_sources(kind):
    pages = {"FY2025": 79, "FY2024": 81, "FY2023": 82, "FY2022": 82, "FY2021": 82, "FY2020": 82, "FY2019": 37}
    urls = AR_URLS if kind == "annual" else P3_URLS
    label = "Annual Report and Accounts" if kind == "annual" else "Year-End Pillar 3 disclosure"
    lines = [f"{y}: Lloyds Bank plc {label}, p.{pages[y]} — {urls[y]}" for y in YEARS if y in pages and y in urls]
    if kind == "annual":
        lines.append(f"FY2018: Lloyds Bank plc Annual Report and Accounts 2018, p.23 (Balance sheets) — {AR_URLS['FY2018']}")
        lines.append(
            f"FY2017: Lloyds Bank plc Annual Report and Accounts 2017 — Consolidated income statement, printed "
            f"p.21 (PDF p.23), and Consolidated balance sheet, printed p.23 — {AR2017_URL}. The GROUP columns "
            f"are used, as for every other year: this is Lloyds Bank plc's own consolidated report, not Lloyds "
            f"Banking Group plc's (whose FY2017 total assets were £812.1bn against Lloyds Bank plc Group's "
            f"£823,030m), and not the Company-only columns on the same pages (total assets £576,953m). "
            f"Re-verified against the primary document 2026-09-16. FY2017 is the only year in this workbook "
            f"with discontinued operations: 'Profit before tax' 5,035 is the report's own 'Profit before tax – "
            f"continuing operations' line, consistent with every other year, and the £796m profit after tax "
            f"from discontinued operations is carried on its own separate row rather than blended in. Balance "
            f"Sheet FY2017 shows the three headline lines only (cash at central banks, loans and advances to "
            f"customers, total assets); the remaining FY2017 balance sheet lines are blank, not zero.")
    else:
        lines.append("FY2018: no standalone Pillar 3 disclosure located (full Pillar 3 reporting for Lloyds Bank plc began with the FY2019 year-end, following 1 January 2019 ring-fencing implementation); regulatory metrics left blank.")
        lines.append("FY2017: no historical Pillar 3 disclosure located; regulatory metrics left blank.")
    return "\n".join(lines + [ENTITY_NOTE, f"Companies House — {CH_URL}"])


bw = BankWorkbook("Lloyds Bank plc", YEARS, header_color="005A8D")

STATEMENTS_SOURCES = (
    "Sources - Lloyds Bank plc Group consolidated Annual Report and Accounts:\n"
    f"FY2025/FY2024/FY2023: Annual Report and Accounts 2025, Consolidated income statement p.73, Consolidated "
    f"statement of comprehensive income p.74, Consolidated balance sheet p.75, Consolidated statement of changes "
    f"in equity p.76-78 - {AR_URLS['FY2025']}\n"
    f"FY2022: Annual Report and Accounts 2023, Consolidated balance sheet p.78, Consolidated statement of changes "
    f"in equity p.80 - {AR_URLS['FY2023']}\n"
    f"FY2021: Annual Report and Accounts 2021, Balance sheets (Group column) p.82-83, and Annual Report and "
    f"Accounts 2023's Consolidated statement of changes in equity p.81-82 for the FY2021 opening/closing equity "
    f"roll-forward - {AR_URLS['FY2021']} and {AR_URLS['FY2023']}\n"
    f"FY2020: Annual Report and Accounts 2020, Consolidated income statement p.79, Statements of comprehensive "
    f"income p.80, Balance sheets p.82-83, Statements of changes in equity p.84-85, Cash flow statements p.89, "
    f"'Financial assets at amortised cost' (loans by IFRS 9 stage) note p.130 - {AR_URLS['FY2020']}\n"
    f"FY2019: Annual Report and Accounts 2019, Consolidated income statement p.34, Statements of comprehensive "
    f"income p.35, Balance sheets p.37-38, Statements of changes in equity p.39-40, Cash flow statements p.44, "
    f"'Financial assets at amortised cost' (loans by IFRS 9 stage) note p.80 - {AR_URLS['FY2019']}\n"
    f"FY2018: Annual Report and Accounts 2018, Consolidated income statement p.20, Statements of comprehensive "
    f"income p.21, Balance sheets p.23, Statements of changes in equity p.25-26, Cash flow statements p.28, "
    f"'Financial assets at amortised cost' (loans by IFRS 9 stage) note p.59 - {AR_URLS['FY2018']}\n\n"
    "DATA QUALITY FLAG: 'Items in the course of collection from banks' (asset) and 'Items in course of "
    "transmission to banks' (liability) are genuinely disclosed as standalone balance sheet lines for FY2018 "
    "(645/615), FY2019 (292/354), FY2020 (300/302) and FY2021 (147/308) alike, before being folded into Other "
    "assets/Other liabilities from FY2022 onward - not a FY2021-only feature. 'Reverse repurchase agreements' "
    "and 'Repurchase agreements' are not disclosed as standalone balance sheet lines in FY2018-FY2020 (embedded "
    "within Loans and advances to banks/customers and Customer deposits/Deposits from banks respectively under "
    "the pre-2021 presentation) and are left blank for those years rather than estimated. 'Deferred tax "
    "liabilities' is not disclosed as a separate line in FY2018-FY2020 (only a Deferred tax assets line appears) "
    "and is left blank for those years. The Cash Flow Statement's own FY2020 Annual Report and Accounts states "
    "cash and cash equivalents at the end of FY2020 as £48,966m, while the FY2021 Annual Report and Accounts "
    "states cash and cash equivalents at the beginning of FY2021 as £51,622m - a genuine £2,656m discontinuity "
    "between what each year's own report discloses (likely a scope/definitional restatement), shown here exactly "
    "as each year's own report states it rather than forced to tie.\n\n"
    + ENTITY_NOTE
)

cash_rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax", {"FY2025": 5472, "FY2024": 4688, "FY2023": 7056, "FY2022": 6094, "FY2021": 5785, "FY2020": 1329, "FY2019": 3474, "FY2018": 6309}),
    ("DATA", "Change in operating assets", {"FY2025": -22432, "FY2024": -21996, "FY2023": 8923, "FY2022": -2900, "FY2021": 5174, "FY2020": -6856, "FY2019": 12872, "FY2018": 34216}),
    ("DATA", "Change in operating liabilities", {"FY2025": 15414, "FY2024": 4470, "FY2023": -15325, "FY2022": 16894, "FY2021": 8110, "FY2020": 17841, "FY2019": -5630, "FY2018": -61433}),
    ("DATA", "Non-cash and other items", {"FY2025": 5889, "FY2024": 6051, "FY2023": 4818, "FY2022": -129, "FY2021": -661, "FY2020": 3484, "FY2019": 2150, "FY2018": -1424}),
    ("DATA", "Tax paid/(refunded), net", {"FY2025": -2157, "FY2024": -462, "FY2023": -1357, "FY2022": -649, "FY2021": -715, "FY2020": -616, "FY2019": -1232, "FY2018": -1616}),
    ("TOTAL", "Net cash provided by/(used in) operating activities", {"FY2025": 2186, "FY2024": -7249, "FY2023": 4115, "FY2022": 19310, "FY2021": 17693, "FY2020": 15182, "FY2019": 11634, "FY2018": -23948}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of financial assets", {"FY2025": -19761, "FY2024": -10508, "FY2023": -10303, "FY2022": -7953, "FY2021": -8885, "FY2020": -8539, "FY2019": -9108, "FY2018": -12309}),
    ("DATA", "Proceeds from sale and maturity of financial assets", {"FY2025": 14296, "FY2024": 7053, "FY2023": 5289, "FY2022": 11041, "FY2021": 8134, "FY2020": 6225, "FY2019": 8847, "FY2018": 26863}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -4454, "FY2024": -3693, "FY2023": -3489, "FY2022": -3704, "FY2021": -3102, "FY2020": -2815, "FY2019": -3552, "FY2018": -3450}),
    ("DATA", "Proceeds from sale of property, plant and equipment", {"FY2025": 1528, "FY2024": 1183, "FY2023": 979, "FY2022": 871, "FY2021": 1028, "FY2020": 1063, "FY2019": 1258, "FY2018": 1262}),
    ("DATA", "Acquisitions of businesses, net of cash acquired", {"FY2018": -26}),
    ("DATA", "Disposals of businesses, net of cash disposed", {"FY2019": 107, "FY2018": 8604}),
    ("TOTAL", "Net cash used in investing activities", {"FY2025": -9635, "FY2024": -7203, "FY2023": -9290, "FY2022": 255, "FY2021": -2828, "FY2020": -4066, "FY2019": -2448, "FY2018": 20944}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividends and distributions paid", {"FY2025": -2810, "FY2024": -4353, "FY2023": -5034, "FY2022": -582, "FY2021": -3244, "FY2020": -424, "FY2019": -4419, "FY2018": -11333}),
    ("DATA", "Issue of subordinated liabilities and other equity", {"FY2025": 3261, "FY2024": 1554, "FY2023": 1415, "FY2022": 837, "FY2021": 3262, "FY2020": 1373, "FY2019": 2428, "FY2018": 201}),
    ("DATA", "Repayments/redemptions of capital instruments", {"FY2025": -2671, "FY2024": -500, "FY2023": -251, "FY2022": -2216, "FY2021": -3745, "FY2020": -5012, "FY2019": -1673, "FY2018": -6262}),
    ("DATA", "Net borrowings from/(repayments to) parent", {"FY2025": 992, "FY2024": 1415, "FY2023": 1011, "FY2022": 1852, "FY2021": -4353, "FY2020": 3298, "FY2019": -6628, "FY2018": -864}),
    ("TOTAL", "Net cash used in financing activities", {"FY2025": -1807, "FY2024": -2251, "FY2023": -3444, "FY2022": -406, "FY2021": -10526, "FY2020": -765, "FY2019": -10292, "FY2018": -18258}),
    ("DATA", "Effects of exchange rate changes", {"FY2025": 143, "FY2024": -123, "FY2023": -44, "FY2022": 82, "FY2021": -1, "FY2020": 1, "FY2019": -3, "FY2018": 3}),
    ("TOTAL", "Change in cash and cash equivalents", {"FY2025": -9113, "FY2024": -16826, "FY2023": -8663, "FY2022": 19241, "FY2021": 4338, "FY2020": 10352, "FY2019": -1109, "FY2018": -21259}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 49712, "FY2024": 66538, "FY2023": 75201, "FY2022": 55960, "FY2021": 51622, "FY2020": 38614, "FY2019": 39723, "FY2018": 60982}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 40599, "FY2024": 49712, "FY2023": 66538, "FY2022": 75201, "FY2021": 55960, "FY2020": 48966, "FY2019": 38614, "FY2018": 39723}),
]
# ---------------------------------------------------------------
# Balance Sheet - equity reconciliation ladder step 1: built first so each
# year's own Total equity is the independent check value for the equity
# sheet below. All 5 years tie exactly to the equity statement's own
# opening/closing balances.
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 37720, "FY2024": 42396, "FY2023": 57909, "FY2022": 72005, "FY2021": 54279, "FY2020": 49888, "FY2019": 38880, "FY2018": 40213, "FY2017": 58521}),
    ("DATA", "Items in the course of collection from banks", {"FY2021": 147, "FY2020": 300, "FY2019": 292, "FY2018": 645}),
    ("DATA", "Financial assets at fair value through profit or loss", {"FY2025": 2279, "FY2024": 2321, "FY2023": 1862, "FY2022": 1371, "FY2021": 1798, "FY2020": 1674, "FY2019": 2284, "FY2018": 23256}),
    ("DATA", "Derivative financial instruments", {"FY2025": 3260, "FY2024": 4235, "FY2023": 3165, "FY2022": 3857, "FY2021": 5511, "FY2020": 8341, "FY2019": 8494, "FY2018": 11293}),
    ("DATA", "Loans and advances to banks", {"FY2025": 5836, "FY2024": 6433, "FY2023": 8810, "FY2022": 8363, "FY2021": 4478, "FY2020": 5950, "FY2019": 4852, "FY2018": 3692}),
    ("DATA", "Loans and advances to customers", {"FY2025": 461504, "FY2024": 441907, "FY2023": 433124, "FY2022": 435627, "FY2021": 430829, "FY2020": 480141, "FY2019": 474470, "FY2018": 464044, "FY2017": 465555}),
    ("DATA", "Reverse repurchase agreements", {"FY2025": 43962, "FY2024": 44143, "FY2023": 32751, "FY2022": 39259, "FY2021": 49708}),
    ("DATA", "Debt securities (at amortised cost)", {"FY2025": 11983, "FY2024": 11854, "FY2023": 12546, "FY2022": 7331, "FY2021": 4562, "FY2020": 5137, "FY2019": 5325, "FY2018": 5095}),
    ("DATA", "Due from fellow Lloyds Banking Group undertakings", {"FY2025": 1182, "FY2024": 560, "FY2023": 840, "FY2022": 816, "FY2021": 739, "FY2020": 738, "FY2019": 1854, "FY2018": 1878}),
    ("TOTAL", "Financial assets at amortised cost", {"FY2025": 524467, "FY2024": 504897, "FY2023": 488071, "FY2022": 491396, "FY2021": 490316, "FY2020": 491966, "FY2019": 486501, "FY2018": 474709}),
    ("DATA", "Financial assets at fair value through other comprehensive income", {"FY2025": 36257, "FY2024": 30344, "FY2023": 27337, "FY2022": 22846, "FY2021": 27786, "FY2020": 27260, "FY2019": 24617, "FY2018": 24368}),
    ("DATA", "Goodwill and other intangible assets", {"FY2025": 5692, "FY2024": 5804, "FY2023": 5837, "FY2022": 5124, "FY2021": 4614, "FY2020": 4582, "FY2019": 4255, "FY2018": 3796}),
    ("DATA", "Current tax recoverable", {"FY2025": 1263, "FY2024": 338, "FY2023": 1026, "FY2022": 527, "FY2021": 220, "FY2020": 537, "FY2019": 4, "FY2018": 1}),
    ("DATA", "Deferred tax assets", {"FY2025": 3917, "FY2024": 4785, "FY2023": 4636, "FY2022": 5857, "FY2021": 4048, "FY2020": 3468, "FY2019": 3366, "FY2018": 3216}),
    ("DATA", "Retirement benefit assets", {"FY2025": 2695, "FY2024": 3028, "FY2023": 3624, "FY2022": 3823, "FY2021": 4531, "FY2020": 1714, "FY2019": 681, "FY2018": 1267}),
    ("DATA", "Other assets", {"FY2025": 13785, "FY2024": 13065, "FY2023": 11938, "FY2022": 10122, "FY2021": 9599, "FY2020": 1892, "FY2019": 2527, "FY2018": 2207}),
    ("TOTAL", "Total assets", {"FY2025": 631335, "FY2024": 611213, "FY2023": 605405, "FY2022": 616928, "FY2021": 602849, "FY2020": 599939, "FY2019": 581368, "FY2018": 593486, "FY2017": 823030}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks", {"FY2025": 3085, "FY2024": 3144, "FY2023": 3557, "FY2022": 4658, "FY2021": 3363, "FY2020": 24997, "FY2019": 23593, "FY2018": 26263}),
    ("DATA", "Customer deposits", {"FY2025": 465207, "FY2024": 451794, "FY2023": 441953, "FY2022": 446172, "FY2021": 449373, "FY2020": 434569, "FY2019": 396839, "FY2018": 391251}),
    ("DATA", "Repurchase agreements (at amortised cost)", {"FY2025": 37567, "FY2024": 37760, "FY2023": 37702, "FY2022": 48590, "FY2021": 30106}),
    ("DATA", "Due to fellow Lloyds Banking Group undertakings", {"FY2025": 3852, "FY2024": 4049, "FY2023": 2932, "FY2022": 2539, "FY2021": 1490, "FY2020": 6875, "FY2019": 4893, "FY2018": 19663}),
    ("DATA", "Items in course of transmission to banks", {"FY2021": 308, "FY2020": 302, "FY2019": 354, "FY2018": 615}),
    ("DATA", "Financial liabilities at fair value through profit or loss", {"FY2025": 4243, "FY2024": 4630, "FY2023": 5255, "FY2022": 5159, "FY2021": 6537, "FY2020": 6831, "FY2019": 7702, "FY2018": 17730}),
    ("DATA", "Derivative financial instruments (liability)", {"FY2025": 4286, "FY2024": 5787, "FY2023": 4307, "FY2022": 5891, "FY2021": 4643, "FY2020": 8228, "FY2019": 9831, "FY2018": 10911}),
    ("DATA", "Notes in circulation", {"FY2025": 2118, "FY2024": 2121, "FY2023": 1392, "FY2022": 1280, "FY2021": 1321, "FY2020": 1305, "FY2019": 1079, "FY2018": 1104}),
    ("DATA", "Debt securities in issue at amortised cost", {"FY2025": 52132, "FY2024": 45281, "FY2023": 52449, "FY2022": 49056, "FY2021": 48724, "FY2020": 59293, "FY2019": 76431, "FY2018": 64533}),
    ("DATA", "Other liabilities", {"FY2025": 5772, "FY2024": 7211, "FY2023": 6260, "FY2022": 6003, "FY2021": 5391, "FY2020": 5181, "FY2019": 5600, "FY2018": 4335}),
    ("DATA", "Retirement benefit obligations", {"FY2025": 120, "FY2024": 122, "FY2023": 136, "FY2022": 126, "FY2021": 230, "FY2020": 245, "FY2019": 257, "FY2018": 245}),
    ("DATA", "Current tax liabilities", {"FY2025": 35, "FY2024": 33, "FY2023": 23, "FY2022": 3, "FY2020": 31, "FY2019": 166, "FY2018": 394}),
    ("DATA", "Deferred tax liabilities", {"FY2025": 146, "FY2024": 125, "FY2023": 157, "FY2022": 208}),
    ("DATA", "Provisions", {"FY2025": 2772, "FY2024": 2198, "FY2023": 1916, "FY2022": 1591, "FY2021": 1933, "FY2020": 1722, "FY2019": 3138, "FY2018": 3344}),
    ("DATA", "Subordinated liabilities", {"FY2025": 8020, "FY2024": 7211, "FY2023": 6935, "FY2022": 6593, "FY2021": 8658, "FY2020": 9242, "FY2019": 12586, "FY2018": 12745}),
    ("TOTAL", "Total liabilities", {"FY2025": 589355, "FY2024": 571466, "FY2023": 564974, "FY2022": 577869, "FY2021": 562077, "FY2020": 558821, "FY2019": 542469, "FY2018": 553133}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 1574, "FY2024": 1574, "FY2023": 1574, "FY2022": 1574, "FY2021": 1574, "FY2020": 1574, "FY2019": 1574, "FY2018": 1574}),
    ("DATA", "Share premium account", {"FY2025": 600, "FY2024": 600, "FY2023": 600, "FY2022": 600, "FY2021": 600, "FY2020": 600, "FY2019": 600, "FY2018": 600}),
    ("DATA", "Other reserves", {"FY2025": 4160, "FY2024": 2389, "FY2023": 2395, "FY2022": 743, "FY2021": 5400, "FY2020": 7181, "FY2019": 7250, "FY2018": 6965}),
    ("DATA", "Retained profits", {"FY2025": 30208, "FY2024": 29412, "FY2023": 30786, "FY2022": 31792, "FY2021": 28836, "FY2020": 25750, "FY2019": 24549, "FY2018": 27924}),
    ("TOTAL", "Ordinary shareholders' equity", {"FY2025": 36542, "FY2024": 33975, "FY2023": 35355, "FY2022": 34709, "FY2021": 36410, "FY2020": 35105, "FY2019": 33973, "FY2018": 37063}),
    ("DATA", "Other equity instruments", {"FY2025": 5367, "FY2024": 5692, "FY2023": 5018, "FY2022": 4268, "FY2021": 4268, "FY2020": 5935, "FY2019": 4865, "FY2018": 3217}),
    ("TOTAL", "Total equity excluding non-controlling interests", {"FY2025": 41909, "FY2024": 39667, "FY2023": 40373, "FY2022": 38977, "FY2021": 40678, "FY2020": 41040, "FY2019": 38838, "FY2018": 40280}),
    ("DATA", "Non-controlling interests", {"FY2025": 71, "FY2024": 80, "FY2023": 58, "FY2022": 82, "FY2021": 94, "FY2020": 78, "FY2019": 61, "FY2018": 73}),
    ("TOTAL", "Total equity", {"FY2025": 41980, "FY2024": 39747, "FY2023": 40431, "FY2022": 39059, "FY2021": 40772, "FY2020": 41118, "FY2019": 38899, "FY2018": 40353}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 631335, "FY2024": 611213, "FY2023": 605405, "FY2022": 616928, "FY2021": 602849, "FY2020": 599939, "FY2019": 581368, "FY2018": 593486, "FY2017": 823030}),
]

bw.add_balance_sheet_sheet(
    title="Lloyds Bank plc — Balance Sheet",
    subtitle="Lloyds Bank plc Group consolidated basis. £m. FY2018-FY2021 show a genuine structural difference "
              "from later years: a standalone 'Items in the course of collection from banks' asset line and "
              "'Items in course of transmission to banks' liability line (both since folded into Other assets/"
              "Other liabilities from FY2022 onward), and Goodwill/Other intangible assets reported as two "
              "separate lines rather than the combined 'Goodwill and other intangible assets' line used FY2022 "
              "onward (each year's combined figure is summed here for comparability: FY2021 4,614 = 470 + 4,144; "
              "FY2020 4,582 = 470 + 4,112; FY2019 4,255 = 474 + 3,781; FY2018 3,796 = 474 + 3,322). "
              "'Reverse repurchase agreements'/'Repurchase agreements' are not disclosed as standalone lines "
              "before FY2021 (embedded within the adjacent loans/deposits lines) and are left blank for "
              "FY2018-FY2020 rather than estimated.",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=72,
    source_height=260,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 28208, "FY2024": 28386, "FY2023": 25300, "FY2022": 16562, "FY2021": 12920, "FY2020": 13866, "FY2019": 16098, "FY2018": 16216, "FY2017": 15853}),
    ("DATA", "Interest expense", {"FY2025": -14845, "FY2024": -15794, "FY2023": -11591, "FY2022": -3457, "FY2021": -1884, "FY2020": -3096, "FY2019": -3878, "FY2018": -3462, "FY2017": -3489}),
    ("TOTAL", "Net interest income", {"FY2025": 13363, "FY2024": 12592, "FY2023": 13709, "FY2022": 13105, "FY2021": 11036, "FY2020": 10770, "FY2019": 12220, "FY2018": 12754, "FY2017": 12364}),
    ("DATA", "Fee and commission income", {"FY2025": 2515, "FY2024": 2416, "FY2023": 2456, "FY2022": 2352, "FY2021": 2195, "FY2020": 1924, "FY2019": 2363, "FY2018": 2497, "FY2017": 2786}),
    ("DATA", "Fee and commission expense", {"FY2025": -1254, "FY2024": -1478, "FY2023": -1104, "FY2022": -1101, "FY2021": -942, "FY2020": -909, "FY2019": -1027, "FY2018": -1228, "FY2017": -1024}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 1261, "FY2024": 938, "FY2023": 1352, "FY2022": 1251, "FY2021": 1253, "FY2020": 1015, "FY2019": 1336, "FY2018": 1269, "FY2017": 1762}),
    ("DATA", "Net trading income", {"FY2025": 523, "FY2024": 597, "FY2023": 384, "FY2022": 180, "FY2021": 385, "FY2020": 750, "FY2019": 360, "FY2018": 408, "FY2017": 773}),
    ("DATA", "Other operating income", {"FY2025": 3282, "FY2024": 2944, "FY2023": 2922, "FY2022": 2209, "FY2021": 1999, "FY2020": 2050, "FY2019": 2692, "FY2018": 2543, "FY2017": 2453}),
    ("TOTAL", "Other income", {"FY2025": 5066, "FY2024": 4479, "FY2023": 4658, "FY2022": 3640, "FY2021": 3637, "FY2020": 3815, "FY2019": 4388, "FY2018": 4220, "FY2017": 4988}),
    ("TOTAL", "Total income", {"FY2025": 18429, "FY2024": 17071, "FY2023": 18367, "FY2022": 16745, "FY2021": 14673, "FY2020": 14585, "FY2019": 16608, "FY2018": 16974, "FY2017": 17352}),
    ("DATA", "Operating expenses", {"FY2025": -12165, "FY2024": -11927, "FY2023": -10968, "FY2022": -9199, "FY2021": -10206, "FY2020": -9196, "FY2019": -11772, "FY2018": -11119, "FY2017": -11630}),
    ("DATA", "Impairment (charge)/credit", {"FY2025": -792, "FY2024": -456, "FY2023": -343, "FY2022": -1452, "FY2021": 1318, "FY2020": -4060, "FY2019": -1362, "FY2018": -926, "FY2017": -687}),
    ("TOTAL", "Profit before tax", {"FY2025": 5472, "FY2024": 4688, "FY2023": 7056, "FY2022": 6094, "FY2021": 5785, "FY2020": 1329, "FY2019": 3474, "FY2018": 4929, "FY2017": 5035}),
    ("DATA", "Tax expense", {"FY2025": -1616, "FY2024": -1202, "FY2023": -1849, "FY2022": -1300, "FY2021": -583, "FY2020": 137, "FY2019": -1241, "FY2018": -1497, "FY2017": -1602}),
    ("DATA", "Profit after tax from discontinued operations", {"FY2018": 1314, "FY2017": 796}),
    ("TOTAL", "Profit for the year", {"FY2025": 3856, "FY2024": 3486, "FY2023": 5207, "FY2022": 4794, "FY2021": 5202, "FY2020": 1466, "FY2019": 2233, "FY2018": 4746, "FY2017": 4229}),
    ("SECTION", "Other comprehensive income, net of tax (per-component figures shown net of tax throughout, matching "
               "the Statement of Changes in Equity - see that sheet for the same figures presented as a roll-forward)", {}),
    ("DATA", "Post-retirement defined benefit scheme remeasurements", {"FY2025": -385, "FY2024": -564, "FY2023": -1205, "FY2022": -2152, "FY2021": 1062, "FY2020": 113, "FY2019": -1117, "FY2018": 120}),
    ("DATA", "Movements in revaluation reserve (FVOCI debt/equity securities)", {"FY2025": 160, "FY2024": 73, "FY2023": 71, "FY2022": -32, "FY2021": 197, "FY2020": -36, "FY2019": -147, "FY2018": -260}),
    ("DATA", "Gains and losses attributable to own credit risk", {"FY2025": -91, "FY2024": -56, "FY2023": -168, "FY2022": 364, "FY2021": -52, "FY2020": -55, "FY2019": -306, "FY2018": 389}),
    ("DATA", "Movements in cash flow hedging reserve", {"FY2025": 1541, "FY2024": -14, "FY2023": 1614, "FY2022": -4717, "FY2021": -1958, "FY2020": -49, "FY2019": 446, "FY2018": -463}),
    ("DATA", "Movements in foreign currency translation reserve", {"FY2025": 70, "FY2024": -65, "FY2023": -33, "FY2022": 91, "FY2021": -19, "FY2020": 0, "FY2019": -2, "FY2018": 93}),
    ("DATA", "Share of other comprehensive income of associates and joint ventures", {"FY2018": 8}),
    ("TOTAL", "Total other comprehensive income/(loss), net of tax", {"FY2025": 1295, "FY2024": -626, "FY2023": 279, "FY2022": -6446, "FY2021": -770, "FY2020": -27, "FY2019": -1126, "FY2018": -113}),
    ("TOTAL", "Total comprehensive income/(loss) for the year", {"FY2025": 5151, "FY2024": 2860, "FY2023": 5486, "FY2022": -1652, "FY2021": 4432, "FY2020": 1439, "FY2019": 1107, "FY2018": 4633}),
]

bw.add_income_statement_sheet(
    title="Lloyds Bank plc — Profit & Loss",
    subtitle="Lloyds Bank plc Group consolidated basis. £m. OCI is shown throughout as each component's net-of-tax "
              "movement (matching the Statement of Changes in Equity's own presentation) rather than the "
              "Consolidated statement of comprehensive income's before-tax/current-tax/deferred-tax split (only "
              "disclosed in that finer form for FY2023-FY2025) - net-of-tax figures reconcile exactly to the "
              "Total OCI and Total comprehensive income rows for all years. FY2018 includes a 'Profit after tax "
              "from discontinued operations' row (£1,314m, from the May 2018 sale of the Scottish Widows Group "
              "to Lloyds Banking Group plc) not present in other years - 'Profit for the year' is Group profit "
              "including this discontinued-operations contribution. FY2020's 'Tax expense' row is a net tax "
              "credit of £137m, as originally disclosed.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=78,
    source_height=260,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - per-year reconciliation ladder confirmed:
# every year's own closing balance ties exactly to both the next year's own
# opening balance and that year's own Balance Sheet Total equity. Zero plug
# rows needed anywhere across all 5 years. Ladder's mandated scan of each
# year's equity note caught genuine "easy to skip" categories: distributions
# on other equity instruments, issuances/repurchases of AT1-type other
# equity instruments, capital contributions/returns, and NCI changes -
# each reproduced as its own row rather than folded into a generic "other".
# ---------------------------------------------------------------
equity_headers = ["Share capital", "Share premium", "Other reserves", "Retained profits",
                   "Ordinary shareholders' equity", "Other equity instruments",
                   "Non-controlling interests", "Total equity"]
equity_rows = [
    ("TOTAL", "At 31 December 2017 (pre-IFRS 9/IFRS 15 transition adjustment)", (1574, 600, 7706, 37718, 47598, 3217, 379, 51194)),
    ("DATA", "Adjustment on adoption of IFRS 9 and IFRS 15", (None, None, -222, -969, -1191, None, None, -1191)),
    ("TOTAL", "At 1 January 2018 (FY2018 opening)", (1574, 600, 7484, 36749, 46407, 3217, 379, 50003)),
    ("DATA", "Profit for the year", (None, None, None, 4711, 4711, None, 35, 4746)),
    ("DATA", "Post-retirement defined benefit scheme remeasurements, net of tax", (None, None, None, 120, 120, None, None, 120)),
    ("DATA", "Share of other comprehensive income of associates and joint ventures", (None, None, None, 8, 8, None, None, 8)),
    ("DATA", "Movements in revaluation reserve (FVOCI debt securities), net of tax", (None, None, -184, None, -184, None, None, -184)),
    ("DATA", "Movements in revaluation reserve (FVOCI equity shares), net of tax", (None, None, -76, None, -76, None, None, -76)),
    ("DATA", "Gains and losses attributable to own credit risk, net of tax", (None, None, None, 389, 389, None, None, 389)),
    ("DATA", "Movements in cash flow hedging reserve, net of tax", (None, None, -463, None, -463, None, None, -463)),
    ("DATA", "Currency translation differences, net of tax", (None, None, 93, None, 93, None, None, 93)),
    ("DATA", "Dividends", (None, None, None, -11022, -11022, None, -36, -11058)),
    ("DATA", "Distributions on other equity instruments, net of tax", (None, None, None, -201, -201, None, None, -201)),
    ("DATA", "Capital repayment to parent", (None, None, None, -2975, -2975, None, None, -2975)),
    ("DATA", "Capital contribution received", (None, None, None, 265, 265, None, None, 265)),
    ("DATA", "Return of capital contributions", (None, None, None, -9, -9, None, None, -9)),
    ("DATA", "Changes in non-controlling interests", (None, None, None, None, None, None, -305, -305)),
    ("DATA", "Realised gains/losses on equity shares held at FVOCI", (None, None, 111, -111, None, None, None, None)),
    ("TOTAL", "At 31 December 2018 (FY2018 closing)", (1574, 600, 6965, 27924, 37063, 3217, 73, 40353)),
    ("DATA", "Profit for the year", (None, None, None, 2193, 2193, None, 40, 2233)),
    ("DATA", "Post-retirement defined benefit scheme remeasurements, net of tax", (None, None, None, -1117, -1117, None, None, -1117)),
    ("DATA", "Movements in revaluation reserve (FVOCI debt securities), net of tax", (None, None, -159, None, -159, None, None, -159)),
    ("DATA", "Movements in revaluation reserve (FVOCI equity shares), net of tax", (None, None, 12, None, 12, None, None, 12)),
    ("DATA", "Gains and losses attributable to own credit risk, net of tax", (None, None, None, -306, -306, None, None, -306)),
    ("DATA", "Movements in cash flow hedging reserve, net of tax", (None, None, 446, None, 446, None, None, 446)),
    ("DATA", "Currency translation differences, net of tax", (None, None, -2, None, -2, None, None, -2)),
    ("DATA", "Dividends", (None, None, None, -4100, -4100, None, -38, -4138)),
    ("DATA", "Distributions on other equity instruments", (None, None, None, -281, -281, None, None, -281)),
    ("DATA", "Issue of other equity instruments", (None, None, None, None, None, 1648, None, 1648)),
    ("DATA", "Capital contribution received", (None, None, None, 229, 229, None, None, 229)),
    ("DATA", "Return of capital contributions", (None, None, None, -5, -5, None, None, -5)),
    ("DATA", "Changes in non-controlling interests", (None, None, None, None, None, None, -14, -14)),
    ("DATA", "Realised gains/losses on equity shares held at FVOCI", (None, None, -12, 12, None, None, None, None)),
    ("TOTAL", "At 31 December 2019 (FY2019 closing)", (1574, 600, 7250, 24549, 33973, 4865, 61, 38899)),
    ("DATA", "Profit for the year", (None, None, None, 1023, 1023, 417, 26, 1466)),
    ("DATA", "Post-retirement defined benefit scheme remeasurements, net of tax", (None, None, None, 113, 113, None, None, 113)),
    ("DATA", "Movements in revaluation reserve (FVOCI debt securities), net of tax", (None, None, -20, None, -20, None, None, -20)),
    ("DATA", "Movements in revaluation reserve (FVOCI equity shares), net of tax", (None, None, -16, None, -16, None, None, -16)),
    ("DATA", "Gains and losses attributable to own credit risk, net of tax", (None, None, None, -55, -55, None, None, -55)),
    ("DATA", "Movements in cash flow hedging reserve, net of tax", (None, None, -49, None, -49, None, None, -49)),
    ("DATA", "Dividends", (None, None, None, None, None, None, -7, -7)),
    ("DATA", "Distributions on other equity instruments", (None, None, None, None, None, -417, None, -417)),
    ("DATA", "Issue of other equity instruments", (None, None, None, None, None, 1070, None, 1070)),
    ("DATA", "Capital contributions received", (None, None, None, 140, 140, None, None, 140)),
    ("DATA", "Return of capital contributions", (None, None, None, -4, -4, None, None, -4)),
    ("DATA", "Changes in non-controlling interests", (None, None, None, None, None, None, -2, -2)),
    ("DATA", "Realised gains/losses on equity shares held at FVOCI", (None, None, 16, -16, None, None, None, None)),
    ("TOTAL", "At 1 January 2021 (FY2021 opening)", (1574, 600, 7181, 25750, 35105, 5935, 78, 41118)),
    ("DATA", "Profit for the year", (None, None, None, 4826, 4826, 344, 32, 5202)),
    ("DATA", "Post-retirement defined benefit scheme remeasurements, net of tax", (None, None, None, 1062, 1062, None, None, 1062)),
    ("DATA", "Movements in revaluation reserve (FVOCI debt/equity securities), net of tax", (None, None, 197, None, 197, None, None, 197)),
    ("DATA", "Gains and losses attributable to own credit risk, net of tax", (None, None, None, -52, -52, None, None, -52)),
    ("DATA", "Movements in cash flow hedging reserve, net of tax", (None, None, -1958, None, -1958, None, None, -1958)),
    ("DATA", "Movements in foreign currency translation reserve, net of tax", (None, None, -19, None, -19, None, None, -19)),
    ("DATA", "Dividends", (None, None, None, -2900, -2900, None, -14, -2914)),
    ("DATA", "Distributions on other equity instruments", (None, None, None, None, None, -344, None, -344)),
    ("DATA", "Issue of other equity instruments", (None, None, None, -1, -1, 1550, None, 1549)),
    ("DATA", "Repurchases and redemptions of other equity instruments", (None, None, None, -9, -9, -3217, None, -3226)),
    ("DATA", "Capital contributions received", (None, None, None, 164, 164, None, None, 164)),
    ("DATA", "Return of capital contributions", (None, None, None, -4, -4, None, None, -4)),
    ("DATA", "Changes in non-controlling interests", (None, None, None, -1, -1, None, -2, -3)),
    ("TOTAL", "At 31 December 2021 (FY2021 closing)", (1574, 600, 5400, 28836, 36410, 4268, 94, 40772)),
    ("DATA", "Profit for the year", (None, None, None, 4528, 4528, 241, 25, 4794)),
    ("DATA", "Post-retirement defined benefit scheme remeasurements, net of tax", (None, None, None, -2152, -2152, None, None, -2152)),
    ("DATA", "Movements in revaluation reserve (FVOCI debt/equity securities), net of tax", (None, None, -32, None, -32, None, None, -32)),
    ("DATA", "Gains and losses attributable to own credit risk, net of tax", (None, None, None, 364, 364, None, None, 364)),
    ("DATA", "Movements in cash flow hedging reserve, net of tax", (None, None, -4717, None, -4717, None, None, -4717)),
    ("DATA", "Movements in foreign currency translation reserve, net of tax", (None, None, 91, None, 91, None, None, 91)),
    ("DATA", "Dividends", (None, None, None, None, None, None, -37, -37)),
    ("DATA", "Distributions on other equity instruments", (None, None, None, None, None, -241, None, -241)),
    ("DATA", "Capital contributions received", (None, None, None, 221, 221, None, None, 221)),
    ("DATA", "Return of capital contributions", (None, None, None, -4, -4, None, None, -4)),
    ("DATA", "Realised gains/losses on equity shares held at FVOCI", (None, None, 1, -1, None, None, None, None)),
    ("TOTAL", "At 31 December 2022 (FY2022 closing)", (1574, 600, 743, 31792, 34709, 4268, 82, 39059)),
    ("DATA", "Profit for the year", (None, None, None, 4858, 4858, 334, 15, 5207)),
    ("DATA", "Post-retirement defined benefit scheme remeasurements, net of tax", (None, None, None, -1205, -1205, None, None, -1205)),
    ("DATA", "Movements in revaluation reserve (FVOCI debt/equity securities), net of tax", (None, None, 71, None, 71, None, None, 71)),
    ("DATA", "Gains and losses attributable to own credit risk, net of tax", (None, None, None, -168, -168, None, None, -168)),
    ("DATA", "Movements in cash flow hedging reserve, net of tax", (None, None, 1614, None, 1614, None, None, 1614)),
    ("DATA", "Movements in foreign currency translation reserve, net of tax", (None, None, -33, None, -33, None, None, -33)),
    ("DATA", "Dividends", (None, None, None, -4700, -4700, None, -39, -4739)),
    ("DATA", "Distributions on other equity instruments", (None, None, None, None, None, -334, None, -334)),
    ("DATA", "Issue of other equity instruments", (None, None, None, -5, -5, 750, None, 745)),
    ("DATA", "Capital contributions received", (None, None, None, 215, 215, None, None, 215)),
    ("DATA", "Return of capital contributions", (None, None, None, -1, -1, None, None, -1)),
    ("TOTAL", "At 31 December 2023 (FY2023 closing)", (1574, 600, 2395, 30786, 35355, 5018, 58, 40431)),
    ("DATA", "Profit for the year", (None, None, None, 3101, 3101, 363, 22, 3486)),
    ("DATA", "Post-retirement defined benefit scheme remeasurements, net of tax", (None, None, None, -564, -564, None, None, -564)),
    ("DATA", "Movements in revaluation reserve (FVOCI debt securities), net of tax", (None, None, 73, None, 73, None, None, 73)),
    ("DATA", "Gains and losses attributable to own credit risk, net of tax", (None, None, None, -56, -56, None, None, -56)),
    ("DATA", "Movements in cash flow hedging reserve, net of tax", (None, None, -14, None, -14, None, None, -14)),
    ("DATA", "Movements in foreign currency translation reserve, net of tax", (None, None, -65, None, -65, None, None, -65)),
    ("DATA", "Dividends", (None, None, None, -3990, -3990, None, None, -3990)),
    ("DATA", "Distributions on other equity instruments", (None, None, None, None, None, -363, None, -363)),
    ("DATA", "Issue of other equity instruments", (None, None, None, -6, -6, 1174, None, 1168)),
    ("DATA", "Repurchases and redemptions of other equity instruments", (None, None, None, None, None, -500, None, -500)),
    ("DATA", "Capital contributions received", (None, None, None, 142, 142, None, None, 142)),
    ("DATA", "Return of capital contributions", (None, None, None, -1, -1, None, None, -1)),
    ("TOTAL", "At 31 December 2024 (FY2024 closing)", (1574, 600, 2389, 29412, 33975, 5692, 80, 39747)),
    ("DATA", "Profit for the year", (None, None, None, 3425, 3425, 404, 27, 3856)),
    ("DATA", "Post-retirement defined benefit scheme remeasurements, net of tax", (None, None, None, -385, -385, None, None, -385)),
    ("DATA", "Movements in revaluation reserve (FVOCI debt securities), net of tax", (None, None, 160, None, 160, None, None, 160)),
    ("DATA", "Gains and losses attributable to own credit risk, net of tax", (None, None, None, -91, -91, None, None, -91)),
    ("DATA", "Movements in cash flow hedging reserve, net of tax", (None, None, 1541, None, 1541, None, None, 1541)),
    ("DATA", "Movements in foreign currency translation reserve, net of tax", (None, None, 70, None, 70, None, None, 70)),
    ("DATA", "Dividends", (None, None, None, -2390, -2390, None, -16, -2406)),
    ("DATA", "Distributions on other equity instruments", (None, None, None, None, None, -404, None, -404)),
    ("DATA", "Issue of other equity instruments", (None, None, None, -14, -14, 1514, None, 1500)),
    ("DATA", "Repurchases and redemptions of other equity instruments", (None, None, None, 81, 81, -1839, None, -1758)),
    ("DATA", "Capital contributions received", (None, None, None, 151, 151, None, None, 151)),
    ("DATA", "Return of capital contributions", (None, None, None, -1, -1, None, None, -1)),
    ("DATA", "Changes in non-controlling interests", (None, None, None, 20, 20, None, -20, None)),
    ("TOTAL", "At 31 December 2025 (FY2025 closing)", (1574, 600, 4160, 30208, 36542, 5367, 71, 41980)),
]

bw.add_equity_changes_sheet(
    title="Lloyds Bank plc — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, Lloyds Bank plc Group consolidated basis. £m. Equity "
              "reconciliation ladder confirmed: every year's own closing balance ties exactly to both the next "
              "year's own opening balance and that year's own Balance Sheet Total equity - zero plug rows needed "
              "anywhere across all years. The ladder starts at 31 December 2017 (as originally reported, before "
              "the FY2018 IFRS 9/IFRS 15 transition adjustment) so the FY2018 opening restatement is shown "
              "explicitly rather than absorbed into an unexplained gap. FY2018/FY2019 show a genuine "
              "presentational difference from FY2020 onward: distributions on AT1 'other equity instruments' "
              "reduce the Retained profits column directly (with the profit-for-the-year line crediting the full "
              "equity-holder profit, including the AT1 share, to Retained profits), whereas from FY2020 the "
              "AT1 profit share and its distributions are both routed through the Other equity instruments "
              "column - each year shown exactly as its own statement discloses it.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=64,
)

# ---------------------------------------------------------------
# Asset Quality - Group loans and advances to customers by IFRS 9 stage
# (portfolio-total level; per-product/segment tables are also disclosed
# each year but not reproduced here at that granularity).
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Group loans and advances to customers, by IFRS 9 stage", {}),
    ("DATA", "Stage 1", {"FY2025": 410428, "FY2024": 387517, "FY2023": 368859, "FY2022": 362766, "FY2021": 429078, "FY2020": 415608, "FY2019": 429767, "FY2018": 420968}),
    ("DATA", "Stage 2", {"FY2025": 42482, "FY2024": 44658, "FY2023": 52973, "FY2022": 60103, "FY2021": 34884, "FY2020": 51280, "FY2019": 28505, "FY2018": 25308}),
    ("DATA", "Stage 3", {"FY2025": 6519, "FY2024": 6708, "FY2023": 7131, "FY2022": 7611, "FY2021": 6406, "FY2020": 6443, "FY2019": 5647, "FY2018": 5397}),
    ("DATA", "Purchased or originated credit-impaired (POCI)", {"FY2025": 5076, "FY2024": 6207, "FY2023": 7854, "FY2022": 9622, "FY2021": 10977, "FY2020": 12511, "FY2019": 13714, "FY2018": 15391}),
    ("TOTAL", "Total gross lending", {"FY2025": 464505, "FY2024": 445090, "FY2023": 436817, "FY2022": 440102, "FY2021": 481345, "FY2020": 485842, "FY2019": 477633, "FY2018": 467064}),
    ("DATA", "ECL allowance on drawn balances", {"FY2025": -3001, "FY2024": -3183, "FY2023": -3693, "FY2022": -4475, "FY2021": -3804, "FY2020": -5701, "FY2019": -3163, "FY2018": -3020}),
    ("TOTAL", "Net balance sheet carrying value", {"FY2025": 461504, "FY2024": 441907, "FY2023": 433124, "FY2022": 435627, "FY2021": 477541, "FY2020": 480141, "FY2019": 474470, "FY2018": 464044}),
    ("DATA", "Total customer-related ECL allowance (drawn and undrawn)", {"FY2025": 3196, "FY2024": 3448, "FY2023": 4007, "FY2022": 4779}),
    ("DATA", "Stage 3 as % of total gross lending (NPL ratio)", {"FY2025": "1.4%", "FY2024": "1.5%", "FY2023": "1.6%", "FY2022": "1.7%", "FY2021": "1.3%", "FY2020": "1.3%", "FY2019": "1.2%", "FY2018": "1.2%"}),
    ("DATA", "Stage 2 as % of total gross lending", {"FY2025": "9.1%", "FY2024": "10.0%", "FY2023": "12.1%", "FY2022": "13.7%", "FY2021": "7.2%", "FY2020": "10.6%", "FY2019": "6.0%", "FY2018": "5.4%"}),
    ("DATA", "ECL allowance on drawn balances as % of total gross lending (coverage)",
     {"FY2025": "0.65%", "FY2024": "0.72%", "FY2023": "0.85%", "FY2022": "1.02%", "FY2021": "0.79%", "FY2020": "1.17%", "FY2019": "0.66%", "FY2018": "0.65%"}),
]

bw.add_cash_flow_sheet("Lloyds Bank plc — Cash Flow Statement", "Lloyds Bank plc Group consolidated basis, £m.", cash_rows, annual_sources("annual"), first_col_width=66, unit_suffix=" (£m)")

bw.add_asset_quality_sheet(
    title="Lloyds Bank plc — Asset Quality",
    subtitle="Group loans and advances to customers, IFRS 9 stage 1/2/3/POCI split, portfolio-total level. £m.",
    rows=asset_quality_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nFY2025/FY2024: Annual Report and Accounts 2025, 'Group loans and advances to customers' table, "
        "p.35-36. FY2023/FY2022: Annual Report and Accounts 2023, same table, p.41-42. FY2021: Annual Report and "
        "Accounts 2021, 'Loans and advances to customers and reverse repurchase agreements and expected credit "
        "loss allowance' table, p.35-36. FY2020: Annual Report and Accounts 2020, Note 16 'Financial assets at "
        f"amortised cost' (Loans and advances to customers, Group), p.130 - {AR_URLS['FY2020']}. FY2019: Annual "
        "Report and Accounts 2019, Note 16 'Financial assets at amortised cost' (Loans and advances to customers, "
        f"Group), p.80 - {AR_URLS['FY2019']}. FY2018: Annual Report and Accounts 2018, Note 16 'Financial assets "
        f"at amortised cost' (Loans and advances to customers, Group), p.59 - {AR_URLS['FY2018']}.\n\n"
        "DATA QUALITY FLAG: FY2021's own table combines 'loans and advances to customers' WITH reverse "
        "repurchase agreements into one Stage 1/2/3/POCI split (Total gross lending 481,345; Net balance sheet "
        "carrying value 477,541), unlike FY2022-FY2025's tables which cover loans and advances to customers "
        "ALONE - a genuine structural difference in what each year's own table covers, not a transcription error. "
        "FY2021's Net balance sheet carrying value of 477,541 therefore does NOT tie to that year's Balance Sheet "
        "'Loans and advances to customers' line (430,829) the way FY2022-FY2025 do - each year's own figure is "
        "shown as originally disclosed rather than adjusted to force a tie. Per-product/segment stage splits "
        "(Retail/Commercial Banking) are also disclosed each year but not reproduced at that finer granularity "
        "here."
    ),
    first_col_width=82,
    source_height=340,
    unit_suffix=" (£m)",
)


ANNUAL = {
    "CET1 Capital": {"FY2025": 26468, "FY2024": 25610, "FY2023": 26220, "FY2022": 25926, "FY2021": 26904, "FY2020": 26567, "FY2019": 24637},
    "CET1 Ratio": {"FY2025": "13.6%", "FY2024": "13.7%", "FY2023": "14.4%", "FY2022": "14.8%", "FY2021": "16.7%", "FY2020": "15.5%", "FY2019": "14.3%"},
    "Tier 1 Capital": {"FY2025": 31835, "FY2024": 31305, "FY2023": 31238, "FY2022": 30194, "FY2021": 31853, "FY2020": 33862, "FY2019": 31542},
    "Tier 1 Ratio": {"FY2025": "16.4%", "FY2024": "16.7%", "FY2023": "17.1%", "FY2022": "17.3%", "FY2021": "19.7%", "FY2020": "19.8%", "FY2019": "18.3%"},
    "Total Capital": {"FY2025": 38995, "FY2024": 37214, "FY2023": 37402, "FY2022": 35815, "FY2021": 37909, "FY2020": 40163, "FY2019": 37976},
    "Total Capital Ratio": {"FY2025": "20.1%", "FY2024": "19.9%", "FY2023": "20.5%", "FY2022": "20.5%", "FY2021": "23.5%", "FY2020": "23.5%", "FY2019": "22.1%"},
    "Total RWAs": {"FY2025": 194300, "FY2024": 186996, "FY2023": 182560, "FY2022": 174902, "FY2021": 161576, "FY2020": 170862, "FY2019": 171940},
    "Leverage Ratio": {"FY2025": "5.2%", "FY2024": "5.4%", "FY2023": "5.6%", "FY2022": "5.4%", "FY2021": "5.3%", "FY2020": "5.5%", "FY2019": "5.1%"},
    "LCR": {"FY2025": "135%", "FY2024": "137%", "FY2023": "133%", "FY2022": "136%", "FY2021": "126%", "FY2020": "126%", "FY2019": "127%"},
    "NSFR": {"FY2025": "119%", "FY2024": "124%", "FY2023": "126%"},
}
# ---------------------------------------------------------------
# KM1 Key Metrics (wayfinder/km1/map.md) - Lloyds Bank plc Group's own
# published key-metrics template, reproduced whole. add_km1_sheet() is
# called BEFORE the first add_metric_sheet() below so the sheet lands
# immediately after Asset Quality and immediately before CET1 Capital:
# sheet order follows call order.
#
# TWO CAPTION BLOCKS, NEVER MERGED (map rule 24). The Group's series crosses
# 1 January 2022 and the table changes identity at that date:
#   FY2022-FY2025  the UK template, "KM1: Key metrics", rows numbered
#                  1-20 with UK 7a-7d, UK 10a, UK 11a and UK 14a-14e.
#   FY2019-FY2021  the older Basel/IFRS9-FL table, "KM1: Key metrics and a
#                  comparison of own funds and capital and leverage ratios
#                  with and without the application of transitional
#                  arrangements for IFRS 9 (IFRS9-FL)".
# The row NUMBERS are reused for different metrics across that break and a
# row number alone never identifies a row - in the older table plain "9" is
# the CET1 ratio and plain "13" the total capital ratio, whereas in the UK
# template "9" is the countercyclical buffer and "13" the leverage exposure
# measure. The two blocks are therefore kept apart, each with the caption
# its own editions printed, and nothing is carried across.
# ---------------------------------------------------------------
km1_rows = [
    ("SECTION", "UK template — 'KM1: Key metrics' (FY2022 onward; row numbers and LR2 cross-references as printed)", {}),
    ("DATA", "1    Common Equity Tier 1 (CET1) capital (£m)",
     {"FY2025": 26468, "FY2024": 25610, "FY2023": 26220, "FY2022": 25926}),
    ("DATA", "2    Tier 1 capital (£m)",
     {"FY2025": 31835, "FY2024": 31305, "FY2023": 31238, "FY2022": 30194}),
    ("DATA", "3    Total capital (£m)",
     {"FY2025": 38995, "FY2024": 37214, "FY2023": 37402, "FY2022": 35815}),
    ("SECTION", "Risk-weighted exposure amounts", {}),
    ("DATA", "4    Total risk-weighted exposure amount (£m)",
     {"FY2025": 194300, "FY2024": 186996, "FY2023": 182560, "FY2022": 174902}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "5    Common Equity Tier 1 ratio (%)",
     {"FY2025": "13.6%", "FY2024": "13.7%", "FY2023": "14.4%", "FY2022": "14.8%"}),
    ("DATA", "6    Tier 1 ratio (%)",
     {"FY2025": "16.4%", "FY2024": "16.7%", "FY2023": "17.1%", "FY2022": "17.3%"}),
    ("DATA", "7    Total capital ratio (%)",
     {"FY2025": "20.1%", "FY2024": "19.9%", "FY2023": "20.5%", "FY2022": "20.5%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "UK 7a    Additional CET1 SREP requirements (%)",
     {"FY2025": "1.6%", "FY2024": "1.7%", "FY2023": "1.7%", "FY2022": "1.7%"}),
    ("DATA", "UK 7b    Additional AT1 SREP requirements (%)",
     {"FY2025": "0.6%", "FY2024": "0.6%", "FY2023": "0.6%", "FY2022": "0.6%"}),
    ("DATA", "UK 7c    Additional T2 SREP requirements (%)",
     {"FY2025": "0.8%", "FY2024": "0.7%", "FY2023": "0.7%", "FY2022": "0.7%"}),
    ("DATA", "UK 7d    Total SREP own funds requirements (%)",
     {"FY2025": "10.9%", "FY2024": "11.0%", "FY2023": "11.0%", "FY2022": "11.0%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "8    Capital conservation buffer (%)",
     {"FY2025": "2.5%", "FY2024": "2.5%", "FY2023": "2.500%", "FY2022": "2.500%"}),
    ("DATA", "9    Institution specific countercyclical capital buffer (%)",
     {"FY2025": "1.9%", "FY2024": "1.9%", "FY2023": "1.905%", "FY2022": "0.934%"}),
    ("DATA", "UK 10a    Other Systemically Important Institution buffer (%)",
     {"FY2025": "2.0%", "FY2024": "2.0%", "FY2023": "2.000%", "FY2022": "2.000%"}),
    ("DATA", "11    Combined buffer requirement (%)",
     {"FY2025": "6.4%", "FY2024": "6.4%", "FY2023": "6.405%", "FY2022": "5.434%"}),
    ("DATA", "UK 11a    Overall capital requirements (%)",
     {"FY2025": "17.3%", "FY2024": "17.4%", "FY2023": "17.4%", "FY2022": "16.5%"}),
    ("DATA", "12    CET1 available after meeting minimum SREP own funds requirements (%)",
     {"FY2025": "7.5%", "FY2024": "7.5%", "FY2023": "8.2%", "FY2022": "8.6%"}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "13  (LR2 UK-24b)    Total exposure measure excluding claims on central banks (£m)",
     {"FY2025": 612730, "FY2024": 582332, "FY2023": 562153, "FY2022": 559585}),
    ("DATA", "14  (LR2 25)    Leverage ratio excluding claims on central banks (%)",
     {"FY2025": "5.2%", "FY2024": "5.4%", "FY2023": "5.6%", "FY2022": "5.4%"}),
    ("SECTION", "Additional leverage ratio disclosure requirements", {}),
    ("DATA", "UK 14a  (LR2 UK-25a)    Fully loaded ECL accounting model leverage ratio excluding claims on central banks (%)",
     {"FY2025": "5.2%", "FY2024": "5.4%", "FY2023": "5.5%", "FY2022": "5.3%"}),
    ("DATA", "UK 14b  (LR2 UK-25c)    Leverage ratio including claims on central banks (%)",
     {"FY2025": "4.9%", "FY2024": "5.0%", "FY2023": "5.0%", "FY2022": "4.8%"}),
    ("DATA", "UK 14c  (LR2 UK-34)    Average leverage ratio excluding claims on central banks (%)",
     {"FY2025": "5.1%", "FY2024": "5.3%", "FY2023": "5.5%", "FY2022": "5.4%"}),
    ("DATA", "UK 14d  (LR2 UK-33)    Average leverage ratio including claims on central banks (%)",
     {"FY2025": "4.8%", "FY2024": "4.9%", "FY2023": "5.0%", "FY2022": "4.8%"}),
    ("DATA", "(LR2 UK-31)    Average total exposure measure including claims on central banks (£m)",
     {"FY2025": 661217, "FY2024": 638358}),
    ("DATA", "(LR2 UK-32)    Average total exposure measure excluding claims on central banks (£m)",
     {"FY2025": 620362, "FY2024": 597279}),
    ("DATA", "(LR2 27)    Leverage ratio buffer (%)", {"FY2025": "1.4%", "FY2024": "1.4%"}),
    ("DATA", "(LR2 UK-27a)    Of which: G-SII or O-SII additional leverage ratio buffer (%)",
     {"FY2025": "0.7%", "FY2024": "0.7%"}),
    ("DATA", "UK 14e  (LR2 UK-27b)    Of which: countercyclical leverage ratio buffer (%)",
     {"FY2025": "0.7%", "FY2024": "0.7%", "FY2023": "0.7%", "FY2022": "0.3%"}),
    ("SECTION", "Average Liquidity Coverage Ratio (weighted) (LCR)", {}),
    ("DATA", "15    Total high-quality liquid assets (HQLA) (Weighted value - average) (£m)",
     {"FY2025": 104542, "FY2024": 107531, "FY2023": 108655, "FY2022": 120822}),
    ("DATA", "UK 16a    Cash outflows - Total weighted value - average (£m)",
     {"FY2025": 83177, "FY2024": 84399, "FY2023": 87371, "FY2022": 92932}),
    ("DATA", "UK 16b    Cash inflows - Total weighted value - average (£m)",
     {"FY2025": 5744, "FY2024": 5738, "FY2023": 5687, "FY2022": 4067}),
    ("DATA", "16    Total net cash outflows (adjusted value - average) (£m)",
     {"FY2025": 77433, "FY2024": 78661, "FY2023": 81684, "FY2022": 88865}),
    ("DATA", "17    Average liquidity coverage ratio (%)",
     {"FY2025": "135%", "FY2024": "137%", "FY2023": "133%", "FY2022": "136%"}),
    ("SECTION", "Average Net Stable Funding Ratio", {}),
    ("DATA", "18    Total available stable funding (Weighted value - average) (£m)",
     {"FY2025": 478176, "FY2024": 481973, "FY2023": 483745}),
    ("DATA", "19    Total required stable funding (Weighted value - average) (£m)",
     {"FY2025": 400607, "FY2024": 390213, "FY2023": 387305}),
    ("DATA", "20    Average NSFR ratio (%)",
     {"FY2025": "119%", "FY2024": "124%", "FY2023": "125%"}),

    ("SECTION", "Pre-2022 Basel template — 'KM1: Key metrics and a comparison of own funds and capital and "
                "leverage ratios with and without the application of transitional arrangements for IFRS 9 "
                "(IFRS9-FL)' (FY2019-FY2021). DIFFERENT TABLE, DIFFERENT ROW NUMBERING — see note", {}),
    ("DATA", "1    Common Equity Tier 1 (CET1) (£m)  [pre-2022 table]",
     {"FY2021": 26904, "FY2020": 26567, "FY2019": 24637}),
    ("DATA", "2    CET1 capital as if IFRS 9 transitional arrangements had not been applied (£m)  [pre-2022 table]",
     {"FY2021": 26253, "FY2020": 24591, "FY2019": 24185}),
    ("DATA", "3    Tier 1 (£m)  [pre-2022 table]", {"FY2021": 31853, "FY2020": 33862, "FY2019": 31542}),
    ("DATA", "4    Tier 1 capital as if IFRS 9 transitional arrangements had not been applied (£m)  [pre-2022 table]",
     {"FY2021": 31202, "FY2020": 31886, "FY2019": 31090}),
    ("DATA", "5    Total capital (£m)  [pre-2022 table]", {"FY2021": 37909, "FY2020": 40163, "FY2019": 37976}),
    ("DATA", "6    Total capital as if IFRS 9 transitional arrangements had not been applied (£m)  [pre-2022 table]",
     {"FY2021": 38039, "FY2020": 39422, "FY2019": 38004}),
    ("DATA", "7    Total risk-weighted assets (£m)  [pre-2022 table]",
     {"FY2021": 161576, "FY2020": 170862, "FY2019": 171940}),
    ("DATA", "8    Total risk-weighted assets as if IFRS 9 transitional arrangements had not been applied (£m)  [pre-2022 table]",
     {"FY2021": 161805, "FY2020": 171015, "FY2019": 172324}),
    ("DATA", "9    Common Equity Tier 1 ratio (%)  [pre-2022 table]",
     {"FY2021": "16.7%", "FY2020": "15.5%", "FY2019": "14.3%"}),
    ("DATA", "10    CET1 ratio as if IFRS 9 transitional arrangements had not been applied (%)  [pre-2022 table]",
     {"FY2021": "16.2%", "FY2020": "14.4%", "FY2019": "14.0%"}),
    ("DATA", "11    Tier 1 ratio (%)  [pre-2022 table]",
     {"FY2021": "19.7%", "FY2020": "19.8%", "FY2019": "18.3%"}),
    ("DATA", "12    Tier 1 ratio as if IFRS 9 transitional arrangements had not been applied (%)  [pre-2022 table]",
     {"FY2021": "19.3%", "FY2020": "18.6%", "FY2019": "18.0%"}),
    ("DATA", "13    Total capital ratio (%)  [pre-2022 table]",
     {"FY2021": "23.5%", "FY2020": "23.5%", "FY2019": "22.1%"}),
    ("DATA", "14    Total capital ratio as if IFRS 9 transitional arrangements had not been applied (%)  [pre-2022 table]",
     {"FY2021": "23.5%", "FY2020": "23.1%", "FY2019": "22.1%"}),
    ("SECTION", "Additional CET1 buffer requirements as a percentage of RWA (pre-2022 table; printed unnumbered)", {}),
    ("DATA", "Capital conservation buffer requirement (%)  [pre-2022 table]",
     {"FY2021": "2.500%", "FY2020": "2.5%", "FY2019": "2.5%"}),
    ("DATA", "Countercyclical buffer requirement (%)  [pre-2022 table]",
     {"FY2021": "0.003%", "FY2020": "0.0%", "FY2019": "0.9%"}),
    ("DATA", "Bank G-SIB and/or D-SIB additional requirements (%)  [pre-2022 table]",
     {"FY2021": "2.000%", "FY2020": "2.0%", "FY2019": "2.0%"}),
    ("DATA", "Total of bank CET1 specific buffer requirements (%)  [pre-2022 table]",
     {"FY2021": "4.503%", "FY2020": "4.5%", "FY2019": "5.4%"}),
    ("DATA", "CET1 available after meeting the bank's minimum capital requirements (%)  [pre-2022 table]",
     {"FY2021": "12.2%", "FY2020": "11.0%", "FY2019": "9.8%"}),
    ("SECTION", "UK leverage ratio (pre-2022 table — ORIGINAL CRR basis, INCLUDING claims on central banks)", {}),
    ("DATA", "15    UK leverage ratio exposure measure (£m)  [pre-2022 table]",
     {"FY2021": 584650, "FY2020": 593546, "FY2019": 582921}),
    ("DATA", "16    UK leverage ratio (%)  [pre-2022 table]",
     {"FY2021": "5.3%", "FY2020": "5.5%", "FY2019": "5.1%"}),
    ("DATA", "17    UK leverage ratio as if IFRS 9 transitional arrangements had not been applied (%)  [pre-2022 table]",
     {"FY2021": "5.2%", "FY2020": "5.2%", "FY2019": "5.0%"}),
    ("SECTION", "Average Liquidity Coverage Ratio (weighted) (LCR) (pre-2022 table; printed unnumbered)", {}),
    ("DATA", "Total High Quality Liquid Assets (HQLA) (£m)  [pre-2022 table]",
     {"FY2021": 114712, "FY2020": 113434, "FY2019": 112203}),
    ("DATA", "Total net cash outflow (£m)  [pre-2022 table]",
     {"FY2021": 91296, "FY2020": 89844, "FY2019": 88490}),
    ("DATA", "LCR ratio (%)  [pre-2022 table]",
     {"FY2021": "126%", "FY2020": "126%", "FY2019": "127%"}),
]

KM1_SOURCES = (
    "Sources - Lloyds Bank plc's own year-end Pillar 3 disclosures, key-metrics template, £m and % exactly as "
    "printed. EACH YEAR IS TAKEN FROM THE EDITION IN WHICH IT IS THE REPORTING YEAR (the '31 Dec' column, or "
    "the 'T'/'Q4' column in the pre-2022 editions), never from a later edition's comparative. Page numbers are "
    "the PRINTED FOLIOS from each document's own 'Page N of M' footer, each cross-confirmed against that "
    "document's own contents/List of Tables entry:\n"
    f"FY2025: 2025 Year-End Pillar 3 Disclosures, 'KM1: Key metrics', printed pp.6-7 (the table breaks across "
    f"two pages, capital and leverage on p.6, LCR and NSFR on p.7) - {P3_URLS['FY2025']}\n"
    f"FY2024: 2024 Year-End Pillar 3 Disclosures, printed pp.8-9 - {P3_URLS['FY2024']}\n"
    f"FY2023: 2023 Year-End Pillar 3 Disclosures, printed p.8 (whole table on one page) - {P3_URLS['FY2023']}\n"
    f"FY2022: 2022 Year-End Pillar 3 Disclosures, printed p.9 - {P3_URLS['FY2022']}\n"
    f"FY2021: 2021 Year-End Pillar 3 Disclosures, printed p.5 - {P3_URLS['FY2021']}\n"
    f"FY2020: 2020 Year-End Pillar 3 Disclosures, 'Table 1: Key metrics (KM1)...', printed p.3 - "
    f"{P3_URLS['FY2020']}\n"
    f"FY2019: Capital and Risk Management Pillar 3 Report 2019, 'Table 1: Key Metrics (KM1)...', printed p.3 - "
    f"{P3_URLS['FY2019']}\n"
    "FY2018 and FY2017: blank. No standalone Lloyds Bank plc Pillar 3 disclosure exists for those years - "
    "full Pillar 3 reporting for this entity began with the FY2019 year-end, following 1 January 2019 "
    "ring-fencing implementation. The blank is the absence of a document, not a row we failed to find.\n\n"
    "ENTITY - THE ONE THING MOST EASILY GOT WRONG IN THIS FAMILY. Every figure above is Lloyds Bank plc GROUP "
    "consolidated. Lloyds Banking Group plc, Lloyds Bank plc and Bank of Scotland plc are three different "
    "entities that each publish their own Pillar 3 document, in the same folder structure on the same website, "
    "with near-identical filenames and near-plausible figures. Each document states its own scope in its first "
    "sentence, and this workbook's editions all read: 'This document presents the consolidated Pillar 3 "
    "disclosures of Lloyds Bank plc (the Group) as at 31 December [year].' No figure from the parent or from "
    "the sibling is substituted anywhere on this sheet.\n\n"
    "LEVEL OF APPLICATION, read from the documents' own 'Introduction and basis of preparation' section rather "
    "than inferred from the group structure. Lloyds Bank plc discloses in its own right, under the Disclosure "
    "(CRR) Part of the PRA Rulebook, and its editions say so affirmatively. The same section also disposes of "
    "the sibling entity in one sentence - 'Additional disclosures surrounding the capital resources, leverage "
    "exposures and capital requirements of Bank of Scotland plc will be published separately in conjunction "
    "with the Annual Report and Accounts for this subsidiary' - so Bank of Scotland's figures are not in this "
    "document and this document's figures are not Bank of Scotland's. Capital instrument main-features and "
    "TLAC2 disclosures are the one thing deliberately pushed up to Lloyds Banking Group plc's own Pillar 3, "
    "and neither is a KM1 row.\n\n"
    "TWO TEMPLATES, KEPT APART (map rule 24 - a dated, corpus-wide break, and not the same thing as the "
    "leverage-basis break below). The Group's FY2019, FY2020 and FY2021 editions print the older Basel "
    "IFRS9-FL table; the FY2022 edition onward prints the UK KM1 template. THE ROW NUMBERS ARE REUSED FOR "
    "DIFFERENT METRICS ACROSS THAT BREAK, so the two are shown as two separate caption blocks above and "
    "nothing is merged into a single series. Worked examples of how badly a row number alone would mislead "
    "here: in the pre-2022 table row 9 is the CET1 RATIO and row 13 the TOTAL CAPITAL RATIO, while in the UK "
    "template row 9 is the countercyclical buffer and row 13 the leverage exposure measure; the pre-2022 "
    "table's rows 15-17 are the UK leverage block, while the UK template's rows 15-17 are the LCR block. "
    "Every pre-2022 row above is also suffixed '[pre-2022 table]' so a row can never be read out of its "
    "block.\n\n"
    "THE PRE-2022 TABLE IS A DIFFERENT DISCLOSURE, NOT A SPARSER ONE. Half its rows are the IFRS 9 "
    "fully-loaded twins ('as if IFRS 9 transitional arrangements had not been applied'), which the UK template "
    "does not carry at all - the Group publishes those separately as IFRS 9-FL from FY2022 onward, and that "
    "separate table is not reproduced on this sheet. Conversely the pre-2022 table has no SREP block "
    "(UK 7a-7d), no O-SII buffer row, and no NSFR rows of any kind.\n\n"
    "THE 1 JANUARY 2022 LEVERAGE BASIS BREAK (map rule 5) falls exactly on the same boundary and is stated by "
    "the Group itself. The pre-2022 block's rows 15/16 are captioned 'UK leverage ratio exposure measure' and "
    "'UK leverage ratio' on the ORIGINAL CRR basis, INCLUDING claims on central banks; from FY2022 rows 13/14 "
    "are captioned 'Total exposure measure EXCLUDING claims on central banks' and 'Leverage ratio EXCLUDING "
    "claims on central banks'. The two are not comparable and are never merged. The pre-2022 editions also "
    "footnote a third figure, the CRD IV leverage ratio, at 4.9% for 31 December 2021, 5.1% for 2020 and 4.8% "
    "for 2019 - a different basis again, recorded here rather than placed in a row the Group did not print.\n\n"
    "ROW SETS DRIFT BETWEEN EDITIONS, and every blank in the UK block is a row that edition did not print:\n"
    "• NSFR (rows 18-20) is absent from the FY2022 edition entirely - its KM1 ends at row 17. The UK NSFR "
    "framework took effect during 2022 and the Group's first KM1 NSFR rows appear in the FY2023 edition. "
    "FY2022 is therefore blank on rows 18-20, not zero.\n"
    "• The four leverage rows carrying only an LR2 reference and no KM1 number (UK-31, UK-32, 27 and UK-27a) "
    "appear inside KM1 only from the FY2024 edition. In the FY2023 edition the same figures are printed in "
    "that edition's footnotes and in its standalone LR2 table instead, and for the record they are: average "
    "total exposure measure for 1 October to 31 December 2023 of £627,191m including and £568,917m excluding "
    "claims on central banks, a total leverage ratio buffer of 1.4% (31 December 2022: 1.0%) and an additional "
    "leverage ratio buffer of 0.7%. They are recorded here rather than written into KM1 rows that edition did "
    "not have.\n"
    "• The Group prints both a 'KM1 Ref' and an 'LR2 Ref' column from the FY2023 edition onward, because the "
    "table embeds extracts of LR2 that must be disclosed quarterly. Both references are kept in the row labels "
    "above.\n\n"
    "CAPTION DRIFT ALONG ROW UK 14e. The FY2024 and FY2025 editions caption it 'Of which: countercyclical "
    "leverage ratio buffer (%)'; the FY2022 and FY2023 editions caption the same row 'Countercyclical leverage "
    "ratio buffer (%)', without the 'Of which'. The newer wording is used for the row label.\n\n"
    "PRECISION DRIFT ALONG ROWS 8, 9, UK 10a AND 11. The FY2022 and FY2023 editions print these to three "
    "decimals ('2.500%', '0.934%', '1.905%', '6.405%'); the FY2024 and FY2025 editions print one ('2.5%', "
    "'1.9%', '6.4%'). Each cell comes from its own year's edition, so the printed precision genuinely varies "
    "along the row. This also means FY2023's countercyclical buffer reads 1.905% here where the FY2024 "
    "edition's comparative rounds it to 1.9%.\n\n"
    "AN UNRESOLVED DISAGREEMENT WITH THIS WORKBOOK'S OWN NSFR FIGURES, RECORDED RATHER THAN RECONCILED, AND "
    "NOT SILENTLY CORRECTED. Row 20 above gives FY2023's average NSFR as 125%. That is what Lloyds Bank plc's "
    "FY2023 year-end Pillar 3 prints for 31 December 2023, in TWO independent places in that document - KM1 "
    "row 20, and row 34 of the LIQ2 net stable funding ratio template - and the FY2024 edition's comparative "
    "column for the same date prints 125% as well. This workbook's separate NSFR metric sheet carries 126% "
    "for FY2023, and its Interim Pillar 3 sheet carries 127% for 2023-Q1, 127% for 2023-H1, 126% for 2023-Q3 "
    "and 126% for 2024-Q1.\n"
    "THOSE FIGURES COULD NOT BE SOURCED TO ANY DOCUMENT, and the search for them was exhaustive rather than "
    "cursory (all checked 2026-09-17, every document fetched directly and verified by HTTP status, "
    "Content-Type and %PDF magic bytes):\n"
    "• Lloyds Bank plc's own 2023 editions print, each in its own reporting-date column, Q1 124%, H1 124%, "
    "Q3 125% and year-end 125%. None of them prints 126% or 127% for any 2023 date, in any column.\n"
    "• The string '126%' does not occur anywhere in the FY2023 year-end Pillar 3 document. The only "
    "three-digit percentages of that magnitude anywhere in it are 115%, 116%, 119%, 124% and 125%.\n"
    "• The Lloyds Bank plc Annual Report and Accounts 2023 states no NSFR figure at all - it names the ratio "
    "once, in narrative, without a number. Its one '127 per cent' is a different measure entirely (internal "
    "liquidity stress-testing resources against modelled outflows) and its one '125 per cent' is a pension "
    "asset-liability hedging ratio.\n"
    "• The obvious remaining explanation - that a parent figure had been substituted for the subsidiary's, "
    "which is the classic failure mode in this three-entity family - was TESTED AND DISPROVED. Lloyds "
    "Banking Group plc's own FY2023 Pillar 3 prints an average NSFR of 130% at 31 December 2023 and its "
    "Q1 2023 edition prints 129%. So 126% and 127% are not the parent's figures either; they match neither "
    "entity.\n"
    "WHAT HAS BEEN DONE ABOUT IT: nothing, deliberately, beyond this record. The KM1 row above is transcribed "
    "as printed at 125%. The 126%/127% figures on the NSFR and Interim Pillar 3 sheets have been left exactly "
    "as they stood - not deleted, not overwritten with the KM1 figure, and not back-solved - because removing "
    "or amending an unexplained figure destroys the evidence that it was ever there, and the correct next "
    "step is for someone to identify its true source. Note that FY2024 and FY2025 do NOT have this problem: "
    "the NSFR sheet's 124% and 119% agree exactly with rows 20 above and with the 2025 and 2026 editions' "
    "comparatives, as do the 2025 interim observations (123%/122%/121%). The anomaly is confined to the four "
    "2023 and 2024-Q1 NSFR cells named above.\n\n"
    "DASHES. The Group states its own convention in the basis of preparation: 'Where relevant, de minimis "
    "monetary amounts (<£0.5 million) are rounded down for reporting purposes and disclosed as a dash in the "
    "table.' So a dash in these documents means a rounded-down small amount rather than an inapplicable "
    "requirement. No such dash falls in the rows above.\n\n"
    "FREE SECOND OPINION FROM THE INTERIM EDITIONS. Lloyds Bank plc publishes quarterly and half-year Pillar 3 "
    "disclosures (this workbook carries them on its Interim Pillar 3 sheet), and each reproduces the four "
    "preceding quarter-ends as comparatives. The 2026 half-year edition's '31 Dec 2025' comparative column "
    "confirms this sheet's whole FY2025 column independently - CET1 26,468, Tier 1 31,835, Total capital "
    "38,995, RWAs 194,300, CET1 ratio 13.6%, Tier 1 ratio 16.4%, total capital ratio 20.1% - at no "
    "transcription cost.\n\n"
    "LATEST-EDITION CHECK (required by the KM1 map), performed 2026-09-17 against the bank's OWN website "
    "rather than our cited URLs. The Lloyds Banking Group plc Financial Downloads page "
    "(lloydsbankinggroup.com/investors/financial-downloads) loads normally with an ordinary browser "
    "User-Agent and lists 20 Lloyds Bank plc Pillar 3 PDFs, from 2021 Q1 through 2026 H1. The newest YEAR-END "
    "edition is the 2025 one, which is this workbook's most recent year - the FY2026 year-end edition is not "
    "due until early 2027. Two editions newer than any year-end document do exist and are interim, not "
    "annual: 2026 Q1 (31 March 2026) and 2026 H1 (30 June 2026). They are half-year and quarterly positions, "
    "not financial years, so they add no column to a workbook of financial years; the 2026 H1 edition was "
    "nonetheless downloaded and used above as a check on FY2025. NO NEWER FULL-YEAR EDITION EXISTS; this "
    "workbook is not an edition behind.\n\n"
    "FETCH PROVENANCE, recorded because this exact website once produced a false 'not published' statement in "
    "a sibling workbook in this project (Bank of Scotland plc, whose script asserted that no standalone "
    "Pillar 3 document is published for that entity, on the strength of a Cloudflare block). All seven "
    "year-end documents cited above, plus the 2026 half-year edition, were downloaded directly on 2026-09-17 "
    "and each was verified by HTTP status 200, Content-Type application/pdf AND the %PDF magic bytes. No "
    "reader-proxy or text-extraction service stands between these figures and the PDFs.\n\n"
    + ENTITY_NOTE
)

bw.add_km1_sheet(
    title="Lloyds Bank plc — KM1 Key Metrics",
    subtitle="Lloyds Bank plc GROUP consolidated basis — not Lloyds Banking Group plc and not Bank of Scotland "
             "plc, each of which publishes its own separate Pillar 3 document. The Group's own published "
             "key-metrics template, from its year-end Pillar 3 disclosures, reproduced in its row order with "
             "its own row numbers, LR2 cross-references and printed precision. Amounts in £m, ratios as "
             "printed. Each year comes from its own edition, never a later comparative. TWO CAPTION BLOCKS: "
             "the UK KM1 template for FY2022-FY2025, and the older Basel IFRS9-FL key-metrics table for "
             "FY2019-FY2021, which reuses the same row numbers for different metrics and is never merged with "
             "it. FY2018 and FY2017 are blank: no Pillar 3 document exists for this entity before FY2019.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=104,
    source_height=560,
)

for name, values in ANNUAL.items():
    unit = "%" if "Ratio" in name or name in {"LCR", "NSFR"} else "£m"
    row = [(name, dict(values))]
    note = "Figures are Group consolidated. NSFR was not separately disclosed in the reviewed FY2019-FY2022 year-end KM1 extracts (the UK NSFR framework took effect from 2022; comparative disclosure was limited)." if name == "NSFR" else None
    bw.add_metric_sheet(name, unit, row, annual_sources("p3"), note=note, first_col_width=58)
    if name == "Total RWAs":
        # RWA Breakdown - Pillar 3 OV1 template, placed right after Total RWAs
        # per the locked sheet order. All years tie exactly to the Total
        # RWAs figure above. FY2021's own template uses "RIRB" (retail IRB)
        # in place of FY2022-FY2025's "slotting approach"/"AIRB" sub-split -
        # a genuine methodology change at the sub-category level shown here
        # only at the top-level risk-type categories, which are consistent
        # across all years with a Pillar 3 disclosure.
        rwa_breakdown_rows = [
            ("DATA", "Credit risk (excluding CCR)", {"FY2025": 158922, "FY2024": 151614, "FY2023": 147061, "FY2022": 144602, "FY2021": 129643, "FY2020": 137461, "FY2019": 138990}),
            ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 1386, "FY2024": 1363, "FY2023": 1329, "FY2022": 1115, "FY2021": 1464, "FY2020": 2488, "FY2019": 2102}),
            ("DATA", "Securitisation exposures in the non-trading/banking book (after the cap)", {"FY2025": 7777, "FY2024": 7648, "FY2023": 8246, "FY2022": 5899, "FY2021": 5373, "FY2020": 5116, "FY2019": 4497}),
            ("DATA", "Position, foreign exchange and commodities risks (Market risk)", {"FY2025": 177, "FY2024": 292, "FY2023": 319, "FY2022": 82, "FY2021": 203, "FY2020": 210, "FY2019": 171}),
            ("DATA", "Operational risk", {"FY2025": 26038, "FY2024": 26079, "FY2023": 25605, "FY2022": 23204, "FY2021": 22575, "FY2020": 23307, "FY2019": 24413}),
            ("DATA", "Memo: Amounts below the thresholds for deduction (subject to 250% risk weight)", {"FY2025": 747, "FY2024": 1211, "FY2023": 1424, "FY2022": 1864, "FY2021": 2318, "FY2020": 2280, "FY2019": 1767}),
            ("TOTAL", "Total", {"FY2025": 194300, "FY2024": 186996, "FY2023": 182560, "FY2022": 174902, "FY2021": 161576, "FY2020": 170862, "FY2019": 171940}),
        ]
        bw.add_rwa_breakdown_sheet(
            title="Lloyds Bank plc — RWA Breakdown",
            subtitle="Lloyds Bank plc Group consolidated basis, Pillar 3 OV1 template (top-level risk-type "
                     "categories). £m.",
            rows=rwa_breakdown_rows,
            sources_text=annual_sources("p3"),
            first_col_width=78,
            source_height=200,
            unit_suffix=" (£m)",
        )
# GA-020 (2026-09-19): outcome wording, evidence in the MREL note below.
GA020_MREL = {y: ("Not published – LB plc Pillar 3 " + y + " states only that internal MREL resources exceed the "
                  "minimum (material subsidiary of LBG plc) plus TLAC 2 ranking; no ratio. ARs likewise")
              for y in ("FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019")}
for _y in ("FY2018", "FY2017"):
    GA020_MREL[_y] = ("Not published – zero 'MREL' in the Lloyds Bank plc " + _y + " Annual Report (searched "
                      "2026-09-19); no Lloyds Bank plc Pillar 3 exists before FY2019")
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    annual_sources("p3"),
    per_note={"MREL Ratio": "A numeric MREL ratio for Lloyds Bank plc Group was not disclosed in the reviewed Lloyds Bank plc year-end reports; parent-level or instrument data is not substituted. "
              "GA-020 RE-CHECK 2026-09-19: every P3_URLS edition (FY2019-FY2025) and AR_URLS/AR2017_URL annual report (FY2017-FY2025) was full-text searched. "
              "From FY2019 the Pillar 3 carries an MREL section stating only that Lloyds Bank plc is a material subsidiary of the resolution entity Lloyds Banking Group plc "
              "and that its internal MREL resources exceeded the minimum required (e.g. FY2025 year-end Pillar 3, p.15), plus the TLAC 2 creditor-ranking template (amounts, not a ratio). "
              "No MREL ratio appears in any edition. The FY2017 and FY2018 annual reports contain zero occurrences of 'MREL', and no Lloyds Bank plc Pillar 3 exists before FY2019."},
    statements={"MREL Ratio": GA020_MREL},
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
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 631335, "FY2024": 611213, "FY2023": 605405, "FY2022": 616928, "FY2021": 602849, "FY2020": 599939, "FY2019": 581368, "FY2018": 593486, "FY2017": 823030}),
        ("Loans and advances to customers", {"FY2025": 461504, "FY2024": 441907, "FY2023": 433124, "FY2022": 435627, "FY2021": 430829, "FY2020": 480141, "FY2019": 474470, "FY2018": 464044, "FY2017": 465555}),
        ("Customer deposits", {"FY2025": 465207, "FY2024": 451794, "FY2023": 441953, "FY2022": 446172, "FY2021": 449373, "FY2020": 434569, "FY2019": 396839, "FY2018": 391251}),
        ("Total equity", {"FY2025": 41980, "FY2024": 39747, "FY2023": 40431, "FY2022": 39059, "FY2021": 40772, "FY2020": 41118, "FY2019": 38899, "FY2018": 40353}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total income", {"FY2025": 18429, "FY2024": 17071, "FY2023": 18367, "FY2022": 16745, "FY2021": 14673, "FY2020": 14585, "FY2019": 16608, "FY2018": 16974, "FY2017": 17352}),
        ("Operating expenses", {"FY2025": -12165, "FY2024": -11927, "FY2023": -10968, "FY2022": -9199, "FY2021": -10206, "FY2020": -9196, "FY2019": -11772, "FY2018": -11119, "FY2017": -11630}),
        ("Profit for the year", {"FY2025": 3856, "FY2024": 3486, "FY2023": 5207, "FY2022": 4794, "FY2021": 5202, "FY2020": 1466, "FY2019": 2233, "FY2018": 4746, "FY2017": 4229}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 39747, "FY2024": 40431, "FY2023": 39059, "FY2022": 40772, "FY2021": 41118, "FY2020": 38899, "FY2019": 40353, "FY2018": 50003}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": 5151, "FY2024": 2860, "FY2023": 5486, "FY2022": -1652, "FY2021": 4432, "FY2020": 1439, "FY2019": 1107, "FY2018": 4633}),
        ("Other equity movements, net", {"FY2025": -2918, "FY2024": -3544, "FY2023": -4114, "FY2022": -61, "FY2021": -4778, "FY2020": 780, "FY2019": -2561, "FY2018": -14283}),
        ("Closing equity", {"FY2025": 41980, "FY2024": 39747, "FY2023": 40431, "FY2022": 39059, "FY2021": 40772, "FY2020": 41118, "FY2019": 38899, "FY2018": 40353}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 2186, "FY2024": -7249, "FY2023": 4115, "FY2022": 19310, "FY2021": 17693, "FY2020": 15182, "FY2019": 11634, "FY2018": -23948}),
        ("Net cash from/(used in) investing activities", {"FY2025": -9635, "FY2024": -7203, "FY2023": -9290, "FY2022": 255, "FY2021": -2828, "FY2020": -4066, "FY2019": -2448, "FY2018": 20944}),
        ("Net cash from/(used in) financing activities", {"FY2025": -1807, "FY2024": -2251, "FY2023": -3444, "FY2022": -406, "FY2021": -10526, "FY2020": -765, "FY2019": -10292, "FY2018": -18258}),
        ("Cash and cash equivalents at end of year", {"FY2025": 40599, "FY2024": 49712, "FY2023": 66538, "FY2022": 75201, "FY2021": 55960, "FY2020": 48966, "FY2019": 38614, "FY2018": 39723}),
    ], cash_flow_unit="£m",
    ratios=[("CET1 Ratio", dict(ANNUAL["CET1 Ratio"])), ("Tier 1 Ratio", dict(ANNUAL["Tier 1 Ratio"])), ("Total Capital Ratio", dict(ANNUAL["Total Capital Ratio"])), ("Leverage Ratio", dict(ANNUAL["Leverage Ratio"])), ("LCR", dict(ANNUAL["LCR"]))],
    note="Annual figures are consolidated Lloyds Bank plc Group metrics; interim observations are on the Interim Pillar 3 sheet. FY2018 Pillar 3 ratios are blank (no standalone Pillar 3 disclosure; full reporting began FY2019).")

# FY2017 now lives in the balance_sheet / pl_rows / Overview dicts above, like
# every other year, so it flows through the normal citation plumbing. It was
# previously bolted on here by writing straight into bw.wb[...] after the
# sheets were built - a pattern that skips the citation helper and, in two
# other scripts in this corpus, concealed a wrong figure for exactly that
# reason. Its label lookup also collapsed duplicate row captions onto the last
# match, so a value could silently land in the wrong section. Do not
# reintroduce it. All FY2017 figures below were re-verified 2026-09-16 against
# the Lloyds Bank plc Annual Report 2017 and were correct as they stood; the
# P&L column was completed at the same time and now ties
# (17,352 - 11,630 - 687 = 5,035; 5,035 - 1,602 = 3,433; 3,433 + 796 = 4,229).

bw.save("/Users/armaan/code/katalysis/banks/LLOYDS BANK FINANCIALS.xlsx")
