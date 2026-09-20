import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2017"]  # most recent first

CH2025_URL = "https://find-and-update.company-information.service.gov.uk/company/00819519/filing-history/MzUyMzkzMjQ5NmFkaXF6a2N4/document?format=pdf&download=0"
CH2023_URL = "https://find-and-update.company-information.service.gov.uk/company/00819519/filing-history/MzQyMzk5NjI0NGFkaXF6a2N4/document?format=pdf&download=0"
CH2021_URL = "https://find-and-update.company-information.service.gov.uk/company/00819519/filing-history/MzM0MTEwODM3MmFkaXF6a2N4/document?format=pdf&download=0"
CH2017_URL = "https://find-and-update.company-information.service.gov.uk/company/00819519/filing-history/MzIwNzQ3NTM0M2FkaXF6a2N4/document?format=pdf&download=0"
# The LSE-listed PARENT's report. Retained deliberately as a provenance record
# of a rejected source, NOT as a figure source - see FY2017_BASIS_NOTE.
AR2017_URL = "https://www.arbuthnotlatham.co.uk/sites/default/files/documents/ABG_Report_and_Accounts_Final_2017.pdf"

P3_H1_2026_URL = "https://www.arbuthnotlatham.co.uk/sites/default/files/documents/ABG-Pillar-3-Disclosures-2026-Interim.pdf"
# ADDED 2026-09-18 (KM1-032). The FY2025 ANNUAL edition, previously recorded as non-existent.
# Note the "-Final" suffix: FY2024's file is "...december-24.pdf" with no suffix and the
# interims are "...YYYY-Interim.pdf", which is why every filename guess missed this one.
P3_2025_URL = "https://www.arbuthnotlatham.co.uk/sites/default/files/documents/ABG-Pillar-3-Disclosures-December-25-Final.pdf"
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


def p3_sources(page_24="6", page_23="6", page_22="6", page_21="31", page_h1_26="4",
               page_25="5", table_25="Template UK KM1", col_25="column a '31-Dec-25*'"):
    return (
        "Sources - Arbuthnot Banking Group PLC Pillar 3 disclosures (UK KM1 Key Metrics template; FY2021 uses the "
        "pre-KM1 'Key Regulatory Metrics' template), £'000 unless stated:\n"
        f"FY2025: Pillar 3 disclosures for the year ended 31 December 2025, printed p.{page_25} ({table_25}), "
        f"{col_25} - {P3_2025_URL}\n"
        f"FY2024 & FY2023 comparative: Pillar 3 disclosures for the year ended 31 December 2024, p.{page_24} (Template UK KM1) - {P3_2024_URL}\n"
        f"FY2023 (own year) & FY2022 comparative: Pillar 3 disclosures for the year ended 31 December 2023, p.{page_23} (Template UK KM1) - {P3_2023_URL}\n"
        f"FY2022 (own year) & FY2021 comparative: Pillar 3 disclosures for the year ended 31 December 2022, p.{page_22} (Template UK KM1) - {P3_2022_URL}\n"
        f"FY2021 (own year): Pillar 3 disclosures for the year ended 31 December 2021, p.{page_21} (Key Regulatory Metrics) - {P3_2021_URL}\n"
        "FY2025 SOURCING CORRECTED 18 September 2026 (KM1-032). This note previously read: 'ABG has not published "
        "a standalone FY2025 ANNUAL Pillar 3 report (every plausible filename under the site's prior-year patterns "
        "returns 404, and the Wayback CDX index for the domain lists no 2025 annual document)', and the 31 December "
        "2025 column was taken from the 30 June 2026 INTERIM report's comparative. THE CLAIM WAS FALSE. ABG's "
        "FY2025 annual Pillar 3 is live and is now the source for this column, so the sheet obeys the standing "
        "rule that a year is read from its OWN edition rather than a later edition's comparative.\n"
        "Why the earlier search missed it, recorded so the next one does not repeat it: (1) the filenames are not "
        "patterned - FY2024 is 'abg-pillar-3-disclosures-december-24.pdf' and FY2025 is "
        "'ABG-Pillar-3-Disclosures-December-25-Final.pdf', with a '-Final' suffix no prior year uses, so no "
        "extrapolation from prior-year patterns could reach it; (2) the IR DOCUMENTS page lists 100+ PDFs and zero "
        "Pillar 3 files - the Pillar 3 index is the IR ANNOUNCEMENTS page, which lists 14 editions covering "
        "2017-2026; (3) an unfiltered CDX sweep of the domain (11,695 rows) lists neither the FY2025 annual nor the "
        "2026 interim, because the archive simply lags this host - a CDX negative is not evidence against a "
        "REACHABLE site. Controls confirm the host serves true 404s (an invented filename and three plausible "
        "FY2025 guesses all return HTTP 200-less 404s with byte-identical bodies, sha e0406d8e4648), so the "
        "original observations were each individually accurate; the error was treating a guess-set as an "
        "enumeration.\n"
        "The figures themselves are UNCHANGED by this correction - the annual edition's column a agrees with the "
        "interim edition's column c to the last digit, which is the cross-check that the previous sourcing was at "
        "least reading the right position. Retained from that earlier verification, and still true: the FY2024 "
        "figures recovered from the interim series (CET1 GBP 234,477k, Total capital GBP 272,459k, RWAs GBP "
        "1,782,645k, CET1/Tier 1 ratio 13.15%, Total capital ratio 15.28%, leverage exposure GBP 3,828,489k / "
        "6.12%, LCR HQLA GBP 1,275,612k / net outflows GBP 730,580k / 175%, NSFR ASF GBP 2,995,437k / RSF GBP "
        "2,274,318k / 132%) match the FY2024 annual report exactly, so the interim and annual KM1s are on an "
        "identical basis. The '*' on the 31-Dec-25 column header carries the document's own footnote 'Includes "
        "year end verified reserves'.\n"
        "Also now available from the annual edition and not from the interim: Template UK OV1 (own funds "
        "requirement and RWEA by risk type) and Template UK REM1. And the document states that ABG is an SDDT and "
        "publishes a Pillar 3 notwithstanding - worth knowing, since elsewhere in this project SDDT status is "
        "cited as a reason a bank publishes none.\n"
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
    f"FY2017 (& FY2016 comparative, not used): Group of companies' accounts made up to 31 December 2017 "
    f"(filed 15 June 2018), Consolidated Statement of Comprehensive Income printed p.22 (PDF p.25) and "
    f"Consolidated Statement of Financial Position printed p.23 (PDF p.26) - {CH2017_URL}\n"
)

FY2017_BASIS_NOTE = (
    "FY2017 basis note (corrected 2026-09-16): the FY2017 column is taken from Arbuthnot Latham & Co., "
    "Limited's OWN statutory consolidated accounts filed at Companies House, the same basis as every other "
    "year in this workbook. It previously carried figures lifted from the LSE-listed parent's Arbuthnot "
    f"Banking Group PLC Report & Accounts 2017 ({AR2017_URL}), which is a different reporting entity. Three "
    "bases appear in that parent report and must not be blended:\n"
    "  (1) ABG Group consolidated (that report's Summarised Balance Sheet, PDF p.15): Total assets "
    "1,853,232; Operating income 54,616; Profit before tax 6,971. This is the PARENT - wrong entity.\n"
    "  (2) ABG's 'Arbuthnot Latham' segmental summary (PDF p.16): Total assets 1,783,675; Operating income "
    "54,925; Profit before tax 10,959. Right entity, but that report states the segmental analysis is "
    "presented BEFORE consolidation adjustments for intergroup operating activities and recharges - so it "
    "is not the statutory consolidated basis either.\n"
    "  (3) The Bank's own statutory consolidated accounts (used here): Total assets 1,783,675; Operating "
    "income 54,925; Profit before tax 9,477; Loans and advances to customers 1,060,769.\n"
    "Total assets and Operating income coincide between (2) and (3); Profit before tax and Loans and "
    "advances to customers do not. The four figures previously shown (1,049,269 / 1,853,232 / 54,616 / "
    "6,971) were all from basis (1) or (2) and have been replaced by basis (3). Both alternative readings "
    "are recorded here rather than reconciled away.\n"
    "The FY2017 Cash Flow Statement column is left blank: the Bank's 2017 consolidated statement of cash "
    "flows (printed p.27, PDF p.30) exists and was read, but its investing section carries lines this "
    "sheet has no rows for (purchase of investment property; disposal of Tarn Crag (Holding) Limited; "
    "purchase of, and cash acquired with, Renaissance Asset Finance Limited), so a partial column would "
    "not reconcile to its own stated net investing outflow of (128,755). Blank, not zero.\n"
    "The 2017 Companies House filing is a scanned document with no text layer; figures were read visually "
    "from the pages rendered at 300 dpi, not taken from OCR output.\n"
)

# ---------------------------------------------------------------
# Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 437548, "FY2024": 911887, "FY2023": 826559, "FY2022": 732728, "FY2021": 814692, "FY2017": 313101}),
    ("DATA", "Loans and advances to banks", {"FY2025": 117491, "FY2024": 66964, "FY2023": 79374, "FY2022": 115781, "FY2021": 73430, "FY2017": 70665}),
    ("DATA", "Debt securities at amortised cost", {"FY2025": 2033158, "FY2024": 1199847, "FY2023": 942437, "FY2022": 439753, "FY2021": 301052, "FY2017": 227019}),
    ("DATA", "Assets classified as held for sale", {"FY2023": 3281, "FY2022": 3279, "FY2021": 3136, "FY2017": 2915}),
    ("DATA", "Derivative financial instruments", {"FY2025": 1398, "FY2024": 2970, "FY2023": 4214, "FY2022": 6322, "FY2021": 1753, "FY2017": 2551}),
    ("DATA", "Loans and advances to customers", {"FY2025": 1960552, "FY2024": 2094226, "FY2023": 2064256, "FY2022": 2047578, "FY2021": 1882461, "FY2017": 1060769}),
    ("DATA", "Current tax assets", {"FY2025": 7010, "FY2024": 1287, "FY2023": 2347}),
    ("DATA", "Other assets", {"FY2025": 50176, "FY2024": 51623, "FY2023": 57092, "FY2022": 52110, "FY2021": 110065, "FY2017": 20589}),
    ("DATA", "Financial investments", {"FY2025": 2061, "FY2024": 4947, "FY2023": 3942, "FY2022": 3404, "FY2021": 3169, "FY2017": 2207}),
    ("DATA", "Deferred tax asset", {"FY2022": 1902, "FY2021": 2040, "FY2017": 886}),
    ("DATA", "Intangible assets", {"FY2025": 37179, "FY2024": 34299, "FY2023": 33320, "FY2022": 36281, "FY2021": 33595, "FY2017": 19728}),
    ("DATA", "Property, plant and equipment", {"FY2025": 310375, "FY2024": 313147, "FY2023": 274176, "FY2022": 175144, "FY2021": 125753, "FY2017": 3806}),
    ("DATA", "Right-of-use assets", {"FY2025": 44502, "FY2024": 47511, "FY2023": 52816, "FY2022": 7714, "FY2021": 15675}),
    ("DATA", "Investment property", {"FY2025": 5250, "FY2024": 5250, "FY2023": 5950, "FY2022": 6550, "FY2021": 6550, "FY2017": 59439}),
    ("TOTAL", "Total assets", {"FY2025": 5006700, "FY2024": 4733958, "FY2023": 4349764, "FY2022": 3628546, "FY2021": 3373371, "FY2017": 1783675}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks", {"FY2025": 1389, "FY2024": 192911, "FY2023": 193410, "FY2022": 236027, "FY2021": 240333, "FY2017": 195097}),
    ("DATA", "Derivative financial instruments", {"FY2023": 1032, "FY2022": 135, "FY2021": 171, "FY2017": 931}),
    ("DATA", "Deposits from customers", {"FY2025": 4575114, "FY2024": 4133406, "FY2023": 3760199, "FY2022": 3112478, "FY2021": 2856949, "FY2017": 1439804}),
    ("DATA", "Current tax liability", {"FY2022": 870, "FY2021": 652, "FY2017": 553}),
    ("DATA", "Other liabilities", {"FY2025": 39960, "FY2024": 34750, "FY2023": 38117, "FY2022": 24189, "FY2021": 19598, "FY2017": 14353}),
    ("DATA", "Lease liabilities", {"FY2025": 58266, "FY2024": 54829, "FY2023": 53761, "FY2022": 7873, "FY2021": 21277}),
    ("DATA", "Deferred tax liability", {"FY2025": 10743, "FY2024": 6186, "FY2023": 5430}),
    ("DATA", "Debt securities in issue", {"FY2025": 38781, "FY2024": 38103, "FY2023": 38129, "FY2022": 24437, "FY2021": 24367}),
    ("TOTAL", "Total liabilities", {"FY2025": 4724253, "FY2024": 4460185, "FY2023": 4090078, "FY2022": 3406009, "FY2021": 3163347, "FY2017": 1650738}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 15000, "FY2024": 15000, "FY2023": 15000, "FY2022": 15000, "FY2021": 15000, "FY2017": 15000}),
    ("DATA", "Retained earnings", {"FY2025": 115767, "FY2024": 105372, "FY2023": 91832, "FY2022": 59957, "FY2021": 47533, "FY2017": 33575}),
    ("DATA", "Other reserves (capital contribution + fair value reserve)", {"FY2025": 151680, "FY2024": 153401, "FY2023": 152854, "FY2022": 147580, "FY2021": 147491, "FY2017": 84362}),
    ("TOTAL", "Total equity", {"FY2025": 282447, "FY2024": 273773, "FY2023": 259686, "FY2022": 222537, "FY2021": 210024, "FY2017": 132937}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 5006700, "FY2024": 4733958, "FY2023": 4349764, "FY2022": 3628546, "FY2021": 3373371, "FY2017": 1783675}),
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
    "FY2017 presentation: the 2017 statements predate IFRS 9 and IFRS 16, so three captions differ. 'Debt "
    "securities at amortised cost' is captioned 'Debt securities held-to-maturity' (the IAS 39 category, also "
    "measured at amortised cost); 'Assets classified as held for sale' is captioned 'Current assets held for "
    "sale'; and FY2017 'Other reserves' 84,362 is the capital contribution reserve plus the IAS 39 available-"
    "for-sale reserve rather than an IFRS 9 fair value reserve. 'Right-of-use assets', 'Lease liabilities', "
    "'Deferred tax liability', 'Current tax assets' and 'Debt securities in issue' have no FY2017 equivalent "
    "and are blank, not zero. The 2017 statement also carries an 'Interests in associates' line, nil at "
    "31 December 2017 (900 at 31 December 2016); no row is added for a nil. The FY2017 column ties exactly - "
    "the twelve asset lines sum to 1,783,675, the five liability lines to 1,650,738, equity to 132,937.\n"
    + FY2017_BASIS_NOTE
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
    ("DATA", "Interest income", {"FY2025": 247248, "FY2024": 263435, "FY2023": 231836, "FY2022": 120013, "FY2021": 77102, "FY2017": 47601}),
    ("DATA", "Interest expense", {"FY2025": -129126, "FY2024": -137562, "FY2023": -90515, "FY2022": -17781, "FY2021": -10384, "FY2017": -6199}),
    ("TOTAL", "Net interest income", {"FY2025": 118122, "FY2024": 125873, "FY2023": 141321, "FY2022": 102232, "FY2021": 66718, "FY2017": 41402}),
    ("DATA", "Fee and commission income", {"FY2025": 31689, "FY2024": 29142, "FY2023": 23170, "FY2022": 21586, "FY2021": 18472, "FY2017": 13805}),
    ("DATA", "Fee and commission expense", {"FY2025": -1444, "FY2024": -1029, "FY2023": -768, "FY2022": -537, "FY2021": -349, "FY2017": -282}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 30245, "FY2024": 28113, "FY2023": 22402, "FY2022": 21049, "FY2021": 18123, "FY2017": 13523}),
    ("TOTAL", "Operating income from banking activities", {"FY2025": 148367, "FY2024": 153986, "FY2023": 163723, "FY2022": 123281, "FY2021": 84841, "FY2017": 54925}),
    ("SECTION", "Income from leasing activities", {}),
    ("DATA", "Revenue", {"FY2025": 118569, "FY2024": 110832, "FY2023": 100952, "FY2022": 99367, "FY2021": 74500}),
    ("DATA", "Cost of goods sold", {"FY2025": -97466, "FY2024": -85301, "FY2023": -81074, "FY2022": -82109, "FY2021": -68027}),
    ("TOTAL", "Gross profit from leasing activities", {"FY2025": 21103, "FY2024": 25531, "FY2023": 19878, "FY2022": 17258, "FY2021": 6473}),
    ("TOTAL", "Total group operating income", {"FY2025": 169470, "FY2024": 179517, "FY2023": 183601, "FY2022": 140539, "FY2021": 91314, "FY2017": 54925}),
    ("DATA", "Impairment loss on financial assets", {"FY2025": -2501, "FY2024": -6275, "FY2023": -3191, "FY2022": -5503, "FY2021": -3196, "FY2017": -394}),
    ("DATA", "Other income", {"FY2025": 5536, "FY2024": 2560, "FY2023": 3361, "FY2022": 2467, "FY2021": 4402, "FY2017": 3870}),
    ("DATA", "Profit from bargain purchase", {"FY2021": 8626}),
    ("DATA", "Loss on sale of commercial property held as inventory", {"FY2022": -4590}),
    ("DATA", "Operating expenses", {"FY2025": -148321, "FY2024": -140712, "FY2023": -136655, "FY2022": -112904, "FY2021": -96512, "FY2017": -48924}),
    ("TOTAL", "Profit/(loss) before tax", {"FY2025": 24184, "FY2024": 35090, "FY2023": 47116, "FY2022": 20009, "FY2021": 4634, "FY2017": 9477}),
    ("DATA", "Income tax (expense)/credit", {"FY2025": -2119, "FY2024": -5339, "FY2023": -8433, "FY2022": -2146, "FY2021": 2157, "FY2017": -540}),
    ("TOTAL", "Profit/(loss) for the year", {"FY2025": 22065, "FY2024": 29751, "FY2023": 38683, "FY2022": 17863, "FY2021": 6791, "FY2017": 8937}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Movement in fair value reserve", {"FY2025": -59, "FY2024": 778, "FY2023": 412, "FY2022": 628, "FY2021": 763, "FY2017": 128}),
    ("DATA", "Tax on other comprehensive income", {"FY2025": 15, "FY2024": -182, "FY2023": -91, "FY2022": -128, "FY2021": -124, "FY2017": -26}),
    ("TOTAL", "Other comprehensive income for the period, net of tax", {"FY2025": -44, "FY2024": 596, "FY2023": 321, "FY2022": 499, "FY2021": 639, "FY2017": 102}),
    ("TOTAL", "Total comprehensive income for the period", {"FY2025": 22021, "FY2024": 30347, "FY2023": 39004, "FY2022": 18363, "FY2021": 7430, "FY2017": 9039}),
]

INCOME_STATEMENT_SOURCES = (
    STATEMENT_SOURCES_HEAD +
    "Presentation note: FY2021 uniquely includes a 'Profit from bargain purchase' line (£8,626k, the AAG "
    "acquisition) and reports an income tax CREDIT (positive); FY2022 uniquely includes a 'Loss on sale of "
    "commercial property held as inventory' line. All other years leave these blank rather than showing zero. "
    "'Sale of financial assets carried at FVOCI' (a reclassification between Retained earnings and the Fair "
    "value reserve, disclosed in the equity statement) is not shown here - it nets to zero on total comprehensive "
    "income and is a transfer within equity rather than a P&L income/expense item.\n"
    "FY2017 presentation: the leasing business was acquired in FY2021, so the 'Income from leasing activities' "
    "section is blank for FY2017 and the 2017 statement's single 'Operating income' line of 54,925 is shown on "
    "both the banking-activities row and the group-total row - the same disclosed figure, not a derivation. "
    "'Movement in fair value reserve' 128 is captioned 'Available-for-sale reserve' in 2017 (IAS 39, pre-IFRS 9). "
    "The FY2017 column ties exactly: 41,402 + 13,523 = 54,925; 54,925 - 394 + 3,870 - 48,924 = 9,477; "
    "9,477 - 540 = 8,937; 8,937 + 102 = 9,039.\n"
    + FY2017_BASIS_NOTE
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

# ---------------------------------------------------------------
# KM1 Key Metrics - "Template UK KM1 - Key metrics template" exactly as ABG
# prints it. Points to watch, all reproduced rather than normalised:
#
#   * COLUMN LETTERS. Every ABG edition prints a THREE-column table headed
#     "a c e" - the current period, the prior half-year, and the prior
#     year-end. Only the year-end columns map onto this workbook's FY years,
#     so the half-year columns (30-Jun-xx) are not carried here. The FY2025
#     column is column c of the 30 June 2026 INTERIM report ("31-Dec-25*"),
#     because ABG published no standalone FY2025 annual Pillar 3 at all - see
#     p3_sources() above for how that reading was verified against the FY2024
#     annual report.
#
#   * A DASH IS A DASH. Rows UK 8a, UK 9a, 10 and UK 10a print "-" in
#     every column of every edition: the requirement does not apply to ABG,
#     which is not the same statement as "the buffer is measured at zero" -
#     and not the same statement as silence either. Those cells CARRY the
#     dash. Rows 14a-14e look similar but are NOT dashes; see the note.
#
#   * THE 1 JANUARY 2022 BASIS BREAK. In the FY2022 edition the Dec-21
#     column of rows 13 and 14 carries, instead of a figure, "NA: For ABG the
#     Leverage Ratio rules which exclude claims on central banks were
#     effective from 1 January 2022", and rows 18-20 carry "NA: The current
#     NSFR rules were effective 1 January 2022." Those five cells are written
#     as "-" (map rule 2; printed glyph "NA") - not blanked and not back-filled from
#     a different basis.
#
#   * Rows 14a-14e are printed with a single note spanning the block, "NA:
#     Only LREQ firms shall disclose values in rows UK KM1;14a to UK KM1;14e".
#     The rows are kept (ABG prints them) with blank cells, and the note is
#     recorded in the source citation.
#
#   * FY2017 pre-dates the template: blank. The FY2021 edition uses a
#     pre-KM1 "Key Regulatory Metrics" layout, so FY2021 here is the Dec-21
#     comparative column of the FY2022 edition, which IS on the KM1 template.
# ---------------------------------------------------------------
# GA-020 (2026-09-19): KM1 map rule 2 - the printed "NA: ..." glyph is carried as a plain ASCII "-";
# the glyph and its wording are recorded in KM1_SOURCES. Previously the cells held the text "NA".
_KM1_NA = "-"

km1_rows = [
    ("SECTION", "Available own funds (amounts, £'000)", {}),
    ("DATA", "1    Common Equity Tier 1 (CET1) capital (£'000)",
     {"FY2025": 241598, "FY2024": 234477, "FY2023": 222291, "FY2022": 175375, "FY2021": 176235}),
    ("DATA", "2    Tier 1 capital (£'000)",
     {"FY2025": 241598, "FY2024": 234477, "FY2023": 222291, "FY2022": 175375, "FY2021": 176235}),
    ("DATA", "3    Total capital (£'000)",
     {"FY2025": 280270, "FY2024": 272459, "FY2023": 260017, "FY2022": 212969, "FY2021": 213007}),
    ("SECTION", "Risk-weighted exposure amounts", {}),
    ("DATA", "4    Total risk-weighted exposure amount (£'000)",
     {"FY2025": 1822551, "FY2024": 1782645, "FY2023": 1713146, "FY2022": 1516141, "FY2021": 1427724}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "5    Common Equity Tier 1 ratio (%)",
     {"FY2025": "13.26%", "FY2024": "13.15%", "FY2023": "12.98%", "FY2022": "11.57%", "FY2021": "12.34%"}),
    ("DATA", "6    Tier 1 ratio (%)",
     {"FY2025": "13.26%", "FY2024": "13.15%", "FY2023": "12.98%", "FY2022": "11.57%", "FY2021": "12.34%"}),
    ("DATA", "7    Total capital ratio (%)",
     {"FY2025": "15.38%", "FY2024": "15.28%", "FY2023": "15.18%", "FY2022": "14.05%", "FY2021": "14.92%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "UK 7a    Additional CET1 SREP requirements (%)",
     {"FY2025": "0.03%", "FY2024": "0.18%", "FY2023": "0.18%", "FY2022": "0.18%", "FY2021": "0.63%"}),
    ("DATA", "UK 7b    Additional AT1 SREP requirements (%)",
     {"FY2025": "0.01%", "FY2024": "0.06%", "FY2023": "0.06%", "FY2022": "0.06%", "FY2021": "0.13%"}),
    ("DATA", "UK 7c    Additional T2 SREP requirements (%)",
     {"FY2025": "0.01%", "FY2024": "0.08%", "FY2023": "0.08%", "FY2022": "0.08%", "FY2021": "0.17%"}),
    ("DATA", "UK 7d    Total SREP own funds requirements (%)",
     {"FY2025": "8.05%", "FY2024": "8.32%", "FY2023": "8.32%", "FY2022": "8.32%", "FY2021": "8.93%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "8    Capital conservation buffer (%)",
     {"FY2025": "2.50%", "FY2024": "2.50%", "FY2023": "2.50%", "FY2022": "2.50%", "FY2021": "2.5%"}),
    ("DATA", "UK 8a    Conservation buffer due to macro-prudential or systemic risk identified at the level of a Member State (%)",
     {"FY2025": "-", "FY2024": "-", "FY2023": "-", "FY2022": "-", "FY2021": "-"}),
    ("DATA", "9    Institution specific countercyclical capital buffer (%)",
     {"FY2025": "1.92%", "FY2024": "1.91%", "FY2023": "1.88%", "FY2022": "0.88%", "FY2021": "0.02%"}),
    # Dashed in EVERY column of EVERY edition. Each year taken from the column
    # that is its own year-end: FY2025 from the 31-Dec-25 column of the 30 June
    # 2026 interim, FY2024/FY2023/FY2022 from column a of their own annual
    # editions, FY2021 from the 31-Dec-21 column of the FY2022 edition (ABG's
    # own FY2021 annual Pillar 3 prints no UK KM1 template at all - rule 28).
    ("DATA", "UK 9a    Systemic risk buffer (%)",
     {"FY2025": "-", "FY2024": "-", "FY2023": "-", "FY2022": "-", "FY2021": "-"}),
    ("DATA", "10    Global Systemically Important Institution buffer (%)",
     {"FY2025": "-", "FY2024": "-", "FY2023": "-", "FY2022": "-", "FY2021": "-"}),
    ("DATA", "UK 10a    Other Systemically Important Institution buffer",
     {"FY2025": "-", "FY2024": "-", "FY2023": "-", "FY2022": "-", "FY2021": "-"}),
    ("DATA", "11    Combined buffer requirement (%)",
     {"FY2025": "4.42%", "FY2024": "4.41%", "FY2023": "4.38%", "FY2022": "3.38%", "FY2021": "2.52%"}),
    ("DATA", "UK 11a    Overall capital requirements (%)",
     {"FY2025": "12.47%", "FY2024": "12.73%", "FY2023": "12.70%", "FY2022": "11.70%", "FY2021": "11.45%"}),
    ("DATA", "12    CET1 available after meeting the total SREP own funds requirements (%)",
     {"FY2025": "7.22%", "FY2024": "6.91%", "FY2023": "6.74%", "FY2022": "5.33%", "FY2021": "5.59%"}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "13    Total exposure measure excluding claims on central banks (£'000)",
     {"FY2025": 4568671, "FY2024": 3828489, "FY2023": 3559597, "FY2022": 2923193, "FY2021": _KM1_NA}),
    ("DATA", "14    Leverage ratio excluding claims on central banks (%)",
     {"FY2025": "5.29%", "FY2024": "6.12%", "FY2023": "6.24%", "FY2022": "6.00%", "FY2021": _KM1_NA}),
    ("SECTION", "Additional leverage ratio disclosure requirements", {}),
    ("DATA", "14a    Fully loaded ECL accounting model leverage ratio excluding claims on central banks (%)", {}),
    ("DATA", "14b    Leverage ratio including claims on central banks (%)", {}),
    ("DATA", "14c    Average leverage ratio excluding claims on central banks (%)", {}),
    ("DATA", "14d    Average leverage ratio including claims on central banks (%)", {}),
    ("DATA", "14e    Countercyclical leverage ratio buffer (%)", {}),
    ("SECTION", "Liquidity Coverage Ratio", {}),
    ("DATA", "15    Total high-quality liquid assets (HQLA) (Weighted value -average) (£'000)",
     {"FY2025": 1891643, "FY2024": 1275612, "FY2023": 1046604, "FY2022": 710180, "FY2021": 776633}),
    ("DATA", "UK 16a    Cash outflows - Total weighted value",
     {"FY2025": 1165658, "FY2024": 912053, "FY2023": 692133, "FY2022": 629384, "FY2021": 547432}),
    ("DATA", "UK 16b    Cash inflows - Total weighted value (£'000)",
     {"FY2025": 170906, "FY2024": 181473, "FY2023": 215585, "FY2022": 223565, "FY2021": 192514}),
    ("DATA", "16    Total net cash outflows (adjusted value) (£'000)",
     {"FY2025": 994752, "FY2024": 730580, "FY2023": 476548, "FY2022": 405819, "FY2021": 354918}),
    ("DATA", "17    Liquidity coverage ratio (%)",
     {"FY2025": "190%", "FY2024": "175%", "FY2023": "220%", "FY2022": "175%", "FY2021": "219%"}),
    ("SECTION", "Net Stable Funding Ratio", {}),
    ("DATA", "18    Total available stable funding (£'000)",
     {"FY2025": 3126629, "FY2024": 2995437, "FY2023": 2784678, "FY2022": 2464147, "FY2021": _KM1_NA}),
    ("DATA", "19    Total required stable funding (£'000)",
     {"FY2025": 2058754, "FY2024": 2274318, "FY2023": 2043499, "FY2022": 1940538, "FY2021": _KM1_NA}),
    ("DATA", "20    NSFR ratio (%)",
     {"FY2025": "152%", "FY2024": "132%", "FY2023": "136%", "FY2022": "127%", "FY2021": _KM1_NA}),
]

KM1_SOURCES = p3_sources() + (
    "\nKM1 presentation notes:\n"
    "• COLUMN SELECTION. Every ABG edition prints a three-column table headed \"a c e\": the current "
    "period, the prior half-year and the prior year-end. Only the year-end columns are carried here "
    "(FY2025 = \"31-Dec-25*\" column c of the 30 June 2026 interim report; FY2024/FY2023/FY2022 = column a "
    "of their own annual reports; FY2021 = the \"Dec - 21*\" column e of the FY2022 report). The 30-Jun-xx "
    "columns are half-year positions and are deliberately not shown in a workbook of financial years.\n"
    "• A DASH IS A DASH - NOT A ZERO, AND NOT A BLANK. Rows UK 8a, UK 9a, 10 and UK 10a print \"-\" in "
    "every column of every edition, meaning the requirement does not apply to ABG, and each cell carries "
    "that dash. Writing 0% would assert a measured value of zero; leaving the cell empty would say ABG "
    "never published the row, and it plainly did. Re-read at source on 2026-09-18 in all four editions: "
    "the 31-Dec-25 column of the 30 June 2026 interim, and the 31-Dec-24, 31-Dec-23 and 31-Dec-22 columns "
    "of their own annual editions, plus the 31-Dec-21 column of the FY2022 edition.\n"
    "• ROWS 14a-14e ARE NOT DASHED, AND STAY BLANK. Those five rows carry one sentence printed across all "
    "of them: \"NA: Only LREQ firms shall disclose values in rows UK KM1;14a to UK KM1;14e\". That is "
    "ABG's own \"NA\", not a dash, and it says which firms the rows apply to rather than giving a value. "
    "The cells stay empty and are deliberately NOT converted to \"-\".\n"
    "• '-' IN FY2021 ROWS 13, 14, 18, 19 AND 20 IS WHERE THE BANK PRINTED \"NA\" (map rule 2: the cell carries "
    "a plain ASCII '-', the glyph is recorded here; converted from the text 'NA' under GA-020, 2026-09-19). "
    "It marks the 1 January 2022 basis break rather than missing data. Rows 13 and 14 print \"NA: For ABG the Leverage Ratio rules which exclude "
    "claims on central banks were effective from 1 January 2022\"; rows 18, 19 and 20 print \"NA: The "
    "current NSFR rules were effective 1 January 2022.\" The FY2022 report adds the general footnote "
    "\"The disclosure of data for previous periods is not required when data is disclosed for the first "
    "time.\" No FY2021 figure on an older basis has been substituted.\n"
    "• Rows 14a-14e are printed by ABG with one note spanning the whole block: \"NA: Only LREQ firms "
    "shall disclose values in rows UK KM1;14a to UK KM1;14e\". The rows are retained with blank cells.\n"
    "• PRECISION DRIFT: the FY2022 edition prints row 8 as \"2.50%\" in its Dec-22 and Jun-22 columns but "
    "\"2.5%\" in its Dec-21 column, within one row of one table. Transcribed as printed.\n"
    "• FOOTNOTED BASES, per ABG's own footnotes in every edition: the year-end columns are marked "
    "\"* Includes year end verified reserves\"; row 17 LCR is the simple average of month-end positions "
    "over the preceding 12 months; row 20 NSFR is an average of the preceding four quarters.\n"
    "• DELIBERATE FY2021 DIVERGENCE FROM THE LCR SHEET, recorded not reconciled. This sheet's FY2021 "
    "liquidity rows are the KM1 comparative from the FY2022 report (HQLA £776,633k, net outflows "
    "£354,918k, LCR 219%), which is the 12-month-average basis the KM1 template requires. The separate "
    "LCR sheet in this workbook carries the FY2021 report's own pre-KM1 'Key Regulatory Metrics' figures "
    "(HQLA £897,493k, net outflows £487,009k, LCR 184.3%), a point-in-time year-end position. Both are "
    "ABG's own published numbers for 31 December 2021 on two different bases; neither has been adjusted "
    "to agree with the other.\n"
    "• FY2017 is blank: it pre-dates the UK KM1 template entirely."
)

bw.add_km1_sheet(
    title="Arbuthnot Banking Group PLC — KM1 Key Metrics",
    subtitle="The group's own published \"Template UK KM1 - Key metrics template\", reproduced in ABG's row "
             "order with its own template row numbers and printed precision. Amounts in £'000, ratios as "
             "printed. Arbuthnot Banking Group PLC (Pillar 3) basis — the consolidated group of which "
             "Arbuthnot Latham & Co., Limited is the banking subsidiary; ABG publishes no subsidiary-level "
             "KM1. FY2017 pre-dates the template and is intentionally blank.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
)

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
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 1511849, "FY2024": 1525678, "FY2023": 1511071, "FY2022": 1333060, "FY2021": 1257789}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 410, "FY2024": 741, "FY2023": 2250, "FY2022": 13540, "FY2021": 2911}),
    ("DATA", "Market risk (position, FX and commodities)", {"FY2025": 418, "FY2024": 1376, "FY2023": 3727, "FY2022": 3753, "FY2021": 7527}),
    ("DATA", "Operational risk", {"FY2025": 309874, "FY2024": 254850, "FY2023": 196098, "FY2022": 165788, "FY2021": 159498}),
    ("TOTAL", "Total risk-weighted exposure amount", {"FY2025": 1822551, "FY2024": 1782645, "FY2023": 1713146, "FY2022": 1516141, "FY2021": 1427725}),
]

RWA_BREAKDOWN_SOURCES = (
    p3_sources(page_24="7", page_23="15", page_22="16", page_21="6",
               page_25="7", table_25="Template UK OV1 - Overview of risk weighted exposure amounts",
               col_25="column a '31-Dec-25' (PDF p.9)") +
    "\nFY2025 FILLED 18 September 2026 (GA- leading-gap pass). This sheet previously left FY2025 blank with the "
    "explanation that ABG had published no FY2025 ANNUAL Pillar 3 and that the 30 June 2026 interim carries KM1 "
    "but not the annual-only OV1. The second half of that statement is still true of the interim; the first half "
    "was false, and the FY2025 annual edition (found under KM1-032) does carry Template UK OV1 on printed p.7. "
    "Its column a '31-Dec-25' is the source for the FY2025 column here, and its column b '31-Dec-24' reproduces "
    "the FY2024 figures already transcribed from the FY2024 annual edition exactly (credit risk 1,525,678; CCR "
    "741; market risk 1,376; operational risk 254,850; total 1,782,645), which is the cross-check that the two "
    "editions are on one basis. The FY2025 total (£1,822,551k) also ties exactly to the Total RWAs sheet's FY2025 "
    "KM1 figure. Sub-rows the FY2025 edition prints and this sheet does not carry, recorded so they are not "
    "re-hunted: 'Of which the standardised approach' 1,511,849 (credit risk), 'Of which credit valuation "
    "adjustment - CVA' 133 and 'Of which other CCR' 277 (both within CCR 410), 'Of which the standardised "
    "approach' 418 (market risk), 'Of which basic indicator approach' 309,874 (operational risk), and a column c "
    "'Total own funds requirements' of 145,804.\n"
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

# GA-020 (2026-09-19) evidenced statement texts, per year.
_ARB_MREL_447H = ("Not published – no MREL figure in this year's Pillar 3 (full-text search 2026-09-19); its KM1 "
                  "preamble says the Art. 447(h) own funds/eligible liabilities ratios 'only apply to G-SIIs'")
_ARB_MREL_P3 = "Not published – no MREL figure or reference in this year's Pillar 3 (full-text search 2026-09-19)"
ARB_MREL = {y: _ARB_MREL_447H for y in ("FY2025", "FY2024", "FY2023")}
ARB_MREL.update({"FY2022": _ARB_MREL_P3, "FY2021": _ARB_MREL_P3,
                 "FY2017": ("Not published – no MREL figure or reference in AL & Co's FY2017 accounts (OCR'd in full "
                            "2026-09-19) or ABG's FY2017 annual report (full-text search)")})
metric(
    "MREL Ratio", None,
    [("MREL ratio", ARB_MREL)],
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
        ("Total assets", {"FY2025": 5006700, "FY2024": 4733958, "FY2023": 4349764, "FY2022": 3628546, "FY2021": 3373371, "FY2017": 1783675}),
        ("Loans and advances to customers", {"FY2025": 1960552, "FY2024": 2094226, "FY2023": 2064256, "FY2022": 2047578, "FY2021": 1882461, "FY2017": 1060769}),
        ("Deposits from customers", {"FY2025": 4575114, "FY2024": 4133406, "FY2023": 3760199, "FY2022": 3112478, "FY2021": 2856949, "FY2017": 1439804}),
        ("Total equity", {"FY2025": 282447, "FY2024": 273773, "FY2023": 259686, "FY2022": 222537, "FY2021": 210024, "FY2017": 132937}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total group operating income", {"FY2025": 169470, "FY2024": 179517, "FY2023": 183601, "FY2022": 140539, "FY2021": 91314, "FY2017": 54925}),
        ("Operating expenses", {"FY2025": -148321, "FY2024": -140712, "FY2023": -136655, "FY2022": -112904, "FY2021": -96512, "FY2017": -48924}),
        ("Profit/(loss) for the year", {"FY2025": 22065, "FY2024": 29751, "FY2023": 38683, "FY2022": 17863, "FY2021": 6791, "FY2017": 8937}),
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

# FY2017 is carried in the balance_sheet_rows / income_statement_rows dicts
# above, like every other year, so it flows through STATEMENT_SOURCES_HEAD and
# is cited. It was previously bolted on here by writing straight into
# bw.wb[...] after the sheets were built, which bypassed the citation plumbing
# and hid an entity-basis error (parent ABG PLC figures in a Bank-basis
# workbook) - see FY2017_BASIS_NOTE. Do not reintroduce that pattern: as well
# as skipping the citation, its label lookup collapsed duplicate row captions
# (this balance sheet has two 'Derivative financial instruments' rows) onto the
# last match, so a value could land in the wrong section silently.

bw.save("/Users/armaan/code/katalysis/banks/ARBUTHNOT LATHAM FINANCIALS.xlsx")
