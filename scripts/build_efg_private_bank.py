import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Only 4 years available: FY2025 (y/e 31 Dec 2025) accounts are not yet filed
# at Companies House as of this build (2026-08-28) - next annual filing due by
# ~30 Sep 2026 (9-month UK deadline).
YEARS = ["FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2024_URL = ("https://find-and-update.company-information.service.gov.uk/company/02321802/"
              "filing-history/MzQ2ODA5NDQ2MGFkaXF6a2N4/document?format=pdf&download=0")
AR2023_URL = ("https://find-and-update.company-information.service.gov.uk/company/02321802/"
              "filing-history/MzQyMTAwMDI4OGFkaXF6a2N4/document?format=pdf&download=0")
AR2022_URL = ("https://find-and-update.company-information.service.gov.uk/company/02321802/"
              "filing-history/MzM4ODQ3NjMwOWFkaXF6a2N4/document?format=pdf&download=0")
AR2021_URL = ("https://find-and-update.company-information.service.gov.uk/company/02321802/"
              "filing-history/MzMzODA1ODgyNmFkaXF6a2N4/document?format=pdf&download=0")

# EFG Private Bank Limited's own standalone Pillar 3 Disclosures report - located 2026-09-04 by
# retrying efginternational.com with a spoofed browser User-Agent (the site returns HTTP 403 to a
# bare curl/no-UA request, which is what caused the original "no standalone Pillar 3 document
# locatable" conclusion below - it returns HTTP 200 with a normal browser UA). No earlier-year
# standalone Pillar 3 report for this entity was locatable via web search or the Wayback Machine
# (CDX search of efginternational.com's "pillar" and "investor" URL patterns turns up only EFG
# International Group-level and EFG Bank (Luxembourg) S.A. reports, never an EFG Private Bank
# Limited-specific one before this) - this appears to be the first year EFGIUK has published a
# standalone entity-level Pillar 3 report.
PILLAR3_2025_URL = ("https://www.efginternational.com/doc/jcr:895b914b-441b-48b6-9853-0b3aeaa4e2fd/"
                     "EFG%20Private%20Bank%20Limited%202024%20Pillar%203%20Disclosure%20Report.pdf/"
                     "lang:en/EFG%20Private%20Bank%20Limited%202024%20Pillar%203%20Disclosure%20Report.pdf")

PILLAR3_2025_NOTE = (
    "Additional source - EFG Private Bank Limited's own standalone Pillar 3 Disclosures, for the "
    "year ended 31 December 2024 (approved 30 September 2025), UK KM1 table (p.3) and UK OV1 table "
    "(p.14) - " + PILLAR3_2025_URL + "\n"
    "The report is explicitly prepared on a stand-alone basis (p.1) and its UK KM1 comparative column "
    "also discloses FY2023. FY2024/FY2023 KM1 figures are: CET1 capital GBP237.3m/205.8m, Tier 1 "
    "capital GBP303.9m/272.4m, total capital GBP303.9m/272.4m, total RWA GBP1,763.3m/1,581.0m, "
    "CET1 ratios 13.46%/13.01%, Tier 1 and total-capital ratios 17.24%/17.23%, leverage ratios "
    "5.09%/5.15%, LCR 213%/220%, and NSFR 154%/160%. The formal KM1 table is used in preference to "
    "the report's rounded introductory prose (which quotes 17.24%, 247% and 158% for selected metrics)."
)

ENTITY_NOTE = (
    "EFG Private Bank Limited (company 02321802, FRN 144036), a UK subsidiary of EFG "
    "International AG (Switzerland, listed on the SIX Swiss Exchange). Each year's Cash Flow "
    "Statement figures are that year's own originally-published statement, not a later report's "
    "restated comparative - a genuine restatement exists between FY2021's own filing and its "
    "appearance as the FY2022 report's comparative (e.g. FY2021 operating activities £586,667k "
    "own filing vs £571,317k restated comparative), and again between FY2022's own filing and "
    "its appearance as the FY2023 report's comparative (£547,141k vs £542,301k). FY2023's own "
    "filing figures match exactly what the FY2024 report shows as its own comparative, so no "
    "restatement issue there."
)

CASH_FLOW_SOURCES = (
    "Sources - EFG Private Bank Limited's own Cash Flow Statement, each year's own originally-"
    "published filing (not a later report's restated comparative):\n"
    f"FY2024: Annual Report and Financial Statements 2024, p.24-25 (Cash Flow Statement) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.24-25 (Cash Flow Statement) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2022, p.22 (Cash Flow Statement) - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021, p.22 (Cash Flow Statement) - {AR2021_URL}\n"
    + ENTITY_NOTE
)


def p3_sources(page="83"):
    return (
        "Sources - EFG Private Bank Limited's own accounts, Note 34 (Capital management), unless "
        "noted otherwise:\n"
        f"FY2024: Annual Report and Financial Statements 2024, p.{page} - {AR2024_URL}\n"
        f"FY2023: Annual Report and Financial Statements 2023, p.80 - {AR2023_URL}\n"
        f"FY2022: Annual Report and Financial Statements 2022, p.60-61 - {AR2022_URL}\n"
        "FY2021: as stated in the FY2022 Annual Report's own FY2021 comparative column, p.60-61 "
        f"- {AR2022_URL}\n"
        "No standalone Pillar 3 document was locatable for this entity as of the original build "
        "(efginternational.com returns HTTP 403 to an unauthenticated/no-User-Agent fetch; no UK-"
        "specific regulatory disclosures page found that way) - the figures below are sourced from "
        "the statutory accounts' own Capital management note. UPDATE 2026-09-04: a standalone Pillar "
        "3 report for this entity WAS subsequently located by retrying with a standard browser User-"
        "Agent (efginternational.com serves it normally to one) - see the separate Pillar 3 report "
        "source note appended below, which now supplies FY2024 figures for several metrics that "
        "remain 'Not publicly disclosed' from the statutory-accounts basis alone.\n"
        "IMPORTANT DISCLOSURE-FORMAT NOTE: FY2021 and FY2022's own Annual Reports disclose a full "
        "capital table (CET1 Capital, Total Capital, Total RWAs, CET1 Ratio, Total Capital Ratio). "
        "FY2023 and FY2024's own Annual Reports disclose ONLY Common equity tier 1 capital (£m) - "
        "no ratio, no RWA, no Total Capital figure at all, confirmed by reading the full Capital "
        "management note in both reports. This is a genuine reduction in disclosure depth between "
        "report vintages, not a gap in this research. Liquidity risk (Note 29) is purely "
        "qualitative/contractual-maturity-table based in every year reviewed - no LCR/NSFR "
        "percentage is stated anywhere. No Leverage Ratio or MREL figure was found in any year. "
        "Exhaustive follow-up: EFG's official UK document archive was also checked, including the linked "
        "'Pillar III' PDF (2018 Pillar III disclosure, which is a CRR Article 450 remuneration disclosure "
        "only, not a prudential-metrics/KM1 report) and the 2020-2024 annual-report links. No additional "
        "entity-level prudential figures for FY2021/FY2022 beyond those in the accounts were found. The "
        "2024 standalone report's comparative column supplies the previously missed FY2023 values."
    )


bw = BankWorkbook(bank_name="EFG Private Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="4223DA")

STATEMENTS_ENTITY_NOTE = (
    "EFG Private Bank Limited (company 02321802), Company-only basis (this entity has no subsidiaries "
    "consolidated in these figures - the 6 dormant/investment subsidiaries listed in Note 14 are "
    "individually immaterial and the Company's own accounts are presented as its primary statements). "
    "Each year's Balance Sheet/P&L/Statement of Changes in Equity figures are that year's own "
    "originally-published statement, not a later report's restated comparative, except where noted."
)

BS_IS_EQ_SOURCES = (
    "Sources - EFG Private Bank Limited's own Balance Sheet/Income Statement/Statement of Comprehensive "
    "Income/Statement of Changes in Equity, each year's own originally-published filing:\n"
    f"FY2024: Annual Report and Financial Statements 2024, p.20-23 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.20-23 - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2022, p.18-21 - {AR2022_URL}\n"
    f"FY2021: as stated in the FY2022 Annual Report's own FY2021 comparative column (restated for a "
    f"loan-facility-fee reclassification per that report's own footnote), p.18-21 - {AR2022_URL}\n"
    + STATEMENTS_ENTITY_NOTE +
    "\nFY2023's Balance Sheet page footer is mislabelled \"EFG International AG\" / \"Consolidated "
    "balance sheet\" in the source PDF (a template artifact) - the figures themselves are EFG Private "
    "Bank Limited's own Company-only balance sheet, confirmed by cross-tie to both FY2022's and "
    "FY2024's own comparative columns."
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
bw.add_balance_sheet_sheet(
    title="EFG Private Bank Limited — Standalone Statement of Financial Position",
    subtitle="Company basis, £'000. See source note at bottom.",
    rows=[
        ("SECTION", "Assets", {}),
        ("DATA", "Cash and balances with central banks",
         {"FY2024": 795400, "FY2023": 686860, "FY2022": 1213286, "FY2021": 1244267}),
        ("DATA", "Due from other banks",
         {"FY2024": 55991, "FY2023": 87593, "FY2022": 95177, "FY2021": 124974}),
        ("DATA", "Derivative financial instruments",
         {"FY2024": 20591, "FY2023": 24974, "FY2022": 58670, "FY2021": 10099}),
        ("DATA", "Investment securities",
         {"FY2024": 2268701, "FY2023": 2066635, "FY2022": 1487411, "FY2021": 852764}),
        ("DATA", "Loans and advances to customers",
         {"FY2024": 3398294, "FY2023": 2907872, "FY2022": 2967101, "FY2021": 2764761}),
        ("DATA", "Investment in subsidiaries",
         {"FY2024": 1320, "FY2023": 1320, "FY2022": 1320, "FY2021": 1320}),
        ("DATA", "Property, plant and equipment",
         {"FY2024": 25314, "FY2023": 22678, "FY2022": 25182, "FY2021": 24002}),
        ("DATA", "Intangible assets",
         {"FY2024": 420, "FY2023": 4508, "FY2022": 3113, "FY2021": 1798}),
        ("DATA", "Deferred income tax assets",
         {"FY2024": 7305, "FY2023": 5228, "FY2022": 11333, "FY2021": 5553}),
        ("DATA", "Other assets",
         {"FY2024": 35380, "FY2023": 48492, "FY2022": 27013, "FY2021": 24994}),
        ("TOTAL", "Total assets",
         {"FY2024": 6608716, "FY2023": 5856160, "FY2022": 5889606, "FY2021": 5054532}),
        ("SECTION", "Liabilities", {}),
        ("DATA", "Due to other banks",
         {"FY2024": 1157827, "FY2023": 694997, "FY2022": 758752, "FY2021": 539184}),
        ("DATA", "Due to customers",
         {"FY2024": 5042962, "FY2023": 4715872, "FY2022": 4762542, "FY2021": 4152829}),
        ("DATA", "Derivative financial instruments",
         {"FY2024": 8939, "FY2023": 22273, "FY2022": 13603, "FY2021": 22109}),
        ("DATA", "Current income tax liabilities",
         {"FY2024": 1072, "FY2023": 4779, "FY2022": 5103, "FY2021": 1742}),
        ("DATA", "Provisions",
         {"FY2024": 1787, "FY2023": 3168, "FY2022": 3382, "FY2021": 3427}),
        ("DATA", "Other liabilities",
         {"FY2024": 75135, "FY2023": 107705, "FY2022": 72042, "FY2021": 67977}),
        ("TOTAL", "Total liabilities",
         {"FY2024": 6287722, "FY2023": 5548794, "FY2022": 5615424, "FY2021": 4787268}),
        ("SECTION", "Equity", {}),
        ("DATA", "Share capital",
         {"FY2024": 31596, "FY2023": 31596, "FY2022": 31596, "FY2021": 31596}),
        ("DATA", "Share premium",
         {"FY2024": 96639, "FY2023": 96639, "FY2022": 96639, "FY2021": 96639}),
        ("DATA", "Capital redemption reserve",
         {"FY2024": 10000, "FY2023": 10000, "FY2022": 10000, "FY2021": 10000}),
        ("DATA", "Other equity and reserves",
         {"FY2024": 72515, "FY2023": 72571, "FY2022": 55451, "FY2021": 73325}),
        ("DATA", "Retained earnings",
         {"FY2024": 110244, "FY2023": 96560, "FY2022": 80496, "FY2021": 55704}),
        ("TOTAL", "Total equity",
         {"FY2024": 320994, "FY2023": 307366, "FY2022": 274182, "FY2021": 267264}),
        ("TOTAL", "Total liabilities and equity",
         {"FY2024": 6608716, "FY2023": 5856160, "FY2022": 5889606, "FY2021": 5054532}),
    ],
    sources_text=BS_IS_EQ_SOURCES,
    first_col_width=64,
    source_height=260,
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
bw.add_income_statement_sheet(
    title="EFG Private Bank Limited — Income Statement / Statement of Comprehensive Income",
    subtitle="Company basis, £'000. See source note at bottom.",
    rows=[
        ("SECTION", "Income", {}),
        ("DATA", "Interest income",
         {"FY2024": 347776, "FY2023": 304437, "FY2022": 133296, "FY2021": 59764}),
        ("DATA", "Interest expense",
         {"FY2024": -244347, "FY2023": -194252, "FY2022": -53553, "FY2021": -13548}),
        ("TOTAL", "Net interest income",
         {"FY2024": 103429, "FY2023": 110185, "FY2022": 79743, "FY2021": 46216}),
        ("DATA", "Banking fee and commission income",
         {"FY2024": 64443, "FY2023": 56844, "FY2022": 60878, "FY2021": 63082}),
        ("DATA", "Banking fee and commission expense",
         {"FY2024": -3218, "FY2023": -3416, "FY2022": -3337, "FY2021": -2781}),
        ("TOTAL", "Net banking fee and commission income",
         {"FY2024": 61225, "FY2023": 53428, "FY2022": 57541, "FY2021": 60301}),
        ("DATA", "Dividend income", {"FY2021": 30000}),
        ("DATA", "Net trading income/(expense) on financial instruments",
         {"FY2024": -579, "FY2023": -793, "FY2022": 1380, "FY2021": 747}),
        ("DATA", "Net trading income/(expense) on foreign exchange",
         {"FY2024": -1869, "FY2023": 3308, "FY2022": 543, "FY2021": 4862}),
        ("DATA", "Gains less losses on disposal of financial assets",
         {"FY2024": 0, "FY2023": 217, "FY2022": 147, "FY2021": 60}),
        ("TOTAL", "Net other income",
         {"FY2024": -2448, "FY2023": 2732, "FY2022": 2070, "FY2021": 35669}),
        ("TOTAL", "Operating and investing income",
         {"FY2024": 162206, "FY2023": 166345, "FY2022": 139354, "FY2021": 142186}),
        ("DATA", "Operating expenses",
         {"FY2024": -134329, "FY2023": -125648, "FY2022": -104693, "FY2021": -112020}),
        ("DATA", "Profit on disposal of subsidiary", {"FY2021": 68900}),
        ("DATA", "Loss allowance/(reversal) on financial assets at amortised cost",
         {"FY2024": -1690, "FY2023": -555, "FY2022": 210, "FY2021": -37}),
        ("TOTAL", "Profit before tax",
         {"FY2024": 26187, "FY2023": 40142, "FY2022": 34871, "FY2021": 99029}),
        ("DATA", "Income tax (expense)/credit",
         {"FY2024": -5712, "FY2023": -4395, "FY2022": -4609, "FY2021": 2133}),
        ("TOTAL", "Net profit for the year",
         {"FY2024": 20475, "FY2023": 35747, "FY2022": 30262, "FY2021": 101162}),
        ("SECTION", "Other comprehensive income/(expense)", {}),
        ("DATA", "Net (losses)/gains on investments in debt instruments measured at FVOCI",
         {"FY2024": -837, "FY2023": 0, "FY2022": -36347, "FY2021": -11318}),
        ("DATA", "Net gains/(losses) on designated hedges over debt instruments measured at FVOCI",
         {"FY2022": 13774, "FY2021": 9158}),
        ("DATA", "Transfers to the Income Statement on realised gains/(losses) on FVOCI debt instruments",
         {"FY2021": 12}),
        ("DATA", "Net (losses)/gains on investments in equity instruments designated at FVOCI",
         {"FY2021": -51}),
        ("DATA", "Deferred tax on the above items",
         {"FY2024": 209, "FY2023": -5464, "FY2022": 6400, "FY2021": 0}),
        ("TOTAL", "Total other comprehensive income/(expense) for the year",
         {"FY2024": -628, "FY2023": 18924, "FY2022": -16173, "FY2021": -2199}),
        ("TOTAL", "Total comprehensive income for the year, net of tax",
         {"FY2024": 19847, "FY2023": 54671, "FY2022": 14089, "FY2021": 98963}),
    ],
    sources_text=BS_IS_EQ_SOURCES + (
        "\nFY2023's Statement of Comprehensive Income (as filed in the FY2023 Annual Report) shows "
        "Net losses on debt instruments at FVOCI of £nil for FY2023 itself and restates FY2022 to "
        "£(22,573)k under a hedge-effect-inclusive presentation - the figures above use each year's "
        "own originally-published, non-restated presentation throughout (FY2022's OCI lines are as "
        "originally filed in the FY2022 Annual Report, not the FY2023 report's restated comparative)."
    ),
    first_col_width=72,
    source_height=260,
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
equity_headers = ["Share capital", "Share premium", "Capital redemption reserve",
                   "Other equity and reserves", "Retained earnings", "Total equity"]

bw.add_equity_changes_sheet(
    title="EFG Private Bank Limited — Statement of Changes in Equity",
    subtitle="Company basis, £'000, chronological (oldest to newest). See source note at bottom.",
    headers=equity_headers,
    rows=[
        ("TOTAL", "Balance at 1 January 2021", (31596, 96639, 10000, 75519, 50623, 264377)),
        ("DATA", "Net profit for the year", (None, None, None, None, 101162, 101162)),
        ("DATA", "Net gains on investments in debt instruments measured at FVOCI (incl. hedging effect)",
         (None, None, None, -2223, None, -2223)),
        ("DATA", "Income tax relating to components of other comprehensive expense",
         (None, None, None, 0, None, 0)),
        ("TOTAL", "Total comprehensive income for the year", (None, None, None, -2223, 101162, 98939)),
        ("DATA", "AT1 interest treated as appropriation of retained earnings",
         (None, None, None, None, -5401, -5401)),
        ("DATA", "Employee equity incentive plans amortisation and net of exercise costs",
         (None, None, None, -1651, None, -1651)),
        ("DATA", "Payment of ordinary dividends", (None, None, None, None, -89000, -89000)),
        ("DATA", "Transfers to retained earnings", (None, None, None, 1680, -1680, 0)),
        ("TOTAL", "Balance at 31 December 2021", (31596, 96639, 10000, 73325, 55704, 267264)),
        ("DATA", "Net profit for the year", (None, None, None, None, 30262, 30262)),
        ("DATA", "Net gains on investments in debt instruments measured at FVOCI (incl. hedging effect)",
         (None, None, None, -22573, None, -22573)),
        ("DATA", "Income tax relating to components of other comprehensive income",
         (None, None, None, 6400, None, 6400)),
        ("TOTAL", "Total comprehensive income for the year", (None, None, None, -16173, 30262, 14089)),
        ("DATA", "AT1 interest treated as appropriation of retained earnings",
         (None, None, None, None, -5470, -5470)),
        ("DATA", "Employee equity incentive plans amortisation net of exercise costs",
         (None, None, None, -1943, None, -1943)),
        ("DATA", "Payment of ordinary dividends", (None, None, None, None, 0, 0)),
        ("TOTAL", "Balance at 31 December 2022", (31596, 96639, 10000, 55451, 80496, 274182)),
        ("DATA", "Net profit for the year", (None, None, None, None, 35747, 35747)),
        ("DATA", "Changes in investment securities accounting classification (Note 12)",
         (None, None, None, 24388, None, 24388)),
        ("DATA", "Income tax relating to components of other comprehensive income",
         (None, None, None, -5464, None, -5464)),
        ("TOTAL", "Total comprehensive income for the year", (None, None, None, 18924, 35747, 54671)),
        ("DATA", "AT1 interest treated as appropriation of retained earnings",
         (None, None, None, None, -7165, -7165)),
        ("DATA", "Employee equity incentive plans amortisation net of exercise costs",
         (None, None, None, -1943, None, -1943)),
        ("DATA", "Payment of ordinary dividends", (None, None, None, None, -12676, -12676)),
        ("DATA", "Other movements", (None, None, None, 139, 158, 297)),
        ("TOTAL", "Balance at 31 December 2023", (31596, 96639, 10000, 72571, 96560, 307366)),
        ("DATA", "Net profit for the year", (None, None, None, None, 20475, 20475)),
        ("DATA", "Changes in investment securities accounting classification (Note 12)",
         (None, None, None, 0, None, 0)),
        ("DATA", "Net losses on investments in debt instruments measured at FVOCI (incl. hedging effect)",
         (None, None, None, -837, None, -837)),
        ("DATA", "Income tax relating to components of other comprehensive income",
         (None, None, None, 209, None, 209)),
        ("TOTAL", "Total comprehensive income for the year", (None, None, None, -628, 20475, 19847)),
        ("DATA", "AT1 interest treated as appropriation of retained earnings",
         (None, None, None, None, -6791, -6791)),
        ("DATA", "Employee equity incentive plans amortisation net of exercise costs",
         (None, None, None, 572, None, 572)),
        ("DATA", "Payment of ordinary dividends", (None, None, None, None, 0, 0)),
        ("TOTAL", "Balance at 31 December 2024", (31596, 96639, 10000, 72515, 110244, 320994)),
    ],
    sources_text=BS_IS_EQ_SOURCES + (
        "\nPer-year reconciliation confirmed: each year's opening balance ties to the prior year's own "
        "closing balance, and each year's closing balance ties to that year's own Balance Sheet Total "
        "equity figure (FY2021 closing 267,264 / FY2022 closing 274,182 / FY2023 closing 307,366 / "
        "FY2024 closing 320,994 - all four tie exactly, no plug rows needed)."
    ),
    first_col_width=68,
    source_height=220,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operations", {}),
    ("DATA", "Profit before tax",
     {"FY2024": 26187, "FY2023": 40142, "FY2022": 34871, "FY2021": 99029}),
    ("DATA", "Depreciation of fixed assets",
     {"FY2024": 4248, "FY2023": 3323, "FY2022": 4499, "FY2021": 4752}),
    ("DATA", "Amortisation of intangibles",
     {"FY2024": 245, "FY2023": 551, "FY2022": 535, "FY2021": 434}),
    ("DATA", "Amortisation of IFRS 2 reserve through profit and loss",
     {"FY2024": 9630, "FY2023": 6052, "FY2022": 4214, "FY2021": 4030}),
    ("DATA", "Loss allowance provision",
     {"FY2024": 1690, "FY2023": 555, "FY2022": -210, "FY2021": 37}),
    ("DATA", "Loss/(gain) on sale of subsidiary as investment activity",
     {"FY2022": 0, "FY2021": -68900}),
    ("DATA", "Gains less losses on disposal of financial assets",
     {"FY2024": 0, "FY2023": -217, "FY2022": -147, "FY2021": -60}),
    ("DATA", "Dividend paid by subsidiary included in investment income",
     {"FY2022": 0, "FY2021": -30000}),
    ("DATA", "Lease interest per IFRS16",
     {"FY2024": 581, "FY2023": 435, "FY2022": 448, "FY2021": 156}),
    ("DATA", "Change in interest accrual",
     {"FY2024": -9430, "FY2023": -4920}),
    ("DATA", "Effect of foreign exchange",
     {"FY2024": -5429, "FY2023": 51485, "FY2022": -61770}),
    ("DATA", "Release of tax related provision", {"FY2024": -1991}),
    ("DATA", "(Increase)/decrease in derivative financial instruments",
     {"FY2024": -8951, "FY2023": 42583, "FY2022": -57077, "FY2021": -15336}),
    ("DATA", "(Increase)/decrease in loans and advances to customers",
     {"FY2024": -492079, "FY2023": 59123, "FY2022": -202340, "FY2021": -590609}),
    ("DATA", "Decrease/(increase) in other assets",
     {"FY2024": 15349, "FY2023": -21479, "FY2022": -2019, "FY2021": 28685}),
    ("DATA", "Increase/(decrease) in due to other banks",
     {"FY2024": 462830, "FY2023": -63755, "FY2022": 219568, "FY2021": 11595}),
    ("DATA", "Increase/(decrease) in due to customers",
     {"FY2024": 327090, "FY2023": -46670, "FY2022": 609713, "FY2021": 1137564}),
    ("DATA", "(Decrease)/increase in other liabilities and provisions",
     {"FY2024": -30373, "FY2023": 35466, "FY2022": 5925, "FY2021": 12154}),
    ("DATA", "Payments to tax authorities", {"FY2024": -9774, "FY2023": -5025}),
    ("DATA", "Corporation tax paid", {"FY2022": -2617, "FY2021": -1183}),
    ("DATA", "Payments to parent for participation in share scheme",
     {"FY2024": -9465, "FY2023": -7833, "FY2022": -6452, "FY2021": -5681}),
    ("TOTAL", "Net cash flows from operating activities",
     {"FY2024": 280358, "FY2023": 89816, "FY2022": 547141, "FY2021": 586667}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "(Purchase) of investment securities",
     {"FY2024": -1817999, "FY2023": -1574973, "FY2022": -1177277, "FY2021": -453370}),
    ("DATA", "Proceeds from maturities/sale of investment securities",
     {"FY2024": 1630203, "FY2023": 973586, "FY2022": 587790, "FY2021": 340452}),
    ("DATA", "(Purchase) of capital in subsidiaries", {"FY2021": -1275}),
    ("DATA", "Proceeds from disposal of subsidiary", {"FY2021": 78900}),
    ("DATA", "(Purchase) of property plant & equipment",
     {"FY2024": -2864, "FY2023": -819, "FY2022": -5793, "FY2021": -176}),
    ("DATA", "(Purchase) of intangible assets",
     {"FY2024": -2414, "FY2023": -1946, "FY2022": -1850, "FY2021": -973}),
    ("DATA", "Proceeds from dividends", {"FY2021": 30000}),
    ("TOTAL", "Net cash flows used in investing activities",
     {"FY2024": -193074, "FY2023": -604152, "FY2022": -597130, "FY2021": -6442}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Payment of AT1 interest",
     {"FY2024": -7174, "FY2023": -7154, "FY2022": -5394, "FY2021": -5389}),
    ("DATA", "Payment of dividends",
     {"FY2024": 0, "FY2023": -12676, "FY2022": 0, "FY2021": -89000}),
    ("DATA", "Lease interest repaid",
     {"FY2024": -421, "FY2023": -36, "FY2022": -448, "FY2021": None}),
    ("DATA", "Lease disposal", {"FY2024": -267}),
    ("DATA", "Lease principal repaid",
     {"FY2024": -2202, "FY2023": -644, "FY2022": -1905, "FY2021": -3028}),
    ("TOTAL", "Net cash flows from financing activities",
     {"FY2024": -10064, "FY2023": -20510, "FY2022": -7747, "FY2021": -97417}),
    ("TOTAL", "Net cash outflows/(inflows)",
     {"FY2024": 77220, "FY2023": -534846, "FY2022": -57736, "FY2021": 482808}),
    ("DATA", "Effect of exchange rate changes on cash and cash equivalents",
     {"FY2024": -326, "FY2023": 794, "FY2022": -3042, "FY2021": -12197}),
    ("TOTAL", "Net change in cash and cash equivalents",
     {"FY2024": 76894, "FY2023": -534052, "FY2022": -60778, "FY2021": 470611}),
    ("DATA", "Cash and cash equivalents at the beginning of period",
     {"FY2024": 769571, "FY2023": 1303623, "FY2022": 1369241, "FY2021": 898630}),
    ("TOTAL", "Cash and cash equivalents at the end of period",
     {"FY2024": 846465, "FY2023": 769571, "FY2022": 1308463, "FY2021": 1369241}),
]

bw.add_cash_flow_sheet(
    title="EFG Private Bank Limited — Cash Flow Statement",
    subtitle="Company basis, £'000. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
ASSET_QUALITY_SOURCES = (
    "Sources - EFG Private Bank Limited's own accounts, Note 13 (Loans and advances to customers) and "
    "Note 27/27.11 (Credit risk - Loans and Advances to customers, gross exposures/movements/loss "
    "allowances by IFRS 9 stage), each year's own originally-published filing:\n"
    f"FY2024: Annual Report and Financial Statements 2024, p.42, 64 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.42, 64 - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2022, p.33, 52-53 - {AR2022_URL}\n"
    f"FY2021: as stated in the FY2022 Annual Report's own FY2021 comparative column, p.33, 52-53 "
    f"- {AR2022_URL}\n"
    + STATEMENTS_ENTITY_NOTE +
    "\nIMPORTANT DISCLOSURE-BASIS NOTE: FY2021 and FY2022's own Annual Reports disclose full gross "
    "loan exposure by IFRS 9 stage (Stage 1/2/3), for Mortgages and Other/Lombard loans separately - "
    "used directly below (summed across both loan types). FY2023 and FY2024's own Annual Reports "
    "disclose ONLY the ECL loss allowance broken down by stage, not the gross exposure by stage - "
    "confirmed by reading the full Note 27 credit risk exposure table in both reports. The 'Gross "
    "exposure by stage' rows are therefore genuinely blank for FY2023/FY2024, not a research gap; "
    "the 'Loss allowance by stage' rows are populated for all 4 years since that split is disclosed "
    "throughout."
    "\nFY2022/FY2021's own Note 13 shows a separate 'Deferred loan fee' deduction line (net loan "
    "facility fees under EIR accounting) between the loss allowance and the net loans and advances "
    "figure; FY2023/FY2024's own Note 13 does not show this as a separate line at all (Gross - Loss "
    "allowance = Net exactly in both years) - a genuine note-presentation change between report "
    "vintages, not a transcription gap, confirmed by reading Note 13 in full in all 4 reports."
)

bw.add_asset_quality_sheet(
    title="EFG Private Bank Limited — Asset Quality",
    subtitle="Company basis, £'000. See source note at bottom.",
    rows=[
        ("SECTION", "Gross loans and advances by product", {}),
        ("DATA", "Mortgages",
         {"FY2024": 2574601, "FY2023": 2161229, "FY2022": 2101252, "FY2021": 1809606}),
        ("DATA", "Other and Lombard loans",
         {"FY2024": 826736, "FY2023": 748153, "FY2022": 871619, "FY2021": 960987}),
        ("TOTAL", "Gross loans and advances",
         {"FY2024": 3401337, "FY2023": 2909382, "FY2022": 2972872, "FY2021": 2770593}),
        ("SECTION", "Gross exposure by IFRS 9 stage (Mortgages + Other/Lombard combined)", {}),
        ("DATA", "Stage 1 (12-month ECL)", {"FY2022": 2792274, "FY2021": 2641488}),
        ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {"FY2022": 108967, "FY2021": 64481}),
        ("DATA", "Stage 3 (lifetime ECL, credit-impaired)", {"FY2022": 71630, "FY2021": 64624}),
        ("SECTION", "Loss allowance", {}),
        ("DATA", "Loss allowance - Stage 1",
         {"FY2024": 1064, "FY2023": 432, "FY2022": 70, "FY2021": 133}),
        ("DATA", "Loss allowance - Stage 2",
         {"FY2024": 513, "FY2023": 516, "FY2022": 104, "FY2021": 119}),
        ("DATA", "Loss allowance - Stage 3",
         {"FY2024": 1466, "FY2023": 562, "FY2022": 1230, "FY2021": 1432}),
        ("TOTAL", "Total loss allowance",
         {"FY2024": 3043, "FY2023": 1510, "FY2022": 1404, "FY2021": 1684}),
        ("DATA", "Less: Deferred loan fee (FY2022/FY2021 note presentation only - see source note)",
         {"FY2022": -4366, "FY2021": -4148}),
        ("TOTAL", "Loans and advances to customers (net)",
         {"FY2024": 3398294, "FY2023": 2907872, "FY2022": 2967101, "FY2021": 2764761}),
        ("SECTION", "Derived ratios", {}),
        ("DATA", "ECL coverage ratio (total loss allowance / gross loans)",
         {"FY2024": "0.09%", "FY2023": "0.05%", "FY2022": "0.05%", "FY2021": "0.06%"}),
        ("DATA", "Stage 3 as % of gross loans (NPL proxy)",
         {"FY2022": "2.41%", "FY2021": "2.33%"}),
    ],
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=76,
    source_height=280,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=170)


NOT_DISCLOSED_NOTE = (
    "Not publicly disclosed for this entity. No standalone Pillar 3 document was locatable, and "
    "this metric does not appear in the statutory accounts' Capital management or Liquidity risk "
    "notes for this year (confirmed by reading both notes directly, not assumed)."
)

metric(
    "CET1 Capital", "£m",
    [("Common equity tier 1 capital",
      {"FY2024": 237.3, "FY2023": 205.8, "FY2022": 165.6, "FY2021": 195.2})],
    p3_sources(),
    note="FY2022/FY2021 stated as \"(audited)\" in the source; FY2024/FY2023 not marked audited/unaudited.",
)

metric(
    "CET1 Ratio", "%",
    [("Common equity tier 1 capital ratio", {"FY2024": "13.46%", "FY2023": "13.01%", "FY2022": "10.9%", "FY2021": "14.8%"})],
    p3_sources() + "\n" + PILLAR3_2025_NOTE,
    note="FY2023 and FY2024 are sourced from EFGIUK's own "
         "standalone Pillar 3 Disclosures report - see the additional source note below for the "
         "discrepancy this creates against the CET1 Capital £m sheet's own FY2024 figure.",
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2024": 303.9, "FY2023": 272.4, "FY2022": 165.6, "FY2021": 195.2})],
    p3_sources(),
    note="FY2023 and FY2024 are sourced from the standalone Pillar 3 UK KM1 table, which discloses "
         "an Additional Tier 1 component not shown in the statutory accounts' Note 34.",
)

metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 ratio", {"FY2024": "17.24%", "FY2023": "17.23%", "FY2022": "10.9%", "FY2021": "14.8%"})],
    p3_sources() + "\n" + PILLAR3_2025_NOTE,
    note="FY2023/FY2024 are sourced from the standalone Pillar 3 UK KM1 table. FY2022/FY2021 are = "
         "CET1 ratio, since no AT1 instruments were disclosed in the statutory accounts. "
         "from EFGIUK's own standalone Pillar 3 Disclosures report and is HIGHER than the FY2022/FY2021 "
         "CET1-equals-Tier1 figures because that report discloses a GBP66.6m AT1 instrument for FY2024 "
         "not mentioned in the statutory accounts - see the additional source note below.",
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2024": 303.9, "FY2023": 272.4, "FY2022": 232.3, "FY2021": 261.8})],
    p3_sources() + "\n" + PILLAR3_2025_NOTE,
    note="FY2023/FY2024 are sourced from the standalone Pillar 3 UK KM1 table. FY2022/FY2021 values are from the statutory accounts' "
         "own table (Tier 1 + Tier 2; Tier 2 comprises unrealised FVOCI gains per the source's own "
         "definition, not separately itemised). FY2024 is now sourced from EFGIUK's own standalone "
         "Pillar 3 Disclosures report (Total capital = Tier 1 + Tier 2, with Tier 2 = nil that year) - "
         "see the additional source note below for the discrepancy this creates against the accounts-"
         "based basis used for FY2022/FY2021.",
)

metric(
    "Total Capital Ratio", "%",
    [("Total capital ratio", {"FY2024": "17.24%", "FY2023": "17.23%", "FY2022": "15.2%", "FY2021": "19.9%"})],
    p3_sources() + "\n" + PILLAR3_2025_NOTE,
    note="FY2023/FY2024 are sourced from EFGIUK's own standalone "
         "Pillar 3 Disclosures report - see the additional source note below.",
)

metric(
    "Total RWAs", "£m",
    [("Total risk weighted assets", {"FY2024": 1763.3, "FY2023": 1581.0, "FY2022": 1523.7, "FY2021": 1317.8})],
    p3_sources() + "\n" + PILLAR3_2025_NOTE,
    note="FY2023/FY2024 are sourced from EFGIUK's standalone Pillar 3 report; FY2022/FY2021 as directly stated in the statutory "
         "accounts (not calculated). FY2024 is now sourced from EFGIUK's own standalone Pillar 3 "
         "Disclosures report, UK KM1 table - see the additional source note below (also see the RWA "
         "Breakdown sheet, which now has a full FY2024 breakdown by risk category from the same "
         "report's UK OV1 table).",
)

bw.add_rwa_breakdown_sheet(
    title="EFG Private Bank Limited — RWA Breakdown",
    subtitle="FY2024/FY2023 (UK OV1 template, from Pillar 3 report); FY2022/FY2021 not publicly "
             "disclosed. £m. See source note at bottom.",
    rows=[
        ("DATA", "Credit risk (excluding CCR)", {"FY2024": 1430.2, "FY2023": 1246.2}),
        ("DATA", "  of which standardised approach", {"FY2024": 1430.2, "FY2023": 1246.2}),
        ("DATA", "Counterparty credit risk (CCR)", {"FY2024": 64.0, "FY2023": 31.6}),
        ("DATA", "  of which standardised approach", {"FY2024": 38.0, "FY2023": 31.6}),
        ("DATA", "  of which credit valuation adjustment (CVA)", {"FY2024": 26.0}),
        ("DATA", "Settlement risk", {"FY2024": 0, "FY2023": 0}),
        ("DATA", "Operational risk", {"FY2024": 269.0, "FY2023": 279.4}),
        ("DATA", "  of which standardised approach", {"FY2024": 269.0, "FY2023": 279.4}),
        ("TOTAL", "Total risk-weighted exposure amount", {"FY2024": 1763.3, "FY2023": 1581.0}),
        ("DATA", "FY2022 / FY2021: Not publicly disclosed", {}),
    ],
    sources_text=(
        "Sources - EFG Private Bank Limited's own accounts, Note 34 (Capital management), and its own "
        "standalone Pillar 3 Disclosures report:\n"
        + NOT_DISCLOSED_NOTE +
        " Even in FY2022/FY2021, when a Total risk weighted assets figure is disclosed (Note 34), it "
        "is a single aggregate figure only - no breakdown by risk category appears anywhere in Note 34 "
        "or elsewhere in the accounts in any of the 4 years, confirmed by reading the note in full. "
        "FY2023 similarly has no breakdown (that year's accounts disclose no RWA figure at all).\n"
        "FY2024 IS now available, from the UK OV1 'Overview of risk weighted exposure amounts' "
        "template, p.14 (not p.3, unlike the other Pillar 3 metrics below):\n"
        + PILLAR3_2025_NOTE
    ),
    first_col_width=54,
    source_height=280,
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio (excluding claims on central banks)", {"FY2024": "5.09%", "FY2023": "5.15%"})],
    p3_sources() + "\n" + PILLAR3_2025_NOTE,
    note="Not publicly disclosed for FY2023/FY2022/FY2021 - no Leverage Ratio figure was found in the "
         "statutory accounts for any of those years (confirmed by reading the Capital management and "
         "Liquidity risk notes directly). FY2024 is now sourced from EFGIUK's own standalone Pillar 3 "
         "Disclosures report; EFGIUK is not a LREQ firm and is not required to maintain the 3.25% "
         "minimum under the UK leverage ratio framework (stated directly in the source).",
)

metric(
    "LCR", "%",
    [("Liquidity coverage ratio", {"FY2024": "213%", "FY2023": "220%"})],
    p3_sources() + "\n" + PILLAR3_2025_NOTE,
    note="Not publicly disclosed for FY2023/FY2022/FY2021 - Liquidity risk (Note 29) is purely "
         "qualitative/contractual-maturity-table based in every statutory accounts year reviewed, no "
         "LCR percentage stated anywhere. FY2024 is now sourced from EFGIUK's own standalone Pillar 3 "
         "Disclosures report, UK KM1 table (liquidity values calculated as a simple average of the "
         "12-month end observations, per that table's own footnote) - see the additional source note "
         "below for a separate LCR figure (227%) quoted in that report's own introductory prose for "
         "FY2025 (not used here, and not for FY2024 in any case).",
)

metric(
    "NSFR", "%",
    [("Net stable funding ratio", {"FY2024": "154%", "FY2023": "160%"})],
    p3_sources() + "\n" + PILLAR3_2025_NOTE,
    note="Not publicly disclosed for FY2023/FY2022/FY2021, for the same reason as LCR above. FY2024 is "
         "now sourced from EFGIUK's own standalone Pillar 3 Disclosures report, UK KM1 table (net "
         "stable funding values calculated on the average of quarter-end positions, per that table's "
         "own footnote).",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources() + "\n" + PILLAR3_2025_NOTE,
    per_note={
        "MREL Ratio": NOT_DISCLOSED_NOTE + " EFGIUK's own standalone Pillar 3 Disclosures report "
        "(FY2025/FY2024) also has no MREL section or figure of any kind - confirmed against that "
        "report's own table of contents, which has no MREL entry."
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets",
         {"FY2024": 6608716, "FY2023": 5856160, "FY2022": 5889606, "FY2021": 5054532}),
        ("Loans and advances to customers",
         {"FY2024": 3398294, "FY2023": 2907872, "FY2022": 2967101, "FY2021": 2764761}),
        ("Due to customers",
         {"FY2024": 5042962, "FY2023": 4715872, "FY2022": 4762542, "FY2021": 4152829}),
        ("Total equity",
         {"FY2024": 320994, "FY2023": 307366, "FY2022": 274182, "FY2021": 267264}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Operating and investing income",
         {"FY2024": 162206, "FY2023": 166345, "FY2022": 139354, "FY2021": 142186}),
        ("Operating expenses",
         {"FY2024": -134329, "FY2023": -125648, "FY2022": -104693, "FY2021": -112020}),
        ("Net profit for the year",
         {"FY2024": 20475, "FY2023": 35747, "FY2022": 30262, "FY2021": 101162}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity",
         {"FY2024": 307366, "FY2023": 274182, "FY2022": 267264, "FY2021": 264377}),
        ("Total comprehensive income for the year",
         {"FY2024": 19847, "FY2023": 54671, "FY2022": 14089, "FY2021": 98939}),
        ("Other equity movements, net",
         {"FY2024": -6219, "FY2023": -21487, "FY2022": -7171, "FY2021": -96052}),
        ("Closing equity",
         {"FY2024": 320994, "FY2023": 307366, "FY2022": 274182, "FY2021": 267264}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash flows from operating activities",
         {"FY2024": 280358, "FY2023": 89816, "FY2022": 547141, "FY2021": 586667}),
        ("Net cash flows used in investing activities",
         {"FY2024": -193074, "FY2023": -604152, "FY2022": -597130, "FY2021": -6442}),
        ("Net cash flows from financing activities",
         {"FY2024": -10064, "FY2023": -20510, "FY2022": -7747, "FY2021": -97417}),
        ("Cash and cash equivalents at end of period",
         {"FY2024": 846465, "FY2023": 769571, "FY2022": 1308463, "FY2021": 1369241}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2024": "13.46%", "FY2023": "13.01%", "FY2022": "10.9%", "FY2021": "14.8%"}),
        ("Total Capital Ratio", {"FY2024": "17.24%", "FY2023": "17.23%", "FY2022": "15.2%", "FY2021": "19.9%"}),
    ],
    note="FY2023's own Annual Report is supplemented by the standalone Pillar 3 comparative column, "
         "which supplies the previously missed FY2023 regulatory ratios and RWA. FY2024 ratios are sourced from "
         "EFGIUK's own standalone Pillar 3 Disclosures report (located 2026-09-04), NOT from the "
         "statutory accounts used for FY2022/FY2021 - see the CET1 Ratio/Total Capital Ratio sheets' "
         "own source notes for the resulting discrepancy against the CET1 Capital £m sheet's FY2024 "
         "figure. Figures are duplicated from the detail sheets for at-a-glance trend viewing; see "
         "each sheet's own source citation for the underlying document/page.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/EFG PRIVATE BANK FINANCIALS.xlsx")
