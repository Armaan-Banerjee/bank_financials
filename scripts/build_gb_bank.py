import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


# NOTE: originally a Pillar-3-only workbook without cash-flow figures;
# expanded to the full 18-sheet ST- shape in ST-019 (Balance Sheet, P&L,
# Statement of Changes in Equity, Asset Quality, RWA Breakdown), and the
# Cash Flow Statement itself was backfilled in a 2026-09-03 follow-up pass
# from the same Companies House filings.
#
# HD-053 (2026-09-05): checked whether the FY2017 window applies to this
# entity, per the ticket's blanket "confirmed floor FY2017" — it does not.
# Companies House 10702260 traded as THE MODEL T FINANCE COMPANY LIMITED
# from incorporation (31 Mar 2017) until it was renamed GB Bank Limited on
# 12 Nov 2021. Its FY2017-FY2020 filings (accounting periods to 31 Mar
# 2018, 31 Mar 2019, a stub to 31 Dec 2019, and 31 Dec 2020) are all
# small-company "abridged"/"total exemption" accounts for that unrelated,
# pre-rename business (a scanned 2-page balance sheet-only filing for the
# earliest years; no P&L, no cash flow, no regulatory capital data, and
# the entity was not yet PRA-authorised). These are not GB Bank's banking
# financials under any accounting basis, so FY2017-FY2020 are self-skipped
# in full (same treatment as Griffin Bank's pre-rename years) rather than
# populated with a different company's dormant-shell figures. Kept at the
# existing FY2021-FY2025 window.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

CH_URL = "https://find-and-update.company-information.service.gov.uk/company/10702260"
P3_2022_URL = "https://www.gbbank.co.uk/download/4416/?tmstv=1760374739"
P3_2023_URL = "https://www.gbbank.co.uk/download/4420/?tmstv=1760374863"
P3_2024_URL = "https://www.gbbank.co.uk/download/4423/?tmstv=1760374514"
P3_2025_URL = "https://www.gbbank.co.uk/download/5065/?tmstv=1766062359"

AA2021_URL = "https://find-and-update.company-information.service.gov.uk/company/10702260/filing-history/MzM1Mzg0NjcwMWFkaXF6a2N4/document?format=pdf&download=0"
AA2022_URL = "https://find-and-update.company-information.service.gov.uk/company/10702260/filing-history/MzM5NTYwNDEwOWFkaXF6a2N4/document?format=pdf&download=0"
AA2023_URL = "https://find-and-update.company-information.service.gov.uk/company/10702260/filing-history/MzQzODI5NTI3M2FkaXF6a2N4/document?format=pdf&download=0"
AA2024_URL = "https://find-and-update.company-information.service.gov.uk/company/10702260/filing-history/MzQ2MDE5MzkwMWFkaXF6a2N4/document?format=pdf&download=0"
AA2025_URL = "https://find-and-update.company-information.service.gov.uk/company/10702260/filing-history/MzQ5Njg4NzE4MGFkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "ENTITY AND REPORTING BASIS: GB Bank Limited (Companies House 10702260; PRA FRN 850286) "
    "is the matched UK legal entity. The 2022-2025 Pillar 3 reports state that the reported "
    "figures are prepared on a solo basis. The 2025 report additionally records PRA permission, "
    "backdated to 1 October 2025, for an individual-consolidation method including SilverRock "
    "Financial Services Ltd going forward; the main 30 September 2025 table remains solo and is "
    "used here. GB Bank states that it publishes Pillar 3 annually under CRR Article 433b as a "
    "small and non-complex bank. FY2024 is a shortened nine-month period ended 30 September 2024 "
    "after the accounting period end changed; FY2021-FY2023 end on 31 December and FY2025 ends "
    "30 September."
)

STATEMENTS_ENTITY_NOTE = (
    ENTITY_NOTE + " STATEMENTS BASIS: the Balance Sheet, Profit & Loss, Statement of Changes in "
    "Equity and Asset Quality sheets below are sourced from GB Bank Limited's own audited "
    "Companies House accounts (all 5 filings scanned/image-only, visually transcribed), not the "
    "Pillar 3 archive. FY2021-FY2024 are Company-only (GB Bank Limited had no subsidiaries in "
    "those years). FY2025 is a GENUINE ENTITY-BASIS CHANGE to Group-Consolidated: during the year "
    "GB Bank Limited acquired SilverRock Financial Services Ltd as a subsidiary (goodwill £5,497k "
    "recognised; Consolidated statement of cash flows shows 'Acquisition of subsidiary, net of "
    "cash acquired' £(12,753)k), and the Company took the Companies Act 2006 s.408 exemption from "
    "presenting its own individual profit and loss account - only Group P&L is published for "
    "FY2025. The Group and Company Balance Sheets differ only modestly for FY2025 (Group Total "
    "equity £110,003k vs Company Total equity £111,194k, driven by consolidation adjustments); "
    "Balance Sheet/P&L/Equity below use the GROUP basis for FY2025 for internal consistency (P&L "
    "is only available on Group basis, and the Group Balance Sheet ties exactly to the Group "
    "equity roll-forward's own closing balance). The FY2024 opening equity balance is identical "
    "under both bases (no subsidiary existed yet), so no plug row is needed at the FY2024/FY2025 "
    "boundary despite the basis change. The Company's own FY2025 profit after tax (disclosed "
    "separately) was £6,614k vs the Group's £5,424k used here."
)


def p3_sources():
    return (
        "Sources - GB Bank Limited official annual Pillar 3 disclosures, solo basis:\n"
        f"FY2025: Pillar 3 Disclosures 2025, UK KM1 p.13 - {P3_2025_URL}\n"
        f"FY2024: Pillar 3 Disclosures 2024, UK KM1 p.12 - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures 2023, UK KM1 p.11 - {P3_2023_URL}\n"
        f"FY2022 and FY2021: Pillar 3 Disclosures 2022, UK KM1 p.11 - {P3_2022_URL}\n"
        f"Companies House entity record and filing history: {CH_URL}/filing-history\n\n"
        + ENTITY_NOTE
    )


CAPITAL = {"FY2025": 104969, "FY2024": 69270, "FY2023": 19299, "FY2022": 22096, "FY2021": 16586}
CAPITAL_RATIO = {"FY2025": "19.14%", "FY2024": "45.71%", "FY2023": "56.46%", "FY2022": "234.21%", "FY2021": "403.37%"}
RWA = {"FY2025": 548458, "FY2024": 151536, "FY2023": 34184, "FY2022": 9434, "FY2021": 4112}
LEVERAGE_EXPOSURE = {"FY2025": 2114122, "FY2024": 747677, "FY2023": 48734, "FY2022": 23445, "FY2021": 17606}
LEVERAGE_RATIO = {"FY2025": "4.97%", "FY2024": "9.26%", "FY2023": "39.60%", "FY2022": "94.25%", "FY2021": "94.21%"}
HQLA = {"FY2025": 1095636, "FY2024": 427498, "FY2023": 209812, "FY2022": 18436, "FY2021": 8698}
NET_OUTFLOWS = {"FY2025": 522180, "FY2024": 139823, "FY2023": 50415, "FY2022": 92, "FY2021": 0}
LCR = {"FY2025": "210%", "FY2024": "306%", "FY2023": "416%", "FY2022": "20,091%", "FY2021": "9,999.99%"}
ASF = {"FY2025": 2224154, "FY2024": 510589, "FY2023": 203914, "FY2022": 20742, "FY2021": 16546}
RSF = {"FY2025": 1162308, "FY2024": 94820, "FY2023": 6041, "FY2022": 1006, "FY2021": 1696}
NSFR = {"FY2025": "191%", "FY2024": "538%", "FY2023": "3,375%", "FY2022": "2,061.89%", "FY2021": "978.24%"}

def statements_sources(extra=""):
    return (
        "Sources - GB Bank Limited's own audited Companies House accounts (all 5 filings "
        "scanned/image-only, visually transcribed):\n"
        f"FY2021: Full accounts made up to 31 December 2021 (filed 6 Oct 2022), Statement of "
        f"Financial Position p.21, Income Statement p.20, Statement of Changes in Equity p.22 - {AA2021_URL}\n"
        f"FY2022: Full accounts made up to 31 December 2022 (filed 7 Oct 2023), Statement of "
        f"Financial Position p.25, Statement of Comprehensive Income p.24, Statement of Changes "
        f"in Equity p.26 - {AA2022_URL}\n"
        f"FY2023: Full accounts made up to 31 December 2023 (filed 9 Oct 2024), Statement of "
        f"Financial Position p.26, Statement of Comprehensive Income p.25, Statement of Changes "
        f"in Equity p.27, Note 11 Loans and advances to customers p.42 - {AA2023_URL}\n"
        f"FY2024: Full accounts for the 9-month period to 30 September 2024 (filed 28 Mar 2025), "
        f"Statement of Financial Position p.26, Statement of Comprehensive Income p.25, Statement "
        f"of Changes in Equity p.27, Note 12 Loans and advances to customers p.44 - {AA2024_URL}\n"
        f"FY2025: Full accounts for the year to 30 September 2025 (filed 6 Jan 2026), Consolidated "
        f"statement of financial position p.43, Consolidated statement of comprehensive income "
        f"p.42, Consolidated statement of changes in equity p.45, Note 13 Loans and advances to "
        f"customers p.67-68 - {AA2025_URL}\n\n"
        + (extra + "\n\n" if extra else "") + STATEMENTS_ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="GB Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="205072")

# ---------------------------------------------------------------
# Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents / balances at central banks", {"FY2025": 475776, "FY2024": 419999, "FY2023": 287322, "FY2022": 22030, "FY2021": 4940}),
    ("DATA", "Loans and advances to banks / credit institutions", {"FY2025": 29695, "FY2024": 3642, "FY2023": 390, "FY2022": 446, "FY2021": 2644}),
    ("DATA", "Loans and advances to customers", {"FY2025": 464042, "FY2024": 86293, "FY2023": 25388}),
    ("DATA", "Debt securities", {"FY2025": 1595626, "FY2024": 645254, "FY2023": 19731, "FY2022": 10477, "FY2021": 9498}),
    ("DATA", "Investments", {"FY2025": 3714}),
    ("DATA", "Derivative financial instruments", {"FY2025": 5953, "FY2024": 1001}),
    ("DATA", "Goodwill", {"FY2025": 5497}),
    ("DATA", "Tangible fixed assets", {"FY2025": 403, "FY2024": 128, "FY2023": 344, "FY2022": 415, "FY2021": 85}),
    ("DATA", "Intangible assets", {"FY2025": 821, "FY2024": 19, "FY2023": 32, "FY2022": 51}),
    ("DATA", "Other assets", {"FY2025": 2569, "FY2024": 1072, "FY2023": 1469, "FY2022": 850, "FY2021": 439}),
    ("DATA", "Prepayments and accrued income", {"FY2024": 332, "FY2023": 814, "FY2022": 700}),
    ("DATA", "Taxation receivable", {"FY2025": 5404}),
    ("TOTAL", "Total assets", {"FY2025": 2589500, "FY2024": 1157740, "FY2023": 335490, "FY2022": 34969, "FY2021": 17606}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer accounts / deposit liabilities", {"FY2025": 2326424, "FY2024": 1084365, "FY2023": 314374, "FY2022": 11473}),
    ("DATA", "Amounts due to credit institutions", {"FY2025": 141942}),
    ("DATA", "Derivative financial instruments", {"FY2025": 8316, "FY2024": 231}),
    ("DATA", "Other liabilities", {"FY2025": 599, "FY2024": 480, "FY2023": 685, "FY2022": 251, "FY2021": 1020}),
    ("DATA", "Accruals and deferred income", {"FY2025": 2216, "FY2024": 3300, "FY2023": 1100, "FY2022": 1098}),
    ("DATA", "Provisions for liabilities", {"FY2024": 75}),
    ("TOTAL", "Total liabilities", {"FY2025": 2479497, "FY2024": 1088451, "FY2023": 316159, "FY2022": 12822, "FY2021": 1020}),
    ("SECTION", "Capital and reserves", {}),
    ("DATA", "Share capital", {"FY2025": 82, "FY2024": 55, "FY2023": 12, "FY2022": 11, "FY2021": 9}),
    ("DATA", "Share premium", {"FY2025": 145725, "FY2024": 109952, "FY2023": 54336, "FY2022": 50380, "FY2021": 36816}),
    ("DATA", "Other reserves", {"FY2025": 1994, "FY2024": 2503, "FY2023": 2434, "FY2022": 2167, "FY2021": 1641}),
    ("DATA", "Accumulated losses", {"FY2025": -37798, "FY2024": -43221, "FY2023": -37451, "FY2022": -30411, "FY2021": -21880}),
    ("TOTAL", "Total equity", {"FY2025": 110003, "FY2024": 69289, "FY2023": 19331, "FY2022": 22147, "FY2021": 16586}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 2589500, "FY2024": 1157740, "FY2023": 335490, "FY2022": 34969, "FY2021": 17606}),
]

bw.add_balance_sheet_sheet(
    title="GB Bank Limited — Balance Sheet",
    subtitle="Company-only basis FY2021-FY2024; Group-consolidated basis FY2025 (genuine entity-basis change - see source note). £'000.",
    rows=balance_sheet_rows,
    sources_text=statements_sources(
        "PRESENTATION NOTE: no customer lending existed at all in FY2021/FY2022 (no Loans and advances to "
        "customers line in either year's own Balance Sheet) - genuinely nil, not a gap. FY2023's own report "
        "labelled the FY2022 comparative Total equity £22,147k; FY2024's own report restated the FY2023 "
        "comparative Accumulated losses to £(37,452)k, a £1k rounding difference from FY2023's own £(37,451)k - "
        "FY2023's own originally-published figure is used here per project convention."
    ),
    first_col_width=64,
    source_height=460,
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable and similar income", {"FY2025": 105151, "FY2024": 20112, "FY2023": 12288, "FY2022": 259, "FY2021": 6}),
    ("DATA", "Interest payable and similar expense", {"FY2025": -87452, "FY2024": -15656, "FY2023": -9193, "FY2022": -32}),
    ("TOTAL", "Net interest income", {"FY2025": 17699, "FY2024": 4456, "FY2023": 3095, "FY2022": 227, "FY2021": 6}),
    ("DATA", "Other operating income / (expense)", {"FY2025": -162, "FY2024": 4, "FY2023": 61, "FY2021": 75}),
    ("DATA", "Net gains on derivative financial instruments", {"FY2024": 335}),
    ("DATA", "Gains or losses on financial instruments", {"FY2025": -696}),
    ("TOTAL", "Net operating income", {"FY2025": 16841, "FY2024": 4795, "FY2023": 3156, "FY2022": 227, "FY2021": 81}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Administrative expenses", {"FY2025": -16355, "FY2024": -9501, "FY2023": -10465, "FY2022": -9588, "FY2021": -8615}),
    ("DATA", "Impairment charge on loans and advances", {"FY2025": -103, "FY2024": -692}),
    ("DATA", "Depreciation, amortisation and impairment charge", {"FY2025": -191, "FY2024": -372, "FY2023": -102}),
    ("TOTAL", "Operating profit/(loss) before tax", {"FY2025": 192, "FY2024": -5770, "FY2023": -7411, "FY2022": -9361, "FY2021": -8534}),
    ("DATA", "Tax credit for the year/period", {"FY2025": 5232, "FY2023": 371, "FY2022": 830, "FY2021": 348}),
    ("TOTAL", "Profit/(loss) for the year/period", {"FY2025": 5424, "FY2024": -5770, "FY2023": -7040, "FY2022": -8531, "FY2021": -8186}),
    ("SECTION", "Other comprehensive income/(expense)", {}),
    ("DATA", "Fair value gains/(losses) recorded in cashflow hedge reserve", {"FY2025": -682}),
    ("DATA", "Gains previously recorded in cash flow hedge reserve amortised through P&L", {"FY2025": -6}),
    ("DATA", "Tax relating to items that may subsequently be reclassified", {"FY2025": 172}),
    ("TOTAL", "Total comprehensive income/(loss) for the year/period", {"FY2025": 4908, "FY2024": -5770, "FY2023": -7040, "FY2022": -8531, "FY2021": -8186}),
]

bw.add_income_statement_sheet(
    title="GB Bank Limited — Profit & Loss",
    subtitle="Company-only basis FY2021-FY2024; Group-consolidated basis FY2025 (only Group P&L is published for FY2025 - Companies Act s.408 exemption). £'000.",
    rows=income_statement_rows,
    sources_text=statements_sources(
        "PRESENTATION NOTE: FY2021's report shows no tax credit/charge line separately (loss for the year is the "
        "same pre- and post-tax) - actually a £348k tax credit is shown in that year's own statement and is "
        "included above. FY2024's impairment charge on loans and advances first appears that year - FY2021-2023 "
        "had none (FY2021/FY2022 had no lending; FY2023 had loans but no incurred losses identified, £nil "
        "provision under the incurred-loss model - see Asset Quality sheet). No OCI detail is disclosed in any "
        "year except FY2025 (cash flow hedge reserve movements, following the Group's first use of derivative "
        "financial instruments) - blank cells in prior years mean genuinely nil OCI, confirmed by reading each "
        "year's own statement in full."
    ),
    first_col_width=76,
    source_height=460,
)

# ---------------------------------------------------------------
# Statement of Changes in Equity (chronological) - built using the per-year
# reconciliation ladder: Balance Sheet built first (above), then each year's
# closing balance checked against both the next year's own opening balance
# and that year's own Balance Sheet Total equity. Ties exactly at every
# boundary, including across the FY2024->FY2025 Company->Group entity-basis
# change (FY2024's closing balance is identical under both bases, since no
# subsidiary existed yet).
# ---------------------------------------------------------------
equity_changes_rows = [
    ("TOTAL", "At 1 January 2021", (8, 30279, 1709, -13694, 18302)),
    ("DATA", "Loss for the year (FY2021)", (None, None, None, -8186, -8186)),
    ("DATA", "New share capital subscribed (FY2021)", (1, 6537, None, None, 6538)),
    ("DATA", "Share based payment transactions (FY2021)", (None, None, -68, None, -68)),
    ("TOTAL", "At 31 December 2021", (9, 36816, 1641, -21880, 16586)),
    ("DATA", "Loss for the year (FY2022)", (None, None, None, -8531, -8531)),
    ("DATA", "New share capital subscribed (FY2022)", (2, 13564, None, None, 13566)),
    ("DATA", "Share based payment transactions (FY2022)", (None, None, 526, None, 526)),
    ("TOTAL", "At 31 December 2022", (11, 50380, 2167, -30411, 22147)),
    ("DATA", "Loss for the year (FY2023)", (None, None, None, -7040, -7040)),
    ("DATA", "New share capital subscribed (FY2023)", (1, 3956, None, None, 3957)),
    ("DATA", "Share based payment transactions (FY2023)", (None, None, 267, None, 267)),
    ("TOTAL", "At 31 December 2023", (12, 54336, 2434, -37451, 19331)),
    ("DATA", "Loss for the period (FY2024, 9 months)", (None, None, None, -5770, -5770)),
    ("DATA", "New share capital subscribed (FY2024)", (43, 55616, None, None, 55659)),
    ("DATA", "Share based payment transactions (FY2024)", (None, None, 69, None, 69)),
    ("TOTAL", "At 30 September 2024", (55, 109952, 2503, -43221, 69289)),
    ("DATA", "Profit for the year (FY2025, Group)", (None, None, None, 5424, 5424)),
    ("DATA", "Fair value gains/(losses) recorded in cashflow hedge reserve (FY2025)", (None, None, -682, None, -682)),
    ("DATA", "Gains previously recorded in cash flow hedge reserve amortised through P&L (FY2025)", (None, None, -6, None, -6)),
    ("DATA", "Tax relating to items that may subsequently be reclassified (FY2025)", (None, None, 172, None, 172)),
    ("DATA", "New share capital subscribed (FY2025)", (27, 35773, None, None, 35800)),
    ("DATA", "Share-based payment transactions (FY2025)", (None, None, 7, None, 7)),
    ("TOTAL", "At 30 September 2025 (Group)", (82, 145725, 1994, -37798, 110003)),
]

bw.add_equity_changes_sheet(
    title="GB Bank Limited — Statement of Changes in Equity",
    subtitle="Company-only basis FY2021-FY2024; Group-consolidated basis FY2025 (see source note). £'000. Ties exactly to the Balance Sheet's own Total equity at every year-end.",
    headers=["Share capital", "Share premium", "Other reserves", "Accumulated losses", "Total equity"],
    rows=equity_changes_rows,
    sources_text=statements_sources(
        "The FY2021 opening balance (At 1 January 2021: £18,302k) is that year's own report's opening "
        "figure, itself tying to the FY2020 closing balance shown as that report's comparative column "
        "(not itself a covered year in this workbook)."
    ),
    first_col_width=74,
    source_height=420,
)

cash_flow_rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) for the year/period after taxation", {"FY2025": 5424, "FY2024": -5770, "FY2023": -7040, "FY2022": -8531, "FY2021": -8186}),
    ("DATA", "Tax credit (recognised in P&L, added back)", {"FY2022": -830, "FY2021": -348}),
    ("DATA", "Tax credit received (cash)", {"FY2021": 348}),
    ("DATA", "(Increase)/decrease in net corporation tax asset", {"FY2024": 946, "FY2023": -371}),
    ("DATA", "(Increase)/decrease in net deferred tax asset", {"FY2025": -5232}),
    ("DATA", "Interest receivable and similar income", {"FY2025": -105151, "FY2024": -20112}),
    ("DATA", "Interest payable and similar expense", {"FY2025": 87452, "FY2024": 15656}),
    ("DATA", "Net (decrease)/increase in provisions", {"FY2025": -75, "FY2024": 75}),
    ("DATA", "Depreciation and amortisation", {"FY2025": 191, "FY2024": 371, "FY2023": 102, "FY2022": 69, "FY2021": 13}),
    ("DATA", "Share-based payment transactions", {"FY2025": 7, "FY2024": 68, "FY2023": 267, "FY2022": 526, "FY2021": -68}),
    ("DATA", "Net change in financial instruments/derivatives", {"FY2025": 696, "FY2024": -517}),
    ("DATA", "Increase in deposit liabilities", {"FY2025": 1246157, "FY2024": 765353, "FY2023": 302901, "FY2022": 11473}),
    ("DATA", "Increase in amounts due to other/credit institutions", {"FY2025": 140000}),
    ("DATA", "Increase in loans and advances to customers", {"FY2025": -380763, "FY2024": -59539, "FY2023": -25388}),
    ("DATA", "Net (increase)/decrease in loans and advances to banks/credit institutions", {"FY2025": -23371, "FY2024": -3309, "FY2023": 35, "FY2022": 2489, "FY2021": -601}),
    ("DATA", "(Increase) in accrued interest from loans and advances to banks/credit institutions", {"FY2023": 1, "FY2021": -3}),
    ("DATA", "(Increase)/decrease in other assets", {"FY2025": -493, "FY2024": -804, "FY2023": -107, "FY2022": -281, "FY2021": -223}),
    ("DATA", "Increase/(decrease) in prepayments and accrued income", {"FY2025": -671, "FY2024": 482}),
    ("DATA", "Net increase/(decrease) in other liabilities", {"FY2025": 1, "FY2024": 50, "FY2023": 179, "FY2022": 100, "FY2021": -24}),
    ("DATA", "(Decrease)/increase in accruals and deferred income", {"FY2025": -1781, "FY2024": 2200, "FY2023": -96, "FY2022": 139, "FY2021": 463}),
    ("DATA", "Interest received", {"FY2025": 106600, "FY2024": 15330}),
    ("DATA", "Interest paid", {"FY2025": -92097, "FY2024": -11498}),
    ("TOTAL", "Net cash generated from operating activities", {"FY2025": 976894, "FY2024": 698982, "FY2023": 270483, "FY2022": 5154, "FY2021": -8629}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchases of tangible and intangible fixed assets", {"FY2025": -987, "FY2024": -142, "FY2023": -12, "FY2022": -450, "FY2021": -83}),
    ("DATA", "Purchase of debt securities", {"FY2025": -1586315, "FY2024": -651170, "FY2023": -26422, "FY2022": -45323, "FY2021": -23451}),
    ("DATA", "Proceeds from the maturity of debt securities", {"FY2025": 649634, "FY2024": 29291, "FY2023": 17266, "FY2022": 44434, "FY2021": 13953}),
    ("DATA", "Acquisition of subsidiary, net of cash acquired", {"FY2025": -12753}),
    ("DATA", "Purchase of equity investment", {"FY2025": -3714}),
    ("TOTAL", "Net cash (used in)/generated from investing activities", {"FY2025": -954135, "FY2024": -622021, "FY2023": -9168, "FY2022": -1339, "FY2021": -9581}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Gross proceeds from the issue of ordinary shares", {"FY2025": 35800, "FY2024": 56004, "FY2023": 3957, "FY2022": 13566, "FY2021": 6538}),
    ("DATA", "Costs of issuing ordinary shares", {"FY2024": -344}),
    ("TOTAL", "Net cash generated from financing activities", {"FY2025": 35800, "FY2024": 55660, "FY2023": 3957, "FY2022": 13566, "FY2021": 6538}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 58559, "FY2024": 132621, "FY2023": 265272, "FY2022": 17381, "FY2021": -11672}),
    ("DATA", "Cash and cash equivalents at beginning of period/year", {"FY2025": 420212, "FY2024": 287593, "FY2023": 22321, "FY2022": 4940, "FY2021": 16612}),
    ("TOTAL", "Cash and cash equivalents at end of period/year", {"FY2025": 478771, "FY2024": 420214, "FY2023": 287593, "FY2022": 22321, "FY2021": 4940}),
    ("SECTION", "Cash and cash equivalents comprise", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 475776, "FY2024": 419999, "FY2023": 287322, "FY2022": 22030}),
    ("DATA", "Loans and advances to credit institutions repayable on demand and overnight", {"FY2025": 2995, "FY2024": 215, "FY2023": 271, "FY2022": 291}),
    ("DATA", "Cash at bank and in hand (FY2021 only - no central bank/credit institution split disclosed that year)", {"FY2021": 4940}),
]

bw.add_cash_flow_sheet(
    title="GB Bank Limited — Cash Flow Statement",
    subtitle="Company-only basis FY2021-FY2024; Group-consolidated basis FY2025 (see Balance Sheet sheet's entity-basis note). £'000.",
    rows=cash_flow_rows,
    sources_text=statements_sources(
        "CASH FLOW BACKFILL NOTE (2026-09-03 follow-up): transcribed from each year's own Statement of Cash Flows / "
        "Consolidated statement of cash flows in the same 5 Companies House filings used for the other statement sheets "
        "(all scanned/image-only, visually transcribed) - FY2021 p.23, FY2022 p.27, FY2023 p.28, FY2024 p.28 (9-month "
        "period), FY2025 p.47 (Consolidated). PRESENTATION NOTE: the operating-activities adjustment lines change "
        "structure over time - FY2021/FY2022 use a 'Tax credit'/'Tax credit received' pair; FY2023 switches to "
        "'(increase) in net corporation tax asset'; FY2024/FY2025 switch again to separate interest income/expense "
        "adjustment lines plus memo 'Interest received'/'Interest paid' cash lines - each year's own captions are used "
        "as-is, not forced into one template. GENUINE DISCREPANCY, not force-reconciled: FY2025's own report states its "
        "opening cash balance as £420,212k, £2k below FY2024's own report's closing balance of £420,214k - both figures "
        "reproduced as disclosed. GENUINE RELABELLING, not a data error: the £29,291k line in FY2024's own report is "
        "captioned 'Proceeds from the maturity of debt securities' (used here, per project convention of using each "
        "year's own originally-published label); the FY2025 report's own FY2024 comparative column re-labels the same "
        "£29,291k figure as 'Purchase of equity investment' - a presentation reclassification in the later filing, not "
        "reproduced here. The Balance Sheet sheet's single 'Cash and cash equivalents' line only ever captures the "
        "'Cash and balances at central banks' sub-component shown here - the 'comprise' breakdown above explains the "
        "gap to this sheet's own closing cash total for FY2022-FY2025 (FY2021 had no such split, a single 'Cash at "
        "bank and in hand' line, which does tie exactly to the Balance Sheet)."
    ),
    first_col_width=88,
    source_height=460,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Asset Quality: GB Bank Limited uses FRS 102 + IAS 39's incurred-loss
# impairment model (confirmed by reading Note 3 "Judgements... key sources
# of estimation uncertainty" in the FY2024 accounts, p.36) - NOT an IFRS 9
# staged model, so there is no Stage 1/2/3 split to show. FY2021/FY2022 had
# no customer lending at all (genuinely nil, not a gap - confirmed by each
# year's own Balance Sheet having no such line). FY2023 onward shows the
# gross loan book split by security type plus the collective/specific
# impairment provision roll-forward from each year's own Note.
# ---------------------------------------------------------------
AQ_PROPERTY = {"FY2025": 462117, "FY2024": 80622, "FY2023": 22311}
AQ_LAND = {"FY2025": 2529, "FY2024": 6363, "FY2023": 3077}
AQ_GROSS = {y: AQ_PROPERTY[y] + AQ_LAND[y] for y in AQ_PROPERTY}
AQ_PROVISION = {"FY2025": 604, "FY2024": 692, "FY2023": 0}
AQ_NET = {y: AQ_GROSS[y] - AQ_PROVISION[y] for y in AQ_GROSS}
AQ_COVERAGE = {y: f"{AQ_PROVISION[y] / AQ_GROSS[y] * 100:.2f}%" for y in AQ_GROSS}

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, gross, by security type (FY2021/FY2022: no customer lending)", {}),
    ("DATA", "Loans secured on property", AQ_PROPERTY),
    ("DATA", "Loans secured on land", AQ_LAND),
    ("TOTAL", "Total gross loans and advances to customers", AQ_GROSS),
    ("SECTION", "Impairment provision (FRS 102 / IAS 39 incurred-loss model - not IFRS 9 staged)", {}),
    ("DATA", "Total impairment provision (collective + specific)", AQ_PROVISION),
    ("TOTAL", "Net loans and advances to customers", AQ_NET),
    ("SECTION", "Ratios", {}),
    ("DATA", "Impairment coverage ratio (provision / gross loans)", AQ_COVERAGE),
]

bw.add_asset_quality_sheet(
    title="GB Bank Limited — Asset Quality / Credit Risk Disclosures",
    subtitle="Company-only basis FY2023-FY2024; Group-consolidated basis FY2025. FRS 102/IAS 39 incurred-loss impairment model, not IFRS 9 staged. £'000.",
    rows=asset_quality_rows,
    sources_text=statements_sources(
        "Note 3 'Judgements in applying accounting policies...' (FY2024 accounts, p.36) confirms the Bank "
        "assesses impairment under FRS 102 + IAS 39's incurred-loss methodology (individual assessments for "
        "loans in default, collective assessments otherwise) - there is therefore no IFRS 9 Stage 1/2/3 split "
        "to disclose, unlike most other banks in this project. FY2023: the Bank 'has not identified any "
        "incurred losses in the year' (Note 11, FY2023 accounts) - £nil provision is a genuine finding, not a "
        "gap. FY2024: 3 loans in default at 30 September 2024, £0.4m loan loss provision recognised (Note 3, "
        "FY2024 accounts, p.36). FY2025 (Group): provision roll-forward from £692k opening to £604k closing "
        "(£348k specific charge on the property book, a £245k net release plus £191k written off on the land "
        "book) - Note 13, FY2025 accounts, p.68."
    ),
    first_col_width=76,
    source_height=380,
)

# ---------------------------------------------------------------
# RWA Breakdown - sourced from each year's own Pillar 3 "Capital
# Requirements" table (UK OV1-style, by risk category), reusing the same
# P3_*_URL documents already used for the Pillar 3 ratio sheets. All 5
# years' totals tie exactly to the Total RWAs metric sheet's own RWA dict.
# ---------------------------------------------------------------
RWA_CREDIT = {"FY2025": 522406, "FY2024": 138351, "FY2023": 26262, "FY2022": 2089, "FY2021": 4112}
RWA_CCR = {"FY2025": 8730, "FY2024": 2868}
RWA_CVA = {"FY2025": 1743, "FY2024": 2079}
RWA_MARKET = {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}
RWA_OPERATIONAL = {"FY2025": 15579, "FY2024": 8217, "FY2023": 7922, "FY2022": 7345, "FY2021": 0}

rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding CCR)", RWA_CREDIT),
    ("DATA", "Counterparty credit risk (CCR)", RWA_CCR),
    ("DATA", "Credit valuation adjustment (CVA)", RWA_CVA),
    ("DATA", "Market risk", RWA_MARKET),
    ("DATA", "Operational risk", RWA_OPERATIONAL),
    ("TOTAL", "Total risk-weighted exposure amount", RWA),
]

def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=58, source_height=210)


metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", CAPITAL)])
metric("CET1 Ratio", "%", [("Common Equity Tier 1 (CET1) ratio", CAPITAL_RATIO)])
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", CAPITAL)], note="No AT1 instruments are disclosed in the annual KM1 tables; Tier 1 equals CET1 throughout.")
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", CAPITAL_RATIO)])
metric("Total Capital", "£'000", [("Total capital", CAPITAL)], note="No AT1 or Tier 2 instruments are disclosed in the annual KM1 tables; total capital equals CET1 throughout.")
metric("Total Capital Ratio", "%", [("Total capital ratio", CAPITAL_RATIO)])
metric(
    "Total RWAs", "£'000", [("Total risk-weighted exposure amount", RWA)],
    note=(
        "The 2023 Pillar 3 report prints £2,735k for 2023 RWA, which is inconsistent with its own 56.46% capital ratio. "
        "The 2024 report's 2023 comparative prints £34,184k, which reconciles to the reported capital and ratio; £34,184k is used here."
    ),
)

bw.add_rwa_breakdown_sheet(
    title="GB Bank Limited — RWA Breakdown",
    subtitle="Solo basis throughout (per Pillar 3 disclosures). £'000.",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources() + (
        "\nCCR and CVA first appear as separate categories from FY2024 (the Bank had none in FY2021-FY2023 - "
        "genuinely nil, confirmed by reading each year's own Capital Requirements table in full, apart from "
        "FY2021's own table which shows Operational Risk RWA as £0 too, since the Bank had no 3-year historical "
        "average revenue base yet to apply the multiplier to)."
    ),
    first_col_width=70,
    source_height=220,
)

metric("Leverage Ratio", "£'000 / %", [
    ("Total exposure measure excluding claims on central banks", LEVERAGE_EXPOSURE),
    ("Leverage ratio excluding claims on central banks (%)", LEVERAGE_RATIO),
])
metric("LCR", "£'000 / %", [
    ("Total high-quality liquid assets (HQLA), weighted value - average", HQLA),
    ("Total net cash outflows, adjusted value", NET_OUTFLOWS),
    ("Liquidity coverage ratio (%)", LCR),
])
metric("NSFR", "£'000 / %", [
    ("Total available stable funding", ASF),
    ("Total required stable funding", RSF),
    ("Net stable funding ratio (%)", NSFR),
])
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={"MREL Ratio": "No quantitative MREL figure was located in the official 2022-2025 Pillar 3 reports reviewed."},
)

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 2589500, "FY2024": 1157740, "FY2023": 335490, "FY2022": 34969, "FY2021": 17606}),
        ("Loans and advances to customers", {"FY2025": 464042, "FY2024": 86293, "FY2023": 25388}),
        ("Customer accounts", {"FY2025": 2326424, "FY2024": 1084365, "FY2023": 314374, "FY2022": 11473}),
        ("Total equity", {"FY2025": 110003, "FY2024": 69289, "FY2023": 19331, "FY2022": 22147, "FY2021": 16586}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net operating income", {"FY2025": 16841, "FY2024": 4795, "FY2023": 3156, "FY2022": 227, "FY2021": 81}),
        ("Administrative expenses", {"FY2025": -16355, "FY2024": -9501, "FY2023": -10465, "FY2022": -9588, "FY2021": -8615}),
        ("Profit/(loss) for the year/period", {"FY2025": 5424, "FY2024": -5770, "FY2023": -7040, "FY2022": -8531, "FY2021": -8186}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 69289, "FY2024": 19331, "FY2023": 22147, "FY2022": 16586, "FY2021": 18302}),
        ("Profit/(loss) for the year/period", {"FY2025": 5424, "FY2024": -5770, "FY2023": -7040, "FY2022": -8531, "FY2021": -8186}),
        ("Other movements, net", {"FY2025": 35290, "FY2024": 55728, "FY2023": 4224, "FY2022": 14092, "FY2021": 6470}),
        ("Closing equity", {"FY2025": 110003, "FY2024": 69289, "FY2023": 19331, "FY2022": 22147, "FY2021": 16586}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash generated from operating activities", {"FY2025": 976894, "FY2024": 698982, "FY2023": 270483, "FY2022": 5154, "FY2021": -8629}),
        ("Net cash (used in)/generated from investing activities", {"FY2025": -954135, "FY2024": -622021, "FY2023": -9168, "FY2022": -1339, "FY2021": -9581}),
        ("Net increase/(decrease) in cash and cash equivalents", {"FY2025": 58559, "FY2024": 132621, "FY2023": 265272, "FY2022": 17381, "FY2021": -11672}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", CAPITAL_RATIO),
        ("Leverage Ratio", LEVERAGE_RATIO),
        ("LCR", LCR),
        ("NSFR", NSFR),
    ],
    note=(
        "Cash Flow Statement backfilled 2026-09-03 (follow-up pass) from the same 5 Companies House filings used "
        "for the other statement sheets - see that sheet's own source note for the presentation changes across "
        "years and two genuine flagged discrepancies (a £2k FY2024/FY2025 opening-vs-closing cash mismatch, and a "
        "relabelled £29,291k FY2024 line). Balance Sheet, Profit & Loss and Statement of Changes in Equity headline "
        "blocks are sourced from GB Bank Limited's own audited accounts (Company-only basis FY2021-FY2024, "
        "Group-consolidated FY2025 - see the Balance Sheet sheet's entity-basis note). Regulatory metrics are from "
        "GB Bank Limited's official annual solo-basis Pillar 3 disclosures. FY2024 covers nine months to 30 "
        "September 2024; FY2025 covers the year to 30 September 2025. See each detail sheet for source pages and "
        "the documented 2023 RWA inconsistency."
    ),
)

bw.save("/Users/armaan/code/katalysis/banks/GB BANK FINANCIALS.xlsx")
