import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015"]
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/04218020/filing-history/MzQ3OTMzNTI0NWFkaXF6a2N4/document?download=0&format=pdf"
AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/04218020/filing-history/MzQzMzA4NzcwMWFkaXF6a2N4/document?download=0&format=pdf"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/04218020/filing-history/MzM4OTExNTc1NmFkaXF6a2N4/document?download=0&format=pdf"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/04218020/filing-history/MzM1NTU5ODQzNmFkaXF6a2N4/document?download=0&format=pdf"
# SCHEME DELIBERATELY SET TO http:// - 2026-09-16. DO NOT "UPGRADE" THIS TO https://.
# persiabank.co.uk's TLS is broken at the server: the TCP connection to port 443 is
# accepted (95.215.227.247:443) and then the server RESETS the connection during the
# TLS handshake - "Recv failure: Connection reset by peer" at Client hello, so no
# certificate is ever presented and no HTTPS client of any kind can fetch the file.
# Plain HTTP serves it perfectly: HTTP 200, %PDF, 1,382,251 bytes, 28 pages. This is
# a server defect, not a redirect and not something a different client or user-agent
# can work around, and it is why earlier sessions wrongly recorded this domain as
# dead. The https:// form is kept below purely as the record of what was tried.
PILLAR3_2021_URL = "http://www.persiabank.co.uk/Pillar%203%202021%20v3.pdf"
PILLAR3_2021_URL_HTTPS_BROKEN = "https://www.persiabank.co.uk/Pillar%203%202021%20v3.pdf"

# HD-021 (extend to FY2015) source documents: Companies House full-accounts filings
# (scanned, no text layer - transcribed from page images) plus Wayback Machine snapshots
# of the Bank's own standalone Pillar 3 disclosures for FY2016/FY2018/FY2020 (its own
# site refused live TLS connections this session, same as the FY2021 Pillar 3 document
# above). No standalone Pillar 3 document was locatable for FY2017 or FY2019; those two
# years' regulatory-capital figures are instead the FY2017/FY2019 comparative columns
# printed inside the FY2018/FY2020 Pillar 3 documents respectively.
AR2020_URL = "https://find-and-update.company-information.service.gov.uk/company/04218020/filing-history/MzI4MjYzOTE2OGFkaXF6a2N4/document?download=0&format=pdf"
AR2019_URL = "https://find-and-update.company-information.service.gov.uk/company/04218020/filing-history/MzI0MDMwNDExNmFkaXF6a2N4/document?download=0&format=pdf"
AR2018_URL = "https://find-and-update.company-information.service.gov.uk/company/04218020/filing-history/MzIxMjI1ODQ3MmFkaXF6a2N4/document?download=0&format=pdf"
AR2017_URL = "https://find-and-update.company-information.service.gov.uk/company/04218020/filing-history/MzE4MTE5NDQwMWFkaXF6a2N4/document?download=0&format=pdf"
AR2016_URL = "https://find-and-update.company-information.service.gov.uk/company/04218020/filing-history/MzE1NjI0NzM2OWFkaXF6a2N4/document?download=0&format=pdf"
AR2015_URL = "https://find-and-update.company-information.service.gov.uk/company/04218020/filing-history/MzEyNzM3Mjc4NWFkaXF6a2N4/document?download=0&format=pdf"
PILLAR3_2020_URL = (
    "http://web.archive.org/web/20220125010012id_/http://www.persiabank.co.uk/Pillar%203%202020%20v7.pdf"
)
PILLAR3_2018_URL = (
    "http://web.archive.org/web/20180902131909id_/http://www.persiabank.co.uk/"
    "Pillar%203%20Disclosure%20as%20at%2031_03_2018%20(final).pdf"
)
PILLAR3_2016_URL = (
    "http://web.archive.org/web/20161024202355id_/http://www.persiabank.co.uk/"
    "Pillar%203%20Disclosure%20as%20at%2031%20March%202016.pdf"
)
# FY2015 STANDALONE PILLAR 3 (2026-09-15). The FY2015 regulatory figures in this
# workbook were previously cited only via the copy embedded in the FY2015 Annual
# Report at pp.35-52. The Bank's own standalone edition has now been recovered
# from the Internet Archive and read directly. It is an 18-page image-only scan
# with no text layer: rendered at 250dpi, OCR'd with tesseract, and then re-read
# visually off the page images for every figure used (pp.8-9 capital tables,
# pp.14-15 market and operational risk), per this project's standing OCR rule.
PILLAR3_2015_URL = (
    "http://web.archive.org/web/20160316221826id_/http://www.persiabank.co.uk/"
    "Pillar3_disclosures_March%202015.pdf"
)

# NOTE ON THE FY2020 CAPTURE (recorded so a later pass does not "upgrade" the URL).
# The Internet Archive holds two captures of the FY2020 edition. The one cited in
# PILLAR3_2020_URL above is the v7 file and is complete (1,109,265 bytes, 28
# pages). There is also a "v6" capture which is TRUNCATED at exactly 1 MiB -
# a capture artefact, not a different edition. Use v7 only.

# The Bank reports in EUR and discloses its own EUR/GBP rates in the accounting
# policies.  Rates are GBP PER EUR, so EUR * rate = GBP (see the RATE DIRECTION
# note above the helpers - this line said "EUR per GBP, so EUR / rate = GBP"
# until 2026-09-16, which inverted every conversion).  FY2015 and FY2016's own
# accounts disclose only an average rate for the year, not a year-end/closing rate -
# so stock (balance-sheet-type) figures for those two years cannot be converted to GBP
# and are left in EUR '000 (see stock_v/stock below, which pass EUR through unchanged
# when no year-end rate is available for that year).
AVG_RATE = {
    "FY2025": 0.8390, "FY2024": 0.8630, "FY2023": 0.8525, "FY2022": 0.8525, "FY2021": 0.8925,
    "FY2020": 0.8852, "FY2019": 0.8823, "FY2018": 0.8827, "FY2017": 0.8400, "FY2016": 0.7390, "FY2015": 0.7819,
}
YEAR_END_RATE = {
    "FY2025": 0.8350, "FY2024": 0.8550, "FY2023": 0.8800, "FY2022": 0.8475, "FY2021": 0.8525,
    "FY2020": 0.8900, "FY2019": 0.8600, "FY2018": 0.8750, "FY2017": 0.8575,
    # FY2016 and FY2015: no year-end/closing EUR/GBP rate is disclosed in either year's
    # own accounts (only an average rate) - deliberately omitted, not a transcription gap.
}

ENTITY_NOTE = (
    "ENTITY AND REPORTING BASIS: Persia International Bank Plc (company 04218020, FRN 208020) is an active UK "
    "PRA/FCA-regulated bank incorporated 16 May 2001, with registered office at 6 Lothbury, London EC2R 7HH. "
    "Companies House shows full accounts filed through the year ended 31 March 2025; the Bank is owned 60% by Bank "
    "Mellat and 40% by Bank Tejarat. STATUS RE-CONFIRMED 2026-09-15: Companies House shows the company as ACTIVE, "
    "with full accounts to 31 March 2025 filed 2 September 2025, accounts to 31 March 2026 due by 31 December 2026, "
    "and a confirmation statement filed 10 June 2026; the Bank also still holds PRA authorisation, appearing as "
    "'Persia International Bank Plc', FRN 208020, in the Bank of England's own 'List of banks' as at 30 September "
    "2026. A further restriction post-dates the FY2025 reporting date: the Bank's own website notice 'Persia "
    "International Bank PLC - Sanctions Notice' (dated 06/10/2025) states it 'has been made subject to financial "
    "sanctions by the UK Government and the European Union as of 29 September 2025' and operates under OFSI General "
    "Licence INT/2025/7345464. These are the Company's own entity-level financial statements, prepared under "
    "UK-adopted IFRS on a going-concern basis, in EUR (the functional and presentation currency). The Bank's reports "
    "say that OFAC sanctions re-imposed in November 2018 and continuing difficulty obtaining UK clearing and "
    "correspondent-bank relationships restrict normal banking activity; Iranian exposures continue to receive a 150% "
    "risk weight because Iran is excluded from the relevant UK/EU equivalence list. The reports nevertheless state "
    "that the Bank expects to continue as a going concern. The FY2022 report's auditor highlighted material uncertainty "
    "over going concern, while later reports continued on a going-concern basis. "
    "HD-021 EXTENSION: EU/UN sanctions on the Bank (imposed 27 July 2010, annulled by the EU General Court in "
    "September 2013, re-imposed November 2013) were lifted 16 January 2016, and the FY2017 report states the PRA "
    "authorised the Bank to resume normal business on 7 November 2016 - so FY2015/FY2016 predate that resumption "
    "and describe a materially more restricted, wind-down-mode bank than FY2017 onward. BASEL II/III CAVEAT: the "
    "FY2015 accounts and the Bank's FY2015 Pillar 3 disclosure predate the UK's CRD IV Pillar 3 rollout for a firm "
    "of this size and disclose only Tier 1 / Tier 2 / Total Capital (no CET1 concept, no Leverage Ratio, no LCR); "
    "CET1, Leverage Ratio and (from FY2018) LCR are all genuinely disclosed from the Bank's FY2016 Pillar 3 "
    "disclosure onward. FY2015's own Pillar 3 disclosure separately states a Total Capital figure (EUR 151,979,000) "
    "that is EUR 518,000 lower than the FY2015 statutory accounts' own capital-management note (EUR 152,497,000, "
    "which ties to the Balance Sheet); the Pillar 3 figure appears to reuse the FY2014 year-end retained-earnings "
    "figure by mistake. This workbook uses each year's own statutory accounts' capital-management note as the "
    "authoritative Tier 1/Tier 2/Total Capital figure (consistent with every other bank in this project), and uses "
    "Pillar 3 disclosures only for figures the statutory accounts do not state at all (RWA, CET1/Total capital "
    "ratios, Leverage Ratio, LCR)."
)

LINK_PROVENANCE = (
    "LINK PROVENANCE (checked 16 September 2026). Two deliberate URL conventions are used for this bank's "
    "Pillar 3 sources. Both are easy to 'helpfully' undo, so both are recorded here with the reason.\n"
    "1) THE FY2021 PILLAR 3 IS CITED OVER PLAIN http://, NOT https://. DO NOT UPGRADE IT. persiabank.co.uk's "
    "TLS is broken at the server, not merely misconfigured: the TCP connection to port 443 is accepted and the "
    "server then RESETS the connection during the TLS handshake ('Recv failure: Connection reset by peer' at "
    "Client hello), so no certificate is ever presented and NO https client can retrieve the file - this is not "
    "something a different user-agent, client or retry can get around. Over plain HTTP the same file serves "
    "perfectly: HTTP 200, %PDF magic bytes, 1,382,251 bytes, 28 pages. The https:// form that fails is kept in "
    "the script as PILLAR3_2021_URL_HTTPS_BROKEN so the record of what was tried is not lost. This TLS failure "
    "is also why earlier sessions wrongly recorded the whole domain as dead; it is alive over HTTP.\n"
    "   INTEGRITY CHECK: the file served live over HTTP is byte-identical to the Internet Archive's capture of "
    "it - both MD5 08b8d37ca13c50b214d275062ab119c3 - so the live HTTP copy and the archived copy are the same "
    "document, and the figures taken from it are unaffected by which one is read.\n"
    "   SCOPE: the live site was re-enumerated over HTTP this session and carries exactly ONE Pillar 3 "
    "document, 'Pillar 3 2021 v3.pdf'. There is no later edition to switch to.\n"
    "2) ALL FIVE WAYBACK CITATIONS USE THE id_ MODIFIER, NOT if_ (changed 16 September 2026). id_ is the "
    "Internet Archive's identity mode, which returns the originally captured bytes; if_ is iframe mode. Every "
    "one of the five was fetched under BOTH modifiers and verified: all returned HTTP 200 with %PDF magic bytes "
    "and byte-identical content, MD5 for MD5, so this change repaired nothing and altered no figure - it simply "
    "pins the citations to the canonical raw-bytes form. Verified page counts and MD5s, id_ form:\n"
    "   FY2021 (capture 20260110002617): 28 pages, 1,382,251 bytes, MD5 08b8d37ca13c50b214d275062ab119c3\n"
    "   FY2020 (capture 20220125010012): 28 pages, 1,109,265 bytes, MD5 1016257632cab1c38991d1bb3dd10606\n"
    "   FY2018 (capture 20180902131909): 27 pages,   936,437 bytes, MD5 f2ba9c655e0d16e9d22889d93f33b6b7\n"
    "   FY2016 (capture 20161024202355): 21 pages,   965,006 bytes, MD5 dfcc56241e21d72f059f5e21e9749c88\n"
    "   FY2015 (capture 20160316221826): 18 pages,   994,951 bytes, MD5 16035cdfe27c311e39daa96e7fde9371\n"
    "   The FY2015 count of 18 pages confirms the image-only scan already described in this script, and the "
    "FY2020 count of 28 pages confirms the v7 capture rather than the 1 MiB-truncated v6 one.\n"
    "   NOTE ON THE ARCHIVED-SIDE SCHEME: inside each Wayback URL the original address is recorded as "
    "http://www.persiabank.co.uk/... That http is part of the archived URL's identity - the key the capture is "
    "stored under - and rewriting it to https would address a DIFFERENT key that the Archive may hold no "
    "capture for. Leave it as http, on both sides."
)

FX_NOTE = (
    "FX METHODOLOGY: the Bank's accounting policies disclose EUR/GBP rates, which are GBP PER EUR (FY2025 Annual "
    "Report, Note 2.1, p.40: \"The average exchange rate for EUR/GBP applied during the year was 0.8390 (2023/24: "
    "0.8630). The year-end exchange rate used was 0.8350 (2023/24: 0.8550)\" - at 31 March 2025 EUR1 bought "
    "GBP0.8358, so 0.8350 is pounds per euro). Flow figures are therefore MULTIPLIED by the year's disclosed "
    "average rate and balance figures by its disclosed year-end rate. CORRECTION 2026-09-16: until that date this "
    "workbook DIVIDED by both rates, on the strength of a code comment that mis-stated them as \"EUR per GBP\"; "
    "every converted figure was consequently overstated by 1/rate-squared (about 1.43x). The conversion was "
    "corrected in both directions of travel; no transcribed source figure was altered, and no percentage moved, "
    "because a ratio converts its numerator and denominator by the same factor. Bank Sepah International, the same "
    "shape of entity (Iranian-owned, EUR presentation, 31 March year-end), discloses near-identical rates, labels "
    "them \"GBP per EUR 1\" and multiplies - which is the corroborating precedent for this direction. The "
    "cash-flow sheet includes the Bank's own exchange-difference line and a programmatic GBP translation line where "
    "the use of average rates for flows and year-end rates for balances creates a residual. FY2021 opening cash is "
    "left blank because the source does not provide a FY2020 year-end rate in the reviewed five-year source set. "
    "HD-021 EXTENSION (FY2015-FY2020): FY2017-FY2020 are converted to GBP the same way, using each year's own "
    "disclosed average/year-end rate. FY2015 and FY2016's own accounts disclose only an average EUR/GBP rate for "
    "the year, not a year-end rate - so every balance-sheet-type (stock) figure for FY2015 and FY2016 in this "
    "workbook (Balance Sheet, Asset Quality, Pillar 3 capital/RWA sheets, and equity closing balances) is shown in "
    "EUR '000, unconverted, not GBP; flow figures (P&L, cash flow, in-year equity movements) for FY2015/FY2016 are "
    "still converted to GBP using that year's own disclosed average rate. This is a genuine source limitation, not "
    "a transcription gap - see stock_v()/stock() below, which pass EUR values through unchanged for any year "
    "missing from YEAR_END_RATE."
)

CASH_FLOW_SOURCES = (
    "Sources - Persia International Bank Plc's own entity-level Statements of Cash Flows, converted from EUR to GBP "
    "using the Bank's disclosed rates (see FX note):\n"
    f"FY2025: Annual Report and Financial Statements for year ended 31 March 2025, p.39 - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements for year ended 31 March 2024, p.32 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements for year ended 31 March 2023, p.31 - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements for year ended 31 March 2022, p.30 - {AR2022_URL}\n"
    "FY2021: FY2022 Annual Report's comparative column, p.30 - " + AR2022_URL + "\n"
    f"FY2020: Annual Report and Financial Statements for year ended 31 March 2020, p.29 (scanned Companies House "
    f"filing, transcribed from the page image) - {AR2020_URL}\n"
    f"FY2019: Annual Report and Financial Statements for year ended 31 March 2019, p.25 (scanned filing) - {AR2019_URL}\n"
    f"FY2018: Annual Report and Financial Statements for year ended 31 March 2018, p.18 (scanned filing) - {AR2018_URL}\n"
    f"FY2017: Annual Report and Financial Statements for year ended 31 March 2017, p.16 (scanned filing) - {AR2017_URL}\n"
    f"FY2016: Annual Report and Financial Statements for year ended 31 March 2016, p.16 (scanned filing) - {AR2016_URL}\n"
    f"FY2015: Annual Report and Financial Statements for year ended 31 March 2015, p.15 (scanned filing) - {AR2015_URL}\n\n"
    + ENTITY_NOTE + "\n" + FX_NOTE + "\n\n"
    "FY2020 CASH RECONCILIATION NOTE: the FY2020 Annual Report's own Statement of Cash Flows states \"Cash and cash "
    "equivalents at the end of the year\" as EUR 174,469k, but its own supporting reconciliation table two lines "
    "below (cash at central banks EUR 27,443k + loans/advances to banks with maturity <3 months EUR 151,026k) sums "
    "to EUR 178,469k - a genuine EUR 4,000k internal inconsistency in the Bank's own document, not a transcription "
    "error here. This workbook uses EUR 178,469k (the reconciliation-table figure, which also ties to opening cash "
    "plus the year's own operating/investing/financing/FX movements) for FY2020 closing cash."
)


# ---------------------------------------------------------------
# P3_CESSATION_NOTE - the evidenced explanation for the FY2022-FY2025 Pillar 3
# gap (Total RWAs, Leverage Ratio, LCR). Established 2026-09-15 under the
# multi-year trailing-gap investigation, independently of the earlier
# 2026-09-12 audit whose findings it confirms and extends.
# ---------------------------------------------------------------
P3_CESSATION_NOTE = (
    "STRUCTURAL CESSATION OF PILLAR 3 PUBLICATION - EVIDENCED, not inferred from a failed search "
    "(established 2026-09-15). The Bank stopped publishing Pillar 3 disclosures after its 31 March 2021 "
    "edition, and says so, in its own words, in its own Annual Reports:\n"
    "  - Annual Report and Financial Statements 2022 (year ended 31 March 2022), 'Pillar 3 Disclosures' "
    "heading in the STRATEGIC REPORT, p.8: \"Pillar 3 disclosures are made separately and ARE PUBLISHED ON "
    "THE BANK'S WEB SITE at www.persiabank.co.uk.\"\n"
    "  - Annual Report and Financial Statements 2023, 2024 and 2025, same heading and same page position "
    "(p.8 of each filing), all three years: \"Pillar 3 disclosures are made separately and CAN BE MADE "
    "AVAILABLE ON REQUEST.\" - the "
    "reference to web publication is gone, and has stayed gone through the most recent filing.\n"
    "VERIFICATION NOTE (2026-09-15): these two paragraphs had been OCR'd by an earlier pass. Because every "
    "one of these filings is a scanned image with no text layer, and because OCR has already produced real "
    "misreads elsewhere in this project, the FY2022 and FY2025 pages were re-rendered and READ VISUALLY this "
    "pass. Both quotations above are confirmed word-for-word. One correction fell out of doing so: the "
    "section is the Bank's STRATEGIC REPORT, not the Directors'/corporate governance report as previously "
    "recorded here.\n"
    "FY2022 IS A DIFFERENT KIND OF NEGATIVE FROM FY2023-FY2025, and the two should not be collapsed into "
    "one. For FY2023, FY2024 and FY2025 the Bank states its own policy: the disclosure is not published, "
    "only available on request. That is a complete, sourced answer - the same shape as Havin - and those "
    "three years should not be re-chased. FY2022 is different: the Bank asserted at the time that the "
    "disclosure WAS published on its website, yet no FY2022 edition is on that website now and none was ever "
    "captured by the Internet Archive despite continued crawling. So FY2022 is a published-then-removed (or "
    "asserted-but-never-actually-posted) case rather than a declared non-publication, and it is the one year "
    "of the four where a copy might still exist somewhere to be found.\n"
    "That wording change is the disclosure-policy change itself, and it lines up exactly with what is on the "
    "Bank's website. The live site was reachable this session over plain HTTP (http://www.persiabank.co.uk/ "
    "- HTTPS still fails the TLS handshake, which is why earlier sessions recorded the domain as dead) and "
    "its complete link list was enumerated: it carries exactly ONE Pillar 3 document, 'Pillar 3 2021 v3.pdf' "
    "(the 31 March 2021 edition already used in this workbook), and no later edition. A full Wayback CDX "
    "enumeration of every URL ever captured on the domain agrees: the newest Pillar 3 file ever archived is "
    "that same 2021 edition, and the domain was still being crawled in 2024 and 2025 (e.g. its 2025 Wolfsberg "
    "questionnaire and its July 2024 GDPR notice were both captured), so this is a genuine absence rather "
    "than a crawl gap.\n"
    "The statutory accounts do not fill the gap either. The FY2022 and FY2024 Annual Reports were "
    "independently re-downloaded from Companies House and OCR'd page-by-page this session (both are scanned "
    "filings with no text layer; the earlier audit had covered FY2023 and FY2025 the same way, so all four "
    "gap years have now been read directly). In every one of them the capital-management note gives only the "
    "capital BASE build-up - Ordinary share capital + Retained earnings = Total regulatory capital base, in "
    "EUR '000 - and explicitly describes the PRA requirement as being 'based upon the ratio of capital to "
    "total risk weighted exposures' while publishing no risk-weighted exposure amount, no ratio, no leverage "
    "ratio and no LCR. Capital adequacy appears only as narrative ('The Tier 1 Capital ratios are still "
    "robust'). Those capital-base amounts are already carried on the CET1/Tier 1/Total Capital sheets; "
    "nothing else in the accounts is transcribable, and no RWA is back-solved from them here.\n"
    "THE ENTITY HAS NOT CEASED, WHICH IS WHY THIS IS A DISCLOSURE-POLICY FINDING RATHER THAN A WIND-UP: "
    "Companies House shows Persia International Bank Plc (04218020) as ACTIVE, with full accounts to 31 March "
    "2025 filed on 2 September 2025, next accounts to 31 March 2026 due by 31 December 2026, and a "
    "confirmation statement filed on 10 June 2026; and the Bank appears as 'Persia International Bank Plc', "
    "FRN 208020, in the Bank of England's own 'List of banks' as at 30 September 2026 - i.e. it retains PRA "
    "authorisation. Its restriction has, however, deepened: the Bank's own website notice 'Persia "
    "International Bank PLC - Sanctions Notice' (dated 06/10/2025) states that it 'has been made subject to "
    "financial sanctions by the UK Government and the European Union as of 29 September 2025' and operates "
    "under OFSI General Licence INT/2025/7345464 - an event that post-dates the FY2025 (31 March 2025) "
    "reporting date and therefore does not explain the FY2022-FY2024 gap, but does make a resumption of "
    "public Pillar 3 disclosure less likely.\n"
    "GOING-CONCERN CONTEXT (added 2026-09-15, read visually from the rendered pages - these filings have no "
    "text layer). The auditor's reports carry a 'Material uncertainty related to going concern' section in "
    "both the first and the last of the four gap years, so the Bank has been reporting under that cloud "
    "throughout the period in which it stopped publishing Pillar 3. The FY2025 report (p.24 of 82) reads: "
    "\"We draw attention to note 2.2 in the financial statements, where the directors explain the basis for "
    "preparing the financial statements on a going concern basis. Due to ongoing US sanctions on the "
    "Republic of Iran, heightened geopolitical tensions in the Middle East, the Iran Israel war, and the "
    "recent change in the US administration, the Bank continues to face significant challenges in "
    "maintaining suitable correspondent banking relationships and clearing services. These events and "
    "conditions create material uncertainties that may cast significant doubt on the Bank's ability to "
    "continue as a going concern. Our opinion is not modified in respect of this matter\". The FY2022 "
    "auditor's report (p.19) carries the equivalent section. NOTE THE QUALIFIER: the opinion is NOT "
    "modified - this is a disclosed material uncertainty, not an adverse or qualified audit opinion, and it "
    "is recorded here as context for why the Bank's disclosure practice narrowed, not as a solvency "
    "judgement. It is also why 'the entity wound down' remains unavailable as an explanation: a bank filing "
    "audited accounts with an unmodified opinion is still operating.\n"
    "USER-ACTIONABLE: a direct written request to the Bank is the only realistic route to FY2022-FY2025 RWA, "
    "leverage and LCR figures - that is what its own Annual Reports invite. Further online searching will not "
    "surface them. If someone wants to try the site in a browser, note that it only answers on "
    "http://www.persiabank.co.uk/ , not https."
)


FY2015_P3_NOTE = (
    "FY2015 STANDALONE PILLAR 3 RECOVERED 2026-09-15 (year ended 31 MARCH 2015; this Bank's year-end is 31 March "
    "throughout). 'Pillar 3 Disclosures March 2015', recovered from the Internet Archive - " + PILLAR3_2015_URL + "\n"
    "  - Section 3 'Capital Resources', p.8, capital structure as at 31 March 2015, in euro: Ordinary share capital "
    "100,000,000; Retained Earnings 5,479,000; TOTAL TIER 1 CAPITAL 105,479,000; Tier 2 capital 46,500,000; TOTAL "
    "CAPITAL 151,979,000. The Tier 2 is described as loan capital, floating rate notes redeemable in 2043 and listed "
    "on the Luxembourg stock exchange.\n"
    "  - Section 4 'Capital Adequacy', p.9: Capital charge under Pillar 1 17,698,000; Pillar 2 requirements (stated "
    "as 225% of Pillar 1) 39,821,000; Total capital resources 151,979,000; Surplus of capital resources 112,158,000. "
    "'Breakdown of exposure classes' table, same page: Central Government/Bank risk-weighted exposure 144,039,000 "
    "(risk capital 11,523,000); Credit institutions 2,514,000 (201,000); Corporate companies 50,022,000 (4,002,000); "
    "Securities 435,000 (35,000); Short term claims on institutions 7,822,000 (626,000); Others 16,389,000 "
    "(1,311,000); TOTAL 221,221,000 (17,698,000).\n"
    "  - Section 6 'Market risk', p.14: 'As at 31 March 2015 the FX spot position risk: EUR 4,128,000'.\n"
    "  - Section 7 'Operational risk', p.15: the Basic Indicator Approach Operational Risk Requirement multiplied by "
    "12.5 gives a Risk Weighted Exposure 'which as at 31 March 2015 was EUR 11,501,000'.\n"
    "  - WHAT THIS EDITION SETTLES. (1) It confirms the composition of the EUR 518,000 divergence already recorded "
    "in this workbook's entity note: the Pillar 3's Tier 1 of 105,479,000 is ordinary share capital 100,000,000 plus "
    "retained earnings 5,479,000, where the FY2015 statutory accounts' capital-management note gives 105,997,000 and "
    "ties to the Balance Sheet. This workbook's existing convention is unchanged - the statutory figure remains the "
    "authoritative Tier 1/Total Capital on those sheets - but the divergence is now traced to the retained-earnings "
    "line specifically, not merely asserted. (2) It confirms that NO capital ratio of any kind is printed anywhere "
    "in the FY2015 edition, which is why the FY2015 ratio cells are this workbook's own calculation - see the "
    "warning on those sheets. (3) It supplies two figures this workbook did not previously hold at all: the market "
    "risk and operational risk risk-weighted exposures, now on the RWA Breakdown sheet.\n"
    "  - THE BIG ONE: THE FY2015 'TOTAL RWA' OF EUR 221,221,000 IS CREDIT-RISK ONLY. The 221,221,000 is the total "
    "line of the 'Breakdown of exposure classes' table (and of the same document's Template CR4), whose six rows are "
    "all credit exposure classes; 17,698,000 is exactly 8% of it. The market risk RWE (4,128,000) and the "
    "operational risk RWE (11,501,000) are disclosed in separate narrative sentences elsewhere in the document and "
    "are NOT included in that total, and the edition prints no Pillar 1 total RWA anywhere. This is the same "
    "credit-subtotal-presented-as-total defect confirmed at Redwood, Ghana International and Bank of Ceylon. It is "
    "flagged on the Total RWAs, Total Capital Ratio and Tier 1 Ratio sheets and the FY2015 figure is left as "
    "disclosed there rather than replaced - no document states a FY2015 total. Note that the later editions do NOT "
    "share the defect: the FY2016 edition prints an explicit 'Total Pillar 1 risk 319,767' row summing credit "
    "306,733, market 3,036 and operational 9,998, and FY2017-FY2021 follow the same layout.\n"
    "  - No leverage ratio, LCR or NSFR appears anywhere in the FY2015 edition - structurally so, since none was a "
    "UK disclosure requirement at 31 March 2015. Its liquidity discussion is the then-current ILAA regime, "
    "narrative only."
)


def p3_sources():
    return (
        "Sources - Persia International Bank Plc entity-level capital disclosures:\n"
        f"FY2025/FY2024: Annual Report and Financial Statements 2025, Note 25 (Capital management), p.77 - {AR2025_URL}\n"
        f"FY2023/FY2022: Annual Report and Financial Statements 2023, Note 26 (Capital management), p.62 - {AR2023_URL}\n"
        f"FY2021: Annual Report and Financial Statements 2022, Note 26 (Capital management), p.58 - {AR2022_URL}\n"
        f"FY2021 Pillar 3: Persia International Bank Pillar 3 Disclosure 2021, pp.16-20 and 26 - {PILLAR3_2021_URL}\n"
        + FY2015_P3_NOTE + "\n"
        "The Bank states in the FY2023-FY2025 annual reports that Pillar 3 disclosures are made separately and can "
        "be made available on request; no public 2022-2025 Pillar 3 document was locatable. The 2021 Pillar 3 document "
        "is unaudited and provides the only directly disclosed FY2021 RWA, LCR and leverage values used here.\n\n"
        + P3_CESSATION_NOTE + "\n\n" + LINK_PROVENANCE
    )


# RATE DIRECTION (corrected 2026-09-16, research/RESUME_fx_scale_sweep.md).
# The rates below are GBP PER EUR, so the conversion is  GBP = EUR * rate.
# These four helpers previously DIVIDED, on the strength of a comment claiming
# the rates were "EUR per GBP"; that comment was wrong and every converted
# figure in this workbook was overstated by 1/rate^2 (~1.43x). Proven twice:
#  1. The Bank's own FY2025 Annual Report, Note 2.1 "Basis of preparation and
#     currency" (p.40): "The euro is both the functional and presentation
#     currency ... Amounts are rounded to the nearest thousand euros ... The
#     average exchange rate for EUR/GBP applied during the year was 0.8390
#     (2023/24: 0.8630). The year-end exchange rate used was 0.8350 (2023/24:
#     0.8550)." Those are AVG_RATE/YEAR_END_RATE FY2025 and FY2024 exactly. At
#     31 Mar 2025 EUR1 bought GBP0.8358 and GBP1 bought EUR1.1965, so 0.8350 can
#     only be pounds-per-euro. No rate in either table is above 1.0, and an
#     EUR-per-GBP rate was never below 1.0 in the FY2015-FY2025 window.
#  2. Bank Sepah International (build_bank_sepah_international.py) is the same
#     shape - Iranian-owned UK bank, EUR presentation, 31 March year-end - and
#     discloses near-identical rates (FY2025 0.8354/0.8418, FY2024 0.8548/0.8636
#     against Persia's 0.8350/0.8390 and 0.8550/0.8630). It documents them as
#     "i.e. GBP per EUR 1" and MULTIPLIES. The two banks cannot both be right.
# Every ratio is unaffected: numerator and denominator are converted by the same
# factor, so this is scale-invariant and no printed ratio moves.


def flow(values):
    return {y: round(v * AVG_RATE[y], 1) if y in AVG_RATE else v for y, v in values.items()}


def stock(values):
    return {y: round(v * YEAR_END_RATE[y], 1) if y in YEAR_END_RATE else v for y, v in values.items()}


bw = BankWorkbook(bank_name="Persia International Bank Plc", years=YEARS, year_label=YEAR_LABEL, header_color="6B3E75")


def stock_v(v, y):  # GBP = EUR * rate - see the RATE DIRECTION note above
    if y not in YEAR_END_RATE:
        return v
    return round(v * YEAR_END_RATE[y], 1)


def flow_v(v, y):  # GBP = EUR * rate - see the RATE DIRECTION note above
    if y not in AVG_RATE:
        return v
    return round(v * AVG_RATE[y], 1)


STATEMENTS_SOURCES = (
    "Sources - Persia International Bank Plc's own entity-level Statement of Comprehensive Income / Statement of "
    "Financial Position / Statement of Changes in Equity / Note 12 (Impairment) / Notes 14-16 (Cash, Loans to "
    "banks, Loans to customers), converted from EUR to GBP using the Bank's disclosed rates (see FX note):\n"
    f"FY2025: Annual Report and Financial Statements 2025, Statement of Comprehensive Income p.36, Statement of "
    f"Financial Position p.37, Statement of Changes in Equity p.38, Note 12 p.69, Notes 14-16 p.71, Credit loss "
    f"exposure/Capital management (Note 25) p.77 - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements 2024, Statement of Comprehensive Income p.29, Statement of "
    f"Financial Position p.30, Statement of Changes in Equity p.31, Note 12 p.57, Notes 14-16 p.59 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, Statement of Comprehensive Income p.28, Statement of "
    f"Financial Position p.29, Statement of Changes in Equity p.30, Note 12 p.54, Notes 14-16 p.56 - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2022, Statement of Comprehensive Income p.27, Statement of "
    f"Financial Position p.28, Statement of Changes in Equity p.29, Note 12 p.51, Notes 14-16 p.53 - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2022's own comparative column (same pages as FY2022 above, "
    f"this is the latest filing that still contains a full FY2021 column) - {AR2022_URL}\n"
    f"FY2020: Annual Report and Financial Statements for year ended 31 March 2020, Statement of Comprehensive "
    f"Income p.26, Statement of Financial Position p.27, Note 28.4 (Capital management) p.62, Note 28.2 (stage-level "
    f"credit exposure) p.61 (scanned Companies House filing) - {AR2020_URL}\n"
    f"FY2019: Annual Report and Financial Statements for year ended 31 March 2019, Statement of Comprehensive "
    f"Income p.22, Statement of Financial Position p.23, Note 28.4 (Capital management) p.58, Note 28 (stage-level "
    f"credit exposure) p.57 (scanned filing) - {AR2019_URL}\n"
    f"FY2018: Annual Report and Financial Statements for year ended 31 March 2018, Statement of Comprehensive "
    f"Income p.15, Statement of Financial Position p.16, capital management note p.31, loan-portfolio note p.30 "
    f"(scanned filing) - {AR2018_URL}\n"
    f"FY2017: Annual Report and Financial Statements for year ended 31 March 2017, Statement of Comprehensive "
    f"Income p.13, Statement of Financial Position p.14, capital management note p.28, loan-portfolio note p.27 "
    f"(scanned filing) - {AR2017_URL}\n"
    f"FY2016: Annual Report and Financial Statements for year ended 31 March 2016, Statement of Comprehensive "
    f"Income p.13, Statement of Financial Position p.14, capital management note p.27, loan-portfolio note p.26 "
    f"(scanned filing) - {AR2016_URL}\n"
    f"FY2015: Annual Report and Financial Statements for year ended 31 March 2015, Statement of Comprehensive "
    f"Income p.12, Statement of Financial Position p.13, capital management note p.31, loan-portfolio note p.30 "
    f"(scanned filing, includes an embedded Pillar 3 disclosure at pp.35-52) - {AR2015_URL}\n\n"
    + ENTITY_NOTE + "\n" + FX_NOTE + "\n\n"
    "RESTATEMENT: the Annual Report and Financial Statements 2024's own Note 33 restates the Bank's FY2022/FY2023 "
    "figures (e.g. FY2023 closing retained earnings restated from EUR (17,439k) to EUR (18,414k), a genuine "
    "EUR 975k downward adjustment; FY2023 loans and advances to customers also restated from EUR 24,653k net to "
    "EUR 28,105k net, reclassifying interest receivable into that line). Each year's Balance Sheet/P&L/Equity "
    "column here uses that year's own originally-reported figures (not the later restated comparative), "
    "consistent with every other bank in this project; the restatement is instead shown as its own explicit "
    "bridging row in the Statement of Changes in Equity, between FY2023's originally-reported closing balance "
    "and FY2024's own restated opening balance, per the Bank's own Note 33.\n\n"
    "DEBT SECURITIES BREAKDOWN: Note 12 (Debt securities) of both the FY2015 (p.23 of the scanned Companies House "
    "filing) and FY2016 (p.23 of the scanned Companies House filing) Annual Reports states the entire Debt securities "
    "balance is one unlisted Sukuk (Islamic) bond, classified as \"Available for sale securities - other debt "
    "securities\" and \"Issued by other than public bodies\" - i.e. 100% one measurement-basis bucket "
    "(available-for-sale/mark-to-market, no amortised-cost or FVTPL component) and 100% one issuer-type bucket "
    "(not UK government/gilts/sovereign - a non-public-body, corporate-type issuer) in both years, so no sub-row "
    "split is added; the Balance Sheet row is instead relabelled in place to state both classifications. FY2015's "
    "note carries a 90.56% impairment provision against this bond; FY2016's note raises that provision to 100% (an "
    "additional EUR 416k impairment, matching the P&L's 'Impairment charge for available-for-sale financial assets' "
    "row), which is why the FY2016 balance is nil."
)

# ---------------------------------------------------------------
# Balance Sheet - equity reconciliation ladder confirmed: every year's own
# closing Total equity ties exactly to both the next year's own opening
# balance and that year's own Statement of Changes in Equity closing row,
# using each year's own originally-reported figures (see RESTATEMENT note
# above for the one genuine bridging item, FY2023->FY2024).
# ---------------------------------------------------------------
bs_rows_eur = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalent", {"FY2025": 77114, "FY2024": 75472, "FY2023": 51929, "FY2022": 103084, "FY2021": 25484,
        "FY2020": 27443, "FY2019": 28882, "FY2018": 30018, "FY2017": 83613, "FY2016": 151493, "FY2015": 147831}),
    ("DATA", "Loans and advances to banks", {"FY2025": 45768, "FY2024": 48056, "FY2023": 122438, "FY2022": 67577, "FY2021": 151008,
        "FY2020": 151026, "FY2019": 117079, "FY2018": 130981, "FY2017": 78708, "FY2016": 14732, "FY2015": 10336}),
    ("DATA", "Loans and advances to customers", {"FY2025": 27178, "FY2024": 49438, "FY2023": 24653, "FY2022": 32356, "FY2021": 36278,
        "FY2020": 34366, "FY2019": 13853, "FY2018": 15512, "FY2017": 28316, "FY2016": 44775, "FY2015": 50022}),
    ("DATA", "Debt securities - other debt securities, available-for-sale, issued by other than public bodies (unlisted Sukuk/Islamic Bonds; FY2015/FY2016 own reports only; no equivalent line FY2017 onward)", {"FY2016": 0, "FY2015": 435}),
    ("DATA", "Property, plant and equipment", {"FY2025": 2855, "FY2024": 3193, "FY2023": 4510, "FY2022": 3432, "FY2021": 3318,
        "FY2020": 4195, "FY2019": 4357, "FY2018": 4199, "FY2017": 4479, "FY2016": 4353, "FY2015": 4456}),
    ("DATA", "Intangible assets (FY2023 report shows this line as nil/dash; FY2015-FY2017 own reports have no separate line)", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 89, "FY2021": 268,
        "FY2020": 446, "FY2019": 625, "FY2018": 803}),
    ("DATA", "Other assets", {"FY2025": 2577, "FY2024": 1984, "FY2023": 1305, "FY2022": 2698, "FY2021": 1397,
        "FY2020": 1557, "FY2019": 901, "FY2018": 1285, "FY2017": 1070, "FY2016": 6074, "FY2015": 11021}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 134, "FY2024": 147, "FY2023": 3971, "FY2022": 652, "FY2021": 723,
        "FY2020": 961, "FY2019": 840, "FY2018": 1331, "FY2017": 1364, "FY2016": 748, "FY2015": 783}),
    ("DATA", "Current tax (FY2015-FY2019 own reports only; FY2020's own report shows this line as nil/dash)", {"FY2019": 192, "FY2018": 189, "FY2017": 193, "FY2016": 209, "FY2015": 129}),
    ("TOTAL", "Total assets", {"FY2025": 155626, "FY2024": 178290, "FY2023": 208806, "FY2022": 209888, "FY2021": 218476,
        "FY2020": 219994, "FY2019": 166729, "FY2018": 184318, "FY2017": 197743, "FY2016": 222384, "FY2015": 225013}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks", {"FY2025": 37468, "FY2024": 41447, "FY2023": 68704, "FY2022": 69319, "FY2021": 78551,
        "FY2020": 83609, "FY2019": 23545, "FY2018": 33881, "FY2017": 43334, "FY2016": 65074, "FY2015": 66801}),
    ("DATA", "Deposits from customers", {"FY2025": 4597, "FY2024": 5603, "FY2023": 5608, "FY2022": 6313, "FY2021": 6270,
        "FY2020": 6299, "FY2019": 6670, "FY2018": 2880, "FY2017": 1534, "FY2016": 2687, "FY2015": 2732}),
    ("DATA", "Other liabilities / Provisions and accruals (FY2015-FY2018 own reports label this 'Provisions and accruals'; FY2019-FY2020 own reports use 'Other liabilities')", {"FY2025": 3137, "FY2024": 3547, "FY2023": 1933, "FY2022": 2498, "FY2021": 3011,
        "FY2020": 2405, "FY2019": 2415, "FY2018": 2755, "FY2017": 2524, "FY2016": 2624, "FY2015": 2983}),
    ("DATA", "Subordinated debt liabilities (FY2015-FY2020 own reports only; converted/extinguished by FY2021 - see the Statement of Changes in Equity's FY2021 share-capital-issued row)", {"FY2020": 46500, "FY2019": 46500, "FY2018": 46500, "FY2017": 46500, "FY2016": 46500, "FY2015": 46500}),
    ("TOTAL", "Total liabilities", {"FY2025": 45202, "FY2024": 50597, "FY2023": 76245, "FY2022": 78130, "FY2021": 87832,
        "FY2020": 138813, "FY2019": 79130, "FY2018": 86016, "FY2017": 93892, "FY2016": 116885, "FY2015": 119016}),
    ("SECTION", "Shareholders' equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 150000, "FY2024": 150000, "FY2023": 150000, "FY2022": 150000, "FY2021": 150000,
        "FY2020": 100000, "FY2019": 100000, "FY2018": 100000, "FY2017": 100000, "FY2016": 100000, "FY2015": 100000}),
    ("DATA", "Retained earnings", {"FY2025": -39576, "FY2024": -22307, "FY2023": -17439, "FY2022": -18242, "FY2021": -19356,
        "FY2020": -18819, "FY2019": -12401, "FY2018": -1698, "FY2017": 3851, "FY2016": 5499, "FY2015": 5997}),
    ("TOTAL", "Total shareholders' equity", {"FY2025": 110424, "FY2024": 127693, "FY2023": 132561, "FY2022": 131758, "FY2021": 130644,
        "FY2020": 81181, "FY2019": 87599, "FY2018": 98302, "FY2017": 103851, "FY2016": 105499, "FY2015": 105997}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 155626, "FY2024": 178290, "FY2023": 208806, "FY2022": 209888, "FY2021": 218476,
        "FY2020": 219994, "FY2019": 166729, "FY2018": 184318, "FY2017": 197743, "FY2016": 222384, "FY2015": 225013}),
]
bs_rows = [(kind, label, {y: stock_v(v, y) for y, v in values.items()}) for kind, label, values in bs_rows_eur]

bw.add_balance_sheet_sheet(
    title="Persia International Bank Plc — Balance Sheet",
    subtitle="Entity-level basis, £'000 converted from EUR (see FX note; FY2015/FY2016 figures are EUR '000, unconverted - "
              "no year-end EUR/GBP rate is disclosed for those two years). Each year shown on its own originally-reported basis - "
              "see the RESTATEMENT note for a genuine FY2022/FY2023 restatement disclosed in the Annual Report and Financial "
              "Statements 2024's own Note 33, bridged explicitly in the Statement of Changes in Equity rather than blended here. "
              "'Deposits from banks'/'Deposits from customers' are labelled 'Due to other banks'/'Customer accounts' in the "
              "Bank's own FY2015-FY2020 reports.",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=100,
    source_height=500,
    unit_suffix=" (£'000, conv. from EUR)",
)

# ---------------------------------------------------------------
# Profit & Loss - each year's own reported structure preserved as-is
# (genuine structural differences across years, not blended): FY2021/
# FY2022's own reports show Net operating income before Administrative
# expenses/Depreciation/impairment reversal; FY2023's own report moves the
# net impairment charge/reversal into that same subtotal instead; FY2024/
# FY2025's own reports use a "Credit impairment" line within Net operating
# income and drop the standalone "Reversal of impairment" line entirely.
# ---------------------------------------------------------------
pl_rows_eur = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest and similar income", {"FY2025": 7044, "FY2024": 7890, "FY2023": 6767, "FY2022": 3644, "FY2021": 3965,
        "FY2020": 2406, "FY2019": 1524, "FY2018": 2696, "FY2017": 4245, "FY2016": 5540, "FY2015": 5142}),
    ("DATA", "Interest and similar expenses", {"FY2025": -357, "FY2024": -297, "FY2023": -198, "FY2022": -456, "FY2021": -302,
        "FY2020": -368, "FY2019": -12, "FY2018": -35, "FY2017": -33, "FY2016": -45, "FY2015": -44}),
    ("TOTAL", "Net Interest Income", {"FY2025": 6687, "FY2024": 7593, "FY2023": 6569, "FY2022": 3188, "FY2021": 3663,
        "FY2020": 2038, "FY2019": 1512, "FY2018": 2661, "FY2017": 4212, "FY2016": 5495, "FY2015": 5098}),
    ("DATA", "Loan impairment (charge)/credit (FY2015-FY2018 own reports only, shown mid-statement; FY2019 onward split out below as its own late-statement line)", {"FY2018": 0, "FY2017": 1353, "FY2016": -251, "FY2015": -238}),
    ("DATA", "Impairment charge for available-for-sale financial assets (FY2016 own report only)", {"FY2016": -416}),
    ("TOTAL", "Net interest income after loan impairments (FY2015-FY2018 own reports only - those years' own statements carry this subtotal; FY2019 onward do not)", {"FY2018": 2661, "FY2017": 5565, "FY2016": 4828, "FY2015": 4860}),
    ("DATA", "Fees and commission income", {"FY2025": 75, "FY2024": 340, "FY2023": 444, "FY2022": 175, "FY2021": 184,
        "FY2020": 1565, "FY2019": 122, "FY2018": 54, "FY2017": 20, "FY2016": 31, "FY2015": 38}),
    ("DATA", "Fees and commission expense", {"FY2025": -14, "FY2024": -47, "FY2023": -109, "FY2022": -81, "FY2021": -22,
        "FY2020": -15, "FY2019": -216, "FY2018": -219, "FY2017": -156, "FY2016": -21, "FY2015": -15}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 61, "FY2024": 293, "FY2023": 335, "FY2022": 94, "FY2021": 162,
        "FY2020": 1550, "FY2019": -94}),
    ("DATA", "Other operating (expense)/income", {"FY2025": -315, "FY2024": -1347, "FY2023": 686, "FY2022": 1611, "FY2021": 842,
        "FY2020": 3, "FY2019": 150, "FY2018": 245, "FY2017": 212, "FY2016": 214, "FY2015": 46}),
    ("TOTAL", "Net fee, commission and other operating income (FY2015-FY2018 own reports only - those years' own statements sum fees and other operating income into one subtotal)", {"FY2018": 80, "FY2017": 76, "FY2016": 224, "FY2015": 69}),
    ("TOTAL", "Net operating income (FY2019/FY2020 own reports only - those years' own statements carry this subtotal, before administrative expenses)", {"FY2020": 3591, "FY2019": 1568}),
    ("DATA", "Credit impairment / Net impairment (charge)/reversal (FY2025/FY2024's own report labels this 'Credit impairment'; FY2023's own report labels it 'Net impairment (charge)/reversal')", {"FY2025": -16719, "FY2024": -3137, "FY2023": -1374}),
    ("TOTAL", "Net operating (loss)/income", {"FY2025": -10286, "FY2024": 3402, "FY2023": 6216, "FY2022": 4893, "FY2021": 4667}),
    ("DATA", "Administrative expenses", {"FY2025": -6643, "FY2024": -6964, "FY2023": -6332, "FY2022": -5261, "FY2021": -5263,
        "FY2020": -5087, "FY2019": -7131, "FY2018": -7914, "FY2017": -7035, "FY2016": -5568, "FY2015": -4220}),
    ("DATA", "Depreciation", {"FY2025": -340, "FY2024": -331, "FY2023": -185, "FY2022": -252, "FY2021": -313,
        "FY2020": -388, "FY2019": -462, "FY2018": -376, "FY2017": -254, "FY2016": -191, "FY2015": -96}),
    ("TOTAL", "Total operating expenses (FY2019/FY2020 own reports only)", {"FY2020": -5475, "FY2019": -7593}),
    ("DATA", "Net impairment (loss)/credit (FY2019/FY2020 own reports only - those years' own statements show this as a single late-statement line rather than a mid-statement loan-impairment charge)", {"FY2020": -4534, "FY2019": 186}),
    ("DATA", "Impairment of property (FY2021 only, per that year's own report)", {"FY2021": -542}),
    ("DATA", "Reversal of impairment / Net impairment reversal (FY2021-FY2023's own reports only; FY2024/FY2025's own reports fold this into 'Credit impairment' above instead)", {"FY2023": 1104, "FY2022": 1734, "FY2021": 914}),
    ("TOTAL", "Total operating expenses", {"FY2025": -6983, "FY2024": -7295, "FY2023": -5413, "FY2022": -3779, "FY2021": -5204}),
    ("TOTAL", "Profit/(loss) before tax", {"FY2025": -17269, "FY2024": -3893, "FY2023": 803, "FY2022": 1114, "FY2021": -537,
        "FY2020": -6418, "FY2019": -5839, "FY2018": -5549, "FY2017": -1648, "FY2016": -707, "FY2015": 613}),
    ("DATA", "Tax on profit", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0,
        "FY2020": 0, "FY2019": 0, "FY2018": 0, "FY2017": 0, "FY2016": 209, "FY2015": -95}),
    ("TOTAL", "Profit/(loss) for the year attributable to equity holders", {"FY2025": -17269, "FY2024": -3893, "FY2023": 803, "FY2022": 1114, "FY2021": -537,
        "FY2020": -6418, "FY2019": -5839, "FY2018": -5549, "FY2017": -1648, "FY2016": -498, "FY2015": 518}),
    ("TOTAL", "Total comprehensive income/(expense) for the year attributable to equity holders", {"FY2025": -17269, "FY2024": -3893, "FY2023": 803, "FY2022": 1114, "FY2021": -537,
        "FY2020": -6418, "FY2019": -5839, "FY2018": -5549, "FY2017": -1648, "FY2016": -498, "FY2015": 518}),
]
pl_rows = [(kind, label, {y: flow_v(v, y) for y, v in values.items()}) for kind, label, values in pl_rows_eur]

bw.add_income_statement_sheet(
    title="Persia International Bank Plc — Profit & Loss",
    subtitle="Entity-level basis, £'000 converted from EUR (see FX note). Structure genuinely differs year to year - see the "
              "'Credit impairment / Net impairment (charge)/reversal' and 'Reversal of impairment' row notes. FY2021's own "
              "report uniquely shows a standalone 'Impairment of property' charge alongside a separate impairment reversal. "
              "The Bank reports no OCI in any year - Total comprehensive income/(expense) equals Profit/(loss) for the year "
              "in every year. FY2015-FY2020 (EUR '000 shown for FY2015/FY2016, £'000 for FY2017-FY2020 - see FX note) use "
              "three more structures again: FY2015-FY2018's own statements subtotal 'Net interest income after loan "
              "impairments' mid-statement then fold fees/other-operating income into one combined subtotal; FY2019/FY2020's "
              "own statements instead carry a 'Net operating income' subtotal (before administrative expenses) and a "
              "'Net impairment (loss)/credit' as a single late-statement line, closer to FY2021 onward's shape.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=120,
    source_height=500,
    unit_suffix=" (£'000, conv. from EUR)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - chronological roll-forward. Ladder
# confirmed in EUR terms across all 5 years (100,000+50,000-537=150,000
# share capital / -18,819+0-537=-19,356 retained earnings roll into
# FY2021's own closing balance; each subsequent year's own profit/loss
# rolls cleanly; the one genuine break is the EUR 975k restatement
# disclosed in the Annual Report and Financial Statements 2024's own Note
# 33, shown below as its own explicit row). The very first opening
# balance (1 April 2020) cannot be converted to GBP - the Bank's disclosed
# EUR/GBP rate series in this workbook's source set only starts at
# FY2021 - so that one row is shown in EUR only, per this workbook's
# established FX-gap convention (see the Cash Flow Statement's FY2021
# opening cash note for the same convention applied there).
# ---------------------------------------------------------------
equity_headers = ["Issued share capital", "Retained earnings", "Total"]
equity_rows = [
    ("TOTAL", "At 1 April 2014 (FY2015 opening; EUR '000, unconverted - no FY2014 year-end EUR/GBP rate disclosed)", (100000, 5479, 105479)),
    ("DATA", "Profit for the year (FY2015; EUR '000, unconverted - see FX note)", (None, 518, 518)),
    ("TOTAL", "At 31 March 2015 (FY2015 closing; EUR '000, unconverted)", (100000, 5997, 105997)),
    ("DATA", "Loss for the year (FY2016; EUR '000, unconverted - see FX note)", (None, -498, -498)),
    ("TOTAL", "At 31 March 2016 (FY2016 closing; EUR '000, unconverted)", (100000, 5499, 105499)),
    ("DATA", "Loss for the year", (None, flow_v(-1648, "FY2017"), flow_v(-1648, "FY2017"))),
    ("TOTAL", "At 31 March 2017 (FY2017 closing)", (stock_v(100000, "FY2017"), stock_v(3851, "FY2017"), stock_v(103851, "FY2017"))),
    ("DATA", "Loss for the year", (None, flow_v(-5549, "FY2018"), flow_v(-5549, "FY2018"))),
    ("TOTAL", "At 31 March 2018 (FY2018 closing)", (stock_v(100000, "FY2018"), stock_v(-1698, "FY2018"), stock_v(98302, "FY2018"))),
    ("DATA", "Loss for the year", (None, flow_v(-5839, "FY2019"), flow_v(-5839, "FY2019"))),
    ("TOTAL", "At 31 March 2019 (FY2019 closing)", (stock_v(100000, "FY2019"), stock_v(-12401, "FY2019"), stock_v(87599, "FY2019"))),
    ("DATA", "Loss for the year", (None, flow_v(-6418, "FY2020"), flow_v(-6418, "FY2020"))),
    ("TOTAL", "At 31 March 2020 (FY2020 closing; source EUR 100,000 / (18,819) / 81,181)", (stock_v(100000, "FY2020"), stock_v(-18819, "FY2020"), stock_v(81181, "FY2020"))),
    ("TOTAL", "At 1 April 2020 (FY2021 opening; source EUR 100,000 / (18,819) / 81,181 - GBP conversion not available, no FY2020 year-end rate in the disclosed source set)", (None, None, None)),
    ("DATA", "Ordinary share capital issued", (flow_v(50000, "FY2021"), None, flow_v(50000, "FY2021"))),
    ("DATA", "Loss for the year", (None, flow_v(-537, "FY2021"), flow_v(-537, "FY2021"))),
    ("TOTAL", "At 31 March 2021 (FY2021 closing)", (stock_v(150000, "FY2021"), stock_v(-19356, "FY2021"), stock_v(130644, "FY2021"))),
    ("DATA", "Profit for the year", (None, flow_v(1114, "FY2022"), flow_v(1114, "FY2022"))),
    ("TOTAL", "At 31 March 2022 (FY2022 closing)", (stock_v(150000, "FY2022"), stock_v(-18242, "FY2022"), stock_v(131758, "FY2022"))),
    ("DATA", "Profit for the year", (None, flow_v(803, "FY2023"), flow_v(803, "FY2023"))),
    ("TOTAL", "At 31 March 2023 (FY2023 closing, as originally reported in the Annual Report and Financial Statements 2023)", (stock_v(150000, "FY2023"), stock_v(-17439, "FY2023"), stock_v(132561, "FY2023"))),
    ("DATA", "Prior period restatement (per the Annual Report and Financial Statements 2024's own Note 33 - a genuine EUR 975k downward adjustment to the FY2023 closing balance, not a transcription error)", (None, stock_v(-975, "FY2023"), stock_v(-975, "FY2023"))),
    ("DATA", "Loss for the year", (None, flow_v(-3893, "FY2024"), flow_v(-3893, "FY2024"))),
    ("TOTAL", "At 31 March 2024 (FY2024 closing)", (stock_v(150000, "FY2024"), stock_v(-22307, "FY2024"), stock_v(127693, "FY2024"))),
    ("DATA", "Loss for the year", (None, flow_v(-17269, "FY2025"), flow_v(-17269, "FY2025"))),
    ("TOTAL", "At 31 March 2025 (FY2025 closing)", (stock_v(150000, "FY2025"), stock_v(-39576, "FY2025"), stock_v(110424, "FY2025"))),
]

bw.add_equity_changes_sheet(
    title="Persia International Bank Plc — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, £'000 converted from EUR (see FX note; FY2015/FY2016 rows are "
              "EUR '000, unconverted - no year-end EUR/GBP rate is disclosed for those two years). Equity reconciliation "
              "ladder confirmed in EUR terms across all 11 years - zero undocumented plug rows. The one genuine bridging row "
              "(a EUR 975k prior period restatement) is disclosed by the Bank itself in Note 33 of the Annual Report and "
              "Financial Statements 2024, not an error found in this workbook. IMPORTANT: each £'000 cell below is an "
              "independent conversion of that row's own EUR figure at its own correct point-in-time rate (year-end rate for "
              "balances, average rate for in-year movements) - the £'000 column does not sum row-to-row the way the EUR "
              "figures do, because the Bank's EUR/GBP rate moves between each conversion point. This is a presentation "
              "artefact of converting a EUR-functional-currency ladder into GBP for this workbook, not a data error; treat "
              "each TOTAL row's £'000 value as independently correct, and see the underlying EUR figures (quoted in the "
              "'At 1 April 2020' row and the RESTATEMENT source note) for the figures that do tie exactly.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=110,
)

# EUR '000, each year's own published cash-flow column.  FY2021 is taken from
# the FY2022 comparative because that is the latest filing that contains it.
OPERATING_EUR = {"FY2025": 1998, "FY2024": -14216, "FY2023": 5116, "FY2022": 3399, "FY2021": -368,
    "FY2020": -27202, "FY2019": -3730, "FY2018": 7679, "FY2017": -3557, "FY2016": 10747, "FY2015": 14582}
INVESTING_EUR = {"FY2025": -2, "FY2024": -72, "FY2023": -46, "FY2022": -44, "FY2021": 0,
    "FY2020": 0, "FY2019": -63, "FY2018": -899, "FY2017": -380, "FY2016": -88, "FY2015": -166}
FINANCING_EUR = {"FY2025": -227, "FY2024": -27477, "FY2023": -1320, "FY2022": -9186, "FY2021": -1609,
    "FY2020": 59710, "FY2019": -11245, "FY2018": 0, "FY2017": 0, "FY2016": 0, "FY2015": 0}
NET_CHANGE_EUR = {"FY2025": 1787, "FY2024": -41765, "FY2023": 3750, "FY2022": -5831, "FY2021": -1977,
    "FY2020": 32508, "FY2019": -15039, "FY2018": -1323, "FY2017": -3904, "FY2016": 10558, "FY2015": 14445}
EXCHANGE_EUR = {"FY2025": -145, "FY2024": 1009, "FY2023": -44, "FY2022": 0, "FY2021": 0,
    "FY2020": 0, "FY2019": 0, "FY2018": 4, "FY2017": 33, "FY2016": -101, "FY2015": 29}
OPENING_EUR = {"FY2025": 75472, "FY2024": 116228, "FY2023": 170661, "FY2022": 176492, "FY2021": 178469,
    "FY2020": 145961, "FY2019": 160999, "FY2018": 162321, "FY2017": 166225, "FY2016": 155667, "FY2015": 141222}
CLOSING_EUR = {"FY2025": 77114, "FY2024": 75472, "FY2023": 174367, "FY2022": 170661, "FY2021": 176492,
    # FY2020: the Bank's own Statement of Cash Flows states EUR 174,469k, but its own
    # supporting reconciliation table (two lines below) sums to EUR 178,469k - a genuine
    # EUR 4,000k inconsistency in the Bank's own document (see CASH_FLOW_SOURCES note).
    # The reconciliation-table figure is used here since it ties to opening + movements.
    "FY2020": 178469, "FY2019": 145961, "FY2018": 160999, "FY2017": 162321, "FY2016": 166225, "FY2015": 155667}

closing_gbp = stock(CLOSING_EUR)
# Opening balances are the prior year's converted closing balances.  This keeps
# the cash-flow chain internally consistent when the Bank's year-end FX rates
# differ between years.  A year is omitted from this chain (opening left blank,
# per the existing FY2021 convention) wherever the *prior* year has no disclosed
# year-end rate to convert from - that break falls at FY2021 (no FY2020 rate in the
# original five-year source set - see FX_NOTE) and at FY2017 (no FY2016 rate).
# FY2016 and FY2015 are both entirely EUR (no year-end rate for either), so their
# own opening/closing figures are self-consistent EUR-to-EUR and chain normally.
opening_gbp = {
    "FY2025": closing_gbp["FY2024"],
    "FY2024": closing_gbp["FY2023"],
    "FY2023": closing_gbp["FY2022"],
    "FY2022": closing_gbp["FY2021"],
    "FY2020": closing_gbp["FY2019"],
    "FY2019": closing_gbp["FY2018"],
    "FY2018": closing_gbp["FY2017"],
    "FY2016": closing_gbp["FY2015"],
    "FY2015": OPENING_EUR["FY2015"],
}
net_change_gbp = flow(NET_CHANGE_EUR)
exchange_gbp = flow(EXCHANGE_EUR)
translation = {
    y: round(closing_gbp[y] - opening_gbp[y] - net_change_gbp[y] - exchange_gbp[y], 1)
    for y in YEARS if y in opening_gbp
}

rows = [
    ("SECTION", "Operating activities", {}),
    ("TOTAL", "Net cash flow from operating activities", flow(OPERATING_EUR)),
    ("SECTION", "Investing activities", {}),
    ("TOTAL", "Net cash flow from investing activities", flow(INVESTING_EUR)),
    ("SECTION", "Financing activities", {}),
    ("TOTAL", "Net cash flow from financing activities", flow(FINANCING_EUR)),
    ("TOTAL", "Net (decrease) / increase in cash and cash equivalents", net_change_gbp),
    ("DATA", "Exchange difference (Bank's own EUR statement line)", exchange_gbp),
    ("DATA", "Effect of GBP/EUR translation (this workbook's conversion line)", translation),
    ("DATA", "Cash and cash equivalents at the beginning of the year", opening_gbp),
    ("TOTAL", "Cash and cash equivalents at the end of the year", closing_gbp),
]

bw.add_cash_flow_sheet(
    title="Persia International Bank Plc — Statement of Cash Flows",
    subtitle="Entity-level basis, £'000 converted from EUR (FY2015/FY2016 figures are EUR '000, unconverted - no year-end "
              "EUR/GBP rate is disclosed for those two years; FY2017 and FY2021 opening cash are each left blank for the "
              "same reason, one year removed); see source note for sanctions, reporting basis and FX methodology",
    rows=rows, sources_text=CASH_FLOW_SOURCES, first_col_width=86, source_height=420,
    unit_suffix=" (£'000, conv. from EUR)",
)

# ---------------------------------------------------------------
# Asset Quality - built from Note 16's own component breakdown of Loans
# and advances to customers (ties exactly to the Balance Sheet net figure
# every year) plus Note 12's IFRS 9 stage split of the annual impairment
# charge/(reversal). FY2022's own component split (Commercial/Syndicated)
# differs from AR2023's later FY2022 comparative despite both giving the
# same net figure (32,356) - a genuine component-level reclassification
# between Syndicated Loans and the ECL allowance, not a data error; this
# year's own AR2022 component split is used, consistent with every other
# year using its own contemporaneous report. A genuine balance-level IFRS
# 9 stage exposure table (gross/allowance/net by stage, not just the
# annual charge) exists only in the Annual Report and Financial
# Statements 2025 (its own new "Credit loss exposure" disclosure, p.77) -
# shown as a FY2025-only supplementary block; no equivalent table was
# found in FY2021-FY2024's reports.
# ---------------------------------------------------------------
aq_rows_eur = [
    ("SECTION", "Loans and advances to customers (Note 16)", {}),
    ("DATA", "Commercial Loan", {"FY2025": 30473, "FY2024": 30221, "FY2023": 4235, "FY2022": 4235, "FY2021": 4235}),
    ("DATA", "Syndicated Loans", {"FY2025": 15334, "FY2024": 24276, "FY2023": 25804, "FY2022": 37408, "FY2021": 41486}),
    ("DATA", "Interest receivable (only disclosed as its own line FY2024-FY2025)", {"FY2025": 5526, "FY2024": 2634}),
    ("TOTAL", "Gross loans and advances to customers", {"FY2025": 51333, "FY2024": 57131, "FY2023": 30039, "FY2022": 41643, "FY2021": 45721}),
    ("DATA", "Less: expected credit loss allowance", {"FY2025": -24155, "FY2024": -7693, "FY2023": -5386, "FY2022": -9287, "FY2021": -9443}),
    ("TOTAL", "Net loans and advances to customers", {"FY2025": 27178, "FY2024": 49438, "FY2023": 24653, "FY2022": 32356, "FY2021": 36278}),
]
aq_rows = [(kind, label, {y: stock_v(v, y) for y, v in values.items()}) for kind, label, values in aq_rows_eur]

aq_ratio_rows_eur = [
    ("DATA", "ECL allowance coverage ratio (allowance / gross loans)", {
        "FY2025": "47.06%", "FY2024": "13.47%", "FY2023": "17.93%", "FY2022": "22.30%", "FY2021": "20.66%",
    }),
    ("SECTION", "IFRS 9 stage split of the annual impairment charge/(reversal) (Note 12)", {}),
]
aq_stage_charge_eur = [
    ("DATA", "Stage 1 - Performing - 12 months ECL", {"FY2025": -6, "FY2024": -736, "FY2023": 2652, "FY2022": 5475, "FY2021": 5009}),
    ("DATA", "Stage 2 - Performing - lifetime ECL", {"FY2025": -6293, "FY2024": -2088, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Stage 3 - Non-performing - lifetime ECL", {"FY2025": -10420, "FY2024": -313, "FY2023": -4026, "FY2022": -3741, "FY2021": -4095}),
    ("TOTAL", "Impairment (charge)/reversal for the year", {"FY2025": -16719, "FY2024": -3137, "FY2023": -1374, "FY2022": 1734, "FY2021": 914}),
]
aq_stage_charge = [(kind, label, {y: flow_v(v, y) for y, v in values.items()}) for kind, label, values in aq_stage_charge_eur]

aq_fy25_exposure_eur = [
    ("SECTION", "FY2025-only: IFRS 9 stage-level loan exposure (Credit loss exposure table, Note 25) - no equivalent balance-level stage table found in FY2021-FY2024's reports", {}),
    ("DATA", "Stage 1 gross exposure - loans and advances to customers", {"FY2025": 49}),
    ("DATA", "Stage 2 gross exposure - loans and advances to customers", {"FY2025": 28683}),
    ("DATA", "Stage 3 gross exposure - loans and advances to customers", {"FY2025": 22650}),
    ("DATA", "Stage 1 impairment allowance", {"FY2025": -5}),
    ("DATA", "Stage 2 impairment allowance", {"FY2025": -8382}),
    ("DATA", "Stage 3 impairment allowance", {"FY2025": -14757}),
    ("TOTAL", "Net exposure - loans and advances to customers, per this stage-level table (FY2025 EUR 28,238k gross-less-allowance - EUR 1,060k / ~4% higher than Note 16's EUR 27,178k net figure used above; a genuine inconsistency between two different notes in the same Annual Report, not reconciled here)", {"FY2025": 28238}),
]
aq_fy25_exposure = [(kind, label, {y: stock_v(v, y) for y, v in values.items()}) for kind, label, values in aq_fy25_exposure_eur]

# ---------------------------------------------------------------
# HD-021 extension (FY2015-FY2020) - two more structures again, both from each
# year's own "Total loan portfolio" / stage-exposure note, both tying exactly to
# that year's own Balance Sheet net "Loans and advances to customers" figure:
#   FY2015-FY2018 (IAS 39 incurred-loss basis, pre-IFRS 9): gross performing +
#   gross non-performing, less a single undifferentiated allowance.
#   FY2019/FY2020 (IFRS 9 adopted): a genuine balance-level stage exposure table,
#   the same shape as the FY2025-only block above. FY2020's own source table shows
#   its Stage 1 gross-exposure column combining what would be Stage 1 and Stage 3
#   gross exposure (Stage 3 gross is not separately given even though a Stage 3
#   allowance is disclosed) - transcribed as the Bank's own table presents it,
#   flagged rather than reconciled, consistent with the FY2025 stage-table note above.
# ---------------------------------------------------------------
aq_pre_ifrs9_eur = [
    ("SECTION", "Total loan portfolio (FY2015-FY2018 own reports; IAS 39 incurred-loss basis, pre-IFRS 9 - performing/non-performing split rather than a stage table)", {}),
    ("DATA", "Gross loans and advances to customers - performing", {"FY2018": 407, "FY2017": 6736, "FY2016": 17366, "FY2015": 19857}),
    ("DATA", "Non performing loans", {"FY2018": 19171, "FY2017": 26355, "FY2016": 33264, "FY2015": 35971}),
    ("DATA", "Less: allowance for impairment", {"FY2018": -4066, "FY2017": -4775, "FY2016": -5855, "FY2015": -5806}),
    ("TOTAL", "Net loans and advances to customers", {"FY2018": 15512, "FY2017": 28316, "FY2016": 44775, "FY2015": 50022}),
]
aq_pre_ifrs9 = [(kind, label, {y: stock_v(v, y) for y, v in values.items()}) for kind, label, values in aq_pre_ifrs9_eur]

aq_fy19_20_exposure_eur = [
    ("SECTION", "FY2019/FY2020: IFRS 9 stage-level loan exposure (own reports' Credit risk / Risk management note)", {}),
    ("DATA", "Stage 1 gross exposure - loans and advances to customers (FY2020's own table does not separately break out Stage 3 gross exposure - see note above)", {"FY2020": 45208, "FY2019": 16109}),
    ("DATA", "Stage 3 gross exposure - loans and advances to customers", {"FY2019": 4491}),
    ("DATA", "Stage 1 impairment allowance", {"FY2020": -6265, "FY2019": -2256}),
    ("DATA", "Stage 3 impairment allowance", {"FY2020": -4577, "FY2019": -4491}),
    ("TOTAL", "Net loans and advances to customers", {"FY2020": 34366, "FY2019": 13853}),
]
aq_fy19_20_exposure = [(kind, label, {y: stock_v(v, y) for y, v in values.items()}) for kind, label, values in aq_fy19_20_exposure_eur]

bw.add_asset_quality_sheet(
    title="Persia International Bank Plc — Asset Quality",
    subtitle="Entity-level basis, £'000 converted from EUR (FY2015/FY2016 figures are EUR '000, unconverted - see FX note). "
              "Net loans and advances to customers ties exactly to the Balance Sheet every year. FY2022's own component "
              "split (Commercial/Syndicated) differs from a later report's FY2022 comparative despite both giving the "
              "identical net figure (EUR 32,356k) - a genuine component-level reclassification, not a data error; this "
              "year's own contemporaneous report is used, as elsewhere in this workbook. FY2015-FY2020 (added under "
              "HD-021) use two more structures again - see the section headers below.",
    rows=aq_rows + aq_ratio_rows_eur + aq_stage_charge + aq_fy25_exposure + aq_pre_ifrs9 + aq_fy19_20_exposure,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=110,
    source_height=500,
    unit_suffix=" (£'000, conv. from EUR)",
)

def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=50, source_height=620)


CAPITAL_EUR = {"FY2025": 110424, "FY2024": 127693, "FY2023": 132561, "FY2022": 131758, "FY2021": 130644}
CAPITAL_GBP = stock(CAPITAL_EUR)
RWA_GBP = {"FY2021": round(318824 * YEAR_END_RATE["FY2021"], 1)}  # GBP = EUR * rate
NOT_DISCLOSED = (
    "Not publicly disclosed for this entity/year. The Bank says later Pillar 3 disclosures are available on request; "
    "no public 2022-2025 Pillar 3 document was found, and the statutory accounts do not state this metric.\n\n"
    "RE-VERIFIED 2026-09-12 (independent disclosure re-audit). The FY2023 and FY2025 Annual Reports were "
    "re-downloaded from Companies House and fully OCR'd page-by-page (both are scanned filings with no text "
    "layer). Findings:\n"
    "- Both reports carry a 'Pillar 3 Disclosures' heading whose entire content is the sentence \"Pillar 3 "
    "disclosures are made separately and can be made available on request.\" - unchanged in the most recent "
    "(year ended 31 March 2025) filing.\n"
    "- The statutory 'Capital management' note (Note 26 in FY2023, Note 25 in FY2025) gives ONLY the capital "
    "base build-up (Ordinary share capital + Retained earnings = Total regulatory capital base) in EUR '000. "
    "It explicitly describes the PRA's requirement as \"based upon the ratio of capital to total risk weighted "
    "exposures\" but publishes NO risk-weighted exposure figure and NO resulting ratio, in any year FY2022 "
    "onward. The capital amounts it does give are already captured on the CET1/Tier 1/Total Capital sheets "
    "(FY2025 EUR110,424k and FY2024 EUR127,693k re-confirmed against this note directly).\n"
    "- Capital adequacy is referred to only in narrative terms (\"The Tier I Capital ratios are still robust\", "
    "\"The Bank maintains a strong capital adequacy ratio and liquidity position\") with no percentage attached.\n"
    "- The Bank's own website was recorded that session as entirely unreachable (DNS/connection failure, "
    "HTTP 000). CORRECTED 2026-09-15: the site is reachable, but only over plain HTTP - "
    "http://www.persiabank.co.uk/ answers 200; the HTTPS URL still fails the TLS handshake, which is what "
    "earlier sessions were hitting. Reading the live site does not change the conclusion: its complete link "
    "list carries exactly one Pillar 3 document, the FY2021 edition, and no later one. A full Wayback Machine "
    "CDX listing of the domain agrees - the newest Pillar 3 document ever archived is that same FY2021 "
    "edition ('Pillar 3 2021 v3.pdf', still being re-crawled as recently as 2025-12-25), and the domain was "
    "actively crawled through 2024-2025, so this is the latest edition that exists, not a crawl gap. No 2022, "
    "2023, 2024 or 2025 Pillar 3 document has ever been published at that domain.\n\n"
    + P3_CESSATION_NOTE
)
CAPITAL_NOTE = (
    "Directly disclosed total regulatory capital base / Tier one capital from the annual-report capital-management "
    "table. The Bank's table does not separately disclose CET1, Additional Tier 1 or Tier 2 amounts for FY2022-FY2025; "
    "the value is therefore repeated as the entity's disclosed Tier one/regulatory capital base, not inferred as a full "
    "Basel capital stack. FY2021's Pillar 3 table reports Own Funds of €130.644m and Tier 2 of zero."
)

# ---------------------------------------------------------------
# HD-021 extension (FY2015-FY2020). Two source layers, used for different rows:
#   - Each year's own STATUTORY capital-management note (in the Annual Report itself)
#     gives Tier 1 = Ordinary share capital + Retained earnings (== Balance Sheet
#     Total shareholders' equity every year) and Tier 2 = the subordinated loan at
#     its full carrying value (EUR 46,500k every year). This workbook uses these
#     statutory figures for the CET1/Tier 1/Total Capital £-value sheets, consistent
#     with using each year's own accounts as the primary source elsewhere.
#   - The Bank's own standalone Pillar 3 disclosures (found for FY2016/FY2018/FY2020,
#     each of which also prints the prior year's figures as a comparative, covering
#     FY2017 and FY2019 too) separately disclose CET1/Total-capital RATIOS and RWA -
#     neither of which the statutory accounts state at all - computed against a
#     CRR-CAPPED Tier 2 (capped at 1/3 of Tier 1 from 1 January 2017) and, for
#     FY2019/FY2020, a CET1 base that nets off that year's own unaudited in-year
#     loss a second time (Pillar 3 FY2020 CET1 EUR 74,763k = statutory equity EUR
#     81,181k less that year's own EUR 6,418k loss again - a CRR prudential filter
#     for not-yet-verified profits/losses, not a transcription error). This workbook
#     uses these Pillar-3-disclosed ratios and RWA figures as-is (they cannot be
#     derived from the statutory £-values above without re-deriving the capping/
#     filter mechanics), so the ratio sheets' own capital base differs from the
#     Total Capital sheet's - flagged here rather than silently reconciled.
# FY2015 predates CRD IV Pillar 3 for a firm this size: only Tier 1/Tier 2/Total
# Capital are disclosed (no CET1, no RWA-by-risk-type split, no Leverage Ratio, no
# LCR) - see ENTITY_NOTE's Basel II/III caveat.
# ---------------------------------------------------------------
TIER1_STATUTORY_EUR = {"FY2020": 81181, "FY2019": 87599, "FY2018": 98302, "FY2017": 103851, "FY2016": 105499, "FY2015": 105997}
TIER2_STATUTORY_EUR = {"FY2020": 46500, "FY2019": 46500, "FY2018": 46500, "FY2017": 46500, "FY2016": 46500, "FY2015": 46500}
TOTAL_CAPITAL_STATUTORY_EUR = {"FY2020": 127681, "FY2019": 134099, "FY2018": 144802, "FY2017": 150351, "FY2016": 151999, "FY2015": 152497}

CET1_TIER1_PILLAR3_EUR = {"FY2020": 74763, "FY2019": 81760, "FY2018": 98302, "FY2017": 103851, "FY2016": 105499}
RWA_CREDIT_EUR = {"FY2020": 262907, "FY2019": 169506, "FY2018": 210723, "FY2017": 243264, "FY2016": 306733}
RWA_MARKET_EUR = {"FY2020": 7355, "FY2019": 6771, "FY2018": 4031, "FY2017": 3604, "FY2016": 3036}
RWA_OPERATIONAL_EUR = {"FY2020": 11212, "FY2019": 7967, "FY2018": 7967, "FY2017": 9514, "FY2016": 9998}
RWA_TOTAL_EUR_EXT = {"FY2020": 281474, "FY2019": 184244, "FY2018": 222721, "FY2017": 256382, "FY2016": 319767, "FY2015": 221221}
CET1_RATIO_EXT = {"FY2020": "28.76%", "FY2019": "50.16%", "FY2018": "44.14%", "FY2017": "40.51%", "FY2016": "32.99%"}
TOTAL_CAPITAL_RATIO_EXT = {
    "FY2020": "38.35%", "FY2019": "66.88%", "FY2018": "58.85%", "FY2017": "54.01%", "FY2016": "47.53%",
    "FY2015": "68.94%",  # FY2015: statutory Total Capital EUR 152,497k / RWA EUR 221,221k (no Pillar 3 ratio table pre-CRD IV)
}
TIER1_RATIO_FY2015 = "47.92%"  # FY2015: statutory Tier 1 EUR 105,997k / RWA EUR 221,221k (Basel II - Tier 1 ratio, no CET1 concept)
LEVERAGE_RATIO_EXT = {"FY2020": "33.77%", "FY2018": "49.27%", "FY2016": "49.99%"}
LCR_EXT = {"FY2020": "181.69%", "FY2018": "539.22%"}

CET1_TIER1_GBP_EXT = stock(CET1_TIER1_PILLAR3_EUR)
TIER1_STATUTORY_GBP = stock(TIER1_STATUTORY_EUR)
TOTAL_CAPITAL_STATUTORY_GBP = stock(TOTAL_CAPITAL_STATUTORY_EUR)
RWA_TOTAL_GBP_EXT = stock(RWA_TOTAL_EUR_EXT)

EXT_CAPITAL_NOTE = (
    "FY2015-FY2020 (added under HD-021): the £-value shown is each year's own STATUTORY capital-management note "
    "(Tier 1 = share capital + retained earnings, tying to the Balance Sheet; FY2016-FY2018 CET1 equals this "
    "statutory Tier 1 exactly). FY2019/FY2020 differ: the Bank's own Pillar 3 disclosure nets off that year's own "
    "in-year loss from CET1 a second time (a CRR prudential filter for unverified profit/loss - see the block "
    "comment above); the Pillar-3-disclosed CET1 figure is shown for FY2019/FY2020 instead of the statutory Tier 1 "
    "figure used for FY2015-FY2018, FY2016-FY2018 and FY2021-FY2025. FY2015 has no CET1 concept at all (pre-CRD IV "
    "Pillar 3 for a firm this size) - its Tier 1 figure appears only on the Tier 1 Capital sheet."
)
EXT_TOTAL_CAPITAL_NOTE = (
    "FY2015-FY2020 (added under HD-021): each year's own statutory capital-management note, Tier 1 (share capital + "
    "retained earnings) plus Tier 2 (the EUR 46,500k subordinated loan at full carrying value, not the CRR-capped "
    "amount used in the Pillar-3-disclosed capital ratios on the Total Capital Ratio sheet)."
)
FY2021_RATIO_NOTE = (
    "FY2021 CORRECTION 2026-09-15: this sheet previously read \"Not publicly disclosed\" for FY2021. That was wrong. "
    "The Bank's Pillar 3 Disclosure as at 31 March 2021 - already cited on this workbook's Total RWAs, Leverage Ratio, "
    "LCR and RWA Breakdown sheets - states the ratios directly in section 3.4 'Capital Buffers', p.19: \"CET1 (and "
    "Tier 1) capital ratio (%) 40.99%\" and \"Total capital ratio (%) 40.99%\" for 31/03/2021 (comparative 31/03/2020: "
    "28.76% and 38.35%, which is where this workbook's FY2020 figures already came from). The document adds \"As the "
    "Bank's Tier 1 capital is entirely made of CET1 capital, the Tier 1 and CET1 ratios are the same\", which is why "
    "all three ratio sheets carry the identical FY2021 figure. It is internally consistent with the rest of the "
    "workbook: Total Capital EUR 130,644k / Pillar 1 RWAs EUR 318,824k = 40.98%, and FY2021 is the year the EUR "
    "46,500k subordinated loan fell to zero, so there is no Tier 2 to separate the Total Capital Ratio from the CET1 "
    "Ratio. The figures are transcribed, not derived. The earlier blank was a sourcing miss - the FY2021 document was "
    "opened for its RWA, leverage and LCR tables but not for its capital-ratio table."
)
EXT_RATIO_NOTE = (
    "FY2015-FY2020 (added under HD-021): FY2016-FY2020 are directly disclosed in the Bank's own standalone Pillar 3 "
    "disclosures (found for FY2016/FY2018/FY2020; FY2017/FY2019 are those documents' own comparative columns). "
    "FY2015 predates CRD IV Pillar 3 for a firm this size (no CET1 concept, no ratio table); the FY2015 figure shown "
    "on the Total Capital Ratio / Tier 1 Ratio sheets is this workbook's own calculation from the FY2015 statutory "
    "Total Capital/Tier 1 figures divided by the FY2015 Pillar 3 disclosure's own Total RWA figure (EUR 221,221k, "
    "the 'Breakdown of exposure classes' table's own total - not the same total as its mislabelled Template CR4 "
    "table, see the RWA Breakdown sheet's note).\n"
    "FY2015 RATIO WARNING, ADDED 2026-09-15 - READ BEFORE USING THE FY2015 RATIO CELLS. The Bank's standalone "
    "FY2015 Pillar 3 edition has now been recovered from the Internet Archive and read in full, and it confirms "
    "two things. First, that no capital ratio of ANY kind is printed anywhere in it - so the FY2015 ratio cells "
    "are, as stated above, calculated here rather than transcribed, which already makes them weaker than every "
    "other cell on these sheets. Second, and worse, that the denominator they use is wrong: the EUR 221,221k is "
    "the CREDIT-RISK RWA only. That edition separately discloses an FX spot position risk of EUR 4,128k and an "
    "operational risk risk-weighted exposure of EUR 11,501k, neither of which is inside the 221,221k, and it "
    "prints no Pillar 1 total at all. The FY2015 ratios shown are therefore OVERSTATED: on the three components' "
    "arithmetic sum of EUR 236,850k, the Total Capital Ratio would be about 64.4% rather than 68.94% and the "
    "Tier 1 Ratio about 44.8% rather than 47.92%.\n"
    "THE CELLS ARE LEFT AS THEY WERE, on purpose. Replacing one calculated ratio with another calculated ratio is "
    "not a transcription improvement, and no FY2015 total RWA exists in any document to divide by. This workbook "
    "does not have a defensible FY2015 capital ratio and the honest reading of these two cells is that they are "
    "an upper bound, not a measurement. Flagged for a decision rather than silently adjusted or silently left."
)
EXT_RWA_NOTE = (
    "FY2015-FY2020 (added under HD-021): FY2016-FY2020 RWA (credit/market/operational) are directly disclosed in "
    "the Bank's own standalone Pillar 3 disclosures, same sourcing as the ratio sheets, and each of those editions "
    "prints its own explicit Pillar 1 total (FY2016's reads 'Total Pillar 1 risk 319,767'), so those years' figures "
    "on this sheet are genuine totals.\n"
    "FY2015 IS NOT A TOTAL AND MUST NOT BE READ AS ONE - corrected 2026-09-15 after the Bank's standalone FY2015 "
    "Pillar 3 edition was recovered from the Internet Archive and read in full. The EUR 221,221k shown for FY2015 "
    "is the total line of that edition's 'Breakdown of exposure classes' table (repeated as its Template CR4 "
    "total), and all six rows of that table are CREDIT exposure classes; the printed 17,698k capital charge beside "
    "it is exactly 8% of it. The same document separately discloses, in two narrative sentences elsewhere, an FX "
    "spot position risk of EUR 4,128k (section 6, p.14) and an operational risk risk-weighted exposure of EUR "
    "11,501k (section 7, p.15) - NEITHER of which is in the 221,221k. The edition prints no Pillar 1 total "
    "anywhere. So FY2015's true total RWA is materially higher than 221,221k, by roughly 7%. This is the same "
    "credit-risk-subtotal-presented-as-a-total defect confirmed at Redwood, Ghana International and Bank of "
    "Ceylon.\n"
    "IT IS FLAGGED RATHER THAN FIXED, deliberately. No document states a FY2015 total, so adding the three "
    "components to 236,850k and putting that here would substitute a figure this workbook computed for one the "
    "Bank disclosed - which this project does not do on this sheet. The component sum is instead shown on its own "
    "clearly-labelled row of the RWA Breakdown sheet, where it can be seen but cannot be mistaken for a "
    "disclosure. CONSEQUENCE FOR THE RATIO SHEETS: the FY2015 Total Capital Ratio (68.94%) and Tier 1 Ratio "
    "(47.92%) in this workbook are this workbook's own calculations using 221,221k as the denominator, so they are "
    "OVERSTATED - on the 236,850k component sum they would be about 64.4% and 44.8%. Those cells are flagged on "
    "their own sheets and left unchanged pending a decision, because replacing a calculated ratio with a "
    "differently-calculated ratio is not an improvement in transcription terms."
)
EXT_LEVERAGE_LCR_NOTE = (
    "FY2015-FY2020 (added under HD-021): directly disclosed in the Bank's own standalone Pillar 3 disclosures where "
    "found (FY2016/FY2018/FY2020). No leverage ratio is disclosed in the FY2017 or FY2019 Pillar 3 comparative "
    "columns (only the current year's leverage ratio is tabulated in each document), and the EBA's LCR disclosure "
    "guidelines only applied from 31 December 2017 - so FY2015-FY2017 LCR, and FY2015 leverage ratio, are genuinely "
    "not disclosed anywhere located, not a gap in this transcription. FY2019's LCR similarly falls in a gap between "
    "the FY2018 and FY2020 Pillar 3 documents' own quarterly disclosure windows (neither one's table includes a "
    "31 March 2019 quarter)."
)

# ---------------------------------------------------------------
# KM1 Key Metrics - NOT APPLICABLE. KM1-024, 16 September 2026.
#
# Two independent reasons, either of which would be enough on its own:
#
#   (a) THE TEMPLATE IS NOT USED in any edition PIB published. Every Pillar 3
#       the Bank ever issued organises itself by its own section headings -
#       Own Funds / Capital Requirements / Total Capital Requirement / Capital
#       Buffers / Credit Risk / Market Risk / Operational Risk / Concentration
#       Risk / IRRBB / Leverage Ratio / Remuneration - with bespoke tables in
#       EUR '000 and no template row numbers anywhere.
#
#   (b) EVERY EDITION PREDATES THE UK KM1 TEMPLATE. PIB's newest Pillar 3 is
#       31 March 2021. The UK KM1 arrived with the PRA Rulebook's Disclosure
#       (CRR) Part on 1 January 2022, and the Bank published no Pillar 3 after
#       that date - see P3_CESSATION_NOTE, which is evidenced from the Bank's
#       own Annual Reports rather than inferred from a failed search.
#
# HOW THE ABSENCE WAS TESTED, so it is not mistaken for a tooling failure.
# Case-insensitive probes of every text-native edition (FY2021, FY2020, FY2018,
# FY2016) return ZERO hits for "km1", "key metric" and "key regulatory", while
# the SAME extraction is rich on neighbouring terms (83-106 hits for "capital",
# 87-109 for "ratio", 7-9 for "cet1", 4-8 for "leverage" in each). Each
# document's own table of contents was read as well, and none lists a
# key-metrics section. The FY2015 edition is an image-only Canon scan with no
# text layer, so no grep could speak to it either way: its contents page was
# RENDERED at 200dpi and READ BY EYE instead (Introduction / Overview of Risk
# Management and RWA / Capital resources / Capital Adequacy / Risk Management /
# Market risk / Operational risk / Interest rate risk / Remuneration policy) -
# again no key-metrics section.
#
# PARENT CHECK, done before writing the non-disclosure claim. A UK subsidiary's
# regulatory figures often live in the PARENT's Pillar 3 instead of its own.
# That does not arise here: PIB is ITSELF the PRA-authorised firm and holds the
# UK disclosure duty, which is why it published a Pillar 3 at all. Its two
# shareholders, Bank Mellat and Bank Tejarat, are Iranian banks supervised by
# the Central Bank of Iran, not the PRA, so no UK KM1 for PIB could exist in
# their disclosures; both are also themselves subject to UK/EU financial
# sanctions. No group Pillar 3 covering PIB exists to search.
# ---------------------------------------------------------------
KM1_SOURCES = (
    "Sources - the UK KM1 key-metrics template is NOT used in any Persia International Bank Plc Pillar 3 "
    "disclosure, in any year. This is a positive finding about the documents, not a failed search.\n\n"
    "TWO INDEPENDENT REASONS, either sufficient on its own:\n"
    "(a) THE TEMPLATE IS NOT USED. Every edition PIB published is organised by the Bank's own section "
    "headings - Own Funds / Capital Requirements / Total Capital Requirement / Capital Buffers / Credit "
    "Risk / Market Risk / Operational Risk / Concentration Risk / IRRBB / Leverage Ratio / Remuneration - "
    "with bespoke tables of its own design and no template row numbers anywhere. Its capital table, for "
    "example, is headed 'Values in (€000)' over columns '31/03/2021' and '31/03/2020' and runs Ordinary "
    "share capital / Retained earnings / Loss of the period / Subordinated loan / Total capital, followed "
    "by an 'Own Funds items' table with an 'Own Funds' and a '% of Own Funds' column. Neither is KM1: no "
    "row numbers, no SREP rows, no combined-buffer row, no leverage rows, no LCR or NSFR template rows. "
    "Under the row-set test that is a different table, so nothing is mapped onto template row numbers.\n"
    "(b) EVERY EDITION PREDATES THE UK KM1 TEMPLATE. PIB's newest Pillar 3 is 31 March 2021. The UK KM1 "
    "template arrived with the Disclosure (CRR) Part of the PRA Rulebook on 1 January 2022, and the Bank "
    "published no Pillar 3 at all after that date (see the cessation note below, which is evidenced from "
    "the Bank's own Annual Reports). There is therefore no PIB edition in which a UK KM1 could appear.\n\n"
    "HOW THE ABSENCE WAS TESTED. Every text-native edition (31 March 2021, 2020, 2018 and 2016) was "
    "extracted with pdftotext -layout and probed CASE-INSENSITIVELY: each returns ZERO hits for 'km1', "
    "'key metric' and 'key regulatory', while the SAME extraction is rich on neighbouring terms - 83-106 "
    "hits for 'capital', 87-109 for 'ratio', 7-9 for 'cet1' and 4-8 for 'leverage' in each document. A zero "
    "beside that richness is a fact about the document rather than a failed tool. Each document's own table "
    "of contents was read as well and none lists a key-metrics section. The 31 March 2015 edition is an "
    "image-only Canon scan with NO text layer, so no grep could speak to it in either direction; its "
    "contents page was RENDERED at 200dpi and READ BY EYE instead - Introduction / Overview of Risk "
    "Management and RWA / Capital resources / Capital Adequacy / Risk Management / Market risk / "
    "Operational risk / Interest rate risk / Remuneration policy - again with no key-metrics section.\n\n"
    "LATEST-EDITION CHECK, 16 September 2026, done on the Bank's OWN site rather than from the URLs already "
    "cited here. persiabank.co.uk's home page was fetched over PLAIN HTTP (its TLS is broken at the server "
    "- see the scheme note at the top of this script) and its links enumerated. The ONLY Pillar 3 link on "
    "the Bank's entire website is 'Pillar 3 2021 v3.pdf', the 31 March 2021 edition already cited here "
    "(re-fetched and verified today: HTTP 200, application/pdf, %PDF magic bytes, 1,382,251 bytes, 29 PDF "
    "pages). No newer Pillar 3 exists on the Bank's site. For the Annual Report, Companies House (company "
    "04218020) was listed directly: the newest accounts filed are 'Full accounts made up to 31 MARCH 2025', "
    "filed 2 September 2025 - already this workbook's FY2025. The 31 March 2026 accounts were not yet filed "
    "as at 16 September 2026. Nothing newer to transcribe; YEARS is unchanged.\n"
    "Also recorded from that same page-fetch, since it bears on whether the Bank is still publishing at "
    "all: the site carries a notice dated 6 October 2025 stating that 'Persia International Bank PLC has "
    "been made subject to financial sanctions by the UK Government and the European Union as of 29 "
    "September 2025' and pointing to OFSI General Licence INT/2025/7345464. The Bank is therefore still "
    "operating and still updating its website - it simply has not published a Pillar 3 since March 2021.\n\n"
    "PARENT CHECK (done before writing this non-disclosure claim). A UK subsidiary's regulatory figures "
    "frequently live in the PARENT's Pillar 3 rather than its own. That pattern does not arise here: PIB is "
    "ITSELF the PRA-authorised firm and holds the UK disclosure obligation, which is why it published a "
    "Pillar 3 at all. Its two shareholders, Bank Mellat and Bank Tejarat, are Iranian banks supervised by "
    "the Central Bank of Iran and not by the PRA, so no UK KM1 for PIB could exist in their disclosures; "
    "both are themselves subject to UK/EU financial sanctions. No group Pillar 3 covering PIB exists to "
    "search.\n\n"
    "NOT BACK-FILLED FROM THE STATUTORY ACCOUNTS. The Bank's Companies House filings do carry capital "
    "figures, and this workbook uses them on the metric sheets for the years the Pillar 3 documents do not "
    "cover. They are statutory-accounts disclosures on a different basis, not KM1 rows, and they are not "
    "mapped onto template row numbers here.\n\n"
    + P3_CESSATION_NOTE + "\n\n" + ENTITY_NOTE
)

bw.add_km1_sheet(
    title="Persia International Bank Plc — KM1 Key Metrics",
    subtitle="Not applicable, for two independent reasons. (1) The template is not used: every Pillar 3 PIB "
             "published is organised by the Bank's own section headings with bespoke tables in EUR '000 and no "
             "template row numbers. (2) Every edition predates the template: PIB's newest Pillar 3 is 31 March "
             "2021, the UK KM1 arrived on 1 January 2022, and the Bank has published no Pillar 3 since — which "
             "its own Annual Reports state. See the source note for how the absence was tested, including the "
             "image-only 2015 edition that was rendered and read by eye.",
    rows=[
        ("DATA", "UK KM1 key-metrics template",
         {y: "Not applicable — template not used, and not published in any year" for y in YEARS}),
    ],
    sources_text=KM1_SOURCES,
    first_col_width=48,
    source_height=620,
)

metric("CET1 Capital", "£'000 (conv. from EUR)", [("Common Equity Tier 1 capital / disclosed Tier one base",
    {**CAPITAL_GBP, **CET1_TIER1_GBP_EXT, "FY2018": TIER1_STATUTORY_GBP["FY2018"], "FY2017": TIER1_STATUTORY_GBP["FY2017"], "FY2016": TIER1_STATUTORY_GBP["FY2016"]})],
    note=CAPITAL_NOTE + "\n\n" + EXT_CAPITAL_NOTE)
metric("CET1 Ratio", "%", [("CET1 ratio", {"FY2021": "40.99%", **CET1_RATIO_EXT})], note=FY2021_RATIO_NOTE + "\n\n" + NOT_DISCLOSED + "\n\n" + EXT_RATIO_NOTE)
metric("Tier 1 Capital", "£'000 (conv. from EUR)", [("Tier one / total regulatory capital base", {**CAPITAL_GBP, **TIER1_STATUTORY_GBP})], note=CAPITAL_NOTE + "\n\n" + EXT_CAPITAL_NOTE)
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", {"FY2021": "40.99%", **CET1_RATIO_EXT, "FY2015": TIER1_RATIO_FY2015})], note=FY2021_RATIO_NOTE + "\n\n" + NOT_DISCLOSED + "\n\n" + EXT_RATIO_NOTE)
metric("Total Capital", "£'000 (conv. from EUR)", [("Total regulatory capital base", {**CAPITAL_GBP, **TOTAL_CAPITAL_STATUTORY_GBP})], note=CAPITAL_NOTE + "\n\n" + EXT_TOTAL_CAPITAL_NOTE)
metric("Total Capital Ratio", "%", [("Total capital ratio", {"FY2021": "40.99%", **TOTAL_CAPITAL_RATIO_EXT})], note=FY2021_RATIO_NOTE + "\n\n" + NOT_DISCLOSED + "\n\n" + EXT_RATIO_NOTE)
metric("Total RWAs", "£'000 (conv. from EUR)", [
    ("Pillar 1 risk-weighted assets (FY2016-FY2021 are each edition's own printed Pillar 1 total; FY2015 is CREDIT-RISK RWA ONLY and understates the total - see note)",
     {**RWA_GBP, **RWA_TOTAL_GBP_EXT}),
    ("FY2015 only - risk-weighted exposures the FY2015 edition discloses SEPARATELY and does NOT include in the 221,221 above: market risk (FX spot position risk) 4,128 and operational risk 11,501",
     {"FY2015": 15629})],
    note="Only FY2021 is directly disclosed among FY2021-FY2025: €318.824m in the 2021 Pillar 3 disclosure, p.18. FY2022-FY2025 "
         "are not publicly disclosed and are not calculated from capital because no corresponding capital ratio is stated.\n\n"
         + P3_CESSATION_NOTE + "\n\n" + EXT_RWA_NOTE)

# ---------------------------------------------------------------
# RWA Breakdown - FY2021's own Pillar 3 disclosure (Table, p.18) gives a
# genuine category-level split, recovered this session via a Wayback
# Machine snapshot after the Bank's own site (persiabank.co.uk) refused
# the TLS handshake on every direct attempt. Ties exactly to the existing
# Total RWAs figure (EUR 318,824k). FY2022-FY2025 remain not publicly
# disclosed, consistent with the Total RWAs sheet above - the Bank's own
# later Annual Reports state Pillar 3 disclosure is available on request,
# and no public standalone Pillar 3 document for those years was located.
# ---------------------------------------------------------------
# FY2015 added 2026-09-15 from the recovered standalone FY2015 Pillar 3 edition.
# Credit 221,221 is that document's own 'Breakdown of exposure classes'/Template
# CR4 total; market risk 4,128 is its section 6 'FX spot position risk'; and
# operational risk 11,501 is its section 7 Basic-Indicator RWE. All three are
# transcribed. Unlike FY2016-FY2021, the FY2015 edition prints NO Pillar 1 total,
# so its three components are shown but its Total row is handled separately below.
RWA_BREAKDOWN_EUR = {
    "Credit and counterparty credit risk": {"FY2021": 298566, **RWA_CREDIT_EUR, "FY2015": 221221},
    "Market risk": {"FY2021": 15321, **RWA_MARKET_EUR, "FY2015": 4128},
    "Operational risk": {"FY2021": 4937, **RWA_OPERATIONAL_EUR, "FY2015": 11501},
}
rwa_breakdown_rows = [
    ("DATA", label, {y: stock_v(v, y) for y, v in values.items()})
    for label, values in RWA_BREAKDOWN_EUR.items()
] + [
    ("TOTAL", "Total Pillar 1 risk-weighted assets (as printed in each edition; FY2015 blank - no total is printed there)",
     {**RWA_GBP, **RWA_TOTAL_GBP_EXT, "FY2015": None}),
    ("DATA", "FY2015 ONLY - arithmetic sum of the three FY2015 rows above (NOT a disclosed figure; shown here so the gap against the Total RWAs sheet's credit-only 221,221 is visible, and deliberately NOT carried onto the Total RWAs sheet - see note)",
     {"FY2015": stock_v(236850, "FY2015")}),
]

bw.add_rwa_breakdown_sheet(
    title="Persia International Bank Plc — RWA Breakdown",
    subtitle="FY2021, plus FY2016-FY2020 added under HD-021 (recovered via Wayback Machine snapshots of the Bank's own "
              "standalone Pillar 3 disclosures, after the Bank's live site refused every direct TLS connection attempt this "
              "session). £'000 converted from EUR (FY2016 figures are EUR '000, unconverted - see FX note). Ties exactly to "
              "the Total RWAs sheet for every year shown. FY2022-FY2025 not publicly disclosed - the Bank stopped publishing "
              "Pillar 3 after its 31 March 2021 edition (its FY2022 report still said the disclosures were published on its "
              "website; FY2023-FY2025 all say they can be made available on request instead), and its live site carries no "
              "later edition - see the source note below. FY2015 IS NOW SHOWN (added 2026-09-15, correcting this subtitle's previous "
              "claim that it could not be): the recovered standalone FY2015 Pillar 3 edition does break its risk down by the "
              "three types after all - the 'Breakdown of exposure classes' table's 221,221 total IS the credit-risk RWA, and "
              "the market and operational risk risk-weighted exposures (4,128 and 11,501) are disclosed separately in that "
              "document's sections 6 and 7. The earlier conclusion came from reading only the exposure-class table. FY2015's "
              "Total row is BLANK because that edition prints no Pillar 1 total, unlike every later one - see the note below.",
    rows=rwa_breakdown_rows,
    sources_text=(
        "Sources - Persia International Bank Plc Pillar 3 disclosures, Pillar 1 capital requirements tables:\n"
        "FY2021, p.18, recovered via Wayback Machine snapshot (captured 10 January 2026) - "
        "http://web.archive.org/web/20260110002617id_/http://www.persiabank.co.uk/Pillar%203%202021%20v3.pdf "
        "(live original URL, plain HTTP: " + PILLAR3_2021_URL + " - re-checked 16 September 2026, HTTP 200, %PDF, "
        "28 pages, and byte-identical to the Wayback capture above, MD5 08b8d37ca13c50b214d275062ab119c3 for both. "
        "The https:// form of the same path, " + PILLAR3_2021_URL_HTTPS_BROKEN + ", still cannot be fetched by any "
        "client: the server resets the TLS handshake at Client hello, so no certificate is presented - see the LINK "
        "PROVENANCE note on this sheet, and do not 'upgrade' the cited scheme. This is the ONLY Pillar 3 document on "
        "the Bank's live site - see the Total RWAs sheet's cessation note)\n"
        f"FY2020/FY2019: Pillar 3 Disclosure as at 31 March 2020, p.17, recovered via Wayback Machine (captured 25 January "
        f"2022) - {PILLAR3_2020_URL}\n"
        f"FY2018/FY2017: Pillar 3 Disclosure as at 31/03/2018, p.16, recovered via Wayback Machine (captured 2 September "
        f"2018) - {PILLAR3_2018_URL}\n"
        f"FY2016: Pillar 3 Disclosure as at 31 March 2016, p.13, recovered via Wayback Machine (captured 24 October 2016) "
        f"- {PILLAR3_2016_URL}\n"
        f"FY2015: Pillar 3 Disclosures March 2015, p.9 (Breakdown of exposure classes - credit risk), p.14 (section 6, "
        f"FX spot position risk) and p.15 (section 7, operational risk RWE), recovered via Wayback Machine (captured "
        f"16 March 2016) - {PILLAR3_2015_URL}\n\n"
        "FY2015 TOTAL ROW IS BLANK, AND THAT IS THE POINT. Every edition from FY2016 on prints an explicit total - "
        "FY2016's reads 'Total Pillar 1 risk 319,767' directly beneath credit 306,733, market 3,036 and operational "
        "9,998. The FY2015 edition prints no such row. Its three components are disclosed in three different places "
        "(an exposure-class table on p.9, one sentence on p.14, one sentence on p.15) and are never added up. The "
        "consequence is that the 221,221 carried on the Total RWAs sheet for FY2015 is the CREDIT-RISK RWA ONLY - "
        "the same credit-subtotal-as-total defect confirmed at Redwood, Ghana International and Bank of Ceylon. It "
        "is left there because no document states a FY2015 total and this project does not substitute a derived "
        "figure for a disclosed one on that sheet; the arithmetic sum of the three components (236,850) is shown on "
        "its own explicitly-labelled row here, and nowhere else, so the size of the understatement is visible "
        "without being presented as a disclosure. See the FY2015 note on the metric sheets for the full extract.\n\n"
        + ENTITY_NOTE + "\n" + FX_NOTE + "\n\n" + LINK_PROVENANCE
    ),
    first_col_width=54,
    source_height=520,
    unit_suffix=" (£'000, conv. from EUR)",
)

metric("Leverage Ratio", "%", [("Leverage ratio", {"FY2021": "53.32%", **LEVERAGE_RATIO_EXT})], note="FY2021, plus FY2016/FY2018/FY2020 added under HD-021: directly disclosed in the Bank's own Pillar 3 disclosures. FY2022-FY2025 are blank because the Bank stopped publishing Pillar 3 after its 31 March 2021 edition - see below.\n\n" + P3_CESSATION_NOTE + "\n\n" + EXT_LEVERAGE_LCR_NOTE)
metric("LCR", "%", [("Liquidity Coverage Ratio (simple average of 12 monthly reports)", {"FY2021": "221.13%", **LCR_EXT})], note="FY2021, plus FY2018/FY2020 added under HD-021: directly disclosed in the Bank's own Pillar 3 disclosures. FY2022-FY2025 are blank because the Bank stopped publishing Pillar 3 after its 31 March 2021 edition - see below; the statutory accounts state no LCR in any of those years.\n\n" + P3_CESSATION_NOTE + "\n\n" + EXT_LEVERAGE_LCR_NOTE)
bw.add_not_disclosed_metric_sheets(["NSFR", "MREL Ratio"], p3_sources(), per_note={m: NOT_DISCLOSED for m in ["NSFR", "MREL Ratio"]})

def _row_values(rows, label):
    for kind, lbl, values in rows:
        if lbl == label:
            return values
    raise KeyError(label)


bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", _row_values(bs_rows, "Total assets")),
        ("Loans and advances to customers", _row_values(bs_rows, "Loans and advances to customers")),
        ("Deposits from customers", _row_values(bs_rows, "Deposits from customers")),
        ("Total shareholders' equity", _row_values(bs_rows, "Total shareholders' equity")),
    ],
    balance_sheet_unit="£'000 (conv. from EUR)",
    income_statement_totals=[
        ("Net Interest Income", _row_values(pl_rows, "Net Interest Income")),
        ("Total operating expenses", _row_values(pl_rows, "Total operating expenses")),
        ("Profit/(loss) for the year attributable to equity holders", _row_values(pl_rows, "Profit/(loss) for the year attributable to equity holders")),
    ],
    income_statement_unit="£'000 (conv. from EUR)",
    equity_changes_totals=[
        ("Opening equity", {"FY2022": stock_v(130644, "FY2021"), "FY2023": stock_v(131758, "FY2022"), "FY2024": stock_v(132561, "FY2023"), "FY2025": stock_v(127693, "FY2024"),
            "FY2020": stock_v(87599, "FY2019"), "FY2019": stock_v(98302, "FY2018"), "FY2018": stock_v(103851, "FY2017"), "FY2017": stock_v(105499, "FY2016"),
            "FY2016": stock_v(105997, "FY2015"), "FY2015": 105479}),
        ("Total comprehensive income/(expense) for the year", {"FY2021": flow_v(-537, "FY2021"), "FY2022": flow_v(1114, "FY2022"), "FY2023": flow_v(803, "FY2023"), "FY2024": flow_v(-3893, "FY2024"), "FY2025": flow_v(-17269, "FY2025"),
            "FY2020": flow_v(-6418, "FY2020"), "FY2019": flow_v(-5839, "FY2019"), "FY2018": flow_v(-5549, "FY2018"), "FY2017": flow_v(-1648, "FY2017"), "FY2016": flow_v(-498, "FY2016"), "FY2015": flow_v(518, "FY2015")}),
        ("Other equity movements, net (FY2021: share capital issuance; FY2024: prior period restatement per Note 33)", {"FY2021": flow_v(50000, "FY2021"), "FY2022": 0, "FY2023": 0, "FY2024": stock_v(-975, "FY2023"), "FY2025": 0,
            "FY2020": 0, "FY2019": 0, "FY2018": 0, "FY2017": 0, "FY2016": 0, "FY2015": 0}),
        ("Closing equity", {"FY2021": stock_v(130644, "FY2021"), "FY2022": stock_v(131758, "FY2022"), "FY2023": stock_v(132561, "FY2023"), "FY2024": stock_v(127693, "FY2024"), "FY2025": stock_v(110424, "FY2025"),
            "FY2020": stock_v(81181, "FY2020"), "FY2019": stock_v(87599, "FY2019"), "FY2018": stock_v(98302, "FY2018"), "FY2017": stock_v(103851, "FY2017"), "FY2016": stock_v(105499, "FY2016"), "FY2015": stock_v(105997, "FY2015")}),
    ],
    equity_changes_unit="£'000 (conv. from EUR)",
    cash_flow_totals=[
        ("Net cash flow from operating activities", flow(OPERATING_EUR)),
        ("Net cash flow from investing activities", flow(INVESTING_EUR)),
        ("Cash and cash equivalents at end of year", closing_gbp),
    ],
    cash_flow_unit="£'000 (conv. from EUR)",
    ratios=[("Leverage Ratio", {"FY2021": "53.32%", **LEVERAGE_RATIO_EXT}), ("LCR", {"FY2021": "221.13%", **LCR_EXT})],
    note="FY2021 leverage and LCR are the only directly disclosed regulatory liquidity metrics located in the public source "
         "set for FY2021-FY2025; later years there are intentionally blank because the Bank ceased publishing Pillar 3 "
         "disclosures after its 31 March 2021 edition - a documented policy change (its FY2022 Annual Report, p.8, says the "
         "disclosures 'are published on the Bank's web site'; the FY2023, FY2024 and FY2025 reports all replace that with "
         "'can be made available on request'), confirmed against the Bank's live site, which carries exactly one Pillar 3 "
         "PDF, the 2021 edition. The Bank itself has not ceased - it is Active at Companies House, filed accounts to "
         "31 March 2025, and still holds PRA authorisation (FRN 208020, Bank of England List of banks at 30 September 2026). "
         "See the Total RWAs / Leverage Ratio / LCR sheets for the full evidence. FY2016/FY2018/FY2020 leverage and "
         "FY2018/FY2020 LCR were added under HD-021 from the Bank's own standalone Pillar 3 disclosures - see the Leverage "
         "Ratio/LCR sheets for the FY2015/FY2017/FY2019 gaps. FY2021's opening equity is blank because the Bank's disclosed "
         "EUR/GBP rate series in this workbook's source set only starts at FY2021 - see the Statement of Changes in Equity "
         "sheet for detail; FY2015's opening equity (EUR 105,479k) and FY2016/FY2017's opening equity are shown unconverted "
         "or independently converted at each year's own rate for the same reason - see that sheet's own methodology note.",
)

bw.save("/Users/armaan/code/katalysis/banks/PERSIA INTERNATIONAL BANK FINANCIALS.xlsx")
