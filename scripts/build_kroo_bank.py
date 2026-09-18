import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Kroo Bank Ltd (FRN 953772, Companies House 10359002, incorporated 5 Sept
# 2016) was authorised as a bank with restrictions on 7 July 2021 and only
# came within scope of UK bank regulation from that date. Only 4 Annual
# Reports have ever been published (FY2021-FY2024, year-end 31 December) -
# no FY2025 report exists yet. Re-checked 2026-09-18 (GA-003) by four
# independent routes; Kroo's FY2025 accounts are not due at Companies House
# until 30 SEPTEMBER 2026, twelve days after that check, and Kroo has filed on
# the deadline in every one of its four years. See ENTITY_NOTE for the
# evidence and the exact date to look again. So only 4 years are included here
# rather than padding to 5, the same pattern as Brown Shipley/Griffin Bank.
YEARS = ["FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2021_URL = "https://www.kroo.com/files/kroo-annual-report-2021.pdf"
AR2022_URL = "https://www.kroo.com/files/kroo-annual-report-2022.pdf"
AR2023_URL = "https://www.kroo.com/files/kroo-annual-report-2023.pdf"
AR2024_URL = "https://www.kroo.com/files/kroo-annual-report-2024.pdf"
P3_2021_URL = "https://www.kroo.com/files/kroo-pillar-3-disclosures-2021.pdf"
P3_2022_URL = "https://www.kroo.com/files/kroo-pillar-3-disclosures-2022.pdf"
P3_2023_URL = "https://www.kroo.com/files/kroo-pillar-3-disclosures-2023.pdf"
P3_2024_URL = "https://www.kroo.com/files/kroo-pillar-3-disclosures-2024.pdf"

ENTITY_NOTE = (
    "Kroo Bank Ltd (Companies House 10359002) was authorised as a bank with restrictions on 7 July 2021 "
    "and only came within scope of UK bank regulation from that date - FY2021 is therefore its first "
    "reporting period as a regulated bank. Only 4 Annual Reports have ever been published "
    "(FY2021-FY2024) - no FY2025 Annual Report or Pillar 3 report exists yet as of this build, so only "
    "4 years are included here rather than padding to 5.\n"
    "FY2025 DOES NOT EXIST YET - CHECKED 18 SEPTEMBER 2026 (GA-003), FOUR INDEPENDENT ROUTES, ALL "
    "AGREEING. This is recorded in full so that a later session can tell 'checked, none newer' from "
    "'never checked', and so that nobody re-runs the same dead search.\n"
    "  (1) Kroo publishes its reports on two DEDICATED index pages, not a general legal page: "
    "kroo.com/annual-reports lists exactly four documents (2021, 2022, 2023, 2024) and "
    "kroo.com/pillar-3-disclosures lists exactly four (2021, 2022, 2023, 2024). Both were fetched as "
    "static HTML - the links are in the served markup, so nothing is hidden behind JavaScript.\n"
    "  (2) Those index pages also SHOW the file-naming convention "
    "(/files/kroo-annual-report-<year>.pdf and /files/kroo-pillar-3-disclosures-<year>.pdf), which is "
    "what makes a direct probe meaningful rather than a guess: the 2025 and 2026 forms of both names "
    "return HTTP 404, while the 2024 forms of both return 200 / Content-Type application/pdf / %PDF "
    "magic bytes (492,016 and 350,437 bytes) as a reach control. Both 2024 files were opened and their "
    "cover pages still read 'For the year ended 31 December 2024' - so Kroo has NOT quietly republished a "
    "FY2025 edition over a FY2024 filename.\n"
    "  (3) Companies House, company 10359002, read 18 Sep 2026: 'Last accounts made up to 31 December "
    "2024'; 'Next accounts made up to 31 December 2025 due by 30 SEPTEMBER 2026'. No FY2025 accounts "
    "filed.\n"
    "  (4) A Wayback CDX sweep of the whole kroo.com domain (6,127 captured URLs) returns no annual "
    "report or Pillar 3 document later than 2024, on either the live host or the dev.kroo.com staging "
    "host that mirrors /files/ - and the FY2024 Pillar 3 was still being captured as recently as 10 March "
    "2026. The staging host's own index pages were fetched too and likewise list only four of each.\n"
    "PUBLICATION LAG, AND THE DATE TO LOOK AGAIN. Kroo files at the statutory deadline every single year: "
    "FY2021 filed 26 Sep 2022, FY2022 filed 5 Oct 2023, FY2023 filed 28 Sep 2024, FY2024 filed 22 Sep "
    "2025. The FY2025 deadline is 30 SEPTEMBER 2026 - twelve days after this check. A re-check in October "
    "2026 should find the Annual Report, and the Pillar 3 disclosure has followed within weeks of it in "
    "every year so far. This is a 'come back in a fortnight', not a dead end."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Kroo Bank Ltd's own Statement of Cash Flows, each year's own originally "
    "published figures used (no restatement affects the cash flow statement itself):\n"
    "FY2024: Annual Report 2024, p.37 (Statement of cash flows) - " + AR2024_URL + "\n"
    "FY2023: Annual Report 2023, p.38 (Statement of Cash Flows) - " + AR2023_URL + "\n"
    "FY2022: Annual Report 2022, p.28 (Statement of Cash Flows) - " + AR2022_URL + "\n"
    "FY2021: Annual Report 2021, p.27 (Statement of Cash Flows) - " + AR2021_URL + "\n"
    "Note: the FY2023 Annual Report's own FY2022 comparative column and the FY2022 Annual Report's own "
    "FY2022 figures present operating-activity line items with different labels/groupings (e.g. FY2022's "
    "own report shows a standalone 'Interest on debt securities' line, while FY2023's report combines "
    "this into a single 'Net interest income' line) - each year's own originally published report's own "
    "line items are used here rather than a later report's re-presentation, consistent with this "
    "project's convention.\n"
    + ENTITY_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - Kroo Bank Ltd Pillar 3 Disclosures, each year's own originally published figures used:\n"
        "FY2024: Pillar 3 Disclosures 2024, Table 3 (Key metrics, 31 Dec 2024 column) - " + P3_2024_URL + "\n"
        "FY2023: Pillar 3 Disclosures 2023, Table 3 (Key metrics, 31 Dec 2023 column) - " + P3_2023_URL + "\n"
        "FY2022: Pillar 3 Disclosures 2022, Table 3 (Capital resources)/Table 6 (Leverage ratio) - "
        + P3_2022_URL + "\n"
        "FY2021: Pillar 3 Disclosures 2021, Table 3 (Capital resources)/Table 6 (Leverage ratio) - "
        + P3_2021_URL + "\n"
        "SDDT - EXPLICIT NEGATIVE, recorded 2026-09-15 (cross-bank SDDT date-fit pass) so that a future pass "
        "does not wrongly apply the Small Domestic Deposit Taker exemption to this workbook's gap year. Kroo "
        "DOES hold the SDDT opt-in: the Bank of England consolidated list of waivers and modifications granted "
        "to PRA-authorised firms (downloaded 2026-09-15, "
        "https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/authorisations/"
        "waivers-and-modifications-of-rules/consolidated-waivers-pra-firms.csv) carries one SDDT row for FRN "
        "953772, 'Kroo Bank Ltd': 'Modification by Consent - PRA Rulebook - CRR Firms - Rule 3.1 of the SDDT "
        "Regime - General Application Part', sub rule 'Ru 3.1', waiver ref 'A00007919P.pdf', START DATE "
        "17/05/2024, no end date. Rule 3.1 is the operative opt-in, and Kroo holds no criteria-only rows (1.2 / "
        "2.1(9) / 2.6) alongside it.\n"
        "DATE FIT - IT DOES NOT FIT THE GAP YEAR. Kroo's accounting reference date is 31 DECEMBER, confirmed at "
        "Companies House (company 10359002, accounts filed to 31 December for 2021 through 2024). The "
        "outstanding gap year is FY2021, which ended 31 DECEMBER 2021 - two and a half years BEFORE the 17 May "
        "2024 start date. A modification cannot explain a gap that predates it, so the SDDT regime explains NONE "
        "of the FY2021 blanks.\n"
        "FY2021's gap keeps its existing and entirely separate explanation, unchanged: Kroo published a full "
        "Pillar 3 document for FY2021, but on the older pre-KM1 template (Table 3 'Capital resources' / Table 6 "
        "'Leverage ratio'), which does not carry every line the FY2023/FY2024 KM1 key-metrics tables do. That is "
        "a template-vintage gap in a document that exists - the opposite of an exemption from publishing one. "
        "The register finding changes no cell in this workbook.\n"
        "A CAUTION FOR FUTURE PASSES: do not assume the modification silenced the later years either. FY2024 "
        "ended 31 December 2024, seven months AFTER the 17 May 2024 start date, and Kroo nonetheless published a "
        "full FY2024 Pillar 3 document with a KM1 key-metrics table - it is the source for this workbook's "
        "FY2024 column. The exemption permits a firm to stop disclosing; it does not compel it to, and Kroo "
        "evidently kept disclosing. So a future absence in FY2025 or later should be investigated on its own "
        "facts rather than attributed to SDDT by default. This is the SDDT DISCLOSURE exemption, in force now - "
        "not the separate SDDT CAPITAL regime beginning 1 January 2027.\n"
        + extra
        + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="Kroo Bank Ltd", years=YEARS, year_label=YEAR_LABEL, header_color="655905")

STATEMENTS_SOURCES = (
    "Sources - Kroo Bank Ltd's own Annual Reports, each year's own originally published figures used:\n"
    "FY2024: Annual Report 2024, Statement of comprehensive income p.34, Statement of financial position p.35, "
    "Statement of changes in equity p.36, Note 9 (Provision for bad and doubtful debts) p.46, Note 14 (Loans and "
    "advances to customers) p.48 - " + AR2024_URL + "\n"
    "FY2023: Annual Report 2023, Statement of Comprehensive Income p.35, Statement of Financial Position p.36, "
    "Statement of Changes in Equity p.37, Note 14 (Loans and Advances to Customers) p.52, Note 22 (Risk "
    "Management - Credit Risk) p.57 - " + AR2023_URL + "\n"
    "FY2022: Annual Report 2022, Statement of Comprehensive Income p.24, Statement of Financial Position p.25-26, "
    "Statement of Changes in Equity p.27, Note 12 (Debt Securities) p.37 - " + AR2022_URL + "\n"
    "FY2021: Annual Report 2021, Statement of Comprehensive Income p.24, Statement of Financial Position p.25, "
    "Statement of Changes in Equity p.26 - " + AR2021_URL + "\n\n"
    "PRESENTATION NOTE: FY2021's own accounts use a single 'Cash at bank' line (£8,891,191) with no separate "
    "'Loans and advances to banks' split, and no 'Cash and balances at central banks' terminology yet (the Bank "
    "was only authorised on 7 July 2021 and had not yet established a Bank of England reserve account "
    "presentation) - shown here under 'Cash and balances at central banks' for comparability; the FY2022 Annual "
    "Report's own FY2021 comparative column later reclassifies part of this as 'Loans and advances to banks', "
    "but FY2021's own originally published single-line figure is used here per this project's convention. "
    "FY2021's own accounts also use a 'Debtors'/'Creditors: amounts falling due within one year' company-accounts "
    "format (net current assets) rather than FY2022 onward's bank-format 'Total assets = Total liabilities + "
    "equity' presentation - both tie to the same totals (verified), just remapped onto the later years' line "
    "labels (Debtors -> Other assets; Creditors -> Other liabilities) for a consistent workbook shape. FY2021 had "
    "no live customer lending or deposit-taking yet (Kroo was only authorised with restrictions from 7 July "
    "2021) - Loans and advances to customers/Customer accounts are genuinely nil, not undisclosed, for that year.\n"
    "'Debt securities' is only ever held/disclosed in FY2022 (Note 12, Annual Report 2022 p.37): a single line of "
    "UK treasury bills maturing 13 Feb 2023, carried at an amortised cost of £9,972,583 (mark-to-market value "
    "£9,963,894) - no further sub-split by measurement basis or issuer type exists, since the whole balance is "
    "one bucket on both dimensions already, so the row is labelled to name both rather than split into sub-rows. "
    "Annual Report 2023's own Note 12 (p.51) confirms 'No debt securities were held on 31 December 2023', and "
    "Annual Report 2024's own Statement of Cash Flows (no 'Purchase of debt securities' line, only a nil "
    "'Sale of debt securities' line) likewise shows none held at 31 December 2024 - genuinely nil for those "
    "years, not undisclosed.\n"
    + ENTITY_NOTE
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet (Statement of Financial Position)
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {
        "FY2024": 940875108, "FY2023": 848278623, "FY2022": 9833288, "FY2021": 8891191,
    }),
    ("DATA", "Loans and advances to banks", {"FY2024": 12224304, "FY2023": 17480800, "FY2022": 1801808}),
    ("DATA", "Debt securities (UK Treasury bills, amortised cost)", {"FY2022": 9972583}),
    ("DATA", "Loans and advances to customers", {"FY2024": 16140896, "FY2023": 2278905, "FY2022": 10446}),
    ("DATA", "Other assets", {"FY2024": 5917566, "FY2023": 5489956, "FY2022": 3807507, "FY2021": 1406463}),
    ("DATA", "Tangible fixed assets", {"FY2024": 183956, "FY2023": 390173, "FY2022": 286147, "FY2021": 110458}),
    ("TOTAL", "Total assets", {"FY2024": 975341830, "FY2023": 873918457, "FY2022": 25711779, "FY2021": 10408112}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer accounts", {"FY2024": 965804257, "FY2023": 854820499, "FY2022": 1243492}),
    ("DATA", "Other liabilities", {"FY2024": 905729, "FY2023": 2981622, "FY2022": 1449973, "FY2021": 542981}),
    ("DATA", "Accruals and deferred income", {"FY2024": 1303862, "FY2023": 1827783, "FY2022": 589981, "FY2021": 307982}),
    ("TOTAL", "Total liabilities", {"FY2024": 968013848, "FY2023": 859629904, "FY2022": 3283446, "FY2021": 850963}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2024": 95, "FY2023": 68, "FY2022": 59, "FY2021": 41}),
    ("DATA", "Share premium", {"FY2024": 88853695, "FY2023": 76423514, "FY2022": 58475774, "FY2021": 31207390}),
    ("DATA", "Share based payments reserve", {"FY2024": 2618433, "FY2023": 1925967, "FY2022": 1165489, "FY2021": 711032}),
    ("DATA", "Accumulated losses", {"FY2024": -84144241, "FY2023": -64060996, "FY2022": -37212989, "FY2021": -22361314}),
    ("TOTAL", "Total equity", {"FY2024": 7327982, "FY2023": 14288553, "FY2022": 22428333, "FY2021": 9557149}),
    ("TOTAL", "Total liabilities and equity", {"FY2024": 975341830, "FY2023": 873918457, "FY2022": 25711779, "FY2021": 10408112}),
]

bw.add_balance_sheet_sheet(
    title="Kroo Bank Ltd — Balance Sheet",
    subtitle="Company-only, £; each year's own originally reported line items preserved (see source note)",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=340,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss (Statement of Comprehensive Income)
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable and similar income", {
        "FY2024": 49198140, "FY2023": 27973249, "FY2022": 165998,
    }),
    ("DATA", "Interest payable and similar expenses", {
        "FY2024": -39738914, "FY2023": -21814000, "FY2022": -1174, "FY2021": -263545,
    }),
    ("DATA", "Other operating income (interest-related, FY2021 only)", {"FY2021": 413}),
    ("TOTAL", "Net interest income", {"FY2024": 9459226, "FY2023": 6159249, "FY2022": 164824, "FY2021": -263132}),
    ("DATA", "Fee and commission income", {"FY2024": 617780, "FY2023": 283795, "FY2022": 1416}),
    ("DATA", "Fee and commission expense", {"FY2024": -43992, "FY2023": -221917, "FY2022": -370}),
    ("TOTAL", "Net fee and commission income", {"FY2024": 573788, "FY2023": 61878, "FY2022": 1046}),
    ("DATA", "Other operating income", {"FY2024": 325963, "FY2023": 7722, "FY2022": 335}),
    ("TOTAL", "Total income", {"FY2024": 10358977, "FY2023": 6228849, "FY2022": 166205, "FY2021": -263132}),
    ("DATA", "Staff costs", {"FY2024": -17473788, "FY2023": -17541262, "FY2022": -9289464, "FY2021": -5464866}),
    ("DATA", "Depreciation", {"FY2024": -196429, "FY2023": -179217}),
    ("DATA", "Other non-staff costs", {"FY2024": -10944554, "FY2023": -16375747, "FY2022": -7193841, "FY2021": -3336660}),
    ("TOTAL", "Total administrative expenses", {
        "FY2024": -28614771, "FY2023": -34096226, "FY2022": -16483305, "FY2021": -8801526,
    }),
    ("DATA", "Provision for/impairment charges on bad and doubtful debts", {
        "FY2024": -1031330, "FY2023": -59996, "FY2022": -1151,
    }),
    ("TOTAL", "Loss before taxation", {
        "FY2024": -19287124, "FY2023": -27927373, "FY2022": -16318251, "FY2021": -9064658,
    }),
    ("DATA", "Tax credit on loss", {"FY2024": 62736, "FY2023": 1079366, "FY2022": 1466576, "FY2021": 1371848}),
    ("TOTAL", "Loss for the financial year", {
        "FY2024": -19224388, "FY2023": -26848007, "FY2022": -14851675, "FY2021": -7692810,
    }),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Other comprehensive income (nil every year)", {"FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("TOTAL", "Total comprehensive loss for the year", {
        "FY2024": -19224388, "FY2023": -26848007, "FY2022": -14851675, "FY2021": -7692810,
    }),
]

bw.add_income_statement_sheet(
    title="Kroo Bank Ltd — Profit & Loss",
    subtitle="Company-only, £; FY2023's own tax credit (£1,079,366) is later restated to £220,509 in AR2024's "
              "comparative column (see Statement of Changes in Equity sheet) - FY2023's own originally published "
              "figure is used here per this project's convention. FY2021's report shows no standalone 'Interest "
              "income' line before Other operating income; both are shown as originally presented.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=78,
    source_height=340,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity - per-year reconciliation
# ladder confirmed: every year's own closing balance ties exactly to
# both the next year's own opening balance and that year's own Balance
# Sheet Total equity, with one genuine documented bridge (see below).
# ---------------------------------------------------------------
equity_headers = [
    "Called up share capital", "Share premium", "Other reserve",
    "Share based payments reserve", "Accumulated losses", "Total equity",
]
equity_rows = [
    ("TOTAL", "Unaudited opening balance at 1 January 2021 (as restated)", (26, 13000898, 260668, None, -14668504, -1406912)),
    ("DATA", "Loss for the year", (None, None, None, None, -7692810, -7692810)),
    ("DATA", "Issue of share capital for cash", (12, 15064164, None, None, None, 15064176)),
    ("DATA", "Conversion of Future Fund loan", (3, 3142328, -260668, None, None, 2881663)),
    ("DATA", "Issue of share options to staff", (None, None, None, 711032, None, 711032)),
    ("TOTAL", "At 31 December 2021 (FY2021 closing)", (41, 31207390, 0, 711032, -22361314, 9557149)),
    ("DATA", "Loss for the year", (None, None, None, None, -14851675, -14851675)),
    ("DATA", "Issue of share capital for cash", (18, 27268384, None, None, None, 27268402)),
    ("DATA", "Issue of share options to staff", (None, None, None, 454457, None, 454457)),
    ("TOTAL", "At 31 December 2022 (FY2022 closing)", (59, 58475774, None, 1165489, -37212989, 22428333)),
    ("DATA", "Loss for the year", (None, None, None, None, -26848007, -26848007)),
    ("DATA", "Issue of share capital for cash", (9, 17947740, None, None, None, 17947749)),
    ("DATA", "Issue of share options to staff", (None, None, None, 760478, None, 760478)),
    ("TOTAL", "At 31 December 2023 (FY2023 closing, own originally-published figure)", (68, 76423514, None, 1925967, -64060996, 14288553)),
    ("DATA", "Prior year tax restatement (AR2024's own FY2023 comparative, Note 10 'Prior year tax adjustment' "
             "£72,627 - revises FY2023's originally reported tax credit of £1,079,366 down to £220,509)",
     (None, None, None, None, -858857, -858857)),
    ("TOTAL", "At 31 December 2023 as restated (FY2024's own opening balance, per AR2024)", (68, 76423514, None, 1925967, -64919853, 13429696)),
    ("DATA", "Loss for the year", (None, None, None, None, -19224388, -19224388)),
    ("DATA", "Issue of share capital for cash", (27, 12508958, None, None, None, 12508985)),
    ("DATA", "Issue of share options", (None, -78777, None, 692466, None, 613689)),
    ("TOTAL", "At 31 December 2024 (FY2024 closing)", (95, 88853695, None, 2618433, -84144241, 7327982)),
]

bw.add_equity_changes_sheet(
    title="Kroo Bank Ltd — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, £. Every year's own closing balance ties exactly to "
              "both the next year's own opening balance and that year's own Balance Sheet Total equity, except one "
              "genuine documented restatement bridge between FY2023's own closing and FY2024's own opening (a "
              "prior-year tax adjustment disclosed in AR2024's Note 10) - not a plug for an undisclosed movement.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to customers", {}),
    ("DATA", "Gross loans and advances to customers", {"FY2024": 17224343, "FY2023": 2337344, "FY2022": 11597}),
    ("DATA", "Provision for impairment", {"FY2024": -1083447, "FY2023": -58439, "FY2022": -1151}),
    ("TOTAL", "Net loans and advances to customers", {"FY2024": 16140896, "FY2023": 2278905, "FY2022": 10446}),
    ("DATA", "Impairment provision coverage (%)", {"FY2024": "6.29%", "FY2023": "2.50%", "FY2022": "9.92%"}),
    ("SECTION", "Movement in impairment provision during the year", {}),
    ("DATA", "Provision for impairment at 1 January", {"FY2024": 58439, "FY2023": 1151}),
    ("DATA", "Impairment charge", {"FY2024": 1031330, "FY2023": 59996, "FY2022": 1151}),
    ("DATA", "Operational losses", {"FY2024": 67515, "FY2023": 0}),
    ("DATA", "Write-offs", {"FY2024": -73837, "FY2023": -2708}),
    ("TOTAL", "Provision for impairment at 31 December", {"FY2024": 1083447, "FY2023": 58439, "FY2022": 1151}),
    ("SECTION", "Credit quality analysis (FY2023/FY2022, Note 22 Risk Management)", {}),
    ("DATA", "Gross impaired advances (overdrafts)", {"FY2023": 36873}),
    ("DATA", "Specific provision for impairment", {"FY2023": -36873}),
    ("TOTAL", "Net impaired advances", {"FY2023": 0}),
    ("DATA", "Neither past due nor impaired (gross)", {"FY2023": 2389776, "FY2022": 11597}),
    ("DATA", "Collective provision", {"FY2023": -21566, "FY2022": -1151}),
    ("TOTAL", "Neither past due nor impaired (net)", {"FY2023": 2368210, "FY2022": 10446}),
]

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Loss before taxation", {
        "FY2024": -19287124, "FY2023": -27927373, "FY2022": -16318251, "FY2021": -9064658,
    }),
    ("DATA", "Depreciation", {"FY2024": 196429, "FY2023": 179217, "FY2022": 94230, "FY2021": 52641}),
    ("DATA", "Loss on disposal of fixed assets", {"FY2024": 25053}),
    ("DATA", "Impairment charge", {"FY2024": 1031330, "FY2023": 59996, "FY2022": 1151}),
    ("DATA", "Share option charge / Value of share options issued", {
        "FY2024": 613689, "FY2023": 760478, "FY2022": 454457, "FY2021": 711032,
    }),
    ("DATA", "Unauthorised overdraft operational loss", {"FY2024": -21790}),
    ("DATA", "Net interest income", {"FY2024": -9459226, "FY2023": -6159249}),
    ("DATA", "Interest on debt securities", {"FY2022": -116040}),
    ("DATA", "Interest on convertible loan", {"FY2021": 259205}),
    ("DATA", "(Increase)/decrease in other assets", {
        "FY2024": -1221715, "FY2023": -1960147, "FY2022": -934468, "FY2021": -232127,
    }),
    ("DATA", "Increase/(decrease) in other liabilities", {
        "FY2024": -2599814, "FY2023": 2769451, "FY2022": 1188991, "FY2021": 359711,
    }),
    ("DATA", "Movement in customer advances", {"FY2024": -14807003, "FY2023": -2315093}),
    ("DATA", "Movement in customer deposits", {"FY2024": 111086286, "FY2023": 850875499}),
    ("DATA", "Movement in customer balances", {"FY2022": 1231895}),
    ("DATA", "R&D tax credit received", {"FY2023": 1369199, "FY2021": 478309}),
    ("DATA", "Interest received", {"FY2024": 49131596, "FY2023": 27920335}),
    ("DATA", "Interest paid", {"FY2024": -39841442, "FY2023": -19112492}),
    ("TOTAL", "Net cash from/(used in) operating activities", {
        "FY2024": 74846269, "FY2023": 826459821, "FY2022": -14398035, "FY2021": -7435887,
    }),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of tangible fixed assets", {
        "FY2024": -15265, "FY2023": -283243, "FY2022": -270719, "FY2021": -70707,
    }),
    ("DATA", "Proceeds of sale of tangible fixed assets", {"FY2022": 800}),
    ("DATA", "Purchase of debt securities", {"FY2022": -19976892}),
    ("DATA", "Sale of debt securities", {"FY2023": 10000000, "FY2022": 10120349}),
    ("TOTAL", "Net cash from/(used in) investing activities", {
        "FY2024": -15265, "FY2023": 9716757, "FY2022": -10126462, "FY2021": -70707,
    }),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Issue of convertible loan note", {}),
    ("DATA", "Issue of share capital / Issue of shares", {
        "FY2024": 12508985, "FY2023": 18020475, "FY2022": 27268402, "FY2021": 15064176,
    }),
    ("DATA", "Cost of share issues", {"FY2023": -72726}),
    ("TOTAL", "Net cash from financing activities", {
        "FY2024": 12508985, "FY2023": 17947749, "FY2022": 27268402, "FY2021": 15064176,
    }),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {
        "FY2024": 87339989, "FY2023": 854124327, "FY2022": 2743905, "FY2021": 7557582,
    }),
    ("DATA", "Cash at beginning of year", {
        "FY2024": 865759423, "FY2023": 11635096, "FY2022": 8891191, "FY2021": 1333609,
    }),
    ("TOTAL", "Cash at end of year", {
        "FY2024": 953099412, "FY2023": 865759423, "FY2022": 11635096, "FY2021": 8891191,
    }),
]

bw.add_cash_flow_sheet(
    title="Kroo Bank Ltd — Statement of Cash Flows",
    subtitle="Bank-only, £; each year's own originally reported line items preserved (see source note)",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=70,
    source_height=180,
    unit_suffix=" (£)",
)

bw.add_asset_quality_sheet(
    title="Kroo Bank Ltd — Asset Quality",
    subtitle="Company-only, £. No IFRS 9 Stage 1/2/3 split is disclosed in any year - only gross/provision/net "
              "and, for FY2023/FY2022, a past-due-or-impaired split (Note 22) are shown.",
    rows=asset_quality_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nFY2021 had no live customer lending yet (Kroo was only authorised with restrictions from 7 July "
        "2021 and its FY2021 accounts show no 'Loans and advances to customers' line at all) - genuinely absent, "
        "not an access gap. No IFRS 9 Stage 1/2/3 gross-exposure or provision split is disclosed in any year's "
        "Annual Report; the Bank's own credit-quality disclosure (Note 22, FY2023/FY2022 only) instead splits "
        "advances into impaired/not-impaired with a specific/collective provision split, shown above instead."
    ),
    first_col_width=68,
    source_height=380,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=48, source_height=150)


# ---------------------------------------------------------------
# KM1 Key Metrics (wayfinder/km1/map.md) - the Bank's own "Table 3 Key
# metrics", reproduced whole in its own row order, labels and precision.
# Called BEFORE the first add_metric_sheet() so the sheet lands immediately
# after Asset Quality and immediately before CET1 Capital: sheet order
# follows call order.
#
# COLUMN PROVENANCE, which differs by year and is stated on the sheet:
#   FY2024, FY2023 - each from its OWN edition's Table 3 (map rule 1).
#   FY2022         - from the FY2023 edition's '31 Dec 2022' comparative
#                    column, because the FY2022 edition prints NO key-metrics
#                    table at all (map rule 28, not rule 20 - the whole table
#                    is missing, rather than a row being dashed inside a
#                    table that exists).
#   FY2021         - BLANK. Its own edition prints no key-metrics table
#                    either, and no later edition anywhere carries a
#                    31 Dec 2021 comparative, so map rule 28(c) applies.
# ---------------------------------------------------------------
km1_rows = [
    ("SECTION", "Available own funds", {}),
    ("DATA", "Common equity tier 1 (CET1) (£, single pounds as printed)",
     {"FY2024": 7327982, "FY2023": 14288553, "FY2022": 22428333}),
    ("DATA", "Tier 1 capital (£, single pounds as printed)",
     {"FY2024": 7327982, "FY2023": 14288553, "FY2022": 22428333}),
    ("DATA", "Total capital (£, single pounds as printed)",
     {"FY2024": 7327982, "FY2023": 14288553, "FY2022": 22428333}),
    ("SECTION", "Risk weighted exposure amounts", {}),
    ("DATA", "Total risk-weighted exposure amount (£, single pounds as printed)",
     {"FY2024": 30590678, "FY2023": 30694218, "FY2022": 24070601}),
    ("SECTION", "Capital ratios (as a percentage of risk weighted exposure amounts)", {}),
    ("DATA", "Common equity tier 1 ratio (%)", {"FY2024": "24.0%", "FY2023": "46.6%", "FY2022": "93.2%"}),
    ("DATA", "Tier 1 ratio (%)", {"FY2024": "24.0%", "FY2023": "46.6%", "FY2022": "93.2%"}),
    ("DATA", "Total capital ratio (%)", {"FY2024": "24.0%", "FY2023": "46.6%", "FY2022": "93.2%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "Additional CET1 SREP requirements (%)", {"FY2024": "1.63%", "FY2023": "2.69%", "FY2022": "2.69%"}),
    ("DATA", "Additional AT1 SREP requirements (%)", {"FY2024": "0.54%", "FY2023": "0.89%", "FY2022": "0.89%"}),
    ("DATA", "Additional T2 SREP requirements (%)", {"FY2024": "0.72%", "FY2023": "1.19%", "FY2022": "1.19%"}),
    ("DATA", "Total SREP own funds requirements (%)", {"FY2024": "10.89%", "FY2023": "12.77%", "FY2022": "12.77%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "Capital conservation buffer (%)", {"FY2024": "2.50%", "FY2023": "2.50%", "FY2022": "2.50%"}),
    ("DATA", "Institution specific countercyclical capital buffer (%)",
     {"FY2024": "2.00%", "FY2023": "2.00%", "FY2022": "1.00%"}),
    ("DATA", "Combined buffer requirement (%)", {"FY2024": "4.50%", "FY2023": "4.50%", "FY2022": "3.50%"}),
    ("DATA", "Overall capital requirements (%)", {"FY2024": "15.39%", "FY2023": "17.27%", "FY2022": "16.27%"}),
    ("DATA", "CET1 available after meeting the total SREP own funds requirements (%)",
     {"FY2024": "5.90%", "FY2023": "27.93%", "FY2022": "71.26%"}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "Total exposure measure excluding claims on central banks (£, single pounds as printed)",
     {"FY2024": 34574564, "FY2023": 25698472, "FY2022": 22434969}),
    ("DATA", "Leverage ratio excluding claims on central banks (%)",
     {"FY2024": "21.2%", "FY2023": "55.6%", "FY2022": "100.0%"}),
    ("SECTION", "Liquidity coverage ratio", {}),
    ("DATA", "Total high-quality liquid assets (HQLA) (Weighted value - average) (£, single pounds as printed)",
     {"FY2024": 935559813, "FY2023": 841232729, "FY2022": 18404383}),
    ("DATA", "Cash outflows - Total weighted value (£, single pounds as printed)",
     {"FY2024": 140540012, "FY2023": 125025307, "FY2022": 189842}),
    ("DATA", "Cash inflows - Total weighted value (£, single pounds as printed)",
     {"FY2024": 17037587, "FY2023": 19802995, "FY2022": 1900810}),
    ("DATA", "Total net cash outflows (adjusted value) (£, single pounds as printed)",
     {"FY2024": 123502425, "FY2023": 19802995, "FY2022": 142381}),
    ("DATA", "Liquidity coverage ratio (%)", {"FY2024": "758%", "FY2023": "4248%", "FY2022": "12926%"}),
    ("SECTION", "Net stable funding ratio", {}),
    ("DATA", "Total available stable funding (£, single pounds as printed)",
     {"FY2024": 813112171, "FY2023": 785009254, "FY2022": 23575372}),
    ("DATA", "Total required stable funding (£, single pounds as printed)",
     {"FY2024": 17979876, "FY2023": 14888848, "FY2022": 4786632}),
    ("DATA", "NSFR ratio (%)", {"FY2024": "4522%", "FY2023": "5272%", "FY2022": "493%"}),
]

KM1_SOURCES = (
    "Sources - Kroo Bank Ltd's own Pillar 3 Disclosures, 'Table 3 Key metrics', in plain single pounds and % "
    "exactly as printed:\n"
    "FY2024: Pillar 3 Disclosures 2024, 'Table 3 - Key metrics', printed p.17, column '31 DEC 2024' - "
    + P3_2024_URL + "\n"
    "FY2023: Pillar 3 Disclosures 2023, 'Table 3 Key metrics', printed p.18, column '31 Dec 2023' - "
    + P3_2023_URL + "\n"
    "FY2022: the '31 Dec 2022' COMPARATIVE column of the FY2023 edition above - see the provenance note "
    "below, which explains why this one column is not from its own edition.\n"
    "FY2021: blank. Not a row we failed to find - see below.\n\n"
    "IS THIS THE KM1 TEMPLATE? YES, ON THE ROW-SET TEST (map rule 8). Kroo heads the table 'Table 3 Key "
    "metrics', prints no template row numbers and never writes the token 'KM1', so no presence test keyed on "
    "the token or on the numbering would find it. The row set is the template's, and in full: available own "
    "funds (CET1/Tier 1/Total), total risk-weighted exposure amount, the three capital ratios, the four SREP "
    "additional own funds requirement rows, the capital conservation and countercyclical buffers with the "
    "combined buffer requirement, overall capital requirements, CET1 available after meeting the total SREP "
    "requirement, the leverage exposure measure and ratio, the full four-row LCR build-up, and the three-row "
    "NSFR build-up. This is the template printed unnumbered, not a short summary table.\n\n"
    "WHY FY2022 COMES FROM THE FY2023 EDITION'S COMPARATIVE (map rule 28, decided by the project owner "
    "2026-09-17). Kroo's FY2022 edition contains NO key-metrics table of any kind. Its contents page lists "
    "twelve tables and they are a different, older set - Table 3 'Capital resources', Table 4 'Risk weighted "
    "assets', Table 5 'Pillar 1 capital surplus', Table 6 'Leverage ratio', Table 9 'Liquidity coverage ratio "
    "(average)' and so on. Verified 2026-09-17 by reading that edition's own table of contents and its table "
    "captions in full, not by a keyword count: searches for 'Key metrics' and 'combined buffer' return zero "
    "hits, and every hit for 'own funds', 'countercyclical', 'stable funding', 'risk-weighted' and 'total "
    "exposure measure' was inspected individually and is narrative prose or a row of one of those older "
    "tables. Because the whole table is missing rather than a row being dashed inside a table that exists, "
    "this is map rule 28 and not map rule 20, and the column is FILLED from the later edition's comparative "
    "and labelled as such here.\n\n"
    "WHY FY2021 IS NEVERTHELESS BLANK (map rule 28(c)). Filling is only possible where a later edition "
    "actually prints the year. Kroo's FY2021 edition prints the same older table set as FY2022 and no "
    "key-metrics table; the FY2022 edition, which would be the only place a 31 Dec 2021 comparative could "
    "appear, has no key-metrics table to carry one. No edition anywhere therefore carries these rows for "
    "31 December 2021, so the column stays empty. Kroo's separate older tables DO give FY2021 capital, RWA, "
    "leverage and LCR figures, and those are on this workbook's individual Pillar 3 metric sheets - but they "
    "are a different table on a different template, and mapping them onto these rows would invent a "
    "correspondence Kroo never published.\n\n"
    "RESTATEMENTS - FY2023 IS PRINTED TWICE AND THE TWO DISAGREE MATERIALLY. FY2023's own edition (used here) "
    "gives CET1/Tier 1/Total capital of £14,288,553 and capital ratios of 46.6%; the FY2024 edition's own "
    "31 Dec 2023 comparative restates those to £13,429,696 and 43.8%, and its LCR comparative to 799% against "
    "the 4,248% FY2023 itself published. The FY2024 edition states the cause in its own words: 'Total assets "
    "and equity for 31 December 2023 differ from those disclosed in the 2023 Pillar 3 report due to a prior "
    "year adjustment. Details of this are set out in note 1 of the Bank's 2024 annual report.' Each year's own "
    "edition is used here (map rule 1), so this sheet carries the originally published FY2023 figures and the "
    "restated ones are recorded here rather than substituted.\n\n"
    "SOURCE DEFECT, REPRODUCED NOT CORRECTED (map rule 7). In the FY2023 edition's own Table 3, the row "
    "'Total net cash outflows (adjusted value)' for 31 Dec 2023 is printed as 19,802,995 - the identical "
    "figure printed one row above it as 'Cash inflows - Total weighted value'. It is not consistent with that "
    "column's own LCR of 4,248% (841,232,729 / 19,802,995 would be about 4,248%, so the two are internally "
    "consistent with each other, but the FY2024 edition's comparative for the same date prints net outflows of "
    "105,222,312 and an LCR of 799%). The figure is reproduced above exactly as the FY2023 edition printed it "
    "and the divergence is flagged here rather than silently reconciled.\n\n"
    "CAPTION DRIFT ALONG THE HQLA ROW. The FY2024 edition captions it 'Total high-quality liquid assets (HQLA) "
    "(Weighted value -average)'; the FY2023 edition captions the same row 'Total high-quality liquid assets "
    "(HQLA) (Weighted value)', without the word average. The FY2024 wording is used for the row label and the "
    "drift is recorded here.\n\n"
    "PRECISION IS THE BANK'S OWN AND VARIES ACROSS THIS SHEET - two decimals on the SREP and buffer rows, one "
    "on the capital ratios, none on the LCR and NSFR percentages. That is Kroo's house style, not an "
    "inconsistency to tidy. Note also that the FY2022 capital ratios read 93.2% here, as the FY2023 edition's "
    "comparative prints them, while this workbook's CET1 Ratio metric sheet carries 93.18% from Kroo's own "
    "FY2022-edition capital-resources table - the same ratio at two different printed precisions from two "
    "different tables, not a disagreement about the number. The same applies to the FY2022 leverage ratio "
    "(100.0% here against 99.97% on the Leverage Ratio sheet).\n\n"
    "LATEST-EDITION CHECK (required by the KM1 map), first performed 2026-09-17 against the Bank's OWN "
    "website and re-performed and WIDENED 2026-09-18 for GA-003: kroo.com/pillar-3-disclosures lists "
    "exactly four Pillar 3 documents - 2021, 2022, 2023 and 2024 - which are the four already cited in "
    "this build script, and kroo.com/annual-reports likewise carries FY2021 through FY2024. The newest "
    "Pillar 3 edition published is the 2024 one. NONE NEWER EXISTS; no FY2025 Annual Report or Pillar 3 "
    "disclosure has been published yet. The 2026-09-17 reading was index-only; the 2026-09-18 re-check "
    "added three further routes - a direct probe of the 2025/2026 filenames on the convention those index "
    "pages themselves demonstrate (404, against a 200/application/pdf/%PDF control on the 2024 names), a "
    "read of the live 2024 files' cover pages to rule out an in-place republication, and Companies House "
    "('next accounts made up to 31 December 2025 due by 30 September 2026'). The full evidence and the "
    "date to look again are in the entity note below.\n\n"
    + ENTITY_NOTE
)

bw.add_km1_sheet(
    title="Kroo Bank Ltd — KM1 Key Metrics",
    subtitle="The Bank's own published 'Table 3 Key metrics', reproduced whole in its own row order, labels and "
             "printed precision. Bank-only basis. Amounts in plain single pounds exactly as printed (Kroo does "
             "not report in £'000 or £m), ratios as printed. Kroo prints the template unnumbered and never uses "
             "the token 'KM1'; the row set is what identifies it. FY2024 and FY2023 come from their own "
             "editions; FY2022 is the FY2023 edition's comparative column because the FY2022 edition prints no "
             "key-metrics table at all; FY2021 is blank because no edition anywhere prints these rows for that "
             "date. See the source note for all of this, and for a reproduced source defect on the FY2023 net "
             "cash outflows row.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=78,
    source_height=520,
)

metric(
    "CET1 Capital", "£",
    [("Common Equity Tier 1 (CET1) capital", {
        "FY2024": 7327982, "FY2023": 14288553, "FY2022": 22428333, "FY2021": 9557150,
    })],
    p3_sources(
        "Note: the FY2024 Pillar 3 report's own FY2023 comparative shows a materially different, "
        "restated CET1/Tier 1/Total Capital figure of £13,429,696 (and RWA £30,694,218 vs the "
        "originally-published £30,694,218 - RWA is unchanged, only capital changed), explicitly "
        "attributed by the document itself to 'a prior year adjustment' detailed in note 1 of the "
        "2024 Annual Report. FY2023's own originally published figure (£14,288,553) is used here per "
        "this project's convention.\n"
    ),
)
metric(
    "CET1 Ratio", "%",
    [("Common equity tier 1 ratio", {
        "FY2024": "24.0%", "FY2023": "46.6%", "FY2022": "93.18%", "FY2021": "287.76%",
    })],
    p3_sources(),
    note="Extreme early-year ratios (287.76% FY2021, 93.18% FY2022) reflect a genuine early-mobilisation "
         "position - capital raised well ahead of RWA growth, confirmed internally consistent against "
         "each year's own RWA figure, not a transcription error.",
)
metric(
    "Tier 1 Capital", "£",
    [("Tier 1 capital", {
        "FY2024": 7327982, "FY2023": 14288553, "FY2022": 22428333, "FY2021": 9557150,
    })],
    p3_sources(),
    note="No Additional Tier 1 instruments in issue any year - Tier 1 capital equals CET1 capital "
         "throughout, per the source's own Table 3/Key metrics.",
)
metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 ratio", {
        "FY2024": "24.0%", "FY2023": "46.6%", "FY2022": "93.18%", "FY2021": "287.76%",
    })],
    p3_sources(),
)
metric(
    "Total Capital", "£",
    [("Total capital", {
        "FY2024": 7327982, "FY2023": 14288553, "FY2022": 22428333, "FY2021": 9557150,
    })],
    p3_sources(),
    note="No Tier 2 instruments in issue any year - Total capital equals CET1/Tier 1 capital throughout.",
)
metric(
    "Total Capital Ratio", "%",
    [("Total capital ratio", {
        "FY2024": "24.0%", "FY2023": "46.6%", "FY2022": "93.18%", "FY2021": "287.76%",
    })],
    p3_sources(),
)
metric(
    "Total RWAs", "£",
    [("Total risk-weighted exposure amount", {
        "FY2024": 30590678, "FY2023": 30694218, "FY2022": 24070601, "FY2021": 3321197,
    })],
    p3_sources(),
)
rwa_breakdown_rows = [
    ("DATA", "Institutions", {"FY2024": 3169193, "FY2023": 3496160, "FY2022": 360362, "FY2021": 1771679}),
    ("DATA", "Corporates", {"FY2024": 1940031, "FY2023": 4337963, "FY2022": 1481817, "FY2021": 545521}),
    ("DATA", "Retail", {"FY2024": 12105672, "FY2023": 1709179, "FY2022": 7835}),
    ("DATA", "Central Bank & Government", {"FY2024": 0, "FY2023": 0, "FY2022": 0}),
    ("DATA", "Cash", {"FY2021": 0}),
    ("DATA", "Other", {"FY2024": 183956, "FY2023": 1542166, "FY2022": 2611837, "FY2021": 1003997}),
    ("TOTAL", "Credit Risk total", {"FY2024": 17398852, "FY2023": 11085468, "FY2022": 4461851}),
    ("DATA", "Operational Risk", {"FY2024": 13191826, "FY2023": 19608750, "FY2022": 19608750}),
    ("TOTAL", "Total risk-weighted exposure amount", {
        "FY2024": 30590678, "FY2023": 30694218, "FY2022": 24070601, "FY2021": 3321197,
    }),
]

bw.add_rwa_breakdown_sheet(
    title="Kroo Bank Ltd — RWA Breakdown",
    subtitle="Standardised approach to credit risk, Basic Indicator Approach to operational risk (each year's own "
              "Pillar 3 Disclosures document, Table 5/4 'Risk weighted assets'). £. FY2021's own table has no "
              "separate 'Credit Risk total'/'Operational Risk' split (a genuine methodology difference in the "
              "Bank's first Pillar 3 report - its 4 category rows sum directly to the Total with no operational "
              "risk charge shown at all), not a transcription omission.",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources(),
    first_col_width=54,
    source_height=170,
    unit_suffix=" (£)",
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio excluding claims on central banks", {
        "FY2024": "21.2%", "FY2023": "55.6%", "FY2022": "99.97%", "FY2021": "91.82%",
    })],
    p3_sources(),
    note="FY2021's own Pillar 3 report does not show the 'claims on central banks excluded, capped at "
         "level of liabilities' adjustment line that appears in every later year's reconciliation table "
         "- its 91.82% is computed on Total Balance Sheet Exposures with no such exclusion applied, a "
         "genuine methodology basis break in the Bank's first reporting year, not a transcription choice.",
)
metric(
    "LCR", "%",
    [("Liquidity coverage ratio", {
        "FY2024": "758%", "FY2023": "4248%", "FY2022": "12926%", "FY2021": "13333%",
    })],
    p3_sources(
        "Note: FY2022's own contemporaneous Pillar 3 report (Table 9) shows a materially different, "
        "much larger LCR of 258,343% for the 31 Dec 2022 quarter alone, apparently using a shorter/"
        "different averaging window than the full-year methodology used in the FY2023 report's own "
        "FY2022 comparative (12,926%, used here). Both the Bank's own FY2021 and FY2022 narrative "
        "sections explicitly caveat that these ratios are 'not representative' during the mobilisation "
        "phase, when the Bank held only small testing-purpose deposit balances - flagged here rather "
        "than silently reconciled.\n"
    ),
    note="Extreme ratios throughout (up to 13,333%) reflect the Bank's own explicit narrative that these "
         "are not representative during its early mobilisation/deposit-ramp phase - genuine per the "
         "source, not a transcription error.",
)
metric(
    "NSFR", "%",
    [("Net stable funding ratio", {"FY2024": "4522%", "FY2023": "5272%", "FY2022": "493%"})],
    p3_sources(),
    note="Not disclosed for FY2021 - the Bank's FY2021 Pillar 3 report discloses no NSFR table at all "
         "(only LCR), confirmed genuinely absent rather than an access gap.",
)

bw.add_not_disclosed_metric_sheets(["MREL Ratio"], sources_text=p3_sources())

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2024": 975341830, "FY2023": 873918457, "FY2022": 25711779, "FY2021": 10408112}),
        ("Loans and advances to customers", {"FY2024": 16140896, "FY2023": 2278905, "FY2022": 10446}),
        ("Customer accounts", {"FY2024": 965804257, "FY2023": 854820499, "FY2022": 1243492}),
        ("Total equity", {"FY2024": 7327982, "FY2023": 14288553, "FY2022": 22428333, "FY2021": 9557149}),
    ],
    balance_sheet_unit="£",
    income_statement_totals=[
        ("Total income", {"FY2024": 10358977, "FY2023": 6228849, "FY2022": 166205, "FY2021": -263132}),
        ("Total administrative expenses", {
            "FY2024": -28614771, "FY2023": -34096226, "FY2022": -16483305, "FY2021": -8801526,
        }),
        ("Loss for the financial year", {
            "FY2024": -19224388, "FY2023": -26848007, "FY2022": -14851675, "FY2021": -7692810,
        }),
    ],
    income_statement_unit="£",
    equity_changes_totals=[
        ("Opening equity", {"FY2024": 13429696, "FY2023": 22428333, "FY2022": 9557149, "FY2021": -1406912}),
        ("Loss for the year", {
            "FY2024": -19224388, "FY2023": -26848007, "FY2022": -14851675, "FY2021": -7692810,
        }),
        ("Other equity movements, net", {
            "FY2024": 13122674, "FY2023": 18708227, "FY2022": 27722859, "FY2021": 18656871,
        }),
        ("Closing equity", {"FY2024": 7327982, "FY2023": 14288553, "FY2022": 22428333, "FY2021": 9557149}),
    ],
    equity_changes_unit="£",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {
            "FY2024": 74846269, "FY2023": 826459821, "FY2022": -14398035, "FY2021": -7435887,
        }),
        ("Net cash from/(used in) investing activities", {
            "FY2024": -15265, "FY2023": 9716757, "FY2022": -10126462, "FY2021": -70707,
        }),
        ("Net cash from financing activities", {
            "FY2024": 12508985, "FY2023": 17947749, "FY2022": 27268402, "FY2021": 15064176,
        }),
        ("Cash at end of year", {
            "FY2024": 953099412, "FY2023": 865759423, "FY2022": 11635096, "FY2021": 8891191,
        }),
    ],
    cash_flow_unit="£",
    ratios=[
        ("CET1 Ratio", {"FY2024": "24.0%", "FY2023": "46.6%", "FY2022": "93.18%", "FY2021": "287.76%"}),
        ("Tier 1 Ratio", {"FY2024": "24.0%", "FY2023": "46.6%", "FY2022": "93.18%", "FY2021": "287.76%"}),
        ("Total Capital Ratio", {"FY2024": "24.0%", "FY2023": "46.6%", "FY2022": "93.18%", "FY2021": "287.76%"}),
        ("Leverage Ratio", {"FY2024": "21.2%", "FY2023": "55.6%", "FY2022": "99.97%", "FY2021": "91.82%"}),
        ("LCR", {"FY2024": "758%", "FY2023": "4248%", "FY2022": "12926%", "FY2021": "13333%"}),
        ("NSFR", {"FY2024": "4522%", "FY2023": "5272%", "FY2022": "493%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's "
         "own source citation for the underlying document/page. Only 4 years shown - no FY2025 Annual "
         "Report or Pillar 3 report has been published yet. That was re-checked on 18 September 2026 by "
         "four independent routes (the Bank's own two index pages, a direct probe of the 2025 filenames "
         "with a live-URL control, Companies House, and a Wayback sweep of the whole domain including the "
         "staging host); Kroo's FY2025 accounts are not due until 30 September 2026 and it has filed on "
         "the deadline in every one of its four years, so October 2026 is when to look again. See the "
         "entity note on any detail sheet for the full evidence.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/KROO BANK FINANCIALS.xlsx")
