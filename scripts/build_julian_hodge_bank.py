import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# PILLAR-3-ONLY WORKBOOK: Julian Hodge Bank Limited (company 00743437, FRN 204439)
# takes the FRS 101 cash-flow-statement disclosure exemption in every one of its FY2021-FY2025
# Annual Reports - explicitly stated each year in Note 1 (Basis of preparation): "the Bank has
# applied the exemptions available under FRS 101 in respect of the following disclosures: A Cash
# Flow Statement and related notes; ..." No Statement of Cash Flows exists in any year's accounts.
# Pillar 3 / capital disclosures are rich for FY2021-FY2023 (full UK KM1-format Key Regulatory
# Metrics tables, standalone Pillar 3 documents), but FY2024-FY2025 have no standalone Pillar 3
# document published - only a brief unaudited "Capital risk management" note inside each year's
# own Annual Report giving CET1/RWA/ratios (no Leverage/LCR/NSFR for those two years). Follows the
# BNY Mellon International / ABC International Bank precedent: standard 13-sheet structure, but
# the Cash Flow Statement sheet documents the exemption instead of line items, and the Overview
# sheet omits the cash-flow chart.

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016",
         "FY2015", "FY2014", "FY2013", "FY2012", "FY2011", "FY2010", "FY2009"]  # most recent first. FY2021-FY2025
# fiscal year-end 30 September; FY2020 is an 11-month transition PERIOD ended 30 September 2020 (the year the
# fiscal year-end changed from 31 October to 30 September - the Bank's own Annual Report 2020 explicitly covers
# "the 11-month period ended 30 September 2020" with its FY2019 comparative column covering the full prior year
# ended 31 October 2019); FY2009-FY2019 fiscal year-end is 31 October.
YEAR_LABEL = {y: y for y in YEARS}

# HD-074 (2026-09-07): Pillar 3 (all 11 metric sheets), Asset Quality, and RWA Breakdown stay out of scope for
# this statutory-statement-only extension - pin them to the original project-wide FY2014-FY2025 window via this
# override. FY2010-FY2013 is HD-004's confirmed real statutory floor for this entity; FY2009 is a bonus beyond
# that floor (found readily as a genuine comparative in the FY2010 Annual Report's own Balance Sheet/Profit and
# Loss Account - see HD074_NOTE below), not force-searched further per the ticket's "don't force it" guidance.
PILLAR3_YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016",
                 "FY2015", "FY2014"]

# HD-080 (2026-09-16): the FY2010-FY2013 Pillar 3 documents were located live (see PILLAR3_URL_NOTE), so the
# FY2014 floor above is no longer a sourcing boundary for the CAPITAL metric sheets - it is now a REGIME
# boundary. Those four editions are Basel II / BIPRU, so only the metric sheets carry them, via this third
# year axis. Asset Quality and RWA Breakdown deliberately stay on PILLAR3_YEARS: neither has any pre-FY2014
# content at all (no IFRS 9 staging existed, and no risk-weighted-asset figure is disclosed in any of the four
# editions), so extending them would add nothing but four empty columns. Project precedent for exactly this
# shape: build_aldermore.py's P3_DISCLOSURE_YEARS.
P3_DISCLOSURE_YEARS = PILLAR3_YEARS + ["FY2013", "FY2012", "FY2011", "FY2010"]

BASEL2_NOTE = (
    "PRE-CRD IV (BASEL II) COLUMNS FY2013-FY2010 - READ BEFORE USING THEM. CRD IV took effect 1 January 2014. "
    "The FY2013, FY2012, FY2011 and FY2010 Pillar 3 documents are Basel II / BIPRU disclosures and they do not "
    "report the same things under the same names. What each of the four actually prints, in its section 4 "
    "'Capital resources' table, is: Tier 1 capital (ordinary shares + profit and loss reserve), a deduction for "
    "investments in subsidiaries, 'Total Tier 1 capital', a Tier 2 line (eligible general provisions, less a "
    "revaluation reserve deduction in FY2013/FY2012/FY2011), and 'Total capital resources'. In its section 5.1 "
    "it prints a 'Pillar 1 capital requirement' by exposure class.\n"
    "WHAT IS DELIBERATELY NOT POPULATED, and why. (1) CET1: the concept did not exist before CRD IV and none of "
    "the four documents uses the term - a Basel II 'Total Tier 1 capital' is NOT a CET1 figure and is not "
    "placed on the CET1 sheet. (2) Tier 1 Capital: each edition's own Total Tier 1 capital is FY2013 113.7, "
    "FY2012 111.1, FY2011 109.7, FY2010 108.1 - recorded here in prose only and NOT as a data column, which is "
    "the treatment this script already applies to the FY2015/FY2014 Basel II Tier 1 figures, kept consistent "
    "rather than changed for the newly-added years. (3) EVERY RATIO SHEET: no risk-weighted-asset amount "
    "appears anywhere in any of the four documents (grep for 'risk weighted'/'risk-weighted' returns zero hits "
    "in all four), so there is no denominator, and none of the four prints a capital ratio of any kind. "
    "Grossing the Pillar 1 capital requirement up by 12.5 would manufacture an RWA no document states, and is "
    "deliberately not done. (4) Leverage / LCR / NSFR: none of the three existed as a UK disclosure "
    "requirement in these years. FY2013's document mentions a leverage ratio exactly once, as forward-looking "
    "prose about CRD IV's forthcoming requirements ('enhanced reporting requirements include the introduction "
    "of a leverage ratio, liquidity coverage...'), with no value; FY2012/FY2011/FY2010 do not mention it at "
    "all. In particular these years belong on NEITHER row of the Leverage Ratio sheet's excluding-/"
    "including-claims-on-central-banks pair - that is a 2022 UK framework distinction and reading it back onto "
    "a Basel II year would be meaningless.\n"
    "WHAT IS POPULATED: 'Total capital resources' only, on the Total Capital sheet - a figure each document "
    "states directly as a total. This matches how FY2015 (122.4) and FY2014 (118.8) were already handled on "
    "that sheet before this extension. The Pillar 1 capital requirement for the four new years is FY2013 35.3 "
    "(credit risk 34.9 + operational risk 0.4), FY2012 36.8 (36.0 + 0.8), FY2011 38.9 (37.7 + 1.2), FY2010 "
    "41.5 (40.2 + 1.3) - recorded in prose on the Total RWAs sheet, as CAPITAL, never converted to RWA."
)

AR2025_URL = "https://hodgebank.co.uk/wp-content/uploads/2026/02/Hodge-AR-28.01.26.pdf"
AR2024_URL = "https://hodgebank.co.uk/wp-content/uploads/2025/02/Hodge-annual-report-21.02.25.pdf"
AR2023_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/Annual-report-Jan-25.01.24.pdf"
AR2022_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/Hodge-Annual-Report-April-04.04.23-optimised.pdf"
AR2021_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/Hodge-Annual-Report-2020_2021.pdf"
P3_2023_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/Hodge-pillar-3-11.03.24.pdf"
P3_2022_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/Hodge-pillar-3-19.06.23.pdf"
P3_2021_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/Hodge-Pillar-3-Document-2020_2021.pdf"

# HD-049 (historical-depth extension, capped at FY2014): FY2014-FY2020 source documents.
#
# ANNUAL REPORTS stay on Wayback. The jhb-financial-statements-YYYY1031.pdf series (FY2010-FY2017)
# and 1.-JHB-Financial-Statements.pdf (FY2020) are genuinely gone from the live host - honest 404
# everywhere tried. FY2018 annual report cross-checked against the Companies House filing history
# (company 00743437) - both copies agree.
AR2020_URL = "https://web.archive.org/web/20210517011507id_/https://hodgebank.co.uk/wp-content/uploads/2021/02/1.-JHB-Financial-Statements.pdf"
AR2019_URL = "https://web.archive.org/web/20220620025335id_/https://hodgebank.co.uk/wp-content/uploads/2020/02/Julian-Hodge-Bank-Limited-Master-FINAL-EY-Signed-FY19.pdf"
AR2018_URL = "https://web.archive.org/web/20210517014628id_/https://hodgebank.co.uk/wp-content/uploads/2020/02/FINAL-Julian-Hodge-Bank-Limited-FY18.pdf"
AR2017_URL = "https://web.archive.org/web/20220620025318id_/https://hodgebank.co.uk/wp-content/uploads/2019/01/jhb-financial-statements-20171031-1.pdf"
AR2016_URL = "https://web.archive.org/web/20220620025318id_/https://hodgebank.co.uk/wp-content/uploads/2019/01/jhb-financial-statements-20161031-1.pdf"
AR2015_URL = "https://web.archive.org/web/20220620025258id_/https://hodgebank.co.uk/wp-content/uploads/2019/01/jhb-financial-statements-20151031.pdf"
AR2014_URL = "https://web.archive.org/web/20220620025529id_/https://hodgebank.co.uk/wp-content/uploads/2019/01/jhb-financial-statements-20141031.pdf"
# AR2018/AR2019 ALSO exist live at /wp-content/uploads/2024/07/FINAL-Julian-Hodge-Bank-Limited-FY18.pdf
# and /2024/07/Julian-Hodge-Bank-Limited-Master-FINAL-EY-Signed-FY19.pdf (both verified 2026-09-16:
# application/pdf, %PDF, 86pp / 79pp). The Wayback captions above are intact and content-equivalent,
# so they are deliberately left as the cited source; the live pair is recorded here as an alternate.

# PILLAR 3 DOCUMENTS ARE LIVE AGAIN ON THE PUBLISHER'S SITE - repointed 2026-09-16 (see PILLAR3_URL_NOTE).
# The whole historical series was re-uploaded on 2024-07-25 to /wp-content/uploads/2024/07/, where it
# is live and genuine. Each Wayback capture is retained immediately below its live URL as a labelled
# fallback - never delete these, they are the proven-good copies the figures were transcribed from.
# (P3_2023_URL / P3_2022_URL / P3_2021_URL above were already live at this path and are unchanged.)
P3_2020_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/2.-JHB-Pillar-III.pdf"
P3_2019_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/Pillar-3-Disclosure-FY19-FINAL.pdf"
P3_2018_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/jhb-pillar3-2018.pdf"
P3_2017_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/jhb-pillar3-2017.pdf"
P3_2016_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/jhb-pillar3-2016.pdf"
P3_2015_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/jhb-pillar3-2015.pdf"
P3_2014_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/jhb-pillar3-2014.pdf"
# Pre-CRD IV Basel II editions, newly located 2026-09-16 (HD-080). Same live directory.
P3_2013_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/jhb-pillar3-2013.pdf"
P3_2012_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/jhb-pillar3-2012.pdf"
P3_2011_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/jhb-pillar3-2011.pdf"
P3_2010_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/jhb-pillar3-2010.pdf"

# Wayback fallbacks - the captures these figures were originally transcribed from. Each was
# re-fetched 2026-09-16 and is byte-identical (md5) to the live file now cited above, which is what
# makes the repointing safe: no figure on any sheet changes meaning.
P3_2020_URL_ARCHIVE = "https://web.archive.org/web/20220620025450id_/https://hodgebank.co.uk/wp-content/uploads/2021/02/2.-JHB-Pillar-III.pdf"
P3_2019_URL_ARCHIVE = "https://web.archive.org/web/20210517002419id_/https://hodgebank.co.uk/wp-content/uploads/2020/02/Pillar-3-Disclosure-FY19-FINAL.pdf"
P3_2018_URL_ARCHIVE = "https://web.archive.org/web/20210517004624id_/https://hodgebank.co.uk/wp-content/uploads/2019/04/jhb-pillar3-2018.pdf"
P3_2017_URL_ARCHIVE = "https://web.archive.org/web/20220620025310id_/https://hodgebank.co.uk/wp-content/uploads/2019/01/jhb-pillar3-2017.pdf"
P3_2016_URL_ARCHIVE = "https://web.archive.org/web/20220620025406id_/https://hodgebank.co.uk/wp-content/uploads/2019/01/jhb-pillar3-2016.pdf"
P3_2015_URL_ARCHIVE = "https://web.archive.org/web/20220620025429id_/https://hodgebank.co.uk/wp-content/uploads/2019/01/jhb-pillar3-2015.pdf"
P3_2014_URL_ARCHIVE = "https://web.archive.org/web/20220620025434id_/https://hodgebank.co.uk/wp-content/uploads/2019/01/jhb-pillar3-2014.pdf"

PILLAR3_URL_NOTE = (
    "PILLAR 3 URL STATUS, established 2026-09-16 (HD-080). This CORRECTS a note previously held here "
    "which asserted that the historical Pillar 3 documents were NOT live on hodgebank.co.uk and that "
    "the Wayback citations must not be repointed. That note tested only the OLD paths - "
    "/wp-content/uploads/2019/01/, /2019/04/, /2020/02/ and /2021/02/ - and about those it was right: "
    "they are dead. But it never tested /wp-content/uploads/2024/07/, and the entire historical series "
    "was re-uploaded there on 2024-07-25. All 14 editions FY2010-FY2023 are live and genuine at that "
    "path. The old note's conclusion was therefore wrong and has been removed.\n"
    "HOW EACH FILE WAS VERIFIED (not by status code): HTTP status + Content-Type: application/pdf + "
    "%PDF magic bytes + pdfinfo page count + the cover page read for its stated period. Two traps on "
    "this host, both real:\n"
    "  (1) www.hodgebank.co.uk 301-redirects to the apex domain. curl without -L returns 301 / 162 "
    "bytes, which looks like a dead link and is almost certainly what produced the earlier report.\n"
    "  (2) The SOFT-404 on this host is PER-FILENAME, not per-directory - do not generalise a "
    "negative control across a directory. WordPress serves one 'Financial Information' landing page "
    "(HTTP 200, text/html, 108,306 bytes, md5 c69229b0d911df8ea64ada86d57738a2) for certain KNOWN OLD "
    "attachment slugs, while an unknown filename in that very same directory 404s honestly (146 "
    "bytes). Measured 2026-09-16: /2020/02/FINAL-Julian-Hodge-Bank-Limited-FY18.pdf -> soft-404 but "
    "/2020/02/zzz-nonexistent-control.pdf -> honest 404; /2021/02/2.-JHB-Pillar-III.pdf -> soft-404 "
    "but /2021/02/zzz-control.pdf -> honest 404; /2019/01/jhb-pillar3-2014.pdf -> honest 404; "
    "/2024/07/zzz-nonexistent-control.pdf -> honest 404. The decisive test is always the per-URL "
    "Content-Type plus %PDF check, never HTTP 200 and never a control run on a different filename.\n"
    "SAFETY OF THE REPOINTING: every live file was md5-compared against the Wayback capture the "
    "figures were originally transcribed from, and all five checked pairs are byte-identical - "
    "FY2018 addbb5d0301b1b2349dbd9b05d3b3dfc, FY2017 b76617584f830bf3f6dbb68720744fdd, FY2016 "
    "0bd97d21c8ebd0972d5e96be8c6c1d9b, FY2015 c448471eea12e998bbfb104e3074d3cc, FY2014 "
    "5318b684c1a1d4ef8e84d62a4ba055a4. The FY2019 (695,975 B) and FY2020 (2,416,601 B) live files "
    "likewise match their captures exactly. No transcribed figure changes. Every superseded Wayback "
    "URL is kept above as a *_URL_ARCHIVE fallback.\n"
    "ENUMERATION: the back catalogue was enumerated three ways - filename permutation "
    "jhb-pillar3-<year>.pdf across 2008-2023 (2008, 2009 and 2019-2023 honestly 404 under that name); "
    "the WordPress REST media API, whose library was walked in full (66 items over 2 pages, complete) "
    "and which is what surfaced the five irregularly-named editions that permutation can never find; "
    "and a Wayback CDX sweep of hodgebank.co.uk and julianhodgebank.co.uk which was BLOCKED (HTTP "
    "503/504, 'Internet Archive services are temporarily offline') and is therefore recorded as "
    "unknown, not as an absence - worth re-running, though the media API is already a complete "
    "listing of the WP library. Result: a continuous FY2010-FY2023 run of 14 editions, no FY2009, no "
    "FY2024, no FY2025.\n"
    "FILENAME NEVER EQUALS PERIOD ON THIS SITE. Hodge-pillar-3-19.06.23.pdf is a 2023 PUBLICATION "
    "date on the FY2022 edition, and Hodge-pillar-3-11.03.24.pdf is a 2024 publication date on the "
    "FY2023 edition. The cover page is the only trustworthy source of the period, and every period "
    "recorded in this script was read off the cover. This matters doubly because the year-end MOVES "
    "mid-series: 31 October through FY2019, 30 September from FY2021, with FY2020 an 11-month "
    "transition period."
)

# HD-074 (2026-09-07): FY2010-FY2013 extension, down to this entity's real statutory floor (HD-004/HD-002).
# Same Wayback archive as HD-049's FY2014-FY2020 batch, at the same /wp-content/uploads/2019/01/ path - all 3
# are text-native PDFs (no OCR needed). FY2012's own standalone Annual Report is NOT present anywhere in this
# archive (confirmed via the Wayback CDX API - a genuine gap, not a search failure) - FY2012 figures are instead
# sourced from the FY2013 Annual Report's own FY2012 comparative column (a document-level self-skip of the
# FY2012 standalone report only, not of the year itself, following this project's established convention for
# this kind of gap - see e.g. Vanquis Bank's FY2016 Pillar 3 treatment). FY2009 is a bonus year beyond the
# HD-004 floor, likewise sourced from the FY2010 Annual Report's own FY2009 comparative column (no standalone
# FY2009 report found in this archive either - not force-searched further per the ticket's guidance).
AR2013_URL_HD074 = "https://web.archive.org/web/20220620025323id_/https://hodgebank.co.uk/wp-content/uploads/2019/01/jhb-financial-statements-20131031.pdf"
AR2011_URL_HD074 = "https://web.archive.org/web/20220620025317id_/https://hodgebank.co.uk/wp-content/uploads/2019/01/jhb-financial-statements-20111031.pdf"
AR2010_URL_HD074 = "https://web.archive.org/web/20220620025334id_/https://hodgebank.co.uk/wp-content/uploads/2019/01/jhb-financial-statements-20101031.pdf"

HD074_NOTE = (
    "HISTORICAL-DEPTH NOTE (HD-074, added 2026-09-07): extends Balance Sheet, Profit & Loss and Statement of "
    "Changes in Equity back to FY2009 (one year beyond HD-004's confirmed FY2010 statutory floor) - Pillar 3, "
    "Asset Quality and RWA Breakdown remain capped at FY2014 as a deliberate project-wide scope decision, not a "
    "sourcing gap. This entity has no Cash Flow Statement in any year (see EXEMPTION_NOTE on the Cash Flow "
    "Statement sheet) - the FRS1 predecessor exemption (identical grounds: a parent undertaking includes the "
    "Bank in its own published consolidated accounts) is confirmed explicitly stated in each of the FY2013/"
    "FY2011/FY2010 Annual Reports too, so this extension adds no Cash Flow Statement columns. "
    f"FY2013 (and its own FY2012 comparative): Directors' report and financial statements 2013 - {AR2013_URL_HD074}\n"
    f"FY2011 (and its own FY2010 comparative): Directors' report and financial statements 2011 - {AR2011_URL_HD074}\n"
    f"FY2010 (and its own FY2009 comparative): Directors' report and financial statements 2010 - {AR2010_URL_HD074}\n"
    "All 3 new filings are old UK GAAP (pre-FRS101), consistent with the existing FY2014/FY2015 treatment "
    "already on this sheet - no basis-transition gap exists at the FY2013/FY2014 boundary (FY2013's own closing "
    "Total equity of GBP128.2m ties exactly to FY2014's own opening position). 'Equity shares' is a genuine "
    "small distinct holding line disclosed in the FY2010-FY2012 Balance Sheets (nil in FY2013) - not folded into "
    "Debt securities or another line, since it is its own numbered note in the source accounts. FY2012's own "
    "Profit and Loss Account (per the FY2013 Annual Report's own comparative) reclassified certain cost/income "
    "sub-lines from how they were originally presented (a reclassification only, explained in that report's own "
    "Note 1 - profit for the year and net assets are unaffected). Every one of the 5 new years' Balance Sheet "
    "ties exactly (Total assets = Total liabilities + Total equity, verified to the exact £000) and every new "
    "year's disclosed Profit on ordinary activities before taxation and Total recognised gains and losses in the "
    "financial year are reproduced exactly by the rows on this sheet and the Profit & Loss sheet."
)

ENTITY_NOTE = (
    "ENTITY NOTE: Julian Hodge Bank Limited (company 00743437, FRN 204439, incorporated 1962) is a "
    "privately-owned Cardiff-based bank; immediate parent Hodge Limited, ultimate parent The Carlyle Trust "
    "(Jersey) Limited. Fiscal year-end is 30 September from FY2021 onward (FY2020 was an 11-month transition "
    "period covering the change from the prior 31 October year-end used FY2014-FY2019). All 12 years' source "
    "documents are text-native PDFs, no OCR required."
)

EXEMPTION_NOTE = (
    "FRS 101 / FRS 1 CASH-FLOW EXEMPTION: every Annual Report FY2016-FY2025 states in Note 1 (Basis of "
    "preparation) that the Bank \"has applied the exemptions available under FRS 101 in respect of the following "
    "disclosures: A Cash Flow Statement and related notes; ...\" - e.g. Julian Hodge Bank Limited Annual Report "
    f"2025, Note 1.1, p.42 - {AR2025_URL}. FY2014-FY2015 (pre-FRS101, old UK GAAP) rely on the equivalent "
    "predecessor exemption under FRS 1 ('the Bank is exempt from the requirement to prepare a cash flow statement "
    "on the grounds that a parent undertaking includes the Bank in its own published consolidated financial "
    f"statements') - e.g. Julian Hodge Bank Limited Directors' report and financial statements 2015, p.19 - "
    f"{AR2015_URL}. The same FRS 1 exemption wording is confirmed present in each of the FY2009-FY2013 Directors' "
    "report and financial statements sourced for HD-074 (e.g. FY2010, FY2011, FY2013 reports, each Note 1) - see "
    "HD074_NOTE below. No Statement of Cash Flows exists in any of the entity's published accounts for any year "
    "FY2009-FY2025 - a standing structural feature spanning both the old-UK-GAAP and FRS101 eras, not a one-off or "
    "data gap. Per the project's established policy for this exemption (see The Bank of New York Mellon "
    "(International) Limited / ABC International Bank plc), this workbook is built as a PILLAR-3-ONLY variant: "
    "all 11 Pillar 3 metric sheets are populated below, but no cash flow figures exist to show. See the Overview "
    "sheet for the equivalent treatment there."
)

CASH_FLOW_SOURCES = ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE + "\n\n" + HD074_NOTE

BASIS_NOTE = (
    "DOCUMENT COVERAGE (re-established 2026-09-16, HD-080): this entity published a CONTINUOUS run of 14 "
    "standalone Pillar 3 documents, FY2010 through FY2023, and all 14 are cited above and live on the "
    "publisher's site. There is no FY2009 edition and no FY2024 or FY2025 edition. The run splits at the CRD IV "
    "boundary: FY2010-FY2015 are Basel II / BIPRU (see the pre-CRD IV note - only Total capital resources is "
    "transcribable from them), FY2016-FY2023 are CRD IV.\n"
    "FY2021-FY2023: full UK KM1-format 'Key Regulatory Metrics' table from each year's own standalone Pillar 3 "
    "Disclosures document. FY2024-FY2025: no standalone Pillar 3 document exists (the bank's financial "
    "information page lists a Pillar 3 disclosure link for FY2018-FY2023 only) - CET1/RWA/ratio figures instead "
    "come from each year's own Annual Report 'Capital risk management (unaudited)' note, which does not include "
    "Leverage Ratio, LCR, or NSFR. For FY2025 those 3 metrics are NOT APPLICABLE (structurally exempt, see "
    "below); for FY2024 they are an ordinary open gap - genuinely not located, not assumed absent.\n"
    "SDDT EXEMPTION - REASON FOR THE FY2025 CESSATION, established 2026-09-15 (cross-bank SDDT pass). Julian "
    "Hodge Bank is a Small Domestic Deposit Taker (SDDT) and is therefore not required to publish Pillar 3 "
    "disclosures, so the FY2025 absence is an EVIDENCED STRUCTURAL EXEMPTION and no FY2025 Pillar 3 document "
    "will ever appear. Evidence - the PRA's own firm-level register, the Bank of England consolidated list of "
    "waivers and modifications granted to PRA-authorised firms (downloaded 2026-09-15, "
    "https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/authorisations/"
    "waivers-and-modifications-of-rules/consolidated-waivers-pra-firms.csv), which carries TWO SDDT rows for "
    "FRN 204439, 'Julian Hodge Bank Limited': (a) 'CRR firms: SDDT Regime - General Application Part 1.2 & "
    "2.1(9)', sub rule 'Ru 1.2 & 2.1(9)', ref 'A00009819P.pdf', start '11/02/2025', end '11/02/2028'; and (b) "
    "'Modification by Consent - PRA Rulebook - CRR Firms - Rule 3.1 of the SDDT Regime - General Application "
    "Part', sub rule 'Ru 3.1', ref 'A00009917P.pdf', start '18/02/2025', no end date. Rule 3.1 is the "
    "modification by which a firm becomes an SDDT. What it does to Pillar 3 is stated by a peer holding the "
    "identical register row - Cynergy Bank plc Annual Report & Accounts 2024, p.71: 'The Bank applied for the "
    "Modification by Consent to become an SDDT and received approval on 17 January 2025. As a result, we are "
    "not required to publish Pillar 3 disclosures as at 31 December 2024 and will submit only a simplified "
    "retail deposit ratio instead of a full Net Stable Funding Ratio (NSFR) going forward.' (Cynergy's row: "
    "FRN 575105, Rule 3.1, start '17/01/2025' - matching its own stated approval date exactly, which is what "
    "ties the register row to the firm-stated effect.)\n"
    "DATE FIT, stated precisely because the two years differ. This bank's year-end is 30 September. FY2025 "
    "(period ended 30 September 2025) falls wholly after the 18 February 2025 modification, so FY2025 is "
    "unambiguously covered. FY2024 (period ended 30 September 2024) ENDED BEFORE the modification took "
    "effect, so the exemption does not straightforwardly cover it. It may still explain the FY2024 "
    "non-publication - Cynergy's 17 January 2025 approval expressly removed its obligation for the 31 "
    "December 2024 reporting date that preceded it, and Hodge's FY2024 Pillar 3 would have fallen due at "
    "almost exactly the point its own modification landed - but Julian Hodge Bank has not said so, so FY2024 "
    "is left as NOT ESTABLISHED rather than claimed as structurally exempt. It is recorded as: no FY2024 "
    "Pillar 3 document published; SDDT exemption effective from 18 February 2025 is a plausible but "
    "unconfirmed cause.\n"
    "The exemption explains NOTHING about FY2014-FY2023, every one of which has its own published Pillar 3 "
    "document cited above. Do not read SDDT back onto FY2023 or earlier. Neither Annual Report claims SDDT "
    "status in the bank's own words: both the FY2024 and FY2025 Annual Reports were downloaded and "
    "text-extracted in full (readable text layers, ~737k and ~751k characters) and searched for 'SDDT', "
    "'Small Domestic Deposit Taker', 'modification by consent', 'Simplified Retail Deposit Ratio', 'SRDR', "
    "'Strong and Simple', 'Interim Capital Regime' and 'Basel 3.1'. SDDT appears only as regulatory-"
    "developments context - AR2024 p.18 refers to 'the draft Small Domestic Deposit Takers' rules and AR2025 "
    "p.18 to 'the ongoing Basel 3.1 and Small Domestic Deposit Takers (SDDT) consultations' - and neither "
    "report mentions Pillar 3 disclosure obligations at all (the word 'Pillar' appears only in 'Pillar 1' and "
    "'Pillar 2'). No Simplified Retail Deposit Ratio value is disclosed, so nothing replaces the NSFR series."
)


LEVERAGE_BASIS_SOURCES = (
    "LEVERAGE-RATIO DUAL-BASIS SOURCES (both bases are printed by the Bank; neither is derived here):\n"
    f"FY2023 and FY2022 comparative, Template UK LRCom 'Leverage Ratio common disclosure at 30 September', "
    f"section 9 'Leverage Ratio' (rows 24, UK-24a, UK-24b, 25, UK-25c) - {P3_2023_URL}\n"
    f"FY2022 and FY2021 comparative, Template UK LRCom, section 9 'Leverage Ratio' (same rows), and Table "
    f"'3 Key Regulatory Metrics' rows 13/14 - {P3_2022_URL}\n"
    f"FY2021 as originally reported ('Basel III Leverage Ratio' / 'Total Basel III Leverage Ratio exposure "
    f"measure'), Summary of Key Regulatory Metrics - {P3_2021_URL}\n"
    "All three PDFs were downloaded and verified before reading (%PDF magic bytes; pdfinfo page counts 39, 41 "
    "and 58 respectively; none at the 1,048,576-byte Wayback truncation size), 2026-09-16."
)


def p3_sources(extra=""):
    return (
        "Sources - Julian Hodge Bank Limited:\n"
        f"FY2023: Hodge Bank Pillar 3 Disclosures - Period ended 30 September 2023, Table \"3 Key Regulatory "
        f"Metrics\", p.9 - {P3_2023_URL}\n"
        f"FY2022: Hodge Bank Pillar 3 Disclosures - Period ended 30 September 2022, Table \"3 Key Regulatory "
        f"Metrics\", p.12 - {P3_2022_URL}\n"
        f"FY2021: Hodge Bank Pillar 3 Disclosures - Period ended 30 September 2021, Table \"Key Metrics\", p.16 - "
        f"{P3_2021_URL}\n"
        f"FY2020: Julian Hodge Bank Limited Pillar 3 Disclosures - Period ended 30 September 2020, Summary of Key Regulatory Metrics, p.8 - {P3_2020_URL}\n"
        f"FY2019: Julian Hodge Bank Limited Pillar 3 Disclosures - Period ended 31 October 2019, Key Regulatory Metrics, p.10-11 - {P3_2019_URL}\n"
        f"FY2018: Julian Hodge Bank Limited Pillar 3 Disclosures - Period ended 31 October 2018, Key Regulatory Metrics, p.10-11 - {P3_2018_URL}\n"
        f"FY2017: Julian Hodge Bank Limited Pillar 3 Disclosures - Period ended 31 October 2017, Summary of Key Capital Ratios/Capital Resources, p.6/15 - {P3_2017_URL}\n"
        f"FY2016: Julian Hodge Bank Limited Pillar 3 Disclosures - Period ended 31 October 2016, Summary of Key Capital Ratios/Capital Resources, p.6/15 - {P3_2016_URL}\n"
        f"FY2015: Julian Hodge Bank Limited Pillar 3 Disclosures - Period ended 31 October 2015, Capital Resources, p.12-13 - {P3_2015_URL}\n"
        f"FY2014: Julian Hodge Bank Limited Pillar 3 Disclosures - period ended 31 October 2014, Capital Resources, p.12-13 - {P3_2014_URL}\n"
        f"FY2013: Julian Hodge Bank Limited Pillar 3 disclosures - as at 31 October 2013 (Basel II), section 4 "
        f"\"Capital resources\", PDF p.12 of 23, and section 5.1 \"Pillar 1 capital requirement\", PDF p.13 - {P3_2013_URL}\n"
        f"FY2012: Julian Hodge Bank Limited Pillar 3 disclosures - as at 31 October 2012 (Basel II), section 4 "
        f"\"Capital resources\", PDF p.11 of 21, and section 5.1 \"Pillar 1 capital requirement\", PDF p.12 - {P3_2012_URL}\n"
        f"FY2011: Julian Hodge Bank Limited Pillar 3 disclosures - as at 31 October 2011 (Basel II), section 4 "
        f"\"Capital resources\", PDF p.13 of 28, and section 5.1 \"Pillar 1 capital requirement\", PDF p.15 - {P3_2011_URL}\n"
        f"FY2010: Julian Hodge Bank Limited Pillar 3 disclosures - as at 31 October 2010 (Basel II), section 4 "
        f"\"Capital resources\", PDF p.13 of 27, and section 5.1 \"Pillar 1 capital requirement\", PDF p.15 - {P3_2010_URL}\n"
        f"FY2024: Julian Hodge Bank Limited Annual Report 2024, Note 32 'Capital risk management (unaudited)', "
        f"p.73 - {AR2024_URL}\n"
        f"FY2025: Julian Hodge Bank Limited Annual Report 2025, Note 34 'Capital risk management (unaudited)', "
        f"p.76 - {AR2025_URL}\n"
        "Wayback fallbacks for the FY2020-FY2014 documents, retained and never to be deleted (each is "
        "byte-identical to the live file now cited above):\n"
        f"  FY2020 - {P3_2020_URL_ARCHIVE}\n"
        f"  FY2019 - {P3_2019_URL_ARCHIVE}\n"
        f"  FY2018 - {P3_2018_URL_ARCHIVE}\n"
        f"  FY2017 - {P3_2017_URL_ARCHIVE}\n"
        f"  FY2016 - {P3_2016_URL_ARCHIVE}\n"
        f"  FY2015 - {P3_2015_URL_ARCHIVE}\n"
        f"  FY2014 - {P3_2014_URL_ARCHIVE}\n"
        + (extra + "\n" if extra else "") + BASIS_NOTE + "\n" + BASEL2_NOTE + "\n" + PILLAR3_URL_NOTE
    )


bw = BankWorkbook(bank_name="Julian Hodge Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="8B4513")

STATEMENTS_SOURCES = (
    "Sources - Julian Hodge Bank Limited Annual Reports:\n"
    f"FY2025: Annual Report 2025, Balance Sheet/Income Statement/Statement of Changes in Equity, p.40-41, "
    f"Note 12 'Loans and advances to customers'/Note 13 'Impairment provisions', p.49-50 - {AR2025_URL}\n"
    f"FY2024: Annual Report 2024, Balance Sheet/Income Statement/Statement of Changes in Equity, p.40-42, "
    f"Note 12/13, p.48-49 - {AR2024_URL}\n"
    f"FY2023: Annual Report 2023, Balance Sheet/Income Statement/Statement of Changes in Equity, p.40-42, "
    f"Note 13/14, p.49-50 - {AR2023_URL}\n"
    f"FY2022: Annual Report 2022, Balance Sheet/Income Statement/Statement of Changes in Equity, p.37-39, "
    f"Note 13/14, p.46-47 - {AR2022_URL}\n"
    f"FY2021: Annual Report 2021, Balance Sheet/Income Statement/Statement of Other Comprehensive Income/"
    f"Statement of Changes in Equity, p.62-65 (printed pages 67-70) - {AR2021_URL}\n"
    f"FY2020: Julian Hodge Bank Limited Annual Report (11-month period ended 30 September 2020), Income "
    f"Statement/Balance Sheet/Statement of Changes in Equity p.26-28, Note 14 'Impairment provisions', p.44-45 - "
    f"{AR2020_URL}\n"
    f"FY2019: Julian Hodge Bank Limited Annual Report and Financial Statements 2019 (Master FINAL EY Signed), "
    f"Income Statement/Balance Sheet/Statement of Changes in Equity p.20-23, Note 15 'Impairment provisions', "
    f"p.42-43 - {AR2019_URL}\n"
    f"FY2018: Julian Hodge Bank Limited Annual Report and Financial Statements 2018, Income Statement/Balance "
    f"Sheet/Statement of Changes in Equity p.24-26, Note 16 'Loans and advances to customers', p.42-44 - "
    f"{AR2018_URL} (cross-checked against the Companies House filing for the period made up to 31 October 2018)\n"
    f"FY2017: Julian Hodge Bank Limited Annual report and financial statements 2017, Income Statement/Balance "
    f"Sheet/Statement of Changes in Equity p.24-26, Note 16 'Loans and advances to customers', p.42-43 - "
    f"{AR2017_URL}\n"
    f"FY2016: Julian Hodge Bank Limited Financial Statements 2016 (FRS 101, first year of transition from UK "
    f"GAAP), Income Statement/Balance Sheet/Statement of Changes in Equity p.16-19, Note 16 'Loans and advances "
    f"to customers', p.34 - {AR2016_URL}\n"
    f"FY2015: Julian Hodge Bank Limited Directors' report and financial statements 2015 (UK GAAP), Profit and "
    f"loss account/Balance sheet p.13-15, Note 22 'reconciliation of movements in shareholder's funds', p.28, "
    f"Note 12 'Provisions for bad and doubtful debts', p.24 - {AR2015_URL}\n"
    f"FY2014: Julian Hodge Bank Limited Directors' report and financial statements 2014 (UK GAAP), Profit and "
    f"loss account/Balance sheet p.14-16, Note 12 'Provisions for bad and doubtful debts', p.24 - {AR2014_URL}\n\n"
    + ENTITY_NOTE + "\n\n"
    "HISTORICAL-DEPTH NOTE (HD-049): FY2016 is this entity's first year of FRS 101 reporting (transitioning from "
    "old UK GAAP used in FY2014-FY2015) - its own report's FY2015 comparative column is FRS101-restated and does "
    "NOT tie to FY2015's own contemporaneous UK GAAP report (e.g. FY2015 closing shareholder's funds/equity: "
    "GBP133.7m as originally reported in the FY2015 Annual Report vs GBP133.3m as restated in the FY2016 Annual "
    "Report's FY2015 comparative - a real GAAP-transition adjustment, not a transcription error). Per this "
    "project's convention, each year's own originally-published figures are used throughout (FY2014/FY2015 in "
    "UK GAAP format; FY2016 onward in FRS101 format), so the equity ladder has one genuine, documented break at "
    "the FY2015/FY2016 boundary rather than a forced tie-out. Separately, FY2017's own report restates FY2016's "
    "shareholder's funds from GBP146.3m (as FY2016's own report showed) to GBP153.5m, citing a 'prior period "
    "error' corrected in Note 36 (GBP6.8m addition to opening retained earnings, GBP0.3m to FY2016's own profit) - "
    "again, FY2016's own originally-published figures are used here, with this restatement documented rather than "
    "applied. IFRS 9 was adopted 1 November 2018 (start of FY2019), so IFRS 9 Stage 1/2/3 impairment staging "
    "exists only from FY2019 onward; FY2014-FY2018 show only the (unstaged) IAS 39/UK GAAP total impairment "
    "provision. FY2014-FY2015 Income Statement rows follow the old UK GAAP layout (interest receivable/payable, "
    "fees, 'other operating income' components including reversionary interest/stock profits, then a single "
    "'profit on ordinary activities before taxation' line) rather than the FRS101 Net interest income / Net "
    "operating income / Operating profit structure used FY2016 onward - both shown on their own basis, not forced "
    "into one template, consistent with how this same script already treats the FY2025 structural change."
)

# ---------------------------------------------------------------
# Balance Sheet
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances held at central banks", {"FY2025": 69.5, "FY2024": 151.3, "FY2023": 93.7, "FY2022": 118.1, "FY2021": 412.2, "FY2020": 147.9, "FY2019": 321.9, "FY2018": 153.2, "FY2017": 87.0, "FY2016": 168.0, "FY2015": 101.6, "FY2014": 18.5, "FY2013": 35.6, "FY2012": 37.0}),
    ("DATA", "Loans and advances to credit institutions", {"FY2025": 7.9, "FY2024": 4.5, "FY2023": 11.2, "FY2022": 0.2, "FY2021": 45.9, "FY2020": 105.2, "FY2019": 86.1, "FY2018": 96.2, "FY2017": 107.6, "FY2016": 128.3, "FY2015": 20.5, "FY2014": 28.8, "FY2013": 25.6, "FY2012": 90.6, "FY2011": 78.4, "FY2010": 188.5, "FY2009": 91.8}),
    ("DATA", "Derivative financial instruments (asset)", {"FY2025": 16.8, "FY2024": 27.9, "FY2023": 58.5, "FY2022": 75.8}),
    ("DATA", "Government bonds (called 'Treasury bills' in FY2009-FY2019 reports)", {"FY2025": 27.9, "FY2024": 27.7, "FY2023": 61.7, "FY2022": 111.2, "FY2021": 29.8, "FY2020": 48.6, "FY2019": 25.1, "FY2018": 81.2, "FY2017": 87.3, "FY2016": 84.7, "FY2015": 81.0, "FY2014": 75.5, "FY2013": 78.1, "FY2012": 81.3, "FY2011": 35.3, "FY2010": 42.5, "FY2009": 17.9}),
    ("DATA", "Debt securities", {"FY2025": 135.8, "FY2024": 70.7, "FY2023": 82.0, "FY2022": 116.2, "FY2021": 42.3, "FY2020": 50.7, "FY2019": 57.0, "FY2018": 87.5, "FY2017": 77.0, "FY2016": 89.1, "FY2015": 81.5, "FY2014": 85.1, "FY2013": 87.6, "FY2012": 89.5, "FY2011": 67.4, "FY2010": 54.2, "FY2009": 31.6}),
    ("DATA", "Loans and advances to customers", {"FY2025": 1839.7, "FY2024": 1699.3, "FY2023": 1488.5, "FY2022": 1404.6, "FY2021": 1061.5, "FY2020": 930.8, "FY2019": 766.9, "FY2018": 827.9, "FY2017": 757.9, "FY2016": 706.9, "FY2015": 557.5, "FY2014": 440.8, "FY2013": 384.0, "FY2012": 358.8, "FY2011": 362.8, "FY2010": 398.4, "FY2009": 470.2}),
    ("DATA", "Shares in group undertakings and participating interests (Hodge Life Assurance Company - sold/reclassified out by FY2018)", {"FY2017": 16.0, "FY2016": 16.0, "FY2015": 16.0, "FY2014": 16.0, "FY2013": 16.0, "FY2012": 16.1, "FY2011": 16.1, "FY2010": 16.1, "FY2009": 16.1}),
    ("DATA", "Equity shares (a small distinct holding, genuinely nil/absent in some years - not a residual)", {"FY2012": 0.8, "FY2011": 0.8, "FY2010": 0.4, "FY2009": 0.4}),
    ("DATA", "Stock and work in progress (UK GAAP line, folded into other line items after the FY2016 FRS101 transition)", {"FY2015": 3.4, "FY2014": 3.2, "FY2013": 4.5, "FY2012": 5.2}),
    ("DATA", "Reversionary interests in properties (UK GAAP line, folded into Investment properties after the FY2016 FRS101 transition)", {"FY2015": 55.0, "FY2014": 57.4, "FY2013": 59.4, "FY2012": 61.2, "FY2011": 62.6, "FY2010": 63.3, "FY2009": 57.3}),
    ("DATA", "Intangible assets", {"FY2025": 14.5, "FY2024": 15.1, "FY2023": 12.7, "FY2022": 9.7, "FY2021": 7.4, "FY2020": 7.3, "FY2019": 5.8, "FY2018": 3.1, "FY2017": 1.7, "FY2016": 1.2}),
    ("DATA", "Property and equipment", {"FY2025": 0.6, "FY2024": 1.0, "FY2023": 1.2, "FY2022": 1.5, "FY2021": 1.6, "FY2020": 1.9, "FY2019": 1.9, "FY2018": 2.2, "FY2017": 2.0, "FY2016": 2.1, "FY2015": 1.3, "FY2014": 0.6, "FY2013": 0.1, "FY2012": 0.1, "FY2011": 0.0, "FY2010": 0.0, "FY2009": 0.1}),
    ("DATA", "Investment properties", {"FY2025": 0.2, "FY2024": 1.5, "FY2023": 2.6, "FY2022": 9.2, "FY2021": 94.6, "FY2020": 97.4, "FY2019": 97.3, "FY2018": 100.3, "FY2017": 118.6, "FY2016": 107.8, "FY2015": 7.7, "FY2014": 9.2, "FY2013": 8.9, "FY2012": 8.9, "FY2011": 9.3, "FY2010": 10.3, "FY2009": 10.3}),
    ("DATA", "Deferred tax assets", {"FY2025": 2.2, "FY2024": 3.7, "FY2023": 5.6, "FY2022": 6.3, "FY2021": 11.5, "FY2020": 9.5, "FY2019": 6.6, "FY2018": 6.5, "FY2017": 7.3, "FY2016": 8.3}),
    ("DATA", "Other assets (includes prepayments/accrued income in FY2009-FY2015)", {"FY2025": 6.6, "FY2024": 5.9, "FY2023": 5.4, "FY2022": 8.0, "FY2021": 6.6, "FY2020": 9.9, "FY2019": 10.1, "FY2018": 5.3, "FY2017": 5.0, "FY2016": 4.4, "FY2015": 73.5, "FY2014": 49.7, "FY2013": 26.7, "FY2012": 53.0, "FY2011": 78.2, "FY2010": 51.7, "FY2009": 42.4}),
    ("DATA", "Pension asset", {"FY2025": 0.9, "FY2024": 0.2}),
    ("TOTAL", "Total assets", {"FY2025": 2122.6, "FY2024": 2008.8, "FY2023": 1823.1, "FY2022": 1860.8, "FY2021": 1713.4, "FY2020": 1409.2, "FY2019": 1378.7, "FY2018": 1363.4, "FY2017": 1267.4, "FY2016": 1316.8, "FY2015": 999.0, "FY2014": 784.7, "FY2013": 726.5, "FY2012": 802.5, "FY2011": 710.9, "FY2010": 825.3, "FY2009": 738.0}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks (called 'amounts owed to credit institutions and central banks' in FY2014-FY2015)", {"FY2025": 67.0, "FY2024": 167.7, "FY2023": 240.7, "FY2022": 221.0, "FY2021": 145.0, "FY2020": 87.5, "FY2019": 72.5, "FY2018": 72.5, "FY2017": 2.8, "FY2016": 2.8, "FY2015": 2.8, "FY2014": 10.0, "FY2013": 5.0, "FY2012": 8.9, "FY2011": 1.1, "FY2010": 0.5}),
    ("DATA", "Deposits from customers (called 'customer accounts' in FY2014-FY2015)", {"FY2025": 1860.3, "FY2024": 1639.4, "FY2023": 1368.1, "FY2022": 1425.0, "FY2021": 1381.0, "FY2020": 1071.4, "FY2019": 1042.8, "FY2018": 994.6, "FY2017": 947.7, "FY2016": 991.7, "FY2015": 848.6, "FY2014": 633.2, "FY2013": 583.6, "FY2012": 658.9, "FY2011": 579.6, "FY2010": 696.2, "FY2009": 610.5}),
    ("DATA", "Derivative financial instruments (liability)", {"FY2025": 5.1, "FY2024": 5.6, "FY2023": 9.7, "FY2022": 11.4, "FY2021": 14.7, "FY2020": 82.0, "FY2019": 80.4, "FY2018": 107.8, "FY2017": 131.1, "FY2016": 150.6}),
    ("DATA", "Other liabilities (includes accruals/deferred income and other provisions in FY2009-FY2020)", {"FY2025": 10.4, "FY2024": 12.9, "FY2023": 16.5, "FY2022": 13.9, "FY2021": 9.9, "FY2020": 6.3, "FY2019": 6.1, "FY2018": 4.0, "FY2017": 5.5, "FY2016": 11.9, "FY2015": 10.3, "FY2014": 6.6, "FY2013": 7.5, "FY2012": 7.7, "FY2011": 4.9, "FY2010": 4.3, "FY2009": 4.5}),
    ("DATA", "Pension liabilities", {"FY2023": 4.3, "FY2022": 4.5, "FY2021": 14.2, "FY2020": 21.0, "FY2019": 16.6, "FY2018": 12.8, "FY2017": 13.0, "FY2016": 13.5, "FY2015": 3.6, "FY2014": 2.9, "FY2013": 2.2, "FY2012": 1.4, "FY2011": 0.6, "FY2010": 0.1, "FY2009": 0.9}),
    ("TOTAL", "Total liabilities", {"FY2025": 1942.8, "FY2024": 1825.6, "FY2023": 1639.3, "FY2022": 1675.8, "FY2021": 1564.8, "FY2020": 1268.2, "FY2019": 1218.4, "FY2018": 1191.7, "FY2017": 1100.1, "FY2016": 1170.5, "FY2015": 865.3, "FY2014": 652.7, "FY2013": 598.3, "FY2012": 676.9, "FY2011": 586.2, "FY2010": 701.1, "FY2009": 615.9}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 130.0, "FY2024": 130.0, "FY2023": 130.0, "FY2022": 130.0, "FY2021": 105.0, "FY2020": 105.0, "FY2019": 105.0, "FY2018": 105.0, "FY2017": 105.0, "FY2016": 100.0, "FY2015": 100.0, "FY2014": 100.0, "FY2013": 100.0, "FY2012": 100.0, "FY2011": 100.0, "FY2010": 100.0, "FY2009": 100.0}),
    ("DATA", "Other reserves (retained earnings + pension reserve; profit and loss account + revaluation reserve in FY2009-FY2015 UK GAAP)", {"FY2025": 49.8, "FY2024": 53.2, "FY2023": 53.8, "FY2022": 55.0, "FY2021": 43.6, "FY2020": 36.0, "FY2019": 55.3, "FY2018": 66.7, "FY2017": 62.3, "FY2016": 46.3, "FY2015": 33.7, "FY2014": 32.0, "FY2013": 28.2, "FY2012": 25.6, "FY2011": 24.7, "FY2010": 24.1, "FY2009": 22.1}),
    ("TOTAL", "Total equity", {"FY2025": 179.8, "FY2024": 183.2, "FY2023": 183.8, "FY2022": 185.0, "FY2021": 148.6, "FY2020": 141.0, "FY2019": 160.3, "FY2018": 171.7, "FY2017": 167.3, "FY2016": 146.3, "FY2015": 133.7, "FY2014": 132.0, "FY2013": 128.2, "FY2012": 125.6, "FY2011": 124.7, "FY2010": 124.1, "FY2009": 122.1}),
    ("TOTAL", "Total equity and liabilities", {"FY2025": 2122.6, "FY2024": 2008.8, "FY2023": 1823.1, "FY2022": 1860.8, "FY2021": 1713.4, "FY2020": 1409.2, "FY2019": 1378.7, "FY2018": 1363.4, "FY2017": 1267.4, "FY2016": 1316.8, "FY2015": 999.0, "FY2014": 784.7, "FY2013": 726.5, "FY2012": 802.5, "FY2011": 710.9, "FY2010": 825.3, "FY2009": 738.0}),
]

bw.add_balance_sheet_sheet(
    title="Julian Hodge Bank Limited — Balance Sheet",
    subtitle="Entity-level (Company-only, FRS 101). £m.",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + HD074_NOTE,
    first_col_width=64,
    source_height=280,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest revenue calculated using the EIR method (FY2014-FY2015: UK GAAP interest receivable, not EIR-method - same row for comparability, see note)",
     {"FY2025": 122.9, "FY2024": 92.1, "FY2023": 67.3, "FY2022": 50.5, "FY2021": 39.6, "FY2020": 38.4, "FY2019": 48.3, "FY2018": 46.0, "FY2017": 41.3, "FY2016": 42.2, "FY2015": 33.3, "FY2014": 28.9,
      "FY2013": 27.5, "FY2012": 26.9, "FY2011": 28.4, "FY2010": 33.5, "FY2009": 32.6}),
    ("DATA", "Interest expense calculated using the EIR method (FY2014-FY2015: UK GAAP interest payable)",
     {"FY2025": -81.1, "FY2024": -52.4, "FY2023": -27.9, "FY2022": -21.1, "FY2021": -22.0, "FY2020": -22.8, "FY2019": -28.1, "FY2018": -27.7, "FY2017": -27.4, "FY2016": -29.0, "FY2015": -27.7, "FY2014": -26.0,
      "FY2013": -29.4, "FY2012": -28.7, "FY2011": -28.3, "FY2010": -31.0, "FY2009": -25.3}),
    ("TOTAL", "Net interest income", {"FY2025": 41.8, "FY2024": 39.7, "FY2023": 39.4, "FY2022": 29.4, "FY2021": 17.6, "FY2020": 15.6, "FY2019": 20.2, "FY2018": 18.3, "FY2017": 13.9, "FY2016": 13.2, "FY2015": 5.6, "FY2014": 2.9,
      "FY2013": -1.9, "FY2012": -1.8, "FY2011": 0.2, "FY2010": 2.4, "FY2009": 7.4}),
    ("DATA", "Fees and commission income", {"FY2025": 1.0, "FY2024": 2.9, "FY2023": 2.5, "FY2022": 2.6, "FY2021": 2.5, "FY2020": 1.8, "FY2019": 0.7, "FY2018": 2.5, "FY2017": 0.5, "FY2016": 1.1, "FY2015": 2.8, "FY2014": 2.2,
      "FY2013": 1.1, "FY2012": 1.2, "FY2011": 1.3, "FY2010": 1.6, "FY2009": 2.6}),
    ("DATA", "Fees and commission expense", {"FY2025": -3.6, "FY2024": -1.2, "FY2023": -0.1, "FY2022": -0.1, "FY2019": -0.1, "FY2018": -1.1, "FY2017": -1.2, "FY2016": -0.7, "FY2015": -0.8, "FY2014": -1.5,
      "FY2013": -0.3, "FY2011": -0.1, "FY2010": -0.4, "FY2009": -1.0}),
    ("TOTAL", "Net fee and commission income/(expense)", {"FY2025": -2.6, "FY2024": 1.7, "FY2023": 2.4, "FY2022": 2.5, "FY2021": 2.5, "FY2020": 1.8, "FY2019": 0.6, "FY2018": 1.4, "FY2017": -0.7, "FY2016": 0.4, "FY2015": 2.0, "FY2014": 0.7,
      "FY2013": 0.8, "FY2012": 1.2, "FY2011": 1.3, "FY2010": 1.2, "FY2009": 1.6}),
    ("DATA", "Investment income (FY2014-FY2015: 'Other finance income')", {"FY2025": 0.6, "FY2024": 0.5, "FY2023": 4.6, "FY2022": 6.7, "FY2021": 6.0, "FY2020": 3.5, "FY2019": 7.2, "FY2018": 6.4, "FY2017": 4.8, "FY2015": 0.4, "FY2014": 0.8,
      "FY2013": 0.3, "FY2012": 0.4, "FY2011": -0.1, "FY2010": 0.1, "FY2009": 0.2}),
    ("DATA", "Dividend income from listed equity shares and subsidiary companies (FY2009-FY2013 only)",
     {"FY2012": 0.2, "FY2011": 0.2, "FY2010": 0.1, "FY2009": 0.4}),
    ("DATA", "Other operating income", {"FY2023": 0.2, "FY2021": 0.1, "FY2018": 0.1, "FY2017": 1.0, "FY2016": 0.8, "FY2015": 5.0, "FY2014": 4.9,
      "FY2013": 9.0, "FY2012": 8.2, "FY2011": 7.5, "FY2010": 12.2, "FY2009": 3.4}),
    ("DATA", "Bad debt recovery", {"FY2022": 0.4}),
    ("TOTAL", "Net operating income", {"FY2025": 39.8, "FY2024": 41.9, "FY2023": 46.6, "FY2022": 38.6, "FY2021": 26.2, "FY2020": 20.9, "FY2019": 28.0, "FY2018": 18.2, "FY2017": 19.3, "FY2016": 33.5, "FY2015": 13.0, "FY2014": 9.3,
      "FY2013": 8.2, "FY2012": 8.1, "FY2011": 9.0, "FY2010": 16.1, "FY2009": 13.0}),
    ("DATA", "Administrative expenses", {"FY2025": -33.7, "FY2024": -36.4, "FY2023": -35.3, "FY2022": -34.2, "FY2021": -25.9, "FY2020": -22.3, "FY2019": -16.4, "FY2018": -12.0, "FY2017": -9.9, "FY2016": -8.1, "FY2015": -6.7, "FY2014": -5.4,
      "FY2013": -4.5, "FY2012": -4.9, "FY2011": -4.9, "FY2010": -5.7, "FY2009": -7.5}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -3.1, "FY2024": -2.9, "FY2023": -2.9, "FY2022": -2.5, "FY2021": -2.4, "FY2020": -1.8, "FY2019": -1.2, "FY2018": -0.9, "FY2017": -0.5, "FY2016": -0.2,
      "FY2013": 0.0, "FY2012": 0.0, "FY2011": 0.0, "FY2010": 0.0, "FY2009": -0.2}),
    ("DATA", "Impairment (losses)/gains on loans and advances to customers", {"FY2025": -6.5, "FY2024": -2.2, "FY2023": -1.6, "FY2020": -5.4, "FY2019": -3.9, "FY2018": 1.0, "FY2017": 1.6, "FY2016": -2.4, "FY2015": -2.1, "FY2014": -0.7,
      "FY2013": -0.1, "FY2012": 0.8, "FY2011": -1.5, "FY2010": -8.2, "FY2009": -4.2}),
    ("DATA", "Movement in valuation of stock/work-in-progress (UK GAAP line, FY2009-FY2015 only)", {"FY2015": 0.9, "FY2014": 1.1, "FY2013": -0.1, "FY2012": -0.9}),
    ("TOTAL", "Operating profit/(loss) (FY2021-FY2024 subtotal; see Net operating (loss)/income for FY2025's own equivalent line)",
     {"FY2024": 0.4, "FY2023": 6.8, "FY2022": 2.3, "FY2021": -2.1, "FY2020": -8.6, "FY2019": 6.5}),
    ("TOTAL", "Net operating (loss)/income (FY2025's own subtotal, structured differently from FY2021-FY2024's 'Operating profit')",
     {"FY2025": -3.5}),
    ("DATA", "(Loss)/gain arising from the derecognition of financial assets managed at amortised cost", {"FY2024": -1.0, "FY2021": 0.0, "FY2020": 4.2, "FY2019": 3.1}),
    ("DATA", "Other fair value gains/(losses)", {"FY2025": -2.3, "FY2024": -1.5, "FY2023": -7.0, "FY2022": 4.3, "FY2021": 11.3, "FY2020": -16.7, "FY2019": -12.8, "FY2018": -8.0, "FY2017": 0.3, "FY2016": 19.2}),
    ("DATA", "Loss on disposal of loans and advances to customers held at fair value", {"FY2021": -5.5, "FY2019": -4.6}),
    ("TOTAL", "Profit/(loss) before taxation (FY2014-FY2015: 'Profit on ordinary activities before taxation')",
     {"FY2025": -5.8, "FY2024": -2.1, "FY2023": -0.2, "FY2022": 6.6, "FY2021": 3.7, "FY2020": -21.1, "FY2019": -7.8, "FY2018": 6.3, "FY2017": 10.5, "FY2016": 22.8, "FY2015": 5.0, "FY2014": 4.3,
      "FY2013": 3.5, "FY2012": 3.1, "FY2011": 2.6, "FY2010": 2.1, "FY2009": 1.2}),
    ("DATA", "Tax credit/(charge) on profit/(loss) before taxation", {"FY2025": 1.9, "FY2024": 0.4, "FY2022": -1.8, "FY2021": 2.1, "FY2020": 5.2, "FY2019": 2.1, "FY2018": -0.8, "FY2017": -0.3, "FY2016": -5.2, "FY2015": -0.8, "FY2014": -0.2,
      "FY2013": 0.1, "FY2012": -0.5, "FY2011": -0.6, "FY2010": -0.8, "FY2009": -0.4}),
    ("TOTAL", "Profit/(loss) for the financial year", {"FY2025": -3.9, "FY2024": -1.7, "FY2023": -0.2, "FY2022": 4.8, "FY2021": 5.8, "FY2020": -15.9, "FY2019": -5.7, "FY2018": 5.5, "FY2017": 10.2, "FY2016": 17.6, "FY2015": 4.3, "FY2014": 4.1,
      "FY2013": 3.5, "FY2012": 2.6, "FY2011": 2.0, "FY2010": 1.3, "FY2009": 0.7}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Re-measurement of defined benefit pension plan (FY2014-FY2015: 'Actuarial loss recognised in the pension scheme')",
     {"FY2025": 0.7, "FY2024": 1.7, "FY2023": -1.7, "FY2022": 9.0, "FY2021": 2.6, "FY2020": -4.4, "FY2019": -3.3, "FY2018": 0.6, "FY2017": 0.4, "FY2016": -9.1, "FY2015": -1.1, "FY2014": -1.4,
      "FY2013": -1.2, "FY2012": -1.4, "FY2011": -0.5, "FY2010": 0.7, "FY2009": -2.8}),
    ("DATA", "Deferred tax on pension plan re-measurement", {"FY2025": -0.2, "FY2024": -0.4, "FY2023": 0.4, "FY2022": -2.2, "FY2021": -0.4, "FY2020": 0.7, "FY2019": 0.6, "FY2018": -0.1, "FY2017": -0.1, "FY2016": 1.5,
      "FY2013": 0.2, "FY2012": 0.2, "FY2011": 0.1}),
    ("DATA", "Deficit on revaluation of investment properties (FY2011-FY2012 only)", {"FY2012": -0.4, "FY2011": -1.0}),
    ("DATA", "Movement of pension scheme reimbursement asset/(liability) (FY2014-FY2015: net of deferred tax)",
     {"FY2024": -0.3, "FY2023": 0.4, "FY2022": -0.2, "FY2021": -1.0, "FY2020": 0.4, "FY2019": 0.5, "FY2018": -0.1, "FY2017": -0.9, "FY2016": 2.3, "FY2015": 0.1, "FY2014": 0.7}),
    ("DATA", "Deferred tax on pension reimbursement movement", {"FY2024": 0.1, "FY2023": -0.1, "FY2021": 0.6, "FY2020": -0.1, "FY2019": -0.1, "FY2017": 0.1, "FY2016": -0.4}),
    ("DATA", "Fair value movements on available-for-sale investments (AFS reserve; discontinued after IFRS 9 replaced it FY2019)",
     {"FY2018": -1.8, "FY2017": -0.1, "FY2016": 1.1}),
    ("DATA", "Deferred tax on available-for-sale fair value movements", {"FY2018": 0.3, "FY2017": -0.8}),
    ("DATA", "Revaluation of investment properties (UK GAAP line, FY2014-FY2015 only, net of deferred tax)", {"FY2015": -1.5, "FY2014": 0.3}),
    ("TOTAL", "Total other comprehensive income/(loss)", {"FY2025": 0.5, "FY2024": 1.1, "FY2023": -1.0, "FY2022": 6.6, "FY2021": 1.8, "FY2020": -3.4, "FY2019": -2.3, "FY2018": -1.1, "FY2017": -1.4, "FY2016": -4.6, "FY2015": -2.5, "FY2014": -0.3,
      "FY2013": -1.0, "FY2012": -1.6, "FY2011": -1.4, "FY2010": 0.7, "FY2009": -2.8}),
    ("TOTAL", "Total comprehensive (loss)/income for the year", {"FY2025": -3.4, "FY2024": -0.6, "FY2023": -1.2, "FY2022": 11.4, "FY2021": 7.6, "FY2020": -19.3, "FY2019": -8.0, "FY2018": 4.4, "FY2017": 8.8, "FY2016": 13.0, "FY2015": 1.8, "FY2014": 3.8,
      "FY2013": 2.6, "FY2012": 1.0, "FY2011": 0.5, "FY2010": 2.0, "FY2009": -2.1}),
]

bw.add_income_statement_sheet(
    title="Julian Hodge Bank Limited — Profit & Loss",
    subtitle="Entity-level (Company-only, FRS 101). £m. Structure genuinely changes FY2025 (Net operating (loss)/income "
              "subtotal replaces the FY2021-FY2024 'Operating profit' subtotal) - both shown on their own basis, not forced "
              "into one template. Each year's own originally-published figures used throughout; note AR2025's own FY2024 "
              "comparative column is separately labelled 'Restated' (Note 33 interest revenue/expense reclassification) - "
              "that restated column is NOT used here, FY2024's own contemporaneous report is used instead, per project convention.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + HD074_NOTE,
    first_col_width=90,
    source_height=280,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - per-year reconciliation ladder. FY2021-FY2025 confirmed: every year's own
# closing balance ties exactly to both the next year's own opening balance and that year's own Balance Sheet
# Total equity - zero plug rows needed. FY2014-FY2020 (HD-049 extension) also ties exactly year-to-year once the
# "Other reserves" column is read as: Revaluation reserve (FY2014-FY2015, UK GAAP) -> Available-for-sale reserve
# + Pension reserve combined (FY2016-FY2019, FRS101/IAS 39) -> Pension reserve only (FY2020 onward, post-IFRS 9 -
# the AFS reserve was extinguished on IFRS 9 adoption 1 November 2018). One genuine, documented break exists at
# the FY2016/FY2017 boundary: FY2016's own Annual Report reported its own closing equity at GBP146.3m, but
# FY2017's Annual Report (Note 36) restates FY2016's opening/closing position for a "prior period error"
# (+GBP7.2m, entirely in retained earnings) - both the originally-published FY2016 closing balance and the
# subsequent restatement are shown explicitly below, rather than silently using one or the other.
# ---------------------------------------------------------------
equity_headers = ["Called up share capital", "Retained earnings", "Other reserves (see sheet note)", "Total"]
equity_rows = [
    ("TOTAL", "Opening balance at 1 November 2009 (FY2010 opening, per the FY2010 Annual Report; FY2009's own "
     "1 November 2008 opening and component movement are not available from the sourced documents - see HD074_NOTE - "
     "so the ladder begins here, one year later than the Balance Sheet/P&L sheets)", (100.0, 22.1, None, 122.1)),
    ("DATA", "Profit for the financial year", (None, 1.3, None, 1.3)),
    ("TOTAL", "At 31 October 2010 (FY2010 closing)", (100.0, 24.1, None, 124.1)),
    ("DATA", "Profit for the financial year", (None, 2.0, None, 2.0)),
    ("DATA", "Deficit on revaluation of investment properties", (None, None, -1.0, -1.0)),
    ("DATA", "Actuarial loss recognised in the pension scheme (net of deferred tax)", (None, -0.4, None, -0.4)),
    ("TOTAL", "At 31 October 2011 (FY2011 closing)", (100.0, 25.7, -1.0, 124.7)),
    ("DATA", "Profit for the financial year", (None, 2.6, None, 2.6)),
    ("DATA", "Deficit on revaluation of investment properties", (None, None, -0.4, -0.4)),
    ("DATA", "Actuarial loss recognised in the pension scheme (net of deferred tax)", (None, -1.2, None, -1.2)),
    ("TOTAL", "At 31 October 2012 (FY2012 closing, per the FY2013 Annual Report's own comparative - see HD074_NOTE "
     "on the FY2012 standalone-document gap)", (100.0, 27.1, -1.4, 125.6)),
    ("DATA", "Profit for the financial year", (None, 3.5, None, 3.5)),
    ("DATA", "Actuarial loss recognised in the pension scheme (net of deferred tax)", (None, -1.0, None, -1.0)),
    ("TOTAL", "Opening balance at 1 November 2013 (FY2014 opening)", (100.0, 29.7, -1.4, 128.2)),
    ("DATA", "Profit for the financial year", (None, 4.1, None, 4.1)),
    ("DATA", "Actuarial loss recognised in the pension scheme (net of deferred tax)", (None, -1.4, None, -1.4)),
    ("DATA", "Recognition of pension scheme reimbursement asset (net of deferred tax)", (None, 0.7, None, 0.7)),
    ("DATA", "Revaluation of investment properties", (None, None, 0.3, 0.3)),
    ("TOTAL", "At 31 October 2014 (FY2014 closing)", (100.0, 33.1, -1.1, 132.0)),
    ("DATA", "Profit for the financial year", (None, 4.3, None, 4.3)),
    ("DATA", "Actuarial loss recognised in the pension scheme (net of deferred tax)", (None, -1.1, None, -1.1)),
    ("DATA", "Recognition of pension scheme reimbursement asset (net of deferred tax)", (None, 0.1, None, 0.1)),
    ("DATA", "Revaluation of investment properties", (None, None, -1.5, -1.5)),
    ("TOTAL", "At 31 October 2015 (FY2015 closing)", (100.0, 36.4, -2.6, 133.7)),
    ("DATA", "Profit for the financial year", (None, 17.6, None, 17.6)),
    ("DATA", "Other comprehensive income (AFS + pension, FRS101 first-year transition)", (None, None, -4.6, -4.6)),
    ("TOTAL", "At 31 October 2016 (FY2016 closing, as originally reported in the FY2016 Annual Report)", (100.0, 49.4, -3.1, 146.3)),
    ("DATA", "Prior period error restatement (FY2017 Annual Report, Note 36 - not reflected in FY2016's own original report)",
     (None, 7.2, None, 7.2)),
    ("TOTAL", "At 31 October 2016 (restated, per the FY2017 Annual Report's own comparative)", (100.0, 56.6, -3.1, 153.5)),
    ("DATA", "Profit for the financial year", (None, 10.2, None, 10.2)),
    ("DATA", "Other comprehensive income (AFS + pension)", (None, None, -1.4, -1.4)),
    ("DATA", "Issue of share capital", (5.0, None, None, 5.0)),
    ("TOTAL", "At 31 October 2017 (FY2017 closing)", (105.0, 66.8, -4.5, 167.3)),
    ("DATA", "Profit for the financial year", (None, 5.9, -0.4, 5.5)),
    ("DATA", "Other comprehensive income (AFS + pension)", (None, None, -1.1, -1.1)),
    ("TOTAL", "At 31 October 2018 (FY2018 closing)", (105.0, 72.7, -6.0, 171.7)),
    ("DATA", "Impact of adoption of IFRS 9 (extinguishes the AFS reserve)", (None, -0.7, -2.7, -3.4)),
    ("DATA", "Loss for the financial year", (None, -5.3, -0.4, -5.7)),
    ("DATA", "Other comprehensive income (pension only - AFS reserve extinguished)", (None, None, -2.3, -2.3)),
    ("TOTAL", "At 31 October 2019 (FY2019 closing)", (105.0, 66.7, -11.4, 160.3)),
    ("DATA", "Loss for the financial year", (None, -16.3, 0.4, -15.9)),
    ("DATA", "Other comprehensive income", (None, None, -3.4, -3.4)),
    ("TOTAL", "At 30 September 2020 (FY2020 closing - 11-month transition period; opening balance below = FY2021 opening)",
     (105.0, 50.4, -14.4, 141.0)),
    ("TOTAL", "Opening balance at 1 October 2020 (FY2021 opening)", (105.0, 50.4, -14.4, 141.0)),
    ("DATA", "Profit for the financial year", (None, 5.5, 0.3, 5.8)),
    ("DATA", "Other comprehensive income", (None, None, 1.8, 1.8)),
    ("TOTAL", "At 30 September 2021 (FY2021 closing)", (105.0, 54.3, -10.7, 148.6)),
    ("DATA", "Issue of share capital", (25.0, None, None, 25.0)),
    ("DATA", "Profit for the financial year", (None, 5.2, -0.4, 4.8)),
    ("DATA", "Other comprehensive income", (None, None, 6.6, 6.6)),
    ("DATA", "Pension additional contribution", (None, -1.2, 1.2, None)),
    ("TOTAL", "At 30 September 2022 (FY2022 closing)", (130.0, 58.3, -3.3, 185.0)),
    ("DATA", "Loss for the financial year", (None, 0.1, -0.3, -0.2)),
    ("DATA", "Other comprehensive loss", (None, None, -1.0, -1.0)),
    ("DATA", "Pension additional contribution", (None, -1.8, 1.8, None)),
    ("TOTAL", "At 30 September 2023 (FY2023 closing)", (130.0, 56.6, -2.8, 183.8)),
    ("DATA", "Loss for the financial year", (None, -1.5, -0.2, -1.7)),
    ("DATA", "Other comprehensive income", (None, None, 1.1, 1.1)),
    ("DATA", "Pension additional contribution", (None, -3.0, 3.0, None)),
    ("TOTAL", "At 30 September 2024 (FY2024 closing)", (130.0, 52.1, 1.1, 183.2)),
    ("DATA", "Loss for the financial year", (None, -3.9, None, -3.9)),
    ("DATA", "Other comprehensive income", (None, None, 0.5, 0.5)),
    ("TOTAL", "At 30 September 2025 (FY2025 closing)", (130.0, 48.2, 1.6, 179.8)),
]

bw.add_equity_changes_sheet(
    title="Julian Hodge Bank Limited — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, FY2014-FY2025. Reconciliation ladder ties exactly year-to-year "
              "and to each year's own Balance Sheet Total equity throughout, with one documented exception: the FY2016/"
              "FY2017 boundary carries an explicit prior-period-error restatement row (see sheet note). 'Other reserves' "
              "column is Revaluation reserve (FY2014-FY2015, UK GAAP) / Available-for-sale + Pension reserve combined "
              "(FY2016-FY2019) / Pension reserve only (FY2020 onward, post-IFRS 9). £m.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + HD074_NOTE,
)

# ---------------------------------------------------------------
# Asset Quality - Note 12/13's own IFRS 9 Stage 1/2/3/PMA provision
# roll-forward (portfolio-wide, all loans and advances to customers at
# amortised cost combined - no gross-exposure-by-stage table exists at
# portfolio level, only per-product segment tables for Commercial/PBTL/
# Motor separately, which don't sum to the full book since Retail's own
# stage split isn't separately disclosed).
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to customers at amortised cost", {}),
    ("DATA", "Gross balances", {"FY2025": 1811.1, "FY2024": 1671.4, "FY2023": 1483.1, "FY2022": 1403.6, "FY2021": 989.9, "FY2020": 709.3, "FY2019": 526.4, "FY2018": 562.3, "FY2017": 469.9, "FY2016": 386.5, "FY2015": 335.3}),
    ("DATA", "Net loan fee deferral", {"FY2025": 13.0, "FY2024": 8.5, "FY2023": 2.9, "FY2022": 3.7, "FY2021": 1.9, "FY2020": -0.8, "FY2019": -1.7, "FY2018": -2.3, "FY2017": -2.5, "FY2016": -2.3, "FY2015": -1.9}),
    ("DATA", "Provision for impairment", {"FY2025": -13.8, "FY2024": -7.7, "FY2023": -6.0, "FY2022": -8.6, "FY2021": -8.4, "FY2020": -7.9, "FY2019": -9.8, "FY2018": -3.7, "FY2017": -6.4, "FY2016": -10.0, "FY2015": -7.6, "FY2014": -5.8}),
    ("TOTAL", "Net balance (amortised cost)", {"FY2025": 1810.3, "FY2024": 1672.2, "FY2023": 1480.0, "FY2022": 1398.7, "FY2021": 983.4, "FY2020": 700.6, "FY2019": 514.9, "FY2018": 556.3, "FY2017": 461.0, "FY2016": 374.2, "FY2015": 325.8}),
    ("DATA", "Impairment provision coverage (%)", {
        "FY2025": "0.76%", "FY2024": "0.46%", "FY2023": "0.40%", "FY2022": "0.61%", "FY2021": "0.85%",
        "FY2020": "1.11%", "FY2019": "1.86%", "FY2018": "0.66%", "FY2017": "1.36%", "FY2016": "2.59%", "FY2015": "2.27%",
    }),
    ("SECTION", "Impairment provision, by IFRS 9 stage (IFRS 9 adopted 1 November 2018 - stage data only exists FY2019 onward; "
               "FY2014-FY2018 show only the unstaged IAS 39/UK GAAP total provision above)", {}),
    ("DATA", "Stage 1 (12-month ECL)", {"FY2025": 3.6, "FY2024": 2.4, "FY2023": 1.3, "FY2022": 1.7, "FY2021": 1.3, "FY2020": 1.5, "FY2019": 2.4}),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {"FY2025": 1.7, "FY2024": 1.2, "FY2023": 3.1, "FY2022": 1.3, "FY2021": 2.0, "FY2020": 1.6, "FY2019": 0.1}),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired)", {"FY2025": 8.3, "FY2024": 4.2, "FY2023": 1.2, "FY2022": 4.8, "FY2021": 5.1, "FY2020": 4.8, "FY2019": 7.3}),
    ("DATA", "Post Model Adjustment", {"FY2025": 0.2, "FY2024": -0.1, "FY2023": 0.4, "FY2022": 0.8}),
    ("TOTAL", "Total provision for impairment", {"FY2025": 13.8, "FY2024": 7.7, "FY2023": 6.0, "FY2022": 8.6, "FY2021": 8.4, "FY2020": 7.9, "FY2019": 9.8, "FY2018": 3.7, "FY2017": 6.4, "FY2016": 10.0, "FY2015": 7.6, "FY2014": 5.8}),
    ("SECTION", "Loans and advances by product, at amortised cost (before hedge FV adjustment / retirement mortgages FVTPL)", {}),
    ("DATA", "Retail", {"FY2025": 1371.8, "FY2024": 1315.9, "FY2023": 1234.9, "FY2022": 1140.0, "FY2021": 679.0}),
    ("DATA", "Commercial (real estate)", {"FY2025": 218.1, "FY2024": 189.7, "FY2023": 170.4, "FY2022": 182.2, "FY2021": 233.9}),
    ("DATA", "Portfolio Buy-to-Let", {"FY2025": 37.3, "FY2024": 70.3, "FY2023": 74.7, "FY2022": 76.5, "FY2021": 70.5}),
    ("DATA", "Motor receivables", {"FY2025": 183.1, "FY2024": 96.3}),
    ("DATA", "Amounts owed from parent and fellow subsidiaries", {"FY2021": 0.4}),
]

# ---------------------------------------------------------------
# Sheet: Cash Flow Statement (exemption note in place of line items)
# ---------------------------------------------------------------
rows = [
    ("SECTION", "No Statement of Cash Flows is published by this entity in any year", {}),
    ("DATA", "See the note below for the FRS 101 exemption this entity relies on every year, and why this "
             "workbook is built as a Pillar-3-only variant.", {}),
]

bw.add_cash_flow_sheet(
    title="Julian Hodge Bank Limited — Cash Flow Statement",
    subtitle="Not applicable — this entity takes the FRS 101 cash-flow-statement disclosure exemption every year. See source note below.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=260,
    unit_suffix="",
)

bw.add_asset_quality_sheet(
    title="Julian Hodge Bank Limited — Asset Quality",
    subtitle="Portfolio-wide IFRS 9 Stage 1/2/3 impairment provision roll-forward (Note 13/14). £m.",
    rows=asset_quality_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nDATA QUALITY FLAG: AR2025's own Note 13 table prints its 2025-year closing row as \"At 30 September 2024\" "
        "and its 2024-year closing row as \"At 30 September 2023\" - both appear to be an off-by-one-year label carried "
        "over from an earlier template (each closing row's own figures follow arithmetically from that block's own "
        "opening row and match the FOLLOWING year's contemporaneous report exactly), so the closing rows are treated "
        "here as FY2025 and FY2024 respectively, not as literally labelled. No gross-exposure-by-IFRS-9-stage table "
        "exists at portfolio level in any year - only the impairment PROVISION is broken out by stage portfolio-wide; "
        "gross exposure by stage is only disclosed for the Commercial/PBTL/Motor segments separately (not for Retail, "
        "the largest segment), so a full gross-by-stage table is not reconstructable without assuming Retail's split."
    ),
    first_col_width=76,
    source_height=380,
    unit_suffix=" (£m)",
    years=PILLAR3_YEARS,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None, first_col_width=52, source_height=170):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=first_col_width,
                        source_height=source_height, years=P3_DISCLOSURE_YEARS)


# ---------------------------------------------------------------
# KM1 Key Metrics (KM1-018, 2026-09-16)
#
# Hodge publishes the key-metrics template in SIX editions, FY2018 to FY2023,
# and it changes TEMPLATE GENERATION in the middle of that run. The two
# generations are kept as two separate blocks on this sheet and are
# deliberately NOT merged, for the same reason the map forbids merging the two
# sides of the 1 January 2022 leverage basis break: they are different tables
# with different row sets, different captions and a different numbering
# convention, and running them down one row would assert a continuity Hodge
# never published.
#
#   BLOCK A - "3 Key Regulatory Metrics", FY2022 and FY2023 editions. Numbered
#       UK KM1, footed "Source: Template UK KM1". Carries UK11a, UK16a, UK16b
#       and row 12, and its leverage rows are on the post-1-Jan-2022
#       EXCLUDING-central-bank-claims basis.
#   BLOCK B - "Key metrics" / "Key Metrics", FY2018 to FY2021 editions.
#       UNNUMBERED, and it is the BCBS Basel III KM1 rather than the UK one:
#       it prints a "Tier 2 (£m)" row the UK template does not have, uses
#       "Total of bank CET1 specific buffer requirements" where the UK
#       template says "Combined buffer requirement", has no UK11a / row 12 /
#       UK16a / UK16b rows, and its leverage rows are the old
#       INCLUDING-central-bank-claims measure. Under the map's row-set test it
#       is still unmistakably the template (own funds, RWA, ratios, buffers,
#       leverage, LCR and - from FY2020 - NSFR), so it is transcribed.
#
# Every cell comes from the edition in which that year is the REPORTING year,
# never from the next edition's comparative. That matters twice here:
#   - FY2021 CET1 is 143.8 in the FY2021 edition and 144 in the FY2022
#     edition's comparative; 143.8 is used.
#   - FY2021's leverage rows are 1,732.2 / 8.3% on its own edition's
#     including-central-banks basis, while the FY2022 edition restates that
#     comparative to 1,320 / 10.9% on the excluding basis. Both are real; the
#     two bases sit in different blocks and are not merged.
#
# FY2024 and FY2025 have NO Pillar 3 document at all: FY2024 is an ordinary
# gap, FY2025 is covered by the bank's SDDT modification (PRA Rule 3.1,
# effective 18 February 2025), so no FY2025 KM1 will ever exist. FY2017 and
# earlier are blank because those editions print no key-metrics table of any
# kind - FY2017's figures exist only as the FY2018 edition's comparative.
# ---------------------------------------------------------------
km1_rows = [
    ("SECTION", "UK KM1 template - \"3 Key Regulatory Metrics\" (FY2022 and FY2023 editions; row numbers as Hodge prints them)", {}),
    ("SECTION", "Available own funds (amounts) (£m)", {}),
    ("DATA", "1    Common Equity Tier 1 (CET1)", {"FY2023": 172.9, "FY2022": 177}),
    ("DATA", "2    Tier 1", {"FY2023": 172.9, "FY2022": 177}),
    ("DATA", "Total capital    [Hodge prints this row WITHOUT the template's row number 3]",
     {"FY2023": 172.9, "FY2022": 177}),
    ("SECTION", "Risk-weighted exposure amounts RWEA (£m)", {}),
    ("DATA", "4    Total RWEA", {"FY2023": 704.7, "FY2022": 705}),
    ("SECTION", "Capital ratios (as a percentage of RWEA)", {}),
    ("DATA", "5    Common Equity Tier 1 ratio", {"FY2023": "24.5%", "FY2022": "25.2%"}),
    ("DATA", "6    Tier 1 ratio", {"FY2023": "24.5%", "FY2022": "25.2%"}),
    ("DATA", "7    Total capital ratio", {"FY2023": "24.5%", "FY2022": "25.2%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of RWEA)", {}),
    ("DATA", "8    Capital conservation buffer", {"FY2023": "2.5%", "FY2022": "2.5%"}),
    ("DATA", "9    Institution specific countercyclical capital buffer", {"FY2023": "2.0%", "FY2022": "0.0%"}),
    ("DATA", "11    Combined buffer requirement", {"FY2023": "4.5%", "FY2022": "2.5%"}),
    ("DATA", "UK11a    Overall capital requirements", {"FY2023": "16.0%", "FY2022": "15.9%"}),
    ("DATA", "12    CET1 available after meeting the total SREP own funds requirements",
     {"FY2023": "13.0%", "FY2022": "9.3%"}),
    ("SECTION", "Leverage Ratio", {}),
    ("DATA", "13    Total leverage Ratio exposure measure (£m)", {"FY2023": 1649.9, "FY2022": 1624}),
    ("DATA", "14    Leverage Ratio", {"FY2023": "10.5%", "FY2022": "10.9%"}),
    ("SECTION", "Liquidity Coverage Ratio*", {}),
    ("DATA", "15    Total HQLA after haircuts (£m)", {"FY2023": 230.4, "FY2022": 334}),
    ("DATA", "UK16a    Cash outflows - Total weighted value (£m)", {"FY2023": 141.0, "FY2022": 137}),
    ("DATA", "UK16b    Cash inflows - Total weighted value (£m)", {"FY2023": 10.7, "FY2022": 4}),
    ("DATA", "16    Total net cash outflows (adjusted value) (£m)", {"FY2023": 130.2, "FY2022": 133}),
    ("DATA", "17    Liquidity coverage ratio (%)", {"FY2023": "176.9%", "FY2022": "252%"}),
    ("SECTION", "Net Stable Funding Ratio", {}),
    ("DATA", "18    Total available stable funding", {"FY2023": 1721.9, "FY2022": 1549}),
    ("DATA", "19    Total required stable funding", {"FY2023": 1144.2, "FY2022": 1085}),
    ("DATA", "20    NSFR ratio (%)", {"FY2023": "150.5%", "FY2022": "143%"}),

    ("SECTION", "Basel III (BCBS) KM1 - \"Key metrics\" (FY2018 to FY2021 editions; Hodge prints no row numbers in these, and none have been added)", {}),
    ("SECTION", "Available capital (amounts)", {}),
    ("DATA", "Common Equity Tier 1 (CET1) (£m)",
     {"FY2021": 143.8, "FY2020": 136.4, "FY2019": 156.6, "FY2018": 168.0}),
    ("DATA", "Tier 1 (£m)", {"FY2021": 143.8, "FY2020": 136.4, "FY2019": 156.6, "FY2018": 168.0}),
    ("DATA", "Tier 2 (£m)    [printed \"-\" in every one of the four editions - left blank, not zeroed]", {}),
    ("DATA", "Total capital (£m)", {"FY2021": 143.8, "FY2020": 136.4, "FY2019": 156.6, "FY2018": 168.0}),
    ("SECTION", "Risk weighted assets (amounts)", {}),
    ("DATA", "Total risk-weighted assets (RWA) (£m)",
     {"FY2021": 711.0, "FY2020": 693.8, "FY2019": 681.9, "FY2018": 754.6}),
    ("SECTION", "Risk-based capital ratios as a percentage of RWA", {}),
    ("DATA", "Common Equity Tier 1 ratio (%)",
     {"FY2021": "20.2%", "FY2020": "19.7%", "FY2019": "23.0%", "FY2018": "22.3%"}),
    ("DATA", "Tier 1 ratio (%)", {"FY2021": "20.2%", "FY2020": "19.7%", "FY2019": "23.0%", "FY2018": "22.3%"}),
    ("DATA", "Total capital ratio (%)",
     {"FY2021": "20.2%", "FY2020": "19.7%", "FY2019": "23.0%", "FY2018": "22.3%"}),
    ("SECTION", "Additional CET1 buffer requirements as a percentage of RWA", {}),
    ("DATA", "Capital conservation buffer requirement (%)",
     {"FY2021": "2.50%", "FY2020": "2.50%", "FY2019": "2.50%", "FY2018": "1.88%"}),
    ("DATA", "Countercyclical buffer requirement (%)",
     {"FY2021": "0.00%", "FY2020": "0.00%", "FY2019": "1.00%", "FY2018": "0.50%"}),
    ("DATA", "Total of bank CET1 specific buffer requirements (%)",
     {"FY2021": "2.50%", "FY2020": "2.50%", "FY2019": "3.50%", "FY2018": "2.38%"}),
    ("SECTION", "Basel III leverage ratio (INCLUDING claims on central banks - the pre-1-January-2022 measure)", {}),
    ("DATA", "Total Basel III leverage ratio exposure measure (£m)",
     {"FY2021": 1732.2, "FY2020": 1423.5, "FY2019": 1393.2, "FY2018": 1412.2}),
    ("DATA", "Basel III leverage ratio (%)",
     {"FY2021": "8.3%", "FY2020": "9.6%", "FY2019": "11.2%", "FY2018": "11.9%"}),
    ("SECTION", "Liquidity Coverage Ratio", {}),
    ("DATA", "Total HQLA after haircuts (£m)    [FY2018 edition prints \"Total HQLA (£m)\", without \"after haircuts\"]",
     {"FY2021": 479.5, "FY2020": 196.4, "FY2019": 346.4, "FY2018": 245.2}),
    ("DATA", "Total net cash outflow (£m)", {"FY2021": 137.1, "FY2020": 72.0, "FY2019": 67.0, "FY2018": 103.5}),
    ("DATA", "LCR ratio (%)    [FY2021 edition prints the row as \"LCR (%)\"]",
     {"FY2021": "349.6%", "FY2020": "272.9%", "FY2019": "516.9%", "FY2018": "236.9%"}),
    ("SECTION", "Net Stable Funding Ratio    [this whole block is absent from the FY2018 and FY2019 editions]", {}),
    ("DATA", "Total available stable funding", {"FY2021": 1551.0, "FY2020": 1226.2}),
    ("DATA", "Total required stable funding", {"FY2021": 922.7, "FY2020": 793.3}),
    ("DATA", "NSFR", {"FY2021": "168.1%", "FY2020": "154.6%"}),
]

KM1_SOURCES = (
    "Sources - Julian Hodge Bank Limited's own key-metrics table in each year's Pillar 3 "
    "Disclosures, from the Bank's own Financial Information page "
    "(https://hodgebank.co.uk/hodge/financial-information/). Page numbers below are the PRINTED "
    "folio on the page carrying the table:\n"
    f"FY2023: Hodge Bank Pillar 3 Disclosures - Period ended 30 September 2023, \"3 Key Regulatory "
    f"Metrics\", printed p.10, column headed 2023, footed \"Source: Template UK KM1\" - {P3_2023_URL}\n"
    f"FY2022: Hodge Bank Pillar 3 Disclosures - Period ended 30 September 2022, \"3 Key Regulatory "
    f"Metrics\", printed p.13, column headed 2022, footed \"Source: Template UK KM1\" - {P3_2022_URL}\n"
    f"FY2021: Hodge Bank Pillar 3 Disclosures - Period ended 30 September 2021, \"Key Metrics\", "
    f"printed p.16, column headed 30 September 2021 - {P3_2021_URL}\n"
    f"FY2020: Julian Hodge Bank Limited Pillar 3 Disclosures - Period ended 30 September 2020, "
    f"\"3. Key Regulatory Metrics\", printed p.16, column headed 30 September 2020 - {P3_2020_URL}\n"
    f"FY2019: Julian Hodge Bank Limited Pillar 3 Disclosures - Period ended 31 October 2019, "
    f"\"4. Key Regulatory Metrics\" / \"Key metrics\", printed p.9, column headed 31 October 2019 - "
    f"{P3_2019_URL}\n"
    f"FY2018: Julian Hodge Bank Limited Pillar 3 Disclosures - Period ended 31 October 2018, "
    f"\"4. Key Regulatory Metrics\" / \"Key metrics\", printed p.9, column headed 31 October 2018 - "
    f"{P3_2018_URL}\n"
    "KM1 presentation notes:\n"
    "• ENTITY: Julian Hodge Bank Limited (trading as Hodge Bank), solo. Every edition's table is "
    "headed \"for JHB\" or \"for the Bank\"; no group or consolidated column is printed anywhere, "
    "so there is no basis ambiguity to resolve.\n"
    "• TWO TEMPLATE GENERATIONS, SHOWN AS TWO BLOCKS AND NEVER MERGED. The FY2022 and FY2023 "
    "editions print the numbered UK KM1 and foot it \"Source: Template UK KM1\". The FY2018-FY2021 "
    "editions print the BCBS Basel III KM1 instead: unnumbered, with a \"Tier 2 (£m)\" row the UK "
    "template does not contain, \"Total of bank CET1 specific buffer requirements\" in place of "
    "\"Combined buffer requirement\", no UK11a / row 12 / UK16a / UK16b rows, and leverage rows on "
    "the old INCLUDING-claims-on-central-banks measure. Running the two down one set of rows would "
    "assert a continuity Hodge never published, so they are kept apart - the same treatment the map "
    "requires for the 1 January 2022 leverage basis break, which is in fact exactly what separates "
    "them.\n"
    "• EACH YEAR FROM ITS OWN EDITION. Two visible consequences: (1) FY2021 CET1/Tier 1/Total "
    "capital are 143.8 here, from the FY2021 edition, where the FY2022 edition's comparative "
    "column rounds them to 144 and its RWA comparative to 711 (from 711.0); (2) FY2021's leverage "
    "exposure and ratio are 1,732.2 and 8.3% here, on its own edition's including-central-banks "
    "basis, where the FY2022 edition restates the same comparative to 1,320 and 10.9% on the "
    "excluding basis. Both restatements are real and neither is applied.\n"
    "• DIVERGENCE FROM THE NSFR METRIC SHEET, DELIBERATE AND EXPLAINED: that sheet carries an "
    "FY2019 NSFR of 217.6%, which this sheet leaves blank. 217.6% is the FY2020 edition's 31 "
    "October 2019 COMPARATIVE column; the FY2019 edition itself prints no Net Stable Funding Ratio "
    "block at all (its table ends after the LCR rows), and neither does the FY2018 edition. A "
    "reproduction of the FY2019 table therefore cannot carry an NSFR row, so the FY2019 and FY2018 "
    "NSFR cells are blank here rather than back-filled from the following edition.\n"
    "• A DASH IS NOT A ZERO: the \"Tier 2 (£m)\" row is printed \"-\" in all four Basel III-era "
    "editions and is left BLANK here. The FY2018 edition prints its FY2017 countercyclical buffer "
    "comparative as \"-%\", the same glyph - that column is not on this sheet in any case, since "
    "the FY2017 edition prints no key-metrics table.\n"
    "• PRECISION AND LABEL DRIFT, REPRODUCED: the FY2022 edition prints amounts as whole £m (177, "
    "705, 1,624) where FY2023 prints one decimal (172.9, 704.7, 1,649.9); FY2022 prints buffers as "
    "\"2.5%\" where the Basel III-era editions print \"2.50%\"; FY2022's row 4 is captioned \"Total "
    "risk-weighted exposures amounts\" and FY2023's \"Total RWEA\" (FY2023's wording labels the "
    "row); FY2022's row 9 is \"Institution specific countercyclical buffer\" and FY2023's adds "
    "\"capital\" (FY2023's wording labels the row). The FY2020 edition lower-cases \"Basel III "
    "leverage ratio\" where FY2021 capitalises it.\n"
    "• ROW 3 IS UNNUMBERED IN THE SOURCE: both UK KM1 editions print \"Total capital\" with no row "
    "number in the number column, while numbering 1, 2 and 4 normally. Reproduced as printed rather "
    "than silently corrected to \"3\". Neither edition prints rows UK 7a-7d, UK 8a, UK 9a, 10 or UK "
    "10a at all.\n"
    "• LCR BASIS FOOTNOTE, HODGE'S OWN: both UK KM1 editions foot the table \"*=year end value for "
    "LCR related metrics whereas detailed analysis at LIQ1 reports average values as defined in the "
    "table\", so rows 15-17 are point-in-time, not the 12-month average most filers print. The "
    "asterisk is kept on the section heading.\n"
    "• FY2024 AND FY2025 ARE BLANK FOR DIFFERENT REASONS. FY2024 is an ordinary gap: no Pillar 3 "
    "document was published for the year ended 30 September 2024, and its capital figures on the "
    "metric sheets come from Note 32 of the FY2024 Annual Report, which is a statutory source and "
    "is deliberately NOT back-filled into this template. FY2025 is NOT APPLICABLE rather than "
    "missing: the Bank's SDDT modification (PRA Disclosure Rule 3.1, effective 18 February 2025) "
    "removed its Pillar 3 duty before the 30 September 2025 year-end, so no FY2025 KM1 will ever "
    "exist. FY2017 and earlier are blank because no edition before FY2018 prints a key-metrics "
    "table of any kind; FY2017's figures survive only as the FY2018 edition's comparative column "
    "and are not transcribed here.\n"
    "• LATEST-EDITION CHECK, 2026-09-16: Hodge's own Financial Information page "
    "(https://hodgebank.co.uk/hodge/financial-information/) was fetched directly and read in full. "
    "Newest Pillar 3 listed = \"Pillar 3 Disclosure 2023\" (the FY2023 document already cited "
    "here); newest Annual Report listed = \"Annual Report and Financial Statements, 30 September "
    "2025\" (Hodge-AR-28.01.26.pdf), which this workbook already carries as its FY2025 source. "
    "The page lists an unbroken Pillar 3 series 2010-2023 and simply stops - consistent with the "
    "SDDT modification above. None newer."
)

bw.add_km1_sheet(
    title="Julian Hodge Bank Limited (Hodge Bank) - KM1 Key Metrics",
    subtitle="The Bank's own published key-metrics template, reproduced in Hodge's row order, row numbers, "
             "labels and printed precision. Solo basis; amounts in £m, ratios as printed. Shown as TWO blocks "
             "because Hodge changes template generation mid-series: the numbered UK KM1 in its FY2022 and "
             "FY2023 editions, and the unnumbered BCBS Basel III KM1 in FY2018-FY2021. The two are not merged "
             "- their leverage rows alone sit on opposite sides of the 1 January 2022 basis break. FY2024 has "
             "no Pillar 3 document and FY2025 is covered by the Bank's SDDT modification; see the source note.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=76,
    source_height=460,
    years=["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018"],
)

metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 162.8, "FY2024": 166.2, "FY2023": 172.9, "FY2022": 177, "FY2021": 143.8, "FY2020": 136.4, "FY2019": 156.6, "FY2018": 168.0, "FY2017": 149.3, "FY2016": 129.1})],
    p3_sources(),
    note="FY2021's own report (P3 2021) shows CET1 = 143.8; the following year's Pillar 3 document (P3 2022) "
         "restates the FY2021 comparative to 144 (rounding to whole £m from that document's own precision) - "
         "each year's own originally-published figure is used per this project's convention. FY2015-FY2010 not "
         "shown: this bank's own Pillar 3 documents for those six years pre-date the CET1 concept (still reporting "
         "under Basel II Pillar 1 - 'Tier 1 capital' and 'Total capital resources' only, no CRD IV capital tiers). "
         "A Basel II 'Total Tier 1 capital' is not a CET1 figure and is deliberately not placed here. See the "
         "Total Capital sheet for those years' Basel II 'Total capital resources' figures instead, and this "
         "sheet's sources for the full pre-CRD IV note. The FY2013-FY2010 columns are blank BY DESIGN and "
         "well-sourced, not unresearched: all four documents were located live, read in full and are cited.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "17.5%", "FY2024": "19.8%", "FY2023": "24.5%", "FY2022": "25.2%", "FY2021": "20.2%", "FY2020": "19.7%", "FY2019": "23.0%", "FY2018": "22.3%", "FY2017": "21.1%", "FY2016": "19.2%"})],
    p3_sources(),
    note="FY2015-FY2010 are blank by design, not unresearched. All six years' Pillar 3 documents were located, "
         "read in full and are cited in this sheet's sources. They are Basel II: none defines CET1, none "
         "discloses a risk-weighted-asset amount to serve as a denominator, and none prints a capital ratio of "
         "any kind. There is therefore no ratio to transcribe, and one is deliberately not derived by grossing "
         "the disclosed Pillar 1 capital requirement up by 12.5. See the Total RWAs sheet note and the pre-CRD "
         "IV note in this sheet's sources.",
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 162.8, "FY2024": 166.2, "FY2023": 172.9, "FY2022": 177, "FY2021": 143.8, "FY2020": 136.4, "FY2019": 156.6, "FY2018": 168.0, "FY2017": 149.3, "FY2016": 129.1})],
    p3_sources(),
    note="Tier 1 = CET1 every year (no AT1 instruments in issue - 'Hold all its capital in the form of Common "
         "Equity Tier 1 and Tier 2 capital', and Tier 2 = nil every year per the Pillar 3 documents). FY2024/FY2025 "
         "not separately labelled 'Tier 1' in the Annual Report's brief capital note but equal to CET1 by the same "
         "pattern confirmed directly in FY2021-FY2023. FY2015-FY2010: pre-CRD IV Basel II regime - see CET1 Capital "
         "sheet note; for those six years 'Total Tier 1 capital' as reported was GBP118.6m (FY2015), GBP117.1m "
         "(FY2014), GBP113.7m (FY2013), GBP111.1m (FY2012), GBP109.7m (FY2011) and GBP108.1m (FY2010), each after "
         "that edition's deduction for investments in subsidiaries (GBP16.0m throughout). Each differs from the "
         "'Total capital resources' shown on the Total Capital sheet because every one of those years DID hold a "
         "small amount of Tier 2 (general provisions, less a revaluation reserve deduction in FY2013/FY2012/FY2011) "
         "- shown here only for completeness, not populated as a data column to avoid conflating Basel II Tier 1 "
         "with CRD IV Tier 1. The FY2013-FY2010 figures were added 2026-09-16 (HD-080) on exactly the same "
         "prose-only footing the FY2015/FY2014 pair already had, deliberately keeping one consistent treatment "
         "across the whole Basel II run rather than promoting the new years to a data column.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "17.5%", "FY2024": "19.8%", "FY2023": "24.5%", "FY2022": "25.2%", "FY2021": "20.2%", "FY2020": "19.7%", "FY2019": "23.0%", "FY2018": "22.3%", "FY2017": "21.1%", "FY2016": "19.2%"})],
    p3_sources(),
    note="Equal to CET1 ratio every year - see Tier 1 Capital sheet note. FY2015-FY2010 blank by design: no RWA "
         "denominator and no capital ratio is published in any of those six Basel II editions, and none is "
         "derived - see the CET1 Ratio and Total RWAs sheet notes.",
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 162.8, "FY2024": 166.2, "FY2023": 172.9, "FY2022": 177, "FY2021": 143.8, "FY2020": 136.4, "FY2019": 156.6, "FY2018": 168.0, "FY2017": 149.5, "FY2016": 129.3, "FY2015": 122.4, "FY2014": 118.8,
       "FY2013": 114.3, "FY2012": 114.1, "FY2011": 114.8, "FY2010": 114.7})],
    p3_sources(),
    note="Equal to CET1/Tier 1 FY2016-FY2025 - the Bank holds no Tier 2 capital in those years. FY2015-FY2010: "
         "these figures are Basel II 'Total capital resources' (Tier 1 after the deduction for investments in "
         "subsidiaries, plus a small Tier 2 add-back for eligible general provisions, net of a revaluation "
         "reserve deduction in FY2013/FY2012/FY2011) - each is a total the source document states directly, none "
         "is summed or derived here. They are NOT directly comparable to the CRD IV 'Total capital' figures "
         "shown FY2016 onward, though presented on the same row per this project's convention of showing each "
         "year's own headline total-capital figure. FY2013-FY2010 added 2026-09-16 (HD-080) from the four "
         "newly-located Basel II editions; FY2015/FY2014 were already on this basis before that, so the four new "
         "years extend an existing Basel II run rather than introducing a new mixed basis. This is the ONLY "
         "metric sheet those four years populate - see the pre-CRD IV note in this sheet's sources for why every "
         "other sheet is deliberately blank for them.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "17.5%", "FY2024": "19.8%", "FY2023": "24.5%", "FY2022": "25.2%", "FY2021": "20.2%", "FY2020": "19.7%", "FY2019": "23.0%", "FY2018": "22.3%", "FY2017": "21.2%", "FY2016": "19.2%"})],
    p3_sources(),
    note="FY2015-FY2010 blank by design even though the NUMERATOR is known for all six years (the Total Capital "
         "sheet carries each year's disclosed 'Total capital resources'). The Basel II editions publish no "
         "risk-weighted-asset amount at all, so there is no denominator, and computing one from the Pillar 1 "
         "capital requirement would be back-solving a figure no document states. See the CET1 Ratio and Total "
         "RWAs sheet notes.",
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted assets / exposure amount", {"FY2025": 930.2, "FY2024": 841.1, "FY2023": 704.7, "FY2022": 705, "FY2021": 711.0, "FY2020": 693.8, "FY2019": 681.9, "FY2018": 754.6, "FY2017": 706.3, "FY2016": 672.8})],
    p3_sources(),
    note="FY2021's own report (P3 2021) shows RWA = 711.0; the FY2022 Pillar 3 document's FY2021 comparative "
         "restates this to 711 (rounding only, immaterial) - each year's own originally-published figure is used. "
         "FY2015-FY2010 not available, and this is the most important gap to understand in the historical "
         "columns: those years' Pillar 3 documents pre-date CRD IV Pillar 3 RWA disclosure for this bank. A "
         "search for 'risk weighted'/'risk-weighted' returns ZERO hits in the FY2013, FY2012, FY2011 and FY2010 "
         "documents - no risk-weighted-asset amount is printed anywhere in any of them, and no capital ratio is "
         "either. What each gives instead is a Basel II 'Pillar 1 capital requirement', which is CAPITAL, not "
         "RWA: FY2015 GBP42.6m, FY2014 GBP36.3m, FY2013 GBP35.3m (credit risk 34.9 + operational risk 0.4), "
         "FY2012 GBP36.8m (36.0 + 0.8), FY2011 GBP38.9m (37.7 + 1.2), FY2010 GBP41.5m (40.2 + 1.3). No RWA is "
         "shown for any of these years rather than backing one out by grossing those figures up via an assumed "
         "8% minimum ratio - a multiplication none of the source documents itself states or invites. Note the "
         "contrast with the FY2016 entry on the RWA Breakdown sheet, where a x12.5 derivation WAS made and is "
         "labelled as derived; that year is CRD IV and its document states the ratio the derivation reproduces, "
         "which is what makes it checkable. Nothing equivalent exists pre-FY2014, so nothing is derived there.",
)

# ---------------------------------------------------------------
# RWA Breakdown - FY2023-FY2017 sourced from each year's own (or, for
# FY2017, the following year's) standalone Pillar 3 document's
# "Risk Type Breakdown"/"Overview of RWA" (UK OV1-style) table;
# FY2016 only has a coarser 2-category Pillar 1 CAPITAL REQUIREMENT
# table (no OV1-style RWA-by-risk-type table), so its figures are
# DERIVED via x12.5 (Pillar 1 capital required = 8% of RWA under CRR
# Article 92) and kept in their own SECTION block, not blended with
# the as-disclosed years above; FY2025/FY2024 have no standalone
# Pillar 3 document (see BASIS_NOTE) and their Annual Report's brief
# "Capital risk management" note gives only the aggregate Total RWAs
# figure (already shown on that sheet), not a category split.
# ---------------------------------------------------------------
rwa_breakdown_rows = [
    ("SECTION", "Risk type breakdown (as disclosed) - Pillar 3 \"Risk Type Breakdown\"/\"Overview of RWA\" table", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2023": 629.2, "FY2022": 644, "FY2021": 639.9, "FY2020": 627.3, "FY2019": 626.8, "FY2018": 699.4, "FY2017": 661.5}),
    ("DATA", "Counterparty credit risk (CCR) - includes CVA memo below for FY2023/FY2022 (this year's own template "
             "shows CVA as a memo item within CCR, not a separately additive line); FY2021-FY2017's own templates "
             "show CVA as its own separately additive line instead (see next-but-one row)",
     {"FY2023": 2.7, "FY2022": 1, "FY2021": 4.6, "FY2020": 4.2, "FY2019": 2.1, "FY2018": 4.0, "FY2017": 4.3}),
    ("DATA", "Of which: Credit valuation adjustment (CVA) - memo only for FY2023/FY2022, already included in CCR above, not separately additive",
     {"FY2023": 0.2, "FY2022": 0}),
    ("DATA", "Credit valuation adjustment (CVA) - shown as its own separately additive risk type in FY2021-FY2017's own Pillar 3 templates "
             "(unlike the FY2023/FY2022 memo treatment above); Market risk is a separate nil/blank line in the FY2020-FY2017 source tables "
             "and is not shown as its own row here since it is nil in every disclosed year",
     {"FY2021": 0.8, "FY2020": 2.3, "FY2019": 2.5, "FY2018": 5.0, "FY2017": 5.7}),
    ("DATA", "Operational risk", {"FY2023": 58.9, "FY2022": 44, "FY2021": 36.5, "FY2020": 36.2, "FY2019": 34.0, "FY2018": 29.9, "FY2017": 16.5}),
    ("DATA", "Amounts below the threshold for deduction (250% risk weight)", {"FY2023": 13.9, "FY2022": 16, "FY2021": 29.2, "FY2020": 23.8, "FY2019": 16.5, "FY2018": 16.3, "FY2017": 18.3}),
    ("TOTAL", "Total risk-weighted exposure amount", {"FY2023": 704.7, "FY2022": 705, "FY2021": 711.0, "FY2020": 693.8, "FY2019": 681.9, "FY2018": 754.6, "FY2017": 706.3}),
    ("SECTION", "Pillar 1 capital requirement x 12.5 (derived from disclosed capital requirement - see sources note)", {}),
    ("DATA", "Credit risk (including CCR/CVA - not separately itemised in this year's own document)", {"FY2016": 661.25}),
    ("DATA", "Operational risk", {"FY2016": 11.25}),
    ("TOTAL", "Total risk-weighted exposure amount (derived)", {"FY2016": 672.5}),
]

bw.add_rwa_breakdown_sheet(
    title="Julian Hodge Bank Limited — RWA Breakdown",
    subtitle="FY2023-FY2017 as disclosed (Pillar 3 \"Risk Type Breakdown\"/\"Overview of RWA\" table); FY2016 derived "
             "from the disclosed Pillar 1 capital requirement x 12.5 (a coarser 2-category split - see SECTION blocks "
             "and source note). FY2025/FY2024/FY2015/FY2014: no category-level RWA breakdown was located - see source "
             "note. £m.",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources(
        "\nRWA Breakdown-specific sources (in addition to the Total RWAs sources above):\n"
        "FY2023: Hodge Bank Pillar 3 Disclosures - Period ended 30 September 2023, \"Risk Type Breakdown\" table, "
        f"p.14 - {P3_2023_URL}\n"
        "FY2022: Hodge Bank Pillar 3 Disclosures - Period ended 30 September 2022, \"Risk Type Breakdown\" table, "
        f"p.17 - {P3_2022_URL}\n"
        "FY2021: Hodge Bank Pillar 3 Disclosures - Period ended 30 September 2021, \"Risk Type Breakdown\" table, "
        f"p.21 - {P3_2021_URL}\n"
        f"FY2020: Julian Hodge Bank Limited Pillar 3 Disclosures - Period ended 30 September 2020, \"Overview of "
        f"RWA\" table (own-year column), p.23 - {P3_2020_URL}\n"
        f"FY2019: Julian Hodge Bank Limited Pillar 3 Disclosures - Period ended 31 October 2019, \"Overview of RWA\" "
        f"table (own-year column), p.14 - {P3_2019_URL}\n"
        f"FY2018: Julian Hodge Bank Limited Pillar 3 Disclosures - Period ended 31 October 2018, \"Overview of RWA\" "
        f"table (own-year column), p.14 - {P3_2018_URL}\n"
        "FY2017: this year's own Pillar 3 document only discloses a coarser Pillar 1 capital-requirement-by-exposure-"
        "class table (no risk-type RWA split); the FY2017 figures above are instead the FY2017 comparator column of "
        f"the FOLLOWING year's \"Overview of RWA\" table - Julian Hodge Bank Limited Pillar 3 Disclosures - Period "
        f"ended 31 October 2018, \"Overview of RWA\" table, FY2017 comparator column, p.14 - {P3_2018_URL} - which "
        "reconciles exactly (706.3) to the Total RWAs sheet's own FY2017 figure sourced from that year's own report.\n"
        "FY2016: no OV1-style RWA-by-risk-type table exists in this year's own Pillar 3 document (or the following "
        "year's) - only a 2-category \"Pillar 1 Capital Requirement\" table (Total Credit Risk, which bundles in CCR/"
        "CVA per this document's own categorisation with no separate line for either, and Operational risk - "
        "standardised approach). DERIVED (not disclosed): each category's Pillar 1 capital requirement x 12.5 (= "
        "divided by 8%, the CRR Article 92 Pillar 1 minimum ratio) - Julian Hodge Bank Limited Pillar 3 Disclosures - "
        f"Period ended 31 October 2016, \"6.1 Pillar 1 Capital Requirement\" table, p.17 - {P3_2016_URL} (Credit Risk "
        "capital 52.9 x 12.5 = 661.25; Operational risk capital 0.9 x 12.5 = 11.25; derived total 672.5 reconciles "
        "to within 0.3 - immaterial source-table rounding before x12.5 - of the Total RWAs sheet's own FY2016 figure "
        "of 672.8). Market risk is not itemised in this document at all for FY2016 (assumed nil, consistent with "
        "every disclosed later year showing nil/blank market risk, but not confirmed for FY2016 itself).\n"
        "FY2025/FY2024: Not publicly disclosed at category level - no standalone Pillar 3 document is published for "
        "these years (see BASIS_NOTE above); each year's own Annual Report 'Capital risk management' note gives only "
        "Total RWAs and CET1/capital ratios, no risk-type split - already shown on the Total RWAs sheet. "
        "Re-confirmed 2026-09-12: a Wayback CDX scan of hodgebank.co.uk's full 2025-2026 crawl history found no "
        "newly-dated Pillar 3 filename beyond the FY2023 document already cited above; the bank's own regulatory-"
        "disclosures pages returned HTTP 403 (bot-blocked) on direct fetch, so this remains an access-limited "
        "re-confirmation, not a from-scratch guarantee no such document exists.\n"
        "FY2015/FY2014: no RWA figure of any kind is disclosed for these two years (pre-CRD IV regime) - see the "
        "Total RWAs sheet note.\n"
        "FY2013-FY2010 ARE DELIBERATELY NOT COLUMNS ON THIS SHEET, even though all four of those years' Pillar 3 "
        "documents were located live and read in full in 2026-09-16's HD-080 pass. This sheet (and the Asset "
        "Quality sheet) stay pinned to the FY2014 window while the 11 capital metric sheets extend back to "
        "FY2010, because there is literally nothing pre-FY2014 to put here: none of the four Basel II editions "
        "discloses a risk-weighted-asset amount at all, in total or by risk type. Adding the columns would add "
        "four entirely empty ones. The four editions' Pillar 1 CAPITAL requirements are recorded instead on the "
        "Total RWAs sheet's note, as capital, deliberately never multiplied by 12.5 into an RWA no document states."
    ),
    first_col_width=90,
    source_height=460,
    unit_suffix=" (£m)",
    years=PILLAR3_YEARS,
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total exposure measure EXCLUDING claims on central banks (£m) (UK LRCom row UK-24b / UK KM1 row 13; "
         "the FY2022-onward basis)",
         {"FY2023": 1649.9, "FY2022": 1624, "FY2021": 1320}),
        ("Leverage ratio EXCLUDING claims on central banks (%) (UK LRCom row 25 / UK KM1 row 14; "
         "the FY2022-onward basis)",
         {"FY2023": "10.5%", "FY2022": "10.9%", "FY2021": "10.9%"}),
        ("Total exposure measure INCLUDING claims on central banks (£m) (UK LRCom row 24 for FY2022-FY2023; "
         "the Basel III/CRR exposure measure as originally reported FY2016-FY2021)",
         {"FY2023": 1803.7, "FY2022": 1852, "FY2021": 1732.2, "FY2020": 1423.5, "FY2019": 1393.2, "FY2018": 1412.2, "FY2017": 1309.5, "FY2016": 1359.3}),
        ("Leverage ratio INCLUDING claims on central banks (%) (UK LRCom row UK-25c for FY2022-FY2023; "
         "the Basel III/CRR leverage ratio as originally reported FY2016-FY2021)",
         {"FY2023": "9.6%", "FY2022": "9.6%", "FY2021": "8.3%", "FY2020": "9.6%", "FY2019": "11.2%", "FY2018": "11.9%", "FY2017": "11.4%", "FY2016": "9.5%"}),
    ],
    p3_sources(LEVERAGE_BASIS_SOURCES),
    first_col_width=96,
    source_height=420,
    note="THE TWO PAIRS OF ROWS ARE NOT A LIKE-FOR-LIKE SERIES AND MUST NOT BE READ AS ONE. The PRA's UK Leverage "
         "Ratio Framework, in force from 1 January 2022, allows firms in its scope to exclude claims on central "
         "banks from the total exposure measure - the Bank's own FY2022 Pillar 3 says so in terms ('The PRA's UK "
         "Leverage Ratio framework that came into force from 1 January 2022, allows institutions within its scope "
         "to exclude assets held with the Bank of England from their leverage calculations'). From FY2022 the Bank "
         "prints BOTH bases in Template UK LRCom, and restated FY2021 onto the excluding basis. Excluding basis: "
         "FY2021 10.9%, FY2022 10.9%, FY2023 10.5% - i.e. flat, then slightly down. Including basis: FY2021 8.3%, "
         "FY2022 9.6%, FY2023 9.6%. The apparent 8.3% -> 10.9% jump a single blended row would show across the "
         "FY2021/FY2022 boundary is ENTIRELY the change of denominator, not a change in the Bank: on either basis "
         "held consistently the ratio did not improve by 2.6pp. The excluded amounts are stated by the Bank: "
         "UK-24a '(-) Claims on central banks excluded' = £411m at 30 Sep 2021, £228m (£228.4m in the FY2023 "
         "edition) at 30 Sep 2022, £153.9m at 30 Sep 2023. Neither basis is computed here from the other; every "
         "figure above is printed in one of the cited documents. FY2021's excluding-basis pair (1,320 / 10.9%) "
         "exists only as the FY2022 edition's comparative column - the Bank published no excluding-basis figure "
         "for FY2020 or earlier, so those years appear on the including row only and are NOT back-solved. "
         "FY2022's exposure measure is 1,624 / 1,852 as the FY2022 edition printed it and 1,623.2 / 1,851.6 as "
         "the FY2023 edition's comparative restates it, a rounding-level difference recorded rather than "
         "reconciled; the own-year figure is the one shown. FY2021's including-basis exposure is 1,732.2 per "
         "FY2021's own report and 1,731 per the FY2022 edition's comparative - same, to rounding. "
         "FY2025 is NOT APPLICABLE rather than undisclosed - the SDDT modification (PRA Rule 3.1, effective 18 "
         "February 2025) removed the Pillar 3 duty before the 30 September 2025 year-end, so no FY2025 leverage "
         "disclosure will ever exist; FY2024 is an ordinary open gap, its year having ended before that "
         "modification took effect, and the Annual Report's brief 'Capital risk management' note carries no "
         "leverage ratio. FY2015-FY2010 not available - no Basel III leverage ratio existed as a UK disclosure "
         "requirement under the Basel II regime those six years used. Those years belong on NEITHER of the two "
         "rows above: the excluding-/including-claims-on-central-banks distinction is a UK framework change "
         "effective 1 January 2022 and is meaningless applied to a Basel II year. The FY2013 document mentions a "
         "leverage ratio exactly once, as forward-looking prose about CRD IV's forthcoming requirements, with no "
         "value attached; FY2012/FY2011/FY2010 do not mention it at all. (FY2013-FY2010 columns added 2026-09-16 "
         "by HD-080's Basel II extension; that pass added no figure to this sheet and collapsed none of its rows.)",
)

metric(
    "LCR", "£m / %",
    [
        ("Total HQLA after haircuts (£m)", {"FY2023": 230.4, "FY2022": 334, "FY2021": 479.5, "FY2020": 196.4, "FY2019": 346.4, "FY2018": 245.2}),
        ("Total net cash outflow, adjusted value (£m)", {"FY2023": 130.2, "FY2022": 133, "FY2021": 137.1, "FY2020": 72.0, "FY2019": 67.0, "FY2018": 103.5}),
        ("Liquidity Coverage Ratio (%)", {"FY2023": "176.9%", "FY2022": "252%", "FY2021": "349.6%", "FY2020": "272.9%", "FY2019": "516.9%", "FY2018": "236.9%"}),
    ],
    p3_sources(),
    note="FY2025 is NOT APPLICABLE, not merely undisclosed - the SDDT modification (PRA Rule 3.1, effective 18 "
         "February 2025) removed this bank's Pillar 3 duty before its 30 September 2025 year-end, so no FY2025 "
         "LCR disclosure will ever exist. FY2024 is an ordinary open gap: its year ended 30 September 2024, "
         "BEFORE that modification took effect, so the exemption does not cover it and no document was found. "
         "The distinction is deliberate - see BASIS_NOTE. Year-end (point-in-time) values shown, per each source "
         "document's own basis ('year end value for LCR related metrics'); these are NOT the 12-month averages a "
         "UK KM1 template prints elsewhere, and the two bases are never merged. FY2017/FY2016 Pillar 3 documents "
         "were reviewed in full but contain no LCR disclosure (UK LCR reporting for this class of firm phased in "
         "gradually; FY2018 is this bank's first year showing it). FY2015-FY2010 not available - the LCR did not "
         "exist as a UK disclosure requirement under the Basel II regime those six years used; see the pre-CRD IV "
         "note in this sheet's sources.",
)

metric(
    "NSFR", "£m / %",
    [
        ("Total available stable funding (£m)", {"FY2023": 1721.9, "FY2022": 1549, "FY2021": 1551.0, "FY2020": 1226.2}),
        ("Total required stable funding (£m)", {"FY2023": 1144.2, "FY2022": 1085, "FY2021": 922.7, "FY2020": 793.3}),
        ("Net Stable Funding Ratio (%)", {"FY2023": "150.5%", "FY2022": "143%", "FY2021": "168.1%", "FY2020": "154.6%", "FY2019": "217.6%"}),
    ],
    p3_sources(),
    note="FY2025 is NOT APPLICABLE, not merely undisclosed - see the LCR sheet note; the SDDT modification "
         "(effective 18 February 2025) also replaces the full NSFR with a Simplified Retail Deposit Ratio going "
         "forward, and no SRDR value is disclosed either, so nothing succeeds this series. FY2024 is an ordinary "
         "open gap (year ended before the modification took effect). FY2019's own Pillar 3 document gives the "
         "ratio only (217.6%), with no ASF/RSF breakdown; the breakdown shown for FY2020 comes from FY2020's own "
         "report. FY2018/FY2017/FY2016 Pillar 3 documents were reviewed in full but contain no NSFR disclosure "
         "(UK NSFR reporting phased in later than LCR for this class of firm - FY2019 is this bank's first year "
         "showing it). FY2015-FY2010 not available - the NSFR did not exist as a UK disclosure requirement under "
         "the Basel II regime those six years used; see the pre-CRD IV note in this sheet's sources.",
)

metric(
    "MREL Ratio", "£m / %",
    [("MREL ratio", {y: ("Not applicable" if y == "FY2025" else "Not publicly disclosed") for y in YEARS})],
    p3_sources(),
    note="FY2025 reads 'Not applicable', every other year 'Not publicly disclosed', and the difference is "
         "deliberate and load-bearing. 'Not publicly disclosed' asserts a figure may exist that was not found; "
         "'Not applicable' means no such disclosure can exist. FY2025 is the latter: the SDDT modification (PRA "
         "Rule 3.1, FRN 204439, effective 18 February 2025) removed this bank's Pillar 3 disclosure duty before "
         "its 30 September 2025 year-end, so no FY2025 Pillar 3 document will ever be published. FY2024 stays "
         "'Not publicly disclosed' because its year ended 30 September 2024, BEFORE the modification took "
         "effect - it is an ordinary negative, not a structural exemption (see BASIS_NOTE for why that is left "
         "as NOT ESTABLISHED rather than claimed). For FY2023-FY2010, no MREL figure (numeric or qualitative) "
         "appears in any of the 14 Pillar 3 documents reviewed, nor in any Annual Report's brief capital note, "
         "and no reason is stated; for the six Basel II years FY2015-FY2010 the concept did not exist as a UK "
         "requirement at all. Consistent with this small private bank not being set an independent MREL "
         "requirement by the Bank of England, the same pattern seen at other small UK banks in this project "
         "(e.g. Cynergy Bank, DF Capital Bank).",
)

# ---------------------------------------------------------------
# Overview sheet (Pillar-3-only: no cash-flow chart)
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 2122.6, "FY2024": 2008.8, "FY2023": 1823.1, "FY2022": 1860.8, "FY2021": 1713.4, "FY2020": 1409.2, "FY2019": 1378.7, "FY2018": 1363.4, "FY2017": 1267.4, "FY2016": 1316.8, "FY2015": 999.0, "FY2014": 784.7}),
        ("Loans and advances to customers", {"FY2025": 1839.7, "FY2024": 1699.3, "FY2023": 1488.5, "FY2022": 1404.6, "FY2021": 1061.5, "FY2020": 930.8, "FY2019": 766.9, "FY2018": 827.9, "FY2017": 757.9, "FY2016": 706.9, "FY2015": 557.5, "FY2014": 440.8}),
        ("Deposits from customers", {"FY2025": 1860.3, "FY2024": 1639.4, "FY2023": 1368.1, "FY2022": 1425.0, "FY2021": 1381.0, "FY2020": 1071.4, "FY2019": 1042.8, "FY2018": 994.6, "FY2017": 947.7, "FY2016": 991.7, "FY2015": 848.6, "FY2014": 633.2}),
        ("Total equity", {"FY2025": 179.8, "FY2024": 183.2, "FY2023": 183.8, "FY2022": 185.0, "FY2021": 148.6, "FY2020": 141.0, "FY2019": 160.3, "FY2018": 171.7, "FY2017": 167.3, "FY2016": 146.3, "FY2015": 133.7, "FY2014": 132.0}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Net interest income", {"FY2025": 41.8, "FY2024": 39.7, "FY2023": 39.4, "FY2022": 29.4, "FY2021": 17.6, "FY2020": 15.6, "FY2019": 20.2, "FY2018": 18.3, "FY2017": 13.9, "FY2016": 13.2, "FY2015": 5.6, "FY2014": 2.9}),
        ("Net operating income", {"FY2025": 39.8, "FY2024": 41.9, "FY2023": 46.6, "FY2022": 38.6, "FY2021": 26.2, "FY2020": 20.9, "FY2019": 28.0, "FY2018": 18.2, "FY2017": 19.3, "FY2016": 33.5, "FY2015": 13.0, "FY2014": 9.3}),
        ("Profit/(loss) for the financial year", {"FY2025": -3.9, "FY2024": -1.7, "FY2023": -0.2, "FY2022": 4.8, "FY2021": 5.8, "FY2020": -15.9, "FY2019": -5.7, "FY2018": 5.5, "FY2017": 10.2, "FY2016": 17.6, "FY2015": 4.3, "FY2014": 4.1}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 183.2, "FY2024": 183.8, "FY2023": 185.0, "FY2022": 148.6, "FY2021": 141.0, "FY2020": 160.3, "FY2019": 171.7, "FY2018": 167.3, "FY2017": 153.5, "FY2016": 133.3, "FY2015": 132.0, "FY2014": 128.2}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": -3.4, "FY2024": -0.6, "FY2023": -1.2, "FY2022": 11.4, "FY2021": 7.6, "FY2020": -19.3, "FY2019": -8.0, "FY2018": 4.4, "FY2017": 8.8, "FY2016": 13.0, "FY2015": 1.8, "FY2014": 3.8}),
        ("Other equity movements, net", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 25.0, "FY2021": 0, "FY2020": 0, "FY2019": -3.4, "FY2018": 0, "FY2017": 5.0, "FY2016": 0, "FY2015": 0, "FY2014": 0}),
        ("Closing equity", {"FY2025": 179.8, "FY2024": 183.2, "FY2023": 183.8, "FY2022": 185.0, "FY2021": 148.6, "FY2020": 141.0, "FY2019": 160.3, "FY2018": 171.7, "FY2017": 167.3, "FY2016": 146.3, "FY2015": 133.7, "FY2014": 132.0}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("CET1 Ratio", {"FY2025": "17.5%", "FY2024": "19.8%", "FY2023": "24.5%", "FY2022": "25.2%", "FY2021": "20.2%", "FY2020": "19.7%", "FY2019": "23.0%", "FY2018": "22.3%", "FY2017": "21.1%", "FY2016": "19.2%"}),
        ("Tier 1 Ratio", {"FY2025": "17.5%", "FY2024": "19.8%", "FY2023": "24.5%", "FY2022": "25.2%", "FY2021": "20.2%", "FY2020": "19.7%", "FY2019": "23.0%", "FY2018": "22.3%", "FY2017": "21.1%", "FY2016": "19.2%"}),
        ("Total Capital Ratio", {"FY2025": "17.5%", "FY2024": "19.8%", "FY2023": "24.5%", "FY2022": "25.2%", "FY2021": "20.2%", "FY2020": "19.7%", "FY2019": "23.0%", "FY2018": "22.3%", "FY2017": "21.2%", "FY2016": "19.2%"}),
        ("Leverage Ratio (incl. claims on central banks - the only basis comparable across all years; see note)", {"FY2023": "9.6%", "FY2022": "9.6%", "FY2021": "8.3%", "FY2020": "9.6%", "FY2019": "11.2%", "FY2018": "11.9%", "FY2017": "11.4%", "FY2016": "9.5%"}),
        ("LCR", {"FY2023": "176.9%", "FY2022": "252%", "FY2021": "349.6%", "FY2020": "272.9%", "FY2019": "516.9%", "FY2018": "236.9%"}),
        ("NSFR", {"FY2023": "150.5%", "FY2022": "143%", "FY2021": "168.1%", "FY2020": "154.6%", "FY2019": "217.6%"}),
    ],
    note="This entity takes the FRS 101/FRS 1 cash-flow-statement exemption every year FY2014-FY2025 (see the Cash "
         "Flow Statement sheet), so no cash flow summary or chart is shown here - Balance Sheet/Profit & Loss/"
         "Statement of Changes in Equity summaries and the Pillar 3 Key Metrics trend chart are shown instead. "
         "PILLAR 3 YEAR COVERAGE (updated 2026-09-16, HD-080): the 11 capital metric sheets now run back to "
         "FY2010, on the strength of a continuous FY2010-FY2023 run of 14 published Pillar 3 documents. Only the "
         "Total Capital sheet carries data before FY2016, because FY2010-FY2015 are Basel II editions that "
         "disclose 'Total capital resources' but no risk-weighted assets, no CET1 and no capital ratio of any "
         "kind - every other pre-FY2016 cell is blank BY DESIGN and well-sourced, never back-solved. The Asset "
         "Quality and RWA Breakdown sheets deliberately stop at FY2014, where their content genuinely stops. "
         "FY2025's Pillar 3 cells read 'Not applicable' rather than 'Not publicly disclosed': the SDDT "
         "modification (PRA Rule 3.1, effective 18 February 2025) ended the disclosure duty before that "
         "year-end, so the figures cannot exist. FY2024 is an ordinary open gap, its year having ended before "
         "the modification took effect. "
         "Leverage/LCR/NSFR availability varies by year - see each Pillar 3 sheet's own source citation for detail "
         "(pre-CRD IV FY2015-FY2010 have none of the three; LCR/NSFR were phased in for this bank in FY2018/FY2019 "
         "respectively). LEVERAGE RATIO BASIS, stated here because this sheet is a standalone copy and the chart "
         "would otherwise draw a false trend: the PRA's UK Leverage Ratio Framework, in force from 1 January 2022, "
         "lets firms exclude claims on central banks from the exposure measure, and from FY2022 the Bank reports "
         "on that excluding basis as its headline (FY2021 restated 10.9%, FY2022 10.9%, FY2023 10.5%). Charting "
         "the headline figures would show an 8.3% -> 10.9% jump across the FY2021/FY2022 boundary that is purely "
         "the change of denominator. The row above therefore uses the INCLUDING-claims-on-central-banks basis, "
         "which is the one the Bank reports consistently from FY2016 through FY2023 (UK LRCom row UK-25c for "
         "FY2022-FY2023, the Basel III/CRR ratio before that). Both bases, with their exposure measures and the "
         "amounts excluded, are on the Leverage Ratio sheet - see its note. The FY2022 and FY2017 'Other equity movements' figures (£25.0m and £5.0m) are real share "
         "capital issuances those years, not plugs; the FY2019 figure (-£3.4m) is the IFRS 9 transition adjustment "
         "on adoption. Note FY2017's own 'Opening equity' (£153.5m) is the FY2017 Annual Report's RESTATED FY2016 "
         "closing position (Note 36 prior-period error, +£7.2m vs. the £146.3m FY2016 originally reported as its "
         "own closing figure) - both figures are shown, and this discontinuity, on the Statement of Changes in "
         "Equity sheet.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/JULIAN HODGE BANK FINANCIALS.xlsx")
