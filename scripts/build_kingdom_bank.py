import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = [
    "FY2025", "FY2024", "FY2023", "FY2022", "FY2021",
    "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014",
    "FY2013", "FY2012", "FY2011", "FY2010", "FY2009", "FY2008", "FY2007", "FY2006", "FY2005", "FY2004",
]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

# HD-077 (2026-09-06): the statutory-statement sheets (Balance Sheet, P&L,
# Statement of Changes in Equity, Cash Flow Statement) use the full YEARS
# above, but Pillar 3 (all 11 metric sheets), Asset Quality, and RWA
# Breakdown are explicitly out of scope for that extension - they must keep
# FY2014 as their earliest column, same as before this ticket. Every call
# building one of those sheets passes years=PILLAR3_YEARS explicitly.
PILLAR3_YEARS = [y for y in YEARS if y not in ("FY2013", "FY2012", "FY2011", "FY2010", "FY2009", "FY2008", "FY2007", "FY2006", "FY2005", "FY2004")]

# All 22 years sourced from Companies House filings (fully scanned/image-only,
# 0 text blocks per page) - the bank's registered site (www.kingdombank.co.uk)
# is an unrelated expired/parked domain; the real site is www.kingdom.bank.
# Per HD-045 (2026-09-05), the FY2014-FY2020 window was added on top of the
# original FY2021-FY2025 build, capped at FY2014 by explicit project-wide
# decision. HD-077 (2026-09-06) lifted that cap for the statutory-statement
# sheets only (Balance Sheet, Profit & Loss, Statement of Changes in Equity,
# Cash Flow Statement) back to the bank's real statutory floor of FY2004 -
# Pillar 3, Asset Quality and RWA Breakdown remain capped at FY2014 by
# design (see those sheets' own notes), since Pillar 3-style disclosure
# genuinely didn't exist for this SDDT bank in the earlier years.
CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/04346834/filing-history"
FY2025_URL = f"{CH_BASE}/MzUzMjA2MDkzOWFkaXF6a2N4/document?format=pdf&download=0"
FY2024_URL = f"{CH_BASE}/MzQ3Mjc3MDk4N2FkaXF6a2N4/document?format=pdf&download=0"
FY2023_URL = f"{CH_BASE}/MzQyNzk5NjY3OGFkaXF6a2N4/document?format=pdf&download=0"
FY2022_URL = f"{CH_BASE}/MzM3Nzc1Mzk0NWFkaXF6a2N4/document?format=pdf&download=0"
FY2021_URL = f"{CH_BASE}/MzM0MzYxNTEyM2FkaXF6a2N4/document?format=pdf&download=0"
FY2020_URL = f"{CH_BASE}/MzMwMDE2MzUyN2FkaXF6a2N4/document?format=pdf&download=0"
FY2019_URL = f"{CH_BASE}/MzI2Mzg1MTA4OWFkaXF6a2N4/document?format=pdf&download=0"
FY2018_URL = f"{CH_BASE}/MzI0NDM5NDgzMGFkaXF6a2N4/document?format=pdf&download=0"
FY2017_URL = f"{CH_BASE}/MzIwMTY1OTMwOWFkaXF6a2N4/document?format=pdf&download=0"
FY2016_URL = f"{CH_BASE}/MzE3Mjc3MDQyOGFkaXF6a2N4/document?format=pdf&download=0"
FY2015_URL = f"{CH_BASE}/MzE1NzU2NjI4N2FkaXF6a2N4/document?format=pdf&download=0"
FY2014_URL = f"{CH_BASE}/MzEyMTIyNDc5OGFkaXF6a2N4/document?format=pdf&download=0"
FY2013_URL = f"{CH_BASE}/MzEwODM5MTg2OWFkaXF6a2N4/document?format=pdf&download=0"
FY2012_URL = f"{CH_BASE}/MzA3NTk1OTAyMWFkaXF6a2N4/document?format=pdf&download=0"
FY2011_URL = f"{CH_BASE}/MzA1NjkzNzEwMWFkaXF6a2N4/document?format=pdf&download=0"
FY2010_URL = f"{CH_BASE}/MzAzNjQzNTIyMWFkaXF6a2N4/document?format=pdf&download=0"
FY2009_URL = f"{CH_BASE}/MzAxMzc0NDMwNmFkaXF6a2N4/document?format=pdf&download=0"
FY2008_URL = f"{CH_BASE}/MjAzMDM3NTQ0OWFkaXF6a2N4/document?format=pdf&download=0"
FY2007_URL = f"{CH_BASE}/MjAwOTc4MTY0NmFkaXF6a2N4/document?format=pdf&download=0"
FY2006_URL = f"{CH_BASE}/MTg2OTAwNzEyYWRpcXprY3g/document?format=pdf&download=0"
FY2005_URL = f"{CH_BASE}/MTY0MjI5OTU5YWRpcXprY3g/document?format=pdf&download=0"
FY2004_URL = f"{CH_BASE}/NzIzMTc1NDBhZGlxemtjeA/document?format=pdf&download=0"

# ---------------------------------------------------------------------------
# Pillar 3 disclosure documents (link-rot repair, 2026-09-15)
#
# Kingdom Bank DID publish standalone Pillar 3 disclosure documents for
# FY2019, FY2020, FY2021, FY2022 and FY2023 - an earlier note in this script
# asserted the bank's Pillar 3 practice lapsed after a FY2015 edition, which
# is wrong and is corrected throughout below.
#
# Every one of the bank's own live Pillar 3 URLs was re-checked on 2026-09-15
# and ALL of them now return a hard HTTP 404 - the whole series has rotted off
# www.kingdom.bank. Per this project's convention the dead original is kept,
# labelled as such, and a Wayback `id_` snapshot is cited alongside it so the
# provenance chain stays readable. Each snapshot below was downloaded and
# confirmed to begin with the `%PDF-` magic bytes (a plain HTTP 200 is not
# sufficient - see the FY2022 case immediately below, which returns 200 with
# an HTML bot-check body).
# ---------------------------------------------------------------------------
P3_FY2019_DEAD_URL = (
    "https://www.kingdom.bank/wp-content/uploads/2021/03/"
    "5ee1ea4628eaae3b944cb122_Pillar-3-Disclosures-approved-14-May-2020.pdf"
)
P3_FY2019_URL = "https://web.archive.org/web/20230321070013id_/" + P3_FY2019_DEAD_URL

P3_FY2020_DEAD_URL = (
    "https://www.kingdom.bank/wp-content/uploads/2021/07/"
    "Pillar-3-Disclosures-approved-3-June-2021-v2.pdf"
)
P3_FY2020_URL = "https://web.archive.org/web/20240701022732id_/" + P3_FY2020_DEAD_URL

P3_FY2021_DEAD_URL = (
    "https://www.kingdom.bank/wp-content/uploads/2022/06/"
    "Pillar-3-Disclosures-2021-approved-9-June-2022-clean-v2.pdf"
)
P3_FY2021_URL = "https://web.archive.org/web/20240617063554id_/" + P3_FY2021_DEAD_URL

# FY2022 edition: the URL is known and the Wayback Machine holds exactly one
# capture of it (20240712045624), but that capture is NOT the PDF - it is a
# 1,489-byte HTML "One moment, please... Please wait while your request is
# being verified" bot-check interstitial served by the site's WAF, returned
# with HTTP 200. Retrieved and inspected 2026-09-15. No other capture exists.
P3_FY2022_DEAD_URL = "https://www.kingdom.bank/wp-content/uploads/2023/04/Pillar-3-Disclosures-2022.pdf"

# FY2023 edition: the FY2024 Annual Report confirms this document existed and
# was reviewed by the Board in March 2024, but it was never archived - a CDX
# listing of the whole /wp-content/uploads/2024/05/ directory (checked
# 2026-09-15) contains FSCS application forms, a mandate form and images, and
# no Pillar 3 file of any name.

AR2024_URL = "https://www.kingdom.bank/wp-content/uploads/KBL-Statutory-Accounts-2024.pdf"

# PRA consolidated waivers/modifications register (downloaded and parsed
# 2026-09-15). One Rule 3.1 row for FRN 400972 'KINGDOM BANK LIMITED':
# 'Modification by Consent - PRA Rulebook - CRR Firms - Rule 3.1 of the SDDT
# Regime - General Application Part', SDDT Regime - General Application,
# Sub Rule Number 'Ru 3.1', waiver ref A00009930P.pdf, START DATE 20/02/2025,
# no end date.
PRA_WAIVERS_URL = (
    "https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/authorisations/"
    "waivers-and-modifications-of-rules/consolidated-waivers-pra-firms.csv"
)

ENTITY_NOTE = (
    "Entity: Kingdom Bank Limited, company 04346834 (formerly Kingdom Banking Limited), FRN 400972 - "
    "confirmed via Banks List 2608.xlsx and Companies House, no identity ambiguity. A small specialist "
    "bank providing mortgages, savings and insurance broking to UK churches, Christian charities and "
    "individuals in Christian ministry; parent/ultimate controlling party is Lamb's Passage Holding "
    "Limited (LPHL) from 31 March 2020 onward (whose investor group includes Stewardship Services (UKET) "
    "Limited); for FY2014-FY2019 the ultimate parent was instead Assemblies of God Property Trust. "
    "Solo/Bank basis throughout - no group consolidation applies. All 12 years' filings on Companies "
    "House are fully scanned/image-only (0 extractable text on every page); the bank's registered-"
    "looking domain www.kingdombank.co.uk is an unrelated expired/parked domain (a GoDaddy-style parking "
    "page) - its real site is www.kingdom.bank. FY2014 was prepared under old UK GAAP/the BBA SORP (pre "
    "FRS 102) and, as a wholly-owned subsidiary whose parent's consolidated accounts are publicly "
    "available, took the FRS 1 (revised 1996) exemption from preparing a cash flow statement - FY2014 "
    "genuinely has no cash flow statement, not a sourcing gap (see Note 1(b) of the FY2014 Annual "
    "Report). FRS 102 was first adopted for FY2015, with a restated opening balance sheet at the 1 "
    "January 2014 transition date; the FY2014 figures used on every sheet here are as originally filed "
    "(old GAAP), not the FRS 102-restated comparatives shown in the FY2015 Annual Report's Statement of "
    "changes in equity (see the Statement of Changes in Equity sheet's source note for the one reconciling "
    "break this creates)."
)

# Used only by the statutory-statement sheets (Balance Sheet / P&L / Statement of Changes in Equity /
# Cash Flow Statement) extended under HD-077 - kept separate from ENTITY_NOTE above so the Pillar 3 /
# Asset Quality / RWA Breakdown sheets (out of HD-077's scope) stay byte-for-byte unchanged.
STATUTORY_ENTITY_NOTE = (
    "Entity: Kingdom Bank Limited, company 04346834 (formerly Kingdom Banking Limited), FRN 400972 - "
    "confirmed via Banks List 2608.xlsx and Companies House, no identity ambiguity. A small specialist "
    "bank providing mortgages, savings and insurance broking to UK churches, Christian charities and "
    "individuals in Christian ministry; parent/ultimate controlling party is Lamb's Passage Holding "
    "Limited (LPHL) from 31 March 2020 onward (whose investor group includes Stewardship Services (UKET) "
    "Limited); for FY2004-FY2019 the ultimate parent was instead Assemblies of God Property Trust "
    "throughout (confirmed directly in each year's own accounting policies note, back to FY2004). "
    "Solo/Bank basis throughout - no group consolidation applies. All 22 years' filings on Companies "
    "House are fully scanned/image-only (0 extractable text on every page); the bank's registered-"
    "looking domain www.kingdombank.co.uk is an unrelated expired/parked domain (a GoDaddy-style parking "
    "page) - its real site is www.kingdom.bank. FY2004-FY2014 were prepared under old UK GAAP/the BBA "
    "SORP (pre FRS 102) and, as a wholly-owned subsidiary whose parent's consolidated accounts are "
    "publicly available, took the FRS 1 (revised 1996) exemption from preparing a cash flow statement in "
    "every one of those years (confirmed directly in each year's own accounting policies note, not "
    "assumed) - none of FY2004-FY2014 has a cash flow statement, and none of this is a sourcing gap "
    "(see Note 1(b) of the FY2014 Annual Report, and Note 1(a) of the FY2004 Annual Report for the "
    "same exemption stated in the bank's very first trading period). FY2004 additionally has no profit "
    "and loss account, statement of total recognised gains and losses, or cash flow statement at all: "
    "the FY2004 Annual Report is an 11-month period (1 February-31 December 2004, following a dormant "
    "shell period back to incorporation - see the two 'Accounts for a dormant company' filings that "
    "precede it on Companies House) and states explicitly, in its own Note 1(d): 'No profit and loss "
    "account has been prepared for the period ended 31 December 2004, as Kingdom Bank Limited did not "
    "commence trading until 1 January 2005.' Only a Balance Sheet exists for FY2004, and it is shown "
    "here on that basis - not a sourcing gap. FRS 102 was first adopted for FY2015, with a restated "
    "opening balance sheet at the 1 "
    "January 2014 transition date; the FY2014 figures used on every sheet here are as originally filed "
    "(old GAAP), not the FRS 102-restated comparatives shown in the FY2015 Annual Report's Statement of "
    "changes in equity (see the Statement of Changes in Equity sheet's source note for the one reconciling "
    "break this creates)."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Kingdom Bank Limited's own Statement of cash flows, £'000, Bank/solo basis "
    "(Companies House filings, all fully scanned):\n"
    f"FY2025 (own) & FY2024 (comparative, cross-checked against FY2024's own report): Annual Report & "
    "Accounts 2025, p.38 (Statement of cash flows) - " + FY2025_URL + "\n"
    f"FY2024 (own): Annual Report & Accounts 2024 - " + FY2024_URL + "\n"
    f"FY2023 (own) & FY2022 (comparative): Annual Report & Accounts 2023, p.39 (Statement of cash flows) - " + FY2023_URL + "\n"
    f"FY2022 (own): Annual Report & Accounts 2022 - " + FY2022_URL + "\n"
    f"FY2021 (own) & FY2020 (comparative, cross-checked against FY2020's own report): Annual Report & "
    "Accounts 2021, p.33 (Statement of cash flows) - " + FY2021_URL + "\n"
    f"FY2020 (own) & FY2019 (comparative): Annual Report & Accounts 2020, p.31 (Statement of cash flows) - " + FY2020_URL + "\n"
    f"FY2019 (own): Annual Report & Accounts 2019, p.26 - " + FY2019_URL + "\n"
    f"FY2018 (own) & FY2017 (comparative): Annual Report & Accounts 2018, p.23 (Statement of cash flows) - " + FY2018_URL + "\n"
    f"FY2017 (own): Annual Report & Accounts 2017 - " + FY2017_URL + "\n"
    f"FY2016 (own) & FY2015 (comparative): Annual Report & Accounts 2016, p.16 (Statement of cash flows) - " + FY2016_URL + "\n"
    f"FY2015 (own): Annual Report & Accounts 2015, p.16 - " + FY2015_URL + "\n"
    "FY2004-FY2014: no cash flow statement was prepared in any of these 11 years - the Bank took the "
    "FRS 1 (revised 1996) 'Cash flow statements' exemption available to a wholly-owned subsidiary whose "
    "parent (Assemblies of God Property Trust) publishes consolidated accounts, re-confirmed directly in "
    "each year's own Note 1 accounting policies back to the FY2004 Annual Report's Note 1(a) (the bank's "
    "very first trading period) - " + FY2014_URL + " (FY2014); " + FY2013_URL + " (FY2013); " + FY2012_URL
    + " (FY2012); " + FY2011_URL + " (FY2011); " + FY2010_URL + " (FY2010); " + FY2009_URL + " (FY2009); "
    + FY2008_URL + " (FY2008); " + FY2007_URL + " (FY2007); " + FY2006_URL + " (FY2006); " + FY2005_URL
    + " (FY2005); " + FY2004_URL + " (FY2004)\n"
    + STATUTORY_ENTITY_NOTE + "\n"
    "Every year-end closing balance ties exactly to the following year's opening balance across all 11 "
    "years for which a cash flow statement exists (FY2015 closing £13,263k = FY2016 opening; FY2016 "
    "closing £13,457k = FY2017 opening; FY2017 closing £14,528k = FY2018 opening; FY2018 closing £10,189k "
    "= FY2019 opening; FY2019 closing £12,010k = FY2020 opening; FY2020 closing £19,561k = FY2021 opening; "
    "FY2021 closing £20,030k = FY2022 opening; FY2022 closing £24,861k = FY2023 opening; FY2023 closing "
    "£35,058k = FY2024 opening; FY2024 closing £39,791k = FY2025 opening) - no restatements found. "
    "FY2004-FY2014 (11 years) genuinely have no cash flow statement at all - not a sourcing gap."
)

STATEMENTS_SOURCES = (
    "Sources - Kingdom Bank Limited's own Statement of financial position / Income statement / Statement of "
    "changes in equity, £'000, Bank/solo basis (Companies House filings, all fully scanned/image-only):\n"
    f"FY2025 & FY2024: Annual Report & Accounts 2025, p.35 (Income statement), p.36 (Statement of financial "
    "position), p.37 (Statement of changes in equity) - " + FY2025_URL + "\n"
    f"FY2024 (own): Annual Report & Accounts 2024 - " + FY2024_URL + "\n"
    f"FY2023 & FY2022: Annual Report & Accounts 2023, p.36 (Income statement), p.37 (Statement of financial "
    "position), p.38 (Statement of changes in equity) - " + FY2023_URL + "\n"
    f"FY2022 (own): Annual Report & Accounts 2022, p.40 (Income statement), p.42 (Statement of financial "
    "position) - " + FY2022_URL + "\n"
    f"FY2021 & FY2020: Annual Report & Accounts 2021, p.27 (P&L), p.29 (Balance sheet), p.30 (Statement of "
    "changes in equity) - " + FY2021_URL + "\n"
    f"FY2020 & FY2019: Annual Report & Accounts 2020, p.27 (P&L), p.29 (Balance sheet), p.30 (Statement of "
    "changes in equity) - " + FY2020_URL + "\n"
    f"FY2019 (own): Annual Report & Accounts 2019, p.22 (P&L), p.24 (Balance sheet), p.25 (SOCE) - " + FY2019_URL + "\n"
    f"FY2018 & FY2017: Annual Report & Accounts 2018, p.19 (P&L), p.21 (Balance sheet), p.22 (Statement of "
    "changes in equity) - " + FY2018_URL + "\n"
    f"FY2017 (own): Annual Report & Accounts 2017 - " + FY2017_URL + "\n"
    f"FY2016 & FY2015: Annual Report & Accounts 2016, p.12 (P&L), p.14 (Balance sheet), p.15 (Statement of "
    "changes in equity) - " + FY2016_URL + "\n"
    f"FY2015 (own, incl. FRS 102 first-time-adoption SOCE at p.15): Annual Report & Accounts 2015 - " + FY2015_URL + "\n"
    f"FY2014 (own, old UK GAAP/BBA SORP - profit and loss account p.10, Statement of total recognised "
    "gains and losses p.11, balance sheet p.12; no SOCE or cash flow statement prepared that year - see "
    "the Statement of Changes in Equity and Cash Flow Statement sheets): Annual Report & Accounts 2014 - "
    + FY2014_URL + "\n"
    f"FY2013 & FY2012: Annual Report & Accounts 2013, p.10 (P&L), p.11 (STRGL), p.12 (Balance sheet), "
    "p.25 (reserves reconciliation notes) - " + FY2013_URL + "\n"
    f"FY2012 (own) & FY2011 (comparative): Annual Report & Accounts 2012, p.9 (P&L), p.10 (STRGL), "
    "p.11 (Balance sheet), p.24 (reserves reconciliation notes) - " + FY2012_URL + "\n"
    f"FY2011 (own) & FY2010 (comparative): Annual Report & Accounts 2011, p.8 (P&L), p.9 (STRGL), "
    "p.10 (Balance sheet), p.22-23 (reserves reconciliation notes) - " + FY2011_URL + "\n"
    f"FY2010 (own) & FY2009 restated (comparative - see PRESENTATION NOTE (9) below): Annual Report & "
    "Accounts 2010, p.9 (P&L), p.10 (STRGL), p.11 (Balance sheet), p.22 (reserves reconciliation notes), "
    "p.14 (Note 1(n), restatement of 2009 comparatives) - " + FY2010_URL + "\n"
    f"FY2009 (own, as originally filed - used here in preference to FY2010's restated comparative, per "
    "this workbook's standing convention of showing each year's own figures as filed): Annual Report & "
    "Accounts 2009, p.8 (P&L), p.9 (STRGL), p.10 (Balance sheet), p.20 (reserves reconciliation notes) - "
    + FY2009_URL + "\n"
    f"FY2008 & FY2007: Annual Report & Accounts 2008, p.8 (P&L), p.9 (STRGL), p.10 (Balance sheet), "
    "p.19 (reserves reconciliation notes) - " + FY2008_URL + "\n"
    f"FY2007 (own) & FY2006 (comparative): Annual Report & Accounts 2007, p.7 (P&L, no STRGL that year), "
    "p.8 (Balance sheet), p.16 (reserves reconciliation notes) - " + FY2007_URL + "\n"
    f"FY2006 (own) & FY2005 (comparative): Annual Report & Accounts 2006, p.7 (P&L, no STRGL), "
    "p.8 (Balance sheet) - " + FY2006_URL + "\n"
    f"FY2005 (own, prepared in whole £, converted to £'000 here) & FY2004 (comparative): Annual Report & "
    "Accounts 2005, p.7 (P&L and STRGL), p.8 (Balance sheet) - " + FY2005_URL + "\n"
    f"FY2004 (own, Balance Sheet only - see PRESENTATION NOTE (10) below): Report and Financial Statements "
    "for the period ended 31 December 2004, p.6 (Balance sheet), p.7 (Note 1, accounting policies) - "
    + FY2004_URL + "\n"
    + STATUTORY_ENTITY_NOTE + "\n"
    "PRESENTATION NOTES: (1) FY2021-FY2022 do not disclose separate 'Prepayments and accrued income' or "
    "'Accruals and deferred income' lines - FY2021/FY2022's own 'Other assets' and 'Other liabilities' totals "
    "bundle what FY2023 onward splits into two lines each; each year's own labelling is followed as published, "
    "not forced into a common template. (2) FY2021's income statement includes a one-off 'Profit on sale of "
    "investment property' line (£634k) and used the subtotal label 'Operating income' rather than 'Total net "
    "income' (introduced from FY2023) - same calculation, different label. (3) FY2021's own equity statement "
    "carried a £172k Revaluation reserve (from a historical operating-property revaluation) that was "
    "transferred to the Profit and loss account and fully extinguished during FY2021 upon reclassification of "
    "that property - a genuine one-off equity movement, not a plug. (4) FY2021's loan-book note used the label "
    "'Charity mortgages' where FY2022 onward uses 'Organisational mortgages' for the same category, and "
    "FY2021/FY2020 additionally had a small 'Fully secured lending to other group companies' sub-category "
    "(nil in FY2021, £269k in FY2020) not present from FY2022 onward. (5) FY2014-FY2018 additionally "
    "disclosed small 'Charity loans'/'Personal loans' unsecured sub-categories (a few £'000 each) that "
    "disappear from FY2019 onward - each year's own labelling is followed, not forced into a common "
    "template. (6) FY2014's balance sheet used its own old-GAAP line structure: 'Loans and advances to "
    "credit institutions' (economically the same line as later years' 'Loans and advances to banks'), no "
    "separately disclosed Investment property (bundled into Tangible fixed assets, which also included "
    "freehold investment property that year), and a single combined 'Prepayments, accrued income and "
    "other assets' line rather than the later three-way split into Other assets / Prepayments and accrued "
    "income / Deferred tax assets - see the dedicated 'Prepayments, accrued income and other assets "
    "(FY2014 combined line)' row below. (7) FY2014-FY2016 carried a materially larger Revaluation reserve "
    "(£578k/£164k/£166k) than FY2017-FY2020 (a flat £172k) from historical property revaluations that were "
    "gradually run down; this reserve is shown as its own Balance Sheet equity line for FY2014-FY2020 and "
    "is blank (not zero) for FY2021-FY2025 once fully extinguished (see the Statement of Changes in "
    "Equity sheet). (8) FRS 102 was first adopted for FY2015, with a restated 1 January 2014 opening "
    "balance sheet shown only in the FY2015 Annual Report's Statement of changes in equity; the FY2014 "
    "column on every sheet here uses the figures as originally filed under old UK GAAP/the BBA SORP (per "
    "the FY2014 Annual Report itself), not the FRS 102-restated comparatives - this creates a one-off, "
    "disclosed reconciling difference between the FY2014 closing position shown here (£4,960k total "
    "shareholders' funds) and the FY2015 Annual Report's restated opening position for 1 January 2015 "
    "(£4,847k), driven mainly by a £77k lower Revaluation reserve and a £365k higher Profit and loss "
    "account balance under the restated basis - not an error. (9) The FY2010 Annual Report's Note 1(n) "
    "discloses a change of accounting policy adopted during FY2010, to recognise commission earned by the "
    "Bank's authorised representative SALT Insurance Services Ltd gross rather than net - the 2009 "
    "comparatives shown in the FY2010 Annual Report were restated for this (fees receivable grossed up "
    "£131k, a matching fees payable line added, and a £65k other-debtor/other-creditor gross-up on the "
    "Balance Sheet), but the Report states explicitly 'There is no impact on the reported losses', and the "
    "restatement nets to zero on every equity total (FY2009's own closing shareholders' funds of £4,788k "
    "is identical either way). This workbook therefore shows FY2009 exactly as filed in the FY2009 Annual "
    "Report itself (net presentation, £265k combined fees receivable, no separate fees payable line, "
    "£75k Prepayments/other assets) rather than the FY2010 Annual Report's restated comparative (£396k/"
    "£131k gross, £140k Prepayments/other assets) - consistent with this workbook's standing principle of "
    "using each year's own figures as originally filed, per PRESENTATION NOTE (8) above for the equivalent "
    "FY2014/FY2015 FRS 102 transition. (10) FY2004 is the bank's first trading period (1 February-31 "
    "December 2004, an 11-month period, not a full year - see the FY2004 Annual Report's own Note 1(a)) "
    "and its Note 1(d) states explicitly that no profit and loss account was prepared for it, since the "
    "Bank did not commence trading until 1 January 2005 - so the Profit & Loss, Statement of Changes in "
    "Equity (movement rows) and Cash Flow Statement sheets are all blank for FY2004, a genuine and "
    "explicitly documented absence, not a sourcing gap; only the Balance Sheet exists for that year. "
    "FY2004's own Balance Sheet additionally used a more granular structure than every later year - a "
    "separate 'Cash' line (£76, immaterial) and separate 'Loans and advances to banks'/'Loans and advances "
    "to building societies' lines - which the FY2005 Annual Report's own FY2004 comparative column already "
    "collapses into the single 'Loans and advances to credit institutions' and 'Prepayments, accrued "
    "income and other assets' lines used here (cross-checked exactly: £7,424,652 + £2,320,638 + £113,101 = "
    "£9,858,391 loans; £76 + £10,364 = £10,440 prepayments/other assets), consistent with this workbook's "
    "practice elsewhere of following each year's own line structure but not inventing new rows for a "
    "single immaterial one-off split. FY2004's Called up share capital of £4,217k combines both the £4,208k "
    "called-up and £9k unpaid share capital shown as separate lines that year only - both were fully paid "
    "by FY2005, when a single 'Called up share capital' line resumes. No 'Cash and balances at central "
    "banks' line existed at all before FY2010 (it was bundled within 'Loans and advances to banks' "
    "throughout FY2004-FY2009 - confirmed absent, not merely blank, in each of those years' own Balance "
    "Sheets); no Revaluation reserve existed before FY2007 (the Bank's freehold properties were first "
    "professionally revalued that year); a 'Loans and advances from credit institutions due within 3 "
    "months' liability line existed only FY2006-FY2009 (nil from FY2010 onward) - see the dedicated row "
    "below. (11) The 'Debt securities' line's only note-level breakdown across all years reviewed is the "
    "FY2009 Annual Report's Note 10 (p.17), which shows the full £1,692k FY2009 balance as a single "
    "'Available-for-sale' bucket in its financial-instruments valuation-hierarchy table, valued as Level 1 "
    "(\"unadjusted quoted prices in active markets\"), with the accompanying text stating this Level 1 "
    "category \"includes UK government bonds and gilts\" - the only issuer-type detail disclosed in any "
    "year. No later year's Debt securities note (e.g. FY2012 Note 10, p.20, or FY2013's equivalent) "
    "discloses any measurement-basis or issuer-type split at all - each shows only a single repayment-"
    "maturity line, with no comparison basis for a genuine sub-row split. Given this, and that every "
    "year's balance is immaterial (£25k or less in FY2011-FY2013, nil FY2010/FY2014, versus total assets "
    "of ~£48-52m each of those years), the row above is labelled in place using the one instance of "
    "disclosed detail (FY2009) rather than split into sub-rows."
)

ASSET_QUALITY_SOURCES = (
    "Sources - Kingdom Bank Limited's own Note 12/9 'Loans and advances to customers' (Advances to customers by "
    "product, part a; Loan loss provision movement, part c), £'000, Bank/solo basis (Companies House filings, "
    "all fully scanned/image-only):\n"
    f"FY2025 & FY2024: Annual Report & Accounts 2025, p.51-52 - " + FY2025_URL + "\n"
    f"FY2024 (own): Annual Report & Accounts 2024 - " + FY2024_URL + "\n"
    f"FY2023 & FY2022: Annual Report & Accounts 2023, p.53-54 - " + FY2023_URL + "\n"
    f"FY2022 (own): Annual Report & Accounts 2022 - " + FY2022_URL + "\n"
    f"FY2021 & FY2020: Annual Report & Accounts 2021, p.45-46 (Note 12) - " + FY2021_URL + "\n"
    f"FY2020 & FY2019: Annual Report & Accounts 2020, p.45-46 (Note 12) - " + FY2020_URL + "\n"
    f"FY2019 (own): Annual Report & Accounts 2019, p.36-37 (Note 12) - " + FY2019_URL + "\n"
    f"FY2018 & FY2017: Annual Report & Accounts 2018, p.37-38 (Note 12) - " + FY2018_URL + "\n"
    f"FY2017 (own): Annual Report & Accounts 2017 - " + FY2017_URL + "\n"
    f"FY2016 & FY2015: Annual Report & Accounts 2016, p.29-31 (Note 12) - " + FY2016_URL + "\n"
    f"FY2015 (own): Annual Report & Accounts 2015 - " + FY2015_URL + "\n"
    f"FY2014 (own, Note 9 'Loans and advances to customers', old UK GAAP/BBA SORP): Annual Report & "
    "Accounts 2014, p.20-21 - " + FY2014_URL + "\n"
    + ENTITY_NOTE + "\n"
    "No IFRS 9 stage (1/2/3) split is disclosed in any year - this entity applies FRS 102 (FRS 102/old UK "
    "GAAP for FY2014), not IFRS 9, and reports a single collective/IBNR loan loss provision instead; the "
    "'Of which collective/IBNR provision' split shown here (where disclosed) is the closest equivalent "
    "breakdown and is only disclosed from FY2022 onward - left blank for FY2014-FY2021, not assumed zero. "
    "FY2014's own Note 9 used a materially different, more granular structure than every later year: its "
    "loan loss provision was split into a 'General provision' (IBNR-based, split further between "
    "incorporated and unincorporated borrowers) and a 'Specific provision', plus a wholly separate "
    "'Provision for suspended interest' deducted from gross advances alongside the main provision - see "
    "the dedicated FY2014 rows below for this one-off structure, which is not comparable line-for-line "
    "with FY2015 onward's single combined provision."
)


def p3_sources():
    return (
        "Sources - Kingdom Bank Limited, Bank/solo basis, £'000 unless stated as a %. TWO DISTINCT SOURCE "
        "SETS, listed in turn below and kept on separate labelled rows on every sheet: (1) each year's own "
        "audited Statement of financial position and Strategic Report 'Key performance indicators' table, "
        "and (2) the bank's own annual Pillar 3 disclosure documents, recovered 2026-09-15.\n"
        "(1) ANNUAL REPORTS (Companies House filings, all fully scanned):\n"
        f"FY2025 & FY2024: Annual Report & Accounts 2025, p.10 (Capital), p.15 (KPI table), p.36 (Statement "
        "of financial position) - " + FY2025_URL + "\n"
        f"FY2023 & FY2022: Annual Report & Accounts 2023, p.10 (Capital), p.15 (KPI table), p.37 (Statement "
        "of financial position) - " + FY2023_URL + "\n"
        f"FY2021 & FY2020: Annual Report & Accounts 2021, p.5 (Capital), p.8 (KPI table), p.31 (Statement of "
        "financial position) - " + FY2021_URL + "\n"
        f"FY2020 & FY2019: Annual Report & Accounts 2020, p.3 (Capital), p.7 (KPI table) - " + FY2020_URL + "\n"
        f"FY2019 (own) & FY2018 (comparative): Annual Report & Accounts 2019, p.3 (Capital), p.6 (KPI "
        "table) - " + FY2019_URL + "\n"
        f"FY2018 (own) & FY2017 (comparative): Annual Report & Accounts 2018, p.3-4 (Capital and KPI table) "
        "- " + FY2018_URL + "\n"
        f"FY2016 (own) & FY2015 (comparative): Annual Report & Accounts 2016, p.3-4 (Capital and KPI table) "
        "- " + FY2016_URL + "\n"
        f"FY2014: Annual Report & Accounts 2014, p.2 (Capital, narrative only - no KPI table) - " + FY2014_URL + "\n"
        "(1b) ANNUAL REPORT NOTE 29(j) 'CAPITAL MANAGEMENT' - added 2026-09-18 (GA-006), and the source "
        "for the Total RWAs and Total Capital Ratio sheets' FY2022-FY2025 rows. This is a different part "
        "of the same documents from the KPI table cited in (1) above: it sits in the notes to the "
        "financial statements, not the Strategic Report, and prints a shareholders'-funds-to-regulatory-"
        "capital reconciliation ending in 'Total Risk Exposure amount (unaudited)' plus a capital-ratio "
        "block. Each year is cited to its OWN edition, at the printed folio:\n"
        f"FY2025 (own) & FY2024 (comparative): Annual Report & Accounts 2025, note 29(j), printed p.73 - "
        + FY2025_URL + " (also live on the bank's own site as "
        "https://www.kingdom.bank/wp-content/uploads/KBL-Statutory-Accounts-2025.pdf, verified 2026-09-18: "
        "HTTP 200, Content-Type application/pdf, %PDF-1.7 magic bytes)\n"
        f"FY2024 (own) & FY2023 (comparative): Annual Report & Accounts 2024, note 29(j), printed p.75 - "
        + FY2024_URL + " (also live at "
        "https://www.kingdom.bank/wp-content/uploads/KBL-Statutory-Accounts-2024.pdf, same verification)\n"
        f"FY2023 (own) & FY2022 (comparative): Annual Report & Accounts 2023, note 29(j), printed p.76 - "
        + FY2023_URL + "\n"
        f"FY2022 (own) & FY2021 (comparative): Annual Report & Accounts 2022, note 29(j), printed p.82 - "
        + FY2022_URL + "\n"
        "EXTRACTION NOTE: the FY2024 and FY2025 editions are text-native (the bank's own site hosts both, "
        "and pdftotext reads them directly), which corrects the blanket 'all fully scanned' description in "
        "(1) above - that remains true of the FY2023 and earlier Companies House filings. The FY2023 and "
        "FY2022 figures were therefore read from rendered page images (pdftoppm at 300dpi and 450dpi, two "
        "independent renderings agreeing digit-for-digit) and then confirmed a second time against the "
        "following year's comparative column, which is text-native for FY2023.\n"
        + "(2) STANDALONE PILLAR 3 DISCLOSURE DOCUMENTS (recovered 2026-09-15 - this CORRECTS an earlier claim "
        "in this workbook that no such document exists for any reported year). Kingdom Bank published an "
        "annual Pillar 3 disclosure document for FY2019, FY2020, FY2021, FY2022 and FY2023. Three of the "
        "five have been retrieved and read in full, and are the source for the regulatory-basis rows on the "
        "capital, RWA, leverage, liquidity and RWA Breakdown sheets:\n"
        "FY2021 (own) & FY2020 (comparative): Pillar 3 Disclosures 2021, revision date May 2022, approved "
        "9 June 2022, p.14 (Template UK KM1 - Key metrics template, capital/RWA/leverage rows), p.15 (UK "
        "KM1 liquidity rows - LCR and NSFR), p.17 (Template UK OV1 - Overview of risk weighted exposure "
        "amounts, plus the credit-risk-by-exposure-class table), p.18 (section 5.2 Leverage Ratio) - "
        + P3_FY2021_URL + " (Wayback id_ snapshot of 17 June 2024; the bank's own URL, "
        + P3_FY2021_DEAD_URL + ", returned HTTP 404 when re-checked on 2026-09-15)\n"
        "FY2020 (own) & FY2019 (comparative leverage ratio only): Pillar 3 Disclosures [2020], revision "
        "date May 2021, approved 3 June 2021, p.15 (section 4 Own funds table), p.16 (section 5.1 risk "
        "weighted exposure amounts by CRR Article 112 exposure category), p.17 (section 5.2 Leverage "
        "Ratio) - " + P3_FY2020_URL + " (Wayback id_ snapshot of 1 July 2024; the bank's own URL, "
        + P3_FY2020_DEAD_URL + ", returned HTTP 404 when re-checked on 2026-09-15)\n"
        "FY2019 (own) & FY2018 (comparative leverage ratio only): Pillar 3 Disclosures [2019], revision "
        "date May 2020, approved 14 May 2020, p.13 (section 4 Own funds table), p.14 (section 5.1 risk "
        "weighted exposure amounts), p.15 (section 5.2 Leverage Ratio) - " + P3_FY2019_URL + " (Wayback "
        "id_ snapshot of 21 March 2023; the bank's own URL, " + P3_FY2019_DEAD_URL + ", returned HTTP 404 "
        "when re-checked on 2026-09-15)\n"
        "FY2022 edition - EXISTS BUT IS NOT RETRIEVABLE. Its URL is known ("
        + P3_FY2022_DEAD_URL + ") and returns HTTP 404 live. The Wayback Machine holds exactly one capture "
        "of it (timestamp 20240712045624), and that capture is not the PDF: it is a 1,489-byte HTML "
        "bot-check interstitial ('One moment, please... Please wait while your request is being verified') "
        "served by the site's WAF with an HTTP 200 status. Downloaded and inspected 2026-09-15; no other "
        "capture exists in the CDX index. FY2022 regulatory figures are therefore blank on the metric "
        "sheets, not zero, and are a genuine retrieval failure rather than a non-disclosure.\n"
        "FY2023 edition - EXISTS BUT WAS NEVER ARCHIVED. The FY2024 Annual Report states directly that "
        "'The annual Pillar 3 disclosure document was reviewed by the Board in March 2024 and contained "
        "the enhanced remuneration disclosures required by CRD V' (p.27, Board Remuneration Committee "
        "report) - " + AR2024_URL + ". A CDX listing of the entire /wp-content/uploads/2024/05/ directory "
        "on kingdom.bank (checked 2026-09-15) returns FSCS application forms, a non-personal mandate form "
        "and site images, and no Pillar 3 file of any name. FY2023 regulatory figures are likewise blank, "
        "not zero.\n"
        "ANNUAL REPORT KPI TABLE (a separate, non-Pillar 3 series - see the individual sheets, which keep "
        "the two on separate labelled rows and never merge them). Each Annual Report from FY2015 onward "
        "discloses a Core Equity Tier 1 ('CET1') ratio, a Leverage ratio and a Liquidity Coverage "
        "Requirement ('LCR') ratio among the 'Key performance indicators' in the Strategic Report - "
        "re-verified directly against seven of this bank's own primary-source PDFs during HD-045 "
        "(2026-09-05), which also confirmed the KPI table did not yet exist in FY2014 (narrative-only "
        "Capital paragraph that year). The KPI table is the ONLY source for FY2014-FY2018 and FY2022-"
        "FY2025; where a Pillar 3 document also covers the year, both series are shown side by side "
        "because they do not agree (see the CET1 Ratio, Leverage Ratio and LCR sheets).\n"
        "No MREL ratio is disclosed in any year, in any document - see that sheet's own note."
    )


ARCHIVE_PROVENANCE_NOTE = (
    "WHY THE PILLAR 3 ROWS CITE THE WAYBACK MACHINE (link-rot repair, 2026-09-15). Every one of Kingdom "
    "Bank's own Pillar 3 disclosure URLs was re-checked on 2026-09-15 and ALL of them now return a hard "
    "HTTP 404 - the whole series has rotted off www.kingdom.bank. Rather than drop the citations (which "
    "would make the figures unverifiable) this workbook cites a Wayback `id_` snapshot of each document "
    "and keeps the bank's own URL alongside it, labelled as the dead original, so the provenance chain "
    "stays readable. Each snapshot was downloaded and confirmed to begin with the `%PDF-` magic bytes, "
    "not merely to return HTTP 200 - which matters here, because the FY2022 document's one and only "
    "Wayback capture DOES return HTTP 200 and is an HTML bot-check page rather than the PDF. See the "
    "source citation below for each document's snapshot timestamp and its dead original URL."
)

EARLY_EDITIONS_NOTE = (
    "FY2014-FY2018 ARE A SEPARATE, OLDER GAP and are not covered by the recovered FY2019-FY2021 "
    "documents. An unfiltered Wayback CDX sweep of kingdom.bank surfaced a dedicated disclosure page at "
    "www.kingdom.bank/about-us/pillar-3-disclosure/, in the About Us > Financial Information menu. Its "
    "only surviving capture (2 February 2017, HTTP 200) links exactly three documents - 'Pillar 3 "
    "Disclosure 2013', 'Pillar 3 Disclosure 2014' and 'Pillar 3 Disclosure 2015' - by opaque content hash "
    "rather than filename: /docs/bb5e9fae40063b28744f4d2d7d8908c1/ (2013), "
    "/docs/d32034542cc36318b9bfa22706e15c90/ (2014) and /docs/997ae5938fc21ec9f20b8bc721e6c6f8/ (2015). "
    "All three return HTTP 404 live, and a CDX prefix sweep of kingdom.bank/docs* returns zero captures - "
    "the Wayback Machine archived the page listing them but never the files themselves. The FY2014 and "
    "FY2015 editions would have supplied the figures still blank for those years; they are not withheld "
    "or unlocated, they no longer exist in any public copy reachable online. No Pillar 3 document of any "
    "kind has been located for FY2016, FY2017 or FY2018."
)

NOT_DISCLOSED_NOTE = (
    "Not publicly disclosed. Kingdom Bank has never disclosed this metric in any year reviewed - not in "
    "any of the five annual Pillar 3 disclosure documents it published (FY2019-FY2023), and not in any "
    "Annual Report's Strategic Report 'Key performance indicators' table.\n\n"
    "CORRECTION LOGGED 2026-09-15. An earlier version of this note asserted that Kingdom Bank's Pillar 3 "
    "practice 'lapsed after the FY2015 edition' and that no standalone Pillar 3 document existed for any "
    "reported year. That was WRONG and has been withdrawn. The bank published Pillar 3 disclosures for "
    "FY2019, FY2020, FY2021, FY2022 and FY2023; the FY2019, FY2020 and FY2021 editions have now been "
    "retrieved from the Wayback Machine and read in full, and they are the source of the regulatory-basis "
    "capital, RWA, leverage and liquidity figures now carried on those sheets. The earlier search missed "
    "them because it enumerated the live WordPress media library and a 2017 capture of the bank's "
    "/about-us/pillar-3-disclosure/ index page; the FY2019-FY2023 documents were published later, under "
    "/wp-content/uploads/, and every one of those URLs has since 404'd - so the live-site enumeration "
    "returned a true but misleading 'nothing there now'. A CDX sweep filtered on 'pillar' is what "
    "surfaced them.\n"
    + ARCHIVE_PROVENANCE_NOTE + "\n\n"
    "SDDT STATUS - EXACT, AND IT ONLY REACHES THE FINAL YEAR. The Bank of England consolidated list of "
    "waivers and modifications granted to PRA-authorised firms (" + PRA_WAIVERS_URL + ", downloaded and "
    "parsed 2026-09-15) carries one Rule 3.1 row for FRN 400972, 'KINGDOM BANK LIMITED': 'Modification by "
    "Consent - PRA Rulebook - CRR Firms - Rule 3.1 of the SDDT Regime - General Application Part', rule "
    "handbook 'SDDT Regime - General Application', sub rule number 'Ru 3.1', waiver ref A00009930P.pdf, "
    "START DATE 20/02/2025, no end date. Only Rule 3.1 removes the Pillar 3 disclosure obligation "
    "outright (Article 433b merely reduces it, and Ru 2.1(9) is an eligibility criterion with no "
    "disclosure effect). The bank states its own intent to the same effect: its FY2024 Annual Report says "
    "'The Bank has submitted a modification by consent to join the SDDT regime' (p.13, Strategic Report, "
    "Future capital requirements) and, in the Board Remuneration Committee report at p.27, 'The annual "
    "Pillar 3 disclosure document was reviewed by the Board in March 2024 and contained the enhanced "
    "remuneration disclosures required by CRD V. Due to the SDDT regime the Pillar 3 disclosure document "
    "will not be required in future years.' - " + AR2024_URL + "\n"
    "DATE-FIT CHECK. Kingdom Bank's accounting reference date is 31 December. Measured against each "
    "affected year's own year-end, only FY2025 (year-end 31 December 2025) falls after the 20/02/2025 "
    "start date, so FY2025 alone is structurally exempt. FY2024 (year-end 31 December 2024) and every "
    "earlier year PREDATE the modification and are NOT explained by it - do not read the SDDT regime back "
    "onto them. No FY2024 Pillar 3 document has been located either, which is consistent with the bank's "
    "stated intent (the FY2024 disclosure would have fallen due in 2025, after the modification took "
    "effect), but that is an observation about the document, not a year-end date fit, and FY2024 is "
    "therefore recorded here as an ordinary non-disclosure rather than as structurally exempt.\n\n"
    + EARLY_EDITIONS_NOTE
)

# Used by the four sheets that the recovered Pillar 3 documents DO populate for
# FY2020/FY2021 but that remain blank in every other year.
PARTIAL_DISCLOSURE_NOTE = (
    "Disclosed for FY2021 and FY2020 only, from the recovered Pillar 3 Disclosures 2021 (Template UK KM1 "
    "/ Template UK OV1, which show both years). Every other year is BLANK rather than zero, for three "
    "distinct reasons that should not be conflated: FY2022 and FY2023 Pillar 3 documents were published "
    "but cannot be retrieved (FY2022's sole Wayback capture is an HTML bot-check page returned with HTTP "
    "200, not the PDF; FY2023 was never archived at all) - see the source citation below; FY2019's own "
    "Pillar 3 document predates the UK KM1/OV1 templates and simply does not contain this metric; and "
    "FY2024 onward were not published. FY2025 is structurally exempt - the PRA register records "
    "Modification by Consent of Rule 3.1 of the SDDT Regime (General Application) for FRN 400972, waiver "
    "ref A00009930P.pdf, START DATE 20/02/2025, no end date, and Rule 3.1 removes the Pillar 3 disclosure "
    "obligation outright; Kingdom Bank's year-end is 31 December, so FY2025 (year-end 31 December 2025) "
    "is the only year whose own year-end falls after that date. FY2024 PREDATES the modification and is "
    "therefore not explained by the register entry alone.\n\n"
    "BUT THE BANK ITSELF EXPLAINS FY2024, IN WORDS, AND THAT SETTLES IT (added 2026-09-18, GA-006). The "
    "Annual Report & Accounts 2024, in the Board Remuneration Committee section, states: 'The annual "
    "Pillar 3 disclosure document was reviewed by the Board in March 2024 and contained the enhanced "
    "remuneration disclosures required by CRD V. Due to the SDDT regime the Pillar 3 disclosure document "
    "will not be required in future years.' The document reviewed in March 2024 is the FY2023 edition, so "
    "the bank is stating that FY2023 was its LAST Pillar 3 and that none follows. The Annual Report & "
    "Accounts 2025 dates the approval precisely - 'On 19 February 2025 the PRA approved the Bank's "
    "modification by consent to become an SDDT firm' - which matches the register's 20/02/2025 start to "
    "the day. So FY2024 and FY2025 are NOT a failed search and NOT merely an unexplained blank: they are "
    "an affirmative, dated statement by the bank that no such document exists. FY2022 and FY2023 are a "
    "different case entirely - both were published and neither can be retrieved - and the two must not be "
    "read as the same kind of gap.\n\n"
    + ARCHIVE_PROVENANCE_NOTE + "\n\n"
    + EARLY_EDITIONS_NOTE
)

# GA-006 (2026-09-18): the Total RWAs and Total Capital Ratio sheets now carry
# an Annual Report note 29(j) series for FY2022-FY2025 as well, so on those two
# sheets the note above describes the PILLAR 3 series only, not the sheet.
PARTIAL_DISCLOSURE_NOTE_P3_SERIES_ONLY = (
    "On the Pillar 3 series specifically (the Annual Report note 29(j) series above covers "
    "FY2022-FY2025 and is unaffected by everything that follows): " + PARTIAL_DISCLOSURE_NOTE
)

TIER1_NOTE = (
    "Kingdom Bank's own Annual Reports state regulatory capital consists only of shareholders' funds "
    "(\"Core Equity Tier 1\") and subordinated liabilities (\"Tier 2\") - no Additional Tier 1 instruments "
    "are in issue in any year reviewed, so Tier 1 Capital equals CET1 Capital exactly. See the CET1 Capital "
    "sheet for the same figures and source."
)

TIER1_RATIO_NOTE = (
    "Tier 1 Ratio equals the CET1 Ratio exactly in every year - Kingdom Bank has never had any Additional "
    "Tier 1 capital in issue (see the Tier 1 Capital sheet), so Tier 1 Capital = CET1 Capital and therefore "
    "Tier 1 Capital / RWA = CET1 Capital / RWA. See the CET1 Ratio sheet for the same figures and source."
)

bw = BankWorkbook(bank_name="Kingdom Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="7A1F2B")

# ---------------------------------------------------------------
# Sheet 1: Balance Sheet - built first per the equity reconciliation
# ladder so each year's own Total equity is an independent check value.
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks (no such line existed before FY2010 - see source note)", {
        "FY2025": 38497, "FY2024": 38548, "FY2023": 34064, "FY2022": 23032, "FY2021": 10087,
        "FY2020": 6678, "FY2019": 6502, "FY2018": 4502, "FY2017": 4523, "FY2016": 4261, "FY2015": 3993, "FY2014": 3973,
        "FY2013": 3703, "FY2012": 4033, "FY2011": 2014, "FY2010": 3001,
    }),
    ("DATA", "Loans and advances to banks (FY2014's own label: 'Loans and advances to credit institutions'; FY2004 combines that year's separate banks/building-societies lines - see source note)", {
        "FY2025": 1217, "FY2024": 1243, "FY2023": 994, "FY2022": 1829, "FY2021": 10795,
        "FY2020": 14135, "FY2019": 5509, "FY2018": 5939, "FY2017": 11311, "FY2016": 9864, "FY2015": 10981, "FY2014": 11905,
        "FY2013": 17724, "FY2012": 13663, "FY2011": 16043, "FY2010": 16236, "FY2009": 15052, "FY2008": 23823,
        "FY2007": 23472, "FY2006": 11711, "FY2005": 10925, "FY2004": 9858,
    }),
    ("DATA", "Loans and advances to customers", {
        "FY2025": 118242, "FY2024": 97733, "FY2023": 77532, "FY2022": 63291, "FY2021": 53795,
        "FY2020": 47114, "FY2019": 45339, "FY2018": 41404, "FY2017": 38438, "FY2016": 35336, "FY2015": 33028, "FY2014": 29724,
        "FY2013": 28355, "FY2012": 27886, "FY2011": 28238, "FY2010": 32538, "FY2009": 33073, "FY2008": 26860,
        "FY2007": 20322, "FY2006": 21208, "FY2005": 17900, "FY2004": 16680,
    }),
    ("DATA", "Debt securities - available-for-sale, UK government gilts/bonds per FY2009 disclosure "
             "(not disclosed before FY2009, nil FY2010; see PRESENTATION NOTE (11))", {
        "FY2014": 0, "FY2013": 24, "FY2012": 25, "FY2011": 25, "FY2010": 0, "FY2009": 1692,
    }),
    ("DATA", "Investment property", {"FY2025": 650, "FY2020": 667, "FY2019": 667, "FY2018": 667, "FY2017": 500, "FY2016": 498}),
    ("DATA", "Intangible fixed assets (nil/absent before FY2008 - see source note)", {
        "FY2025": 18, "FY2024": 39, "FY2023": 75, "FY2022": 76, "FY2021": 83,
        "FY2020": 69, "FY2019": 69, "FY2018": 122, "FY2017": 189, "FY2016": 255, "FY2015": 168, "FY2014": 131,
        "FY2013": 162, "FY2012": 192, "FY2011": 222, "FY2010": 252, "FY2009": 283, "FY2008": 0,
    }),
    ("DATA", "Tangible fixed assets (FY2014 figure includes freehold investment property, not separately disclosed that year)", {
        "FY2025": 171, "FY2024": 174, "FY2023": 192, "FY2022": 230, "FY2021": 268,
        "FY2020": 730, "FY2019": 742, "FY2018": 685, "FY2017": 842, "FY2016": 845, "FY2015": 1369, "FY2014": 3883,
        "FY2013": 3599, "FY2012": 3399, "FY2011": 1289, "FY2010": 1355, "FY2009": 1384, "FY2008": 2235,
        "FY2007": 2171, "FY2006": 2035, "FY2005": 2110, "FY2004": 2146,
    }),
    ("DATA", "Fixed asset investment / Participating interests (49% of SALT Insurance Services Ltd, acquired 2 June 2008, sold during FY2012)", {
        "FY2011": 15, "FY2010": 15, "FY2009": 15, "FY2008": 15,
    }),
    ("DATA", "Other assets", {
        "FY2025": 23, "FY2024": 63, "FY2023": 37, "FY2022": 481, "FY2021": 347,
        "FY2020": 388, "FY2019": 482, "FY2018": 484, "FY2017": 447, "FY2016": 390, "FY2015": 270,
    }),
    ("DATA", "Prepayments and accrued income", {"FY2025": 1056, "FY2024": 662, "FY2023": 571}),
    ("DATA", "Prepayments, accrued income and other assets (combined line every year before FY2015 - see source note)", {
        "FY2014": 227, "FY2013": 251, "FY2012": 309, "FY2011": 296, "FY2010": 162, "FY2009": 75,
        "FY2008": 26, "FY2007": 13, "FY2006": 30, "FY2005": 20, "FY2004": 10,
    }),
    ("DATA", "Deferred tax assets", {"FY2025": 297, "FY2024": 30, "FY2023": 44, "FY2022": 83, "FY2021": 166}),
    ("TOTAL", "Total assets", {
        "FY2025": 160171, "FY2024": 138492, "FY2023": 113509, "FY2022": 89022, "FY2021": 75541,
        "FY2020": 69781, "FY2019": 59310, "FY2018": 53803, "FY2017": 56250, "FY2016": 51449, "FY2015": 49809, "FY2014": 49843,
    }),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Loans and advances from credit institutions due within 3 months (existed FY2006-FY2009 only - see source note)", {
        "FY2009": 0, "FY2008": 507, "FY2007": 510, "FY2006": 503,
    }),
    ("DATA", "Customer accounts", {
        "FY2025": 141758, "FY2024": 121269, "FY2023": 102091, "FY2022": 78452, "FY2021": 66668,
        "FY2020": 61287, "FY2019": 51378, "FY2018": 46112, "FY2017": 48656, "FY2016": 43885, "FY2015": 41906, "FY2014": 42935,
        "FY2013": 47013, "FY2012": 42546, "FY2011": 41638, "FY2010": 47247, "FY2009": 45168, "FY2008": 46737,
        "FY2007": 39931, "FY2006": 29520, "FY2005": 26294, "FY2004": 24187,
    }),
    ("DATA", "Other liabilities", {
        "FY2025": 616, "FY2024": 448, "FY2023": 438, "FY2022": 517, "FY2021": 661,
        "FY2020": 292, "FY2019": 356, "FY2018": 352, "FY2017": 235, "FY2016": 316, "FY2015": 591, "FY2014": 267,
        "FY2013": 267, "FY2012": 412, "FY2011": 346, "FY2010": 341, "FY2009": 296, "FY2008": 322,
        "FY2007": 274, "FY2006": 231, "FY2005": 176, "FY2004": 290,
    }),
    ("DATA", "Accruals and deferred income", {"FY2025": 1289, "FY2024": 563, "FY2023": 404}),
    ("DATA", "Subordinated liabilities (FY2014's own label: 'Subordinated deposits'; nil/absent before FY2007 - see source note)", {
        "FY2025": 700, "FY2024": 700, "FY2023": 700, "FY2022": 700, "FY2021": 761,
        "FY2020": 1431, "FY2019": 1431, "FY2018": 1431, "FY2017": 1581, "FY2016": 1581, "FY2015": 1681, "FY2014": 1681,
        "FY2013": 1892, "FY2012": 1892, "FY2011": 1892, "FY2010": 1322, "FY2009": 1322, "FY2008": 172,
        "FY2007": 172,
    }),
    ("TOTAL", "Total liabilities", {
        "FY2025": 144363, "FY2024": 122980, "FY2023": 103633, "FY2022": 79669, "FY2021": 68090,
        "FY2020": 63010, "FY2019": 53165, "FY2018": 47895, "FY2017": 50472, "FY2016": 45782, "FY2015": 44178, "FY2014": 44883,
        "FY2013": 49172, "FY2012": 44850, "FY2011": 43876, "FY2010": 48910, "FY2009": 46786, "FY2008": 47738,
        "FY2007": 40887, "FY2006": 30426, "FY2005": 26643, "FY2004": 24477,
    }),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital (FY2004 combines that year's separate 'called up' and 'unpaid' share capital lines, both fully paid by FY2005 - see source note)", {
        "FY2025": 13237, "FY2024": 12067, "FY2023": 6667, "FY2022": 6667, "FY2021": 4867,
        "FY2020": 4867, "FY2019": 4217, "FY2018": 4217, "FY2017": 4217, "FY2016": 4217, "FY2015": 4217, "FY2014": 4217,
        "FY2013": 4217, "FY2012": 4217, "FY2011": 4217, "FY2010": 4217, "FY2009": 4217, "FY2008": 4217,
        "FY2007": 4217, "FY2006": 4217, "FY2005": 4217, "FY2004": 4217,
    }),
    ("DATA", "Revaluation reserve (fully extinguished during FY2021 - see Statement of Changes in Equity sheet; nil/absent before FY2007, when the Bank's freehold properties were first professionally revalued)", {
        "FY2020": 172, "FY2019": 172, "FY2018": 172, "FY2017": 172, "FY2016": 166, "FY2015": 164, "FY2014": 578,
        "FY2013": 333, "FY2012": 416, "FY2011": 71, "FY2010": 71, "FY2009": 65, "FY2008": 406, "FY2007": 406,
    }),
    ("DATA", "Profit and loss account", {
        "FY2025": 2571, "FY2024": 3445, "FY2023": 3209, "FY2022": 2686, "FY2021": 2584,
        "FY2020": 1732, "FY2019": 1756, "FY2018": 1519, "FY2017": 1389, "FY2016": 1284, "FY2015": 1250, "FY2014": 165,
        "FY2013": 96, "FY2012": 24, "FY2011": -22, "FY2010": 361, "FY2009": 506, "FY2008": 598,
        "FY2007": 468, "FY2006": 341, "FY2005": 95, "FY2004": 0,
    }),
    ("TOTAL", "Total shareholders' funds", {
        "FY2025": 15808, "FY2024": 15512, "FY2023": 9876, "FY2022": 9353, "FY2021": 7451,
        "FY2020": 6771, "FY2019": 6145, "FY2018": 5908, "FY2017": 5778, "FY2016": 5667, "FY2015": 5631, "FY2014": 4960,
        "FY2013": 4646, "FY2012": 4657, "FY2011": 4266, "FY2010": 4649, "FY2009": 4788, "FY2008": 5221,
        "FY2007": 5091, "FY2006": 4558, "FY2005": 4312, "FY2004": 4217,
    }),
    ("TOTAL", "Total liabilities and total shareholders' funds", {
        "FY2025": 160171, "FY2024": 138492, "FY2023": 113509, "FY2022": 89022, "FY2021": 75541,
        "FY2020": 69781, "FY2019": 59310, "FY2018": 53803, "FY2017": 56250, "FY2016": 51449, "FY2015": 49809, "FY2014": 49843,
        "FY2013": 53818, "FY2012": 49507, "FY2011": 48142, "FY2010": 53559, "FY2009": 51574, "FY2008": 52959,
        "FY2007": 45978, "FY2006": 34984, "FY2005": 30955, "FY2004": 28695,
    }),
]

bw.add_balance_sheet_sheet(
    title="Kingdom Bank Limited — Balance Sheet",
    subtitle="Statement of financial position, Bank/solo basis, £'000. See source note at bottom.",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=460,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet 2: Profit & Loss
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable", {
        "FY2025": 8637, "FY2024": 7828, "FY2023": 6003, "FY2022": 3144, "FY2021": 2419,
        "FY2020": 2297, "FY2019": 2330, "FY2018": 2168, "FY2017": 1955, "FY2016": 1904, "FY2015": 1744, "FY2014": 1699,
        "FY2013": 1776, "FY2012": 1755, "FY2011": 1843, "FY2010": 1794, "FY2009": 1646, "FY2008": 2959,
        "FY2007": 2678, "FY2006": 1920, "FY2005": 1703,
    }),
    ("DATA", "Interest payable", {
        "FY2025": -2942, "FY2024": -3207, "FY2023": -2193, "FY2022": -454, "FY2021": -345,
        "FY2020": -523, "FY2019": -552, "FY2018": -495, "FY2017": -478, "FY2016": -527, "FY2015": -511, "FY2014": -650,
        "FY2013": -915, "FY2012": -877, "FY2011": -755, "FY2010": -811, "FY2009": -859, "FY2008": -2004,
        "FY2007": -1827, "FY2006": -1161, "FY2005": -1051,
    }),
    ("TOTAL", "Net interest income", {
        "FY2025": 5695, "FY2024": 4621, "FY2023": 3810, "FY2022": 2690, "FY2021": 2074,
        "FY2020": 1774, "FY2019": 1778, "FY2018": 1673, "FY2017": 1477, "FY2016": 1377, "FY2015": 1233, "FY2014": 1049,
        "FY2013": 861, "FY2012": 878, "FY2011": 1088, "FY2010": 983, "FY2009": 787, "FY2008": 955,
        "FY2007": 851, "FY2006": 759, "FY2005": 652,
    }),
    ("DATA", "Insurance commission income (FY2014's own label: 'Fees and commission receivable/(payable), net'; FY2004-FY2013 own presentation combines fees receivable and payable into one net figure - see source note)", {
        "FY2025": 666, "FY2024": 576, "FY2023": 543, "FY2022": 482, "FY2021": 419,
        "FY2020": 433, "FY2019": 388, "FY2018": 369, "FY2017": 335, "FY2016": 319, "FY2015": 315, "FY2014": 361,
        "FY2013": 362, "FY2012": 313, "FY2011": 258, "FY2010": 248, "FY2009": 265, "FY2008": 168,
        "FY2007": 86, "FY2006": 129, "FY2005": 96,
    }),
    ("DATA", "Other operating income", {
        "FY2025": 43, "FY2024": 8, "FY2023": 7, "FY2022": 3, "FY2021": 117,
        "FY2020": 80, "FY2019": 76, "FY2018": 64, "FY2017": 63, "FY2016": 59, "FY2015": 89, "FY2014": 138,
        "FY2013": 149, "FY2012": 43, "FY2011": 53, "FY2010": 35, "FY2009": 31, "FY2008": 26,
        "FY2007": 16, "FY2006": 12, "FY2005": 13,
    }),
    ("TOTAL", "Total net income (FY2014-FY2022's own equivalent subtotal is labelled 'Operating income' - same calculation)",
     {
         "FY2025": 6404, "FY2024": 5205, "FY2023": 4360, "FY2022": 3175, "FY2021": 2610,
         "FY2020": 2287, "FY2019": 2242, "FY2018": 2106, "FY2017": 1875, "FY2016": 1755, "FY2015": 1637, "FY2014": 1548,
         "FY2013": 1372, "FY2012": 1234, "FY2011": 1399, "FY2010": 1266, "FY2009": 1083, "FY2008": 1149,
         "FY2007": 953, "FY2006": 900, "FY2005": 761,
     }),
    ("TOTAL", "Administrative expenses", {
        "FY2025": -7241, "FY2024": -4776, "FY2023": -3597, "FY2022": -2953, "FY2021": -2437,
        "FY2020": -2167, "FY2019": -1780, "FY2018": -1776, "FY2017": -1538, "FY2016": -1554, "FY2015": -1487, "FY2014": -1413,
        "FY2013": -1241, "FY2012": -1201, "FY2011": -1185, "FY2010": -1194, "FY2009": -1082, "FY2008": -838,
        "FY2007": -726, "FY2006": -548, "FY2005": -568,
    }),
    ("DATA", "Depreciation and amortisation", {
        "FY2025": -67, "FY2024": -79, "FY2023": -86, "FY2022": -85, "FY2021": -80,
        "FY2020": -81, "FY2019": -93, "FY2018": -109, "FY2017": -111, "FY2016": -130, "FY2015": -124, "FY2014": -113,
        "FY2013": -117, "FY2012": -126, "FY2011": -116, "FY2010": -117, "FY2009": -102, "FY2008": -66,
        "FY2007": -37, "FY2006": -47, "FY2005": -44,
    }),
    ("DATA", "Profit on sale / unrealised surplus on revaluation of investment property (FY2004-FY2012 own equivalents: profit on sale of participating interests/fixed assets, net of loss on revaluation of property - see source note)", {
        "FY2022": 0, "FY2021": 634, "FY2018": 0, "FY2017": 2, "FY2015": 898,
        "FY2012": 40, "FY2009": -30, "FY2007": 22, "FY2006": 43,
    }),
    ("DATA", "Movement in loan loss provision (FY2014's own label: 'Provision for bad and doubtful debts')", {
        "FY2025": -158, "FY2024": -9, "FY2023": -12, "FY2022": -9, "FY2021": -24,
        "FY2020": -77, "FY2019": -43, "FY2018": -43, "FY2017": -88, "FY2016": -16, "FY2015": -21, "FY2014": 70,
        "FY2013": 92, "FY2012": 111, "FY2011": -576, "FY2010": -127, "FY2009": -74, "FY2008": -66,
        "FY2007": 10, "FY2006": -38, "FY2005": -13,
    }),
    ("TOTAL", "(Loss)/profit on ordinary activities before taxation", {
        "FY2025": -1062, "FY2024": 341, "FY2023": 665, "FY2022": 128, "FY2021": 703,
        "FY2020": -38, "FY2019": 326, "FY2018": 178, "FY2017": 140, "FY2016": 55, "FY2015": 903, "FY2014": 92,
        "FY2013": 106, "FY2012": 58, "FY2011": -478, "FY2010": -172, "FY2009": -205, "FY2008": 179,
        "FY2007": 222, "FY2006": 310, "FY2005": 136,
    }),
    ("DATA", "Tax credit/(charge) on (loss)/profit", {
        "FY2025": 258, "FY2024": -62, "FY2023": -142, "FY2022": -26, "FY2021": -23,
        "FY2020": 14, "FY2019": -69, "FY2018": -32, "FY2017": -35, "FY2016": -21, "FY2015": -183, "FY2014": -23,
        "FY2013": -34, "FY2012": -12, "FY2011": 95, "FY2010": 27, "FY2009": 113, "FY2008": -49,
        "FY2007": -95, "FY2006": -64, "FY2005": -41,
    }),
    ("TOTAL", "(Loss)/profit and total comprehensive income for the financial year", {
        "FY2025": -804, "FY2024": 279, "FY2023": 523, "FY2022": 102, "FY2021": 680,
        "FY2020": -24, "FY2019": 257, "FY2018": 146, "FY2017": 105, "FY2016": 34, "FY2015": 720, "FY2014": 69,
        "FY2013": 72, "FY2012": 46, "FY2011": -383, "FY2010": -145, "FY2009": -92, "FY2008": 130,
        "FY2007": 127, "FY2006": 246, "FY2005": 95,
    }),
]

bw.add_income_statement_sheet(
    title="Kingdom Bank Limited — Profit & Loss",
    subtitle="Income statement, Bank/solo basis, £'000. All results arise from continuing operations, attributable to the "
              "owners of the Bank, every year. See source note at bottom.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=90,
    source_height=460,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet 3: Statement of Changes in Equity - per-year reconciliation
# ladder confirmed: every year's own closing balance ties exactly to
# both the next year's own opening balance and that year's own Balance
# Sheet Total shareholders' funds, FY2014 onward. Zero plug rows needed
# anywhere. FY2014's own closing balance is used here (old UK GAAP, as
# originally filed) rather than the FRS 102-restated 1 January 2015
# opening figure the FY2015 Annual Report separately discloses - see
# the source note below for the one reconciling break this creates.
# ---------------------------------------------------------------
equity_headers = ["Called up share capital", "Profit and loss account", "Revaluation reserve", "Total shareholders' funds"]
equity_rows = [
    ("TOTAL", "Balance as at 31 December 2004 (FY2004 closing - first trading period, 1 Feb-31 Dec 2004; no profit "
     "and loss account was prepared for this period, see source note, so no opening balance/movement row precedes "
     "this one)", (4217, 0, None, 4217)),
    ("DATA", "Profit for the financial year", (None, 95, None, 95)),
    ("TOTAL", "Balance as at 31 December 2005 (FY2005 closing)", (4217, 95, None, 4312)),
    ("DATA", "Profit for the financial year", (None, 246, None, 246)),
    ("TOTAL", "Balance as at 31 December 2006 (FY2006 closing)", (4217, 341, None, 4558)),
    ("DATA", "Profit for the financial year", (None, 127, None, 127)),
    ("DATA", "Revaluation surplus during the year on freehold properties", (None, None, 406, 406)),
    ("TOTAL", "Balance as at 31 December 2007 (FY2007 closing)", (4217, 468, 406, 5091)),
    ("DATA", "Profit for the financial year", (None, 130, None, 130)),
    ("TOTAL", "Balance as at 31 December 2008 (FY2008 closing)", (4217, 598, 406, 5221)),
    ("DATA", "Loss for the financial year", (None, -92, None, -92)),
    ("DATA", "Revaluation deficit during the year on freehold properties (see PRESENTATION NOTE (9))", (None, None, -341, -341)),
    ("TOTAL", "Balance as at 31 December 2009 (FY2009 closing, own as-filed figures - see PRESENTATION NOTE (9) on the "
     "FY2010 restatement of the FY2009 comparative)", (4217, 506, 65, 4788)),
    ("DATA", "Loss for the financial year", (None, -145, None, -145)),
    ("DATA", "Reversal of previously recognised revaluation losses on freehold properties", (None, None, 6, 6)),
    ("TOTAL", "Balance as at 31 December 2010 (FY2010 closing)", (4217, 361, 71, 4649)),
    ("DATA", "Loss for the financial year", (None, -383, None, -383)),
    ("TOTAL", "Balance as at 31 December 2011 (FY2011 closing)", (4217, -22, 71, 4266)),
    ("DATA", "Profit for the financial year", (None, 46, None, 46)),
    ("DATA", "Revaluation surplus during the year on freehold properties", (None, None, 345, 345)),
    ("TOTAL", "Balance as at 31 December 2012 (FY2012 closing)", (4217, 24, 416, 4657)),
    ("DATA", "Profit for the financial year", (None, 72, None, 72)),
    ("DATA", "Revaluation deficit during the year on freehold properties", (None, None, -83, -83)),
    ("TOTAL", "Balance as at 1 January 2014 (own report, old UK GAAP/BBA SORP)", (4217, 96, 333, 4646)),
    ("DATA", "Profit for the financial year", (None, 69, None, 69)),
    ("DATA", "Revaluation surplus during the year on investment properties", (None, None, 167, 167)),
    ("DATA", "Revaluation deficit during the year on investment properties", (None, None, -10, -10)),
    ("DATA", "Revaluation surplus during the year on freehold buildings", (None, None, 88, 88)),
    ("TOTAL", "Balance as at 31 December 2014 (FY2014 closing, own report)", (4217, 165, 578, 4960)),
    ("DATA", "FRS 102 first-time-adoption restatement (see source note - not a FY2014 or FY2015 P&L movement)",
     (None, 365, -478, -113)),
    ("TOTAL", "Balance as at 1 January 2015 (FRS 102-restated, per FY2015 Annual Report SOCE)", (4217, 530, 100, 4847)),
    ("DATA", "Profit for the financial year", (None, 720, None, 720)),
    ("DATA", "Unrealised surplus on revaluation of operating properties, net of deferred tax", (None, None, 64, 64)),
    ("TOTAL", "Balance as at 31 December 2015 (FY2015 closing)", (4217, 1250, 164, 5631)),
    ("DATA", "Profit for the financial year", (None, 34, None, 34)),
    ("DATA", "Unrealised surplus on revaluation of operating properties, net of deferred tax", (None, None, 2, 2)),
    ("TOTAL", "Balance as at 31 December 2016 (FY2016 closing)", (4217, 1284, 166, 5667)),
    ("DATA", "Profit for the financial year", (None, 105, None, 105)),
    ("DATA", "Unrealised surplus on revaluation of operating property, net of deferred tax", (None, None, 6, 6)),
    ("TOTAL", "Balance as at 31 December 2017 (FY2017 closing)", (4217, 1389, 172, 5778)),
    ("DATA", "Profit for the financial year", (None, 146, None, 146)),
    ("DATA", "Dividends paid", (None, -16, None, -16)),
    ("TOTAL", "Balance as at 31 December 2018 (FY2018 closing)", (4217, 1519, 172, 5908)),
    ("DATA", "Profit for the financial year", (None, 257, None, 257)),
    ("TOTAL", "Balance as at 31 December 2019 (FY2019 closing)", (4217, 1756, 172, 6145)),
    ("DATA", "Loss for the financial year", (None, -24, None, -24)),
    ("DATA", "Share allotment", (650, None, None, 650)),
    ("TOTAL", "Balance as at 31 December 2020 (FY2020 closing)", (4867, 1732, 172, 6771)),
    ("DATA", "Profit for the financial year", (None, 680, None, 680)),
    ("DATA", "Transfer of revaluation reserve to profit and loss reserve upon reclassification of operating property", (None, 172, -172, None)),
    ("TOTAL", "Balance as at 31 December 2021 (FY2021 closing)", (4867, 2584, 0, 7451)),
    ("DATA", "Profit for the financial year", (None, 102, None, 102)),
    ("DATA", "Share allotment", (1800, None, None, 1800)),
    ("TOTAL", "Balance as at 31 December 2022 (FY2022 closing)", (6667, 2686, 0, 9353)),
    ("DATA", "Profit for the financial year", (None, 523, None, 523)),
    ("TOTAL", "Balance as at 31 December 2023 (FY2023 closing)", (6667, 3209, 0, 9876)),
    ("DATA", "Profit for the financial year", (None, 279, None, 279)),
    ("DATA", "Share allotment", (5400, None, None, 5400)),
    ("DATA", "Dividends paid", (None, -43, None, -43)),
    ("TOTAL", "Balance as at 31 December 2024 (FY2024 closing)", (12067, 3445, 0, 15512)),
    ("DATA", "Loss for the financial year", (None, -804, None, -804)),
    ("DATA", "Share allotment", (1170, None, None, 1170)),
    ("DATA", "Dividends paid", (None, -70, None, -70)),
    ("TOTAL", "Balance as at 31 December 2025 (FY2025 closing)", (13237, 2571, 0, 15808)),
]

bw.add_equity_changes_sheet(
    title="Kingdom Bank Limited — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, from FY2004 (first trading period) onward. Equity "
              "reconciliation ladder confirmed: every year's own closing balance ties exactly to both the next "
              "year's own opening balance and that year's own Balance Sheet Total shareholders' funds - zero plug "
              "rows needed anywhere, including across the FY2004-FY2013 extension. £'000. FY2014 is "
              "shown as originally filed under old UK GAAP/the BBA SORP (no SOCE was published that year - built "
              "here from Notes 16-19 of the FY2014 Annual Report); FRS 102 was first adopted for FY2015 and its "
              "Annual Report separately discloses a restated 1 January 2015 opening position (£4,847k total "
              "shareholders' funds) that differs from the £4,960k shown here as FY2014's own closing figure - both "
              "are shown, with the reconciling FRS 102 transition adjustment on its own row, so the ladder still "
              "ties exactly on both sides of the GAAP change. The Revaluation reserve column runs down from £578k "
              "(FY2014) to a flat £172k (FY2017-FY2020) as historical property revaluations were realised, and is "
              "fully extinguished from FY2021 onward (see FY2021's transfer row) and shown as 0, not blank, for "
              "FY2022-FY2025 to make the reconciliation explicit.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
)

# ---------------------------------------------------------------
# Sheet 4: Cash Flow Statement - FY2004-FY2014 (all 11 years) have no
# cash flow statement at all (FRS 1 wholly-owned-subsidiary exemption -
# see source note), so these are the columns left entirely blank on
# this sheet, not zero.
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Net cash (used in)/generated from operating activities excluding tax", {
        "FY2025": -1079, "FY2024": -481, "FY2023": 10255, "FY2022": 3157, "FY2021": -630,
        "FY2020": 7026, "FY2019": 1978, "FY2018": -4088, "FY2017": 1125, "FY2016": 718, "FY2015": -5610,
    }),
    ("DATA", "Taxation paid", {
        "FY2025": -55, "FY2024": -102, "FY2023": -11, "FY2022": -25,
        "FY2020": -56, "FY2019": -40, "FY2018": -33, "FY2017": -23, "FY2016": -233, "FY2015": -2,
    }),
    ("TOTAL", "Net cash (used in)/generated from operating activities", {
        "FY2025": -1134, "FY2024": -583, "FY2023": 10244, "FY2022": 3132, "FY2021": -630,
        "FY2020": 6970, "FY2019": 1938, "FY2018": -4121, "FY2017": 1102, "FY2016": 485, "FY2015": -5612,
    }),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of intangible assets", {
        "FY2025": 0, "FY2024": 0, "FY2023": -23, "FY2022": -16, "FY2021": -47,
        "FY2020": -39, "FY2019": -8, "FY2018": -12, "FY2017": -16, "FY2016": -170, "FY2015": -33,
    }),
    ("DATA", "Capital expenditure on investment property", {"FY2015": -13}),
    ("DATA", "Purchase of tangible assets", {
        "FY2025": -43, "FY2024": -41, "FY2023": -24, "FY2022": -24, "FY2021": -197,
        "FY2020": -30, "FY2019": -89, "FY2018": -40, "FY2017": -15, "FY2016": -21, "FY2015": -23,
    }),
    ("DATA", "Sale of investment property / proceeds from disposals of investment property", {"FY2021": 2013, "FY2015": 3394}),
    ("TOTAL", "Net cash (used in)/generated from investing activities", {
        "FY2025": -43, "FY2024": -41, "FY2023": -47, "FY2022": -40, "FY2021": 1769,
        "FY2020": -69, "FY2019": -97, "FY2018": -52, "FY2017": -31, "FY2016": -191, "FY2015": 3325,
    }),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Repayment of subordinated liabilities", {
        "FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": -61, "FY2021": -670, "FY2018": -150, "FY2016": -800,
    }),
    ("DATA", "Issue of subordinated liabilities", {"FY2016": 700}),
    ("DATA", "Share allotment", {
        "FY2025": 1170, "FY2024": 5400, "FY2023": 0, "FY2022": 1800, "FY2021": 0, "FY2020": 650,
    }),
    ("DATA", "Dividends paid", {"FY2025": -70, "FY2024": -43, "FY2019": -20, "FY2018": -16}),
    ("TOTAL", "Net cash generated from/(used in) financing activities", {
        "FY2025": 1100, "FY2024": 5357, "FY2023": 0, "FY2022": 1739, "FY2021": -670,
        "FY2020": 650, "FY2019": -20, "FY2018": -166, "FY2017": 0, "FY2016": -100, "FY2015": 0,
    }),
    ("TOTAL", "Net movement in cash and cash equivalents", {
        "FY2025": -77, "FY2024": 4733, "FY2023": 10197, "FY2022": 4831, "FY2021": 469,
        "FY2020": 7551, "FY2019": 1821, "FY2018": -4339, "FY2017": 1071, "FY2016": 194, "FY2015": -2287,
    }),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {
        "FY2025": 39791, "FY2024": 35058, "FY2023": 24861, "FY2022": 20030, "FY2021": 19561,
        "FY2020": 12010, "FY2019": 10189, "FY2018": 14528, "FY2017": 13457, "FY2016": 13263, "FY2015": 15550,
    }),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {
        "FY2025": 39714, "FY2024": 39791, "FY2023": 35058, "FY2022": 24861, "FY2021": 20030,
        "FY2020": 19561, "FY2019": 12010, "FY2018": 10189, "FY2017": 14528, "FY2016": 13457, "FY2015": 13263,
    }),
]

bw.add_cash_flow_sheet(
    title="Kingdom Bank Limited — Statement of Cash Flows",
    subtitle="Bank/solo basis, £'000. FY2004-FY2014 (11 years) have no cash flow statement (FRS 1 wholly-owned-"
              "subsidiary exemption - columns intentionally blank, not zero). See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=68,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet 5: Asset Quality - loan book by product (Note 12a/9a) plus loan
# loss provision movement, incl. collective/IBNR split where disclosed
# (Note 12c, FY2022 onward only). No IFRS 9 stage split exists - FRS 102
# (old UK GAAP for FY2014) entity, not IFRS 9. FY2014 used a one-off,
# more granular General/Specific/suspended-interest provision structure
# - see the dedicated FY2014-only rows below.
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, gross", {}),
    ("DATA", "Organisational/Charity mortgages (FY2014-FY2021's own label: 'Charity mortgages')", {
        "FY2025": 98455, "FY2024": 79806, "FY2023": 60628, "FY2022": 48320, "FY2021": 42846,
        "FY2020": 40095, "FY2019": 40653, "FY2018": 40390, "FY2017": 37417, "FY2016": 34479, "FY2015": 31898, "FY2014": 29039,
    }),
    ("DATA", "Personal mortgages", {
        "FY2025": 19897, "FY2024": 18049, "FY2023": 17017, "FY2022": 15086, "FY2021": 11063,
        "FY2020": 7074, "FY2019": 4659, "FY2018": 1008, "FY2017": 1027, "FY2016": 764, "FY2015": 993, "FY2014": 538,
    }),
    ("DATA", "Charity loans, unsecured (FY2014-FY2018 only - discontinued as a separate category from FY2019)", {
        "FY2018": 6, "FY2017": 20, "FY2016": 34, "FY2015": 46, "FY2014": 56,
    }),
    ("DATA", "Personal loans, unsecured (FY2014-FY2018 only - discontinued as a separate category from FY2019)", {
        "FY2018": 4, "FY2017": 9, "FY2016": 4, "FY2015": 18, "FY2014": 10,
    }),
    ("DATA", "Fully secured lending to other group companies (FY2014-FY2021 only)", {
        "FY2021": 0, "FY2020": 269, "FY2019": 274, "FY2018": 279, "FY2017": 282, "FY2016": 284, "FY2015": 286, "FY2014": 289,
    }),
    ("DATA", "Unsecured lending to other group companies (FY2014 only - nil that year)", {"FY2014": 0}),
    ("DATA", "Unsecured personal loans", {"FY2025": 89, "FY2024": 72, "FY2023": 72, "FY2022": 58, "FY2021": 50}),
    ("TOTAL", "Gross advances to customers", {
        "FY2025": 118441, "FY2024": 97927, "FY2023": 77717, "FY2022": 63464, "FY2021": 53959,
        "FY2020": 47438, "FY2019": 45586, "FY2018": 41687, "FY2017": 38755, "FY2016": 35565, "FY2015": 33241, "FY2014": 29932,
    }),
    ("DATA", "Less: loan loss provision", {
        "FY2025": -199, "FY2024": -194, "FY2023": -185, "FY2022": -173, "FY2021": -164,
        "FY2020": -324, "FY2019": -247, "FY2018": -283, "FY2017": -317, "FY2016": -229, "FY2015": -213, "FY2014": -192,
    }),
    ("DATA", "Less: provision for suspended interest (FY2014 only - old-GAAP structure, deducted separately from the main loan loss provision)",
     {"FY2014": -16}),
    ("TOTAL", "Net advances to customers", {
        "FY2025": 118242, "FY2024": 97733, "FY2023": 77532, "FY2022": 63291, "FY2021": 53795,
        "FY2020": 47114, "FY2019": 45339, "FY2018": 41404, "FY2017": 38438, "FY2016": 35336, "FY2015": 33028, "FY2014": 29724,
    }),
    ("DATA", "Loan loss provision coverage (% of gross advances)", {
        "FY2025": "0.17%", "FY2024": "0.20%", "FY2023": "0.24%", "FY2022": "0.27%", "FY2021": "0.30%",
        "FY2020": "0.68%", "FY2019": "0.54%", "FY2018": "0.68%", "FY2017": "0.82%", "FY2016": "0.64%", "FY2015": "0.64%", "FY2014": "0.64%",
    }),
    ("SECTION", "Loan loss provision movement (Note 12c/9c)", {}),
    ("DATA", "Balance at 1 January", {
        "FY2025": 194, "FY2024": 185, "FY2023": 173, "FY2022": 164, "FY2021": 324,
        "FY2020": 247, "FY2019": 283, "FY2018": 317, "FY2017": 229, "FY2016": 213, "FY2015": 192,
    }),
    ("DATA", "Charge for the year", {
        "FY2025": 160, "FY2024": 11, "FY2023": 13, "FY2022": 10, "FY2021": 26,
        "FY2020": 89, "FY2019": 44, "FY2018": 60, "FY2017": 113, "FY2016": 34, "FY2015": 46,
    }),
    ("DATA", "Utilised during the year", {
        "FY2025": -153, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": -184,
        "FY2020": 0, "FY2019": -79, "FY2018": -77,
    }),
    ("DATA", "Released during the year", {
        "FY2025": -2, "FY2024": -2, "FY2023": -1, "FY2022": -1, "FY2021": -2,
        "FY2020": -12, "FY2019": -1, "FY2018": -17, "FY2017": -25, "FY2016": -18, "FY2015": -25,
    }),
    ("TOTAL", "Balance at 31 December", {
        "FY2025": 199, "FY2024": 194, "FY2023": 185, "FY2022": 173, "FY2021": 164,
        "FY2020": 324, "FY2019": 247, "FY2018": 283, "FY2017": 317, "FY2016": 229, "FY2015": 213, "FY2014": 192,
    }),
    ("DATA", "Of which: collective/IBNR provision (not disclosed for FY2014-FY2021 - sub-split introduced FY2022 onward)",
     {"FY2025": 156, "FY2024": 148, "FY2023": 137, "FY2022": 124}),
    ("SECTION", "FY2014-only provision structure (old UK GAAP/BBA SORP - see source note)", {}),
    ("DATA", "General provision (IBNR-based): balance at 1 January", {"FY2014": 163}),
    ("DATA", "General provision (IBNR-based): released during the year", {"FY2014": -30}),
    ("DATA", "General provision (IBNR-based): balance at 31 December", {"FY2014": 133}),
    ("DATA", "Specific provision: balance at 1 January", {"FY2014": 99}),
    ("DATA", "Specific provision: charge for the year", {"FY2014": 22}),
    ("DATA", "Specific provision: released during the year", {"FY2014": -62}),
    ("DATA", "Specific provision: balance at 31 December", {"FY2014": 59}),
    ("DATA", "Provision for suspended interest: balance at 1 January", {"FY2014": 25}),
    ("DATA", "Provision for suspended interest: decrease during the year", {"FY2014": -9}),
    ("DATA", "Provision for suspended interest: balance at 31 December", {"FY2014": 16}),
]

bw.add_asset_quality_sheet(
    title="Kingdom Bank Limited — Asset Quality",
    subtitle="Loan book by product (Note 12a/9a) and loan loss provision movement (Note 12c/9c), Bank/solo basis, "
              "£'000. No IFRS 9 stage 1/2/3 split is disclosed in any year - this entity applies FRS 102 (old UK "
              "GAAP for FY2014), not IFRS 9. See source note at bottom.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=100,
    source_height=340,
    unit_suffix=" (£'000)",
    years=PILLAR3_YEARS,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
#
# HD-045 correction (2026-09-05): re-verifying seven of this bank's own
# primary-source PDFs to extend the build back to FY2014 turned up a
# Key Performance Indicators table in each year's Strategic Report
# (FY2015 onward) disclosing a CET1 ratio, Leverage ratio and LCR ratio
# - contradicting this workbook's earlier "not publicly disclosed"
# treatment of those three metrics for FY2021-FY2025. That treatment is
# corrected below with real, sourced figures for all years FY2015-
# FY2025 (FY2014 predates the KPI table and remains not disclosed).
#
# LINK-ROT REPAIR + SECOND CORRECTION (2026-09-15): three of Kingdom
# Bank's own annual Pillar 3 disclosure documents (FY2019, FY2020,
# FY2021) have been recovered from the Wayback Machine and read in full.
# This overturns the earlier finding that the bank's Pillar 3 practice
# lapsed after FY2015 and that Total Capital Ratio, Total RWAs and NSFR
# were undisclosed in every year - all three are disclosed, along with a
# full UK OV1 RWA breakdown, for FY2021 and FY2020. Those four sheets
# stop being "Not publicly disclosed" sheets below. Only MREL Ratio
# remains genuinely undisclosed in every year.
#
# TWO SERIES, NEVER MERGED. The Pillar 3 documents and the Annual Report
# KPI table disagree on CET1 Ratio, Leverage Ratio and LCR, because they
# are computed on different bases (regulatory own funds excluding
# unapproved profits vs accounting shareholders' funds; leverage
# excluding vs including central bank claims; a 12-month average LCR vs
# the Annual Report's own measure). Per this project's validation gate,
# the Pillar 3 figures are added as SEPARATE LABELLED ROWS and the
# existing KPI-table rows are left untouched rather than overwritten.
# ---------------------------------------------------------------

def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, f"Bank/solo basis, {unit}" if unit else "Bank/solo basis",
                         rows_data, p3_sources(), note=note, first_col_width=52, source_height=230,
                         years=PILLAR3_YEARS)


# ---------------------------------------------------------------
# KM1 Key Metrics (wayfinder/km1/map.md) - the Bank's own published
# "Template UK KM1 - Key metrics template", reproduced whole in its own row
# order, row numbers, labels and printed precision. Called BEFORE the first
# add_metric_sheet() so the sheet lands immediately after Asset Quality and
# immediately before CET1 Capital: sheet order follows call order.
#
# COLUMN PROVENANCE, which differs by year and is stated on the sheet:
#   FY2021 - from its OWN edition (the Pillar 3 approved 9 June 2022), whose
#            KM1 is headed with a "31 December 2021" column (map rule 1).
#   FY2020 - from that same FY2021 edition's "31 December 2020" COMPARATIVE
#            column, because the FY2020 edition prints NO key-metrics table
#            at all - its contents page runs Introduction / Risk management /
#            Board and committee structure / Own funds / Exposure amounts /
#            Credit risk / Remuneration / Conclusion, with no key-metrics
#            section anywhere. Whole table missing, so this is map rule 28
#            (fill from the later edition's comparative) and NOT map rule 20.
#   Every other year - BLANK, for two different reasons, both set out in the
#            sheet note: FY2019 and earlier have no comparative anywhere, and
#            FY2022 onward have no obtainable edition.
# ---------------------------------------------------------------
# LEADING-GAPS QUEUE, 2026-09-18. The FY2022-FY2025 columns on this sheet, on
# RWA Breakdown and on NSFR were entirely EMPTY. The notes below already
# explained why, but an empty cell states nothing on its own: a reader sees a
# blank and cannot tell a gap in OUR REACH from a gap in the BANK'S PUBLISHING.
# These cells now carry that statement explicitly, and the two kinds are
# deliberately worded differently because they are different findings:
#
#   FY2022 / FY2023 - "Not available today". The bank DID publish for these
#     years; its own FY2024 Annual Report says the annual Pillar 3 document was
#     reviewed by the Board in March 2024, which is the FY2023 edition. The
#     documents have rotted off www.kingdom.bank (the FY2022 URL returns a hard
#     404; the FY2023 edition was never archived). That is a limit on our reach
#     and must NEVER be recorded as a non-publication.
#
#   FY2024 / FY2025 - "Not published". The bank states in its own words that no
#     further Pillar 3 is required, and FY2025 is additionally covered by the
#     dated SDDT modification. These are genuine non-publications.
#
# THE WAIVER REACHES FY2025 ONLY, AND MUST NOT BE SPREAD BACKWARDS. BoE
# consolidated waivers register, FRN 400972 KINGDOM BANK LIMITED, matched on
# BOTH conjuncts - rule description 'SDDT Regime - General Application' AND
# sub-rule 'Ru 3.1' (the description alone also covers eligibility-criteria
# rules such as 'Ru 1.2 & 2.1(9)' and 'Ru 3.2', which remove no disclosure duty
# at all) - waiver ref A00009930P, START DATE 20/02/2025, no end date. Kingdom's
# accounting reference date is 31 December, so only FY2025's year-end falls
# after that date. FY2022, FY2023 and FY2024 are NOT excused by it. Closing all
# four on the waiver would be a false negative dressed up as a regulatory fact.
KINGDOM_P3_STATUS = {
    "FY2025": "Not published - SDDT Rule 3.1 opt-in from 20/02/2025",
    "FY2024": "Not published - Bank states none required after FY2023",
    "FY2023": "Not available today - published, no copy retrievable",
    "FY2022": "Not available today - published, no copy retrievable",
}

km1_rows = [
    ("DATA", "Pillar 3 edition status for this year (see source note - 'not available' and "
             "'not published' are different findings and are not interchangeable)", KINGDOM_P3_STATUS),
    ("SECTION", "Available own funds (£'000)", {}),
    ("DATA", "1    Common Equity Tier 1 (CET1) capital (£'000)", {"FY2021": 6892, "FY2020": 6594}),
    ("DATA", "2    Tier 1 capital (£'000)", {"FY2021": 6892, "FY2020": 6594}),
    ("DATA", "3    Total capital (£'000)", {"FY2021": 7653, "FY2020": 7448}),
    ("SECTION", "Risk-weighted exposure amounts (£'000)", {}),
    ("DATA", "4    Total risk-weighted exposure amount (£'000)", {"FY2021": 40617, "FY2020": 39632}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "5    Common Equity Tier 1 ratio (%)", {"FY2021": "16.97%", "FY2020": "16.64%"}),
    ("DATA", "6    Tier 1 ratio (%)", {"FY2021": "16.97%", "FY2020": "16.64%"}),
    ("DATA", "7    Total capital ratio (%)", {"FY2021": "18.84%", "FY2020": "18.79%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "UK 7a    Additional CET1 SREP requirements (%)", {"FY2021": "2.50%", "FY2020": "2.22%"}),
    ("DATA", "UK 7b    Additional AT1 SREP requirements (%)", {"FY2021": "0.84%", "FY2020": "0.78%"}),
    ("DATA", "UK 7c    Additional T2 SREP requirements (%)", {"FY2021": "1.11%", "FY2020": "1.00%"}),
    ("DATA", "UK 7d    Total SREP own funds requirements (%)", {"FY2021": "12.45%", "FY2020": "12.00%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "8    Capital conservation buffer (%)", {"FY2021": "2.50%", "FY2020": "2.50%"}),
    ("DATA", "UK 8a    Conservation buffer due to macro-prudential or systemic risk identified at the level of a "
             "Member State (%)", {"FY2021": "0.56%", "FY2020": "0.56%"}),
    # All four are printed '-' by the Bank in BOTH columns of the FY2021
    # edition - re-read off that PDF on 2026-09-18, where UK 8a immediately
    # above prints a real 0.56 in both columns. The dash is the Bank saying the
    # buffer does not apply to it; it is not a blank and it is not a zero.
    ("DATA", "9    Institution specific countercyclical capital buffer (%)", {"FY2021": "-", "FY2020": "-"}),
    ("DATA", "UK 9a    Systemic risk buffer (%)", {"FY2021": "-", "FY2020": "-"}),
    ("DATA", "10    Global Systemically Important Institution buffer (%)", {"FY2021": "-", "FY2020": "-"}),
    ("DATA", "UK 10a    Other Systemically Important Institution buffer (%)", {"FY2021": "-", "FY2020": "-"}),
    ("DATA", "11    Combined buffer requirement (%)", {"FY2021": "3.06%", "FY2020": "3.06%"}),
    ("DATA", "UK 11a    Overall capital requirements (%)", {"FY2021": "15.51%", "FY2020": "15.06%"}),
    ("DATA", "12    CET1 available after meeting the total SREP own funds requirements (%)",
     {"FY2021": "4.52%", "FY2020": "4.64%"}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "13    Total exposure measure excluding claims on central banks (£'000)",
     {"FY2021": 66250, "FY2020": 63697}),
    ("DATA", "14    Leverage ratio excluding claims on central banks (%)",
     {"FY2021": "10.40%", "FY2020": "10.35%"}),
    ("SECTION", "Liquidity Coverage Ratio — average based on end-of-the-month observations over the preceding 12 "
                "months, for each year shown (printed by the Bank as a separate table below the capital table)", {}),
    ("DATA", "15    Total high-quality liquid assets (HQLA) (Weighted value-average) (£'000)",
     {"FY2021": 8840, "FY2020": 6580}),
    ("DATA", "UK 16a    Cash outflows - Total weighted value (£'000)", {"FY2021": 2558, "FY2020": 2637}),
    ("DATA", "UK 16b    Cash inflows - Total weighted value (£'000)", {"FY2021": 8241, "FY2020": 7799}),
    ("DATA", "16    Total net cash outflows (adjusted value) (£'000)", {"FY2021": 640, "FY2020": 659}),
    ("DATA", "17    Liquidity coverage ratio (%)", {"FY2021": "1,382.23%", "FY2020": "998.00%"}),
    ("SECTION", "Net Stable Funding Ratio — average based on end-of-the-quarter observations over the preceding "
                "four quarters, for each year shown; the Bank footnotes the whole block '*based on estimated "
                "data (first NSFR return submitted to the PRA for reference point 31 March 2022 under CRR II)'", {}),
    ("DATA", "18    Total available stable funding (£'000)", {"FY2021": 68868, "FY2020": 60757}),
    ("DATA", "19    Total required stable funding (£'000)", {"FY2021": 42862, "FY2020": 40085}),
    ("DATA", "20    NSFR ratio (%)", {"FY2021": "160.67%", "FY2020": "151.57%"}),
]

KM1_SOURCES = (
    "Sources - Kingdom Bank Limited's own Pillar 3 Disclosures, 'Template UK KM1 - Key metrics template', "
    "£'000 and % exactly as printed:\n"
    f"FY2021: Pillar 3 Disclosures 2021 (approved 9 June 2022), section 4 'Key metrics', printed p.14 for the "
    f"capital table and p.15 for the liquidity and NSFR tables, column '31 December 2021'. Original URL "
    f"{P3_FY2021_DEAD_URL} now returns a hard HTTP 404; read from the Wayback capture {P3_FY2021_URL}, "
    f"confirmed to begin with the %PDF magic bytes.\n"
    f"FY2020: the '31 December 2020' COMPARATIVE column of that same FY2021 edition - see the provenance note "
    f"below, which explains why this column is not from its own edition.\n\n"
    "WHY FY2020 COMES FROM THE FY2021 EDITION'S COMPARATIVE (map rule 28, decided by the project owner "
    "2026-09-17). The FY2020 edition exists and was read in full (Pillar 3 Disclosures approved 3 June 2021, "
    f"{P3_FY2020_URL}), and it contains NO key-metrics table of any kind. Its own contents page lists eight "
    "sections - 1 Introduction, 1.1 COVID-19, 2 Risk management objectives and policies, 3 Board and "
    "committee structure, 4 Own funds, 5 Exposure amounts under the standardised approach, 6 Credit risk and "
    "provisioning, 7 Remuneration policies and practices, 8 Conclusion - and there is no key-metrics section "
    "among them. Its section 4 'Own funds' is a capital build-up table (permanent share capital, profit and "
    "loss account, revaluation reserve, deductions, Tier 2), which is a CC1-style disclosure and not this "
    "template. The FY2021 edition is the first to add a 'Key metrics' section, and it is that edition which "
    "introduced the template to this bank. Because the whole table is missing from FY2020's own edition "
    "rather than a row being dashed inside a table that exists, this is map rule 28 and not map rule 20, and "
    "the column is FILLED from the later edition's comparative and labelled as such here.\n\n"
    "VERIFIED THE WAY THE MAP REQUIRES, not by a keyword count. The absence above was established by reading "
    "the FY2020 edition's own table of contents and its section 4, then confirming with whole-word searches "
    "whose every hit was inspected individually: 'KM1' returns zero hits in that edition, 'combined buffer' "
    "zero, 'total exposure measure' zero, and the single 'key metrics' hit is a sentence in the introduction "
    "about the disclosure regime for small and non-complex firms, not a table heading. The same is true of "
    "the FY2019 edition.\n\n"
    "WHY EVERY OTHER COLUMN IS BLANK - two different reasons, and neither is 'the bank does not publish "
    "Pillar 3':\n"
    "• FY2019 AND EARLIER: no comparative exists anywhere. The FY2019 edition (approved 14 May 2020) has the "
    "same eight-section structure as FY2020 and no key-metrics table, and the FY2020 edition, which would be "
    "the only place a 31 December 2019 comparative could appear, has no such table to carry one. So map rule "
    "28(c) applies and the column stays empty. This is also the expected shape: the UK KM1 template arrived "
    "with the Disclosure (CRR) Part of the PRA Rulebook and genuinely post-dates those editions (map rule "
    "25).\n"
    "• FY2022 ONWARD: the editions are NOT OBTAINABLE, which is a statement about our reach and not about the "
    "bank (map rule 9). Kingdom Bank DID publish a Pillar 3 document for FY2022 and for FY2023 - the FY2024 "
    "Annual Report confirms the FY2023 one was reviewed by the Board in March 2024 - but the whole series has "
    "rotted off www.kingdom.bank. Re-checked 2026-09-17: the FY2022 URL "
    f"({P3_FY2022_DEAD_URL}) returns a hard HTTP 404 with an HTML body, and the single Wayback capture of it "
    "is not the PDF but a 1,489-byte WAF interstitial reading 'One moment, please... Please wait while your "
    "request is being verified', served with HTTP 200. The FY2023 edition was never archived at all. NOTHING "
    "HERE LICENSES AN INFERENCE THAT THE ROWS WERE NOT PUBLISHED; they are simply out of reach, and a future "
    "session that obtains either document should fill these columns.\n"
    "• A NOTE ON SDDT, so it is not misapplied to those blanks. Kingdom Bank holds the Small Domestic Deposit "
    "Taker opt-in that removes the Pillar 3 disclosure duty: the Bank of England consolidated waivers "
    "register carries one row for FRN 400972, 'Modification by Consent - PRA Rulebook - CRR Firms - Rule 3.1 "
    "of the SDDT Regime - General Application Part', sub rule 'Ru 3.1', waiver reference A00009930P.pdf, "
    f"START DATE 20/02/2025, no end date ({PRA_WAIVERS_URL}). Date-fitted against this bank's 31 December "
    "accounting reference date, that start date falls AFTER the FY2022, FY2023 and FY2024 year-ends, so the "
    "waiver explains NONE of those three blanks - they are link rot, as described above. It is capable of "
    "explaining a genuine absence from FY2025 onward, but the exemption permits a firm to stop disclosing "
    "rather than compelling it to, so an FY2025 absence should still be investigated on its own facts.\n\n"
    "LATEST-EDITION CHECK (required by the KM1 map), performed 2026-09-17 against the bank's OWN website. "
    "www.kingdom.bank serves no Pillar 3 document today and has no regulatory-disclosures page: the site's own "
    "sitemap index (wp-sitemap.xml) lists seven section sitemaps, and the page sitemap enumerates twenty "
    "pages - home, privacy, complaints, fraud awareness, cookies, useful documents, the About and product "
    "sections, terms - with no Pillar 3, results or investor page among them. The 'Useful documents' page, "
    "the only document library on the site, carries seventeen PDFs and all of them are customer forms "
    "(deposit slips, change of address, ISA transfer authority, mandates, savings conditions). A Wayback "
    "CDX sweep of the whole kingdom.bank domain returns one Pillar 3 page capture, from 2017. So the newest "
    "KM1-bearing edition obtainable anywhere remains the FY2021 one used above. The bank's registered domain "
    "www.kingdombank.co.uk is an unrelated parked domain and is not this bank.\n\n"
    "DASHES ARE REPRODUCED AS BLANKS, NOT ZEROS (map rule 2). Rows 9, UK 9a, 10 and UK 10a are printed '-' in "
    "both columns of the FY2021 edition - the Bank had no countercyclical, systemic risk, G-SII or O-SII "
    "buffer requirement - and a dash is left blank here rather than recorded as a zero. The rows themselves "
    "are kept so a reader can see the Bank printed them and what it printed in them.\n\n"
    "PRECISION IS THE BANK'S OWN. Kingdom prints its ratios to two decimal places throughout, including an "
    "LCR of 1,382.23% and an NSFR of 160.67%. Those very large liquidity ratios are genuine for a bank of "
    "this size and shape - total net cash outflows of £640k against £8,840k of high-quality liquid assets - "
    "and are reproduced as printed rather than rounded.\n\n"
    "A SOURCE CAVEAT THE BANK ITSELF FLAGS (map rule 7). The NSFR block carries the Bank's own footnote: "
    "'*based on estimated data (first NSFR return submitted to the PRA for reference point 31 March 2022 "
    "under CRR II)'. Both NSFR columns above are therefore the Bank's own estimate rather than a submitted "
    "regulatory return, which is a basis qualification carried here rather than dropped.\n\n"
    "TWO SERIES, NEVER MERGED - see also the individual Pillar 3 metric sheets in this workbook. This "
    "workbook's metric sheets carry BOTH a Pillar 3-basis row and an Annual Report KPI-table row for CET1 "
    "Ratio, Leverage Ratio and LCR, because the two disagree on basis (regulatory own funds excluding "
    "unapproved profits against accounting shareholders' funds; leverage excluding against including central "
    "bank claims; a 12-month average LCR against the Annual Report's own measure). Every figure on THIS sheet "
    "is the Pillar 3 series, and it ties to those sheets' Pillar 3 rows exactly: CET1 £6,892k/£6,594k, CET1 "
    "ratio 16.97%/16.64%, total RWEA £40,617k/£39,632k and leverage 10.40%/10.35%.\n\n"
    + ENTITY_NOTE
)

bw.add_km1_sheet(
    title="Kingdom Bank Limited — KM1 Key Metrics",
    subtitle="The Bank's own published 'Template UK KM1 - Key metrics template', reproduced whole in its own "
             "row order, row numbers, labels and printed precision. Bank/solo basis. Amounts in £'000, ratios "
             "as printed. Only FY2021 and FY2020 carry figures: FY2021 from its own edition, FY2020 from that "
             "edition's comparative column because the FY2020 edition prints no key-metrics table at all. "
             "Earlier years have no comparative anywhere and pre-date the template. FY2022-FY2025 now carry a "
             "STATED status rather than a blank, and the four are NOT one finding: FY2022 and FY2023 were "
             "published by the Bank and are simply not obtainable today (link rot), whereas FY2024 and FY2025 "
             "were not published at all - the Bank says so in its own words and FY2025 is additionally covered "
             "by the dated SDDT Rule 3.1 modification. Do not read the waiver back onto FY2022-FY2024. Rows "
             "9, UK 9a, 10 and UK 10a are printed as dashes by the Bank and are left blank, not zero. See the "
             "source note.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=88,
    source_height=560,
    years=PILLAR3_YEARS,
)

CET1_VALUES = {
    "FY2025": 15808, "FY2024": 15512, "FY2023": 9876, "FY2022": 9353, "FY2021": 7451,
    "FY2020": 6771, "FY2019": 6145, "FY2018": 5908, "FY2017": 5778, "FY2016": 5667, "FY2015": 5631, "FY2014": 4960,
}
TIER2_VALUES = {
    "FY2025": 700, "FY2024": 700, "FY2023": 700, "FY2022": 700, "FY2021": 761,
    "FY2020": 1431, "FY2019": 1431, "FY2018": 1431, "FY2017": 1581, "FY2016": 1581, "FY2015": 1681, "FY2014": 1681,
}
TOTAL_CAPITAL_VALUES = {y: CET1_VALUES[y] + TIER2_VALUES[y] for y in YEARS if y in CET1_VALUES and y in TIER2_VALUES}

# ---------------------------------------------------------------
# Regulatory-basis capital, straight off the recovered Pillar 3
# documents. These are NOT the same numbers as the accounting
# shareholders'-funds rows above and must never be merged with them:
# regulatory CET1 excludes the year's audited profits where those were
# not approved before the Pillar 3 document was signed, and deducts
# intangible assets and DTAs relying on future profits.
#
# FY2019's own Pillar 3 document is denominated in £m to one decimal
# place (the FY2020 and FY2021 editions moved to £'000). Its figures are
# carried here converted to £'000 at the precision the document itself
# states - so 5,700 means "£5.7m as printed", not £5,700k measured to
# the nearest £1k. The row labels say so.
# ---------------------------------------------------------------
P3_CET1_VALUES = {"FY2021": 6892, "FY2020": 6594}          # UK KM1 row 1 / FY2020 own funds table
P3_CET1_VALUES_FY2019_M = {"FY2019": 5700}                  # "Tier 1 Capital after deductions £5.7m"
P3_TIER2_VALUES = {"FY2020": 854}                           # FY2020 own funds table
P3_TIER2_VALUES_FY2019_M = {"FY2019": 1000}                 # "Tier 2 Capital (no deductions) £1.0m"
P3_TOTAL_CAPITAL_VALUES = {"FY2021": 7653, "FY2020": 7448}  # UK KM1 row 3 / FY2020 own funds table
P3_TOTAL_CAPITAL_VALUES_FY2019_M = {"FY2019": 6700}         # "Total Capital after deductions £6.7m"
P3_CET1_BEFORE_DEDUCTIONS = {"FY2020": 6759}
P3_DEDUCTIONS = {"FY2020": -165}

P3_CET1_RATIO_VALUES = {"FY2021": "16.97%", "FY2020": "16.64%"}   # UK KM1 rows 5/6
P3_TOTAL_CAPITAL_RATIO_VALUES = {"FY2021": "18.84%", "FY2020": "18.79%"}  # UK KM1 row 7
P3_TOTAL_RWA_VALUES = {"FY2021": 40617, "FY2020": 39632}          # UK KM1 row 4 / UK OV1 row 29

# GA-006 (2026-09-18): a THIRD source set, found by reading the Annual Reports
# to the end rather than stopping at the Strategic Report's KPI table. Note 29
# "Financial instruments", sub-note (j) "Capital management", prints a
# shareholders'-funds-to-regulatory-capital reconciliation ending in "Total
# Risk Exposure amount (unaudited)" and a three-line capital-ratio block. The
# earlier finding recorded on these two sheets - that the Annual Report "has
# never carried" a Total Capital ratio or a Total RWAs figure - was true of
# the KPI TABLE and false of the Annual Report, which is where the four
# FY2022-FY2025 gaps were sitting the whole time. Each year is taken from its
# OWN edition (map rule 1); every adjacent edition's comparative agrees
# exactly, which is recorded on the sheets as a control.
AR_TOTAL_RWA_VALUES = {"FY2025": 82630, "FY2024": 68191, "FY2023": 53182, "FY2022": 43648}
AR_TOTAL_CAPITAL_RATIO_VALUES = {
    "FY2025": "18.96%", "FY2024": "22.70%", "FY2023": "18.16%", "FY2022": "22.12%",
}
P3_LEVERAGE_EXPOSURE_VALUES = {"FY2021": 66250, "FY2020": 63697}  # UK KM1 row 13
P3_LEVERAGE_RATIO_EXCL_CB = {"FY2021": "10.40%", "FY2020": "10.35%"}  # UK KM1 row 14

# UK KM1 liquidity rows: "Average based on end-of-the-month observations
# over the preceding 12 months, for each year shown" - a genuine 12-month
# average, stated as such in the template's own row caption, and a
# different series from the Annual Report KPI table's LCR.
P3_LCR_HQLA = {"FY2021": 8840, "FY2020": 6580}
P3_LCR_OUTFLOWS = {"FY2021": 2558, "FY2020": 2637}
P3_LCR_INFLOWS = {"FY2021": 8241, "FY2020": 7799}
P3_LCR_NET_OUTFLOWS = {"FY2021": 640, "FY2020": 659}
P3_LCR_RATIO = {"FY2021": "1,382.23%", "FY2020": "998.00%"}

# UK KM1 NSFR rows: "Average based on end-of-the-quarter observations
# over the preceding four quarters, for each year shown", footnoted in
# the document itself as "*based on estimated data (first NSFR return
# submitted to the PRA for reference point 31 March 2022 under CRR II)".
P3_NSFR_ASF = {"FY2021": 68868, "FY2020": 60757}
P3_NSFR_RSF = {"FY2021": 42862, "FY2020": 40085}
P3_NSFR_RATIO = {"FY2021": "160.67%", "FY2020": "151.57%"}

CET1_RATIO_VALUES = {
    "FY2025": "18.8%", "FY2024": "22.2%", "FY2023": "17.37%", "FY2022": "20.84%", "FY2021": "16.97%",
    "FY2020": "17.13%", "FY2019": "15.27%", "FY2018": "14.57%", "FY2017": "14.41%", "FY2016": "16.25%", "FY2015": "14.45%",
}
LEVERAGE_RATIO_VALUES = {
    "FY2025": "12.4%", "FY2024": "10.8%", "FY2023": "7.96%", "FY2022": "10.02%", "FY2021": "9.03%",
    "FY2020": "9.37%", "FY2019": "9.40%", "FY2018": "10.10%", "FY2017": "9.38%", "FY2016": "10.09%", "FY2015": "8.96%",
}
LCR_VALUES = {
    "FY2025": "332.1%", "FY2024": "429.0%", "FY2023": "766.7%", "FY2022": "681.04%", "FY2021": "1,475.9%",
    "FY2020": "1,304.6%", "FY2019": "861.0%", "FY2018": "556.3%", "FY2017": "520.3%", "FY2016": "648.1%", "FY2015": "900.9%",
}

KPI_NOT_YET_INTRODUCED_NOTE = (
    "FY2014 predates this KPI table: the FY2014 Annual Report's Strategic Report 'Capital' section is "
    "narrative-only (£m totals for shareholders' funds and subordinated deposits, no ratio) - the Bank "
    "first began disclosing a CET1/Leverage/LCR KPI table from FY2015 onward (see the FY2016 Annual "
    "Report, which is this metric's earliest-available source, showing both FY2016 and FY2015). This is a "
    "genuine 'not yet introduced' gap, not a sourcing failure."
)

TWO_SERIES_NOTE = (
    "TWO DIFFERENT SERIES ARE SHOWN ABOVE AND MUST NOT BE MERGED. The 'per Annual Report KPI table' row "
    "is the bank's own Strategic Report key-performance-indicator figure, available for FY2015-FY2025. "
    "The 'per Pillar 3' row is the regulatory figure from Kingdom Bank's own annual Pillar 3 disclosure "
    "document, available only for the years those recovered documents cover. Where both exist they "
    "disagree, and this workbook's validation gate requires that they be carried on separate labelled "
    "rows rather than one overwriting the other. "
)

metric(
    "CET1 Capital", "£'000",
    [
        ("Shareholders' funds (Core Equity Tier 1) - per Annual Report balance sheet", CET1_VALUES),
        ("CET1 capital, regulatory - per Pillar 3 (UK KM1 row 1 / Own funds table)", P3_CET1_VALUES),
        ("CET1 capital, regulatory - per Pillar 3 FY2019 edition, which states £m to 1 d.p. (£5.7m)",
         P3_CET1_VALUES_FY2019_M),
        ("Of which: Core Tier 1 capital before deductions - per Pillar 3", P3_CET1_BEFORE_DEDUCTIONS),
        ("Of which: deductions (intangible assets, DTAs relying on future profits) - per Pillar 3",
         P3_DEDUCTIONS),
    ],
    note=TWO_SERIES_NOTE
    + "Regulatory CET1 is materially LOWER than shareholders' funds in every overlapping year (FY2021 "
      "£6,892k vs £7,451k; FY2020 £6,594k vs £6,771k) for two reasons the documents state themselves: the "
      "profit and loss account component excludes the year's audited profits where those were not approved "
      "until after the disclosure was signed (the FY2020 edition footnotes this explicitly - 'The profit "
      "and loss account figure excludes audited profits for 2020, which were not approved until 16 April "
      "2021'), and intangible assets and deferred tax assets relying on future profits are deducted "
      "(£165k in FY2020). Neither figure is wrong; they are different measures.",
)

metric(
    "CET1 Ratio", "%",
    [
        ("CET1 ratio - per Annual Report KPI table", CET1_RATIO_VALUES),
        ("CET1 ratio - per Pillar 3 (Template UK KM1 row 5)", P3_CET1_RATIO_VALUES),
    ],
    note=TWO_SERIES_NOTE
    + "FY2021 agrees to the basis point (16.97% on both), which is a useful control. FY2020 does NOT: the "
      "Annual Report KPI table gives 17.13% while the Pillar 3 Disclosures 2021 comparative column gives "
      "16.64%, a 49bp gap consistent with the regulatory CET1 base being £6,594k against shareholders' "
      "funds of £6,771k. Both are shown; neither is overwritten. "
    + KPI_NOT_YET_INTRODUCED_NOTE,
)

metric(
    "Tier 1 Capital", "£'000",
    [
        ("Shareholders' funds (Core Equity Tier 1) - per Annual Report balance sheet", CET1_VALUES),
        ("Tier 1 capital after deductions - per Pillar 3 (UK KM1 row 2 / Own funds table)", P3_CET1_VALUES),
        ("Tier 1 capital after deductions - per Pillar 3 FY2019 edition, which states £m to 1 d.p. (£5.7m)",
         P3_CET1_VALUES_FY2019_M),
    ],
    note=TIER1_NOTE + " The recovered Pillar 3 documents confirm this directly: the FY2020 and FY2019 "
         "editions' own funds tables show a Tier 1 section containing only permanent share capital, the "
         "profit and loss account and the revaluation reserve, and Template UK KM1 in the FY2021 edition "
         "prints an identical value on row 1 (CET1 capital) and row 2 (Tier 1 capital) for both FY2021 "
         "(£6,892k) and FY2020 (£6,594k). " + TWO_SERIES_NOTE,
)

metric(
    "Tier 1 Ratio", "%",
    [
        ("Tier 1 ratio (= CET1 ratio - see note) - per Annual Report KPI table", CET1_RATIO_VALUES),
        ("Tier 1 ratio - per Pillar 3 (Template UK KM1 row 6)", P3_CET1_RATIO_VALUES),
    ],
    note=TIER1_RATIO_NOTE + " Template UK KM1 in the FY2021 Pillar 3 edition prints the same value on "
         "row 5 (CET1 ratio) and row 6 (Tier 1 ratio) for both years shown, confirming this directly "
         "rather than by inference. " + TWO_SERIES_NOTE + KPI_NOT_YET_INTRODUCED_NOTE,
)

metric(
    "Total Capital", "£'000",
    [
        ("Shareholders' funds (Core Equity Tier 1) - per Annual Report balance sheet", CET1_VALUES),
        ("Subordinated liabilities (Tier 2) - per Annual Report balance sheet", TIER2_VALUES),
        ("Total of the two Annual Report lines above (CET1 + Tier 2)", TOTAL_CAPITAL_VALUES),
        ("Tier 1 capital after deductions - per Pillar 3", P3_CET1_VALUES),
        ("Tier 2 capital instruments (subordinated debt), eligible - per Pillar 3", P3_TIER2_VALUES),
        ("Total own funds after deductions - per Pillar 3 (UK KM1 row 3 / Own funds table)",
         P3_TOTAL_CAPITAL_VALUES),
        ("Total own funds after deductions - per Pillar 3 FY2019 edition, which states £m to 1 d.p. "
         "(Tier 1 £5.7m + Tier 2 £1.0m = £6.7m)", P3_TOTAL_CAPITAL_VALUES_FY2019_M),
    ],
    note=TWO_SERIES_NOTE
    + "The Tier 2 rows diverge sharply and deliberately: the balance sheet carries subordinated "
      "liabilities at their full nominal amount (£1,431k in FY2020), whereas only £854k of that was "
      "eligible as regulatory Tier 2 capital in FY2020 - regulatory eligibility of dated subordinated "
      "debt amortises over its final five years. The FY2021 Pillar 3 edition uses Template UK KM1, which "
      "prints total capital (£7,653k) and Tier 1 (£6,892k) but no separate Tier 2 line, so no FY2021 "
      "Pillar 3 Tier 2 figure is shown here - it is deliberately NOT back-solved from the other two.",
)

metric(
    "Total Capital Ratio", "%",
    [
        ("Total capital ratio - per Annual Report note 29(j) Capital management",
         AR_TOTAL_CAPITAL_RATIO_VALUES),
        ("Total capital ratio - per Pillar 3 (Template UK KM1 row 7)", P3_TOTAL_CAPITAL_RATIO_VALUES),
    ],
    note="CORRECTED 2026-09-18 (GA-006). This sheet previously said the Annual Report 'has never carried a "
         "Total Capital ratio in any year' and left FY2022-FY2025 blank. That was true of the Strategic "
         "Report's KPI table, which is where the other sheets' Annual Report series comes from, and false "
         "of the Annual Report itself: note 29 'Financial instruments', sub-note (j) 'Capital management', "
         "prints the ratio every year. FY2022-FY2025 are now filled from each year's OWN edition.\n\n"
         "THE TWO SERIES ARE ON DIFFERENT BASES AND ARE NOT MERGED. At FY2021, the one year both sources "
         "cover, they DISAGREE: the Pillar 3 UK KM1 gives 18.84% and the Annual Report note 29(j) gives "
         "17.93%. The cause is the numerator, not the denominator - both put total risk exposure at "
         "40,617, but Pillar 3 total capital is 7,653 against the Annual Report's 7,283, the Annual Report "
         "excluding current-year profits until the audit completes (its own reconciliation carries an "
         "explicit 'Less: current year profits (included after audit is completed)' line). 7,653/40,617 = "
         "18.84% and 7,283/40,617 = 17.93%, so each ratio is internally consistent with its own source. "
         "Neither overwrites the other.\n\n"
         "CONTROL: every adjacent edition's comparative agrees exactly with the own-edition figure used "
         "here - FY2022 22.12% appears in both the FY2022 and FY2023 editions, FY2023 18.16% in both the "
         "FY2023 and FY2024 editions, FY2024 22.70% in both the FY2024 and FY2025 editions.\n\n"
         + PARTIAL_DISCLOSURE_NOTE_P3_SERIES_ONLY,
)

metric(
    "Total RWAs", "£'000",
    [
        ("Total Risk Exposure amount - per Annual Report note 29(j) Capital management",
         AR_TOTAL_RWA_VALUES),
        ("Total risk-weighted exposure amount - per Pillar 3 (UK KM1 row 4 / UK OV1 row 29)",
         P3_TOTAL_RWA_VALUES),
    ],
    note="CORRECTED 2026-09-18 (GA-006). FY2022-FY2025 were blank here because this sheet looked only at "
         "the Strategic Report's KPI table, which indeed carries no RWA figure in any year. The Annual "
         "Report does: note 29 'Financial instruments', sub-note (j) 'Capital management', ends its "
         "regulatory-capital reconciliation with a 'Total Risk Exposure amount (unaudited)' line every "
         "year. Each of the four years is taken from its own edition.\n\n"
         "UNLIKE THE TOTAL CAPITAL RATIO SHEET, THE TWO SERIES HERE COINCIDE. At FY2021, the one year both "
         "sources cover, the Pillar 3 UK KM1 row 4 and the Annual Report note 29(j) both give 40,617 - the "
         "bases differ on regulatory own funds (see the Total Capital Ratio sheet) but not on the risk "
         "exposure denominator. The rows are still kept separate rather than run together, because a "
         "reader should be able to see which document each cell came from. 'Total Risk Exposure amount' is "
         "the bank's own caption and is the CRR term for the same quantity the Pillar 3 row calls total "
         "risk-weighted exposure amount.\n\n"
         "CONTROL: FY2022 43,648, FY2023 53,182 and FY2024 68,191 each appear identically in their own "
         "edition and in the following year's comparative column.\n\n"
         "On the Pillar 3 series: the "
         "FY2020 and FY2019 Pillar 3 editions predate the UK OV1 template and disclose only a credit-risk "
         "risk-weighted exposure subtotal plus a separate operational-risk capital requirement, with no "
         "total risk-weighted exposure amount stated anywhere - so no FY2019 total is shown here, and the "
         "FY2020 total above is taken from the FY2021 edition's UK OV1 comparative column (where it IS "
         "stated directly) rather than being summed or back-solved. See the RWA Breakdown sheet for the "
         "components. " + PARTIAL_DISCLOSURE_NOTE_P3_SERIES_ONLY,
)

# RWA Breakdown - placed immediately after Total RWAs, before Leverage
# Ratio, per the locked sheet order. Populated 2026-09-15 from the
# recovered Pillar 3 Disclosures 2021 (Template UK OV1 and the
# credit-risk-by-exposure-class table beneath it).
rwa_rows = [
    ("DATA", "Pillar 3 edition status for this year (see source note - 'not available' and "
             "'not published' are different findings and are not interchangeable)", KINGDOM_P3_STATUS),
    ("SECTION", "Template UK OV1 - Overview of risk weighted exposure amounts", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2021": 36472, "FY2020": 35487}),
    ("DATA", "Of which: the standardised approach", {"FY2021": 36472, "FY2020": 35487}),
    ("DATA", "Operational risk", {"FY2021": 4145, "FY2020": 4145}),
    ("DATA", "Of which: basic indicator approach", {"FY2021": 4145, "FY2020": 4145}),
    ("DATA", "Amounts below the thresholds for deduction (subject to 250% risk weight) - disclosed by the "
             "template 'For information' only and NOT included in the total below", {"FY2021": 214, "FY2020": 48}),
    ("TOTAL", "Total risk weighted exposure amount", {"FY2021": 40617, "FY2020": 39632}),
    ("SECTION", "Credit risk by standardised exposure class (FY2021 edition's own analysis)", {}),
    ("DATA", "Central governments or central banks", {"FY2021": 0}),
    ("DATA", "Institutions", {"FY2021": 1715}),
    ("DATA", "Retail", {"FY2021": 53}),
    ("DATA", "Secured by mortgages on immovable property", {"FY2021": 33472}),
    ("DATA", "Exposures in default", {"FY2021": 67}),
    ("DATA", "Claims on institutions and corporates with a short-term credit assessment", {"FY2021": 444}),
    ("DATA", "Other items", {"FY2021": 721}),
    ("TOTAL", "SA exposure classes excluding securitisation positions", {"FY2021": 36472}),
    ("SECTION", "Credit risk by CRR Article 112 exposure category (FY2020 and FY2019 editions' own, "
                "differently-structured analysis - see source note)", {}),
    ("DATA", "Exposures to central governments or central banks (Bank of England Reserve Account)",
     {"FY2020": 0, "FY2019": 0}),
    ("DATA", "Retail exposures (unsecured loans)", {"FY2020": 657, "FY2019": 200}),
    ("DATA", "Exposures secured by mortgages on immovable property (non-residential loans performing)",
     {"FY2020": 26073, "FY2019": 27200}),
    ("DATA", "Exposures secured by mortgages on immovable property (residential loans performing)",
     {"FY2020": 3937, "FY2019": 3300}),
    ("DATA", "Exposures in default (non-residential loans)", {"FY2020": 266, "FY2019": 300}),
    ("DATA", "Exposures in default (residential loans)", {"FY2020": 0, "FY2019": 0}),
    ("DATA", "Exposures in default (unsecured loans)", {"FY2020": 0, "FY2019": 0}),
    ("DATA", "Exposures to institutions", {"FY2020": 2827, "FY2019": 1100}),
    ("DATA", "Other items (fixed and other assets)", {"FY2020": 1728, "FY2019": 1900}),
    ("TOTAL", "Credit Risk - risk weighted exposure amounts", {"FY2020": 35488, "FY2019": 34000}),
    ("SECTION", "Own funds requirement (8% of the risk weighted exposure amounts above)", {}),
    ("DATA", "Credit risk - capital resources required", {"FY2021": 2917, "FY2020": 2839, "FY2019": 2700}),
    ("DATA", "Operational risk - capital resources required", {"FY2021": 332, "FY2020": 332, "FY2019": 300}),
    ("TOTAL", "Pillar 1 capital resources required", {"FY2021": 3249, "FY2020": 3171, "FY2019": 3000}),
]

RWA_BREAKDOWN_NOTE = (
    "THREE DIFFERENT DISCLOSURE STRUCTURES ARE SHOWN, one per Pillar 3 edition, deliberately NOT forced "
    "into a common template. The FY2021 edition uses the UK OV1 template and a seven-class standardised "
    "analysis; the FY2020 and FY2019 editions predate UK OV1 and instead tabulate CRR Article 112 "
    "exposure categories, splitting property lending into non-residential/residential and defaults into "
    "three sub-classes. The two structures are not comparable line for line.\n"
    "ONE £1k RECONCILING DIFFERENCE, documented rather than smoothed: the FY2020 edition's own credit "
    "risk RWEA subtotal is £35,488k, while the FY2021 edition's UK OV1 comparative column for the same "
    "date gives £35,487k. Both are shown above on their own rows, as this workbook's validation gate "
    "requires; neither has been adjusted to match the other.\n"
    "FY2019 ROWS ARE £m-PRECISION. The FY2019 Pillar 3 edition states every figure in £m to one decimal "
    "place. Its rows above are carried in £'000 at that precision - '34,000' means '£34.0m as printed', "
    "not a figure measured to the nearest £1k. Rows shown above as 0 are printed in the source as either "
    "'-' (central government/central bank exposures, which carry a 0% risk weight) or '0.0' (the "
    "residential and unsecured default classes) - genuinely nil or below the rounding floor, which is why "
    "they are 0 rather than blank.\n"
    "ONE TYPO IN THE FY2021 SOURCE, reproduced faithfully and flagged rather than silently corrected: the "
    "narrative above that edition's UK OV1 table reads 'The Bank's total Pillar 1 capital resources "
    "requirement ... amounted to £3,249k as at 31 December 2020', but £3,249k is the 31 December 2021 "
    "figure - the table's own column header, and the FY2020 edition's own £3,171k for 31 December 2020, "
    "both establish this. The £3,249k is therefore carried above in the FY2021 column.\n"
    "NO TOTAL RWA IS STATED IN THE FY2020 OR FY2019 EDITIONS - neither adds credit and operational risk "
    "into a single risk-weighted total, and nothing here does so on their behalf. The FY2020 total on the "
    "UK OV1 rows comes from the FY2021 edition's own comparative column.\n"
    "THE 250%-RISK-WEIGHT ROW IS INFORMATIONAL. Template UK OV1 marks it '(For information)' and the "
    "template's own total excludes it: 36,472 + 4,145 = 40,617 for FY2021 and 35,487 + 4,145 = 39,632 "
    "for FY2020, in both cases without the 214/48. It is reproduced above on that basis.\n\n"
    + PARTIAL_DISCLOSURE_NOTE
)

bw.add_rwa_breakdown_sheet(
    title="Kingdom Bank Limited — RWA Breakdown",
    subtitle="Risk weighted exposure amounts, Bank/solo basis, £'000. Disclosed FY2019-FY2021 only, in three "
             "different structures - see source note at bottom.",
    rows=rwa_rows,
    sources_text=p3_sources() + "\n\n" + RWA_BREAKDOWN_NOTE,
    first_col_width=76,
    source_height=460,
    years=PILLAR3_YEARS,
)

metric(
    "Leverage Ratio", "%",
    [
        ("Leverage ratio - per Annual Report KPI table / Pillar 3 section 5.2 (total exposure measure)",
         LEVERAGE_RATIO_VALUES),
        ("Leverage ratio excluding claims on central banks - per Pillar 3 (Template UK KM1 row 14)",
         P3_LEVERAGE_RATIO_EXCL_CB),
        ("Total exposure measure excluding claims on central banks (£'000) - per Pillar 3 (UK KM1 row 13)",
         P3_LEVERAGE_EXPOSURE_VALUES),
    ],
    note="THE TWO RATIO ROWS ARE DIFFERENT MEASURES, not a discrepancy. Row 14 of Template UK KM1 "
         "excludes claims on central banks from the exposure measure, which for this bank means excluding "
         "its Bank of England Reserve Account - so it is structurally the higher of the two (FY2021 "
         "10.40% vs 9.03%; FY2020 10.35% vs 9.37%). The first row's FY2020, FY2019 and FY2018 values are "
         "independently confirmed by the recovered Pillar 3 documents themselves, which is a useful "
         "control on the Annual Report KPI series: the FY2020 edition's section 5.2 states 'The Bank's "
         "calculated leverage ratio at 31 December 2020 was 9.37% (2019: 9.40%)' and the FY2019 edition "
         "states '...at 31 December 2019 was 9.40% (2018: 10.10%)' - matching the KPI table exactly in "
         "all three years. " + KPI_NOT_YET_INTRODUCED_NOTE,
)

metric(
    "LCR", "%",
    [
        ("Liquidity Coverage Requirement (LCR) ratio - per Annual Report KPI table", LCR_VALUES),
        ("LCR, 12-month average of end-of-month observations - per Pillar 3 (UK KM1 row 17)", P3_LCR_RATIO),
        ("Total high-quality liquid assets (HQLA), weighted value-average (£'000) - per Pillar 3 (row 15)",
         P3_LCR_HQLA),
        ("Cash outflows, total weighted value (£'000) - per Pillar 3 (row UK 16a)", P3_LCR_OUTFLOWS),
        ("Cash inflows, total weighted value (£'000) - per Pillar 3 (row UK 16b)", P3_LCR_INFLOWS),
        ("Total net cash outflows, adjusted value (£'000) - per Pillar 3 (row 16)", P3_LCR_NET_OUTFLOWS),
    ],
    note="TWO DIFFERENT LCR SERIES - never merge them. The Pillar 3 row is explicitly captioned in the "
         "template itself as an 'Average based on end-of-the-month observations over the preceding 12 "
         "months, for each year shown', and its components (HQLA, inflows, outflows) are shown above so "
         "the basis is checkable rather than asserted: 8,840 / 640 = 1,382% for FY2021 and 6,580 / 659 = "
         "998% for FY2020, both consistent with the printed ratio, which is what confirms this caption "
         "really does print an average rather than a year-end value. The Annual Report KPI series gives "
         "1,475.9% for FY2021 and 1,304.6% for FY2020 on its own, different measure. The gap is 94pp in "
         "FY2021 and 307pp in FY2020. " + TWO_SERIES_NOTE + KPI_NOT_YET_INTRODUCED_NOTE,
)

metric(
    "NSFR", "%",
    [
        ("NSFR ratio, 4-quarter average of end-of-quarter observations - per Pillar 3 (UK KM1 row 20)",
         dict(KINGDOM_P3_STATUS, **P3_NSFR_RATIO)),
        ("Total available stable funding (£'000) - per Pillar 3 (UK KM1 row 18)", P3_NSFR_ASF),
        ("Total required stable funding (£'000) - per Pillar 3 (UK KM1 row 19)", P3_NSFR_RSF),
    ],
    note="BOTH YEARS ARE THE BANK'S OWN ESTIMATES, and the document says so. The FY2021 Pillar 3 edition "
         "footnotes its NSFR block '*based on estimated data (first NSFR return submitted to the PRA for "
         "reference point 31 March 2022 under CRR II)'. That is consistent with the project-wide "
         "structural position on NSFR: the PRA requirement began 1 January 2022 (PS17/21), so a FY2021 or "
         "FY2020 NSFR is a voluntary pre-requirement estimate, not a regulatory return.\n\n"
         "FY2022-FY2025 CHECKED AND CONFIRMED ABSENT FROM THE ANNUAL REPORTS (GA-006, 2026-09-18). The "
         "FY2022-FY2025 blanks here are NOT the same kind of blank as the ones on the Total RWAs and Total "
         "Capital Ratio sheets, which were filled on this date from Annual Report note 29(j). That note "
         "carries capital only; the Annual Report discloses no NSFR anywhere. Searched whole-document on "
         "the text-native FY2024 and FY2025 editions for 'NSFR', 'net stable' and 'stable funding': zero "
         "hits each, against a richness control of 30 hits for 'liquidity' and 121/126 for 'capital' in "
         "the same extraction, so the zero is a fact about the documents and not about the search. The "
         "FY2023 edition is a scan and was checked the same way over its Strategic Report and KPI-table "
         "pages via OCR - again zero for all three terms, against 12 'liquidity' and 23 'ratio' hits. In "
         "every edition the only liquidity metric the bank publishes is the Liquidity Coverage "
         "Requirement ratio, which is why the LCR sheet has a continuous series and this one does not. "
         "These four years are therefore not a sourcing gap in the Annual Reports; they are a gap that "
         "only a Pillar 3 document could close, and the Pillar 3 position for those years is below.\n\n"
         + PARTIAL_DISCLOSURE_NOTE_P3_SERIES_ONLY,
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={"MREL Ratio": NOT_DISCLOSED_NOTE},
    years=PILLAR3_YEARS,
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {
            "FY2025": 160171, "FY2024": 138492, "FY2023": 113509, "FY2022": 89022, "FY2021": 75541,
            "FY2020": 69781, "FY2019": 59310, "FY2018": 53803, "FY2017": 56250, "FY2016": 51449, "FY2015": 49809, "FY2014": 49843,
        }),
        ("Loans and advances to customers", {
            "FY2025": 118242, "FY2024": 97733, "FY2023": 77532, "FY2022": 63291, "FY2021": 53795,
            "FY2020": 47114, "FY2019": 45339, "FY2018": 41404, "FY2017": 38438, "FY2016": 35336, "FY2015": 33028, "FY2014": 29724,
        }),
        ("Customer accounts", {
            "FY2025": 141758, "FY2024": 121269, "FY2023": 102091, "FY2022": 78452, "FY2021": 66668,
            "FY2020": 61287, "FY2019": 51378, "FY2018": 46112, "FY2017": 48656, "FY2016": 43885, "FY2015": 41906, "FY2014": 42935,
        }),
        ("Total shareholders' funds", {
            "FY2025": 15808, "FY2024": 15512, "FY2023": 9876, "FY2022": 9353, "FY2021": 7451,
            "FY2020": 6771, "FY2019": 6145, "FY2018": 5908, "FY2017": 5778, "FY2016": 5667, "FY2015": 5631, "FY2014": 4960,
        }),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total net income", {
            "FY2025": 6404, "FY2024": 5205, "FY2023": 4360, "FY2022": 3175, "FY2021": 2610,
            "FY2020": 2287, "FY2019": 2242, "FY2018": 2106, "FY2017": 1875, "FY2016": 1755, "FY2015": 1637, "FY2014": 1548,
        }),
        ("Administrative expenses", {
            "FY2025": -7241, "FY2024": -4776, "FY2023": -3597, "FY2022": -2953, "FY2021": -2437,
            "FY2020": -2167, "FY2019": -1780, "FY2018": -1776, "FY2017": -1538, "FY2016": -1554, "FY2015": -1487, "FY2014": -1413,
        }),
        ("(Loss)/profit for the financial year", {
            "FY2025": -804, "FY2024": 279, "FY2023": 523, "FY2022": 102, "FY2021": 680,
            "FY2020": -24, "FY2019": 257, "FY2018": 146, "FY2017": 105, "FY2016": 34, "FY2015": 720, "FY2014": 69,
        }),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening total shareholders' funds", {
            "FY2025": 15512, "FY2024": 9876, "FY2023": 9353, "FY2022": 7451, "FY2021": 6771,
            "FY2020": 6145, "FY2019": 5908, "FY2018": 5778, "FY2017": 5667, "FY2016": 5631, "FY2015": 4847, "FY2014": 4646,
        }),
        ("(Loss)/profit for the financial year", {
            "FY2025": -804, "FY2024": 279, "FY2023": 523, "FY2022": 102, "FY2021": 680,
            "FY2020": -24, "FY2019": 257, "FY2018": 146, "FY2017": 105, "FY2016": 34, "FY2015": 720, "FY2014": 69,
        }),
        ("Other equity movements, net", {
            "FY2025": 1100, "FY2024": 5357, "FY2023": 0, "FY2022": 1800, "FY2021": 0,
            "FY2020": 650, "FY2019": 0, "FY2018": -16, "FY2017": 6, "FY2016": 2, "FY2015": 64, "FY2014": 245,
        }),
        ("Closing total shareholders' funds", {
            "FY2025": 15808, "FY2024": 15512, "FY2023": 9876, "FY2022": 9353, "FY2021": 7451,
            "FY2020": 6771, "FY2019": 6145, "FY2018": 5908, "FY2017": 5778, "FY2016": 5667, "FY2015": 5631, "FY2014": 4960,
        }),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash flow from/(used in) operating activities", {
            "FY2025": -1134, "FY2024": -583, "FY2023": 10244, "FY2022": 3132, "FY2021": -630,
            "FY2020": 6970, "FY2019": 1938, "FY2018": -4121, "FY2017": 1102, "FY2016": 485, "FY2015": -5612,
        }),
        ("Net cash flow from/(used in) investing activities", {
            "FY2025": -43, "FY2024": -41, "FY2023": -47, "FY2022": -40, "FY2021": 1769,
            "FY2020": -69, "FY2019": -97, "FY2018": -52, "FY2017": -31, "FY2016": -191, "FY2015": 3325,
        }),
        ("Net cash flow from/(used in) financing activities", {
            "FY2025": 1100, "FY2024": 5357, "FY2023": 0, "FY2022": 1739, "FY2021": -670,
            "FY2020": 650, "FY2019": -20, "FY2018": -166, "FY2017": 0, "FY2016": -100, "FY2015": 0,
        }),
        ("Cash and cash equivalents at end of year", {
            "FY2025": 39714, "FY2024": 39791, "FY2023": 35058, "FY2022": 24861, "FY2021": 20030,
            "FY2020": 19561, "FY2019": 12010, "FY2018": 10189, "FY2017": 14528, "FY2016": 13457, "FY2015": 13263,
        }),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 ratio", CET1_RATIO_VALUES),
        ("Leverage ratio", LEVERAGE_RATIO_VALUES),
    ],
    note="The two ratios charted above are the Annual Report Strategic Report 'Key performance indicators' "
         "series, disclosed each year from FY2015 onward; FY2014 predates the KPI table and has no ratio "
         "data. LCR is disclosed on the same basis but omitted from the chart only because its scale, "
         "running into four figures in most years, dwarfs the other two - see the LCR sheet directly. "
         "SEPARATELY, and recovered on 2026-09-15, Kingdom Bank published standalone annual Pillar 3 "
         "disclosure documents for FY2019-FY2023; the FY2019, FY2020 and FY2021 editions have been "
         "retrieved (every one of the bank's own live URLs now 404s, so the citations point at Wayback "
         "`id_` snapshots with the dead originals kept alongside them) and supply regulatory-basis CET1, "
         "Tier 1 and Total Capital, a Total Capital ratio, Total RWAs, a full UK OV1 RWA breakdown, a "
         "leverage ratio excluding central bank claims, a 12-month-average LCR and an NSFR. Those "
         "regulatory figures do NOT agree with the KPI-table series above - they are computed on a "
         "different basis - so each affected sheet carries both on separate labelled rows, and the charts "
         "above deliberately continue to plot only the KPI series so that a single consistent measure is "
         "charted across all years. Only the MREL ratio remains undisclosed in every year. CET1 Capital, "
         "Tier 1 Capital and Total Capital (£'000) are disclosed on an accounting basis for all 12 years "
         "on their own sheets. Balance Sheet, Profit & Loss, Statement of Changes in Equity and Cash Flow "
         "figures are duplicated from their own sheets for at-a-glance trend viewing - how the bank is using "
         "its money (steady growth in loans and advances to churches/charities/individuals, funded by "
         "customer deposits) and the risk it is taking with it (a small, consistently sub-1%-of-gross-"
         "advances loan loss provision throughout). FY2014 has no cash flow figures (see the Cash Flow "
         "Statement sheet's source note).",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/KINGDOM BANK FINANCIALS.xlsx")
