import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2026", "FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019"]  # most recent first, y/e 31 March
YEAR_LABEL = {y: y for y in YEARS}

AR2026_URL = "https://www.hoaresbank.co.uk/files/2026-06/Financial_Report_2026.pdf"
AR2025_URL = "https://www.hoaresbank.co.uk/files/2025-07/Financial_Report_2025.pdf"
AR2024_URL = "https://www.hoaresbank.co.uk/files/2024-06/Financial_Report_2024.pdf"
AR2023_URL = "https://www.hoaresbank.co.uk/files/2023-07/Financial_Report_2023.pdf"
AR2022_URL = "https://www.hoaresbank.co.uk/files/2022-07/Annual_Report_2022.pdf"
AR2021_URL = "https://www.hoaresbank.co.uk/files/2021-10/CHC_Cons_Accounts21.pdf"
AR2020_URL = "https://www.hoaresbank.co.uk/files/2021-05/Annual_Report_and_Accounts_for_2020.pdf"
AR2019_URL = "https://www.hoaresbank.co.uk/files/2021-05/Financial_Report_2019.pdf"

P3_2025_URL = "https://www.hoaresbank.co.uk/files/2025-07/Pillar_3_Disclosure_2025.pdf"
P3_2024_URL = "https://www.hoaresbank.co.uk/files/2024-06/Pillar_3_Disclosure_2024.pdf"
P3_2023_URL = "https://www.hoaresbank.co.uk/files/2023-07/Pillar_3_Disclosure_2023.pdf"
P3_2022_URL = "https://www.hoaresbank.co.uk/files/2022-07/2022_Pillar_3_Disclosures_0.pdf"
P3_2021_URL = "https://www.hoaresbank.co.uk/files/2021-10/CHC_2021_Pillar_3_Disclosures.pdf"
# FY2019 edition: published on the bank's pre-Drupal site at
# hoaresbank.co.uk/sites/default/files/styles/ and NOT carried over in the 2021
# migration that back-loaded the older annual reports into /files/2021-05/ and
# /files/2021-06/.  The original path now returns an honest 404 (verified, as
# did a deliberate control filename in the same directory), so the Wayback
# timestamped `id_` capture is the live citation and the original path is kept
# below as a labelled dead fallback rather than deleted.
P3_2019_URL = ("https://web.archive.org/web/20190923044126id_/https://www.hoaresbank.co.uk/"
               "sites/default/files/styles/2019%20Pillar%203%20Disclosures.pdf")
P3_2019_ORIGINAL_DEAD_URL = ("https://www.hoaresbank.co.uk/sites/default/files/styles/"
                             "2019%20Pillar%203%20Disclosures.pdf")

ENTITY_NOTE = (
    "C. Hoare & Co. (company 00240822, FRN 122093) is a private unlimited company - Britain's oldest "
    "privately-owned bank, founded 1672, owned by the Hoare family. Despite the unlimited-company legal "
    "form, it voluntarily publishes full audited Consolidated (Group) accounts and Pillar 3 disclosures every "
    "year on its own site (hoaresbank.co.uk/financial-reports), all text-native, no OCR needed, 0 WebSearch "
    "calls used (all sourcing via WebFetch against the bank's own site and Companies House). Fiscal year-end "
    "31 March. Every figure below is each year's own originally-published report - not a later restated "
    "comparative. (Two narrow, documented exceptions, both on the Pillar 3 sheets and both flagged where "
    "they occur: FY2020 Pillar 3 figures come from the FY2021 edition's comparative column because no "
    "standalone FY2020 edition exists by any route; and the FY2021 LCR comes from the FY2022 edition's "
    "comparative because the FY2021 edition printed no numeric LCR at all.) FY2025's report introduced a new 'Effect of exchange rate changes' line splitting out what "
    "FY2024's own report folded into a single net-change figure; FY2024's own presentation (no separate FX "
    "line) is preserved here rather than using FY2025's restated split. FY2024's own printed 'Net decrease in "
    "cash and cash equivalents' (164,034) is £1k off from summing its own three section totals (164,033) - an "
    "immaterial rounding artifact in the source document itself, kept as printed. The bank stopped publishing "
    "Pillar 3 disclosures entirely after FY2025: its Financial Report 2026 records that it was approved under "
    "the PRA's Small Domestic Deposit Taking (SDDT) regime in December 2025 and 'no longer prepares Pillar III "
    "disclosures'. FY2026 Pillar 3 figures here therefore come from the Annual Report's own capital note "
    "instead, and the metrics that note does not print are blank rather than estimated.\n"
    "SDDT DATE TEST (independently corroborated 2026-09-15): the PRA's 'Consolidated Waivers list for "
    "PRA-regulated firms - as of 1 July 2026' (bankofengland.co.uk/prudential-regulation/authorisations/"
    "waivers-and-modifications-of-rules) records that C. HOARE & CO. (FRN 122093) holds a 'Modification by "
    "Consent - PRA Rulebook - CRR Firms - Rule 3.1 of the SDDT Regime - General Application Part', sub-rule 'Ru "
    "3.1', with a start date of 09/12/2025 and no end date (still in force). That register date matches the "
    "Bank's own Financial Report 2026 statement of approval 'in December 2025' exactly, so the regulatory record "
    "and the Bank's own account agree. Rule 3.1 removes the Pillar 3 disclosure obligation outright, which is a "
    "stronger and distinct relief from UK CRR Article 433b (that one merely reduces disclosure frequency and "
    "content for small and non-complex institutions); the two must not be conflated. Applying the date test to "
    "this Bank's 31 March year-end: FY2025 (y/e 31 March 2025) PREDATES the modification, so a Pillar 3 was "
    "still required - and the Pillar 3 Disclosures 2025 duly exists and is cited throughout this workbook. "
    "FY2026 (y/e 31 March 2026) falls after it, so the FY2026 blanks are a permanent structural end to the "
    "series rather than a document that is late or merely hard to obtain."
)

CASH_FLOW_SOURCES = (
    "Sources - C. Hoare & Co.'s own Consolidated Cash Flow Statement, each year from its own year's Financial "
    "Report (not a later comparative):\n"
    f"FY2026: Financial Report 2026, p.53 (Consolidated Cash Flow Statement) - {AR2026_URL}\n"
    f"FY2025: Financial Report 2025, p.39 (Consolidated Cash Flow Statement) - {AR2025_URL}\n"
    f"FY2024: Financial Report 2024, p.41 (Consolidated Cash Flow Statement) - {AR2024_URL}\n"
    f"FY2023: Financial Report 2023, p.37 (Consolidated Cash Flow Statement) - {AR2023_URL}\n"
    f"FY2022: Annual Report 2022, p.36 (Consolidated Cash Flow Statement) - {AR2022_URL}\n"
    f"FY2021: Annual Report 2021, p.36 (Consolidated Cash Flow Statement) - {AR2021_URL}\n"
    f"FY2020: Annual Report 2020, p.33 (Consolidated Cash Flow Statement) - {AR2020_URL}\n"
    f"FY2019: Financial Report 2019, p.27 (Consolidated Cash Flow Statement) - {AR2019_URL}\n"
    "The face of the statement itself gives operating cash flow as a single pre-tax total (with a detailed "
    "profit/adjustments/working-capital breakdown in a separate Notes to the Cash Flow Statement note) - that "
    "single total is transcribed here as one DATA line rather than the full note-level breakdown, to keep row "
    "structure consistent across all 5 years.\n"
    + ENTITY_NOTE
)


def p3_sources(page):
    return (
        "Sources - C. Hoare & Co. Pillar 3 Disclosures, Appendix 1 (Own Funds Disclosure template, UK KM1 "
        "basis), solo-consolidated basis. Each year is cited to ITS OWN year's edition (every edition's "
        "period is taken from its cover, which reads 'Year ended 31 March <year>' - never from the "
        "filename):\n"
        f"FY2025: Pillar 3 Disclosures 2025, p.{page.get('recent','15')} - {P3_2025_URL}\n"
        f"FY2024: Pillar 3 Disclosures 2024, p.22 - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures 2023, p.25 - {P3_2023_URL}\n"
        f"FY2022: Pillar 3 Disclosures 2022, p.29 - {P3_2022_URL}\n"
        f"FY2021/FY2020: Pillar 3 Disclosures 2021, Table 3 'Capital Resources' p.12 and Own funds "
        f"disclosure template pp.32-35 - {P3_2021_URL}\n"
        f"FY2019: Pillar 3 Disclosures 2019, Table 3 'Capital Resources' p.19 and Appendix 1 'Own funds "
        f"disclosure template' pp.43-46 - {P3_2019_URL}\n"
        "FY2019 RETRIEVAL NOTE (added 2026-09-16): the FY2019 edition was previously recorded here as "
        "unavailable. It is not - it was published on the bank's pre-Drupal site and simply was not carried "
        "across in the 2021 site migration, which back-loaded the older ANNUAL REPORTS into /files/2021-05/ "
        "and /files/2021-06/ but no Pillar 3 of any vintage. Its original URL, "
        f"{P3_2019_ORIGINAL_DEAD_URL}, now returns an honest 404 (a deliberate control filename in the same "
        "directory returns the identical 404, so this host does not soft-404); the citation above is "
        "therefore the Internet Archive's timestamped capture of that exact path, 957,075 bytes, 54 pages, "
        "cover 'C. Hoare & Co. / Capital and Risk Management / Pillar 3 Disclosures / Year ended 31 March "
        "2019', last page confirmed to carry text. The dead original is kept on the record above rather "
        "than deleted. The FY2018 edition survives the same way (Year ended 31 March 2018, 53pp, "
        "web.archive.org/web/20210506235636id_/.../2018%20Pillar%203%20Disclosures.pdf) but falls outside "
        "this workbook's year range and is not used.\n"
        "FY2020 EDITION - ENUMERATED ABSENCE: no standalone FY2020 (y/e 31 March 2020) Pillar 3 edition "
        "could be found by any route - the live /financial-reports index, a Wayback CDX domain sweep of "
        "hoaresbank.co.uk, a CDX sweep of the pre-migration sites/default/files/styles/ directory, and "
        "direct-fetch of the exact filename pattern that does work for 2018 and 2019 all return nothing or "
        "honest 404s. This costs the workbook nothing: FY2020 is fully covered by the FY2021 edition's own "
        "comparative column, which is what is cited above.\n"
        "FY2026: the bank no longer publishes Pillar 3 disclosures at all. Its own Annual Report 2026 states "
        "that 'In December 2025 the bank was approved under the Small Domestic Deposit Taking regime by the "
        "PRA and, as such, it no longer prepares Pillar III disclosures.' FY2026 is therefore a permanent "
        "structural end to this series, not a document that is merely late. Where the FY2026 column IS "
        "populated below, the figure comes from the Directors' Report capital note in the Financial Report "
        "2026, p.32 ('The bank's regulatory capital, risk-weighted assets and capital ratios at 31st of March "
        f"were as follows') - {AR2026_URL}. That note is on the same basis as the Pillar 3 KM1 it replaces: "
        "its own 2025 comparative column (CET1 and Tier 1 capital GBP526,455k, total regulatory capital "
        "GBP531,333k, RWAs GBP2,289,414k) matches the Pillar 3 Disclosures 2025 KM1 rows 1-4 exactly. The "
        "note prints capital amounts and the CET1 and total capital ratios only - it carries no leverage "
        "ratio, LCR or NSFR, and no separately-labelled Tier 1 ratio row, so those sheets stay blank for "
        "FY2026 rather than being derived. Note also that the capital note rounds ratios to 1dp (22.7%, "
        "22.9%) where the Pillar 3 KM1 used 2dp; both are shown as printed.\n"
        + ENTITY_NOTE
    )


PAGES = {"recent": "15", "older": "26"}

bw = BankWorkbook(bank_name="C. Hoare & Co.", years=YEARS, year_label=YEAR_LABEL, header_color="6F1D1B")

# ---------------------------------------------------------------
# ST- rollout (batch ST-014): Balance Sheet, P&L, Statement of Changes in
# Equity, Asset Quality, RWA Breakdown. C. Hoare & Co. is a private
# unlimited company (not a partnership, despite general references to it
# as a "private bank" - its statutory accounts use standard Companies Act
# equity line items: Called up share capital, Reserve Fund, Revaluation
# reserves, Retained earnings, not partnership capital accounts). Group
# basis throughout (Company-only columns also published but not used
# here, consistent with the existing Cash Flow Statement/Pillar 3 sheets).
# ---------------------------------------------------------------
STATEMENTS_SOURCES = (
    "Sources - C. Hoare & Co.'s own Consolidated Statement of Comprehensive Income / Consolidated and Company "
    "Balance Sheets / Consolidated Statement of Changes in Equity (Group column only used), £'000, each from "
    "that year's own originally-published Financial Report:\n"
    f"FY2026: Financial Report 2026, pp.45,47,49 - {AR2026_URL}\n"
    f"FY2025: Financial Report 2025, pp.35,36,37 - {AR2025_URL}\n"
    f"FY2024: Financial Report 2024, pp.37,38,39 - {AR2024_URL}\n"
    f"FY2023: Financial Report 2023, pp.33,34,35 - {AR2023_URL}\n"
    f"FY2022: Annual Report 2022, pp.32,33,34 - {AR2022_URL}\n\n"
    f"FY2021: Annual Report 2021, pp.32,33,34 - {AR2021_URL}\n"
    f"FY2020: Annual Report 2020, pp.29,30,31 - {AR2020_URL}\n"
    f"FY2019: Financial Report 2019, pp.23,24,25 - {AR2019_URL}\n\n"
    "'Total financial assets' is broken down per each year's own Note 13 (Financial Assets), which is NOT a "
    "pure investment-securities note - it's the Bank's catch-all measurement-basis note covering Loans and "
    "advances to banks/customers alongside genuine investment securities, so those loan lines are broken out "
    "here too (not just the securities legs) to avoid overstating the investment book: FY2026 Financial Report "
    f"2026, p.72 - {AR2026_URL}; FY2025 Financial Report 2025, p.61 - {AR2025_URL}; FY2024 Financial Report "
    f"2024, p.61 - {AR2024_URL}; FY2023 Financial Report 2023, p.57 - {AR2023_URL}; FY2022 Annual Report 2022, "
    f"p.57 - {AR2022_URL}; FY2021 Annual Report 2021, p.60 - {AR2021_URL}; FY2020 Annual Report 2020, p.57 - "
    f"{AR2020_URL}; FY2019 Financial Report 2019, p.49 - {AR2019_URL}. The 'of which: UK government gilts' "
    "split within Debt securities is a disclosure introduced for the first time in the FY2026 Financial Report "
    "(£1,193,292k of the £2,967,631k FY2026 debt securities balance) - it is NOT backfilled to FY2025 or "
    "earlier years' own reports, which disclosed Debt securities only as one lump 'financial assets measured "
    "at amortised cost' sub-line with no government/other split; 'Non-UK-government debt securities' nets out "
    "exactly against 'UK government gilts' for FY2026 only, so the two together equal that year's full Debt "
    "securities figure without double-counting.\n\n"
    + ENTITY_NOTE
)

PRESENTATION_NOTE = (
    "PRESENTATION NOTE: the Balance Sheet's own 'Retained earnings' figure is the sum of two separate lines the "
    "Bank's own balance sheet prints ('Current year net income' + 'Retained earnings brought forward') - shown "
    "here as a single combined line to match the Statement of Changes in Equity's own single 'Retained Earnings' "
    "column, which already combines them. 'Deferred tax asset' only appears as its own Balance Sheet line "
    "FY2022-24 (nil/absent FY2025-26 on a Group basis); 'Post retirement benefit asset' only appears FY2022-23; "
    "'Post retirement benefit liability' only appears FY2024; 'Provision for other liabilities' only appears "
    "FY2022. 'Other operating income' is disclosed with the opposite sign convention in FY2022-23 (printed as "
    "'Other operating (expense)/income', both years negative) vs FY2024-26 (printed as 'Other operating income', "
    "all positive) - both reproduced as signed, not relabelled."
)

# ---------------------------------------------------------------
# Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {
        "FY2026": 896317, "FY2025": 1548443, "FY2024": 1345322, "FY2023": 1452949, "FY2022": 1843378}),
    ("DATA", "Items in course of collection from banks", {
        "FY2026": 316, "FY2025": 136, "FY2024": 266, "FY2023": 240, "FY2022": 330}),
    ("DATA", "Derivative financial instruments (assets)", {
        "FY2026": 215175, "FY2025": 100364, "FY2024": 117813, "FY2023": 126976, "FY2022": 110851}),
    ("DATA", "Total financial assets", {
        "FY2026": 6339519, "FY2025": 5399523, "FY2024": 5229721, "FY2023": 5164686, "FY2022": 5204233}),
    ("DATA", "Financial assets at fair value through profit or loss", {
        "FY2026": 371563, "FY2025": 595373, "FY2024": 593212, "FY2023": 352586, "FY2022": 652752}),
    ("DATA", "Investment in equity shares (financial assets at cost less impairment)", {
        "FY2026": 2530, "FY2025": 2530, "FY2024": 2529, "FY2023": 2529, "FY2022": 1528}),
    ("DATA", "Loans and advances to banks, at amortised cost", {
        "FY2026": 219597, "FY2025": 65834, "FY2024": 123470, "FY2023": 248662, "FY2022": 275813}),
    ("DATA", "Loans and advances to customers, net of impairment, at amortised cost", {
        "FY2026": 2579028, "FY2025": 2274402, "FY2024": 2116584, "FY2023": 1966972, "FY2022": 1994820}),
    ("DATA", "Bank and building society certificates of deposit (financial assets at amortised cost)", {
        "FY2026": 199170, "FY2025": 106148, "FY2024": 104099, "FY2023": 460996, "FY2022": 220405}),
    ("DATA", "Debt securities at amortised cost", {
        "FY2025": 2355236, "FY2024": 2289827, "FY2023": 2132941, "FY2022": 2058915}),
    ("DATA", "UK government gilts, within debt securities at amortised cost", {
        "FY2026": 1193292}),
    ("DATA", "Non-UK-government debt securities, at amortised cost", {
        "FY2026": 1774339}),
    ("DATA", "Intangible assets", {
        "FY2026": 37247, "FY2025": 31776, "FY2024": 17363, "FY2023": 16765, "FY2022": 17821}),
    ("DATA", "Property and equipment", {
        "FY2026": 52872, "FY2025": 53192, "FY2024": 50064, "FY2023": 51008, "FY2022": 55428}),
    ("DATA", "Heritage assets", {
        "FY2026": 15297, "FY2025": 15105, "FY2024": 15098, "FY2023": 15040, "FY2022": 14987}),
    ("DATA", "Deferred tax asset", {"FY2024": 27, "FY2023": 496, "FY2022": 989}),
    ("DATA", "Other assets", {
        "FY2026": 3358, "FY2025": 1237, "FY2024": 4519, "FY2023": 3849, "FY2022": 3672}),
    ("DATA", "Prepayments and accrued income", {
        "FY2026": 7880, "FY2025": 9064, "FY2024": 21268, "FY2023": 17071, "FY2022": 13145}),
    ("DATA", "Post retirement benefit asset", {"FY2023": 3859, "FY2022": 9831}),
    ("TOTAL", "Total assets", {
        "FY2026": 7567981, "FY2025": 7158840, "FY2024": 6801461, "FY2023": 6852939, "FY2022": 7274665}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {
        "FY2026": 309283, "FY2025": 99590, "FY2024": 109543, "FY2023": 122958, "FY2022": 119572}),
    ("DATA", "Customer accounts", {
        "FY2026": 6555269, "FY2025": 6427375, "FY2024": 6096719, "FY2023": 6214358, "FY2022": 6689431}),
    ("DATA", "Derivative financial instruments (liabilities)", {
        "FY2026": 668, "FY2025": 712, "FY2024": 6764, "FY2023": 3158, "FY2022": 4629}),
    ("DATA", "Deferred tax liability", {
        "FY2026": 14802, "FY2025": 11555, "FY2024": 11331, "FY2023": 12342, "FY2022": 15548}),
    ("DATA", "Other liabilities", {
        "FY2026": 5457, "FY2025": 29582, "FY2024": 4901, "FY2023": 3072, "FY2022": 2485}),
    ("DATA", "Accruals and deferred income", {
        "FY2026": 77819, "FY2025": 31795, "FY2024": 60428, "FY2023": 39719, "FY2022": 24557}),
    ("DATA", "Post retirement benefit liability", {"FY2024": 107}),
    ("DATA", "Provision for other liabilities", {"FY2022": 2750}),
    ("TOTAL", "Total liabilities", {
        "FY2026": 6963298, "FY2025": 6600609, "FY2024": 6289793, "FY2023": 6395607, "FY2022": 6858972}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {
        "FY2026": 120, "FY2025": 120, "FY2024": 120, "FY2023": 120, "FY2022": 120}),
    ("DATA", "Reserve fund", {
        "FY2026": 22598, "FY2025": 22598, "FY2024": 22598, "FY2023": 22598, "FY2022": 22598}),
    ("DATA", "Revaluation reserves", {
        "FY2026": 30893, "FY2025": 31518, "FY2024": 31526, "FY2023": 32004, "FY2022": 35878}),
    ("DATA", "Retained earnings", {
        "FY2026": 551072, "FY2025": 503995, "FY2024": 457424, "FY2023": 402610, "FY2022": 357097}),
    ("TOTAL", "Total equity", {
        "FY2026": 604683, "FY2025": 558231, "FY2024": 511668, "FY2023": 457332, "FY2022": 415693}),
    ("TOTAL", "Total liabilities and equity", {
        "FY2026": 7567981, "FY2025": 7158840, "FY2024": 6801461, "FY2023": 6852939, "FY2022": 7274665}),
]

# FY2019-21 are transcribed from each year's own published Group balance
# sheet (rather than later comparative/restated columns).  Where the older
# face statement used a combined tangible/software line, it stays in
# Property and equipment and Intangible assets remains blank.
_HISTORICAL_BALANCE_SHEET = {
    "Cash and balances at central banks": (1709735, 1161138, 1525359),
    "Items in course of collection from banks": (303, 12, 1074),
    "Derivative financial instruments (assets)": (29394, 31, 2105),
    "Total financial assets": (4159605, 3956424, 3227198),
    "Financial assets at fair value through profit or loss": (141084, 6038, 5104),
    "Investment in equity shares (financial assets at cost less impairment)": (1528, 1528, 1528),
    "Loans and advances to banks, at amortised cost": (326999, 384872, 217116),
    "Loans and advances to customers, net of impairment, at amortised cost": (1857015, 1805994, 1698366),
    "Bank and building society certificates of deposit (financial assets at amortised cost)": (180403, 617362, 519344),
    "Debt securities at amortised cost": (1652576, 1140630, 785740),
    "Intangible assets": (16067, None, None),
    "Property and equipment": (57697, 82849, 83668),
    "Heritage assets": (9477, 9473, 9438),
    "Deferred tax asset": (1677, 1016, 856),
    "Other assets": (3266, 3591, 343),
    "Prepayments and accrued income": (13045, 9121, 12469),
    "Post retirement benefit asset": (3950, 8482, 579),
    "Total assets": (6004216, 5232137, 4863089),
    "Deposits by banks": (0, 466, 60),
    "Customer accounts": (5544294, 4761856, 4364933),
    "Derivative financial instruments (liabilities)": (21787, 37128, 80184),
    "Deferred tax liability": (10725, 8629, 9425),
    "Other liabilities": (3318, 845, 2990),
    "Accruals and deferred income": (21547, 24946, 30738),
    "Provision for other liabilities": (4813, 4546, 3370),
    "Total liabilities": (5606484, 4838416, 4491700),
    "Called up share capital": (120, 120, 120),
    "Reserve fund": (22598, 22598, 22598),
    "Revaluation reserves": (34784, 37531, 40740),
    "Retained earnings": (340230, 333472, 307931),
    "Total equity": (397732, 393721, 371389),
    "Total liabilities and equity": (6004216, 5232137, 4863089),
}
for _kind, _label, _values in balance_sheet_rows:
    if _label in _HISTORICAL_BALANCE_SHEET:
        for _year, _value in zip(("FY2021", "FY2020", "FY2019"), _HISTORICAL_BALANCE_SHEET[_label]):
            if _value is not None:
                _values[_year] = _value

bw.add_balance_sheet_sheet(
    title="C. Hoare & Co. — Consolidated and Company Balance Sheets",
    subtitle="Group column, £'000. See source note at bottom.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + PRESENTATION_NOTE,
    first_col_width=68,
    source_height=380,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable", {
        "FY2026": 362505, "FY2025": 397149, "FY2024": 368204, "FY2023": 217811, "FY2022": 94938}),
    ("DATA", "Interest payable", {
        "FY2026": -152001, "FY2025": -182502, "FY2024": -153516, "FY2023": -40520, "FY2022": -6681}),
    ("TOTAL", "Net interest income", {
        "FY2026": 210504, "FY2025": 214647, "FY2024": 214688, "FY2023": 177291, "FY2022": 88257}),
    ("DATA", "Dividend income", {
        "FY2026": 7708, "FY2025": 9621, "FY2024": 24831, "FY2023": 11150, "FY2022": 3587}),
    ("DATA", "Other finance income", {"FY2025": 1, "FY2024": 413, "FY2023": 275, "FY2022": 79}),
    ("DATA", "Fees and commissions receivable", {
        "FY2026": 15571, "FY2025": 10858, "FY2024": 15018, "FY2023": 16534, "FY2022": 15662}),
    ("DATA", "Fees and commissions payable", {
        "FY2026": -1350, "FY2025": -1227, "FY2024": -1338, "FY2023": -1251, "FY2022": -1274}),
    ("TOTAL", "Net fees and commissions income", {
        "FY2026": 14221, "FY2025": 9631, "FY2024": 13680, "FY2023": 15283, "FY2022": 14388}),
    ("DATA", "Dealing profits", {
        "FY2026": 9461, "FY2025": 8778, "FY2024": 8551, "FY2023": 16696, "FY2022": 7542}),
    ("DATA", "Other operating income/(expense)", {
        "FY2026": 12733, "FY2025": 6723, "FY2024": 9533, "FY2023": -10227, "FY2022": -5041}),
    ("TOTAL", "Total income", {
        "FY2026": 254627, "FY2025": 249401, "FY2024": 271696, "FY2023": 210468, "FY2022": 108812}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Administrative expenses including staff costs", {
        "FY2026": -179587, "FY2025": -172087, "FY2024": -176381, "FY2023": -125030, "FY2022": -79937}),
    ("DATA", "Amortisation", {
        "FY2026": -8685, "FY2025": -8608, "FY2024": -8385, "FY2023": -9483, "FY2022": -9099}),
    ("DATA", "Depreciation", {
        "FY2026": -2891, "FY2025": -2750, "FY2024": -2435, "FY2023": -2053, "FY2022": -1717}),
    ("TOTAL", "Total operating expenses", {
        "FY2026": -191163, "FY2025": -183445, "FY2024": -187201, "FY2023": -136566, "FY2022": -90753}),
    ("DATA", "Impairment charge on loans and advances", {
        "FY2026": -1278, "FY2025": -2222, "FY2024": -3659, "FY2023": -6213, "FY2022": -1522}),
    ("TOTAL", "Profit before taxation", {
        "FY2026": 62186, "FY2025": 63734, "FY2024": 80836, "FY2023": 67689, "FY2022": 16537}),
    ("DATA", "Tax on profit", {
        "FY2026": -15103, "FY2025": -16958, "FY2024": -15437, "FY2023": -17485, "FY2022": -3794}),
    ("TOTAL", "Profit for the financial year", {
        "FY2026": 47083, "FY2025": 46776, "FY2024": 65399, "FY2023": 50204, "FY2022": 12743}),
    ("SECTION", "Other comprehensive income/(expense)", {}),
    ("DATA", "Remeasurement of retirement benefit obligations", {
        "FY2025": -172, "FY2024": -11570, "FY2023": -6247, "FY2022": 5802}),
    ("DATA", "Deferred tax arising on pension scheme", {
        "FY2025": -27, "FY2024": 991, "FY2023": 1562, "FY2022": -1672}),
    ("DATA", "Revaluation gain/(loss) of property and heritage assets", {
        "FY2026": -833, "FY2025": -11, "FY2024": -638, "FY2023": -5165, "FY2022": 4895}),
    ("DATA", "Deferred tax on valuation gain/(loss)", {
        "FY2026": 208, "FY2025": 3, "FY2024": 160, "FY2023": 1291, "FY2022": -3801}),
    ("TOTAL", "Other comprehensive income/(expense), net of tax", {
        "FY2026": -625, "FY2025": -207, "FY2024": -11057, "FY2023": -8559, "FY2022": 5224}),
    ("TOTAL", "Total comprehensive income for the year", {
        "FY2026": 46458, "FY2025": 46569, "FY2024": 54342, "FY2023": 41645, "FY2022": 17967}),
]

_HISTORICAL_INCOME_STATEMENT = {
    "Interest receivable": (89772, 113495, 103740),
    "Interest payable": (-9131, -11492, -8705),
    "Net interest income": (80641, 102003, 95035),
    "Dividend income": (-2, 14, 19),
    "Other finance income": (256, 20, 268),
    "Fees and commissions receivable": (12490, 12991, 14665),
    "Fees and commissions payable": (-1864, -2421, -1284),
    "Net fees and commissions income": (10626, 10570, 13381),
    "Dealing profits": (6264, 10890, 12878),
    "Other operating income/(expense)": (4821, 477, 1925),
    "Total income": (102606, 123974, 123506),
    "Administrative expenses including staff costs": (-76184, -78033, -76529),
    "Amortisation": (-7626, None, None),
    "Depreciation": (-1964, -8795, -7018),
    "Total operating expenses": (-85774, -86828, -83547),
    "Impairment charge on loans and advances": (-730, -15434, -7544),
    "Profit before taxation": (16102, 21712, 32473),
    "Tax on profit": (-3848, -4053, -6713),
    "Profit for the financial year": (12254, 17659, 25760),
    "Remeasurement of retirement benefit obligations": (-6526, 9502, -9867),
    "Deferred tax arising on pension scheme": (1036, -1614, 1677),
    "Revaluation gain/(loss) of property and heritage assets": (-2275, -3866, 1648),
    "Deferred tax on valuation gain/(loss)": (-472, 657, -280),
    "Other comprehensive income/(expense), net of tax": (-8237, 4679, -6822),
    "Total comprehensive income for the year": (4017, 22338, 18938),
}
for _kind, _label, _values in income_statement_rows:
    if _label in _HISTORICAL_INCOME_STATEMENT:
        for _year, _value in zip(("FY2021", "FY2020", "FY2019"), _HISTORICAL_INCOME_STATEMENT[_label]):
            if _value is not None:
                _values[_year] = _value

bw.add_income_statement_sheet(
    title="C. Hoare & Co. — Consolidated Statement of Comprehensive Income",
    subtitle="Group column, £'000. See source note at bottom.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + PRESENTATION_NOTE,
    first_col_width=68,
    source_height=380,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity (chronological). All 5 movement years
# tie exactly to source (each year's own Profit + OCI split across the
# Revaluation reserves and Retained earnings columns, per the Bank's own
# presentation) - verified against every consecutive opening/closing pair.
# ---------------------------------------------------------------
equity_changes_rows = [
    ("TOTAL", "Balance as at 1 April 2018", (120, 22598, 43122, 286617, 352457)),
    ("DATA", "Profit for the year (FY2019)", (None, None, None, 25760, 25760)),
    ("DATA", "Other comprehensive expense, net of tax (FY2019)", (None, None, -2382, -4440, -6822)),
    ("DATA", "Dividends (FY2019)", (None, None, None, -6, -6)),
    ("TOTAL", "Balance as at 31 March 2019", (120, 22598, 40740, 307931, 371389)),
    ("DATA", "Profit for the year (FY2020)", (None, None, None, 17659, 17659)),
    ("DATA", "Other comprehensive income, net of tax (FY2020)", (None, None, -3209, 25547, 22338)),
    ("DATA", "Dividends (FY2020)", (None, None, None, -6, -6)),
    ("TOTAL", "Balance as at 31 March 2020", (120, 22598, 37531, 333472, 393721)),
    ("DATA", "Profit for the year (FY2021)", (None, None, None, 12254, 12254)),
    ("DATA", "Other comprehensive expense, net of tax (FY2021)", (None, None, -2747, -548, -3295)),
    ("DATA", "Dividends (FY2021)", (None, None, None, -6, -6)),
    ("TOTAL", "Balance as at 31 March 2021", (120, 22598, 34784, 340230, 397732)),
    ("TOTAL", "Balance as at 1 April 2021", (120, 22598, 34784, 340230, 397732)),
    ("DATA", "Profit for the year (FY2022)", (None, None, None, 12743, 12743)),
    ("DATA", "Other comprehensive income, net of tax (FY2022)", (None, None, 1094, 4130, 5224)),
    ("DATA", "Dividends (FY2022)", (None, None, None, -6, -6)),
    ("TOTAL", "Balance as at 31 March 2022", (120, 22598, 35878, 357097, 415693)),
    ("DATA", "Profit for the year (FY2023)", (None, None, None, 50204, 50204)),
    ("DATA", "Other comprehensive expense, net of tax (FY2023)", (None, None, -3874, -4685, -8559)),
    ("DATA", "Dividends (FY2023)", (None, None, None, -6, -6)),
    ("TOTAL", "Balance as at 31 March 2023", (120, 22598, 32004, 402610, 457332)),
    ("DATA", "Profit for the year (FY2024)", (None, None, None, 65399, 65399)),
    ("DATA", "Other comprehensive expense, net of tax (FY2024)", (None, None, -478, -10579, -11057)),
    ("DATA", "Dividends (FY2024)", (None, None, None, -6, -6)),
    ("TOTAL", "Balance as at 31 March 2024", (120, 22598, 31526, 457424, 511668)),
    ("DATA", "Profit for the year (FY2025)", (None, None, None, 46776, 46776)),
    ("DATA", "Other comprehensive expense, net of tax (FY2025)", (None, None, -8, -199, -207)),
    ("DATA", "Dividends (FY2025)", (None, None, None, -6, -6)),
    ("TOTAL", "Balance as at 31 March 2025", (120, 22598, 31518, 503995, 558231)),
    ("DATA", "Profit for the year (FY2026)", (None, None, None, 47083, 47083)),
    ("DATA", "Other comprehensive expense, net of tax (FY2026)", (None, None, -625, 0, -625)),
    ("DATA", "Dividends (FY2026)", (None, None, None, -6, -6)),
    ("TOTAL", "Balance as at 31 March 2026", (120, 22598, 30893, 551072, 604683)),
]

bw.add_equity_changes_sheet(
    title="C. Hoare & Co. — Consolidated Statement of Changes in Equity",
    subtitle="Group column, £'000. Chronological roll-forward, oldest to newest.",
    headers=["Called up Share Capital", "Reserve Fund", "Revaluation Reserves", "Retained Earnings", "Total Equity"],
    rows=equity_changes_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + PRESENTATION_NOTE,
    first_col_width=56,
    source_height=380,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Net cash from/(used in) operating activities (before tax)", {
        "FY2026": 87472, "FY2025": 333415, "FY2024": -94951, "FY2023": -418678, "FY2022": 1121381}),
    ("DATA", "Taxation paid", {
        "FY2026": -12154, "FY2025": -11881, "FY2024": -15618, "FY2023": -17355, "FY2022": -4932}),
    ("TOTAL", "Net cash from/(used in) operating activities", {
        "FY2026": 75318, "FY2025": 321534, "FY2024": -110569, "FY2023": -436033, "FY2022": 1116449}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of investment securities", {
        "FY2026": -1648567, "FY2025": -779143, "FY2024": -1648464, "FY2023": -1562892, "FY2022": -3121342}),
    ("DATA", "Sale and maturity of investment securities", {
        "FY2026": 1064233, "FY2025": 684225, "FY2024": 1614146, "FY2023": 1640306, "FY2022": 2122564}),
    ("DATA", "Purchase of bulk annuity policy", {"FY2025": -278, "FY2024": -7191}),
    ("DATA", "Purchase of intangible assets", {
        "FY2026": -16598, "FY2025": -23130, "FY2024": -9220, "FY2023": -8427, "FY2022": -10853}),
    ("DATA", "Purchase of tangible fixed assets", {
        "FY2026": -5725, "FY2025": -6425, "FY2024": -2671, "FY2023": -4318, "FY2022": -350}),
    ("DATA", "Purchase of heritage assets", {"FY2026": -192, "FY2025": -9, "FY2024": -58, "FY2023": -53}),
    ("DATA", "Proceeds from sale of subsidiary", {"FY2025": 745}),
    ("DATA", "Proceeds from disposals of tangible assets", {"FY2021": 1, "FY2020": 2}),
    ("TOTAL", "Net cash from/(used in) investing activities", {
        "FY2026": -606849, "FY2025": -124015, "FY2024": -53458, "FY2023": 64616, "FY2022": -1009981}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividend paid", {"FY2026": -6, "FY2025": -6, "FY2024": -6, "FY2023": -6, "FY2022": -6}),
    ("TOTAL", "Net cash from/(used in) financing activities", {
        "FY2026": -6, "FY2025": -6, "FY2024": -6, "FY2023": -6, "FY2022": -6}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {
        "FY2026": -531537, "FY2025": 197513, "FY2024": -164034, "FY2023": -371423, "FY2022": 106462}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {
        "FY2026": 1580850, "FY2025": 1382976, "FY2024": 1547010, "FY2023": 1918433, "FY2022": 1811971}),
    ("DATA", "Effect of exchange rate changes", {"FY2026": -12, "FY2025": 361}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {
        "FY2026": 1049301, "FY2025": 1580850, "FY2024": 1382976, "FY2023": 1547010, "FY2022": 1918433}),
    ("SECTION", "Cash and cash equivalents comprise", {}),
    ("DATA", "Cash at bank and in hand", {
        "FY2026": 896317, "FY2025": 1548443, "FY2024": 1345322, "FY2023": 1452949, "FY2022": 1843378}),
    ("DATA", "Short term deposits", {
        "FY2026": 152984, "FY2025": 32407, "FY2024": 37654, "FY2023": 94061, "FY2022": 75055}),
    ("TOTAL", "Cash and cash equivalents", {
        "FY2026": 1049301, "FY2025": 1580850, "FY2024": 1382976, "FY2023": 1547010, "FY2022": 1918433}),
]

_HISTORICAL_CASH_FLOW = {
    "Net cash from/(used in) operating activities (before tax)": (830193, 154741, 465462),
    "Taxation paid": (-3329, -7851, -7243),
    "Net cash from/(used in) operating activities": (826864, 146890, 458219),
    "Purchase of investment securities": (-1647128, -2318017, -2292637),
    "Sale and maturity of investment securities": (1407391, 1815052, 2194962),
    "Purchase of intangible assets": (-1981, None, None),
    "Purchase of tangible fixed assets": (-1316, -12902, -9451),
    "Proceeds from disposals of tangible assets": (1, 2, None),
    "Net cash from/(used in) investing activities": (-243033, -515865, -107126),
    "Dividend paid": (-6, -6, -6),
    "Net cash from/(used in) financing activities": (-6, -6, -6),
    "Net (decrease)/increase in cash and cash equivalents": (583825, -368981, 351087),
    "Cash and cash equivalents at the beginning of the year": (1228146, 1597127, 1246040),
    "Cash and cash equivalents at the end of the year": (1811971, 1228146, 1597127),
    "Cash at bank and in hand": (1709735, 1161138, 1525359),
    "Short term deposits": (102236, 67008, 71768),
    "Cash and cash equivalents": (1811971, 1228146, 1597127),
}
for _kind, _label, _values in rows:
    if _label in _HISTORICAL_CASH_FLOW:
        for _year, _value in zip(("FY2021", "FY2020", "FY2019"), _HISTORICAL_CASH_FLOW[_label]):
            if _value is not None:
                _values[_year] = _value

bw.add_cash_flow_sheet(
    title="C. Hoare & Co. — Consolidated Cash Flow Statement",
    subtitle="Consolidated Group basis, £'000. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Asset Quality: FRS 102 basis (not IFRS 9) - confirmed by reading the
# Bank's own Note 14 "Allowance for Impairment Losses" (specific/
# collective allowance roll-forward, no Stage 1/2/3 split anywhere in any
# of the 5 reports checked) - loans and advances to customers only.
# ---------------------------------------------------------------
AQ_GROSS = {"FY2026": 2592710, "FY2025": 2286817, "FY2024": 2130465, "FY2023": 1989288, "FY2022": 2024798, "FY2021": 1886062, "FY2020": 1859678, "FY2019": 1709977}
AQ_SPECIFIC = {"FY2026": 8378, "FY2025": 7537, "FY2024": 9003, "FY2023": 17003, "FY2022": 25575, "FY2021": 24724, "FY2020": 22682, "FY2019": 8474}
AQ_COLLECTIVE = {"FY2026": 5304, "FY2025": 4878, "FY2024": 4878, "FY2023": 5313, "FY2022": 4403, "FY2021": 4323, "FY2020": 4160, "FY2019": 3137}
AQ_TOTAL_ALLOWANCE = {y: AQ_SPECIFIC[y] + AQ_COLLECTIVE[y] for y in YEARS}
AQ_NET = {y: AQ_GROSS[y] - AQ_TOTAL_ALLOWANCE[y] for y in YEARS}
AQ_COVERAGE = {y: f"{AQ_TOTAL_ALLOWANCE[y] / AQ_GROSS[y] * 100:.2f}%" for y in YEARS}

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers (gross)", {}),
    ("DATA", "Total gross loans and advances to customers", AQ_GROSS),
    ("SECTION", "Allowance for impairment losses", {}),
    ("DATA", "Specific allowance for impairment", {y: -v for y, v in AQ_SPECIFIC.items()}),
    ("DATA", "Collective allowance for impairment", {y: -v for y, v in AQ_COLLECTIVE.items()}),
    ("TOTAL", "Total allowance for impairment", {y: -v for y, v in AQ_TOTAL_ALLOWANCE.items()}),
    ("TOTAL", "Net loans and advances to customers", AQ_NET),
    ("SECTION", "Ratios", {}),
    ("DATA", "Overall coverage ratio (total allowance / gross loans)", AQ_COVERAGE),
]

bw.add_asset_quality_sheet(
    title="C. Hoare & Co. — Asset Quality / Credit Risk Disclosures",
    subtitle="Loans and advances to customers, £'000. FRS 102 basis (specific/collective allowance), Group & Company.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - C. Hoare & Co.'s own Note 13(b) 'Loans and advances to customers' and Note 14 'Allowance for "
        "Impairment Losses' (Group & Company, no separate Group-only figures disclosed), each from that year's "
        "own originally-published Financial Report:\n"
        f"FY2026: Financial Report 2026, p.73 - {AR2026_URL}\n"
        f"FY2025: Financial Report 2025, pp.60-61 - {AR2025_URL}\n"
        f"FY2024: Financial Report 2024, pp.62-63 - {AR2024_URL}\n"
        f"FY2023: Financial Report 2023, pp.58-59 - {AR2023_URL}\n"
        f"FY2022: Annual Report 2022, p.58 - {AR2022_URL}\n\n"
        f"FY2021: Annual Report 2021, pp.62-63 - {AR2021_URL}\n"
        f"FY2020: Annual Report 2020, p.59 - {AR2020_URL}\n"
        f"FY2019: Financial Report 2019, pp.50-51 - {AR2019_URL}\n\n"
        "Note: C. Hoare & Co. reports under FRS 102, not IFRS 9 - there is no Stage 1/2/3 split anywhere in any "
        "of the 5 reports checked (confirmed by reading each year's impairment note in full), only a specific/"
        "collective allowance roll-forward. Coverage fell steadily from 1.48% (FY2022) to 0.53% (FY2026), driven "
        "by large specific-provision write-offs each year (e.g. £14.0m written off in FY2023 alone) outpacing new "
        "specific charges - flagged here, not smoothed. Figures are Group & Company (identical - the Bank's own "
        "note discloses no separate Group-only split for this line).\n\n" + ENTITY_NOTE
    ),
    first_col_width=62,
    source_height=340,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(PAGES), note=note, first_col_width=48, source_height=170)


OWN_YEAR_2024_NOTE = (
    "FY2024 EDITION vs FY2025 COMPARATIVE (both recorded, neither overwritten): the FY2024 edition's own "
    "Appendix 1 prints CET1/Tier 1 capital GBP483,236k and total capital GBP488,114k; the FY2025 edition's "
    "31-Mar-24 comparative column prints GBP483,235k and GBP488,113k for the same two lines - a GBP1k "
    "rounding difference between editions. The FY2024 column here uses the FY2024 edition's own "
    "originally-published figure, per this project's convention; the FY2025 comparative's GBP1k-lower "
    "figure is recorded in this note rather than silently discarded. Both editions agree exactly on that "
    "year's RWA (2,091,044) and on all three ratios (23.11%/23.11%/23.34%)."
)

metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", {
    "FY2026": 567436, "FY2025": 526455, "FY2024": 483236, "FY2023": 428543, "FY2022": 381989, "FY2021": 381441, "FY2020": 375716, "FY2019": 370810})],
    note=OWN_YEAR_2024_NOTE)

metric("CET1 Ratio", "%", [("Common Equity Tier 1 ratio", {
    "FY2026": "22.7%", "FY2025": "23.00%", "FY2024": "23.11%", "FY2023": "21.44%", "FY2022": "20.96%", "FY2021": "21.61%", "FY2020": "21.11%", "FY2019": "22.42%"})],
    note="FY2023 is shown as its OWN edition prints it (21.44%, on RWAs of 1,997,896). The FY2024 edition's "
         "31-Mar-23 comparative column prints 21.45% against an RWA of 1,977,896 - that RWA is a "
         "transposed-digit typo in the FY2024 edition itself, demonstrable from that same document: its own "
         "Table 6 (UK OV1, p.12) gives the FY2023 total as 1,997,896, and 428,543/1,977,896 would be 21.67%, "
         "not the 21.45% the comparative column prints, whereas 428,543/1,997,896 = 21.4497%. Flagged, not "
         "reconciled away.")

metric("Tier 1 Capital", "£'000 (= CET1 capital; no AT1 instruments)", [("Tier 1 capital", {
    "FY2026": 567436, "FY2025": 526455, "FY2024": 483236, "FY2023": 428543, "FY2022": 381989, "FY2021": 381441, "FY2020": 375716, "FY2019": 370810})],
    note=OWN_YEAR_2024_NOTE)

metric("Tier 1 Ratio", "%", [("Tier 1 ratio", {
    "FY2025": "23.00%", "FY2024": "23.11%", "FY2023": "21.44%", "FY2022": "20.96%", "FY2021": "21.61%", "FY2020": "21.11%", "FY2019": "22.42%"})],
    note="FY2019: the FY2019 edition's Appendix 1 row 62 prints the Tier 1 ratio as 22.42%, identical to "
         "CET1 - the bank held no AT1 instruments that year either (Appendix 1 rows 36/44 are nil).")

metric("Total Capital", "£'000", [("Total capital", {
    "FY2026": 572740, "FY2025": 531333, "FY2024": 488114, "FY2023": 433856, "FY2022": 386392, "FY2021": 385764, "FY2020": 379876, "FY2019": 373947})],
    note="FY2019 total capital of GBP373,947k is CET1 GBP370,810k plus GBP3,137k of Tier 2 capital, which "
         "that year consisted entirely of the collective impairment allowance (FY2019 edition, Table 3, "
         "p.19) - the same Tier 2 composition as every other year in this series.\n" + OWN_YEAR_2024_NOTE)

metric("Total Capital Ratio", "%", [("Total capital ratio", {
    "FY2026": "22.9%", "FY2025": "23.21%", "FY2024": "23.34%", "FY2023": "21.72%", "FY2022": "21.20%", "FY2021": "21.86%", "FY2020": "21.34%", "FY2019": "22.61%"})])

metric("Total RWAs", "£'000", [("Total risk-weighted exposure amount", {
    "FY2026": 2499834, "FY2025": 2289414, "FY2024": 2091044, "FY2023": 1997896, "FY2022": 1822244, "FY2021": 1764829, "FY2020": 1779927, "FY2019": 1653911})],
    note="TOTAL-RWA VALIDATION (all years re-checked 2026-09-16, including the newly-added FY2019): the "
         "figure on this sheet is the genuine total risk-weighted exposure amount, not a credit-risk "
         "subtotal. Confirmed by reproducing each year's own printed ratio from it - FY2019 370,810/"
         "1,653,911 = 22.42% and 373,947/1,653,911 = 22.61%, both matching the FY2019 edition's printed "
         "ratios exactly - and by confirming that the RWA Breakdown sheet's credit-risk, market-risk and "
         "operational-risk rows sum to this total in every year (FY2019: 1,457,860 + 1,443 + 194,608 = "
         "1,653,911).")

# ---------------------------------------------------------------
# RWA Breakdown (Pillar 3's UK OV1 template - Table 6/Table 5 "Risk
# weighted assets and Pillar 1 capital requirements by exposure class").
# No FY2026 OV1: the bank left the Pillar 3 regime entirely (SDDT approval,
# December 2025), and the Annual Report capital note that replaces it gives
# only a single RWA total with no exposure-class split.
# ---------------------------------------------------------------
RWA_SOURCES = (
    "Sources - C. Hoare & Co. Pillar 3 Disclosures, UK OV1 'Risk weighted assets and Pillar 1 capital "
    "requirements by exposure class' table, each year taken from ITS OWN year's edition (period read off "
    "each cover, never the filename):\n"
    f"FY2025: Pillar 3 Disclosures 2025, Table 6, p.10 - {P3_2025_URL}\n"
    f"FY2024: Pillar 3 Disclosures 2024, Table 6, p.12 - {P3_2024_URL}\n"
    f"FY2023: Pillar 3 Disclosures 2023, Table 5, p.14 - {P3_2023_URL}\n"
    f"FY2022: Pillar 3 Disclosures 2022, Table 5, p.14 - {P3_2022_URL}\n"
    f"FY2021/FY2020: Pillar 3 Disclosures 2021, Table 5, p.14 - {P3_2021_URL}\n"
    f"FY2019: Pillar 3 Disclosures 2019, Table 5 'Risk weighted assets and Pillar 1 capital requirements "
    f"by exposure class', p.21 - {P3_2019_URL} (see the Pillar 3 metric sheets' source note for why this "
    "is an Internet Archive citation and what the dead original URL was).\n"
    "FY2019 EXPOSURE-CLASS COVERAGE: the FY2019 table carries no 'Claims in the form of Collective "
    "Investment Undertakings (CIU)' row and no 'Securitisations' row at all - those two exposure classes "
    "first appear in this bank's OV1 in later editions - so those cells are blank for FY2019 because the "
    "class does not exist in the source, not because the value is unknown. Its rows sum exactly: credit "
    "1,457,860 + market 1,443 + operational 194,608 = 1,653,911.\n"
    "EQUITY EXPOSURES ROW (added 2026-09-16 - this is a correction, not just an extension): the 'Equity "
    "exposures' exposure class was previously missing from this sheet entirely, with the consequence that "
    "the FY2021 and FY2020 credit-risk rows did not sum to their own printed 'Total credit risk'. The "
    "class is a genuine, separately-printed line in the bank's own OV1 every year: GBP10,583k (FY2021), "
    "GBP5,928k (FY2020) and GBP5,003k (FY2019), and an explicit dash/nil FY2022-FY2025. With the row "
    "restored, every year's credit-risk rows now sum exactly to that year's printed Total credit risk "
    "(FY2021 = 1,572,334; FY2020 = 1,584,434), verified arithmetically.\n"
    "RESTATED FY2021 COMPARATIVE NOT USED: the FY2022 edition reprints FY2021 in a column headed "
    "'restated' and changes some exposure-class allocations there (most visibly CIU 129,997 -> 140,580). "
    "This sheet keeps FY2021 as the FY2021 edition itself originally published it, per this project's "
    "convention of preserving each year's own as-reported figures; the restated variant is recorded here "
    "and not silently substituted.\n"
    "ROUNDING IN THE SOURCE (checked, not a transcription error): in FY2023, FY2024 and FY2025 the bank's "
    "own OV1 rows sum to GBP1k away from its own printed subtotal/total (e.g. FY2025 exposure classes sum "
    "to 1,894,850 against a printed Total credit risk of 1,894,851; FY2023 credit 1,767,060 + operational "
    "230,837 = 1,997,897 against a printed total of 1,997,896). Every figure is reproduced exactly as "
    "printed rather than being forced to add up. FY2019, FY2020, FY2021 and FY2022 tie exactly with no "
    "residual.\n"
    "FY2026: the bank no longer publishes Pillar 3 disclosures at all - its Financial Report 2026 (p.32) "
    "states it was approved under the PRA's Small Domestic Deposit Taking regime in December 2025 and 'no "
    "longer prepares Pillar III disclosures'. The FY2026 Annual Report capital note that supplies the FY2026 "
    "headline capital figures on the other Pillar 3 sheets gives a single Risk weighted assets total only, "
    "with no exposure-class split, so there is no FY2026 OV1 breakdown to transcribe. This is a permanent "
    "end to the series, not a late document.\n"
    + ENTITY_NOTE
)

rwa_breakdown_rows = [
    ("SECTION", "RWA by exposure class, £'000", {}),
    ("DATA", "Institutions", {"FY2025": 41830, "FY2024": 54239, "FY2023": 162882, "FY2022": 61655}),
    ("DATA", "Corporates", {"FY2025": 76500, "FY2024": 102248, "FY2023": 107319, "FY2022": 95307}),
    ("DATA", "Retail", {"FY2025": 23348, "FY2024": 26562, "FY2023": 26867, "FY2022": 23919}),
    ("DATA", "Secured by mortgages on immovable property", {
        "FY2025": 1090724, "FY2024": 968778, "FY2023": 952975, "FY2022": 880391}),
    ("DATA", "Exposures in default", {"FY2025": 31891, "FY2024": 26252, "FY2023": 31691, "FY2022": 61214}),
    ("DATA", "Items associated with particularly high risk", {
        "FY2025": 120576, "FY2024": 109542, "FY2023": 43564, "FY2022": 45923}),
    ("DATA", "Covered bonds", {"FY2025": 158663, "FY2024": 154784, "FY2023": 159974, "FY2022": 132987}),
    ("DATA", "Claims on institutions/corporates with short-term credit assessment", {
        "FY2023": 0, "FY2022": 45485}),
    ("DATA", "Claims in the form of Collective Investment Undertakings (CIU)", {
        "FY2025": 177450, "FY2024": 148636, "FY2023": 146236, "FY2022": 165017}),
    ("DATA", "Equity exposures", {
        "FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0}),
    ("DATA", "Other items", {"FY2025": 99101, "FY2024": 115345, "FY2023": 96342, "FY2022": 89211}),
    ("DATA", "Securitisations", {"FY2025": 74767, "FY2024": 65116, "FY2023": 39209, "FY2022": 36844}),
    ("TOTAL", "Total credit risk", {
        "FY2025": 1894851, "FY2024": 1771501, "FY2023": 1767060, "FY2022": 1637953}),
    ("DATA", "Total market risk (FX PRR)", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0}),
    ("DATA", "Total operational risk", {
        "FY2025": 394563, "FY2024": 319543, "FY2023": 230837, "FY2022": 184291}),
    ("TOTAL", "Total Pillar 1 capital requirement (Total RWAs)", {
        "FY2025": 2289414, "FY2024": 2091044, "FY2023": 1997896, "FY2022": 1822244}),
]

# (FY2021, FY2020, FY2019).  None means that year's own OV1 table carries no
# such exposure class at all - CIU and Securitisations only enter this bank's
# OV1 after FY2019 - so the cell is left blank rather than written as a zero.
_HISTORICAL_RWA = {
    "Institutions": (66031, 148148, 124623), "Corporates": (139936, 76760, 86579),
    "Retail": (22667, 20936, 23677), "Secured by mortgages on immovable property": (749416, 802993, 772077),
    "Exposures in default": (114437, 103721, 47866),
    "Items associated with particularly high risk": (50392, 126877, 188138),
    "Covered bonds": (96282, 96428, 41581),
    "Claims on institutions/corporates with short-term credit assessment": (70016, 100307, 65941),
    "Claims in the form of Collective Investment Undertakings (CIU)": (129997, 0, None),
    "Equity exposures": (10583, 5928, 5003),
    "Other items": (91239, 93629, 102375), "Securitisations": (31338, 8707, None),
    "Total credit risk": (1572334, 1584434, 1457860), "Total market risk (FX PRR)": (0, 350, 1443),
    "Total operational risk": (192495, 195143, 194608),
    "Total Pillar 1 capital requirement (Total RWAs)": (1764829, 1779927, 1653911),
}
for _kind, _label, _values in rwa_breakdown_rows:
    if _label in _HISTORICAL_RWA:
        for _year, _value in zip(("FY2021", "FY2020", "FY2019"), _HISTORICAL_RWA[_label]):
            if _value is not None:
                _values[_year] = _value

bw.add_rwa_breakdown_sheet(
    title="C. Hoare & Co. — RWA Breakdown",
    subtitle="UK OV1 exposure-class split, £'000. No FY2026: bank left the Pillar 3 regime (SDDT, Dec 2025).",
    rows=rwa_breakdown_rows,
    sources_text=RWA_SOURCES,
    first_col_width=64,
    source_height=280,
)

metric("Leverage Ratio", "%, TWO BASES - see rows and note", [
    ("Leverage ratio excluding claims on central banks (UK KM1 row 14, FY2022 onward)", {
        "FY2025": "9.29%", "FY2024": "7.61%", "FY2023": "6.96%", "FY2022": "6.61%"}),
    ("Total exposure measure excluding claims on central banks (£'000)", {
        "FY2025": 5668227, "FY2024": 5517665, "FY2023": 5497608, "FY2022": 5526723}),
    ("Leverage ratio INCLUDING claims on central banks (CRD IV Table 6b basis, FY2021 and earlier)", {
        "FY2021": "6.32%", "FY2020": "7.18%", "FY2019": "7.55%"}),
    ("Total leverage ratio exposure including claims on central banks (£'000)", {
        "FY2021": 6031619, "FY2020": 5235408, "FY2019": 4910489}),
    ("FY2021 restated onto the excluding-central-bank-claims basis (FY2022 edition comparative only)", {
        "FY2021": "8.72%"}),
    ("FY2021 restated total exposure measure excluding claims on central banks (£'000)", {
        "FY2021": 4375666}),
],
    note="BASIS BREAK - CORRECTED 2026-09-16. This sheet previously carried FY2021 (6.32%) and FY2020 "
         "(7.18%) on a row captioned 'excluding claims on central banks', with a note asserting there was "
         "no mid-series methodology break at this bank. Both were wrong, and the primary documents say so "
         "plainly. The FY2021 edition's Table 6b 'Leverage ratio common disclosure' computes the ratio on "
         "a total leverage ratio exposure of GBP6,031,619k (FY2021) and GBP5,235,408k (FY2020) whose "
         "line 1 is the bank's FULL on-balance-sheet total - central bank claims included; the newly "
         "recovered FY2019 edition does the same on GBP4,910,489k. The UK excluded claims on central "
         "banks from the exposure measure from 1 January 2022, and the FY2022 edition's UK KM1 row 13/14 "
         "is the first on the new basis. The two bases are therefore kept on separate rows and are NOT to "
         "be merged or charted as one series: the FY2021->FY2022 step is a definitional change, not a "
         "deleveraging.\n"
         "RESTATED FY2021: the FY2022 edition reprints FY2021 on the NEW basis in its comparative column - "
         "8.72% on an exposure measure of GBP4,375,665,802 (shown above in GBP'000 as 4,375,666). That is "
         "the same year measured two ways, 6.32% and 8.72%; both are printed by the bank and both are "
         "recorded here on their own labelled rows, neither overwriting the other.\n"
         "FY2019 ROUNDING: the FY2019 edition prints its leverage ratio three times at three precisions - "
         "7.55% in the summary risk-measures table (p.4), 7.6% in the section 7.3 narrative (p.22) and "
         "7.5% in Table 6b row 22 (p.23). These are not three different figures but three roundings of "
         "one: Tier 1 capital 370,810 / total leverage exposure 4,910,489 = 7.5514%. The 2dp form is used "
         "above to match the precision of the other years on this sheet; the document's own 1dp variants "
         "are recorded here rather than discarded.")

metric("LCR", "%, 12-month rolling average of month-end positions", [
    ("Liquidity coverage ratio", {
        "FY2025": "341%", "FY2024": "308%", "FY2023": "273%", "FY2022": "272%", "FY2021": "357%"}),
    ("Total high-quality liquid assets (HQLA), weighted value, 12-month average (£'000)", {
        "FY2025": 3800472, "FY2024": 3587504, "FY2023": 3837797, "FY2022": 4066151, "FY2021": 3199721}),
    ("Total net cash outflows, adjusted value (£'000)", {
        "FY2025": 1118849, "FY2024": 1167925, "FY2023": 1410045, "FY2022": 1495945, "FY2021": 896247}),
],
    note="Basis is the bank's own stated one, identical in every edition that prints it: 'Liquidity "
         "measures are based on a 12-month rolling average of month end positions'. No point-in-time LCR "
         "has been mixed in.\n"
         "FY2021 (added 2026-09-16) comes from the FY2022 edition's 31-Mar-21 comparative column, which is "
         "the only place this bank ever printed a numeric FY2021 LCR - the FY2021 edition itself carries "
         "no KM1 template and only the qualitative statement that 'The bank's LCR was above regulatory "
         "requirements throughout the year'. It is on the same 12-month-average basis as the rest of the "
         "row.\n"
         "FY2020 AND FY2019: genuinely never published as a number. The FY2021 edition prints no FY2020 "
         "LCR comparative, and the FY2019 edition's section 11 says only that 'The bank exceeds its "
         "regulatory requirements for the LCR ratio' with no template and no figure. Blank, not estimated."
         "\nFY2026: the bank left the Pillar 3 regime entirely (SDDT approval, December 2025) and the "
         "Annual Report capital note that replaces it carries no liquidity metrics at all.")

metric("NSFR", "%, 4-quarter rolling average of quarter-end positions", [
    ("NSFR ratio", {"FY2025": "250%", "FY2024": "246%", "FY2023": "256%", "FY2022": "269%"}),
    ("Total available stable funding (£'000)", {
        "FY2025": 5331412, "FY2024": 4999224, "FY2023": 5346941, "FY2022": 5241977}),
    ("Total required stable funding (£'000)", {
        "FY2025": 2133068, "FY2024": 2029170, "FY2023": 2085219, "FY2022": 1950439}),
],
    note="Basis is the bank's own stated one: 'Net Stable Funding Ratio measure are based on a 4-quarter "
         "rolling average of quarter end positions'.\n"
         "FY2021 NSFR IS AN ENUMERATED ABSENCE, and deliberately differs from the LCR row above. The "
         "FY2022 edition's KM1 prints a 31-Mar-21 comparative for the LCR block (rows 15-17) but leaves "
         "the NSFR block (rows 18-20) blank in that column - so unlike the LCR, no restated FY2021 NSFR "
         "exists to recover. FY2020 and FY2019 likewise carry no numeric NSFR in any edition. Left blank "
         "rather than inferred from the LCR or from the following year.")

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources(PAGES),
    per_note={"MREL Ratio": "Not found in either Pillar 3 document reviewed (2025 or 2023 edition) - no MREL "
                             "row exists in this bank's Own Funds Disclosure template at all, and no separate "
                             "qualitative statement was found either."},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {
            "FY2026": 7567981, "FY2025": 7158840, "FY2024": 6801461, "FY2023": 6852939, "FY2022": 7274665, "FY2021": 6004216, "FY2020": 5232137, "FY2019": 4863089}),
        ("Financial assets", {
            "FY2026": 6339519, "FY2025": 5399523, "FY2024": 5229721, "FY2023": 5164686, "FY2022": 5204233, "FY2021": 4159605, "FY2020": 3956424, "FY2019": 3227198}),
        ("Customer accounts", {
            "FY2026": 6555269, "FY2025": 6427375, "FY2024": 6096719, "FY2023": 6214358, "FY2022": 6689431, "FY2021": 5544294, "FY2020": 4761856, "FY2019": 4364933}),
        ("Total equity", {
            "FY2026": 604683, "FY2025": 558231, "FY2024": 511668, "FY2023": 457332, "FY2022": 415693, "FY2021": 397732, "FY2020": 393721, "FY2019": 371389}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total income", {
            "FY2026": 254627, "FY2025": 249401, "FY2024": 271696, "FY2023": 210468, "FY2022": 108812, "FY2021": 102606, "FY2020": 123974, "FY2019": 123506}),
        ("Total operating expenses", {
            "FY2026": -191163, "FY2025": -183445, "FY2024": -187201, "FY2023": -136566, "FY2022": -90753, "FY2021": -85774, "FY2020": -86828, "FY2019": -83547}),
        ("Profit for the financial year", {
            "FY2026": 47083, "FY2025": 46776, "FY2024": 65399, "FY2023": 50204, "FY2022": 12743, "FY2021": 12254, "FY2020": 17659, "FY2019": 25760}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {
            "FY2026": 558231, "FY2025": 511668, "FY2024": 457332, "FY2023": 415693, "FY2022": 397732, "FY2021": 393721, "FY2020": 371389, "FY2019": 352457}),
        ("Total comprehensive income for the year", {
            "FY2026": 46458, "FY2025": 46569, "FY2024": 54342, "FY2023": 41645, "FY2022": 17967, "FY2021": 4017, "FY2020": 22338, "FY2019": 18938}),
        ("Dividends", {"FY2026": -6, "FY2025": -6, "FY2024": -6, "FY2023": -6, "FY2022": -6, "FY2021": -6, "FY2020": -6, "FY2019": -6}),
        ("Closing equity", {
            "FY2026": 604683, "FY2025": 558231, "FY2024": 511668, "FY2023": 457332, "FY2022": 415693, "FY2021": 397732, "FY2020": 393721, "FY2019": 371389}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {
            "FY2026": 75318, "FY2025": 321534, "FY2024": -110569, "FY2023": -436033, "FY2022": 1116449, "FY2021": 826864, "FY2020": 146890, "FY2019": 458219}),
        ("Net cash from/(used in) investing activities", {
            "FY2026": -606849, "FY2025": -124015, "FY2024": -53458, "FY2023": 64616, "FY2022": -1009981, "FY2021": -243033, "FY2020": -515865, "FY2019": -107126}),
        ("Net cash from/(used in) financing activities", {
            "FY2026": -6, "FY2025": -6, "FY2024": -6, "FY2023": -6, "FY2022": -6, "FY2021": -6, "FY2020": -6, "FY2019": -6}),
        ("Cash and cash equivalents at end of year", {
            "FY2026": 1049301, "FY2025": 1580850, "FY2024": 1382976, "FY2023": 1547010, "FY2022": 1918433, "FY2021": 1811971, "FY2020": 1228146, "FY2019": 1597127}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {
            "FY2026": "22.7%", "FY2025": "23.00%", "FY2024": "23.11%", "FY2023": "21.44%",
            "FY2022": "20.96%", "FY2021": "21.61%", "FY2020": "21.11%", "FY2019": "22.42%"}),
        ("Tier 1 Ratio", {
            "FY2025": "23.00%", "FY2024": "23.11%", "FY2023": "21.44%", "FY2022": "20.96%",
            "FY2021": "21.61%", "FY2020": "21.11%", "FY2019": "22.42%"}),
        ("Total Capital Ratio", {
            "FY2026": "22.9%", "FY2025": "23.21%", "FY2024": "23.34%", "FY2023": "21.72%",
            "FY2022": "21.20%", "FY2021": "21.86%", "FY2020": "21.34%", "FY2019": "22.61%"}),
        ("Leverage Ratio (excl. central bank claims, FY2022 onward)", {
            "FY2025": "9.29%", "FY2024": "7.61%", "FY2023": "6.96%", "FY2022": "6.61%"}),
        ("Leverage Ratio (incl. central bank claims, pre-2022 basis)", {
            "FY2021": "6.32%", "FY2020": "7.18%", "FY2019": "7.55%"}),
        ("LCR", {"FY2025": "341%", "FY2024": "308%", "FY2023": "273%", "FY2022": "272%", "FY2021": "357%"}),
        ("NSFR", {"FY2025": "250%", "FY2024": "246%", "FY2023": "256%", "FY2022": "269%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page.\n"
         "FY2026 Pillar 3 ratios are a PERMANENT end to the series, not a pending publication: the bank was "
         "approved under the PRA's Small Domestic Deposit Taking regime in December 2025 and no longer "
         "prepares Pillar III disclosures. The two FY2026 ratios shown come from the Financial Report 2026's "
         "own capital note (p.32), which prints the capital amounts and the CET1 and total capital ratios "
         "only - hence no FY2026 Tier 1 ratio, leverage ratio, LCR or NSFR here.\n"
         "LEVERAGE RATIO IS TWO SERIES, NOT ONE. The UK removed claims on central banks from the leverage "
         "exposure measure from 1 January 2022, and this bank's own disclosures change basis at exactly that "
         "point. The two rows above are deliberately kept separate and must not be read as a single trend - "
         "the apparent FY2021-to-FY2022 movement is a definitional change. For the one year the bank "
         "published both, FY2021 measures 6.32% on the old basis and 8.72% on the new one; see the Leverage "
         "Ratio sheet, which carries both plus the underlying exposure measures.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/C HOARE AND CO FINANCIALS.xlsx")
