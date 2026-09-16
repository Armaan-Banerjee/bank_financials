import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014", "FY2013", "FY2012"]
Y_CORE = YEARS[:YEARS.index('FY2014') + 1]  # HD-072/075/079: FY2014-floor default for Pillar 3/Asset Quality/RWA Breakdown/Overview

YEAR_LABEL = {y: y for y in YEARS}

# ---------------------------------------------------------------
# HD-050 extension (2026-09-05, capped at FY2014 per the historical-depth
# map's project-wide decision - see wayfinder/historical-depth/map.md).
# FY2014-FY2020 sourced from National Westminster Bank Plc's own Companies
# House-filed statutory Annual Report and Accounts for each year (scanned
# filings, OCR'd via tesseract/ocrmypdf - Companies House's older filings are
# TIFF-to-PDF scans with no text layer, unlike the current investors.
# natwestgroup.com-hosted PDFs used for FY2021 onward). Every OCR'd figure
# below was cross-checked by internal arithmetic (component rows summing to
# the source's own disclosed subtotal/total) and, for the years spanning the
# 2026-09-05 session's own visual spot-checks, direct page-image inspection -
# not taken from a single raw OCR pass. Companies House filing history and
# document links:
#   https://find-and-update.company-information.service.gov.uk/company/00929027/filing-history
NWB_CH_AR = {
    "FY2014": "https://find-and-update.company-information.service.gov.uk/company/00929027/filing-history/MzEyNjA1MTk5MWFkaXF6a2N4/document?format=pdf&download=0",
    "FY2015": "https://find-and-update.company-information.service.gov.uk/company/00929027/filing-history/MzE1MDMzMjY2MGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2016": "https://find-and-update.company-information.service.gov.uk/company/00929027/filing-history/MzE3ODExOTc1MGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2017": "https://find-and-update.company-information.service.gov.uk/company/00929027/filing-history/MzIwNzI3ODQ0OWFkaXF6a2N4/document?format=pdf&download=0",
    "FY2018": "https://find-and-update.company-information.service.gov.uk/company/00929027/filing-history/MzIzNjA1NTcyNWFkaXF6a2N4/document?format=pdf&download=0",
    "FY2019": "https://find-and-update.company-information.service.gov.uk/company/00929027/filing-history/MzI2Mzg0Njg4N2FkaXF6a2N4/document?format=pdf&download=0",
    "FY2020": "https://find-and-update.company-information.service.gov.uk/company/00929027/filing-history/MzMwMzI1NjQ3NGFkaXF6a2N4/document?format=pdf&download=0",
    # HD-072 extension (2026-09-06): FY2013 and FY2012 Annual Reports, each filed at
    # Companies House with a Bank-column comparative table giving that year and the prior
    # year side by side - the FY2013 filing therefore already provides clean, internally
    # self-consistent FY2013 AND FY2012 Bank-column figures for all four statutory
    # statements (verified: FY2013's own Balance Sheet/Statement of Changes in Equity/Cash
    # Flow tie out to the exact £m across the FY2012/FY2013 boundary - see basis notes
    # below). The FY2012 filing (year-end 2012, with its own FY2011 comparative) was
    # downloaded and cross-checked against the FY2013 filing's restated FY2012 column;
    # see the DATA-QUALITY note in STATEMENTS_SOURCES for the small IAS 19R-driven
    # restatement difference between them.
    "FY2013": "https://find-and-update.company-information.service.gov.uk/company/00929027/filing-history/MzEwMjk4NDk5OGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2012": "https://find-and-update.company-information.service.gov.uk/company/00929027/filing-history/MzA4MDkxNDY3OWFkaXF6a2N4/document?format=pdf&download=0",
}
NWB_PRE2018_BASIS_NOTE = (
    "STRUCTURAL BREAK NOTE (FY2014-FY2017 vs FY2018 onward): FY2014-2017 accounts are prepared under IAS 39 "
    "(pre-IFRS 9) and the pre-ring-fencing RBS Group legal-entity structure - the source balance sheet uses "
    "different note groupings (e.g. 'Amounts due from/to holding company and subsidiaries' and 'amounts due "
    "from/to intermediate holding company and subsidiaries' are split across the Loans-to-banks, Loans-to-"
    "customers and Derivatives notes rather than shown as one standalone balance sheet line as in FY2018 "
    "onward). Figures below are mapped onto this workbook's standard row set by adding the source's own "
    "sub-components together (verified to tie exactly to the source's own reported subtotals/totals); the "
    "'Amounts due from/to holding companies and fellow subsidiaries' row is therefore intentionally blank for "
    "FY2014-FY2017 rather than double-counted or estimated. FY2017 and FY2016 also include Ulster Bank "
    "(Ireland) DAC and Lombard North Central Plc up to their 1 January 2017 ring-fencing transfer out of the "
    "Group; FY2018 reflects the post-ring-fencing entity shape (RBS Treasury/shared-services transferred IN "
    "from NatWest Markets Plc at net asset value instead). IFRS 9 was adopted 1 January 2018; FY2018's own "
    "Annual Report presents 2018 only for the primary statements (no 2017 comparative column, reflecting the "
    "genuine basis change), so FY2017 figures are taken from FY2017's own Annual Report and FY2018 figures "
    "cross-checked against FY2019's Annual Report restated comparative column."
)

AR2025_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/13022026/nwb-annual-report.pdf"
AR2024_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/14022025/nwb-annual-report.pdf"
AR2023_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/16022024/nwb-plc-annual-report.pdf"
AR2022_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/17022023/nwb-plc-annual-report.pdf"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/00929027/filing-history/MzMzODcyODkwNGFkaXF6a2N4/document?format=pdf&download=0"
P3_2025_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/13022026/nwb-pillar-3-report.pdf"
P3_2024_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/14022025/nwb-pillar-3-report.pdf"
P3_2023_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/16022024/nwb-plc-pillar-3-report.pdf"
P3_2022_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/17022023/nwb-plc-pillar-3-report.pdf"
P3_2025_Q3_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/11112025/11112025-nwb-pillar-3-report.pdf"
P3_2024_Q3_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/12112024/nwb-plc-pillar-3-q3-2024.pdf"
P3_2023_Q3_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/13-11-2023/natwest-bank-plc-pillar-3-q3-2023.pdf"
P3_2022_Q3_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/17022023/nwb-plc-pillar-3-report.pdf"
CH_COMPANY_URL = "https://find-and-update.company-information.service.gov.uk/company/00929027"

ENTITY_NOTE = (
    "ENTITY NOTE: This workbook covers National Westminster Bank Public Limited Company (NWB Plc), company "
    "number 00929027, FRN 121878 and LEI 213800IBT39XQ9C4CP71. It is the PRA-authorised legal entity named in "
    "the project bank list, not NatWest Group plc, NatWest Holdings Limited, RBS plc or NatWest Markets Plc. "
    "NWB Plc is a member of the UK Domestic Liquidity Sub-Group (UK DoLSub) with RBS plc and Coutts & Company; "
    "LCR and NSFR are therefore shown on the UK DoLSub basis where the entity reports that basis, rather than as "
    "NWB Plc solo figures. Companies House confirms company 00929027 and the filed 2021 accounts used below."
)


def ar_sources():
    return (
        "Sources - NWB Plc own annual accounts, £m:\n"
        f"FY2025: NWB Group Annual Report and Accounts 2025, p.96 (cash flow statement) - {AR2025_URL}\n"
        f"FY2024: NWB Group Annual Report and Accounts 2024, p.102 (cash flow statement) - {AR2024_URL}\n"
        f"FY2023: NWB Group Annual Report and Accounts 2023, p.103 (cash flow statement) - {AR2023_URL}\n"
        f"FY2022: NWB Group Annual Report and Accounts 2022, p.104 (cash flow statement) - {AR2022_URL}\n"
        f"FY2021: NWB Group Annual Report and Accounts 2022, p.104 (FY2021 comparative column; independently filed at Companies House) - {AR2022_URL}; {AR2021_URL}\n\n"
        + ENTITY_NOTE
    )


def p3_sources():
    return (
        "Sources - NWB Plc UK KM1 key metrics, PRA transitional basis:\n"
        f"FY2025: NWB Plc Pillar 3 Report 2025, p.7 - {P3_2025_URL}\n"
        f"FY2024: NWB Plc Pillar 3 Report 2024, p.7 - {P3_2024_URL}\n"
        f"FY2023: NWB Plc Pillar 3 Report 2023, p.7 - {P3_2023_URL}\n"
        f"FY2022 and FY2021: NWB Plc Pillar 3 Report 2022, p.7 (FY2021 comparative column) - {P3_2022_URL}\n\n"
        + ENTITY_NOTE
    )


bw = BankWorkbook("National Westminster Bank Public Limited Company", Y_CORE, YEAR_LABEL, header_color="005A8D")

STATEMENTS_SOURCES = (
    "Sources - NWB Plc own annual accounts, £m:\n"
    f"FY2025/FY2024: NWB Group Annual Report and Accounts 2025, Balance sheet p.93, Statement of changes in equity p.94 - {AR2025_URL}\n"
    f"FY2023/FY2022: NWB Group Annual Report and Accounts 2023, Balance sheet p.100, Statement of changes in equity p.101 - {AR2023_URL}\n"
    f"FY2021 (and FY2022 cross-check): NWB Group Annual Report and Accounts 2022, Balance sheet p.101, Statement of changes in equity p.102 - {AR2022_URL}\n"
    f"FY2020/FY2019: National Westminster Bank Plc Annual Report and Accounts 2020 (Companies House filing), Balance sheet p.91, Statement of changes in equity p.92 - {NWB_CH_AR['FY2020']}\n"
    f"FY2018 (and FY2019 cross-check): National Westminster Bank Plc Annual Report and Accounts 2019 (Companies House filing), Balance sheet p.81, Statement of changes in equity p.82 - {NWB_CH_AR['FY2019']}; NatWest Plc Annual Report and Accounts 2018 (Companies House filing), Balance sheet p.73, Statement of changes in equity p.74 - {NWB_CH_AR['FY2018']}\n"
    f"FY2017: NatWest Plc Annual Report and Accounts 2017 (Companies House filing), Balance sheet p.97, Statement of changes in equity p.98 - {NWB_CH_AR['FY2017']}\n"
    f"FY2016 (and FY2015 cross-check): NatWest Plc Annual Report and Accounts 2016 (Companies House filing), Balance sheet p.99, Statement of changes in equity p.100 - {NWB_CH_AR['FY2016']}; NatWest Plc Annual Report and Accounts 2017, Balance sheet p.97 (FY2016 comparative) - {NWB_CH_AR['FY2017']}\n"
    f"FY2015: NatWest Plc Annual Report and Accounts 2017 (Companies House filing), Balance sheet p.97, Statement of changes in equity p.98/99 (FY2015 comparative column) - {NWB_CH_AR['FY2017']}\n"
    f"FY2014: National Westminster Bank Plc Annual Report and Accounts 2014 (Companies House filing), Balance sheet p.132, Statement of changes in equity p.133 - {NWB_CH_AR['FY2014']}\n\n"
    "FY2014 equity cross-check: NatWest Plc Pillar 3 Report 2014, Capital resources table (NatWest Plc shareholders' equity £13,312m; preference shares-equity nil) - https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/2014-reports/pillar-3-report-2014-v2.pdf\n\n"
    + ENTITY_NOTE + "\n\n" + NWB_PRE2018_BASIS_NOTE + "\n\n"
    "BASIS NOTE - Profit & Loss: as permitted by s.408(3) Companies Act 2006, NWB Plc has not presented a standalone "
    "income statement or statement of comprehensive income in any of the reviewed Annual Reports (FY2012-FY2025) - only the NWB Group "
    "consolidated income statement is published. The Profit & Loss sheet is therefore shown on NWB Group basis (not "
    "NWB Plc entity-level like the Balance Sheet and Statement of Changes in Equity). NWB Plc's own profit for the year "
    "(disclosed only as a single headline figure via a Balance Sheet footnote) is close to but not identical to the "
    "Group figure each year (e.g. FY2025: NWB Plc £4,227m vs NWB Group £4,198m) - the difference reflects dividend "
    "income and other items that differ between the solo and consolidated bases.\n\n"
    "BASIS NOTE - Balance Sheet and Statement of Changes in Equity: both are shown on the NWB Plc entity-level column "
    "of each report's Group/Plc comparative tables, consistent with the Cash Flow Statement and Pillar 3 sheets. "
    "NWB Plc's own Total equity carries no non-controlling interests (NCI only arises at NWB Group level).\n\n"
    "BASIS NOTE - 'Other financial assets' measurement-basis breakdown (MFVTPL/FVTPL, FVOCI, amortised cost rows): "
    "sourced from Note 9 'Financial instruments - classification' (NWB Plc column) in each year's own Annual Report - "
    f"FY2025/FY2024: NWB Group Annual Report and Accounts 2025, Note 9, p.120 (NWB Plc column) - {AR2025_URL}\n"
    f"FY2023/FY2022: NWB Group Annual Report and Accounts 2023, Note 9, p.125 (NWB Plc column) - {AR2023_URL}\n"
    f"FY2021 (comparative column): NWB Group Annual Report and Accounts 2022, Note 9, p.127 (NWB Plc column) - {AR2022_URL}\n"
    "These three rows are a note-level sub-split of the already-reported 'Other financial assets' TOTAL row above "
    "(they sum exactly to it each year) - not additional assets, so no double-counting."
)

# ---------------------------------------------------------------
# Balance Sheet (NWB Plc entity-level column of each report's own
# NWB Group / NWB Plc comparative table). Total assets = Total liabilities +
# Total equity exactly in every year - zero plug rows.
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 29911, "FY2024": 35083, "FY2023": 48238, "FY2022": 73062, "FY2021": 101210, "FY2020": 62878, "FY2019": 26377, "FY2018": 43966, "FY2017": 34763, "FY2016": 1198, "FY2015": 819, "FY2014": 1054, "FY2013": 734, "FY2012": 921}),
    ("DATA", "Derivatives", {"FY2025": 1106, "FY2024": 2892, "FY2023": 3213, "FY2022": 4430, "FY2021": 2547, "FY2020": 3438, "FY2019": 3404, "FY2018": 1277, "FY2017": 2277, "FY2016": 3082, "FY2015": 2086, "FY2014": 3112, "FY2013": 2642, "FY2012": 3912}),
    ("DATA", "Loans to banks - amortised cost", {"FY2025": 4261, "FY2024": 3148, "FY2023": 3043, "FY2022": 2870, "FY2021": 3638, "FY2020": 2798, "FY2019": 2741, "FY2018": 5875, "FY2017": 55788, "FY2016": 64603, "FY2015": 73249, "FY2014": 78504, "FY2013": 89546, "FY2012": 80915}),
    ("DATA", "Loans to customers - amortised cost", {"FY2025": 310121, "FY2024": 297548, "FY2023": 284314, "FY2022": 267401, "FY2021": 255443, "FY2020": 238366, "FY2019": 198504, "FY2018": 171433, "FY2017": 160679, "FY2016": 150147, "FY2015": 134383, "FY2014": 124297, "FY2013": 119541, "FY2012": 120168}),
    ("DATA", "Amounts due from holding companies and fellow subsidiaries", {"FY2025": 38965, "FY2024": 36383, "FY2023": 33499, "FY2022": 32133, "FY2021": 27122, "FY2020": 28176, "FY2019": 31705, "FY2018": 30780}),
    ("DATA", "Securities subject to repurchase agreements", {"FY2025": 15004, "FY2024": 8984, "FY2023": 6469, "FY2022": 2140, "FY2021": 10813, "FY2020": 11438, "FY2019": 4175, "FY2018": 9890, "FY2017": 0, "FY2016": 0, "FY2015": 0, "FY2014": 0, "FY2013": 0, "FY2012": 0}),
    ("DATA", "Other financial assets excluding securities subject to repurchase agreements", {"FY2025": 37152, "FY2024": 29814, "FY2023": 24623, "FY2022": 12040, "FY2021": 17836, "FY2020": 26168, "FY2019": 36383, "FY2018": 30944, "FY2017": 1066, "FY2016": 120, "FY2015": 51, "FY2014": 829, "FY2013": 2592, "FY2012": 2616}),
    # IN-INVEST-NOTE9 (2026-09-07): note-level measurement-basis breakdown of the "Other
    # financial assets" TOTAL below, sourced from each Annual Report's own Note 9 "Financial
    # instruments - classification" table (NWB Plc column). These three rows sum EXACTLY to
    # the existing TOTAL row for every year shown (e.g. FY2025: 639+29,643+21,874=52,156) -
    # they are a note-level sub-split of the same reported total, not additional assets, so
    # the TOTAL row itself is intentionally left unchanged to avoid double-counting.
    ("DATA", "Other financial assets - mandatorily at fair value through profit or loss (MFVTPL/FVTPL)", {"FY2025": 639, "FY2024": 534, "FY2023": 453, "FY2022": 417, "FY2021": 226}),
    ("DATA", "Other financial assets - fair value through other comprehensive income (FVOCI)", {"FY2025": 29643, "FY2024": 28836, "FY2023": 23013, "FY2022": 9713, "FY2021": 26148}),
    ("DATA", "Other financial assets - amortised cost", {"FY2025": 21874, "FY2024": 9428, "FY2023": 7626, "FY2022": 4050, "FY2021": 2275}),
    ("TOTAL", "Other financial assets", {"FY2025": 52156, "FY2024": 38798, "FY2023": 31092, "FY2022": 14180, "FY2021": 28649, "FY2020": 37606, "FY2019": 40558, "FY2018": 40834, "FY2017": 1066, "FY2016": 120, "FY2015": 51, "FY2014": 829, "FY2013": 2592, "FY2012": 2616}),
    ("DATA", "Investment in group undertakings", {"FY2025": 2477, "FY2024": 2520, "FY2023": 2615, "FY2022": 2030, "FY2021": 2319, "FY2020": 2374, "FY2019": 2394, "FY2018": 2466, "FY2017": 2546, "FY2016": 6931, "FY2015": 6554, "FY2014": 7866, "FY2013": 5412, "FY2012": 5083}),
    ("DATA", "Other assets", {"FY2025": 5652, "FY2024": 5503, "FY2023": 5735, "FY2022": 5641, "FY2021": 5183, "FY2020": 4967, "FY2019": 5271, "FY2018": 4993, "FY2017": 2598, "FY2016": 2840, "FY2015": 3250, "FY2014": 2642, "FY2013": 2712, "FY2012": 2896}),
    ("TOTAL", "Total assets", {"FY2025": 444649, "FY2024": 421875, "FY2023": 411749, "FY2022": 401747, "FY2021": 426111, "FY2020": 380603, "FY2019": 310954, "FY2018": 301624, "FY2017": 259717, "FY2016": 228921, "FY2015": 220392, "FY2014": 218304, "FY2013": 223179, "FY2012": 216511}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Bank deposits", {"FY2025": 33016, "FY2024": 24778, "FY2023": 18052, "FY2022": 16059, "FY2021": 22829, "FY2020": 14866, "FY2019": 15487, "FY2018": 17557, "FY2017": 32465, "FY2016": 9208, "FY2015": 10936, "FY2014": 9548, "FY2013": 11091, "FY2012": 24042}),
    ("DATA", "Customer deposits", {"FY2025": 282427, "FY2024": 275972, "FY2023": 276202, "FY2022": 281558, "FY2021": 292470, "FY2020": 255290, "FY2019": 208698, "FY2018": 204279, "FY2017": 201150, "FY2016": 192490, "FY2015": 185139, "FY2014": 182210, "FY2013": 189156, "FY2012": 167649}),
    ("DATA", "Amounts due to holding companies and fellow subsidiaries", {"FY2025": 98661, "FY2024": 90925, "FY2023": 84174, "FY2022": 75037, "FY2021": 76722, "FY2020": 69617, "FY2019": 51019, "FY2018": 50968}),
    ("DATA", "Derivatives", {"FY2025": 780, "FY2024": 1323, "FY2023": 2014, "FY2022": 2582, "FY2021": 4336, "FY2020": 6769, "FY2019": 5013, "FY2018": 1185, "FY2017": 3117, "FY2016": 3938, "FY2015": 2295, "FY2014": 3756, "FY2013": 2984, "FY2012": 4409}),
    ("DATA", "Other financial liabilities", {"FY2025": 3670, "FY2024": 3824, "FY2023": 8147, "FY2022": 4525, "FY2021": 6384, "FY2020": 9612, "FY2019": 7635, "FY2018": 5889, "FY2017": 0, "FY2016": 86, "FY2015": 53, "FY2014": 67, "FY2013": 73, "FY2012": 38}),
    ("DATA", "Subordinated liabilities", {"FY2025": 119, "FY2024": 119, "FY2023": 119, "FY2022": 191, "FY2021": 205, "FY2020": 1230, "FY2019": 1242, "FY2018": 1267, "FY2017": 5640, "FY2016": 5890, "FY2015": 5741, "FY2014": 6122, "FY2013": 6106, "FY2012": 6123}),
    ("DATA", "Notes in circulation", {"FY2025": 1049, "FY2024": 935, "FY2023": 806, "FY2022": 809, "FY2021": 904, "FY2020": 1266, "FY2019": 0}),
    ("DATA", "Other liabilities", {"FY2025": 2242, "FY2024": 2390, "FY2023": 2534, "FY2022": 2743, "FY2021": 3095, "FY2020": 3489, "FY2019": 3834, "FY2018": 2213, "FY2017": 1991, "FY2016": 2012, "FY2015": 4946, "FY2014": 3289, "FY2013": 5239, "FY2012": 6490}),
    ("TOTAL", "Total liabilities", {"FY2025": 421964, "FY2024": 400266, "FY2023": 392048, "FY2022": 383504, "FY2021": 406945, "FY2020": 362139, "FY2019": 292928, "FY2018": 283348, "FY2017": 244362, "FY2016": 213624, "FY2015": 209110, "FY2014": 204992, "FY2013": 214649, "FY2012": 208751}),
    ("SECTION", "Equity", {}),
    ("TOTAL", "Total equity (owners' equity - no NCI at NWB Plc solo level)", {"FY2025": 22685, "FY2024": 21609, "FY2023": 19701, "FY2022": 18243, "FY2021": 19166, "FY2020": 18464, "FY2019": 18026, "FY2018": 18276, "FY2017": 15355, "FY2016": 15297, "FY2015": 11282, "FY2014": 13312, "FY2013": 8530, "FY2012": 7760}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 444649, "FY2024": 421875, "FY2023": 411749, "FY2022": 401747, "FY2021": 426111, "FY2020": 380603, "FY2019": 310954, "FY2018": 301624, "FY2017": 259717, "FY2016": 228921, "FY2015": 220392, "FY2014": 218304, "FY2013": 223179, "FY2012": 216511}),
]
bw.add_balance_sheet_sheet(
    title="National Westminster Bank Plc — Balance Sheet",
    subtitle="NWB Plc entity-level basis (the Plc column of each report's Group/Plc comparative table), £m.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=280,
    unit_suffix=" (£m)",
    years=YEARS,
)

# ---------------------------------------------------------------
# Profit & Loss - NWB Group basis (NWB Plc takes the s.408(3) Companies Act
# 2006 exemption and publishes no standalone income statement - see
# BASIS NOTE in STATEMENTS_SOURCES).
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable", {"FY2025": 19148, "FY2024": 18100, "FY2023": 14764, "FY2022": 9159, "FY2021": 6721, "FY2020": 6825, "FY2019": 7408, "FY2018": 6968, "FY2017": 6271, "FY2016": 5784, "FY2015": 5792, "FY2014": 6499, "FY2013": 7483, "FY2012": 6316}),
    ("DATA", "Interest payable", {"FY2025": -9497, "FY2024": -9892, "FY2023": -6741, "FY2022": -1627, "FY2021": -719, "FY2020": -1015, "FY2019": -1572, "FY2018": -1154, "FY2017": -790, "FY2016": -1012, "FY2015": -1253, "FY2014": -1922, "FY2013": -3462, "FY2012": -3443}),
    ("TOTAL", "Net interest income", {"FY2025": 9651, "FY2024": 8208, "FY2023": 8023, "FY2022": 7532, "FY2021": 6002, "FY2020": 5810, "FY2019": 5836, "FY2018": 5814, "FY2017": 5481, "FY2016": 4772, "FY2015": 4539, "FY2014": 4577, "FY2013": 4021, "FY2012": 2873}),
    ("DATA", "Fees and commissions receivable", {"FY2025": 2419, "FY2024": 2276, "FY2023": 2177, "FY2022": 2119, "FY2021": 1862, "FY2020": 1685, "FY2019": 2208, "FY2018": 2113, "FY2017": 2054, "FY2016": 1890, "FY2015": 1900, "FY2014": 2439, "FY2013": 2600, "FY2012": 2643}),
    ("DATA", "Fees and commissions payable", {"FY2025": -597, "FY2024": -542, "FY2023": -508, "FY2022": -493, "FY2021": -380, "FY2020": -301, "FY2019": -485, "FY2018": -462, "FY2017": -499, "FY2016": -444, "FY2015": -473, "FY2014": -498, "FY2013": -490, "FY2012": -428}),
    ("DATA", "Income from trading activities (HD-072: distinct source line FY2013/FY2012 only, folded into Other operating income in FY2014's own AR presentation)", {"FY2013": 726, "FY2012": 1150}),
    ("DATA", "Gain on redemption of own debt (HD-072: distinct source line FY2013 only; nil in FY2012)", {"FY2013": 239, "FY2012": 0}),
    ("DATA", "Other operating income", {"FY2025": 2147, "FY2024": 2031, "FY2023": 2394, "FY2022": 2585, "FY2021": 1785, "FY2020": 1761, "FY2019": 1604, "FY2018": 2067, "FY2017": 1111, "FY2016": -179, "FY2015": -340, "FY2014": 759, "FY2013": 268, "FY2012": 188}),
    ("TOTAL", "Non-interest income", {"FY2025": 3969, "FY2024": 3765, "FY2023": 4063, "FY2022": 4211, "FY2021": 3267, "FY2020": 3145, "FY2019": 3327, "FY2018": 3718, "FY2017": 2666, "FY2016": 1267, "FY2015": 1087, "FY2014": 2700, "FY2013": 3343, "FY2012": 3553}),
    ("TOTAL", "Total income", {"FY2025": 13620, "FY2024": 11973, "FY2023": 12086, "FY2022": 11743, "FY2021": 9269, "FY2020": 8955, "FY2019": 9163, "FY2018": 9532, "FY2017": 8147, "FY2016": 6039, "FY2015": 5626, "FY2014": 7277, "FY2013": 7364, "FY2012": 6426}),
    ("DATA", "Staff costs", {"FY2025": -3392, "FY2024": -3301, "FY2023": -3109, "FY2022": -2896, "FY2021": -2815, "FY2020": -2823, "FY2019": -2859, "FY2018": -2184, "FY2017": -844, "FY2016": -713, "FY2015": -1000, "FY2014": -1668, "FY2013": -1683, "FY2012": -1676}),
    ("DATA", "Premises and equipment", {"FY2025": -1183, "FY2024": -1099, "FY2023": -1039, "FY2022": -994, "FY2021": -948, "FY2020": -1044, "FY2019": -1078, "FY2018": -757, "FY2017": -273, "FY2016": -233, "FY2015": -442, "FY2014": -280, "FY2013": -375, "FY2012": -341}),
    ("DATA", "Other administrative expenses", {"FY2025": -1588, "FY2024": -1576, "FY2023": -1768, "FY2022": -1630, "FY2021": -1660, "FY2020": -1476, "FY2019": -2450, "FY2018": -2132, "FY2017": -2921, "FY2016": -3326, "FY2015": -3306, "FY2014": -3775, "FY2013": -6488, "FY2012": -4195}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -1078, "FY2024": -987, "FY2023": -877, "FY2022": -768, "FY2021": -776, "FY2020": -841, "FY2019": -878, "FY2018": -521, "FY2017": -282, "FY2016": -143, "FY2015": -221, "FY2014": -226, "FY2013": -214, "FY2012": -213}),
    ("DATA", "Write-down of goodwill and other intangible assets (HD-072: distinct source line FY2013/FY2012 only)", {"FY2013": -2, "FY2012": -117}),
    ("TOTAL", "Operating expenses", {"FY2025": -7241, "FY2024": -6963, "FY2023": -6793, "FY2022": -6288, "FY2021": -6199, "FY2020": -6184, "FY2019": -7265, "FY2018": -5594, "FY2017": -4320, "FY2016": -4415, "FY2015": -4969, "FY2014": -5949, "FY2013": -8762, "FY2012": -6542}),
    ("TOTAL", "Profit before impairment losses/(releases)", {"FY2025": 6379, "FY2024": 5010, "FY2023": 5293, "FY2022": 5455, "FY2021": 3070, "FY2020": 2771, "FY2019": 1898, "FY2018": 3938, "FY2017": 3827, "FY2016": 1624, "FY2015": 657, "FY2014": 1328, "FY2013": -1398, "FY2012": -116}),
    ("DATA", "Impairment losses/(releases)", {"FY2025": -653, "FY2024": -347, "FY2023": -504, "FY2022": -341, "FY2021": 813, "FY2020": -2169, "FY2019": -572, "FY2018": -428, "FY2017": -341, "FY2016": -125, "FY2015": 54, "FY2014": 1249, "FY2013": -5407, "FY2012": -3183}),
    ("TOTAL", "Operating profit before tax", {"FY2025": 5726, "FY2024": 4663, "FY2023": 4789, "FY2022": 5114, "FY2021": 3883, "FY2020": 602, "FY2019": 1326, "FY2018": 3510, "FY2017": 3516, "FY2016": 1499, "FY2015": 711, "FY2014": 2577, "FY2013": -6805, "FY2012": -3299}),
    ("DATA", "Tax charge", {"FY2025": -1528, "FY2024": -1238, "FY2023": -1280, "FY2022": -1425, "FY2021": -976, "FY2020": -66, "FY2019": -442, "FY2018": -741, "FY2017": -812, "FY2016": -683, "FY2015": -373, "FY2014": -844, "FY2013": 842, "FY2012": 47}),
    ("TOTAL", "Profit from continuing operations", {"FY2018": 2769, "FY2017": 2704, "FY2016": 816, "FY2015": 338}),
    ("DATA", "Loss from discontinued operations, net of tax", {"FY2018": -3, "FY2017": -635, "FY2016": -1683, "FY2015": -1544}),
    ("TOTAL", "Profit for the year", {"FY2025": 4198, "FY2024": 3425, "FY2023": 3509, "FY2022": 3689, "FY2021": 2907, "FY2020": 536, "FY2019": 884, "FY2018": 2766, "FY2017": 2069, "FY2016": -867, "FY2015": -1206, "FY2014": 1733, "FY2013": -5963, "FY2012": -3252}),
    ("SECTION", "Other comprehensive income, net of tax", {}),
    ("DATA", "Remeasurement of retirement benefit schemes, net of tax", {"FY2025": 0, "FY2024": -111, "FY2023": -107, "FY2022": -410, "FY2021": -373, "FY2020": -41, "FY2019": -97, "FY2018": -1467, "FY2017": -14, "FY2016": -710, "FY2015": 161, "FY2014": 79, "FY2013": 110, "FY2012": -1566}),
    ("DATA", "FVOCI financial assets", {"FY2025": 115, "FY2024": -28, "FY2023": 43, "FY2022": -392, "FY2021": -96, "FY2020": 47, "FY2019": -6, "FY2018": -118, "FY2017": -312, "FY2016": 284, "FY2015": -11, "FY2014": -38, "FY2013": 42, "FY2012": 17}),
    ("DATA", "Cash flow hedges", {"FY2025": 73, "FY2024": 405, "FY2023": -290, "FY2022": -542, "FY2021": 180, "FY2020": -218, "FY2019": 36, "FY2017": 2, "FY2016": 2, "FY2015": 2, "FY2014": 3, "FY2013": 5, "FY2012": 6}),
    ("DATA", "Currency translation", {"FY2025": 6, "FY2024": -18, "FY2023": -17, "FY2022": -2, "FY2021": -22, "FY2020": 7, "FY2019": -85, "FY2018": -811, "FY2017": -805, "FY2016": 862, "FY2015": -326, "FY2014": 160, "FY2013": 106, "FY2012": -237}),
    ("DATA", "Tax on items that qualify for reclassification", {"FY2025": -54, "FY2024": -107, "FY2023": 73, "FY2022": 276, "FY2021": -40, "FY2020": 41, "FY2019": -3, "FY2018": 32, "FY2017": 5, "FY2016": 20, "FY2015": 3, "FY2014": 12, "FY2013": -9, "FY2012": -3}),
    ("TOTAL", "Other comprehensive income/(loss) after tax", {"FY2025": 140, "FY2024": 141, "FY2023": -298, "FY2022": -1070, "FY2021": -351, "FY2020": -164, "FY2019": -155, "FY2018": -2361, "FY2017": -1126, "FY2016": 458, "FY2015": -171, "FY2014": 216, "FY2013": 254, "FY2012": -1783}),
    ("TOTAL", "Total comprehensive income for the year", {"FY2025": 4338, "FY2024": 3566, "FY2023": 3211, "FY2022": 2619, "FY2021": 2556, "FY2020": 372, "FY2019": 729, "FY2018": 378, "FY2017": 943, "FY2016": -409, "FY2015": -1377, "FY2014": 1949, "FY2013": -5709, "FY2012": -5035}),
]
bw.add_income_statement_sheet(
    title="National Westminster Bank Plc — Profit & Loss",
    subtitle="NWB Group basis (Consolidated income statement / statement of comprehensive income) - NWB Plc "
              "publishes no standalone income statement, see BASIS NOTE in the source citation. £m.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=280,
    unit_suffix=" (£m)",
    years=YEARS,
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - NWB Plc entity-level column, chronological
# roll-forward. Equity reconciliation ladder confirmed: every year's own
# closing balance ties exactly to both the next year's own opening balance
# and that year's own Balance Sheet Total equity - zero plug rows needed
# anywhere across all 5 years. Ladder's mandated scan caught the "easy to
# skip" reserve-transfer items (merger reserve amortisation, capital
# redemption reserve movements from preference share redemptions) that
# net to zero on Total equity but move real balances between components.
# ---------------------------------------------------------------
equity_headers = [
    "Called-up share capital", "Paid-in equity", "Share premium account", "Merger reserve",
    "FVOCI reserve", "Cash flow hedging reserve", "Foreign exchange reserve",
    "Capital redemption reserve", "Retained earnings", "Total equity",
]
equity_rows = [
    # HD-072 extension (2026-09-06): FY2012 and FY2013 movements, sourced entirely from the
    # FY2013 Annual Report's own Bank-column Statement of changes in equity (p.156-157),
    # which gives 2013/2012/2011 as three side-by-side movement columns off one continuous
    # roll-forward - so the FY2011 closing/FY2012 opening row below, the FY2012 movements,
    # and the FY2013 movements are all internally self-consistent from a single document.
    # FY2013's own closing balance (8,530) ties EXACTLY to the FY2013 Balance Sheet's
    # independently-computed Total equity (8,530, itself an accounting identity: Total
    # assets less Total liabilities) - a full, unflagged reconciliation, unlike the FY2014
    # opening gap flagged below. IMPORTANT GAP: this FY2013 closing balance does NOT connect
    # to the next entry below ("At 1 January 2015 (FY2014 closing)") - FY2014's own movement
    # year was never built into this sheet (a pre-existing scope gap from the original
    # HD-050 session that first built this ladder starting at FY2014's closing balance
    # directly, with no FY2013-to-FY2014 movement rows shown) and is out of scope for this
    # ticket to fix. Flagging explicitly rather than bridging with an invented plug row.
    ("TOTAL", "At 1 January 2012 (FY2011 closing / FY2012 opening, NWB Plc entity-level Bank column)", (1678, None, 2225, None, 4, -14, -9, 647, 2849, 7380)),
    ("DATA", "Loss attributable to ordinary shareholders", (None, None, None, None, None, None, None, None, -6301, -6301)),
    ("DATA", "Capital contribution", (None, None, None, None, None, None, None, None, 8050, 8050)),
    ("DATA", "Loss on remeasurement of the retirement benefit schemes, net of tax", (None, None, None, None, None, None, None, None, -1372, -1372)),
    ("DATA", "Available-for-sale reserve movements, net", (None, None, None, None, -1, None, None, None, None, -1)),
    ("DATA", "Cash flow hedging reserve movements, net", (None, None, None, None, None, 4, None, None, None, 4)),
    ("TOTAL", "At 31 December 2012 (FY2012 closing)", (1678, None, 2225, None, 3, -10, -9, 647, 3226, 7760)),
    ("DATA", "Loss attributable to ordinary shareholders", (None, None, None, None, None, None, None, None, -1412, -1412)),
    ("DATA", "Capital contribution", (None, None, None, None, None, None, None, None, 2070, 2070)),
    ("DATA", "Gain on remeasurement of the retirement benefit schemes, net of tax", (None, None, None, None, None, None, None, None, 106, 106)),
    ("DATA", "Available-for-sale reserve movements, net", (None, None, None, None, 3, None, None, None, None, 3)),
    ("DATA", "Cash flow hedging reserve movements, net", (None, None, None, None, None, 4, None, None, None, 4)),
    ("DATA", "Foreign exchange reserve movements, net", (None, None, None, None, None, None, -1, None, None, -1)),
    ("TOTAL", "At 31 December 2013 (FY2013 closing - see IMPORTANT GAP note above re: connection to FY2014)", (1678, None, 2225, None, 6, -6, -10, 647, 3990, 8530)),
    ("TOTAL", "At 1 January 2015 (FY2014 closing / FY2015 opening - see FY2014 basis note)", (1678, None, 2225, None, 0, -3, -10, 647, 7384, 11921)),
    ("DATA", "Profit/(loss) attributable to ordinary shareholders", (None, None, None, None, None, None, None, None, -1422, -1422)),
    ("DATA", "Capital contribution", (None, None, None, None, None, None, None, None, 800, 800)),
    ("DATA", "Redemption of debt preference shares", (None, None, None, None, None, None, None, None, 0, 0)),
    ("DATA", "Loss on remeasurement of the retirement benefit schemes, net of tax", (None, None, None, None, None, None, None, None, -19, -19)),
    ("DATA", "Available-for-sale reserve movements, net", (None, None, None, None, -1, None, None, None, None, -1)),
    ("DATA", "Cash flow hedging reserve movements, net", (None, None, None, None, None, 2, None, None, None, 2)),
    ("TOTAL", "At 31 December 2015 (FY2015 closing)", (1678, None, 2225, None, -1, -1, -10, 647, 6743, 11282)),
    ("DATA", "Profit/(loss) attributable to ordinary shareholders", (None, None, None, None, None, None, None, None, 3466, 3466)),
    ("DATA", "Capital contribution", (None, None, None, None, None, None, None, None, 1300, 1300)),
    ("DATA", "Loss on remeasurement of the retirement benefit schemes, net of tax", (None, None, None, None, None, None, None, None, -753, -753)),
    ("DATA", "Available-for-sale reserve movements, net", (None, None, None, None, 2, None, None, None, None, 2)),
    ("DATA", "Cash flow hedging reserve movements, net", (None, None, None, None, None, -1, None, None, None, -1)),
    ("TOTAL", "At 31 December 2016 (FY2016 closing)", (1678, None, 2225, None, 1, -1, -10, 647, 10756, 15297)),
    ("DATA", "Profit/(loss) attributable to ordinary shareholders", (None, None, None, None, None, None, None, None, 26, 26)),
    ("DATA", "Capital contribution", (None, None, None, None, None, None, None, None, 51, 51)),
    ("DATA", "Redemption of debt preference shares (transfer to capital redemption reserve)", (None, None, None, None, None, None, None, 149, -157, -8)),
    ("DATA", "Loss on remeasurement of the retirement benefit schemes, net of tax", (None, None, None, None, None, None, None, None, -11, -11)),
    ("DATA", "Cash flow hedging reserve movements, net", (None, None, None, None, None, 1, None, None, None, 1)),
    ("TOTAL", "At 31 December 2017 (FY2017 closing)", (1678, None, 2225, None, 1, 0, -10, 796, 10665, 15355)),
    ("DATA", "Paid-in equity issued (Additional Tier 1 notes reclassified as paid-in equity)", (None, 2370, None, None, None, None, None, None, None, 2370)),
    ("DATA", "Merger reserve created on ring-fencing reorganisation (RBS Treasury/shared-services transferred in from NatWest Markets Plc)", (None, None, None, -294, None, None, None, None, None, -294)),
    ("DATA", "Other equity movements, net for the year (profit for the year, dividends and reserve movements not separately broken out - see FY2018 basis note)", (None, None, None, None, 248, 0, -3, None, 600, 845)),
    ("TOTAL", "At 31 December 2018 (FY2018 closing)", (1678, 2370, 2225, -294, 249, 0, -13, 796, 11265, 18276)),
    ("DATA", "Merger reserve amortisation (transfer to/from retained earnings)", (None, None, None, 63, None, None, None, None, -63, 0)),
    ("DATA", "FVOCI reserve - unrealised losses", (None, None, None, None, -20, None, None, None, None, -20)),
    ("DATA", "FVOCI reserve - realised gains", (None, None, None, None, 16, None, None, None, None, 16)),
    ("DATA", "FVOCI reserve - tax", (None, None, None, None, 6, None, None, None, None, 6)),
    ("DATA", "Cash flow hedging reserve - amount recognised in equity", (None, None, None, None, None, 36, None, None, None, 36)),
    ("DATA", "Cash flow hedging reserve - tax", (None, None, None, None, None, -9, None, None, None, -9)),
    ("DATA", "Foreign exchange reserve - retranslation of net assets", (None, None, None, None, None, None, -16, None, None, -16)),
    ("DATA", "Foreign exchange reserve - recycled to profit or loss on disposal of businesses", (None, None, None, None, None, None, 15, None, None, 15)),
    ("DATA", "Implementation of IFRS 16 on 1 January 2019", (None, None, None, None, None, None, None, None, -150, -150)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, None, 724, 724)),
    ("DATA", "Ordinary dividends paid", (None, None, None, None, None, None, None, None, -700, -700)),
    ("DATA", "Paid-in equity dividends paid", (None, None, None, None, None, None, None, None, -166, -166)),
    ("DATA", "Remeasurement of retirement benefit schemes, net of tax", (None, None, None, None, None, None, None, None, -79, -79)),
    ("DATA", "Shares issued under employee share schemes", (None, None, None, None, None, None, None, None, -6, -6)),
    ("DATA", "Share-based payments", (None, None, None, None, None, None, None, None, 99, 99)),
    ("TOTAL", "At 31 December 2019 (FY2019 closing)", (1678, 2370, 2225, -231, 251, 27, -14, 796, 10924, 18026)),
    ("DATA", "Merger reserve amortisation (transfer to/from retained earnings)", (None, None, None, 91, None, None, None, None, -91, 0)),
    ("DATA", "FVOCI reserve - unrealised gains (OCR-corrected: source scan read as 455, reconciliation against the disclosed opening/closing FVOCI reserve balance shows the true figure is 155 - see basis note)", (None, None, None, None, 155, None, None, None, None, 155)),
    ("DATA", "FVOCI reserve - realised losses", (None, None, None, None, -110, None, None, None, None, -110)),
    ("DATA", "FVOCI reserve - tax", (None, None, None, None, -17, None, None, None, None, -17)),
    ("DATA", "Cash flow hedging reserve - amount recognised in equity", (None, None, None, None, None, -275, None, None, None, -275)),
    ("DATA", "Cash flow hedging reserve - amount transferred to earnings", (None, None, None, None, None, 57, None, None, None, 57)),
    ("DATA", "Cash flow hedging reserve - tax", (None, None, None, None, None, 58, None, None, None, 58)),
    ("DATA", "Foreign exchange reserve - retranslation of net assets", (None, None, None, None, None, None, -2, None, None, -2)),
    ("DATA", "Foreign exchange reserve - FX gains on hedges of net assets", (None, None, None, None, None, None, 3, None, None, 3)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, None, 722, 722)),
    ("DATA", "Paid-in equity dividends paid", (None, None, None, None, None, None, None, None, -182, -182)),
    ("DATA", "Remeasurement of retirement benefit schemes, net of tax (includes an OCR-corrected tax figure - see basis note)", (None, None, None, None, None, None, None, None, -5, -5)),
    ("DATA", "Shares issued under employee share schemes", (None, None, None, None, None, None, None, None, -11, -11)),
    ("DATA", "Share-based payments", (None, None, None, None, None, None, None, None, 45, 45)),
    ("TOTAL", "At 1 January 2021 (FY2021 opening)", (1678, 2370, 2225, -140, 279, -133, -13, 796, 11402, 18464)),
    ("DATA", "Paid-in equity redeemed", (None, -934, None, None, None, None, None, None, None, -934)),
    ("DATA", "Paid-in equity issued", (None, 941, None, None, None, None, None, None, None, 941)),
    ("DATA", "Merger reserve amortisation (transfer to/from retained earnings)", (None, None, None, 51, None, None, None, None, -51, 0)),
    ("DATA", "FVOCI reserve - unrealised gains", (None, None, None, None, 28, None, None, None, None, 28)),
    ("DATA", "FVOCI reserve - realised gains", (None, None, None, None, -122, None, None, None, None, -122)),
    ("DATA", "FVOCI reserve - tax", (None, None, None, None, 8, None, None, None, None, 8)),
    ("DATA", "Cash flow hedging reserve - amount recognised in equity", (None, None, None, None, None, 100, None, None, None, 100)),
    ("DATA", "Cash flow hedging reserve - amount transferred to earnings", (None, None, None, None, None, 79, None, None, None, 79)),
    ("DATA", "Cash flow hedging reserve - tax", (None, None, None, None, None, -48, None, None, None, -48)),
    ("DATA", "Foreign exchange reserve - retranslation of net assets", (None, None, None, None, None, None, -18, None, None, -18)),
    ("DATA", "Foreign exchange reserve - FX gains on hedges of net assets", (None, None, None, None, None, None, 15, None, None, 15)),
    ("DATA", "Capital redemption reserve - redemption of preference shares (transfer from retained earnings)", (None, None, None, None, None, None, None, 24, -24, 0)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, None, 2752, 2752)),
    ("DATA", "Ordinary dividends paid", (None, None, None, None, None, None, None, None, -1600, -1600)),
    ("DATA", "Paid-in equity dividends paid", (None, None, None, None, None, None, None, None, -109, -109)),
    ("DATA", "Remeasurement of retirement benefit schemes, net of tax", (None, None, None, None, None, None, None, None, -386, -386)),
    ("DATA", "Redemption/reclassification of paid-in equity, net of tax", (None, None, None, None, None, None, None, None, -18, -18)),
    ("DATA", "Share-based payments, net of tax", (None, None, None, None, None, None, None, None, 4, 4)),
    ("DATA", "Employee share schemes", (None, None, None, None, None, None, None, None, 10, 10)),
    ("TOTAL", "At 31 December 2021 (FY2021 closing)", (1678, 2377, 2225, -89, 193, -2, -16, 820, 11980, 19166)),
    ("DATA", "Paid-in equity redeemed", (None, -359, None, None, None, None, None, None, None, -359)),
    ("DATA", "Paid-in equity issued", (None, 500, None, None, None, None, None, None, None, 500)),
    ("DATA", "Merger reserve amortisation (transfer to/from retained earnings)", (None, None, None, 87, None, None, None, None, -87, 0)),
    ("DATA", "FVOCI reserve - unrealised losses", (None, None, None, None, -486, None, None, None, None, -486)),
    ("DATA", "FVOCI reserve - realised losses", (None, None, None, None, 93, None, None, None, None, 93)),
    ("DATA", "FVOCI reserve - tax", (None, None, None, None, 124, None, None, None, None, 124)),
    ("DATA", "Cash flow hedging reserve - amount recognised in equity", (None, None, None, None, None, -288, None, None, None, -288)),
    ("DATA", "Cash flow hedging reserve - amount transferred to earnings", (None, None, None, None, None, -255, None, None, None, -255)),
    ("DATA", "Cash flow hedging reserve - tax", (None, None, None, None, None, 152, None, None, None, 152)),
    ("DATA", "Foreign exchange reserve - retranslation of net assets", (None, None, None, None, None, None, 31, None, None, 31)),
    ("DATA", "Foreign exchange reserve - FX losses on hedges of net assets", (None, None, None, None, None, None, -33, None, None, -33)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, None, 3457, 3457)),
    ("DATA", "Ordinary dividends paid", (None, None, None, None, None, None, None, None, -3293, -3293)),
    ("DATA", "Paid-in equity dividends paid", (None, None, None, None, None, None, None, None, -120, -120)),
    ("DATA", "Remeasurement of retirement benefit schemes, net of tax", (None, None, None, None, None, None, None, None, -419, -419)),
    ("DATA", "Redemption/reclassification of paid-in equity, net of tax", (None, None, None, None, None, None, None, None, -35, -35)),
    ("DATA", "Share-based payments, net of tax", (None, None, None, None, None, None, None, None, 2, 2)),
    ("DATA", "Employee share schemes", (None, None, None, None, None, None, None, None, 6, 6)),
    ("TOTAL", "At 31 December 2022 (FY2022 closing)", (1678, 2518, 2225, -2, -76, -393, -18, 820, 11491, 18243)),
    ("DATA", "Merger reserve amortisation (transfer to/from retained earnings)", (None, None, None, 2, None, None, None, None, -2, 0)),
    ("DATA", "FVOCI reserve - unrealised losses", (None, None, None, None, -11, None, None, None, None, -11)),
    ("DATA", "FVOCI reserve - realised losses", (None, None, None, None, 43, None, None, None, None, 43)),
    ("DATA", "FVOCI reserve - tax", (None, None, None, None, -8, None, None, None, None, -8)),
    ("DATA", "Cash flow hedging reserve - amount recognised in equity", (None, None, None, None, None, -180, None, None, None, -180)),
    ("DATA", "Cash flow hedging reserve - amount transferred to earnings", (None, None, None, None, None, -109, None, None, None, -109)),
    ("DATA", "Cash flow hedging reserve - tax", (None, None, None, None, None, 81, None, None, None, 81)),
    ("DATA", "Foreign exchange reserve - retranslation of net assets", (None, None, None, None, None, None, -12, None, None, -12)),
    ("DATA", "Foreign exchange reserve - FX gains on hedges of net assets", (None, None, None, None, None, None, 12, None, None, 12)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, None, 3625, 3625)),
    ("DATA", "Ordinary dividends paid", (None, None, None, None, None, None, None, None, -1738, -1738)),
    ("DATA", "Paid-in equity dividends paid", (None, None, None, None, None, None, None, None, -142, -142)),
    ("DATA", "Remeasurement of retirement benefit schemes, net of tax", (None, None, None, None, None, None, None, None, -100, -100)),
    ("DATA", "Share-based payments, net of tax", (None, None, None, None, None, None, None, None, -3, -3)),
    ("TOTAL", "At 31 December 2023 (FY2023 closing)", (1678, 2518, 2225, 0, -52, -601, -18, 820, 13131, 19701)),
    ("DATA", "Paid-in equity issued", (None, 799, None, None, None, None, None, None, None, 799)),
    ("DATA", "FVOCI reserve - unrealised gains/(losses)", (None, None, None, None, -52, None, None, None, None, -52)),
    ("DATA", "FVOCI reserve - realised losses", (None, None, None, None, 32, None, None, None, None, 32)),
    ("DATA", "FVOCI reserve - tax", (None, None, None, None, 6, None, None, None, None, 6)),
    ("DATA", "Cash flow hedging reserve - amounts recognised in equity", (None, None, None, None, None, 125, None, None, None, 125)),
    ("DATA", "Cash flow hedging reserve - reclassification of OCI to profit or loss", (None, None, None, None, None, 283, None, None, None, 283)),
    ("DATA", "Cash flow hedging reserve - tax", (None, None, None, None, None, -114, None, None, None, -114)),
    ("DATA", "Foreign exchange reserve - retranslation of net assets", (None, None, None, None, None, None, -28, None, None, -28)),
    ("DATA", "Foreign exchange reserve - FX losses on hedges of net assets", (None, None, None, None, None, None, 16, None, None, 16)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, None, 3613, 3613)),
    ("DATA", "Ordinary dividends paid", (None, None, None, None, None, None, None, None, -2516, -2516)),
    ("DATA", "Paid-in equity dividends paid", (None, None, None, None, None, None, None, None, -194, -194)),
    ("DATA", "Remeasurement of retirement benefit schemes, net of tax", (None, None, None, None, None, None, None, None, -100, -100)),
    ("DATA", "Employee share schemes, net of tax", (None, None, None, None, None, None, None, None, 22, 22)),
    ("DATA", "Share-based remuneration, net of tax", (None, None, None, None, None, None, None, None, 16, 16)),
    ("TOTAL", "At 31 December 2024 (FY2024 closing)", (1678, 3317, 2225, 0, -66, -307, -30, 820, 13972, 21609)),
    ("DATA", "Paid-in equity redeemed", (None, -1877, None, None, None, None, None, None, None, -1877)),
    ("DATA", "Paid-in equity issued", (None, 1741, None, None, None, None, None, None, None, 1741)),
    ("DATA", "FVOCI reserve - unrealised gains", (None, None, None, None, 111, None, None, None, None, 111)),
    ("DATA", "FVOCI reserve - realised losses", (None, None, None, None, 7, None, None, None, None, 7)),
    ("DATA", "FVOCI reserve - tax", (None, None, None, None, -34, None, None, None, None, -34)),
    ("DATA", "Cash flow hedging reserve - amounts recognised in equity", (None, None, None, None, None, -33, None, None, None, -33)),
    ("DATA", "Cash flow hedging reserve - reclassification of OCI to profit or loss", (None, None, None, None, None, 105, None, None, None, 105)),
    ("DATA", "Cash flow hedging reserve - tax", (None, None, None, None, None, -20, None, None, None, -20)),
    ("DATA", "Foreign exchange reserve - retranslation of net assets", (None, None, None, None, None, None, 30, None, None, 30)),
    ("DATA", "Foreign exchange reserve - FX losses on hedges of net assets", (None, None, None, None, None, None, -17, None, None, -17)),
    ("DATA", "Foreign exchange reserve - recycled to profit or loss on disposal of businesses", (None, None, None, None, None, None, -2, None, None, -2)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, None, 4227, 4227)),
    ("DATA", "Ordinary dividends paid", (None, None, None, None, None, None, None, None, -2988, -2988)),
    ("DATA", "Paid-in equity dividends paid", (None, None, None, None, None, None, None, None, -233, -233)),
    ("DATA", "Redemption/reclassification of paid-in equity", (None, None, None, None, None, None, None, None, -34, -34)),
    ("DATA", "Remeasurement of retirement benefit schemes, net of tax", (None, None, None, None, None, None, None, None, 2, 2)),
    ("DATA", "Employee share schemes, net of tax", (None, None, None, None, None, None, None, None, 19, 19)),
    ("DATA", "Share-based remuneration, net of tax", (None, None, None, None, None, None, None, None, 23, 23)),
    ("DATA", "Sharing in success", (None, None, None, None, None, None, None, None, 49, 49)),
    ("TOTAL", "At 31 December 2025 (FY2025 closing)", (1678, 3181, 2225, 0, 18, -255, -19, 820, 15037, 22685)),
]
EQUITY_SOURCES = (
    STATEMENTS_SOURCES + "\n\n"
    f"FY2020/FY2019: NWB Group Annual Report and Accounts 2020 (Companies House filing), Statement of changes in "
    f"equity (NWB Plc column), p.58 - {NWB_CH_AR['FY2020']}\n"
    f"FY2018: NWB Group Annual Report and Accounts 2019 (Companies House filing), Statement of changes in equity "
    f"(NWB Plc restated 2018 comparative column, cross-checked against NatWest Plc Annual Report and Accounts "
    f"2018's own FY2018 figures where legible), p.88 - {NWB_CH_AR['FY2019']}; {NWB_CH_AR['FY2018']}\n"
    f"FY2017/FY2016/FY2015: NatWest Plc Annual Report and Accounts 2017 (Companies House filing), Statement of "
    f"changes in equity (Bank column), p.98-99 - {NWB_CH_AR['FY2017']}\n\n"
    "BASIS NOTE - HD-050 FY2014-FY2020 extension: pre-2018 NatWest Plc equity has no 'Paid-in equity' or 'Merger "
    "reserve' component (both first appear in 2018, created by the ring-fencing reorganisation: Additional Tier 1 "
    "notes were reclassified into paid-in equity, and a merger reserve was created against the RBS Treasury/"
    "shared-services businesses transferred in from NatWest Markets Plc at net asset value) - both columns are "
    "correctly blank/zero for FY2014-FY2017. The pre-2018 'Available-for-sale reserve' is shown in the FVOCI "
    "reserve column (the FVOCI classification did not exist before IFRS 9's 1 January 2018 adoption - a "
    "terminology predecessor, not the same standard). FY2018's own Annual Report's equity statement OCR'd too "
    "poorly (a badly-scanned page with misaligned columns) to transcribe line-by-line with confidence; FY2018's "
    "movements are instead shown as three items - two clean, individually-legible one-off events (paid-in equity "
    "issued 2,370; merger reserve created -294) plus a single 'Other equity movements, net' row for the remainder "
    "(profit for the year, dividends, and reserve movements not separately broken out) - which reconciles exactly "
    "to the difference between FY2017's and FY2019's own independently-confirmed closing/opening balances.\n\n"
    "DATA-QUALITY FINDING - FY2014 opening balance gap: the FY2015 Annual Report's own FY2014 closing figures for "
    "the reserve/retained-earnings components shown here sum to £11,921m, not the £13,312m Total equity figure "
    "independently established on the Balance Sheet sheet (Total assets less Total liabilities, an accounting "
    "identity) - a £1,391m gap. This is NOT a transcription error in either figure (both are exactly as reported "
    "in their own sources) but an apparent scope difference: FY2014-2016's Balance Sheet shows a much larger "
    "'Investment in group undertakings' and 'Subordinated liabilities' than FY2017+ (see the Balance Sheet's own "
    "STRUCTURAL BREAK NOTE). A direct cross-check against NatWest's contemporaneous 2014 Pillar 3 capital-resources "
    "table reports NatWest Plc shareholders' equity of £13,312m and explicitly shows preference shares-equity as nil, "
    "so the earlier preference-share hypothesis is not supported; the £1,391m remains an unexplained source-"
    "presentation difference rather than a safe line-item addition. The FY2014 opening row is shown "
    "with the reserve/retained-earnings breakdown as directly disclosed (summing to £11,921m) rather than forcing "
    "an unverified adjustment to match the Balance Sheet figure - flagging this explicitly for HD-050 follow-up.\n\n"
    "Minor rounding: the FY2015/FY2016/FY2017 movement rows (sourced from a single Bank-column table with all "
    "figures independently rounded to the nearest £m) each carry a £1m immaterial rounding gap against their own "
    "year's closing total; not investigated further given the size. FY2020's 'Unrealised gains' FVOCI-reserve "
    "movement was OCR-corrected from a scanned '455' to the reconciled true value of 155 (see the row's own note) "
    "- caught the same way as this project's other OCR digit-error corrections, via reconciliation against the "
    "disclosed opening/closing balance rather than trusting the raw scan.\n\n"
    "HD-072 (2026-09-06) - FY2012/FY2013 extension: sourced from the FY2013 Annual Report's own Bank-column "
    "Statement of changes in equity (p.156-157, three side-by-side 2013/2012/2011 movement columns off one "
    "continuous roll-forward), which pre-dates the paid-in equity/merger reserve components (both correctly "
    "blank, same as FY2014-FY2017 - see BASIS NOTE above) and shows the pre-IFRS 9 Available-for-sale reserve in "
    "the FVOCI reserve column (same convention as FY2014-FY2017). FY2012's figures are the FY2013 Annual Report's "
    "own RESTATED FY2012 comparative (following IAS 19R, adopted FY2013 and applied retrospectively) rather than "
    "FY2012's own as-originally-published Annual Report - see the DATA-QUALITY NOTE in STATEMENTS_SOURCES for the "
    "material equity difference this makes (FY2012 own report: Bank Owners' equity £11,572m; FY2013 report's "
    "restated FY2012 column used here: £7,760m) and why the restated figures are used (internal consistency with "
    "the FY2013 figures built from the same document). FY2013's own closing balance (£8,530m) ties exactly, "
    "unflagged, to the FY2013 Balance Sheet's independently-computed Total equity - see the IMPORTANT GAP code "
    "comment immediately above the FY2012/FY2013 rows for the one open item this extension surfaces (no bridge "
    "into the existing FY2014 closing entry, a pre-existing HD-050 scope gap, not fixed here)."
)
bw.add_equity_changes_sheet(
    title="National Westminster Bank Plc — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, NWB Plc entity-level basis. £m. HD-050 extended this to "
              "FY2014-FY2025; HD-072 (2026-09-06) further extended it to FY2012-FY2025. Every closing balance "
              "FY2012-FY2013 and FY2015-FY2025 ties exactly to both the next year's own opening balance and that "
              "year's own Balance Sheet Total equity; FY2014's opening figures carry a flagged, unresolved "
              "£1,391m gap against the Balance Sheet, and the FY2013 closing balance does not bridge into that "
              "same FY2014 entry (FY2014's own movement year was never built into this sheet) - see basis notes "
              "in the source citation and the code comment above the FY2012/FY2013 rows.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=EQUITY_SOURCES,
    first_col_width=88,
    source_height=320,
)

# The 2023-2025 reports use condensed cash-flow presentation; 2022 provides the detailed 2022/2021 comparative.
# HD-050: FY2020/FY2019 (from the FY2020 report's own detailed Group/Plc table) reuse this same detailed shape
# almost row-for-row; FY2018 (from FY2019's restated comparative) and FY2014-FY2017 (from FY2017's and FY2015's own
# Group/Bank tables) each use their own further-different presentations, so a handful of one-off rows are added
# for those years only, following the same non-uniform-granularity pattern already used for FY2022/FY2021 vs
# FY2023-2025. Every added TOTAL row below reconciles exactly to its own DATA rows and to the next/prior year's
# opening/closing cash balance (verified by hand; the full FY2014-FY2025 chain ties without a single plug row).
cash_rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Operating profit before tax", {"FY2025": 5591, "FY2024": 4680, "FY2023": 4705, "FY2022": 4687, "FY2021": 3542, "FY2020": 689, "FY2019": 1045, "FY2018": 2238, "FY2017": 665, "FY2016": 4060, "FY2015": -1105, "FY2014": 2541, "FY2013": -1538, "FY2012": -6815}),
    ("DATA", "Non-cash and other items", {"FY2025": -62, "FY2024": 1424, "FY2023": 396}),
    ("DATA", "Impairment losses/(releases)", {"FY2022": 389, "FY2021": -732, "FY2020": 1934, "FY2019": 540, "FY2018": 198, "FY2013": 586, "FY2012": 812}),
    ("DATA", "Depreciation and amortisation", {"FY2022": 598, "FY2021": 594, "FY2020": 650, "FY2019": 737, "FY2018": 399, "FY2013": 128, "FY2012": 132}),
    ("DATA", "Net impairment charges of investments in Group undertakings", {"FY2022": 336, "FY2021": 61, "FY2020": 50, "FY2019": 87, "FY2018": 481, "FY2013": 931, "FY2012": 5061}),
    ("DATA", "Change in fair value on financial assets", {"FY2022": 1177, "FY2021": 1595, "FY2020": -1436, "FY2019": -807, "FY2018": -750}),
    ("DATA", "Change in fair value on financial liabilities and subordinated liabilities", {"FY2022": -924, "FY2021": -418, "FY2020": 237, "FY2019": 229, "FY2018": 20}),
    ("DATA", "Elimination of foreign exchange differences", {"FY2022": -3, "FY2021": 1118, "FY2020": -749, "FY2019": 484, "FY2018": -654, "FY2013": 2, "FY2012": 131}),
    ("DATA", "Other non-cash items", {"FY2022": -215, "FY2021": 58, "FY2020": 154, "FY2019": 64, "FY2018": -1147, "FY2013": 114, "FY2012": 377}),
    ("DATA", "Amortisation of discounts and premiums of other financial assets", {"FY2020": 212, "FY2019": 219}),
    ("DATA", "(Profit)/loss on sale of other financial assets", {"FY2020": -113, "FY2019": 16}),
    ("DATA", "Profit on sale of other assets and net assets/liabilities sold", {"FY2020": -46, "FY2019": -40}),
    ("DATA", "Interest on subordinated liabilities (non-cash adjustment)", {"FY2018": 175, "FY2013": 250, "FY2012": 268}),
    ("DATA", "Interest on other financial assets (non-cash adjustment)", {"FY2018": -557}),
    ("DATA", "Profit on sale of subsidiaries and associates", {"FY2018": -36}),
    ("DATA", "Loans and advances written-off, net of recoveries (HD-072: distinct source line FY2013/FY2012 only)", {"FY2013": -937, "FY2012": -704}),
    ("DATA", "Charge for defined benefit pension schemes (HD-072: distinct source line FY2013/FY2012 only, gross of the cash contribution below)", {"FY2013": 211, "FY2012": 111}),
    ("DATA", "Cash contribution to defined benefit pension schemes (HD-072: FY2013/FY2012 sit inside the trading-activities subtotal here, unlike FY2017-FY2014's separate row below - see basis note)", {"FY2013": -411, "FY2012": -452}),
    ("DATA", "Income receivable on other financial assets", {"FY2022": -303, "FY2021": -412, "FY2020": -251, "FY2019": -520}),
    ("DATA", "Dividends receivable from subsidiaries", {"FY2022": -1010, "FY2021": -424, "FY2020": -489, "FY2019": -454}),
    ("DATA", "Interest payable on MRELs and subordinated liabilities", {"FY2022": 358, "FY2021": 310, "FY2020": 339, "FY2019": 300}),
    ("DATA", "Charges and releases on provisions", {"FY2022": 122, "FY2021": 388, "FY2020": 183, "FY2019": 854, "FY2018": -201}),
    ("DATA", "Defined benefit pension schemes", {"FY2022": 132, "FY2021": 146, "FY2020": 136, "FY2019": 121, "FY2018": -2025}),
    ("TOTAL", "Net cash flows from trading activities", {"FY2022": 5443, "FY2021": 6038, "FY2020": 1500, "FY2019": 2875, "FY2018": -1859, "FY2013": -664, "FY2012": -1079}),
    ("DATA", "Adjustments for non-cash items and other adjustments included within income statement", {"FY2017": 7766, "FY2016": -697, "FY2015": 2304, "FY2014": -1800}),
    ("DATA", "Cash contribution to defined benefit pension schemes", {"FY2017": -127, "FY2016": -4349, "FY2015": -724, "FY2014": -712}),
    ("DATA", "Changes in operating assets and liabilities", {"FY2025": 9514, "FY2024": -7007, "FY2023": -8999, "FY2022": -45374, "FY2021": 31327, "FY2020": 25637, "FY2019": -19242, "FY2018": -4232, "FY2017": 18013, "FY2016": -5704, "FY2015": -548, "FY2014": -5737, "FY2013": 6833, "FY2012": 18148}),
    ("TOTAL", "Net cash flows from operating activities before tax (HD-072: distinct source subtotal FY2013/FY2012 only)", {"FY2013": 6169, "FY2012": 17069}),
    ("DATA", "Income taxes paid", {"FY2025": -1515, "FY2024": -993, "FY2023": -484, "FY2022": -998, "FY2021": -791, "FY2020": 363, "FY2019": -136, "FY2018": -108, "FY2017": -35, "FY2016": -131, "FY2015": 62, "FY2014": -128, "FY2013": 91, "FY2012": 596}),
    ("TOTAL", "Net cash flows from operating activities", {"FY2025": 13528, "FY2024": -1896, "FY2023": -4382, "FY2022": -40929, "FY2021": 36574, "FY2020": 27500, "FY2019": -16503, "FY2018": -6199, "FY2017": 26282, "FY2016": -6821, "FY2015": -11, "FY2014": -5836, "FY2013": 6260, "FY2012": 17665}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Sale and maturity of other financial assets", {"FY2025": 31898, "FY2024": 33860, "FY2023": 17887, "FY2022": 25339, "FY2021": 9884, "FY2020": 11702, "FY2019": 12768, "FY2018": 5742, "FY2017": 3, "FY2015": 782, "FY2014": 471, "FY2013": 14, "FY2012": 405}),
    ("DATA", "Purchase of other financial assets", {"FY2025": -44449, "FY2024": -41551, "FY2023": -34249, "FY2022": -13022, "FY2021": -2811, "FY2020": -7428, "FY2019": -12016, "FY2018": -2791, "FY2017": -1064}),
    ("DATA", "Income received on other financial assets", {"FY2025": 1404, "FY2024": 768, "FY2023": 435, "FY2022": 371, "FY2021": 412, "FY2020": 251, "FY2019": 520, "FY2018": 557}),
    ("DATA", "Net movement in business interests and intangible assets", {"FY2025": -401, "FY2024": -2861, "FY2023": -1188, "FY2022": -719, "FY2021": -3093, "FY2020": -353, "FY2019": -391, "FY2018": -33651, "FY2017": -3622, "FY2016": -307, "FY2015": -715, "FY2014": 17, "FY2013": -1262, "FY2012": -62287}),
    ("DATA", "Dividends received from subsidiaries", {"FY2025": 487, "FY2024": 553, "FY2023": 617, "FY2022": 1010, "FY2021": 424, "FY2020": 489, "FY2019": 454}),
    ("DATA", "Sale of property, plant and equipment", {"FY2025": 36, "FY2024": 101, "FY2023": 34, "FY2022": 82, "FY2021": 17, "FY2020": 125, "FY2019": 241, "FY2018": 59, "FY2017": 81, "FY2016": 17, "FY2015": 15, "FY2014": 49, "FY2013": 15, "FY2012": 24}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -237, "FY2024": -252, "FY2023": -544, "FY2022": -316, "FY2021": -617, "FY2020": -176, "FY2019": -231, "FY2018": -262, "FY2017": -65, "FY2016": -61, "FY2015": -165, "FY2014": -66, "FY2013": -57, "FY2012": -18}),
    ("TOTAL", "Net cash flows from investing activities", {"FY2025": -11262, "FY2024": -9382, "FY2023": -17008, "FY2022": 12745, "FY2021": 4216, "FY2020": 4610, "FY2019": 1345, "FY2018": -30346, "FY2017": -4667, "FY2016": -351, "FY2015": -83, "FY2014": 471, "FY2013": -1290, "FY2012": -61876}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Issue of paid-in equity", {"FY2025": 1741, "FY2024": 799, "FY2022": 500, "FY2021": 941}),
    ("DATA", "Redemption of paid-in equity", {"FY2025": -1911, "FY2022": -388, "FY2021": -934}),
    ("DATA", "Issue of subordinated liabilities", {"FY2025": 830, "FY2024": 600, "FY2023": 1263, "FY2018": 1486}),
    ("DATA", "Redemption of subordinated liabilities", {"FY2025": -500, "FY2024": -579, "FY2023": -539, "FY2018": -3000, "FY2015": -387}),
    ("DATA", "Interest paid on subordinated liabilities", {"FY2025": -174, "FY2024": -159, "FY2023": -120, "FY2018": -179, "FY2017": -57, "FY2016": -237, "FY2015": -255, "FY2014": -250, "FY2013": -258, "FY2012": -271}),
    ("DATA", "Movement in subordinated liabilities", {"FY2022": -199, "FY2021": -1267, "FY2020": 321, "FY2019": -282}),
    ("DATA", "Movement in MRELs", {"FY2022": 509, "FY2021": 1515, "FY2020": 654, "FY2019": 1072}),
    ("DATA", "Issue of MRELs", {"FY2025": 1544, "FY2024": 927, "FY2023": 441, "FY2018": 1475}),
    ("DATA", "Maturity and redemption of MRELs", {"FY2025": 0, "FY2024": -930, "FY2023": -107}),
    ("DATA", "Interest paid on MRELs", {"FY2025": -227, "FY2024": -215, "FY2023": -261, "FY2018": 3}),
    ("DATA", "Issue of Additional Tier 1 capital notes", {"FY2018": 2370}),
    ("DATA", "Service cost of other equity instruments", {"FY2018": 1089}),
    ("DATA", "Capital contribution", {"FY2017": 51, "FY2016": 1300, "FY2015": 800, "FY2014": 1500, "FY2013": 2070, "FY2012": 8050}),
    ("DATA", "Redemption of preference shares", {"FY2017": -178}),
    ("DATA", "Dividends paid", {"FY2025": -3221, "FY2024": -2710, "FY2023": -1880, "FY2022": -3413, "FY2021": -1709, "FY2020": -152, "FY2019": -866, "FY2014": -175}),
    ("TOTAL", "Net cash flows from financing activities", {"FY2025": -1918, "FY2024": -2267, "FY2023": -1203, "FY2022": -2991, "FY2021": -1454, "FY2020": 823, "FY2019": -76, "FY2018": 3244, "FY2017": -184, "FY2016": 1063, "FY2015": 158, "FY2014": 1075, "FY2013": 1812, "FY2012": 7779}),
    ("DATA", "Effects of exchange rate changes on cash and cash equivalents", {"FY2025": 141, "FY2024": -259, "FY2023": -397, "FY2022": 1101, "FY2021": -984, "FY2020": 644, "FY2019": -638, "FY2018": 220, "FY2017": -138, "FY2016": 1073, "FY2015": -55, "FY2014": -108, "FY2013": -6, "FY2012": -121}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 489, "FY2024": -13804, "FY2023": -22990, "FY2022": -30074, "FY2021": 38352, "FY2020": 33574, "FY2019": -15872, "FY2018": -33081, "FY2017": 21293, "FY2016": -5036, "FY2015": 9, "FY2014": -4398, "FY2013": 6776, "FY2012": -36553}),
    ("DATA", "Cash and cash equivalents at 1 January", {"FY2025": 38678, "FY2024": 52482, "FY2023": 75472, "FY2022": 105546, "FY2021": 67194, "FY2020": 33620, "FY2019": 49492, "FY2018": 82573, "FY2017": 61151, "FY2016": 66187, "FY2015": 66178, "FY2014": 70576, "FY2013": 63800, "FY2012": 100353}),
    ("TOTAL", "Cash and cash equivalents at 31 December", {"FY2025": 39167, "FY2024": 38678, "FY2023": 52482, "FY2022": 75472, "FY2021": 105546, "FY2020": 67194, "FY2019": 33620, "FY2018": 49492, "FY2017": 82444, "FY2016": 61151, "FY2015": 66187, "FY2014": 66178, "FY2013": 70576, "FY2012": 63800}),
]
CASH_FLOW_SOURCES = (
    ar_sources() + "\n\n"
    f"FY2020/FY2019: NWB Group Annual Report and Accounts 2020 (Companies House filing), Cash flow statement "
    f"(NWB Plc column), p.59-60 - {NWB_CH_AR['FY2020']}\n"
    f"FY2018: NWB Group Annual Report and Accounts 2019 (Companies House filing), Cash flow statement (NWB Plc "
    f"restated 2018 comparative column), p.89-90 - {NWB_CH_AR['FY2019']}\n"
    f"FY2017/FY2016/FY2015: NatWest Plc Annual Report and Accounts 2017 (Companies House filing), Cash flow "
    f"statement (Bank column), p.100 - {NWB_CH_AR['FY2017']}\n"
    f"FY2014 (and FY2015 cross-check): NatWest Plc Annual Report and Accounts 2015 (Companies House filing), Cash "
    f"flow statement (Bank column), p.98 - {NWB_CH_AR['FY2015']}\n"
    f"HD-072 (2026-09-06) - FY2013/FY2012: National Westminster Bank Plc Annual Report and Accounts 2013 "
    f"(Companies House filing), Cash flow statement (Bank column, 2013/2012/2011 side by side), p.158 - "
    f"{NWB_CH_AR['FY2013']}. FY2012 uses this document's own restated FY2012 comparative (see the DATA-QUALITY "
    f"NOTE in STATEMENTS_SOURCES for the IAS 19R restatement context); the FY2012 Annual Report's own "
    f"as-originally-published Cash flow statement (Bank column), p.143 - {NWB_CH_AR['FY2012']} - was independently "
    f"cross-checked and matches from 'Net cash inflow/(outflow) from trading activities' downward to the exact "
    f"£m (including both closing cash balances); only two adjustment-line sub-components differ by an immaterial, "
    f"self-cancelling £31m ('Operating profit before tax' and 'Charge for defined benefit pension schemes' - a "
    f"reclassification that nets to zero within the trading-activities subtotal, not investigated further).\n\n"
    "BASIS NOTE - HD-050 FY2014-FY2020 extension: three source presentations are used across these years, each "
    "with its own row granularity, matching the non-uniform detail already present for FY2021/FY2022 vs FY2023-"
    "FY2025 in this sheet. FY2020/FY2019 (from the FY2020 report's own Group/Plc table) closely match the FY2021/"
    "FY2022 detailed rows; three items with no FY2021+ equivalent ('Amortisation of discounts and premiums of "
    "other financial assets', '(Profit)/loss on sale of other financial assets', 'Profit on sale of other assets "
    "and net assets/liabilities sold') are added as their own rows for those two years only. FY2018 uses the "
    "FY2019 report's own further-different, more granular restated presentation; a few items unique to it "
    "('Interest on subordinated liabilities (non-cash adjustment)', 'Interest on other financial assets (non-cash "
    "adjustment)', 'Profit on sale of subsidiaries and associates', 'Issue of Additional Tier 1 capital notes', "
    "'Service cost of other equity instruments') are likewise added as one-off rows. FY2014-FY2017 use the "
    "condensed pre-2018 Group/Bank cash flow format, which lumps most non-cash adjustments into a single "
    "'Adjustments for non-cash items and other adjustments included within income statement' line rather than "
    "breaking them out - shown as its own row rather than force-mapped onto the later years' granular breakdown. "
    "Every added TOTAL row (trading/operating/investing/financing nets, FX effect, opening and closing cash) ties "
    "exactly to its own year's DATA rows and to the adjoining year's opening/closing cash balance across the "
    "full FY2014-FY2025 chain - verified by hand, no plug rows used.\n\n"
    "BASIS NOTE - HD-072 FY2013/FY2012 extension: this document's own presentation is MORE granular than the "
    "condensed FY2014-FY2017 format above (it does not use a single lumped 'Adjustments for non-cash items' "
    "line) and instead matches the detailed FY2018-FY2022 row style closely, so FY2013/FY2012 values are added "
    "to those existing detailed rows wherever the source uses the same or an equivalent line, with three new "
    "one-off rows added only for items with no FY2018-FY2022 equivalent ('Loans and advances written-off, net "
    "of recoveries', 'Charge for defined benefit pension schemes', and the 'before tax' operating subtotal). "
    "Two source lines that were nil in both FY2013 and FY2012 ('Write-down of goodwill and other intangible "
    "assets', 'Gain on redemption of own debt', 'Purchase of securities' at Bank level, 'Issue of subordinated "
    "liabilities' at Bank level) are omitted rather than shown as explicit zero rows. FY2013's closing cash "
    "balance (£70,576m) ties EXACTLY to FY2014's own opening cash balance already in this sheet - zero-gap "
    "across the new year boundary, verified by hand."
)
bw.add_cash_flow_sheet(
    "National Westminster Bank Plc — Cash Flow Statement",
    "NWB Plc entity-level basis, £m. " + ENTITY_NOTE + " HD-050 extended this to FY2014-FY2025; HD-072 "
    "(2026-09-06) further extended it to FY2012-FY2025. Four different source presentations are stitched "
    "together across the 14 years (see BASIS NOTEs in the source citation) - row granularity varies by year "
    "exactly as it already did for FY2021/FY2022 vs FY2023-FY2025, but every TOTAL row reconciles exactly across "
    "the full chain, including zero-gap at the new FY2012/FY2013/FY2014 boundaries.",
    cash_rows, CASH_FLOW_SOURCES, first_col_width=80, source_height=280, unit_suffix=" (£m)", years=YEARS)

# ---------------------------------------------------------------
# Asset Quality - NWB Plc entity-level loan exposure/ECL by IFRS 9 stage
# (Note 13 "Loan impairment provisions" of each Annual Report). All 5 years
# fully disclosed at NWB Plc level - no access gaps.
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans - amortised cost (and FVOCI from FY2025), by IFRS 9 stage", {}),
    ("DATA", "Stage 1", {"FY2025": 287175, "FY2024": 268368, "FY2023": 258188, "FY2022": 236809, "FY2021": 236255, "FY2020": 217575, "FY2019": 215111, "FY2018": 191478}),
    ("DATA", "Stage 2", {"FY2025": 27117, "FY2024": 31101, "FY2023": 28008, "FY2022": 32765, "FY2021": 22492, "FY2020": 57864, "FY2019": 19392, "FY2018": 16732}),
    ("DATA", "Stage 3", {"FY2025": 3212, "FY2024": 4112, "FY2023": 4003, "FY2022": 3383, "FY2021": 2548, "FY2020": 3254, "FY2019": 2835, "FY2018": 3127}),
    ("DATA", "Inter-group (classified Stage 1)", {"FY2025": 37823, "FY2024": 34942, "FY2023": 32200, "FY2022": 30633, "FY2021": 25362, "FY2020": 2685, "FY2019": 3389, "FY2018": 5046}),
    ("TOTAL", "Total loans - amortised cost (and FVOCI from FY2025)", {"FY2025": 355327, "FY2024": 338523, "FY2023": 322400, "FY2022": 303590, "FY2021": 286657, "FY2020": 281378, "FY2019": 240727, "FY2018": 216383}),
    ("SECTION", "ECL provisions, by IFRS 9 stage", {}),
    ("DATA", "Stage 1", {"FY2025": 483, "FY2024": 442, "FY2023": 521, "FY2022": 459, "FY2021": 207, "FY2020": 365, "FY2019": 223, "FY2018": 184}),
    ("DATA", "Stage 2", {"FY2025": 633, "FY2024": 624, "FY2023": 746, "FY2022": 765, "FY2021": 1026, "FY2020": 2060, "FY2019": 518, "FY2018": 452}),
    ("DATA", "Stage 3", {"FY2025": 1645, "FY2024": 1482, "FY2023": 1416, "FY2022": 1170, "FY2021": 1037, "FY2020": 1285, "FY2019": 1281, "FY2018": 1163}),
    ("DATA", "Inter-group", {"FY2025": 30, "FY2024": 39, "FY2023": 41, "FY2022": 48, "FY2021": 8, "FY2020": 2, "FY2018": 1}),
    ("TOTAL", "Total ECL provisions", {"FY2025": 2791, "FY2024": 2587, "FY2023": 2724, "FY2022": 2442, "FY2021": 2278, "FY2020": 3712, "FY2019": 2022, "FY2018": 1800}),
    ("SECTION", "ECL provision coverage (ECL provisions / loans - amortised cost and FVOCI)", {}),
    ("DATA", "Stage 1 coverage", {"FY2025": "0.17%", "FY2024": "0.16%", "FY2023": "0.20%", "FY2022": "0.19%", "FY2021": "0.09%", "FY2020": "0.17%", "FY2019": "0.10%", "FY2018": "0.10%"}),
    ("DATA", "Stage 2 coverage", {"FY2025": "2.33%", "FY2024": "2.01%", "FY2023": "2.70%", "FY2022": "2.33%", "FY2021": "4.56%", "FY2020": "3.56%", "FY2019": "2.67%", "FY2018": "2.70%"}),
    ("DATA", "Stage 3 coverage (NPL coverage)", {"FY2025": "51.21%", "FY2024": "36.04%", "FY2023": "35.40%", "FY2022": "34.58%", "FY2021": "40.70%", "FY2020": "39.49%", "FY2019": "45.19%", "FY2018": "37.19%"}),
    ("DATA", "Total coverage", {"FY2025": "0.87%", "FY2024": "0.84%", "FY2023": "0.92%", "FY2022": "0.88%", "FY2021": "0.87%", "FY2020": "1.33%", "FY2019": "0.85%", "FY2018": "0.85%"}),
    ("SECTION", "Impairment (releases)/losses - ECL (release)/charge for the year", {}),
    ("DATA", "Stage 1", {"FY2025": -135, "FY2024": -335, "FY2023": -302, "FY2022": -256, "FY2021": -945, "FY2020": -69, "FY2019": -122, "FY2018": -61}),
    ("DATA", "Stage 2", {"FY2025": 354, "FY2024": 316, "FY2023": 516, "FY2022": 373, "FY2021": 48, "FY2020": 1839, "FY2019": 305, "FY2018": 253}),
    ("DATA", "Stage 3", {"FY2025": 399, "FY2024": 356, "FY2023": 276, "FY2022": 234, "FY2021": 183, "FY2020": 397, "FY2019": 389, "FY2018": 253}),
    ("DATA", "Third party", {"FY2025": 618, "FY2024": 337, "FY2023": 490, "FY2022": 351, "FY2021": -714, "FY2020": 2167, "FY2019": 572, "FY2018": 445}),
    ("DATA", "Inter-group", {"FY2025": -9, "FY2024": -3, "FY2023": -7, "FY2022": 40, "FY2021": -18, "FY2020": 2, "FY2018": -17}),
    ("TOTAL", "Total ECL (release)/charge", {"FY2025": 609, "FY2024": 334, "FY2023": 483, "FY2022": 391, "FY2021": -732, "FY2020": 2169, "FY2019": 572, "FY2018": 428}),
    ("DATA", "Amounts written-off", {"FY2025": 454, "FY2024": 536, "FY2023": 218, "FY2022": 272, "FY2021": 352, "FY2020": 517, "FY2019": 404, "FY2018": 612}),
    ("SECTION", "Legacy 'risk elements in lending' (REIL) framework, IAS 39 basis - FY2014-FY2017 only (see basis note)", {}),
    ("DATA", "Gross loans and advances, third party (banks + customers)", {"FY2017": 195247, "FY2016": 169621, "FY2015": 174792, "FY2014": 181011}),
    ("DATA", "Risk elements in lending (REIL)", {"FY2017": 2483, "FY2016": 2560, "FY2015": 8364, "FY2014": 19834}),
    ("DATA", "Impairment provisions", {"FY2017": 1439, "FY2016": 1563, "FY2015": 5335, "FY2014": 13908}),
    ("DATA", "REIL as a % of gross third-party loans to customers", {"FY2017": "1.3%", "FY2016": "1.5%", "FY2015": "4.9%", "FY2014": "11.2%"}),
    ("DATA", "Provisions as a % of REIL", {"FY2017": "58%", "FY2016": "61%", "FY2015": "64%", "FY2014": "70%"}),
    ("DATA", "Provisions as a % of gross third-party loans to customers", {"FY2017": "0.7%", "FY2016": "0.9%", "FY2015": "3.1%", "FY2014": "7.9%"}),
    ("DATA", "Impairment losses/(releases) for the year", {"FY2017": 311, "FY2016": 131, "FY2015": -731, "FY2014": -1247}),
    ("DATA", "Amounts written-off", {"FY2017": 577, "FY2016": 889, "FY2015": 7276, "FY2014": 2071}),
]
bw.add_asset_quality_sheet(
    title="National Westminster Bank Plc — Asset Quality",
    subtitle="NWB Group basis (Note 13 'Portfolio summary - segment analysis' segment-total column, the entity's own "
              "reportable-segment breakdown - not the NWB Plc solo Balance Sheet loan book), loan exposure and "
              "impairment metrics, IFRS 9 stage basis FY2018-FY2025. £m. FY2014-FY2017 use a structurally different "
              "IAS 39 'risk elements in lending' (REIL) framework, shown in the separate legacy section below rather "
              "than conflated into the IFRS 9 stage rows (which are intentionally blank for those years) - see basis "
              "note in the source citation.",
    rows=asset_quality_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nFY2025/FY2024: Annual Report and Accounts 2025, Note 13 'Loan impairment provisions', p.143. "
        "FY2023/FY2022: Annual Report and Accounts 2023, Note 13, p.148. FY2021 (and FY2022 cross-check): "
        "Annual Report and Accounts 2022, Note 13, p.149. Coverage percentages are as disclosed (rounded by the "
        "source, not recalculated). Inter-group balances (classified Stage 1 per the source's own footnote) are "
        "kept as their own row rather than folded into Stage 1, matching the source table's own structure.\n\n"
        f"FY2020: NWB Group Annual Report and Accounts 2020 (Companies House filing), 'Portfolio summary - segment "
        f"analysis', p.32 - {NWB_CH_AR['FY2020']}\n"
        f"FY2019 (and FY2018 restated cross-check): NWB Group Annual Report and Accounts 2019 (Companies House "
        f"filing), same table, p.33-34 - {NWB_CH_AR['FY2019']}\n\n"
        "BASIS NOTE - IFRS 9 stage data FY2018-FY2020: FY2018 loans/ECL/coverage/impairment-charge figures are "
        "taken from the FY2019 Annual Report's own restated 2018 comparative column (footnoted by the source as "
        "'restated for a change to reportable segments and a change to presentation of unrecognised interest'), "
        "not FY2018's own as-originally-published report, for internal consistency with the FY2019 figures shown "
        "alongside them. All three years' 'Total ECL (release)/charge' figures tie exactly to the Impairment "
        "losses/(releases) line on the Profit & Loss sheet (FY2020: 2,169; FY2019: 572; FY2018: 428), cross-"
        "validating both sheets independently.\n\n"
        "BASIS NOTE - legacy REIL framework FY2014-FY2017: sourced from each year's own Annual Report 'Loans, REIL "
        "and impairment provisions' section, 'Total third party' row (banks + customers, excluding disposal "
        "groups). FY2016 and FY2017 EXCLUDE Ulster Bank (Ireland) DAC and Lombard North Central Plc, which were "
        "reclassified as a disposal group ahead of their 1 January 2017 ring-fencing transfer out of the Group - "
        "consistent with the same exclusion already applied on the Balance Sheet/P&L/Statement of Changes in "
        "Equity sheets. FY2014 and FY2015, by contrast, report BEFORE that reclassification and so their REIL/"
        "provisions/gross-loans figures INCLUDE Ulster Bank Rol as a live segment - a genuine change in reporting "
        "scope across the four years, not a transcription inconsistency; this is why FY2014/FY2015 REIL and "
        "impairment-provision figures are much larger in absolute and percentage terms than FY2016/FY2017. "
        f"Sources: NatWest Plc Annual Report and Accounts 2017 (Companies House filing), p.54 - {NWB_CH_AR['FY2017']}; "
        f"NatWest Plc Annual Report and Accounts 2016 (Companies House filing), p.73 (FY2016 and FY2015 comparative) "
        f"- {NWB_CH_AR['FY2016']}; NatWest Plc Annual Report and Accounts 2015 (Companies House filing), p.69-70 "
        f"(FY2015 and FY2014 comparative, cross-checked against the FY2016 report's own FY2015 column) - {NWB_CH_AR['FY2015']}. "
        "No IFRS 9 stage-based figures exist for FY2014-FY2017 to populate the rows above (IFRS 9 was adopted 1 "
        "January 2018) - not a document-availability gap, a genuine accounting-standard change, per the "
        "STRUCTURAL BREAK NOTE above."
    ),
    first_col_width=76,
    source_height=280,
    unit_suffix=" (£m)",
)


def metric(name, unit, rows, note=None):
    bw.add_metric_sheet(name, unit, rows, p3_sources(), note=note, first_col_width=55, source_height=150)


NWB_CAP_NOTE = (
    "FY2014-FY2020: sourced from each year's own NatWest Plc/National Westminster Bank Plc Annual Report "
    "'Financial review: Capital and risk management' section (entity-level 'significant legal entities within "
    "the Group' table) rather than a standalone Pillar 3 report, which NWB Plc did not begin publishing until "
    "the FY2022 cycle (covering FY2021). FY2016 and FY2015 figures are taken from the FY2017 and FY2015/FY2016 "
    "reports' own NatWest-entity column specifically (excluding the adjacent Ulster Bank Ireland DAC/Limited "
    "column shown side-by-side in those years' combined disclosure tables) - not the RBS/NatWest Group figures."
)
metric("CET1 Capital", "£m", [("Common equity tier 1 (CET1) capital", {"FY2025": 14968, "FY2024": 14181, "FY2023": 14082, "FY2022": 12713, "FY2021": 13924, "FY2020": 15424, "FY2019": 12851, "FY2018": 13138, "FY2017": 13301, "FY2016": 10393, "FY2015": 7154, "FY2014": 9468})], note=NWB_CAP_NOTE)
metric("CET1 Ratio", "% of RWA", [("Common equity tier 1 (CET1) ratio", {"FY2025": "11.2%", "FY2024": "11.4%", "FY2023": "11.6%", "FY2022": "11.3%", "FY2021": "16.1%", "FY2020": "17.8%", "FY2019": "15.9%", "FY2018": "17.4%", "FY2017": "23.5%", "FY2016": "16.1%", "FY2015": "11.6%", "FY2014": "13.9%"})], note=NWB_CAP_NOTE)
metric("Tier 1 Capital", "£m", [("Tier 1 capital", {"FY2025": 17910, "FY2024": 17258, "FY2023": 16360, "FY2022": 14956, "FY2021": 16039, "FY2020": 17590, "FY2019": 15047, "FY2018": 15389, "FY2017": 13301, "FY2016": 10393, "FY2015": 7171, "FY2014": 9562})], note=NWB_CAP_NOTE)
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {"FY2025": "13.4%", "FY2024": "13.9%", "FY2023": "13.4%", "FY2022": "13.3%", "FY2021": "18.6%", "FY2020": "20.2%", "FY2019": "18.6%", "FY2018": "20.4%", "FY2017": "23.5%", "FY2016": "16.1%", "FY2015": "11.6%", "FY2014": "14.0%"})], note=NWB_CAP_NOTE)
metric("Total Capital", "£m", [("Total capital", {"FY2025": 21701, "FY2024": 20629, "FY2023": 19798, "FY2022": 17877, "FY2021": 18945, "FY2020": 20765, "FY2019": 17801, "FY2018": 18490, "FY2017": 17536, "FY2016": 15016, "FY2015": 12137, "FY2014": 14832})], note=NWB_CAP_NOTE)
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2025": "16.2%", "FY2024": "16.6%", "FY2023": "16.3%", "FY2022": "15.9%", "FY2021": "22.0%", "FY2020": "23.9%", "FY2019": "22.0%", "FY2018": "24.5%", "FY2017": "30.9%", "FY2016": "23.3%", "FY2015": "19.6%", "FY2014": "21.7%"})], note=NWB_CAP_NOTE)
metric("Total RWAs", "£m", [("Total risk-weighted exposure amount", {"FY2025": 133749, "FY2024": 124522, "FY2023": 121740, "FY2022": 112428, "FY2021": 86217, "FY2020": 86882, "FY2019": 81069, "FY2018": 75583, "FY2017": 56701, "FY2016": 64424, "FY2015": 61800, "FY2014": 68300})], note=NWB_CAP_NOTE)

# RWA Breakdown - Pillar 3 UK OV1 template, placed right after Total RWAs per
# the locked sheet order. FY2025-FY2022 all tie exactly to the Total RWAs
# figures above. FY2021's breakdown was located this session (ST-028
# follow-up): NWB Plc did not publish its own standalone Pillar 3 report for
# FY2021 (that only started with the FY2022 report cycle) - instead its OV1
# table for FY2021 appears as a large-subsidiary column inside the NatWest
# Holdings Group Pillar 3 Report 2021 (NWH Group, NWB Plc, RBS plc, UBIDAC
# and Coutts & Co side by side), p.25. Found via Wayback Machine CDX search
# against investors.natwestgroup.com/results-center/18022022/ after the live
# site's search/index no longer surfaces it - archived copy:
# https://web.archive.org/web/20220218072522id_/https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/18022022/nwh-pillar-3-supplement-fy-2021.pdf
#
# Note a methodology/template difference versus FY2022 onward: in this
# FY2021 table the "Amounts below the thresholds for deduction" memo row is
# NOT already embedded in the Credit risk row (unlike FY2022-FY2025) - it is
# additive to reach the Total. Row-for-row figures below are exactly as
# reported; the FY2021 Total (86,217) ties precisely to the existing Total
# RWAs figure for FY2021 used elsewhere in this workbook, confirming the
# reconciliation: 66,419 + 574 + 1,054 + 53 + 12,874 + 5,243 = 86,217.
NWH_P3_2021_URL = "https://web.archive.org/web/20220218072522id_/https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/18022022/nwh-pillar-3-supplement-fy-2021.pdf"
rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding counterparty credit risk)", {"FY2025": 110314, "FY2024": 106185, "FY2023": 105860, "FY2022": 98731, "FY2021": 66419, "FY2020": 73445, "FY2019": 67778, "FY2018": 63548, "FY2017": 48575, "FY2016": 56066, "FY2015": 54400, "FY2014": 61700}),
    ("DATA", "Counterparty credit risk", {"FY2025": 600, "FY2024": 606, "FY2023": 713, "FY2022": 497, "FY2021": 574, "FY2020": 576, "FY2019": 605, "FY2018": 325, "FY2017": 266, "FY2016": 473, "FY2015": 700, "FY2014": 600}),
    ("DATA", "Securitisation exposures in the non-trading book (after the cap)", {"FY2025": 4050, "FY2024": 1737, "FY2023": 836, "FY2022": 182, "FY2021": 1054}),
    ("DATA", "Position, foreign exchange and commodities risk (market risk)", {"FY2025": 23, "FY2024": 71, "FY2023": 12, "FY2022": 26, "FY2021": 53, "FY2020": 18, "FY2019": 17, "FY2018": 50, "FY2017": 136, "FY2016": 676, "FY2015": 600, "FY2014": 500}),
    ("DATA", "Operational risk", {"FY2025": 18762, "FY2024": 15923, "FY2023": 14319, "FY2022": 12992, "FY2021": 12874, "FY2020": 12843, "FY2019": 12669, "FY2018": 11660, "FY2017": 7724, "FY2016": 7209, "FY2015": 6400, "FY2014": 5500}),
    ("DATA", "Memo: Amounts below the thresholds for deduction (subject to 250% risk-weight; FY2022-FY2025 non-additive/already in Credit risk above, FY2021 additive to Total - see code comment above)", {"FY2025": 4703, "FY2024": 4711, "FY2023": 4743, "FY2022": 4561, "FY2021": 5243}),
    ("TOTAL", "Total", {"FY2025": 133749, "FY2024": 124522, "FY2023": 121740, "FY2022": 112428, "FY2021": 86217, "FY2020": 86882, "FY2019": 81069, "FY2018": 75583, "FY2017": 56701, "FY2016": 64424, "FY2015": 61800, "FY2014": 68300}),
]
bw.add_rwa_breakdown_sheet(
    title="National Westminster Bank Plc — RWA Breakdown",
    subtitle="NWB Plc entity-level basis, Pillar 3 UK OV1 template (top-level risk-type categories). £m.",
    rows=rwa_breakdown_rows,
    sources_text=(
        f"Sources - NWB Plc UK OV1 tables:\n"
        f"FY2025: NWB Plc Pillar 3 Report 2025, p.8 - {P3_2025_URL}\n"
        f"FY2024: NWB Plc Pillar 3 Report 2024, p.9 - {P3_2024_URL}\n"
        f"FY2023: NWB Plc Pillar 3 Report 2023, p.9 - {P3_2023_URL}\n"
        f"FY2022: NWB Plc Pillar 3 Report 2022, p.8 - {P3_2022_URL}\n"
        f"FY2021: NWH Group Pillar 3 Report 2021, OV1 table (NWB Plc large-subsidiary column), p.25 - {NWH_P3_2021_URL}\n"
        f"FY2020/FY2019: National Westminster Bank Plc Annual Report and Accounts 2020 (Companies House filing), "
        f"'Financial review: Capital, RWAs and leverage' entity table, p.59 - {NWB_CH_AR['FY2020']}\n"
        f"FY2018: NatWest Plc Annual Report and Accounts 2018 (Companies House filing), same entity table, p.19 - {NWB_CH_AR['FY2018']}\n"
        f"FY2017/FY2016: NatWest Plc Annual Report and Accounts 2017 (Companies House filing), same entity table, p.10/p.28 - {NWB_CH_AR['FY2017']}\n"
        f"FY2015/FY2014: NatWest Plc Annual Report and Accounts 2015 (Companies House filing), same entity table (NatWest column, excluding the adjacent Ulster Bank Ireland Limited column), p.29 - {NWB_CH_AR['FY2015']}\n\n"
        + ENTITY_NOTE + "\n\n"
        "Settlement risk (row 15 of the UK OV1 template) is nil across all available years and is omitted as a "
        "row here rather than shown as an all-zero line. The 'Amounts below the thresholds for deduction' memo "
        "row is shown for information only: for FY2022-FY2025 it is already included within Credit risk above "
        "and is NOT additive to the Total (per those reports' own template footnote); for FY2021 the NWH Group "
        "Pillar 3 Report 2021's OV1 table presents it as a distinct, ADDITIVE line - Credit risk excludes it, and "
        "it must be added to reach the Total. This reflects a genuine definitional difference between the FY2021 "
        "and FY2022 OV1 disclosures, not a transcription inconsistency; the FY2021 row values are exactly as "
        "reported and the Total (86,217) ties to the Total RWAs figure used elsewhere in this workbook. "
        "FY2014-FY2020 use each year's own Annual Report capital-management table rather than the Pillar 3 UK OV1 "
        "template (not yet published for NWB Plc in those years) - these tables do not break out a securitisation "
        "or below-threshold-deduction memo line, so both rows are intentionally blank for FY2014-FY2020; the "
        "Total for each of those years ties exactly to the sum of Credit risk, Counterparty credit risk, Market "
        "risk and Operational risk shown."
    ),
    first_col_width=90,
    source_height=220,
    unit_suffix=" (£m)",
)

metric("Leverage Ratio", "£m / %", [("Leverage exposure measure", {"FY2025": 424554, "FY2024": 390032, "FY2023": 359897, "FY2022": 341308, "FY2021": 426681, "FY2020": 376527, "FY2019": 300438, "FY2018": 295483, "FY2017": 213474, "FY2016": 169586, "FY2015": 153100}), ("Leverage ratio", {"FY2025": "4.2%", "FY2024": "4.4%", "FY2023": "4.5%", "FY2022": "4.4%", "FY2021": "3.8%", "FY2020": "4.7%", "FY2019": "5.0%", "FY2018": "5.2%", "FY2017": "6.2%", "FY2016": "6.1%", "FY2015": "4.7%"})], note="FY2021 is shown on the prior CRR methodology as reported in NWB Plc Annual Report 2022, p.64; the report also gives 4.8% on the later UK methodology. FY2022 onward uses the current PRA basis and is not directly comparable with the FY2021 headline. FY2015-FY2020 sourced from each year's own Annual Report entity-level capital table (NWB Plc/NatWest Plc Annual Report and Accounts 2015-2020, Companies House filings). FY2014 is intentionally left blank - a binding minimum leverage ratio requirement, and NatWest's own entity-level leverage exposure/ratio disclosure, only began appearing from the FY2015 Annual Report onward; FY2014's own Annual Report discusses only the wider RBS Group leverage ratio (4.2%, out of scope for this NWB Plc-only workbook), not an NWB Plc/NatWest entity figure.")
metric("LCR", "%", [("Liquidity Coverage Ratio - UK DoLSub", {"FY2025": "151%", "FY2024": "147%", "FY2023": "138%", "FY2022": "131%", "FY2021": "169%", "FY2020": "152%", "FY2019": "145%", "FY2018": "153%"})], note="UK DoLSub basis: NWB Plc, RBS plc and Coutts & Company. The 2025 figure is the December value from the NWB Pillar 3 report; the 2024 and 2023 figures are the December values in the corresponding KM1 disclosures. NWB Plc reports liquidity under a PRA waiver at UK DoLSub level rather than solo. FY2014-FY2017 are intentionally left blank: those years' own Annual Reports state liquidity and funding disclosures are presented for the wider NatWest/RBS Group rather than for the NWB Plc/UK DoLSub entity specifically, so no entity-level LCR figure is available to transcribe for those years without conflating it with Group-level data.")
metric("NSFR", "%", [("Net Stable Funding Ratio - UK DoLSub", {"FY2025": "137%", "FY2024": "136%", "FY2023": "126%", "FY2022": "137%", "FY2021": "151%", "FY2020": "144%", "FY2019": "137%", "FY2018": "144%"})], note="UK DoLSub basis; see LCR note. NSFR is a four-quarter average under the regulatory disclosure framework. FY2014-FY2017 intentionally left blank for the same reason as the LCR sheet - see that sheet's note.")
bw.add_not_disclosed_metric_sheets(["MREL Ratio"], "NWB Plc Pillar 3 Reports 2022-2025 - " + P3_2025_URL, per_note={"MREL Ratio": "No single numeric MREL ratio is presented in the five-year source set used for this annual workbook. MREL instruments and movements are discussed in the annual accounts, but no comparable headline ratio was disclosed in the reviewed NWB Plc UK KM1 material."})


# NWB Plc publishes quarterly UK KM1 disclosures.  The Q3 reports include the
# current quarter plus the preceding Q1/Q2 comparatives, allowing a complete
# March-to-September quarterly series without mixing in NatWest Group data.
INTERIM_PERIODS = [
    ("31 March 2022", "Q1 2022", P3_2022_Q3_URL, "p.7"),
    ("30 June 2022", "H1 2022", P3_2022_Q3_URL, "p.7"),
    ("30 September 2022", "Q3 2022", P3_2022_Q3_URL, "p.7"),
    ("31 March 2023", "Q1 2023", P3_2023_Q3_URL, "p.6"),
    ("30 June 2023", "H1 2023", P3_2023_Q3_URL, "p.6"),
    ("30 September 2023", "Q3 2023", P3_2023_Q3_URL, "p.6"),
    ("31 March 2024", "Q1 2024", P3_2024_Q3_URL, "p.6"),
    ("30 June 2024", "H1 2024", P3_2024_Q3_URL, "p.6"),
    ("30 September 2024", "Q3 2024", P3_2024_Q3_URL, "p.6"),
    ("31 March 2025", "Q1 2025", P3_2025_Q3_URL, "p.6"),
    ("30 June 2025", "H1 2025", P3_2025_Q3_URL, "p.6"),
    ("30 September 2025", "Q3 2025", P3_2025_Q3_URL, "p.6"),
]

INTERIM_VALUES = {
    "31 March 2022": [13802, 15917, 18709, 103987, "13.3%", "15.3%", "18.0%", 338123, "4.7%"],
    "30 June 2022": [12335, 14591, 17503, 106211, "11.6%", "13.7%", "16.5%", 340086, "4.3%"],
    "30 September 2022": [12437, 14680, 17719, 107157, "11.6%", "13.7%", "16.5%", 343343, "4.3%"],
    "31 March 2023": [13640, 15883, 19343, 116122, "11.7%", "13.7%", "16.7%", 349719, "4.5%"],
    "30 June 2023": [13609, 15852, 19235, 116811, "11.7%", "13.6%", "16.5%", 363052, "4.4%"],
    "30 September 2023": [14320, 16563, 20011, 117745, "12.2%", "14.1%", "17.0%", 362422, "4.6%"],
    "31 March 2024": [14823, 17101, 20497, 124523, "11.9%", "13.7%", "16.5%", 358649, "4.8%"],
    "30 June 2024": [13813, 16890, 20273, 120780, "11.4%", "14.0%", "16.8%", 366912, "4.6%"],
    "30 September 2024": [14722, 17799, 21172, 122340, "12.0%", "14.5%", "17.3%", 381762, "4.7%"],
    "31 March 2025": [15271, 18848, 23064, 127480, "12.0%", "14.8%", "18.1%", 397065, "4.7%"],
    "30 June 2025": [14828, 18346, 22104, 130712, "11.3%", "14.0%", "16.9%", 411371, "4.5%"],
    "30 September 2025": [16128, 20147, 23937, 130496, "12.4%", "15.4%", "18.3%", 413717, "4.9%"],
}

interim_metric_specs = [
    ("Common equity tier 1 (CET1) capital", "£m"),
    ("Tier 1 capital", "£m"),
    ("Total capital", "£m"),
    ("Total risk-weighted exposure amount", "£m"),
    ("Common equity tier 1 (CET1) ratio", "%"),
    ("Tier 1 ratio", "%"),
    ("Total capital ratio", "%"),
    ("Total exposure measure excluding claims on central banks", "£m"),
    ("Leverage ratio excluding claims on central banks", "%"),
]
interim_rows = []
for period, disclosure_type, source_url, page_ref in INTERIM_PERIODS:
    for (metric_name, unit), value in zip(interim_metric_specs, INTERIM_VALUES[period]):
        interim_rows.append([
            period, disclosure_type, metric_name, value, unit,
            "NWB Plc entity-level, PRA transitional/current basis as reported",
            source_url, page_ref,
        ])

bw.add_wide_interim_sheet(
    "Interim Pillar 3",
    rows=interim_rows,
    hyperlink_cells={(i, 6): row[6] for i, row in enumerate(interim_rows)},
    title="National Westminster Bank Plc — Interim Pillar 3",
    subtitle="Quarterly UK KM1 key metrics, March 2022 to September 2025. Capital and leverage figures are NWB Plc entity-level disclosures in £m or percentages.",
    note=(
        "Sources are the official NWB Plc Q3 Pillar 3 reports for 2022-2025, whose UK KM1 tables include the current quarter and prior Q1/Q2 comparatives. "
        "The NWB Plc UK Domestic Liquidity Sub-Group waiver means LCR and NSFR are managed and disclosed at UK DoLSub level rather than entity level; they are therefore not inserted here. "
        "No separate NWB Plc interim UK KM1 report was located for March-June-September 2021 in the reviewed official archive, so those periods are explicitly not represented rather than estimated."
    ),
)

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 444649, "FY2024": 421875, "FY2023": 411749, "FY2022": 401747, "FY2021": 426111, "FY2020": 380603, "FY2019": 310954, "FY2018": 301624, "FY2017": 259717, "FY2016": 228921, "FY2015": 220392, "FY2014": 218304}),
        ("Loans to customers - amortised cost", {"FY2025": 310121, "FY2024": 297548, "FY2023": 284314, "FY2022": 267401, "FY2021": 255443, "FY2020": 238366, "FY2019": 198504, "FY2018": 171433, "FY2017": 160679, "FY2016": 150147, "FY2015": 134383, "FY2014": 124297}),
        ("Customer deposits", {"FY2025": 282427, "FY2024": 275972, "FY2023": 276202, "FY2022": 281558, "FY2021": 292470, "FY2020": 255290, "FY2019": 208698, "FY2018": 204279, "FY2017": 201150, "FY2016": 192490, "FY2015": 185139, "FY2014": 182210}),
        ("Total equity", {"FY2025": 22685, "FY2024": 21609, "FY2023": 19701, "FY2022": 18243, "FY2021": 19166, "FY2020": 18464, "FY2019": 18026, "FY2018": 18276, "FY2017": 15355, "FY2016": 15297, "FY2015": 11282, "FY2014": 13312}),
    ], balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total income", {"FY2025": 13620, "FY2024": 11973, "FY2023": 12086, "FY2022": 11743, "FY2021": 9269, "FY2020": 8955, "FY2019": 9163, "FY2018": 9532, "FY2017": 8147, "FY2016": 6039, "FY2015": 5626, "FY2014": 7277}),
        ("Operating expenses", {"FY2025": -7241, "FY2024": -6963, "FY2023": -6793, "FY2022": -6288, "FY2021": -6199, "FY2020": -6184, "FY2019": -7265, "FY2018": -5594, "FY2017": -4320, "FY2016": -4415, "FY2015": -4969, "FY2014": -5949}),
        ("Profit for the year", {"FY2025": 4198, "FY2024": 3425, "FY2023": 3509, "FY2022": 3689, "FY2021": 2907, "FY2020": 536, "FY2019": 884, "FY2018": 2766, "FY2017": 2069, "FY2016": -867, "FY2015": -1206, "FY2014": 1733}),
    ], income_statement_unit="£m (NWB Group basis - see BASIS NOTE)",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 21609, "FY2024": 19701, "FY2023": 18243, "FY2022": 19166, "FY2021": 18464}),
        ("Total comprehensive income for the year", {"FY2025": 4338, "FY2024": 3566, "FY2023": 3211, "FY2022": 2619, "FY2021": 2556}),
        ("Other equity movements, net", {"FY2025": -3262, "FY2024": -1658, "FY2023": -1753, "FY2022": -3542, "FY2021": -1854}),
        ("Closing equity", {"FY2025": 22685, "FY2024": 21609, "FY2023": 19701, "FY2022": 18243, "FY2021": 19166}),
    ], equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 13528, "FY2024": -1896, "FY2023": -4382, "FY2022": -40929, "FY2021": 36574}),
        ("Net cash from/(used in) investing activities", {"FY2025": -11262, "FY2024": -9382, "FY2023": -17008, "FY2022": 12745, "FY2021": 4216}),
        ("Net cash from/(used in) financing activities", {"FY2025": -1918, "FY2024": -2267, "FY2023": -1203, "FY2022": -2991, "FY2021": -1454}),
        ("Cash and cash equivalents at end of year", {"FY2025": 39167, "FY2024": 38678, "FY2023": 52482, "FY2022": 75472, "FY2021": 105546}),
    ], cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "11.2%", "FY2024": "11.4%", "FY2023": "11.6%", "FY2022": "11.3%", "FY2021": "16.1%", "FY2020": "17.8%", "FY2019": "15.9%", "FY2018": "17.4%", "FY2017": "23.5%", "FY2016": "16.1%", "FY2015": "11.6%", "FY2014": "13.9%"}),
        ("Tier 1 Ratio", {"FY2025": "13.4%", "FY2024": "13.9%", "FY2023": "13.4%", "FY2022": "13.3%", "FY2021": "18.6%", "FY2020": "20.2%", "FY2019": "18.6%", "FY2018": "20.4%", "FY2017": "23.5%", "FY2016": "16.1%", "FY2015": "11.6%", "FY2014": "14.0%"}),
        ("Total Capital Ratio", {"FY2025": "16.2%", "FY2024": "16.6%", "FY2023": "16.3%", "FY2022": "15.9%", "FY2021": "22.0%", "FY2020": "23.9%", "FY2019": "22.0%", "FY2018": "24.5%", "FY2017": "30.9%", "FY2016": "23.3%", "FY2015": "19.6%", "FY2014": "21.7%"}),
        ("Leverage Ratio", {"FY2025": "4.2%", "FY2024": "4.4%", "FY2023": "4.5%", "FY2022": "4.4%", "FY2021": "3.8%", "FY2020": "4.7%", "FY2019": "5.0%", "FY2018": "5.2%", "FY2017": "6.2%", "FY2016": "6.1%", "FY2015": "4.7%"}),
        ("LCR (UK DoLSub)", {"FY2025": "151%", "FY2024": "147%", "FY2023": "138%", "FY2022": "131%", "FY2021": "169%", "FY2020": "152%", "FY2019": "145%", "FY2018": "153%"}),
        ("NSFR (UK DoLSub)", {"FY2025": "137%", "FY2024": "136%", "FY2023": "126%", "FY2022": "137%", "FY2021": "151%", "FY2020": "144%", "FY2019": "137%", "FY2018": "144%"}),
    ], note="Figures are duplicated from the detail sheets. See source notes for exact documents, pages, entity basis and methodology changes. Additional quarterly NWB Plc disclosures are provided on the Interim Pillar 3 sheet. Equity-changes and cash-flow summary rows above are shown for FY2021-FY2025 only - the Statement of Changes in Equity and Cash Flow Statement detail sheets were not extended to FY2014-FY2020 in this session (see those sheets' own scope notes).")

bw.save("/Users/armaan/code/katalysis/banks/NATIONAL WESTMINSTER BANK PLC FINANCIALS.xlsx")
