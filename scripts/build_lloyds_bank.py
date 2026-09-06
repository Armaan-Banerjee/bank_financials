import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2017"]
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
AR2017_URL = "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-plc/2017/2017-lb-annual-report-v2.pdf"

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
    lines = [f"{y}: Lloyds Bank plc {label}, p.{pages[y]} — {urls[y]}" for y in YEARS if y in pages and y in urls]
    if kind == "annual":
        lines.append(f"FY2017: Lloyds Bank plc Annual Report and Accounts 2017, pp.21-27 — {AR2017_URL}")
    else:
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
    f"roll-forward - {AR_URLS['FY2021']} and {AR_URLS['FY2023']}\n\n"
    + ENTITY_NOTE
)

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
# ---------------------------------------------------------------
# Balance Sheet - equity reconciliation ladder step 1: built first so each
# year's own Total equity is the independent check value for the equity
# sheet below. All 5 years tie exactly to the equity statement's own
# opening/closing balances.
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 37720, "FY2024": 42396, "FY2023": 57909, "FY2022": 72005, "FY2021": 54279}),
    ("DATA", "Items in the course of collection from banks", {"FY2021": 147}),
    ("DATA", "Financial assets at fair value through profit or loss", {"FY2025": 2279, "FY2024": 2321, "FY2023": 1862, "FY2022": 1371, "FY2021": 1798}),
    ("DATA", "Derivative financial instruments", {"FY2025": 3260, "FY2024": 4235, "FY2023": 3165, "FY2022": 3857, "FY2021": 5511}),
    ("DATA", "Loans and advances to banks", {"FY2025": 5836, "FY2024": 6433, "FY2023": 8810, "FY2022": 8363, "FY2021": 4478}),
    ("DATA", "Loans and advances to customers", {"FY2025": 461504, "FY2024": 441907, "FY2023": 433124, "FY2022": 435627, "FY2021": 430829}),
    ("DATA", "Reverse repurchase agreements", {"FY2025": 43962, "FY2024": 44143, "FY2023": 32751, "FY2022": 39259, "FY2021": 49708}),
    ("DATA", "Debt securities (at amortised cost)", {"FY2025": 11983, "FY2024": 11854, "FY2023": 12546, "FY2022": 7331, "FY2021": 4562}),
    ("DATA", "Due from fellow Lloyds Banking Group undertakings", {"FY2025": 1182, "FY2024": 560, "FY2023": 840, "FY2022": 816, "FY2021": 739}),
    ("TOTAL", "Financial assets at amortised cost", {"FY2025": 524467, "FY2024": 504897, "FY2023": 488071, "FY2022": 491396, "FY2021": 490316}),
    ("DATA", "Financial assets at fair value through other comprehensive income", {"FY2025": 36257, "FY2024": 30344, "FY2023": 27337, "FY2022": 22846, "FY2021": 27786}),
    ("DATA", "Goodwill and other intangible assets", {"FY2025": 5692, "FY2024": 5804, "FY2023": 5837, "FY2022": 5124, "FY2021": 4614}),
    ("DATA", "Current tax recoverable", {"FY2025": 1263, "FY2024": 338, "FY2023": 1026, "FY2022": 527, "FY2021": 220}),
    ("DATA", "Deferred tax assets", {"FY2025": 3917, "FY2024": 4785, "FY2023": 4636, "FY2022": 5857, "FY2021": 4048}),
    ("DATA", "Retirement benefit assets", {"FY2025": 2695, "FY2024": 3028, "FY2023": 3624, "FY2022": 3823, "FY2021": 4531}),
    ("DATA", "Other assets", {"FY2025": 13785, "FY2024": 13065, "FY2023": 11938, "FY2022": 10122, "FY2021": 9599}),
    ("TOTAL", "Total assets", {"FY2025": 631335, "FY2024": 611213, "FY2023": 605405, "FY2022": 616928, "FY2021": 602849}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks", {"FY2025": 3085, "FY2024": 3144, "FY2023": 3557, "FY2022": 4658, "FY2021": 3363}),
    ("DATA", "Customer deposits", {"FY2025": 465207, "FY2024": 451794, "FY2023": 441953, "FY2022": 446172, "FY2021": 449373}),
    ("DATA", "Repurchase agreements (at amortised cost)", {"FY2025": 37567, "FY2024": 37760, "FY2023": 37702, "FY2022": 48590, "FY2021": 30106}),
    ("DATA", "Due to fellow Lloyds Banking Group undertakings", {"FY2025": 3852, "FY2024": 4049, "FY2023": 2932, "FY2022": 2539, "FY2021": 1490}),
    ("DATA", "Items in course of transmission to banks", {"FY2021": 308}),
    ("DATA", "Financial liabilities at fair value through profit or loss", {"FY2025": 4243, "FY2024": 4630, "FY2023": 5255, "FY2022": 5159, "FY2021": 6537}),
    ("DATA", "Derivative financial instruments (liability)", {"FY2025": 4286, "FY2024": 5787, "FY2023": 4307, "FY2022": 5891, "FY2021": 4643}),
    ("DATA", "Notes in circulation", {"FY2025": 2118, "FY2024": 2121, "FY2023": 1392, "FY2022": 1280, "FY2021": 1321}),
    ("DATA", "Debt securities in issue at amortised cost", {"FY2025": 52132, "FY2024": 45281, "FY2023": 52449, "FY2022": 49056, "FY2021": 48724}),
    ("DATA", "Other liabilities", {"FY2025": 5772, "FY2024": 7211, "FY2023": 6260, "FY2022": 6003, "FY2021": 5391}),
    ("DATA", "Retirement benefit obligations", {"FY2025": 120, "FY2024": 122, "FY2023": 136, "FY2022": 126, "FY2021": 230}),
    ("DATA", "Current tax liabilities", {"FY2025": 35, "FY2024": 33, "FY2023": 23, "FY2022": 3}),
    ("DATA", "Deferred tax liabilities", {"FY2025": 146, "FY2024": 125, "FY2023": 157, "FY2022": 208}),
    ("DATA", "Provisions", {"FY2025": 2772, "FY2024": 2198, "FY2023": 1916, "FY2022": 1591, "FY2021": 1933}),
    ("DATA", "Subordinated liabilities", {"FY2025": 8020, "FY2024": 7211, "FY2023": 6935, "FY2022": 6593, "FY2021": 8658}),
    ("TOTAL", "Total liabilities", {"FY2025": 589355, "FY2024": 571466, "FY2023": 564974, "FY2022": 577869, "FY2021": 562077}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 1574, "FY2024": 1574, "FY2023": 1574, "FY2022": 1574, "FY2021": 1574}),
    ("DATA", "Share premium account", {"FY2025": 600, "FY2024": 600, "FY2023": 600, "FY2022": 600, "FY2021": 600}),
    ("DATA", "Other reserves", {"FY2025": 4160, "FY2024": 2389, "FY2023": 2395, "FY2022": 743, "FY2021": 5400}),
    ("DATA", "Retained profits", {"FY2025": 30208, "FY2024": 29412, "FY2023": 30786, "FY2022": 31792, "FY2021": 28836}),
    ("TOTAL", "Ordinary shareholders' equity", {"FY2025": 36542, "FY2024": 33975, "FY2023": 35355, "FY2022": 34709, "FY2021": 36410}),
    ("DATA", "Other equity instruments", {"FY2025": 5367, "FY2024": 5692, "FY2023": 5018, "FY2022": 4268, "FY2021": 4268}),
    ("TOTAL", "Total equity excluding non-controlling interests", {"FY2025": 41909, "FY2024": 39667, "FY2023": 40373, "FY2022": 38977, "FY2021": 40678}),
    ("DATA", "Non-controlling interests", {"FY2025": 71, "FY2024": 80, "FY2023": 58, "FY2022": 82, "FY2021": 94}),
    ("TOTAL", "Total equity", {"FY2025": 41980, "FY2024": 39747, "FY2023": 40431, "FY2022": 39059, "FY2021": 40772}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 631335, "FY2024": 611213, "FY2023": 605405, "FY2022": 616928, "FY2021": 602849}),
]

bw.add_balance_sheet_sheet(
    title="Lloyds Bank plc — Balance Sheet",
    subtitle="Lloyds Bank plc Group consolidated basis. £m. FY2021 shows two genuine structural differences from "
              "later years: a standalone 'Items in the course of collection from banks' asset line and 'Items in "
              "course of transmission to banks' liability line (both since folded into Other assets/Other "
              "liabilities), and Goodwill/Other intangible assets reported as two separate lines rather than the "
              "combined 'Goodwill and other intangible assets' line used FY2022 onward (FY2021's combined figure "
              "of 4,614 = 470 goodwill + 4,144 other intangibles, summed here for comparability).",
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
    ("DATA", "Interest income", {"FY2025": 28208, "FY2024": 28386, "FY2023": 25300, "FY2022": 16562, "FY2021": 12920}),
    ("DATA", "Interest expense", {"FY2025": -14845, "FY2024": -15794, "FY2023": -11591, "FY2022": -3457, "FY2021": -1884}),
    ("TOTAL", "Net interest income", {"FY2025": 13363, "FY2024": 12592, "FY2023": 13709, "FY2022": 13105, "FY2021": 11036}),
    ("DATA", "Fee and commission income", {"FY2025": 2515, "FY2024": 2416, "FY2023": 2456, "FY2022": 2352, "FY2021": 2195}),
    ("DATA", "Fee and commission expense", {"FY2025": -1254, "FY2024": -1478, "FY2023": -1104, "FY2022": -1101, "FY2021": -942}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 1261, "FY2024": 938, "FY2023": 1352, "FY2022": 1251, "FY2021": 1253}),
    ("DATA", "Net trading income", {"FY2025": 523, "FY2024": 597, "FY2023": 384, "FY2022": 180, "FY2021": 385}),
    ("DATA", "Other operating income", {"FY2025": 3282, "FY2024": 2944, "FY2023": 2922, "FY2022": 2209, "FY2021": 1999}),
    ("TOTAL", "Other income", {"FY2025": 5066, "FY2024": 4479, "FY2023": 4658, "FY2022": 3640, "FY2021": 3637}),
    ("TOTAL", "Total income", {"FY2025": 18429, "FY2024": 17071, "FY2023": 18367, "FY2022": 16745, "FY2021": 14673}),
    ("DATA", "Operating expenses", {"FY2025": -12165, "FY2024": -11927, "FY2023": -10968, "FY2022": -9199, "FY2021": -10206}),
    ("DATA", "Impairment (charge)/credit", {"FY2025": -792, "FY2024": -456, "FY2023": -343, "FY2022": -1452, "FY2021": 1318}),
    ("TOTAL", "Profit before tax", {"FY2025": 5472, "FY2024": 4688, "FY2023": 7056, "FY2022": 6094, "FY2021": 5785}),
    ("DATA", "Tax expense", {"FY2025": -1616, "FY2024": -1202, "FY2023": -1849, "FY2022": -1300, "FY2021": -583}),
    ("TOTAL", "Profit for the year", {"FY2025": 3856, "FY2024": 3486, "FY2023": 5207, "FY2022": 4794, "FY2021": 5202}),
    ("SECTION", "Other comprehensive income, net of tax (per-component figures shown net of tax throughout, matching "
               "the Statement of Changes in Equity - see that sheet for the same figures presented as a roll-forward)", {}),
    ("DATA", "Post-retirement defined benefit scheme remeasurements", {"FY2025": -385, "FY2024": -564, "FY2023": -1205, "FY2022": -2152, "FY2021": 1062}),
    ("DATA", "Movements in revaluation reserve (FVOCI debt/equity securities)", {"FY2025": 160, "FY2024": 73, "FY2023": 71, "FY2022": -32, "FY2021": 197}),
    ("DATA", "Gains and losses attributable to own credit risk", {"FY2025": -91, "FY2024": -56, "FY2023": -168, "FY2022": 364, "FY2021": -52}),
    ("DATA", "Movements in cash flow hedging reserve", {"FY2025": 1541, "FY2024": -14, "FY2023": 1614, "FY2022": -4717, "FY2021": -1958}),
    ("DATA", "Movements in foreign currency translation reserve", {"FY2025": 70, "FY2024": -65, "FY2023": -33, "FY2022": 91, "FY2021": -19}),
    ("TOTAL", "Total other comprehensive income/(loss), net of tax", {"FY2025": 1295, "FY2024": -626, "FY2023": 279, "FY2022": -6446, "FY2021": -770}),
    ("TOTAL", "Total comprehensive income/(loss) for the year", {"FY2025": 5151, "FY2024": 2860, "FY2023": 5486, "FY2022": -1652, "FY2021": 4432}),
]

bw.add_income_statement_sheet(
    title="Lloyds Bank plc — Profit & Loss",
    subtitle="Lloyds Bank plc Group consolidated basis. £m. OCI is shown throughout as each component's net-of-tax "
              "movement (matching the Statement of Changes in Equity's own presentation) rather than the "
              "Consolidated statement of comprehensive income's before-tax/current-tax/deferred-tax split (only "
              "disclosed in that finer form for FY2023-FY2025) - net-of-tax figures reconcile exactly to the "
              "Total OCI and Total comprehensive income rows for all 5 years.",
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
              "anywhere across all 5 years.",
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
    ("DATA", "Stage 1", {"FY2025": 410428, "FY2024": 387517, "FY2023": 368859, "FY2022": 362766, "FY2021": 429078}),
    ("DATA", "Stage 2", {"FY2025": 42482, "FY2024": 44658, "FY2023": 52973, "FY2022": 60103, "FY2021": 34884}),
    ("DATA", "Stage 3", {"FY2025": 6519, "FY2024": 6708, "FY2023": 7131, "FY2022": 7611, "FY2021": 6406}),
    ("DATA", "Purchased or originated credit-impaired (POCI)", {"FY2025": 5076, "FY2024": 6207, "FY2023": 7854, "FY2022": 9622, "FY2021": 10977}),
    ("TOTAL", "Total gross lending", {"FY2025": 464505, "FY2024": 445090, "FY2023": 436817, "FY2022": 440102, "FY2021": 481345}),
    ("DATA", "ECL allowance on drawn balances", {"FY2025": -3001, "FY2024": -3183, "FY2023": -3693, "FY2022": -4475, "FY2021": -3804}),
    ("TOTAL", "Net balance sheet carrying value", {"FY2025": 461504, "FY2024": 441907, "FY2023": 433124, "FY2022": 435627, "FY2021": 477541}),
    ("DATA", "Total customer-related ECL allowance (drawn and undrawn)", {"FY2025": 3196, "FY2024": 3448, "FY2023": 4007, "FY2022": 4779}),
    ("DATA", "Stage 3 as % of total gross lending (NPL ratio)", {"FY2025": "1.4%", "FY2024": "1.5%", "FY2023": "1.6%", "FY2022": "1.7%", "FY2021": "1.3%"}),
    ("DATA", "Stage 2 as % of total gross lending", {"FY2025": "9.1%", "FY2024": "10.0%", "FY2023": "12.1%", "FY2022": "13.7%", "FY2021": "7.2%"}),
    ("DATA", "ECL allowance on drawn balances as % of total gross lending (coverage)",
     {"FY2025": "0.65%", "FY2024": "0.72%", "FY2023": "0.85%", "FY2022": "1.02%", "FY2021": "0.79%"}),
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
        "loss allowance' table, p.35-36.\n\n"
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
    if name == "Total RWAs":
        # RWA Breakdown - Pillar 3 OV1 template, placed right after Total RWAs
        # per the locked sheet order. All 5 years tie exactly to the Total
        # RWAs figure above. FY2021's own template uses "RIRB" (retail IRB)
        # in place of FY2022-FY2025's "slotting approach"/"AIRB" sub-split -
        # a genuine methodology change at the sub-category level shown here
        # only at the top-level risk-type categories, which are consistent
        # across all 5 years.
        rwa_breakdown_rows = [
            ("DATA", "Credit risk (excluding CCR)", {"FY2025": 158922, "FY2024": 151614, "FY2023": 147061, "FY2022": 144602, "FY2021": 129643}),
            ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 1386, "FY2024": 1363, "FY2023": 1329, "FY2022": 1115, "FY2021": 1464}),
            ("DATA", "Securitisation exposures in the non-trading/banking book (after the cap)", {"FY2025": 7777, "FY2024": 7648, "FY2023": 8246, "FY2022": 5899, "FY2021": 5373}),
            ("DATA", "Position, foreign exchange and commodities risks (Market risk)", {"FY2025": 177, "FY2024": 292, "FY2023": 319, "FY2022": 82, "FY2021": 203}),
            ("DATA", "Operational risk", {"FY2025": 26038, "FY2024": 26079, "FY2023": 25605, "FY2022": 23204, "FY2021": 22575}),
            ("DATA", "Memo: Amounts below the thresholds for deduction (subject to 250% risk weight)", {"FY2025": 747, "FY2024": 1211, "FY2023": 1424, "FY2022": 1864, "FY2021": 2318}),
            ("TOTAL", "Total", {"FY2025": 194300, "FY2024": 186996, "FY2023": 182560, "FY2022": 174902, "FY2021": 161576}),
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
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 631335, "FY2024": 611213, "FY2023": 605405, "FY2022": 616928, "FY2021": 602849}),
        ("Loans and advances to customers", {"FY2025": 461504, "FY2024": 441907, "FY2023": 433124, "FY2022": 435627, "FY2021": 430829}),
        ("Customer deposits", {"FY2025": 465207, "FY2024": 451794, "FY2023": 441953, "FY2022": 446172, "FY2021": 449373}),
        ("Total equity", {"FY2025": 41980, "FY2024": 39747, "FY2023": 40431, "FY2022": 39059, "FY2021": 40772}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total income", {"FY2025": 18429, "FY2024": 17071, "FY2023": 18367, "FY2022": 16745, "FY2021": 14673}),
        ("Operating expenses", {"FY2025": -12165, "FY2024": -11927, "FY2023": -10968, "FY2022": -9199, "FY2021": -10206}),
        ("Profit for the year", {"FY2025": 3856, "FY2024": 3486, "FY2023": 5207, "FY2022": 4794, "FY2021": 5202}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 39747, "FY2024": 40431, "FY2023": 39059, "FY2022": 40772, "FY2021": 41118}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": 5151, "FY2024": 2860, "FY2023": 5486, "FY2022": -1652, "FY2021": 4432}),
        ("Other equity movements, net", {"FY2025": -2918, "FY2024": -3544, "FY2023": -4114, "FY2022": -61, "FY2021": -4778}),
        ("Closing equity", {"FY2025": 41980, "FY2024": 39747, "FY2023": 40431, "FY2022": 39059, "FY2021": 40772}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 2186, "FY2024": -7249, "FY2023": 4115, "FY2022": 19310, "FY2021": 17693}),
        ("Net cash from/(used in) investing activities", {"FY2025": -9635, "FY2024": -7203, "FY2023": -9290, "FY2022": 255, "FY2021": -2828}),
        ("Net cash from/(used in) financing activities", {"FY2025": -1807, "FY2024": -2251, "FY2023": -3444, "FY2022": -406, "FY2021": -10526}),
        ("Cash and cash equivalents at end of year", {"FY2025": 40599, "FY2024": 49712, "FY2023": 66538, "FY2022": 75201, "FY2021": 55960}),
    ], cash_flow_unit="£m",
    ratios=[("CET1 Ratio", {y: v for y, v in zip(YEARS, ANNUAL["CET1 Ratio"])}), ("Tier 1 Ratio", {y: v for y, v in zip(YEARS, ANNUAL["Tier 1 Ratio"])}), ("Total Capital Ratio", {y: v for y, v in zip(YEARS, ANNUAL["Total Capital Ratio"])}), ("Leverage Ratio", {y: v for y, v in zip(YEARS, ANNUAL["Leverage Ratio"])}), ("LCR", {y: v for y, v in zip(YEARS, ANNUAL["LCR"])})],
    note="Annual figures are consolidated Lloyds Bank plc Group metrics; interim observations are on the Interim Pillar 3 sheet.")

# FY2017 extension from Lloyds Bank plc Annual Report 2017 (official report,
# pp.21-27), £m. The report predates the current Pillar 3 series; absent
# historical regulatory metrics remain blank.
_fy17 = {
    "Balance Sheet": {"Cash and balances at central banks": 58521,
                      "Loans and advances to customers": 465555,
                      "Total assets": 823030},
    "Profit & Loss": {"Total income": 17352, "Profit before tax": 5035},
}
for _sheet, _values in _fy17.items():
    _ws = bw.wb[_sheet]
    _labels = {str(_ws.cell(r, 1).value).strip(): r for r in range(4, _ws.max_row + 1)}
    _col = 1 + YEARS.index("FY2017") + 1
    for _label, _value in _values.items():
        if _label in _labels:
            _ws.cell(_labels[_label], _col, _value)

bw.save("/Users/armaan/code/katalysis/banks/LLOYDS BANK FINANCIALS.xlsx")
