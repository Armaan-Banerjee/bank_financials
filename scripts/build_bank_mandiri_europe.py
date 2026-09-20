import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# PILLAR-3-ONLY WORKBOOK: Bank Mandiri (Europe) Limited (company 03793679, FRN 204424)
# is a qualifying entity under FRS 101 and takes the "presentation of a cash-flow
# statement" (IAS 7) disclosure exemption every year - explicitly stated in Note 1.4
# "Disclosure Exemptions" of its FY2025 Annual Report, deferring to the accounts of
# its parent, PT Bank Mandiri (Persero) Tbk. Confirmed as a standing feature by
# checking both the FY2020 filing (earliest available, filed 2021) and the FY2025
# filing (most recent) - no Contents-page entry for a cash flow statement in either,
# 5 years apart. Follows the BNY Mellon International / ABC International Bank
# precedent: 13-sheet structure, Cash Flow Statement sheet documents the exemption
# instead of line items, Overview sheet omits the cash-flow chart.
#
# The Bank's functional currency is US Dollars (Note 1.2). The entity has published
# exactly ONE Pillar 3 document in its history, covering 31 December 2016 (see
# PILLAR3_2016_ARCHIVE_URL). For every other year the only capital/liquidity
# disclosures are a narrative paragraph + "Key Performance Indicator" table in the
# Strategic Report of each Annual Report, giving only a combined Total Capital Ratio
# (labelled "Capital Adequacy Ratio", Own Funds / Total RWA - no separate CET1/Tier 1
# breakdown is printed there), LCR, NSFR, and total "regulatory capital resources"
# (Own Funds, $m); plus, in the FY2018-FY2021 Annual Reports only, a "regulatory
# Tier 1 resources" table inside the Risk management note.
# The KPI table format was only introduced from the FY2023 Annual Report onward
# (FY2022's own report has a KPI table with no capital/liquidity rows, and no
# capital/liquidity narrative was found in its Strategic Report or Directors'
# Report) - FY2022's figures come from FY2023's own comparative column instead.
# FY2021's Annual Report carries no capital ratio, LCR or NSFR in any form (checked
# 2026-09-18 against the bank's own text-layer copy) - left blank, not estimated.
#
# GA-005 (2026-09-18) - THREE CLAIMS THIS SCRIPT PREVIOUSLY MADE WERE WRONG AND ARE
# CORRECTED THROUGHOUT:
#   (1) "no RWA figure appears in any source checked for any year" - the 2016 Pillar 3
#       prints a full "Risk weighted assets" table (Total Risk Exposure US$64,242k) and
#       a "Total Eligible Capital" of US$49,163k. Both are now on their sheets, as the
#       bank's own DISCLOSED figures - not derived, and unrelated to the back-solved
#       values withdrawn on 2026-09-15, which stay withdrawn.
#   (2) "the credit-quality-per-class table was NOT found in any of the FY2023-FY2014
#       Annual Reports" - it is in EVERY one of them, FY2014 through FY2025, plus the
#       2016 Pillar 3. Asset Quality is now populated for all twelve years.
#   (3) "the regulatory Tier 1 resources table appears in the FY2021-style report" only
#       - it is also in the FY2020, FY2019 and FY2018 Annual Reports. The FY2017, FY2016,
#       FY2015 and FY2014 reports' "(G) Capital adequacy risk" note is narrative only,
#       with no table, which is a positive finding rather than a failed search.

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014"]  # most recent first, calendar year-end (31 December)
YEAR_LABEL = {y: y for y in YEARS}

# HD-017: extended back to FY2014 (confirmed floor per HD-002) — see ST_ENTITY_NOTE below for the
# 7 new years' sourcing (Companies House statutory accounts, all scanned/image-only, visually
# transcribed) and NOT_DISCLOSED_NOTE for why the Pillar-3-style regulatory metric sheets (CET1,
# Tier 1, Total Capital, Leverage, LCR, NSFR, MREL) have nothing to add for FY2014-FY2020: this
# entity's Annual Report "Key Performance Indicator" table format (the only source for these
# metrics) was not introduced until the FY2023 Annual Report - confirmed both by HD-002's original
# finding and by this session's own check of the FY2020 and FY2014 Chairman's Statement/Strategic
# Report narratives (capital/liquidity discussed only qualitatively, no ratio figures, in either).

# ---------------------------------------------------------------
# FX conversion (functional currency USD; converting to £ per this project's
# established FX methodology - see build_zenith.py / build_smbc.py precedent).
# Only point-in-time (stock) figures need conversion here - there's no cash flow
# statement, so no average/flow rate is needed.
# Rates are Bank of England GBP/USD spot via poundsterlinglive.com's published
# archive, £1 = $X, same table used throughout this project's USD-reporting banks.
# ---------------------------------------------------------------
FX_SPOT = {
    "FY2021": 1.3728,  # 31 Dec 2021
    "FY2022": 1.2097,  # 30 Dec 2022 (31st was a Saturday)
    "FY2023": 1.2732,  # 29 Dec 2023 (31st was a Sunday)
    "FY2024": 1.2515,  # 31 Dec 2024
    "FY2025": 1.3448,  # 31 Dec 2025
    "FY2020": 1.3649,  # 31 Dec 2020
    "FY2019": 1.3210,  # 31 Dec 2019
    "FY2018": 1.2769,  # 31 Dec 2018
    "FY2017": 1.3510,  # 29 Dec 2017 (31st was a Sunday)
    "FY2016": 1.2303,  # 30 Dec 2016 (31st was a Saturday)
    "FY2015": 1.4819,  # 31 Dec 2015
    "FY2014": 1.5608,  # 31 Dec 2014
}

# Calendar-year average GBP/USD spot rate (£1 = $X), computed from the daily
# Bank of England spot series published at poundsterlinglive.com's historical
# archive (~250 trading days per year averaged) - used for flow figures
# (P&L, equity movements) per this project's established FX methodology
# (see build_smbc.py precedent: spot for stocks, average for flows).
# FY2015-FY2020 averages are the mean of 12 HMRC monthly-average GBP/USD
# rates (tealfx.com's HMRC rate archive) for that calendar year - the same
# "spot for stocks, average for flows" convention, using HMRC's official
# monthly averages as the closest available proxy to a full daily series.
# FY2014 could not be sourced at monthly granularity (tealfx's HMRC archive
# starts at 2015) - approximated as the mean of the 4 first-trading-day-of-
# quarter Bank of England spot rates for 2014 (Jan/Apr/Jul/Oct), a coarser
# proxy than the other years - flagged here as a lower-confidence figure.
FX_AVG = {
    "FY2021": 1.3756,
    "FY2022": 1.2365,
    "FY2023": 1.2434,
    "FY2024": 1.2780,
    "FY2025": 1.3183,
    "FY2020": 1.2767,
    "FY2019": 1.2767,
    "FY2018": 1.3436,
    "FY2017": 1.2827,
    "FY2016": 1.3779,
    "FY2015": 1.5353,
    "FY2014": 1.6604,  # coarser 4-point-quarterly-snapshot proxy - see note above
}


def stock(usd):
    """Point-in-time (capital/RWA/balance sheet) figures, £'000, at that year's period-end spot rate."""
    return {y: round(v / FX_SPOT[y] / 1000, 0) for y, v in usd.items()}


def flow(usd):
    """Flow (P&L/equity-movement) figures, £'000, at that year's calendar-year average rate."""
    return {y: round(v / FX_AVG[y] / 1000, 0) for y, v in usd.items()}


FY2025_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/03793679/filing-history/MzUyODU0NjIyMmFkaXF6a2N4/document?format=pdf&download=0"
FY2024_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/03793679/filing-history/MzQ2ODc4NDgyMGFkaXF6a2N4/document?format=pdf&download=0"
FY2023_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/03793679/filing-history/MzQyNjk5Njk1M2FkaXF6a2N4/document?format=pdf&download=0"
# HD-017: FY2014-FY2020 Annual Report filings (Companies House filing history), all scanned/
# image-only PDFs (0 text blocks/page, confirmed via pdf_tools.py scan) - visually transcribed.
# NOTE (RWA Breakdown review, 2026-09-08): this URL previously pointed to the wrong Companies
# House filing (a 2-page Deloitte LLP auditor-resignation letter, filed 27-Jul-2023, not the
# accounts) - corrected here to the actual "Full accounts made up to 31 December 2022" filing
# (filed 06-Jul-2023, 53 pages).
FY2022_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/03793679/filing-history/MzM4NDY2OTkyM2FkaXF6a2N4/document?format=pdf&download=0"
# ADDED 2026-09-15: the FY2021 accounts filing was never previously on file for this
# entity - the script jumped straight from FY2022 to FY2020 - which is why FY2021 was
# recorded as unrecoverable. It is a real filing (AA, made up to 31 December 2021,
# filed 13 July 2022) and it carries a regulatory Tier 1 capital table.
FY2021_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/03793679/filing-history/MzM0NDk3Nzg2MGFkaXF6a2N4/document?format=pdf&download=0"
FY2020_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/03793679/filing-history/MzMwMDY0ODM2MWFkaXF6a2N4/document?format=pdf&download=0"
FY2019_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/03793679/filing-history/MzI4MzQzODYxOWFkaXF6a2N4/document?format=pdf&download=0"
FY2018_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/03793679/filing-history/MzI0MzE1NDIyNmFkaXF6a2N4/document?format=pdf&download=0"
FY2017_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/03793679/filing-history/MzIwMTI4MzM0M2FkaXF6a2N4/document?format=pdf&download=0"
FY2016_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/03793679/filing-history/MzE3NzM1OTQ5OWFkaXF6a2N4/document?format=pdf&download=0"
FY2015_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/03793679/filing-history/MzE0ODg4NjI3NWFkaXF6a2N4/document?format=pdf&download=0"
FY2014_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/03793679/filing-history/MzExOTM5OTY1MmFkaXF6a2N4/document?format=pdf&download=0"

# ADDED 2026-09-15 - the bank hosts its own Annual Reports, and MOST OF THEM ARE
# FULL TEXT-LAYER PDFs. Earlier notes in this script state that all four of the
# FY2022-FY2025 Annual Reports are "scanned/image-only" and were reviewed only
# page-by-page; that is true of the Companies House filings this script cites,
# but NOT of the bank's own copies. FY2021, FY2022, FY2024 and FY2025 all
# extract cleanly with pdftotext (160-172KB of text each). Only FY2023 is a
# genuine scan. Every figure on the capital and liquidity sheets has now been
# re-verified against these machine-readable originals - see CAPITAL_SOURCES.
# These were found by an unfiltered Wayback CDX sweep of bkmandiri.co.uk; the
# site's WordPress REST API is blocked by its security plugin and its sitemap
# lists no documents, so directory enumeration was the only route to them.
SITE_AR2025_URL = "https://www.bkmandiri.co.uk/media/2026/04/BMEL-Annual-Report-2025.pdf"
SITE_AR2024_URL = "https://www.bkmandiri.co.uk/media/2025/04/BMEL-Annual-Report-2024.pdf"
SITE_AR2023_URL = "https://www.bkmandiri.co.uk/media/2024/12/BMEL-Annual-Report-2023.pdf"
SITE_AR2022_URL = "https://www.bkmandiri.co.uk/media/2024/12/BMEL-Annual-Report-2022.pdf"
SITE_AR2021_URL = "https://www.bkmandiri.co.uk/media/2024/12/BMEL-Annual-Report-2021.pdf"

# The ONLY Pillar 3 document this entity has ever published, so far as any sweep
# has found: a single FY2016 disclosure. It is dead on the live site (404) and
# survives only in the Wayback Machine. This is the relevant test of the "if a
# bank disclosed before, it must still disclose" inference - here the practice
# lapsed roughly a decade before this workbook's earliest open year, so the past
# disclosure carries no implication for FY2021-FY2025. Compare Kingdom Bank.
PILLAR3_2016_ARCHIVE_URL = (
    "https://web.archive.org/web/20240301085228/https://bkmandiri.co.uk/"
    "BMEL%20-%20Pillar%203%20%20Disclosures%2031st%20December%202016.pdf"
)

ENTITY_NOTE = (
    "ENTITY NOTE: Bank Mandiri (Europe) Limited (company 03793679, FRN 204424, incorporated 22 June 1999 as "
    "'Exitmode Limited', renamed 26 July 1999) is a wholly-owned UK subsidiary of PT Bank Mandiri (Persero) Tbk, "
    "Indonesia's largest bank by assets. All figures below are on the Bank's own entity-level basis - it has no "
    "subsidiaries of its own."
)

EXEMPTION_NOTE = (
    "FRS 101 CASH-FLOW EXEMPTION: the FY2025 Annual Report states (Note 1.4, Disclosure Exemptions): \"As permitted "
    "by FRS 101, the Company has taken advantage of the disclosure exemptions available under that standard "
    "concerning the presentation of comparative information in respect of certain assets, presentation of a "
    "cash-flow statement, standards not yet effective, impairment of assets and related party transactions between "
    "two or more wholly owned members of the group. Where required, equivalent disclosures are given in the "
    "accounts of PT Bank Mandiri (Persero) Tbk\", and explicitly lists 'IAS 7 Statement of Cash Flows and related "
    f"notes' among the exemptions applied - Bank Mandiri (Europe) Limited Annual Report FY2025, p.24-25 - "
    f"{FY2025_AR_URL}. No Statement of Cash Flows appears in the Contents page of the FY2014 filing (earliest "
    "available Companies House filing, extended back from FY2020 under HD-017), any intervening year's filing "
    "(FY2015-FY2019 all checked), or the FY2025 (most recent) accounts, confirming this is a standing structural "
    "feature across the entity's entire filing history, not a one-off. Per the project's established policy for this exemption "
    "(see The Bank of New York Mellon (International) Limited / ABC International Bank plc), this workbook is "
    "built as a PILLAR-3-ONLY variant: the capital/liquidity metrics that are disclosed are populated below, but no "
    "cash flow figures exist to show. See the Overview sheet for the equivalent treatment there."
)

CASH_FLOW_SOURCES = ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE

NOT_DISCLOSED_NOTE = (
    "This metric is not disclosed by this entity in any year, and that has been established positively rather "
    "than by failing to find it. The entity has published exactly one Pillar 3 disclosure in its history, for "
    "31 December 2016; that document contains ZERO occurrences of \"Tier 1\", \"Tier 2\", \"own funds\", "
    "\"leverage\" and \"MREL\" across its whole 98,380-character text, while returning 38 hits for \"Pillar 3\" "
    "and 36 for \"liquidity\" in the same extraction, so the zeros are facts about the document. For every "
    "other year the only capital/liquidity disclosures are a narrative paragraph and Key Performance Indicator "
    "table in each Annual Report's Strategic Report - a single combined Total Capital Ratio (no CET1/Tier 1 "
    "breakdown), LCR and NSFR - plus, in the FY2018-FY2021 reports only, a Tier 1 resources table inside the "
    "Risk management note, which itemises Tier 1 and says nothing about ratios, leverage or MREL. The KPI-table "
    "format was only introduced from the FY2023 Annual Report onward; the FY2014-FY2022 reports discuss capital "
    "and liquidity only in qualitative terms, with no ratio figures of any kind. Full-text searches of the "
    "bank's own text-layer copies of the FY2021, FY2022, FY2024 and FY2025 reports (2026-09-18) return no "
    "leverage ratio and no MREL figure; the two \"leverage\" hits in the FY2024 and FY2025 reports are the verb "
    "(\"leverage Bank Mandiri Group's wholesale banking ecosystem\", \"a PD model that leverages the financial "
    "... macroeconomic series\"), not the ratio."
)


def p3_sources(extra=""):
    return (
        "Sources - Bank Mandiri (Europe) Limited (figures reported in US Dollars, converted to £ at the Bank of "
        "England GBP/USD spot rate as at each fiscal year-end - see FX conversion note below; % ratios shown "
        "exactly as reported, not converted):\n"
        f"FY2025 & FY2024: Bank Mandiri (Europe) Limited Annual Report FY2025, Strategic Report \"Key Performance "
        f"Indicator\" table, p.6 - {FY2025_AR_URL}\n"
        f"FY2024 (as originally reported) & FY2023: Bank Mandiri (Europe) Limited Annual Report FY2024, Strategic "
        f"Report \"Key Performance Indicator\" table, p.6 - {FY2024_AR_URL}\n"
        f"FY2023 (as originally reported) & FY2022: Bank Mandiri (Europe) Limited Annual Report FY2023, Strategic "
        f"Report \"Key Performance Indicator\" table, p.6 - {FY2023_AR_URL}\n"
        "FX rates (£1 = $X, Bank of England spot via poundsterlinglive.com): 31 Dec 2022 1.2097; 29 Dec 2023 "
        "1.2732 (31st was a Sunday); 31 Dec 2024 1.2515; 31 Dec 2025 1.3448.\n"
        f"TEXT-LAYER PRIMARY SOURCES (added 2026-09-15, preferred over the Companies House scans above): "
        f"FY2025 {SITE_AR2025_URL}; FY2024 {SITE_AR2024_URL}; FY2023 (scanned) {SITE_AR2023_URL}; "
        f"FY2022 {SITE_AR2022_URL}; FY2021 {SITE_AR2021_URL}\n"
        "RE-VERIFIED 2026-09-15 AGAINST MACHINE-READABLE ORIGINALS. Every ratio on these sheets was "
        "re-extracted from the bank's own text-layer PDFs and matches what was already recorded, to the digit "
        "and to the same precision: Total Capital Ratio FY2025 33.59%, FY2024 42.90%, FY2023 34.30%, FY2022 "
        "34.09%; LCR FY2025 446.89%, FY2024 382%, FY2023 264.29%, FY2022 147.59%; NSFR FY2025 121.85%, FY2024 "
        "142%, FY2023 131.85%, FY2022 143.26%; regulatory capital resources FY2025 US$56.4m, FY2024 US$54.3m, "
        "FY2023 US$52.3m, FY2022 US$49.71m. Each year is corroborated twice, because every report prints the "
        "prior year as a comparative. The FY2023 figures were confirmed by re-rendering the scanned FY2023 "
        "report at 500 dpi and re-OCR'ing the KPI table, after a 250 dpi pass returned the capital-ratio row as "
        "unreadable characters while the rows above and below came out cleanly - a reminder that a low-"
        "confidence OCR region must be magnified and re-read rather than accepted or skipped.\n"
        "DEFINITION CHECKED: the KPI table labels this row 'Total Capital Ratio' and prints its definition "
        "directly beneath as '(Own Funds / Total Risk Weighted Asset)'. That is a genuine CRR total capital "
        "ratio, so mapping it onto the Total Capital Ratio sheet is correct. This check matters because several "
        "banks in this project publish a similarly-named 'capital adequacy ratio' that turns out to be capital "
        "over a REQUIREMENT rather than over RWAs - Bank Saderat's 'Capital Cover' and Alpha Bank London's "
        "shareholders'-funds-over-RWA measure are both in that category and must not be mapped here.\n"
        f"PILLAR 3 HISTORY: the only Pillar 3 document this entity is known to have published covers FY2016 and "
        f"is now dead on the live site, surviving only in the Wayback Machine ({PILLAR3_2016_ARCHIVE_URL}). "
        f"Re-read in full on 2026-09-18, and it is NOT the narrative-only document an earlier note here "
        f"described: it is a CRD IV Pillar 3 & Remuneration Code disclosure carrying real quantitative tables, "
        f"and it is the only source in this entity's history that prints a risk-weighted-asset total (Total "
        f"Risk Exposure US$64,242k, p.11) or an eligible-capital total (Total Eligible Capital US$49,163k, "
        f"p.12). Both are now carried on the Total RWAs, Total Capital and RWA Breakdown sheets. It contains no "
        f"CET1/Tier 1/Tier 2 split, no leverage ratio, no capital RATIO and no LCR or NSFR, so it adds nothing "
        f"to the other metric sheets. The practice lapsed after that one edition, so it gives no reason to "
        f"expect a recent disclosure - but it does mean FY2016 is better documented than any year between it "
        f"and FY2022.\n"
        "LEVEL OF APPLICATION / PARENT DISCLOSURE (KM1 map rule 18), settled 2026-09-18 from the bank's own "
        "words. Section 1.4 \"Scope\" of the 2016 Pillar 3 states: \"BMEL operates solely without subsidiaries "
        "or affiliate companies included in its financial statements and, accordingly, these Pillar 3 "
        "disclosures apply entirely to BMEL.\" This entity discloses on a SOLO basis and is not consolidated "
        "into any UK parent's disclosure, so there is no UK parent Pillar 3 that could carry a subsidiary block "
        "for it. Its only parent is PT Bank Mandiri (Persero) Tbk, an Indonesian bank supervised by OJK, which "
        "carries neither a UK Disclosure (CRR) Article 433 duty nor an EU CRR Article 13(1) large-subsidiary "
        "duty - the two regimes that make a parent's Pillar 3 the normal home for a subsidiary's numbers. "
        "Stated plainly: bankmandiri.co.id was not read, because two attempts on 2026-09-18 returned an HTTP/2 "
        "INTERNAL_ERROR and then a 90-second timeout. That is a fact about the fetch and not about the parent; "
        "the conclusion above rests on the regime and on BMEL's own Scope paragraph, not on that failed fetch.\n"
        "COMPANIES HOUSE STATUS CHECKED 2026-09-18: company 03793679 is ACTIVE, SIC 64191 (Banks), last "
        "accounts made up to 31 December 2025 and filed 28 June 2026, next accounts to 31 December 2026 due "
        "30 September 2027, confirmation statement filed 23 June 2026 and a director appointed 10 July 2026. "
        "The entity has NOT wound down, surrendered its permission or deregistered, so none of the blank years "
        "below can be explained that way - they are years in which an operating, PRA-authorised bank simply "
        "published no regulatory disclosure.\n"
        "PRA WAIVERS REGISTER CHECKED 2026-09-18 (map rule 29): the Bank of England consolidated waivers "
        "register carries exactly one row for FRN 204424 - a direction for modification by consent of 5.1 to "
        "5.3 of the CAPITAL BUFFERS Part of the PRA Rulebook, ref 00007751, start date 12/04/2024, no end "
        "date. That is not an SDDT Regime General Application Rule 3.1 opt-in and removes no Pillar 3 "
        "disclosure duty; it also post-dates every year before FY2024, so it could not explain an earlier "
        "absence even if it were one. The years with no Pillar 3 therefore have no registered instrument "
        "behind them: the bank simply stopped publishing after 2016.\n"
        + (extra + "\n" if extra else "")
        + "FY2022's Total Capital Ratio/LCR/NSFR are sourced from the FY2023 Annual Report's own comparative column "
          "- the FY2022 Annual Report's own KPI table and Strategic Report do not include these figures at all "
          "(this KPI format was only introduced from the FY2023 report onward). FY2021 has no capital ratio, LCR "
          "or NSFR in any form: neither in the FY2022 Annual Report's comparative column nor in the FY2021 "
          "Annual Report itself, whose own text-layer copy was full-text searched on 2026-09-18 and returns zero "
          "hits on 'risk weighted', 'own funds', 'Total Capital Ratio' and 'liquidity coverage' against 43 hits "
          "on 'capital' in the same text - left blank, not estimated. HD-017 (2026-09-05) "
          "extended the source-year window back to FY2014 and confirmed this KPI-table format simply did not exist "
          "before FY2023: none of the FY2014-FY2020 Annual Reports checked contain a numeric capital or liquidity "
          "RATIO anywhere (Chairman's Statement, Strategic Report, or notes) - see NOT_DISCLOSED_NOTE. That "
          "remains true of the RATIO sheets. GA-005 (2026-09-18) qualifies it for the AMOUNT sheets, where it was "
          "over-broad: the FY2018-FY2021 reports each carry a 'regulatory Tier 1 resources' table inside the Risk "
          "management note (a different part of the document from the Strategic Report those passes searched), "
          "and the 2016 Pillar 3 carries both an RWA total and an eligible-capital total. Those are now on the "
          "CET1 Capital, Tier 1 Capital, Total Capital, Total RWAs and RWA Breakdown sheets. FY2014-FY2017 remain "
          "blank on every regulatory-metric sheet except the FY2016 column fed by the 2016 Pillar 3, and except "
          "FY2017's Tier 1 figure, which comes from the FY2018 edition's comparative.\n"
          "RE-VERIFIED 2026-09-12 (disclosure audit, independent of the 2026-09-08 RWA-only review): the FY2022 "
          "and FY2025 Annual Reports were re-downloaded from Companies House and OCR'd page-by-page (both are "
          "scanned, no text layer). Three findings, all confirming the existing treatment. (1) The FY2022 report "
          "contains no capital-adequacy ratio, no own-funds figure and no RWA figure anywhere - its KPI table "
          "carries only return on equity, return on assets, cost efficiency and yield on assets - so FY2021's "
          "capital RATIO, LCR and NSFR cannot be recovered from it (and, per the FY2021 report's own full-text "
          "search above, do not exist anywhere; FY2021's Tier 1 AMOUNT does exist and is on its sheets). "
          "(2) The FY2025 KPI table's capital line is a single combined "
          "'(Own Funds / Risk Weighted Asset) 33.59% 42.90%', and the Strategic Report narrative gives one "
          "combined amount ('The Bank's regulatory capital resources were US$56.4 million on 31 December 2025 "
          "(2024: US$54.3 million)') - there is no CET1/Tier 1/Tier 2 split to transcribe, confirming those four "
          "sheets' non-disclosure. (3) No leverage ratio appears in any form in either report."
    )


bw = BankWorkbook(bank_name="Bank Mandiri (Europe) Limited", years=YEARS, year_label=YEAR_LABEL, header_color="8B0000")

# ---------------------------------------------------------------
# ST- wayfinder map rollout (batch ST-011): Balance Sheet, Profit & Loss,
# Statement of Changes in Equity, Asset Quality, RWA Breakdown.
#
# All 5 years (FY2021-FY2025) were sourced by visually transcribing this
# entity's own scanned/image-only Companies House statutory accounts filings
# (fy2025.pdf, fy2024.pdf, fy2023.pdf, fy2022.pdf - all confirmed image-only
# via pdf_tools.py scan, 0 text blocks per page) via pdf_tools.py render +
# visual reading, per the project's established OCR/visual-transcription
# approach for scanned filings. FY2025's own report gives FY2025/FY2024;
# FY2024's own report gives FY2024/FY2023 (used to cross-check FY2024, which
# matched exactly); FY2023's own report gives FY2023/FY2022 (cross-checked
# FY2023, matched exactly); FY2022's own report gives FY2022/FY2021
# (cross-checked FY2022, matched exactly). Figures reported in US$'000
# (entity's functional currency), converted to £'000 at Bank of England
# GBP/USD spot rate for point-in-time (balance sheet, equity closing/opening
# balances) figures and calendar-year average rate for flow (P&L, equity
# in-year movement) figures - see FX_SPOT/FX_AVG/stock()/flow() above and
# the SMBC Bank International precedent this follows.
ST_ENTITY_NOTE = ENTITY_NOTE + (
    "\n\nAll years (FY2021-FY2025) sourced from this entity's own Companies House statutory accounts filings "
    "(all scanned/image-only PDFs - no text layer - visually transcribed page-by-page): Annual Report FY2025 "
    f"(Profit and Loss Account p.20, Statement of Comprehensive Income p.21, Balance Sheet p.22, Statement of "
    f"Changes in Equity p.23) - {FY2025_AR_URL}; Annual Report FY2024 (same page layout, FY2024/FY2023 columns) "
    f"- {FY2024_AR_URL}; Annual Report FY2023 (same page layout, FY2023/FY2022 columns) - {FY2023_AR_URL}; "
    "Annual Report FY2022 (Profit and Loss Account p.18, Statement of Comprehensive Income p.19, Balance Sheet "
    "p.20, Statement of Changes in Equity p.21, FY2022/FY2021 columns) - Companies House filing history, company "
    "03793679, accounts made up to 31 December 2022. Each year's own comparative column was cross-checked against "
    "the following year's report where both exist - all matched exactly, no discrepancies found.\n\n"
    "FX conversion: £1 = $X, Bank of England spot via poundsterlinglive.com. Spot rates (period-end, used for "
    "balance sheet and equity opening/closing balances): 31 Dec 2021 1.3728; 31 Dec 2022 1.2097 (30 Dec, 31st was "
    "a Saturday); 31 Dec 2023 1.2732 (29 Dec, 31st was a Sunday); 31 Dec 2024 1.2515; 31 Dec 2025 1.3448. Average "
    "rates (calendar-year mean of ~250 daily spot quotes, used for P&L and in-year equity movements): FY2021 "
    "1.3756; FY2022 1.2365; FY2023 1.2434; FY2024 1.2780; FY2025 1.3183."
    "\n\nHD-017 (2026-09-05): FY2014-FY2020 extended from the same Companies House filing history (all 7 filings "
    "confirmed image-only/0 text blocks per page via pdf_tools.py scan, visually transcribed page-by-page, same "
    "method as FY2021-FY2025 above). Balance Sheet/Profit and Loss Account/Statement of Comprehensive Income (or, "
    "pre-FY2016, the equivalent \"Statement of total recognised gains and losses\") page layout is consistent "
    "across all 7 filings but the exact page numbers printed in each report's own Contents page were found to be "
    "STALE for FY2016 and FY2017 (both filings' Contents pages under-count by 4 pages, apparently left over from "
    "before the extended Key Audit Matters auditor's report format was adopted - verified by rendering the pages "
    "the Contents page named and finding auditor's-report text there instead, then locating the true statement "
    "pages 4 pages later) - a caveat for anyone re-deriving these citations from the Contents page alone rather "
    "than the statement's own printed page number, which is what is cited below:\n"
    f"FY2020 Annual Report (P&L p.15, Statement of Comprehensive Income p.16, Balance Sheet p.17, Statement of "
    f"Change in Equity p.18, FY2020/FY2019 columns) - {FY2020_AR_URL}\n"
    f"FY2019 Annual Report (P&L p.17, SOCI p.18, Balance Sheet p.19, Statement of Change in Equity p.20, "
    f"FY2019/FY2018 columns) - {FY2019_AR_URL}\n"
    f"FY2018 Annual Report (P&L p.15, SOCI p.16, Balance Sheet p.17, Statement of Change in Equity p.18 - this "
    f"page also shows the FY2017 movement block in full, i.e. FY2016/FY2017/FY2018 combined - FY2018/FY2017 "
    f"columns on P&L/BS/SOCI) - {FY2018_AR_URL}\n"
    f"FY2017 Annual Report (P&L printed p.13, SOCI printed p.14, Balance Sheet printed p.15, Statement of Change "
    f"in Equity printed p.16 - NOT the p.9-12 the Contents page names, see stale-pagination caveat above - "
    f"FY2017/FY2016 columns) - {FY2017_AR_URL}\n"
    f"FY2016 Annual Report (P&L printed p.9, SOCI printed p.10, Balance Sheet printed p.11, Statement of Change "
    f"in Equity printed p.12, FY2016/FY2015 columns) - {FY2016_AR_URL}\n"
    f"FY2015 Annual Report (P&L p.9, \"Statement of total recognised gains and losses\" p.10 - pre-FY2016 "
    f"terminology, economically equivalent to the FY2016+ Statement of Comprehensive Income - Balance Sheet p.11, "
    f"Statement of Change in Equity p.12, FY2015/FY2014 columns) - {FY2015_AR_URL}\n"
    f"FY2014 Annual Report: Chairman's Statement (p.2) cross-checked for narrative confirmation only - FY2014's "
    f"own P&L/Balance Sheet/equity figures were taken from the FY2015 Annual Report's FY2014 comparative column "
    f"and FY2015's Statement of Change in Equity (which gives the 1 January 2014 opening equity balance and the "
    f"FY2014 movement block in full) rather than re-transcribing FY2014's own statement pages a second time - "
    f"{FY2014_AR_URL}\n"
    "Each year's own comparative column was cross-checked against the adjacent year's report where both exist - "
    "all matched exactly except one immaterial rounding-scale artefact in the FY2016 Statement of Change in "
    "Equity's AFS-reserve rounding (\"(11974)\" shown without a thousands comma on one row only - a formatting "
    "quirk of that one filing, not a numeric discrepancy).\n\n"
    "BALANCE SHEET STRUCTURE CHANGES over FY2014-FY2020: (1) \"Right of use assets\" (asset) and \"Lease "
    "liability\" only appear from the FY2019 Annual Report onward (IFRS 16 adoption) - blank, not zero, for "
    "FY2014-FY2018. (2) \"Current tax liability\" and \"Deferred tax liability\" are only broken out as separate "
    "line items from the FY2018 Annual Report onward - FY2014-FY2017's own filings show a single combined \"Other "
    "liabilities, accruals and deferred income\" line only (the FY2018 report's own FY2017 comparative column "
    "later split this same total into three lines, but FY2017's own filing - the authoritative source used here "
    "- did not) - the combined figure is shown in \"Other liabilities, accruals and deferred income\" for "
    "FY2014-FY2017, with Current/Deferred tax liability left blank rather than estimated. (3) The FY2014-FY2016 "
    "P&L uses \"Recoveries from bad and doubtful debts\" (same sign convention: positive = credit/write-back) "
    "where FY2018 onward uses \"Loan impairment losses - write-back/(charge)\" - both are shown on the same row. "
    "FY2017's own P&L omits this line entirely for both FY2017 and FY2016 (the year's profit reconciles exactly "
    "without it, confirming a true nil/immaterial year, not an omission) - left blank for FY2017.\n\n"
    "OTHER COMPREHENSIVE INCOME STRUCTURE CHANGES: pre-FY2018 filings use \"available-for-sale\" (AFS) "
    "terminology for the debt-securities fair-value reserve; FY2018 onward uses \"FVTOCI\" (fair value through "
    "other comprehensive income) following IFRS 9 adoption - both are the same underlying reserve and are shown "
    "on the same \"Change in fair value of investments (AFS/FVOCI)\" row. FY2014-FY2015 show only a single "
    "combined tax line against this reserve movement (\"Current UK corporation tax (charge)/credit on change in "
    "fair value of investments available-for-sale\"); FY2016 onward split this into a \"transitional adjustment\" "
    "component and a \"financial instruments\" component (plus, from FY2019, a separate \"current charge on "
    "transitional adjustment\" line) - each year's own most granular disclosure is used, with blanks where a "
    "component was not separately disclosed that year."
)

BALANCE_SHEET_USD = {
    "Cash and cash equivalent": {"FY2025": 3_622_000, "FY2024": 14_000_000, "FY2023": 17_781_000, "FY2022": 30_448_000, "FY2021": 31_508_000, "FY2020": 35_972_000, "FY2019": 30_989_000, "FY2018": 14_729_000, "FY2017": 12_225_000, "FY2016": 30_677_000, "FY2015": 33_140_000, "FY2014": 34_620_000},
    "Loan and advances to banks": {"FY2025": 29_404_000, "FY2024": 30_509_000, "FY2023": 34_531_000, "FY2022": 37_011_000, "FY2021": 19_985_000, "FY2020": 19_989_000, "FY2019": 45_985_000, "FY2018": 38_996_000, "FY2017": 17_005_000, "FY2016": 0, "FY2015": 40_000_000, "FY2014": 64_000_000},
    "Loan and advances to customers": {"FY2025": 131_430_000, "FY2024": 88_010_000, "FY2023": 87_428_000, "FY2022": 74_065_000, "FY2021": 59_912_000, "FY2020": 42_748_000, "FY2019": 59_044_000, "FY2018": 76_535_000, "FY2017": 88_506_000, "FY2016": 93_240_000, "FY2015": 74_148_000, "FY2014": 68_247_000},
    "Debt securities": {"FY2025": 132_298_000, "FY2024": 128_310_000, "FY2023": 118_990_000, "FY2022": 99_423_000, "FY2021": 71_107_000, "FY2020": 55_542_000, "FY2019": 49_136_000, "FY2018": 43_158_000, "FY2017": 38_504_000, "FY2016": 49_172_000, "FY2015": 36_240_000, "FY2014": 20_854_000},
    # ST-011 follow-up (2026-09-07): Note 10 "Debt Securities" in each year's own Annual Report
    # (Note 12/13 pre-2022, renumbered to Note 10 from the FY2022 Annual Report onward) breaks the
    # "Debt securities" balance-sheet line into a real, exactly-reconciling split by BOTH
    # measurement basis (FVOCI, called "available-for-sale"/AFS pre-FY2018) and issuer type
    # (government/gilts vs other banks/corporates) - see DEBT_SECURITIES_SOURCES below for the
    # full per-year note/page citations. "Pledged as collateral" sub-amounts shown as a separate
    # issuer-type line in the FY2020-FY2022 Annual Reports' own note are folded into "other
    # (banks/corporates)" below - confirmed by the following year's own Annual Report re-presenting
    # that same prior-year comparative column collapsed into exactly two issuer buckets (government
    # vs other), with the former "pledged as collateral" amount landing inside "other" every time
    # this was checked (FY2021's, FY2022's, and FY2023's own comparative columns all confirm this).
    "Debt securities — FVOCI/AFS, UK government & gilts": {"FY2025": 63_187_000, "FY2024": 59_748_000, "FY2023": 40_521_000, "FY2022": 18_205_000, "FY2021": 24_596_000, "FY2020": 10_103_000, "FY2019": 17_617_000, "FY2018": 16_745_000, "FY2017": 17_391_000, "FY2016": 19_979_000, "FY2015": 13_584_000, "FY2014": 9_684_000},
    "Debt securities — FVOCI/AFS, other (banks & corporates)": {"FY2025": 28_736_000, "FY2024": 22_299_000, "FY2023": 30_480_000, "FY2022": 35_561_000, "FY2021": 36_311_000, "FY2020": 37_508_000, "FY2019": 18_544_000, "FY2018": 8_501_000, "FY2017": 1_069_000, "FY2016": 14_403_000, "FY2015": 22_656_000, "FY2014": 11_170_000},
    # Amortised cost (called "held-to-maturity"/HTM pre-FY2018) by issuer only broken out from the
    # FY2022 Annual Report onward (both years disclosed there — FY2022 and its FY2021 comparative —
    # each showing a nil/"-" government line, i.e. 100% banks/corporates); FY2016-FY2020's own Annual
    # Reports show only a single undifferentiated amortised-cost/HTM total with no issuer split at
    # all (see the "(issuer split not disclosed)" row below for those 5 years); FY2014-FY2015 had no
    # amortised-cost/HTM holdings whatsoever (both years' own notes show FVOCI/AFS as 100% of the
    # balance, confirmed by the FVOCI/AFS sub-rows above reconciling to the FULL "Debt securities"
    # total with nothing left over) - left blank for FY2014-FY2015, not zero, per this project's
    # missing-vs-nil convention.
    "Debt securities — amortised cost/HTM, UK government & gilts": {"FY2025": 9_414_000, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0},
    "Debt securities — amortised cost/HTM, other (banks & corporates)": {"FY2025": 30_962_000, "FY2024": 46_263_000, "FY2023": 47_989_000, "FY2022": 45_657_000, "FY2021": 10_200_000},
    "Debt securities — amortised cost/HTM (issuer split not disclosed)": {"FY2020": 7_931_000, "FY2019": 12_974_000, "FY2018": 17_911_000, "FY2017": 20_044_000, "FY2016": 14_790_000},
    "Tangible fixed assets": {"FY2025": 14_000, "FY2024": 14_000, "FY2023": 2_000, "FY2022": 6_000, "FY2021": 15_000, "FY2020": 50_000, "FY2019": 86_000, "FY2018": 93_000, "FY2017": 129_000, "FY2016": 162_000, "FY2015": 7_000, "FY2014": 13_000},
    "Intangible fixed assets": {"FY2025": 179_000, "FY2024": 187_000, "FY2023": 3_000, "FY2022": 3_000, "FY2021": 16_000, "FY2020": 50_000, "FY2019": 70_000, "FY2018": 53_000, "FY2017": 43_000, "FY2016": 247_000, "FY2015": 419_000, "FY2014": 431_000},
    "Right of use assets": {"FY2025": 106_000, "FY2024": 235_000, "FY2023": 381_000, "FY2022": 499_000, "FY2021": 37_000, "FY2020": 129_000, "FY2019": 276_000},  # not applicable pre-FY2019 (IFRS 16 adoption) - blank, not zero
    "Other assets, prepayments and accrued income": {"FY2025": 1_296_000, "FY2024": 507_000, "FY2023": 448_000, "FY2022": 442_000, "FY2021": 776_000, "FY2020": 556_000, "FY2019": 693_000, "FY2018": 444_000, "FY2017": 325_000, "FY2016": 539_000, "FY2015": 524_000, "FY2014": 306_000},
    "Total assets": {"FY2025": 298_349_000, "FY2024": 261_772_000, "FY2023": 259_564_000, "FY2022": 241_897_000, "FY2021": 183_356_000, "FY2020": 155_036_000, "FY2019": 186_279_000, "FY2018": 174_008_000, "FY2017": 156_737_000, "FY2016": 174_037_000, "FY2015": 184_478_000, "FY2014": 188_471_000},
    "Deposit from banks": {"FY2025": 236_320_000, "FY2024": 201_729_000, "FY2023": 189_826_000, "FY2022": 172_796_000, "FY2021": 113_533_000, "FY2020": 95_940_000, "FY2019": 112_774_000, "FY2018": 119_484_000, "FY2017": 103_486_000, "FY2016": 119_682_000, "FY2015": 134_977_000, "FY2014": 132_442_000},
    "Customer accounts": {"FY2025": 4_190_000, "FY2024": 4_298_000, "FY2023": 15_674_000, "FY2022": 17_526_000, "FY2021": 15_862_000, "FY2020": 4_374_000, "FY2019": 20_195_000, "FY2018": 4_708_000, "FY2017": 1_893_000, "FY2016": 4_325_000, "FY2015": 1_901_000, "FY2014": 6_789_000},
    "Other liabilities, accruals and deferred income": {"FY2025": 953_000, "FY2024": 1_150_000, "FY2023": 1_234_000, "FY2022": 1_195_000, "FY2021": 1_279_000, "FY2020": 1_386_000, "FY2019": 954_000, "FY2018": 457_000, "FY2017": 951_000, "FY2016": 867_000, "FY2015": 585_000, "FY2014": 664_000},  # FY2014-FY2017: combined figure - see ST_ENTITY_NOTE (tax liabilities not split out until FY2018)
    "Lease liability": {"FY2025": 106_000, "FY2024": 235_000, "FY2023": 381_000, "FY2022": 499_000, "FY2021": 37_000, "FY2020": 129_000, "FY2019": 276_000},  # not applicable pre-FY2019 (IFRS 16 adoption) - blank, not zero
    "Current tax liability": {"FY2025": 296_000, "FY2024": 106_000, "FY2023": 126_000, "FY2022": 167_000, "FY2021": 69_000, "FY2020": 99_000, "FY2019": 138_000, "FY2018": 101_000},  # not split out pre-FY2018 - see ST_ENTITY_NOTE
    "Deferred tax liability": {"FY2022": 0, "FY2021": 87_000, "FY2020": 201_000, "FY2019": 106_000, "FY2018": 59_000},  # nil FY2023-25; blank FY2022 shown as "-" (nil) in source; not split out pre-FY2018
    "Total liabilities excluding shareholders' funds": {"FY2025": 241_865_000, "FY2024": 207_518_000, "FY2023": 207_241_000, "FY2022": 192_183_000, "FY2021": 130_867_000, "FY2020": 102_129_000, "FY2019": 134_443_000, "FY2018": 124_809_000, "FY2017": 106_330_000, "FY2016": 124_874_000, "FY2015": 137_463_000, "FY2014": 139_895_000},
    "Called up share capital": {"FY2025": 49_000_000, "FY2024": 49_000_000, "FY2023": 49_000_000, "FY2022": 49_000_000, "FY2021": 49_000_000, "FY2020": 49_000_000, "FY2019": 49_000_000, "FY2018": 49_000_000, "FY2017": 49_000_000, "FY2016": 49_000_000, "FY2015": 49_000_000, "FY2014": 49_000_000},
    "Capital reserve": {"FY2025": 11_496_000, "FY2024": 11_496_000, "FY2023": 11_496_000, "FY2022": 11_496_000, "FY2021": 11_496_000, "FY2020": 11_496_000, "FY2019": 11_496_000, "FY2018": 11_496_000, "FY2017": 11_496_000, "FY2016": 11_496_000, "FY2015": 11_496_000, "FY2014": 11_496_000},
    "Revaluation reserve": {"FY2025": 637_000, "FY2024": -317_000, "FY2023": -1_189_000, "FY2022": -2_959_000, "FY2021": 425_000, "FY2020": 1_219_000, "FY2019": 588_000, "FY2018": -1_386_000, "FY2017": 107_000, "FY2016": -535_000, "FY2015": -2_067_000, "FY2014": 54_000},
    "Profit and loss account": {"FY2025": -4_649_000, "FY2024": -5_925_000, "FY2023": -6_984_000, "FY2022": -7_823_000, "FY2021": -8_432_000, "FY2020": -8_808_000, "FY2019": -9_248_000, "FY2018": -9_911_000, "FY2017": -10_196_000, "FY2016": -10_798_000, "FY2015": -11_414_000, "FY2014": -11_974_000},
    "Total shareholders' funds": {"FY2025": 56_484_000, "FY2024": 54_254_000, "FY2023": 52_323_000, "FY2022": 49_714_000, "FY2021": 52_489_000, "FY2020": 52_907_000, "FY2019": 51_836_000, "FY2018": 49_199_000, "FY2017": 50_407_000, "FY2016": 49_163_000, "FY2015": 47_015_000, "FY2014": 48_576_000},
    "Total liabilities and shareholders' funds": {"FY2025": 298_349_000, "FY2024": 261_772_000, "FY2023": 259_564_000, "FY2022": 241_897_000, "FY2021": 183_356_000, "FY2020": 155_036_000, "FY2019": 186_279_000, "FY2018": 174_008_000, "FY2017": 156_737_000, "FY2016": 174_037_000, "FY2015": 184_478_000, "FY2014": 188_471_000},
}
BS = {k: stock(v) for k, v in BALANCE_SHEET_USD.items()}

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalent", BS["Cash and cash equivalent"]),
    ("DATA", "Loan and advances to banks", BS["Loan and advances to banks"]),
    ("DATA", "Loan and advances to customers", BS["Loan and advances to customers"]),
    ("DATA", "Total debt securities", BS["Debt securities"]),
    ("DATA", "Debt securities — FVOCI/AFS, UK government & gilts", BS["Debt securities — FVOCI/AFS, UK government & gilts"]),
    ("DATA", "Debt securities — FVOCI/AFS, other (banks & corporates)", BS["Debt securities — FVOCI/AFS, other (banks & corporates)"]),
    ("DATA", "Debt securities — amortised cost/HTM, UK government & gilts", BS["Debt securities — amortised cost/HTM, UK government & gilts"]),
    ("DATA", "Debt securities — amortised cost/HTM, other (banks & corporates)", BS["Debt securities — amortised cost/HTM, other (banks & corporates)"]),
    ("DATA", "Debt securities — amortised cost/HTM (issuer split not disclosed)", BS["Debt securities — amortised cost/HTM (issuer split not disclosed)"]),
    ("DATA", "Tangible fixed assets", BS["Tangible fixed assets"]),
    ("DATA", "Intangible fixed assets", BS["Intangible fixed assets"]),
    ("DATA", "Right of use assets", BS["Right of use assets"]),
    ("DATA", "Other assets, prepayments and accrued income", BS["Other assets, prepayments and accrued income"]),
    ("TOTAL", "Total assets", BS["Total assets"]),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposit from banks", BS["Deposit from banks"]),
    ("DATA", "Customer accounts", BS["Customer accounts"]),
    ("DATA", "Other liabilities, accruals and deferred income", BS["Other liabilities, accruals and deferred income"]),
    ("DATA", "Lease liability", BS["Lease liability"]),
    ("DATA", "Current tax liability", BS["Current tax liability"]),
    ("DATA", "Deferred tax liability", BS["Deferred tax liability"]),
    ("TOTAL", "Total liabilities excluding shareholders' funds", BS["Total liabilities excluding shareholders' funds"]),
    ("SECTION", "Shareholders' funds", {}),
    ("DATA", "Called up share capital", BS["Called up share capital"]),
    ("DATA", "Capital reserve", BS["Capital reserve"]),
    ("DATA", "Revaluation reserve", BS["Revaluation reserve"]),
    ("DATA", "Profit and loss account", BS["Profit and loss account"]),
    ("TOTAL", "Total shareholders' funds — equity interests", BS["Total shareholders' funds"]),
    ("TOTAL", "Total liabilities and shareholders' funds", BS["Total liabilities and shareholders' funds"]),
]

DEBT_SECURITIES_SOURCES = (
    "\n\nDEBT SECURITIES BREAKDOWN (added 2026-09-07): each year's own Annual Report's \"Debt Securities\" note "
    "(Note 10 from the FY2022 Annual Report onward; Note 12 in the FY2016/FY2020 Annual Reports; Note 13 in the "
    "FY2015 Annual Report) splits the Balance Sheet's single \"Debt securities\" line by measurement basis "
    "(FVOCI, called \"available-for-sale\"/AFS pre-FY2018; and amortised cost, called \"held-to-maturity\"/HTM "
    "pre-FY2018) and, within FVOCI/AFS, by issuer type (government/gilts vs other banks/corporates):\n"
    f"FY2025/FY2024 — Annual Report FY2025, Note 10 \"Debt Securities\", p.38 — {FY2025_AR_URL}\n"
    f"FY2024/FY2023 comparative — Annual Report FY2024, Note 10, p.37-38 — {FY2024_AR_URL}\n"
    f"FY2023/FY2022 comparative — Annual Report FY2023, Note 10, p.37 — {FY2023_AR_URL}\n"
    f"FY2022/FY2021 comparative — Annual Report FY2022, Note 10, p.36 — {FY2022_AR_URL}\n"
    f"FY2020/FY2019 comparative — Annual Report FY2020, Note 12, p.36-37 — {FY2020_AR_URL}\n"
    f"FY2018/FY2017 comparative — Annual Report FY2018, Note 12, p.37-38 — {FY2018_AR_URL}\n"
    f"FY2016/FY2015 comparative — Annual Report FY2016, Note 12, p.24 — {FY2016_AR_URL}\n"
    f"FY2015/FY2014 comparative — Annual Report FY2015, Note 13, p.25 — {FY2015_AR_URL}\n"
    "Each year's own comparative column was cross-checked against the adjacent year's report where both exist — "
    "all matched exactly except three immaterial ($1k) rounding artefacts already present WITHIN the source "
    "documents themselves (i.e. not introduced by this transcription): the FY2025 Annual Report's own FY2025 "
    "FVOCI government+other subtotal (63,187+28,736=91,923) is $1k above its own printed FVOCI total (91,922); "
    "the FY2020 Annual Report's own FY2019 comparative government+other subtotal (17,617+18,544=36,161) is $1k "
    "below its own printed FVOCI total (36,162); and the FY2018 Annual Report's own FY2018 government+other "
    "subtotal (16,745+8,501=25,246) is $1k below its own printed FVOCI total (25,247). The sub-row figures below "
    "are transcribed exactly as printed in each source; the parent \"Total debt securities\" row is unaffected "
    "(it is the Balance Sheet's own total, not a re-sum of the sub-rows).\n\n"
    "\"PLEDGED AS COLLATERAL\" TREATMENT: the FY2020-FY2022 Annual Reports' own FVOCI/AFS note presents amounts "
    "\"pledged as collateral\" as a third issuer-type line sitting between \"government securities\" and \"other "
    "debt securities — banks/corporates\". These are folded into \"other (banks & corporates)\" below, not "
    "government — confirmed because each of those years' own comparative column, when re-presented the "
    "following year in only two issuer buckets (government vs other), lands the former \"pledged as collateral\" "
    "amount inside \"other\" every time (checked for the FY2020→FY2021, FY2021→FY2022 and FY2022→FY2023 "
    "transitions).\n\n"
    "AMORTISED COST / HTM ISSUER SPLIT: only broken out by issuer from the FY2022 Annual Report onward (both "
    "FY2022 and its FY2021 comparative show a nil/\"-\" government line, i.e. 100% banks/corporates that both "
    "years). The FY2016-FY2020 Annual Reports' own amortised-cost/HTM note gives only a single undifferentiated "
    "total with no issuer breakdown at all — shown in the \"(issuer split not disclosed)\" row rather than "
    "assumed to be 100% banks/corporates. FY2014-FY2015 held no amortised-cost/HTM investments at all (both "
    "years' FVOCI/AFS sub-rows reconcile to the FULL \"Debt securities\" total with nothing left over) — left "
    "blank for FY2014-FY2015, not zero."
)

BALANCE_SHEET_SOURCES = (
    "Sources — Bank Mandiri (Europe) Limited's own Balance Sheet, converted from USD to £'000 at the Bank of "
    "England GBP/USD spot rate as at each fiscal year-end (point-in-time figures — see FX conversion note below):\n"
    + ST_ENTITY_NOTE
    + DEBT_SECURITIES_SOURCES
)

bw.add_balance_sheet_sheet(
    title="Bank Mandiri (Europe) Limited — Balance Sheet",
    subtitle="£'000, converted from USD — see source note for FX methodology and rates used. Entity-level basis (no subsidiaries).",
    rows=balance_sheet_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=52,
    source_height=420,
)

INCOME_STATEMENT_USD = {
    "Interest receivable": {"FY2025": 13_124_000, "FY2024": 13_430_000, "FY2023": 11_175_000, "FY2022": 6_198_000, "FY2021": 4_431_000, "FY2020": 5_100_000, "FY2019": 6_505_000, "FY2018": 5_839_000, "FY2017": 4_804_000, "FY2016": 4_285_000, "FY2015": 3_590_000, "FY2014": 3_247_000},
    "Interest payable": {"FY2025": -8_080_000, "FY2024": -8_683_000, "FY2023": -6_790_000, "FY2022": -2_546_000, "FY2021": -928_000, "FY2020": -1_528_000, "FY2019": -2_940_000, "FY2018": -2_714_000, "FY2017": -1_435_000, "FY2016": -1_135_000, "FY2015": -568_000, "FY2014": -349_000},
    "Net interest income": {"FY2025": 5_044_000, "FY2024": 4_747_000, "FY2023": 4_385_000, "FY2022": 3_652_000, "FY2021": 3_503_000, "FY2020": 3_572_000, "FY2019": 3_565_000, "FY2018": 3_125_000, "FY2017": 3_369_000, "FY2016": 3_150_000, "FY2015": 3_022_000, "FY2014": 2_898_000},
    "Fees and commissions receivable": {"FY2025": 311_000, "FY2024": 446_000, "FY2023": 243_000, "FY2022": 205_000, "FY2021": 246_000, "FY2020": 328_000, "FY2019": 255_000, "FY2018": 104_000, "FY2017": 59_000, "FY2016": 34_000, "FY2015": 11_000, "FY2014": 5_000},
    "Other operating income": {"FY2025": 461_000, "FY2024": 184_000, "FY2023": 378_000, "FY2022": 472_000, "FY2021": 90_000, "FY2020": 31_000, "FY2019": 171_000, "FY2018": 148_000, "FY2017": 202_000, "FY2016": 456_000, "FY2015": 696_000, "FY2014": 1_043_000},
    "Total operating income": {"FY2025": 5_816_000, "FY2024": 5_377_000, "FY2023": 5_006_000, "FY2022": 4_329_000, "FY2021": 3_839_000, "FY2020": 3_931_000, "FY2019": 3_991_000, "FY2018": 3_377_000, "FY2017": 3_630_000, "FY2016": 3_640_000, "FY2015": 3_729_000, "FY2014": 3_946_000},
    "Administrative expenses": {"FY2025": -4_072_000, "FY2024": -3_963_000, "FY2023": -3_328_000, "FY2022": -3_269_000, "FY2021": -3_012_000, "FY2020": -3_305_000, "FY2019": -2_981_000, "FY2018": -2_740_000, "FY2017": -2_576_000, "FY2016": -2_821_000, "FY2015": -3_024_000, "FY2014": -3_361_000},
    "Depreciation and amortisation": {"FY2025": -199_000, "FY2024": -183_000, "FY2023": -150_000, "FY2022": -168_000, "FY2021": -230_000, "FY2020": -228_000, "FY2019": -223_000, "FY2018": -77_000, "FY2017": -244_000, "FY2016": -222_000, "FY2015": -186_000, "FY2014": -19_000},
    # FY2014-FY2016 disclosed as "Recoveries from bad and doubtful debts" (same sign convention: positive=credit).
    # FY2017's own P&L omits this line entirely for both FY2017 and FY2016 (profit reconciles exactly without it,
    # confirming a true nil year, not an omission) - left blank for FY2017. See ST_ENTITY_NOTE.
    "Loan impairment losses — write-back/(charge)": {"FY2025": 27_000, "FY2024": 22_000, "FY2023": -427_000, "FY2022": -116_000, "FY2021": -123_000, "FY2020": 65_000, "FY2019": -46_000, "FY2018": -147_000, "FY2016": 0, "FY2015": 164_000, "FY2014": 309_000},
    "Profit on ordinary activities before tax": {"FY2025": 1_572_000, "FY2024": 1_253_000, "FY2023": 1_101_000, "FY2022": 776_000, "FY2021": 474_000, "FY2020": 463_000, "FY2019": 741_000, "FY2018": 413_000, "FY2017": 810_000, "FY2016": 597_000, "FY2015": 683_000, "FY2014": 875_000},
    "Taxation (charge)/credit": {"FY2025": -296_000, "FY2024": -194_000, "FY2023": -262_000, "FY2022": -167_000, "FY2021": -98_000, "FY2020": -23_000, "FY2019": -78_000, "FY2018": -128_000, "FY2017": -208_000, "FY2016": 19_000, "FY2015": -123_000, "FY2014": 204_000},
    "Profit on ordinary activities after tax": {"FY2025": 1_276_000, "FY2024": 1_059_000, "FY2023": 839_000, "FY2022": 609_000, "FY2021": 376_000, "FY2020": 440_000, "FY2019": 663_000, "FY2018": 285_000, "FY2017": 602_000, "FY2016": 616_000, "FY2015": 560_000, "FY2014": 1_079_000},
    # OCI: pre-FY2018 "available-for-sale" (AFS) terminology; FY2018+ "FVTOCI" (IFRS 9). Same reserve, same row.
    "Change in fair value of investments measured at FVOCI": {"FY2025": 954_000, "FY2024": 872_000, "FY2023": 1_770_000, "FY2022": -3_384_000, "FY2021": -938_000, "FY2020": 801_000, "FY2019": 2_100_000, "FY2018": -1_574_000, "FY2017": 642_000, "FY2016": 1_688_000, "FY2015": -2_244_000, "FY2014": 710_000},
    # FY2014-FY2015 only: single combined tax line against the AFS reserve movement (not split into
    # transitional-adjustment/financial-instruments components as FY2016 onward does) - see ST_ENTITY_NOTE.
    "Current UK corporation tax (charge)/credit on fair value of investments (AFS, FY2014-FY2015 only)": {"FY2015": 123_000, "FY2014": -204_000},
    # FY2019-FY2020 only: a distinct "current charge" component alongside the deferred-tax transitional line below.
    "Current (charge) on FVTOCI transitional adjustment (FY2019-FY2020 only)": {"FY2020": -41_000, "FY2019": -41_000},
    "Deferred tax (charge)/credit on AFS/FVTOCI transitional adjustment": {"FY2020": -152_000, "FY2019": -136_000, "FY2018": 62_000, "FY2017": 105_000, "FY2016": -261_000},
    "Deferred tax credit on FVTOCI financial instruments": {"FY2021": 178_000, "FY2020": 41_000, "FY2019": 41_000, "FY2018": 29_000, "FY2017": -124_000, "FY2016": 98_000},  # nil/not disclosed other years
    "Effects of changes in tax rate": {"FY2021": -34_000, "FY2020": -18_000, "FY2019": 10_000, "FY2018": -10_000, "FY2017": 19_000, "FY2016": 8_000},  # nil/not disclosed other years
    "Total comprehensive income/(loss) for the period": {"FY2025": 2_230_000, "FY2024": 1_931_000, "FY2023": 2_609_000, "FY2022": -2_775_000, "FY2021": -418_000, "FY2020": 1_071_000, "FY2019": 2_637_000, "FY2018": -1_208_000, "FY2017": 1_244_000, "FY2016": 2_149_000, "FY2015": -1_561_000, "FY2014": 1_585_000},
}
IS_USD = INCOME_STATEMENT_USD
IS = {k: flow(v) for k, v in IS_USD.items()}

income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable", IS["Interest receivable"]),
    ("DATA", "Interest payable", IS["Interest payable"]),
    ("TOTAL", "Net interest income", IS["Net interest income"]),
    ("DATA", "Fees and commissions receivable", IS["Fees and commissions receivable"]),
    ("DATA", "Other operating income", IS["Other operating income"]),
    ("TOTAL", "Total operating income", IS["Total operating income"]),
    ("SECTION", "Expenses", {}),
    ("DATA", "Administrative expenses", IS["Administrative expenses"]),
    ("DATA", "Depreciation and amortisation", IS["Depreciation and amortisation"]),
    ("DATA", "Loan impairment losses — write-back/(charge)", IS["Loan impairment losses — write-back/(charge)"]),
    ("TOTAL", "Profit on ordinary activities before tax", IS["Profit on ordinary activities before tax"]),
    ("DATA", "Taxation (charge)/credit", IS["Taxation (charge)/credit"]),
    ("TOTAL", "Profit on ordinary activities after tax", IS["Profit on ordinary activities after tax"]),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Change in fair value of investments measured at FVOCI", IS["Change in fair value of investments measured at FVOCI"]),
    ("DATA", "Current UK corporation tax (charge)/credit on fair value of investments (AFS, FY2014-FY2015 only)", IS["Current UK corporation tax (charge)/credit on fair value of investments (AFS, FY2014-FY2015 only)"]),
    ("DATA", "Current (charge) on FVTOCI transitional adjustment (FY2019-FY2020 only)", IS["Current (charge) on FVTOCI transitional adjustment (FY2019-FY2020 only)"]),
    ("DATA", "Deferred tax (charge)/credit on AFS/FVTOCI transitional adjustment", IS["Deferred tax (charge)/credit on AFS/FVTOCI transitional adjustment"]),
    ("DATA", "Deferred tax credit on FVTOCI financial instruments", IS["Deferred tax credit on FVTOCI financial instruments"]),
    ("DATA", "Effects of changes in tax rate", IS["Effects of changes in tax rate"]),
    ("TOTAL", "Total comprehensive income/(loss) for the period", IS["Total comprehensive income/(loss) for the period"]),
]

INCOME_STATEMENT_SOURCES = (
    "Sources — Bank Mandiri (Europe) Limited's own Profit and Loss Account and Statement of Comprehensive Income, "
    "converted from USD to £'000 at the Bank of England GBP/USD calendar-year average spot rate (flow figures — "
    "see FX conversion note below):\n"
    + ST_ENTITY_NOTE
    + "\n\nFY2022 and FY2021's OCI detail (deferred tax credit on FVTOCI, effects of tax rate changes) is disclosed "
      "only for FY2021 in the FY2022 Annual Report's own comparative column — FY2022's own OCI detail below the "
      "fair-value-change line was reported as nil/not itemised. Total comprehensive income/(loss) is the one row "
      "genuinely comparable and populated across all 5 years.\n\n"
      "HD-017: FY2014-FY2020's OCI tax-line breakdown changed structure repeatedly across the extended window — "
      "FY2014-FY2015 disclose a single combined tax line against the AFS reserve movement; FY2016-FY2018 split "
      "this into a 'transitional adjustment' component and a 'financial instruments' component; FY2019-FY2020 add "
      "a third 'current charge on transitional adjustment' component alongside the deferred one. Each year's own "
      "most granular disclosure is used, with blanks (not zeros) for components not separately disclosed that "
      "year — the 'Total comprehensive income/(loss)' row is, as with FY2021-FY2025, the one row genuinely "
      "comparable across every year in the full FY2014-FY2025 window; each year's own component rows reconcile "
      "exactly to it (profit + all populated OCI component rows = total, verified for every year FY2014-FY2020)."
)
# (FY2021 gap note removed by GA-005 - the gap is closed; see EQUITY_CHANGES_SOURCES.)

bw.add_income_statement_sheet(
    title="Bank Mandiri (Europe) Limited — Profit and Loss Account and Statement of Comprehensive Income",
    subtitle="£'000, converted from USD — see source note for FX methodology and rates used. Entity-level basis (no subsidiaries).",
    rows=income_statement_rows,
    sources_text=INCOME_STATEMENT_SOURCES,
    first_col_width=58,
    source_height=280,
)

EQUITY_HEADERS = ["Share capital", "Capital reserve", "Revaluation reserve", "Profit and loss account", "Total shareholders' funds"]

# Build each movement row directly in £'000 (inputs are US$'000), using spot rate for balance rows
# (opening/closing — point-in-time) and average rate for movement rows
# (in-year flows), consistent with BS/IS above.
def bal(usd_thousands, year):
    return tuple(round(v / FX_SPOT[year], 0) if v is not None else None for v in usd_thousands)

def mov(usd_thousands, year):
    return tuple(round(v / FX_AVG[year], 0) if v is not None else None for v in usd_thousands)

# Opening ("At 1 January Y") rows are the SAME point in time as the prior
# year's "At 31 December" row (31 December Y-1) - both must therefore use
# that same 31-December spot rate (FX_SPOT["FY"+str(Y-1)]), not year Y's own
# rate, or the roll-forward would show a false discontinuity purely from an
# FX-rate mismatch. Caught and fixed this exact bug before finalizing.
#
# Even with that fix, opening (prior year's spot rate) + this year's
# movements (this year's AVERAGE rate) does not exactly equal closing (this
# year's own spot rate) in £ terms, even though it does exactly in $ terms -
# because three different GBP/USD rates are in play across one year's
# block. This is a real currency-translation artifact (the same phenomenon
# SMBC Bank International's Cash Flow Statement handles with an explicit
# "Effect of GBP/USD translation" line - see build_smbc.py), not a data
# error. An explicit "FX translation effect on equity, net" row (Total
# column only - there is no currency-translation-reserve component in this
# entity's own accounts to attribute it to) absorbs the gap so opening +
# movements + this line = closing exactly, each year.
FX_TRANSLATION_EFFECT = {
    "FY2022": 5105, "FY2023": -2099, "FY2024": 744, "FY2025": -3041,
    # GA-005 (2026-09-18): FY2021 added once the FY2021 Statement of change in equity was read.
    "FY2021": -224,
    # HD-017: FY2014-FY2020, computed the same way (closing - opening - sum of movement rows, £'000, per year).
    "FY2014": 1738, "FY2015": 1619, "FY2016": 6675, "FY2017": -3618, "FY2018": 2118, "FY2019": -1355, "FY2020": -1316,
}

# 31 December 2013 GBP/USD spot rate (poundsterlinglive.com Bank of England archive) - FY2013 is not
# itself a covered year, this is used only to convert the equity sheet's very first opening balance
# (1 January 2014 = 31 December 2013, the same point in time) at the correct period-end rate.
FX_SPOT["FY2013"] = 1.6528

equity_changes_rows = [
    # HD-017: FY2014-FY2020 roll-forward, chained from the 1 January 2014 opening balance disclosed in
    # the FY2015 Annual Report's Statement of Change in Equity (which shows the full FY2014 movement
    # block) through to the FY2020 Annual Report's own closing balance. Each year's own filing's actual
    # reserve-movement line items are reproduced as disclosed (2 lines pre-FY2018, 3 from FY2018 onward
    # once a separate UK corporation tax line on the AFS/FVTOCI reserve starts being shown directly in
    # the equity statement) - see ST_ENTITY_NOTE / EQUITY_CHANGES_SOURCES for the full sourcing and the
    # FY2016 closing AFS-reserve scan-legibility note.
    ("TOTAL", "At 1 January 2014", bal((49000, 11496, -452, -13053, 46991), "FY2013")),
    ("DATA", "Realised to profit and loss", mov((None, None, 127, None, 127), "FY2014")),
    ("DATA", "Increase in fair value of debt securities", mov((None, None, 379, None, 379), "FY2014")),
    ("DATA", "Profit for the year", mov((None, None, None, 1079, 1079), "FY2014")),
    ("DATA", "FX translation effect on equity, net (£'000, see FX conversion note)", (None, None, None, None, FX_TRANSLATION_EFFECT["FY2014"])),
    ("TOTAL", "At 31 December 2014", bal((49000, 11496, 54, -11974, 48576), "FY2014")),
    ("TOTAL", "At 1 January 2015", bal((49000, 11496, 54, -11974, 48576), "FY2014")),
    ("DATA", "Realised to profit and loss", mov((None, None, -317, None, -317), "FY2015")),
    ("DATA", "Decrease in fair value of debt securities", mov((None, None, -1804, None, -1804), "FY2015")),
    ("DATA", "Profit for the year", mov((None, None, None, 560, 560), "FY2015")),
    ("DATA", "FX translation effect on equity, net (£'000, see FX conversion note)", (None, None, None, None, FX_TRANSLATION_EFFECT["FY2015"])),
    ("TOTAL", "At 31 December 2015", bal((49000, 11496, -2067, -11414, 47015), "FY2015")),
    ("TOTAL", "At 1 January 2016", bal((49000, 11496, -2067, -11414, 47015), "FY2015")),
    ("DATA", "Realised to profit and loss", mov((None, None, 852, None, 852), "FY2016")),
    ("DATA", "Increase in fair value of debt securities", mov((None, None, 680, None, 680), "FY2016")),
    ("DATA", "Profit for the year", mov((None, None, None, 616, 616), "FY2016")),
    ("DATA", "FX translation effect on equity, net (£'000, see FX conversion note)", (None, None, None, None, FX_TRANSLATION_EFFECT["FY2016"])),
    ("TOTAL", "At 31 December 2016", bal((49000, 11496, -535, -10798, 49163), "FY2016")),
    ("TOTAL", "At 1 January 2017", bal((49000, 11496, -535, -10798, 49163), "FY2016")),
    ("DATA", "Realised to profit and loss", mov((None, None, 117, None, 117), "FY2017")),
    ("DATA", "Increase in fair value of debt securities", mov((None, None, 525, None, 525), "FY2017")),
    ("DATA", "Profit for the year", mov((None, None, None, 602, 602), "FY2017")),
    ("DATA", "FX translation effect on equity, net (£'000, see FX conversion note)", (None, None, None, None, FX_TRANSLATION_EFFECT["FY2017"])),
    ("TOTAL", "At 31 December 2017", bal((49000, 11496, 107, -10196, 50407), "FY2017")),
    ("TOTAL", "At 1 January 2018", bal((49000, 11496, 107, -10196, 50407), "FY2017")),
    ("DATA", "Realised to profit and loss", mov((None, None, 44, None, 44), "FY2018")),
    ("DATA", "Decrease in fair value of debt securities", mov((None, None, -1618, None, -1618), "FY2018")),
    ("DATA", "UK corporation tax credit on fair value of financial instruments at FVTOCI", mov((None, None, 81, None, 81), "FY2018")),
    ("DATA", "Profit for the year", mov((None, None, None, 285, 285), "FY2018")),
    ("DATA", "FX translation effect on equity, net (£'000, see FX conversion note)", (None, None, None, None, FX_TRANSLATION_EFFECT["FY2018"])),
    ("TOTAL", "At 31 December 2018", bal((49000, 11496, -1386, -9911, 49199), "FY2018")),
    ("TOTAL", "At 1 January 2019", bal((49000, 11496, -1386, -9911, 49199), "FY2018")),
    ("DATA", "Increase in fair value of debt securities", mov((None, None, 2100, None, 2100), "FY2019")),
    ("DATA", "UK corporation tax charged on fair value of financial instruments at FVTOCI", mov((None, None, -126, None, -126), "FY2019")),
    ("DATA", "Profit for the year", mov((None, None, None, 663, 663), "FY2019")),
    ("DATA", "FX translation effect on equity, net (£'000, see FX conversion note)", (None, None, None, None, FX_TRANSLATION_EFFECT["FY2019"])),
    ("TOTAL", "At 31 December 2019", bal((49000, 11496, 588, -9248, 51836), "FY2019")),
    ("TOTAL", "At 1 January 2020", bal((49000, 11496, 588, -9248, 51836), "FY2019")),
    ("DATA", "Increase in fair value of debt securities", mov((None, None, 801, None, 801), "FY2020")),
    ("DATA", "UK corporation tax charged on fair value of financial instruments at FVTOCI", mov((None, None, -170, None, -170), "FY2020")),
    ("DATA", "Profit for the year", mov((None, None, None, 440, 440), "FY2020")),
    ("DATA", "FX translation effect on equity, net (£'000, see FX conversion note)", (None, None, None, None, FX_TRANSLATION_EFFECT["FY2020"])),
    ("TOTAL", "At 31 December 2020", bal((49000, 11496, 1219, -8808, 52907), "FY2020")),
    # GA-005 (2026-09-18): the FY2021 gap is CLOSED. The FY2021 Annual Report does carry a full Statement of
    # change in equity (printed p.20) with a "At 1 January 2021" opening row; the 2026-09-15 session that
    # first fetched that filing read its Note 24(H) capital table but not its equity statement.
    ("TOTAL", "At 1 January 2021", bal((49000, 11496, 1219, -8808, 52907), "FY2020")),
    ("DATA", "Decrease in fair value of debt securities", mov((None, None, -938, None, -938), "FY2021")),
    ("DATA", "UK corporation tax credit on fair value of financial instruments at FVTOCI", mov((None, None, 144, None, 144), "FY2021")),
    ("DATA", "Profit for the year", mov((None, None, None, 376, 376), "FY2021")),
    ("DATA", "FX translation effect on equity, net (£'000, see FX conversion note)", (None, None, None, None, FX_TRANSLATION_EFFECT["FY2021"])),
    ("TOTAL", "At 31 December 2021", bal((49000, 11496, 425, -8432, 52489), "FY2021")),
    ("TOTAL", "At 1 January 2022", bal((49000, 11496, 425, -8432, 52489), "FY2021")),
    ("DATA", "Decrease in fair value of debt securities", mov((None, None, -3384, None, -3384), "FY2022")),
    ("DATA", "Profit for the year", mov((None, None, None, 609, 609), "FY2022")),
    ("DATA", "FX translation effect on equity, net (£'000, see FX conversion note)", (None, None, None, None, FX_TRANSLATION_EFFECT["FY2022"])),
    ("TOTAL", "At 31 December 2022", bal((49000, 11496, -2959, -7823, 49714), "FY2022")),
    ("TOTAL", "At 1 January 2023", bal((49000, 11496, -2959, -7823, 49714), "FY2022")),
    ("DATA", "Increase in fair value of debt securities", mov((None, None, 1770, None, 1770), "FY2023")),
    ("DATA", "Profit for the year", mov((None, None, None, 839, 839), "FY2023")),
    ("DATA", "FX translation effect on equity, net (£'000, see FX conversion note)", (None, None, None, None, FX_TRANSLATION_EFFECT["FY2023"])),
    ("TOTAL", "At 31 December 2023", bal((49000, 11496, -1189, -6984, 52323), "FY2023")),
    ("TOTAL", "At 1 January 2024", bal((49000, 11496, -1189, -6984, 52323), "FY2023")),
    ("DATA", "Increase in fair value of debt securities", mov((None, None, 872, None, 872), "FY2024")),
    ("DATA", "Profit for the year", mov((None, None, None, 1059, 1059), "FY2024")),
    ("DATA", "FX translation effect on equity, net (£'000, see FX conversion note)", (None, None, None, None, FX_TRANSLATION_EFFECT["FY2024"])),
    ("TOTAL", "At 31 December 2024", bal((49000, 11496, -317, -5925, 54254), "FY2024")),
    ("TOTAL", "At 1 January 2025", bal((49000, 11496, -317, -5925, 54254), "FY2024")),
    ("DATA", "Increase in fair value of debt securities", mov((None, None, 954, None, 954), "FY2025")),
    ("DATA", "Profit for the year", mov((None, None, None, 1276, 1276), "FY2025")),
    ("DATA", "FX translation effect on equity, net (£'000, see FX conversion note)", (None, None, None, None, FX_TRANSLATION_EFFECT["FY2025"])),
    ("TOTAL", "At 31 December 2025", bal((49000, 11496, 637, -4649, 56484), "FY2025")),
]

EQUITY_CHANGES_SOURCES = (
    "Sources — Bank Mandiri (Europe) Limited's own Statement of Change in Equity, converted from USD to £'000 "
    "(balance/opening/closing rows at that date's spot rate; movement rows at that year's average rate — see FX "
    "conversion note below):\n"
    + ST_ENTITY_NOTE
    + "\n\nHD-017 (FY2014-FY2020 extension): the roll-forward from 1 January 2014 through 31 December 2020 is "
      "chained year-by-year off each own year's Annual Report Statement of Change in Equity (2 reserve-movement "
      "lines — 'realised to P&L' and 'increase/(decrease) in fair value of debt securities' — through FY2017; a "
      "third 'UK corporation tax credit/(charge) on fair value of financial instruments at FVTOCI' line from "
      "FY2018 onward, once that entity begins showing the tax effect directly within the equity statement rather "
      "than only within the P&L/OCI note). FY2015 and FY2016 were separated using each year's OWN Annual Report "
      "(FY2016's report was used in preference to FY2017's combined/ambiguous '1 January 2015' opening row, which "
      "arithmetically reconciles to the 31 December 2015 balance, not a genuine 1 January 2015 balance — treated "
      "as a mislabelled row in the FY2017 filing and disregarded). The FY2016 closing revaluation/FVOCI reserve is "
      "recorded here as £(535)k, not the £(627)k that a literal read of the FY2016 filing's own equity statement's "
      "scanned closing cell suggests — £(535)k is corroborated independently by both the FY2016 Balance Sheet's own "
      "reserve line and by the arithmetic of that year's roll-forward (opening £(2,067)k + realised £852k + "
      "increase £680k = £(535)k), so the scanned £(627)k is treated as an OCR/legibility misread of one digit. The "
      "1 January 2014 opening balance is converted at the 31 December 2013 GBP/USD spot rate (not itself a covered "
      "year in this workbook — sourced separately, see FX_SPOT['FY2013'] in the build script) since that date is "
      "the same point in time as the FY2013 year-end.\n\n"
      "FY2021 — GAP CLOSED, GA-005 (2026-09-18). This sheet previously jumped from 31 December 2020 straight to "
      "1 January 2022, on the stated basis that the FY2021 Annual Report had never been sourced and that the "
      "FY2022 report shows no 1 January 2021 opening row. The first half of that had already stopped being true "
      "on 2026-09-15, when the FY2021 filing was found and used for the Tier 1 capital table; what that session "
      "did not do was open the same document's Statement of change in equity. It is there, printed p.20, and it "
      "carries the full FY2021 roll-forward: At 1 January 2021 US$52,907k total (share capital 49,000, capital "
      "reserve 11,496, revaluation reserve 1,219, profit and loss (8,808)); Decrease in fair value of debt "
      "securities (938); UK corporation tax credit on fair value of financial instruments at FVTOCI 144; Profit "
      "for the year 376; At 31 December 2021 US$52,489k (49,000 / 11,496 / 425 / (8,432)). The column foots "
      f"exactly and the opening row equals the 31 December 2020 closing row above. Source: Annual Report FY2021, "
      f"Statement of change in equity, p.20 — {FY2021_AR_URL}. The equity statement presents the FVTOCI tax "
      "effect as one combined US$144k line, where the Profit & Loss sheet reproduces the more granular "
      "presentation the same report's OCI note uses (deferred tax credit $178k plus a $(34)k effect of changes "
      "in tax rate); 178 - 34 = 144, so the two agree. Each sheet reproduces the table it comes from.\n\n"
      "FX TRANSLATION EFFECT: each year's opening balance is converted at the PRIOR year-end's spot rate (the same "
      "point in time as that row, so opening always exactly equals the prior year's closing row); each year's "
      "movement rows (FVOCI change, profit) are converted at that year's AVERAGE rate, consistent with the "
      "Profit & Loss sheet; each year's closing balance is converted at that year's OWN year-end spot rate. Because "
      "three different GBP/USD rates are used within one year's block, opening + movements does not exactly equal "
      "closing in £ terms even though it does exactly in $ terms (Bank Mandiri Europe's underlying accounts have "
      "no currency-translation-reserve component to attribute this to, unlike a genuine multi-currency group). The "
      "explicit 'FX translation effect on equity, net' row absorbs this gap so the roll-forward ties exactly every "
      "year — it is a pure artefact of £ conversion, not a real equity movement, the same treatment SMBC Bank "
      "International plc's Cash Flow Statement sheet uses for its analogous 'Effect of GBP/USD translation' line."
)

bw.add_equity_changes_sheet(
    title="Bank Mandiri (Europe) Limited — Statement of Change in Equity",
    subtitle="£'000, converted from USD — see source note for FX methodology and rates used. Chronological, oldest to newest, 1 January 2014 to 31 December 2025 (FY2021 gap — see source note).",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQUITY_CHANGES_SOURCES,
    first_col_width=32,
    source_height=280,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (exemption note in place of line items)
# ---------------------------------------------------------------
rows = [
    ("SECTION", "No Statement of Cash Flows is published by this entity in any year", {}),
    ("DATA", "See the note below for the FRS 101 exemption this entity relies on every year, and why this "
             "workbook is built as a Pillar-3-only variant.", {}),
]

bw.add_cash_flow_sheet(
    title="Bank Mandiri (Europe) Limited — Cash Flow Statement",
    subtitle="Not applicable — this entity takes the FRS 101 cash-flow-statement disclosure exemption every year. See source note below.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=300,
    unit_suffix="",
)

# ---------------------------------------------------------------
# Asset Quality (loans and advances to customers by credit quality + ECL)
# ---------------------------------------------------------------
# GA-005 (2026-09-18): EVERY Annual Report from FY2014 to FY2025 carries a
# "Credit quality per class of financial assets" table inside its Risk
# management note, and so does the 2016 Pillar 3. The earlier claim that the
# table was absent before FY2024 was wrong; all twelve years are populated
# below, each from its OWN edition.
#
# The table changes presentation at IFRS 9 adoption and the two presentations
# are NOT merged, because they measure different things:
#   FY2018-FY2025 - columns "Neither past due nor impaired" / "12-mo ECL" /
#       "Total". Loss allowances are measured on ALL financial assets at
#       12-month expected credit losses (the note says so in terms).
#   FY2014-FY2017 - columns "Neither past due nor impaired (Current)" /
#       "Impaired" / "Total". No ECL column exists; the Impaired column is
#       printed "-" in every one of those four years.
# No Stage 1/2/3 lifetime-ECL split is disclosed in any year, and no
# non-performing or Stage 3 loan balance appears anywhere in any edition, so
# no NPL/Stage 3 ratio is presented.
ASSET_QUALITY_USD = {
    # IFRS 9 presentation, FY2018-FY2025
    "Sub-investment grade (rated below Baa3 by Moody's) — gross": {"FY2025": 4_814_000},
    "Sub-investment grade (rated below Baa3 by Moody's) — 12-mo ECL": {"FY2025": -57_000},
    "Unrated — gross": {
        "FY2025": 127_274_000, "FY2024": 88_401_000, "FY2023": 87_748_000, "FY2022": 74_202_000,
        "FY2021": 59_961_000, "FY2020": 42_782_000, "FY2019": 59_104_000, "FY2018": 76_571_000,
    },
    "Unrated — 12-mo ECL": {
        "FY2025": -601_000, "FY2024": -391_000, "FY2023": -320_000, "FY2022": -137_000,
        "FY2021": -49_000, "FY2020": -34_000, "FY2019": -60_000, "FY2018": -36_000,
    },
    "Total gross loans and advances to customers": {
        "FY2025": 132_088_000, "FY2024": 88_401_000, "FY2023": 87_748_000, "FY2022": 74_202_000,
        "FY2021": 59_961_000, "FY2020": 42_782_000, "FY2019": 59_104_000, "FY2018": 76_571_000,
    },
    "Total 12-mo ECL allowance": {
        "FY2025": -658_000, "FY2024": -391_000, "FY2023": -320_000, "FY2022": -137_000,
        "FY2021": -49_000, "FY2020": -34_000, "FY2019": -60_000, "FY2018": -36_000,
    },
    "Total net loans and advances to customers": {
        "FY2025": 131_430_000, "FY2024": 88_010_000, "FY2023": 87_428_000, "FY2022": 74_065_000,
        "FY2021": 59_912_000, "FY2020": 42_748_000, "FY2019": 59_044_000, "FY2018": 76_535_000,
    },
    # Pre-IFRS 9 presentation, FY2014-FY2017 (no ECL column; "Impaired" instead)
    "Unrated — neither past due nor impaired (pre-IFRS 9)": {
        "FY2017": 88_506_000, "FY2016": 93_240_000, "FY2015": 74_148_000, "FY2014": 68_247_000,
    },
    "Total loans and advances to customers (pre-IFRS 9 presentation)": {
        "FY2017": 88_506_000, "FY2016": 93_240_000, "FY2015": 74_148_000, "FY2014": 68_247_000,
    },
}
AQ = {k: stock(v) for k, v in ASSET_QUALITY_USD.items()}
# The pre-IFRS 9 table prints "-" on the sub-investment-grade and Impaired rows in all
# four years. A printed dash is the bank saying the row does not apply to it, which is a
# different statement from silence, so it is reproduced as a dash rather than blanked.
DASH4 = {y: "-" for y in ("FY2017", "FY2016", "FY2015", "FY2014")}
# CALCULATED, not disclosed: 12-mo ECL allowance / gross loans, to 2 d.p., for the eight
# years where the bank prints both components. Blank for FY2014-FY2017, which have no
# ECL allowance to divide by (their Impaired column is a dash, not a zero).
ECL_COVERAGE = {
    "FY2025": "0.50%", "FY2024": "0.44%", "FY2023": "0.36%", "FY2022": "0.18%",
    "FY2021": "0.08%", "FY2020": "0.08%", "FY2019": "0.10%", "FY2018": "0.05%",
}

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, by credit quality — IFRS 9 presentation (FY2018-FY2025)", {}),
    ("DATA", "Sub-investment grade (rated below Baa3 by Moody's) — gross", AQ["Sub-investment grade (rated below Baa3 by Moody's) — gross"]),
    ("DATA", "Sub-investment grade (rated below Baa3 by Moody's) — 12-mo ECL", AQ["Sub-investment grade (rated below Baa3 by Moody's) — 12-mo ECL"]),
    ("DATA", "Unrated — gross", AQ["Unrated — gross"]),
    ("DATA", "Unrated — 12-mo ECL", AQ["Unrated — 12-mo ECL"]),
    ("TOTAL", "Total gross loans and advances to customers", AQ["Total gross loans and advances to customers"]),
    ("DATA", "Total 12-mo ECL allowance", AQ["Total 12-mo ECL allowance"]),
    ("TOTAL", "Total net loans and advances to customers", AQ["Total net loans and advances to customers"]),
    ("SECTION", "Loans and advances to customers, by credit quality — pre-IFRS 9 presentation (FY2014-FY2017)", {}),
    ("DATA", "Sub-investment grade — neither past due nor impaired (pre-IFRS 9)", DASH4),
    ("DATA", "Unrated — neither past due nor impaired (pre-IFRS 9)", AQ["Unrated — neither past due nor impaired (pre-IFRS 9)"]),
    ("DATA", "Impaired (pre-IFRS 9)", DASH4),
    ("TOTAL", "Total loans and advances to customers (pre-IFRS 9 presentation)", AQ["Total loans and advances to customers (pre-IFRS 9 presentation)"]),
    ("SECTION", "Ratios (calculated)", {}),
    ("DATA", "ECL coverage ratio (12-mo ECL allowance ÷ gross loans)", ECL_COVERAGE),
]

ASSET_QUALITY_SOURCES = (
    "Sources — Bank Mandiri (Europe) Limited's own \"Credit quality per class of financial assets\" table, which "
    "sits inside the Risk management note of every Annual Report from FY2014 to FY2025. Only the \"Loans and "
    "advances to customers\" rows are reproduced here. Figures converted from USD to £'000 at each year-end's "
    "Bank of England GBP/USD spot rate (see FX conversion note below). EACH YEAR IS TAKEN FROM ITS OWN EDITION, "
    "and each was independently confirmed against the adjacent edition's comparative column for the same date — "
    "all twelve agreed digit for digit:\n"
    f"FY2025 & FY2024 comparative — Annual Report FY2025, Note 23, pp.49-50 — {FY2025_AR_URL}\n"
    f"FY2024 & FY2023 comparative — Annual Report FY2024, Note 23, p.50 — {FY2024_AR_URL}\n"
    f"FY2023 & FY2022 comparative — Annual Report FY2023, Note 23, p.49 — {FY2023_AR_URL}\n"
    f"FY2022 & FY2021 comparative — Annual Report FY2022, Note 23, p.49 — {FY2022_AR_URL}\n"
    f"FY2021 & FY2020 comparative — Annual Report FY2021, Note 24, p.51 — {FY2021_AR_URL}\n"
    f"FY2020 & FY2019 comparative — Annual Report FY2020, Note 24, p.49 — {FY2020_AR_URL}\n"
    f"FY2019 & FY2018 comparative — Annual Report FY2019, Note 24, pp.51-52 — {FY2019_AR_URL}\n"
    f"FY2018 & FY2017 comparative — Annual Report FY2018, Note 24, pp.50-51 — {FY2018_AR_URL}\n"
    f"FY2017 & FY2016 comparative — Annual Report FY2017, Note 24, pp.40-41 — {FY2017_AR_URL}\n"
    f"FY2016 & FY2015 comparative — Annual Report FY2016, Note 26, pp.36-37 — {FY2016_AR_URL}\n"
    f"FY2015 & FY2014 comparative — Annual Report FY2015, Note 27, pp.37-38 — {FY2015_AR_URL}\n"
    f"FY2014 & FY2013 comparative — Annual Report FY2014, Note 24, pp.31-32 — {FY2014_AR_URL}\n"
    f"FY2016 is additionally corroborated a THIRD time by the bank's 2016 Pillar 3 disclosure, printed p.28, "
    f"which reproduces the same table for 31 December 2016 and 31 December 2015 with identical figures — "
    f"{PILLAR3_2016_ARCHIVE_URL}\n\n"
    "TWO PRESENTATIONS, DELIBERATELY NOT MERGED. From the FY2018 Annual Report onward the table's second column "
    "is \"12-mo ECL\" and the note states that loss allowances are measured on all financial assets at an amount "
    "equal to 12-month expected credit losses. In the FY2014-FY2017 editions the second column is \"Impaired\" "
    "and there is no ECL concept at all; the loans rows print \"-\" in that column in all four years, and \"-\" "
    "on the sub-investment-grade line. Those dashes are reproduced as dashes, not converted to zeros and not "
    "blanked: the bank printed something, and what it printed was \"not applicable to us\".\n\n"
    "SOURCE DEFECT, RECORDED NOT CORRECTED (FY2014). The FY2014 Annual Report's own table prints the Unrated "
    "loans row as \"68,247 - 166,308\": the Total column carries 166,308, which is the PRIOR year's unrated "
    "loans figure (31 December 2013), not FY2014's. The row does not foot, while the table's own Total line "
    "(188,022) does foot to the five \"neither past due nor impaired\" figures including 68,247. The FY2015 "
    "Annual Report's FY2014 comparative prints the row correctly as \"68,247 - 68,247\". 68,247 is carried "
    "here; the misprinted 166,308 is recorded in this note rather than reproduced as a figure. Confirmed by two "
    "independent renderings of the FY2014 page at 300 dpi and 500 dpi, which agree digit for digit, so the "
    "166,308 is the document's and not an extraction artefact.\n\n"
    "SOURCING METHOD. The FY2021, FY2022, FY2024 and FY2025 Annual Reports are text-layer PDFs (the bank hosts "
    "its own copies) and were read directly. The FY2014-FY2020 and FY2023 filings are image-only scans with no "
    "text layer and were recovered by page-image OCR at 300 dpi, with every figure re-read at 500 dpi or "
    "confirmed against a text-layer edition's comparative column before use.\n\n"
    "No Stage 1/2/3 IFRS 9 staging split is disclosed in any year — every row carries only an aggregate 12-month "
    "ECL — and this entity discloses no non-performing or Stage 3 loan balance anywhere in any edition, so no "
    "NPL/Stage 3 ratio is presented here. The ECL coverage ratio row is CALCULATED (12-mo ECL allowance ÷ gross "
    "loans), not directly disclosed, and is shown only for the eight years where the bank prints both "
    "components.\n\n"
    + ENTITY_NOTE
)

bw.add_asset_quality_sheet(
    title="Bank Mandiri (Europe) Limited — Asset Quality",
    subtitle="£'000, converted from USD — see source note for FX methodology, rates used, and years covered.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=64,
    source_height=280,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=170)


TOTAL_CAPITAL_USD = {"FY2025": 56_400_000, "FY2024": 54_300_000, "FY2023": 52_300_000, "FY2022": 49_710_000}
CAR = {"FY2025": "33.59%", "FY2024": "42.90%", "FY2023": "34.30%", "FY2022": "34.09%"}

# ---------------------------------------------------------------
# THE FINDING GOES IN THE CELL, NOT ONLY IN THE NOTE (remaining-gap round,
# 18 September 2026). Nothing below is new research. Every one of these 31
# sheet-years was ALREADY established as a non-disclosure, with evidence, in
# TIER1_SOURCES / P3_2016_NOTE / RWA_BREAKDOWN_SOURCES / KM1_SOURCES - some of it
# re-gathered three times. What was wrong is WHERE it was written: a finding that
# lives only in a note= string is invisible to audit_gaps.py, which reads the year
# grid, so this workbook scored 31 untouched unexplained gaps while carrying the
# answer to all of them a few rows below. These short cell statements move the
# finding into the grid; the evidence stays in the notes.
#
# THE SHAPE OF THIS WORKBOOK'S GAP IS THE ANSWER TO IT, and it is worth stating
# plainly because it looks like a bank that stopped disclosing and is not. Capital
# is populated FY2017-FY2021 and empty FY2022-FY2025; Total Capital is the exact
# reverse. That is not one series with a hole in it - it is TWO DIFFERENT SOURCE
# DOCUMENTS meeting at a break:
#   - FY2017-FY2021: the "Capital adequacy risk" note in the FY2018-FY2021 Annual
#     Reports tabulates "the regulatory Tier 1 resources of the Bank" - Tier 1
#     ONLY, with no Tier 2, no total own funds, no RWA and no ratio. So those
#     years have a Tier 1/CET1 figure and CANNOT have a Total Capital one.
#   - FY2022-FY2025: that table is gone from the reports. What replaces it is a
#     single narrative sentence in the Strategic Report giving one combined
#     "regulatory capital resources" amount - a total, with no CET1/Tier 1/Tier 2
#     split. So those years have a Total Capital figure and CANNOT have a
#     CET1/Tier 1 one.
# Neither document type ever prints an RWA, which is why Total RWAs and RWA
# Breakdown are blank in BOTH halves and carry FY2016 alone, from the bank's only
# Pillar 3 disclosure.
#
# RE-VERIFIED INDEPENDENTLY THIS SESSION rather than inherited. The FY2025 and
# FY2024 Annual Reports were re-fetched from the bank's own site (HTTP 200,
# application/pdf, %PDF- magic, 1,681,014 and 285,830 bytes) and re-extracted:
# 162,945 and 161,914 characters, matching the counts already on record to the
# digit. RICHNESS CONTROL FIRST - 'the ' returns 1,357 and 1,334 hits and
# 'capital' 31 and 28, so the extraction is sound. Against that, BOTH reports
# return ZERO hits for 'tier 1', 'tier one', 'pillar 3', 'pillar 1', 'cet1',
# 'common equity', 'leverage ratio' and '12.5'. Every 'risk-weighted' / 'RWA' /
# 'own funds' hit was read in context and is one of exactly two things: the
# narrative "the decrease in CAR reflects an increase in risk-weighted assets",
# and the KPI parenthetical "(Own Funds / Total Risk Weighted Asset)". Neither
# carries a number. The only capital amount in the FY2025 report is the sentence
# "The Bank's regulatory capital resources were US$56.4 million on 31 December
# 2025 (2024: US$54.3 million)" - the two values TOTAL_CAPITAL_USD already holds.
# The bank's legal page was re-enumerated the same day (HTTP 200 with a browser
# UA; a plain curl gets 403) and lists 14 PDFs with ZERO occurrences of "pillar".
# ---------------------------------------------------------------
_NO_RWA_LATE = "Not disclosed - AR prints the Own Funds / Total RWA ratio but no RWA amount"
_NO_RWA_EARLY = "Not disclosed - AR capital note tabulates Tier 1 resources only, no RWA line"
NO_RWA = {
    # FY2022-FY2025: text-layer PDFs on the bank's own site, searched in full.
    "FY2025": _NO_RWA_LATE, "FY2024": _NO_RWA_LATE, "FY2023": _NO_RWA_LATE, "FY2022": _NO_RWA_LATE,
    # FY2017-FY2021: image-only Companies House scans (FY2019/FY2018/FY2017 yield
    # 57/56/47 characters of text layer for 57/56/51 pages), re-rendered and OCR'd
    # page-by-page at 250 dpi, plus the FY2021 report's own text layer.
    "FY2021": _NO_RWA_EARLY, "FY2020": _NO_RWA_EARLY, "FY2019": _NO_RWA_EARLY,
    "FY2018": _NO_RWA_EARLY, "FY2017": _NO_RWA_EARLY,
}
# The two halves of the capital break described above, each stated from the side
# of the break the reader is standing on.
NO_TIER1_SPLIT = {y: "Not disclosed - Tier 1 resources table dropped from FY2022 AR onward; only a combined capital figure is given"
                  for y in ("FY2025", "FY2024", "FY2023", "FY2022")}
NO_TOTAL_CAPITAL = {y: "Not disclosed - the FY2018-FY2021 capital note tabulates Tier 1 only; no Tier 2 or total own funds line"
                    for y in ("FY2021", "FY2020", "FY2019", "FY2018", "FY2017")}
# RWA_USD removed 2026-09-15 - those four values (FY2022-FY2025) were BACK-SOLVED as
# Own Funds / Total Capital Ratio, never disclosed, and stay withdrawn. Nothing below
# reinstates them. What IS below is a different thing entirely: an RWA total the bank
# actually printed, for one year only.

# ---------------------------------------------------------------
# The 2016 Pillar 3 - the one regulatory disclosure this entity has ever published,
# and the only source in its whole history that prints a risk-weighted-asset figure
# or an eligible-capital figure. Found by GA-005 (2026-09-18). The document had been
# fetched before, but only searched for UK KM1 template vocabulary ("KM1", "CET1",
# "own funds", "leverage ratio"), all of which are genuinely absent from it - it
# pre-dates that template by six years. It was described as "narrative" on the
# strength of those zeros. It is not: it is a CRD IV Pillar 3 & Remuneration Code
# disclosure carrying real quantitative tables, in the Bank's own house vocabulary
# ("Total Risk Exposure", "Total Eligible Capital"), which is why a template-word
# search found nothing. Text-native, 33 pages, read in full with pdftotext -layout.
P3_2016_TOTAL_RWA_USD = {"FY2016": 64_242_000}          # "Total Risk Exposure", printed p.11
P3_2016_ELIGIBLE_CAPITAL_USD = {"FY2016": 49_163_000}   # "Total Eligible Capital", printed p.12

P3_2016_NOTE = (
    "THE 2016 PILLAR 3 IS THE ONLY SOURCE IN THIS ENTITY'S HISTORY THAT PRINTS AN RWA OR ELIGIBLE-CAPITAL "
    "FIGURE. \"Bank Mandiri (Europe) Limited - Pillar 3 Disclosures as at 31st December 2016\", 33 pages, "
    f"text-native, single column headed \"Dec-16\" in U$'000 - {PILLAR3_2016_ARCHIVE_URL}. The document is dead "
    "on the live site and survives only in the Wayback Machine. As printed, p.11: Risk weighted assets for "
    "credit risk 57,663; Risk exposure for operational risk 6,579; Risk exposure for market risk \"-\"; Total "
    "Risk Exposure 64,242. p.12: Total Eligible Capital 49,163, against a Total Capital Requirement of 25,529 "
    "measured against the ICG ratio and 28,053 measured against the trigger ratio. The Total Eligible Capital "
    "figure equals the FY2016 Balance Sheet's own Total shareholders' funds (US$49,163k) to the digit, which is "
    "an independent corroboration from a separate document.\n"
    "WHAT THE DOCUMENT DOES NOT CONTAIN, checked with a richness control (map rule 15): zero occurrences of "
    "\"Tier 1\", \"Tier 2\", \"own funds\", \"leverage\" and \"MREL\" in the whole 98,380-character extraction, "
    "against 38 hits for \"Pillar 3\", 36 for \"liquidity\", 12 for \"capital requirement\" and 4 for \"capital "
    "resources\" in the same text - so those zeros are facts about the document rather than about the search. "
    "There is therefore no CET1/Tier 1/Tier 2 split and no leverage ratio for FY2016 either, and no capital "
    "RATIO is printed anywhere in the document: the ratio is NOT computed here from the capital and RWA figures, "
    "because this project does not derive a disclosure the bank did not make."
)

# Sheet order matches the project-wide standard (CET1 Capital/Ratio, Tier 1 Capital/Ratio,
# Total Capital/Ratio, Total RWAs, Leverage Ratio, LCR, NSFR, MREL Ratio) even though this
# entity only discloses the Total Capital/RWA/LCR/NSFR metrics.
# FOUND 2026-09-15: the FY2021 Annual Report (a filing never previously on file for
# this entity - see FY2021_AR_URL) carries, in Note 24(H) "Capital adequacy risk", a
# table the later reports dropped: "The following table summarises the regulatory
# Tier 1 resources of the Bank as at 31st December". Earlier audits searched the
# Strategic Report KPI table, which is a different part of the document, and so
# missed it.
# EXTENDED BY GA-005 (2026-09-18): the same table is also printed in the FY2020,
# FY2019 and FY2018 Annual Reports, which the 2026-09-15 pass did not check because
# it was looking for the reason the table STOPPED rather than for how far back it
# went. FY2020/FY2019/FY2018 now come from their own editions; FY2017 comes from the
# FY2018 edition's comparative column, because the FY2017 report prints no such table
# at all (see below). FY2016 and earlier: no table in any edition.
TIER1_CAPITAL_USD = {
    "FY2021": 52_489_000,
    "FY2020": 52_907_000,
    "FY2019": 51_836_000,
    "FY2018": 49_199_000,
    "FY2017": 50_407_000,
}

TIER1_SOURCES = (
    "Sources - Bank Mandiri (Europe) Limited's own \"Capital adequacy risk\" table inside the Risk management "
    "note, headed \"The following table summarises the regulatory Tier 1 resources of the Bank as at 31st "
    "December\". Each year is taken from ITS OWN edition except FY2017, which has none of its own (see below):\n"
    f"FY2021 (with FY2020 comparative): Annual Report FY2021, Note 24(H), p.48 - {FY2021_AR_URL}\n"
    f"FY2020 (with FY2019 comparative): Annual Report FY2020, Note 24(H), p.46 - {FY2020_AR_URL}\n"
    f"FY2019 (with FY2018 comparative): Annual Report FY2019, Note 24(H), p.48 - {FY2019_AR_URL}\n"
    f"FY2018 (with FY2017 comparative): Annual Report FY2018, Note 24, p.47 - {FY2018_AR_URL}\n\n"
    "AS PRINTED (US$'000), each column footing exactly to its stated total: FY2021 49,000 / 11,496 / 425 / "
    "(8,432) = 52,489. FY2020 49,000 / 11,496 / 1,219 / (8,808) = 52,907. FY2019 49,000 / 11,496 / 588 / "
    "(9,248) = 51,836. FY2018 49,000 / 11,496 / (1,386) / (9,911) = 49,199. FY2017 49,000 / 11,496 / 107 / "
    "(10,196) = 50,407. Converted to GBP at this workbook's existing period-end spot rates.\n\n"
    "SOURCE DEFECT, RECORDED NOT CORRECTED. The FY2018 Annual Report's own table prints its FY2018 revaluation "
    "reserve as \"(1,368)\", which does not foot to its own stated total of 49,199; the FY2019 edition's FY2018 "
    "comparative prints \"(1,386)\", which does foot, and (1,386) is also what the FY2018 Balance Sheet itself "
    "shows. Two independent renderings of the FY2018 page (300 dpi and 500 dpi) agree on \"(1,368)\", so the "
    "transposition is the document's, not an extraction artefact. Only the Total tier 1 capital line is carried "
    "onto this sheet and both editions print that identically as 49,199, so nothing on the sheet depends on the "
    "defective component.\n\n"
    "FY2017 IS FILLED FROM THE FY2018 EDITION'S COMPARATIVE, and the reason is a positive finding rather than a "
    "failed search: the FY2017 Annual Report's own \"(G) Capital adequacy risk\" note is four sentences of "
    "narrative with NO table - it says only that \"For regulatory purposes, the capital is made up of share "
    "capital, capital reserve and accumulated losses\". The FY2016, FY2015 and FY2014 reports carry the identical "
    "narrative-only note. The table is an addition made in the FY2018 report, so FY2016 and earlier have no "
    "Tier 1 figure of any kind in any edition and stay blank.\n\n"
    "WHY THIS TABLE STOPS AT THE OTHER END: it appears through the FY2021 report and not in FY2022 onward. "
    "Full-document searches of the FY2022 and FY2023 filings (OCR 2026-09-15, re-confirmed 2026-09-18 against "
    "the bank's own text-layer FY2022 copy, which returns ZERO hits on \"Tier 1\", \"own funds\", "
    "\"risk weighted\" and \"capital adequacy\" while returning 30 hits on \"capital\") find no Tier 1 table and "
    "no own-funds itemisation. FY2022 contains no capital figure at all; FY2023 onward give only the single "
    "combined narrative figure already carried on the Total Capital sheet. So FY2022-FY2025 genuinely have no "
    "CET1/Tier 1 split to transcribe.\n\n"
    "SOURCING METHOD: the FY2021 figures were read from the bank's own text-layer PDF of that report; the "
    "FY2020, FY2019 and FY2018 filings are image-only scans and were recovered by page-image OCR at 300 dpi and "
    "re-read at 500 dpi, with every total additionally cross-read from the adjacent edition's comparative "
    "column.\n\n" + ENTITY_NOTE
)

CET1_EQUIV_NOTE = (
    "BASIS: the table itemises the Bank's entire Tier 1 capital as share capital, capital reserve, revaluation "
    "reserve and retained earnings - every one a Common Equity Tier 1 item under CRR - and the four lines foot "
    "exactly to the stated Total tier 1 capital, with no Additional Tier 1 line of any kind. The Bank states "
    "alongside it that \"The Bank's capital resources consist of share capital, capital reserve and accumulated "
    "losses\" and that \"There are no terms and conditions attached to the Bank's Tier 1 capital resources\". "
    "CET1 = Tier 1 therefore follows from the composition the Bank itself prints, not from an assumption made "
    "here. NOTE this does NOT extend to Total Capital: the table covers Tier 1 only and discloses nothing about "
    "Tier 2, so Total Capital is left to the separate combined 'regulatory capital resources' figure the Bank "
    "publishes from FY2022 onward and to the 2016 Pillar 3's 'Total Eligible Capital', and stays blank for "
    "FY2017-FY2021."
)

# ---------------------------------------------------------------
# Sheet: KM1 Key Metrics (KM1-005) - documented NOT APPLICABLE
# ---------------------------------------------------------------
KM1_SOURCES = (
    "UK KM1 - KEY METRICS TEMPLATE: NOT PUBLISHED BY THIS ENTITY IN ANY YEAR.\n"
    "BMEL has published exactly one Pillar 3 disclosure in its history, for 31 December 2016, and that "
    "document pre-dates the template. Recorded on positive evidence, checked 2026-09-16, with the one part "
    "that could not be checked stated as such.\n"
    "\n"
    "THE ONLY PILLAR 3 THAT EXISTS. 'BMEL - Pillar 3 Disclosures 31st December 2016' (1,041,727 bytes, "
    "text-native, 33 pages) mentions 'Pillar 3' 38 times and contains ZERO occurrences of "
    "'KM1', 'key metric', 'CET1', 'Common Equity', 'own funds', 'leverage ratio' and 'liquidity coverage'. "
    "Those zeros are correct and stand. But a note here previously drew the wrong conclusion from them and "
    "called the document 'narrative'; it is not. It is a CRD IV Pillar 3 & Remuneration Code disclosure "
    "carrying real quantitative tables in the Bank's own house vocabulary - 'Total Risk Exposure' 64,242 and "
    "'Total Eligible Capital' 49,163 (U$'000, pp.11-12), a Pillar 1 and Pillar 2 capital build-up, a "
    "credit-risk RWA split by country, and a credit-quality-per-class table for 2016 and 2015. Those figures "
    "are now carried on the Total RWAs, Total Capital, RWA Breakdown and Asset Quality sheets. What the "
    "document genuinely lacks is the TEMPLATE: the UK KM1 template arrived with the Disclosure (CRR) Part "
    "of the PRA Rulebook, six years after it, so its absence there is expected rather than a gap (map rule "
    "25). The lesson worth keeping is that a zero on template vocabulary is evidence about the template and "
    "not about the document's contents.\n"
    "\n"
    "THE LIVE SITE WAS ENUMERATED IN FULL, NOT SAMPLED. bkmandiri.co.uk is a five-page site: the home page, "
    "/about-us/, /products-services/, /contact-us/ and /legal-important-information/, plus /sitemap/ which "
    "lists exactly those five. Every page returned HTTP 200 and was read. The home and about pages carry no "
    "PDF links whatsoever. Every PDF the site publishes is linked from the legal page, and there are fourteen "
    "of them: the US Patriot Act certificate, website terms, privacy policy, complaints policy, W-8BEN-E, "
    "FSCS declaration, anti-money-laundering declaration, statement of ethics, UK tax strategy, anti-slavery "
    "statement, a Wolfsberg questionnaire, and the BMEL Annual Reports for 2023, 2024 and 2025. No Pillar 3 "
    "document of any year is among them.\n"
    "\n"
    "THE ARCHIVE AGREES. A Wayback CDX sweep of the whole bkmandiri.co.uk domain returned 276 captures "
    "covering 27 distinct PDFs across the site's history, going back to a 2012 capture. Exactly one is a "
    "Pillar 3 disclosure: the 2016 document above. The Annual Reports for 2021 and 2022 appear there too and "
    "are no longer linked live, so the sweep was demonstrably capable of surfacing withdrawn documents - it "
    "found withdrawn annual reports and still found no second Pillar 3.\n"
    "\n"
    "AND THE ANNUAL REPORTS CARRY NO KM1 EITHER, which is worth stating because some small banks put their "
    "Pillar 3 inside the annual report. The FY2025 and FY2024 Annual Reports were fetched live and extract to "
    "162,945 and 161,914 characters. Both contain ZERO occurrences of 'KM1', 'key metric', 'Pillar 3', "
    "'CET1', 'Common Equity' and 'leverage ratio'. Those zeros are trustworthy rather than an extractor "
    "failure because the same documents return real hits on neighbouring terms - 'liquidity coverage' four "
    "times in FY2025 and three in FY2024, 'own funds' once in each (map rule 15).\n"
    "\n"
    "WHAT WAS NOT CHECKED, STATED PLAINLY (map rule 9). The site's REST API is blocked: "
    "https://www.bkmandiri.co.uk/bkm-api/wp/v2/media returns "
    "'itsec_rest_api_access_restricted - Access to REST API requests is restricted by Kadence Security "
    "settings' for every query. So the WordPress media library could not be enumerated directly, and an "
    "unlinked file sitting in it would not appear in the page-link enumeration above. Wayback partly covers "
    "that gap and found nothing, but the two routes are not equivalent. If a Pillar 3 document for this "
    "entity is ever found, that blocked media library is where it will be.\n"
    "\n"
    "The entity's capital and liquidity disclosures, such as they are, are the narrative paragraph and KPI "
    "table in each Annual Report's Strategic Report - a single combined Total Capital Ratio, LCR and NSFR "
    "with no CET1/Tier 1 breakdown. Those are carried on the single-metric sheets under their own citations "
    "and are unaffected by this sheet being blank.\n"
    "\n" + ENTITY_NOTE
)

# GA-020 (2026-09-19): outcome wording for the cells below, on the evidence in
# KM1_SOURCES / NOT_DISCLOSED_NOTE (both name the documents checked).
KM1_CELL = ("Not published – only Pillar 3 ever is the 31 Dec 2016 edition (pre-dates KM1); live site + Wayback CDX "
            "enumerated 2026-09-16, no later one; ARs FY2024/FY2025 contain no KM1")
GA020_EV = "only Pillar 3 ever (31 Dec 2016) has zero hits; ARs FY2014-FY2025 give capital only as Tier 1 (FY2017-21) or a combined total capital ratio (KPI table p.6, FY2022+). See note."
GA020_STATEMENTS = {
    "CET1 Ratio": "Not published – no CET1 ratio in any edition: " + GA020_EV,
    "Tier 1 Ratio": "Not published – no Tier 1 ratio in any edition: " + GA020_EV,
    "Leverage Ratio": "Not published – no leverage ratio in any edition: " + GA020_EV,
    "MREL Ratio": "Not published – no MREL figure in any edition: " + GA020_EV,
}

bw.add_km1_sheet(
    title="Bank Mandiri (Europe) Limited - KM1 Key Metrics",
    subtitle="Not applicable: this entity has published exactly one Pillar 3 disclosure in its history, for "
             "31 December 2016, which pre-dates the template. No later Pillar 3 exists on the live site or in "
             "the Wayback archive, and the annual reports contain no KM1. See the sources note, which also "
             "records the one route that is blocked rather than empty.",
    rows=[("DATA", "UK KM1 - Key metrics template: not published by this entity in any year",
           {y: KM1_CELL for y in YEARS})],
    sources_text=KM1_SOURCES,
    first_col_width=64,
    source_height=300,
    years=YEARS,
)

metric(
    "CET1 Capital", "£'000 (conv. from USD)",
    [("Common Equity Tier 1 capital (= Tier 1; no AT1 component disclosed)",
      {**stock(TIER1_CAPITAL_USD), **NO_TIER1_SPLIT})],
    TIER1_SOURCES,
    note=CET1_EQUIV_NOTE + " FY2022-FY2025 are blank because the Bank stopped publishing this table - see the "
         "source note. No CET1 RATIO is derivable: no directly disclosed RWA exists in any year (see Total RWAs).",
)

bw.add_not_disclosed_metric_sheets(
    ["CET1 Ratio"], p3_sources(), per_note={"CET1 Ratio": NOT_DISCLOSED_NOTE},
    statements={"CET1 Ratio": GA020_STATEMENTS["CET1 Ratio"]},
)

metric(
    "Tier 1 Capital", "£'000 (conv. from USD)",
    [("Total tier 1 capital", {**stock(TIER1_CAPITAL_USD), **NO_TIER1_SPLIT})],
    TIER1_SOURCES,
    note="Directly disclosed as \"Total tier 1 capital\" in the Bank's own Note 24(H) table. " + CET1_EQUIV_NOTE,
)

bw.add_not_disclosed_metric_sheets(
    ["Tier 1 Ratio"], p3_sources(), per_note={"Tier 1 Ratio": NOT_DISCLOSED_NOTE},
    statements={"Tier 1 Ratio": GA020_STATEMENTS["Tier 1 Ratio"]},
)

metric(
    "Total Capital", "£'000 (conv. from USD)",
    [
        ("Regulatory capital resources (\"Own Funds\")", {**stock(TOTAL_CAPITAL_USD), **NO_TOTAL_CAPITAL}),
        ("Total Eligible Capital (2016 Pillar 3 disclosure)", stock(P3_2016_ELIGIBLE_CAPITAL_USD)),
    ],
    p3_sources(),
    note="Two rows, because the two figures come from different documents under different captions and are not "
         "the same series. FY2022-FY2025 is the single combined \"regulatory capital resources\" amount the "
         "Strategic Report narrates; FY2016 is the \"Total Eligible Capital\" line of the bank's 2016 Pillar 3. "
         "No CET1/Tier 1/Tier 2 breakdown accompanies either. FY2017-FY2021 stay blank: the Tier 1 table those "
         "reports carry covers Tier 1 only and says nothing about Tier 2, so no total capital figure exists for "
         "them. See the CET1 Capital / Tier 1 Capital sheets.\n\n" + P3_2016_NOTE,
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Capital Adequacy Ratio / Total Capital Ratio (Own Funds / Total Risk Weighted Asset)", CAR)],
    p3_sources(),
)

metric(
    "Total RWAs", "£'000 (conv. from USD)",
    [("Total Risk Exposure (2016 Pillar 3 disclosure)", {**stock(P3_2016_TOTAL_RWA_USD), **NO_RWA})],
    p3_sources(),
    note="ONE YEAR ONLY, AND IT IS DISCLOSED RATHER THAN DERIVED. FY2016 carries the \"Total Risk Exposure\" "
         "line the bank printed in its 2016 Pillar 3; see the block below. Every other year is blank because "
         "the bank has never printed an RWA figure for it - not because a figure was removed.\n\n"
         + P3_2016_NOTE + "\n\n"
         "EVERY OTHER YEAR: NOT DISCLOSED. No RWA figure, aggregate or by category, appears in any Annual "
         "Report or other source found for any year but FY2016.\n\n"
         "EVIDENCE UPGRADED 2026-09-15 - this is now a machine-verified negative, not a visual one. An earlier "
         "version of this note said all four FY2022-FY2025 Annual Reports were scanned/image-only and had been "
         "reviewed page-by-page; that was true of the Companies House filings but WRONG about the documents "
         "themselves. The bank publishes its own copies at bkmandiri.co.uk and the FY2021, FY2022, FY2024 and "
         "FY2025 reports are full text-layer PDFs (only FY2023 is a real scan). Searching the complete extracted "
         "text of all four for 'risk-weighted', 'RWA', 'exposure class', 'Pillar 1' and '12.5' returns exactly two "
         "kinds of hit in every year: the narrative sentence explaining that the change in CAR 'reflects an "
         "increase in risk-weighted assets', and the parenthetical defining the ratio as '(Own Funds / Total Risk "
         "Weighted Asset)'. Neither carries a number. The FY2023 scan was separately re-OCR'd at 500 dpi and its "
         "KPI table likewise shows a ratio with no denominator. The absence is therefore established by exhaustive "
         "full-text search rather than by eye, which is a materially stronger basis than the claim it replaces. "
         "WITHDRAWN 2026-09-15: this sheet previously carried four back-solved values (FY2025 167,907,000; "
         "FY2024 126,573,000; FY2023 152,478,000; FY2022 145,820,000), computed as regulatory capital resources "
         "DIVIDED BY the Total Capital Ratio, and openly labelled as derived. They were removed for consistency "
         "with the project-wide rule against deriving RWA from capital / ratio, which is already applied to Alpha "
         "Bank London, Nomura Bank International, State Bank of India (UK), Ghana International, Weatherbys and "
         "Havin. The derivation was in any case limited by the 2-decimal-place ratio it inverted, and using the "
         "result to compute any further ratio would simply return its own inputs. The Total Capital and Total "
         "Capital Ratio sheets carry the Bank's own printed figures and are unaffected. THE FY2016 FIGURE ABOVE "
         "IS NOT A REINSTATEMENT OF ANY OF THOSE: it is a number the bank printed, in a document, under its own "
         "caption, for a year none of the withdrawn values covered.\n\n"
         "FY2017-FY2019 UPGRADED THE SAME WAY, 2026-09-18 (leading-gap sweep). The paragraph above made "
         "FY2022-FY2025 a machine-verified negative but left the middle years resting on a 'checked page by "
         "page' claim, which is exactly the kind of assertion this project has repeatedly found to be wrong. "
         "Those filings are genuine image-only scans - a text extraction of the FY2019, FY2018 and FY2017 "
         "Companies House filings yields 57, 56 and 47 characters respectively for 57, 56 and 51 pages - so "
         "they were re-rendered and OCR'd page-by-page at 250 dpi and searched the same way the later years "
         "were. RESULT: across the full OCR of both the FY2019 and the FY2018 filing, the strings "
         "'risk-weighted' / 'risk weight' / 'RWA' / 'own funds' / 'eligible capital' / 'Pillar' return ZERO "
         "hits of any kind. The only capital disclosure in either document is the note headed 'Capital "
         "adequacy risk' (note 24(H) in FY2019, 24(G) in FY2018), which says the Bank manages capital against "
         "its PRA Individual Capital Guidance, describes ICAAP/SREP in words, and then prints ONE table - "
         "'The following table summarises the regulatory Tier 1 resources of the Bank as at 31 December' - "
         "with no RWA line, no capital requirement, no ratio and no total-own-funds line. Both tables "
         "reproduce exactly what this workbook already carries: FY2019 49,000 / 11,496 / 588 / (9,248) = "
         "51,836 with FY2018 comparative 49,199, and FY2018 49,000 / 11,496 / (1,368) / (9,911) = 49,199 "
         "with FY2017 comparative 50,407. (That (1,368) is the FY2018 edition's own printing of its "
         "revaluation reserve against the (1,386) the FY2019 edition prints as its comparative - the source "
         "defect already recorded on the Tier 1 Capital sheet, re-observed here independently and again NOT "
         "corrected.) FY2020 and FY2021 are covered from the other direction by the FY2021 Annual Report, a "
         "text-layer PDF whose full text contains no risk-weighted-asset amount for either year while "
         "carrying the same Tier 1 table (52,489 / 52,907). So the RWA blank now rests on a full-document "
         "search for every year from FY2017 to FY2025, not on a visual pass for any of them.",
)

# GA-005 (2026-09-18): this sheet was a documented "not disclosed" stub. It is now a
# real sheet for ONE year. The 2016 Pillar 3 splits the Bank's risk exposure two
# different ways - by risk type and by country of exposure - and those are two
# different templates from the same document, so they are shown as separate sections
# rather than merged (gaps map general point 3). The £ figures are converted at the
# 31 Dec 2016 spot rate, £1 = $1.2303, the same rate the Balance Sheet uses.
P3_2016_RWA_BY_RISK_USD = {
    "Risk weighted assets for credit risk": {"FY2016": 57_663_000},
    "Risk exposure for operational risk": {"FY2016": 6_579_000},
    "Total Risk Exposure": {"FY2016": 64_242_000},
}
P3_2016_PILLAR1_USD = {
    "4.2.1 Credit risk (including supporting factor)": {"FY2016": 4_613_000},
    "4.2.2 Operational risk": {"FY2016": 526_000},
    "Total Pillar 1": {"FY2016": 5_139_000},
}
P3_2016_RWA_BY_COUNTRY_USD = {
    "Belgium": {"FY2016": 160_000},
    "Germany": {"FY2016": 201_000},
    "Hong Kong": {"FY2016": 9_417_000},
    "Indonesia": {"FY2016": 41_507_000},
    "United Kingdom": {"FY2016": 2_695_000},
    "United States": {"FY2016": 3_682_000},
    "Total Exposure": {"FY2016": 57_663_000},
}
DASH16 = {"FY2016": "-"}

rwa_breakdown_rows = (
    [("SECTION", "FY2016 — risk exposure by risk type (2016 Pillar 3, printed p.11)", {})]
    + [("DATA", "Risk weighted assets for credit risk", stock(P3_2016_RWA_BY_RISK_USD["Risk weighted assets for credit risk"])),
       ("DATA", "Risk exposure for operational risk", stock(P3_2016_RWA_BY_RISK_USD["Risk exposure for operational risk"])),
       ("DATA", "Risk exposure for market risk", DASH16),
       ("TOTAL", "Total Risk Exposure", stock(P3_2016_RWA_BY_RISK_USD["Total Risk Exposure"]))]
    + [("SECTION", "FY2016 — Pillar 1 capital requirement, same table (2016 Pillar 3, printed p.11)", {})]
    + [("DATA", "4.2.1 Credit risk (including supporting factor)", stock(P3_2016_PILLAR1_USD["4.2.1 Credit risk (including supporting factor)"])),
       ("DATA", "4.2.2 Operational risk", stock(P3_2016_PILLAR1_USD["4.2.2 Operational risk"])),
       ("DATA", "4.2.3 Market risk", DASH16),
       ("TOTAL", "Total Pillar 1", stock(P3_2016_PILLAR1_USD["Total Pillar 1"]))]
    + [("SECTION", "FY2016 — credit-risk RWA by country of exposure (2016 Pillar 3, printed p.19)", {})]
    + [("DATA", c, stock(P3_2016_RWA_BY_COUNTRY_USD[c])) for c in
       ("Belgium", "Germany", "Hong Kong", "Indonesia", "United Kingdom", "United States")]
    + [("TOTAL", "Total Exposure (credit-risk RWA)", stock(P3_2016_RWA_BY_COUNTRY_USD["Total Exposure"]))]
    # Disclosure-status row for the eleven years that are not FY2016, so the grid
    # itself says why those columns are empty instead of leaving the reader - and
    # audit_gaps.py - to infer it from the subtitle. Deliberately placed LAST,
    # after every TOTAL: put above one, verify_workbook.py folds it into the
    # summation block it checks against that total.
    + [("DATA", "Disclosure status where no figures are shown", dict(NO_RWA))]
)

RWA_BREAKDOWN_SOURCES = (
    "ONE YEAR IS DISCLOSED; ELEVEN ARE NOT. FY2016 is sourced from this entity's only Pillar 3 disclosure, "
    f"\"Bank Mandiri (Europe) Limited - Pillar 3 Disclosures as at 31st December 2016\" - "
    f"{PILLAR3_2016_ARCHIVE_URL} - which prints the Bank's risk exposure two different ways, shown above as two "
    "separate sections because they are two different templates rather than one split:\n"
    "(a) BY RISK TYPE, printed p.11, single column headed \"Dec-16\", U$'000: Risk weighted assets for credit "
    "risk 57,663; Risk exposure for operational risk 6,579; Risk exposure for market risk \"-\"; Total Risk "
    "Exposure 64,242. The same table continues into the Pillar 1 capital requirement shown in the second "
    "section (4,613 / 526 / \"-\" / 5,139), which foots exactly. The two market-risk dashes are reproduced as "
    "dashes: the document does print a market-risk figure elsewhere, as a US$10k capital requirement on a "
    "US$131k FX open position at p.17, but in THIS table it prints a dash, and a dash is not a zero.\n"
    "ROUNDING NOTE on section (a): in US$ the table foots exactly (57,663 + 6,579 + nil = 64,242). In the "
    "£'000 shown above it is one short - 46,869 + 5,347 = 52,216 against a total of 52,217 - because every "
    "line is converted from its own US$ figure at the 31 Dec 2016 spot rate (£1 = $1.2303) and rounded to the "
    "nearest £'000 independently, and the total's own unrounded value is 52,216.53. The £1k gap is created by "
    "that rounding; it is not a discrepancy in the Bank's disclosure. Section (b)'s Pillar 1 block happens to "
    "foot in both currencies.\n"
    "(b) BY COUNTRY OF EXPOSURE, printed p.19, a concentration-risk table giving gross exposure, RWA exposure "
    "and capital requirement per country. Only the RWA EXPOSURE column is reproduced above. In U$'000 as "
    "printed: Belgium 160; Germany 201; Hong Kong 9,417; Indonesia 41,507; United Kingdom 2,695; United States "
    "3,682; Total Exposure 57,663 — which reconciles to the credit-risk RWA line in section (a).\n"
    "SOURCE ROUNDING, RECORDED NOT CORRECTED: the six country lines sum to 57,662, one thousand dollars below "
    "the 57,663 the same table prints as its own total. Each line is reproduced exactly as printed; the total "
    "row is the bank's own printed total, not a re-sum. The £ figures shown here also carry ordinary conversion "
    "rounding, since each line is converted individually at £1 = $1.2303 and then rounded to the nearest "
    "£'000.\n"
    "THE 2016 DISCLOSURE IS A CRD IV DOCUMENT AND HAS NO UK OV1 TEMPLATE, which is not a defect: the UK OV1 "
    "template post-dates it. There is no exposure-class split (central governments / institutions / corporates "
    "/ retail) in it, only the risk-type and country splits above.\n\n"
    "EVERY OTHER YEAR: NOT DISCLOSED, and established as such rather than merely not found. No dedicated Pillar "
    "3 document exists for any year but 2016 (the live site was enumerated in full and a Wayback CDX sweep of "
    "the whole bkmandiri.co.uk domain returned 27 distinct PDFs across its history, of which exactly one is a "
    "Pillar 3 - see the KM1 Key Metrics sheet for that enumeration, re-run and re-confirmed 2026-09-18). The "
    "Annual Reports carry no RWA figure at all: the FY2021, FY2022, FY2024 and FY2025 reports are text-layer "
    "PDFs and full-text searches of them return no risk-weighted-asset amount anywhere, only the narrative "
    "sentence that the change in capital ratio \"reflects an increase in risk-weighted assets\" and the "
    "parenthetical defining the KPI as \"(Own Funds / Total Risk Weighted Asset)\", neither carrying a number; "
    "the FY2023 scan was re-OCR'd at 500 dpi with the same result; and the FY2014-FY2020 filings were checked "
    "page by page. Each year's Risk Management note covers market, interest rate, currency, liquidity and "
    "credit risk and no capital-requirement table that could be grossed up by x12.5.\n"
    "NOTE ON AN EARLIER CORRECTION: the FY2022_AR_URL constant once pointed to the wrong Companies House filing "
    f"(a Deloitte auditor-resignation letter, not the accounts); it has since pointed to the real FY2022 \"Full "
    f"accounts\" filing ({FY2022_AR_URL}), which is the document the checks above were run against.\n\n"
    + ENTITY_NOTE
)

bw.add_rwa_breakdown_sheet(
    title="Bank Mandiri (Europe) Limited — RWA Breakdown",
    subtitle="£'000, converted from USD at £1 = $1.2303 (31 Dec 2016 spot). FY2016 only — the one year this "
             "entity published a Pillar 3 disclosure. See the source note for how the other eleven years were "
             "established as non-disclosures.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=54,
    source_height=320,
)

bw.add_not_disclosed_metric_sheets(
    ["Leverage Ratio"], p3_sources(), per_note={"Leverage Ratio": NOT_DISCLOSED_NOTE},
    statements={"Leverage Ratio": GA020_STATEMENTS["Leverage Ratio"]},
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio (%)", {"FY2025": "446.89%", "FY2024": "382%", "FY2023": "264.29%", "FY2022": "147.59%"})],
    p3_sources(),
    note="No £/$ breakdown (HQLA, net cash outflows) is disclosed anywhere - only the ratio itself. FY2025 shown to "
         "2 d.p. as stated in the Strategic Report narrative (446.89%); the report's own KPI table rounds this to 447%.",
)

metric(
    "NSFR", "%",
    [("Net Stable Fund Ratio (%)", {"FY2025": "121.85%", "FY2024": "142%", "FY2023": "131.85%", "FY2022": "143.26%"})],
    p3_sources(),
    note="No £/$ breakdown (available/required stable funding) is disclosed anywhere - only the ratio itself. "
         "FY2025 shown to 2 d.p. as stated in the Strategic Report narrative (121.85%); the report's own KPI table "
         "rounds this to 122%.",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources(), per_note={"MREL Ratio": NOT_DISCLOSED_NOTE},
    statements={"MREL Ratio": GA020_STATEMENTS["MREL Ratio"]},
)

# ---------------------------------------------------------------
# Overview sheet (Pillar-3-only: no cash-flow chart)
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit=None,
    balance_sheet_totals=[
        ("Total assets", BS["Total assets"]),
        ("Loan and advances to customers", BS["Loan and advances to customers"]),
        ("Customer accounts", BS["Customer accounts"]),
        ("Total shareholders' funds", BS["Total shareholders' funds"]),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total operating income", IS["Total operating income"]),
        ("Administrative expenses", IS["Administrative expenses"]),
        ("Profit on ordinary activities after tax", IS["Profit on ordinary activities after tax"]),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        # Each opening balance is 31-Dec-(Y-1)'s figure, converted at THAT
        # date's spot rate (FX_SPOT["FY"+str(Y-1)]) - same fix as the
        # Statement of Change in Equity sheet's "At 1 January" rows above.
        ("Opening shareholders' funds", {"FY2025": bal((54254,), "FY2024")[0], "FY2024": bal((52323,), "FY2023")[0], "FY2023": bal((49714,), "FY2022")[0], "FY2022": bal((52489,), "FY2021")[0], "FY2021": bal((52907,), "FY2020")[0]}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": flow({"FY2025": 2_230_000})["FY2025"], "FY2024": flow({"FY2024": 1_931_000})["FY2024"], "FY2023": flow({"FY2023": 2_609_000})["FY2023"], "FY2022": flow({"FY2022": -2_775_000})["FY2022"], "FY2021": flow({"FY2021": -418_000})["FY2021"]}),
        # Pure FX-translation artefact of converting opening/movements/closing at 3 different
        # GBP/USD rates within one year - see the Statement of Change in Equity sheet's source
        # note. Not a real equity movement; absorbs the gap so this bridge ties exactly.
        ("Other equity movements, net (FX translation effect — see Statement of Change in Equity)", {y: v for y, v in FX_TRANSLATION_EFFECT.items()}),
        ("Closing shareholders' funds", BS["Total shareholders' funds"]),
    ],
    equity_changes_unit="£'000",
    ratios=[
        ("Total Capital Ratio", CAR),
        ("LCR", {"FY2025": "446.89%", "FY2024": "382%", "FY2023": "264.29%", "FY2022": "147.59%"}),
        ("NSFR", {"FY2025": "121.85%", "FY2024": "142%", "FY2023": "131.85%", "FY2022": "143.26%"}),
    ],
    note="This entity takes the FRS 101 cash-flow-statement exemption every year (see the Cash Flow Statement "
         "sheet), so no cash flow summary or chart is shown here. It has published exactly one Pillar 3 "
         "disclosure in its history, covering 31 December 2016; for every other year the only regulatory "
         "disclosures are a combined Total Capital Ratio (no CET1/Tier 1 breakdown), LCR and NSFR in each Annual "
         "Report's Strategic Report, plus a Tier 1 resources table in the FY2018-FY2021 reports. Total RWAs and "
         "RWA Breakdown therefore carry FY2016 only, from that 2016 Pillar 3, and are blank elsewhere; the four "
         "Total RWAs values shown before 2026-09-15 were back-solved from capital and ratio and stay withdrawn "
         "— the FY2016 figure is not one of them, it is a figure the bank printed. No capital ratio, LCR or NSFR "
         "exists for FY2021 or for any year before FY2022, so the ratio trend chart starts at FY2022 — see each "
         "Pillar 3 sheet's own source citation.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BANK MANDIRI EUROPE FINANCIALS.xlsx")
