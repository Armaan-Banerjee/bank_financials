import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Entity was named "Belmont Green Finance Limited" (trading as Vida/Vida
# Homeloans) through FY2023, renamed "Vida Bank Limited" on receiving its PRA
# banking licence 19 Nov 2024. FY2022 cash flow is a genuine gap - see
# ENTITY_NOTE. Pillar 3 only exists from FY2024 (first year as a bank).
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://www.vidabank.co.uk/media/pkmnxlqg/annual-report-and-accounts-2025-company.pdf"
AR2024_URL = "https://www.vidabank.co.uk/media/emghy4z2/annual-report-and-accounts-2024-company.pdf"
AR2023_URL = "https://www.vidabank.co.uk/media/zhoj0swe/annual-report-and-accounts-2023.pdf"
AR2021_URL = "https://www.vidabank.co.uk/media/p3wau0ms/annual-report-and-accounts-2021.pdf"

P3_2025_URL = "https://www.vidabank.co.uk/media/od2lpxc0/vghl-pillar-3-report-2025-final.pdf"
P3_2024_URL = "https://www.vidabank.co.uk/media/mucbqgwi/vghl-pillar-3-report-2024-final.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: the company (FRN 738741, Companies House 09837692) was named 'Belmont Green Finance Limited' "
    "(trading as Vida / Vida Homeloans) through its FY2023 Annual Report, and was renamed 'Vida Bank Limited' after "
    "receiving its PRA banking licence on 19 November 2024. This workbook uses 'Vida Bank Limited' throughout since "
    "that is its current name. Pre-authorisation (FY2021-FY2023), the business was funded mainly through mortgage "
    "securitisation (numerous 'Tower Bridge Funding' special-purpose vehicles) rather than retail deposits; the "
    "FY2023 Annual Report's own commentary describes the business as still 'preparing for the banking licence'. "
    "Cash flow figures below are on the Company's own (non-consolidated/solo) basis in every populated year - this "
    "is the only basis for which a full three-part cash flow statement (operating/investing/financing) could be "
    "found in every report; the Consolidated (Group) statement of financial position was reported each year, but "
    "the FY2022 and FY2023 Annual Reports' own primary financial statements do not include a full Group cash flow "
    "statement, only a partial 'Net cash flow from operating activities' reconciliation note (Note 25) on the Group "
    "basis - see FY2022_GAP_NOTE below."
)

FY2022_GAP_NOTE = (
    "FY2022 is blank on this sheet: neither the FY2022 nor FY2023 Annual Report presents a full three-part Company "
    f"cash flow statement for FY2022 (checked both directly - {AR2023_URL} - and via the FY2023 report's own prior-"
    "year comparative column, which is likewise not present.) The FY2023 Annual Report's Note 25 gives only a "
    "partial Group-basis operating reconciliation ending at 'Net cash flows from operating activities: £68,297k' "
    "for FY2022 - not on the same (Company) basis as every other populated year here and with no investing/"
    "financing breakdown at all, so it is not shown rather than presented as a misleadingly partial column."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Vida Bank Limited's own Company (non-consolidated) cash flow statement, £'000:\n"
    f"FY2025: Vida Bank Limited Annual Report and Accounts 2025 (Company), p.55 (Statement of Cash Flows) - "
    f"{AR2025_URL}\n"
    f"FY2024: Vida Bank Limited Annual Report and Accounts 2024 (Company), p.73 (Statement of Cash Flows) - "
    f"{AR2024_URL}\n"
    f"FY2023: taken from Vida Bank Limited's FY2024 Annual Report's own FY2023 comparative column (p.73, same "
    f"document as above) - Belmont Green Finance Limited's own FY2023 Annual Report does not present a comparable "
    f"Company-basis statement (see ENTITY_NOTE/FY2022_GAP_NOTE).\n"
    f"FY2021: Belmont Green Finance Limited (Vida) Annual Report and Accounts 2021, p.150 (Company Statement of "
    f"Cash Flows) - {AR2021_URL}\n\n"
    + ENTITY_NOTE + "\n\n" + FY2022_GAP_NOTE
)


def p3_sources():
    return (
        "Sources - Vida Group Holdings Limited/plc Pillar 3 disclosures (Table 3.1 KM1 - Key Metrics; the smallest "
        "regulatory group Vida Bank Limited is consolidated into - no Vida-Bank-Limited-only Pillar 3 disclosure is "
        "separately published):\n"
        f"FY2025: Vida Group Holdings plc Pillar 3 Disclosures 2025, p.5 (3.1 Key Metrics / Table KM1) - {P3_2025_URL}\n"
        f"FY2024: Vida Group Holdings Limited Pillar 3 Disclosures 2024, p.5 (3.1 Key Metrics / Table KM1) - {P3_2024_URL}\n"
        "No Pillar 3 disclosure exists for FY2021-FY2023: Pillar 3 only applies once PRA-authorised as a deposit-"
        "taker, which happened 19 November 2024 (see ENTITY_NOTE on the Cash Flow Statement sheet)."
    )


bw = BankWorkbook(bank_name="Vida Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="6E2C00")

STATEMENTS_ENTITY_NOTE = (
    "Balance Sheet / Statement of Changes in Equity are on Vida Bank Limited's own Company (non-consolidated) "
    "basis in every year, matching the Cash Flow Statement sheet's basis (see its own ENTITY_NOTE). Profit & Loss "
    "is on the Company basis for FY2025/FY2024 only (Vida's own Company Statement of Comprehensive Income exists "
    "for those two years); for FY2023/FY2022/FY2021, the Company took the section 408 Companies Act 2006 "
    "exemption and published no separate Company income statement (only a one-line narrative profit/loss-after-tax "
    "figure, which ties to the equity ladder's own movement for that year), so the Group/Consolidated income "
    "statement is shown instead for those 3 years - a genuine basis difference, not forced to a single basis."
)

BALANCE_SHEET_SOURCES = (
    "Sources - Vida Bank Limited's own Company (non-consolidated) Statement of Financial Position, £'000:\n"
    f"FY2025: Vida Bank Limited Annual Report and Accounts 2025 (Company), p.53 - {AR2025_URL}\n"
    f"FY2024: Vida Bank Limited Annual Report and Accounts 2024 (Company), p.71 - {AR2024_URL}\n"
    f"FY2023: Belmont Green Finance Limited Annual Report and Accounts 2023, p.185 (Company Statement of "
    f"Financial Position) - {AR2023_URL}\n"
    f"FY2022: taken from the FY2023 Annual Report's own restated FY2022 comparative column (same document/page "
    f"as above) - Belmont Green's own FY2022 Annual Report was not fetched this session.\n"
    f"FY2021: Belmont Green Finance Limited Annual Report and Accounts 2021, p.149 (Company Statement of "
    f"Financial Position) - {AR2021_URL}\n\n"
    + STATEMENTS_ENTITY_NOTE
)

INCOME_STATEMENT_SOURCES = (
    "Sources - £'000. FY2025/FY2024: Vida Bank Limited's own Company Statement of Comprehensive Income. "
    "FY2023/FY2022/FY2021: Group/Consolidated Statement of Profit and Loss and Other Comprehensive Income "
    "(Company P&L exempted under s.408, see ENTITY_NOTE below):\n"
    f"FY2025: Vida Bank Limited Annual Report and Accounts 2025 (Company), p.52 - {AR2025_URL}\n"
    f"FY2024: Vida Bank Limited Annual Report and Accounts 2025 (Company), p.52, FY2024 comparative column - "
    f"{AR2025_URL}\n"
    f"FY2023: Belmont Green Finance Limited Annual Report and Accounts 2023, p.143 (Consolidated Statement of "
    f"Profit and Loss and Other Comprehensive Income) - {AR2023_URL}\n"
    f"FY2022: taken from the FY2023 Annual Report's own FY2022 comparative column (same document/page as above).\n"
    f"FY2021: Belmont Green Finance Limited Annual Report and Accounts 2021, p.109 (Consolidated Statement of "
    f"Comprehensive Income) - {AR2021_URL}\n\n"
    "Presentation notes (not silently reconciled): FY2021's Group statement labels its operating-income subtotal "
    "\"Total income\" rather than FY2022-25's \"Net operating income\" - same position in the statement, different "
    "label, reproduced as printed. FY2025's own Statement of Comprehensive Income prints its final row as \"Total "
    "other comprehensive profit\" with a value of 12,699 - this is actually the year's Total comprehensive income "
    "(Profit after tax 13,097 less the 3 OCI items above it, -21-98-279=-398, gives exactly 12,699); the source's "
    "own row label is internally inconsistent (a subtotal, not \"other\" comprehensive income), so this row is "
    "relabelled \"Total comprehensive income for the year, net of tax\" here to match the other 4 years' own "
    "correctly-labelled totals - the £'000 value itself is reproduced exactly as printed, unchanged.\n\n"
    + STATEMENTS_ENTITY_NOTE
)

EQUITY_SOURCES = (
    "Sources - Vida Bank Limited's own Company (non-consolidated) Statement of Changes in Equity, £'000:\n"
    f"FY2021 boundary (1 Jan 2021 opening, FY2021 movements, 31 Dec 2021 closing): Belmont Green Finance Limited "
    f"Annual Report and Accounts 2021, p.150 - {AR2021_URL}\n"
    f"FY2022 boundary: Belmont Green Finance Limited Annual Report and Accounts 2023, p.184 (FY2022 comparative "
    f"rows) - {AR2023_URL}\n"
    f"FY2023 boundary: same document, p.184 - {AR2023_URL}\n"
    f"FY2024 boundary: Vida Bank Limited Annual Report and Accounts 2024, p.72 - {AR2024_URL}\n"
    f"FY2025 boundary: Vida Bank Limited Annual Report and Accounts 2025 (Company), p.54 - {AR2025_URL}\n\n"
    "Discrepancy flagged, not forced to tie: the FY2024 Annual Report's own opening balance at 1 January 2024 "
    "(share capital 204,463 / total equity 122,070) differs by £1k from the FY2023 Annual Report's own closing "
    "balance at 31 December 2023 (share capital 204,462 / total equity 122,069) - a genuine £1k rounding artefact "
    "between the two source documents, each reproduced exactly as its own report states.\n\n"
    "The FY2025 Statement of Changes in Equity's own \"Total comprehensive income\" subtotal row is omitted from "
    "this ladder: it prints running balances (not that year's movement) in its Retained earnings and Total "
    "columns - see the Profit & Loss sheet's own source note for the same issue on that sheet. Every individual "
    "movement row above it (Profit for the year, Deferred tax on Gilts, Fair value through OCI reserve, Amounts "
    "deferred to cash flow hedge reserve) is reproduced in full and the ladder ties exactly without it.\n\n"
    + STATEMENTS_ENTITY_NOTE
)

ASSET_QUALITY_SOURCES = (
    "Sources - Vida Bank Limited's own IFRS 9 stage disclosure (Note 13/14, \"Expected credit losses\"), £'000, "
    "on a Group/Consolidated basis (the only basis at which this note is disclosed in every source document; "
    "gross/net loan totals below therefore don't tie exactly to the Balance Sheet sheet's Company-basis \"Loans "
    "to customers\" line - a genuine basis difference, documented not blended):\n"
    f"FY2025/FY2024: Vida Bank Limited Annual Report and Accounts 2025, p.79-81 (Note 14, Expected credit "
    f"losses) - {AR2025_URL}\n"
    f"FY2023/FY2022: Belmont Green Finance Limited Annual Report and Accounts 2023, p.168-169 (Note 14, Expected "
    f"credit losses) - {AR2023_URL}\n"
    f"FY2021: Belmont Green Finance Limited Annual Report and Accounts 2021, p.132-133 (Note 13, Expected credit "
    f"losses) - {AR2021_URL}\n\n"
    "NPL ratio = Stage 3 gross balance / Total gross balance. Coverage ratio = Stage 3 impairment provision / "
    "Stage 3 gross balance. Both derived, not separately disclosed by the Bank."
)


def rwa_not_disclosed_note():
    return (
        "No UK OV1 (RWA-by-risk-category) template, or equivalent RWA breakdown table, exists in either Pillar 3 "
        "Disclosures document (2025 or 2024) checked this session - both are short (9-page) documents covering "
        "only the KM1 Key Metrics table already used on the other Pillar 3 sheets. Confirmed non-disclosure, not "
        "an access gap. No Pillar 3 disclosure exists at all for FY2021-FY2023 (see ENTITY_NOTE on the Cash Flow "
        "Statement sheet)."
    )


# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents", {"FY2025": 254874, "FY2024": 143485, "FY2023": 17161, "FY2022": 14919, "FY2021": 13500}),
    ("DATA", "Debt securities", {"FY2025": 819770, "FY2024": 34135}),
    ("DATA", "Loans to customers", {"FY2025": 2301831, "FY2024": 1866006, "FY2023": 1712271, "FY2022": 1761996, "FY2021": 1811577}),
    ("DATA", "Derivative financial instruments", {"FY2025": 10198, "FY2024": 2123, "FY2022": 731}),
    ("DATA", "Other receivables", {"FY2025": 71715, "FY2024": 16412, "FY2023": 34000, "FY2022": 13982, "FY2021": 11399}),
    ("DATA", "Deferred taxation asset", {"FY2025": 15299, "FY2024": 13565, "FY2023": 13565, "FY2022": 13565, "FY2021": 12975}),
    ("DATA", "Investment in subsidiaries", {}),
    ("DATA", "Property, plant and equipment", {"FY2025": 1343, "FY2024": 1551, "FY2023": 401, "FY2022": 965, "FY2021": 2407}),
    ("DATA", "Intangible assets", {"FY2025": 1316, "FY2024": 2190, "FY2023": 2704, "FY2022": 2837, "FY2021": 2408}),
    ("DATA", "Corporation tax", {"FY2022": 25}),
    ("TOTAL", "Total assets", {"FY2025": 3476346, "FY2024": 2079467, "FY2023": 1780102, "FY2022": 1809020, "FY2021": 1854266}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Retail deposits", {"FY2025": 2425702, "FY2024": 173113}),
    ("DATA", "Amounts owed to credit institutions", {"FY2025": 40345, "FY2024": 74254, "FY2023": 44437, "FY2022": 15188, "FY2021": 15336}),
    ("DATA", "Deemed loan due to Group undertakings", {"FY2025": 767720, "FY2024": 1659540, "FY2023": 1544083, "FY2022": 1606178, "FY2021": 1690865}),
    ("DATA", "Derivative financial liabilities", {"FY2025": 19403, "FY2024": 184, "FY2023": 4727}),
    ("DATA", "Other liabilities", {"FY2025": 44269, "FY2024": 7067, "FY2023": 64722, "FY2022": 56584, "FY2021": 21050}),
    ("DATA", "Provisions", {"FY2023": 64, "FY2022": 64, "FY2021": 374}),
    ("DATA", "Corporation tax", {"FY2025": 1128, "FY2024": 229}),
    ("TOTAL", "Total liabilities", {"FY2025": 3298567, "FY2024": 1914387, "FY2023": 1658033, "FY2022": 1678014, "FY2021": 1727625}),
    ("SECTION", "Shareholders' equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 36156, "FY2024": 241039, "FY2023": 204462, "FY2022": 204462, "FY2021": 204462}),
    ("DATA", "Other reserves", {"FY2025": -398}),
    ("DATA", "Retained profit/(losses)", {"FY2025": 142021, "FY2024": -75959, "FY2023": -82393, "FY2022": -73456, "FY2021": -77821}),
    ("TOTAL", "Total shareholders' equity", {"FY2025": 177779, "FY2024": 165080, "FY2023": 122069, "FY2022": 131006, "FY2021": 126641}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 3476346, "FY2024": 2079467, "FY2023": 1780102, "FY2022": 1809020, "FY2021": 1854266}),
]

bw.add_balance_sheet_sheet(
    title="Vida Bank Limited — Company Statement of Financial Position",
    subtitle="Company (non-consolidated) basis, £'000.",
    rows=bs_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=60,
    source_height=180,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income and similar income", {"FY2025": 171518, "FY2024": 121718, "FY2023": 144373, "FY2022": 99941, "FY2021": 68551}),
    ("DATA", "Interest expense and similar charges", {"FY2025": -124229, "FY2024": -87898, "FY2023": -110660, "FY2022": -57037, "FY2021": -34046}),
    ("TOTAL", "Net interest income", {"FY2025": 47289, "FY2024": 33820, "FY2023": 33713, "FY2022": 42904, "FY2021": 34505}),
    ("DATA", "Other operating income/(expense)", {"FY2025": 7035, "FY2024": 1158, "FY2023": 920, "FY2022": -6174, "FY2021": 987}),
    ("DATA", "Net fair value gain/(loss) on financial instruments", {"FY2025": 3331, "FY2024": 6045, "FY2023": 3903, "FY2022": -706, "FY2021": -1404}),
    ("TOTAL", "Net operating income", {"FY2025": 57655, "FY2024": 41023, "FY2023": 38536, "FY2022": 36024, "FY2021": 34088}),
    ("DATA", "Administrative expenses", {"FY2025": -42450, "FY2024": -34231, "FY2023": -32438, "FY2022": -35502, "FY2021": -30932}),
    ("TOTAL", "Operating profit before impairment", {"FY2025": 15205, "FY2024": 6792, "FY2023": 6098, "FY2022": 522, "FY2021": 3156}),
    ("DATA", "Provisions", {"FY2023": 0, "FY2022": 310, "FY2021": 223}),
    ("DATA", "Impairment (losses)/releases", {"FY2025": -2736, "FY2024": -128, "FY2023": -55, "FY2022": 543, "FY2021": -725}),
    ("TOTAL", "Profit before taxation", {"FY2025": 12469, "FY2024": 6664, "FY2023": 6043, "FY2022": 1375, "FY2021": 2654}),
    ("DATA", "Tax credit/(charge) for the year", {"FY2025": 628, "FY2024": -230, "FY2023": 25, "FY2022": 609, "FY2021": 2005}),
    ("TOTAL", "Profit for the year", {"FY2025": 13097, "FY2024": 6434, "FY2023": 6068, "FY2022": 1984, "FY2021": 4659}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Cash flow hedge reserve (losses)/gains", {"FY2025": -21, "FY2024": 0, "FY2023": -10468, "FY2022": 16864, "FY2021": 0}),
    ("DATA", "Tax on items in other comprehensive income", {"FY2025": -98}),
    ("DATA", "Fair value through OCI reserve", {"FY2025": -279}),
    ("TOTAL", "Total comprehensive income/(loss) for the year, net of tax", {"FY2025": 12699, "FY2024": 6434, "FY2023": -4400, "FY2022": 18848, "FY2021": 4659}),
]

bw.add_income_statement_sheet(
    title="Vida Bank Limited — Statement of Comprehensive Income",
    subtitle="FY2025/FY2024: Company basis. FY2023-FY2021: Group/Consolidated basis (Company P&L exempted under s.408). £'000.",
    rows=pl_rows,
    sources_text=INCOME_STATEMENT_SOURCES,
    first_col_width=64,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
equity_headers = ["Called up share capital", "Retained earnings", "Other reserves", "Total"]
equity_rows = [
    ("TOTAL", "Balance at 1 January 2021", (196162, -71916, None, 124246)),
    ("DATA", "Share issuance", (8300, None, None, 8300)),
    ("DATA", "Loss for the year", (None, -5905, None, -5905)),
    ("TOTAL", "Balance at 31 December 2021", (204462, -77821, None, 126641)),
    ("DATA", "Profit for the year", (None, 4365, None, 4365)),
    ("TOTAL", "Balance at 31 December 2022", (204462, -73456, None, 131006)),
    ("DATA", "Loss for the year", (None, -8937, None, -8937)),
    ("TOTAL", "Balance at 31 December 2023", (204462, -82393, None, 122069)),
    ("TOTAL", "Balance at 1 January 2024 (per FY2024 Annual Report - see source note)", (204463, -82393, None, 122070)),
    ("DATA", "Profit for the year", (None, 6434, None, 6434)),
    ("DATA", "Share issuance", (36576, None, None, 36576)),
    ("TOTAL", "Balance at 31 December 2024", (241039, -75959, None, 165080)),
    ("DATA", "Profit for the year", (None, 13097, None, 13097)),
    ("DATA", "Deferred tax on Gilts", (None, None, -98, -98)),
    ("DATA", "Fair value through OCI reserve", (None, None, -279, -279)),
    ("DATA", "Amounts deferred to cash flow hedge reserve, net of tax", (None, None, -21, -21)),
    ("DATA", "Share capital reallocation", (-204883, 204883, None, 0)),
    ("TOTAL", "Balance at 31 December 2025", (36156, 142021, -398, 177779)),
]

bw.add_equity_changes_sheet(
    title="Vida Bank Limited — Company Statement of Changes in Equity",
    subtitle="Company (non-consolidated) basis, £'000. Chronological, oldest to newest.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=EQUITY_SOURCES,
    first_col_width=56,
    source_height=260,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("TOTAL", "Net cash flows from/(used in) operating activities", {"FY2025": 1766849, "FY2024": 70662, "FY2023": 65493, "FY2021": -179449}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -92, "FY2024": -57, "FY2023": -24, "FY2021": -190}),
    ("DATA", "Expenditure on software development", {"FY2025": -12, "FY2024": -351, "FY2023": -674, "FY2021": -1567}),
    ("TOTAL", "Net cash flows from/(used in) investing activities", {"FY2025": -104, "FY2024": -408, "FY2023": -698, "FY2021": -1757}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Proceeds from shares issued", {"FY2021": 8300}),
    ("DATA", "Movement of deemed loans due to Group undertakings", {"FY2025": -904243, "FY2024": 115457, "FY2023": -62096, "FY2021": 169705}),
    ("DATA", "Repayment of loans", {"FY2024": -25000}),
    ("DATA", "Issuance of Tier 2 subordinated liabilities", {"FY2025": 35000}),
    ("DATA", "Repayment of lease liabilities", {"FY2025": -479, "FY2024": -225, "FY2023": -446, "FY2021": -1407}),
    ("DATA", "Movement in debt securities", {"FY2025": -785634, "FY2024": -34135}),
    ("DATA", "Other movements", {"FY2025": 0, "FY2024": -27, "FY2023": -12}),
    ("TOTAL", "Net cash flows (used in)/generated from financing activities", {"FY2025": -1655356, "FY2024": 56070, "FY2023": -62554, "FY2021": 176598}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 111389, "FY2024": 126324, "FY2023": 2241, "FY2021": -4608}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {"FY2025": 143485, "FY2024": 17161, "FY2023": 14920, "FY2021": 18108}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2025": 254874, "FY2024": 143485, "FY2023": 17161, "FY2021": 13500}),
]

bw.add_cash_flow_sheet(
    title="Vida Bank Limited — Company Cash Flow Statement",
    subtitle="Company (non-consolidated) basis, £'000. FY2022 blank - see source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=68,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
aq_rows = [
    ("SECTION", "Gross loans to customers by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (performing)", {"FY2025": 1915462, "FY2024": 1463371, "FY2023": 1254493, "FY2022": 1041635, "FY2021": 1124656}),
    ("DATA", "Stage 2 (underperforming)", {"FY2025": 321347, "FY2024": 330053, "FY2023": 392712, "FY2022": 662983, "FY2021": 643597}),
    ("DATA", "Stage 3 (non-performing)", {"FY2025": 65403, "FY2024": 63782, "FY2023": 51849, "FY2022": 45129, "FY2021": 44090}),
    ("TOTAL", "Total gross loans to customers", {"FY2025": 2302212, "FY2024": 1857206, "FY2023": 1699054, "FY2022": 1749747, "FY2021": 1812343}),
    ("SECTION", "Impairment provision (ECL) by IFRS 9 stage", {}),
    ("DATA", "Stage 1 provision", {"FY2025": 1671, "FY2024": 1053, "FY2023": 1105, "FY2022": 647, "FY2021": 1217}),
    ("DATA", "Stage 2 provision", {"FY2025": 1555, "FY2024": 1341, "FY2023": 1885, "FY2022": 3443, "FY2021": 3889}),
    ("DATA", "Stage 3 provision", {"FY2025": 3865, "FY2024": 2480, "FY2023": 2599, "FY2022": 1835, "FY2021": 2541}),
    ("TOTAL", "Total impairment provision", {"FY2025": 7091, "FY2024": 4874, "FY2023": 5589, "FY2022": 5925, "FY2021": 7647}),
    ("SECTION", "Derived ratios", {}),
    ("DATA", "NPL ratio (Stage 3 / Total gross loans)", {"FY2025": "2.84%", "FY2024": "3.43%", "FY2023": "3.05%", "FY2022": "2.58%", "FY2021": "2.43%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 provision / Stage 3 gross)", {"FY2025": "5.91%", "FY2024": "3.89%", "FY2023": "5.01%", "FY2022": "4.07%", "FY2021": "5.77%"}),
]

bw.add_asset_quality_sheet(
    title="Vida Bank Limited — Asset Quality",
    subtitle="Group/Consolidated basis (see source note), £'000.",
    rows=aq_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=64,
    source_height=200,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, f"Vida Group Holdings basis, {unit}" if unit else "Vida Group Holdings basis",
                         rows_data, p3_sources(), note=note, first_col_width=48, source_height=130)


metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", {"FY2025": 168319, "FY2024": 160316})])
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "15.2%", "FY2024": "16.2%"})])
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", {"FY2025": 168319, "FY2024": 160316})],
       note="Equal to CET1 capital in both years - Vida has no Additional Tier 1 (AT1) instruments.")
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {"FY2025": "15.2%", "FY2024": "16.2%"})])
metric("Total Capital", "£'000", [("Total capital", {"FY2025": 202429, "FY2024": 160316})],
       note="FY2025 total capital exceeds Tier 1 capital because the Group issued £35m of qualifying Tier 2 capital "
            "during the year to support planned balance sheet expansion; FY2024 had no Tier 2 capital.")
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2025": "18.3%", "FY2024": "16.2%"})])
metric("Total RWAs", "£'000", [("Total risk-weighted exposure amount", {"FY2025": 1105780, "FY2024": 986809})])
bw.add_rwa_breakdown_sheet(
    title="Vida Bank Limited — RWA Breakdown",
    subtitle="Vida Group Holdings basis",
    rows=[("DATA", "RWA Breakdown", {y: "Not publicly disclosed" for y in YEARS})],
    sources_text=rwa_not_disclosed_note(),
    first_col_width=54,
    source_height=120,
    unit_suffix="",
)
metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Total exposure measure excluding claims on central banks", {"FY2025": 3440332, "FY2024": 2331835}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "4.9%", "FY2024": "6.9%"}),
    ],
)
metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value (average)", {"FY2025": 1073005, "FY2024": 167705}),
        ("Total net cash outflows, adjusted value", {"FY2025": 669438, "FY2024": 16046}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "163%", "FY2024": "1,045%"}),
    ],
    note="FY2024's very high LCR (1,045%) reflects a build-up of liquid assets immediately following PRA "
         "authorisation on 19 November 2024, per the Group's own Pillar 3 commentary.",
)
metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding", {"FY2025": 2377496, "FY2024": 2016146}),
        ("Total required stable funding", {"FY2025": 1719626, "FY2024": 1830180}),
        ("Net Stable Funding Ratio (%)", {"FY2025": "138%", "FY2024": "110%"}),
    ],
)
metric("MREL Ratio", None, [("MREL ratio", {y: "Not disclosed" for y in YEARS})],
       note="No MREL disclosure (numeric or qualitative) found in either Pillar 3 report - Vida is a small, "
            "recently-authorised bank and does not appear to be within scope of an MREL-above-minimum-capital "
            "requirement based on its own disclosures.")

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 3476346, "FY2024": 2079467, "FY2023": 1780102, "FY2022": 1809020, "FY2021": 1854266}),
        ("Loans to customers", {"FY2025": 2301831, "FY2024": 1866006, "FY2023": 1712271, "FY2022": 1761996, "FY2021": 1811577}),
        ("Retail deposits", {"FY2025": 2425702, "FY2024": 173113}),
        ("Total shareholders' equity", {"FY2025": 177779, "FY2024": 165080, "FY2023": 122069, "FY2022": 131006, "FY2021": 126641}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net operating income", {"FY2025": 57655, "FY2024": 41023, "FY2023": 38536, "FY2022": 36024, "FY2021": 34088}),
        ("Administrative expenses", {"FY2025": -42450, "FY2024": -34231, "FY2023": -32438, "FY2022": -35502, "FY2021": -30932}),
        ("Profit for the year", {"FY2025": 13097, "FY2024": 6434, "FY2023": 6068, "FY2022": 1984, "FY2021": 4659}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 165080, "FY2024": 122070, "FY2023": 131006, "FY2022": 126641, "FY2021": 124246}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": 12699, "FY2024": 6434, "FY2023": -8937, "FY2022": 4365, "FY2021": -5905}),
        ("Other equity movements, net", {"FY2025": 0, "FY2024": 36576, "FY2023": 0, "FY2022": 0, "FY2021": 8300}),
        ("Closing equity", {"FY2025": 177779, "FY2024": 165080, "FY2023": 122069, "FY2022": 131006, "FY2021": 126641}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 1766849, "FY2024": 70662, "FY2023": 65493, "FY2021": -179449}),
        ("Net cash from/(used in) investing activities", {"FY2025": -104, "FY2024": -408, "FY2023": -698, "FY2021": -1757}),
        ("Net cash from/(used in) financing activities", {"FY2025": -1655356, "FY2024": 56070, "FY2023": -62554, "FY2021": 176598}),
        ("Cash and cash equivalents at end of year", {"FY2025": 254874, "FY2024": 143485, "FY2023": 17161, "FY2021": 13500}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "15.2%", "FY2024": "16.2%"}),
        ("Tier 1 Ratio", {"FY2025": "15.2%", "FY2024": "16.2%"}),
        ("Total Capital Ratio", {"FY2025": "18.3%", "FY2024": "16.2%"}),
        ("Leverage Ratio", {"FY2025": "4.9%", "FY2024": "6.9%"}),
        ("LCR", {"FY2025": "163%", "FY2024": "1,045%"}),
        ("NSFR", {"FY2025": "138%", "FY2024": "110%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. FY2022 cash flow and FY2021-FY2023 Pillar 3 are blank - Vida "
         "only became a PRA-authorised bank on 19 November 2024 (no Pillar 3 exists before then), and FY2022's own "
         "Annual Report doesn't present a full cash flow statement on a basis comparable to other years - see the "
         "Cash Flow Statement sheet's source note for details.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/VIDA FINANCIALS.xlsx")
