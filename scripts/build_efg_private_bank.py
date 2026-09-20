import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# FY2025 ADDED 2026-09-16 (KM1-012 latest-edition check). The earlier note here
# said only 4 years were available because the FY2025 accounts were not yet filed
# as of the 2026-08-28 build. They have since been filed: Companies House shows
# "Full accounts made up to 31 December 2025" filed 14 September 2026, and EFG
# published its FY2025 Pillar 3 on 1 September 2026. Both are transcribed below.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = ("https://find-and-update.company-information.service.gov.uk/company/02321802/"
              "filing-history/MzU0NDEyNDQ4MWFkaXF6a2N4/document?format=pdf&download=0")
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
# locatable" conclusion - now corrected everywhere in this file, see PILLAR3_REACH_NOTE).
#
# CORRECTED 2026-09-18 (KM1-032). This comment used to continue: "No earlier-year standalone
# Pillar 3 report for this entity was locatable via web search or the Wayback Machine (CDX
# search of efginternational.com's 'pillar' and 'investor' URL patterns turns up only EFG
# International Group-level and EFG Bank (Luxembourg) S.A. reports, never an EFG Private Bank
# Limited-specific one) - the FY2024 edition appears to have been the first standalone
# entity-level Pillar 3 report EFGIUK published." The parenthetical was false about a result
# set this project already had. An unfiltered CDX sweep of efginternational.com* (26,072 rows)
# contains 47 "pillar" URLs, and one of them IS an EFG Private Bank Limited document, at the
# very jcr asset id cited elsewhere in this file:
#   https://www.efginternational.com/doc/jcr:895b914b-441b-48b6-9853-0b3aeaa4e2fd/2018%20Pillar%20III%20Disclosure.pdf
# captured 20220630160355 and 20250805050752. Fetched via the Wayback id_ raw form: HTTP 200,
# application/pdf, %PDF, 41,426 bytes, 2 pages, opening "Remuneration Code / 2018 Pillar 3
# disclosure ... Remuneration policy for EFG Private Bank Limited (EFGIUK) and its subsidiaries
# ... Registered no. 2321802" - the same company number as the Companies House URLs below. It
# is an entity-level UK Pillar 3 disclosure under CRR Article 450.
#
# So EFGIUK published at least one standalone entity-level Pillar 3 before FY2024. The row it
# sits on MATCHES the "pillar" filter, so the miss was not in the filter - the result set was
# not read to the end. A filtered sweep whose output is skimmed produces a negative that looks
# method-backed and is not. FY2019-FY2023 remain genuinely unestablished.
#
# MECHANICAL FINDING, established with a negative control, which also corrects this file's own
# explanation of the "one URL, two editions" puzzle: on this host the filename segment in
# /doc/jcr:<id>/<name>.pdf is DECORATIVE - the jcr id alone addresses the asset. The real 2018
# filename, the FY2024 filename and an invented NOT_A_REAL_FILE_ctrl.pdf all return the same
# 5,881,612-byte FY2025 report. EFG did not republish over an asset while keeping an old
# filename; the filename never identified anything. Likewise, the statement elsewhere in this
# file that CDX on the exact jcr: asset returns nothing is wrong - it holds two captures,
# indexed under the asset's 2018 display name.
#
# ===============================================================================================
# 2026-09-16, KM1-012: THIS ONE URL HAS SERVED TWO DIFFERENT EDITIONS. Its path still spells
# "...2024 Pillar 3 Disclosure Report.pdf", but the file it now returns is the **FY2025** report:
# title page "Pillar 3 Disclosures / For the year ended 31 December 2025", PDF CreationDate
# 1 September 2026, running footer "Pillar 3 Disclosures 2025", KM1 columns 31 Dec 2025 / 31 Dec
# 2024. EFG republished the new edition over the old asset and kept the old filename. Verified
# 2026-09-16: HTTP 200, Content-Type application/pdf, 5,881,612 bytes, %PDF magic bytes, 28 pages.
#
# Consequences, both of which this file now handles explicitly:
#  (1) The FY2024 edition is NO LONGER RETRIEVABLE at this or any known address, and the Wayback
#      Machine has no capture of it (CDX on the exact jcr: asset returns nothing; a full domain
#      CDX listing of efginternational.com, 26,498 rows, contains 47 "pillar" URLs and not one of
#      them is an EFG Private Bank Limited report). The FY2024 KM1 figures recorded in
#      PILLAR3_FY2024_EDITION_NOTE below, transcribed from that edition on 2026-09-04, are now the
#      only surviving record of it in this project. They are kept verbatim and are NOT overwritten
#      with the FY2025 edition's restated comparative.
#  (2) A citation naming this URL for an FY2024 figure would now point a reader at a document that
#      does not contain it. Every such citation below says so.
# ===============================================================================================
PILLAR3_URL = ("https://www.efginternational.com/doc/jcr:895b914b-441b-48b6-9853-0b3aeaa4e2fd/"
               "EFG%20Private%20Bank%20Limited%202024%20Pillar%203%20Disclosure%20Report.pdf/"
               "lang:en/EFG%20Private%20Bank%20Limited%202024%20Pillar%203%20Disclosure%20Report.pdf")
# Kept as an alias so no existing reference in this file silently changes meaning.
PILLAR3_2025_URL = PILLAR3_URL

# The correction that replaces the old "no standalone Pillar 3 document was locatable" sentence
# everywhere it used to appear. That sentence was a fact about OUR REACH, not about the Bank.
PILLAR3_REACH_NOTE = (
    "REACH, NOT ABSENCE - correction recorded 2026-09-04 and completed 2026-09-16. An earlier build "
    "of this workbook stated that no standalone Pillar 3 document could be located for this entity. "
    "That was wrong, and the cause was a blocked fetch being written down as a fact about the Bank: "
    "efginternational.com returns HTTP 403 to a bare curl with no User-Agent, and still does (every "
    "HTML page on the host was re-tested on 2026-09-16 and returned 403, including with a full "
    "browser header set). Its document-delivery path is NOT blocked - the Pillar 3 PDF itself "
    "returns HTTP 200, Content-Type application/pdf and valid %PDF magic bytes to a request carrying "
    "an ordinary browser User-Agent. EFG Private Bank Limited DOES publish a standalone, "
    "entity-level Pillar 3 report containing a full row-numbered UK KM1. The superseded sentence has "
    "been removed from every sheet in this workbook rather than corrected on one of them."
)

PILLAR3_FY2025_NOTE = (
    "Source - EFG Private Bank Limited's own standalone Pillar 3 Disclosures for the year ended "
    "31 December 2025 (the edition this URL currently serves; PDF created 1 September 2026), UK KM1 "
    "table s.1.6 p.3 and UK OV1 table s.3.2 p.14 - " + PILLAR3_URL + "\n"
    "The report is explicitly prepared on a stand-alone basis (s.1.2) and its KM1 prints two columns, "
    "31 December 2025 and a 31 December 2024 comparative. FY2025 KM1 figures: CET1 capital "
    "GBP267.7m, Tier 1 and total capital GBP334.3m, total RWA GBP1,918.2m, CET1 ratio 13.96%, Tier 1 "
    "and total-capital ratio 17.43%, leverage ratio 5.34% on an exposure measure of GBP6,265.4m, "
    "LCR 218% and NSFR 145%.\n"
    "NOTE THE FILENAME. The URL's path says \"2024 Pillar 3 Disclosure Report\" and the document it "
    "returns is the 2025 report. EFG republished over the same asset without renaming it, so the "
    "filename cannot be used to identify the edition - the title page, the running footer and the "
    "KM1 column headers can, and all three say 2025."
)

PILLAR3_FY2024_EDITION_NOTE = (
    "Source for FY2024 and FY2023 - the FY2024 edition of the same report (for the year ended "
    "31 December 2024, approved 30 September 2025), read and transcribed on 2026-09-04 from the URL "
    "above, WHICH NO LONGER SERVES IT (see the edition-swap note in this script's header). Its UK "
    "KM1 gave, FY2024 / FY2023: CET1 capital GBP237.3m/205.8m, Tier 1 capital GBP303.9m/272.4m, "
    "total capital GBP303.9m/272.4m, total RWA GBP1,763.3m/1,581.0m, CET1 ratios 13.46%/13.01%, "
    "Tier 1 and total-capital ratios 17.24%/17.23%, leverage ratios 5.09%/5.15%, LCR 213%/220% and "
    "NSFR 154%/160%. The formal KM1 table was used in preference to that report's rounded "
    "introductory prose (which quoted 17.24%, 247% and 158% for selected metrics).\n"
    "THE FY2025 EDITION RESTATES FY2024 OWN FUNDS UPWARD BY GBP14.9m and this workbook does not "
    "adopt the restatement, because each year is taken from the edition in which it is the reporting "
    "year. The FY2025 edition's 31 December 2024 comparative column reads CET1 252.2 (vs 237.3), "
    "Tier 1 and total capital 318.8 (vs 303.9), CET1 ratio 14.30% (vs 13.46%), Tier 1 and "
    "total-capital ratio 18.08% (vs 17.24%) and leverage ratio 5.34% (vs 5.09%), while total RWA "
    "(1,763.3), LCR (213%) and NSFR (154%) are unchanged - a restatement of own funds alone, with "
    "the denominator untouched. The FY2025 accounts' own Note 34 comparative agrees with the "
    "restated figure (CET1 252.2), and the FY2025 Strategic Report states \"CET1 capital increased "
    "by GBP 15.5 million to GBP 267.7 million (2024: GBP 252.2 million)\". Both figures are "
    "therefore real and neither is reconciled away here."
)

# Superseded name, kept so nothing in this file silently loses its citation. It now carries BOTH
# editions, because a reader following it needs to know which document holds which year.
PILLAR3_2025_NOTE = PILLAR3_FY2025_NOTE + "\n" + PILLAR3_FY2024_EDITION_NOTE

EFGI_GROUP_P3_2024_URL = ("https://www.efginternational.com/doc/jcr:7e330f8b-4688-4ce3-8de3-"
                          "000e6d4f11e1/Pillar-3_19_02.pdf/lang:en/Pillar-3_19_02.pdf")
EFGI_GROUP_P3_2025H1_URL = ("https://www.efginternational.com/doc/jcr:354f259a-45aa-466f-a8ab-"
                            "ddee13ac57ab/Pillar-3_23_07.pdf/lang:en/Pillar-3_23_07.pdf")

# A UK subsidiary's prudential figures are very often published inside its PARENT's Pillar 3 rather
# than its own (Close Brothers Limited's leverage ratio sits in Close Brothers Group plc's report in
# a column headed "Individual"; Clydesdale Bank's KM1 sits in an appendix of Virgin Money UK's).
# So before writing any non-disclosure for this entity, the parent's disclosures were searched.
PARENT_CHECK_NOTE = (
    "THE PARENT'S DISCLOSURES WERE CHECKED TOO, on 2026-09-16, because a UK subsidiary's prudential "
    "figures are commonly published inside the parent's Pillar 3 rather than its own - as a column "
    "of the parent's table or as an appendix table - rather than in a document of the subsidiary's "
    "own. They are not, here, and this is a positive finding rather than a search that ran out:\n"
    f"* EFG International AG, Basel III Pillar 3 Disclosures 31 December 2024 (68pp) - "
    f"{EFGI_GROUP_P3_2024_URL} - and 30 June 2025 (23pp) - {EFGI_GROUP_P3_2025H1_URL} . Both fetched "
    "live (HTTP 200, application/pdf, %PDF magic bytes, 2,348,844 and 1,001,813 bytes). Text "
    "extraction on both is RICH, which is what makes a zero meaningful rather than a tool failure: "
    "124 and 90 occurrences of 'capital', 26 and 22 of 'CET1', 19 and 8 of 'leverage'. Against that, "
    "'EFGIUK' occurs ZERO times in either, and 'United Kingdom' occurs once - inside a list of "
    "countries in a geographic exposure breakdown, not as an entity heading.\n"
    "* Its KM1 (s.2.2) carries five columns (a)-(e), and they are five QUARTERLY DATES for the "
    "consolidated Group in CHF millions (31 Dec 2024 / 30 Sep 2024 / 30 Jun 2024 / 31 Mar 2024 / "
    "31 Dec 2023) - not five entities. There is no solo, individual or subsidiary column anywhere in "
    "it. The appendices (12.1 LIQ1, 12.2 LIQ2, 12.3 CC1, 12.4 CC2) are all Group-scope templates; "
    "none is an entity block. The document is a Swiss FINMA/Basel III disclosure in CHF, not a UK "
    "CRR one.\n"
    "* The two documents on the same site titled '2022 Pillar III Disclosures' and '2023 Pillar III "
    "Disclosures' are EFG Bank (Luxembourg) S.A.'s, not this entity's - they use the EU templates "
    "and their own Article-mapping table reads 'Not applicable to EFGLUX'.\n"
    "* WHY THAT IS THE EXPECTED ANSWER HERE, rather than a gap: EFGIUK is supervised solo. Its own "
    "FY2025 accounts, Note 34, state \"The Prudential Regulation Authority ('PRA') supervises the "
    "Company on a stand-alone basis\", and its own Pillar 3 s.1.2 states \"These Pillar 3 disclosures "
    "are prepared on a stand-alone basis, as are the Company's financial statements\". There is no UK "
    "regulatory consolidation group above this entity whose Pillar 3 would carry its block; the "
    "entity discharges the obligation itself, which is why it publishes a standalone report at all."
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
    f"FY2025: Annual Report and Financial Statements 2025, p.23 (Cash Flow Statement) - {AR2025_URL}\n"
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
        f"FY2025: Annual Report and Financial Statements 2025, Note 34 (Capital management), p.76 "
        f"- {AR2025_URL}\n"
        f"FY2024: Annual Report and Financial Statements 2024, p.{page} - {AR2024_URL}\n"
        f"FY2023: Annual Report and Financial Statements 2023, p.80 - {AR2023_URL}\n"
        f"FY2022: Annual Report and Financial Statements 2022, p.60-61 - {AR2022_URL}\n"
        "FY2021: as stated in the FY2022 Annual Report's own FY2021 comparative column, p.60-61 "
        f"- {AR2022_URL}\n"
        + PILLAR3_REACH_NOTE + " The figures on this sheet are sourced from the statutory accounts' "
        "own Capital management note where that note states them, and from the standalone Pillar 3 "
        "report where it does - see the separate Pillar 3 source note appended below, which supplies "
        "figures for several metrics the statutory accounts do not state at all.\n"
        "IMPORTANT DISCLOSURE-FORMAT NOTE: FY2021 and FY2022's own Annual Reports disclose a full "
        "capital table (CET1 Capital, Total Capital, Total RWAs, CET1 Ratio, Total Capital Ratio). "
        "FY2023, FY2024 and FY2025's own Annual Reports disclose ONLY Common equity tier 1 capital "
        "(£m) - no ratio, no RWA, no Total Capital figure at all, confirmed by reading the full "
        "Capital management note in all three reports (FY2025's Note 34, p.76, states one line: "
        "'Common equity tier 1 capital 267.7 / 252.2'). This is a genuine reduction in disclosure "
        "depth between report vintages, not a gap in this research, and it is the reason the ratio, "
        "RWA and Total Capital figures for those years come from the standalone Pillar 3 instead. "
        "Liquidity risk (Note 29) is purely qualitative/contractual-maturity-table based in every "
        "year reviewed - no LCR/NSFR percentage is stated in the notes anywhere, though the "
        "Strategic Report does state a year-end LCR in prose (see the LCR sheet). No Leverage "
        "Ratio or MREL figure appears in the accounts in any year. "
        "Exhaustive follow-up: EFG's official UK document archive was also checked, including the linked "
        "'Pillar III' PDF (2018 Pillar III disclosure, which is a CRR Article 450 remuneration disclosure "
        "only, not a prudential-metrics/KM1 report) and the 2020-2024 annual-report links. No additional "
        "entity-level prudential figures for FY2021/FY2022 beyond those in the accounts were found. The "
        "2024 standalone report's comparative column supplies the previously missed FY2023 values, and "
        "the 2025 report supplies FY2025.\n"
        + PARENT_CHECK_NOTE
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
    f"FY2025: Annual Report and Financial Statements 2025, p.19-22 (Income Statement / Statement "
    f"of Comprehensive Income / Balance Sheet / Statement of Changes in Equity) - {AR2025_URL}\n"
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
    "\nTHE SAME TEMPLATE ARTIFACT RECURS IN FY2025, which corroborates that reading rather "
    "than undermining it: the FY2025 report's Statement of Comprehensive Income (p.20) carries the "
    "page footer \"Statement of comprehensive income | Annual Report 2025 | EFG International AG\", "
    "while every other statement page in the same report is footed \"EFG Private Bank Limited\". The "
    "figures are this Company's: net profit 23,357 ties exactly to its own Income Statement and to "
    "its own Statement of Changes in Equity. It is a footer left over from a group template."
)

INVESTMENT_SECURITIES_NOTE = (
    "\n\nINVESTMENT SECURITIES MEASUREMENT-BASIS SPLIT: each year's own accounts break the 'Investment "
    "securities' balance down by IFRS 9 measurement category (debt securities at amortised cost vs debt "
    "securities at FVOCI, fair value through other comprehensive income), which the 'Investment "
    "securities at amortised cost'/'at FVOCI' rows above reproduce as a genuine sub-split - each year's "
    "two legs reconcile exactly to that year's 'Total investment securities' figure:\n"
    f"FY2024: Annual Report and Financial Statements 2024, Note 12 'Investment securities', p.41 - "
    f"{AR2024_URL} (£1,799,311k amortised cost / £469,390k FVOCI; the note states the Company acquired "
    "bonds within the 'Hold to Collect and Sell' business model during 2024 - its first such acquisition "
    "since the November 2022 business-model reclassification described below).\n"
    f"FY2023: Annual Report and Financial Statements 2023, Note 12 'Investment securities', p.40 - "
    f"{AR2023_URL} (£2,066,635k amortised cost, £nil FVOCI - wholly held-to-collect that year, following "
    "a business-model reclassification from 'Hold to Collect and Sell' to 'Hold to Collect' that the same "
    "note states took effect 1 January 2023).\n"
    f"FY2022: Annual Report and Financial Statements 2022, Note 12 'Financial assets at fair value "
    f"through Other Comprehensive Income', p.33 - {AR2022_URL} (£nil amortised cost, £1,487,411k FVOCI - "
    "wholly FVOCI; the 'Hold to Collect' reclassification above was not yet effective at this year end, "
    "and this year's own accounts have no separate amortised-cost investment-securities note at all).\n"
    "FY2021: as stated in the FY2022 Annual Report's own FY2021 comparative column, same note and page - "
    f"{AR2022_URL} (£nil amortised cost, £852,764k FVOCI).\n"
    "The same note also breaks the balance down a second way, by issuer type (Government vs Banks), for "
    "every year (net carrying amounts - FY2024: £1,702,937k/£565,764k; FY2023: £1,647,410k/£419,225k; "
    "FY2022: £1,005,478k/£481,933k; FY2021: £384,256k/£468,508k - each pair also reconciling exactly to "
    "the same year's Total investment securities figure). This issuer-type split is NOT added as its own "
    "set of rows on this sheet: the cross-bank curation that consumes this Balance Sheet sums ALL matching "
    "sibling rows under a given total per bucket, and a second, independent 2-way split of the same total "
    "would double-count against the measurement-basis split already added above (a row not naming "
    "'Government' falls into that logic's 'other' bucket by default, which would then wrongly include the "
    "amortised-cost/FVOCI rows a second time). The issuer-type figures are recorded here in the source "
    "note instead, so they remain available without creating that double-counting sibling-row conflict."
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
         {"FY2025": 219018, "FY2024": 795400, "FY2023": 686860, "FY2022": 1213286, "FY2021": 1244267}),
        ("DATA", "Due from other banks",
         {"FY2025": 70759, "FY2024": 55991, "FY2023": 87593, "FY2022": 95177, "FY2021": 124974}),
        ("DATA", "Derivative financial instruments",
         {"FY2025": 7323, "FY2024": 20591, "FY2023": 24974, "FY2022": 58670, "FY2021": 10099}),
        ("TOTAL", "Total investment securities",
         {"FY2025": 2300562, "FY2024": 2268701, "FY2023": 2066635, "FY2022": 1487411, "FY2021": 852764}),
        ("DATA", "Investment securities at amortised cost",
         {"FY2025": 1379416, "FY2024": 1799311, "FY2023": 2066635}),
        ("DATA", "Investment securities at FVOCI (fair value through other comprehensive income)",
         {"FY2025": 921146, "FY2024": 469390, "FY2022": 1487411, "FY2021": 852764}),
        ("DATA", "Loans and advances to customers",
         {"FY2025": 3615957, "FY2024": 3398294, "FY2023": 2907872, "FY2022": 2967101, "FY2021": 2764761}),
        ("DATA", "Investment in subsidiaries",
         {"FY2025": 1320, "FY2024": 1320, "FY2023": 1320, "FY2022": 1320, "FY2021": 1320}),
        ("DATA", "Property, plant and equipment",
         {"FY2025": 22674, "FY2024": 25314, "FY2023": 22678, "FY2022": 25182, "FY2021": 24002}),
        ("DATA", "Intangible assets",
         {"FY2025": 449, "FY2024": 420, "FY2023": 4508, "FY2022": 3113, "FY2021": 1798}),
        ("DATA", "Deferred income tax assets",
         {"FY2025": 9739, "FY2024": 7305, "FY2023": 5228, "FY2022": 11333, "FY2021": 5553}),
        ("DATA", "Other assets",
         {"FY2025": 31124, "FY2024": 35380, "FY2023": 48492, "FY2022": 27013, "FY2021": 24994}),
        ("TOTAL", "Total assets",
         {"FY2025": 6278925, "FY2024": 6608716, "FY2023": 5856160, "FY2022": 5889606, "FY2021": 5054532}),
        ("SECTION", "Liabilities", {}),
        ("DATA", "Due to other banks",
         {"FY2025": 906235, "FY2024": 1157827, "FY2023": 694997, "FY2022": 758752, "FY2021": 539184}),
        ("DATA", "Due to customers",
         {"FY2025": 4932678, "FY2024": 5042962, "FY2023": 4715872, "FY2022": 4762542, "FY2021": 4152829}),
        ("DATA", "Derivative financial instruments",
         {"FY2025": 31835, "FY2024": 8939, "FY2023": 22273, "FY2022": 13603, "FY2021": 22109}),
        ("DATA", "Current income tax liabilities",
         {"FY2025": 1323, "FY2024": 1072, "FY2023": 4779, "FY2022": 5103, "FY2021": 1742}),
        ("DATA", "Provisions",
         {"FY2025": 3657, "FY2024": 1787, "FY2023": 3168, "FY2022": 3382, "FY2021": 3427}),
        ("DATA", "Other liabilities",
         {"FY2025": 66147, "FY2024": 75135, "FY2023": 107705, "FY2022": 72042, "FY2021": 67977}),
        ("TOTAL", "Total liabilities",
         {"FY2025": 5941875, "FY2024": 6287722, "FY2023": 5548794, "FY2022": 5615424, "FY2021": 4787268}),
        ("SECTION", "Equity", {}),
        ("DATA", "Share capital",
         {"FY2025": 31596, "FY2024": 31596, "FY2023": 31596, "FY2022": 31596, "FY2021": 31596}),
        ("DATA", "Share premium",
         {"FY2025": 96639, "FY2024": 96639, "FY2023": 96639, "FY2022": 96639, "FY2021": 96639}),
        ("DATA", "Capital redemption reserve",
         {"FY2025": 10000, "FY2024": 10000, "FY2023": 10000, "FY2022": 10000, "FY2021": 10000}),
        ("DATA", "Other equity and reserves",
         {"FY2025": 72369, "FY2024": 72515, "FY2023": 72571, "FY2022": 55451, "FY2021": 73325}),
        ("DATA", "Retained earnings",
         {"FY2025": 126446, "FY2024": 110244, "FY2023": 96560, "FY2022": 80496, "FY2021": 55704}),
        ("TOTAL", "Total equity",
         {"FY2025": 337050, "FY2024": 320994, "FY2023": 307366, "FY2022": 274182, "FY2021": 267264}),
        ("TOTAL", "Total liabilities and equity",
         {"FY2025": 6278925, "FY2024": 6608716, "FY2023": 5856160, "FY2022": 5889606, "FY2021": 5054532}),
    ],
    sources_text=BS_IS_EQ_SOURCES + INVESTMENT_SECURITIES_NOTE,
    first_col_width=64,
    source_height=420,
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
         {"FY2025": 348328, "FY2024": 347776, "FY2023": 304437, "FY2022": 133296, "FY2021": 59764}),
        ("DATA", "Interest expense",
         {"FY2025": -241239, "FY2024": -244347, "FY2023": -194252, "FY2022": -53553, "FY2021": -13548}),
        ("TOTAL", "Net interest income",
         {"FY2025": 107089, "FY2024": 103429, "FY2023": 110185, "FY2022": 79743, "FY2021": 46216}),
        ("DATA", "Banking fee and commission income",
         {"FY2025": 68667, "FY2024": 64443, "FY2023": 56844, "FY2022": 60878, "FY2021": 63082}),
        ("DATA", "Banking fee and commission expense",
         {"FY2025": -3219, "FY2024": -3218, "FY2023": -3416, "FY2022": -3337, "FY2021": -2781}),
        ("TOTAL", "Net banking fee and commission income",
         {"FY2025": 65448, "FY2024": 61225, "FY2023": 53428, "FY2022": 57541, "FY2021": 60301}),
        ("DATA", "Dividend income", {"FY2021": 30000}),
        ("DATA", "Net trading income/(expense) on financial instruments",
         {"FY2025": -1247, "FY2024": -579, "FY2023": -793, "FY2022": 1380, "FY2021": 747}),
        ("DATA", "Net trading income/(expense) on foreign exchange",
         {"FY2025": -9866, "FY2024": -1869, "FY2023": 3308, "FY2022": 543, "FY2021": 4862}),
        ("DATA", "Gains less losses on disposal of financial assets",
         {"FY2024": 0, "FY2023": 217, "FY2022": 147, "FY2021": 60}),
        ("DATA", "Other operating income/(expense) (a separate line only in the FY2025 Income Statement; earlier years print no such row)",
         {"FY2025": 14}),
        ("TOTAL", "Net other income",
         {"FY2025": -11099, "FY2024": -2448, "FY2023": 2732, "FY2022": 2070, "FY2021": 35669}),
        ("TOTAL", "Operating and investing income",
         {"FY2025": 161438, "FY2024": 162206, "FY2023": 166345, "FY2022": 139354, "FY2021": 142186}),
        ("DATA", "Operating expenses",
         {"FY2025": -131917, "FY2024": -134329, "FY2023": -125648, "FY2022": -104693, "FY2021": -112020}),
        ("DATA", "Profit on disposal of subsidiary", {"FY2021": 68900}),
        ("DATA", "Loss allowance/(reversal) on financial assets at amortised cost",
         {"FY2025": -1655, "FY2024": -1690, "FY2023": -555, "FY2022": 210, "FY2021": -37}),
        ("TOTAL", "Profit before tax",
         {"FY2025": 27866, "FY2024": 26187, "FY2023": 40142, "FY2022": 34871, "FY2021": 99029}),
        ("DATA", "Income tax (expense)/credit",
         {"FY2025": -4509, "FY2024": -5712, "FY2023": -4395, "FY2022": -4609, "FY2021": 2133}),
        ("TOTAL", "Net profit for the year",
         {"FY2025": 23357, "FY2024": 20475, "FY2023": 35747, "FY2022": 30262, "FY2021": 101162}),
        ("SECTION", "Other comprehensive income/(expense)", {}),
        ("DATA", "Net (losses)/gains on investments in debt instruments measured at FVOCI",
         {"FY2025": 1036, "FY2024": -837, "FY2023": 0, "FY2022": -36347, "FY2021": -11318}),
        ("DATA", "Net gains/(losses) on designated hedges over debt instruments measured at FVOCI",
         {"FY2022": 13774, "FY2021": 9158}),
        ("DATA", "Transfers to the Income Statement on realised gains/(losses) on FVOCI debt instruments",
         {"FY2021": 12}),
        ("DATA", "Net (losses)/gains on investments in equity instruments designated at FVOCI",
         {"FY2021": -51}),
        ("DATA", "Deferred tax on the above items",
         {"FY2025": -259, "FY2024": 209, "FY2023": -5464, "FY2022": 6400, "FY2021": 0}),
        ("TOTAL", "Total other comprehensive income/(expense) for the year",
         {"FY2025": 777, "FY2024": -628, "FY2023": 18924, "FY2022": -16173, "FY2021": -2199}),
        ("TOTAL", "Total comprehensive income for the year, net of tax",
         {"FY2025": 24134, "FY2024": 19847, "FY2023": 54671, "FY2022": 14089, "FY2021": 98963}),
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
        ("DATA", "Net profit for the year", (None, None, None, None, 23357, 23357)),
        ("DATA", "Net gains on investments in debt instruments measured at FVOCI (incl. hedging effect)",
         (None, None, None, 1036, None, 1036)),
        ("DATA", "Income tax relating to components of other comprehensive income",
         (None, None, None, -259, None, -259)),
        ("TOTAL", "Total comprehensive income for the year", (None, None, None, 777, 23357, 24134)),
        ("DATA", "AT1 interest treated as appropriation of retained earnings",
         (None, None, None, None, -7155, -7155)),
        ("DATA", "Employee equity incentive plans amortisation net of exercise costs",
         (None, None, None, -923, None, -923)),
        ("TOTAL", "Balance at 31 December 2025", (31596, 96639, 10000, 72369, 126446, 337050)),
    ],
    sources_text=BS_IS_EQ_SOURCES + (
        "\nPer-year reconciliation confirmed: each year's opening balance ties to the prior year's own "
        "closing balance, and each year's closing balance ties to that year's own Balance Sheet Total "
        "equity figure (FY2021 closing 267,264 / FY2022 closing 274,182 / FY2023 closing 307,366 / "
        "FY2024 closing 320,994 / FY2025 closing 337,050 - all five tie exactly, no plug rows "
        "needed). The FY2025 block is the FY2025 Annual Report's own second panel, p.22, which opens "
        "at 1 January 2025 on exactly the FY2024 closing balance already shown above."
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
     {"FY2025": 27866, "FY2024": 26187, "FY2023": 40142, "FY2022": 34871, "FY2021": 99029}),
    ("DATA", "Depreciation of fixed assets",
     {"FY2025": 3491, "FY2024": 4248, "FY2023": 3323, "FY2022": 4499, "FY2021": 4752}),
    ("DATA", "Amortisation of intangibles",
     {"FY2025": 357, "FY2024": 245, "FY2023": 551, "FY2022": 535, "FY2021": 434}),
    ("DATA", "Amortisation of IFRS 2 reserve through profit and loss",
     {"FY2025": 8864, "FY2024": 9630, "FY2023": 6052, "FY2022": 4214, "FY2021": 4030}),
    ("DATA", "Loss allowance provision",
     {"FY2025": 1655, "FY2024": 1690, "FY2023": 555, "FY2022": -210, "FY2021": 37}),
    ("DATA", "Loss/(gain) on sale of subsidiary as investment activity",
     {"FY2022": 0, "FY2021": -68900}),
    ("DATA", "Gains less losses on disposal of financial assets",
     {"FY2025": 43, "FY2024": 0, "FY2023": -217, "FY2022": -147, "FY2021": -60}),
    ("DATA", "Dividend paid by subsidiary included in investment income",
     {"FY2022": 0, "FY2021": -30000}),
    ("DATA", "Lease interest per IFRS16",
     {"FY2025": 528, "FY2024": 581, "FY2023": 435, "FY2022": 448, "FY2021": 156}),
    ("DATA", "Change in interest accrual",
     {"FY2025": -9290, "FY2024": -9430, "FY2023": -4920}),
    ("DATA", "Effect of foreign exchange / Other non-cash movements (the FY2025 statement renames "
             "this line 'Other non-cash movements'; same position in the reconciliation)",
     {"FY2025": 33048,"FY2024": -5429, "FY2023": 51485, "FY2022": -61770}),
    ("DATA", "Release of tax related provision", {"FY2024": -1991}),
    ("DATA", "(Increase)/decrease in derivative financial instruments",
     {"FY2025": 36164, "FY2024": -8951, "FY2023": 42583, "FY2022": -57077, "FY2021": -15336}),
    ("DATA", "(Increase)/decrease in loans and advances to customers",
     {"FY2025": -222473, "FY2024": -492079, "FY2023": 59123, "FY2022": -202340, "FY2021": -590609}),
    ("DATA", "Decrease/(increase) in other assets",
     {"FY2025": 4287, "FY2024": 15349, "FY2023": -21479, "FY2022": -2019, "FY2021": 28685}),
    ("DATA", "Increase/(decrease) in due to other banks",
     {"FY2025": -243670, "FY2024": 462830, "FY2023": -63755, "FY2022": 219568, "FY2021": 11595}),
    ("DATA", "Increase/(decrease) in due to customers",
     {"FY2025": -96659, "FY2024": 327090, "FY2023": -46670, "FY2022": 609713, "FY2021": 1137564}),
    ("DATA", "(Decrease)/increase in other liabilities and provisions",
     {"FY2025": -3939, "FY2024": -30373, "FY2023": 35466, "FY2022": 5925, "FY2021": 12154}),
    ("DATA", "Payments to tax authorities", {"FY2025": -4157, "FY2024": -9774, "FY2023": -5025}),
    ("DATA", "Corporation tax paid", {"FY2022": -2617, "FY2021": -1183}),
    ("DATA", "Payments to parent for participation in share scheme",
     {"FY2025": -13023, "FY2024": -9465, "FY2023": -7833, "FY2022": -6452, "FY2021": -5681}),
    ("TOTAL", "Net cash flows from operating activities",
     {"FY2025": -476908, "FY2024": 280358, "FY2023": 89816, "FY2022": 547141, "FY2021": 586667}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "(Purchase) of investment securities",
     {"FY2025": -1202454, "FY2024": -1817999, "FY2023": -1574973, "FY2022": -1177277, "FY2021": -453370}),
    ("DATA", "Proceeds from maturities/sale of investment securities",
     {"FY2025": 1128755, "FY2024": 1630203, "FY2023": 973586, "FY2022": 587790, "FY2021": 340452}),
    ("DATA", "(Purchase) of capital in subsidiaries", {"FY2021": -1275}),
    ("DATA", "Proceeds from disposal of subsidiary", {"FY2021": 78900}),
    ("DATA", "(Purchase) of property plant & equipment",
     {"FY2025": -882, "FY2024": -2864, "FY2023": -819, "FY2022": -5793, "FY2021": -176}),
    ("DATA", "(Purchase) of intangible assets",
     {"FY2025": -386, "FY2024": -2414, "FY2023": -1946, "FY2022": -1850, "FY2021": -973}),
    ("DATA", "Proceeds from dividends", {"FY2021": 30000}),
    ("TOTAL", "Net cash flows used in investing activities",
     {"FY2025": -74967, "FY2024": -193074, "FY2023": -604152, "FY2022": -597130, "FY2021": -6442}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Payment of AT1 interest",
     {"FY2025": -7155, "FY2024": -7174, "FY2023": -7154, "FY2022": -5394, "FY2021": -5389}),
    ("DATA", "Payment of dividends",
     {"FY2024": 0, "FY2023": -12676, "FY2022": 0, "FY2021": -89000}),
    ("DATA", "Lease interest repaid",
     {"FY2025": -528, "FY2024": -421, "FY2023": -36, "FY2022": -448, "FY2021": None}),
    ("DATA", "Lease disposal", {"FY2025": -150, "FY2024": -267}),
    ("DATA", "Lease principal repaid",
     {"FY2025": -2587, "FY2024": -2202, "FY2023": -644, "FY2022": -1905, "FY2021": -3028}),
    ("TOTAL", "Net cash flows from financing activities",
     {"FY2025": -10420, "FY2024": -10064, "FY2023": -20510, "FY2022": -7747, "FY2021": -97417}),
    ("TOTAL", "Net cash outflows/(inflows)",
     {"FY2025": -562295, "FY2024": 77220, "FY2023": -534846, "FY2022": -57736, "FY2021": 482808}),
    ("DATA", "Effect of exchange rate changes on cash and cash equivalents",
     {"FY2025": 637, "FY2024": -326, "FY2023": 794, "FY2022": -3042, "FY2021": -12197}),
    ("TOTAL", "Net change in cash and cash equivalents",
     {"FY2025": -561658, "FY2024": 76894, "FY2023": -534052, "FY2022": -60778, "FY2021": 470611}),
    ("DATA", "Cash and cash equivalents at the beginning of period",
     {"FY2025": 846465, "FY2024": 769571, "FY2023": 1303623, "FY2022": 1369241, "FY2021": 898630}),
    ("TOTAL", "Cash and cash equivalents at the end of period",
     {"FY2025": 284807, "FY2024": 846465, "FY2023": 769571, "FY2022": 1308463, "FY2021": 1369241}),
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
    "\n\nFY2025 (added 2026-09-16): Annual Report and Financial Statements 2025, Note 13 "
    "'Loans and advances to customers' p.38 and Note 27.10 p.63-65 - " + AR2025_URL + "\n"
    "* GROSS EXPOSURE BY STAGE IS DISCLOSED AGAIN IN FY2025, for the first time since FY2022. The "
    "FY2025 report prints a full gross-carrying-value roll-forward by stage for mortgage loans "
    "(p.63) and for Lombard loans (p.65). The Stage 1/2/3 rows above are the two closing balances "
    "added together: Stage 1 2,486,319 + 917,304 = 3,403,623; Stage 2 121,878 + 127 = 122,005; "
    "Stage 3 93,493 + 738 = 94,231. THEY DO NOT FOOT EXACTLY TO THE GROSS LOANS ROW: the three sum "
    "to 3,619,859 against gross loans of 3,620,119, a difference of 260 (0.007%). That is the "
    "source's own inconsistency between its Note 13 total and its Note 27 roll-forward closing "
    "balances, and it is shown rather than forced to agree.\n"
    "* THREE DIFFERENT 'GROSS' FIGURES APPEAR IN THE FY2025 REPORT and they reconcile once the "
    "deferred loan fee is accounted for, which also explains the note-presentation change described "
    "above. Note 13 gives Mortgages 2,703,983 + Lombard and Other 916,136 = gross 3,620,119, less "
    "allowance 4,162 = 3,615,957. Note 27.10 gives Mortgage gross 2,705,766, Other and lombard gross "
    "919,787 (total 3,625,553), less ECL 3,610 + 552, less a separately-stated Deferred loan fee of "
    "5,434 = the same 3,615,957. So Note 13's 'gross' is already NET of the deferred loan fee "
    "(3,625,553 - 5,434 = 3,620,119 exactly) while Note 27.10's is before it. The rows above use "
    "Note 13's presentation, which is the same basis FY2023 and FY2024 are on, so the four most "
    "recent years are like-for-like; the Note 27.10 figures are recorded here instead of being put "
    "on the sheet in a second, incompatible basis. FY2024 on the Note 27.10 basis, for the record: "
    "mortgage gross 2,578,636, other and lombard 828,080, deferred loan fee 5,379.\n"
    "* A GBP2k INTERNAL INCONSISTENCY IN THE SOURCE, recorded not reconciled: the FY2025 report's "
    "mortgage loss-allowance roll-forward closes FY2024 at 2,798, while its own Note 27.10 states "
    "the FY2024 mortgage ECL as 2,796. With Lombard's 247 (which both agree on) the latter gives "
    "3,043, which is what FY2024's own Note 13 states and what this sheet carries for FY2024. The "
    "FY2025 column is unaffected: mortgage 3,610 + Lombard 552 = 4,162, agreeing across Note 13, "
    "Note 27.10 and both roll-forwards."
)

bw.add_asset_quality_sheet(
    title="EFG Private Bank Limited — Asset Quality",
    subtitle="Company basis, £'000. See source note at bottom.",
    rows=[
        ("SECTION", "Gross loans and advances by product", {}),
        ("DATA", "Mortgages",
         {"FY2025": 2703983, "FY2024": 2574601, "FY2023": 2161229, "FY2022": 2101252, "FY2021": 1809606}),
        ("DATA", "Other and Lombard loans",
         {"FY2025": 916136, "FY2024": 826736, "FY2023": 748153, "FY2022": 871619, "FY2021": 960987}),
        ("TOTAL", "Gross loans and advances",
         {"FY2025": 3620119, "FY2024": 3401337, "FY2023": 2909382, "FY2022": 2972872, "FY2021": 2770593}),
        ("SECTION", "Gross exposure by IFRS 9 stage (Mortgages + Other/Lombard combined)", {}),
        ("DATA", "Stage 1 (12-month ECL)", {"FY2025": 3403623, "FY2022": 2792274, "FY2021": 2641488}),
        ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {"FY2025": 122005, "FY2022": 108967, "FY2021": 64481}),
        ("DATA", "Stage 3 (lifetime ECL, credit-impaired)", {"FY2025": 94231, "FY2022": 71630, "FY2021": 64624}),
        ("SECTION", "Loss allowance", {}),
        ("DATA", "Loss allowance - Stage 1",
         {"FY2025": 846, "FY2024": 1064, "FY2023": 432, "FY2022": 70, "FY2021": 133}),
        ("DATA", "Loss allowance - Stage 2",
         {"FY2025": 104, "FY2024": 513, "FY2023": 516, "FY2022": 104, "FY2021": 119}),
        ("DATA", "Loss allowance - Stage 3",
         {"FY2025": 3212, "FY2024": 1466, "FY2023": 562, "FY2022": 1230, "FY2021": 1432}),
        ("TOTAL", "Total loss allowance",
         {"FY2025": 4162, "FY2024": 3043, "FY2023": 1510, "FY2022": 1404, "FY2021": 1684}),
        ("DATA", "Less: Deferred loan fee (FY2022/FY2021 note presentation only - see source note)",
         {"FY2022": -4366, "FY2021": -4148}),
        ("TOTAL", "Loans and advances to customers (net)",
         {"FY2025": 3615957, "FY2024": 3398294, "FY2023": 2907872, "FY2022": 2967101, "FY2021": 2764761}),
        ("SECTION", "Derived ratios", {}),
        ("DATA", "ECL coverage ratio (total loss allowance / gross loans)",
         {"FY2025": "0.11%", "FY2024": "0.09%", "FY2023": "0.05%", "FY2022": "0.05%", "FY2021": "0.06%"}),
        ("DATA", "Stage 3 as % of gross loans (NPL proxy)",
         {"FY2025": "2.60%", "FY2022": "2.41%", "FY2021": "2.33%"}),
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
    "Not publicly disclosed for this entity in the years shown. This metric appears neither in the "
    "statutory accounts' Capital management or Liquidity risk notes for those years (confirmed by "
    "reading both notes directly, not assumed) nor in the Company's own standalone Pillar 3 report, "
    "nor in its parent's group Pillar 3.\n"
    + PILLAR3_REACH_NOTE + "\n" + PARENT_CHECK_NOTE
)

# ---------------------------------------------------------------
# Sheet: KM1 Key Metrics (KM1-012)
#
# EFGIUK prints a full, row-numbered UK KM1 - "UK KM1", GBP millions, section
# 1.6 of its standalone Pillar 3, located from the document's OWN contents page
# rather than by hunting for a digit-dense page (map rule 16).
#
# FY2025 and FY2024 are each taken from the edition in which that year is the
# REPORTING year (map rule 1), which here means two different editions served at
# one URL - see the edition-swap note in this script's header. FY2023 is the
# FY2024 edition's comparative column, the only place it exists: EFGIUK had no
# standalone Pillar 3 before that edition, so FY2023 has no edition of its own.
# FY2022 and FY2021 are BLANK because no KM1 exists for them anywhere - not in
# the Company's accounts, not in an earlier Pillar 3 (there is none), and not in
# the parent's group Pillar 3 (checked; see PARENT_CHECK_NOTE).
#
# THREE PRINTED TYPOS ARE REPRODUCED AS PRINTED (map rule 7). Row 4's FY2025
# cell, row UK 16a's FY2024 cell and row 18's FY2024 cell each carry a comma
# where a decimal point belongs. All three were confirmed by rendering p.3 at
# 220dpi and reading the page, so they are the source's glyphs and not an
# extraction artefact; each is identified with certainty by the document's own
# arithmetic, recorded in the citation. They are NOT silently corrected.
# ---------------------------------------------------------------
KM1_SOURCES = (
    "Sources - EFG Private Bank Limited's own published UK KM1 key-metrics template, stand-alone "
    "entity basis, GBP millions, reproduced in the Company's own row order, row numbering and "
    "printed precision. Located via the document's own contents page (s.1.6 'Basic regulatory key "
    "figures (KM1)', printed page 2, table on printed page 3).\n"
    "FY2025 (column (a)) - the FY2025 edition, s.1.6 p.3. Columns '31 December 2025' and "
    "'31 December 2024'.\n"
    "FY2024 (column (a) of its own edition) and FY2023 (that edition's comparative column) - the "
    "FY2024 edition, s.1.6 p.3.\n"
    + PILLAR3_FY2025_NOTE + "\n" + PILLAR3_FY2024_EDITION_NOTE + "\n\n"
    "WHY THE FY2024 COLUMN IS ONLY PARTLY FILLED - a deliberate consequence of the edition swap, and "
    "the one place on this sheet where a blank means 'this project cannot verify it' rather than "
    "'the Company did not print it'. The Company printed a COMPLETE FY2024 column in its FY2024 "
    "edition. That edition is gone from the web and unarchived, and what this project holds of it is "
    "the ten values transcribed on 2026-09-04 and listed above: rows 1, 2, 3, 4, 5, 6, 7, 14, 17 and "
    "20. Those ten are the FY2024 cells shown. The remaining FY2024 cells are left BLANK rather than "
    "filled from the FY2025 edition's 31 December 2024 comparative column, because that column is "
    "demonstrably NOT a faithful copy of what the FY2024 edition printed - it restates own funds by "
    "GBP14.9m, and eight of the ten rows we can compare differ. Mixing verified and restated cells "
    "inside one column would produce a column that never appeared in any document.\n"
    "  Row 13 is the clearest case and shows why this matters. The FY2025 edition's FY2024 "
    "comparative gives an exposure measure of 5,965.2, which pairs with Tier 1 of 318.8 to give the "
    "restated 5.34%. FY2024's own edition reported 5.09%, which with its own Tier 1 of 303.9 implies "
    "an exposure measure near 5,971. Printing 5,965.2 beside 5.09% would put two numbers on one row "
    "pair that do not belong to each other.\n"
    "  NOTHING IS LOST: the FY2025 edition's full 31 December 2024 comparative column is recorded "
    "here so a later reader has it. UK 7a 1.29%; UK 7d 10.29%; row 8 2.50%; row 9 1.11%; row 11 "
    "3.61%; UK 11a 13.90%; row 12 4.01%; row 13 5,965.2; row 15 2,599.1; UK 16a 1,336.1 (printed "
    "'1,336,.1'); UK 16b 115.8; row 16 1,220.3; row 18 3,545.1 (printed '3,545,1'); row 19 2,297.8. "
    "Two of the three printed typos described above live in this unused column, which is why they do "
    "not appear as cells on the sheet.\n\n"
    "PRESENTATION NOTES - things the Company did, not choices made here:\n"
    "* THREE PRINTED TYPOS, REPRODUCED AS PRINTED. The FY2025 edition prints a COMMA where a "
    "decimal point belongs in three cells, and each is reproduced here exactly as published rather "
    "than tidied. The page was rendered at 220dpi and read by eye to confirm these are the "
    "document's own glyphs and not a text-extraction artefact. Each is identifiable with certainty "
    "from the document's own arithmetic:\n"
    "   - Row 4, FY2025: printed '1,918,2'. It is 1,918.2 - the same document's UK OV1 (p.14) foots "
    "to 1,918.2, the FY2025 Strategic Report states 'Total risk weighted assets 1,918.2', and "
    "267.7/1,918.2 = 13.95% against the printed CET1 ratio of 13.96%.\n"
    "   - Row UK 16a, FY2024: printed '1,336,.1' (both a comma and a point). It is 1,336.1 - "
    "outflows 1,336.1 less inflows 115.8 = 1,220.3, exactly the printed row 16.\n"
    "   - Row 18, FY2024: printed '3,545,1'. It is 3,545.1 - 3,545.1/2,297.8 = 154.3%, exactly the "
    "printed row 20 of 154%.\n"
    "* THE ROW SET IS THE COMPANY'S OWN AND IS NOT THE FULL TEMPLATE. EFGIUK prints rows 1-9, 11, "
    "UK 11a, 12, 13-20 and UK 7a/UK 7d, and omits rows 10, UK 7b, UK 7c, UK 8a, UK 9a, UK 10a and "
    "the MREL block entirely. Omitted rows are not shown as blank rows, because a row the Company "
    "never printed and a row it printed empty are different disclosures.\n"
    "* THE LIQUIDITY AND LEVERAGE ROWS ARE AVERAGES, by the Company's own footnotes: footnote 2, "
    "'Liquidity values have been calculated as a simple average of the 12-month end observations'; "
    "footnote 3, 'Net stable funding values have been calculated on the average of quarter end "
    "positions'. This is why row 17 reads 218% for FY2025 while the FY2025 Strategic Report states a "
    "year-end LCR of 227% (2024: 247%) - a period basis difference, not a disagreement. Both are "
    "recorded; see the LCR sheet.\n"
    "* FOOTNOTE 1 IS THE COMPANY'S OWN LEVERAGE CAVEAT: 'EFGIUK is not a LREQ firm and is not "
    "required to maintain the 3.25% minimum under the UK leverage ratio framework. However, in PRA "
    "supervisory statement 45/15 the PRA outline that even banks who are not subject to the 3.25% "
    "threshold should continue to monitor their leverage ratio and manage the ratio so that it does "
    "not ordinarily fall below 3.25%.'\n"
    "* NO DASHES AND NO PRINTED ZEROES appear anywhere in this table in either edition, so the "
    "dash-versus-zero question does not arise for this bank.\n\n"
    "WHY FY2022 AND FY2021 ARE BLANK - an absence established from documents, not a failed search:\n"
    "* The FY2024 edition is the first standalone Pillar 3 report EFGIUK published that carries a KM1, "
    "so there is no KM1 for those years to take, and none is back-filled from the statutory accounts, "
    "which are a "
    "different basis. The accounts' own Capital management note for those years states CET1 capital, "
    "Total capital, Total RWAs and two ratios and nothing else - no SREP rows, no buffer rows, no "
    "leverage exposure measure, no HQLA or cash-flow rows, no ASF/RSF. Those figures are on the "
    "individual metric sheets that follow, where they belong; assembled into a KM1 shape they would "
    "look like a template without being one.\n"
    "* No MREL row exists in any year. The Company's own Pillar 3 contains ZERO occurrences of "
    "'MREL', and that zero is meaningful rather than a failed grep because the same extraction is "
    "rich on neighbouring terms - 70 occurrences of 'capital', 107 of 'ratio', 15 of 'CET1'.\n"
    + PILLAR3_REACH_NOTE + "\n" + PARENT_CHECK_NOTE
)

bw.add_km1_sheet(
    title="EFG Private Bank Limited — KM1 Key Metrics",
    subtitle="The Company's own published UK KM1 key-metrics template, stand-alone entity basis, in "
             "GBP millions, reproduced in its own row order, row numbering and printed precision. "
             "FY2025 and FY2024 each come from the edition in which that year is the reporting year; "
             "FY2023 is the FY2024 edition's comparative, the only place it exists. FY2022/FY2021 are "
             "blank because EFGIUK published no Pillar 3 before the FY2024 edition. Three cells "
             "reproduce a printed comma-for-decimal-point typo exactly as published - see the source "
             "note, which identifies each from the document's own arithmetic.",
    rows=[
        ("SECTION", "Available own funds (amounts, £m)", {}),
        ("DATA", "1    Common Equity Tier 1 (CET1) capital",
         {"FY2025": 267.7, "FY2024": 237.3, "FY2023": 205.8}),
        ("DATA", "2    Tier 1 capital", {"FY2025": 334.3, "FY2024": 303.9, "FY2023": 272.4}),
        ("DATA", "3    Total capital", {"FY2025": 334.3, "FY2024": 303.9, "FY2023": 272.4}),
        ("SECTION", "Risk-weighted exposure amounts (£m)", {}),
        ("DATA", "4    Total risk-weighted exposure amount [FY2025 printed '1,918,2' - a "
                 "comma-for-decimal-point typo in the source, reproduced as printed; it is 1,918.2]",
         {"FY2025": "1,918,2", "FY2024": 1763.3, "FY2023": 1581.0}),
        ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
        ("DATA", "5    Common Equity Tier 1 ratio (%)",
         {"FY2025": "13.96%", "FY2024": "13.46%", "FY2023": "13.01%"}),
        ("DATA", "6    Tier 1 ratio (%)",
         {"FY2025": "17.43%", "FY2024": "17.24%", "FY2023": "17.23%"}),
        ("DATA", "7    Total capital ratio (%)",
         {"FY2025": "17.43%", "FY2024": "17.24%", "FY2023": "17.23%"}),
        ("SECTION", "Additional own funds requirements based on SREP (as a percentage of "
                    "risk-weighted exposure amount)", {}),
        ("DATA", "UK 7a    Additional CET1 SREP requirements (%)", {"FY2025": "1.29%"}),
        ("DATA", "UK 7d    Total SREP own funds requirements (%)", {"FY2025": "10.82%"}),
        ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure "
                    "amount)", {}),
        ("DATA", "8    Capital conservation buffer (%)", {"FY2025": "2.50%"}),
        ("DATA", "9    Institution specific countercyclical capital buffer (%)", {"FY2025": "1.17%"}),
        ("DATA", "11    Combined buffer requirements (%)", {"FY2025": "3.67%"}),
        ("DATA", "UK 11a    Overall capital requirements (%)", {"FY2025": "14.49%"}),
        ("DATA", "12    CET1 available after meeting the total SREP own funds requirements (%)",
         {"FY2025": "3.14%"}),
        ("SECTION", "Leverage ratio (£m / %)", {}),
        ("DATA", "13    Leverage ratio total exposure measure excluding claims on central banks (£m)",
         {"FY2025": 6265.4}),
        ("DATA", "14    Leverage ratio excluding claims on central banks (%)",
         {"FY2025": "5.34%", "FY2024": "5.09%", "FY2023": "5.15%"}),
        ("SECTION", "Liquidity coverage Ratio (£m / %) — weighted values, simple average of the "
                    "12 month-end observations per the source's own footnote 2", {}),
        ("DATA", "15    Total high-quality liquid assets (HQLA) (Weighted value - average) (£m)",
         {"FY2025": 2651.9}),
        ("DATA", "UK 16a    Cash outflows - Total weighted value (£m)", {"FY2025": 1317.2}),
        ("DATA", "UK 16b    Cash inflows - Total weighted value (£m)", {"FY2025": 102.1}),
        ("DATA", "16    Total net cash outflows (adjusted value) (£m)", {"FY2025": 1215.3}),
        ("DATA", "17    Liquidity coverage ratio (%)",
         {"FY2025": "218%", "FY2024": "213%", "FY2023": "220%"}),
        ("SECTION", "Net stable funding ratio (NSFR) (£m / %) — average of quarter-end positions "
                    "per the source's own footnote 3", {}),
        ("DATA", "18    Total available stable funding (£m)", {"FY2025": 3713.5}),
        ("DATA", "19    Total required stable funding (£m)", {"FY2025": 2564.9}),
        ("DATA", "20    NSFR ratio (%)",
         {"FY2025": "145%", "FY2024": "154%", "FY2023": "160%"}),
    ],
    sources_text=KM1_SOURCES,
    first_col_width=76,
    source_height=420,
)

metric(
    "CET1 Capital", "£m",
    [("Common equity tier 1 capital",
      {"FY2025": 267.7, "FY2024": 237.3, "FY2023": 205.8, "FY2022": 165.6, "FY2021": 195.2})],
    p3_sources(),
    note="FY2022/FY2021 stated as \"(audited)\" in the source; FY2024/FY2023 not marked audited/unaudited.",
)

metric(
    "CET1 Ratio", "%",
    [("Common equity tier 1 capital ratio", {"FY2025": "13.96%", "FY2024": "13.46%", "FY2023": "13.01%", "FY2022": "10.9%", "FY2021": "14.8%"})],
    p3_sources() + "\n" + PILLAR3_2025_NOTE,
    note="FY2023 and FY2024 are sourced from EFGIUK's own "
         "standalone Pillar 3 Disclosures report - see the additional source note below for the "
         "discrepancy this creates against the CET1 Capital £m sheet's own FY2024 figure.",
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 334.3, "FY2024": 303.9, "FY2023": 272.4, "FY2022": 165.6, "FY2021": 195.2})],
    p3_sources(),
    note="FY2023 and FY2024 are sourced from the standalone Pillar 3 UK KM1 table, which discloses "
         "an Additional Tier 1 component not shown in the statutory accounts' Note 34.",
)

metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 ratio", {"FY2025": "17.43%", "FY2024": "17.24%", "FY2023": "17.23%", "FY2022": "10.9%", "FY2021": "14.8%"})],
    p3_sources() + "\n" + PILLAR3_2025_NOTE,
    note="FY2023/FY2024 are sourced from the standalone Pillar 3 UK KM1 table. FY2022/FY2021 are = "
         "CET1 ratio, since no AT1 instruments were disclosed in the statutory accounts. "
         "from EFGIUK's own standalone Pillar 3 Disclosures report and is HIGHER than the FY2022/FY2021 "
         "CET1-equals-Tier1 figures because that report discloses a GBP66.6m AT1 instrument for FY2024 "
         "not mentioned in the statutory accounts - see the additional source note below.",
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 334.3, "FY2024": 303.9, "FY2023": 272.4, "FY2022": 232.3, "FY2021": 261.8})],
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
    [("Total capital ratio", {"FY2025": "17.43%", "FY2024": "17.24%", "FY2023": "17.23%", "FY2022": "15.2%", "FY2021": "19.9%"})],
    p3_sources() + "\n" + PILLAR3_2025_NOTE,
    note="FY2023/FY2024 are sourced from EFGIUK's own standalone "
         "Pillar 3 Disclosures report - see the additional source note below.",
)

metric(
    "Total RWAs", "£m",
    [("Total risk weighted assets", {"FY2025": 1918.2, "FY2024": 1763.3, "FY2023": 1581.0, "FY2022": 1523.7, "FY2021": 1317.8})],
    p3_sources() + "\n" + PILLAR3_2025_NOTE,
    note="FY2023/FY2024 are sourced from EFGIUK's standalone Pillar 3 report; FY2022/FY2021 as directly stated in the statutory "
         "accounts (not calculated). FY2024 is now sourced from EFGIUK's own standalone Pillar 3 "
         "Disclosures report, UK KM1 table - see the additional source note below (also see the RWA "
         "Breakdown sheet, which now has a full FY2024 breakdown by risk category from the same "
         "report's UK OV1 table).",
)

bw.add_rwa_breakdown_sheet(
    title="EFG Private Bank Limited — RWA Breakdown",
    subtitle="FY2025/FY2024/FY2023 (UK OV1 template, from Pillar 3 report, £m); FY2022/FY2021 a coarser "
             "2-category split (Credit risk vs. all other risk types combined) recovered from the "
             "Strategic Report (2026-09-12 re-verification) - not the same category basis as FY2023/FY2024, "
             "see source note.",
    rows=[
        ("DATA", "Credit risk (excluding CCR)", {"FY2025": 1574.8, "FY2024": 1430.2, "FY2023": 1246.2}),
        ("DATA", "  of which standardised approach", {"FY2025": 1574.8, "FY2024": 1430.2, "FY2023": 1246.2}),
        ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 55.3, "FY2024": 64.0, "FY2023": 31.6}),
        ("DATA", "  of which standardised approach", {"FY2025": 31.3, "FY2024": 38.0, "FY2023": 31.6}),
        ("DATA", "  of which credit valuation adjustment (CVA)", {"FY2025": 24.0, "FY2024": 26.0}),
        ("DATA", "Settlement risk", {"FY2025": 0, "FY2024": 0, "FY2023": 0}),
        ("DATA", "Operational risk", {"FY2025": 288.1, "FY2024": 269.0, "FY2023": 279.4}),
        ("DATA", "  of which standardised approach", {"FY2025": 288.1, "FY2024": 269.0, "FY2023": 279.4}),
        ("DATA", "Credit RWA (FY2022/FY2021 basis - pre-OV1, likely combines CCR; not directly "
                 "comparable to the 'Credit risk (excluding CCR)' row above)", {"FY2022": 1273.5, "FY2021": 1086.9}),
        ("DATA", "Other risk types combined (market, operational, settlement, non-counterparty-related - "
                 "derived residual: Total RWA less disclosed Credit RWA)", {"FY2022": 250.2, "FY2021": 230.9}),
        ("TOTAL", "Total risk-weighted exposure amount", {"FY2025": 1918.2, "FY2024": 1763.3, "FY2023": 1581.0, "FY2022": 1523.7, "FY2021": 1317.8}),
    ],
    sources_text=(
        "Sources - EFG Private Bank Limited's own accounts, Note 34 (Capital management), and its own "
        "standalone Pillar 3 Disclosures report:\n"
        "FY2025 (added 2026-09-16): the FY2025 Pillar 3's UK OV1 table, s.3.2 p.14 - credit risk "
        "(excl. CCR) 1,574.8 (all standardised), CCR 55.3 (of which standardised 31.3, CVA 24.0), "
        "settlement risk 0, operational risk 288.1 (all standardised), total 1,918.2. The components "
        "foot exactly (1,574.8 + 55.3 + 0 + 288.1 = 1,918.2). Its own column (c) also states the 8% "
        "minimum capital requirement behind each line (126.0 / 4.4 / 2.5 / 1.9 / 0 / 23.1 / 153.5), "
        "which is not reproduced as rows here because this sheet carries RWA, not requirements.\n"
        "A GBP0.1m ROUNDING DIFFERENCE BETWEEN TWO TABLES OF THE SAME DOCUMENT, recorded not "
        "reconciled: the FY2025 OV1 states FY2024 total RWA as 1,763.2, while the FY2025 KM1 (and "
        "the FY2024 edition before it) states 1,763.3. The FY2025 OV1 carries its own footnote for "
        "exactly this - 'The figures presented in the above tables may in some cases show "
        "non-significant differences due to rounding.' This sheet keeps 1,763.3 for FY2024, which is "
        "the figure FY2024's own edition reported and the one the Total RWAs sheet carries. The "
        "FY2025 figure is unaffected: OV1 and KM1 both give 1,918.2.\n"
        + NOT_DISCLOSED_NOTE +
        " Note 34 (Capital management) itself is aggregate-only in every year checked, confirmed by reading "
        "the note in full each time - no breakdown by risk category appears there.\n"
        f"FY2022/FY2021 (2026-09-12 re-verification, real data recovered - NOT a genuine non-disclosure as "
        f"previously claimed): the FY2022 Annual Report and Financial Statements' own Strategic Report, "
        f"'Capital' section, p.3 - {AR2022_URL} - states: 'Credit RWA increased by £186.6 million to £1,273.5 "
        f"million (2021: £1,086.9 million) largely due to the increased mortgage book and Treasury investment "
        f"securities holdings' - a genuine disclosed Credit RWA figure for both years (FY2021 as that year's "
        f"own comparative). This basis pre-dates the UK OV1 template used from FY2023 onward and does not "
        f"separately break out CCR/market/operational/settlement risk - Note 34's own text that year describes "
        f"RWAs as covering 'credit risk, market risk, non-counterparty-related risk, settlement risk, and "
        f"operational risk' without a category-level table, so 'Other risk types combined' here is a derived "
        f"residual (Total RWA per Note 34/Strategic Report, less the disclosed Credit RWA figure), not itself "
        f"a directly disclosed line. The FY2021 Annual Report and Financial Statements' own Strategic Report, "
        f"p.4 - {AR2021_URL} - was independently checked and confirmed to give only the aggregate Total RWA "
        f"(£1,317.8m) with no Credit RWA breakdown that year - the FY2021 Credit RWA figure used here comes "
        f"from the FY2022 report's own comparative column instead.\n"
        "FY2024 IS now available, from the UK OV1 'Overview of risk weighted exposure amounts' "
        "template, p.14 (not p.3, unlike the other Pillar 3 metrics below):\n"
        + PILLAR3_2025_NOTE
    ),
    first_col_width=54,
    source_height=280,
    unit_suffix=" (£m)",
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio (excluding claims on central banks)", {"FY2025": "5.34%", "FY2024": "5.09%", "FY2023": "5.15%"})],
    p3_sources() + "\n" + PILLAR3_2025_NOTE,
    note="FY2025, FY2024 and FY2023 all come from EFGIUK's own standalone Pillar 3 UK KM1 (row 14), "
         "each from the edition in which that year is the reporting year except FY2023, which is the "
         "FY2024 edition's comparative. FY2022 and FY2021 are blank: no leverage ratio is stated in "
         "the statutory accounts for those years (confirmed by reading the Capital management and "
         "Liquidity risk notes in full), no standalone Pillar 3 carrying a KM1 existed yet (CORRECTED "
         "2026-09-18, KM1-032: this read 'no standalone Pillar 3 existed yet', which is false - EFGIUK "
         "published a 2-page remuneration-only Pillar 3 disclosure under CRR Article 450 for FY2018, "
         "recovered from the Wayback id_ raw form of the jcr asset cited in this file's header comment; "
         "it carries no KM1, no capital amounts and no ratios, so these cells stay blank either way), "
         "and the parent's group "
         "Pillar 3 carries no block for this entity. EFGIUK is not a LREQ firm and is not required to "
         "maintain the 3.25% minimum under the UK leverage ratio framework, which the source states "
         "directly. NOTE THE FY2024 RESTATEMENT: the FY2025 edition's comparative column shows 5.34% "
         "for FY2024 where the FY2024 edition itself showed 5.09%, part of the GBP14.9m own-funds "
         "restatement described in the source note below. This sheet keeps each year's own edition.",
)

metric(
    "LCR", "%",
    [("Liquidity coverage ratio", {"FY2025": "218%", "FY2024": "213%", "FY2023": "220%"})],
    p3_sources() + "\n" + PILLAR3_2025_NOTE,
    note="BASIS: these are AVERAGES, not year-end figures. FY2025, FY2024 and FY2023 come from "
         "EFGIUK's own standalone Pillar 3 UK KM1 (row 17), whose footnote 2 states that 'Liquidity "
         "values have been calculated as a simple average of the 12-month end observations'. "
         "A SECOND, DIFFERENT LCR EXISTS FOR THE SAME YEARS and is deliberately not used here: the "
         "Annual Report's Strategic Report states a POINT-IN-TIME year-end ratio - 'The Company "
         "maintains a strong Liquidity Coverage Ratio (LCR) of 227% as at 31 December 2025 (2024: "
         "247%), against a minimum regulatory requirement of 100%'. 227%/247% and 218%/213% are two "
         "correct measurements of different things, and neither is adjusted to match the other; this "
         "sheet and the KM1 sheet both carry the KM1 average, so they agree. FY2022 and FY2021 are "
         "blank: Liquidity risk (Note 29) is purely qualitative/contractual-maturity-table based in "
         "every statutory accounts year reviewed with no LCR percentage stated anywhere, no "
         "standalone Pillar 3 existed yet, and the parent's group Pillar 3 carries no block for this "
         "entity.",
)

metric(
    "NSFR", "%",
    [("Net stable funding ratio", {"FY2025": "145%", "FY2024": "154%", "FY2023": "160%"})],
    p3_sources() + "\n" + PILLAR3_2025_NOTE,
    note="BASIS: these are AVERAGES. FY2025, FY2024 and FY2023 come from EFGIUK's own standalone "
         "Pillar 3 UK KM1 (row 20), whose footnote 3 states that 'Net stable funding values have "
         "been calculated on the average of quarter end positions'. The FY2024 Annual Report's "
         "Strategic Report separately quoted 158% for FY2024 on a year-end basis; the KM1 average of "
         "154% is used here and on the KM1 sheet, and the two are not reconciled. FY2022 and FY2021 "
         "are blank for the same reasons given on the LCR sheet.",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources() + "\n" + PILLAR3_2025_NOTE,
    per_note={
        "MREL Ratio": NOT_DISCLOSED_NOTE + " EFGIUK's own standalone Pillar 3 Disclosures report "
        "(FY2025/FY2024) also has no MREL section or figure of any kind - confirmed against that "
        "report's own table of contents, which has no MREL entry. GA-020 (2026-09-19): the FY2021-FY2025 "
        "accounts (Companies House scans, OCR) and the FY2025 Pillar 3 now served at PILLAR3_URL were re-read, "
        "with 0 MREL, eligible-liabilities or KM2 hits against 45-73 'capital' hits per document."
    },
    statements={"MREL Ratio": {
        "FY2025": "Not published – FY2025 Pillar 3 (28pp, no MREL section) and FY2025 accounts (Companies House) read 2026-09-19: no MREL figure",
        "FY2024": "Not published – FY2024 Pillar 3 (read 2026-09-04, no MREL in contents or text) and FY2024 accounts (re-read 2026-09-19): no MREL figure",
        **{y: f"Not published – {y} accounts (Companies House, OCR 2026-09-19) have no MREL figure; no {y} entity Pillar 3 (efginternational.com CDX: 47 pillar URLs, no EFGPB prudential edition)"
           for y in ["FY2023", "FY2022", "FY2021"]},
    }},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets",
         {"FY2025": 6278925, "FY2024": 6608716, "FY2023": 5856160, "FY2022": 5889606, "FY2021": 5054532}),
        ("Loans and advances to customers",
         {"FY2025": 3615957, "FY2024": 3398294, "FY2023": 2907872, "FY2022": 2967101, "FY2021": 2764761}),
        ("Due to customers",
         {"FY2025": 4932678, "FY2024": 5042962, "FY2023": 4715872, "FY2022": 4762542, "FY2021": 4152829}),
        ("Total equity",
         {"FY2025": 337050, "FY2024": 320994, "FY2023": 307366, "FY2022": 274182, "FY2021": 267264}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Operating and investing income",
         {"FY2025": 161438, "FY2024": 162206, "FY2023": 166345, "FY2022": 139354, "FY2021": 142186}),
        ("Operating expenses",
         {"FY2025": -131917, "FY2024": -134329, "FY2023": -125648, "FY2022": -104693, "FY2021": -112020}),
        ("Net profit for the year",
         {"FY2025": 23357, "FY2024": 20475, "FY2023": 35747, "FY2022": 30262, "FY2021": 101162}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity",
         {"FY2025": 320994, "FY2024": 307366, "FY2023": 274182, "FY2022": 267264, "FY2021": 264377}),
        ("Total comprehensive income for the year",
         {"FY2025": 24134, "FY2024": 19847, "FY2023": 54671, "FY2022": 14089, "FY2021": 98939}),
        ("Other equity movements, net",
         {"FY2025": -8078, "FY2024": -6219, "FY2023": -21487, "FY2022": -7171, "FY2021": -96052}),
        ("Closing equity",
         {"FY2025": 337050, "FY2024": 320994, "FY2023": 307366, "FY2022": 274182, "FY2021": 267264}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash flows from operating activities",
         {"FY2025": -476908, "FY2024": 280358, "FY2023": 89816, "FY2022": 547141, "FY2021": 586667}),
        ("Net cash flows used in investing activities",
         {"FY2025": -74967, "FY2024": -193074, "FY2023": -604152, "FY2022": -597130, "FY2021": -6442}),
        ("Net cash flows from financing activities",
         {"FY2025": -10420, "FY2024": -10064, "FY2023": -20510, "FY2022": -7747, "FY2021": -97417}),
        ("Cash and cash equivalents at end of period",
         {"FY2025": 284807, "FY2024": 846465, "FY2023": 769571, "FY2022": 1308463, "FY2021": 1369241}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "13.96%", "FY2024": "13.46%", "FY2023": "13.01%", "FY2022": "10.9%", "FY2021": "14.8%"}),
        ("Total Capital Ratio", {"FY2025": "17.43%", "FY2024": "17.24%", "FY2023": "17.23%", "FY2022": "15.2%", "FY2021": "19.9%"}),
    ],
    note="FY2025 ADDED 2026-09-16 from two documents that did not exist at the previous build: the "
         "Annual Report and Financial Statements 2025 (filed at Companies House 14 September 2026) "
         "and the FY2025 standalone Pillar 3 Disclosures (published 1 September 2026). FY2025 ratios "
         "and RWA come from the latter's UK KM1.\n"
         "FY2023's own Annual Report is supplemented by the standalone Pillar 3 comparative column, "
         "which supplies the previously missed FY2023 regulatory ratios and RWA. FY2024 ratios are "
         "sourced from EFGIUK's own standalone Pillar 3 Disclosures report (located 2026-09-04), NOT "
         "from the statutory accounts used for FY2022/FY2021 - see the CET1 Ratio/Total Capital "
         "Ratio sheets' own source notes for the resulting discrepancy against the CET1 Capital £m "
         "sheet's FY2024 figure. Note also that the FY2025 edition RESTATES FY2024 own funds upward "
         "by GBP14.9m; this workbook keeps each year on its own edition and records the restatement "
         "rather than adopting it - see the KM1 Key Metrics sheet's source note.\n"
         "FY2025 CASH FLOWS ARE A LARGE OUTFLOW and that is the Company's own reported position, not "
         "a sign error: operating activities are -476,908 against +280,358 the year before, driven "
         "by a 243,670 decrease in due to other banks and a 96,659 decrease in due to customers "
         "alongside 222,473 of net new lending. Cash and balances with central banks fall from "
         "795,400 to 219,018, which the Strategic Report explains directly ('The Company's cash at "
         "central banks decreased by GBP576.4 million due to an increase in client lending and "
         "decreases in customer deposits and deposits from related entities').\n"
         "Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each "
         "sheet's own source citation for the underlying document/page.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/EFG PRIVATE BANK FINANCIALS.xlsx")
