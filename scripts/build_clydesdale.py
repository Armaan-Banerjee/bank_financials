import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Fiscal year-end changed from 30 September to 31 March via an 18-month PRA-
# approved transition period (1 Oct 2023 - 31 Mar 2025); there is no separate
# "FY2024". See FY2025_TRANSITION_NOTE below.
YEARS = ["FY2026", "FY2025", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014", "FY2013", "FY2012", "FY2011", "FY2010", "FY2009"]  # most recent first

# HD-073 (2026-09-06): the statutory-statement sheets (Balance Sheet, P&L,
# Statement of Changes in Equity, Cash Flow Statement) use the full YEARS
# above, but Pillar 3 (all 11 metric sheets), Asset Quality, and RWA
# Breakdown are explicitly out of scope for that extension - they must keep
# FY2014 as their earliest column, same as before this ticket. Every call
# building one of those sheets passes years=PILLAR3_YEARS explicitly.
PILLAR3_YEARS = [y for y in YEARS if y not in ("FY2013", "FY2012", "FY2011", "FY2010", "FY2009")]
YEAR_LABEL = {
    "FY2026": "FY2026",
    "FY2025": "FY2025 (18mo)",
    "FY2023": "FY2023",
    "FY2022": "FY2022",
    "FY2021": "FY2021",
    "FY2020": "FY2020",
    "FY2019": "FY2019",
    "FY2018": "FY2018",
    "FY2017": "FY2017",
    "FY2016": "FY2016",
    "FY2015": "FY2015",
    "FY2014": "FY2014",
    "FY2013": "FY2013",
    "FY2012": "FY2012",
    "FY2011": "FY2011",
    "FY2010": "FY2010",
    "FY2009": "FY2009",
}

# HD-047: FY2014-FY2020 extension. Capped at FY2014 by explicit project-wide user
# decision (Pillar 3 pre-CRD IV/Basel III isn't comparable) even though Clydesdale
# Bank PLC's real disclosure archive extends to FY2009 (per HD-004). All FY2014-
# FY2020 documents below are Clydesdale Bank PLC's own entity-level Annual Report
# and Accounts (the Bank was wholly NAB-owned through Feb 2016, then part of CYBG
# plc post-demerger, then Virgin Money UK PLC from Oct 2019 rebrand - but published
# its own statutory accounts throughout, which is what is cited here, not the
# parent group's). No standalone Clydesdale Bank PLC Pillar 3 report exists for
# FY2014-FY2018 - Pillar 3-equivalent capital/RWA/leverage/LCR/NSFR disclosures for
# those years are embedded directly in the Annual Report's Risk Report section
# (confirmed by reading each report; CYBG plc's first standalone group Pillar 3
# report is cybg-pillar-3-2016.pdf, at the CYBG plc consolidated level, not the
# Clydesdale Bank PLC entity level used throughout this workbook).
AR2020_HIST_URL = "https://www.virginmoneyukplc.com/downloads/pdf/cb-ara-2020.pdf"
AR2019_HIST_URL = "https://www.virginmoneyukplc.com/downloads/pdf/cb-ara-2019.pdf"
AR2018_HIST_URL = "https://www.virginmoneyukplc.com/downloads/pdf/cb-ara-2018.pdf"
AR2017_HIST_URL = "https://www.virginmoneyukplc.com/downloads/pdf/cb-ara-2017.pdf"
AR2016_HIST_URL = "https://www.virginmoneyukplc.com/downloads/pdf/cb-ara-2016.pdf"
AR2015_HIST_URL = "https://www.virginmoneyukplc.com/downloads/pdf/cb-ara-2015.pdf"
AR2014_HIST_URL = "https://www.virginmoneyukplc.com/downloads/pdf/cb-ara-2014.pdf"

HISTORICAL_SOURCING_NOTE = (
    "HD-047 HISTORICAL SOURCING NOTE (FY2014-FY2020): all figures on this sheet for these years are transcribed "
    "from Clydesdale Bank PLC's own entity-level Annual Report and Accounts for that year, each year's own "
    "originally-published figures (not a later restated comparative), Group consolidated basis throughout. FY2015, "
    "FY2017 and FY2019 P&L/OCI figures were read from that year's own comparative column inside the FOLLOWING "
    "year's Annual Report (e.g. FY2015 from the FY2016 AR) where that gave a cleaner typeset extraction than the "
    "year's own PDF; FY2014, FY2016, FY2018 and FY2020 are each read from that year's own AR directly. The FY2014 "
    "Balance Sheet was recovered via OCR (Tesseract) since that one page of the source PDF is an embedded image "
    "with no text layer - cross-checked against the FY2014 Statement of Changes in Equity's independently-typeset "
    "closing balances, which tie out exactly, so OCR misreads are not believed to affect any figure used here. "
    "Clydesdale Bank PLC was wholly owned by National Australia Bank through the Feb 2016 CYBG plc demerger, then "
    "part of CYBG plc (renamed Virgin Money UK PLC in Oct 2019 following the Oct 2018 Virgin Money Holdings (UK) "
    "PLC acquisition) - throughout, Clydesdale Bank PLC continued publishing its own entity-level statutory "
    "accounts, which is what is used here, not the parent group's consolidated accounts."
)

HD073_AR2013_URL = "https://find-and-update.company-information.service.gov.uk/company/SC001111/filing-history/MzA4OTI2NzU1N2FkaXF6a2N4/document?format=pdf&download=0"
HD073_AR2011_URL = "https://find-and-update.company-information.service.gov.uk/company/SC001111/filing-history/MzA0NzM2MDEyOWFkaXF6a2N4/document?format=pdf&download=0"
HD073_AR2010_URL = "https://find-and-update.company-information.service.gov.uk/company/SC001111/filing-history/MzAyNzcxMTEzMGFkaXF6a2N4/document?format=pdf&download=0"

HD073_SOURCING_NOTE = (
    "HD-073 (2026-09-06) HISTORICAL SOURCING NOTE (FY2009-FY2013): all figures on this sheet for these years are "
    "transcribed from Clydesdale Bank PLC's own Group consolidated statutory accounts as filed at Companies House "
    "(company number SC001111) - the same entity-level accounts used for FY2014-FY2020 above, sourced directly "
    "from Companies House rather than virginmoneyukplc.com since that site does not host filings this old. FY2013 "
    "and FY2012 are read from the 'Annual report and consolidated financial statements for the year ended 30 "
    "September 2013' (FY2013 own-year column and FY2012 comparative column respectively) - "
    f"{HD073_AR2013_URL}. FY2011 and FY2010 are read from the 'Annual Report & Consolidated Financial Statements "
    f"30 September 2011' (FY2011 own-year column and FY2010 comparative column) - {HD073_AR2011_URL}. FY2009 is "
    "read from the 'Annual Report and Consolidated Financial Statements for the year ended 30 September 2010' "
    f"FY2009 comparative column (a standalone FY2009 filing was not separately re-verified since the FY2010 "
    f"filing reproduces FY2009's own figures as its comparative) - {HD073_AR2010_URL}. All figures are Group "
    "(consolidated) basis, £m, each year's own as-originally-filed presentation (own-year column preferred over "
    "a later comparative wherever both were available and did not tie out exactly - see the Profit & Loss sheet's "
    "own note on one confirmed FY2010 restatement). Balance Sheet, Profit & Loss and Cash Flow Statement totals "
    "for FY2009-FY2013 all reconcile to the source documents' own printed subtotals; the Statement of Changes in "
    "Equity's per-column reserve splits for FY2009-FY2010 are reconstructed from a lower-resolution scan of the "
    "filed roll-forward table and may be off by a pound or two within a row, but every closing TOTAL EQUITY "
    "balance ties exactly to the corresponding year's own Balance Sheet 'Total equity' figure, which is the "
    "authoritative anchor."
)

AR2026_URL = "https://www.virginmoneyukplc.com/downloads/pdf/cb-ara-2026-signed.pdf"
AR2025_URL = "https://www.virginmoneyukplc.com/downloads/pdf/cb-ara-2025-signed.pdf"
AR2023_URL = "https://www.virginmoneyukplc.com/downloads/pdf/cbplc-2023-ar-cfs.pdf"
AR2022_URL = "https://www.virginmoneyukplc.com/downloads/pdf/cbplc-2022-ar-cfs.pdf"
AR2021_URL = "https://www.virginmoneyukplc.com/downloads/pdf/cb-ara-2021.pdf"

P3_2026_URL = "https://www.virginmoneyukplc.com/downloads/pdf/cb-2026-pillar-3-report.pdf"
P3_2025_URL = "https://www.virginmoneyukplc.com/downloads/pdf/vmukplc-2025-pillar-3-report.pdf"
P3_2023_URL = "https://www.virginmoneyukplc.com/downloads/pdf/vmukplc-2023-pillar-3-report.pdf"
P3_2022_URL = "https://www.virginmoneyukplc.com/downloads/pdf/vmukplc-2022-pillar-3-report.pdf"
P3_2021_URL = "https://www.virginmoneyukplc.com/downloads/pdf/vm-pillar-3-2021.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Clydesdale Bank PLC (company number SC001111) is the PRA-authorised entity (FRN 121873) and the "
    "main operating banking subsidiary of Virgin Money UK PLC. On 28 July 2026 the company re-registered from a "
    "public limited company to a private limited company and is now named 'Clydesdale Bank Limited' - this workbook "
    "uses 'Clydesdale Bank PLC' throughout since that was its name for the entirety of the period covered (FY2021-"
    "FY2026). The fiscal year-end changed from 30 September to 31 March via a PRA-approved 18-month transition "
    "period (1 October 2023 - 31 March 2025, shown as 'FY2025 (18mo)' below); there is no separate FY2024 - that "
    "period is entirely contained within the 18-month column. Cash flow and Pillar 3 figures are on the 'CB Group "
    "Consolidated' / 'CB Solo-Consolidated Group' basis (Clydesdale Bank PLC's own consolidation perimeter) rather "
    "than the wider Virgin Money UK PLC group, consistent with the ring-fenced-entity basis used elsewhere in this "
    "workbook series; most annual Pillar 3 reports through FY2025 are published under the 'Virgin Money UK PLC' "
    "title but contain a dedicated CB Group Consolidated appendix, which is what is cited here."
)

NATIONWIDE_NOTE = (
    "NATIONWIDE ACQUISITION NOTE: Nationwide Building Society completed its acquisition of Virgin Money UK PLC "
    "(Clydesdale Bank PLC's parent) on 1 October 2024. On 14 November 2025 the Bank's Directors publicly announced "
    "a decision to move substantially all of the Bank's business to Nationwide by way of a Part VII banking business "
    "transfer; the High Court approved the transfer on 23 February 2026 and on 2 April 2026 the majority of the "
    "Bank's assets and liabilities transferred to Nationwide. At 31 March 2026 the transferred assets/liabilities "
    "were classified as a disposal group 'held for distribution' and the related financial performance presented as "
    f"a discontinued operation (FY2026 Annual Report and Accounts, p.60) - {AR2026_URL}."
)

FY2026_CASH_FLOW_GAP_NOTE = (
    "FY2026 cash flow is blank: the FY2026 Annual Report and Accounts moved to the FRS 101 Reduced Disclosure "
    f"Framework and explicitly took the IAS 7 'Statement of Cash Flows' disclosure exemption (p.60) - {AR2026_URL} "
    "- available to it as a qualifying subsidiary whose ultimate parent (Nationwide Building Society) publishes "
    "consolidated financial statements. No cash flow statement of any kind appears in the FY2026 accounts. See the "
    "Nationwide acquisition note above for context (the exemption coincides with the Part VII transfer of "
    "substantially all of the Bank's business)."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Clydesdale Bank PLC (CB) Group consolidated cash flow statement, £m:\n"
    f"FY2025 (18mo, 1 Oct 2023 - 31 Mar 2025): Clydesdale Bank PLC 2025 Annual Report and Accounts, p.113 "
    f"(Statement of cash flows) - {AR2025_URL}\n"
    f"FY2023: Clydesdale Bank PLC 2023 Annual report & consolidated financial statements, p.116 (Statement of cash "
    f"flows) - {AR2023_URL}\n"
    f"FY2022: Clydesdale Bank PLC 2022 Annual Report and consolidated financial statements, p.119 (Statement of "
    f"cash flows) - {AR2022_URL}\n"
    f"FY2021: Clydesdale Bank PLC 2021 Annual report & consolidated financial statements, p.119 (Statement of cash "
    f"flows) - {AR2021_URL}\n"
    f"FY2020: Clydesdale Bank PLC 2020 Annual Report and Accounts, p.120-121 (Statement of cash flows) - "
    f"{AR2020_HIST_URL}\n"
    f"FY2019: Clydesdale Bank PLC 2019 Annual Report and Accounts, p.97-98 (Statement of cash flows, own-year "
    f"presentation, not the restated comparative in the FY2020 AR) - {AR2019_HIST_URL}\n"
    f"FY2018: Clydesdale Bank PLC 2018 Annual Report and Accounts, p.79-80 (Statement of cash flows) - "
    f"{AR2018_HIST_URL}\n"
    f"FY2017: Clydesdale Bank PLC 2018 Annual Report and Accounts' FY2017 comparative column, p.79-80 (within the "
    f"FY2018 AR) - {AR2018_HIST_URL}\n"
    f"FY2016: Clydesdale Bank PLC 2016 Annual Report and Accounts, p.73 (Statement of cash flows) - "
    f"{AR2016_HIST_URL}\n"
    f"FY2015: Clydesdale Bank PLC 2016 Annual Report and Accounts' FY2015 comparative column, p.73 (within the "
    f"FY2016 AR) - {AR2016_HIST_URL}\n"
    f"FY2014: Clydesdale Bank PLC 2014 Annual Report and Accounts, p.34 (Statement of cash flows) - "
    f"{AR2014_HIST_URL}\n\n"
    "Note: the FY2025 (18mo) statement's comparative period (FY2023) is presented on a basis restated to align "
    "Group accounting policies/presentation with Nationwide, and combines some line items (e.g. interest received/"
    "paid, changes in operating assets and liabilities) that FY2021-FY2023 report split out individually; FY2023's "
    "own column above uses that year's own as-originally-reported presentation, not the restated comparative. Blank "
    "cells indicate that year's report did not disclose that specific split; where a coarser combined figure was "
    "reported instead, it appears on its own row. Section totals and cash/cash equivalents figures are consistent "
    "and comparable across all 4 populated years FY2021-FY2025.\n\n"
    "FY2014-FY2020 CASH FLOW NOTE: FY2014-FY2018 predate IFRS 9/IFRS 16 and use 'available for sale'/undifferentiated "
    "investment categories rather than FVOCI - shown on their own dedicated rows rather than merged into the FVOCI "
    "rows used from FY2019 onward. FY2018-FY2019 are dominated by the Oct 2018 Virgin Money Holdings (UK) PLC "
    "acquisition (£4,106m cash acquired, shown on its own row in FY2019). A genuine cash-and-cash-equivalents "
    "definitional discontinuity exists between FY2019 and FY2020: the FY2019 Annual Report's own closing balance "
    "is £10,120m, but the FY2020 Annual Report restates the FY2019 comparative opening balance for FY2020 to "
    "£11,131m 'in line with the current year presentation' (FY2020 AR, cash flow statement footnote 2) - both "
    "figures are shown as originally disclosed in their respective years' own reports rather than reconciled, "
    "consistent with this project's convention of using each year's own originally-published figures.\n\n"
    "FY2009-FY2013 CASH FLOW NOTE: fully disclosed for all 5 years (unlike some other HD-073 banks, Clydesdale "
    "Bank PLC's old-era statutory accounts already include a full Statement of Cash Flows, no FRS 1 exemption "
    "applies). Line items follow each year's own presentation; where FY2009-FY2013 use a label not present in "
    "later years (e.g. 'Cash inflow from matured held to maturity investments', 'Share options settled' as a "
    "financing-activity line), these appear as their own rows rather than being forced onto a later year's "
    "structure. Cash Flow figures for FY2010 are identical between the FY2010 Annual Report and the following "
    "year's FY2010 comparative column (no restatement affects this statement, unlike the Income Statement's "
    "£3m 'Other operating income' discrepancy noted on the Profit & Loss sheet).\n\n"
    + ENTITY_NOTE + "\n\n" + NATIONWIDE_NOTE + "\n\n" + FY2026_CASH_FLOW_GAP_NOTE + "\n\n" + HISTORICAL_SOURCING_NOTE
    + "\n\n" + HD073_SOURCING_NOTE
)


def p3_sources(source_label_25="21.1.2 UK KM1 - Key metrics (Appendix 1: CB Solo-Consolidated Group)", page_25="140",
               source_label_23="21.1.2 UK KM1 - Key metrics (Appendix 1: CB Group Consolidated)", page_23="123",
               source_label_22="21.1.2 UK KM1 - Key metrics (Appendix 1: CB Group Consolidated)", page_22="103",
               source_label_21="Table 57/59 (Appendix 1: Disclosures for CB Group consolidated)", page_21="77, 79",
               include_historical=True):
    text = (
        "Sources - Clydesdale Bank PLC (CB) Group/Solo-Consolidated basis:\n"
        f"FY2026: Clydesdale Bank PLC 2026 Pillar 3 Report, p.5-6 (2.1 UK KM1 - Key metrics) - {P3_2026_URL}\n"
        f"FY2025 (18mo): Virgin Money UK PLC 2025 Pillar 3 Report, p.{page_25} ({source_label_25}) - {P3_2025_URL}\n"
        f"FY2023: Virgin Money UK PLC 2023 Pillar 3 Report, p.{page_23} ({source_label_23}) - {P3_2023_URL}\n"
        f"FY2022: Virgin Money UK PLC 2022 Pillar 3 Report, p.{page_22} ({source_label_22}) - {P3_2022_URL}\n"
        f"FY2021: Virgin Money UK PLC 2021 Pillar 3 Report, p.{page_21} ({source_label_21}) - {P3_2021_URL}"
    )
    if include_historical:
        text += (
            "\n\nFY2014-FY2020 sources (no standalone Clydesdale Bank PLC Pillar 3 report exists for these years - "
            "capital/RWA/leverage/LCR/NSFR/MREL metrics are embedded in the Annual Report's Risk Report/Strategic "
            "Report 'Capital position' and liquidity sections instead, entity-level, confirmed by reading each "
            f"report):\n"
            f"FY2020 (own AR, Risk report 'Capital position'/'Capital risk', p.55-61) - {AR2020_HIST_URL}\n"
            f"FY2019 (own AR, Strategic Report 'Capital position', p.15-16) - {AR2019_HIST_URL}\n"
            f"FY2018 (own AR, Risk Report 'Balance sheet & prudential regulation risks', p.35-38) - {AR2018_HIST_URL}\n"
            f"FY2017 (FY2018 AR's FY2017 comparative column, same tables) - {AR2018_HIST_URL}\n"
            f"FY2016 (own AR, Risk Report 'Balance sheet & prudential regulation risks', p.39-42) - {AR2016_HIST_URL}\n"
            f"FY2015 (FY2016 AR's FY2015 comparative column, same tables; also own AR Strategic Report 'Capital "
            f"position', p.20-23) - {AR2016_HIST_URL} , {AR2015_HIST_URL}\n"
            f"FY2014 (own AR, Strategic Report 'Capital position', p.17-19) - {AR2014_HIST_URL}\n"
            + HISTORICAL_SOURCING_NOTE
        )
    return text


bw = BankWorkbook(bank_name="Clydesdale Bank PLC", years=YEARS, year_label=YEAR_LABEL, header_color="6D0E23")

BASIS_NOTE = (
    "BASIS NOTE: Balance Sheet/P&L figures for FY2021-FY2025 are CB Group consolidated (matching the Cash Flow "
    "Statement's own basis); each year's own originally-published figures are used, not a later restated "
    "comparative (e.g. FY2023's own 2023 Annual Report column, not the restated FY2023 comparative shown in the "
    "FY2025 report). FY2026 is a genuine entity-basis change: following the Part VII transfer of substantially all "
    "of the Bank's business to Nationwide, the FY2026 Annual Report states the Bank 'has not prepared consolidated "
    "financial statements' (relying on the Section 400 Companies Act / IFRS 10.4 exemption, since results are now "
    f"included in Nationwide's own consolidated accounts) - {AR2026_URL}. FY2026's Balance Sheet/P&L/RWA figures "
    "are therefore Bank (Company)-solo, not Group consolidated - the last comparable Group figure is FY2025."
)

STATEMENTS_SOURCES = (
    "Sources - Clydesdale Bank PLC (CB) Group consolidated Balance Sheet / Income Statement / Statement of "
    "Comprehensive Income, £m, except FY2026 which is Bank (Company)-solo (see basis note below):\n"
    f"FY2026: Clydesdale Bank PLC 2026 Annual Report and Accounts, p.57-58 (Statement of comprehensive income, "
    f"Balance sheet) - {AR2026_URL}\n"
    f"FY2025 (18mo): Clydesdale Bank PLC 2025 Annual Report and Accounts, p.108-111 (Consolidated income "
    f"statement, Consolidated statement of comprehensive income, Balance sheets, Statements of changes in equity) "
    f"- {AR2025_URL}\n"
    f"FY2023: Clydesdale Bank PLC 2023 Annual report & consolidated financial statements, p.111-114 (Consolidated "
    f"income statement, Consolidated statement of comprehensive income, Balance sheets, Statements of changes in "
    f"equity) - {AR2023_URL}\n"
    f"FY2022: Clydesdale Bank PLC 2022 Annual Report and consolidated financial statements, p.114-117 (same "
    f"statement set) - {AR2022_URL}\n"
    f"FY2021: Clydesdale Bank PLC 2021 Annual report & consolidated financial statements, p.114-118 (same "
    f"statement set) - {AR2021_URL}\n"
    f"FY2020: Clydesdale Bank PLC 2020 Annual Report and Accounts, p.116-119 (Balance sheets, Statements of "
    f"changes in equity) - {AR2020_HIST_URL}\n"
    f"FY2019: Clydesdale Bank PLC 2019 Annual Report and Accounts, p.94-97 (Balance sheets, Statements of changes "
    f"in equity) - {AR2019_HIST_URL}\n"
    f"FY2018: Clydesdale Bank PLC 2018 Annual Report and Accounts, p.75-78 (Balance sheets, Statements of changes "
    f"in equity) - {AR2018_HIST_URL}\n"
    f"FY2017: Clydesdale Bank PLC 2017 Annual Report and Accounts' FY2017 comparative column, p.76-78 (Balance "
    f"sheets, Statements of changes in equity, within the FY2018 AR) - {AR2018_HIST_URL}\n"
    f"FY2016: Clydesdale Bank PLC 2016 Annual Report and Accounts, p.70-73 (Balance sheets, Statements of changes "
    f"in equity) - {AR2016_HIST_URL}\n"
    f"FY2015: Clydesdale Bank PLC 2016 Annual Report and Accounts' FY2015 comparative column, p.70-73 (within the "
    f"FY2016 AR) - {AR2016_HIST_URL}\n"
    f"FY2014: Clydesdale Bank PLC 2014 Annual Report and Accounts, p.30-33 (Balance sheet recovered via OCR - see "
    f"historical sourcing note; income statement typeset) - {AR2014_HIST_URL}\n"
    f"FY2013: Clydesdale Bank PLC Annual report and consolidated financial statements for the year ended 30 "
    f"September 2013, p.27-31 (Consolidated income statement, Statements of comprehensive income, Balance "
    f"sheets, Statements of changes in equity) - {HD073_AR2013_URL}\n"
    f"FY2012: same FY2013 filing's FY2012 comparative column, p.27-31 - {HD073_AR2013_URL}\n"
    f"FY2011: Clydesdale Bank PLC Annual Report & Consolidated Financial Statements 30 September 2011, p.19-23 "
    f"(Consolidated Income Statement, Statements of Comprehensive Income, Balance Sheets, Statement of Changes "
    f"in Equity) - {HD073_AR2011_URL}\n"
    f"FY2010: same FY2011 filing's FY2010 comparative column, p.19-23 - {HD073_AR2011_URL}; cross-checked "
    f"against FY2010's own Annual Report and Consolidated Financial Statements for the year ended 30 September "
    f"2010, p.21-24 (own-year figures used - see FY2010 RESTATEMENT NOTE below) - {HD073_AR2010_URL}\n"
    f"FY2009: FY2010 Annual Report's FY2009 comparative column, p.21-24 - {HD073_AR2010_URL}\n\n"
    "FY2010 RESTATEMENT NOTE: the FY2010 Annual Report's own Consolidated Income Statement shows 'Other operating "
    "income' of £225m and 'Total operating income' of £1,136m for FY2010; the following year's FY2011 Annual "
    "Report's FY2010 comparative column instead shows £228m and £1,139m for the same lines (a £3m difference, "
    "unexplained in either document). This sheet uses FY2010's own as-originally-filed figures (£225m / £1,136m), "
    "consistent with this project's convention of using each year's own originally-published figures rather than "
    "a later restated comparative; the Balance Sheet and Cash Flow Statement for FY2010 are identical between "
    "both filings (no restatement affects those statements).\n\n"
    "PRESENTATION NOTE: the income statement's line-item structure changed between vintages - FY2021-FY2023 report "
    "'Gains less losses on financial instruments at fair value' + 'Other operating income' netted into a single "
    "'Non-interest income' subtotal with no separate Fee and commission income/expense lines; FY2025-FY2026 "
    "introduce explicit Fee and commission income/expense and Gains/(losses) from derivatives and hedge accounting "
    "lines instead. Both are shown as reported, not forced onto one basis. FY2026's Statement of comprehensive "
    "income splits Continuing/Discontinued operations (following the Part VII transfer); this workbook uses the "
    "combined Total column throughout, consistent with earlier years which do not split operations. FY2026's "
    "Other comprehensive income is shown only as a single total (not split into reclassifiable/non-reclassifiable "
    "sub-totals as in other years) since the FY2026 accounts do not disclose that split. A genuine cross-statement "
    "inconsistency: the FY2025 Annual Report's own P&L discloses FY2025's Total comprehensive loss as £(343)m, "
    "while its own Statement of changes in equity (Group basis) shows the same period's total comprehensive "
    "movement summing to £(331)m (a £12m difference not explained in the source document) - both figures are "
    "reproduced as disclosed on their respective sheets (P&L and Statement of Changes in Equity), not reconciled.\n\n"
    + BASIS_NOTE + "\n\n" + HISTORICAL_SOURCING_NOTE + "\n\n" + HD073_SOURCING_NOTE
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Loans and advances to customers (amortised cost)", {"FY2026": 69060, "FY2025": 71072, "FY2023": 72191, "FY2022": 71749, "FY2021": 71874, "FY2020": 72428, "FY2019": 73093, "FY2018": 32744, "FY2017": 31293, "FY2016": 29202, "FY2015": 27482, "FY2014": 25901, "FY2013": 23895, "FY2012": 24346, "FY2011": 28238, "FY2010": 26981, "FY2009": 27147}),
    ("DATA", "Fair value adjustment for portfolio hedged risk", {"FY2026": -185, "FY2025": -116}),
    ("DATA", "Cash and balances with central banks", {"FY2026": 16158, "FY2025": 10882, "FY2023": 11282, "FY2022": 12221, "FY2021": 9711, "FY2020": 9107, "FY2019": 10296, "FY2018": 6573, "FY2017": 6937, "FY2016": 5955, "FY2015": 6431, "FY2014": 5971, "FY2013": 6715, "FY2012": 7923, "FY2011": 6022, "FY2010": 4070, "FY2009": 2713}),
    ("DATA", "Due from other banks and similar institutions", {"FY2026": 528, "FY2025": 364, "FY2023": 661, "FY2022": 656, "FY2021": 800, "FY2020": 927, "FY2019": 1018, "FY2018": 836, "FY2017": 810, "FY2016": 945, "FY2015": 128, "FY2014": 184, "FY2013": 184, "FY2012": 14, "FY2011": 12, "FY2010": 11, "FY2009": 340}),
    ("DATA", "Financial assets at FVOCI", {"FY2026": 3835, "FY2025": 6197, "FY2023": 6184, "FY2022": 5064, "FY2021": 4352, "FY2020": 5080, "FY2019": 4328}),
    ("DATA", "Financial assets available for sale (pre-IFRS 9 FVOCI equivalent)", {"FY2018": 1562, "FY2017": 2076, "FY2016": 1731, "FY2015": 1462, "FY2014": 1168, "FY2013": 973, "FY2012": 1039, "FY2011": 1110, "FY2010": 2262, "FY2009": 1541}),
    ("DATA", "Investments held to maturity (pre-IFRS 9, matured/disposed of during FY2010)", {"FY2009": 639}),
    ("DATA", "Loans and advances to customers, at FVTPL", {"FY2026": 37, "FY2025": 47, "FY2023": 59, "FY2022": 70, "FY2021": 133, "FY2020": 190, "FY2019": 253}),
    ("DATA", "Other financial assets at fair value (undifferentiated FVTPL, pre-FY2019 split)", {"FY2018": 362, "FY2017": 477, "FY2016": 750, "FY2015": 1097, "FY2014": 1583, "FY2013": 2155, "FY2012": 2791, "FY2011": 5327, "FY2010": 5396, "FY2009": 5983}),
    ("DATA", "Derivative financial assets", {"FY2026": 13, "FY2025": 48, "FY2023": 135, "FY2022": 342, "FY2021": 140, "FY2020": 318, "FY2019": 366, "FY2018": 262, "FY2017": 282, "FY2016": 585, "FY2015": 285, "FY2014": 220, "FY2013": 240, "FY2012": 600, "FY2011": 537, "FY2010": 719, "FY2009": 942}),
    ("DATA", "Other financial assets at FVTPL", {"FY2026": 2, "FY2025": 1, "FY2023": 2, "FY2022": 2, "FY2021": 16, "FY2020": 1, "FY2019": 8}),
    ("DATA", "Due from related entities", {"FY2026": 614, "FY2025": 3, "FY2023": 0, "FY2022": 4, "FY2021": 4, "FY2020": 11, "FY2019": 18, "FY2018": 35, "FY2017": 366, "FY2016": 7, "FY2015": 786, "FY2014": 1495, "FY2013": 1408, "FY2012": 1256, "FY2011": 4950, "FY2010": 2839, "FY2009": 1971}),
    ("DATA", "Intangible assets and goodwill", {"FY2026": 0, "FY2025": 127, "FY2023": 173, "FY2022": 267, "FY2021": 373, "FY2020": 491, "FY2019": 516, "FY2018": 412, "FY2017": 339, "FY2016": 256, "FY2015": 265}),
    ("DATA", "Property, plant and equipment", {"FY2026": 32, "FY2025": 181, "FY2022": 211, "FY2021": 250, "FY2020": 288, "FY2019": 145, "FY2018": 88, "FY2017": 86, "FY2016": 99, "FY2015": 109, "FY2014": 106, "FY2013": 120, "FY2012": 128, "FY2011": 151, "FY2010": 157, "FY2009": 167}),
    ("DATA", "Investment properties", {"FY2018": 7, "FY2017": 14, "FY2016": 22, "FY2015": 32, "FY2014": 44, "FY2013": 63, "FY2012": 77, "FY2011": 81, "FY2010": 77, "FY2009": 33}),
    ("DATA", "Property inventory (pre-IFRS 9 era)", {"FY2013": 6, "FY2012": 9, "FY2011": 27, "FY2010": 31, "FY2009": 25}),
    ("DATA", "Due from customers on acceptances", {"FY2018": 4, "FY2017": 4, "FY2016": 4, "FY2015": 4, "FY2014": 4, "FY2013": 4, "FY2012": 7, "FY2011": 7, "FY2010": 8, "FY2009": 2}),
    ("DATA", "Accrued income and prepaid expenses", {"FY2026": 83, "FY2025": 100}),
    ("DATA", "Investments in controlled entities and associates", {"FY2022": 0, "FY2021": 0, "FY2020": 0, "FY2019": 0, "FY2018": 0, "FY2016": 0, "FY2015": 2, "FY2014": 2, "FY2013": 3, "FY2012": 3, "FY2011": 3, "FY2010": 2, "FY2009": 2}),
    ("DATA", "Current tax assets", {"FY2026": 21, "FY2025": 129, "FY2022": 0, "FY2021": 10, "FY2020": 22, "FY2019": 10, "FY2013": 23, "FY2012": 55, "FY2011": 14, "FY2010": 10, "FY2009": 5}),
    ("DATA", "Deferred tax assets", {"FY2026": 406, "FY2025": 403, "FY2023": 296, "FY2022": 256, "FY2021": 497, "FY2020": 382, "FY2019": 418, "FY2018": 298, "FY2017": 236, "FY2016": 219, "FY2015": 389, "FY2014": 287, "FY2013": 227, "FY2012": 249, "FY2011": 112, "FY2010": 144, "FY2009": 147}),
    ("DATA", "Defined benefit pension assets", {"FY2026": 366, "FY2025": 357, "FY2023": 512, "FY2022": 1000, "FY2021": 847, "FY2020": 723, "FY2019": 396, "FY2018": 212, "FY2017": 207, "FY2015": 52, "FY2014": 49}),
    ("DATA", "Other assets", {"FY2026": 50, "FY2025": 81, "FY2023": 389, "FY2022": 168, "FY2021": 209, "FY2020": 339, "FY2019": 236, "FY2018": 188, "FY2017": 187, "FY2016": 188, "FY2015": 177, "FY2014": 237, "FY2013": 616, "FY2012": 499, "FY2011": 661, "FY2010": 953, "FY2009": 713}),
    ("DATA", "Assets held for sale", {"FY2012": 5225}),
    ("TOTAL", "Total assets", {"FY2026": 91020, "FY2025": 89876, "FY2023": 91884, "FY2022": 92010, "FY2021": 89216, "FY2020": 90307, "FY2019": 91101, "FY2018": 43583, "FY2017": 43314, "FY2016": 39963, "FY2015": 38701, "FY2014": 37083, "FY2013": 36632, "FY2012": 44221, "FY2011": 47252, "FY2010": 43660, "FY2009": 42370}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer deposits", {"FY2026": 72711, "FY2025": 70383, "FY2023": 66827, "FY2022": 65434, "FY2021": 66971, "FY2020": 67710, "FY2019": 64000, "FY2018": 28904, "FY2017": 27718, "FY2016": 27090, "FY2015": 26407, "FY2014": 24073, "FY2013": 24146, "FY2012": 26381, "FY2011": 28170, "FY2010": 28434, "FY2009": 26656}),
    ("DATA", "Debt securities in issue", {"FY2026": 3749, "FY2025": 6557, "FY2023": 6155, "FY2022": 5347, "FY2021": 4241, "FY2020": 5933, "FY2019": 7267, "FY2018": 3698, "FY2017": 4006, "FY2016": 4021, "FY2015": 3766, "FY2014": 3453, "FY2013": 3071, "FY2012": 3163, "FY2011": 3553, "FY2010": 4409, "FY2009": 5287}),
    ("DATA", "Due to other banks and similar institutions", {"FY2026": 975, "FY2025": 934, "FY2023": 6920, "FY2022": 8486, "FY2021": 5918, "FY2020": 5469, "FY2019": 8916, "FY2018": 3105, "FY2017": 3808, "FY2016": 1309, "FY2015": 393, "FY2014": 914, "FY2013": 521, "FY2012": 557, "FY2011": 1507, "FY2010": 1373, "FY2009": 1920}),
    ("DATA", "Derivative financial liabilities", {"FY2026": 33, "FY2025": 132, "FY2023": 290, "FY2022": 327, "FY2021": 209, "FY2020": 250, "FY2019": 273, "FY2018": 361, "FY2017": 376, "FY2016": 598, "FY2015": 534, "FY2014": 548, "FY2013": 663, "FY2012": 952, "FY2011": 81, "FY2010": 117, "FY2009": 113}),
    ("DATA", "Other financial liabilities at fair value", {"FY2018": 15, "FY2017": 26, "FY2016": 48, "FY2015": 67, "FY2014": 91, "FY2013": 120, "FY2012": 147, "FY2011": 1005, "FY2010": 896, "FY2009": 597}),
    ("DATA", "Due to related entities", {"FY2026": 6224, "FY2025": 4304, "FY2023": 3605, "FY2022": 3210, "FY2021": 3450, "FY2020": 2822, "FY2019": 2315, "FY2018": 1313, "FY2017": 809, "FY2016": 498, "FY2015": 979, "FY2014": 2452, "FY2013": 2850, "FY2012": 7527, "FY2011": 7758, "FY2010": 3386, "FY2009": 3321}),
    ("DATA", "Liabilities on acceptances", {"FY2018": 4, "FY2017": 4, "FY2016": 4, "FY2015": 4, "FY2014": 4, "FY2013": 4, "FY2012": 7, "FY2011": 7, "FY2010": 8, "FY2009": 2}),
    ("DATA", "Current tax liabilities", {"FY2022": 7, "FY2018": 1, "FY2017": 1, "FY2016": 8}),
    ("DATA", "Deferred tax liabilities", {"FY2026": 91, "FY2025": 89, "FY2023": 179, "FY2022": 350, "FY2021": 296, "FY2020": 271, "FY2019": 199, "FY2018": 77, "FY2017": 75, "FY2016": 27, "FY2015": 10, "FY2014": 10, "FY2013": 7, "FY2012": 21, "FY2011": 32, "FY2010": 43, "FY2009": 50}),
    ("DATA", "Provisions for liabilities and charges", {"FY2026": 44, "FY2025": 39, "FY2023": 69, "FY2022": 50, "FY2021": 104, "FY2020": 172, "FY2019": 459, "FY2018": 331, "FY2017": 554, "FY2016": 852, "FY2015": 1006, "FY2014": 952, "FY2013": 315, "FY2012": 292, "FY2011": 108, "FY2010": 27, "FY2009": 14}),
    ("DATA", "Retirement benefit obligations", {"FY2018": 3, "FY2017": 3, "FY2016": 79, "FY2015": 4, "FY2014": 4, "FY2013": 202, "FY2012": 306, "FY2011": 185, "FY2010": 317, "FY2009": 320}),
    ("DATA", "Accruals and deferred income", {"FY2026": 165, "FY2025": 163}),
    ("DATA", "Other liabilities", {"FY2026": 1446, "FY2025": 1666, "FY2023": 2150, "FY2022": 2388, "FY2021": 2445, "FY2020": 2690, "FY2019": 2527, "FY2018": 2480, "FY2017": 2470, "FY2016": 2208, "FY2015": 2073, "FY2014": 2057, "FY2013": 2323, "FY2012": 2122, "FY2011": 1967, "FY2010": 2103, "FY2009": 1840}),
    ("DATA", "Liabilities associated with assets held for sale", {"FY2012": 142}),
    ("TOTAL", "Total liabilities", {"FY2026": 85438, "FY2025": 84267, "FY2023": 86195, "FY2022": 85599, "FY2021": 83634, "FY2020": 85317, "FY2019": 85960, "FY2018": 40292, "FY2017": 39850, "FY2016": 36742, "FY2015": 35243, "FY2014": 34578, "FY2013": 34222, "FY2012": 41617, "FY2011": 44373, "FY2010": 41113, "FY2009": 40120}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital and share premium", {"FY2026": 2328, "FY2025": 2043, "FY2023": 2792, "FY2022": 2792, "FY2021": 2792, "FY2020": 2792, "FY2019": 2792, "FY2018": 1013, "FY2017": 502, "FY2016": 324, "FY2015": 2812, "FY2014": 2285, "FY2013": 1985, "FY2012": 1985, "FY2011": 1485, "FY2010": 1185, "FY2009": 875}),
    ("DATA", "Other equity instruments", {"FY2026": 698, "FY2025": 693, "FY2023": 594, "FY2022": 662, "FY2021": 672, "FY2020": 672, "FY2019": 672, "FY2018": 425, "FY2017": 425, "FY2016": 425, "FY2015": 450, "FY2014": 0}),
    ("DATA", "Other reserves", {"FY2026": 44, "FY2025": 145, "FY2023": 503, "FY2022": 743, "FY2021": 44, "FY2020": -69, "FY2019": -13, "FY2018": -28, "FY2017": 373, "FY2016": 104, "FY2015": 4, "FY2014": 334, "FY2013": 370, "FY2012": 480, "FY2011": 490, "FY2010": 477, "FY2009": 459}),
    ("DATA", "Retained earnings", {"FY2026": 2512, "FY2025": 2728, "FY2023": 1800, "FY2022": 2214, "FY2021": 2074, "FY2020": 1595, "FY2019": 1690, "FY2018": 1881, "FY2017": 2164, "FY2016": 2368, "FY2015": 192, "FY2014": -114, "FY2013": 55, "FY2012": 139, "FY2011": 904, "FY2010": 885, "FY2009": 916}),
    ("TOTAL", "Total equity", {"FY2026": 5582, "FY2025": 5609, "FY2023": 5689, "FY2022": 6411, "FY2021": 5582, "FY2020": 4990, "FY2019": 5141, "FY2018": 3291, "FY2017": 3464, "FY2016": 3221, "FY2015": 3458, "FY2014": 2505, "FY2013": 2410, "FY2012": 2604, "FY2011": 2879, "FY2010": 2547, "FY2009": 2250}),
    ("TOTAL", "Total liabilities and equity", {"FY2026": 91020, "FY2025": 89876, "FY2023": 91884, "FY2022": 92010, "FY2021": 89216, "FY2020": 90307, "FY2019": 91101, "FY2018": 43583, "FY2017": 43314, "FY2016": 39963, "FY2015": 38701, "FY2014": 37083, "FY2013": 36632, "FY2012": 44221, "FY2011": 47252, "FY2010": 43660, "FY2009": 42370}),
]

bw.add_balance_sheet_sheet(
    title="Clydesdale Bank PLC — Balance Sheet",
    subtitle="CB Group consolidated basis, £m (FY2026 Bank-solo - see basis note at bottom).",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=340,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2026": 4305, "FY2025": 7042, "FY2023": 3830, "FY2022": 2215, "FY2021": 1906, "FY2020": 2137, "FY2019": 2433, "FY2018": 1113, "FY2017": 1075, "FY2016": 1101, "FY2015": 1110, "FY2014": 1135, "FY2013": 1209, "FY2012": 1461, "FY2011": 1425, "FY2010": 1392, "FY2009": 1722}),
    ("DATA", "Other similar interest", {"FY2025": 5, "FY2023": 3, "FY2022": 2, "FY2021": 4}),
    ("DATA", "Interest expense and similar charges", {"FY2026": -2594, "FY2025": -4512, "FY2023": -2147, "FY2022": -641, "FY2021": -550, "FY2020": -853, "FY2019": -917, "FY2018": -258, "FY2017": -230, "FY2016": -294, "FY2015": -321, "FY2014": -364, "FY2013": -453, "FY2012": -592, "FY2011": -442, "FY2010": -432, "FY2009": -877}),
    ("TOTAL", "Net interest income", {"FY2026": 1711, "FY2025": 2535, "FY2023": 1686, "FY2022": 1576, "FY2021": 1360, "FY2020": 1284, "FY2019": 1516, "FY2018": 855, "FY2017": 845, "FY2016": 807, "FY2015": 789, "FY2014": 771, "FY2013": 756, "FY2012": 869, "FY2011": 983, "FY2010": 960, "FY2009": 845}),
    ("DATA", "Fee and commission income", {"FY2026": 195, "FY2025": 288}),
    ("DATA", "Fee and commission expense", {"FY2026": -92, "FY2025": -119}),
    ("DATA", "Gains less losses on financial instruments at fair value", {"FY2023": -17, "FY2022": -22, "FY2021": -9, "FY2020": -20, "FY2019": -20, "FY2018": -3, "FY2017": 6, "FY2016": 9, "FY2015": 2, "FY2014": 11, "FY2013": -14, "FY2012": -123, "FY2011": -89, "FY2010": -49, "FY2009": 9}),
    ("DATA", "Gains/(losses) from derivatives and hedge accounting", {"FY2026": 5, "FY2025": -9}),
    ("DATA", "Other operating income", {"FY2026": 14, "FY2025": 46, "FY2023": 157, "FY2022": 157, "FY2021": 136, "FY2020": 171, "FY2019": 277, "FY2018": 159, "FY2017": 186, "FY2016": 182, "FY2015": 213, "FY2014": 181, "FY2013": 68, "FY2012": 251, "FY2011": 157, "FY2010": 225, "FY2009": 268}),
    ("TOTAL", "Total income", {"FY2026": 1833, "FY2025": 2741, "FY2023": 1826, "FY2022": 1711, "FY2021": 1487, "FY2020": 1435, "FY2019": 1773, "FY2018": 1011, "FY2017": 1037, "FY2016": 998, "FY2015": 1004, "FY2014": 963, "FY2013": 810, "FY2012": 997, "FY2011": 1051, "FY2010": 1136, "FY2009": 1122}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Operating and administrative expenses", {"FY2026": -1462, "FY2025": -2126, "FY2023": -1173, "FY2022": -1069, "FY2021": -1202, "FY2020": -1101, "FY2019": -1703, "FY2018": -1246, "FY2017": -1250, "FY2016": -1311, "FY2015": -1234, "FY2014": -1105}),
    ("DATA", "Personnel expenses (FY2009-FY2013, disclosed separately - see basis note)", {"FY2013": -203, "FY2012": -225, "FY2011": -265, "FY2010": -251, "FY2009": -216}),
    ("DATA", "Depreciation expense (FY2009-FY2013)", {"FY2013": -19, "FY2012": -19, "FY2011": -15, "FY2010": -21, "FY2009": -23}),
    ("DATA", "Efficiency, quality and service initiatives (FY2010-FY2011 only, as disclosed)", {"FY2011": -11, "FY2010": -19}),
    ("DATA", "Other operating expenses (FY2009-FY2013)", {"FY2013": -477, "FY2012": -481, "FY2011": -442, "FY2010": -435, "FY2009": -419}),
    ("DATA", "Restructuring expenses (FY2012 only, as disclosed)", {"FY2012": -149}),
    # Derived total-opex row bridging the two presentations: FY2014 onward, "Operating and
    # administrative expenses" alone is the full operating-expense figure (nothing else precedes
    # the profit TOTAL row for those years); FY2009-FY2013 predate that single-line presentation,
    # so the full figure is the sum of that era's own sub-component rows above (Personnel +
    # Depreciation + Efficiency initiatives (FY2010-FY2011 only) + Other operating + Restructuring
    # (FY2012 only)) - see basis note.
    ("TOTAL", "Total operating expenses (FY2014+ = 'Operating and administrative expenses' as reported; FY2009-FY2013 = sum of Personnel + Depreciation + Efficiency initiatives (FY2010-FY2011) + Other operating + Restructuring (FY2012) expenses, that era's own presentation)",
     {"FY2026": -1462, "FY2025": -2126, "FY2023": -1173, "FY2022": -1069, "FY2021": -1202, "FY2020": -1101, "FY2019": -1703, "FY2018": -1246, "FY2017": -1250, "FY2016": -1311, "FY2015": -1234, "FY2014": -1105, "FY2013": -699, "FY2012": -874, "FY2011": -733, "FY2010": -726, "FY2009": -658}),
    ("TOTAL", "Operating profit before impairment losses", {"FY2026": 371, "FY2025": 615, "FY2023": 653, "FY2022": 642, "FY2021": 285, "FY2020": 334, "FY2019": 70, "FY2018": -235, "FY2017": -213, "FY2016": -313, "FY2015": -230, "FY2014": -142, "FY2013": 111, "FY2012": 123, "FY2011": 318, "FY2010": 410, "FY2009": 442}),
    ("DATA", "Impairment losses/(credit) on credit exposures", {"FY2026": -180, "FY2025": -429, "FY2023": -309, "FY2022": -52, "FY2021": 131, "FY2020": -507, "FY2019": -252, "FY2018": -41, "FY2017": -48, "FY2016": -39, "FY2015": -78, "FY2014": -74, "FY2013": -144, "FY2012": -737, "FY2011": -297, "FY2010": -362, "FY2009": -399}),
    ("TOTAL", "Group operating profit (FY2009-FY2010 only, as disclosed - see basis note)", {"FY2010": 48, "FY2009": 43}),
    ("DATA", "Profit on sale of land and buildings (FY2009-FY2010 only)", {"FY2010": 3, "FY2009": 11}),
    ("DATA", "Special Financial Services Compensation Scheme levy (FY2009-FY2010 only)", {"FY2010": -2, "FY2009": -6}),
    ("TOTAL", "Profit on ordinary activities before tax", {"FY2026": 191, "FY2025": 186, "FY2023": 344, "FY2022": 590, "FY2021": 416, "FY2020": -173, "FY2019": -182, "FY2018": -276, "FY2017": -261, "FY2016": -352, "FY2015": -308, "FY2014": -216, "FY2013": -33, "FY2012": -614, "FY2011": 21, "FY2010": 49, "FY2009": 48}),
    ("DATA", "Tax (expense)/credit", {"FY2026": -41, "FY2025": -36, "FY2023": -95, "FY2022": -70, "FY2021": 116, "FY2020": -18, "FY2019": 43, "FY2018": 37, "FY2017": -33, "FY2016": -206, "FY2015": 59, "FY2014": 38, "FY2013": 6, "FY2012": 144, "FY2011": -3, "FY2010": -13, "FY2009": -14}),
    ("TOTAL", "Profit for the period/year", {"FY2026": 150, "FY2025": 150, "FY2023": 249, "FY2022": 520, "FY2021": 532, "FY2020": -191, "FY2019": -139, "FY2018": -239, "FY2017": -294, "FY2016": -558, "FY2015": -249, "FY2014": -178, "FY2013": -27, "FY2012": -470, "FY2011": 18, "FY2010": 36, "FY2009": 34}),
    ("SECTION", "Other comprehensive income/(expense)", {}),
    ("DATA", "Items that may be reclassified to the income statement, net of tax", {"FY2025": -358, "FY2023": -240, "FY2022": 699, "FY2021": 113}),
    ("DATA", "Items that will not be reclassified to the income statement, net of tax", {"FY2025": -135, "FY2023": -355, "FY2022": 78, "FY2021": 29}),
    ("TOTAL", "Other comprehensive income/(losses), net of tax", {"FY2026": -113, "FY2025": -493, "FY2023": -595, "FY2022": 777, "FY2021": 142, "FY2020": 129, "FY2019": 79, "FY2018": -43, "FY2017": 31, "FY2016": -39, "FY2015": -22, "FY2014": -13, "FY2013": -140, "FY2012": -281, "FY2011": 20, "FY2010": -37, "FY2009": -322}),
    ("TOTAL", "Total comprehensive income/(losses) for the period/year, net of tax", {"FY2026": 37, "FY2025": -343, "FY2023": -346, "FY2022": 1297, "FY2021": 674, "FY2020": -62, "FY2019": -60, "FY2018": -282, "FY2017": -263, "FY2016": -597, "FY2015": -271, "FY2014": -191, "FY2013": -167, "FY2012": -751, "FY2011": 38, "FY2010": -1, "FY2009": -288}),
]

bw.add_income_statement_sheet(
    title="Clydesdale Bank PLC — Profit & Loss",
    subtitle="CB Group consolidated basis, £m (FY2026 Bank-solo - see basis note at bottom).",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=340,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
equity_headers = ["Share capital and share premium", "Other equity instruments", "FVOCI reserve", "Other reserves (asset revaluation / merger / capital contribution / NCI through FY2020; other hedging reserve from FY2025)", "Cash flow hedge reserve", "Retained earnings", "Total equity"]
equity_rows = [
    ("TOTAL", "At 1 October 2008", (475, 0, 0, 365, 11, 1313, 2164)),
    ("DATA", "Profit for the year", (None, None, None, None, None, 34, 34)),
    ("DATA", "Other equity movements, net (OCI, dividends, share issuances, share options - see basis note)", (400, None, 14, -23, 92, -431, 52)),
    ("TOTAL", "At 30 September 2009", (875, 0, 14, 342, 103, 916, 2250)),
    ("DATA", "Profit for the year", (None, None, None, None, None, 36, 36)),
    ("DATA", "Other equity movements, net (OCI, dividends, share issuances, share options - see basis note)", (310, None, -8, -1, 27, -67, 261)),
    ("TOTAL", "At 30 September 2010", (1185, 0, 6, 341, 130, 885, 2547)),
    ("DATA", "Profit for the year", (None, None, None, None, None, 18, 18)),
    ("DATA", "Other equity movements, net (OCI, dividends, share issuances, share options - see basis note)", (300, None, 10, 13, -10, 1, 314)),
    ("TOTAL", "At 30 September 2011", (1485, 0, 16, 354, 120, 904, 2879)),
    ("DATA", "Loss for the year", (None, None, None, None, None, -470, -470)),
    ("DATA", "Other equity movements, net (OCI, dividends, share issuances, share options - see basis note)", (500, None, -4, -10, 4, -295, 195)),
    ("TOTAL", "At 30 September 2012", (1985, 0, 12, 344, 124, 139, 2604)),
    ("DATA", "Loss for the year", (None, None, None, None, None, -27, -27)),
    ("DATA", "Other equity movements, net (OCI, dividends, share issuances, share options - see basis note)", (0, None, -7, -2, -101, -57, -167)),
    ("TOTAL", "At 30 September 2013", (1985, 0, 5, 342, 23, 55, 2410)),
    ("DATA", "Loss for the year", (None, None, None, None, None, -178, -178)),
    ("DATA", "Other comprehensive income/(losses), net of tax", (None, None, 3, 0, -39, 23, -13)),
    ("DATA", "Dividends paid to preference shareholders", (None, None, None, None, None, -14, -14)),
    ("DATA", "Ordinary shares issued / preference shares redeemed, net", (300, None, None, None, None, None, 300)),
    ("TOTAL", "At 30 September 2014", (2285, 0, 8, 342, -16, -114, 2505)),
    ("DATA", "Loss for the year", (None, None, None, None, None, -249, -249)),
    ("DATA", "Other comprehensive income, net of tax", (None, None, 4, 0, 3, -29, -22)),
    ("DATA", "Ordinary and B ordinary shares issued, share premium reallocation and B share cancellation, net", (527, None, None, None, None, 585, 1112)),
    ("DATA", "AT1 (Additional Tier 1) capital instruments issued", (None, 450, None, None, None, None, 450)),
    ("DATA", "Merger reserve capitalised", (None, None, None, -338, None, None, -338)),
    ("TOTAL", "At 30 September 2015", (2812, 450, 12, 4, -13, 192, 3458)),
    ("DATA", "Loss for the year", (None, None, None, None, None, -558, -558)),
    ("DATA", "Other comprehensive income, net of tax", (None, None, 15, 0, 82, -136, -39)),
    ("DATA", "AT1 distributions and ordinary dividends paid", (None, None, None, None, None, -66, -66)),
    ("DATA", "Ordinary shares issued and share capital reduction, net", (-2488, None, None, None, None, 2914, 426)),
    ("DATA", "AT1 issuance and capital note repurchase, net", (None, -25, None, None, None, 21, -4)),
    ("DATA", "Other equity movements, net (share-based compensation, capital contribution, asset revaluation transfer)", (None, None, None, 3, None, 1, 4)),
    ("TOTAL", "At 30 September 2016", (324, 425, 27, 8, 69, 2368, 3221)),
    ("DATA", "Loss for the year", (None, None, None, None, None, -294, -294)),
    ("DATA", "Other comprehensive income, net of tax", (None, None, -20, 0, -68, 119, 31)),
    ("DATA", "AT1 distribution paid", (None, None, None, None, None, -29, -29)),
    ("DATA", "Ordinary shares issued", (178, None, None, None, None, None, 178)),
    ("DATA", "Capital contribution", (None, None, None, 357, None, None, 357)),
    ("TOTAL", "At 30 September 2017", (502, 425, 7, 365, 1, 2164, 3464)),
    ("DATA", "Loss for the year", (None, None, None, None, None, -239, -239)),
    ("DATA", "Other comprehensive income/(losses), net of tax", (None, None, 0, 1, -38, -6, -43)),
    ("DATA", "AT1 distribution paid", (None, None, None, None, None, -29, -29)),
    ("DATA", "Dividend paid", (None, None, None, None, None, -9, -9)),
    ("DATA", "Ordinary shares issued", (511, None, None, None, None, None, 511)),
    ("DATA", "Capital contribution", (None, None, None, -364, None, None, -364)),
    ("TOTAL", "At 30 September 2018", (1013, 425, 7, 2, -37, 1881, 3291)),
    ("DATA", "Changes on adoption of IFRS 9 and IFRS 15 (net)", (None, None, -3, None, None, -18, -21)),
    ("DATA", "Loss for the year", (None, None, None, None, None, -139, -139)),
    ("DATA", "Other comprehensive income/(losses), net of tax", (None, None, 7, -1, 12, 61, 79)),
    ("DATA", "Acquisition of Virgin Money Holdings (UK) PLC (incl. non-controlling interest)", (1549, None, None, 422, None, -17, 1954)),
    ("DATA", "Dividends, AT1 distributions, NCI distributions and share award settlements, net", (None, None, None, None, None, -107, -107)),
    ("DATA", "Ordinary shares issued", (230, None, None, None, None, None, 230)),
    ("DATA", "Capital note redemption (non-controlling interest)", (None, None, None, -422, None, 29, -393)),
    ("DATA", "AT1 issuance", (None, 247, None, None, None, None, 247)),
    ("TOTAL", "At 30 September 2019", (2792, 672, 11, 1, -25, 1690, 5141)),
    ("DATA", "Adjustment on adoption of IFRS 16 (net of tax)", (None, None, None, None, None, 1, 1)),
    ("DATA", "Loss for the year", (None, None, None, None, None, -191, -191)),
    ("DATA", "Other comprehensive losses/(income), net of tax", (None, None, None, 0, -55, 184, 129)),
    ("DATA", "AT1 distribution paid, dividends paid, share award settlements and FSMA Part VII transfer, net", (None, None, None, None, None, -89, -89)),
    ("DATA", "Release of asset revaluation reserve", (None, None, None, -1, None, None, -1)),
    ("TOTAL", "As at 1 October 2020 (=30 Sep 2020)", (2792, 672, 11, None, -80, 1595, 4990)),
    ("DATA", "Profit for the year", (None, None, None, None, None, 532, 532)),
    ("DATA", "Other comprehensive income, net of tax", (None, None, 23, None, 90, 29, 142)),
    ("DATA", "AT1 distributions paid", (None, None, None, None, None, -59, -59)),
    ("DATA", "Dividends paid to ordinary shareholders", (None, None, None, None, None, -20, -20)),
    ("DATA", "Settlement of Virgin Money Holdings (UK) Limited share awards", (None, None, None, None, None, -3, -3)),
    ("TOTAL", "At 30 September 2021", (2792, 672, 34, None, 10, 2074, 5582)),
    ("DATA", "Profit for the year", (None, None, None, None, None, 520, 520)),
    ("DATA", "Other comprehensive income, net of tax", (None, None, 10, None, 689, 78, 777)),
    ("DATA", "AT1 distributions paid", (None, None, None, None, None, -60, -60)),
    ("DATA", "Dividends paid to ordinary shareholders", (None, None, None, None, None, -367, -367)),
    ("DATA", "Settlement of Virgin Money Holdings (UK) Limited share awards", (None, None, None, None, None, -3, -3)),
    ("DATA", "AT1 issuance", (None, 346, None, None, None, None, 346)),
    ("DATA", "AT1 redemption", (None, -356, None, None, None, -28, -384)),
    ("TOTAL", "At 30 September 2022", (2792, 662, 44, None, 699, 2214, 6411)),
    ("DATA", "Profit for the year", (None, None, None, None, None, 249, 249)),
    ("DATA", "Other comprehensive losses, net of tax", (None, None, -37, None, -203, -355, -595)),
    ("DATA", "AT1 distributions paid", (None, None, None, None, None, -54, -54)),
    ("DATA", "Dividends paid to ordinary shareholders", (None, None, None, None, None, -248, -248)),
    ("DATA", "Settlement of Virgin Money Holdings (UK) Limited share awards", (None, None, None, None, None, -2, -2)),
    ("DATA", "AT1 redemption", (None, -68, None, None, None, -4, -72)),
    ("TOTAL", "At 30 September 2023 (as originally reported)", (2792, 594, 7, None, 496, 1800, 5689)),
    ("DATA", "Restatement to align Group accounting policies with Nationwide, net (per FY2025 Annual Report note 1.7)", (None, None, None, None, None, -355, -355)),
    ("TOTAL", "At 1 October 2023 (restated, per FY2025 Annual Report)", (2792, 594, 7, None, 496, 1445, 5334)),
    ("DATA", "Profit for the period", (None, None, None, None, None, 150, 150)),
    ("DATA", "Other comprehensive losses, net of tax", (None, None, -29, -3, -326, -135, -493)),
    ("DATA", "AT1 distributions paid", (None, None, None, None, None, -100, -100)),
    ("DATA", "Dividends paid to ordinary shareholders", (None, None, None, None, None, -177, -177)),
    ("DATA", "Ordinary shares issued", (800, None, None, None, None, None, 800)),
    ("DATA", "Release of share premium to retained earnings", (-1549, None, None, None, None, 1549, 0)),
    ("DATA", "Impact of share schemes moving from equity settled to cash settled", (None, None, None, None, None, -1, -1)),
    ("DATA", "AT1 issuance", (None, 346, None, None, None, None, 346)),
    ("DATA", "AT1 redemption", (None, -247, None, None, None, -3, -250)),
    ("TOTAL", "At 31 March 2025 (Group basis)", (2043, 693, -22, -3, 170, 2728, 5609)),
    ("DATA", "Entity basis change: Group to Bank (Company)-solo consolidation, net (per FY2026 Annual Report, s.400/IFRS 10.4 exemption)", (None, None, None, 2, None, -28, -26)),
    ("TOTAL", "At 31 March 2025 (restated to Bank-solo basis)", (2043, 693, -22, -1, 170, 2700, 5583)),
    ("DATA", "Profit for the period", (None, None, None, None, None, 150, 150)),
    ("DATA", "Other comprehensive income/(losses), net of tax", (None, None, 5, 1, -109, -10, -113)),
    ("DATA", "AT1 distributions paid", (None, None, None, None, None, -77, -77)),
    ("DATA", "Ordinary shares issued", (285, None, None, None, None, None, 285)),
    ("DATA", "AT1 issuance", (None, 520, None, None, None, None, 520)),
    ("DATA", "AT1 redemption", (None, -515, None, None, None, -43, -558)),
    ("DATA", "Impairment of disposal group assets", (None, None, None, None, None, -208, -208)),
    ("TOTAL", "At 31 March 2026", (2328, 698, -17, 0, 61, 2512, 5582)),
]

EQUITY_HISTORICAL_NOTE = (
    "EQUITY COLUMN NOTE (FY2014-FY2020): the 'Other reserves' column combines several reserve types that were "
    "tracked as separate line items in the FY2014-2020 Annual Reports but consolidate into a single immaterial "
    "residual by FY2021 - principally the Merger reserve (capitalised/extinguished by FY2016), Asset revaluation "
    "reserve, Capital contribution reserve (large NAB-era capital injections/returns, e.g. +£357m in FY2015-16, "
    "-£364m in FY2017-18), Share option reserve, and the temporary non-controlling interest arising from AT1 "
    "capital notes held by the immediate parent around the Oct 2018 Virgin Money Holdings (UK) PLC acquisition "
    "(+£422m, fully redeemed within FY2019). All closing-balance TOTAL rows tie exactly to each year's own "
    "Annual Report Balance Sheet and Statement of Changes in Equity; movement rows group smaller items (e.g. "
    "share-based compensation settlements, reserve transfers) into a single 'net' line per year rather than "
    "reproducing every sub-£5m entry, since the full detail is out of proportion to this ticket - the FY2020 "
    "closing balance reconciles exactly to the pre-existing FY2021 opening balance below, confirming no rounding "
    "error was introduced. See STATEMENTS_SOURCES below for exact page citations per year.\n\n"
    "EQUITY COLUMN NOTE (FY2009-FY2013, HD-073): the FY2009-2012 opening/closing TOTAL rows and 'Profit/(loss) "
    "for the year' rows are transcribed directly from each year's own Statement of Changes in Equity; every "
    "other movement in a given year (OCI reserve movements, dividends, share issuances, share option grants and "
    "settlements) is combined into a single 'Other equity movements, net' line per year, following the same "
    "documented convention as the FY2014-2020 note above. This is a deliberate simplification, not a data gap: "
    "each year's combined line is computed as that year's own closing TOTAL minus its own opening TOTAL minus "
    "the separately-shown profit/(loss) line, so every closing balance below ties exactly to the corresponding "
    "year's own Balance Sheet 'Total equity' figure (independently confirmed for all 5 years: FY2009 £2,250m, "
    "FY2010 £2,547m, FY2011 £2,879m, FY2012 £2,604m, FY2013 £2,410m - the last of which was already the "
    "pre-existing FY2014-cap opening anchor and is unchanged by this extension). FY2013's own movement rows "
    "(previously absent, since FY2013 only served as an anchor for FY2014's opening balance before this "
    "extension) are added on the same basis."
)

bw.add_equity_changes_sheet(
    title="Clydesdale Bank PLC — Statement of Changes in Equity",
    subtitle="CB Group consolidated basis through 31 Mar 2025; Bank-solo basis from 31 Mar 2025 restated onward - see basis note at bottom.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + EQUITY_HISTORICAL_NOTE,
    first_col_width=58,
    source_height=340,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit on ordinary activities before tax", {"FY2025": 186, "FY2023": 344, "FY2022": 590, "FY2021": 416, "FY2020": -173, "FY2019": -182, "FY2018": -276, "FY2017": -261, "FY2016": -352, "FY2015": -308, "FY2014": -216, "FY2013": -33, "FY2012": -614, "FY2011": 21, "FY2010": 49, "FY2009": 48}),
    ("DATA", "Non-cash or non-operating items included in profit before tax", {"FY2025": 368, "FY2023": -1203, "FY2022": -1306, "FY2021": -1221, "FY2020": -544, "FY2019": -935, "FY2018": -761, "FY2017": -735, "FY2016": -644, "FY2015": -721, "FY2014": -696, "FY2013": -583, "FY2012": -136, "FY2011": -630, "FY2010": -690, "FY2009": -685}),
    ("DATA", "Changes in operating assets", {"FY2023": -551, "FY2022": 1213, "FY2021": 819, "FY2020": -102, "FY2019": -2350, "FY2018": -1423, "FY2017": -1497, "FY2016": -2279, "FY2015": -1837, "FY2014": -1191, "FY2013": 6129, "FY2012": 463, "FY2011": -1304, "FY2010": 1119, "FY2009": -498}),
    ("DATA", "Changes in operating liabilities", {"FY2023": 284, "FY2022": -240, "FY2021": -1026, "FY2020": 1878, "FY2019": 2662, "FY2018": -122, "FY2017": 917, "FY2016": 1585, "FY2015": 2021, "FY2014": 563, "FY2013": -2657, "FY2012": -2172, "FY2011": 32, "FY2010": 1380, "FY2009": 2128}),
    ("DATA", "Changes in operating assets and liabilities (combined, as reported)", {"FY2025": -1738}),
    ("DATA", "Payments for short-term and low value leases", {"FY2023": -3, "FY2022": -2, "FY2021": -1, "FY2020": -2}),
    ("DATA", "Interest received (operating)", {"FY2023": 3300, "FY2022": 2112, "FY2021": 2088, "FY2020": 2151, "FY2019": 2320, "FY2018": 1108, "FY2017": 1124, "FY2016": 1101, "FY2015": 1257, "FY2014": 1134, "FY2013": 1213, "FY2012": 1563, "FY2011": 1649, "FY2010": 1070, "FY2009": 2017}),
    ("DATA", "Interest paid (operating)", {"FY2023": -1173, "FY2022": -378, "FY2021": -461, "FY2020": -790, "FY2019": -808, "FY2018": -169, "FY2017": -260, "FY2016": -198, "FY2015": -432, "FY2014": -257, "FY2013": -317, "FY2012": -451, "FY2011": -553, "FY2010": -134, "FY2009": -758}),
    ("DATA", "Tax paid including group relief", {"FY2025": -37, "FY2023": -50, "FY2022": -59, "FY2021": -32, "FY2020": -15, "FY2019": -8, "FY2018": -1, "FY2017": -8, "FY2016": 5, "FY2015": -4, "FY2014": 34, "FY2013": 50, "FY2012": 4, "FY2011": -13, "FY2010": -10, "FY2009": 13}),
    ("TOTAL", "Net cash provided by/(used in) operating activities", {"FY2025": -1221, "FY2023": 948, "FY2022": 1930, "FY2021": 582, "FY2020": 2403, "FY2019": 699, "FY2018": -1644, "FY2017": -720, "FY2016": -782, "FY2015": -24, "FY2014": -629, "FY2013": 3802, "FY2012": -1343, "FY2011": -798, "FY2010": 2784, "FY2009": 2265}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Interest received (investing)", {"FY2023": 232, "FY2022": 47, "FY2021": 19, "FY2020": 35, "FY2019": 28, "FY2018": 12, "FY2017": 12, "FY2016": 11, "FY2015": 8, "FY2014": 8, "FY2013": 8, "FY2012": 12, "FY2011": 25, "FY2010": 26, "FY2009": 45}),
    ("DATA", "Proceeds from maturity of financial instruments at FVOCI", {"FY2022": 479, "FY2021": 1079, "FY2020": 1568, "FY2019": 659}),
    ("DATA", "Proceeds from sale of financial assets at FVOCI", {"FY2022": 194, "FY2020": 587, "FY2019": 352}),
    ("DATA", "Proceeds from sale and maturity of financial instruments at FVOCI (combined, as reported)", {"FY2025": 2266, "FY2023": 1868}),
    ("DATA", "Purchase of financial assets at FVOCI", {"FY2025": -2198, "FY2023": -2950, "FY2022": -2019, "FY2021": -521, "FY2020": -2838, "FY2019": -1647}),
    ("DATA", "Proceeds from/(purchase of) financial assets available for sale (pre-IFRS 9)", {"FY2018": 822, "FY2017": 60, "FY2016": 56, "FY2015": 0}),
    ("DATA", "Purchase of financial assets available for sale (pre-IFRS 9)", {"FY2018": -593, "FY2017": -492, "FY2016": -357, "FY2015": -269, "FY2014": -251, "FY2013": -50, "FY2010": -735, "FY2009": -1508}),
    ("DATA", "Proceeds from maturity of investments (pre-IFRS 9)", {"FY2018": 245, "FY2017": 20, "FY2016": 101, "FY2014": 50}),
    ("DATA", "Proceeds from sale of investments (FY2009-FY2013, as disclosed)", {"FY2013": 50, "FY2012": 71, "FY2011": 1174, "FY2010": 4, "FY2009": 6}),
    ("DATA", "Purchase of held to maturity investments (FY2009, pre-IFRS 9)", {"FY2009": -638}),
    ("DATA", "Cash inflow from matured held to maturity investments (FY2010, pre-IFRS 9)", {"FY2010": 639}),
    ("DATA", "Investment in joint venture (FY2011 only)", {"FY2011": -1}),
    ("DATA", "Proceeds from sale of subsidiary (FY2009 only)", {"FY2009": 2}),
    ("DATA", "Cash acquired on acquisition of Virgin Money Holdings (UK) PLC", {"FY2019": 4106}),
    ("DATA", "Purchase of shares in UTM previously held in Virgin Money Holdings (UK) Limited", {"FY2022": -4, "FY2021": -12, "FY2020": -2, "FY2019": 45}),
    ("DATA", "Acquisition of controlled entities", {"FY2025": -20}),
    ("DATA", "Dividends received", {"FY2016": 0}),
    ("DATA", "Proceeds from sale of property, plant and equipment", {"FY2025": 3, "FY2023": 1, "FY2022": 1, "FY2021": 6, "FY2020": 5, "FY2019": 3, "FY2018": 9, "FY2017": 19, "FY2016": 17, "FY2015": 17, "FY2014": 41, "FY2013": 39, "FY2012": 38, "FY2011": 33, "FY2010": 17, "FY2009": 66}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -15, "FY2023": -9, "FY2022": -13, "FY2021": -26, "FY2020": -14, "FY2019": -20, "FY2018": -22, "FY2017": -21, "FY2016": -22, "FY2015": -15, "FY2014": -16, "FY2013": -32, "FY2012": -13, "FY2011": -41, "FY2010": -73, "FY2009": -81}),
    ("DATA", "Purchase and development of intangible assets", {"FY2025": -6, "FY2023": -11, "FY2022": -53, "FY2021": -80, "FY2020": -78, "FY2019": -130, "FY2018": -144, "FY2017": -148, "FY2016": -99}),
    ("TOTAL", "Net cash provided by/(used in) investing activities", {"FY2025": 30, "FY2023": -869, "FY2022": -1368, "FY2021": 465, "FY2020": -737, "FY2019": 3396, "FY2018": 329, "FY2017": -550, "FY2016": -293, "FY2015": -259, "FY2014": -168, "FY2013": 15, "FY2012": 108, "FY2011": 1190, "FY2010": -122, "FY2009": -2108}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Interest received (financing)", {"FY2016": 1, "FY2015": 3, "FY2014": 4, "FY2013": 5, "FY2012": 13, "FY2011": 22, "FY2010": 15}),
    ("DATA", "Interest paid (financing)", {"FY2023": -743, "FY2022": -246, "FY2021": -158, "FY2020": -87, "FY2019": -13, "FY2018": -94, "FY2017": -89, "FY2016": -97, "FY2015": -120, "FY2014": -132, "FY2013": -132, "FY2012": -229, "FY2011": -141, "FY2010": -115, "FY2009": -319}),
    ("DATA", "Repayment of principal portion of lease liabilities", {"FY2025": -40, "FY2023": -24, "FY2022": -26, "FY2021": -28, "FY2020": -30}),
    ("DATA", "Redemption and principal repayment on RMBS and covered bonds", {"FY2023": -1012, "FY2022": -1264, "FY2021": -1543, "FY2020": -1492, "FY2019": -2003, "FY2018": -1372, "FY2017": -740, "FY2016": -1029, "FY2015": -921, "FY2014": -216, "FY2013": -613, "FY2012": -936, "FY2011": -856, "FY2010": -877, "FY2009": -1414}),
    ("DATA", "Issuance of RMBS and covered bonds", {"FY2023": 1826, "FY2022": 2480, "FY2020": 491, "FY2019": 2226, "FY2018": 1049, "FY2017": 750, "FY2016": 750, "FY2015": 1207, "FY2014": 601, "FY2013": 541, "FY2012": 2644, "FY2009": 1250}),
    ("DATA", "Redemption of subordinated debt / medium-term notes", {"FY2016": -474, "FY2015": -989, "FY2012": -200}),
    ("DATA", "Maturity of medium term notes (FY2012 only)", {"FY2012": -1898}),
    ("DATA", "Issuance of AT1 securities", {"FY2025": 347, "FY2022": 347, "FY2016": 425, "FY2015": 450}),
    ("DATA", "Redemption of AT1 securities", {"FY2025": -250, "FY2023": -72, "FY2022": -384, "FY2020": 0, "FY2019": -160, "FY2016": -429}),
    ("DATA", "Redemption and principal repayment on medium-term notes", {"FY2021": 0, "FY2020": -300}),
    ("DATA", "Amounts drawn down under the TFSME", {"FY2022": 2550, "FY2021": 3350, "FY2020": 1300}),
    ("DATA", "Amounts repaid under the TFSME", {"FY2023": -1000}),
    ("DATA", "Amounts drawn down under the TFS", {"FY2018": 1250, "FY2017": 1900}),
    ("DATA", "Amounts repaid under the TFS", {"FY2022": -1244, "FY2021": -2864, "FY2020": -3234, "FY2019": -1295, "FY2018": -900}),
    ("DATA", "Proceeds from ordinary shares issued (financing)", {"FY2018": 511, "FY2017": 178, "FY2016": 426, "FY2015": 770, "FY2014": 600, "FY2012": 500, "FY2011": 100, "FY2010": 310, "FY2009": 300}),
    ("DATA", "Proceeds from redeemable preference shares issued (FY2009, FY2011 only)", {"FY2011": 200, "FY2009": 100}),
    ("DATA", "Redemption of preference shares", {"FY2014": -300}),
    ("DATA", "Share options settled (FY2009-FY2010 only, as disclosed)", {"FY2010": -17, "FY2009": -35}),
    ("DATA", "Net (increase)/decrease in amounts due from related entities", {"FY2025": -55, "FY2023": 7, "FY2022": 1, "FY2021": 9, "FY2020": 9, "FY2019": -12, "FY2018": 0, "FY2017": -2, "FY2016": 786, "FY2015": 694, "FY2014": -73, "FY2013": -152, "FY2012": 3694, "FY2011": -2111, "FY2010": -868, "FY2009": -818}),
    ("DATA", "Net increase/(decrease) in amounts due to related entities", {"FY2025": 373, "FY2023": 297, "FY2022": 9, "FY2021": 705, "FY2020": 439, "FY2019": 611, "FY2018": 505, "FY2017": 311, "FY2016": 407, "FY2015": -354, "FY2014": -338, "FY2013": -4846, "FY2012": -233, "FY2011": 4368, "FY2010": 180, "FY2009": -1792}),
    ("DATA", "AT1 distributions", {"FY2025": -66, "FY2023": -54, "FY2022": -60, "FY2021": -59, "FY2020": -59, "FY2019": -41, "FY2018": -36, "FY2017": -36, "FY2016": -19}),
    ("DATA", "Distributions to non-controlling interests", {"FY2019": -33}),
    ("DATA", "Ordinary dividends paid", {"FY2025": -211, "FY2023": -248, "FY2022": -367, "FY2021": -20, "FY2020": -20, "FY2019": -44, "FY2018": -9, "FY2016": -51, "FY2014": -14}),
    ("DATA", "Dividends paid (FY2009-FY2013, preference shares - see Statement of Changes in Equity)", {"FY2013": -24, "FY2012": -15, "FY2011": -21, "FY2010": -12, "FY2009": -6}),
    ("DATA", "Proceeds from issuance of other equity instruments", {"FY2020": 0, "FY2019": 247}),
    ("DATA", "Proceeds from ordinary shares issued", {"FY2025": 800}),
    ("DATA", "Other financing items, net (equity-based compensation settlements, etc.)", {"FY2016": -7}),
    ("TOTAL", "Net cash provided by/(used in) financing activities", {"FY2025": 898, "FY2023": -1023, "FY2022": 1796, "FY2021": -608, "FY2020": -2983, "FY2019": -517, "FY2018": 905, "FY2017": 2272, "FY2016": 688, "FY2015": 740, "FY2014": 132, "FY2013": -5221, "FY2012": 3340, "FY2011": 1561, "FY2010": -1384, "FY2009": -2734}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -293, "FY2023": -944, "FY2022": 2358, "FY2021": 439, "FY2020": -1317, "FY2019": 3578, "FY2018": -410, "FY2017": 1002, "FY2016": -387, "FY2015": 457, "FY2014": -665, "FY2013": -1404, "FY2012": 2105, "FY2011": 1953, "FY2010": 1278, "FY2009": -2577}),
    ("DATA", "Cash and cash equivalents at the beginning of the period/year", {"FY2025": 10589, "FY2023": 12611, "FY2022": 10253, "FY2021": 9814, "FY2020": 11131, "FY2019": 6542, "FY2018": 6952, "FY2017": 5950, "FY2016": 6337, "FY2015": 5880, "FY2014": 6545, "FY2013": 7949, "FY2012": 5844, "FY2011": 3891, "FY2010": 2613, "FY2009": 5190}),
    ("TOTAL", "Cash and cash equivalents at the end of the period/year", {"FY2025": 10296, "FY2023": 11667, "FY2022": 12611, "FY2021": 10253, "FY2020": 9814, "FY2019": 10120, "FY2018": 6542, "FY2017": 6952, "FY2016": 5950, "FY2015": 6337, "FY2014": 5880, "FY2013": 6545, "FY2012": 7949, "FY2011": 5844, "FY2010": 3891, "FY2009": 2613}),
]

bw.add_cash_flow_sheet(
    title="Clydesdale Bank PLC — Consolidated Cash Flow Statement",
    subtitle="Clydesdale Bank (CB) Group (consolidated basis), £m unless stated. FY2026 blank - see source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=72,
    source_height=280,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
ASSET_QUALITY_SOURCES = (
    "Sources - 'Gross loans and advances ECL and coverage' table (audited), Risk report, Total column, £m:\n"
    f"FY2026/FY2025: Clydesdale Bank PLC 2026 Annual Report and Accounts, p.15 - {AR2026_URL}\n"
    f"FY2023/FY2022: Clydesdale Bank PLC 2023 Annual report & consolidated financial statements, p.22 - {AR2023_URL}\n"
    f"FY2021: Clydesdale Bank PLC 2021 Annual report & consolidated financial statements, p.25 - {AR2021_URL}\n"
    f"FY2020: Clydesdale Bank PLC 2020 Annual Report and Accounts, 'Gross loans and advances by IFRS 9 stage "
    f"allocation' / 'ECL impairment allowance by IFRS 9 stage allocation' tables (Risk report) - {AR2020_HIST_URL}\n"
    f"FY2019: Clydesdale Bank PLC 2019 Annual Report and Accounts, same tables, p.18-25 (Risk report) - "
    f"{AR2019_HIST_URL}\n\n"
    "Excludes loans designated at FVTPL, balances due from customers on acceptances, accrued interest and "
    "deferred/unamortised fee income - so the Total gross figure here is smaller than the Balance Sheet's "
    "'Loans and advances to customers (amortised cost)' line, which is expected and not reconciled (a source-"
    "table scope difference, not an error). Ratios calculated here from the disclosed stage-level figures: NPL "
    "ratio = Stage 3 gross / Total gross; Stage 3 coverage = Stage 3 ECL / Stage 3 gross; Total coverage = Total "
    "ECL / Total gross - all match the source table's own disclosed coverage percentages exactly. FY2019's Stage 3 "
    "figures include POCI (purchased or originated credit-impaired) balances acquired with Virgin Money Holdings "
    "(UK) PLC in Oct 2018, combined onto the Stage 3 row rather than shown separately.\n\n"
    "FY2014-FY2018 PRE-IFRS 9 NOTE: IFRS 9 (and its Stage 1/2/3 model) was adopted by Clydesdale Bank PLC on 1 "
    "October 2018 (transition disclosed in the FY2019 AR); FY2014-FY2018 used the IAS 39 incurred-loss model, "
    "which does not have an equivalent stage split. A second table below shows the IAS 39-era metrics as actually "
    "disclosed for FY2014-FY2018 (gross loans and advances, 90+ days-past-due assets, impaired assets, total "
    "impairment provisions) - these are NOT the same measure as the IFRS 9 Stage 1/2/3 table above and are not "
    "comparable to it; see FY2014-FY2018 source citations directly below that table.\n\n"
    "FY2014-FY2018 SOURCES (IAS 39-era table): Clydesdale Bank PLC Annual Report and Accounts, Strategic Report / "
    "Risk report 'Past due and impaired assets' and 'Impairment provisions on credit exposures' disclosures - "
    f"FY2014 (own AR, p.~10) - {AR2014_HIST_URL}; FY2015 (own AR, p.21-22) - {AR2015_HIST_URL}; FY2016 (own AR) - "
    f"{AR2016_HIST_URL}; FY2017 (own AR narrative, p.3) - {AR2017_HIST_URL}; FY2018 total impairment provisions "
    f"only (own AR note 3.6/5.2) - {AR2018_HIST_URL}. FY2018's 90+DPD and gross impaired assets £m figures are "
    "left blank: the FY2018 Annual Report's entity-level Strategic Report no longer carries this narrative KPI "
    "table (confirmed absent by reading the full report), likely because that level of detail migrated to CYBG "
    "plc's own group-level annual report following the Feb 2016 demerger - self-skipped per this project's "
    "self-skip convention rather than substituting a group-level figure for an entity-level metric.\n\n"
    + BASIS_NOTE
)

asset_quality_rows = [
    ("SECTION", "Gross lending assets by IFRS 9 stage (FY2019-FY2026 only - see IAS 39 note)", {}),
    ("DATA", "Stage 1", {"FY2026": 60522, "FY2025": 61585, "FY2023": 65889, "FY2022": 66385, "FY2021": 61416, "FY2020": 59219, "FY2019": 67923}),
    ("DATA", "Stage 2", {"FY2026": 8069, "FY2025": 8271, "FY2023": 6326, "FY2022": 5723, "FY2021": 10176, "FY2020": 12842, "FY2019": 4514}),
    ("DATA", "Stage 3 (incl. POCI from FY2019)", {"FY2026": 1145, "FY2025": 1351, "FY2023": 1080, "FY2022": 1036, "FY2021": 957, "FY2020": 862, "FY2019": 807}),
    ("TOTAL", "Total gross lending assets", {"FY2026": 69736, "FY2025": 71207, "FY2023": 73295, "FY2022": 73144, "FY2021": 72549, "FY2020": 72923, "FY2019": 73244}),
    ("SECTION", "Expected credit loss (ECL) allowance by stage (FY2019-FY2026 only)", {}),
    ("DATA", "Stage 1", {"FY2026": 139, "FY2025": 119, "FY2023": 89, "FY2022": 85, "FY2021": 111, "FY2020": 136, "FY2019": 79}),
    ("DATA", "Stage 2", {"FY2026": 359, "FY2025": 406, "FY2023": 400, "FY2022": 268, "FY2021": 302, "FY2020": 465, "FY2019": 168}),
    ("DATA", "Stage 3 (incl. POCI from FY2019)", {"FY2026": 181, "FY2025": 212, "FY2023": 128, "FY2022": 104, "FY2021": 91, "FY2020": 134, "FY2019": 115}),
    ("TOTAL", "Total ECL allowance", {"FY2026": 679, "FY2025": 737, "FY2023": 617, "FY2022": 457, "FY2021": 504, "FY2020": 735, "FY2019": 362}),
    ("TOTAL", "Net lending assets (Total gross - Total ECL)", {"FY2026": 69057, "FY2025": 70470, "FY2023": 72678, "FY2022": 72687, "FY2021": 72045, "FY2020": 72188, "FY2019": 72882}),
    ("SECTION", "Asset quality ratios (FY2019-FY2026 only)", {}),
    ("DATA", "Total coverage ratio (Total ECL / Total gross)", {"FY2026": "0.97%", "FY2025": "1.04%", "FY2023": "0.84%", "FY2022": "0.62%", "FY2021": "0.70%", "FY2020": "1.01%", "FY2019": "0.49%"}),
    ("DATA", "NPL ratio (Stage 3 gross / Total gross)", {"FY2026": "1.6%", "FY2025": "1.9%", "FY2023": "1.5%", "FY2022": "1.4%", "FY2021": "1.3%", "FY2020": "1.18%", "FY2019": "1.10%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 ECL / Stage 3 gross)", {"FY2026": "15.81%", "FY2025": "15.69%", "FY2023": "13.93%", "FY2022": "11.24%", "FY2021": "9.59%", "FY2020": "15.55%", "FY2019": "14.25%"}),
    ("SECTION", "IAS 39-era asset quality (FY2014-FY2018 - not comparable to IFRS 9 stages above)", {}),
    ("DATA", "Gross loans and advances to customers", {"FY2018": 32917, "FY2017": 31488, "FY2016": 29396, "FY2015": 27687, "FY2014": 26121}),
    ("DATA", "90+ days past due (DPD) assets", {"FY2017": 161, "FY2016": 150, "FY2015": 143, "FY2014": 182}),
    ("DATA", "Gross impaired assets", {"FY2017": 179, "FY2016": 233, "FY2015": 263, "FY2014": 375}),
    ("TOTAL", "Total impairment provisions on credit exposures", {"FY2018": 195, "FY2017": 210, "FY2016": 215, "FY2015": 230, "FY2014": 245}),
    ("DATA", "Total provision to gross loans and acceptances (%, as disclosed)", {"FY2016": "0.79%", "FY2015": "0.93%", "FY2014": "1.15%"}),
    ("DATA", "90+DPD plus gross impaired assets to gross loans (%, as disclosed)", {"FY2017": "1.06%", "FY2016": "1.27%", "FY2015": "1.41%", "FY2014": "2.01%"}),
]

bw.add_asset_quality_sheet(
    title="Clydesdale Bank PLC — Asset Quality",
    subtitle="CB Group consolidated basis through FY2025; Bank-solo basis for FY2026, £m (ratios as disclosed). See source note at bottom.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=76,
    source_height=280,
    unit_suffix=" (£m)",
    years=PILLAR3_YEARS,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"CB consolidated basis, {unit}" if unit else "CB consolidated basis",
                         rows_data, sources_text, note=note, first_col_width=44, source_height=110,
                         years=PILLAR3_YEARS)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2026": 4248, "FY2025": 3900, "FY2023": 3685, "FY2022": 3606, "FY2021": 3603, "FY2020": 3508, "FY2019": 3462, "FY2018": 2148, "FY2017": 2440, "FY2016": 2393, "FY2015": 2420, "FY2014": 2227})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2026": "14.3%", "FY2025": "14.2%", "FY2023": "14.6%", "FY2022": "14.9%", "FY2021": "14.9%", "FY2020": "14.4%", "FY2019": "14.4%", "FY2018": "10.7%", "FY2017": "12.2%", "FY2016": "12.6%", "FY2015": "13.3%", "FY2014": "12.1%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2026": 4946, "FY2025": 4593, "FY2023": 4279, "FY2022": 4268, "FY2021": 4275, "FY2020": 4180, "FY2019": 4134, "FY2018": 2573, "FY2017": 2865, "FY2016": 2818, "FY2015": 2870, "FY2014": 2227})],
    p3_sources(),
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2026": "16.6%", "FY2025": "16.7%", "FY2023": "17.0%", "FY2022": "17.7%", "FY2021": "17.7%", "FY2020": "17.1%", "FY2019": "17.2%", "FY2018": "12.8%", "FY2017": "14.3%", "FY2016": "14.8%", "FY2015": "15.8%", "FY2014": "12.1%"})],
    p3_sources(),
    note="FY2014 Tier 1 ratio equals the CET1 ratio: Clydesdale Bank PLC held no Additional Tier 1 (AT1) capital "
         "instruments at 30 September 2014 - the first AT1 issuance (£350m) came in December 2014, within FY2015.",
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2026": 5747, "FY2025": 5347, "FY2023": 5301, "FY2022": 5288, "FY2021": 5294, "FY2020": 4929, "FY2019": 4857, "FY2018": 3202, "FY2017": 3495, "FY2016": 3448, "FY2015": 3483, "FY2014": 3438})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2026": "19.3%", "FY2025": "19.4%", "FY2023": "21.1%", "FY2022": "21.9%", "FY2021": "21.9%", "FY2020": "20.2%", "FY2019": "20.2%", "FY2018": "15.9%", "FY2017": "17.4%", "FY2016": "18.1%", "FY2015": "19.1%", "FY2014": "18.6%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted exposure amount", {"FY2026": 29742, "FY2025": 27555, "FY2023": 25172, "FY2022": 24128, "FY2021": 24194, "FY2020": 24384, "FY2019": 24046, "FY2018": 20117, "FY2017": 20055, "FY2016": 19017, "FY2015": 18207, "FY2014": 18472})],
    p3_sources(),
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - UK OV1: Overview of risk-weighted exposure amounts, CB Group/Solo-Consolidated basis, £m:\n"
    f"FY2026: Clydesdale Bank PLC 2026 Pillar 3 Report, p.9 (2.3 UK OV1) - {P3_2026_URL}\n"
    f"FY2025 (18mo): Virgin Money UK PLC 2025 Pillar 3 Report, p.139 (Appendix 1: CB Solo-Consolidated Group, "
    f"21.1.1 UK OV1) - {P3_2025_URL}\n"
    f"FY2023: Virgin Money UK PLC 2023 Pillar 3 Report, p.122 (Appendix 1: CB Group Consolidated, 21.1.1 UK OV1) "
    f"- {P3_2023_URL}\n"
    f"FY2022: Virgin Money UK PLC 2022 Pillar 3 Report, p.102 (Appendix 1: CB Group Consolidated, 21.1.1 UK OV1) "
    f"- {P3_2022_URL}\n\n"
    "FY2021: not publicly disclosed at category level - the CB appendix in Virgin Money UK PLC's 2021 Pillar 3 "
    "Report only carries Table 57 (capital composition) and Table 58 (capital flow statement), both of which "
    "disclose only the Total RWA figure (£24,194m, already shown on the Total RWAs sheet), not a risk-category "
    "split - confirmed by reading the full appendix (pp.77-79), not assumed. A restated FY2021 comparative split "
    "does exist in the FY2022 Pillar 3 report's own OV1 table (per its PS22/21 restatement footnote) but is not "
    "used here, consistent with this project's convention of using each year's own originally-published figures.\n\n"
    "FY2014-FY2020: sourced from each year's own Annual Report 'RWA' / 'Capital position and CET1' tables (Risk "
    "Report), which split RWA into Credit risk, Operational risk, Counterparty risk and Credit valuation "
    "adjustment (CVA) rather than the standardised/FIRB/AIRB/CCR sub-splits used from FY2021 onward - shown on "
    "the 'Credit risk' and 'Operational risk' rows with the CCR/CVA sub-split combined onto the 'Counterparty "
    "credit risk (CCR)' row's CVA line (FY2014-FY2019 pre-date the separate IRB accreditation that produced "
    "FY2020's finer approach-level split, so no standardised/FIRB/AIRB breakdown exists for FY2014-FY2019).\n\n"
    + BASIS_NOTE
)

rwa_breakdown_rows = [
    ("SECTION", "RWA by risk category", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2026": 26567, "FY2025": 24361, "FY2023": 21907, "FY2022": 21061, "FY2020": 21463, "FY2019": 21042, "FY2018": 18104, "FY2017": 18116, "FY2016": 16912, "FY2015": 16301, "FY2014": 16605}),
    ("DATA", "Of which: standardised approach", {"FY2026": 6186, "FY2025": 6674, "FY2023": 6431, "FY2022": 6120, "FY2020": 5618, "FY2019": 5938, "FY2018": 18104, "FY2017": 18116, "FY2016": 16912, "FY2015": 16301, "FY2014": 16605}),
    ("DATA", "Of which: foundation IRB (FIRB) approach", {"FY2026": 7658, "FY2025": 7725, "FY2023": 5994, "FY2022": 5424}),
    ("DATA", "Of which: slotting approach", {"FY2026": 691, "FY2025": 618, "FY2023": 410, "FY2022": 362}),
    ("DATA", "Of which: advanced IRB (AIRB) approach", {"FY2026": 12032, "FY2025": 9344, "FY2023": 9072, "FY2022": 9155, "FY2020": 15845, "FY2019": 15104}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2026": 48, "FY2025": 103, "FY2023": 424, "FY2022": 443, "FY2020": 354, "FY2019": 383, "FY2018": 343, "FY2017": 305, "FY2016": 499, "FY2015": 344, "FY2014": 318}),
    ("DATA", "Of which: standardised approach", {"FY2026": 35, "FY2025": 80, "FY2023": 141, "FY2022": 180}),
    ("DATA", "Of which: credit valuation adjustment (CVA)", {"FY2026": 8, "FY2025": 19, "FY2023": 278, "FY2022": 258, "FY2020": 175, "FY2019": 192, "FY2018": 218, "FY2017": 167, "FY2016": 285, "FY2015": 206, "FY2014": 137}),
    ("DATA", "Operational risk", {"FY2026": 3127, "FY2025": 3091, "FY2023": 2841, "FY2022": 2624, "FY2020": 2567, "FY2019": 2621, "FY2018": 1670, "FY2017": 1634, "FY2016": 1606, "FY2015": 1562, "FY2014": 1549}),
    ("DATA", "Amounts below thresholds for deduction (subject to 250% risk weight)", {"FY2026": 513, "FY2025": 516, "FY2023": 284, "FY2022": 251}),
    ("TOTAL", "Total RWAs", {"FY2026": 29742, "FY2025": 27555, "FY2023": 25172, "FY2022": 24128, "FY2021": 24194, "FY2020": 24384, "FY2019": 24046, "FY2018": 20117, "FY2017": 20055, "FY2016": 19017, "FY2015": 18207, "FY2014": 18472}),
]

bw.add_rwa_breakdown_sheet(
    title="Clydesdale Bank PLC — RWA Breakdown",
    subtitle="CB Group/Solo-Consolidated basis, £m. FY2021 category split not publicly disclosed; FY2014-FY2020 use a coarser standardised-approach-only split - see source note at bottom.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=54,
    source_height=280,
    years=PILLAR3_YEARS,
    unit_suffix=" (£m)",
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total exposure measure excluding claims on central banks", {"FY2026": 78792, "FY2025": 83120, "FY2023": 86545, "FY2022": 83758, "FY2021": 84293, "FY2020": 86475, "FY2019": 94742}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2026": "6.3%", "FY2025": "5.5%", "FY2023": "4.9%", "FY2022": "5.1%", "FY2021": "5.1%", "FY2020": "4.8%", "FY2019": "4.4%", "FY2018": "5.6%", "FY2017": "6.2%", "FY2016": "6.8%", "FY2015": "7.2%", "FY2014": "5.7%"}),
        ("Leverage ratio including claims on central banks (%)", {"FY2026": "5.3%", "FY2025": "5.0%", "FY2023": "4.5%", "FY2022": "4.5%"}),
        ("UK leverage ratio (%)", {"FY2020": "4.9%", "FY2019": "4.9%", "FY2018": "6.5%", "FY2017": "7.3%"}),
    ],
    p3_sources(),
    note="FY2021's Pillar 3 report disclosed a single 'Leverage ratio' (5.1%) without an excluding/including claims "
         "on central banks split (that distinction was introduced in later reports), shown here on the 'excluding' "
         "row for comparability. FY2022's exposure measure (83,758) reflects a PS22/21-driven restatement to "
         "exclude Bounce Back Loan Scheme (BBLS) balances; FY2021's figure (84,293) is as originally reported and "
         "was not restated on the same basis, so the FY2021-to-FY2022 leverage exposure movement is not fully "
         "like-for-like. FY2014-FY2020 report a plain 'CRD IV Leverage ratio' (Tier 1 capital / total exposure, no "
         "central-bank-claims split) shown on the 'excluding' row for continuity; a separate 'UK leverage ratio' "
         "(modified basis excluding qualifying central bank claims from the exposure measure, a UK-specific "
         "framework in force from 1 Jan 2016) is shown on its own row from FY2017, the first year it was disclosed.",
)

metric(
    "LCR", "£m / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value (average)", {"FY2026": 16246, "FY2025": 14868, "FY2023": 13798, "FY2022": 11503}),
        ("Total net cash outflows, adjusted value", {"FY2026": 9912, "FY2025": 9414, "FY2023": 9424, "FY2022": 8222}),
        ("Liquidity Coverage Ratio (%)", {"FY2026": "164%", "FY2025": "158%", "FY2023": "146%", "FY2022": "140%", "FY2021": "Not disclosed", "FY2020": "140%", "FY2019": "152%", "FY2018": "137%", "FY2017": "164%", "FY2016": "140%", "FY2015": "136%", "FY2014": "110%"}),
    ],
    p3_sources(),
    note="LCR is a 12-month simple average of month-end observations. Not disclosed for FY2021 at the CB Group "
         "Consolidated level in the 2021 Pillar 3 report's dedicated CB appendix (only narrative/glossary mentions "
         "of LCR appear elsewhere in that report). FY2014-FY2020 LCR percentages are narrative disclosures in the "
         "Annual Report (Strategic Report/Risk Report) rather than a KM1-style table with HQLA/outflow £m amounts, "
         "so only the ratio itself is populated for those years, not the underlying £m components.",
)

metric(
    "NSFR", "£m / %",
    [
        ("Total available stable funding", {"FY2026": 78219, "FY2025": 77427, "FY2023": 79295}),
        ("Total required stable funding", {"FY2026": 54560, "FY2025": 54375, "FY2023": 58450}),
        ("NSFR ratio (%)", {"FY2026": "143%", "FY2025": "142%", "FY2023": "136%", "FY2022": "136%", "FY2021": "134%", "FY2020": "131%", "FY2019": "128%", "FY2018": "125%", "FY2017": "118%", "FY2016": "124%", "FY2015": "120%", "FY2014": "108%"}),
    ],
    p3_sources() + (
        f"\n\nFY2022 & FY2021 NSFR ONLY: not in the Pillar 3 reports above - the UK NSFR disclosure regime (PRA "
        f"PS17/21 / PS22/21, in force 1 January 2022) requires a four-quarter average, which PS17/21 states makes "
        f"'the first disclosures being required after Sunday 1 January 2023'; with a 30 September year-end, CB's "
        f"first KM1 NSFR is therefore FY2023. The Bank did however continue its own voluntary narrative disclosure "
        f"in both years:\n"
        f"FY2022 (136%, y/e 30 Sep 2022): Clydesdale Bank PLC Annual Report and Accounts 2022, Business and "
        f"Financial Review 'Funding and liquidity', p.2 - {AR2022_URL}\n"
        f"FY2021 (134%, y/e 30 Sep 2021): Clydesdale Bank PLC Annual Report and Accounts 2021, Risk Report "
        f"'Liquidity and funding risk' asset-encumbrance commentary ('The introduction of a binding NSFR is due to "
        f"be implemented in the UK on 1 January 2022. Based on current interpretations of European regulatory "
        f"requirements and guidance, the ratio as at 30 September 2021 is 134% (2020: 131%)') - {AR2021_URL}. Note "
        f"the FY2021 report's own front-section highlights mis-state this as 'at 30 September 2020'; the Risk "
        f"Report wording above is unambiguous and its 2020 comparative of 131% ties to this workbook's FY2020.\n"
    ),
    note="FY2014-FY2022 NSFR is the Bank's own voluntary/early estimate under its own interpretation of then-draft "
         "Basel III / CRD IV guidance (the Annual Reports say so explicitly), narrative-only (no £m components "
         "disclosed). FY2023 onward is the PRA-mandated UK KM1 measure, a four-quarter average - the two bases are "
         "not directly comparable, which is why only FY2023+ carry available/required stable funding components. "
         "The UK NSFR requirement itself only took effect 1 January 2022, and the four-quarter-average disclosure "
         "basis meant no KM1 NSFR was required of a 30 September year-end firm until FY2023.",
)

metric(
    "MREL Ratio", "£m / %",
    [
        ("Total capital resources", {"FY2026": 5747, "FY2025": 5347, "FY2023": 5301, "FY2022": 5288, "FY2020": 4929, "FY2019": 4857}),
        ("Eligible senior unsecured securities", {"FY2026": 3520, "FY2025": 3004, "FY2023": 2707, "FY2022": 2423, "FY2020": 2002, "FY2019": 1550}),
        ("Total MREL resources", {"FY2026": 9267, "FY2025": 8351, "FY2023": 8008, "FY2022": 7711, "FY2020": 6931, "FY2019": 6407}),
        ("MREL resources (% of total risk-weighted assets)", {"FY2026": "31.2%", "FY2025": "30.3%", "FY2023": "31.8%", "FY2022": "32.0%", "FY2021": "Not disclosed", "FY2020": "28.4%", "FY2019": "26.6%", "FY2018": "Not disclosed", "FY2017": "Not disclosed", "FY2016": "Not disclosed", "FY2015": "Not disclosed", "FY2014": "Not disclosed"}),
        ("MREL resources (% of UK leverage exposure measure)", {"FY2026": "11.8%", "FY2025": "10.0%", "FY2023": "9.3%", "FY2022": "9.2%"}),
    ],
    p3_sources(),
    note="'Eligible senior unsecured securities' were issued by Clydesdale Bank PLC through FY2023, but by Virgin "
         "Money UK PLC from the FY2025 (18mo) report onward - shown as reported each year, not adjusted for this "
         "change. FY2021's Pillar 3 report contains only qualitative MREL narrative (no numeric MREL disclosure of "
         "any kind), consistent with the UK KM2 MREL template not yet being in use for CB Group Consolidated that "
         "year. FY2019 and FY2020 numeric MREL figures are from the Annual Report's own 'Minimum requirement for "
         "own funds and eligible liabilities (MREL)' table (Risk Report) - the Bank of England's MREL policy and "
         "phased implementation only began applying case-by-case from 2016 onward (BRRD requirement), with the "
         "Bank's first numeric MREL disclosure appearing in the FY2019/FY2020 Annual Reports; FY2014-FY2018 "
         "Annual Reports discuss MREL only narratively (e.g. 'progression towards meeting the BoE's MREL by 2022'), "
         "with no numeric ratio disclosed.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2026": 91020, "FY2025": 89876, "FY2023": 91884, "FY2022": 92010, "FY2021": 89216, "FY2020": 90307, "FY2019": 91101, "FY2018": 43583, "FY2017": 43314, "FY2016": 39963, "FY2015": 38701, "FY2014": 37083}),
        ("Loans and advances to customers (amortised cost)", {"FY2026": 69060, "FY2025": 71072, "FY2023": 72191, "FY2022": 71749, "FY2021": 71874, "FY2020": 72428, "FY2019": 73093, "FY2018": 32744, "FY2017": 31293, "FY2016": 29202, "FY2015": 27482, "FY2014": 25901}),
        ("Customer deposits", {"FY2026": 72711, "FY2025": 70383, "FY2023": 66827, "FY2022": 65434, "FY2021": 66971, "FY2020": 67710, "FY2019": 64000, "FY2018": 28904, "FY2017": 27718, "FY2016": 27090, "FY2015": 26407, "FY2014": 24073}),
        ("Total equity", {"FY2026": 5582, "FY2025": 5609, "FY2023": 5689, "FY2022": 6411, "FY2021": 5582, "FY2020": 4990, "FY2019": 5141, "FY2018": 3291, "FY2017": 3464, "FY2016": 3221, "FY2015": 3458, "FY2014": 2505}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total income", {"FY2026": 1833, "FY2025": 2741, "FY2023": 1826, "FY2022": 1711, "FY2021": 1487, "FY2020": 1435, "FY2019": 1773, "FY2018": 1011, "FY2017": 1037, "FY2016": 998, "FY2015": 1004, "FY2014": 963}),
        ("Operating and administrative expenses", {"FY2026": -1462, "FY2025": -2126, "FY2023": -1173, "FY2022": -1069, "FY2021": -1202, "FY2020": -1101, "FY2019": -1703, "FY2018": -1246, "FY2017": -1250, "FY2016": -1311, "FY2015": -1234, "FY2014": -1105}),
        ("Profit for the period/year", {"FY2026": 150, "FY2025": 150, "FY2023": 249, "FY2022": 520, "FY2021": 532, "FY2020": -191, "FY2019": -139, "FY2018": -239, "FY2017": -294, "FY2016": -558, "FY2015": -249, "FY2014": -178}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2026": 5583, "FY2025": 5334, "FY2023": 6411, "FY2022": 5582, "FY2021": 4990, "FY2020": 5141, "FY2019": 3291, "FY2018": 3464, "FY2017": 3221, "FY2016": 3458, "FY2015": 2505, "FY2014": 2410}),
        ("Total comprehensive income/(losses) for the period/year", {"FY2026": 37, "FY2025": -343, "FY2023": -346, "FY2022": 1297, "FY2021": 674, "FY2020": -62, "FY2019": -60, "FY2018": -282, "FY2017": -263, "FY2016": -597, "FY2015": -271, "FY2014": -191}),
        ("Other equity movements, net", {"FY2026": -38, "FY2025": 618, "FY2023": -376, "FY2022": -468, "FY2021": -82, "FY2020": -89, "FY2019": 1910, "FY2018": 109, "FY2017": 506, "FY2016": 360, "FY2015": 1224, "FY2014": 286}),
        ("Closing equity", {"FY2026": 5582, "FY2025": 5609, "FY2023": 5689, "FY2022": 6411, "FY2021": 5582, "FY2020": 4990, "FY2019": 5141, "FY2018": 3291, "FY2017": 3464, "FY2016": 3221, "FY2015": 3458, "FY2014": 2505}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": -1221, "FY2023": 948, "FY2022": 1930, "FY2021": 582, "FY2020": 2403, "FY2019": 699, "FY2018": -1644, "FY2017": -720, "FY2016": -782, "FY2015": -24, "FY2014": -629}),
        ("Net cash from/(used in) investing activities", {"FY2025": 30, "FY2023": -869, "FY2022": -1368, "FY2021": 465, "FY2020": -737, "FY2019": 3396, "FY2018": 329, "FY2017": -550, "FY2016": -293, "FY2015": -259, "FY2014": -168}),
        ("Net cash from/(used in) financing activities", {"FY2025": 898, "FY2023": -1023, "FY2022": 1796, "FY2021": -608, "FY2020": -2983, "FY2019": -517, "FY2018": 905, "FY2017": 2272, "FY2016": 688, "FY2015": 740, "FY2014": 132}),
        ("Cash and cash equivalents at end of period/year", {"FY2025": 10296, "FY2023": 11667, "FY2022": 12611, "FY2021": 10253, "FY2020": 9814, "FY2019": 10120, "FY2018": 6542, "FY2017": 6952, "FY2016": 5950, "FY2015": 6337, "FY2014": 5880}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2026": "14.3%", "FY2025": "14.2%", "FY2023": "14.6%", "FY2022": "14.9%", "FY2021": "14.9%", "FY2020": "14.4%", "FY2019": "14.4%", "FY2018": "10.7%", "FY2017": "12.2%", "FY2016": "12.6%", "FY2015": "13.3%", "FY2014": "12.1%"}),
        ("Tier 1 Ratio", {"FY2026": "16.6%", "FY2025": "16.7%", "FY2023": "17.0%", "FY2022": "17.7%", "FY2021": "17.7%", "FY2020": "17.1%", "FY2019": "17.2%", "FY2018": "12.8%", "FY2017": "14.3%", "FY2016": "14.8%", "FY2015": "15.8%", "FY2014": "12.1%"}),
        ("Total Capital Ratio", {"FY2026": "19.3%", "FY2025": "19.4%", "FY2023": "21.1%", "FY2022": "21.9%", "FY2021": "21.9%", "FY2020": "20.2%", "FY2019": "20.2%", "FY2018": "15.9%", "FY2017": "17.4%", "FY2016": "18.1%", "FY2015": "19.1%", "FY2014": "18.6%"}),
        ("Leverage Ratio", {"FY2026": "6.3%", "FY2025": "5.5%", "FY2023": "4.9%", "FY2022": "5.1%", "FY2021": "5.1%", "FY2020": "4.8%", "FY2019": "4.4%", "FY2018": "5.6%", "FY2017": "6.2%", "FY2016": "6.8%", "FY2015": "7.2%", "FY2014": "5.7%"}),
        ("LCR", {"FY2026": "164%", "FY2025": "158%", "FY2023": "146%", "FY2022": "140%", "FY2020": "140%", "FY2019": "152%", "FY2018": "137%", "FY2017": "164%", "FY2016": "140%", "FY2015": "136%", "FY2014": "110%"}),
        ("NSFR", {"FY2026": "143%", "FY2025": "142%", "FY2023": "136%", "FY2022": "136%", "FY2021": "134%", "FY2020": "131%", "FY2019": "128%", "FY2018": "125%", "FY2017": "118%", "FY2016": "124%", "FY2015": "120%", "FY2014": "108%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. FY2026 cash flow is blank because the FY2026 Annual Report "
         "took the FRS 101/IAS 7 cash-flow-statement exemption (see Cash Flow Statement sheet note) following the "
         "Part VII transfer of substantially all of the Bank's business to Nationwide on 2 April 2026; Pillar 3 "
         "disclosures were unaffected and continue for FY2026. Balance Sheet/P&L/Equity figures are CB Group "
         "consolidated through FY2025 and Bank (Company)-solo for FY2026 - a genuine entity-basis change since the "
         "FY2026 Annual Report no longer prepares consolidated financial statements (see the Balance Sheet sheet's "
         "basis note); FY2025's equity roll-forward also includes an explicit restatement plug (aligning to "
         "Nationwide's accounting policies) that is not reflected in the FY2023 column, since that column uses "
         "FY2023's own originally-published closing balance. HD-047 (2026-09-05) extended the workbook back to "
         "FY2014 (capped project-wide - see wayfinder/historical-depth/tickets/HD-047.md); FY2014's cash flow "
         "'Opening equity' of £2,410m is Sep-2013's closing balance, one year before this workbook's own FY2014 "
         "column, shown for roll-forward continuity only.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/CLYDESDALE FINANCIALS.xlsx")
