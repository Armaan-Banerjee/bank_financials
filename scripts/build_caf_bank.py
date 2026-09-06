import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# CAF Bank Limited (Companies House 01837656, FRN 204451), owned by Charities
# Aid Foundation (CAF), serves charities/non-profits. Fiscal year-end 30 April.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/01837656/filing-history"
AR2025_URL = f"{CH_BASE}/MzUwNDA1NTExOGFkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = f"{CH_BASE}/MzM5MjYwNDE2NmFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = f"{CH_BASE}/MzMxMTMwNTcwNWFkaXF6a2N4/document?format=pdf&download=0"
# FY2020 own filing (found 2026-09-06 during HD-061's FY2020 extension) - re-verified directly
# against a rendered page-image read (0 text layer, same as every other CAF Bank filing), not
# assumed from the ticket's nominal "confirmed floor" alone. Its own FY2019 comparative column
# and FY2021's own FY2020 comparative column (in AR2021_URL) both cross-check exactly.
AR2020_URL = f"{CH_BASE}/MzI3NzEzMDk0OWFkaXF6a2N4/document?format=pdf&download=0"

# CAF Bank's own Pillar 3 archive (cafonline.org) - found 2026-09-05 during a
# historical-depth feasibility check (wayfinder/historical-depth/, HD-002)
# that flagged this workbook's original "no Pillar 3 disclosure of any kind"
# finding as likely wrong; a dedicated verification pass confirmed real,
# CAF-Bank-specific standalone Pillar 3 PDFs exist for FY2021-FY2024 (FY2020
# too, outside this workbook's window). FY2025 has no standalone document -
# CAF Bank moved to the PRA's SDDT ("Small Domestic Deposit Taker") regime,
# which doesn't require one - but the FY2025 Annual Report's own Strategic
# Report discloses 3 of the metrics directly (Total Capital Ratio, Leverage
# Ratio, LCR), used below instead of leaving that year fully blank.
P3_2021_URL = "https://www.cafonline.org/docs/default-source/about-us-governance/caf_bank_pillar3_2021.pdf"
P3_2022_URL = "https://www.cafonline.org/docs/default-source/about-us-governance/caf_bank_pillar3_2022.pdf"
P3_2023_URL = "https://www.cafonline.org/docs/default-source/about-us-governance/caf_bank_pillar_ar_2023.pdf"
P3_2024_URL = "https://www.cafonline.org/docs/default-source/annual-reports/caf-bank-pillar-3-disclosure-2023_2024.pdf"
# FY2020 Pillar 3 (found 2026-09-06, HD-061): NOT at the naive "caf_bank_pillar3_2020.pdf" guess
# (404s live - a different, retired page path) - recovered via a Wayback CDX domain scan of
# cafonline.org for historical Pillar 3 filenames, which surfaced this bank's own internal
# publish-date-coded naming convention (each PDF's filename ends in a YYMMDD publish-date code,
# e.g. "_250920" = published 25 Sep 2020). Confirmed live at its original URL (not just archived).
P3_2020_URL = "https://www.cafonline.org/docs/default-source/about-us-about-caf-bank/cafbank_pillar3_disclosure_2921d_250920.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: CAF Bank Limited (Companies House 01837656, FRN 204451, formerly Cafcash Limited) is a UK bank "
    "wholly owned by the Charities Aid Foundation (CAF, registered charity 268369), serving charities/non-profits. "
    "It takes no FRS 101/102 cash-flow exemption - full Cash Flow Statement every year. All 4 source Companies "
    "House filings used (FY2025, FY2023-with-FY2022-comparative, FY2021, FY2020) are fully scanned/image-only (0 "
    "text blocks/page) - every figure was transcribed via high-resolution page-image review, cross-checked against "
    "the following year's comparative column where available. FY2024's own standalone filing was not needed since "
    "FY2025's filing carries it as a comparative; FY2022's standalone filing was likewise not needed since FY2023's "
    "filing carries it as a comparative.\n\n"
    "HISTORICAL-DEPTH EXTENSION (2026-09-06, HD-061): extended back to FY2020, this project's confirmed floor for "
    "this entity. FY2020's own filing was re-verified directly (rendered page images, not assumed from the "
    "ticket's nominal floor) and cross-checks exactly against FY2021's own FY2020 comparative column in every "
    "statement - no restatement found anywhere in this extension. One genuine label quirk in FY2020's own "
    "Profit and Loss Account, reproduced as printed rather than silently corrected: its fee-income subtotal is "
    "itself labelled 'Net operating income' (a mislabelling that FY2021 onward's own presentation calls 'Net fee "
    "income', reserving 'Net operating income' for the combined interest+fee total) - this workbook's 'Net fee "
    "income' row for FY2020 uses that same figure, and its 'Net operating income' row for FY2020 is a computed "
    "sum (interest £11,499k + fee £1,101k = £12,600k) since FY2020's own document never prints that combined "
    "total under any label. The FY2020 Companies House filing (Note 10) discloses the individual/collective loan "
    "loss provision split directly - unlike FY2022/FY2023, no follow-up pass was needed to find it.\n\n"
    "DATA QUALITY NOTE: the FY2025 column's 'Net cash generated from operating activities' total (£20,729k) and "
    "'Net cash used in investing activities' total (£60,368k) are both independently corroborated - they sum "
    "exactly to the stated 'Change in cash and cash equivalents in the year' (£(39,639)k), and the closing balance "
    "these imply matches the 'Represented by' breakdown exactly. However, one underlying adjustment line "
    "('Amortisation of investments') is genuinely ambiguous in the source scan between the two plausible digit "
    "readings £(6,041)k and £(8,041)k - only the former makes the itemised adjustments sum exactly to the stated "
    "operating total, so £(6,041)k is used here as the internally-consistent figure (the same approach used "
    "elsewhere in this project for LHV/Zempler/Vanquis source-document ambiguities). The FY2024 comparative "
    "column's own itemised lines sum exactly to its own stated totals with no ambiguity.\n\n"
    "CORRECTION (2026-09-05): an earlier version of this workbook stated that no Pillar 3 disclosure of any kind "
    "existed for this entity - that was wrong. CAF Bank Limited publishes its own standalone Pillar 3 Disclosure "
    "PDFs on cafonline.org; the original build simply didn't find them (it checked the Annual Report/Companies "
    "House filings only, where the observation of 'no figures in the financial statements themselves' is true but "
    "incomplete). Real solo-basis Pillar 3 documents exist for FY2020-FY2024 (see PILLAR3_SOURCES below for exact "
    "URLs/pages); see each metric sheet for its own sourcing. FY2025 has no standalone Pillar 3 document - CAF "
    "Bank's own site states it 'has become part of the PRA's SDDT (\"Small Domestic Deposit Taker\") regime under "
    "which, as a non-listed institution, the Bank is not required to publish a Pillar 3 report' - but the FY2025 "
    "Annual Report's own Strategic Report ('Liquidity, the Investment Portfolio and Capital' section, p.27-28) "
    "discloses 3 of the 11 metrics directly (Total Capital Ratio, Leverage Ratio, LCR), used on those 3 sheets "
    "instead of leaving FY2025 blank; CET1/Tier 1/Total Capital (£)/Total RWAs/RWA Breakdown/NSFR are genuinely "
    "not disclosed anywhere for FY2025, confirmed by a full-document search of the 51-page Annual Report. MREL "
    "Ratio is not disclosed in any year FY2020-FY2025, in either the Pillar 3 documents or the Annual Reports."
)

PILLAR3_SOURCES = (
    "Sources - CAF Bank Limited's own standalone Pillar 3 Disclosure PDFs (solo basis, fiscal year-end 30 April), "
    "found on cafonline.org (not Companies House) - a 2026-09-05 correction, see ENTITY_NOTE above:\n"
    f"FY2020: CAF Bank Ltd Pillar 3 Disclosure, 30 April 2020, 'Capital resources' table (p.7) and 'Pillar 1 "
    f"capital requirement' table (p.9) - {P3_2020_URL}\n"
    f"FY2021: CAF Bank Ltd Pillar 3 Disclosure, 30 April 2021, 'Total Capital Resources' table (p.4) and 'Pillar 1 "
    f"capital requirement' table (p.7) - {P3_2021_URL}\n"
    f"FY2022: CAF BANK LTD Pillar 3 Disclosure, 30 April 2022, Template UK KM1 'Key metrics' (p.5), Template UK OV1 "
    f"'Overview of risk weighted exposure amounts' (p.11), Template UK LIQ1/LIQ2 (p.25-26) - {P3_2022_URL}\n"
    f"FY2023: Pillar 3 Report 2022/23, CAF Bank Ltd Pillar 3 Disclosure, 30 April 2023, Template UK KM1 (p.4), "
    f"Template UK OV1 (p.7) - {P3_2023_URL}\n"
    f"FY2024: Pillar 3 Report 2023/24, Pillar 3 Disclosure, CAF Bank Ltd, 30 April 2024, Template UK KM1 (p.5), "
    f"Template UK OV1 (p.8), Template UK LRCom (p.9) - {P3_2024_URL}\n"
    f"FY2025: no standalone Pillar 3 document exists (SDDT-exempt) - CAF Bank Ltd Annual Report and Financial "
    f"Statements for the year ended 30 April 2025, Strategic Report, 'Liquidity, the Investment Portfolio and "
    f"Capital' section (p.27-28) - {AR2025_URL}\n\n"
    "RESTATEMENT NOTE (each year's own originally-published figure used, not a later comparative, per this "
    "project's standard convention): FY2022's own document's 2021 comparative column shows Total RWAs of "
    "£127,844k and Leverage Ratio (incl. central banks) of 2.74% - both differ immaterially from FY2021's own "
    "originally-published figures (£127,881k and 2.72% respectively, used here). FY2021's own document also "
    "predates the LIQ1/KM1 templates that introduced LCR/NSFR reporting - FY2022's document later shows a 268% "
    "LCR comparative for FY2021, but since FY2021's own document never disclosed an LCR figure at all, FY2021 LCR "
    "is left 'Not publicly disclosed' here rather than back-filled from a later document. FY2020's own document "
    "(pre-dating the KM1/LIQ1 templates even more than FY2021's) confirms the same absence: no LCR, NSFR or MREL "
    "figure of any kind appears anywhere in the FY2020 Pillar 3 document, found by a full read of all 27 pages - "
    "not assumed from the FY2021 pattern alone. FY2021's own document's 2020 comparative column shows CET1/Tier1/"
    "Total Capital/RWA/leverage figures identical to FY2020's own originally-published figures (used here) - no "
    "restatement at all between the two, unlike the FY2021-to-FY2022 gap above."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are CAF Bank Limited's own Cash Flow Statement, transcribed from each year's own "
    "Companies House filing (or, for FY2024/FY2022, that year's own comparative column in the following year's "
    "filing):\n"
    f"FY2025/FY2024: Full accounts made up to 30 April 2025 (filed 10 Feb 2026), Cash Flow Statement - {AR2025_URL}\n"
    f"FY2023/FY2022: Full accounts made up to 30 April 2023 (filed 14 Sep 2023), Cash Flow Statement - {AR2023_URL}\n"
    f"FY2021: Full accounts made up to 30 April 2021 (filed 31 Aug 2021), Cash Flow Statement - {AR2021_URL}\n"
    f"FY2020: Full accounts made up to 30 April 2020 (filed 10 Sep 2020), Cash Flow Statement (p.36) - {AR2020_URL}\n"
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
    f"FY2020: Full accounts made up to 30 April 2020 (filed 10 Sep 2020), Profit and loss account (p.33)/Balance "
    f"sheet (p.34)/Statement of changes in equity (p.35) - {AR2020_URL}\n"
    + ENTITY_NOTE
    + "\n\nPRESENTATION NOTE: the Statement of Changes in Equity had 4 equity components (Called-up share "
    "capital, Additional Tier 1 securities, Distributable reserve, Retained earnings) through FY2023; the AT1 "
    "securities were redeemed and the distributable reserve fully transferred to retained earnings during "
    "FY2023, leaving only 2 components (Called-up share capital, Retained earnings) from FY2024 onward. "
    "DISCREPANCY NOTE: the FY2021 filing's own Balance Sheet shows the Distributable reserve at 30 April 2021 as "
    "£939k, but the FY2023 filing's own equity reconciliation shows the same opening balance (at 1 May 2021) as "
    "£1,000k - a £61k gap between the two source filings, reproduced here as each document states it rather than "
    "silently reconciled. FY2020's own filing's Statement of Changes in Equity and FY2021's own filing's FY2020 "
    "comparative column agree exactly (Distributable reserve £1,000k, Retained earnings £0k, Total £41,350k at "
    "30 April 2020) - no equivalent discrepancy at the FY2019/FY2020 boundary.\n\n"
    "ROLL-FORWARD NOTE: the Statement of Changes in Equity now opens at 'At 30 April 2019' purely as the anchoring "
    "opening balance for FY2020's own movement rows (FY2019 itself is outside this workbook's year window, one "
    "year before the confirmed floor). Before the FY2020 extension (HD-061, 2026-09-06), this sheet started "
    "directly at a row labelled 'At 1 May 2021' with no FY2021 movement detail shown at all - that row's figures "
    "(29,350/11,000/1,000/(61)/41,289) were always FY2021's own CLOSING balance, just used as a shortcut opening "
    "seed for FY2022 since FY2020/FY2021 were both then out of scope. It is now correctly split into its own "
    "'At 30 April 2021' TOTAL row with FY2021's real movements (comprehensive profit £929k, AT1 dividends payable "
    "£(990)k, no charitable donation that year) shown leading up to it - no figures changed, only the previously-"
    "collapsed roll-forward detail restored."
)

ASSET_QUALITY_SOURCES = (
    "Sources - CAF Bank Limited's own Notes to the Financial Statements (Note 10, Loans and advances to "
    f"customers, p.43 of {AR2021_URL} for FY2021's individual/collective impairment tables; p.43 of {AR2020_URL} "
    "for FY2020's own equivalent table), same filings as STATEMENTS_SOURCES above.\n"
    + ENTITY_NOTE
    + "\n\nDISCLOSURE GRANULARITY NOTE: this is an FRS 102 bank (not IFRS 9), so there is no Stage 1/2/3 split - "
    "only an individual/collective impairment provision split. FY2021's own filing (Note 10, p.43) does in fact "
    "disclose this split (Individual impairments provision closing balance £(1,376)k, Collective impairments "
    "provision closing balance £(802)k, summing to the £(2,178)k aggregate) - found on a follow-up pass after an "
    "earlier build initially left FY2021 blank, having assumed (without having actually located the note) that "
    "the split was only disclosed from FY2024 onward. FY2022/FY2023 were not re-checked in this follow-up pass "
    "for a similar split (their columns above still show the single aggregate figure only, £(1,078)k/£(1,651)k, "
    "as originally sourced) - worth a similar check if those years are revisited. FY2020's own filing (Note 10, "
    "p.43) also discloses the split directly (Individual impairments provision closing balance £(938)k, "
    "Collective impairments provision closing balance £(707)k, summing to £(1,645)k) - and independently ties to "
    "the Profit and Loss Account's own £(1,200)k loan loss provision charge for the year (£938k newly individually "
    "provided + £262k collective movement = £1,200k), a cross-check performed before transcribing."
)

# ---------------------------------------------------------------
# Sheet 1: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Balances at Bank of England", {"FY2025": 610671, "FY2024": 630526, "FY2023": 620476, "FY2022": 602553, "FY2021": 417756, "FY2020": 327571}),
    ("DATA", "Loans and advances to banks", {"FY2025": 4214, "FY2024": 23998, "FY2023": 6116, "FY2022": 7471, "FY2021": 7897, "FY2020": 6273}),
    ("DATA", "Loans and advances to customers", {"FY2025": 219101, "FY2024": 197701, "FY2023": 177734, "FY2022": 160407, "FY2021": 124506, "FY2020": 103625}),
    ("DATA", "Debt securities", {"FY2025": 682783, "FY2024": 637376, "FY2023": 752100, "FY2022": 777145, "FY2021": 885876, "FY2020": 771083}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 11882, "FY2024": 10566, "FY2023": 8775, "FY2022": 3792, "FY2021": 4067, "FY2020": 4378}),
    ("DATA", "Intangible assets", {"FY2025": 15908, "FY2024": 10758, "FY2023": 6333, "FY2022": 4676, "FY2021": 1194}),
    ("TOTAL", "Total assets", {"FY2025": 1544559, "FY2024": 1510925, "FY2023": 1571534, "FY2022": 1556044, "FY2021": 1441296, "FY2020": 1212930}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer accounts", {"FY2025": 1450926, "FY2024": 1419433, "FY2023": 1505425, "FY2022": 1508937, "FY2021": 1398146, "FY2020": 1156995}),
    ("DATA", "Repurchase agreements", {"FY2025": 12394, "FY2024": 13852, "FY2023": 8852, "FY2021": 0, "FY2020": 10142}),
    ("DATA", "Other liabilities", {"FY2025": 5000, "FY2024": 7540, "FY2023": 5784, "FY2022": 4178, "FY2021": 1848, "FY2020": 4197}),
    ("DATA", "Accruals and deferred income", {"FY2021": 13, "FY2020": 246}),
    ("DATA", "Subordinated debt", {"FY2024": 5000}),
    ("TOTAL", "Total liabilities", {"FY2025": 1468320, "FY2024": 1445825, "FY2023": 1520061, "FY2022": 1513115, "FY2021": 1400007, "FY2020": 1171580}),
    ("SECTION", "Shareholders' funds", {}),
    ("DATA", "Called up share capital", {"FY2025": 40319, "FY2024": 40319, "FY2023": 40319, "FY2022": 29350, "FY2021": 29350, "FY2020": 29350}),
    ("DATA", "Additional Tier 1 capital", {"FY2022": 11000, "FY2021": 11000, "FY2020": 11000}),
    ("DATA", "Distributable reserve", {"FY2022": 1000, "FY2021": 939, "FY2020": 1000}),
    ("DATA", "Retained earnings", {"FY2025": 35920, "FY2024": 24781, "FY2023": 11154, "FY2022": 1579, "FY2021": -61, "FY2020": 0}),
    ("TOTAL", "Total shareholders' funds", {"FY2025": 76239, "FY2024": 65100, "FY2023": 51473, "FY2022": 42929, "FY2021": 41289, "FY2020": 41350}),
    ("TOTAL", "Total liabilities and shareholders' funds", {"FY2025": 1544559, "FY2024": 1510925, "FY2023": 1571534, "FY2022": 1556044, "FY2021": 1441296, "FY2020": 1212930}),
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
    ("DATA", "Interest receivable", {"FY2025": 66478, "FY2024": 65025, "FY2023": 35396, "FY2022": 10823, "FY2021": 10059, "FY2020": 12534}),
    ("DATA", "Interest payable", {"FY2025": -20929, "FY2024": -20250, "FY2023": -7350, "FY2022": -182, "FY2021": -263, "FY2020": -1035}),
    ("TOTAL", "Net interest income", {"FY2025": 45549, "FY2024": 44775, "FY2023": 28046, "FY2022": 10641, "FY2021": 9796, "FY2020": 11499}),
    ("DATA", "Fees and commissions receivable", {"FY2025": 2744, "FY2024": 2710, "FY2023": 2560, "FY2022": 2947, "FY2021": 2230, "FY2020": 2109}),
    ("DATA", "Fees and commissions payable", {"FY2025": -989, "FY2024": -945, "FY2023": -913, "FY2022": -885, "FY2021": -815, "FY2020": -1008}),
    ("TOTAL", "Net fee income", {"FY2025": 1755, "FY2024": 1765, "FY2023": 1647, "FY2022": 2062, "FY2021": 1415, "FY2020": 1101}),
    ("TOTAL", "Net operating income", {"FY2025": 47304, "FY2024": 46540, "FY2023": 29693, "FY2022": 12703, "FY2021": 11211, "FY2020": 12600}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Administrative expenses", {"FY2025": -32827, "FY2024": -27655, "FY2023": -18472, "FY2022": -11774, "FY2021": -9763, "FY2020": -10109}),
    ("DATA", "Loan loss provision credit/(charge)", {"FY2025": 184, "FY2024": -716, "FY2023": -573, "FY2022": 1100, "FY2021": -533, "FY2020": -1200}),
    ("TOTAL", "Profit on ordinary activities before taxation", {"FY2025": 14661, "FY2024": 18169, "FY2023": 10648, "FY2022": 2029, "FY2021": 915, "FY2020": 1291}),
    ("DATA", "Tax on profit on ordinary activities", {"FY2025": -2522, "FY2024": -4542, "FY2023": -2073, "FY2022": -389, "FY2021": 14, "FY2020": -1}),
    ("TOTAL", "Profit on ordinary activities after taxation", {"FY2025": 12139, "FY2024": 13627, "FY2023": 8575, "FY2022": 1640, "FY2021": 929, "FY2020": 1290}),
    ("TOTAL", "Total comprehensive income for the year, net of tax", {"FY2025": 12139, "FY2024": 13627, "FY2023": 8575, "FY2022": 1640, "FY2021": 929, "FY2020": 1290}),
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
    ("TOTAL", "At 30 April 2019", (29350, 11000, 1000, 0, 41350)),
    ("DATA", "Total comprehensive profit for the financial year", (None, None, None, 1290, 1290)),
    ("DATA", "Charitable donation to parent", (None, None, None, -297, -297)),
    ("DATA", "AT1 dividends payable", (None, None, None, -993, -993)),
    ("TOTAL", "At 30 April 2020", (29350, 11000, 1000, 0, 41350)),
    ("DATA", "Total comprehensive profit for the financial year", (None, None, None, 929, 929)),
    ("DATA", "AT1 dividends payable", (None, None, None, -990, -990)),
    ("TOTAL", "At 30 April 2021", (29350, 11000, 1000, -61, 41289)),
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
    ("DATA", "Profit on ordinary activities", {"FY2025": 14661, "FY2024": 18169, "FY2023": 8575, "FY2022": 1640, "FY2021": 929, "FY2020": 1291}),
    ("DATA", "Amortisation of investments", {"FY2025": -6041, "FY2024": -2450, "FY2023": 344, "FY2022": 1170, "FY2021": 21919, "FY2020": 2451}),
    ("DATA", "Corporation tax paid", {"FY2025": -1705, "FY2024": -5815, "FY2023": -830, "FY2021": None, "FY2020": 0}),
    ("DATA", "(Increase)/decrease in prepayments and accrued income", {"FY2025": -1316, "FY2024": -1791, "FY2023": -4982, "FY2022": 275, "FY2021": 311, "FY2020": 206}),
    ("DATA", "(Decrease)/increase in accruals and deferred income", {"FY2021": -98, "FY2020": 4}),
    ("DATA", "Increase/(decrease) in Cash Ratio Deposit with the Bank of England", {"FY2024": 3582, "FY2023": -369, "FY2022": -918, "FY2021": -828, "FY2020": -242}),
    ("DATA", "Decrease in loans and advances to banks", {"FY2021": 0, "FY2020": 0}),
    ("DATA", "(Increase) in loans and advances to customers", {"FY2025": -21216, "FY2024": -20683, "FY2023": -17900, "FY2022": -34801, "FY2021": -21414, "FY2020": -14363}),
    ("DATA", "Increase/(decrease) in loan loss provision", {"FY2025": -184, "FY2024": 716, "FY2023": 573, "FY2022": -1100, "FY2021": 533, "FY2020": 1200}),
    ("DATA", "Increase/(decrease) in customer accounts", {"FY2025": 31493, "FY2024": -85992, "FY2023": -3512, "FY2022": 110791, "FY2021": 241151, "FY2020": 122767}),
    ("DATA", "Increase in other liabilities", {"FY2025": 5037, "FY2024": 3028, "FY2023": 2435, "FY2022": 2317, "FY2021": -2052, "FY2020": 2335}),
    ("TOTAL", "Net cash generated from/(used in) operating activities", {"FY2025": 20729, "FY2024": -91236, "FY2023": -15666, "FY2022": 79374, "FY2021": 240451, "FY2020": 115649}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Acquisitions of debt securities", {"FY2025": -156964, "FY2024": -254111, "FY2023": -88130, "FY2022": -228836, "FY2021": -293668, "FY2020": -514420}),
    ("DATA", "Redemptions of debt securities", {"FY2025": 115598, "FY2024": 371286, "FY2023": 112831, "FY2022": 336397, "FY2021": 156956, "FY2020": 408809}),
    ("DATA", "Disposals of debt securities", {"FY2021": 0, "FY2020": 2163}),
    ("DATA", "Net proceeds/(repayments) from repurchase agreements", {"FY2025": -13852, "FY2024": 5000, "FY2023": 8852, "FY2021": -10142}),
    ("DATA", "Acquisition of intangible assets", {"FY2025": -5150, "FY2024": -4425, "FY2023": -1657, "FY2022": -3482, "FY2021": -1194}),
    ("DATA", "Proceeds from subordinated debt", {"FY2024": 15000}),
    ("DATA", "Repayment of subordinated debt", {"FY2024": -10000}),
    ("TOTAL", "Net cash generated from/(used in) investing activities", {"FY2025": -60368, "FY2024": 122750, "FY2023": 31896, "FY2022": 104079, "FY2021": -148048, "FY2020": -103448}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Costs of redemption of additional tier 1 securities and exchange for ordinary share capital", {"FY2023": -31}),
    ("DATA", "Charitable donations paid", {"FY2021": -297, "FY2020": -4908}),
    ("DATA", "AT1 dividend paid", {"FY2021": -1126, "FY2020": -858}),
    ("TOTAL", "Net cash used in financing activities", {"FY2025": 0, "FY2024": 0, "FY2023": -31, "FY2022": 0, "FY2021": -1423, "FY2020": -5766}),
    ("TOTAL", "Change in cash and cash equivalents in the year", {"FY2025": -39639, "FY2024": 31514, "FY2023": 16199, "FY2022": 183453, "FY2021": 90980, "FY2020": 6435}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 654524, "FY2024": 623010, "FY2023": 606811, "FY2022": 423358, "FY2021": 332378, "FY2020": 325943}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 614885, "FY2024": 654524, "FY2023": 623010, "FY2022": 606811, "FY2021": 423358, "FY2020": 332378}),
    ("SECTION", "Represented by:", {}),
    ("DATA", "Balances at Bank of England repayable on demand", {"FY2025": 610671, "FY2024": 630526, "FY2023": 616894, "FY2022": 599340, "FY2021": 415461, "FY2020": 326105}),
    ("DATA", "Loans and advances to banks repayable on demand", {"FY2025": 4214, "FY2024": 23998, "FY2023": 6116, "FY2022": 7471, "FY2021": 7897, "FY2020": 6273}),
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
    ("DATA", "Loans and advances to customers, net", {"FY2025": 219101, "FY2024": 197701, "FY2023": 177734, "FY2022": 160407, "FY2021": 124506, "FY2020": 103625}),
    ("SECTION", "Loan loss provision (FRS 102 - no IFRS 9 stage split)", {}),
    ("DATA", "Individual impairment provision, closing balance", {"FY2025": -1021, "FY2024": -552, "FY2021": -1376, "FY2020": -938}),
    ("DATA", "Collective impairment provision, closing balance", {"FY2025": -1162, "FY2024": -1815, "FY2021": -802, "FY2020": -707}),
    ("TOTAL", "Total loan loss provision, closing balance", {"FY2025": -2183, "FY2024": -2367, "FY2023": -1651, "FY2022": -1078, "FY2021": -2178, "FY2020": -1645}),
    ("DATA", "Loan loss provision credit/(charge) for the year", {"FY2025": 184, "FY2024": -716, "FY2023": -573, "FY2022": 1100, "FY2021": -533, "FY2020": -1200}),
]

bw.add_asset_quality_sheet(
    title="CAF Bank Limited — Asset Quality",
    subtitle="CAF Bank Limited's own basis, £'000. FRS 102 incurred-loss bank (not IFRS 9) - individual/"
              "collective split disclosed FY2020/FY2021/FY2024/FY2025; FY2022/FY2023 only an aggregate was "
              "sourced. See source note at bottom.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=88,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets — corrected 2026-09-05: real data exists, see
# PILLAR3_SOURCES/ENTITY_NOTE above for how the original "not publicly
# disclosed" finding was wrong and what changed.
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, PILLAR3_SOURCES, note=note, first_col_width=54, source_height=320)

FY2025_NO_STANDALONE_NOTE = (
    "FY2025 has no standalone Pillar 3 document (CAF Bank is SDDT-exempt from FY2025) and this metric isn't "
    "disclosed in the FY2025 Annual Report either - genuinely not publicly disclosed for FY2025 only."
)

metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2024": 54342, "FY2023": 45140, "FY2022": 27253, "FY2021": 29095, "FY2020": 30350})],
    note=FY2025_NO_STANDALONE_NOTE,
)

metric(
    "CET1 Ratio", "% of RWA",
    [("CET1 ratio", {"FY2024": "29.35%", "FY2023": "30.8%", "FY2022": "21.9%", "FY2021": "22.8%", "FY2020": "20.6%"})],
    note=FY2025_NO_STANDALONE_NOTE,
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2024": 54342, "FY2023": 45140, "FY2022": 38253, "FY2021": 40095, "FY2020": 41350})],
    note=FY2025_NO_STANDALONE_NOTE + " Equal to CET1 capital from FY2023 onward - CAF Bank's Additional Tier 1 "
         "securities were fully redeemed during FY2023 (see Statement of Changes in Equity); FY2020/FY2021/FY2022 "
         "include the AT1 instrument.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2024": "29.35%", "FY2023": "30.8%", "FY2022": "30.8%", "FY2021": "31.4%", "FY2020": "28.0%"})],
    note=FY2025_NO_STANDALONE_NOTE,
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2024": 56157, "FY2023": 45140, "FY2022": 38253, "FY2021": 40095, "FY2020": 41350})],
    note=FY2025_NO_STANDALONE_NOTE + " FY2024 is the only year with Tier 2 capital (£1,815k) - equal to Tier 1 "
         "capital in every other year shown.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "29.7%", "FY2024": "30.33%", "FY2023": "30.8%", "FY2022": "30.8%", "FY2021": "31.4%", "FY2020": "28.0%"})],
    note="FY2025 is the only ratio sourced from the Annual Report's own Strategic Report (no standalone Pillar 3 "
         "document exists for FY2025) - see PILLAR3_SOURCES.",
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted exposure amount", {"FY2024": 185123, "FY2023": 146334, "FY2022": 124243, "FY2021": 127881, "FY2020": 147540})],
    note=FY2025_NO_STANDALONE_NOTE + " FY2021's own document states £127,881k; a later document's FY2021 "
         "comparative shows a immaterially different £127,844k - FY2021's own originally-published figure is "
         "used here, per this project's standard convention (see PILLAR3_SOURCES restatement note). FY2020's own "
         "document (£147,540k) ties exactly to FY2021's own FY2020 comparative column - no restatement at that "
         "boundary.",
)

rwa_breakdown_rows = [
    ("SECTION", "RWA by risk category", {}),
    ("DATA", "Credit risk (incl. counterparty credit risk, FY2020-FY2021 only)", {"FY2021": 105880, "FY2020": 125890}),
    ("DATA", "Credit risk and counterparty credit risk", {"FY2024": 129538, "FY2023": 112829, "FY2022": 102044}),
    ("DATA", "Operational risk", {"FY2024": 55585, "FY2023": 33505, "FY2022": 22199, "FY2021": 22001, "FY2020": 21650}),
    ("TOTAL", "Total", {"FY2024": 185123, "FY2023": 146334, "FY2022": 124243, "FY2021": 127881, "FY2020": 147540}),
]
bw.add_rwa_breakdown_sheet(
    title="CAF Bank Limited — RWA Breakdown",
    subtitle="£'000, solo basis. FY2025 not disclosed (no standalone Pillar 3 document - SDDT-exempt). See source note at bottom.",
    rows=rwa_breakdown_rows,
    sources_text=PILLAR3_SOURCES + "\n\nFY2020-FY2021's pre-KM1/OV1 category table combines credit and "
         "counterparty credit risk into a single 'Credit risk' line, unlike FY2022 onward's OV1 template which "
         "keeps them combined too under a single 'Credit risk and counterparty credit risk' row - both eras' "
         "rows are kept exactly as each document itself presents them, not force-aligned into one label.",
    first_col_width=54,
    source_height=320,
)

metric(
    "Leverage Ratio", "%",
    [
        ("Leverage ratio, excluding claims on central banks", {"FY2025": "6.35%", "FY2024": "6.05%", "FY2023": "4.64%", "FY2022": "3.97%", "FY2021": "3.81%", "FY2020": "4.62%"}),
        ("Leverage ratio, including claims on central banks", {"FY2023": "2.83%", "FY2022": "2.44%", "FY2021": "2.72%", "FY2020": "3.35%"}),
    ],
    note="FY2025 sourced from the Annual Report's Strategic Report (no standalone Pillar 3 document - SDDT-exempt); "
         "its 6.35% figure reconciles exactly against FY2024's own 6.05% 'excluding central banks' comparative "
         "quoted in the same Annual Report passage. FY2024's own Pillar 3 document discloses only the 'excluding' "
         "basis (the 'including central banks' exposure measure is given with no accompanying %, a genuine "
         "reduction in disclosure granularity vs. FY2021-2023) - FY2024/FY2025 'including central banks' left "
         "blank rather than calculated. FY2021's own document states 2.72%; a later document's FY2021 comparative "
         "shows an immaterially different 2.74% - FY2021's own originally-published figure is used here. FY2020's "
         "own document (4.62%/3.35%) ties exactly to FY2021's own FY2020 comparative column - no restatement at "
         "that boundary, unlike the FY2021-to-FY2022 gap.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("High-quality liquid assets (weighted, average)", {"FY2024": 1150942, "FY2023": 1244786, "FY2022": 1255456}),
        ("Net cash outflows (adjusted)", {"FY2024": 447586, "FY2023": 478804, "FY2022": 476184}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "543%", "FY2024": "257%", "FY2023": "260%", "FY2022": "264%"}),
    ],
    note="FY2025's 543% is sourced from the Annual Report's Strategic Report (no standalone Pillar 3 document - "
         "SDDT-exempt); its own comparator ties exactly to FY2024's Pillar 3 KM1 figure. FY2020 and FY2021 are "
         "both 'Not publicly disclosed' - both years' own Pillar 3 documents predate the LIQ1/KM1 templates that "
         "introduced LCR reporting, so no LCR figure was ever published for either year in its own document (a "
         "later document's FY2021 comparative of 268% exists, but per this project's convention of using each "
         "year's own originally-published figure, it is not back-filled here); confirmed for FY2020 by a full "
         "27-page read of its own Pillar 3 document, not assumed from the FY2021 pattern.",
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Available stable funding", {"FY2024": 1377360, "FY2023": 1429893, "FY2022": 1426183}),
        ("Required stable funding", {"FY2024": 272188, "FY2023": 154418, "FY2022": 177361}),
        ("Net Stable Funding Ratio (%)", {"FY2024": "506%", "FY2023": "926%", "FY2022": "804%"}),
    ],
    note="Not disclosed in FY2020 or FY2021's own documents (both predate the KM1 template that introduced NSFR "
         "reporting) or FY2025 (no standalone Pillar 3 document - SDDT-exempt; the FY2025 Annual Report's own "
         "Strategic Report doesn't mention NSFR either, unlike its 3 other ratios).",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    PILLAR3_SOURCES,
    per_note={"MREL Ratio": "Not publicly disclosed by CAF Bank Limited in any year FY2020-FY2025 - not in any "
              "standalone Pillar 3 document, nor in any Annual Report. CAF Bank is not a UK resolution entity."},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 1544559, "FY2024": 1510925, "FY2023": 1571534, "FY2022": 1556044, "FY2021": 1441296, "FY2020": 1212930}),
        ("Loans and advances to customers", {"FY2025": 219101, "FY2024": 197701, "FY2023": 177734, "FY2022": 160407, "FY2021": 124506, "FY2020": 103625}),
        ("Customer accounts", {"FY2025": 1450926, "FY2024": 1419433, "FY2023": 1505425, "FY2022": 1508937, "FY2021": 1398146, "FY2020": 1156995}),
        ("Total shareholders' funds", {"FY2025": 76239, "FY2024": 65100, "FY2023": 51473, "FY2022": 42929, "FY2021": 41289, "FY2020": 41350}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net operating income", {"FY2025": 47304, "FY2024": 46540, "FY2023": 29693, "FY2022": 12703, "FY2021": 11211, "FY2020": 12600}),
        ("Administrative expenses", {"FY2025": -32827, "FY2024": -27655, "FY2023": -18472, "FY2022": -11774, "FY2021": -9763, "FY2020": -10109}),
        ("Profit on ordinary activities after taxation", {"FY2025": 12139, "FY2024": 13627, "FY2023": 8575, "FY2022": 1640, "FY2021": 929, "FY2020": 1290}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 65100, "FY2024": 51473, "FY2023": 42929, "FY2022": 41289, "FY2021": 41350}),
        ("Total comprehensive income for the year", {"FY2025": 12139, "FY2024": 13627, "FY2023": 8575, "FY2022": 1640, "FY2021": 929, "FY2020": 1290}),
        ("Other equity movements, net", {"FY2023": -31, "FY2021": -990, "FY2020": -1290}),
        ("Closing equity", {"FY2025": 76239, "FY2024": 65100, "FY2023": 51473, "FY2022": 42929, "FY2021": 41289, "FY2020": 41350}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash generated from/(used in) operating activities", {"FY2025": 20729, "FY2024": -91236, "FY2023": -15666, "FY2022": 79374, "FY2021": 240451, "FY2020": 115649}),
        ("Net cash generated from/(used in) investing activities", {"FY2025": -60368, "FY2024": 122750, "FY2023": 31896, "FY2022": 104079, "FY2021": -148048, "FY2020": -103448}),
        ("Net cash used in financing activities", {"FY2025": 0, "FY2024": 0, "FY2023": -31, "FY2022": 0, "FY2021": -1423, "FY2020": -5766}),
        ("Cash and cash equivalents at end of year", {"FY2025": 614885, "FY2024": 654524, "FY2023": 623010, "FY2022": 606811, "FY2021": 423358, "FY2020": 332378}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2024": "29.35%", "FY2023": "30.8%", "FY2022": "21.9%", "FY2021": "22.8%", "FY2020": "20.6%"}),
        ("Tier 1 Ratio", {"FY2024": "29.35%", "FY2023": "30.8%", "FY2022": "30.8%", "FY2021": "31.4%", "FY2020": "28.0%"}),
        ("Total Capital Ratio", {"FY2025": "29.7%", "FY2024": "30.33%", "FY2023": "30.8%", "FY2022": "30.8%", "FY2021": "31.4%", "FY2020": "28.0%"}),
        ("Leverage Ratio", {"FY2025": "6.35%", "FY2024": "6.05%", "FY2023": "4.64%", "FY2022": "3.97%", "FY2021": "3.81%", "FY2020": "4.62%"}),
        ("LCR", {"FY2025": "543%", "FY2024": "257%", "FY2023": "260%", "FY2022": "264%"}),
        ("NSFR", {"FY2024": "506%", "FY2023": "926%", "FY2022": "804%"}),
    ],
    note="Full 6-year Balance Sheet/P&L/Statement of Changes in Equity/Cash Flow Statement (FY2020-FY2025), no "
         "FRS 101/102 cash-flow exemption. Extended back to FY2020 2026-09-06 (HD-061) - re-verified directly "
         "against a rendered page-image read of FY2020's own Companies House filing and FY2021's own FY2020 "
         "comparative column, both of which tie exactly with no restatement found. CORRECTION (2026-09-05): CAF "
         "Bank Limited does publish real Pillar 3 disclosure via standalone PDFs on cafonline.org (not Companies "
         "House) for FY2020-FY2024, and the FY2025 Annual Report's own Strategic Report discloses Total Capital "
         "Ratio/Leverage Ratio/LCR directly; an earlier build of this workbook incorrectly marked all 11 Pillar 3 "
         "metric sheets 'Not publicly disclosed' - only MREL Ratio remains genuinely undisclosed in every year. "
         "See ENTITY_NOTE and PILLAR3_SOURCES on the Cash Flow Statement sheet for the full correction and "
         "citations. Asset Quality's individual/collective loan loss provision split is disclosed for FY2020, "
         "FY2021, FY2024 and FY2025 but not FY2022/FY2023 (FRS 102, not IFRS 9 - no stage split at all).",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/CAF BANK FINANCIALS.xlsx")
