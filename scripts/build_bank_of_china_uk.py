import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = [
    "FY2025", "FY2024", "FY2023", "FY2022", "FY2021",
    "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014",
]  # most recent first

AR2021_URL = "https://pic.bankofchina.com/bocappd/uk/202303/P020230331590070165221.pdf"
AR2022_URL = "https://pic.bankofchina.com/bocappd/uk/202403/P020240315379765805794.pdf"
AR2023_URL = "https://pic.bankofchina.com/bocappd/uk/202405/P020240508355110735895.pdf"
AR2024_URL = "https://pic.bankofchina.com/bocappd/uk/202507/P020250718380377744220.pdf"
AR2025_URL = "https://pic.bankofchina.com/bocappd/uk/202605/P020260506389809417235.pdf"

P3_2021_URL = "https://www.bankofchina.com/uk/aboutus/ab5/202303/P020230315381669571541.pdf"
P3_2022_URL = "https://www.bankofchina.com/uk/aboutus/ab5/202310/P020231026347190320350.pdf"
P3_2023_URL = "https://www.bankofchina.com/uk/aboutus/ab5/202410/P020241008402737321677.pdf"
P3_2024_URL = "https://www.bankofchina.com/uk/aboutus/ab5/202507/P020250718380587744231.pdf"
P3_2025_URL = "https://pic.bankofchina.com/bocappd/uk/202607/P020260716391457618567.pdf"

# --- HD-046 (2026-09-05): FY2014-FY2020 extension, capped at FY2014 by explicit
# user decision even though the entity's own archive genuinely runs to FY2008
# (HD-001's reference finding). All 14 documents below are still live on
# bankofchina.com/pic.bankofchina.com (confirmed via direct HTTP fetch, no
# Wayback fallback needed) - the deepest, cleanest self-hosted archive found
# across the whole HD- effort so far.
AR2020_URL = "https://pic.bankofchina.com/bocappd/uk/202109/P020210902654360894172.pdf"
AR2019_URL = "https://pic.bankofchina.com/bocappd/uk/202007/P020200727323473194461.pdf"
AR2018_URL = "https://pic.bankofchina.com/bocappd/uk/201904/P020190410506087628158.pdf"
AR2017_URL = "https://pic.bankofchina.com/bocappd/uk/201805/P020180517534275167127.pdf"
AR2016_URL = "https://pic.bankofchina.com/bocappd/uk/201706/P020170627373089457851.pdf"
AR2015_URL = "https://pic.bankofchina.com/bocappd/uk/201606/P020160620504225340480.pdf"
AR2014_URL = "https://pic.bankofchina.com/bocappd/uk/201505/P020150504352614441641.pdf"

P3_2020_URL = "https://pic.bankofchina.com/bocappd/uk/202110/P020211027537761891740.pdf"
P3_2019_URL = "https://pic.bankofchina.com/bocappd/uk/202009/P020200909535865685853.pdf"
P3_2018_URL = "https://pic.bankofchina.com/bocappd/uk/201904/P020190410408108385209.pdf"
P3_2017_URL = "https://pic.bankofchina.com/bocappd/uk/201803/P020180328577372288229.pdf"
P3_2016_URL = "https://pic.bankofchina.com/bocappd/uk/201706/P020170627381103226068.pdf"
P3_2015_URL = "https://pic.bankofchina.com/bocappd/uk/201606/P020160620504436264971.pdf"
P3_2014_URL = "https://pic.bankofchina.com/bocappd/uk/201509/P020150910375228515274.pdf"

AR2014_SCAN_NOTE = (
    "AR2014_URL note: the Bank's own FY2014 Annual Report PDF is a scanned/photocopied "
    "document (Canon iR-ADV C5045 scanner output) with no extractable text layer - "
    "pdftotext and qpdf both confirm zero recoverable text after a repair pass. FY2014 "
    "figures on every sheet are therefore taken from the FY2015 Annual Report's own "
    "FY2014 comparative column instead (a real, live, text-searchable document), the "
    "same each-year's-own-report methodology used everywhere else in this workbook, "
    "just one year removed since FY2014's own PDF cannot be read as text."
)

ENTITY_NOTE = (
    "Entity note: Bank of China (UK) Limited (company 06193060, FRN 467410) is a wholly-owned UK subsidiary of "
    "Bank of China Limited (state-owned). It does not take the FRS 101/102 cash-flow-statement exemption - a full "
    "Statement of Cash Flows is published every year. All figures are the Bank's own solo entity basis throughout."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Bank of China (UK) Limited's own Statement of Cash Flows, £'000, as published on "
    "the Bank's own site (each year's own originally-published report, not a later restated comparative):\n"
    f"FY2025: Annual Report and Financial Statements for the year ended 31 December 2025, p.51-52 - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements for the year ended 31 December 2024, p.52-53 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements for the year ended 31 December 2023, p.52-53 - {AR2023_URL}\n"
    f"FY2022: Financial Statements for the year ended 31 December 2022, p.40 - {AR2022_URL}\n"
    f"FY2021: Financial Statements for the year ended 31 December 2021, p.37 - {AR2021_URL}\n"
    f"FY2020: Financial Statements for the year ended 31 December 2020, p.34-35 - {AR2020_URL}\n"
    f"FY2019: Financial Statements for the year ended 31 December 2019, p.33-34 - {AR2019_URL}\n"
    f"FY2018: Financial Statements for the year ended 31 December 2018, p.28-29 - {AR2018_URL}\n"
    f"FY2017: Financial Statements for the year ended 31 December 2017, p.26-27 - {AR2017_URL}\n"
    f"FY2016: Financial Statements for the year ended 31 December 2016, p.21-22 - {AR2016_URL}\n"
    f"FY2015: Financial Statements for the year ended 31 December 2015, p.20-21 - {AR2015_URL}\n"
    f"FY2014: Financial Statements 2015's own FY2014 comparative column, p.20-21 - {AR2015_URL} ({AR2014_SCAN_NOTE})\n"
    "FY2014-FY2020 presentation note: through FY2020's own report, 'Dividend paid' and 'Interest paid' sit inside "
    "the operating-activities 'Adjustment for cash items' subsection (own rows here, labelled '...FY2014-FY2020 "
    "presentation' to distinguish them from the FY2021-onward financing-section rows of the same name, which are "
    "left blank for FY2014-FY2020 rather than merged into a single row spanning two different statement "
    "sections); 'Cash flows from financing activities' is genuinely nil every year FY2014-FY2019 and, in FY2020's "
    "own report, contains only the new lease-liability repayment line. FY2014's cash flow reconciles a genuine "
    "£100k discrepancy against the Balance Sheet (see the Balance Sheet sheet's own source note); every other "
    "year's cash-flow closing balance ties exactly to that year's own Balance Sheet cash figure. Individual "
    "reconciling items were independently verified by summing each year's disclosed components back to that "
    "year's own reported 'Net cash generated from operating activities' total (all matched exactly), used as a "
    "correction check against several PDFs' garbled OCR text (e.g. FY2014's 'Acquisition of intangible assets' "
    "printed without its minus sign was resolved to -£426k this way).\n"
    "Restatement note: FY2023's own report marks its FY2022 comparative column 'Restated' and shows different "
    "figures (e.g. operating activities -£17,138k, closing cash £687,013k) to FY2022's own originally-published "
    "report (operating activities +£22,570k, closing cash £657,656k). This workbook uses each year's own "
    "originally-published figures as the primary column (project convention), which creates a genuine, disclosed "
    "£29,357k gap between FY2022's own closing balance and FY2023's own opening balance - flagged here rather "
    "than silently blended or force-reconciled. The underlying cause of the restatement is not explained in "
    "either source.\n"
    "Presentation notes: FY2021-FY2023 include small 'Exchange rate movements on plant and equipment/on equity' "
    "lines not present in FY2024/FY2025's statements. FY2022 alone shows a one-off Tier 2-to-AT1 capital "
    "replacement (subordinated debt of £60,000k repaid, an equal Additional Tier 1 instrument issued, both under "
    "financing activities). FY2025's own report split 'Change in financial assets at amortised cost/fair value' "
    "into two lines (the government-bond component shown separately) and separated lease-liability cash flows "
    "into principal and interest portions for the first time - both are FY2025-only presentational changes with "
    "no net impact on any section total. FY2025's own supplementary 'cash and cash equivalents comprise' note "
    "totals £1,073,245k (£157k less than the statement's own £1,073,402k closing balance), a gap matching the "
    "same page's separately-shown expected-credit-loss allowance of £157k - the statement's own total is used as "
    "the primary closing-balance figure here. FY2022's own report does not break out a separate 'Interest paid "
    "on Additional Tier 1 instrument' line (the AT1 instrument was only issued in June 2022); FY2023's restated "
    "FY2022 comparative does show one (£1,759k), consistent with the broader FY2022 restatement noted above - "
    "not included here since it wasn't part of FY2022's own originally-published statement.\n"
    + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - Bank of China (UK) Limited Pillar 3 disclosures (UK KM1 Key Metrics template from FY2022 "
        "onward; FY2021's own document is narrative/ratio-only and predates the KM1 template; FY2014-FY2020 use "
        "the pre-KM1 CRD IV 'Table 1: Total capital resources and risk asset ratios' / 'Table 2: Leverage ratio' "
        "narrative-table format), £'000 unless stated:\n"
        f"FY2025 & FY2024 comparative: Pillar 3 Disclosure 31 December 2025, p.15 (UK KM1) - {P3_2025_URL}\n"
        f"FY2024 (own year) & FY2023 comparative: Pillar 3 Disclosures 31 December 2024, p.16 (UK KM1) - {P3_2024_URL}\n"
        f"FY2023 (own year) & FY2022 comparative: Pillar 3 disclosures 31 December 2023, p.14 (UK KM1) - {P3_2023_URL}\n"
        f"FY2022 (own year) & FY2021 comparative: Pillar 3 Disclosures 2022, p.14 (UK KM1) - {P3_2022_URL}\n"
        f"FY2021 (own year, narrative/ratio-only - no KM1 template yet): Pillar 3 Disclosures 2021, p.12-14, 24 - {P3_2021_URL}\n"
        "FY2021 note: the Bank's own FY2021 Pillar 3 document states CET1/Total Capital as rounded £275m/£335m "
        "and gives no £-breakdown for leverage exposure, LCR HQLA/outflow, or NSFR (NSFR was not yet a formal "
        "disclosure). The precise FY2021 figures used on those sheets (CET1/Tier 1 £275,164k, Total Capital "
        "£335,164k, leverage exposure £2,431,869k, LCR HQLA £527,697k/outflow £294,774k, NSFR £1,438,026k/"
        "£950,742k) are taken from the FY2022 Pillar 3 document's FY2021 comparative column instead, since it is "
        "the more complete disclosure - all overlapping ratios (CET1 24.6%, Total Capital 29.9%, Leverage 11.3%, "
        "LCR 179.0%) match the FY2021 document's own narrative figures exactly.\n"
        f"FY2020 (own year) & FY2019 comparative: Pillar 3 Disclosures 31 December 2020, Table 9 'Overview of "
        f"risk weighted assets', p.20-22, Table 31 'Liquidity coverage ratio' - {P3_2020_URL}\n"
        f"FY2019 (own year) & FY2018 comparative: Pillar 3 Disclosures 31 December 2019, p.16-19, 33 - {P3_2019_URL}\n"
        f"FY2018 (own year) & FY2017 comparative: Pillar 3 Disclosures 31 December 2018, p.15-18, 31 - {P3_2018_URL}\n"
        f"FY2017 (own year) & FY2016 comparative: Pillar 3 Disclosures 2017, Table 1/Table 2, p.9-10 - {P3_2017_URL}\n"
        f"FY2016 (own year) & FY2015 comparative: Pillar 3 Disclosures 2016, Table 1/Table 2, p.10-11 - {P3_2016_URL}\n"
        f"FY2015 (own year) & FY2014 comparative: Pillar III Disclosures 2015, Table 1/Table 2, p.9-10 - {P3_2015_URL}\n"
        f"FY2014 (own year) & FY2013 comparative: Pillar III Disclosure 2014, Table 1/Table 2, p.8-9 - {P3_2014_URL}\n"
        "FY2014-FY2017 note: 'Tier 1 capital' equals 'CET1 capital' every year (£274,958k throughout - the Bank "
        "issued no AT1 instruments until far later) and 'Total capital' equals CET1 capital plus the £60,000k "
        "Tier 2 subordinated debt facility, both stated directly in each year's own Table 1. LCR and NSFR are "
        "genuinely undisclosed for FY2014-FY2016 (no LCR/HQLA/NSFR concept appears anywhere in those 3 documents, "
        "confirmed by reading each in full); FY2017's LCR ratio (167%) is not in FY2017's own document at all "
        "(confirmed absent) but appears as the FY2018 Pillar 3 document's own FY2017 comparative column, the "
        "earliest point any LCR figure for this bank exists - shown here with no £-breakdown since none is given "
        "for that comparative year. RWA breakdown by risk category (credit/market/operational/CVA) is genuinely "
        "undisclosed for FY2014-FY2018 (only the single aggregate RWA figure appears in each Table 1); the FY2020 "
        "Pillar 3 document introduces a full 'Table 9: Overview of risk weighted assets' (its own year plus its "
        "own FY2019 comparative column), the first and only such breakdown found across all 12 years covered.\n"
        + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="Bank of China (UK) Limited", years=YEARS, header_color="B22222")

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
AR2024_OWN_NOTE = (
    "FY2024's own primary source is its own report (AR2024_URL), not AR2025's comparative column - both are "
    "identical figures (verified), no restatement."
)

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 982512, "FY2024": 975201, "FY2023": 687070, "FY2022": 657656, "FY2021": 716133, "FY2020": 481379, "FY2019": 332542, "FY2018": 333275, "FY2017": 281944, "FY2016": 311917, "FY2015": 344019, "FY2014": 199954}),
    ("DATA", "Government bonds", {"FY2025": 142529, "FY2024": 144495, "FY2023": 118328, "FY2022": 44264}),
    ("DATA", "Loans and advances to banks", {"FY2025": 90733, "FY2024": 73658, "FY2023": 86477, "FY2022": 29357, "FY2021": 69065, "FY2020": 110446, "FY2019": 85247, "FY2018": 61391, "FY2017": 83706, "FY2016": 24270, "FY2015": 62633, "FY2014": 207026}),
    ("DATA", "Loans and advances to customers", {"FY2025": 810985, "FY2024": 941507, "FY2023": 990763, "FY2022": 1122459, "FY2021": 1194653, "FY2020": 1138583, "FY2019": 1064347, "FY2018": 1044570, "FY2017": 1054454, "FY2016": 1159696, "FY2015": 810776, "FY2014": 722307}),
    ("DATA", "Derivative financial instruments", {"FY2025": 2504, "FY2024": 4667, "FY2023": 5506, "FY2022": 7702, "FY2021": 11, "FY2020": 48163, "FY2019": 4614, "FY2018": 1344, "FY2017": 1717, "FY2016": 4577, "FY2015": 8173, "FY2014": 16173}),
    ("DATA", "Prepayments, accrued income and other assets", {"FY2025": 156554, "FY2024": 138246, "FY2023": 130581, "FY2022": 351967, "FY2021": 87868, "FY2020": 78769, "FY2019": 58405, "FY2018": 6273, "FY2017": 5204, "FY2016": 4762, "FY2015": 25831, "FY2014": 27820}),
    ("DATA", "Financial assets at fair value through profit and loss", {"FY2025": 71293, "FY2024": 30150, "FY2023": 47445, "FY2022": 60514, "FY2021": 64659, "FY2020": 77482, "FY2019": 83928, "FY2018": 76171}),
    ("DATA", "Available for sale financial investments", {"FY2017": 12, "FY2016": 40716, "FY2015": 35859, "FY2014": 37469}),
    ("DATA", "Held to maturity / debt instruments at amortised cost", {"FY2019": 50431, "FY2018": 103189, "FY2017": 107478}),
    ("DATA", "Current tax asset", {"FY2025": 4582, "FY2024": 2934, "FY2023": 637, "FY2022": 2351, "FY2021": 5979}),
    ("DATA", "Deferred tax assets", {"FY2025": 289, "FY2024": 406, "FY2023": 359, "FY2022": 1280, "FY2021": 1283, "FY2020": 1227, "FY2019": 787, "FY2018": 1546, "FY2017": 1462, "FY2016": 562, "FY2015": 425, "FY2014": 751}),
    ("DATA", "Property, plant and equipment", {"FY2025": 11573, "FY2024": 11419, "FY2023": 11902, "FY2022": 12769, "FY2021": 11167, "FY2020": 4527, "FY2019": 6328, "FY2018": 2761, "FY2017": 3149, "FY2016": 3276, "FY2015": 3514, "FY2014": 3390}),
    ("DATA", "Intangible assets", {"FY2025": 887, "FY2024": 636, "FY2023": 305, "FY2022": 274, "FY2021": 362, "FY2020": 529, "FY2019": 759, "FY2018": 462, "FY2017": 95, "FY2016": 122, "FY2015": 180, "FY2014": 326}),
    ("TOTAL", "Total assets", {"FY2025": 2274441, "FY2024": 2323319, "FY2023": 2079373, "FY2022": 2290593, "FY2021": 2151180, "FY2020": 1941105, "FY2019": 1687388, "FY2018": 1630982, "FY2017": 1539221, "FY2016": 1549898, "FY2015": 1291410, "FY2014": 1215116}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks", {"FY2025": 511961, "FY2024": 493256, "FY2023": 369590, "FY2022": 539387, "FY2021": 396254, "FY2020": 219378, "FY2019": 128590, "FY2018": 102919, "FY2017": 123122, "FY2016": 164849, "FY2015": 136736, "FY2014": 40270}),
    ("DATA", "Deposits from customers", {"FY2025": 1304816, "FY2024": 1355529, "FY2023": 1223068, "FY2022": 1291150, "FY2021": 1333523, "FY2020": 1215647, "FY2019": 1132193, "FY2018": 1107439, "FY2017": 1019007, "FY2016": 982361, "FY2015": 737724, "FY2014": 765899}),
    ("DATA", "Derivative financial instruments", {"FY2025": 289, "FY2024": 2, "FY2023": 3, "FY2022": 13, "FY2021": 5280, "FY2020": 56924, "FY2019": 8771, "FY2018": 1977, "FY2017": 257, "FY2016": 4150, "FY2015": 11505, "FY2014": 21499}),
    ("DATA", "Other liabilities", {"FY2025": 39574, "FY2024": 37473, "FY2023": 38352, "FY2022": 50379, "FY2021": 43571, "FY2020": 36086, "FY2019": 43609, "FY2018": 21359, "FY2017": 20158, "FY2016": 13620, "FY2015": 17145, "FY2014": 18089}),
    ("DATA", "Accruals and deferred income", {"FY2025": 18650, "FY2024": 23257, "FY2023": 15017, "FY2022": 7720, "FY2021": 5657, "FY2020": 5705, "FY2019": 6390, "FY2018": 6207, "FY2017": 4176, "FY2016": 5874, "FY2015": 4512, "FY2014": 4016}),
    ("DATA", "Current tax liabilities", {"FY2020": 4891, "FY2019": 675, "FY2018": 4908, "FY2017": 5447, "FY2016": 8680, "FY2015": 3520, "FY2014": 3873}),
    ("DATA", "Impairment provision on off balance sheet products", {"FY2025": 138, "FY2024": 58, "FY2023": 54, "FY2022": 51, "FY2021": 119, "FY2020": 310, "FY2019": 102, "FY2018": 97}),
    ("DATA", "Subordinated liabilities", {"FY2021": 60000, "FY2020": 60000, "FY2019": 60000, "FY2018": 60000, "FY2017": 60000, "FY2016": 60000, "FY2015": 60000, "FY2014": 60000}),
    ("TOTAL", "Total liabilities", {"FY2025": 1875428, "FY2024": 1909575, "FY2023": 1646084, "FY2022": 1888700, "FY2021": 1844404, "FY2020": 1598941, "FY2019": 1380330, "FY2018": 1304906, "FY2017": 1232167, "FY2016": 1239534, "FY2015": 971142, "FY2014": 913636}),
    ("SECTION", "Equity", {}),
    ("DATA", "Authorised and called up share capital", {"FY2025": 250000, "FY2024": 250000, "FY2023": 250000, "FY2022": 250000, "FY2021": 250000, "FY2020": 250000, "FY2019": 250000, "FY2018": 250000, "FY2017": 250000, "FY2016": 250000, "FY2015": 250000, "FY2014": 250000}),
    ("DATA", "Other equity instruments (Additional Tier 1)", {"FY2025": 60000, "FY2024": 60000, "FY2023": 60000, "FY2022": 60000}),
    ("DATA", "Retained earnings", {"FY2025": 89013, "FY2024": 103744, "FY2023": 123289, "FY2022": 91893, "FY2021": 56776, "FY2020": 92164, "FY2019": 57058, "FY2018": 76076, "FY2017": 57022, "FY2016": 60648, "FY2015": 70408, "FY2014": 50913}),
    ("DATA", "Available for sale reserve", {"FY2017": 32, "FY2016": -284, "FY2015": -140, "FY2014": 567}),
    ("TOTAL", "Total shareholders' equity", {"FY2025": 399013, "FY2024": 413744, "FY2023": 433289, "FY2022": 401893, "FY2021": 306776, "FY2020": 342164, "FY2019": 307058, "FY2018": 326076, "FY2017": 307054, "FY2016": 310364, "FY2015": 320268, "FY2014": 301480}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 2274441, "FY2024": 2323319, "FY2023": 2079373, "FY2022": 2290593, "FY2021": 2151180, "FY2020": 1941105, "FY2019": 1687388, "FY2018": 1630982, "FY2017": 1539221, "FY2016": 1549898, "FY2015": 1291410, "FY2014": 1215116}),
]

BALANCE_SHEET_SOURCES = (
    "Sources - Bank of China (UK) Limited's own Statement of Financial Position (Bank/solo basis - no group "
    "accounts prepared, Companies Act 2006 s.401 exemption), £'000, each year's own originally-published report:\n"
    f"FY2025: Annual Report 2025, p.49 - {AR2025_URL}\n"
    f"FY2024: Annual Report 2024, p.49 - {AR2024_URL} ({AR2024_OWN_NOTE})\n"
    f"FY2023: Annual Report 2023, p.50 - {AR2023_URL}\n"
    f"FY2022: Financial Statements 2022, p.38 - {AR2022_URL}\n"
    f"FY2021: Financial Statements 2021, p.35 - {AR2021_URL}\n"
    f"FY2020: Financial Statements 2020, p.33 - {AR2020_URL}\n"
    f"FY2019: Financial Statements 2019, p.32 - {AR2019_URL}\n"
    f"FY2018: Financial Statements 2018, p.27 - {AR2018_URL}\n"
    f"FY2017: Financial Statements 2017, p.25 - {AR2017_URL}\n"
    f"FY2016: Financial Statements 2016, p.20 - {AR2016_URL}\n"
    f"FY2015: Financial Statements 2015, p.19 - {AR2015_URL}\n"
    f"FY2014: Financial Statements 2015's own FY2014 comparative column, p.19 - {AR2015_URL} ({AR2014_SCAN_NOTE})\n"
    "Presentation notes: 'Government bonds' only appears as its own line from FY2022 onward. 'Subordinated "
    "liabilities' (£60,000k every year FY2014-FY2021) was repaid and replaced by an equal £60,000k Additional "
    "Tier 1 instrument in June 2022 - both nil/blank in the years they don't apply. 'Investment in subsidiary "
    "companies' is nil every year and omitted as a row. 'Available for sale financial investments' and its "
    "matching equity 'Available for sale reserve' existed under IAS 39 through FY2017 and were replaced by "
    "'Financial assets at fair value through profit and loss' / 'Debt instruments at amortised cost' at the "
    "1 January 2018 IFRS 9 transition (a £495k opening-equity charge that year, see the Statement of Changes "
    "in Equity sheet) - both pairs of rows are blank/zero in the years they don't apply, not force-matched. "
    "FY2021's own report's Statement of Changes in Equity states closing retained earnings as £56,706k, £70k "
    "less than the Balance Sheet's own £56,776k for the same date - the Balance Sheet's single 'Retained "
    "earnings' line appears to combine the SOCE's separate retained-earnings and FX-translation-reserve columns "
    "(£56,706k + £70k = £56,776k); the same pattern recurs one year earlier at FY2020 (SOCE retained earnings "
    "£92,228k + FX reserve -£64k = Balance Sheet's own £92,164k); total equity ties out exactly either way in "
    "both years. FY2014 cash: the Balance Sheet (via FY2015's comparative) shows £199,954k while the Cash Flow "
    "Statement's own closing balance for the same date shows £199,854k - a genuine £100k digit discrepancy "
    "between the two notes of the same FY2015 filing (likely one OCR-affected digit somewhere upstream of both "
    "extractions), left unresolved and shown as each note's own figure rather than force-matched, since FY2014's "
    "own primary report cannot be read to arbitrate (see AR2014_SCAN_NOTE).\n"
    + ENTITY_NOTE
)

bw.add_balance_sheet_sheet(
    title="Bank of China (UK) Limited — Statement of Financial Position",
    subtitle="Bank of China (UK) Limited (solo entity basis), £'000",
    rows=balance_sheet_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=68,
    source_height=200,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 110123, "FY2024": 128817, "FY2023": 121217, "FY2022": 62661, "FY2021": 36936, "FY2020": 40327, "FY2019": 45693, "FY2018": 40759, "FY2017": 38234, "FY2016": 34591, "FY2015": 25645, "FY2014": 26082}),
    ("DATA", "Interest expense", {"FY2025": -53024, "FY2024": -57415, "FY2023": -40422, "FY2022": -13239, "FY2021": -3650, "FY2020": -6276, "FY2019": -9313, "FY2018": -6553, "FY2017": -5788, "FY2016": -4629, "FY2015": -3095, "FY2014": -3635}),
    ("TOTAL", "Net interest income", {"FY2025": 57099, "FY2024": 71402, "FY2023": 80795, "FY2022": 49422, "FY2021": 33286, "FY2020": 34051, "FY2019": 36380, "FY2018": 34206, "FY2017": 32446, "FY2016": 29962, "FY2015": 22550, "FY2014": 22447}),
    ("DATA", "Fee and commission income", {"FY2025": 3399, "FY2024": 3228, "FY2023": 3378, "FY2022": 3955, "FY2021": 4294, "FY2020": 3627, "FY2019": 4674, "FY2018": 4850, "FY2017": 5502, "FY2016": 4029, "FY2015": 8906, "FY2014": 7109}),
    ("DATA", "Fee and commission expense", {"FY2025": -1462, "FY2024": -1481, "FY2023": -1692, "FY2022": -1694, "FY2021": -1319, "FY2020": -1549, "FY2019": -1170, "FY2018": -886, "FY2017": -813, "FY2016": -776, "FY2015": -582, "FY2014": -1022}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 1937, "FY2024": 1747, "FY2023": 1686, "FY2022": 2261, "FY2021": 2975, "FY2020": 2078, "FY2019": 3504, "FY2018": 3964, "FY2017": 4689, "FY2016": 3253, "FY2015": 8324, "FY2014": 6087}),
    ("DATA", "Net fair value gain/(loss) on financial instruments", {"FY2025": 3431, "FY2024": 4711, "FY2023": 9119, "FY2022": 148, "FY2021": 1923, "FY2020": -3151, "FY2019": -1165, "FY2018": -331, "FY2017": 51, "FY2016": 241, "FY2015": 511, "FY2014": -1413}),
    ("DATA", "Foreign exchange gain", {"FY2025": 2388, "FY2024": 2295, "FY2023": 386, "FY2022": 4916, "FY2021": 2590, "FY2020": 1489, "FY2019": 4767, "FY2018": 3167, "FY2017": 2593, "FY2016": 2827, "FY2015": 2492, "FY2014": 2100}),
    ("DATA", "Net other operating income", {"FY2025": 123435, "FY2024": 107108, "FY2023": 114199, "FY2022": 93633, "FY2021": 83274, "FY2020": 85636, "FY2019": 71751, "FY2018": 73555, "FY2017": 54704, "FY2016": 54899, "FY2015": 61054, "FY2014": 42403}),
    ("DATA", "Loss on sale of debt securities", {"FY2014": -3}),
    ("TOTAL", "Non-interest income", {"FY2025": 129254, "FY2024": 114114, "FY2023": 123704, "FY2022": 98697, "FY2021": 87787, "FY2020": 83974, "FY2019": 75353, "FY2018": 76391, "FY2017": 57348, "FY2016": 57967, "FY2015": 64047, "FY2014": 43087}),
    ("TOTAL", "Total income", {"FY2025": 188290, "FY2024": 187263, "FY2023": 206185, "FY2022": 150380, "FY2021": 124048, "FY2020": 120103, "FY2019": 115237, "FY2018": 114561, "FY2017": 94483, "FY2016": 91182, "FY2015": 94921, "FY2014": 71621}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Staff costs", {"FY2025": -86079, "FY2024": -72194, "FY2023": -68058, "FY2022": -59208, "FY2021": -50154, "FY2020": -47607, "FY2019": -47279, "FY2018": -41868, "FY2017": -41365, "FY2016": -32821, "FY2015": -29500, "FY2014": -30178}),
    ("DATA", "Other expenses", {"FY2025": -10029, "FY2024": -9735, "FY2023": -9543, "FY2022": -9818, "FY2021": -8924, "FY2020": -18816, "FY2019": -23048, "FY2018": -7857, "FY2017": -7870, "FY2016": -6914, "FY2015": -6544, "FY2014": -6402}),
    ("DATA", "Depreciation of plant and equipment", {"FY2025": -1870, "FY2024": -1540, "FY2023": -1572, "FY2022": -1462, "FY2021": -1802, "FY2020": -2342, "FY2019": -2498, "FY2018": -691, "FY2017": -794, "FY2016": -918, "FY2015": -965, "FY2014": -859}),
    ("DATA", "Amortisation of intangible assets", {"FY2025": -161, "FY2024": -104, "FY2023": -52, "FY2022": -271, "FY2021": -237, "FY2020": -256, "FY2019": -100, "FY2018": -53, "FY2017": -45, "FY2016": -144, "FY2015": -146, "FY2014": -129}),
    ("DATA", "Credit/(provision) for expected credit losses", {"FY2025": 217, "FY2024": 3953, "FY2023": 11235, "FY2022": 11526, "FY2021": -23665, "FY2020": -3172, "FY2019": -377, "FY2018": 458, "FY2017": 187, "FY2016": -527, "FY2015": 155, "FY2014": -722}),
    ("DATA", "Loss on disposal of subsidiary", {"FY2015": -1707}),
    ("TOTAL", "Profit before income tax", {"FY2025": 90368, "FY2024": 107643, "FY2023": 138195, "FY2022": 91147, "FY2021": 39266, "FY2020": 47910, "FY2019": 41935, "FY2018": 64550, "FY2017": 44596, "FY2016": 49858, "FY2015": 56214, "FY2014": 33331}),
    ("DATA", "Income tax expense", {"FY2025": -21437, "FY2024": -23726, "FY2023": -34982, "FY2022": -22583, "FY2021": -7788, "FY2020": -12745, "FY2019": -9830, "FY2018": -13427, "FY2017": -12532, "FY2016": -14168, "FY2015": -10764, "FY2014": -7376}),
    ("TOTAL", "Profit for the year", {"FY2025": 68931, "FY2024": 83917, "FY2023": 103213, "FY2022": 68564, "FY2021": 31478, "FY2020": 35165, "FY2019": 32105, "FY2018": 51123, "FY2017": 32064, "FY2016": 35690, "FY2015": 45450, "FY2014": 25955}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Foreign currency translation", {"FY2025": 80, "FY2023": -2, "FY2022": 12, "FY2021": 134, "FY2020": -59}),
    ("DATA", "Net change in fair value of available-for-sale financial assets (net of tax)", {"FY2017": 316, "FY2016": -144, "FY2015": -707, "FY2014": -276}),
    ("TOTAL", "Other comprehensive income/(expense) for the year", {"FY2025": 80, "FY2024": 0, "FY2023": -2, "FY2022": 12, "FY2021": 134, "FY2020": -59, "FY2019": 0, "FY2018": 0, "FY2017": 316, "FY2016": -144, "FY2015": -707, "FY2014": -276}),
    ("TOTAL", "Total comprehensive income for the year", {"FY2025": 69011, "FY2024": 83917, "FY2023": 103211, "FY2022": 68576, "FY2021": 31612, "FY2020": 35106, "FY2019": 32105, "FY2018": 51123, "FY2017": 32380, "FY2016": 35546, "FY2015": 44743, "FY2014": 25679}),
]

INCOME_STATEMENT_SOURCES = (
    "Sources - Bank of China (UK) Limited's own Income Statement / Statement of Comprehensive Income (Bank/solo "
    "basis), £'000, each year's own originally-published report:\n"
    f"FY2025: Annual Report 2025, p.47-48 - {AR2025_URL}\n"
    f"FY2024: Annual Report 2024, p.48-49 - {AR2024_URL} ({AR2024_OWN_NOTE})\n"
    f"FY2023: Annual Report 2023, p.48-49 - {AR2023_URL}\n"
    f"FY2022: Financial Statements 2022, p.36-37 - {AR2022_URL}\n"
    f"FY2021: Financial Statements 2021, p.33-34 - {AR2021_URL}\n"
    f"FY2020: Financial Statements 2020, p.31-32 - {AR2020_URL}\n"
    f"FY2019: Financial Statements 2019, p.30-31 - {AR2019_URL}\n"
    f"FY2018: Financial Statements 2018, p.24-26 - {AR2018_URL}\n"
    f"FY2017: Financial Statements 2017, p.23-24 - {AR2017_URL}\n"
    f"FY2016: Financial Statements 2016, p.18-19 - {AR2016_URL}\n"
    f"FY2015: Financial Statements 2015, p.16-18 - {AR2015_URL}\n"
    f"FY2014: Financial Statements 2015's own FY2014 comparative column, p.16-18 - {AR2015_URL} ({AR2014_SCAN_NOTE})\n"
    "Profit before income tax ties exactly to the Cash Flow Statement's own 'Profit before income tax' row for "
    "every year, cross-checked as a reconciliation. Presentation notes: FY2014's Income Statement splits "
    "'Interest income' into 'Interest income from financial investments' + 'Other interest income' sub-lines "
    "through FY2020 (summed into the single 'Interest income' row here to match FY2021 onward's presentation - "
    "e.g. FY2014's £654k + £25,428k = £26,082k). FY2014's own P&L shows a one-off £3k 'Loss on sale of debt "
    "securities' (its own row here, income section); FY2015's own P&L shows a separate one-off £1,707k 'Loss on "
    "disposal of subsidiary' (its own row here, expenses section, immediately before Profit before income tax) - "
    "neither recurs in any other year. Other comprehensive income was governed by IAS 39's 'available for sale "
    "financial assets' fair-value reserve through FY2017 (its own row here) before the 1 January 2018 IFRS 9 "
    "transition removed the AFS category entirely (FY2018/FY2019 OCI is genuinely nil); the 'Foreign currency "
    "translation' OCI item used FY2021 onward first appears at FY2020 (a different, unrelated OCI component, not "
    "a renamed AFS reserve) - both rows are blank in the years the other applies, not force-matched.\n"
    + ENTITY_NOTE
)

bw.add_income_statement_sheet(
    title="Bank of China (UK) Limited — Income Statement and Statement of Comprehensive Income",
    subtitle="Bank of China (UK) Limited (solo entity basis), £'000",
    rows=income_statement_rows,
    sources_text=INCOME_STATEMENT_SOURCES,
    first_col_width=68,
    source_height=180,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Issued share capital", "Other equity instruments", "Retained earnings", "Available for sale reserve", "Foreign currency translation reserve", "Total"]

equity_changes_rows = [
    ("DATA", "As at 1 January 2014", (250000, 0, 56831, 843, None, 307674)),
    ("DATA", "Unrealised loss on available for sale investments, net of tax", (0, 0, 0, -276, None, -276)),
    ("DATA", "Profit for the financial year", (0, 0, 25955, 0, None, 25955)),
    ("TOTAL", "Total comprehensive income", (0, 0, 25955, -276, None, 25679)),
    ("DATA", "Dividend paid", (0, 0, -31873, 0, None, -31873)),
    ("TOTAL", "As at 31 December 2014", (250000, 0, 50913, 567, None, 301480)),
    ("DATA", "Unrealised loss on available for sale investments, net of tax", (0, 0, 0, -707, None, -707)),
    ("DATA", "Profit for the financial year", (0, 0, 45450, 0, None, 45450)),
    ("TOTAL", "Total comprehensive income", (0, 0, 45450, -707, None, 44743)),
    ("DATA", "Dividend paid", (0, 0, -25955, 0, None, -25955)),
    ("TOTAL", "As at 31 December 2015", (250000, 0, 70408, -140, None, 320268)),
    ("DATA", "Unrealised loss on available for sale investments, net of tax", (0, 0, 0, -144, None, -144)),
    ("DATA", "Profit for the financial year", (0, 0, 35690, 0, None, 35690)),
    ("TOTAL", "Total comprehensive income", (0, 0, 35690, -144, None, 35546)),
    ("DATA", "Dividend paid", (0, 0, -45450, 0, None, -45450)),
    ("TOTAL", "As at 31 December 2016", (250000, 0, 60648, -284, None, 310364)),
    ("DATA", "Unrealised gain on available for sale investments, net of tax", (0, 0, 0, 316, None, 316)),
    ("DATA", "Profit for the financial year", (0, 0, 32064, 0, None, 32064)),
    ("TOTAL", "Total comprehensive income", (0, 0, 32064, 316, None, 32380)),
    ("DATA", "Dividend paid", (0, 0, -35690, 0, None, -35690)),
    ("TOTAL", "As at 31 December 2017", (250000, 0, 57022, 32, None, 307054)),
    ("DATA", "Impact of adopting IFRS 9 (1 January 2018)", (0, 0, -463, -32, None, -495)),
    ("TOTAL", "Restated opening balance under IFRS 9", (250000, 0, 56559, 0, None, 306559)),
    ("DATA", "Profit for the financial year", (0, 0, 51123, None, None, 51123)),
    ("TOTAL", "Total comprehensive income", (0, 0, 51123, None, None, 51123)),
    ("DATA", "Dividend paid", (0, 0, -31606, None, None, -31606)),
    ("TOTAL", "As at 31 December 2018", (250000, 0, 76076, None, None, 326076)),
    ("DATA", "Profit for the financial year", (0, 0, 32105, None, None, 32105)),
    ("TOTAL", "Total comprehensive income", (0, 0, 32105, None, None, 32105)),
    ("DATA", "Foreign exchange and other", (0, 0, -5, None, None, -5)),
    ("DATA", "Dividend paid", (0, 0, -51118, None, None, -51118)),
    ("TOTAL", "As at 31 December 2019", (250000, 0, 57058, None, None, 307058)),
    ("DATA", "FY2020 report's re-split of the FY2019 closing balance (retained earnings/FX reserve)", (0, 0, 5, None, -5, 0)),
    ("DATA", "Profit for the financial year", (0, 0, 35165, None, 0, 35165)),
    ("DATA", "Foreign exchange and other", (0, 0, 0, None, -59, -59)),
    ("TOTAL", "Total comprehensive income", (0, 0, 35165, None, -59, 35106)),
    ("TOTAL", "As at 31 December 2020", (250000, 0, 92228, None, -64, 342164)),
    ("DATA", "Profit for the financial year", (0, 0, 31478, None, 0, 31478)),
    ("DATA", "Foreign exchange and other", (0, 0, 0, None, 134, 134)),
    ("TOTAL", "Total comprehensive income", (0, 0, 31478, None, 134, 31612)),
    ("DATA", "Dividend paid", (0, 0, -67000, None, 0, -67000)),
    ("TOTAL", "As at 31 December 2021", (250000, 0, 56706, None, 70, 306776)),
    ("DATA", "Additional Tier 1 capital issued", (0, 60000, 0, None, 0, 60000)),
    ("DATA", "Profit for the financial year", (0, 0, 68564, None, 0, 68564)),
    ("DATA", "Foreign exchange and other", (0, 0, 0, None, 12, 12)),
    ("TOTAL", "Total comprehensive income", (0, 0, 68564, None, 12, 68576)),
    ("DATA", "Dividend paid", (0, 0, -33459, None, 0, -33459)),
    ("TOTAL", "As at 31 December 2022", (250000, 60000, 91811, None, 82, 401893)),
    ("DATA", "Profit for the financial year", (0, 0, 103213, None, 0, 103213)),
    ("DATA", "Foreign exchange and other", (0, 0, 0, None, -2, -2)),
    ("TOTAL", "Total comprehensive income", (0, 0, 103213, None, -2, 103211)),
    ("DATA", "Dividend paid", (0, 0, -71815, None, 0, -71815)),
    ("TOTAL", "As at 31 December 2023", (250000, 60000, 123209, None, 80, 433289)),
    ("DATA", "Profit for the financial year", (0, 0, 83917, None, 0, 83917)),
    ("TOTAL", "Total comprehensive income", (0, 0, 83917, None, 0, 83917)),
    ("DATA", "Dividend paid", (0, 0, -103462, None, 0, -103462)),
    ("TOTAL", "As at 31 December 2024", (250000, 60000, 103664, None, 80, 413744)),
    ("DATA", "Profit for the financial year", (0, 0, 68931, None, 0, 68931)),
    ("DATA", "Transfer", (0, 0, 80, None, -80, 0)),
    ("TOTAL", "Total comprehensive income", (0, 0, 69011, None, 0, 69011)),
    ("DATA", "Dividend paid", (0, 0, -83662, None, 0, -83662)),
    ("TOTAL", "As at 31 December 2025", (250000, 60000, 89013, None, 0, 399013)),
]

EQUITY_CHANGES_SOURCES = (
    "Sources - Bank of China (UK) Limited's own Statement of Changes in Equity (Bank/solo basis), £'000, "
    "chronological roll-forward reconstructed from each year's own originally-published report:\n"
    f"2014 movements: Financial Statements 2015's own FY2014 comparative, p.17 - {AR2015_URL} ({AR2014_SCAN_NOTE})\n"
    f"2015 movements: Financial Statements 2015, p.17 - {AR2015_URL}\n"
    f"2016 movements: Financial Statements 2016, p.20 - {AR2016_URL}\n"
    f"2017 movements: Financial Statements 2017, p.25 - {AR2017_URL}\n"
    f"2018 movements: Financial Statements 2018, p.27 - {AR2018_URL}\n"
    f"2019 movements: Financial Statements 2019, p.32 - {AR2019_URL}\n"
    f"2020 movements: Financial Statements 2020, p.33 - {AR2020_URL}\n"
    f"2021 movements: Financial Statements 2021, p.36 - {AR2021_URL}\n"
    f"2022 movements: Financial Statements 2022, p.39 - {AR2022_URL}\n"
    f"2023 movements: Annual Report 2023, p.51 - {AR2023_URL}\n"
    f"2024 movements: Annual Report 2024, p.50 - {AR2024_URL} ({AR2024_OWN_NOTE})\n"
    f"2025 movements: Annual Report 2025, p.50 - {AR2025_URL}\n"
    "Note: the 'Dividend paid' row in this statement (which includes both ordinary share dividends and Additional "
    "Tier 1 coupon/interest payments to the parent) differs from the Cash Flow Statement's separately-split "
    "'Dividend paid'/'Interest paid on Additional Tier 1 instrument' lines - e.g. FY2025's £83,662k here vs "
    "£78,700k + £4,962k = £83,662k on the Cash Flow Statement (ties out exactly once combined; genuinely two "
    "different presentations of the same total, not a discrepancy). "
    "The 'Available for sale reserve' column applied under IAS 39 through the FY2018 IFRS 9 transition (a "
    "£495k opening-equity charge, split £463k retained earnings / £32k AFS reserve per the Bank's own FY2018 and "
    "FY2019 reports); the 'Foreign currency translation reserve' column is a separate, later, unrelated OCI "
    "component that first appears at FY2020 - both are blank in the years the other applies, not force-matched, "
    "and there is a genuine one-year gap (FY2019) where neither column is populated (OCI was nil that year). A "
    "restatement-split quirk is flagged rather than silently resolved: the FY2019 closing balance is shown twice "
    "with a different retained-earnings/FX-reserve split - £57,058k/blank per FY2019's own report (its own "
    "presentation had no separate FX column yet) as 'As at 31 December 2019', and £57,063k/-£5k per FY2020's own "
    "report's FY2019 opening comparative (which introduced the new column and re-split the same £57,058k total); "
    "the FY2020 movement rows that follow use this second, FY2020-report split as their starting point. The "
    "FY2021 opening balance is likewise stated directly from FY2021's own report rather than carried forward "
    "arithmetically, and ties out exactly to the FY2020 closing row above it.\n"
    + ENTITY_NOTE
)

bw.add_equity_changes_sheet(
    title="Bank of China (UK) Limited — Statement of Changes in Equity",
    subtitle="Bank of China (UK) Limited (solo entity basis), £'000, chronological",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQUITY_CHANGES_SOURCES,
    first_col_width=42,
    source_height=190,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit before income tax", {"FY2025": 90368, "FY2024": 107644, "FY2023": 138195, "FY2022": 91147, "FY2021": 39266, "FY2020": 47910, "FY2019": 41935, "FY2018": 64550, "FY2017": 44596, "FY2016": 49858, "FY2015": 56214, "FY2014": 33331}),
    ("DATA", "Depreciation and amortisation of plant and equipment and intangible assets", {"FY2025": 2031, "FY2024": 1644, "FY2023": 1624, "FY2022": 1733, "FY2021": 2039, "FY2020": 2601, "FY2019": 2599, "FY2018": 744, "FY2017": 839, "FY2016": 1062, "FY2015": 1111, "FY2014": 988}),
    ("DATA", "Net (credit)/loss for expected credit losses", {"FY2025": -297, "FY2024": -3958, "FY2023": -11237, "FY2022": -11526, "FY2021": 23665, "FY2020": 3172, "FY2019": 377, "FY2018": -458, "FY2017": -187, "FY2016": 527, "FY2015": -155, "FY2014": 722}),
    ("DATA", "Interest receivable from financial investments", {"FY2020": 13, "FY2019": 93, "FY2018": 0, "FY2017": -692, "FY2016": -1216, "FY2015": -1134, "FY2014": -654}),
    ("DATA", "Other interest receivable (from loans and advances)", {"FY2020": -40326, "FY2019": -46357, "FY2018": -41792, "FY2017": -38599, "FY2016": -33375, "FY2015": -24511, "FY2014": -25428}),
    ("DATA", "Interest payable (non-cash addback)", {"FY2019": 9313, "FY2018": 6553, "FY2017": 5788, "FY2016": 4629, "FY2015": 3095, "FY2014": 3635}),
    ("DATA", "(Gain)/loss on disposal of fixed assets", {"FY2018": -1, "FY2017": 1, "FY2014": 3}),
    ("DATA", "Net loss on sale of available-for-sale investments / debt securities", {"FY2017": 45, "FY2014": 3}),
    ("DATA", "Amortisation of premiums on debt instruments at amortised cost / held-to-maturity investments", {"FY2018": 116, "FY2017": 96}),
    ("DATA", "Other income receivable", {"FY2017": -504}),
    ("DATA", "Fee income receivable", {"FY2020": 283}),
    ("DATA", "Exchange rate movements on plant and equipment", {"FY2021": -1, "FY2020": -79}),
    ("DATA", "Exchange rate movements on equity", {"FY2023": -1, "FY2022": 12, "FY2021": 135, "FY2020": -59}),
    ("DATA", "Exchange-rate movements on available-for-sale investments", {"FY2016": -4958, "FY2015": 704, "FY2014": 1721}),
    ("DATA", "Net fair value (gain)/loss on financial instruments", {"FY2025": -1895, "FY2024": -1310, "FY2023": -7446, "FY2022": 10358, "FY2021": 2656}),
    ("SECTION", "Changes in operating assets and liabilities", {}),
    ("DATA", "Change in derivative financial instruments assets", {"FY2025": 2163, "FY2024": 839, "FY2023": 2196, "FY2022": -7691, "FY2021": -8, "FY2020": -43549, "FY2019": -3270, "FY2018": 372, "FY2017": 2860, "FY2016": 3596, "FY2015": 8000, "FY2014": 25329}),
    ("DATA", "Change in loans and advances to banks", {"FY2022": 39708, "FY2021": 41381, "FY2020": -25199, "FY2019": -23856, "FY2018": 22315, "FY2017": -59436, "FY2016": 37836, "FY2015": 144643, "FY2014": -38459}),
    ("DATA", "Change in loans and advances to customers", {"FY2025": 130992, "FY2024": 53197, "FY2023": 142977, "FY2022": 83721, "FY2021": -79736, "FY2020": -77438, "FY2019": -20154, "FY2018": -31910, "FY2017": 105429, "FY2016": -348920, "FY2015": -88564, "FY2014": -141927}),
    ("DATA", "Change in financial assets at amortised cost/fair value", {"FY2025": -39251, "FY2024": 16787, "FY2023": 20515, "FY2022": -6213, "FY2021": 10167, "FY2020": 6877, "FY2019": -4241, "FY2018": -30262}),
    ("DATA", "Change in financial assets at amortised cost - Government bonds", {"FY2025": 2147}),
    ("DATA", "Change in other assets", {"FY2025": -18315, "FY2024": -7665, "FY2023": 221384, "FY2022": -264099, "FY2021": -9099, "FY2020": -20489, "FY2019": -57250, "FY2018": 2055, "FY2017": 574, "FY2016": 20998, "FY2015": 1918, "FY2014": 38117}),
    ("DATA", "Change in derivative financial instruments liabilities", {"FY2025": 287, "FY2024": 1, "FY2023": -10, "FY2022": -5267, "FY2021": -3484, "FY2020": 48153, "FY2019": 6794, "FY2018": 1720, "FY2017": -3893, "FY2016": -7355, "FY2015": -9984, "FY2014": -21016}),
    ("DATA", "Change in deposits from banks", {"FY2025": 18705, "FY2024": 123666, "FY2023": -169797, "FY2022": 143133, "FY2021": 176876, "FY2020": 90788, "FY2019": 25671, "FY2018": -20203, "FY2017": -41727, "FY2016": 28113, "FY2015": 96466, "FY2014": -31862}),
    ("DATA", "Change in deposits from customers", {"FY2025": -50713, "FY2024": 132461, "FY2023": -68081, "FY2022": -42374, "FY2021": 117876, "FY2020": 83454, "FY2019": 24754, "FY2018": 88432, "FY2017": 36646, "FY2016": 244637, "FY2015": -28175, "FY2014": 228200}),
    ("DATA", "Change in other liabilities and provisions", {"FY2025": -2001, "FY2024": 7855, "FY2023": -4681, "FY2022": 8883, "FY2021": 1456, "FY2020": -6246, "FY2019": 22251, "FY2018": -793, "FY2017": 6672, "FY2016": -3584, "FY2015": -466, "FY2014": -5499}),
    ("DATA", "Interest and coupon received (operating, FY2014-FY2020 presentation)", {"FY2020": 40314, "FY2019": 45600, "FY2018": 40643, "FY2017": 37848, "FY2016": 34582, "FY2015": 25736, "FY2014": 28126}),
    ("DATA", "Dividend paid (operating activities, FY2014-FY2020 presentation)", {"FY2020": 0, "FY2019": -51118, "FY2018": -31606, "FY2017": -35690, "FY2016": -45450, "FY2015": -25955, "FY2014": -31873}),
    ("DATA", "Interest paid (operating activities, FY2014-FY2020 presentation)", {"FY2020": -7121, "FY2019": -9313, "FY2018": -4522, "FY2017": -7487, "FY2016": -4527, "FY2015": -2994, "FY2014": -3895}),
    ("DATA", "Income taxes paid", {"FY2025": -22969, "FY2024": -26070, "FY2023": -32346, "FY2022": -18955, "FY2021": -18895, "FY2020": -8430, "FY2019": -13293, "FY2018": -13859, "FY2017": -16749, "FY2016": -7780, "FY2015": -10695, "FY2014": -6670}),
    ("TOTAL", "Net cash generated from operating activities", {"FY2025": 111252, "FY2024": 405091, "FY2023": 233292, "FY2022": 22570, "FY2021": 304294, "FY2020": 100905, "FY2019": -49465, "FY2018": 52094, "FY2017": 36430, "FY2016": -31327, "FY2015": 145254, "FY2014": 52892}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Acquisition of government bonds", {"FY2025": -78477, "FY2024": -36107, "FY2023": -74108, "FY2022": -44264}),
    ("DATA", "Proceeds from government bonds", {"FY2025": 78289, "FY2024": 11775}),
    ("DATA", "Acquisition of investment securities", {"FY2017": -106425, "FY2016": -8, "FY2014": -26932}),
    ("DATA", "Proceeds from sale of investment securities", {"FY2014": 15590}),
    ("DATA", "Proceeds from maturity of investment securities", {"FY2020": 50000, "FY2019": 50000, "FY2017": 40708}),
    ("DATA", "Acquisition of property, plant and equipment", {"FY2025": -2120, "FY2024": -1086, "FY2023": -745, "FY2022": -3086, "FY2021": -1349, "FY2020": -519, "FY2019": -870, "FY2018": -318, "FY2017": -668, "FY2016": -681, "FY2015": -1089, "FY2014": -489}),
    ("DATA", "Acquisition of intangible assets", {"FY2025": -412, "FY2024": -435, "FY2023": -83, "FY2022": -183, "FY2021": -86, "FY2020": -52, "FY2019": -398, "FY2018": -419, "FY2017": -18, "FY2016": -86, "FY2014": -426}),
    ("DATA", "Proceeds from disposal of property, plant and equipment", {"FY2025": 97, "FY2024": 27, "FY2023": 40, "FY2022": 22, "FY2021": 272, "FY2020": 82}),
    ("DATA", "Proceeds from disposal of intangible assets", {"FY2021": 16}),
    ("TOTAL", "Net cash from/(used in) investing activities", {"FY2025": -2623, "FY2024": -25826, "FY2023": -74896, "FY2022": -47511, "FY2021": -1147, "FY2020": 49511, "FY2019": 48732, "FY2018": -737, "FY2017": -66403, "FY2016": -775, "FY2015": -1089, "FY2014": -12257}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Repayment of subordinated debt", {"FY2022": -60000}),
    ("DATA", "Issuance of Additional Tier 1 instrument", {"FY2022": 60000}),
    ("DATA", "Dividend paid", {"FY2025": -78700, "FY2024": -98100, "FY2023": -66800, "FY2022": -33459, "FY2021": -67000}),
    ("DATA", "Interest paid on Additional Tier 1 instrument", {"FY2025": -4962, "FY2024": -5362, "FY2023": -5015}),
    ("DATA", "Repayment of principal portion of lease liabilities", {"FY2025": -722, "FY2024": -491, "FY2023": -47, "FY2022": -77, "FY2021": -1393, "FY2020": -1578}),
    ("DATA", "Repayment of interest portion of lease liabilities", {"FY2025": 298}),
    ("TOTAL", "Net cash used in financing activities", {"FY2025": -84086, "FY2024": -103953, "FY2023": -71862, "FY2022": -33536, "FY2021": -68393, "FY2020": -1578, "FY2019": 0, "FY2018": 0, "FY2017": 0, "FY2016": 0, "FY2015": 0, "FY2014": 0}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 24543, "FY2024": 275312, "FY2023": 86534, "FY2022": -58477, "FY2021": 234754, "FY2020": 148837, "FY2019": -733, "FY2018": 51357, "FY2017": -29973, "FY2016": -32102, "FY2015": 144165, "FY2014": 40635}),
    ("DATA", "Current/prior year reclassification adjustments", {"FY2018": -26}),
    ("DATA", "Cash and cash equivalents at beginning of period", {"FY2025": 1048859, "FY2024": 773547, "FY2023": 687013, "FY2022": 716133, "FY2021": 481379, "FY2020": 332542, "FY2019": 333275, "FY2018": 281944, "FY2017": 311917, "FY2016": 344019, "FY2015": 199854, "FY2014": 159219}),
    ("TOTAL", "Cash and cash equivalents at end of period", {"FY2025": 1073402, "FY2024": 1048859, "FY2023": 773547, "FY2022": 657656, "FY2021": 716133, "FY2020": 481379, "FY2019": 332542, "FY2018": 333275, "FY2017": 281944, "FY2016": 311917, "FY2015": 344019, "FY2014": 199854}),
]

bw.add_cash_flow_sheet(
    title="Bank of China (UK) Limited — Statement of Cash Flows",
    subtitle="Bank of China (UK) Limited (solo entity basis), £'000",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=72,
    source_height=210,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Gross carrying amount by product", {}),
    ("DATA", "Wholesale loans", {"FY2025": 2162, "FY2024": 2242, "FY2023": 2352, "FY2022": 2535, "FY2021": 4806, "FY2020": 4987, "FY2019": 2629, "FY2018": 5222}),
    ("DATA", "Housing loans", {"FY2025": 895, "FY2024": 1117, "FY2023": 2279, "FY2022": 2417, "FY2021": 2607, "FY2020": 3398, "FY2019": 4519, "FY2018": 5894}),
    ("DATA", "Syndicated loans", {"FY2025": 194775, "FY2024": 238983, "FY2023": 173584, "FY2022": 155931, "FY2021": 183604, "FY2020": 215270, "FY2019": 229152, "FY2018": 263321}),
    ("DATA", "Factoring financing", {"FY2025": 1898, "FY2024": 2185, "FY2023": 4840, "FY2022": 4219, "FY2021": 7892, "FY2020": 4097, "FY2019": 686, "FY2018": 1043}),
    ("DATA", "Overdraft corporate accounts", {"FY2020": 1, "FY2019": 1, "FY2018": 258}),
    ("DATA", "Overdraft personal accounts", {"FY2019": 2, "FY2018": 2}),
    ("DATA", "Credit cards", {"FY2025": 343, "FY2024": 382, "FY2023": 501, "FY2022": 401, "FY2021": 449, "FY2020": 460, "FY2019": 778, "FY2018": 784}),
    ("DATA", "Mortgage loans", {"FY2025": 611782, "FY2024": 697619, "FY2023": 812348, "FY2022": 973424, "FY2021": 1035418, "FY2020": 913853, "FY2019": 827596, "FY2018": 767860}),
    ("DATA", "Financing order", {"FY2024": 319, "FY2023": 140, "FY2022": 92, "FY2021": 1960, "FY2020": 655, "FY2019": 93, "FY2018": 1009}),
    ("TOTAL", "Total gross carrying amount", {"FY2025": 811855, "FY2024": 942847, "FY2023": 996044, "FY2022": 1139019, "FY2021": 1236736, "FY2020": 1142721, "FY2019": 1065456, "FY2018": 1045393}),
    ("SECTION", "Gross carrying amount by IFRS 9 stage", {}),
    ("DATA", "Stage 1: 12-month ECL", {"FY2025": 755256, "FY2024": 838850, "FY2023": 875144, "FY2022": 932381, "FY2021": 1161138, "FY2020": 1502398, "FY2019": 1429872, "FY2018": 1136718}),
    ("DATA", "Stage 2: Lifetime ECL, not credit-impaired", {"FY2025": 52230, "FY2024": 99518, "FY2023": 117365, "FY2022": 133805, "FY2021": 23529, "FY2020": 143650, "FY2019": 22324, "FY2018": 29296}),
    ("DATA", "Stage 3: Lifetime ECL, credit-impaired", {"FY2025": 4369, "FY2024": 4479, "FY2023": 3535, "FY2022": 72833, "FY2021": 52069, "FY2020": 3939, "FY2019": 1776, "FY2018": 686}),
    ("TOTAL", "Total gross carrying amount (by stage)", {"FY2025": 811855, "FY2024": 942847, "FY2023": 996044, "FY2022": 1139019, "FY2021": 1236736, "FY2020": 1649987, "FY2019": 1453972, "FY2018": 1166700}),
    ("SECTION", "Reconciliation to Balance Sheet", {}),
    ("DATA", "Net carrying value (Balance Sheet's Loans and advances to customers)", {"FY2025": 810985, "FY2024": 941507, "FY2023": 990763, "FY2022": 1122459, "FY2021": 1194653, "FY2020": 1138583, "FY2019": 1064347, "FY2018": 1044570}),
    ("DATA", "Implied total ECL allowance (gross − net)", {"FY2025": 870, "FY2024": 1340, "FY2023": 5281, "FY2022": 16560, "FY2021": 42083, "FY2020": 4138, "FY2019": 1109, "FY2018": 823}),
    ("SECTION", "Asset quality ratios", {}),
    ("DATA", "ECL coverage ratio (implied allowance / gross carrying amount)", {"FY2025": "0.11%", "FY2024": "0.14%", "FY2023": "0.53%", "FY2022": "1.45%", "FY2021": "3.40%", "FY2020": "0.36%", "FY2019": "0.10%", "FY2018": "0.08%"}),
    ("DATA", "Stage 3 / NPL ratio (Stage 3 gross / total gross carrying amount)", {"FY2025": "0.54%", "FY2024": "0.48%", "FY2023": "0.35%", "FY2022": "6.39%", "FY2021": "4.21%", "FY2020": "0.24%", "FY2019": "0.12%", "FY2018": "0.06%"}),
    ("SECTION", "Loans and advances to customers - credit quality (IAS 39, pre-IFRS 9, FY2014-FY2017)", {}),
    ("DATA", "Gross exposure", {"FY2017": 1055142, "FY2016": 1160589, "FY2015": 811185, "FY2014": 722717}),
    ("DATA", "Allowance for impairment", {"FY2017": -688, "FY2016": -893, "FY2015": -409, "FY2014": -410}),
    ("TOTAL", "Carrying amount", {"FY2017": 1054454, "FY2016": 1159696, "FY2015": 810776, "FY2014": 722307}),
    ("DATA", "Individually impaired (gross)", {"FY2017": 1, "FY2016": 3, "FY2015": 33, "FY2014": 5}),
    ("DATA", "Neither past due nor impaired", {"FY2017": 1041377, "FY2016": 1147306, "FY2015": 800575, "FY2014": 710358}),
    ("DATA", "Past due but not impaired", {"FY2017": 13077, "FY2016": 12390, "FY2015": 10201, "FY2014": 11949}),
    ("SECTION", "Credit quality categories (IAS 39, pre-IFRS 9, FY2014-FY2017)", {}),
    ("DATA", "Performing", {"FY2017": 1013454, "FY2016": 1110954}),
    ("DATA", "Special mention (unrated)", {"FY2017": 40645, "FY2016": 46426, "FY2015": 26740, "FY2014": 17106}),
    ("DATA", "Substandard (unrated)", {"FY2016": 2209, "FY2014": 740}),
    ("DATA", "Loss (unrated)", {"FY2016": 108}),
    ("SECTION", "Asset quality ratios (IAS 39 basis, FY2014-FY2017)", {}),
    ("DATA", "Individually impaired ratio (individually impaired / gross exposure)", {"FY2017": "0.00%", "FY2016": "0.00%", "FY2015": "0.00%", "FY2014": "0.00%"}),
    ("DATA", "Special mention ratio (special mention / gross exposure)", {"FY2017": "3.85%", "FY2016": "4.00%", "FY2015": "3.30%", "FY2014": "2.37%"}),
]

ASSET_QUALITY_SOURCES = (
    "Sources - Note 6(a) 'Analysis of risk concentration in the financial position' (Global/Europe/US/UK/UK "
    "Retail x Stage 1/2/3 geographic table), Bank/solo basis, £'000. By-product figures here are summed from "
    "that table's 'Loans and advances to customers' product rows (Wholesale/Housing/Syndicated/Factoring/"
    "Overdraft/Credit Cards/Mortgage/Financing Order) across all geography columns:\n"
    f"FY2025: Annual Report 2025, p.77 - {AR2025_URL}\n"
    f"FY2024: Annual Report 2025's own FY2024 comparative column, p.78 (figures independently cross-checked "
    "against AR2024's own Balance Sheet net-loans figure) - {AR2025_URL}\n"
    f"FY2023: Annual Report 2023, p.80 - {AR2023_URL}\n"
    f"FY2022: Annual Report 2023's own FY2022 comparative column, p.81 - {AR2023_URL}\n"
    f"FY2021: Financial Statements 2021, p.67 - {AR2021_URL}\n"
    f"FY2020: Financial Statements 2020, note 6(a)(x) 'Analysis of risk concentration', p.61-62 - {AR2020_URL}\n"
    f"FY2019: Financial Statements 2019, note 6(a)(x), p.62-63 (own-year table; FY2018 by-product Totals taken "
    "from this same table's own FY2018 comparative column since FY2018's own report's equivalent table has "
    "unreliable OCR alignment) - {AR2019_URL}\n"
    f"FY2018 by-stage totals: Financial Statements 2018, note 6(a)(xii) 'Impairment allowance analysis', p.54 "
    "- {AR2018_URL}\n"
    f"FY2019/FY2020 by-stage totals: Financial Statements 2019/2020, note 6(a)(xi)/(xii) 'Impairment allowance "
    "analysis' - {AR2019_URL}, {AR2020_URL}\n"
    "'Implied total ECL allowance' is not separately disclosed by product/stage anywhere in these documents - it "
    "is the residual gap between the by-product gross carrying total and the Balance Sheet's own net carrying "
    "value, so it captures the whole-portfolio allowance only (not split by stage), hence no separate Stage 3 "
    "coverage ratio is shown here (would require a stage-level allowance split that isn't disclosed). FY2021's "
    "large ECL gap (£42,083k, 3.40% coverage) is consistent with that year's Cash Flow Statement, which shows "
    "the largest single-year 'Net loss for expected credit losses' charge (£23,665k) in the whole 5-year series. "
    "FY2022's elevated Stage 3/NPL ratio (6.39%, mostly Syndicated loans) fell sharply by FY2023 (0.35%) - both "
    "years' own source tables, not smoothed or averaged. "
    "Scope caveat for FY2018-FY2020: unlike FY2021-2025 (where the by-product and by-stage groupings tie exactly "
    "to each other, both restricted to customer loans only), the FY2018-FY2020 by-stage totals are the note's "
    "broader 'On Balance Sheet' Impairment allowance analysis figures, which also include cash balances and debt "
    "instruments at amortised cost alongside customer loans - they do NOT tie to the by-product (loans-only) "
    "total for these three years (e.g. FY2020: £1,649,987k by-stage vs £1,142,721k by-product), because a clean "
    "stage-level split restricted to customer loans only could not be reliably read off the geography-table's "
    "column layout in these three PDFs' extracted text. The FY2018-FY2020 Stage 3/NPL ratio is therefore computed "
    "against the broader by-stage total, not the narrower by-product total used FY2021 onward - not directly "
    "comparable across that boundary, shown as each year's own disclosed figures rather than force-aligned.\n"
    "FY2014-FY2017 pre-IFRS 9 section: the Bank's own 'Loans and advances to customers' credit-risk note used "
    "IAS 39's incurred-loss classification (gross exposure/individually impaired/past due but not "
    "impaired/neither past due nor impaired, plus an internal-rating-based Performing/Special mention/"
    "Substandard/Doubtful/Loss category split) before the 1 January 2018 IFRS 9 transition replaced it with the "
    "Stage 1/2/3 model used from FY2018 onward - shown here as its own section rather than force-mapped onto the "
    "IFRS 9 rows above, per the same regime-change convention used elsewhere in this project:\n"
    f"FY2017: Financial Statements 2017, p.39-40 - {AR2017_URL}\n"
    f"FY2016: Financial Statements 2016, p.33-34 - {AR2016_URL}\n"
    f"FY2015: Financial Statements 2015, p.32-33 - {AR2015_URL}\n"
    f"FY2014: Financial Statements 2015's own FY2014 comparative, p.32-33 - {AR2015_URL} ({AR2014_SCAN_NOTE})\n"
    "'Performing' is left blank for FY2014/FY2015 where the source table's OCR text was too garbled to read "
    "reliably (rather than transcribe a guessed figure); 'Individually impaired' is negligible in all four years "
    "under IAS 39's incurred-loss model (rounds to 0.00% of gross exposure every year) - 'Special mention "
    "(unrated)', an internal early-warning watchlist category, is shown alongside it as a more informative "
    "leading indicator of the period's credit quality.\n"
    + ENTITY_NOTE
)

bw.add_asset_quality_sheet(
    title="Bank of China (UK) Limited — Asset Quality / Credit Risk Disclosures",
    subtitle="Bank of China (UK) Limited (solo entity basis), £'000 (ratios as calculated)",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=68,
    source_height=430,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=46, source_height=170)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 274521, "FY2024": 274294, "FY2023": 275056, "FY2022": 275000, "FY2021": 275164, "FY2020": 307058, "FY2019": 274958, "FY2018": 274958, "FY2017": 274958, "FY2016": 274958, "FY2015": 274958, "FY2014": 274958})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 ratio", {"FY2025": "27.2%", "FY2024": "24.8%", "FY2023": "26.8%", "FY2022": "23.4%", "FY2021": "24.6%", "FY2020": "26.7%", "FY2019": "27.8%", "FY2018": "29.2%", "FY2017": "30%", "FY2016": "27%", "FY2015": "31%", "FY2014": "34%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2025": 334521, "FY2024": 334294, "FY2023": 335056, "FY2022": 335000, "FY2021": 275164, "FY2020": 307058, "FY2019": 274958, "FY2018": 274958, "FY2017": 274958, "FY2016": 274958, "FY2015": 274958, "FY2014": 274958})],
    p3_sources(),
    note="Equal to CET1 capital every year FY2014-FY2021 (no AT1 instruments in issue until June 2022). A £60m "
         "Additional Tier 1 instrument was issued in June 2022, replacing an equal amount of Tier 2 subordinated "
         "debt.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "33.2%", "FY2024": "30.2%", "FY2023": "32.7%", "FY2022": "28.5%", "FY2021": "24.6%", "FY2020": "26.7%", "FY2019": "27.8%", "FY2018": "29.2%", "FY2017": "30%", "FY2016": "27%", "FY2015": "31%", "FY2014": "34%"})],
    p3_sources(),
    note="Numerically equal to the CET1 ratio every year FY2014-FY2021 since Tier 1 capital equalled CET1 capital "
         "exactly (no AT1 in issue until June 2022); each year's own Table 1/KM1 document states this explicitly "
         "as its own 'Tier 1 capital ratio' line, not just inferred.",
)

metric(
    "Total Capital", "£'000",
    [("Total regulatory capital", {"FY2025": 334521, "FY2024": 334294, "FY2023": 335056, "FY2022": 335000, "FY2021": 335164, "FY2020": 367058, "FY2019": 334958, "FY2018": 334958, "FY2017": 334958, "FY2016": 334958, "FY2015": 334958, "FY2014": 334958})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "33.2%", "FY2024": "30.2%", "FY2023": "32.7%", "FY2022": "28.5%", "FY2021": "29.9%", "FY2020": "31.9%", "FY2019": "33.9%", "FY2018": "35.6%", "FY2017": "36%", "FY2016": "33%", "FY2015": "37%", "FY2014": "42%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted assets (RWA)", {"FY2025": 1008110, "FY2024": 1106898, "FY2023": 1024452, "FY2022": 1176625, "FY2021": 1119380, "FY2020": 1151516, "FY2019": 988901, "FY2018": 941052, "FY2017": 931206, "FY2016": 1003913, "FY2015": 895473, "FY2014": 800993})],
    p3_sources(),
    note="FY2016's own Table 1 states RWA as £1,003,913k; the FY2017 Pillar 3 document's own FY2016 comparative "
         "column shows a slightly different £1,002,116k (a ~£1.8k/0.2% difference, not explained in either "
         "document) - each year's own originally-published figure is used as the primary value throughout, per "
         "project convention.",
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - Bank of China (UK) Limited's UK KM1 Key Metrics tables (same 5 Pillar 3 documents as the Total "
    "RWAs sheet):\n"
    f"FY2025 & FY2024 comparative: Pillar 3 Disclosure 31 December 2025, p.15 - {P3_2025_URL}\n"
    f"FY2023-FY2021: see p3_sources() citations on the Total RWAs sheet.\n\n"
    "NOT DISCLOSED (category breakdown) for FY2014-FY2018 and FY2021-FY2025: none of those Pillar 3 documents "
    "contains a UK OV1/'Overview of risk weighted assets' table breaking RWA down by risk category - confirmed "
    "by reading the FY2025 document's own table of contents and KM1 template in full, and each of the FY2014-"
    "FY2018 documents' own Table 1 in full. Only the single aggregate Total RWA figure exists for those 10 years "
    "(see the Total RWAs sheet, which this sheet's Total row ties out to exactly).\n"
    f"FY2020 (own year) & FY2019 comparative: the FY2020 Pillar 3 document's own Table 9 'Overview of risk "
    "weighted assets' (UK OV1 template), p.20-22 - {P3_2020_URL}. The only year in this bank's whole 12-year "
    "history where a category breakdown was found - it splits Credit risk (standardised approach only), Credit "
    "valuation adjustment (CVA), Market risk (standardised approach only) and Operational risk, each tying "
    "exactly to the Total RWAs sheet's own aggregate figure for both years."
)

bw.add_rwa_breakdown_sheet(
    title="Bank of China (UK) Limited — RWA Breakdown",
    subtitle="Bank of China (UK) Limited (solo entity basis), £'000",
    rows=[
        ("DATA", "Not publicly disclosed — category breakdown", {"FY2025": "Not publicly disclosed", "FY2024": "Not publicly disclosed", "FY2023": "Not publicly disclosed", "FY2022": "Not publicly disclosed", "FY2021": "Not publicly disclosed", "FY2018": "Not publicly disclosed", "FY2017": "Not publicly disclosed", "FY2016": "Not publicly disclosed", "FY2015": "Not publicly disclosed", "FY2014": "Not publicly disclosed"}),
        ("DATA", "Credit risk (excluding counterparty credit risk, standardised approach)", {"FY2020": 822496, "FY2019": 783214}),
        ("DATA", "Credit valuation adjustment (CVA)", {"FY2020": 114722, "FY2019": 12598}),
        ("DATA", "Market risk (standardised approach)", {"FY2020": 11621, "FY2019": 5448}),
        ("DATA", "Operational risk", {"FY2020": 202676, "FY2019": 187641}),
        ("TOTAL", "Total risk exposure amount", {"FY2025": 1008110, "FY2024": 1106898, "FY2023": 1024452, "FY2022": 1176625, "FY2021": 1119380, "FY2020": 1151516, "FY2019": 988901, "FY2018": 941052, "FY2017": 931206, "FY2016": 1003913, "FY2015": 895473, "FY2014": 800993}),
    ],
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=58,
    source_height=220,
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Total Basel III leverage ratio exposure measure", {"FY2025": 1373968, "FY2024": 1462346, "FY2023": 1473437, "FY2022": 1814024, "FY2021": 2431869, "FY2020": 2147455, "FY2019": 1894456, "FY2018": 1860587, "FY2017": 1794647, "FY2016": 1801366, "FY2015": 1593203, "FY2014": 1582346}),
        ("Basel III leverage ratio (%)", {"FY2025": "24.4%", "FY2024": "22.9%", "FY2023": "22.7%", "FY2022": "18.5%", "FY2021": "11.3%", "FY2020": "14.3%", "FY2019": "14.5%", "FY2018": "14.8%", "FY2017": "15%", "FY2016": "15%", "FY2015": "17%", "FY2014": "17%"}),
    ],
    p3_sources(),
    note="FY2021's 11.3% is on an older/broader exposure-measure basis (pre-dates the KM1 'excluding claims on "
         "central banks' framework used from FY2022 onward) - not directly comparable to later years, kept on "
         "its own row per project convention. FY2014-FY2020 use the pre-KM1 CRD IV leverage framework (Table 2 "
         "in each year's own document) - broadly the same 'Tier 1 capital / total exposure measure' concept "
         "throughout, but methodology details (e.g. treatment of off-balance-sheet items, central bank claims) "
         "evolved gradually across this whole span, so a smooth-looking multi-year trend should be read with "
         "that caveat rather than as a single unbroken methodology.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA)", {"FY2025": 1007375, "FY2024": 1014087, "FY2023": 677646, "FY2022": 545654, "FY2021": 527697, "FY2020": 360820, "FY2019": 302154, "FY2018": 381928}),
        ("Total net cash outflow", {"FY2025": 310866, "FY2024": 272240, "FY2023": 174967, "FY2022": 299877, "FY2021": 294774, "FY2020": 148715, "FY2019": 139559, "FY2018": 164459}),
        ("LCR ratio (%)", {"FY2025": "324.1%", "FY2024": "372.5%", "FY2023": "387.3%", "FY2022": "182.0%", "FY2021": "179.0%", "FY2020": "243%", "FY2019": "217%", "FY2018": "232%", "FY2017": "167%"}),
    ],
    p3_sources(),
    note="FY2017's 167% ratio is the only FY2017 LCR figure available anywhere (from the FY2018 Pillar 3 "
         "document's own FY2017 comparative column - FY2017's own document predates LCR disclosure entirely) and "
         "has no accompanying HQLA/outflow £-breakdown, hence the blank cells on those two rows. LCR is "
         "genuinely undisclosed for FY2014-FY2016 (confirmed absent from all three years' own Pillar 3 "
         "documents, read in full).",
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding", {"FY2025": 1389486, "FY2024": 1630136, "FY2023": 1289845, "FY2022": 1463448, "FY2021": 1438026, "FY2020": 1429700, "FY2019": 1263428, "FY2018": 1219968}),
        ("Total required stable funding", {"FY2025": 714820, "FY2024": 752941, "FY2023": 959234, "FY2022": 1209361, "FY2021": 950742, "FY2020": 884460, "FY2019": 797680, "FY2018": 843948}),
        ("NSFR ratio (%)", {"FY2025": "194.4%", "FY2024": "216.5%", "FY2023": "134.5%", "FY2022": "121.0%", "FY2021": "151.3%", "FY2020": "162%", "FY2019": "158%", "FY2018": "145%"}),
    ],
    p3_sources(),
    note="FY2021's own Pillar 3 document does not disclose an NSFR figure at all (the UK NSFR regime's formal KM1 "
         "disclosure only started from FY2022) - the FY2021 figures here are taken from the FY2022 Pillar 3 "
         "document's FY2021 comparative column instead, the only source where they appear. NSFR is genuinely "
         "undisclosed for FY2014-FY2017 (confirmed absent from all four years' own Pillar 3 documents, read in "
         "full) - FY2018 is the earliest year any NSFR figure exists for this bank.",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not disclosed" for y in YEARS})],
    p3_sources(),
    note="No MREL disclosure found in any of the 12 available Pillar 3 documents (FY2014-FY2025) - each was read "
         "in full (table of contents plus a full-text search for 'MREL') and none contains one.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 2274441, "FY2024": 2323319, "FY2023": 2079373, "FY2022": 2290593, "FY2021": 2151180, "FY2020": 1941105, "FY2019": 1687388, "FY2018": 1630982, "FY2017": 1539221, "FY2016": 1549898, "FY2015": 1291410, "FY2014": 1215116}),
        ("Loans and advances to customers", {"FY2025": 810985, "FY2024": 941507, "FY2023": 990763, "FY2022": 1122459, "FY2021": 1194653, "FY2020": 1138583, "FY2019": 1064347, "FY2018": 1044570, "FY2017": 1054454, "FY2016": 1159696, "FY2015": 810776, "FY2014": 722307}),
        ("Deposits from customers", {"FY2025": 1304816, "FY2024": 1355529, "FY2023": 1223068, "FY2022": 1291150, "FY2021": 1333523, "FY2020": 1215647, "FY2019": 1132193, "FY2018": 1107439, "FY2017": 1019007, "FY2016": 982361, "FY2015": 737724, "FY2014": 765899}),
        ("Total shareholders' equity", {"FY2025": 399013, "FY2024": 413744, "FY2023": 433289, "FY2022": 401893, "FY2021": 306776, "FY2020": 342164, "FY2019": 307058, "FY2018": 326076, "FY2017": 307054, "FY2016": 310364, "FY2015": 320268, "FY2014": 301480}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total income", {"FY2025": 188290, "FY2024": 187263, "FY2023": 206185, "FY2022": 150380, "FY2021": 124048, "FY2020": 120103, "FY2019": 115237, "FY2018": 114561, "FY2017": 94483, "FY2016": 91182, "FY2015": 94921, "FY2014": 71621}),
        ("Staff costs", {"FY2025": -86079, "FY2024": -72194, "FY2023": -68058, "FY2022": -59208, "FY2021": -50154, "FY2020": -47607, "FY2019": -47279, "FY2018": -41868, "FY2017": -41365, "FY2016": -32821, "FY2015": -29500, "FY2014": -30178}),
        ("Profit for the year", {"FY2025": 68931, "FY2024": 83917, "FY2023": 103213, "FY2022": 68564, "FY2021": 31478, "FY2020": 35165, "FY2019": 32105, "FY2018": 51123, "FY2017": 32064, "FY2016": 35690, "FY2015": 45450, "FY2014": 25955}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 413744, "FY2024": 433289, "FY2023": 401893, "FY2022": 306776, "FY2021": 342164, "FY2020": 307058, "FY2019": 326076, "FY2018": 307054, "FY2017": 310364, "FY2016": 320268, "FY2015": 301480, "FY2014": 307674}),
        ("Total comprehensive income", {"FY2025": 69011, "FY2024": 83917, "FY2023": 103211, "FY2022": 68576, "FY2021": 31612, "FY2020": 35106, "FY2019": 32105, "FY2018": 51123, "FY2017": 32380, "FY2016": 35546, "FY2015": 44743, "FY2014": 25679}),
        ("Other movements, net (AT1 issued / dividends / IFRS 9 transition)", {"FY2025": -83662, "FY2024": -103462, "FY2023": -71815, "FY2022": 26541, "FY2021": -67000, "FY2020": 0, "FY2019": -51123, "FY2018": -32101, "FY2017": -35690, "FY2016": -45450, "FY2015": -25955, "FY2014": -31873}),
        ("Closing equity", {"FY2025": 399013, "FY2024": 413744, "FY2023": 433289, "FY2022": 401893, "FY2021": 306776, "FY2020": 342164, "FY2019": 307058, "FY2018": 326076, "FY2017": 307054, "FY2016": 310364, "FY2015": 320268, "FY2014": 301480}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash generated from operating activities", {"FY2025": 111252, "FY2024": 405091, "FY2023": 233292, "FY2022": 22570, "FY2021": 304294, "FY2020": 100905, "FY2019": -49465, "FY2018": 52094, "FY2017": 36430, "FY2016": -31327, "FY2015": 145254, "FY2014": 52892}),
        ("Net cash from/(used in) investing activities", {"FY2025": -2623, "FY2024": -25826, "FY2023": -74896, "FY2022": -47511, "FY2021": -1147, "FY2020": 49511, "FY2019": 48732, "FY2018": -737, "FY2017": -66403, "FY2016": -775, "FY2015": -1089, "FY2014": -12257}),
        ("Net cash used in financing activities", {"FY2025": -84086, "FY2024": -103953, "FY2023": -71862, "FY2022": -33536, "FY2021": -68393, "FY2020": -1578, "FY2019": 0, "FY2018": 0, "FY2017": 0, "FY2016": 0, "FY2015": 0, "FY2014": 0}),
        ("Cash and cash equivalents at end of period", {"FY2025": 1073402, "FY2024": 1048859, "FY2023": 773547, "FY2022": 657656, "FY2021": 716133, "FY2020": 481379, "FY2019": 332542, "FY2018": 333275, "FY2017": 281944, "FY2016": 311917, "FY2015": 344019, "FY2014": 199854}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "27.2%", "FY2024": "24.8%", "FY2023": "26.8%", "FY2022": "23.4%", "FY2021": "24.6%", "FY2020": "26.7%", "FY2019": "27.8%", "FY2018": "29.2%", "FY2017": "30%", "FY2016": "27%", "FY2015": "31%", "FY2014": "34%"}),
        ("Tier 1 Ratio", {"FY2025": "33.2%", "FY2024": "30.2%", "FY2023": "32.7%", "FY2022": "28.5%", "FY2021": "24.6%", "FY2020": "26.7%", "FY2019": "27.8%", "FY2018": "29.2%", "FY2017": "30%", "FY2016": "27%", "FY2015": "31%", "FY2014": "34%"}),
        ("Total Capital Ratio", {"FY2025": "33.2%", "FY2024": "30.2%", "FY2023": "32.7%", "FY2022": "28.5%", "FY2021": "29.9%", "FY2020": "31.9%", "FY2019": "33.9%", "FY2018": "35.6%", "FY2017": "36%", "FY2016": "33%", "FY2015": "37%", "FY2014": "42%"}),
        ("Leverage Ratio", {"FY2025": "24.4%", "FY2024": "22.9%", "FY2023": "22.7%", "FY2022": "18.5%", "FY2021": "11.3%", "FY2020": "14.3%", "FY2019": "14.5%", "FY2018": "14.8%", "FY2017": "15%", "FY2016": "15%", "FY2015": "17%", "FY2014": "17%"}),
        ("LCR", {"FY2025": "324.1%", "FY2024": "372.5%", "FY2023": "387.3%", "FY2022": "182.0%", "FY2021": "179.0%", "FY2020": "243%", "FY2019": "217%", "FY2018": "232%", "FY2017": "167%"}),
        ("NSFR", {"FY2025": "194.4%", "FY2024": "216.5%", "FY2023": "134.5%", "FY2022": "121.0%", "FY2021": "151.3%", "FY2020": "162%", "FY2019": "158%", "FY2018": "145%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. See the Cash Flow Statement sheet's source note for "
         "a disclosed restatement gap between FY2022's and FY2023's own reports. FY2014's own Annual Report PDF "
         "is a scanned document with no extractable text layer - its figures are taken from FY2015's own report's "
         "FY2014 comparative column instead (see AR2014_SCAN_NOTE on the Balance Sheet sheet). LCR and NSFR are "
         "genuinely undisclosed before FY2017/FY2018 respectively (blank, not zero).",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BANK OF CHINA UK FINANCIALS.xlsx")
