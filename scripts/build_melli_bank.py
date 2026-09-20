import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

# The Pillar 3 sheets run deeper than the statement sheets. Only TWO Melli Pillar 3
# editions have ever been public and only those two survive anywhere (FY2014 and
# FY2016 - see PILLAR3_HISTORY_NOTE), so those two columns are appended to the
# Pillar 3 / RWA Breakdown sheets and to those sheets only. FY2015 and FY2017-FY2020
# are deliberately absent rather than blank: see PILLAR3_HISTORY_NOTE for why each
# missing year is a closed question, not an unresearched gap.
P3_YEARS = YEARS + ["FY2016", "FY2014"]
YEAR_LABEL = {y: y for y in P3_YEARS}

AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/04152338/filing-history/MzUyNjMyOTE4OGFkaXF6a2N4/document?download=0&format=pdf"
AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/04152338/filing-history/MzQ3MDI0ODU4NWFkaXF6a2N4/document?download=0&format=pdf"
AR2023_URL = "https://vpr.hkma.gov.hk/statics/assets/doc/100273/ar_23/ar_23_eng.pdf"
AR2022_URL = "https://vpr.hkma.gov.hk/statics/assets/doc/100273/ar_22/ar_22_eng.pdf"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/04152338/filing-history/MzM0MzE1NzIzOWFkaXF6a2N4/document?download=0&format=pdf"

# The only two Melli Bank plc Pillar 3 disclosure documents that have ever been
# public, both recovered from the Internet Archive (mellibank.com itself is down).
# Both verified on retrieval: %PDF magic bytes, page count, and cover text naming
# "Registered number 4152338" - i.e. the UK entity, NOT Bank Melli Iran the parent.
P3_2016_URL = ("https://web.archive.org/web/20190405190315id_/http://mellibank.com/File/"
               "DownloadReportFiles?filename=Melli%20Bank%20-%20Pillar%203%20%20Disclosures%202016%20-%20Final.pdf")
P3_2014_URL = ("https://web.archive.org/web/20170407223115id_/http://mellibank.com/PDFs/"
               "Melli%20Bank%20P3%20Disclosures%20as%20at%2031%20December%202014%20FINAL.pdf")
P3_2014_ALT_URL = "https://web.archive.org/web/20160221234533*/mellibank.co.uk"
CH_FILING_HISTORY_URL = "https://find-and-update.company-information.service.gov.uk/company/04152338/filing-history"
HKMA_REGISTER_URL = "https://vpr.hkma.gov.hk/statics/assets/doc/100273/"

ACCESS_ROUTES_NOTE = (
    "ACCESS ROUTES - RECORDED SO THEY ARE NOT REDISCOVERED. Melli Bank plc's own domains are down: "
    "mellibank.com resolves (62.232.194.164) but times out on both ports, consistent with the 29 September 2025 "
    "sanctions designation, and mellibank.co.uk is long gone. Three routes work and between them supply every "
    "document cited in this workbook:\n"
    f"  (1) COMPANIES HOUSE, company 04152338 - the filing history carries every annual report from FY2002 to "
    f"FY2025 as a downloadable PDF. This is the route for all the statutory accounts: {CH_FILING_HISTORY_URL}\n"
    f"  (2) THE HONG KONG MONETARY AUTHORITY PUBLIC REGISTER - a non-obvious route worth keeping. Melli Bank plc "
    f"has a Hong Kong branch regulated by the HKMA (stated in its own Pillar 3: 'The Bank has one branch in Hong "
    f"Kong which is regulated by the Hong Kong Monetary Authority'), and the HKMA register therefore hosts readable "
    f"copies of the Bank's annual reports under institution id 100273 - e.g. {HKMA_REGISTER_URL}ar_23/ar_23_eng.pdf "
    f"(FY2023) and {HKMA_REGISTER_URL}ar_22/ar_22_eng.pdf (FY2022). Nothing about a UK bank's name suggests "
    f"searching a Hong Kong regulator's register; it was found via the branch disclosure.\n"
    "  (3) THE INTERNET ARCHIVE, for the two surviving Pillar 3 documents only - see PILLAR3_HISTORY_NOTE. Use the "
    "'id_' raw-capture form of the Wayback URL; the ordinary wayback form returns the archive's HTML wrapper."
)

PILLAR3_HISTORY_NOTE = (
    "PILLAR 3 PUBLICATION HISTORY - THE COMPLETE ANSWER FOR THIS BANK (compiled 2026-09-16; do not re-chase).\n"
    "Melli Bank plc's Directors' report states, in terms, what the Bank did with its Pillar 3 disclosure each year. "
    "All thirteen annual reports FY2013-FY2025 were read from Companies House (company 04152338) and the wording "
    "extracted year by year. It is not one policy but four phases, and the phase matters because it determines "
    "whether a missing document was ever public at all:\n"
    "  FY2013-FY2015: the disclosures 'will be posted to the Bank's website, www.mellibank.com' (FY2013 adds the "
    "condition 'after the agreement of the capital planning buffer with the PRA') - a FORWARD-LOOKING promise.\n"
    "  FY2016-FY2019: the disclosures 'have been posted to the Bank's website' - a statement that publication HAS "
    "HAPPENED.\n"
    "  FY2020-FY2022: 'available on request from the Bank' - a declared NON-publication.\n"
    "  FY2023: 'The Pillar 3 disclosure is available on the Bank's website (www.mellibank.com)' - this REVERSES to "
    "website publication, for one year only.\n"
    "  FY2024-FY2025: back to 'available on request'. The FY2025 report also records the 29 September 2025 "
    "sanctions designation.\n"
    "\n"
    "WHAT SURVIVES: exactly TWO editions, both recovered from the Internet Archive and both transcribed into this "
    "workbook's Pillar 3 sheets (the FY2016 and FY2014 columns):\n"
    f"  FY2016 - 23 pages, cover 'Pillar 3 Disclosures / As at 31st December 2016', 'Registered number 4152338' - "
    f"{P3_2016_URL}\n"
    f"  FY2014 - 16 pages, cover 'Pillar 3 Disclosures / As at 31st December 2014', 'Registered number 4152338' - "
    f"{P3_2014_URL}\n"
    f"  (the FY2014 document is additionally archived on the retired domain mellibank.co.uk, capture 20160221234533 "
    f"- {P3_2014_ALT_URL})\n"
    "The registered number on both covers is 4152338, which is Melli Bank plc the UK entity - these are entity-basis "
    "documents, not Bank Melli Iran group disclosures. Both were verified on retrieval (%PDF magic bytes, page "
    "count, cover text) rather than trusted on URL alone.\n"
    "\n"
    "WHAT DOES NOT SURVIVE, AND WHY THAT IS A FINDING RATHER THAN A GAP: no Pillar 3 later than the FY2016 edition "
    "is archived anywhere on mellibank.com. Captures of the domain continue into MAY 2026, so this is an EVIDENCED "
    "absence, not a crawl gap. The site's own DownloadReportFiles index was enumerated and holds Annual Reports "
    "2002-2008 and 2016, plus the FY2016 Pillar 3, and nothing else.\n"
    "\n"
    "THE FY2023 CLAIM IS CONTRADICTED BY THE BANK'S OWN WEBSITE - recorded, deliberately not resolved. The FY2023 "
    "Annual Report says the Pillar 3 disclosure 'is available on the Bank's website (www.mellibank.com)'. The "
    "archived mellibank.com /reports page was read across five captures spanning September 2021, April 2023, June "
    "2023, June 2025, February 2026 and May 2026. EVERY ONE of them says: 'Financial Statements and Pillar 3 "
    "Disclosures are available on request.' So throughout the period in which the Annual Report asserted website "
    "publication, the website itself said available on request. That is a tension between TWO OF THE BANK'S OWN "
    "STATEMENTS - a Directors' report and its own web page - not between a claim and a hole in the archive. Both "
    "are recorded here as they stand; neither is treated as correcting the other, and no FY2023 Pillar 3 figure is "
    "inferred from the Annual Report's assertion that one was published. COMMON CRAWL (2026-09-19) agrees: "
    "mellibank.com and mellibank.co.uk, every host and path, in all 31 crawls CC-MAIN-2024-10 to CC-MAIN-2026-39 "
    "hold compliance PDFs only (Wolfsberg, FSCS, AML, W-8BEN) and no Pillar 3 or report file; the /reports page "
    "captured 3 November 2024 (CC-MAIN-2024-46) carries the same 'available on request' sentence and no report "
    "link. FY2023 therefore stays Unreached.\n"
    "\n"
    "WHAT THIS MEANS FOR FUTURE PASSES, year by year:\n"
    "  FY2013-FY2019 and FY2023 - the Bank states the documents were (or would be) published. These are "
    "PUBLISHED-THEN-LOST, a materially stronger position than never-published, and a written request to the Bank "
    "for a document it says it published is a reasonable ask. The Wayback route above already redeems two of them "
    "(FY2014, FY2016); FY2013, FY2015, FY2017, FY2018, FY2019 and FY2023 are the remaining candidates.\n"
    "  FY2020-FY2022 and FY2024-FY2025 - a DECLARED NON-PUBLICATION. The Bank says the document was never put on "
    "the website; it exists only on request. This is a COMPLETE ANSWER, the same shape as Havin's elsewhere in this "
    "project, and these years must NOT be re-chased through archives or link permutation. Nothing is there to find."
)

ENTITY_NOTE = (
    "ENTITY AND REPORTING BASIS: Melli Bank plc (company 04152338, FRN 207380, LEI "
    "213800BC4TEGCCQH9V07) is an active UK public limited company and PRA-authorised bank, "
    "incorporated in England and Wales. Companies House identifies the registered office as "
    "98a Kensington High Street, London W8 4SG and the latest accounts as made up to 31 December "
    "2025. The Bank's functional and reporting currency is EUR; amounts are therefore retained in "
    "EUR thousands/millions, consistent with the source accounts. The figures are standalone Melli "
    "Bank plc entity figures, not Bank Melli Iran group figures."
)

CASH_FLOW_SOURCES = (
    "Sources - Melli Bank plc entity-level Statements of Cash Flows:\n"
    f"FY2025: Annual Report and Accounts 2025, Statement of Cash Flows p.26 - {AR2025_URL}\n"
    f"FY2024: Annual Report and Accounts 2024, p.24; also shown as the FY2025 report's own comparative column, "
    f"p.26 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Accounts 2023, p.24 - {AR2023_URL}\n"
    f"FY2022: Annual Report and Accounts 2023 comparative column, p.24 - {AR2023_URL}\n"
    "FY2021: genuinely not disclosed, confirmed by two independent checks of the Annual Report 2021 - its "
    "accounting policy note (ii) 'Cash flow exemptions' (p.23) states the Company applied the FRS 102 exemption "
    "from producing a statement of cash flows because it was consolidated with Bank Melli Iran, and its own "
    "Contents page (p.2) lists no Statement of Cash Flows among the report's financial statements at all. This "
    "is a structural non-disclosure at the source, not a retrieval gap - re-confirmed this batch by re-reading "
    f"the full PDF - {AR2021_URL}\n\n"
    + ENTITY_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - Melli Bank plc entity-level regulatory KPI and capital disclosures:\n"
        f"FY2024/FY2023: Annual Report and Accounts 2024, KPI p.9 and capital management p.49 - {AR2024_URL}\n"
        f"FY2023/FY2022/FY2021: Annual Report and Accounts 2023, KPI p.9 and capital management p.49 - {AR2023_URL}\n"
        f"FY2021 comparative context: Annual Report 2021, KPI p.8 and capital management p.46 - {AR2021_URL}\n"
        f"FY2025: Annual Report and Accounts 2025, 'Capital and Liquidity Position' KPI table p.10 - {AR2025_URL}\n"
        f"FY2016: Pillar 3 Disclosures as at 31st December 2016 (the Bank's OWN Pillar 3 document, 23pp) - "
        f"{P3_2016_URL}\n"
        f"FY2014: Pillar 3 Disclosures as at 31st December 2014 (the Bank's OWN Pillar 3 document, 16pp) - "
        f"{P3_2014_URL}\n"
        "\n"
        "BASIS NOTE - TWO DIFFERENT KINDS OF SOURCE ON ONE SHEET. FY2021-FY2025 figures come from the Annual "
        "Report's own KPI / capital-management tables, because no Pillar 3 document exists for those years (the "
        "reports themselves say so - see PILLAR 3 PUBLICATION HISTORY below). FY2016 and FY2014 come from the "
        "Bank's actual Pillar 3 disclosure documents. The two are not the same disclosure regime and the columns "
        "are not a continuous series: FY2014's is a CRD IV-transition-era document with Tier 2 capital "
        "outstanding, FY2016's is post-conversion all-CET1, and FY2021-FY2025's are annual-report KPI extracts. "
        "Years between them are absent, not blank-because-unresearched - see the publication history.\n"
        + (extra + "\n" if extra else "")
        + "\n" + PILLAR3_HISTORY_NOTE
        + "\n\n" + ACCESS_ROUTES_NOTE
    )


bw = BankWorkbook(
    bank_name="Melli Bank plc",
    years=YEARS,
    year_label=YEAR_LABEL,
    header_color="6E4B3A",
)

# ---------------------------------------------------------------
# Statement sources - entity-level Annual Report statements, all 5 years
# now reachable this session (FY2025's Companies House PDF, previously
# noted as "not retrievable in this run" for the Cash Flow Statement sheet,
# was successfully downloaded and read for this batch - see the Balance
# Sheet/P&L/Equity/Asset Quality sheets below; the Cash Flow Statement
# sheet itself is left unchanged per this ticket's scope).
# ---------------------------------------------------------------
STATEMENTS_SOURCES = (
    "Sources - Melli Bank plc entity-level Balance Sheet/Profit and Loss Account/Statement of Change in "
    "Equity/Notes 9 and 11 (Loans and advances - customers / Impairment provisions):\n"
    f"FY2025: Annual Report and Accounts 2025, Balance Sheet p.24, Profit and Loss Account p.22, Statement of "
    f"Change in Equity p.25, Note 9 p.39-40, Note 11 p.41 - {AR2025_URL}\n"
    f"FY2024: Annual Report and Accounts 2024, Balance Sheet p.22, Profit and Loss Account p.20, Statement of "
    f"Change in Equity p.23, Note 9 p.34-35, Note 11 p.36 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Accounts 2023, Balance Sheet p.22, Profit and Loss Account p.20, Statement of "
    f"Change in Equity p.23, Note 9 p.34-35, Note 11 p.36 - {AR2023_URL}\n"
    f"FY2022: Annual Report and Accounts 2023 comparative column (same pages as FY2023 above) - {AR2023_URL}\n"
    f"FY2021: Annual Report 2021, Balance Sheet p.21, Profit and Loss Account p.19, Statement of Comprehensive "
    f"Income p.20, Statement of Change in Equity p.22, Note 9 p.32-33 - {AR2021_URL}\n\n"
    + ENTITY_NOTE
)

# ---------------------------------------------------------------
# Balance Sheet - equity reconciliation ladder confirmed: every year's own
# closing Total Equity ties exactly to both the next year's own opening
# balance and that year's own Statement of Change in Equity closing row.
# Zero plug rows needed anywhere across all 5 years.
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents", {"FY2025": 30504, "FY2024": 52378, "FY2023": 39289, "FY2022": 66955, "FY2021": 119058}),
    ("DATA", "Other financial balances (correspondent-bank balances not meeting the cash-equivalent criteria due to sanctions-related external restrictions - first appears FY2025)", {"FY2025": 71070}),
    ("DATA", "Loans and advances to banks", {"FY2025": 248695, "FY2024": 304655, "FY2023": 294073, "FY2022": 234811, "FY2021": 177182}),
    ("DATA", "Loans and advances to customers", {"FY2025": 3317, "FY2024": 3709, "FY2023": 8275, "FY2022": 8260, "FY2021": 8899}),
    ("DATA", "Tangible assets", {"FY2025": 3392, "FY2024": 3364, "FY2023": 3513, "FY2022": 3509, "FY2021": 3643}),
    ("DATA", "Intangible assets", {"FY2025": 109, "FY2024": 529, "FY2023": 81, "FY2022": 219, "FY2021": 513}),
    ("DATA", "Other assets (FY2021 shown per that year's own combined 'Debtors' line - see subtitle)", {"FY2025": 2545, "FY2024": 4473, "FY2023": 4176, "FY2022": 4970, "FY2021": 4438}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 3243, "FY2024": 6433, "FY2023": 5910, "FY2022": 1329}),
    ("DATA", "Derivative assets", {"FY2024": 0, "FY2023": 271, "FY2022": 136}),
    ("TOTAL", "Total assets", {"FY2025": 362875, "FY2024": 375541, "FY2023": 355588, "FY2022": 320189, "FY2021": 313733}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2025": 95095, "FY2024": 108461, "FY2023": 91412, "FY2022": 54081, "FY2021": 50725}),
    ("DATA", "Customer accounts", {"FY2025": 2973, "FY2024": 3248, "FY2023": 3820, "FY2022": 3980, "FY2021": 4004}),
    ("DATA", "Other liabilities", {"FY2025": 1184, "FY2024": 1238, "FY2023": 505, "FY2022": 1079, "FY2021": 1033}),
    ("DATA", "Accruals and deferred income", {"FY2025": 4674, "FY2024": 3930, "FY2023": 3319, "FY2022": 4919, "FY2021": 2048}),
    ("DATA", "Derivative liabilities", {"FY2025": 104, "FY2021": 311}),
    ("TOTAL", "Total liabilities", {"FY2025": 104030, "FY2024": 116877, "FY2023": 99056, "FY2022": 64059, "FY2021": 58121}),
    ("SECTION", "Shareholder's funds", {}),
    ("DATA", "Called up share capital", {"FY2025": 264412, "FY2024": 264412, "FY2023": 264412, "FY2022": 264412, "FY2021": 264412}),
    ("DATA", "Retained earnings / Accumulated losses", {"FY2025": -5567, "FY2024": -5748, "FY2023": -7880, "FY2022": -8282, "FY2021": -8800}),
    ("DATA", "Other reserves", {"FY2021": 0}),
    ("TOTAL", "Total equity", {"FY2025": 258845, "FY2024": 258664, "FY2023": 256532, "FY2022": 256130, "FY2021": 255612}),
    ("TOTAL", "Total equity and liabilities", {"FY2025": 362875, "FY2024": 375541, "FY2023": 355588, "FY2022": 320189, "FY2021": 313733}),
]

bw.add_balance_sheet_sheet(
    title="Melli Bank plc — Balance Sheet",
    subtitle="Entity-level basis, EUR '000. FY2021's own accounts combine Other assets/Prepayments and accrued income/Derivative "
              "assets into a single 'Debtors' line (4,438) - shown here under Other assets, not blended with later years' split "
              "presentation. FY2025 introduces a new 'Other financial balances' line (correspondent-bank balances that no longer "
              "meet the cash-equivalent criteria due to sanctions-related external restrictions imposed 29 September 2025).",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=100,
    source_height=280,
    unit_suffix=" (EUR '000)",
)

# ---------------------------------------------------------------
# Profit & Loss - each year's own reported structure preserved as-is
# (genuine structural differences across years, not blended).
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable and similar income", {"FY2025": 11658, "FY2024": 13344, "FY2023": 10089, "FY2022": 10725, "FY2021": 3694}),
    ("DATA", "Interest expense (FY2021's own account shows this as a positive net recovery, +14 - transcribed as reported)", {"FY2025": -994, "FY2024": -2016, "FY2023": -1558, "FY2022": -200, "FY2021": 14}),
    ("TOTAL", "Net interest income", {"FY2025": 10664, "FY2024": 11328, "FY2023": 8531, "FY2022": 10525, "FY2021": 3708}),
    ("DATA", "Fees and commission(s) receivable", {"FY2025": 2317, "FY2024": 1356, "FY2023": 55, "FY2022": 73, "FY2021": 80}),
    ("DATA", "Fees and commission(s) payable", {"FY2025": -57, "FY2024": -174, "FY2023": -253, "FY2022": -1171, "FY2021": -40}),
    ("DATA", "Foreign exchange gains/(losses)", {"FY2025": -638, "FY2024": 255, "FY2023": -44, "FY2022": -206, "FY2021": 28}),
    ("DATA", "Other operating income", {"FY2021": 1}),
    ("TOTAL", "Total revenue / Total net income (FY2025's own report relabels this subtotal 'Total net income' - same position in the account, not a different line)", {"FY2025": 12286, "FY2024": 12765, "FY2023": 8289, "FY2022": 9221, "FY2021": 3777}),
    ("DATA", "Administrative expenses", {"FY2025": -11439, "FY2024": -9065, "FY2023": -7495, "FY2022": -8202, "FY2021": -7711}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -666, "FY2024": -365, "FY2023": -392, "FY2022": -475, "FY2021": -743}),
    # Not a line the source statement itself prints - the Bank's own P&L has
    # no combined opex subtotal in any year (its own subtotal position
    # shifts year to year, see the two TOTAL rows below). This row is simply
    # Administrative expenses + Depreciation and amortisation - the two
    # genuinely routine operating-cost lines present every year - deliberately
    # excluding the DB Pension Scheme remeasurement item just below (a one-off
    # item that flips between "Other charges" and "Other income" depending on
    # the year, not a stable operating cost) and the impairment line further
    # down (credit-related, kept out of opex per this project's convention).
    # Added 2026-09-07 so cost-to-income analysis has a "Total operating
    # expenses" numerator to work from.
    ("TOTAL", "Total operating expenses (sum of Administrative expenses + Depreciation and amortisation above - not itself a printed subtotal)", {
        "FY2025": -12105, "FY2024": -9430, "FY2023": -7887, "FY2022": -8677, "FY2021": -8454,
    }),
    ("DATA", "Other charges - DB Pension Scheme / Other income (same underlying pension remeasurement item, presented as an add-back 'Other charges' in FY2024/FY2025's own account and as 'Other income' in FY2023/FY2022's own account)", {"FY2025": 0, "FY2024": 224, "FY2023": 228, "FY2022": 41, "FY2021": 12}),
    ("TOTAL", "Operating profit/(loss) (FY2021's own subtotal position, before Other charges)", {"FY2021": -4677}),
    ("TOTAL", "Profit before provision and taxation (FY2022/FY2023's own subtotal position, after Other income)", {"FY2023": 630, "FY2022": 585}),
    ("DATA", "Impairment - other / Impairment on loans and advances", {"FY2025": 0, "FY2024": -1203, "FY2023": 0, "FY2022": -26, "FY2021": -2643}),
    ("TOTAL", "Profit/(loss) before taxation", {"FY2025": 181, "FY2024": 2356, "FY2023": 630, "FY2022": 559, "FY2021": -7308}),
    ("DATA", "Tax", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("TOTAL", "Profit/(loss) for the financial year", {"FY2025": 181, "FY2024": 2356, "FY2023": 630, "FY2022": 559, "FY2021": -7308}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Remeasurements of net defined benefit pension obligations", {"FY2025": 0, "FY2024": -224, "FY2023": -228, "FY2022": -41, "FY2021": -12}),
    ("DATA", "Movement in other reserves", {"FY2021": 0}),
    ("TOTAL", "Other comprehensive income/(loss) for the year", {"FY2025": 0, "FY2024": -224, "FY2023": -228, "FY2022": -41, "FY2021": -12}),
    ("TOTAL", "Total comprehensive income/(loss) for the year, net of tax", {"FY2025": 181, "FY2024": 2132, "FY2023": 402, "FY2022": 518, "FY2021": -7320}),
]

bw.add_income_statement_sheet(
    title="Melli Bank plc — Profit & Loss",
    subtitle="Entity-level basis, EUR '000. Structure genuinely differs year to year (Total revenue/Operating profit/Other income "
              "structure in FY2021-FY2023 vs Total net income/Other charges structure in FY2024-FY2025 - same pension remeasurement "
              "item presented on opposite sides of the account) - each year shown on its own reported basis, not forced into one "
              "template. FY2021's own account shows Interest expense as a small positive net recovery (+14), transcribed as reported.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=110,
    source_height=280,
    unit_suffix=" (EUR '000)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - chronological roll-forward. Ladder
# confirmed: every year's own closing balance ties exactly to both the
# next year's own opening balance and that year's own Balance Sheet Total
# equity. Zero plug rows needed anywhere across all 5 years - the one
# genuine "easy to skip" movement caught by the mandated scan is FY2021's
# own €21k Other reserves write-off, bundled into that year's own "Loss
# for the financial year" retained-earnings/other-reserves split in the
# source table and reproduced here the same way.
# ---------------------------------------------------------------
equity_headers = ["Called-up share capital", "Retained earnings", "Other reserves", "Total"]
equity_rows = [
    ("TOTAL", "At 31 December 2020 (FY2021 opening)", (264412, -1480, 21, 262953)),
    ("DATA", "Loss for the financial year (includes a €21k write-off of the Other reserves balance, bundled into this row in the source table)", (None, -7308, -21, -7329)),
    ("DATA", "Other comprehensive loss for the year", (None, -12, None, -12)),
    ("TOTAL", "At 31 December 2021 (FY2021 closing)", (264412, -8800, 0, 255612)),
    ("DATA", "Profit for the financial year", (None, 559, None, 559)),
    ("DATA", "Other comprehensive loss for the year", (None, -41, None, -41)),
    ("TOTAL", "At 31 December 2022 (FY2022 closing)", (264412, -8282, 0, 256130)),
    ("DATA", "Profit for the financial year", (None, 630, None, 630)),
    ("DATA", "Other comprehensive loss for the year", (None, -228, None, -228)),
    ("TOTAL", "At 31 December 2023 (FY2023 closing)", (264412, -7880, 0, 256532)),
    ("DATA", "Profit for the financial year", (None, 2356, None, 2356)),
    ("DATA", "Other comprehensive loss for the year", (None, -224, None, -224)),
    ("TOTAL", "At 31 December 2024 (FY2024 closing)", (264412, -5748, 0, 258664)),
    ("DATA", "Profit for the financial year", (None, 181, None, 181)),
    ("DATA", "Other comprehensive income for the year", (None, 0, None, 0)),
    ("TOTAL", "At 31 December 2025 (FY2025 closing)", (264412, -5567, 0, 258845)),
]

bw.add_equity_changes_sheet(
    title="Melli Bank plc — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest. EUR '000. Equity reconciliation ladder confirmed: every year's own "
              "closing balance ties exactly to both the next year's own opening balance and that year's own Balance Sheet Total "
              "equity - zero plug rows needed anywhere across all 5 years.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
)

# Source cash-flow figures are EUR '000. FY2021 is blank because the 2021
# accounts expressly claim the FRS 102 qualifying-entity exemption (re-confirmed
# this batch - see CASH_FLOW_SOURCES). FY2025 added this batch from the
# Annual Report and Accounts 2025's own Statement of Cash Flows (p.26); its
# FY2024 comparative column there (13,753 / -664 / 13,089 / 39,289 / 52,378)
# matches this script's existing FY2024 figures exactly, cross-confirming both.
OPERATING = {"FY2025": -21600, "FY2024": 13753, "FY2023": -27408, "FY2022": -52056}
INVESTING = {"FY2025": -274, "FY2024": -664, "FY2023": -258, "FY2022": -47}
NET_CHANGE = {"FY2025": -21874, "FY2024": 13089, "FY2023": -27666, "FY2022": -52103}
OPENING = {"FY2025": 52378, "FY2024": 39289, "FY2023": 66955, "FY2022": 119058}
CLOSING = {"FY2025": 30504, "FY2024": 52378, "FY2023": 39289, "FY2022": 66955}

cash_rows = [
    ("SECTION", "Operating activities", {}),
    ("TOTAL", "Net cash from operating activities", OPERATING),
    ("SECTION", "Investing activities", {}),
    ("TOTAL", "Net cash from investing activities", INVESTING),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", NET_CHANGE),
    ("DATA", "Cash and cash equivalents at the beginning of the period", OPENING),
    ("TOTAL", "Cash and cash equivalents at the end of the period", CLOSING),
]

bw.add_cash_flow_sheet(
    title="Melli Bank plc — Statement of Cash Flows",
    subtitle="Entity-level basis, EUR '000; FY2021 has no Statement of Cash Flows under the FRS 102 exemption",
    rows=cash_rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=270,
    unit_suffix=" (EUR '000)",
)

# ---------------------------------------------------------------
# Asset Quality - FRS 102 entity, no IFRS 9 stage split disclosed; the
# Bank instead assesses impairment loan-by-loan against a small named
# book of Iranian-exposure legacy loans (Note 9's own past-due analysis /
# Note 11's own impairment-provision roll-forward). Coverage and past-due
# ratios computed here as the closest available proxy for NPL/coverage
# ratios given the disclosed granularity.
# ---------------------------------------------------------------
aq_rows = [
    ("SECTION", "Loans and advances to customers (Note 9)", {}),
    ("DATA", "Gross loans and advances to customers", {"FY2025": 23372, "FY2024": 25446, "FY2023": 27718, "FY2022": 27267, "FY2021": 22414}),
    ("DATA", "Impairment provisions (loans and advances to customers only - see Note 11)", {"FY2025": -20055, "FY2024": -21737, "FY2023": -19443, "FY2022": -19007, "FY2021": -13515}),
    ("TOTAL", "Net loans and advances to customers", {"FY2025": 3317, "FY2024": 3709, "FY2023": 8275, "FY2022": 8260, "FY2021": 8899}),
    ("DATA", "of which: past due (any ageing bucket)", {"FY2025": 22164, "FY2024": 23410, "FY2023": 24395, "FY2022": 23373, "FY2021": 17683}),
    ("DATA", "Impairment provision coverage (impairment provisions / gross loans)", {"FY2025": "85.83%", "FY2024": "85.42%", "FY2023": "70.14%", "FY2022": "69.70%", "FY2021": "60.30%"}),
    ("DATA", "Past due ratio (past due / gross loans) - the closest available proxy for an NPL ratio at this entity's disclosed granularity (no IFRS 9 stage split; individually-assessed legacy loan book only)", {"FY2025": "94.83%", "FY2024": "91.99%", "FY2023": "88.01%", "FY2022": "85.73%", "FY2021": "78.90%"}),
    ("SECTION", "Total impairment loss provision, all classes (Note 11 - includes debt securities as well as loans)", {}),
    ("DATA", "Impairment loss provision at year end", {"FY2025": 20076, "FY2024": 22495, "FY2023": 20126, "FY2022": 19713, "FY2021": None}),
]

bw.add_asset_quality_sheet(
    title="Melli Bank plc — Asset Quality",
    subtitle="Entity-level basis, EUR '000. FRS 102 entity - no IFRS 9 stage split disclosed; impairment is assessed loan-by-loan "
              "against a small named book of legacy Iranian-exposure loans (Note 9), most of which are individually past due but "
              "either guaranteed/secured (not impaired) or 100% provided (fully impaired). Coverage and past-due ratios shown here "
              "as the closest available proxy for the usual NPL/coverage ratios given this entity's disclosed granularity.",
    rows=aq_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=100,
    source_height=260,
    unit_suffix=" (EUR '000)",
)


def metric(name, unit, rows_data, note=None, sources_text=None):
    bw.add_metric_sheet(
        name,
        unit,
        rows_data,
        sources_text if sources_text is not None else p3_sources(),
        note=note,
        first_col_width=58,
        source_height=1500,
        note_height=340,
        years=P3_YEARS,
    )


# FY2016/FY2014 additions below are transcribed from the Bank's own Pillar 3
# documents (see P3_2016_URL / P3_2014_URL). Both are text-native PDFs, read
# directly - no OCR involved.
#
# FY2016 Pillar 3, section 4 "Eligible Regulatory Capital", Capital Resources table
# (printed p.17): CET 1 Capital - Share Capital 264,412; Retained Surplus 16,242;
# Total CET 1 Capital 280,654; Total Capital Resources 280,654. All capital is CET1
# that year, following the 19 December 2016 conversion described in the same section.
#
# FY2014 Pillar 3, section 6 "Eligible Regulatory Capital" (printed p.9): Tier 1
# Capital - Share Capital 192,785; Retained Surplus 14,953; Total Tier 1 Capital
# 207,738; Tier 2 Capital 61,810; Total Capital Resources 269,548. The FY2014 edition
# never uses the term "CET1" for its own Tier 1 figure, so the CET1 Capital sheet
# leaves FY2014 blank rather than asserting CET1 = Tier 1 - see that sheet's note.
ELIGIBLE_CAPITAL = {
    "FY2025": 259000,
    "FY2024": 258360,
    "FY2023": 256049,
    "FY2022": 255912,
    "FY2021": 255099,
    "FY2016": 280654,
}
CET1_CAPITAL = dict(ELIGIBLE_CAPITAL)
TIER1_CAPITAL = dict(ELIGIBLE_CAPITAL, FY2014=207738)
TOTAL_CAPITAL = dict(ELIGIBLE_CAPITAL, FY2014=269548)
RWA = {"FY2025": 458000, "FY2024": 466000, "FY2023": 498000, "FY2022": 423000, "FY2021": 399000}
CAPITAL_RATIO = {"FY2025": "56%", "FY2024": "55%", "FY2023": "51%", "FY2022": "60%", "FY2021": "64%"}
LCR = {"FY2025": "679%", "FY2024": "697%", "FY2023": "529%", "FY2022": "617%", "FY2021": "350%",
       "FY2016": "119.16%"}
# GA-006 (2026-09-18): FY2021-FY2025 now carry the non-disclosure statement in the
# cell rather than being left blank, matching how the NSFR and MREL sheets in this
# same workbook already present an evidenced absence. See LEVERAGE_NOTE for the
# richness-controlled evidence behind it.
LEVERAGE = {"FY2016": "75%", "FY2014": "approximately 60%"}
# GA-020 (2026-09-19): all five Annual Reports FY2021-FY2025 (CH / HKMA scans) re-OCR'd at
# 200 dpi. 'leverage' occurs only in the credit-risk sentence about borrowers' "liquidity,
# leverage, profitability"; 'NSFR'/'stable funding' only in FY2025 narrative ("continues to
# monitor ... Net Stable Funding Ratio"), never a figure; 'MREL'/'eligible liabilities'/
# 'loss-absorb' zero in all five (richness: 'capital' 29-35 hits each). The Directors'
# report says the Pillar 3 is 'available on request' (FY2021/22/24/25) - but for FY2023 it
# says 'available on the Bank's website', and that edition was never obtained: mellibank.com
# times out (2026-09-19), Wayback CDX from 2023 holds no report/Pillar 3 file (only
# compliance PDFs), and the Pillar 3 is not a Companies House filing. FY2023 is therefore
# UNREACHED, not "not published" - the one year a public edition may exist.
def _ga020(term):
    d = {y: ("Not published – no " + term + " in Melli AR " + y + " (OCR, 2026-09-19); Directors' report says "
             "Pillar 3 is 'available on request' only.") for y in ["FY2025", "FY2024", "FY2022", "FY2021"]}
    # GA-020 unreached pass, 2026-09-19: the Bank's own /reports page, in every Wayback
    # capture from 4 Jun 2023 to 17 May 2026 (20230604145859, 20250209023014,
    # 20260517153413), reads "Financial Statements and Pillar 3 Disclosures are available
    # on request" and links no report file at all. So the edition the FY2023 AR points to
    # is, on the Bank's own website, an on-request document: still UNREACHED, not
    # "not published". Also tried: CDX of mellibank.com and mellibank.co.uk
    # (matchType=domain, no mimetype filter: 266 + 294 URLs; newest Pillar 3 file is the
    # 2016 edition); the HKMA VPR folder for the HK branch (100273) holds annual reports
    # only; live site timed out again over HTTP/1.1.
    # Common Crawl pass, 2026-09-19: mellibank.com and mellibank.co.uk (every host, every path) in all
    # 31 crawls CC-MAIN-2024-10..2026-39 (self-hosted ZipNum lookup on data.commoncrawl.org): the only
    # files are compliance PDFs (File/DownloadComplianceFiles?filename=Wolfsberg/FSCS/AML/W-8BEN...),
    # no Pillar 3 or report file; the /reports page's CC-MAIN-2024-46 capture (2024-11-03, fetched,
    # CC-MAIN-20241102231001-20241103021001-00360.warc.gz offset 370157579) carries the same 'available
    # on request' sentence and no report link. Log: wayfinder/gaps/ga020/unreached/done/MELLI BANK.jsonl
    d["FY2023"] = ("Unreached today – FY2023 AR (no " + term + ") points to the website, but mellibank.com/reports "
                   "(Wayback Jun 2023-May 2026) says Pillar 3 is 'available on request'; site times out (2026-09-19); "
                   "Common Crawl 2024-10..2026-39 checked.")
    return d
LEVERAGE.update(_ga020("leverage ratio"))
NSFR_ST = dict(_ga020("NSFR figure"),
               FY2016="Not published – Melli Pillar 3 FY2016 (read in full) says NSFR is used to manage funding risk "
                      "but gives no figure.",
               FY2014="Not published – Melli Pillar 3 FY2014 (read in full) does not mention stable funding.")
MREL_ST = dict(_ga020("MREL figure"),
               FY2016="Not published – Melli Pillar 3 FY2016 (read in full) does not mention MREL or eligible liabilities.",
               FY2014="Not published – Melli Pillar 3 FY2014 (read in full) does not mention MREL or eligible liabilities.")

CAPITAL_NOTE = (
    "FY2021-FY2025: eligible regulatory capital is 100% CET1 in the disclosed KPI/capital-management tables; "
    "the same disclosed amount is therefore shown for CET1, Tier 1 and Total Capital. Values are EUR '000. "
    "FY2025's own KPI table (Annual Report and Accounts 2025, p.10, 'Capital and Liquidity Position') is presented "
    "in whole EUR millions only (a changed presentation from prior years' more precise KPI table, coinciding with "
    "the September 2025 sanctions re-imposition) - the FY2025 figure (259) is therefore rounded to the nearest EUR "
    "million before conversion to EUR '000, one significant figure less precise than FY2021-FY2024's figures.\n"
    "FY2016 (from the Bank's own Pillar 3, section 4, Capital Resources table): Total CET 1 Capital EUR 280,654k = "
    "Share Capital EUR 264,412k + Retained Surplus EUR 16,242k, and Total Capital Resources the same EUR 280,654k. "
    "The all-CET1 position is not an assumption: the document states 'At 31 December 2016, the Bank's capital "
    "resources amounted to EUR 280,654,000 (2015: EUR 278,147,000) all of which was Common Equity Tier One "
    "(\"CET1\") capital', and explains why - on 19 December 2016 the Bank issued 71,626,396 EUR1 shares to Bank "
    "Melli Iran for cash and on the same day redeemed and repaid all of the US$75m Subordinated Loan Notes that had "
    "qualified as Tier 2, 'effectively convert[ing] the tier 2 capital into CET1 capital'. So CET1 = Tier 1 = Total "
    "Capital for FY2016 by the Bank's own statement.\n"
    "FY2014 (from the Bank's own Pillar 3, section 6, Capital Resources table): Total Tier 1 Capital EUR 207,738k = "
    "Share Capital EUR 192,785k + Retained Surplus EUR 14,953k; Tier 2 Capital EUR 61,810k; Total Capital Resources "
    "EUR 269,548k. The Tier 2 is described as 'subordinated floating rate loan notes of US$75m issued to Bank Melli "
    "Iran', repayable 15 November 2050 - the same notes retired in December 2016. FY2014 is therefore the one year "
    "on these sheets where Tier 1 and Total Capital genuinely DIFFER, and the difference is real, not a "
    "transcription artefact.\n"
    "WHY FY2014 IS BLANK ON THE CET1 CAPITAL SHEET: the FY2014 edition labels its figure 'Total Tier 1 Capital' and "
    "never uses the term CET1 for it (CET1 appears in that document only in the forward-looking CRD IV buffer "
    "discussion). Its components - share capital and retained surplus, with no AT1 instrument named - would make it "
    "CET1 on any ordinary reading, but that is an inference and this project transcribes only what a document "
    "states. Recorded as a deliberate blank, not an unresearched gap.\n"
    "FY2015 IS DELIBERATELY NOT SHOWN AS A COLUMN, and this is a recorded decision rather than an oversight. No "
    "FY2015 Pillar 3 document survives; FY2015 figures exist only as narrative comparatives inside the FY2016 "
    "edition, and that edition is INTERNALLY INCONSISTENT about them: section 4 says capital resources were 'EUR "
    "278,147,000' at 31 December 2015 'of which 75% [was CET1] amounting to EUR 209,264,000', while section 5.5 of "
    "the same document says 'Euro 276m of which 75% was CET1 capital'. 75% of 278,147 is 208,610, not 209,264. Both "
    "statements are recorded here as they stand and neither is reconciled to the other; no FY2015 cell is written "
    "from either."
)
RATIO_NOTE = (
    "FY2021-FY2025: the Bank discloses a single Total Capital Ratio and states all capital is CET1; the ratio is "
    "shown as the CET1, Tier 1 and Total Capital ratio.\n"
    "FY2016 AND FY2014 ARE BLANK BECAUSE NO RATIO IS DISCLOSED, AND MUST NOT BE COMPUTED. Neither Pillar 3 edition "
    "states a capital ratio as a percentage anywhere. The FY2016 edition comes closest - 'significantly "
    "strengthening the core CET1 capital ratio, which is now equal to the Total Capital Ratio' - but gives no "
    "number. Both editions disclose a Pillar 1 MINIMUM CAPITAL REQUIREMENT (FY2016 EUR 30,383k, FY2014 EUR "
    "23,792k) and describe it as capital held 'of at least 8%' against risk weighted exposure. Dividing capital "
    "resources by a requirement grossed up at 8% would be back-solving a ratio from a floor, which this project "
    "forbids and which would in any case produce a number the Bank never published. Left blank deliberately."
)
RWA_NOTE = (
    "FY2021-FY2025: Total Risk Exposure Amount is the directly disclosed regulatory KPI, shown in EUR '000 (source "
    "table reports EUR millions for every year FY2021-FY2025, so no year loses precision relative to another here - "
    "unlike the Eligible Capital figure, see CET1 Capital sheet note).\n"
    "FY2016 AND FY2014 ARE BLANK, AND DELIBERATELY SO. Neither Pillar 3 edition states a risk weighted assets or "
    "total risk exposure amount figure. What each DOES state is the Pillar 1 minimum capital requirement, broken "
    "down by risk category (EUR '000):\n"
    "  FY2016 - Credit risk 29,249; Market risk nil ('The Bank does not have a trading book' and 'does not allocate "
    "capital for market risk as the net foreign exchange position is less than 2% of total own funds'); "
    "Operational risk 1,134 (Basic Indicator Approach); TOTAL 30,383.\n"
    "  FY2014 - Credit risk 22,658; Market risk 0; Operational risk 1,134; TOTAL 23,792.\n"
    "  FY2016 credit risk by exposure class: Central governments or Central banks 7,439; Institutions 18,460; "
    "Exposures in default 2,691; Other items 659.\n"
    "  FY2014 credit risk by exposure class: Central governments or Central banks 4,659; Institutions 13,448; "
    "Corporates 104; Past due items 3,474; Other items 972.\n"
    "These are CAPITAL REQUIREMENTS, not RWAs. Multiplying them by 12.5 (the inverse of the 8% floor each document "
    "cites) would be back-solving, and the result would not be a disclosed figure - so it is not done here, and no "
    "RWA cell is written for FY2016 or FY2014. The figures are recorded in this note so the disclosure is not lost, "
    "and are kept OUT of the RWA Breakdown sheet's rows so they can never be read as RWAs by anything consuming "
    "this workbook."
)
GAP_NOTE = (
    "Not publicly disclosed for this entity/year in the reviewed official source set. For FY2021-FY2025 the Bank's "
    "own reports state that the Pillar 3 disclosure is available on request rather than published, and no public "
    "KM1 document exists. For FY2016 and FY2014 the Bank's actual Pillar 3 documents were obtained and read in "
    "full (see the source note below) and simply do not disclose this metric."
)
LEVERAGE_NOTE = (
    "FY2016 and FY2014 are the only years with a leverage ratio, and both come from the Bank's own Pillar 3 "
    "documents:\n"
    "  FY2016 (section 7, Leverage): 'The Bank's year-end 2016 Leverage Ratio under Basel III is 75% (versus a "
    "minimum regulatory requirement of 3%).'\n"
    "  FY2014 (section 9, Leverage): 'The Bank's year-end Leverage Ratio under Basel 3 is APPROXIMATELY 60% (versus "
    "a minimum of 3%).' The word 'approximately' is the Bank's own and is preserved verbatim in the cell rather "
    "than being silently rendered as a precise 60% - the document does not offer a precise figure, and both "
    "editions add that 'detailed statistics will not become relevant until normal business recommences and "
    "significant balance sheet expansion takes place', the position of a sanctioned bank holding a large capital "
    "base against a shrunken balance sheet.\n"
    "FY2021-FY2025 record 'Not publicly disclosed': no leverage ratio appears in any of those years' Annual "
    "Reports, and no Pillar 3 document exists for them to appear in.\n"
    "EVIDENCE FOR THAT ABSENCE, re-established independently 2026-09-18 (GA-006), because every Melli source is "
    "an image scan and a zero from an unreadable document is worth nothing. The FY2025 Annual Report (Companies "
    "House, a go-tiff2pdf scan with no text layer at all - pdftotext returns zero characters for all 54 pages) "
    "was rendered at 200dpi and OCR'd across its whole front section. 'Leverage' appears ZERO times, against a "
    "richness control in the SAME extraction of 19 hits for 'capital', 65 for 'ratio' and 18 for 'liquidity' - "
    "so the zero is a fact about the document, not about the extraction. Decisively, the 'Capital and Liquidity "
    "Position' KPI table was read in full and its eight rows are: Shareholders' Equity, Eligible Capital, Total "
    "Assets, Total Risk Exposure Amount, Total Capital Ratio, Equity to Assets Ratio, Liquidity Coverage Ratio, "
    "Total Net Income. There is no leverage row, and that table is the only place the metric could sit. Its two "
    "columns are 2025 and 2024, so FY2024 is covered by the same reading. The FY2023 edition (Hong Kong Monetary "
    "Authority register, also an image scan) was checked the same way and gives the same result - zero "
    "'leverage' against 18 'capital', 41 'ratio' and 11 'liquidity' - which covers FY2023 and its FY2022 "
    "comparative. This is an evidenced absence, not a failed search."
)
LCR_NOTE = (
    "FY2021-FY2025: directly disclosed in the Annual Report KPI tables. FY2021 is reported in the FY2023 Annual "
    "Report KPI comparative table (p.9); FY2022-FY2025 are reported in the later corresponding KPI tables.\n"
    "FY2016: 119.16%, from the Bank's own Pillar 3 document, section 8 (Liquidity): 'The Bank's year-end 2016 "
    "Liquidity Coverage Ratio was 119.16% (versus a minimum regulatory requirement of 80%).'\n"
    "BASIS - IMPORTANT: every figure on this row is a POINT-IN-TIME YEAR-END ratio, not a 12-month average. The "
    "FY2016 figure says 'year-end' in terms. Melli publishes no UK KM1 table (which would carry a 12-month "
    "average), so there is no average series in existence for this bank; if one is ever obtained it must go on its "
    "own row and must not be merged into this one.\n"
    "FY2014 IS BLANK, and the FY2014 Pillar 3 explains why in its own words: its entire Liquidity section reads "
    "'Whilst the Bank maintains large short term deposit balances with banks, the PRA acknowledges that the "
    "sanctions prevent it undertaking most financial transactions (including the purchase of higher quality assets) "
    "which prevent the Bank from improving its Liquidity Coverage Ratio.' The ratio is discussed but never "
    "quantified. That is a disclosed non-disclosure, not a retrieval gap."
)
NSFR_NOTE = (
    GAP_NOTE + "\n"
    "SPECIFIC TO FY2016: the Bank's own FY2016 Pillar 3 document mentions the NSFR - 'In addition to the Liquidity "
    "Coverage Ratio, the Bank also uses the Liquidity Maintenance Ratio (for the Hong Kong Branch) and the Net "
    "Stable Funding Ratio to manage its liquidity and funding risk' - but gives no figure for it. The FY2014 "
    "edition does not mention stable funding at all. Both blanks are therefore evidenced against the primary "
    "documents. Note also that the UK NSFR became a binding requirement only from 1 January 2022, so FY2014 and "
    "FY2016 blanks are structural as well as evidenced."
)

# ---------------------------------------------------------------
# KM1 Key Metrics - NOT APPLICABLE. Melli Bank plc has never published a UK KM1
# template, in any year, and the reason is structural rather than a search
# failure. Three separate findings stack up, and all three are positive:
#
#   1. TIMING. The UK KM1 template arrived with the Disclosure (CRR) Part of
#      the PRA Rulebook, applying from 1 January 2022. The only two Melli
#      Pillar 3 documents that have ever been public are the FY2014 and FY2016
#      editions, which pre-date it by five and six years respectively. Both
#      were re-read cover to cover for this ticket: they are narrative CRD
#      IV-era documents whose contents pages run "Eligible Regulatory Capital /
#      Capital Adequacy / Credit Risk Adjustments / Leverage / Liquidity /
#      Additional Disclosures", with no tabular key-metrics template of any
#      kind and no occurrence of the string "KM1" or "key metrics" anywhere.
#
#   2. PUBLICATION. For every year from 1 January 2022 onward - the years in
#      which a KM1 would have been required - the Bank's own Directors' report
#      states that its Pillar 3 disclosure is "available on request" rather
#      than published. The FY2025 report (p.11 of 54, "Basel III - Pillar 3
#      Disclosure") reads in full: "The Pillar 3 disclosure is available on
#      request." A document that is not published has no published KM1.
#
#   3. THE ANNUAL REPORT'S OWN TABLE IS NOT A KM1, and is not reshaped into
#      one. The FY2025 report's "Capital and Liquidity Position" table (p.10 of
#      54) has eight rows - Shareholders' Equity, Eligible Capital, Total
#      Assets, Total Risk Exposure Amount, Total Capital Ratio, Equity to
#      Assets Ratio, Liquidity Coverage Ratio, Total Net Income - with no row
#      numbers, no SREP rows, no buffer rows, no leverage row and no NSFR row.
#      That is a different and shorter table, not an unnumbered template (map
#      rule 8), and the KM1 sheet is not back-filled from it.
#
# SEPARATELY: the Bank's own website is UNREACHABLE, which is recorded as
# BLOCKED and is NOT the basis of any claim above. Re-tested 2026-09-16 -
# mellibank.com and www.mellibank.com resolve to 62.232.194.164 and
# mellibank.co.uk to 195.224.32.52, and all four hostnames time out on both
# http and https (curl exit 28 after 25s), consistent with the 29 September
# 2025 sanctions designation. None of the three findings above depends on that
# site; each rests on a document the Bank filed and that was read directly.
# ---------------------------------------------------------------
KM1_SOURCES = (
    "Sources - every document behind the 'Not applicable' finding on this sheet, each read directly rather than "
    "inferred:\n"
    f"FY2025: Annual Report and Accounts 2025, Directors' Report p.11 of 54, 'Basel III - Pillar 3 Disclosure: The "
    f"Pillar 3 disclosure is available on request'; and 'Capital and Liquidity Position' p.10 of 54, the eight-row "
    f"KPI table that is NOT a KM1 - {AR2025_URL}\n"
    f"FY2024: Annual Report and Accounts 2024, same 'available on request' wording - {AR2024_URL}\n"
    f"FY2023: Annual Report and Accounts 2023 - {AR2023_URL}\n"
    f"FY2022: Annual Report and Accounts 2022 - {AR2022_URL}\n"
    f"FY2021: Annual Report and Accounts 2021 - {AR2021_URL}\n"
    f"FY2016: Pillar 3 Disclosures as at 31st December 2016, 23pp, re-read in full 2026-09-16 (HTTP 200, "
    f"application/pdf, %PDF magic bytes) - no KM1 table, no 'key metrics' heading - {P3_2016_URL}\n"
    f"FY2014: Pillar 3 Disclosures as at 31st December 2014, 16pp - same finding - {P3_2014_URL}\n"
    f"Companies House filing history (company 04152338), read live 2026-09-16 - {CH_FILING_HISTORY_URL}\n\n"
    "WHY THIS SHEET IS 'NOT APPLICABLE', in three independent findings:\n"
    "1. TIMING. The UK KM1 template arrived with the Disclosure (CRR) Part of the PRA Rulebook and applies from 1 "
    "January 2022. The only two Melli Pillar 3 documents that have ever been public are the FY2014 and FY2016 "
    "editions, which pre-date it. Both were re-read cover to cover for this ticket. Their contents pages run "
    "'Eligible Regulatory Capital / Capital Adequacy / Credit Risk Adjustments / Leverage / Liquidity / Additional "
    "Disclosures'; there is no tabular key-metrics template of any kind and no occurrence of 'KM1' or 'key metrics' "
    "anywhere in either document. Those zero hit-counts are a fact about the documents rather than about the "
    "extraction, which was shown to be rich on neighbouring terms first: the FY2016 text yields 112 hits for "
    "'capital', 65 for 'ratio', 42 for 'liquidity', 13 for 'CET', 9 for 'Tier', 5 for 'leverage' and 252 for "
    "'risk' (FY2014: 80/52/10/1/7/5/153), against 0 for 'KM1' and 0 for 'key metric'. This was checked against "
    "images as well as text, because a KM1 table can be "
    "published as a bitmap inside an otherwise text-native PDF and then extract as nothing at all: `pdfimages "
    "-list` on both editions returns only the 203x73 letterhead logo repeated on every page, plus one larger "
    "image on page 5 of each, and both of those were rendered at 150dpi and looked at - they are governance "
    "organisation charts (FY2016: Main Board / Board Risk Committee / ALCO; FY2014: Board of Directors / "
    "Executive and Non-Executive Committees), not tables. There is no image anywhere in either document that "
    "could be concealing a key-metrics table.\n"
    "2. PUBLICATION. For every year from 2022 onward - exactly the years in which a KM1 would have been required - "
    "the Bank's own Directors' report says its Pillar 3 disclosure is 'available on request' rather than published. "
    "The FY2025 report's Basel III - Pillar 3 Disclosure section reads, in full: 'The Pillar 3 disclosure is "
    "available on request.' An unpublished document has no published KM1. (FY2023 is the one year whose Directors' "
    "report claims website publication; see the PILLAR 3 PUBLICATION HISTORY below, where that claim and the "
    "website's own contradicting statement are both recorded and neither is treated as correcting the other.)\n"
    "3. THE ANNUAL REPORT'S OWN TABLE IS NOT A KM1, and is deliberately not reshaped into one. The FY2025 report's "
    "'Capital and Liquidity Position' table (p.10 of 54) has eight rows - Shareholders' Equity EUR259m, Eligible "
    "Capital EUR259m, Total Assets EUR363m, Total Risk Exposure Amount EUR458m, Total Capital Ratio 56%, Equity to "
    "Assets Ratio 71%, Liquidity Coverage Ratio 679%, Total Net Income EUR12,286k - with no row numbers, no SREP "
    "rows, no buffer rows, no leverage row and no NSFR row. It is a different and shorter table, in the same class "
    "as ABC International Bank's 'Table 3 Key Regulatory Metrics' rather than as Europe Arab Bank's unnumbered "
    "template. Those figures do populate this workbook's individual metric sheets, where they belong; mapping them "
    "onto KM1 row numbers would invent a correspondence the Bank never published.\n\n"
    "BLOCKED, NOT ABSENT - recorded so it is never mistaken for evidence. The Bank's own website is unreachable. "
    "Re-tested 2026-09-16: mellibank.com and www.mellibank.com resolve to 62.232.194.164 and mellibank.co.uk to "
    "195.224.32.52, and all four hostnames time out on both http and https (curl exit 28 after 25 seconds), "
    "consistent with the 29 September 2025 sanctions designation recorded in the Bank's own FY2025 report. That is "
    "a fact about reachability, not about publication, and NONE of the three findings above rests on it - each "
    "rests on a document the Bank filed and that was read directly.\n\n"
    "LATEST-EDITION CHECK, 2026-09-16. With the Bank's own site unreachable, the two live routes recorded in the "
    "ACCESS ROUTES note were used instead. Companies House (company 04152338) was read live: the newest accounts "
    "filed are 'made up to 31 December 2025', filed 21 June 2026, signed 28 April 2026 - which is the FY2025 "
    "edition this workbook already holds. Nothing newer exists. The Hong Kong Monetary Authority public register "
    "(institution 100273) currently goes only as far as FY2024: .../ar_24/ar_24_eng.pdf returns a real PDF (HTTP "
    "200, application/pdf, 2.9MB) while .../ar_25/ar_25_eng.pdf returns HTTP 200 with Content-Type text/html - a "
    "SOFT-404, not a document. Worth writing down because the status code alone would have said 'found'.\n\n"
    + PILLAR3_HISTORY_NOTE + "\n\n" + ACCESS_ROUTES_NOTE + "\n\n" + ENTITY_NOTE
)

bw.add_km1_sheet(
    title="Melli Bank plc — KM1 Key Metrics",
    subtitle="Not applicable. The Bank has never published a UK KM1 template. Its only two ever-public Pillar 3 "
             "documents (FY2014 and FY2016) pre-date the template, and for every year from 2022 onward - when a "
             "KM1 would have been required - its own Directors' report states the Pillar 3 disclosure is "
             "'available on request' rather than published. The Annual Report's eight-row 'Capital and Liquidity "
             "Position' KPI table is not the template and is not reshaped into it. The Bank's website is "
             "unreachable under sanctions; that is recorded as BLOCKED and is not the basis of this finding.",
    # GA-006 (2026-09-18): the "not applicable" finding was stated only in this
    # sheet's subtitle and in the row LABEL, leaving all 7 year columns blank to a
    # reader and scored as 7 empty year-columns by audit_gaps.py. The finding was
    # never in doubt; it simply was not in the columns. It is now, per year.
    rows=[("DATA", "UK KM1 - Key metrics template",
           {y: "Not applicable - no UK KM1 template ever published by this entity" for y in P3_YEARS})],
    sources_text=KM1_SOURCES,
    first_col_width=88,
    source_height=1500,
    years=P3_YEARS,
)


metric("CET1 Capital", "EUR '000", [("Common Equity Tier 1 / eligible regulatory capital", CET1_CAPITAL)], note=CAPITAL_NOTE)
metric("CET1 Ratio", "%", [("CET1 capital ratio", CAPITAL_RATIO)], note=RATIO_NOTE)
metric("Tier 1 Capital", "EUR '000", [("Tier 1 / eligible regulatory capital", TIER1_CAPITAL)], note=CAPITAL_NOTE)
metric("Tier 1 Ratio", "%", [("Tier 1 capital ratio", CAPITAL_RATIO)], note=RATIO_NOTE)
metric(
    "Total Capital", "EUR '000",
    [
        ("Total regulatory capital / eligible capital", TOTAL_CAPITAL),
        ("of which: Tier 2 capital (US$75m subordinated floating rate loan notes issued to Bank Melli Iran, "
         "redeemed and repaid in full 19 December 2016)", {"FY2014": 61810}),
    ],
    note=CAPITAL_NOTE,
)
metric("Total Capital Ratio", "%", [("Total capital ratio", CAPITAL_RATIO)], note=RATIO_NOTE)
metric("Total RWAs", "EUR '000", [("Total risk exposure amount", RWA)], note=RWA_NOTE)

bw.add_rwa_breakdown_sheet(
    title="Melli Bank plc — RWA Breakdown",
    subtitle="Not disclosed at category level for any year - including in the Bank's own FY2016 and FY2014 Pillar 3 documents. EUR '000. See source note.",
    # GA-006 (2026-09-18): same fix as the KM1 sheet above - the evidenced
    # non-disclosure now appears in each year column instead of only in the label.
    rows=[("DATA", "RWA breakdown by risk category",
           {y: "Not disclosed at category level in any surviving source" for y in P3_YEARS})],
    sources_text=p3_sources(
        "RWA BREAKDOWN: no category-level (credit risk / market risk / operational risk / CVA) RWA breakdown is "
        "disclosed for ANY year, FY2014 through FY2025 - and as of 2026-09-16 that now covers the Bank's own "
        "Pillar 3 documents as well as its Annual Reports, so it is an evidenced non-disclosure across every "
        "surviving source rather than an inference from the annual reports alone.\n"
        "FY2021-FY2025: each year's own 'Capital management' note (and, for FY2025, the 'Capital and Liquidity "
        "Position' KPI table on p.10) discloses only the aggregate Total Risk Exposure Amount shown on the Total "
        "RWAs sheet, consistent with the reports' own statement that full Pillar 3 disclosure is available on "
        "request rather than published. All 5 Annual Reports were fully read, including the current FY2025 report. "
        "RE-VERIFIED 2026-09-12 (independent second pass): re-downloaded and OCR'd the live FY2025 Annual Report "
        "directly and confirmed the same 'Basel III - Pillar 3 Disclosure / The Pillar 3 disclosure is available "
        "on request' statement, plus the KPI table's Total Risk Exposure Amount (EUR 458m FY2025 / EUR 466m "
        "FY2024) with no category split anywhere in the document.\n"
        "FY2016 AND FY2014: the two surviving Pillar 3 documents were read in full on 2026-09-16. Neither states "
        "an RWA figure at all - not in total and not by category. What each discloses instead is the Pillar 1 "
        "MINIMUM CAPITAL REQUIREMENT by risk category and by exposure class; those numbers are set out in full on "
        "the Total RWAs sheet's note. They are NOT reproduced as rows on this sheet, and deliberately so: a "
        "capital requirement placed in an RWA breakdown would be understated by a factor of 12.5 to anything "
        "reading this workbook, and grossing it up to an RWA would be back-solving from the 8% floor. So this "
        "sheet stays empty for those two years while the underlying disclosure is preserved in prose."
    ),
    first_col_width=54,
    source_height=1500,
    unit_suffix=" (EUR '000)",
    years=P3_YEARS,
)

metric("Leverage Ratio", "%", [("Leverage ratio (year-end, Basel III)", LEVERAGE)], note=LEVERAGE_NOTE)
metric("LCR", "%", [("Liquidity Coverage Ratio (point-in-time, year-end)", LCR)], note=LCR_NOTE)
metric("NSFR", "%", [("NSFR", NSFR_ST)], note=NSFR_NOTE)
metric(
    "MREL Ratio", "%",
    [("MREL Ratio", MREL_ST)],
    note=GAP_NOTE + "\nSPECIFIC TO FY2016 AND FY2014: both Pillar 3 documents were read in full and neither "
                    "mentions MREL, minimum requirement for own funds and eligible liabilities, or resolution "
                    "planning of any kind - unsurprising for a sanctioned bank whose stated objective in both "
                    "documents is simply 'to ensure that it continues to meet the Threshold Conditions of the PRA "
                    "and retains its authorisation', and which pre-dates the UK MREL regime's application to firms "
                    "of this size. Evidenced blanks, not gaps.",
)

def _row_values(rows, label):
    for kind, lbl, values in rows:
        if lbl == label:
            return values
    raise KeyError(label)


bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", _row_values(bs_rows, "Total assets")),
        ("Loans and advances to customers", _row_values(bs_rows, "Loans and advances to customers")),
        ("Customer accounts", _row_values(bs_rows, "Customer accounts")),
        ("Total equity", _row_values(bs_rows, "Total equity")),
    ],
    balance_sheet_unit="EUR '000",
    income_statement_totals=[
        (
            "Total revenue / Total net income",
            _row_values(
                pl_rows,
                "Total revenue / Total net income (FY2025's own report relabels this subtotal 'Total net income' - same position in the account, not a different line)",
            ),
        ),
        ("Administrative expenses", _row_values(pl_rows, "Administrative expenses")),
        ("Profit/(loss) for the financial year", _row_values(pl_rows, "Profit/(loss) for the financial year")),
    ],
    income_statement_unit="EUR '000",
    equity_changes_totals=[
        ("Opening equity", {"FY2021": 262953, "FY2022": 255612, "FY2023": 256130, "FY2024": 256532, "FY2025": 258664}),
        ("Total comprehensive income/(loss) for the year", {"FY2021": -7320, "FY2022": 518, "FY2023": 402, "FY2024": 2132, "FY2025": 181}),
        ("Other equity movements, net", {"FY2021": -21, "FY2022": 0, "FY2023": 0, "FY2024": 0, "FY2025": 0}),
        ("Closing equity", {"FY2021": 255612, "FY2022": 256130, "FY2023": 256532, "FY2024": 258664, "FY2025": 258845}),
    ],
    equity_changes_unit="EUR '000",
    cash_flow_totals=[
        ("Net cash from operating activities", OPERATING),
        ("Net cash from investing activities", INVESTING),
        ("Cash and cash equivalents at end of year", CLOSING),
    ],
    cash_flow_unit="EUR '000",
    ratios=[("CET1 Ratio", CAPITAL_RATIO), ("LCR", LCR)],
    note="FY2021 has no Statement of Cash Flows at all in the source Annual Report - the Company applied the FRS 102 "
         "qualifying-entity exemption, confirmed by both its accounting policy note and its own Contents page. "
         "FY2025 cash flow figures were added this batch from the Annual Report and Accounts 2025's own Statement "
         "of Cash Flows (p.26).\n"
         "THIS OVERVIEW COVERS FY2021-FY2025 ONLY. The Pillar 3 sheets in this workbook run deeper - they carry "
         "FY2016 and FY2014 columns as well, transcribed from the only two Pillar 3 disclosure documents Melli Bank "
         "plc has ever made public (both recovered from the Internet Archive; the Bank's own site is down). That "
         "extra depth is not replicated here because there are no FY2016/FY2014 statement figures in this "
         "workbook's window, and because this Overview is a COPY of the detail sheets rather than a source. For "
         "the leverage ratio (75% at end-2016, 'approximately 60%' at end-2014), the FY2016 LCR (119.16%) and the "
         "FY2016/FY2014 capital resources, read the Pillar 3 sheets directly. Those sheets also carry the full "
         "publication history explaining which missing years are closed questions and which are worth a written "
         "request to the Bank.",
)

bw.save("/Users/armaan/code/katalysis/banks/MELLI BANK FINANCIALS.xlsx")
