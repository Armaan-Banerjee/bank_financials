import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

AR_2025 = "https://www.mcafundingforchurches.co.uk/media/4bcl2vk5/mca-ar-2025.pdf"
AR_2024 = "https://www.mcafundingforchurches.co.uk/media/keybconk/annual-report-2024.pdf"
AR_2022 = "https://www.mcafundingforchurches.co.uk/sitefiles/resources/pdf/annualreport2022.pdf"
P3_2023 = "https://www.mcafundingforchurches.co.uk/media/ngqlqg5o/pillar-3-disclosures-2023.pdf"
P3_2022 = "https://www.mcafundingforchurches.co.uk/siteFiles/resources/pdf/Pillar3disclosures2022.pdf"

ENTITY = (
    "ENTITY NOTE: Methodist Chapel Aid Limited (Companies House 00030546, FRN 204508, "
    "LEI 213800GD7EDYBP4LH202) matches Banks List 2608.xlsx and Companies House. It is a "
    "UK-incorporated PRA/FCA-authorised bank operating on a standalone company basis. The "
    "2025 reporting period covers nine months ended 30 September 2025 after the accounting "
    "reference date changed from 31 December. The Company states that its Pillar 3 policy is "
    "annual. No defensible entity-level interim Pillar 3 series was located, so this is a "
    "13-sheet annual workbook. FY2024 and FY2025 absolute regulatory capital metrics were "
    "not separately disclosed in the located sources and are left blank rather than inferred "
    "from statutory net assets. MREL was not disclosed."
)


def cash_sources():
    return (
        "Sources - Methodist Chapel Aid Limited entity-level Statement of Cash Flows, £:\n"
        f"FY2025 (9 months ended 30 September 2025): MCA Annual report and accounts 2025, pp. 38-39 - {AR_2025}\n"
        f"FY2024: MCA Annual report and accounts 2024, pp. 36-39 - {AR_2024}\n"
        f"FY2023: MCA Annual report and accounts 2024 comparative, p. 39 - {AR_2024}\n"
        f"FY2022: MCA Annual report and accounts 2022, p. 38 - {AR_2022}\n"
        f"FY2021: MCA Annual report and accounts 2022 comparative, p. 38 - {AR_2022}\n\n"
        + ENTITY
    )


def p3_sources():
    return (
        "Sources - Methodist Chapel Aid Limited entity-level Pillar 3 / regulatory capital disclosures, £'000 unless stated:\n"
        f"FY2023: Pillar 3 Disclosures for year ended 31 December 2023, Key Metrics table, p. 3 - {P3_2023}\n"
        f"FY2022 and FY2021: Pillar 3 Disclosures for year ended 31 December 2022, Key Metrics table, p. 3 - {P3_2022}\n"
        "FY2024/FY2025: no separate absolute Key Metrics table was located; values left blank.\n\n"
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
    f"Statement of Financial Position p.36 - {AR_2022}\n\n"
    "Note: the Company has no standalone Statement of Changes in Equity - equity movements are shown within "
    "the combined Statement of Income and Retained Earnings (surplus/(deficit) for the period less dividends "
    "paid and payable, rolled into Reserves; Called up equity share capital is unchanged across all 5 years). "
    "The 2025 reporting period covers 9 months (accounting reference date changed from 31 December to 30 "
    "September); all other periods are 12 months.\n\n"
    + ENTITY
)

ASSET_QUALITY_SOURCES = (
    "Sources - Methodist Chapel Aid Limited entity-level loan book detail, Note 11/13 Debtors (Loans and "
    "advances to customers), £:\n"
    f"FY2025 and FY2024 comparative: MCA Annual report and accounts 2025, Note 11, pp.49-50 - {AR_2025}\n"
    f"FY2023 comparative: MCA Annual report and accounts 2024, Note 11, pp.47-48 - {AR_2024}\n"
    f"FY2022 and FY2021 comparative: MCA Annual report and accounts 2022, Note 13, pp.48-49 - {AR_2022}\n\n"
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
    "periods (consistent with the existing Total RWAs sheet, which is also blank for these years).\n\n"
    + ENTITY
)


bw = BankWorkbook("Methodist Chapel Aid Limited", YEARS, header_color="6B4E71")

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and bank balances", {"FY2025": 9417754, "FY2024": 8355272, "FY2023": 7520873, "FY2022": 10132743, "FY2021": 12459792}),
    ("DATA", "Loans and advances to customers", {"FY2025": 8262627, "FY2024": 9138711, "FY2023": 10330064, "FY2022": 8485497, "FY2021": 7197340}),
    ("DATA", "Investments - issued by public body", {"FY2025": 4941874, "FY2024": 4208030, "FY2023": 4824018}),
    ("DATA", "Investments - other loans and advances", {"FY2025": 3843427, "FY2024": 4049871, "FY2023": 4500425}),
    ("DATA", "Investments - equity investments", {"FY2025": 8230600, "FY2024": 8135418, "FY2023": 7100690}),
    ("TOTAL", "Total investments", {"FY2025": 17015901, "FY2024": 16393319, "FY2023": 16425133, "FY2022": 16047858, "FY2021": 17733105}),
    ("DATA", "Intangible fixed assets", {"FY2025": 3957}),
    ("DATA", "Tangible fixed assets", {"FY2025": 287367, "FY2024": 300959, "FY2023": 305490, "FY2022": 37749, "FY2021": 31127}),
    ("DATA", "Investments held for short term purposes", {"FY2025": 748688, "FY2024": 1831800, "FY2023": 1576261, "FY2022": 2380720, "FY2021": 2661841}),
    ("DATA", "Prepayments, accrued income and other assets", {"FY2025": 219743, "FY2024": 127040, "FY2023": 135703, "FY2022": 109921, "FY2021": 71600}),
    ("TOTAL", "Total Assets", {"FY2025": 35956037, "FY2024": 36147101, "FY2023": 36293524, "FY2022": 37194488, "FY2021": 40154805}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer accounts", {"FY2025": 21227564, "FY2024": 22043458, "FY2023": 22687021, "FY2022": 24113288, "FY2021": 25374073}),
    ("DATA", "Other liabilities", {"FY2025": 370311, "FY2024": 167472, "FY2023": 131713, "FY2022": 83947, "FY2021": 64139}),
    ("TOTAL", "Total Liabilities", {"FY2025": 21597875, "FY2024": 22210930, "FY2023": 22818734, "FY2022": 24197235, "FY2021": 25438212}),
    ("SECTION", "Provisions", {}),
    ("DATA", "Deferred tax", {"FY2025": 241076, "FY2024": 188844, "FY2023": 121158, "FY2022": 45234, "FY2021": 540391}),
    ("TOTAL", "Net Assets", {"FY2025": 14117086, "FY2024": 13747327, "FY2023": 13353632, "FY2022": 12952019, "FY2021": 14176202}),
    ("SECTION", "Shareholders' Funds", {}),
    ("DATA", "Called up equity share capital", {"FY2025": 1197, "FY2024": 1197, "FY2023": 1197, "FY2022": 1197, "FY2021": 1197}),
    ("DATA", "Reserves", {"FY2025": 14115889, "FY2024": 13746130, "FY2023": 13352435, "FY2022": 12950822, "FY2021": 14175005}),
    ("TOTAL", "Total equity", {"FY2025": 14117086, "FY2024": 13747327, "FY2023": 13353632, "FY2022": 12952019, "FY2021": 14176202}),
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
    ("DATA", "Interest receivable - on loans", {"FY2025": 364536, "FY2024": 542736, "FY2023": 485539, "FY2022": 241994, "FY2021": 226796}),
    ("DATA", "Interest receivable - on debt securities", {"FY2025": 254891, "FY2024": 351721, "FY2023": 346423, "FY2022": 292232, "FY2021": 297207}),
    ("DATA", "Interest receivable - on bank and building society deposits", {"FY2025": 301668, "FY2024": 412981, "FY2023": 347139, "FY2022": 114132, "FY2021": 11584}),
    ("DATA", "Interest payable to depositors", {"FY2025": -513856, "FY2024": -702772, "FY2023": -570746, "FY2022": -167638, "FY2021": -158940}),
    ("DATA", "Interest payable - amortisation of debt securities", {"FY2025": -12204, "FY2024": -55620, "FY2023": -101184, "FY2022": -87073, "FY2021": -86814}),
    ("DATA", "Dividend income from equity shares", {"FY2025": 149236, "FY2024": 186640, "FY2023": 172192, "FY2022": 226757, "FY2021": 220001}),
    ("DATA", "Investment gains/(losses) on debt securities", {"FY2024": -371214, "FY2023": -27579, "FY2022": -12251, "FY2021": -30549}),
    ("DATA", "Fees and commissions payable to Investment Manager", {"FY2025": -32837, "FY2024": -3575, "FY2023": -19845, "FY2022": -37299, "FY2021": -29476}),
    ("DATA", "Other operating income", {"FY2025": 4302, "FY2024": 4900, "FY2023": 6543, "FY2022": 11797, "FY2021": 177145}),
    ("DATA", "Administrative expenses - staff costs", {"FY2025": -241735, "FY2024": -310501, "FY2023": -281131, "FY2022": -236031, "FY2021": -202930}),
    ("DATA", "Administrative expenses - other", {"FY2025": -230594, "FY2024": -246970, "FY2023": -260190, "FY2022": -212268, "FY2021": -154761}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -9635, "FY2024": -13288, "FY2023": -9937, "FY2022": -7168, "FY2021": -3633}),
    ("TOTAL", "Operating surplus/(deficit)", {"FY2025": 33772, "FY2024": -204962, "FY2023": 87224, "FY2022": 127184, "FY2021": 265630}),
    ("DATA", "Fair value adjustment to investments", {"FY2025": 385195, "FY2024": 694496, "FY2023": 391546, "FY2022": -1845411, "FY2021": 711942}),
    ("TOTAL", "Surplus/(deficit) on ordinary activities before taxation", {"FY2025": 418967, "FY2024": 489534, "FY2023": 478770, "FY2022": -1718227, "FY2021": 977572}),
    ("DATA", "Tax on surplus/(deficit) on ordinary activities", {"FY2025": -47855, "FY2024": -94522, "FY2023": -75924, "FY2022": 495157, "FY2021": -243291}),
    ("TOTAL", "Surplus/(deficit) for the period/year and total comprehensive income", {"FY2025": 371112, "FY2024": 395012, "FY2023": 402846, "FY2022": -1223070, "FY2021": 734281}),
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
    ("TOTAL", "Balance at 1 January 2021", (1197, 13441792, 13442989)),
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
    ("TOTAL", "Net cash generated/(used) from operating activities", {"FY2025": 230314, "FY2024": 429322, "FY2023": -3050504, "FY2022": -2346030, "FY2021": 714322}),
    ("SECTION", "Investing activities", {}),
    ("TOTAL", "Net cash generated/(used) from investing activities", {"FY2025": -249591, "FY2024": 661933, "FY2023": -364592, "FY2022": -261027, "FY2021": 519122}),
    ("SECTION", "Financing activities", {}),
    ("TOTAL", "Net cash generated/(used) in financing activities", {"FY2025": -1353, "FY2024": -1317, "FY2023": -1233, "FY2022": -1113, "FY2021": -1068}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": -20630, "FY2024": 1089938, "FY2023": -3416329, "FY2022": -2608170, "FY2021": 1232376}),
    ("DATA", "Cash and cash equivalents at the beginning of year/period", {"FY2025": 10187072, "FY2024": 9097134, "FY2023": 12513463, "FY2022": 15121633, "FY2021": 13889257}),
    ("TOTAL", "Cash and cash equivalents at the end of year/period", {"FY2025": 10166442, "FY2024": 10187072, "FY2023": 9097134, "FY2022": 12513463, "FY2021": 15121633}),
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
    ("DATA", "Property loans - secured", {"FY2025": 6882826, "FY2024": 7487986, "FY2023": 7265355, "FY2022": 7037375, "FY2021": 5840927}),
    ("DATA", "Property loans - unsecured", {"FY2025": 1375657, "FY2024": 1644631, "FY2023": 3055122, "FY2022": 1432495, "FY2021": 1346352}),
    ("TOTAL", "Property loans - total", {"FY2025": 8258483, "FY2024": 9132617, "FY2023": 10320477, "FY2022": 8469870, "FY2021": 7187279}),
    ("DATA", "Car loans - unsecured", {"FY2025": 4250, "FY2024": 6250, "FY2023": 9833, "FY2022": 16028, "FY2021": 10319}),
    ("TOTAL", "Total loans and advances (gross)", {"FY2025": 8262733, "FY2024": 9138867, "FY2023": 10330310, "FY2022": 8485898, "FY2021": 7197598}),
    ("DATA", "Provision for bad debts", {"FY2025": -106, "FY2024": -156, "FY2023": -246, "FY2022": -401, "FY2021": -258}),
    ("TOTAL", "Total loans and advances (net)", {"FY2025": 8262627, "FY2024": 9138711, "FY2023": 10330064, "FY2022": 8485497, "FY2021": 7197340}),
    ("SECTION", "Maturity profile of loans and advances (net)", {}),
    ("DATA", "Due within 3 months", {"FY2025": 480809, "FY2024": 350750, "FY2023": 1449455, "FY2022": 1861, "FY2021": 1848}),
    ("DATA", "In more than 3 months but not more than 1 year", {"FY2025": 1166309, "FY2024": 1907530, "FY2023": 2103477, "FY2022": 2223451, "FY2021": 364515}),
    ("DATA", "In more than 1 year but not more than 5 years", {"FY2025": 3075037, "FY2024": 3184280, "FY2023": 3463531, "FY2022": 3069212, "FY2021": 3182168}),
    ("DATA", "In more than 5 years", {"FY2025": 3540578, "FY2024": 3696307, "FY2023": 3313847, "FY2022": 3191374, "FY2021": 3649067}),
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


metric("CET1 Capital", "£'000", "CET1 capital", {"FY2023": 13354, "FY2022": 12952, "FY2021": 13919}, "FY2024 and FY2025 absolute regulatory capital was not separately disclosed in the located sources.")
metric("CET1 Ratio", "%", "CET1 ratio", {"FY2023": "52.88%", "FY2022": "53.85%", "FY2021": "52.79%"}, "FY2024 and FY2025 ratio not separately disclosed in the located sources.")
metric("Tier 1 Capital", "£'000", "Tier 1 capital", {"FY2023": 13354, "FY2022": 12952, "FY2021": 13919}, "All disclosed Tier 1 capital was CET1; FY2024 and FY2025 were not separately disclosed.")
metric("Tier 1 Ratio", "%", "Tier 1 ratio", {"FY2023": "52.88%", "FY2022": "53.85%", "FY2021": "52.79%"}, "FY2024 and FY2025 ratio not separately disclosed in the located sources.")
metric("Total Capital", "£'000", "Total capital", {"FY2023": 13354, "FY2022": 12952, "FY2021": 13919}, "All disclosed total capital was CET1; FY2024 and FY2025 were not separately disclosed.")
metric("Total Capital Ratio", "%", "Total capital ratio", {"FY2023": "52.88%", "FY2022": "53.85%", "FY2021": "52.79%"}, "FY2024 and FY2025 ratio not separately disclosed in the located sources.")
metric("Total RWAs", "£'000", "Total risk-weighted exposure amount", {"FY2023": 25253, "FY2022": 24052, "FY2021": 26369}, "FY2024 and FY2025 absolute RWA was not separately disclosed in the located sources.")

rwa_breakdown_rows = [
    ("SECTION", "Credit risk exposure by class (Risk Weighted Exposure)", {}),
    ("DATA", "Credit institutions", {"FY2023": 1825, "FY2022": 2713}),
    ("DATA", "UK Treasury Stocks", {"FY2023": 0, "FY2022": 0}),
    ("DATA", "Collective investment undertakings", {"FY2023": 3271, "FY2022": 3092}),
    ("DATA", "Equity investments", {"FY2023": 7101, "FY2022": 7160}),
    ("DATA", "Higher Risk Weighted Equities", {"FY2022": 30}),
    ("DATA", "Property loans and advances to customers (drawn)", {"FY2023": 10320, "FY2022": 8470}),
    ("DATA", "Property loans and advances to customers (50% of undrawn)", {"FY2023": 1125, "FY2022": 1195}),
    ("DATA", "Car loans and advances to customers", {"FY2023": 7, "FY2022": 12}),
    ("DATA", "Fixed and other assets", {"FY2023": 436, "FY2022": 145}),
    ("TOTAL", "Total credit risk exposure (RWA)", {"FY2023": 24085, "FY2022": 22817}),
    ("DATA", "Operational risk capital requirement (RWA)", {"FY2023": 1168, "FY2022": 1235}),
    ("TOTAL", "Total RWAs (Pillar 1)", {"FY2023": 25253, "FY2022": 24052, "FY2021": 26369}),
]
bw.add_rwa_breakdown_sheet(
    "Methodist Chapel Aid Limited — RWA Breakdown",
    "Entity-level basis, £'000, Standardised Approach.",
    rwa_breakdown_rows,
    RWA_BREAKDOWN_SOURCES,
    first_col_width=58,
    source_height=230,
)

metric("Leverage Ratio", "%", "Leverage ratio", {"FY2023": "35.4%", "FY2022": "33.49%", "FY2021": "33.05%"}, "The Company states that the smaller-bank leverage requirement does not apply; reported ratios are included as disclosed. FY2024 and FY2025 were not separately disclosed.")
metric("LCR", "%", "Average liquidity coverage ratio", {"FY2023": "835%", "FY2022": "833%", "FY2021": "603%"}, "FY2023 is the average based on quarterly end-of-month positions; FY2024 and FY2025 were not separately disclosed.")
metric("NSFR", "%", "Average net stable funding ratio", {"FY2023": "182%", "FY2022": "192%", "FY2021": "184%"}, "FY2023 is the average based on quarterly end-of-month positions; FY2024 and FY2025 were not separately disclosed.")
bw.add_not_disclosed_metric_sheets(["MREL Ratio"], p3_sources(), per_note={"MREL Ratio": "No MREL ratio was disclosed in the located Methodist Chapel Aid Pillar 3 documents."})

bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash generated/(used) from operating activities", {"FY2025": 230314, "FY2024": 429322, "FY2023": -3050504, "FY2022": -2346030, "FY2021": 714322}),
        ("Net cash generated/(used) from investing activities", {"FY2025": -249591, "FY2024": 661933, "FY2023": -364592, "FY2022": -261027, "FY2021": 519122}),
        ("Net cash generated/(used) in financing activities", {"FY2025": -1353, "FY2024": -1317, "FY2023": -1233, "FY2022": -1113, "FY2021": -1068}),
        ("Cash and cash equivalents at end of year/period", {"FY2025": 10166442, "FY2024": 10187072, "FY2023": 9097134, "FY2022": 12513463, "FY2021": 15121633}),
    ],
    cash_flow_unit="£",
    ratios=[
        ("CET1 Ratio", {"FY2023": "52.88%", "FY2022": "53.85%", "FY2021": "52.79%"}),
        ("Total Capital Ratio", {"FY2023": "52.88%", "FY2022": "53.85%", "FY2021": "52.79%"}),
        ("Leverage Ratio", {"FY2023": "35.4%", "FY2022": "33.49%", "FY2021": "33.05%"}),
        ("LCR", {"FY2023": "835%", "FY2022": "833%", "FY2021": "603%"}),
    ],
    note=ENTITY,
    balance_sheet_totals=[
        ("Total Assets", {"FY2025": 35956037, "FY2024": 36147101, "FY2023": 36293524, "FY2022": 37194488, "FY2021": 40154805}),
        ("Loans and advances to customers", {"FY2025": 8262627, "FY2024": 9138711, "FY2023": 10330064, "FY2022": 8485497, "FY2021": 7197340}),
        ("Customer accounts", {"FY2025": 21227564, "FY2024": 22043458, "FY2023": 22687021, "FY2022": 24113288, "FY2021": 25374073}),
        ("Total equity", {"FY2025": 14117086, "FY2024": 13747327, "FY2023": 13353632, "FY2022": 12952019, "FY2021": 14176202}),
    ],
    balance_sheet_unit="£",
    income_statement_totals=[
        ("Total operating expense", {"FY2025": -481964, "FY2024": -570759, "FY2023": -551258, "FY2022": -455467, "FY2021": -361324}),
        ("Surplus/(deficit) before taxation", {"FY2025": 418967, "FY2024": 489534, "FY2023": 478770, "FY2022": -1718227, "FY2021": 977572}),
        ("Surplus/(deficit) for the period/year", {"FY2025": 371112, "FY2024": 395012, "FY2023": 402846, "FY2022": -1223070, "FY2021": 734281}),
    ],
    income_statement_unit="£",
    equity_changes_totals=[
        ("Surplus/(deficit) for the period/year", {"FY2025": 371112, "FY2024": 395012, "FY2023": 402846, "FY2022": -1223070, "FY2021": 734281}),
        ("Dividends paid and payable", {"FY2025": -1353, "FY2024": -1317, "FY2023": -1233, "FY2022": -1113, "FY2021": -1068}),
        ("Closing equity", {"FY2025": 14117086, "FY2024": 13747327, "FY2023": 13353632, "FY2022": 12952019, "FY2021": 14176202}),
    ],
    equity_changes_unit="£",
)

bw.save("/Users/armaan/code/katalysis/banks/METHODIST CHAPEL AID FINANCIALS.xlsx")
print("Saved.")
