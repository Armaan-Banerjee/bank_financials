import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/01448919/filing-history/MzUyMjY1MjQyNWFkaXF6a2N4/document?download=0&format=pdf"
AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/01448919/filing-history/MzQ3MzI5ODI4OWFkaXF6a2N4/document?download=0&format=pdf"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/01448919/filing-history/MzQyMjI5MjUwM2FkaXF6a2N4/document?download=0&format=pdf"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/01448919/filing-history/MzM4MTE3NjI0OGFkaXF6a2N4/document?download=0&format=pdf"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/01448919/filing-history/MzM0MjM1MjU5OWFkaXF6a2N4/document?download=0&format=pdf"
PILLAR_URL = "https://www.rathbones.com/sites/main/files/results_and_presentations/files/31_december_2024_pillar_3_disclosures.pdf"
# Dead original, retained for provenance - do NOT delete. rathbones.com renamed
# the site directory from /sites/rathbones.com/ to /sites/main/; only that one
# path segment changed. The URL below was confirmed HTTP 404 (not blocked, not
# a soft-404) on 15 September 2026 and replaced by PILLAR_URL above, which was
# fetched and confirmed to be a real PDF (%PDF magic bytes, not merely HTTP
# 200): 49 pages, cover "PILLAR 3 DISCLOSURES / 31 DECEMBER 2024 / RATHBONES
# GROUP PLC". It is the only rathbones.com URL in this script; every other
# source here is a Companies House filing-history document (all five
# re-verified live and serving %PDF on 15 September 2026), so no other URL in
# this file is exposed to the same rename.
PILLAR_URL_DEAD = "https://www.rathbones.com/sites/rathbones.com/files/results_and_presentations/files/31_december_2024_pillar_3_disclosures.pdf"
# LATEST-EDITION CHECK, 16 September 2026 (KM1-024). Checked rathbones.com's own
# investor page (https://www.rathbones.com/investor-relations/results-and-
# presentations, which now redirects to /en-gb/wealth-management/investor-
# relations/results-reports-and-presentations) rather than any URL already cited
# here. NEWEST Pillar 3 on that page is "PILLAR 3 DISCLOSURES / 31 DECEMBER 2025
# / RATHBONES GROUP PLC" (49pp, %PDF verified, application/pdf, 2,610,804 bytes)
# at PILLAR2025_URL below - one edition newer than PILLAR_URL. A semi-annual
# edition at 30 June 2025 is also published (PILLAR2025H1_URL). NOTE the site
# spells the annual file "discosures" (sic).
# NO new figures for this workbook follow from either document: both are
# Rathbones Group Plc CONSOLIDATED, and the FY2025 edition repeats the
# consolidated-only position verbatim on printed p.6. The Company's own FY2025
# statutory accounts (AR2025_URL) were already the newest RIM filing and are
# already transcribed here, so YEARS is unchanged.
PILLAR2025_URL = "https://www.rathbones.com/sites/main/files/results_and_presentations/files/31_december_2025_pillar_3_discosures.pdf"
PILLAR2025H1_URL = "https://www.rathbones.com/sites/main/files/results_and_presentations/files/interim_pillar_3_disclosures_30_june_2025_1.pdf"

ENTITY_NOTE = (
    "Entity: Rathbones Investment Management Limited (FRN 116316, company 01448919), formerly "
    "Rathbone Investment Management Limited until 7 December 2022. The Company is a wholly-owned "
    "subsidiary of Rathbones Group Plc and prepares entity-only IFRS financial statements under the "
    "Companies Act 2006 Section 400 exemption from consolidated accounts. Figures are GBP'000. "
    "The Company is an investment and wealth-management business, not the consolidated Rathbones Group.\n\n"
    "Pillar 3 metrics are not substituted from Rathbones Group Plc: the official 2024 Pillar 3 report "
    "states that disclosures are consolidated and that no large subsidiary meets the definition requiring "
    "individual disclosure. Accordingly, entity-level CET1, Tier 1, Total Capital, RWA, leverage, LCR, "
    "NSFR and MREL figures are not publicly disclosed in the Company's accounts.\n"
    "SOURCE FOR THAT STATEMENT (citation added 15 September 2026 - the document was named here but its URL "
    "was previously not printed on any sheet): Rathbones Group Plc, Pillar 3 Disclosures 31 December 2024, "
    "section 1 'Executive summary', p.6 - 'Disclosures are made on a consolidated group level, as we have no "
    "large subsidiaries meeting the requirements for individual disclosure under the definition within CRR "
    "Article 4(146).' - " + PILLAR_URL + "\n"
    "BASIS WARNING - this Group document is cited ONLY as evidence of ABSENCE, i.e. as the reason the "
    "entity-level Pillar 3 sheets in this workbook are blank. Not one figure in this workbook is taken from "
    "it. Every figure here comes from Rathbones Investment Management Limited's own entity-only statutory "
    "accounts filed at Companies House under company number 01448919. Re-checked 15 September 2026 against "
    "the replacement document in full: it discloses no RIM-solo quantitative metric anywhere. Its NSFR "
    "section (p.25) does say Rathbones 'is required to calculate and monitor the ratio on a RIM-solo and "
    "group consolidated basis, reporting the positions quarterly', but it prints only the group consolidated "
    "figures - templates UK KM1, UK LIQ1 and UK LIQ2 are all group-level - so there is no solo-consolidation "
    "or significant-subsidiary annex to draw entity data from, and no Group figure has been substituted.\n"
    "LATEST-EDITION CHECK (16 September 2026): rathbones.com's own investor page was checked directly and now "
    "carries a NEWER annual edition, Rathbones Group Plc Pillar 3 Disclosures 31 December 2025 - "
    + PILLAR2025_URL + " - plus a semi-annual edition at 30 June 2025 - " + PILLAR2025H1_URL + ". The FY2025 "
    "edition repeats the consolidated-only position verbatim at section 1 'Executive summary', printed p.6: "
    "'Disclosures are made on a consolidated group level, as the grouphave [sic] no large subsidiaries meeting "
    "the requirements for individual disclosure under the definition within CRR Article 4(146).' Its only KM1 is "
    "again a Rathbones Group Plc consolidated table, so nothing in this entity-level workbook changes; no figure "
    "has been taken from it either.\n"
    "LINK PROVENANCE (15 September 2026): the URL above is a REPLACEMENT. rathbones.com renamed its site "
    "directory from /sites/rathbones.com/ to /sites/main/, so the URL originally cited for this document now "
    "returns HTTP 404. Dead original, kept so the provenance chain stays readable: " + PILLAR_URL_DEAD + "\n\n"
    "The 2021 own-account "
    "closing cash (£1,530,445k) does not equal the 2022 account's comparative opening cash (£1,527,887k); "
    "both source-presented figures are retained and the difference is not inferred or forced."
)

CASH_SOURCES = (
    "Sources - Rathbones Investment Management Limited statutory Statement of cash flows, GBP'000. "
    "Each year's own column was checked against the next year's comparative column where available.\n"
    f"FY2025 and FY2024 comparative: Annual report and financial statements 2025, p.25 - {AR2025_URL}\n"
    f"FY2024 and FY2023 comparative: Annual report and financial statements 2024, p.28 - {AR2024_URL}\n"
    f"FY2023 and FY2022 comparative: Annual report and financial statements 2023, p.29 - {AR2023_URL}\n"
    f"FY2022 and FY2021 comparative: Annual report and financial statements 2022, p.29 - {AR2022_URL}\n"
    f"FY2021: Annual report and financial statements 2021, p.29 - {AR2021_URL}\n\n"
    + ENTITY_NOTE
)

rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax", {"FY2025":111473,"FY2024":21167,"FY2023":63864,"FY2022":49174,"FY2021":75198}),
    ("DATA", "Change in fair value through profit or loss", {"FY2024":19,"FY2023":-958,"FY2022":-588}),
    ("DATA", "Net charge for provisions", {"FY2025":6493,"FY2024":1962,"FY2023":1914,"FY2022":150,"FY2021":1436}),
    ("DATA", "Net interest income", {"FY2025":-83158,"FY2024":-56469,"FY2023":-49638,"FY2022":-22576,"FY2021":-6657}),
    ("DATA", "Impairment losses on financial instruments", {"FY2025":4,"FY2024":17,"FY2023":-7,"FY2022":-39,"FY2021":-727}),
    ("DATA", "Profit on disposal of property, plant and equipment", {"FY2023":0,"FY2022":0,"FY2021":67}),
    ("DATA", "Depreciation and amortisation", {"FY2025":43690,"FY2024":23492,"FY2023":22843,"FY2022":22072,"FY2021":23966}),
    ("DATA", "Impairment in investment in subsidiary", {"FY2025":43888}),
    ("DATA", "Foreign exchange movements", {"FY2025":3025,"FY2024":-1012,"FY2023":3433,"FY2022":-7078,"FY2021":-519}),
    ("DATA", "Interest paid", {"FY2025":-74032,"FY2024":-81871,"FY2023":-67542,"FY2022":-19438,"FY2021":-1300}),
    ("DATA", "Interest received", {"FY2025":150214,"FY2024":137180,"FY2023":93817,"FY2022":31519,"FY2021":-10470}),
    ("DATA", "Net (increase)/decrease in loans and advances to banks and customers", {"FY2025":-81775,"FY2024":21867,"FY2023":87017,"FY2022":7357,"FY2021":-38715}),
    ("DATA", "Net (increase)/decrease in settlement balance debtors", {"FY2025":-9406,"FY2024":3800,"FY2023":-19223,"FY2022":9006,"FY2021":14260}),
    ("DATA", "Net increase/(decrease) in prepayments, accrued income and other assets", {"FY2025":-57400,"FY2024":-41320,"FY2023":21727,"FY2022":-13828,"FY2021":-364}),
    ("DATA", "Net increase/(decrease) in amounts due to customers and deposits by banks", {"FY2025":938715,"FY2024":172629,"FY2023":-251998,"FY2022":231254,"FY2021":-260531}),
    ("DATA", "Net increase/(decrease) in settlement balance creditors", {"FY2025":15921,"FY2024":5283,"FY2023":10914,"FY2022":3910,"FY2021":-27472}),
    ("DATA", "Net increase/(decrease) in accruals, deferred income, provisions and other liabilities", {"FY2025":14555,"FY2024":3739,"FY2023":-239,"FY2022":-2741,"FY2021":2395}),
    ("DATA", "Tax paid", {"FY2025":-34027,"FY2024":-10227,"FY2023":-15392,"FY2022":-11426,"FY2021":-19676}),
    ("TOTAL", "Net cash inflow/(outflow) from operating activities", {"FY2025":988180,"FY2024":200256,"FY2023":-99468,"FY2022":276728,"FY2021":-249109}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Cash acquired on acquisition of subsidiaries", {"FY2025":46460}),
    ("DATA", "Acquisition of investment in subsidiary undertaking", {"FY2021":0}),
    ("DATA", "Purchase of property, plant and equipment and intangible assets", {"FY2025":-16629,"FY2024":-20925,"FY2023":-6521,"FY2022":-8561,"FY2021":-17275}),
    ("DATA", "Proceeds from sale of equity securities", {"FY2024":1162,"FY2023":2922}),
    ("DATA", "Purchase of investment securities", {"FY2025":-2690119,"FY2024":-2027961,"FY2023":-2059899,"FY2022":-1259979,"FY2021":-930728}),
    ("DATA", "Proceeds from sale and redemption of investment securities", {"FY2025":2101020,"FY2024":2045349,"FY2023":1807092,"FY2022":983481,"FY2021":821100}),
    ("TOTAL", "Net cash used in investing activities", {"FY2025":-559268,"FY2024":-2375,"FY2023":-256406,"FY2022":-285059,"FY2021":-126903}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividends paid", {"FY2025":-69000,"FY2024":-27000,"FY2023":-50000,"FY2022":-35000,"FY2021":-55000}),
    ("DATA", "Payment of lease liabilities", {"FY2022":-81,"FY2021":-90}),
    ("TOTAL", "Net cash used in financing activities", {"FY2025":-69000,"FY2024":-27000,"FY2023":-50000,"FY2022":-35081,"FY2021":-55090}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025":359912,"FY2024":170881,"FY2023":-405874,"FY2022":-43412,"FY2021":-431102}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {"FY2025":1249482,"FY2024":1078601,"FY2023":1484475,"FY2022":1527887,"FY2021":1961547}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2025":1609394,"FY2024":1249482,"FY2023":1078601,"FY2022":1484475,"FY2021":1530445}),
]

bw = BankWorkbook(bank_name="Rathbones Investment Management Limited", years=YEARS, year_label=None, header_color="6B3F8C")

STATEMENTS_SOURCES = (
    "Sources - Rathbones Investment Management Limited statutory accounts, entity basis, GBP'000.\n"
    f"FY2025 and FY2024 comparative: Annual report and financial statements 2025, Statement of comprehensive "
    f"income p.22, Statement of changes in equity p.23, Balance sheet p.24 - {AR2025_URL}\n"
    f"FY2024 and FY2023 comparative: Annual report and financial statements 2024, p.25/26/27 - {AR2024_URL}\n"
    f"FY2023 and FY2022 comparative: Annual report and financial statements 2023, p.26/27/28 - {AR2023_URL}\n"
    f"FY2022 and FY2021 comparative: Annual report and financial statements 2022, p.26/27/29 - {AR2022_URL}\n\n"
    + ENTITY_NOTE
)

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances with central banks", {"FY2025": 1503963, "FY2024": 1165956, "FY2023": 1038280, "FY2022": 1412915, "FY2021": 1463293}),
    ("DATA", "Settlement balances", {"FY2025": 44654, "FY2024": 35248, "FY2023": 39048, "FY2022": 19825, "FY2021": 28831}),
    ("DATA", "Loans and advances to banks", {"FY2025": 105394, "FY2024": 83482, "FY2023": 42601, "FY2022": 106475, "FY2021": 97887}),
    ("DATA", "Loans and advances to customers", {"FY2025": 206392, "FY2024": 124556, "FY2023": 131817, "FY2022": 205120, "FY2021": 194424}),
    ("DATA", "Investment securities - fair value through profit and loss", {"FY2023": 1181, "FY2022": 3146, "FY2021": 2558}),
    ("DATA", "Investment securities - amortised cost", {"FY2025": 1864282, "FY2024": 1278219, "FY2023": 1294589, "FY2022": 1045234, "FY2021": 761654}),
    ("DATA", "Prepayments, accrued income and other assets", {"FY2025": 209933, "FY2024": 147396, "FY2023": 118622, "FY2022": 92179, "FY2021": 85601}),
    ("DATA", "Property, plant and equipment", {"FY2025": 48050, "FY2024": 10939, "FY2023": 7783, "FY2022": 12341, "FY2021": 12496}),
    ("DATA", "Right of use assets", {"FY2023": 1, "FY2022": 17, "FY2021": 83}),
    ("DATA", "Current tax asset", {"FY2025": 6770, "FY2024": 7992, "FY2023": 2130, "FY2022": 3520, "FY2021": 2826}),
    ("DATA", "Deferred tax asset", {"FY2024": 1116, "FY2023": 1158}),
    ("DATA", "Intangible assets", {"FY2025": 779332, "FY2024": 153029, "FY2023": 158751, "FY2022": 170498, "FY2021": 183788}),
    ("DATA", "Investments in subsidiary undertakings", {"FY2025": 40913, "FY2024": 9798, "FY2023": 9798, "FY2022": 9798, "FY2021": 9798}),
    ("TOTAL", "Total assets", {"FY2025": 4809683, "FY2024": 3017731, "FY2023": 2845759, "FY2022": 3081068, "FY2021": 2843239}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2025": 8410, "FY2024": 3770, "FY2023": 12359, "FY2022": 1035, "FY2021": 2213}),
    ("DATA", "Settlement balances", {"FY2025": 63146, "FY2024": 47225, "FY2023": 41942, "FY2022": 31028, "FY2021": 27118}),
    ("DATA", "Due to customers", {"FY2025": 3474635, "FY2024": 2540560, "FY2023": 2359342, "FY2022": 2622664, "FY2021": 2390232}),
    ("DATA", "Accruals, deferred income, provisions and other liabilities", {"FY2025": 41844, "FY2024": 20964, "FY2023": 16271, "FY2022": 8736, "FY2021": 9432}),
    ("DATA", "Lease liabilities", {"FY2022": 0, "FY2021": 81}),
    ("DATA", "Deferred tax liability", {"FY2025": 74300, "FY2022": 1718, "FY2021": 4243}),
    ("TOTAL", "Total liabilities", {"FY2025": 3662335, "FY2024": 2612519, "FY2023": 2429914, "FY2022": 2665181, "FY2021": 2433319}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 4996, "FY2024": 4996, "FY2023": 4996, "FY2022": 4996, "FY2021": 4996}),
    ("DATA", "Share premium", {"FY2025": 751899, "FY2024": 298066, "FY2023": 298066, "FY2022": 298066, "FY2021": 298066}),
    ("DATA", "Other reserves", {"FY2025": -21897}),
    ("DATA", "Retained earnings", {"FY2025": 412350, "FY2024": 102150, "FY2023": 112783, "FY2022": 112825, "FY2021": 106858}),
    ("TOTAL", "Total equity", {"FY2025": 1147348, "FY2024": 405212, "FY2023": 415845, "FY2022": 415887, "FY2021": 409920}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 4809683, "FY2024": 3017731, "FY2023": 2845759, "FY2022": 3081068, "FY2021": 2843239}),
]
bw.add_balance_sheet_sheet(
    title="Rathbones Investment Management Limited — Balance Sheet",
    subtitle="Entity basis, £'000. Blank cells indicate a line not disclosed that year (0 indicates a line disclosed as nil, not a gap).",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=280,
    unit_suffix=" (£'000)",
)

income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest and similar income", {"FY2025": 155597, "FY2024": 137333, "FY2023": 123040, "FY2022": 43908, "FY2021": 7577}),
    ("DATA", "Interest expense and similar charges", {"FY2025": -72439, "FY2024": -80881, "FY2023": -73395, "FY2022": -21293, "FY2021": -193}),
    ("TOTAL", "Net interest income", {"FY2025": 83158, "FY2024": 56452, "FY2023": 49645, "FY2022": 22615, "FY2021": 7384}),
    ("DATA", "Fee and commission income", {"FY2025": 626296, "FY2024": 352499, "FY2023": 318826, "FY2022": 318304, "FY2021": 335389}),
    ("DATA", "Fee and commission expense", {"FY2025": -3515, "FY2024": -3050, "FY2023": -2811, "FY2022": -3666, "FY2021": -4016}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 622781, "FY2024": 349449, "FY2023": 316015, "FY2022": 314638, "FY2021": 331373}),
    ("DATA", "Intra-group management charges", {"FY2025": 16754, "FY2024": 13433, "FY2023": 13760, "FY2022": 12705, "FY2021": 13518}),
    ("DATA", "Dividends from subsidiaries", {"FY2025": 57002, "FY2024": 5000, "FY2023": 5000, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Other operating income", {"FY2025": 1943, "FY2024": 630, "FY2023": 1331, "FY2022": 1189, "FY2021": 664}),
    ("TOTAL", "Operating income", {"FY2025": 781638, "FY2024": 424964, "FY2023": 385751, "FY2022": 351147, "FY2021": 352939}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Charges in relation to client relationships and goodwill", {"FY2025": -32717, "FY2024": -13244, "FY2023": -12593, "FY2022": -13311, "FY2021": -13515}),
    ("DATA", "Impairment in investment in subsidiaries", {"FY2025": -43888}),
    ("DATA", "Other operating expenses", {"FY2025": -593560, "FY2024": -390553, "FY2023": -309294, "FY2022": -288662, "FY2021": -264226}),
    ("TOTAL", "Operating expenses", {"FY2025": -670165, "FY2024": -403797, "FY2023": -321887, "FY2022": -301973, "FY2021": -277741}),
    ("TOTAL", "Profit before tax", {"FY2025": 111473, "FY2024": 21167, "FY2023": 63864, "FY2022": 49174, "FY2021": 75198}),
    ("DATA", "Taxation", {"FY2025": -30356, "FY2024": -4800, "FY2023": -13906, "FY2022": -8207, "FY2021": -16234}),
    ("TOTAL", "Profit for the year attributable to equity holders of the Company", {"FY2025": 81117, "FY2024": 16367, "FY2023": 49958, "FY2022": 40967, "FY2021": 58964}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Other comprehensive income for the year, net of tax", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("TOTAL", "Total comprehensive income for the year, net of tax", {"FY2025": 81117, "FY2024": 16367, "FY2023": 49958, "FY2022": 40967, "FY2021": 58964}),
]
bw.add_income_statement_sheet(
    title="Rathbones Investment Management Limited — Profit & Loss",
    subtitle="Entity basis, £'000. Statement of comprehensive income; all comprehensive income each year is attributable to equity holders of the Company.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=280,
    unit_suffix=" (£'000)",
)

equity_headers = ["Share capital", "Share premium", "Other reserves", "Retained earnings", "Total equity"]
equity_rows = [
    ("TOTAL", "At 1 January 2021", (4996, 298066, None, 102894, 405956)),
    ("TOTAL", "Total comprehensive income for the year (FY2021)", (None, None, None, 58964, 58964)),
    ("DATA", "Dividends paid (FY2021)", (None, None, None, -55000, -55000)),
    ("TOTAL", "At 31 December 2021", (4996, 298066, None, 106858, 409920)),
    ("TOTAL", "Total comprehensive income for the year (FY2022)", (None, None, None, 40967, 40967)),
    ("DATA", "Dividends paid (FY2022)", (None, None, None, -35000, -35000)),
    ("TOTAL", "At 31 December 2022", (4996, 298066, None, 112825, 415887)),
    ("TOTAL", "Total comprehensive income for the year (FY2023)", (None, None, None, 49958, 49958)),
    ("DATA", "Dividends paid (FY2023)", (None, None, None, -50000, -50000)),
    ("TOTAL", "At 31 December 2023", (4996, 298066, None, 112783, 415845)),
    ("TOTAL", "Total comprehensive income for the year (FY2024)", (None, None, None, 16367, 16367)),
    ("DATA", "Dividends paid (FY2024)", (None, None, None, -27000, -27000)),
    ("TOTAL", "At 31 December 2024", (4996, 298066, None, 102150, 405212)),
    ("TOTAL", "Total comprehensive income for the year (FY2025)", (None, None, None, 81117, 81117)),
    ("DATA", "Dividends paid (FY2025)", (None, None, None, -69000, -69000)),
    ("DATA", "Arisen from business transfer (FY2025)", (None, None, -21897, None, -21897)),
    ("DATA", "Issue of share capital (FY2025)", (None, 751898, None, None, 751898)),
    ("DATA", "Cancellation of share premium (FY2025)", (None, -298065, None, 298065, 0)),
    ("DATA", "Other movement (FY2025)", (None, None, None, 18, 18)),
    ("TOTAL", "At 31 December 2025", (4996, 751899, -21897, 412350, 1147348)),
]
bw.add_equity_changes_sheet(
    title="Rathbones Investment Management Limited — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, entity basis, £'000. Equity reconciliation ladder confirmed: "
              "every year's own closing balance ties exactly to both the next year's own opening balance and that "
              "year's own Balance Sheet Total equity - zero undocumented plug rows across all 5 years, including "
              "FY2025's four separate movements (business transfer, share issue, share premium cancellation, other).",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=52,
    source_height=260,
)

bw.add_cash_flow_sheet(title="Rathbones Investment Management Limited — Cash Flow Statement", subtitle="Entity basis, £'000. All figures transcribed from the Company's statutory accounts.", rows=rows, sources_text=CASH_SOURCES, first_col_width=86, source_height=470, unit_suffix=" (£'000)")

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, by product", {}),
    ("DATA", "Overdrafts", {"FY2025": 17710, "FY2024": 15606, "FY2023": 9558, "FY2022": 6238, "FY2021": 6742}),
    ("DATA", "Loan book", {"FY2025": 146810, "FY2024": 75942, "FY2023": 101666, "FY2022": 159694, "FY2021": 167981}),
    ("DATA", "Amounts owed by group undertakings", {"FY2025": 39880, "FY2024": 31935, "FY2023": 19629, "FY2022": 38576, "FY2021": 18936}),
    ("DATA", "Financial planning debtors", {"FY2025": 747, "FY2024": 718, "FY2023": 656, "FY2022": 520, "FY2021": 310}),
    ("DATA", "Other debtors", {"FY2025": 1246, "FY2024": 417, "FY2023": 308, "FY2022": 104, "FY2021": 455}),
    ("TOTAL", "Total before impairment loss allowance", {"FY2025": 206393, "FY2024": 124618, "FY2023": 131817, "FY2022": 205132, "FY2021": 194424}),
    ("DATA", "Less: impairment loss allowance", {"FY2025": 0, "FY2024": -62, "FY2023": 0, "FY2022": -12, "FY2021": 0}),
    ("TOTAL", "Net loans and advances to customers", {"FY2025": 206392, "FY2024": 124556, "FY2023": 131817, "FY2022": 205120, "FY2021": 194424}),
    ("SECTION", "Asset quality ratio (derived)", {}),
    ("DATA", "Impairment loss allowance as % of gross loans and advances to customers", {"FY2025": "0.0%", "FY2024": "0.05%", "FY2023": "0.0%", "FY2022": "0.01%", "FY2021": "0.0%"}),
]
bw.add_asset_quality_sheet(
    title="Rathbones Investment Management Limited — Asset Quality",
    subtitle="Entity basis, £'000. Loans and advances to customers by product (Note 14); no IFRS 9 Stage 1/2/3 split "
              "is disclosed for this book - loans are fully secured against clients' investment portfolios held in "
              "Rathbones' nominee name, and the Company's own risk-management note (27) reports £nil-to-negligible "
              "impairment losses arising from the loan book in every year covered. (The Company's separate treasury "
              "book - money-market/interbank placements, not customer lending - does carry a 12-month/lifetime ECL "
              "stage split in note 27, but that reflects counterparty credit risk on Company cash, not loan asset "
              "quality, so it is not reproduced here.)",
    rows=asset_quality_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nNote 14 (Loans and advances to customers) page references - FY2025/FY2024: p.39; FY2024/FY2023: p.41; "
        "FY2023/FY2022: p.41 (AR2023); FY2022/FY2021: p.43 (AR2022). FY2025's component lines sum to £206,393k "
        "against a reported net total of £206,392k - a genuine £1k source rounding artifact, not a transcription "
        "error; the reported net total is used for the Balance Sheet tie-out."
    ),
    first_col_width=90,
    source_height=280,
    unit_suffix=" (£'000)",
)

NOT_DISCLOSED = "Not publicly disclosed at Rathbones Investment Management Limited entity level. Rathbones Group Plc's official Pillar 3 reports are consolidated and state that no large subsidiary meets the definition requiring individual disclosure; group metrics must not be substituted for this Company's metrics. See the source note."

# Re-verified 2026-09-15 against the FY2025 Pillar 3, which confirms the
# consolidated-only position verbatim: "Disclosures are made on a consolidated
# group level, as the group have no large subsidiaries meeting the requirements
# for individual disclosure under the definition within CRR Article 4(146)."
# That document also records that Rathbones "is required to calculate and
# monitor the ratio on a RIM-solo and group consolidated basis, reporting the
# positions quarterly" - so a RIM-solo position exists but goes to the
# regulator only and is not published.  The Pillar 3 templates therefore stay
# blank at entity level.
#
# BUT the Company's OWN statutory accounts do disclose one entity-level
# regulatory figure, which had been missed: a single own-funds total in the
# capital-management note.  That is transcribed into Total Capital below.
RCR_SOURCES = CASH_SOURCES + (
    "\n\nENTITY-LEVEL REGULATORY CAPITAL RESOURCES (added 2026-09-15). Each year's own Annual Report and Financial "
    "Statements, capital-management note (scanned filings - figures read by OCR at 300-400 dpi and confirmed "
    "visually):\n"
    "FY2025 and FY2024 comparative: 'At 31 December 2025, the Company's regulatory capital resources, including "
    "retained earnings for 2025, were GBP467,062,000 (2024: GBP261,190,000).' - " + AR2025_URL + "\n"
    "FY2024 own-year, and FY2023 comparative: 'At 31 December 2024 ... were GBP261,190,000 (2023: "
    "GBP267,182,000).' - " + AR2024_URL + "\n"
    "FY2023 own-year, and FY2022 comparative: 'At 31 December 2023 ... were GBP267,182,000 (2022: "
    "GBP256,378,000).' - " + AR2023_URL + "\n"
    "FY2021 own-year: 'At 31 December 2021 ... were GBP237,897,000 (2020: GBP247,786,000).' - " + AR2021_URL + "\n"
    "VALIDATION: every year except FY2022 and FY2025 appears in two separate filings and agrees in both - FY2024 "
    "reads GBP261,190,000 in both the FY2025 comparative and the FY2024 own-year note, and FY2023 reads "
    "GBP267,182,000 in both the FY2024 comparative and the FY2023 own-year note.\n"
    "BASIS: this is the Company's total regulatory capital RESOURCES (own funds) as defined in its own note - "
    "'accounting capital and certain deductions from accounting capital, the latter largely in respect of "
    "intangible assets', measured against Pillar I and Pillar II requirements under the PRA's application of CRD. "
    "The note gives NO tier split and NO risk-weighted assets, so CET1 Capital, Tier 1 Capital, all three capital "
    "ratios and Total RWAs remain blank rather than derived - in particular this figure has NOT been copied into "
    "CET1 or Tier 1, because the Company nowhere states that its capital is wholly CET1."
)

# ---------------------------------------------------------------
# KM1 Key Metrics - NOT APPLICABLE at this entity's level.
#
# The finding here is the middle one of the three the KM1 map distinguishes:
# it is NOT "no Pillar 3 is published" and NOT "the template is not used".
# Rathbones Group Plc publishes a Pillar 3 every year and DOES print the UK KM1
# template in it - but only on a consolidated Rathbones Group Plc basis, and the
# document states in terms that no subsidiary is large enough to require
# individual disclosure. This workbook is Rathbones Investment Management
# Limited, entity-only, so the Group's KM1 is a different reporting entity and
# a different basis; transcribing it here would put Group capital against RIM
# statutory accounts. Every one of the 11 single-metric sheets in this workbook
# is blank for exactly the same reason, so a populated KM1 would also contradict
# them. The evidence is positive and quoted below - not a failed fetch: both the
# FY2024 and the newer FY2025 editions were downloaded (%PDF verified) and read.
# ---------------------------------------------------------------
KM1_SOURCES = (
    "Sources - the UK KM1 key-metrics template is NOT published for Rathbones Investment Management Limited "
    "in any year, and no figure on this sheet is withheld for want of looking. Positive evidence, from the "
    "publisher's own documents:\n"
    "• Rathbones Group Plc, Pillar 3 Disclosures 31 December 2025 (the NEWEST edition on rathbones.com as at "
    "16 September 2026, found on the bank's own results/reports/presentations page rather than from a cited "
    "URL), section 1 'Executive summary', printed p.6: 'Disclosures are made on a consolidated group level, as "
    "the grouphave [sic] no large subsidiaries meeting the requirements for individual disclosure under the "
    "definition within CRR Article 4(146).' - " + PILLAR2025_URL + "\n"
    "• The same document DOES print a 'UK KM1 - Key metrics template' (contents p.3; table at printed p.3, "
    "in GBP million), but its header block reads 'A summary of the Rathbones group's key ratios' and the table "
    "is Rathbones Group Plc CONSOLIDATED. That is a different reporting entity and a different basis from this "
    "workbook, whose every figure is Rathbones Investment Management Limited entity-only, so it is deliberately "
    "not reproduced here.\n"
    "• Rathbones Group Plc, Pillar 3 Disclosures 31 December 2024, same statement at section 1, printed p.6 - "
    + PILLAR_URL + "\n"
    "• Rathbones Group Plc, Pillar 3 Semi-annual Disclosures 30 June 2025, section 1.2: 'We have no large "
    "subsidiaries meeting the...' [requirements for individual disclosure] - " + PILLAR2025H1_URL + "\n"
    "• The FY2025 annual edition also records (p.25 area, NSFR section) that Rathbones 'is required to "
    "calculate and monitor the ratio on a RIM-solo and group consolidated basis, reporting the positions "
    "quarterly'. A RIM-solo regulatory position therefore EXISTS but goes to the regulator only; it is not "
    "published in any Pillar 3 template, and nothing has been derived from the Group figures to stand in for it.\n"
    "• THE PARENT'S PILLAR 3 WAS SEARCHED FOR A SUBSIDIARY BLOCK, which is the first place a UK subsidiary's "
    "regulatory figures normally live - not the last. It has none. The FY2025 edition was read end to end for "
    "an 'Individual'/'Solo'/'RIM' COLUMN inside a group table and for a separate subsidiary TABLE in an "
    "appendix (both of which exist at other UK groups), case-insensitively and with a richness control to "
    "prove the extraction was working ('capital' 96 hits, 'ratio' 135, 'cet1' 17, 'leverage' 20, 'RIM' 24). "
    "Findings, all negative for an entity-level figure: every KM1/OV1/CC1/CC2/LR/LIQ template in the document "
    "and in all ten appendices is captioned for the consolidated group; no template carries an entity column; "
    "and template UK CCA's row 6, 'Eligible at solo/(sub-)consolidated/solo&(sub-)consolidated', reads "
    "'Consolidated' for every one of the group's own-funds instruments. The 24 'RIM' mentions are all "
    "narrative - governance, committees, client lending, the liquidity buffer - and carry no RIM-solo "
    "regulatory figure. Appendix 1's excluded-templates listing likewise excludes templates on relevance and "
    "materiality grounds, not an entity-level annex.\n"
    "• The 30 June 2025 SEMI-ANNUAL edition was used as an independent second opinion at no transcription "
    "cost, and agrees: section 1.2 'We have no large subsidiaries meeting the...' requirements for individual "
    "disclosure, and its key-metrics table is likewise consolidated group only.\n"
    "• NOT BACK-FILLED FROM THE STATUTORY ACCOUNTS. The Company's own accounts do disclose a single "
    "entity-level own-funds total (see the Total Capital sheet), but that is a capital-management note, not a "
    "KM1 row, and it carries no tier split and no RWA. It is not mapped onto template row numbers here, because "
    "doing so would invent a correspondence the Company never published.\n"
    "• SOURCE DEFECT RECORDED, NOT CORRECTED (and not relied on, since nothing here is transcribed from it): "
    "the FY2025 annual edition's prose says its KM1 shows key ratios 'as at 31 December 2025', but the table's "
    "own column headers are printed 'c 30 June 2025' and 'e 31 December 2024'. Noted for a future reader who "
    "goes looking for 31 December 2025 columns in that document.\n\n"
    + ENTITY_NOTE
)

bw.add_km1_sheet(
    title="Rathbones Investment Management Limited — KM1 Key Metrics",
    subtitle="Not applicable at this entity's level. Pillar 3 IS published and the UK KM1 template IS used - but "
             "only by the parent, Rathbones Group Plc, on a consolidated basis, which its own Pillar 3 states is "
             "the only basis of disclosure because no subsidiary is large enough to require individual disclosure "
             "(CRR Article 4(146)). Group KM1 figures are a different entity and a different basis from this "
             "entity-only workbook and are deliberately NOT reproduced. See the source note for the quoted "
             "evidence and the editions checked.",
    rows=[
        ("DATA", "UK KM1 key-metrics template — Rathbones Investment Management Limited (entity)",
         {y: "Not applicable — published only at Rathbones Group Plc consolidated level" for y in YEARS}),
    ],
    sources_text=KM1_SOURCES,
    first_col_width=60,
    source_height=470,
)

_pillar3_pre = ["CET1 Capital", "CET1 Ratio", "Tier 1 Capital", "Tier 1 Ratio"]
_pillar3_post = ["Total Capital Ratio", "Total RWAs"]
_pillar3_after_rwa = ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"]
bw.add_not_disclosed_metric_sheets(_pillar3_pre, CASH_SOURCES, per_note={m: NOT_DISCLOSED for m in _pillar3_pre}, source_height=430)
bw.add_metric_sheet(
    "Total Capital",
    "£'000",
    [("Regulatory capital resources (own funds) — Company entity level",
      {"FY2025": 467062, "FY2024": 261190, "FY2023": 267182, "FY2022": 256378, "FY2021": 237897})],
    RCR_SOURCES,
    note="ENTITY-LEVEL own-funds total taken from the Company's own statutory accounts, not from a Pillar 3 "
         "template - Rathbones Group Plc's Pillar 3 is consolidated only and discloses nothing at this entity's "
         "level. No tier split or RWA accompanies it, so no ratio on this sheet or the Total Capital Ratio / Total "
         "RWAs sheets is derivable from it. The FY2024-to-FY2025 near-doubling is genuine and reflects the "
         "migration of Investec Wealth & Investment clients into this entity, which also drives the Balance Sheet "
         "and equity jump visible on the Overview sheet.",
    first_col_width=60,
    source_height=470,
)
bw.add_not_disclosed_metric_sheets(_pillar3_post, CASH_SOURCES, per_note={m: NOT_DISCLOSED for m in _pillar3_post}, source_height=430)
bw.add_rwa_breakdown_sheet(
    title="Rathbones Investment Management Limited — RWA Breakdown",
    subtitle="Not publicly disclosed at entity level.",
    rows=[("DATA", "RWA Breakdown", {y: "Not publicly disclosed" for y in YEARS})],
    sources_text=CASH_SOURCES,
    first_col_width=54,
    source_height=430,
    unit_suffix="",
)
bw.add_not_disclosed_metric_sheets(_pillar3_after_rwa, CASH_SOURCES, per_note={m: NOT_DISCLOSED for m in _pillar3_after_rwa}, source_height=430)

bw.add_overview_sheet(
    cash_flow_totals=[("Net cash inflow/(outflow) from operating activities", {"FY2025":988180,"FY2024":200256,"FY2023":-99468,"FY2022":276728,"FY2021":-249109}), ("Net cash used in investing activities", {"FY2025":-559268,"FY2024":-2375,"FY2023":-256406,"FY2022":-285059,"FY2021":-126903}), ("Cash and cash equivalents at the end of the year", {"FY2025":1609394,"FY2024":1249482,"FY2023":1078601,"FY2022":1484475,"FY2021":1530445})],
    cash_flow_unit=" (£'000)",
    ratios=[("CET1 Ratio", {})],
    balance_sheet_totals=[("Total assets", {"FY2025": 4809683, "FY2024": 3017731, "FY2023": 2845759, "FY2022": 3081068, "FY2021": 2843239}), ("Loans and advances to customers", {"FY2025": 206392, "FY2024": 124556, "FY2023": 131817, "FY2022": 205120, "FY2021": 194424}), ("Due to customers", {"FY2025": 3474635, "FY2024": 2540560, "FY2023": 2359342, "FY2022": 2622664, "FY2021": 2390232}), ("Total equity", {"FY2025": 1147348, "FY2024": 405212, "FY2023": 415845, "FY2022": 415887, "FY2021": 409920})],
    balance_sheet_unit=" (£'000)",
    income_statement_totals=[("Operating income", {"FY2025": 781638, "FY2024": 424964, "FY2023": 385751, "FY2022": 351147, "FY2021": 352939}), ("Operating expenses", {"FY2025": -670165, "FY2024": -403797, "FY2023": -321887, "FY2022": -301973, "FY2021": -277741}), ("Profit for the year", {"FY2025": 81117, "FY2024": 16367, "FY2023": 49958, "FY2022": 40967, "FY2021": 58964})],
    income_statement_unit=" (£'000)",
    equity_changes_totals=[("Opening equity", {"FY2025": 405212, "FY2024": 415845, "FY2023": 415887, "FY2022": 409920, "FY2021": 405956}), ("Total comprehensive income for the year", {"FY2025": 81117, "FY2024": 16367, "FY2023": 49958, "FY2022": 40967, "FY2021": 58964}), ("Closing equity", {"FY2025": 1147348, "FY2024": 405212, "FY2023": 415845, "FY2022": 415887, "FY2021": 409920})],
    equity_changes_unit=" (£'000)",
)
bw.save("/Users/armaan/code/katalysis/banks/RATHBONES INVESTMENT MANAGEMENT FINANCIALS.xlsx")
