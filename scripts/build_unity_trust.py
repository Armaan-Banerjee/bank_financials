import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://assets.unity.co.uk/Unity-Trust-Bank-Annual-Report-and-Accounts-2025.pdf"
AR2024_URL = "https://assets.unity.co.uk/Unity-Trust-Bank-Annual-Report-and-Accounts-2024.pdf"
AR2023_URL = "https://assets.unity.co.uk/U798_0324_Unity_Trust_Bank_Annual-Report-and-Accounts_2023.pdf"
AR2021_URL = "https://assets.unity.co.uk/2022/08/Unity-Trust-Bank_Report-and-Accounts-2021.pdf"

P3_2025_URL = "https://assets.unity.co.uk/Unity-Trust-Bank-PILLAR3-2025-1.pdf"
P3_2024_URL = "https://assets.unity.co.uk/Unity-Trust-Bank-PILLAR3-2024.pdf"
P3_2023_URL = "https://assets.unity.co.uk/Unity-Trust-Bank-PILLAR3-2023-1.pdf"
P3_2022_URL = "https://assets.unity.co.uk/2023/03/Unity-Trust-Bank_2022-Pillar-3-Disclosures.pdf"
P3_2021_URL = "https://assets.unity.co.uk/2022/08/PILLAR3-2021-FINAL.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Unity Trust Bank Plc (FRN 204570) is an independent UK bank with no ultimate parent company - "
    "owned by a mix of trade unions, co-operative and charitable bodies, and other institutions, focused on "
    "lending to charities, social enterprises, housing providers, SMEs and public sector bodies. Its own accounts "
    "state it 'does not have an ultimate parent company'. The Bank presents its results on an 'extended entity "
    "basis' combining itself with a small dormant subsidiary, Unity EBT Limited (the trustee of an employee share "
    "scheme, one £1 ordinary share, 100% held) - not a full IFRS 10 consolidation, which the Bank elected not to "
    "apply on materiality grounds (Companies Act 2006 s405(2)); in practice this makes no discernible difference "
    "to the figures. All years reconcile exactly (operating + investing + financing = net change; opening + net "
    "change = closing) with no restatements or presentation-basis changes across the 5 years covered."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Unity Trust Bank Plc's own Statement of Cash Flows, £'000:\n"
    f"FY2025: Report & Accounts 2025, p.51 (Statement of Cash Flows) - {AR2025_URL}\n"
    f"FY2024: Report & Accounts 2024, p.39 (Statement of Cash Flows) - {AR2024_URL}\n"
    f"FY2023: Report & Accounts 2023, p.41-42 (Statement of Cash Flows) - {AR2023_URL}\n"
    f"FY2022: Report & Accounts 2023, p.41-42 (Statement of Cash Flows, 2022 comparative column) - {AR2023_URL}\n"
    f"FY2021: Report & Accounts 2021, p.35-36 (Statement of Cash Flows) - {AR2021_URL}\n"
    "Each year's own report was used for its own column (FY2022 taken from the FY2023 report's comparative, since "
    "no standalone FY2022 annual report was separately sourced); every year's own figure was cross-checked against "
    "its appearance as the following year's comparative column and matched exactly in every case - no material "
    "arithmetic errors found, no presentation-basis restatements across the 5 years (FY2025's single 'Finance "
    "costs' line was split into lease/central-bank components that year only, kept on separate rows). FY2022's "
    "operating-activities line items sum to £1k more than the operating total as printed (immaterial rounding, not "
    "corrected).\n\n"
    + ENTITY_NOTE
)


def p3_sources(page="6"):
    return (
        "Sources - Unity Trust Bank Plc Pillar 3 Disclosures, 'Summary of Key Metrics' table:\n"
        f"FY2025: Pillar 3 Disclosures 2025, p.{page} - {P3_2025_URL}\n"
        f"FY2024: Pillar 3 Disclosures 2024, p.6 - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures 2023, p.6 - {P3_2023_URL}\n"
        f"FY2022: Pillar 3 Disclosures 2022, p.5 - {P3_2022_URL}\n"
        f"FY2021: Pillar 3 Disclosures 2021, p.4 (Tier 1/Total Capital and NSFR rows sourced instead from the "
        f"following year's comparative column, Pillar 3 Disclosures 2022, p.5, since the 2021 report itself only "
        f"published CET1 and LCR) - {P3_2021_URL} / {P3_2022_URL}"
    )


bw = BankWorkbook(bank_name="Unity Trust Bank Plc", years=YEARS, year_label=YEAR_LABEL, header_color="7A0C2E")

STATEMENTS_SOURCES = (
    "Sources - all figures are Unity Trust Bank Plc's own primary statements, £'000:\n"
    f"FY2025 & FY2024: Report & Accounts 2025, p.47 (Income Statement/Statement of Comprehensive Income), "
    f"p.48 (Statement of Financial Position), p.49-50 (Statement of Changes in Equity) - {AR2025_URL}\n"
    f"FY2023 & FY2022: Report & Accounts 2023, p.77-78 (Income Statement), p.79 (Statement of Financial "
    f"Position), p.81 (Statement of Changes in Equity, 2022 comparative) - {AR2023_URL}\n"
    f"FY2021: Report & Accounts 2021, p.31 (Income Statement), p.33 (Statement of Financial Position), "
    f"p.34 (Statement of Changes in Equity) - {AR2021_URL}\n\n"
    "PRESENTATION NOTE: the Statement of Changes in Equity gained a 'Cash flow hedge reserve' column from "
    "FY2024 onward (the Bank had no cash flow hedges before then) - left blank for FY2021-FY2023 rows rather "
    "than shown as zero, since the column didn't exist in those years' own statements. FY2023's own printed "
    "'At 31 December 2023' Total equity in the equity statement (£172,167k) is a text-extraction/OCR digit "
    "transposition in the source table - the correct figure, cross-checked against (a) the components summing "
    "exactly (24,792+18,205+4,511-3,041+128,229-79 = 172,617) and (b) the Balance Sheet's own independently-"
    "stated Total equity (£172,617k) and the FY2025 report's own 'At 1 January 2024' comparative (£172,617k), "
    "is £172,617k - used here.\n\n"
    + ENTITY_NOTE
)

ASSET_QUALITY_SOURCES = (
    "Sources - Unity Trust Bank Plc's own 'Gross balance movements in the year' (ECL stage) tables:\n"
    f"FY2025: Report & Accounts 2025, p.32 (Risk Management) - {AR2025_URL}\n"
    f"FY2024: Report & Accounts 2024, p.24 (Risk Management, own originally-published figures, not AR2025's "
    f"restated comparative - see presentation note below) - {AR2024_URL}\n"
    f"FY2023: Report & Accounts 2023, p.26 (Risk Management) - {AR2023_URL}\n"
    f"FY2022: Report & Accounts 2023, p.27 (Risk Management, 2022 comparative column) - {AR2023_URL}\n"
    f"FY2021: Report & Accounts 2021, p.64 (Notes to the Financial Statements) - {AR2021_URL}\n\n"
    "SCOPE NOTE: this table 'includes loans and advances to customers, including pipeline commitments and "
    "investment securities' (per the Bank's own footnote) - a broader scope than the Balance Sheet's "
    "'Loans and advances to customers' line alone, so gross carrying amounts here do not tie to that line; "
    "reproduced faithfully from each year's own disclosure, not forced to a narrower scope.\n\n"
    "PRESENTATION NOTE: from the FY2025 report onward, this table excludes treasury investments (per the "
    "Bank's own footnote: 'the table has been updated to align the asset composition... treasury investments "
    "are no longer included'); FY2021-FY2024 all include treasury investments. FY2024's figures shown here "
    "are its own originally-published ones (from Report & Accounts 2024) - AR2025's own FY2024 comparative "
    "column re-presents FY2024 excluding treasury investments too (a different, smaller figure), which is not "
    "used here per project convention (each year's own originally-published figure). This creates a genuine, "
    "documented scope break between FY2024's closing balance and FY2025's opening balance (both labelled "
    "'as at 1 January 2025'/'as at 31 December 2024' but on different scopes) - not a data error.\n\n"
    "Derived ratios: NPL ratio = Stage 3 gross carrying amount / Total gross carrying amount. Coverage ratio "
    "= Total impairment provision / Total gross carrying amount. Stage 3 coverage = Stage 3 impairment "
    "provision / Stage 3 gross carrying amount.\n\n"
    + ENTITY_NOTE
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - Unity Trust Bank Plc's own 'Risk weighted exposure amounts and Pillar 1 capital requirements' "
    "tables (Standardised approach; not a UK OV1-formatted table, but the Bank's own full RWA-by-category "
    "breakdown):\n"
    f"FY2025 & FY2024: Pillar 3 Disclosures 2025, p.15 - {P3_2025_URL}\n"
    f"FY2023 & FY2022: Pillar 3 Disclosures 2023, p.17 - {P3_2023_URL}\n"
    f"FY2021: Pillar 3 Disclosures 2021, p.15 - {P3_2021_URL}\n\n"
    "Each year's category rows sum exactly to that year's own Total RWA figure (see Total RWAs sheet). A "
    "separate 'Credit Valuation Adjustment' risk category first appears in the FY2024 Pillar 3 report - "
    "FY2021-FY2023 have no such line (left blank, not zero, since the category wasn't disclosed those years)."
)


def _stage_pct(numerator, denominator):
    return f"{100 * numerator / denominator:.2f}%"


# ---------------------------------------------------------------
# Sheet 1: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances with the Bank of England", {"FY2025": 218684, "FY2024": 621898, "FY2023": 476613, "FY2022": 567701, "FY2021": 680112}),
    ("DATA", "Loans and advances to banks", {"FY2025": 2059, "FY2024": 2689, "FY2023": 1799, "FY2021": 529}),
    ("DATA", "Investment securities - fair value through OCI", {"FY2025": 587595, "FY2024": 314130}),
    ("DATA", "Investment securities - amortised cost", {"FY2025": 232581}),
    ("DATA", "Investment securities (FY2023-FY2021, not split by measurement basis)", {"FY2023": 247416, "FY2022": 256638, "FY2021": 207632}),
    ("DATA", "Derivative financial instruments", {"FY2025": 579}),
    ("DATA", "Loans and advances to customers", {"FY2025": 1133097, "FY2024": 1013816, "FY2023": 1013646, "FY2022": 836576, "FY2021": 723523}),
    ("DATA", "Right of use assets", {"FY2025": 782, "FY2024": 1025, "FY2023": 1307, "FY2022": 1581, "FY2021": 1824}),
    ("DATA", "Pension scheme net assets", {"FY2025": 1423, "FY2024": 1122, "FY2023": 2341, "FY2022": 3788, "FY2021": 7095}),
    ("DATA", "Other assets", {"FY2025": 815, "FY2024": 56, "FY2023": 109, "FY2022": 278, "FY2021": 126}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 2403, "FY2024": 1448, "FY2023": 1535, "FY2022": 1149, "FY2021": 1090}),
    ("DATA", "Current tax assets", {"FY2025": 5936, "FY2023": 0, "FY2022": 0, "FY2021": 43}),
    ("DATA", "Deferred tax assets", {"FY2024": 235, "FY2023": 451, "FY2022": 793}),
    ("DATA", "Property, plant and equipment", {"FY2025": 1353, "FY2024": 870, "FY2023": 585, "FY2022": 653, "FY2021": 760}),
    ("DATA", "Intangible assets", {"FY2025": 446, "FY2023": 6, "FY2022": 22, "FY2021": 60}),
    ("TOTAL", "Total assets", {"FY2025": 2187753, "FY2024": 1957289, "FY2023": 1745808, "FY2022": 1669179, "FY2021": 1622794}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Central bank facilities", {"FY2025": 50145}),
    ("DATA", "Amounts owed to banks", {"FY2022": 85}),
    ("DATA", "Customer deposits", {"FY2025": 1861280, "FY2024": 1717204, "FY2023": 1559309, "FY2022": 1538657, "FY2021": 1507227}),
    ("DATA", "Derivative financial instruments", {"FY2025": 51, "FY2024": 1674}),
    ("DATA", "Other liabilities", {"FY2025": 4211, "FY2024": 3404, "FY2023": 3858, "FY2022": 3448, "FY2021": 3689}),
    ("DATA", "Accruals and deferred income", {"FY2025": 3821, "FY2024": 2814, "FY2023": 1830, "FY2022": 1493, "FY2021": 1111}),
    ("DATA", "Provisions for liabilities and charges", {"FY2025": 3207, "FY2024": 1992, "FY2023": 670, "FY2022": 368, "FY2021": 175}),
    ("DATA", "Current tax liabilities", {"FY2024": 8084, "FY2023": 7524, "FY2022": 1313, "FY2021": 0}),
    ("DATA", "Deferred tax liabilities", {"FY2025": 1044, "FY2021": 1629}),
    ("TOTAL", "Total liabilities", {"FY2025": 1923759, "FY2024": 1735172, "FY2023": 1573191, "FY2022": 1545364, "FY2021": 1513831}),
    ("SECTION", "Equity", {}),
    ("DATA", "Ordinary share capital", {"FY2025": 24881, "FY2024": 24825, "FY2023": 24792, "FY2022": 24730, "FY2021": 24678}),
    ("DATA", "Share premium account", {"FY2025": 18360, "FY2024": 18263, "FY2023": 18205, "FY2022": 18150, "FY2021": 18113}),
    ("DATA", "Capital redemption reserve", {"FY2025": 4511, "FY2024": 4511, "FY2023": 4511, "FY2022": 4511, "FY2021": 4511}),
    ("DATA", "Retained earnings", {"FY2025": 214350, "FY2024": 176336, "FY2023": 128229, "FY2022": 81615, "FY2021": 62040}),
    ("DATA", "Financial asset valuation reserve (FVTOCI)", {"FY2025": 1115, "FY2024": -617, "FY2023": -3041, "FY2022": -5131, "FY2021": -342}),
    ("DATA", "Cash flow hedge reserve", {"FY2025": 777, "FY2024": -1141}),
    ("DATA", "Employee share ownership plan (ESOP) reserve", {"FY2025": 0, "FY2024": -60, "FY2023": -79, "FY2022": -60, "FY2021": -37}),
    ("TOTAL", "Total equity", {"FY2025": 263994, "FY2024": 222117, "FY2023": 172617, "FY2022": 123815, "FY2021": 108963}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 2187753, "FY2024": 1957289, "FY2023": 1745808, "FY2022": 1669179, "FY2021": 1622794}),
]

bw.add_balance_sheet_sheet(
    title="Unity Trust Bank Plc — Statement of Financial Position",
    subtitle="Extended entity basis (Bank + Unity EBT Limited), £'000",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=64,
    source_height=200,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet 2: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable and similar income", {"FY2025": 118236, "FY2024": 122813}),
    ("DATA", "Interest income under EIR method", {"FY2023": 102947, "FY2022": 47121, "FY2021": 21693}),
    ("DATA", "Interest expense and similar charges", {"FY2025": -26011, "FY2024": -23561, "FY2023": -13762, "FY2022": -3327, "FY2021": -204}),
    ("TOTAL", "Net Interest Income", {"FY2025": 92225, "FY2024": 99252, "FY2023": 89185, "FY2022": 43794, "FY2021": 21489}),
    ("DATA", "Fee and commission income", {"FY2025": 4362, "FY2024": 4205, "FY2023": 4405, "FY2022": 4548, "FY2021": 4422}),
    ("DATA", "Fee and commission expense", {"FY2025": -1561, "FY2024": -1360, "FY2023": -1169, "FY2022": -1159, "FY2021": -774}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 2801, "FY2024": 2845, "FY2023": 3236, "FY2022": 3389, "FY2021": 3648}),
    ("TOTAL", "Total income", {"FY2025": 95026, "FY2024": 102097, "FY2023": 92421, "FY2022": 47183, "FY2021": 25137}),
    ("DATA", "Operating expenses", {"FY2025": -41377, "FY2024": -33314, "FY2023": -25011, "FY2022": -17354, "FY2021": -13614}),
    ("DATA", "Losses on financial instruments held at fair value", {"FY2025": -28, "FY2024": -2015}),
    ("DATA", "Impairment charge", {"FY2025": -1206, "FY2024": -1017, "FY2023": -3548, "FY2022": -2477, "FY2021": -470}),
    ("TOTAL", "Profit before taxation", {"FY2025": 52415, "FY2024": 65751, "FY2023": 63862, "FY2022": 27352, "FY2021": 11053}),
    ("DATA", "Taxation charge", {"FY2025": -11626, "FY2024": -15275, "FY2023": -15004, "FY2022": -4509, "FY2021": -1382}),
    ("TOTAL", "Profit for the year attributable to shareholders", {"FY2025": 40789, "FY2024": 50476, "FY2023": 48858, "FY2022": 22843, "FY2021": 9671}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Movement in cash flow hedge reserve: gains/(losses) taken to reserves", {"FY2025": 1460, "FY2024": -1521}),
    ("DATA", "Movement in cash flow hedge reserve: reclassification to profit or loss", {"FY2025": 1097}),
    ("DATA", "Movement in cash flow hedge reserve: taxation", {"FY2025": -639, "FY2024": 380}),
    ("DATA", "Movement in financial asset revaluation reserve: valuation gains/(losses) taken to equity", {"FY2025": 2309, "FY2024": 3232, "FY2023": 2672, "FY2022": -6385, "FY2021": -1193}),
    ("DATA", "Movement in financial asset revaluation reserve: taxation", {"FY2025": -577, "FY2024": -808, "FY2023": -582, "FY2022": 1596, "FY2021": 256}),
    ("DATA", "Actuarial gains/(losses) on defined benefit obligations", {"FY2025": 590, "FY2024": -1047, "FY2023": -1311, "FY2022": -3170, "FY2021": 2718}),
    ("DATA", "Actuarial gains/(losses): taxation", {"FY2025": -148, "FY2024": 258, "FY2023": 335, "FY2022": 799, "FY2021": -953}),
    ("TOTAL", "Other comprehensive income/(charges) for the year, net of tax", {"FY2025": 4092, "FY2024": 494, "FY2023": 1114, "FY2022": -7160, "FY2021": 828}),
    ("TOTAL", "Total comprehensive income for the year - equity shareholders", {"FY2025": 44881, "FY2024": 50970, "FY2023": 49972, "FY2022": 15683, "FY2021": 10499}),
    ("DATA", "Dividend paid in the year", {"FY2025": -2979, "FY2024": -1734, "FY2023": -1361, "FY2022": -949, "FY2021": -741}),
]

bw.add_income_statement_sheet(
    title="Unity Trust Bank Plc — Statement of Comprehensive Income",
    subtitle="Extended entity basis (Bank + Unity EBT Limited), £'000",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=70,
    source_height=200,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet 3: Statement of Changes in Equity
# ---------------------------------------------------------------
equity_headers = ["Share capital", "Share premium", "Capital redemption reserve", "FVTOCI", "Retained earnings", "Cash flow hedge reserve", "ESOP reserve", "Total equity"]

equity_rows = [
    ("TOTAL", "At 1 January 2021", (22421, 11808, 4511, 595, 51334, None, None, 90669)),
    ("DATA", "Profit for the financial year", (None, None, None, None, 9671, None, None, 9671)),
    ("DATA", "Issue of share capital - Capital raise", (2205, 6277, None, None, None, None, None, 8482)),
    ("DATA", "Issue of share capital - Share Incentive Plan", (52, 28, None, None, None, None, None, 80)),
    ("DATA", "Adjustment for equity-settled share-based payments", (None, None, None, None, 11, None, -37, -26)),
    ("DATA", "Actuarial gain on Defined Benefit pension", (None, None, None, None, 2718, None, None, 2718)),
    ("DATA", "Deferred Tax movements", (None, None, None, 256, -953, None, None, -697)),
    ("DATA", "Net movement in Fair value through other comprehensive income", (None, None, None, -1193, None, None, None, -1193)),
    ("DATA", "Dividend paid", (None, None, None, None, -741, None, None, -741)),
    ("TOTAL", "At 31 December 2021", (24678, 18113, 4511, -342, 62040, None, -37, 108963)),
    ("DATA", "Profit for the financial year", (None, None, None, None, 22843, None, None, 22843)),
    ("DATA", "Issue of share capital - Share Incentive Plan", (52, 37, None, None, None, None, None, 89)),
    ("DATA", "Adjustment for equity-settled share-based payments", (None, None, None, None, 52, None, -23, 29)),
    ("DATA", "Actuarial gain/(loss) on Defined Benefit pension", (None, None, None, None, -3170, None, None, -3170)),
    ("DATA", "Deferred Tax movements", (None, None, None, 1596, 799, None, None, 2395)),
    ("DATA", "Net movement in Fair value through other comprehensive income", (None, None, None, -6385, None, None, None, -6385)),
    ("DATA", "Dividend paid", (None, None, None, None, -949, None, None, -949)),
    ("TOTAL", "At 31 December 2022", (24730, 18150, 4511, -5131, 81615, None, -60, 123815)),
    ("DATA", "Profit for the financial year", (None, None, None, None, 48858, None, None, 48858)),
    ("DATA", "Issue of share capital - Share Incentive Plan", (62, 55, None, None, None, None, -49, 68)),
    ("DATA", "Adjustment for equity-settled share-based payments", (None, None, None, None, 93, None, 30, 123)),
    ("DATA", "Actuarial loss on Defined Benefit pension", (None, None, None, None, -1311, None, None, -1311)),
    ("DATA", "Deferred Tax movements", (None, None, None, -582, 335, None, None, -247)),
    ("DATA", "Net movement in Fair value through other comprehensive income", (None, None, None, 2672, None, None, None, 2672)),
    ("DATA", "Dividend paid", (None, None, None, None, -1361, None, None, -1361)),
    ("TOTAL", "At 31 December 2023 (£172,617k, see presentation note; text-extraction artefact in source table corrected)", (24792, 18205, 4511, -3041, 128229, None, -79, 172617)),
    ("DATA", "Profit for the financial year", (None, None, None, None, 50476, None, None, 50476)),
    ("DATA", "Issue of share capital - Share Incentive Plan", (33, 58, None, None, None, None, -23, 68)),
    ("DATA", "Adjustment for equity-settled share-based payments", (None, None, None, None, 154, None, 42, 196)),
    ("DATA", "Actuarial loss on Defined Benefit pension", (None, None, None, None, -1047, None, None, -1047)),
    ("DATA", "Fair value on cash flow hedges", (None, None, None, None, None, -1521, None, -1521)),
    ("DATA", "Deferred Tax movements", (None, None, None, -808, 258, 380, None, -170)),
    ("DATA", "Net movement in Fair value through other comprehensive income", (None, None, None, 3232, None, None, None, 3232)),
    ("DATA", "Dividend paid", (None, None, None, None, -1734, None, None, -1734)),
    ("TOTAL", "At 31 December 2024", (24825, 18263, 4511, -617, 176336, -1141, -60, 222117)),
    ("DATA", "Profit for the financial year", (None, None, None, None, 40789, None, None, 40789)),
    ("DATA", "Issue of share capital - Share Incentive Plan", (50, 77, None, None, None, None, -40, 87)),
    ("DATA", "Adjustment for equity-settled share-based payments", (6, 20, None, None, -320, None, 100, -194)),
    ("DATA", "Actuarial gain on Defined Benefit pension", (None, None, None, None, 590, None, None, 590)),
    ("DATA", "Fair value on cash flow hedges", (None, None, None, None, None, 1460, None, 1460)),
    ("DATA", "Recycling of cash flow hedge reserve", (None, None, None, None, None, 1097, None, 1097)),
    ("DATA", "Deferred Tax movements", (None, None, None, -577, -66, -639, None, -1282)),
    ("DATA", "Net movement in Fair value through other comprehensive income", (None, None, None, 2309, None, None, None, 2309)),
    ("DATA", "Dividend paid", (None, None, None, None, -2979, None, None, -2979)),
    ("TOTAL", "At 31 December 2025", (24881, 18360, 4511, 1115, 214350, 777, 0, 263994)),
]

bw.add_equity_changes_sheet(
    title="Unity Trust Bank Plc — Statement of Changes in Equity",
    subtitle="Extended entity basis (Bank + Unity EBT Limited), £'000, chronological (oldest to newest). Each year's closing Total equity ties exactly to that year's own Balance Sheet Total equity and to the next year's opening balance - zero undocumented plug rows across all 5 years.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=60,
    source_height=220,
    col_width=17,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before taxation", {"FY2025": 52415, "FY2024": 65751, "FY2023": 63862, "FY2022": 27352, "FY2021": 11053}),
    ("DATA", "Finance costs on lease liabilities", {"FY2025": 58}),
    ("DATA", "Finance costs on central bank facilities", {"FY2025": 145}),
    ("DATA", "Finance costs (combined, as reported)", {"FY2024": 73, "FY2023": 85, "FY2022": 249, "FY2021": 240}),
    ("DATA", "Impairment losses, net of reversals, on financial assets", {"FY2025": 1206, "FY2024": 1017, "FY2023": 3548, "FY2022": 2477, "FY2021": 470}),
    ("DATA", "Non-cash movements in relation to investment securities", {"FY2025": -24580, "FY2024": -10770, "FY2023": -8428, "FY2022": -3871}),
    ("DATA", "Depreciation of property, plant and equipment", {"FY2025": 368, "FY2024": 280, "FY2023": 283, "FY2022": 270, "FY2021": 305}),
    ("DATA", "Depreciation of right-of-use assets", {"FY2025": 262, "FY2024": 266, "FY2023": 250, "FY2022": 269, "FY2021": 276}),
    ("DATA", "Amortisation of intangible assets", {"FY2025": 15, "FY2024": 6, "FY2023": 16, "FY2022": 38, "FY2021": 50}),
    ("DATA", "Loss on disposal of property, plant and equipment", {"FY2024": 0, "FY2023": 3, "FY2021": 12}),
    ("DATA", "Increase/(decrease) in provisions", {"FY2025": 1642, "FY2024": 1441, "FY2023": 567, "FY2022": 320, "FY2021": 88}),
    ("DATA", "Fair value loss on derivatives", {"FY2025": 1106, "FY2024": 153}),
    ("DATA", "Share-based payment expense", {"FY2025": 853, "FY2024": 174}),
    ("DATA", "Pension administration expense", {"FY2025": 289, "FY2024": 172}),
    ("DATA", "Other non-cash movements", {"FY2021": 244}),
    ("DATA", "(Increase)/decrease in prepayments and accrued income", {"FY2025": -955, "FY2024": 87, "FY2023": -386, "FY2022": -59, "FY2021": -424}),
    ("DATA", "(Increase)/decrease in other operating assets", {"FY2025": -759, "FY2024": 69, "FY2023": 155, "FY2022": -151, "FY2021": 28}),
    ("DATA", "(Increase) in derivatives", {"FY2025": -770}),
    ("DATA", "Increase in loans and advances to customers", {"FY2025": -120381, "FY2024": -1187, "FY2023": -180618, "FY2022": -115530, "FY2021": -122183}),
    ("DATA", "(Increase)/decrease in Bank of England mandatory reserve", {"FY2024": 3448, "FY2023": 310, "FY2022": -355, "FY2021": -1294}),
    ("DATA", "Increase/(decrease) in accruals and deferred income", {"FY2025": 1007, "FY2024": 984, "FY2023": 337, "FY2022": 382, "FY2021": 28}),
    ("DATA", "Increase in customer deposits", {"FY2025": 144076, "FY2024": 157895, "FY2023": 20652, "FY2022": 31430, "FY2021": 171502}),
    ("DATA", "Increase/(decrease) in other operating liabilities", {"FY2025": -251, "FY2024": -361, "FY2023": 527, "FY2022": -101, "FY2021": 655}),
    ("DATA", "Income tax paid", {"FY2025": -25649, "FY2024": -14668, "FY2023": -8698, "FY2022": -3180, "FY2021": -1328}),
    ("TOTAL", "Net cash generated from/(used in) operating activities", {"FY2025": 30097, "FY2024": 204830, "FY2023": -107535, "FY2022": -60460, "FY2021": 59722}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -852, "FY2024": -565, "FY2023": -218, "FY2022": -163, "FY2021": -390}),
    ("DATA", "Intangible asset additions", {"FY2025": -461, "FY2021": 0}),
    ("DATA", "Interest received from investment securities", {"FY2025": 23945}),
    ("DATA", "Purchase of investment securities", {"FY2025": -576821, "FY2024": -159028, "FY2023": -96260, "FY2022": -261001, "FY2021": -30302}),
    ("DATA", "Proceeds from sale and redemption of investment securities", {"FY2025": 73615, "FY2024": 106314, "FY2023": 116948, "FY2022": 209523, "FY2021": 73666}),
    ("TOTAL", "Net cash generated from/(used in) investing activities", {"FY2025": -480574, "FY2024": -53279, "FY2023": 20470, "FY2022": -51641, "FY2021": 42974}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividends paid", {"FY2025": -2979, "FY2024": -1734, "FY2023": -1361, "FY2022": -949, "FY2021": -741}),
    ("DATA", "Repayment of lease liabilities", {"FY2025": -474, "FY2024": -285, "FY2023": -468, "FY2022": -380, "FY2021": -186}),
    ("DATA", "Proceeds on issue of share capital, net of transaction costs", {"FY2025": 86, "FY2024": 91, "FY2023": 0, "FY2022": 50, "FY2021": 8520}),
    ("DATA", "Drawdown on central bank facilities", {"FY2025": 50000}),
    ("TOTAL", "Net cash generated from/(used in) financing activities", {"FY2025": 46633, "FY2024": -1928, "FY2023": -1829, "FY2022": -1279, "FY2021": 7593}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -403844, "FY2024": 149623, "FY2023": -88894, "FY2022": -113380, "FY2021": 110289}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 624587, "FY2024": 474964, "FY2023": 563858, "FY2022": 677238, "FY2021": 566949}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 220743, "FY2024": 624587, "FY2023": 474964, "FY2022": 563858, "FY2021": 677238}),
]

bw.add_cash_flow_sheet(
    title="Unity Trust Bank Plc — Statement of Cash Flows",
    subtitle="Extended entity basis (Bank + Unity EBT Limited), £'000",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=170,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Gross carrying amount by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (12 month ECL)", {"FY2025": 1155109, "FY2024": 1321056, "FY2023": 1244119, "FY2022": 1093651, "FY2021": 958279}),
    ("DATA", "Stage 2 (Lifetime ECL - SICR)", {"FY2025": 38911, "FY2024": 42399, "FY2023": 43080, "FY2022": 39504, "FY2021": 17591}),
    ("DATA", "Stage 3 (Lifetime ECL - credit impaired)", {"FY2025": 29356, "FY2024": 29358, "FY2023": 24903, "FY2022": 6314, "FY2021": 5374}),
    ("TOTAL", "Total gross carrying amount", {"FY2025": 1223376, "FY2024": 1392813, "FY2023": 1312102, "FY2022": 1139469, "FY2021": 981244}),
    ("SECTION", "Impairment provision by IFRS 9 stage", {}),
    ("DATA", "Stage 1 provision", {"FY2025": 2856, "FY2024": 2708, "FY2023": 4145, "FY2022": 2848, "FY2021": 556}),
    ("DATA", "Stage 2 provision", {"FY2025": 1592, "FY2024": 1457, "FY2023": 2313, "FY2022": 1394, "FY2021": 966}),
    ("DATA", "Stage 3 provision", {"FY2025": 6905, "FY2024": 5599, "FY2023": 3233, "FY2022": 1891, "FY2021": 2134}),
    ("TOTAL", "Total impairment provision", {"FY2025": 11353, "FY2024": 9764, "FY2023": 9691, "FY2022": 6133, "FY2021": 3656}),
    ("TOTAL", "Net carrying amount (Total gross - Total provision)", {"FY2025": 1212023, "FY2024": 1383049, "FY2023": 1302411, "FY2022": 1133336, "FY2021": 977588}),
    ("SECTION", "Derived asset quality ratios", {}),
    ("DATA", "NPL ratio (Stage 3 gross / Total gross)", {"FY2025": _stage_pct(29356, 1223376), "FY2024": _stage_pct(29358, 1392813), "FY2023": _stage_pct(24903, 1312102), "FY2022": _stage_pct(6314, 1139469), "FY2021": _stage_pct(5374, 981244)}),
    ("DATA", "Total coverage ratio (Total provision / Total gross)", {"FY2025": _stage_pct(11353, 1223376), "FY2024": _stage_pct(9764, 1392813), "FY2023": _stage_pct(9691, 1312102), "FY2022": _stage_pct(6133, 1139469), "FY2021": _stage_pct(3656, 981244)}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 provision / Stage 3 gross)", {"FY2025": _stage_pct(6905, 29356), "FY2024": _stage_pct(5599, 29358), "FY2023": _stage_pct(3233, 24903), "FY2022": _stage_pct(1891, 6314), "FY2021": _stage_pct(2134, 5374)}),
]

bw.add_asset_quality_sheet(
    title="Unity Trust Bank Plc — Asset Quality",
    subtitle="Extended entity basis (Bank + Unity EBT Limited), £'000 - loans and advances to customers (incl. pipeline commitments) and investment securities by IFRS 9 stage",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=64,
    source_height=230,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=48, source_height=130)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 259127, "FY2024": 222740, "FY2023": 172898, "FY2022": 122931, "FY2021": 104260})],
    p3_sources(),
    note="The Bank has no Additional Tier 1 or Tier 2 capital instruments in any year shown - CET1 capital, Tier 1 "
         "capital and Total capital are identical figures throughout.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("CET1 ratio", {"FY2025": "24.33%", "FY2024": "24.05%", "FY2023": "19.68%", "FY2022": "18.27%", "FY2021": "17.7%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2025": 259127, "FY2024": 222740, "FY2023": 172898, "FY2022": 122931, "FY2021": 104260})],
    p3_sources(),
    note="Equal to CET1 capital in every year - the Bank has no Additional Tier 1 capital instruments.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "24.33%", "FY2024": "24.05%", "FY2023": "19.68%", "FY2022": "18.27%", "FY2021": "17.69%"})],
    p3_sources(),
    note="FY2021's own Pillar 3 report only stated a CET1 ratio (no separate Tier 1 figure); the FY2021 Tier 1 "
         "ratio shown here (17.69%) is taken from the FY2022 Pillar 3 report's own FY2021 comparative column, "
         "which confirms Tier 1 capital equalled CET1 capital that year too.",
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2025": 259127, "FY2024": 222740, "FY2023": 172898, "FY2022": 122931, "FY2021": 104260})],
    p3_sources(),
    note="Equal to CET1 capital in every year - the Bank has no Tier 2 capital instruments.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "24.33%", "FY2024": "24.05%", "FY2023": "19.68%", "FY2022": "18.27%", "FY2021": "17.69%"})],
    p3_sources(),
    note="FY2021's own Pillar 3 report only stated a CET1 ratio; the FY2021 figure shown here is taken from the "
         "FY2022 Pillar 3 report's own FY2021 comparative column (see Tier 1 Ratio sheet note).",
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted assets (RWA)", {"FY2025": 1065248, "FY2024": 925984, "FY2023": 878472, "FY2022": 672893, "FY2021": 589551})],
    p3_sources(),
)

rwa_breakdown_rows = [
    ("DATA", "Total credit risk", {"FY2025": 883650, "FY2024": 774294, "FY2023": 775509, "FY2022": 613975, "FY2021": 550200}),
    ("DATA", "Operational risk", {"FY2025": 180965, "FY2024": 151062, "FY2023": 102963, "FY2022": 58918, "FY2021": 39351}),
    ("DATA", "Credit Valuation Adjustment", {"FY2025": 633, "FY2024": 628}),
    ("TOTAL", "Total RWA", {"FY2025": 1065248, "FY2024": 925984, "FY2023": 878472, "FY2022": 672893, "FY2021": 589551}),
]

bw.add_rwa_breakdown_sheet(
    title="Unity Trust Bank Plc — RWA Breakdown",
    subtitle="Risk weighted exposure amounts by category, Standardised approach, £'000",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=54,
    source_height=150,
    unit_suffix=" (£'000)",
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Total UK leverage ratio exposure measure", {"FY2025": 2045234, "FY2024": 1394612}),
        ("UK leverage ratio, excl. temporary central bank reserves exemption (%)", {"FY2025": "12.67%", "FY2024": "15.97%"}),
        ("Total Basel III leverage ratio exposure measure", {"FY2025": 2263918, "FY2024": 2016510, "FY2023": 1797760, "FY2022": 1710211, "FY2021": 1673611}),
        ("Basel III leverage ratio, incl. temporary central bank reserves exemption (%)", {"FY2025": "11.45%", "FY2024": "11.05%", "FY2023": "9.62%", "FY2022": "7.19%", "FY2021": "5.7%"}),
    ],
    p3_sources(),
    note="Unity introduced a separate 'UK leverage ratio' (excluding the temporary central bank reserves "
         "exemption) alongside its existing 'Basel III leverage ratio' (including that exemption) from the FY2024 "
         "Pillar 3 report onward - FY2021-FY2023 only ever disclosed the Basel III basis. FY2021's Basel III "
         "leverage ratio is shown here as originally reported that year (5.7%); the FY2022 Pillar 3 report's own "
         "FY2021 comparative column restates this to 6.23% (including)/6.22% (excluding the exemption) - a basis "
         "change, not a data error, so the original 5.7% figure is kept as the primary FY2021 value.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA)", {"FY2025": 915263, "FY2024": 913969, "FY2023": 697018, "FY2022": 782783, "FY2021": 822783}),
        ("Total net cash outflow", {"FY2025": 405412, "FY2024": 400945, "FY2023": 332338, "FY2022": 355595, "FY2021": 303007}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "225.76%", "FY2024": "227.95%", "FY2023": "210%", "FY2022": "220%", "FY2021": "272%"}),
    ],
    p3_sources(),
    note="LCR figures are as at year-end (31 December), not a trailing average - per the Pillar 3 report's own "
         "footnote, this does not agree to the average LCR balances disclosed elsewhere in the same report.",
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding", {"FY2025": 1420532, "FY2024": 1303839, "FY2023": 1200480, "FY2022": 1144865, "FY2021": 1077138}),
        ("Total required stable funding", {"FY2025": 955318, "FY2024": 845763, "FY2023": 909694, "FY2022": 741481, "FY2021": 628367}),
        ("Net Stable Funding Ratio (%)", {"FY2025": "148.70%", "FY2024": "154.16%", "FY2023": "131.97%", "FY2022": "154.4%", "FY2021": "171.4%"}),
    ],
    p3_sources(),
    note="FY2021's own Pillar 3 report did not disclose NSFR at all; the FY2021 figures shown here are taken from "
         "the FY2022 Pillar 3 report's own FY2021 comparative column instead.",
)

metric(
    "MREL Ratio", None,
    [("MREL requirement (= Total Capital Requirement, %)", {"FY2025": "10.69%", "FY2024": "10.69%", "FY2023": "10.69%", "FY2022": "10.10%", "FY2021": "10.14%"})],
    p3_sources(),
    note="Unity is in the lowest resolution risk category, where its MREL requirement is set to equal its Total "
         "Capital Requirement (TCR) - no separate numeric MREL resources figure or MREL ratio distinct from TCR is "
         "published in any year.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 2187753, "FY2024": 1957289, "FY2023": 1745808, "FY2022": 1669179, "FY2021": 1622794}),
        ("Loans and advances to customers", {"FY2025": 1133097, "FY2024": 1013816, "FY2023": 1013646, "FY2022": 836576, "FY2021": 723523}),
        ("Customer deposits", {"FY2025": 1861280, "FY2024": 1717204, "FY2023": 1559309, "FY2022": 1538657, "FY2021": 1507227}),
        ("Total equity", {"FY2025": 263994, "FY2024": 222117, "FY2023": 172617, "FY2022": 123815, "FY2021": 108963}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total income", {"FY2025": 95026, "FY2024": 102097, "FY2023": 92421, "FY2022": 47183, "FY2021": 25137}),
        ("Operating expenses", {"FY2025": -41377, "FY2024": -33314, "FY2023": -25011, "FY2022": -17354, "FY2021": -13614}),
        ("Profit for the year", {"FY2025": 40789, "FY2024": 50476, "FY2023": 48858, "FY2022": 22843, "FY2021": 9671}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 222117, "FY2024": 172617, "FY2023": 123815, "FY2022": 108963, "FY2021": 90669}),
        ("Total comprehensive income for the year", {"FY2025": 44881, "FY2024": 50970, "FY2023": 49972, "FY2022": 15683, "FY2021": 10499}),
        ("Other equity movements, net", {"FY2025": -3004, "FY2024": -1470, "FY2023": -1170, "FY2022": -831, "FY2021": 7795}),
        ("Closing equity", {"FY2025": 263994, "FY2024": 222117, "FY2023": 172617, "FY2022": 123815, "FY2021": 108963}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 30097, "FY2024": 204830, "FY2023": -107535, "FY2022": -60460, "FY2021": 59722}),
        ("Net cash from/(used in) investing activities", {"FY2025": -480574, "FY2024": -53279, "FY2023": 20470, "FY2022": -51641, "FY2021": 42974}),
        ("Net cash from/(used in) financing activities", {"FY2025": 46633, "FY2024": -1928, "FY2023": -1829, "FY2022": -1279, "FY2021": 7593}),
        ("Cash and cash equivalents at end of year", {"FY2025": 220743, "FY2024": 624587, "FY2023": 474964, "FY2022": 563858, "FY2021": 677238}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "24.33%", "FY2024": "24.05%", "FY2023": "19.68%", "FY2022": "18.27%", "FY2021": "17.7%"}),
        ("Tier 1 Ratio", {"FY2025": "24.33%", "FY2024": "24.05%", "FY2023": "19.68%", "FY2022": "18.27%", "FY2021": "17.69%"}),
        ("Total Capital Ratio", {"FY2025": "24.33%", "FY2024": "24.05%", "FY2023": "19.68%", "FY2022": "18.27%", "FY2021": "17.69%"}),
        ("Leverage Ratio (Basel III)", {"FY2025": "11.45%", "FY2024": "11.05%", "FY2023": "9.62%", "FY2022": "7.19%", "FY2021": "5.7%"}),
        ("LCR", {"FY2025": "225.76%", "FY2024": "227.95%", "FY2023": "210%", "FY2022": "220%", "FY2021": "272%"}),
        ("NSFR", {"FY2025": "148.70%", "FY2024": "154.16%", "FY2023": "131.97%", "FY2022": "154.4%", "FY2021": "171.4%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Leverage Ratio shown on the Basel III basis (available for "
         "all 5 years) rather than the UK basis (only introduced from FY2024) - see Leverage Ratio sheet for both.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/UNITY TRUST FINANCIALS.xlsx")
