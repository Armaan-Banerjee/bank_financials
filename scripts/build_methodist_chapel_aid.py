import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016"]

AR_2025 = "https://www.mcafundingforchurches.co.uk/media/4bcl2vk5/mca-ar-2025.pdf"
AR_2024 = "https://www.mcafundingforchurches.co.uk/media/keybconk/annual-report-2024.pdf"
AR_2022 = "https://www.mcafundingforchurches.co.uk/sitefiles/resources/pdf/annualreport2022.pdf"
P3_2023 = "https://www.mcafundingforchurches.co.uk/media/ngqlqg5o/pillar-3-disclosures-2023.pdf"
P3_2022 = "https://www.mcafundingforchurches.co.uk/siteFiles/resources/pdf/Pillar3disclosures2022.pdf"

# HD-027 extension (2026-09-06): statutory accounts for FY2016-FY2020 were re-verified directly
# from Companies House filing history (not just the HD-004 domain/earliest-snapshot signal) -
# each PDF was downloaded, rendered page-by-page and read as images (all five filings are
# scanned, non-OCR documents; pdftotext extracted 0 characters from each).
CH_FY2020 = "https://find-and-update.company-information.service.gov.uk/company/00030546/filing-history/MzMwMDQ2Njg3M2FkaXF6a2N4/document?format=pdf&download=0"
CH_FY2018 = "https://find-and-update.company-information.service.gov.uk/company/00030546/filing-history/MzIzMzkxMzU5MGFkaXF6a2N4/document?format=pdf&download=0"
CH_FY2016 = "https://find-and-update.company-information.service.gov.uk/company/00030546/filing-history/MzE3NTQ2MDUyOWFkaXF6a2N4/document?format=pdf&download=0"
# Pillar 3 disclosures for FY2019/FY2020/FY2021 were located via Wayback Machine snapshots of
# mcafundingforchurches.co.uk (not present live) - these are the earliest Pillar 3 documents
# found anywhere on the domain's crawl history; no FY2016/FY2017/FY2018 Pillar 3 document exists
# in the Wayback CDX index for this domain (a full-domain PDF listing was checked, not just a
# single guessed filename), consistent with Pillar 3 disclosure only starting for this small
# firm from FY2019.
P3_2020_WAYBACK = "https://web.archive.org/web/20210515024743/https://www.mcafundingforchurches.co.uk/sitefiles/resources/pdf/pillar3disclosures2020.pdf"
P3_2019_WAYBACK = "https://web.archive.org/web/20200930032441/http://mcafundingforchurches.co.uk/sitefiles/resources/pdf/pillar3disclosures2019.pdf"

ENTITY = (
    "ENTITY NOTE: Methodist Chapel Aid Limited (Companies House 00030546, FRN 204508, "
    "LEI 213800GD7EDYBP4LH202) matches Banks List 2608.xlsx and Companies House. It is a "
    "UK-incorporated PRA/FCA-authorised bank operating on a standalone company basis. The "
    "2025 reporting period covers nine months ended 30 September 2025 after the accounting "
    "reference date changed from 31 December. The Company states that its Pillar 3 policy is "
    "annual. No defensible entity-level interim Pillar 3 series was located, so this is an "
    "18-sheet annual workbook (Overview, Balance Sheet, Profit & Loss, Statement of Changes in "
    "Equity, Cash Flow Statement, Asset Quality, the 11 Pillar 3 key metric sheets, RWA "
    "Breakdown), extended back to FY2016 - the Company's confirmed floor per HD-004 (Companies "
    "House filing history for this entity, 00030546, goes back further, but FY2016 is the year "
    "confirmed for this batch). FY2024 and FY2025 absolute regulatory capital metrics were "
    "not separately disclosed in the located sources and are left blank rather than inferred "
    "from statutory net assets. Pillar 3 disclosure (CET1/Tier 1/Total Capital, RWAs, leverage "
    "ratio) was not published for this entity before FY2019 - see the Wayback Machine note "
    "above - so CET1/Tier1/TotalCapital/RWA/Leverage sheets are genuinely blank for FY2016-"
    "FY2018 (not a search miss). LCR and NSFR were not disclosed for FY2019-FY2021 either: the "
    "FY2019/FY2020/FY2021 standalone Pillar 3 documents only state a policy of maintaining LCR "
    "at or above 200% and do not disclose an actual measured LCR or NSFR figure (no numeric Key "
    "Metrics table exists in these documents, unlike the FY2022/FY2023 disclosures). MREL was "
    "not disclosed in any year."
)


def cash_sources():
    return (
        "Sources - Methodist Chapel Aid Limited entity-level Statement of Cash Flows, £:\n"
        f"FY2025 (9 months ended 30 September 2025): MCA Annual report and accounts 2025, pp. 38-39 - {AR_2025}\n"
        f"FY2024: MCA Annual report and accounts 2024, pp. 36-39 - {AR_2024}\n"
        f"FY2023: MCA Annual report and accounts 2024 comparative, p. 39 - {AR_2024}\n"
        f"FY2022: MCA Annual report and accounts 2022, p. 38 - {AR_2022}\n"
        f"FY2021: MCA Annual report and accounts 2022 comparative, p. 38 - {AR_2022}\n"
        f"FY2020: Companies House full accounts to 31 December 2020 (filed 13 May 2021), Statement of Cash Flows p. 27 - {CH_FY2020}\n"
        f"FY2019: Companies House full accounts to 31 December 2020 comparative, p. 27 - {CH_FY2020}\n"
        f"FY2018: Companies House full accounts to 31 December 2018 (filed 10 May 2019), Statement of Cash Flows p. 25 - {CH_FY2018}\n"
        f"FY2017: Companies House full accounts to 31 December 2018 comparative, p. 25 - {CH_FY2018}\n"
        f"FY2016: Companies House full accounts to 31 December 2016 (filed 11 May 2017), Statement of Cash Flows p. 23 - {CH_FY2016}\n\n"
        + ENTITY
    )


def p3_sources():
    return (
        "Sources - Methodist Chapel Aid Limited entity-level Pillar 3 / regulatory capital disclosures, £'000 unless stated:\n"
        f"FY2023: Pillar 3 Disclosures for year ended 31 December 2023, Key Metrics table, p. 3 - {P3_2023}\n"
        f"FY2022 and FY2021: Pillar 3 Disclosures for year ended 31 December 2022, Key Metrics table, p. 3 - {P3_2022}\n"
        "FY2024/FY2025: no separate absolute Key Metrics table was located; values left blank.\n"
        f"FY2020: Pillar 3 Disclosures for year ended 31 December 2020, Section 5 Capital Adequacy, p. 7 (Wayback Machine snapshot - live URL 404s) - {P3_2020_WAYBACK}\n"
        f"FY2019: Pillar 3 Disclosures for year ended 31 December 2019, Section 5 Capital Adequacy, p. 7 (Wayback Machine snapshot - live URL 404s) - {P3_2019_WAYBACK}\n"
        "FY2018/FY2017/FY2016: no Pillar 3 document exists anywhere in the Wayback Machine CDX "
        "index for mcafundingforchurches.co.uk before FY2019 (a full-domain PDF listing was "
        "checked); values left blank as genuinely not disclosed, not a search miss.\n\n"
        + ENTITY
    )


P3_2023_WAYBACK = "https://web.archive.org/web/20250407005711/https://www.mcafundingforchurches.co.uk/media/ngqlqg5o/pillar-3-disclosures-2023.pdf"

STATEMENTS_SOURCES = (
    "Sources - Methodist Chapel Aid Limited entity-level Statement of Income and Retained Earnings / "
    "Statement of Financial Position, £:\n"
    f"FY2025 (9 months ended 30 September 2025) and FY2024 comparative: MCA Annual report and accounts 2025, "
    f"Statement of Income and Retained Earnings p.37, Statement of Financial Position p.38 - {AR_2025}\n"
    f"FY2023 comparative: MCA Annual report and accounts 2024, Statement of Income and Retained Earnings p.36, "
    f"Statement of Financial Position p.37 - {AR_2024}\n"
    f"FY2022 comparative: MCA Annual report and accounts 2022, Statement of Income and Retained Earnings p.35, "
    f"Statement of Financial Position p.36 - {AR_2022}\n"
    f"FY2021 comparative: MCA Annual report and accounts 2022, Statement of Income and Retained Earnings p.35, "
    f"Statement of Financial Position p.36 - {AR_2022}\n"
    f"FY2020: Companies House full accounts to 31 December 2020, Statement of Income and Retained Earnings p.25, "
    f"Statement of Financial Position p.26 - {CH_FY2020}\n"
    f"FY2019 comparative: Companies House full accounts to 31 December 2020, same pages - {CH_FY2020}\n"
    f"FY2018: Companies House full accounts to 31 December 2018, Statement of Income and Retained Earnings p.23, "
    f"Statement of Financial Position p.24 - {CH_FY2018}\n"
    f"FY2017 comparative: Companies House full accounts to 31 December 2018, same pages - {CH_FY2018}\n"
    f"FY2016: Companies House full accounts to 31 December 2016, Statement of Income and Retained Earnings p.21, "
    f"Statement of Financial Position p.22 - {CH_FY2016}\n\n"
    "Note: the Company has no standalone Statement of Changes in Equity - equity movements are shown within "
    "the combined Statement of Income and Retained Earnings (surplus/(deficit) for the period less dividends "
    "paid and payable, rolled into Reserves; Called up equity share capital is unchanged across all 10 years). "
    "The 2025 reporting period covers 9 months (accounting reference date changed from 31 December to 30 "
    "September); all other periods are 12 months. FY2016-FY2020 statutory line-item labels differ slightly "
    "from later years' Pillar 3-derived labels in two places: 'Interest receivable - on National Savings and "
    "bank deposits' (FY2016-FY2020 statutory wording) is the same line as 'Interest receivable - on bank and "
    "building society deposits' (FY2021+ wording); and the FY2016-FY2020 Investments note (12) splits "
    "investments only into 'Debt and fixed income securities' vs 'Equity investments' (no further split by "
    "issuer type), unlike the FY2023-FY2025 note's three-way split - see the Balance Sheet sheet's separate "
    "'Investments - debt and fixed income securities (aggregate, pre-2021 disclosure)' row.\n\n"
    + ENTITY
)

ASSET_QUALITY_SOURCES = (
    "Sources - Methodist Chapel Aid Limited entity-level loan book detail, Note 11/13 Debtors (Loans and "
    "advances to customers), £:\n"
    f"FY2025 and FY2024 comparative: MCA Annual report and accounts 2025, Note 11, pp.49-50 - {AR_2025}\n"
    f"FY2023 comparative: MCA Annual report and accounts 2024, Note 11, pp.47-48 - {AR_2024}\n"
    f"FY2022 and FY2021 comparative: MCA Annual report and accounts 2022, Note 13, pp.48-49 - {AR_2022}\n"
    f"FY2020: Companies House full accounts to 31 December 2020, Note 13, p.36 - {CH_FY2020}\n"
    f"FY2019 comparative: Companies House full accounts to 31 December 2020, Note 13, p.36 - {CH_FY2020}\n"
    f"FY2018: Companies House full accounts to 31 December 2018, Note 13, p.34 - {CH_FY2018}\n"
    f"FY2017 comparative: Companies House full accounts to 31 December 2018, Note 13, p.34 - {CH_FY2018}\n"
    f"FY2016: Companies House full accounts to 31 December 2016, Note 13, p.32 - {CH_FY2016}\n\n"
    "Note: the Company applies FRS 102 (not IFRS 9), so no Stage 1/2/3 ECL split is disclosed - credit quality "
    "is shown instead via the Company's own product/security split and a single collective 'Provision for bad "
    "debts' balance. No past-due/impaired-loan analysis beyond the provision balance was located.\n\n"
    + ENTITY
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - Methodist Chapel Aid Limited entity-level Pillar 1 capital requirement / RWA breakdown by "
    "exposure class, £'000:\n"
    f"FY2023: Pillar 3 Disclosures for year ended 31 December 2023, Section 5 Capital Adequacy table, p.7 - "
    f"{P3_2023} (URL 404s as of this session; retrieved via Wayback Machine snapshot - {P3_2023_WAYBACK})\n"
    f"FY2022: Pillar 3 Disclosures for year ended 31 December 2022, Section 5 Capital Adequacy table, p.8 - {P3_2022}\n"
    "FY2021: no category-level breakdown was located - only the Key Metrics table's single Total "
    "risk-weighted exposure amount (26,369) is disclosed for FY2021, in the FY2022 Pillar 3 document's "
    "comparative column; the underlying Section 5 capital-adequacy table there is 'as at 31 December 2022' "
    "only, with no FY2021 equivalent table. Category rows left blank for FY2021; the Total RWAs row is "
    "populated from that comparative figure.\n"
    "FY2024/FY2025: no Pillar 3 Key Metrics table or capital-adequacy breakdown was located for these "
    "periods (consistent with the existing Total RWAs sheet, which is also blank for these years).\n"
    f"FY2020: Pillar 3 Disclosures for year ended 31 December 2020, Section 5 Capital Adequacy table, p.7 "
    f"(Wayback Machine snapshot - live URL 404s) - {P3_2020_WAYBACK}. Operational risk RWA is derived as "
    "capital requirement x 12.5 (i.e. /8%), the same Pillar 1 formula the document itself states, since the "
    "table discloses operational risk only as a capital requirement, not directly as RWA.\n"
    f"FY2019: Pillar 3 Disclosures for year ended 31 December 2019, Section 5 Capital Adequacy table, p.7 "
    f"(Wayback Machine snapshot - live URL 404s) - {P3_2019_WAYBACK}. Operational risk RWA derived the same way.\n"
    "FY2018/FY2017/FY2016: no Pillar 3 document exists anywhere in the Wayback Machine CDX index for "
    "mcafundingforchurches.co.uk before FY2019; category rows left blank as genuinely not disclosed.\n\n"
    + ENTITY
)


bw = BankWorkbook("Methodist Chapel Aid Limited", YEARS, header_color="6B4E71")

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and bank balances", {"FY2025": 9417754, "FY2024": 8355272, "FY2023": 7520873, "FY2022": 10132743, "FY2021": 12459792, "FY2020": 13653122, "FY2019": 10947148, "FY2018": 10984433, "FY2017": 11252440, "FY2016": 12174432}),
    ("DATA", "Loans and advances to customers", {"FY2025": 8262627, "FY2024": 9138711, "FY2023": 10330064, "FY2022": 8485497, "FY2021": 7197340, "FY2020": 7314586, "FY2019": 7888087, "FY2018": 6315264, "FY2017": 5210921, "FY2016": 4295209}),
    ("DATA", "Investments - issued by public body", {"FY2025": 4941874, "FY2024": 4208030, "FY2023": 4824018}),
    ("DATA", "Investments - other loans and advances", {"FY2025": 3843427, "FY2024": 4049871, "FY2023": 4500425}),
    ("DATA", "Investments - debt and fixed income securities (aggregate, pre-2021 disclosure)", {"FY2020": 9047492, "FY2019": 8170744, "FY2018": 7957868, "FY2017": 8122521, "FY2016": 7940441}),
    ("DATA", "Investments - equity investments", {"FY2025": 8230600, "FY2024": 8135418, "FY2023": 7100690, "FY2020": 8606515, "FY2019": 8368796, "FY2018": 7260746, "FY2017": 8090285, "FY2016": 7927810}),
    ("TOTAL", "Total investments", {"FY2025": 17015901, "FY2024": 16393319, "FY2023": 16425133, "FY2022": 16047858, "FY2021": 17733105, "FY2020": 17654007, "FY2019": 16539540, "FY2018": 15218614, "FY2017": 16212806, "FY2016": 15868251}),
    ("DATA", "Intangible fixed assets", {"FY2025": 3957}),
    ("DATA", "Tangible fixed assets", {"FY2025": 287367, "FY2024": 300959, "FY2023": 305490, "FY2022": 37749, "FY2021": 31127, "FY2020": 7852, "FY2019": 22084, "FY2018": 32058, "FY2017": 50429, "FY2016": 66102}),
    ("DATA", "Investments held for short term purposes", {"FY2025": 748688, "FY2024": 1831800, "FY2023": 1576261, "FY2022": 2380720, "FY2021": 2661841, "FY2020": 236135, "FY2019": 862056, "FY2018": 892171, "FY2017": 750539, "FY2016": 476027}),
    ("DATA", "Prepayments, accrued income and other assets", {"FY2025": 219743, "FY2024": 127040, "FY2023": 135703, "FY2022": 109921, "FY2021": 71600, "FY2020": 74764, "FY2019": 110945, "FY2018": 93275, "FY2017": 99700, "FY2016": 92648}),
    ("TOTAL", "Total Assets", {"FY2025": 35956037, "FY2024": 36147101, "FY2023": 36293524, "FY2022": 37194488, "FY2021": 40154805, "FY2020": 38940466, "FY2019": 36369860, "FY2018": 33535815, "FY2017": 33576835, "FY2016": 32972669}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer accounts", {"FY2025": 21227564, "FY2024": 22043458, "FY2023": 22687021, "FY2022": 24113288, "FY2021": 25374073, "FY2020": 25034413, "FY2019": 23169408, "FY2018": 21897604, "FY2017": 21344785, "FY2016": 21572515}),
    ("DATA", "Other liabilities", {"FY2025": 370311, "FY2024": 167472, "FY2023": 131713, "FY2022": 83947, "FY2021": 64139, "FY2020": 167071, "FY2019": 75034, "FY2018": 64494, "FY2017": 85883, "FY2016": 88824}),
    ("TOTAL", "Total Liabilities", {"FY2025": 21597875, "FY2024": 22210930, "FY2023": 22818734, "FY2022": 24197235, "FY2021": 25438212, "FY2020": 25201484, "FY2019": 23244442, "FY2018": 21962098, "FY2017": 21430668, "FY2016": 21661339}),
    ("SECTION", "Provisions", {}),
    ("DATA", "Deferred tax", {"FY2025": 241076, "FY2024": 188844, "FY2023": 121158, "FY2022": 45234, "FY2021": 540391, "FY2020": 295993, "FY2019": 257972, "FY2018": 4956, "FY2017": 147721, "FY2016": 239818}),
    ("TOTAL", "Net Assets", {"FY2025": 14117086, "FY2024": 13747327, "FY2023": 13353632, "FY2022": 12952019, "FY2021": 14176202, "FY2020": 13442989, "FY2019": 12867446, "FY2018": 11568761, "FY2017": 11998446, "FY2016": 11071512}),
    ("SECTION", "Shareholders' Funds", {}),
    ("DATA", "Called up equity share capital", {"FY2025": 1197, "FY2024": 1197, "FY2023": 1197, "FY2022": 1197, "FY2021": 1197, "FY2020": 1197, "FY2019": 1197, "FY2018": 1197, "FY2017": 1197, "FY2016": 1197}),
    ("DATA", "Reserves", {"FY2025": 14115889, "FY2024": 13746130, "FY2023": 13352435, "FY2022": 12950822, "FY2021": 14175005, "FY2020": 13441792, "FY2019": 12866249, "FY2018": 11567564, "FY2017": 11997249, "FY2016": 11070315}),
    ("TOTAL", "Total equity", {"FY2025": 14117086, "FY2024": 13747327, "FY2023": 13353632, "FY2022": 12952019, "FY2021": 14176202, "FY2020": 13442989, "FY2019": 12867446, "FY2018": 11568761, "FY2017": 11998446, "FY2016": 11071512}),
]
bw.add_balance_sheet_sheet(
    "Methodist Chapel Aid Limited — Statement of Financial Position",
    "Entity-level basis, £. FY2025 as at 30 September 2025 (9-month period end); all other years as at 31 December.",
    balance_sheet_rows,
    STATEMENTS_SOURCES,
    first_col_width=58,
    source_height=230,
    unit_suffix=" (£)",
)

income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable - on loans", {"FY2025": 364536, "FY2024": 542736, "FY2023": 485539, "FY2022": 241994, "FY2021": 226796, "FY2020": 238045, "FY2019": 216819, "FY2018": 188593, "FY2017": 150120, "FY2016": 140331}),
    ("DATA", "Interest receivable - on debt securities", {"FY2025": 254891, "FY2024": 351721, "FY2023": 346423, "FY2022": 292232, "FY2021": 297207, "FY2020": 310571, "FY2019": 321383, "FY2018": 322478, "FY2017": 326582, "FY2016": 329862}),
    ("DATA", "Interest receivable - on bank and building society deposits", {"FY2025": 301668, "FY2024": 412981, "FY2023": 347139, "FY2022": 114132, "FY2021": 11584, "FY2020": 42272, "FY2019": 71244, "FY2018": 57941, "FY2017": 42354, "FY2016": 89504}),
    ("DATA", "Interest payable to depositors", {"FY2025": -513856, "FY2024": -702772, "FY2023": -570746, "FY2022": -167638, "FY2021": -158940, "FY2020": -218608, "FY2019": -229881, "FY2018": -206421, "FY2017": -182991, "FY2016": -263234}),
    ("DATA", "Interest payable - amortisation of debt securities", {"FY2025": -12204, "FY2024": -55620, "FY2023": -101184, "FY2022": -87073, "FY2021": -86814, "FY2020": -96429, "FY2019": -69882, "FY2018": -61467, "FY2017": -54842, "FY2016": -52449}),
    ("DATA", "Dividend income from equity shares", {"FY2025": 149236, "FY2024": 186640, "FY2023": 172192, "FY2022": 226757, "FY2021": 220001, "FY2020": 190548, "FY2019": 259323, "FY2018": 261860, "FY2017": 271126, "FY2016": 287571}),
    ("DATA", "Investment gains/(losses) on debt securities", {"FY2024": -371214, "FY2023": -27579, "FY2022": -12251, "FY2021": -30549, "FY2020": 328406, "FY2019": 4366, "FY2018": 37062, "FY2017": 4681, "FY2016": 24643}),
    ("DATA", "Fees and commissions payable to Investment Manager", {"FY2025": -32837, "FY2024": -3575, "FY2023": -19845, "FY2022": -37299, "FY2021": -29476, "FY2020": -43050, "FY2019": -43816, "FY2018": -51541, "FY2017": -52371, "FY2016": -66220}),
    ("DATA", "Other operating income", {"FY2025": 4302, "FY2024": 4900, "FY2023": 6543, "FY2022": 11797, "FY2021": 177145, "FY2020": 2924, "FY2019": 5692, "FY2018": 3666, "FY2017": 7218, "FY2016": 3925}),
    # Derived sum (not a printed AR subtotal) of every DATA row in the Income
    # section above, so the cross-bank insights pipeline (in041_spend_metrics.py)
    # has a TOTAL-tagged revenue row to divide against. FY2025 excludes
    # "Investment gains/(losses) on debt securities" since the AR doesn't
    # disclose that line for the 9-month FY2025 period.
    ("TOTAL", "Total income", {"FY2025": 515736, "FY2024": 365797, "FY2023": 638482, "FY2022": 582651, "FY2021": 626954, "FY2020": 754679, "FY2019": 535248, "FY2018": 552171, "FY2017": 511877, "FY2016": 493933}),
    ("DATA", "Administrative expenses - staff costs", {"FY2025": -241735, "FY2024": -310501, "FY2023": -281131, "FY2022": -236031, "FY2021": -202930, "FY2020": -205751, "FY2019": -198443, "FY2018": -191928, "FY2017": -180526, "FY2016": -179379}),
    ("DATA", "Administrative expenses - other", {"FY2025": -230594, "FY2024": -246970, "FY2023": -260190, "FY2022": -212268, "FY2021": -154761, "FY2020": -150767, "FY2019": -162438, "FY2018": -159701, "FY2017": -162332, "FY2016": -162246}),
    # Derived sum (not a printed AR subtotal) of the two administrative expense
    # DATA rows above, so the cross-bank insights pipeline has a TOTAL-tagged
    # opex row to divide against.
    ("TOTAL", "Total administrative expenses", {"FY2025": -472329, "FY2024": -557471, "FY2023": -541321, "FY2022": -448299, "FY2021": -357691, "FY2020": -356518, "FY2019": -360881, "FY2018": -351629, "FY2017": -342858, "FY2016": -341625}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -9635, "FY2024": -13288, "FY2023": -9937, "FY2022": -7168, "FY2021": -3633, "FY2020": -14732, "FY2019": -17132, "FY2018": -18651, "FY2017": -18377, "FY2016": -14038}),
    ("TOTAL", "Operating surplus/(deficit)", {"FY2025": 33772, "FY2024": -204962, "FY2023": 87224, "FY2022": 127184, "FY2021": 265630, "FY2020": 383429, "FY2019": 157235, "FY2018": 181891, "FY2017": 150642, "FY2016": 138270}),
    ("DATA", "Fair value adjustment to investments", {"FY2025": 385195, "FY2024": 694496, "FY2023": 391546, "FY2022": -1845411, "FY2021": 711942, "FY2020": 318792, "FY2019": 1402028, "FY2018": -754426, "FY2017": 729845, "FY2016": 666013}),
    ("TOTAL", "Surplus/(deficit) on ordinary activities before taxation", {"FY2025": 418967, "FY2024": 489534, "FY2023": 478770, "FY2022": -1718227, "FY2021": 977572, "FY2020": 702221, "FY2019": 1559263, "FY2018": -572535, "FY2017": 880487, "FY2016": 804283}),
    ("DATA", "Tax on surplus/(deficit) on ordinary activities", {"FY2025": -47855, "FY2024": -94522, "FY2023": -75924, "FY2022": 495157, "FY2021": -243291, "FY2020": -125620, "FY2019": -259537, "FY2018": 143868, "FY2017": 47426, "FY2016": -46629}),
    ("TOTAL", "Surplus/(deficit) for the period/year and total comprehensive income", {"FY2025": 371112, "FY2024": 395012, "FY2023": 402846, "FY2022": -1223070, "FY2021": 734281, "FY2020": 576601, "FY2019": 1299726, "FY2018": -428667, "FY2017": 927913, "FY2016": 757654}),
]
bw.add_income_statement_sheet(
    "Methodist Chapel Aid Limited — Statement of Income and Retained Earnings",
    "Entity-level basis, £. FY2025 covers the 9 months ended 30 September 2025; all other years are 12-month periods.",
    income_statement_rows,
    STATEMENTS_SOURCES,
    first_col_width=64,
    source_height=230,
    unit_suffix=" (£)",
)

equity_headers = ["Called up share capital", "Reserves", "Total equity"]
equity_rows = [
    ("TOTAL", "Balance at 1 January 2016", (1197, 10313628, 10314825)),
    ("DATA", "Surplus for the year", (None, 757654, 757654)),
    ("DATA", "Dividends paid and payable", (None, -967, -967)),
    ("TOTAL", "Balance at 31 December 2016 / 1 January 2017", (1197, 11070315, 11071512)),
    ("DATA", "Surplus for the year", (None, 927913, 927913)),
    ("DATA", "Dividends paid and payable", (None, -979, -979)),
    ("TOTAL", "Balance at 31 December 2017 / 1 January 2018", (1197, 11997249, 11998446)),
    ("DATA", "Deficit for the year", (None, -428667, -428667)),
    ("DATA", "Dividends paid and payable", (None, -1018, -1018)),
    ("TOTAL", "Balance at 31 December 2018 / 1 January 2019", (1197, 11567564, 11568761)),
    ("DATA", "Surplus for the year", (None, 1299726, 1299726)),
    ("DATA", "Dividends paid and payable", (None, -1041, -1041)),
    ("TOTAL", "Balance at 31 December 2019 / 1 January 2020", (1197, 12866249, 12867446)),
    ("DATA", "Surplus for the year", (None, 576601, 576601)),
    ("DATA", "Dividends paid and payable", (None, -1058, -1058)),
    ("TOTAL", "Balance at 31 December 2020 / 1 January 2021", (1197, 13441792, 13442989)),
    ("DATA", "Surplus for the year", (None, 734281, 734281)),
    ("DATA", "Dividends paid and payable", (None, -1068, -1068)),
    ("TOTAL", "Balance at 31 December 2021 / 1 January 2022", (1197, 14175005, 14176202)),
    ("DATA", "Deficit for the year", (None, -1223070, -1223070)),
    ("DATA", "Dividends paid and payable", (None, -1113, -1113)),
    ("TOTAL", "Balance at 31 December 2022 / 1 January 2023", (1197, 12950822, 12952019)),
    ("DATA", "Surplus for the year", (None, 402846, 402846)),
    ("DATA", "Dividends paid and payable", (None, -1233, -1233)),
    ("TOTAL", "Balance at 31 December 2023 / 1 January 2024", (1197, 13352435, 13353632)),
    ("DATA", "Surplus for the year", (None, 395012, 395012)),
    ("DATA", "Dividends paid and payable", (None, -1317, -1317)),
    ("TOTAL", "Balance at 31 December 2024 / 1 January 2025", (1197, 13746130, 13747327)),
    ("DATA", "Surplus for the period (9 months)", (None, 371112, 371112)),
    ("DATA", "Dividends paid and payable", (None, -1353, -1353)),
    ("TOTAL", "Balance at 30 September 2025", (1197, 14115889, 14117086)),
]
bw.add_equity_changes_sheet(
    "Methodist Chapel Aid Limited — Statement of Changes in Equity",
    "Entity-level basis, £. Reconstructed from the combined Statement of Income and Retained Earnings, chronological, oldest to newest.",
    equity_headers,
    equity_rows,
    STATEMENTS_SOURCES,
    source_height=230,
)

cash_rows = [
    ("SECTION", "Operating activities", {}),
    ("TOTAL", "Net cash generated/(used) from operating activities", {"FY2025": 230314, "FY2024": 429322, "FY2023": -3050504, "FY2022": -2346030, "FY2021": 714322, "FY2020": 2973715, "FY2019": -70421, "FY2018": -303376, "FY2017": -974245, "FY2016": 161846}),
    ("SECTION", "Investing activities", {}),
    ("TOTAL", "Net cash generated/(used) from investing activities", {"FY2025": -249591, "FY2024": 661933, "FY2023": -364592, "FY2022": -261027, "FY2021": 519122, "FY2020": -892604, "FY2019": 4062, "FY2018": 178019, "FY2017": 327744, "FY2016": 171836}),
    ("SECTION", "Financing activities", {}),
    ("TOTAL", "Net cash generated/(used) in financing activities", {"FY2025": -1353, "FY2024": -1317, "FY2023": -1233, "FY2022": -1113, "FY2021": -1068, "FY2020": -1058, "FY2019": -1041, "FY2018": -1018, "FY2017": -979, "FY2016": -967}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": -20630, "FY2024": 1089938, "FY2023": -3416329, "FY2022": -2608170, "FY2021": 1232376, "FY2020": 2080053, "FY2019": -67400, "FY2018": -126375, "FY2017": -647480, "FY2016": 332715}),
    ("DATA", "Cash and cash equivalents at the beginning of year/period", {"FY2025": 10187072, "FY2024": 9097134, "FY2023": 12513463, "FY2022": 15121633, "FY2021": 13889257, "FY2020": 11809204, "FY2019": 11876604, "FY2018": 12002979, "FY2017": 12650459, "FY2016": 12317744}),
    ("TOTAL", "Cash and cash equivalents at the end of year/period", {"FY2025": 10166442, "FY2024": 10187072, "FY2023": 9097134, "FY2022": 12513463, "FY2021": 15121633, "FY2020": 13889257, "FY2019": 11809204, "FY2018": 11876604, "FY2017": 12002979, "FY2016": 12650459}),
]
bw.add_cash_flow_sheet(
    "Methodist Chapel Aid Limited — Cash Flow Statement",
    "Entity-level basis, £",
    cash_rows,
    cash_sources(),
    first_col_width=65,
    source_height=190,
    unit_suffix=" (£)",
)

asset_quality_rows = [
    ("SECTION", "Loan book by product (gross)", {}),
    ("DATA", "Property loans - secured", {"FY2025": 6882826, "FY2024": 7487986, "FY2023": 7265355, "FY2022": 7037375, "FY2021": 5840927, "FY2020": 6141270, "FY2019": 6821441, "FY2018": 5789736, "FY2017": 4159580, "FY2016": 3532033}),
    ("DATA", "Property loans - unsecured", {"FY2025": 1375657, "FY2024": 1644631, "FY2023": 3055122, "FY2022": 1432495, "FY2021": 1346352, "FY2020": 1160251, "FY2019": 1039071, "FY2018": 477458, "FY2017": 972672, "FY2016": 643066}),
    ("TOTAL", "Property loans - total", {"FY2025": 8258483, "FY2024": 9132617, "FY2023": 10320477, "FY2022": 8469870, "FY2021": 7187279, "FY2020": 7301521, "FY2019": 7860512, "FY2018": 6267194, "FY2017": 5132252, "FY2016": 4175099}),
    ("DATA", "Car loans - unsecured", {"FY2025": 4250, "FY2024": 6250, "FY2023": 9833, "FY2022": 16028, "FY2021": 10319, "FY2020": 13400, "FY2019": 28282, "FY2018": 49302, "FY2017": 80686, "FY2016": 123190}),
    ("TOTAL", "Total loans and advances (gross)", {"FY2025": 8262733, "FY2024": 9138867, "FY2023": 10330310, "FY2022": 8485898, "FY2021": 7197598, "FY2020": 7314921, "FY2019": 7888794, "FY2018": 6316496, "FY2017": 5212938, "FY2016": 4298289}),
    ("DATA", "Provision for bad debts", {"FY2025": -106, "FY2024": -156, "FY2023": -246, "FY2022": -401, "FY2021": -258, "FY2020": -335, "FY2019": -707, "FY2018": -1232, "FY2017": -2017, "FY2016": -3080}),
    ("TOTAL", "Total loans and advances (net)", {"FY2025": 8262627, "FY2024": 9138711, "FY2023": 10330064, "FY2022": 8485497, "FY2021": 7197340, "FY2020": 7314586, "FY2019": 7888087, "FY2018": 6315264, "FY2017": 5210921, "FY2016": 4295209}),
    ("SECTION", "Maturity profile of loans and advances (net)", {}),
    ("DATA", "Due within 3 months", {"FY2025": 480809, "FY2024": 350750, "FY2023": 1449455, "FY2022": 1861, "FY2021": 1848, "FY2020": 57672, "FY2019": 488356, "FY2018": 8880, "FY2017": 12201, "FY2016": 9959}),
    ("DATA", "In more than 3 months but not more than 1 year", {"FY2025": 1166309, "FY2024": 1907530, "FY2023": 2103477, "FY2022": 2223451, "FY2021": 364515, "FY2020": 672303, "FY2019": 588968, "FY2018": 1190672, "FY2017": 1211741, "FY2016": 1183851}),
    ("DATA", "In more than 1 year but not more than 5 years", {"FY2025": 3075037, "FY2024": 3184280, "FY2023": 3463531, "FY2022": 3069212, "FY2021": 3182168, "FY2020": 2328530, "FY2019": 1827551, "FY2018": 1796008, "FY2017": 1588387, "FY2016": 1241379}),
    ("DATA", "In more than 5 years", {"FY2025": 3540578, "FY2024": 3696307, "FY2023": 3313847, "FY2022": 3191374, "FY2021": 3649067, "FY2020": 4256416, "FY2019": 4983919, "FY2018": 3320936, "FY2017": 2400609, "FY2016": 1863100}),
]
bw.add_asset_quality_sheet(
    "Methodist Chapel Aid Limited — Asset Quality",
    "Entity-level basis, £. FRS 102 reporting - no IFRS 9 Stage 1/2/3 split disclosed; credit quality shown via product/security split and a single collective provision for bad debts.",
    asset_quality_rows,
    ASSET_QUALITY_SOURCES,
    first_col_width=62,
    source_height=210,
    unit_suffix=" (£)",
)


def metric(name, unit, label, data, note=None):
    bw.add_metric_sheet(name, unit, [(label, data)], p3_sources(), note=note, first_col_width=50, source_height=190)


metric("CET1 Capital", "£'000", "CET1 capital", {"FY2023": 13354, "FY2022": 12952, "FY2021": 13919, "FY2020": 13032, "FY2019": 12307}, "FY2024 and FY2025 absolute regulatory capital was not separately disclosed in the located sources. FY2016-FY2018: no Pillar 3 document was located (genuinely not disclosed, not a search miss - see note above).")
metric("CET1 Ratio", "%", "CET1 ratio", {"FY2023": "52.88%", "FY2022": "53.85%", "FY2021": "52.79%", "FY2020": "51.48%", "FY2019": "58.68%"}, "FY2024 and FY2025 ratio not separately disclosed in the located sources. FY2020/FY2019 ratios are calculated as disclosed CET1 capital divided by this workbook's derived Total RWAs (not stated as a ready-made ratio in the source, which only gives the £ components). FY2016-FY2018 not disclosed.")
metric("Tier 1 Capital", "£'000", "Tier 1 capital", {"FY2023": 13354, "FY2022": 12952, "FY2021": 13919, "FY2020": 13032, "FY2019": 12307}, "All disclosed Tier 1 capital was CET1; FY2024 and FY2025 were not separately disclosed. FY2016-FY2018 not disclosed.")
metric("Tier 1 Ratio", "%", "Tier 1 ratio", {"FY2023": "52.88%", "FY2022": "53.85%", "FY2021": "52.79%", "FY2020": "51.48%", "FY2019": "58.68%"}, "FY2024 and FY2025 ratio not separately disclosed in the located sources. FY2016-FY2018 not disclosed.")
metric("Total Capital", "£'000", "Total capital", {"FY2023": 13354, "FY2022": 12952, "FY2021": 13919, "FY2020": 13032, "FY2019": 12307}, "All disclosed total capital was CET1; FY2024 and FY2025 were not separately disclosed. FY2016-FY2018 not disclosed.")
metric("Total Capital Ratio", "%", "Total capital ratio", {"FY2023": "52.88%", "FY2022": "53.85%", "FY2021": "52.79%", "FY2020": "51.48%", "FY2019": "58.68%"}, "FY2024 and FY2025 ratio not separately disclosed in the located sources. FY2016-FY2018 not disclosed.")
metric("Total RWAs", "£'000", "Total risk-weighted exposure amount", {"FY2023": 25253, "FY2022": 24052, "FY2021": 26369, "FY2020": 25316, "FY2019": 20975}, "FY2024 and FY2025 absolute RWA was not separately disclosed in the located sources. FY2020/FY2019 Total RWAs are the sum of the disclosed credit risk RWA plus an operational risk RWA derived as capital requirement x 12.5 (the document's own Pillar 1 formula) since operational risk is disclosed there only as a capital requirement. FY2016-FY2018 not disclosed.")

rwa_breakdown_rows = [
    ("SECTION", "Credit risk exposure by class (Risk Weighted Exposure)", {}),
    ("DATA", "Credit institutions", {"FY2023": 1825, "FY2022": 2713, "FY2020": 3255, "FY2019": 2835}),
    ("DATA", "UK Treasury Stocks", {"FY2023": 0, "FY2022": 0, "FY2020": 0, "FY2019": 0}),
    ("DATA", "Multilateral Development Banks", {"FY2019": 0}),
    ("DATA", "Sterling Corporate Bonds", {"FY2019": 961}),
    ("DATA", "Collective investment undertakings", {"FY2023": 3271, "FY2022": 3092, "FY2020": 4097, "FY2019": 1607}),
    ("DATA", "Equity investments", {"FY2023": 7101, "FY2022": 7160, "FY2020": 8138, "FY2019": 7678}),
    ("DATA", "Loans and advances to customers (drawn) (aggregate, pre-2021 disclosure)", {"FY2020": 7315, "FY2019": 5916}),
    ("DATA", "Loans and advances to customers (50% of undrawn) (aggregate, pre-2021 disclosure)", {"FY2020": 1440, "FY2019": 857}),
    ("DATA", "Higher Risk Weighted Equities", {"FY2022": 30}),
    ("DATA", "Property loans and advances to customers (drawn)", {"FY2023": 10320, "FY2022": 8470}),
    ("DATA", "Property loans and advances to customers (50% of undrawn)", {"FY2023": 1125, "FY2022": 1195}),
    ("DATA", "Car loans and advances to customers", {"FY2023": 7, "FY2022": 12}),
    ("DATA", "Fixed and other assets", {"FY2023": 436, "FY2022": 145, "FY2020": 83, "FY2019": 133}),
    ("TOTAL", "Total credit risk exposure (RWA)", {"FY2023": 24085, "FY2022": 22817, "FY2020": 24328, "FY2019": 19987}),
    ("DATA", "Operational risk capital requirement (RWA)", {"FY2023": 1168, "FY2022": 1235, "FY2020": 988, "FY2019": 988}),
    ("TOTAL", "Total RWAs (Pillar 1)", {"FY2023": 25253, "FY2022": 24052, "FY2021": 26369, "FY2020": 25316, "FY2019": 20975}),
]
bw.add_rwa_breakdown_sheet(
    "Methodist Chapel Aid Limited — RWA Breakdown",
    "Entity-level basis, £'000, Standardised Approach.",
    rwa_breakdown_rows,
    RWA_BREAKDOWN_SOURCES,
    first_col_width=58,
    source_height=230,
)

metric("Leverage Ratio", "%", "Leverage ratio", {"FY2023": "35.4%", "FY2022": "33.49%", "FY2021": "33.05%", "FY2020": "~30%", "FY2019": "~30%"}, "The Company states that the smaller-bank leverage requirement does not apply; reported ratios are included as disclosed. FY2024 and FY2025 were not separately disclosed. FY2020/FY2019 are transcribed as disclosed - the narrative Pillar 3 documents for these years state only 'approximately 30%', not an exact figure (the FY2021 standalone Pillar 3 document uses the same approximate wording, but a more precise 33.05% is used for FY2021 above, sourced from the newer FY2022 Pillar 3 document's comparative column). FY2016-FY2018 not disclosed.")
metric("LCR", "%", "Average liquidity coverage ratio", {"FY2023": "835%", "FY2022": "833%", "FY2021": "603%"}, "FY2023 is the average based on quarterly end-of-month positions; FY2024 and FY2025 were not separately disclosed. FY2019-FY2021: the standalone Pillar 3 documents for these years state only a policy of maintaining LCR at or above 200% and do not disclose an actual measured ratio; left blank rather than treating the policy floor as an actual value. FY2016-FY2018 not disclosed.")
metric("NSFR", "%", "Average net stable funding ratio", {"FY2023": "182%", "FY2022": "192%", "FY2021": "184%"}, "FY2023 is the average based on quarterly end-of-month positions; FY2024 and FY2025 were not separately disclosed. FY2019/FY2020: no NSFR was disclosed anywhere in the standalone Pillar 3 documents for these years (no Key Metrics table format existed yet). FY2016-FY2018 not disclosed.")
bw.add_not_disclosed_metric_sheets(["MREL Ratio"], p3_sources(), per_note={"MREL Ratio": "No MREL ratio was disclosed in the located Methodist Chapel Aid Pillar 3 documents."})

bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash generated/(used) from operating activities", {"FY2025": 230314, "FY2024": 429322, "FY2023": -3050504, "FY2022": -2346030, "FY2021": 714322, "FY2020": 2973715, "FY2019": -70421, "FY2018": -303376, "FY2017": -974245, "FY2016": 161846}),
        ("Net cash generated/(used) from investing activities", {"FY2025": -249591, "FY2024": 661933, "FY2023": -364592, "FY2022": -261027, "FY2021": 519122, "FY2020": -892604, "FY2019": 4062, "FY2018": 178019, "FY2017": 327744, "FY2016": 171836}),
        ("Net cash generated/(used) in financing activities", {"FY2025": -1353, "FY2024": -1317, "FY2023": -1233, "FY2022": -1113, "FY2021": -1068, "FY2020": -1058, "FY2019": -1041, "FY2018": -1018, "FY2017": -979, "FY2016": -967}),
        ("Cash and cash equivalents at end of year/period", {"FY2025": 10166442, "FY2024": 10187072, "FY2023": 9097134, "FY2022": 12513463, "FY2021": 15121633, "FY2020": 13889257, "FY2019": 11809204, "FY2018": 11876604, "FY2017": 12002979, "FY2016": 12650459}),
    ],
    cash_flow_unit="£",
    ratios=[
        ("CET1 Ratio", {"FY2023": "52.88%", "FY2022": "53.85%", "FY2021": "52.79%", "FY2020": "51.48%", "FY2019": "58.68%"}),
        ("Total Capital Ratio", {"FY2023": "52.88%", "FY2022": "53.85%", "FY2021": "52.79%", "FY2020": "51.48%", "FY2019": "58.68%"}),
        ("Leverage Ratio", {"FY2023": "35.4%", "FY2022": "33.49%", "FY2021": "33.05%", "FY2020": "~30%", "FY2019": "~30%"}),
        ("LCR", {"FY2023": "835%", "FY2022": "833%", "FY2021": "603%"}),
    ],
    note=ENTITY,
    balance_sheet_totals=[
        ("Total Assets", {"FY2025": 35956037, "FY2024": 36147101, "FY2023": 36293524, "FY2022": 37194488, "FY2021": 40154805, "FY2020": 38940466, "FY2019": 36369860, "FY2018": 33535815, "FY2017": 33576835, "FY2016": 32972669}),
        ("Loans and advances to customers", {"FY2025": 8262627, "FY2024": 9138711, "FY2023": 10330064, "FY2022": 8485497, "FY2021": 7197340, "FY2020": 7314586, "FY2019": 7888087, "FY2018": 6315264, "FY2017": 5210921, "FY2016": 4295209}),
        ("Customer accounts", {"FY2025": 21227564, "FY2024": 22043458, "FY2023": 22687021, "FY2022": 24113288, "FY2021": 25374073, "FY2020": 25034413, "FY2019": 23169408, "FY2018": 21897604, "FY2017": 21344785, "FY2016": 21572515}),
        ("Total equity", {"FY2025": 14117086, "FY2024": 13747327, "FY2023": 13353632, "FY2022": 12952019, "FY2021": 14176202, "FY2020": 13442989, "FY2019": 12867446, "FY2018": 11568761, "FY2017": 11998446, "FY2016": 11071512}),
    ],
    balance_sheet_unit="£",
    income_statement_totals=[
        ("Total operating expense", {"FY2025": -481964, "FY2024": -570759, "FY2023": -551258, "FY2022": -455467, "FY2021": -361324, "FY2020": -371250, "FY2019": -378013, "FY2018": -370280, "FY2017": -361235, "FY2016": -355663}),
        ("Surplus/(deficit) before taxation", {"FY2025": 418967, "FY2024": 489534, "FY2023": 478770, "FY2022": -1718227, "FY2021": 977572, "FY2020": 702221, "FY2019": 1559263, "FY2018": -572535, "FY2017": 880487, "FY2016": 804283}),
        ("Surplus/(deficit) for the period/year", {"FY2025": 371112, "FY2024": 395012, "FY2023": 402846, "FY2022": -1223070, "FY2021": 734281, "FY2020": 576601, "FY2019": 1299726, "FY2018": -428667, "FY2017": 927913, "FY2016": 757654}),
    ],
    income_statement_unit="£",
    equity_changes_totals=[
        ("Surplus/(deficit) for the period/year", {"FY2025": 371112, "FY2024": 395012, "FY2023": 402846, "FY2022": -1223070, "FY2021": 734281, "FY2020": 576601, "FY2019": 1299726, "FY2018": -428667, "FY2017": 927913, "FY2016": 757654}),
        ("Dividends paid and payable", {"FY2025": -1353, "FY2024": -1317, "FY2023": -1233, "FY2022": -1113, "FY2021": -1068, "FY2020": -1058, "FY2019": -1041, "FY2018": -1018, "FY2017": -979, "FY2016": -967}),
        ("Closing equity", {"FY2025": 14117086, "FY2024": 13747327, "FY2023": 13353632, "FY2022": 12952019, "FY2021": 14176202, "FY2020": 13442989, "FY2019": 12867446, "FY2018": 11568761, "FY2017": 11998446, "FY2016": 11071512}),
    ],
    equity_changes_unit="£",
)

bw.save("/Users/armaan/code/katalysis/banks/METHODIST CHAPEL AID FINANCIALS.xlsx")
print("Saved.")
