import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = [
    "FY2025", "FY2024", "FY2023", "FY2022", "FY2021",
    "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014",
]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

# All 12 years sourced from Companies House filings (fully scanned/image-only,
# 0 text blocks per page) - the bank's registered site (www.kingdombank.co.uk)
# is an unrelated expired/parked domain; the real site is www.kingdom.bank.
# Per HD-045 (2026-09-05), the FY2014-FY2020 window was added on top of the
# original FY2021-FY2025 build, capped at FY2014 by explicit project-wide
# decision even though the bank's real Companies House archive goes back to
# ~FY2004 - do not extend earlier than FY2014.
CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/04346834/filing-history"
FY2025_URL = f"{CH_BASE}/MzUzMjA2MDkzOWFkaXF6a2N4/document?format=pdf&download=0"
FY2024_URL = f"{CH_BASE}/MzQ3Mjc3MDk4N2FkaXF6a2N4/document?format=pdf&download=0"
FY2023_URL = f"{CH_BASE}/MzQyNzk5NjY3OGFkaXF6a2N4/document?format=pdf&download=0"
FY2022_URL = f"{CH_BASE}/MzM3Nzc1Mzk0NWFkaXF6a2N4/document?format=pdf&download=0"
FY2021_URL = f"{CH_BASE}/MzM0MzYxNTEyM2FkaXF6a2N4/document?format=pdf&download=0"
FY2020_URL = f"{CH_BASE}/MzMwMDE2MzUyN2FkaXF6a2N4/document?format=pdf&download=0"
FY2019_URL = f"{CH_BASE}/MzI2Mzg1MTA4OWFkaXF6a2N4/document?format=pdf&download=0"
FY2018_URL = f"{CH_BASE}/MzI0NDM5NDgzMGFkaXF6a2N4/document?format=pdf&download=0"
FY2017_URL = f"{CH_BASE}/MzIwMTY1OTMwOWFkaXF6a2N4/document?format=pdf&download=0"
FY2016_URL = f"{CH_BASE}/MzE3Mjc3MDQyOGFkaXF6a2N4/document?format=pdf&download=0"
FY2015_URL = f"{CH_BASE}/MzE1NzU2NjI4N2FkaXF6a2N4/document?format=pdf&download=0"
FY2014_URL = f"{CH_BASE}/MzEyMTIyNDc5OGFkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "Entity: Kingdom Bank Limited, company 04346834 (formerly Kingdom Banking Limited), FRN 400972 - "
    "confirmed via Banks List 2608.xlsx and Companies House, no identity ambiguity. A small specialist "
    "bank providing mortgages, savings and insurance broking to UK churches, Christian charities and "
    "individuals in Christian ministry; parent/ultimate controlling party is Lamb's Passage Holding "
    "Limited (LPHL) from 31 March 2020 onward (whose investor group includes Stewardship Services (UKET) "
    "Limited); for FY2014-FY2019 the ultimate parent was instead Assemblies of God Property Trust. "
    "Solo/Bank basis throughout - no group consolidation applies. All 12 years' filings on Companies "
    "House are fully scanned/image-only (0 extractable text on every page); the bank's registered-"
    "looking domain www.kingdombank.co.uk is an unrelated expired/parked domain (a GoDaddy-style parking "
    "page) - its real site is www.kingdom.bank. FY2014 was prepared under old UK GAAP/the BBA SORP (pre "
    "FRS 102) and, as a wholly-owned subsidiary whose parent's consolidated accounts are publicly "
    "available, took the FRS 1 (revised 1996) exemption from preparing a cash flow statement - FY2014 "
    "genuinely has no cash flow statement, not a sourcing gap (see Note 1(b) of the FY2014 Annual "
    "Report). FRS 102 was first adopted for FY2015, with a restated opening balance sheet at the 1 "
    "January 2014 transition date; the FY2014 figures used on every sheet here are as originally filed "
    "(old GAAP), not the FRS 102-restated comparatives shown in the FY2015 Annual Report's Statement of "
    "changes in equity (see the Statement of Changes in Equity sheet's source note for the one reconciling "
    "break this creates)."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Kingdom Bank Limited's own Statement of cash flows, £'000, Bank/solo basis "
    "(Companies House filings, all fully scanned):\n"
    f"FY2025 (own) & FY2024 (comparative, cross-checked against FY2024's own report): Annual Report & "
    "Accounts 2025, p.38 (Statement of cash flows) - " + FY2025_URL + "\n"
    f"FY2024 (own): Annual Report & Accounts 2024 - " + FY2024_URL + "\n"
    f"FY2023 (own) & FY2022 (comparative): Annual Report & Accounts 2023, p.39 (Statement of cash flows) - " + FY2023_URL + "\n"
    f"FY2022 (own): Annual Report & Accounts 2022 - " + FY2022_URL + "\n"
    f"FY2021 (own) & FY2020 (comparative, cross-checked against FY2020's own report): Annual Report & "
    "Accounts 2021, p.33 (Statement of cash flows) - " + FY2021_URL + "\n"
    f"FY2020 (own) & FY2019 (comparative): Annual Report & Accounts 2020, p.31 (Statement of cash flows) - " + FY2020_URL + "\n"
    f"FY2019 (own): Annual Report & Accounts 2019, p.26 - " + FY2019_URL + "\n"
    f"FY2018 (own) & FY2017 (comparative): Annual Report & Accounts 2018, p.23 (Statement of cash flows) - " + FY2018_URL + "\n"
    f"FY2017 (own): Annual Report & Accounts 2017 - " + FY2017_URL + "\n"
    f"FY2016 (own) & FY2015 (comparative): Annual Report & Accounts 2016, p.16 (Statement of cash flows) - " + FY2016_URL + "\n"
    f"FY2015 (own): Annual Report & Accounts 2015, p.16 - " + FY2015_URL + "\n"
    "FY2014: no cash flow statement was prepared - the Bank took the FRS 1 (revised 1996) 'Cash flow "
    "statements' exemption available to a wholly-owned subsidiary whose parent (Assemblies of God "
    "Property Trust) publishes consolidated accounts (FY2014 Annual Report, Note 1(b)) - " + FY2014_URL + "\n"
    + ENTITY_NOTE + "\n"
    "Every year-end closing balance ties exactly to the following year's opening balance across all 11 "
    "years for which a cash flow statement exists (FY2015 closing £13,263k = FY2016 opening; FY2016 "
    "closing £13,457k = FY2017 opening; FY2017 closing £14,528k = FY2018 opening; FY2018 closing £10,189k "
    "= FY2019 opening; FY2019 closing £12,010k = FY2020 opening; FY2020 closing £19,561k = FY2021 opening; "
    "FY2021 closing £20,030k = FY2022 opening; FY2022 closing £24,861k = FY2023 opening; FY2023 closing "
    "£35,058k = FY2024 opening; FY2024 closing £39,791k = FY2025 opening) - no restatements found."
)

STATEMENTS_SOURCES = (
    "Sources - Kingdom Bank Limited's own Statement of financial position / Income statement / Statement of "
    "changes in equity, £'000, Bank/solo basis (Companies House filings, all fully scanned/image-only):\n"
    f"FY2025 & FY2024: Annual Report & Accounts 2025, p.35 (Income statement), p.36 (Statement of financial "
    "position), p.37 (Statement of changes in equity) - " + FY2025_URL + "\n"
    f"FY2024 (own): Annual Report & Accounts 2024 - " + FY2024_URL + "\n"
    f"FY2023 & FY2022: Annual Report & Accounts 2023, p.36 (Income statement), p.37 (Statement of financial "
    "position), p.38 (Statement of changes in equity) - " + FY2023_URL + "\n"
    f"FY2022 (own): Annual Report & Accounts 2022, p.40 (Income statement), p.42 (Statement of financial "
    "position) - " + FY2022_URL + "\n"
    f"FY2021 & FY2020: Annual Report & Accounts 2021, p.27 (P&L), p.29 (Balance sheet), p.30 (Statement of "
    "changes in equity) - " + FY2021_URL + "\n"
    f"FY2020 & FY2019: Annual Report & Accounts 2020, p.27 (P&L), p.29 (Balance sheet), p.30 (Statement of "
    "changes in equity) - " + FY2020_URL + "\n"
    f"FY2019 (own): Annual Report & Accounts 2019, p.22 (P&L), p.24 (Balance sheet), p.25 (SOCE) - " + FY2019_URL + "\n"
    f"FY2018 & FY2017: Annual Report & Accounts 2018, p.19 (P&L), p.21 (Balance sheet), p.22 (Statement of "
    "changes in equity) - " + FY2018_URL + "\n"
    f"FY2017 (own): Annual Report & Accounts 2017 - " + FY2017_URL + "\n"
    f"FY2016 & FY2015: Annual Report & Accounts 2016, p.12 (P&L), p.14 (Balance sheet), p.15 (Statement of "
    "changes in equity) - " + FY2016_URL + "\n"
    f"FY2015 (own, incl. FRS 102 first-time-adoption SOCE at p.15): Annual Report & Accounts 2015 - " + FY2015_URL + "\n"
    f"FY2014 (own, old UK GAAP/BBA SORP - profit and loss account p.10, Statement of total recognised "
    "gains and losses p.11, balance sheet p.12; no SOCE or cash flow statement prepared that year - see "
    "the Statement of Changes in Equity and Cash Flow Statement sheets): Annual Report & Accounts 2014 - "
    + FY2014_URL + "\n"
    + ENTITY_NOTE + "\n"
    "PRESENTATION NOTES: (1) FY2021-FY2022 do not disclose separate 'Prepayments and accrued income' or "
    "'Accruals and deferred income' lines - FY2021/FY2022's own 'Other assets' and 'Other liabilities' totals "
    "bundle what FY2023 onward splits into two lines each; each year's own labelling is followed as published, "
    "not forced into a common template. (2) FY2021's income statement includes a one-off 'Profit on sale of "
    "investment property' line (£634k) and used the subtotal label 'Operating income' rather than 'Total net "
    "income' (introduced from FY2023) - same calculation, different label. (3) FY2021's own equity statement "
    "carried a £172k Revaluation reserve (from a historical operating-property revaluation) that was "
    "transferred to the Profit and loss account and fully extinguished during FY2021 upon reclassification of "
    "that property - a genuine one-off equity movement, not a plug. (4) FY2021's loan-book note used the label "
    "'Charity mortgages' where FY2022 onward uses 'Organisational mortgages' for the same category, and "
    "FY2021/FY2020 additionally had a small 'Fully secured lending to other group companies' sub-category "
    "(nil in FY2021, £269k in FY2020) not present from FY2022 onward. (5) FY2014-FY2018 additionally "
    "disclosed small 'Charity loans'/'Personal loans' unsecured sub-categories (a few £'000 each) that "
    "disappear from FY2019 onward - each year's own labelling is followed, not forced into a common "
    "template. (6) FY2014's balance sheet used its own old-GAAP line structure: 'Loans and advances to "
    "credit institutions' (economically the same line as later years' 'Loans and advances to banks'), no "
    "separately disclosed Investment property (bundled into Tangible fixed assets, which also included "
    "freehold investment property that year), and a single combined 'Prepayments, accrued income and "
    "other assets' line rather than the later three-way split into Other assets / Prepayments and accrued "
    "income / Deferred tax assets - see the dedicated 'Prepayments, accrued income and other assets "
    "(FY2014 combined line)' row below. (7) FY2014-FY2016 carried a materially larger Revaluation reserve "
    "(£578k/£164k/£166k) than FY2017-FY2020 (a flat £172k) from historical property revaluations that were "
    "gradually run down; this reserve is shown as its own Balance Sheet equity line for FY2014-FY2020 and "
    "is blank (not zero) for FY2021-FY2025 once fully extinguished (see the Statement of Changes in "
    "Equity sheet). (8) FRS 102 was first adopted for FY2015, with a restated 1 January 2014 opening "
    "balance sheet shown only in the FY2015 Annual Report's Statement of changes in equity; the FY2014 "
    "column on every sheet here uses the figures as originally filed under old UK GAAP/the BBA SORP (per "
    "the FY2014 Annual Report itself), not the FRS 102-restated comparatives - this creates a one-off, "
    "disclosed reconciling difference between the FY2014 closing position shown here (£4,960k total "
    "shareholders' funds) and the FY2015 Annual Report's restated opening position for 1 January 2015 "
    "(£4,847k), driven mainly by a £77k lower Revaluation reserve and a £365k higher Profit and loss "
    "account balance under the restated basis - not an error."
)

ASSET_QUALITY_SOURCES = (
    "Sources - Kingdom Bank Limited's own Note 12/9 'Loans and advances to customers' (Advances to customers by "
    "product, part a; Loan loss provision movement, part c), £'000, Bank/solo basis (Companies House filings, "
    "all fully scanned/image-only):\n"
    f"FY2025 & FY2024: Annual Report & Accounts 2025, p.51-52 - " + FY2025_URL + "\n"
    f"FY2024 (own): Annual Report & Accounts 2024 - " + FY2024_URL + "\n"
    f"FY2023 & FY2022: Annual Report & Accounts 2023, p.53-54 - " + FY2023_URL + "\n"
    f"FY2022 (own): Annual Report & Accounts 2022 - " + FY2022_URL + "\n"
    f"FY2021 & FY2020: Annual Report & Accounts 2021, p.45-46 (Note 12) - " + FY2021_URL + "\n"
    f"FY2020 & FY2019: Annual Report & Accounts 2020, p.45-46 (Note 12) - " + FY2020_URL + "\n"
    f"FY2019 (own): Annual Report & Accounts 2019, p.36-37 (Note 12) - " + FY2019_URL + "\n"
    f"FY2018 & FY2017: Annual Report & Accounts 2018, p.37-38 (Note 12) - " + FY2018_URL + "\n"
    f"FY2017 (own): Annual Report & Accounts 2017 - " + FY2017_URL + "\n"
    f"FY2016 & FY2015: Annual Report & Accounts 2016, p.29-31 (Note 12) - " + FY2016_URL + "\n"
    f"FY2015 (own): Annual Report & Accounts 2015 - " + FY2015_URL + "\n"
    f"FY2014 (own, Note 9 'Loans and advances to customers', old UK GAAP/BBA SORP): Annual Report & "
    "Accounts 2014, p.20-21 - " + FY2014_URL + "\n"
    + ENTITY_NOTE + "\n"
    "No IFRS 9 stage (1/2/3) split is disclosed in any year - this entity applies FRS 102 (FRS 102/old UK "
    "GAAP for FY2014), not IFRS 9, and reports a single collective/IBNR loan loss provision instead; the "
    "'Of which collective/IBNR provision' split shown here (where disclosed) is the closest equivalent "
    "breakdown and is only disclosed from FY2022 onward - left blank for FY2014-FY2021, not assumed zero. "
    "FY2014's own Note 9 used a materially different, more granular structure than every later year: its "
    "loan loss provision was split into a 'General provision' (IBNR-based, split further between "
    "incorporated and unincorporated borrowers) and a 'Specific provision', plus a wholly separate "
    "'Provision for suspended interest' deducted from gross advances alongside the main provision - see "
    "the dedicated FY2014 rows below for this one-off structure, which is not comparable line-for-line "
    "with FY2015 onward's single combined provision."
)


def p3_sources():
    return (
        "Sources - Kingdom Bank Limited, Bank/solo basis, £'000 unless stated as a % (from each year's own "
        "audited Statement of financial position and Strategic Report 'Key performance indicators' table):\n"
        f"FY2025 & FY2024: Annual Report & Accounts 2025, p.10 (Capital), p.15 (KPI table), p.36 (Statement "
        "of financial position) - " + FY2025_URL + "\n"
        f"FY2023 & FY2022: Annual Report & Accounts 2023, p.10 (Capital), p.15 (KPI table), p.37 (Statement "
        "of financial position) - " + FY2023_URL + "\n"
        f"FY2021 & FY2020: Annual Report & Accounts 2021, p.5 (Capital), p.8 (KPI table), p.31 (Statement of "
        "financial position) - " + FY2021_URL + "\n"
        f"FY2020 & FY2019: Annual Report & Accounts 2020, p.3 (Capital), p.7 (KPI table) - " + FY2020_URL + "\n"
        f"FY2019 (own) & FY2018 (comparative): Annual Report & Accounts 2019, p.3 (Capital), p.6 (KPI "
        "table) - " + FY2019_URL + "\n"
        f"FY2018 (own) & FY2017 (comparative): Annual Report & Accounts 2018, p.3-4 (Capital and KPI table) "
        "- " + FY2018_URL + "\n"
        f"FY2016 (own) & FY2015 (comparative): Annual Report & Accounts 2016, p.3-4 (Capital and KPI table) "
        "- " + FY2016_URL + "\n"
        f"FY2014: Annual Report & Accounts 2014, p.2 (Capital, narrative only - no KPI table) - " + FY2014_URL + "\n"
        + "No standalone Pillar 3/KM1 disclosure document was found on the bank's own site (www.kingdom.bank) "
        "or via Companies House in any year. However, correction to an earlier assumption in this workbook: "
        "each Annual Report from FY2015 onward DOES disclose a Core Equity Tier 1 ('CET1') ratio, a Leverage "
        "ratio and a Liquidity Coverage Requirement ('LCR') ratio as three of several 'Key performance "
        "indicators' in the Strategic Report (a KPI table, not a Pillar 3/KM1 document) - re-verified "
        "directly against seven of this bank's own primary-source PDFs during HD-045 (2026-09-05), which "
        "also confirmed the KPI table did not yet exist in FY2014 (narrative-only Capital paragraph that "
        "year, consistent with the pre-KPI-table pattern). No year, including FY2014, discloses a Total "
        "Capital ratio, Total RWAs figure, NSFR or MREL ratio in any form - see those sheets' own notes. "
        "This is otherwise consistent with the PRA's Small Domestic Deposit Taker (SDDT) thin-disclosure "
        "pattern already seen at Cynergy Bank Plc/DF Capital Bank Limited in this project."
    )


NOT_DISCLOSED_NOTE = (
    "Not publicly disclosed in any of the 12 years reviewed (FY2014-FY2025). Kingdom Bank's Annual Reports "
    "disclose a CET1 ratio, Leverage ratio and LCR ratio (see those sheets) via each year's Strategic Report "
    "'Key performance indicators' table (from FY2015 onward), but never a Total Capital ratio, a Total RWAs "
    "figure, an NSFR or an MREL ratio in any year, and no standalone Pillar 3 document exists on the bank's "
    "own site or via Companies House. See the CET1 Capital/CET1 Ratio sheets' source note for the SDDT-"
    "regime context that plausibly explains this."
)

TIER1_NOTE = (
    "Kingdom Bank's own Annual Reports state regulatory capital consists only of shareholders' funds "
    "(\"Core Equity Tier 1\") and subordinated liabilities (\"Tier 2\") - no Additional Tier 1 instruments "
    "are in issue in any year reviewed, so Tier 1 Capital equals CET1 Capital exactly. See the CET1 Capital "
    "sheet for the same figures and source."
)

TIER1_RATIO_NOTE = (
    "Tier 1 Ratio equals the CET1 Ratio exactly in every year - Kingdom Bank has never had any Additional "
    "Tier 1 capital in issue (see the Tier 1 Capital sheet), so Tier 1 Capital = CET1 Capital and therefore "
    "Tier 1 Capital / RWA = CET1 Capital / RWA. See the CET1 Ratio sheet for the same figures and source."
)

RWA_NOT_DISCLOSED_NOTE = (
    "Not publicly disclosed. No Total RWAs figure is disclosed by Kingdom Bank in any of the 12 years "
    "reviewed (see the Total RWAs sheet's source note), so no RWA-by-risk-category breakdown exists either - "
    "no standalone Pillar 3 document was located on the bank's own site or via Companies House."
)

bw = BankWorkbook(bank_name="Kingdom Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="7A1F2B")

# ---------------------------------------------------------------
# Sheet 1: Balance Sheet - built first per the equity reconciliation
# ladder so each year's own Total equity is an independent check value.
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {
        "FY2025": 38497, "FY2024": 38548, "FY2023": 34064, "FY2022": 23032, "FY2021": 10087,
        "FY2020": 6678, "FY2019": 6502, "FY2018": 4502, "FY2017": 4523, "FY2016": 4261, "FY2015": 3993, "FY2014": 3973,
    }),
    ("DATA", "Loans and advances to banks (FY2014's own label: 'Loans and advances to credit institutions')", {
        "FY2025": 1217, "FY2024": 1243, "FY2023": 994, "FY2022": 1829, "FY2021": 10795,
        "FY2020": 14135, "FY2019": 5509, "FY2018": 5939, "FY2017": 11311, "FY2016": 9864, "FY2015": 10981, "FY2014": 11905,
    }),
    ("DATA", "Loans and advances to customers", {
        "FY2025": 118242, "FY2024": 97733, "FY2023": 77532, "FY2022": 63291, "FY2021": 53795,
        "FY2020": 47114, "FY2019": 45339, "FY2018": 41404, "FY2017": 38438, "FY2016": 35336, "FY2015": 33028, "FY2014": 29724,
    }),
    ("DATA", "Debt securities (FY2014 only)", {"FY2014": 0}),
    ("DATA", "Investment property", {"FY2025": 650, "FY2020": 667, "FY2019": 667, "FY2018": 667, "FY2017": 500, "FY2016": 498}),
    ("DATA", "Intangible fixed assets", {
        "FY2025": 18, "FY2024": 39, "FY2023": 75, "FY2022": 76, "FY2021": 83,
        "FY2020": 69, "FY2019": 69, "FY2018": 122, "FY2017": 189, "FY2016": 255, "FY2015": 168, "FY2014": 131,
    }),
    ("DATA", "Tangible fixed assets (FY2014 figure includes freehold investment property, not separately disclosed that year)", {
        "FY2025": 171, "FY2024": 174, "FY2023": 192, "FY2022": 230, "FY2021": 268,
        "FY2020": 730, "FY2019": 742, "FY2018": 685, "FY2017": 842, "FY2016": 845, "FY2015": 1369, "FY2014": 3883,
    }),
    ("DATA", "Other assets", {
        "FY2025": 23, "FY2024": 63, "FY2023": 37, "FY2022": 481, "FY2021": 347,
        "FY2020": 388, "FY2019": 482, "FY2018": 484, "FY2017": 447, "FY2016": 390, "FY2015": 270,
    }),
    ("DATA", "Prepayments and accrued income", {"FY2025": 1056, "FY2024": 662, "FY2023": 571}),
    ("DATA", "Prepayments, accrued income and other assets (FY2014 combined line - see note)", {"FY2014": 227}),
    ("DATA", "Deferred tax assets", {"FY2025": 297, "FY2024": 30, "FY2023": 44, "FY2022": 83, "FY2021": 166}),
    ("TOTAL", "Total assets", {
        "FY2025": 160171, "FY2024": 138492, "FY2023": 113509, "FY2022": 89022, "FY2021": 75541,
        "FY2020": 69781, "FY2019": 59310, "FY2018": 53803, "FY2017": 56250, "FY2016": 51449, "FY2015": 49809, "FY2014": 49843,
    }),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer accounts", {
        "FY2025": 141758, "FY2024": 121269, "FY2023": 102091, "FY2022": 78452, "FY2021": 66668,
        "FY2020": 61287, "FY2019": 51378, "FY2018": 46112, "FY2017": 48656, "FY2016": 43885, "FY2015": 41906, "FY2014": 42935,
    }),
    ("DATA", "Other liabilities", {
        "FY2025": 616, "FY2024": 448, "FY2023": 438, "FY2022": 517, "FY2021": 661,
        "FY2020": 292, "FY2019": 356, "FY2018": 352, "FY2017": 235, "FY2016": 316, "FY2015": 591, "FY2014": 267,
    }),
    ("DATA", "Accruals and deferred income", {"FY2025": 1289, "FY2024": 563, "FY2023": 404}),
    ("DATA", "Subordinated liabilities (FY2014's own label: 'Subordinated deposits')", {
        "FY2025": 700, "FY2024": 700, "FY2023": 700, "FY2022": 700, "FY2021": 761,
        "FY2020": 1431, "FY2019": 1431, "FY2018": 1431, "FY2017": 1581, "FY2016": 1581, "FY2015": 1681, "FY2014": 1681,
    }),
    ("TOTAL", "Total liabilities", {
        "FY2025": 144363, "FY2024": 122980, "FY2023": 103633, "FY2022": 79669, "FY2021": 68090,
        "FY2020": 63010, "FY2019": 53165, "FY2018": 47895, "FY2017": 50472, "FY2016": 45782, "FY2015": 44178, "FY2014": 44883,
    }),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {
        "FY2025": 13237, "FY2024": 12067, "FY2023": 6667, "FY2022": 6667, "FY2021": 4867,
        "FY2020": 4867, "FY2019": 4217, "FY2018": 4217, "FY2017": 4217, "FY2016": 4217, "FY2015": 4217, "FY2014": 4217,
    }),
    ("DATA", "Revaluation reserve (fully extinguished during FY2021 - see Statement of Changes in Equity sheet)", {
        "FY2020": 172, "FY2019": 172, "FY2018": 172, "FY2017": 172, "FY2016": 166, "FY2015": 164, "FY2014": 578,
    }),
    ("DATA", "Profit and loss account", {
        "FY2025": 2571, "FY2024": 3445, "FY2023": 3209, "FY2022": 2686, "FY2021": 2584,
        "FY2020": 1732, "FY2019": 1756, "FY2018": 1519, "FY2017": 1389, "FY2016": 1284, "FY2015": 1250, "FY2014": 165,
    }),
    ("TOTAL", "Total shareholders' funds", {
        "FY2025": 15808, "FY2024": 15512, "FY2023": 9876, "FY2022": 9353, "FY2021": 7451,
        "FY2020": 6771, "FY2019": 6145, "FY2018": 5908, "FY2017": 5778, "FY2016": 5667, "FY2015": 5631, "FY2014": 4960,
    }),
    ("TOTAL", "Total liabilities and total shareholders' funds", {
        "FY2025": 160171, "FY2024": 138492, "FY2023": 113509, "FY2022": 89022, "FY2021": 75541,
        "FY2020": 69781, "FY2019": 59310, "FY2018": 53803, "FY2017": 56250, "FY2016": 51449, "FY2015": 49809, "FY2014": 49843,
    }),
]

bw.add_balance_sheet_sheet(
    title="Kingdom Bank Limited — Balance Sheet",
    subtitle="Statement of financial position, Bank/solo basis, £'000. See source note at bottom.",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=460,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet 2: Profit & Loss
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable", {
        "FY2025": 8637, "FY2024": 7828, "FY2023": 6003, "FY2022": 3144, "FY2021": 2419,
        "FY2020": 2297, "FY2019": 2330, "FY2018": 2168, "FY2017": 1955, "FY2016": 1904, "FY2015": 1744, "FY2014": 1699,
    }),
    ("DATA", "Interest payable", {
        "FY2025": -2942, "FY2024": -3207, "FY2023": -2193, "FY2022": -454, "FY2021": -345,
        "FY2020": -523, "FY2019": -552, "FY2018": -495, "FY2017": -478, "FY2016": -527, "FY2015": -511, "FY2014": -650,
    }),
    ("TOTAL", "Net interest income", {
        "FY2025": 5695, "FY2024": 4621, "FY2023": 3810, "FY2022": 2690, "FY2021": 2074,
        "FY2020": 1774, "FY2019": 1778, "FY2018": 1673, "FY2017": 1477, "FY2016": 1377, "FY2015": 1233, "FY2014": 1049,
    }),
    ("DATA", "Insurance commission income (FY2014's own label: 'Fees and commission receivable/(payable), net')", {
        "FY2025": 666, "FY2024": 576, "FY2023": 543, "FY2022": 482, "FY2021": 419,
        "FY2020": 433, "FY2019": 388, "FY2018": 369, "FY2017": 335, "FY2016": 319, "FY2015": 315, "FY2014": 361,
    }),
    ("DATA", "Other operating income", {
        "FY2025": 43, "FY2024": 8, "FY2023": 7, "FY2022": 3, "FY2021": 117,
        "FY2020": 80, "FY2019": 76, "FY2018": 64, "FY2017": 63, "FY2016": 59, "FY2015": 89, "FY2014": 138,
    }),
    ("TOTAL", "Total net income (FY2014-FY2022's own equivalent subtotal is labelled 'Operating income' - same calculation)",
     {
         "FY2025": 6404, "FY2024": 5205, "FY2023": 4360, "FY2022": 3175, "FY2021": 2610,
         "FY2020": 2287, "FY2019": 2242, "FY2018": 2106, "FY2017": 1875, "FY2016": 1755, "FY2015": 1637, "FY2014": 1548,
     }),
    ("DATA", "Administrative expenses", {
        "FY2025": -7241, "FY2024": -4776, "FY2023": -3597, "FY2022": -2953, "FY2021": -2437,
        "FY2020": -2167, "FY2019": -1780, "FY2018": -1776, "FY2017": -1538, "FY2016": -1554, "FY2015": -1487, "FY2014": -1413,
    }),
    ("DATA", "Depreciation and amortisation", {
        "FY2025": -67, "FY2024": -79, "FY2023": -86, "FY2022": -85, "FY2021": -80,
        "FY2020": -81, "FY2019": -93, "FY2018": -109, "FY2017": -111, "FY2016": -130, "FY2015": -124, "FY2014": -113,
    }),
    ("DATA", "Profit on sale / unrealised surplus on revaluation of investment property", {
        "FY2022": 0, "FY2021": 634, "FY2018": 0, "FY2017": 2, "FY2015": 898,
    }),
    ("DATA", "Movement in loan loss provision (FY2014's own label: 'Provision for bad and doubtful debts')", {
        "FY2025": -158, "FY2024": -9, "FY2023": -12, "FY2022": -9, "FY2021": -24,
        "FY2020": -77, "FY2019": -43, "FY2018": -43, "FY2017": -88, "FY2016": -16, "FY2015": -21, "FY2014": 70,
    }),
    ("TOTAL", "(Loss)/profit on ordinary activities before taxation", {
        "FY2025": -1062, "FY2024": 341, "FY2023": 665, "FY2022": 128, "FY2021": 703,
        "FY2020": -38, "FY2019": 326, "FY2018": 178, "FY2017": 140, "FY2016": 55, "FY2015": 903, "FY2014": 92,
    }),
    ("DATA", "Tax credit/(charge) on (loss)/profit", {
        "FY2025": 258, "FY2024": -62, "FY2023": -142, "FY2022": -26, "FY2021": -23,
        "FY2020": 14, "FY2019": -69, "FY2018": -32, "FY2017": -35, "FY2016": -21, "FY2015": -183, "FY2014": -23,
    }),
    ("TOTAL", "(Loss)/profit and total comprehensive income for the financial year", {
        "FY2025": -804, "FY2024": 279, "FY2023": 523, "FY2022": 102, "FY2021": 680,
        "FY2020": -24, "FY2019": 257, "FY2018": 146, "FY2017": 105, "FY2016": 34, "FY2015": 720, "FY2014": 69,
    }),
]

bw.add_income_statement_sheet(
    title="Kingdom Bank Limited — Profit & Loss",
    subtitle="Income statement, Bank/solo basis, £'000. All results arise from continuing operations, attributable to the "
              "owners of the Bank, every year. See source note at bottom.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=90,
    source_height=460,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet 3: Statement of Changes in Equity - per-year reconciliation
# ladder confirmed: every year's own closing balance ties exactly to
# both the next year's own opening balance and that year's own Balance
# Sheet Total shareholders' funds, FY2014 onward. Zero plug rows needed
# anywhere. FY2014's own closing balance is used here (old UK GAAP, as
# originally filed) rather than the FRS 102-restated 1 January 2015
# opening figure the FY2015 Annual Report separately discloses - see
# the source note below for the one reconciling break this creates.
# ---------------------------------------------------------------
equity_headers = ["Called up share capital", "Profit and loss account", "Revaluation reserve", "Total shareholders' funds"]
equity_rows = [
    ("TOTAL", "Balance as at 1 January 2014 (own report, old UK GAAP/BBA SORP)", (4217, 96, 333, 4646)),
    ("DATA", "Profit for the financial year", (None, 69, None, 69)),
    ("DATA", "Revaluation surplus during the year on investment properties", (None, None, 167, 167)),
    ("DATA", "Revaluation deficit during the year on investment properties", (None, None, -10, -10)),
    ("DATA", "Revaluation surplus during the year on freehold buildings", (None, None, 88, 88)),
    ("TOTAL", "Balance as at 31 December 2014 (FY2014 closing, own report)", (4217, 165, 578, 4960)),
    ("DATA", "FRS 102 first-time-adoption restatement (see source note - not a FY2014 or FY2015 P&L movement)",
     (None, 365, -478, -113)),
    ("TOTAL", "Balance as at 1 January 2015 (FRS 102-restated, per FY2015 Annual Report SOCE)", (4217, 530, 100, 4847)),
    ("DATA", "Profit for the financial year", (None, 720, None, 720)),
    ("DATA", "Unrealised surplus on revaluation of operating properties, net of deferred tax", (None, None, 64, 64)),
    ("TOTAL", "Balance as at 31 December 2015 (FY2015 closing)", (4217, 1250, 164, 5631)),
    ("DATA", "Profit for the financial year", (None, 34, None, 34)),
    ("DATA", "Unrealised surplus on revaluation of operating properties, net of deferred tax", (None, None, 2, 2)),
    ("TOTAL", "Balance as at 31 December 2016 (FY2016 closing)", (4217, 1284, 166, 5667)),
    ("DATA", "Profit for the financial year", (None, 105, None, 105)),
    ("DATA", "Unrealised surplus on revaluation of operating property, net of deferred tax", (None, None, 6, 6)),
    ("TOTAL", "Balance as at 31 December 2017 (FY2017 closing)", (4217, 1389, 172, 5778)),
    ("DATA", "Profit for the financial year", (None, 146, None, 146)),
    ("DATA", "Dividends paid", (None, -16, None, -16)),
    ("TOTAL", "Balance as at 31 December 2018 (FY2018 closing)", (4217, 1519, 172, 5908)),
    ("DATA", "Profit for the financial year", (None, 257, None, 257)),
    ("TOTAL", "Balance as at 31 December 2019 (FY2019 closing)", (4217, 1756, 172, 6145)),
    ("DATA", "Loss for the financial year", (None, -24, None, -24)),
    ("DATA", "Share allotment", (650, None, None, 650)),
    ("TOTAL", "Balance as at 31 December 2020 (FY2020 closing)", (4867, 1732, 172, 6771)),
    ("DATA", "Profit for the financial year", (None, 680, None, 680)),
    ("DATA", "Transfer of revaluation reserve to profit and loss reserve upon reclassification of operating property", (None, 172, -172, None)),
    ("TOTAL", "Balance as at 31 December 2021 (FY2021 closing)", (4867, 2584, 0, 7451)),
    ("DATA", "Profit for the financial year", (None, 102, None, 102)),
    ("DATA", "Share allotment", (1800, None, None, 1800)),
    ("TOTAL", "Balance as at 31 December 2022 (FY2022 closing)", (6667, 2686, 0, 9353)),
    ("DATA", "Profit for the financial year", (None, 523, None, 523)),
    ("TOTAL", "Balance as at 31 December 2023 (FY2023 closing)", (6667, 3209, 0, 9876)),
    ("DATA", "Profit for the financial year", (None, 279, None, 279)),
    ("DATA", "Share allotment", (5400, None, None, 5400)),
    ("DATA", "Dividends paid", (None, -43, None, -43)),
    ("TOTAL", "Balance as at 31 December 2024 (FY2024 closing)", (12067, 3445, 0, 15512)),
    ("DATA", "Loss for the financial year", (None, -804, None, -804)),
    ("DATA", "Share allotment", (1170, None, None, 1170)),
    ("DATA", "Dividends paid", (None, -70, None, -70)),
    ("TOTAL", "Balance as at 31 December 2025 (FY2025 closing)", (13237, 2571, 0, 15808)),
]

bw.add_equity_changes_sheet(
    title="Kingdom Bank Limited — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest. Equity reconciliation ladder confirmed: every year's own "
              "closing balance ties exactly to both the next year's own opening balance and that year's own Balance "
              "Sheet Total shareholders' funds - zero plug rows needed anywhere, FY2014 onward. £'000. FY2014 is "
              "shown as originally filed under old UK GAAP/the BBA SORP (no SOCE was published that year - built "
              "here from Notes 16-19 of the FY2014 Annual Report); FRS 102 was first adopted for FY2015 and its "
              "Annual Report separately discloses a restated 1 January 2015 opening position (£4,847k total "
              "shareholders' funds) that differs from the £4,960k shown here as FY2014's own closing figure - both "
              "are shown, with the reconciling FRS 102 transition adjustment on its own row, so the ladder still "
              "ties exactly on both sides of the GAAP change. The Revaluation reserve column runs down from £578k "
              "(FY2014) to a flat £172k (FY2017-FY2020) as historical property revaluations were realised, and is "
              "fully extinguished from FY2021 onward (see FY2021's transfer row) and shown as 0, not blank, for "
              "FY2022-FY2025 to make the reconciliation explicit.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
)

# ---------------------------------------------------------------
# Sheet 4: Cash Flow Statement - FY2014 has no cash flow statement at
# all (FRS 1 wholly-owned-subsidiary exemption - see source note), so
# it is the one column left entirely blank on this sheet, not zero.
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Net cash (used in)/generated from operating activities excluding tax", {
        "FY2025": -1079, "FY2024": -481, "FY2023": 10255, "FY2022": 3157, "FY2021": -630,
        "FY2020": 7026, "FY2019": 1978, "FY2018": -4088, "FY2017": 1125, "FY2016": 718, "FY2015": -5610,
    }),
    ("DATA", "Taxation paid", {
        "FY2025": -55, "FY2024": -102, "FY2023": -11, "FY2022": -25,
        "FY2020": -56, "FY2019": -40, "FY2018": -33, "FY2017": -23, "FY2016": -233, "FY2015": -2,
    }),
    ("TOTAL", "Net cash (used in)/generated from operating activities", {
        "FY2025": -1134, "FY2024": -583, "FY2023": 10244, "FY2022": 3132, "FY2021": -630,
        "FY2020": 6970, "FY2019": 1938, "FY2018": -4121, "FY2017": 1102, "FY2016": 485, "FY2015": -5612,
    }),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of intangible assets", {
        "FY2025": 0, "FY2024": 0, "FY2023": -23, "FY2022": -16, "FY2021": -47,
        "FY2020": -39, "FY2019": -8, "FY2018": -12, "FY2017": -16, "FY2016": -170, "FY2015": -33,
    }),
    ("DATA", "Capital expenditure on investment property", {"FY2015": -13}),
    ("DATA", "Purchase of tangible assets", {
        "FY2025": -43, "FY2024": -41, "FY2023": -24, "FY2022": -24, "FY2021": -197,
        "FY2020": -30, "FY2019": -89, "FY2018": -40, "FY2017": -15, "FY2016": -21, "FY2015": -23,
    }),
    ("DATA", "Sale of investment property / proceeds from disposals of investment property", {"FY2021": 2013, "FY2015": 3394}),
    ("TOTAL", "Net cash (used in)/generated from investing activities", {
        "FY2025": -43, "FY2024": -41, "FY2023": -47, "FY2022": -40, "FY2021": 1769,
        "FY2020": -69, "FY2019": -97, "FY2018": -52, "FY2017": -31, "FY2016": -191, "FY2015": 3325,
    }),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Repayment of subordinated liabilities", {
        "FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": -61, "FY2021": -670, "FY2018": -150, "FY2016": -800,
    }),
    ("DATA", "Issue of subordinated liabilities", {"FY2016": 700}),
    ("DATA", "Share allotment", {
        "FY2025": 1170, "FY2024": 5400, "FY2023": 0, "FY2022": 1800, "FY2021": 0, "FY2020": 650,
    }),
    ("DATA", "Dividends paid", {"FY2025": -70, "FY2024": -43, "FY2019": -20, "FY2018": -16}),
    ("TOTAL", "Net cash generated from/(used in) financing activities", {
        "FY2025": 1100, "FY2024": 5357, "FY2023": 0, "FY2022": 1739, "FY2021": -670,
        "FY2020": 650, "FY2019": -20, "FY2018": -166, "FY2017": 0, "FY2016": -100, "FY2015": 0,
    }),
    ("TOTAL", "Net movement in cash and cash equivalents", {
        "FY2025": -77, "FY2024": 4733, "FY2023": 10197, "FY2022": 4831, "FY2021": 469,
        "FY2020": 7551, "FY2019": 1821, "FY2018": -4339, "FY2017": 1071, "FY2016": 194, "FY2015": -2287,
    }),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {
        "FY2025": 39791, "FY2024": 35058, "FY2023": 24861, "FY2022": 20030, "FY2021": 19561,
        "FY2020": 12010, "FY2019": 10189, "FY2018": 14528, "FY2017": 13457, "FY2016": 13263, "FY2015": 15550,
    }),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {
        "FY2025": 39714, "FY2024": 39791, "FY2023": 35058, "FY2022": 24861, "FY2021": 20030,
        "FY2020": 19561, "FY2019": 12010, "FY2018": 10189, "FY2017": 14528, "FY2016": 13457, "FY2015": 13263,
    }),
]

bw.add_cash_flow_sheet(
    title="Kingdom Bank Limited — Statement of Cash Flows",
    subtitle="Bank/solo basis, £'000. FY2014 has no cash flow statement (FRS 1 wholly-owned-subsidiary exemption - "
              "column intentionally blank, not zero). See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=68,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet 5: Asset Quality - loan book by product (Note 12a/9a) plus loan
# loss provision movement, incl. collective/IBNR split where disclosed
# (Note 12c, FY2022 onward only). No IFRS 9 stage split exists - FRS 102
# (old UK GAAP for FY2014) entity, not IFRS 9. FY2014 used a one-off,
# more granular General/Specific/suspended-interest provision structure
# - see the dedicated FY2014-only rows below.
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, gross", {}),
    ("DATA", "Organisational/Charity mortgages (FY2014-FY2021's own label: 'Charity mortgages')", {
        "FY2025": 98455, "FY2024": 79806, "FY2023": 60628, "FY2022": 48320, "FY2021": 42846,
        "FY2020": 40095, "FY2019": 40653, "FY2018": 40390, "FY2017": 37417, "FY2016": 34479, "FY2015": 31898, "FY2014": 29039,
    }),
    ("DATA", "Personal mortgages", {
        "FY2025": 19897, "FY2024": 18049, "FY2023": 17017, "FY2022": 15086, "FY2021": 11063,
        "FY2020": 7074, "FY2019": 4659, "FY2018": 1008, "FY2017": 1027, "FY2016": 764, "FY2015": 993, "FY2014": 538,
    }),
    ("DATA", "Charity loans, unsecured (FY2014-FY2018 only - discontinued as a separate category from FY2019)", {
        "FY2018": 6, "FY2017": 20, "FY2016": 34, "FY2015": 46, "FY2014": 56,
    }),
    ("DATA", "Personal loans, unsecured (FY2014-FY2018 only - discontinued as a separate category from FY2019)", {
        "FY2018": 4, "FY2017": 9, "FY2016": 4, "FY2015": 18, "FY2014": 10,
    }),
    ("DATA", "Fully secured lending to other group companies (FY2014-FY2021 only)", {
        "FY2021": 0, "FY2020": 269, "FY2019": 274, "FY2018": 279, "FY2017": 282, "FY2016": 284, "FY2015": 286, "FY2014": 289,
    }),
    ("DATA", "Unsecured lending to other group companies (FY2014 only - nil that year)", {"FY2014": 0}),
    ("DATA", "Unsecured personal loans", {"FY2025": 89, "FY2024": 72, "FY2023": 72, "FY2022": 58, "FY2021": 50}),
    ("TOTAL", "Gross advances to customers", {
        "FY2025": 118441, "FY2024": 97927, "FY2023": 77717, "FY2022": 63464, "FY2021": 53959,
        "FY2020": 47438, "FY2019": 45586, "FY2018": 41687, "FY2017": 38755, "FY2016": 35565, "FY2015": 33241, "FY2014": 29932,
    }),
    ("DATA", "Less: loan loss provision", {
        "FY2025": -199, "FY2024": -194, "FY2023": -185, "FY2022": -173, "FY2021": -164,
        "FY2020": -324, "FY2019": -247, "FY2018": -283, "FY2017": -317, "FY2016": -229, "FY2015": -213, "FY2014": -192,
    }),
    ("DATA", "Less: provision for suspended interest (FY2014 only - old-GAAP structure, deducted separately from the main loan loss provision)",
     {"FY2014": -16}),
    ("TOTAL", "Net advances to customers", {
        "FY2025": 118242, "FY2024": 97733, "FY2023": 77532, "FY2022": 63291, "FY2021": 53795,
        "FY2020": 47114, "FY2019": 45339, "FY2018": 41404, "FY2017": 38438, "FY2016": 35336, "FY2015": 33028, "FY2014": 29724,
    }),
    ("DATA", "Loan loss provision coverage (% of gross advances)", {
        "FY2025": "0.17%", "FY2024": "0.20%", "FY2023": "0.24%", "FY2022": "0.27%", "FY2021": "0.30%",
        "FY2020": "0.68%", "FY2019": "0.54%", "FY2018": "0.68%", "FY2017": "0.82%", "FY2016": "0.64%", "FY2015": "0.64%", "FY2014": "0.64%",
    }),
    ("SECTION", "Loan loss provision movement (Note 12c/9c)", {}),
    ("DATA", "Balance at 1 January", {
        "FY2025": 194, "FY2024": 185, "FY2023": 173, "FY2022": 164, "FY2021": 324,
        "FY2020": 247, "FY2019": 283, "FY2018": 317, "FY2017": 229, "FY2016": 213, "FY2015": 192,
    }),
    ("DATA", "Charge for the year", {
        "FY2025": 160, "FY2024": 11, "FY2023": 13, "FY2022": 10, "FY2021": 26,
        "FY2020": 89, "FY2019": 44, "FY2018": 60, "FY2017": 113, "FY2016": 34, "FY2015": 46,
    }),
    ("DATA", "Utilised during the year", {
        "FY2025": -153, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": -184,
        "FY2020": 0, "FY2019": -79, "FY2018": -77,
    }),
    ("DATA", "Released during the year", {
        "FY2025": -2, "FY2024": -2, "FY2023": -1, "FY2022": -1, "FY2021": -2,
        "FY2020": -12, "FY2019": -1, "FY2018": -17, "FY2017": -25, "FY2016": -18, "FY2015": -25,
    }),
    ("TOTAL", "Balance at 31 December", {
        "FY2025": 199, "FY2024": 194, "FY2023": 185, "FY2022": 173, "FY2021": 164,
        "FY2020": 324, "FY2019": 247, "FY2018": 283, "FY2017": 317, "FY2016": 229, "FY2015": 213, "FY2014": 192,
    }),
    ("DATA", "Of which: collective/IBNR provision (not disclosed for FY2014-FY2021 - sub-split introduced FY2022 onward)",
     {"FY2025": 156, "FY2024": 148, "FY2023": 137, "FY2022": 124}),
    ("SECTION", "FY2014-only provision structure (old UK GAAP/BBA SORP - see source note)", {}),
    ("DATA", "General provision (IBNR-based): balance at 1 January", {"FY2014": 163}),
    ("DATA", "General provision (IBNR-based): released during the year", {"FY2014": -30}),
    ("DATA", "General provision (IBNR-based): balance at 31 December", {"FY2014": 133}),
    ("DATA", "Specific provision: balance at 1 January", {"FY2014": 99}),
    ("DATA", "Specific provision: charge for the year", {"FY2014": 22}),
    ("DATA", "Specific provision: released during the year", {"FY2014": -62}),
    ("DATA", "Specific provision: balance at 31 December", {"FY2014": 59}),
    ("DATA", "Provision for suspended interest: balance at 1 January", {"FY2014": 25}),
    ("DATA", "Provision for suspended interest: decrease during the year", {"FY2014": -9}),
    ("DATA", "Provision for suspended interest: balance at 31 December", {"FY2014": 16}),
]

bw.add_asset_quality_sheet(
    title="Kingdom Bank Limited — Asset Quality",
    subtitle="Loan book by product (Note 12a/9a) and loan loss provision movement (Note 12c/9c), Bank/solo basis, "
              "£'000. No IFRS 9 stage 1/2/3 split is disclosed in any year - this entity applies FRS 102 (old UK "
              "GAAP for FY2014), not IFRS 9. See source note at bottom.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=100,
    source_height=340,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
#
# HD-045 correction (2026-09-05): re-verifying seven of this bank's own
# primary-source PDFs to extend the build back to FY2014 turned up a
# Key Performance Indicators table in each year's Strategic Report
# (FY2015 onward) disclosing a CET1 ratio, Leverage ratio and LCR ratio
# - contradicting this workbook's earlier "not publicly disclosed"
# treatment of those three metrics for FY2021-FY2025. That treatment is
# corrected below with real, sourced figures for all years FY2015-
# FY2025 (FY2014 predates the KPI table and remains not disclosed).
# Total Capital Ratio, Total RWAs, NSFR and MREL Ratio remain genuinely
# undisclosed in every year, including FY2014 - see NOT_DISCLOSED_NOTE.
# ---------------------------------------------------------------

def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, f"Bank/solo basis, {unit}" if unit else "Bank/solo basis",
                         rows_data, p3_sources(), note=note, first_col_width=52, source_height=230)


CET1_VALUES = {
    "FY2025": 15808, "FY2024": 15512, "FY2023": 9876, "FY2022": 9353, "FY2021": 7451,
    "FY2020": 6771, "FY2019": 6145, "FY2018": 5908, "FY2017": 5778, "FY2016": 5667, "FY2015": 5631, "FY2014": 4960,
}
TIER2_VALUES = {
    "FY2025": 700, "FY2024": 700, "FY2023": 700, "FY2022": 700, "FY2021": 761,
    "FY2020": 1431, "FY2019": 1431, "FY2018": 1431, "FY2017": 1581, "FY2016": 1581, "FY2015": 1681, "FY2014": 1681,
}
TOTAL_CAPITAL_VALUES = {y: CET1_VALUES[y] + TIER2_VALUES[y] for y in YEARS}

CET1_RATIO_VALUES = {
    "FY2025": "18.8%", "FY2024": "22.2%", "FY2023": "17.37%", "FY2022": "20.84%", "FY2021": "16.97%",
    "FY2020": "17.13%", "FY2019": "15.27%", "FY2018": "14.57%", "FY2017": "14.41%", "FY2016": "16.25%", "FY2015": "14.45%",
}
LEVERAGE_RATIO_VALUES = {
    "FY2025": "12.4%", "FY2024": "10.8%", "FY2023": "7.96%", "FY2022": "10.02%", "FY2021": "9.03%",
    "FY2020": "9.37%", "FY2019": "9.40%", "FY2018": "10.10%", "FY2017": "9.38%", "FY2016": "10.09%", "FY2015": "8.96%",
}
LCR_VALUES = {
    "FY2025": "332.1%", "FY2024": "429.0%", "FY2023": "766.7%", "FY2022": "681.04%", "FY2021": "1,475.9%",
    "FY2020": "1,304.6%", "FY2019": "861.0%", "FY2018": "556.3%", "FY2017": "520.3%", "FY2016": "648.1%", "FY2015": "900.9%",
}

KPI_NOT_YET_INTRODUCED_NOTE = (
    "FY2014 predates this KPI table: the FY2014 Annual Report's Strategic Report 'Capital' section is "
    "narrative-only (£m totals for shareholders' funds and subordinated deposits, no ratio) - the Bank "
    "first began disclosing a CET1/Leverage/LCR KPI table from FY2015 onward (see the FY2016 Annual "
    "Report, which is this metric's earliest-available source, showing both FY2016 and FY2015). This is a "
    "genuine 'not yet introduced' gap, not a sourcing failure."
)

metric(
    "CET1 Capital", "£'000",
    [("Shareholders' funds (Core Equity Tier 1)", CET1_VALUES)],
)

metric(
    "CET1 Ratio", "%",
    [("CET1 ratio", CET1_RATIO_VALUES)],
    note=KPI_NOT_YET_INTRODUCED_NOTE,
)

metric(
    "Tier 1 Capital", "£'000",
    [("Shareholders' funds (Core Equity Tier 1)", CET1_VALUES)],
    note=TIER1_NOTE,
)

metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 ratio (= CET1 ratio - see note)", CET1_RATIO_VALUES)],
    note=TIER1_RATIO_NOTE + " " + KPI_NOT_YET_INTRODUCED_NOTE,
)

metric(
    "Total Capital", "£'000",
    [
        ("Shareholders' funds (Core Equity Tier 1)", CET1_VALUES),
        ("Subordinated liabilities (Tier 2)", TIER2_VALUES),
        ("Total regulatory capital (CET1 + Tier 2)", TOTAL_CAPITAL_VALUES),
    ],
)

bw.add_not_disclosed_metric_sheets(
    ["Total Capital Ratio", "Total RWAs"],
    p3_sources(),
    per_note={m: NOT_DISCLOSED_NOTE for m in ["Total Capital Ratio", "Total RWAs"]},
)

# RWA Breakdown - placed immediately after Total RWAs, before Leverage
# Ratio, per the locked sheet order. Not publicly disclosed (no RWA
# figure exists in any form for this bank - see Total RWAs sheet).
bw.add_rwa_breakdown_sheet(
    title="Kingdom Bank Limited — RWA Breakdown",
    subtitle="Bank/solo basis. Not publicly disclosed - see source note.",
    rows=[("DATA", "Not publicly disclosed", {})],
    sources_text=p3_sources() + "\n\n" + RWA_NOT_DISCLOSED_NOTE,
    first_col_width=54,
    source_height=230,
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio", LEVERAGE_RATIO_VALUES)],
    note=KPI_NOT_YET_INTRODUCED_NOTE,
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Requirement (LCR) ratio", LCR_VALUES)],
    note=KPI_NOT_YET_INTRODUCED_NOTE,
)

bw.add_not_disclosed_metric_sheets(
    ["NSFR", "MREL Ratio"],
    p3_sources(),
    per_note={m: NOT_DISCLOSED_NOTE for m in ["NSFR", "MREL Ratio"]},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {
            "FY2025": 160171, "FY2024": 138492, "FY2023": 113509, "FY2022": 89022, "FY2021": 75541,
            "FY2020": 69781, "FY2019": 59310, "FY2018": 53803, "FY2017": 56250, "FY2016": 51449, "FY2015": 49809, "FY2014": 49843,
        }),
        ("Loans and advances to customers", {
            "FY2025": 118242, "FY2024": 97733, "FY2023": 77532, "FY2022": 63291, "FY2021": 53795,
            "FY2020": 47114, "FY2019": 45339, "FY2018": 41404, "FY2017": 38438, "FY2016": 35336, "FY2015": 33028, "FY2014": 29724,
        }),
        ("Customer accounts", {
            "FY2025": 141758, "FY2024": 121269, "FY2023": 102091, "FY2022": 78452, "FY2021": 66668,
            "FY2020": 61287, "FY2019": 51378, "FY2018": 46112, "FY2017": 48656, "FY2016": 43885, "FY2015": 41906, "FY2014": 42935,
        }),
        ("Total shareholders' funds", {
            "FY2025": 15808, "FY2024": 15512, "FY2023": 9876, "FY2022": 9353, "FY2021": 7451,
            "FY2020": 6771, "FY2019": 6145, "FY2018": 5908, "FY2017": 5778, "FY2016": 5667, "FY2015": 5631, "FY2014": 4960,
        }),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total net income", {
            "FY2025": 6404, "FY2024": 5205, "FY2023": 4360, "FY2022": 3175, "FY2021": 2610,
            "FY2020": 2287, "FY2019": 2242, "FY2018": 2106, "FY2017": 1875, "FY2016": 1755, "FY2015": 1637, "FY2014": 1548,
        }),
        ("Administrative expenses", {
            "FY2025": -7241, "FY2024": -4776, "FY2023": -3597, "FY2022": -2953, "FY2021": -2437,
            "FY2020": -2167, "FY2019": -1780, "FY2018": -1776, "FY2017": -1538, "FY2016": -1554, "FY2015": -1487, "FY2014": -1413,
        }),
        ("(Loss)/profit for the financial year", {
            "FY2025": -804, "FY2024": 279, "FY2023": 523, "FY2022": 102, "FY2021": 680,
            "FY2020": -24, "FY2019": 257, "FY2018": 146, "FY2017": 105, "FY2016": 34, "FY2015": 720, "FY2014": 69,
        }),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening total shareholders' funds", {
            "FY2025": 15512, "FY2024": 9876, "FY2023": 9353, "FY2022": 7451, "FY2021": 6771,
            "FY2020": 6145, "FY2019": 5908, "FY2018": 5778, "FY2017": 5667, "FY2016": 5631, "FY2015": 4847, "FY2014": 4646,
        }),
        ("(Loss)/profit for the financial year", {
            "FY2025": -804, "FY2024": 279, "FY2023": 523, "FY2022": 102, "FY2021": 680,
            "FY2020": -24, "FY2019": 257, "FY2018": 146, "FY2017": 105, "FY2016": 34, "FY2015": 720, "FY2014": 69,
        }),
        ("Other equity movements, net", {
            "FY2025": 1100, "FY2024": 5357, "FY2023": 0, "FY2022": 1800, "FY2021": 0,
            "FY2020": 650, "FY2019": 0, "FY2018": -16, "FY2017": 6, "FY2016": 2, "FY2015": 64, "FY2014": 245,
        }),
        ("Closing total shareholders' funds", {
            "FY2025": 15808, "FY2024": 15512, "FY2023": 9876, "FY2022": 9353, "FY2021": 7451,
            "FY2020": 6771, "FY2019": 6145, "FY2018": 5908, "FY2017": 5778, "FY2016": 5667, "FY2015": 5631, "FY2014": 4960,
        }),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash flow from/(used in) operating activities", {
            "FY2025": -1134, "FY2024": -583, "FY2023": 10244, "FY2022": 3132, "FY2021": -630,
            "FY2020": 6970, "FY2019": 1938, "FY2018": -4121, "FY2017": 1102, "FY2016": 485, "FY2015": -5612,
        }),
        ("Net cash flow from/(used in) investing activities", {
            "FY2025": -43, "FY2024": -41, "FY2023": -47, "FY2022": -40, "FY2021": 1769,
            "FY2020": -69, "FY2019": -97, "FY2018": -52, "FY2017": -31, "FY2016": -191, "FY2015": 3325,
        }),
        ("Net cash flow from/(used in) financing activities", {
            "FY2025": 1100, "FY2024": 5357, "FY2023": 0, "FY2022": 1739, "FY2021": -670,
            "FY2020": 650, "FY2019": -20, "FY2018": -166, "FY2017": 0, "FY2016": -100, "FY2015": 0,
        }),
        ("Cash and cash equivalents at end of year", {
            "FY2025": 39714, "FY2024": 39791, "FY2023": 35058, "FY2022": 24861, "FY2021": 20030,
            "FY2020": 19561, "FY2019": 12010, "FY2018": 10189, "FY2017": 14528, "FY2016": 13457, "FY2015": 13263,
        }),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 ratio", CET1_RATIO_VALUES),
        ("Leverage ratio", LEVERAGE_RATIO_VALUES),
    ],
    note="No Pillar 3 ratio-type metrics (CET1/Tier 1/Total Capital Ratio, Leverage Ratio, LCR, NSFR, MREL "
         "Ratio) or Total RWAs are disclosed by Kingdom Bank via a standalone Pillar 3 document in any of the "
         "12 years reviewed, but a CET1 ratio and Leverage ratio (both charted above) plus an LCR ratio are "
         "disclosed as Key Performance Indicators in each year's Strategic Report from FY2015 onward (LCR is "
         "omitted from the chart above only because its scale, running into four figures in most years, "
         "dwarfs the other two - see the LCR sheet directly). FY2014 predates this KPI table and has no ratio "
         "data. Total Capital ratio, Total RWAs, NSFR and MREL ratio remain genuinely undisclosed in every "
         "year. CET1 Capital, Tier 1 Capital and Total Capital (£'000) are disclosed for all 12 years on "
         "their own sheets. Balance Sheet, Profit & Loss, Statement of Changes in Equity and Cash Flow "
         "figures are duplicated from their own sheets for at-a-glance trend viewing - how the bank is using "
         "its money (steady growth in loans and advances to churches/charities/individuals, funded by "
         "customer deposits) and the risk it is taking with it (a small, consistently sub-1%-of-gross-"
         "advances loan loss provision throughout). FY2014 has no cash flow figures (see the Cash Flow "
         "Statement sheet's source note).",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/KINGDOM BANK FINANCIALS.xlsx")
