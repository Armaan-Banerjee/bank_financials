import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

AR_URLS = {
    "FY2025": "https://oaknorth.co.uk/wp-content/uploads/2026/03/Annual_Report_2025.pdf",
    "FY2024": "https://oaknorth.co.uk/wp-content/uploads/2025/03/Annual_Report_2024.pdf",
    "FY2023": "https://oaknorth.co.uk/wp-content/uploads/2024/03/OakNorth_Annual_Report_2023.pdf",
    "FY2022": "https://oaknorth.co.uk/wp-content/uploads/2023/03/OakNorth-Annual-Report-2022.pdf",
    "FY2021": "https://www.oaknorth.co.uk/wp-content/uploads/2022/03/OakNorth-Bank-Annual-Report-2021.pdf",
}
P3_URLS = {
    "FY2025": "https://oaknorth.co.uk/wp-content/uploads/2026/04/Pillar-3-Disclosures-OakNorth-Bank-Plc-2025-1.pdf",
    "FY2024": "https://oaknorth.co.uk/wp-content/uploads/2025/05/Pillar-3-Disclosures-OakNorth-Bank-Plc-2024.pdf",
    "FY2023": "https://oaknorth.co.uk/wp-content/uploads/2024/05/Pillar-3-Disclosure-OakNorth-Bank-Plc-2023.pdf",
    "FY2022": "https://oaknorth.co.uk/wp-content/uploads/2023/05/Pillar-3-disclosures-2022_Final.pdf",
    "FY2021": "https://oaknorth.co.uk/wp-content/uploads/2022/07/OakNorth_Pillar-3_2021.pdf",
}


def cash_flow_sources():
    return (
        "Sources — OakNorth Bank plc cash flows, £'000. FY2025: OakNorth Bank Plc Annual Report 2025, "
        f"pp.102-103 (Statement of cash flows) — {AR_URLS['FY2025']}\n"
        f"FY2024: Annual Report 2024, pp.94-95 — {AR_URLS['FY2024']}\n"
        f"FY2023: Annual Report 2023, pp.87-88 — {AR_URLS['FY2023']}\n"
        f"FY2022: Annual Report 2022, pp.106-107 — {AR_URLS['FY2022']}\n"
        f"FY2021: Annual Report 2021, p.87 — {AR_URLS['FY2021']}\n"
        "The 2022–2025 reports present both Bank Group and standalone Bank columns; this sheet uses the Bank Group "
        "column for those years. The 2021 report predates the ASK Partners consolidation and presents OakNorth Bank "
        "plc standalone figures, which are used for FY2021. Blank cells mean the line was not separately disclosed "
        "under that year's presentation; they are not zeros."
    )


def p3_sources():
    return (
        "Sources — OakNorth Bank Pillar 3 disclosures, £'000 unless percentages are shown. FY2025: UK KM1 p.14 "
        f"and OV1 p.15 — {P3_URLS['FY2025']}\n"
        f"FY2024: UK KM1 pp.16-17 — {P3_URLS['FY2024']}\n"
        f"FY2023: UK KM1 p.6 and capital adequacy p.10 — {P3_URLS['FY2023']}\n"
        f"FY2022: capital metrics pp.19-23 — {P3_URLS['FY2022']}\n"
        f"FY2021: regulatory capital and leverage pp.11-15 — {P3_URLS['FY2021']}\n"
        "The 2025 disclosure states that the prudential disclosures are on a consolidated Bank Group basis, while "
        "the 2022–2024 reports describe the relevant regulatory templates as solo/Bank basis. The 2021 figures are "
        "the standalone Bank figures."
    )


bw = BankWorkbook("OakNorth Bank plc", YEARS, header_color="6B8E23")

STATEMENTS_SOURCES = (
    "Sources - OakNorth Bank plc consolidated financial statements, £'000, Bank Group basis (Bank standalone "
    "for FY2021 - see basis note below):\n"
    f"FY2025/FY2024: Annual Report 2025, Consolidated Statement of Profit or Loss p.94, Consolidated Statement "
    f"of Comprehensive Income p.95, Consolidated Balance Sheet pp.96-97, Consolidated Statement of Changes in "
    f"Equity p.100 - {AR_URLS['FY2025']}\n"
    f"FY2023: Annual Report 2024, Consolidated Statement of Profit & Loss p.86, Consolidated Statement of "
    f"Comprehensive Income p.87, Consolidated Balance Sheet pp.88-89, Consolidated Statement of Changes in "
    f"Equity p.92 (FY2023 own-year column) - {AR_URLS['FY2024']}\n"
    f"FY2022: Annual Report 2023, Consolidated Statement of Profit & Loss and Comprehensive Income pp.79-80, "
    f"Consolidated Balance Sheet pp.81-82, Consolidated Statement of Changes in Equity p.85 (FY2022 own-year "
    f"column) - {AR_URLS['FY2023']}\n"
    f"FY2021: Annual Report 2022, Consolidated Statement of Profit and Loss and Comprehensive Income p.99, "
    f"Consolidated Balance Sheet pp.100-101, Consolidated Statement of Changes in Equity p.104 (2021 IFRS "
    f"Restated column and 1 Jan 2021 opening) - {AR_URLS['FY2022']}\n\n"
    "BASIS NOTE: OakNorth Bank plc transitioned from FRS 102 to UK-adopted IAS (IFRS) with effect from the year "
    "ended 31 December 2022 (Annual Report 2022, Note 1.6). FY2021 figures shown throughout the Balance Sheet, "
    "Profit & Loss and Statement of Changes in Equity sheets are the Bank's own officially IFRS-restated FY2021 "
    "comparatives (as republished in the Annual Report 2022), not the originally-reported FRS 102 figures from "
    "the Annual Report 2021 - this is done for comparability with FY2022-FY2025, all of which are prepared under "
    "IFRS. A genuine £470k IFRS transition adjustment (net of tax, to retained earnings) was applied between the "
    "31 December 2021 closing balance and the 1 January 2022 opening balance and is shown as its own explicit "
    "row on the Statement of Changes in Equity sheet, not absorbed into any other line. OakNorth's subsidiary "
    "A.S.K Partners Limited was first consolidated during FY2022 (goodwill and non-controlling interests first "
    "appear that year); FY2021's 'Bank Group' figures are therefore identical to Bank standalone that year. "
    "Balance Sheet/P&L/Equity are Bank Group (consolidated) basis for all 5 years; the Asset Quality sheet is "
    "Bank-standalone (entity-level) basis throughout - see that sheet's own note for the resulting basis "
    "difference against these three sheets' Bank Group loans and advances to customers figure."
)

# ---------------------------------------------------------------
# Balance Sheet - equity reconciliation ladder step 1: built first so each
# year's own Total equity is the independent check value for the equity
# sheet below. All 5 years tie exactly to the equity statement's own
# opening/closing balances and to Total assets = Total liabilities + equity.
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central bank", {"FY2025": 2184464, "FY2024": 2689013, "FY2023": 1637314, "FY2022": 1235711, "FY2021": 446374}),
    ("DATA", "Loans and advances to banks", {"FY2025": 96776, "FY2024": 80632, "FY2023": 38474, "FY2022": 42127, "FY2021": 30019}),
    ("DATA", "Loans and advances to customers", {"FY2025": 4889874, "FY2024": 4393100, "FY2023": 3817344, "FY2022": 3127950, "FY2021": 2886305}),
    ("DATA", "Investment securities / Debt securities", {"FY2025": 599436, "FY2024": 331238, "FY2023": 237660, "FY2022": 204005, "FY2021": 191849}),
    ("DATA", "Derivative assets held for risk management", {"FY2025": 33742, "FY2024": 2809, "FY2023": 5765, "FY2022": 0}),
    ("DATA", "Goodwill", {"FY2025": 11647, "FY2024": 11647, "FY2023": 11647, "FY2022": 11647}),
    ("DATA", "Intangible assets", {"FY2025": 14238, "FY2024": 8967, "FY2023": 5639, "FY2022": 4293, "FY2021": 28}),
    ("DATA", "Tangible fixed assets", {"FY2025": 116, "FY2024": 79, "FY2023": 51, "FY2022": 305, "FY2021": 484}),
    ("DATA", "Right of use (\"ROU\") assets", {"FY2025": 3202, "FY2024": 2323, "FY2023": 2258, "FY2022": 2557, "FY2021": 0}),
    ("DATA", "Current tax assets", {"FY2025": 785, "FY2024": 4886, "FY2023": 2136, "FY2022": 0}),
    ("DATA", "Deferred tax assets (net)", {"FY2024": 1409, "FY2023": 367, "FY2022": 1012, "FY2021": 872}),
    ("DATA", "Other assets", {"FY2025": 22609, "FY2024": 47056, "FY2023": 51992, "FY2022": 27813, "FY2021": 14380}),
    ("TOTAL", "Total assets", {"FY2025": 7856889, "FY2024": 7573159, "FY2023": 5810647, "FY2022": 4657420, "FY2021": 3570311}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer deposits", {"FY2025": 6513248, "FY2024": 6103046, "FY2023": 4639352, "FY2022": 3613260, "FY2021": 2643603}),
    ("DATA", "Borrowings under BoE facilities (Term Funding Scheme)", {"FY2025": 5031, "FY2024": 202445, "FY2023": 202647, "FY2022": 201423, "FY2021": 200050}),
    ("DATA", "Derivative liabilities held for risk management", {"FY2025": 7898, "FY2024": 14411, "FY2023": 0}),
    ("DATA", "Trade and other payables", {"FY2025": 35558, "FY2024": 22935, "FY2023": 19780, "FY2022": 14619, "FY2021": 23396}),
    ("DATA", "Intercompany borrowings", {"FY2025": 6007, "FY2024": 8345, "FY2023": 11953, "FY2022": 0}),
    ("DATA", "Current tax liabilities", {"FY2025": 745, "FY2024": 58, "FY2023": 0}),
    ("DATA", "Other liabilities", {"FY2025": 30042, "FY2024": 21389, "FY2023": 21644, "FY2022": 33955, "FY2021": 24266}),
    ("DATA", "Deferred tax liabilities (net)", {"FY2025": 2754, "FY2024": 0}),
    ("DATA", "Tier 2 subordinated debt", {"FY2025": 188076, "FY2024": 180949, "FY2023": 30141, "FY2022": 49778, "FY2021": 49678}),
    ("TOTAL", "Total liabilities", {"FY2025": 6789359, "FY2024": 6553578, "FY2023": 4925517, "FY2022": 3913035, "FY2021": 2940993}),
    ("SECTION", "Capital and reserves", {}),
    ("DATA", "Called up share capital", {"FY2025": 389320, "FY2024": 389320, "FY2023": 389320, "FY2022": 389320, "FY2021": 389320}),
    ("DATA", "Share-based payments reserve", {"FY2025": 146, "FY2024": 176, "FY2023": 149, "FY2022": 111, "FY2021": 83}),
    ("DATA", "Retained earnings", {"FY2025": 667507, "FY2024": 625420, "FY2023": 487565, "FY2022": 351208, "FY2021": 239670}),
    ("DATA", "Fair value reserve (FVOCI)", {"FY2025": 25, "FY2024": 8, "FY2023": 56, "FY2022": 24, "FY2021": 245}),
    ("DATA", "Cash flow hedge reserve", {"FY2025": -39, "FY2024": -2785, "FY2023": 2261, "FY2022": 0}),
    ("DATA", "Non-controlling interests", {"FY2025": 10571, "FY2024": 7442, "FY2023": 5835, "FY2022": 3722, "FY2021": 0}),
    ("TOTAL", "Total equity", {"FY2025": 1067530, "FY2024": 1019581, "FY2023": 885130, "FY2022": 744385, "FY2021": 629318}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 7856889, "FY2024": 7573159, "FY2023": 5810647, "FY2022": 4657420, "FY2021": 3570311}),
]

bw.add_balance_sheet_sheet(
    title="OakNorth Bank plc — Balance Sheet",
    subtitle="Bank Group (consolidated) basis, £'000 (FY2021 is the Bank's own officially IFRS-restated comparative - "
              "see basis note below; identical to Bank standalone that year, as its subsidiary was not yet acquired). "
              "Blank cells indicate a line not disclosed that year (0 indicates a line disclosed as nil, not a gap).",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 568469, "FY2024": 568925, "FY2023": 438860, "FY2022": 248605, "FY2021": 188540}),
    ("DATA", "Interest expense", {"FY2025": -287872, "FY2024": -285202, "FY2023": -169664, "FY2022": -47936, "FY2021": -25852}),
    ("TOTAL", "Net interest income", {"FY2025": 280597, "FY2024": 283723, "FY2023": 269196, "FY2022": 200669, "FY2021": 162688}),
    ("DATA", "Fee and commission income", {"FY2025": 37403, "FY2024": 29027, "FY2023": 27410, "FY2022": 20421, "FY2021": 13502}),
    ("DATA", "Net gains/(losses) from financial instruments at FVPL", {"FY2025": 47, "FY2024": -791, "FY2023": 173}),
    ("DATA", "Loss on derecognition of financial instruments at amortised cost", {"FY2024": -2108}),
    ("TOTAL", "Net interest and fee income", {"FY2025": 318047, "FY2024": 309851, "FY2023": 296779, "FY2022": 221090, "FY2021": 176190}),
    ("SECTION", "Operating expenses and provisions", {}),
    ("DATA", "Administrative expenses", {"FY2025": -88007, "FY2024": -93307, "FY2023": -81843, "FY2022": -57105, "FY2021": -44385}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -3572, "FY2024": -2659, "FY2023": -2490, "FY2022": -887, "FY2021": -959}),
    ("DATA", "(Charge)/reversal of provision for credit impairment losses", {"FY2025": -91, "FY2024": 4427, "FY2023": -25113, "FY2022": -10762, "FY2021": 3694}),
    ("DATA", "Charge for provision for other assets", {"FY2025": -3848, "FY2024": -3518, "FY2023": -929}),
    ("TOTAL", "Operating expenses and provisions", {"FY2025": -95518, "FY2024": -95057, "FY2023": -109446, "FY2022": -68754, "FY2021": -41650}),
    ("TOTAL", "Profit before tax", {"FY2025": 222529, "FY2024": 214794, "FY2023": 187333, "FY2022": 152336, "FY2021": 134540}),
    ("DATA", "Taxation", {"FY2025": -57318, "FY2024": -55460, "FY2023": -48863, "FY2022": -39077, "FY2021": -34148}),
    ("TOTAL", "Profit for the year", {"FY2025": 165211, "FY2024": 159334, "FY2023": 138470, "FY2022": 113259, "FY2021": 100392}),
    ("SECTION", "Other comprehensive income/(expense), net of tax", {}),
    ("DATA", "Fair value changes on financial assets at FVOCI", {"FY2025": 17, "FY2024": -48, "FY2023": 32, "FY2022": -221, "FY2021": 245}),
    ("DATA", "Changes in cash flow hedge reserve", {"FY2025": 2746, "FY2024": -5046, "FY2023": 2261}),
    ("DATA", "Changes in cost of hedging reserve", {"FY2024": 56, "FY2023": -56}),
    ("TOTAL", "Total other comprehensive income/(expense) for the year", {"FY2025": 2763, "FY2024": -5038, "FY2023": 2237, "FY2022": -221, "FY2021": 245}),
    ("TOTAL", "Total comprehensive income for the year", {"FY2025": 167974, "FY2024": 154296, "FY2023": 140707, "FY2022": 113038, "FY2021": 100637}),
]

bw.add_income_statement_sheet(
    title="OakNorth Bank plc — Profit & Loss",
    subtitle="Bank Group (consolidated) basis, £'000 (FY2021 is the Bank's own officially IFRS-restated comparative - "
              "see basis note below). FY2025's own presentation combines 'Net gains/(losses) from financial "
              "instruments at FVPL' and 'Loss on derecognition of financial instruments at amortised cost' into a "
              "single 'Other gains/(losses) from financial instruments' line (£47k) - shown here in the FVPL row for "
              "comparability, since no derecognition loss was separately disclosed that year.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - per-year reconciliation ladder confirmed:
# every year's own closing balance ties exactly to both the next year's own
# opening balance and that year's own Balance Sheet Total equity. Zero plug
# rows needed anywhere across all 5 years, once the bank's own genuine £470k
# IFRS transition adjustment (FRS 102 -> IFRS, effective FY2022) is shown as
# its own explicit row rather than absorbed elsewhere.
# ---------------------------------------------------------------
equity_headers = ["Called up Share Capital", "Retained earnings", "Fair value reserve (FVOCI)",
                   "Cash flow hedge reserve", "Cost of hedging reserve", "Share-based payments reserve",
                   "Non-controlling interests", "Total equity"]
equity_rows = [
    ("TOTAL", "At 1 January 2021 (FY2021 opening)", (389320, 139278, None, None, None, 79, None, 528677)),
    ("DATA", "Profit for the year", (None, 100392, None, None, None, None, None, 100392)),
    ("DATA", "Other comprehensive income for the year (FVOCI)", (None, None, 245, None, None, None, None, 245)),
    ("DATA", "Employee share-based payments", (None, None, None, None, None, 4, None, 4)),
    ("TOTAL", "At 31 December 2021 (FY2021 closing, IFRS restated)", (389320, 239670, 245, None, None, 83, None, 629318)),
    ("DATA", "IFRS transition adjustment, net of tax (FRS 102 -> IFRS, Note 1.6)", (None, -470, None, None, None, None, None, -470)),
    ("TOTAL", "At 1 January 2022 (FY2022 opening, IFRS restated)", (389320, 239200, 245, None, None, 83, None, 628848)),
    ("DATA", "Non-controlling interest on acquisition of subsidiary", (None, None, None, None, None, None, 2593, 2593)),
    ("DATA", "Profit for the year", (None, 112069, None, None, None, None, 1190, 113259)),
    ("DATA", "Other comprehensive expense for the year (FVOCI)", (None, None, -221, None, None, None, None, -221)),
    ("DATA", "Employee share-based payments", (None, None, None, None, None, 28, None, 28)),
    ("DATA", "Unwinding of investment in A.S.K entities", (None, -61, None, None, None, None, -61, -122)),
    ("TOTAL", "At 31 December 2022 (FY2022 closing)", (389320, 351208, 24, None, None, 111, 3722, 744385)),
    ("DATA", "Profit for the year", (None, 136357, None, None, None, None, 2113, 138470)),
    ("DATA", "Other comprehensive income for the year", (None, None, 32, 2261, -56, None, None, 2237)),
    ("DATA", "Employee share-based payments", (None, None, None, None, None, 38, None, 38)),
    ("TOTAL", "At 31 December 2023 (FY2023 closing)", (389320, 487565, 56, 2261, -56, 149, 5835, 885130)),
    ("DATA", "Profit for the year", (None, 157823, None, None, None, None, 1511, 159334)),
    ("DATA", "Other comprehensive (expense)/income for the year", (None, None, -48, -5046, 56, None, None, -5038)),
    ("DATA", "Employee share-based payments", (None, None, None, None, None, 27, None, 27)),
    ("DATA", "Issue of growth shares", (None, None, None, None, None, None, 64, 64)),
    ("DATA", "Payment of dividend to parent", (None, -20000, None, None, None, None, None, -20000)),
    ("DATA", "Unwinding of investments in A.S.K Group entities", (None, 32, None, None, None, None, 32, 64)),
    ("TOTAL", "At 31 December 2024 (FY2024 closing)", (389320, 625420, 8, -2785, None, 176, 7442, 1019581)),
    ("DATA", "Profit for the year", (None, 162087, None, None, None, None, 3124, 165211)),
    ("DATA", "Other comprehensive income for the year", (None, None, 17, 2746, None, None, None, 2763)),
    ("DATA", "Employee share-based payments", (None, None, None, None, None, 58, None, 58)),
    ("DATA", "ESS settlement", (None, None, None, None, None, -88, None, -88)),
    ("DATA", "Issue of growth shares", (None, None, None, None, None, None, 5, 5)),
    ("DATA", "Payment of dividend to parent", (None, -120000, None, None, None, None, None, -120000)),
    ("TOTAL", "At 31 December 2025 (FY2025 closing)", (389320, 667507, 25, -39, None, 146, 10571, 1067530)),
]

bw.add_equity_changes_sheet(
    title="OakNorth Bank plc — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, Bank Group (consolidated) basis, £'000. Equity "
              "reconciliation ladder confirmed: every year's own closing balance ties exactly to both the next "
              "year's own opening balance and that year's own Balance Sheet Total equity - zero undocumented plug "
              "rows anywhere across all 5 years. The one bridging row (the FRS 102 -> IFRS transition adjustment) "
              "is a genuine, bank-disclosed item, not an error.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=66,
)

cash_rows = [
    ("SECTION", "Reconciliation of profit before tax to operating cash flows", {}),
    ("DATA", "Profit before tax", {"FY2025": 222529, "FY2024": 214794, "FY2023": 187333, "FY2022": 152336, "FY2021": 134540}),
    ("DATA", "Adjustments for non-cash items", {"FY2025": 20707, "FY2024": 11139, "FY2023": 30215, "FY2022": 7056, "FY2021": 646}),
    ("DATA", "Net change in other assets and liabilities", {"FY2025": 41185, "FY2024": 4665, "FY2023": -30857, "FY2022": -14137, "FY2021": -2050}),
    ("DATA", "Increase in loan receivables", {"FY2025": -496341, "FY2024": -573437, "FY2023": -714507, "FY2022": -251805, "FY2021": -390362}),
    ("DATA", "Increase in customer deposits", {"FY2025": 408891, "FY2024": 1463663, "FY2023": 1026092, "FY2022": 969657, "FY2021": 329975}),
    ("DATA", "(Increase)/decrease in derivatives held for risk management", {"FY2025": -29903, "FY2024": 7655, "FY2023": -2530}),
    ("DATA", "Income taxes paid", {"FY2025": -49351, "FY2024": -57333, "FY2023": -52840, "FY2022": -39766, "FY2021": -31850}),
    ("DATA", "Other operating adjustments not separately shown", {"FY2023": 531, "FY2022": 9880, "FY2021": 710}),
    ("TOTAL", "Net cash flows generated from operating activities", {"FY2025": 117717, "FY2024": 1071146, "FY2023": 443437, "FY2022": 833221, "FY2021": 41609}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of intangible assets", {"FY2025": -7832, "FY2024": -5279, "FY2023": -2961, "FY2022": -4358}),
    ("DATA", "Purchase of tangible assets", {"FY2025": -299, "FY2024": -75, "FY2023": -18, "FY2022": -19, "FY2021": -57}),
    ("DATA", "Acquisition of subsidiary, net of cash acquired", {"FY2022": -10475}),
    ("DATA", "Purchase of investment securities", {"FY2025": -621941, "FY2024": -820024, "FY2023": -897488, "FY2022": -202501, "FY2021": -191086}),
    ("DATA", "Proceeds from sale/maturity of investment securities", {"FY2025": 409522, "FY2024": 830700, "FY2023": 905244, "FY2022": 191000, "FY2021": 126771}),
    ("DATA", "Interest received on investment securities", {"FY2025": 21152, "FY2023": 623, "FY2022": 1076, "FY2021": 4029}),
    ("DATA", "Other investing cash flows and classification differences", {"FY2025": 90, "FY2024": 19, "FY2023": 18}),
    ("TOTAL", "Net cash flows from/(used in) investing activities", {"FY2025": -199308, "FY2024": 5341, "FY2023": 5418, "FY2022": -25277, "FY2021": -60343}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Increase in borrowings from Bank of England facilities", {"FY2025": 15000}),
    ("DATA", "Repayment of borrowings from Bank of England facilities", {"FY2025": -210000}),
    ("DATA", "Increase in subordinated debt", {"FY2024": 150000, "FY2023": 30000}),
    ("DATA", "Increase in intercompany borrowings", {"FY2025": 4541, "FY2024": 6326, "FY2023": 11660}),
    ("DATA", "Repayment/decrease of intercompany borrowings", {"FY2025": -7041, "FY2024": -9772}),
    ("DATA", "Interest paid on borrowings and subordinated debt", {"FY2025": -24084, "FY2024": -15538, "FY2023": -10073, "FY2022": -5449, "FY2021": -3964}),
    ("DATA", "Cash outflow on lease liabilities", {"FY2025": -1456, "FY2024": -1408, "FY2023": -686, "FY2022": -1050}),
    ("DATA", "Payment of dividend to parent", {"FY2025": -120000, "FY2024": -20000}),
    ("DATA", "Repayment of subordinated debt", {"FY2023": -50000}),
    ("DATA", "Other financing cash flows and classification differences", {"FY2025": -199}),
    ("DATA", "Increase in TFS borrowings", {"FY2021": 18100}),
    ("TOTAL", "Net cash flows from/(used in) financing activities", {"FY2025": -343239, "FY2024": 109608, "FY2023": -19099, "FY2022": -6499, "FY2021": 14136}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": -424920, "FY2024": 1186076, "FY2023": 429738, "FY2022": 801445, "FY2021": -4598}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 2893652, "FY2024": 1707576, "FY2023": 1277838, "FY2022": 476393, "FY2021": 480991}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 2468732, "FY2024": 2893652, "FY2023": 1707576, "FY2022": 1277838, "FY2021": 476393}),
    ("SECTION", "Reconciliation to cash at banks", {}),
    ("DATA", "Cash and balances at central bank", {"FY2025": 2199053, "FY2024": 2689013, "FY2023": 1637314, "FY2022": 1235711, "FY2021": 446374}),
    ("DATA", "Loans and advances to banks", {"FY2025": 77587, "FY2024": 75477, "FY2023": 33458, "FY2022": 37507, "FY2021": 30019}),
    ("DATA", "Investment securities (US money market funds)", {"FY2025": 192092, "FY2024": 124007, "FY2023": 31788}),
    ("TOTAL", "Total cash and cash equivalents", {"FY2025": 2468732, "FY2024": 2888497, "FY2023": 1702560, "FY2022": 1273218, "FY2021": 476393}),
]
bw.add_cash_flow_sheet(
    "OakNorth Bank plc — Consolidated Statement of Cash Flows",
    "Bank Group basis for FY2022–FY2025; standalone Bank basis for FY2021, £'000",
    cash_rows, cash_flow_sources(), first_col_width=62, source_height=155, unit_suffix=" (£'000)"
)

# ---------------------------------------------------------------
# Asset Quality - OakNorth Bank standalone (entity-level) loans and advances
# to customers, IFRS 9 stage 1/2/3 split. Bank-only basis (not Bank Group) -
# this is the finest granularity the Bank discloses; net carrying value ties
# exactly to the Balance Sheet's Bank Group loans and advances figure only
# for FY2021 (before the subsidiary was consolidated) - later years differ
# by the subsidiary's own lending, a genuine basis difference, not an error.
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "OakNorth Bank (standalone) loans and advances to customers, on-balance sheet, by IFRS 9 stage", {}),
    ("DATA", "Stage 1 gross carrying amount", {"FY2025": 4514265, "FY2024": 3976861, "FY2023": 3397765, "FY2022": 2990755, "FY2021": 2782991}),
    ("DATA", "Stage 2 gross carrying amount", {"FY2025": 242557, "FY2024": 358650, "FY2023": 357847, "FY2022": 64825, "FY2021": 69097}),
    ("DATA", "Stage 3 gross carrying amount", {"FY2025": 146439, "FY2024": 76908, "FY2023": 91089, "FY2022": 95415, "FY2021": 63228}),
    ("TOTAL", "Total gross carrying amount", {"FY2025": 4903261, "FY2024": 4412419, "FY2023": 3846701, "FY2022": 3150995, "FY2021": 2915316}),
    ("DATA", "Stage 1 allowance for ECL", {"FY2025": -7088, "FY2024": -6838, "FY2023": -13260, "FY2022": -13311, "FY2021": -8929}),
    ("DATA", "Stage 2 allowance for ECL", {"FY2025": -4303, "FY2024": -6292, "FY2023": -5082, "FY2022": -2507, "FY2021": -6481}),
    ("DATA", "Stage 3 allowance for ECL", {"FY2025": -6368, "FY2024": -8949, "FY2023": -12219, "FY2022": -7684, "FY2021": -13601}),
    ("TOTAL", "Total allowance for ECL", {"FY2025": -17759, "FY2024": -22079, "FY2023": -30561, "FY2022": -23502, "FY2021": -29011}),
    ("TOTAL", "Net carrying amount", {"FY2025": 4885502, "FY2024": 4390340, "FY2023": 3816140, "FY2022": 3127493, "FY2021": 2886305}),
    ("DATA", "Stage 3 as % of total gross carrying amount (NPL ratio)", {"FY2025": "2.99%", "FY2024": "1.74%", "FY2023": "2.37%", "FY2022": "3.03%", "FY2021": "2.17%"}),
    ("DATA", "Stage 2 as % of total gross carrying amount", {"FY2025": "4.95%", "FY2024": "8.13%", "FY2023": "9.30%", "FY2022": "2.06%", "FY2021": "2.37%"}),
    ("DATA", "Total allowance for ECL as % of total gross carrying amount (coverage)", {"FY2025": "0.36%", "FY2024": "0.50%", "FY2023": "0.79%", "FY2022": "0.75%", "FY2021": "1.00%"}),
]

bw.add_asset_quality_sheet(
    title="OakNorth Bank plc — Asset Quality",
    subtitle="OakNorth Bank plc standalone (entity-level, not Bank Group) loans and advances to customers, IFRS 9 "
              "stage 1/2/3 split, on-balance sheet only (excludes undrawn loan commitments, disclosed separately). £'000.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - OakNorth Bank plc, on-balance sheet Stage 1/2/3 exposure and ECL allowance tables (OakNorth "
        "Bank standalone, not Bank Group):\n"
        f"FY2025: Annual Report 2025, Table 5 'Movement in gross exposures and impairment allowance ... "
        f"(OakNorth Bank Plc)', p.66 - {AR_URLS['FY2025']}\n"
        f"FY2024: Annual Report 2024, Table 3 (same title), p.63 - {AR_URLS['FY2024']}\n"
        f"FY2023: Annual Report 2023, Table 1 'Maximum exposure to credit risk in the loan book, ECL provisions and "
        f"Staging (OakNorth Bank)', p.55 - {AR_URLS['FY2023']}\n"
        f"FY2022/FY2021: Annual Report 2022, Table 1 (same title, both years shown), p.71 - {AR_URLS['FY2022']}\n\n"
        "DATA QUALITY / BASIS NOTE: this sheet is OakNorth Bank plc standalone (entity-level), the finest "
        "granularity at which IFRS 9 stage data is disclosed - it is NOT the Bank Group consolidated figure used "
        "on the Balance Sheet/Profit & Loss/Statement of Changes in Equity sheets. For FY2021 (before the A.S.K "
        "Partners Limited subsidiary was consolidated) the two bases are identical and this sheet's net carrying "
        "amount (2,886,305) ties exactly to the Balance Sheet's Bank Group loans and advances to customers figure "
        "for that year. From FY2022 onward the two bases diverge by the subsidiary's own lending (FY2022: 457; "
        "FY2023: 1,204; FY2024: 2,760; FY2025: 4,372) - each year's own figure is shown as originally disclosed "
        "rather than adjusted to force a tie."
    ),
    first_col_width=76,
    source_height=280,
    unit_suffix=" (£'000)",
)


def metric(name, unit, rows, note=None):
    bw.add_metric_sheet(name, unit, rows, p3_sources(), note=note, first_col_width=52, source_height=155)


metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", {"FY2025": 988868, "FY2024": 952901, "FY2023": 853523, "FY2022": 719977, "FY2021": 628446})])
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 ratio", {"FY2025": "15.5%", "FY2024": "17.3%", "FY2023": "18.6%", "FY2022": "18.7%", "FY2021": "20.5%"})])
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", {"FY2025": 988868, "FY2024": 952901, "FY2023": 853523, "FY2022": 719977, "FY2021": 628446})])
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {"FY2025": "15.5%", "FY2024": "17.3%", "FY2023": "18.6%", "FY2022": "18.7%", "FY2021": "20.5%"})])
metric("Total Capital", "£'000", [("Total capital", {"FY2025": 1168868, "FY2024": 1132901, "FY2023": 883523, "FY2022": 769977, "FY2021": 678446})])
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2025": "18.4%", "FY2024": "20.5%", "FY2023": "19.3%", "FY2022": "20.1%", "FY2021": "22.1%"})])
metric("Total RWAs", "£'000", [("Total risk-weighted exposure amount", {"FY2025": 6363514, "FY2024": 5517819, "FY2023": 4577382, "FY2022": 3840274, "FY2021": 3065585})])

# RWA Breakdown - Pillar 3 UK OV1 template, placed right after Total RWAs per
# the locked sheet order. All 5 years tie to the Total RWAs figure above
# (FY2022/FY2023 off by £1 due to source-document rounding).
rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding CCR & CVA)", {"FY2025": 5801031, "FY2024": 5057693, "FY2023": 4230433, "FY2022": 3577369, "FY2021": 2875251}),
    ("DATA", "Counterparty credit risk (CCR, including CVA)", {"FY2025": 32843, "FY2024": 31736, "FY2023": 13633}),
    ("DATA", "Securitisation exposures in the non-trading book (after the cap)", {"FY2025": 22393}),
    ("DATA", "Operational risk", {"FY2025": 507247, "FY2024": 428390, "FY2023": 333317, "FY2022": 262904, "FY2021": 190334}),
    ("TOTAL", "Total", {"FY2025": 6363514, "FY2024": 5517819, "FY2023": 4577382, "FY2022": 3840274, "FY2021": 3065585}),
]
bw.add_rwa_breakdown_sheet(
    title="OakNorth Bank plc — RWA Breakdown",
    subtitle="Pillar 3 UK OV1 template (top-level risk-type categories), £'000. FY2025's Bank Group consolidated "
              "basis; FY2022–FY2024 solo/Bank basis; FY2021 standalone Bank basis (per each year's own Pillar 3 "
              "disclosure - see p3_sources note). No CCR or securitisation exposure was disclosed FY2021–FY2023, "
              "and no securitisation exposure existed before the FY2025 CLO investment programme (see that "
              "sheet's own note) - both genuine absences, not gaps.",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources(),
    first_col_width=68,
    source_height=200,
    unit_suffix=" (£'000)",
)

metric("Leverage Ratio", "£'000 / %", [
    ("Leverage ratio exposure measure excluding central banks", {"FY2025": 6177019, "FY2024": 5262074, "FY2023": 4463419, "FY2022": 4954910, "FY2021": 3855405}),
    ("Leverage ratio excluding central banks", {"FY2025": "16.0%", "FY2024": "18.1%", "FY2023": "19.1%", "FY2022": "14.5%", "FY2021": "21.4%"}),
    ("Leverage ratio exposure measure including central banks", {"FY2025": 8361483, "FY2024": 7951087, "FY2023": 6100733}),
    ("Leverage ratio including central banks", {"FY2025": "11.8%", "FY2024": "12.0%", "FY2023": "14.0%"}),
], note="The FY2021 disclosure labels its 21.4% figure as the UK leverage-ratio-framework calculation excluding claims on central banks; FY2022–FY2025 use the corresponding KM1 excluding-central-bank measure. FY2022–FY2025 do not disclose the including-central-bank variant in the same way until FY2023.")
metric("LCR", "£'000 / %", [
    ("Total high-quality liquid assets (HQLA), weighted value-average", {"FY2025": 2609639, "FY2024": 1876341, "FY2023": 1189319, "FY2022": 556199, "FY2021": "Not disclosed"}),
    ("Total net cash outflows, adjusted value", {"FY2025": 555901, "FY2024": 384055, "FY2023": 325606, "FY2022": 158569, "FY2021": "Not disclosed"}),
    ("Liquidity Coverage Ratio", {"FY2025": "478%", "FY2024": "489%", "FY2023": "365%", "FY2022": "351%", "FY2021": "Not publicly disclosed"}),
], note="The 2022–2025 LCR figures are the reported average/weighted-value disclosures (UK KM1 template). CORRECTED: FY2023 previously showed the FY2023 Pillar 3 disclosure's UK LIQ1 table's Dec-23 quarter-end point-in-time snapshot (HQLA 1,441,255; net cash outflows 374,177; LCR 385%) rather than that same document's own UK KM1 summary table average-of-4-quarters figure used for every other year - corrected to the average basis (HQLA 1,189,319; net cash outflows 325,606; LCR 365%) for consistency across all 5 years. The FY2021 Pillar 3 report does not contain a comparable LCR key-metrics disclosure.")
metric("NSFR", "£'000 / %", [
    ("Total available stable funding", {"FY2025": 6855628, "FY2024": 6303663, "FY2023": 4831446, "FY2022": 3748427, "FY2021": "Not disclosed"}),
    ("Total required stable funding", {"FY2025": 3608230, "FY2024": 3324269, "FY2023": 2993447, "FY2022": 2436946, "FY2021": "Not disclosed"}),
    ("Net Stable Funding Ratio", {"FY2025": "190%", "FY2024": "190%", "FY2023": "161%", "FY2022": "154%", "FY2021": "Not publicly disclosed"}),
], note="UK NSFR disclosures began from 1 January 2022; no FY2021 NSFR disclosure exists in OakNorth's official Pillar 3 report.")
metric("MREL Ratio", None, [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})], note="No MREL ratio is presented in OakNorth's five annual Pillar 3 disclosures. This is a documented non-disclosure, not a zero.")

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 7856889, "FY2024": 7573159, "FY2023": 5810647, "FY2022": 4657420, "FY2021": 3570311}),
        ("Loans and advances to customers", {"FY2025": 4889874, "FY2024": 4393100, "FY2023": 3817344, "FY2022": 3127950, "FY2021": 2886305}),
        ("Customer deposits", {"FY2025": 6513248, "FY2024": 6103046, "FY2023": 4639352, "FY2022": 3613260, "FY2021": 2643603}),
        ("Total equity", {"FY2025": 1067530, "FY2024": 1019581, "FY2023": 885130, "FY2022": 744385, "FY2021": 629318}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net interest and fee income", {"FY2025": 318047, "FY2024": 309851, "FY2023": 296779, "FY2022": 221090, "FY2021": 176190}),
        ("Operating expenses and provisions", {"FY2025": -95518, "FY2024": -95057, "FY2023": -109446, "FY2022": -68754, "FY2021": -41650}),
        ("Profit for the year", {"FY2025": 165211, "FY2024": 159334, "FY2023": 138470, "FY2022": 113259, "FY2021": 100392}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 1019581, "FY2024": 885130, "FY2023": 744385, "FY2022": 629318, "FY2021": 528677}),
        ("Total comprehensive income for the year", {"FY2025": 167974, "FY2024": 154296, "FY2023": 140707, "FY2022": 113038, "FY2021": 100637}),
        ("Other equity movements, net", {"FY2025": -120025, "FY2024": -19845, "FY2023": 38, "FY2022": 2029, "FY2021": 4}),
        ("Closing equity", {"FY2025": 1067530, "FY2024": 1019581, "FY2023": 885130, "FY2022": 744385, "FY2021": 629318}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash flows generated from operating activities", {"FY2025": 117717, "FY2024": 1071146, "FY2023": 443437, "FY2022": 833221, "FY2021": 41609}),
        ("Net cash flows from/(used in) investing activities", {"FY2025": -199308, "FY2024": 5341, "FY2023": 5418, "FY2022": -25277, "FY2021": -60343}),
        ("Net cash flows from/(used in) financing activities", {"FY2025": -343239, "FY2024": 109608, "FY2023": -19099, "FY2022": -6499, "FY2021": 14136}),
        ("Cash and cash equivalents at end of year", {"FY2025": 2468732, "FY2024": 2888497, "FY2023": 1702560, "FY2022": 1273218, "FY2021": 476393}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "15.5%", "FY2024": "17.3%", "FY2023": "18.6%", "FY2022": "18.7%", "FY2021": "20.5%"}),
        ("Tier 1 Ratio", {"FY2025": "15.5%", "FY2024": "17.3%", "FY2023": "18.6%", "FY2022": "18.7%", "FY2021": "20.5%"}),
        ("Total Capital Ratio", {"FY2025": "18.4%", "FY2024": "20.5%", "FY2023": "19.3%", "FY2022": "20.1%", "FY2021": "22.1%"}),
        ("Leverage Ratio", {"FY2025": "16.0%", "FY2024": "18.1%", "FY2023": "19.1%", "FY2022": "14.5%", "FY2021": "21.4%"}),
        ("LCR", {"FY2025": "478%", "FY2024": "489%", "FY2023": "365%", "FY2022": "351%", "FY2021": "Not disclosed"}),
        ("NSFR", {"FY2025": "190%", "FY2024": "190%", "FY2023": "161%", "FY2022": "154%", "FY2021": "Not disclosed"}),
    ],
    note="OakNorth's official Pillar 3 archive is annual, so no interim/14th worksheet is added. FY2023's LCR "
         "figures were corrected during the ST-028 rollout to use the average-of-4-quarters basis consistent with "
         "every other year - see the LCR sheet's own note for detail.",
)

bw.save("/Users/armaan/code/katalysis/banks/OAKNORTH BANK FINANCIALS.xlsx")
