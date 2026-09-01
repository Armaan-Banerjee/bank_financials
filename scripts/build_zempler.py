import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Zempler Bank Limited's first Pillar 3 report covered FY2022 (it only received
# its full banking licence in 2021), so the 5-year window here is FY2022-FY2026
# (year end 31 March each year) rather than the usual FY2021-FY2025 - there is
# no FY2021 Pillar 3 disclosure to pair with a cash flow column.
YEARS = ["FY2026", "FY2025", "FY2024", "FY2023", "FY2022"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2026_URL = "https://www.zemplerbank.com/media/yqkhclip/annual-report-2026-final.pdf"
AR2025_URL = "https://www.zemplerbank.com/media/5qxdezfu/annual-report-2025-final.pdf"
AR2023_URL = "https://www.zemplerbank.com/media/x5sbu2bc/annual-report-2023-010923.pdf"

P3_2026_URL = "https://www.zemplerbank.com/media/hfllow3d/pillar-3-fy2025-26-final.pdf"
P3_2024_URL = "https://www.zemplerbank.com/media/mszljzed/pillar-3-fy2023-24.pdf"
P3_2023_URL = "https://www.zemplerbank.com/media/f3vjwqov/pillar-3-fy2022-23.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Zempler Bank Limited (FRN 671140, company number 04947027) is a UK-domestic challenger bank - "
    "not a foreign subsidiary, so there was no reason to expect (and none was found) the FRS 101/102 cash-flow-"
    "statement exemption that blocked ICICI/PNBE/Citibank UK/State Bank of India UK. The company traded as "
    "'Cashplus Bank' under the legal name 'Advanced Payment Solutions Limited' through the FY2023 annual report; "
    "it was renamed 'Zempler Bank Limited' in July 2024 (FY2024/FY2025/FY2026 reports use the new name). Same "
    "company number throughout - this is a rename, not a different entity. FY2023's own annual report also notes "
    "that 'the Group no longer exists as at 31 March 2023' (a prior group restructuring), so the cash flow "
    "statement is presented on a Company-only basis for FY2023 and its FY2022 comparative, which this workbook "
    "uses for both years - there is no consolidated/Group-basis alternative available for FY2022-FY2023."
)

DATA_QUALITY_NOTE = (
    "DATA QUALITY NOTE - two apparent arithmetic errors were found in Zempler's own published, audited annual "
    "reports and are flagged here rather than silently smoothed over: "
    "(1) FY2025's own operating-activities line items (as printed) sum to £75,870k, not the £75,570k the source "
    "states as 'Net cash flow generated from operating activities' - a £300k gap in one of the individual "
    "components. The £75,570k TOTAL is used here (not the £75,870k component sum) because it is independently "
    "corroborated: operating + investing + financing (75,570 - 92,016 - 491) ties exactly to the source's own "
    "stated 'Net (decrease)/increase in cash and cash equivalent' of -£16,937k. The individual FY2025 operating "
    f"line items are transcribed exactly as printed in the source ({AR2025_URL}, p.64-66) despite this discrepancy. "
    "(2) FY2026's financing activities: the source prints 'Proceeds from issue of ordinary shares' £1,232k and "
    "'Interest paid' (£492k), which sum to +£740k, but the source's own 'Net cash used in financing activities' "
    "subtotal is printed as (£740k) - the opposite sign. +£740k is used here (not the printed -£740k) because it "
    "is the only figure consistent with both its own two components (1,232-492=740) and the overall cash bridge "
    f"(80,642 operating - 53,638 investing + 740 = 27,744, matching the source's own stated net increase in cash "
    f"exactly) - {AR2026_URL}, p.65-67."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Zempler Bank Limited's own (Company-only) cash flow statement, £'000:\n"
    f"FY2026: Zempler Bank Annual Report 2026, p.65-67 (Cash Flow Statement) - {AR2026_URL}\n"
    f"FY2025: Zempler Bank Annual Report 2025, p.64-66 (Cash Flow Statement) - {AR2025_URL}\n"
    f"FY2024 (restated): Zempler Bank Annual Report 2025, p.64-66 (Cash Flow Statement, restated comparative "
    f"column) - {AR2025_URL} - the restatement (see Note 38 in that report) reclassified some operating-section "
    "line items but did NOT change the operating/investing/financing TOTALS, which are identical to the "
    "originally-reported FY2024 figures.\n"
    f"FY2023: Annual Report and Financial Statements (Cashplus Bank / Advanced Payment Solutions Limited) for the "
    f"year ended 31 March 2023, p.56 (Cash Flow Statement) - {AR2023_URL}\n"
    f"FY2022 (restated to Company-only basis): Annual Report and Financial Statements for the year ended 31 March "
    f"2023, p.56 (Cash Flow Statement, comparative column) - {AR2023_URL}\n"
    "Blank cells indicate that year's report did not disclose that specific line item (e.g. prepayments/accrued "
    "income was only split out from FY2024 onward; tangible and intangible asset purchases were combined through "
    "FY2023 and split from FY2024). Section totals and cash/cash equivalents figures chain exactly year-to-year "
    "(each year's closing balance equals the next year's opening balance) across all 5 years.\n\n"
    + ENTITY_NOTE + "\n\n" + DATA_QUALITY_NOTE
)


P3_SOURCE_LINES = {
    "FY2026": f"FY2026: Zempler Bank Pillar 3 Disclosures for the year ended 31 March 2026, p.53-54 - {P3_2026_URL}",
    "FY2025": f"FY2025: Zempler Bank Pillar 3 Disclosures for the year ended 31 March 2026 (FY2025 comparative column), p.53-54 - {P3_2026_URL}",
    "FY2024": f"FY2024: Zempler Bank Pillar 3 Disclosures for the year ended 31 March 2024, p.51-52 - {P3_2024_URL}",
    "FY2023": f"FY2023: Pillar 3 Disclosures for the year ended 31 March 2023 (Cashplus Bank), p.40 - {P3_2023_URL}",
    "FY2022": f"FY2022: Pillar 3 Disclosures for the year ended 31 March 2023 (Cashplus Bank, FY2022 comparative column), p.40 - {P3_2023_URL}",
}

P3_SOURCES = (
    "Sources - Zempler Bank Limited's own entity-level Table 14: Key Metrics (KM1), £'000:\n"
    + "\n".join(P3_SOURCE_LINES[y] for y in YEARS)
)

bw = BankWorkbook(bank_name="Zempler Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="8A5A00")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) for the financial year before taxation", {"FY2026": 4225, "FY2025": 5217, "FY2024": 3291, "FY2023": 3243, "FY2022": -2103}),
    ("DATA", "Corporation tax paid", {"FY2023": 0, "FY2022": 0}),
    ("DATA", "Interest income from non-operating activities", {"FY2026": -12548, "FY2025": -9944, "FY2024": -5584, "FY2023": -1392, "FY2022": 289}),
    ("DATA", "Amortisation and depreciation / write offs", {"FY2026": 2991, "FY2025": 2987, "FY2024": 2326, "FY2023": 1427, "FY2022": 1754}),
    ("DATA", "Loss on disposal of tangible and intangible assets", {"FY2023": 619}),
    ("DATA", "Changes in fair value of derivatives", {"FY2025": 137, "FY2024": -137}),
    ("DATA", "Share based payment charge", {"FY2025": 887, "FY2024": 746, "FY2023": 898, "FY2022": 676}),
    ("DATA", "Amortisation of discount/premium for investment securities", {"FY2026": 196, "FY2025": 772, "FY2024": -2185, "FY2023": -1292, "FY2022": 196}),
    ("DATA", "Net increase/(decrease) in loans and advances to customers", {"FY2026": -9670, "FY2025": 2773, "FY2024": -5012, "FY2023": -814, "FY2022": -4593}),
    ("DATA", "Net decrease/(increase) in other assets", {"FY2026": 1281, "FY2025": 11992, "FY2024": -10054, "FY2023": 168, "FY2022": 1193}),
    ("DATA", "Net decrease in prepayments and accrued income", {"FY2026": 119, "FY2025": 303, "FY2024": 285}),
    ("DATA", "Net increase/(decrease) in customer deposits", {"FY2026": 88691, "FY2025": 82431, "FY2024": 32660, "FY2023": 58963, "FY2022": -7662}),
    ("DATA", "Net increase/(decrease) in other liabilities", {"FY2026": 5024, "FY2025": -20913, "FY2024": 20030, "FY2023": 2022, "FY2022": 1464}),
    ("DATA", "Net increase/(decrease) in deferred income", {"FY2026": 333, "FY2025": -772, "FY2024": 1843, "FY2023": -3205, "FY2022": 3071}),
    ("TOTAL", "Net cash flow generated from/(used in) operating activities", {"FY2026": 80642, "FY2025": 75570, "FY2024": 38209, "FY2023": 60637, "FY2022": -5715}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of tangible and intangible assets (combined, as reported)", {"FY2023": -3362, "FY2022": -6206}),
    ("DATA", "Purchase of intangible assets", {"FY2026": -593, "FY2025": -1712, "FY2024": -2753}),
    ("DATA", "Purchase of tangible fixed assets", {"FY2026": -61, "FY2025": -181, "FY2024": -623}),
    ("DATA", "Purchase of investment securities", {"FY2026": -287687, "FY2025": -316715, "FY2024": -242450, "FY2023": -134949, "FY2022": -1155196}),
    ("DATA", "Sale/maturity/disposal of investment securities", {"FY2026": 221859, "FY2025": 216929, "FY2024": 205326, "FY2023": 130196, "FY2022": 1460883}),
    ("DATA", "Interest received on investment securities", {"FY2026": 12844, "FY2025": 9663, "FY2024": 8262, "FY2023": 3148, "FY2022": -25}),
    ("TOTAL", "Net cash from/(used in) investing activities", {"FY2026": -53638, "FY2025": -92016, "FY2024": -32238, "FY2023": -4967, "FY2022": 299456}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Proceeds from issue of ordinary shares", {"FY2026": 1232, "FY2024": 14, "FY2022": 2261}),
    ("DATA", "Interest paid", {"FY2026": -492, "FY2025": -491, "FY2024": -493, "FY2023": -464, "FY2022": -478}),
    ("TOTAL", "Net cash from/(used in) financing activities", {"FY2026": 740, "FY2025": -491, "FY2024": -479, "FY2023": -464, "FY2022": 1783}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2026": 27744, "FY2025": -16937, "FY2024": 5492, "FY2023": 55206, "FY2022": 295524}),
    ("DATA", "Cash and cash equivalents at beginning of period", {"FY2026": 369088, "FY2025": 386025, "FY2024": 380533, "FY2023": 325327, "FY2022": 29803}),
    ("TOTAL", "Cash and cash equivalents at end of period", {"FY2026": 396832, "FY2025": 369088, "FY2024": 386025, "FY2023": 380533, "FY2022": 325327}),
]

bw.add_cash_flow_sheet(
    title="Zempler Bank Limited — Cash Flow Statement",
    subtitle="Company basis (see entity note), £'000. FY2026 financing subtotal and FY2025 operating subtotal are "
              "adjusted from the source's own printed figures - see DATA QUALITY NOTE at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=68,
    source_height=320,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, P3_SOURCES, note=note, first_col_width=44, source_height=140)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 capital", {"FY2026": 30728, "FY2025": 24728, "FY2024": 19877, "FY2023": 17672, "FY2022": 16115})],
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 ratio", {"FY2026": "21.74%", "FY2025": "19.32%", "FY2024": "15.57%", "FY2023": "18.17%", "FY2022": "14.79%"})],
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2026": 30728, "FY2025": 24728, "FY2024": 19877, "FY2023": 17672, "FY2022": 16115})],
    note="Equal to CET1 capital in every year shown - Zempler holds no Additional Tier 1 (AT1) instruments.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2026": "21.74%", "FY2025": "19.32%", "FY2024": "15.57%", "FY2023": "18.17%", "FY2022": "14.79%"})],
    note="Equal to the CET1 ratio in every year shown - Zempler holds no Additional Tier 1 (AT1) instruments.",
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2026": 31755, "FY2025": 26354, "FY2024": 22103, "FY2023": 20465, "FY2022": 18343})],
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2026": "22.47%", "FY2025": "20.59%", "FY2024": "17.31%", "FY2023": "21.04%", "FY2022": "16.83%"})],
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted assets", {"FY2026": 141317, "FY2025": 127987, "FY2024": 127670, "FY2023": 97282, "FY2022": 108982})],
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Leverage ratio total exposure measure", {"FY2026": 383737, "FY2025": 310657, "FY2024": 238194, "FY2023": 181803, "FY2022": 177724}),
        ("Leverage ratio (%)", {"FY2026": "7.99%", "FY2025": "7.96%", "FY2024": "8.34%", "FY2023": "9.72%", "FY2022": "9.07%"}),
    ],
    note="Zempler's Pillar 3 reports do not distinguish an 'excluding/including claims on central banks' basis - a "
         "single leverage ratio definition is used throughout.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA)", {"FY2026": 672041, "FY2025": 593599, "FY2024": 499336, "FY2023": 465257, "FY2022": 443570}),
        ("Total net cash outflows", {"FY2026": 60635, "FY2025": 68646, "FY2024": 55908, "FY2023": 53002, "FY2022": 45275}),
        ("Liquidity Coverage Ratio (%)", {"FY2026": "1108%", "FY2025": "865%", "FY2024": "893%", "FY2023": "878%", "FY2022": "980%"}),
    ],
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding", {"FY2026": 700696, "FY2025": 606213, "FY2024": 539411, "FY2023": 498682, "FY2022": 435465}),
        ("Total required stable funding", {"FY2026": 84273, "FY2025": 75978, "FY2024": 67565, "FY2023": 45238, "FY2022": 38105}),
        ("NSFR ratio (%)", {"FY2026": "831%", "FY2025": "798%", "FY2024": "798%", "FY2023": "1102%", "FY2022": "1143%"}),
    ],
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not applicable" for y in YEARS})],
    note="Per Zempler's FY2026 Pillar 3 Disclosures: 'MREL is set annually by the Bank of England on a case-by-case "
         "basis. In line with its preferred resolution strategy for Zempler, the Bank of England does not "
         "currently require any additional MREL to be held by the bank over and above its minimum Pillar 1 and "
         "Pillar 2A requirements.' No numeric MREL disclosure exists in any year's Pillar 3 report (no KM2 template "
         "is presented), consistent with this qualitative statement.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2026": 80642, "FY2025": 75570, "FY2024": 38209, "FY2023": 60637, "FY2022": -5715}),
        ("Net cash from/(used in) investing activities", {"FY2026": -53638, "FY2025": -92016, "FY2024": -32238, "FY2023": -4967, "FY2022": 299456}),
        ("Net cash from/(used in) financing activities", {"FY2026": 740, "FY2025": -491, "FY2024": -479, "FY2023": -464, "FY2022": 1783}),
        ("Cash and cash equivalents at end of period", {"FY2026": 396832, "FY2025": 369088, "FY2024": 386025, "FY2023": 380533, "FY2022": 325327}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2026": "21.74%", "FY2025": "19.32%", "FY2024": "15.57%", "FY2023": "18.17%", "FY2022": "14.79%"}),
        ("Tier 1 Ratio", {"FY2026": "21.74%", "FY2025": "19.32%", "FY2024": "15.57%", "FY2023": "18.17%", "FY2022": "14.79%"}),
        ("Total Capital Ratio", {"FY2026": "22.47%", "FY2025": "20.59%", "FY2024": "17.31%", "FY2023": "21.04%", "FY2022": "16.83%"}),
        ("Leverage Ratio", {"FY2026": "7.99%", "FY2025": "7.96%", "FY2024": "8.34%", "FY2023": "9.72%", "FY2022": "9.07%"}),
        ("LCR", {"FY2026": "1108%", "FY2025": "865%", "FY2024": "893%", "FY2023": "878%", "FY2022": "980%"}),
        ("NSFR", {"FY2026": "831%", "FY2025": "798%", "FY2024": "798%", "FY2023": "1102%", "FY2022": "1143%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. This workbook covers FY2022-FY2026 (not the usual FY2021-"
         "FY2025) since Zempler's first Pillar 3 disclosure covered FY2022 - it did not hold a full banking "
         "licence before 2021. See the Cash Flow Statement sheet's DATA QUALITY NOTE re: two apparent arithmetic "
         "errors found in the bank's own published FY2025/FY2026 annual reports.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/ZEMPLER FINANCIALS.xlsx")
