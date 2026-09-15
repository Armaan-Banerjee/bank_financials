import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2017"]  # most recent first

CH2025_URL = "https://find-and-update.company-information.service.gov.uk/company/00819519/filing-history/MzUyMzkzMjQ5NmFkaXF6a2N4/document?format=pdf&download=0"
CH2023_URL = "https://find-and-update.company-information.service.gov.uk/company/00819519/filing-history/MzQyMzk5NjI0NGFkaXF6a2N4/document?format=pdf&download=0"
CH2021_URL = "https://find-and-update.company-information.service.gov.uk/company/00819519/filing-history/MzM0MTEwODM3MmFkaXF6a2N4/document?format=pdf&download=0"
AR2017_URL = "https://www.arbuthnotlatham.co.uk/sites/default/files/documents/ABG_Report_and_Accounts_Final_2017.pdf"

P3_H1_2026_URL = "https://www.arbuthnotlatham.co.uk/sites/default/files/documents/ABG-Pillar-3-Disclosures-2026-Interim.pdf"
P3_2024_URL = "https://www.arbuthnotlatham.co.uk/sites/default/files/documents/abg-pillar-3-disclosures-december-24.pdf"
P3_2023_URL = "https://www.arbuthnotlatham.co.uk/sites/default/files/documents/ABG_Pillar_3_Disclosures_2023_Final.pdf"
P3_2022_URL = "https://www.arbuthnotlatham.co.uk/sites/default/files/documents/ABG_Pillar_3_Disclosures_2022_Final.pdf"
P3_2021_URL = "https://www.arbuthnotlatham.co.uk/sites/default/files/documents/ABG_Pillar_3_Disclosures_2021_Annual.pdf"

ENTITY_NOTE = (
    "Entity note: Arbuthnot Latham & Co., Limited (company 00819519, FRN 143336) is the PRA-authorised Bank "
    "itself, not the wider LSE-listed ultimate holding company Arbuthnot Banking Group PLC. The Bank files its "
    "own 'Group of companies' accounts' at Companies House (Arbuthnot Latham & Co., Limited and its own "
    "subsidiaries - Wealth Management, Asset Finance, Asset Based Lending and Commercial Vehicle Finance), which "
    "is the basis used for the cash flow statement here. The Bank's Annual Report also states its own 'Group Key "
    "Metrics' (e.g. FY2024 Tier 1 capital ratio 13.3%, Total capital ratio 15.4%, LCR 179%), which differ "
    "slightly from the formal Pillar 3 disclosures published under the Arbuthnot Banking Group PLC name (FY2024 "
    "CET1/Tier 1 ratio 13.15%, Total capital ratio 15.28%, LCR 175%) - the Pillar 3 sheets in this workbook use "
    "the formal ABG PLC Pillar 3 (Article 447 CRR) disclosures, since that is the entity's actual published "
    "Pillar 3 document; the small basis difference vs. the Bank's own Annual Report figures is not explained in "
    "either source and is flagged here rather than silently blended.\n"
    "SDDT status (checked 2026-09-15): the PRA's consolidated register of waivers and modifications for "
    "PRA-regulated firms ('Consolidated Waivers list for PRA-regulated firms - as of 1 July 2026', "
    "bankofengland.co.uk/prudential-regulation/authorisations/waivers-and-modifications-of-rules) records that "
    "ARBUTHNOT LATHAM & CO., LIMITED (FRN 143336) holds a 'Modification by Consent - PRA Rulebook - CRR Firms - "
    "Rule 3.1 of the SDDT Regime - General Application Part', sub-rule 'Ru 3.1', with a start date of 02/03/2024 "
    "and no end date (still in force). That modification removes the Pillar 3 disclosure obligation outright, and "
    "is a different and stronger relief than UK CRR Article 433b, which merely reduces disclosure frequency and "
    "content for small and non-complex institutions - the two must not be conflated.\n"
    "Why that does NOT make the Pillar 3 sheets here structurally blank: the modification is held by the BANK "
    "(Arbuthnot Latham & Co., Limited, FRN 143336), whereas the Pillar 3 documents this workbook cites are "
    "published by the LSE-listed parent, Arbuthnot Banking Group PLC, which is not itself an SDDT and continues "
    "to disclose on a consolidated basis. ABG in fact published a Pillar 3 report for the six months ended 30 "
    "June 2026 - over two years after the Bank's opt-in - so the relief demonstrably was not used to stop group "
    "disclosure. The absence of a standalone FY2025 ANNUAL ABG Pillar 3 is therefore a reporting-cadence change "
    "(KM1 continues in the interim reports; the annual-only OV1 does not), not a structural exemption. Holding a "
    "Rule 3.1 modification is necessary but not sufficient evidence that a firm stopped disclosing, and it is "
    "not treated as sufficient here."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Arbuthnot Latham & Co., Limited's own Consolidated Statement of Cash Flows "
    "(the Bank + its own subsidiaries), £'000, as filed at Companies House:\n"
    f"FY2025 & FY2024: accounts made up to 31 December 2025, p.41 (Consolidated Statement of Cash Flows) - {CH2025_URL}\n"
    f"FY2023 & FY2022: accounts made up to 31 December 2023, p.42 (Consolidated Statement of Cash Flows) - {CH2023_URL}\n"
    f"FY2021 (& FY2020 comparative, not used): accounts made up to 31 December 2021, p.48 (Consolidated Statement "
    f"of Cash Flows) - {CH2021_URL}\n"
    "Presentation note: FY2021's own report builds the operating-profit-before-changes subtotal from actual cash "
    "interest/fee/payment flows (Interest received, Interest paid, Fees and commissions received, Other income, "
    "Cash payments to employees and suppliers, Taxation paid); FY2022 onward builds the same subtotal indirectly "
    "from Profit before tax plus non-cash adjustments (Depreciation, Impairment, Net interest expense, FX "
    "elimination on debt securities, Other non-cash items, Tax paid/expense). Both bases reconcile to a "
    "consistent, comparable 'Cash flows from operating profit before changes in operating assets and liabilities' "
    "subtotal each year - blank cells simply mean that year's report used the other presentation. FY2025's "
    "investing-activities total has an immaterial £1k rounding gap vs. the sum of its own printed line items, "
    "kept as printed rather than force-corrected. Every other section total and the full opening/closing cash "
    "chain reconciles exactly year-to-year across all 3 source documents.\n"
    + ENTITY_NOTE
)


def p3_sources(page_24="6", page_23="6", page_22="6", page_21="31", page_h1_26="4"):
    return (
        "Sources - Arbuthnot Banking Group PLC Pillar 3 disclosures (UK KM1 Key Metrics template; FY2021 uses the "
        "pre-KM1 'Key Regulatory Metrics' template), £'000 unless stated:\n"
        f"FY2025: Pillar 3 disclosures for the six months ended 30 June 2026, p.{page_h1_26} (Template UK KM1), "
        f"column c '31-Dec-25' - {P3_H1_2026_URL}\n"
        f"FY2024 & FY2023 comparative: Pillar 3 disclosures for the year ended 31 December 2024, p.{page_24} (Template UK KM1) - {P3_2024_URL}\n"
        f"FY2023 (own year) & FY2022 comparative: Pillar 3 disclosures for the year ended 31 December 2023, p.{page_23} (Template UK KM1) - {P3_2023_URL}\n"
        f"FY2022 (own year) & FY2021 comparative: Pillar 3 disclosures for the year ended 31 December 2022, p.{page_22} (Template UK KM1) - {P3_2022_URL}\n"
        f"FY2021 (own year): Pillar 3 disclosures for the year ended 31 December 2021, p.{page_21} (Key Regulatory Metrics) - {P3_2021_URL}\n"
        "FY2025 sourcing note: ABG has not published a standalone FY2025 ANNUAL Pillar 3 report (every plausible "
        "filename under the site's prior-year patterns returns 404, and the Wayback CDX index for the domain lists "
        "no 2025 annual document). The 31 December 2025 figures here are instead taken from the 30 June 2026 "
        "INTERIM Pillar 3 report, whose UK KM1 template carries 31-Dec-25 as its column c comparative. That "
        "document footnotes the column '* Includes year end verified reserves', i.e. it is the audited year-end "
        "position rather than an interim estimate. The same document's 30-Jun-25 column and the equivalent 30 June "
        "2025 interim report's 31-Dec-24 column were used to verify the reading: every FY2024 figure recovered that "
        "way (CET1 £234,477k, Total capital £272,459k, RWAs £1,782,645k, CET1/Tier 1 ratio 13.15%, Total capital "
        "ratio 15.28%, leverage exposure £3,828,489k / 6.12%, LCR HQLA £1,275,612k / net outflows £730,580k / 175%, "
        "NSFR ASF £2,995,437k / RSF £2,274,318k / 132%) matches the FY2024 annual report's own figures exactly, so "
        "the interim KM1 is on an identical basis, not a different one.\n"
        + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="Arbuthnot Latham & Co., Limited", years=YEARS, header_color="4E3B31")

STATEMENT_SOURCES_HEAD = (
    "Sources - all figures are Arbuthnot Latham & Co., Limited's own Consolidated financial statements "
    "(the Bank + its own subsidiaries), £'000, as filed at Companies House:\n"
    f"FY2025 & FY2024: accounts made up to 31 December 2025, Consolidated Statement of Financial Position/"
    f"Comprehensive Income/Changes in Equity, pp.36-40 - {CH2025_URL}\n"
    f"FY2023 & FY2022: accounts made up to 31 December 2023, same statements, pp.37-40 - {CH2023_URL}\n"
    f"FY2021 (& FY2020 comparative, not used): accounts made up to 31 December 2021, same statements, "
    f"pp.43-46 - {CH2021_URL}\n"
)

# ---------------------------------------------------------------
# Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 437548, "FY2024": 911887, "FY2023": 826559, "FY2022": 732728, "FY2021": 814692}),
    ("DATA", "Loans and advances to banks", {"FY2025": 117491, "FY2024": 66964, "FY2023": 79374, "FY2022": 115781, "FY2021": 73430}),
    ("DATA", "Debt securities at amortised cost", {"FY2025": 2033158, "FY2024": 1199847, "FY2023": 942437, "FY2022": 439753, "FY2021": 301052}),
    ("DATA", "Assets classified as held for sale", {"FY2023": 3281, "FY2022": 3279, "FY2021": 3136}),
    ("DATA", "Derivative financial instruments", {"FY2025": 1398, "FY2024": 2970, "FY2023": 4214, "FY2022": 6322, "FY2021": 1753}),
    ("DATA", "Loans and advances to customers", {"FY2025": 1960552, "FY2024": 2094226, "FY2023": 2064256, "FY2022": 2047578, "FY2021": 1882461}),
    ("DATA", "Current tax assets", {"FY2025": 7010, "FY2024": 1287, "FY2023": 2347}),
    ("DATA", "Other assets", {"FY2025": 50176, "FY2024": 51623, "FY2023": 57092, "FY2022": 52110, "FY2021": 110065}),
    ("DATA", "Financial investments", {"FY2025": 2061, "FY2024": 4947, "FY2023": 3942, "FY2022": 3404, "FY2021": 3169}),
    ("DATA", "Deferred tax asset", {"FY2022": 1902, "FY2021": 2040}),
    ("DATA", "Intangible assets", {"FY2025": 37179, "FY2024": 34299, "FY2023": 33320, "FY2022": 36281, "FY2021": 33595}),
    ("DATA", "Property, plant and equipment", {"FY2025": 310375, "FY2024": 313147, "FY2023": 274176, "FY2022": 175144, "FY2021": 125753}),
    ("DATA", "Right-of-use assets", {"FY2025": 44502, "FY2024": 47511, "FY2023": 52816, "FY2022": 7714, "FY2021": 15675}),
    ("DATA", "Investment property", {"FY2025": 5250, "FY2024": 5250, "FY2023": 5950, "FY2022": 6550, "FY2021": 6550}),
    ("TOTAL", "Total assets", {"FY2025": 5006700, "FY2024": 4733958, "FY2023": 4349764, "FY2022": 3628546, "FY2021": 3373371}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks", {"FY2025": 1389, "FY2024": 192911, "FY2023": 193410, "FY2022": 236027, "FY2021": 240333}),
    ("DATA", "Derivative financial instruments", {"FY2023": 1032, "FY2022": 135, "FY2021": 171}),
    ("DATA", "Deposits from customers", {"FY2025": 4575114, "FY2024": 4133406, "FY2023": 3760199, "FY2022": 3112478, "FY2021": 2856949}),
    ("DATA", "Current tax liability", {"FY2022": 870, "FY2021": 652}),
    ("DATA", "Other liabilities", {"FY2025": 39960, "FY2024": 34750, "FY2023": 38117, "FY2022": 24189, "FY2021": 19598}),
    ("DATA", "Lease liabilities", {"FY2025": 58266, "FY2024": 54829, "FY2023": 53761, "FY2022": 7873, "FY2021": 21277}),
    ("DATA", "Deferred tax liability", {"FY2025": 10743, "FY2024": 6186, "FY2023": 5430}),
    ("DATA", "Debt securities in issue", {"FY2025": 38781, "FY2024": 38103, "FY2023": 38129, "FY2022": 24437, "FY2021": 24367}),
    ("TOTAL", "Total liabilities", {"FY2025": 4724253, "FY2024": 4460185, "FY2023": 4090078, "FY2022": 3406009, "FY2021": 3163347}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 15000, "FY2024": 15000, "FY2023": 15000, "FY2022": 15000, "FY2021": 15000}),
    ("DATA", "Retained earnings", {"FY2025": 115767, "FY2024": 105372, "FY2023": 91832, "FY2022": 59957, "FY2021": 47533}),
    ("DATA", "Other reserves (capital contribution + fair value reserve)", {"FY2025": 151680, "FY2024": 153401, "FY2023": 152854, "FY2022": 147580, "FY2021": 147491}),
    ("TOTAL", "Total equity", {"FY2025": 282447, "FY2024": 273773, "FY2023": 259686, "FY2022": 222537, "FY2021": 210024}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 5006700, "FY2024": 4733958, "FY2023": 4349764, "FY2022": 3628546, "FY2021": 3373371}),
]

BALANCE_SHEET_SOURCES = (
    STATEMENT_SOURCES_HEAD +
    "Presentation note: 'Assets classified as held for sale' and 'Current tax liability' are only disclosed as "
    "separate lines FY2021-FY2023; FY2025-FY2024's own statements omit or fold them elsewhere (immaterial/"
    "reclassified per those years' own reports, not explained further in either source). 'Deferred tax asset' is "
    "only a separate line FY2021-FY2022; 'Deferred tax liability' and 'Current tax assets' only appear from "
    "FY2023/FY2025 respectively. 'Derivative financial instruments' appears as a liability line only FY2021-"
    "FY2023 - FY2024-FY2025's own statements show no separate derivative liability line (netted/immaterial per "
    "those years, not explained further). Blank cells reflect each year's own statement structure, not missing "
    "data. 'Other reserves' is shown here as a single combined line (capital contribution reserve + fair value "
    "reserve) to match each year's own Statement of Financial Position; see the Statement of Changes in Equity "
    "sheet for the two components separately.\n"
    + ENTITY_NOTE
)

bw.add_balance_sheet_sheet(
    title="Arbuthnot Latham & Co., Limited — Consolidated Statement of Financial Position",
    subtitle="Arbuthnot Latham & Co., Limited Group (consolidated basis), £'000",
    rows=balance_sheet_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=64,
    source_height=190,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Operating income from banking activities", {}),
    ("DATA", "Interest income", {"FY2025": 247248, "FY2024": 263435, "FY2023": 231836, "FY2022": 120013, "FY2021": 77102}),
    ("DATA", "Interest expense", {"FY2025": -129126, "FY2024": -137562, "FY2023": -90515, "FY2022": -17781, "FY2021": -10384}),
    ("TOTAL", "Net interest income", {"FY2025": 118122, "FY2024": 125873, "FY2023": 141321, "FY2022": 102232, "FY2021": 66718}),
    ("DATA", "Fee and commission income", {"FY2025": 31689, "FY2024": 29142, "FY2023": 23170, "FY2022": 21586, "FY2021": 18472}),
    ("DATA", "Fee and commission expense", {"FY2025": -1444, "FY2024": -1029, "FY2023": -768, "FY2022": -537, "FY2021": -349}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 30245, "FY2024": 28113, "FY2023": 22402, "FY2022": 21049, "FY2021": 18123}),
    ("TOTAL", "Operating income from banking activities", {"FY2025": 148367, "FY2024": 153986, "FY2023": 163723, "FY2022": 123281, "FY2021": 84841}),
    ("SECTION", "Income from leasing activities", {}),
    ("DATA", "Revenue", {"FY2025": 118569, "FY2024": 110832, "FY2023": 100952, "FY2022": 99367, "FY2021": 74500}),
    ("DATA", "Cost of goods sold", {"FY2025": -97466, "FY2024": -85301, "FY2023": -81074, "FY2022": -82109, "FY2021": -68027}),
    ("TOTAL", "Gross profit from leasing activities", {"FY2025": 21103, "FY2024": 25531, "FY2023": 19878, "FY2022": 17258, "FY2021": 6473}),
    ("TOTAL", "Total group operating income", {"FY2025": 169470, "FY2024": 179517, "FY2023": 183601, "FY2022": 140539, "FY2021": 91314}),
    ("DATA", "Impairment loss on financial assets", {"FY2025": -2501, "FY2024": -6275, "FY2023": -3191, "FY2022": -5503, "FY2021": -3196}),
    ("DATA", "Other income", {"FY2025": 5536, "FY2024": 2560, "FY2023": 3361, "FY2022": 2467, "FY2021": 4402}),
    ("DATA", "Profit from bargain purchase", {"FY2021": 8626}),
    ("DATA", "Loss on sale of commercial property held as inventory", {"FY2022": -4590}),
    ("DATA", "Operating expenses", {"FY2025": -148321, "FY2024": -140712, "FY2023": -136655, "FY2022": -112904, "FY2021": -96512}),
    ("TOTAL", "Profit/(loss) before tax", {"FY2025": 24184, "FY2024": 35090, "FY2023": 47116, "FY2022": 20009, "FY2021": 4634}),
    ("DATA", "Income tax (expense)/credit", {"FY2025": -2119, "FY2024": -5339, "FY2023": -8433, "FY2022": -2146, "FY2021": 2157}),
    ("TOTAL", "Profit/(loss) for the year", {"FY2025": 22065, "FY2024": 29751, "FY2023": 38683, "FY2022": 17863, "FY2021": 6791}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Movement in fair value reserve", {"FY2025": -59, "FY2024": 778, "FY2023": 412, "FY2022": 628, "FY2021": 763}),
    ("DATA", "Tax on other comprehensive income", {"FY2025": 15, "FY2024": -182, "FY2023": -91, "FY2022": -128, "FY2021": -124}),
    ("TOTAL", "Other comprehensive income for the period, net of tax", {"FY2025": -44, "FY2024": 596, "FY2023": 321, "FY2022": 499, "FY2021": 639}),
    ("TOTAL", "Total comprehensive income for the period", {"FY2025": 22021, "FY2024": 30347, "FY2023": 39004, "FY2022": 18363, "FY2021": 7430}),
]

INCOME_STATEMENT_SOURCES = (
    STATEMENT_SOURCES_HEAD +
    "Presentation note: FY2021 uniquely includes a 'Profit from bargain purchase' line (£8,626k, the AAG "
    "acquisition) and reports an income tax CREDIT (positive); FY2022 uniquely includes a 'Loss on sale of "
    "commercial property held as inventory' line. All other years leave these blank rather than showing zero. "
    "'Sale of financial assets carried at FVOCI' (a reclassification between Retained earnings and the Fair "
    "value reserve, disclosed in the equity statement) is not shown here - it nets to zero on total comprehensive "
    "income and is a transfer within equity rather than a P&L income/expense item.\n"
    + ENTITY_NOTE
)

bw.add_income_statement_sheet(
    title="Arbuthnot Latham & Co., Limited — Consolidated Statement of Comprehensive Income",
    subtitle="Arbuthnot Latham & Co., Limited Group (consolidated basis), £'000",
    rows=income_statement_rows,
    sources_text=INCOME_STATEMENT_SOURCES,
    first_col_width=64,
    source_height=170,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Share capital", "Retained earnings", "Capital contribution reserve", "Fair value reserve", "Total equity"]

equity_changes_rows = [
    ("TOTAL", "Balance at 1 January 2021", (15000, 46835, 121012, -203, 182644)),
    ("DATA", "Profit for 2021", (None, 6791, None, None, 6791)),
    ("DATA", "Fair value reserve - net change in fair value", (None, None, None, 637, 637)),
    ("DATA", "Tax on other comprehensive income", (None, None, None, 2, 2)),
    ("TOTAL", "Total comprehensive income for 2021", (None, 6791, None, 639, 7430)),
    ("DATA", "Capital contribution", (None, None, 25500, None, 25500)),
    ("DATA", "Loss on disposal of assets held at FVOCI", (None, -543, None, 543, 0)),
    ("DATA", "Interim dividend relating to 2021", (None, -5550, None, None, -5550)),
    ("TOTAL", "Total contributions by and distributions to owners", (None, -6093, 25500, 543, 19950)),
    ("TOTAL", "Balance at 31 December 2021", (15000, 47533, 146512, 979, 210024)),
    ("DATA", "Profit for 2022", (None, 17863, None, None, 17863)),
    ("DATA", "Fair value reserve - net change in fair value", (None, None, None, 628, 628)),
    ("DATA", "Sale of financial assets carried at FVOCI", (None, 411, None, -411, 0)),
    ("DATA", "Tax on other comprehensive income", (None, None, None, -128, -128)),
    ("TOTAL", "Total comprehensive income for 2022", (None, 18274, None, 89, 18363)),
    ("DATA", "Final dividend relating to 2021", (None, -3300, None, None, -3300)),
    ("DATA", "Interim dividend relating to 2022", (None, -2550, None, None, -2550)),
    ("TOTAL", "Total contributions by and distributions to owners", (None, -5850, None, None, -5850)),
    ("TOTAL", "Balance at 31 December 2022", (15000, 59957, 146512, 1068, 222537)),
    ("DATA", "Profit for 2023", (None, 38683, None, None, 38683)),
    ("DATA", "Fair value reserve - net change in fair value", (None, None, None, 412, 412)),
    ("DATA", "Sale of financial assets carried at FVOCI", (None, 47, None, -47, 0)),
    ("DATA", "Tax on other comprehensive income", (None, None, None, -91, -91)),
    ("TOTAL", "Total comprehensive income for 2023", (None, 38730, None, 274, 39004)),
    ("DATA", "Capital contribution", (None, None, 5000, None, 5000)),
    ("DATA", "Final dividend relating to 2022", (None, -3755, None, None, -3755)),
    ("DATA", "Interim dividend relating to 2023", (None, -3100, None, None, -3100)),
    ("TOTAL", "Total contributions by and distributions to owners", (None, -6855, 5000, None, -1855)),
    ("TOTAL", "Balance at 31 December 2023", (15000, 91832, 151512, 1342, 259686)),
    ("DATA", "Profit for 2024", (None, 29751, None, None, 29751)),
    ("DATA", "Fair value reserve - net change in fair value", (None, None, None, 778, 778)),
    ("DATA", "Sale of financial assets carried at FVOCI", (None, 49, None, -49, 0)),
    ("DATA", "Tax on other comprehensive income", (None, None, None, -182, -182)),
    ("TOTAL", "Total comprehensive income for 2024", (None, 29800, None, 547, 30347)),
    ("DATA", "Final dividend relating to 2023", (None, -4407, None, None, -4407)),
    ("DATA", "Interim dividend relating to 2024", (None, -11853, None, None, -11853)),
    ("TOTAL", "Total contributions by and distributions to owners", (None, -16260, None, None, -16260)),
    ("TOTAL", "Balance at 31 December 2024", (15000, 105372, 151512, 1889, 273773)),
    ("DATA", "Profit for 2025", (None, 22065, None, None, 22065)),
    ("DATA", "Fair value reserve - net change in fair value", (None, None, None, -59, -59)),
    ("DATA", "Sale of financial assets carried at FVOCI", (None, 1677, None, -1677, 0)),
    ("DATA", "Tax on other comprehensive income", (None, None, None, 15, 15)),
    ("TOTAL", "Total comprehensive income for 2025", (None, 23742, None, -1721, 22021)),
    ("DATA", "Final dividend relating to 2024", (None, -7611, None, None, -7611)),
    ("DATA", "Interim dividends relating to 2025", (None, -5736, None, None, -5736)),
    ("TOTAL", "Total contributions by and distributions to owners", (None, -13347, None, None, -13347)),
    ("TOTAL", "Balance at 31 December 2025", (15000, 115767, 151512, 168, 282447)),
]

EQUITY_CHANGES_SOURCES = (
    "Sources - Arbuthnot Latham & Co., Limited's own Consolidated Statement of Changes in Equity (the Bank + "
    "its own subsidiaries), £'000, as filed at Companies House:\n"
    f"1 Jan 2021 - 31 Dec 2023: accounts made up to 31 December 2023, pp.39-40 - {CH2023_URL}\n"
    f"31 Dec 2023 - 31 Dec 2025: accounts made up to 31 December 2025, p.39 - {CH2025_URL}\n"
    f"1 Jan 2020 - 31 Dec 2021 (opening balance): accounts made up to 31 December 2021, p.46 - {CH2021_URL}\n"
    "'Other reserves' on the Balance Sheet sheet is the sum of the 'Capital contribution reserve' and 'Fair "
    "value reserve' columns here. Chronological, oldest-to-newest, unlike the year-column shape used elsewhere "
    "in this workbook - see the sheet's own column headers.\n"
    + ENTITY_NOTE
)

bw.add_equity_changes_sheet(
    title="Arbuthnot Latham & Co., Limited — Consolidated Statement of Changes in Equity",
    subtitle="Arbuthnot Latham & Co., Limited Group (consolidated basis), £'000",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQUITY_CHANGES_SOURCES,
    first_col_width=52,
    source_height=180,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit before tax", {"FY2025": 24184, "FY2024": 35091, "FY2023": 47117, "FY2022": 20009}),
    ("DATA", "Interest received", {"FY2021": 77319}),
    ("DATA", "Interest paid", {"FY2021": -11752}),
    ("DATA", "Fees and commissions received", {"FY2021": 15579}),
    ("DATA", "Other income", {"FY2021": 4402}),
    ("DATA", "Cash payments to employees and suppliers", {"FY2021": -59153}),
    ("DATA", "Taxation paid", {"FY2021": 0}),
    ("DATA", "Depreciation and amortisation", {"FY2025": 10674, "FY2024": 11691, "FY2023": 9817, "FY2022": 7180}),
    ("DATA", "Impairment loss on loans and advances", {"FY2025": 1576, "FY2024": 4778, "FY2023": 208, "FY2022": 214}),
    ("DATA", "Net interest expense", {"FY2025": 3203, "FY2024": 598, "FY2023": 564, "FY2022": 70}),
    ("DATA", "Elimination of exchange differences on debt securities", {"FY2025": 11337, "FY2024": -3157, "FY2023": 8712, "FY2022": -9524}),
    ("DATA", "Other non-cash or non-operating items included in profit before tax", {"FY2025": 3402, "FY2024": -73, "FY2023": 31, "FY2022": -276}),
    ("DATA", "Tax paid/(expense)", {"FY2025": -6690, "FY2024": -4150, "FY2023": -8433, "FY2022": -2146}),
    ("TOTAL", "Cash flows from operating profit before changes in operating assets and liabilities", {"FY2025": 47686, "FY2024": 44778, "FY2023": 58016, "FY2022": 15527, "FY2021": 26395}),
    ("SECTION", "Changes in operating assets and liabilities", {}),
    ("DATA", "Net decrease/(increase) in derivative financial instruments", {"FY2025": 1572, "FY2024": 212, "FY2023": 3005, "FY2022": -4605, "FY2021": -388}),
    ("DATA", "Net decrease/(increase) in loans and advances to customers", {"FY2025": 132098, "FY2024": -34748, "FY2023": -16886, "FY2022": -165331, "FY2021": -284871}),
    ("DATA", "Net decrease/(increase) in assets held for leasing", {"FY2025": 721, "FY2024": -18474, "FY2023": -95960, "FY2022": -50175}),
    ("DATA", "Net increase/(decrease) in other assets", {"FY2025": 1447, "FY2024": 12828, "FY2023": -4063, "FY2022": 57955, "FY2021": -12558}),
    ("DATA", "Net increase in amounts due to customers", {"FY2025": 441708, "FY2024": 373207, "FY2023": 647721, "FY2022": 255529, "FY2021": 465088}),
    ("DATA", "Net increase/(decrease) in other liabilities", {"FY2025": 5211, "FY2024": -3369, "FY2023": 18490, "FY2022": 4593, "FY2021": 12651}),
    ("TOTAL", "Net cash inflow from operating activities", {"FY2025": 630443, "FY2024": 374434, "FY2023": 610323, "FY2022": 113493, "FY2021": 206317}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Acquisition of financial investments", {"FY2025": -131, "FY2024": -215, "FY2023": -174, "FY2022": -53}),
    ("DATA", "Disposal of financial investments", {"FY2025": 2958, "FY2024": 84, "FY2023": 63, "FY2022": 640, "FY2021": 2400}),
    ("DATA", "Purchase of subsidiary undertakings", {"FY2021": -9998}),
    ("DATA", "Purchase of intangible assets / computer software", {"FY2025": -6425, "FY2024": -4739, "FY2023": -1523, "FY2022": -5837, "FY2021": -5100}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -985, "FY2024": -22808, "FY2023": -4611, "FY2022": -1065, "FY2021": -172915}),
    ("DATA", "Proceeds from sale of property, plant and equipment", {"FY2021": 48255}),
    ("DATA", "Disposal of assets held for sale", {"FY2021": 149}),
    ("DATA", "Purchase of debt securities", {"FY2025": -3273055, "FY2024": -1621196, "FY2023": -1582889, "FY2022": -799341, "FY2021": -590492}),
    ("DATA", "Proceeds from redemption of debt securities", {"FY2025": 2428998, "FY2024": 1366350, "FY2023": 1071232, "FY2022": 670164, "FY2021": 635155}),
    ("DATA", "Dividends received", {"FY2025": 18}),
    ("TOTAL", "Net cash outflow from investing activities", {"FY2025": -848623, "FY2024": -282524, "FY2023": -517902, "FY2022": -135492, "FY2021": -92546}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "(Decrease)/increase in borrowings", {"FY2025": -191522, "FY2024": -530, "FY2023": -29489, "FY2022": -4306, "FY2021": 10243}),
    ("DATA", "Dividends paid", {"FY2025": -13347, "FY2024": -16260, "FY2023": -6855, "FY2022": -5850, "FY2021": -5550}),
    ("DATA", "Capital contribution received", {"FY2023": 5000, "FY2021": 25500}),
    ("DATA", "Repayment of lease liabilities", {"FY2025": -763, "FY2024": -2202, "FY2023": -3653, "FY2022": -7458, "FY2021": -2893}),
    ("TOTAL", "Net cash (outflow)/inflow from financing activities", {"FY2025": -205632, "FY2024": -18992, "FY2023": -34997, "FY2022": -17614, "FY2021": 27300}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -423812, "FY2024": 72918, "FY2023": 57424, "FY2022": -39613, "FY2021": 141071}),
    ("DATA", "Cash and cash equivalents at 1 January", {"FY2025": 978851, "FY2024": 905933, "FY2023": 848509, "FY2022": 888122, "FY2021": 747051}),
    ("TOTAL", "Cash and cash equivalents at 31 December", {"FY2025": 555039, "FY2024": 978851, "FY2023": 905933, "FY2022": 848509, "FY2021": 888122}),
]

bw.add_cash_flow_sheet(
    title="Arbuthnot Latham & Co., Limited — Consolidated Cash Flow Statement",
    subtitle="Arbuthnot Latham & Co., Limited Group (consolidated basis), £'000",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=72,
    source_height=170,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Asset Quality / Credit Risk Disclosures
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loan book by IFRS 9 stage (gross of ECL)", {}),
    ("DATA", "Stage 1", {"FY2025": 1856653, "FY2024": 1929191, "FY2023": 1908981, "FY2022": 1929390}),
    ("DATA", "Stage 2", {"FY2025": 53383, "FY2024": 103275, "FY2023": 82751, "FY2022": 74512}),
    ("DATA", "Stage 3", {"FY2025": 63677, "FY2024": 73349, "FY2023": 79332, "FY2022": 50278}),
    ("TOTAL", "Loans and advances to customers (gross of ECL)", {"FY2025": 1973713, "FY2024": 2105815, "FY2023": 2071064, "FY2022": 2054180, "FY2021": 1888848}),
    ("SECTION", "Expected credit loss (ECL) allowance", {}),
    ("DATA", "Stage 1", {"FY2021": 388}),
    ("DATA", "Stage 2", {"FY2021": 77}),
    ("DATA", "Stage 3", {"FY2021": 5922}),
    ("TOTAL", "Total ECL allowance", {"FY2025": 13161, "FY2024": 11589, "FY2023": 6808, "FY2022": 6602, "FY2021": 6387}),
    ("SECTION", "Asset quality ratios", {}),
    ("DATA", "Stage 3 / NPL ratio (Stage 3 gross / total gross loans)", {"FY2025": "3.23%", "FY2024": "3.48%", "FY2023": "3.83%", "FY2022": "2.45%"}),
    ("DATA", "ECL coverage ratio (total ECL / total gross loans)", {"FY2025": "0.67%", "FY2024": "0.55%", "FY2023": "0.33%", "FY2022": "0.32%", "FY2021": "0.34%"}),
]

ASSET_QUALITY_SOURCES = (
    "Sources - Arbuthnot Latham & Co., Limited's own Note 6(a) 'Credit risk' (maximum credit risk exposure "
    "table, Group basis), £'000:\n"
    f"FY2025 & FY2024: accounts made up to 31 December 2025, pp.61-62 - {CH2025_URL}\n"
    f"FY2023 & FY2022: accounts made up to 31 December 2023, pp.62-63 - {CH2023_URL}\n"
    f"FY2021 ECL allowance by stage only (Note 4.1(a)): accounts made up to 31 December 2021, p.60 - {CH2021_URL}\n"
    "All 4 source documents are scanned/image-only PDFs (no extractable text layer) - figures were visually "
    "transcribed from rendered page images (pdf_tools.py render + Read), not OCR'd or estimated.\n"
    "Gaps, documented rather than guessed: (1) FY2021's gross Stage 1/2/3 loan-book split was not located - only "
    "the ECL allowance by stage (Note 4.1(a)) was found for that year, so the Stage 3/NPL ratio is left blank "
    "for FY2021 while the ECL coverage ratio (which only needs the ECL total, not its stage split) is still "
    "computable; FY2021's gross total loan figure shown here is DERIVED (Balance Sheet net loans £1,882,461k + "
    "ECL allowance £6,387k = £1,888,848k), not a directly disclosed figure. (2) A loan-book-by-product/"
    "collateral-type breakdown exists in the FY2025 Annual Report (concentration by collateral type, Note 6(a)) "
    "but was not transcribed this session - the IFRS 9 stage breakdown above is the sheet's primary content per "
    "its own convention; a future session could add the by-product view if wanted.\n"
    + ENTITY_NOTE
)

bw.add_asset_quality_sheet(
    title="Arbuthnot Latham & Co., Limited — Asset Quality / Credit Risk Disclosures",
    subtitle="Arbuthnot Latham & Co., Limited Group (consolidated basis), £'000 unless stated",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=62,
    source_height=210,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Arbuthnot Banking Group PLC (Pillar 3) basis, {unit}" if unit else "Arbuthnot Banking Group PLC (Pillar 3) basis",
                         rows_data, sources_text, note=note, first_col_width=46, source_height=140)

metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 241598, "FY2024": 234477, "FY2023": 222291, "FY2022": 175375, "FY2021": 176235})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 ratio", {"FY2025": "13.26%", "FY2024": "13.15%", "FY2023": "12.98%", "FY2022": "11.57%", "FY2021": "12.3%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2025": 241598, "FY2024": 234477, "FY2023": 222291, "FY2022": 175375, "FY2021": 176235})],
    p3_sources(),
    note="Equal to CET1 capital every year - no AT1 instruments in issue.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "13.26%", "FY2024": "13.15%", "FY2023": "12.98%", "FY2022": "11.57%", "FY2021": "12.3%"})],
    p3_sources(),
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2025": 280270, "FY2024": 272459, "FY2023": 260017, "FY2022": 212969, "FY2021": 213007})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "15.38%", "FY2024": "15.28%", "FY2023": "15.18%", "FY2022": "14.05%", "FY2021": "14.9%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted exposure amount", {"FY2025": 1822551, "FY2024": 1782645, "FY2023": 1713146, "FY2022": 1516141, "FY2021": 1427724})],
    p3_sources(),
)

rwa_breakdown_rows = [
    ("SECTION", "Risk weighted exposure amounts (Template UK OV1)", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2024": 1525678, "FY2023": 1511071, "FY2022": 1333060, "FY2021": 1257789}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2024": 741, "FY2023": 2250, "FY2022": 13540, "FY2021": 2911}),
    ("DATA", "Market risk (position, FX and commodities)", {"FY2024": 1376, "FY2023": 3727, "FY2022": 3753, "FY2021": 7527}),
    ("DATA", "Operational risk", {"FY2024": 254850, "FY2023": 196098, "FY2022": 165788, "FY2021": 159498}),
    ("TOTAL", "Total risk-weighted exposure amount", {"FY2024": 1782645, "FY2023": 1713146, "FY2022": 1516141, "FY2021": 1427725}),
]

RWA_BREAKDOWN_SOURCES = (
    p3_sources(page_24="7", page_23="15", page_22="16", page_21="6") +
    "\nFY2025 is blank on this sheet even though the Total RWAs sheet carries an FY2025 figure. This is a real "
    "scope difference, not a missing transcription: ABG discloses as an SDDT, and the 30 June 2026 interim Pillar "
    "3 report (the source of the FY2025 KM1 headline) states in its own scope section that the Article 438(d) "
    "'Own Funds Requirements and Risk-Weighted Exposure Amounts' template (UK OV1) is disclosed only 'On an annual "
    "basis'. The interim report therefore contains KM1 but no OV1, and no FY2025 annual Pillar 3 report has been "
    "published. The FY2025 RWA split will only become available with that annual document.\n"
    "FY2021's Total row (£1,427,725k) is £1k higher than the Total RWAs sheet's own FY2021 figure "
    "(£1,427,724k) - both are read directly off their respective source tables (the OV1 breakdown here vs. the "
    "KM1 headline total there); an immaterial rounding gap between the two templates in ABG's own Pillar 3 "
    "reports, not corrected here."
)

bw.add_rwa_breakdown_sheet(
    title="Arbuthnot Latham & Co., Limited — RWA Breakdown",
    subtitle="Arbuthnot Banking Group PLC (Pillar 3) basis, £'000",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=54,
    source_height=170,
    unit_suffix=" (£'000)",
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Total exposure measure excluding claims on central banks", {"FY2025": 4568671, "FY2024": 3828489, "FY2023": 3559597, "FY2022": 2923193}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "5.29%", "FY2024": "6.12%", "FY2023": "6.24%", "FY2022": "6.00%"}),
        ("Total Basel III leverage ratio measure (FY2021 basis, includes claims on central banks)", {"FY2021": 3409123}),
        ("Basel III leverage ratio (%) (FY2021 basis)", {"FY2021": "5.2%"}),
    ],
    p3_sources(),
    note="The 'excluding claims on central banks' leverage framework took effect from 1 January 2022 (per the "
         "FY2022 Pillar 3 report itself); FY2021 is shown on its own report's 'Basel III leverage ratio' basis "
         "(includes claims on central banks) as a separate row rather than blended with the later basis.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value", {"FY2025": 1891643, "FY2024": 1275612, "FY2023": 1046604, "FY2022": 710180, "FY2021": 897493}),
        ("Total net cash outflows, adjusted value", {"FY2025": 994752, "FY2024": 730580, "FY2023": 476548, "FY2022": 405819, "FY2021": 487009}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "190%", "FY2024": "175%", "FY2023": "220%", "FY2022": "175%", "FY2021": "184.3%"}),
    ],
    p3_sources(),
    note="FY2021 figures are from the FY2021 report's own 'Key Regulatory Metrics' table (pre-KM1 format). The "
         "FY2022 Pillar 3 report's own Dec-2021 comparative column instead shows HQLA £776,633k, net cash "
         "outflows £354,918k and LCR 219% for the same date - a real discrepancy between the two vintages' own "
         "figures, not resolved in either source. The FY2021 standalone figure is used here as the year's own "
         "original disclosure; the later restated comparative is flagged here rather than silently substituted.",
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding", {"FY2025": 3126629, "FY2024": 2995437, "FY2023": 2784678, "FY2022": 2464147, "FY2021": 2389237}),
        ("Total required stable funding", {"FY2025": 2058754, "FY2024": 2274318, "FY2023": 2043499, "FY2022": 1940538, "FY2021": 1794905}),
        ("NSFR ratio (%)", {"FY2025": "152%", "FY2024": "132%", "FY2023": "136%", "FY2022": "127%", "FY2021": "133.1%"}),
    ],
    p3_sources(),
    note="FY2021 is from the FY2021 report's own table; the UK NSFR regime's KM1 disclosure only became a formal "
         "requirement from 1 January 2022, so the FY2022 Pillar 3 report's KM1 template carries no FY2021 "
         "comparative for this line (marked 'NA' in that document) even though FY2021's own report did disclose "
         "a figure.",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not disclosed" for y in YEARS})],
    p3_sources(),
    note="No MREL disclosure found in any of the available Pillar 3 reports (FY2021-FY2024 annual, plus the 2025 "
         "and 2026 interim reports) - Arbuthnot Banking Group is not designated as a resolution entity subject to "
         "MREL reporting at this level. The 30 June 2026 interim report states this directly: the Article 447(h) "
         "own funds and eligible liabilities ratios are calculated under CRR Articles 92a/92b, which 'only apply "
         "to G-SIIs and so are not applicable to the Group'.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 5006700, "FY2024": 4733958, "FY2023": 4349764, "FY2022": 3628546, "FY2021": 3373371}),
        ("Loans and advances to customers", {"FY2025": 1960552, "FY2024": 2094226, "FY2023": 2064256, "FY2022": 2047578, "FY2021": 1882461}),
        ("Deposits from customers", {"FY2025": 4575114, "FY2024": 4133406, "FY2023": 3760199, "FY2022": 3112478, "FY2021": 2856949}),
        ("Total equity", {"FY2025": 282447, "FY2024": 273773, "FY2023": 259686, "FY2022": 222537, "FY2021": 210024}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total group operating income", {"FY2025": 169470, "FY2024": 179517, "FY2023": 183601, "FY2022": 140539, "FY2021": 91314}),
        ("Operating expenses", {"FY2025": -148321, "FY2024": -140712, "FY2023": -136655, "FY2022": -112904, "FY2021": -96512}),
        ("Profit/(loss) for the year", {"FY2025": 22065, "FY2024": 29751, "FY2023": 38683, "FY2022": 17863, "FY2021": 6791}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 273773, "FY2024": 259686, "FY2023": 222537, "FY2022": 210024, "FY2021": 182644}),
        ("Total comprehensive income for the year", {"FY2025": 22021, "FY2024": 30347, "FY2023": 39004, "FY2022": 18363, "FY2021": 7430}),
        ("Other equity movements, net", {"FY2025": -13347, "FY2024": -16260, "FY2023": -1855, "FY2022": -5850, "FY2021": 19950}),
        ("Closing equity", {"FY2025": 282447, "FY2024": 273773, "FY2023": 259686, "FY2022": 222537, "FY2021": 210024}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash inflow from operating activities", {"FY2025": 630443, "FY2024": 374434, "FY2023": 610323, "FY2022": 113493, "FY2021": 206317}),
        ("Net cash outflow from investing activities", {"FY2025": -848623, "FY2024": -282524, "FY2023": -517902, "FY2022": -135492, "FY2021": -92546}),
        ("Net cash (outflow)/inflow from financing activities", {"FY2025": -205632, "FY2024": -18992, "FY2023": -34997, "FY2022": -17614, "FY2021": 27300}),
        ("Cash and cash equivalents at 31 December", {"FY2025": 555039, "FY2024": 978851, "FY2023": 905933, "FY2022": 848509, "FY2021": 888122}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2024": "13.15%", "FY2023": "12.98%", "FY2022": "11.57%", "FY2021": "12.3%"}),
        ("Tier 1 Ratio", {"FY2024": "13.15%", "FY2023": "12.98%", "FY2022": "11.57%", "FY2021": "12.3%"}),
        ("Total Capital Ratio", {"FY2024": "15.28%", "FY2023": "15.18%", "FY2022": "14.05%", "FY2021": "14.9%"}),
        ("Leverage Ratio", {"FY2024": "6.12%", "FY2023": "6.24%", "FY2022": "6.00%", "FY2021": "5.2%"}),
        ("LCR", {"FY2024": "175%", "FY2023": "220%", "FY2022": "175%", "FY2021": "184.3%"}),
        ("NSFR", {"FY2024": "132%", "FY2023": "136%", "FY2022": "127%", "FY2021": "133.1%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. Balance Sheet, Profit & Loss, Statement of Changes "
         "in Equity and Cash Flow are all the Bank's own Group basis (Companies House); Pillar 3 ratios are the "
         "Arbuthnot Banking Group PLC published Pillar 3 basis - see the entity note on the Cash Flow Statement "
         "sheet for the small scope difference between the two. FY2025 Pillar 3 is not yet published.",
)

# FY2017 headline extension from Arbuthnot Banking Group Report & Accounts
# 2017 (official source, pp.9-15), £'000. Historical Pillar 3 metrics were
# not published in this report and remain blank.
_fy17 = {
    "Balance Sheet": {"Loans and advances to customers": 1049269, "Total assets": 1853232},
    "Profit & Loss": {"Operating income from banking activities": 54616, "Profit before tax": 6971},
    "Cash Flow Statement": {},
}
for _sheet, _values in _fy17.items():
    _ws = bw.wb[_sheet]
    _labels = {str(_ws.cell(r, 1).value).strip(): r for r in range(4, _ws.max_row + 1)}
    _col = 1 + YEARS.index("FY2017") + 1
    for _label, _value in _values.items():
        if _label in _labels:
            _ws.cell(_labels[_label], _col, _value)

bw.save("/Users/armaan/code/katalysis/banks/ARBUTHNOT LATHAM FINANCIALS.xlsx")
