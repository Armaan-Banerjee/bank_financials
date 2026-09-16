import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018"]

AR_URLS = {
    "FY2025": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2025/q4/2025-lbcm-annual-report.pdf",
    "FY2024": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2024/q4/2024-lbcm-annual-report.pdf",
    "FY2023": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2023/q4/2023-lbcm-annual-report.pdf",
    "FY2022": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2022/q4/2022-lbcm-annual-report.pdf",
    "FY2021": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2021/2021-lbcm-annual-report.pdf",
    "FY2020": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2020/2020-lbcm-annual-report.pdf",
    "FY2019": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2019/2019-lbcm-annual-report.pdf",
    "FY2018": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2018/2018-lbcm-annual-report-v2.pdf",
}
P3_URLS = {
    "FY2025": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2025/q4/2025-lbcm-fy-pillar-3.pdf",
    "FY2024": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2024/q4/2024-lbcm-fy-pillar-3.pdf",
    "FY2023": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2023/q4/2023-lbcm-fy-pillar-3.pdf",
    "FY2022": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2022/q4/2022-lbcm-fy-pillar-3.pdf",
    "FY2021": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2021/2021-lbcm-fy-pillar3.pdf",
    "FY2020": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2020/2020-lbcm-fy-pillar-3.pdf",
    "FY2019": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2019/2019-lbcm-pillar-3-report-v2.xlsx",
    # FY2018: no standalone Pillar 3 report was ever published for LBCM - its first year of
    # trading. Capital/RWA disclosure for FY2018 lives instead in the Annual Report's own
    # Strategic Report (Table 1: Capital resources, Table 2: RWAs), on a Group basis.
    "FY2018": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2018/2018-lbcm-annual-report-v2.pdf",
}
CH_URL = "https://find-and-update.company-information.service.gov.uk/company/10399850"
# The live index every URL above was re-verified against on 2026-09-16. It
# Cloudflare-blocks (error 1007) a plain automated fetch and loads normally
# with an ordinary browser User-Agent - see the KM1 sheet's sourcing note and
# wayfinder/km1/tickets/KM1-032.md.
P3_INDEX_URL = "https://www.lloydsbankinggroup.com/investors/financial-downloads.html"

ENTITY_NOTE = (
    "Entity: Lloyds Bank Corporate Markets plc, company number 10399850, FRN 763256, "
    "LEI 213800MBWEIJDM5CU638. Companies House confirms the active bank company. "
    "This is the non-ring-fenced wholesale/markets entity created as part of Lloyds "
    "Banking Group's 2018 ring-fencing restructuring, DISTINCT from the ring-fenced "
    "Lloyds Bank plc (FRN 119278, built separately as 'LLOYDS BANK FINANCIALS.xlsx'). "
    "All figures below are the Bank (solo) column, not the Group consolidated column "
    "also shown in each source document.\n"
    "FLOOR NOTE: FY2018 is the entity's genuine floor, not FY2016. Companies House confirms "
    "incorporation on 28 September 2016 as a dormant shelf company ('25 Gresham Finance "
    "Limited', renamed Lloyds Bank Corporate Markets plc 21 April 2017), which did not trade "
    "in 2016 or 2017 - the Bank's own FY2018 Annual Report states explicitly 'No comparative "
    "information is presented as the Group did not trade in the prior period' and its own "
    "FY2017 balance sheet shows only £20m of share capital and £20m cash, nothing else. "
    "Substantive trading began only when LBCM went live as the non-ring-fenced bank of Lloyds "
    "Banking Group via a staggered business transfer between May and December 2018."
)


def annual_sources(kind):
    pages = {
        "annual": {"FY2025": 61, "FY2024": 68, "FY2023": 67, "FY2022": 63, "FY2021": 36,
                   "FY2020": 32, "FY2019": 30, "FY2018": 26},
        "p3": {"FY2025": 4, "FY2024": 4, "FY2023": 4, "FY2022": 5, "FY2021": 5,
               "FY2020": 5, "FY2019": "'Key Ratios'/'OV1' tabs", "FY2018": 4},
    }[kind]
    urls = AR_URLS if kind == "annual" else P3_URLS
    default_label = "Annual Report and Accounts, Cash flow statements (Bank column)" if kind == "annual" else "Year-End Pillar 3 disclosure, KM1 Key Metrics (Bank-level)"
    p3_label_override = {
        "FY2019": "Year-End Pillar 3 disclosure (xlsx), 'Key Ratios'/'OV1' tabs — KM1 Key Metrics, "
                  "disclosed on a Group/consolidated basis (own document labels the entity 'the Group', "
                  "unlike FY2020 onward's 'the Bank')",
        "FY2018": "Annual Report and Accounts, Strategic Report Table 1 (Capital resources)/Table 2 "
                  "(Risk-weighted assets) — Group basis; no standalone Pillar 3 report was published "
                  "for FY2018, LBCM's first year of trading",
    }
    lines = []
    for y in YEARS:
        label = p3_label_override.get(y, default_label) if kind == "p3" else default_label
        loc = pages[y]
        prefix = "p." if isinstance(loc, int) else ""
        lines.append(f"{y}: Lloyds Bank Corporate Markets plc {label}, {prefix}{loc} — {urls[y]}")
    return "\n".join(lines + [ENTITY_NOTE, f"Companies House — {CH_URL}"])


bw = BankWorkbook("Lloyds Bank Corporate Markets plc", YEARS, header_color="6A1B9A")

STATEMENTS_SOURCES = (
    "Sources - Lloyds Bank Corporate Markets plc Annual Report and Accounts, Bank (solo) column unless noted:\n"
    f"FY2025/FY2024: Annual Report and Accounts 2025, Consolidated income statement p.57, Statements of comprehensive "
    f"income p.57, Balance sheets p.58, Statements of changes in equity (Bank) p.60 - {AR_URLS['FY2025']}\n"
    f"FY2023/FY2022: Annual Report and Accounts 2023, Consolidated income statement p.63, Statements of comprehensive "
    f"income p.63, Balance sheets p.64, Statements of changes in equity (Bank) p.66 - {AR_URLS['FY2023']}\n"
    f"FY2021: Annual Report and Accounts 2021 (2020 comparative also shown that year), Consolidated income statement "
    f"p.30, Statements of comprehensive income p.31, Balance sheets p.32, Statements of changes in equity (Bank) p.34 "
    f"- {AR_URLS['FY2021']}\n"
    f"FY2020: Annual Report and Accounts 2020, Group consolidated income statement p.27, Statements of comprehensive "
    f"income p.28, Balance sheets p.29, Statements of changes in equity (Bank) p.30-31 - {AR_URLS['FY2020']}\n"
    f"FY2019: Annual Report and Accounts 2019, Group consolidated income statement p.22, Statements of comprehensive "
    f"income p.23, Balance sheets p.24, Statements of changes in equity (Bank) p.25-26 - {AR_URLS['FY2019']}\n"
    f"FY2018: Annual Report and Accounts 2018 (LBCM's first year of trading; no FY2017 comparative - the Bank did "
    f"not trade in 2017), Consolidated income statement p.18, Statements of comprehensive income p.19, Balance "
    f"sheets p.20, Statements of changes in equity (Bank) p.21-22, Cash flow statements p.23 - {AR_URLS['FY2018']}\n\n"
    + ENTITY_NOTE + "\n\n"
    "BASIS NOTE: Balance Sheet and Statement of Changes in Equity below use the Bank (solo) column, matching the "
    "entity note above. The Profit & Loss sheet is necessarily the Group consolidated income statement - LBCM's own "
    "reports present only one consolidated income statement (no separate Bank-solo income statement line items), with "
    "the Bank's own profit for the year and OCI given only as aggregate rows within the Statements of comprehensive "
    "income (e.g. FY2025: Bank profit for the year £495m vs Group £541m) - these aggregate Bank figures are shown on "
    "the P&L sheet's Total rows, not fabricated line-item detail."
)

cash_rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax", {"FY2025": 583, "FY2024": 468, "FY2023": 399, "FY2022": 436, "FY2021": 293, "FY2020": 3, "FY2019": 473, "FY2018": 135}),
    ("DATA", "Change in operating assets", {"FY2025": 863, "FY2024": -5920, "FY2023": -3331, "FY2022": -1657, "FY2021": 180, "FY2020": -5476, "FY2019": -1150, "FY2018": -18123}),
    ("DATA", "Change in operating liabilities", {"FY2025": -4782, "FY2024": 4619, "FY2023": 3614, "FY2022": -2881, "FY2021": -3502, "FY2020": 13574, "FY2019": -2329, "FY2018": 41916}),
    ("DATA", "Non-cash and other items", {"FY2025": 623, "FY2024": 282, "FY2023": 702, "FY2022": -296, "FY2021": -152, "FY2020": 111, "FY2019": -158, "FY2018": -5}),
    ("DATA", "Tax paid, net", {"FY2025": -87, "FY2024": -84, "FY2023": -96, "FY2022": -58, "FY2021": -38, "FY2020": -51, "FY2019": -72}),
    ("TOTAL", "Net cash provided by/(used in) operating activities", {"FY2025": -2800, "FY2024": -635, "FY2023": 1288, "FY2022": -4456, "FY2021": -3219, "FY2020": 8161, "FY2019": -3236, "FY2018": 23923}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of financial assets", {"FY2024": 0, "FY2023": -3, "FY2022": -27, "FY2021": -85}),
    ("DATA", "Proceeds from sale and maturity of financial assets", {"FY2024": 0, "FY2023": 10, "FY2022": 132, "FY2021": 138}),
    ("DATA", "Purchase of fixed assets", {"FY2025": -3, "FY2024": -2, "FY2023": -2, "FY2022": -5, "FY2021": -1, "FY2020": -20, "FY2019": -1, "FY2018": -8}),
    ("DATA", "Purchase of intangible assets", {"FY2025": 0, "FY2024": -4}),
    ("DATA", "Proceeds from sale of fixed assets", {"FY2025": 0, "FY2024": 1}),
    ("DATA", "Dividends received from subsidiaries", {"FY2022": 22, "FY2021": 44, "FY2020": 57, "FY2019": 811}),
    ("DATA", "Acquisition of businesses", {"FY2019": 6130, "FY2018": -13049}),
    ("TOTAL", "Net cash provided by/(used in) investing activities", {"FY2025": -3, "FY2024": -5, "FY2023": 5, "FY2022": 122, "FY2021": 96, "FY2020": 37, "FY2019": 6940, "FY2018": -13057}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividends paid to ordinary shareholders", {"FY2024": -450, "FY2022": -220, "FY2021": -200, "FY2020": -700}),
    ("DATA", "Distributions on other equity instruments", {"FY2025": -210, "FY2024": -78, "FY2023": -80, "FY2022": -43, "FY2021": -33, "FY2020": -40, "FY2019": -49, "FY2018": -18}),
    ("DATA", "Issue of ordinary shares", {"FY2022": 250, "FY2018": 100}),
    ("DATA", "Interest paid on subordinated liabilities", {"FY2025": -24, "FY2024": -54, "FY2023": -58, "FY2022": -25, "FY2021": -16, "FY2020": -23, "FY2019": -32}),
    ("DATA", "Finance leases", {"FY2025": -5, "FY2024": -4, "FY2023": -5, "FY2022": -8}),
    ("DATA", "Proceeds from issue of subordinated liabilities", {"FY2023": 299, "FY2018": 725}),
    ("DATA", "Repayment of subordinated liabilities", {"FY2025": -730, "FY2023": -284}),
    ("DATA", "Loss on repayment of other equity instruments", {"FY2023": -15}),
    ("DATA", "Proceeds from issue of other equity instruments", {"FY2025": 3637, "FY2023": 289, "FY2018": 782}),
    ("DATA", "Repurchases and redemptions of other equity instruments", {"FY2025": -296, "FY2023": -263}),
    ("DATA", "Receipt of capital contribution from parent company", {"FY2018": 2975}),
    ("TOTAL", "Net cash provided by/(used in) financing activities", {"FY2025": 2372, "FY2024": -586, "FY2023": -117, "FY2022": -46, "FY2021": -249, "FY2020": -763, "FY2019": -81, "FY2018": 4564}),
    ("DATA", "Effect of exchange rate changes on cash and cash equivalents", {"FY2025": -521, "FY2024": 116, "FY2023": -403, "FY2022": 693, "FY2021": 69, "FY2020": -167, "FY2019": 0, "FY2018": 0}),
    ("TOTAL", "Change in cash and cash equivalents", {"FY2025": -952, "FY2024": -1110, "FY2023": 773, "FY2022": -3687, "FY2021": -3303, "FY2020": 7268, "FY2019": 3623, "FY2018": 15430}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 20633, "FY2024": 21743, "FY2023": 19396, "FY2022": 23083, "FY2021": 26341, "FY2020": 19073, "FY2019": 15450, "FY2018": 20}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 19681, "FY2024": 20633, "FY2023": 20169, "FY2022": 19396, "FY2021": 23038, "FY2020": 26341, "FY2019": 19073, "FY2018": 15450}),
]

# ---------------------------------------------------------------
# Balance Sheet - equity reconciliation ladder step 1: built first so each
# year's own Total equity is the independent check value for the equity
# sheet below. Bank (solo) basis. All 5 years tie exactly to the equity
# statement's own opening/closing balances below.
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 18941, "FY2024": 20308, "FY2023": 20201, "FY2022": 19382, "FY2021": 22140, "FY2020": 23369, "FY2019": 16250, "FY2018": 14441}),
    ("DATA", "Items in the course of collection from banks", {"FY2019": 21}),
    ("DATA", "Financial assets at fair value through profit or loss", {"FY2025": 25855, "FY2024": 25620, "FY2023": 21847, "FY2022": 14642, "FY2021": 22268, "FY2020": 20841, "FY2019": 18059, "FY2018": 17092}),
    ("DATA", "Derivative financial instruments", {"FY2025": 18314, "FY2024": 22416, "FY2023": 22606, "FY2022": 24647, "FY2021": 18042, "FY2020": 21818, "FY2019": 18892, "FY2018": 15921}),
    ("DATA", "Loans and advances to banks", {"FY2025": 1006, "FY2024": 1224, "FY2023": 1726, "FY2022": 2063, "FY2021": 2333, "FY2020": 5231, "FY2019": 4792, "FY2018": 2561}),
    ("DATA", "Loans and advances to customers", {"FY2025": 19504, "FY2024": 17524, "FY2023": 16167, "FY2022": 18864, "FY2021": 17176, "FY2020": 18189, "FY2019": 19986, "FY2018": 17036}),
    ("DATA", "Reverse repurchase agreements", {"FY2025": 7024, "FY2024": 5332, "FY2023": 6020, "FY2022": 5606, "FY2021": 5044}),
    ("DATA", "Debt securities", {"FY2025": 379, "FY2024": 336, "FY2023": 374, "FY2022": 305, "FY2021": 229, "FY2020": 257, "FY2019": 112, "FY2018": 132}),
    ("DATA", "Due from fellow Lloyds Banking Group undertakings", {"FY2025": 641, "FY2024": 642, "FY2023": 629, "FY2022": 593, "FY2021": 862, "FY2020": 1218, "FY2019": 819, "FY2018": 1388}),
    ("TOTAL", "Financial assets at amortised cost", {"FY2025": 28554, "FY2024": 25058, "FY2023": 24916, "FY2022": 27431, "FY2021": 25644, "FY2020": 24895, "FY2019": 25709, "FY2018": 21117}),
    ("DATA", "Financial assets at fair value through other comprehensive income", {"FY2023": 0, "FY2022": 6, "FY2021": 100, "FY2020": 149, "FY2019": 314, "FY2018": 412}),
    ("DATA", "Property, plant and equipment", {"FY2023": 38, "FY2022": 45, "FY2021": 53, "FY2020": 61, "FY2019": 55, "FY2018": 6}),
    ("DATA", "Current tax recoverable", {"FY2025": 9, "FY2024": 4, "FY2023": 10, "FY2022": 2, "FY2021": 14, "FY2020": 15}),
    ("DATA", "Deferred tax assets", {"FY2025": 51, "FY2024": 101, "FY2023": 128, "FY2022": 226, "FY2021": 40, "FY2020": 18, "FY2019": 2, "FY2018": 4}),
    ("DATA", "Investment in subsidiary undertakings", {"FY2025": 143, "FY2024": 168, "FY2023": 180, "FY2022": 180, "FY2021": 203, "FY2020": 223, "FY2019": 295, "FY2018": 908}),
    ("DATA", "Other assets", {"FY2025": 866, "FY2024": 1328, "FY2023": 449, "FY2022": 164, "FY2021": 317, "FY2020": 1019, "FY2019": 105, "FY2018": 533}),
    ("TOTAL", "Total assets", {"FY2025": 92733, "FY2024": 95003, "FY2023": 90375, "FY2022": 86725, "FY2021": 88821, "FY2020": 92408, "FY2019": 79702, "FY2018": 70434}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks", {"FY2025": 2214, "FY2024": 2645, "FY2023": 2078, "FY2022": 2456, "FY2021": 3821, "FY2020": 5601, "FY2019": 3970, "FY2018": 3176}),
    ("DATA", "Customer deposits", {"FY2025": 31246, "FY2024": 30945, "FY2023": 29439, "FY2022": 29152, "FY2021": 26553, "FY2020": 25061, "FY2019": 24010, "FY2018": 14180}),
    ("DATA", "Repurchase agreements at amortised cost", {"FY2025": 1002, "FY2024": 0, "FY2023": 1, "FY2022": 7, "FY2021": 1019}),
    ("DATA", "Due to fellow Lloyds Banking Group undertakings", {"FY2025": 603, "FY2024": 1560, "FY2023": 1256, "FY2022": 1526, "FY2021": 3920, "FY2020": 3659, "FY2019": 2084, "FY2018": 6501}),
    ("DATA", "Financial liabilities at fair value through profit or loss", {"FY2025": 24182, "FY2024": 22981, "FY2023": 19686, "FY2022": 12578, "FY2021": 16582, "FY2020": 15815, "FY2019": 13784, "FY2018": 14008}),
    ("DATA", "Derivative financial instruments (liability)", {"FY2025": 12432, "FY2024": 16588, "FY2023": 17576, "FY2022": 20070, "FY2021": 15571, "FY2020": 21233, "FY2019": 17762, "FY2018": 14510}),
    ("DATA", "Debt securities in issue at amortised cost", {"FY2025": 12583, "FY2024": 15090, "FY2023": 15378, "FY2022": 16131, "FY2021": 16644, "FY2020": 15602, "FY2019": 12429, "FY2018": 12942}),
    ("DATA", "Other liabilities", {"FY2025": 885, "FY2024": 600, "FY2023": 280, "FY2022": 558, "FY2021": 444, "FY2020": 1020, "FY2019": 550, "FY2018": 401}),
    ("DATA", "Current tax liabilities", {"FY2025": 18, "FY2024": 11, "FY2023": 12, "FY2022": 29, "FY2021": 8, "FY2019": 24, "FY2018": 19}),
    ("DATA", "Deferred tax liabilities", {"FY2021": 0, "FY2020": 35, "FY2019": 16}),
    ("DATA", "Provisions", {"FY2025": 10, "FY2024": 10, "FY2023": 15, "FY2022": 25, "FY2021": 10}),
    ("DATA", "Subordinated liabilities", {"FY2025": 0, "FY2024": 746, "FY2023": 755, "FY2022": 761, "FY2021": 684, "FY2020": 686, "FY2019": 698, "FY2018": 725}),
    ("TOTAL", "Total liabilities", {"FY2025": 85175, "FY2024": 91176, "FY2023": 86476, "FY2022": 83293, "FY2021": 85256, "FY2020": 88712, "FY2019": 75327, "FY2018": 66462}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 370, "FY2024": 370, "FY2023": 370, "FY2022": 370, "FY2021": 120, "FY2020": 120, "FY2019": 120, "FY2018": 120}),
    ("DATA", "Other reserves", {"FY2025": -131, "FY2024": -236, "FY2023": -314, "FY2022": -530, "FY2021": -62, "FY2020": 83, "FY2019": 31, "FY2018": -17}),
    ("DATA", "Retained profits", {"FY2025": 3174, "FY2024": 2885, "FY2023": 3035, "FY2022": 2810, "FY2021": 2725, "FY2020": 2711, "FY2019": 3442, "FY2018": 3087}),
    ("TOTAL", "Ordinary shareholders' equity", {"FY2025": 3413, "FY2024": 3019, "FY2023": 3091, "FY2022": 2650, "FY2021": 2783, "FY2020": 2914, "FY2019": 3593, "FY2018": 3190}),
    ("DATA", "Other equity instruments", {"FY2025": 4145, "FY2024": 808, "FY2023": 808, "FY2022": 782, "FY2021": 782, "FY2020": 782, "FY2019": 782, "FY2018": 782}),
    ("TOTAL", "Total equity", {"FY2025": 7558, "FY2024": 3827, "FY2023": 3899, "FY2022": 3432, "FY2021": 3565, "FY2020": 3696, "FY2019": 4375, "FY2018": 3972}),
    ("TOTAL", "Total equity and liabilities", {"FY2025": 92733, "FY2024": 95003, "FY2023": 90375, "FY2022": 86725, "FY2021": 88821, "FY2020": 92408, "FY2019": 79702, "FY2018": 70434}),
]

bw.add_balance_sheet_sheet(
    title="Lloyds Bank Corporate Markets plc — Balance Sheet",
    subtitle="Bank (solo) basis. £m. FY2021-FY2023 show a standalone 'Property, plant and equipment' line and a "
              "'Financial assets at fair value through other comprehensive income' line, both since folded into "
              "'Other assets' from FY2024 onward (a genuine structural simplification, not a data gap). FY2018-FY2020 "
              "have no separate 'Reverse repurchase agreements' or 'Repurchase agreements at amortised cost' or "
              "'Provisions' lines at all (genuinely absent from those years' own balance sheets, not folded in "
              "unlabeled - the entity had no repo book or separate provisions line yet), and instead have an "
              "'Items in the course of collection from banks' line (FY2019 only; FY2018/FY2020 Bank column show "
              "£0/blank) not carried in any later year.",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=72,
    source_height=260,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Profit & Loss - necessarily Group consolidated basis (see BASIS NOTE in
# STATEMENTS_SOURCES); Bank's own bottom-line profit/OCI totals shown on the
# Total rows.
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 2424, "FY2024": 2759, "FY2023": 2696, "FY2022": 1087, "FY2021": 356, "FY2020": 444, "FY2019": 813, "FY2018": 354}),
    ("DATA", "Interest expense", {"FY2025": -1981, "FY2024": -2593, "FY2023": -2498, "FY2022": -812, "FY2021": -169, "FY2020": -370, "FY2019": -643, "FY2018": -251}),
    ("TOTAL", "Net interest income", {"FY2025": 443, "FY2024": 166, "FY2023": 198, "FY2022": 275, "FY2021": 187, "FY2020": 74, "FY2019": 170, "FY2018": 103}),
    ("DATA", "Fee and commission income", {"FY2025": 329, "FY2024": 321, "FY2023": 303, "FY2022": 228, "FY2021": 248, "FY2020": 218, "FY2019": 230, "FY2018": 148}),
    ("DATA", "Fee and commission expense", {"FY2025": -58, "FY2024": -53, "FY2023": -39, "FY2022": -36, "FY2021": -27, "FY2020": -27, "FY2019": -42, "FY2018": -27}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 271, "FY2024": 268, "FY2023": 264, "FY2022": 192, "FY2021": 221, "FY2020": 191, "FY2019": 188, "FY2018": 121}),
    ("DATA", "Net trading income", {"FY2025": 472, "FY2024": 552, "FY2023": 442, "FY2022": 495, "FY2021": 244, "FY2020": 279, "FY2019": 461, "FY2018": 231}),
    ("DATA", "Other operating income/(expense)", {"FY2025": -39, "FY2024": -2, "FY2023": 4, "FY2022": 5, "FY2021": -11}),
    ("TOTAL", "Other income", {"FY2025": 704, "FY2024": 818, "FY2023": 710, "FY2022": 692, "FY2021": 454, "FY2020": 470, "FY2019": 649, "FY2018": 352}),
    ("TOTAL", "Total income", {"FY2025": 1147, "FY2024": 984, "FY2023": 908, "FY2022": 967, "FY2021": 641, "FY2020": 544, "FY2019": 819, "FY2018": 455}),
    ("TOTAL", "Operating expenses", {"FY2025": -510, "FY2024": -499, "FY2023": -509, "FY2022": -444, "FY2021": -414, "FY2020": -428, "FY2019": -462, "FY2018": -273}),
    ("DATA", "Impairment (charge)/credit", {"FY2025": -1, "FY2024": 16, "FY2023": 28, "FY2022": -46, "FY2021": 62, "FY2020": -71, "FY2019": 11, "FY2018": 8}),
    ("TOTAL", "Profit before tax (Group)", {"FY2025": 636, "FY2024": 501, "FY2023": 427, "FY2022": 477, "FY2021": 289, "FY2020": 45, "FY2019": 368, "FY2018": 190}),
    ("DATA", "Tax expense (Group)", {"FY2025": -95, "FY2024": -97, "FY2023": -89, "FY2022": -97, "FY2021": -51, "FY2020": -1, "FY2019": -85, "FY2018": -37}),
    ("TOTAL", "Profit for the year (Group)", {"FY2025": 541, "FY2024": 404, "FY2023": 338, "FY2022": 380, "FY2021": 238, "FY2020": 44, "FY2019": 283, "FY2018": 153}),
    ("TOTAL", "Profit for the year (Bank)", {"FY2025": 495, "FY2024": 378, "FY2023": 320, "FY2022": 348, "FY2021": 247, "FY2020": 9, "FY2019": 397, "FY2018": 106}),
    ("SECTION", "Other comprehensive income, net of tax (Bank column, ties to Statement of Changes in Equity)", {}),
    ("DATA", "Movements in revaluation reserve (FVOCI debt securities), net of tax", {"FY2023": 2, "FY2022": 0, "FY2020": -1, "FY2019": -2, "FY2018": -7}),
    ("DATA", "Movements in cash flow hedging reserve, net of tax", {"FY2025": 128, "FY2024": 70, "FY2023": 230, "FY2022": -471, "FY2021": -153, "FY2020": 49, "FY2019": 51, "FY2018": 5}),
    ("DATA", "Movements in foreign currency translation reserve, net of tax", {"FY2025": -23, "FY2024": 8, "FY2023": -16, "FY2022": 3, "FY2021": 4, "FY2020": 4, "FY2019": -1, "FY2018": 0}),
    ("TOTAL", "Total other comprehensive income/(loss), net of tax (Bank)", {"FY2025": 105, "FY2024": 78, "FY2023": 216, "FY2022": -468, "FY2021": -145, "FY2020": 52, "FY2019": 48, "FY2018": -2}),
    ("TOTAL", "Total comprehensive income/(loss) for the year (Bank)", {"FY2025": 600, "FY2024": 456, "FY2023": 536, "FY2022": -120, "FY2021": 102, "FY2020": 61, "FY2019": 445, "FY2018": 104}),
]

bw.add_income_statement_sheet(
    title="Lloyds Bank Corporate Markets plc — Profit & Loss",
    subtitle="Income statement is Group consolidated (LBCM publishes no separate Bank-solo income statement line "
              "items - see BASIS NOTE in the source citation). The Bank's own bottom-line 'Profit for the year' and "
              "OCI/total comprehensive income rows are the Bank-column aggregate figures, matching the Statement of "
              "Changes in Equity. £m. FY2018 is LBCM's first year of trading (see FLOOR NOTE) - its own Annual "
              "Report presents no FY2017 comparative at all, stating 'No comparative information is presented as "
              "the Group did not trade in the prior period'.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=80,
    source_height=280,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - Bank (solo) basis. Per-year reconciliation
# ladder confirmed: every year's own closing balance ties exactly to both the
# next year's own opening balance and that year's own Balance Sheet Total
# equity above. Zero plug rows needed anywhere across all 5 years. Ladder's
# mandated scan of each year's equity note caught genuine "easy to skip"
# categories: distributions on other equity instruments, issuances/
# repurchases/gains on other equity instruments, and (FY2022) an ordinary
# share issuance and a loss on repayment of other equity instruments.
# ---------------------------------------------------------------
equity_headers = ["Share capital", "Other reserves", "Retained profits",
                   "Ordinary shareholders' equity", "Other equity instruments", "Total equity"]
equity_rows = [
    ("TOTAL", "At 1 January 2018 (incorporation, FY2017 closing - dormant shell company)", (20, 0, 0, 20, 0, 20)),
    ("DATA", "Profit for the year", (None, None, 106, 106, None, 106)),
    ("DATA", "Movements in revaluation reserve (FVOCI debt securities), net of tax", (None, -7, None, -7, None, -7)),
    ("DATA", "Movements in cash flow hedging reserve, net of tax", (None, 5, None, 5, None, 5)),
    ("DATA", "Distributions on other equity instruments", (None, None, -18, -18, None, -18)),
    ("DATA", "Issue of ordinary shares", (100, None, None, 100, None, 100)),
    ("DATA", "Establishment of foreign currency translation opening reserve", (None, -15, 15, 0, None, 0)),
    ("DATA", "Opening reserves adjustment in respect of other transfers", (None, None, 9, 9, None, 9)),
    ("DATA", "Capital contribution received", (None, None, 2975, 2975, None, 2975)),
    ("DATA", "Issue of other equity instruments (AT1)", (None, None, None, None, 782, 782)),
    ("TOTAL", "At 31 December 2018 (FY2018 closing)", (120, -17, 3087, 3190, 782, 3972)),
    ("DATA", "Profit for the year", (None, None, 397, 397, None, 397)),
    ("DATA", "Movements in revaluation reserve (FVOCI debt securities), net of tax", (None, -2, None, -2, None, -2)),
    ("DATA", "Movements in cash flow hedging reserve, net of tax", (None, 51, None, 51, None, 51)),
    ("DATA", "Movements in foreign currency translation reserve, net of tax", (None, -1, None, -1, None, -1)),
    ("DATA", "Distributions on other equity instruments", (None, None, -49, -49, None, -49)),
    ("DATA", "Other adjustments", (None, None, 7, 7, None, 7)),
    ("TOTAL", "At 31 December 2019 (FY2019 closing)", (120, 31, 3442, 3593, 782, 4375)),
    ("DATA", "Profit for the year", (None, None, -31, -31, 40, 9)),
    ("DATA", "Movements in revaluation reserve (FVOCI debt securities), net of tax", (None, -1, None, -1, None, -1)),
    ("DATA", "Movements in cash flow hedging reserve, net of tax", (None, 49, None, 49, None, 49)),
    ("DATA", "Movements in foreign currency translation reserve, net of tax", (None, 4, None, 4, None, 4)),
    ("DATA", "Dividends", (None, None, -700, -700, None, -700)),
    ("DATA", "Distributions on other equity instruments", (None, None, None, None, -40, -40)),
    ("TOTAL", "At 31 December 2020 (FY2020 closing)", (120, 83, 2711, 2914, 782, 3696)),
    ("DATA", "Profit for the year", (None, None, 214, 214, 33, 247)),
    ("DATA", "Movements in revaluation reserve (FVOCI debt securities), net of tax", (None, 8, None, 8, None, 8)),
    ("DATA", "Movements in cash flow hedging reserve, net of tax", (None, -153, None, -153, None, -153)),
    ("DATA", "Dividends", (None, None, -200, -200, None, -200)),
    ("DATA", "Distributions on other equity instruments", (None, None, None, None, -33, -33)),
    ("TOTAL", "At 1 January 2022 (FY2021 closing)", (120, -62, 2725, 2783, 782, 3565)),
    ("DATA", "Profit for the year", (None, None, 305, 305, 43, 348)),
    ("DATA", "Movements in cash flow hedging reserve, net of tax", (None, -471, None, -471, None, -471)),
    ("DATA", "Movements in foreign currency translation reserve, net of tax", (None, 3, None, 3, None, 3)),
    ("DATA", "Dividends", (None, None, -220, -220, None, -220)),
    ("DATA", "Distributions on other equity instruments", (None, None, None, None, -43, -43)),
    ("DATA", "Issue of ordinary shares", (250, None, None, 250, None, 250)),
    ("TOTAL", "At 31 December 2022 (FY2022 closing)", (370, -530, 2810, 2650, 782, 3432)),
    ("DATA", "Profit for the year", (None, None, 240, 240, 80, 320)),
    ("DATA", "Movements in revaluation reserve (FVOCI debt securities), net of tax", (None, 2, None, 2, None, 2)),
    ("DATA", "Movements in cash flow hedging reserve, net of tax", (None, 230, None, 230, None, 230)),
    ("DATA", "Movements in foreign currency translation reserve, net of tax", (None, -16, None, -16, None, -16)),
    ("DATA", "Distributions on other equity instruments", (None, None, None, None, -80, -80)),
    ("DATA", "Net issuance of other equity instruments", (None, None, None, None, 26, 26)),
    ("DATA", "Loss on repayment of other equity instruments", (None, None, -15, -15, None, -15)),
    ("TOTAL", "At 31 December 2023 (FY2023 closing)", (370, -314, 3035, 3091, 808, 3899)),
    ("DATA", "Profit for the year", (None, None, 300, 300, 78, 378)),
    ("DATA", "Movements in cash flow hedging reserve, net of tax", (None, 70, None, 70, None, 70)),
    ("DATA", "Movements in foreign currency translation reserve, net of tax", (None, 8, None, 8, None, 8)),
    ("DATA", "Dividends", (None, None, -450, -450, None, -450)),
    ("DATA", "Distributions on other equity instruments", (None, None, None, None, -78, -78)),
    ("TOTAL", "At 31 December 2024 (FY2024 closing)", (370, -236, 2885, 3019, 808, 3827)),
    ("DATA", "Profit for the year", (None, None, 285, 285, 210, 495)),
    ("DATA", "Movements in cash flow hedging reserve, net of tax", (None, 128, None, 128, None, 128)),
    ("DATA", "Movements in foreign currency translation reserve, net of tax", (None, -23, None, -23, None, -23)),
    ("DATA", "Distributions on other equity instruments", (None, None, None, None, -210, -210)),
    ("DATA", "Net issuance of other equity instruments", (None, None, None, None, 3337, 3337)),
    ("DATA", "Gain on other equity instruments", (None, None, 4, 4, None, 4)),
    ("TOTAL", "At 31 December 2025 (FY2025 closing)", (370, -131, 3174, 3413, 4145, 7558)),
]

bw.add_equity_changes_sheet(
    title="Lloyds Bank Corporate Markets plc — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, Bank (solo) basis, from incorporation (28 September 2016, "
              "dormant until FY2018 - see FLOOR NOTE) through FY2025. £m. Equity reconciliation ladder confirmed: "
              "every year's own closing balance ties exactly to both the next year's own opening balance and that "
              "year's own Balance Sheet Total equity - zero plug rows needed anywhere across all 8 years, including "
              "the FY2018-FY2021 movements newly added here (each hand-verified against that year's own Annual "
              "Report's own Bank-column Statement of Changes in Equity, not a later year's restated comparative).",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=64,
)

CASH_NOTE = (
    "Two genuine restatements exist between years' opening/closing cash balances; each "
    "year's own originally-published figure is used (not the following year's restated "
    "comparative), per this project's standard convention: (1) FY2021's own report shows "
    "Bank closing cash of £23,038m, but FY2022's own report's FY2021 comparative shows "
    "£23,083m (a £45m gap). (2) FY2023's own report shows Bank closing cash of £20,169m, "
    "but FY2024's own report's FY2023 comparative shows £21,743m (a much larger £1,574m "
    "gap) — flagged prominently as it is the larger of the two and not further explained "
    "in either source document. FY2024→FY2025 and FY2022→FY2023 both tie exactly. "
    "FY2018→FY2019→FY2020→FY2021 each tie exactly as well (each year's own closing cash "
    "matches the next year's own opening cash, hand-verified against each year's own "
    "originally-published report) — no restatement gaps anywhere across the newly added "
    "years. FY2018's own cash flow statement discloses no separate 'Tax paid' line (blank "
    "here, not a transcription gap — the year's first, partial trading period simply nets "
    "tax within the total) and no 'Effect of exchange rate changes' line either (shown as "
    "0, matching the Bank column's own '-' entry); FY2019's Bank column also shows '-' "
    "(0) for that line."
)
bw.add_cash_flow_sheet(
    "Lloyds Bank Corporate Markets plc — Cash Flow Statement",
    "Lloyds Bank Corporate Markets plc, Bank (solo) basis, £m. " + CASH_NOTE,
    cash_rows,
    annual_sources("annual"),
    first_col_width=66,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Asset Quality - Loans and advances to customers by IFRS 9 stage. Bank
# (solo) basis for FY2022-FY2025 (net carrying value ties exactly to that
# year's own Balance Sheet loans line each year). FY2021's own report
# discloses only a Group-level table that additionally combines loans and
# advances to customers WITH reverse repurchase agreements - a genuine
# structural difference (not a transcription gap), shown here as-disclosed
# and flagged; it does not tie to FY2021's Bank Balance Sheet loans line.
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, by IFRS 9 stage (Bank, FY2018-FY2020 and FY2022-FY2025; Group combined with reverse repos, FY2021)", {}),
    ("DATA", "Stage 1 (gross)", {"FY2025": 19322, "FY2024": 17428, "FY2023": 15996, "FY2022": 17851, "FY2021": 21874, "FY2020": 17833, "FY2019": 19759, "FY2018": 16849}),
    ("DATA", "Stage 2 (gross)", {"FY2025": 184, "FY2024": 96, "FY2023": 180, "FY2022": 1029, "FY2021": 47, "FY2020": 364, "FY2019": 19, "FY2018": 0}),
    ("DATA", "Stage 3 (gross)", {"FY2025": 6, "FY2024": 7, "FY2023": 9, "FY2022": 22, "FY2021": 29, "FY2020": 39, "FY2019": 293, "FY2018": 277}),
    ("TOTAL", "Total gross carrying amount", {"FY2025": 19512, "FY2024": 17531, "FY2023": 16185, "FY2022": 18902, "FY2021": 21950, "FY2020": 18236, "FY2019": 20071, "FY2018": 17126}),
    ("DATA", "Allowance for expected credit losses", {"FY2025": -8, "FY2024": -7, "FY2023": -18, "FY2022": -38, "FY2021": -10, "FY2020": -47, "FY2019": -85, "FY2018": -90}),
    ("TOTAL", "Net carrying amount", {"FY2025": 19504, "FY2024": 17524, "FY2023": 16167, "FY2022": 18864, "FY2021": 21940, "FY2020": 18189, "FY2019": 19986, "FY2018": 17036}),
    ("DATA", "Stage 3 as % of total gross carrying amount (NPL ratio)", {"FY2025": "0.03%", "FY2024": "0.04%", "FY2023": "0.06%", "FY2022": "0.12%", "FY2021": "0.13%", "FY2020": "0.21%", "FY2019": "1.46%", "FY2018": "1.62%"}),
    ("DATA", "ECL allowance as % of total gross carrying amount (coverage)", {"FY2025": "0.04%", "FY2024": "0.04%", "FY2023": "0.11%", "FY2022": "0.20%", "FY2021": "0.05%", "FY2020": "0.26%", "FY2019": "0.42%", "FY2018": "0.53%"}),
]

bw.add_asset_quality_sheet(
    title="Lloyds Bank Corporate Markets plc — Asset Quality",
    subtitle="Loans and advances to customers, IFRS 9 stage 1/2/3 split. £m.",
    rows=asset_quality_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nFY2025/FY2024: Annual Report and Accounts 2025, Note 14 'Loans and advances to customers' (Bank table), "
        "p.87. FY2023/FY2022: Annual Report and Accounts 2023, Note 12 'Loans and advances to customers' (Bank "
        "table), p.83. FY2021: Annual Report and Accounts 2021, Note 13 'Financial assets at amortised cost', "
        "'Loans and advances to customers and reverse repurchase agreements' table, p.59-60. FY2020: Annual Report "
        "and Accounts 2020, Note 13 'Financial assets at amortised cost' (2) The Bank, 'Year ended 31 December 2020' "
        f"table, p.56 — {AR_URLS['FY2020']}. FY2019: Annual Report and Accounts 2019, Note 14 'Financial assets at "
        f"amortised cost' (2) The Bank, 'Year ended 31 December 2019' table, p.48 — {AR_URLS['FY2019']}. FY2018: "
        f"Annual Report and Accounts 2018, Note 14 'Financial assets at amortised cost' 2) The Bank, p.43 — "
        f"{AR_URLS['FY2018']}.\n\n"
        "DATA QUALITY FLAG: FY2021's own report discloses this stage split only at Group level, and only as a "
        "combined 'Loans and advances to customers and reverse repurchase agreements' category (Total gross carrying "
        "amount 21,950; Net carrying amount 21,940), unlike FY2022-FY2025's Bank-level tables which cover loans and "
        "advances to customers ALONE - a genuine structural/disclosure difference, not a transcription error. "
        "FY2021's Net carrying amount therefore does NOT tie to FY2021's Bank Balance Sheet 'Loans and advances to "
        "customers' line (17,176) the way FY2022-FY2025 do - shown as originally disclosed rather than adjusted to "
        "force a tie. FY2018-FY2020's Bank-level tables DO tie exactly to those years' own Balance Sheet 'Loans and "
        "advances to customers' line (17,036 / 19,986 / 18,189 respectively)."
    ),
    first_col_width=90,
    source_height=340,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# KM1 Key Metrics - "KM1: Key Metrics" from Lloyds Bank Corporate Markets
# plc's own Year-End Pillar 3 Disclosures. Placed before the 11 single-metric
# sheets so it lands after Asset Quality and before CET1 Capital.
#
# Points to watch, all preserved as printed:
#
#   * THREE COLUMNS PER EDITION (31 Dec, 30 Jun, 31 Dec prior). Only the
#     year-end column of each edition is carried here; the 30-Jun half-year
#     column is a half-year position and lives on the Interim Pillar 3 sheet.
#
#   * A DOUBLE REFERENCE COLUMN ("KM1 Ref" and "LR2 Ref"), because the table
#     embeds extracts of LR2 (Leverage ratio common disclosure) that must be
#     published quarterly. Rows UK-31, UK-32 and 27 have an LR2 reference and
#     no KM1 number at all; they are kept and labelled by their LR2 reference
#     because the Bank prints them inside its KM1.
#
#   * THE FY2021 AND FY2020 EDITIONS DO NOT PRINT A UK KM1. Both print
#     "KM1: Comparison of institution's own funds and capital and leverage
#     ratios with and without the application of transitional arrangements for
#     IFRS 9 or analogous ECLs (IFRS9 - FL)" - a 17-row IFRS9-FL table with
#     CRD IV leverage rows, which is a DIFFERENT template, not an unnumbered
#     or shortened UK KM1 (map rule 8). FY2021 here is therefore the 31 Dec
#     2021 comparative column of the FY2022 edition, which is the first LBCM
#     edition to print the UK template. FY2020/FY2019/FY2018 have no UK KM1
#     source at all and are left blank rather than back-filled.
#
#   * THE 1 JANUARY 2022 LEVERAGE BASIS BREAK, stated by the Bank itself: the
#     FY2022 edition footnotes rows 13/14 "The leverage exposure measure and
#     ratios reported for 31 December 2021 have been calculated under the
#     original CRR leverage rules, inclusive of claims on central banks." The
#     two bases are kept as two separate blocks and never merged.
#
#   * PRECISION DRIFT ALONG ROWS 8, 9 AND 11: the FY2022 and FY2023 editions
#     print three decimals ("2.500%", "0.506%", "3.006%"), the FY2024 and
#     FY2025 editions one ("2.5%", "1.0%", "3.5%"). Each cell is from its own
#     year's edition, so the precision varies along the row.
#
#   * ROW 10a APPEARS ONLY IN THE FY2022 EDITION, and it prints an em dash in
#     all three of its columns. A dash is not a zero, so the row is kept and
#     left blank (map rule 2).
#
#   * UNLIKE BANK OF SCOTLAND, LBCM DOES NOT EXCLUDE LIQ1/LIQ2. Its own
#     "Appendix 1: Excluded templates" lists only INS1, INS2, CR2a, CQ2, CQ6,
#     CQ7, CQ8, CR7, CR10.3, CR10.4, CR10.5 and CCR7 - no liquidity template -
#     and the Bank prints rows 15-20 itself. The blanks in the LCR block for
#     FY2021 and in the NSFR block for FY2021/FY2022 are rows the Bank did not
#     print in those editions, not a formal Article 432 exclusion.
# ---------------------------------------------------------------
km1_rows = [
    ("SECTION", "Available own funds (amounts)", {}),
    ("DATA", "1    Common Equity Tier 1 (CET1) capital (£m)",
     {"FY2025": 3085, "FY2024": 2797, "FY2023": 2725, "FY2022": 2948, "FY2021": 2423}),
    ("DATA", "2    Tier 1 capital (£m)",
     {"FY2025": 7137, "FY2024": 3580, "FY2023": 3508, "FY2022": 3705, "FY2021": 3180}),
    ("DATA", "3    Total capital (£m)",
     {"FY2025": 7137, "FY2024": 4171, "FY2023": 4109, "FY2022": 4285, "FY2021": 3709}),
    ("SECTION", "Risk-weighted exposure amounts", {}),
    ("DATA", "4    Total risk-weighted exposure amount (£m)",
     {"FY2025": 22442, "FY2024": 20605, "FY2023": 20492, "FY2022": 20195, "FY2021": 18436}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "5    Common Equity Tier 1 ratio (%)",
     {"FY2025": "13.7%", "FY2024": "13.6%", "FY2023": "13.3%", "FY2022": "14.6%", "FY2021": "13.1%"}),
    ("DATA", "6    Tier 1 ratio (%)",
     {"FY2025": "31.8%", "FY2024": "17.4%", "FY2023": "17.1%", "FY2022": "18.3%", "FY2021": "17.2%"}),
    ("DATA", "7    Total capital ratio (%)",
     {"FY2025": "31.8%", "FY2024": "20.2%", "FY2023": "20.1%", "FY2022": "21.2%", "FY2021": "20.1%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "UK 7a    Additional CET1 SREP requirements (%)",
     {"FY2025": "2.3%", "FY2024": "2.4%", "FY2023": "2.7%", "FY2022": "2.6%", "FY2021": "2.6%"}),
    ("DATA", "UK 7b    Additional AT1 SREP requirements (%)",
     {"FY2025": "0.7%", "FY2024": "0.8%", "FY2023": "0.9%", "FY2022": "0.9%", "FY2021": "0.9%"}),
    ("DATA", "UK 7c    Additional T2 SREP requirements (%)",
     {"FY2025": "1.0%", "FY2024": "1.0%", "FY2023": "1.2%", "FY2022": "1.1%", "FY2021": "1.1%"}),
    ("DATA", "UK 7d    Total SREP own funds requirements (%)",
     {"FY2025": "12.0%", "FY2024": "12.2%", "FY2023": "12.9%", "FY2022": "12.6%", "FY2021": "12.6%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "8    Capital conservation buffer (%)",
     {"FY2025": "2.5%", "FY2024": "2.5%", "FY2023": "2.500%", "FY2022": "2.500%", "FY2021": "2.500%"}),
    ("DATA", "9    Institution specific countercyclical capital buffer (%)",
     {"FY2025": "0.8%", "FY2024": "1.0%", "FY2023": "0.960%", "FY2022": "0.506%", "FY2021": "0.029%"}),
    ("DATA", "10a    Other Systemically Important Institution buffer (%)  — printed only in the FY2022 edition, "
             "and printed there as an em dash in every column", {}),
    ("DATA", "11    Combined buffer requirement (%)",
     {"FY2025": "3.3%", "FY2024": "3.5%", "FY2023": "3.460%", "FY2022": "3.006%", "FY2021": "2.529%"}),
    ("DATA", "UK 11a    Overall capital requirements (%)",
     {"FY2025": "15.3%", "FY2024": "15.7%", "FY2023": "16.3%", "FY2022": "15.6%", "FY2021": "15.1%"}),
    ("DATA", "12    CET1 available after meeting minimum SREP own funds requirements (%)",
     {"FY2025": "7.0%", "FY2024": "6.7%", "FY2023": "6.1%", "FY2022": "7.5%", "FY2021": "6.0%"}),
    ("SECTION", "Leverage ratio — UK basis, excluding claims on central banks (from 1 January 2022)", {}),
    ("DATA", "13  (LR2 UK-24b)    Total exposure measure excluding claims on central banks (£m)",
     {"FY2025": 84702, "FY2024": 79612, "FY2023": 74378, "FY2022": 69175}),
    ("DATA", "14  (LR2 25)    Leverage ratio excluding claims on central banks (%)",
     {"FY2025": "8.4%", "FY2024": "4.5%", "FY2023": "4.7%", "FY2022": "5.4%"}),
    ("SECTION", "Leverage ratio — original CRR basis, including claims on central banks (to 31 December 2021)", {}),
    ("DATA", "13  (as footnoted in the FY2022 edition)    Total exposure measure, original CRR rules inclusive of "
             "claims on central banks (£m)", {"FY2021": 92034}),
    ("DATA", "14  (as footnoted in the FY2022 edition)    Leverage ratio, original CRR rules inclusive of claims on "
             "central banks (%)", {"FY2021": "3.5%"}),
    ("SECTION", "Additional leverage ratio disclosure requirements", {}),
    ("DATA", "UK 14a  (LR2 UK-25a)    Fully loaded ECL accounting model leverage ratio excluding claims on central banks (%)",
     {"FY2025": "8.4%", "FY2024": "4.5%", "FY2023": "4.7%"}),
    ("DATA", "UK 14b  (LR2 UK-25c)    Leverage ratio including claims on central banks (%)",
     {"FY2025": "6.9%", "FY2024": "3.6%", "FY2023": "3.7%"}),
    ("DATA", "UK 14c  (LR2 UK-34)    Average leverage ratio excluding claims on central banks (%)",
     {"FY2025": "8.1%", "FY2024": "4.4%", "FY2023": "4.9%"}),
    ("DATA", "UK 14d  (LR2 UK-33)    Average leverage ratio including claims on central banks (%)",
     {"FY2025": "6.6%", "FY2024": "3.5%", "FY2023": "3.9%"}),
    ("DATA", "(LR2 UK-31)    Average total exposure measure including claims on central banks (£m)",
     {"FY2025": 108537, "FY2024": 101559}),
    ("DATA", "(LR2 UK-32)    Average total exposure measure excluding claims on central banks (£m)",
     {"FY2025": 88057, "FY2024": 81359}),
    ("DATA", "(LR2 27)    Leverage ratio buffer (%)", {"FY2025": "0.3%", "FY2024": "0.3%"}),
    ("DATA", "UK 14e  (LR2 UK-27b)    Of which: countercyclical leverage ratio buffer (%)",
     {"FY2025": "0.3%", "FY2024": "0.3%", "FY2023": "0.3%"}),
    ("SECTION", "Average Liquidity Coverage Ratio (weighted) (LCR)", {}),
    ("DATA", "15    Total high-quality liquid assets (HQLA) (Weighted value - average) (£m)",
     {"FY2025": 26830, "FY2024": 26839, "FY2023": 27207, "FY2022": 23858}),
    ("DATA", "UK 16a    Cash outflows - Total weighted value - average (£m)",
     {"FY2025": 24667, "FY2024": 26051, "FY2023": 26741, "FY2022": 24799}),
    ("DATA", "UK 16b    Cash inflows - Total weighted value - average (£m)",
     {"FY2025": 8734, "FY2024": 10042, "FY2023": 10289, "FY2022": 10692}),
    ("DATA", "16    Total net cash outflows (adjusted value - average) (£m)",
     {"FY2025": 15933, "FY2024": 16009, "FY2023": 16452, "FY2022": 14107}),
    ("DATA", "17    Average liquidity coverage ratio (%)",
     {"FY2025": "169%", "FY2024": "168%", "FY2023": "166%", "FY2022": "170%"}),
    ("SECTION", "Average Net Stable Funding Ratio", {}),
    ("DATA", "18    Total available stable funding (Weighted value - average) (£m)",
     {"FY2025": 31298, "FY2024": 26344, "FY2023": 28855}),
    ("DATA", "19    Total required stable funding (Weighted value - average) (£m)",
     {"FY2025": 23500, "FY2024": 19111, "FY2023": 19891}),
    ("DATA", "20    Average NSFR ratio (%)", {"FY2025": "133%", "FY2024": "138%", "FY2023": "145%"}),
]

KM1_SOURCES = (
    "Sources - Lloyds Bank Corporate Markets plc's own Year-End Pillar 3 Disclosures, 'KM1: Key Metrics' template, "
    "£m and % exactly as printed. Each year is taken from the edition in which it is the reporting year, never from "
    "a later edition's comparative, except FY2021 as explained below:\n"
    f"FY2025: 2025 Year-End Pillar 3 Disclosures, KM1, p.4 (column '31 Dec 2025') - {P3_URLS['FY2025']}\n"
    f"FY2024: 2024 Year-End Pillar 3 Disclosures, KM1, p.4 (column '31 Dec 2024') - {P3_URLS['FY2024']}\n"
    f"FY2023: 2023 Year-End Pillar 3 Disclosures, KM1, p.4 (column '31 Dec 2023') - {P3_URLS['FY2023']}\n"
    f"FY2022: 2022 Year-End Pillar 3 Disclosures, KM1, p.5 (column '31 Dec 2022') - {P3_URLS['FY2022']}\n"
    f"FY2021: the '31 Dec 2021' comparative column of the FY2022 edition above. The FY2021 edition's own key-metrics "
    f"table is a DIFFERENT template - 'KM1: Comparison of institution's own funds and capital and leverage ratios "
    f"with and without the application of transitional arrangements for IFRS 9 or analogous ECLs (IFRS9 - FL)', a "
    f"17-row IFRS9-FL table whose rows are CET1/Tier 1/Total capital and RWA with and without transitional relief "
    f"plus three CRD IV leverage rows. It carries none of the SREP, buffer, LCR or NSFR rows of the UK template, so "
    f"it cannot supply UK KM1 rows and is not treated as an unnumbered KM1: {P3_URLS['FY2021']}\n"
    "  (Checked against images as well as text, because a KM1 table can be published as a bitmap inside an "
    "otherwise text-native PDF and then extract as nothing at all. `pdfimages -list` returns ZERO embedded images "
    "for all six LBCM year-end editions, FY2020 through FY2025, so no table in any of them can be hidden from "
    "text extraction, and the IFRS9-FL tables in the FY2020 and FY2021 editions do extract in full - 17 numbered "
    "rows and three columns each.)\n"
    f"FY2020: the FY2020 edition likewise prints only the IFRS9-FL template, so FY2020 has no UK KM1 source and its "
    f"column is blank here - {P3_URLS['FY2020']}\n"
    "FY2019 and FY2018: blank. FY2019's Pillar 3 is an xlsx with 'Key Ratios'/'OV1' tabs rather than the UK KM1 "
    "template, and no standalone Pillar 3 report exists for FY2018 (LBCM's first year of trading) - verified "
    "against the Lloyds Banking Group Financial Downloads index below, whose LBCM 2018 folder contains an annual "
    "report, carve-out financial statements and a fixed-income presentation and no Pillar 3 document.\n"
    f"Index (live, re-checked 2026-09-16): {P3_INDEX_URL}\n\n"
    "SOURCING NOTE, recorded because the underlying mistake generalises (see KM1-032). The Lloyds Banking Group "
    "Financial Downloads page returns a Cloudflare block (error 1007) to a plain automated fetch, and on an earlier "
    "build of a sibling workbook in this project that block was written down as a fact about the BANK - producing a "
    "false 'no standalone Pillar 3 document is published for this entity' claim. A block is a fact about our reach, "
    "not about the bank. Re-fetched 2026-09-16 with an ordinary browser User-Agent, the page loads normally and "
    "carries 129 Pillar 3 PDFs, 41 of them LBCM's own (full-year, half-year and quarterly, 2019 through 2026). No "
    "such false claim was present in this LBCM script - its URLs were already correct - and every one of the six "
    "full-year Pillar 3 PDFs was re-downloaded and verified on 2026-09-16 (HTTP 200, Content-Type application/pdf, "
    "%PDF magic bytes).\n\n"
    "KM1 presentation notes:\n"
    "• THREE COLUMNS PER EDITION (31 Dec, 30 Jun, 31 Dec prior). Only the year-end columns are carried here; the "
    "30-Jun half-year columns are half-year positions and appear on the Interim Pillar 3 sheet instead.\n"
    "• A DOUBLE REFERENCE COLUMN. Each row carries both a 'KM1 Ref' and an 'LR2 Ref', because the table embeds "
    "extracts of LR2 (Leverage ratio common disclosure) required to be disclosed quarterly. Rows UK-31, UK-32 and "
    "27 have an LR2 reference and no KM1 number at all; they are kept and labelled by their LR2 reference because "
    "the Bank prints them inside its KM1.\n"
    "• THE 1 JANUARY 2022 LEVERAGE BASIS BREAK is stated by the Bank itself. The FY2022 edition footnotes rows "
    "13/14: 'The leverage exposure measure and ratios reported for 31 December 2021 have been calculated under the "
    "original CRR leverage rules, inclusive of claims on central banks.' The two bases are shown as two separate "
    "blocks above and are never merged into one series.\n"
    "• PRECISION DRIFT ALONG ROWS 8, 9 AND 11. The FY2022 and FY2023 editions print three decimals ('2.500%', "
    "'0.506%', '3.006%'); the FY2024 and FY2025 editions print one ('2.5%', '1.0%', '3.5%'). Each cell is from its "
    "own year's edition, so the precision varies along the row. The FY2022 edition additionally prints its "
    "countercyclical buffer figures with a space before the per-cent sign ('0.046 %', '0.029 %'); that spacing is "
    "not reproducible in a spreadsheet cell and is recorded here instead.\n"
    "• ROW 10a (Other Systemically Important Institution buffer) IS PRINTED ONLY IN THE FY2022 EDITION, and printed "
    "there as an em dash in all three of its columns. A dash is not a zero, so the row is kept and left blank.\n"
    "• ROW SETS DRIFT. The FY2022 edition's KM1 stops at row 17 - it has no 14a-14e leverage block and no NSFR "
    "block at all - and its 31 Dec 2021 column is empty for the whole LCR block. The FY2023 edition adds 14a-14e "
    "but has no UK-31/UK-32/27 rows and captions UK 14e 'Countercyclical leverage ratio buffer (%)' where the "
    "FY2024 and FY2025 editions caption it 'Of which: countercyclical leverage ratio buffer (%)'. Every blank above "
    "is a row-and-column the Bank did not print, not a row this project failed to find.\n"
    "• KNOWN DIVERGENCE FROM THE NSFR METRIC SHEET, kept deliberately. Row 20 is blank for FY2022 here because the "
    "FY2022 edition prints no NSFR block, while the NSFR metric sheet carries 137% for FY2022 recovered from the "
    "FY2023 edition's comparative column. KM1 reproduces one edition's printed table; the metric sheet is a "
    "best-available time series. Neither figure is wrong and neither has been adjusted to match the other.\n"
    "• NO ARTICLE 432 LIQUIDITY EXCLUSION HERE. Unlike its sister entity Bank of Scotland plc, whose Appendix 1 "
    "excludes LIQ1/LIQ2/LIQA/LIQB because 'Liquidity is managed at a Lloyds Bank Liquidity Sub-Group level', LBCM's "
    "own 'Appendix 1: Excluded templates' lists only INS1, INS2, CR2a, CQ2, CQ6, CQ7, CQ8, CR7, CR10.3, CR10.4, "
    "CR10.5 and CCR7 - no liquidity template - and LBCM prints rows 15-20 itself.\n"
    "• DASHES: the Bank states in its basis of preparation that 'de minimis monetary amounts (<£0.5 million) are "
    "rounded down for reporting purposes and disclosed as a dash', so a dash in these documents is a rounded-down "
    "small amount rather than an inapplicable requirement. Row 10a's em dashes are the only dashes falling in the "
    "rows above.\n"
    "• ENTITY AND BASIS: every edition prints the template exactly once, headed 'This document presents the Pillar "
    "3 disclosures of Lloyds Bank Corporate Markets plc (\"the Bank\")'. There is no second solo-beside-consolidated "
    "printing to confuse it with, and the figures tie exactly to the 'Capital resources of the Bank' table in the "
    "matching Annual Report (FY2025: CET1 £3,085m, RWAs £22,442m in both).\n\n"
    + ENTITY_NOTE
)

bw.add_km1_sheet(
    title="Lloyds Bank Corporate Markets plc — KM1 Key Metrics",
    subtitle="The Bank's own published 'KM1: Key Metrics' template, from its Year-End Pillar 3 Disclosures, "
             "reproduced in its row order with its own row numbers, LR2 cross-references and printed precision. "
             "Amounts in £m, ratios as printed. FY2021's leverage figures are on the original CRR basis (inclusive "
             "of claims on central banks) and are shown as a separate block. FY2020-FY2018 are blank: those years' "
             "own sources print the IFRS9-FL comparison template or no Pillar 3 at all, never the UK KM1.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=88,
    source_height=440,
)


ANNUAL = {
    "CET1 Capital": [3085, 2797, 2725, 2948, 2423, 2462, 2331, 2723],
    "CET1 Ratio": ["13.7%", "13.6%", "13.3%", "14.6%", "13.1%", "14.8%", "14.0%", "13.7%"],
    "Tier 1 Capital": [7137, 3580, 3508, 3705, 3180, 3219, 3088, 3480],
    "Tier 1 Ratio": ["31.8%", "17.4%", "17.1%", "18.3%", "17.2%", "19.4%", "18.6%", "17.5%"],
    "Total Capital": [7137, 4171, 4109, 4285, 3709, 3745, 3733, 4152],
    "Total Capital Ratio": ["31.8%", "20.2%", "20.1%", "21.2%", "20.1%", "22.5%", "22.5%", "20.9%"],
    "Total RWAs": [22442, 20605, 20492, 20195, 18436, 16610, 16620, 19868],
    "Leverage Ratio": ["8.4%", "4.5%", "4.7%", "5.4%", "3.5%", "3.7%", "3.8%", None],
    "LCR": ["169%", "168%", "166%", "170%", None, None, None, None],
    "NSFR": ["133%", "138%", "145%", "137%", None, None, None, None],
}
NOTES = {
    "Leverage Ratio": (
        "FY2021's 3.5% is on the original CRR basis (inclusive of claims on central "
        "banks), explicitly confirmed by a footnote in the FY2022 Pillar 3 report. "
        "FY2022 onward are 'excluding claims on central banks' under the revised basis "
        "— a genuine methodology break, not a data error. FY2020's 3.7% and FY2019's "
        "3.8% are each year's own-report figure (CRD IV leverage ratio, on the same "
        "inclusive-of-central-banks basis as FY2021). FY2018 disclosed no leverage "
        "ratio at all — genuinely absent from that year's Annual Report Strategic "
        "Report (its Table 1/Table 2 capital disclosure covers CET1/Tier 1/Total "
        "capital and RWAs only, not leverage)."
    ),
    "NSFR": (
        "FY2021 NSFR was not disclosed at all in that year's Pillar 3 report (the metric "
        "predates this entity's KM1 template). FY2022's 137% was not shown in FY2022's "
        "own report either — recovered from FY2023's own report's FY2022 comparative "
        "column, per this project's standard convention for a metric a bank starts "
        "disclosing only in a later year. FY2018-FY2020 likewise disclose no NSFR at "
        "all — confirmed absent from each year's own Pillar 3 report/xlsx (or, for "
        "FY2018, the Annual Report's own capital disclosure)."
    ),
    "LCR": "FY2021 LCR was not disclosed at all in that year's Pillar 3 report — genuinely absent, not an access "
           "gap. FY2018-FY2020 likewise disclose no LCR at all — confirmed absent from each year's own source.",
    "Total Capital Ratio": (
        "FY2019 and FY2020 both round to 22.5% (FY2019: 22.47%; FY2020: 22.53%) on each "
        "year's own-report figures — a genuine coincidence, not a transcription error."
    ),
}
for name, values in ANNUAL.items():
    unit = "%" if "Ratio" in name or name in {"LCR", "NSFR"} else "£m"
    row = [(name, {y: v for y, v in zip(YEARS, values) if v is not None})]
    bw.add_metric_sheet(name, unit, row, annual_sources("p3"), note=NOTES.get(name), first_col_width=58)
    if name == "Total RWAs":
        # RWA Breakdown - Pillar 3 OV1 template, placed right after Total RWAs
        # per the locked sheet order. All 5 years tie exactly to the Total
        # RWAs figures above. "Memo: Amounts below the thresholds for
        # deduction" is shown as an informational row (not additive to
        # Total) for FY2022-FY2025, matching each year's own OV1 template
        # structure; FY2021's own template additively includes this
        # category within its disclosed Total (18,436 = sum of all 6 rows
        # below including the memo line) - a genuine year-on-year format
        # change in LBCM's own Pillar 3 template, not a data error.
        rwa_breakdown_rows = [
            ("DATA", "Credit risk (excluding CCR)", {"FY2025": 11261, "FY2024": 9582, "FY2023": 9483, "FY2022": 10119, "FY2021": 9026, "FY2020": 8236, "FY2019": 9544, "FY2018": 12890}),
            ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 5675, "FY2024": 5828, "FY2023": 5380, "FY2022": 5515, "FY2021": 4621, "FY2020": 4272, "FY2019": 3779, "FY2018": 3979}),
            ("DATA", "Securitisation exposures in the non-trading/banking book (after the cap)", {"FY2025": 541, "FY2024": 531, "FY2023": 544, "FY2022": 498, "FY2021": 446, "FY2020": 558, "FY2019": 504}),
            ("DATA", "Position, foreign exchange and commodities risks (Market risk)", {"FY2025": 3667, "FY2024": 3422, "FY2023": 3923, "FY2022": 3133, "FY2021": 2933, "FY2020": 1982, "FY2019": 1588, "FY2018": 1607}),
            ("DATA", "Operational risk", {"FY2025": 1298, "FY2024": 1242, "FY2023": 1162, "FY2022": 930, "FY2021": 855, "FY2020": 952, "FY2019": 1189, "FY2018": 1378}),
            ("DATA", "Memo: Amounts below the thresholds for deduction (subject to 250% risk weight)", {"FY2025": 398, "FY2024": 458, "FY2023": 490, "FY2022": 509, "FY2021": 555, "FY2020": 610, "FY2019": 16, "FY2018": 14}),
            ("TOTAL", "Total", {"FY2025": 22442, "FY2024": 20605, "FY2023": 20492, "FY2022": 20195, "FY2021": 18436, "FY2020": 16610, "FY2019": 16620, "FY2018": 19868}),
        ]
        bw.add_rwa_breakdown_sheet(
            title="Lloyds Bank Corporate Markets plc — RWA Breakdown",
            subtitle="Bank (solo) basis for FY2020-FY2025 (Pillar 3 OV1 template, top-level risk-type categories). "
                     "FY2019 is Group/consolidated basis (own document's own terminology - see FLOOR NOTE / P3 "
                     "source labels), same OV1 template. FY2018 is Group basis, mapped from the Annual Report's own "
                     "Strategic Report Table 2 (a differently-structured, pre-OV1-template RWA table): its "
                     "'Counterparty credit risk' row here combines that table's three separate rows 'Counterparty "
                     "credit risk' (£3,389m) + 'Contributions to the default fund of a central counterparty' "
                     "(£193m) + 'Credit valuation adjustment risk' (£397m) = £3,979m, matching how those three "
                     "components are nested inside the single 'Counterparty credit risk' OV1 row in FY2019 onward. "
                     "FY2018 had no disclosed securitisation RWA category at all (blank, not zero) - all 6 rows "
                     "shown (excluding securitisation) sum exactly to FY2018's own disclosed Total RWA of £19,868m. "
                     "£m.",
            rows=rwa_breakdown_rows,
            sources_text=annual_sources("p3"),
            first_col_width=82,
            source_height=220,
            unit_suffix=" (£m)",
        )

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    annual_sources("p3"),
    per_note={
        "MREL Ratio": (
            "Each year's own Pillar 3 report explicitly states MREL disclosures for this "
            "entity are made via Template TLAC 2 within Lloyds Banking Group plc's own "
            "consolidated Pillar 3 disclosures, not at this solo entity level — the same "
            "not-a-resolution-entity pattern seen at RBS plc/Coutts & Company/several HSBC "
            "ring-fenced subsidiaries in this project. Group-level MREL figures are not "
            "substituted here."
        )
    },
)

# Sheet 13: Interim Pillar 3
INTERIM_URLS = {
    "2025-Q1": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2025/q1/2025-lbcm-q1-pillar-3.pdf",
    "2025-H1": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2025/q2/2025-lbcm-hy-pillar-3.pdf",
    "2025-Q3": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2025/q3/2025-lbcm-q3-pillar-3.pdf",
    "2024-Q1": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2024/q1/2024-lbcm-q1-pillar-3.pdf",
    "2024-H1": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2024/q2/2024-lbcm-hy-pillar-3.pdf",
    "2024-Q3": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2024/q3/2024-lbcm-q3-pillar-3.pdf",
    "2023-Q1": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2023/q1/2023-lbcm-q1-pillar-3.pdf",
    "2023-H1": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2023/q2/2023-lbcm-hy-pillar-3.pdf",
    "2023-Q3": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2023/q3/2023-lbcm-q3-pillar-3.pdf",
    "2022-Q1": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2022/q1/2022-lbcm-q1-pillar-3.pdf",
    "2022-H1": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2022/half-year/2022-lbcm-hy-pillar-3.pdf",
    "2022-Q3": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2022/q3/2022-lbcm-q3-pillar-3.pdf",
}
# Only H1 (half-year) reports publish the full KM1 table (CET1/Tier 1/Total
# Capital amounts and ratios, plus NSFR). Q1/Q3 reports publish only LR2
# (leverage), OV1 (RWA) and LIQ1 (LCR) — a genuine, source-confirmed scope
# difference from Lloyds Bank plc's own quarterly disclosures, not a gap in
# this project's research. The Q1/Q3 2022 reports additionally omit the
# leverage template entirely (it wasn't yet part of LBCM's quarterly
# disclosure set); NSFR first appears in the Dec-2022 comparative column of
# the 2023-H1 report. No interim (non-year-end) Pillar 3 disclosures exist
# for LBCM in 2021 (confirmed: every 2021 interim URL pattern 404s).
INTERIM_VALUES = {
    "2025-Q1": [None, None, None, 21775, None, None, None, 81263, "4.4%", "166%", None],
    "2025-H1": [2971, 6950, 6950, 22419, "13.3%", "31.0%", "31.0%", 84779, "8.2%", "167%", "132%"],
    "2025-Q3": [None, None, None, 23391, None, None, None, 86981, "8.0%", "168%", None],
    "2024-Q1": [None, None, None, 20805, None, None, None, 76908, "4.6%", "167%", None],
    "2024-H1": [2908, 3691, 4283, 21204, "13.7%", "17.4%", "20.2%", 78930, "4.7%", "168%", "145%"],
    "2024-Q3": [None, None, None, 21229, None, None, None, 79004, "4.4%", "165%", None],
    "2023-Q1": [None, None, None, 20597, None, None, None, 75981, "4.9%", "171%", None],
    "2023-H1": [3055, 3812, 4380, 21079, "14.5%", "18.1%", "20.8%", 76243, "5.0%", "167%", "139%"],
    "2023-Q3": [None, None, None, 21460, None, None, None, 80485, "4.7%", "165%", None],
    "2022-Q1": [None, None, None, 20326, None, None, None, None, None, "166%", None],
    "2022-H1": [2588, 3345, 3941, 20572, "12.6%", "16.3%", "19.2%", 74898, "4.5%", "168%", None],
    "2022-Q3": [None, None, None, 22093, None, None, None, None, None, "169%", None],
}
INTERIM_METRICS = [
    ("CET1 capital", "£m"), ("Tier 1 capital", "£m"), ("Total capital", "£m"),
    ("Total risk-weighted exposure amount", "£m"), ("CET1 ratio", "%"),
    ("Tier 1 ratio", "%"), ("Total capital ratio", "%"),
    ("Total exposure measure excluding claims on central banks", "£m"),
    ("Leverage ratio excluding claims on central banks", "%"),
    ("Average liquidity coverage ratio", "%"), ("Average net stable funding ratio", "%"),
]
interim_rows = []
for period, values in INTERIM_VALUES.items():
    for metric_name, unit, value in [(m, u, v) for (m, u), v in zip(INTERIM_METRICS, values)]:
        if value is None:
            continue
        interim_rows.append([period, "Quarterly/interim Pillar 3 disclosure", metric_name, value, unit, "Lloyds Bank Corporate Markets plc Bank (solo) basis", INTERIM_URLS[period], "KM1/LR2/OV1/LIQ1"])
wide_interim_rows = [row[:6] + [INTERIM_URLS[row[0]], row[7]] for row in interim_rows]
bw.add_wide_interim_sheet(
    "Interim Pillar 3",
    rows=wide_interim_rows,
    hyperlink_cells={(i, 6): row[6] for i, row in enumerate(wide_interim_rows)},
    title="Lloyds Bank Corporate Markets plc — Interim Pillar 3",
    subtitle="Quarterly and half-year disclosures, 2022–2025 (Bank solo basis)",
    note=(
        "Official LBCM reports publish limited Pillar 3 disclosures at interim quarter "
        "ends and half-year, on the Bank's own (solo) basis. Only the half-year (H1) "
        "reports include the full KM1 table (CET1/Tier 1/Total Capital and their ratios, "
        "plus NSFR); Q1/Q3 reports disclose only LR2 (leverage), OV1 (total RWA) and LIQ1 "
        "(LCR) — confirmed by direct inspection of each report's table of contents, not an "
        "extraction gap. No leverage template was published in the Q1/Q3 2022 reports "
        "(first appears from the 2022 half-year report onward). NSFR was not disclosed "
        "before the 31 December 2022 comparative shown in the 2023 half-year report. No "
        "interim (non-year-end) Pillar 3 disclosures exist for LBCM for 2021 — confirmed "
        "via direct URL-pattern checks against the same archive structure used for "
        "2022–2025, all of which 404."
    ),
)

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 92733, "FY2024": 95003, "FY2023": 90375, "FY2022": 86725, "FY2021": 88821, "FY2020": 92408, "FY2019": 79702, "FY2018": 70434}),
        ("Loans and advances to customers", {"FY2025": 19504, "FY2024": 17524, "FY2023": 16167, "FY2022": 18864, "FY2021": 17176, "FY2020": 18189, "FY2019": 19986, "FY2018": 17036}),
        ("Customer deposits", {"FY2025": 31246, "FY2024": 30945, "FY2023": 29439, "FY2022": 29152, "FY2021": 26553, "FY2020": 25061, "FY2019": 24010, "FY2018": 14180}),
        ("Total equity", {"FY2025": 7558, "FY2024": 3827, "FY2023": 3899, "FY2022": 3432, "FY2021": 3565, "FY2020": 3696, "FY2019": 4375, "FY2018": 3972}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total income (Group)", {"FY2025": 1147, "FY2024": 984, "FY2023": 908, "FY2022": 967, "FY2021": 641, "FY2020": 544, "FY2019": 819, "FY2018": 455}),
        ("Operating expenses (Group)", {"FY2025": -510, "FY2024": -499, "FY2023": -509, "FY2022": -444, "FY2021": -414, "FY2020": -428, "FY2019": -462, "FY2018": -273}),
        ("Profit for the year (Bank)", {"FY2025": 495, "FY2024": 378, "FY2023": 320, "FY2022": 348, "FY2021": 247, "FY2020": 9, "FY2019": 397, "FY2018": 106}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 3827, "FY2024": 3899, "FY2023": 3432, "FY2022": 3565, "FY2021": 3696, "FY2020": 4375, "FY2019": 3972, "FY2018": 20}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": 600, "FY2024": 456, "FY2023": 536, "FY2022": -120, "FY2021": 102, "FY2020": 61, "FY2019": 445, "FY2018": 104}),
        ("Other equity movements, net", {"FY2025": 3131, "FY2024": -528, "FY2023": -69, "FY2022": -13, "FY2021": -233, "FY2020": -740, "FY2019": -42, "FY2018": 3848}),
        ("Closing equity", {"FY2025": 7558, "FY2024": 3827, "FY2023": 3899, "FY2022": 3432, "FY2021": 3565, "FY2020": 3696, "FY2019": 4375, "FY2018": 3972}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash provided by/(used in) operating activities", {"FY2025": -2800, "FY2024": -635, "FY2023": 1288, "FY2022": -4456, "FY2021": -3219, "FY2020": 8161, "FY2019": -3236, "FY2018": 23923}),
        ("Net cash provided by/(used in) investing activities", {"FY2025": -3, "FY2024": -5, "FY2023": 5, "FY2022": 122, "FY2021": 96, "FY2020": 37, "FY2019": 6940, "FY2018": -13057}),
        ("Net cash provided by/(used in) financing activities", {"FY2025": 2372, "FY2024": -586, "FY2023": -117, "FY2022": -46, "FY2021": -249, "FY2020": -763, "FY2019": -81, "FY2018": 4564}),
        ("Cash and cash equivalents at end of year", {"FY2025": 19681, "FY2024": 20633, "FY2023": 20169, "FY2022": 19396, "FY2021": 23038, "FY2020": 26341, "FY2019": 19073, "FY2018": 15450}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {y: v for y, v in zip(YEARS, ANNUAL["CET1 Ratio"])}),
        ("Tier 1 Ratio", {y: v for y, v in zip(YEARS, ANNUAL["Tier 1 Ratio"])}),
        ("Total Capital Ratio", {y: v for y, v in zip(YEARS, ANNUAL["Total Capital Ratio"])}),
        ("Leverage Ratio", {y: v for y, v in zip(YEARS, ANNUAL["Leverage Ratio"])}),
    ],
    note="All figures are Lloyds Bank Corporate Markets plc's own Bank (solo) basis, not the wider Lloyds Banking "
         "Group (FY2018/FY2019 capital ratios are Group/consolidated basis per that year's own source labeling - "
         "see FLOOR NOTE). FY2018 is LBCM's first year of trading (incorporated 28 September 2016 as a dormant "
         "shelf company; no genuine trading floor exists earlier than FY2018) - its 'Other equity movements, net' "
         "row of £3,848m on the Overview reflects one-off initial capitalisation events (capital contribution from "
         "parent, AT1 issuance, share capital issuance) as LBCM went live via the 2018 ring-fencing business "
         "transfer, not a recurring pattern.",
)

bw.save("/Users/armaan/code/katalysis/banks/LLOYDS BANK CORPORATE MARKETS FINANCIALS.xlsx")
print("Saved.")
