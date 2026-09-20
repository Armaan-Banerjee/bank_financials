import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://www.crownagentsbank.com/wp-content/uploads/2026/04/Crown-Agents-Bank-2025-Annual-Report.pdf"
AR2023_URL = "http://www.crownagentsbank.com/wp-content/uploads/2025/09/cab_fs_ye_2023_signed_3_april_2024_audited.pdf"
AR2022_URL = "http://www.crownagentsbank.com/wp-content/uploads/2025/09/cab_financial_statements_2022_signed_19_april_formatted_version.pdf"
AR2021_URL = "http://www.crownagentsbank.com/wp-content/uploads/2025/09/cab_2021_financial_statements_1_apr.pdf"

P3_2025_URL = "https://www.crownagentsbank.com/wp-content/uploads/2026/04/CAB-Pillar-3-Document-2025-FINAL.pdf"
P3_2024_URL = "http://www.crownagentsbank.com/wp-content/uploads/2025/09/cab_pillar_3_-_document_2024_post_bac.pdf"
P3_2023_URL = "http://www.crownagentsbank.com/wp-content/uploads/2025/09/2023_cab_pillar_3_disclosures_final.pdf"
P3_2022_URL = "http://www.crownagentsbank.com/wp-content/uploads/2025/09/cab_pillar_3_disclosures_2022_v3.pdf"

ENTITY_NOTE = (
    "Crown Agents Bank Limited (FRN 204456, company 02334687) is the PRA-regulated bank entity - "
    "distinct from its LSE-listed ultimate parent CAB Payments Holdings plc (which IPO'd in 2023 and "
    "has faced separate, unrelated corporate-control events - a withdrawn possible offer from StoneX "
    "and an unrecommended offer from Helios - neither of which affects this Bank entity's own figures "
    "below). All figures are the Bank's OWN entity-level disclosures (Companies House filing history "
    "and the Bank's own Pillar 3 documents), not the wider listed Group's consolidated figures, which "
    "are published separately under the \"CAB Payments Holdings plc\" name and are NOT used here.\n\n"
    "RESTATEMENTS: two genuine cross-vintage restatements were found in the cash flow statement. "
    "FY2022's own originally-published net cash used in operating activities was £(252,244)k; the "
    "FY2023 Annual Report's own comparative column restates this to £(236,806)k (a £15,438k "
    "difference), with no explanation located for the change. FY2021's own originally-published net "
    "cash generated from operating activities was £318,950k; the FY2022 Annual Report's own "
    "comparative column restates this to £313,819k (a £5,131k difference). Per project convention, "
    "each year's own originally-published figures are used throughout (not later restated "
    "comparatives).\n\n"
    "Two minor, unexplained cross-vintage cash-bridge gaps also exist and are left as genuinely "
    "reported rather than forced to reconcile: FY2021's own closing balance (£1,118,821k) does not "
    "match FY2022's own opening balance (£1,113,467k), a £5,354k gap; FY2023's own closing balance "
    "(£1,179,607k) does not exactly match FY2024's own opening balance (£1,181,046k), a £1,439k gap."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Crown Agents Bank Limited's own Statement of Cash Flows (Bank-solo, "
    "no subsidiaries consolidated):\n"
    f"FY2025/FY2024: Annual Report and Financial Statements 2025, p.56-57 & p.105-106 (Statement of "
    f"Cash Flows + Note 28 reconciliation) - {AR2025_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.59 (Statement of cash flows) - {AR2023_URL}\n"
    f"FY2022/FY2021 (own originally-published figures, not FY2023's or FY2022's restated comparatives): "
    f"Annual Report and Financial Statements 2022, p.41 (Statement of Cash Flows) - {AR2022_URL}; "
    f"Annual Report and Financial Statements 2021, p.38 (Cash Flow Statement) - {AR2021_URL}\n\n"
    + ENTITY_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - Crown Agents Bank Limited Pillar 3 basis (Bank-solo, UK KM1 Key Metrics table unless noted):\n"
        f"FY2025: Pillar 3 Disclosures - 31 December 2025, p.9 (UK KM1) - {P3_2025_URL}\n"
        f"FY2024: Pillar 3 Disclosures - 31 December 2024, p.9 (UK KM1) - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures - 31 December 2023, p.9 (UK KM1) - {P3_2023_URL}\n"
        f"FY2022: Pillar 3 Disclosures - 31 December 2022, p.9 (Summary of Key Ratios - pre-KM1-template "
        f"format) - {P3_2022_URL}, cross-checked against FY2023's own KM1 comparative column where available\n"
        f"FY2021: Pillar 3 Disclosures - 31 December 2021, p.7 (Summary of Key Ratios) and p.18 (Capital "
        f"Resources / RWA / Capital Ratios) - https://www.crownagentsbank.com/wp-content/uploads/2025/09/"
        f"cab_pillar_3_disclosures_2021.pdf\n"
        "FY2021 predates the UK's post-Brexit CRR/KM1 regulatory regime, which UK banks became subject to "
        "from 1 January 2022 (per the FY2022 document's own Introduction) - FY2021 figures may not be "
        "directly comparable to FY2022 onward on a like-for-like basis.\n"
        + extra
    )


bw = BankWorkbook(bank_name="Crown Agents Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="A9152C")

STATEMENTS_ENTITY_NOTE = (
    ENTITY_NOTE
    + "\n\nRESTATEMENT (Balance Sheet/Equity): FY2021's own originally-published Total Assets/Total "
    "equity (£1,311,970k/£75,204k) differ slightly from FY2022's own Annual Report's FY2021 comparative "
    "(£1,312,701k/£75,150k, a £731k/£54k gap) - the same restatement already documented on the Cash Flow "
    "Statement (Note 28). FY2021's own originally-published Profit for the financial year (£8,658k) "
    "likewise differs from FY2022's own comparative (£8,714k, a £56k gap). Per project convention, each "
    "year's own originally-published figures are used throughout, not later restated comparatives - this "
    "creates a genuine, documented (not force-reconciled) £54k discontinuity between the FY2021 and FY2022 "
    "columns of the Statement of Changes in Equity.\n\n"
    "PRESENTATION NOTE: FY2021's own Balance Sheet ('Balance Sheet') and Profit and Loss Account use "
    "different line-item structure and terminology than FY2022 onward's IFRS-style 'Statement of Financial "
    "Position'/'Statement of Profit or Loss' (e.g. FY2021 has no separate 'Loans and advances to customers', "
    "'Unsettled transactions', 'Right of use assets', or 'Current tax asset' lines - some of these may be "
    "folded into other lines that year, some genuinely didn't exist yet). FY2021's Profit and Loss Account "
    "also predates the Revenue/Total-income structure used FY2022 onward. FY2024's Investment in debt "
    "securities was reclassified from a single amortised-cost line into separate amortised-cost and FVOCI "
    "lines from FY2025 onward, following the FY2025 report's own presentation. Blank cells indicate that "
    "year's own report did not disclose that specific line at that granularity."
)

STATEMENTS_SOURCES = (
    "Sources - Crown Agents Bank Limited's own Balance Sheet / Statement of Financial Position, Profit and "
    "Loss Account / Statement of Profit or Loss, and Statement of Changes in Equity, transcribed from each "
    "year's own report (not a later year's comparative column):\n"
    f"FY2025/FY2024: Annual Report and Financial Statements 2025, pp.53-56 - {AR2025_URL}\n"
    f"FY2023 (and FY2022's own comparative used only for FY2022's balance sheet where FY2022's own report "
    f"is not more direct): Annual Report and Financial Statements 2023, pp.55-58 - {AR2023_URL}\n"
    f"FY2022 (own originally-published figures): Annual Report and Financial Statements 2022, pp.36-40 - "
    f"{AR2022_URL}\n"
    f"FY2021 (own originally-published figures, not FY2022's restated comparative): Annual Report and "
    f"Financial Statements 2021, pp.34-37 - {AR2021_URL}\n\n"
    + STATEMENTS_ENTITY_NOTE
)

ASSET_QUALITY_SOURCES = (
    "Sources - Crown Agents Bank Limited's own Credit Risk note (IFRS 9 staging), Bank-solo basis:\n"
    f"FY2025/FY2024: Annual Report and Financial Statements 2025, Note 31(v) 'Breakdown as a function of "
    f"staging', p.121-122 (on-balance-sheet maximum exposure per stage and total ECL) - {AR2025_URL}\n"
    f"FY2023/FY2022: Annual Report and Financial Statements 2023, Note 31(v), p.138-139 (total maximum "
    f"exposure per stage and total ECL, on- and off-balance-sheet combined) - {AR2023_URL}\n"
    "FY2021: no IFRS 9 staging/expected-credit-loss table was located in the FY2021 Annual Report (it "
    "predates the Bank's IFRS-style statement presentation adopted from FY2022 onward, and its own P&L "
    "shows a nominal 'Write-off of doubtful debts' rather than an ECL/staging disclosure) - confirmed "
    "absent by checking, not assumed; left blank rather than guessed.\n\n"
    + ENTITY_NOTE
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks",
     {"FY2025": 257867, "FY2024": 584679, "FY2023": 528396, "FY2022": 607358, "FY2021": 676492}),
    ("DATA", "Money market funds",
     {"FY2025": 218157, "FY2024": 488197, "FY2023": 518764, "FY2022": 209486, "FY2021": 336737}),
    ("DATA", "Loans and advances on demand to banks",
     {"FY2025": 127035, "FY2024": 184683, "FY2023": 132447, "FY2022": 89957, "FY2021": 105592}),
    ("DATA", "Other loans and advances to banks",
     {"FY2025": 274956, "FY2024": 180095, "FY2023": 137569, "FY2022": 91691, "FY2021": 74030}),
    ("DATA", "Loans and advances to customers / non-banks",
     {"FY2025": 21521, "FY2024": 32564, "FY2023": 8216, "FY2022": 4748}),
    ("DATA", "Investments in debt securities, at amortised cost",
     {"FY2025": 234790, "FY2024": 246021, "FY2023": 353028, "FY2022": 414061, "FY2021": 73249}),
    ("DATA", "Investment in debt securities, at fair value through OCI",
     {"FY2025": 442751}),
    ("DATA", "Investments in equity securities",
     {"FY2025": 679, "FY2024": 553, "FY2023": 495, "FY2022": 488, "FY2021": 341}),
    ("DATA", "Derivative financial assets",
     {"FY2025": 489, "FY2024": 4884, "FY2023": 3829, "FY2022": 6589, "FY2021": 1641}),
    ("DATA", "Unsettled transactions",
     {"FY2025": 8900, "FY2024": 10866, "FY2023": 8417, "FY2022": 12960}),
    ("DATA", "Investments in subsidiary undertakings",
     {"FY2025": 4476, "FY2024": 1899}),
    ("DATA", "Current tax asset",
     {"FY2025": 8839, "FY2024": 9386}),
    ("DATA", "Other assets",
     {"FY2025": 27071, "FY2024": 29352, "FY2023": 34653, "FY2022": 24022, "FY2021": 19902}),
    ("DATA", "Accrued income",
     {"FY2025": 2033, "FY2024": 925, "FY2023": 1217, "FY2022": 857}),
    ("DATA", "Prepayments and accrued income",
     {"FY2021": 3646}),
    ("DATA", "Property, plant and equipment / tangible fixed assets",
     {"FY2025": 2188, "FY2024": 2679, "FY2023": 1177, "FY2022": 1568, "FY2021": 2043}),
    ("DATA", "Right of use assets",
     {"FY2025": 14977, "FY2024": 16830, "FY2023": 689, "FY2022": 1134}),
    ("DATA", "Intangible assets",
     {"FY2025": 23840, "FY2024": 24398, "FY2023": 19084, "FY2022": 17523, "FY2021": 18297}),
    ("TOTAL", "Total assets",
     {"FY2025": 1670569, "FY2024": 1818011, "FY2023": 1747981, "FY2022": 1482442, "FY2021": 1311970}),

    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer accounts",
     {"FY2025": 1441097, "FY2024": 1589481, "FY2023": 1546632, "FY2022": 1310809, "FY2021": 1194682}),
    ("DATA", "Derivative financial liabilities",
     {"FY2025": 1384, "FY2024": 539, "FY2023": 9679, "FY2022": 4565, "FY2021": 7669}),
    ("DATA", "Unsettled transactions",
     {"FY2025": 20772, "FY2024": 35173, "FY2023": 20081, "FY2022": 25782}),
    ("DATA", "Other liabilities",
     {"FY2025": 6725, "FY2024": 12818, "FY2023": 18255, "FY2022": 11314, "FY2021": 26193}),
    ("DATA", "Accruals / accruals and deferred income",
     {"FY2025": 13529, "FY2024": 9160, "FY2023": 17315, "FY2022": 18368, "FY2021": 8222}),
    ("DATA", "Lease liabilities",
     {"FY2025": 18281, "FY2024": 17076, "FY2023": 884, "FY2022": 1281}),
    ("DATA", "Deferred tax liability",
     {"FY2025": 928, "FY2024": 1217, "FY2023": 695, "FY2022": 316}),
    ("DATA", "Provisions",
     {"FY2025": 2054, "FY2024": 1949, "FY2023": 236, "FY2022": 79}),
    ("TOTAL", "Total liabilities",
     {"FY2025": 1504770, "FY2024": 1667413, "FY2023": 1613777, "FY2022": 1372514, "FY2021": 1236766}),

    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital",
     {"FY2025": 41200, "FY2024": 41200, "FY2023": 41200, "FY2022": 41200, "FY2021": 41200}),
    ("DATA", "Retained earnings",
     {"FY2025": 124563, "FY2024": 109264, "FY2023": 92885, "FY2022": 68624, "FY2021": 34004}),
    ("DATA", "Investment revaluation reserve",
     {"FY2025": 207, "FY2024": 134, "FY2023": 119, "FY2022": 104}),
    ("DATA", "Debt securities revaluation reserve",
     {"FY2025": 73}),
    ("DATA", "Cash flow hedge reserve",
     {"FY2025": -244}),
    ("TOTAL", "Total equity / shareholders' funds",
     {"FY2025": 165799, "FY2024": 150598, "FY2023": 134204, "FY2022": 109928, "FY2021": 75204}),
    ("TOTAL", "Total liabilities and equity",
     {"FY2025": 1670569, "FY2024": 1818011, "FY2023": 1747981, "FY2022": 1482442, "FY2021": 1311970}),
]

bw.add_balance_sheet_sheet(
    title="Crown Agents Bank Limited — Balance Sheet",
    subtitle="Bank-solo basis, £'000. See source note at bottom (genuine restatement and presentation changes documented).",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=88,
    source_height=340,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income",
     {"FY2025": 55772, "FY2024": 58831, "FY2023": 52309, "FY2022": 17163, "FY2021": 3584}),
    ("DATA", "Interest expense",
     {"FY2025": -29770, "FY2024": -38403, "FY2023": -30854, "FY2022": -10398, "FY2021": -1376}),
    ("TOTAL", "Net interest income",
     {"FY2025": 26002, "FY2024": 20428, "FY2023": 21455, "FY2022": 6765, "FY2021": 2208}),
    ("DATA", "Gains on money market funds",
     {"FY2025": 14688, "FY2024": 16070, "FY2023": 11034, "FY2022": 3585}),
    ("DATA", "Net (loss)/gain on financial instruments at FVTPL",
     {"FY2025": -1616, "FY2024": -247, "FY2023": 1232, "FY2022": 1009}),
    ("DATA", "Fees and commission income",
     {"FY2025": 16429, "FY2024": 15835, "FY2023": 14647, "FY2022": 15831, "FY2021": 11755}),
    ("DATA", "Net foreign exchange gain",
     {"FY2025": 61965, "FY2024": 53797, "FY2023": 88742, "FY2022": 82682, "FY2021": 39133}),
    ("DATA", "Write-off of doubtful debts",
     {"FY2021": -38}),
    ("DATA", "Other operating income/(loss)",
     {"FY2025": 735, "FY2024": 616, "FY2023": 313, "FY2022": -484, "FY2021": 347}),
    ("TOTAL", "Total income / operating income",
     {"FY2025": 118203, "FY2024": 106499, "FY2023": 137423, "FY2022": 109388, "FY2021": 53405}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Operating expenses (recurring + non-recurring / before & after non-underlying items)",
     {"FY2025": -97050, "FY2024": -85931, "FY2023": -79472, "FY2022": -64357}),
    ("DATA", "Administrative expenses",
     {"FY2021": -37122}),
    ("DATA", "Amortisation",
     {"FY2021": -4775}),
    ("DATA", "Depreciation",
     {"FY2021": -836}),
    ("DATA", "Other finance costs",
     {"FY2025": -1339, "FY2024": -876}),
    ("DATA", "Impairment reversal/(loss) on financial assets at amortised cost",
     {"FY2025": 154, "FY2024": 377, "FY2023": -454, "FY2022": -329}),
    ("TOTAL", "Profit before taxation",
     {"FY2025": 19968, "FY2024": 20069, "FY2023": 57497, "FY2022": 44702, "FY2021": 10672}),
    ("DATA", "Tax expense",
     {"FY2025": -5459, "FY2024": -4678, "FY2023": -14708, "FY2022": -10444, "FY2021": -2014}),
    ("TOTAL", "Profit for the year",
     {"FY2025": 14509, "FY2024": 15391, "FY2023": 42789, "FY2022": 34258, "FY2021": 8658}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Movement in investment revaluation reserve (equity instruments at FVOCI)",
     {"FY2025": 98, "FY2024": 20, "FY2023": 27, "FY2022": 88}),
    ("DATA", "Cash flow hedge reserve movement",
     {"FY2025": -244}),
    ("DATA", "Movement in debt securities at fair value through OCI",
     {"FY2025": 73}),
    ("DATA", "Income tax relating to these items",
     {"FY2025": -25, "FY2024": -5, "FY2023": -12, "FY2022": -17}),
    ("TOTAL", "Other comprehensive income, net of tax",
     {"FY2025": -98, "FY2024": 15, "FY2023": 15, "FY2022": 71}),
    ("TOTAL", "Total comprehensive income for the year",
     {"FY2025": 14411, "FY2024": 15406, "FY2023": 42804, "FY2022": 34329, "FY2021": 8658}),
]

bw.add_income_statement_sheet(
    title="Crown Agents Bank Limited — Profit & Loss",
    subtitle="Bank-solo basis, £'000. See source note at bottom (genuine presentation changes documented).",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=88,
    source_height=340,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
equity_headers = ["Share capital", "Retained earnings", "Investment revaluation reserve",
                   "Debt securities revaluation reserve", "Cash flow hedge reserve", "Total"]
equity_rows = [
    ("TOTAL", "At 1 January 2021 (own report)", (41200, 25088, None, None, None, 66288)),
    ("DATA", "Profit for the financial year", (None, 8658, None, None, None, 8658)),
    ("DATA", "Share based payment expense", (None, 258, None, None, None, 258)),
    ("TOTAL", "At 31 December 2021", (41200, 34004, None, None, None, 75204)),

    ("TOTAL", "At 1 January 2022 (own report - see restatement note re: FY2021 close)",
     (41200, 33917, 33, None, None, 75150)),
    ("DATA", "Profit for the year", (None, 34258, None, None, None, 34258)),
    ("DATA", "Movement in investment revaluation reserve", (None, None, 88, None, None, 88)),
    ("DATA", "Income tax relating to these items", (None, None, -17, None, None, -17)),
    ("DATA", "Share based payment expense", (None, 449, None, None, None, 449)),
    ("TOTAL", "At 31 December 2022", (41200, 68624, 104, None, None, 109928)),

    ("TOTAL", "At 1 January 2023", (41200, 68624, 104, None, None, 109928)),
    ("DATA", "Profit for the year", (None, 42789, None, None, None, 42789)),
    ("DATA", "Movement in investment revaluation reserve", (None, None, 27, None, None, 27)),
    ("DATA", "Income tax relating to these items", (None, None, -12, None, None, -12)),
    ("DATA", "Share based payment expense", (None, 972, None, None, None, 972)),
    ("DATA", "Dividends declared", (None, -19500, None, None, None, -19500)),
    ("TOTAL", "At 31 December 2023", (41200, 92885, 119, None, None, 134204)),

    ("TOTAL", "At 1 January 2024", (41200, 92885, 119, None, None, 134204)),
    ("DATA", "Profit for the year", (None, 15391, None, None, None, 15391)),
    ("DATA", "Movement in investment revaluation reserve", (None, None, 20, None, None, 20)),
    ("DATA", "Income tax relating to these items", (None, None, -5, None, None, -5)),
    ("DATA", "Share based payment expense", (None, 988, None, None, None, 988)),
    ("DATA", "Dividends declared", (None, 0, None, None, None, 0)),
    ("TOTAL", "At 31 December 2024", (41200, 109264, 134, None, None, 150598)),

    ("TOTAL", "At 1 January 2025", (41200, 109264, 134, None, None, 150598)),
    ("DATA", "Profit for the year", (None, 14509, None, None, None, 14509)),
    ("DATA", "Movement in investment revaluation reserve", (None, None, 98, None, None, 98)),
    ("DATA", "Cash flow hedge reserve", (None, None, None, None, -244, -244)),
    ("DATA", "Movement in debt securities at fair value through OCI", (None, None, None, 73, None, 73)),
    ("DATA", "Income tax relating to these items", (None, None, -25, None, None, -25)),
    ("DATA", "Share-based payment expense", (None, 620, None, None, None, 620)),
    ("DATA", "Deferred tax on share-based payment expense", (None, 170, None, None, None, 170)),
    ("TOTAL", "At 31 December 2025", (41200, 124563, 207, 73, -244, 165799)),
]

bw.add_equity_changes_sheet(
    title="Crown Agents Bank Limited — Statement of Changes in Equity",
    subtitle="Bank-solo basis, £'000, chronological (oldest to newest). See source note at bottom - a genuine "
              "£54k restatement gap exists between the FY2021 and FY2022 columns (documented, not plugged).",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=58,
    source_height=340,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Cash (outflow)/inflow from operating activities (before tax/lease interest)",
     {"FY2025": -614029, "FY2024": 99180, "FY2023": 308912, "FY2022": -242642, "FY2021": 321062}),
    ("DATA", "Tax paid",
     {"FY2025": -4687, "FY2024": -11766, "FY2023": -14084, "FY2022": -9583, "FY2021": -2112}),
    ("DATA", "Payments for interest on lease liabilities",
     {"FY2025": 0, "FY2024": -33, "FY2023": -65, "FY2022": -19}),
    ("TOTAL", "Net cash (used in)/generated from operating activities",
     {"FY2025": -618716, "FY2024": 87381, "FY2023": 294763, "FY2022": -252244, "FY2021": 318950}),

    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment",
     {"FY2025": -108, "FY2024": -2334, "FY2023": -416, "FY2022": -346, "FY2021": -302}),
    ("DATA", "Purchase/capitalisation of intangible assets",
     {"FY2025": -6778, "FY2024": -12141, "FY2023": -6642, "FY2022": -4375, "FY2021": -4313}),
    ("DATA", "Sale/(purchase) of equity investments/shares/exchange traded funds",
     {"FY2024": -53, "FY2021": -228}),
    ("DATA", "Purchase of investments in subsidiary undertakings",
     {"FY2025": -2577, "FY2024": -1269, "FY2023": -543}),
    ("TOTAL", "Net cash used in investing activities",
     {"FY2025": -9463, "FY2024": -15797, "FY2023": -7601, "FY2022": -4721, "FY2021": -4843}),

    ("SECTION", "Financing activities", {}),
    ("DATA", "Repayment of principal portion of lease liability", {"FY2024": -257, "FY2023": -462, "FY2022": -233}),
    ("DATA", "Reduction in overdraft", {}),
    ("TOTAL", "Net cash (used in)/generated from financing activities",
     {"FY2025": 0, "FY2024": -257, "FY2023": -462, "FY2022": -233, "FY2021": 0}),

    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents",
     {"FY2025": -628179, "FY2024": 71327, "FY2023": 286700, "FY2022": -257198, "FY2021": 314107}),
    ("DATA", "Cash and cash equivalents at the beginning of the year",
     {"FY2025": 1257559, "FY2024": 1181046, "FY2023": 906801, "FY2022": 1113467, "FY2021": 803412}),
    ("DATA", "Effect of exchange rate changes on cash and cash equivalents",
     {"FY2025": -26321, "FY2024": 5186, "FY2023": -13894, "FY2022": 50531, "FY2021": 1302}),
    ("TOTAL", "Cash and cash equivalents at the end of the year",
     {"FY2025": 603059, "FY2024": 1257559, "FY2023": 1179607, "FY2022": 906801, "FY2021": 1118821}),
]

bw.add_cash_flow_sheet(
    title="Crown Agents Bank Limited — Statement of Cash Flows",
    subtitle="Bank-solo basis, £'000. See source note at bottom (genuine restatements and cross-vintage gaps documented).",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=340,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Maximum credit exposure by IFRS 9 stage (on- and off-balance sheet)", {}),
    ("DATA", "Stage 1 exposure",
     {"FY2025": 1400040, "FY2024": 1242511, "FY2023": 1203697, "FY2022": 1290241}),
    ("DATA", "Stage 2 exposure",
     {"FY2025": 6097, "FY2024": 61435, "FY2023": 25033, "FY2022": 1163}),
    ("DATA", "Stage 3 exposure",
     {"FY2025": 94, "FY2024": 94, "FY2023": 184, "FY2022": 0}),
    ("TOTAL", "Total maximum credit exposure",
     {"FY2025": 1406231, "FY2024": 1304040, "FY2023": 1228914, "FY2022": 1291404}),
    ("DATA", "Total expected credit loss (ECL) allowance",
     {"FY2025": 324, "FY2024": 475, "FY2023": 854, "FY2022": 400}),
    ("SECTION", "Derived ratios", {}),
    ("DATA", "Stage 3 / total exposure ratio",
     {"FY2025": "0.007%", "FY2024": "0.007%", "FY2023": "0.015%", "FY2022": "0.000%"}),
    ("DATA", "Total ECL / total exposure (overall coverage)",
     {"FY2025": "0.023%", "FY2024": "0.036%", "FY2023": "0.069%", "FY2022": "0.031%"}),
]

bw.add_asset_quality_sheet(
    title="Crown Agents Bank Limited — Asset Quality",
    subtitle="Bank-solo basis, £'000 (ratios as calculated). This is a treasury/correspondent-banking-led "
              "balance sheet with minimal customer lending - the credit risk note covers all financial "
              "asset classes (cash, interbank placements, debt securities, loans and advances), not "
              "customer loans alone. See source note at bottom.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=58,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None, source_height=170):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=48, source_height=source_height)


CET1_CAPITAL = {"FY2025": 141776, "FY2024": 126265, "FY2023": 115358, "FY2022": 89871, "FY2021": 56906}
RWA = {"FY2025": 619414, "FY2024": 627016, "FY2023": 436220, "FY2022": 269258, "FY2021": 186856}
CET1_RATIO = {"FY2025": "22.9%", "FY2024": "20.1%", "FY2023": "26.4%", "FY2022": "33.4%", "FY2021": "30.5%"}
LEVERAGE_RATIO = {"FY2025": "9.5%", "FY2024": "7.4%", "FY2023": "7.3%", "FY2022": "6.9%", "FY2021": "5.0%"}
LCR = {"FY2025": "134.7%", "FY2024": "136.4%", "FY2023": "149.7%", "FY2022": "143.2%", "FY2021": "132%"}
NSFR = {"FY2025": "130.0%", "FY2024": "130.9%", "FY2023": "159.4%", "FY2022": "206.6%", "FY2021": "211%"}

RWA_NOTE = (
    "FY2021's RWA (£186,856k) is directly stated in the Bank's own 2021 Pillar 3 disclosure, p.18. "
    "All other years are disclosed to the £'000 in their own KM1 tables."
)
CET1_CAPITAL_NOTE = (
    "FY2021's CET1/Tier1/Total Capital (£56,906k) is directly disclosed as Total Common Equity Tier 1 "
    "Capital / Total Capital Resources in the Bank's own 2021 Pillar 3 disclosure, p.18. Its own 2021 "
    "capital-ratio table gives 30.5%. All other years (FY2022 onward) are directly disclosed in the respective year's own KM1 table "
    "(FY2022's calculated cross-check: £269,258k x 33.4% = £89,933k vs the directly-disclosed £89,871k - "
    "matches closely, confirming the calculation method is sound)."
)
LIQUIDITY_BASIS_NOTE = (
    "LIQUIDITY RATIO BASIS CAVEAT: the FY2022 Pillar 3 document's own \"Summary of Key Ratios\" table shows "
    "LCR 158% and NSFR 213% for FY2022, and LCR 132%/NSFR 211% for FY2021 - but the FY2023 document's own "
    "KM1 table, which explicitly states its LCR is a \"12 month average\" and NSFR a \"4 quarter average\", "
    "gives a materially different Dec-2022 comparative (LCR 143.2%, NSFR 206.6%). This is the same "
    "spot-vs-average LCR/NSFR basis trap seen elsewhere in this project (e.g. ALRAYAN Bank, Bank of Africa "
    "UK) - the FY2022 document's own summary table doesn't state its methodology explicitly, but the gap "
    "strongly suggests a different (likely point-in-time/spot) basis. Used the KM1/average-basis figure for "
    "FY2022 (143.2%/206.6%) for consistency with every other bank in this project; the FY2022 document's own "
    "158%/213% figures are documented here for reference. FY2021 has no KM1-basis alternative available "
    "(predates the KM1 template rollout, per the FY2022 document's own note that UK banks became subject "
    "to the current regime from 1 January 2022) - FY2021's 132%/211% are used as the only figures found, "
    "flagged as likely not directly comparable to FY2022-onward's KM1-basis figures."
)

KM1_SOURCES = (
    "Sources - Crown Agents Bank Limited's own published 'UK KM1 - Key Metrics' template, Bank-solo basis, "
    "reproduced whole in the Bank's own row order, row numbers, labels and precision. Amounts in £'000, "
    "ratios exactly as printed:\n"
    f"FY2025: Pillar 3 Disclosures - 31 December 2025, p.9 ('UK KM1 - Key Metrics', 31 Dec 2025 column) - {P3_2025_URL}\n"
    f"FY2024: Pillar 3 Disclosures - 31 December 2024, p.9 (31 Dec 2024 column) - {P3_2024_URL}\n"
    f"FY2023: Pillar 3 Disclosures - 31 December 2023, p.8 (31 Dec 2023 column) - {P3_2023_URL}\n"
    f"FY2022: THE FY2022 EDITION PRINTS NO KM1 TABLE AT ALL - it carries only a short bespoke 'Summary of Key "
    f"Ratios' table (p.9: seven rows - RWA, CET1 ratio, Total capital ratio, Leverage ratio, HQLA, LCR, NSFR - "
    f"with no row numbers, no SREP rows, no buffer rows and no HQLA/cash-flow build-up), which is NOT the "
    f"template. The FY2022 column here is therefore taken from the FY2023 edition's own '31 Dec 2022' "
    f"COMPARATIVE COLUMN (p.8) - {P3_2023_URL}. The FY2022 edition itself is at {P3_2022_URL}.\n"
    "FY2021: BLANK, and this is a genuine absence rather than a gap in our searching. The FY2021 edition "
    "likewise prints only the short 'Summary of Key Ratios' table (p.7), the FY2020 edition contains no "
    "occurrence of 'KM1' at all, and no later edition anywhere carries a 31 December 2021 comparative column "
    "(the FY2023 edition's oldest column is 31 Dec 2022). FY2021 also predates the UK CRR/KM1 regime, which "
    "took effect from 1 January 2022 per the FY2022 document's own Introduction.\n\n"
    "ROW-NUMBERING DRIFT BETWEEN EDITIONS (reproduced, not normalised): the FY2023 edition numbers the three "
    "liquidity build-up rows '16a', 'UK 16b' and 'UK 16', while the FY2024 and FY2025 editions number the same "
    "three rows 'UK 16a', 'UK 16b' and '16'. The row numbers shown on this sheet are the FY2025 edition's; the "
    "FY2023 edition's own variants are recorded here rather than silently harmonised.\n"
    "Rows UK 8a, UK 9a, 10, UK 10a and 14a-14e do not appear in any Crown Agents edition. Every edition states "
    "in a footnote that 'Rows 14a-14e have been removed as only LREQ firms are required to disclose this "
    "information' - a formal exclusion, not a data gap. The remaining absent rows are simply not printed.\n"
    "Each edition's LCR is a 12-month average and its NSFR a 4-quarter average, per each document's own "
    "footnotes. UK 7a moves from 4.4% (FY2022/FY2023) to 2.5% (FY2024/FY2025) - a real change in the Bank's "
    "SREP requirement, reproduced as printed.\n"
    "CROSS-EDITION DIVERGENCE ON THE FY2022 COLUMN, documented rather than reconciled: the Bank's HY-2023 "
    "interim Pillar 3 (30 June 2023) also prints a 31 Dec 2022 comparative, and it disagrees with the FY2023 "
    "annual edition on three rows - leverage ratio 7.0% vs 6.9%, NSFR 215% vs 206.6%, and 'CET1 available after "
    "meeting the total SREP own funds requirements' 26.4% vs 22.0%. The FY2023 annual edition's figures are "
    "used here; the interim's are recorded for reference. The interim is internally inconsistent on that "
    "column, which is why the annual edition is preferred rather than merely chosen: the interim prints "
    "available stable funding of £191m against required stable funding of £92m, a ratio of 207.6%, yet prints "
    "215% on its own NSFR row, whereas the FY2023 annual edition's 191,001 / 92,449 does give the 206.6% it "
    "prints. The two editions also differ on row 13, total exposure measure: £1,292m in the interim against "
    "£1,298,776 thousand in the annual edition. No figure here is derived from those components - they are "
    "cited only to show which edition is self-consistent.\n"
    "INDEPENDENT CONFIRMATION OF THE FY2024 COLUMN: Crown Agents has published semi-annually since H1 2023, "
    "and the HY-2025 interim Pillar 3 (30 June 2025, p.2) prints its own 31 December 2024 comparative column. "
    "It reproduces the FY2024 annual edition exactly on every row transcribed here - CET1/Tier 1/Total capital "
    "126,265; RWA 627,016; rows 5/6/7 all 20.1%; UK 7a 2.5%; UK 7d 12.4%; buffers 2.5%, 0.4% and 2.9%; "
    "UK 11a 15.2%; row 12 13.2%; row 13 1,695,874; row 14 7.4%; row 15 1,111,440; UK 16a 989,420; UK 16b "
    "174,615; row 16 814,805; row 17 136.4%. Two independent editions agreeing row-for-row is the strongest "
    "check available on a transcribed column.\n\n"
    "LATEST-EDITION CHECK (2026-09-17): crownagentsbank.com's own WordPress media index was enumerated in full. "
    "The newest Crown Agents Bank Limited Pillar 3 is the 31 December 2025 edition used here (uploaded "
    "2026-04-02) and the newest Bank Annual Report is the 2025 one (uploaded 2026-04-01), so this workbook is "
    "current. NOTE THE ENTITY TRAP: the same website hosts a PARALLEL Pillar 3 series for the listed parent, "
    "CAB Payments Holdings plc ('cab_payments_*', 'cab_ph_*', 'CAB-PH-*' filenames), including a half-year "
    "2026 edition that is newer than anything above. Those are the GROUP's consolidated disclosures and are "
    "deliberately NOT used anywhere in this workbook, which is Bank-solo throughout.\n\n"
    + ENTITY_NOTE
)

km1_rows = [
    ("SECTION", "Available own funds (amounts)", {}),
    ("DATA", "1  Common Equity Tier 1 (CET1) capital (£'000)",
     {"FY2025": 141776, "FY2024": 126265, "FY2023": 115358, "FY2022": 89871}),
    ("DATA", "2  Tier 1 capital (£'000)",
     {"FY2025": 141776, "FY2024": 126265, "FY2023": 115358, "FY2022": 89871}),
    ("DATA", "3  Total capital (£'000)",
     {"FY2025": 141776, "FY2024": 126265, "FY2023": 115358, "FY2022": 89871}),
    ("SECTION", "Risk-weighted exposure amounts", {}),
    ("DATA", "4  Total risk-weighted exposure amount (£'000)",
     {"FY2025": 619414, "FY2024": 627016, "FY2023": 436220, "FY2022": 269258}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "5  Common Equity Tier 1 ratio (%)",
     {"FY2025": "22.9%", "FY2024": "20.1%", "FY2023": "26.4%", "FY2022": "33.4%"}),
    ("DATA", "6  Tier 1 ratio (%)",
     {"FY2025": "22.9%", "FY2024": "20.1%", "FY2023": "26.4%", "FY2022": "33.4%"}),
    ("DATA", "7  Total capital ratio (%)",
     {"FY2025": "22.9%", "FY2024": "20.1%", "FY2023": "26.4%", "FY2022": "33.4%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "UK 7a  Additional CET1 SREP requirements (%)",
     {"FY2025": "2.5%", "FY2024": "2.5%", "FY2023": "4.4%", "FY2022": "4.4%"}),
    ("DATA", "UK 7d  Total SREP own funds requirements (%)",
     {"FY2025": "12.4%", "FY2024": "12.4%", "FY2023": "12.4%", "FY2022": "12.4%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "8  Capital conservation buffer (%)",
     {"FY2025": "2.5%", "FY2024": "2.5%", "FY2023": "2.5%", "FY2022": "2.5%"}),
    ("DATA", "9  Institution specific countercyclical capital buffer (%)",
     {"FY2025": "0.5%", "FY2024": "0.4%", "FY2023": "0.2%", "FY2022": "0.2%"}),
    ("DATA", "11  Combined buffer requirement (%)",
     {"FY2025": "3.0%", "FY2024": "2.9%", "FY2023": "2.7%", "FY2022": "2.7%"}),
    ("DATA", "UK 11a  Overall capital requirements (%)",
     {"FY2025": "15.3%", "FY2024": "15.2%", "FY2023": "15.1%", "FY2022": "15.0%"}),
    ("DATA", "12  CET1 available after meeting the total SREP own funds requirements (%)",
     {"FY2025": "15.9%", "FY2024": "13.2%", "FY2023": "19.5%", "FY2022": "22.0%"}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "13  Total exposure measure excluding claims on central banks (£'000)",
     {"FY2025": 1493971, "FY2024": 1695874, "FY2023": 1584105, "FY2022": 1298776}),
    ("DATA", "14  Leverage ratio excluding claims on central banks (%)",
     {"FY2025": "9.5%", "FY2024": "7.4%", "FY2023": "7.3%", "FY2022": "6.9%"}),
    ("SECTION", "Liquidity Coverage Ratio (12-month average, per each edition's own footnote)", {}),
    ("DATA", "15  Total high-quality liquid assets (HQLA) (Weighted value - average) (£'000)",
     {"FY2025": 1126209, "FY2024": 1111440, "FY2023": 1114654, "FY2022": 1065155}),
    ("DATA", "UK 16a  Cash outflows - Total weighted value (£'000)  [numbered '16a' in the FY2023 edition]",
     {"FY2025": 1050882, "FY2024": 989420, "FY2023": 877292, "FY2022": 863205}),
    ("DATA", "UK 16b  Cash inflows - Total weighted value (£'000)",
     {"FY2025": 214871, "FY2024": 174615, "FY2023": 132613, "FY2022": 119636}),
    ("DATA", "16  Total net cash outflows (adjusted value) (£'000)  [numbered 'UK 16' in the FY2023 edition]",
     {"FY2025": 836012, "FY2024": 814805, "FY2023": 744678, "FY2022": 743569}),
    ("DATA", "17  Liquidity coverage ratio (%)",
     {"FY2025": "134.7%", "FY2024": "136.4%", "FY2023": "149.7%", "FY2022": "143.2%"}),
    ("SECTION", "Net Stable Funding Ratio (4-quarter average, per each edition's own footnote)", {}),
    ("DATA", "18  Total available stable funding (£'000)",
     {"FY2025": 212942, "FY2024": 210991, "FY2023": 214380, "FY2022": 191001}),
    ("DATA", "19  Total required stable funding (£'000)",
     {"FY2025": 163739, "FY2024": 161171, "FY2023": 134472, "FY2022": 92449}),
    ("DATA", "20  NSFR ratio (%)",
     {"FY2025": "130.0%", "FY2024": "130.9%", "FY2023": "159.4%", "FY2022": "206.6%"}),
]

bw.add_km1_sheet(
    title="Crown Agents Bank Limited — KM1 Key Metrics",
    subtitle="The Bank's own published 'UK KM1 - Key Metrics' template (Bank-solo), reproduced whole in its own "
             "row order, row numbers, labels and precision. Amounts in £'000, ratios as printed. FY2025-FY2023 "
             "are each from that year's OWN edition; FY2022 is the FY2023 edition's comparative column, because "
             "the FY2022 edition prints no KM1 table at all. FY2021 is blank - no edition anywhere publishes a "
             "KM1 for it. See source note.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=72,
    source_height=300,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", CET1_CAPITAL)],
       p3_sources(), note=CET1_CAPITAL_NOTE)
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 (CET1) ratio", CET1_RATIO)], p3_sources())
metric("Tier 1 Capital", "£'000 (= CET1 Capital; no AT1 instruments)", [("Tier 1 capital", CET1_CAPITAL)],
       p3_sources(), note=CET1_CAPITAL_NOTE)
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", CET1_RATIO)], p3_sources())
metric("Total Capital", "£'000 (= CET1 Capital; no Tier 2 instruments)", [("Total capital", CET1_CAPITAL)],
       p3_sources(), note=CET1_CAPITAL_NOTE)
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", CET1_RATIO)], p3_sources())
metric("Total RWAs", "£'000", [("Total risk-weighted exposure amount", RWA)], p3_sources(), note=RWA_NOTE)

RWA_BREAKDOWN_NOTE = (
    "RE-VERIFIED 2026-09-12 (independent fresh check, not just re-reading this note): all 4 previously-blank "
    "years' Pillar 3 Disclosures were re-downloaded and read in full - each DOES contain a genuine category-"
    "level RWA breakdown, previously missed.\n\n"
    "FY2021/FY2022 use an older 'Risk Weighted Assets - Pillar 1' table format (both years' figures, £'000): "
    "FY2021 - Pillar 3 Disclosures 2021, p.18 - Credit Risk 106,588; Counterparty Risk (Derivatives) 1,720; "
    "Total Credit Risk Weighted Assets 108,308; Settlement Risk and CVA 1,047; Market Risk 5,110; Operational "
    "Risk 72,390; Total Risk Weighted Assets 186,856. FY2022 - Pillar 3 Disclosures 2022 (v3), p.5 - Credit "
    "Risk 136,308; Counterparty Risk (Derivatives) 4,207; Total Credit Risk Weighted Assets 140,515; "
    "Settlement Risk and CVA 975; Market Risk 5,240; Operational Risk 122,529; Total Risk Weighted Assets "
    "269,258 (ties exactly to the Total RWAs sheet's FY2022 figure).\n\n"
    "FY2023-FY2025 use the newer 'UK OV1 - Overview of risk weighted exposure amounts' template (own-year "
    "column each time, £'000): FY2023 - Pillar 3 Disclosures 2023, p.21 - Credit risk (excl. CCR) 234,740; "
    "Counterparty credit risk (CCR) 8,971 (of which CVA 1,194); Market risk 3,299; Operational risk 187,635; "
    "Amounts below thresholds for deduction (memo, not in Total) 1,575; Total 434,645. FY2024 - Pillar 3 "
    "Disclosures 2024, p.20-21 - Credit risk (excl. CCR) 396,867; CCR 6,299 (of which CVA 1,432); Market risk "
    "3,577; Operational risk 220,273; Total 627,016 (ties exactly to the Total RWAs sheet's FY2024 figure). "
    "FY2025 - Pillar 3 Disclosures 2025, p.20-21 - Credit risk (excl. CCR) 379,430; CCR 4,705 (of which CVA "
    "1,568); Market risk 9,497; Operational risk 225,782; Total 619,414 (ties exactly to the Total RWAs "
    "sheet's FY2025 figure).\n\n"
    "GENUINE UNRESOLVED DISCREPANCY, documented not forced: FY2023's own OV1 table Total (434,645) does not "
    "match the SAME FY2023 document's own KM1 Key Metrics table Total risk-weighted exposure amount (436,220, "
    "the figure used on the Total RWAs sheet) - the difference (1,575) exactly equals the OV1 table's own "
    "memo-only 'Amounts below thresholds for deduction' row, which is excluded from the OV1 Total but "
    "apparently included in the KM1 Total. Both figures are shown exactly as each table states them."
)
bw.add_rwa_breakdown_sheet(
    title="Crown Agents Bank Limited — RWA Breakdown",
    subtitle="FY2021/FY2022: Pillar 1 category format. FY2023-FY2025: UK OV1 template (different category "
              "granularity - see source note). All £'000.",
    rows=[
        ("SECTION", "FY2021-FY2022 (Pillar 1 category format, as originally disclosed)", {}),
        ("DATA", "Credit risk", {"FY2021": 106588, "FY2022": 136308}),
        ("DATA", "Counterparty risk (derivatives)", {"FY2021": 1720, "FY2022": 4207}),
        ("TOTAL", "Total credit risk weighted assets", {"FY2021": 108308, "FY2022": 140515}),
        ("DATA", "Settlement risk and CVA", {"FY2021": 1047, "FY2022": 975}),
        ("DATA", "Market risk", {"FY2021": 5110, "FY2022": 5240}),
        ("DATA", "Operational risk", {"FY2021": 72390, "FY2022": 122529}),
        ("TOTAL", "Total risk weighted assets (Pillar 1 format)", {"FY2021": 186856, "FY2022": 269258}),
        ("SECTION", "FY2023-FY2025 (UK OV1 template, as disclosed from FY2023 onward)", {}),
        ("DATA", "Credit risk (excluding CCR)", {"FY2023": 234740, "FY2024": 396867, "FY2025": 379430}),
        ("DATA", "Counterparty credit risk (CCR)", {"FY2023": 8971, "FY2024": 6299, "FY2025": 4705}),
        ("DATA", "  of which: credit valuation adjustment (CVA)", {"FY2023": 1194, "FY2024": 1432, "FY2025": 1568}),
        ("DATA", "Market risk (position, FX and commodities)", {"FY2023": 3299, "FY2024": 3577, "FY2025": 9497}),
        ("DATA", "Operational risk", {"FY2023": 187635, "FY2024": 220273, "FY2025": 225782}),
        ("DATA", "Amounts below thresholds for deduction (memo, excluded from Total)", {"FY2023": 1575}),
        ("TOTAL", "Total (UK OV1 format)", {"FY2023": 434645, "FY2024": 627016, "FY2025": 619414}),
    ],
    sources_text=p3_sources() + "\n\n" + RWA_BREAKDOWN_NOTE,
    first_col_width=54,
    source_height=420,
)

metric(
    "Leverage Ratio", "%, excluding claims on central banks",
    [("Leverage ratio", LEVERAGE_RATIO)],
    p3_sources(),
    note="NO BASIS BREAK AT FY2021/FY2022 - CHECKED AND CLEARED 2026-09-16, recorded so this series is not "
         "'corrected' later on a false positive. Many UK banks' leverage series break across that boundary "
         "because the UK Leverage Ratio Framework excluded claims on central banks from the exposure measure from "
         "1 January 2022; this Bank's does not, because it was already excluding them well before then. Its own "
         "FY2021 Pillar 3 (p.19, Table LR Sum) carries the line 'Less: central bank exposures (160,863)' for 2021 "
         "and '(125,844)' for 2020, footnoted 'Exposures to central banks subject to a maximum of deposits in the "
         "same currency is excluded from the leverage ratio exposure measure', and cites PS21/17 'UK leverage "
         "ratio: treatment of claims on central banks (October 2017)'. The FY2022 document carries the identical "
         "line at (189,334). So FY2021 and FY2022 are on the SAME excluding basis and the 5.0% -> 6.9% rise is "
         "real: Tier 1 capital rose 59% (£56,595k to £89,871k) while the exposure measure rose only 13% "
         "(£1,144,181k to £1,298,041k), and the Bank attributes it in its own words to 'current year profit being "
         "included in the Capital resources'. Note also that the exclusion is CAPPED at the level of the Bank's "
         "deposits in the same currency, so it is much smaller than the gross BoE balance - at 31 December 2022 "
         "the Bank's BoE reserve account held £608,298k but only £189,334k was excluded. The general "
         "FY2021-comparability hedge in the source citation below is about the wider CRR/KM1 regime change and "
         "does NOT apply to the leverage ratio, which is like-for-like across all five years.",
    source_height=260,
)
metric("LCR", "%", [("Liquidity Coverage Ratio", LCR)], p3_sources(), note=LIQUIDITY_BASIS_NOTE)
metric("NSFR", "%", [("Net Stable Funding Ratio", NSFR)], p3_sources(), note=LIQUIDITY_BASIS_NOTE)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources(),
    # GA-020 (2026-09-19): the FY2021-FY2025 Pillar 3 editions and the FY2021/22/23/25
    # Annual Reports were re-downloaded and full-text searched: no MREL figure,
    # requirement or exemption statement ('eligible liabilities' appears only as
    # the title of the CCA own-funds-instruments template, FY2023-FY2025).
    statements={"MREL Ratio": {y: (f"Not published – Crown Agents Bank {y} Pillar 3 (full text searched 2026-09-19) "
                                   "contains no MREL figure, requirement or exemption statement") for y in YEARS}},
    per_note={"MREL Ratio": "Not publicly disclosed - no MREL figure or exemption statement found in any "
                             "of the 5 years' Pillar 3 documents reviewed."},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 1670569, "FY2024": 1818011, "FY2023": 1747981, "FY2022": 1482442, "FY2021": 1311970}),
        ("Loans and advances to customers / non-banks", {"FY2025": 21521, "FY2024": 32564, "FY2023": 8216, "FY2022": 4748}),
        ("Customer accounts", {"FY2025": 1441097, "FY2024": 1589481, "FY2023": 1546632, "FY2022": 1310809, "FY2021": 1194682}),
        ("Total equity / shareholders' funds", {"FY2025": 165799, "FY2024": 150598, "FY2023": 134204, "FY2022": 109928, "FY2021": 75204}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total income / operating income", {"FY2025": 118203, "FY2024": 106499, "FY2023": 137423, "FY2022": 109388, "FY2021": 53405}),
        ("Operating expenses", {"FY2025": -97050, "FY2024": -85931, "FY2023": -79472, "FY2022": -64357, "FY2021": -42733}),
        ("Profit for the year", {"FY2025": 14509, "FY2024": 15391, "FY2023": 42789, "FY2022": 34258, "FY2021": 8658}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 150598, "FY2024": 134204, "FY2023": 109928, "FY2022": 75150, "FY2021": 66288}),
        ("Total comprehensive income for the year", {"FY2025": 14411, "FY2024": 15406, "FY2023": 42804, "FY2022": 34329, "FY2021": 8658}),
        ("Other equity movements, net", {"FY2025": 790, "FY2024": 988, "FY2023": -18528, "FY2022": 449, "FY2021": 258}),
        ("Closing equity", {"FY2025": 165799, "FY2024": 150598, "FY2023": 134204, "FY2022": 109928, "FY2021": 75204}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash (used in)/generated from operating activities",
         {"FY2025": -618716, "FY2024": 87381, "FY2023": 294763, "FY2022": -252244, "FY2021": 318950}),
        ("Net cash used in investing activities",
         {"FY2025": -9463, "FY2024": -15797, "FY2023": -7601, "FY2022": -4721, "FY2021": -4843}),
        ("Net cash (used in)/generated from financing activities",
         {"FY2025": 0, "FY2024": -257, "FY2023": -462, "FY2022": -233, "FY2021": 0}),
        ("Cash and cash equivalents at end of year",
         {"FY2025": 603059, "FY2024": 1257559, "FY2023": 1179607, "FY2022": 906801, "FY2021": 1118821}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Total Capital Ratio", CET1_RATIO),
        ("Leverage Ratio", LEVERAGE_RATIO),
        ("LCR", LCR),
        ("NSFR", NSFR),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. LCR/NSFR shown here use the KM1/average basis "
         "from FY2022 onward - see the LCR/NSFR sheets' own CAVEAT note for FY2021/FY2022 basis ambiguity.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/CROWN AGENTS BANK FINANCIALS.xlsx")
