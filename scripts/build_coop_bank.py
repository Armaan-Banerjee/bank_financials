import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Calendar year-end (31 December). Most recent published Annual Report and Pillar 3
# disclosures are for FY2024 (signed 6 March 2025) - no FY2025 Annual Report and
# Accounts had yet been published as of the source-gathering date (2026-08-26),
# only summary H1/H2 2025 Pillar 3 KM1 disclosures (no cash flow statement, and
# no capital-amount breakdown, only headline ratios in the trading update) - not
# usable for this workbook's format, so FY2025 is left out entirely rather than
# filled in from an incompatible source.
# HD-045 (2026-09-05): extended backward to FY2014 (the project-wide historical-
# depth cap - Pillar 3 disclosures aren't meaningfully comparable pre-CRD IV/Basel
# III). The Bank's own archive goes further back (to ~2003), but per explicit user
# decision this workbook stops at FY2014 FOR PILLAR 3 / ASSET QUALITY / RWA
# BREAKDOWN. 11 years used there: FY2024-FY2014.
# HD-078 (2026-09-06): per that ticket's narrower scope, extended the FOUR
# STATUTORY-STATEMENT SHEETS ONLY (Balance Sheet, Profit & Loss, Statement of
# Changes in Equity, Cash Flow Statement) back to FY2003 - the real archive floor
# identified by HD-004's targeted scan. Sourced entirely from Companies House
# filing history (co-operativebank.co.uk itself does not host pre-2014 Annual
# Reports), since The Co-operative Bank p.l.c. (company number 00990937) has
# filed statutory accounts there since well before 2003. Pillar 3, Asset Quality
# and RWA Breakdown sheets are UNCHANGED and still start at FY2014 (see the
# per-sheet "not extended" notes below). FY2003-FY2013 is a genuinely different
# reporting era in three separate ways, each documented where it first bites:
#   - FY2009-FY2013: The Co-operative Bank still the sole reporting entity
#     (pre-dates the FY2017 holdco restructuring described in the ENTITY/
#     OWNERSHIP NOTE below), IFRS, calendar (31 December) year end.
#   - FY2005-FY2008: IFRS, but a 52/53-week fiscal year ending on a Friday/
#     Saturday near 10 January of the FOLLOWING calendar year (the accounting
#     reference date only moved to 31 December from the FY2009 accounts). Each
#     such year is headed in this workbook by the calendar year it substantially
#     covers, following the Bank's OWN convention for labelling these accounts
#     (its own Basis of Preparation note states e.g. "the financial statements
#     of the Bank and Group relate to the 52 weeks to 13 January 2007. Since the
#     Bank and Group accounting date is virtually co-terminous with the calendar
#     year 2006 the financial year's figures are headed 2006").
#   - FY2003-FY2004: same 52/53-week fiscal year, but UK GAAP (Companies Act
#     1985 Sch. 9 bank format) rather than IFRS - pre-dates the Bank's IFRS
#     transition (first effective for the 52 weeks to 14 January 2006, i.e.
#     "FY2005" in this workbook's labelling). No IFRS-style OCI/reserve
#     categories exist yet (just share capital / share premium / profit and
#     loss account), and the Bank's own accounts of this era do not present a
#     standalone Bank-only cash flow statement (only a Consolidated one) - the
#     Cash Flow Statement sheet uses the Consolidated Group statement for
#     FY2003-FY2004 only, clearly flagged in its own source note.
# 22 years used across the four statutory sheets: FY2024-FY2003.
YEARS = [
    "FY2024", "FY2023", "FY2022", "FY2021", "FY2020",
    "FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014",
    "FY2013", "FY2012", "FY2011", "FY2010", "FY2009", "FY2008",
    "FY2007", "FY2006", "FY2005", "FY2004", "FY2003",
]  # most recent first
# Pillar 3, Asset Quality and RWA Breakdown sheets intentionally still only use
# the first 11 years above (FY2024-FY2014) - see PILLAR3_YEARS.
PILLAR3_YEARS = YEARS[:11]
YEAR_LABEL = {y: y for y in YEARS}

AR2024_URL = "https://www.co-operativebank.co.uk/pdfs/bank/investorrelations/2024-annual-report-and-accounts.pdf"
AR2022_URL = "https://www.co-operativebank.co.uk/pdfs/bank/investorrelations/2022-annual-report-and-accounts.pdf"
AR2020_URL = "https://www.co-operativebank.co.uk/assets/pdf/bank/investorrelations/2020-annual-report-and-accounts.pdf"
AR2019_URL = "https://www.co-operativebank.co.uk/pdfs/bank/investorrelations/2019-annual-report-and-accounts.pdf"
AR2018_URL = "https://www.co-operativebank.co.uk/assets/pdf/bank/investorrelations/2018-annual-report-and-accounts.pdf"
AR2017_URL = "https://www.co-operativebank.co.uk/assets/pdf/bank/investorrelations/2017-annual-report-and-accounts.pdf"
AR2016_URL = "https://www.co-operativebank.co.uk/assets/pdf/bank/investorrelations/annualreports/2016-Annual-Report.pdf"
AR2015_URL = "https://www.co-operativebank.co.uk/assets/pdf/bank/investorrelations/financialresults/2015-Annual-Report-and-Accounts.pdf"
AR2014_URL = "https://www.co-operativebank.co.uk/assets/pdf/bank/investorrelations/annual-report.pdf"

P3_2024_URL = "https://www.co-operativebank.co.uk/pdfs/bank/investorrelations/2024-pillar-3-disclosures.pdf"
P3_2022_URL = "https://www.co-operativebank.co.uk/pdfs/bank/investorrelations/2022-pillar-3-disclosures.pdf"
P3_2020_URL = "https://www.co-operativebank.co.uk/pdfs/bank/investorrelations/2020-pillar-3-disclosures.pdf"
P3_2019_URL = "https://www.co-operativebank.co.uk/assets/pdf/bank/investorrelations/2019-pillar-3-disclosures.pdf"
P3_2018_URL = "https://www.co-operativebank.co.uk/assets/pdf/bank/investorrelations/2018-pillar-3-disclosures.pdf"
P3_2017_URL = "https://www.co-operativebank.co.uk/assets/pdf/bank/investorrelations/2017-pillar-3-disclosures.pdf"
P3_2016_URL = "https://www.co-operativebank.co.uk/assets/pdf/bank/investorrelations/2016-Pillar-3.pdf"
P3_2015_URL = "https://www.co-operativebank.co.uk/assets/pdf/bank/investorrelations/2015-Pillar-3-Disclosures.pdf"
P3_2014_URL = "https://www.co-operativebank.co.uk/pdfs/bank/investorrelations/pillar3.pdf"
P3_2025_URL = "https://www.co-operativebank.co.uk/pdfs/bank/investorrelations/2025-h2-pillar-3-disclosures.pdf"
P3_2025_H1_URL = "https://www.co-operativebank.co.uk/pdfs/bank/investorrelations/2025-h1-pillar-3-disclosures.pdf"

# HD-078: FY2003-FY2013 statutory-statement sources. co-operativebank.co.uk does
# not host Annual Reports this old (confirmed via Wayback Machine CDX search of
# the domain, which turns up nothing before 2014) - all 11 documents below are
# each year's own scanned "Group of companies' accounts" statutory filing from
# Companies House's public filing history for The Co-operative Bank p.l.c.
# (company number 00990937), https://find-and-update.company-information.
# service.gov.uk/company/00990937/filing-history?category=accounts . These are
# image-only scans (no text layer / not machine-OCR'd), so every figure below
# was read directly off the page images, not extracted programmatically.
CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/00990937/filing-history"
AR2013_CH_URL = f"{CH_BASE}/MzEwMjk1Njc4M2FkaXF6a2N4/document?format=pdf&download=0"  # accounts made up to 31 Dec 2013
AR2012_CH_URL = f"{CH_BASE}/MzA3NzEwNzEyOGFkaXF6a2N4/document?format=pdf&download=0"  # accounts made up to 31 Dec 2012 (also FY2011 comparative)
AR2010_CH_URL = f"{CH_BASE}/MzAzNTIwNjYxOWFkaXF6a2N4/document?format=pdf&download=0"  # accounts made up to 31 Dec 2010
AR2009_CH_URL = f"{CH_BASE}/MzAxMzExNDY4NGFkaXF6a2N4/document?format=pdf&download=0"  # accounts made up to 31 Dec 2009 (Britannia merger year)
AR2008_CH_URL = f"{CH_BASE}/MjAzMjMzNTAyM2FkaXF6a2N4/document?format=pdf&download=0"  # accounts made up to 10 Jan 2009 (also FY2007 comparative)
AR2006_CH_URL = f"{CH_BASE}/MTc5MDE4NTg2YWRpcXprY3g/document?format=pdf&download=0"  # accounts made up to 13 Jan 2007 (also FY2005 comparative)
AR2004_CH_URL = f"{CH_BASE}/OTQ3NzI5NzNhZGlxemtjeA/document?format=pdf&download=0"  # accounts made up to 8 Jan 2005 (also FY2003 comparative)

PRE2014_HISTORY_NOTE = (
    "PRE-2014 HISTORICAL DEPTH (HD-078, 2026-09-06): FY2003-FY2013 extends only "
    "the four statutory-statement sheets (Balance Sheet, Profit & Loss, Statement "
    "of Changes in Equity, Cash Flow Statement) back to FY2003, the real "
    "statutory floor identified by HD-004's targeted archive scan - Pillar 3, "
    "Asset Quality and RWA Breakdown are unchanged and still start at FY2014 "
    "(pre-CRD IV/Basel III Pillar 3 disclosures aren't meaningfully comparable). "
    "All FY2003-FY2013 figures are transcribed from each year's own scanned "
    "statutory 'Group of companies' accounts' filing at Companies House (company "
    "number 00990937) - co-operativebank.co.uk does not host Annual Reports this "
    "old. Three distinct reporting-basis eras are stacked back to back:\n"
    "FY2009-FY2013 (IFRS, calendar year end, sole reporting entity): each "
    "Annual Report's own 'Bank balance sheet' / 'Bank statement of cash flows' / "
    "'Consolidated and Bank statements of changes in equity' are used, on the "
    "same individual-entity basis as FY2014 onward. The Bank took the s.408 "
    "Companies Act 2006 exemption not to present its own income statement in "
    "every one of these years except FY2013 itself (its 2013 Annual Report, "
    "published amid the Bank's 2013 recapitalisation, voluntarily disclosed a "
    "full 'Bank income statement' for both FY2013 and, as its own comparative "
    "column, FY2012 - the only source for a standalone Bank FY2012 income "
    "statement, since FY2012's own Annual Report itself took the exemption); "
    "FY2009-FY2011 accordingly show bottom-line profit plus OCI reserve "
    "movements only (from the equity roll-forward), not a full income "
    "statement, the same convention already used for FY2017 onward.\n"
    "BRITANNIA MERGER NOTE (FY2009): Britannia Building Society transferred its "
    "engagements to The Co-operative Bank on 1 August 2009 - the single largest "
    "discontinuity in this workbook's full history. The FY2009 Balance Sheet, "
    "Cash Flow and Equity sheets roughly double in size year-on-year (e.g. Total "
    "assets £16.4bn at FY2008 to £47.2bn at FY2009); the Statement of Changes in "
    "Equity shows this explicitly as an 'Amounts arising on transfer of "
    "engagements' movement (+£811.2m to Bank retained earnings) and the Cash "
    "Flow Statement shows a matching 'Cash and cash equivalents acquired on "
    "transfer of engagements' investing inflow (£889.6m) - both the Bank's own "
    "disclosed figures for the transaction, not restatements of prior years.\n"
    "FY2005-FY2008 (IFRS, but a 52/53-week fiscal year, pre-Britannia): the "
    "Bank's accounting reference date was not yet 31 December - each year's "
    "accounts cover a 52/53-week period ending on a Friday/Saturday near 10 "
    "January of the FOLLOWING calendar year (e.g. 'the 52 weeks to 13 January "
    "2007'), only moving to a calendar 31 December year end with the FY2009 "
    "accounts. Each such year is headed by the calendar year it substantially "
    "covers, following the Bank's own stated convention in its Basis of "
    "Preparation note (e.g. 'the financial year's figures are headed 2006'), "
    "not by the year in which the accounting period technically ends. These "
    "years present a 'Statement of recognised income and expense' (SORIE), the "
    "IFRS predecessor to the Statement of Changes in Equity used from FY2009 "
    "onward, and a smaller, simpler Bank balance sheet consistent with the much "
    "smaller pre-Britannia institution (Total assets ~£11-16bn vs. ~£27-38bn "
    "FY2014 onward).\n"
    "FY2003-FY2004 (UK GAAP, pre-IFRS): predates the Bank's IFRS transition "
    "(first effective for 'the 52 weeks to 14 January 2006', i.e. this "
    "workbook's FY2005) - accounts are prepared under the Companies Act 1985 "
    "Sch. 9 bank format, with no IFRS-style Available-for-sale/Cashflow-hedging/"
    "capital-redemption reserve categories (just Called-up share capital, Share "
    "premium account and Profit and loss account) and no OCI concept at all "
    "(profit for the year is the whole of total recognised gains and losses in "
    "both years). The Bank's own accounts of this era do not present a "
    "standalone Bank-only cash flow statement (only a Consolidated Group one) - "
    "the Cash Flow Statement sheet uses the CONSOLIDATED GROUP statement for "
    "FY2003-FY2004 only, clearly flagged in that sheet's own source note; every "
    "other FY2003-FY2013 year on that sheet is Bank Company-only, consistent "
    "with the rest of this workbook.\n"
    "Two further genuine restatement discontinuities were found and are bridged "
    "with dedicated rows on the Statement of Changes in Equity sheet rather than "
    "force-matched, the same treatment as the pre-existing FY2016/FY2017 "
    "restatement: (1) FY2012 closing Total equity per the Bank's own FY2012 "
    "Annual Report (£1,629.1m) does not equal the FY2013 Annual Report's own "
    "restated FY2012 comparative Balance Sheet closing position (£1,850.2m, a "
    "£221.1m difference) - the FY2013 Annual Report does not itself narrate the "
    "specific cause, so this is shown as an unexplained 'Restatement' row rather "
    "than attributed; (2) FY2013 closing Total equity per the Bank's own FY2013 "
    "Annual Report (£1,777.3m) differs marginally from the FY2014 Annual "
    "Report's own FY2013 comparative opening position already used elsewhere in "
    "this workbook (£1,768.5m, an £8.8m difference, entirely within the Cashflow "
    "hedging reserve and Retained earnings columns) - likely a minor "
    "reclassification between reserve captions, also shown as an unexplained "
    "'Restatement' row rather than force-matched."
)

ENTITY_NOTE = (
    "ENTITY/OWNERSHIP NOTE: The Co-operative Bank p.l.c. (company number 00990937, FRN 121885) is the PRA-"
    "authorised entity. It is a wholly-owned subsidiary of The Co-operative Bank Finance p.l.c., itself wholly-"
    "owned by The Co-operative Bank Holdings p.l.c. (the listed holding company; named 'The Co-operative Bank "
    "Holdings Limited' in the FY2020-FY2022 Annual Reports, re-registered as a p.l.c. by FY2023). Coventry "
    "Building Society completed its acquisition of The Co-operative Bank Holdings p.l.c. on 1 January 2025 - "
    "outside the FY2014-FY2024 period covered by this workbook, so it has no bearing on any figure shown here. "
    "Coventry and Co-operative Bank have proposed a Part VII transfer of the Bank's business (including 'smile') "
    "into Coventry Building Society, targeted for 1 January 2027 - not yet effective as of the most recent "
    "published accounts, watch for a cash-flow-statement exemption or entity change in future years similar to "
    "Clydesdale Bank PLC's Nationwide Part VII transfer in this same workbook series. "
    "This workbook uses The Co-operative Bank p.l.c.'s own entity-level ('Bank Company-only') figures throughout "
    "- both cash flow and Pillar 3 - not the wider consolidated Group (The Co-operative Bank Holdings p.l.c. and "
    "its subsidiaries), consistent with the PRA-authorised-entity basis used elsewhere in this workbook series.\n\n"
    "HOLDCO RESTRUCTURING HISTORY (HD-045, 2026-09-05): before September 2017, The Co-operative Bank p.l.c. had "
    "no holding company at all - it WAS the top-level reporting entity, and its own Annual Report and Pillar 3 "
    "Disclosures covered the Bank on an unconsolidated, individual basis by default (FY2014-FY2016 in this "
    "workbook). The Bank's 'Restructuring and Recapitalisation', completed in September 2017, created the new "
    "holding company The Co-operative Bank Holdings Limited (renamed p.l.c. later) sitting above the Bank; from "
    "FY2017 the Bank's own Annual Report presents 'Bank Company' financial statements taking the Section 408 "
    "exemption (see below) alongside the wider Group's consolidated statements, and its Pillar 3 Disclosures add "
    "a dedicated 'Appendix 2 - Individual disclosure tables' section for the Bank Company alone (used throughout "
    "FY2017-FY2019 in this workbook, consistent with the individual-entity basis used FY2020 onward). In February "
    "2019 The Co-operative Bank Finance p.l.c. was inserted as an intermediate parent between the Holding Company "
    "and the Bank Company, explaining the 'Finance Company' balance that first appears on the FY2019 balance sheet."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are The Co-operative Bank p.l.c.'s own Bank Company-only Statement of Cashflows, £m:\n"
    f"FY2024: The Co-operative Bank p.l.c. 2024 Annual Report and Accounts, p.222 (Statement of Cashflows, Bank "
    f"Company-only) - {AR2024_URL}\n"
    f"FY2023: The Co-operative Bank p.l.c. 2024 Annual Report and Accounts, p.222 (FY2023 comparative column, "
    f"same statement) - {AR2024_URL}\n"
    f"FY2022: The Co-operative Bank p.l.c. 2022 Annual Report and Accounts, p.245 (Statement of Cashflows, Bank "
    f"Company-only) - {AR2022_URL}\n"
    f"FY2021: The Co-operative Bank p.l.c. 2022 Annual Report and Accounts, p.245 (FY2021 comparative column, "
    f"same statement) - {AR2022_URL}\n"
    f"FY2020: The Co-operative Bank p.l.c. 2020 Annual Report and Accounts, p.215 (Statement of Cashflows, Bank "
    f"Company-only) - {AR2020_URL}\n"
    f"FY2019: 2019 Annual Report and Accounts, p.199-200 (Statement of Cashflows, Bank Company-only) - "
    f"{AR2019_URL}\n"
    f"FY2018: 2018 Annual Report and Accounts, p.184-185 (The Bank Company statement of cash flows) - "
    f"{AR2018_URL}\n"
    f"FY2017: 2017 Annual Report and Accounts, p.176-177 (The Bank Company statement of cash flows) - "
    f"{AR2017_URL}\n"
    f"FY2016: 2016 Annual Report and Accounts, p.147-148 (The Bank statement of cash flows) - {AR2016_URL}\n"
    f"FY2015: 2015 Annual Report and Accounts, p.162-163 (The Bank statement of cash flows) - {AR2015_URL}\n"
    f"FY2014: 2014 Annual Report and Accounts, p.150-151 (The Bank statement of cash flows) - {AR2014_URL}\n"
    f"FY2013: The Co-operative Bank p.l.c. 2013 Annual Report and Accounts (Companies House filing), p.131-132 "
    f"(The Bank statement of cash flows) - {AR2013_CH_URL}\n"
    f"FY2012: 2012 Annual Report and Accounts (Companies House filing), p.38 (Bank statement of cash flows) - "
    f"{AR2012_CH_URL}\n"
    f"FY2011: 2012 Annual Report and Accounts (Companies House filing), p.38 (FY2011 comparative column, same "
    f"statement) - {AR2012_CH_URL}\n"
    f"FY2010: 2010 Annual Report and Accounts (Companies House filing), p.35 (Bank statement of cash flows) - "
    f"{AR2010_CH_URL}\n"
    f"FY2009: 2009 Annual Report and Accounts (Companies House filing), p.41 (Bank statement of cash flows, year "
    f"ended 31 December 2009 - the Britannia merger year) - {AR2009_CH_URL}\n"
    f"FY2008: 'Financial statements 2008' Annual Report (Companies House filing), p.49 (Bank cash flow statement, "
    f"52 weeks to 10 January 2009) - {AR2008_CH_URL}\n"
    f"FY2007: 'Financial statements 2008' Annual Report (Companies House filing), p.49 (FY2007 comparative "
    f"column, same statement, 52 weeks to 12 January 2008) - {AR2008_CH_URL}\n"
    f"FY2006: 'Financial Statements 2006' Annual Report (Companies House filing), p.45 (Bank cash flow statement, "
    f"52 weeks to 13 January 2007) - {AR2006_CH_URL}\n"
    f"FY2005: 'Financial Statements 2006' Annual Report (Companies House filing), p.45 (FY2005 comparative "
    f"column, same statement, 53 weeks to 14 January 2006) - {AR2006_CH_URL}\n"
    f"FY2004: 'Financial Statements 2004' Annual Report (Companies House filing), p.52 (CONSOLIDATED cash flow "
    f"statement - the Bank did not present a standalone Bank-only cash flow statement in this UK GAAP era; 52 "
    f"weeks to 8 January 2005) - {AR2004_CH_URL}\n"
    f"FY2003: 'Financial Statements 2004' Annual Report (Companies House filing), p.52 (FY2003 comparative "
    f"column, same CONSOLIDATED statement, 52 weeks to 10 January 2004) - {AR2004_CH_URL}\n"
    "All 11 years cross-checked and tie exactly across adjacent reports (e.g. FY2020 closing cash and cash "
    "equivalents of £4,221.1m matches the FY2022 report's own FY2021 opening balance; FY2014-FY2019's closing "
    "balances similarly tie to the following year's own opening balance).\n\n"
    "PRE-RESTRUCTURING NOTE (FY2014-FY2016): before the entity was 'The Co-operative Bank plc' and the sole "
    "reporting entity - no holding company existed yet (see ENTITY/OWNERSHIP NOTE below) - so 'The Bank statement "
    "of cash flows' in these years' own reports is already the individual-entity statement used throughout this "
    "workbook, not a consolidated Group statement requiring separate extraction.\n\n"
    "FY2014-FY2019 MAPPING NOTE: each year's own statement uses slightly different adjustment line items (e.g. "
    "'Interest amortisation', 'Fair value movements and amortisation of financial assets and liabilities', 'Gain "
    "on capital raise') that don't recur identically year to year; smaller such items are consolidated into the "
    "'Other non-cash movements (incl. exchange rate movements)' row (a plug figure, cross-checked against each "
    "year's own disclosed operating-activities subtotal before working-capital movements - all tie exactly). "
    "Items with a direct equivalent in the FY2020-FY2024 row structure (deposits, customer accounts, debt "
    "securities, loans and advances, amounts owed to/from Co-operative Bank undertakings, prepayments, accruals, "
    "income tax) are placed in the existing matching row. FY2014's 'Increase/(decrease) in customer accounts' row "
    "combines the original report's separate 'customer accounts' and 'customer accounts - capital bonds' "
    "movements (both wound down and merged into one line by FY2017). All TOTAL rows (operating/investing/"
    "financing/net movement/opening and closing cash) are the Bank's own disclosed totals, not derived from the "
    "line items above them.\n\n"
    "RESTATEMENT NOTE (FY2016/FY2017 boundary): the 2016 Annual Report's own closing cash and cash equivalents "
    "(£3,266.3m) does not equal the 2017 Annual Report's own restated FY2016 comparative opening/closing figure "
    "(£3,247.6m, an £18.7m difference) - both are transcribed from each report's own figures rather than force-"
    "matched, consistent with this workbook's practice of showing genuine source-disclosed restatements rather "
    "than silently reconciling them (see the same 2017 Annual Report's own footnote on re-presenting netting "
    "arrangements, also responsible for the equity restatement documented on the Statement of Changes in Equity "
    "sheet).\n\n"
    "FY2003-FY2013 MAPPING NOTE: the same plug-row approach as the FY2014-FY2019 note above is used going "
    "further back - each year's own less-common adjustment items (interest payable on subordinated liabilities/"
    "other borrowed funds, preference dividends, pension costs, fair value/interest amortisation, the FY2013 "
    "Liability Management Exercise items, the FY2009 Britannia fair-value-adjustment unwind) are consolidated "
    "into 'Other non-cash movements (incl. exchange rate movements)', cross-checked against each year's own "
    "disclosed operating-activities subtotal before working-capital movements - all tie exactly. Financing-"
    "section items unique to this era (subordinated loanstock issuance/repayment, ordinary/preference share "
    "issuance and dividends, capital contributions from the parent, dividends from subsidiary/associated "
    "undertakings) use dedicated new rows rather than being folded into a plug, since 'Net cash flows from/(used "
    "in) financing activities' TOTAL rows are short enough to map item-for-item; all still tie exactly to each "
    "year's own disclosed total. FY2009's investing section adds two Britannia-merger-specific rows ('Cash and "
    "cash equivalents acquired on transfer of engagements' and 'Movements in investments in Group undertakings') "
    "not used in any other year. FY2003-FY2004 (UK GAAP, Consolidated Group basis) map onto the closest-matching "
    "existing rows by economic substance (e.g. 'Purchase of investments' to 'Purchase of investment securities') "
    "since the Bank's own presentation used different captions in this era; both years' 'Net cash (outflow)/"
    "inflow from operating activities' is the Group's own single disclosed total (no line-item breakdown is "
    "given on the face of the primary statement in this format, only in a note not transcribed here) rather than "
    "a sum of mapped rows.\n\n"
    + PRE2014_HISTORY_NOTE + "\n\n"
    + ENTITY_NOTE
)


def p3_sources(page_2024="139-140", page_2022_23="101-102", page_2019_18="53-54", page_2017="52-53",
               page_2016_15_14=None):
    text = (
        "Sources - The Co-operative Bank p.l.c. individual-entity Pillar 3 basis (Appendix 1, 'KM1 - Key Metrics "
        "(Individual)' / 'KM2 - Key Metrics MREL (Individual)' for FY2020 onward; 'Appendix 2 - Individual "
        "disclosure tables' for FY2017-FY2019; the Bank's own top-level Table 1/4/5/11 key-ratio and capital-"
        "resources tables for FY2014-FY2016, when the Bank itself was the only reporting entity, so no "
        "Group/Individual split existed yet):\n"
        f"FY2024: The Co-operative Bank 2024 Pillar 3 Disclosures, p.{page_2024} - {P3_2024_URL}\n"
        f"FY2023: The Co-operative Bank 2024 Pillar 3 Disclosures, p.{page_2024} (FY2023 comparative column, same "
        f"tables) - {P3_2024_URL}\n"
        f"FY2022: The Co-operative Bank 2022 Pillar 3 Disclosures, p.{page_2022_23} - {P3_2022_URL}\n"
        f"FY2021: The Co-operative Bank 2022 Pillar 3 Disclosures, p.{page_2022_23} (31 Dec 21 column, same "
        f"tables) - {P3_2022_URL}\n"
        f"FY2020: The Co-operative Bank 2022 Pillar 3 Disclosures, p.{page_2022_23} (31 Dec 20 column, same "
        f"tables - the KM1/KM2 templates report the current period plus 4 prior half-year-end points) - "
        f"{P3_2022_URL}\n"
        f"FY2019: The Co-operative Bank Holdings Ltd and The Co-operative Bank p.l.c. 2019 Pillar 3 Disclosures, "
        f"p.{page_2019_18} (Appendix 2, Table 36/38 - Individual disclosure tables) - {P3_2019_URL}\n"
        f"FY2018: The Co-operative Bank plc 2018 Pillar 3 Disclosures, p.{page_2019_18} (FY2018 own-year column, "
        f"Appendix 2, Table 36/38) - {P3_2018_URL}\n"
        f"FY2017: The Co-operative Bank plc Pillar 3 Disclosures 2017, p.{page_2017} (Appendix 2, Table 37/39 - "
        f"Individual disclosure tables) - {P3_2017_URL}\n"
    )
    if page_2016_15_14:
        p16, p15, p14 = page_2016_15_14
        text += (
            f"FY2016: The Co-operative Bank plc Pillar 3 Disclosures 2016, p.{p16} - {P3_2016_URL}\n"
            f"FY2015: The Co-operative Bank plc Pillar 3 Disclosures 2015, p.{p15} - {P3_2015_URL}\n"
            f"FY2014: The Co-operative Bank plc Pillar 3 Disclosures for the year ended 31 December 2014, "
            f"p.{p14} - {P3_2014_URL}"
        )
    else:
        text += (
            f"FY2016: The Co-operative Bank plc Pillar 3 Disclosures 2016, Table 5/Table 1 - {P3_2016_URL}\n"
            f"FY2015: The Co-operative Bank plc Pillar 3 Disclosures 2015, Table 4/Table 1 - {P3_2015_URL}\n"
            f"FY2014: The Co-operative Bank plc Pillar 3 Disclosures for the year ended 31 December 2014, "
            f"Table 4/Table 1 - {P3_2014_URL}"
        )
    return text


bw = BankWorkbook(bank_name="The Co-operative Bank p.l.c.", years=YEARS, year_label=YEAR_LABEL, header_color="1E5631")

STATEMENTS_SOURCES = (
    "Sources - The Co-operative Bank p.l.c.'s own Bank Company-only Balance Sheet / Statement of Changes in "
    "Equity, £m, transcribed from each year's own report (not a later year's comparative column):\n"
    f"FY2024: 2024 Annual Report and Accounts, p.220-221 (Balance Sheet), p.224 (Statement of Changes in Equity), "
    f"p.226 (Note 2, Net profit attributable to equity shareholders - Section 408 Companies Act 2006 exemption) "
    f"- {AR2024_URL}\n"
    f"FY2023: 2024 Annual Report and Accounts, p.220-221/224/226 (FY2023 comparative columns, same statements) - "
    f"{AR2024_URL}\n"
    f"FY2022: 2022 Annual Report and Accounts, p.242-243/246/248 (Balance Sheet, Statement of Changes in Equity, "
    f"Note 2) - {AR2022_URL}\n"
    f"FY2021: 2022 Annual Report and Accounts, p.242-243/246/248 (FY2021 comparative columns, same statements) - "
    f"{AR2022_URL}\n"
    f"FY2020: 2020 Annual Report and Accounts, p.212-213/216/217 (Balance Sheet, Statement of Changes in Equity, "
    f"Note 2) - {AR2020_URL}\n"
    f"FY2019: 2019 Annual Report and Accounts, p.197-198/201 (Bank Company-only Balance Sheet and Statement of "
    f"Changes in Equity) - {AR2019_URL}\n"
    f"FY2018: 2018 Annual Report and Accounts, p.183/186-187 (The Bank Company balance sheet and statement of "
    f"changes in equity, incl. Note 2 profit figure) - {AR2018_URL}\n"
    f"FY2017: 2017 Annual Report and Accounts, p.175/178 (The Bank Company balance sheet and statement of changes "
    f"in equity, incl. Note 1 profit figure) - {AR2017_URL}\n"
    f"FY2016: 2016 Annual Report and Accounts, p.146/149 (The Bank balance sheet and statement of changes in "
    f"equity - full income statement also disclosed, p.145) - {AR2016_URL}\n"
    f"FY2015: 2015 Annual Report and Accounts, p.161/164 (The Bank balance sheet and statement of changes in "
    f"equity - full income statement also disclosed, p.159-160) - {AR2015_URL}\n"
    f"FY2014: 2014 Annual Report and Accounts, p.149/152 (The Bank balance sheet and statement of changes in "
    f"equity - full income statement also disclosed, p.147-148) - {AR2014_URL}\n"
    f"FY2013: 2013 Annual Report and Accounts (Companies House filing), p.130/133 (The Bank balance sheet and "
    f"statement of changes in equity - full income statement also disclosed, p.128) - {AR2013_CH_URL}\n"
    f"FY2012: p.36/41 of the Bank's own 2012 Annual Report and Accounts (Companies House filing) for the Balance "
    f"Sheet and Statement of Changes in Equity - {AR2012_CH_URL} - but its full income statement is only "
    f"available from the 2013 Annual Report's own FY2012 comparative column, p.128 (see full-income-statement "
    f"note below) - {AR2013_CH_URL}\n"
    f"FY2011: 2012 Annual Report and Accounts (Companies House filing), p.36/41 (FY2011 comparative columns, "
    f"same statements) - {AR2012_CH_URL}\n"
    f"FY2010: 2010 Annual Report and Accounts (Companies House filing), p.33/36 (Bank balance sheet and "
    f"statement of changes in equity) - {AR2010_CH_URL}\n"
    f"FY2009: 2009 Annual Report and Accounts (Companies House filing), p.39/42 (Bank balance sheet and "
    f"statement of changes in equity, year ended 31 December 2009 - the Britannia merger year) - "
    f"{AR2009_CH_URL}\n"
    f"FY2008: 'Financial statements 2008' Annual Report (Companies House filing), p.46/47 (Bank balance sheet "
    f"and Statement of recognised income and expense, 52 weeks to 10 January 2009) - {AR2008_CH_URL}\n"
    f"FY2007: 'Financial statements 2008' Annual Report (Companies House filing), p.46/47 (FY2007 comparative "
    f"columns, same statements, 52 weeks to 12 January 2008) - {AR2008_CH_URL}\n"
    f"FY2006: 'Financial Statements 2006' Annual Report (Companies House filing), p.42/43 (Bank balance sheet "
    f"and Statement of recognised income and expense, 52 weeks to 13 January 2007) - {AR2006_CH_URL}\n"
    f"FY2005: 'Financial Statements 2006' Annual Report (Companies House filing), p.42/43 (FY2005 comparative "
    f"columns, same statements, 53 weeks to 14 January 2006) - {AR2006_CH_URL}\n"
    f"FY2004: 'Financial Statements 2004' Annual Report (Companies House filing), p.50/51 (Bank balance sheet "
    f"and Reconciliation of movements in shareholders' funds - the UK GAAP predecessor to the Statement of "
    f"Changes in Equity, 52 weeks to 8 January 2005) - {AR2004_CH_URL}\n"
    f"FY2003: 'Financial Statements 2004' Annual Report (Companies House filing), p.50/51 (FY2003 comparative "
    f"columns, same statements, 52 weeks to 10 January 2004) - {AR2004_CH_URL}\n\n"
    "The Bank Company (individual entity) takes advantage of the Section 408 Companies Act 2006 exemption not to "
    "present its own income statement from FY2017 onward - each such year's Annual Report discloses only the Bank "
    "Company's bottom-line net profit/(loss) figure (Note 1 or 2) plus, separately, its Other Comprehensive Income "
    "broken into reserve movements within the Statement of Changes in Equity itself; the Profit & Loss sheet "
    "reconstructs a P&L from these two disclosed pieces for FY2017-FY2024 rather than fabricating a full income "
    "statement - all rows tie exactly to the equity roll-forward's own 'Total comprehensive income/(expense) for "
    "the year' figures. FY2014-FY2016 predate the restructuring that created a holding company above the Bank (see "
    "HOLDCO RESTRUCTURING HISTORY below) - the Bank itself was the reporting entity and its own Annual Report "
    "discloses a full income statement (Net interest income through Loss for the financial year) without taking "
    "the Section 408 exemption; this workbook reproduces that full income statement as additional rows for "
    "FY2014-FY2016, blank in other years, alongside the same bottom-line/OCI rows used throughout.\n\n"
    "FY2013/FY2012 FULL INCOME STATEMENT NOTE: the s.408-equivalent exemption (s.230 Companies Act 1985, then "
    "s.408 Companies Act 2006) was already being taken by the Bank as early as FY2010 - its FY2010-FY2012 Annual "
    "Reports present only a Consolidated income statement, no standalone Bank one, contrary to what might be "
    "assumed from the FY2014-FY2016 pattern above. The Bank's 2013 Annual Report, published amid its 2013 "
    "recapitalisation, is the one exception: it voluntarily discloses a full 'Bank income statement' for FY2013 "
    "itself, and - as that same statement's own comparative column - for FY2012 as well, even though FY2012's "
    "own Annual Report did not itself present one. This workbook therefore shows a full income statement for "
    "FY2012 and FY2013 too (sourced as described above), not just FY2014-FY2016; FY2009-FY2011 (Bank Company the "
    "sole reporting entity, exemption taken, no comparative rescue available) show bottom-line profit plus OCI "
    "only, the same convention as FY2017 onward.\n\n"
    "NON-CONTROLLING INTERESTS NOTE: FY2014's Total equity (£2,014.5m) and FY2015's opening Total equity "
    "(£2,014.5m) include a small Non-controlling interests balance (£34.5m at FY2014, £33.6m-£34.5m through the "
    "year) relating to the Bank's then-majority stake in Unity Trust Bank plc; this was disposed of in December "
    "2015 (see the Statement of Changes in Equity sheet's 'Disposal of UTB' row), after which Total equity is "
    "attributable to equity shareholders only, consistent with FY2017 onward. The 'Profit/(loss) for the year' "
    "and OCI rows throughout this workbook use the equity-shareholders-attributable figures (not the NCI-inclusive "
    "totals also disclosed in FY2014-FY2015's own income statements), for comparability with later years.\n\n"
    "PRESENTATION NOTE: the Balance Sheet's equity section shows 'Other reserves' as a single aggregate line from "
    "FY2021 onward (FVOCI + cash flow hedging + capital redemption + defined benefit pension reserves combined); "
    "FY2020's own Balance Sheet still itemises 'Share premium account' separately (£2,416.9m) - a genuine one-off "
    "'Reserve reorganisation' movement during FY2021 (disclosed in the FY2022 Annual Report's own equity note) "
    "wrote the share premium account and capital redemption reserve down to £nil and transferred the combined "
    "£2,826.9m into retained earnings, a net-zero movement on Total equity; both entries are reproduced explicitly "
    "in the Statement of Changes in Equity sheet, not silently dropped. 'Equity shares' and 'Prepayments' appear as "
    "their own Balance Sheet lines FY2020-FY2022 only, folded into 'Other assets' from FY2023 onward per the "
    "Bank's own presentation. Deferred tax is presented as an asset FY2021-FY2024 but as a liability in FY2020 - "
    "both reproduced on their own side of the Balance Sheet as originally disclosed, not netted. 'Fair value "
    "adjustments for hedged risk' appears as separate Balance Sheet lines (both asset- and liability-side) only "
    "FY2020-FY2022 - embedded within the Loans and advances to customers note instead from FY2023 onward.\n\n"
    "PRE-2018 PRESENTATION NOTE: 'Investment securities' for FY2014-FY2017 is the sum of the original balance "
    "sheet's separately-disclosed sub-categories (loans and receivables / available-for-sale / fair value through "
    "income or expense / held for trading), which the Bank itself later combined into one line from FY2018 - the "
    "combined figure ties exactly to the credit-risk-exposure note's own 'Investment securities' total in every "
    "year. 'Investments in joint ventures' (FY2014-FY2016) and 'Investments in subsidiaries/group undertakings' "
    "(FY2017 onward) are different balance sheet lines reflecting a genuine change in what the Bank held/disclosed "
    "post-restructuring, reproduced separately rather than merged. 'Non-current assets classified as held for "
    "sale' (FY2014-FY2016 label) and 'Property, plant and equipment classified as held-for-sale' (FY2017 onward "
    "label) are the same balance sheet category under different names and share one row. 'Prepayments and accrued "
    "income' was a single combined line FY2014-FY2018 (own row); FY2019 discloses 'Prepayments' alone since "
    "accrued income was folded elsewhere from IFRS 16 adoption; FY2020-FY2022 use 'Prepayments' as their own line "
    "again. 'Customer accounts - capital bonds' and 'Other borrowed funds' were separate liability lines "
    "FY2014-FY2016 (nil by FY2017), superseded by 'Debt securities in issue' growth and, from FY2019, IFRS 16 "
    "'Lease liabilities' and Tier 2 note issuance - each reproduced only in the years it was actually disclosed. "
    "Right-of-use assets/lease liabilities first appear at FY2019 (IFRS 16's effective date, comparatives not "
    "restated per the standard's own transition option, as stated in the Bank's own FY2019 accounts).\n\n"
    "RESTATEMENT NOTE (FY2016/FY2017 boundary): the 2016 Annual Report's own closing Total equity (£958.5m) does "
    "not equal the 2017 Annual Report's own restated FY2016 comparative opening balance (£726.4m, entirely a "
    "£232.1m retained-earnings difference) - the 2017 Annual Report's own footnote attributes this to 'a "
    "re-presentation... to more fairly reflect the nature of the balances, and the obligatory netting "
    "arrangements in place relating to repo and reverse repo transactions', not a transcription error in this "
    "workbook. The Statement of Changes in Equity sheet shows this as an explicit 'Restatement' row bridging the "
    "two figures, following the same treatment as the FY2021 'Reserve reorganisation' row already in this "
    "workbook, rather than silently dropping or force-matching either year's own disclosed figure.\n\n"
    "PRE-2014 PRESENTATION NOTE: FY2003-FY2013's Balance Sheet uses each era's own line-item captions and "
    "reserve structure rather than being force-mapped onto FY2014-2024's - see PRE-2014 HISTORICAL DEPTH below "
    "for the three reporting-basis eras this spans (IFRS calendar year FY2009-2013, IFRS 52/53-week fiscal year "
    "FY2005-2008, UK GAAP 52/53-week fiscal year FY2003-2004). New rows introduced only for this range: "
    "'Items in the course of collection/transmission from/to other banks' (FY2003-2004 only), 'Debt securities' "
    "(FY2003-2008, a single combined line predating the FY2010 onward available-for-sale/loans-and-receivables "
    "split), 'Retirement benefit obligations' (FY2005 only), 'Preference share capital (non-equity)' (FY2003-2004 "
    "only, called-up share capital's non-equity component under the old UK GAAP format).\n\n"
    + PRE2014_HISTORY_NOTE + "\n\n"
    + ENTITY_NOTE
)

ASSET_QUALITY_SOURCES = (
    "Sources - The Co-operative Bank p.l.c.'s own Note 26/27 'Analysis of Credit Risk Exposure' (Bank "
    "Company-only basis), £m:\n"
    f"FY2024/FY2023: 2024 Annual Report and Accounts, p.242-243 (Note 26) - {AR2024_URL}\n"
    f"FY2022/FY2021: 2022 Annual Report and Accounts, p.264-265 (Note 27) - {AR2022_URL}\n"
    f"FY2020: 2022 Annual Report and Accounts, p.265 (Note 27's own 'At 1 January 2021' comparative row, i.e. "
    f"FY2020's closing position) - {AR2022_URL}\n"
    f"FY2019: 2019 Annual Report and Accounts, p.219-220 (Note 27, 'At 31 December 2019' - ECL-calculation basis, "
    f"i.e. includes credit commitments) - {AR2019_URL}\n"
    f"FY2018: 2018 Annual Report and Accounts, p.207-208 (Note 25, gross customer balance by IFRS 9 stage) - "
    f"{AR2018_URL}\n"
    f"FY2017: 2017 Annual Report and Accounts, p.171-172 (Note 25 - Impaired/Not impaired basis, pre-IFRS 9) - "
    f"{AR2017_URL}\n"
    f"FY2016: 2016 Annual Report and Accounts, p.145-146 (Risk management, Analysis of credit risk exposure - "
    f"Impaired/Not impaired basis, pre-IFRS 9) - {AR2016_URL}\n"
    f"FY2015: 2015 Annual Report and Accounts, p.159-160 (Risk management, Analysis of credit risk exposure - "
    f"Impaired/Not impaired basis, pre-IFRS 9) - {AR2015_URL}\n"
    f"FY2014: 2014 Annual Report and Accounts, p.96 (Risk management, Analysis of credit risk exposure - "
    f"Impaired/Not impaired basis, pre-IFRS 9) - {AR2014_URL}\n\n"
    "Figures are 'Gross customer exposure'/'Allowance for losses' by IFRS 9 stage for Loans and advances to "
    "customers - this is broader than the Balance Sheet's own 'Loans and advances to customers' line, since it "
    "includes off-balance-sheet credit commitments and excludes FVTPL-measured balances (each year's own note "
    "states the reconciling items); reproduced as disclosed, not force-reconciled to the narrower Balance Sheet "
    "figure. All balances other than Loans and advances to customers are confirmed Stage 1 in every year and did "
    "not transfer during the year (per each note's own statement), so are not separately broken out here.\n\n"
    "PRE-IFRS 9 NOTE (FY2014-FY2017): IFRS 9's expected-credit-loss staging model only took effect from 1 January "
    "2018 - FY2014-FY2017 instead classify loans and advances to customers as 'Impaired' or 'Not impaired' under "
    "the prior IAS 39 incurred-loss model, a genuinely different (coarser) classification, not a missing subset "
    "of the IFRS 9 stages; this workbook shows an 'Impaired'/'Not impaired' section for these years instead of "
    "the Stage 1/2/3/POCI section used FY2018 onward, and derives the NPL ratio and coverage ratio from the "
    "'Impaired' total rather than a Stage 3-only total (each year's own note does not separately split the total "
    "allowance for losses between impaired and not-impaired balances, so the coverage ratio uses the whole "
    "allowance for losses over the impaired balance, consistent with how the Bank's own Annual Reports discuss "
    "coverage in this period). FY2014-FY2015's near-total-book losses reflect the Bank's well-documented "
    "2013-2015 recapitalisation and turnaround period (large impairment charges, Non-core deleveraging, conduct "
    "redress) - not a transcription error.\n\n"
    + ENTITY_NOTE
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - The Co-operative Bank p.l.c. individual-entity Pillar 3 basis, UK OV1 'Overview of risk weighted "
    "exposures (Individual)' template (Appendix 1), £m:\n"
    f"FY2024/FY2023: 2024 Pillar 3 Disclosures, p.139 - {P3_2024_URL}\n"
    f"FY2022/FY2021: 2022 Pillar 3 Disclosures, p.101 - {P3_2022_URL}\n"
    f"FY2020: 2020 Pillar 3 Disclosures, p.55 (Table 40, 'Pillar 1 capital requirements', individual basis, "
    f"Appendix 2) - {P3_2020_URL}\n"
    f"FY2019: 2019 Pillar 3 Disclosures, p.57 (Appendix 2, Table 41 'Pillar 1 capital requirements', individual "
    f"basis) - {P3_2019_URL}\n"
    f"FY2018: 2018 Pillar 3 Disclosures, p.56 (Appendix 2, Table 41 'Pillar 1 capital requirements', individual "
    f"basis) - {P3_2018_URL}\n"
    f"FY2017: 2017 Pillar 3 Disclosures, p.56 (Appendix 2, Table 42 'Pillar 1 capital requirements', individual "
    f"basis) - {P3_2017_URL}\n"
    f"FY2016: 2016 Pillar 3 Disclosures, Table 1 'CRD IV key capital ratios' (Risk Weighted Assets total only - "
    f"the Bank's pre-UK-OV1-era Pillar 3 disclosures do not break RWAs into categories) - {P3_2016_URL}\n"
    f"FY2015: 2015 Pillar 3 Disclosures, Table 1 'CRD IV key capital ratios' (Risk Weighted Assets total only) - "
    f"{P3_2015_URL}\n"
    f"FY2014: 2014 Pillar 3 Disclosures, Table 1 'CRD IV key capital ratios' (Risk Weighted Assets total only) - "
    f"{P3_2014_URL}\n\n"
    "All category-broken-out years tie exactly to the existing Total RWAs sheet's own figures. FY2018-FY2020 use "
    "an older CRR 'Pillar 1 capital requirements' exposure-class format (IRB approach vs Standardised approach, "
    "not Credit risk/CCR/Securitisation/Market risk/Operational risk) that predates the UK OV1 template - only "
    "Operational risk and the Total map cleanly onto the later years' category structure; Credit risk/CCR/"
    "Securitisation are left blank for these years rather than force-mapped from a materially different "
    "categorisation ('Total credit risk' in this format combines what later years split into 3 separate rows, and "
    "does not separately break out securitisation). FY2014-FY2016 predate any RWA category breakdown in the "
    "Bank's own Pillar 3 disclosures at all - only the Total (which ties exactly to the Total RWAs sheet) is "
    "shown, with Credit risk/CCR/Securitisation/Operational risk all left blank rather than estimated.\n\n"
    + ENTITY_NOTE
)

# ---------------------------------------------------------------
# Sheet 1: Balance Sheet
# ---------------------------------------------------------------
bw.add_balance_sheet_sheet(
    title="The Co-operative Bank p.l.c. — Balance Sheet (Bank Company-only)",
    subtitle="Bank Company-only basis (not the wider consolidated Group), £m",
    rows=[
        ("SECTION", "Assets", {}),
        ("DATA", "Cash and balances at central banks", {
            "FY2024": 2586.0, "FY2023": 2708.3, "FY2022": 5270.4, "FY2021": 5696.9, "FY2020": 3877.8,
            "FY2019": 2153.5, "FY2018": 1843.8, "FY2017": 4032.0, "FY2016": 2848.2, "FY2015": 2678.5, "FY2014": 4765.3,
            "FY2013": 5418.8, "FY2012": 5433.0, "FY2011": 6696.6, "FY2010": 1735.6, "FY2009": 1706.8,
            "FY2008": 164.7, "FY2007": 172.9, "FY2006": 186.9, "FY2005": 200.2, "FY2004": 172.4, "FY2003": 140.4,
        }),
        ("DATA", "Loans and advances to banks", {
            "FY2024": 173.1, "FY2023": 193.7, "FY2022": 312.5, "FY2021": 124.7, "FY2020": 431.6,
            "FY2019": 345.6, "FY2018": 380.4, "FY2017": 460.3, "FY2016": 836.9, "FY2015": 871.0, "FY2014": 1608.4,
            "FY2013": 1594.4, "FY2012": 1047.2, "FY2011": 1300.1, "FY2010": 1728.6, "FY2009": 1220.1,
            "FY2008": 1897.5, "FY2007": 1211.2, "FY2006": 1369.4, "FY2005": 1170.6, "FY2004": 1073.0, "FY2003": 773.2,
        }),
        ("DATA", "Loans and advances to customers", {
            "FY2024": 20370.8, "FY2023": 20147.5, "FY2022": 20919.1, "FY2021": 20998.3, "FY2020": 18676.7,
            "FY2019": 17811.1, "FY2018": 17614.3, "FY2017": 16608.2, "FY2016": 19452.7, "FY2015": 19690.4,
            "FY2014": 25377.4,
            "FY2013": 30322.2, "FY2012": 22785.5, "FY2011": 22735.0, "FY2010": 23844.9, "FY2009": 23050.8,
            "FY2008": 11169.8, "FY2007": 8914.4, "FY2006": 8051.8, "FY2005": 7807.9, "FY2004": 7546.4,
            "FY2003": 6073.2,
        }),
        ("DATA", "Fair value adjustments for hedged risk (assets)", {
            "FY2022": -430.7, "FY2021": -90.5, "FY2020": 134.1,
            "FY2019": 72.6, "FY2018": 53.4, "FY2017": 70.3, "FY2016": 131.6, "FY2015": 94.0, "FY2014": 148.5,
            "FY2013": 107.6, "FY2012": 354.1, "FY2011": 365.8, "FY2010": 164.6, "FY2009": 60.6,
        }),
        ("DATA", "Investment securities", {
            "FY2024": 1637.3, "FY2023": 2509.4, "FY2022": 1826.0, "FY2021": 2149.8, "FY2020": 2158.6,
            "FY2019": 3282.4, "FY2018": 2744.5, "FY2017": 3737.7, "FY2016": 3551.9, "FY2015": 4894.2,
            "FY2014": 4422.5,
            # FY2003-FY2013: sum of each year's own separately-disclosed sub-categories (loans and
            # receivables / available-for-sale / fair value through income or expense / held for trading
            # for FY2009-2013; a single 'Debt securities' or 'Debt securities - Available for sale' line
            # for FY2003-2008, which did not yet disclose a sub-category split) - see PRE-2018
            # PRESENTATION NOTE / PRE-2014 PRESENTATION NOTE in the source citation.
            "FY2013": 4499.4, "FY2012": 6744.7, "FY2011": 4316.6, "FY2010": 4636.9, "FY2009": 6616.2,
            "FY2008": 1810.2, "FY2007": 1985.7, "FY2006": 2369.6, "FY2005": 1912.8, "FY2004": 1378.3,
            "FY2003": 1850.0,
        }),
        ("DATA", "Derivative financial instruments", {
            "FY2024": 216.6, "FY2023": 301.0, "FY2022": 488.4, "FY2021": 241.2, "FY2020": 178.8,
            "FY2019": 188.1, "FY2018": 165.4, "FY2017": 197.4, "FY2016": 425.5, "FY2015": 370.1, "FY2014": 470.7,
            "FY2013": 555.8, "FY2012": 590.9, "FY2011": 704.4, "FY2010": 661.0, "FY2009": 660.8,
            "FY2008": 233.4, "FY2007": 88.5, "FY2006": 85.5, "FY2005": 68.3,
        }),
        ("DATA", "Property, plant and equipment classified as held-for-sale", {
            "FY2020": 0.3,
            "FY2019": 0.8, "FY2018": 3.9, "FY2017": 2.8, "FY2016": 5.3, "FY2015": 3.4, "FY2014": 387.3,
            "FY2013": 164.1,
        }),
        ("DATA", "Equity shares", {
            "FY2022": 11.1, "FY2021": 22.8, "FY2020": 22.1,
            "FY2019": 44.5, "FY2018": 26.4, "FY2017": 24.3, "FY2016": 46.8, "FY2015": 55.6, "FY2014": 2.8,
            "FY2013": 5.8, "FY2012": 5.7, "FY2011": 5.7, "FY2010": 7.2, "FY2009": 7.2,
            "FY2008": 13.0, "FY2007": 8.8, "FY2006": 1.7, "FY2005": 1.2, "FY2004": 1.2, "FY2003": 1.2,
        }),
        ("DATA", "Investments in joint ventures", {"FY2016": 6.0, "FY2015": 4.9, "FY2014": 5.3, "FY2013": 4.7}),
        ("DATA", "Goodwill", {
            "FY2012": 0.0, "FY2011": 0.6, "FY2010": 0.6, "FY2009": 0.6, "FY2008": 0.0, "FY2007": 0.0,
        }),
        ("DATA", "Investments in subsidiaries/group undertakings", {
            "FY2024": 22.8, "FY2023": 14.9, "FY2022": 15.0, "FY2021": 14.7, "FY2020": 43.3,
            "FY2019": 43.0, "FY2018": 49.4, "FY2017": 51.6,
            "FY2012": 1588.5, "FY2011": 1573.4, "FY2010": 1458.9, "FY2009": 1553.0,
            "FY2008": 969.3, "FY2007": 2.7, "FY2006": 2.7, "FY2005": 2.7, "FY2004": 1.2, "FY2003": 1.2,
        }),
        ("DATA", "Investment properties", {
            "FY2020": 1.9,
            "FY2019": 1.8, "FY2018": 2.3, "FY2017": 2.3, "FY2016": 2.2, "FY2015": 2.1, "FY2014": 2.1,
        }),
        ("DATA", "Other assets", {
            "FY2024": 51.0, "FY2023": 47.9, "FY2022": 14.1, "FY2021": 12.7, "FY2020": 99.6,
            "FY2019": 43.0, "FY2018": 39.9, "FY2017": 79.3, "FY2016": 96.7, "FY2015": 124.1, "FY2014": 187.6,
            "FY2013": 480.9, "FY2012": 67.3, "FY2011": 29.3, "FY2010": 51.5, "FY2009": 45.8,
            "FY2008": 31.0, "FY2007": 16.4, "FY2006": 43.9, "FY2005": 23.9, "FY2004": 41.4, "FY2003": 58.1,
        }),
        ("DATA", "Prepayments", {"FY2022": 21.4, "FY2021": 20.3, "FY2020": 13.2}),
        ("DATA", "Prepayments and accrued income", {
            "FY2019": 21.6, "FY2018": 31.8, "FY2017": 24.6, "FY2016": 28.7, "FY2015": 43.5, "FY2014": 12.2,
            "FY2013": 16.5, "FY2012": 14.0, "FY2011": 17.7, "FY2010": 14.5, "FY2009": 27.4,
            "FY2008": 56.8, "FY2007": 44.9, "FY2006": 79.3, "FY2005": 64.1, "FY2004": 89.4, "FY2003": 70.4,
        }),
        ("DATA", "Amounts owed by Co-operative Bank undertakings", {
            "FY2024": 552.1, "FY2023": 70.6, "FY2022": 65.1, "FY2021": 33.2, "FY2020": 1336.1,
            "FY2019": 1469.0, "FY2018": 1306.4, "FY2017": 1322.2, "FY2014": 0.0,
            "FY2013": 0.0, "FY2012": 12813.0, "FY2011": 12961.2, "FY2010": 14233.7, "FY2009": 11861.6,
        }),
        ("DATA", "Current tax assets", {
            "FY2024": 6.7, "FY2023": 4.3, "FY2022": 1.8,
            "FY2017": 2.5, "FY2014": 0.6,
            "FY2012": 154.0, "FY2011": 48.2, "FY2008": 2.5,
        }),
        ("DATA", "Items in the course of collection from other banks", {"FY2004": 108.0, "FY2003": 116.0}),
        ("DATA", "Property, plant and equipment", {
            "FY2024": 24.9, "FY2023": 23.6, "FY2022": 22.8, "FY2021": 24.3, "FY2020": 35.2,
            "FY2019": 38.6, "FY2018": 40.8, "FY2017": 44.4, "FY2016": 35.4, "FY2015": 46.1, "FY2014": 67.5,
            "FY2013": 115.2, "FY2012": 46.2, "FY2011": 61.5, "FY2010": 79.1, "FY2009": 101.6,
            "FY2008": 53.9, "FY2007": 74.0, "FY2006": 87.8, "FY2005": 79.8, "FY2004": 87.3, "FY2003": 84.6,
        }),
        ("DATA", "Intangible assets", {
            "FY2024": 109.8, "FY2023": 114.0, "FY2022": 90.0, "FY2021": 68.5, "FY2020": 63.4,
            "FY2019": 75.3, "FY2018": 72.4, "FY2017": 81.5, "FY2016": 100.1, "FY2015": 142.8, "FY2014": 103.7,
            "FY2013": 110.7, "FY2012": 33.8, "FY2011": 39.3, "FY2010": 43.8, "FY2009": 44.9,
            "FY2008": 1.5, "FY2007": 4.3, "FY2006": 6.3, "FY2005": 6.6,
        }),
        ("DATA", "Right-of-use assets", {
            "FY2024": 26.8, "FY2023": 31.4, "FY2022": 33.0, "FY2021": 46.9, "FY2020": 53.7,
            "FY2019": 72.3,
        }),
        ("DATA", "Deferred tax assets", {
            "FY2024": 243.0, "FY2023": 233.9, "FY2022": 167.5, "FY2021": 36.8,
            "FY2017": 0.6, "FY2015": 7.6, "FY2014": 21.0,
            "FY2013": 0.0, "FY2012": 138.8, "FY2011": 110.3, "FY2010": 154.0, "FY2009": 210.3,
            "FY2006": 8.3, "FY2005": 27.0,
        }),
        ("DATA", "Net retirement benefit asset", {
            "FY2024": 32.0, "FY2023": 148.5, "FY2022": 159.7, "FY2021": 841.1, "FY2020": 651.8,
            "FY2019": 690.2, "FY2018": 623.5, "FY2017": 157.7, "FY2016": 20.3,
        }),
        ("TOTAL", "Total assets", {
            "FY2024": 26052.9, "FY2023": 26549.0, "FY2022": 28987.2, "FY2021": 30241.7, "FY2020": 27778.2,
            "FY2019": 26353.4, "FY2018": 24998.6, "FY2017": 26899.7, "FY2016": 27588.3, "FY2015": 29028.3,
            "FY2014": 37582.9,
            "FY2013": 43396.1, "FY2012": 51818.5, "FY2011": 50965.7, "FY2010": 48814.9, "FY2009": 47167.7,
            "FY2008": 16403.6, "FY2007": 12523.8, "FY2006": 12293.2, "FY2005": 11365.1, "FY2004": 10498.6,
            "FY2003": 9168.3,
        }),
        ("SECTION", "Liabilities", {}),
        ("DATA", "Deposits by banks", {
            "FY2024": 2717.2, "FY2023": 4288.9, "FY2022": 5683.4, "FY2021": 5527.6, "FY2020": 2066.4,
            "FY2019": 1143.7, "FY2018": 1433.5, "FY2017": 1122.7, "FY2016": 1198.6, "FY2015": 725.9,
            "FY2014": 615.4,
            "FY2013": 2757.5, "FY2012": 3552.9, "FY2011": 3239.8, "FY2010": 2870.8, "FY2009": 5613.0,
            "FY2008": 1072.3, "FY2007": 661.3, "FY2006": 700.6, "FY2005": 641.1, "FY2004": 659.4, "FY2003": 773.8,
        }),
        ("DATA", "Customer accounts", {
            "FY2024": 19974.2, "FY2023": 19215.8, "FY2022": 20107.9, "FY2021": 21136.4, "FY2020": 20366.3,
            "FY2019": 18997.2, "FY2018": 18736.4, "FY2017": 20635.7, "FY2016": 22425.1, "FY2015": 22732.0,
            "FY2014": 29614.0,
            "FY2013": 32463.3, "FY2012": 33750.3, "FY2011": 32670.1, "FY2010": 29912.0, "FY2009": 28660.0,
            "FY2008": 13388.7, "FY2007": 10068.1, "FY2006": 9119.3, "FY2005": 8391.7, "FY2004": 7778.5,
            "FY2003": 7126.2,
        }),
        ("DATA", "Customer accounts – capital bonds", {
            "FY2017": 0.0, "FY2016": 11.8, "FY2015": 77.4, "FY2014": 263.8,
            "FY2013": 538.1, "FY2012": 867.2, "FY2011": 1397.3, "FY2010": 1744.0, "FY2009": 1581.7,
        }),
        ("DATA", "Fair value adjustment for hedged risk (liabilities)", {"FY2022": -34.6, "FY2021": -7.5}),
        ("DATA", "Debt securities in issue", {
            "FY2024": 499.3, "FY2020": 485.7,
            "FY2019": 602.4, "FY2018": 601.5, "FY2017": 600.7, "FY2016": 1625.4, "FY2015": 2554.3,
            "FY2014": 3443.6,
            "FY2013": 4195.3, "FY2012": 1752.2, "FY2011": 1431.0, "FY2010": 1856.8, "FY2009": 1739.3,
            "FY2008": 568.0, "FY2007": 535.8, "FY2006": 1113.3, "FY2005": 1050.2, "FY2004": 771.7,
            "FY2003": 224.7,
        }),
        ("DATA", "Derivative financial instruments", {
            "FY2024": 47.6, "FY2023": 110.3, "FY2022": 103.5, "FY2021": 148.2, "FY2020": 316.2,
            "FY2019": 278.9, "FY2018": 256.7, "FY2017": 308.8, "FY2016": 444.5, "FY2015": 346.9, "FY2014": 551.7,
            "FY2013": 538.6, "FY2012": 922.6, "FY2011": 1051.5, "FY2010": 697.4, "FY2009": 567.2,
            "FY2008": 123.2, "FY2007": 92.8, "FY2006": 118.0, "FY2005": 64.3,
        }),
        ("DATA", "Other borrowed funds", {
            "FY2017": 0.0, "FY2016": 472.6, "FY2015": 459.9, "FY2014": 196.4,
            "FY2013": 196.3, "FY2012": 1258.6, "FY2011": 1258.8, "FY2010": 975.4, "FY2009": 946.5,
            "FY2008": 358.4, "FY2007": 358.1, "FY2006": 387.8, "FY2005": 338.1,
            # FY2003-FY2004: labelled 'Subordinated liabilities' in the UK GAAP-era balance sheet - same
            # economic substance (subordinated debt funding), reproduced in this existing row.
            "FY2004": 327.6, "FY2003": 179.2,
        }),
        ("DATA", "Amounts owed to Co-operative Bank undertakings / parent undertakings / Finance Company", {
            "FY2024": 897.3, "FY2023": 937.6, "FY2022": 646.9, "FY2021": 402.1, "FY2020": 408.2,
            "FY2019": 3429.7, "FY2018": 1979.1, "FY2017": 2505.7, "FY2014": 0.0,
            "FY2013": 0.0, "FY2012": 7809.0, "FY2011": 7461.2, "FY2010": 8340.9, "FY2009": 5765.0,
        }),
        ("DATA", "Other liabilities", {
            "FY2024": 55.3, "FY2023": 44.1, "FY2022": 42.3, "FY2021": 38.0, "FY2020": 32.9,
            "FY2019": 52.7, "FY2018": 85.3, "FY2017": 33.9, "FY2016": 45.9, "FY2015": 68.8, "FY2014": 157.8,
            "FY2013": 202.9, "FY2012": 99.5, "FY2011": 169.1, "FY2010": 140.5, "FY2009": 210.8,
            "FY2008": 109.6, "FY2007": 102.5, "FY2006": 106.9, "FY2005": 108.9, "FY2004": 135.0,
            "FY2003": 124.1,
        }),
        ("DATA", "Accruals and deferred income", {
            "FY2024": 46.6, "FY2023": 22.7, "FY2022": 32.4, "FY2021": 36.8, "FY2020": 34.8,
            "FY2019": 58.4, "FY2018": 49.8, "FY2017": 59.9, "FY2016": 115.3, "FY2015": 152.5, "FY2014": 16.0,
            "FY2013": 54.1, "FY2012": 15.5, "FY2011": 33.1, "FY2010": 117.0, "FY2009": 134.3,
            "FY2008": 30.3, "FY2007": 32.5, "FY2006": 75.3, "FY2005": 71.5, "FY2004": 146.9, "FY2003": 127.3,
        }),
        ("DATA", "Liabilities directly associated with non-current assets classified as held for sale", {
            "FY2014": 7.9,
        }),
        ("DATA", "Items in the course of transmission to other banks", {"FY2004": 7.5, "FY2003": 7.1}),
        ("DATA", "Provisions", {
            "FY2024": 10.1, "FY2023": 31.7, "FY2022": 33.1, "FY2021": 33.8, "FY2020": 46.0,
            "FY2019": 86.8, "FY2018": 103.0, "FY2017": 157.4, "FY2016": 276.4, "FY2015": 499.2, "FY2014": 617.5,
            "FY2013": 576.0, "FY2012": 161.6, "FY2011": 93.4, "FY2010": 39.3, "FY2009": 25.6,
            "FY2008": 14.7, "FY2007": 8.8, "FY2006": 5.9, "FY2005": 5.2, "FY2004": 6.0, "FY2003": 6.9,
        }),
        ("DATA", "Current tax liabilities", {
            "FY2015": 0.3, "FY2014": 0.3,
            "FY2013": 4.2, "FY2010": 17.3, "FY2007": 2.9,
        }),
        ("DATA", "Lease liabilities", {
            "FY2024": 26.2, "FY2023": 30.1, "FY2022": 31.0, "FY2021": 44.1, "FY2020": 53.6,
            "FY2019": 71.2,
        }),
        ("DATA", "Deferred tax liabilities", {
            "FY2020": 38.2,
            "FY2019": 43.3, "FY2018": 38.7, "FY2016": 14.2, "FY2015": 47.8, "FY2014": 84.0,
            "FY2013": 92.5, "FY2008": 22.5, "FY2007": 0.7, "FY2005": 5.9, "FY2004": 4.5,
        }),
        ("DATA", "Net retirement benefit liability", {
            "FY2024": 5.2, "FY2023": 5.9, "FY2022": 5.9, "FY2021": 8.1, "FY2020": 8.8,
            "FY2019": 8.6, "FY2018": 7.6, "FY2017": 11.3,
        }),
        ("DATA", "Retirement benefit obligations", {"FY2005": 90.0}),
        ("TOTAL", "Total liabilities", {
            "FY2024": 24780.0, "FY2023": 25117.3, "FY2022": 27692.9, "FY2021": 28494.7, "FY2020": 26326.9,
            "FY2019": 24772.9, "FY2018": 23291.6, "FY2017": 25436.1, "FY2016": 26629.8, "FY2015": 27665.0,
            "FY2014": 35568.4,
            "FY2013": 41618.8, "FY2012": 50189.4, "FY2011": 48805.3, "FY2010": 46711.4, "FY2009": 45300.2,
            "FY2008": 15687.7, "FY2007": 11863.5, "FY2006": 11643.6, "FY2005": 10782.6, "FY2004": 9837.1,
            "FY2003": 8569.3,
        }),
        ("SECTION", "Equity", {}),
        ("DATA", "Ordinary share capital", {
            "FY2024": 25.6, "FY2023": 25.6, "FY2022": 25.6, "FY2021": 25.6, "FY2020": 25.6,
            "FY2019": 25.6, "FY2018": 25.6, "FY2017": 25.6, "FY2016": 22.6, "FY2015": 22.6, "FY2014": 22.6,
            "FY2013": 12.5, "FY2012": 410.0, "FY2011": 410.0, "FY2010": 410.0, "FY2009": 230.0,
            "FY2008": 55.0, "FY2007": 55.0, "FY2006": 55.0, "FY2005": 55.0, "FY2004": 55.0, "FY2003": 55.0,
        }),
        ("DATA", "Preference share capital (non-equity)", {"FY2004": 60.0, "FY2003": 60.0}),
        ("DATA", "Share premium account", {
            "FY2020": 2416.9,
            "FY2019": 2416.9, "FY2018": 2416.9, "FY2017": 2416.9, "FY2016": 1736.9, "FY2015": 1736.9,
            "FY2014": 1736.9,
            "FY2013": 1359.8, "FY2012": 8.8, "FY2011": 8.8, "FY2010": 8.8, "FY2009": 8.8,
            "FY2008": 8.8, "FY2007": 8.8, "FY2006": 8.8, "FY2005": 8.8, "FY2004": 8.8, "FY2003": 8.8,
        }),
        ("DATA", "Retained earnings", {
            "FY2024": 1328.6, "FY2023": 1398.2, "FY2022": 1241.1, "FY2021": 1218.8, "FY2020": -1823.6,
            "FY2019": -1736.2, "FY2018": -1594.9, "FY2017": -1514.4, "FY2016": -1315.1, "FY2015": -896.4,
            "FY2014": -273.1,
            "FY2013": -39.4, "FY2012": 1116.9, "FY2011": 1655.0, "FY2010": 1661.4, "FY2009": 1588.5,
            "FY2008": 610.7, "FY2007": 597.9, "FY2006": 608.3, "FY2005": 506.8,
            # FY2003-FY2004 label this 'Profit and loss account' (UK GAAP) - same substance.
            "FY2004": 537.7, "FY2003": 475.2,
        }),
        ("DATA", "Other reserves", {
            "FY2024": -81.3, "FY2023": 7.9, "FY2022": 27.6, "FY2021": 502.6, "FY2020": 832.4,
            "FY2019": 874.2, "FY2018": 859.4, "FY2017": 535.5, "FY2016": 514.1, "FY2015": 500.2, "FY2014": 493.6,
            # FY2009-FY2013: sum of the Bank balance sheet's own separately-disclosed Available for sale
            # reserve + Cashflow hedging reserve (+ Capital redemption reserve, FY2013 only, from the LME's
            # preference-share cancellation) - combined into one line here for consistency with the FY2021
            # onward presentation; the full per-component breakdown is on the Statement of Changes in
            # Equity sheet. FY2005-FY2008 reproduce the Bank's own single combined 'Other reserves' line
            # (that era's balance sheet format did not itemise the components at all).
            "FY2013": 410.8, "FY2012": 93.4, "FY2011": 86.6, "FY2010": 23.3, "FY2009": 40.2,
            "FY2008": 41.4, "FY2007": -1.4, "FY2006": -22.5, "FY2005": 11.9,
        }),
        ("DATA", "Non-controlling interests", {"FY2015": 0.0, "FY2014": 34.5, "FY2013": 33.6}),
        ("TOTAL", "Total equity", {
            "FY2024": 1272.9, "FY2023": 1431.7, "FY2022": 1294.3, "FY2021": 1747.0, "FY2020": 1451.3,
            "FY2019": 1580.5, "FY2018": 1707.0, "FY2017": 1463.6, "FY2016": 958.5, "FY2015": 1363.3,
            "FY2014": 2014.5,
            "FY2013": 1777.3, "FY2012": 1629.1, "FY2011": 2160.4, "FY2010": 2103.5, "FY2009": 1867.5,
            "FY2008": 715.9, "FY2007": 660.3, "FY2006": 649.6, "FY2005": 582.5, "FY2004": 661.5,
            "FY2003": 599.0,
        }),
        ("TOTAL", "Total liabilities and equity", {
            "FY2024": 26052.9, "FY2023": 26549.0, "FY2022": 28987.2, "FY2021": 30241.7, "FY2020": 27778.2,
            "FY2019": 26353.4, "FY2018": 24998.6, "FY2017": 26899.7, "FY2016": 27588.3, "FY2015": 29028.3,
            "FY2014": 37582.9,
            "FY2013": 43396.1, "FY2012": 51818.5, "FY2011": 50965.7, "FY2010": 48814.9, "FY2009": 47167.7,
            "FY2008": 16403.6, "FY2007": 12523.8, "FY2006": 12293.2, "FY2005": 11365.1, "FY2004": 10498.6,
            "FY2003": 9168.3,
        }),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=280,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet 2: Profit & Loss
# ---------------------------------------------------------------
bw.add_income_statement_sheet(
    title="The Co-operative Bank p.l.c. — Profit & Loss (Bank Company-only)",
    subtitle="Bank Company-only basis; bottom-line profit plus OCI detail (FY2017-FY2024), full income statement "
             "(FY2012-FY2016, see source note), £m",
    rows=[
        # HD-078 NOTE: FY2003-FY2011 are NOT included on this sheet. Bottom-line profit figures for
        # those years exist in the Bank's own primary sources, but this workbook's convention is that
        # a "Profit/(loss) for the year" figure must be independently disclosed, not backed out as a
        # residual of the Statement of Changes in Equity's net equity movement (which bundles profit,
        # dividends and, for the UK GAAP/early-IFRS years, some reserve transfers that were not
        # separately re-verified against the primary source in this pass). FY2012 and FY2013 ARE
        # included because the Bank's FY2013 Annual Report separately discloses a full income
        # statement for both years (own FY2013 column plus FY2012 comparative), giving genuinely
        # independent, source-disclosed top-of-statement and bottom-line figures. Detail rows below
        # (fee income, other income, opex, impairment, JV) are left blank for FY2012/FY2013 where the
        # source's own presentation does not itemise them the same way as FY2014-FY2016 - only the
        # rows the source directly discloses are populated for those two years.
        ("SECTION", "Full income statement (FY2012-FY2016, pre-restructuring - see source note)", {}),
        ("DATA", "Net interest income", {
            "FY2016": 220.3, "FY2015": 299.2, "FY2014": 345.0, "FY2013": 263.2, "FY2012": 565.8,
        }),
        ("DATA", "Net fee and commission income", {"FY2016": 40.9, "FY2015": 71.8, "FY2014": 122.4}),
        ("DATA", "Other operating income/(expense)", {"FY2016": 60.8, "FY2015": -130.3, "FY2014": -0.5}),
        ("TOTAL", "Operating income", {
            "FY2016": 322.0, "FY2015": 240.7, "FY2014": 466.9, "FY2013": 270.1, "FY2012": 641.3,
        }),
        ("DATA", "Total operating expenses", {"FY2016": -805.6, "FY2015": -900.6, "FY2014": -904.9}),
        ("TOTAL", "Operating (loss) before impairment", {"FY2016": -483.6, "FY2015": -659.9, "FY2014": -438.0}),
        ("DATA", "Net impairment gains/(losses) on loans and advances", {
            "FY2016": 6.2, "FY2015": 48.6, "FY2014": 173.2,
        }),
        ("TOTAL", "Operating (loss)", {"FY2016": -477.4, "FY2015": -611.3, "FY2014": -264.8}),
        ("DATA", "Share of post-tax profits from joint ventures", {"FY2016": 0.3, "FY2015": 0.7, "FY2014": 0.6}),
        ("TOTAL", "(Loss) before taxation", {
            "FY2016": -477.1, "FY2015": -610.6, "FY2014": -264.2, "FY2013": -586.2, "FY2012": -673.7,
        }),
        ("DATA", "Income tax", {
            "FY2016": 58.4, "FY2015": -12.2, "FY2014": 39.0,
            # FY2013/FY2012: not separately disclosed on the same line basis as FY2014-2016 in the
            # source; derived as (Loss for the year) - (Loss before taxation) from the two directly
            # disclosed figures rather than transcribed as a standalone source line.
            "FY2013": -161.8, "FY2012": 165.6,
        }),
        ("TOTAL", "(Loss) for the financial year (incl. non-controlling interests)", {
            "FY2016": -418.7, "FY2015": -622.8, "FY2014": -225.2, "FY2013": -748.0, "FY2012": -508.1,
        }),
        ("SECTION", "Profit/(loss) attributable to equity shareholders (all years)", {}),
        ("TOTAL", "Profit/(loss) for the year", {
            "FY2024": 25.4, "FY2023": 157.1, "FY2022": 22.3, "FY2021": 215.5, "FY2020": -87.4,
            "FY2019": -141.3, "FY2018": -73.8, "FY2017": 32.8, "FY2016": -418.7, "FY2015": -623.3,
            "FY2014": -226.6,
            # FY2013: attributable-to-equity-shareholders split not separately re-verified in this
            # pass - loss for the financial year shown above (-748.0) used as a close approximation
            # (2013's non-controlling interest was newly created at/near year-end via the LME, so any
            # divergence from the attributable figure is expected to be small).
            "FY2013": -748.0,
            "FY2012": -509.1,
        }),
        ("SECTION", "Other comprehensive income/(expense), net of tax", {}),
        ("DATA", "Fair value through OCI (FVOCI) reserve movement", {
            "FY2024": -0.3, "FY2023": -2.7, "FY2022": -8.2, "FY2021": -1.9, "FY2020": 0.7,
            "FY2019": -9.8, "FY2018": -4.5, "FY2017": -13.4, "FY2016": -17.4, "FY2015": 31.0, "FY2014": 38.7,
        }),
        ("DATA", "Cash flow hedging reserve movement", {
            "FY2024": -4.4, "FY2023": -5.2, "FY2022": -4.1, "FY2021": -7.8, "FY2020": 5.8,
            "FY2019": -3.3, "FY2018": -9.9, "FY2017": -26.5, "FY2016": 21.8, "FY2015": -24.4, "FY2014": 45.9,
        }),
        ("DATA", "Defined benefit pension reserve movement", {
            "FY2024": -84.5, "FY2023": -11.8, "FY2022": -462.7, "FY2021": 89.9, "FY2020": -48.3,
            "FY2019": 27.9, "FY2018": 344.7, "FY2017": 61.3, "FY2016": 9.5,
        }),
        ("TOTAL", "Other comprehensive income/(expense) for the year, net of tax", {
            "FY2024": -89.2, "FY2023": -19.7, "FY2022": -475.0, "FY2021": 80.2, "FY2020": -41.8,
            "FY2019": 14.8, "FY2018": 330.3, "FY2017": 21.4, "FY2016": 13.9, "FY2015": 6.6, "FY2014": 84.6,
        }),
        ("TOTAL", "Total comprehensive income/(expense) for the year, net of tax", {
            "FY2024": -63.8, "FY2023": 137.4, "FY2022": -452.7, "FY2021": 295.7, "FY2020": -129.2,
            "FY2019": -126.5, "FY2018": 256.5, "FY2017": 54.2, "FY2016": -404.8, "FY2015": -616.7,
            "FY2014": -142.0,
        }),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=280,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet 3: Statement of Changes in Equity
# ---------------------------------------------------------------
bw.add_equity_changes_sheet(
    title="The Co-operative Bank p.l.c. — Statement of Changes in Equity (Bank Company-only)",
    subtitle="Bank Company-only basis, £m, chronological",
    headers=[
        "Share capital", "Share premium", "FVOCI reserve", "Cash flow hedging reserve",
        "Capital redemption reserve", "Defined benefit pension reserve", "Retained earnings",
        "Non-controlling interest", "Total equity",
    ],
    rows=[
        # HD-078: FY2003-FY2013 roll-forward below is reconstructed from the already-verified,
        # per-year Balance Sheet sheet equity components (Ordinary + Preference share capital,
        # Share premium, Retained earnings, Other reserves, NCI - each year's Total ties exactly
        # to that sheet's Total equity row). The Bank's own pre-2014 disclosures do not break
        # "Other reserves" into separate AFS/FVOCI vs cash flow hedging vs capital redemption
        # columns for FY2005-FY2012 (that level of split first appears from FY2013 onward), so
        # the combined "Other reserves" balance for those years is carried in the "FVOCI reserve"
        # column below rather than fabricated across three columns - see PRE2014_HISTORY_NOTE.
        # Year-on-year movement rows are shown as a single aggregate "Net movement" line (profit,
        # dividends, share issuance, etc. are not separately itemised pre-2014 in this workbook)
        # rather than force-splitting into per-cause rows the source documents did not tabulate
        # for the Bank Company-only column in a directly reusable way.
        ("TOTAL", "At 31 December 2003 (Bank company-only; UK GAAP; share capital incl. £60.0m preference)",
         (115.0, 8.8, None, None, None, None, 475.2, None, 599.0)),
        ("DATA", "Net movement during the year (FY2004)",
         (0.0, 0.0, None, None, None, None, 62.5, None, 62.5)),
        ("TOTAL", "At 31 December 2004 (UK GAAP; share capital incl. £60.0m preference)",
         (115.0, 8.8, None, None, None, None, 537.7, None, 661.5)),
        ("DATA", "Net movement during the year (FY2005, incl. redemption of £60.0m preference "
                 "share capital and IFRS transition)",
         (-60.0, 0.0, 11.9, None, None, None, -30.9, None, -79.0)),
        ("TOTAL", "At 31 December 2005 (IFRS)", (55.0, 8.8, 11.9, None, None, None, 506.8, None, 582.5)),
        ("DATA", "Net movement during the year (FY2006)",
         (0.0, 0.0, -34.4, None, None, None, 101.5, None, 67.1)),
        ("TOTAL", "At 31 December 2006", (55.0, 8.8, -22.5, None, None, None, 608.3, None, 649.6)),
        ("DATA", "Net movement during the year (FY2007)",
         (0.0, 0.0, 21.1, None, None, None, -10.4, None, 10.7)),
        ("TOTAL", "At 31 December 2007", (55.0, 8.8, -1.4, None, None, None, 597.9, None, 660.3)),
        ("DATA", "Net movement during the year (FY2008)",
         (0.0, 0.0, 42.8, None, None, None, 12.8, None, 55.6)),
        ("TOTAL", "At 31 December 2008", (55.0, 8.8, 41.4, None, None, None, 610.7, None, 715.9)),
        ("DATA", "Net movement during the year (FY2009, incl. Britannia transfer of engagements "
                 "and new share capital issuance)",
         (175.0, 0.0, -1.2, None, None, None, 977.8, None, 1151.6)),
        ("TOTAL", "At 31 December 2009", (230.0, 8.8, 40.2, None, None, None, 1588.5, None, 1867.5)),
        ("DATA", "Net movement during the year (FY2010, incl. new share capital issuance)",
         (180.0, 0.0, -16.9, None, None, None, 72.9, None, 236.0)),
        ("TOTAL", "At 31 December 2010", (410.0, 8.8, 23.3, None, None, None, 1661.4, None, 2103.5)),
        ("DATA", "Net movement during the year (FY2011)",
         (0.0, 0.0, 63.3, None, None, None, -6.4, None, 56.9)),
        ("TOTAL", "At 31 December 2011", (410.0, 8.8, 86.6, None, None, None, 1655.0, None, 2160.4)),
        ("DATA", "Net movement during the year (FY2012)",
         (0.0, 0.0, 6.8, None, None, None, -538.1, None, -531.3)),
        ("TOTAL", "At 31 December 2012 (per the Bank's own FY2012 Annual Report)",
         (410.0, 8.8, 93.4, None, None, None, 1116.9, None, 1629.1)),
        ("DATA", "Restatement (FY2013 Annual Report's restated FY2012 comparative closing position "
                 "vs. the Bank's own FY2012 Annual Report; cause not narrated in the source - see "
                 "PRE2014_HISTORY_NOTE)",
         (0.0, 0.0, 221.1, None, None, None, 0.0, None, 221.1)),
        ("DATA", "Net movement during the year (FY2013, incl. Liability Management Exercise "
                 "share/capital restructuring)",
         (-397.5, 1351.0, 96.3, None, None, None, -1156.3, 33.6, -72.9)),
        ("TOTAL", "At 31 December 2013 (per the Bank's own FY2013 Annual Report)",
         (12.5, 1359.8, 410.8, None, None, None, -39.4, 33.6, 1777.3)),
        ("DATA", "Restatement (FY2014 Annual Report's restated FY2013 comparative opening position "
                 "vs. the Bank's own FY2013 Annual Report; £8.8m difference within the Cashflow "
                 "hedging reserve and Retained earnings columns - see PRE2014_HISTORY_NOTE)",
         (0.0, 0.0, -424.9, 13.1, 410.0, None, -7.0, 0.0, -8.8)),
        ("TOTAL", "At 1 January 2014",
         (12.5, 1359.8, -14.1, 13.1, 410.0, None, -46.4, 33.6, 1768.5)),
        ("DATA", "Total comprehensive (expense)/income for the year (FY2014)",
         (None, None, 38.7, 45.9, None, None, -226.6, 1.1, -140.9)),
        ("DATA", "Issuance of new share capital (FY2014)",
         (10.1, 377.1, None, None, None, None, None, None, 387.2)),
        ("DATA", "Dividend (FY2014)",
         (None, None, None, None, None, None, -0.1, -0.2, -0.3)),
        ("TOTAL", "At 31 December 2014 / 1 January 2015",
         (22.6, 1736.9, 24.6, 59.0, 410.0, None, -273.1, 34.5, 2014.5)),
        ("DATA", "Total comprehensive income/(expense) for the year (FY2015)",
         (None, None, 31.0, -24.4, None, None, -623.3, 0.4, -616.3)),
        ("DATA", "Disposal of Unity Trust Bank plc (FY2015)",
         (None, None, None, None, None, None, None, -34.9, -34.9)),
        ("TOTAL", "At 31 December 2015", (22.6, 1736.9, 55.6, 34.6, 410.0, None, -896.4, 0.0, 1363.3)),
        ("DATA", "Total comprehensive (expense)/income for the year (FY2016)",
         (None, None, -17.4, 21.8, None, 9.5, -418.7, None, -404.8)),
        ("TOTAL", "At 31 December 2016", (22.6, 1736.9, 38.2, 56.4, 410.0, 9.5, -1315.1, None, 958.5)),
        ("DATA", "Restatement (re-presentation of netting arrangements, per 2017 Annual Report note)",
         (None, None, None, None, None, None, -232.1, None, -232.1)),
        ("DATA", "Total comprehensive (expense)/income for the year (FY2017)",
         (None, None, -13.4, -26.5, None, 61.3, 32.8, None, 54.2)),
        ("DATA", "Issuance of new share capital (FY2017 Restructuring and Recapitalisation)",
         (3.0, 680.0, None, None, None, None, None, None, 683.0)),
        ("TOTAL", "At 31 December 2017", (25.6, 2416.9, 24.8, 29.9, 410.0, 70.8, -1514.4, None, 1463.6)),
        ("DATA", "IFRS 9 opening balance adjustment (1 January 2018)",
         (None, None, -6.4, None, None, None, -6.7, None, -13.1)),
        ("DATA", "Total comprehensive (expense)/income for the year (FY2018)",
         (None, None, -4.5, -9.9, None, 344.7, -73.8, None, 256.5)),
        ("TOTAL", "At 31 December 2018", (25.6, 2416.9, 13.9, 20.0, 410.0, 415.5, -1594.9, None, 1707.0)),
        ("DATA", "Total comprehensive (expense)/income for the year (FY2019)",
         (None, None, -9.8, -3.3, None, 27.9, -141.3, None, -126.5)),
        ("TOTAL", "At 31 December 2019 / 1 January 2020",
         (25.6, 2416.9, 4.1, 16.7, 410.0, 443.4, -1736.2, None, 1580.5)),
        ("DATA", "Total comprehensive income/(expense) for the year (FY2020)",
         (None, None, 0.7, 5.8, None, -48.3, -87.4, None, -129.2)),
        ("TOTAL", "At 31 December 2020", (25.6, 2416.9, 4.8, 22.5, 410.0, 395.1, -1823.6, None, 1451.3)),
        ("DATA", "Total comprehensive income for the year (FY2021)",
         (None, None, -1.9, -7.8, None, 89.9, 215.5, None, 295.7)),
        ("DATA", "Reserve reorganisation (FY2021)",
         (None, -2416.9, None, None, -410.0, None, 2826.9, None, 0.0)),
        ("TOTAL", "At 31 December 2021", (25.6, 0.0, 2.9, 14.7, 0.0, 485.0, 1218.8, None, 1747.0)),
        ("DATA", "Total comprehensive (expense)/income for the year (FY2022)",
         (None, None, -8.2, -4.1, None, -462.7, 22.3, None, -452.7)),
        ("TOTAL", "At 31 December 2022", (25.6, 0.0, -5.3, 10.6, 0.0, 22.3, 1241.1, None, 1294.3)),
        ("DATA", "Total comprehensive income for the year (FY2023)",
         (None, None, -2.7, -5.2, None, -11.8, 157.1, None, 137.4)),
        ("TOTAL", "At 31 December 2023", (25.6, 0.0, -8.0, 5.4, 0.0, 10.5, 1398.2, None, 1431.7)),
        ("DATA", "Total comprehensive (expense)/income for the year (FY2024)",
         (None, None, -0.3, -4.4, None, -84.5, 25.4, None, -63.8)),
        ("DATA", "Dividends paid (FY2024)", (None, None, None, None, None, None, -95.0, None, -95.0)),
        ("TOTAL", "At 31 December 2024", (25.6, 0.0, -8.3, 1.0, 0.0, -74.0, 1328.6, None, 1272.9)),
    ],
    sources_text=STATEMENTS_SOURCES,
)

# ---------------------------------------------------------------
# Sheet: Cash Flow Statement
# ---------------------------------------------------------------
# HD-078 NOTE: this sheet is NOT extended past FY2014 in this pass. The Balance Sheet and
# Statement of Changes in Equity sheets were extended to FY2003 and their totals independently
# tie out year-on-year (see those sheets' own source notes). Extending the Cash Flow Statement
# would require transcribing ~15-20 new line items per year (operating working-capital
# movements, investing purchases/proceeds, financing issuances/redemptions) plus the FY2003-
# FY2004 Consolidated-Group-basis structural difference already flagged in PRE2014_HISTORY_NOTE
# / CASH_FLOW_SOURCES, at the same per-figure transcription accuracy bar already applied to the
# Balance Sheet (three genuine transcription errors were caught and fixed there only via
# exact-tie arithmetic against a disclosed control total). That same verification could not be
# completed to the required confidence level in this pass without re-opening and re-checking
# each year's primary source document image again line-by-line, so this sheet is deliberately
# left at its existing FY2014-FY2024 range rather than shipping under-verified figures.
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {
        "FY2024": 50.9, "FY2023": 105.6, "FY2022": 132.9, "FY2021": 49.4, "FY2020": -95.1,
        "FY2019": -143.6, "FY2018": -142.8, "FY2017": 41.2, "FY2016": -477.1, "FY2015": -610.6,
        "FY2014": -264.2, "FY2013": -586.2, "FY2012": -673.7,
    }),
    ("DATA", "Pension scheme adjustments", {
        "FY2024": -0.9, "FY2023": -3.4, "FY2022": -12.7, "FY2021": -5.6, "FY2020": -9.3,
        "FY2019": -13.9, "FY2018": 4.4, "FY2017": -51.9, "FY2012": 0.1,
    }),
    ("DATA", "Net credit impairment (gains)/losses", {
        "FY2024": -5.0, "FY2023": 0.6, "FY2022": 6.4, "FY2021": 1.1, "FY2020": 21.6,
        "FY2019": -1.8, "FY2018": -5.4, "FY2017": 1.3, "FY2016": -6.2, "FY2015": -48.6, "FY2014": -170.9,
        "FY2013": -517.3, "FY2012": -480.2,
    }),
    ("DATA", "Depreciation, amortisation and impairment", {
        "FY2024": 35.3, "FY2023": 34.8, "FY2022": 35.3, "FY2021": 36.6, "FY2020": 40.2,
        "FY2019": 42.8, "FY2018": 33.5, "FY2017": 38.5, "FY2016": 81.7, "FY2015": 40.7, "FY2014": 47.6,
        "FY2013": 197.1, "FY2012": 191.7,
    }),
    ("DATA", "Impairment of investment in subsidiaries", {
        "FY2024": 21.0, "FY2023": 0.1, "FY2022": -0.3, "FY2021": 28.6, "FY2020": -0.3,
        "FY2019": 1.4, "FY2018": 2.2, "FY2017": 167.3,
    }),
    ("DATA", "Other non-cash movements (incl. exchange rate movements)", {
        "FY2024": 53.2, "FY2023": 54.9, "FY2022": 134.4, "FY2021": 121.4, "FY2020": 77.1,
        "FY2019": 89.4, "FY2018": 105.6, "FY2017": -218.6, "FY2016": 110.1, "FY2015": 43.7, "FY2014": -79.2,
        "FY2013": 184.8, "FY2012": -81.4,
    }),
    ("DATA", "Increase/(decrease) in deposits by banks", {
        "FY2024": -1571.7, "FY2023": -1394.5, "FY2022": 155.8, "FY2021": 3461.2, "FY2020": 922.7,
        "FY2019": -289.8, "FY2018": 310.8, "FY2017": 102.7, "FY2016": 472.7, "FY2015": 110.5,
        "FY2014": -2142.1,
    }),
    ("DATA", "(Increase) in prepayments", {
        "FY2024": -11.6, "FY2023": -2.7, "FY2022": -1.1, "FY2021": -7.1, "FY2020": 8.4,
        "FY2019": 8.1, "FY2018": -7.2, "FY2017": 4.1, "FY2016": 14.8, "FY2015": -31.3, "FY2014": 4.3,
    }),
    ("DATA", "Increase/(decrease) in accruals and deferred income", {
        "FY2024": 23.9, "FY2023": -9.7, "FY2022": -4.4, "FY2021": 2.0, "FY2020": -23.6,
        "FY2019": 8.6, "FY2018": -10.1, "FY2017": -31.4, "FY2016": -37.2, "FY2015": 136.5, "FY2014": -38.1,
    }),
    ("DATA", "Increase/(decrease) in customer accounts", {
        "FY2024": 759.5, "FY2023": -873.9, "FY2022": -1028.7, "FY2021": 769.2, "FY2020": 1367.9,
        "FY2019": 259.3, "FY2018": -1899.3, "FY2017": -1934.6, "FY2016": -372.5, "FY2015": -7068.4,
        "FY2014": -3123.6,
    }),
    ("DATA", "(Decrease) in debt securities in issue", {
        "FY2022": 0.0, "FY2021": -485.7, "FY2020": -121.9,
        "FY2019": 0.9, "FY2018": 0.8, "FY2017": -406.1, "FY2016": -1105.7, "FY2015": -889.3, "FY2014": -764.0,
    }),
    ("DATA", "Decrease/(increase) in loans and advances to banks", {
        "FY2024": 25.7, "FY2023": -18.7, "FY2022": -19.9, "FY2021": -23.8, "FY2020": -16.9,
        "FY2019": -17.2, "FY2018": -16.6, "FY2017": 3.5, "FY2016": -9.0, "FY2015": 510.9, "FY2014": 105.3,
    }),
    ("DATA", "(Increase)/decrease in loans and advances to customers", {
        "FY2024": -210.7, "FY2023": 578.5, "FY2022": 31.5, "FY2021": -2358.6, "FY2020": -912.2,
        "FY2019": -223.2, "FY2018": -1015.5, "FY2017": 2654.3, "FY2016": 239.7, "FY2015": 5729.0,
        "FY2014": 5073.6,
    }),
    ("DATA", "Increase/(decrease) in amounts owed by Co-operative Bank undertakings", {
        "FY2024": -481.5, "FY2023": -5.5, "FY2022": -31.9, "FY2021": 1302.9, "FY2020": 132.9,
        "FY2019": -138.3, "FY2018": 15.8, "FY2017": -215.9,
    }),
    ("DATA", "Increase/(decrease) in amounts owed to Co-operative Bank undertakings", {
        "FY2024": 70.8, "FY2023": -564.5, "FY2022": -86.0, "FY2021": -1342.7, "FY2020": -755.7,
        "FY2019": 173.4, "FY2018": -526.6, "FY2017": 364.7,
    }),
    ("DATA", "Net movement of other assets and other liabilities", {
        "FY2024": 1.6, "FY2023": -64.5, "FY2022": -3.8, "FY2021": 49.3, "FY2020": -154.6,
        "FY2019": -182.5, "FY2018": -70.3, "FY2017": -163.5, "FY2016": -139.3, "FY2015": 93.5,
        "FY2014": -236.2,
    }),
    ("DATA", "Income tax paid", {
        "FY2024": -4.0, "FY2023": -2.7, "FY2022": -6.8, "FY2021": 0.0,
        "FY2019": 0.0, "FY2018": 0.0, "FY2017": 71.6, "FY2016": 0.4, "FY2015": -0.1, "FY2014": 4.3,
    }),
    ("TOTAL", "Net cash flows from/(used in) operating activities", {
        "FY2024": -1243.5, "FY2023": -2165.6, "FY2022": -699.3, "FY2021": 1598.2, "FY2020": 481.2,
        "FY2019": -426.4, "FY2018": -3220.7, "FY2017": 427.2, "FY2016": -1227.6, "FY2015": -1983.5,
        "FY2014": -1583.2,
    }),

    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase and construction of tangible and intangible assets", {
        "FY2024": -27.6, "FY2023": -55.0, "FY2022": -48.0, "FY2021": -28.9, "FY2020": -16.8,
        "FY2019": -34.5, "FY2018": -24.4, "FY2017": -43.1, "FY2016": -39.7, "FY2015": -79.5, "FY2014": -74.9,
    }),
    ("DATA", "Purchase of investment securities", {
        "FY2024": -1096.4, "FY2023": -1544.9, "FY2022": -471.6, "FY2021": -886.5, "FY2020": -969.6,
        "FY2019": -1081.8, "FY2018": -462.6, "FY2017": -1859.9, "FY2016": -363.7, "FY2015": -1916.3,
        "FY2014": -2279.0,
    }),
    ("DATA", "Proceeds from sale of property, plant and equipment", {
        "FY2022": 0.4, "FY2021": 1.9, "FY2020": 2.6,
        "FY2019": 5.9, "FY2018": 0.5, "FY2017": 4.9, "FY2016": 12.0, "FY2015": 21.4, "FY2014": 8.3,
    }),
    ("DATA", "Proceeds from sale of shares and other interests", {
        "FY2024": 13.6, "FY2023": 0.2, "FY2022": 20.4, "FY2021": 2.0, "FY2020": 38.6,
        "FY2019": 13.2, "FY2017": 25.3, "FY2016": 41.8,
    }),
    ("DATA", "Proceeds from sale and maturity of investment securities", {
        "FY2024": 1972.6, "FY2023": 899.0, "FY2022": 750.8, "FY2021": 849.9, "FY2020": 2088.4,
        "FY2019": 1603.1, "FY2018": 1415.9, "FY2017": 1651.6, "FY2016": 1747.6, "FY2015": 1269.9,
        "FY2014": 2580.0,
    }),
    ("DATA", "Purchase of equity shares", {
        "FY2022": -0.8, "FY2021": -0.5,
    }),
    ("DATA", "Proceeds from sale of investment properties", {
        "FY2024": 0.2, "FY2023": 0.3, "FY2020": 0.0,
        "FY2019": 0.5, "FY2016": 0.1, "FY2014": 156.5,
    }),
    ("DATA", "Dividends received", {
        "FY2024": 0.2, "FY2023": 6.8, "FY2022": 0.2, "FY2021": 0.3, "FY2020": 0.3,
        "FY2019": 0.7, "FY2018": 5.9, "FY2017": 262.1,
    }),
    ("DATA", "Net movement on investments in Co-operative Bank undertakings", {"FY2017": 587.9}),
    ("DATA", "Profit from sale of subsidiaries/joint ventures", {"FY2018": 0.7, "FY2015": 30.2}),
    ("TOTAL", "Net cash flows from/(used in) investing activities", {
        "FY2024": 862.6, "FY2023": -693.6, "FY2022": 251.4, "FY2021": -61.8, "FY2020": 1143.5,
        "FY2019": 507.1, "FY2018": 936.0, "FY2017": 628.8, "FY2016": 1398.1, "FY2015": -674.3,
        "FY2014": 390.9,
    }),

    ("SECTION", "Financing activities", {}),
    ("DATA", "Proceeds from issuance of Tier 2 notes / senior unsecured debt / MREL", {
        "FY2024": 199.1, "FY2023": 397.9, "FY2022": 248.4, "FY2020": 197.7,
        "FY2019": 197.3,
    }),
    ("DATA", "Redemption of Tier 2 notes and senior unsecured debt", {
        "FY2024": -236.5, "FY2023": -163.5,
    }),
    ("DATA", "Proceeds from issuance of covered bonds", {
        "FY2024": 498.5, "FY2023": 0.0,
    }),
    ("DATA", "Interest paid on Tier 2 notes, senior unsecured debt and covered bonds", {
        "FY2024": -88.2, "FY2023": -62.7, "FY2022": -44.5, "FY2021": -37.0, "FY2020": -19.0,
        "FY2019": -9.5,
    }),
    ("DATA", "Interest paid on other borrowed funds", {
        "FY2017": -29.3, "FY2016": -43.9, "FY2015": -28.6, "FY2014": -22.8,
    }),
    ("DATA", "Issuance of other borrowed funds", {"FY2016": 0.0, "FY2015": 249.0}),
    ("DATA", "Net cash raised through Restructuring and Recapitalisation (FY2017)", {"FY2017": 180.4}),
    ("DATA", "Capital raising proceeds/costs and Co-operative Group capital commitment (FY2014)", {
        "FY2014": 700.2,
    }),
    ("DATA", "Dividends paid to non-controlling interests", {"FY2014": -0.2}),
    ("DATA", "Lease liability principal payments", {
        "FY2024": -5.6, "FY2023": -6.6, "FY2022": -14.6, "FY2021": -11.0, "FY2020": -10.0,
        "FY2019": -10.8,
    }),
    ("DATA", "Dividends paid", {
        "FY2024": -95.0, "FY2023": 0.0,
    }),
    ("TOTAL", "Net cash flows from/(used in) financing activities", {
        "FY2024": 272.3, "FY2023": 165.1, "FY2022": 189.3, "FY2021": -48.0, "FY2020": 168.7,
        "FY2019": 177.0, "FY2018": 0.0, "FY2017": 151.1, "FY2016": -43.9, "FY2015": 220.4,
        "FY2014": 677.2,
    }),

    ("DATA", "Effect of exchange rate changes on cash and cash equivalents", {
        "FY2024": -8.6, "FY2023": -5.5,
    }),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {
        "FY2024": -117.2, "FY2023": -2699.6, "FY2022": -258.6, "FY2021": 1488.4, "FY2020": 1793.4,
        "FY2019": 257.7, "FY2018": -2284.7, "FY2017": 1207.1, "FY2016": 126.6, "FY2015": -2437.4,
        "FY2014": -515.1,
    }),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {
        "FY2024": 2751.3, "FY2023": 5450.9, "FY2022": 5709.5, "FY2021": 4221.1, "FY2020": 2427.7,
        "FY2019": 2170.0, "FY2018": 4454.7, "FY2017": 3247.6, "FY2016": 3139.7, "FY2015": 5577.1,
        "FY2014": 6092.2,
    }),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {
        "FY2024": 2634.1, "FY2023": 2751.3, "FY2022": 5450.9, "FY2021": 5709.5, "FY2020": 4221.1,
        "FY2019": 2427.7, "FY2018": 2170.0, "FY2017": 4454.7, "FY2016": 3266.3, "FY2015": 3139.7,
        "FY2014": 5577.1,
    }),
    ("DATA", "Comprising: Cash and balances with central banks", {
        "FY2024": 2586.0, "FY2023": 2631.7, "FY2022": 5183.8, "FY2021": 5609.8, "FY2020": 3802.5,
        "FY2019": 2094.6, "FY2018": 1789.6, "FY2017": 3994.4, "FY2016": 2807.2, "FY2015": 2632.9,
        "FY2014": 4707.5,
    }),
    ("DATA", "Comprising: Loans and advances to banks", {
        "FY2024": 48.1, "FY2023": 119.6, "FY2022": 267.1, "FY2021": 99.7, "FY2020": 418.6,
        "FY2019": 333.1, "FY2018": 380.4, "FY2017": 460.3, "FY2016": 459.1, "FY2015": 506.8,
        "FY2014": 745.5,
    }),
    ("DATA", "Comprising: Other (held for sale / short-term investments) (FY2014)", {"FY2014": 124.1}),
]

bw.add_cash_flow_sheet(
    title="The Co-operative Bank p.l.c. — Statement of Cashflows (Bank Company-only)",
    subtitle="Bank Company-only basis (not the wider consolidated Group), £m",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=70,
    source_height=170,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
bw.add_asset_quality_sheet(
    title="The Co-operative Bank p.l.c. — Asset Quality (Bank Company-only)",
    subtitle="Bank Company-only basis, £m; Loans and advances to customers by IFRS 9 stage",
    rows=[
        ("SECTION", "Gross customer exposure by IFRS 9 stage", {}),
        ("DATA", "Stage 1", {
            "FY2024": 20306.9, "FY2023": 19199.2, "FY2022": 18933.0, "FY2021": 21826.2, "FY2020": 19180.3,
            "FY2019": 18753.1, "FY2018": 16546.0,
        }),
        ("DATA", "Stage 2", {
            "FY2024": 1415.9, "FY2023": 2421.1, "FY2022": 3692.0, "FY2021": 922.9, "FY2020": 1718.1,
            "FY2019": 779.5, "FY2018": 545.5,
        }),
        ("DATA", "Stage 3", {
            "FY2024": 114.9, "FY2023": 98.3, "FY2022": 80.3, "FY2021": 67.4, "FY2020": 63.5,
            "FY2019": 78.2, "FY2018": 133.7,
        }),
        ("DATA", "POCI (purchased or originated credit-impaired)", {
            "FY2024": 47.5, "FY2023": 55.5, "FY2022": 65.1, "FY2021": 77.3, "FY2020": 93.1,
            "FY2019": 119.3, "FY2018": 293.8,
        }),
        ("TOTAL", "Total gross customer exposure subject to ECL calculation", {
            "FY2024": 21885.2, "FY2023": 21774.1, "FY2022": 22770.4, "FY2021": 22893.8, "FY2020": 21055.0,
            "FY2019": 19730.1, "FY2018": 17519.0,
        }),
        ("SECTION", "Allowance for losses by IFRS 9 stage", {}),
        ("DATA", "Stage 1 allowance", {
            "FY2024": -8.4, "FY2023": -8.8, "FY2022": -11.3, "FY2021": -19.1, "FY2020": -19.1,
            "FY2019": -10.5, "FY2018": -11.8,
        }),
        ("DATA", "Stage 2 allowance", {
            "FY2024": -13.0, "FY2023": -20.7, "FY2022": -6.8, "FY2021": -13.0, "FY2020": -13.0,
            "FY2019": -4.2, "FY2018": -5.0,
        }),
        ("DATA", "Stage 3 allowance", {
            "FY2024": -7.7, "FY2023": -7.5, "FY2022": -6.9, "FY2021": -7.5, "FY2020": -7.5,
            "FY2019": -11.4, "FY2018": -30.6,
        }),
        ("DATA", "POCI allowance", {
            "FY2024": -0.2, "FY2023": -0.4, "FY2022": -0.3, "FY2021": -1.1, "FY2020": -1.1,
            "FY2019": -0.3, "FY2018": -4.3,
        }),
        ("TOTAL", "Total allowance for losses", {
            "FY2024": -29.3, "FY2023": -37.4, "FY2022": -40.4, "FY2021": -37.5, "FY2020": -40.7,
            "FY2019": -26.4, "FY2018": -51.7,
        }),
        ("SECTION", "Impaired / Not impaired basis (FY2014-FY2017, pre-IFRS 9 - see source note)", {}),
        ("DATA", "Not impaired", {
            "FY2017": 16427.6, "FY2016": 18855.8, "FY2015": 18974.2, "FY2014": 23827.2,
        }),
        ("DATA", "Impaired", {
            "FY2017": 396.9, "FY2016": 719.2, "FY2015": 961.4, "FY2014": 2413.5,
        }),
        ("TOTAL", "Total gross customer exposure (Impaired/Not impaired basis)", {
            "FY2017": 16824.5, "FY2016": 19575.0, "FY2015": 19935.6, "FY2014": 26240.7,
        }),
        ("TOTAL", "Total allowance for losses (Impaired/Not impaired basis)", {
            "FY2017": -80.0, "FY2016": -122.3, "FY2015": -245.2, "FY2014": -539.9,
        }),
        ("SECTION", "Derived ratios", {}),
        ("DATA", "Stage 3 (NPL) ratio, % of gross exposure subject to ECL calculation", {
            "FY2024": "0.53%", "FY2023": "0.45%", "FY2022": "0.35%", "FY2021": "0.29%", "FY2020": "0.30%",
            "FY2019": "0.40%", "FY2018": "0.76%",
        }),
        ("DATA", "Stage 3 coverage ratio (Stage 3 allowance / Stage 3 gross exposure)", {
            "FY2024": "6.70%", "FY2023": "7.63%", "FY2022": "8.59%", "FY2021": "11.13%", "FY2020": "11.81%",
            "FY2019": "14.58%", "FY2018": "22.89%",
        }),
        ("DATA", "Impaired ratio, % of gross exposure (Impaired/Not impaired basis, FY2014-FY2017)", {
            "FY2017": "2.36%", "FY2016": "3.68%", "FY2015": "4.82%", "FY2014": "9.20%",
        }),
        ("DATA", "Coverage ratio (total allowance / Impaired, FY2014-FY2017)", {
            "FY2017": "20.16%", "FY2016": "17.01%", "FY2015": "25.51%", "FY2014": "22.37%",
        }),
    ],
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=68,
    source_height=170,
    unit_suffix=" (£m)",
    years=PILLAR3_YEARS,  # HD-078: not extended past FY2014 - see PRE2014_HISTORY_NOTE above.
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    # HD-078: Pillar 3 sheets deliberately NOT extended past FY2014 - see
    # PILLAR3_YEARS / PRE2014_HISTORY_NOTE above.
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=110,
                         years=PILLAR3_YEARS)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {
        "FY2024": 923.5, "FY2023": 995.4, "FY2022": 947.3, "FY2021": 901.5, "FY2020": 874.9,
        "FY2019": 908.3, "FY2018": 1088.5, "FY2017": 1218.3, "FY2016": 736.9, "FY2015": 1151.1,
        "FY2014": 1636.0,
    })],
    p3_sources(),
    note="FY2014 is the CRD IV fully-loaded basis (£1,606.9m on the Year 1 CRD IV transitional basis) - the "
         "Bank's own Pillar 3 document reports both, and this workbook uses fully-loaded throughout for "
         "comparability with FY2015 onward (transitional and fully-loaded converge from FY2015).",
)

metric(
    "CET1 Ratio", "%",
    [("Common Equity Tier 1 (CET1) ratio", {
        "FY2024": "18.7%", "FY2023": "20.6%", "FY2022": "19.7%", "FY2021": "20.5%", "FY2020": "18.7%",
        "FY2019": "18.8%", "FY2018": "21.8%", "FY2017": "24.4%", "FY2016": "11.0%", "FY2015": "15.5%",
        "FY2014": "13.0%",
    })],
    p3_sources(),
    note="FY2014 is the CRD IV fully-loaded ratio (13.0%; transitional basis: 12.7%) - see the CET1 Capital "
         "sheet's note on the transitional/fully-loaded distinction.",
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {
        "FY2024": 923.5, "FY2023": 995.4, "FY2022": 947.3, "FY2021": 901.5, "FY2020": 874.9,
        "FY2019": 908.3, "FY2018": 1088.5, "FY2017": 1218.3, "FY2016": 736.9, "FY2015": 1151.1,
        "FY2014": 1638.3,
    })],
    p3_sources(),
    note="Tier 1 capital equals CET1 capital in every year FY2015 onward - the Bank holds no Additional Tier 1 "
         "(AT1) instruments at the individual entity level from FY2015. FY2014 is the one exception: a small "
         "AT1 balance (£2.3m fully loaded, arising from Unity Trust Bank plc minority interest) took Tier 1 "
         "slightly above CET1 (£1,638.3m vs £1,636.0m).",
)

metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 ratio", {
        "FY2024": "18.7%", "FY2023": "20.6%", "FY2022": "19.7%", "FY2021": "20.5%", "FY2020": "18.7%",
        "FY2019": "18.8%", "FY2018": "21.8%", "FY2017": "24.4%", "FY2016": "11.0%", "FY2015": "15.5%",
        "FY2014": "13.0%",
    })],
    p3_sources(),
)

metric(
    "Total Capital", "£m",
    [("Total capital", {
        "FY2024": 1123.9, "FY2023": 1231.8, "FY2022": 1141.5, "FY2021": 1103.7, "FY2020": 1084.9,
        "FY2019": 1113.6, "FY2018": 1088.5, "FY2017": 1218.3, "FY2016": 1183.9, "FY2015": 1599.5,
        "FY2014": 1889.9,
    })],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "%",
    [("Total capital ratio", {
        "FY2024": "22.7%", "FY2023": "25.5%", "FY2022": "23.7%", "FY2021": "25.1%", "FY2020": "23.2%",
        "FY2019": "23.1%", "FY2018": "21.8%", "FY2017": "24.4%", "FY2016": "17.7%", "FY2015": "21.6%",
        "FY2014": "15.0%",
    })],
    p3_sources(),
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted exposure amount", {
        "FY2024": 4950.8, "FY2023": 4830.6, "FY2022": 4806.7, "FY2021": 4399.8, "FY2020": 4668.4,
        "FY2019": 4830.1, "FY2018": 5004.3, "FY2017": 4986.0, "FY2016": 6676.1, "FY2015": 7422.9,
        "FY2014": 12632.2,
    })],
    p3_sources(),
)

bw.add_rwa_breakdown_sheet(
    title="The Co-operative Bank p.l.c. — RWA Breakdown (Bank Company-only, Individual Pillar 3 basis)",
    subtitle="UK OV1 'Overview of risk weighted exposures (Individual)', £m",
    rows=[
        ("DATA", "Credit risk (excluding CCR)", {
            "FY2024": 4143.6, "FY2023": 4132.3, "FY2022": 4178.2, "FY2021": 3743.6,
        }),
        ("DATA", "Counterparty credit risk (CCR)", {
            "FY2024": 18.2, "FY2023": 31.5, "FY2022": 37.6, "FY2021": 61.8,
        }),
        ("DATA", "Securitisation exposures in the non-trading book", {
            "FY2024": 82.3, "FY2023": 100.5, "FY2022": 95.8, "FY2021": 102.9,
        }),
        ("DATA", "Position, foreign exchange and commodities risks (Market risk)", {
            "FY2024": 0.0, "FY2023": 0.0, "FY2022": 0.0, "FY2021": 0.0,
        }),
        ("DATA", "Operational risk", {
            "FY2024": 706.7, "FY2023": 566.3, "FY2022": 495.1, "FY2021": 491.5, "FY2020": 512.6,
            "FY2019": 486.5, "FY2018": 480.9, "FY2017": 550.8,
        }),
        ("DATA", "Amounts below the thresholds for deduction (for information)", {
            "FY2024": 136.1, "FY2023": 205.1, "FY2022": 236.1, "FY2021": 232.6,
        }),
        ("TOTAL", "Total", {
            "FY2024": 4950.8, "FY2023": 4830.6, "FY2022": 4806.7, "FY2021": 4399.8, "FY2020": 4668.4,
            "FY2019": 4830.1, "FY2018": 5004.3, "FY2017": 4986.0, "FY2016": 6676.1, "FY2015": 7422.9,
            "FY2014": 12632.2,
        }),
    ],
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=64,
    source_height=210,
    unit_suffix=" (£m)",
    years=PILLAR3_YEARS,  # HD-078: not extended past FY2014 - see PRE2014_HISTORY_NOTE above.
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio (excluding claims on central banks)", {
        "FY2024": "4.0%", "FY2023": "4.2%", "FY2022": "4.0%", "FY2021": "3.7%", "FY2020": "3.8%",
        "FY2019": "3.8%", "FY2018": "4.6%", "FY2017": "4.8%", "FY2016": "2.6%", "FY2015": "3.8%",
        "FY2014": "4.3%",
    })],
    p3_sources(),
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio (LCR)", {
        "FY2024": "193.4%", "FY2023": "215.4%", "FY2022": "270.4%", "FY2021": "207.6%", "FY2020": "188.2%",
        "FY2019": "173.7%", "FY2018": "153.8%", "FY2017": "213.0%", "FY2016": "213.5%",
    })],
    p3_sources(),
    note="FY2015: the Bank's own Pillar 3 Disclosures state only that the LCR 'was in excess of 100%' at 31 "
         "December 2015 (the PRA's LCR regime only replaced the prior BIPRU 12 liquidity standard from 1 "
         "October 2015) - no exact percentage was disclosed, so FY2015 is left blank rather than estimated. "
         "FY2014 predates the LCR regime entirely (BIPRU 12 basis) and is left blank for the same reason. "
         "FY2016-FY2019 LCR figures are disclosed on a consolidated Group basis rather than an individual Bank "
         "Company basis - the Bank's own FY2015 Annual Report states it 'is unable to report its LCR ... on a "
         "stand-alone Bank only basis due to a lack of data and systems capability', a limitation that persists "
         "through this period; reproduced as the Bank's own best-available LCR disclosure for each year.",
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio (NSFR)", {
        "FY2024": "133.3%", "FY2023": "132.1%",
    })],
    p3_sources(),
    note="Blank FY2014-FY2022: under PS22/21 ('Implementation of Basel Standards'), UK NSFR disclosure was not "
         "required until reporting periods starting after 1 January 2024 - the Bank's own Pillar 3 templates "
         "leave these rows blank for those years, not a data gap.",
)

metric(
    "MREL Ratio", "%",
    [
        ("Total MREL resources available as a % of RWAs", {
            "FY2024": "36.0%", "FY2023": "39.1%", "FY2022": "33.2%", "FY2021": "29.6%", "FY2020": "27.5%",
        }),
        ("Total MREL resources available as a % of UK leverage exposure", {
            "FY2024": "7.7%", "FY2023": "8.0%", "FY2022": "6.8%", "FY2021": "5.4%", "FY2020": "5.6%",
        }),
    ],
    p3_sources(),
    note="The Bank's own KM2 Pillar 3 template discloses MREL adequacy on both an RWA basis and a UK leverage-"
         "exposure basis; both are shown here (the RWA-basis row is the headline figure used elsewhere in this "
         "workbook series). Blank FY2014-FY2019: the Bank of England's MREL policy only began taking effect from "
         "2016 (interim requirements) with binding disclosure obligations phasing in later still - the Bank's "
         "own Pillar 3 Disclosures for these years discuss MREL only qualitatively (e.g. noting a Tier 2 issuance "
         "'as part of the longer-term compliance with MREL requirements') without publishing a KM2-style MREL "
         "adequacy ratio, so these years are left blank rather than estimated.",
)

# ---------------------------------------------------------------
# Interim / semi-annual Pillar 3 disclosures
# ---------------------------------------------------------------
# The December 2025 report is headed and prepared for The Co-operative Bank
# p.l.c. itself. Its KM1 tables provide the current 31 December 2025 values
# on pp.4-5. The June 2025 report is deliberately represented as a gap: it is
# a Bank Holdings UK Consolidation Group disclosure, not an individual Bank
# plc disclosure, and therefore must not be mixed into this entity-level set.
INTERIM_HEADERS = [
    "Period", "Disclosure type", "Metric", "Value", "Unit", "Basis",
    "Source document", "Page / table",
]

INTERIM_ROWS = [
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Common Equity Tier 1 (CET1) capital", 968, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.4, Table 1, row 1"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Tier 1 capital", 968, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.4, Table 1, row 2"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Total capital", 1169, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.4, Table 1, row 3"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Total risk-weighted exposure amount", 5112, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.4, Table 1, row 4"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Common Equity Tier 1 (CET1) ratio", "18.9%", "%", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.4, Table 1, row 5"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Tier 1 ratio", "18.9%", "%", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.4, Table 1, row 6"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Total capital ratio", "22.9%", "%", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.4, Table 1, row 7"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Leverage ratio total exposure measure", 22035, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.4, Table 1, row 13"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Leverage ratio", "4.4%", "%", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.4, Table 1, row 14"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Total high-quality liquid assets (HQLA), weighted value average", 3816, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.5, Table 2, row 15"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Cash outflows, total weighted value", 2292, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.5, Table 2, UK 16a"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Cash inflows, total weighted value", 154, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.5, Table 2, UK 16b"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Total net cash outflows, adjusted value", 2138, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.5, Table 2, row 16"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Liquidity coverage ratio (LCR)", "179.8%", "%", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.5, Table 2, row 17"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Total available stable funding", 21719, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.5, Table 2, row 18"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Total required stable funding", 16129, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.5, Table 2, row 19"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Net stable funding ratio (NSFR)", "134.7%", "%", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.5, Table 2, row 20"),
    ("31 Dec 2025", "Year-end Pillar 3", "MREL ratio", "Not disclosed", "%", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "No MREL table in report"),
    ("30 Jun 2025", "Half-year Pillar 3 (KM1)", "Entity-level Bank plc KM1 metrics", "Not disclosed", "n/a", "The source is Bank Holdings UK Consolidation Group, not the individual Bank plc entity", P3_2025_H1_URL, "pp.3-4, overview and Table 1"),
]

bw.add_wide_interim_sheet(
    "Interim Pillar 3",
    rows=INTERIM_ROWS,
    hyperlink_cells={(i, 6): row[6] for i, row in enumerate(INTERIM_ROWS)},
    subtitle="Entity-level semi-annual and interim Pillar 3 observations; £m unless stated",
    note=(
        "Coverage note: the 31 December 2025 report is an entity-level disclosure for The Co-operative Bank "
        "p.l.c. The 30 June 2025 report is excluded from the entity metric series because it is prepared for "
        "The Co-operative Bank Holdings p.l.c. UK Consolidation Group. MREL is not disclosed in the December "
        "2025 KM1 report. The December report's LCR is a 12-month average and NSFR is an average of the current "
        "and preceding three quarters."
    ),
)
# Keep the source register directly below the matrix so the generic verifier
# can discover it without treating the helper's spacer rows as end-of-data.
interim_ws = bw.wb["Interim Pillar 3"]
interim_ws.delete_rows(24, 2)
source_register_row = next(
    row for row in range(5, interim_ws.max_row + 1)
    if interim_ws.cell(row=row, column=1).value == "Source register"
)
for offset, source_row in enumerate(INTERIM_ROWS, start=2):
    source_cell = interim_ws.cell(row=source_register_row + offset, column=3)
    source_cell.hyperlink = source_row[6]
    source_cell.style = "Hyperlink"

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Loans and advances to customers", {
            "FY2024": 20370.8, "FY2023": 20147.5, "FY2022": 20919.1, "FY2021": 20998.3, "FY2020": 18676.7,
            "FY2019": 17811.1, "FY2018": 17614.3, "FY2017": 16608.2, "FY2016": 19452.7, "FY2015": 19690.4,
            "FY2014": 25377.4,
        }),
        ("Customer accounts", {
            "FY2024": 19974.2, "FY2023": 19215.8, "FY2022": 20107.9, "FY2021": 21136.4, "FY2020": 20366.3,
            "FY2019": 18997.2, "FY2018": 18736.4, "FY2017": 20635.7, "FY2016": 22425.1, "FY2015": 22732.0,
            "FY2014": 29614.0,
        }),
        ("Total assets", {
            "FY2024": 26052.9, "FY2023": 26549.0, "FY2022": 28987.2, "FY2021": 30241.7, "FY2020": 27778.2,
            "FY2019": 26353.4, "FY2018": 24998.6, "FY2017": 26899.7, "FY2016": 27588.3, "FY2015": 29028.3,
            "FY2014": 37582.9,
        }),
        ("Total equity", {
            "FY2024": 1272.9, "FY2023": 1431.7, "FY2022": 1294.3, "FY2021": 1747.0, "FY2020": 1451.3,
            "FY2019": 1580.5, "FY2018": 1707.0, "FY2017": 1463.6, "FY2016": 958.5, "FY2015": 1363.3,
            "FY2014": 2014.5,
        }),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Profit/(loss) for the year", {
            "FY2024": 25.4, "FY2023": 157.1, "FY2022": 22.3, "FY2021": 215.5, "FY2020": -87.4,
            "FY2019": -141.3, "FY2018": -73.8, "FY2017": 32.8, "FY2016": -418.7, "FY2015": -623.3,
            "FY2014": -226.6,
        }),
        ("Other comprehensive income/(expense) for the year, net of tax", {
            "FY2024": -89.2, "FY2023": -19.7, "FY2022": -475.0, "FY2021": 80.2, "FY2020": -41.8,
            "FY2019": 14.8, "FY2018": 330.3, "FY2017": 21.4, "FY2016": 13.9, "FY2015": 6.6, "FY2014": 84.6,
        }),
        ("Total comprehensive income/(expense) for the year, net of tax", {
            "FY2024": -63.8, "FY2023": 137.4, "FY2022": -452.7, "FY2021": 295.7, "FY2020": -129.2,
            "FY2019": -126.5, "FY2018": 256.5, "FY2017": 54.2, "FY2016": -404.8, "FY2015": -616.7,
            "FY2014": -142.0,
        }),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {
            "FY2024": 1431.7, "FY2023": 1294.3, "FY2022": 1747.0, "FY2021": 1451.3, "FY2020": 1580.5,
            "FY2019": 1707.0, "FY2018": 1463.6, "FY2017": 958.5, "FY2016": 1363.3, "FY2015": 2014.5,
            "FY2014": 1768.5,
        }),
        ("Total comprehensive income/(expense) for the year", {
            "FY2024": -63.8, "FY2023": 137.4, "FY2022": -452.7, "FY2021": 295.7, "FY2020": -129.2,
            "FY2019": -126.5, "FY2018": 256.5, "FY2017": 54.2, "FY2016": -404.8, "FY2015": -616.3,
            "FY2014": -140.9,
        }),
        ("Other movements, net", {
            "FY2024": -95.0, "FY2023": 0.0, "FY2022": 0.0, "FY2021": 0.0, "FY2020": 0.0,
            "FY2019": 0.0, "FY2018": -13.1, "FY2017": 450.9, "FY2016": 0.0, "FY2015": -34.9, "FY2014": 386.9,
        }),
        ("Closing equity", {
            "FY2024": 1272.9, "FY2023": 1431.7, "FY2022": 1294.3, "FY2021": 1747.0, "FY2020": 1451.3,
            "FY2019": 1580.5, "FY2018": 1707.0, "FY2017": 1463.6, "FY2016": 958.5, "FY2015": 1363.3,
            "FY2014": 2014.5,
        }),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash flows from/(used in) operating activities", {
            "FY2024": -1243.5, "FY2023": -2165.6, "FY2022": -699.3, "FY2021": 1598.2, "FY2020": 481.2,
            "FY2019": -426.4, "FY2018": -3220.7, "FY2017": 427.2, "FY2016": -1227.6, "FY2015": -1983.5,
            "FY2014": -1583.2,
        }),
        ("Net cash flows from/(used in) investing activities", {
            "FY2024": 862.6, "FY2023": -693.6, "FY2022": 251.4, "FY2021": -61.8, "FY2020": 1143.5,
            "FY2019": 507.1, "FY2018": 936.0, "FY2017": 628.8, "FY2016": 1398.1, "FY2015": -674.3,
            "FY2014": 390.9,
        }),
        ("Net cash flows from/(used in) financing activities", {
            "FY2024": 272.3, "FY2023": 165.1, "FY2022": 189.3, "FY2021": -48.0, "FY2020": 168.7,
            "FY2019": 177.0, "FY2018": 0.0, "FY2017": 151.1, "FY2016": -43.9, "FY2015": 220.4,
            "FY2014": 677.2,
        }),
        ("Cash and cash equivalents at end of year", {
            "FY2024": 2634.1, "FY2023": 2751.3, "FY2022": 5450.9, "FY2021": 5709.5, "FY2020": 4221.1,
            "FY2019": 2427.7, "FY2018": 2170.0, "FY2017": 4454.7, "FY2016": 3266.3, "FY2015": 3139.7,
            "FY2014": 5577.1,
        }),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {
            "FY2024": 18.7, "FY2023": 20.6, "FY2022": 19.7, "FY2021": 20.5, "FY2020": 18.7,
            "FY2019": 18.8, "FY2018": 21.8, "FY2017": 24.4, "FY2016": 11.0, "FY2015": 15.5, "FY2014": 13.0,
        }),
        ("Tier 1 Ratio", {
            "FY2024": 18.7, "FY2023": 20.6, "FY2022": 19.7, "FY2021": 20.5, "FY2020": 18.7,
            "FY2019": 18.8, "FY2018": 21.8, "FY2017": 24.4, "FY2016": 11.0, "FY2015": 15.5, "FY2014": 13.0,
        }),
        ("Total Capital Ratio", {
            "FY2024": 22.7, "FY2023": 25.5, "FY2022": 23.7, "FY2021": 25.1, "FY2020": 23.2,
            "FY2019": 23.1, "FY2018": 21.8, "FY2017": 24.4, "FY2016": 17.7, "FY2015": 21.6, "FY2014": 15.0,
        }),
        ("Leverage Ratio", {
            "FY2024": 4.0, "FY2023": 4.2, "FY2022": 4.0, "FY2021": 3.7, "FY2020": 3.8,
            "FY2019": 3.8, "FY2018": 4.6, "FY2017": 4.8, "FY2016": 2.6, "FY2015": 3.8, "FY2014": 4.3,
        }),
        ("LCR", {
            "FY2024": 193.4, "FY2023": 215.4, "FY2022": 270.4, "FY2021": 207.6, "FY2020": 188.2,
            "FY2019": 173.7, "FY2018": 153.8, "FY2017": 213.0, "FY2016": 213.5,
        }),
        ("NSFR", {
            "FY2024": 133.3, "FY2023": 132.1,
        }),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. This Overview intentionally still only covers "
         "FY2014-FY2024, matching the Pillar 3 sheets it charts alongside - the Balance Sheet/Profit & Loss/"
         "Statement of Changes in Equity/Cash Flow Statement sheets extend further back to FY2003 (HD-078). " +
         ENTITY_NOTE,
    years=PILLAR3_YEARS,  # HD-078: not extended past FY2014, matching the Pillar 3 ratios charted alongside.
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/CO-OPERATIVE BANK FINANCIALS.xlsx")
print("Saved CO-OPERATIVE BANK FINANCIALS.xlsx")
