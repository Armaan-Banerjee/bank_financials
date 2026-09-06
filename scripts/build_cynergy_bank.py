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
        f"FY2024 & FY2023: Cynergy Bank plc Annual Report & Accounts 2024, p.146 (Note 32, Capital resources) - {AR2024_URL}\n"
        "FY2025, FY2022, FY2021: no quantitative capital or liquidity figures were found in the corresponding "
        "Annual Report - only qualitative narrative in the 'Capital, liquidity and funding risk' section of "
        "each report's Risk report (e.g. 'we held surplus regulatory capital', 'the liquidity coverage ratio "
        "has exceeded the regulatory requirements'), with no £ or % figures stated. Note this batch (HD-051) "
        "found real standalone Pillar 3 PDFs for FY2018-2020 via the Wayback Machine even though none is "
        "linked from the live site - FY2021's own equivalent document was not searched for (out of scope for "
        "this batch; flagged for the wayfinder map) and may well also exist despite this note's absence-claim "
        "for FY2021.\n"
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
    "no standalone Pillar 3 document was found on the bank's own site. See the Cash Flow Statement sheet's "
    "source note for the SDDT-regime context that plausibly explains this."
)

TIER1_NOTE = (
    "Cynergy Bank's own Annual Report labels this line 'Total eligible Tier 1 capital (CET1)' - i.e. it "
    "states Tier 1 capital and CET1 capital are identical (no Additional Tier 1 instruments in issue) - see "
    "the CET1 Capital sheet for the same figures and source."
)

def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, f"Consolidated basis, {unit}" if unit else "Consolidated basis",
                         rows_data, p3_sources(), note=note, first_col_width=52, source_height=170)


FY2017_RWA_CAVEAT = (
    "FY2017 Total Capital (£) and Total RWAs are left blank deliberately, not omitted by oversight: the "
    "FY2018 Pillar 3 document's FY2017 comparative discloses CET1/Tier 1 capital (£109,910k) and three ratios "
    "(CET1 16.6%, Total Capital 21.0%, Leverage 5.8%) but never states a Total Capital £ amount or a Total "
    "RWA £ amount directly, and the same document's own FY2017 credit-risk RWA figure (£629,000k) is larger "
    "than either of the two different 'implied total RWA' figures that back-solving from the two disclosed "
    "ratios would produce (~£523m assuming Total Capital = CET1 that year, or ~£662m assuming CET1 ratio "
    "alone pins down RWA) - these are inconsistent with each other and with the disclosed credit-risk RWA, "
    "so no single figure can be derived reliably. Rather than guess, these two cells are left blank for "
    "FY2017 only; the three ratios above are the source's own directly-stated figures and are populated."
)

metric(
    "CET1 Capital", "£'000",
    [
        ("Total eligible Tier 1 capital (CET1)",
         {"FY2024": 321877, "FY2023": 306251, "FY2020": 182844, "FY2019": 156836, "FY2018": 135416, "FY2017": 109910}),
        ("Core Tier 1 capital (Basel II/CRD III era terminology; shown as the closest equivalent to CET1 - see note)",
         {"FY2016": 65017, "FY2015": 69180, "FY2014": 65533}),
    ],
)

metric(
    "CET1 Ratio", "%",
    [
        ("CET1 ratio", {"FY2020": "14.12%", "FY2019": "13.7%", "FY2018": "17.0%", "FY2017": "16.6%"}),
        ("Core Tier 1 / Tier 1 ratio (Basel II/CRD III era terminology; closest equivalent to CET1 ratio)",
         {"FY2016": "12.1%", "FY2015": "16.6%", "FY2014": "16.9%"}),
    ],
)

metric(
    "Tier 1 Capital", "£'000",
    [
        ("Total eligible Tier 1 capital (CET1)",
         {"FY2024": 321877, "FY2023": 306251, "FY2020": 182844, "FY2019": 156836, "FY2018": 135416, "FY2017": 109910}),
        ("Core Tier 1 capital (Basel II/CRD III era terminology; shown as the closest equivalent - see note)",
         {"FY2016": 65017, "FY2015": 69180, "FY2014": 65533}),
    ],
    note=TIER1_NOTE,
)

metric(
    "Tier 1 Ratio", "%",
    [
        ("Tier 1 ratio (= CET1 ratio; no Additional Tier 1 instrument in issue any year reviewed)",
         {"FY2020": "14.12%", "FY2019": "13.7%", "FY2018": "17.0%", "FY2017": "16.6%",
          "FY2016": "12.1%", "FY2015": "16.6%", "FY2014": "16.9%"}),
    ],
    note=TIER1_NOTE,
)

metric(
    "Total Capital", "£'000",
    [("Total eligible regulatory capital (CET1/Core Tier 1 + Tier 2 subordinated debt)",
      {"FY2024": 336877, "FY2023": 321251, "FY2020": 212588, "FY2019": 186465, "FY2018": 165416,
       "FY2016": 96777, "FY2015": 101139, "FY2014": 98022})],
    note=FY2017_RWA_CAVEAT,
)

metric(
    "Total Capital Ratio", "%",
    [("Total capital ratio",
      {"FY2020": "16.42%", "FY2019": "16.3%", "FY2018": "20.7%", "FY2017": "21.0%",
       "FY2016": "18.2%", "FY2015": "24.4%", "FY2014": "25.4%"})],
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted assets",
      {"FY2020": 1294931, "FY2019": 1144428, "FY2018": 796565,
       "FY2016": 531742, "FY2015": 416813, "FY2014": 385638})],
    note=FY2017_RWA_CAVEAT
    + "\nFY2020 is the document's own directly-stated Total RWA figure; FY2014-2016, FY2018 and FY2019 are "
      "derived from that year's own disclosed Total Capital (or minimum capital requirement) divided by that "
      "year's own disclosed Total Capital ratio (or x12.5 of the minimum capital requirement) - both inputs "
      "to each derivation come from the same source document/year, not mixed across years.",
)

RWA_BREAKDOWN_NOTE = (
    "FY2016 and FY2017 are deliberately left blank on this sheet, not omitted by oversight: FY2016's "
    "Annual Report discloses only the aggregate Total Capital and ratio, no risk-category RWA split at all; "
    "FY2017 is left blank for the same reason given on the Total RWAs sheet (the disclosed ratios don't "
    "reliably pin down a single RWA figure that year). FY2020's own Pillar 3 document does disclose a "
    "summary of on-balance-sheet credit-risk RWA by exposure class (p.25); those figures are now included "
    "below as a separate credit-risk section. They are not the complete Total RWAs figure because the source "
    "does not provide the corresponding operational-risk/other Pillar 1 components at this granularity. FY2014/FY2015 "
    "Operational risk RWA is derived (that year's own disclosed operational risk capital requirement x12.5); "
    "FY2018/FY2019 only Credit risk RWA was located (no Operational/Market risk category breakdown found in "
    "either Pillar 3 document), so Total RWA on this sheet for those two years is Credit risk RWA alone and "
    "will not tie to the (higher) Total RWAs sheet figure for the same year - that gap is the other, "
    "undisclosed risk categories, not an error."
)
bw.add_rwa_breakdown_sheet(
    title="Cynergy Bank Plc — RWA Breakdown",
    subtitle="Consolidated (Company-only FY2014-2015) basis, £'000. FY2020 credit-risk exposure-class RWA "
             "summary is shown separately; FY2016/FY2017 remain unavailable - see source note at bottom.",
    rows=[
        ("SECTION", "Risk-weighted assets by category", {}),
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
        ("DATA", "Credit risk RWA", {"FY2019": 1066000, "FY2018": 742000, "FY2015": 385977, "FY2014": 355707}),
        ("DATA", "Operational risk RWA (derived from disclosed capital requirement x12.5)",
         {"FY2015": 30838, "FY2014": 29938}),
        ("TOTAL", "Total RWA", {"FY2019": 1066000, "FY2018": 742000, "FY2015": 416815, "FY2014": 385645}),
    ],
    sources_text=p3_sources() + "\nFY2020: Cynergy Bank Pillar 3 Disclosures 2020, 'Summary of On Balance Sheet Credit Risk Exposure', p.25 (source reports £m; converted to £'000) - " + P3_2020_URL + "\n\n" + RWA_BREAKDOWN_NOTE,
    first_col_width=60,
    source_height=280,
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio",
      {"FY2020": "6.1%", "FY2019": "6.3%", "FY2018": "6.9%", "FY2017": "5.8%",
       "FY2016": "4.7%", "FY2015": "6.0%", "FY2014": "6.1%"})],
    note="FY2020's Pillar 3 document states two different leverage exposure measure figures on different "
         "pages (£3,006,579k in the reconciliation table vs £2,953,625k in the common disclosure table) that "
         "would imply slightly different ratios from the same £182,844k Tier 1 capital - the document's own "
         "stated 6.1% ratio is used here rather than recomputing from either exposure figure. FY2018's own "
         "Pillar 3 document states 6.9% for FY2018; FY2019's Pillar 3 document's own FY2018 comparative "
         "instead shows 6.8% - each year's own report is used for its own figure (FY2018 = 6.9%), per this "
         "project's standing convention; the two documents disagree on FY2018 by 0.1pp.",
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio", {"FY2020": "340%"})],
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio", {"FY2020": "132%"})],
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources(), per_note={"MREL Ratio": NOT_DISCLOSED_NOTE},
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
        ("CET1/Core Tier 1 ratio", {"FY2020": "14.12%", "FY2019": "13.7%", "FY2018": "17.0%", "FY2017": "16.6%", "FY2016": "12.1%", "FY2015": "16.6%", "FY2014": "16.9%"}),
        ("Total Capital ratio", {"FY2020": "16.42%", "FY2019": "16.3%", "FY2018": "20.7%", "FY2017": "21.0%", "FY2016": "18.2%", "FY2015": "24.4%", "FY2014": "25.4%"}),
        ("Leverage ratio", {"FY2020": "6.1%", "FY2019": "6.3%", "FY2018": "6.9%", "FY2017": "5.8%", "FY2016": "4.7%", "FY2015": "6.0%", "FY2014": "6.1%"}),
    ],
    note="This batch (HD-051) found real Pillar 3 capital/leverage ratios for FY2014-FY2020 (see the "
         "individual Pillar 3 sheets) - shown here even though FY2021-FY2025 have none disclosed (a prior "
         "sourcing note claiming no ratio-type Pillar 3 metric exists in any year was wrong; corrected on "
         "each affected sheet, see the Cash Flow Statement sheet's source note). CET1 Capital, Tier 1 Capital "
         "and Total Capital (£'000) are disclosed for FY2014-FY2020 and FY2023-FY2024 - see their own sheets. "
         "Cash flow figures are duplicated from the Cash Flow Statement sheet for at-a-glance trend viewing.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/CYNERGY BANK FINANCIALS.xlsx")
