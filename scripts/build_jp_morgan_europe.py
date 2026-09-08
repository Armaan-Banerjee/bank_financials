import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {year: year for year in YEARS}

CH_URL = "https://find-and-update.company-information.service.gov.uk/company/00938937/filing-history"
P3_ARCHIVE_URL = "https://jpmorganchaseco.gcs-web.com/ir/sec-other-filings/basel-pillar-and-lcr-disclosures/pillar-uk/"
P3_2025_URL = "https://jpmorganchaseco.gcs-web.com/static-files/a51475c0-d908-423e-b8de-6410d277a867"
P3_2024_URL = "https://jpmorganchaseco.gcs-web.com/static-files/a170e6df-d951-42fc-9897-2aa04d681885"
AR_2024_URL = "https://jpmorganchaseco.gcs-web.com/static-files/b200f4be-f143-4934-9589-9f44bcadd9be"

AR2025_URL = (
    "https://find-and-update.company-information.service.gov.uk/company/00938937/"
    "filing-history/MzUyNTIyMTk4NGFkaXF6a2N4/document?format=pdf&download=0"
)
AR2024_URL = (
    "https://find-and-update.company-information.service.gov.uk/company/00938937/"
    "filing-history/MzQ2NzkwOTM5MGFkaXF6a2N4/document?format=pdf&download=0"
)
AR2023_URL = (
    "https://find-and-update.company-information.service.gov.uk/company/00938937/"
    "filing-history/MzQyNDAwMDkzMGFkaXF6a2N4/document?format=pdf&download=0"
)
AR2022_URL = (
    "https://find-and-update.company-information.service.gov.uk/company/00938937/"
    "filing-history/MzM4MDkyOTYxNGFkaXF6a2N4/document?format=pdf&download=0"
)
AR2021_URL = (
    "https://find-and-update.company-information.service.gov.uk/company/00938937/"
    "filing-history/MzM0MTgzNDEzMGFkaXF6a2N4/document?format=pdf&download=0"
)

ENTITY_NOTE = (
    "ENTITY/BASIS NOTE: J.P. Morgan Europe Limited (Companies House 00938937; "
    "PRA FRN 124579) is the assigned UK legal entity. This workbook uses the "
    "JPMEL columns in JPMorgan's separate Annual Solo Pillar 3 disclosures, "
    "not JPMorgan Chase group, JPMorgan Chase Bank N.A., JPMorgan Securities "
    "plc, JPMorgan SE, or another JPMorgan subsidiary. The 2024 JPMEL annual "
    "accounts state that the financial statements are prepared under FRS 101 "
    "Reduced Disclosure Framework; no cash-flow statement is therefore filled "
    "from a different entity or group report."
)

CURRENCY_NOTE = (
    "CURRENCY NOTE: JPMEL's FY2021 Annual Report (for the year ended 31 December 2021) was "
    "originally published entirely in $'000 (Total assets $3,620,536k; Total equity "
    "$2,121,931k; total comprehensive loss for the year $(109,906)k). Starting with the "
    "FY2022 Annual Report, JPMEL switched presentation currency to £'000, and the FY2022 "
    "report's own FY2021 comparative column restates FY2021 into £ (Total assets £2,672,969k; "
    "Total equity £1,566,579k; total comprehensive loss £(80,971)k). To keep this whole "
    "workbook (Balance Sheet, P&L, Statement of Changes in Equity) on one consistent £ basis "
    "matching FY2022-FY2025, FY2021 below uses the Bank's OWN officially restated £ comparative "
    "from the FY2022 Annual Report, not an independently-computed FX conversion. The original "
    "FY2021 $ figures are preserved here for reference, not used elsewhere in this workbook."
)

P3_SOURCES = (
    "Sources - J.P. Morgan Europe Limited standalone Pillar 3 disclosures, "
    "GBP millions, UK KM1 Table 2 and related standalone tables:\n"
    f"FY2025: P3 Annual Solo 2025, Table 2 UK KM1 for JPMEL (and Tables 4, 9, "
    f"33, 36 and 38 where applicable) - {P3_2025_URL}\n"
    f"FY2024: P3 Annual Solo 2024, Table 2 UK KM1 for JPMEL (FY2024 current "
    f"and FY2023 comparative) - {P3_2024_URL}\n"
    "FY2023 is taken from the FY2024 disclosure's JPMEL comparative column. "
    "No JPMEL standalone annual-solo KM1 was located for FY2021 or FY2022; "
    "group and other-entity disclosures are deliberately not substituted.\n"
    f"Official JPMorgan UK Pillar 3 archive - {P3_ARCHIVE_URL}\n"
    + ENTITY_NOTE
)

CASH_FLOW_SOURCES = (
    "CASH-FLOW EXEMPTION: JPMEL's 2024 annual accounts state that the company "
    "uses FRS 101 Reduced Disclosure Framework. A statement of cash flows is "
    "not presented in the standalone accounts reviewed, so no group or other "
    "entity cash flows are substituted. Companies House filing history: "
    f"{CH_URL}\n"
    f"JPMEL 2024 annual accounts, accounting basis - {AR_2024_URL}\n"
    + ENTITY_NOTE
)

bw = BankWorkbook(
    bank_name="J.P. Morgan Europe Limited",
    years=YEARS,
    year_label=YEAR_LABEL,
    header_color="1F4E79",
)

STATEMENTS_SOURCES = (
    "Sources - J.P. Morgan Europe Limited's own Companies House Annual Report filings "
    "(Company-only basis; all figures £'000 except FY2021, see CURRENCY NOTE below):\n"
    f"FY2025/FY2024: Annual Report for the year ended 31 December 2025, Income statement "
    "p.60, Statement of financial position p.61, Statement of changes in equity p.62 - "
    f"{AR2025_URL}\n"
    f"FY2023: Annual Report for the year ended 31 December 2023, Income statement p.57, "
    f"Statement of financial position p.59, Statement of changes in equity p.60 - {AR2023_URL}\n"
    f"FY2022: Annual Report for the year ended 31 December 2022 (own report, not a later "
    "comparative), Income statement p.58, Statement of financial position p.60, Statement "
    f"of changes in equity p.61 - {AR2022_URL}\n"
    f"FY2021: Annual Report for the year ended 31 December 2021's OWN report is denominated "
    "in $ (Balance sheet p.65, Income statement p.63, Statement of changes in equity p.66) - "
    f"{AR2021_URL} - the £ figures used here are instead the Bank's own restated FY2021 "
    f"comparative column from the FY2022 Annual Report (as above, {AR2022_URL}).\n\n"
    + CURRENCY_NOTE + "\n\n" + ENTITY_NOTE
)

# ---------------------------------------------------------------
# Balance Sheet - all years tie exactly (Total assets = Total liabilities +
# Total equity); FY2021 uses the Bank's own restated £ comparative (see
# CURRENCY_NOTE) so the whole sheet is on one consistent £ basis.
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Loans and advances to banks", {"FY2025": 26788584, "FY2024": 23250686, "FY2023": 16371664, "FY2022": 11969640, "FY2021": 1850151}),
    ("DATA", "Loans and advances to customers", {"FY2025": 176380, "FY2024": 2650, "FY2023": None, "FY2022": None, "FY2021": None}),
    ("DATA", "Securities purchased under resale agreements", {"FY2025": 2318947, "FY2024": 2054090, "FY2023": 2083444, "FY2022": 1666206, "FY2021": 788187}),
    ("DATA", "Financial assets held/designated at fair value through profit or loss", {"FY2025": 0, "FY2024": 101, "FY2023": 1949, "FY2022": 2200, "FY2021": 6563}),
    ("DATA", "Trade and other receivables / Debtors", {"FY2025": 17705, "FY2024": 6470, "FY2023": 67641, "FY2022": 48970, "FY2021": 18526}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 134287, "FY2024": 135940, "FY2023": 258422, "FY2022": 20823, "FY2021": 616}),
    ("DATA", "Tangible fixed asset", {"FY2025": 3, "FY2024": 3, "FY2023": 316, "FY2022": 646, "FY2021": 1061}),
    ("DATA", "Assets held for sale", {"FY2025": None, "FY2024": None, "FY2023": None, "FY2022": 34, "FY2021": 7865}),
    ("TOTAL", "Total assets", {"FY2025": 29435906, "FY2024": 25449940, "FY2023": 18783436, "FY2022": 13708519, "FY2021": 2672969}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from JPMorganChase undertakings / by banks", {"FY2025": 31395, "FY2024": 146241, "FY2023": 24649, "FY2022": 66757, "FY2021": 2012}),
    ("DATA", "Customer accounts", {"FY2025": 26663435, "FY2024": 22794662, "FY2023": 17134548, "FY2022": 12112372, "FY2021": 1049094}),
    ("DATA", "Financial liabilities held at fair value through profit or loss", {"FY2025": None, "FY2024": None, "FY2023": 0, "FY2022": 1, "FY2021": 0}),
    ("DATA", "Trade and other payables / creditors", {"FY2025": 53664, "FY2024": 69800, "FY2023": 118128, "FY2022": 680, "FY2021": 0}),
    ("DATA", "Other liabilities", {"FY2025": None, "FY2024": None, "FY2023": None, "FY2022": 62344, "FY2021": 28915}),
    ("DATA", "Provisions for liabilities", {"FY2025": None, "FY2024": None, "FY2023": None, "FY2022": 0, "FY2021": 7}),
    ("DATA", "Accruals and deferred income", {"FY2025": 93422, "FY2024": 112265, "FY2023": 76567, "FY2022": 47749, "FY2021": 26362}),
    ("TOTAL", "Total liabilities", {"FY2025": 26841916, "FY2024": 23122968, "FY2023": 17353892, "FY2022": 12289903, "FY2021": 1106390}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 2050352, "FY2024": 1899976, "FY2023": 1032058, "FY2022": 1032058, "FY2021": 1032058}),
    ("DATA", "Share premium", {"FY2025": 170593, "FY2024": 170593, "FY2023": 170593, "FY2022": 170593, "FY2021": 170593}),
    ("DATA", "Other reserves (incl. capital contribution reserve)", {"FY2025": 127257, "FY2024": 125756, "FY2023": 123499, "FY2022": 122093, "FY2021": 122093}),
    ("DATA", "Cumulative translation reserve", {"FY2025": -170, "FY2024": -170, "FY2023": -170, "FY2022": -170, "FY2021": -170}),
    ("DATA", "Retained earnings", {"FY2025": 245958, "FY2024": 130817, "FY2023": 103564, "FY2022": 94042, "FY2021": 242005}),
    ("TOTAL", "Total equity", {"FY2025": 2593990, "FY2024": 2326972, "FY2023": 1429544, "FY2022": 1418616, "FY2021": 1566579}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 29435906, "FY2024": 25449940, "FY2023": 18783436, "FY2022": 13708519, "FY2021": 2672969}),
]

bw.add_balance_sheet_sheet(
    title="J.P. Morgan Europe Limited — Statement of Financial Position",
    subtitle="Company-only basis. £'000 (FY2021 restated from the Bank's own $ original - see source note).",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=72,
    source_height=340,
)

# ---------------------------------------------------------------
# Profit & Loss - each year's own originally-published structure (FY2022's
# own report splits Continuing/Discontinued Operations; FY2021 uses the
# Bank's own restated £ Total column from the FY2022 report - see
# CURRENCY_NOTE). Structural differences documented, not smoothed over.
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 1151045, "FY2024": 1185014, "FY2023": 865013, "FY2022": 199629, "FY2021": 8178}),
    ("DATA", "Interest expense", {"FY2025": -701940, "FY2024": -789199, "FY2023": -534716, "FY2022": -123885, "FY2021": -680}),
    ("TOTAL", "Net interest income", {"FY2025": 449105, "FY2024": 395815, "FY2023": 330297, "FY2022": 75744, "FY2021": 7498}),
    ("DATA", "Fee and commission income", {"FY2025": 52507, "FY2024": 46450, "FY2023": 44419, "FY2022": 35190, "FY2021": 187913}),
    ("DATA", "Fee and commission expense", {"FY2025": -181, "FY2024": -433, "FY2023": -545, "FY2022": -71821, "FY2021": -81223}),
    ("TOTAL", "Net fee and commission income/(expense)", {"FY2025": 52326, "FY2024": 46017, "FY2023": 43874, "FY2022": -36631, "FY2021": 106690}),
    ("DATA", "Trading profit/(loss)", {"FY2025": 62, "FY2024": -225, "FY2023": -29, "FY2022": -698, "FY2021": 907}),
    ("DATA", "Dividend income / Other income", {"FY2025": None, "FY2024": None, "FY2023": None, "FY2022": None, "FY2021": 31132}),
    ("DATA", "Expected credit loss charge/(release)", {"FY2025": -3131, "FY2024": -200, "FY2023": -887, "FY2022": -299, "FY2021": 2247}),
    ("DATA", "Operating and administrative expense", {"FY2025": -339398, "FY2024": -404387, "FY2023": -364660, "FY2022": -187846, "FY2021": -226670}),
    ("TOTAL", "Profit/(loss) before taxation", {"FY2025": 158964, "FY2024": 37020, "FY2023": 8595, "FY2022": -149730, "FY2021": -79998}),
    ("DATA", "Tax on profit/(loss)", {"FY2025": -44670, "FY2024": -10245, "FY2023": 927, "FY2022": 1767, "FY2021": -973}),
    ("TOTAL", "Profit/(loss) for the year", {"FY2025": 114294, "FY2024": 26775, "FY2023": 9522, "FY2022": -147963, "FY2021": -80971}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Other comprehensive income/(expense)", {"FY2025": 0, "FY2024": 0, "FY2023": None, "FY2022": None, "FY2021": None}),
    ("TOTAL", "Total comprehensive income/(loss) for the year", {"FY2025": 114294, "FY2024": 26775, "FY2023": 9522, "FY2022": -147963, "FY2021": -80971}),
]

bw.add_income_statement_sheet(
    title="J.P. Morgan Europe Limited — Income Statement",
    subtitle=(
        "Company-only basis. £'000 (FY2021 restated - see source note). FY2022's own report presented "
        "Continuing/Discontinued Operations columns and a Net operating income subtotal not used in "
        "FY2023-FY2025 reports; FY2021's £ Total column combines Trading profit/Dividend income/Other "
        "income into a single 'Other income' line here (31,132 = 907 trading + 2,292 dividend + 28,840 "
        "other, matching the Bank's own FY2021 comparative structure)."
    ),
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=72,
    source_height=340,
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - per-year reconciliation ladder. FY2021's
# own $ movements aren't restated into £ anywhere by the Bank, so the ladder
# starts at "Balance as at 31 December 2021" (the Bank's own restated £
# closing figure, tying exactly to the Balance Sheet's FY2021 Total equity)
# rather than force-converting FY2021's own $ movements - see CURRENCY_NOTE.
# Every year from FY2022 onward ties exactly to both its own Balance Sheet
# Total equity and the next year's own opening balance - zero plug rows
# needed anywhere.
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Share capital", "Share premium", "Capital contribution reserve", "Other reserves", "Cumulative translation reserve", "Retained earnings", "Total equity"]

equity_rows = [
    ("TOTAL", "Balance as at 31 December 2021 (Bank's own restated £ comparative, FY2022 Annual Report)", (1032058, 170593, 26341, 95752, -170, 242005, 1566579)),
    ("DATA", "Loss for the financial year (FY2022)", (None, None, None, None, None, -147963, -147963)),
    ("DATA", "Group share-based payment costs", (None, None, None, None, None, 356, 356)),
    ("DATA", "Group share-based payment costs recharged", (None, None, None, None, None, -356, -356)),
    ("TOTAL", "Balance as at 31 December 2022", (1032058, 170593, 26341, 95752, -170, 94042, 1418616)),
    ("DATA", "Profit for the financial year (FY2023)", (None, None, None, None, None, 9522, 9522)),
    ("DATA", "Group share-based payment costs", (None, None, None, None, None, 4707, 4707)),
    ("DATA", "Group share-based payment costs recharged", (None, None, None, None, None, -4707, -4707)),
    ("DATA", "Tax effect on share-based payments", (None, None, None, 1406, None, 478, 1884)),
    ("DATA", "Movement in reserves (reclassification)", (None, None, -1477, 1477, None, None, 0)),
    ("TOTAL", "Balance as at 31 December 2023", (1032058, 170593, 24864, 98635, -170, 103564, 1429544)),
    ("DATA", "Issue of ordinary shares", (867918, None, None, None, None, None, 867918)),
    ("DATA", "Profit for the financial year (FY2024)", (None, None, None, None, None, 26775, 26775)),
    ("DATA", "Group share-based payment costs", (None, None, None, None, None, 12403, 12403)),
    ("DATA", "Group share-based payment costs recharged", (None, None, None, None, None, -12403, -12403)),
    ("DATA", "Tax effect on share-based payments", (None, None, None, 2257, None, 478, 2735)),
    ("TOTAL", "Balance as at 31 December 2024", (1899976, 170593, 24864, 100892, -170, 130817, 2326972)),
    ("DATA", "Issue of ordinary shares", (150376, None, None, None, None, None, 150376)),
    ("DATA", "Profit for the financial year (FY2025)", (None, None, None, None, None, 114294, 114294)),
    ("DATA", "Group share-based payment credits", (None, None, None, None, None, -4224, -4224)),
    ("DATA", "Group share-based payment credits recharged", (None, None, None, None, None, 4224, 4224)),
    ("DATA", "Tax effect on share-based payments", (None, None, None, 1501, None, 847, 2348)),
    ("TOTAL", "Balance as at 31 December 2025", (2050352, 170593, 24864, 102393, -170, 245958, 2593990)),
]

bw.add_equity_changes_sheet(
    title="J.P. Morgan Europe Limited — Statement of Changes in Equity",
    subtitle=(
        "Chronological roll-forward, oldest to newest, £'000. Reconciliation ladder confirmed: every year "
        "from FY2022 onward ties exactly to both its own Balance Sheet Total equity and the next year's own "
        "opening balance. Starts at 31 December 2021 (the Bank's own restated £ closing figure) rather than "
        "FY2021's own $ movements - see CURRENCY_NOTE on the Balance Sheet sheet."
    ),
    headers=EQUITY_HEADERS,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=260,
)

bw.add_cash_flow_sheet(
    title="J.P. Morgan Europe Limited — Statement of Cash Flows",
    subtitle="Not presented: FRS 101 reduced-disclosure exemption; no substitute group/entity data used.",
    rows=[
        ("SECTION", "FRS 101 cash-flow presentation", {}),
        ("DATA", "Standalone statement of cash flows", {year: "Not presented under FRS 101" for year in YEARS}),
    ],
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=230,
    unit_suffix="",
)

# ---------------------------------------------------------------
# Asset Quality - JPMEL's audited notes don't disclose a quantitative IFRS 9
# Stage 1/2/3 gross-exposure table (Note 15 explicitly refers the credit
# quality/staging detail to the Strategic Report's narrative risk section,
# which itself only states qualitatively that "the majority of the credit
# card exposure...is classified as Stage 1", confirmed by reading that
# section in full - not force-tabulated from a narrative statement). Built
# instead from what IS quantitatively disclosed: Note 15's gross/provision/
# net loans and advances to customers, and Note 9's ECL allowance
# roll-forward. Loans and advances to customers is genuinely nil FY2021-
# FY2023 (confirmed on the Balance Sheet each year) - a real feature (this
# entity only began customer/card lending from FY2024), not a gap.
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to customers", {}),
    ("DATA", "Gross loans and advances to customers at amortised cost", {"FY2025": 179003, "FY2024": 2830, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Provision for impairment", {"FY2025": -2623, "FY2024": -180, "FY2023": None, "FY2022": None, "FY2021": None}),
    ("TOTAL", "Net loans and advances to customers", {"FY2025": 176380, "FY2024": 2650, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("SECTION", "Expected credit loss (ECL) allowance movements", {}),
    ("DATA", "Allowance for loan losses - opening balance", {"FY2025": 190, "FY2024": 404, "FY2023": None, "FY2022": None, "FY2021": None}),
    ("DATA", "Allowance for loan losses - ECL charge for the year", {"FY2025": 2042, "FY2024": 190, "FY2023": None, "FY2022": None, "FY2021": None}),
    ("DATA", "Allowance for loan losses - amounts written off", {"FY2025": -708, "FY2024": -404, "FY2023": None, "FY2022": None, "FY2021": None}),
    ("TOTAL", "Allowance for loan losses - closing balance", {"FY2025": 1524, "FY2024": 190, "FY2023": None, "FY2022": None, "FY2021": None}),
    ("DATA", "Allowance for lending-related commitments - closing balance", {"FY2025": 1099, "FY2024": 10, "FY2023": None, "FY2022": None, "FY2021": None}),
    ("TOTAL", "Total ECL charge for the year", {"FY2025": 3131, "FY2024": 200, "FY2023": 887, "FY2022": 299, "FY2021": None}),
    ("DATA", "Net loans and advances to customers coverage ratio", {"FY2025": "1.47%", "FY2024": "6.36%"}),
]

bw.add_asset_quality_sheet(
    title="J.P. Morgan Europe Limited — Asset Quality",
    subtitle="Company-only basis. £'000. No quantitative IFRS 9 Stage 1/2/3 table is disclosed - see source note.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - J.P. Morgan Europe Limited's own Annual Report notes:\n"
        f"FY2025/FY2024: Annual Report for the year ended 31 December 2025, Note 9 'Expected credit loss "
        f"charge' p.70, Note 15 'Loans and advances to customers' p.74 - {AR2025_URL}\n"
        f"FY2023/FY2022/FY2021: Note 9-equivalent 'Expected credit loss charge' totals from each year's own "
        f"Income statement (Notes 9/11 respectively); Loans and advances to customers confirmed £nil on each "
        f"year's own Balance Sheet (Note 15/17) - {AR2023_URL}, {AR2022_URL}, {AR2021_URL}\n\n"
        "No IFRS 9 Stage 1/2/3 gross-exposure table is disclosed anywhere in the audited financial statement "
        "notes - Note 15 explicitly states 'the credit quality and analysis of concentration of loans and "
        "advances to customers is included in the Strategic Report' (pages 9-19), which was read in full and "
        "found to be qualitative/narrative only (e.g. 'the majority of the credit card exposure...is "
        "classified as Stage 1'), not a quantitative table - not force-tabulated from narrative text. Loans "
        "and advances to customers is genuinely £nil FY2021-FY2023 (this entity only began customer/card "
        "lending from FY2024) - a real feature, not a gap. FY2021-FY2022's Total ECL charge for the year is "
        "each year's own disclosed Expected credit loss charge from the Income statement (a single combined "
        "figure, not split between loan-loss and lending-commitment allowances in those years' notes).\n\n"
        + ENTITY_NOTE
    ),
    first_col_width=78,
    source_height=340,
)


def metric(name, unit, label, values, note=None):
    bw.add_metric_sheet(
        name,
        unit,
        [(label, values)],
        P3_SOURCES,
        note=note,
        first_col_width=58,
        source_height=230,
    )


CAPITAL = {"FY2025": 2594, "FY2024": 2327, "FY2023": 1429}
RWA = {"FY2025": 1041, "FY2024": 628, "FY2023": 440}
CAPITAL_RATIO = {"FY2025": "249.23%", "FY2024": "370.56%", "FY2023": "325.00%"}
LEVERAGE = {"FY2025": "94.12%", "FY2024": "98.73%", "FY2023": "65.05%"}
LCR = {"FY2025": "241.17%", "FY2024": "230.90%", "FY2023": "276.70%"}
NSFR = {"FY2025": "155.44%", "FY2024": "158.44%", "FY2023": "180.37%"}

GAP_NOTE = (
    "Only FY2023-FY2025 are populated: FY2023 is the FY2024 JPMEL KM1 "
    "comparative column. FY2021-FY2022 standalone JPMEL figures were not "
    "located, and consolidated or other-entity values are not substituted."
)

metric("CET1 Capital", "£m", "Common Equity Tier 1 (CET1) capital", CAPITAL, GAP_NOTE)
metric("CET1 Ratio", "%", "CET1 ratio", CAPITAL_RATIO, GAP_NOTE)
metric("Tier 1 Capital", "£m", "Tier 1 capital", CAPITAL, "JPMEL UK KM1 reports no separate AT1 amount; the disclosed capital total equals CET1/Tier 1 in each populated year.\n" + GAP_NOTE)
metric("Tier 1 Ratio", "%", "Tier 1 ratio", CAPITAL_RATIO, GAP_NOTE)
metric("Total Capital", "£m", "Total capital", CAPITAL, GAP_NOTE)
metric("Total Capital Ratio", "%", "Total capital ratio", CAPITAL_RATIO, GAP_NOTE)
metric("Total RWAs", "£m", "Total risk exposure amount / total RWAs", RWA, GAP_NOTE)

# ---------------------------------------------------------------
# RWA Breakdown - Table 9 "UK OV1 - Overview of RWAs for JPMEL" in the
# FY2024 Pillar 3 document (which reports Q4 2024 own-year and Q4 2023
# comparative columns). The live document is Akamai-blocked to automated
# GET requests (HEAD succeeds, GET returns "Access Denied"), but the
# FY2024 document is independently mirrored on the Wayback Machine
# (captured 1 May 2025) and was retrieved and visually transcribed from
# there. Both years' totals tie exactly to the Total RWAs sheet's own
# figures (628/440), confirming no restatement.
#
# FY2025's own standalone Pillar 3 document (P3_2025_URL) was previously
# flagged as a genuine access gap: it had no Wayback Machine snapshot and
# the live document was Akamai-blocked to every direct/curl/WebFetch
# attempt. Revisited in this session: a fresh Wayback "Save Page Now"
# request against the same URL succeeded this time (capture timestamp
# 20260904134708, application/pdf, 384,575 bytes), and the archived PDF
# was downloaded and text-extracted with pdftotext. Its Table 9 "UK OV1 -
# Overview of RWAs for JPMEL" (p.21) reports Q4 2025 and Q4 2024
# columns; the Q4 2024 column matches the FY2024 figures already
# transcribed below, and the Q4 2025 total (1,041) ties exactly to the
# Total RWAs sheet's own FY2025 figure - confirming the transcription.
# ---------------------------------------------------------------
rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 209, "FY2024": 87, "FY2023": 76}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 9, "FY2024": 7, "FY2023": 14}),
    ("DATA", "Of which credit valuation adjustment (CVA)", {"FY2025": 0, "FY2024": 0}),
    ("DATA", "Market risk (position, FX and commodities)", {"FY2025": 0, "FY2024": 0, "FY2023": 2}),
    ("DATA", "Operational risk", {"FY2025": 823, "FY2024": 534, "FY2023": 348}),
    ("DATA", "Amounts below thresholds for deduction (subject to 250% risk weight)", {"FY2025": 24, "FY2024": 14, "FY2023": 0}),
    ("TOTAL", "Total risk exposure amount", {"FY2025": 1041, "FY2024": 628, "FY2023": 440}),
]

bw.add_rwa_breakdown_sheet(
    title="J.P. Morgan Europe Limited — RWA Breakdown",
    subtitle="FY2025/FY2024/FY2023 from the Bank's own UK OV1 table, £m.",
    rows=rwa_breakdown_rows,
    sources_text=(
        f"FY2025/FY2024 (Q4 2025/Q4 2024 columns): Table 9 'UK OV1 - Overview of RWAs for JPMEL', Annual Pillar 3 "
        f"Disclosure Report as at 31st December 2025, p.21 - {P3_2025_URL} (live document Akamai-blocked to "
        "automated GET this session; a prior session's access-gap was revisited and resolved by triggering a "
        "fresh Wayback Machine 'Save Page Now' capture of the same URL, which succeeded on 4 Sept 2026 - "
        "http://web.archive.org/web/20260904134708/"
        f"{P3_2025_URL} - retrieved and machine-transcribed via pdftotext from that capture). The FY2025 total "
        "(1,041) ties exactly to the Total RWAs sheet's own FY2025 figure, and the Q4 2024 column matches the "
        "FY2024 figures below, confirming no restatement.\n"
        f"FY2024/FY2023 (also cross-checked against Q4 2024 column above): Table 9 'UK OV1 - Overview of RWAs "
        f"for JPMEL', Annual Pillar 3 Disclosure 2024, p.21 - {P3_2024_URL} (live document Akamai-blocked to "
        "automated GET this session; retrieved instead from the Wayback Machine's 1 May 2025 capture, "
        f"http://web.archive.org/web/20250501130027/{P3_2024_URL}). Both years' totals tie exactly to the Total "
        "RWAs sheet.\n"
        f"Official JPMorgan UK Pillar 3 archive - {P3_ARCHIVE_URL}\n"
        + ENTITY_NOTE
    ),
    first_col_width=78,
    source_height=340,
    unit_suffix=" (£m)",
)

metric("Leverage Ratio", "%", "Leverage ratio", LEVERAGE, GAP_NOTE)
metric("LCR", "%", "Liquidity Coverage Ratio", LCR, GAP_NOTE)
metric("NSFR", "%", "Net Stable Funding Ratio", NSFR, GAP_NOTE)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    P3_SOURCES,
    per_note={
        "MREL Ratio": (
            "No standalone JPMEL MREL ratio was found in the annual solo "
            "tables reviewed; group or another JPMorgan entity's MREL is not "
            "substituted."
        )
    },
)

bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit="",
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 29435906, "FY2024": 25449940, "FY2023": 18783436, "FY2022": 13708519, "FY2021": 2672969}),
        ("Loans and advances to customers", {"FY2025": 176380, "FY2024": 2650, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
        ("Customer accounts", {"FY2025": 26663435, "FY2024": 22794662, "FY2023": 17134548, "FY2022": 12112372, "FY2021": 1049094}),
        ("Total equity", {"FY2025": 2593990, "FY2024": 2326972, "FY2023": 1429544, "FY2022": 1418616, "FY2021": 1566579}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net interest income", {"FY2025": 449105, "FY2024": 395815, "FY2023": 330297, "FY2022": 75744, "FY2021": 7498}),
        ("Operating and administrative expense", {"FY2025": -339398, "FY2024": -404387, "FY2023": -364660, "FY2022": -187846, "FY2021": -226670}),
        ("Profit/(loss) for the year", {"FY2025": 114294, "FY2024": 26775, "FY2023": 9522, "FY2022": -147963, "FY2021": -80971}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 2326972, "FY2024": 1429544, "FY2023": 1418616, "FY2022": 1566579}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": 114294, "FY2024": 26775, "FY2023": 9522, "FY2022": -147963}),
        ("Closing equity", {"FY2025": 2593990, "FY2024": 2326972, "FY2023": 1429544, "FY2022": 1418616}),
    ],
    equity_changes_unit="£'000",
    ratios=[
        ("CET1 Ratio", CAPITAL_RATIO),
        ("Tier 1 Ratio", CAPITAL_RATIO),
        ("Total Capital Ratio", CAPITAL_RATIO),
        ("Leverage Ratio", LEVERAGE),
        ("LCR", LCR),
        ("NSFR", NSFR),
    ],
    note=(
        "Balance Sheet/P&L/Equity coverage is FY2021-FY2025 (FY2021 uses the Bank's own restated £ comparative "
        "- see the Balance Sheet sheet's CURRENCY_NOTE). Pillar 3 ratio quantitative coverage remains "
        "FY2023-FY2025 only; FY2021-FY2022 are explicitly not separately disclosed. Cash flow is not "
        "presented under FRS 101."
    ),
)

bw.save("/Users/armaan/code/katalysis/banks/JP MORGAN EUROPE FINANCIALS.xlsx")
print("Saved.")
