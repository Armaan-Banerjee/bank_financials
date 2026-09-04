import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024"]
YEAR_LABEL = {y: y for y in YEARS}

P3_2025_URL = "https://www.pnb.com.ph/storage/asset-libraries/Me1hxgtaSlrRs32Dvl6SIB1qgOfY1WbTDfGv2ZzQ.pdf"
P3_2024_URL = "https://pnb-website.s3-ap-southeast-1.amazonaws.com/uploads/docs/Pillar3_Disclosures.pdf"
CH_PROFILE_URL = "https://find-and-update.company-information.service.gov.uk/company/02939223"
CH_ACCOUNTS_URL = CH_PROFILE_URL + "/filing-history?category=accounts"
AR2025_URL = CH_ACCOUNTS_URL  # Full Report and Financial Statements, year ended 31 December 2025, filed via Companies House (image-only scan)

ENTITY_NOTE = (
    "ENTITY/BASIS: Philippine National Bank (Europe) Plc (Companies House 02939223; FRN 204532; "
    "LEI 8945002FWV05NGBXJJ26) is the UK-registered bank, wholly owned by Philippine National Bank "
    "(Manila). The official FY2024 and FY2025 Pillar 3 documents state that PNBE has no subsidiaries "
    "and disclose on an un-consolidated basis. Parent PNB Manila figures and parent-group disclosures "
    "are expressly excluded. Companies House confirms the entity and annual 31 December accounts history."
)

P3_SOURCES = (
    "Sources - PNBE's own standalone Pillar 3 disclosures (GBP '000 unless stated):\n"
    f"FY2025: Pillar 3 Disclosures for 31 December 2025, pp.3, 5-8 - {P3_2025_URL}\n"
    f"FY2024: Pillar 3 Disclosures for 31 December 2024, pp.3, 5-8 - {P3_2024_URL}\n"
    f"Entity identity and accounts filing history: Companies House - {CH_PROFILE_URL}; {CH_ACCOUNTS_URL}\n"
    + ENTITY_NOTE
)

EXEMPTION_NOTE = (
    "PILLAR-3-ONLY, two-year scope: the prior project screening identified PNBE's qualifying-entity "
    "cash-flow disclosure exemption in its UK accounts, so no audited cash-flow statement is populated "
    "here. The current build does not infer cash flows from parent PNB disclosures. The two official "
    "standalone Pillar 3 documents located provide quantitative capital/RWA data for FY2024-FY2025 only; "
    "no defensible standalone PNBE Pillar 3 quantitative documents were located for FY2021-FY2023, so "
    "those years are intentionally outside this workbook's scope (the Balance Sheet/P&L/Equity sheets "
    "below are limited to the same FY2024-FY2025 window for consistency, even though Companies House "
    "holds full accounts back to at least FY2021, to keep every sheet on the same two-year footing)."
)

BS_PL_SOURCES = (
    "Sources - Philippine National Bank (Europe) Plc's own Report and Financial Statements for the year "
    f"ended 31 December 2025 (image-only scan, Companies House filing history) - {AR2025_URL}. This single "
    "document's own FY2025 column and its own FY2024 comparative column are used for both years (Statement "
    "of Comprehensive Income p.18/printed p.17, Statement of Financial Position p.19/printed p.18, Statement "
    "of Changes in Equity p.20/printed p.19), so no separate FY2024 Annual Report was needed.\n\n"
    + ENTITY_NOTE
)

bw = BankWorkbook(bank_name="Philippine National Bank (Europe) Plc", years=YEARS,
                  year_label=YEAR_LABEL, header_color="007A33")

# --- Balance Sheet -------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash in hand", {"FY2025": 58, "FY2024": 136}),
    ("DATA", "Treasury bills", {"FY2025": 1294, "FY2024": 2263}),
    ("DATA", "Loans and advances to banks", {"FY2025": 12073, "FY2024": 12073}),
    ("DATA", "Loans and advances to customers", {"FY2025": 5, "FY2024": 10}),
    ("DATA", "Tangible fixed assets", {"FY2025": 364, "FY2024": 412}),
    ("DATA", "Other assets", {"FY2025": 37, "FY2024": 33}),
    ("DATA", "Prepayments", {"FY2025": 142, "FY2024": 35}),
    ("TOTAL", "Total assets", {"FY2025": 13973, "FY2024": 14962}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer accounts", {"FY2025": 397, "FY2024": 411}),
    ("DATA", "Other liabilities", {"FY2025": 3002, "FY2024": 3849}),
    ("DATA", "Accruals and deferred income", {"FY2025": 162, "FY2024": 170}),
    ("DATA", "Dilapidation provision", {"FY2025": 68, "FY2024": 65}),
    ("TOTAL", "Total liabilities", {"FY2025": 3629, "FY2024": 4495}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 10914, "FY2024": 10914}),
    ("DATA", "Merger reserve", {"FY2025": 6768, "FY2024": 6768}),
    ("DATA", "Accumulated losses", {"FY2025": -7338, "FY2024": -7215}),
    ("TOTAL", "Total equity", {"FY2025": 10344, "FY2024": 10467}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 13973, "FY2024": 14962}),
]

bw.add_balance_sheet_sheet(
    title="Philippine National Bank (Europe) Plc — Statement of Financial Position",
    subtitle="Entity-level (solo, no subsidiaries), £'000",
    rows=balance_sheet_rows,
    sources_text=BS_PL_SOURCES,
    first_col_width=52,
    source_height=210,
    unit_suffix=" (£'000)",
)

# --- Profit & Loss ---------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Continuing operations", {}),
    ("DATA", "Interest receivable and similar income arising from debt securities", {"FY2025": 281, "FY2024": 329}),
    ("TOTAL", "Net interest income", {"FY2025": 281, "FY2024": 329}),
    ("DATA", "Fees and commission income", {"FY2025": 915, "FY2024": 913}),
    ("DATA", "Dealing profits", {"FY2025": 450, "FY2024": 460}),
    ("DATA", "Other operating income", {"FY2025": 19, "FY2024": 30}),
    ("DATA", "Losses from foreign exchange transactions", {"FY2025": -18, "FY2024": -10}),
    ("TOTAL", "Operating income", {"FY2025": 1647, "FY2024": 1722}),
    ("DATA", "Administrative expenses", {"FY2025": -2091, "FY2024": -1665}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -48, "FY2024": -46}),
    ("TOTAL", "(Loss)/profit on ordinary activities before tax", {"FY2025": -492, "FY2024": 11}),
    ("DATA", "Taxation", {"FY2025": 0, "FY2024": 0}),
    ("TOTAL", "(Loss)/profit for the year", {"FY2025": -492, "FY2024": 11}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Pension plan actuarial gain recognised", {"FY2025": 369, "FY2024": 115}),
    ("TOTAL", "Total comprehensive (loss)/income", {"FY2025": -123, "FY2024": 126}),
]

bw.add_income_statement_sheet(
    title="Philippine National Bank (Europe) Plc — Statement of Comprehensive Income",
    subtitle="Entity-level (solo, no subsidiaries), £'000. Taxation is £nil in both years (shown as \"-\" in "
             "the source), not a blank/undisclosed cell.",
    rows=income_statement_rows,
    sources_text=BS_PL_SOURCES,
    first_col_width=76,
    source_height=210,
    unit_suffix=" (£'000)",
)

# --- Statement of Changes in Equity (chronological) ------------------------
EQUITY_HEADERS = ["Called up share capital", "Merger reserve", "Accumulated losses", "Total equity"]
equity_changes_rows = [
    ("TOTAL", "Balance as at 31 December 2023", (10914, 6768, -7341, 10341)),
    ("DATA", "Profit for the year", (None, None, 11, 11)),
    ("DATA", "Change in the pension scheme asset ceiling", (None, None, 185, 185)),
    ("DATA", "Actuarial loss on pension scheme", (None, None, -70, -70)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, 126, 126)),
    ("TOTAL", "Balance as at 31 December 2024", (10914, 6768, -7215, 10467)),
    ("DATA", "(Loss) for the year", (None, None, -492, -492)),
    ("DATA", "Change in the pension scheme asset ceiling", (None, None, 741, 741)),
    ("DATA", "Actuarial loss on pension scheme", (None, None, -372, -372)),
    ("TOTAL", "Total comprehensive (loss) for the year", (None, None, -123, -123)),
    ("TOTAL", "Balance as at 31 December 2025", (10914, 6768, -7338, 10344)),
]

bw.add_equity_changes_sheet(
    title="Philippine National Bank (Europe) Plc — Statement of Changes in Equity",
    subtitle="Entity-level (solo, no subsidiaries), £'000, chronological. Opening row is the Bank's own "
             "31 December 2023 balance (the FY2024 opening position), reproduced from this document's own "
             "comparative column - not itself a covered year in this workbook's FY2024-FY2025 scope.",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=BS_PL_SOURCES + (
        "\n\nEQUITY-SHEET-SPECIFIC NOTE: zero plug rows - every movement above is a distinct line the Bank's "
        "own Statement of Changes in Equity discloses (Profit/(loss) for the year, Change in the pension scheme "
        "asset ceiling, Actuarial loss on pension scheme). Both years' Total comprehensive income/(loss) figures "
        "tie exactly to both the Statement of Comprehensive Income and the Balance Sheet's own Total equity."
    ),
)

bw.add_cash_flow_sheet(
    title="Philippine National Bank (Europe) Plc — Cash Flow Statement",
    subtitle="Not applicable — Pillar-3-only scope; see the exemption and coverage note below.",
    rows=[
        ("SECTION", "No standalone Statement of Cash Flows populated", {}),
        ("DATA", "PNBE cash-flow disclosure exemption; parent-group cash flows are not substituted.", {}),
    ],
    sources_text=ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE + "\n\n" + P3_SOURCES,
    first_col_width=78, source_height=260, unit_suffix=" (£'000)",
)

# --- Asset Quality ----------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to banks, by maturity", {}),
    ("DATA", "Payable on demand", {"FY2025": 7045, "FY2024": 8794}),
    ("DATA", "Payable in more than three months but not more than six months", {"FY2025": 5028, "FY2024": 3279}),
    ("TOTAL", "Total loans and advances to banks", {"FY2025": 12073, "FY2024": 12073}),
    ("DATA", "of which: due from parent and fellow subsidiary undertakings", {"FY2025": 134, "FY2024": 447}),
    ("SECTION", "Loans and advances to customers, by maturity", {}),
    ("DATA", "Not more than three months", {"FY2025": 1, "FY2024": 0}),
    ("DATA", "More than three months but less than one year", {"FY2025": 0, "FY2024": 1}),
    ("DATA", "More than one year but less than five years", {"FY2025": 4, "FY2024": 9}),
    ("TOTAL", "Total loans and advances to customers", {"FY2025": 5, "FY2024": 10}),
]

bw.add_asset_quality_sheet(
    title="Philippine National Bank (Europe) Plc — Asset Quality",
    subtitle="Entity-level, £'000. No IFRS 9 Stage 1/2/3 split, no impairment provision, and no credit-quality "
             "grading is disclosed for either loan category in either year.",
    rows=asset_quality_rows,
    sources_text=BS_PL_SOURCES + (
        "\n\nDATA QUALITY NOTE: this Bank carries almost no customer-facing lending book - Loans and advances "
        "to customers is £5k (2024: £10k), entirely three (2024: five) personal loans outstanding with "
        "employees, interest rates 6.0%-6.75%, repayable within three years (Note 8). No impairment provision, "
        "write-off, or IFRS 9 stage split is disclosed against this balance in either year - the Bank's own "
        "notes show no bad-debt note at all for it, consistent with its immateriality. The Bank's principal "
        "credit exposure is instead Loans and advances to banks (Note 7, its correspondent/deposit-placement "
        "business with other banks including its own parent and fellow PNB subsidiaries), shown above by "
        "maturity instead of by IFRS 9 stage since no stage split is disclosed for that balance either - this "
        "Bank is a treasury/correspondent-banking entity for its parent, not a retail or commercial lender."
    ),
    first_col_width=78,
    source_height=280,
    unit_suffix=" (£'000)",
)


def metric(name, unit, rows, note=None):
    bw.add_metric_sheet(name, unit, rows, P3_SOURCES, note=note,
                        first_col_width=48, source_height=220)


OWN_FUNDS = {"FY2025": 10344, "FY2024": 10467}
CAPITAL_RATIO = {"FY2025": "127.55%", "FY2024": "136.95%"}
TOTAL_RWA = {"FY2025": 8110, "FY2024": 7643}

metric("CET1 Capital", "GBP '000", [("Common Equity Tier 1 (CET1) capital", OWN_FUNDS)])
metric("CET1 Ratio", "%", [("CET1 capital ratio", CAPITAL_RATIO)],
       note="CET1 = Tier 1 = total capital in both reported years; PNBE states it holds no Tier 2 capital.")
metric("Tier 1 Capital", "GBP '000", [("Tier 1 capital", OWN_FUNDS)])
metric("Tier 1 Ratio", "%", [("Tier 1 capital ratio", CAPITAL_RATIO)])
metric("Total Capital", "GBP '000", [("Own funds / total capital", OWN_FUNDS)])
metric("Total Capital Ratio", "%", [("Total capital ratio", CAPITAL_RATIO)])
metric("Total RWAs", "GBP '000", [("Total risk-weighted assets", TOTAL_RWA)],
       note="Total is the sum of credit/counterparty, market and operational RWA components in each source table.")

# --- RWA Breakdown (placed right after Total RWAs, per the locked sheet order) ---
rwa_breakdown_rows = [
    ("DATA", "Credit and counterparty credit risk", {"FY2025": 4568, "FY2024": 4486}),
    ("DATA", "Market risk", {"FY2025": 370, "FY2024": 36}),
    ("DATA", "Operational risk", {"FY2025": 3172, "FY2024": 3121}),
    ("TOTAL", "Total Pillar 1 risk-weighted assets", {"FY2025": 8110, "FY2024": 7643}),
]

bw.add_rwa_breakdown_sheet(
    title="Philippine National Bank (Europe) Plc — RWA Breakdown",
    subtitle="Entity-level, GBP '000. Pillar 1 capital requirements table, by risk category.",
    rows=rwa_breakdown_rows,
    sources_text=P3_SOURCES + (
        "\n\nBoth years' tables (\"The Bank's Pillar 1 capital requirements are presented in the table "
        f"below\"), p.6 of the respective Pillar 3 Disclosures - FY2025: {P3_2025_URL}; "
        f"FY2024: {P3_2024_URL}. Ties exactly to the Total RWAs sheet's figures (FY2025: 8,110; "
        "FY2024: 7,643)."
    ),
    first_col_width=54,
    source_height=220,
    unit_suffix=" (GBP '000)",
)

UNDISCLOSED = ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"]
bw.add_not_disclosed_metric_sheets(
    UNDISCLOSED, P3_SOURCES,
    per_note={name: "No quantitative standalone PNBE disclosure was located in the FY2024 or FY2025 "
                    "Pillar 3 documents; left blank rather than estimated." for name in UNDISCLOSED},
)

bw.add_overview_sheet(
    cash_flow_totals=[], cash_flow_unit=None,
    ratios=[("CET1 Ratio", CAPITAL_RATIO), ("Tier 1 Ratio", CAPITAL_RATIO),
            ("Total Capital Ratio", CAPITAL_RATIO)],
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 13973, "FY2024": 14962}),
        ("Loans and advances to banks", {"FY2025": 12073, "FY2024": 12073}),
        ("Customer accounts", {"FY2025": 397, "FY2024": 411}),
        ("Total equity", {"FY2025": 10344, "FY2024": 10467}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Operating income", {"FY2025": 1647, "FY2024": 1722}),
        ("Administrative expenses", {"FY2025": -2091, "FY2024": -1665}),
        ("(Loss)/profit for the year", {"FY2025": -492, "FY2024": 11}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 10467, "FY2024": 10341}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": -123, "FY2024": 126}),
        ("Closing equity", {"FY2025": 10344, "FY2024": 10467}),
    ],
    equity_changes_unit="£'000",
    note=("PILLAR-3-ONLY, two-year scope (FY2024-FY2025). FY2021-FY2023 are excluded because no defensible "
          "standalone PNBE Pillar 3 quantitative disclosures were located; the Balance Sheet/P&L/Equity sheets "
          "keep the same two-year window for consistency, even though full accounts exist further back. No "
          "parent-group data is used."),
)

bw.save("/Users/armaan/code/katalysis/banks/PHILIPPINE NATIONAL BANK EUROPE FINANCIALS.xlsx")
