import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Full 5 years of cash flow AND Pillar 3 coverage, FY2021-FY2025. No FRS 101/102
# cash-flow exemption. Bank-solo ("BLME plc") basis throughout for both statements -
# BLME also publishes wider "BLME Holdings" group accounts but the PRA entity here
# is the plc, and its Pillar 3 KM1 tables are already at the plc level.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

CH_URL = "https://find-and-update.company-information.service.gov.uk/company/05897786"
FS2025_URL = "https://www.blme.com/media/z0jd2sah/blme-plc-financial-statements-31-december-2025.pdf"
FS2024_URL = "https://www.blme.com/media/rneds5db/blme-plc-financial-statements-31-december-2024.pdf"
FS2023_URL = "https://www.blme.com/media/2j5fy4tv/blme-plc-financial-statements-31-december-2023.pdf"
FS2022_URL = "https://www.blme.com/media/2014/blme-plc-financial-statements-31-december-2022.pdf"
FS2021_URL = "https://www.blme.com/media/1964/blme-plc-fin-stats-31-december-2021-for-website.pdf"
P32025_URL = "https://www.blme.com/media/jf2dbyrm/2025-pillar-iii-disclosure.pdf"
P32024_URL = "https://www.blme.com/media/mhantsoh/2024-pillar-iii-disclosure.pdf"
P32023_URL = "https://www.blme.com/media/fluobg0d/2023-pillar-iii-disclosure.pdf"
P32022_URL = "https://www.blme.com/media/2017/2022-pillar-iii-disclosure.pdf"
P32021_URL = "https://www.blme.com/media/1997/2021-pillar-iii-disclosure.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Bank of London and The Middle East plc (FRN 464292, Companies House 05897786, matches "
    "Banks List 2608.xlsx exactly) is a UK-incorporated Sharia-compliant wholesale/private bank, majority-owned "
    "by Boubyan Bank (Kuwait). It publishes both wider 'BLME Holdings' group accounts and standalone 'BLME plc' "
    "(Bank-solo) accounts on its own site - this workbook uses the plc/solo figures throughout for both the cash "
    "flow statement and Pillar 3, matching the PRA-regulated entity. Terminology uses 'profit'/'financing' rather "
    "than 'interest'/'loans' (Sharia-compliant banking), consistent with ALRAYAN Bank elsewhere in this project."
)

CASH_FLOW_SOURCES = (
    "Sources - BLME plc's own Statement of Cash Flows, £'000s, all years, each from that year's own "
    "originally-published Financial Statements (not a later restated comparative):\n"
    f"FY2025: BLME plc Financial Statements 31 December 2025, p.31-32 - {FS2025_URL}\n"
    f"FY2024: BLME plc Financial Statements 31 December 2024, p.31 - {FS2024_URL}\n"
    f"FY2023: BLME plc Financial Statements 31 December 2023, p.32 - {FS2023_URL}\n"
    f"FY2022: BLME plc Financial Statements 31 December 2022, p.32 - {FS2022_URL}\n"
    f"FY2021: BLME plc Financial Statements 31 December 2021, p.30 - {FS2021_URL}\n"
    "The FY2025 report restates FY2024's comparative (a prior period adjustment of -£9,035k to retained earnings "
    "at 1 Jan 2024, per its own Note 2.3), and the FY2024 report itself already restated FY2023's comparative "
    "(-£3,964k, per its own Note 2b) - both are genuine disclosed restatements, but every column in this sheet "
    "uses each year's own originally-published figures (project convention), not a later restated version.\n"
    "Presentation changed twice across the 5 years: FY2021-FY2023 include a separate 'Due from customers' line "
    "in operating assets (dropped from FY2024 onward), and FY2025 combines the 'operating assets' and 'operating "
    "liabilities' movements into a single unlabelled subtotal rather than the two separate ones FY2021-FY2024 "
    "printed - shown as blank cells where a line doesn't apply that year, not gaps. All TOTAL rows reconcile "
    "exactly to source for every year.\n\n"
    + ENTITY_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - BLME plc's own Pillar III Disclosures, £m capital amounts / % ratios, all years:\n"
        f"FY2025: Pillar III Disclosure - 31 December 2025, Key metrics table, p.4 - {P32025_URL}\n"
        f"FY2024: Pillar III Disclosure - 31 December 2024, Key metrics table, p.4 - {P32024_URL}\n"
        f"FY2023: Pillar III Disclosure - 31 December 2023, Key metrics table, p.4 - {P32023_URL}\n"
        f"FY2022: Pillar III Disclosure - 31 December 2022, Key metrics table, p.4 - {P32022_URL}\n"
        f"FY2021: sourced from the FY2022 Pillar III Disclosure's own FY2021 comparative column, Key metrics "
        f"table, p.4 - {P32022_URL} (the FY2021 edition itself, {P32021_URL}, pre-dates BLME's adoption of the "
        f"standardised KM1 template - it uses the older CRR own-funds/appendix format instead, so the FY2022 "
        f"report's comparative column is used for consistency with every other year in this workbook).\n"
        + (extra + "\n" if extra else "")
        + "\n" + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="Bank of London and The Middle East plc", years=YEARS, year_label=YEAR_LABEL,
                   header_color="5D3FD3")

# ---------------------------------------------------------------
# ST- rollout (batch ST-013): Balance Sheet, P&L, Statement of Changes in
# Equity, Asset Quality, RWA Breakdown. Sourced from the same 5 Companies
# House / blme.com Financial Statements filings already cited above
# (FS20XX_URL) - each year's OWN originally-published report is used
# (project convention), not a later restated comparative column, even
# though the FY2024 and FY2025 reports both restate their prior year's
# comparative (Note 2.3/2b) - see PRESENTATION_NOTE below.
# ---------------------------------------------------------------
STATEMENTS_SOURCES = (
    "Sources - BLME plc's own Income Statement / Statement of Financial Position / Statement of Changes in "
    "Equity, £'000s, each from that year's own originally-published Financial Statements:\n"
    f"FY2025: BLME plc Financial Statements 31 December 2025, pp.26,28-29 - {FS2025_URL}\n"
    f"FY2024: BLME plc Financial Statements 31 December 2024, pp.28,30,32 - {FS2024_URL}\n"
    f"FY2023: BLME plc Financial Statements 31 December 2023, pp.29,31,33 - {FS2023_URL}\n"
    f"FY2022: BLME plc Financial Statements 31 December 2022, pp.29,31,33 - {FS2022_URL}\n"
    f"FY2021: BLME plc Financial Statements 31 December 2021, pp.27,29,31 - {FS2021_URL}\n\n"
    + ENTITY_NOTE
)

PRESENTATION_NOTE = (
    "PRESENTATION NOTE: the FY2024 report restated FY2023's comparative (Note 2b, -£3,964k to retained earnings "
    "at 1 Jan 2023) and the FY2025 report restated FY2024's comparative (Note 2.3, -£8,762k to retained earnings "
    "at 1 Jan 2024) - both genuine disclosed restatements. Every P&L/Balance Sheet column here uses each year's "
    "own originally-published figures (project convention, matching the Cash Flow Statement sheet), and the "
    "Statement of Changes in Equity shows both restatements as explicit 'Prior period adjustment' rows (as "
    "disclosed) rather than silently bridging FY2023->FY2024 or FY2024->FY2025. 'Investments in subsidiaries' "
    "only appears as its own Balance Sheet line FY2024-25 (FY2021-23's own reports don't show it separately); "
    "'Due from customers' only appears FY2021-22 (nil/absent thereafter); 'Profit rate swaps' liability only "
    "appears FY2021 (£334k, nil FY2022 onward); 'Assets held for sale' is a one-off FY2023 line (£29,934k). "
    "FY2025's own equity statement renames the 'Fair value reserve' column 'Other reserves' - shown here under "
    "the FY2021-24 label for column consistency; the underlying balance is the same reserve."
)

# ---------------------------------------------------------------
# Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents", {"FY2025": 130528, "FY2024": 90139, "FY2023": 76008, "FY2022": 135262, "FY2021": 112076}),
    ("DATA", "Due from financial institutions", {"FY2025": 26703, "FY2024": 153704, "FY2023": 299363, "FY2022": 451675, "FY2021": 479210}),
    ("DATA", "Due from customers", {"FY2022": 0, "FY2021": 24993}),
    ("DATA", "Investment securities", {"FY2025": 29228, "FY2024": 44584, "FY2023": 44927, "FY2022": 35734, "FY2021": 59807}),
    ("DATA", "Investments in subsidiaries", {"FY2025": 21574, "FY2024": 29151}),
    ("DATA", "Financing arrangements", {"FY2025": 1218128, "FY2024": 1151123, "FY2023": 1010255, "FY2022": 912937, "FY2021": 800318}),
    ("DATA", "Finance lease receivables", {"FY2025": 1424, "FY2024": 2705, "FY2023": 3014, "FY2022": 35550, "FY2021": 42755}),
    ("DATA", "Investment in joint ventures", {"FY2025": 28994, "FY2024": 32157, "FY2023": 7350, "FY2022": 1154, "FY2021": 1157}),
    ("DATA", "Property and equipment", {"FY2025": 1336, "FY2024": 2136, "FY2023": 2548, "FY2022": 3801, "FY2021": 2782}),
    ("DATA", "Intangible assets", {"FY2025": 2661, "FY2024": 2611, "FY2023": 1607, "FY2022": 714}),
    ("DATA", "Other assets", {"FY2025": 8793, "FY2024": 16450, "FY2023": 6421, "FY2022": 17221, "FY2021": 11719}),
    ("DATA", "Current tax asset", {"FY2025": 1015, "FY2024": 1998, "FY2023": 2243, "FY2022": 2587, "FY2021": 934}),
    ("DATA", "Deferred tax asset", {"FY2025": 14418, "FY2024": 13600, "FY2023": 13830, "FY2022": 15741, "FY2021": 13099}),
    ("DATA", "Assets held for sale", {"FY2023": 29934}),
    ("TOTAL", "Total assets", {"FY2025": 1484802, "FY2024": 1540358, "FY2023": 1497500, "FY2022": 1612376, "FY2021": 1548850}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Due to financial institutions", {"FY2025": 49571, "FY2024": 33754, "FY2023": 6967, "FY2022": 51039, "FY2021": 272605}),
    ("DATA", "Due to customers", {"FY2025": 1197104, "FY2024": 1262682, "FY2023": 1248979, "FY2022": 1323870, "FY2021": 1031887}),
    ("DATA", "Profit rate swaps", {"FY2021": 334}),
    ("DATA", "Other liabilities", {"FY2025": 14059, "FY2024": 13088, "FY2023": 13322, "FY2022": 14552, "FY2021": 14307}),
    ("TOTAL", "Total liabilities", {"FY2025": 1260734, "FY2024": 1309524, "FY2023": 1269268, "FY2022": 1389461, "FY2021": 1319133}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 48933, "FY2024": 48933, "FY2023": 48933, "FY2022": 48933, "FY2021": 48933}),
    ("DATA", "Share premium", {"FY2025": 140623, "FY2024": 140623, "FY2023": 140623, "FY2022": 140623, "FY2021": 140623}),
    ("DATA", "Capital contribution", {"FY2025": 3527, "FY2024": 3527, "FY2023": 3527, "FY2022": 3527, "FY2021": 3527}),
    ("DATA", "Fair value reserve", {"FY2025": -145, "FY2024": -347, "FY2023": -63, "FY2022": -108, "FY2021": -107}),
    ("DATA", "Retained earnings", {"FY2025": 31130, "FY2024": 38098, "FY2023": 35212, "FY2022": 29940, "FY2021": 36741}),
    ("TOTAL", "Total equity", {"FY2025": 224068, "FY2024": 230834, "FY2023": 228232, "FY2022": 222915, "FY2021": 229717}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 1484802, "FY2024": 1540358, "FY2023": 1497500, "FY2022": 1612376, "FY2021": 1548850}),
]

bw.add_balance_sheet_sheet(
    title="Bank of London and The Middle East plc — Statement of Financial Position",
    subtitle="BLME plc, Bank-solo basis, £'000s.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + PRESENTATION_NOTE,
    first_col_width=64,
    source_height=420,
    unit_suffix=" (£'000s)",
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Income from financing and investing activities", {"FY2025": 92246, "FY2024": 96103, "FY2023": 81198, "FY2022": 57261, "FY2021": 47649}),
    ("DATA", "Returns to financial institutions and customers", {"FY2025": -53752, "FY2024": -57877, "FY2023": -45550, "FY2022": -23845, "FY2021": -17678}),
    ("TOTAL", "Net margin", {"FY2025": 38494, "FY2024": 38226, "FY2023": 35648, "FY2022": 33416, "FY2021": 29971}),
    ("DATA", "Fee and commission income", {"FY2025": 2274, "FY2024": 2232, "FY2023": 1764, "FY2022": 364, "FY2021": 665}),
    ("DATA", "Fee and commission expense", {"FY2025": -5321, "FY2024": -2135, "FY2023": -1381, "FY2022": -964, "FY2021": -2417}),
    ("TOTAL", "Net fee and commission income", {"FY2025": -3047, "FY2024": 97, "FY2023": 383, "FY2022": -600, "FY2021": -1752}),
    ("DATA", "Net investment gains", {"FY2023": 0, "FY2022": 629, "FY2021": 763}),
    ("DATA", "Credit impairment (losses)/gains", {"FY2025": -3938, "FY2024": -3236, "FY2023": 555, "FY2022": -13398, "FY2021": -12451}),
    ("DATA", "Impairment of investment in subsidiary", {"FY2025": 1185, "FY2024": 339, "FY2023": -3434}),
    ("DATA", "Other operating income", {"FY2025": 17795, "FY2024": 13440, "FY2023": 14785, "FY2022": 11274, "FY2021": 4720}),
    ("DATA", "Share of profit/(loss) of equity-accounted investees, net of tax", {"FY2025": 658, "FY2024": 2921, "FY2023": 81, "FY2022": 97, "FY2021": 98}),
    ("TOTAL", "Net operating income", {"FY2025": 51147, "FY2024": 51787, "FY2023": 48018, "FY2022": 31418, "FY2021": 21349}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Personnel/staff costs", {"FY2025": -28090, "FY2024": -27850, "FY2023": -23624, "FY2022": -20134, "FY2021": -14090}),
    ("DATA", "Other operating expenses", {"FY2025": -20212, "FY2024": -15301, "FY2023": -15547, "FY2022": -19364, "FY2021": -13631}),
    ("DATA", "Other depreciation and amortisation", {"FY2025": -1242, "FY2024": -897, "FY2023": -1010, "FY2022": -957, "FY2021": -804}),
    ("TOTAL", "Total operating expenses", {"FY2025": -49544, "FY2024": -44048, "FY2023": -40181, "FY2022": -40455, "FY2021": -28525}),
    ("TOTAL", "Profit/(loss) before tax", {"FY2025": 1603, "FY2024": 7739, "FY2023": 7837, "FY2022": -9037, "FY2021": -7176}),
    ("DATA", "Tax charge/credit", {"FY2025": -184, "FY2024": -889, "FY2023": -2515, "FY2022": 2230, "FY2021": 2840}),
    ("TOTAL", "Profit/(loss) for the year", {"FY2025": 1419, "FY2024": 6850, "FY2023": 5322, "FY2022": -6807, "FY2021": -4336}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Other comprehensive income/(expense), net of tax", {"FY2025": -43, "FY2024": -284, "FY2023": -5, "FY2022": 7, "FY2021": -208}),
    ("TOTAL", "Total comprehensive income/(loss) for the year", {"FY2025": 1376, "FY2024": 6566, "FY2023": 5317, "FY2022": -6800, "FY2021": -4544}),
]

bw.add_income_statement_sheet(
    title="Bank of London and The Middle East plc — Income Statement",
    subtitle="BLME plc, Bank-solo basis, £'000s.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + PRESENTATION_NOTE,
    first_col_width=64,
    source_height=420,
    unit_suffix=" (£'000s)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity (chronological)
# ---------------------------------------------------------------
equity_changes_rows = [
    ("TOTAL", "At 1 January 2021", (48933, 140623, 3527, 101, 41077, 234261)),
    ("DATA", "Loss for the year (FY2021)", (None, None, None, None, -4336, -4336)),
    ("DATA", "Other comprehensive expense (FY2021)", (None, None, None, -208, None, -208)),
    ("TOTAL", "At 31 December 2021", (48933, 140623, 3527, -107, 36741, 229717)),
    ("DATA", "Loss for the year (FY2022)", (None, None, None, None, -6807, -6807)),
    ("DATA", "Other comprehensive income (FY2022)", (None, None, None, 7, None, 7)),
    ("DATA", "Transactions with owners, net (FY2022)", (None, None, None, -8, 6, -2)),
    ("TOTAL", "At 31 December 2022", (48933, 140623, 3527, -108, 29940, 222915)),
    ("DATA", "Profit for the year (FY2023)", (None, None, None, None, 5322, 5322)),
    ("DATA", "Other comprehensive expense (FY2023)", (None, None, None, -5, None, -5)),
    ("DATA", "Transactions with owners, net (FY2023)", (None, None, None, 50, -50, 0)),
    ("TOTAL", "At 31 December 2023", (48933, 140623, 3527, -63, 35212, 228232)),
    ("DATA", "Prior period adjustment (FY2024 Annual Report Note 2b)", (None, None, None, None, -3964, -3964)),
    ("TOTAL", "At 1 January 2024 (as restated)", (48933, 140623, 3527, -63, 31248, 224268)),
    ("DATA", "Profit for the year (FY2024)", (None, None, None, None, 6850, 6850)),
    ("DATA", "Other comprehensive expense (FY2024)", (None, None, None, -284, None, -284)),
    ("TOTAL", "At 31 December 2024", (48933, 140623, 3527, -347, 38098, 230834)),
    ("DATA", "Prior period adjustment (FY2025 Annual Report Note 2.3)", (None, None, None, None, -8762, -8762)),
    ("TOTAL", "At 1 January 2025 (as restated)", (48933, 140623, 3527, -347, 29336, 222072)),
    ("DATA", "Profit for the year (FY2025)", (None, None, None, None, 1419, 1419)),
    ("DATA", "Other comprehensive income/(expense) (FY2025)", (None, None, None, 202, -245, -43)),
    ("DATA", "Sale of equity instrument at FVOCI (FY2025)", (None, None, None, None, 620, 620)),
    ("TOTAL", "At 31 December 2025", (48933, 140623, 3527, -145, 31130, 224068)),
]

bw.add_equity_changes_sheet(
    title="Bank of London and The Middle East plc — Statement of Changes in Equity",
    subtitle="BLME plc, Bank-solo basis, £'000s. Chronological roll-forward, oldest to newest.",
    headers=["Share capital", "Share premium", "Capital contribution", "Fair value reserve", "Retained earnings", "Total"],
    rows=equity_changes_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + PRESENTATION_NOTE,
    first_col_width=54,
    source_height=420,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {"FY2025": 1603, "FY2024": 7739, "FY2023": 7837, "FY2022": -9037, "FY2021": -7176}),
    ("DATA", "Exchange differences", {"FY2025": -21, "FY2024": -3, "FY2023": -5, "FY2022": -10, "FY2021": -12}),
    ("DATA", "Fair value (gain)/loss on investment securities", {"FY2022": 195, "FY2021": -8}),
    ("DATA", "Share of profit of equity-accounted investees, net of tax", {"FY2025": -658, "FY2024": -2921, "FY2023": -81, "FY2022": -97, "FY2021": -100}),
    ("DATA", "Credit impairment losses / provision for impairment", {"FY2025": 3938, "FY2024": 2897, "FY2023": 2879, "FY2022": 13398, "FY2021": 12451}),
    ("DATA", "Impairment of investment in subsidiary", {"FY2025": -1185}),
    ("DATA", "Depreciation and amortisation", {"FY2025": 748, "FY2024": 343, "FY2023": 235, "FY2022": 60, "FY2021": 29}),
    ("DATA", "Movements relating to profit rate swaps", {"FY2022": -112}),
    ("DATA", "IFRS 16 - depreciation and finance charges/additions", {"FY2025": 494, "FY2024": 630, "FY2023": 775, "FY2022": 2797, "FY2021": 878}),
    ("DATA", "Accretion of finance charge on lease liabilities", {"FY2025": 65}),
    ("DATA", "Amortisation of investment securities", {"FY2025": -195, "FY2024": 365, "FY2023": 152, "FY2022": 239, "FY2021": 257}),
    ("DATA", "Net change in fair value of investment in equity/debt at FVOCI", {"FY2025": 280}),
    ("TOTAL", "Net cash generated before changes in operating assets and liabilities",
     {"FY2025": 5069, "FY2024": 9050, "FY2023": 11792, "FY2022": 7433, "FY2021": 6319}),
    ("DATA", "Due from financial institutions", {"FY2025": 127437, "FY2024": 145520, "FY2023": 152940, "FY2022": 26243, "FY2021": -138243}),
    ("DATA", "Due from customers", {"FY2022": 24950, "FY2021": 9594}),
    ("DATA", "Financing arrangements", {"FY2025": -69536, "FY2024": -143580, "FY2023": -97301, "FY2022": -126771, "FY2021": 13336}),
    ("DATA", "Finance lease receivables", {"FY2025": 1262, "FY2024": -1367, "FY2023": 32645, "FY2022": 7214, "FY2021": 159360}),
    ("DATA", "Other assets", {"FY2025": 7645, "FY2024": -10275, "FY2023": 10797, "FY2022": -5460, "FY2021": -4206}),
    ("DATA", "Due to financial institutions", {"FY2025": 15709, "FY2024": 26815, "FY2023": -42286, "FY2022": -226876, "FY2021": 83757}),
    ("DATA", "Due to customers", {"FY2025": -64011, "FY2024": 13193, "FY2023": -75983, "FY2022": 290262, "FY2021": -263860}),
    ("DATA", "Other liabilities", {"FY2025": 1403, "FY2024": -649, "FY2023": 294, "FY2022": 1930, "FY2021": -9295}),
    ("DATA", "Income taxes/corporation tax paid", {"FY2025": -7, "FY2023": -260, "FY2022": -2062, "FY2021": -2847}),
    ("TOTAL", "Net cash generated from/(used in) operating activities",
     {"FY2025": 24971, "FY2024": 38707, "FY2023": -7362, "FY2022": -3137, "FY2021": -146085}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase/(disposal) of property and equipment", {"FY2025": 23, "FY2024": -123, "FY2023": -791, "FY2022": -876, "FY2021": -15}),
    ("DATA", "Purchase of intangible assets", {"FY2025": -452, "FY2024": -1031, "FY2023": -893, "FY2022": -714}),
    ("DATA", "Purchase of investment securities", {"FY2025": -7598, "FY2024": -34858, "FY2023": -15629, "FY2022": -4873}),
    ("DATA", "Sale of investment securities", {"FY2025": 19615, "FY2024": 8006, "FY2023": 1741, "FY2022": 33130, "FY2021": 30483}),
    ("DATA", "Sale of subsidiary to a fellow subsidiary", {"FY2023": 298}),
    ("DATA", "Purchase of interest in assets held for sale", {"FY2023": -35763}),
    ("DATA", "Sale of interest in assets held for sale", {"FY2024": 1800, "FY2023": 6000, "FY2021": 485}),
    ("DATA", "Purchase of interest in joint venture", {"FY2023": -6440}),
    ("DATA", "Dividend(s) received from joint venture(s)", {"FY2025": 2170, "FY2024": 2284, "FY2023": 325, "FY2022": 100, "FY2021": 100}),
    ("DATA", "Sale of equity instrument at FVOCI", {"FY2025": 620}),
    ("DATA", "Sale of interest in joint venture", {"FY2025": 1650}),
    ("TOTAL", "Net cash generated from/(used in) investing activities",
     {"FY2025": 16028, "FY2024": -23922, "FY2023": -51152, "FY2022": 26767, "FY2021": 31053}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Payment of principal portion of lease liabilities", {"FY2025": -512, "FY2024": -589, "FY2023": -719, "FY2022": -1123, "FY2021": -1086}),
    ("DATA", "Payment of finance charge on lease liabilities", {"FY2025": -65}),
    ("TOTAL", "Net cash generated from/(used in) financing activities",
     {"FY2025": -577, "FY2024": -589, "FY2023": -719, "FY2022": -1123, "FY2021": -1086}),
    ("TOTAL", "Net change in cash and cash equivalents",
     {"FY2025": 40422, "FY2024": 14196, "FY2023": -59233, "FY2022": 22507, "FY2021": -116118}),
    ("DATA", "Exchange differences in respect of cash and cash equivalents", {"FY2025": -33, "FY2024": -65, "FY2023": -21, "FY2022": 679, "FY2021": -3292}),
    ("DATA", "Cash and cash equivalents at the beginning of the period", {"FY2025": 90139, "FY2024": 76008, "FY2023": 135262, "FY2022": 112076, "FY2021": 231486}),
    ("TOTAL", "Cash and cash equivalents at the end of the period",
     {"FY2025": 130528, "FY2024": 90139, "FY2023": 76008, "FY2022": 135262, "FY2021": 112076}),
]

bw.add_cash_flow_sheet(
    title="Bank of London and The Middle East plc — Statement of Cash Flows",
    subtitle="BLME plc, Bank-solo basis, £'000s. Full 5 years, no cash-flow exemption.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=80,
    source_height=280,
    unit_suffix=" (£'000s)",
)

# ---------------------------------------------------------------
# Asset Quality: Financing arrangements by IFRS 9 stage - gross exposure
# and ECL allowance, from the Bank's own Note 12/14 "Exposure by Stage" /
# "Impairments of financial assets" tables (each year's own report).
# NOTE: "Total exposure" here is higher than the Balance Sheet's own
# Financing arrangements carrying value because it includes undrawn credit
# facilities and off-balance-sheet commitments (per the Bank's own note) -
# not a reconciliation error.
# ---------------------------------------------------------------
AQ_GROSS_S1 = {"FY2025": 1091948, "FY2024": 1194794, "FY2023": 1105472, "FY2022": 1379874, "FY2021": 1444155}
AQ_GROSS_S2 = {"FY2025": 330284, "FY2024": 226768, "FY2023": 331650, "FY2022": 195379, "FY2021": 99784}
AQ_GROSS_S3 = {"FY2025": 62168, "FY2024": 62031, "FY2023": 64893, "FY2022": 78708, "FY2021": 43059}
AQ_GROSS_TOTAL = {y: AQ_GROSS_S1[y] + AQ_GROSS_S2[y] + AQ_GROSS_S3[y] for y in YEARS}

AQ_ECL_S1 = {"FY2025": 998, "FY2024": 534, "FY2023": 504, "FY2022": 577, "FY2021": 559}
AQ_ECL_S2 = {"FY2025": 1230, "FY2024": 797, "FY2023": 749, "FY2022": 2151, "FY2021": 1455}
AQ_ECL_S3 = {"FY2025": 4851, "FY2024": 12554, "FY2023": 7647, "FY2022": 11236, "FY2021": 13275}
AQ_ECL_TOTAL = {y: AQ_ECL_S1[y] + AQ_ECL_S2[y] + AQ_ECL_S3[y] for y in YEARS}

AQ_NET_TOTAL = {y: AQ_GROSS_TOTAL[y] - AQ_ECL_TOTAL[y] for y in YEARS}
AQ_STAGE3_RATIO = {y: f"{AQ_GROSS_S3[y] / AQ_GROSS_TOTAL[y] * 100:.1f}%" for y in YEARS}
AQ_STAGE3_COVERAGE = {y: f"{AQ_ECL_S3[y] / AQ_GROSS_S3[y] * 100:.1f}%" for y in YEARS}
AQ_OVERALL_COVERAGE = {y: f"{AQ_ECL_TOTAL[y] / AQ_GROSS_TOTAL[y] * 100:.2f}%" for y in YEARS}

asset_quality_rows = [
    ("SECTION", "Financing arrangements, by IFRS 9 stage (gross exposure, incl. undrawn commitments)", {}),
    ("DATA", "Stage 1 (12-month ECL)", AQ_GROSS_S1),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", AQ_GROSS_S2),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired)", AQ_GROSS_S3),
    ("TOTAL", "Total gross exposure", AQ_GROSS_TOTAL),
    ("SECTION", "Expected credit loss (ECL) allowance, by stage", {}),
    ("DATA", "Stage 1 allowance", {y: -v for y, v in AQ_ECL_S1.items()}),
    ("DATA", "Stage 2 allowance", {y: -v for y, v in AQ_ECL_S2.items()}),
    ("DATA", "Stage 3 allowance", {y: -v for y, v in AQ_ECL_S3.items()}),
    ("TOTAL", "Total ECL allowance", {y: -v for y, v in AQ_ECL_TOTAL.items()}),
    ("TOTAL", "Net financing arrangements exposure", AQ_NET_TOTAL),
    ("SECTION", "Ratios", {}),
    ("DATA", "Stage 3 exposure ratio (Stage 3 / total gross exposure)", AQ_STAGE3_RATIO),
    ("DATA", "Stage 3 coverage ratio (Stage 3 allowance / Stage 3 exposure)", AQ_STAGE3_COVERAGE),
    ("DATA", "Overall coverage ratio (total allowance / total gross exposure)", AQ_OVERALL_COVERAGE),
]

bw.add_asset_quality_sheet(
    title="Bank of London and The Middle East plc — Asset Quality / Credit Risk Disclosures",
    subtitle="Financing arrangements by IFRS 9 stage, £'000s. BLME plc, Bank-solo basis.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - BLME plc's own 'Exposure by Stage' and 'Impairments of financial assets' notes (Financing "
        "arrangements only, £'000s):\n"
        f"FY2025/FY2024: BLME plc Financial Statements 31 December 2025, pp.51,53 - {FS2025_URL}\n"
        f"FY2023/FY2022: BLME plc Financial Statements 31 December 2023, pp.59,61 - {FS2023_URL}\n"
        f"FY2021: BLME plc Financial Statements 31 December 2021, p.59 - {FS2021_URL}\n\n"
        "Note: Stage 3 coverage fell sharply from 30.8% (FY2021) to 7.8% (FY2025) - genuine, driven by write-offs "
        "of specifically-provisioned exposures each year (e.g. £13.8m written off in FY2025 alone, per Note 12) "
        "reducing the Stage 3 allowance balance faster than the Stage 3 gross exposure balance - flagged here, "
        "not smoothed. 'Total gross exposure' figures are higher than the Balance Sheet's own Financing "
        "arrangements carrying value because they include undrawn credit facilities and off-balance-sheet "
        "commitments (per the Bank's own note) - not a reconciliation error.\n\n" + ENTITY_NOTE
    ),
    first_col_width=68,
    source_height=340,
    unit_suffix=" (£'000s)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else "", rows_data, sources_text,
                         note=note, first_col_width=52, source_height=200)


metric("CET1 Capital", "£m",
       [("Common Equity Tier 1 (CET1) capital", {"FY2025": 225.806, "FY2024": 227.639, "FY2023": 226.478, "FY2022": 227.212, "FY2021": 238.839})],
       p3_sources())

metric("CET1 Ratio", "% of RWA",
       [("CET1 ratio", {"FY2025": "19.29%", "FY2024": "17.80%", "FY2023": "16.87%", "FY2022": "16.51%", "FY2021": "18.18%"})],
       p3_sources())

metric("Tier 1 Capital", "£m",
       [("Tier 1 capital", {"FY2025": 225.806, "FY2024": 227.639, "FY2023": 226.478, "FY2022": 227.212, "FY2021": 238.839})],
       p3_sources(), note="CET1 = Tier 1 = Total Capital every year - BLME has no Additional Tier 1 or Tier 2 instruments.")

metric("Tier 1 Ratio", "% of RWA",
       [("Tier 1 ratio", {"FY2025": "19.29%", "FY2024": "17.80%", "FY2023": "16.87%", "FY2022": "16.51%", "FY2021": "18.18%"})],
       p3_sources())

metric("Total Capital", "£m",
       [("Total capital", {"FY2025": 225.806, "FY2024": 227.639, "FY2023": 226.478, "FY2022": 227.212, "FY2021": 238.839})],
       p3_sources())

metric("Total Capital Ratio", "% of RWA",
       [("Total capital ratio", {"FY2025": "19.29%", "FY2024": "17.80%", "FY2023": "16.87%", "FY2022": "16.51%", "FY2021": "18.18%"})],
       p3_sources())

metric("Total RWAs", "£m",
       [("Total risk-weighted exposure amount", {"FY2025": 1170.428, "FY2024": 1279.034, "FY2023": 1342.418, "FY2022": 1376.389, "FY2021": 1313.776})],
       p3_sources())

# ---------------------------------------------------------------
# RWA Breakdown: only the FY2021 Pillar III Disclosure (55 pages, using the
# older CRR own-funds/appendix format - see p3_sources() note) includes a
# category breakdown ("Table 8: Overview of Risk Weighted Assets"). The
# FY2022-2025 Pillar III Disclosures are all short (4-5 page) documents
# containing only the KM1 Key Metrics table (Total RWA as a single figure,
# no category split) - confirmed by reading each document in full, not
# assumed.
# ---------------------------------------------------------------
RWA_SOURCES = (
    "Sources - BLME plc's own Pillar III Disclosures:\n"
    f"FY2021: Pillar III Disclosure - 31 December 2021, Table 8 'Overview of Risk Weighted Assets', p.15 - "
    f"{P32021_URL}\n"
    f"FY2022-FY2025: Pillar III Disclosures for those years ({P32022_URL}, {P32023_URL}, {P32024_URL}, "
    f"{P32025_URL}) each checked in full (4-5 pages each) - none contains an RWA-by-category breakdown, only the "
    f"single Key metrics 'Total risk-weighted exposure amount' figure (already shown on the Total RWAs sheet).\n\n"
    + ENTITY_NOTE
)

rwa_breakdown_rows = [
    ("SECTION", "RWA by risk category (£m)", {}),
    ("DATA", "Credit risk (excluding counterparty credit risk)", {"FY2021": 1244.608, "FY2022": "Not publicly disclosed",
     "FY2023": "Not publicly disclosed", "FY2024": "Not publicly disclosed", "FY2025": "Not publicly disclosed"}),
    ("DATA", "Counterparty credit risk", {"FY2021": 0.509}),
    ("DATA", "Market risk", {"FY2021": 1.397}),
    ("DATA", "Operational risk", {"FY2021": 67.263}),
    ("TOTAL", "Total RWAs", {"FY2021": 1313.777, "FY2022": "Not publicly disclosed", "FY2023": "Not publicly disclosed",
     "FY2024": "Not publicly disclosed", "FY2025": "Not publicly disclosed"}),
]

bw.add_rwa_breakdown_sheet(
    title="Bank of London and The Middle East plc — RWA Breakdown",
    subtitle="FY2021 only (UK OV1-equivalent category split) - not disclosed at this granularity FY2022-25, see note below.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_SOURCES,
    first_col_width=58,
    source_height=280,
)

metric("Leverage Ratio", "%",
       [("Leverage ratio (excluding claims on central banks)", {"FY2025": "14.95%", "FY2024": "14.98%", "FY2023": "14.88%", "FY2022": "14.00%", "FY2021": "14.92%"})],
       p3_sources(),
       note="No basis break across the 5 years - all figures are on the 'excluding claims on central banks' basis, "
            "unlike several other banks in this project where FY2021 sits on an older methodology.")

metric("LCR", "%",
       [("Liquidity Coverage Ratio (12-month average)", {"FY2025": "308%", "FY2024": "310%", "FY2023": "288%", "FY2022": "352%", "FY2021": "315%"})],
       p3_sources())

metric("NSFR", "%",
       [("Net Stable Funding Ratio", {"FY2025": "121%", "FY2024": "125%", "FY2023": "144%", "FY2022": "143%"})],
       p3_sources(),
       note="FY2021 shown as N/A in the FY2022 report's own comparative column - UK NSFR requirement not yet in "
            "force for the FY2021 reporting date.")

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={"MREL Ratio": "MREL is not mentioned in any of the 5 Pillar III Disclosures reviewed (searched "
                             "directly, no hits any year) - consistent with a bank of this size not being its "
                             "own resolution entity under the Bank of England's MREL framework."},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 1484802, "FY2024": 1540358, "FY2023": 1497500, "FY2022": 1612376, "FY2021": 1548850}),
        ("Financing arrangements", {"FY2025": 1218128, "FY2024": 1151123, "FY2023": 1010255, "FY2022": 912937, "FY2021": 800318}),
        ("Due to customers", {"FY2025": 1197104, "FY2024": 1262682, "FY2023": 1248979, "FY2022": 1323870, "FY2021": 1031887}),
        ("Total equity", {"FY2025": 224068, "FY2024": 230834, "FY2023": 228232, "FY2022": 222915, "FY2021": 229717}),
    ],
    balance_sheet_unit="£'000s",
    income_statement_totals=[
        ("Net margin", {"FY2025": 38494, "FY2024": 38226, "FY2023": 35648, "FY2022": 33416, "FY2021": 29971}),
        ("Total operating expenses", {"FY2025": -49544, "FY2024": -44048, "FY2023": -40181, "FY2022": -40455, "FY2021": -28525}),
        ("Profit/(loss) for the year", {"FY2025": 1419, "FY2024": 6850, "FY2023": 5322, "FY2022": -6807, "FY2021": -4336}),
    ],
    income_statement_unit="£'000s",
    equity_changes_totals=[
        ("Opening equity (restated where applicable)", {"FY2025": 222072, "FY2024": 224268, "FY2023": 222915, "FY2022": 229717, "FY2021": 234261}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": 1376, "FY2024": 6566, "FY2023": 5317, "FY2022": -6800, "FY2021": -4544}),
        ("Other movements, net", {"FY2025": 620, "FY2024": 0, "FY2023": 0, "FY2022": -2, "FY2021": 0}),
        ("Closing equity", {"FY2025": 224068, "FY2024": 230834, "FY2023": 228232, "FY2022": 222915, "FY2021": 229717}),
    ],
    equity_changes_unit="£'000s",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities",
         {"FY2025": 24971, "FY2024": 38707, "FY2023": -7362, "FY2022": -3137, "FY2021": -146085}),
        ("Net cash from/(used in) investing activities",
         {"FY2025": 16028, "FY2024": -23922, "FY2023": -51152, "FY2022": 26767, "FY2021": 31053}),
        ("Net cash from/(used in) financing activities",
         {"FY2025": -577, "FY2024": -589, "FY2023": -719, "FY2022": -1123, "FY2021": -1086}),
        ("Cash and cash equivalents at end of period",
         {"FY2025": 130528, "FY2024": 90139, "FY2023": 76008, "FY2022": 135262, "FY2021": 112076}),
    ],
    cash_flow_unit="£'000s",
    ratios=[
        ("CET1 Ratio", {"FY2025": "19.29%", "FY2024": "17.80%", "FY2023": "16.87%", "FY2022": "16.51%", "FY2021": "18.18%"}),
        ("Tier 1 Ratio", {"FY2025": "19.29%", "FY2024": "17.80%", "FY2023": "16.87%", "FY2022": "16.51%", "FY2021": "18.18%"}),
        ("Total Capital Ratio", {"FY2025": "19.29%", "FY2024": "17.80%", "FY2023": "16.87%", "FY2022": "16.51%", "FY2021": "18.18%"}),
        ("Leverage Ratio", {"FY2025": "14.95%", "FY2024": "14.98%", "FY2023": "14.88%", "FY2022": "14.00%", "FY2021": "14.92%"}),
        ("LCR", {"FY2025": "308%", "FY2024": "310%", "FY2023": "288%", "FY2022": "352%", "FY2021": "315%"}),
        ("NSFR", {"FY2025": "121%", "FY2024": "125%", "FY2023": "144%", "FY2022": "143%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. NSFR blank for FY2021 (not yet in force). BLME plc solo basis "
         "throughout, not the wider BLME Holdings group.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BLME FINANCIALS.xlsx")
