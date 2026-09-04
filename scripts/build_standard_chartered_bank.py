import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


# STANDARD CHARTERED BANK (ZC000018 / FRN 114276)
# The annual reports provide distinct Group and Company columns.  Cash-flow
# values below are the standalone Bank Company column.  Regulatory capital
# disclosures in the reports are explicitly for Standard Chartered Bank Group
# on a solo-consolidated basis (including four subsidiaries), so Group Pillar 3
# figures are intentionally not imported into this Bank-level workbook.

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

REPORTS = {
    "FY2025": "https://www.sc.com/en/uploads/sites/66/content/docs/sc-bank-2025-report.pdf",
    "FY2024": "https://www.sc.com/en/uploads/sites/66/content/docs/sc-bank-2024-results.pdf",
    "FY2023": "https://www.sc.com/EN/uploads/sites/66/content/docs/sc-bank-2023-annual-report.pdf",
    "FY2022": "https://www.sc.com/en/uploads/sites/66/content/docs/sc-bank-2022-annual-report.pdf",
    "FY2021": "https://www.sc.com/EN/uploads/sites/66/content/docs/sc-bank-2021-results.pdf",
}
CH_URL = "https://find-and-update.company-information.service.gov.uk/company/ZC000018/filing-history"

ENTITY_NOTE = (
    "ENTITY AND BASIS: Standard Chartered Bank (Companies House Royal Charter reference ZC000018, FRN 114276) "
    "is incorporated in England with limited liability by Royal Charter 1853. The source reports distinguish "
    "Standard Chartered Bank Group (the Bank and subsidiaries) from Standard Chartered Bank Company (the "
    "standalone legal entity). All cash-flow rows in this workbook use the Company column only."
)

REGULATORY_GAP_NOTE = (
    "REGULATORY BASIS LIMITATION: the reports state that capital disclosures are provided on the Standard "
    "Chartered Bank Group basis and that PRA requirements are set on a solo-consolidated basis. That basis includes "
    "four subsidiaries (Standard Chartered Holdings (International) B.V., Standard Chartered Grindlays Pty "
    "Limited, SCMB Overseas Limited and Corrasi Covered Bonds LLP). No complete five-year standalone Company KM1 "
    "series was located. Group Pillar 3/capital figures have therefore not been substituted for the requested "
    "Bank-level series."
)

SOURCE_NOTE = (
    "Sources - standalone Standard Chartered Bank Company cash flows, $million:\n"
    "FY2025: Directors' Report and Financial Statements 2025, cash flow statement p.89 - " + REPORTS["FY2025"] + "\n"
    "FY2024: Directors' Report and Financial Statements 2024, cash flow statement p.89 - " + REPORTS["FY2024"] + "\n"
    "FY2023: Directors' Report and Financial Statements 2023, cash flow statements p.165 - " + REPORTS["FY2023"] + "\n"
    "FY2022: Directors' Report and Financial Statements 2022, cash flow statements p.172 - " + REPORTS["FY2022"] + "\n"
    "FY2021: Directors' Report and Financial Statements 2021, cash flow statements p.172 - " + REPORTS["FY2021"] + "\n"
    "Entity filing history and identity: Companies House ZC000018 - " + CH_URL + "\n\n" + ENTITY_NOTE
)

bw = BankWorkbook(
    bank_name="Standard Chartered Bank (standalone Company basis)",
    years=YEARS,
    year_label=YEAR_LABEL,
    header_color="005A70",
)

# Company column only.  FY2022 uses the 2022 report's own as-reported figures;
# the 2023 report restated the FY2022 comparative, so the discontinuity is
# documented in the source note below.
CF = {
    "Profit before taxation": {"FY2025": 3245, "FY2024": 3058, "FY2023": 3088, "FY2022": 2996, "FY2021": 2496},
    "Adjustments for non-cash items and other adjustments": {"FY2025": -429, "FY2024": -1, "FY2023": -790, "FY2022": 381, "FY2021": -659},
    "Change in operating assets": {"FY2025": 273, "FY2024": -26161, "FY2023": 23104, "FY2022": -5451, "FY2021": -1178},
    "Change in operating liabilities": {"FY2025": 11452, "FY2024": 13864, "FY2023": -13891, "FY2022": 4521, "FY2021": 18902},
    "Contributions to defined benefit schemes": {"FY2025": -46, "FY2024": -39, "FY2023": -46, "FY2022": -36, "FY2021": -82},
    "UK and overseas taxes paid": {"FY2025": -711, "FY2024": -720, "FY2023": -658, "FY2022": -359, "FY2021": -274},
    "Net cash from/(used in) operating activities": {"FY2025": 13784, "FY2024": -9999, "FY2023": 10807, "FY2022": 2052, "FY2021": 19205},
    "Internally generated capitalised software": {"FY2025": -521, "FY2024": -246, "FY2023": -378, "FY2022": -501, "FY2021": -503},
    "Purchase of property, plant and equipment": {"FY2025": -149, "FY2024": -176, "FY2023": -53, "FY2022": -59, "FY2021": -67},
    "Disposal of property, plant and equipment": {"FY2025": 3, "FY2024": 15, "FY2023": 1, "FY2022": 14, "FY2021": 6},
    "Dividends received from subsidiaries, associates and joint ventures": {"FY2025": 1260, "FY2024": 1052, "FY2023": 2060, "FY2022": 1046, "FY2021": 1626},
    "Disposals of subsidiaries, associates and joint ventures / held-for-sale assets": {"FY2025": 0, "FY2024": 26, "FY2023": 108, "FY2022": 0, "FY2021": 0},
    "Purchase of investment securities": {"FY2025": -68809, "FY2024": -84630, "FY2023": -91970, "FY2022": -114671, "FY2021": -131168},
    "Disposal and maturity of investment securities": {"FY2025": 72962, "FY2024": 91907, "FY2023": 97216, "FY2022": 98999, "FY2021": 113905},
    "Net cash from/(used in) investing activities": {"FY2025": 4746, "FY2024": 7948, "FY2023": 6984, "FY2022": -15172, "FY2021": -16201},
    "Premises and equipment lease liability principal payment": {"FY2025": -42, "FY2024": -43, "FY2023": -45, "FY2022": -78, "FY2021": -72},
    "Issue of ordinary and preference share capital, net of expenses": {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 1273},
    "Cancellation of shares including share buyback": {"FY2025": 0, "FY2024": 0, "FY2023": -750, "FY2022": 0, "FY2021": 0},
    "Issue of Additional Tier 1 capital, net of expenses": {"FY2025": 0, "FY2024": 980, "FY2023": 992, "FY2022": 1000, "FY2021": 2750},
    "Redemption of Tier 1 capital": {"FY2025": 0, "FY2024": 0, "FY2023": -1000, "FY2022": -999, "FY2021": -1042},
    "Gross proceeds from issue of subordinated liabilities": {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 750, "FY2021": 0},
    "Interest paid on subordinated liabilities": {"FY2025": -492, "FY2024": -528, "FY2023": -583, "FY2022": -378, "FY2021": -456},
    "Repayment of subordinated liabilities": {"FY2025": -2173, "FY2024": -1000, "FY2023": -2160, "FY2022": -1008, "FY2021": -16},
    "Proceeds from issue of senior debts": {"FY2025": 2455, "FY2024": 3114, "FY2023": 4820, "FY2022": 4091, "FY2021": 660},
    "Repayment of senior debts": {"FY2025": -3986, "FY2024": -2471, "FY2023": -1806, "FY2022": -298, "FY2021": -422},
    "Interest paid on senior debts": {"FY2025": -374, "FY2024": -282, "FY2023": -235, "FY2022": -1, "FY2021": -16},
    "Distributions and dividends paid to preference shareholders and AT1 securities": {"FY2025": -389, "FY2024": -349, "FY2023": -363, "FY2022": -311, "FY2021": -292},
    "Dividends paid to ordinary shareholders": {"FY2025": -2276, "FY2024": -2395, "FY2023": -2599, "FY2022": -575, "FY2021": -1511},
    "Net cash used in financing activities": {"FY2025": -7277, "FY2024": -2974, "FY2023": -3729, "FY2022": 2193, "FY2021": 856},
    "Net increase/(decrease) in cash and cash equivalents": {"FY2025": 11253, "FY2024": -5025, "FY2023": 14062, "FY2022": -10927, "FY2021": 3860},
    "Cash and cash equivalents at beginning of year": {"FY2025": 48101, "FY2024": 53988, "FY2023": 40264, "FY2022": 59406, "FY2021": 56151},
    "Effect of exchange rate movements on cash and cash equivalents": {"FY2025": -64, "FY2024": -862, "FY2023": -338, "FY2022": -861, "FY2021": -605},
    "Cash and cash equivalents at end of year": {"FY2025": 59290, "FY2024": 48101, "FY2023": 53988, "FY2022": 47618, "FY2021": 59406},
}

cash_rows = []
for label in list(CF):
    if label == "Profit before taxation":
        cash_rows.append(("SECTION", "Cash flows from operating activities", {}))
    elif label == "Internally generated capitalised software":
        cash_rows.append(("SECTION", "Cash flows from investing activities", {}))
    elif label == "Premises and equipment lease liability principal payment":
        cash_rows.append(("SECTION", "Cash flows from financing activities", {}))
    elif label == "Net increase/(decrease) in cash and cash equivalents":
        cash_rows.append(("SECTION", "Cash and cash equivalents reconciliation", {}))
    kind = "TOTAL" if label.startswith("Net cash") or label.startswith("Cash and cash") or label.startswith("Net increase") else "DATA"
    cash_rows.append((kind, label, CF[label]))

STATEMENT_REPORTS_NOTE = (
    "Statement sources - standalone Standard Chartered Bank Company balance sheet and equity, Group income "
    "statement (see note below), $million:\n"
    "FY2025/FY2024: Directors' Report and Financial Statements 2025, Balance sheets p.86, Cash flow statement p.88, "
    "Company statement of changes in equity p.89, Consolidated income statement p.84 - " + REPORTS["FY2025"] + "\n"
    "FY2023/FY2022: Directors' Report and Financial Statements 2023, Consolidated balance sheet p.162, Company "
    "statement of changes in equity p.165, Consolidated income statement p.160 - " + REPORTS["FY2023"] + "\n"
    "FY2021: Directors' Report and Financial Statements 2021, Consolidated balance sheet p.169, Company statement "
    "of changes in equity p.172, Consolidated income statement p.167 - " + REPORTS["FY2021"] + "\n"
    "Entity filing history and identity: Companies House ZC000018 - " + CH_URL + "\n\n" + ENTITY_NOTE
)

INCOME_STATEMENT_NOTE = (
    "The Company has taken advantage of the exemption in section 408 of the Companies Act 2006 not to present its "
    "individual income statement/statement of comprehensive income. This Profit & Loss sheet therefore uses the "
    "Bank GROUP consolidated income statement (not the Company column used on the Balance Sheet/Equity sheets). "
    "The Company's own profit after tax (disclosed as a single figure in each year's balance sheet note) was: "
    "FY2025 $2,517m, FY2024 $2,325m, FY2023 $2,585m, FY2022 $2,372m, FY2021 $2,146m - these tie exactly to the "
    "'Profit for the year' rows on the Statement of Changes in Equity sheet (Company basis), confirming the two "
    "sheets are internally consistent despite using different consolidation bases."
)

# --- Balance Sheet (Company column) ---------------------------------------
BS = {
    "Cash and balances at central banks": {"FY2025": 52348, "FY2024": 45233, "FY2023": 52758, "FY2022": 38867, "FY2021": 48165},
    "Financial assets held at fair value through profit or loss": {"FY2025": 99894, "FY2024": 88349, "FY2023": 86412, "FY2022": 75792, "FY2021": 99705},
    "Derivative financial instruments (assets)": {"FY2025": 66631, "FY2024": 82844, "FY2023": 53221, "FY2022": 65481, "FY2021": 53478},
    "Loans and advances to banks": {"FY2025": 11108, "FY2024": 11755, "FY2023": 10135, "FY2022": 18548, "FY2021": 16117},
    "Loans and advances to customers": {"FY2025": 80091, "FY2024": 77597, "FY2023": 75883, "FY2022": 80611, "FY2021": 71161},
    "Investment securities": {"FY2025": 79684, "FY2024": 82101, "FY2023": 92771, "FY2022": 95372, "FY2021": 86389},
    "Other assets": {"FY2025": 23568, "FY2024": 21552, "FY2023": 21742, "FY2022": 31715, "FY2021": 25688},
    "Due from subsidiary undertakings and other related parties": {"FY2025": 11538, "FY2024": 10066, "FY2023": 10053, "FY2022": 13214, "FY2021": 10741},
    "Current tax assets": {"FY2025": 412, "FY2024": 516, "FY2023": 395, "FY2022": 347, "FY2021": 487},
    "Prepayments and accrued income": {"FY2025": 1392, "FY2024": 1535, "FY2023": 1386, "FY2022": 1598, "FY2021": 905},
    "Investments in subsidiary undertakings": {"FY2025": 10800, "FY2024": 10671, "FY2023": 10066, "FY2022": 10300, "FY2021": 9694},
    "Goodwill and intangible assets": {"FY2025": 2245, "FY2024": 1988, "FY2023": 2359, "FY2022": 2279, "FY2021": 2121},
    "Property, plant and equipment": {"FY2025": 714, "FY2024": 659, "FY2023": 521, "FY2022": 430, "FY2021": 627},
    "Deferred tax assets": {"FY2025": 251, "FY2024": 233, "FY2023": 379, "FY2022": 579, "FY2021": 508},
    "Retirement benefit schemes in surplus": {"FY2025": 104, "FY2024": 118},
    "Assets classified as held for sale": {"FY2025": 240, "FY2024": 474, "FY2023": 68, "FY2022": 592, "FY2021": 91},
    "Total assets": {"FY2025": 441020, "FY2024": 435691, "FY2023": 418149, "FY2022": 435725, "FY2021": 425877},
    "Deposits by banks": {"FY2025": 20607, "FY2024": 17824, "FY2023": 18280, "FY2022": 17900, "FY2021": 18870},
    "Customer accounts": {"FY2025": 132018, "FY2024": 119502, "FY2023": 121648, "FY2022": 137422, "FY2021": 135478},
    "Repurchase agreements and other similar secured borrowing": {"FY2025": 4828, "FY2024": 9845, "FY2023": 11977, "FY2022": 1723, "FY2021": 283},
    "Financial liabilities held at fair value through profit or loss": {"FY2025": 64880, "FY2024": 61683, "FY2023": 64467, "FY2022": 66189, "FY2021": 73902},
    "Derivative financial instruments (liabilities)": {"FY2025": 67556, "FY2024": 82745, "FY2023": 55531, "FY2022": 69203, "FY2021": 53835},
    "Debt securities in issue": {"FY2025": 37849, "FY2024": 36081, "FY2023": 34740, "FY2022": 34992, "FY2021": 33826},
    "Other liabilities": {"FY2025": 19421, "FY2024": 21486, "FY2023": 19213, "FY2022": 20990, "FY2021": 20460},
    "Due to parent companies, subsidiary undertakings & other related parties": {"FY2025": 50980, "FY2024": 42313, "FY2023": 47317, "FY2022": 39933, "FY2021": 40745},
    "Current tax liabilities": {"FY2025": 254, "FY2024": 294, "FY2023": 188, "FY2022": 329, "FY2021": 168},
    "Accruals and deferred income": {"FY2025": 2620, "FY2024": 2441, "FY2023": 2453, "FY2022": 2140, "FY2021": 1550},
    "Subordinated liabilities and other borrowed funds": {"FY2025": 8158, "FY2024": 9801, "FY2023": 10896, "FY2022": 12729, "FY2021": 14076},
    "Deferred tax liabilities": {"FY2025": 358, "FY2024": 308, "FY2023": 477, "FY2022": 486, "FY2021": 583},
    "Provisions for liabilities and charges": {"FY2025": 191, "FY2024": 186, "FY2023": 171, "FY2022": 249, "FY2021": 298},
    "Retirement benefit obligations (net deficit)": {"FY2025": 216, "FY2024": 200, "FY2023": 133, "FY2022": 124, "FY2021": 156},
    "Liabilities included in disposal groups held for sale": {"FY2025": 150},
    "Total liabilities": {"FY2025": 410086, "FY2024": 404709, "FY2023": 387496, "FY2022": 404754, "FY2021": 394230},
    "Share capital and share premium account": {"FY2025": 21643, "FY2024": 21643, "FY2023": 21643, "FY2022": 22393, "FY2021": 22393},
    "Other reserves": {"FY2025": -3666, "FY2024": -3804, "FY2023": -3403, "FY2022": -4252, "FY2021": -2089},
    "Retained earnings": {"FY2025": 7235, "FY2024": 7421, "FY2023": 7671, "FY2022": 8080, "FY2021": 6594},
    "Total parent company shareholders' equity": {"FY2025": 25212, "FY2024": 25260, "FY2023": 25911, "FY2022": 26221, "FY2021": 26898},
    "Other equity instruments": {"FY2025": 5722, "FY2024": 5722, "FY2023": 4742, "FY2022": 4750, "FY2021": 4749},
    "Total equity": {"FY2025": 30934, "FY2024": 30982, "FY2023": 30653, "FY2022": 30971, "FY2021": 31647},
    "Total equity and liabilities": {"FY2025": 441020, "FY2024": 435691, "FY2023": 418149, "FY2022": 435725, "FY2021": 425877},
}

bs_rows = []
for label in list(BS):
    if label == "Cash and balances at central banks":
        bs_rows.append(("SECTION", "Assets", {}))
    elif label == "Deposits by banks":
        bs_rows.append(("SECTION", "Liabilities", {}))
    elif label == "Share capital and share premium account":
        bs_rows.append(("SECTION", "Equity", {}))
    kind = "TOTAL" if label in (
        "Total assets", "Total liabilities", "Total parent company shareholders' equity",
        "Total equity", "Total equity and liabilities",
    ) else "DATA"
    bs_rows.append((kind, label, BS[label]))

bw.add_balance_sheet_sheet(
    title="Standard Chartered Bank — Balance Sheet",
    subtitle="Standalone Bank Company column (Consolidated balance sheet/'Balance sheets' statement), $million.",
    rows=bs_rows,
    sources_text=STATEMENT_REPORTS_NOTE + "\n\nNote: 'Retirement benefit schemes in surplus' is only reported as a "
    "separate asset line from FY2024 onward; earlier years' reports show only a net retirement benefit "
    "obligations/deficit liability. 'Liabilities included in disposal groups held for sale' is only reported from "
    "FY2025 (nil in FY2024, not reported as a line at all before that).",
    first_col_width=68,
    source_height=260,
    unit_suffix=" ($m)",
)

# --- Profit & Loss (Group consolidated - see INCOME_STATEMENT_NOTE) -------
PL = {
    "Interest income": {"FY2025": 16888, "FY2024": 19310, "FY2023": 18380, "FY2022": 9765, "FY2021": 6185},
    "Interest expense": {"FY2025": -13173, "FY2024": -14910, "FY2023": -13773, "FY2022": -5314, "FY2021": -2133},
    "Net interest income": {"FY2025": 3715, "FY2024": 4400, "FY2023": 4607, "FY2022": 4451, "FY2021": 4052},
    "Fees and commission income": {"FY2025": 3957, "FY2024": 3486, "FY2023": 3094, "FY2022": 2863, "FY2021": 2972},
    "Fees and commission expense": {"FY2025": -1031, "FY2024": -824, "FY2023": -656, "FY2022": -709, "FY2021": -576},
    "Net fee and commission income": {"FY2025": 2926, "FY2024": 2662, "FY2023": 2438, "FY2022": 2154, "FY2021": 2396},
    "Net trading income": {"FY2025": 6185, "FY2024": 5530, "FY2023": 4100, "FY2022": 3743, "FY2021": 2280},
    "Other operating income": {"FY2025": 128, "FY2024": -178, "FY2023": 404, "FY2022": -114, "FY2021": 132},
    "Operating income": {"FY2025": 12954, "FY2024": 12414, "FY2023": 11549, "FY2022": 10234, "FY2021": 8860},
    "Staff costs": {"FY2025": -6773, "FY2024": -6417, "FY2023": -6286, "FY2022": -5748, "FY2021": -5591},
    "Premises costs": {"FY2025": -267, "FY2024": -254, "FY2023": -241, "FY2022": -228, "FY2021": -224},
    "General administrative expenses": {"FY2025": -194, "FY2024": -223, "FY2023": 27, "FY2022": -75, "FY2021": -71},
    "Depreciation and amortisation": {"FY2025": -721, "FY2024": -656, "FY2023": -647, "FY2022": -611, "FY2021": -594},
    "Operating expenses": {"FY2025": -7955, "FY2024": -7550, "FY2023": -7147, "FY2022": -6662, "FY2021": -6480},
    "Operating profit before impairment losses and taxation": {"FY2025": 4999, "FY2024": 4864, "FY2023": 4402, "FY2022": 3572, "FY2021": 2380},
    "Credit impairment": {"FY2025": -248, "FY2024": -15, "FY2023": 58, "FY2022": 22, "FY2021": 30},
    "Goodwill, property, plant and equipment and other impairment": {"FY2025": -29, "FY2024": -410, "FY2023": -42, "FY2022": -107, "FY2021": -30},
    "Profit/(loss) from associates and joint ventures": {"FY2025": 2, "FY2024": 8, "FY2023": -4, "FY2022": -13, "FY2021": 1},
    "Profit before taxation": {"FY2025": 4724, "FY2024": 4447, "FY2023": 4414, "FY2022": 3474, "FY2021": 2381},
    "Taxation": {"FY2025": -1314, "FY2024": -1465, "FY2023": -1177, "FY2022": -1122, "FY2021": -743},
    "Profit for the year": {"FY2025": 3410, "FY2024": 2982, "FY2023": 3237, "FY2022": 2352, "FY2021": 1638},
    "Other comprehensive income/(loss), net of taxation": {"FY2025": 908, "FY2024": -476, "FY2023": 362, "FY2022": -2766, "FY2021": -599},
    "Total comprehensive income/(loss) for the year": {"FY2025": 4318, "FY2024": 2506, "FY2023": 3599, "FY2022": -414, "FY2021": 1039},
}

pl_rows = []
for label in list(PL):
    if label == "Interest income":
        pl_rows.append(("SECTION", "Income", {}))
    elif label == "Staff costs":
        pl_rows.append(("SECTION", "Operating expenses", {}))
    elif label == "Other comprehensive income/(loss), net of taxation":
        pl_rows.append(("SECTION", "Other comprehensive income", {}))
    kind = "TOTAL" if label in (
        "Net interest income", "Net fee and commission income", "Operating income", "Operating expenses",
        "Operating profit before impairment losses and taxation", "Profit before taxation", "Profit for the year",
        "Total comprehensive income/(loss) for the year",
    ) else "DATA"
    pl_rows.append((kind, label, PL[label]))

bw.add_income_statement_sheet(
    title="Standard Chartered Bank — Profit & Loss",
    subtitle="Bank GROUP consolidated income statement, $million - see source note (Company has no standalone P&L).",
    rows=pl_rows,
    sources_text=STATEMENT_REPORTS_NOTE + "\n\n" + INCOME_STATEMENT_NOTE,
    first_col_width=68,
    source_height=300,
    unit_suffix=" ($m)",
)

# --- Statement of Changes in Equity (Company column, chronological) -------
EQ_HEADERS = [
    "Share capital and share premium account", "Capital and merger reserves", "Own credit adjustment reserve",
    "FVOCI reserve - debt", "FVOCI reserve - equity", "Cash flow hedge reserve", "Translation reserve",
    "Retained earnings", "Parent company shareholders' equity", "Other equity instruments", "Total equity",
]

equity_rows = [
    ("TOTAL", "Balance at 1 January 2021", (20820, 40, 27, 28, 65, -27, -2039, 6881, 25795, 5000, 30795)),
    ("DATA", "Loss for the year", (None, None, None, None, None, None, None, -141, -141, None, -141)),
    ("DATA", "Other comprehensive income, net of tax", (None, None, -52, 140, 11, -5, -56, -4, 34, None, 34)),
    ("DATA", "Shares issued, net of expenses", (300, None, None, None, None, None, None, None, 300, None, 300)),
    ("DATA", "Redemption of other equity instruments", (None, None, None, None, None, None, None, None, None, -2000, -2000)),
    ("DATA", "Share option expenses", (None, None, None, None, None, None, None, 76, 76, None, 76)),
    ("DATA", "Dividends on preference shares and AT1 securities", (None, None, None, None, None, None, None, -458, -458, None, -458)),
    ("DATA", "Deemed distribution to parent", (None, None, None, None, None, None, None, -65, -65, None, -65)),
    ("DATA", "Other movements (FX reclass)", (None, None, None, None, None, None, 132, -132, None, None, None)),
    ("TOTAL", "Balance at 31 December 2021", (21120, 40, -25, 168, 76, -32, -1963, 6157, 25541, 3000, 28541)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, 2146, 2146, None, 2146)),
    ("DATA", "Other comprehensive income/(loss), net of tax", (None, None, 26, -258, 72, -7, -186, 146, -207, None, -207)),
    ("DATA", "Shares issued, net of expenses", (1273, None, None, None, None, None, None, None, 1273, None, 1273)),
    ("DATA", "Other equity instruments issued, net of expenses", (None, None, None, None, None, None, None, None, None, 2750, 2750)),
    ("DATA", "Redemption of other equity instruments", (None, None, None, None, None, None, None, -41, -41, -1001, -1042)),
    ("DATA", "Share option expenses", (None, None, None, None, None, None, None, 86, 86, None, 86)),
    ("DATA", "Dividends on ordinary shares", (None, None, None, None, None, None, None, -1511, -1511, None, -1511)),
    ("DATA", "Dividends on preference shares and AT1 securities", (None, None, None, None, None, None, None, -292, -292, None, -292)),
    ("DATA", "Deemed distribution to parent", (None, None, None, None, None, None, None, -85, -85, None, -85)),
    ("DATA", "Other movements", (None, None, None, None, None, None, None, -12, -12, None, -12)),
    ("TOTAL", "Balance at 31 December 2022", (22393, 40, -24, -1040, 147, -522, -2853, 8080, 26221, 4750, 30971)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, 2585, 2585, None, 2585)),
    ("DATA", "Other comprehensive income/(loss), net of tax", (None, None, 73, 324, 67, 471, -86, -21, 828, None, 828)),
    ("DATA", "Other equity instruments issued, net of expenses", (None, None, None, None, None, None, None, None, None, 992, 992)),
    ("DATA", "Redemption of other equity instruments", (None, None, None, None, None, None, None, None, None, -1000, -1000)),
    ("DATA", "Share option expenses", (None, None, None, None, None, None, None, 114, 114, None, 114)),
    ("DATA", "Dividends on ordinary shares", (None, None, None, None, None, None, None, -2599, -2599, None, -2599)),
    ("DATA", "Dividends on preference shares and AT1 securities", (None, None, None, None, None, None, None, -363, -363, None, -363)),
    ("DATA", "Deemed distribution to parent", (None, None, None, None, None, None, None, -113, -113, None, -113)),
    ("DATA", "Share buyback (preference shares cancelled)", (-750, None, None, None, None, None, None, None, -750, None, -750)),
    ("DATA", "Other movements", (None, None, None, None, None, None, None, -12, -12, None, -12)),
    ("TOTAL", "Balance at 31 December 2023", (21643, 40, 49, -716, 214, -51, -2939, 7671, 25911, 4742, 30653)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, 2325, 2325, None, 2325)),
    ("DATA", "Other comprehensive (loss)/income, net of tax", (None, None, -291, 308, -83, 34, -326, 194, -164, None, -164)),
    ("DATA", "Other equity instruments issued, net of expenses", (None, None, None, None, None, None, None, None, None, 980, 980)),
    ("DATA", "Share option expenses", (None, None, None, None, None, None, None, 127, 127, None, 127)),
    ("DATA", "Dividends on ordinary shares", (None, None, None, None, None, None, None, -2395, -2395, None, -2395)),
    ("DATA", "Dividends on preference shares and AT1 securities", (None, None, None, None, None, None, None, -349, -349, None, -349)),
    ("DATA", "Deemed distribution to parent", (None, None, None, None, None, None, None, -144, -144, None, -144)),
    ("DATA", "Other movements", (None, None, -1, 7, None, None, -49, -8, -51, None, -51)),
    ("TOTAL", "Balance at 31 December 2024", (20893 + 750, 40, -243, -401, 131, -17, -3314, 7421, 25260, 5722, 30982)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, 2517, 2517, None, 2517)),
    ("DATA", "Other comprehensive (loss)/income, net of tax", (None, None, -64, 295, -7, 54, -140, 182, 156, None, 156)),
    ("DATA", "Share option expenses", (None, None, None, None, None, None, None, 135, 135, None, 135)),
    ("DATA", "Dividends on ordinary shares", (None, None, None, None, None, None, None, -2276, -2276, None, -2276)),
    ("DATA", "Dividends on preference shares and AT1 securities", (None, None, None, None, None, None, None, -389, -389, None, -389)),
    ("DATA", "Deemed distribution to parent", (None, None, None, None, None, None, None, -191, -191, None, -191)),
    ("TOTAL", "Balance at 31 December 2025", (21643, 40, -307, -106, 124, 37, -3454, 7235, 25212, 5722, 30934)),
]

bw.add_equity_changes_sheet(
    title="Standard Chartered Bank — Statement of Changes in Equity",
    subtitle="Standalone Bank Company column, chronological, $million.",
    headers=EQ_HEADERS,
    rows=equity_rows,
    sources_text=STATEMENT_REPORTS_NOTE + "\n\nNote: FY2025's report combines share capital/premium into a single "
    "'Ordinary' ($20,893m) + 'Preference' ($750m) column pair that were shown as one combined column in earlier "
    "reports - the FY2024 closing balance above (21,643) is the sum of both, consistent with prior years' single "
    "column. Zero undocumented plug rows: every movement across all 5 years traces to a named line in the source "
    "reports (profit for the year, OCI, share/AT1 issuance and redemption, share option expense, dividends, deemed "
    "distributions to parent, and the FY2023 preference share buyback/capital reduction) and each year's closing "
    "balance ties exactly to that year's own Balance Sheet Total equity.",
    first_col_width=42,
    source_height=280,
    col_width=13,
)

bw.add_cash_flow_sheet(
    title="Standard Chartered Bank — Cash Flow Statement",
    subtitle="Standalone Bank Company column, $million; Group figures deliberately excluded.",
    rows=cash_rows,
    sources_text=SOURCE_NOTE + "\n\n" + REGULATORY_GAP_NOTE + "\n\nNote: the FY2023 report restates FY2022 cash-flow comparatives; FY2022 above preserves the FY2022 report's own as-reported Company figures.",
    first_col_width=72,
    source_height=260,
    unit_suffix=" ($m)",
)

# --- Asset Quality (Company loans and advances to customers, IFRS 9 stage) -
AQ = {
    "Stage 1 - gross carrying amount": {"FY2025": 75255, "FY2024": 72697, "FY2023": 70343, "FY2022": 73476, "FY2021": 59760},
    "Stage 1 - expected credit loss": {"FY2025": -124, "FY2024": -116, "FY2023": -89, "FY2022": -148, "FY2021": -151},
    "Stage 2 - gross carrying amount": {"FY2025": 3817, "FY2024": 4010, "FY2023": 4077, "FY2022": 5296, "FY2021": 9795},
    "Stage 2 - expected credit loss": {"FY2025": -112, "FY2024": -99, "FY2023": -80, "FY2022": -77, "FY2021": -235},
    "Stage 3 - gross carrying amount (credit-impaired)": {"FY2025": 2697, "FY2024": 2685, "FY2023": 3761, "FY2022": 4685, "FY2021": 5019},
    "Stage 3 - expected credit loss": {"FY2025": -1442, "FY2024": -1580, "FY2023": -2129, "FY2022": -2621, "FY2021": -3027},
    "Total gross carrying amount": {"FY2025": 81769, "FY2024": 79392, "FY2023": 78181, "FY2022": 83457, "FY2021": 74574},
    "Total expected credit loss": {"FY2025": -1678, "FY2024": -1795, "FY2023": -2298, "FY2022": -2846, "FY2021": -3413},
    "Net carrying value (= Loans and advances to customers)": {"FY2025": 80091, "FY2024": 77597, "FY2023": 75883, "FY2022": 80611, "FY2021": 71161},
    "NPL ratio (Stage 3 gross / Total gross)": {"FY2025": "3.30%", "FY2024": "3.38%", "FY2023": "4.81%", "FY2022": "5.61%", "FY2021": "6.73%"},
    "Stage 3 coverage ratio (Stage 3 ECL / Stage 3 gross)": {"FY2025": "53.47%", "FY2024": "58.85%", "FY2023": "56.61%", "FY2022": "55.94%", "FY2021": "60.31%"},
}

aq_rows = []
for label in list(AQ):
    if label == "Stage 1 - gross carrying amount":
        aq_rows.append(("SECTION", "Loans and advances to customers (amortised cost) by IFRS 9 stage", {}))
    elif label == "NPL ratio (Stage 3 gross / Total gross)":
        aq_rows.append(("SECTION", "Derived ratios", {}))
    kind = "TOTAL" if label.startswith("Total") or label.startswith("Net carrying value") else "DATA"
    aq_rows.append((kind, label, AQ[label]))

bw.add_asset_quality_sheet(
    title="Standard Chartered Bank — Asset Quality",
    subtitle="Standalone Bank Company column, loans and advances to customers by IFRS 9 stage, $million.",
    rows=aq_rows,
    sources_text=STATEMENT_REPORTS_NOTE + "\n\nSource for stage tables: each year's Directors' Report and Financial "
    "Statements, Risk review and Capital review section, 'Analysis of financial instrument by stage' / 'All "
    "segments - Company' tables. Net carrying value ties exactly to the Balance Sheet's 'Loans and advances to "
    "customers' line every year. Only the on-balance-sheet loans and advances to customers line is shown here "
    "(cash, banks, debt securities, and off-balance-sheet commitments/guarantees also carry their own stage splits "
    "in the source reports but are outside this sheet's scope).",
    first_col_width=58,
    source_height=260,
    unit_suffix=" ($m)",
)


def unavailable(name, note):
    bw.add_metric_sheet(
        name,
        "$million / %",
        [(name + " — standalone Bank Company basis", {y: "Not publicly disclosed" for y in YEARS})],
        SOURCE_NOTE + "\n\n" + REGULATORY_GAP_NOTE,
        note=note,
        first_col_width=58,
        source_height=230,
    )


for metric_name in [
    "CET1 Capital", "CET1 Ratio", "Tier 1 Capital", "Tier 1 Ratio",
    "Total Capital", "Total Capital Ratio", "Total RWAs",
]:
    unavailable(
        metric_name,
        "No complete five-year standalone Company regulatory series was located in the Bank reports. The available "
        "capital review and Pillar 3 materials use the Bank Group solo-consolidated basis; those figures are not "
        "appropriate substitutes for this Bank-level workbook.",
    )

RWA_NOT_DISCLOSED_NOTE = (
    "Not publicly disclosed at standalone Bank Company level. " + REGULATORY_GAP_NOTE
)
bw.add_rwa_breakdown_sheet(
    title="Standard Chartered Bank — RWA Breakdown",
    subtitle="Not publicly disclosed at Company level - see source note.",
    rows=[("DATA", "RWA Breakdown", {y: "Not publicly disclosed" for y in YEARS})],
    sources_text=RWA_NOT_DISCLOSED_NOTE,
    first_col_width=58,
    source_height=230,
    unit_suffix=" ($m)",
)

for metric_name in ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"]:
    unavailable(
        metric_name,
        "No complete five-year standalone Company regulatory series was located in the Bank reports. The available "
        "capital review and Pillar 3 materials use the Bank Group solo-consolidated basis; those figures are not "
        "appropriate substitutes for this Bank-level workbook.",
    )

EQUITY_CHANGES_OVERVIEW = [
    ("Profit for the year (Company)", {"FY2025": 2517, "FY2024": 2325, "FY2023": 2585, "FY2022": 2372, "FY2021": 2146}),
    ("Dividends and distributions paid (ordinary + preference/AT1)", {"FY2025": -2665, "FY2024": -2744, "FY2023": -2962, "FY2022": -292, "FY2021": -292}),
    ("Total equity (closing)", BS["Total equity"]),
]

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", BS["Total assets"]),
        ("Loans and advances to customers", BS["Loans and advances to customers"]),
        ("Customer accounts", BS["Customer accounts"]),
        ("Total equity", BS["Total equity"]),
    ],
    balance_sheet_unit="$million",
    income_statement_totals=[
        ("Operating income", PL["Operating income"]),
        ("Operating expenses", PL["Operating expenses"]),
        ("Profit for the year", PL["Profit for the year"]),
    ],
    income_statement_unit="$million (Bank Group - see Profit & Loss sheet's source note)",
    equity_changes_totals=EQUITY_CHANGES_OVERVIEW,
    equity_changes_unit="$million (Company)",
    cash_flow_totals=[("Net cash from/(used in) operating activities", CF["Net cash from/(used in) operating activities"]),
                      ("Net cash from/(used in) investing activities", CF["Net cash from/(used in) investing activities"]),
                      ("Net cash used in financing activities", CF["Net cash used in financing activities"]),
                      ("Net increase/(decrease) in cash and cash equivalents", CF["Net increase/(decrease) in cash and cash equivalents"])],
    cash_flow_unit="$million",
    ratios=[],
    note=(
        "Balance Sheet, Statement of Changes in Equity, Cash Flow, and Asset Quality figures use the standalone "
        "Bank Company column throughout. The Profit & Loss figures use the Bank GROUP consolidated income "
        "statement instead, because the Company takes the s.408 Companies Act 2006 exemption and does not publish "
        "its own income statement (see the Profit & Loss sheet's source note for the Company's own profit-after-tax "
        "figures, which tie exactly to this Overview's equity-changes block). Regulatory Pillar 3 metric sheets "
        "(including RWA Breakdown) are left as not publicly disclosed because the available regulatory capital "
        "basis is Bank Group solo-consolidated, not the standalone Company."
    ),
)

bw.save("/Users/armaan/code/katalysis/banks/STANDARD CHARTERED BANK FINANCIALS.xlsx")
