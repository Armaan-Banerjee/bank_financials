import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

AR2025_URL = "https://www.oxbury.com/media/e3xppqoe/2025-company-accounts.pdf"
AR2024_URL = "https://www.oxbury.com/media/03rk55or/oxbury-2024-accounts-1pg.pdf"
AR2023_URL = "https://www.oxbury.com/media/dxeb3xqx/oxbury-bank-annual-accounts-31122023.pdf"
AR2022_URL = "https://www.oxbury.com/media/brmf2riv/annual-report-2022.pdf"
AR2021_URL = "https://www.oxbury.com/media/g5xibgrw/annual-report-2021.pdf"
P3_2023_URL = "https://www.oxbury.com/media/xttezclr/oxbury-bank-plc-pillar-3-2023-final.pdf"

ENTITY_NOTE = (
    "ENTITY / BASIS NOTE: Oxbury Bank Plc (FRN 834822; Companies House no. 11383418) is the PRA-authorised "
    "bank and the entity covered by this workbook. The annual reports present both Group and Company columns. "
    "This workbook uses the Company/entity-level cash-flow figures throughout. The Group includes Oxbury Bank Plc "
    "and its wholly owned subsidiary Oxbury Earth Ltd (and, from FY2025, Oxbury Earth LLC); Group figures are not "
    "substituted for the Bank's own figures. The FY2025 report describes a new wider holding structure, but the "
    "legal bank entity remains Oxbury Bank Plc."
)

CASH_FLOW_SOURCES = (
    "Sources - Oxbury Bank Plc Company/entity basis; all figures £'000:\n"
    f"FY2025 and restated FY2024: Oxbury Bank Plc Annual Report and Accounts 2025, pp.40-41, Company columns - {AR2025_URL}\n"
    f"FY2023: Oxbury Bank Plc Annual Report and Accounts 2024, pp.40-41, Company columns - {AR2024_URL}\n"
    f"FY2022: Oxbury Bank Plc Annual Report and Accounts 2023, pp.40-41, Company columns; the report marks the affected comparative figures with an asterisk and explains the restatement in Note 31 - {AR2023_URL}\n"
    f"FY2021: Oxbury Bank Plc Annual Report and Accounts 2022, p.39, Company columns - {AR2022_URL}\n"
    f"The FY2021 source report also reproduces the FY2021 statement in the 2021 Annual Report, p.35 - {AR2021_URL}\n\n"
    "The FY2025 financing subtotal is £1k above the sum of the displayed rounded component lines; the explicit "
    "£1k rounding adjustment preserves the report's stated subtotal.\n\n"
    + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - Oxbury Bank Plc regulatory/entity basis:\n"
        f"FY2023 and FY2022: Oxbury Bank Plc Pillar 3 Disclosures December 2023, pp.11-12 (capital resources, "
        f"RWA, capital ratios), pp.17-18 (leverage), pp.36-40 (LCR and NSFR) - {P3_2023_URL}\n"
        f"FY2025 and FY2024: Oxbury Bank Plc Annual Report and Accounts 2025, p.6 (Company Key Performance "
        f"Indicators, unaudited capital/liquidity measures) - {AR2025_URL}\n"
        f"FY2021: Oxbury Bank Plc Annual Report and Accounts 2021, p.6 (Company Key Performance Indicators, "
        f"unaudited CET1/Total Capital, leverage and LCR measures) - {AR2021_URL}\n\n"
        + ENTITY_NOTE
    )


bw = BankWorkbook(
    bank_name="Oxbury Bank Plc",
    years=YEARS,
    header_color="2F5597",
)

# ---------------------------------------------------------------
# Balance Sheet / P&L / Equity source-report mapping mirrors the existing
# cash flow sheet exactly: each year uses the LATEST available report's
# presentation of that year, not necessarily that year's own original
# report - FY2025 and restated FY2024 both come from AR2025; FY2023 comes
# from AR2024's own comparative; FY2022 (restated) comes from AR2023's own
# comparative; FY2021 comes from AR2022's own comparative. Balance Sheet
# built FIRST (equity reconciliation ladder step 1) so each year's own
# Total equity is the independent check value for the equity sheet below.
# All 5 years tie exactly - zero plug rows needed anywhere.
# ---------------------------------------------------------------
STATEMENTS_SOURCES = (
    "Sources - Oxbury Bank Plc Company/entity basis, £'000. Same year-to-report mapping as the Cash Flow "
    "Statement (see that sheet):\n"
    f"FY2025 and restated FY2024: Annual Report and Accounts 2025, Statement of Profit or Loss p.39, Statement "
    f"of Financial Position p.39, Statement of Changes in Equity p.42 - {AR2025_URL}\n"
    f"FY2023: Annual Report and Accounts 2024, Statement of Profit or Loss p.38, Statement of Financial Position "
    f"p.38, Statement of Changes in Equity p.42 - {AR2024_URL}\n"
    f"FY2022 (restated): Annual Report and Accounts 2023, Statement of Profit or Loss / Statement of Financial "
    f"Position p.19, Statement of Changes in Equity p.21 - {AR2023_URL}\n"
    f"FY2021: Annual Report and Accounts 2022, Statement of Profit or Loss / Statement of Financial Position "
    f"p.36-37, Statement of Changes in Equity p.40 - {AR2022_URL}\n"
    f"The FY2021 source report also reproduces the FY2021 statements in the 2021 Annual Report, pp.32-34 - "
    f"{AR2021_URL}. That original 2021 report shows Total Assets/Loans and advances to customers as "
    f"£165,797k/£110,525k, £20k lower than the £165,817k/£110,545k shown in the 2022 report's own FY2021 "
    f"comparative used here - a small genuine restatement between the two reports, reproduced as the later "
    f"report's own figures for consistency with the rest of this workbook, not blended.\n\n"
    "DATA QUALITY NOTE: the 2022 Annual Report's own Company Statement of Changes in Equity discloses the "
    "Company's FY2022 'Loss for the year' movement as £(334)k, while that same report's own Company Statement "
    "of Profit or Loss discloses the Company's FY2022 loss after tax as £(344)k - a genuine £10k inconsistency "
    "between the Bank's own two primary statements for the same year. Both figures are reproduced exactly as "
    "each statement discloses them (P&L sheet shows £(344)k; the equity sheet's movement and the Balance "
    "Sheet's Total Equity both tie to the equity statement's own £(334)k figure) rather than picking one.\n\n"
    + ENTITY_NOTE
)

bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash at Bank of England", {"FY2025": 1406822, "FY2024": 1470898, "FY2023": 530991, "FY2022": 130522, "FY2021": 44016}),
    ("DATA", "Cash at Credit Institutions", {"FY2025": 20657, "FY2024": 21120, "FY2023": 12674, "FY2022": 15122, "FY2021": 6542}),
    ("DATA", "Investment Securities", {"FY2025": 373924}),
    ("DATA", "Loans and Advances to Customers", {"FY2025": 1748444, "FY2024": 1021621, "FY2023": 605711, "FY2022": 349532, "FY2021": 110545}),
    ("DATA", "Investment in Subsidiary", {"FY2025": 2466, "FY2024": 2466, "FY2023": 2466, "FY2022": 2466}),
    ("DATA", "Other Assets", {"FY2025": 3332, "FY2024": 2598, "FY2023": 2487, "FY2022": 1025, "FY2021": 460}),
    ("DATA", "Property, Plant & Equipment", {"FY2025": 550, "FY2024": 786, "FY2023": 971, "FY2022": 429, "FY2021": 486}),
    ("DATA", "Intangible Assets", {"FY2025": 5713, "FY2024": 5426, "FY2023": 5416, "FY2022": 4252, "FY2021": 3768}),
    ("DATA", "Net Deferred Tax Asset", {"FY2024": 1942, "FY2023": 3209, "FY2022": 4283}),
    ("TOTAL", "Total Assets", {"FY2025": 3561908, "FY2024": 2526857, "FY2023": 1163925, "FY2022": 508358, "FY2021": 165817}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer Deposits", {"FY2025": 3309014, "FY2024": 2350433, "FY2023": 1060658, "FY2022": 441918, "FY2021": 138217}),
    ("DATA", "Other Liabilities and Accruals", {"FY2025": 7993, "FY2024": 3319, "FY2023": 7409, "FY2022": 4617, "FY2021": 1202}),
    ("DATA", "Subordinated Debt", {"FY2025": 34191, "FY2024": 17798, "FY2023": 15191, "FY2022": 7665}),
    ("DATA", "Net Deferred Tax Liability", {"FY2025": 431}),
    ("TOTAL", "Total Liabilities", {"FY2025": 3351629, "FY2024": 2371550, "FY2023": 1083258, "FY2022": 454200, "FY2021": 139419}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called Up Share Capital", {"FY2025": 1156, "FY2024": 1028, "FY2023": 762, "FY2022": 650, "FY2021": 514}),
    ("DATA", "Share Premium", {"FY2025": 203356, "FY2024": 160636, "FY2023": 92226, "FY2022": 68302, "FY2021": 40424}),
    ("DATA", "Accumulated Profits/(Losses)", {"FY2025": 5196, "FY2024": -6724, "FY2023": -12587, "FY2022": -14901, "FY2021": -14557}),
    ("DATA", "Share-based payment / capital contribution reserve (Note 23)", {"FY2025": 571, "FY2024": 367, "FY2023": 266, "FY2022": 107, "FY2021": 17}),
    ("TOTAL", "Total Equity", {"FY2025": 210279, "FY2024": 155307, "FY2023": 80667, "FY2022": 54158, "FY2021": 26398}),
    ("TOTAL", "Total Liabilities & Equity", {"FY2025": 3561908, "FY2024": 2526857, "FY2023": 1163925, "FY2022": 508358, "FY2021": 165817}),
]

bw.add_balance_sheet_sheet(
    title="Oxbury Bank Plc — Balance Sheet",
    subtitle="Company/entity-level basis, £'000. Investment Securities and the Net Deferred Tax Liability line are "
              "new FY2025 items (blank in earlier years, not zero); Investment in Subsidiary starts FY2022 "
              "(the Naqoda Ltd/Oxbury Earth Ltd acquisition, January 2022); Net Deferred Tax Asset is blank "
              "FY2025 (a small Net Deferred Tax Liability instead) and FY2021 (not disclosed as a separate line "
              "that early). Subordinated Debt is blank FY2021 (nil that year).",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=340,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Profit & Loss - FY2025's own report combines "Interest receivable on
# loans" and "Interest income - deposits" into a single line; FY2021-FY2023
# disclose them split. Both shown, blank where not split. FY2025's own
# report also combines the Taxation - R&D Credit / Deferred Tax / Income
# Tax split (available FY2021-FY2022) into one Taxation line - blank split
# rows for FY2023-FY2025, whose sourced reports also use a single line.
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable - on loans and advances to customers", {"FY2023": 34375, "FY2022": 9222, "FY2021": 865}),
    ("DATA", "Interest income - deposits placed with financial institutions", {"FY2023": 14255, "FY2022": 1254, "FY2021": 39}),
    ("TOTAL", "Total interest income", {"FY2025": 151488, "FY2024": 112467, "FY2023": 48630, "FY2022": 10476, "FY2021": 904}),
    ("DATA", "Interest payable & similar expenditure", {"FY2025": -104252, "FY2024": -81060, "FY2023": -29258, "FY2022": -4798, "FY2021": -542}),
    ("TOTAL", "Net Interest Income", {"FY2025": 47236, "FY2024": 31407, "FY2023": 19372, "FY2022": 5678, "FY2021": 362}),
    ("DATA", "Other Income/(Expenditure)", {"FY2025": 169, "FY2024": -104, "FY2023": 22, "FY2022": -35, "FY2021": -10}),
    ("TOTAL", "Total Net Income", {"FY2025": 47405, "FY2024": 31303, "FY2023": 19394, "FY2022": 5643, "FY2021": 352}),
    ("DATA", "Staff Costs", {"FY2025": -14854, "FY2024": -10741, "FY2023": -7844, "FY2022": -5514, "FY2021": -4035}),
    ("DATA", "Other Operating Expense", {"FY2025": -11166, "FY2024": -8039, "FY2023": -5471, "FY2022": -3875, "FY2021": -2797}),
    ("DATA", "Depreciation & Amortisation", {"FY2025": -1932, "FY2024": -1937, "FY2023": -1319, "FY2022": -1298, "FY2021": -898}),
    ("TOTAL", "Operating Profit/(Loss) before expected credit loss provisions", {"FY2025": 19453, "FY2024": 10586, "FY2023": 4760, "FY2022": -5044, "FY2021": -7378}),
    ("DATA", "Expected credit loss on loans and advances", {"FY2025": -1219, "FY2024": -1031, "FY2023": -464, "FY2022": -95, "FY2021": -85}),
    ("TOTAL", "Profit/(Loss) on Operations", {"FY2025": 18234, "FY2024": 9555, "FY2023": 4296, "FY2022": -5139, "FY2021": -7463}),
    ("DATA", "Finance costs/Interest expense", {"FY2025": -2507, "FY2024": -2067, "FY2023": -1249, "FY2022": -215}),
    ("TOTAL", "Profit/(Loss) from Ordinary Activities before tax", {"FY2025": 15727, "FY2024": 7488, "FY2023": 3047, "FY2022": -5354, "FY2021": -7463}),
    ("DATA", "Taxation - Research & Development Credit", {"FY2022": 727}),
    ("DATA", "Taxation - Deferred Tax", {"FY2022": 4283}),
    ("DATA", "Taxation - Income Tax", {"FY2022": 0}),
    ("DATA", "Taxation (combined)", {"FY2025": -3807, "FY2024": -1625, "FY2023": -733}),
    ("TOTAL", "Profit/(Loss) from Ordinary Activities after tax", {"FY2025": 11920, "FY2024": 5863, "FY2023": 2314, "FY2022": -344, "FY2021": -7463}),
    ("TOTAL", "Total Comprehensive Profit/(Loss)", {"FY2025": 11920, "FY2024": 5863, "FY2023": 2314, "FY2022": -344, "FY2021": -7463}),
]

bw.add_income_statement_sheet(
    title="Oxbury Bank Plc — Profit & Loss",
    subtitle="Company/entity-level basis, £'000. FY2022's Profit/(Loss) after tax of £(344)k reflects the source "
              "P&L's own figure - see the DATA QUALITY NOTE in the source citation for the £10k inconsistency "
              "against that year's own equity statement. Blank cells indicate that year's own report did not "
              "disclose that specific split.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=78,
    source_height=340,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - per-year reconciliation ladder confirmed:
# every year's own closing balance ties exactly to both the next year's own
# opening balance and that year's own Balance Sheet Total Equity. Zero plug
# rows needed anywhere across all 5 years. "Capital Contribution Reserve"
# only becomes its own column from the FY2025 transfer (see below); before
# that, its balance sits within "Share Based Payments" (both reported
# together on the Balance Sheet's single Note 23 line throughout).
# ---------------------------------------------------------------
equity_headers = ["Called Up Share Capital", "Share Premium", "Accumulated Profits/(Losses)", "Share Based Payments",
                   "Capital Contribution Reserve", "Total"]
equity_rows = [
    ("TOTAL", "At 31 December 2020 (FY2021 opening)", (448, 28541, -7094, 5, None, 21900)),
    ("DATA", "Issue of Share Capital", (66, 11883, None, None, None, 11949)),
    ("DATA", "Loss for the year", (None, None, -7463, None, None, -7463)),
    ("DATA", "Employee based share awards", (None, None, None, 12, None, 12)),
    ("TOTAL", "At 31 December 2021 (FY2021 closing)", (514, 40424, -14557, 17, None, 26398)),
    ("DATA", "Issue of Share Capital (net of costs)", (136, 27878, None, None, None, 28014)),
    ("DATA", "Loss for the year", (None, None, -334, None, None, -334)),
    ("DATA", "Employee based share awards", (None, None, None, 90, None, 90)),
    ("TOTAL", "At 31 December 2022 (FY2022 closing)", (650, 68302, -14901, 107, None, 54158)),
    ("DATA", "Issue of Share Capital (net of costs)", (112, 23924, None, None, None, 24036)),
    ("DATA", "Profit for the year", (None, None, 2314, None, None, 2314)),
    ("DATA", "Employee based share awards", (None, None, None, 159, None, 159)),
    ("TOTAL", "At 31 December 2023 (FY2023 closing)", (762, 92226, -12587, 266, None, 80667)),
    ("DATA", "Issue of Share Capital (net of costs)", (266, 68410, None, None, None, 68676)),
    ("DATA", "Profit for the year", (None, None, 5863, None, None, 5863)),
    ("DATA", "Employee based share awards", (None, None, None, 101, None, 101)),
    ("TOTAL", "At 31 December 2024 (FY2024 closing, restated)", (1028, 160636, -6724, 367, None, 155307)),
    ("DATA", "Issue of Share Capital (net of costs)", (128, 42720, None, None, None, 42848)),
    ("DATA", "Profit for the year", (None, None, 11920, None, None, 11920)),
    ("DATA", "Transfer from Share Based Payment Reserve to Capital Contribution Reserve", (None, None, None, -367, 367, 0)),
    ("DATA", "Employee based share awards", (None, None, None, None, 204, 204)),
    ("TOTAL", "At 31 December 2025 (FY2025 closing)", (1156, 203356, 5196, 0, 571, 210279)),
]

bw.add_equity_changes_sheet(
    title="Oxbury Bank Plc — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, Company/entity-level basis, £'000. Equity "
              "reconciliation ladder confirmed: every year's own closing balance ties exactly to both the next "
              "year's own opening balance and that year's own Balance Sheet Total Equity - zero plug rows "
              "needed anywhere across all 5 years. FY2022's £(334)k Loss-for-the-year movement is this "
              "statement's own figure, £10k different from the P&L's own £(344)k - see the source citation's "
              "DATA QUALITY NOTE.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=64,
)

cash_flow_rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit and adjustments before net changes in operating assets and liabilities", {"FY2025": -26222, "FY2024": -17894, "FY2023": -12067, "FY2022": -9138, "FY2021": -6468}),
    ("DATA", "Net changes in operating assets and liabilities (aggregate of source line items)", {"FY2025": 280132, "FY2024": 898886, "FY2023": 382363, "FY2022": 73038, "FY2021": 27493}),
    ("TOTAL", "Cash flows generated from/(used in) operating activities", {"FY2025": 253910, "FY2024": 880992, "FY2023": 370296, "FY2022": 63900, "FY2021": 21025}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of tangible assets", {"FY2025": -72, "FY2024": -119, "FY2023": -188, "FY2022": -72, "FY2021": -64}),
    ("DATA", "Disposal/(purchase) of gilts", {"FY2021": 50}),
    ("DATA", "Investment in subsidiary", {"FY2022": -2466}),
    ("DATA", "Addition in intangible assets and trademarks", {"FY2025": -1911, "FY2024": -1643, "FY2023": -2281, "FY2022": -1638, "FY2021": -1524}),
    ("DATA", "Purchase of investment securities", {"FY2025": -820188}),
    ("DATA", "Sale of investment securities", {"FY2025": 447232}),
    ("TOTAL", "Net cash flows used in investing activities", {"FY2025": -374939, "FY2024": -1762, "FY2023": -2469, "FY2022": -4176, "FY2021": -1538}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Issue of share capital", {"FY2025": 43129, "FY2024": 68951, "FY2023": 24262, "FY2022": 28167, "FY2021": 12019}),
    ("DATA", "Costs directly related to issue of share capital", {"FY2025": -282, "FY2024": -275, "FY2023": -226, "FY2022": -153, "FY2021": -70}),
    ("DATA", "Increase in subordinated debt", {"FY2025": 16250, "FY2024": 2500, "FY2023": 7500, "FY2022": 7500, "FY2021": 0}),
    ("DATA", "Interest paid on subordinated debt", {"FY2025": -2301, "FY2024": -1873, "FY2023": -1151, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Interest paid on lease payments", {"FY2025": -55, "FY2024": -71, "FY2023": -43, "FY2022": -37, "FY2021": 0}),
    ("DATA", "Payments in relation to leases", {"FY2025": -252, "FY2024": -109, "FY2023": -148, "FY2022": -115, "FY2021": -93}),
    ("DATA", "Rounding adjustment to FY2025 reported financing subtotal", {"FY2025": 1}),
    ("TOTAL", "Net cash flows from financing activities", {"FY2025": 56490, "FY2024": 69123, "FY2023": 30194, "FY2022": 35362, "FY2021": 11856}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents in the year", {"FY2025": -64539, "FY2024": 948353, "FY2023": 398021, "FY2022": 95086, "FY2021": 31343}),
    ("DATA", "Cash and cash equivalents at start of year", {"FY2025": 1492018, "FY2024": 543665, "FY2023": 145644, "FY2022": 50558, "FY2021": 19215}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 1427479, "FY2024": 1492018, "FY2023": 543665, "FY2022": 145644, "FY2021": 50558}),
]

bw.add_cash_flow_sheet(
    title="Oxbury Bank Plc — Statement of Cash Flows",
    subtitle="Company/entity-level basis, £'000; FY2024 is the restated comparative presented in the FY2025 report",
    rows=cash_flow_rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=72,
    source_height=220,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Asset Quality - IFRS 9 stage split by gross carrying amount and ECL
# allowance, sourced from each year's own report where a full stage split
# is disclosed (FY2025, FY2024 original, FY2023). FY2024's own original
# report figures are used here (not the later-restated Balance Sheet net
# total) since they're the only source with a full stage/ECL split -
# flagged, not blended, per the source note. FY2022 is only disclosed at
# stage level net of ECL (via the FY2023 report's own roll-forward opening
# balance); FY2021 predates any stage-level disclosure - only the
# aggregate net figure and cumulative £85k provision movement exist.
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, by IFRS 9 stage (gross carrying amount)", {}),
    ("DATA", "Stage 1 gross carrying amount", {"FY2025": 1711257, "FY2024": 1009280, "FY2023": 597332}),
    ("DATA", "Stage 2 gross carrying amount", {"FY2025": 33224, "FY2024": 12698, "FY2023": 8303}),
    ("DATA", "Stage 3 gross carrying amount", {"FY2025": 6458, "FY2024": 5190, "FY2023": 621}),
    ("TOTAL", "Gross carrying amount", {"FY2025": 1750938, "FY2024": 1027168, "FY2023": 606256, "FY2022": 349676}),
    ("DATA", "Stage 1 ECL allowance", {"FY2025": -1957, "FY2024": -1236, "FY2023": -507}),
    ("DATA", "Stage 2 ECL allowance", {"FY2025": -268, "FY2024": -45, "FY2023": -31}),
    ("DATA", "Stage 3 ECL allowance", {"FY2025": -269, "FY2024": -63, "FY2023": -7}),
    ("TOTAL", "ECL allowance", {"FY2025": -2494, "FY2024": -1344, "FY2023": -545, "FY2022": -144}),
    ("DATA", "Stage 1 net carrying amount", {"FY2025": 1709300, "FY2024": 1008044, "FY2023": 596825, "FY2022": 346425}),
    ("DATA", "Stage 2 net carrying amount", {"FY2025": 32956, "FY2024": 12653, "FY2023": 8272, "FY2022": 2602}),
    ("DATA", "Stage 3 net carrying amount", {"FY2025": 6189, "FY2024": 5127, "FY2023": 614, "FY2022": 505}),
    ("TOTAL", "Net carrying amount", {"FY2025": 1748444, "FY2024": 1025824, "FY2023": 605711, "FY2022": 349532, "FY2021": 110545}),
    ("DATA", "Stage 3 as % of gross carrying amount (NPL ratio)", {"FY2025": "0.37%", "FY2024": "0.51%", "FY2023": "0.10%"}),
    ("DATA", "ECL allowance as % of gross carrying amount (coverage)", {"FY2025": "0.14%", "FY2024": "0.13%", "FY2023": "0.09%", "FY2022": "0.04%"}),
]

bw.add_asset_quality_sheet(
    title="Oxbury Bank Plc — Asset Quality",
    subtitle="Company/entity-level basis, £'000. Loans and advances to customers, IFRS 9 stage 1/2/3 split.",
    rows=asset_quality_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nStage-split note references: FY2025 Annual Report and Accounts 2025 p.53 (Note 4.11); FY2024 "
        f"Annual Report and Accounts 2024 p.51 (Note); FY2023 Annual Report and Accounts 2024 p.51 (comparative "
        f"note, closing balance) and Annual Report and Accounts 2023 p.27 (own-year note) - {AR2024_URL} / "
        f"{AR2023_URL}; FY2022 is only disclosed net of ECL, via the Annual Report and Accounts 2023 p.27 "
        f"roll-forward's own '1 January 2023' opening balance - {AR2023_URL}; FY2021's cumulative £85k provision "
        f"movement is from the Cash Flow Statement's own 'increase in impairment provisions on loans and "
        f"advances' line, no stage split disclosed that early.\n\n"
        "DATA QUALITY NOTE: FY2024's gross/stage/ECL figures above are the Annual Report and Accounts 2024's own "
        "originally-published closing figures (net total £1,025,824k). The Annual Report and Accounts 2025 later "
        "restates FY2024's net loans to £1,021,621k (used on the Balance Sheet and Overview sheets, per a "
        "deferred income/deferred cost restatement described in that report's Note 25) but does not disclose a "
        "restated stage-level split - both figures are genuine Bank disclosures from different report vintages, "
        "shown as each report states them rather than blended.\n\n"
        "FY2022's Stage 1/2/3 figures are net of ECL (the only granularity disclosed for that year); FY2022's "
        "Gross carrying amount and ECL allowance TOTAL rows are the combined (non-stage-split) figures the Bank "
        "discloses for that year, so FY2022's coverage ratio is computed on a different basis (net-stage/gross-"
        "total) than other years - not directly comparable stage-for-stage."
    ),
    first_col_width=82,
    source_height=380,
    unit_suffix=" (£'000)",
)


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=48, source_height=180)


metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", {"FY2023": 68026, "FY2022": 45557})], "Not publicly disclosed for FY2025, FY2024 and FY2021 in the sources reviewed; FY2023 and FY2022 are from the dedicated Pillar 3 capital-resources table.")
metric("CET1 Ratio", "%", [("Common Equity Tier 1 (CET1) ratio", {"FY2023": "15.94%", "FY2022": "16.16%", "FY2021": "23%"})], "FY2021 is reported as ‘CET1 / Total Capital Ratio’ in the annual-report KPI table; FY2024-FY2025 CET1-specific ratios were not disclosed in the sources reviewed.")
metric("Tier 1 Capital", "£'000", [("Total Tier 1 capital", {"FY2023": 68026, "FY2022": 45557})], "Not publicly disclosed for FY2025, FY2024 and FY2021 in the sources reviewed.")
metric("Tier 1 Ratio", "%", [("Tier 1 capital ratio", {"FY2023": "15.94%", "FY2022": "16.16%", "FY2021": "23%"})], "FY2021 annual-report KPI is labelled CET1 / Total Capital Ratio and is used as the only disclosed capital-ratio measure for that year.")
metric("Total Capital", "£'000", [("Total regulatory capital", {"FY2023": 82214, "FY2022": 53057})], "Not publicly disclosed for FY2025, FY2024 and FY2021 in the sources reviewed.")
metric("Total Capital Ratio", "%", [("Total capital ratio", {"FY2025": "18.8%", "FY2024": "22.5%", "FY2023": "19.27%", "FY2022": "18.81%", "FY2021": "23%"})], "FY2025 and FY2024 are the annual-report Company Key Performance Indicators; FY2023-FY2022 are dedicated Pillar 3 ratios; FY2021 annual-report KPI is labelled CET1 / Total Capital Ratio.")
metric("Total RWAs", "£'000", [("Total risk-weighted assets", {"FY2023": 426705, "FY2022": 282001})], "Not publicly disclosed for FY2025, FY2024 and FY2021 in the sources reviewed.")

# RWA Breakdown - Pillar 3 UK OV1 template. FY2023/FY2022 only (RWAs not
# publicly disclosed for FY2025, FY2024, FY2021 - see Total RWAs above).
# DATA QUALITY FLAG: the Bank's own OV1 table's "Total" row (426,705/
# 282,001) equals the Credit Risk row alone - it does NOT include the
# separately-disclosed Operational risk RWA (18,622/9,411), even though
# arithmetically Credit + Operational would be higher. Reproduced exactly
# as the Bank's own Pillar 3 document discloses it, not corrected, since
# the "Total" figure is what ties to the Total RWAs sheet and the Bank's
# own reported capital ratios.
rwa_breakdown_rows = [
    ("DATA", "Credit Risk (excluding CCR)", {"FY2023": 426705, "FY2022": 282001}),
    ("DATA", "Operational risk", {"FY2023": 18622, "FY2022": 9411}),
    ("TOTAL", "Total risk weighted exposure amount (as disclosed - see data quality note)", {"FY2023": 426705, "FY2022": 282001}),
]
bw.add_rwa_breakdown_sheet(
    title="Oxbury Bank Plc — RWA Breakdown",
    subtitle="Company/entity-level basis, £'000. Pillar 3 UK OV1 template (4.4 Overview of Risk Weighted "
              "Exposure Amounts). Counterparty credit risk was disclosed as nil both years.",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources() + (
        "\n\nDATA QUALITY NOTE: the source document's own 'Total' row (426,705 for FY2023; 282,001 for FY2022) "
        "equals the Credit Risk row alone, not the sum of Credit Risk plus the separately-disclosed Operational "
        "risk row (18,622/9,411) - an apparent inconsistency within the Bank's own Pillar 3 table. Reproduced "
        "exactly as disclosed (the 'Total' ties to the pre-existing Total RWAs sheet and the Bank's own reported "
        "capital ratios), not corrected or blended."
    ),
    first_col_width=64,
    source_height=200,
    unit_suffix=" (£'000)",
)

metric("Leverage Ratio", "%", [("Leverage ratio excluding claims on central banks", {"FY2025": "9.2%", "FY2024": "12.7%", "FY2023": "10.69%", "FY2022": "12.17%", "FY2021": "15%"})], "FY2025-FY2024 are annual-report KPI measures; FY2023-FY2022 are Pillar 3 ratios excluding claims on central banks; FY2021 is the annual-report KPI.")
metric("LCR", "%", [("Liquidity Coverage Ratio", {"FY2025": "296%", "FY2024": "460%", "FY2023": "545.2%", "FY2022": "2,132%", "FY2021": "1,090%"})], "FY2025-FY2024 are annual-report KPI measures; FY2023-FY2022 are the Pillar 3 LCR ratios (the annual report also shows a year-end 614%/2,819% measure on a different basis); FY2021 is the annual-report KPI.")
metric("NSFR", "%", [("Net Stable Funding Ratio", {"FY2023": "201.1%", "FY2022": "149.1%"})], "Not publicly disclosed for FY2025, FY2024 and FY2021 in the sources reviewed.")
metric("MREL Ratio", None, [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})], "No quantitative MREL ratio was found in the annual reports or the dedicated FY2023 Pillar 3 disclosure reviewed.")

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total Assets", {"FY2025": 3561908, "FY2024": 2526857, "FY2023": 1163925, "FY2022": 508358, "FY2021": 165817}),
        ("Loans and Advances to Customers", {"FY2025": 1748444, "FY2024": 1021621, "FY2023": 605711, "FY2022": 349532, "FY2021": 110545}),
        ("Customer Deposits", {"FY2025": 3309014, "FY2024": 2350433, "FY2023": 1060658, "FY2022": 441918, "FY2021": 138217}),
        ("Total Equity", {"FY2025": 210279, "FY2024": 155307, "FY2023": 80667, "FY2022": 54158, "FY2021": 26398}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total Net Income", {"FY2025": 47405, "FY2024": 31303, "FY2023": 19394, "FY2022": 5643, "FY2021": 352}),
        ("Staff Costs, Other Operating Expense & Depreciation", {"FY2025": -27952, "FY2024": -20717, "FY2023": -14634, "FY2022": -10687, "FY2021": -7730}),
        ("Profit/(Loss) from Ordinary Activities after tax", {"FY2025": 11920, "FY2024": 5863, "FY2023": 2314, "FY2022": -344, "FY2021": -7463}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 155307, "FY2024": 80667, "FY2023": 54158, "FY2022": 26398, "FY2021": 21900}),
        ("Total comprehensive profit/(loss) for the year", {"FY2025": 11920, "FY2024": 5863, "FY2023": 2314, "FY2022": -334, "FY2021": -7463}),
        ("Other equity movements, net", {"FY2025": 43052, "FY2024": 68777, "FY2023": 24195, "FY2022": 28094, "FY2021": 11961}),
        ("Closing equity", {"FY2025": 210279, "FY2024": 155307, "FY2023": 80667, "FY2022": 54158, "FY2021": 26398}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 253910, "FY2024": 880992, "FY2023": 370296, "FY2022": 63900, "FY2021": 21025}),
        ("Net cash used in investing activities", {"FY2025": -374939, "FY2024": -1762, "FY2023": -2469, "FY2022": -4176, "FY2021": -1538}),
        ("Net cash from financing activities", {"FY2025": 56490, "FY2024": 69123, "FY2023": 30194, "FY2022": 35362, "FY2021": 11856}),
        ("Cash and cash equivalents at end of year", {"FY2025": 1427479, "FY2024": 1492018, "FY2023": 543665, "FY2022": 145644, "FY2021": 50558}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2023": "15.94%", "FY2022": "16.16%", "FY2021": "23%"}),
        ("Tier 1 Ratio", {"FY2023": "15.94%", "FY2022": "16.16%", "FY2021": "23%"}),
        ("Total Capital Ratio", {"FY2025": "18.8%", "FY2024": "22.5%", "FY2023": "19.27%", "FY2022": "18.81%", "FY2021": "23%"}),
        ("Leverage Ratio", {"FY2025": "9.2%", "FY2024": "12.7%", "FY2023": "10.69%", "FY2022": "12.17%", "FY2021": "15%"}),
        ("LCR", {"FY2025": "296%", "FY2024": "460%", "FY2023": "545.2%", "FY2022": "2,132%", "FY2021": "1,090%"}),
        ("NSFR", {"FY2023": "201.1%", "FY2022": "149.1%"}),
    ],
    note="Five latest financial years are covered (FY2021-FY2025). All statements use Oxbury Bank Plc Company columns. Dedicated Pillar 3 quantitative disclosures were located for FY2022-FY2023; FY2024-FY2025 capital/liquidity KPI ratios come from the annual reports, and FY2021 KPI ratios from the FY2021 annual report. Blank cells represent metrics not disclosed for that year, not zero. See the Balance Sheet/Profit & Loss/Statement of Changes in Equity sheets for the £10k FY2022 P&L-vs-equity-statement inconsistency this Overview's equity movement figures follow.\n\n" + ENTITY_NOTE,
)

bw.save("/Users/armaan/code/katalysis/banks/OXBURY FINANCIALS.xlsx")
