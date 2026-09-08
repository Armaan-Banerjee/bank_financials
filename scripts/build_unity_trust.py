import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://assets.unity.co.uk/Unity-Trust-Bank-Annual-Report-and-Accounts-2025.pdf"
AR2024_URL = "https://assets.unity.co.uk/Unity-Trust-Bank-Annual-Report-and-Accounts-2024.pdf"
AR2023_URL = "https://assets.unity.co.uk/U798_0324_Unity_Trust_Bank_Annual-Report-and-Accounts_2023.pdf"
AR2021_URL = "https://assets.unity.co.uk/2022/08/Unity-Trust-Bank_Report-and-Accounts-2021.pdf"
# FY2018-FY2020 Annual Report & Accounts are no longer hosted on unity.co.uk (live or via Wayback
# Machine - checked); each year's own accounts were instead sourced from its own Companies House
# filing (Unity Trust Bank Plc, company no. 01713124).
CH_2020_URL = "https://find-and-update.company-information.service.gov.uk/company/01713124/filing-history/MzI5NzIyNTE1N2FkaXF6a2N4/document?format=pdf&download=0"
CH_2019_URL = "https://find-and-update.company-information.service.gov.uk/company/01713124/filing-history/MzI2NzM2MDE4NWFkaXF6a2N4/document?format=pdf&download=0"
CH_2018_URL = "https://find-and-update.company-information.service.gov.uk/company/01713124/filing-history/MzIzMTYwOTI0NmFkaXF6a2N4/document?format=pdf&download=0"

P3_2025_URL = "https://assets.unity.co.uk/Unity-Trust-Bank-PILLAR3-2025-1.pdf"
P3_2024_URL = "https://assets.unity.co.uk/Unity-Trust-Bank-PILLAR3-2024.pdf"
P3_2023_URL = "https://assets.unity.co.uk/Unity-Trust-Bank-PILLAR3-2023-1.pdf"
P3_2022_URL = "https://assets.unity.co.uk/2023/03/Unity-Trust-Bank_2022-Pillar-3-Disclosures.pdf"
P3_2021_URL = "https://assets.unity.co.uk/2022/08/PILLAR3-2021-FINAL.pdf"
# FY2020 Pillar 3 disclosures no longer live on unity.co.uk - recovered via Wayback Machine.
P3_2020_URL = "https://web.archive.org/web/20221124023931/https://assets.unity.co.uk/2022/08/PILLAR3-2020-Final.pdf"
# FY2019 Pillar 3 disclosures are still live at this URL (checked directly, not just via a prior scan).
P3_2019_URL = "https://assets.unity.co.uk/Unity-Trust-Bank-PILLAR3-2019.pdf"
# FY2018 Pillar 3 disclosures ("PILLAR3-2018-Final-Clean.pdf") are genuinely unobtainable - not live
# on unity.co.uk and the only Wayback Machine capture of that URL is a 345-byte error page, not the
# PDF (checked via a full CDX search of the unity.co.uk domain for every "pillar" filename ever
# archived - no other candidate filename found either). FY2018's Pillar 3 figures used throughout
# this script are instead taken from the FY2019 Pillar 3 report's own FY2018 comparative column.

ENTITY_NOTE = (
    "ENTITY NOTE: Unity Trust Bank Plc (FRN 204570) is an independent UK bank with no ultimate parent company - "
    "owned by a mix of trade unions, co-operative and charitable bodies, and other institutions, focused on "
    "lending to charities, social enterprises, housing providers, SMEs and public sector bodies. Its own accounts "
    "state it 'does not have an ultimate parent company'. The Bank presents its results on an 'extended entity "
    "basis' combining itself with a small dormant subsidiary, Unity EBT Limited (the trustee of an employee share "
    "scheme, one £1 ordinary share, 100% held) - not a full IFRS 10 consolidation, which the Bank elected not to "
    "apply on materiality grounds (Companies Act 2006 s405(2)); in practice this makes no discernible difference "
    "to the figures. All years reconcile exactly (operating + investing + financing = net change; opening + net "
    "change = closing) with no restatements or presentation-basis changes across the 8 years covered (FY2018-FY2025). "
    "The Bank adopted IFRS 9 with effect from 1 January 2018 (comparative FY2017 not restated - not itself in the "
    "years covered here) and IFRS 16 with effect from 1 January 2019 (Right-of-use assets first appear FY2019 "
    "onward; FY2018 has none)."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Unity Trust Bank Plc's own Statement of Cash Flows, £'000:\n"
    f"FY2025: Report & Accounts 2025, p.51 (Statement of Cash Flows) - {AR2025_URL}\n"
    f"FY2024: Report & Accounts 2024, p.39 (Statement of Cash Flows) - {AR2024_URL}\n"
    f"FY2023: Report & Accounts 2023, p.41-42 (Statement of Cash Flows) - {AR2023_URL}\n"
    f"FY2022: Report & Accounts 2023, p.41-42 (Statement of Cash Flows, 2022 comparative column) - {AR2023_URL}\n"
    f"FY2021: Report & Accounts 2021, p.35-36 (Statement of Cash Flows) - {AR2021_URL}\n"
    f"FY2020: Report & Accounts 2020 (Companies House filing, 13 Apr 2021), p.27 (Statement of Cash Flows) - {CH_2020_URL}\n"
    f"FY2019: Report & Accounts 2019 (Companies House filing, 25 Jun 2020), p.23 (Statement of Cash Flows) - {CH_2019_URL}\n"
    f"FY2018: Report & Accounts 2018 (Companies House filing, 11 Apr 2019), p.21 (Statement of Cash Flows) - {CH_2018_URL}\n"
    "Each year's own report was used for its own column (FY2022 taken from the FY2023 report's comparative, since "
    "no standalone FY2022 annual report was separately sourced); every year's own figure was cross-checked against "
    "its appearance as the following year's comparative column and matched exactly in every case - no material "
    "arithmetic errors found, no presentation-basis restatements across the 8 years (FY2025's single 'Finance "
    "costs' line was split into lease/central-bank components that year only, kept on separate rows). FY2022's "
    "operating-activities line items sum to £1k more than the operating total as printed (immaterial rounding, not "
    "corrected). FY2018's closing cash of £280,923k ties exactly to FY2019's opening cash; FY2019's closing "
    "£300,958k ties exactly to FY2020's opening cash; FY2020's closing £566,949k ties exactly to FY2021's opening "
    "cash - continuous across the pre-2021 extension with no basis break. FY2018 predates IFRS 16 (no lease "
    "liability repayment line, no separate depreciation-of-right-of-use-assets line - a single combined "
    "'Depreciation and amortisation' line is used instead, see below) and its cash flow statement also shows a "
    "one-off 'Buy back of own shares' financing outflow (£2,534k, from the share buyback/cancellation described in "
    "the Statement of Changes in Equity) not seen in any other year.\n\n"
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
        f"published CET1 and LCR) - {P3_2021_URL} / {P3_2022_URL}\n"
        f"FY2020: Pillar 3 Disclosures 2020, p.3 - {P3_2020_URL}\n"
        f"FY2019: Pillar 3 Disclosures 2019, p.3 - {P3_2019_URL}\n"
        f"FY2018: Pillar 3 Disclosures 2019, p.3 (2018 comparative column) - {P3_2019_URL} - a standalone FY2018 "
        f"Pillar 3 document is not obtainable (not live on unity.co.uk, and the only Wayback Machine capture of "
        f"its known filename is a 345-byte error page, not the PDF - checked via a full CDX search of the "
        f"unity.co.uk domain for every 'pillar' filename ever archived, not just the one filename a prior scan "
        f"had flagged)."
    )


bw = BankWorkbook(bank_name="Unity Trust Bank Plc", years=YEARS, year_label=YEAR_LABEL, header_color="7A0C2E")

STATEMENTS_SOURCES = (
    "Sources - all figures are Unity Trust Bank Plc's own primary statements, £'000:\n"
    f"FY2025 & FY2024: Report & Accounts 2025, p.47 (Income Statement/Statement of Comprehensive Income), "
    f"p.48 (Statement of Financial Position), p.49-50 (Statement of Changes in Equity) - {AR2025_URL}\n"
    f"FY2023 & FY2022: Report & Accounts 2023, p.77-78 (Income Statement), p.79 (Statement of Financial "
    f"Position), p.81 (Statement of Changes in Equity, 2022 comparative) - {AR2023_URL}\n"
    f"FY2021: Report & Accounts 2021, p.31 (Income Statement), p.33 (Statement of Financial Position), "
    f"p.34 (Statement of Changes in Equity) - {AR2021_URL}\n"
    f"FY2020: Report & Accounts 2020 (Companies House filing, 13 Apr 2021), p.23 (Income Statement), p.24 "
    f"(Statement of Comprehensive Income), p.25 (Statement of Financial Position), p.26 (Statement of Changes "
    f"in Equity) - {CH_2020_URL}\n"
    f"FY2019: Report & Accounts 2019 (Companies House filing, 25 Jun 2020), p.19 (Income Statement), p.20 "
    f"(Statement of Comprehensive Income), p.21 (Statement of Financial Position), p.22 (Statement of Changes "
    f"in Equity) - {CH_2019_URL}\n"
    f"FY2018: Report & Accounts 2018 (Companies House filing, 11 Apr 2019), p.17 (Income Statement), p.18 "
    f"(Statement of Comprehensive Income), p.19 (Statement of Financial Position), p.20 (Statement of Changes "
    f"in Equity) - {CH_2018_URL}\n\n"
    "PRESENTATION NOTE: the Statement of Changes in Equity gained a 'Cash flow hedge reserve' column from "
    "FY2024 onward (the Bank had no cash flow hedges before then) - left blank for FY2018-FY2023 rows rather "
    "than shown as zero, since the column didn't exist in those years' own statements. FY2023's own printed "
    "'At 31 December 2023' Total equity in the equity statement (£172,167k) is a text-extraction/OCR digit "
    "transposition in the source table - the correct figure, cross-checked against (a) the components summing "
    "exactly (24,792+18,205+4,511-3,041+128,229-79 = 172,617) and (b) the Balance Sheet's own independently-"
    "stated Total equity (£172,617k) and the FY2025 report's own 'At 1 January 2024' comparative (£172,617k), "
    "is £172,617k - used here.\n\n"
    "IFRS 9 TRANSITION NOTE: the Bank adopted IFRS 9 with effect from 1 January 2018 using the modified "
    "retrospective approach permitted by the standard, so FY2017 (not itself covered by this workbook) was not "
    "restated. The FY2018 Statement of Changes in Equity accordingly shows an 'Effects of changes in accounting "
    "policies' adjustment of £(277)k to retained earnings between the reported 'At 31 December 2017' balance "
    "(£60,096k) and the restated 'At 1 January 2018' opening balance (£59,819k) actually rolled forward through "
    "FY2018 - not a correction of an error, a one-off transition adjustment. FY2018's Statement of Financial "
    "Position also has no Right-of-use assets line (pre-IFRS 16; first appears FY2019) and its Statement of "
    "Changes in Equity includes a one-off FY2018-only 'Issue of share capital' and 'Own shares acquired during "
    "the financial year' pair of movements (a capital raise plus a buyback-and-cancellation of shares, per the "
    "Report of the Directors) not seen in any other year shown.\n\n"
    + ENTITY_NOTE
)

ASSET_QUALITY_SOURCES = (
    "Sources - Unity Trust Bank Plc's own 'Gross balance movements in the year' (ECL stage) tables:\n"
    f"FY2025: Report & Accounts 2025, p.32 (Risk Management) - {AR2025_URL}\n"
    f"FY2024: Report & Accounts 2024, p.24 (Risk Management, own originally-published figures, not AR2025's "
    f"restated comparative - see presentation note below) - {AR2024_URL}\n"
    f"FY2023: Report & Accounts 2023, p.26 (Risk Management) - {AR2023_URL}\n"
    f"FY2022: Report & Accounts 2023, p.27 (Risk Management, 2022 comparative column) - {AR2023_URL}\n"
    f"FY2021: Report & Accounts 2021, p.64 (Notes to the Financial Statements) - {AR2021_URL}\n"
    f"FY2020: Report & Accounts 2020 (Companies House filing), note 26 'Financial risk management' - Credit "
    f"risk analysis, p.50 - {CH_2020_URL}\n"
    f"FY2019: Report & Accounts 2019 (Companies House filing), note 26 'Financial risk management' - Credit "
    f"risk analysis, p.46 - {CH_2019_URL}\n"
    f"FY2018: Report & Accounts 2019 (Companies House filing), note 26 'Financial risk management' - Credit "
    f"risk analysis, p.47 (2018 comparative column) - {CH_2019_URL}\n\n"
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
    f"FY2021: Pillar 3 Disclosures 2021, p.15 - {P3_2021_URL}\n"
    f"FY2020 & FY2019: Pillar 3 Disclosures 2020, p.15 - {P3_2020_URL}\n"
    f"FY2018: Pillar 3 Disclosures 2019, p.14 (2018 comparative column) - {P3_2019_URL}\n\n"
    "Each year's category rows sum exactly to that year's own Total RWA figure (see Total RWAs sheet). A "
    "separate 'Credit Valuation Adjustment' risk category first appears in the FY2024 Pillar 3 report - "
    "FY2018-FY2023 have no such line (left blank, not zero, since the category wasn't disclosed those years)."
)


def _stage_pct(numerator, denominator):
    return f"{100 * numerator / denominator:.2f}%"


# ---------------------------------------------------------------
# Sheet 1: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances with the Bank of England", {"FY2025": 218684, "FY2024": 621898, "FY2023": 476613, "FY2022": 567701, "FY2021": 680112, "FY2020": 568804, "FY2019": 301858, "FY2018": 280390}),
    ("DATA", "Loans and advances to banks", {"FY2025": 2059, "FY2024": 2689, "FY2023": 1799, "FY2021": 529, "FY2020": 254, "FY2019": 2, "FY2018": 1243}),
    ("DATA", "Investment securities - fair value through OCI", {"FY2025": 587595, "FY2024": 314130}),
    ("DATA", "Investment securities - amortised cost", {"FY2025": 232581}),
    ("DATA", "Investment securities (FY2023-FY2018, not split by measurement basis)", {"FY2023": 247416, "FY2022": 256638, "FY2021": 207632, "FY2020": 252413, "FY2019": 331713, "FY2018": 426368}),
    ("DATA", "Derivative financial instruments", {"FY2025": 579}),
    ("DATA", "Loans and advances to customers", {"FY2025": 1133097, "FY2024": 1013816, "FY2023": 1013646, "FY2022": 836576, "FY2021": 723523, "FY2020": 601810, "FY2019": 477554, "FY2018": 362446}),
    ("DATA", "Right of use assets", {"FY2025": 782, "FY2024": 1025, "FY2023": 1307, "FY2022": 1581, "FY2021": 1824, "FY2020": 2099, "FY2019": 2381}),
    ("DATA", "Pension scheme net assets", {"FY2025": 1423, "FY2024": 1122, "FY2023": 2341, "FY2022": 3788, "FY2021": 7095, "FY2020": 4501, "FY2019": 6700, "FY2018": 4020}),
    ("DATA", "Other assets", {"FY2025": 815, "FY2024": 56, "FY2023": 109, "FY2022": 278, "FY2021": 126, "FY2020": 154, "FY2019": 172, "FY2018": 48}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 2403, "FY2024": 1448, "FY2023": 1535, "FY2022": 1149, "FY2021": 1090, "FY2020": 666, "FY2019": 787, "FY2018": 964}),
    ("DATA", "Current tax assets", {"FY2025": 5936, "FY2023": 0, "FY2022": 0, "FY2021": 43, "FY2020": 96, "FY2019": 0, "FY2018": 0}),
    ("DATA", "Deferred tax assets", {"FY2024": 235, "FY2023": 451, "FY2022": 793}),
    ("DATA", "Property, plant and equipment", {"FY2025": 1353, "FY2024": 870, "FY2023": 585, "FY2022": 653, "FY2021": 760, "FY2020": 687, "FY2019": 904, "FY2018": 1195}),
    ("DATA", "Intangible assets", {"FY2025": 446, "FY2023": 6, "FY2022": 22, "FY2021": 60, "FY2020": 110, "FY2019": 135, "FY2018": 220}),
    ("TOTAL", "Total assets", {"FY2025": 2187753, "FY2024": 1957289, "FY2023": 1745808, "FY2022": 1669179, "FY2021": 1622794, "FY2020": 1431594, "FY2019": 1122206, "FY2018": 1076894}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Central bank facilities", {"FY2025": 50145}),
    ("DATA", "Amounts owed to banks", {"FY2022": 85}),
    ("DATA", "Customer deposits", {"FY2025": 1861280, "FY2024": 1717204, "FY2023": 1559309, "FY2022": 1538657, "FY2021": 1507227, "FY2020": 1335725, "FY2019": 1030435, "FY2018": 998130}),
    ("DATA", "Derivative financial instruments", {"FY2025": 51, "FY2024": 1674}),
    ("DATA", "Other liabilities", {"FY2025": 4211, "FY2024": 3404, "FY2023": 3858, "FY2022": 3448, "FY2021": 3689, "FY2020": 2978, "FY2019": 3326, "FY2018": 479}),
    ("DATA", "Accruals and deferred income", {"FY2025": 3821, "FY2024": 2814, "FY2023": 1830, "FY2022": 1493, "FY2021": 1111, "FY2020": 1083, "FY2019": 1581, "FY2018": 1527}),
    ("DATA", "Provisions for liabilities and charges", {"FY2025": 3207, "FY2024": 1992, "FY2023": 670, "FY2022": 368, "FY2021": 175, "FY2020": 209, "FY2019": 416, "FY2018": 274}),
    ("DATA", "Current tax liabilities", {"FY2024": 8084, "FY2023": 7524, "FY2022": 1313, "FY2021": 0, "FY2020": 0, "FY2019": 330, "FY2018": 708}),
    ("DATA", "Deferred tax liabilities", {"FY2025": 1044, "FY2021": 1629, "FY2020": 930, "FY2019": 986, "FY2018": 353}),
    ("TOTAL", "Total liabilities", {"FY2025": 1923759, "FY2024": 1735172, "FY2023": 1573191, "FY2022": 1545364, "FY2021": 1513831, "FY2020": 1340925, "FY2019": 1037074, "FY2018": 1001471}),
    ("SECTION", "Equity", {}),
    ("DATA", "Ordinary share capital", {"FY2025": 24881, "FY2024": 24825, "FY2023": 24792, "FY2022": 24730, "FY2021": 24678, "FY2020": 22421, "FY2019": 22421, "FY2018": 22421}),
    ("DATA", "Share premium account", {"FY2025": 18360, "FY2024": 18263, "FY2023": 18205, "FY2022": 18150, "FY2021": 18113, "FY2020": 11808, "FY2019": 11808, "FY2018": 11808}),
    ("DATA", "Capital redemption reserve", {"FY2025": 4511, "FY2024": 4511, "FY2023": 4511, "FY2022": 4511, "FY2021": 4511, "FY2020": 4511, "FY2019": 4511, "FY2018": 4511}),
    ("DATA", "Retained earnings", {"FY2025": 214350, "FY2024": 176336, "FY2023": 128229, "FY2022": 81615, "FY2021": 62040, "FY2020": 51334, "FY2019": 46850, "FY2018": 37555}),
    ("DATA", "Financial asset valuation reserve (FVTOCI)", {"FY2025": 1115, "FY2024": -617, "FY2023": -3041, "FY2022": -5131, "FY2021": -342, "FY2020": 595, "FY2019": -458, "FY2018": -872}),
    ("DATA", "Cash flow hedge reserve", {"FY2025": 777, "FY2024": -1141}),
    ("DATA", "Employee share ownership plan (ESOP) reserve", {"FY2025": 0, "FY2024": -60, "FY2023": -79, "FY2022": -60, "FY2021": -37}),
    ("TOTAL", "Total equity", {"FY2025": 263994, "FY2024": 222117, "FY2023": 172617, "FY2022": 123815, "FY2021": 108963, "FY2020": 90669, "FY2019": 85132, "FY2018": 75423}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 2187753, "FY2024": 1957289, "FY2023": 1745808, "FY2022": 1669179, "FY2021": 1622794, "FY2020": 1431594, "FY2019": 1122206, "FY2018": 1076894}),
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
    ("DATA", "Interest income under EIR method", {"FY2023": 102947, "FY2022": 47121, "FY2021": 21693, "FY2020": 19513, "FY2019": 21336, "FY2018": 16874}),
    ("DATA", "Interest expense and similar charges", {"FY2025": -26011, "FY2024": -23561, "FY2023": -13762, "FY2022": -3327, "FY2021": -204, "FY2020": -854, "FY2019": -2002, "FY2018": -1323}),
    ("TOTAL", "Net Interest Income", {"FY2025": 92225, "FY2024": 99252, "FY2023": 89185, "FY2022": 43794, "FY2021": 21489, "FY2020": 18659, "FY2019": 19334, "FY2018": 15551}),
    ("DATA", "Fee and commission income", {"FY2025": 4362, "FY2024": 4205, "FY2023": 4405, "FY2022": 4548, "FY2021": 4422, "FY2020": 4257, "FY2019": 4483, "FY2018": 3944}),
    ("DATA", "Fee and commission expense", {"FY2025": -1561, "FY2024": -1360, "FY2023": -1169, "FY2022": -1159, "FY2021": -774, "FY2020": -968, "FY2019": -1175, "FY2018": -1124}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 2801, "FY2024": 2845, "FY2023": 3236, "FY2022": 3389, "FY2021": 3648, "FY2020": 3289, "FY2019": 3308, "FY2018": 2820}),
    ("TOTAL", "Total income", {"FY2025": 95026, "FY2024": 102097, "FY2023": 92421, "FY2022": 47183, "FY2021": 25137, "FY2020": 21948, "FY2019": 22642, "FY2018": 18371}),
    ("TOTAL", "Operating expenses", {"FY2025": -41377, "FY2024": -33314, "FY2023": -25011, "FY2022": -17354, "FY2021": -13614, "FY2020": -12614, "FY2019": -13315, "FY2018": -10623}),
    ("DATA", "Losses on financial instruments held at fair value", {"FY2025": -28, "FY2024": -2015}),
    ("DATA", "Impairment charge/(credit) on loans and advances", {"FY2025": -1206, "FY2024": -1017, "FY2023": -3548, "FY2022": -2477, "FY2021": -470, "FY2020": -1788, "FY2019": -251, "FY2018": 52}),
    ("DATA", "Exceptional pension scheme related costs (exit from Pace multi-employer DB scheme, FY2018 only)", {"FY2018": -1045}),
    ("TOTAL", "Profit before taxation", {"FY2025": 52415, "FY2024": 65751, "FY2023": 63862, "FY2022": 27352, "FY2021": 11053, "FY2020": 7546, "FY2019": 9076, "FY2018": 6755}),
    ("DATA", "Taxation charge", {"FY2025": -11626, "FY2024": -15275, "FY2023": -15004, "FY2022": -4509, "FY2021": -1382, "FY2020": -519, "FY2019": -1095, "FY2018": -788}),
    ("TOTAL", "Profit for the year attributable to shareholders", {"FY2025": 40789, "FY2024": 50476, "FY2023": 48858, "FY2022": 22843, "FY2021": 9671, "FY2020": 7027, "FY2019": 7981, "FY2018": 5967}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Movement in cash flow hedge reserve: gains/(losses) taken to reserves", {"FY2025": 1460, "FY2024": -1521}),
    ("DATA", "Movement in cash flow hedge reserve: reclassification to profit or loss", {"FY2025": 1097}),
    ("DATA", "Movement in cash flow hedge reserve: taxation", {"FY2025": -639, "FY2024": 380}),
    ("DATA", "Initial recognition of DB pension surplus (FY2018 only - exit from Pace multi-employer scheme)", {"FY2018": 4277}),
    ("DATA", "FVTOCI: prior year charges (FY2018 only)", {"FY2018": -28}),
    ("DATA", "Movement in financial asset revaluation reserve: valuation gains/(losses) taken to equity", {"FY2025": 2309, "FY2024": 3232, "FY2023": 2672, "FY2022": -6385, "FY2021": -1193, "FY2020": 1253, "FY2019": 532, "FY2018": -1891}),
    ("DATA", "FVTOCI: reclassification adjustments included in profit (FY2018 only)", {"FY2018": -10}),
    ("DATA", "Movement in financial asset revaluation reserve: taxation", {"FY2025": -577, "FY2024": -808, "FY2023": -582, "FY2022": 1596, "FY2021": 256, "FY2020": -200, "FY2019": -118, "FY2018": 322}),
    ("DATA", "Actuarial gains/(losses) on defined benefit obligations", {"FY2025": 590, "FY2024": -1047, "FY2023": -1311, "FY2022": -3170, "FY2021": 2718, "FY2020": -2142, "FY2019": 2731, "FY2018": -275}),
    ("DATA", "Actuarial gains/(losses): taxation", {"FY2025": -148, "FY2024": 258, "FY2023": 335, "FY2022": 799, "FY2021": -953, "FY2020": 272, "FY2019": -464, "FY2018": -680}),
    ("TOTAL", "Other comprehensive income/(charges) for the year, net of tax", {"FY2025": 4092, "FY2024": 494, "FY2023": 1114, "FY2022": -7160, "FY2021": 828, "FY2020": -817, "FY2019": 2681, "FY2018": 1715}),
    ("TOTAL", "Total comprehensive income for the year - equity shareholders", {"FY2025": 44881, "FY2024": 50970, "FY2023": 49972, "FY2022": 15683, "FY2021": 10499, "FY2020": 6210, "FY2019": 10662, "FY2018": 7682}),
    ("DATA", "Dividend paid in the year", {"FY2025": -2979, "FY2024": -1734, "FY2023": -1361, "FY2022": -949, "FY2021": -741, "FY2020": -673, "FY2019": -953, "FY2018": -538}),
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
    ("TOTAL", "At 31 December 2017 (as originally reported, pre-IFRS 9)", (18943, 5563, 3250, 725, 31615, None, None, 60096)),
    ("DATA", "Effects of changes in accounting policies (IFRS 9 transition, 1 January 2018)", (None, None, None, None, -277, None, None, -277)),
    ("TOTAL", "At 1 January 2018 (restated)", (18943, 5563, 3250, 725, 31338, None, None, 59819)),
    ("DATA", "Profit for the financial year", (None, None, None, None, 5967, None, None, 5967)),
    ("DATA", "Initial recognition of DB pension surplus", (None, None, None, None, 3322, None, None, 3322)),
    ("DATA", "FVTOCI: prior year charges, reclassification adjustments, valuation losses and taxation, net", (None, None, None, -1597, None, None, None, -1597)),
    ("DATA", "Issue of share capital - capital raise", (4739, 6245, None, None, None, None, None, 10984)),
    ("DATA", "Own shares acquired during the financial year (buyback and cancellation)", (-1261, None, 1261, None, -2534, None, None, -2534)),
    ("DATA", "Dividend paid", (None, None, None, None, -538, None, None, -538)),
    ("TOTAL", "At 31 December 2018", (22421, 11808, 4511, -872, 37555, None, None, 75423)),
    ("DATA", "Profit for the financial year", (None, None, None, None, 7981, None, None, 7981)),
    ("DATA", "Actuarial gain on Defined Benefit pension", (None, None, None, None, 2731, None, None, 2731)),
    ("DATA", "Deferred Tax movements", (None, None, None, -118, -464, None, None, -582)),
    ("DATA", "Net movement in Fair value through other comprehensive income", (None, None, None, 532, None, None, None, 532)),
    ("DATA", "Dividend paid", (None, None, None, None, -953, None, None, -953)),
    ("TOTAL", "At 31 December 2019", (22421, 11808, 4511, -458, 46850, None, None, 85132)),
    ("DATA", "Profit for the financial year", (None, None, None, None, 7027, None, None, 7027)),
    ("DATA", "Actuarial losses on Defined Benefit pension", (None, None, None, None, -2142, None, None, -2142)),
    ("DATA", "Deferred Tax movements", (None, None, None, -200, 272, None, None, 72)),
    ("DATA", "Net movement in Fair value through other comprehensive income", (None, None, None, 1253, None, None, None, 1253)),
    ("DATA", "Dividend paid", (None, None, None, None, -673, None, None, -673)),
    ("TOTAL", "At 31 December 2020", (22421, 11808, 4511, 595, 51334, None, None, 90669)),
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
    subtitle="Extended entity basis (Bank + Unity EBT Limited), £'000, chronological (oldest to newest). Each year's closing Total equity ties exactly to that year's own Balance Sheet Total equity and to the next year's opening balance - zero undocumented plug rows across all 8 years (the one documented exception being the FY2018 IFRS 9 transition adjustment, itself independently disclosed as such in the Bank's own accounts).",
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
    ("DATA", "Profit before taxation", {"FY2025": 52415, "FY2024": 65751, "FY2023": 63862, "FY2022": 27352, "FY2021": 11053, "FY2020": 7546, "FY2019": 9076, "FY2018": 6755}),
    ("DATA", "Finance costs on lease liabilities", {"FY2025": 58}),
    ("DATA", "Finance costs on central bank facilities", {"FY2025": 145}),
    ("DATA", "Finance costs (combined, as reported)", {"FY2024": 73, "FY2023": 85, "FY2022": 249, "FY2021": 240, "FY2020": 129, "FY2019": 123}),
    ("DATA", "Impairment losses, net of reversals, on financial assets", {"FY2025": 1206, "FY2024": 1017, "FY2023": 3548, "FY2022": 2477, "FY2021": 470, "FY2020": 1788, "FY2019": 251, "FY2018": -52}),
    ("DATA", "Non-cash movements in relation to investment securities", {"FY2025": -24580, "FY2024": -10770, "FY2023": -8428, "FY2022": -3871}),
    ("DATA", "Depreciation of property, plant and equipment", {"FY2025": 368, "FY2024": 280, "FY2023": 283, "FY2022": 270, "FY2021": 305, "FY2020": 321, "FY2019": 310}),
    ("DATA", "Depreciation of right-of-use assets", {"FY2025": 262, "FY2024": 266, "FY2023": 250, "FY2022": 269, "FY2021": 276, "FY2020": 282, "FY2019": 286}),
    ("DATA", "Amortisation of intangible assets", {"FY2025": 15, "FY2024": 6, "FY2023": 16, "FY2022": 38, "FY2021": 50, "FY2020": 91, "FY2019": 85}),
    ("DATA", "Depreciation and amortisation (combined, as reported - pre-IFRS 16, FY2018 only)", {"FY2018": 272}),
    ("DATA", "Loss on disposal of property, plant and equipment", {"FY2024": 0, "FY2023": 3, "FY2021": 12, "FY2020": 47, "FY2019": 105, "FY2018": 56}),
    ("DATA", "Increase/(decrease) in provisions", {"FY2025": 1642, "FY2024": 1441, "FY2023": 567, "FY2022": 320, "FY2021": 88, "FY2020": -17, "FY2019": 142, "FY2018": 124}),
    ("DATA", "Fair value loss on derivatives", {"FY2025": 1106, "FY2024": 153}),
    ("DATA", "Share-based payment expense", {"FY2025": 853, "FY2024": 174}),
    ("DATA", "Pension administration expense", {"FY2025": 289, "FY2024": 172}),
    ("DATA", "Other non-cash movements", {"FY2021": 244, "FY2020": 49}),
    ("DATA", "(Increase)/decrease in prepayments and accrued income", {"FY2025": -955, "FY2024": 87, "FY2023": -386, "FY2022": -59, "FY2021": -424, "FY2020": 121, "FY2019": 177, "FY2018": -206}),
    ("DATA", "(Increase)/decrease in other operating assets", {"FY2025": -759, "FY2024": 69, "FY2023": 155, "FY2022": -151, "FY2021": 28, "FY2020": 18, "FY2019": 126}),
    ("DATA", "(Increase) in derivatives", {"FY2025": -770}),
    ("DATA", "Increase in loans and advances to customers", {"FY2025": -120381, "FY2024": -1187, "FY2023": -180618, "FY2022": -115530, "FY2021": -122183, "FY2020": -126044, "FY2019": -115356, "FY2018": -83356}),
    ("DATA", "(Increase)/decrease in Bank of England mandatory reserve", {"FY2024": 3448, "FY2023": 310, "FY2022": -355, "FY2021": -1294, "FY2020": -1207, "FY2019": -192, "FY2018": -381}),
    ("DATA", "Increase/(decrease) in accruals and deferred income", {"FY2025": 1007, "FY2024": 984, "FY2023": 337, "FY2022": 382, "FY2021": 28, "FY2020": -498, "FY2019": 54, "FY2018": 466}),
    ("DATA", "Increase in customer deposits", {"FY2025": 144076, "FY2024": 157895, "FY2023": 20652, "FY2022": 31430, "FY2021": 171502, "FY2020": 305290, "FY2019": 32305, "FY2018": 48197}),
    ("DATA", "Increase/(decrease) in other operating liabilities", {"FY2025": -251, "FY2024": -361, "FY2023": 527, "FY2022": -101, "FY2021": 655, "FY2020": -254, "FY2019": -106}),
    ("DATA", "Net movement in other operating assets and liabilities (combined, as reported, FY2018 only)", {"FY2018": -621}),
    ("DATA", "Income tax paid", {"FY2025": -25649, "FY2024": -14668, "FY2023": -8698, "FY2022": -3180, "FY2021": -1328, "FY2020": -929, "FY2019": -1422, "FY2018": 0}),
    ("TOTAL", "Net cash generated from/(used in) operating activities", {"FY2025": 30097, "FY2024": 204830, "FY2023": -107535, "FY2022": -60460, "FY2021": 59722, "FY2020": 186733, "FY2019": -74036, "FY2018": -28746}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -852, "FY2024": -565, "FY2023": -218, "FY2022": -163, "FY2021": -390, "FY2020": -132, "FY2019": -124, "FY2018": -1153}),
    ("DATA", "Intangible asset additions", {"FY2025": -461, "FY2021": 0, "FY2020": -85, "FY2019": 0, "FY2018": -162}),
    ("DATA", "Interest received from investment securities", {"FY2025": 23945}),
    ("DATA", "Purchase of investment securities", {"FY2025": -576821, "FY2024": -159028, "FY2023": -96260, "FY2022": -261001, "FY2021": -30302, "FY2020": -42347, "FY2019": -60317, "FY2018": -174045}),
    ("DATA", "Proceeds from sale and redemption of investment securities", {"FY2025": 73615, "FY2024": 106314, "FY2023": 116948, "FY2022": 209523, "FY2021": 73666, "FY2020": 122900, "FY2019": 155503, "FY2018": 120951}),
    ("TOTAL", "Net cash generated from/(used in) investing activities", {"FY2025": -480574, "FY2024": -53279, "FY2023": 20470, "FY2022": -51641, "FY2021": 42974, "FY2020": 80336, "FY2019": 95062, "FY2018": -54409}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividends paid", {"FY2025": -2979, "FY2024": -1734, "FY2023": -1361, "FY2022": -949, "FY2021": -741, "FY2020": -673, "FY2019": -953, "FY2018": -538}),
    ("DATA", "Repayment of lease liabilities", {"FY2025": -474, "FY2024": -285, "FY2023": -468, "FY2022": -380, "FY2021": -186, "FY2020": -405, "FY2019": -38}),
    ("DATA", "Proceeds on issue of share capital, net of transaction costs", {"FY2025": 86, "FY2024": 91, "FY2023": 0, "FY2022": 50, "FY2021": 8520, "FY2018": 10984}),
    ("DATA", "Buy back of own shares (FY2018 only - see Statement of Changes in Equity)", {"FY2018": -2534}),
    ("DATA", "Drawdown on central bank facilities", {"FY2025": 50000}),
    ("TOTAL", "Net cash generated from/(used in) financing activities", {"FY2025": 46633, "FY2024": -1928, "FY2023": -1829, "FY2022": -1279, "FY2021": 7593, "FY2020": -1078, "FY2019": -991, "FY2018": 7912}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -403844, "FY2024": 149623, "FY2023": -88894, "FY2022": -113380, "FY2021": 110289, "FY2020": 265991, "FY2019": 20035, "FY2018": -75243}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 624587, "FY2024": 474964, "FY2023": 563858, "FY2022": 677238, "FY2021": 566949, "FY2020": 300958, "FY2019": 280923, "FY2018": 356166}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 220743, "FY2024": 624587, "FY2023": 474964, "FY2022": 563858, "FY2021": 677238, "FY2020": 566949, "FY2019": 300958, "FY2018": 280923}),
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
    ("DATA", "Stage 1 (12 month ECL)", {"FY2025": 1155109, "FY2024": 1321056, "FY2023": 1244119, "FY2022": 1093651, "FY2021": 958279, "FY2020": 880475, "FY2019": 853511, "FY2018": 834757}),
    ("DATA", "Stage 2 (Lifetime ECL - SICR)", {"FY2025": 38911, "FY2024": 42399, "FY2023": 43080, "FY2022": 39504, "FY2021": 17591, "FY2020": 20347, "FY2019": 12423, "FY2018": 6896}),
    ("DATA", "Stage 3 (Lifetime ECL - credit impaired)", {"FY2025": 29356, "FY2024": 29358, "FY2023": 24903, "FY2022": 6314, "FY2021": 5374, "FY2020": 3820, "FY2019": 2172, "FY2018": 1947}),
    ("TOTAL", "Total gross carrying amount", {"FY2025": 1223376, "FY2024": 1392813, "FY2023": 1312102, "FY2022": 1139469, "FY2021": 981244, "FY2020": 904642, "FY2019": 868106, "FY2018": 843600}),
    ("SECTION", "Impairment provision by IFRS 9 stage", {}),
    ("DATA", "Stage 1 provision", {"FY2025": 2856, "FY2024": 2708, "FY2023": 4145, "FY2022": 2848, "FY2021": 556, "FY2020": 347, "FY2019": 587, "FY2018": 389}),
    ("DATA", "Stage 2 provision", {"FY2025": 1592, "FY2024": 1457, "FY2023": 2313, "FY2022": 1394, "FY2021": 966, "FY2020": 949, "FY2019": 200, "FY2018": 80}),
    ("DATA", "Stage 3 provision", {"FY2025": 6905, "FY2024": 5599, "FY2023": 3233, "FY2022": 1891, "FY2021": 2134, "FY2020": 2121, "FY2019": 854, "FY2018": 1110}),
    ("TOTAL", "Total impairment provision", {"FY2025": 11353, "FY2024": 9764, "FY2023": 9691, "FY2022": 6133, "FY2021": 3656, "FY2020": 3417, "FY2019": 1641, "FY2018": 1579}),
    ("TOTAL", "Net carrying amount (Total gross - Total provision)", {"FY2025": 1212023, "FY2024": 1383049, "FY2023": 1302411, "FY2022": 1133336, "FY2021": 977588, "FY2020": 901225, "FY2019": 866465, "FY2018": 842021}),
    ("SECTION", "Derived asset quality ratios", {}),
    ("DATA", "NPL ratio (Stage 3 gross / Total gross)", {"FY2025": _stage_pct(29356, 1223376), "FY2024": _stage_pct(29358, 1392813), "FY2023": _stage_pct(24903, 1312102), "FY2022": _stage_pct(6314, 1139469), "FY2021": _stage_pct(5374, 981244), "FY2020": _stage_pct(3820, 904642), "FY2019": _stage_pct(2172, 868106), "FY2018": _stage_pct(1947, 843600)}),
    ("DATA", "Total coverage ratio (Total provision / Total gross)", {"FY2025": _stage_pct(11353, 1223376), "FY2024": _stage_pct(9764, 1392813), "FY2023": _stage_pct(9691, 1312102), "FY2022": _stage_pct(6133, 1139469), "FY2021": _stage_pct(3656, 981244), "FY2020": _stage_pct(3417, 904642), "FY2019": _stage_pct(1641, 868106), "FY2018": _stage_pct(1579, 843600)}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 provision / Stage 3 gross)", {"FY2025": _stage_pct(6905, 29356), "FY2024": _stage_pct(5599, 29358), "FY2023": _stage_pct(3233, 24903), "FY2022": _stage_pct(1891, 6314), "FY2021": _stage_pct(2134, 5374), "FY2020": _stage_pct(2121, 3820), "FY2019": _stage_pct(854, 2172), "FY2018": _stage_pct(1110, 1947)}),
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
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 259127, "FY2024": 222740, "FY2023": 172898, "FY2022": 122931, "FY2021": 104260, "FY2020": 87476, "FY2019": 79645, "FY2018": 71801})],
    p3_sources(),
    note="The Bank has no Additional Tier 1 or Tier 2 capital instruments in any year shown - CET1 capital, Tier 1 "
         "capital and Total capital are identical figures throughout. FY2018-FY2020 figures also independently "
         "tie to the CET1 capital shown in each year's own Annual Report & Accounts capital management note.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("CET1 ratio", {"FY2025": "24.33%", "FY2024": "24.05%", "FY2023": "19.68%", "FY2022": "18.27%", "FY2021": "17.7%", "FY2020": "16.7%", "FY2019": "17.6%", "FY2018": "19.3%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2025": 259127, "FY2024": 222740, "FY2023": 172898, "FY2022": 122931, "FY2021": 104260, "FY2020": 87476, "FY2019": 79645, "FY2018": 71801})],
    p3_sources(),
    note="Equal to CET1 capital in every year - the Bank has no Additional Tier 1 capital instruments.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "24.33%", "FY2024": "24.05%", "FY2023": "19.68%", "FY2022": "18.27%", "FY2021": "17.69%", "FY2020": "16.7%", "FY2019": "17.6%", "FY2018": "19.3%"})],
    p3_sources(),
    note="FY2021's own Pillar 3 report only stated a CET1 ratio (no separate Tier 1 figure); the FY2021 Tier 1 "
         "ratio shown here (17.69%) is taken from the FY2022 Pillar 3 report's own FY2021 comparative column, "
         "which confirms Tier 1 capital equalled CET1 capital that year too. FY2018-FY2020's own Pillar 3 reports "
         "likewise only state a single 'Common Equity Tier 1 ratio' - shown here too, since Tier 1 capital equals "
         "CET1 capital in those years as well (no Additional Tier 1 instruments).",
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2025": 259127, "FY2024": 222740, "FY2023": 172898, "FY2022": 122931, "FY2021": 104260, "FY2020": 87476, "FY2019": 79645, "FY2018": 71801})],
    p3_sources(),
    note="Equal to CET1 capital in every year - the Bank has no Tier 2 capital instruments.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "24.33%", "FY2024": "24.05%", "FY2023": "19.68%", "FY2022": "18.27%", "FY2021": "17.69%", "FY2020": "16.7%", "FY2019": "17.6%", "FY2018": "19.3%"})],
    p3_sources(),
    note="FY2021's own Pillar 3 report only stated a CET1 ratio; the FY2021 figure shown here is taken from the "
         "FY2022 Pillar 3 report's own FY2021 comparative column (see Tier 1 Ratio sheet note). FY2018-FY2020 "
         "shown on the same CET1-equals-Total-Capital basis (see Total Capital sheet note).",
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted assets (RWA)", {"FY2025": 1065248, "FY2024": 925984, "FY2023": 878472, "FY2022": 672893, "FY2021": 589551, "FY2020": 524088, "FY2019": 453226, "FY2018": 372156})],
    p3_sources(),
)

rwa_breakdown_rows = [
    ("DATA", "Total credit risk", {"FY2025": 883650, "FY2024": 774294, "FY2023": 775509, "FY2022": 613975, "FY2021": 550200, "FY2020": 484737, "FY2019": 418750, "FY2018": 344214}),
    ("DATA", "Operational risk", {"FY2025": 180965, "FY2024": 151062, "FY2023": 102963, "FY2022": 58918, "FY2021": 39351, "FY2020": 39351, "FY2019": 34476, "FY2018": 27942}),
    ("DATA", "Credit Valuation Adjustment", {"FY2025": 633, "FY2024": 628}),
    ("TOTAL", "Total RWA", {"FY2025": 1065248, "FY2024": 925984, "FY2023": 878472, "FY2022": 672893, "FY2021": 589551, "FY2020": 524088, "FY2019": 453226, "FY2018": 372156}),
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
        ("Total Basel III leverage ratio exposure measure", {"FY2025": 2263918, "FY2024": 2016510, "FY2023": 1797760, "FY2022": 1710211, "FY2021": 1673611, "FY2020": 1481176, "FY2019": 1162383, "FY2018": 1120424}),
        ("Basel III leverage ratio, incl. temporary central bank reserves exemption (%)", {"FY2025": "11.45%", "FY2024": "11.05%", "FY2023": "9.62%", "FY2022": "7.19%", "FY2021": "5.7%", "FY2020": "5.9%", "FY2019": "6.9%", "FY2018": "6.4%"}),
    ],
    p3_sources(),
    note="Unity introduced a separate 'UK leverage ratio' (excluding the temporary central bank reserves "
         "exemption) alongside its existing 'Basel III leverage ratio' (including that exemption) from the FY2024 "
         "Pillar 3 report onward - FY2018-FY2023 only ever disclosed the Basel III basis. FY2021's Basel III "
         "leverage ratio is shown here as originally reported that year (5.7%); the FY2022 Pillar 3 report's own "
         "FY2021 comparative column restates this to 6.23% (including)/6.22% (excluding the exemption) - a basis "
         "change, not a data error, so the original 5.7% figure is kept as the primary FY2021 value. FY2018-FY2020 "
         "ratios shown as each year's own summary 'Summary of Key Metrics' figure (5.9%/6.9%/6.4%); the more "
         "granular 'Leverage ratio common disclosure template' elsewhere in the same reports computes these to "
         "one more decimal place (5.91%/6.85%/6.41%) - an immaterial rounding difference within the same report, "
         "not a restatement.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA)", {"FY2025": 915263, "FY2024": 913969, "FY2023": 697018, "FY2022": 782783, "FY2021": 822783, "FY2020": 760666, "FY2019": 548149, "FY2018": 587850}),
        ("Total net cash outflow", {"FY2025": 405412, "FY2024": 400945, "FY2023": 332338, "FY2022": 355595, "FY2021": 303007, "FY2020": 229721, "FY2019": 161586, "FY2018": 149557}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "225.76%", "FY2024": "227.95%", "FY2023": "210%", "FY2022": "220%", "FY2021": "272%", "FY2020": "331%", "FY2019": "339%", "FY2018": "393%"}),
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
        ("Net Stable Funding Ratio (%)", {"FY2025": "148.70%", "FY2024": "154.16%", "FY2023": "131.97%", "FY2022": "154.4%", "FY2021": "171.4%", "FY2020": "Not publicly disclosed", "FY2019": "Not publicly disclosed", "FY2018": "Not publicly disclosed"}),
    ],
    p3_sources(),
    note="FY2021's own Pillar 3 report did not disclose NSFR at all; the FY2021 figures shown here are taken from "
         "the FY2022 Pillar 3 report's own FY2021 comparative column instead. NSFR reporting only became a live "
         "CRR II requirement being phased in through 2020-2021 (per the Bank's own FY2019 and FY2020 Pillar 3 "
         "reports, both read in full) - neither the FY2018, FY2019, nor FY2020 Pillar 3 report discloses an NSFR "
         "figure at all (for any year, including as a prior-year comparative), so these three years are "
         "genuinely not publicly disclosed rather than merely unsourced.",
)

metric(
    "MREL Ratio", None,
    [("MREL requirement (= Total Capital Requirement, %)", {"FY2025": "10.69%", "FY2024": "10.69%", "FY2023": "10.69%", "FY2022": "10.10%", "FY2021": "10.14%", "FY2020": "10.18%", "FY2019": "10.55%", "FY2018": "10.65%"})],
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
        ("Total assets", {"FY2025": 2187753, "FY2024": 1957289, "FY2023": 1745808, "FY2022": 1669179, "FY2021": 1622794, "FY2020": 1431594, "FY2019": 1122206, "FY2018": 1076894}),
        ("Loans and advances to customers", {"FY2025": 1133097, "FY2024": 1013816, "FY2023": 1013646, "FY2022": 836576, "FY2021": 723523, "FY2020": 601810, "FY2019": 477554, "FY2018": 362446}),
        ("Customer deposits", {"FY2025": 1861280, "FY2024": 1717204, "FY2023": 1559309, "FY2022": 1538657, "FY2021": 1507227, "FY2020": 1335725, "FY2019": 1030435, "FY2018": 998130}),
        ("Total equity", {"FY2025": 263994, "FY2024": 222117, "FY2023": 172617, "FY2022": 123815, "FY2021": 108963, "FY2020": 90669, "FY2019": 85132, "FY2018": 75423}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total income", {"FY2025": 95026, "FY2024": 102097, "FY2023": 92421, "FY2022": 47183, "FY2021": 25137, "FY2020": 21948, "FY2019": 22642, "FY2018": 18371}),
        ("Operating expenses", {"FY2025": -41377, "FY2024": -33314, "FY2023": -25011, "FY2022": -17354, "FY2021": -13614, "FY2020": -12614, "FY2019": -13315, "FY2018": -10623}),
        ("Profit for the year", {"FY2025": 40789, "FY2024": 50476, "FY2023": 48858, "FY2022": 22843, "FY2021": 9671, "FY2020": 7027, "FY2019": 7981, "FY2018": 5967}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 222117, "FY2024": 172617, "FY2023": 123815, "FY2022": 108963, "FY2021": 90669, "FY2020": 85132, "FY2019": 75423, "FY2018": 59819}),
        ("Total comprehensive income for the year", {"FY2025": 44881, "FY2024": 50970, "FY2023": 49972, "FY2022": 15683, "FY2021": 10499, "FY2020": 6210, "FY2019": 10662, "FY2018": 7682}),
        ("Other equity movements, net", {"FY2025": -3004, "FY2024": -1470, "FY2023": -1170, "FY2022": -831, "FY2021": 7795, "FY2020": -673, "FY2019": -953, "FY2018": 7922}),
        ("Closing equity", {"FY2025": 263994, "FY2024": 222117, "FY2023": 172617, "FY2022": 123815, "FY2021": 108963, "FY2020": 90669, "FY2019": 85132, "FY2018": 75423}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 30097, "FY2024": 204830, "FY2023": -107535, "FY2022": -60460, "FY2021": 59722, "FY2020": 186733, "FY2019": -74036, "FY2018": -28746}),
        ("Net cash from/(used in) investing activities", {"FY2025": -480574, "FY2024": -53279, "FY2023": 20470, "FY2022": -51641, "FY2021": 42974, "FY2020": 80336, "FY2019": 95062, "FY2018": -54409}),
        ("Net cash from/(used in) financing activities", {"FY2025": 46633, "FY2024": -1928, "FY2023": -1829, "FY2022": -1279, "FY2021": 7593, "FY2020": -1078, "FY2019": -991, "FY2018": 7912}),
        ("Cash and cash equivalents at end of year", {"FY2025": 220743, "FY2024": 624587, "FY2023": 474964, "FY2022": 563858, "FY2021": 677238, "FY2020": 566949, "FY2019": 300958, "FY2018": 280923}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "24.33%", "FY2024": "24.05%", "FY2023": "19.68%", "FY2022": "18.27%", "FY2021": "17.7%", "FY2020": "16.7%", "FY2019": "17.6%", "FY2018": "19.3%"}),
        ("Tier 1 Ratio", {"FY2025": "24.33%", "FY2024": "24.05%", "FY2023": "19.68%", "FY2022": "18.27%", "FY2021": "17.69%", "FY2020": "16.7%", "FY2019": "17.6%", "FY2018": "19.3%"}),
        ("Total Capital Ratio", {"FY2025": "24.33%", "FY2024": "24.05%", "FY2023": "19.68%", "FY2022": "18.27%", "FY2021": "17.69%", "FY2020": "16.7%", "FY2019": "17.6%", "FY2018": "19.3%"}),
        ("Leverage Ratio (Basel III)", {"FY2025": "11.45%", "FY2024": "11.05%", "FY2023": "9.62%", "FY2022": "7.19%", "FY2021": "5.7%", "FY2020": "5.9%", "FY2019": "6.9%", "FY2018": "6.4%"}),
        ("LCR", {"FY2025": "225.76%", "FY2024": "227.95%", "FY2023": "210%", "FY2022": "220%", "FY2021": "272%", "FY2020": "331%", "FY2019": "339%", "FY2018": "393%"}),
        ("NSFR", {"FY2025": "148.70%", "FY2024": "154.16%", "FY2023": "131.97%", "FY2022": "154.4%", "FY2021": "171.4%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Leverage Ratio shown on the Basel III basis (available for "
         "all 8 years) rather than the UK basis (only introduced from FY2024) - see Leverage Ratio sheet for both. "
         "NSFR was not disclosed by the Bank at all before FY2021 (left blank for FY2018-FY2020, not zero - see "
         "NSFR sheet). FY2018's 'Other equity movements, net' folds in that year's IFRS 9 transition adjustment "
         "(£(277)k) alongside the pension-scheme exit and share capital/buyback movements - see the Statement of "
         "Changes in Equity sheet for the full, unfolded breakdown.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/UNITY TRUST FINANCIALS.xlsx")
