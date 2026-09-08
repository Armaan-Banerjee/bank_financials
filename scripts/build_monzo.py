import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018"]  # most recent first
YEAR_LABEL = {
    "FY2025": "FY2025 (MBHG)",
    "FY2024": "FY2024 (MBHG)*",
    "FY2023": "FY2023 (MBL)",
    "FY2022": "FY2022 (MBL)",
    "FY2021": "FY2021 (MBL)",
    "FY2020": "FY2020 (MBL)",
    "FY2019": "FY2019 (MBL)",
    "FY2018": "FY2018 (MBL)",
}

AR26_URL = "https://monzo.com/annual-report/2026/Monzo-Annual-Report-2026.pdf"
AR25_URL = "https://monzo.com/annual-report/2025/Monzo%20Bank%20Group%20FY2025%20Annual%20Report.pdf"
AR24_URL = "https://monzo.com/docs/monzo-annual-report-2024.pdf"
AR23_URL = "https://monzo.com/docs/monzo-annual-report-2023.pdf"
AR22_URL = "https://monzo.com/static/docs/monzo-annual-report-2022.pdf"
AR20_URL = "https://monzo.com/docs/monzo-annual-report-2020.pdf"
# FY2019 and FY2018 statutory accounts are not archived under a guessable URL on monzo.com (only FY2020
# onward are); sourced instead directly from Companies House's own filed-accounts PDF for Monzo Bank
# Limited (co. no. 09446231), a stable government primary source.
CH_FY2019_URL = "https://find-and-update.company-information.service.gov.uk/company/09446231/filing-history/MzIzOTY5Nzg5MGFkaXF6a2N4/document?format=pdf&download=0"
CH_FY2018_URL = "https://find-and-update.company-information.service.gov.uk/company/09446231/filing-history/MzE4MzMzNTM5OWFkaXF6a2N4/document?format=pdf&download=0"

P3_25_URL = "https://monzo.com/annual-report/2025/monzo-pillar-3-2025.pdf"
P3_24_URL = "https://monzo.com/docs/monzo-pillar-3-2024.pdf"
P3_23_URL = "https://monzo.com/docs/monzo-pillar-3-2023.pdf"
P3_22_URL = "https://monzo.com/static/docs/monzo-pillar-3-2022.pdf"
P3_21_URL = "https://monzo.com/static/docs/monzo-pillar-3-2021.pdf"
P3_20_URL = "https://monzo.com/documents/pillar_3_2020.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: FY2025 and FY2024 (marked MBHG) are Monzo Bank Holding Group Limited, the new parent company "
    "formed April 2023 - a broader consolidation scope than Monzo Bank Limited (MBL), which includes MBL plus "
    "(from FY2025) additional EU/US subsidiaries. FY2018-FY2023 (marked MBL) are Monzo Bank Limited, the entity on "
    "the PRA register (company no. 09446231). Monzo Bank Limited continued filing its own standalone accounts through FY2025, but that "
    "filing was only available as a scanned, non-text Companies House filing and could not be extracted; MBHG's "
    "figures were used for FY2024/25 instead as the only cleanly-extractable source, per user direction. FY2018-FY2020's "
    "MBL statutory accounts (also scanned Companies House filings, plus FY2020 was additionally cross-checked "
    "against Monzo's own website-hosted copy) were read page-by-page as images rather than machine-extracted. "
    "Also note: Monzo changed its financial year end from 28 February to 31 March starting FY2024, making FY2024 "
    "a 13-month period (1 March 2023 - 31 March 2024) rather than 12 months - it is not directly run-rate "
    "comparable to the other four years."
)

FLOOR_NOTE = (
    "HISTORICAL FLOOR NOTE (HD-024, 2026-09-06): the same company (09446231) was incorporated 18 Feb 2015 but "
    "traded as a pre-launch shell ('Focus FS Limited', then other names) with no banking licence and no deposits "
    "or loans on its balance sheet through the period ended 29 Feb 2016 and the year ended 28 Feb 2017 (that "
    "FY2016 accounts show total assets of only GBP568k, no interest income, no customer deposits, no loans - not "
    "a real operating bank year; FY2017's accounts likewise show GBP0 customer deposits and GBP0 loans, "
    "confirmed by the FY2018 Annual Report's own comparative column). Monzo received its restricted UK banking "
    "licence in August 2016 and its full/unrestricted licence in April 2017 (per the FY2018 Annual Report's "
    "audit opinion). FY2018 (year ended 28 Feb 2018) is therefore the first year with a genuine bank balance "
    "sheet (Customer deposits GBP71,276k, Loans and advances to customers GBP160k) and is used here as the real, "
    "verified floor - not FY2016 as originally guessed from GLEIF entity-creation-year grouping (which conflated "
    "the shell company's 2015 incorporation with Monzo's later start as an operating bank). No further extension "
    "before FY2018 is possible: it is the first year the company operated as a bank at all."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Monzo Group (consolidated) cash flow statement, £'000. See entity note above for "
    "MBL vs MBHG scope by year.\n"
    f"FY2025: Monzo Annual Report and Accounts 2025, p.119 (Consolidated statement of cash flows) - {AR25_URL}\n"
    f"FY2024: Monzo Bank Holding Group Limited Annual Report and Group Financial Statements 2024, p.98 "
    f"(Consolidated statement of cash flows, 13-month period ended 31 March 2024) - {AR24_URL}\n"
    f"FY2023: Monzo Bank Limited Annual Report and Accounts 2023, p.100-101 (Statement of cash flows, year ended "
    f"28 February 2023) - {AR23_URL}\n"
    f"FY2022: Monzo Bank Limited Group Annual Report 2022, p.111-112 (Statement of cash flows, year ended "
    f"28 February 2022) - {AR22_URL}\n"
    f"FY2021: Monzo Bank Limited Group Annual Report 2022, p.110-111 (Statement of cash flows, FY2021 restated "
    f"comparative, year ended 28 February 2021) - {AR22_URL}\n"
    f"FY2020: Monzo Bank Limited Group Annual Report 2020, p.98 (Statement of cash flows, Group, year ended 29 "
    f"February 2020) - {AR20_URL}\n"
    f"FY2019: Monzo Bank Limited Annual Report and Financial Statements 2019, p.54 (Statement of cash flows, "
    f"Group, year ended 28 February 2019) - {CH_FY2019_URL}\n"
    f"FY2018: Monzo Bank Limited Annual Report and Financial Statements 2018, p.26 (Statement of cash flows, "
    f"year ended 28 February 2018) - {CH_FY2018_URL}\n\n" + ENTITY_NOTE + "\n\n" + FLOOR_NOTE + "\n\n"
    "PRESENTATION NOTE: Monzo's cash flow statement format changed materially between the MBL years (FY2021-23) "
    "and the MBHG years (FY2024-25) - e.g. separate lease/subordinated-debt/treasury interest lines were combined "
    "into a single 'Net interest' line, and 'Impairment and charge-offs' became its own line. Blank cells indicate "
    "that year's report did not disclose that specific split. Section totals (net cash from operating/investing/"
    "financing, cash and cash equivalents) are consistent and comparable across all years regardless of this - "
    "hand-traced year-over-year: FY2018 close 96,943 = FY2019 open 96,943; FY2019 close 549,847 = FY2020 open "
    "549,847; FY2020 close 1,373,722 = FY2021 open 1,373,722 (already in the FY2021 column below)."
)

def p3_sources(page_25="20", page_24="29", page_23="30", page_22="32-33", page_21="12-13,20,32-33",
               table_25="Appendix 1: Key metrics - KM1 (Group)", table_24="Appendix 1: Key metrics - KM1 (Group)",
               table_23="Appendix 1: Key metrics - KM1", table_22="Appendix 1: Key metrics - KM1",
               table_21="Table E/F/K and Appendix 4 IFRS9 transitional impact"):
    return (
        "Sources (see entity note on Cash Flow Statement sheet: FY2025/24 = Monzo Bank Holding Group Limited "
        "consolidated (Group); FY2023-21 = Monzo Bank Limited, solo/Group basis as disclosed):\n"
        f"FY2025: Monzo Bank Holding Group Limited Pillar 3 Disclosures 2025, p.{page_25} ({table_25}) - {P3_25_URL}\n"
        f"FY2024: Monzo Bank Holding Group Limited Pillar 3 Disclosures 2024, p.{page_24} ({table_24}) - {P3_24_URL}\n"
        f"FY2023: Monzo Bank Limited Pillar 3 Disclosures 2023, p.{page_23} ({table_23}) - {P3_23_URL}\n"
        f"FY2022: Monzo Bank Limited Pillar 3 Disclosures 2022, p.{page_22} ({table_22}) - {P3_22_URL}\n"
        f"FY2021: Monzo Bank Limited Pillar 3 Disclosures 2021, p.{page_21} ({table_21}) - {P3_21_URL}\n"
        f"FY2020: Monzo Bank Limited Group Pillar 3 Disclosures 2020, pp.9-15, 21-28 (capital, leverage, RWA and LCR tables) - {P3_20_URL}"
    )

bw = BankWorkbook(bank_name="Monzo", years=YEARS, year_label=YEAR_LABEL, header_color="B8322A")

# ---------------------------------------------------------------
# Sheet: Balance Sheet (Consolidated Statement of Financial Position)
# ---------------------------------------------------------------
BALANCE_SHEET_PRESENTATION_NOTE = (
    "PRESENTATION NOTE: FY2021-23 (MBL) labelled the first asset line 'Cash and balances at bank' - "
    "shown here on the same 'Cash and cash equivalents' row as FY2024-25 (MBHG)'s renamed line, same "
    "underlying balance. 'Deferred tax asset' is only disclosed as its own line in FY2025. 'Collateral held "
    "with third parties' is its own line FY2021-24; FY2025's Annual Report states this was merged into "
    "'Other assets' that year (see its own footnote), so that cell is blank for FY2025 rather than a "
    "genuine zero. Called up share capital is reported as nil ('-') for FY2021-23 and FY2018-20; shown as 0 here. "
    "'Treasury investments' first appears as its own line in FY2020 (blank for FY2018-19, genuinely not yet a "
    "product Monzo held). 'Collateral held with third parties' first appears in FY2019 (blank for FY2018, before "
    "the product existed on balance sheet). 'Intangible assets' is only its own line in FY2018 (GBP14k) - folded "
    "into 'Other assets' in every later year. Total assets / Total liabilities / Total equity / Total "
    "liabilities and equity are consistent and comparable across all 8 years regardless of the above.\n\n"
    "TREASURY INVESTMENTS BREAKDOWN NOTE: 'Total treasury investments' (renamed from 'Treasury investments' "
    "so it reads unambiguously as an aggregate) is broken down by both measurement basis and issuer type using "
    "Note 12 'Treasury investments' (Note 11 in the FY2020 Annual Report) in each year's Annual Report - both "
    "splits are sourced from that note's table, not estimated. Measurement basis: FY2020-24 were disclosed "
    "entirely 'at amortised cost' (0 FVOCI/FVTPL each year - a genuine zero, not a missing figure); FY2025 is "
    "the first year Monzo also holds treasury investments at FVOCI and at FVTPL, per the FY2025 Annual Report's "
    "three-way split. Issuer type: 'UK government bonds (Gilts)' sums each year's UK Government debt line "
    "(across whichever measurement-basis sub-tables it appears in); 'other securities' sums every remaining "
    "line in the note (supranational debt, covered bonds, asset-backed securities, certificates of deposit, "
    "commercial paper, fixed term deposits) - see the per-year note breakdown in each row for the underlying "
    "components. Both breakdowns reconcile exactly to 'Total treasury investments' for all 6 years."
)

BALANCE_SHEET_SOURCES = (
    "Sources - all figures are Monzo Group (consolidated) statement of financial position, £'000. See "
    "entity note on the Cash Flow Statement sheet for MBL vs MBHG scope by year.\n"
    f"FY2025: Monzo Annual Report and Accounts 2025, p.117 (Consolidated statement of financial position) - {AR25_URL}\n"
    f"FY2024: Monzo Bank Holding Group Limited Annual Report and Group Financial Statements 2024, p.96 "
    f"(Consolidated statement of financial position, as at 31 March 2024) - {AR24_URL}\n"
    f"FY2023: Monzo Bank Limited Annual Report and Accounts 2023, p.97 (Statement of financial position, "
    f"Group, as at 28 February 2023) - {AR23_URL}\n"
    f"FY2022: Monzo Bank Limited Group Annual Report 2022, p.106 (Statement of financial position, Group, "
    f"restated, as at 28 February 2022) - {AR22_URL}\n"
    f"FY2021: Monzo Bank Limited Group Annual Report 2022, p.106 (Statement of financial position, Group, "
    f"restated comparative, as at 28 February 2021) - {AR22_URL}\n"
    f"FY2020: Monzo Bank Limited Group Annual Report 2020, p.94 (Statement of financial position, Group, as at "
    f"29 February 2020) - {AR20_URL}\n"
    "\nTreasury investments breakdown rows (measurement basis and UK government vs other securities) sourced "
    "from Note 12 'Treasury investments' (Note 11 for FY2020), Group column, £'000:\n"
    f"FY2025: Monzo Annual Report and Accounts 2025, p.136 (Note 12: Treasury investments) - {AR25_URL}\n"
    f"FY2024: Monzo Bank Holding Group Limited Annual Report and Group Financial Statements 2024, p.114 "
    f"(Note 12: Treasury investments) - {AR24_URL}\n"
    f"FY2023: Monzo Bank Limited Annual Report and Accounts 2023, p.118 (Note 12: Treasury investments) - {AR23_URL}\n"
    f"FY2022: Monzo Bank Limited Group Annual Report 2022, p.129 (Note 12: Treasury investments) - {AR22_URL}\n"
    f"FY2021: Monzo Bank Limited Group Annual Report 2022, p.129 (Note 12: Treasury investments, comparative "
    f"column) - {AR22_URL}\n"
    f"FY2020: Monzo Bank Limited Group Annual Report 2020, p.115 (Note 11: Treasury investments) - {AR20_URL}\n"
    f"FY2019: Monzo Bank Limited Annual Report and Financial Statements 2019, p.50 (Statement of financial "
    f"position, Group, as at 28 February 2019) - {CH_FY2019_URL}\n"
    f"FY2018: Monzo Bank Limited Annual Report and Financial Statements 2018, p.24 (Statement of financial "
    f"position, as at 28 February 2018) - {CH_FY2018_URL}\n\n" + ENTITY_NOTE + "\n\n" + FLOOR_NOTE + "\n\n"
    + BALANCE_SHEET_PRESENTATION_NOTE
)

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents", {"FY2025": 11021763, "FY2024": 7624300, "FY2023": 3101242, "FY2022": 3134540, "FY2021": 2977368, "FY2020": 1373722, "FY2019": 549847, "FY2018": 96943}),
    ("DATA", "Total treasury investments", {"FY2025": 5381870, "FY2024": 3634401, "FY2023": 2727520, "FY2022": 1675478, "FY2021": 376641, "FY2020": 98953}),
    ("DATA", "Treasury investments at amortised cost", {"FY2025": 2188961, "FY2024": 3634401, "FY2023": 2727520, "FY2022": 1675478, "FY2021": 376641, "FY2020": 98953}),
    ("DATA", "Treasury investments at FVOCI (fair value through other comprehensive income)", {"FY2025": 596586, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0, "FY2020": 0}),
    ("DATA", "Treasury investments at FVTPL (fair value through profit or loss)", {"FY2025": 2596323, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0, "FY2020": 0}),
    ("DATA", "Treasury investments - UK government bonds (Gilts)", {"FY2025": 2142409, "FY2024": 1068284, "FY2023": 931051, "FY2022": 857717, "FY2021": 0, "FY2020": 98953}),
    ("DATA", "Treasury investments - other securities (supranational debt, covered bonds, ABS, certificates of deposit, commercial paper, fixed term deposits)", {"FY2025": 3239461, "FY2024": 2566117, "FY2023": 1796469, "FY2022": 817761, "FY2021": 376641, "FY2020": 0}),
    ("DATA", "Loans and advances to customers", {"FY2025": 1602470, "FY2024": 1190215, "FY2023": 653733, "FY2022": 235083, "FY2021": 87147, "FY2020": 123913, "FY2019": 16054, "FY2018": 160}),
    ("DATA", "Other assets", {"FY2025": 186290, "FY2024": 411228, "FY2023": 113495, "FY2022": 75200, "FY2021": 105642, "FY2020": 87925, "FY2019": 29434, "FY2018": 41880}),
    ("DATA", "Collateral held with third parties", {"FY2024": 78506, "FY2023": 76461, "FY2022": 76292, "FY2021": 56314, "FY2020": 15642, "FY2019": 16777}),
    ("DATA", "Current tax asset", {"FY2025": 10279, "FY2024": 7089}),
    ("DATA", "Deferred tax asset", {"FY2025": 45788}),
    ("DATA", "Intangible assets", {"FY2018": 14}),
    ("DATA", "Property, plant and equipment", {"FY2025": 15391, "FY2024": 20074, "FY2023": 15325, "FY2022": 21836, "FY2021": 26595, "FY2020": 21253, "FY2019": 2278, "FY2018": 823}),
    ("TOTAL", "Total assets", {"FY2025": 18263851, "FY2024": 12965813, "FY2023": 6687776, "FY2022": 5218429, "FY2021": 3629707, "FY2020": 1721408, "FY2019": 614390, "FY2018": 139820}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer deposits", {"FY2025": 16599371, "FY2024": 11197622, "FY2023": 5945947, "FY2022": 4440650, "FY2021": 3124046, "FY2020": 1392517, "FY2019": 461821, "FY2018": 71276}),
    ("DATA", "Subordinated debt liability", {"FY2025": 15421, "FY2024": 15113, "FY2023": 14823, "FY2022": 14593}),
    ("DATA", "Other liabilities", {"FY2025": 436116, "FY2024": 890933, "FY2023": 251356, "FY2022": 200918, "FY2021": 283767, "FY2020": 199887, "FY2019": 36899, "FY2018": 12365}),
    ("TOTAL", "Total liabilities", {"FY2025": 17050908, "FY2024": 12103668, "FY2023": 6212126, "FY2022": 4656161, "FY2021": 3407813, "FY2020": 1592404, "FY2019": 498720, "FY2018": 83641}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 238, "FY2024": 217, "FY2023": 0, "FY2022": 0, "FY2021": 0, "FY2020": 0, "FY2019": 0, "FY2018": 0}),
    ("DATA", "Share premium account", {"FY2025": 501730, "FY2024": 339388, "FY2023": 944786, "FY2022": 944486, "FY2021": 508478, "FY2020": 311139, "FY2019": 198146, "FY2018": 93989}),
    ("DATA", "Other reserves", {"FY2025": 1013604, "FY2024": 966947, "FY2023": 108117, "FY2022": 79186, "FY2021": 56459, "FY2020": 17301, "FY2019": 3164, "FY2018": 871}),
    ("DATA", "Accumulated losses", {"FY2025": -302629, "FY2024": -444407, "FY2023": -577253, "FY2022": -461404, "FY2021": -343043, "FY2020": -199436, "FY2019": -85640, "FY2018": -38681}),
    ("TOTAL", "Total equity", {"FY2025": 1212943, "FY2024": 862145, "FY2023": 475650, "FY2022": 562268, "FY2021": 221894, "FY2020": 129004, "FY2019": 115670, "FY2018": 56179}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 18263851, "FY2024": 12965813, "FY2023": 6687776, "FY2022": 5218429, "FY2021": 3629707, "FY2020": 1721408, "FY2019": 614390, "FY2018": 139820}),
]

bw.add_balance_sheet_sheet(
    title="Monzo — Consolidated Statement of Financial Position",
    subtitle="Monzo Group (consolidated basis), £'000. See entity note on the Cash Flow Statement sheet.",
    rows=balance_sheet_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=42,
    source_height=110,
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss (Consolidated Statement of Comprehensive Income)
# ---------------------------------------------------------------
INCOME_STATEMENT_PRESENTATION_NOTE = (
    "PRESENTATION NOTE: Monzo's income statement structure changed materially between the MBL years "
    "(FY2021-23), which build to 'Net interest income' / 'Net fee and commission income' / 'Net operating "
    "income' subtotals, and the MBHG years (FY2024-25), which instead build to 'Revenue' / 'Cost of Revenue' "
    "/ 'Gross Profit'. Blank cells indicate that year's report did not disclose that specific line at that "
    "granularity. FY2023 disclosed no separate 'Profit before tax' / 'Taxation' split (tax was nil that "
    "year) and no in-table other-comprehensive-income breakout (only a footnote); FY2022 and FY2021 "
    "likewise disclosed no in-table OCI breakout. FY2018-20 (MBL's earliest standalone accounts) never "
    "disclosed an in-table OCI breakout either (no OCI existed - 'Total comprehensive loss' equals 'Loss "
    "for the year' exactly in all three). FY2018's own statement has no 'Net interest income' subtotal row at "
    "all (interest income was immaterial pre-overdraft-launch); FY2018's impairment line was labelled 'Credit "
    "impairment charges' (IAS 39 basis) rather than 'Credit loss expense on financial assets' (IFRS 9 basis, "
    "adopted from FY2019) - both are shown on the same row here as the same underlying concept. "
    "'Profit/(Loss) for the year' and 'Total comprehensive "
    "income/(loss) for the year, net of tax' are consistent and comparable across all 8 years regardless "
    "of the above."
)

INCOME_STATEMENT_SOURCES = (
    "Sources - all figures are Monzo Group (consolidated) statement of comprehensive income, £'000. See "
    "entity note on the Cash Flow Statement sheet for MBL vs MBHG scope by year.\n"
    f"FY2025: Monzo Annual Report and Accounts 2025, p.116 (Consolidated statement of comprehensive income) - {AR25_URL}\n"
    f"FY2024: Monzo Bank Holding Group Limited Annual Report and Group Financial Statements 2024, p.95 "
    f"(Consolidated statement of comprehensive income, 13-month period ended 31 March 2024) - {AR24_URL}\n"
    f"FY2023: Monzo Bank Limited Annual Report and Accounts 2023, p.96 (Statement of comprehensive income, "
    f"Group, year ended 28 February 2023) - {AR23_URL}\n"
    f"FY2022: Monzo Bank Limited Group Annual Report 2022, p.104 (Statement of comprehensive income, Group, "
    f"restated, year ended 28 February 2022) - {AR22_URL}\n"
    f"FY2021: Monzo Bank Limited Group Annual Report 2022, p.104 (Statement of comprehensive income, Group, "
    f"restated comparative, year ended 28 February 2021) - {AR22_URL}\n"
    f"FY2020: Monzo Bank Limited Group Annual Report 2020, p.92 (Statement of comprehensive income, Group, "
    f"year ended 29 February 2020) - {AR20_URL}\n"
    f"FY2019: Monzo Bank Limited Annual Report and Financial Statements 2019, p.48 (Statement of comprehensive "
    f"income, Group, year ended 28 February 2019) - {CH_FY2019_URL}\n"
    f"FY2018: Monzo Bank Limited Annual Report and Financial Statements 2018, p.23 (Statement of comprehensive "
    f"income, year ended 28 February 2018) - {CH_FY2018_URL}\n\n" + ENTITY_NOTE + "\n\n" + FLOOR_NOTE + "\n\n"
    + INCOME_STATEMENT_PRESENTATION_NOTE
)

income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 861673, "FY2024": 575974, "FY2023": 167956, "FY2022": 37809, "FY2021": 23950, "FY2020": 25018, "FY2019": 4918, "FY2018": 150}),
    ("DATA", "Interest expense", {"FY2025": -262833, "FY2024": -138002, "FY2023": -3709, "FY2022": -3727, "FY2021": -1564, "FY2020": -589}),
    ("TOTAL", "Net interest income", {"FY2024": 437972, "FY2023": 164247, "FY2022": 34082, "FY2021": 22386, "FY2020": 24429, "FY2019": 4918}),
    ("DATA", "Fee and commission income", {"FY2025": 329165, "FY2024": 255531, "FY2023": 169095, "FY2022": 103270, "FY2021": 54051, "FY2020": 40085, "FY2019": 13231, "FY2018": 2201}),
    ("DATA", "Fee and commission expense", {"FY2025": -72000, "FY2024": -50696, "FY2023": -36212, "FY2022": -22481, "FY2021": -12265, "FY2020": -10681, "FY2019": -6664, "FY2018": -834}),
    ("TOTAL", "Net fee and commission income", {"FY2024": 204835, "FY2023": 132883, "FY2022": 80789, "FY2021": 41786, "FY2020": 29404, "FY2019": 6567, "FY2018": 1367}),
    ("DATA", "Other operating income", {"FY2025": 44517, "FY2024": 48452, "FY2023": 18582, "FY2022": 13161, "FY2021": 2490, "FY2020": 2079, "FY2019": 1553, "FY2018": 309}),
    ("DATA", "Total Revenue", {"FY2025": 1235355}),
    ("DATA", "Credit loss expense on financial assets", {"FY2025": -152595, "FY2024": -176868, "FY2023": -101203, "FY2022": -14013, "FY2021": -3821, "FY2020": -20254, "FY2019": -3880, "FY2018": -12}),
    ("DATA", "Cost of Revenue", {"FY2025": -487428}),
    ("DATA", "Gross Profit", {"FY2025": 747927}),
    ("TOTAL", "Net operating income", {"FY2024": 514391, "FY2023": 214509, "FY2022": 114019, "FY2021": 62841, "FY2020": 35658, "FY2019": 9158, "FY2018": 1814}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Personnel expense", {"FY2025": -352929, "FY2024": -256913, "FY2023": -175325, "FY2022": -130151, "FY2021": -105269, "FY2020": -77486, "FY2019": -25654, "FY2018": -9214}),
    ("DATA", "Depreciation & impairment expense", {"FY2023": -7601, "FY2022": -8311, "FY2021": -9010, "FY2020": -3210, "FY2019": -799, "FY2018": -250}),
    ("DATA", "Other operating expense", {"FY2025": -334520, "FY2024": -242080, "FY2023": -147342, "FY2022": -94405, "FY2021": -79977, "FY2020": -70372, "FY2019": -33421, "FY2018": -25426}),
    ("TOTAL", "Total operating expense", {"FY2025": -687449, "FY2024": -498993, "FY2023": -330268, "FY2022": -232867, "FY2021": -194256, "FY2020": -151068, "FY2019": -59874, "FY2018": -34890}),
    ("DATA", "Exchange differences through profit or loss", {"FY2024": 50, "FY2023": -582, "FY2022": -172, "FY2021": 35, "FY2020": -61}),
    ("TOTAL", "Profit/(Loss) before tax", {"FY2025": 60478, "FY2024": 15448, "FY2022": -119020, "FY2021": -131380, "FY2020": -115471, "FY2019": -50716, "FY2018": -33076}),
    ("DATA", "Taxation credit/(expense)", {"FY2025": 34090, "FY2024": -6739, "FY2022": 0, "FY2021": 303, "FY2020": 1655, "FY2019": 3552, "FY2018": 2530}),
    ("TOTAL", "Profit/(Loss) for the year", {"FY2025": 94568, "FY2024": 8709, "FY2023": -116341, "FY2022": -119020, "FY2021": -131077, "FY2020": -113816, "FY2019": -47164, "FY2018": -30546}),
    ("SECTION", "Other comprehensive income that may be recycled to profit or loss", {}),
    ("DATA", "Currency translation differences", {"FY2025": -159, "FY2024": -305}),
    ("DATA", "Cash flow hedging reserve: net gains from changes in fair value", {"FY2025": 5524, "FY2024": 1391}),
    ("DATA", "Cash flow hedging reserve: net losses/(gains) transferred to net profit", {"FY2025": 180, "FY2024": -71}),
    ("DATA", "Cash flow hedging reserve: tax", {"FY2025": -1637, "FY2024": -330}),
    ("DATA", "Financial assets reserve: net changes in FVOCI financial assets", {"FY2025": 598}),
    ("DATA", "Financial assets reserve: tax", {"FY2025": -167}),
    ("TOTAL", "Other comprehensive income that may be recycled to profit or loss", {"FY2025": 4339, "FY2024": 685}),
    ("TOTAL", "Total comprehensive income/(loss) for the year, net of tax", {"FY2025": 98907, "FY2024": 9394, "FY2023": -116341, "FY2022": -119020, "FY2021": -131077, "FY2020": -113816, "FY2019": -47164, "FY2018": -30546}),
]

bw.add_income_statement_sheet(
    title="Monzo — Consolidated Statement of Comprehensive Income",
    subtitle="Monzo Group (consolidated basis), £'000. See entity note on the Cash Flow Statement sheet.",
    rows=income_statement_rows,
    sources_text=INCOME_STATEMENT_SOURCES,
    first_col_width=52,
    source_height=120,
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
EQUITY_CHANGES_PRESENTATION_NOTE = (
    "PRESENTATION NOTE: Read chronologically top-to-bottom (oldest to newest), not year-columned like "
    "every other sheet - each 'Balance as at ...' row (bold) opens/closes one year's block of movements. "
    "'Merger reserve' only exists from the FY2024 group reorganisation onward (blank for FY2021-23). This "
    "sheet's 'Other reserves' + 'Merger reserve' columns sum exactly to the Balance Sheet sheet's combined "
    "'Other reserves' line for FY2024/FY2025 (e.g. FY2025: 68,791 + 944,813 = 1,013,604) - confirms both "
    "sheets tie together. "
    "DISCREPANCY IN MONZO'S OWN REPORTING: the Profit & Loss sheet's FY2023 'Total comprehensive "
    "income/(loss) for the year, net of tax' is -116,341 (per the Statement of Comprehensive Income face "
    "table, which shows no separate OCI line for FY2023 despite a footnote mentioning £0.3m of currency "
    "translation differences). This sheet's FY2023 'Total comprehensive income/(loss) for the year' is "
    "-116,015 (per the Statement of Changes in Equity, which does show a +326 Other reserves movement for "
    "that £0.3m). Both figures are transcribed exactly as each of Monzo's own statements presents them - "
    "the -326 difference is Monzo's own inter-statement inconsistency, not a transcription error here."
)

EQUITY_CHANGES_SOURCES = (
    "Sources - all figures are Monzo Group (consolidated) statement of changes in equity, £'000. See "
    "entity note on the Cash Flow Statement sheet for MBL vs MBHG scope by year.\n"
    f"FY2025 (movements + balances at 31 March 2025 and 1 April 2024): Monzo Annual Report and Accounts "
    f"2026, p.122 (Consolidated statement of changes in equity) - {AR26_URL}\n"
    f"FY2024 (movements + balances at 31 March 2024 and 1 March 2022): Monzo Bank Holding Group Limited "
    f"Annual Report and Group Financial Statements 2024, p.97 (Consolidated statement of changes in "
    f"equity, 13-month period ended 31 March 2024) - {AR24_URL}\n"
    f"FY2023 (movements + balance at 28 February 2023, cross-checked against AR2024 above): Monzo Bank "
    f"Limited Annual Report and Accounts 2023, p.98 (Statement of changes in equity, Group, year ended 28 "
    f"February 2023) - {AR23_URL}\n"
    f"FY2022 and FY2021 (movements + balances at 28 February 2022, 28 February 2021 restated, and 1 March "
    f"2020 restated): Monzo Bank Limited Group Annual Report 2022, p.107-108 (Statement of changes in "
    f"equity, Group, restated) - {AR22_URL}\n"
    f"FY2020 (movements + balances at 29 February 2020 and 28 February 2018): Monzo Bank Limited Group Annual "
    f"Report 2020, p.96 (Statement of changes in equity) - {AR20_URL}\n"
    f"FY2019 (movements + balances at 28 February 2019 and 28 February 2018, cross-checked against AR2020 "
    f"above): Monzo Bank Limited Annual Report and Financial Statements 2019, p.52 (Statement of changes in "
    f"equity, Group) - {CH_FY2019_URL}\n"
    f"FY2018 (movements + balance at 28 February 2018): Monzo Bank Limited Annual Report and Financial "
    f"Statements 2018, p.25 (Statement of changes in equity) - {CH_FY2018_URL}\n\n" + ENTITY_NOTE + "\n\n" + FLOOR_NOTE + "\n\n"
    + EQUITY_CHANGES_PRESENTATION_NOTE
)

EQUITY_HEADERS = ["Share capital", "Share premium", "Other reserves", "Merger reserve", "Retained losses", "Total equity"]

equity_changes_rows = [
    ("TOTAL", "Balance as at 28 February 2018", (0, 93989, 871, None, -38681, 56179)),
    ("DATA", "Shares issued", (0, 105294, None, None, None, 105294)),
    ("DATA", "Cost of issuance", (None, -1207, None, None, None, -1207)),
    ("DATA", "Share-based payments reserve", (None, None, 2511, None, None, 2511)),
    ("DATA", "Exercise of options", (0, 70, -218, None, 205, 57)),
    ("DATA", "Loss for the year (FY2019)", (None, None, None, None, -47164, -47164)),
    ("TOTAL", "Balance as at 28 February 2019", (0, 198146, 3164, None, -85640, 115670)),
    ("DATA", "Shares issued", (0, 113629, None, None, None, 113629)),
    ("DATA", "Cost of issuance", (None, -658, None, None, None, -658)),
    ("DATA", "Share-based payments reserve", (None, None, 14371, None, None, 14371)),
    ("DATA", "Cumulative translation adjustment", (None, None, -5, None, None, -5)),
    ("DATA", "Share buyback", (None, None, -209, None, None, -209)),
    ("DATA", "Exercise of options", (0, 22, -20, None, 20, 22)),
    ("DATA", "Loss for the year (FY2020)", (None, None, None, None, -113816, -113816)),
    ("TOTAL", "Balance as at 1 March 2020 (as previously reported)", (0, 311139, 17301, None, -199436, 129004)),
    ("DATA", "Prior year adjustments", (0, 0, 12536, None, -12536, 0)),
    ("TOTAL", "Restated balance as at 1 March 2020", (0, 311139, 29837, None, -211972, 129004)),
    ("DATA", "Loss for the year (FY2021, restated)", (None, None, None, None, -131077, -131077)),
    ("DATA", "Cumulative translation adjustment", (None, None, -131, None, None, -131)),
    ("TOTAL", "Total comprehensive loss for the year (FY2021, restated)", (None, None, -131, None, -131077, -131208)),
    ("DATA", "Shares issued", (None, 198019, None, None, None, 198019)),
    ("DATA", "Cost of issuance", (None, -476, None, None, None, -476)),
    ("DATA", "Share-based payments reserve (restated)", (None, None, 26550, None, None, 26550)),
    ("DATA", "Share reclassification", (None, -209, 209, None, None, 0)),
    ("DATA", "Exercise of options", (None, 5, -6, None, 6, 5)),
    ("TOTAL", "Restated balance as at 28 February 2021", (0, 508478, 56459, None, -343043, 221894)),
    ("DATA", "Loss for the year (FY2022)", (None, None, None, None, -119020, -119020)),
    ("DATA", "Cumulative translation adjustment", (None, None, -1, None, None, -1)),
    ("TOTAL", "Total comprehensive loss for the year (FY2022)", (None, None, -1, None, -119020, -119021)),
    ("DATA", "Shares issued", (None, 454585, None, None, None, 454585)),
    ("DATA", "Cost of issuance", (None, -18629, None, None, None, -18629)),
    ("DATA", "Share-based payments reserve", (None, None, 23387, None, None, 23387)),
    ("DATA", "Exercise of options", (None, 52, -659, None, 659, 52)),
    ("TOTAL", "Balance as at 28 February 2022", (0, 944486, 79186, None, -461404, 562268)),
    ("DATA", "Loss for the year (FY2023)", (None, None, None, None, -116341, -116341)),
    ("DATA", "Cumulative translation adjustment", (None, None, 326, None, None, 326)),
    ("TOTAL", "Total comprehensive income/(loss) for the year (FY2023)", (None, None, 326, None, -116341, -116015)),
    ("DATA", "Shares issued", (None, 210, None, None, None, 210)),
    ("DATA", "Cost of issuance", (None, -79, None, None, None, -79)),
    ("DATA", "Share-based payments reserve", (None, None, 29097, None, None, 29097)),
    ("DATA", "Exercise of options", (None, 169, -492, None, 492, 169)),
    ("TOTAL", "Balance as at 28 February 2023", (0, 944786, 108117, None, -577253, 475650)),
    ("DATA", "Profit for the year (FY2024)", (None, None, None, None, 8709, 8709)),
    ("DATA", "Cumulative translation adjustment", (None, None, -305, None, None, -305)),
    ("DATA", "Cash flow hedge reserve", (None, None, 990, None, None, 990)),
    ("TOTAL", "Total comprehensive income for the year (FY2024)", (None, None, 685, None, 8709, 9394)),
    ("DATA", "Shares issued", (217, 340496, None, None, None, 340713)),
    ("DATA", "Cost of issuance", (None, -1356, None, None, None, -1356)),
    ("DATA", "Share-based payments reserve", (None, None, 37469, None, None, 37469)),
    ("DATA", "Exercise of options", (None, 275, -3761, None, 3761, 275)),
    ("DATA", "Reserve reclassification", (None, None, -120376, None, 120376, 0)),
    ("DATA", "Creation of merger reserve on group reorganisation", (None, -944813, None, 944813, None, 0)),
    ("TOTAL", "Balance as at 31 March 2024", (217, 339388, 22134, 944813, -444407, 862145)),
    ("DATA", "Profit for the year (FY2025)", (None, None, None, None, 94568, 94568)),
    ("DATA", "Cumulative translation adjustment", (None, None, -159, None, None, -159)),
    ("DATA", "Cash flow hedge reserve", (None, None, 4067, None, None, 4067)),
    ("DATA", "Treasury investment fair value movements", (None, None, 431, None, None, 431)),
    ("TOTAL", "Total comprehensive income for the year (FY2025)", (None, None, 4339, None, 94568, 98907)),
    ("DATA", "Shares issued", (21, 150627, None, None, None, 150648)),
    ("DATA", "Cost of issuance", (None, -20, None, None, None, -20)),
    ("DATA", "Share-based payments reserve", (None, None, 89528, None, None, 89528)),
    ("DATA", "Exercise of options", (None, 11735, -47210, None, 47210, 11735)),
    ("TOTAL", "Balance as at 31 March 2025", (238, 501730, 68791, 944813, -302629, 1212943)),
]

bw.add_equity_changes_sheet(
    title="Monzo — Consolidated Statement of Changes in Equity",
    subtitle="Monzo Group (consolidated basis), £'000, chronological FY2018-FY2025. See entity note on the Cash Flow Statement sheet.",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQUITY_CHANGES_SOURCES,
    first_col_width=54,
    source_height=190,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit/(Loss) for the year", {"FY2025": 94568, "FY2024": 8709, "FY2023": -116341, "FY2022": -119020, "FY2021": -131077, "FY2020": -113816, "FY2019": -47164, "FY2018": -30546}),
    ("DATA", "Impairment and charge-offs", {"FY2025": 152595, "FY2024": 176868}),
    ("DATA", "Depreciation & impairment expense", {"FY2025": 4623, "FY2024": 7288, "FY2023": 7601, "FY2022": 8311, "FY2021": 9010, "FY2020": 3210, "FY2019": 799, "FY2018": 241}),
    ("DATA", "Amortisation of intangible assets", {"FY2018": 10}),
    ("DATA", "Share-based payments", {"FY2025": 83468, "FY2024": 37469, "FY2023": 29100, "FY2022": 23254, "FY2021": 26547, "FY2020": 14365, "FY2019": 2511, "FY2018": 916}),
    ("DATA", "Loss on disposals and write-offs", {"FY2023": 510, "FY2022": 495, "FY2021": 274, "FY2020": 47, "FY2019": 161}),
    ("DATA", "(Decrease)/increase in provisions", {"FY2025": 3281, "FY2024": -9830, "FY2023": 8787, "FY2022": -290, "FY2021": 8098, "FY2018": 12}),
    ("DATA", "Loss on warrants", {"FY2023": 23, "FY2022": 502}),
    ("DATA", "Net interest expense on leases", {"FY2023": 1191, "FY2022": 1690, "FY2021": 1450, "FY2020": 491}),
    ("DATA", "Interest expense on subordinated debt", {"FY2023": 2031, "FY2022": 1958}),
    ("DATA", "Interest on collateral", {"FY2023": 403}),
    ("DATA", "Interest on treasury investments", {"FY2023": -29392, "FY2022": -2381, "FY2021": -183, "FY2020": -358}),
    ("DATA", "Net interest (combined, MBHG presentation)", {"FY2025": -68155, "FY2024": -75798}),
    ("DATA", "Taxation", {"FY2025": -34090}),
    ("DATA", "Other non-cash items", {"FY2025": -7494, "FY2024": -1049}),
    ("DATA", "Movement in loans and advances to customers", {"FY2025": -564849, "FY2024": -713349, "FY2023": -418650, "FY2022": -147936, "FY2021": 36766, "FY2020": -107859, "FY2019": -15893, "FY2018": -160}),
    ("DATA", "Movement in customer deposits", {"FY2025": 5401749, "FY2024": 5251674, "FY2023": 1505297, "FY2022": 1316604, "FY2021": 1731529, "FY2020": 930696, "FY2019": 390545, "FY2018": 71276}),
    ("DATA", "Movement in other assets (excluding RDEC claim)", {"FY2023": -36597, "FY2022": 30628, "FY2021": -20379, "FY2020": -61060, "FY2019": -2329, "FY2018": -37477}),
    ("DATA", "Movement in RDEC claim receivable", {"FY2023": -1698, "FY2022": -186, "FY2021": 2662, "FY2020": 2569, "FY2019": 1242}),
    ("DATA", "Movement in other assets (combined, MBHG presentation)", {"FY2025": 312246, "FY2024": -299495}),
    ("DATA", "Movement in current tax asset/liability", {"FY2024": -7090}),
    ("DATA", "Net tax paid", {"FY2025": -6019}),
    ("DATA", "Movement in collateral held with third parties", {"FY2025": -1075, "FY2024": -63, "FY2023": -169, "FY2022": -19978, "FY2021": -40672, "FY2020": 1135, "FY2019": -3245}),
    ("DATA", "Movement in other liabilities (excl. leases/provisions, MBL) / other liabilities (MBHG)", {"FY2025": -454084, "FY2024": 644962, "FY2023": 46717, "FY2022": -77125, "FY2021": 71024, "FY2020": 145270, "FY2019": 24534, "FY2018": 11285}),
    ("TOTAL", "Net cash from operating activities", {"FY2025": 4916764, "FY2024": 5020296, "FY2023": 998813, "FY2022": 1016526, "FY2021": 1695049, "FY2020": 814690, "FY2019": 351161, "FY2018": 15557}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Purchase of treasury investments", {"FY2023": -1495059, "FY2022": -1310560, "FY2021": -420977, "FY2020": -121611}),
    ("DATA", "Interest received on treasury investments", {"FY2023": 14892, "FY2022": 5048, "FY2021": 1359, "FY2020": 41}),
    ("DATA", "Proceeds from sale and maturity of treasury investments", {"FY2023": 457517, "FY2022": 9000, "FY2021": 142112, "FY2020": 22975}),
    ("DATA", "Net movement in treasury investments (combined, MBHG presentation)", {"FY2025": -1676621, "FY2024": -829471}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -213, "FY2024": -1060, "FY2023": -3453, "FY2022": -4383, "FY2021": -8290, "FY2020": -3279, "FY2019": -2415, "FY2018": -886}),
    ("DATA", "Proceeds on disposal of property, plant and equipment", {"FY2021": 75, "FY2019": 8}),
    ("DATA", "Movement in sublease receivables", {"FY2025": 171, "FY2024": 1010}),
    ("DATA", "Cumulative translation adjustment (investing)", {"FY2020": -5}),
    ("DATA", "Other cash flows from investing activities", {"FY2021": -38}),
    ("TOTAL", "Net cash from/(used in) investing activities", {"FY2025": -1676663, "FY2024": -829521, "FY2023": -1026103, "FY2022": -1300895, "FY2021": -285759, "FY2020": -101879, "FY2019": -2407, "FY2018": -886}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Net proceeds from issuance of ordinary shares", {"FY2025": 162362, "FY2024": 339440, "FY2023": 300, "FY2022": 436008, "FY2021": 197548, "FY2020": 112993, "FY2019": 104150, "FY2018": 67398}),
    ("DATA", "Payment of interest portion of lease liabilities", {"FY2023": -1988, "FY2022": -385, "FY2021": -388, "FY2020": -165}),
    ("DATA", "Payment of principal portion of lease liabilities", {"FY2023": -3075, "FY2022": -7136, "FY2021": -2654, "FY2020": -1555}),
    ("DATA", "Payment of lease liabilities (combined, MBHG presentation)", {"FY2025": -4955, "FY2024": -7008}),
    ("DATA", "Purchase of treasury shares", {"FY2020": -209}),
    ("DATA", "Issuance of subordinated debt and warrant liability", {"FY2022": 14812}),
    ("DATA", "Interest paid on subordinated debt liability", {"FY2023": -1801, "FY2022": -1765}),
    ("TOTAL", "Net cash from/(used in) financing activities", {"FY2025": 157407, "FY2024": 332432, "FY2023": -6564, "FY2022": 441534, "FY2021": 194506, "FY2020": 111064, "FY2019": 104150, "FY2018": 67398}),
    ("DATA", "Effect of exchange rates on cash and cash equivalents", {"FY2025": -45, "FY2024": -149, "FY2023": 556, "FY2022": -150}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 3397463, "FY2024": 4523058, "FY2023": -33298, "FY2022": 157172, "FY2021": 1603646, "FY2020": 823875, "FY2019": 452904, "FY2018": 82069}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 7624300, "FY2024": 3101242, "FY2023": 3134540, "FY2022": 2977368, "FY2021": 1373722, "FY2020": 549847, "FY2019": 96943, "FY2018": 14874}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 11021763, "FY2024": 7624300, "FY2023": 3101242, "FY2022": 3134540, "FY2021": 2977368, "FY2020": 1373722, "FY2019": 549847, "FY2018": 96943}),
]

bw.add_cash_flow_sheet(
    title="Monzo — Consolidated (Group) Cash Flow Statement",
    subtitle="£'000 unless stated. FY2025/24 = Monzo Bank Holding Group Limited; FY2023-18 = Monzo Bank Limited. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=62,
    source_height=190,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality / Credit Risk Disclosures
# ---------------------------------------------------------------
ASSET_QUALITY_PRESENTATION_NOTE = (
    "PRESENTATION NOTE: 'Flex Loans' was only reported as its own product line from FY2023 onward - FY2021 "
    "and FY2022's own reports combined it into 'Loans' (blank Flex Loans cells for those years; AR2023 "
    "later restated FY2022 with the split - 130,892 Loans + 27,004 Flex Loans - matching FY2022's own "
    "combined 157,896 exactly, but this sheet keeps each year's own primary-source figures for consistency "
    "with the rest of the workbook). "
    "The 'by IFRS 9 stage' Total gross loans for FY2024 (1,394,005) differs from the 'by product' Total "
    "gross loans for FY2024 (1,394,222) by £217k - a small scope difference in Monzo's own two disclosures "
    "(Note 13 vs the impairment loss allowance movement table); both are transcribed exactly as disclosed. "
    "All other years' by-product and by-stage gross/impairment totals match exactly. "
    "Stage 1 = performing, Stage 2 = underperforming/significant increase in credit risk since origination, "
    "Stage 3 = credit-impaired (Monzo's proxy for non-performing). ECL coverage ratio = Total impairment "
    "allowance / Total gross loans (by-product total); Stage 3 (NPL) ratio and Stage 3 coverage ratio use "
    "the by-stage totals. "
    "FY2019 and FY2020 (MBL's earliest years with a material loan book) disclosed only the by-IFRS-9-stage "
    "table, not a by-product (Overdrafts/Loans/Flex Loans) split - those rows are blank for FY2019-20. FY2020's "
    "by-stage impairment-allowance total (per its own note) nets both on-balance-sheet loan impairment and "
    "off-balance-sheet undrawn-overdraft-commitment provision together (both ultimately reduce the same "
    "revolving overdraft facility), which is why FY2020's Total gross minus Total impairment allowance ties "
    "exactly to the Balance Sheet's Loans and advances to customers figure even though the 'impairment "
    "allowance' total is not a pure funded-balance ECL figure. FY2018 is not populated at all: its loan book "
    "was GBP160k (all overdrafts, first year of the product), and Monzo's own FY2019 Annual Report states "
    "FY2018 comparatives for this table 'are not presented as they are not material'; FY2018 also used IAS 39 "
    "(not IFRS 9, adopted from FY2019) for impairment, so no stage-based table exists for that year at all."
)

ASSET_QUALITY_SOURCES = (
    "Sources - all figures are Monzo Group (consolidated) Note 13 'Loans and advances to customers' and "
    "the 'Impairment loss allowance movement table', £'000. See entity note on the Cash Flow Statement "
    "sheet for MBL vs MBHG scope by year.\n"
    f"FY2025 and FY2024 (by product and by stage): Monzo Annual Report and Accounts 2025, p.137 (Note 13) "
    f"and p.167-168 (Impairment loss allowance movement table) - {AR25_URL}\n"
    f"FY2023 (by product): Monzo Bank Limited Annual Report and Accounts 2023, p.119 (Note 13) - {AR23_URL}\n"
    f"FY2023 and FY2022 and FY2021 (by stage): Monzo Bank Limited Annual Report and Accounts 2023, p.147-149 "
    f"(Impairment loss allowance movement table, 'As at 1 March 2021' / 'As at 28 February 2022' / 'As at "
    f"28 February 2023' snapshots) - {AR23_URL}\n"
    f"FY2022 (by product): Monzo Bank Limited Group Annual Report 2022, p.131 (Note 13) - {AR22_URL}\n"
    f"FY2021 (by product): Monzo Bank Limited Group Annual Report 2022, p.131 (Note 13, restated "
    f"comparative) - {AR22_URL}\n"
    f"FY2020 (by stage, 'Analysis of overdrafts and loans by stage'): Monzo Bank Limited Group Annual Report "
    f"2020, p.132 - {AR20_URL}\n"
    f"FY2019 (by stage): Monzo Bank Limited Annual Report and Financial Statements 2019, p.88 (Note 31 Credit "
    f"risk) - {CH_FY2019_URL}\n\n" + ENTITY_NOTE + "\n\n" + FLOOR_NOTE + "\n\n" + ASSET_QUALITY_PRESENTATION_NOTE
)

asset_quality_rows = [
    ("SECTION", "Gross loans and advances to customers, by product", {}),
    ("DATA", "Overdrafts and overdrawn balances", {"FY2025": 402876, "FY2024": 318960, "FY2023": 197104, "FY2022": 100911, "FY2021": 56818}),
    ("DATA", "Loans", {"FY2025": 897426, "FY2024": 683976, "FY2023": 393349, "FY2022": 157896, "FY2021": 47772}),
    ("DATA", "Flex Loans", {"FY2025": 553394, "FY2024": 391286, "FY2023": 169281}),
    ("TOTAL", "Total gross loans and advances to customers", {"FY2025": 1853696, "FY2024": 1394222, "FY2023": 759734, "FY2022": 258807, "FY2021": 104590}),
    ("SECTION", "Impairment loss allowance (ECL), by product", {}),
    ("DATA", "Overdrafts and overdrawn balances", {"FY2025": -83013, "FY2024": -61938, "FY2023": -36266, "FY2022": -15179, "FY2021": -12600}),
    ("DATA", "Loans", {"FY2025": -81429, "FY2024": -75892, "FY2023": -33247, "FY2022": -8545, "FY2021": -4843}),
    ("DATA", "Flex Loans", {"FY2025": -86784, "FY2024": -66177, "FY2023": -36488}),
    ("TOTAL", "Total impairment loss allowance", {"FY2025": -251226, "FY2024": -204007, "FY2023": -106001, "FY2022": -23724, "FY2021": -17443}),
    ("SECTION", "Net loans and advances to customers, by product", {}),
    ("DATA", "Overdrafts and overdrawn balances", {"FY2025": 319863, "FY2024": 257022, "FY2023": 160838, "FY2022": 85732, "FY2021": 44218}),
    ("DATA", "Loans", {"FY2025": 815997, "FY2024": 608084, "FY2023": 360102, "FY2022": 149351, "FY2021": 42929}),
    ("DATA", "Flex Loans", {"FY2025": 466610, "FY2024": 325109, "FY2023": 132793}),
    ("TOTAL", "Total net loans and advances to customers", {"FY2025": 1602470, "FY2024": 1190215, "FY2023": 653733, "FY2022": 235083, "FY2021": 87147}),
    ("SECTION", "Gross loans and advances to customers, by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (performing)", {"FY2025": 1347607, "FY2024": 1103258, "FY2023": 598627, "FY2022": 189761, "FY2021": 60059, "FY2020": 107480, "FY2019": 14804}),
    ("DATA", "Stage 2 (underperforming)", {"FY2025": 397399, "FY2024": 206174, "FY2023": 128104, "FY2022": 59765, "FY2021": 36901, "FY2020": 33150, "FY2019": 3293}),
    ("DATA", "Stage 3 (credit-impaired)", {"FY2025": 108690, "FY2024": 84573, "FY2023": 33003, "FY2022": 9281, "FY2021": 7630, "FY2020": 3279, "FY2019": 1076}),
    ("TOTAL", "Total gross loans and advances to customers (by stage)", {"FY2025": 1853696, "FY2024": 1394005, "FY2023": 759734, "FY2022": 258807, "FY2021": 104590, "FY2020": 143909, "FY2019": 19173}),
    ("SECTION", "Impairment loss allowance, by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (performing)", {"FY2025": -54783, "FY2024": -69167, "FY2023": -43742, "FY2022": -7855, "FY2021": -2833, "FY2020": -7399, "FY2019": -1198}),
    ("DATA", "Stage 2 (underperforming)", {"FY2025": -130326, "FY2024": -80852, "FY2023": -38022, "FY2022": -9765, "FY2021": -9341, "FY2020": -9645, "FY2019": -961}),
    ("DATA", "Stage 3 (credit-impaired)", {"FY2025": -66117, "FY2024": -53988, "FY2023": -24237, "FY2022": -6104, "FY2021": -5269, "FY2020": -2952, "FY2019": -960}),
    ("TOTAL", "Total impairment loss allowance (by stage)", {"FY2025": -251226, "FY2024": -204007, "FY2023": -106001, "FY2022": -23724, "FY2021": -17443, "FY2020": -19996, "FY2019": -3119}),
    ("SECTION", "Asset quality ratios", {}),
    ("DATA", "ECL coverage ratio (Total impairment allowance / Total gross loans)", {"FY2025": "13.55%", "FY2024": "14.63%", "FY2023": "13.95%", "FY2022": "9.17%", "FY2021": "16.68%", "FY2020": "13.89%", "FY2019": "16.27%"}),
    ("DATA", "Stage 3 (NPL) ratio (Stage 3 gross loans / Total gross loans)", {"FY2025": "5.86%", "FY2024": "6.07%", "FY2023": "4.34%", "FY2022": "3.59%", "FY2021": "7.30%", "FY2020": "2.28%", "FY2019": "5.61%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 impairment allowance / Stage 3 gross loans)", {"FY2025": "60.83%", "FY2024": "63.83%", "FY2023": "73.44%", "FY2022": "65.77%", "FY2021": "69.06%", "FY2020": "90.03%", "FY2019": "89.22%"}),
]

bw.add_asset_quality_sheet(
    title="Monzo — Asset Quality / Credit Risk Disclosures",
    subtitle="Monzo Group (consolidated basis), £'000. See entity note on the Cash Flow Statement sheet.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=62,
    source_height=170,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=46, source_height=150)

NOT_DISCLOSED_1820 = {"FY2020": "Not publicly disclosed", "FY2019": "Not publicly disclosed", "FY2018": "Not publicly disclosed"}

PRE2021_PILLAR3_NOTE = (
    "FY2018-19 (MBL's earliest years) predate this workbook's Pillar 3 report series. The FY2020 report is "
    "available at the Monzo-hosted URL cited below and supplies FY2020's full capital, RWA, leverage and LCR "
    "detail; it is included here. The only capital-adequacy figure FY2018-19 statutory accounts disclose at all is an unaudited "
    "CET1 ratio (FY2018: no capital management note exists at all - Monzo's FY2018 accounts predate any such "
    "disclosure; FY2019: 126%; FY2020: 70% - both per each year's own 'Capital management' note). No CET1 "
    "capital £ amount, Total Capital, RWA total, leverage ratio, LCR, NSFR or MREL figure is disclosed for FY2018-19."
)

metric(
    "CET1 Capital", "£'000, Group/consolidated basis (solo basis for MBL years - Monzo's subsidiaries are excluded from prudential consolidation as below UK CRR Article 19 thresholds)",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 1158302, "FY2024": 888274, "FY2023": 532582, "FY2022": 575287, "FY2021": 233604, "FY2020": 142642, **{**NOT_DISCLOSED_1820, "FY2020": 142642}})],
    p3_sources(),
    note=PRE2021_PILLAR3_NOTE,
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "55.92%", "FY2024": "54.94%", "FY2023": "54.40%", "FY2022": "155.1%", "FY2021": "99%", "FY2020": "70% (unaudited)", "FY2019": "126% (unaudited)", "FY2018": "Not publicly disclosed"})],
    p3_sources(),
    note="FY2020 and FY2019 values are each year's own unaudited CET1 ratio disclosed in its Annual Report's 'Capital "
         "management' note (not from a Pillar 3 report - see " + "the CET1 Capital sheet's note). " + PRE2021_PILLAR3_NOTE,
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2025": 1158302, "FY2024": 888274, "FY2023": 532582, "FY2022": 575287, "FY2021": 233604, "FY2020": 142642, **{**NOT_DISCLOSED_1820, "FY2020": 142642}})],
    p3_sources(),
    note="Equal to CET1 capital in every year shown - Monzo has not issued any Additional Tier 1 (AT1) instruments. " + PRE2021_PILLAR3_NOTE,
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "55.92%", "FY2024": "54.94%", "FY2023": "54.40%", "FY2022": "155.1%", "FY2021": "99%", "FY2020": "70% (unaudited)", "FY2019": "126% (unaudited)", "FY2018": "Not publicly disclosed"})],
    p3_sources(),
    note="FY2020/FY2019 shown equal to CET1 ratio (Tier 1 capital = CET1 capital in every disclosed year - see Tier "
         "1 Capital sheet); the source itself only ever uses the term 'CET1 ratio' for these two years, never "
         "'Tier 1 ratio' explicitly. " + PRE2021_PILLAR3_NOTE,
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2025": 1173723, "FY2024": 903387, "FY2023": 547407, "FY2022": 589880, "FY2021": 233604, "FY2020": 142642, **{**NOT_DISCLOSED_1820, "FY2020": 142642}})],
    p3_sources(),
    note=PRE2021_PILLAR3_NOTE,
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "56.67%", "FY2024": "55.87%", "FY2023": "55.91%", "FY2022": "159.1%", "FY2021": "99%", **NOT_DISCLOSED_1820})],
    p3_sources(),
    note=PRE2021_PILLAR3_NOTE,
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted exposure amount", {"FY2025": 2071182, "FY2024": 1616928, "FY2023": 979042, "FY2022": 370849, "FY2021": 236653, "FY2020": 202708, **{**NOT_DISCLOSED_1820, "FY2020": 202708}})],
    p3_sources(),
    note=PRE2021_PILLAR3_NOTE,
)

# ---------------------------------------------------------------
# Sheet: RWA Breakdown (Pillar 3's UK OV1 template - placed next to
# Total RWAs, since it's itself a Pillar 3 disclosure)
# ---------------------------------------------------------------
RWA_BREAKDOWN_PRESENTATION_NOTE = (
    "PRESENTATION NOTE: Transcribed from each year's own UK OV1 'Overview of risk weighted exposure "
    "amounts' template. FY2021 has no OV1 template of its own (too early in Monzo's disclosure history) - "
    "its figures are the FY2022 report's own comparative column instead, same per-year-primary-source "
    "convention used throughout this workbook. '-' in the source table means a genuinely disclosed nil "
    "exposure (written as 0 here), not 'not disclosed' - contrast with the Statement of Changes in Equity/"
    "Balance Sheet/P&L sheets' convention where a blank cell means the source didn't disclose that line at "
    "all. 'Of which' sub-rows are only shown where they differ from their parent row (e.g. Monzo only ever "
    "uses the standardised approach for credit risk and the basic indicator approach for operational risk, "
    "so those redundant 'of which' lines are omitted). This sheet's Total row ties out exactly to the "
    "Total RWAs sheet for all years with data. FY2018-19 are blank throughout - no Pillar 3/OV1 disclosure "
    "exists for those years (see the CET1 Capital sheet's note); this is a genuine 'not disclosed', not the "
    "sheet's own 'disclosed nil' convention."
)

RWA_BREAKDOWN_SOURCES = (
    "Sources (see entity note on Cash Flow Statement sheet: FY2025/24 = Monzo Bank Holding Group Limited "
    "consolidated (Group); FY2023-21 = Monzo Bank Limited (Bank)):\n"
    f"FY2025: Monzo Bank Holding Group Limited Pillar 3 Disclosures 2025, p.24 (Appendix 4 - Overview of "
    f"risk weighted exposure amounts - OV1) - {P3_25_URL}\n"
    f"FY2024: Monzo Bank Holding Group Limited Pillar 3 Disclosures 2024, p.43 (Appendix 7 - Overview of "
    f"risk weighted exposure amounts - OV1) - {P3_24_URL}\n"
    f"FY2023: Monzo Bank Limited Pillar 3 Disclosures 2023, p.40 (Appendix 7 - Overview of risk weighted "
    f"exposure amounts - OV1) - {P3_23_URL}\n"
    f"FY2022: Monzo Bank Limited Pillar 3 Disclosures 2022, p.47-48 (Appendix 7 - Overview of risk weighted "
    f"exposure amounts - OV1) - {P3_22_URL}\n"
    f"FY2021: Monzo Bank Limited Pillar 3 Disclosures 2022, p.47-48 (Appendix 7 - Overview of risk weighted "
    f"exposure amounts - OV1, FY2021 comparative column) - {P3_22_URL}\n"
    f"FY2020: Monzo Bank Limited Group Pillar 3 Disclosures 2020, p.11 (Table d: RWAs) - {P3_20_URL}\n\n" + RWA_BREAKDOWN_PRESENTATION_NOTE
)

rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 1336768, "FY2024": 1290471, "FY2023": 821178, "FY2022": 285793, "FY2021": 151226, "FY2020": 157594}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 1031, "FY2024": 7052, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "  of which exposures to a CCP", {"FY2025": 1031}),
    ("DATA", "  of which credit valuation adjustment (CVA)", {"FY2024": 4371}),
    ("DATA", "  of which other CCR", {"FY2024": 2681}),
    ("DATA", "Securitisation exposures (non-trading book, after the cap)", {"FY2025": 48405, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "  of which SEC-ERBA (including IAA)", {"FY2025": 28426}),
    ("DATA", "  of which SEC-SA approach", {"FY2025": 19979}),
    ("DATA", "Market risk (position, FX and commodities risks)", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Operational risk", {"FY2025": 684978, "FY2024": 319405, "FY2023": 157864, "FY2022": 85056, "FY2021": 85427, "FY2020": 45114}),
    ("DATA", "Amounts below thresholds for deduction (subject to 250% risk weight, for information)", {"FY2025": 0, "FY2024": 8688, "FY2023": 5797, "FY2022": 0, "FY2021": 0}),
    ("TOTAL", "Total risk-weighted exposure amount (RWEAs)", {"FY2025": 2071182, "FY2024": 1616928, "FY2023": 979042, "FY2022": 370849, "FY2021": 236653, "FY2020": 202708}),
]

bw.add_rwa_breakdown_sheet(
    title="Monzo — RWA Breakdown (UK OV1: Overview of Risk Weighted Exposure Amounts)",
    subtitle="Consolidated/Bank basis by year (see entity note on Cash Flow Statement sheet), £'000",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=58,
    source_height=140,
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Total exposure measure excluding claims on central banks", {"FY2025": 7459493, "FY2024": 5550297, "FY2023": 3763096, "FY2021": 796590, "FY2020": 1764243}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "15.53%", "FY2024": "16.00%", "FY2023": "14.15%", "FY2021": "29.3%", "FY2020": "8.1%", **{**NOT_DISCLOSED_1820, "FY2020": "8.1%"}}),
        ("Leverage ratio total exposure measure - 2022 KM1 format, basis not specified in source", {"FY2022": 2238857}),
        ("Leverage ratio (%) - 2022 KM1 format, basis not specified in source", {"FY2022": "25.7%"}),
        ("Total exposure measure including claims on central banks (CRR basis, retired from FY2022)", {"FY2021": 3667694}),
        ("Leverage ratio including claims on central banks (%) (CRR basis, retired from FY2022)", {"FY2021": "6.4%"}),
    ],
    p3_sources(),
    note="Leverage ratio terminology changed across these reports. FY2021 disclosed both a UK ratio (excluding central "
         "bank claims) and a CRR ratio (including them); the CRR ratio was retired PRA-wide from FY2022 onward "
         "('The CRR leverage ratio will no longer apply for UK banks' - FY2022 Pillar 3 report). FY2022's KM1 table "
         "shows a single unlabelled 'Leverage ratio' whose exact basis is not stated in the source document, so it is "
         "kept on its own row rather than assumed to match the 'excluding central banks' series. FY2023 onward "
         "explicitly reintroduced 'excluding claims on central banks' labelling, matching the convention used for "
         "Barclays. Monzo is not currently subject to a binding leverage ratio requirement (below the size threshold). "
         + PRE2021_PILLAR3_NOTE,
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets / liquidity buffer (weighted value)", {"FY2025": 13124870, "FY2024": 7651328, "FY2023": 5103316, "FY2022": 4600376, "FY2021": 3212266, "FY2020": 1415419}),
        ("Total net cash outflows (adjusted value)", {"FY2025": 1133118, "FY2024": 1070436, "FY2023": 671159, "FY2022": 428980, "FY2021": 355375, "FY2020": 183675}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "1,178.76%", "FY2024": "724.51%", "FY2023": "760.4%", "FY2022": "1,072.4%", "FY2021": "904%", "FY2020": "771%", **{**NOT_DISCLOSED_1820, "FY2020": "771%"}}),
    ],
    p3_sources(),
    note="FY2020 uses Monzo's own Pillar 3 Table i (liquidity buffer / net outflows); FY2021 used a simpler 'Table K: LCR' disclosure (liquidity buffer / net cash outflows) rather than the full "
         "KM1 template used from FY2022 onward; the two are conceptually equivalent to the HQLA/net cash outflow rows "
         "used in later years. FY2018-19's Annual Reports each only say liquidity 'was significantly in excess of all "
         "liquidity targets' throughout the year, with no numeric LCR disclosed. " + PRE2021_PILLAR3_NOTE,
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding", {"FY2025": 14543697, "FY2024": 9139028, "FY2023": 6055616, "FY2022": 4703076}),
        ("Total required stable funding", {"FY2025": 1807551, "FY2024": 1345619, "FY2023": 835938, "FY2022": 444598}),
        ("Net Stable Funding Ratio (%)", {"FY2025": "843.98%", "FY2024": "680.81%", "FY2023": "724.4%", "FY2022": "1,057.8%", "FY2021": "Not disclosed", **NOT_DISCLOSED_1820}),
    ],
    p3_sources(),
    note="NSFR was not disclosed in Monzo's FY2021 Pillar 3 report (no NSFR table or mention present); it first "
         "appears from the FY2022 report onward. " + PRE2021_PILLAR3_NOTE,
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not disclosed (ratio)" for y in YEARS if y not in ("FY2020", "FY2019", "FY2018")} | NOT_DISCLOSED_1820)],
    p3_sources(),
    note="Unlike Barclays Bank UK PLC, Monzo IS subject to its own MREL requirement (preferred resolution strategy: "
         "partial transfer) - but no Pillar 3 report in this series discloses a numeric MREL ratio or MREL resources "
         "figure, only the qualitative target. As disclosed: an indicative interim MREL requirement was set from "
         "April 2021 (updated April 2022, then April 2023), with an end-state requirement effective from April 2024/25 "
         "of 1.3x Total Capital Requirement (TCR) - reduced from earlier guidance of 2.0x TCR (per the FY2023 report). "
         "FY2018-20 predate any MREL requirement being set for Monzo at all. " + PRE2021_PILLAR3_NOTE,
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 18263851, "FY2024": 12965813, "FY2023": 6687776, "FY2022": 5218429, "FY2021": 3629707, "FY2020": 1721408, "FY2019": 614390, "FY2018": 139820}),
        ("Loans and advances to customers", {"FY2025": 1602470, "FY2024": 1190215, "FY2023": 653733, "FY2022": 235083, "FY2021": 87147, "FY2020": 123913, "FY2019": 16054, "FY2018": 160}),
        ("Customer deposits", {"FY2025": 16599371, "FY2024": 11197622, "FY2023": 5945947, "FY2022": 4440650, "FY2021": 3124046, "FY2020": 1392517, "FY2019": 461821, "FY2018": 71276}),
        ("Total equity", {"FY2025": 1212943, "FY2024": 862145, "FY2023": 475650, "FY2022": 562268, "FY2021": 221894, "FY2020": 129004, "FY2019": 115670, "FY2018": 56179}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Revenue / Net operating income", {"FY2025": 747927, "FY2024": 514391, "FY2023": 214509, "FY2022": 114019, "FY2021": 62841, "FY2020": 35658, "FY2019": 9158, "FY2018": 1814}),
        ("Total operating expense", {"FY2025": -687449, "FY2024": -498993, "FY2023": -330268, "FY2022": -232867, "FY2021": -194256, "FY2020": -151068, "FY2019": -59874, "FY2018": -34890}),
        ("Profit/(Loss) for the year", {"FY2025": 94568, "FY2024": 8709, "FY2023": -116341, "FY2022": -119020, "FY2021": -131077, "FY2020": -113816, "FY2019": -47164, "FY2018": -30546}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 862145, "FY2024": 475650, "FY2023": 562268, "FY2022": 221894, "FY2021": 129004, "FY2020": 115670, "FY2019": 56179}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": 98907, "FY2024": 9394, "FY2023": -116015, "FY2022": -119021, "FY2021": -131208, "FY2020": -113816, "FY2019": -47164, "FY2018": -30546}),
        ("Other equity movements, net", {"FY2025": 251891, "FY2024": 377101, "FY2023": 29397, "FY2022": 459395, "FY2021": 224098, "FY2020": 127150, "FY2019": 106655, "FY2018": 68327}),
        ("Closing equity", {"FY2025": 1212943, "FY2024": 862145, "FY2023": 475650, "FY2022": 562268, "FY2021": 221894, "FY2020": 129004, "FY2019": 115670, "FY2018": 56179}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from operating activities", {"FY2025": 4916764, "FY2024": 5020296, "FY2023": 998813, "FY2022": 1016526, "FY2021": 1695049, "FY2020": 814690, "FY2019": 351161, "FY2018": 15557}),
        ("Net cash from/(used in) investing activities", {"FY2025": -1676663, "FY2024": -829521, "FY2023": -1026103, "FY2022": -1300895, "FY2021": -285759, "FY2020": -101879, "FY2019": -2407, "FY2018": -886}),
        ("Net cash from/(used in) financing activities", {"FY2025": 157407, "FY2024": 332432, "FY2023": -6564, "FY2022": 441534, "FY2021": 194506, "FY2020": 111064, "FY2019": 104150, "FY2018": 67398}),
        ("Cash and cash equivalents at end of year", {"FY2025": 11021763, "FY2024": 7624300, "FY2023": 3101242, "FY2022": 3134540, "FY2021": 2977368, "FY2020": 1373722, "FY2019": 549847, "FY2018": 96943}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "55.92%", "FY2024": "54.94%", "FY2023": "54.40%", "FY2022": "155.1%", "FY2021": "99%", "FY2020": "70% (unaudited)", "FY2019": "126% (unaudited)", "FY2018": "Not publicly disclosed"}),
        ("Tier 1 Ratio", {"FY2025": "55.92%", "FY2024": "54.94%", "FY2023": "54.40%", "FY2022": "155.1%", "FY2021": "99%", "FY2020": "70% (unaudited)", "FY2019": "126% (unaudited)", "FY2018": "Not publicly disclosed"}),
        ("Total Capital Ratio", {"FY2025": "56.67%", "FY2024": "55.87%", "FY2023": "55.91%", "FY2022": "159.1%", "FY2021": "99%", "FY2020": "Not publicly disclosed", "FY2019": "Not publicly disclosed", "FY2018": "Not publicly disclosed"}),
        ("Leverage Ratio", {"FY2025": "15.53%", "FY2024": "16.00%", "FY2023": "14.15%", "FY2022": "25.7%", "FY2021": "29.3%", "FY2020": "Not publicly disclosed", "FY2019": "Not publicly disclosed", "FY2018": "Not publicly disclosed"}),
        ("LCR", {"FY2025": "1,178.76%", "FY2024": "724.51%", "FY2023": "760.4%", "FY2022": "1,072.4%", "FY2021": "904%", "FY2020": "Not publicly disclosed", "FY2019": "Not publicly disclosed", "FY2018": "Not publicly disclosed"}),
        ("NSFR", {"FY2025": "843.98%", "FY2024": "680.81%", "FY2023": "724.4%", "FY2022": "1,057.8%", "FY2021": "Not disclosed", "FY2020": "Not publicly disclosed", "FY2019": "Not publicly disclosed", "FY2018": "Not publicly disclosed"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Entity basis switches from Monzo Bank Limited (FY2018-23) to "
         "Monzo Bank Holding Group Limited (FY2024-25); FY2024 is a 13-month transition period from a fiscal-year-end "
         "change. Leverage ratio for FY2022 uses the single unlabelled 'Leverage ratio' KM1 row whose basis is not "
         "stated in the source (see Leverage Ratio sheet). 'Revenue / Net operating income' uses FY2025's 'Gross "
         "Profit' row and FY2018-24's 'Net operating income' row from the Profit & Loss sheet - both are the same "
         "underlying concept (income after netting interest/fee expense and credit losses, before operating "
         "expenses), just grouped under different labels across Monzo's presentation-format change. "
         "'Other equity movements, net' combines shares issued, cost of issuance, share-based payments, "
         "exercise of options, and reserve reclassifications/merger reserve creation from the Statement of "
         "Changes in Equity sheet into one line; see that sheet for the full year-by-year breakdown. "
         "FY2018-20 are Monzo's real, verified historical floor (not FY2016 as originally guessed by "
         "HD-024's GLEIF-based ticket description) - see the FLOOR NOTE on the Cash Flow Statement sheet.",
)

bw.save("/Users/armaan/code/katalysis/banks/MONZO FINANCIALS.xlsx")
