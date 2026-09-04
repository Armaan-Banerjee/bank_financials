import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# PILLAR-3-ONLY WORKBOOK: KEXIM Bank (UK) Limited (company 02693038, FRN 204490,
# formerly KEXIM International (U.K.) Limited) is the wholly-owned UK subsidiary of
# the Export-Import Bank of Korea ("KEXIM", the sole shareholder). It takes the FRS
# 101 "presentation of a cash flow statement" disclosure exemption every year -
# confirmed explicitly in Note 2 "Significant accounting policies" of the FY2025
# Annual Report ("As permitted by FRS 101, the Bank has taken advantage of the
# disclosure exemptions available under that standard in relation to ... presentation
# of a cash flow statement ...", with "a statement of cash flows for the period"
# listed as the first bulleted exemption applied). No Contents/statement list in any
# of the 5 filings includes a cash flow statement. Follows the BNY Mellon
# International / ABC International Bank / Bank Mandiri Europe / DB UK Bank
# precedent: 13-sheet Pillar-3-only structure.
#
# No dedicated Pillar 3 document exists for this entity and no reachable bank-owned
# website was found this session (see WEBSITE_NOTE below) - the ONLY capital metric
# disclosed anywhere in the 5 Annual Reports checked is a single combined "Common
# Equity Tier 1 and total capital adequacy ratio" percentage, stated once per report
# in the Strategic Report's "Review of the business" section, with a prior-year
# comparative given each time (independently cross-checked and consistent across all
# 5 consecutive report-pairs - no restatements). No £ CET1/Tier1/Total Capital
# amount, no RWA figure, no Tier 1-vs-CET1 breakdown, no Leverage Ratio, LCR, NSFR or
# MREL Ratio is disclosed anywhere in the Strategic Report, Directors' Report, Risk
# Management notes, or the Notes to the Financial Statements (including Note 27
# "Parent and subsidiary relationships", which only refers the reader to the parent
# Export-Import Bank of Korea's own group accounts, and Note 28, which is an
# unrelated Capital Requirements (Country-by-Country Reporting) Regulations 2013
# disclosure, not a Pillar 3/capital-adequacy note). All 5 Companies House filings
# are fully scanned (image-only, 0 extractable text layer) - transcribed via
# targeted page-image reads, not full-document OCR.

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, calendar year-end (31 December)
YEAR_LABEL = {y: y for y in YEARS}

FY2025_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/02693038/filing-history/MzUzMDYxMTU0N2FkaXF6a2N4/document?format=pdf&download=0"
FY2024_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/02693038/filing-history/MzQ2ODk1NTg1M2FkaXF6a2N4/document?format=pdf&download=0"
FY2023_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/02693038/filing-history/MzQyMzUxMTIzMWFkaXF6a2N4/document?format=pdf&download=0"
FY2022_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/02693038/filing-history/MzM4NTcxODk4NWFkaXF6a2N4/document?format=pdf&download=0"
FY2021_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/02693038/filing-history/MzM0NjA0OTUyMGFkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "ENTITY NOTE: KEXIM Bank (UK) Limited (company 02693038, FRN 204490, incorporated 3 March 1992 as KEXIM "
    "International (U.K.) Limited) is a wholly-owned subsidiary of the Export-Import Bank of Korea (\"the Parent "
    "Bank\"), which is itself 100% owned by the Korean government and is registered in South Korea. The Bank's "
    "principal activity is wholesale banking - providing credit facilities to corporates with a Korean linkage. "
    "All figures below are on the Bank's own entity-level basis, reported in pound Sterling throughout (no FX "
    "conversion needed) - it has no subsidiaries of its own."
)

EXEMPTION_NOTE = (
    "FRS 101 CASH-FLOW EXEMPTION: the FY2025 Annual Report's Note 2 \"Significant accounting policies - Basis of "
    "accounting\" states the financial statements are prepared in accordance with FRS 101 'Reduced Disclosure "
    "Framework' and that the Bank has taken advantage of the available disclosure exemptions, the first bulleted "
    f"item being \"a statement of cash flows for the period\" - KEXIM Bank (UK) Limited Annual Report 2025, p.31 - "
    f"{FY2025_AR_URL}. No cash flow statement appears in any of the 5 filings checked (FY2021-FY2025), consistent "
    "with a standing structural feature of this entity's accounts, not a one-off. Per the project's established "
    "policy for this exemption (see The Bank of New York Mellon (International) Limited / ABC International Bank "
    "plc / Bank Mandiri (Europe) Limited / DB UK Bank Limited), this workbook is built as a PILLAR-3-ONLY variant: "
    "the capital metric that is disclosed is populated below, but no cash flow figures exist to show."
)

CASH_FLOW_SOURCES = ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE

WEBSITE_NOTE = (
    "ACCESS NOTE: the domain keximbank.co.uk (as listed in some directories) resolves to an unrelated Fasthosts "
    "domain-parking page, not the Bank's own site. Two other plausible domains (keximuk.com, kexim.co.uk) either "
    "did not resolve or refused connections this session, and the Wayback Machine returned persistent HTTP 429 "
    "rate-limit responses throughout this session (a known ongoing Internet Archive-side issue also seen on "
    "other tickets in this project - not bank-specific). No standalone Pillar 3 document could therefore be "
    "located this session; worth a revisit with fresh Wayback/WebSearch budget."
)

NOT_DISCLOSED_NOTE = (
    "No dedicated Pillar 3 document is published by this entity that could be located this session (see the "
    "access note on the Cash Flow Statement sheet), and no separate quantitative capital note exists in any of "
    "the 5 Annual Reports checked (FY2021-FY2025) beyond the single combined ratio disclosed on the CET1 Ratio "
    "and Total Capital Ratio sheets - this metric is not disclosed in any form in any of the 5 filings checked, "
    "including Note 27 (which only refers to the Parent Bank's own group accounts) and Note 28 (an unrelated "
    "Country-by-Country Reporting disclosure). CONFIRMED AGAIN during the ST-024 statements build (2026-09-03): "
    "read every note in all 5 Annual Reports in full - impairment/ECL notes (9, 14, 15, 16), off-balance sheet "
    "items (25), fair value measurement, liquidity/interest-rate risk tables, and Note 27 - no RWA figure, no "
    "CET1/Tier 1/Total Capital £ amount, and no capital-management note of any kind exists anywhere. This is a "
    "genuine, thoroughly-checked non-disclosure, not a research gap."
)

STATEMENTS_SOURCES = (
    "Sources - KEXIM Bank (UK) Limited's own audited financial statements (each year's own primary statements, "
    "as originally published - all 5 Companies House filings scanned/image-only, visually transcribed):\n"
    f"FY2025: Annual Report 2025, Profit and loss account p.26, Statement of comprehensive income p.27, Balance "
    f"sheet p.28, Statement of changes in equity p.30 - {FY2025_AR_URL}\n"
    f"FY2024: Annual Report 2024, Profit and loss account p.26, Balance sheet p.28, Statement of changes in "
    f"equity p.30 - {FY2024_AR_URL}\n"
    f"FY2023: Annual Report 2023, Profit and loss account p.26, Balance sheet p.28, Statement of changes in "
    f"equity p.30 - {FY2023_AR_URL}\n"
    f"FY2022: Annual Report 2022, Profit and loss account p.24, Statement of comprehensive income p.25, Balance "
    f"sheet p.26, Statement of changes in equity p.28 - {FY2022_AR_URL}\n"
    f"FY2021: Annual Report 2021, Profit and loss account p.23, Balance sheet p.25, Statement of changes in "
    f"equity p.27 - {FY2021_AR_URL}\n\n"
)

STATEMENTS_PRESENTATION_NOTE = (
    "PRESENTATION NOTE: all figures are the Bank's own whole-pound (not £'000) presentation, GBP throughout - "
    "no FX conversion needed. FY2021's own Balance Sheet uses a current/non-current split (Non-current assets / "
    "Current assets, Creditors due within one year / after more than one year) genuinely different from "
    "FY2022-FY2025's direct Assets/Liabilities/Capital structure - combined here into the same line-item "
    "structure as the later years for comparability (e.g. 'Loans and advances to banks' sums FY2021's own "
    "non-current £23,638,936 + current £11,057,274 = £34,696,210), with the combination verified to tie exactly "
    "to FY2021's own reported Total assets/Total liabilities. Genuine £1 rounding differences exist within "
    "FY2021's own Annual Report between its Balance Sheet's Revaluation reserve/Profit and loss account figures "
    "((341,980) / 15,786,654) and its Statement of Changes in Equity's own closing figures for the same date "
    "((341,981) / 15,786,655) - each sheet below reproduces its own source page's figure as printed, not "
    "force-reconciled. Deferred tax assets/liabilities and Corporation tax receivable/payable lines are shown "
    "only in the years the Bank had a recognised balance - blank cells mean that year's own statement has no "
    "such line, not that the value is unknown."
)


def p3_sources(extra=""):
    return (
        "Sources - KEXIM Bank (UK) Limited, all figures GBP (no FX conversion needed), from each year's own "
        "Companies House full-accounts filing, Strategic Report, 'Review of the business' section:\n"
        f"FY2025: Annual Report 2025, p.3 (\"The Bank's Common Equity Tier 1 and total capital adequacy ratios "
        f"decreased to 20.5% at the end of 2025 (2024: 20.9%)\") - {FY2025_AR_URL}\n"
        f"FY2024: Annual Report 2024, p.3 (\"...has decreased to 20.9% at the end of 2024 (2023: 22.8%)\") - "
        f"{FY2024_AR_URL} (independently cross-checked against the FY2025 report's own FY2024 comparative above - "
        "consistent, no restatement)\n"
        f"FY2023: Annual Report 2023, p.3 (\"...has increased slightly to 22.8% at the end of 2023 (2022: "
        f"22.5%)\") - {FY2023_AR_URL} (cross-checked against the FY2024 report's comparative - consistent)\n"
        f"FY2022: Annual Report 2022, p.3 (\"...has reduced to 22.5% at the end of 2022 (2021: 30%)\") - "
        f"{FY2022_AR_URL} (cross-checked against the FY2023 report's comparative - consistent)\n"
        f"FY2021: Annual Report 2021, p.3 (\"...ratios improved from 13.5% and 18.0% respectively at the end of "
        f"2019, to both being 36.4% at the end of 2020 and 30.0% following the partial deployment of this capital "
        f"by the end of 2021\") - {FY2021_AR_URL} (cross-checked against the FY2022 report's comparative - "
        "consistent). All 5 filings are fully scanned (image-only); figures transcribed via targeted page-image "
        "reads of the Strategic Report's 'Review of the business' section (p.3 in every filing).\n"
        + (extra + "\n" if extra else "")
    )


bw = BankWorkbook(bank_name="KEXIM Bank (UK) Limited", years=YEARS, year_label=YEAR_LABEL, header_color="7A1F2B")

# ---------------------------------------------------------------
# Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents", {"FY2025": 4915304, "FY2024": 10021152, "FY2023": 2688613, "FY2022": 19199889, "FY2021": 6262744}),
    ("DATA", "Financial investments", {"FY2025": 179394842, "FY2024": 181605174, "FY2023": 160938795, "FY2022": 143109644, "FY2021": 119019308}),
    ("DATA", "Debt securities: private placement bonds", {"FY2025": 90653832, "FY2024": 68218209, "FY2023": 72521740, "FY2022": 72526543, "FY2021": 61374708}),
    ("DATA", "Loans and advances to banks", {"FY2025": 55353800, "FY2024": 69952929, "FY2023": 64926885, "FY2022": 64280786, "FY2021": 34696210}),
    ("DATA", "Loans and advances to customers", {"FY2025": 272874882, "FY2024": 255692188, "FY2023": 221939171, "FY2022": 219863026, "FY2021": 162324430}),
    ("DATA", "Prepayments and other receivables", {"FY2025": 113759, "FY2024": 127231, "FY2023": 278605, "FY2022": 43913, "FY2021": 1839029}),
    ("DATA", "Intangible assets", {"FY2025": 91953, "FY2024": 16896, "FY2023": 28234, "FY2022": 61980, "FY2021": 85969}),
    ("DATA", "Tangible fixed assets", {"FY2025": 13991, "FY2024": 7280, "FY2023": 17751, "FY2022": 28945, "FY2021": 42073}),
    ("DATA", "'Right-of-use' asset", {"FY2025": 195759, "FY2024": 352367, "FY2023": 508975, "FY2022": 682036, "FY2021": 844708}),
    ("DATA", "Corporation tax receivable", {"FY2025": 620628}),
    ("DATA", "Deferred tax assets", {"FY2024": 14126, "FY2023": 401909, "FY2022": 1407543, "FY2021": 876}),
    ("TOTAL", "Total assets", {"FY2025": 604228751, "FY2024": 586007552, "FY2023": 524250678, "FY2022": 521204305, "FY2021": 386490055}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Borrowings from credit institutions", {"FY2025": -490903342, "FY2024": -475810294, "FY2023": -418559481, "FY2022": -406105536, "FY2021": -285675937}),
    ("DATA", "Accruals and other liabilities", {"FY2025": -4219189, "FY2024": -4490359, "FY2023": -4071702, "FY2022": -19163045, "FY2021": -3103150}),
    ("DATA", "Provisions for off-balance sheet items", {"FY2025": -61253, "FY2024": -80532, "FY2023": -35410, "FY2022": -3997}),
    ("DATA", "Corporation tax payable", {"FY2024": -548690, "FY2023": -458585, "FY2022": -274868, "FY2021": -155239}),
    ("DATA", "Deferred tax liabilities", {"FY2025": -425834}),
    ("DATA", "Lease liabilities", {"FY2025": -175022, "FY2024": -336374, "FY2023": -495550, "FY2022": -668190, "FY2021": -827158}),
    ("TOTAL", "Total liabilities", {"FY2025": -495784639, "FY2024": -481266249, "FY2023": -423620728, "FY2022": -426215636, "FY2021": -289761484}),
    ("SECTION", "Capital and reserves", {}),
    ("DATA", "Called up share capital", {"FY2025": 81283897, "FY2024": 81283897, "FY2023": 81283897, "FY2022": 81283897, "FY2021": 81283897}),
    ("DATA", "Revaluation reserve", {"FY2025": 1287040, "FY2024": -18375, "FY2023": -1328490, "FY2022": -4604133, "FY2021": -341980}),
    ("DATA", "Profit and loss account", {"FY2025": 25873175, "FY2024": 23475781, "FY2023": 20674543, "FY2022": 18308905, "FY2021": 15786654}),
    ("TOTAL", "Total shareholders' funds", {"FY2025": 108444112, "FY2024": 104741303, "FY2023": 100629950, "FY2022": 94988669, "FY2021": 96728571}),
]

bw.add_balance_sheet_sheet(
    title="KEXIM Bank (UK) Limited — Balance Sheet",
    subtitle="Entity-level basis (Bank has no subsidiaries of its own). Whole £, no FX conversion needed.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES + STATEMENTS_PRESENTATION_NOTE + "\n\n" + ENTITY_NOTE,
    first_col_width=68,
    source_height=420,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 29994776, "FY2024": 30655788, "FY2023": 25325615, "FY2022": 11556877, "FY2021": 4905429}),
    ("DATA", "Interest expense", {"FY2025": -21374863, "FY2024": -23894652, "FY2023": -20979927, "FY2022": -7253595, "FY2021": -1647023}),
    ("TOTAL", "Net interest income", {"FY2025": 8619913, "FY2024": 6761136, "FY2023": 4345688, "FY2022": 4303282, "FY2021": 3258406}),
    ("DATA", "Net loss on financial assets designated at FVTPL", {"FY2021": -10063}),
    ("DATA", "Net gain on derivatives", {"FY2021": 812}),
    ("DATA", "Fees and commission income", {"FY2025": 1358502, "FY2024": 746764, "FY2023": 1473358, "FY2022": 1456092, "FY2021": 1148928}),
    ("DATA", "Fees and commission expense", {"FY2025": -30523, "FY2024": -25301, "FY2023": -31231, "FY2022": -2908, "FY2021": -9309}),
    ("DATA", "Other operating income/(loss)", {"FY2025": -168584, "FY2024": 265263, "FY2023": -55678, "FY2022": 400171, "FY2021": -235485}),
    ("TOTAL", "Total operating income", {"FY2025": 9779308, "FY2024": 7747862, "FY2023": 5732137, "FY2022": 6156637, "FY2021": 4153289}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Administrative expenses", {"FY2025": -4398250, "FY2024": -3657484, "FY2023": -2628149, "FY2022": -2806180, "FY2021": -2489926}),
    ("DATA", "Impairment charge on financial assets", {"FY2025": -1982010, "FY2024": -348957, "FY2023": -5459, "FY2022": -241383, "FY2021": -93026}),
    ("TOTAL", "Profit on ordinary activities before tax", {"FY2025": 3399048, "FY2024": 3741421, "FY2023": 3098529, "FY2022": 3109074, "FY2021": 1570337}),
    ("DATA", "Tax on profit on ordinary activities", {"FY2025": -861590, "FY2024": -940183, "FY2023": -732891, "FY2022": -591640, "FY2021": -321939}),
    ("TOTAL", "Profit on ordinary activities after tax", {"FY2025": 2537458, "FY2024": 2801238, "FY2023": 2365638, "FY2022": 2517434, "FY2021": 1248398}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Reclassified to profit and loss", {"FY2025": -80276, "FY2024": -211575}),
    ("DATA", "Gain/(loss) arising during the year", {"FY2025": 1855966, "FY2024": 1936519, "FY2023": None, "FY2022": -5640570}),
    ("DATA", "Changes in allowance for expected credit losses during the year - FVOCI", {"FY2025": -35137, "FY2024": 21876, "FY2022": 9305}),
    ("DATA", "Credit/(debit) to deferred tax", {"FY2025": -435138, "FY2024": -436705, "FY2022": 1385670}),
    ("DATA", "Debit to deferred tax - prior year", {"FY2022": -16110}),
    ("TOTAL", "Other comprehensive income/(loss) for the year, net of tax", {"FY2025": 1305415, "FY2024": 1310115, "FY2023": 3275643, "FY2022": -4262152, "FY2021": -1442616}),
    ("TOTAL", "Total comprehensive income/(loss) for the year", {"FY2025": 3842873, "FY2024": 4111353, "FY2023": 5641281, "FY2022": -1744718, "FY2021": -194218}),
]

bw.add_income_statement_sheet(
    title="KEXIM Bank (UK) Limited — Profit & Loss",
    subtitle="Entity-level basis, whole £. FY2023's own report discloses no OCI line-item breakdown beyond the "
              "net total - the FY2023 'Gain/(loss) arising during the year' cell is deliberately left blank, not "
              "guessed, while the Other comprehensive income TOTAL row (3,275,643) is the Bank's own disclosed "
              "figure. FY2021 alone discloses small FVTPL/derivatives lines, absent FY2022-2025.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES + STATEMENTS_PRESENTATION_NOTE + "\n\n" + ENTITY_NOTE,
    first_col_width=72,
    source_height=420,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity (chronological) - built using the per-year
# reconciliation ladder: Balance Sheet built first (above), then each
# year's closing balance checked against both the next year's own opening
# balance and that year's own Balance Sheet Total. Ties exactly at every
# boundary (subject to the two documented £1 source-rounding artifacts and
# one £3 artifact within FY2025's own equity statement, all reproduced as
# disclosed, not force-reconciled - see source note).
# ---------------------------------------------------------------
equity_changes_rows = [
    ("TOTAL", "Balance at 1 January 2021", (81283897, 1100635, 14578021, 96962553)),
    ("DATA", "Profit for the year (FY2021)", (None, None, 1248398, 1248398)),
    ("DATA", "Dividends paid during the year (FY2021)", (None, None, -39764, -39764)),
    ("DATA", "Other comprehensive loss for the year (FY2021)", (None, -1442616, None, -1442616)),
    ("TOTAL", "Balance at 31 December 2021 (per FY2021's own Equity Statement; FY2021's own Balance Sheet "
              "shows Revaluation reserve (341,980) and Profit and loss account 15,786,654, each £1 different - "
              "reproduced as disclosed)", (81283897, -341981, 15786655, 96728571)),
    ("DATA", "Prior year adjustment (corporation tax) (FY2022)", (None, None, 4816, 4816)),
    ("DATA", "Profit for the year (FY2022)", (None, None, 2517434, 2517434)),
    ("DATA", "Other comprehensive loss for the year (FY2022)", (None, -4262152, None, -4262152)),
    ("TOTAL", "Balance at 31 December 2022", (81283897, -4604133, 18308905, 94988669)),
    ("DATA", "Profit for the year (FY2023)", (None, None, 2365638, 2365638)),
    ("DATA", "Other comprehensive income for the year (FY2023)", (None, 3275643, None, 3275643)),
    ("TOTAL", "Balance at 31 December 2023", (81283897, -1328490, 20674543, 100629950)),
    ("DATA", "Profit for the year (FY2024)", (None, None, 2801238, 2801238)),
    ("DATA", "Other comprehensive income for the year (FY2024)", (None, 1310115, None, 1310115)),
    ("TOTAL", "Balance at 31 December 2024", (81283897, -18375, 23475781, 104741303)),
    ("DATA", "Dividends paid during the year (FY2025)", (None, None, -140062, -140062)),
    ("DATA", "Profit for the year (FY2025)", (None, None, 2537458, 2537458)),
    ("DATA", "Other comprehensive income for the year (FY2025) (per FY2025's own Equity Statement; the "
              "Statement of Comprehensive Income shows this year's OCI total as 1,305,415, £1 different - "
              "reproduced as disclosed, see source note)", (None, 1305416, None, 1305416)),
    ("TOTAL", "Balance at 31 December 2025 (FY2025's own Equity Statement's column arithmetic is £2-3 off its "
              "own printed closing total - reproduced exactly as printed, not recomputed)", (81283897, 1287040, 25873175, 108444112)),
]

bw.add_equity_changes_sheet(
    title="KEXIM Bank (UK) Limited — Statement of Changes in Equity",
    subtitle="Entity-level basis, whole £. Chronological roll-forward, oldest to newest. GBP throughout - no FX "
              "conversion needed. Ties exactly to the Balance Sheet's own Total shareholders' funds at every "
              "year-end (subject to the documented £1-3 source-rounding artifacts noted in each row).",
    headers=["Called up share capital", "Revaluation reserve", "Profit and loss account", "Total equity"],
    rows=equity_changes_rows,
    sources_text=STATEMENTS_SOURCES + STATEMENTS_PRESENTATION_NOTE + "\n\n" + ENTITY_NOTE,
    first_col_width=90,
    source_height=460,
)

# ---------------------------------------------------------------
# Sheet: Cash Flow Statement (exemption note in place of line items)
# ---------------------------------------------------------------
rows = [
    ("SECTION", "No Statement of Cash Flows is published by this entity in any year", {}),
    ("DATA", "See the notes below for the FRS 101 exemption this entity relies on every year, and why this "
             "workbook is built as a Pillar-3-only variant.", {}),
]

bw.add_cash_flow_sheet(
    title="KEXIM Bank (UK) Limited — Cash Flow Statement",
    subtitle="Not applicable — this entity takes the FRS 101 cash-flow-statement disclosure exemption every year. See source notes below.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES + "\n\n" + WEBSITE_NOTE,
    first_col_width=90,
    source_height=340,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Asset Quality - the Bank's own Note 15 "Loans and advances to customers"
# discloses a full IFRS 9 Stage 1/2/3 gross-carrying-amount roll-forward
# and a stage-by-rating-grade net-of-provision table for every year. All
# 5 years are 100% Stage 1 except FY2025 (Stage 2 appeared for the first
# time) and FY2024 (a small Stage 2 balance also existed) - confirmed by
# reading Note 15 in full for every year, cross-checked against the
# FY2025 Independent Auditor's Report's own Key Audit Matter figures
# (£266,875k Stage 1 / £9,030k Stage 2 at 31 December 2025, in thousands
# - matches the whole-£ note figures below exactly once rounded).
# ---------------------------------------------------------------
AQ_GROSS_S1 = {"FY2025": 266875202, "FY2024": 256529805, "FY2023": 222698727, "FY2022": 220649996, "FY2021": 162920170}
AQ_GROSS_S2 = {"FY2025": 9029903, "FY2024": 155589, "FY2023": 0, "FY2022": 0, "FY2021": 0}
AQ_GROSS_S3 = {y: 0 for y in YEARS}
AQ_GROSS_TOTAL = {y: AQ_GROSS_S1[y] + AQ_GROSS_S2[y] + AQ_GROSS_S3[y] for y in YEARS}
AQ_PROV_TOTAL = {"FY2025": 3030223, "FY2024": 993206, "FY2023": 759555, "FY2022": 786970, "FY2021": 595740}
AQ_NET_S1 = {"FY2025": 265322599, "FY2024": 255544563, "FY2023": None, "FY2022": None, "FY2021": None}
AQ_NET_S2 = {"FY2025": 7552283, "FY2024": 147626, "FY2023": None, "FY2022": None, "FY2021": None}
AQ_PROV_S1 = {y: (AQ_GROSS_S1[y] - AQ_NET_S1[y]) if AQ_NET_S1[y] is not None else None for y in YEARS}
AQ_PROV_S2 = {y: (AQ_GROSS_S2[y] - AQ_NET_S2[y]) if AQ_NET_S2[y] is not None else None for y in YEARS}
AQ_NET_TOTAL = {"FY2025": 272874882, "FY2024": 255692188, "FY2023": 221939172, "FY2022": 219863026, "FY2021": 162324430}
AQ_COVERAGE = {y: f"{AQ_PROV_TOTAL[y] / AQ_GROSS_TOTAL[y] * 100:.4f}%" for y in YEARS}
AQ_STAGE2_RATIO = {y: f"{AQ_GROSS_S2[y] / AQ_GROSS_TOTAL[y] * 100:.4f}%" for y in YEARS}

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, gross carrying amount by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (12-month ECL)", AQ_GROSS_S1),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", AQ_GROSS_S2),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired)", AQ_GROSS_S3),
    ("TOTAL", "Total gross carrying amount", AQ_GROSS_TOTAL),
    ("SECTION", "Loss allowance (ECL) by stage - only disclosed by stage for FY2025/FY2024, "
                "when Stage 2 first appeared; FY2021-FY2023 were 100% Stage 1 so the total loss allowance "
                "IS the Stage 1 loss allowance", {}),
    ("DATA", "Stage 1 loss allowance", AQ_PROV_S1),
    ("DATA", "Stage 2 loss allowance", AQ_PROV_S2),
    ("DATA", "Total loss allowance", AQ_PROV_TOTAL),
    ("SECTION", "Net carrying amount", {}),
    ("TOTAL", "Total net carrying amount (ties to Balance Sheet's own Loans and advances to customers)", AQ_NET_TOTAL),
    ("SECTION", "Ratios", {}),
    ("DATA", "Stage 2 exposure ratio (Stage 2 / total gross carrying amount)", AQ_STAGE2_RATIO),
    ("DATA", "Overall coverage ratio (total loss allowance / total gross carrying amount)", AQ_COVERAGE),
]

bw.add_asset_quality_sheet(
    title="KEXIM Bank (UK) Limited — Asset Quality / Credit Risk Disclosures",
    subtitle="Loans and advances to customers by IFRS 9 stage, whole £. Entity-level basis - the Bank has no "
              "subsidiaries of its own.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - KEXIM Bank (UK) Limited's own Note 15 'Loans and advances to customers' (gross carrying "
        "amount roll-forward and stage-by-rating-grade table), all 5 filings scanned/image-only, visually "
        "transcribed:\n"
        f"FY2025/FY2024: Annual Report 2025, Note 15, p.52-53 - {FY2025_AR_URL}\n"
        f"FY2023/FY2022: Annual Report 2023, Note 15, p.54-56 - {FY2023_AR_URL}\n"
        f"FY2021: Annual Report 2021, Note 15, p.50 - {FY2021_AR_URL}\n\n"
        "FY2021-FY2023 are genuinely 100% Stage 1 (confirmed by reading each year's own stage-by-rating-grade "
        "table in full, all showing nil Stage 2/Stage 3 columns) - Stage 2 first appears in FY2024 (£155,589, "
        "a single transferred exposure) and grows materially in FY2025 (£9,029,903). No Stage 3 (credit-impaired) "
        "balance has existed in any of the 5 years covered. Net-by-stage figures (and therefore per-stage loss "
        "allowance) are only derivable for FY2025/FY2024, since only those years' own tables show a nonzero "
        "Stage 2 net balance to work from - FY2021-FY2023's Total loss allowance is shown undivided since it is "
        "entirely Stage 1 by construction.\n\n" + ENTITY_NOTE
    ),
    first_col_width=88,
    source_height=440,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=190)


CAPITAL_RATIO = {"FY2025": "20.5%", "FY2024": "20.9%", "FY2023": "22.8%", "FY2022": "22.5%", "FY2021": "30.0%"}

RATIO_NOTE = (
    "The source discloses this as a single combined \"Common Equity Tier 1 and total capital adequacy ratio\" "
    "(the same percentage for both measures, explicitly stated as one figure covering both in every one of the 5 "
    "reports checked) - populated identically on both the CET1 Ratio and Total Capital Ratio sheets rather than "
    "assumed for only one. No £ CET1/Total Capital amount and no RWA figure is disclosed anywhere, so the "
    "underlying capital amount cannot be calculated. Tier 1 Ratio is not separately disclosed (no AT1/Tier 2 "
    "instruments are mentioned in any report, but the source never explicitly confirms Tier 1 = CET1 = Total "
    "Capital, so Tier 1 Ratio is left not-disclosed rather than assumed equal)."
)

bw.add_not_disclosed_metric_sheets(
    ["CET1 Capital"], p3_sources(), per_note={"CET1 Capital": NOT_DISCLOSED_NOTE},
)

metric(
    "CET1 Ratio", "%",
    [("Common Equity Tier 1 ratio", CAPITAL_RATIO)],
    p3_sources(),
    note=RATIO_NOTE,
)

bw.add_not_disclosed_metric_sheets(
    ["Tier 1 Capital", "Tier 1 Ratio", "Total Capital"],
    p3_sources(),
    per_note={m: NOT_DISCLOSED_NOTE for m in ["Tier 1 Capital", "Tier 1 Ratio", "Total Capital"]},
)

metric(
    "Total Capital Ratio", "%",
    [("Total capital adequacy ratio", CAPITAL_RATIO)],
    p3_sources(),
    note=RATIO_NOTE,
)

bw.add_not_disclosed_metric_sheets(
    ["Total RWAs"], p3_sources(), per_note={"Total RWAs": NOT_DISCLOSED_NOTE},
)

rwa_breakdown_rows = [
    ("DATA", "Not publicly disclosed - no RWA figure (aggregate or by category) appears anywhere in the "
             "FY2021-FY2025 Annual Reports checked, and no dedicated Pillar 3 document is published by this "
             "entity (see the Cash Flow Statement sheet's access note - a second, more thorough search during "
             "this ST-024 build, reading every note in all 5 filings in full, confirmed no capital-management "
             "note or RWA figure exists anywhere). See the CET1 Ratio/Total Capital Ratio sheets for the only "
             "capital-related figures disclosed.", {}),
]

bw.add_rwa_breakdown_sheet(
    title="KEXIM Bank (UK) Limited — RWA Breakdown",
    subtitle="See source note - no RWA figure of any kind is published for this entity.",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources() + NOT_DISCLOSED_NOTE,
    first_col_width=90,
    source_height=260,
)

bw.add_not_disclosed_metric_sheets(
    ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"],
    p3_sources(),
    per_note={m: NOT_DISCLOSED_NOTE for m in ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"]},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 604228751, "FY2024": 586007552, "FY2023": 524250678, "FY2022": 521204305, "FY2021": 386490055}),
        ("Loans and advances to customers", {"FY2025": 272874882, "FY2024": 255692188, "FY2023": 221939171, "FY2022": 219863026, "FY2021": 162324430}),
        ("Borrowings from credit institutions", {"FY2025": 490903342, "FY2024": 475810294, "FY2023": 418559481, "FY2022": 406105536, "FY2021": 285675937}),
        ("Total shareholders' funds", {"FY2025": 108444112, "FY2024": 104741303, "FY2023": 100629950, "FY2022": 94988669, "FY2021": 96728571}),
    ],
    balance_sheet_unit="£",
    income_statement_totals=[
        ("Total operating income", {"FY2025": 9779308, "FY2024": 7747862, "FY2023": 5732137, "FY2022": 6156637, "FY2021": 4153289}),
        ("Administrative expenses", {"FY2025": -4398250, "FY2024": -3657484, "FY2023": -2628149, "FY2022": -2806180, "FY2021": -2489926}),
        ("Profit on ordinary activities after tax", {"FY2025": 2537458, "FY2024": 2801238, "FY2023": 2365638, "FY2022": 2517434, "FY2021": 1248398}),
    ],
    income_statement_unit="£",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 104741303, "FY2024": 100629950, "FY2023": 94988669, "FY2022": 96728571, "FY2021": 96962553}),
        ("Profit for the year", {"FY2025": 2537458, "FY2024": 2801238, "FY2023": 2365638, "FY2022": 2517434, "FY2021": 1248398}),
        ("Other movements, net", {"FY2025": 1165351, "FY2024": 1310115, "FY2023": 3275643, "FY2022": -4257336, "FY2021": -1482380}),
        ("Closing equity", {"FY2025": 108444112, "FY2024": 104741303, "FY2023": 100629950, "FY2022": 94988669, "FY2021": 96728571}),
    ],
    equity_changes_unit="£",
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("CET1 / Total Capital Ratio", CAPITAL_RATIO),
    ],
    note="No cash flow summary or chart is shown here: KEXIM Bank (UK) Limited takes the FRS 101 cash-flow-"
         "statement exemption every year (see the Cash Flow Statement sheet). Balance Sheet, Profit & Loss and "
         "Statement of Changes in Equity headline blocks are all fully populated below, sourced from the Bank's "
         "own primary financial statements (not just the Strategic Report). No dedicated Pillar 3 document is "
         "published by this entity, and a thorough re-check of every note in all 5 Annual Reports during this "
         "ST-024 build confirmed no RWA or capital-management figure exists anywhere - the only capital metric "
         "disclosed anywhere is a single combined CET1/Total Capital adequacy ratio, stated once per year in each "
         "Annual Report's Strategic Report - all 5 years fully cross-checked and consistent, no restatements.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/KEXIM BANK UK FINANCIALS.xlsx")
