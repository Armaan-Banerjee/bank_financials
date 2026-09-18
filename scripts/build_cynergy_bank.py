import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021",
         "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014", "FY2013"]  # most recent first
# HD-072: FY2013 added for the four statutory-statement sheets only (Balance Sheet, Profit & Loss,
# Statement of Changes in Equity, Cash Flow Statement) - Pillar 3, Asset Quality and RWA Breakdown
# dicts below intentionally have no FY2013 entries (out of scope for this ticket, per the map's
# hard FY2014 cap for those sheet types). Y_CORE is that FY2014 floor, passed to BankWorkbook() so
# Pillar 3/Asset Quality/RWA Breakdown/Overview default to it; the three statutory sheets below pass
# years=YEARS explicitly to get the extended column set.
Y_CORE = [y for y in YEARS if y != "FY2013"]
YEAR_LABEL = {y: y for y in YEARS}

# Site (Contentful CDN) hosts text-native copies of the last 3 Annual Reports;
# FY2022/FY2021 only exist as scanned Companies House filings.
AR2025_URL = "https://assets.ctfassets.net/xzmqg68ot16t/1aUkuB7BcAd8Pj5Kq0RNqh/101ced4af6be2d55cd37fad3542829b2/Cynergy_Bank_-_Annual_Report_2025.pdf"
AR2024_URL = "https://assets.ctfassets.net/xzmqg68ot16t/2AeSbXsBP7fwKhngGTLWxb/ca86e60128ab83d41842b85ae74aa326/Annual_Report_2024.pdf"
AR2023_URL = "https://assets.ctfassets.net/xzmqg68ot16t/2oPLoaeUJ2c4kRJcNMSyMp/54230fc39821a0d6ede6f81f1c7528ce/Cynergy_Bank_Limited_-_Annual_Report_2023.pdf"
AR2022_CH_URL = "https://find-and-update.company-information.service.gov.uk/company/04728421/filing-history/MzM3OTM0NzA5MmFkaXF6a2N4/document?format=pdf&download=0"

# HD-051 (historical-depth batch 7) additions: FY2014-FY2020, all sourced from Companies House's
# scanned filing history for company 04728421 (the entity now called Cynergy Bank Plc traded as
# Bank of Cyprus UK Limited FY2014-2017, then Cynergy Bank Limited from the 2018 rebrand). Every
# filing below was independently downloaded and re-verified from Companies House during this batch
# (OCR'd where scanned, cross-checked visually against the original page image for any page where
# OCR text came out unreliable) -- none of these were assumed present from a prior scan.
CH_DOC_URL = "https://find-and-update.company-information.service.gov.uk/company/04728421/filing-history/{}/document?format=pdf&download=0"
AR2020_CH_URL = CH_DOC_URL.format("MzMwMTMwNjM2MWFkaXF6a2N4")  # filed 19 May 2021
AR2019_CH_URL = CH_DOC_URL.format("MzI2ODIzMzE4NmFkaXF6a2N4")  # filed 30 Jun 2020
AR2018_CH_URL = CH_DOC_URL.format("MzI0NTUxMzA1N2FkaXF6a2N4")  # filed 02 Oct 2019
AR2017_CH_URL = CH_DOC_URL.format("MzIwNjAyOTg3MmFkaXF6a2N4")  # filed 29 May 2018 (Bank of Cyprus UK Limited)
AR2016_CH_URL = CH_DOC_URL.format("MzE4MTU5MjQyMmFkaXF6a2N4")  # filed 28 Jul 2017
AR2015_CH_URL = CH_DOC_URL.format("MzE0NDMzNzcwNGFkaXF6a2N4")  # filed 22 Mar 2016
AR2014_CH_URL = CH_DOC_URL.format("MzEyMTQ1OTQ5MGFkaXF6a2N4")  # filed (Bank of Cyprus UK Limited)

# HD-072 addition: FY2013, real statutory floor per HD-002's deep dive. Independently re-downloaded and
# read in full from Companies House (not assumed from a prior scan) - Bank of Cyprus UK Limited's own
# Annual Report 2013 (company converted from a Bank of Cyprus Public Company Limited UK branch to this
# subsidiary on 25 June 2012, so the FY2012 comparative column within this same document only covers a
# part-year 25 Jun-31 Dec 2012 and is NOT used here - only FY2013's own column is transcribed).
AR2013_CH_URL = CH_DOC_URL.format("MzA5OTE1OTY0MGFkaXF6a2N4")  # filed 30 Apr 2014

# Real standalone Pillar 3 disclosure documents for FY2018-FY2020, found via the Wayback Machine's
# CDX API (the "document library" landing pages that used to link them are gone from the live
# site, replaced with only the 3 most recent Annual Reports) then re-fetched from the current
# production domain, which still serves the underlying PDFs even though nothing links to them any
# more. This directly CONTRADICTS this script's own prior sourcing note (see p3_sources() below,
# and the ENTITY_NOTE) that no standalone Pillar 3 document could be found for Cynergy Bank --
# that finding was wrong for at least these 3 years, and very likely FY2021 too (out of scope for
# this batch; flagged separately for the wayfinder map, not corrected here).
P3_2018_URL = "https://www.cynergybank.co.uk/media/2534/pillar-3-disclosures-2018.pdf"
P3_2019_URL = "https://www.cynergybank.co.uk/media/ioueypnz/pillar-3-disclosures-2019.pdf"
P3_2020_URL = "https://www.cynergybank.co.uk/media/liqngpna/pillar-3-disclosures-2020.pdf"
P3_2021_URL = "https://www.cynergybank.co.uk/media/drcj252b/cynergy-bank-pillar-3-2021.pdf"
P3_2022_URL = "https://www.cynergybank.co.uk/media/bkhp10sd/cynergy-bank-2022-pillar-3-disclosures.pdf"
# Neither 2021 nor 2022 is linked from the live site any more; both are archived in full:
P3_2021_WAYBACK = "https://web.archive.org/web/20230808000642if_/" + P3_2021_URL
P3_2022_WAYBACK = "https://web.archive.org/web/20230807203320if_/" + P3_2022_URL

# FOUND 2026-09-15, overturning this script's own prior "unreachable" finding for FY2023 (see
# p3_sources()). The FY2023 Pillar 3 is live on the Contentful CDN behind the current site. It is
# linked ONLY from https://www.cynergybank.co.uk/strong-and-prudent-management -- NOT from
# /about-us/company-performance or /document-library, which is why four earlier search routes all
# missed it. That page's links are JavaScript-rendered, so a fetcher sees no href; curling the raw
# HTML and grepping for the CDN host exposes them:
#   curl -sL https://www.cynergybank.co.uk/strong-and-prudent-management \
#     | grep -o 'assets\.ctfassets\.net[^"'"'"' ]*' | sort -u
# That enumeration (run 2026-09-15) returns 15 assets in Contentful space xzmqg68ot16t, of which
# exactly SIX are Pillar 3 editions -- FY2018, FY2019, FY2020, FY2021, FY2022, FY2023 -- and the
# rest are Gender Pay Gap reports (2017-2026) plus an FSCS information sheet. See ENUMERATION_NOTE.
P3_2023_URL = ("https://assets.ctfassets.net/xzmqg68ot16t/5lTzyJuIg2zRrc7GGyH6Gv/"
               "6eb39217d6164e649f946b7aed50a0cb/Cynergy_Bank_Pillar_3_Disclosures_2023.pdf")
# Same page also re-serves the 2021 and 2022 editions on the CDN (different hash segment from the
# old cynergybank.co.uk/media/ URLs above, which is why permutation on the old paths never found
# them); both resolve, and both agree with the archived copies already used as sources below.
P3_2021_CDN_URL = ("https://assets.ctfassets.net/xzmqg68ot16t/2v6FmkY7vFJwKVYPsdkTkg/"
                   "2c74d882695a4854e99edf9a78ac6b00/cynergy-bank-pillar-3-2021.pdf")
P3_2022_CDN_URL = ("https://assets.ctfassets.net/xzmqg68ot16t/3qKJzsAiu3dGAA2EQBSzPo/"
                   "bbb85f662bef802d29fb7144d087c761/cynergy-bank-2022-pillar-3-disclosures.pdf")
P3_INDEX_URL = "https://www.cynergybank.co.uk/strong-and-prudent-management"

ENUMERATION_NOTE = (
    "FY2024/FY2025 Pillar 3 - ENUMERATED NEGATIVE (2026-09-15), not a failed search. The Bank's own "
    "Pillar 3 landing page (https://www.cynergybank.co.uk/strong-and-prudent-management) has "
    "JavaScript-rendered links; curling its raw HTML and grepping for the Contentful asset host "
    "enumerates every PDF the page can serve. The result is 15 assets, of which exactly six are "
    "Pillar 3 editions: FY2018, FY2019, FY2020, FY2021, FY2022 and FY2023. There is no FY2024 and no "
    "FY2025 edition. The absence is meaningful rather than merely unfound because the same page is "
    "demonstrably current - it carries a Gender Pay Gap report dated 2026 - and because it agrees "
    "with the Bank's own narrative reason for stopping (SDDT approval on 17 January 2025, quoted "
    "below from both Annual Reports)."
)

ENTITY_NOTE = (
    "Entity: Cynergy Bank Plc, company 04728421 (formerly Bank of Cyprus UK Limited / Bank of Cyprus "
    "Advances Limited before a 2018 rebrand/ownership change to a consortium led by Cynergy Capital Ltd) - "
    "same company number throughout, no entity-identity ambiguity. Consolidated basis throughout (the Bank "
    "plus subsidiaries Cynergy Business Finance Limited and, in earlier years, Cynergy Connect Technologies "
    "Ltd, which never traded and was dissolved during 2023).\n"
    "Each year's own originally-published figures are used (not later restated comparatives) - FY2025's own "
    "Annual Report explicitly restates its FY2024 comparative column (see its own footnote: 'Comparatives "
    "have been re-presented to conform with the current year's presentation... presentational only and have "
    "no impact on the reported cash and cash equivalents') and the FY2025 report's own Alternative "
    "Performance Measures note gives a full reconciliation of the reclassifications; FY2024's own column here "
    "uses FY2024's own Annual Report instead. Similarly FY2022's own Annual Report (Companies House, scanned) "
    "presents cash and cash equivalents movements without a separate 'effects of exchange rate' line "
    "(opening + net change ties to closing exactly on its own); a later report's FY2022 comparative adds a "
    "separate £760k FX line by reclassifying it out of the opening balance - FY2022's own original figures "
    "are used here, not that later restatement.\n"
    "FY2021 figures are the FY2021 comparative column within FY2022's own Annual Report (the FY2021 Annual "
    "Report itself is only available as a further scanned Companies House filing and was not independently "
    "re-checked) - this is the standard 'sourced from the following year's own comparative' pattern used "
    "elsewhere in this project when a year's own standalone report isn't the primary source.\n"
    "Line items vary in granularity across report vintages (e.g. 'purchase' and 'redemption' of asset-backed "
    "securities are reported as one combined net line in FY2022/FY2021's presentation but split into two "
    "lines from FY2023 onward) - blank cells indicate that year's report did not disclose that specific "
    "split; a combined figure appears on its own row where reported that way. Section TOTALs are consistent "
    "and comparable across all 5 years regardless of this granularity.\n\n"
    "HD-051 (historical depth to FY2014, capped project-wide): FY2014-FY2017 are Bank of Cyprus UK Limited "
    "(the same company, before the 2018 rebrand/ownership change) reporting on a COMPANY-ONLY (non-"
    "consolidated) basis - it had one dormant-ish subsidiary (Bank of Cyprus Financial Services Limited, an "
    "insurance-referral entity) that was never consolidated in these years. Consolidation of a trading "
    "subsidiary (Cynergy Business Finance Limited) begins only from FY2018 onward. This is a genuine basis "
    "change, not a data gap - FY2014-2017 figures are that year's own Company statements, not restated onto "
    "a consolidated basis. FY2014-2016 predate the CRD IV/Basel III 'CET1' terminology entirely - the Pillar "
    "3 sheets for these years use the Basel II/CRD III era term 'Core Tier 1', which is presented on the "
    "CET1 Capital sheet as the closest equivalent (see each Pillar 3 sheet's own note). "
    "A material, previously-unknown finding from this batch: Cynergy Bank DOES have real standalone Pillar 3 "
    "disclosure PDFs for FY2018, FY2019 and FY2020 (found via the Wayback Machine, since the current site's "
    "document-library page only links the 3 most recent Annual Reports) - see p3_sources() below, which "
    "corrects this script's own prior claim that no such document existed for any year."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Cynergy Bank Plc's own Consolidated statement of cash flows, £'000:\n"
    f"FY2025 (& FY2024 restated comparative, not used - see note): Cynergy Bank plc Annual Report & Accounts 2025, p.54 (Consolidated and company statement of cash flows) - {AR2025_URL}\n"
    f"FY2024 (own, & FY2023 comparative cross-checked): Cynergy Bank plc Annual Report & Accounts 2024, p.87-88 (Consolidated and company statement of cash flows) - {AR2024_URL}\n"
    f"FY2023 (own, & FY2022 comparative cross-checked): Cynergy Bank Limited Annual Report & Accounts 2023, p.93-94 (Consolidated and company statement of cash flows) - {AR2023_URL}\n"
    f"FY2022 (own) & FY2021 (comparative): Cynergy Bank Limited Annual Report & Accounts 2022 (Companies House filing, scanned), p.95-96 (Consolidated and Company statement of cash flows) - {AR2022_CH_URL}\n"
    f"FY2020 (own): Cynergy Bank Limited Annual Report & Accounts 2020 (Companies House filing, scanned), p.58-60 (Statement of cash flows) - {AR2020_CH_URL}\n"
    f"FY2019 (own): Cynergy Bank Limited Annual Report & Accounts 2019 (Companies House filing, scanned), p.53-54 (Statement of cash flows) - {AR2019_CH_URL}\n"
    f"FY2018 (own): Cynergy Bank Limited Annual Report & Accounts 2018 (Companies House filing, scanned), p.23 (Statement of cash flows, Company-only basis) - {AR2018_CH_URL}\n"
    f"FY2017 (own): Bank of Cyprus UK Limited Annual Report & Accounts 2017 (Companies House filing, scanned), p.22 (Statement of cash flows, Company-only basis) - {AR2017_CH_URL}\n"
    f"FY2016 (own): Bank of Cyprus UK Limited Annual Report & Accounts 2016 (Companies House filing, scanned), p.13 (Statement of cash flows, Company-only basis) - {AR2016_CH_URL}\n"
    f"FY2015 (own): Bank of Cyprus UK Limited Annual Report & Accounts 2015 (Companies House filing, scanned), p.12 (Statement of cash flows, Company-only basis) - {AR2015_CH_URL}\n"
    f"FY2014 (own): Bank of Cyprus UK Limited Annual Report & Accounts 2014 (Companies House filing, scanned), p.12 (Statement of cash flows, Company-only basis) - {AR2014_CH_URL}\n"
    f"FY2013 (own): Bank of Cyprus UK Limited Annual Report & Accounts 2013 (Companies House filing, scanned), p.13 (Statement of cash flows, Company-only basis) - {AR2013_CH_URL}\n"
    + ENTITY_NOTE
    + "\n\nHD-072 (statutory statements extended to FY2013): FY2013's own Statement of cash flows presents "
    "'Changes in operating assets and liabilities' as one flat, unsplit list (not the separate 'assets' / "
    "'liabilities' sub-sections used from FY2014 onward) - each FY2013 line has been placed on the row that "
    "matches its FY2014+ equivalent by content (e.g. 'Increase in customer deposits' -> 'Customer and bank "
    "deposits'). FY2013's own source document has a 1-unit rounding inconsistency between its own two "
    "statements of the year's net cash movement (£136,197k in the operating/investing/financing summary "
    "line vs an implied £136,198k in the Cash and cash equivalents reconciliation below it, which is what "
    "makes the reconciliation's own stated closing balance of £511,643k not tie exactly to opening £374,506k "
    "+ net movement £136,197k + FX £939k = £511,642k) - both figures are the source's own, not a "
    "transcription error here; the summary line's £136,197k is used for the 'Net (decrease)/increase in cash "
    "and cash equivalents for the year' row, and the reconciliation's own stated £511,643k is used for the "
    "closing balance row, exactly as each is printed."
)


def p3_sources():
    return (
        "Sources - Cynergy Bank Plc Consolidated (Company-only FY2014-2017, see note) basis:\n"
        f"FY2025: Cynergy Bank plc Annual Report & Accounts 2025, p.85 (Note 32, Capital management - 'Capital "
        f"resources' table, Consolidated column: Ordinary share capital 202,000 + Retained earnings 226,322 + "
        f"Property revaluation reserve nil - Regulatory deductions (unaudited) 79,716 = Total eligible tier 1 "
        f"capital (CET1) 348,606; plus Tier 2 subordinated loans 50,000 = Total eligible regulatory capital "
        f"398,606). The same table's FY2024 comparative column (321,877 / 15,000 / 336,877) agrees exactly with "
        f"FY2024's own Annual Report figures already used below - {AR2025_URL}\n"
        f"FY2023 (ratios, RWAs, leverage, LCR, NSFR): Cynergy Bank Limited 2023 Pillar 3 Disclosures, "
        f"'Key metrics' table (UK KM1) p.7, 'Overview of risk-weighted exposure amounts' (UK OV1) p.8 and "
        f"'Composition of regulatory own funds' (CC1) p.9 - {P3_2023_URL} (found 2026-09-15; see the "
        f"FY2023 correction below)\n"
        f"FY2024 & FY2023 (capital AMOUNTS): Cynergy Bank plc Annual Report & Accounts 2024, p.146 (Note 32, Capital resources) - {AR2024_URL}\n"
        f"FY2024 CET1 ratio (13.59%): Cynergy Bank plc Annual Report & Accounts 2024, p.6 (Chief Executive's "
        f"review): 'The common equity tier 1 (CET1) ratio remains stable at 13.59%. This level provides a solid "
        f"capital buffer...'. This is the only capital or liquidity RATIO stated numerically anywhere in the "
        f"FY2023-FY2025 Annual Reports; FY2023's and FY2025's equivalent narrative passages are purely "
        f"qualitative ('Our common equity tier 1 ratio remained robust', AR2023 p.6) - {AR2024_URL}\n"
        f"FY2022: Cynergy Bank Limited 2022 Pillar 3, 'Key metrics' table p.5 and 'Overview of "
        f"risk-weighted exposure amounts' p.6 - {P3_2022_URL} (delisted from the live site; archived copy "
        f"used: {P3_2022_WAYBACK})\n"
        f"FY2021: Cynergy Bank Limited Pillar 3 - 31 December 2021, 'Key capital, liquidity and leverage "
        f"metrics' table p.20 and NSFR table p.21, cross-checked against the 2022 edition's own FY2021 "
        f"comparative column (which restates the same figures at full precision) - {P3_2021_URL} "
        f"(delisted from the live site; archived copy used: {P3_2021_WAYBACK})\n"
        "RESOLVED 2026-09-12: this note previously claimed FY2021 and FY2022 had no quantitative capital "
        "or liquidity figures, on the basis that their Annual Reports carry only qualitative narrative. "
        "It also flagged, correctly, that an FY2021 standalone Pillar 3 'may well also exist'. It does - "
        "and so does FY2022. Both were found via a Wayback CDX search of cynergybank.co.uk and are now "
        "the source for those two years above. The Annual-Report observation still stands and is why "
        "those documents are not used for these metrics.\n"
        "RESOLVED 2026-09-15 (multi-year trailing-gap investigation). The FY2024 and FY2025 Pillar 3 gaps "
        "are a DOCUMENTED STRUCTURAL ABSENCE, not a sourcing failure: Cynergy Bank became a Small Domestic "
        "Deposit Taker (SDDT) and is no longer required to publish Pillar 3 disclosures at all. The Bank "
        "states this itself, twice, in its own Annual Reports:\n"
        f"  - Annual Report & Accounts 2024, p.71 (Risk report, 'Basel 3.1 Strong and Simple Regime'): 'The "
        f"Bank applied for the Modification by Consent to become an SDDT and received approval on 17 January "
        f"2025. As a result, we are not required to publish Pillar 3 disclosures as at 31 December 2024 and "
        f"will submit only a simplified retail deposit ratio instead of a full Net Stable Funding Ratio "
        f"(NSFR) going forward.' - {AR2024_URL}\n"
        f"  - Annual Report & Accounts 2025, p.45 (Emerging risks): 'On 17 January 2025, the Bank's "
        f"application for modification by consent to be treated as an SDDT was approved. Consequently, the "
        f"Bank is no longer required to publish Pillar 3 disclosures for the period ended 31 December 2025. "
        f"Furthermore, liquidity reporting has been streamlined, with the Simplified Retail Deposit Ratio "
        f"(SRDR) replacing the full Net Stable Funding Ratio (NSFR) requirement.' The same page records that "
        f"Interim Capital Regime modification-by-consent applications for both Cynergy Capital Ltd and "
        f"Cynergy Bank plc were approved on 22 May 2025 - {AR2025_URL}\n"
        "So for FY2024 and FY2025 there is no Pillar 3 document to find, and NSFR in particular is no longer "
        "even a metric the Bank is required to compute (SRDR replaces it). The Bank remains fully PRA-"
        "authorised throughout - it appears as 'Cynergy Bank Plc', FRN 575105, in the Bank of England's own "
        "'List of banks' as at 30 September 2026 (banks-list-2609.csv) - so this is a disclosure-regime "
        "change, not an entity cessation.\n"
        "INDEPENDENTLY CORROBORATED 2026-09-15 against the PRA's own firm-level register (found while "
        "generalising this finding across the rest of the bank set, and recorded here because it is the "
        "control that validates the method). The Bank of England consolidated list of waivers and "
        "modifications granted to PRA-authorised firms (downloaded 2026-09-15, "
        "https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/authorisations/"
        "waivers-and-modifications-of-rules/consolidated-waivers-pra-firms.csv) carries the row: FRN 575105, "
        "'Cynergy Bank Plc', 'Description - Modification by Consent - PRA Rulebook- CRR Firms- Rule 3.1 of "
        "the SDDT Regime - General Application Part 3.1', rule 'SDDT Regime - General Application', sub rule "
        "'Ru 3.1', waiver ref 'A00009569P.pdf', start date '17/01/2025', no end date. That start date matches "
        "the Bank's own stated approval date to the day, which establishes that a Rule 3.1 row in this "
        "register is exactly the instrument the Bank describes - the basis on which the same register is used "
        "to evidence SDDT status for other banks in this project that do not narrate it themselves (Methodist "
        "Chapel Aid, Julian Hodge, Cambridge & Counties, Triodos UK, Monument, among others).\n"
        "**FY2023 CORRECTION, 2026-09-15 - THE 'UNREACHABLE' FINDING RECORDED BELOW WAS WRONG, AND THE "
        "FY2023 PILLAR 3 DOCUMENT IS NOW THE SOURCE FOR THAT YEAR'S RATIOS, RWAs, LEVERAGE AND LIQUIDITY.** "
        f"It is live on the Bank's own current site at {P3_2023_URL} .\n"
        "WHY EVERY EARLIER ROUTE MISSED IT, since the failure mode is reusable across this project: the "
        "FY2023 edition is linked from exactly one page - /strong-and-prudent-management - and from nowhere "
        "else. The pages the earlier passes enumerated (/about-us/company-performance and /document-library) "
        "genuinely do not list it, so each negative result recorded below was individually accurate and "
        "collectively wrong. In particular the claim that the Contentful space 'exposes exactly 15 PDFs, "
        "every one an Annual Report' was an artefact of enumerating from the company-performance page: that "
        "page's asset set is 15 Annual Reports, while the strong-and-prudent-management page's asset set is a "
        "DIFFERENT 15 assets containing six Pillar 3 editions. A Contentful space is not enumerable from any "
        "one rendered page, so treating a single page's asset list as 'the whole asset set' is what produced "
        "a confident false negative. The Wayback CDX sweep missed it for a second, independent reason: the "
        "FY2023 edition never lived on the old cynergybank.co.uk /media/ tree at all, only on "
        "assets.ctfassets.net, so no CDX search of the bank's own domain could ever have returned it.\n"
        + ENUMERATION_NOTE + "\n"
        "Consequence for the sheets: FY2023 is now populated from its own Pillar 3 - Total RWAs 2,084,246; "
        "CET1 and Tier 1 ratio 14.69%; Total capital ratio 15.41%; leverage ratio 6.96% (on a leverage "
        "exposure measure of 4,398,669); LCR 304.44%; NSFR 148.67%. Nothing already in the workbook was "
        "overwritten: the FY2023 capital AMOUNTS previously taken from AR2024's Note 32 are independently "
        "confirmed by this document's own CC1 table (CET1 306,251 and Total capital 321,251 in both), and "
        "its FY2022 comparative column reproduces the FY2022 capital, RWA, ratio and leverage figures "
        "already held here exactly. FY2024 and FY2025 keep only the AR2025 Note 32 capital amounts and the "
        "AR2024 narrative CET1 ratio; those two years are an enumerated structural absence, not an open gap. "
        "Nothing is back-solved.\n"
        "--- superseded reasoning, retained so the same dead ends are not re-walked ---\n"
        "FY2023 is a different, weaker case and is deliberately NOT claimed as structurally absent: the SDDT "
        "approval post-dates it (17 January 2025), so a 31 December 2023 Pillar 3 disclosure was still "
        "required, and the FY2023 Annual Report's own Board Risk Committee agenda (p.43) lists 'Pillar 3 "
        "disclosure' among the items the committee reviewed during 2023 - i.e. the document almost certainly "
        "existed. [SUPERSEDED] It simply cannot be reached any more: cynergybank.co.uk migrated off its old Umbraco "
        "/media/ tree (which hosted the 2018-2022 editions) onto a Contentful-backed Next.js site during "
        "2024, and re-checked 2026-09-15 the replacement pages carry no Pillar 3 document at all - "
        "/about-us/company-performance lists 15 Annual Reports (FY2012-FY2025) and nothing else, and "
        "/document-library lists only product terms/fee documents. A full Wayback CDX enumeration of every "
        "PDF ever captured on the domain returns no Pillar 3 edition later than 2022. USER-ACTIONABLE: the "
        "FY2023 edition would have to be requested from the Bank directly.\n"
        "RE-VERIFIED 2026-09-15 under a maximum-effort sweep that treated this script's own 'unreachable' "
        "finding as unproven (five comparable claims elsewhere in this project were disproved the same day). "
        "Four independent routes, all negative: (1) the Contentful asset space behind the current site "
        "(xzmqg68ot16t) exposes exactly 15 PDFs, every one an Annual Report FY2012-FY2025 and not one a "
        "Pillar 3 - enumerated from the rendered company-performance page rather than the 3 reports it "
        "links, so this is the whole asset set, not the page's selection; (2) a full Wayback CDX sweep of "
        "cynergybank.co.uk with no filename filter returns 125 distinct PDFs ever captured, of which exactly "
        "3 are Pillar 3 editions (FY2020, FY2021, FY2022) and none later; (3) the archived Next.js "
        "document-library.json payloads from 25 Sep 2024 and 11 Mar 2025 - i.e. after the FY2023 edition "
        "would have been due - contain zero occurrences of 'pillar', so the replacement site never listed "
        "one; (4) the FY2023 Annual Report's own capital narrative is qualitative only ('Our common equity "
        "tier 1 ratio remained robust', 'The liquidity coverage ratio has continued to exceed the regulatory "
        "requirements throughout 2023') with no RWA figure and no ratio anywhere in the document. Its Note 32 "
        "capital table is already the source for the FY2023 capital AMOUNTS carried above. [SUPERSEDED - the "
        "document was reached on 2026-09-15 via the /strong-and-prudent-management page; the four routes "
        "listed here were each accurate about the pages they checked and wrong about the conclusion.]\n"
        "--- end of superseded reasoning ---\n"
        "FY2025 capital AMOUNTS come from the Annual Report's own Note 32 capital-management table (above), "
        "and the FY2024 CET1/Tier 1 RATIO from the AR2024 narrative (above). The remaining FY2024-FY2025 "
        "cells - Total RWAs, Total Capital Ratio, LCR, Leverage Ratio, NSFR, and the FY2025 CET1 and Tier 1 "
        "ratios - stay blank. They are not derived from the disclosed capital amounts (that would require "
        "back-solving RWAs out of a ratio, which this project does not do).\n"
        f"FY2020: Cynergy Bank Pillar 3 Disclosures 2020, capital and leverage tables (pp.7-11) and liquidity "
        f"tables (pp.13-14) - {P3_2020_URL}\n"
        f"FY2019: Cynergy Bank Pillar 3 Disclosures 2019, capital and RWA tables (pp.6-9) - {P3_2019_URL}\n"
        f"FY2018: Cynergy Bank Pillar 3 Disclosures 2018, capital, leverage and RWA tables (pp.5-9) - {P3_2018_URL}\n"
        f"FY2017: via FY2018 Pillar 3 Disclosures 2018's own FY2017 comparative column (same document/pages as "
        f"FY2018 above) - the FY2017 Pillar 3 document itself was not located - {P3_2018_URL}\n"
        f"FY2016: Bank of Cyprus UK Limited Annual Report & Accounts 2016 (Companies House filing, scanned), "
        f"Note on Capital management/Pillar 3, p.14-15 - {AR2016_CH_URL}\n"
        f"FY2015: Bank of Cyprus UK Limited Annual Report & Accounts 2015 (Companies House filing, scanned), "
        f"Note on Capital management, p.13-14 - {AR2015_CH_URL}\n"
        f"FY2014: Bank of Cyprus UK Limited Annual Report & Accounts 2014 (Companies House filing, scanned), "
        f"Note on Capital management, p.13-14 - {AR2014_CH_URL}\n\n"
        "HD-051 note: FY2014-FY2016 predate the CRD IV/Basel III 'CET1' concept - these Annual Reports disclose "
        "'Core Tier 1 capital' and 'Tier 1 ratio' only (Basel II/CRD III era terminology), shown here as the "
        "closest equivalent to CET1/Tier 1 (there was no Additional Tier 1 instrument in issue in any year "
        "reviewed, so Core Tier 1 = Tier 1 for these years, same as the modern-era convention of Tier 1 = "
        "CET1). FY2014-2017 figures are on the Company-only (non-consolidated) basis - see the Cash Flow "
        "Statement sheet's source note."
    )


bw = BankWorkbook(bank_name="Cynergy Bank Plc", years=Y_CORE, year_label=YEAR_LABEL, header_color="46C505")

STATEMENTS_ENTITY_NOTE = (
    ENTITY_NOTE
    + "\n\nEach year's own originally-published figures are used for the Balance Sheet, Profit & Loss and "
    "Statement of Changes in Equity below (not later restated comparatives) - the same convention already "
    "applied to the Cash Flow Statement. FY2025's own report explicitly restates FY2024 (e.g. Total assets "
    "£5,098,500k own-report vs £5,083,343k restated comparative shown in the FY2025 report) - FY2024's own "
    "Annual Report is used instead. FY2021 figures are the FY2021 comparative column within FY2022's own "
    "Annual Report (Companies House, scanned) - the FY2021 Annual Report itself was not independently "
    "re-checked, same pattern as the Cash Flow Statement's FY2021 sourcing.\n"
    "PRESENTATION NOTE: 'Current tax asset(s)' and 'Deferred tax liabilities' only appear as their own "
    "Balance Sheet lines from FY2025 onward (per that year's own restatement note); earlier years fold these "
    "into Other assets/Other liabilities - left blank rather than guessed for FY2021-FY2024. 'Assets "
    "classified as held for sale' appears only FY2022-FY2023. Subordinated loan(s) were fully repaid during "
    "FY2022 (nil at 31 Dec 2022) and re-issued during FY2023 (£14,847k) - a genuine, disclosed movement, not "
    "a data gap.\n\n"
    "FY2014-FY2017 are Company-only (non-consolidated) - see ENTITY_NOTE. FY2017's own equity statement "
    "shows a single £46,000k 'Issue of share capital' line taking share capital from £65,000k to £111,000k, "
    "but FY2017's own cash flow statement shows only £16,000k 'Proceeds from issuance of new share capital' "
    "in financing activities for the same year - a genuine £30m gap between the two statements within "
    "FY2017's own Annual Report (not resolved by anything else in that report; possibly a non-cash "
    "conversion of existing related-party debt into equity alongside a separate cash subscription), "
    "reported here exactly as each statement states it, not reconciled or guessed. FY2018's equity "
    "statement shows a 'Restated opening balance under IFRS 9' adjustment (+£96k) and two same-year "
    "share-capital movements that net to nil (a £7,000k 'capitalisation of revaluation reserve' followed by "
    "a £7,000k 'reduction in share capital') - both are shown as separate rows here to match the source "
    "exactly. FY2019 introduces a £300k dividend paid to the then-parent Cynergy Capital Ltd - the first "
    "dividend in this equity history - plus IFRS 16 transition and (per Note 20) a small held-for-sale "
    "asset reclassification. 'Investment in subsidiary' drops from £400k (FY2014-2017) to £10k from FY2018 "
    "onward - a genuine revaluation/deconsolidation-adjustment disclosed in FY2018's own accounts, not a "
    "transcription error."
)

STATEMENTS_SOURCES = (
    "Sources - Cynergy Bank Plc's own Consolidated statement of financial position, statement of profit or "
    "loss / income statement, statement of comprehensive income, and statement of changes in equity, "
    "transcribed from each year's own report (not a later year's restated comparative):\n"
    f"FY2025 (& FY2024 restated comparative used only for the equity roll-forward's opening-balance cross-"
    f"check, not as FY2024's own figures): Cynergy Bank plc Annual Report & Accounts 2025, p.52-53 - "
    f"{AR2025_URL}\n"
    f"FY2024 (own, & FY2023 comparative cross-checked): Cynergy Bank plc Annual Report & Accounts 2024, "
    f"p.83-86 - {AR2024_URL}\n"
    f"FY2023 (own, & FY2022 comparative cross-checked): Cynergy Bank Limited Annual Report & Accounts 2023, "
    f"p.89-93 - {AR2023_URL}\n"
    f"FY2022 (own) & FY2021 (comparative): Cynergy Bank Limited Annual Report & Accounts 2022 (Companies "
    f"House filing, scanned), p.91-93 - {AR2022_CH_URL}\n"
    f"FY2020 (own): Cynergy Bank Limited Annual Report & Accounts 2020 (Companies House filing, scanned), "
    f"p.56-58 - {AR2020_CH_URL}\n"
    f"FY2019 (own): Cynergy Bank Limited Annual Report & Accounts 2019 (Companies House filing, scanned), "
    f"p.50-52 (dense pages visually re-rendered from the original PDF page images at 200dpi and read "
    f"directly, since raw OCR text extraction came out badly garbled on these specific pages) - {AR2019_CH_URL}\n"
    f"FY2018 (own): Cynergy Bank Limited Annual Report & Accounts 2018 (Companies House filing, scanned), "
    f"p.20-22, Company-only basis - {AR2018_CH_URL}\n"
    f"FY2017 (own): Bank of Cyprus UK Limited Annual Report & Accounts 2017 (Companies House filing, "
    f"scanned), p.19-21, Company-only basis - {AR2017_CH_URL}\n"
    f"FY2016 (own): Bank of Cyprus UK Limited Annual Report & Accounts 2016 (Companies House filing, "
    f"scanned), p.10-12, Company-only basis - {AR2016_CH_URL}\n"
    f"FY2015 (own): Bank of Cyprus UK Limited Annual Report & Accounts 2015 (Companies House filing, "
    f"scanned), p.9-11, Company-only basis - {AR2015_CH_URL}\n"
    f"FY2014 (own): Bank of Cyprus UK Limited Annual Report & Accounts 2014 (Companies House filing, "
    f"scanned), p.9-11, Company-only basis - {AR2014_CH_URL}\n"
    f"FY2013 (own): Bank of Cyprus UK Limited Annual Report & Accounts 2013 (Companies House filing, "
    f"scanned), p.10-12, Company-only basis - {AR2013_CH_URL}\n\n"
    + STATEMENTS_ENTITY_NOTE
    + "\n\nHD-072 (statutory statements extended to FY2013): FY2013 is the real statutory floor for this "
    "entity (per HD-002's deep dive) - Bank of Cyprus UK Limited was incorporated 9 Apr 2003 as 'Bank of "
    "Cyprus Advances Limited' but only became an independently-capitalised subsidiary (rather than a UK "
    "branch of the Cyprus parent) on 25 June 2012, so no earlier year has a comparable standalone statutory "
    "statement - FY2012 itself is a part-year (25 Jun-31 Dec 2012) stub and is not usable as a prior year. "
    "FY2013's own Statement of financial position has no 'Property revaluation reserve' line at all (the "
    "reserve first appears in FY2014's own accounts, at £3,332k) - shown as 0 on the FY2013 closing / FY2014 "
    "opening equity balance, consistent with the source, not a gap. FY2013 also predates the 'Right-of-use "
    "assets'/'Lease liabilities' (pre-IFRS16), 'Assets classified as held for sale' and 'Deferred tax "
    "liabilities' lines seen in later years - left blank, same convention as FY2014-2017. FY2013's own Income "
    "Statement reports a 'Net gains on financial instrument transactions' line (£332k), shown on the 'Fair "
    "value adjustment/(loss)/gain on hedging or derivative instruments' row - the closest equivalent line in "
    "later years' presentation."
)

ASSET_QUALITY_SOURCES = (
    "Sources - Cynergy Bank Plc's own Credit Risk note (IFRS 9 staging, Consolidated Loans + Overdrafts "
    "gross carrying amount and ECL reconciliation tables combined):\n"
    f"FY2025 (& FY2024 own-report comparative used for cross-check only): Annual Report & Accounts 2025, "
    f"Note 15/Credit risk section, p.65-67 - {AR2025_URL}\n"
    f"FY2024 (own) & FY2023 (own-report comparative, cross-checked against AR2023's own FY2023 figures): "
    f"Annual Report & Accounts 2024, p.113-118 - {AR2024_URL}\n"
    f"FY2022 (own, via AR2023's own comparative column) & the FY2021 closing balance (via AR2023's own "
    f"'At 1 January 2022' opening-balance row, which is FY2021's own closing balance): Annual Report & "
    f"Accounts 2023, p.123-126 - {AR2023_URL}\n"
    f"FY2020 (own): Cynergy Bank Limited Annual Report & Accounts 2020 (Companies House filing, scanned), "
    f"Note 17 (Loans and advances to customers), p.89-91 - {AR2020_CH_URL}\n"
    f"FY2019 (own): Cynergy Bank Limited Annual Report & Accounts 2019 (Companies House filing, scanned), "
    f"Note 17, p.81-83 - {AR2019_CH_URL}\n"
    f"FY2018 (own): Cynergy Bank Limited Annual Report & Accounts 2018 (Companies House filing, scanned), "
    f"Note 17, p.43-45 - {AR2018_CH_URL}\n"
    f"FY2017 (own): Bank of Cyprus UK Limited Annual Report & Accounts 2017 (Companies House filing, scanned), "
    f"Note 17, p.35, Company-only basis - {AR2017_CH_URL}\n"
    f"FY2016 (own): Bank of Cyprus UK Limited Annual Report & Accounts 2016 (Companies House filing, scanned), "
    f"Note 17, p.29, Company-only basis - {AR2016_CH_URL}\n"
    f"FY2015 (own): Bank of Cyprus UK Limited Annual Report & Accounts 2015 (Companies House filing, scanned), "
    f"Note 16, p.20, Company-only basis - {AR2015_CH_URL}\n"
    f"FY2014 (own): Bank of Cyprus UK Limited Annual Report & Accounts 2014 (Companies House filing, scanned), "
    f"Note 16, p.24, Company-only basis - {AR2014_CH_URL}\n\n"
    + ENTITY_NOTE
    + "\n\nFY2021's stage split is the FY2021 closing balance recovered from FY2022's own reconciliation "
    "table 'At 1 January' row (the FY2021 Annual Report's own credit risk note was not independently "
    "re-checked) - same 'sourced from the following year's own comparative' pattern used elsewhere in this "
    "project. Ratios (Stage 3/Total gross exposure, Total ECL/Total gross exposure coverage, Stage 3 "
    "coverage) are calculated from the gross carrying amount and ECL figures above, not separately "
    "disclosed."
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances with central banks",
     {"FY2025": 575031, "FY2024": 1014572, "FY2023": 697790, "FY2022": 553007, "FY2021": 324982, "FY2020": 246256, "FY2019": 111754, "FY2018": 196454, "FY2017": 358724, "FY2016": 205062, "FY2015": 228858, "FY2014": 367398, "FY2013": 468784}),
    ("DATA", "Placements with banks",
     {"FY2025": 36872, "FY2024": 44279, "FY2023": 63156, "FY2022": 102320, "FY2021": 54529, "FY2020": 44784, "FY2019": 63265, "FY2018": 55538, "FY2017": 32625, "FY2016": 67948, "FY2015": 83373, "FY2014": 58528, "FY2013": 47519}),
    ("DATA", "Placements with related entities",
     {"FY2017": 25226, "FY2016": 24949, "FY2015": 21127, "FY2014": 9555, "FY2013": 9916}),
    ("DATA", "Investment in subsidiary",
     {"FY2019": 10, "FY2018": 10, "FY2017": 400, "FY2016": 400, "FY2015": 400, "FY2014": 400, "FY2013": 400}),
    ("DATA", "Loans and advances to customers",
     {"FY2025": 3745133, "FY2024": 3653477, "FY2023": 3564297, "FY2022": 3254230, "FY2021": 2949578, "FY2020": 2613962, "FY2019": 2264381, "FY2018": 1668923, "FY2017": 1407200, "FY2016": 1083922, "FY2015": 820807, "FY2014": 617976, "FY2013": 550494}),
    ("DATA", "Investment in securities",
     {"FY2025": 1080929, "FY2024": 252914, "FY2023": 127547, "FY2022": 113377, "FY2021": 137782}),
    ("DATA", "Derivative assets",
     {"FY2025": 1843, "FY2024": 6404, "FY2023": 4512, "FY2022": 12404, "FY2021": 54, "FY2020": 31}),
    ("DATA", "Intangible assets",
     {"FY2025": 78293, "FY2024": 63455, "FY2023": 49303, "FY2022": 27469, "FY2021": 26513, "FY2020": 19712, "FY2019": 9804, "FY2018": 1010, "FY2017": 1623, "FY2016": 840, "FY2015": 640, "FY2014": 683, "FY2013": 510}),
    ("DATA", "Right-of-use assets",
     {"FY2025": 9918, "FY2024": 11060, "FY2023": 11553, "FY2022": 11891, "FY2021": 220, "FY2020": 242, "FY2019": 87}),
    ("DATA", "Property and equipment",
     {"FY2025": 3080, "FY2024": 7934, "FY2023": 3861, "FY2022": 914, "FY2021": 12875, "FY2020": 13573, "FY2019": 7514, "FY2018": 15652, "FY2017": 15773, "FY2016": 16445, "FY2015": 11178, "FY2014": 12085, "FY2013": 9315}),
    ("DATA", "Assets classified as held for sale",
     {"FY2023": 7070, "FY2022": 7070, "FY2019": 8819}),
    ("DATA", "Other assets",
     {"FY2025": 58369, "FY2024": 44405, "FY2023": 82142, "FY2022": 42031, "FY2021": 11501, "FY2020": 4886, "FY2019": 6270, "FY2018": 17433, "FY2017": 35547, "FY2016": 3411, "FY2015": 2480, "FY2014": 2418, "FY2013": 3899}),
    ("DATA", "Current tax assets",
     {"FY2025": 7854}),
    ("TOTAL", "Total assets",
     {"FY2025": 5597322, "FY2024": 5098500, "FY2023": 4611231, "FY2022": 4124713, "FY2021": 3518034, "FY2020": 2943446, "FY2019": 2471904, "FY2018": 1955020, "FY2017": 1877118, "FY2016": 1402977, "FY2015": 1168863, "FY2014": 1069043, "FY2013": 1090837}),

    ("SECTION", "Liabilities", {}),
    ("DATA", "Placements by related entities",
     {"FY2017": 26605, "FY2016": 28381, "FY2015": 24216, "FY2014": 13123, "FY2013": 13570}),
    ("DATA", "Amounts due to banks",
     {"FY2016": 0, "FY2015": 7, "FY2014": 10, "FY2013": 1006}),
    ("DATA", "Customer deposits",
     {"FY2025": 4910863, "FY2024": 4492026, "FY2023": 3758037, "FY2022": 3336442, "FY2021": 2832564, "FY2020": 2352241, "FY2019": 2227678, "FY2018": 1762654, "FY2017": 1656975, "FY2016": 1257403, "FY2015": 1038348, "FY2014": 955464, "FY2013": 980845}),
    ("DATA", "Bank deposits",
     {"FY2025": 85131, "FY2024": 80924, "FY2023": 359667, "FY2022": 390170, "FY2021": 400125, "FY2020": 340131, "FY2019": 25063, "FY2018": 240}),
    ("DATA", "Subordinated loan(s)",
     {"FY2025": 49805, "FY2024": 14881, "FY2023": 14847, "FY2022": 0, "FY2021": 29868, "FY2020": 29744, "FY2019": 29629, "FY2018": 29524, "FY2017": 29537, "FY2016": 30061, "FY2015": 30062, "FY2014": 30062, "FY2013": 30056}),
    ("DATA", "Lease liabilities",
     {"FY2025": 10690, "FY2024": 11895, "FY2023": 12873, "FY2022": 12065, "FY2021": 278, "FY2020": 261, "FY2019": 110}),
    ("DATA", "Provision for customer redress",
     {"FY2022": 716, "FY2021": 261, "FY2020": 132, "FY2019": 1164, "FY2018": 12221, "FY2017": 41516, "FY2016": 14910}),
    ("DATA", "Deferred tax liabilities",
     {"FY2025": 11526}),
    ("DATA", "Derivative liabilities",
     {"FY2025": 14563, "FY2024": 11478, "FY2023": 32374, "FY2022": 3838, "FY2021": 429, "FY2020": 772}),
    ("DATA", "Other liabilities",
     {"FY2025": 88515, "FY2024": 99440, "FY2023": 83883, "FY2022": 72036, "FY2021": 33793, "FY2020": 24378, "FY2019": 21810, "FY2018": 13050, "FY2017": 9767, "FY2016": 6365, "FY2015": 6410, "FY2014": 4168, "FY2013": 5777}),
    ("TOTAL", "Total liabilities",
     {"FY2025": 5171093, "FY2024": 4710644, "FY2023": 4261681, "FY2022": 3815267, "FY2021": 3297318, "FY2020": 2747659, "FY2019": 2305254, "FY2018": 1817689, "FY2017": 1764400, "FY2016": 1337120, "FY2015": 1099043, "FY2014": 1002827, "FY2013": 1031254}),

    ("SECTION", "Equity", {}),
    ("DATA", "Share capital",
     {"FY2025": 202000, "FY2024": 202000, "FY2023": 202000, "FY2022": 202000, "FY2021": 155000, "FY2020": 155000, "FY2019": 146000, "FY2018": 131000, "FY2017": 111000, "FY2016": 65000, "FY2015": 65000, "FY2014": 65000, "FY2013": 65000}),
    ("DATA", "Property revaluation reserve",
     {"FY2024": 505, "FY2023": 2433, "FY2022": 3148, "FY2021": 1674, "FY2020": 1674, "FY2019": 2435, "FY2018": 1306, "FY2017": 8389, "FY2016": 8389, "FY2015": 3332, "FY2014": 3332}),
    ("DATA", "Accumulated profits",
     {"FY2025": 222240, "FY2024": 184557, "FY2023": 145003, "FY2022": 104490, "FY2021": 64191, "FY2020": 39113, "FY2019": 18215, "FY2018": 5025, "FY2017": -6671, "FY2016": -7532, "FY2015": 1488, "FY2014": -2116, "FY2013": -5417}),
    ("TOTAL", "Equity attributable to owners of the company",
     {"FY2025": 424240, "FY2024": 387062, "FY2023": 349436, "FY2022": 309638, "FY2021": 220865, "FY2020": 195787, "FY2019": 166650, "FY2018": 137331, "FY2017": 112718, "FY2016": 65857, "FY2015": 69820, "FY2014": 66216, "FY2013": 59583}),
    ("DATA", "Non-controlling interest",
     {"FY2025": 1989, "FY2024": 794, "FY2023": 114, "FY2022": -192, "FY2021": -149}),
    ("TOTAL", "Total equity",
     {"FY2025": 426229, "FY2024": 387856, "FY2023": 349550, "FY2022": 309446, "FY2021": 220716, "FY2020": 195787, "FY2019": 166650, "FY2018": 137331, "FY2017": 112718, "FY2016": 65857, "FY2015": 69820, "FY2014": 66216, "FY2013": 59583}),
    ("TOTAL", "Total liabilities and equity",
     {"FY2025": 5597322, "FY2024": 5098500, "FY2023": 4611231, "FY2022": 4124713, "FY2021": 3518034, "FY2020": 2943446, "FY2019": 2471904, "FY2018": 1955020, "FY2017": 1877118, "FY2016": 1402977, "FY2015": 1168863, "FY2014": 1069043, "FY2013": 1090837}),
]

bw.add_balance_sheet_sheet(
    title="Cynergy Bank Plc — Consolidated Statement of Financial Position",
    subtitle="Consolidated basis, £'000. See source note at bottom (presentation changes documented).",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=86,
    source_height=320,
    unit_suffix=" (£'000)",
    years=YEARS,
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income calculated using the effective interest method",
     {"FY2025": 328554, "FY2024": 312777, "FY2023": 276395, "FY2022": 167199, "FY2021": 105716, "FY2020": 103143, "FY2019": 78051, "FY2018": 63667}),
    ("DATA", "Other interest and similar income/(expense)",
     {"FY2025": 59793, "FY2024": 57827, "FY2023": 41559, "FY2022": 1610, "FY2021": -187, "FY2020": 729, "FY2019": 4407, "FY2018": 3565}),
    ("DATA", "Interest income (FY2013-2017 Company-only presentation, not split into EIM/other)",
     {"FY2017": 52715, "FY2016": 43419, "FY2015": 33757, "FY2014": 31070, "FY2013": 35808}),
    ("DATA", "Interest expense calculated using the effective interest method",
     {"FY2025": -193820, "FY2024": -191478, "FY2023": -128355, "FY2022": -44103, "FY2021": -18356, "FY2020": -26915, "FY2019": -26348, "FY2018": -21565}),
    ("DATA", "Other interest expense",
     {"FY2025": -61768, "FY2024": -48550, "FY2023": -34811, "FY2022": -1578}),
    ("DATA", "Interest expense (FY2013-2017 Company-only presentation, not split into EIM/other)",
     {"FY2017": -15318, "FY2016": -16340, "FY2015": -14577, "FY2014": -16467, "FY2013": -23510}),
    ("TOTAL", "Net interest income",
     {"FY2025": 132759, "FY2024": 130576, "FY2023": 154788, "FY2022": 123128, "FY2021": 87173, "FY2020": 76957, "FY2019": 56110, "FY2018": 45667, "FY2017": 37397, "FY2016": 27079, "FY2015": 19180, "FY2014": 14603, "FY2013": 12298}),
    ("DATA", "Fee and commission income",
     {"FY2025": 3777, "FY2024": 3089, "FY2023": 2606, "FY2022": 1667, "FY2021": 1193, "FY2020": 1814, "FY2019": 2364, "FY2018": 2433, "FY2017": 2360, "FY2016": 2556, "FY2015": 4238, "FY2014": 3590, "FY2013": 3321}),
    ("DATA", "Foreign exchange (losses)/gains",
     {"FY2025": -677, "FY2024": 712, "FY2023": 42, "FY2022": -1194, "FY2021": 1853, "FY2020": -1626, "FY2019": 424, "FY2018": 285, "FY2017": 302, "FY2016": 348, "FY2015": 372, "FY2014": 341, "FY2013": 458}),
    ("DATA", "Fair value adjustment/(loss)/gain on hedging or derivative instruments",
     {"FY2025": 544, "FY2024": -204, "FY2023": 2110, "FY2022": 3983, "FY2021": -2190, "FY2020": 1180, "FY2019": 100, "FY2018": 211, "FY2017": -38, "FY2016": 68, "FY2015": 209, "FY2014": 185, "FY2013": 332}),
    ("DATA", "Net gains on derecognition of financial assets",
     {"FY2025": 3578}),
    ("DATA", "Other income",
     {"FY2025": 504, "FY2024": 473}),
    ("TOTAL", "Total operating income",
     {"FY2025": 140485, "FY2024": 134646, "FY2023": 159546, "FY2022": 127584, "FY2021": 88029, "FY2020": 78325, "FY2019": 58998, "FY2018": 48596, "FY2017": 40021, "FY2016": 30051, "FY2015": 23999, "FY2014": 18719, "FY2013": 16409}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Staff costs",
     {"FY2025": -41616, "FY2024": -42783, "FY2023": -49464, "FY2022": -38334, "FY2021": -28874, "FY2020": -23715, "FY2019": -20015, "FY2018": -22221, "FY2017": -18689, "FY2016": -13260, "FY2015": -10042, "FY2014": -9273, "FY2013": -8086}),
    ("DATA", "Depreciation, amortisation and impairment/write-offs",
     {"FY2025": -12516, "FY2024": -9766, "FY2023": -7072, "FY2022": -5758, "FY2021": -3447, "FY2020": -4446, "FY2019": -1274, "FY2018": -3382, "FY2017": -1509, "FY2016": -1426, "FY2015": -1491, "FY2014": -1453, "FY2013": -1453}),
    ("DATA", "Other operating expenses",
     {"FY2025": -35284, "FY2024": -28383, "FY2023": -43684, "FY2022": -33133, "FY2021": -19912, "FY2020": -18162, "FY2019": -14846, "FY2018": -16613, "FY2017": -14404, "FY2016": -9465, "FY2015": -8571, "FY2014": -7098, "FY2013": -5468}),
    ("TOTAL", "Total operating expenses",
     {"FY2025": -89416, "FY2024": -80932, "FY2023": -100220, "FY2022": -77225, "FY2021": -52233, "FY2020": -46323, "FY2019": -36135, "FY2018": -42216, "FY2017": -34602, "FY2016": -24151, "FY2015": -20104, "FY2014": -17824, "FY2013": -15007}),
    ("DATA", "Provision for customer redress",
     {"FY2017": -4000, "FY2016": -14910}),
    ("DATA", "Other gains",
     {"FY2025": 404, "FY2024": 1000}),
    ("DATA", "Gain on sale of property",
     {"FY2023": 276, "FY2022": 9230}),
    ("TOTAL", "Profit before credit impairment reversals/(charges)",
     {"FY2025": 51473, "FY2024": 54714, "FY2023": 59602, "FY2022": 59589, "FY2021": 35796, "FY2020": 32002, "FY2019": 16863, "FY2018": 6380, "FY2017": 1419, "FY2016": -9010, "FY2015": 3895, "FY2014": 895, "FY2013": 1402}),
    ("DATA", "Credit impairment reversals/(charges) on financial assets",
     {"FY2025": 91, "FY2024": -2082, "FY2023": -4445, "FY2022": -9100, "FY2021": -5396, "FY2020": -4986, "FY2019": -292, "FY2018": -223, "FY2017": 497, "FY2016": 898, "FY2015": 688, "FY2014": 3294, "FY2013": -1287}),
    ("TOTAL", "Profit before tax",
     {"FY2025": 51564, "FY2024": 52632, "FY2023": 55157, "FY2022": 50489, "FY2021": 30400, "FY2020": 27016, "FY2019": 16571, "FY2018": 6157, "FY2017": 1916, "FY2016": -8112, "FY2015": 4583, "FY2014": 4189, "FY2013": 115}),
    ("DATA", "Income tax expense",
     {"FY2025": -13624, "FY2024": -12398, "FY2023": -14544, "FY2022": -10233, "FY2021": -5471, "FY2020": -6188, "FY2019": -3052, "FY2018": -1557, "FY2017": -1055, "FY2016": -908, "FY2015": -979, "FY2014": -888, "FY2013": -627}),
    ("TOTAL", "Profit for the year",
     {"FY2025": 37940, "FY2024": 40234, "FY2023": 40613, "FY2022": 40256, "FY2021": 24929, "FY2020": 20828, "FY2019": 13519, "FY2018": 4600, "FY2017": 861, "FY2016": -9020, "FY2015": 3604, "FY2014": 3301, "FY2013": -512}),
    ("DATA", "Profit attributable to: Owners of the company",
     {"FY2025": 36745, "FY2024": 39554, "FY2023": 40307, "FY2022": 40299, "FY2021": 25078}),
    ("DATA", "Profit/(loss) attributable to: Non-controlling interest",
     {"FY2025": 1195, "FY2024": 680, "FY2023": 306, "FY2022": -43, "FY2021": -149}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Revaluation gain/(loss) on property",
     {"FY2024": -2571, "FY2022": 1474, "FY2020": -1227, "FY2019": 1024, "FY2014": 3535}),
    ("DATA", "Income tax relating to property revaluation",
     {"FY2024": 643, "FY2023": -509, "FY2020": 536, "FY2019": 105, "FY2018": -83, "FY2014": -203}),
    ("TOTAL", "Other comprehensive income/(expense) for the year, net of tax",
     {"FY2025": 0, "FY2024": -1928, "FY2023": -509, "FY2022": 1474, "FY2021": 0, "FY2020": -691, "FY2019": 1129, "FY2018": -83, "FY2017": 0, "FY2016": 0, "FY2015": 0, "FY2014": 3332, "FY2013": 0}),
    ("TOTAL", "Total comprehensive income for the year",
     {"FY2025": 37940, "FY2024": 38306, "FY2023": 40104, "FY2022": 41730, "FY2021": 24929, "FY2020": 20137, "FY2019": 14648, "FY2018": 4517, "FY2017": 861, "FY2016": -9020, "FY2015": 3604, "FY2014": 6633, "FY2013": -512}),
]

bw.add_income_statement_sheet(
    title="Cynergy Bank Plc — Consolidated Statement of Comprehensive Income",
    subtitle="Consolidated basis, £'000. See source note at bottom.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=86,
    source_height=320,
    unit_suffix=" (£'000)",
    years=YEARS,
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
equity_headers = ["Share capital", "Property revaluation reserve", "Accumulated profits",
                   "Total attributable to owners", "Non-controlling interest", "Total equity"]
equity_rows = [
    ("TOTAL", "At 1 January 2013",
     (65000, 0, -4905, 60095, None, 60095)),
    ("DATA", "Total comprehensive loss for the year", (None, None, -512, -512, None, -512)),
    ("TOTAL", "At 31 December 2013",
     (65000, 0, -5417, 59583, None, 59583)),

    ("TOTAL", "At 1 January 2014",
     (65000, 0, -5417, 59583, None, 59583)),
    ("DATA", "Total comprehensive profit for the year", (None, 3332, 3301, 6633, None, 6633)),
    ("TOTAL", "At 31 December 2014", (65000, 3332, -2116, 66216, None, 66216)),

    ("TOTAL", "At 1 January 2015", (65000, 3332, -2116, 66216, None, 66216)),
    ("DATA", "Total comprehensive profit for the year", (None, None, 3604, 3604, None, 3604)),
    ("TOTAL", "At 31 December 2015", (65000, 3332, 1488, 69820, None, 69820)),

    ("TOTAL", "At 1 January 2016", (65000, 3332, 1488, 69820, None, 69820)),
    ("DATA", "Total comprehensive (loss)/profit for the year", (None, 5057, -9020, -3963, None, -3963)),
    ("TOTAL", "At 31 December 2016", (65000, 8389, -7532, 65857, None, 65857)),

    ("TOTAL", "At 1 January 2017", (65000, 8389, -7532, 65857, None, 65857)),
    ("DATA", "Profit for the year after tax", (None, None, 861, 861, None, 861)),
    ("DATA", "Issue of share capital (note 25)", (46000, None, None, 46000, None, 46000)),
    ("TOTAL", "At 31 December 2017", (111000, 8389, -6671, 112718, None, 112718)),

    ("TOTAL", "At 1 January 2018", (111000, 8389, -6671, 112718, None, 112718)),
    ("DATA", "Impact of adopting IFRS 9 (Note 33)", (None, None, 96, 96, None, 96)),
    ("DATA", "Issue of shares by way of capitalisation of revaluation reserve", (7000, -7000, None, None, None, None)),
    ("DATA", "Reduction in share capital", (-7000, None, 7000, None, None, None)),
    ("DATA", "Profit for the year after tax", (None, None, 4600, 4600, None, 4600)),
    ("DATA", "Other comprehensive income (tax on property revaluation)", (None, -83, None, -83, None, -83)),
    ("DATA", "Issue of share capital (note 26)", (20000, None, None, 20000, None, 20000)),
    ("TOTAL", "At 31 December 2018", (131000, 1306, 5025, 137331, None, 137331)),

    ("TOTAL", "At 1 January 2019", (131000, 1306, 5025, 137331, None, 137331)),
    ("DATA", "Impact of adopting IFRS 16 (Note 20)", (None, None, -29, -29, None, -29)),
    ("DATA", "Dividend to Cynergy Capital Ltd", (None, None, -300, -300, None, -300)),
    ("DATA", "Profit for the year after tax", (None, None, 13519, 13519, None, 13519)),
    ("DATA", "Other comprehensive income", (None, 1129, None, 1129, None, 1129)),
    ("DATA", "Issue of share capital (Note 27)", (15000, None, None, 15000, None, 15000)),
    ("TOTAL", "At 31 December 2019", (146000, 2435, 18215, 166650, None, 166650)),

    ("TOTAL", "At 1 January 2020", (146000, 2435, 18215, 166650, None, 166650)),
    ("DATA", "Profit for the year after tax", (None, None, 20828, 20828, None, 20828)),
    ("DATA", "Other comprehensive expense", (None, -761, 70, -691, None, -691)),
    ("DATA", "Issue of share capital (note 27)", (9000, None, None, 9000, None, 9000)),
    ("TOTAL", "At 31 December 2020", (155000, 1674, 39113, 195787, None, 195787)),

    ("TOTAL", "At 1 January 2021 (via FY2022 report's own comparative)",
     (155000, 1674, 39113, 195787, 0, 195787)),
    ("DATA", "Profit for the year after tax", (None, None, 25078, 25078, -149, 24929)),
    ("TOTAL", "At 31 December 2021", (155000, 1674, 64191, 220865, -149, 220716)),

    ("TOTAL", "At 1 January 2022", (155000, 1674, 64191, 220865, -149, 220716)),
    ("DATA", "Profit/(loss) for the year after tax", (None, None, 40299, 40299, -43, 40256)),
    ("DATA", "Other comprehensive income (revaluation of own properties)", (None, 1474, None, 1474, None, 1474)),
    ("DATA", "Issue of share capital", (47000, None, None, 47000, None, 47000)),
    ("TOTAL", "At 31 December 2022", (202000, 3148, 104490, 309638, -192, 309446)),

    ("TOTAL", "At 1 January 2023", (202000, 3148, 104490, 309638, -192, 309446)),
    ("DATA", "Profit for the year after tax", (None, None, 40307, 40307, 306, 40613)),
    ("DATA", "Other comprehensive income (tax on property revaluation)", (None, -509, None, -509, None, -509)),
    ("DATA", "Transfer from revaluation reserve to retained earnings", (None, -206, 206, None, None, None)),
    ("TOTAL", "At 31 December 2023", (202000, 2433, 145003, 349436, 114, 349550)),

    ("TOTAL", "At 1 January 2024", (202000, 2433, 145003, 349436, 114, 349550)),
    ("DATA", "Profit for the year after tax", (None, None, 39554, 39554, 680, 40234)),
    ("DATA", "Other comprehensive income (revaluation loss on property, net of tax)", (None, -1928, None, -1928, None, -1928)),
    ("TOTAL", "At 31 December 2024", (202000, 505, 184557, 387062, 794, 387856)),

    ("TOTAL", "At 1 January 2025", (202000, 505, 184557, 387062, 794, 387856)),
    ("DATA", "Profit for the year after tax", (None, None, 36745, 36745, 1195, 37940)),
    ("DATA", "Transfer and tax release on disposal of revalued asset", (None, -505, 938, 433, None, 433)),
    ("TOTAL", "At 31 December 2025", (202000, 0, 222240, 424240, 1989, 426229)),
]

bw.add_equity_changes_sheet(
    title="Cynergy Bank Plc — Consolidated Statement of Changes in Equity",
    subtitle="Consolidated basis, £'000, chronological (oldest to newest). See source note at bottom.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=58,
    source_height=320,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax", {"FY2025": 51564, "FY2024": 52632, "FY2023": 55157, "FY2022": 50489, "FY2021": 30400, "FY2020": 27016, "FY2019": 16571, "FY2018": 6157, "FY2017": 1916, "FY2016": -8112, "FY2015": 4583, "FY2014": 4189, "FY2013": 115}),
    ("DATA", "Credit impairment charges/(reversals) on financial assets", {"FY2025": -91, "FY2024": 2082, "FY2023": 4445, "FY2022": 9100, "FY2021": 5396, "FY2020": 4986, "FY2019": 292, "FY2018": 223, "FY2017": -497, "FY2016": -898, "FY2015": -688, "FY2014": -3294, "FY2013": 1287}),
    ("DATA", "Depreciation of property, equipment and right-of-use assets", {"FY2025": 2028, "FY2024": 2197, "FY2023": 1730, "FY2022": 378, "FY2021": 1018, "FY2020": 1301, "FY2019": 773, "FY2018": 1036, "FY2017": 940, "FY2016": 969, "FY2015": 1085, "FY2014": 1087, "FY2013": 1123}),
    ("DATA", "Amortisation of intangible assets", {"FY2025": 9891, "FY2024": 7264, "FY2023": 4636, "FY2022": 3876, "FY2021": 2429, "FY2020": 3070, "FY2019": 501, "FY2018": 643, "FY2017": 569, "FY2016": 457, "FY2015": 406, "FY2014": 366, "FY2013": 330}),
    ("DATA", "Write-off/impairment of fixed and intangible assets", {"FY2025": 597, "FY2024": 305, "FY2023": 706, "FY2022": 1215, "FY2020": 77, "FY2018": 1703}),
    ("DATA", "Gain on disposal of property", {"FY2022": -9230, "FY2020": -30}),
    ("DATA", "Deferred gain on disposal of property", {"FY2023": -276, "FY2022": -277}),
    ("DATA", "Other gains", {"FY2025": -404, "FY2024": -1000}),
    ("DATA", "Net gains on derecognition of financial assets", {"FY2025": -3578}),
    ("DATA", "Dissolution of subsidiary", {"FY2020": 10}),
    ("DATA", "Collection of previously written off debt", {"FY2017": 249}),
    ("DATA", "Lease interest", {"FY2025": 877, "FY2024": 946, "FY2023": 937, "FY2022": 81, "FY2021": 29, "FY2020": 18, "FY2019": 8}),
    ("DATA", "Interest expense on subordinated loan(s)", {"FY2025": 4218, "FY2024": 1851, "FY2023": 783, "FY2022": 2328, "FY2021": 2400, "FY2020": 2406, "FY2019": 2400, "FY2018": 2500, "FY2017": 949, "FY2016": 2264, "FY2015": 2272, "FY2014": 2262, "FY2013": 2262}),
    ("DATA", "Interest income on asset-backed securities (accrual adjustment)", {"FY2025": -21020, "FY2024": -11703, "FY2023": -5667, "FY2022": -2570, "FY2021": -76}),
    ("DATA", "Amortisation of issuance costs relating to subordinated loan(s)", {"FY2025": -76, "FY2024": 34, "FY2023": 21, "FY2021": 125, "FY2020": 115, "FY2019": 105, "FY2018": 100}),
    ("DATA", "Interest paid on lease liabilities (accrual adjustment)", {"FY2025": -839}),
    ("DATA", "Tax paid", {"FY2025": -13475, "FY2024": -6580, "FY2023": -17052, "FY2022": -9937, "FY2021": -6409, "FY2020": -5255, "FY2019": -2087, "FY2018": -1613, "FY2017": -820, "FY2016": 998, "FY2015": 407, "FY2014": 0, "FY2013": -382}),
    ("DATA", "Foreign exchange losses/(gains)", {"FY2025": 677, "FY2024": -711, "FY2023": -42, "FY2022": 977, "FY2021": 68, "FY2019": -424, "FY2018": -285, "FY2017": -302}),
    ("DATA", "Foreign exchange and fair value losses/(gains) on derivative instruments (combined, as reported)", {"FY2020": 446}),
    ("DATA", "Fair value (gains)/losses on derivative/hedging instruments", {"FY2025": -544, "FY2024": 204, "FY2023": -2111, "FY2022": -3983}),
    ("SECTION", "Changes in operating assets", {}),
    ("DATA", "Mandatory deposits with central bank", {"FY2025": 0, "FY2024": 9348, "FY2023": -549, "FY2022": -1576, "FY2021": -1491, "FY2020": -1969, "FY2019": -1081, "FY2018": -1621, "FY2017": -464, "FY2016": -258, "FY2014": 0}),
    ("DATA", "Loans and advances to customers", {"FY2025": -545166, "FY2024": -90320, "FY2023": -313908, "FY2022": -313752, "FY2021": -341012, "FY2020": -354567, "FY2019": -595750, "FY2018": -261849, "FY2017": -323808, "FY2016": -259271, "FY2015": -201878, "FY2014": -64908, "FY2013": 69283}),
    ("DATA", "Other assets", {"FY2025": -11434, "FY2024": 38737, "FY2023": -41284, "FY2022": -23449, "FY2021": -225, "FY2020": 1647, "FY2019": 10869, "FY2018": 18440, "FY2017": -32309, "FY2016": -366, "FY2015": 70, "FY2014": -58, "FY2013": -1483}),
    ("DATA", "Derivative assets", {"FY2025": 4299, "FY2024": -2096, "FY2023": 10003, "FY2022": -12350, "FY2021": -23, "FY2020": 451}),
    ("DATA", "Accrued income and prepaid expenses", {"FY2022": -4072, "FY2021": -6391, "FY2020": -744, "FY2019": -602, "FY2018": -328, "FY2017": 235, "FY2016": -338, "FY2015": -362, "FY2014": 248, "FY2013": -161}),
    ("DATA", "Proceeds from sale of financial assets", {"FY2025": 76687}),
    ("SECTION", "Changes in operating liabilities", {}),
    ("DATA", "Customer and bank deposits", {"FY2025": 423044, "FY2024": 455246, "FY2023": 391092, "FY2022": 493923, "FY2021": 540317, "FY2020": 439631, "FY2019": 489847, "FY2018": 105920, "FY2017": 398877, "FY2016": 207610, "FY2015": 84697, "FY2014": -23721, "FY2013": 68213}),
    ("DATA", "Derivative liabilities", {"FY2025": 3085, "FY2024": -20896, "FY2023": 28536, "FY2022": 3409, "FY2021": -344, "FY2020": 99}),
    ("DATA", "Other liabilities", {"FY2025": 2517, "FY2024": 8019, "FY2023": 13796, "FY2022": 4916, "FY2021": -213, "FY2016": 11495, "FY2015": -97, "FY2014": -1903, "FY2013": 323}),
    ("DATA", "Other liabilities and provision for customer redress (combined, as reported)", {"FY2020": -4128, "FY2019": -8240, "FY2018": -29349, "FY2017": 27381}),
    ("DATA", "Accrued expenses", {"FY2022": 1290, "FY2021": 8305, "FY2020": 3329, "FY2019": 2908, "FY2018": 1024, "FY2017": 2627, "FY2016": 666, "FY2015": 1099, "FY2014": 295, "FY2013": -675}),
    ("TOTAL", "Net cash flow generated from/(used in) operating activities", {"FY2025": -17143, "FY2024": 445559, "FY2023": 130953, "FY2022": 190786, "FY2021": 234303, "FY2020": 117909, "FY2019": -83910, "FY2018": -157299, "FY2017": 75543, "FY2016": -44784, "FY2015": -108406, "FY2014": -85437, "FY2013": 140235}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property and equipment", {"FY2025": -204, "FY2024": -398, "FY2023": -3343, "FY2022": -877, "FY2021": -72, "FY2020": -230, "FY2019": -387, "FY2018": -1281, "FY2017": -268, "FY2016": -380, "FY2015": -178, "FY2014": -227, "FY2013": -195}),
    ("DATA", "Purchase of intangible assets", {"FY2025": -25325, "FY2024": -21721, "FY2023": -27176, "FY2022": -6048, "FY2021": -9230, "FY2020": -12992, "FY2019": -8400, "FY2018": -1366, "FY2017": -1352, "FY2016": -654, "FY2015": -364, "FY2014": -539, "FY2013": -414}),
    ("DATA", "Purchase of asset-backed/debt securities", {"FY2025": -484349, "FY2024": -149500, "FY2023": -76396}),
    ("DATA", "Redemption of asset-backed/debt securities", {"FY2025": 26952, "FY2024": 35836, "FY2023": 67893}),
    ("DATA", "Redemption/(purchase) of asset-backed securities (combined, as reported)", {"FY2022": 26975, "FY2021": -137782}),
    ("DATA", "Interest received on asset-backed securities", {"FY2025": 17692}),
    ("DATA", "Proceeds of sale of investment", {"FY2018": 390}),
    ("DATA", "Proceeds from sale of property", {"FY2025": 5904, "FY2022": 16370, "FY2020": 531}),
    ("TOTAL", "Net cash flow generated from/(used in) investing activities", {"FY2025": -459330, "FY2024": -135783, "FY2023": -39022, "FY2022": 36420, "FY2021": -147084, "FY2020": -12691, "FY2019": -8787, "FY2018": -2257, "FY2017": -1620, "FY2016": -1034, "FY2015": -542, "FY2014": -766, "FY2013": -609}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Proceeds from issuance of new share capital", {"FY2022": 47000, "FY2020": 9000, "FY2019": 15000, "FY2018": 20000, "FY2017": 16000}),
    ("DATA", "Proceeds from issuance of subordinated loan(s)", {"FY2025": 35000, "FY2023": 14826, "FY2017": 29464}),
    ("DATA", "(Decrease)/increase in subordinated loan", {"FY2018": -43}),
    ("DATA", "Capital repayment from finance lease obligations", {"FY2025": -1487, "FY2024": -2292, "FY2023": -1125, "FY2022": 34, "FY2021": -238, "FY2020": -166, "FY2019": -58}),
    ("DATA", "Interest paid on subordinated loan(s)", {"FY2025": -4032, "FY2017": -938, "FY2016": -2265, "FY2015": -2271, "FY2014": -2256, "FY2013": -3429}),
    ("DATA", "Dividend paid", {"FY2019": -300}),
    ("TOTAL", "Net cash flow generated from/(used in) financing activities", {"FY2025": 29481, "FY2024": -2292, "FY2023": 13701, "FY2022": 47034, "FY2021": -238, "FY2020": 8834, "FY2019": 14642, "FY2018": 19957, "FY2017": 44526, "FY2016": -2265, "FY2015": -2271, "FY2014": -2256, "FY2013": -3429}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents for the year", {"FY2025": -446992, "FY2024": 307484, "FY2023": 105632, "FY2022": 274240, "FY2021": 86981, "FY2020": 114052, "FY2019": -78055, "FY2018": -139599, "FY2017": 118449, "FY2016": -48083, "FY2015": -111119, "FY2014": -88459, "FY2013": 136197}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {"FY2025": 1058851, "FY2024": 751598, "FY2023": 646528, "FY2022": 372288, "FY2021": 285307, "FY2020": 171255, "FY2019": 249310, "FY2018": 388909, "FY2017": 268981, "FY2016": 308796, "FY2015": 422348, "FY2014": 511643, "FY2013": 374506}),
    ("DATA", "Effects of exchange rate changes on cash and cash equivalents", {"FY2025": 44, "FY2024": -231, "FY2023": -562, "FY2017": 1479, "FY2016": 8268, "FY2015": -1994, "FY2014": -836, "FY2013": 939}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2025": 611903, "FY2024": 1058851, "FY2023": 751598, "FY2022": 646528, "FY2021": 372288, "FY2020": 285307, "FY2019": 171255, "FY2018": 249310, "FY2017": 388909, "FY2016": 268981, "FY2015": 309135, "FY2014": 422348, "FY2013": 511643}),
]

bw.add_cash_flow_sheet(
    title="Cynergy Bank Plc — Consolidated and Company Statement of Cash Flows",
    subtitle="Consolidated basis, £'000. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=80,
    source_height=260,
    unit_suffix=" (£'000)",
    years=YEARS,
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Gross carrying amount by IFRS 9 stage (Loans + Overdrafts; Consolidated FY2018-2025, Company-only FY2018 per that year's own report)", {}),
    ("DATA", "Stage 1 gross carrying amount",
     {"FY2025": 3423245, "FY2024": 3210782, "FY2023": 2968247, "FY2022": 2826161, "FY2021": 2687050,
      "FY2020": 2409575, "FY2019": 2169994, "FY2018": 1576985}),
    ("DATA", "Stage 2 gross carrying amount",
     {"FY2025": 259276, "FY2024": 372480, "FY2023": 549578, "FY2022": 385150, "FY2021": 232788,
      "FY2020": 187845, "FY2019": 78327, "FY2018": 75151}),
    ("DATA", "Stage 3 gross carrying amount",
     {"FY2025": 91016, "FY2024": 99046, "FY2023": 73262, "FY2022": 65258, "FY2021": 43661,
      "FY2020": 25089, "FY2019": 19800, "FY2018": 20333}),
    ("TOTAL", "Total gross carrying amount",
     {"FY2025": 3773537, "FY2024": 3682308, "FY2023": 3591087, "FY2022": 3276569, "FY2021": 2963499,
      "FY2020": 2622509, "FY2019": 2268121, "FY2018": 1672469}),
    ("SECTION", "Expected credit loss (ECL) allowance by stage", {}),
    ("DATA", "Stage 1 ECL", {"FY2025": 3964, "FY2024": 4403, "FY2023": 5372, "FY2022": 3338, "FY2021": 2124,
                             "FY2020": 3956, "FY2019": 1912, "FY2018": 1443}),
    ("DATA", "Stage 2 ECL", {"FY2025": 2951, "FY2024": 4118, "FY2023": 8485, "FY2022": 5321, "FY2021": 2175,
                             "FY2020": 3117, "FY2019": 326, "FY2018": 349}),
    ("DATA", "Stage 3 ECL", {"FY2025": 21489, "FY2024": 20310, "FY2023": 12933, "FY2022": 13680, "FY2021": 9626,
                             "FY2020": 1474, "FY2019": 1502, "FY2018": 1754}),
    ("TOTAL", "Total ECL allowance",
     {"FY2025": 28404, "FY2024": 28831, "FY2023": 26790, "FY2022": 22339, "FY2021": 13925,
      "FY2020": 8547, "FY2019": 3740, "FY2018": 3546}),
    ("SECTION", "Derived ratios (IFRS 9 basis)", {}),
    ("DATA", "Stage 3 / total gross carrying amount",
     {"FY2025": "2.412%", "FY2024": "2.690%", "FY2023": "2.040%", "FY2022": "1.992%", "FY2021": "1.473%",
      "FY2020": "0.957%", "FY2019": "0.873%", "FY2018": "1.216%"}),
    ("DATA", "Total ECL / total gross carrying amount (overall coverage)",
     {"FY2025": "0.753%", "FY2024": "0.783%", "FY2023": "0.746%", "FY2022": "0.682%", "FY2021": "0.470%",
      "FY2020": "0.326%", "FY2019": "0.165%", "FY2018": "0.212%"}),
    ("DATA", "Stage 3 ECL / Stage 3 gross carrying amount (Stage 3 coverage)",
     {"FY2025": "23.61%", "FY2024": "20.51%", "FY2023": "17.65%", "FY2022": "20.96%", "FY2021": "22.05%",
      "FY2020": "5.876%", "FY2019": "7.586%", "FY2018": "8.626%"}),

    ("SECTION", "Legacy IAS 39 basis (FY2014-FY2017, Bank of Cyprus UK Limited, Company-only) - "
                "credit quality of gross loans and advances to customers (Loans + Overdrafts combined)", {}),
    ("DATA", "Gross loans and advances",
     {"FY2017": 1411255, "FY2016": 1088298, "FY2015": 827016, "FY2014": 629744}),
    ("DATA", "Provisions for impairment of loans and advances (individual + collective, IAS 39 incurred-loss basis)",
     {"FY2017": -4055, "FY2016": -4376, "FY2015": -6209, "FY2014": -11768}),
    ("TOTAL", "Net loans and advances to customers",
     {"FY2017": 1407200, "FY2016": 1083922, "FY2015": 820807, "FY2014": 617976}),
    ("DATA", "Neither past due nor impaired",
     {"FY2017": 1373534, "FY2016": 1064883, "FY2015": 797582, "FY2014": 579666}),
    ("DATA", "Past due but not impaired",
     {"FY2017": 34850, "FY2016": 18330, "FY2015": 19698, "FY2014": 33370}),
    ("DATA", "Impaired",
     {"FY2017": 2871, "FY2016": 5085, "FY2015": 9736, "FY2014": 16708}),
    ("TOTAL", "Total gross loans and advances (credit-quality analysis)",
     {"FY2017": 1411255, "FY2016": 1088298, "FY2015": 827016, "FY2014": 629744}),
    ("SECTION", "Ageing of past due but not impaired loans and advances (Legacy IAS 39 basis)", {}),
    ("DATA", "Up to 30 days", {"FY2017": 21107, "FY2016": 10818, "FY2015": 8258, "FY2014": 18716}),
    ("DATA", "31 to 90 days", {"FY2017": 6475, "FY2016": 311, "FY2015": 2768, "FY2014": 3494}),
    ("DATA", "91 to 180 days", {"FY2017": 2823, "FY2016": 2752, "FY2015": 1558, "FY2014": 1247}),
    ("DATA", "181 to 365 days", {"FY2017": 2910, "FY2016": 546, "FY2015": 649, "FY2014": 2118}),
    ("DATA", "Over one year", {"FY2017": 1535, "FY2016": 3903, "FY2015": 6465, "FY2014": 7795}),
    ("SECTION", "Derived ratios (Legacy IAS 39 basis)", {}),
    ("DATA", "Impaired / total gross loans and advances",
     {"FY2017": "0.203%", "FY2016": "0.467%", "FY2015": "1.177%", "FY2014": "2.653%"}),
    ("DATA", "Total provisions / total gross loans and advances (overall coverage)",
     {"FY2017": "0.287%", "FY2016": "0.402%", "FY2015": "0.751%", "FY2014": "1.869%"}),
]

ASSET_QUALITY_LEGACY_NOTE = (
    "HD-051 note: FY2014-FY2017 predate IFRS 9 (effective 1 Jan 2018) and use the IAS 39 incurred-loss "
    "framework instead of the IFRS 9 expected-credit-loss stage model used from FY2018 onward - these years "
    "are shown in a separate 'Legacy IAS 39 basis' section using that era's own terminology ('neither past "
    "due nor impaired' / 'past due but not impaired' / 'impaired', with an arrears-ageing analysis of the "
    "past-due-but-not-impaired category), not forced into the Stage 1/2/3 framework, and not skipped. "
    "Figures are Bank of Cyprus UK Limited's own Company-only (non-consolidated) Loans and advances to "
    "customers note (Loans + Overdrafts columns summed) for each year's own Annual Report - same Companies "
    "House filings already used for the Balance Sheet/P&L/Cash Flow sheets, re-read for this note specifically "
    "(no new documents sourced). FY2018 is the first year presented under IFRS 9's Stage 1/2/3 model (Cynergy "
    "Bank Limited's own FY2018 Annual Report note 17 already discloses the gross-carrying and ECL tables by "
    "stage, individual/collective-split that first year only) and is included directly in the IFRS 9 section "
    "above, not as a separate transitional block - no further transitional treatment was needed because the "
    "FY2018 report itself already presents the post-transition Stage 1/2/3 basis in full.\n"
    "FY2019 Stage 2 ECL is a balancing figure, not a direct transcription: the FY2019 Annual Report's "
    "Overdrafts ECL movement table (scanned filing) was faint enough that its own reported per-stage 'Total' "
    "row (£110k) did not sum from its own individually-legible Stage 1/2/3 cells (£31k/£40k/£69k = £140k, not "
    "£110k) - rather than transcribe an internally-inconsistent reading, the Overdrafts Stage 2 figure is "
    "backed out as £110k - £31k - £69k = £10k so that the combined Stage 1/2/3 ECL ties exactly to the "
    "report's own disclosed combined total of £3,740k; this affects only the Stage 2 ECL split, not any "
    "total."
)

bw.add_asset_quality_sheet(
    title="Cynergy Bank Plc — Asset Quality",
    subtitle="Consolidated (Company-only FY2014-2017) basis, £'000 (ratios as calculated), combining the "
              "Loans and Overdrafts credit risk note tables. Two methodology sections - see source note at "
              "bottom.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES + "\n\n" + ASSET_QUALITY_LEGACY_NOTE,
    first_col_width=60,
    source_height=420,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
NOT_DISCLOSED_NOTE = (
    "Not publicly disclosed. Cynergy Bank's Annual Reports discuss capital/liquidity/funding risk only "
    "qualitatively (e.g. 'we held surplus regulatory capital', 'the liquidity coverage ratio has exceeded "
    "the regulatory requirements') with no £ or % figures stated in any year reviewed for this metric, and "
    "no standalone Pillar 3 document was found on the bank's own site. MREL in particular is not a metric "
    "Cynergy Bank has ever disclosed, in any year or any document reviewed, including the 2018-2022 Pillar 3 "
    "editions. For FY2024/FY2025 the SDDT exemption below removes the Pillar 3 obligation entirely."
)

SDDT_NOTE = (
    "WHY PILLAR 3 DATA STOPS AFTER FY2022 - A DOCUMENTED STRUCTURAL REASON, not a sourcing failure (the "
    "capital AMOUNTS on the CET1/Tier 1/Total Capital sheets continue because the Annual Report's own "
    "capital-management note states them; every ratio, RWA, leverage and liquidity metric stops because only "
    "a Pillar 3 document ever carried them). Cynergy Bank's "
    "modification-by-consent application to be treated as a Small Domestic Deposit Taker (SDDT) was approved "
    "on 17 January 2025, and the Bank states in its own Annual Reports that it is consequently 'not required "
    "to publish Pillar 3 disclosures as at 31 December 2024' (AR2024 p.71) and 'no longer required to publish "
    "Pillar 3 disclosures for the period ended 31 December 2025' (AR2025 p.45). There is therefore no Pillar 3 "
    "document to find for either year. FY2023 predates that approval and its Pillar 3 disclosure was still "
    "required (the FY2023 Annual Report's own Board Risk Committee agenda, p.43, lists 'Pillar 3 disclosure' "
    "among the items reviewed during the year) - but the 2018-2022 editions' /media/ hosting was decommissioned "
    "when the site moved to Contentful during 2024 and no FY2023 edition is reachable anywhere, live or "
    "archived. See this sheet's source note for the full evidence and the exact quotations."
)

NSFR_SDDT_NOTE = (
    SDDT_NOTE
    + " NSFR SPECIFICALLY: the SDDT approval does not merely stop publication of this metric, it replaces it. "
    "AR2024 p.71 says the Bank 'will submit only a simplified retail deposit ratio instead of a full Net "
    "Stable Funding Ratio (NSFR) going forward', and AR2025 p.45 confirms 'the Simplified Retail Deposit Ratio "
    "(SRDR) replacing the full Net Stable Funding Ratio (NSFR) requirement'. From FY2025 the Bank does not "
    "report a full NSFR at all, so no figure exists to disclose - the blank is the correct answer, not a gap."
)

FY25_CAP = (
    "\n\nFY2025 (added 2026-09-15) is the Annual Report & Accounts 2025's own Note 32 'Capital management' "
    "capital-resources table, p.85 (Consolidated column), the same note and table this sheet already uses for "
    "FY2024 and FY2023. That table's FY2024 comparative column reproduces FY2024's own reported figures "
    "exactly, so there is no restatement to reconcile."
)

FY24_RATIO = (
    "\n\nFY2024 (added 2026-09-15) is the Annual Report & Accounts 2024's own narrative figure (p.6: 'The "
    "common equity tier 1 (CET1) ratio remains stable at 13.59%'), the only capital or liquidity ratio stated "
    "numerically anywhere in the FY2023-FY2025 Annual Reports. It is carried onto the Tier 1 Ratio sheet too "
    "because the Bank's own capital table labels its Tier 1 line 'Total eligible tier 1 capital (CET1)' - the "
    "source itself asserts Tier 1 = CET1, with no Additional Tier 1 in issue; that is the source's identity, "
    "not a derivation by this workbook. FY2023 and FY2025 state no equivalent figure - their narrative is "
    "purely qualitative - so they stay blank."
)

TIER1_NOTE = (
    "Cynergy Bank's own Annual Report labels this line 'Total eligible Tier 1 capital (CET1)' - i.e. it "
    "states Tier 1 capital and CET1 capital are identical (no Additional Tier 1 instruments in issue) - see "
    "the CET1 Capital sheet for the same figures and source."
)

def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, f"Consolidated basis, {unit}" if unit else "Consolidated basis",
                         rows_data, p3_sources(), note=note, first_col_width=52, source_height=170)


P3_2021_2022_NOTE = (
    "FY2022 and FY2021 were recovered on 2026-09-12 from Cynergy Bank's own standalone Pillar 3 "
    "documents, which are no longer linked from the live cynergybank.co.uk site but are archived in "
    "full on the Wayback Machine (see the sources note). The prior claim that no standalone Pillar 3 "
    "document existed for this bank was incorrect - editions for 2018, 2019, 2020, 2021 and 2022 are "
    "all archived. FY2021 figures are taken from the 2022 edition's own FY2021 comparative column, "
    "which restates them at full precision; the 2021 edition's own rounded figures agree (CET1 £197m, "
    "Total capital £227m, RWAs £1,417m, CET1 ratio 13.9%, Total capital ratio 16.0%, leverage 5.5%, "
    "LCR 243%)."
)

FY2023_P3_NOTE = (
    "FY2023 was filled on 2026-09-15 from Cynergy Bank's own 2023 Pillar 3 Disclosures (UK KM1 table, "
    "p.7), a document two earlier passes of this script had concluded did not exist or could not be "
    "reached. It does exist and is live on the Bank's site - linked only from "
    "/strong-and-prudent-management, which is the single page neither earlier pass checked. The full "
    "correction, including why each earlier negative result was individually accurate and collectively "
    "wrong, is in this sheet's Sources note.\n"
    "VALIDATION GATE PASSED: this document's FY2022 comparative column reproduces the FY2022 figures "
    "already in this workbook exactly - CET1/Tier 1 capital 287,447, Total capital 287,447, Total RWAs "
    "1,822,159, CET1/Tier 1/Total capital ratio 15.78%, leverage ratio 7.40% - and its CC1 table "
    "independently confirms the FY2023 capital amounts already carried here from AR2024's Note 32 "
    "(CET1 306,251, Total capital 321,251). No existing figure was overwritten."
)

FY2023_RESTATEMENT_NOTE = (
    "TWO FY2022 LIQUIDITY FIGURES ARE NOT RECONCILED, DELIBERATELY. The 2023 Pillar 3 edition's FY2022 "
    "comparative column disagrees with the 2022 edition's own FY2022 column on the liquidity metrics "
    "only - LCR 249.66% (2023 edition) vs 315.98% (2022 edition), and NSFR 144.09% vs 149.48% - with "
    "the underlying components restated too (FY2022 HQLA 525,228 vs 602,317; net outflows 212,745 vs "
    "190,621; available stable funding 3,546,316 vs 3,721,028). Both editions label the LCR inputs the "
    "same way ('Weighted value - average'), so this is not the average-vs-point-in-time basis trap; it "
    "is a genuine restatement by the Bank between editions. Every capital, RWA and leverage figure in "
    "the same two columns agrees exactly, which is what makes the liquidity divergence conspicuous. "
    "Per this project's standing convention each year keeps its own edition's figure, so FY2022 retains "
    "315.98% / 149.48% and the divergence is recorded here rather than silently resolved."
)

FY2017_RWA_CAVEAT = (
    "FY2017 Total Capital (£139,447k) and Total RWAs (£663,552k) ARE DIRECTLY DISCLOSED, and were filled on "
    "2026-09-18. Both are printed, in those words and to the pound, in the FY2017 column of 'Appendix 1 - "
    "Own Funds Disclosure' on printed p.13 of the Cynergy Bank Pillar 3 Disclosures 2018. That appendix "
    "gives the whole FY2017 stack: CET1 capital before regulatory adjustments 112,718, less intangibles "
    "(2,408) and a significant-investment deduction (400), giving CET1 = Tier 1 = 109,910; Tier 2 capital "
    "29,537; TOTAL CAPITAL 139,447; TOTAL RISK WEIGHTED ASSETS 663,552; and the ratios 16.6% / 16.6% / "
    "21.0%. Everything foots: 109,910 + 29,537 = 139,447, 109,910 / 663,552 = 16.56% and 139,447 / 663,552 "
    "= 21.01%, matching the printed ratios and the CET1 figure this workbook already carried for FY2017.\n"
    "WHAT THIS REPLACES, KEPT VISIBLE BECAUSE IT IS INSTRUCTIVE. The note here used to state that the FY2018 "
    "Pillar 3's FY2017 comparative 'never states a Total Capital £ amount or a Total RWA £ amount directly', "
    "and then reasoned at length about why back-solving from the ratios was unsafe - concluding, correctly "
    "on its own premise, that the cells must stay blank. The premise was false. The figures are in the same "
    "document, six pages after the credit-risk table that reasoning was built on, in the appendix that "
    "exists precisely to state them. The elaborate argument against deriving a number was, in the end, an "
    "argument for reading further into the document. Note in passing that it also came close to the right "
    "answer and rejected it: its '~£662m assuming CET1 ratio alone pins down RWA' is £663.55m.\n"
    "A SECOND, GENUINELY DIFFERENT FY2017 CAPITAL FIGURE EXISTS and is deliberately NOT used here. Bank of "
    "Cyprus UK Limited's own FY2017 Annual Report (Companies House, filed 29 May 2018; an image-only scan, "
    "OCR'd at 200 dpi on 2026-09-18) carries a 'Composition of regulatory capital and ratios (Unaudited)' "
    "table in the Strategic Report giving Core Tier 1 111,095, qualifying Tier 2 of 29,537 subordinated "
    "loan PLUS 2,451 of collective provisions, Total regulatory capital 143,083, Core tier 1 ratio 16.5%, "
    "Total capital ratio 21.4% and leverage 6.0%. That is £3,636k more capital than the Pillar 3 figure, "
    "because it counts collective provisions in Tier 2 and applies a smaller intangibles deduction (1,623 "
    "vs 2,408) and no significant-investment deduction. The Pillar 3 basis is used on these sheets because "
    "it is the basis every FY2018-FY2023 year already uses and the basis the FY2017 CET1 and ratio cells "
    "already carried; the Annual Report basis is recorded here so the £143,083 / 21.4% pair is recognised "
    "if it is met again rather than treated as a contradiction.\n"
    "FY2017 RWA BREAKDOWN is a separate question and is only partly answered - see that sheet."
)

DERIVED_RWA_FLAG = (
    "FY2018 CORRECTED 2026-09-18, from a derived £796,565k to the DISCLOSED £794,959k. The line below lists "
    "FY2018 among the years derived as Total Capital / Total Capital ratio. It did not need to be: 'Appendix "
    "1 - Own Funds Disclosure' prints 'Total risk weighted assets 794,959' for 2018 outright, on printed "
    "p.13 of the 2018 edition, and the 2019 edition's own 2018 comparative prints the same 794,959 - two "
    "independent printings agreeing to the pound against a derivation that was £1.6m out. The same appendix "
    "is what supplied FY2017 above. No figure was adjusted to satisfy a checker; a derivation was replaced "
    "by the source it was standing in for.\n"
    "STILL DERIVED, AND STILL FLAGGED: FY2016. Bank of Cyprus UK's FY2016 Annual Report was re-downloaded "
    "and OCR'd in full on 2026-09-18 (44 pages, image-only scan) and states no risk-weighted-asset amount "
    "anywhere - its note 30 capital table gives Core Tier 1 65,017, Total regulatory capital 96,777, Tier 1 "
    "ratio 12.1%, Total capital ratio 18.2% and leverage 4.7%, and the Strategic Report says only 'total "
    "capital standing at 18.2% of risk weighted assets'. 96,777 / 0.182 = 531,742.0 exactly, which is this "
    "sheet's FY2016 figure to the pound, so the derivation is confirmed as such rather than merely declared. "
    "It is left in place, because it is disclosed as derived rather than passed off as printed, but a ratio "
    "quoted to one decimal place cannot pin RWA to six significant figures and the figure should not be "
    "treated as precise. FY2015 and FY2014 do not reproduce under the same test (101,139 / 0.244 = 414,504 "
    "against a stated 416,813; 98,022 / 0.254 = 385,913 against 385,638), so a different route produced "
    "those two.\n"
    "SEPARATELY FLAGGED, NOT CHANGED (out of this pass's scope, and the discrepancy is small but real): the "
    "Total Capital sheet carries £165,416k for FY2018 and £186,465k for FY2019, while the 2018 and 2019 "
    "Pillar 3 Own Funds appendices both print 164,940 for 2018 and the 2019 edition prints 186,464 for "
    "2019. A £476k gap on FY2018 and £1k on FY2019. Whoever revisits this should find which table the "
    "workbook's figures came from before changing anything."
)

# ---------------------------------------------------------------
# KM1 Key Metrics - Cynergy's own published key-metrics table, reproduced as
# printed (KM1-012).
#
# WHICH YEARS EXIST AT ALL. Cynergy publishes a UK KM1 table in exactly two
# editions: the 2023 Pillar 3 (whose contents page names it "Key metrics table
# (UK KM1)") and the 2022 Pillar 3 (headed only "Key metrics"). Neither prints
# the template's row NUMBERS, so a presence test keyed on "UK 7a" or on a bare
# leading "1" reports nothing here - the row labels, order and section headings
# are the template line for line, which is what identifies it.
#   - FY2023 and FY2022 each come from the edition in which that year is the
#     reporting year.
#   - FY2021 is the FY2022 edition's comparative column. The 2021 Pillar 3's
#     own table (p.20, "Key capital, liquidity and leverage metrics", £m) is a
#     much narrower pre-KM1 disclosure - nine rows, no SREP/buffer/NSFR/HQLA
#     sections, and "risk-weighted assets" rather than the template's
#     "risk-weighted exposure amount" - so it is NOT the KM1 template and is
#     not transcribed here as one.
#   - FY2020 and earlier predate the template; FY2024 and FY2025 postdate
#     Cynergy's SDDT approval (17 January 2025), after which it is not required
#     to publish Pillar 3 at all. Both absences are enumerated, not unfound -
#     see ENUMERATION_NOTE and p3_sources().
#
# UNIT BREAK BETWEEN EDITIONS - the reason this sheet's amount rows are not one
# unit down a row. The 2023 edition states "All amounts are presented rounded to
# the nearest thousand except where stated" and prints CET1 as 306,251. The 2022
# edition prints the SAME kind of row in WHOLE POUNDS (287,446,662) and states
# no unit anywhere on or above the table. Each cell is transcribed from the
# edition in which that year is the reporting year, exactly as printed, so
# FY2023 amounts are £'000 and FY2022/FY2021 amounts are £. They are not
# rescaled onto a common unit: rescaling is the one thing this sheet may not do,
# and the £'000 equivalents are in any case already on the individual metric
# sheets.
#
# HOW THAT IS EXPRESSED HERE (map rule 17, and the same shape rule 5 uses for
# the 1 Jan 2022 leverage basis break): each amount row is printed TWICE, as two
# adjacent caption blocks, one per unit - a "(£'000 ...)" row carrying the FY2023
# column and a "(£ ...)" row carrying the FY2022/FY2021 columns. Neither series
# is merged into the other and nothing is restated. This is a presentation of the
# Bank's 24 published rows, NOT 35 disclosed rows: the two captions of a pair are
# the same template row read out of two editions that printed it in two units.
# The earlier single-row form, which named both units inside one label, is what
# verify_workbook.py has to refuse to cross-check (one row, one scale); split
# this way every amount cell is checked against its metric sheet automatically.
# Ratio rows are unaffected - they are percentages in both editions.
# ---------------------------------------------------------------
# Unit captions. Deliberately worded WITHOUT "FY20xx" tokens: a label naming a
# year beside a currency is how verify_workbook.py detects a row that declares
# more than one unit, which is exactly the state this split exists to leave.
_K = " (£'000 — the 2023 edition's own stated unit)"
_P = " (£ — whole pounds, as the 2022 edition prints it; that edition states no unit at all)"

km1_rows = [
    # GA-006 (2026-09-18): the FY2024 and FY2025 columns carried no cell at all,
    # so a reader opening this sheet saw two blank year columns and the census
    # scored them as gaps - even though the reason is established and quoted in
    # the sources note below (SDDT approval 17 January 2025; the Bank says so in
    # both Annual Reports, the PRA register carries the matching Rule 3.1 row,
    # and its own disclosures page still lists six Pillar 3 editions, FY2018-
    # FY2023, and none later - re-checked live 2026-09-18). The statement now
    # appears IN those columns. Nothing is computed, reordered or restated; this
    # is a statement row, not a template row, and it is labelled as such so the
    # KM1/metric-sheet cross-check does not resolve it to any metric sheet.
    ("DATA", "[No UK KM1 published for this year - see note below]",
     {"FY2025": "Not required - SDDT, no Pillar 3 published",
      "FY2024": "Not required - SDDT, no Pillar 3 published"}),
    ("SECTION", "Available own funds (amounts)", {}),
    ("DATA", "Common Equity Tier 1 (CET1) capital" + _K, {"FY2023": 306251}),
    ("DATA", "Common Equity Tier 1 (CET1) capital" + _P,
     {"FY2022": "287,446,662", "FY2021": "197,331,379"}),
    ("DATA", "Tier 1 capital" + _K, {"FY2023": 306251}),
    ("DATA", "Tier 1 capital" + _P,
     {"FY2022": "287,446,662", "FY2021": "197,331,379"}),
    ("DATA", "Total capital" + _K, {"FY2023": 321251}),
    ("DATA", "Total capital" + _P,
     {"FY2022": "287,446,662", "FY2021": "227,199,733"}),
    ("SECTION", "Risk-weighted exposure amounts", {}),
    ("DATA", "Total risk-weighted exposure amount" + _K, {"FY2023": 2084246}),
    ("DATA", "Total risk-weighted exposure amount" + _P,
     {"FY2022": "1,822,159,262", "FY2021": "1,417,122,603"}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "Common Equity Tier 1 ratio (%)",
     {"FY2023": "14.69%", "FY2022": "15.78%", "FY2021": "13.92%"}),
    ("DATA", "Tier 1 ratio (%)",
     {"FY2023": "14.69%", "FY2022": "15.78%", "FY2021": "13.92%"}),
    ("DATA", "Total capital ratio (%)",
     {"FY2023": "15.41%", "FY2022": "15.78%", "FY2021": "16.03%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "Additional CET1 SREP requirements (%)",
     {"FY2023": "0.00%", "FY2022": "0.50%", "FY2021": "1.06%"}),
    ("DATA", "Total SREP own funds requirements (%)",
     {"FY2023": "8.51%", "FY2022": "9.60%", "FY2021": "9.60%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "Capital conservation buffer (%)",
     {"FY2023": "2.50%", "FY2022": "2.50%", "FY2021": "2.50%"}),
    ("DATA", "Institution specific countercyclical capital buffer (%)",
     {"FY2023": "2.00%", "FY2022": "1%", "FY2021": "0%"}),
    ("DATA", "Combined buffer requirement (%)",
     {"FY2023": "4.50%", "FY2022": "3.50%", "FY2021": "2.50%"}),
    ("DATA", "Overall capital requirements (%)",
     {"FY2023": "13.01%", "FY2022": "13.60%", "FY2021": "13.16%"}),
    ("DATA", "CET1 available after meeting the total SREP own funds requirements (%)",
     {"FY2023": "6.18%", "FY2022": "5.66%", "FY2021": "3.26%"}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "Leverage ratio total exposure measure" + _K, {"FY2023": 4398669}),
    ("DATA", "Leverage ratio total exposure measure" + _P,
     {"FY2022": "3,886,578,610", "FY2021": "3,611,450,020"}),
    ("DATA", "Leverage ratio",
     {"FY2023": "6.96%", "FY2022": "7.40%", "FY2021": "5.46%"}),
    ("SECTION", "Liquidity Coverage Ratio", {}),
    ("DATA", "Total high-quality liquid assets (HQLA) (Weighted value - average)" + _K,
     {"FY2023": 714224}),
    ("DATA", "Total high-quality liquid assets (HQLA) (Weighted value - average)" + _P,
     {"FY2022": "602,316,820", "FY2021": "395,795,983"}),
    ("DATA", "Cash outflows - Total weighted value" + _K, {"FY2023": 364374}),
    ("DATA", "Cash outflows - Total weighted value" + _P,
     {"FY2022": "353,365,211", "FY2021": "250,909,201"}),
    ("DATA", "Cash inflows - Total weighted value" + _K, {"FY2023": 129561}),
    ("DATA", "Cash inflows - Total weighted value" + _P,
     {"FY2022": "162,744,676", "FY2021": "97,008,515"}),
    ("DATA", "Total net cash outflows (adjusted value)" + _K, {"FY2023": 234813}),
    ("DATA", "Total net cash outflows (adjusted value)" + _P,
     {"FY2022": "190,620,534", "FY2021": "153,900,686"}),
    ("DATA", "Liquidity coverage ratio (%)",
     {"FY2023": "304.44%", "FY2022": "315.98%", "FY2021": "242.91%"}),
    ("SECTION", "Net Stable Funding Ratio", {}),
    # DASH RULE, applied 2026-09-18 (GA-006, on the user's reversal of KM1 map
    # rule 2): the 2022 edition prints a literal "-" in all THREE NSFR rows of
    # its FY2021 comparative column, and a dash is the Bank saying the row does
    # not apply to it - a different statement from silence. Those three cells
    # were previously BLANKED under the old rule; they now carry "-" as printed.
    # Verified against the source PDF itself, not against the note that claimed
    # it: cynergy-bank-2022-pillar-3-disclosures.pdf, "Key metrics" p.5 (printed
    # PAGE 5), re-read 2026-09-18. Those three are the ONLY dash cells in that
    # table - every other FY2022/FY2021 cell prints a figure - and the 2023
    # edition's KM1 prints no dash in either of its columns.
    ("DATA", "Total available stable funding" + _K, {"FY2023": 3903341}),
    ("DATA", "Total available stable funding" + _P, {"FY2022": "3,721,028,413", "FY2021": "-"}),
    ("DATA", "Total required stable funding" + _K, {"FY2023": 2625631}),
    ("DATA", "Total required stable funding" + _P, {"FY2022": "2,489,263,786", "FY2021": "-"}),
    ("DATA", "NSFR ratio (%)",
     {"FY2023": "148.67%", "FY2022": "149.48%", "FY2021": "-"}),
]

KM1_SOURCES = (
    "Sources - Cynergy Bank's own published key-metrics (UK KM1) table, Consolidated Bank basis, "
    "reproduced as printed:\n"
    f"FY2023 (own column) and the FY2022 comparative (NOT used - see the restatement note below): "
    f"Cynergy Bank Limited 2023 Pillar 3 Disclosures, 'Key metrics', p.7. The document's own contents "
    f"page names this table 'Key metrics table (UK KM1)'. Columns: '31-Dec-23' and '31-Dec-22' - "
    f"{P3_2023_URL}\n"
    f"FY2022 (own column) and FY2021 (comparative column): Cynergy Bank Limited - 2022 Pillar 3, "
    f"'Key metrics', p.6 (printed 'PAGE 6'). Columns: '31 Dec 2022' and '31 Dec 2021' - {P3_2022_URL} "
    f"(delisted from the live site; the identical copy on the Bank's current Contentful CDN was used: "
    f"{P3_2022_CDN_URL} , and the archived copy {P3_2022_WAYBACK} agrees)\n\n"
    "PRESENTATION NOTES, all of them things the Bank did rather than choices made here:\n"
    "* NO TEMPLATE ROW NUMBERS. Neither edition prints the template's row numbers ('1', 'UK 7a', '11a' "
    "...). The row labels, their order and the section headings are the UK KM1 template line for line, "
    "which is what identifies the table; the numbers are simply absent from the source and are not "
    "added here.\n"
    "* EACH AMOUNT ROW IS PRINTED TWICE, one caption per unit, and that is a presentation of the Bank's "
    "24 published rows rather than 35 disclosed ones. Because the unit break falls between COLUMNS "
    "(editions) while a spreadsheet row can carry only one unit, each of the 11 amount rows appears as "
    "two adjacent rows: a \"(£'000 ...)\" caption carrying the FY2023 column, and a \"(£ — whole "
    "pounds ...)\" caption carrying FY2022/FY2021. The two captions of a pair are the SAME template row, "
    "read out of two editions that printed it in two different units; neither series is merged into the "
    "other and no figure is restated. This is the shape the KM1 map's rule 17 prescribes for a unit break "
    "between editions, and the same shape rule 5 uses for the 1 January 2022 leverage basis break. Ratio "
    "rows are single, because percentages are percentages in both editions.\n"
    "* REDUCED ROW SET. Both editions print the same 24 value rows. The template rows Cynergy omits "
    "entirely - UK 7b/7c/7d in part, UK 8a, UK 9a, 10, UK 10a, 14a-14e and the MREL block - are not "
    "shown as blank rows because the Bank does not print them at all; an omitted row and a row printed "
    "empty are different disclosures. Cynergy does print 'Additional CET1 SREP requirements (%)' and "
    "'Total SREP own funds requirements (%)' but not the AT1/T2 SREP split.\n"
    "* UNIT BREAK BETWEEN EDITIONS, the reason the amount rows above carry a per-year unit marker. The "
    "2023 edition says 'All amounts are presented rounded to the nearest thousand except where stated' "
    "and prints CET1 capital as 306,251. The 2022 edition prints the same row in WHOLE POUNDS "
    "(287,446,662) and states no unit at all, on or above the table. Each cell here is the figure the "
    "edition in which that year is the reporting year actually printed, so FY2023 amounts are £'000 and "
    "FY2022/FY2021 amounts are £. They are deliberately NOT rescaled onto one unit: this sheet "
    "reproduces a published template, and the £'000 equivalents for FY2022/FY2021 are already on the "
    "individual Pillar 3 metric sheets that follow (e.g. CET1 Capital FY2022 = 287,447). Percentage "
    "rows are unaffected.\n"
    "  DO NOT 'FIX' THIS. The four amount rows that also appear on a metric sheet (CET1 capital, Tier 1 "
    "capital, Total capital, Total risk-weighted exposure amount) look a thousand times too large in "
    "their \"(£ — whole pounds)\" caption beside those sheets. That is the Bank's own presentation, not "
    "an error: 287,446,662 / 1000 = 287,446.662 vs the metric sheet's 287,447, and 1,417,122,603 / 1000 "
    "= 1,417,122.603 vs 1,417,123 - each pair agrees to the rounding, which is itself the proof that the "
    "difference is the unit and not a digit slip. All four rows were re-read cell by cell off p.6 of the "
    "2022 edition on 2026-09-16 and are exactly as printed, as were the other seven amount rows. "
    "Rescaling them onto £'000 would make this sheet stop reproducing the disclosure. With the two-"
    "caption split above, verify_workbook.py resolves each cell's unit from its own row label and "
    "cross-checks all of them against the metric sheets automatically - they agree.\n"
    "* PRECISION AS PRINTED. The countercyclical buffer row is printed '2.00%' in the 2023 edition but "
    "'1%' and '0%' (no decimals) in the 2022 edition; '0%' is a printed zero and is kept as such.\n"
    "* A DASH IS NOT A ZERO, AND IS NOT A BLANK EITHER. The 2022 edition prints '-' in all three Net "
    "Stable Funding Ratio rows of its FY2021 comparative column - the Bank had no NSFR disclosure for "
    "2021 on this basis - so those three FY2021 cells carry the literal '-' the Bank printed. They are "
    "NOT zero, and they are NOT blank: a dash is the Bank stating the row does not apply to it, which is "
    "a different statement from silence. (Changed 2026-09-18, on the user's reversal of the earlier rule "
    "that blanked a printed dash; these three cells were blank until then. Re-read off p.5 of the 2022 "
    "edition on 2026-09-18 to confirm the dash rather than trusting the note that recorded it - and those "
    "three are the only dash cells in that table, while the 2023 edition's KM1 prints none at all.) The "
    "2021 edition's own narrative states an FY2021 NSFR of 130%, on its own different basis; that figure "
    "is on the NSFR sheet, not here.\n"
    "* FY2021 COMES FROM THE 2022 EDITION'S COMPARATIVE, not from its own year's document. The 2021 "
    "Pillar 3's own table (p.20, 'Key capital, liquidity and leverage metrics', columns '2021' and "
    "'2020', figures in £m) is a much narrower PRE-KM1 disclosure: nine value rows, no SREP, buffer, "
    "NSFR or HQLA sections at all, and captioned 'Total risk-weighted assets' rather than the "
    "template's 'Total risk-weighted exposure amount'. It is not the KM1 template and is not reproduced "
    "here as one. Its rounded figures do agree with the comparative used (CET1 £197m, Total capital "
    "£227m, RWAs £1,417m, CET1 ratio 13.9%, Total capital ratio 16.0%, leverage 5.5%, LCR 243%).\n\n"
    "WHY FY2024, FY2025 AND FY2020-FY2014 ARE BLANK - both ends are enumerated absences, not failed "
    "searches:\n"
    + ENUMERATION_NOTE
    + " Re-run independently on 2026-09-16 for this ticket with the same result: the page serves six "
      "Pillar 3 editions (FY2018, FY2019, FY2020, FY2021, FY2022, FY2023) and nothing later.\n"
    "At the older end, the FY2018, FY2019 and FY2020 editions contain no key-metrics table of any kind "
    "(the UK KM1 template arrives with the Disclosure (CRR) Part of the PRA Rulebook, which post-dates "
    "them), and FY2014-FY2017 predate standalone Pillar 3 publication by this entity altogether. Those "
    "years' individual capital and ratio figures, where the Bank disclosed them at all, are on the "
    "metric sheets that follow, sourced from narrative capital tables rather than from a KM1.\n\n"
    + FY2023_RESTATEMENT_NOTE
    + "\nThat restatement is visible on this sheet as a deliberate difference between what the 2023 "
      "edition shows in its FY2022 comparative column (LCR 249.66%, NSFR 144.09%, HQLA 525,228, net "
      "outflows 212,745, available stable funding 3,546,316, leverage exposure 3,886,759 - all £'000) "
      "and the FY2022 column reproduced above from the 2022 edition itself.\n\n"
    + SDDT_NOTE
)

bw.add_km1_sheet(
    title="Cynergy Bank Plc — KM1 Key Metrics",
    subtitle="The Bank's own published UK key-metrics (KM1) table, reproduced in Cynergy's row order and "
             "printed precision, Consolidated Bank basis. Cynergy prints this table in only two editions "
             "(2022 and 2023) and prints no template row numbers in either. AMOUNT ROWS ARE NOT ONE UNIT: "
             "the 2023 edition prints £'000, the 2022 edition whole pounds, and each year keeps its own "
             "edition's presentation, so every amount row appears TWICE - once captioned (£'000) carrying "
             "FY2023, once captioned (£) carrying FY2022/FY2021. Those pairs are the same published row in "
             "two units, not two disclosures, and nothing is rescaled. FY2024/FY2025 carry a statement "
             "rather than figures because Cynergy became an SDDT on 17 January 2025 and no longer "
             "publishes Pillar 3; FY2020 and earlier predate the template.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=72,
    source_height=300,
)

metric(
    "CET1 Capital", "£'000",
    [
        ("Total eligible Tier 1 capital (CET1)",
         {"FY2025": 348606, "FY2024": 321877, "FY2023": 306251, "FY2022": 287447, "FY2021": 197331,
          "FY2020": 182844, "FY2019": 156836, "FY2018": 135416, "FY2017": 109910}),
        ("Core Tier 1 capital (Basel II/CRD III era terminology; shown as the closest equivalent to CET1 - see note)",
         {"FY2016": 65017, "FY2015": 69180, "FY2014": 65533}),
    ],
    note=P3_2021_2022_NOTE + FY25_CAP + "\n\n" + SDDT_NOTE,
)

# GA-006 (2026-09-18): FY2024/FY2025 were left as EMPTY cells on every Pillar 3
# metric sheet, so the census scored 16 "leading gaps" against this bank even though
# the reason is fully established and quoted in the notes below (SDDT approval
# 17 January 2025 - the Bank says so itself in both Annual Reports, and the PRA
# register carries the matching Rule 3.1 row). The finding now appears IN the cells
# instead of only in the prose. Independently re-confirmed 2026-09-18 against the
# Bank's own disclosures page, which still lists six Pillar 3 editions (2018-2023)
# and none for 2024 or 2025.
SDDT_NA = "Not required - SDDT, no Pillar 3 published"
SDDT_NA_NSFR = "Not published - SDDT; SRDR replaces the NSFR requirement"

metric(
    "CET1 Ratio", "%",
    [
        ("CET1 ratio", {"FY2025": SDDT_NA, "FY2024": "13.59%", "FY2023": "14.69%", "FY2022": "15.78%", "FY2021": "13.92%",
                        "FY2020": "14.12%", "FY2019": "13.7%", "FY2018": "17.0%", "FY2017": "16.6%"}),
        ("Core Tier 1 / Tier 1 ratio (Basel II/CRD III era terminology; closest equivalent to CET1 ratio)",
         {"FY2016": "12.1%", "FY2015": "16.6%", "FY2014": "16.9%"}),
    ],
    note=FY2023_P3_NOTE + "\n\n" + P3_2021_2022_NOTE + FY24_RATIO + "\n\n" + SDDT_NOTE,
)

metric(
    "Tier 1 Capital", "£'000",
    [
        ("Total eligible Tier 1 capital (CET1)",
         {"FY2025": 348606, "FY2024": 321877, "FY2023": 306251, "FY2022": 287447, "FY2021": 197331,
          "FY2020": 182844, "FY2019": 156836, "FY2018": 135416, "FY2017": 109910}),
        ("Core Tier 1 capital (Basel II/CRD III era terminology; shown as the closest equivalent - see note)",
         {"FY2016": 65017, "FY2015": 69180, "FY2014": 65533}),
    ],
    note=TIER1_NOTE + FY25_CAP + "\n\n" + SDDT_NOTE,
)

metric(
    "Tier 1 Ratio", "%",
    [
        ("Tier 1 ratio (= CET1 ratio; no Additional Tier 1 instrument in issue any year reviewed)",
         {"FY2025": SDDT_NA, "FY2024": "13.59%", "FY2023": "14.69%", "FY2022": "15.78%", "FY2021": "13.92%",
          "FY2020": "14.12%", "FY2019": "13.7%", "FY2018": "17.0%", "FY2017": "16.6%",
          "FY2016": "12.1%", "FY2015": "16.6%", "FY2014": "16.9%"}),
    ],
    note=FY2023_P3_NOTE + "\n\n" + TIER1_NOTE + FY24_RATIO + "\n\n" + SDDT_NOTE,
)

metric(
    "Total Capital", "£'000",
    [("Total eligible regulatory capital (CET1/Core Tier 1 + Tier 2 subordinated debt)",
      {"FY2025": 398606, "FY2024": 336877, "FY2023": 321251, "FY2022": 287447, "FY2021": 227200,
       "FY2020": 212588, "FY2019": 186465, "FY2018": 165416, "FY2017": 139447,
       "FY2016": 96777, "FY2015": 101139, "FY2014": 98022})],
    note=FY2017_RWA_CAVEAT + FY25_CAP + "\n\n" + SDDT_NOTE,
)

metric(
    "Total Capital Ratio", "%",
    [("Total capital ratio",
      {"FY2025": SDDT_NA, "FY2024": SDDT_NA, "FY2023": "15.41%", "FY2022": "15.78%", "FY2021": "16.03%",
       "FY2020": "16.42%", "FY2019": "16.3%", "FY2018": "20.7%", "FY2017": "21.0%",
       "FY2016": "18.2%", "FY2015": "24.4%", "FY2014": "25.4%"})],
    note=FY2023_P3_NOTE
         + "\n\nFY2024 and FY2025 are blank because no total capital ratio is stated anywhere in those "
           "years' Annual Reports (the FY2024 report states only a CET1 ratio) and no Pillar 3 document "
           "exists for them - it is NOT derived from the disclosed Total Capital amount, which would "
           "require back-solving RWAs. FY2024's disclosed CET1 ratio of 13.59% is on the CET1/Tier 1 "
           "Ratio sheets.\n\n"
         + SDDT_NOTE,
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted assets",
      {"FY2025": SDDT_NA, "FY2024": SDDT_NA, "FY2023": 2084246, "FY2022": 1822159, "FY2021": 1417123,
       "FY2020": 1294931, "FY2019": 1144428, "FY2018": 794959, "FY2017": 663552,
       "FY2016": 531742, "FY2015": 416813, "FY2014": 385638})],
    note=FY2023_P3_NOTE + "\n\n"
    + FY2017_RWA_CAVEAT + "\n\n" + DERIVED_RWA_FLAG
    + "\nFY2017 to FY2020 are now the documents' own directly-stated Total RWA figures (FY2017 and FY2018 "
      "from the 2018 edition's Own Funds appendix, FY2019 from the 2019 edition's, FY2020 from the 2020 "
      "edition's); FY2014-FY2016 remain derived from that year's own disclosed Total Capital (or minimum "
      "capital requirement) divided by that year's own disclosed Total Capital ratio (or x12.5 of the "
      "minimum capital requirement) - both inputs to each derivation come from the same source "
      "document/year, not mixed across years.\n\n"
    + SDDT_NOTE
    + " No FY2024 or FY2025 RWA figure is stated in any Annual Report (the word 'risk weighted assets' "
      "appears in AR2025 only inside a restatement note, with no amount), and none is back-solved here from "
      "the FY2024 CET1 ratio and CET1 capital amount - that is exactly the derivation this project does not "
      "make. FY2023 is no longer in that category: it is the 2023 Pillar 3's own directly-stated UK KM1 "
      "figure (2,084,246), which its UK OV1 table independently corroborates at the source's own £m "
      "granularity (1,905 credit + 179 operational + nil CCR = 2,084).",
)

RWA_BREAKDOWN_NOTE = (
    "FY2017 FILLED 2026-09-18, on exactly the footing FY2018 and FY2019 already sit on: credit-risk RWA "
    "only, £629,000k, from 'Table 9 - Summary of On Balance Sheet Credit Risk Exposure, As at 31 December "
    "2017' on printed p.10 of the Cynergy Bank Pillar 3 Disclosures 2018 (the source reports £m; converted "
    "to £'000). Like FY2018 and FY2019, that is NOT the complete Pillar 1 total - the same document's Own "
    "Funds appendix puts FY2017 total RWA at £663,552k, so £34.5m of operational and other Pillar 1 risk is "
    "disclosed in aggregate but never split by category. The 'Total RWA' row therefore shows £629,000k for "
    "FY2017 and will not tie to the Total RWAs sheet; that difference is the undisclosed categories, not an "
    "error. The note this replaces said FY2017 was blank because 'the disclosed ratios don't reliably pin "
    "down a single RWA figure that year' - see the Total RWAs sheet for why that reasoning fell away.\n"
    "FY2016 IS still blank, and now for a checked reason rather than an assumed one: Bank of Cyprus UK's "
    "FY2016 Annual Report is an image-only scan, so the earlier text-search finding proved nothing; it was "
    "re-rendered at 200 dpi and OCR'd page by page on 2026-09-18, and it contains no exposure-class table, "
    "no risk-category split and in fact no risk-weighted-asset amount of any kind. The entity published no "
    "standalone Pillar 3 for FY2016, and the earliest edition that exists (2018) reaches back only to "
    "FY2017. FY2020's own Pillar 3 document does disclose a "
    "summary of on-balance-sheet credit-risk RWA by exposure class (p.25); those figures are now included "
    "below as a separate credit-risk section. They are not the complete Total RWAs figure because the source "
    "does not provide the corresponding operational-risk/other Pillar 1 components at this granularity. FY2014/FY2015 "
    "Operational risk RWA is derived (that year's own disclosed operational risk capital requirement x12.5); "
    "FY2018/FY2019 only Credit risk RWA was located (no Operational/Market risk category breakdown found in "
    "either Pillar 3 document), so Total RWA on this sheet for those two years is Credit risk RWA alone and "
    "will not tie to the (higher) Total RWAs sheet figure for the same year - that gap is the other, "
    "undisclosed risk categories, not an error.\n"
    "FY2023 (added 2026-09-15) has none of those problems: its OV1 components (credit risk 1,905 + "
    "operational risk 179 + CCR nil) foot exactly to the stated total of 2,084, which in turn matches the "
    "same document's UK KM1 total RWA of 2,084,246 once the £m presentation is allowed for. CCR is shown as "
    "0 rather than blank because the source prints a dash for it in 2023, i.e. it is a disclosed nil, not an "
    "undisclosed component. 'Securitisations' (13) is again an 'of which' line inside credit risk, not a "
    "fourth component."
)
bw.add_rwa_breakdown_sheet(
    title="Cynergy Bank Plc — RWA Breakdown",
    subtitle="Consolidated (Company-only FY2014-2015) basis, £'000. FY2023 added 2026-09-15 from the 2023 "
             "Pillar 3's UK OV1 table; FY2017 added 2026-09-18 from the 2018 Pillar 3's own FY2017 "
             "credit-risk table (credit risk only, like FY2018/FY2019 - see source note). FY2020 "
             "credit-risk exposure-class RWA summary is shown separately; FY2016 has no category split in "
             "any document and stays blank.",
    rows=[
        ("SECTION", "Risk-weighted assets by category", {}),
        # GA-006 (2026-09-18): state the SDDT absence in the FY2024/FY2025 columns
        # rather than leaving them blank - same reason as the metric sheets.
        ("DATA", "UK OV1 - overview of risk weighted exposure amounts",
         {"FY2025": "Not required - SDDT, no Pillar 3 published",
          "FY2024": "Not required - SDDT, no Pillar 3 published"}),
        ("SECTION", "FY2020 credit-risk RWA by exposure class (source summary; not complete Pillar 1 total)", {}),
        ("DATA", "Central governments or central banks", {"FY2020": 0}),
        ("DATA", "Institutions", {"FY2020": 9000}),
        ("DATA", "Corporates", {"FY2020": 401000}),
        ("DATA", "Retail", {"FY2020": 74000}),
        ("DATA", "Secured by mortgages on immovable property", {"FY2020": 638000}),
        ("DATA", "Exposures in default", {"FY2020": 30000}),
        ("DATA", "Items associated with particularly high risk", {"FY2020": 24000}),
        ("DATA", "Other items", {"FY2020": 19000}),
        ("TOTAL", "Total credit-risk RWA (FY2020 source summary)", {"FY2020": 1195000}),
        ("SECTION", "UK OV1 basis (2023 and 2022 Pillar 3 editions)", {}),
        ("DATA", "Total credit risk (excluding CCR)", {"FY2023": 1905000, "FY2022": 1685000, "FY2021": 1272000}),
        ("DATA", "of which: securitisations", {"FY2023": 13000, "FY2022": 19000}),
        ("DATA", "Counterparty credit risk (CCR)", {"FY2023": 0, "FY2022": 2000}),
        ("DATA", "Total operational risk (standardised approach)", {"FY2023": 179000, "FY2022": 136000, "FY2021": 117000}),
        ("TOTAL", "Total Pillar 1 RWA per the OV1 table", {"FY2023": 2084000, "FY2022": 1822000, "FY2021": 1389000}),
        ("SECTION", "Earlier editions", {}),
        ("DATA", "Credit risk RWA", {"FY2019": 1066000, "FY2018": 742000, "FY2017": 629000, "FY2015": 385977, "FY2014": 355707}),
        ("DATA", "Operational risk RWA (derived from disclosed capital requirement x12.5)",
         {"FY2015": 30838, "FY2014": 29938}),
        ("TOTAL", "Total RWA", {"FY2019": 1066000, "FY2018": 742000, "FY2017": 629000, "FY2015": 416815, "FY2014": 385645}),
    ],
    sources_text=p3_sources() + "\nFY2017: Cynergy Bank Pillar 3 Disclosures 2018, 'Table 9 - Summary of On Balance Sheet Credit Risk Exposure, As at 31 December 2017', p.10 (source reports £m; converted to £'000; Central governments nil, Institutions 12, Corporates 151, Retail 75, Secured by mortgages 350, Exposures in default 6, High risk 14, Other items 21, Total 629) - " + P3_2018_URL
                 + "\nFY2020: Cynergy Bank Pillar 3 Disclosures 2020, 'Summary of On Balance Sheet Credit Risk Exposure', p.25 (source reports £m; converted to £'000) - " + P3_2020_URL
                 + "\nFY2023: Cynergy Bank Limited 2023 Pillar 3 Disclosures, 'Overview of risk-weighted "
                   "exposure amounts' (UK OV1) table, p.8 (source reports £m; converted to £'000) - "
                   + P3_2023_URL
                 + "\nFY2022 & FY2021: Cynergy Bank Limited 2022 Pillar 3, 'Overview of risk-weighted "
                   "exposure amounts' table, p.6 (source reports £m; converted to £'000) - " + P3_2022_URL
                 + "\n\nTWO DOCUMENTED INCONSISTENCIES IN THE 2022 SOURCE TABLE, shown as published rather "
                   "than silently reconciled. (1) Its FY2021 comparative column totals £1,389m (credit "
                   "1,272 + operational 117), but the SAME document's own FY2021 Key-metrics comparative - "
                   "and the 2021 edition's own Key-metrics table - both state total RWAs of £1,417m, a "
                   "£28m (2.0%) difference. The Total RWAs sheet uses the Key-metrics figure (£1,417m) "
                   "because that is the figure both editions agree on and the one the disclosed FY2021 "
                   "ratios are computed against; this OV1 row is kept at its own stated £1,389m. (2) Its "
                   "FY2022 components (1,685 credit + 2 CCR + 136 operational) sum to £1,823m against a "
                   "stated total of £1,822m - a £1m rounding artifact of the source's own £m presentation. "
                   "'Securitisations' (£19m) is shown as an 'of which' line because including it as a "
                   "fourth component would overstate the total by that amount.\n\n" + RWA_BREAKDOWN_NOTE,
    first_col_width=60,
    source_height=280,
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio",
      {"FY2025": SDDT_NA, "FY2024": SDDT_NA, "FY2023": "6.96%", "FY2022": "7.40%", "FY2021": "5.46%",
       "FY2020": "6.1%", "FY2019": "6.3%", "FY2018": "6.9%", "FY2017": "5.8%",
       "FY2016": "4.7%", "FY2015": "6.0%", "FY2014": "6.1%"})],
    note=FY2023_P3_NOTE
         + " The FY2023 leverage ratio of 6.96% is stated directly in the 2023 UK KM1 table, on a leverage "
           "ratio total exposure measure of 4,398,669 (against Tier 1 capital of 306,251); it is not "
           "recomputed here from those two inputs.\n\n"
         + "FY2020's Pillar 3 document states two different leverage exposure measure figures on different "
         "pages (£3,006,579k in the reconciliation table vs £2,953,625k in the common disclosure table) that "
         "would imply slightly different ratios from the same £182,844k Tier 1 capital - the document's own "
         "stated 6.1% ratio is used here rather than recomputing from either exposure figure. FY2018's own "
         "Pillar 3 document states 6.9% for FY2018; FY2019's Pillar 3 document's own FY2018 comparative "
         "instead shows 6.8% - each year's own report is used for its own figure (FY2018 = 6.9%), per this "
         "project's standing convention; the two documents disagree on FY2018 by 0.1pp.\n\n"
         + SDDT_NOTE
         + " No leverage ratio figure appears anywhere in the FY2024 or FY2025 Annual Reports (full-text "
           "searched 2026-09-15 - the only hits for 'leverage' are unrelated lending/business usages), and "
           "there is no Pillar 3 edition for either year, so those two years stay blank.",
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio (12-month average basis; source labels the HQLA input 'Weighted value - average')",
      {"FY2025": SDDT_NA, "FY2024": SDDT_NA, "FY2023": "304.44%", "FY2022": "315.98%", "FY2021": "242.91%", "FY2020": "340%"})],
    note=FY2023_P3_NOTE + "\n\n" + FY2023_RESTATEMENT_NOTE + "\n\n"
         + P3_2021_2022_NOTE + " NOTE ON FY2020: this sheet's FY2020 figure (340%) comes from the 2020 "
         "Pillar 3 edition's own statement, but the 2021 edition's FY2020 comparative column instead "
         "shows 330%. Each year's own report is used for its own figure per this project's standing "
         "convention, so 340% is retained for FY2020; the 1.0pp disagreement between the two documents "
         "is recorded here rather than silently reconciled.\n\n"
         + SDDT_NOTE
         + " The FY2024 and FY2025 Annual Reports describe the LCR only qualitatively ('the liquidity "
           "coverage ratio has exceeded the regulatory requirements throughout 2025', AR2025 p.37) - a "
           "statement, not a value - so nothing is transcribed from them, and there is no Pillar 3 edition "
           "for either year. FY2023's Annual Report is equally qualitative, but its Pillar 3 edition is not, "
           "which is where this sheet's FY2023 figure comes from.",
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio", {"FY2025": SDDT_NA_NSFR, "FY2024": SDDT_NA_NSFR, "FY2023": "148.67%", "FY2022": "149.48%", "FY2021": "130%", "FY2020": "132%"})],
    note=FY2023_P3_NOTE + "\n\n" + FY2023_RESTATEMENT_NOTE + "\n\n"
         + P3_2021_2022_NOTE + " FY2021's NSFR is taken from the 2021 edition's own ratio table (130%); "
         "the 2022 edition shows a dash rather than an FY2021 NSFR comparative, so the 2021 edition is "
         "the only source for that year.\n\n" + NSFR_SDDT_NOTE,
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources(), per_note={"MREL Ratio": NOT_DISCLOSED_NOTE + "\n\n" + SDDT_NOTE},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 5597322, "FY2024": 5098500, "FY2023": 4611231, "FY2022": 4124713, "FY2021": 3518034, "FY2020": 2943446, "FY2019": 2471904, "FY2018": 1955020, "FY2017": 1877118, "FY2016": 1402977, "FY2015": 1168863, "FY2014": 1069043}),
        ("Loans and advances to customers", {"FY2025": 3745133, "FY2024": 3653477, "FY2023": 3564297, "FY2022": 3254230, "FY2021": 2949578, "FY2020": 2613962, "FY2019": 2264381, "FY2018": 1668923, "FY2017": 1407200, "FY2016": 1083922, "FY2015": 820807, "FY2014": 617976}),
        ("Customer deposits", {"FY2025": 4910863, "FY2024": 4492026, "FY2023": 3758037, "FY2022": 3336442, "FY2021": 2832564, "FY2020": 2352241, "FY2019": 2227678, "FY2018": 1762654, "FY2017": 1656975, "FY2016": 1257403, "FY2015": 1038348, "FY2014": 955464}),
        ("Total equity", {"FY2025": 426229, "FY2024": 387856, "FY2023": 349550, "FY2022": 309446, "FY2021": 220716, "FY2020": 195787, "FY2019": 166650, "FY2018": 137331, "FY2017": 112718, "FY2016": 65857, "FY2015": 69820, "FY2014": 66216}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total operating income", {"FY2025": 140485, "FY2024": 134646, "FY2023": 159546, "FY2022": 127584, "FY2021": 88029, "FY2020": 78325, "FY2019": 58998, "FY2018": 48596, "FY2017": 40021, "FY2016": 30051, "FY2015": 23999, "FY2014": 18719}),
        ("Total operating expenses", {"FY2025": -89416, "FY2024": -80932, "FY2023": -100220, "FY2022": -77225, "FY2021": -52233, "FY2020": -46323, "FY2019": -36135, "FY2018": -42216, "FY2017": -34602, "FY2016": -24151, "FY2015": -20104, "FY2014": -17824}),
        ("Profit for the year", {"FY2025": 37940, "FY2024": 40234, "FY2023": 40613, "FY2022": 40256, "FY2021": 24929, "FY2020": 20828, "FY2019": 13519, "FY2018": 4600, "FY2017": 861, "FY2016": -9020, "FY2015": 3604, "FY2014": 3301}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 387856, "FY2024": 349550, "FY2023": 309446, "FY2022": 220716, "FY2021": 195787, "FY2020": 166650, "FY2019": 137331, "FY2018": 112718, "FY2017": 65857, "FY2016": 69820, "FY2015": 66216, "FY2014": 59583}),
        ("Total comprehensive income for the year", {"FY2025": 37940, "FY2024": 38306, "FY2023": 40104, "FY2022": 41730, "FY2021": 24929, "FY2020": 20137, "FY2019": 14648, "FY2018": 4517, "FY2017": 861, "FY2016": -3963, "FY2015": 3604, "FY2014": 6633}),
        ("Other equity movements, net", {"FY2025": 433, "FY2024": 0, "FY2023": 0, "FY2022": 47000, "FY2021": 0, "FY2020": 9000, "FY2019": 14671, "FY2018": 20096, "FY2017": 46000, "FY2016": 0, "FY2015": 0, "FY2014": 0}),
        ("Closing equity", {"FY2025": 426229, "FY2024": 387856, "FY2023": 349550, "FY2022": 309446, "FY2021": 220716, "FY2020": 195787, "FY2019": 166650, "FY2018": 137331, "FY2017": 112718, "FY2016": 65857, "FY2015": 69820, "FY2014": 66216}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash flow from/(used in) operating activities", {"FY2025": -17143, "FY2024": 445559, "FY2023": 130953, "FY2022": 190786, "FY2021": 234303, "FY2020": 117909, "FY2019": -83910, "FY2018": -157299, "FY2017": 75543, "FY2016": -44784, "FY2015": -108406, "FY2014": -85437}),
        ("Net cash flow from/(used in) investing activities", {"FY2025": -459330, "FY2024": -135783, "FY2023": -39022, "FY2022": 36420, "FY2021": -147084, "FY2020": -12691, "FY2019": -8787, "FY2018": -2257, "FY2017": -1620, "FY2016": -1034, "FY2015": -542, "FY2014": -766}),
        ("Net cash flow from/(used in) financing activities", {"FY2025": 29481, "FY2024": -2292, "FY2023": 13701, "FY2022": 47034, "FY2021": -238, "FY2020": 8834, "FY2019": 14642, "FY2018": 19957, "FY2017": 44526, "FY2016": -2265, "FY2015": -2271, "FY2014": -2256}),
        ("Cash and cash equivalents at end of year", {"FY2025": 611903, "FY2024": 1058851, "FY2023": 751598, "FY2022": 646528, "FY2021": 372288, "FY2020": 285307, "FY2019": 171255, "FY2018": 249310, "FY2017": 388909, "FY2016": 268981, "FY2015": 309135, "FY2014": 422348}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1/Core Tier 1 ratio", {"FY2024": "13.59%", "FY2023": "14.69%", "FY2022": "15.78%", "FY2021": "13.92%", "FY2020": "14.12%", "FY2019": "13.7%", "FY2018": "17.0%", "FY2017": "16.6%", "FY2016": "12.1%", "FY2015": "16.6%", "FY2014": "16.9%"}),
        ("Total Capital ratio", {"FY2023": "15.41%", "FY2022": "15.78%", "FY2021": "16.03%", "FY2020": "16.42%", "FY2019": "16.3%", "FY2018": "20.7%", "FY2017": "21.0%", "FY2016": "18.2%", "FY2015": "24.4%", "FY2014": "25.4%"}),
        ("Leverage ratio", {"FY2023": "6.96%", "FY2022": "7.40%", "FY2021": "5.46%", "FY2020": "6.1%", "FY2019": "6.3%", "FY2018": "6.9%", "FY2017": "5.8%", "FY2016": "4.7%", "FY2015": "6.0%", "FY2014": "6.1%"}),
        ("LCR (12-month average)", {"FY2023": "304.44%", "FY2022": "315.98%", "FY2021": "242.91%", "FY2020": "340%"}),
    ],
    note="Pillar 3 ratio coverage runs FY2014-FY2023 (from the Bank's own Pillar 3 documents - editions "
         "2018-2022 recovered from the Wayback Machine, and the 2023 edition found on 2026-09-15 on the "
         "Contentful CDN behind the current site, linked only from the Bank's /strong-and-prudent-management "
         "page) plus a FY2024 CET1 ratio of 13.59% taken from the Annual Report & Accounts 2024's own "
         "narrative (p.6), the only ratio stated numerically in either of the FY2024/FY2025 Annual Reports. "
         "FY2025 has no ratio of any kind disclosed. FY2023's row was blank until 2026-09-15 on the basis of "
         "an earlier conclusion, now overturned, that its Pillar 3 document was unreachable. "
         "WHY THE RATIO ROWS STOP: Cynergy Bank's modification-by-consent application to be treated as a "
         "Small Domestic Deposit Taker (SDDT) was approved on 17 January 2025, and the Bank states in its own "
         "Annual Reports that it is consequently not required to publish Pillar 3 disclosures for either "
         "31 December 2024 (AR2024 p.71) or 31 December 2025 (AR2025 p.45); the same passages record that the "
         "full NSFR has been replaced by a Simplified Retail Deposit Ratio. That absence is enumerated, not "
         "merely unfound: the Bank's Pillar 3 page serves exactly six editions (FY2018-FY2023) and no later "
         "one, and the same page is demonstrably current (it also carries a 2026 Gender Pay Gap report). "
         "FY2023 predates the exemption and its Pillar 3 disclosure was both produced and published. This is "
         "a disclosure-regime change, not an entity cessation - Cynergy Bank Plc (FRN 575105) is still on "
         "the Bank of England's List of banks as at 30 September 2026. "
         "CET1 Capital, Tier 1 Capital and Total Capital (£'000) are disclosed for FY2014-FY2020 and "
         "FY2023-FY2025 - see their own sheets. Cash flow figures are duplicated from the Cash Flow Statement "
         "sheet for at-a-glance trend viewing.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/CYNERGY BANK FINANCIALS.xlsx")
