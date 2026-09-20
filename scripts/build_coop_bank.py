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
    # HD-078 follow-up (2026-09-07): FY2002-FY1991 extended further still, sourced
    # entirely from each year's own Companies House filing (Balance Sheet and
    # Statement of Changes in Equity only - see HD078_1991_2002_NOTE below for
    # full methodology, including why Cash Flow Statement and Profit & Loss are
    # NOT extended for this range).
    "FY2002", "FY2001", "FY2000", "FY1999", "FY1998", "FY1997", "FY1996",
    "FY1995", "FY1994", "FY1993", "FY1992", "FY1991",
    # HD-078 follow-up (2026-09-07): FY1990-FY1981 extended further still, sourced
    # entirely from each year's own Companies House filing (Balance Sheet and
    # Statement of Changes in Equity only - see HD078_1981_1990_NOTE below for full
    # methodology, including why Cash Flow Statement and Profit & Loss are NOT
    # extended for this range, and why no true Cash Flow Statement exists at all
    # for this era - see below).
    "FY1990", "FY1989", "FY1988", "FY1987", "FY1986",
    "FY1985", "FY1984", "FY1983", "FY1982", "FY1981",
    # HD-078 follow-up (2026-09-07): FY1980-FY1972 extended further still - the
    # documented hard floor (incorporated 5 Oct 1970; earliest filed accounts are
    # for the year ended 13 Jan 1973, whose own comparative column is only a
    # 26-week stub period, not a full prior year - see HD078_1972_1980_NOTE below
    # for full methodology, including why Cash Flow Statement and Profit & Loss
    # (Bank Company-only basis) are NOT extended for this range).
    "FY1980", "FY1979", "FY1978", "FY1977", "FY1976",
    "FY1975", "FY1974", "FY1973", "FY1972",
]  # most recent first
# Pillar 3, Asset Quality and RWA Breakdown sheets intentionally still only use
# the first 11 years above (FY2024-FY2014) - see PILLAR3_YEARS.
PILLAR3_YEARS = YEARS[:11]
YEAR_LABEL = {y: y for y in YEARS}

# KM1-011: the KM1 Key Metrics sheet spans FY2025-FY2020 on its own, which is
# neither YEARS nor PILLAR3_YEARS. FY2025 is one year NEWER than anything else
# in this workbook: the Bank's December 2025 Pillar 3 is published, but the
# FY2025 Annual Report that every statement sheet depends on is not reflected
# here yet, so FY2025 is carried only on the sheet whose own source document
# supports it rather than added to YEARS (which would open a blank FY2025
# column on all four statement sheets). FY2020 is included because the 2022
# edition's KM1 prints five half-year columns reaching back to 31 Dec 2020.
KM1_YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020"]
YEAR_LABEL["FY2025"] = "FY2025"

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
P3_2023_URL = "https://www.co-operativebank.co.uk/pdfs/bank/investorrelations/2023-pillar-3-disclosures.pdf"
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

# HD-078 follow-up (2026-09-07): FY2002-FY1991 statutory-statement sources, each
# year's own Companies House filing (same domain confirmed by HD-078 to hold no
# pre-2014 Annual Reports).
AR2002_CH_URL = f"{CH_BASE}/MTEyMTAwMDczYWRpcXprY3g/document?format=pdf&download=0"  # accounts made up to 11 Jan 2003
AR2001_CH_URL = f"{CH_BASE}/MzE5OTExMDdhZGlxemtjeA/document?format=pdf&download=0"  # accounts made up to 12 Jan 2002
AR2000_CH_URL = f"{CH_BASE}/NjIxOTc0MTVhZGlxemtjeA/document?format=pdf&download=0"  # accounts made up to 13 Jan 2001
AR1999_CH_URL = f"{CH_BASE}/MTI2NTUyNTk5YWRpcXprY3g/document?format=pdf&download=0"  # accounts made up to 8 Jan 2000
AR1998_CH_URL = f"{CH_BASE}/MTM5OTg0MTEyYWRpcXprY3g/document?format=pdf&download=0"  # accounts made up to 9 Jan 1999
AR1997_CH_URL = f"{CH_BASE}/MTA1NzY2NjU4YWRpcXprY3g/document?format=pdf&download=0"  # accounts made up to 10 Jan 1998
AR1996_CH_URL = f"{CH_BASE}/MTM2Nzk5NjI5YWRpcXprY3g/document?format=pdf&download=0"  # accounts made up to 11 Jan 1997
AR1995_CH_URL = f"{CH_BASE}/MzQwNzE1MTJhZGlxemtjeA/document?format=pdf&download=0"  # accounts made up to 13 Jan 1996
AR1994_CH_URL = f"{CH_BASE}/MTQ5NDQxMjA4YWRpcXprY3g/document?format=pdf&download=0"  # accounts made up to 14 Jan 1995
AR1993_CH_URL = f"{CH_BASE}/OTQ3NzQwNzNhZGlxemtjeA/document?format=pdf&download=0"  # accounts made up to 8 Jan 1994 (also FY1992 comparative)
AR1991_CH_URL = f"{CH_BASE}/OTk0ODQ2MjRhZGlxemtjeA/document?format=pdf&download=0"  # accounts made up to 11 Jan 1992

# HD-078 follow-up (2026-09-07): FY1990-FY1981 statutory-statement sources, each
# year's own Companies House filing. Confirmed via each year's own filed report's
# table of contents that no true Cash Flow Statement exists for any of these years
# (UK companies were not required to publish one until FRS 1, effective for
# accounting periods beginning on/after 23 March 1992) - only a structurally
# different "Statement of Source and Application of Funds" (SSAP 10) appears, and
# it is not force-mapped onto the Cash Flow Statement sheet's row structure.
# GA-024 (2026-09-19): THESE CONSTANTS ARE NAMED BY THE CALENDAR YEAR OF THE
# JANUARY YEAR-END, NOT BY FISCAL YEAR - unlike AR1991+ above, which are named by
# fiscal year. AR<n> is the accounts made up to early January <n>, i.e. FY<n-1>.
# Every date below is the one printed on the document itself and matches the
# Companies House filing-history description (1985+). The FY1990 filing (made up
# to 12 Jan 1991) had never been used here and is FY1990_CH_URL.
FY1990_CH_URL = f"{CH_BASE}/MTQyMTMwNTk0YWRpcXprY3g/document?format=pdf&download=0"  # full group accounts made up to 12 Jan 1991 = FY1990 (filed 20 May 1991)
AR1990_CH_URL = f"{CH_BASE}/NDE5NjQxMjFhZGlxemtjeA/document?format=pdf&download=0"  # accounts made up to 13 Jan 1990 = FY1989
AR1989_CH_URL = f"{CH_BASE}/NDk0ODQ2MjdhZGlxemtjeA/document?format=pdf&download=0"  # accounts made up to 14 Jan 1989 = FY1988
AR1988_CH_URL = f"{CH_BASE}/MzAwNDIyMjdhZGlxemtjeA/document?format=pdf&download=0"  # accounts made up to 9 Jan 1988 = FY1987
AR1987_CH_URL = f"{CH_BASE}/NTUxNzgzNDBhZGlxemtjeA/document?format=pdf&download=0"  # accounts made up to 10 Jan 1987 = FY1986
AR1986_CH_URL = f"{CH_BASE}/NTg3OTI0NzVhZGlxemtjeA/document?format=pdf&download=0"  # accounts made up to 11 Jan 1986 = FY1985 ('Financial Statement 1985' on its own cover)
AR1985_CH_URL = f"{CH_BASE}/MjAyNDY1Mjk3MmFkaXF6a2N4/document?format=pdf&download=0"  # accounts made up to 12 Jan 1985 = FY1984
AR1984_CH_URL = f"{CH_BASE}/MjAyNDY1Mjk3M2FkaXF6a2N4/document?format=pdf&download=0"  # accounts made up to 14 Jan 1984 = FY1983
AR1983_CH_URL = f"{CH_BASE}/MjAyNDY1Mjk3NGFkaXF6a2N4/document?format=pdf&download=0"  # accounts made up to 8 Jan 1983 = FY1982
AR1982_CH_URL = f"{CH_BASE}/MjAyNDY1Mjk2OWFkaXF6a2N4/document?format=pdf&download=0"  # accounts made up to 9 Jan 1982 = FY1981
AR1981_CH_URL = f"{CH_BASE}/MjAyNDY1Mjk3MGFkaXF6a2N4/document?format=pdf&download=0"  # accounts made up to 10 Jan 1981 = FY1980

# HD-078 (2026-09-07): FY1980-FY1972, the workbook's genuine hard floor - see HD078_1972_1980_NOTE
# below for full methodology (why P&L/Cash Flow Statement are not extended the same way as FY1990-
# FY1981, the FY1972 26-week-stub floor confirmation, the FY1973 capitalisation issue, and the
# FY1979 SSAP15/bad-debt restatement).
AR1980_CH_URL = f"{CH_BASE}/MjAyNDY1Mjk3MWFkaXF6a2N4/document?format=pdf&download=0"  # accounts made up to early Jan 1980 (FY1979)
AR1979_CH_URL = f"{CH_BASE}/MjAyNDY1Mjk2NmFkaXF6a2N4/document?format=pdf&download=0"  # accounts made up to early Jan 1979 (FY1978)
AR1978_CH_URL = f"{CH_BASE}/MjAyNDY1Mjk2N2FkaXF6a2N4/document?format=pdf&download=0"  # accounts made up to 14 Jan 1978 (FY1977)
AR1977_CH_URL = f"{CH_BASE}/MjAyNDY1Mjk2OGFkaXF6a2N4/document?format=pdf&download=0"  # accounts made up to early Jan 1977 (FY1976)
AR1976_CH_URL = f"{CH_BASE}/MjAyNDY1Mjk2NGFkaXF6a2N4/document?format=pdf&download=0"  # accounts made up to early Jan 1976 (FY1975)
AR1975_CH_URL = f"{CH_BASE}/MjAyNDY1Mjk2NWFkaXF6a2N4/document?format=pdf&download=0"  # accounts made up to early Jan 1975 (FY1974)
AR1974_CH_URL = f"{CH_BASE}/MjAyNDY1Mjk2MmFkaXF6a2N4/document?format=pdf&download=0"  # accounts made up to early Jan 1974 (FY1973) - the FY1973 capitalisation-issue year
AR1973_CH_URL = f"{CH_BASE}/MjAyNDY1Mjk2M2FkaXF6a2N4/document?format=pdf&download=0"  # accounts made up to 13 Jan 1973 (FY1972) - the workbook's earliest filed accounts; comparative column is only a 26-week stub (10 Jul 1971 - 8 Jan 1972), not a full prior year

# Full-length narrative research notes for the HD-078 pre-2014 extension effort
# (methodology, source-page detail, era-by-era reasoning) are preserved in git
# history and in this script's own comments near each affected row; the
# *_NOTE strings below are deliberately condensed before being folded into
# STATEMENTS_SOURCES, since that text is written into a single Excel cell
# subject to openpyxl's ~32,767-char hard limit (silent truncation past it -
# see HD-078 session log, 2026-09-07).
PRE2014_HISTORY_NOTE = (
    "PRE-2014 HISTORICAL DEPTH (HD-078, 2026-09-06): FY2003-FY2013 extends the "
    "four statutory-statement sheets back to FY2003 (HD-004's real statutory "
    "floor); Pillar 3/Asset Quality/RWA Breakdown stay FY2014-floored. Figures "
    "transcribed from each year's own scanned Companies House filing (co "
    "00990937) - co-operativebank.co.uk hosts nothing this old. Three eras:\n"
    "FY2009-FY2013 (IFRS, calendar year end): each Annual Report's own Bank "
    "balance sheet/cash flow/equity statements, individual-entity basis. "
    "s.408 Companies Act 2006 exemption taken every year except FY2013 (whose "
    "AR, amid the 2013 recapitalisation, voluntarily disclosed a full Bank "
    "income statement for FY2013 and FY2012 comparative - the only source for "
    "a standalone FY2012 income statement); FY2009-FY2011 show bottom-line "
    "profit + OCI movements only, as FY2017 onward.\n"
    "BRITANNIA MERGER (FY2009): Britannia Building Society transferred its "
    "engagements to the Bank 1 Aug 2009 - Total assets roughly double £16.4bn "
    "to £47.2bn; Equity sheet shows '+£811.2m Amounts arising on transfer of "
    "engagements'; Cash Flow shows a matching £889.6m acquired-cash inflow. "
    "Both are the Bank's own disclosed transaction figures, not restatements.\n"
    "FY2005-FY2008 (IFRS, pre-Britannia, 52/53-week year ending near 10 Jan "
    "the following calendar year, e.g. 'the 52 weeks to 13 January 2007'): "
    "headed by the calendar year the period substantially covers, per the "
    "Bank's own Basis of Preparation note. Presents a SORIE (pre-2009 "
    "predecessor to the Statement of Changes in Equity); smaller pre-"
    "Britannia balance sheet (~£11-16bn vs ~£27-38bn FY2014 onward).\n"
    "FY2003-FY2004 (UK GAAP, pre-IFRS transition, which first applies FY2005): "
    "Companies Act 1985 Sch. 9 bank format, no IFRS reserve categories, no OCI "
    "concept. No standalone Bank cash flow statement exists this era - the "
    "Cash Flow Statement sheet uses the CONSOLIDATED GROUP statement for "
    "FY2003-FY2004 only (flagged on that sheet); every other year there is "
    "Bank Company-only.\n"
    "Two genuine restatement discontinuities are shown as dedicated "
    "Statement of Changes in Equity rows rather than force-matched (same "
    "treatment as the FY2016/FY2017 restatement): (1) FY2012 closing Total "
    "equity per the Bank's own FY2012 AR (£1,629.1m) vs the FY2013 AR's own "
    "restated FY2012 comparative (£1,850.2m, £221.1m gap, cause not narrated "
    "by the source); (2) FY2013 closing Total equity per the Bank's own "
    "FY2013 AR (£1,777.3m) vs the FY2014 AR's own FY2013 comparative "
    "(£1,768.5m, £8.8m gap, within Cashflow hedging reserve/Retained "
    "earnings - likely a minor reclassification)."
)

HD078_1991_2002_NOTE = (
    "HD-078 FOLLOW-UP (2026-09-07): FY2002-FY1991 extends Balance Sheet and "
    "Statement of Changes in Equity ONLY (P&L/Cash Flow not extended, see "
    "below), 12 years below the FY2003 floor. Transcribed from each year's "
    "own scanned Companies House filing (co 00990937), except FY1992 - "
    "sourced from the FY1993 AR's own FY1992 comparative (cross-checked "
    "against FY1991's continuity, e.g. identical £75.0m subordinated Loan "
    "Stock). 34 years now on both extended sheets: FY2024-FY1991.\n"
    "P&L: SUPERSEDED 2026-09-19 - the s.230 note DOES state the Bank's own "
    "profit every year, and the P&L sheet now carries FY2002-FY1992.\n"
    "CASH FLOW NOT EXTENDED: FRS 1 only applies to periods beginning on/"
    "after 23 Mar 1992 - FY1991 instead presents an incompatible 'Statement "
    "of Source and Application of Funds' (SSAP 10). Separately, this "
    "workbook's own Cash Flow sheet doesn't yet reach past FY2012, so "
    "extending FY1991-2002 here would leave a disconnected island above an "
    "unexplained FY2003-2011 gap - self-skipped, closing that gap is a "
    "separate follow-up.\n"
    "FY1991 FORMAT: predates the Sch. 9 detail used FY1992+ - 'Liquid "
    "Assets' maps onto Cash/Items in course of collection/Loans to banks; "
    "'Certificates of Deposit'+'Investments' combine into Investment "
    "securities; 'Current, deposit and other accounts' (aggregate, one new "
    "one-off row - later years split Deposits by banks/Customer accounts); "
    "'Loan Stock' maps to Other borrowed funds (£75.0m, ties to FY1992); "
    "'Deferred Taxation' to Provisions. FY1991 Reserves (£51.6m) isn't "
    "split into share premium/retained earnings like every adjacent year - "
    "this workbook infers £8.8m/£42.8m (flagged as inferred, not "
    "disclosed). A ~£0.03m unresolved sub-total gap (degraded scan image) "
    "is absorbed by anchoring on the disclosed Total assets/liabilities "
    "figure (£2,572.6m) rather than a component sum; liabilities side ties "
    "exactly.\n"
    "EQUITY MOVEMENT ROWS (FY1992-2002): no Bank-only profit/dividends "
    "split is disclosed before the FY2001 AR introduced one, so FY1992-1999 "
    "and FY2002 show a single aggregate 'Net movement during the year' row "
    "(from the Balance Sheet's own opening/closing funds, not a fabricated "
    "split, as already used FY2004-2008); FY2000-2001 DO show the split, "
    "per the FY2001 AR's own Bank reconciliation.\n"
    "RESTATEMENT (FY2001/2002 boundary): FY2001 AR's own closing Bank "
    "shareholders' funds (£438.4m) vs FY2002 AR's own restated FY2001 "
    "comparative (£440.0m, £1.6m gap) - both transcribed as disclosed, not "
    "force-matched, consistent with the FY2016/2017 and FY2012/2013 "
    "restatement treatment elsewhere in this workbook."
)

HD078_1981_1990_NOTE = (
    "HD-078 FOLLOW-UP (2026-09-07): FY1990-FY1981 extends Balance Sheet and "
    "Statement of Changes in Equity ONLY (Cash Flow not extended, pre-FRS1; "
    "P&L extended 2026-09-19 on a GROUP basis - no Bank-only one exists). Transcribed "
    "from each year's own Companies House filing.\n"
    "FORMAT: FY1985-1990 continue FY1991's Sch. 9 mapping (see "
    "HD078_1991_2002_NOTE). FY1981-1984 predate the Companies Act 1985 "
    "(1948/1967 regime, coarser presentation) but map onto the same rows, "
    "reusing the 'Deposits by trustees of CWS employees' pension scheme "
    "(secured)' row (last appears FY1981).\n"
    "SHARE CAPITAL/PREFERENCE: one-off events, each shown as its own "
    "Equity-sheet movement row: ordinary share subdivision (14 Jul 1987, "
    "25.0m £1 shares -> 100.0m 25p) + Nov 1987 20.0m-share issue at par; "
    "earlier CWS issues at par (13.8m £1 shares, Dec 1984/Jan 1985, in "
    "FY1984; 3.2m £1 shares, Jan 1983, in FY1982); first preference issue "
    "(40.0m 8.48% cumulative redeemable £1 shares, Apr 1988), converted 23 "
    "Jun 1989 to 9.25% non-cumulative irredeemable, +20.0m more 31 May 1989 "
    "(total £60.0m into FY1991). Preference capital folds into the single "
    "'Share capital' Equity-sheet column; Balance Sheet shows it as its own "
    "'Preference share capital (non-equity)' row, FY1988-1990 only.\n"
    "SHARE PREMIUM: genuinely drifts £9.636m-£9.824m FY1983-1987 (immaterial "
    "at 1-decimal £m precision); FY1988-1990 use the £8.8m value consistent "
    "with FY1991+. FY1981/1982 have no disclosed share-premium sub-split "
    "anywhere (primary or comparative) - left undifferentiated within "
    "Retained earnings for those two years only.\n"
    "FY1984 RESERVES TRANSFER: £13.153m Reserves -> P&L account, funding a "
    "Group deferred-tax provision (Finance Act 1984), per that year's own "
    "Reserves note - folded into the FY1984 Equity movement row.\n"
    "FY1984 RESTATEMENT NOT CARRIED: FY1985's AR restates its FY1984 "
    "comparative (finance-lease/money-at-call reclassification); this "
    "workbook keeps FY1984's own originally-published figures, per its "
    "'own year primary source' convention throughout.\n"
    "FY1988 LIMITATION: liabilities-side detail wasn't independently "
    "re-captured at the same granularity as adjacent years - 'Current, "
    "deposit and other accounts (aggregate)' (£1,875.2m) is a residual "
    "(Total assets less Capital/Reserves, Loan Stock, Deferred Tax); ties "
    "exactly with this residual approach, same Total-assets-anchor "
    "precedent as FY1991.\n"
    "CURIOSITIES (source-disclosed, re-checked, not errors): 'Subsidiaries' "
    "column negative for FY1983 (-£1.8m); Associated Undertakings drops "
    "£15.4m (FY1987) to £17k (FY1988, near-nil pattern continues FY1992+); "
    "£3,192,000 Special Tax on Banking Deposits (Group extraordinary item, "
    "FY1981 windfall tax) doesn't affect any shown figure (no Bank-only P&L "
    "this year) - noted for context only.\n"
    "RECONCILIATION: Total assets = Total liabilities + Total equity ties "
    "exactly (or sub-£0.1m rounding) for all 10 years FY1990-1981, "
    "independently re-verified; Equity roll-forward ties at every boundary, "
    "opening anchor (At 31 Dec 1980, £41.6m) from the FY1981 AR's own "
    "FY1980 comparative."
)

HD078_1972_1980_NOTE = (
    "HD-078 FOLLOW-UP (2026-09-07): FY1980-FY1972 extends the Balance Sheet and "
    "Statement of Changes in Equity sheets ONLY, a further 9 years below the "
    "FY1991 floor - and reaches this workbook's genuine hard floor: the Bank was "
    "incorporated 5 October 1970 and its earliest filed accounts at Companies "
    "House are for the year ended 13 January 1973 (labelled FY1972). That "
    "filing's own Note 2 states its comparative column is 'for the 26 weeks' "
    "period from 10th July, 1971, to 8th January, 1972' - not a full prior year "
    "- tying to Note 1(a)'s statement that C.W.S.'s banking activities were "
    "vested in Co-operative Bank Limited on 10 July 1971; no earlier full "
    "accounting year exists to extend to. All 9 years transcribed from each "
    "year's own scanned Companies House filing (company 00990937).\n"
    "P&L NOT EXTENDED (Bank-only): no Bank Company-only income statement is "
    "presented at all, only a Consolidated Group one, carried in its own "
    "Group-basis section (extended to FY1991 on 2026-09-19).\n"
    "CASH FLOW NOT EXTENDED: predates SSAP 10 (1975) and FRS 1 (1992); where a "
    "Source and Application of Funds statement exists (FY1975+) its structure "
    "is incompatible with this sheet's row layout, same treatment as FY1991.\n"
    "ROW MAPPING: reuses the FY1991-2002 aggregated presentation (Liquid "
    "Assets sub-lines, Certificates of Deposit/Investments/Special Deposits "
    "combined into Investment securities, Customer and Other Accounts, "
    "Subsidiaries, Associated Companies, Fixed Assets). New one-off rows: "
    "'Deposits by trustees of CWS employees' pension scheme (secured)' "
    "(material every year); 'Proposed dividend' (FY1980 only). 'Subordinated "
    "Loans' (US $25m Floating Rate Capital Notes, first FY1979) maps onto "
    "Other borrowed funds; 'Deferred Taxation' onto Provisions (from FY1974).\n"
    "EQUITY/RESERVES: no formal Statement of Changes in Equity is filed this "
    "era - each year's own 'Reserves' note is reconstructed into a roll-"
    "forward, cross-validated against the Balance Sheet's own Reserves figure "
    "for all 9 years (ties exactly). Two genuine discontinuities shown as "
    "explicit rows: (1) FY1973 bonus/capitalisation issue - Ordinary share "
    "capital doubled £4.0m to £8.0m, funded by a £4.02m capitalisation of "
    "Reserves; (2) a FY1979-disclosed restatement of FY1978 closing Reserves "
    "from £21.563m (as originally reported) to £23.021m, +£1.458m combined for "
    "a SSAP 15 deferred-tax policy change plus a released general bad-debt "
    "provision, shown as its own 'Restatement' row."
)

# HD-078 follow-up (2026-09-19): the Bank's OWN-edition Financial Statements for
# FY2003-FY2011, hosted on co-operativebank.co.uk. These are born-digital,
# searchable PDFs (pdftotext returns 1,300-3,800 hits for " the ", so keyword
# search on them is trustworthy - unlike the Companies House scans above, which
# have no text layer at all and had to be OCR'd and then read off rendered page
# images). They are preferred over the Companies House filings for these years
# because several of the CH filings are a later year's edition carrying the year
# in question only as a comparative.
COOP_FS_BASE = ("https://www.co-operativebank.co.uk/pdfs/bank/investorrelations/"
                "financialresults/bank-financial-statement")
FS2011_URL = f"{COOP_FS_BASE}-2011.pdf"
FS2010_URL = f"{COOP_FS_BASE}-2010.pdf"
FS2009_URL = f"{COOP_FS_BASE}-2009.pdf"
FS2008_URL = f"{COOP_FS_BASE}-2008.pdf"
FS2007_URL = f"{COOP_FS_BASE}-2007.pdf"
FS2005_URL = f"{COOP_FS_BASE}-2005.pdf"
FS2004_URL = f"{COOP_FS_BASE}-2004.pdf"
FS2003_URL = f"{COOP_FS_BASE}-2003.pdf"
# NOTE: there is no usable FS2006_URL. The bank's own index page links
# .../bank-financial-statement-2006.pdf, but that path SERVES THE 2007 DOCUMENT -
# byte-identical (md5 d893321826b9d07d9ae47ab5ff978be1) to the -2007.pdf path, on
# both the /pdfs/ and /assets/pdf/ prefixes, and in the Wayback Machine's capture
# too, so it is a long-standing site-side error rather than a transient one.
# FY2006 therefore uses its own Companies House filing (AR2006_CH_URL) instead.

HD078_PL_1981_2011_NOTE = (
    "HD-078 FOLLOW-UP (2026-09-19) - CLOSING THE FY2011-FY1981 PROFIT & LOSS HOLE.\n"
    "Before this pass the P&L sheet was populated for FY1980-FY1972 and for "
    "FY2024-FY2012 and empty for the 31 years in between, with no statement in "
    "the cells saying why. Every one of those 31 years is now filled from a "
    "primary source. Two different things were found, and they are kept on "
    "separate rows because they are different measures:\n"
    "(1) FY2011-FY1992 - A BANK COMPANY-ONLY BOTTOM LINE DOES EXIST, and is "
    "independently disclosed. The Bank took the s.230 Companies Act 1985 "
    "exemption (from FY2006 onward its s.408 Companies Act 2006 successor) from "
    "presenting its own individual profit and loss account every year in this "
    "range - but that exemption REQUIRES the amount of the Group profit dealt "
    "with in the parent's own accounts to be stated in a note, and that note is "
    "present in all 20 editions. The earlier HD-078 pass left FY2003-FY2011 "
    "blank on the ground that a Bank-only profit would have to be backed out as "
    "a residual of the equity roll-forward; that premise was wrong - the figure "
    "is printed, and nothing below is derived, netted or back-solved.\n"
    "THE NOTE'S BASIS CHANGES TWICE, so the figures are carried on three rows, "
    "not one:\n"
    "  - FY2011-FY2005 'Group profit attributable to EQUITY shareholders dealt "
    "with in the accounts of The Co-operative Bank p.l.c.';\n"
    "  - FY2004-FY1999 'Group profit for the financial year attributable to "
    "SHAREHOLDERS...' (preference holders included);\n"
    "  - FY1998-FY1993 'Group profit attributable to ORDINARY shareholders...' "
    "(i.e. struck AFTER the preference dividend).\n"
    "The break between the second and third is arithmetically demonstrable and "
    "is NOT reconciled away: the FY1998 edition's note says £40,088,000 while "
    "the FY1999 edition restates that same comparative to £45,623,000, and the "
    "difference is exactly the £5,535,000 preference dividend printed in the "
    "FY1998 edition's own note 10 (60,000,000 9.25% non-cumulative irredeemable "
    "£1 preference shares). Each year below is its OWN edition's figure.\n"
    "FY1992 is the one exception and is flagged on its own row: FY1992's own "
    "filing was not retrieved, so its £472,000 comes from the FY1993 edition's "
    "own FY1992 comparative column - the same limitation the Balance Sheet "
    "sheet already records for FY1992.\n"
    "FY2004 RESTATEMENT (both figures disclosed, neither suppressed): FY2004's "
    "own edition (UK GAAP) states £88.0m; the FY2005 edition restates the same "
    "FY2004 comparative to £78.7m on first-time IFRS adoption. The workbook's "
    "own-edition convention keeps £88.0m on the sheet and records £78.7m here.\n"
    "FY2009 BRITANNIA MERGER: Britannia Building Society transferred its "
    "engagements to the Bank on 1 August 2009, roughly trebling the balance "
    "sheet. FY2009 and FY2010 are therefore NOT like-for-like with FY2008 and "
    "earlier, and the step up in this series should not be read as organic.\n"
    "Sources, each year from its own edition:\n"
    f"  FY2011 note 11 - {FS2011_URL}\n"
    f"  FY2010 note 11 - {FS2010_URL}\n"
    f"  FY2009 note 11 - {FS2009_URL}\n"
    f"  FY2008 note 10 - {FS2008_URL}\n"
    f"  FY2007 note 10 - {FS2007_URL}\n"
    f"  FY2006 note 9, p.67 (Companies House scan; see the FS2006 caveat above) - {AR2006_CH_URL}\n"
    f"  FY2005 note 9 - {FS2005_URL}\n"
    f"  FY2004 note 6 - {FS2004_URL}\n"
    f"  FY2003 note 6 - {FS2003_URL}\n"
    f"  FY2002 note 6, p.43 - {AR2002_CH_URL}\n"
    f"  FY2001 note 6, p.43 - {AR2001_CH_URL}\n"
    f"  FY2000 note 6, p.43 - {AR2000_CH_URL}\n"
    f"  FY1999 note 9, p.43 - {AR1999_CH_URL}\n"
    f"  FY1998 note 9, p.39 - {AR1998_CH_URL}\n"
    f"  FY1997 note 10, p.36 - {AR1997_CH_URL}\n"
    f"  FY1996 note 10, p.28 - {AR1996_CH_URL}\n"
    f"  FY1995 note 8, p.42 - {AR1995_CH_URL}\n"
    f"  FY1994 note 8, p.31 - {AR1994_CH_URL}\n"
    f"  FY1993 note 8, p.36 - {AR1993_CH_URL}\n"
    f"  FY1992 (FY1993 edition's comparative) - {AR1993_CH_URL}\n"
    "(2) FY1991-FY1981 - NO BANK COMPANY-ONLY INCOME STATEMENT AND NO s.230 "
    "NOTE EXIST. Every one of these 11 filings was OCR'd in full and the "
    "relevant pages read off rendered page images; the phrase 'dealt with in "
    "the accounts of The Co-operative Bank' appears nowhere before the FY1993 "
    "edition. What these editions DO print is a Consolidated (Group) Profit and "
    "Loss Account, plus a single Bank Company-only line at its foot, "
    "'Profits/(Losses) Retained - By The Bank'. Both are now on the sheet: the "
    "Group statement extends the existing FY1980-FY1972 Group block up to "
    "FY1991, and the Bank-only retained line has its own row. That retained "
    "line is a POST-DIVIDEND APPROPRIATION, not a profit for the year, so it is "
    "deliberately not written into the 'Profit/(loss) for the year' row.\n"
    "DOCUMENT DATING - READ THIS BEFORE RE-USING THE AR<year>_CH_URL "
    "CONSTANTS. The Bank's year end in this era was an early-January 52/53-week "
    "date, and each constant below was opened and dated from the statement's own "
    "printed dateline and column headings rather than from its name or from the "
    "Companies House description:\n"
    f"  FY1991 - 'year ended January 1992', columns 1991/1990, p.25 - {AR1991_CH_URL}\n"
    f"  FY1990 - 'for the year ended 12th January, 1991', columns 1990/1989, Consolidated P&L printed "
    f"p.23 (PDF p.25) - {FY1990_CH_URL}. This own-edition filing (filed 20 May 1991) was not located "
    f"before 2026-09-19 and FY1990 had been filled from the FY1991 edition's comparative column, which "
    f"RE-PRESENTS the year: it splits the own edition's single 'Operating (Loss)/Profit' (14,687) into "
    f"(14,041) plus a separate 'Unity Trust Bank plc and its subsidiaries' line (646), prints an "
    f"Exceptional Item line as a dash, and merges the preference dividend (5,535) into one 'Dividend' "
    f"line. FY1990 now carries the OWN edition (own-year-primary convention); every subtotal "
    f"is unchanged.\n"
    f"  FY1989 - 'for the year ended 13th January, 1990', columns 1989/1988, p.23 - {AR1990_CH_URL}\n"
    f"  FY1988 - 'for the year ended 14th January, 1989', columns 1988/1987, p.3 - {AR1989_CH_URL}\n"
    f"  FY1987 - 'for the year ended 9th January, 1988', columns 1987/1986, p.3 - {AR1988_CH_URL}\n"
    f"  FY1986 - 'for the year ended 10th January, 1987', columns 1986/1985 - {AR1987_CH_URL}\n"
    f"  FY1985 - 'for the year ended 11th January, 1986', columns 1985/1984, p.3 - {AR1986_CH_URL}\n"
    f"  FY1984 - 'for the year ended 12th January, 1985', columns 1984/1983, p.9 - {AR1985_CH_URL}\n"
    f"  FY1983 - 'for the year ended 14th January, 1984', columns 1983/1982, p.9 - {AR1984_CH_URL}\n"
    f"  FY1982 - 'for the year ended 8th January, 1983', columns 1982/1981, p.9 - {AR1983_CH_URL}\n"
    f"  FY1981 - 'for the year ended 9th January, 1982', columns 1981/1980, p.9 - {AR1982_CH_URL}\n"
    f"  FY1980 - 'for the year ended 10th January, 1981', columns 1980/1979, p.13 - {AR1981_CH_URL}\n"
    "That last line is the one to notice: AR1981_CH_URL holds the FY1980 "
    "statement, AR1982_CH_URL holds FY1981, and so on up the range - each "
    "constant holds the filing for the year ended in the January that names it, "
    "which is the PRECEDING fiscal year. The Balance Sheet/Statement of Changes "
    "in Equity citation block used to label these same constants one year later; "
    "that was corrected on 2026-09-19 (GA-024) after each document's own dateline "
    "was re-read and matched to its Companies House filing description. The "
    "FIGURES on those sheets were right throughout (e.g. Total assets FY1981 696.3 "
    "/ FY1982 816.1 / FY1983 905.4 tie to 696,331 / 816,072 / 905,414 in the "
    "9 Jan 1982, 8 Jan 1983 and 14 Jan 1984 filings).\n"
    "SIGN CONVENTION: these editions switch convention mid-range. Up to the "
    "FY1985 statement a deduction is printed unbracketed and an addition "
    "bracketed; from the FY1986 statement brackets mean a deduction. Every "
    "column above was settled by footing it to its own printed Retained "
    "Earnings total, not by reading the brackets.\n"
    "ONE ILLEGIBLE CELL: the FY1987 edition's 'Sovereign Debt Provisions' "
    "figure is physically damaged on the Companies House scan. It is carried as "
    "1.384 from the FY1988 edition's legible FY1987 comparative column, cited as "
    "a comparative. It was NOT inferred from the 15,684 / 14,300 subtotals "
    "printed either side of it, although those do agree with it.\n"
    "ONE FIGURE DELIBERATELY LEFT OUT: the FY1988 edition's FY1987 comparative "
    "also prints 'Profit attributable to Ordinary Shareholders 9,164' for "
    "FY1987, a line FY1987's own edition does not carry. It is recorded here "
    "rather than placed in an own-edition row.\n"
    "ONE NEW verify_workbook.py BLOCK MISMATCH, EXPECTED AND NOT A DATA "
    "ERROR: that script checks a TOTAL row against the sum of the DATA rows "
    "since the PREVIOUS TOTAL, and cannot carry a running subtotal forward. "
    "'Profit attributable to ordinary shareholders (Group)' is a genuine "
    "subtotal on the face of the FY1990, FY1989 and FY1988 statements, struck as "
    "Profit before Taxation LESS the five lines under it - so it needs the "
    "preceding TOTAL row (Profit before taxation) as well as its own block, "
    "and the checker reports 18.543 - 12.667 = 5.876 as a mismatch because it "
    "starts from zero instead of from 18.543. Both columns foot exactly "
    "against their own printed statements (FY1989 5,876; FY1988 12,477). The "
    "sheet's existing 'Retained earnings (Group)' TOTAL has had the same "
    "property since HD-078 for the same reason. Nothing was adjusted to make "
    "either reconcile.\n"
    "RICHNESS CONTROL: all 11 Companies House filings in this range are "
    "image-only - pdftotext returns ZERO hits for ' the ' on every one, so a "
    "keyword search of them proves nothing either way. They were OCR'd "
    "(ocrmypdf/tesseract) to locate pages, and every figure above was then read "
    "off a rendered page image at 170-400 dpi."
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
    f"FY2024: 2024 AR, p.220-221 (BS), p.224 (Equity), p.226 (Note 2, Net profit attrib. to equity "
    f"shareholders - s.408 exemption) - {AR2024_URL}\n"
    f"FY2023: 2024 AR, p.220-221/224/226 (FY2023 comparative columns) - {AR2024_URL}\n"
    f"FY2022: 2022 AR, p.242-243/246/248 (BS/Equity/Note 2) - {AR2022_URL}\n"
    f"FY2021: 2022 AR, p.242-243/246/248 (FY2021 comparative columns) - {AR2022_URL}\n"
    f"FY2020: 2020 AR, p.212-213/216/217 (BS/Equity/Note 2) - {AR2020_URL}\n"
    f"FY2019: 2019 AR, p.197-198/201 (Bank Company-only BS+Equity) - {AR2019_URL}\n"
    f"FY2018: 2018 AR, p.183/186-187 (Bank Company BS+Equity, incl. Note 2 profit) - {AR2018_URL}\n"
    f"FY2017: 2017 AR, p.175/178 (Bank Company BS+Equity, incl. Note 1 profit) - {AR2017_URL}\n"
    f"FY2016: 2016 AR, p.146/149 (Bank BS+Equity - full income statement also disclosed, p.145) - "
    f"{AR2016_URL}\n"
    f"FY2015: 2015 AR, p.161/164 (Bank BS+Equity - full income statement also disclosed, p.159-160) - "
    f"{AR2015_URL}\n"
    f"FY2014: 2014 AR, p.149/152 (Bank BS+Equity - full income statement also disclosed, p.147-148) - "
    f"{AR2014_URL}\n"
    f"FY2013: 2013 AR (CH filing), p.130/133 (Bank BS+Equity - full income statement also disclosed, "
    f"p.128) - {AR2013_CH_URL}\n"
    f"FY2012: 2012 AR (CH filing), p.36/41 (BS+Equity) - {AR2012_CH_URL} - full income statement only "
    f"from the 2013 AR's own FY2012 comparative column, p.128 - {AR2013_CH_URL}\n"
    f"FY2011: 2012 AR (CH filing), p.36/41 (FY2011 comparative columns) - {AR2012_CH_URL}\n"
    f"FY2010: 2010 AR (CH filing), p.33/36 (Bank BS+Equity) - {AR2010_CH_URL}\n"
    f"FY2009: 2009 AR (CH filing), p.39/42 (Bank BS+Equity, year ended 31 Dec 2009 - Britannia merger "
    f"year) - {AR2009_CH_URL}\n"
    f"FY2008: 'Financial statements 2008' AR (CH filing), p.46/47 (Bank BS+SORIE, 52wk to 10 Jan 2009) - "
    f"{AR2008_CH_URL}\n"
    f"FY2007: 'Financial statements 2008' AR (CH filing), p.46/47 (FY2007 comparative columns, 52wk to "
    f"12 Jan 2008) - {AR2008_CH_URL}\n"
    f"FY2006: 'Financial Statements 2006' AR (CH filing), p.42/43 (Bank BS+SORIE, 52wk to 13 Jan 2007) - "
    f"{AR2006_CH_URL}\n"
    f"FY2005: 'Financial Statements 2006' AR (CH filing), p.42/43 (FY2005 comparative columns, 53wk to "
    f"14 Jan 2006) - {AR2006_CH_URL}\n"
    f"FY2004: 'Financial Statements 2004' AR (CH filing), p.50/51 (Bank BS+Reconciliation of movements "
    f"in shareholders' funds - UK GAAP predecessor to the Equity statement, 52wk to 8 Jan 2005) - "
    f"{AR2004_CH_URL}\n"
    f"FY2003: 'Financial Statements 2004' AR (CH filing), p.50/51 (FY2003 comparative columns, 52wk to "
    f"10 Jan 2004) - {AR2004_CH_URL}\n\n"
    "HD-078 FOLLOW-UP - FY2002-FY1991 (Balance Sheet/Equity only, all Companies House filings; see "
    "HD078_1991_2002_NOTE for full methodology):\n"
    f"FY2002: 'Financial Statements 2002' AR, p.34/35 (BS+Reconciliation of movements in shareholders' funds, "
    f"52wk to 11 Jan 2003) - {AR2002_CH_URL}\n"
    f"FY2001: 'Financial Statements 2001' AR, p.34/35 (BS+Reconciliation, Bank section, 52wk to 12 Jan 2002) - "
    f"{AR2001_CH_URL}\n"
    f"FY2000: 'Financial Statements 2000' AR, p.34 (BS, 52wk to 13 Jan 2001; profit/dividends from FY2001 AR's "
    f"own FY2000 comparative Bank reconciliation, since this AR's own reconciliation is Group-level only) - "
    f"{AR2000_CH_URL}\n"
    f"FY1999: 'Financial Statements 1999' AR, p.34 (BS, 52wk to 8 Jan 2000) - {AR1999_CH_URL}\n"
    f"FY1998: 'Financial Statements 1998' AR, p.32 (BS, 52wk to 9 Jan 1999) - {AR1998_CH_URL}\n"
    f"FY1997: 'Financial Statements 1997' AR, p.29 (BS, 52wk to 10 Jan 1998) - {AR1997_CH_URL}\n"
    f"FY1996: 'Financial Statements 1996' AR, p.21 (BS, 52wk to 11 Jan 1997) - {AR1996_CH_URL}\n"
    f"FY1995: 'Financial Statements 1995' AR, p.35 (BS, 52wk to 13 Jan 1996) - {AR1995_CH_URL}\n"
    f"FY1994: 'Financial Statements 1994' AR, p.29 (BS, 53wk to 14 Jan 1995) - {AR1994_CH_URL}\n"
    f"FY1993: 'Financial Statements 1993' AR, p.29 (BS, 52wk to 8 Jan 1994) - {AR1993_CH_URL}\n"
    f"FY1992: 'Financial Statements 1993' AR, p.29 (FY1992 comparative column, same BS - used in place of "
    f"separately re-opening FY1992's own filing; see HD078_1991_2002_NOTE) - {AR1993_CH_URL}\n"
    f"FY1991: 'Annual Report and Financial Statements 1991', p.28/29 (BS, 52wk to 11 Jan 1992 - coarser "
    f"pre-Sch.9 presentation, see HD078_1991_2002_NOTE) - {AR1991_CH_URL}\n\n"
    "HD-078 FOLLOW-UP - FY1990-FY1981 (Balance Sheet/Equity only, all Companies House filings; see "
    "HD078_1981_1990_NOTE for full methodology):\n"
    f"FY1990: Report and Accounts, Bank Balance Sheet at 12 Jan 1991, printed p.26/27 + Reserves note "
    f"- {FY1990_CH_URL}\n"
    f"FY1989: Report and Accounts, BS+Reserves note (to 13 Jan 1990; discloses restated FY1988 Share premium "
    f"comparative - see HD078_1981_1990_NOTE) - {AR1990_CH_URL}\n"
    f"FY1988: Report and Accounts, BS (assets side only re-captured, liabilities a residual - see "
    f"HD078_1981_1990_NOTE) + Reserves note (to 14 Jan 1989) - {AR1989_CH_URL}\n"
    f"FY1987: Report and Accounts, BS+Reserves note (to 9 Jan 1988) - {AR1988_CH_URL}\n"
    f"FY1986: Report and Accounts, BS+Reserves note (to 10 Jan 1987) - {AR1987_CH_URL}\n"
    f"FY1985: 'Financial Statement 1985' AR (own cover title), BS+Reserves note (to 11 Jan 1986) - {AR1986_CH_URL}\n"
    f"FY1984: Report and Accounts, BS+Reserves note, as originally reported (to 12 Jan 1985; not "
    f"FY1985's restated comparative - see HD078_1981_1990_NOTE) - {AR1985_CH_URL}\n"
    f"FY1983: Report and Accounts, BS+Reserves note (to 14 Jan 1984) - {AR1984_CH_URL}\n"
    f"FY1982: Report and Accounts, BS+Reserves note (to 8 Jan 1983) - {AR1983_CH_URL}\n"
    f"FY1981: 'Report and Accounts for the year ended 9th January 1982', BS+Reserves note - {AR1982_CH_URL}\n"
    "GA-024 (2026-09-19): these lines previously cited one document too early (FY<n> -> AR<n>, the "
    "FY<n-1> filing); the figures were always right.\n\n"
    "HD-078 FOLLOW-UP - FY1980-FY1972 (Balance Sheet/Equity only, the workbook's genuine hard floor; see "
    "HD078_1972_1980_NOTE for full methodology):\n"
    f"FY1980: Report and Accounts, BS+Note 9 Reserves (year ended 10 Jan 1981) - {AR1981_CH_URL}\n"
    f"FY1979: Report and Accounts, BS+Reserves note (year ended early Jan 1980; discloses the SSAP15/bad-debt "
    f"restatement of the FY1978 comparative) - {AR1980_CH_URL}\n"
    f"FY1978: Report and Accounts, BS+Reserves note (year ended early Jan 1979; as originally reported, "
    f"pre-FY1979 restatement) - {AR1979_CH_URL}\n"
    f"FY1977: Report and Accounts, BS+Reserves note (year ended 14 Jan 1978) - {AR1978_CH_URL}\n"
    f"FY1976: Report and Accounts, BS+Reserves note (year ended early Jan 1977) - {AR1977_CH_URL}\n"
    f"FY1975: Report and Accounts, BS+Reserves note (year ended early Jan 1976) - {AR1976_CH_URL}\n"
    f"FY1974: Report and Accounts, BS+Reserves note (year ended early Jan 1975) - {AR1975_CH_URL}\n"
    f"FY1973: Report and Accounts, BS+Reserves note (year ended early Jan 1974; discloses the £4.0m to £8.0m "
    f"Ordinary share capital bonus issue) - {AR1974_CH_URL}\n"
    f"FY1972: Report and Accounts, BS+Note 2 (year ended 13 Jan 1973 - earliest filed accounts; Note 2 confirms "
    f"the comparative is only a 26-week stub, 10 Jul 1971-8 Jan 1972, tying to Note 1(a)'s vesting of C.W.S.'s "
    f"banking activities in Co-operative Bank Limited on 10 Jul 1971) - {AR1973_CH_URL}\n\n"
    "The Bank Company takes the Section 408 Companies Act 2006 exemption not to present its own income "
    "statement from FY2017 onward - each AR discloses only the bottom-line net profit/(loss) figure plus OCI "
    "reserve movements within the Equity statement; the P&L sheet reconstructs from these two pieces for "
    "FY2017-FY2024, tying exactly to the equity roll-forward's own Total comprehensive income figures. "
    "FY2014-FY2016 predate the holdco restructuring (see HOLDCO RESTRUCTURING HISTORY below) - the Bank itself "
    "was the reporting entity and discloses a full income statement without the exemption; reproduced as "
    "additional rows FY2014-FY2016 only.\n\n"
    "FY2013/FY2012: the exemption was already being taken from FY2010 (Consolidated-only income statements "
    "FY2010-FY2012), except the Bank's 2013 AR, published amid its 2013 recapitalisation, which voluntarily "
    "discloses a full Bank income statement for FY2013 and, as its own comparative, FY2012 too - the only "
    "source for a standalone FY2012 income statement. FY2009-FY2011 show bottom-line profit + OCI only, as "
    "FY2017 onward.\n\n"
    "NON-CONTROLLING INTERESTS: FY2014 Total equity (£2,014.5m) and FY2015 opening equity include a small NCI "
    "balance (£34.5m) from the Bank's then-majority stake in Unity Trust Bank plc, disposed December 2015 (see "
    "Equity sheet's 'Disposal of UTB' row); Profit/OCI rows throughout use equity-shareholder-attributable "
    "figures only, for comparability with later years.\n\n"
    "PRESENTATION: 'Other reserves' is a single aggregate line FY2021 onward (FVOCI+hedging+capital "
    "redemption+pension reserves); FY2020 still itemises Share premium (£2,416.9m) separately - a FY2021 "
    "'Reserve reorganisation' wrote share premium/capital redemption reserve to £nil into retained earnings "
    "(net-zero on Total equity, shown explicitly on the Equity sheet). 'Equity shares'/'Prepayments' are their "
    "own lines FY2020-2022 only (folded into Other assets from FY2023). Deferred tax is an asset FY2021-2024, a "
    "liability in FY2020 - both shown as originally disclosed, not netted. 'Fair value adjustments for hedged "
    "risk' appears as separate lines only FY2020-2022 (embedded in the Loans note thereafter).\n\n"
    "PRE-2018 PRESENTATION: 'Investment securities' FY2014-FY2017 sums the original sub-categories (loans and "
    "receivables/AFS/FVTPL/held for trading), combined into one line by the Bank from FY2018 - ties to the "
    "credit-risk note's own total every year. 'Non-current assets held for sale' (FY2014-2016 label) and "
    "'PP&E classified as held-for-sale' (FY2017+ label) are the same category, one shared row. 'Prepayments and "
    "accrued income' was combined FY2014-2018; FY2019 shows 'Prepayments' alone (IFRS 16); FY2020-2022 use "
    "'Prepayments' again. 'Customer accounts - capital bonds'/'Other borrowed funds' were separate FY2014-2016 "
    "(nil by FY2017), superseded by Debt securities in issue and, from FY2019, IFRS 16 lease liabilities/Tier 2 "
    "notes - each shown only in years actually disclosed. Right-of-use assets/lease liabilities first appear "
    "FY2019 (IFRS 16 effective date, comparatives not restated per the Bank's own transition option).\n\n"
    "RESTATEMENT (FY2016/FY2017 boundary): 2016 AR's own closing Total equity (£958.5m) vs 2017 AR's own "
    "restated FY2016 comparative (£726.4m, £232.1m retained-earnings gap) - the 2017 AR's footnote attributes "
    "this to a re-presentation of repo/reverse-repo netting arrangements, not a transcription error. Shown as "
    "an explicit 'Restatement' row on the Equity sheet, same treatment as the FY2021 'Reserve reorganisation' "
    "row, rather than force-matched.\n\n"
    "PRE-2014 PRESENTATION: FY2003-FY2013 uses each era's own captions rather than force-mapped onto FY2014+ "
    "(see PRE-2014 HISTORICAL DEPTH below for the three reporting-basis eras). New rows for this range: 'Items "
    "in the course of collection/transmission from/to other banks' (FY2003-2004), 'Debt securities' "
    "(FY2003-2008, pre-split combined line), 'Retirement benefit obligations' (FY2005), 'Preference share "
    "capital (non-equity)' (FY2003-2004). FY2002-FY1991 adds: 'Treasury bills and other eligible bills' "
    "(intermittent throughout), 'Interests in associated undertakings' (~£17k FY1993-1999), and FY1991-only "
    "'Current, deposit and other accounts (aggregate)' and 'Creditors, accrued expenses and accrued preference "
    "dividend (FY1991 only)' - see HD078_1991_2002_NOTE for why FY1991 couldn't map onto the finer row set.\n\n"
    + PRE2014_HISTORY_NOTE + "\n\n"
    + HD078_1991_2002_NOTE + "\n\n"
    + HD078_1981_1990_NOTE + "\n\n"
    + HD078_1972_1980_NOTE + "\n\n"
    + ENTITY_NOTE
)

# P&L-only addition to STATEMENTS_SOURCES (kept separate, not folded into the
# shared block above, which Balance Sheet and Equity also use and already
# sits close to openpyxl's 32,000-char citation-cell warning threshold).
PL_SOURCES = STATEMENTS_SOURCES + (
    "\n\nCOST:INCOME RATIO (2026-09-07): headline-disclosed every year on the Bank/Group's own KPI page, "
    "independent of the itemised opex rows above (only exist FY2014-FY2016) - not derived. Basis drifts by "
    "year, per the source: FY2013-FY2016 Bank; FY2017-FY2018 Group; FY2020+ 'Group and Bank' (converged); "
    "FY2019 not disambiguated by the source. Own-year figures used, not restated comparatives (AR URLs as "
    "cited above for the same year):\n"
    "FY2024/FY2023(comp): 2024 AR p.6\nFY2022/FY2021(comp): 2022 AR p.6\nFY2020: 2020 AR p.6\n"
    "FY2019: 2019 AR p.6\nFY2018: 2018 AR p.4 (Group)\nFY2017: 2017 AR p.15 (Group)\n"
    "FY2016: 2016 AR p.19 (Bank)\nFY2015: 2015 AR p.23 (Bank)\nFY2014/FY2013(comp): 2014 AR p.19 (Bank)\n"
    "\nFY2011-FY1981 P&L sources: SECOND source cell below (this one is at openpyxl's size ceiling).\n"
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
            # HD-078 follow-up (FY2002-FY1991): FY1991's own 'Coin and bank notes' sub-line of Liquid Assets.
            "FY2002": 97.5, "FY2001": 113.7, "FY2000": 61.7, "FY1999": 74.9, "FY1998": 47.7, "FY1997": 33.7,
            "FY1996": 35.1, "FY1995": 33.1, "FY1994": 37.6, "FY1993": 31.7, "FY1992": 19.0, "FY1991": 18.0,
            # HD-078 follow-up (2026-09-07): FY1990-FY1981, each year's own Companies House filing - see
            # HD078_1981_1990_NOTE. 'Coin and bank notes' sub-line of Liquid Assets, same mapping.
            "FY1990": 12.1, "FY1989": 11.0, "FY1988": 10.1, "FY1987": 7.8, "FY1986": 7.1, "FY1985": 8.3,
            "FY1984": 7.1, "FY1983": 5.5, "FY1982": 7.3, "FY1981": 5.1,
            # HD-078 (2026-09-07): FY1990-FY1972 (Balance Sheet/Statement of Changes in Equity only, own
            # filed reports at Companies House) - see HD078_1972_1980_NOTE for the full FY1980-FY1972
            # leg of this range (FY1990-FY1981 sourced separately). 'Coin and bank notes' sub-line of
            # Liquid Assets, same as FY1991-2002 mapping above.
            "FY1980": 4.515, "FY1979": 4.777, "FY1978": 4.210, "FY1977": 4.171, "FY1976": 4.602,
            "FY1975": 4.531, "FY1974": 3.562, "FY1973": 3.142, "FY1972": 2.106,
        }),
        ("DATA", "Loans and advances to banks", {
            "FY2024": 173.1, "FY2023": 193.7, "FY2022": 312.5, "FY2021": 124.7, "FY2020": 431.6,
            "FY2019": 345.6, "FY2018": 380.4, "FY2017": 460.3, "FY2016": 836.9, "FY2015": 871.0, "FY2014": 1608.4,
            "FY2013": 1594.4, "FY2012": 1047.2, "FY2011": 1300.1, "FY2010": 1728.6, "FY2009": 1220.1,
            "FY2008": 1897.5, "FY2007": 1211.2, "FY2006": 1369.4, "FY2005": 1170.6, "FY2004": 1073.0, "FY2003": 773.2,
            # FY1991: 'Money at call and short notice' sub-line of Liquid Assets (closest economic match).
            "FY2002": 1291.0, "FY2001": 733.2, "FY2000": 580.6, "FY1999": 493.9, "FY1998": 431.3, "FY1997": 507.7,
            "FY1996": 615.7, "FY1995": 905.7, "FY1994": 617.3, "FY1993": 946.6, "FY1992": 910.9, "FY1991": 387.3,
            # HD-078 follow-up (2026-09-07): FY1990-FY1981 'Money at call and short notice' sub-line of
            # Liquid Assets - see HD078_1981_1990_NOTE.
            "FY1990": 372.0, "FY1989": 433.6, "FY1988": 334.8, "FY1987": 120.8, "FY1986": 242.9,
            "FY1985": 98.6, "FY1984": 161.8, "FY1983": 151.6, "FY1982": 129.0, "FY1981": 90.7,
            # HD-078 (2026-09-07): FY1980-FY1972 'Money at call and short notice' sub-line of Liquid Assets.
            "FY1980": 114.888, "FY1979": 84.620, "FY1978": 56.668, "FY1977": 45.715, "FY1976": 38.717,
            "FY1975": 33.718, "FY1974": 44.090, "FY1973": 44.955, "FY1972": 30.065,
        }),
        ("DATA", "Loans and advances to customers", {
            "FY2024": 20370.8, "FY2023": 20147.5, "FY2022": 20919.1, "FY2021": 20998.3, "FY2020": 18676.7,
            "FY2019": 17811.1, "FY2018": 17614.3, "FY2017": 16608.2, "FY2016": 19452.7, "FY2015": 19690.4,
            "FY2014": 25377.4,
            "FY2013": 30322.2, "FY2012": 22785.5, "FY2011": 22735.0, "FY2010": 23844.9, "FY2009": 23050.8,
            "FY2008": 11169.8, "FY2007": 8914.4, "FY2006": 8051.8, "FY2005": 7807.9, "FY2004": 7546.4,
            "FY2003": 6073.2,
            "FY2002": 4329.2, "FY2001": 3817.4, "FY2000": 3305.0, "FY1999": 2925.8, "FY1998": 2732.7,
            "FY1997": 2453.5, "FY1996": 2152.0, "FY1995": 1903.4, "FY1994": 1717.7, "FY1993": 1655.4,
            "FY1992": 1586.8,
            # FY1991: 'Customer and Other Accounts' (asset-side).
            "FY1991": 1711.9,
            # HD-078 follow-up (2026-09-07): FY1990-FY1981 'Customer and Other Accounts' (asset-side) -
            # see HD078_1981_1990_NOTE.
            "FY1990": 1972.6, "FY1989": 1741.3, "FY1988": 1405.0, "FY1987": 1062.8, "FY1986": 954.0,
            "FY1985": 778.0, "FY1984": 690.6, "FY1983": 590.9, "FY1982": 492.9, "FY1981": 405.8,
            # HD-078 (2026-09-07): FY1980-FY1972 'Customer and Other Accounts' (Advances less provisions,
            # plus Debtors, combined - the source does not split these further on the face of the Bank
            # balance sheet this era).
            "FY1980": 318.334, "FY1979": 252.929, "FY1978": 141.927, "FY1977": 118.345, "FY1976": 98.913,
            "FY1975": 69.446, "FY1974": 67.383, "FY1973": 75.970, "FY1972": 33.927,
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
            # HD-078 follow-up (FY2002-FY1991): 'Debt securities' line each year. FY1991 combines the
            # source's own separate 'Investments' (£88.5m) and 'Certificates of Deposit' (£59.7m) lines
            # into this one row, since neither maps independently onto any other year's row set.
            "FY2002": 2266.0, "FY2001": 2560.6, "FY2000": 2187.6, "FY1999": 2191.8, "FY1998": 1837.7,
            "FY1997": 1803.0, "FY1996": 1244.8, "FY1995": 586.7, "FY1994": 528.5, "FY1993": 350.2,
            "FY1992": 205.3, "FY1991": 148.2,
            # HD-078 follow-up (2026-09-07): FY1990-FY1981 combines the source's own separate
            # 'Investments' and 'Certificates of Deposit' lines into this one row, same treatment as
            # FY1991 above; FY1981 additionally includes that year's own 'Special Deposits with the Bank
            # of England' line (£1.721m), which no other row on this sheet maps onto - see
            # HD078_1981_1990_NOTE. FY1990: 92.638+78.249; FY1989: 114.500+45.711; FY1988: 107.446+43.556;
            # FY1987: 97.576+70.048; FY1986: 62.372+3.466; FY1985: 59.538+8.417; FY1984: 73.638+11.834;
            # FY1983: 78.307+9.077; FY1982: 86.841+10.038; FY1981: 96.495+28.034+1.721.
            "FY1990": 170.9, "FY1989": 160.2, "FY1988": 151.0, "FY1987": 167.6, "FY1986": 65.8,
            "FY1985": 68.0, "FY1984": 85.5, "FY1983": 87.4, "FY1982": 96.9, "FY1981": 126.3,
            # HD-078 (2026-09-07): FY1980-FY1972 combines the source's own separate 'Investments',
            # 'Certificates of Deposit' (or 'Sterling Certificates of Deposit') and 'Special Deposits with
            # the Bank of England' lines into this one row, same treatment as FY1991 above - none of the
            # three maps independently onto any other row on this sheet. FY1980: 47.151+2.980+0 (nil
            # Special Deposits that year); FY1979: 63.565+2.697+5.737; FY1978: 86.327+3.403+6.871;
            # FY1977: 70.800+25.760+6.334; FY1976: 65.635+17.232+9.778; FY1975: 57.552+36.982+4.677;
            # FY1974: 42.362+3.541+3.385; FY1973: 45.892+9.320+6.331; FY1972: 60.953+31.898+2.192.
            "FY1980": 50.131, "FY1979": 71.999, "FY1978": 96.601, "FY1977": 102.894, "FY1976": 92.645,
            "FY1975": 99.211, "FY1974": 49.288, "FY1973": 61.543, "FY1972": 95.043,
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
            "FY2002": 0.9, "FY2001": 1.3, "FY2000": 1.3, "FY1999": 1.2, "FY1998": 1.2, "FY1997": 1.2,
            "FY1996": 1.1, "FY1995": 0.9, "FY1994": 0.5, "FY1993": 0.5, "FY1992": 0.5,
        }),
        ("DATA", "Investments in joint ventures", {"FY2016": 6.0, "FY2015": 4.9, "FY2014": 5.3, "FY2013": 4.7}),
        ("DATA", "Goodwill", {
            "FY2012": 0.0, "FY2011": 0.6, "FY2010": 0.6, "FY2009": 0.6, "FY2008": 0.0, "FY2007": 0.0,
        }),
        ("DATA", "Treasury bills and other eligible bills", {
            # HD-078 follow-up (FY2002-FY1991): a distinct Bank balance sheet line in this era, recurring
            # intermittently (nil/not disclosed in FY1998, FY1994, FY1993, FY1992, FY1991 - the last four
            # of those years' own accounts either state nil or do not present this line at all).
            "FY2002": 18.0, "FY2001": 1.6, "FY2000": 55.6, "FY1999": 35.6, "FY1997": 13.1, "FY1996": 0.7,
            "FY1995": 55.5,
        }),
        ("DATA", "Interests in associated undertakings", {
            # HD-078 follow-up: a small, near-constant Bank balance sheet line FY1993-FY1999 (£17k each
            # year); not separately disclosed FY2000-FY2002 (likely folded into Equity shares) or FY1991.
            "FY1999": 0.0, "FY1998": 0.0, "FY1997": 0.0, "FY1996": 0.0, "FY1995": 0.0, "FY1994": 0.0,
            "FY1993": 0.0,
            # HD-078 follow-up (2026-09-07): FY1990-FY1981 'Associated Companies' - drops from a material
            # £15-26m across FY1984-FY1987 to the same near-nil ~£17k basis seen FY1993-FY1999 by FY1988,
            # confirming this is a genuine disposal/write-down over FY1987-FY1988, not a transcription
            # error - see HD078_1981_1990_NOTE.
            "FY1990": 0.0, "FY1989": 0.0, "FY1988": 0.0, "FY1987": 15.4, "FY1986": 21.9, "FY1985": 22.5,
            "FY1984": 25.7, "FY1983": 0.1, "FY1982": 0.1, "FY1981": 0.7,
            # HD-078 (2026-09-07): FY1980-FY1972 'Associated Companies' - a small Bank balance sheet line
            # each year of this range.
            "FY1980": 0.183, "FY1979": 0.096, "FY1978": 0.350, "FY1977": 0.347, "FY1976": 0.360,
            "FY1975": 0.402, "FY1974": 3.248, "FY1973": 0.001, "FY1972": 0.001,
        }),
        ("DATA", "Investments in subsidiaries/group undertakings", {
            "FY2024": 22.8, "FY2023": 14.9, "FY2022": 15.0, "FY2021": 14.7, "FY2020": 43.3,
            "FY2019": 43.0, "FY2018": 49.4, "FY2017": 51.6,
            "FY2012": 1588.5, "FY2011": 1573.4, "FY2010": 1458.9, "FY2009": 1553.0,
            "FY2008": 969.3, "FY2007": 2.7, "FY2006": 2.7, "FY2005": 2.7, "FY2004": 1.2, "FY2003": 1.2,
            "FY2002": 1.2, "FY2001": 1.2, "FY2000": 1.2, "FY1999": 1.1, "FY1998": 1.1, "FY1997": 1.1,
            "FY1996": 1.1, "FY1995": 1.2, "FY1994": 1.2, "FY1993": 1.2, "FY1992": 1.2,
            # FY1991: 'Subsidiary Undertakings' - a much larger gross figure than FY1992 onward's ~£1.2m,
            # a genuine measurement-basis difference across the pre-1992 format change, not an error - see
            # HD078_1991_2002_NOTE.
            "FY1991": 176.0,
            # HD-078 follow-up (2026-09-07): FY1990-FY1981 'Subsidiary Undertakings'/'Subsidiaries', same
            # larger pre-1992-format basis as FY1991 above - see HD078_1981_1990_NOTE.
            "FY1990": 112.1, "FY1989": 94.2, "FY1988": 93.1, "FY1987": 70.7, "FY1986": 75.2, "FY1985": 41.6,
            "FY1984": 11.4, "FY1983": -1.8, "FY1982": 1.0, "FY1981": 0.0,
            # HD-078 (2026-09-07): FY1980-FY1972 'Subsidiaries' (gross cost of investment plus amounts due
            # by subsidiaries, on the same larger pre-1992-format basis as FY1991 above, not the ~£1.2m
            # basis used FY1992 onward).
            "FY1980": 31.911, "FY1979": 35.640, "FY1978": 35.160, "FY1977": 32.612, "FY1976": 28.978,
            "FY1975": 23.012, "FY1974": 43.800, "FY1973": 13.354, "FY1972": 7.781,
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
            "FY2002": 69.9, "FY2001": 37.2, "FY2000": 33.7, "FY1999": 34.1, "FY1998": 55.1, "FY1997": 24.7,
            "FY1996": 24.1, "FY1995": 17.9, "FY1994": 15.7, "FY1993": 13.5, "FY1992": 13.8,
        }),
        ("DATA", "Prepayments", {"FY2022": 21.4, "FY2021": 20.3, "FY2020": 13.2}),
        ("DATA", "Prepayments and accrued income", {
            "FY2019": 21.6, "FY2018": 31.8, "FY2017": 24.6, "FY2016": 28.7, "FY2015": 43.5, "FY2014": 12.2,
            "FY2013": 16.5, "FY2012": 14.0, "FY2011": 17.7, "FY2010": 14.5, "FY2009": 27.4,
            "FY2008": 56.8, "FY2007": 44.9, "FY2006": 79.3, "FY2005": 64.1, "FY2004": 89.4, "FY2003": 70.4,
            "FY2002": 96.2, "FY2001": 100.3, "FY2000": 137.6, "FY1999": 72.9, "FY1998": 73.3, "FY1997": 72.3,
            "FY1996": 53.8, "FY1995": 47.1, "FY1994": 34.2, "FY1993": 28.4, "FY1992": 24.8,
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
        ("DATA", "Items in the course of collection from other banks", {
            "FY2004": 108.0, "FY2003": 116.0,
            # HD-078 follow-up: 'Cheques in course of collection' (FY1994-FY1993) / 'Items in the course of
            # collection from other banks' (FY2002-FY1995) - same substance. FY1991: sub-line of Liquid
            # Assets ('Balances with, and amounts in course of collection from, other banks').
            "FY2002": 164.9, "FY2001": 145.3, "FY2000": 116.7, "FY1999": 135.0, "FY1998": 104.8,
            "FY1997": 124.2, "FY1996": 120.6, "FY1995": 115.5, "FY1994": 105.4, "FY1993": 155.8,
            "FY1992": 124.3, "FY1991": 99.0,
            # HD-078 follow-up (2026-09-07): FY1990-FY1981 'Balances with, and amounts in course of
            # collection from, other banks' sub-line of Liquid Assets - see HD078_1981_1990_NOTE.
            "FY1990": 103.6, "FY1989": 73.5, "FY1988": 68.3, "FY1987": 72.8, "FY1986": 59.8, "FY1985": 69.3,
            "FY1984": 56.6, "FY1983": 54.5, "FY1982": 71.4, "FY1981": 53.6,
            # HD-078 (2026-09-07): FY1980-FY1972 'Balances with and amounts in course of collection from
            # other banks' sub-line of Liquid Assets, same mapping as FY1991-2002 above.
            "FY1980": 46.716, "FY1979": 42.643, "FY1978": 37.690, "FY1977": 27.162, "FY1976": 32.678,
            "FY1975": 28.895, "FY1974": 25.940, "FY1973": 21.822, "FY1972": 15.240,
        }),
        ("DATA", "Property, plant and equipment", {
            "FY2024": 24.9, "FY2023": 23.6, "FY2022": 22.8, "FY2021": 24.3, "FY2020": 35.2,
            "FY2019": 38.6, "FY2018": 40.8, "FY2017": 44.4, "FY2016": 35.4, "FY2015": 46.1, "FY2014": 67.5,
            "FY2013": 115.2, "FY2012": 46.2, "FY2011": 61.5, "FY2010": 79.1, "FY2009": 101.6,
            "FY2008": 53.9, "FY2007": 74.0, "FY2006": 87.8, "FY2005": 79.8, "FY2004": 87.3, "FY2003": 84.6,
            "FY2002": 70.6, "FY2001": 59.1, "FY2000": 60.6, "FY1999": 56.0, "FY1998": 52.0, "FY1997": 55.1,
            "FY1996": 54.1, "FY1995": 51.0, "FY1994": 43.9, "FY1993": 39.8, "FY1992": 32.5,
            # FY1991: 'Fixed Assets'.
            "FY1991": 32.0,
            # HD-078 follow-up (2026-09-07): FY1990-FY1981 'Fixed Assets' - see HD078_1981_1990_NOTE.
            "FY1990": 31.5, "FY1989": 30.9, "FY1988": 29.1, "FY1987": 22.3, "FY1986": 22.1, "FY1985": 20.2,
            "FY1984": 18.1, "FY1983": 17.3, "FY1982": 17.5, "FY1981": 14.0,
            # HD-078 (2026-09-07): FY1980-FY1972 'Fixed Assets', same mapping as FY1991 above.
            "FY1980": 11.148, "FY1979": 8.228, "FY1978": 4.621, "FY1977": 3.876, "FY1976": 3.021,
            "FY1975": 2.772, "FY1974": 1.985, "FY1973": 1.134, "FY1972": 0.953,
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
            "FY2002": 8405.4, "FY2001": 7570.9, "FY2000": 6541.6, "FY1999": 6022.4, "FY1998": 5337.1,
            "FY1997": 5089.7, "FY1996": 4303.1, "FY1995": 3718.0, "FY1994": 3101.9, "FY1993": 3223.0,
            "FY1992": 2968.8,
            # FY1991: disclosed Total assets figure used as the authoritative anchor rather than a
            # component sum - see HD078_1991_2002_NOTE (a ~£0.03m/0.001% gap could not be resolved to the
            # individual digit against the severely degraded FY1991 scan image).
            "FY1991": 2572.6,
            # HD-078 follow-up (2026-09-07): FY1990-FY1981 disclosed Total assets figures, each
            # independently cross-checked against the component sum above (all tie exactly) - see
            # HD078_1981_1990_NOTE.
            "FY1990": 2774.8, "FY1989": 2544.6, "FY1988": 2091.4, "FY1987": 1540.1, "FY1986": 1448.8,
            "FY1985": 1106.5, "FY1984": 1056.6, "FY1983": 905.4, "FY1982": 816.1, "FY1981": 696.3,
            # HD-078 (2026-09-07): FY1980-FY1972 disclosed Total assets figures, each independently
            # cross-checked against the component sum above (all tie exactly).
            "FY1980": 577.826, "FY1979": 500.932, "FY1978": 377.227, "FY1977": 335.122, "FY1976": 299.914,
            "FY1975": 261.987, "FY1974": 239.296, "FY1973": 221.921, "FY1972": 185.116,
        }),
        ("SECTION", "Liabilities", {}),
        ("DATA", "Deposits by banks", {
            "FY2024": 2717.2, "FY2023": 4288.9, "FY2022": 5683.4, "FY2021": 5527.6, "FY2020": 2066.4,
            "FY2019": 1143.7, "FY2018": 1433.5, "FY2017": 1122.7, "FY2016": 1198.6, "FY2015": 725.9,
            "FY2014": 615.4,
            "FY2013": 2757.5, "FY2012": 3552.9, "FY2011": 3239.8, "FY2010": 2870.8, "FY2009": 5613.0,
            "FY2008": 1072.3, "FY2007": 661.3, "FY2006": 700.6, "FY2005": 641.1, "FY2004": 659.4, "FY2003": 773.8,
            "FY2002": 756.4, "FY2001": 733.6, "FY2000": 750.5, "FY1999": 913.7, "FY1998": 599.1, "FY1997": 578.1,
            "FY1996": 565.5, "FY1995": 404.9, "FY1994": 605.7, "FY1993": 572.4, "FY1992": 560.4,
            # FY1991: not separately disclosed - see 'Current, deposit and other accounts' below.
        }),
        ("DATA", "Customer accounts", {
            "FY2024": 19974.2, "FY2023": 19215.8, "FY2022": 20107.9, "FY2021": 21136.4, "FY2020": 20366.3,
            "FY2019": 18997.2, "FY2018": 18736.4, "FY2017": 20635.7, "FY2016": 22425.1, "FY2015": 22732.0,
            "FY2014": 29614.0,
            "FY2013": 32463.3, "FY2012": 33750.3, "FY2011": 32670.1, "FY2010": 29912.0, "FY2009": 28660.0,
            "FY2008": 13388.7, "FY2007": 10068.1, "FY2006": 9119.3, "FY2005": 8391.7, "FY2004": 7778.5,
            "FY2003": 7126.2,
            "FY2002": 6679.5, "FY2001": 5906.8, "FY2000": 4992.0, "FY1999": 4368.1, "FY1998": 4041.8,
            "FY1997": 3766.1, "FY1996": 3180.7, "FY1995": 2740.5, "FY1994": 2133.0, "FY1993": 2282.2,
            "FY1992": 2033.8,
            # FY1991: not separately disclosed - see 'Current, deposit and other accounts' below.
        }),
        ("DATA", "Current, deposit and other accounts (aggregate - not split by counterparty)", {
            # HD-078 follow-up: FY1991's own presentation combines what later years split into 'Deposits
            # by banks' and 'Customer accounts' into one line - see HD078_1991_2002_NOTE.
            "FY1991": 2324.6,
            # HD-078 follow-up (2026-09-07): FY1990-FY1981's own 'Current, deposit and other accounts'
            # line - undifferentiated between banks/customers throughout this era, matching the FY1991
            # presentation - see HD078_1981_1990_NOTE. FY1988 is a residual computed as Total assets less
            # Share Capital and Reserves, Loan Stock, and Deferred Tax, since that year's own report did not
            # split its liabilities page as granularly as adjacent years.
            "FY1990": 2513.8, "FY1989": 2276.0, "FY1988": 1875.2, "FY1987": 1345.9, "FY1986": 1266.1,
            "FY1985": 937.7, "FY1984": 941.0, "FY1983": 815.3, "FY1982": 740.2, "FY1981": 626.1,
            # HD-078 (2026-09-07): FY1980-FY1972's own 'Current, deposit and other accounts' line - the
            # entire FY1980-FY1972 range uses this same single aggregate line (not split into 'Deposits by
            # banks' and 'Customer accounts' at all this era) - see HD078_1972_1980_NOTE.
            "FY1980": 508.468, "FY1979": 436.645, "FY1978": 331.641, "FY1977": 290.494, "FY1976": 255.689,
            "FY1975": 218.312, "FY1974": 196.561, "FY1973": 178.667, "FY1972": 141.130,
        }),
        ("DATA", "Deposits by trustees of CWS employees' pension scheme (secured)", {
            # HD-078 (2026-09-07): FY1981-FY1972 - a distinct, separately-secured deposit line in this
            # era's Bank balance sheet (deposits from the trustees of the Co-operative Wholesale Society
            # employees' pension scheme, secured over specific investments per each year's own notes) -
            # not present in any FY1982-onward balance sheet in this workbook; FY1981 is the last year it
            # appears - see HD078_1981_1990_NOTE.
            "FY1981": 5.6,
            "FY1980": 8.149, "FY1979": 9.954, "FY1978": 12.264, "FY1977": 14.367, "FY1976": 15.565,
            "FY1975": 16.676, "FY1974": 18.000, "FY1973": 19.784, "FY1972": 21.880,
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
            # HD-078 follow-up: 'Subordinated liabilities' (FY2002-FY1993) / 'Loan Stock' (FY1991, £75.0m -
            # identical to the FY1992 subordinated balance, confirming continuity across the format change).
            "FY2002": 178.9, "FY2001": 178.7, "FY2000": 178.4, "FY1999": 192.2, "FY1998": 192.0,
            "FY1997": 191.9, "FY1996": 162.0, "FY1995": 198.9, "FY1994": 75.0, "FY1993": 75.0, "FY1992": 75.0,
            "FY1991": 75.0,
            # HD-078 follow-up (2026-09-07): FY1990-FY1981 'Loan Stock' / 'Subordinated Loans' - see
            # HD078_1981_1990_NOTE.
            "FY1990": 75.0, "FY1989": 75.0, "FY1988": 75.0, "FY1987": 75.0, "FY1986": 75.0, "FY1985": 75.0,
            "FY1984": 22.2, "FY1983": 17.8, "FY1982": 15.6, "FY1981": 12.8,
            # HD-078 (2026-09-07): FY1980-FY1979 'Subordinated Loans' (US $25,000,000 Floating Rate
            # (minimum 6%) Capital Notes redeemable not later than November 1986) - the Bank's first
            # subordinated debt issuance, not present in any earlier year in this range (FY1978 and
            # earlier have no Subordinated Loans line at all).
            "FY1980": 10.426, "FY1979": 11.074,
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
            "FY2002": 128.4, "FY2001": 86.3, "FY2000": 70.3, "FY1999": 76.7, "FY1998": 92.6, "FY1997": 61.2,
            "FY1996": 52.3, "FY1995": 41.9, "FY1994": 53.2, "FY1993": 66.3, "FY1992": 42.9,
            # HD-078 follow-up (2026-09-07): FY1990-FY1981 'Creditors' plus accrued preference dividend
            # (FY1989-FY1988 only) and proposed dividend, combined into this existing row - see
            # HD078_1981_1990_NOTE. FY1988: genuinely not separable from the aggregate deposits/current
            # liabilities residual that year (folded there instead) - left blank here for FY1988 only.
            "FY1990": 34.8, "FY1989": 23.2, "FY1987": 20.4, "FY1986": 19.2, "FY1985": 16.1, "FY1984": 19.8,
            "FY1983": 13.4, "FY1982": 9.9, "FY1981": 8.5,
            # HD-078 (2026-09-07): FY1980-FY1972 'Creditors' plus, in the two years it is separately
            # disclosed within Current Liabilities (FY1977 and FY1973), 'Taxation' - combined into this
            # existing row since neither maps independently. FY1980: 8.540 (no separate Taxation line that
            # year); FY1979: 6.218; FY1978: 2.886; FY1977: 1.969+0.224; FY1976: 1.957; FY1975: 1.727;
            # FY1974: 0.956; FY1973: 0.558+0.262; FY1972: 0.829.
            "FY1980": 8.540, "FY1979": 6.218, "FY1978": 2.886, "FY1977": 2.193, "FY1976": 1.957,
            "FY1975": 1.727, "FY1974": 0.956, "FY1973": 0.820, "FY1972": 0.829,
        }),
        ("DATA", "Accruals and deferred income", {
            "FY2024": 46.6, "FY2023": 22.7, "FY2022": 32.4, "FY2021": 36.8, "FY2020": 34.8,
            "FY2019": 58.4, "FY2018": 49.8, "FY2017": 59.9, "FY2016": 115.3, "FY2015": 152.5, "FY2014": 16.0,
            "FY2013": 54.1, "FY2012": 15.5, "FY2011": 33.1, "FY2010": 117.0, "FY2009": 134.3,
            "FY2008": 30.3, "FY2007": 32.5, "FY2006": 75.3, "FY2005": 71.5, "FY2004": 146.9, "FY2003": 127.3,
            "FY2002": 122.2, "FY2001": 126.1, "FY2000": 111.4, "FY1999": 83.1, "FY1998": 84.8, "FY1997": 94.7,
            "FY1996": 65.2, "FY1995": 51.9, "FY1994": 30.8, "FY1993": 16.0, "FY1992": 13.7,
        }),
        ("DATA", "Liabilities directly associated with non-current assets classified as held for sale", {
            "FY2014": 7.9,
        }),
        ("DATA", "Items in the course of transmission to other banks", {
            "FY2004": 7.5, "FY2003": 7.1,
            "FY2002": 6.7, "FY2001": 9.9, "FY2000": 11.1, "FY1999": 8.4, "FY1998": 7.1, "FY1997": 7.9,
            "FY1996": 5.8, "FY1995": 3.7,
            # FY1994: genuinely not presented as a separate line in that year's own Bank balance sheet.
        }),
        ("DATA", "Creditors, accrued expenses and accrued preference dividend (FY1991 only)", {
            # HD-078 follow-up: FY1991's own 'Creditors and accrued expenses' (£29.7m) plus 'Accrued
            # preference dividend' (£0.6m), combined - see HD078_1991_2002_NOTE.
            "FY1991": 30.4,
        }),
        ("DATA", "Provisions", {
            "FY2024": 10.1, "FY2023": 31.7, "FY2022": 33.1, "FY2021": 33.8, "FY2020": 46.0,
            "FY2019": 86.8, "FY2018": 103.0, "FY2017": 157.4, "FY2016": 276.4, "FY2015": 499.2, "FY2014": 617.5,
            "FY2013": 576.0, "FY2012": 161.6, "FY2011": 93.4, "FY2010": 39.3, "FY2009": 25.6,
            "FY2008": 14.7, "FY2007": 8.8, "FY2006": 5.9, "FY2005": 5.2, "FY2004": 6.0, "FY2003": 6.9,
            # HD-078 follow-up: 'Deferred taxation' within Provisions for liabilities and charges (nil/not
            # disclosed FY1996-FY1998).
            "FY2002": 9.9, "FY2001": 3.6, "FY2000": 2.6, "FY1999": 2.8, "FY1995": 2.8, "FY1994": 2.6,
            "FY1993": 1.1, "FY1992": 2.6,
            # FY1991: 'Deferred Taxation'.
            "FY1991": 1.1,
            # HD-078 follow-up (2026-09-07): FY1990-FY1981 'Deferred Taxation' - see HD078_1981_1990_NOTE.
            "FY1990": 3.0, "FY1989": 3.1, "FY1988": 5.3, "FY1987": 5.6, "FY1986": 5.1, "FY1985": 7.4,
            "FY1984": 8.3, "FY1983": 1.4, "FY1982": 0.1, "FY1981": 0.4,
            # HD-078 (2026-09-07): FY1980-FY1974 'Deferred Taxation' - a separate Bank balance sheet line
            # from FY1974 onward; not yet a distinct line in FY1973-FY1972 (nil/not applicable those two
            # years - the concept is not presented on the face of the Bank balance sheet that early).
            "FY1980": 0.260, "FY1979": 0.447, "FY1978": 0.873, "FY1977": 0.658, "FY1976": 0.593,
            "FY1975": 0.560, "FY1974": 0.025,
        }),
        ("DATA", "Current tax liabilities", {
            "FY2015": 0.3, "FY2014": 0.3,
            "FY2013": 4.2, "FY2010": 17.3, "FY2007": 2.9,
            # HD-078 follow-up (2026-09-07): FY1989, FY1987, FY1986's own separately-disclosed 'Taxation'
            # line (Bank Company-only) - see HD078_1981_1990_NOTE. FY1990: the own edition's Bank balance
            # sheet (12 Jan 1991, printed p.26) prints 'Current taxation' as a literal DASH, carried as
            # '-' (was 0.0 until GA-024 - a printed dash is content, not a measured zero). FY1988 and FY1985-FY1981: not
            # separately disclosed that year - folded into the aggregate deposits residual (FY1988) or
            # genuinely not itemised as a distinct balance sheet line (FY1985-FY1981) - left blank.
            "FY1990": "-", "FY1989": 9.1, "FY1987": 6.7, "FY1986": 5.9,
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
        ("DATA", "Proposed dividend", {
            # HD-078 (2026-09-07): FY1980 only - a separately-disclosed 'Proposed Dividend' line on
            # that year's own Bank balance sheet (not present as a separate line FY1979 and earlier -
            # folded into that era's aggregate Creditors/Current-liabilities figures instead - see
            # HD078_1972_1980_NOTE).
            "FY1980": 0.400,
        }),
        ("TOTAL", "Total liabilities", {
            "FY2024": 24780.0, "FY2023": 25117.3, "FY2022": 27692.9, "FY2021": 28494.7, "FY2020": 26326.9,
            "FY2019": 24772.9, "FY2018": 23291.6, "FY2017": 25436.1, "FY2016": 26629.8, "FY2015": 27665.0,
            "FY2014": 35568.4,
            "FY2013": 41618.8, "FY2012": 50189.4, "FY2011": 48805.3, "FY2010": 46711.4, "FY2009": 45300.2,
            "FY2008": 15687.7, "FY2007": 11863.5, "FY2006": 11643.6, "FY2005": 10782.6, "FY2004": 9837.1,
            "FY2003": 8569.3,
            "FY2002": 7887.0, "FY2001": 7132.5, "FY2000": 6170.4, "FY1999": 5707.4, "FY1998": 5074.2,
            "FY1997": 4866.9, "FY1996": 4115.8, "FY1995": 3552.0, "FY1994": 2949.8, "FY1993": 3079.7,
            "FY1992": 2826.7, "FY1991": 2431.0,
            # HD-078 follow-up (2026-09-07): FY1990-FY1981 = component sum (Current-deposit-other
            # accounts + Deposits by CWS trustees [FY1981 only] + Loan Stock/Other borrowed funds +
            # Provisions + Current tax liabilities + Other liabilities); ties exactly to Total assets less
            # Total equity every year - see HD078_1981_1990_NOTE.
            "FY1990": 2626.6, "FY1989": 2386.5, "FY1988": 1955.5, "FY1987": 1453.5, "FY1986": 1371.3,
            "FY1985": 1036.3, "FY1984": 991.3, "FY1983": 847.9, "FY1982": 765.9, "FY1981": 653.4,
            # HD-078 (2026-09-07): FY1980-FY1972 = Total assets less Total equity (component sum of
            # Subordinated Loans/Deposits by trustees/Current-deposit-other accounts/Creditors/Proposed
            # dividend/Deferred Taxation ties exactly in every year).
            "FY1980": 536.243, "FY1979": 464.338, "FY1978": 347.664, "FY1977": 307.712, "FY1976": 273.804,
            "FY1975": 237.275, "FY1974": 215.542, "FY1973": 199.271, "FY1972": 163.839,
        }),
        ("SECTION", "Equity", {}),
        ("DATA", "Ordinary share capital", {
            "FY2024": 25.6, "FY2023": 25.6, "FY2022": 25.6, "FY2021": 25.6, "FY2020": 25.6,
            "FY2019": 25.6, "FY2018": 25.6, "FY2017": 25.6, "FY2016": 22.6, "FY2015": 22.6, "FY2014": 22.6,
            "FY2013": 12.5, "FY2012": 410.0, "FY2011": 410.0, "FY2010": 410.0, "FY2009": 230.0,
            "FY2008": 55.0, "FY2007": 55.0, "FY2006": 55.0, "FY2005": 55.0, "FY2004": 55.0, "FY2003": 55.0,
            "FY2002": 35.0, "FY2001": 35.0, "FY2000": 35.0, "FY1999": 35.0, "FY1998": 35.0,
            # FY1997: £5.0m ordinary share issue during the year (£30.0m at FY1996).
            "FY1997": 35.0, "FY1996": 30.0, "FY1995": 30.0, "FY1994": 30.0, "FY1993": 30.0, "FY1992": 30.0,
            "FY1991": 30.0,
            # HD-078 follow-up (2026-09-07): FY1990-FY1987 £30.0m following the 14 July 1987 subdivision
            # of 25,000,000 £1 ordinary shares into 100,000,000 25p shares plus a November 1987 issue of
            # 20,000,000 new 25p shares at par (£25.0m -> £30.0m). FY1986-FY1985 £25.0m following the
            # Dec 1984/Jan 1985 issue of 13,800,000 £1 shares at par to CWS (£11.2m -> £25.0m, captured
            # within FY1984 since the Bank's FY1984 year-end falls in Jan 1985). FY1983 unchanged at
            # £11.2m following the Jan 1983 issue of 3,200,000 £1 shares at par to CWS (£8.0m -> £11.2m,
            # captured within FY1982 since the Bank's FY1982 year-end falls in Jan 1983). FY1981 unchanged
            # at £8.0m - see HD078_1981_1990_NOTE.
            "FY1990": 30.0, "FY1989": 30.0, "FY1988": 30.0, "FY1987": 30.0, "FY1986": 25.0, "FY1985": 25.0,
            "FY1984": 25.0, "FY1983": 11.2, "FY1982": 11.2, "FY1981": 8.0,
            # HD-078 (2026-09-07): FY1980-FY1973 unchanged at £8.0m following the FY1973 bonus/
            # capitalisation issue (doubled from £4.0m, funded by a £4.02m capitalisation of Reserves -
            # see HD078_1972_1980_NOTE). FY1972 = £4.0m, the pre-capitalisation-issue amount.
            "FY1980": 8.000, "FY1979": 8.000, "FY1978": 8.000, "FY1977": 8.000, "FY1976": 8.000,
            "FY1975": 8.000, "FY1974": 8.000, "FY1973": 8.000, "FY1972": 4.000,
        }),
        ("DATA", "Preference share capital (non-equity)", {
            "FY2004": 60.0, "FY2003": 60.0,
            "FY2002": 60.0, "FY2001": 60.0, "FY2000": 60.0, "FY1999": 60.0, "FY1998": 60.0, "FY1997": 60.0,
            "FY1996": 60.0, "FY1995": 60.0, "FY1994": 60.0, "FY1993": 60.0, "FY1992": 60.0, "FY1991": 60.0,
            # HD-078 follow-up (2026-09-07): preference shares first issued April 1988 (40,000,000 8.48%
            # cumulative redeemable £1 shares at 100.06p, converted 23 June 1989 to 9.25% non-cumulative
            # irredeemable); a further 20,000,000 9.25% preference shares issued 31 May 1989 (total
            # 60,000,000, £60.0m). No preference share capital in any year before FY1988 - see
            # HD078_1981_1990_NOTE.
            "FY1990": 60.0, "FY1989": 60.0, "FY1988": 40.0,
        }),
        ("DATA", "Share premium account", {
            "FY2020": 2416.9,
            "FY2019": 2416.9, "FY2018": 2416.9, "FY2017": 2416.9, "FY2016": 1736.9, "FY2015": 1736.9,
            "FY2014": 1736.9,
            "FY2013": 1359.8, "FY2012": 8.8, "FY2011": 8.8, "FY2010": 8.8, "FY2009": 8.8,
            "FY2008": 8.8, "FY2007": 8.8, "FY2006": 8.8, "FY2005": 8.8, "FY2004": 8.8, "FY2003": 8.8,
            "FY2002": 8.8, "FY2001": 8.8, "FY2000": 8.8, "FY1999": 8.8, "FY1998": 8.8, "FY1997": 8.8,
            "FY1996": 8.8, "FY1995": 8.8, "FY1994": 8.8, "FY1993": 8.8, "FY1992": 8.8,
            # FY1991: not itemised separately from Retained earnings in that year's own 'Reserves' line -
            # inferred at £8.8m, consistent with the unchanged balance disclosed in every adjacent year -
            # see HD078_1991_2002_NOTE.
            "FY1991": 8.8,
            # HD-078 follow-up (2026-09-07): FY1990-FY1983 £8.8m-£9.7m range, a genuine year-to-year drift
            # in the source's own disclosed figure (£9,636,000-£9,824,000 across FY1983-1987, and a
            # discrepancy between FY1988's own report (£9,176,000) vs FY1989's report's restated FY1988
            # comparative (£8,814,000)) - treated as immaterial at this workbook's 1-decimal £m precision;
            # FY1988-FY1990 use the £8.8m value consistent with FY1991 onward. FY1982 and FY1981: no
            # independently-disclosed share premium sub-split found in either year's own primary source or
            # its adjacent-year comparative - left fully undifferentiated within Retained earnings below
            # for these two years only - see HD078_1981_1990_NOTE.
            "FY1990": 8.8, "FY1989": 8.8, "FY1988": 8.8, "FY1987": 9.6, "FY1986": 9.7, "FY1985": 9.7,
            "FY1984": 9.7, "FY1983": 9.8,
        }),
        ("DATA", "Retained earnings", {
            "FY2024": 1328.6, "FY2023": 1398.2, "FY2022": 1241.1, "FY2021": 1218.8, "FY2020": -1823.6,
            "FY2019": -1736.2, "FY2018": -1594.9, "FY2017": -1514.4, "FY2016": -1315.1, "FY2015": -896.4,
            "FY2014": -273.1,
            "FY2013": -39.4, "FY2012": 1116.9, "FY2011": 1655.0, "FY2010": 1661.4, "FY2009": 1588.5,
            "FY2008": 610.7, "FY2007": 597.9, "FY2006": 608.3, "FY2005": 506.8,
            # FY2003-FY2004 label this 'Profit and loss account' (UK GAAP) - same substance.
            "FY2004": 537.7, "FY2003": 475.2,
            "FY2002": 414.6, "FY2001": 334.6, "FY2000": 267.4, "FY1999": 211.2, "FY1998": 159.1,
            "FY1997": 119.0, "FY1996": 88.5, "FY1995": 67.2, "FY1994": 53.2, "FY1993": 44.5, "FY1992": 43.2,
            # FY1991: inferred as 'Reserves' (£51.6m) less the inferred £8.8m share premium above - see
            # HD078_1991_2002_NOTE.
            "FY1991": 42.8,
            # HD-078 follow-up (2026-09-07): FY1990-FY1983 = disclosed Reserves less the Share premium
            # account figure above. FY1982-FY1981 = the Bank's undifferentiated 'Reserves' note figure in
            # full (no independently-disclosed share premium sub-split for these two years - see
            # HD078_1981_1990_NOTE). A genuine FY1984 reserves transfer of £13.153m to the profit and loss
            # account (funding a Group deferred-tax provision required by Finance Act 1984 changes) is
            # reflected in the FY1984 figure below, per that year's own Reserves note.
            "FY1990": 49.4, "FY1989": 59.3, "FY1988": 57.1, "FY1987": 47.0, "FY1986": 42.8, "FY1985": 35.5,
            "FY1984": 30.6, "FY1983": 36.5, "FY1982": 39.0, "FY1981": 34.9,
            # HD-078 (2026-09-07): FY1980-FY1972 = the Bank's single, undivided 'Reserves' note figure
            # (no separate Share premium disclosed this era - see HD078_1972_1980_NOTE) - i.e. the sum
            # of the 'Reserves proper' and 'Investment suspense account' sub-components tracked on the
            # Statement of Changes in Equity sheet. FY1978 restated from 21.563 to 23.021 by a FY1979
            # SSAP15/bad-debt-provision prior-year adjustment (+1.458); figure shown here for FY1978 is
            # the AS-ORIGINALLY-REPORTED 21.563, with the restatement itself shown as its own row on the
            # Statement of Changes in Equity sheet, consistent with the FY2001 restatement treatment
            # above.
            "FY1980": 33.583, "FY1979": 28.594, "FY1978": 21.563, "FY1977": 19.410, "FY1976": 18.110,
            "FY1975": 16.712, "FY1974": 15.754, "FY1973": 14.650, "FY1972": 17.277,
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
            # FY2002 = ordinary 35.0 + preference 60.0 + share premium 8.8 + retained earnings 414.6.
            "FY2002": 518.4,
            # FY2001 restated - see 'Restatement' row on the Statement of Changes in Equity sheet and
            # HD078_1991_2002_NOTE (FY2001 as originally reported = 438.4; carried forward into FY2002's
            # own opening balance as 440.0).
            "FY2001": 438.4, "FY2000": 371.2, "FY1999": 315.0, "FY1998": 262.9, "FY1997": 222.8,
            "FY1996": 187.3, "FY1995": 166.0,
            # FY1994/FY1992: component sum (30.0+60.0+8.8+53.2=152.0; 30.0+60.0+8.8+43.2=142.0) rounds
            # 0.1 below Total assets less Total liabilities (3101.9-2949.8=152.1; 2968.8-2826.7=142.1) -
            # a sub-£0.1m independent-rounding artefact between the two source totals, not a real
            # discrepancy; the Total equity row here is plugged to the disclosed totals so Total assets =
            # Total liabilities + Total equity ties exactly, consistent with the FY1991 anchoring approach
            # documented in HD078_1991_2002_NOTE.
            "FY1994": 152.1, "FY1993": 143.3, "FY1992": 142.1,
            "FY1991": 141.6,
            # HD-078 follow-up (2026-09-07): FY1990-FY1981 = component sum (Ordinary share capital +
            # Preference share capital + Share premium account + Retained earnings); ties exactly to Total
            # assets less Total liabilities every year - see HD078_1981_1990_NOTE.
            "FY1990": 148.2, "FY1989": 158.1, "FY1988": 135.9, "FY1987": 86.6, "FY1986": 77.5, "FY1985": 70.2,
            "FY1984": 65.3, "FY1983": 57.5, "FY1982": 50.2, "FY1981": 42.9,
            # HD-078 (2026-09-07): FY1980-FY1972 = Ordinary share capital + Retained earnings (no
            # Preference share capital, Share premium, or Other reserves lines disclosed this era) -
            # ties exactly to Total assets less Total liabilities in every year.
            "FY1980": 41.583, "FY1979": 36.594, "FY1978": 29.563, "FY1977": 27.410, "FY1976": 26.110,
            "FY1975": 24.712, "FY1974": 23.754, "FY1973": 22.650, "FY1972": 21.277,
        }),
        ("TOTAL", "Total liabilities and equity", {
            "FY2024": 26052.9, "FY2023": 26549.0, "FY2022": 28987.2, "FY2021": 30241.7, "FY2020": 27778.2,
            "FY2019": 26353.4, "FY2018": 24998.6, "FY2017": 26899.7, "FY2016": 27588.3, "FY2015": 29028.3,
            "FY2014": 37582.9,
            "FY2013": 43396.1, "FY2012": 51818.5, "FY2011": 50965.7, "FY2010": 48814.9, "FY2009": 47167.7,
            "FY2008": 16403.6, "FY2007": 12523.8, "FY2006": 12293.2, "FY2005": 11365.1, "FY2004": 10498.6,
            "FY2003": 9168.3,
            "FY2002": 8405.4, "FY2001": 7570.9, "FY2000": 6541.6, "FY1999": 6022.4, "FY1998": 5337.1,
            "FY1997": 5089.7, "FY1996": 4303.1, "FY1995": 3718.0, "FY1994": 3101.9, "FY1993": 3223.0,
            "FY1992": 2968.8, "FY1991": 2572.6,
            # HD-078 follow-up (2026-09-07): FY1990-FY1981 = disclosed Total assets figures (identical to
            # the 'Total assets' row above - independently re-checked, ties exactly every year) - see
            # HD078_1981_1990_NOTE.
            "FY1990": 2774.8, "FY1989": 2544.6, "FY1988": 2091.4, "FY1987": 1540.1, "FY1986": 1448.8,
            "FY1985": 1106.5, "FY1984": 1056.6, "FY1983": 905.4, "FY1982": 816.1, "FY1981": 696.3,
            # HD-078 (2026-09-07): FY1980-FY1972 = disclosed Total assets figures (identical to the
            # 'Total assets' row above - independently re-checked, ties exactly every year).
            "FY1980": 577.826, "FY1979": 500.932, "FY1978": 377.227, "FY1977": 335.122, "FY1976": 299.914,
            "FY1975": 261.987, "FY1974": 239.296, "FY1973": 221.921, "FY1972": 185.116,
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
             "(FY2012-FY2016), Bank-only s.230/s.408 note profit (FY1992-FY2011), and Consolidated GROUP P&L "
             "(FY1972-FY1991, the years no Bank-only income statement exists at all) - see source note, £m",
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
        ("SECTION", "Cost:income ratio - as separately headline-disclosed each year (basis varies; "
                    "see source note) - NOT derived from the detail rows above, which only exist "
                    "FY2014-FY2016", {}),
        ("DATA", "Cost:income ratio (as reported)", {
            "FY2024": "86.7%", "FY2023": "86.1%", "FY2022": "73%", "FY2021": "91%", "FY2020": "113.8%",
            "FY2019": "106.2%", "FY2018": "97.1%", "FY2017": "108.1%", "FY2016": "103.7%",
            "FY2015": "100.0%", "FY2014": "100.1%", "FY2013": "97.8%",
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
        ("SECTION", "HD-078 (2026-09-07; extended to FY1991 on 2026-09-19): Consolidated Group P&L, "
                    "FY1991-FY1972 (Group basis, NOT Bank Company-only, since no Bank-only income "
                    "statement is disclosed at all this era - see HD078_1972_1980_NOTE and "
                    "HD078_PL_1981_2011_NOTE. The 'Profit/(loss) for the year' row above is deliberately "
                    "left blank for these years rather than populated with a Group figure that would "
                    "conflate two different consolidation bases; the one genuinely Bank-only line these "
                    "editions print - 'Profits/(Losses) Retained By The Bank' - is carried on its own row "
                    "at the foot of this block.)", {}),
        ("DATA", "Operating profit/Profit for the year (Group, before exceptional items)", {
            # HD-078 (2026-09-07): each year's own source label varies ('Operating Profit' FY1974-1980;
            # 'Profit for the year' FY1972-1973, where no separate exceptional-item line is disclosed).
            # HD-078 follow-up (2026-09-19), FY1991-FY1981: the label varies again by era - 'Profit/(Loss)
            # before Exceptional Item and certain Subsidiary Undertakings' (FY1991); 'Operating (Loss)/Profit'
            # (FY1990's own edition, which does not carve out Unity Trust - GA-024); 'Operating
            # Profit (Bank and Subsidiaries)' (FY1989-FY1988); 'Profit before Taxation and Sovereign Debt
            # Provisions - Bank and Subsidiaries' (FY1987); 'Profit before Taxation - The Bank and
            # Subsidiaries' (FY1986-FY1985); 'Operating Profit' (FY1982-FY1981). FY1984 and FY1983 are
            # blank because those two editions start the statement at Profit before Taxation and print no
            # line above it - a presentation gap, not a missing figure.
            "FY1991": 2.137, "FY1990": -14.687, "FY1989": 20.187, "FY1988": 23.597, "FY1987": 15.675,
            "FY1986": 14.271, "FY1985": 12.941, "FY1982": 1.689, "FY1981": 4.003,
            "FY1980": 5.422, "FY1979": 6.244, "FY1978": 5.429, "FY1977": 3.974, "FY1976": 3.018,
            "FY1975": 3.569, "FY1974": 4.763, "FY1973": 4.867, "FY1972": 3.699,
        }),
        ("DATA", "Sovereign debt provisions (Group)", {
            # HD-078 follow-up (2026-09-19): a separate line on the face of the statement FY1989-FY1987
            # only. FY1987's own edition (year ended 9 Jan 1988) has this cell physically damaged on the
            # Companies House scan; the value below is the FY1988 edition's own FY1987 COMPARATIVE column,
            # which is legible, and is cited as a comparative - it is NOT back-solved from the subtotals.
            "FY1989": -1.500, "FY1988": -1.655, "FY1987": -1.384,
        }),
        ("DATA", "Unity Trust Bank plc and its subsidiaries (Group)", {
            # HD-078 follow-up (2026-09-19): FY1991 only - that edition carves Unity Trust out of the
            # headline profit line. FY1990's OWN edition does not (its (14,687) includes it); the FY1991
            # edition's FY1990 comparative shows (646) here, recorded in the P&L note, not in this cell.
            "FY1991": -1.708,
        }),
        ("DATA", "Exceptional items", {
            # HD-078 (2026-09-07): FY1976 = Pension Fund provision (0.350); FY1975 = Additional
            # provision (1.400); FY1974 = Additional provision (2.650) + Special contribution to
            # Pension Fund (0.146). Not disclosed as a separate line FY1972-1973 or FY1977-1980.
            # HD-078 follow-up (2026-09-19): FY1991 = Restructuring Costs (6.328); FY1988 = a CREDIT
            # (0.969, surplus on disposal of loans to and investment in an associated company); FY1981 =
            # 0.377 charge. FY1990's own edition prints no such line (blank; the dash was the FY1991
            # edition's comparative). FY1989/FY1982 print a literal DASH, carried as '-' because a printed
            # dash is the bank saying the line is nil, not silence. FY1987-FY1983 print no such line at
            # all in their own editions, so those cells are blank rather than dashed.
            "FY1991": -6.328, "FY1989": "-", "FY1988": 0.969, "FY1982": "-",
            "FY1981": -0.377,
            "FY1976": -0.350, "FY1975": -1.400, "FY1974": -2.796,
        }),
        ("DATA", "Share of profits/(losses) of associated companies", {
            # HD-078 (2026-09-07): not disclosed as a separate line on the face of this statement
            # FY1978-FY1980 (folded into Operating profit that era).
            # HD-078 follow-up (2026-09-19): reappears FY1991-FY1985 ('Associated Undertakings' FY1991-
            # FY1990, 'Associated Companies' FY1989-FY1985). FY1984-FY1981 print no separate line.
            "FY1991": -0.073, "FY1990": -0.185, "FY1989": -0.144, "FY1988": 0.295, "FY1987": 0.009,
            "FY1986": -0.500, "FY1985": -0.025,
            "FY1977": 0.028, "FY1976": 0.002, "FY1975": -0.011, "FY1974": -0.714, "FY1973": -0.113,
            "FY1972": 0.149,
        }),
        ("TOTAL", "Profit before taxation (and extraordinary item, FY1974)", {
            "FY1991": -5.972, "FY1990": -14.872, "FY1989": 18.543, "FY1988": 23.206, "FY1987": 14.300,
            "FY1986": 13.771, "FY1985": 12.916, "FY1984": 13.035, "FY1983": 7.524, "FY1982": 1.689,
            "FY1981": 3.626,
            "FY1980": 5.769, "FY1979": 6.028, "FY1978": 3.569, "FY1977": 4.002, "FY1976": 2.670,
            "FY1975": 2.158, "FY1974": 1.253, "FY1973": 4.754, "FY1972": 3.848,
        }),
        ("DATA", "Taxation", {
            # HD-078 (2026-09-07): FY1980/FY1979 shown as tax CREDITS (reconciling the disclosed
            # Operating profit to the disclosed post-tax subtotal); all other years are tax charges.
            # HD-078 follow-up (2026-09-19): FY1991/FY1990/FY1982 are CREDITS (loss-making or reversing
            # years). The scanned editions change their bracket convention mid-range - up to FY1985 a
            # deduction is printed unbracketed and an addition bracketed; from FY1986 brackets mean a
            # deduction. Each column's direction below was settled by footing that column to its own
            # printed Retained Earnings figure, never assumed from the brackets.
            "FY1991": 3.343, "FY1990": 9.744, "FY1989": -7.644, "FY1988": -9.075, "FY1987": -5.981,
            "FY1986": -5.411, "FY1985": -5.078, "FY1984": -4.616, "FY1983": -0.117, "FY1982": 0.317,
            "FY1981": -0.301,
            "FY1980": 0.347, "FY1979": -0.216, "FY1978": -1.860, "FY1977": -2.036, "FY1976": -1.457,
            "FY1975": -1.047, "FY1974": -0.676, "FY1973": -2.269, "FY1972": -1.108,
        }),
        ("DATA", "Minority interest", {
            "FY1991": 0.955, "FY1990": 0.276, "FY1989": -0.312, "FY1988": 0.211, "FY1987": -0.159,
            "FY1986": -0.151, "FY1985": -0.042, "FY1984": 0.019, "FY1983": -0.020, "FY1982": -0.019,
            "FY1981": 0.022,
            "FY1980": -0.025, "FY1979": -0.087, "FY1978": -0.173, "FY1977": -0.163, "FY1976": -0.090,
            "FY1975": -0.085, "FY1974": 0.015, "FY1973": -0.187, "FY1972": -0.233,
        }),
        ("DATA", "Extraordinary item", {
            # HD-078 (2026-09-07): FY1974 only - disclosed as a separate item below the tax/minority-
            # interest line, per that year's own presentation (Note 7).
            # HD-078 follow-up (2026-09-19): FY1989-FY1981. FY1981's 2.321 charge is the net of the
            # £3,192,000 Special Tax on Banking Deposits (the 1981 windfall tax already flagged in
            # HD078_1981_1990_NOTE) less an £871,000 'Other' credit; FY1982 is a £59,000 credit with the
            # Special Tax line printing a dash. FY1989 prints a literal dash. FY1991/FY1990 print no
            # extraordinary-items line at all.
            "FY1989": "-", "FY1988": -0.050, "FY1987": 1.004, "FY1986": -0.030, "FY1985": -0.607,
            "FY1984": -13.017, "FY1983": -2.889, "FY1982": 0.059, "FY1981": -2.321,
            "FY1974": 0.186,
        }),
        ("DATA", "Transfer from reserves (Group)", {
            # HD-078 follow-up (2026-09-19): FY1984 only as a figure - the £13.0m Reserves -> P&L
            # transfer that funded the Finance Act 1984 Group deferred-tax provision, already narrated in
            # HD078_1981_1990_NOTE. Shown on the face of the FY1984 and FY1985 statements as its own
            # line; FY1985 prints a dash.
            "FY1985": "-", "FY1984": 13.000,
        }),
        ("DATA", "Preference dividend", {
            # HD-078 follow-up (2026-09-19): first appears FY1988 (the 40.0m 8.48% cumulative redeemable
            # £1 preference issue of Apr 1988), rising to 4.711 in FY1989 after the Jun-1989 conversion
            # to 9.25% non-cumulative irredeemable plus the May-1989 20.0m top-up. FY1990's own edition
            # prints 'Dividend on Preference Shares' (5,535). FY1991 reverts to a single undifferentiated
            # 'Dividend' line carried on the Proposed/final dividend row below, so this row is blank there.
            "FY1990": -5.535, "FY1989": -4.711, "FY1988": -1.815,
        }),
        ("TOTAL", "Profit attributable to ordinary shareholders (Group)", {
            # HD-078 follow-up (2026-09-19): printed on the face of the statement only FY1990-FY1988.
            # FY1987's figure (9.164) exists solely in the FY1988 edition's comparative column and is
            # left out here rather than mixed into an own-edition row - see HD078_PL_1981_2011_NOTE.
            "FY1990": -10.387, "FY1989": 5.876, "FY1988": 12.477,
        }),
        ("DATA", "Proposed/final dividend", {
            # HD-078 (2026-09-07): FY1980 = first year with a proposed dividend (£0.4m, 5p per £1
            # share); FY1972 = Nil (the comparative 26-week stub period to 8 Jan 1972 had a final
            # dividend of £0.2m/5%, not shown here since it is not a full prior year - see
            # HD078_1972_1980_NOTE).
            # HD-078 follow-up (2026-09-19): FY1991 is the single undifferentiated 'Dividend' line
            # (ordinary + preference together); FY1990's own edition prints 'Dividend on Ordinary Shares'
            # as a literal dash (GA-024); FY1989-FY1988 are 'Proposed Dividend on Ordinary
            # Shares' with preference split out on its own row above. FY1981 prints a literal dash.
            # FY1982's own edition omits the line entirely, so that cell is blank, not dashed.
            "FY1991": -5.535, "FY1990": "-", "FY1989": -2.500, "FY1988": -2.500, "FY1987": -2.000,
            "FY1986": -1.900, "FY1985": -1.850, "FY1984": -0.840, "FY1983": -0.560, "FY1981": "-",
            "FY1980": -0.400,
        }),
        ("TOTAL", "Retained earnings (Group)", {
            "FY1991": -7.209, "FY1990": -10.387, "FY1989": 3.376, "FY1988": 9.977, "FY1987": 7.164,
            "FY1986": 6.279, "FY1985": 5.339, "FY1984": 7.581, "FY1983": 3.938, "FY1982": 2.046,
            "FY1981": 1.026,
            "FY1980": 5.344, "FY1979": 5.941, "FY1978": 3.396, "FY1977": 1.803, "FY1976": 1.123,
            "FY1975": 1.026, "FY1974": 0.778, "FY1973": 2.298, "FY1972": 2.507,
        }),
        ("DATA", "of which retained by the Bank (Bank Company-only - the ONLY Bank-only figure these "
                 "editions print)", {
            # HD-078 follow-up (2026-09-19): the 'Profits Retained - By The Bank' line at the foot of
            # each Consolidated P&L. This is a RETAINED (post-dividend) appropriation, NOT a profit for
            # the year, so it is deliberately NOT written into the 'Profit/(loss) for the year' row
            # above. It is the era's only genuinely Bank Company-only income-statement disclosure.
            "FY1991": -6.630, "FY1990": -9.883, "FY1989": 2.532, "FY1988": 9.811, "FY1987": 8.056,
            "FY1986": 7.372, "FY1985": 4.910, "FY1984": 7.237, "FY1983": 7.364, "FY1982": 4.293,
            "FY1981": 1.508, "FY1980": 5.032, "FY1979": 5.911,
        }),
        ("SECTION", "HD-078 follow-up (2026-09-19): Bank Company-only profit for the financial year, "
                    "FY2011-FY1992 - the Companies Act s.230 (CA1985) / s.408 (CA2006) NOTE disclosure. "
                    "The Bank took the exemption from presenting its own individual profit and loss "
                    "account in every one of these years, but that exemption REQUIRES the amount of the "
                    "Group profit dealt with in the Bank's own accounts to be disclosed in a note - so "
                    "these are independently disclosed figures, not residuals backed out of the equity "
                    "roll-forward. The note's own basis label changes twice across the range, so the "
                    "three rows below are deliberately NOT merged into one; see "
                    "HD078_PL_1981_2011_NOTE.", {}),
        ("TOTAL", "Profit/(loss) attributable to EQUITY shareholders, Bank Company-only (s.230/s.408 "
                  "note; FY2009-FY2011 after significant items)", {
            "FY2011": -93.3, "FY2010": 73.1, "FY2009": 166.6, "FY2008": 12.4, "FY2007": -1.1,
            "FY2006": 119.0, "FY2005": 60.9,
        }),
        ("DATA", "of which: before significant items (as separately disclosed FY2011-FY2006)", {
            "FY2011": 11.9, "FY2010": 108.1, "FY2009": 194.0, "FY2008": 46.1, "FY2007": 25.5,
            "FY2006": 44.4,
        }),
        ("TOTAL", "Profit for the financial year attributable to SHAREHOLDERS, Bank Company-only "
                  "(s.230 note wording FY2004-FY1999; preference holders NOT excluded)", {
            # FY2004's own edition (UK GAAP) says 88.0; the FY2005 edition restates that comparative to
            # 78.7 on first-time IFRS. Both are source-disclosed; the workbook's own-edition convention
            # keeps 88.0 here and records the restatement in HD078_PL_1981_2011_NOTE rather than
            # silently adopting one of the two.
            "FY2004": 88.0, "FY2003": 86.1, "FY2002": 83.9, "FY2001": 72.7, "FY2000": 61.8,
            "FY1999": 57.618,
        }),
        ("TOTAL", "Profit attributable to ORDINARY shareholders, Bank Company-only (s.230 note wording "
                  "FY1998-FY1993; i.e. AFTER the preference dividend - not comparable with the row "
                  "above)", {
            "FY1998": 40.088, "FY1997": 30.452, "FY1996": 26.308, "FY1995": 17.979, "FY1994": 11.697,
            "FY1993": 3.802,
        }),
        ("DATA", "FY1992 - same measure, taken from the FY1993 edition's own FY1992 COMPARATIVE column "
                 "(FY1992's own filing was not retrieved; same limitation the Balance Sheet sheet "
                 "already records for FY1992)", {
            "FY1992": 0.472,
        }),
    ],
    sources_text=PL_SOURCES,
    first_col_width=68,
    source_height=280,
    unit_suffix=" (£m)",
)

# HD-078 follow-up (2026-09-19): the FY2011-FY1981 evidence goes in its own
# citation cell directly under the main one - see append_source_cell's docstring
# for why it cannot simply be appended to PL_SOURCES.
bw.append_source_cell(bw.wb["Profit & Loss"], HD078_PL_1981_2011_NOTE, height=560)

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
        # HD-078 follow-up (2026-09-07): FY1991-FY2002 roll-forward below, reconstructed the same way
        # as the FY2003-FY2013 block above, from each year's own Balance Sheet sheet equity components
        # (Ordinary + Preference share capital combined into the single "Share capital" column here, to
        # match how the existing FY2003 row already combines its own 55.0 ordinary + 60.0 preference into
        # 115.0). FY1992 and FY1994's Total equity is plugged £0.1m above its own component sum (142.0->
        # 142.1; 152.0->152.1) to tie exactly to the Balance Sheet sheet's own Total assets less Total
        # liabilities - see the matching comment on that sheet and HD078_1991_2002_NOTE; the adjacent
        # "Net movement" rows absorb that same £0.1m as an offsetting rounding artefact, not a real
        # additional movement. Profit and loss and Cash Flow Statement are NOT extended for this range
        # (see HD078_1991_2002_NOTE) so, as with FY2004-2008 above, movements are shown as a single
        # aggregate "Net movement" line rather than split into profit/dividend/issuance components the
        # sources do not tabulate for the Bank Company-only column across this whole range.
        # HD-078 follow-up (2026-09-07): FY1990-FY1981 roll-forward below, reconstructed the same way as
        # the FY1991-2002 block above, from each year's own already-verified Balance Sheet sheet equity
        # components (Ordinary + Preference share capital combined into the single "Share capital" column
        # here, matching the FY1991 anchor row's own style). The opening anchor below is sourced from the
        # Bank's own FY1981 Annual Report's FY1980 comparative column. Movements combine genuine profit/
        # loss, dividends, and share issuances/reclassifications into a single aggregate line per year
        # (Profit & Loss is not independently disclosed on a Bank Company-only basis for this era - see
        # HD078_1981_1990_NOTE) - each labelled with the specific structural event(s) it embeds where one
        # occurred. FY1982 and FY1981 pre-date the Bank's own separate disclosure of a Share premium
        # sub-balance, so their "Share premium" column is left blank (undifferentiated within Retained
        # earnings, per the Balance Sheet sheet's own note); the reclassification when Share premium is
        # first separately disclosed (FY1983) is folded into that year's Net movement line rather than
        # shown as a distinct restatement row, since the underlying total is unaffected.
        # HD-078 follow-up (2026-09-07): FY1980-FY1972 roll-forward below, the workbook's genuine hard
        # floor - see HD078_1972_1980_NOTE. Reconstructed from each year's own Reserves note (Note 6, 7,
        # 8 or 9 depending on the year), cross-validated against the Balance Sheet sheet's own single
        # "Reserves" figure for every one of these 9 years (all tie exactly). "Retained earnings" here is
        # the Bank's whole undivided Reserves figure (no separate Share premium disclosed this era). Two
        # genuine discontinuities are shown as explicit rows: the FY1973 bonus/capitalisation share issue,
        # and the FY1979-disclosed restatement of the FY1978 closing Reserves figure (SSAP15 deferred tax
        # policy change plus a released general bad-debt provision, +£1.458m combined).
        ("TOTAL", "At 8 January 1972 (Bank company-only; Companies Act 1948 basis; the workbook's "
                  "earliest reachable balance - FY1972's own comparative column is only a 26-week stub "
                  "period, 10 July 1971 - 8 January 1972, not a full prior year, so no earlier opening "
                  "balance exists - see HD078_1972_1980_NOTE)",
         (4.0, None, None, None, None, None, 17.277, None, 21.277)),
        ("DATA", "Net movement during the year (FY1973, incl. £4.0m bonus/capitalisation share issue - "
                 "Ordinary share capital doubled from £4.0m to £8.0m, funded by a £4.02m capitalisation "
                 "of Reserves)",
         (4.0, None, None, None, None, None, -2.627, None, 1.373)),
        ("TOTAL", "At 31 December 1973 (post-capitalisation issue)",
         (8.0, None, None, None, None, None, 14.650, None, 22.650)),
        ("DATA", "Net movement during the year (FY1974)",
         (0.0, None, None, None, None, None, 1.104, None, 1.104)),
        ("TOTAL", "At 31 December 1974",
         (8.0, None, None, None, None, None, 15.754, None, 23.754)),
        ("DATA", "Net movement during the year (FY1975)",
         (0.0, None, None, None, None, None, 0.958, None, 0.958)),
        ("TOTAL", "At 31 December 1975",
         (8.0, None, None, None, None, None, 16.712, None, 24.712)),
        ("DATA", "Net movement during the year (FY1976)",
         (0.0, None, None, None, None, None, 1.398, None, 1.398)),
        ("TOTAL", "At 31 December 1976",
         (8.0, None, None, None, None, None, 18.110, None, 26.110)),
        ("DATA", "Net movement during the year (FY1977)",
         (0.0, None, None, None, None, None, 1.300, None, 1.300)),
        ("TOTAL", "At 14 January 1978 (FY1977 year-end, per that filing's own Directors' Report)",
         (8.0, None, None, None, None, None, 19.410, None, 27.410)),
        ("DATA", "Net movement during the year (FY1978, as originally reported - see restatement below)",
         (0.0, None, None, None, None, None, 2.153, None, 2.153)),
        ("TOTAL", "At 31 December 1978 (as originally reported; restated below per the FY1979 Annual "
                  "Report's own disclosure)",
         (8.0, None, None, None, None, None, 21.563, None, 29.563)),
        ("DATA", "Restatement (SSAP15 deferred tax policy change + released general bad-debt provision, "
                 "per the FY1979 Annual Report's own prior-year adjustment disclosure)",
         (0.0, None, None, None, None, None, 1.458, None, 1.458)),
        ("TOTAL", "At 31 December 1978, restated",
         (8.0, None, None, None, None, None, 23.021, None, 31.021)),
        ("DATA", "Net movement during the year (FY1979, incl. the Bank's first Subordinated Loan "
                 "issuance - US $25,000,000 Floating Rate Capital Notes)",
         (0.0, None, None, None, None, None, 5.573, None, 5.573)),
        ("TOTAL", "At 31 December 1979",
         (8.0, None, None, None, None, None, 28.594, None, 36.594)),
        ("DATA", "Net movement during the year (FY1980, incl. first separately-disclosed Proposed "
                 "dividend of £0.4m)",
         (0.0, None, None, None, None, None, 4.989, None, 4.989)),
        ("TOTAL", "At 31 December 1980 (Bank company-only; UK GAAP; per the Bank's own FY1981 Annual "
                  "Report's FY1980 comparative column)",
         (8.0, None, None, None, None, None, 33.6, None, 41.6)),
        ("DATA", "Net movement during the year (FY1981)",
         (0.0, None, None, None, None, None, 1.3, None, 1.3)),
        ("TOTAL", "At 31 December 1981 (share premium undifferentiated within Retained earnings - see "
                  "HD078_1981_1990_NOTE)",
         (8.0, None, None, None, None, None, 34.9, None, 42.9)),
        ("DATA", "Net movement during the year (FY1982, incl. £3.2m ordinary share issue at par to CWS, "
                 "Jan 1983, captured within the Bank's FY1982 year-end)",
         (3.2, None, None, None, None, None, 4.1, None, 7.3)),
        ("TOTAL", "At 31 December 1982 (share premium undifferentiated within Retained earnings - see "
                  "HD078_1981_1990_NOTE)",
         (11.2, None, None, None, None, None, 39.0, None, 50.2)),
        ("DATA", "Net movement during the year (FY1983, incl. first separate disclosure of a £9.8m Share "
                 "premium balance, reclassified out of the undifferentiated Reserves/Retained earnings "
                 "figure above)",
         (0.0, 9.8, None, None, None, None, -2.5, None, 7.3)),
        ("TOTAL", "At 31 December 1983", (11.2, 9.8, None, None, None, None, 36.5, None, 57.5)),
        ("DATA", "Net movement during the year (FY1984, incl. £13.8m ordinary share issue at par to CWS, "
                 "Dec 1984/Jan 1985, captured within the Bank's FY1984 year-end, and a £13.153m reserves "
                 "transfer to the profit and loss account funding a Group deferred-tax provision required "
                 "by Finance Act 1984 changes)",
         (13.8, -0.1, None, None, None, None, -5.9, None, 7.8)),
        ("TOTAL", "At 31 December 1984", (25.0, 9.7, None, None, None, None, 30.6, None, 65.3)),
        ("DATA", "Net movement during the year (FY1985)",
         (0.0, 0.0, None, None, None, None, 4.9, None, 4.9)),
        ("TOTAL", "At 31 December 1985", (25.0, 9.7, None, None, None, None, 35.5, None, 70.2)),
        ("DATA", "Net movement during the year (FY1986)",
         (0.0, 0.0, None, None, None, None, 7.3, None, 7.3)),
        ("TOTAL", "At 31 December 1986", (25.0, 9.7, None, None, None, None, 42.8, None, 77.5)),
        ("DATA", "Net movement during the year (FY1987, incl. 14 July 1987 subdivision of 25,000,000 £1 "
                 "ordinary shares into 100,000,000 25p shares and a November 1987 issue of 20,000,000 new "
                 "25p shares at par)",
         (5.0, -0.1, None, None, None, None, 4.2, None, 9.1)),
        ("TOTAL", "At 31 December 1987", (30.0, 9.6, None, None, None, None, 47.0, None, 86.6)),
        ("DATA", "Net movement during the year (FY1988, incl. April 1988 issue of 40,000,000 8.48% "
                 "cumulative redeemable preference shares of £1 each at 100.06p, £40.0m)",
         (40.0, -0.8, None, None, None, None, 10.1, None, 49.3)),
        ("TOTAL", "At 31 December 1988 (share capital incl. £40.0m preference)",
         (70.0, 8.8, None, None, None, None, 57.1, None, 135.9)),
        ("DATA", "Net movement during the year (FY1989, incl. 23 June 1989 conversion of the existing "
                 "preference shares to 9.25% non-cumulative irredeemable and a further 31 May 1989 issue "
                 "of 20,000,000 9.25% preference shares of £1 each, £20.0m, taking total preference share "
                 "capital to £60.0m)",
         (20.0, 0.0, None, None, None, None, 2.2, None, 22.2)),
        ("TOTAL", "At 31 December 1989 (share capital incl. £60.0m preference)",
         (90.0, 8.8, None, None, None, None, 59.3, None, 158.1)),
        ("DATA", "Net movement during the year (FY1990)",
         (0.0, 0.0, None, None, None, None, -9.9, None, -9.9)),
        ("TOTAL", "At 31 December 1990 (Bank company-only; UK GAAP; share capital incl. £60.0m preference)",
         (90.0, 8.8, None, None, None, None, 49.4, None, 148.2)),
        ("TOTAL", "At 31 December 1991 (Bank company-only; UK GAAP; share capital incl. £60.0m preference)",
         (90.0, 8.8, None, None, None, None, 42.8, None, 141.6)),
        ("DATA", "Net movement during the year (FY1992)",
         (0.0, 0.0, None, None, None, None, 0.4, None, 0.5)),
        ("TOTAL", "At 31 December 1992", (90.0, 8.8, None, None, None, None, 43.2, None, 142.1)),
        ("DATA", "Net movement during the year (FY1993)",
         (0.0, 0.0, None, None, None, None, 1.3, None, 1.2)),
        ("TOTAL", "At 31 December 1993", (90.0, 8.8, None, None, None, None, 44.5, None, 143.3)),
        ("DATA", "Net movement during the year (FY1994)",
         (0.0, 0.0, None, None, None, None, 8.7, None, 8.8)),
        ("TOTAL", "At 31 December 1994", (90.0, 8.8, None, None, None, None, 53.2, None, 152.1)),
        ("DATA", "Net movement during the year (FY1995)",
         (0.0, 0.0, None, None, None, None, 14.0, None, 13.9)),
        ("TOTAL", "At 31 December 1995", (90.0, 8.8, None, None, None, None, 67.2, None, 166.0)),
        ("DATA", "Net movement during the year (FY1996)",
         (0.0, 0.0, None, None, None, None, 21.3, None, 21.3)),
        ("TOTAL", "At 31 December 1996", (90.0, 8.8, None, None, None, None, 88.5, None, 187.3)),
        ("DATA", "Net movement during the year (FY1997, incl. £5.0m ordinary share capital increase)",
         (5.0, 0.0, None, None, None, None, 30.5, None, 35.5)),
        ("TOTAL", "At 31 December 1997", (95.0, 8.8, None, None, None, None, 119.0, None, 222.8)),
        ("DATA", "Net movement during the year (FY1998)",
         (0.0, 0.0, None, None, None, None, 40.1, None, 40.1)),
        ("TOTAL", "At 31 December 1998", (95.0, 8.8, None, None, None, None, 159.1, None, 262.9)),
        ("DATA", "Net movement during the year (FY1999)",
         (0.0, 0.0, None, None, None, None, 52.1, None, 52.1)),
        ("TOTAL", "At 31 December 1999", (95.0, 8.8, None, None, None, None, 211.2, None, 315.0)),
        ("DATA", "Net movement during the year (FY2000)",
         (0.0, 0.0, None, None, None, None, 56.2, None, 56.2)),
        ("TOTAL", "At 31 December 2000", (95.0, 8.8, None, None, None, None, 267.4, None, 371.2)),
        ("DATA", "Net movement during the year (FY2001)",
         (0.0, 0.0, None, None, None, None, 67.2, None, 67.2)),
        ("TOTAL", "At 31 December 2001 (as originally reported in the Bank's FY2001 Annual Report)",
         (95.0, 8.8, None, None, None, None, 334.6, None, 438.4)),
        ("DATA", "Restatement (FY2002 Annual Report's restated FY2001 comparative closing position vs. "
                 "the Bank's own FY2001 Annual Report; cause not narrated in the source - see "
                 "HD078_1991_2002_NOTE)",
         (0.0, 0.0, None, None, None, None, 1.6, None, 1.6)),
        ("TOTAL", "At 1 January 2002 (restated)", (95.0, 8.8, None, None, None, None, 336.2, None, 440.0)),
        ("DATA", "Net movement during the year (FY2002)",
         (0.0, 0.0, None, None, None, None, 78.4, None, 78.4)),
        ("TOTAL", "At 31 December 2002", (95.0, 8.8, None, None, None, None, 414.6, None, 518.4)),
        ("DATA", "Net movement during the year (FY2003, incl. £20.0m ordinary share capital increase - "
                 "cause not disclosed in the sources reviewed for this range)",
         (20.0, 0.0, None, None, None, None, 60.6, None, 80.6)),
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

KM1_SOURCES = (
    "Sources - The Co-operative Bank p.l.c.'s own published 'UK KM1 - Key Metrics' template on the "
    "INDIVIDUAL (Bank) basis, reproduced whole in the Bank's own row order, row numbers, labels and "
    "precision. Amounts in £m, ratios exactly as printed.\n\n"
    "ENTITY TRAP - EACH EDITION PRINTS THIS TEMPLATE TWICE. The 2022, 2023 and 2024 editions carry a GROUP "
    "KM1 at section 3.2 in the front of the document AND a separate 'KM1 - KEY METRICS TEMPLATE "
    "(INDIVIDUAL)' in the appendix. This workbook is Bank Company-only throughout, so every figure below is "
    "taken from the INDIVIDUAL table and never from the Group one.\n"
    f"FY2025: Pillar 3 Disclosures December 2025, section 2.1 'Template UK KM1 - Key metrics', printed "
    f"folios 4-5 (31 December 2025 column) - {P3_2025_URL}\n"
    f"FY2024: 2024 Pillar 3 Disclosures, 'KM1 - Key Metrics (Individual)', printed folios 139-140 "
    f"(31 December 2024 column) - {P3_2024_URL}\n"
    f"FY2023: 2023 Pillar 3 Disclosures, 'KM1 - Key Metrics Template (Individual)', printed folios 140-141 "
    f"(31 December 2023 column) - {P3_2023_URL}\n"
    f"FY2022: 2022 Pillar 3 Disclosures, 'KM1 - Key Metrics Template (Individual)', printed folios 101-102 "
    f"(column a, 31 Dec 22) - {P3_2022_URL}\n"
    f"FY2021 and FY2020: FILLED FROM A LATER EDITION'S COMPARATIVE COLUMNS, and flagged here rather than "
    f"presented as own-year figures. Neither the 2020 nor the 2021 edition prints a KM1 template at all - "
    f"both pre-date the UK CRR template regime. That was tested rather than assumed: each contains zero "
    f"occurrences of 'KM1', 'combined buffer', 'total exposure measure', 'high-quality liquid' and 'net "
    f"stable funding', while the same documents return healthy counts for the control phrases 'own funds' "
    f"(12 and 10) and 'countercyclical' (10 and 10) - so both texts extract fine and the template is "
    f"genuinely absent. The 2022 edition's Individual KM1 prints five columns (31 Dec 22 / 30 Jun 22 / 31 "
    f"Dec 21 / 30 Jun 21 / 31 Dec 20), so FY2021 is its column c and FY2020 its column e - {P3_2022_URL}\n\n"
    "THE FY2025 COLUMN IS ONE YEAR NEWER THAN THE REST OF THIS WORKBOOK. The Bank's December 2025 Pillar 3 "
    "is published and supports this sheet in full; the statement sheets still end at FY2024 because they "
    "depend on the FY2025 Annual Report, which is a separate transcription. This sheet therefore carries "
    "FY2025 while the others do not - a deliberate difference, not an inconsistency.\n\n"
    "PRECISION CHANGES BETWEEN EDITIONS AND IS REPRODUCED, NOT NORMALISED. The FY2025 edition prints whole "
    "£m (CET1 968, RWA 5,112) where the FY2020-FY2024 editions print one decimal (923.5, 4,950.8). Each "
    "edition's own precision is kept.\n\n"
    "ROWS 18-20 ARE BLANK FOR FY2022, FY2021 AND FY2020 BY FORMAL EXCLUSION, not for want of data, and this "
    "is the reason they are left blank rather than back-filled. The 2022 edition's own footnote 4 states: "
    "'In line with PS22/21 \"Implementation of Basel Standards...\", disclosures for the Net Stable Funding "
    "Ratio (NSFR) are not required until after 1 January 2024.' The 2023 edition does later print an NSFR "
    "for 31 Dec 2022 in its comparative column (available stable funding 25,930.2, required stable funding "
    "18,994.5, NSFR 136.5%). Those rows are absent from an otherwise complete FY2022 table, so they stay "
    "blank here and the later figures are recorded in this note instead.\n"
    "Rows 14a-14e are likewise blank by formal exclusion in every edition. Each document's footnote 2 "
    "states the additional leverage disclosures are 'Only required for LREQ firms... The rows have been "
    "left blank as the Bank is not currently captured by either threshold'. Rows UK 8a, UK 9a, 10 and "
    "UK 10a are DASHED in the FY2024, FY2023 and FY2022 editions' Individual tables and in the FY2022 "
    "edition's 31-Dec-21 and 31-Dec-20 comparative columns, and they carry that dash here - FY2024, FY2023, "
    "FY2022, FY2021 and FY2020, twenty cells, re-read at source on 2026-09-18. They are NOT PRINTED AT ALL "
    "in the FY2025 edition, whose Table 1 runs straight from row 9 to row 11, so FY2025 is correctly BLANK "
    "on those four rows. That contrast is the whole point: a dash means the Bank printed 'this does not "
    "apply to us', a blank means the Bank printed nothing, and this sheet now shows both on the same four "
    "rows. A dash is never reproduced as a zero, and never as a blank.\n"
    "Note the FY2025 edition was read by RENDERING printed folios 4-5 at 150 dpi: its text layer extracts "
    "225,000 characters of mojibake (zero occurrences of even the word 'the'), so a text search of it would "
    "have reported the whole template as absent.\n"
    "Each edition's footnote 3 records that the LCR rows 'have been calculated as a simple average of the "
    "12 month end observations preceding the end of each half year', and the FY2025 edition adds that the "
    "NSFR 'is calculated as an average of the current and three preceding quarters'. The FY2025 edition "
    "also warns that 'the liquidity position reported in the ARAs is not a 12-month average but is reported "
    "as at 31 December 2025, therefore is not directly comparable to Pillar 3 disclosures'.\n\n"
    "LATEST-EDITION CHECK (2026-09-17): co-operativebank.co.uk's own investor-relations results page was "
    "enumerated directly. The newest FULL-YEAR Pillar 3 is the December 2025 edition used above, and it is "
    "used here, so this sheet is current. The Bank also publishes interim editions - a June 2025 half-year "
    "and a 'Bank Pillar 3 Disclosures March 2026' quarterly - which add no further year-end column. A "
    "caution for anyone repeating this check: several plausible filenames on that site "
    "('2025-pillar-3-disclosures.pdf', '2026-pillar-3-disclosures.pdf', '2026-h1-pillar-3-disclosures.pdf', "
    "'2026-annual-report-and-accounts.pdf') return HTTP 200 with an 81,445-byte HTML page rather than a PDF. "
    "They are soft-404s and are NOT evidence of a newer edition; each was checked for the %PDF magic bytes.\n"
)

km1_rows = [
    ("SECTION", "Available own funds (amounts)", {}),
    ("DATA", "1  Common Equity Tier 1 (CET1) capital (£m)", {
        "FY2025": 968, "FY2024": 923.5, "FY2023": 995.4, "FY2022": 947.3, "FY2021": 901.5, "FY2020": 874.9}),
    ("DATA", "2  Tier 1 capital (£m)", {
        "FY2025": 968, "FY2024": 923.5, "FY2023": 995.4, "FY2022": 947.3, "FY2021": 901.5, "FY2020": 874.9}),
    ("DATA", "3  Total capital (£m)", {
        "FY2025": 1169, "FY2024": 1123.9, "FY2023": 1231.8, "FY2022": 1141.5, "FY2021": 1103.7,
        "FY2020": 1084.9}),
    ("SECTION", "Risk-weighted exposure amounts", {}),
    ("DATA", "4  Total risk-weighted exposure amount (£m)", {
        "FY2025": 5112, "FY2024": 4950.8, "FY2023": 4830.6, "FY2022": 4806.7, "FY2021": 4399.8,
        "FY2020": 4668.4}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "5  Common Equity Tier 1 ratio (%)", {
        "FY2025": "18.9%", "FY2024": "18.7%", "FY2023": "20.6%", "FY2022": "19.7%", "FY2021": "20.5%",
        "FY2020": "18.7%"}),
    ("DATA", "6  Tier 1 ratio (%)", {
        "FY2025": "18.9%", "FY2024": "18.7%", "FY2023": "20.6%", "FY2022": "19.7%", "FY2021": "20.5%",
        "FY2020": "18.7%"}),
    ("DATA", "7  Total capital ratio (%)", {
        "FY2025": "22.9%", "FY2024": "22.7%", "FY2023": "25.5%", "FY2022": "23.7%", "FY2021": "25.1%",
        "FY2020": "23.2%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted "
                "exposure amount)", {}),
    ("DATA", "UK 7a  Additional CET1 SREP requirements (%)", {
        "FY2025": "2.3%", "FY2024": "2.8%", "FY2023": "2.8%", "FY2022": "2.8%", "FY2021": "3.4%",
        "FY2020": "3.2%"}),
    ("DATA", "UK 7b  Additional AT1 SREP requirements (%)", {
        "FY2025": "0.7%", "FY2024": "1.0%", "FY2023": "1.0%", "FY2022": "1.0%", "FY2021": "1.1%",
        "FY2020": "1.1%"}),
    ("DATA", "UK 7c  Additional T2 SREP requirements (%)", {
        "FY2025": "1.0%", "FY2024": "1.3%", "FY2023": "1.3%", "FY2022": "1.3%", "FY2021": "1.5%",
        "FY2020": "1.4%"}),
    ("DATA", "UK 7d  Total SREP own funds requirements (%)", {
        "FY2025": "12.0%", "FY2024": "13.1%", "FY2023": "13.1%", "FY2022": "13.1%", "FY2021": "14.0%",
        "FY2020": "13.7%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "8  Capital conservation buffer (%)", {
        "FY2025": "2.5%", "FY2024": "2.5%", "FY2023": "2.5%", "FY2022": "2.5%", "FY2021": "2.5%",
        "FY2020": "2.5%"}),
    # Dashed in the INDIVIDUAL table of every edition that prints one - read on
    # 2026-09-18 in the FY2024, FY2023 and FY2022 editions' appendix tables
    # ("KM1 - KEY METRICS TEMPLATE (INDIVIDUAL)"), never the section 3.2 GROUP
    # table. FY2021 and FY2020 come from the FY2022 INDIVIDUAL table's columns
    # c and e, the same columns every other FY2021/FY2020 cell here comes from.
    ("DATA", "UK 8a  Conservation buffer due to macro-prudential or systemic risk identified at the level "
             "of a Member State (%)",
     {"FY2024": "-", "FY2023": "-", "FY2022": "-", "FY2021": "-", "FY2020": "-"}),
    ("DATA", "9  Institution specific countercyclical capital buffer (%)", {
        "FY2025": "2.0%", "FY2024": "2.0%", "FY2023": "2.0%", "FY2022": "1.0%"}),
    ("DATA", "UK 9a  Systemic risk buffer (%)",
     {"FY2024": "-", "FY2023": "-", "FY2022": "-", "FY2021": "-", "FY2020": "-"}),
    ("DATA", "10  Global Systemically Important Institution buffer (%)",
     {"FY2024": "-", "FY2023": "-", "FY2022": "-", "FY2021": "-", "FY2020": "-"}),
    ("DATA", "UK 10a  Other Systemically Important Institution buffer",
     {"FY2024": "-", "FY2023": "-", "FY2022": "-", "FY2021": "-", "FY2020": "-"}),
    ("DATA", "11  Combined buffer requirement (%)", {
        "FY2025": "4.5%", "FY2024": "4.5%", "FY2023": "4.5%", "FY2022": "3.5%", "FY2021": "2.5%",
        "FY2020": "2.5%"}),
    ("DATA", "UK 11a  Overall capital requirements (%)", {
        "FY2025": "16.5%", "FY2024": "17.5%", "FY2023": "17.5%", "FY2022": "16.6%", "FY2021": "16.5%",
        "FY2020": "16.2%"}),
    ("DATA", "12  CET1 available after meeting the total SREP own funds requirements (%)", {
        "FY2025": "9.9%", "FY2024": "8.9%", "FY2023": "10.8%", "FY2022": "9.9%", "FY2021": "10.0%",
        "FY2020": "8.5%"}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "13  Total exposure measure excluding claims on central banks (£m)", {
        "FY2025": 22035, "FY2024": 23124.4, "FY2023": 23572.7, "FY2022": 23525.6, "FY2021": 24100.6,
        "FY2020": 22736.0}),
    ("DATA", "14  Leverage ratio excluding claims on central banks (%)", {
        "FY2025": "4.4%", "FY2024": "4.0%", "FY2023": "4.2%", "FY2022": "4.0%", "FY2021": "3.7%",
        "FY2020": "3.8%"}),
    ("SECTION", "Additional leverage ratio disclosure requirements (LREQ firms only - left blank by the "
                "Bank in every edition, see note)", {}),
    ("DATA", "14a  Fully loaded ECL accounting model leverage ratio excluding claims on central banks (%)", {}),
    ("DATA", "14b  Leverage ratio including claims on central banks (%)", {}),
    ("DATA", "14c  Average leverage ratio excluding claims on central banks (%)", {}),
    ("DATA", "14d  Average leverage ratio including claims on central banks (%)", {}),
    ("DATA", "14e  Countercyclical leverage ratio buffer (%)", {}),
    ("SECTION", "Liquidity Coverage Ratio", {}),
    ("DATA", "15  Total high-quality liquid assets (HQLA) (Weighted value - average) (£m)", {
        "FY2025": 3816, "FY2024": 4014.6, "FY2023": 4457.7, "FY2022": 5880.3, "FY2021": 4708.0,
        "FY2020": 3367.2}),
    ("DATA", "UK 16a  Cash outflows - Total weighted value (£m)", {
        "FY2025": 2292, "FY2024": 2418.8, "FY2023": 2703.5, "FY2022": 2792.3, "FY2021": 2927.1,
        "FY2020": 2998.4}),
    ("DATA", "UK 16b  Cash inflows - Total weighted value (£m)", {
        "FY2025": 154, "FY2024": 337.6, "FY2023": 636.0, "FY2022": 611.8, "FY2021": 656.1,
        "FY2020": 1210.9}),
    ("DATA", "16  Total net cash outflows (adjusted value) (£m)", {
        "FY2025": 2138, "FY2024": 2081.1, "FY2023": 2067.6, "FY2022": 2180.5, "FY2021": 2271.0,
        "FY2020": 1787.6}),
    ("DATA", "17  Liquidity coverage ratio (%)", {
        "FY2025": "179.8%", "FY2024": "193.4%", "FY2023": "215.4%", "FY2022": "270.4%", "FY2021": "207.6%",
        "FY2020": "188.2%"}),
    ("SECTION", "Net stable funding ratio", {}),
    ("DATA", "18  Total available stable funding (£m)", {
        "FY2025": 21719, "FY2024": 22318.3, "FY2023": 23816.4}),
    ("DATA", "19  Total required stable funding (£m)", {
        "FY2025": 16129, "FY2024": 16751.5, "FY2023": 18027.2}),
    ("DATA", "20  NSFR ratio (%)", {
        "FY2025": "134.7%", "FY2024": "133.3%", "FY2023": "132.1%"}),
]

bw.add_km1_sheet(
    title="The Co-operative Bank p.l.c. — KM1 Key Metrics",
    subtitle="The Bank's own published 'UK KM1 - Key Metrics' template on the INDIVIDUAL (Bank) basis - not "
             "the Group table printed alongside it - reproduced whole; £m and ratios as printed. FY2021 and "
             "FY2020 are filled from the 2022 edition's comparative columns; FY2025 is one year newer than "
             "the rest of this workbook. See note.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=76,
    source_height=480,
    years=KM1_YEARS,
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
        ("SECTION", "UK OV1 'Overview of risk weighted exposures (Individual)' — each year's own Pillar 3 Disclosures (FY2024-FY2021)", {}),
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
            "FY2024": 706.7, "FY2023": 566.3, "FY2022": 495.1, "FY2021": 491.5,
        }),
        ("DATA", "Amounts below the thresholds for deduction (for information)", {
            "FY2024": 136.1, "FY2023": 205.1, "FY2022": 236.1, "FY2021": 232.6,
        }),
        ("TOTAL", "Total", {
            "FY2024": 4950.8, "FY2023": 4830.6, "FY2022": 4806.7, "FY2021": 4399.8,
        }),
        ("SECTION", "'Pillar 1 capital requirements' table, Appendix 2 (Table 40/41/42, individual basis) — an older CRR exposure-class format (IRB approach vs Standardised approach) that predates the UK OV1 template. Only Operational risk and the Total map onto the categories above, so no other category row is shown for these years and this block does NOT foot — the remaining components are published on an exposure-class basis that cannot be mapped to the rows above without inventing a correspondence the Bank never published (FY2020-FY2017)", {}),
        ("DATA", "Operational risk", {
            "FY2020": 512.6, "FY2019": 486.5, "FY2018": 480.9, "FY2017": 550.8,
        }),
        ("TOTAL", "Total", {
            "FY2020": 4668.4, "FY2019": 4830.1, "FY2018": 5004.3, "FY2017": 4986.0,
        }),
        ("SECTION", "Total risk weighted assets only, no category breakdown published — the Bank's pre-UK-OV1-era Pillar 3 disclosures (Table 1 'CRD IV key capital ratios' and equivalents) state the RWA total and do not break it into risk categories (FY2016-FY2014)", {}),
        ("TOTAL", "Total", {
            "FY2016": 6676.1, "FY2015": 7422.9, "FY2014": 12632.2,
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
