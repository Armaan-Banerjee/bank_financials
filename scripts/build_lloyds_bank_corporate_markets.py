import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

AR_URLS = {
    "FY2025": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2025/q4/2025-lbcm-annual-report.pdf",
    "FY2024": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2024/q4/2024-lbcm-annual-report.pdf",
    "FY2023": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2023/q4/2023-lbcm-annual-report.pdf",
    "FY2022": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2022/q4/2022-lbcm-annual-report.pdf",
    "FY2021": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2021/2021-lbcm-annual-report.pdf",
}
P3_URLS = {
    "FY2025": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2025/q4/2025-lbcm-fy-pillar-3.pdf",
    "FY2024": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2024/q4/2024-lbcm-fy-pillar-3.pdf",
    "FY2023": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2023/q4/2023-lbcm-fy-pillar-3.pdf",
    "FY2022": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2022/q4/2022-lbcm-fy-pillar-3.pdf",
    "FY2021": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2021/2021-lbcm-fy-pillar3.pdf",
}
CH_URL = "https://find-and-update.company-information.service.gov.uk/company/10399850"

ENTITY_NOTE = (
    "Entity: Lloyds Bank Corporate Markets plc, company number 10399850, FRN 763256, "
    "LEI 213800MBWEIJDM5CU638. Companies House confirms the active bank company. "
    "This is the non-ring-fenced wholesale/markets entity created as part of Lloyds "
    "Banking Group's 2018 ring-fencing restructuring, DISTINCT from the ring-fenced "
    "Lloyds Bank plc (FRN 119278, built separately as 'LLOYDS BANK FINANCIALS.xlsx'). "
    "All figures below are the Bank (solo) column, not the Group consolidated column "
    "also shown in each source document."
)


def annual_sources(kind):
    pages = {
        "annual": {"FY2025": 61, "FY2024": 68, "FY2023": 67, "FY2022": 63, "FY2021": 36},
        "p3": {"FY2025": 4, "FY2024": 4, "FY2023": 4, "FY2022": 5, "FY2021": 5},
    }[kind]
    urls = AR_URLS if kind == "annual" else P3_URLS
    label = "Annual Report and Accounts, Cash flow statements (Bank column)" if kind == "annual" else "Year-End Pillar 3 disclosure, KM1 Key Metrics (Bank-level)"
    return "\n".join(
        [f"{y}: Lloyds Bank Corporate Markets plc {label}, p.{pages[y]} — {urls[y]}" for y in YEARS]
        + [ENTITY_NOTE, f"Companies House — {CH_URL}"]
    )


bw = BankWorkbook("Lloyds Bank Corporate Markets plc", YEARS, header_color="6A1B9A")

STATEMENTS_SOURCES = (
    "Sources - Lloyds Bank Corporate Markets plc Annual Report and Accounts, Bank (solo) column unless noted:\n"
    f"FY2025/FY2024: Annual Report and Accounts 2025, Consolidated income statement p.57, Statements of comprehensive "
    f"income p.57, Balance sheets p.58, Statements of changes in equity (Bank) p.60 - {AR_URLS['FY2025']}\n"
    f"FY2023/FY2022: Annual Report and Accounts 2023, Consolidated income statement p.63, Statements of comprehensive "
    f"income p.63, Balance sheets p.64, Statements of changes in equity (Bank) p.66 - {AR_URLS['FY2023']}\n"
    f"FY2021: Annual Report and Accounts 2021 (2020 comparative also shown that year), Consolidated income statement "
    f"p.30, Statements of comprehensive income p.31, Balance sheets p.32, Statements of changes in equity (Bank) p.34 "
    f"- {AR_URLS['FY2021']}\n\n"
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
    ("DATA", "Profit before tax", {"FY2025": 583, "FY2024": 468, "FY2023": 399, "FY2022": 436, "FY2021": 293}),
    ("DATA", "Change in operating assets", {"FY2025": 863, "FY2024": -5920, "FY2023": -3331, "FY2022": -1657, "FY2021": 180}),
    ("DATA", "Change in operating liabilities", {"FY2025": -4782, "FY2024": 4619, "FY2023": 3614, "FY2022": -2881, "FY2021": -3502}),
    ("DATA", "Non-cash and other items", {"FY2025": 623, "FY2024": 282, "FY2023": 702, "FY2022": -296, "FY2021": -152}),
    ("DATA", "Tax paid, net", {"FY2025": -87, "FY2024": -84, "FY2023": -96, "FY2022": -58, "FY2021": -38}),
    ("TOTAL", "Net cash provided by/(used in) operating activities", {"FY2025": -2800, "FY2024": -635, "FY2023": 1288, "FY2022": -4456, "FY2021": -3219}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of financial assets", {"FY2024": 0, "FY2023": -3, "FY2022": -27, "FY2021": -85}),
    ("DATA", "Proceeds from sale and maturity of financial assets", {"FY2024": 0, "FY2023": 10, "FY2022": 132, "FY2021": 138}),
    ("DATA", "Purchase of fixed assets", {"FY2025": -3, "FY2024": -2, "FY2023": -2, "FY2022": -5, "FY2021": -1}),
    ("DATA", "Purchase of intangible assets", {"FY2025": 0, "FY2024": -4}),
    ("DATA", "Proceeds from sale of fixed assets", {"FY2025": 0, "FY2024": 1}),
    ("DATA", "Dividends received from subsidiaries", {"FY2022": 22, "FY2021": 44}),
    ("TOTAL", "Net cash provided by/(used in) investing activities", {"FY2025": -3, "FY2024": -5, "FY2023": 5, "FY2022": 122, "FY2021": 96}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividends paid to ordinary shareholders", {"FY2024": -450, "FY2022": -220, "FY2021": -200}),
    ("DATA", "Distributions on other equity instruments", {"FY2025": -210, "FY2024": -78, "FY2023": -80, "FY2022": -43, "FY2021": -33}),
    ("DATA", "Issue of ordinary shares", {"FY2022": 250}),
    ("DATA", "Interest paid on subordinated liabilities", {"FY2025": -24, "FY2024": -54, "FY2023": -58, "FY2022": -25, "FY2021": -16}),
    ("DATA", "Finance leases", {"FY2025": -5, "FY2024": -4, "FY2023": -5, "FY2022": -8}),
    ("DATA", "Proceeds from issue of subordinated liabilities", {"FY2023": 299}),
    ("DATA", "Repayment of subordinated liabilities", {"FY2025": -730, "FY2023": -284}),
    ("DATA", "Loss on repayment of other equity instruments", {"FY2023": -15}),
    ("DATA", "Proceeds from issue of other equity instruments", {"FY2025": 3637, "FY2023": 289}),
    ("DATA", "Repurchases and redemptions of other equity instruments", {"FY2025": -296, "FY2023": -263}),
    ("TOTAL", "Net cash provided by/(used in) financing activities", {"FY2025": 2372, "FY2024": -586, "FY2023": -117, "FY2022": -46, "FY2021": -249}),
    ("DATA", "Effect of exchange rate changes on cash and cash equivalents", {"FY2025": -521, "FY2024": 116, "FY2023": -403, "FY2022": 693, "FY2021": 69}),
    ("TOTAL", "Change in cash and cash equivalents", {"FY2025": -952, "FY2024": -1110, "FY2023": 773, "FY2022": -3687, "FY2021": -3303}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 20633, "FY2024": 21743, "FY2023": 19396, "FY2022": 23083, "FY2021": 26341}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 19681, "FY2024": 20633, "FY2023": 20169, "FY2022": 19396, "FY2021": 23038}),
]

# ---------------------------------------------------------------
# Balance Sheet - equity reconciliation ladder step 1: built first so each
# year's own Total equity is the independent check value for the equity
# sheet below. Bank (solo) basis. All 5 years tie exactly to the equity
# statement's own opening/closing balances below.
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 18941, "FY2024": 20308, "FY2023": 20201, "FY2022": 19382, "FY2021": 22140}),
    ("DATA", "Financial assets at fair value through profit or loss", {"FY2025": 25855, "FY2024": 25620, "FY2023": 21847, "FY2022": 14642, "FY2021": 22268}),
    ("DATA", "Derivative financial instruments", {"FY2025": 18314, "FY2024": 22416, "FY2023": 22606, "FY2022": 24647, "FY2021": 18042}),
    ("DATA", "Loans and advances to banks", {"FY2025": 1006, "FY2024": 1224, "FY2023": 1726, "FY2022": 2063, "FY2021": 2333}),
    ("DATA", "Loans and advances to customers", {"FY2025": 19504, "FY2024": 17524, "FY2023": 16167, "FY2022": 18864, "FY2021": 17176}),
    ("DATA", "Reverse repurchase agreements", {"FY2025": 7024, "FY2024": 5332, "FY2023": 6020, "FY2022": 5606, "FY2021": 5044}),
    ("DATA", "Debt securities", {"FY2025": 379, "FY2024": 336, "FY2023": 374, "FY2022": 305, "FY2021": 229}),
    ("DATA", "Due from fellow Lloyds Banking Group undertakings", {"FY2025": 641, "FY2024": 642, "FY2023": 629, "FY2022": 593, "FY2021": 862}),
    ("TOTAL", "Financial assets at amortised cost", {"FY2025": 28554, "FY2024": 25058, "FY2023": 24916, "FY2022": 27431, "FY2021": 25644}),
    ("DATA", "Financial assets at fair value through other comprehensive income", {"FY2023": 0, "FY2022": 6, "FY2021": 100}),
    ("DATA", "Property, plant and equipment", {"FY2023": 38, "FY2022": 45, "FY2021": 53}),
    ("DATA", "Current tax recoverable", {"FY2025": 9, "FY2024": 4, "FY2023": 10, "FY2022": 2, "FY2021": 14}),
    ("DATA", "Deferred tax assets", {"FY2025": 51, "FY2024": 101, "FY2023": 128, "FY2022": 226, "FY2021": 40}),
    ("DATA", "Investment in subsidiary undertakings", {"FY2025": 143, "FY2024": 168, "FY2023": 180, "FY2022": 180, "FY2021": 203}),
    ("DATA", "Other assets", {"FY2025": 866, "FY2024": 1328, "FY2023": 449, "FY2022": 164, "FY2021": 317}),
    ("TOTAL", "Total assets", {"FY2025": 92733, "FY2024": 95003, "FY2023": 90375, "FY2022": 86725, "FY2021": 88821}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks", {"FY2025": 2214, "FY2024": 2645, "FY2023": 2078, "FY2022": 2456, "FY2021": 3821}),
    ("DATA", "Customer deposits", {"FY2025": 31246, "FY2024": 30945, "FY2023": 29439, "FY2022": 29152, "FY2021": 26553}),
    ("DATA", "Repurchase agreements at amortised cost", {"FY2025": 1002, "FY2024": 0, "FY2023": 1, "FY2022": 7, "FY2021": 1019}),
    ("DATA", "Due to fellow Lloyds Banking Group undertakings", {"FY2025": 603, "FY2024": 1560, "FY2023": 1256, "FY2022": 1526, "FY2021": 3920}),
    ("DATA", "Financial liabilities at fair value through profit or loss", {"FY2025": 24182, "FY2024": 22981, "FY2023": 19686, "FY2022": 12578, "FY2021": 16582}),
    ("DATA", "Derivative financial instruments (liability)", {"FY2025": 12432, "FY2024": 16588, "FY2023": 17576, "FY2022": 20070, "FY2021": 15571}),
    ("DATA", "Debt securities in issue at amortised cost", {"FY2025": 12583, "FY2024": 15090, "FY2023": 15378, "FY2022": 16131, "FY2021": 16644}),
    ("DATA", "Other liabilities", {"FY2025": 885, "FY2024": 600, "FY2023": 280, "FY2022": 558, "FY2021": 444}),
    ("DATA", "Current tax liabilities", {"FY2025": 18, "FY2024": 11, "FY2023": 12, "FY2022": 29, "FY2021": 8}),
    ("DATA", "Deferred tax liabilities", {"FY2021": 0}),
    ("DATA", "Provisions", {"FY2025": 10, "FY2024": 10, "FY2023": 15, "FY2022": 25, "FY2021": 10}),
    ("DATA", "Subordinated liabilities", {"FY2025": 0, "FY2024": 746, "FY2023": 755, "FY2022": 761, "FY2021": 684}),
    ("TOTAL", "Total liabilities", {"FY2025": 85175, "FY2024": 91176, "FY2023": 86476, "FY2022": 83293, "FY2021": 85256}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 370, "FY2024": 370, "FY2023": 370, "FY2022": 370, "FY2021": 120}),
    ("DATA", "Other reserves", {"FY2025": -131, "FY2024": -236, "FY2023": -314, "FY2022": -530, "FY2021": -62}),
    ("DATA", "Retained profits", {"FY2025": 3174, "FY2024": 2885, "FY2023": 3035, "FY2022": 2810, "FY2021": 2725}),
    ("TOTAL", "Ordinary shareholders' equity", {"FY2025": 3413, "FY2024": 3019, "FY2023": 3091, "FY2022": 2650, "FY2021": 2783}),
    ("DATA", "Other equity instruments", {"FY2025": 4145, "FY2024": 808, "FY2023": 808, "FY2022": 782, "FY2021": 782}),
    ("TOTAL", "Total equity", {"FY2025": 7558, "FY2024": 3827, "FY2023": 3899, "FY2022": 3432, "FY2021": 3565}),
    ("TOTAL", "Total equity and liabilities", {"FY2025": 92733, "FY2024": 95003, "FY2023": 90375, "FY2022": 86725, "FY2021": 88821}),
]

bw.add_balance_sheet_sheet(
    title="Lloyds Bank Corporate Markets plc — Balance Sheet",
    subtitle="Bank (solo) basis. £m. FY2021-FY2023 show a standalone 'Property, plant and equipment' line and a "
              "'Financial assets at fair value through other comprehensive income' line, both since folded into "
              "'Other assets' from FY2024 onward (a genuine structural simplification, not a data gap).",
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
    ("DATA", "Interest income", {"FY2025": 2424, "FY2024": 2759, "FY2023": 2696, "FY2022": 1087, "FY2021": 356}),
    ("DATA", "Interest expense", {"FY2025": -1981, "FY2024": -2593, "FY2023": -2498, "FY2022": -812, "FY2021": -169}),
    ("TOTAL", "Net interest income", {"FY2025": 443, "FY2024": 166, "FY2023": 198, "FY2022": 275, "FY2021": 187}),
    ("DATA", "Fee and commission income", {"FY2025": 329, "FY2024": 321, "FY2023": 303, "FY2022": 228, "FY2021": 248}),
    ("DATA", "Fee and commission expense", {"FY2025": -58, "FY2024": -53, "FY2023": -39, "FY2022": -36, "FY2021": -27}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 271, "FY2024": 268, "FY2023": 264, "FY2022": 192, "FY2021": 221}),
    ("DATA", "Net trading income", {"FY2025": 472, "FY2024": 552, "FY2023": 442, "FY2022": 495, "FY2021": 244}),
    ("DATA", "Other operating income/(expense)", {"FY2025": -39, "FY2024": -2, "FY2023": 4, "FY2022": 5, "FY2021": -11}),
    ("TOTAL", "Other income", {"FY2025": 704, "FY2024": 818, "FY2023": 710, "FY2022": 692, "FY2021": 454}),
    ("TOTAL", "Total income", {"FY2025": 1147, "FY2024": 984, "FY2023": 908, "FY2022": 967, "FY2021": 641}),
    ("DATA", "Operating expenses", {"FY2025": -510, "FY2024": -499, "FY2023": -509, "FY2022": -444, "FY2021": -414}),
    ("DATA", "Impairment (charge)/credit", {"FY2025": -1, "FY2024": 16, "FY2023": 28, "FY2022": -46, "FY2021": 62}),
    ("TOTAL", "Profit before tax (Group)", {"FY2025": 636, "FY2024": 501, "FY2023": 427, "FY2022": 477, "FY2021": 289}),
    ("DATA", "Tax expense (Group)", {"FY2025": -95, "FY2024": -97, "FY2023": -89, "FY2022": -97, "FY2021": -51}),
    ("TOTAL", "Profit for the year (Group)", {"FY2025": 541, "FY2024": 404, "FY2023": 338, "FY2022": 380, "FY2021": 238}),
    ("TOTAL", "Profit for the year (Bank)", {"FY2025": 495, "FY2024": 378, "FY2023": 320, "FY2022": 348, "FY2021": 247}),
    ("SECTION", "Other comprehensive income, net of tax (Bank column, ties to Statement of Changes in Equity)", {}),
    ("DATA", "Movements in revaluation reserve (FVOCI debt securities), net of tax", {"FY2023": 2, "FY2022": 0}),
    ("DATA", "Movements in cash flow hedging reserve, net of tax", {"FY2025": 128, "FY2024": 70, "FY2023": 230, "FY2022": -471, "FY2021": -153}),
    ("DATA", "Movements in foreign currency translation reserve, net of tax", {"FY2025": -23, "FY2024": 8, "FY2023": -16, "FY2022": 3, "FY2021": 4}),
    ("TOTAL", "Total other comprehensive income/(loss), net of tax (Bank)", {"FY2025": 105, "FY2024": 78, "FY2023": 216, "FY2022": -468, "FY2021": -145}),
    ("TOTAL", "Total comprehensive income/(loss) for the year (Bank)", {"FY2025": 600, "FY2024": 456, "FY2023": 536, "FY2022": -120, "FY2021": 102}),
]

bw.add_income_statement_sheet(
    title="Lloyds Bank Corporate Markets plc — Profit & Loss",
    subtitle="Income statement is Group consolidated (LBCM publishes no separate Bank-solo income statement line "
              "items - see BASIS NOTE in the source citation). The Bank's own bottom-line 'Profit for the year' and "
              "OCI/total comprehensive income rows are the Bank-column aggregate figures, matching the Statement of "
              "Changes in Equity. £m.",
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
    subtitle="Chronological roll-forward, oldest to newest, Bank (solo) basis. £m. Equity reconciliation ladder "
              "confirmed: every year's own closing balance ties exactly to both the next year's own opening balance "
              "and that year's own Balance Sheet Total equity - zero plug rows needed anywhere across all 5 years. "
              "FY2022's own AR2023 comparative provides the FY2021 closing/FY2022 opening balance shown as the first "
              "row here.",
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
    "in either source document. FY2024→FY2025 and FY2022→FY2023 both tie exactly."
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
    ("SECTION", "Loans and advances to customers, by IFRS 9 stage (Bank, FY2022-FY2025; Group combined with reverse repos, FY2021)", {}),
    ("DATA", "Stage 1 (gross)", {"FY2025": 19322, "FY2024": 17428, "FY2023": 15996, "FY2022": 17851, "FY2021": 21874}),
    ("DATA", "Stage 2 (gross)", {"FY2025": 184, "FY2024": 96, "FY2023": 180, "FY2022": 1029, "FY2021": 47}),
    ("DATA", "Stage 3 (gross)", {"FY2025": 6, "FY2024": 7, "FY2023": 9, "FY2022": 22, "FY2021": 29}),
    ("TOTAL", "Total gross carrying amount", {"FY2025": 19512, "FY2024": 17531, "FY2023": 16185, "FY2022": 18902, "FY2021": 21950}),
    ("DATA", "Allowance for expected credit losses", {"FY2025": -8, "FY2024": -7, "FY2023": -18, "FY2022": -38, "FY2021": -10}),
    ("TOTAL", "Net carrying amount", {"FY2025": 19504, "FY2024": 17524, "FY2023": 16167, "FY2022": 18864, "FY2021": 21940}),
    ("DATA", "Stage 3 as % of total gross carrying amount (NPL ratio)", {"FY2025": "0.03%", "FY2024": "0.04%", "FY2023": "0.06%", "FY2022": "0.12%", "FY2021": "0.13%"}),
    ("DATA", "ECL allowance as % of total gross carrying amount (coverage)", {"FY2025": "0.04%", "FY2024": "0.04%", "FY2023": "0.11%", "FY2022": "0.20%", "FY2021": "0.05%"}),
]

bw.add_asset_quality_sheet(
    title="Lloyds Bank Corporate Markets plc — Asset Quality",
    subtitle="Loans and advances to customers, IFRS 9 stage 1/2/3 split. £m.",
    rows=asset_quality_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nFY2025/FY2024: Annual Report and Accounts 2025, Note 14 'Loans and advances to customers' (Bank table), "
        "p.87. FY2023/FY2022: Annual Report and Accounts 2023, Note 12 'Loans and advances to customers' (Bank "
        "table), p.83. FY2021: Annual Report and Accounts 2021, Note 13 'Financial assets at amortised cost', "
        "'Loans and advances to customers and reverse repurchase agreements' table, p.59-60.\n\n"
        "DATA QUALITY FLAG: FY2021's own report discloses this stage split only at Group level, and only as a "
        "combined 'Loans and advances to customers and reverse repurchase agreements' category (Total gross carrying "
        "amount 21,950; Net carrying amount 21,940), unlike FY2022-FY2025's Bank-level tables which cover loans and "
        "advances to customers ALONE - a genuine structural/disclosure difference, not a transcription error. "
        "FY2021's Net carrying amount therefore does NOT tie to FY2021's Bank Balance Sheet 'Loans and advances to "
        "customers' line (17,176) the way FY2022-FY2025 do - shown as originally disclosed rather than adjusted to "
        "force a tie."
    ),
    first_col_width=90,
    source_height=340,
    unit_suffix=" (£m)",
)

ANNUAL = {
    "CET1 Capital": [3085, 2797, 2725, 2948, 2423],
    "CET1 Ratio": ["13.7%", "13.6%", "13.3%", "14.6%", "13.1%"],
    "Tier 1 Capital": [7137, 3580, 3508, 3705, 3180],
    "Tier 1 Ratio": ["31.8%", "17.4%", "17.1%", "18.3%", "17.2%"],
    "Total Capital": [7137, 4171, 4109, 4285, 3709],
    "Total Capital Ratio": ["31.8%", "20.2%", "20.1%", "21.2%", "20.1%"],
    "Total RWAs": [22442, 20605, 20492, 20195, 18436],
    "Leverage Ratio": ["8.4%", "4.5%", "4.7%", "5.4%", "3.5%"],
    "LCR": ["169%", "168%", "166%", "170%", None],
    "NSFR": ["133%", "138%", "145%", "137%", None],
}
NOTES = {
    "Leverage Ratio": (
        "FY2021's 3.5% is on the original CRR basis (inclusive of claims on central "
        "banks), explicitly confirmed by a footnote in the FY2022 Pillar 3 report. "
        "FY2022 onward are 'excluding claims on central banks' under the revised basis "
        "— a genuine methodology break, not a data error."
    ),
    "NSFR": (
        "FY2021 NSFR was not disclosed at all in that year's Pillar 3 report (the metric "
        "predates this entity's KM1 template). FY2022's 137% was not shown in FY2022's "
        "own report either — recovered from FY2023's own report's FY2022 comparative "
        "column, per this project's standard convention for a metric a bank starts "
        "disclosing only in a later year."
    ),
    "LCR": "FY2021 LCR was not disclosed at all in that year's Pillar 3 report — genuinely absent, not an access gap.",
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
            ("DATA", "Credit risk (excluding CCR)", {"FY2025": 11261, "FY2024": 9582, "FY2023": 9483, "FY2022": 10119, "FY2021": 9026}),
            ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 5675, "FY2024": 5828, "FY2023": 5380, "FY2022": 5515, "FY2021": 4621}),
            ("DATA", "Securitisation exposures in the non-trading/banking book (after the cap)", {"FY2025": 541, "FY2024": 531, "FY2023": 544, "FY2022": 498, "FY2021": 446}),
            ("DATA", "Position, foreign exchange and commodities risks (Market risk)", {"FY2025": 3667, "FY2024": 3422, "FY2023": 3923, "FY2022": 3133, "FY2021": 2933}),
            ("DATA", "Operational risk", {"FY2025": 1298, "FY2024": 1242, "FY2023": 1162, "FY2022": 930, "FY2021": 855}),
            ("DATA", "Memo: Amounts below the thresholds for deduction (subject to 250% risk weight)", {"FY2025": 398, "FY2024": 458, "FY2023": 490, "FY2022": 509, "FY2021": 555}),
            ("TOTAL", "Total", {"FY2025": 22442, "FY2024": 20605, "FY2023": 20492, "FY2022": 20195, "FY2021": 18436}),
        ]
        bw.add_rwa_breakdown_sheet(
            title="Lloyds Bank Corporate Markets plc — RWA Breakdown",
            subtitle="Bank (solo) basis, Pillar 3 OV1 template (top-level risk-type categories). £m.",
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
        ("Total assets", {"FY2025": 92733, "FY2024": 95003, "FY2023": 90375, "FY2022": 86725, "FY2021": 88821}),
        ("Loans and advances to customers", {"FY2025": 19504, "FY2024": 17524, "FY2023": 16167, "FY2022": 18864, "FY2021": 17176}),
        ("Customer deposits", {"FY2025": 31246, "FY2024": 30945, "FY2023": 29439, "FY2022": 29152, "FY2021": 26553}),
        ("Total equity", {"FY2025": 7558, "FY2024": 3827, "FY2023": 3899, "FY2022": 3432, "FY2021": 3565}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total income (Group)", {"FY2025": 1147, "FY2024": 984, "FY2023": 908, "FY2022": 967, "FY2021": 641}),
        ("Operating expenses (Group)", {"FY2025": -510, "FY2024": -499, "FY2023": -509, "FY2022": -444, "FY2021": -414}),
        ("Profit for the year (Bank)", {"FY2025": 495, "FY2024": 378, "FY2023": 320, "FY2022": 348, "FY2021": 247}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 3827, "FY2024": 3899, "FY2023": 3432, "FY2022": 3565, "FY2021": 3696}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": 600, "FY2024": 456, "FY2023": 536, "FY2022": -120, "FY2021": 102}),
        ("Other equity movements, net", {"FY2025": 3131, "FY2024": -528, "FY2023": -69, "FY2022": -13, "FY2021": -233}),
        ("Closing equity", {"FY2025": 7558, "FY2024": 3827, "FY2023": 3899, "FY2022": 3432, "FY2021": 3565}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash provided by/(used in) operating activities", {"FY2025": -2800, "FY2024": -635, "FY2023": 1288, "FY2022": -4456, "FY2021": -3219}),
        ("Net cash provided by/(used in) investing activities", {"FY2025": -3, "FY2024": -5, "FY2023": 5, "FY2022": 122, "FY2021": 96}),
        ("Net cash provided by/(used in) financing activities", {"FY2025": 2372, "FY2024": -586, "FY2023": -117, "FY2022": -46, "FY2021": -249}),
        ("Cash and cash equivalents at end of year", {"FY2025": 19681, "FY2024": 20633, "FY2023": 20169, "FY2022": 19396, "FY2021": 23038}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {y: v for y, v in zip(YEARS, ANNUAL["CET1 Ratio"])}),
        ("Tier 1 Ratio", {y: v for y, v in zip(YEARS, ANNUAL["Tier 1 Ratio"])}),
        ("Total Capital Ratio", {y: v for y, v in zip(YEARS, ANNUAL["Total Capital Ratio"])}),
        ("Leverage Ratio", {y: v for y, v in zip(YEARS, ANNUAL["Leverage Ratio"])}),
    ],
    note="All figures are Lloyds Bank Corporate Markets plc's own Bank (solo) basis, not the wider Lloyds Banking Group.",
)

bw.save("/Users/armaan/code/katalysis/banks/LLOYDS BANK CORPORATE MARKETS FINANCIALS.xlsx")
print("Saved.")
