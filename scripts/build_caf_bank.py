import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# CAF Bank Limited (Companies House 01837656, FRN 204451), owned by Charities
# Aid Foundation (CAF), serves charities/non-profits. Fiscal year-end 30 April.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/01837656/filing-history"
AR2025_URL = f"{CH_BASE}/MzUwNDA1NTExOGFkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = f"{CH_BASE}/MzM5MjYwNDE2NmFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = f"{CH_BASE}/MzMxMTMwNTcwNWFkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "ENTITY NOTE: CAF Bank Limited (Companies House 01837656, FRN 204451, formerly Cafcash Limited) is a UK bank "
    "wholly owned by the Charities Aid Foundation (CAF, registered charity 268369), serving charities/non-profits. "
    "It takes no FRS 101/102 cash-flow exemption - full Cash Flow Statement every year. All 3 source Companies "
    "House filings used (FY2025, FY2023-with-FY2022-comparative, FY2021) are fully scanned/image-only (0 text "
    "blocks/page) - every figure was transcribed via high-resolution page-image review, cross-checked against the "
    "following year's comparative column where available. FY2024's own standalone filing was not needed since "
    "FY2025's filing carries it as a comparative; FY2022's standalone filing was likewise not needed since FY2023's "
    "filing carries it as a comparative.\n\n"
    "DATA QUALITY NOTE: the FY2025 column's 'Net cash generated from operating activities' total (£20,729k) and "
    "'Net cash used in investing activities' total (£60,368k) are both independently corroborated - they sum "
    "exactly to the stated 'Change in cash and cash equivalents in the year' (£(39,639)k), and the closing balance "
    "these imply matches the 'Represented by' breakdown exactly. However, one underlying adjustment line "
    "('Amortisation of investments') is genuinely ambiguous in the source scan between the two plausible digit "
    "readings £(6,041)k and £(8,041)k - only the former makes the itemised adjustments sum exactly to the stated "
    "operating total, so £(6,041)k is used here as the internally-consistent figure (the same approach used "
    "elsewhere in this project for LHV/Zempler/Vanquis source-document ambiguities). The FY2024 comparative "
    "column's own itemised lines sum exactly to its own stated totals with no ambiguity.\n\n"
    "No Pillar 3 disclosure, standalone or embedded, was found anywhere for this entity: the Annual Report itself "
    "(Strategic Report, Risk management report, and all Notes to the Financial Statements) contains no CET1/"
    "Tier 1/Total Capital £ figures, no Total RWAs, no Leverage Ratio, no LCR/NSFR, and no MREL Ratio in any of "
    "the 5 years reviewed - only a passing reference to 'ICAAP and liquidity adequacy assessments' as a governance "
    "activity, with no figures given. No standalone Pillar 3 document exists on CAF Bank's own site or CAF's "
    "wider governance/regulatory-disclosures pages. All 11 Pillar 3 metrics are therefore 'Not publicly "
    "disclosed', consistent with a small, non-complex institution under simplified UK prudential disclosure rules."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are CAF Bank Limited's own Cash Flow Statement, transcribed from each year's own "
    "Companies House filing (or, for FY2024/FY2022, that year's own comparative column in the following year's "
    "filing):\n"
    f"FY2025/FY2024: Full accounts made up to 30 April 2025 (filed 10 Feb 2026), Cash Flow Statement - {AR2025_URL}\n"
    f"FY2023/FY2022: Full accounts made up to 30 April 2023 (filed 14 Sep 2023), Cash Flow Statement - {AR2023_URL}\n"
    f"FY2021: Full accounts made up to 30 April 2021 (filed 31 Aug 2021), Cash Flow Statement - {AR2021_URL}\n"
    + ENTITY_NOTE
)

bw = BankWorkbook(bank_name="CAF Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="2E7D32")

STATEMENTS_SOURCES = (
    "Sources - all figures are CAF Bank Limited's own Profit and Loss Account / Balance Sheet / Statement of "
    "Changes in Equity, transcribed from each year's own Companies House filing (or, for FY2024/FY2022, that "
    "year's own comparative column in the following year's filing):\n"
    f"FY2025/FY2024: Full accounts made up to 30 April 2025 (filed 10 Feb 2026), Profit and loss account/Balance "
    f"sheet/Statement of changes in equity - {AR2025_URL}\n"
    f"FY2023/FY2022: Full accounts made up to 30 April 2023 (filed 14 Sep 2023), Profit and loss account/Balance "
    f"sheet/Statement of changes in equity - {AR2023_URL}\n"
    f"FY2021: Full accounts made up to 30 April 2021 (filed 31 Aug 2021), Profit and loss account/Balance sheet - "
    f"{AR2021_URL}\n"
    + ENTITY_NOTE
    + "\n\nPRESENTATION NOTE: the Statement of Changes in Equity had 4 equity components (Called-up share "
    "capital, Additional Tier 1 securities, Distributable reserve, Retained earnings) through FY2023; the AT1 "
    "securities were redeemed and the distributable reserve fully transferred to retained earnings during "
    "FY2023, leaving only 2 components (Called-up share capital, Retained earnings) from FY2024 onward. "
    "DISCREPANCY NOTE: the FY2021 filing's own Balance Sheet shows the Distributable reserve at 30 April 2021 as "
    "£939k, but the FY2023 filing's own equity reconciliation shows the same opening balance (at 1 May 2021) as "
    "£1,000k - a £61k gap between the two source filings, reproduced here as each document states it rather than "
    "silently reconciled."
)

ASSET_QUALITY_SOURCES = (
    "Sources - CAF Bank Limited's own Notes to the Financial Statements (Note 10, Loans and advances to "
    f"customers, p.43 of {AR2021_URL} for FY2021's individual/collective impairment tables), same filings as "
    "STATEMENTS_SOURCES above.\n"
    + ENTITY_NOTE
    + "\n\nDISCLOSURE GRANULARITY NOTE: this is an FRS 102 bank (not IFRS 9), so there is no Stage 1/2/3 split - "
    "only an individual/collective impairment provision split. FY2021's own filing (Note 10, p.43) does in fact "
    "disclose this split (Individual impairments provision closing balance £(1,376)k, Collective impairments "
    "provision closing balance £(802)k, summing to the £(2,178)k aggregate) - found on a follow-up pass after an "
    "earlier build initially left FY2021 blank, having assumed (without having actually located the note) that "
    "the split was only disclosed from FY2024 onward. FY2022/FY2023 were not re-checked in this follow-up pass "
    "for a similar split (their columns above still show the single aggregate figure only, £(1,078)k/£(1,651)k, "
    "as originally sourced) - worth a similar check if those years are revisited."
)

# ---------------------------------------------------------------
# Sheet 1: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Balances at Bank of England", {"FY2025": 610671, "FY2024": 630526, "FY2023": 620476, "FY2022": 602553, "FY2021": 417756}),
    ("DATA", "Loans and advances to banks", {"FY2025": 4214, "FY2024": 23998, "FY2023": 6116, "FY2022": 7471, "FY2021": 7897}),
    ("DATA", "Loans and advances to customers", {"FY2025": 219101, "FY2024": 197701, "FY2023": 177734, "FY2022": 160407, "FY2021": 124506}),
    ("DATA", "Debt securities", {"FY2025": 682783, "FY2024": 637376, "FY2023": 752100, "FY2022": 777145, "FY2021": 885876}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 11882, "FY2024": 10566, "FY2023": 8775, "FY2022": 3792, "FY2021": 4067}),
    ("DATA", "Intangible assets", {"FY2025": 15908, "FY2024": 10758, "FY2023": 6333, "FY2022": 4676, "FY2021": 1194}),
    ("TOTAL", "Total assets", {"FY2025": 1544559, "FY2024": 1510925, "FY2023": 1571534, "FY2022": 1556044, "FY2021": 1441296}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer accounts", {"FY2025": 1450926, "FY2024": 1419433, "FY2023": 1505425, "FY2022": 1508937, "FY2021": 1398146}),
    ("DATA", "Repurchase agreements", {"FY2025": 12394, "FY2024": 13852, "FY2023": 8852, "FY2021": 0}),
    ("DATA", "Other liabilities", {"FY2025": 5000, "FY2024": 7540, "FY2023": 5784, "FY2022": 4178, "FY2021": 1848}),
    ("DATA", "Accruals and deferred income", {"FY2021": 13}),
    ("DATA", "Subordinated debt", {"FY2024": 5000}),
    ("TOTAL", "Total liabilities", {"FY2025": 1468320, "FY2024": 1445825, "FY2023": 1520061, "FY2022": 1513115, "FY2021": 1400007}),
    ("SECTION", "Shareholders' funds", {}),
    ("DATA", "Called up share capital", {"FY2025": 40319, "FY2024": 40319, "FY2023": 40319, "FY2022": 29350, "FY2021": 29350}),
    ("DATA", "Additional Tier 1 capital", {"FY2022": 11000, "FY2021": 11000}),
    ("DATA", "Distributable reserve", {"FY2022": 1000, "FY2021": 939}),
    ("DATA", "Retained earnings", {"FY2025": 35920, "FY2024": 24781, "FY2023": 11154, "FY2022": 1579, "FY2021": -61}),
    ("TOTAL", "Total shareholders' funds", {"FY2025": 76239, "FY2024": 65100, "FY2023": 51473, "FY2022": 42929, "FY2021": 41289}),
    ("TOTAL", "Total liabilities and shareholders' funds", {"FY2025": 1544559, "FY2024": 1510925, "FY2023": 1571534, "FY2022": 1556044, "FY2021": 1441296}),
]

bw.add_balance_sheet_sheet(
    title="CAF Bank Limited — Balance Sheet",
    subtitle="CAF Bank Limited's own basis, £'000. See source note at bottom.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=88,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet 2: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable", {"FY2025": 66478, "FY2024": 65025, "FY2023": 35396, "FY2022": 10823, "FY2021": 10059}),
    ("DATA", "Interest payable", {"FY2025": -20929, "FY2024": -20250, "FY2023": -7350, "FY2022": -182, "FY2021": -263}),
    ("TOTAL", "Net interest income", {"FY2025": 45549, "FY2024": 44775, "FY2023": 28046, "FY2022": 10641, "FY2021": 9796}),
    ("DATA", "Fees and commissions receivable", {"FY2025": 2744, "FY2024": 2710, "FY2023": 2560, "FY2022": 2947, "FY2021": 2230}),
    ("DATA", "Fees and commissions payable", {"FY2025": -989, "FY2024": -945, "FY2023": -913, "FY2022": -885, "FY2021": -815}),
    ("TOTAL", "Net fee income", {"FY2025": 1755, "FY2024": 1765, "FY2023": 1647, "FY2022": 2062, "FY2021": 1415}),
    ("TOTAL", "Net operating income", {"FY2025": 47304, "FY2024": 46540, "FY2023": 29693, "FY2022": 12703, "FY2021": 11211}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Administrative expenses", {"FY2025": -32827, "FY2024": -27655, "FY2023": -18472, "FY2022": -11774, "FY2021": -9763}),
    ("DATA", "Loan loss provision credit/(charge)", {"FY2025": 184, "FY2024": -716, "FY2023": -573, "FY2022": 1100, "FY2021": -533}),
    ("TOTAL", "Profit on ordinary activities before taxation", {"FY2025": 14661, "FY2024": 18169, "FY2023": 10648, "FY2022": 2029, "FY2021": 915}),
    ("DATA", "Tax on profit on ordinary activities", {"FY2025": -2522, "FY2024": -4542, "FY2023": -2073, "FY2022": -389, "FY2021": 14}),
    ("TOTAL", "Profit on ordinary activities after taxation", {"FY2025": 12139, "FY2024": 13627, "FY2023": 8575, "FY2022": 1640, "FY2021": 929}),
    ("TOTAL", "Total comprehensive income for the year, net of tax", {"FY2025": 12139, "FY2024": 13627, "FY2023": 8575, "FY2022": 1640, "FY2021": 929}),
]

bw.add_income_statement_sheet(
    title="CAF Bank Limited — Profit & Loss",
    subtitle="CAF Bank Limited's own basis, £'000. No OCI - there are no recognised gains or losses in any "
              "year other than those shown in the profit and loss account (per the Bank's own disclosure). See "
              "source note at bottom.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=88,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet 3: Statement of Changes in Equity
# ---------------------------------------------------------------
equity_headers = ["Called-up share capital", "Additional Tier 1 securities", "Distributable reserve", "Retained earnings", "Total"]
equity_rows = [
    ("TOTAL", "At 1 May 2021", (29350, 11000, 1000, -61, 41289)),
    ("DATA", "Total comprehensive profit for the financial year", (None, None, None, 1640, 1640)),
    ("TOTAL", "At 30 April 2022", (29350, 11000, 1000, 1579, 42929)),
    ("DATA", "Total comprehensive profit for the financial year", (None, None, None, 8575, 8575)),
    ("DATA", "Transferred from distributable reserve", (None, None, -1000, 1000, 0)),
    ("DATA", "Redemption of additional tier 1 securities", (None, -11000, None, None, -11000)),
    ("DATA", "Issue of share capital", (10969, None, None, None, 10969)),
    ("TOTAL", "At 30 April 2023", (40319, 0, 0, 11154, 51473)),
    ("DATA", "Profit on ordinary activities after taxation for the financial year", (None, None, None, 13627, 13627)),
    ("TOTAL", "At 30 April 2024", (40319, 0, 0, 24781, 65100)),
    ("DATA", "Profit on ordinary activities after taxation for the financial year", (None, None, None, 11139, 11139)),
    ("TOTAL", "At 30 April 2025", (40319, 0, 0, 35920, 76239)),
]

bw.add_equity_changes_sheet(
    title="CAF Bank Limited — Statement of Changes in Equity",
    subtitle="CAF Bank Limited's own basis, £'000, chronological (oldest to newest). See source note at bottom.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=58,
    source_height=280,
)

# ---------------------------------------------------------------
# Sheet: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit on ordinary activities", {"FY2025": 14661, "FY2024": 18169, "FY2023": 8575, "FY2022": 1640, "FY2021": 929}),
    ("DATA", "Amortisation of investments", {"FY2025": -6041, "FY2024": -2450, "FY2023": 344, "FY2022": 1170, "FY2021": 21919}),
    ("DATA", "Corporation tax paid", {"FY2025": -1705, "FY2024": -5815, "FY2023": -830, "FY2021": None}),
    ("DATA", "(Increase)/decrease in prepayments and accrued income", {"FY2025": -1316, "FY2024": -1791, "FY2023": -4982, "FY2022": 275, "FY2021": 311}),
    ("DATA", "(Decrease)/increase in accruals and deferred income", {"FY2021": -98}),
    ("DATA", "Increase/(decrease) in Cash Ratio Deposit with the Bank of England", {"FY2024": 3582, "FY2023": -369, "FY2022": -918, "FY2021": -828}),
    ("DATA", "Decrease in loans and advances to banks", {"FY2021": 0}),
    ("DATA", "(Increase) in loans and advances to customers", {"FY2025": -21216, "FY2024": -20683, "FY2023": -17900, "FY2022": -34801, "FY2021": -21414}),
    ("DATA", "Increase/(decrease) in loan loss provision", {"FY2025": -184, "FY2024": 716, "FY2023": 573, "FY2022": -1100, "FY2021": 533}),
    ("DATA", "Increase/(decrease) in customer accounts", {"FY2025": 31493, "FY2024": -85992, "FY2023": -3512, "FY2022": 110791, "FY2021": 241151}),
    ("DATA", "Increase in other liabilities", {"FY2025": 5037, "FY2024": 3028, "FY2023": 2435, "FY2022": 2317, "FY2021": -2052}),
    ("TOTAL", "Net cash generated from/(used in) operating activities", {"FY2025": 20729, "FY2024": -91236, "FY2023": -15666, "FY2022": 79374, "FY2021": 240451}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Acquisitions of debt securities", {"FY2025": -156964, "FY2024": -254111, "FY2023": -88130, "FY2022": -228836, "FY2021": -293668}),
    ("DATA", "Redemptions of debt securities", {"FY2025": 115598, "FY2024": 371286, "FY2023": 112831, "FY2022": 336397, "FY2021": 156956}),
    ("DATA", "Disposals of debt securities", {"FY2021": 0}),
    ("DATA", "Net proceeds/(repayments) from repurchase agreements", {"FY2025": -13852, "FY2024": 5000, "FY2023": 8852, "FY2021": -10142}),
    ("DATA", "Acquisition of intangible assets", {"FY2025": -5150, "FY2024": -4425, "FY2023": -1657, "FY2022": -3482, "FY2021": -1194}),
    ("DATA", "Proceeds from subordinated debt", {"FY2024": 15000}),
    ("DATA", "Repayment of subordinated debt", {"FY2024": -10000}),
    ("TOTAL", "Net cash generated from/(used in) investing activities", {"FY2025": -60368, "FY2024": 122750, "FY2023": 31896, "FY2022": 104079, "FY2021": -148048}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Costs of redemption of additional tier 1 securities and exchange for ordinary share capital", {"FY2023": -31}),
    ("DATA", "Charitable donations paid", {"FY2021": -297}),
    ("DATA", "AT1 dividend paid", {"FY2021": -1126}),
    ("TOTAL", "Net cash used in financing activities", {"FY2025": 0, "FY2024": 0, "FY2023": -31, "FY2022": 0, "FY2021": -1423}),
    ("TOTAL", "Change in cash and cash equivalents in the year", {"FY2025": -39639, "FY2024": 31514, "FY2023": 16199, "FY2022": 183453, "FY2021": 90980}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 654524, "FY2024": 623010, "FY2023": 606811, "FY2022": 423358, "FY2021": 332378}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 614885, "FY2024": 654524, "FY2023": 623010, "FY2022": 606811, "FY2021": 423358}),
    ("SECTION", "Represented by:", {}),
    ("DATA", "Balances at Bank of England repayable on demand", {"FY2025": 610671, "FY2024": 630526, "FY2023": 616894, "FY2022": 599340, "FY2021": 415461}),
    ("DATA", "Loans and advances to banks repayable on demand", {"FY2025": 4214, "FY2024": 23998, "FY2023": 6116, "FY2022": 7471, "FY2021": 7897}),
]

bw.add_cash_flow_sheet(
    title="CAF Bank Limited — Cash Flow Statement",
    subtitle="CAF Bank Limited's own basis, £'000. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=88,
    source_height=320,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loan book", {}),
    ("DATA", "Loans and advances to customers, net", {"FY2025": 219101, "FY2024": 197701, "FY2023": 177734, "FY2022": 160407, "FY2021": 124506}),
    ("SECTION", "Loan loss provision (FRS 102 - no IFRS 9 stage split)", {}),
    ("DATA", "Individual impairment provision, closing balance", {"FY2025": -1021, "FY2024": -552, "FY2021": -1376}),
    ("DATA", "Collective impairment provision, closing balance", {"FY2025": -1162, "FY2024": -1815, "FY2021": -802}),
    ("TOTAL", "Total loan loss provision, closing balance", {"FY2025": -2183, "FY2024": -2367, "FY2023": -1651, "FY2022": -1078, "FY2021": -2178}),
    ("DATA", "Loan loss provision credit/(charge) for the year", {"FY2025": 184, "FY2024": -716, "FY2023": -573, "FY2022": 1100, "FY2021": -533}),
]

bw.add_asset_quality_sheet(
    title="CAF Bank Limited — Asset Quality",
    subtitle="CAF Bank Limited's own basis, £'000. FRS 102 incurred-loss bank (not IFRS 9) - individual/"
              "collective split disclosed FY2024/FY2025 and FY2021; FY2022/FY2023 only an aggregate was "
              "sourced. See source note at bottom.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=88,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets — nothing publicly disclosed for this entity
# ---------------------------------------------------------------
NOT_DISCLOSED_NOTE = (
    "Not publicly disclosed by CAF Bank Limited in any year reviewed (FY2021-FY2025) - checked the Annual "
    "Report's Strategic Report, Risk management report, and full Notes to the Financial Statements, plus CAF "
    "Bank's own site and CAF's wider governance/regulatory-disclosures pages. No standalone Pillar 3 document "
    "exists; see ENTITY_NOTE on the Cash Flow Statement sheet."
)

bw.add_not_disclosed_metric_sheets(
    ["CET1 Capital", "CET1 Ratio", "Tier 1 Capital", "Tier 1 Ratio", "Total Capital", "Total Capital Ratio",
     "Total RWAs"],
    CASH_FLOW_SOURCES,
    per_note={m: NOT_DISCLOSED_NOTE for m in
              ["CET1 Capital", "CET1 Ratio", "Tier 1 Capital", "Tier 1 Ratio", "Total Capital", "Total Capital Ratio",
               "Total RWAs"]},
)

bw.add_rwa_breakdown_sheet(
    title="CAF Bank Limited — RWA Breakdown",
    subtitle="Not publicly disclosed. See source note at bottom.",
    rows=[("DATA", "Not publicly disclosed", {})],
    sources_text=CASH_FLOW_SOURCES + "\n\n" + NOT_DISCLOSED_NOTE,
    first_col_width=54,
    source_height=280,
)

bw.add_not_disclosed_metric_sheets(
    ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"],
    CASH_FLOW_SOURCES,
    per_note={m: NOT_DISCLOSED_NOTE for m in
              ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"]},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 1544559, "FY2024": 1510925, "FY2023": 1571534, "FY2022": 1556044, "FY2021": 1441296}),
        ("Loans and advances to customers", {"FY2025": 219101, "FY2024": 197701, "FY2023": 177734, "FY2022": 160407, "FY2021": 124506}),
        ("Customer accounts", {"FY2025": 1450926, "FY2024": 1419433, "FY2023": 1505425, "FY2022": 1508937, "FY2021": 1398146}),
        ("Total shareholders' funds", {"FY2025": 76239, "FY2024": 65100, "FY2023": 51473, "FY2022": 42929, "FY2021": 41289}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net operating income", {"FY2025": 47304, "FY2024": 46540, "FY2023": 29693, "FY2022": 12703, "FY2021": 11211}),
        ("Administrative expenses", {"FY2025": -32827, "FY2024": -27655, "FY2023": -18472, "FY2022": -11774, "FY2021": -9763}),
        ("Profit on ordinary activities after taxation", {"FY2025": 12139, "FY2024": 13627, "FY2023": 8575, "FY2022": 1640, "FY2021": 929}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 65100, "FY2024": 51473, "FY2023": 42929, "FY2022": 41289}),
        ("Total comprehensive income for the year", {"FY2025": 12139, "FY2024": 13627, "FY2023": 8575, "FY2022": 1640, "FY2021": 929}),
        ("Other equity movements, net", {"FY2023": -31}),
        ("Closing equity", {"FY2025": 76239, "FY2024": 65100, "FY2023": 51473, "FY2022": 42929, "FY2021": 41289}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash generated from/(used in) operating activities", {"FY2025": 20729, "FY2024": -91236, "FY2023": -15666, "FY2022": 79374, "FY2021": 240451}),
        ("Net cash generated from/(used in) investing activities", {"FY2025": -60368, "FY2024": 122750, "FY2023": 31896, "FY2022": 104079, "FY2021": -148048}),
        ("Net cash used in financing activities", {"FY2025": 0, "FY2024": 0, "FY2023": -31, "FY2022": 0, "FY2021": -1423}),
        ("Cash and cash equivalents at end of year", {"FY2025": 614885, "FY2024": 654524, "FY2023": 623010, "FY2022": 606811, "FY2021": 423358}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {}),
        ("Tier 1 Ratio", {}),
        ("Total Capital Ratio", {}),
        ("Leverage Ratio", {}),
        ("LCR", {}),
        ("NSFR", {}),
    ],
    note="Full 5-year Balance Sheet/P&L/Statement of Changes in Equity/Cash Flow Statement (FY2021-FY2025), no "
         "FRS 101/102 cash-flow exemption. No Pillar 3 disclosure of any kind (CET1/Tier 1/Total Capital, RWAs "
         "and RWA Breakdown, Leverage Ratio, LCR, NSFR, MREL) is published by this entity in any year - all 11 "
         "metric sheets plus RWA Breakdown are 'Not publicly disclosed'; see ENTITY_NOTE on the Cash Flow "
         "Statement sheet. Asset Quality's individual/collective loan loss provision split is only disclosed at "
         "that granularity from FY2024 onward (FRS 102, not IFRS 9 - no stage split at all).",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/CAF BANK FINANCIALS.xlsx")
