import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016"]

AR_2025 = "https://www.mcafundingforchurches.co.uk/media/4bcl2vk5/mca-ar-2025.pdf"
AR_2024 = "https://www.mcafundingforchurches.co.uk/media/keybconk/annual-report-2024.pdf"
AR_2022 = "https://www.mcafundingforchurches.co.uk/sitefiles/resources/pdf/annualreport2022.pdf"
# ---------------------------------------------------------------------------
# Pillar 3 document URLs. LINK-ROT STATUS RE-VERIFIED 2026-09-15: every URL
# below was fetched and checked for the `%PDF-` magic bytes, not merely for an
# HTTP 200 (soft-404s returning 200 with an HTML body are a known trap on this
# project). Results are recorded against each constant.
#
# Convention: when a live URL dies, cite a Wayback `id_` snapshot (the `id_`
# modifier returns the raw archived bytes rather than a Wayback-wrapped HTML
# page) and KEEP the dead original alongside it, labelled as such, so the
# provenance chain stays readable.
# ---------------------------------------------------------------------------

# FY2023: the Company's own URL now 404s. Two good Wayback captures exist
# (20240722103538 and 20250407005711) with an IDENTICAL content digest
# (IBZRVVYWANAYMDURC7ETVSZEWBFVN5CL), so the archived file is stable across
# captures; the later one is cited. Retrieved 2026-09-15: 318,898 bytes,
# begins `%PDF-`.
P3_2023_DEAD = "https://www.mcafundingforchurches.co.uk/media/ngqlqg5o/pillar-3-disclosures-2023.pdf"
P3_2023_WAYBACK = "https://web.archive.org/web/20250407005711id_/" + P3_2023_DEAD

# FY2022: this edition is the one case where a LIVE URL still works, so the
# live URL is cited in preference to any archive copy. The Company published
# the same file at two paths; the newer Umbraco /media/honer1yl/ path has since
# 404'd, but the older /siteFiles/resources/pdf/ path is still served.
# Confirmed 2026-09-15 that they are the same document rather than two
# editions: the live file and the Wayback copy of the dead /media/honer1yl/
# path are BYTE-IDENTICAL - both 314,344 bytes, both SHA-256 44326e0da4312b73...
P3_2022 = "https://www.mcafundingforchurches.co.uk/siteFiles/resources/pdf/Pillar3disclosures2022.pdf"
P3_2022_DEAD = "https://www.mcafundingforchurches.co.uk/media/honer1yl/pillar3disclosures2022.pdf"
P3_2022_WAYBACK = "https://web.archive.org/web/20240517201255id_/https://mcafundingforchurches.co.uk/media/honer1yl/pillar3disclosures2022.pdf"

# ---------------------------------------------------------------------------
# PRE-FY2019 PILLAR 3: THE EVIDENCE DOES NOT REACH, AND THIS IS A CORRECTION.
# Established 2026-09-18 (GA-005). Earlier revisions of this file said the
# FY2016-FY2018 Pillar 3 blanks were "genuinely not disclosed, not a search
# miss", resting on the fact that a full-domain Wayback CDX listing returns no
# Pillar 3 PDF before FY2019. That inference does not hold, and the CDX index
# itself is what refutes it:
#
#   * THE EARLIEST CAPTURE OF ANY PDF ON THIS DOMAIN, of any kind, is
#     30 September 2020 (annualreport2019.pdf). Not the earliest Pillar 3 - the
#     earliest PDF full stop.
#   * The archive DID crawl the domain across 2016-2018 (53 captures in 2016,
#     101 in 2017, 84 in 2018), but every one of them is the HOMEPAGE or a CSS
#     / JS / image asset. No interior page and no document was ever fetched.
#   * The 30 August 2018 homepage capture links a financial-information page at
#     the OLD path /financial-information/ (today's is /about-us/financial-
#     information/), and that page has no capture at all.
#   * The corroborating check: no FY2016, FY2017 or FY2018 ANNUAL REPORT is in
#     the index either, and those documents certainly existed - they are on the
#     Companies House filing history cited below. So the index's silence on
#     this era is demonstrably not evidence of non-publication.
#
# Pillar 3 was a live duty for this firm in those years (CRR Part Eight applied
# to all institutions from 1 January 2014), so the prior absence of a document
# is more likely a reach limit than a fact about the Company.
#
# STATUS: the FY2016-FY2018 Pillar 3 columns are UNPROVEN - no document has
# been reached and no instrument has been found that removed the duty. They are
# NOT recorded as never-published. Live-site probes on the still-served
# /siteFiles/resources/pdf/ path (which does still serve the FY2022 edition, so
# the path itself is alive) returned 404 for nine spellings of a pre-2019
# filename on 2026-09-18, but this Company uses a different naming style every
# single year, so a guessed path's 404 is evidence about the guess.
# WHAT A LATER SESSION SHOULD TRY: the Company directly (it is a ten-person
# mutual and may simply send them); a Companies House document search for a
# disclosure filing; and the British Library / national web archive, whose UK
# domain crawl is independent of the Internet Archive and did cover this period.
# ---------------------------------------------------------------------------
PRE2019_STATUS = (
    "FY2016-FY2018: UNPROVEN, not established as unpublished (corrected 2026-09-18). No Pillar 3 document "
    "for these years has been reached, and no instrument removing the duty has been found - Pillar 3 was a "
    "live obligation for this firm then (CRR Part Eight, applying to all institutions from 1 January 2014). "
    "An earlier revision of this workbook called these years 'genuinely not disclosed, not a search miss' on "
    "the strength of a full-domain Wayback CDX listing that returns no pre-FY2019 Pillar 3 PDF. That "
    "inference has been withdrawn, because the same index shows the earliest capture of ANY PDF on this "
    "domain is 30 September 2020: the archive crawled the site throughout 2016-2018 (53/101/84 captures per "
    "year) but fetched only the homepage and its CSS, JS and image assets, never an interior page and never "
    "a document. The 30 August 2018 homepage capture links a financial-information page at the old path "
    "/financial-information/ which has no capture at all. Confirming the point: no FY2016, FY2017 or FY2018 "
    "ANNUAL REPORT is in the index either, though those documents demonstrably exist (they are on the "
    "Companies House filing history cited here). The archive's silence about this era is therefore a limit "
    "of its coverage, not a fact about the Company. These cells are blank because nothing has been read, "
    "which is a different statement from the FY2024/FY2025 blanks, where a dated instrument removed the duty."
)

# HD-027 extension (2026-09-06): statutory accounts for FY2016-FY2020 were re-verified directly
# from Companies House filing history (not just the HD-004 domain/earliest-snapshot signal) -
# each PDF was downloaded, rendered page-by-page and read as images (all five filings are
# scanned, non-OCR documents; pdftotext extracted 0 characters from each).
CH_FY2020 = "https://find-and-update.company-information.service.gov.uk/company/00030546/filing-history/MzMwMDQ2Njg3M2FkaXF6a2N4/document?format=pdf&download=0"
CH_FY2018 = "https://find-and-update.company-information.service.gov.uk/company/00030546/filing-history/MzIzMzkxMzU5MGFkaXF6a2N4/document?format=pdf&download=0"
CH_FY2016 = "https://find-and-update.company-information.service.gov.uk/company/00030546/filing-history/MzE3NTQ2MDUyOWFkaXF6a2N4/document?format=pdf&download=0"
# Pillar 3 disclosures for FY2019/FY2020/FY2021 were located via Wayback Machine snapshots of
# mcafundingforchurches.co.uk (not present live) - these are the earliest Pillar 3 documents
# found anywhere on the domain's crawl history; no FY2016/FY2017/FY2018 Pillar 3 document exists
# in the Wayback CDX index for this domain (a full-domain PDF listing was checked, not just a
# single guessed filename), consistent with Pillar 3 disclosure only starting for this small
# firm from FY2019.
# FY2021 is the one edition that breaks the 'pillar3disclosures<YYYY>.pdf'
# naming convention - it is published as '2021-pillar-3-disclosures.pdf'
# instead, which is why filename-pattern guessing never found it. Located
# 2026-09-15 by listing the whole domain from the Wayback CDX index. The live
# URL 404s and this remains the only capture of it in the index. Re-fetched
# 2026-09-15: 319,857 bytes, begins `%PDF-`.
P3_2021_DEAD = "https://www.mcafundingforchurches.co.uk/sitefiles/resources/pdf/2021-pillar-3-disclosures.pdf"
P3_2021_WAYBACK = "https://web.archive.org/web/20220625084136id_/" + P3_2021_DEAD

# Both re-fetched 2026-09-15 with the `id_` modifier and confirmed to begin
# `%PDF-` (FY2020: 311,788 bytes; FY2019: 274,658 bytes). The Company's own
# URLs for both remain dead.
P3_2020_DEAD = "https://www.mcafundingforchurches.co.uk/sitefiles/resources/pdf/pillar3disclosures2020.pdf"
P3_2020_WAYBACK = "https://web.archive.org/web/20210515024743id_/" + P3_2020_DEAD
P3_2019_DEAD = "http://mcafundingforchurches.co.uk/sitefiles/resources/pdf/pillar3disclosures2019.pdf"
P3_2019_WAYBACK = "https://web.archive.org/web/20200930032441id_/" + P3_2019_DEAD

ENTITY = (
    "ENTITY NOTE: Methodist Chapel Aid Limited (Companies House 00030546, FRN 204508, "
    "LEI 213800GD7EDYBP4LH202) matches Banks List 2608.xlsx and Companies House. It is a "
    "UK-incorporated PRA/FCA-authorised bank operating on a standalone company basis. The "
    "2025 reporting period covers nine months ended 30 September 2025 after the accounting "
    "reference date changed from 31 December. The Company states that its Pillar 3 policy is "
    "annual. No defensible entity-level interim Pillar 3 series was located, so this is an "
    "18-sheet annual workbook (Overview, Balance Sheet, Profit & Loss, Statement of Changes in "
    "Equity, Cash Flow Statement, Asset Quality, the 11 Pillar 3 key metric sheets, RWA "
    "Breakdown), extended back to FY2016 - the Company's confirmed floor per HD-004 (Companies "
    "House filing history for this entity, 00030546, goes back further, but FY2016 is the year "
    "confirmed for this batch). FY2024 and FY2025 Pillar 3 metrics are blank because the Company "
    "is an SDDT and is exempt from publishing Pillar 3 disclosures - a PRA modification by "
    "consent under Rule 3.1 of the SDDT Regime - General Application Part, effective 11 April "
    "2024 (see the dated evidence in the Pillar 3 source note); this is a structural exemption, "
    "not a sourcing gap, and nothing is inferred from statutory net assets. No Pillar 3 document has been "
    "REACHED for this entity before FY2019, but that is a limit of the surviving evidence rather than an "
    "established absence - the FY2016-FY2018 columns are UNPROVEN, not never-published, and the reason the "
    "web archive cannot speak to that era is set out in full in the Pillar 3 source note. "
    "LCR and NSFR were not disclosed for FY2019-FY2021 either: the "
    "FY2019/FY2020/FY2021 standalone Pillar 3 documents only state a policy of maintaining LCR "
    "at or above 200% and do not disclose an actual measured LCR or NSFR figure (no numeric Key "
    "Metrics table exists in these documents, unlike the FY2022/FY2023 disclosures). MREL was "
    "not disclosed in any year."
)


def cash_sources():
    return (
        "Sources - Methodist Chapel Aid Limited entity-level Statement of Cash Flows, £:\n"
        f"FY2025 (9 months ended 30 September 2025): MCA Annual report and accounts 2025, pp. 38-39 - {AR_2025}\n"
        f"FY2024: MCA Annual report and accounts 2024, pp. 36-39 - {AR_2024}\n"
        f"FY2023: MCA Annual report and accounts 2024 comparative, p. 39 - {AR_2024}\n"
        f"FY2022: MCA Annual report and accounts 2022, p. 38 - {AR_2022}\n"
        f"FY2021: MCA Annual report and accounts 2022 comparative, p. 38 - {AR_2022}\n"
        f"FY2020: Companies House full accounts to 31 December 2020 (filed 13 May 2021), Statement of Cash Flows p. 27 - {CH_FY2020}\n"
        f"FY2019: Companies House full accounts to 31 December 2020 comparative, p. 27 - {CH_FY2020}\n"
        f"FY2018: Companies House full accounts to 31 December 2018 (filed 10 May 2019), Statement of Cash Flows p. 25 - {CH_FY2018}\n"
        f"FY2017: Companies House full accounts to 31 December 2018 comparative, p. 25 - {CH_FY2018}\n"
        f"FY2016: Companies House full accounts to 31 December 2016 (filed 11 May 2017), Statement of Cash Flows p. 23 - {CH_FY2016}\n\n"
        + ENTITY
    )


# Bank of England consolidated list of waivers and modifications granted to PRA-authorised firms
# (the PRA's own firm-level register), linked from
# https://www.bankofengland.co.uk/prudential-regulation/authorisations/waivers-and-modifications-of-rules
PRA_WAIVERS_CSV = (
    "https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/authorisations/"
    "waivers-and-modifications-of-rules/consolidated-waivers-pra-firms.csv"
)

SDDT_NOTE = (
    "REASON FOR THE CESSATION ESTABLISHED 2026-09-15 (cross-bank SDDT pass) - the FY2024 and FY2025 Pillar 3 "
    "gaps are an EVIDENCED STRUCTURAL EXEMPTION, not a sourcing failure, and no Pillar 3 document for those "
    "years will ever exist to be found. Methodist Chapel Aid Limited holds a PRA modification by consent "
    "under Rule 3.1 of the 'SDDT Regime - General Application' Part of the PRA Rulebook - the instrument by "
    "which a firm becomes a Small Domestic Deposit Taker (SDDT) under the PRA's 'Strong and Simple' "
    "framework. The register row reads, verbatim: FRN 204508, 'Methodist Chapel Aid Limited', 'Modification "
    "by Consent - PRA Rulebook- CRR Firms- Rule 3.1 of the SDDT Regime - General Application Part 3.1', rule "
    "'SDDT Regime - General Application', sub rule 'Ru 3.1', waiver ref 'A00007737P.pdf', start date "
    "'11/04/2024', no end date. Source: Bank of England consolidated list of waivers and modifications "
    f"granted to PRA-authorised firms, downloaded 2026-09-15 - {PRA_WAIVERS_CSV}\n"
    "What that modification does to Pillar 3 is stated in a peer bank's own words, and the same register "
    "carries the identical Rule 3.1 row for that peer, so the register row and the firm-stated effect are "
    "demonstrably the same instrument: Cynergy Bank plc Annual Report & Accounts 2024, p.71 - 'The Bank "
    "applied for the Modification by Consent to become an SDDT and received approval on 17 January 2025. As "
    "a result, we are not required to publish Pillar 3 disclosures as at 31 December 2024 and will submit "
    "only a simplified retail deposit ratio instead of a full Net Stable Funding Ratio (NSFR) going forward.' "
    "(Cynergy's register row: FRN 575105, Rule 3.1, start '17/01/2025' - matching its own stated approval "
    "date to the day.)\n"
    "DATE FIT: MCA's modification took effect 11 April 2024, i.e. BEFORE its 31 December 2024 year-end and "
    "before the 30 September 2025 period-end, so it cleanly covers both FY2024 and FY2025 - the two years "
    "with no Pillar 3 document - and the five published editions FY2019-FY2023 all predate it. The "
    "exemption therefore explains the cessation exactly and explains NOTHING about FY2016-FY2018, whose "
    "blanks have an entirely separate and unrelated cause (no Pillar 3 document was ever published that "
    "early - see the Wayback CDX note below). Do not read the SDDT exemption back onto FY2023 or earlier.\n"
    "RE-DOWNLOADED AND RE-CHECKED 2026-09-15 under a maximum-effort sweep that treated every prior "
    "'unavailable' verdict in this project as unproven. The PRA register was pulled fresh from the Bank of "
    "England (2,919 rows, 135 of them SDDT Rule 3.1 modifications) and MCA's row reproduces the citation "
    "above exactly: FRN 204508, 'Methodist Chapel Aid Limited', 'Modification by Consent - PRA Rulebook- CRR "
    "Firms- Rule 3.1 of the SDDT Regime - General Application Part 3.1', sub-rule 'Ru 3.1', ref "
    "A00007737P.pdf, start 11/04/2024, no end date - so the modification is still in force and has not been "
    "re-dated. The register also shows MCA's separate Capital Buffers 5.1-5.3 direction (06/11/2024), which "
    "is NOT a disclosure exemption and is not relied on here. The date fit above therefore stands unchanged, "
    "and both FY2024 (31 December 2024) and FY2025 (the nine months to 30 September 2025, after the "
    "accounting reference date change) fall after 11 April 2024.\n"
    "Neither Annual Report names SDDT: both the FY2024 and FY2025 Annual Reports were downloaded fresh and "
    "text-extracted in full (readable text layers, 144k and 157k characters respectively) and searched for "
    "'SDDT', 'Small Domestic Deposit Taker', 'modification by consent', 'Simplified Retail Deposit Ratio', "
    "'SRDR', 'Strong and Simple', 'Interim Capital Regime' and 'Basel 3.1' - zero hits, and the word "
    "'Pillar' appears once in each, only in the phrase 'Pillar 1 plus Pillar 2A'. The Company simply does "
    "not discuss the change; the PRA register is what evidences it. No Simplified Retail Deposit Ratio "
    "value is disclosed by the Company either, so nothing replaces the NSFR series here.\n"
    "THE COMPANY'S OWN DOCUMENT INDEX IS CONSISTENT WITH THE EXEMPTION, checked 2026-09-15 across three "
    "dated Wayback captures of https://www.mcafundingforchurches.co.uk/about-us/financial-information/ "
    "spanning a year: 22 April 2025 (20250422192754), 15 September 2025 (20250915123834) and 17 January "
    "2026 (20260117041203). Each capture was retrieved and every PDF link on it extracted. All three list "
    "the same short set - annual-report-2024.pdf, country-by-country-reporting-2024.pdf and an FSCS "
    "leaflet - and none lists a Pillar 3 document of any vintage; the live page today lists the FY2025 "
    "Annual Report, the 2025 country-by-country report and the same FSCS leaflet, again with no Pillar 3. "
    "So the index kept being updated with new statutory documents across the whole period in which an "
    "FY2024 edition would have been due, and no Pillar 3 document was ever added back. This is supporting "
    "evidence only, and deliberately weighted as such: as noted above, this page did not link the Pillar 3 "
    "documents even in the years they demonstrably existed, so it cannot prove absence on its own. The "
    "weight rests on the Rule 3.1 register row and its date fit.\n"
)


LINK_ROT_NOTE = (
    "LINK-ROT REPAIR, 2026-09-15. Four of this Company's five Pillar 3 editions are no longer served from "
    "its own site: the FY2019, FY2020 and FY2021 URLs died some time ago, and the FY2023 URL "
    "(/media/ngqlqg5o/) and one of the two FY2022 URLs (/media/honer1yl/) have BOTH gone dead since this "
    "workbook was last touched. Rather than delete the citations - which would leave the figures on these "
    "sheets unverifiable - each dead URL is cited via a Wayback `id_` snapshot, with the Company's own "
    "dead URL kept alongside it and labelled as such, so the provenance chain stays readable. The `id_` "
    "modifier is deliberate: it returns the raw archived bytes instead of a Wayback-wrapped HTML page.\n"
    "EVERY REPLACEMENT WAS VERIFIED BY RETRIEVAL, not by status code. Each URL below was downloaded on "
    "2026-09-15 and confirmed to begin with the `%PDF-` magic bytes; byte sizes are quoted against each "
    "one. An HTTP 200 alone is not accepted as proof on this project - soft-404s that return 200 with an "
    "HTML body have been encountered repeatedly.\n"
    "The FY2022 edition is the one that is still live, and its live URL is cited in preference to any "
    "archive copy.\n"
)


def p3_sources():
    return (
        "Sources - Methodist Chapel Aid Limited entity-level Pillar 3 / regulatory capital disclosures, £'000 unless stated:\n"
        + LINK_ROT_NOTE +
        f"FY2023: Pillar 3 Disclosures for year ended 31 December 2023, Key Metrics table (p. 3) and the "
        f"quarterly LCR/NSFR averaging tables in section 6.2 (pp. 10-11) - {P3_2023_WAYBACK} (Wayback "
        f"`id_` snapshot of 7 April 2025. The Company's own URL, {P3_2023_DEAD}, returns HTTP 404 - "
        f"re-checked 2026-09-15.)\n"
        f"FY2022 and FY2021: Pillar 3 Disclosures for year ended 31 December 2022, Key Metrics table (p. 3) "
        f"and the quarterly LCR/NSFR averaging tables in section 6.2 (pp. 10-11) - {P3_2022} (THIS ONE IS "
        f"STILL LIVE and is cited in preference to any archive copy - re-fetched 2026-09-15, HTTP 200, "
        f"314,344 bytes, begins `%PDF-`. The Company also published this same edition at "
        f"{P3_2022_DEAD}, which now returns HTTP 404; that dead path's Wayback copy "
        f"({P3_2022_WAYBACK}) was downloaded and is BYTE-IDENTICAL to the live file - same 314,344 bytes, "
        f"same SHA-256 44326e0da4312b73... - which is what establishes the two paths served one document "
        f"rather than two editions.)\n"
        "FY2024/FY2025: no separate absolute Key Metrics table was located; values left blank. "
        "RE-VERIFIED 2026-09-12 (independent disclosure audit): confirmed genuinely unpublished rather than "
        "an access gap. The Company's own live 'Financial information' page "
        "(https://www.mcafundingforchurches.co.uk/about-us/financial-information/) lists only the FY2025 Annual "
        "Report and a country-by-country reporting PDF - no Pillar 3 document of any vintage - and a full Wayback "
        "Machine CDX listing of the domain returns Pillar 3 PDFs for FY2019-FY2023 only, nothing later. The FY2025 "
        "Annual Report was downloaded and read in full: its capital and liquidity discussion is entirely "
        "policy/appetite language, not disclosed outturns - it gives the Total Capital Requirement as 17.72% of RWAs "
        "(a regulatory REQUIREMENT set for the Company, not its actual ratio, p.20), a CET1 risk appetite of 'at "
        "least 35% of risk weighted assets' (a target floor, p.20), and an LCR 'policy ... to maintain at least 200%' "
        "(a policy minimum, p.16). Note 24 confirms actual regulatory capital 'remained above that required' without "
        "stating an amount. None of these is a disclosed value for the metric concerned, so nothing is transcribed "
        "from them - no RWA figure, capital amount, or outturn ratio appears anywhere in the document.\n"
        "RE-VERIFIED INDEPENDENTLY 2026-09-15, extending the 2026-09-12 audit to the FY2024 Annual Report, which "
        "that audit had not itself opened (it had read only the FY2025 one). Both Annual Reports were downloaded "
        "fresh and text-extracted in full, and they behave identically: each states the Total Capital Requirement "
        "as 17.72% of risk-weighted assets (FY2024 as at 31 December 2024, FY2025 as at 30 September 2025) - a "
        "requirement SET FOR the Company, not its outturn; each states the same 'at least 35% of risk weighted "
        "assets' CET1 risk appetite and the same 'at least 200%' LCR policy minimum; and each closes its Financial "
        "Instruments note with the identical sentence that the Company's actual regulatory capital, all CET1, "
        "'remained above that required by the regulatory limit and internal policy' - naming no amount, no RWA "
        "denominator and no ratio. Neither report contains a Key Metrics/UK KM1 table, an own-funds table, an RWA "
        "figure, a leverage ratio, an outturn LCR or any NSFR reference. So all 20 FY2024+FY2025 Pillar 3 cells are "
        "genuinely undisclosed at source. Nothing is derived from the 17.72% TCR or the 35% CET1 appetite: both are "
        "requirement/appetite percentages, and back-solving an RWA or capital amount from a capital REQUIREMENT is "
        "barred by this project's no-derivation rule.\n"
        "Publication-side re-check the same date, to separate 'not published' from 'published but not found': the "
        "Company's own live 'Financial information' page lists exactly three PDFs (the FY2025 Annual Report, a "
        "country-by-country reporting 2025 PDF, and an FSCS leaflet) and no Pillar 3 document; the site's own "
        "sitemap.xml lists only 11 pages in total, with no Pillar-3 page among them; and a Wayback CDX scan of the "
        "whole mcafundingforchurches.co.uk domain filtered to Pillar-3 URLs returns editions for FY2019, FY2020, "
        "FY2021, FY2022 and FY2023 and nothing later, while a separate CDX listing of every PDF captured on the "
        "domain since January 2025 shows Annual Reports and country-by-country reports continuing but no Pillar 3 "
        "document. The Company therefore published a Pillar 3 disclosure annually for five consecutive years and "
        "then stopped after FY2023. Its own stated Pillar 3 policy is annual (see ENTITY NOTE).\n"
        "RE-ENUMERATED INDEPENDENTLY 2026-09-15 (third pass, run without assuming the two above were right). "
        "This bank cannot be searched by filename permutation - it uses a different naming style every "
        "single year ('pillar3disclosures2019.pdf', 'pillar3disclosures2020.pdf', "
        "'2021-pillar-3-disclosures.pdf', 'pillar3disclosures2022.pdf', then the Umbraco opaque-key form "
        "'/media/ngqlqg5o/pillar-3-disclosures-2023.pdf') - so the only method that can prove anything here "
        "is domain enumeration. An unfiltered Wayback CDX listing of the whole domain "
        "(http://web.archive.org/cdx/search/cdx?url=mcafundingforchurches.co.uk&output=json&matchType="
        "domain&collapse=urlkey&limit=5000) returns 160 distinct URLs ever captured, of which exactly SIX "
        "are Pillar 3 documents, covering FIVE editions - FY2019, FY2020, FY2021, FY2022 and FY2023 - with "
        "the FY2022 edition appearing twice because it was captured both on the old "
        "/sitefiles/resources/pdf/ path and again after the site migrated to Umbraco's opaque /media/<key>/ "
        "paths. Nothing later exists in the index, and "
        "the archive is current for this domain - its most recent captures are dated June 2026, well after "
        "an FY2024 or FY2025 edition would have been due.\n"
        "The live site was separately re-scraped the same day, page by page from its own sitemap.xml (11 "
        "pages, the complete site), collecting every PDF href rather than reading any single page: five "
        "PDFs total - the FY2025 Annual Report, a 2025 country-by-country reporting PDF, an FSCS leaflet, a "
        "privacy notice and a 'funding you can trust' brochure. No Pillar 3 document of any vintage. IMPORTANT "
        "CAVEAT ON THAT EVIDENCE, which is why it is cited second and not first: the Company's "
        "/about-us/financial-information page has never linked its Pillar 3 documents even in the years when "
        "they demonstrably existed, so its silence proves nothing on its own and must NOT be cited as proof "
        "of absence. The weight here rests on the CDX enumeration and on the SDDT date test below.\n"
        + SDDT_NOTE +
        "LATEST-EDITION CHECK RE-RUN INDEPENDENTLY 2026-09-18 (GA-005), against the Company's own site "
        "first rather than against the URLs cited here. Four things were established, all on that date.\n"
        "(i) NEWEST ANNUAL REPORT: the Annual Report 2025, covering the 9 months ended 30 September 2025 - "
        "the period this workbook already holds as FY2025. The Company's live 'Financial information' page "
        "was fetched directly (HTTP 200, no block, no interstitial) and lists exactly three PDFs: "
        "mca-ar-2025.pdf, country-by-country-reporting-2025.pdf and an FSCS leaflet. Companies House "
        "confirms the position from the other side - the most recent accounts filing for company 00030546 "
        "is the full accounts filed 28 January 2026, which are those same 9-month accounts, preceded by the "
        "AA01 of 27 August 2025 that shortened the accounting period. NOTHING NEWER EXISTS RATHER THAN "
        "NOTHING NEWER WAS REACHED: the Company's next year-end, 30 September 2026, had not yet occurred on "
        "the date of this check.\n"
        "(ii) NEWEST PILLAR 3: still the FY2023 edition. No Pillar 3 document of any vintage appears on the "
        "live site, whose sitemap.xml lists the complete site at 11 pages.\n"
        "(iii) The SDDT modification was re-read from a fresh download of the Bank of England register the "
        "same day (2,916 rows) and is unchanged: FRN 204508, Rule Description 'SDDT Regime - General "
        "Application', sub-rule 'Ru 3.1', ref A00007737P.pdf, start 11/04/2024, no end date. The match is on "
        "the Rule Description, not on the sub-rule number - the Company's OTHER register row, the capital "
        "buffers direction of 06/11/2024, sits under the 'Permissions and Waivers (CRR Firms)' rulebook and "
        "is not a disclosure exemption and is not relied on here.\n"
        "(iv) The FY2024 and FY2025 Annual Reports were re-downloaded and re-read in full on the same date "
        "to test whether either discloses an outturn that could fill these columns without a Pillar 3. "
        "Neither does, and every hit was read rather than counted. Each document contains exactly one "
        "'Total Capital Requirement' passage (17.72% of risk-weighted assets - a minimum SET FOR the "
        "Company), one CET1 passage ('capital risk appetite is to maintain Common Equity Tier 1 (CET1) "
        "capital ... of at least 35% of risk weighted assets' - an appetite floor), one 'Own Funds' mention "
        "(inside an operational risk appetite limit of 2% of own funds), two LCR mentions (the same 'at "
        "least 200%' policy floor), and a Financial Instruments note closing that actual regulatory capital "
        "'remained above that required by the regulatory limit and internal policy' without naming an "
        "amount. There is no key-metrics table, no own-funds table, no RWA figure, no leverage ratio, no "
        "LCR or NSFR outturn, and the token 'Pillar 3' does not occur in either report. Requirement and "
        "appetite percentages are not outturns and nothing is back-solved from them.\n"
        "ONE CAVEAT ON THE WEB-ARCHIVE EVIDENCE, recorded because it cuts against the argument it supports: "
        "the Wayback CDX index is NOT a complete record of this domain's documents. The Annual Report 2025 "
        "is live on the Company's own site today and does not appear in the index at all. So 'absent from "
        "CDX' is weaker evidence here than it looks, and the FY2024/FY2025 conclusion rests on the dated "
        "Rule 3.1 modification and on the live site, with the CDX enumeration as corroboration only.\n"
        "Note also that FY2025 is a 9-month period (the accounting reference date moved from 31 December "
        "to 30 September during 2025), so even a future FY2025 Pillar 3 edition would not be period-comparable with "
        "the FY2019-FY2023 12-month series without an explicit basis caveat.\n"
        f"FY2020: Pillar 3 Disclosures for year ended 31 December 2020, Section 5 Capital Adequacy, p. 7 - "
        f"{P3_2020_WAYBACK} (Wayback `id_` snapshot of 15 May 2021; re-fetched 2026-09-15, 311,788 bytes, "
        f"begins `%PDF-`. The Company's own URL, {P3_2020_DEAD}, is dead.)\n"
        f"FY2019: Pillar 3 Disclosures for year ended 31 December 2019, Section 5 Capital Adequacy, p. 7 - "
        f"{P3_2019_WAYBACK} (Wayback `id_` snapshot of 30 September 2020; re-fetched 2026-09-15, 274,658 "
        f"bytes, begins `%PDF-`. The Company's own URL, {P3_2019_DEAD}, is dead.)\n"
        + PRE2019_STATUS + "\n\n"
        + ENTITY
    )


# (P3_2023_WAYBACK is defined with the other Pillar 3 URL constants at the top
# of this file, alongside its dead original - a second, non-`id_` definition
# used to sit here and silently overwrote it. Removed 2026-09-15.)

STATEMENTS_SOURCES = (
    "Sources - Methodist Chapel Aid Limited entity-level Statement of Income and Retained Earnings / "
    "Statement of Financial Position, £:\n"
    f"FY2025 (9 months ended 30 September 2025) and FY2024 comparative: MCA Annual report and accounts 2025, "
    f"Statement of Income and Retained Earnings p.37, Statement of Financial Position p.38 - {AR_2025}\n"
    f"FY2023 comparative: MCA Annual report and accounts 2024, Statement of Income and Retained Earnings p.36, "
    f"Statement of Financial Position p.37 - {AR_2024}\n"
    f"FY2022 comparative: MCA Annual report and accounts 2022, Statement of Income and Retained Earnings p.35, "
    f"Statement of Financial Position p.36 - {AR_2022}\n"
    f"FY2021 comparative: MCA Annual report and accounts 2022, Statement of Income and Retained Earnings p.35, "
    f"Statement of Financial Position p.36 - {AR_2022}\n"
    f"FY2020: Companies House full accounts to 31 December 2020, Statement of Income and Retained Earnings p.25, "
    f"Statement of Financial Position p.26 - {CH_FY2020}\n"
    f"FY2019 comparative: Companies House full accounts to 31 December 2020, same pages - {CH_FY2020}\n"
    f"FY2018: Companies House full accounts to 31 December 2018, Statement of Income and Retained Earnings p.23, "
    f"Statement of Financial Position p.24 - {CH_FY2018}\n"
    f"FY2017 comparative: Companies House full accounts to 31 December 2018, same pages - {CH_FY2018}\n"
    f"FY2016: Companies House full accounts to 31 December 2016, Statement of Income and Retained Earnings p.21, "
    f"Statement of Financial Position p.22 - {CH_FY2016}\n\n"
    "Note: the Company has no standalone Statement of Changes in Equity - equity movements are shown within "
    "the combined Statement of Income and Retained Earnings (surplus/(deficit) for the period less dividends "
    "paid and payable, rolled into Reserves; Called up equity share capital is unchanged across all 10 years). "
    "The 2025 reporting period covers 9 months (accounting reference date changed from 31 December to 30 "
    "September); all other periods are 12 months. FY2016-FY2020 statutory line-item labels differ slightly "
    "from later years' Pillar 3-derived labels in two places: 'Interest receivable - on National Savings and "
    "bank deposits' (FY2016-FY2020 statutory wording) is the same line as 'Interest receivable - on bank and "
    "building society deposits' (FY2021+ wording); and the FY2016-FY2020 Investments note (12) splits "
    "investments only into 'Debt and fixed income securities' vs 'Equity investments' (no further split by "
    "issuer type), unlike the FY2023-FY2025 note's three-way split - see the Balance Sheet sheet's separate "
    "'Investments - debt and fixed income securities (aggregate, pre-2021 disclosure)' row.\n\n"
    + ENTITY
)

ASSET_QUALITY_SOURCES = (
    "Sources - Methodist Chapel Aid Limited entity-level loan book detail, Note 11/13 Debtors (Loans and "
    "advances to customers), £:\n"
    f"FY2025 and FY2024 comparative: MCA Annual report and accounts 2025, Note 11, pp.49-50 - {AR_2025}\n"
    f"FY2023 comparative: MCA Annual report and accounts 2024, Note 11, pp.47-48 - {AR_2024}\n"
    f"FY2022 and FY2021 comparative: MCA Annual report and accounts 2022, Note 13, pp.48-49 - {AR_2022}\n"
    f"FY2020: Companies House full accounts to 31 December 2020, Note 13, p.36 - {CH_FY2020}\n"
    f"FY2019 comparative: Companies House full accounts to 31 December 2020, Note 13, p.36 - {CH_FY2020}\n"
    f"FY2018: Companies House full accounts to 31 December 2018, Note 13, p.34 - {CH_FY2018}\n"
    f"FY2017 comparative: Companies House full accounts to 31 December 2018, Note 13, p.34 - {CH_FY2018}\n"
    f"FY2016: Companies House full accounts to 31 December 2016, Note 13, p.32 - {CH_FY2016}\n\n"
    "Note: the Company applies FRS 102 (not IFRS 9), so no Stage 1/2/3 ECL split is disclosed - credit quality "
    "is shown instead via the Company's own product/security split and a single collective 'Provision for bad "
    "debts' balance. No past-due/impaired-loan analysis beyond the provision balance was located.\n\n"
    + ENTITY
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - Methodist Chapel Aid Limited entity-level Pillar 1 capital requirement / RWA breakdown by "
    "exposure class, £'000:\n"
    + LINK_ROT_NOTE +
    f"FY2023: Pillar 3 Disclosures for year ended 31 December 2023, Section 5 Capital Adequacy table, p.7 - "
    f"{P3_2023_WAYBACK} (Wayback `id_` snapshot of 7 April 2025; the Company's own URL, {P3_2023_DEAD}, "
    f"returns HTTP 404 - re-checked 2026-09-15)\n"
    f"FY2022: Pillar 3 Disclosures for year ended 31 December 2022, Section 5 Capital Adequacy table, p.8 - "
    f"{P3_2022} (still live; the Company's duplicate copy at {P3_2022_DEAD} is dead but byte-identical in "
    f"the archive - see the FY2022 entry on the Pillar 3 metric sheets for the full check)\n"
    f"FY2021: Pillar 3 Disclosures for year ended 31 December 2021, Section 5 Capital Adequacy table, p.6 - "
    f"{P3_2021_WAYBACK} (Wayback `id_` snapshot of 25 June 2022, the only capture of this file in the CDX "
    f"index; re-fetched 2026-09-15, 319,857 bytes, begins `%PDF-`. The Company's own URL, {P3_2021_DEAD}, "
    f"is dead). CORRECTION 2026-09-15: this sheet previously said no category-level breakdown "
    "existed for FY2021 and left every category row blank. That was a sourcing miss, not an absence. The "
    "FY2021 standalone Pillar 3 document does exist and carries the same Section 5 capital-adequacy table as "
    "every other year; it was missed because the Company changed its filename convention for this one "
    "edition - every other year is 'pillar3disclosures<YYYY>.pdf', but FY2021 is "
    "'2021-pillar-3-disclosures.pdf', so guessing filenames by pattern could never reach it. It was found by "
    "listing the whole mcafundingforchurches.co.uk domain from the Wayback CDX index instead of constructing "
    "candidate URLs. FY2021 uses the pre-FY2022 aggregate presentation of customer loans (a single 'drawn' "
    "and '50% of undrawn' pair, not the property/car split introduced in FY2022), which is why those rows "
    "carry FY2021 alongside FY2020/FY2019.\n"
    "FY2021 RECONCILIATION - the category rows deliberately do NOT sum to the Total RWAs row, and this is a "
    "real difference between two of the Company's own documents rather than a transcription error. The "
    "FY2021 document's own table gives credit risk RWA of 25,171 and an operational risk capital requirement "
    "of 92 (= 1,150 RWA at x12.5, the document's own Pillar 1 formula), totalling 26,321. The FY2022 "
    "document's Key Metrics comparative column states 26,369 for the same date, £48k higher. The Total RWAs "
    "row keeps the 26,369 Key Metrics figure so that this sheet ties to the Total RWAs sheet, and the £48k "
    "gap is flagged here rather than silently reconciled by adjusting either source.\n"
    "FY2024/FY2025: no Pillar 3 Key Metrics table or capital-adequacy breakdown was located for these "
    "periods (consistent with the existing Total RWAs sheet, which is also blank for these years).\n"
    f"FY2020: Pillar 3 Disclosures for year ended 31 December 2020, Section 5 Capital Adequacy table, p.7 "
    f"- {P3_2020_WAYBACK} (Wayback `id_` snapshot of 15 May 2021; the Company's own URL, {P3_2020_DEAD}, "
    f"is dead). Operational risk RWA is derived as "
    "capital requirement x 12.5 (i.e. /8%), the same Pillar 1 formula the document itself states, since the "
    "table discloses operational risk only as a capital requirement, not directly as RWA.\n"
    f"FY2019: Pillar 3 Disclosures for year ended 31 December 2019, Section 5 Capital Adequacy table, p.7 "
    f"- {P3_2019_WAYBACK} (Wayback `id_` snapshot of 30 September 2020; the Company's own URL, "
    f"{P3_2019_DEAD}, is dead). Operational risk RWA derived the same way.\n"
    + PRE2019_STATUS + "\n\n"
    + ENTITY
)


bw = BankWorkbook("Methodist Chapel Aid Limited", YEARS, header_color="6B4E71")

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and bank balances", {"FY2025": 9417754, "FY2024": 8355272, "FY2023": 7520873, "FY2022": 10132743, "FY2021": 12459792, "FY2020": 13653122, "FY2019": 10947148, "FY2018": 10984433, "FY2017": 11252440, "FY2016": 12174432}),
    ("DATA", "Loans and advances to customers", {"FY2025": 8262627, "FY2024": 9138711, "FY2023": 10330064, "FY2022": 8485497, "FY2021": 7197340, "FY2020": 7314586, "FY2019": 7888087, "FY2018": 6315264, "FY2017": 5210921, "FY2016": 4295209}),
    ("DATA", "Investments - issued by public body", {"FY2025": 4941874, "FY2024": 4208030, "FY2023": 4824018}),
    ("DATA", "Investments - other loans and advances", {"FY2025": 3843427, "FY2024": 4049871, "FY2023": 4500425}),
    ("DATA", "Investments - debt and fixed income securities (aggregate, pre-2021 disclosure)", {"FY2020": 9047492, "FY2019": 8170744, "FY2018": 7957868, "FY2017": 8122521, "FY2016": 7940441}),
    ("DATA", "Investments - equity investments", {"FY2025": 8230600, "FY2024": 8135418, "FY2023": 7100690, "FY2020": 8606515, "FY2019": 8368796, "FY2018": 7260746, "FY2017": 8090285, "FY2016": 7927810}),
    ("TOTAL", "Total investments", {"FY2025": 17015901, "FY2024": 16393319, "FY2023": 16425133, "FY2022": 16047858, "FY2021": 17733105, "FY2020": 17654007, "FY2019": 16539540, "FY2018": 15218614, "FY2017": 16212806, "FY2016": 15868251}),
    ("DATA", "Intangible fixed assets", {"FY2025": 3957}),
    ("DATA", "Tangible fixed assets", {"FY2025": 287367, "FY2024": 300959, "FY2023": 305490, "FY2022": 37749, "FY2021": 31127, "FY2020": 7852, "FY2019": 22084, "FY2018": 32058, "FY2017": 50429, "FY2016": 66102}),
    ("DATA", "Investments held for short term purposes", {"FY2025": 748688, "FY2024": 1831800, "FY2023": 1576261, "FY2022": 2380720, "FY2021": 2661841, "FY2020": 236135, "FY2019": 862056, "FY2018": 892171, "FY2017": 750539, "FY2016": 476027}),
    ("DATA", "Prepayments, accrued income and other assets", {"FY2025": 219743, "FY2024": 127040, "FY2023": 135703, "FY2022": 109921, "FY2021": 71600, "FY2020": 74764, "FY2019": 110945, "FY2018": 93275, "FY2017": 99700, "FY2016": 92648}),
    ("TOTAL", "Total Assets", {"FY2025": 35956037, "FY2024": 36147101, "FY2023": 36293524, "FY2022": 37194488, "FY2021": 40154805, "FY2020": 38940466, "FY2019": 36369860, "FY2018": 33535815, "FY2017": 33576835, "FY2016": 32972669}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer accounts", {"FY2025": 21227564, "FY2024": 22043458, "FY2023": 22687021, "FY2022": 24113288, "FY2021": 25374073, "FY2020": 25034413, "FY2019": 23169408, "FY2018": 21897604, "FY2017": 21344785, "FY2016": 21572515}),
    ("DATA", "Other liabilities", {"FY2025": 370311, "FY2024": 167472, "FY2023": 131713, "FY2022": 83947, "FY2021": 64139, "FY2020": 167071, "FY2019": 75034, "FY2018": 64494, "FY2017": 85883, "FY2016": 88824}),
    ("TOTAL", "Total Liabilities", {"FY2025": 21597875, "FY2024": 22210930, "FY2023": 22818734, "FY2022": 24197235, "FY2021": 25438212, "FY2020": 25201484, "FY2019": 23244442, "FY2018": 21962098, "FY2017": 21430668, "FY2016": 21661339}),
    ("SECTION", "Provisions", {}),
    ("DATA", "Deferred tax", {"FY2025": 241076, "FY2024": 188844, "FY2023": 121158, "FY2022": 45234, "FY2021": 540391, "FY2020": 295993, "FY2019": 257972, "FY2018": 4956, "FY2017": 147721, "FY2016": 239818}),
    ("TOTAL", "Net Assets", {"FY2025": 14117086, "FY2024": 13747327, "FY2023": 13353632, "FY2022": 12952019, "FY2021": 14176202, "FY2020": 13442989, "FY2019": 12867446, "FY2018": 11568761, "FY2017": 11998446, "FY2016": 11071512}),
    ("SECTION", "Shareholders' Funds", {}),
    ("DATA", "Called up equity share capital", {"FY2025": 1197, "FY2024": 1197, "FY2023": 1197, "FY2022": 1197, "FY2021": 1197, "FY2020": 1197, "FY2019": 1197, "FY2018": 1197, "FY2017": 1197, "FY2016": 1197}),
    ("DATA", "Reserves", {"FY2025": 14115889, "FY2024": 13746130, "FY2023": 13352435, "FY2022": 12950822, "FY2021": 14175005, "FY2020": 13441792, "FY2019": 12866249, "FY2018": 11567564, "FY2017": 11997249, "FY2016": 11070315}),
    ("TOTAL", "Total equity", {"FY2025": 14117086, "FY2024": 13747327, "FY2023": 13353632, "FY2022": 12952019, "FY2021": 14176202, "FY2020": 13442989, "FY2019": 12867446, "FY2018": 11568761, "FY2017": 11998446, "FY2016": 11071512}),
]
bw.add_balance_sheet_sheet(
    "Methodist Chapel Aid Limited — Statement of Financial Position",
    "Entity-level basis, £. FY2025 as at 30 September 2025 (9-month period end); all other years as at 31 December.",
    balance_sheet_rows,
    STATEMENTS_SOURCES,
    first_col_width=58,
    source_height=230,
    unit_suffix=" (£)",
)

income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable - on loans", {"FY2025": 364536, "FY2024": 542736, "FY2023": 485539, "FY2022": 241994, "FY2021": 226796, "FY2020": 238045, "FY2019": 216819, "FY2018": 188593, "FY2017": 150120, "FY2016": 140331}),
    ("DATA", "Interest receivable - on debt securities", {"FY2025": 254891, "FY2024": 351721, "FY2023": 346423, "FY2022": 292232, "FY2021": 297207, "FY2020": 310571, "FY2019": 321383, "FY2018": 322478, "FY2017": 326582, "FY2016": 329862}),
    ("DATA", "Interest receivable - on bank and building society deposits", {"FY2025": 301668, "FY2024": 412981, "FY2023": 347139, "FY2022": 114132, "FY2021": 11584, "FY2020": 42272, "FY2019": 71244, "FY2018": 57941, "FY2017": 42354, "FY2016": 89504}),
    ("DATA", "Interest payable to depositors", {"FY2025": -513856, "FY2024": -702772, "FY2023": -570746, "FY2022": -167638, "FY2021": -158940, "FY2020": -218608, "FY2019": -229881, "FY2018": -206421, "FY2017": -182991, "FY2016": -263234}),
    ("DATA", "Interest payable - amortisation of debt securities", {"FY2025": -12204, "FY2024": -55620, "FY2023": -101184, "FY2022": -87073, "FY2021": -86814, "FY2020": -96429, "FY2019": -69882, "FY2018": -61467, "FY2017": -54842, "FY2016": -52449}),
    ("DATA", "Dividend income from equity shares", {"FY2025": 149236, "FY2024": 186640, "FY2023": 172192, "FY2022": 226757, "FY2021": 220001, "FY2020": 190548, "FY2019": 259323, "FY2018": 261860, "FY2017": 271126, "FY2016": 287571}),
    ("DATA", "Investment gains/(losses) on debt securities", {"FY2024": -371214, "FY2023": -27579, "FY2022": -12251, "FY2021": -30549, "FY2020": 328406, "FY2019": 4366, "FY2018": 37062, "FY2017": 4681, "FY2016": 24643}),
    ("DATA", "Fees and commissions payable to Investment Manager", {"FY2025": -32837, "FY2024": -3575, "FY2023": -19845, "FY2022": -37299, "FY2021": -29476, "FY2020": -43050, "FY2019": -43816, "FY2018": -51541, "FY2017": -52371, "FY2016": -66220}),
    ("DATA", "Other operating income", {"FY2025": 4302, "FY2024": 4900, "FY2023": 6543, "FY2022": 11797, "FY2021": 177145, "FY2020": 2924, "FY2019": 5692, "FY2018": 3666, "FY2017": 7218, "FY2016": 3925}),
    # Derived sum (not a printed AR subtotal) of every DATA row in the Income
    # section above, so the cross-bank insights pipeline (in041_spend_metrics.py)
    # has a TOTAL-tagged revenue row to divide against. FY2025 excludes
    # "Investment gains/(losses) on debt securities" since the AR doesn't
    # disclose that line for the 9-month FY2025 period.
    ("TOTAL", "Total income", {"FY2025": 515736, "FY2024": 365797, "FY2023": 638482, "FY2022": 582651, "FY2021": 626954, "FY2020": 754679, "FY2019": 535248, "FY2018": 552171, "FY2017": 511877, "FY2016": 493933}),
    ("DATA", "Administrative expenses - staff costs", {"FY2025": -241735, "FY2024": -310501, "FY2023": -281131, "FY2022": -236031, "FY2021": -202930, "FY2020": -205751, "FY2019": -198443, "FY2018": -191928, "FY2017": -180526, "FY2016": -179379}),
    ("DATA", "Administrative expenses - other", {"FY2025": -230594, "FY2024": -246970, "FY2023": -260190, "FY2022": -212268, "FY2021": -154761, "FY2020": -150767, "FY2019": -162438, "FY2018": -159701, "FY2017": -162332, "FY2016": -162246}),
    # Derived sum (not a printed AR subtotal) of the two administrative expense
    # DATA rows above, so the cross-bank insights pipeline has a TOTAL-tagged
    # opex row to divide against.
    ("TOTAL", "Total administrative expenses", {"FY2025": -472329, "FY2024": -557471, "FY2023": -541321, "FY2022": -448299, "FY2021": -357691, "FY2020": -356518, "FY2019": -360881, "FY2018": -351629, "FY2017": -342858, "FY2016": -341625}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -9635, "FY2024": -13288, "FY2023": -9937, "FY2022": -7168, "FY2021": -3633, "FY2020": -14732, "FY2019": -17132, "FY2018": -18651, "FY2017": -18377, "FY2016": -14038}),
    ("TOTAL", "Operating surplus/(deficit)", {"FY2025": 33772, "FY2024": -204962, "FY2023": 87224, "FY2022": 127184, "FY2021": 265630, "FY2020": 383429, "FY2019": 157235, "FY2018": 181891, "FY2017": 150642, "FY2016": 138270}),
    ("DATA", "Fair value adjustment to investments", {"FY2025": 385195, "FY2024": 694496, "FY2023": 391546, "FY2022": -1845411, "FY2021": 711942, "FY2020": 318792, "FY2019": 1402028, "FY2018": -754426, "FY2017": 729845, "FY2016": 666013}),
    ("TOTAL", "Surplus/(deficit) on ordinary activities before taxation", {"FY2025": 418967, "FY2024": 489534, "FY2023": 478770, "FY2022": -1718227, "FY2021": 977572, "FY2020": 702221, "FY2019": 1559263, "FY2018": -572535, "FY2017": 880487, "FY2016": 804283}),
    ("DATA", "Tax on surplus/(deficit) on ordinary activities", {"FY2025": -47855, "FY2024": -94522, "FY2023": -75924, "FY2022": 495157, "FY2021": -243291, "FY2020": -125620, "FY2019": -259537, "FY2018": 143868, "FY2017": 47426, "FY2016": -46629}),
    ("TOTAL", "Surplus/(deficit) for the period/year and total comprehensive income", {"FY2025": 371112, "FY2024": 395012, "FY2023": 402846, "FY2022": -1223070, "FY2021": 734281, "FY2020": 576601, "FY2019": 1299726, "FY2018": -428667, "FY2017": 927913, "FY2016": 757654}),
]
bw.add_income_statement_sheet(
    "Methodist Chapel Aid Limited — Statement of Income and Retained Earnings",
    "Entity-level basis, £. FY2025 covers the 9 months ended 30 September 2025; all other years are 12-month periods.",
    income_statement_rows,
    STATEMENTS_SOURCES,
    first_col_width=64,
    source_height=230,
    unit_suffix=" (£)",
)

equity_headers = ["Called up share capital", "Reserves", "Total equity"]
equity_rows = [
    ("TOTAL", "Balance at 1 January 2016", (1197, 10313628, 10314825)),
    ("DATA", "Surplus for the year", (None, 757654, 757654)),
    ("DATA", "Dividends paid and payable", (None, -967, -967)),
    ("TOTAL", "Balance at 31 December 2016 / 1 January 2017", (1197, 11070315, 11071512)),
    ("DATA", "Surplus for the year", (None, 927913, 927913)),
    ("DATA", "Dividends paid and payable", (None, -979, -979)),
    ("TOTAL", "Balance at 31 December 2017 / 1 January 2018", (1197, 11997249, 11998446)),
    ("DATA", "Deficit for the year", (None, -428667, -428667)),
    ("DATA", "Dividends paid and payable", (None, -1018, -1018)),
    ("TOTAL", "Balance at 31 December 2018 / 1 January 2019", (1197, 11567564, 11568761)),
    ("DATA", "Surplus for the year", (None, 1299726, 1299726)),
    ("DATA", "Dividends paid and payable", (None, -1041, -1041)),
    ("TOTAL", "Balance at 31 December 2019 / 1 January 2020", (1197, 12866249, 12867446)),
    ("DATA", "Surplus for the year", (None, 576601, 576601)),
    ("DATA", "Dividends paid and payable", (None, -1058, -1058)),
    ("TOTAL", "Balance at 31 December 2020 / 1 January 2021", (1197, 13441792, 13442989)),
    ("DATA", "Surplus for the year", (None, 734281, 734281)),
    ("DATA", "Dividends paid and payable", (None, -1068, -1068)),
    ("TOTAL", "Balance at 31 December 2021 / 1 January 2022", (1197, 14175005, 14176202)),
    ("DATA", "Deficit for the year", (None, -1223070, -1223070)),
    ("DATA", "Dividends paid and payable", (None, -1113, -1113)),
    ("TOTAL", "Balance at 31 December 2022 / 1 January 2023", (1197, 12950822, 12952019)),
    ("DATA", "Surplus for the year", (None, 402846, 402846)),
    ("DATA", "Dividends paid and payable", (None, -1233, -1233)),
    ("TOTAL", "Balance at 31 December 2023 / 1 January 2024", (1197, 13352435, 13353632)),
    ("DATA", "Surplus for the year", (None, 395012, 395012)),
    ("DATA", "Dividends paid and payable", (None, -1317, -1317)),
    ("TOTAL", "Balance at 31 December 2024 / 1 January 2025", (1197, 13746130, 13747327)),
    ("DATA", "Surplus for the period (9 months)", (None, 371112, 371112)),
    ("DATA", "Dividends paid and payable", (None, -1353, -1353)),
    ("TOTAL", "Balance at 30 September 2025", (1197, 14115889, 14117086)),
]
bw.add_equity_changes_sheet(
    "Methodist Chapel Aid Limited — Statement of Changes in Equity",
    "Entity-level basis, £. Reconstructed from the combined Statement of Income and Retained Earnings, chronological, oldest to newest.",
    equity_headers,
    equity_rows,
    STATEMENTS_SOURCES,
    source_height=230,
)

cash_rows = [
    ("SECTION", "Operating activities", {}),
    ("TOTAL", "Net cash generated/(used) from operating activities", {"FY2025": 230314, "FY2024": 429322, "FY2023": -3050504, "FY2022": -2346030, "FY2021": 714322, "FY2020": 2973715, "FY2019": -70421, "FY2018": -303376, "FY2017": -974245, "FY2016": 161846}),
    ("SECTION", "Investing activities", {}),
    ("TOTAL", "Net cash generated/(used) from investing activities", {"FY2025": -249591, "FY2024": 661933, "FY2023": -364592, "FY2022": -261027, "FY2021": 519122, "FY2020": -892604, "FY2019": 4062, "FY2018": 178019, "FY2017": 327744, "FY2016": 171836}),
    ("SECTION", "Financing activities", {}),
    ("TOTAL", "Net cash generated/(used) in financing activities", {"FY2025": -1353, "FY2024": -1317, "FY2023": -1233, "FY2022": -1113, "FY2021": -1068, "FY2020": -1058, "FY2019": -1041, "FY2018": -1018, "FY2017": -979, "FY2016": -967}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": -20630, "FY2024": 1089938, "FY2023": -3416329, "FY2022": -2608170, "FY2021": 1232376, "FY2020": 2080053, "FY2019": -67400, "FY2018": -126375, "FY2017": -647480, "FY2016": 332715}),
    ("DATA", "Cash and cash equivalents at the beginning of year/period", {"FY2025": 10187072, "FY2024": 9097134, "FY2023": 12513463, "FY2022": 15121633, "FY2021": 13889257, "FY2020": 11809204, "FY2019": 11876604, "FY2018": 12002979, "FY2017": 12650459, "FY2016": 12317744}),
    ("TOTAL", "Cash and cash equivalents at the end of year/period", {"FY2025": 10166442, "FY2024": 10187072, "FY2023": 9097134, "FY2022": 12513463, "FY2021": 15121633, "FY2020": 13889257, "FY2019": 11809204, "FY2018": 11876604, "FY2017": 12002979, "FY2016": 12650459}),
]
bw.add_cash_flow_sheet(
    "Methodist Chapel Aid Limited — Cash Flow Statement",
    "Entity-level basis, £",
    cash_rows,
    cash_sources(),
    first_col_width=65,
    source_height=190,
    unit_suffix=" (£)",
)

asset_quality_rows = [
    ("SECTION", "Loan book by product (gross)", {}),
    ("DATA", "Property loans - secured", {"FY2025": 6882826, "FY2024": 7487986, "FY2023": 7265355, "FY2022": 7037375, "FY2021": 5840927, "FY2020": 6141270, "FY2019": 6821441, "FY2018": 5789736, "FY2017": 4159580, "FY2016": 3532033}),
    ("DATA", "Property loans - unsecured", {"FY2025": 1375657, "FY2024": 1644631, "FY2023": 3055122, "FY2022": 1432495, "FY2021": 1346352, "FY2020": 1160251, "FY2019": 1039071, "FY2018": 477458, "FY2017": 972672, "FY2016": 643066}),
    ("TOTAL", "Property loans - total", {"FY2025": 8258483, "FY2024": 9132617, "FY2023": 10320477, "FY2022": 8469870, "FY2021": 7187279, "FY2020": 7301521, "FY2019": 7860512, "FY2018": 6267194, "FY2017": 5132252, "FY2016": 4175099}),
    ("DATA", "Car loans - unsecured", {"FY2025": 4250, "FY2024": 6250, "FY2023": 9833, "FY2022": 16028, "FY2021": 10319, "FY2020": 13400, "FY2019": 28282, "FY2018": 49302, "FY2017": 80686, "FY2016": 123190}),
    ("TOTAL", "Total loans and advances (gross)", {"FY2025": 8262733, "FY2024": 9138867, "FY2023": 10330310, "FY2022": 8485898, "FY2021": 7197598, "FY2020": 7314921, "FY2019": 7888794, "FY2018": 6316496, "FY2017": 5212938, "FY2016": 4298289}),
    ("DATA", "Provision for bad debts", {"FY2025": -106, "FY2024": -156, "FY2023": -246, "FY2022": -401, "FY2021": -258, "FY2020": -335, "FY2019": -707, "FY2018": -1232, "FY2017": -2017, "FY2016": -3080}),
    ("TOTAL", "Total loans and advances (net)", {"FY2025": 8262627, "FY2024": 9138711, "FY2023": 10330064, "FY2022": 8485497, "FY2021": 7197340, "FY2020": 7314586, "FY2019": 7888087, "FY2018": 6315264, "FY2017": 5210921, "FY2016": 4295209}),
    ("SECTION", "Maturity profile of loans and advances (net)", {}),
    ("DATA", "Due within 3 months", {"FY2025": 480809, "FY2024": 350750, "FY2023": 1449455, "FY2022": 1861, "FY2021": 1848, "FY2020": 57672, "FY2019": 488356, "FY2018": 8880, "FY2017": 12201, "FY2016": 9959}),
    ("DATA", "In more than 3 months but not more than 1 year", {"FY2025": 1166309, "FY2024": 1907530, "FY2023": 2103477, "FY2022": 2223451, "FY2021": 364515, "FY2020": 672303, "FY2019": 588968, "FY2018": 1190672, "FY2017": 1211741, "FY2016": 1183851}),
    ("DATA", "In more than 1 year but not more than 5 years", {"FY2025": 3075037, "FY2024": 3184280, "FY2023": 3463531, "FY2022": 3069212, "FY2021": 3182168, "FY2020": 2328530, "FY2019": 1827551, "FY2018": 1796008, "FY2017": 1588387, "FY2016": 1241379}),
    ("DATA", "In more than 5 years", {"FY2025": 3540578, "FY2024": 3696307, "FY2023": 3313847, "FY2022": 3191374, "FY2021": 3649067, "FY2020": 4256416, "FY2019": 4983919, "FY2018": 3320936, "FY2017": 2400609, "FY2016": 1863100}),
]
bw.add_asset_quality_sheet(
    "Methodist Chapel Aid Limited — Asset Quality",
    "Entity-level basis, £. FRS 102 reporting - no IFRS 9 Stage 1/2/3 split disclosed; credit quality shown via product/security split and a single collective provision for bad debts.",
    asset_quality_rows,
    ASSET_QUALITY_SOURCES,
    first_col_width=62,
    source_height=210,
    unit_suffix=" (£)",
)


# ---------------------------------------------------------------------------
# THE FY2024/FY2025 FINDING, WRITTEN WHERE A READER AND A TOOL CAN SEE IT.
# Added 2026-09-18 (remaining-gap round). The exemption below was established in
# earlier sessions and is set out at length in SDDT_NOTE and p3_sources(), but
# it lived ONLY in prose - the FY2024 and FY2025 year columns of all twelve
# Pillar 3 sheets sat empty, and an empty cell is indistinguishable from a year
# nobody has looked at. `audit_gaps.py` scored 24 sheet-years here as
# unexplained gaps for exactly that reason. The statement now goes in the CELL;
# the evidence stays in the source note.
#
# RE-VERIFIED INDEPENDENTLY 2026-09-18, not carried over on trust:
#   * PRA consolidated waivers register downloaded fresh that day (2,899 rows)
#     and matched on BOTH conjuncts - Rule Description 'SDDT Regime - General
#     Application' AND Sub Rule Number 'Ru 3.1'. Either column alone is wrong.
#     The row: FRN 204508, 'Methodist Chapel Aid Limited', ref A00007737P.pdf,
#     start 11/04/2024, NO end date. The Company's other register row (Permissions
#     and Waivers (CRR Firms), CA.BU 5.1-5.3, 06/11/2024) is a capital-buffers
#     direction, not a disclosure exemption, and is not relied on.
#   * The Company's own index, https://www.mcafundingforchurches.co.uk/about-us/
#     financial-information/, fetched live the same day (HTTP 200, text/html,
#     7,185 bytes - not a block, not an interstitial). It lists exactly three
#     PDFs: mca-ar-2025.pdf, country-by-country-reporting-2025.pdf and an FSCS
#     leaflet. No Pillar 3 document of any vintage.
#
# DATE FIT, STATED PER YEAR because a modification cannot excuse a reporting
# date that precedes it:
#   FY2024 reporting date 31 December 2024 - AFTER 11 April 2024. Covered.
#   FY2025 reporting date 30 September 2025 (a 9-month period; the accounting
#     reference date moved from 31 December during 2025) - AFTER. Covered.
# Both are covered, so both cells carry the same statement. FY2023 (31 December
# 2023) PRECEDES the modification, which is exactly why an FY2023 edition exists
# and is the last one that does. Nothing here reaches back past FY2023, and in
# particular it says nothing about FY2016-FY2018, whose blanks are UNPROVEN for
# an unrelated reason (see PRE2019_STATUS).
#
# This is outcome 2 (never published), not outcome 3 (unreached today): the duty
# was removed by a dated instrument, so no FY2024 or FY2025 Pillar 3 document
# exists anywhere to be fetched.
MCA_P3_STATUS = {
    "FY2025": "Not published - SDDT Rule 3.1 opt-in from 11/04/2024",
    "FY2024": "Not published - SDDT Rule 3.1 opt-in from 11/04/2024",
}


def metric(name, unit, label, data, note=None):
    bw.add_metric_sheet(name, unit, [(label, dict(MCA_P3_STATUS, **data))], p3_sources(), note=note,
                        first_col_width=50, source_height=190)


def metric_rows(name, unit, rows, note=None):
    """Same as metric() but for sheets that must carry more than one basis on separate rows."""
    bw.add_metric_sheet(name, unit, rows, p3_sources(), note=note, first_col_width=50, source_height=190)


# Shared explanation for the LCR and NSFR sheets, both of which were corrected on 2026-09-15.
LIQUIDITY_BASIS_NOTE = (
    "TWO BASES, KEPT ON SEPARATE ROWS (corrected 2026-09-15). This sheet previously carried a single row "
    "labelled as the AVERAGE ratio which in fact mixed two different series, and the mixture was not "
    "visible to a reader. Each of the Company's Pillar 3 documents publishes the metric twice, on "
    "different bases:\n"
    "  (a) an AVERAGE for the financial year, described by the document itself as 'based on quarterly "
    "end-of-month positions over the preceding 12 months', shown beneath a four-column quarterly table; and\n"
    "  (b) a YEAR-END point-in-time figure, in the UK KM1 Key Metrics table at the front of the document.\n"
    "The old single row took the average for FY2023 but the KM1 year-end figure for FY2022 and FY2021, so a "
    "reader comparing FY2023 with FY2022 was comparing an average against a point-in-time value. Both "
    "series are now shown in full, each on its own labelled row, and neither is merged into the other.\n"
    "ONE SOURCE QUIRK, RECORDED RATHER THAN CORRECTED: in both the FY2022 and FY2023 editions the KM1 "
    "table's HQLA input row is captioned '(Weighted value - average)', yet the ratio the KM1 states is "
    "demonstrably the year-end point-in-time value - it reproduces the 31-December column of that same "
    "document's own quarterly table exactly (FY2023: KM1 970% = the quarterly table's 31-Dec-23 column; "
    "FY2022: KM1 833% = its 31-Dec-22 column), while the document's separately-stated average for the same "
    "year is a different number (835% and 827% respectively). The KM1 caption is therefore inaccurate in "
    "the source. The year-end rows here are labelled for what the figures demonstrably are, not for what "
    "the KM1 caption says, and the caption discrepancy is left as published.\n"
    "FY2021 appears on the year-end row only, and that is not an oversight: the FY2021 standalone Pillar 3 "
    "document contains no KM1 table and no quarterly averaging table at all, so no FY2021 average was ever "
    "published. Its year-end figure survives solely as the comparative column of the FY2022 edition's KM1."
)


# ---------------------------------------------------------------
# KM1 Key Metrics - the Company's own "Key Metrics table", reproduced whole.
#
# THIS BANK DOES PUBLISH THE TEMPLATE, despite being a ten-person mutual whose
# whole Pillar 3 document is 22 pages. It is easy to miss, because:
#
#   * IT IS UNNUMBERED. The Company prints no row numbers at all - no "1", no
#     "UK 7a". Under the row-set test that is irrelevant: what makes a table
#     the template is the ROW SET, not the numbering, and this one carries the
#     full UK KM1 row set (available own funds, risk-weighted exposure
#     amounts, capital ratios, C-SREP additional own funds requirements,
#     combined buffer requirement, leverage ratio, LCR block, NSFR block). It
#     is the Europe Arab Bank pattern, not the ABC International Bank pattern.
#   * IT IS NEVER CALLED "KM1". The heading is "1.1 Key Metrics table", and
#     the string "KM1" appears nowhere in any edition.
#   * IT EXISTS IN ONLY TWO EDITIONS. The Company published a Pillar 3
#     disclosure for five consecutive years, FY2019 through FY2023, and then
#     stopped; only the FY2022 and FY2023 editions contain the table.
#
# ROWS THE COMPANY PRINTS THAT THE STANDARD TEMPLATE DOES NOT, kept as
# published: "Systemic risk buffer (%)" (zero in every year) sits inside the
# combined buffer block, and the SREP block is captioned against the PRA's
# C-SREP rather than the generic SREP.
#
# SOURCE DEFECTS, REPRODUCED RATHER THAN CORRECTED:
#   * The combined-buffer section heading is TRUNCATED in both editions - it
#     reads "Combined buffer requirement (as a percentage of risk-weighted
#     exposure" with the word "amount" missing. Kept as printed.
#   * The LCR block's HQLA row is captioned "(Weighted value - average)" but
#     the figures are year-end point-in-time values, not averages - proven by
#     the same documents' own quarterly tables (the KM1's 970% for FY2023 is
#     the 31-Dec-23 column of the quarterly table, while that document's
#     stated average for FY2023 is 835%). The caption is left as published and
#     the discrepancy is flagged; the LCR and NSFR metric sheets carry both
#     bases on separate rows.
#   * The explanatory note about the 18.27% base capital requirement is
#     printed ABOVE the table in the FY2023 edition and BELOW it in the
#     FY2022 edition. Recorded once here.
#
# ZERO GLYPHS (map rule 2): every zero in this table is printed as a real
# "0.00%", never as a dash, so each is recorded as a zero rather than blanked.
# ---------------------------------------------------------------
km1_rows = [
    # Not a template row - a status row, carried FIRST so the two newest columns
    # say what happened to them instead of sitting blank. It is deliberately NOT
    # given a KM1 row number and does not begin with any of the Company's printed
    # wording, so `verify_workbook.py`'s startswith-matching cannot mistake it for
    # a template row (KM1 map rule 32a). Nothing below it is altered.
    ("DATA", "Pillar 3 edition status for this year (see source note)", MCA_P3_STATUS),
    ("SECTION", "Available own funds (amounts)", {}),
    ("DATA", "Common Equity Tier 1 (CET1) capital (£'000)",
     {"FY2023": 13354, "FY2022": 12952, "FY2021": 13919}),
    ("DATA", "Tier 1 capital (£'000)",
     {"FY2023": 13354, "FY2022": 12952, "FY2021": 13919}),
    ("DATA", "Total capital (£'000)",
     {"FY2023": 13354, "FY2022": 12952, "FY2021": 13919}),
    ("SECTION", "Risk-weighted exposure amounts", {}),
    ("DATA", "Total risk-weighted exposure amount (£'000)",
     {"FY2023": 25253, "FY2022": 24052, "FY2021": 26369}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "Common Equity Tier 1 (CET1) ratio (%)",
     {"FY2023": "52.88%", "FY2022": "53.85%", "FY2021": "52.79%"}),
    ("DATA", "Tier 1 ratio (%)",
     {"FY2023": "52.88%", "FY2022": "53.85%", "FY2021": "52.79%"}),
    ("DATA", "Total capital ratio (%)",
     {"FY2023": "52.88%", "FY2022": "53.85%", "FY2021": "52.79%"}),
    ("SECTION", "Additional own funds requirements based on PRA Supervisory Review Process (C-SREP) "
                "(as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "Additional SREP own funds requirements (%)",
     {"FY2023": "0.00%", "FY2022": "0.00%", "FY2021": "0.00%"}),
    ("DATA", "Total SREP own funds requirements (%)",
     {"FY2023": "18.27%", "FY2022": "18.27%", "FY2021": "18.27%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure "
                "[heading truncated in the source, which omits the word 'amount'])", {}),
    ("DATA", "Capital conservation buffer (%)",
     {"FY2023": "2.50%", "FY2022": "2.50%", "FY2021": "2.50%"}),
    ("DATA", "Institution specific countercyclical capital buffer (%)",
     {"FY2023": "1.97%", "FY2022": "0.98%", "FY2021": "0.00%"}),
    ("DATA", "Systemic risk buffer (%)",
     {"FY2023": "0.00%", "FY2022": "0.00%", "FY2021": "0.00%"}),
    ("DATA", "Combined buffer requirement (%)",
     {"FY2023": "4.47%", "FY2022": "3.48%", "FY2021": "2.50%"}),
    ("DATA", "Overall capital requirements (%)",
     {"FY2023": "22.74%", "FY2022": "21.75%", "FY2021": "20.77%"}),
    ("DATA", "CET1 available after meeting the total SREP own funds requirements (%)",
     {"FY2023": "30.14%", "FY2022": "32.10%", "FY2021": "32.02%"}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "Leverage ratio total exposure measure (£'000)",
     {"FY2023": 37777, "FY2022": 38672, "FY2021": 42114}),
    ("DATA", "Leverage ratio (%)",
     {"FY2023": "35.35%", "FY2022": "33.49%", "FY2021": "33.05%"}),
    ("SECTION", "Liquidity Coverage Ratio", {}),
    ("DATA", "Total high-quality liquid assets (HQLA) (Weighted value - average) (£'000)",
     {"FY2023": 4373, "FY2022": 4231, "FY2021": 4220}),
    ("DATA", "Cash outflows - Total weighted value (£'000)",
     {"FY2023": 1803, "FY2022": 2032, "FY2021": 2801}),
    ("DATA", "Cash inflows - Total weighted value (£'000)",
     {"FY2023": 5596, "FY2022": 8745, "FY2021": 11248}),
    ("DATA", "Total net cash outflows (adjusted value) (£'000)",
     {"FY2023": 451, "FY2022": 508, "FY2021": 700}),
    ("DATA", "Liquidity coverage ratio (%)",
     {"FY2023": "970%", "FY2022": "833%", "FY2021": "603%"}),
    ("SECTION", "Net Stable Funding Ratio (NSFR)", {}),
    ("DATA", "Total available stable funding (£'000)",
     {"FY2023": 34839, "FY2022": 35740, "FY2021": 37077}),
    ("DATA", "Total required stable funding (£'000)",
     {"FY2023": 20068, "FY2022": 18568, "FY2021": 20165}),
    ("DATA", "NSFR (%)",
     {"FY2023": "174%", "FY2022": "192%", "FY2021": "184%"}),
]

KM1_SOURCES = (
    "Sources - the Company's own 'Key Metrics table', section 1.1 of its Pillar 3 Disclosures, reproduced in its "
    "own row order, its own labels and its own printed precision. Each year is taken from the edition in which it "
    "is the reporting year, except FY2021 as explained below:\n"
    f"FY2023: Pillar 3 Disclosures for the year ended 31 December 2023, 'Key Metrics table' p.3 (column "
    f"'31-Dec-23') - {P3_2023_WAYBACK} (Wayback `id_` snapshot; the Company's own URL {P3_2023_DEAD} returns HTTP "
    f"404 - re-checked 2026-09-16)\n"
    f"FY2022: Pillar 3 Disclosures for the year ended 31 December 2022, 'Key Metrics table' p.3 (column "
    f"'31-Dec-22') - {P3_2022} (still live; re-fetched 2026-09-16, HTTP 200, Content-Type application/pdf, "
    f"314,344 bytes, begins %PDF)\n"
    f"FY2021: the '31-Dec-21' comparative column of the FY2022 edition above. This is a deliberate departure from "
    f"this project's use-each-year's-own-edition rule, and the reason is positive rather than convenient: the "
    f"FY2021 edition EXISTS and was re-read in full for this ticket ({P3_2021_WAYBACK}, HTTP 200, "
    f"application/pdf, 319,857 bytes, 20pp), and it contains no Key Metrics table at all - its contents page runs "
    f"Overview / Governance / Risk Management Policies / Capital Resources and Business Strategy / Capital "
    f"Adequacy / Principal Risks, with no key-metrics entry, and the strings 'KM1' and 'Key Metrics' appear "
    f"nowhere in it. The FY2022 edition's comparative column is therefore the only published source for FY2021.\n"
    "FY2024, FY2025, and FY2016-FY2020: blank. See the detailed publication evidence in the Pillar 3 source note "
    "on the metric sheets - in summary, the Company published a Pillar 3 disclosure for five consecutive years "
    "(FY2019-FY2023) and then stopped after taking the SDDT exemption, and the FY2019, FY2020 and FY2021 editions "
    "carry no Key Metrics table.\n\n"
    "WHAT MAKES THIS A KM1, AND HOW IT WAS ESTABLISHED:\n"
    "• IT IS UNNUMBERED. The Company prints no row numbers at all - no '1', no 'UK 7a'. That does not matter: what "
    "makes a table the template is its ROW SET, not its numbering, and this one carries the full UK KM1 row set - "
    "available own funds, risk-weighted exposure amounts, capital ratios, C-SREP additional own funds "
    "requirements, combined buffer requirement, leverage ratio, the five-row LCR block and the three-row NSFR "
    "block. It is the same pattern as Europe Arab Bank's unnumbered template, not the same as a short bespoke "
    "summary table.\n"
    "• IT IS NEVER CALLED 'KM1'. The heading is '1.1 Key Metrics table'; the token 'KM1' appears nowhere in any "
    "edition. No presence test that keys on the token or on row numbering would have found it.\n"
    "• ROWS THE STANDARD TEMPLATE DOES NOT HAVE, kept as published: 'Systemic risk buffer (%)' sits inside the "
    "combined buffer block (zero in every year), and the additional-own-funds block is captioned against the PRA's "
    "C-SREP rather than the generic SREP.\n"
    "• THE ABSENCE OF THE TABLE IN THE FY2019-FY2021 EDITIONS WAS TESTED AGAINST IMAGES AS WELL AS TEXT, because a "
    "KM1 can be published as a bitmap inside an otherwise text-native PDF and then extract as nothing. "
    "`pdfimages -list` on the FY2019, FY2020, FY2021 and FY2022 editions returns exactly ONE image each - the "
    "286x165 RGB corporate logo, the same object in every edition - and the FY2023 edition two (that logo plus a "
    "391x200 graphic on p.19). There is no bitmap anywhere in these documents large enough or placed where a "
    "concealed key-metrics table could sit. The zero hit-counts for 'KM1' and 'Key Metrics' in the FY2019-FY2021 "
    "editions are also a fact about the documents rather than about the extraction: the same text yields 86-88 "
    "hits for 'capital', 48-49 for 'ratio', 3 for 'Tier 1' and 3 for 'leverage' in each.\n\n"
    "SOURCE DEFECTS, REPRODUCED RATHER THAN CORRECTED:\n"
    "• THE COMBINED-BUFFER SECTION HEADING IS TRUNCATED in both editions. It reads 'Combined buffer requirement "
    "(as a percentage of risk-weighted exposure' - the word 'amount' is missing, in both the FY2022 and the FY2023 "
    "document. Kept as printed, with the omission flagged in square brackets.\n"
    "• THE LCR BLOCK'S HQLA ROW IS CAPTIONED '(Weighted value - average)' BUT THE FIGURES ARE YEAR-END "
    "POINT-IN-TIME VALUES. This is demonstrable from the same documents: the KM1's 970% for FY2023 reproduces the "
    "31-Dec-23 column of that document's own quarterly table exactly, while the average it states separately for "
    "the same year is 835% (FY2022: KM1 833% = the 31-Dec-22 column; stated average 827%). The caption is left "
    "exactly as published rather than corrected, and both bases are carried on separate rows of the LCR and NSFR "
    "metric sheets, which is why those sheets and this one can show different numbers for the same year without "
    "either being wrong.\n"
    "• THE 18.27% EXPLANATORY NOTE MOVES. 'Note: although there are no C-SREP additional own funds requirements, "
    "the Company is required to hold 18.27% of risk-weighted exposures or EUR 5 million (the regulatory base "
    "capital requirement), whichever is the greater' is printed ABOVE the table in the FY2023 edition and BELOW it "
    "in the FY2022 edition.\n"
    "• PRECISION. The leverage ratio reads 35.35% here for FY2023, from the Key Metrics table itself; the Leverage "
    "Ratio metric sheet carries 35.4% for the same year from the same document's narrative. Both are the "
    "Company's own printed figures at its own two precisions, and neither has been adjusted to match the other.\n\n"
    "LATEST-EDITION CHECK, 2026-09-16. The Company's own live 'Financial information' page "
    "(https://www.mcafundingforchurches.co.uk/about-us/financial-information/) was fetched directly - HTTP 200, "
    "27KB, no block and no interstitial - and lists exactly two documents plus an FSCS leaflet: the Annual Report "
    "2025 (/media/4bcl2vk5/mca-ar-2025.pdf, already cited by this workbook) and a country-by-country reporting "
    "2025 PDF. NO PILLAR 3 DOCUMENT OF ANY VINTAGE. The Annual Report 2025 was re-downloaded the same day (HTTP "
    "200, application/pdf, %PDF, 1.06MB) and covers the 9 months ended 30 September 2025, which is the period this "
    "workbook already holds as FY2025; the string 'Pillar 3' does not occur in it. Nothing newer than FY2025 "
    "exists, and no Pillar 3 edition later than FY2023 exists.\n\n"
    + p3_sources()
)

bw.add_km1_sheet(
    title="Methodist Chapel Aid Limited — KM1 Key Metrics",
    subtitle="The Company's own 'Key Metrics table' (section 1.1 of its Pillar 3 Disclosures), reproduced whole in "
             "its own row order, labels and printed precision. It is the UK KM1 template but the Company prints no "
             "row numbers and never uses the token 'KM1'. Amounts in £'000, ratios as printed. Only the FY2022 and "
             "FY2023 editions contain the table; FY2021 is the FY2022 edition's comparative column, because the "
             "FY2021 edition exists and carries no such table. The FY2025 and FY2024 columns stay visible and now "
             "carry an explicit stated negative on their own status row rather than sitting blank: the Company holds "
             "a PRA SDDT Rule 3.1 modification effective 11 April 2024 with no end date, which precedes both the "
             "30 September 2025 and 31 December 2024 reporting dates, so no KM1 exists for either year and none "
             "will - see the source note.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=80,
    source_height=520,
)


metric("CET1 Capital", "£'000", "CET1 capital", {"FY2023": 13354, "FY2022": 12952, "FY2021": 13919, "FY2020": 13032, "FY2019": 12307}, "FY2024 and FY2025 now STATE the non-publication in the cell rather than sitting empty (2026-09-18): the Company holds a PRA SDDT Rule 3.1 modification effective 11/04/2024 with no end date, which removed its Pillar 3 duty before both reporting dates (31 December 2024 and 30 September 2025), so no edition exists for either year and neither Annual Report discloses an outturn capital amount. FY2016-FY2018: no Pillar 3 document has been reached - UNPROVEN, not established as unpublished (see Sources).")
metric("CET1 Ratio", "%", "CET1 ratio", {"FY2023": "52.88%", "FY2022": "53.85%", "FY2021": "52.79%", "FY2020": "51.48%", "FY2019": "58.68%"}, "FY2024 and FY2025 now STATE the non-publication in the cell rather than sitting empty (2026-09-18): the Company holds a PRA SDDT Rule 3.1 modification effective 11/04/2024 with no end date, which removed its Pillar 3 duty before both reporting dates (31 December 2024 and 30 September 2025), so no edition exists for either year and neither Annual Report discloses an outturn ratio. FY2020/FY2019 ratios are calculated as disclosed CET1 capital divided by this workbook's derived Total RWAs (not stated as a ready-made ratio in the source, which only gives the £ components). FY2016-FY2018: no Pillar 3 document has been reached - UNPROVEN, not established as unpublished (see Sources).")
metric("Tier 1 Capital", "£'000", "Tier 1 capital", {"FY2023": 13354, "FY2022": 12952, "FY2021": 13919, "FY2020": 13032, "FY2019": 12307}, "All disclosed Tier 1 capital was CET1. FY2024 and FY2025 now STATE the non-publication in the cell rather than sitting empty (2026-09-18): SDDT Rule 3.1 modification effective 11/04/2024, no end date, preceding both reporting dates. FY2016-FY2018: no Pillar 3 document has been reached - UNPROVEN, not established as unpublished (see Sources).")
metric("Tier 1 Ratio", "%", "Tier 1 ratio", {"FY2023": "52.88%", "FY2022": "53.85%", "FY2021": "52.79%", "FY2020": "51.48%", "FY2019": "58.68%"}, "FY2024 and FY2025 now STATE the non-publication in the cell rather than sitting empty (2026-09-18): the Company holds a PRA SDDT Rule 3.1 modification effective 11/04/2024 with no end date, which removed its Pillar 3 duty before both reporting dates (31 December 2024 and 30 September 2025), so no edition exists for either year and neither Annual Report discloses an outturn ratio. FY2016-FY2018: no Pillar 3 document has been reached - UNPROVEN, not established as unpublished (see Sources).")
metric("Total Capital", "£'000", "Total capital", {"FY2023": 13354, "FY2022": 12952, "FY2021": 13919, "FY2020": 13032, "FY2019": 12307}, "All disclosed total capital was CET1. FY2024 and FY2025 now STATE the non-publication in the cell rather than sitting empty (2026-09-18): SDDT Rule 3.1 modification effective 11/04/2024, no end date, preceding both reporting dates. FY2016-FY2018: no Pillar 3 document has been reached - UNPROVEN, not established as unpublished (see Sources).")
metric("Total Capital Ratio", "%", "Total capital ratio", {"FY2023": "52.88%", "FY2022": "53.85%", "FY2021": "52.79%", "FY2020": "51.48%", "FY2019": "58.68%"}, "FY2024 and FY2025 now STATE the non-publication in the cell rather than sitting empty (2026-09-18): the Company holds a PRA SDDT Rule 3.1 modification effective 11/04/2024 with no end date, which removed its Pillar 3 duty before both reporting dates (31 December 2024 and 30 September 2025), so no edition exists for either year and neither Annual Report discloses an outturn ratio. FY2016-FY2018: no Pillar 3 document has been reached - UNPROVEN, not established as unpublished (see Sources).")
metric("Total RWAs", "£'000", "Total risk-weighted exposure amount", {"FY2023": 25253, "FY2022": 24052, "FY2021": 26369, "FY2020": 25316, "FY2019": 20975}, "FY2024 and FY2025 now STATE the non-publication in the cell rather than sitting empty (2026-09-18): SDDT Rule 3.1 modification effective 11/04/2024, no end date, preceding both reporting dates (31 December 2024 and 30 September 2025). Nothing is back-solved from the 17.72% Total Capital Requirement the Annual Reports do print - that is a requirement set for the Company, not an outturn. FY2020/FY2019 Total RWAs are the sum of the disclosed credit risk RWA plus an operational risk RWA derived as capital requirement x 12.5 (the document's own Pillar 1 formula) since operational risk is disclosed there only as a capital requirement. FY2016-FY2018: no Pillar 3 document has been reached - UNPROVEN, not established as unpublished (see Sources).")

rwa_breakdown_rows = [
    ("DATA", "Pillar 3 edition status for this year (see source note)", MCA_P3_STATUS),
    ("SECTION", "Credit risk exposure by class (Risk Weighted Exposure)", {}),
    ("DATA", "Credit institutions", {"FY2023": 1825, "FY2022": 2713, "FY2021": 3233, "FY2020": 3255, "FY2019": 2835}),
    ("DATA", "UK Treasury Stocks", {"FY2023": 0, "FY2022": 0, "FY2021": 0, "FY2020": 0, "FY2019": 0}),
    ("DATA", "Multilateral Development Banks", {"FY2019": 0}),
    ("DATA", "Sterling Corporate Bonds", {"FY2019": 961}),
    ("DATA", "Collective investment undertakings", {"FY2023": 3271, "FY2022": 3092, "FY2021": 3449, "FY2020": 4097, "FY2019": 1607}),
    ("DATA", "Equity investments", {"FY2023": 7101, "FY2022": 7160, "FY2021": 9123, "FY2020": 8138, "FY2019": 7678}),
    ("DATA", "Loans and advances to customers (drawn) (aggregate, pre-FY2022 disclosure form)", {"FY2021": 7197, "FY2020": 7315, "FY2019": 5916}),
    ("DATA", "Loans and advances to customers (50% of undrawn) (aggregate, pre-FY2022 disclosure form)", {"FY2021": 2066, "FY2020": 1440, "FY2019": 857}),
    ("DATA", "Higher Risk Weighted Equities", {"FY2022": 30}),
    ("DATA", "Property loans and advances to customers (drawn)", {"FY2023": 10320, "FY2022": 8470}),
    ("DATA", "Property loans and advances to customers (50% of undrawn)", {"FY2023": 1125, "FY2022": 1195}),
    ("DATA", "Car loans and advances to customers", {"FY2023": 7, "FY2022": 12}),
    ("DATA", "Fixed and other assets", {"FY2023": 436, "FY2022": 145, "FY2021": 103, "FY2020": 83, "FY2019": 133}),
    ("TOTAL", "Total credit risk exposure (RWA)", {"FY2023": 24085, "FY2022": 22817, "FY2021": 25171, "FY2020": 24328, "FY2019": 19987}),
    ("DATA", "Operational risk capital requirement (RWA)", {"FY2023": 1168, "FY2022": 1235, "FY2021": 1150, "FY2020": 988, "FY2019": 988}),
    ("TOTAL", "Total RWAs (Pillar 1)", {"FY2023": 25253, "FY2022": 24052, "FY2021": 26369, "FY2020": 25316, "FY2019": 20975}),
]
bw.add_rwa_breakdown_sheet(
    "Methodist Chapel Aid Limited — RWA Breakdown",
    "Entity-level basis, £'000, Standardised Approach. The FY2025 and FY2024 columns stay visible and carry an "
    "explicit stated negative on the status row rather than sitting blank: the Company holds a PRA SDDT Rule 3.1 "
    "modification effective 11 April 2024 with no end date, preceding both reporting dates, so no Pillar 3 "
    "edition - and therefore no RWA breakdown - exists for either year.",
    rwa_breakdown_rows,
    RWA_BREAKDOWN_SOURCES,
    first_col_width=58,
    source_height=230,
)

metric("Leverage Ratio", "%", "Leverage ratio", {"FY2023": "35.4%", "FY2022": "33.49%", "FY2021": "33.05%", "FY2020": "~30%", "FY2019": "~30%"}, "The Company states that the smaller-bank leverage requirement does not apply; reported ratios are included as disclosed. FY2024 and FY2025 now STATE the non-publication in the cell rather than sitting empty (2026-09-18): SDDT Rule 3.1 modification effective 11/04/2024, no end date, preceding both reporting dates. FY2020/FY2019 are transcribed as disclosed - the narrative Pillar 3 documents for these years state only 'approximately 30%', not an exact figure (the FY2021 standalone Pillar 3 document uses the same approximate wording, but a more precise 33.05% is used for FY2021 above, sourced from the newer FY2022 Pillar 3 document's comparative column). FY2016-FY2018: no Pillar 3 document has been reached - UNPROVEN, not established as unpublished (see Sources).")
# GA-020 (2026-09-19): outcome wording for the statement cells below.
GA020_LCR = {y: ("Not published – the " + y + " Pillar 3 (re-read 2026-09-18) states only a policy of LCR "
                 ">= 200%, no measured LCR") for y in ("FY2020", "FY2019")}
GA020_NSFR = {y: "Not applicable – no UK NSFR requirement before 1 Jan 2022 (PRA PS17/21, PS22/21)"
              for y in ("FY2018", "FY2017", "FY2016")}
GA020_NSFR.update({y: ("Not applicable – no UK NSFR requirement before 1 Jan 2022 (PRA PS17/21, PS22/21); the "
                       + y + " Pillar 3 has no NSFR section") for y in ("FY2020", "FY2019")})
GA020_MREL = {}
for _y in ("FY2025", "FY2024"):
    GA020_MREL[_y] = ("Not published – no Pillar 3 after the SDDT Rule 3.1 opt-in of 11 Apr 2024 (PRA waivers "
                      "register); zero 'MREL' in AR2024/AR2025, searched 2026-09-19")
for _y in ("FY2023", "FY2022", "FY2021", "FY2020", "FY2019"):
    GA020_MREL[_y] = ("Not published – zero 'MREL' in the " + _y + " Pillar 3 edition (full text searched "
                      "2026-09-19)")
# GA-020 unreached pass (2026-09-19), second attempt, still UNREACHED. A web search
# returns an index entry for .../sitefiles/resources/pdf/pillar3disclosures2016.pdf
# (titled only "Home"), so a file of that name probably existed. Tried: that URL and
# the 2017/2018 equivalents live (404; the site has since moved to /media/<id>/ paths,
# so even the cited FY2023 /media/ URL now 404s - the live probes are no control);
# Wayback CDX for each exact URL on both hosts (no capture) and for the whole domain
# before 2020 (no document at all); archive.ph/newest for each (404, control OK);
# CDX of candidate former domains (methodistchapelaid.org/.org.uk/.co.uk: none;
# mca-ltd.co.uk and mcafundingforchurches.com: unrelated/empty).
for _y in ("FY2018", "FY2017", "FY2016"):
    GA020_MREL[_y] = ("Unreached today – no " + _y + " Pillar 3 reached: live paths 404, no Wayback/archive.ph "
                      "capture (exact URLs + domain pre-2020), web search (2026-09-19); CH accounts OCR'd: no MREL")

metric_rows(
    "LCR", "%",
    [
        ("Average liquidity coverage ratio (12-month average of quarterly end-of-month positions)",
         {"FY2023": "835%", "FY2022": "827%"}),
        ("Liquidity coverage ratio at year-end (point-in-time, per UK KM1)",
         dict(MCA_P3_STATUS,
              **{"FY2023": "970%", "FY2022": "833%", "FY2021": "603%",
                 "FY2020": GA020_LCR["FY2020"], "FY2019": GA020_LCR["FY2019"]})),
    ],
    LIQUIDITY_BASIS_NOTE
    + "\n\nFY2022's average of 827% is newly added here (2026-09-15) from the FY2022 Pillar 3 document's own "
      "narrative - 'The Company's average LCR for the financial year to 31 December 2022 ... was 827%' - which "
      "had not previously been transcribed; the 833% that the old single row carried for FY2022 was that "
      "document's KM1 year-end figure and is retained, correctly labelled, on the year-end row. FY2023's "
      "year-end 970% is likewise newly added from the FY2023 KM1.\n"
      "FY2019-FY2021 have no average: the standalone Pillar 3 documents for those years state only a policy "
      "of maintaining LCR at or above 200% and disclose no actual measured ratio, and a policy floor is not "
      "an outturn, so nothing is transcribed from them. RE-VERIFIED AGAINST THE DOCUMENTS 2026-09-18: the "
      "FY2019, FY2020 and FY2021 editions were re-downloaded and read, and each carries exactly one LCR "
      "passage, in its liquidity Risk Appetite section - 'b) Liquidity coverage ratio (LCR) ... The Company's "
      "policy is to maintain a LCR of at least 200% at all times, i.e. double the regulatory minimum' - and "
      "no measured figure anywhere. The reading is a fact about those documents and not about the "
      "extraction: the same text yields 86-88 hits for 'capital', 48-49 for 'ratio' and 22 for 'liquid' in "
      "each edition, while 'Net Stable Funding', 'NSFR', 'Key Metrics' and 'KM1' return zero in all three.\n"
      "WHY FY2020 AND FY2019 READ 'Not disclosed' HERE WHILE THE NSFR SHEET READS 'Not applicable' FOR THE "
      "SAME YEARS (made consistent with the evidence 2026-09-18). The two sheets are answering different "
      "questions and the difference is real, not an oversight. The NSFR did not exist as a UK requirement "
      "before 1 January 2022, so there was no ratio for the Company to compute - a structural "
      "non-applicability. The LCR did exist and did bind: it has applied since Commission Delegated "
      "Regulation (EU) 2015/61 took effect on 1 October 2015, at a 100% minimum from 1 January 2018, and was "
      "retained in UK law. So for FY2019 and FY2020 the metric applied, the Company published a Pillar 3 "
      "document, and that document simply did not state the outturn. That is a disclosure gap the Company "
      "owns, not an inapplicable metric, and 'Not applicable' would misdescribe it. FY2021 needs no such "
      "record because a figure was in fact published for it, as the FY2022 edition's comparative.\n"
      "FY2021's year-end value comes from the FY2022 "
      "edition's KM1 comparative column. FY2016-FY2018: no Pillar 3 document has been reached (unproven - see "
      "Sources). FY2024 and FY2025 now CARRY THE STATEMENT IN THE CELL rather than sitting empty (changed "
      "2026-09-18): the Company is exempt from publishing Pillar 3 disclosures (SDDT, PRA Rule 3.1, effective "
      "11 April 2024, no end date), and both reporting dates - 31 December 2024 and 30 September 2025 - fall "
      "after it, so no edition exists for either year. An empty cell was indistinguishable from a year nobody "
      "had searched. See the Sources note.",
)
metric_rows(
    "NSFR", "%",
    [
        ("Average net stable funding ratio (12-month average of quarterly end-of-month positions)",
         {"FY2023": "182%", "FY2022": "194%"}),
        ("Net stable funding ratio at year-end (point-in-time, per UK KM1)",
         dict(MCA_P3_STATUS,
              **{"FY2023": "174%", "FY2022": "192%", "FY2021": "184%",
                 **GA020_NSFR})),
    ],
    LIQUIDITY_BASIS_NOTE
    + "\n\nFY2022's average of 194% is newly added here (2026-09-15) from the FY2022 Pillar 3 document's own "
      "narrative - 'The Company's average NSFR for the financial year to 31 December 2022 ... was 194%' - "
      "which had not previously been transcribed; the 192% that the old single row carried for FY2022 was "
      "that document's KM1 year-end figure and is retained, correctly labelled, on the year-end row. "
      "FY2023's year-end 174% is likewise newly added from the FY2023 KM1.\n"
      "FY2016-FY2020 are marked 'Not applicable' rather than left blank (changed 2026-09-15). These are "
      "STRUCTURAL blanks: the UK had no NSFR requirement and no NSFR disclosure template before 1 January "
      "2022 (PRA PS17/21 / PS22/21, 'Implementation of Basel standards'), so there was no ratio for the "
      "Company to compute or publish in those years - consistent with the FY2019 and FY2020 Pillar 3 "
      "documents, which exist but contain no NSFR section at all, and with FY2016-FY2018, for which no "
      "Pillar 3 document exists. An empty cell would be indistinguishable from an unresearched gap and "
      "would be re-chased indefinitely; these five will never yield a figure.\n"
      "FY2021 is deliberately NOT marked 'Not applicable' even though it also predates the requirement, "
      "because a figure was in fact published for it - as the comparative column of the FY2022 edition's "
      "KM1 - and a disclosed figure always outranks the structural argument.\n"
      "FY2024 and FY2025 are deliberately NOT marked 'Not applicable', because the metric did apply in both "
      "periods; what was removed is the DUTY TO PUBLISH, by the SDDT Rule 3.1 modification effective 11 April "
      "2024 (no end date), which precedes both the 31 December 2024 and the 30 September 2025 reporting dates. "
      "Changed 2026-09-18: those two cells previously sat empty and now state that non-publication explicitly, "
      "because an empty cell is indistinguishable from a year nobody searched. The distinction from the "
      "FY2016-FY2020 'Not applicable' cells is preserved - those years had no NSFR requirement at all.",
)
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources(),
    per_note={"MREL Ratio": "No MREL ratio was disclosed in the located Methodist Chapel Aid Pillar 3 documents. "
              "GA-020 RE-CHECK 2026-09-19: zero 'MREL', 'loss-absorbing', 'eligible liabilities' or "
              "'resolution' in the FY2019-FY2023 Pillar 3 editions and the text-native Annual Reports 2022, 2024 "
              "and 2025, against 57-84 hits for 'capital' in each; the image-only Companies House accounts for "
              "FY2016 and FY2018 (the latter carrying FY2017 comparatives) were OCR'd and also return zero. "
              "FY2016-FY2018 nonetheless read 'Unreached today', because no Pillar 3 edition for those years has "
              "been reached (see PRE2019_STATUS) and an MREL statement, if any, would live there."},
    statements={"MREL Ratio": GA020_MREL},
)

bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash generated/(used) from operating activities", {"FY2025": 230314, "FY2024": 429322, "FY2023": -3050504, "FY2022": -2346030, "FY2021": 714322, "FY2020": 2973715, "FY2019": -70421, "FY2018": -303376, "FY2017": -974245, "FY2016": 161846}),
        ("Net cash generated/(used) from investing activities", {"FY2025": -249591, "FY2024": 661933, "FY2023": -364592, "FY2022": -261027, "FY2021": 519122, "FY2020": -892604, "FY2019": 4062, "FY2018": 178019, "FY2017": 327744, "FY2016": 171836}),
        ("Net cash generated/(used) in financing activities", {"FY2025": -1353, "FY2024": -1317, "FY2023": -1233, "FY2022": -1113, "FY2021": -1068, "FY2020": -1058, "FY2019": -1041, "FY2018": -1018, "FY2017": -979, "FY2016": -967}),
        ("Cash and cash equivalents at end of year/period", {"FY2025": 10166442, "FY2024": 10187072, "FY2023": 9097134, "FY2022": 12513463, "FY2021": 15121633, "FY2020": 13889257, "FY2019": 11809204, "FY2018": 11876604, "FY2017": 12002979, "FY2016": 12650459}),
    ],
    cash_flow_unit="£",
    ratios=[
        ("CET1 Ratio", {"FY2023": "52.88%", "FY2022": "53.85%", "FY2021": "52.79%", "FY2020": "51.48%", "FY2019": "58.68%"}),
        ("Total Capital Ratio", {"FY2023": "52.88%", "FY2022": "53.85%", "FY2021": "52.79%", "FY2020": "51.48%", "FY2019": "58.68%"}),
        ("Leverage Ratio", {"FY2023": "35.4%", "FY2022": "33.49%", "FY2021": "33.05%", "FY2020": "~30%", "FY2019": "~30%"}),
        ("LCR (12-month average of quarterly end-of-month positions)", {"FY2023": "835%", "FY2022": "827%"}),
        ("LCR at year-end (point-in-time, per UK KM1)",
         {"FY2023": "970%", "FY2022": "833%", "FY2021": "603%",
          "FY2020": GA020_LCR["FY2020"], "FY2019": GA020_LCR["FY2019"]}),
        ("NSFR (12-month average of quarterly end-of-month positions)", {"FY2023": "182%", "FY2022": "194%"}),
        ("NSFR at year-end (point-in-time, per UK KM1)",
         {"FY2023": "174%", "FY2022": "192%", "FY2021": "184%",
          "FY2020": "Not applicable", "FY2019": "Not applicable", "FY2018": "Not applicable",
          "FY2017": "Not applicable", "FY2016": "Not applicable"}),
    ],
    note="CORRECTED 2026-09-15. This sheet previously showed ONE LCR row reading 835% / 833% / 603% for "
         "FY2023 / FY2022 / FY2021, which silently mixed two different series: 835% is the FY2023 "
         "12-month average, while 833% and 603% are year-end point-in-time figures from the UK KM1 tables. "
         "The FY2022 average (827%) and the FY2023 year-end value (970%) had never been transcribed at all, "
         "so the row read as a flat trend when the two real series in fact move differently. Both series are "
         "now shown in full on separate labelled rows, for NSFR as well as LCR, and an NSFR row has been "
         "added here for the first time. NSFR FY2016-FY2020 read 'Not applicable' because the UK had no "
         "NSFR requirement before 1 January 2022 (PRA PS17/21). See the LCR and NSFR sheets for the full "
         "basis note, including the caption error in the source's own KM1 tables.\n\n"
         + ENTITY,
    balance_sheet_totals=[
        ("Total Assets", {"FY2025": 35956037, "FY2024": 36147101, "FY2023": 36293524, "FY2022": 37194488, "FY2021": 40154805, "FY2020": 38940466, "FY2019": 36369860, "FY2018": 33535815, "FY2017": 33576835, "FY2016": 32972669}),
        ("Loans and advances to customers", {"FY2025": 8262627, "FY2024": 9138711, "FY2023": 10330064, "FY2022": 8485497, "FY2021": 7197340, "FY2020": 7314586, "FY2019": 7888087, "FY2018": 6315264, "FY2017": 5210921, "FY2016": 4295209}),
        ("Customer accounts", {"FY2025": 21227564, "FY2024": 22043458, "FY2023": 22687021, "FY2022": 24113288, "FY2021": 25374073, "FY2020": 25034413, "FY2019": 23169408, "FY2018": 21897604, "FY2017": 21344785, "FY2016": 21572515}),
        ("Total equity", {"FY2025": 14117086, "FY2024": 13747327, "FY2023": 13353632, "FY2022": 12952019, "FY2021": 14176202, "FY2020": 13442989, "FY2019": 12867446, "FY2018": 11568761, "FY2017": 11998446, "FY2016": 11071512}),
    ],
    balance_sheet_unit="£",
    income_statement_totals=[
        ("Total operating expense", {"FY2025": -481964, "FY2024": -570759, "FY2023": -551258, "FY2022": -455467, "FY2021": -361324, "FY2020": -371250, "FY2019": -378013, "FY2018": -370280, "FY2017": -361235, "FY2016": -355663}),
        ("Surplus/(deficit) before taxation", {"FY2025": 418967, "FY2024": 489534, "FY2023": 478770, "FY2022": -1718227, "FY2021": 977572, "FY2020": 702221, "FY2019": 1559263, "FY2018": -572535, "FY2017": 880487, "FY2016": 804283}),
        ("Surplus/(deficit) for the period/year", {"FY2025": 371112, "FY2024": 395012, "FY2023": 402846, "FY2022": -1223070, "FY2021": 734281, "FY2020": 576601, "FY2019": 1299726, "FY2018": -428667, "FY2017": 927913, "FY2016": 757654}),
    ],
    income_statement_unit="£",
    equity_changes_totals=[
        ("Surplus/(deficit) for the period/year", {"FY2025": 371112, "FY2024": 395012, "FY2023": 402846, "FY2022": -1223070, "FY2021": 734281, "FY2020": 576601, "FY2019": 1299726, "FY2018": -428667, "FY2017": 927913, "FY2016": 757654}),
        ("Dividends paid and payable", {"FY2025": -1353, "FY2024": -1317, "FY2023": -1233, "FY2022": -1113, "FY2021": -1068, "FY2020": -1058, "FY2019": -1041, "FY2018": -1018, "FY2017": -979, "FY2016": -967}),
        ("Closing equity", {"FY2025": 14117086, "FY2024": 13747327, "FY2023": 13353632, "FY2022": 12952019, "FY2021": 14176202, "FY2020": 13442989, "FY2019": 12867446, "FY2018": 11568761, "FY2017": 11998446, "FY2016": 11071512}),
    ],
    equity_changes_unit="£",
)

bw.save("/Users/armaan/code/katalysis/banks/METHODIST CHAPEL AID FINANCIALS.xlsx")
print("Saved.")
