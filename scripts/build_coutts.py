import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/00036695/filing-history"
AR2025_URL = CH_BASE + "/MzUyMTA2MDcwMGFkaXF6a2N4/document?format=pdf&download=0"  # FY2025 accounts (FY2025+FY2024)
AR2023_URL = CH_BASE + "/MzQyMDgzOTQ5OWFkaXF6a2N4/document?format=pdf&download=0"  # FY2023 accounts (FY2023+FY2022)
AR2022_URL = CH_BASE + "/MzM4NTMwNzEyMGFkaXF6a2N4/document?format=pdf&download=0"  # FY2022 accounts (FY2022+FY2021)

ENTITY_NOTE = (
    "Coutts & Company (company 00036695, FRN 122287) is a wholly-owned subsidiary of NatWest Group plc, "
    "part of the ring-fenced NatWest Holdings (NWH) Group sub-group. All figures are Coutts & Company's own "
    "entity-level financial statements/disclosures, not the wider NatWest Group. A private unlimited company - "
    "voluntarily files full audited accounts at Companies House despite the unlimited-company form (which "
    "would otherwise exempt it from public filing), same as C. Hoare & Co. elsewhere in this project.\n\n"
    "BASIS CHANGE: the FY2022 Annual Report states its financial statements 'are prepared on a standalone "
    "basis for Coutts. Previously these were prepared on a consolidated basis for Coutts and its "
    "subsidiaries.' The FY2021 figures used here are as shown in the FY2022 report's own comparative column "
    "(the only source available for FY2021) - it isn't confirmed whether that comparative was itself restated "
    "onto the new standalone basis or retains the original consolidated FY2021 basis. Flagged, not resolved.\n\n"
    "In September 2022 Coutts acquired the 'Adam & Company' private-banking business from The Royal Bank of "
    "Scotland plc (a Part VII-style transfer) - RBS plc is a separate entity already built in this project; "
    "that acquisition is the source-side counterpart of this project's earlier RBS plc entity-identity finding."
)

CASH_FLOW_SOURCES = (
    "Sources - Coutts & Company's own Cash Flow Statement, from its audited Companies House filings:\n"
    f"FY2025/FY2024: Annual Report and Accounts 2025, p.56 - {AR2025_URL}\n"
    f"FY2023/FY2022 (summary presentation): Annual Report and Accounts 2023, p.53 - {AR2023_URL}\n"
    f"FY2022/FY2021 (detailed presentation, used for the itemized operating-activities breakdown and as the "
    f"source for FY2021): Annual Report and Accounts 2022, p.56 - {AR2022_URL}\n\n"
    "FY2021/FY2022 use a more detailed operating-activities presentation (a 'Net cash flows from trading "
    "activities' subtotal, then an itemized 'Changes in operating assets and liabilities' breakdown) than "
    "FY2023-FY2025's simpler 3-line 'Adjustments for' presentation - both feed the same-labelled 'Changes in "
    "operating assets and liabilities' total line; FY2023-FY2025 state it as a single figure with no "
    "breakdown. Full opening-to-closing cash chain reconciles exactly across all 5 years, cross-checked "
    "against each year's appearance as the following year's comparative in every case.\n\n" + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - Coutts & Company's own 'Risk and capital management' section, Companies House filings:\n"
        f"FY2025/FY2024: Annual Report and Accounts 2025, p.30 - {AR2025_URL}\n"
        f"FY2023/FY2022 (capital): Annual Report and Accounts 2023, p.30 - {AR2023_URL}\n"
        f"FY2022/FY2021 (capital): Annual Report and Accounts 2022, p.34 - {AR2022_URL}\n\n"
        "LCR/NSFR/MREL are NOT disclosed at Coutts's own entity level in any year - the FY2025 report states "
        "explicitly: 'Disclosures relating to these metrics... are completed at UK DoLSub level and published "
        "in the... NatWest Holdings Group Annual Report and Accounts. Under the UK DoLSub waiver NWB Plc, RBS "
        "plc and Coutts are permitted to manage liquidity on a consolidated sub-group basis rather than "
        "individually at the entity level.' Only the regulatory minimum requirement (100%/100%) is stated, "
        "never an achieved value - this matches the RBS plc build's precedent elsewhere in this project "
        "(RBS plc + NatWest Bank plc + Coutts share one DoLSub liquidity disclosure). MREL is mentioned only "
        "as a defined concept, with no ratio ever stated for Coutts specifically.\n\n" + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="Coutts & Company", years=YEARS, year_label=YEAR_LABEL, header_color="8444FC")

STATEMENTS_SOURCES = (
    "Sources - Coutts & Company's own Statement of Comprehensive Income / Balance Sheet / Statement of Changes "
    "in Equity, from its audited Companies House filings:\n"
    f"FY2025/FY2024: Annual Report and Accounts 2025, pp.53-55 - {AR2025_URL}\n"
    f"FY2023/FY2022: Annual Report and Accounts 2023, pp.50-52 - {AR2023_URL}\n"
    f"FY2022/FY2021 (used for the FY2021 column - the only source available for FY2021): Annual Report and "
    f"Accounts 2022, pp.53-55 - {AR2022_URL}\n\n"
    "All figures reconcile exactly across all 5 years - every year's own closing Owners' equity ties to the "
    "next year's opening balance and to that year's own Balance Sheet Total equity figure, with no plug row "
    "needed anywhere in the chain. FY2022's own comparative figures (as republished in the FY2023 report) "
    "match FY2022's own originally-published figures (from the FY2022 report) exactly in every case checked - "
    "no restatement found. FY2023 Called-up share capital is nil ('-') in the source, consistent with earlier "
    "years' static £41m balance - flagged as a likely OCR/transcription artifact in the source scan rather "
    "than a genuine change, since Paid-in equity/Capital contribution reserve continuity around FY2023 shows "
    "no other sign of a share capital event; not corrected, shown as reported.\n\n" + ENTITY_NOTE
)

ASSET_QUALITY_SOURCES = (
    "Sources - Coutts & Company's own Note 8 'Loan impairment provisions', Companies House filings:\n"
    f"FY2025/FY2024: Annual Report and Accounts 2025, p.69 - {AR2025_URL}\n"
    f"FY2023/FY2022: Annual Report and Accounts 2023, p.65 - {AR2023_URL}\n"
    f"FY2022/FY2021 (used for the FY2021 column): Annual Report and Accounts 2022, p.68 - {AR2022_URL}\n\n"
    "'Inter-Group' is loans/placements with holding companies and fellow subsidiaries (dominant on this "
    "entity's balance sheet - see Amount due from holding companies and fellow subsidiaries on the Balance "
    "Sheet) - classified Stage 1 by the Bank's own convention and shown as its own row here, not blended into "
    "the third-party Stage 1/2/3 split. FY2022's own comparative figures (as republished in the FY2023 report) "
    "match FY2022's own originally-published figures exactly - no restatement found. The derived 'Stage 3 / "
    "gross third-party loans' ratio below excludes Inter-Group from the denominator, since inter-group "
    "placements carry negligible credit risk and would otherwise dilute the third-party asset-quality "
    "signal.\n\n" + ENTITY_NOTE
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - Coutts & Company's own 'Risk and capital management' section (Capital, RWAs and leverage "
    "table), Companies House filings:\n"
    f"FY2025/FY2024: Annual Report and Accounts 2025, p.30 - {AR2025_URL}\n"
    f"FY2023/FY2022: Annual Report and Accounts 2023, p.30 - {AR2023_URL}\n"
    f"FY2022/FY2021 (used for the FY2021 column): Annual Report and Accounts 2022, p.34 - {AR2022_URL}\n\n"
    "Every year's Total RWAs figure here ties exactly to the existing Total RWAs sheet; FY2022's own "
    "comparative figures (as republished in the FY2023 report) match FY2022's own originally-published figures "
    "exactly - no restatement found.\n\n" + ENTITY_NOTE
)

# ---------------------------------------------------------------
# Balance Sheet
# ---------------------------------------------------------------
bw.add_balance_sheet_sheet(
    title="Coutts & Company — Balance Sheet",
    subtitle="Entity-level basis, £m. See source note at bottom.",
    rows=[
        ("SECTION", "Assets", {}),
        ("DATA", "Cash and balances at central banks", {"FY2025": 3, "FY2024": 3, "FY2023": 3, "FY2022": 3, "FY2021": 3}),
        ("DATA", "Loans to banks - amortised cost", {"FY2025": 29, "FY2024": 22, "FY2023": 98, "FY2022": 92, "FY2021": 321}),
        ("DATA", "Loans to customers - amortised cost", {"FY2025": 18642, "FY2024": 18034, "FY2023": 18333, "FY2022": 18934, "FY2021": 17388}),
        ("DATA", "Amount due from holding companies and fellow subsidiaries", {"FY2025": 42546, "FY2024": 44307, "FY2023": 36623, "FY2022": 34681, "FY2021": 28682}),
        ("DATA", "Derivatives", {"FY2025": 11, "FY2024": 17, "FY2023": 23, "FY2022": 37, "FY2021": 14}),
        ("DATA", "Investment in group undertakings", {"FY2025": 110, "FY2024": 110, "FY2023": 110, "FY2022": 110, "FY2021": 110}),
        ("DATA", "Other assets", {"FY2025": 354, "FY2024": 367, "FY2023": 383, "FY2022": 413, "FY2021": 397}),
        ("TOTAL", "Total assets", {"FY2025": 61695, "FY2024": 62860, "FY2023": 55573, "FY2022": 54270, "FY2021": 46915}),
        ("SECTION", "Liabilities", {}),
        ("DATA", "Bank deposits", {"FY2025": 0, "FY2024": 2, "FY2022": 0, "FY2021": 2}),
        ("DATA", "Customer deposits", {"FY2025": 42642, "FY2024": 42318, "FY2023": 37549, "FY2022": 41057, "FY2021": 36971}),
        ("DATA", "Amount due to holding companies and fellow subsidiaries", {"FY2025": 17306, "FY2024": 18868, "FY2023": 16243, "FY2022": 11349, "FY2021": 8291}),
        ("DATA", "Derivatives", {"FY2025": 12, "FY2024": 17, "FY2023": 20, "FY2022": 34, "FY2021": 12}),
        ("DATA", "Other liabilities", {"FY2025": 191, "FY2024": 158, "FY2023": 143, "FY2022": 230, "FY2021": 118}),
        ("TOTAL", "Total liabilities", {"FY2025": 60151, "FY2024": 61363, "FY2023": 53955, "FY2022": 52670, "FY2021": 45394}),
        ("SECTION", "Equity", {}),
        ("TOTAL", "Owners' equity", {"FY2025": 1544, "FY2024": 1497, "FY2023": 1618, "FY2022": 1600, "FY2021": 1521}),
        ("TOTAL", "Total liabilities and equity", {"FY2025": 61695, "FY2024": 62860, "FY2023": 55573, "FY2022": 54270, "FY2021": 46915}),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=260,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
bw.add_income_statement_sheet(
    title="Coutts & Company — Statement of Comprehensive Income",
    subtitle="Entity-level basis, £m. See source note at bottom.",
    rows=[
        ("SECTION", "Income", {}),
        ("DATA", "Interest receivable", {"FY2025": 2404, "FY2024": 2450, "FY2023": 1861, "FY2022": 934, "FY2021": 486}),
        ("DATA", "Interest payable", {"FY2025": -1729, "FY2024": -1839, "FY2023": -1160, "FY2022": -225, "FY2021": -72}),
        ("TOTAL", "Net interest income", {"FY2025": 675, "FY2024": 611, "FY2023": 701, "FY2022": 709, "FY2021": 414}),
        ("DATA", "Fees and commissions receivable", {"FY2025": 266, "FY2024": 229, "FY2023": 197, "FY2022": 207, "FY2021": 208}),
        ("DATA", "Fees and commissions payable", {"FY2025": -21, "FY2024": -20, "FY2023": -22, "FY2022": -25, "FY2021": -29}),
        ("DATA", "Other operating income", {"FY2025": 70, "FY2024": 62, "FY2023": 83, "FY2022": 31, "FY2021": 39}),
        ("TOTAL", "Non-interest income", {"FY2025": 315, "FY2024": 271, "FY2023": 258, "FY2022": 213, "FY2021": 218}),
        ("TOTAL", "Total income", {"FY2025": 990, "FY2024": 882, "FY2023": 959, "FY2022": 922, "FY2021": 632}),
        ("DATA", "Staff costs", {"FY2025": -235, "FY2024": -213, "FY2023": -196, "FY2022": -176, "FY2021": -150}),
        ("DATA", "Premises and equipment", {"FY2025": -19, "FY2024": -13, "FY2023": -12, "FY2022": -20, "FY2021": -36}),
        ("DATA", "Depreciation and amortisation", {"FY2025": -34, "FY2024": -34, "FY2023": -38, "FY2022": -21, "FY2021": -19}),
        ("DATA", "Other administrative expenses", {"FY2025": -351, "FY2024": -379, "FY2023": -329, "FY2022": -316, "FY2021": -243}),
        ("TOTAL", "Operating expenses", {"FY2025": -639, "FY2024": -639, "FY2023": -575, "FY2022": -533, "FY2021": -448}),
        ("TOTAL", "Profit before impairments", {"FY2025": 351, "FY2024": 243, "FY2023": 384, "FY2022": 389, "FY2021": 184}),
        ("DATA", "Impairment (losses)/releases", {"FY2025": -5, "FY2024": 19, "FY2023": -3, "FY2022": -31, "FY2021": 57}),
        ("TOTAL", "Operating profit before tax", {"FY2025": 346, "FY2024": 262, "FY2023": 381, "FY2022": 358, "FY2021": 241}),
        ("DATA", "Tax charge", {"FY2025": -87, "FY2024": -64, "FY2023": -87, "FY2022": -111, "FY2021": -60}),
        ("TOTAL", "Profit for the year", {"FY2025": 259, "FY2024": 198, "FY2023": 294, "FY2022": 247, "FY2021": 181}),
        ("SECTION", "Other comprehensive income", {}),
        ("DATA", "Cash flow hedges", {"FY2025": 1, "FY2024": -3, "FY2023": 0, "FY2022": 1, "FY2021": 1}),
        ("DATA", "Tax", {"FY2025": 0, "FY2024": 1, "FY2023": 0, "FY2022": -1, "FY2021": 0}),
        ("TOTAL", "Other comprehensive income/(losses) after tax", {"FY2025": 1, "FY2024": -2, "FY2023": 0, "FY2022": 0, "FY2021": 1}),
        ("TOTAL", "Total comprehensive income for the year, net of tax", {"FY2025": 260, "FY2024": 196, "FY2023": 294, "FY2022": 247, "FY2021": 182}),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=260,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity
# ---------------------------------------------------------------
equity_headers = ["Called-up share capital", "Paid-in equity", "Cash flow hedging reserve", "Capital contribution reserve", "Retained earnings", "Total"]
equity_rows = [
    ("TOTAL", "At 1 January 2021", (41, 200, 0, 382, 833, 1456)),
    ("DATA", "Profit for the year (FY2021)", (None, None, None, None, 181, 181)),
    ("DATA", "Cash flow hedges: amount recognised in equity (FY2021)", (None, None, 1, None, None, 1)),
    ("DATA", "Paid-in equity dividends paid (FY2021)", (None, None, None, None, -12, -12)),
    ("DATA", "Ordinary dividends paid (FY2021)", (None, None, None, None, -105, -105)),
    ("TOTAL", "At 31 December 2021", (41, 200, 1, 382, 897, 1521)),
    ("DATA", "Profit for the year (FY2022)", (None, None, None, None, 247, 247)),
    ("DATA", "Paid-in equity redeemed (FY2022)", (None, -165, None, None, None, -165)),
    ("DATA", "Paid-in equity issued (FY2022)", (None, 240, None, None, None, 240)),
    ("DATA", "Cash flow hedges: amount recognised in equity (FY2022)", (None, None, 4, None, None, 4)),
    ("DATA", "Cash flow hedges: amount transferred from equity to earnings (FY2022)", (None, None, -3, None, None, -3)),
    ("DATA", "Cash flow hedges: tax (FY2022)", (None, None, -1, None, None, -1)),
    ("DATA", "Paid-in equity dividends paid (FY2022)", (None, None, None, None, -16, -16)),
    ("DATA", "Ordinary dividends paid (FY2022)", (None, None, None, None, -225, -225)),
    ("DATA", "Redemption of paid-in equity, gross (FY2022)", (None, None, None, None, -2, -2)),
    ("TOTAL", "At 31 December 2022", (41, 275, 1, 382, 901, 1600)),
    ("DATA", "Profit for the year (FY2023)", (None, None, None, None, 294, 294)),
    ("DATA", "Paid-in equity redeemed (FY2023)", (None, -35, None, None, None, -35)),
    ("DATA", "Cash flow hedges: amount recognised in equity (FY2023)", (None, None, 1, None, None, 1)),
    ("DATA", "Cash flow hedges: amount transferred from equity to earnings (FY2023)", (None, None, -1, None, None, -1)),
    ("DATA", "Paid-in equity dividends paid (FY2023)", (None, None, None, None, -31, -31)),
    ("DATA", "Ordinary dividends paid (FY2023)", (None, None, None, None, -210, -210)),
    ("TOTAL", "At 31 December 2023", (41, 240, 1, 382, 954, 1618)),
    ("DATA", "Profit for the year (FY2024)", (None, None, None, None, 198, 198)),
    ("DATA", "Cash flow hedges: amount recognised in equity (FY2024)", (None, None, -6, None, None, -6)),
    ("DATA", "Cash flow hedges: reclassification of OCI to P&L (FY2024)", (None, None, 3, None, None, 3)),
    ("DATA", "Cash flow hedges: tax (FY2024)", (None, None, 1, None, None, 1)),
    ("DATA", "Paid-in equity dividends paid (FY2024)", (None, None, None, None, -28, -28)),
    ("DATA", "Ordinary dividends paid (FY2024)", (None, None, None, None, -289, -289)),
    ("TOTAL", "At 31 December 2024", (41, 240, -1, 382, 835, 1497)),
    ("DATA", "Profit for the year (FY2025)", (None, None, None, None, 259, 259)),
    ("DATA", "Cash flow hedges: reclassification of OCI to P&L (FY2025)", (None, None, 1, None, None, 1)),
    ("DATA", "Paid-in equity dividends paid (FY2025)", (None, None, None, None, -26, -26)),
    ("DATA", "Ordinary dividends paid (FY2025)", (None, None, None, None, -187, -187)),
    ("TOTAL", "At 31 December 2025", (41, 240, 0, 382, 881, 1544)),
]
bw.add_equity_changes_sheet(
    title="Coutts & Company — Statement of Changes in Equity",
    subtitle="Entity-level basis, £m, chronological (oldest to newest). See source note at bottom.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=62,
    source_height=260,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Operating profit before tax", {"FY2025": 346, "FY2024": 262, "FY2023": 381, "FY2022": 358, "FY2021": 241}),
    ("DATA", "Non-cash and other items (FY2023-FY2025 summary presentation)", {"FY2025": 81, "FY2024": 39, "FY2023": 61}),
    ("DATA", "Depreciation and amortisation (FY2021-FY2022 detailed presentation)", {"FY2022": 21, "FY2021": 19}),
    ("DATA", "Impairment losses/(releases) (FY2021-FY2022 detailed presentation)", {"FY2022": 31, "FY2021": -57}),
    ("DATA", "Other non-cash items (FY2021-FY2022 detailed presentation)", {"FY2022": 8, "FY2021": 3}),
    ("DATA", "Provision releases (FY2021-FY2022 detailed presentation)", {"FY2022": -1, "FY2021": -3}),
    ("DATA", "Elimination of foreign exchange differences (FY2021-FY2022 detailed presentation)", {"FY2022": -11, "FY2021": 30}),
    ("DATA", "Interest payable on debt securities in issue and subordinated liabilities (FY2021-FY2022 detailed presentation)", {"FY2022": 23, "FY2021": 12}),
    ("DATA", "Dividends receivable from subsidiaries (FY2021-FY2022 detailed presentation)", {"FY2022": -8, "FY2021": -15}),
    ("TOTAL", "Net cash flows from trading activities (FY2021-FY2022 subtotal; no equivalent line FY2023-FY2025)", {"FY2022": 421, "FY2021": 230}),
    ("DATA", "(Increase)/decrease in derivative assets", {"FY2022": -18, "FY2021": 15}),
    ("DATA", "Decrease in loans to banks", {"FY2022": 5, "FY2021": 49}),
    ("DATA", "Increase in loans to customers", {"FY2022": -944, "FY2021": -1449}),
    ("DATA", "Decrease in amounts due from holding companies and fellow subsidiaries", {"FY2022": 2234, "FY2021": 9513}),
    ("DATA", "Increase in other assets", {"FY2022": -4, "FY2021": -2}),
    ("DATA", "Decrease in bank deposits", {"FY2022": -2, "FY2021": -2}),
    ("DATA", "Increase in customer deposits", {"FY2022": 1847, "FY2021": 6829}),
    ("DATA", "Increase in amounts due to holding companies and fellow subsidiaries", {"FY2022": 2680, "FY2021": 1360}),
    ("DATA", "Increase/(decrease) in derivative liabilities", {"FY2022": 22, "FY2021": -16}),
    ("DATA", "Increase in other liabilities", {"FY2022": 1, "FY2021": 5}),
    ("TOTAL", "Changes in operating assets and liabilities", {"FY2025": -1841, "FY2024": 7767, "FY2023": 2095, "FY2022": 5821, "FY2021": 16302}),
    ("DATA", "Income taxes paid", {"FY2025": -89, "FY2024": -55, "FY2023": -192, "FY2022": 0, "FY2021": -71}),
    ("TOTAL", "Net cash flows from operating activities", {"FY2025": -1503, "FY2024": 8013, "FY2023": 2345, "FY2022": 6242, "FY2021": 16461}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -2, "FY2024": -9, "FY2023": -2, "FY2022": -3, "FY2021": -4}),
    ("DATA", "Sale of property, plant and equipment", {"FY2022": 0, "FY2021": 3}),
    ("DATA", "Cash expenditure on / purchase of intangible assets", {"FY2025": -9, "FY2024": -10, "FY2023": -22, "FY2022": -28, "FY2021": -27}),
    ("DATA", "Sale of intangible assets", {"FY2022": 0, "FY2021": 1}),
    ("DATA", "Purchase of net assets and liabilities", {"FY2023": 0, "FY2022": -270, "FY2021": 0}),
    ("DATA", "Dividends received from subsidiaries", {"FY2025": 33, "FY2024": 28, "FY2023": 60, "FY2022": 8, "FY2021": 15}),
    ("TOTAL", "Net cash flows from investing activities", {"FY2025": 22, "FY2024": 9, "FY2023": 36, "FY2022": -293, "FY2021": -12}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Issue of debt securities in issue", {"FY2025": 0, "FY2024": 260, "FY2023": 0, "FY2022": 50, "FY2021": 252}),
    ("DATA", "Redemption of debt securities in issue", {"FY2025": 0, "FY2024": -260, "FY2023": -50, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Issue of paid-in equity", {"FY2023": 0, "FY2022": 240, "FY2021": 0}),
    ("DATA", "Redemption of paid-in equity", {"FY2023": -35, "FY2022": -167, "FY2021": 0}),
    ("DATA", "Issue of subordinated liabilities", {"FY2023": 300, "FY2022": 0}),
    ("DATA", "Redemption of subordinated liabilities", {"FY2023": -266, "FY2022": 0}),
    ("DATA", "Interest paid on subordinated liabilities and debt securities in issue", {"FY2025": -45, "FY2024": -44, "FY2023": -55, "FY2022": -21, "FY2021": -12}),
    ("DATA", "Paid-in equity dividends paid", {"FY2025": -26, "FY2024": -28, "FY2023": -31, "FY2022": -16, "FY2021": -12}),
    ("DATA", "Dividends paid", {"FY2025": -187, "FY2024": -289, "FY2023": -210, "FY2022": -225, "FY2021": -105}),
    ("TOTAL", "Net cash flows from financing activities", {"FY2025": -258, "FY2024": -361, "FY2023": -347, "FY2022": -139, "FY2021": 123}),
    ("DATA", "Effects of exchange rate changes on cash and cash equivalents", {"FY2025": -1, "FY2024": 0, "FY2023": -1, "FY2022": 24, "FY2021": -38}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -1740, "FY2024": 7661, "FY2023": 2033, "FY2022": 5834, "FY2021": 16534}),
    ("DATA", "Cash and cash equivalents at 1 January", {"FY2025": 44222, "FY2024": 36561, "FY2023": 34528, "FY2022": 28694, "FY2021": 12160}),
    ("TOTAL", "Cash and cash equivalents at 31 December", {"FY2025": 42482, "FY2024": 44222, "FY2023": 36561, "FY2022": 34528, "FY2021": 28694}),
]

bw.add_cash_flow_sheet(
    title="Coutts & Company — Cash Flow Statement",
    subtitle="Entity-level basis, £m. Presentation varies by year - see source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=95,
    source_height=280,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Asset Quality
# ---------------------------------------------------------------
bw.add_asset_quality_sheet(
    title="Coutts & Company — Asset Quality",
    subtitle="Entity-level basis, £m. See source note at bottom.",
    rows=[
        ("SECTION", "Loans - amortised cost and FVOCI, by IFRS 9 stage", {}),
        ("DATA", "Stage 1", {"FY2025": 17334, "FY2024": 16998, "FY2023": 17400, "FY2022": 18112, "FY2021": 16648}),
        ("DATA", "Stage 2", {"FY2025": 1110, "FY2024": 840, "FY2023": 906, "FY2022": 795, "FY2021": 936}),
        ("DATA", "Stage 3", {"FY2025": 338, "FY2024": 317, "FY2023": 247, "FY2022": 230, "FY2021": 250}),
        ("DATA", "Inter-Group (classified Stage 1)", {"FY2025": 42464, "FY2024": 44301, "FY2023": 36633, "FY2022": 34681, "FY2021": 28678}),
        ("TOTAL", "Total gross loans (amortised cost and FVOCI)", {"FY2025": 61246, "FY2024": 62456, "FY2023": 55186, "FY2022": 53818, "FY2021": 46512}),
        ("SECTION", "ECL provisions, by IFRS 9 stage", {}),
        ("DATA", "Stage 1", {"FY2025": 13, "FY2024": 16, "FY2023": 20, "FY2022": 22, "FY2021": 11}),
        ("DATA", "Stage 2", {"FY2025": 13, "FY2024": 10, "FY2023": 20, "FY2022": 14, "FY2021": 27}),
        ("DATA", "Stage 3", {"FY2025": 50, "FY2024": 37, "FY2023": 32, "FY2022": 23, "FY2021": 35}),
        ("DATA", "Inter-Group", {"FY2025": 14, "FY2024": 19, "FY2023": 27, "FY2022": 38, "FY2021": 5}),
        ("TOTAL", "Total ECL provisions", {"FY2025": 90, "FY2024": 82, "FY2023": 99, "FY2022": 97, "FY2021": 78}),
        ("SECTION", "ECL provisions coverage", {}),
        ("DATA", "Stage 1 (%)", {"FY2025": "0.07%", "FY2024": "0.09%", "FY2023": "0.11%", "FY2022": "0.12%", "FY2021": "0.07%"}),
        ("DATA", "Stage 2 (%)", {"FY2025": "1.17%", "FY2024": "1.19%", "FY2023": "2.21%", "FY2022": "1.76%", "FY2021": "2.88%"}),
        ("DATA", "Stage 3 (%)", {"FY2025": "14.79%", "FY2024": "11.67%", "FY2023": "12.96%", "FY2022": "10.00%", "FY2021": "14.00%"}),
        ("DATA", "Inter-Group (%)", {"FY2025": "0.03%", "FY2024": "0.04%", "FY2023": "0.07%", "FY2022": "0.11%", "FY2021": "0.02%"}),
        ("DATA", "Overall coverage (%)", {"FY2025": "0.40%", "FY2024": "0.35%", "FY2023": "0.39%", "FY2022": "0.31%", "FY2021": "0.41%"}),
        ("SECTION", "ECL charge/(release) for the year, by IFRS 9 stage", {}),
        ("DATA", "Stage 1", {"FY2025": -9, "FY2024": -11, "FY2023": -9, "FY2022": 2, "FY2021": -44}),
        ("DATA", "Stage 2", {"FY2025": 9, "FY2024": -1, "FY2023": 16, "FY2022": -8, "FY2021": -15}),
        ("DATA", "Stage 3", {"FY2025": 10, "FY2024": 1, "FY2023": 7, "FY2022": 3, "FY2021": 7}),
        ("DATA", "Inter-Group", {"FY2025": -5, "FY2024": -8, "FY2023": -11, "FY2022": 34, "FY2021": -5}),
        ("TOTAL", "Total ECL charge/(release) for the year", {"FY2025": 5, "FY2024": -19, "FY2023": 3, "FY2022": 31, "FY2021": -57}),
        ("DATA", "Amounts written off", {"FY2025": 1, "FY2024": 1, "FY2023": 2, "FY2022": 15, "FY2021": 6}),
        ("SECTION", "Derived ratio", {}),
        ("DATA", "Stage 3 / gross third-party loans (excl. Inter-Group)", {"FY2025": "1.80%", "FY2024": "1.75%", "FY2023": "1.33%", "FY2022": "1.20%", "FY2021": "1.40%"}),
    ],
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=68,
    source_height=220,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 / capital metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=44, source_height=170)


CET1_CAPITAL = {"FY2025": 1248, "FY2024": 1192, "FY2023": 1199, "FY2022": 1260, "FY2021": 1235}
CET1_RATIO = {"FY2025": "11.4%", "FY2024": "11.3%", "FY2023": "11.3%", "FY2022": "11.8%", "FY2021": "11.9%"}
TIER1_CAPITAL = {"FY2025": 1488, "FY2024": 1432, "FY2023": 1439, "FY2022": 1535, "FY2021": 1437}
TIER1_RATIO = {"FY2025": "13.5%", "FY2024": "13.6%", "FY2023": "13.6%", "FY2022": "14.3%", "FY2021": "13.9%"}
TOTAL_CAPITAL = {"FY2025": 1788, "FY2024": 1732, "FY2023": 1739, "FY2022": 1790, "FY2021": 1703}
TOTAL_CAPITAL_RATIO = {"FY2025": "16.3%", "FY2024": "16.4%", "FY2023": "16.4%", "FY2022": "16.7%", "FY2021": "16.4%"}
TOTAL_RWA = {"FY2025": 10982, "FY2024": 10564, "FY2023": 10591, "FY2022": 10722, "FY2021": 10367}
LEVERAGE_RATIO = {"FY2025": "7.6%", "FY2024": "7.5%", "FY2023": "7.4%", "FY2022": "7.7%"}

NOT_DISCLOSED_LIQ_NOTE = (
    "Not publicly disclosed at Coutts's own entity level in any year - managed and disclosed only at the "
    "UK DoLSub sub-group level (NatWest Bank Plc + RBS plc + Coutts). See the sheet's source note for the "
    "exact quoted basis."
)
NOT_DISCLOSED_MREL_NOTE = (
    "Not publicly disclosed for any year - MREL is defined in the Annual Report's own glossary of capital "
    "concepts, but no MREL ratio for Coutts specifically is ever stated."
)

metric("CET1 Capital", "£m", [("Common Equity Tier 1 (CET1) capital", CET1_CAPITAL)])
metric("CET1 Ratio", "%", [("CET1 ratio", CET1_RATIO)])
metric("Tier 1 Capital", "£m", [("Tier 1 capital", TIER1_CAPITAL)])
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", TIER1_RATIO)])
metric("Total Capital", "£m", [("Total regulatory capital", TOTAL_CAPITAL)])
metric("Total Capital Ratio", "%", [("Total capital ratio", TOTAL_CAPITAL_RATIO)])
metric("Total RWAs", "£m", [("Total risk-weighted assets", TOTAL_RWA)])

bw.add_rwa_breakdown_sheet(
    title="Coutts & Company — RWA Breakdown",
    subtitle="Entity-level basis, £m. See source note at bottom.",
    rows=[
        ("SECTION", "RWA by risk category", {}),
        ("DATA", "Credit risk", {"FY2025": 9416, "FY2024": 9231, "FY2023": 9420, "FY2022": 9664, "FY2021": 9284}),
        ("DATA", "Counterparty credit risk", {"FY2025": 1, "FY2024": 1, "FY2023": 1, "FY2022": 6, "FY2021": 5}),
        ("DATA", "Market risk", {"FY2025": 20, "FY2024": 24, "FY2023": 2, "FY2022": 9, "FY2021": 4}),
        ("DATA", "Operational risk", {"FY2025": 1545, "FY2024": 1308, "FY2023": 1168, "FY2022": 1043, "FY2021": 1074}),
        ("TOTAL", "Total RWAs", {"FY2025": 10982, "FY2024": 10564, "FY2023": 10591, "FY2022": 10722, "FY2021": 10367}),
    ],
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=54,
    source_height=200,
    unit_suffix=" (£m)",
)
metric(
    "Leverage Ratio", "%", [("UK leverage ratio", LEVERAGE_RATIO)],
    note="FY2021 not disclosed - the FY2022 Annual Report (the only source for FY2021) does not include a "
         "leverage ratio table at all; the leverage-ratio disclosure only begins from the FY2023 report "
         "onward (shown there with a FY2022 comparative, used for the FY2022 column here).",
)

bw.add_not_disclosed_metric_sheets(
    ["LCR", "NSFR"], p3_sources(), per_note={"LCR": NOT_DISCLOSED_LIQ_NOTE, "NSFR": NOT_DISCLOSED_LIQ_NOTE},
)
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources(), per_note={"MREL Ratio": NOT_DISCLOSED_MREL_NOTE},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 61695, "FY2024": 62860, "FY2023": 55573, "FY2022": 54270, "FY2021": 46915}),
        ("Loans to customers - amortised cost", {"FY2025": 18642, "FY2024": 18034, "FY2023": 18333, "FY2022": 18934, "FY2021": 17388}),
        ("Customer deposits", {"FY2025": 42642, "FY2024": 42318, "FY2023": 37549, "FY2022": 41057, "FY2021": 36971}),
        ("Owners' equity", {"FY2025": 1544, "FY2024": 1497, "FY2023": 1618, "FY2022": 1600, "FY2021": 1521}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total income", {"FY2025": 990, "FY2024": 882, "FY2023": 959, "FY2022": 922, "FY2021": 632}),
        ("Operating expenses", {"FY2025": -639, "FY2024": -639, "FY2023": -575, "FY2022": -533, "FY2021": -448}),
        ("Profit for the year", {"FY2025": 259, "FY2024": 198, "FY2023": 294, "FY2022": 247, "FY2021": 181}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 1497, "FY2024": 1618, "FY2023": 1600, "FY2022": 1521, "FY2021": 1456}),
        ("Total comprehensive income for the year, net of tax", {"FY2025": 260, "FY2024": 196, "FY2023": 294, "FY2022": 247, "FY2021": 182}),
        ("Other equity movements, net", {"FY2025": -213, "FY2024": -317, "FY2023": -276, "FY2022": -168, "FY2021": -117}),
        ("Closing equity", {"FY2025": 1544, "FY2024": 1497, "FY2023": 1618, "FY2022": 1600, "FY2021": 1521}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash flows from operating activities", {"FY2025": -1503, "FY2024": 8013, "FY2023": 2345, "FY2022": 6242, "FY2021": 16461}),
        ("Net cash flows from investing activities", {"FY2025": 22, "FY2024": 9, "FY2023": 36, "FY2022": -293, "FY2021": -12}),
        ("Net cash flows from financing activities", {"FY2025": -258, "FY2024": -361, "FY2023": -347, "FY2022": -139, "FY2021": 123}),
        ("Cash and cash equivalents at 31 December", {"FY2025": 42482, "FY2024": 44222, "FY2023": 36561, "FY2022": 34528, "FY2021": 28694}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Tier 1 Ratio", TIER1_RATIO),
        ("Total Capital Ratio", TOTAL_CAPITAL_RATIO),
        ("Leverage Ratio", LEVERAGE_RATIO),
    ],
    note="LCR/NSFR/MREL omitted from this chart - not disclosed at Coutts's own entity level in any year "
         "(see the individual sheets). Figures are duplicated from the detail sheets for at-a-glance trend "
         "viewing; see each sheet's own source citation for the underlying document/page.",
)

bw.save("/Users/armaan/code/katalysis/banks/COUTTS FINANCIALS.xlsx")
