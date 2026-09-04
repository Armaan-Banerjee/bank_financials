import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# PILLAR-3-ONLY WORKBOOK: DB UK Bank Limited (company 00315841, FRN 140848) is a UK
# private-banking/wealth-management subsidiary of Deutsche Bank AG (via Deutsche
# Holdings Limited -> DB Investments (GB) Limited -> Deutsche Bank AG). It takes the
# FRS 101 "Cashflow Statement and related notes (IAS 7)" disclosure exemption every
# year - confirmed as a standing feature across three filing vintages 4 years apart
# (FY2021, FY2023, FY2025 Annual Reports all list the same exemption in their
# "Basis of preparation" note, and none of their Contents pages lists a cash flow
# statement). Follows the BNY Mellon International / ABC International Bank /
# Bank Mandiri Europe precedent: 13-sheet structure, Cash Flow Statement sheet
# documents the exemption instead of line items, Overview sheet omits the cash-flow
# chart.
#
# No dedicated Pillar 3 document exists and no standalone Pillar 3 page was found on
# db.com. The ONLY capital/liquidity figures found anywhere in the Annual Reports
# are: a single generic "regulatory capital ratio" (unaudited) mentioned once in the
# Going Concern paragraph of Note 1 (no CET1/Tier 1/Total Capital breakdown, no RWA,
# no £ capital amount - just the one ratio, for the report's own year only, never a
# prior-year comparative), and a Liquidity Risk KPI table (note 27/29 "Risk Report")
# giving LCR and NSFR for the current and one comparative year. All figures reported
# in GBP (the Company's functional currency) - no FX conversion needed.

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, calendar year-end (31 December)
YEAR_LABEL = {y: y for y in YEARS}

FY2025_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/00315841/filing-history/MzUxOTM5NDA3NGFkaXF6a2N4/document?format=pdf&download=0"
FY2023_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/00315841/filing-history/MzQyMDM4NDU3MmFkaXF6a2N4/document?format=pdf&download=0"
FY2021_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/00315841/filing-history/MzMzODM1NTI4NGFkaXF6a2N4/document?format=pdf&download=0"

STATEMENTS_SOURCES = (
    "Sources - DB UK Bank Limited's own audited financial statements (all scanned/image-only Companies House "
    "filings, visually transcribed):\n"
    f"FY2025/FY2024: Annual Report 2025, Statement of Profit and Loss p.25, Statement of Total Comprehensive "
    f"Income p.26, Balance Sheet p.27, Statement of Changes in Equity p.28 - {FY2025_AR_URL}\n"
    f"FY2023/FY2022: Annual Report 2023, Statement of Profit and Loss p.25, Balance Sheet p.27, Statement of "
    f"Changes in Equity p.28 - {FY2023_AR_URL}\n"
    f"FY2021 (FY2020 comparative used only for the opening equity roll-forward): Annual Report 2021, Statement of "
    f"Profit and Loss p.22, Balance Sheet p.24, Statement of Changes in Equity p.25 - {FY2021_AR_URL}\n\n"
)

STATEMENTS_PRESENTATION_NOTE = (
    "PRESENTATION NOTE: line-item structure varies across the 3 filings. Balance Sheet: FY2021-2023 label the cash "
    "line 'Cash and balances at banks'; FY2024-2025 keep the same label. 'Group relief' and 'Current tax assets' "
    "both appear as separate lines with identical values in the FY2025 report (reproduced as disclosed, not "
    "merged). 'Tangible fixed assets' / 'Tangible fixed assets held for sale' appear only in the FY2021 and FY2023 "
    "reports (nil/absent by FY2025 - the Company's only property was sold, see the equity statement's 'Transfer to "
    "Retained earnings from Revaluation reserve on sale of tangible asset' FY2023 movement). 'Deferred tax assets' "
    "first appears as an explicit line in the FY2023 report; 'Revaluation reserve' (relating to that same tangible "
    "asset) is fully released by FY2023 year-end and never reappears. 'Income tax payable' / 'Deferred tax "
    "liabilities' are shown only in the years the Company had a recognised balance - blank cells mean that year's "
    "own statement has no such line at all, not that the value is unknown. P&L: FY2021 alone discloses a small "
    "'Derivatives (loss)/gain' line, absent FY2022-2025."
)

ENTITY_NOTE = (
    "ENTITY NOTE: DB UK Bank Limited (company 00315841, FRN 140848, incorporated 30 June 1936) is a wholly-owned "
    "subsidiary of Deutsche Holdings Limited (\"DHL\"), itself wholly owned by DB Investments (GB) Limited "
    "(\"DBIGB\"), whose parent is Deutsche Bank Aktiengesellschaft (\"DB AG\", Germany). The Company provides "
    "Wealth Management services to High and Ultra High Net Worth clients as part of Deutsche Bank's Private Bank. "
    "All figures below are on the Company's own entity-level basis - it has no subsidiaries of its own."
)

EXEMPTION_NOTE = (
    "FRS 101 CASH-FLOW EXEMPTION: the FY2025 Annual Report's Note 1 \"Basis of preparation\" states the Company has "
    "applied the FRS 101 exemptions available in respect of, among others, \"A Cashflow Statement and related notes "
    "(the requirements of IAS 7 Statement of Cash Flows and the requirements of paragraphs 10(d) and 111 of IAS 1)\" "
    f"- DB UK Bank Limited Annual Report 2025, p.29 - {FY2025_AR_URL}. The identical exemption (worded slightly more "
    f"briefly, \"A Cashflow Statement and related notes\") appears in the FY2023 Annual Report (p.29 - "
    f"{FY2023_AR_URL}) and the FY2021 Annual Report (p.26 - {FY2021_AR_URL}), confirming this is a standing "
    "structural feature across the entity's history (checked 4 years apart), not a one-off. None of the three "
    "filings' own Contents pages lists a cash flow statement. Per the project's established policy for this "
    "exemption (see The Bank of New York Mellon (International) Limited / ABC International Bank plc / Bank "
    "Mandiri (Europe) Limited), this workbook is built as a PILLAR-3-ONLY variant: the capital/liquidity metrics "
    "that are disclosed are populated below, but no cash flow figures exist to show."
)

CASH_FLOW_SOURCES = ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE

NOT_DISCLOSED_NOTE = (
    "No dedicated Pillar 3 document is published by this entity, and no separate regulatory-disclosures page for "
    "DB UK Bank Limited was found on db.com. The only capital/liquidity figures found anywhere in the FY2021, "
    "FY2023 and FY2025 Annual Reports (the three filings checked) are a single generic \"regulatory capital ratio\" "
    "(see Total Capital Ratio sheet) and LCR/NSFR (see those sheets) - this metric is not disclosed in any form in "
    "any of the three filings checked."
)


def p3_sources(extra=""):
    return (
        "Sources - DB UK Bank Limited, all figures GBP (no FX conversion needed):\n"
        f"FY2025: Annual Report 2025, Note 1 Going Concern paragraph (regulatory capital ratio, p.29) and Note 27 "
        f"Risk Report (c) Liquidity Risk KPI table (LCR/NSFR, p.65) - {FY2025_AR_URL}\n"
        f"FY2024: Annual Report 2025's own FY2024 comparative column in the same Note 27 Liquidity Risk KPI table "
        f"(p.65) - {FY2025_AR_URL}. No FY2024 capital ratio found (the going-concern note only ever states the "
        "report's own current year, never a prior-year comparative) - left blank, not estimated.\n"
        f"FY2023: Annual Report 2023, Note 1 Going Concern paragraph (regulatory capital ratio, p.29) and Note 29 "
        f"Risk Report (c) Liquidity Risk KPI table (LCR/NSFR, p.65) - {FY2023_AR_URL}\n"
        f"FY2022: Annual Report 2023's own FY2022 comparative column in the same Note 29 Liquidity Risk KPI table "
        f"(p.65) - {FY2023_AR_URL}. No FY2022 capital ratio found (same reason as FY2024) - left blank.\n"
        f"FY2021: Annual Report 2021, Note 1 Going Concern paragraph (regulatory capital ratio and LCR, p.26) - "
        f"{FY2021_AR_URL}. No NSFR for FY2021 - the Company's own FY2023 Annual Report states NSFR only became a "
        "regulatory requirement \"from 1 January 2022\", consistent with no NSFR being mentioned anywhere in the "
        "FY2021 report - left blank, not estimated, not a gap.\n"
        + (extra + "\n" if extra else "")
    )


bw = BankWorkbook(bank_name="DB UK Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="995A1C")

# ---------------------------------------------------------------
# Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at banks", {"FY2025": 29950, "FY2024": 14251, "FY2023": 23617, "FY2022": 23201, "FY2021": 17554}),
    ("DATA", "Loans and advances to banks", {"FY2025": 1423630, "FY2024": 1684974, "FY2023": 1207263, "FY2022": 1486499, "FY2021": 987264}),
    ("DATA", "Loans and advances to customers", {"FY2025": 925756, "FY2024": 1387504, "FY2023": 836432, "FY2022": 845537, "FY2021": 637226}),
    ("DATA", "Derivatives", {"FY2025": 242, "FY2024": 3252, "FY2023": 185, "FY2022": 298, "FY2021": 0}),
    ("DATA", "Other assets", {"FY2025": 35701, "FY2024": 37371, "FY2023": 32634, "FY2022": 10806, "FY2021": 16966}),
    ("DATA", "Group relief", {"FY2025": 946, "FY2024": 185, "FY2023": 0, "FY2022": 3900, "FY2021": 2882}),
    ("DATA", "Current tax assets", {"FY2025": 946, "FY2024": 185}),
    ("DATA", "Tangible fixed assets", {"FY2023": 1, "FY2022": 1, "FY2021": 10342}),
    ("DATA", "Tangible fixed assets held for sale", {"FY2023": 0, "FY2022": 10340}),
    ("DATA", "Intangible fixed assets", {"FY2025": 11499, "FY2024": 10360, "FY2023": 9689, "FY2022": 7619, "FY2021": 5937}),
    ("DATA", "Deferred tax assets", {"FY2025": 1094, "FY2024": 969, "FY2023": 905, "FY2022": 0}),
    ("TOTAL", "Total assets", {"FY2025": 2429764, "FY2024": 3139051, "FY2023": 2110726, "FY2022": 2388201, "FY2021": 1678171}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2025": 1202489, "FY2024": 2121221, "FY2023": 906382, "FY2022": 1011051, "FY2021": 751088}),
    ("DATA", "Customer accounts", {"FY2025": 583015, "FY2024": 362851, "FY2023": 542146, "FY2022": 741604, "FY2021": 289877}),
    ("DATA", "Derivatives", {"FY2025": 241, "FY2024": 3252, "FY2023": 185, "FY2022": 298, "FY2021": 0}),
    ("DATA", "Other liabilities", {"FY2025": 18271, "FY2024": 20930, "FY2023": 25305, "FY2022": 23845, "FY2021": 21257}),
    ("DATA", "Accruals and deferred income", {"FY2025": 9870, "FY2024": 7968, "FY2023": 7117, "FY2022": 6799, "FY2021": 6297}),
    ("DATA", "Provisions for liabilities", {"FY2025": 1004, "FY2024": 1117, "FY2023": 1165, "FY2022": 1201, "FY2021": 1471}),
    ("DATA", "Income tax payable", {"FY2023": 6556, "FY2022": 0}),
    ("DATA", "Deferred tax liabilities", {"FY2023": 0, "FY2022": 1565, "FY2021": 2106}),
    ("TOTAL", "Total liabilities", {"FY2025": 1814890, "FY2024": 2517339, "FY2023": 1488856, "FY2022": 1786363, "FY2021": 1072096}),
    ("SECTION", "Shareholder's funds", {}),
    ("DATA", "Called up share capital", {"FY2025": 385000, "FY2024": 385000, "FY2023": 385000, "FY2022": 385000, "FY2021": 385000}),
    ("DATA", "Revaluation reserve", {"FY2023": 0, "FY2022": 6919, "FY2021": 6557}),
    ("DATA", "Profit and loss account", {"FY2025": 229874, "FY2024": 236712, "FY2023": 236870, "FY2022": 209919, "FY2021": 214518}),
    ("TOTAL", "Shareholder's funds", {"FY2025": 614874, "FY2024": 621712, "FY2023": 621870, "FY2022": 601838, "FY2021": 606075}),
    ("TOTAL", "Total liabilities and shareholder's funds", {"FY2025": 2429764, "FY2024": 3139051, "FY2023": 2110726, "FY2022": 2388201, "FY2021": 1678171}),
]

bw.add_balance_sheet_sheet(
    title="DB UK Bank Limited — Balance Sheet",
    subtitle="Entity-level basis, £'000.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES + STATEMENTS_PRESENTATION_NOTE + "\n\n" + ENTITY_NOTE,
    first_col_width=64,
    source_height=400,
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable", {"FY2025": 105428, "FY2024": 121745, "FY2023": 117677, "FY2022": 47627, "FY2021": 14898}),
    ("DATA", "Interest payable", {"FY2025": -63128, "FY2024": -73163, "FY2023": -72605, "FY2022": -24013, "FY2021": -4270}),
    ("TOTAL", "Net interest income", {"FY2025": 42300, "FY2024": 48582, "FY2023": 45072, "FY2022": 23614, "FY2021": 10628}),
    ("DATA", "Fees and commissions receivable", {"FY2025": 9026, "FY2024": 7924, "FY2023": 8218, "FY2022": 7933, "FY2021": 7205}),
    ("DATA", "Fees and commissions payable", {"FY2025": -2290, "FY2024": -1841, "FY2023": -1009, "FY2022": -903, "FY2021": -948}),
    ("DATA", "Foreign exchange gain/(loss)", {"FY2025": 588, "FY2024": 444, "FY2023": 286, "FY2022": 105, "FY2021": -72}),
    ("DATA", "Derivatives (loss)/gain", {"FY2021": -1}),
    ("DATA", "Other operating income", {"FY2025": 11037, "FY2024": 12262, "FY2023": 9361, "FY2022": 6925, "FY2021": 6424}),
    ("TOTAL", "Operating income", {"FY2025": 60661, "FY2024": 67371, "FY2023": 61928, "FY2022": 37674, "FY2021": 23236}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Administrative expenses", {"FY2025": -41255, "FY2024": -40542, "FY2023": -36098, "FY2022": -41566, "FY2021": -32396}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -1562, "FY2024": -1550, "FY2023": -979, "FY2022": -1090, "FY2021": -1329}),
    ("DATA", "Other operating charges", {"FY2025": -55, "FY2024": -44, "FY2023": -827, "FY2022": -76, "FY2021": -37}),
    ("DATA", "Impairment on financial instruments", {"FY2025": -1168, "FY2024": -68, "FY2023": 411, "FY2022": -571, "FY2021": 91}),
    ("TOTAL", "Profit/(loss) on ordinary activities before taxation", {"FY2025": 16621, "FY2024": 25167, "FY2023": 24435, "FY2022": -5629, "FY2021": -10435}),
    ("DATA", "Taxation on profit/(loss) on ordinary activities", {"FY2025": -4571, "FY2024": -7102, "FY2023": -6795, "FY2022": 1223, "FY2021": 2987}),
    ("TOTAL", "Profit/(loss) for the financial year", {"FY2025": 12050, "FY2024": 18065, "FY2023": 17640, "FY2022": -4406, "FY2021": -7448}),
]

bw.add_income_statement_sheet(
    title="DB UK Bank Limited — Profit & Loss",
    subtitle="Entity-level basis, £'000. No other comprehensive income in any year (Statement of Total Comprehensive "
              "Income shows only Profit/(loss) for the financial year every year - confirmed by reading each year's "
              "own statement in full).",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES + STATEMENTS_PRESENTATION_NOTE + "\n\n" + ENTITY_NOTE,
    first_col_width=64,
    source_height=400,
)

# ---------------------------------------------------------------
# Statement of Changes in Equity (chronological) - built using the per-year
# reconciliation ladder: Balance Sheet built first (above), then each year's
# closing balance checked against both the next year's own opening balance
# and that year's own Balance Sheet Total. Ties exactly at every boundary,
# no plug rows needed anywhere.
# ---------------------------------------------------------------
equity_changes_rows = [
    ("TOTAL", "At 1 January 2021", (385000, 6991, 222468, 614459)),
    ("DATA", "Loss for the financial year (FY2021)", (None, None, -7448, -7448)),
    ("DATA", "Equity-settled share-based compensation, net of tax (FY2021)", (None, None, -502, -502)),
    ("DATA", "Impact on Revaluation reserve of change in tax rate (FY2021)", (None, -434, None, -434)),
    ("TOTAL", "At 31 December 2021", (385000, 6557, 214518, 606075)),
    ("DATA", "Loss for the financial year (FY2022)", (None, None, -4406, -4406)),
    ("DATA", "Equity-settled share-based compensation, net of tax (FY2022)", (None, None, -193, -193)),
    ("DATA", "Impact on Revaluation reserve of change in tax rate (FY2022)", (None, 362, None, 362)),
    ("TOTAL", "At 31 December 2022", (385000, 6919, 209919, 601838)),
    ("DATA", "Profit for the financial year (FY2023)", (None, None, 17640, 17640)),
    ("DATA", "Equity-settled share-based compensation, net of tax (FY2023)", (None, None, -265, -265)),
    ("DATA", "Release of deferred tax liability on Revaluation reserve (FY2023)", (None, 2657, None, 2657)),
    ("DATA", "Transfer to Retained earnings from Revaluation reserve on sale of tangible asset (FY2023)", (None, -9576, 9576, 0)),
    ("TOTAL", "At 31 December 2023", (385000, 0, 236870, 621870)),
    ("DATA", "Profit for the financial year (FY2024)", (None, None, 18065, 18065)),
    ("DATA", "Dividends paid during the year (FY2024)", (None, None, -17640, -17640)),
    ("DATA", "Equity-settled share-based compensation, net of tax (FY2024)", (None, None, -583, -583)),
    ("TOTAL", "At 31 December 2024", (385000, 0, 236712, 621712)),
    ("DATA", "Profit for the financial year (FY2025)", (None, None, 12050, 12050)),
    ("DATA", "Dividends paid during the year (FY2025)", (None, None, -18065, -18065)),
    ("DATA", "Equity-settled share-based compensation, net of tax (FY2025)", (None, None, -823, -823)),
    ("TOTAL", "At 31 December 2025", (385000, 0, 229874, 614874)),
]

bw.add_equity_changes_sheet(
    title="DB UK Bank Limited — Statement of Changes in Equity",
    subtitle="Entity-level basis, £'000. Chronological roll-forward, oldest to newest. GBP throughout - no FX "
              "conversion needed. Ties exactly to the Balance Sheet's own Shareholder's funds at every year-end.",
    headers=["Called up share capital", "Revaluation reserve", "Profit and loss account", "Total equity"],
    rows=equity_changes_rows,
    sources_text=STATEMENTS_SOURCES + STATEMENTS_PRESENTATION_NOTE + "\n\n" + ENTITY_NOTE,
    first_col_width=68,
    source_height=400,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (exemption note in place of line items)
# ---------------------------------------------------------------
rows = [
    ("SECTION", "No Statement of Cash Flows is published by this entity in any year", {}),
    ("DATA", "See the note below for the FRS 101 exemption this entity relies on every year, and why this "
             "workbook is built as a Pillar-3-only variant.", {}),
]

bw.add_cash_flow_sheet(
    title="DB UK Bank Limited — Cash Flow Statement",
    subtitle="Not applicable — this entity takes the FRS 101 cash-flow-statement disclosure exemption every year. See source note below.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=300,
    unit_suffix="",
)

# ---------------------------------------------------------------
# Asset Quality: the Company's own "Overview of financial assets subject to
# impairment by IFRS 9 Stage" note covers ALL ECL-bearing financial assets
# (cash at banks, loans to banks, loans to customers, other assets) - used
# here in full (same "richer than customer-loans-alone" treatment as BNY
# Mellon International/Bank Sepah International), not narrowed to the
# customer loan book alone. Disclosure basis is consistent across all 5
# years (same note structure every year, unlike some other banks in this
# project).
# ---------------------------------------------------------------
AQ_STAGE1 = {"FY2025": 2315179, "FY2024": 3116983, "FY2023": 2068670, "FY2022": 2351365, "FY2021": 1626980}
AQ_STAGE2 = {"FY2025": 101901, "FY2024": 11005, "FY2023": 21590, "FY2022": 19853, "FY2021": 19508}
AQ_STAGE3 = {"FY2025": 0, "FY2024": 0, "FY2023": 10439, "FY2022": 0, "FY2021": 15793}
AQ_TOTAL = {y: AQ_STAGE1[y] + AQ_STAGE2[y] + AQ_STAGE3[y] for y in YEARS}
AQ_PROV1 = {"FY2025": 1370, "FY2024": 633, "FY2023": 550, "FY2022": 939, "FY2021": 396}
AQ_PROV2 = {"FY2025": 431, "FY2024": 3, "FY2023": 18, "FY2022": 38, "FY2021": 12}
AQ_PROV3 = {y: 0 for y in YEARS}
AQ_PROV_TOTAL = {y: AQ_PROV1[y] + AQ_PROV2[y] + AQ_PROV3[y] for y in YEARS}
AQ_STAGE3_RATIO = {y: f"{AQ_STAGE3[y] / AQ_TOTAL[y] * 100:.2f}%" for y in YEARS}
AQ_COVERAGE = {y: f"{AQ_PROV_TOTAL[y] / AQ_TOTAL[y] * 100:.4f}%" for y in YEARS}

asset_quality_rows = [
    ("SECTION", "Total assets in scope by IFRS 9 stage, across all ECL-bearing financial assets "
                "(cash and balances at banks, loans and advances to banks, loans and advances to customers, "
                "other assets)", {}),
    ("DATA", "Stage 1 (12-month ECL)", AQ_STAGE1),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", AQ_STAGE2),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired)", AQ_STAGE3),
    ("TOTAL", "Total assets in scope", AQ_TOTAL),
    ("SECTION", "Provisions for impairment (on-balance-sheet, by stage)", {}),
    ("DATA", "Stage 1 provisions", AQ_PROV1),
    ("DATA", "Stage 2 provisions", AQ_PROV2),
    ("DATA", "Stage 3 provisions", AQ_PROV3),
    ("TOTAL", "Total provisions for impairment", AQ_PROV_TOTAL),
    ("SECTION", "Ratios", {}),
    ("DATA", "Stage 3 exposure ratio (Stage 3 / total assets in scope)", AQ_STAGE3_RATIO),
    ("DATA", "Overall coverage ratio (total provisions / total assets in scope)", AQ_COVERAGE),
]

bw.add_asset_quality_sheet(
    title="DB UK Bank Limited — Asset Quality / Credit Risk Disclosures",
    subtitle="Overview of financial assets subject to impairment by IFRS 9 Stage, £'000. Entity-level basis.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - DB UK Bank Limited's own 'Provisions for impairment on financial instruments' note (all "
        "scanned/image-only Companies House filings, visually transcribed):\n"
        f"FY2025/FY2024: Annual Report 2025, Note 14, p.55 - {FY2025_AR_URL}\n"
        f"FY2023/FY2022: Annual Report 2023, Note 14, p.54 - {FY2023_AR_URL}\n"
        f"FY2021: Annual Report 2021, Note 15, p.48 - {FY2021_AR_URL}\n\n"
        "Note: FY2023 is the only year with a nonzero Stage 3 balance under this table's methodology - two assets "
        "totalling £10,439k met the Stage 3 (default) criteria that year, with no provision considered necessary "
        "due to the value of collateral held (Annual Report 2023, Note 14, p.55). FY2021's own comparative FY2020 "
        "column (not shown here) also carried a Stage 3 balance (£7,298k) - both are genuine period features, not "
        "gaps.\n\n" + ENTITY_NOTE
    ),
    first_col_width=90,
    source_height=340,
)

# ---------------------------------------------------------------
# RWA Breakdown - not publicly disclosed (see NOT_DISCLOSED_NOTE below):
# no dedicated Pillar 3 document exists for this entity and no RWA figure
# (aggregate or by category) appears anywhere in any of the 3 Annual
# Reports checked - only a single generic "regulatory capital ratio" (see
# Total Capital Ratio sheet).
# ---------------------------------------------------------------
rwa_breakdown_rows = [
    ("DATA", "Not publicly disclosed - no RWA figure (aggregate or by category) appears anywhere in the "
             "FY2021, FY2023 or FY2025 Annual Reports checked, and no dedicated Pillar 3 document is published "
             "by this entity. See the Total Capital Ratio sheet for the only capital-related ratio disclosed.", {}),
]

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=170)


TOTAL_CAPITAL_RATIO = {"FY2025": "536%", "FY2023": "491%", "FY2021": "473%"}
LCR = {"FY2025": "381%", "FY2024": "351%", "FY2023": "437%", "FY2022": "304%", "FY2021": "459%"}
NSFR = {"FY2025": "202%", "FY2024": "140%", "FY2023": "213%", "FY2022": "235%"}

# Sheet order matches the project-wide standard (CET1 Capital/Ratio, Tier 1 Capital/Ratio,
# Total Capital/Ratio, Total RWAs, Leverage Ratio, LCR, NSFR, MREL Ratio) even though this
# entity only discloses Total Capital Ratio/LCR/NSFR.
bw.add_not_disclosed_metric_sheets(
    ["CET1 Capital", "CET1 Ratio", "Tier 1 Capital", "Tier 1 Ratio", "Total Capital"],
    p3_sources(),
    per_note={m: NOT_DISCLOSED_NOTE for m in
              ["CET1 Capital", "CET1 Ratio", "Tier 1 Capital", "Tier 1 Ratio", "Total Capital"]},
)

metric(
    "Total Capital Ratio", "% (unaudited)",
    [("Regulatory capital ratio", TOTAL_CAPITAL_RATIO)],
    p3_sources(),
    note="Only a single generic 'regulatory capital ratio' is disclosed, mentioned once in each report's Going "
         "Concern paragraph - no CET1/Tier 1 breakdown exists anywhere, and no £ capital amount or RWA figure is "
         "disclosed either (so Total RWAs cannot be calculated). This ratio is described only as 'well above the "
         "regulatory minimum of 100%' and is explicitly marked unaudited in the source. Placed on Total Capital "
         "Ratio (the broadest measure) rather than assumed equal to CET1/Tier 1, since the source never specifies "
         "which capital tier(s) the ratio uses.",
)

bw.add_not_disclosed_metric_sheets(
    ["Total RWAs"],
    p3_sources(),
    per_note={"Total RWAs": NOT_DISCLOSED_NOTE},
)

bw.add_rwa_breakdown_sheet(
    title="DB UK Bank Limited — RWA Breakdown",
    subtitle="See source note - no RWA figure is published for this entity.",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources(),
    first_col_width=90,
    source_height=220,
)

bw.add_not_disclosed_metric_sheets(
    ["Leverage Ratio"],
    p3_sources(),
    per_note={"Leverage Ratio": NOT_DISCLOSED_NOTE},
)

metric(
    "LCR", "% (unaudited)",
    [("Liquidity Coverage Ratio", LCR)],
    p3_sources(),
    note="No £ breakdown (HQLA, net cash outflows) is disclosed anywhere - only the ratio itself. Explicitly "
         "marked unaudited in the source (Risk Report note (c) Liquidity Risk is headed '(unaudited)').",
)

metric(
    "NSFR", "% (unaudited)",
    [("Net Stable Funding Ratio", NSFR)],
    p3_sources(),
    note="No £ breakdown (available/required stable funding) is disclosed anywhere - only the ratio itself. "
         "FY2021 genuinely blank: the Company's own FY2023 Annual Report states NSFR only became a regulatory "
         "requirement from 1 January 2022, and no NSFR figure appears anywhere in the FY2021 Annual Report.",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources(), per_note={"MREL Ratio": NOT_DISCLOSED_NOTE},
)

# ---------------------------------------------------------------
# Overview sheet (Pillar-3-only: no cash-flow chart)
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 2429764, "FY2024": 3139051, "FY2023": 2110726, "FY2022": 2388201, "FY2021": 1678171}),
        ("Loans and advances to customers", {"FY2025": 925756, "FY2024": 1387504, "FY2023": 836432, "FY2022": 845537, "FY2021": 637226}),
        ("Customer accounts", {"FY2025": 583015, "FY2024": 362851, "FY2023": 542146, "FY2022": 741604, "FY2021": 289877}),
        ("Shareholder's funds", {"FY2025": 614874, "FY2024": 621712, "FY2023": 621870, "FY2022": 601838, "FY2021": 606075}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Operating income", {"FY2025": 60661, "FY2024": 67371, "FY2023": 61928, "FY2022": 37674, "FY2021": 23236}),
        ("Administrative expenses", {"FY2025": -41255, "FY2024": -40542, "FY2023": -36098, "FY2022": -41566, "FY2021": -32396}),
        ("Profit/(loss) for the financial year", {"FY2025": 12050, "FY2024": 18065, "FY2023": 17640, "FY2022": -4406, "FY2021": -7448}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 621712, "FY2024": 621870, "FY2023": 601838, "FY2022": 606075, "FY2021": 614459}),
        ("Profit/(loss) for the year", {"FY2025": 12050, "FY2024": 18065, "FY2023": 17640, "FY2022": -4406, "FY2021": -7448}),
        ("Other movements, net", {"FY2025": -18888, "FY2024": -18223, "FY2023": 2392, "FY2022": 169, "FY2021": -936}),
        ("Closing equity", {"FY2025": 614874, "FY2024": 621712, "FY2023": 621870, "FY2022": 601838, "FY2021": 606075}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("Total Capital Ratio", TOTAL_CAPITAL_RATIO),
        ("LCR", LCR),
        ("NSFR", NSFR),
    ],
    note="No cash flow summary or chart is shown here: DB UK Bank Limited takes the FRS 101 cash-flow-statement "
         "exemption every year (see the Cash Flow Statement sheet). Balance Sheet, Profit & Loss and Statement of "
         "Changes in Equity headline blocks are all fully populated below. No dedicated Pillar 3 document is "
         "published by this entity; only a single generic 'regulatory capital ratio' (no CET1/Tier 1 breakdown, 3 "
         "of 5 years only), LCR (5 of 5 years) and NSFR (4 of 5 years, not applicable pre-2022) are disclosed, "
         "each in a different part of the Annual Report's own Notes - see each sheet's own source citation.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/DB UK BANK FINANCIALS.xlsx")
