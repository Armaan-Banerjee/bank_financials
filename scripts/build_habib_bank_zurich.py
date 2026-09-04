import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/08864609/filing-history"
AR2025_URL = CH_BASE + "/MzUyNTkxNzE0NGFkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = CH_BASE + "/MzQxOTMzMTc3MGFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = CH_BASE + "/MzM4MjUzMDg5N2FkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = CH_BASE + "/MzM0MjYxMTQxOWFkaXF6a2N4/document?format=pdf&download=0"

RESTATEMENT_NOTE = (
    "DATA NOTE - FY2022/FY2023 opening-vs-closing cash gap (£14,806k): the FY2022 Annual "
    "Report's own originally-published cash flow statement (p.54) shows FY2022 closing cash "
    "of £96,506k, driven by a 'Due to banks' operating-liability movement of £22,119k and "
    "'Accruals, deferred income and other liabilities' of £4,453k. The FY2023 Annual Report's "
    "FY2022 comparative (p.58) restates these to £36,925k and £3,429k respectively (a £14,806k "
    "net reclassification, with a matching £1,024k offset between 'Accruals' and 'Loans and "
    "advances to customers'), producing a restated FY2022 closing cash of £111,312k that "
    "reconciles onto FY2023's own opening balance. Per this project's convention, each year "
    "keeps its own originally-published figures (FY2022 = FY2022 AR's figures throughout) "
    "rather than a later restated comparative, so the FY2022-to-FY2023 opening/closing bridge "
    "does not tie by £14,806k - this is a traced, disclosed reclassification, not an error."
)

ENTITY_NOTE = (
    "Habib Bank Zurich Plc (company 08864609) is a UK-incorporated public "
    "limited company, a wholly-owned subsidiary of Habib Bank AG Zurich "
    "(Switzerland). Figures throughout are Company-level (the Bank has no "
    "subsidiaries of its own, so Company and Group are the same entity). "
    "Each year uses that year's own originally-published Annual Report "
    "figures, not later restated comparatives (see the FY2022 note below)."
)

BALANCE_SHEET_SOURCES = (
    "Sources - Habib Bank Zurich Plc's own Statement of Financial Position, "
    "from each year's Companies House-filed Annual Report and Financial "
    "Statements (company 08864609):\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements for the year "
    f"ended 31 December 2025, Statement of Financial Position, p.57 - {AR2025_URL}\n"
    f"FY2023: Annual Report and Financial Statements for the year ended 31 "
    f"December 2023, Statement of Financial Position, p.56 (FY2023's own "
    f"originally-published figures used, not the later restated FY2022 "
    f"comparative shown here - see note below) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements for the year ended 31 "
    f"December 2022, Statement of Financial Position, p.52 (FY2022's own "
    f"originally-published figures used) - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements for the year ended 31 "
    f"December 2021, Statement of Financial Position, p.50 - {AR2021_URL}\n"
    + ENTITY_NOTE + "\n"
    "DATA NOTE - line-item structure genuinely changed across years, not a "
    "transcription gap: 'Financial investments' was reported as a single "
    "line through FY2022, split into 'Amortised cost' and 'FVOCI' sub-lines "
    "from FY2023 onward (blank cells below reflect this - see the combined "
    "'Financial investments (total)' row for FY2021/FY2022). 'Right of use "
    "lease assets' and 'Lease liability' only appear as their own lines "
    "from FY2023 onward (folded into other lines before then, per each "
    "year's own disclosure). 'Intangible assets under development' and "
    "'Advance tax' first appear as their own lines from FY2022 "
    "(Advance tax) and FY2024 (Intangible assets, nil that year, £808k "
    "FY2025) respectively. 'Deferred tax liabilities' appears only in "
    "FY2021 (nil that year). FY2022's Balance Sheet comparatives were later "
    "restated in the FY2023 Annual Report (a loan-fee reclassification "
    "reducing Loans and advances to customers and Other liabilities by "
    "£1.024m, and a Due from banks/Cash reclassification of £14.8m, per "
    "that report's Note 2) - per this project's convention, FY2022's own "
    "originally-published figures are used throughout, so this Balance "
    "Sheet does not tie exactly to the FY2023 report's own FY2022 "
    "comparative column."
)

INCOME_STATEMENT_SOURCES = (
    "Sources - Habib Bank Zurich Plc's own Income Statement and Statement "
    "of Comprehensive Income, from each year's Companies House-filed "
    "Annual Report and Financial Statements (company 08864609):\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements for the year "
    f"ended 31 December 2025, Income Statement p.55 and Statement of "
    f"Comprehensive Income p.56 - {AR2025_URL}\n"
    f"FY2023: Annual Report and Financial Statements for the year ended 31 "
    f"December 2023, Income Statement p.54 (FY2023's own originally-"
    f"published figures used) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements for the year ended 31 "
    f"December 2022, Income Statement p.50 and Statement of Other "
    f"Comprehensive Income p.51 (FY2022's own originally-published figures "
    f"used) - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements for the year ended 31 "
    f"December 2021, Income Statement p.48 (OCI detail for FY2021 taken "
    f"from the FY2022 Annual Report's own FY2021 comparative column in its "
    f"Statement of Other Comprehensive Income, since the FY2021 Annual "
    f"Report's own OCI statement was not part of this year's sourcing "
    f"scope) - {AR2021_URL}\n"
    + ENTITY_NOTE + "\n"
    "'Total comprehensive income for the year' is computed as Profit after "
    "tax plus Other comprehensive income for the year, net of tax, per "
    "each year's own disclosed figures - this is the one row genuinely "
    "comparable across all 5 years and ties exactly to the Statement of "
    "Changes in Equity's own closing-balance movements."
)

EQUITY_SOURCES = (
    "Sources - Habib Bank Zurich Plc's own Statement of Changes in Equity, "
    "from each year's Companies House-filed Annual Report and Financial "
    "Statements (company 08864609):\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements for the year "
    f"ended 31 December 2025, Statement of Changes in Equity, p.58 - {AR2025_URL}\n"
    f"FY2023: Annual Report and Financial Statements for the year ended 31 "
    f"December 2023, Statement of Changes in Equity, p.57 - {AR2023_URL}\n"
    f"FY2022 & FY2021: Annual Report and Financial Statements for the year "
    f"ended 31 December 2022, Statement of Changes in Equity, p.53 (gives "
    f"both years' own movements in one table) - {AR2022_URL}\n"
    + ENTITY_NOTE + "\n"
    "Built using this project's per-year reconciliation ladder: every "
    "year's closing balance ties exactly to both the next year's own "
    "opening balance and that year's own Balance Sheet Total equity - zero "
    "plug rows needed anywhere across all 5 years. One flagged, not "
    "force-reconciled, discrepancy: FY2025's dividend is £5,544k in this "
    "statement vs £5,543k in the Cash Flow Statement's 'Dividend paid' "
    "line - both reproduced exactly as each disclosed, a £1k rounding "
    "artifact between the two statements in the Bank's own FY2025 Annual "
    "Report, not a transcription error here."
)

ASSET_QUALITY_SOURCES = (
    "Sources - Habib Bank Zurich Plc's own Note 31.14 'Credit quality "
    "analysis' (Loans and advances to customers, IFRS 9 stage split), from "
    "each year's Companies House-filed Annual Report and Financial "
    "Statements (company 08864609):\n"
    f"FY2025 (with FY2024 total-only comparative): Annual Report and "
    f"Financial Statements for the year ended 31 December 2025, Note "
    f"31.14, p.94 - {AR2025_URL}\n"
    f"FY2023 (with FY2022 total-only comparative): Annual Report and "
    f"Financial Statements for the year ended 31 December 2023, Note "
    f"31.14/31.15, p.96 - {AR2023_URL}\n"
    f"FY2022 (own stage split, with FY2021 total-only comparative): Annual "
    f"Report and Financial Statements for the year ended 31 December 2022, "
    f"Note 31.15, p.95 - {AR2022_URL}\n"
    f"FY2021 (own stage split): Annual Report and Financial Statements for "
    f"the year ended 31 December 2021, Note 31.15, p.95 - {AR2021_URL}\n"
    + ENTITY_NOTE + "\n"
    "DATA NOTE - FY2024's own Stage 1/2/3 gross split is not shown: the "
    "FY2025 Annual Report's Note 31.14 only carries a FY2024 Total column "
    "as a comparative, not the FY2024 stage breakdown - left blank rather "
    "than guessed. Net loans and advances to customers (Total gross minus "
    "loss allowance) ties exactly to the Balance Sheet's own Loans and "
    "advances to customers figure for every year. Coverage/NPL ratios are "
    "derived (gross loans / loss allowance, not separately disclosed by "
    "the Bank) and labelled as such."
)

CASH_FLOW_SOURCES = (
    "Sources - Habib Bank Zurich Plc's own Cash Flow Statement, from each year's Companies "
    "House-filed Annual Report and Financial Statements (company 08864609):\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements for the year ended 31 December 2025, "
    f"Cash Flow Statement, p.59 - {AR2025_URL}\n"
    f"FY2023: Annual Report and Financial Statements for the year ended 31 December 2023, "
    f"Cash Flow Statement, p.58 (FY2023's own originally-published figures used; not the FY2022 "
    f"comparative shown here - see note below) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements for the year ended 31 December 2022, "
    f"Cash Flow Statement, p.54 (FY2022's own originally-published figures used) - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements for the year ended 31 December 2021, "
    f"Cash Flow Statement, p.52 - {AR2021_URL}\n"
    + RESTATEMENT_NOTE
)


def p3_sources():
    return (
        "Sources - Habib Bank Zurich Plc does not publish a standalone Pillar 3 disclosure "
        "(no such document was locatable on the Bank's own site, via Wayback Machine, or via "
        "web search this session); figures are the Bank's own regulatory-capital and liquidity "
        "disclosures from its statutory Annual Report and Financial Statements (company "
        "08864609), Notes to the Financial Statements:\n"
        f"FY2025 & FY2024: Note 31.25 'Capital Management and Risk' p.106 (CET1/Tier 1/Total "
        f"Capital) and Note 31.21 'Liquidity Risk Management' p.104 (LCR, average-for-period "
        f"basis) of the FY2025 Annual Report - {AR2025_URL}\n"
        f"FY2023 & FY2022: Note 31.25 p.106 and Note 31.21 p.104 of the FY2023 Annual Report "
        f"- {AR2023_URL}\n"
        f"FY2021: Note 31.25 p.107 and Note 31.21 p.103 of the FY2021 Annual Report "
        f"- {AR2021_URL}\n"
        "No Additional Tier 1 capital is disclosed in any year (Tier 1 = CET1 throughout, per "
        "the Bank's own 'Common equity Tier 1 (CET1) capital' labelling in the FY2023 Annual "
        "Report's capital note). No RWA figure is disclosed in any year, so CET1/Tier 1/Total "
        "Capital Ratios, Leverage Ratio and NSFR cannot be computed from the statutory accounts; "
        "MREL is not disclosed (Habib Bank Zurich Plc is not identified as a UK resolution "
        "entity in these accounts)."
    )


bw = BankWorkbook(bank_name="Habib Bank Zurich Plc", years=YEARS, year_label=YEAR_LABEL, header_color="CF0DF5")

# ---------------------------------------------------------------
# Sheet 1: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents", {
        "FY2025": 291217, "FY2024": 232380, "FY2023": 215342, "FY2022": 96506, "FY2021": 88689,
    }),
    ("DATA", "Due from banks", {
        "FY2025": 153760, "FY2024": 122152, "FY2023": 112789, "FY2022": 157240, "FY2021": 101317,
    }),
    ("DATA", "Loans and advances to customers at amortised cost", {
        "FY2025": 800598, "FY2024": 682470, "FY2023": 632149, "FY2022": 601062, "FY2021": 514061,
    }),
    ("DATA", "Financial investments - Amortised cost", {
        "FY2025": 163281, "FY2024": 192040, "FY2023": 130678,
    }),
    ("DATA", "Financial investments - FVOCI", {
        "FY2025": 55222, "FY2024": 35761, "FY2023": 32704,
    }),
    ("DATA", "Financial investments (total)", {
        "FY2022": 144352, "FY2021": 175654,
    }),
    ("DATA", "Derivative assets held for risk management", {
        "FY2025": 742, "FY2024": 226, "FY2023": 101, "FY2022": 192, "FY2021": 304,
    }),
    ("DATA", "Property and equipment", {
        "FY2025": 10805, "FY2024": 11664, "FY2023": 12545, "FY2022": 15369, "FY2021": 7498,
    }),
    ("DATA", "Right of use lease assets", {
        "FY2025": 2455, "FY2024": 2758, "FY2023": 2751,
    }),
    ("DATA", "Intangible assets under development", {
        "FY2025": 808, "FY2024": 0,
    }),
    ("DATA", "Other assets", {
        "FY2025": 2061, "FY2024": 2294, "FY2023": 1283, "FY2022": 1496, "FY2021": 2048,
    }),
    ("DATA", "Advance tax", {
        "FY2025": 471, "FY2024": 0, "FY2023": 931, "FY2022": 422,
    }),
    ("DATA", "Deferred tax assets", {
        "FY2025": 1849, "FY2024": 2653, "FY2023": 3754, "FY2022": 2399, "FY2021": 2506,
    }),
    ("TOTAL", "Total assets", {
        "FY2025": 1483269, "FY2024": 1284398, "FY2023": 1145027, "FY2022": 1019038, "FY2021": 892077,
    }),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Due to banks at amortised cost", {
        "FY2025": 186139, "FY2024": 108224, "FY2023": 123581, "FY2022": 129266, "FY2021": 107147,
    }),
    ("DATA", "Due to customers at amortised cost", {
        "FY2025": 1142802, "FY2024": 1023002, "FY2023": 885890, "FY2022": 769556, "FY2021": 672008,
    }),
    ("DATA", "Derivative liabilities held for risk management", {
        "FY2025": 164, "FY2024": 187, "FY2023": 42, "FY2022": 229, "FY2021": 514,
    }),
    ("DATA", "Accruals, deferred income and other liabilities", {
        "FY2025": 6750, "FY2024": 8815, "FY2023": 7075, "FY2022": 9860, "FY2021": 5540,
    }),
    ("DATA", "Lease liability", {
        "FY2025": 2562, "FY2024": 2833, "FY2023": 2920,
    }),
    ("DATA", "Current tax liabilities", {
        "FY2025": 0, "FY2024": 1145, "FY2023": 2300, "FY2022": 346, "FY2021": 573,
    }),
    ("DATA", "Deferred tax liabilities", {
        "FY2021": 0,
    }),
    ("DATA", "Subordinated liabilities", {
        "FY2025": 20265, "FY2024": 20296, "FY2023": 20340, "FY2022": 20273, "FY2021": 20092,
    }),
    ("TOTAL", "Total liabilities", {
        "FY2025": 1358682, "FY2024": 1164502, "FY2023": 1042148, "FY2022": 929530, "FY2021": 805874,
    }),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {
        "FY2025": 80000, "FY2024": 80000, "FY2023": 70000, "FY2022": 70000, "FY2021": 70000,
    }),
    ("DATA", "Retained earnings", {
        "FY2025": 44501, "FY2024": 40022, "FY2023": 33077, "FY2022": 20525, "FY2021": 16301,
    }),
    ("DATA", "Fair value through other comprehensive income reserve", {
        "FY2025": 86, "FY2024": -126, "FY2023": -198, "FY2022": -1017, "FY2021": -98,
    }),
    ("TOTAL", "Total equity", {
        "FY2025": 124587, "FY2024": 119896, "FY2023": 102879, "FY2022": 89508, "FY2021": 86203,
    }),
    ("TOTAL", "Total liabilities and equity", {
        "FY2025": 1483269, "FY2024": 1284398, "FY2023": 1145027, "FY2022": 1019038, "FY2021": 892077,
    }),
]

bw.add_balance_sheet_sheet(
    title="Habib Bank Zurich Plc — Balance Sheet",
    subtitle="Statement of Financial Position, figures as reported in each year's own Annual Report",
    rows=balance_sheet_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=64,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet 2: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {
        "FY2025": 77936, "FY2024": 80264, "FY2023": 61056, "FY2022": 32352, "FY2021": 21888,
    }),
    ("DATA", "Interest expense", {
        "FY2025": -40202, "FY2024": -42267, "FY2023": -26892, "FY2022": -8441, "FY2021": -4133,
    }),
    ("TOTAL", "Net interest income", {
        "FY2025": 37734, "FY2024": 37997, "FY2023": 34164, "FY2022": 23911, "FY2021": 17755,
    }),
    ("DATA", "Fee and commission income", {
        "FY2025": 2143, "FY2024": 2082, "FY2023": 1888, "FY2022": 2296, "FY2021": 2325,
    }),
    ("DATA", "Fee and commission expense", {
        "FY2025": -343, "FY2024": -367, "FY2023": -405, "FY2022": -533, "FY2021": -434,
    }),
    ("TOTAL", "Net fee and commission income", {
        "FY2025": 1800, "FY2024": 1715, "FY2023": 1483, "FY2022": 1763, "FY2021": 1891,
    }),
    ("DATA", "Net foreign exchange income", {
        "FY2025": 319, "FY2024": 551, "FY2023": 311, "FY2022": 597, "FY2021": 484,
    }),
    ("DATA", "Fair value gain/(loss) on derivative financial instruments", {
        "FY2025": 538, "FY2024": 40, "FY2023": -101, "FY2022": -38, "FY2021": -210,
    }),
    ("DATA", "Gain/(loss) on sale of financial investments", {
        "FY2025": 508, "FY2022": -92, "FY2021": 114,
    }),
    ("DATA", "Other costs/income", {
        "FY2025": -27, "FY2024": -9, "FY2023": -12, "FY2022": -2, "FY2021": 10,
    }),
    ("TOTAL", "Net other income", {
        "FY2025": 1338, "FY2024": 582, "FY2023": 198, "FY2022": 465, "FY2021": 398,
    }),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Staff costs", {
        "FY2025": -16456, "FY2024": -15738, "FY2023": -13348, "FY2022": -11214, "FY2021": -10151,
    }),
    ("DATA", "Depreciation", {
        "FY2025": -1475, "FY2024": -1341, "FY2023": -1510, "FY2022": -1119, "FY2021": -933,
    }),
    ("DATA", "Administrative and general expenses", {
        "FY2025": -10488, "FY2024": -9423, "FY2023": -8566, "FY2022": -6743, "FY2021": -5179,
    }),
    ("TOTAL", "Operating expenses", {
        "FY2025": -28419, "FY2024": -26502, "FY2023": -23424, "FY2022": -19076, "FY2021": -16263,
    }),
    ("TOTAL", "Operating profit before credit impairment losses", {
        "FY2025": 12453, "FY2024": 13792, "FY2023": 12421, "FY2022": 7063, "FY2021": 3781,
    }),
    ("DATA", "Credit impairment reversals/(charges)", {
        "FY2025": 937, "FY2024": 1183, "FY2023": 866, "FY2022": -684, "FY2021": 68,
    }),
    ("TOTAL", "Profit before tax", {
        "FY2025": 13390, "FY2024": 14975, "FY2023": 13287, "FY2022": 6379, "FY2021": 3849,
    }),
    ("DATA", "Tax charge/(credit)", {
        "FY2025": -3367, "FY2024": -3888, "FY2023": -735, "FY2022": -679, "FY2021": 626,
    }),
    ("TOTAL", "Profit after tax", {
        "FY2025": 10023, "FY2024": 11087, "FY2023": 12552, "FY2022": 5700, "FY2021": 4475,
    }),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Fair value through OCI reserve - net gains/(losses) from changes in fair value", {
        "FY2025": 283, "FY2024": 90, "FY2023": 997, "FY2022": -1210, "FY2021": -486,
    }),
    ("DATA", "Fair value through OCI reserve - reversal due to sale of investment", {
        "FY2022": 92, "FY2021": -20,
    }),
    ("DATA", "Fair value through OCI reserve - deferred tax", {
        "FY2025": -71, "FY2024": -18, "FY2023": -178, "FY2022": 212, "FY2021": 96,
    }),
    ("DATA", "Net reversals/(losses) transferred to income statement due to impairment", {
        "FY2022": -13, "FY2021": -44,
    }),
    ("TOTAL", "Other comprehensive income for the year, net of tax", {
        "FY2025": 212, "FY2024": 72, "FY2023": 819, "FY2022": -919, "FY2021": -454,
    }),
    ("TOTAL", "Total comprehensive income for the year, net of tax", {
        "FY2025": 10235, "FY2024": 11159, "FY2023": 13371, "FY2022": 4781, "FY2021": 4021,
    }),
]

bw.add_income_statement_sheet(
    title="Habib Bank Zurich Plc — Profit & Loss",
    subtitle="Income Statement and Statement of Comprehensive Income, figures as reported in each year's own Annual Report",
    rows=income_statement_rows,
    sources_text=INCOME_STATEMENT_SOURCES,
    first_col_width=72,
    source_height=190,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet 3: Statement of Changes in Equity
# ---------------------------------------------------------------
equity_headers = ["Called up share capital", "Fair value reserve", "Retained earnings", "Total"]
equity_rows = [
    ("TOTAL", "Balance as at 1 January 2021", (60000, 356, 11826, 72182)),
    ("DATA", "Capital raised during the year", (10000, None, None, 10000)),
    ("DATA", "Profit after tax", (None, None, 4475, 4475)),
    ("DATA", "FV through OCI reserve - net losses during the year", (None, -486, None, -486)),
    ("DATA", "FV through OCI reserve - reversal due to sale of investment", (None, -20, None, -20)),
    ("DATA", "Deferred tax", (None, 96, None, 96)),
    ("DATA", "Net reversals transferred due to impairment", (None, -44, None, -44)),
    ("TOTAL", "Balance as at 31 December 2021 / 1 January 2022", (70000, -98, 16301, 86203)),
    ("DATA", "Dividend paid during the year", (None, None, -1476, -1476)),
    ("DATA", "Profit after tax", (None, None, 5700, 5700)),
    ("DATA", "FV through OCI reserve - net losses during the year", (None, -1210, None, -1210)),
    ("DATA", "FV through OCI reserve - reversal due to sale of investment", (None, 92, None, 92)),
    ("DATA", "Deferred tax", (None, 212, None, 212)),
    ("DATA", "Net reversals transferred due to impairment", (None, -13, None, -13)),
    ("TOTAL", "Balance as at 31 December 2022 / 1 January 2023", (70000, -1017, 20525, 89508)),
    ("DATA", "Profit after tax", (None, None, 12552, 12552)),
    ("DATA", "FV through OCI reserve - net gains during the year", (None, 997, None, 997)),
    ("DATA", "Deferred tax", (None, -178, None, -178)),
    ("TOTAL", "Balance as at 31 December 2023 / 1 January 2024", (70000, -198, 33077, 102879)),
    ("DATA", "Dividend paid during the year", (None, None, -4142, -4142)),
    ("DATA", "Additional capital", (10000, None, None, 10000)),
    ("DATA", "Profit after tax", (None, None, 11087, 11087)),
    ("DATA", "FV through OCI reserve - net losses during the year", (None, 90, None, 90)),
    ("DATA", "Deferred tax", (None, -18, None, -18)),
    ("TOTAL", "Balance as at 31 December 2024 / 1 January 2025", (80000, -126, 40022, 119896)),
    ("DATA", "Dividend declared & paid during the year", (None, None, -5544, -5544)),
    ("DATA", "Profit after tax", (None, None, 10023, 10023)),
    ("DATA", "FV through OCI reserve - net gains during the year", (None, 283, None, 283)),
    ("DATA", "Deferred tax", (None, -71, None, -71)),
    ("TOTAL", "Balance as at 31 December 2025", (80000, 86, 44501, 124587)),
]

bw.add_equity_changes_sheet(
    title="Habib Bank Zurich Plc — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, figures as reported in each year's own Annual Report",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=EQUITY_SOURCES,
    first_col_width=58,
    source_height=210,
)

# ---------------------------------------------------------------
# Sheet 4: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax", {
        "FY2025": 13390, "FY2024": 14975, "FY2023": 13287, "FY2022": 6379, "FY2021": 3849,
    }),
    ("DATA", "(Reversals)/impairment losses on loans and advances at amortised cost", {
        "FY2025": -937, "FY2024": -1183, "FY2023": -866, "FY2022": 684, "FY2021": -68,
    }),
    ("DATA", "(Gain)/loss on sale of financial assets at FVOCI", {
        "FY2025": -508, "FY2022": 92, "FY2021": -114,
    }),
    ("DATA", "Depreciation", {
        "FY2025": 1475, "FY2024": 1341, "FY2023": 1510, "FY2022": 1119, "FY2021": 933,
    }),
    ("DATA", "Gain on sale of property and equipment", {
        "FY2021": -1,
    }),
    ("TOTAL", "Profit before tax adjusted for non-cash items", {
        "FY2025": 13420, "FY2024": 15133, "FY2023": 13931, "FY2022": 8274, "FY2021": 4599,
    }),
    ("SECTION", "Net (increase)/decrease in operating assets", {}),
    ("DATA", "Loans and advances to banks at amortised cost", {
        "FY2025": -31608, "FY2024": -9363, "FY2023": 29645, "FY2022": -55923, "FY2021": 11053,
    }),
    ("DATA", "Loans and advances to customers at amortised cost", {
        "FY2025": -117191, "FY2024": -49138, "FY2023": -30221, "FY2022": -87685, "FY2021": -58584,
    }),
    ("DATA", "Derivative financial instruments for risk management", {
        "FY2025": -516, "FY2024": -125, "FY2023": 91, "FY2022": 112, "FY2021": 312,
    }),
    ("DATA", "Other assets", {
        "FY2025": 1037, "FY2024": -1011, "FY2023": -1651, "FY2022": 1128, "FY2021": -966,
    }),
    ("TOTAL", "Net (increase)/decrease in operating assets", {
        "FY2025": -148278, "FY2024": -59637, "FY2023": -2136, "FY2022": -142368, "FY2021": -48185,
    }),
    ("SECTION", "Net increase/(decrease) in operating liabilities", {}),
    ("DATA", "Due to banks at amortised cost", {
        "FY2025": 77915, "FY2024": -15357, "FY2023": -4420, "FY2022": 22119, "FY2021": 67056,
    }),
    ("DATA", "Due to customers at amortised cost", {
        "FY2025": 119800, "FY2024": 137112, "FY2023": 116334, "FY2022": 97548, "FY2021": 48364,
    }),
    ("DATA", "Derivative financial instruments for risk management", {
        "FY2025": -23, "FY2024": 145, "FY2023": -187, "FY2022": -285, "FY2021": 156,
    }),
    ("DATA", "Accruals, deferred income and other liabilities", {
        "FY2025": -2295, "FY2024": 3204, "FY2023": 2710, "FY2022": 4453, "FY2021": 351,
    }),
    ("DATA", "Tax paid", {
        "FY2025": -4395, "FY2024": -3029, "FY2023": -931, "FY2022": -824, "FY2021": -306,
    }),
    ("TOTAL", "Net increase/(decrease) in operating liabilities", {
        "FY2025": 191002, "FY2024": 122075, "FY2023": 113506, "FY2022": 123011, "FY2021": 115621,
    }),
    ("TOTAL", "Net cash flow from operating activities", {
        "FY2025": 56144, "FY2024": 77571, "FY2023": 125301, "FY2022": -11083, "FY2021": 72035,
    }),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property and equipment", {
        "FY2025": -313, "FY2024": -193, "FY2023": -1437, "FY2022": -8990, "FY2021": -652,
    }),
    ("DATA", "Proceeds on sale of property and equipment", {
        "FY2022": 0, "FY2021": 1,
    }),
    ("DATA", "Intangible assets under development", {
        "FY2025": -808,
    }),
    ("DATA", "Purchase of financial investments", {
        "FY2025": -101174, "FY2024": -133828, "FY2023": -91617, "FY2022": -19234, "FY2021": -114123,
    }),
    ("DATA", "Proceeds on sale/maturity of financial investments", {
        "FY2025": 111192, "FY2024": 69499, "FY2023": 73406, "FY2022": 49525, "FY2021": 42421,
    }),
    ("TOTAL", "Net cash from/(used in) investing activities", {
        "FY2025": 8897, "FY2024": -64522, "FY2023": -19648, "FY2022": 21301, "FY2021": -72353,
    }),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Capital issuance", {
        "FY2024": 10000, "FY2021": 10000,
    }),
    ("DATA", "Dividend paid", {
        "FY2025": -5543, "FY2024": -4142, "FY2022": -1476,
    }),
    ("DATA", "Leases paid", {
        "FY2025": -630, "FY2024": -461, "FY2023": -424, "FY2022": -434, "FY2021": -432,
    }),
    ("DATA", "Interest paid/(charges) on subordinated liabilities", {
        "FY2025": -31, "FY2024": -1408, "FY2023": -1199, "FY2022": -491, "FY2021": 29,
    }),
    ("TOTAL", "Net cash from/(used in) financing activities", {
        "FY2025": -6204, "FY2024": 3989, "FY2023": -1623, "FY2022": -2401, "FY2021": 9597,
    }),
    ("TOTAL", "Net increase in cash and cash equivalents", {
        "FY2025": 58837, "FY2024": 17038, "FY2023": 104030, "FY2022": 7817, "FY2021": 9279,
    }),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {
        "FY2025": 232380, "FY2024": 215342, "FY2023": 111312, "FY2022": 88689, "FY2021": 79410,
    }),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {
        "FY2025": 291217, "FY2024": 232380, "FY2023": 215342, "FY2022": 96506, "FY2021": 88689,
    }),
]

bw.add_cash_flow_sheet(
    title="Habib Bank Zurich Plc — Cash Flow Statement",
    subtitle="Figures as reported in each year's own Annual Report and Financial Statements",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=70,
    source_height=210,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to customers at amortised cost, gross carrying amount", {}),
    ("DATA", "Stage 1 (12-month ECL)", {
        "FY2025": 763217, "FY2023": 593300, "FY2022": 560009, "FY2021": 493355,
    }),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {
        "FY2025": 33227, "FY2023": 25704, "FY2022": 26131, "FY2021": 12310,
    }),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired)", {
        "FY2025": 6076, "FY2023": 17310, "FY2022": 20029, "FY2021": 12849,
    }),
    ("TOTAL", "Total gross loans and advances to customers", {
        "FY2025": 802520, "FY2024": 685362, "FY2023": 636314, "FY2022": 606169, "FY2021": 518514,
    }),
    ("DATA", "Less: loss allowance", {
        "FY2025": -1922, "FY2024": -2892, "FY2023": -4165, "FY2022": -5107, "FY2021": -4453,
    }),
    ("TOTAL", "Net loans and advances to customers", {
        "FY2025": 800598, "FY2024": 682470, "FY2023": 632149, "FY2022": 601062, "FY2021": 514061,
    }),
    ("SECTION", "Derived ratios", {}),
    ("DATA", "Stage 3 / gross loans (derived NPL ratio)", {
        "FY2025": "0.76%", "FY2023": "2.72%", "FY2022": "3.30%", "FY2021": "2.48%",
    }),
    ("DATA", "Loss allowance / gross loans (derived coverage ratio)", {
        "FY2025": "0.24%", "FY2024": "0.42%", "FY2023": "0.65%", "FY2022": "0.84%", "FY2021": "0.86%",
    }),
]

bw.add_asset_quality_sheet(
    title="Habib Bank Zurich Plc — Asset Quality",
    subtitle="Loans and advances to customers by IFRS 9 stage, figures as reported in each year's own Annual Report",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=64,
    source_height=200,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=140)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {
        "FY2025": 124587, "FY2024": 119896, "FY2023": 103077, "FY2022": 90525, "FY2021": 86301,
    })],
    p3_sources(),
    note="No Additional Tier 1 capital is disclosed in any year, so CET1 = Tier 1 capital throughout.",
)
bw.add_not_disclosed_metric_sheets(["CET1 Ratio"], p3_sources(),
    per_note={"CET1 Ratio": "No RWA figure is disclosed in any year's statutory accounts, so this ratio cannot be computed."})

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {
        "FY2025": 124587, "FY2024": 119896, "FY2023": 103077, "FY2022": 90525, "FY2021": 86301,
    })],
    p3_sources(),
    note="Equal to CET1 capital - no Additional Tier 1 instruments are disclosed in any year.",
)
bw.add_not_disclosed_metric_sheets(["Tier 1 Ratio"], p3_sources(),
    per_note={"Tier 1 Ratio": "No RWA figure is disclosed in any year's statutory accounts, so this ratio cannot be computed."})

metric(
    "Total Capital", "£'000",
    [("Own funds (Tier 1 + Tier 2 capital)", {
        "FY2025": 144852, "FY2024": 140192, "FY2023": 123417, "FY2022": 111377, "FY2021": 106687,
    })],
    p3_sources(),
    note="Tier 2 capital comprises qualifying subordinated liabilities (plus, in FY2023/FY2022, a small IFRS 9 "
         "ECL regulatory-capital adjustment disclosed by the Bank).",
)
bw.add_not_disclosed_metric_sheets(
    ["Total Capital Ratio", "Total RWAs"], p3_sources(),
    per_note={
        "Total Capital Ratio": "No RWA figure is disclosed in any year's statutory accounts, so this ratio cannot be computed.",
        "Total RWAs": "Not disclosed in any year's statutory accounts.",
    },
)

rwa_breakdown_rows = [
    ("DATA", "Not publicly disclosed - Habib Bank Zurich Plc does not publish a standalone Pillar 3 "
             "disclosure and no RWA figure (aggregate or by risk category) appears in any year's statutory "
             "accounts, confirmed by reading each year's capital management note (31.25) in full.", {}),
]
bw.add_rwa_breakdown_sheet(
    title="Habib Bank Zurich Plc — RWA Breakdown",
    subtitle="See source note - no RWA figure of any kind is published for this entity.",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources(),
    first_col_width=90,
    source_height=220,
)

bw.add_not_disclosed_metric_sheets(
    ["Leverage Ratio"], p3_sources(),
    per_note={"Leverage Ratio": "No leverage exposure measure is disclosed in any year's statutory accounts."},
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio (average for the period)", {
        "FY2025": "232%", "FY2024": "287%", "FY2023": "196%", "FY2022": "205%", "FY2021": "159%",
    })],
    p3_sources(),
    note="The Bank discloses LCR on 4 bases each year (as at 31 December, average/maximum/minimum for the "
         "period); the average-for-the-period figure is used for consistency with this project's convention "
         "elsewhere. As-at-31-December figures are higher every year (e.g. FY2025 180%, FY2024 243%).",
)
bw.add_not_disclosed_metric_sheets(
    ["NSFR", "MREL Ratio"], p3_sources(),
    per_note={
        "NSFR": "Not disclosed in any year's statutory accounts.",
        "MREL Ratio": "Not disclosed - Habib Bank Zurich Plc is not identified as a UK resolution entity in these accounts.",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {
            "FY2025": 1483269, "FY2024": 1284398, "FY2023": 1145027, "FY2022": 1019038, "FY2021": 892077,
        }),
        ("Loans and advances to customers at amortised cost", {
            "FY2025": 800598, "FY2024": 682470, "FY2023": 632149, "FY2022": 601062, "FY2021": 514061,
        }),
        ("Due to customers at amortised cost", {
            "FY2025": 1142802, "FY2024": 1023002, "FY2023": 885890, "FY2022": 769556, "FY2021": 672008,
        }),
        ("Total equity", {
            "FY2025": 124587, "FY2024": 119896, "FY2023": 102879, "FY2022": 89508, "FY2021": 86203,
        }),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net interest income", {
            "FY2025": 37734, "FY2024": 37997, "FY2023": 34164, "FY2022": 23911, "FY2021": 17755,
        }),
        ("Operating expenses", {
            "FY2025": -28419, "FY2024": -26502, "FY2023": -23424, "FY2022": -19076, "FY2021": -16263,
        }),
        ("Profit after tax", {
            "FY2025": 10023, "FY2024": 11087, "FY2023": 12552, "FY2022": 5700, "FY2021": 4475,
        }),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {
            "FY2025": 119896, "FY2024": 102879, "FY2023": 89508, "FY2022": 86203, "FY2021": 72182,
        }),
        ("Total comprehensive income for the year, net of tax", {
            "FY2025": 10235, "FY2024": 11159, "FY2023": 13371, "FY2022": 4781, "FY2021": 4021,
        }),
        ("Other equity movements, net", {
            "FY2025": -5544, "FY2024": 5858, "FY2023": 0, "FY2022": -1476, "FY2021": 10000,
        }),
        ("Closing equity", {
            "FY2025": 124587, "FY2024": 119896, "FY2023": 102879, "FY2022": 89508, "FY2021": 86203,
        }),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {
            "FY2025": 56144, "FY2024": 77571, "FY2023": 125301, "FY2022": -11083, "FY2021": 72035,
        }),
        ("Net cash from/(used in) investing activities", {
            "FY2025": 8897, "FY2024": -64522, "FY2023": -19648, "FY2022": 21301, "FY2021": -72353,
        }),
        ("Net cash from/(used in) financing activities", {
            "FY2025": -6204, "FY2024": 3989, "FY2023": -1623, "FY2022": -2401, "FY2021": 9597,
        }),
        ("Cash and cash equivalents at end of year", {
            "FY2025": 291217, "FY2024": 232380, "FY2023": 215342, "FY2022": 96506, "FY2021": 88689,
        }),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("LCR (average, %)", {
            "FY2025": 232, "FY2024": 287, "FY2023": 196, "FY2022": 205, "FY2021": 159,
        }),
    ],
    note="Only LCR is charted here - CET1/Tier 1/Total Capital Ratio, Leverage Ratio, NSFR and MREL Ratio are "
         "not disclosed in this entity's statutory accounts (no standalone Pillar 3 document exists and no RWA "
         "figure is published); see the individual Pillar 3 metric sheets. Figures are duplicated from the "
         "detail sheets for at-a-glance trend viewing; see each sheet's own source citation for the underlying "
         "document/page.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/HABIB BANK ZURICH FINANCIALS.xlsx")
