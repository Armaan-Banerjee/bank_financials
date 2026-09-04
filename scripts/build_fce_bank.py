import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

# Companies House filing history, company 00772784 (FCE Bank Plc)
AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/00772784/filing-history/MzUxMTcwMTU1NGFkaXF6a2N4/document?format=pdf&download=0"
AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/00772784/filing-history/MzQ2MTUzNDU1OGFkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/00772784/filing-history/MzQxNTY0NTE3NGFkaXF6a2N4/document?format=pdf&download=0"
AR2022_AMENDED_URL = "https://find-and-update.company-information.service.gov.uk/company/00772784/filing-history/MzM5ODE1MjYzNmFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/00772784/filing-history/MzMzMzk0NjU4NWFkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "FCE Bank Plc (company 00772784) is the UK-regulated captive auto-finance bank for Ford "
    "Motor Company's European operations (vehicle financing/leasing across Ford's European "
    "markets, not just the UK). Does NOT take the FRS 101/102 cash-flow exemption - full "
    "Group-basis Statement of Cash Flows every year. All 5 Companies House filings are fully "
    "scanned/image-only (0 text blocks/page); every figure was transcribed via page rendering.\n"
    "FY2022's accounts were AMENDED (30 Oct 2023, replacing the original 24 Mar 2023 filing) - "
    "the amended FY2022 figures were used as the operative record for that year, since this is "
    "the entity's own correction to its own year's accounts (not a later year's restatement). "
    "Confirmed the amended FY2022 figures are internally consistent with how FY2023's own report "
    "later carries them forward as its FY2022 comparative - no discrepancy found.\n"
    "FY2024's cash and cash equivalents at end of year include a genuine, disclosed "
    "'Cash and cash equivalents in respect of discontinued operations' adjustment of £(873)m "
    "(Group basis) - a real disposal/discontinuation event that year, not a data error; kept as "
    "the entity's own disclosed reconciling item, not silently absorbed elsewhere.\n"
    "FY2021's own Statement of Cash Flows classifies 'Net cash inflow/(outflow) on derivative "
    "financial instruments', 'Increase in restricted cash', and 'Decrease in restricted cash' "
    "under Financing activities (Group: £44m/£(97)m/£463m respectively, p.49); FY2022 onward "
    "reclassify these same three items under Investing activities instead. Confirmed via direct "
    "page image (p.49) - each year's own reported section placement is used, not forced into a "
    "single consistent classification across the 5 years."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are FCE Bank Plc's own consolidated (Group) Statement of Cash Flows, "
    "each year's own originally-published figures (not a later year's restated comparative):\n"
    f"FY2025: Annual Report 2025, p.53 (Statements of Cash Flows) - {AR2025_URL}\n"
    f"FY2024: Annual Report 2024, p.58 (Statements of Cash Flows) - {AR2024_URL}\n"
    f"FY2023: Annual Report 2023, p.55 (Statements of Cash Flows) - {AR2023_URL}\n"
    f"FY2022: Annual Report 2022 (AMENDED filing, 30 Oct 2023), p.53 (Statements of Cash Flows) - {AR2022_AMENDED_URL}\n"
    f"FY2021: Annual Report 2021, p.49 (Statements of Cash Flow) - {AR2021_URL}\n"
    + ENTITY_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - FCE Bank Plc Pillar 3 / capital basis, Group/Consolidated:\n"
        f"FY2021-FY2025 Tier 1 Capital, Tier 2 Capital and Total Capital Ratio: Annual Report 2025, "
        f"p.5 ('Business Performance' - 'Total Capital' chart, values to the nearest £0.1bn) - {AR2025_URL}\n"
        "FY2021 CET1/Tier 1 Capital (exact, £2,684m) and Leverage Ratio (16.95%): Annual Report 2021, "
        f"'Pillar 3 Disclosures' Table 2 (p.135) and Table 19 (p.155) - {AR2021_URL}\n"
        "CET1 = Tier 1 Capital every year (confirmed via the FY2021 Pillar 3 Own Funds reconciliation - "
        "no Additional Tier 1 instruments held).\n"
        "FY2022-FY2025 CET1/Tier 1 Capital and CET1/Tier 1 Ratio are CALCULATED, not directly disclosed: "
        "the Annual Report only publishes the rounded (nearest £0.1bn) Tier 1/Tier 2 chart and the "
        "Total Capital Ratio %; no standalone Pillar 3 document or CET1/Tier 1 Ratio % is published for "
        "these years (the dedicated 'Pillar 3 Disclosures' chapter present in the FY2021 report was "
        "dropped from FY2022 onward). Total RWAs is likewise calculated (Total Capital / Total Capital "
        "Ratio) for every year, since no year discloses RWA directly.\n"
        "Leverage Ratio, LCR, NSFR, MREL Ratio: not located for FY2022-FY2025 - no Pillar 3 chapter "
        "exists in those reports to check, and none of these appear in the Business Performance/Business "
        "Environment narrative sections reviewed.\n"
        + extra
    )


bw = BankWorkbook(bank_name="FCE Bank Plc", years=YEARS, year_label=YEAR_LABEL, header_color="881D78")

STATEMENTS_ENTITY_NOTE = (
    ENTITY_NOTE
    + "\n\nPRESENTATION NOTE (Balance Sheet): FY2021-FY2023's own Statements of Financial Position show "
    "separate 'Property and equipment' and 'Right-of-use assets' lines; these are not shown as separate "
    "lines in FY2024/FY2025 (each year's own report presents them consolidated within 'Other assets' - "
    "confirmed by checking FY2024's/FY2025's own report has no such lines at all, not merely omitted here). "
    "FY2021-FY2023 use a single 'Financial liabilities' line and a separate 'Lease liabilities' line; "
    "FY2024-FY2025 relabel this as 'Borrowings from parent, banks and other financial institutions' with no "
    "separate lease liabilities line (folded in). FY2021-FY2023 combine 'Other liabilities and provisions' "
    "into one line; FY2024-FY2025 split this into separate 'Other liabilities' and 'Provisions' lines. "
    "Blank cells indicate that year's own report did not disclose that specific line separately at that "
    "granularity - the underlying totals reconcile exactly across all 5 years regardless of presentation.\n\n"
    "PRESENTATION NOTE (P&L): FY2021-FY2023's own P&L show 'Income from leasing & other operating income' "
    "as one combined line, plus separate '(Loss)/Gain on disposal of Operating Leases', 'Depreciation of "
    "property and equipment' and 'Depreciation of right-of-use assets' lines. FY2024 renames the combined "
    "income line 'Other operating income' and keeps the two depreciation lines split (no disposal-of-leases "
    "line that year). FY2025 combines both depreciation lines into a single 'Depreciation and amortisation' "
    "line and drops the disposal-of-leases line entirely. FY2024 is also the only year with a Discontinued "
    "Operations split (Ford Bank GmbH, sold during FY2024 - Note 40/36) - FY2025 has no discontinued "
    "operations since the disposal is already complete; FY2021-FY2023 predate the disposal and never had a "
    "discontinued-operations split at all. Each year's own originally-published figures are used throughout "
    "- FY2023's own £974m interest income / £575m total income / £121m PBT / £88m PAT / £55m total "
    "comprehensive income (this workbook's FY2023 column) differ substantially from the RESTATED FY2023 "
    "comparative shown in the FY2024 Annual Report (£722m/£368m/£97m/£88m PAT unchanged but total comp £55m "
    "same, driven by the Ford Bank GmbH disposal being reclassified as a discontinued operation after the "
    "fact) - per project convention, each year's own original figures are used, not a later year's restated "
    "comparative.\n\n"
    "EQUITY RECONCILIATION: verified via the per-year reconciliation ladder - every year's Statement of "
    "Changes in Equity closing balance ties exactly to that year's own Balance Sheet Total equity, and to "
    "the next year's own opening balance, with zero gaps found across all 5 years (FY2021 £2,742m -> FY2022 "
    "£2,502m -> FY2023 £2,556m -> FY2024 £2,065m -> FY2025 £1,704m, all independently confirmed against the "
    "Group Balance Sheet's own Total equity each year)."
)

STATEMENTS_SOURCES = (
    "Sources - all figures are FCE Bank Plc's own consolidated (Group) Statement of Financial Position, "
    "Statement of Profit or Loss and Other Comprehensive Income, and Statement of Changes in Equity, each "
    "year's own originally-published figures (not a later year's restated comparative):\n"
    f"FY2025: Annual Report 2025, pp.52,51,55 - {AR2025_URL}\n"
    f"FY2024: Annual Report 2024, pp.57,56,58 - {AR2024_URL}\n"
    f"FY2023: Annual Report 2023, pp.54,53,57 - {AR2023_URL}\n"
    f"FY2022: Annual Report 2022 (AMENDED filing, 30 Oct 2023), pp.52,51,55 - {AR2022_AMENDED_URL}\n"
    f"FY2021: Annual Report 2021, pp.48,47,51 - {AR2021_URL}\n"
    + STATEMENTS_ENTITY_NOTE
)

ASSET_QUALITY_SOURCES = (
    "Sources - FCE Bank Plc's own Note 13 'Allowance for Expected Credit Losses', Group basis (retail, "
    "finance leases and wholesale receivables), Stage 1/2/3 gross carrying amount (GCA) and ECL allowance, "
    "closing balances each year:\n"
    f"FY2025/FY2024: Annual Report 2025, p.83 (Note 13, Group table) - {AR2025_URL}\n"
    f"FY2023/FY2022: Annual Report 2023, p.83 (Note 13, Group table) - {AR2023_URL}\n"
    f"FY2021: Annual Report 2021, p.78 (Note 13, Group table) - {AR2021_URL}\n"
    "Each year's own closing balance ties exactly to the next year's own opening balance in the same note "
    "(confirmed chained across all 5 years). Portfolio Split (Retail and Finance Leases vs Wholesale) is "
    "also disclosed each year but not reproduced here for brevity - see the note itself for that breakdown.\n"
    + ENTITY_NOTE
)

RWA_BREAKDOWN_NOTE = (
    "FY2021 only: directly disclosed in the FY2021 Annual Report's dedicated 'Pillar 3 Disclosures' chapter "
    "(Table 5, 'Pillar 1 Capital Requirement Split by Risk Type', p.138) - the only year this chapter exists "
    "(dropped from FY2022 onward, per the existing note on this workbook's Pillar 3 metric sheets). "
    "'Total all risk types' (£11,427m) is FCE's own directly-disclosed Total RWA figure for FY2021, closely "
    "matching (but more precise than) the £11,450m calculated cross-check used on the Total RWAs metric "
    "sheet (Total Capital £2,994m / Total Capital Ratio 26.20%, rounded to nearest £0.1bn inputs).\n"
    "FY2022-FY2025: Not publicly disclosed - no Pillar 3 chapter exists in these years' Annual Reports "
    "(confirmed by reading each report's own contents page - no 'Pillar 3 Disclosures' section listed for "
    "FY2022 onward), consistent with the existing gap on this workbook's Leverage Ratio/LCR/NSFR/MREL "
    "sheets."
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents",
     {"FY2025": 1111, "FY2024": 1253, "FY2023": 2557, "FY2022": 2536, "FY2021": 1822}),
    ("DATA", "Derivative financial instruments",
     {"FY2025": 44, "FY2024": 96, "FY2023": 112, "FY2022": 301, "FY2021": 63}),
    ("DATA", "Other assets",
     {"FY2025": 299, "FY2024": 333, "FY2023": 481, "FY2022": 441, "FY2021": 320}),
    ("DATA", "Loans and advances to customers",
     {"FY2025": 11490, "FY2024": 12021, "FY2023": 15115, "FY2022": 14297, "FY2021": 12602}),
    ("DATA", "Property and equipment",
     {"FY2023": 218, "FY2022": 99, "FY2021": 162}),
    ("DATA", "Right-of-use assets",
     {"FY2023": 10, "FY2022": 15, "FY2021": 17}),
    ("DATA", "Intangible assets",
     {"FY2025": 68, "FY2024": 67, "FY2023": 58, "FY2022": 46, "FY2021": 38}),
    ("DATA", "Income taxes receivable",
     {"FY2025": 51, "FY2024": 32, "FY2023": 44, "FY2022": 40, "FY2021": 6}),
    ("DATA", "Deferred tax assets",
     {"FY2025": 32, "FY2024": 35, "FY2023": 35, "FY2022": 28, "FY2021": 35}),
    ("TOTAL", "Total assets",
     {"FY2025": 13095, "FY2024": 13837, "FY2023": 18630, "FY2022": 17803, "FY2021": 15065}),

    ("SECTION", "Liabilities", {}),
    ("DATA", "Financial liabilities / Borrowings from parent, banks and other financial institutions",
     {"FY2025": 4940, "FY2024": 5005, "FY2023": 6580, "FY2022": 7542, "FY2021": 6987}),
    ("DATA", "Lease liabilities",
     {"FY2023": 11, "FY2022": 15, "FY2021": 17}),
    ("DATA", "Deposits",
     {"FY2025": 5892, "FY2024": 6300, "FY2023": 8962, "FY2022": 7131, "FY2021": 5001}),
    ("DATA", "Derivative financial instruments",
     {"FY2025": 91, "FY2024": 100, "FY2023": 104, "FY2022": 135, "FY2021": 16}),
    ("DATA", "Other liabilities",
     {"FY2025": 226, "FY2024": 250}),
    ("DATA", "Provisions",
     {"FY2025": 161, "FY2024": 84}),
    ("DATA", "Other liabilities and provisions (combined)",
     {"FY2023": 359, "FY2022": 390, "FY2021": 235}),
    ("DATA", "Income taxes payable",
     {"FY2025": 66, "FY2024": 25, "FY2023": 19, "FY2022": 26, "FY2021": 40}),
    ("DATA", "Deferred tax liabilities",
     {"FY2025": 15, "FY2024": 8, "FY2023": 39, "FY2022": 62, "FY2021": 27}),
    ("TOTAL", "Total liabilities",
     {"FY2025": 11391, "FY2024": 11772, "FY2023": 16074, "FY2022": 15301, "FY2021": 12323}),

    ("SECTION", "Equity", {}),
    ("DATA", "Ordinary shares",
     {"FY2025": 614, "FY2024": 614, "FY2023": 614, "FY2022": 614, "FY2021": 614}),
    ("DATA", "Share premium",
     {"FY2025": 352, "FY2024": 352, "FY2023": 352, "FY2022": 352, "FY2021": 352}),
    ("DATA", "Retained earnings",
     {"FY2025": 738, "FY2024": 1099, "FY2023": 1590, "FY2022": 1536, "FY2021": 1776}),
    ("TOTAL", "Total equity",
     {"FY2025": 1704, "FY2024": 2065, "FY2023": 2556, "FY2022": 2502, "FY2021": 2742}),
    ("TOTAL", "Total liabilities and equity",
     {"FY2025": 13095, "FY2024": 13837, "FY2023": 18630, "FY2022": 17803, "FY2021": 15065}),
]

bw.add_balance_sheet_sheet(
    title="FCE Bank Plc — Balance Sheet",
    subtitle="Group/Consolidated basis, £m. See source note at bottom (presentation changes documented).",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=95,
    source_height=420,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income",
     {"FY2025": 860, "FY2024": 874, "FY2023": 974, "FY2022": 576, "FY2021": 552}),
    ("DATA", "Interest expense",
     {"FY2025": -470, "FY2024": -527, "FY2023": -505, "FY2022": -170, "FY2021": -162}),
    ("TOTAL", "Net interest income",
     {"FY2025": 390, "FY2024": 347, "FY2023": 469, "FY2022": 406, "FY2021": 390}),
    ("DATA", "Fees and commissions income",
     {"FY2025": 43, "FY2024": 58, "FY2023": 61, "FY2022": 62, "FY2021": 53}),
    ("DATA", "Fees and commissions expense",
     {"FY2025": -11, "FY2024": -8, "FY2023": -7, "FY2022": -6, "FY2021": -8}),
    ("TOTAL", "Net fees and commissions income",
     {"FY2025": 32, "FY2024": 50, "FY2023": 54, "FY2022": 56, "FY2021": 45}),
    ("DATA", "Other operating income / Income from leasing & other operating income",
     {"FY2025": 0, "FY2024": 8, "FY2023": 52, "FY2022": 54, "FY2021": 164}),
    ("TOTAL", "Total income",
     {"FY2025": 422, "FY2024": 405, "FY2023": 575, "FY2022": 516, "FY2021": 599}),

    ("SECTION", "Expenses", {}),
    ("DATA", "Allowance for expected credit losses",
     {"FY2025": -31, "FY2024": -18, "FY2023": -2, "FY2022": 4, "FY2021": 5}),
    ("DATA", "Operating expenses",
     {"FY2025": -265, "FY2024": -243, "FY2023": -287, "FY2022": -255, "FY2021": -239}),
    ("DATA", "(Loss)/Gain on disposal of Operating Leases",
     {"FY2023": -13, "FY2022": 30, "FY2021": -16}),
    ("DATA", "Depreciation and amortisation (combined, FY2025 only)",
     {"FY2025": -15}),
    ("DATA", "Depreciation of property and equipment",
     {"FY2024": 0, "FY2023": -37, "FY2022": -29, "FY2021": -131}),
    ("DATA", "Depreciation of right-of-use assets",
     {"FY2024": -4, "FY2023": -5, "FY2022": -5, "FY2021": -8}),
    ("DATA", "(Loss)/Gain on fair value adjustment - non designated derivatives",
     {"FY2025": -31, "FY2024": 46, "FY2023": -98, "FY2022": 128, "FY2021": 46}),
    ("DATA", "Gain/(Loss) on foreign exchange",
     {"FY2025": 87, "FY2024": -69, "FY2023": -12, "FY2022": 28, "FY2021": -18}),
    ("TOTAL", "Profit before tax",
     {"FY2025": 167, "FY2024": 117, "FY2023": 121, "FY2022": 417, "FY2021": 238}),
    ("DATA", "Income tax expense",
     {"FY2025": -71, "FY2024": -62, "FY2023": -33, "FY2022": -130, "FY2021": -84}),
    ("TOTAL", "Profit after tax in respect of continuing operations",
     {"FY2025": 96, "FY2024": 55, "FY2023": 88, "FY2022": 287, "FY2021": 154}),
    ("DATA", "Profit after tax in respect of discontinued operations (Ford Bank GmbH, FY2024 only)",
     {"FY2024": 157}),
    ("TOTAL", "Profit for the period",
     {"FY2025": 96, "FY2024": 212, "FY2023": 88, "FY2022": 287, "FY2021": 154}),

    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Translation differences on foreign currency net investments (continuing operations)",
     {"FY2025": 43, "FY2024": -42}),
    ("DATA", "Translation differences on foreign currency net investments (discontinued operations)",
     {"FY2024": -27}),
    ("DATA", "Translation differences on foreign currency net investments (FY2021-FY2023, not split)",
     {"FY2023": -33, "FY2022": 78, "FY2021": -115}),
    ("DATA", "Items recycled through profit or loss (realisation of FX on sale of subsidiaries)",
     {"FY2024": -134}),
    ("TOTAL", "Total comprehensive income for the period",
     {"FY2025": 139, "FY2024": 9, "FY2023": 55, "FY2022": 365, "FY2021": 39}),
]

bw.add_income_statement_sheet(
    title="FCE Bank Plc — Profit & Loss",
    subtitle="Group/Consolidated basis, £m. See source note at bottom (presentation changes and FY2023 "
              "non-restated own-year figures documented).",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=95,
    source_height=420,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
equity_headers = ["Share capital", "Share premium", "Profit or loss reserve", "Translation reserve",
                   "Total retained earnings", "Total"]
equity_rows = [
    ("TOTAL", "At 1 January 2021", (614, 352, 1577, 460, 2037, 3003)),
    ("DATA", "Profit for the year", (None, None, 154, None, 154, 154)),
    ("DATA", "Translation differences", (None, None, None, -115, -115, -115)),
    ("DATA", "Dividend paid", (None, None, -300, None, -300, -300)),
    ("TOTAL", "At 31 December 2021", (614, 352, 1431, 345, 1776, 2742)),

    ("TOTAL", "At 1 January 2022", (614, 352, 1431, 345, 1776, 2742)),
    ("DATA", "Profit for the year", (None, None, 287, None, 287, 287)),
    ("DATA", "Translation differences", (None, None, None, 89, 89, 89)),
    ("DATA", "Reclassification of foreign exchange on transfer of subsidiaries", (None, None, None, -11, -11, -11)),
    ("DATA", "Dividend paid", (None, None, -600, None, -600, -600)),
    ("DATA", "Other equity adjustments", (None, None, -5, None, -5, -5)),
    ("TOTAL", "At 31 December 2022", (614, 352, 1113, 423, 1536, 2502)),

    ("TOTAL", "At 1 January 2023", (614, 352, 1113, 423, 1536, 2502)),
    ("DATA", "Profit for the year", (None, None, 88, None, 88, 88)),
    ("DATA", "Translation differences", (None, None, None, -33, -33, -33)),
    ("DATA", "Other equity adjustments", (None, None, -1, None, -1, -1)),
    ("TOTAL", "At 31 December 2023", (614, 352, 1200, 390, 1590, 2556)),

    ("TOTAL", "At 1 January 2024", (614, 352, 1214, 376, 1590, 2556)),
    ("DATA", "Profit for the year", (None, None, 212, None, 212, 212)),
    ("DATA", "Translation differences", (None, None, None, -69, -69, -69)),
    ("DATA", "Realisation of foreign exchange on sale of subsidiaries", (None, None, None, -134, -134, -134)),
    ("DATA", "Dividend paid", (None, None, -500, None, -500, -500)),
    ("TOTAL", "At 31 December 2024 / 1 January 2025", (614, 352, 926, 173, 1099, 2065)),

    ("DATA", "Profit for the year", (None, None, 96, None, 96, 96)),
    ("DATA", "Translation differences", (None, None, None, 43, 43, 43)),
    ("DATA", "Dividend paid", (None, None, -500, None, -500, -500)),
    ("TOTAL", "At 31 December 2025", (614, 352, 522, 216, 738, 1704)),
]

bw.add_equity_changes_sheet(
    title="FCE Bank Plc — Statement of Changes in Equity",
    subtitle="Group/Consolidated basis, £m, chronological (oldest to newest). Per-year reconciliation "
              "ladder confirmed: every closing balance ties exactly to the Balance Sheet's own Total "
              "equity and to the next year's own opening balance - zero gaps found. Note: FY2023's own "
              "'Profit or loss reserve'/'Translation reserve' 1 Jan 2024 opening (1,214/376) is restated "
              "vs FY2023's own closing (1,200/390) - AR2024's own report; both feed the same Total (2,556).",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=54,
    source_height=420,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (Group/Consolidated basis)
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Cash from/(used in) operating activities",
     {"FY2025": 554, "FY2024": -1420, "FY2023": -1661, "FY2022": -1431, "FY2021": 2574}),
    ("DATA", "Interest paid",
     {"FY2025": -475, "FY2024": -672, "FY2023": -542, "FY2022": -177, "FY2021": -184}),
    ("DATA", "Interest received",
     {"FY2025": 926, "FY2024": 1160, "FY2023": 1071, "FY2022": 442, "FY2021": 836}),
    ("DATA", "Other operating income received",
     {"FY2025": 0, "FY2024": 48, "FY2023": 72, "FY2022": 26, "FY2021": 109}),
    ("DATA", "Income taxes paid",
     {"FY2025": -39, "FY2024": -51, "FY2023": -73, "FY2022": -133, "FY2021": -43}),
    ("TOTAL", "Net cash generated from/(used in) operating activities",
     {"FY2025": 966, "FY2024": -935, "FY2023": -1133, "FY2022": -1273, "FY2021": 3292}),

    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property and equipment",
     {"FY2025": -2, "FY2024": 0, "FY2023": -6, "FY2022": -6, "FY2021": -1}),
    ("DATA", "Proceeds from sale of property and equipment",
     {"FY2021": 6}),
    ("DATA", "Investment in internally and externally generated software",
     {"FY2025": -13, "FY2024": -19, "FY2023": -21, "FY2022": -15, "FY2021": -11}),
    ("DATA", "Net cash movement in sale of subsidiaries",
     {"FY2023": 0, "FY2022": -13}),
    ("DATA", "Net cash (outflow)/inflow on derivative financial instruments",
     {"FY2025": 2, "FY2024": 109, "FY2023": 165, "FY2022": 29}),
    ("DATA", "Increase in restricted cash",
     {"FY2025": -65, "FY2024": -61, "FY2023": -61, "FY2022": -73}),
    ("DATA", "Decrease in restricted cash",
     {"FY2025": 61, "FY2024": 84, "FY2023": 62, "FY2022": 63}),
    ("DATA", "Dividend from subsidiaries",
     {"FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("TOTAL", "Net cash (used in)/generated from investing activities",
     {"FY2025": -17, "FY2024": 113, "FY2023": 139, "FY2022": -15, "FY2021": -6}),

    ("SECTION", "Financing activities", {}),
    ("DATA", "Proceeds from the issue of debt securities and from loans provided by banks and other financial institutions",
     {"FY2025": 1001, "FY2024": 1642, "FY2023": 1311, "FY2022": 4482, "FY2021": 2972}),
    ("DATA", "Repayments of debt securities and of loans provided by banks and other financial institutions",
     {"FY2025": -797, "FY2024": -1790, "FY2023": -2022, "FY2022": -3861, "FY2021": -6212}),
    ("DATA", "Proceeds of funds provided by parent and related undertakings",
     {"FY2025": 211, "FY2024": 214, "FY2023": 698, "FY2022": 568, "FY2021": 398}),
    ("DATA", "Repayment of funds provided by parent and related undertakings",
     {"FY2025": -557, "FY2024": -485, "FY2023": -548, "FY2022": -480, "FY2021": -2614}),
    ("DATA", "Net (decrease)/increase in short-term borrowings",
     {"FY2025": -61, "FY2024": 343, "FY2023": -289, "FY2022": -168, "FY2021": 472}),
    ("DATA", "Net (decrease)/increase in deposits",
     {"FY2025": -408, "FY2024": 517, "FY2023": 1891, "FY2022": 2005, "FY2021": 1427}),
    ("DATA", "Net cash inflow/(outflow) on derivative financial instruments (FY2021 only - "
             "classified under Investing in later years' presentation, see ENTITY_NOTE)",
     {"FY2021": 44}),
    ("DATA", "Increase in restricted cash (FY2021 only - classified under Investing in later "
             "years' presentation)",
     {"FY2021": -97}),
    ("DATA", "Decrease in restricted cash (FY2021 only - classified under Investing in later "
             "years' presentation)",
     {"FY2021": 463}),
    ("DATA", "Dividend paid",
     {"FY2025": -500, "FY2024": 0, "FY2023": 0, "FY2022": -600, "FY2021": -300}),
    ("TOTAL", "Net cash (used in)/generated from financing activities",
     {"FY2025": -1111, "FY2024": 441, "FY2023": 1041, "FY2022": 1946, "FY2021": -3447}),

    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents",
     {"FY2025": -162, "FY2024": -381, "FY2023": 47, "FY2022": 658, "FY2021": -161}),
    ("DATA", "Cash and cash equivalents at beginning of year",
     {"FY2025": 1253, "FY2024": 2557, "FY2023": 2536, "FY2022": 1822, "FY2021": 2048}),
    ("DATA", "Effect of exchange rate changes on cash and cash equivalents",
     {"FY2025": 20, "FY2024": -50, "FY2023": -26, "FY2022": 56, "FY2021": -65}),
    ("DATA", "Cash and cash equivalents in respect of discontinued operations",
     {"FY2024": -873}),
    ("TOTAL", "Cash and cash equivalents at end of year",
     {"FY2025": 1111, "FY2024": 1253, "FY2023": 2557, "FY2022": 2536, "FY2021": 1822}),
]

bw.add_cash_flow_sheet(
    title="FCE Bank Plc — Consolidated Statement of Cash Flows",
    subtitle="Group/Consolidated basis, £m. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=210,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Gross Carrying Amount (GCA) by IFRS 9 stage, closing balance", {}),
    ("DATA", "Stage 1 GCA",
     {"FY2025": 11363, "FY2024": 11731, "FY2023": 14782, "FY2022": 12290, "FY2021": 12355}),
    ("DATA", "Stage 2 GCA",
     {"FY2025": 127, "FY2024": 269, "FY2023": 242, "FY2022": 1959, "FY2021": 153}),
    ("DATA", "Stage 3 GCA",
     {"FY2025": 22, "FY2024": 34, "FY2023": 108, "FY2022": 72, "FY2021": 127}),
    ("TOTAL", "Total GCA",
     {"FY2025": 11512, "FY2024": 12034, "FY2023": 15132, "FY2022": 14321, "FY2021": 12635}),

    ("SECTION", "Expected Credit Loss (ECL) allowance by IFRS 9 stage, closing balance", {}),
    ("DATA", "Stage 1 ECL",
     {"FY2025": -20, "FY2024": -12, "FY2023": -16, "FY2022": -16, "FY2021": -30}),
    ("DATA", "Stage 2 ECL",
     {"FY2025": 0, "FY2024": -1, "FY2023": -1, "FY2022": -8, "FY2021": -1}),
    ("DATA", "Stage 3 ECL",
     {"FY2025": -2, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": -2}),
    ("TOTAL", "Total ECL",
     {"FY2025": -22, "FY2024": -13, "FY2023": -17, "FY2022": -24, "FY2021": -33}),

    ("SECTION", "Derived ratios", {}),
    ("DATA", "Stage 3 / Total GCA",
     {"FY2025": "0.19%", "FY2024": "0.28%", "FY2023": "0.71%", "FY2022": "0.50%", "FY2021": "1.01%"}),
    ("DATA", "Total ECL / Total GCA (overall coverage)",
     {"FY2025": "0.19%", "FY2024": "0.11%", "FY2023": "0.11%", "FY2022": "0.17%", "FY2021": "0.26%"}),
]

bw.add_asset_quality_sheet(
    title="FCE Bank Plc — Asset Quality",
    subtitle="Group/Consolidated basis, £m (ratios as calculated). Retail, finance leases and wholesale "
              "receivables combined - see source note at bottom for the Retail/Wholesale portfolio split "
              "disclosed in the same note.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=68,
    source_height=280,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=48, source_height=210)


CALC_NOTE = (
    "CALCULATED, not directly disclosed for FY2022-FY2025 (only the rounded nearest-£0.1bn chart "
    "value is published) - see the sheet's own source note for the exact FY2021 figure and full "
    "methodology."
)

metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital (= Tier 1 Capital, no AT1 instruments held)",
      {"FY2025": 1600, "FY2024": 1800, "FY2023": 2400, "FY2022": 2100, "FY2021": 2684})],
    note=CALC_NOTE,
)

metric(
    "CET1 Ratio", "%",
    [("CET1 Ratio (= Tier 1 Ratio, calculated as CET1 Capital / Total RWAs)",
      {"FY2025": "16.59%", "FY2024": "17.61%", "FY2023": "17.16%", "FY2022": "16.65%", "FY2021": "23.58%"})],
    note=CALC_NOTE + " FY2021 also independently cross-checked against the exact Pillar 3 Own Funds table.",
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital (= CET1, no AT1 instruments held)",
      {"FY2025": 1600, "FY2024": 1800, "FY2023": 2400, "FY2022": 2100, "FY2021": 2684})],
    note=CALC_NOTE,
)

metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 Ratio (= CET1 Ratio, no AT1 instruments held)",
      {"FY2025": "16.59%", "FY2024": "17.61%", "FY2023": "17.16%", "FY2022": "16.65%", "FY2021": "23.58%"})],
    note=CALC_NOTE,
)

metric(
    "Total Capital", "£m",
    [("Total Capital (Tier 1 + Tier 2)",
      {"FY2025": 1800, "FY2024": 2000, "FY2023": 2700, "FY2022": 2400, "FY2021": 2994})],
    note="FY2022-FY2025 summed from the Annual Report's own rounded (nearest £0.1bn) Tier 1/Tier 2 "
         "chart. FY2021 exact from the Pillar 3 Own Funds tables (£2,684m CET1 + £310m Tier 2).",
)

metric(
    "Total Capital Ratio", "%",
    [("Total Capital / Total Risk-Weighted Exposure Amounts",
      {"FY2025": "18.66%", "FY2024": "19.57%", "FY2023": "19.30%", "FY2022": "19.03%", "FY2021": "26.20%"})],
    note="Directly disclosed every year in the Annual Report's own 'Business Performance' - 'Total "
         "Capital' chart, the only capital ratio consistently published across all 5 years.",
)

metric(
    "Total RWAs", "£m",
    [("Total Risk-Weighted Exposure Amounts",
      {"FY2025": 9646, "FY2024": 10220, "FY2023": 13990, "FY2022": 12612, "FY2021": 11427})],
    note="FY2021 directly disclosed ('Total all risk types', Pillar 3 Disclosures Table 5, p.138) - see "
         "the RWA Breakdown sheet immediately following for the full risk-category split. "
         "FY2022-FY2025 CALCULATED (Total Capital / Total Capital Ratio) - not directly disclosed in "
         "any of those years (no Pillar 3 chapter exists after FY2021).",
)

bw.add_rwa_breakdown_sheet(
    title="FCE Bank Plc — RWA Breakdown",
    subtitle="FY2021 only (Consolidated), £m. See source note at bottom for why FY2022-FY2025 are not "
              "publicly disclosed.",
    rows=[
        ("SECTION", "Credit risk", {}),
        ("DATA", "Credit risk (excl. counterparty credit risk)", {"FY2021": 10238}),
        ("DATA", "Counterparty credit risk", {"FY2021": 56}),
        ("TOTAL", "Total credit risk", {"FY2021": 10294}),
        ("SECTION", "Other risk types", {}),
        ("DATA", "Credit valuation adjustment (CVA) risk", {"FY2021": 33}),
        ("DATA", "Market risk (foreign exchange risk)", {"FY2021": 170}),
        ("DATA", "Operational risk", {"FY2021": 930}),
        ("TOTAL", "Total all risk types (Total RWAs)", {"FY2021": 11427}),
    ],
    sources_text=p3_sources() + "\n\n" + RWA_BREAKDOWN_NOTE,
    first_col_width=58,
    source_height=280,
    unit_suffix=" (£m)",
)

metric(
    "Leverage Ratio", "%",
    [("Leverage Ratio", {"FY2021": "16.95%"})],
    note="Only directly disclosed for FY2021, from the dedicated 'Pillar 3 Disclosures' chapter "
         "present in that year's Annual Report (Table 19, p.155) - this chapter was dropped from "
         "FY2022 onward, and no leverage ratio was found anywhere in the FY2022-FY2025 reports. "
         "Not calculated for those years since no leverage exposure measure is disclosed either.",
)

bw.add_not_disclosed_metric_sheets(
    ["LCR"],
    p3_sources(),
    per_note={
        "LCR": "Not publicly disclosed - no LCR reference found in any of the 5 Annual Reports "
               "reviewed, including the FY2021 Pillar 3 Disclosures chapter's own index of every "
               "CRR disclosure article it covers (no liquidity-ratio article listed at all). "
               "Plausibly reflects FCE Bank's captive auto-finance/wholesale-funded business model.",
    },
)

bw.add_not_disclosed_metric_sheets(
    ["NSFR", "MREL Ratio"],
    p3_sources(),
    per_note={
        "NSFR": "Not publicly disclosed - no NSFR reference found in any of the 5 Annual Reports "
                "reviewed, including the FY2021 Pillar 3 Disclosures chapter's own index of every "
                "CRR disclosure article it covers (no liquidity-ratio article listed at all).",
        "MREL Ratio": "Not publicly disclosed - no MREL reference found in any of the 5 Annual "
                      "Reports reviewed.",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 13095, "FY2024": 13837, "FY2023": 18630, "FY2022": 17803, "FY2021": 15065}),
        ("Loans and advances to customers", {"FY2025": 11490, "FY2024": 12021, "FY2023": 15115, "FY2022": 14297, "FY2021": 12602}),
        ("Deposits", {"FY2025": 5892, "FY2024": 6300, "FY2023": 8962, "FY2022": 7131, "FY2021": 5001}),
        ("Total equity", {"FY2025": 1704, "FY2024": 2065, "FY2023": 2556, "FY2022": 2502, "FY2021": 2742}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total income", {"FY2025": 422, "FY2024": 405, "FY2023": 575, "FY2022": 516, "FY2021": 599}),
        ("Operating expenses", {"FY2025": -265, "FY2024": -243, "FY2023": -287, "FY2022": -255, "FY2021": -239}),
        ("Profit for the period", {"FY2025": 96, "FY2024": 212, "FY2023": 88, "FY2022": 287, "FY2021": 154}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 2065, "FY2024": 2556, "FY2023": 2502, "FY2022": 2742, "FY2021": 3003}),
        ("Total comprehensive income for the year", {"FY2025": 139, "FY2024": 9, "FY2023": 55, "FY2022": 365, "FY2021": 39}),
        ("Other equity movements, net", {"FY2025": -500, "FY2024": -500, "FY2023": -1, "FY2022": -605, "FY2021": -300}),
        ("Closing equity", {"FY2025": 1704, "FY2024": 2065, "FY2023": 2556, "FY2022": 2502, "FY2021": 2742}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash generated from/(used in) operating activities",
         {"FY2025": 966, "FY2024": -935, "FY2023": -1133, "FY2022": -1273, "FY2021": 3292}),
        ("Net cash (used in)/generated from investing activities",
         {"FY2025": -17, "FY2024": 113, "FY2023": 139, "FY2022": -15, "FY2021": -6}),
        ("Net cash (used in)/generated from financing activities",
         {"FY2025": -1111, "FY2024": 441, "FY2023": 1041, "FY2022": 1946, "FY2021": -3447}),
        ("Cash and cash equivalents at end of year",
         {"FY2025": 1111, "FY2024": 1253, "FY2023": 2557, "FY2022": 2536, "FY2021": 1822}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "16.59%", "FY2024": "17.61%", "FY2023": "17.16%", "FY2022": "16.65%", "FY2021": "23.58%"}),
        ("Total Capital Ratio", {"FY2025": "18.66%", "FY2024": "19.57%", "FY2023": "19.30%", "FY2022": "19.03%", "FY2021": "26.20%"}),
        ("Leverage Ratio", {"FY2021": "16.95%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. CET1/Tier 1 Ratio and Total RWAs are calculated "
         "for FY2022-FY2025 (only the rounded Tier 1/Tier 2/Total Capital Ratio chart is published for "
         "those years) - see the individual metric sheets for the full methodology.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/FCE BANK FINANCIALS.xlsx")
