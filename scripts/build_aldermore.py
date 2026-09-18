import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Aldermore Bank PLC (Companies House 00947662, FRN 204503) reports to a
# 30 June fiscal year end - "FY2025" below means the year ended 30 June 2025.
# Historical-depth extension (HD-047, 2026-09-05): extended back to FY2014
# (capped there by explicit user decision - see wayfinder/historical-depth
# ticket HD-047 - even though the Bank's real archive goes back to FY2009).
#
# Two structural quirks in the pre-2021 history, both explained in the
# per-sheet source notes below rather than papered over:
#   - Following the FirstRand acquisition (completed 14 Mar 2018), the Bank
#     changed its accounting reference date from 31 December to 30 June to
#     align with FirstRand Group. This produced one 18-MONTH set of
#     statutory accounts covering 1 Jan 2017 - 30 Jun 2018 ("FY2018" below)
#     instead of a normal 12-month FY2017 + FY2018. There is no standalone
#     12-month FY2017 period in the Bank's own disclosures at all, so
#     FY2017 is left blank throughout (a genuine self-skip, not an
#     oversight) and FY2018's column is an 18-month, not 12-month, period.
#   - No standalone Pillar 3 disclosure document could be located (via the
#     Bank's own site, Wayback Machine CDX search, or web search) for
#     FY2016 or FY2020 specifically, despite real effort - only a single
#     "CET1 ratio" headline figure survives for each in that year's own
#     Annual Report "Financial highlights" page. Balance Sheet/P&L/Cash
#     Flow/Equity/Asset Quality are unaffected (sourced from Companies
#     House statutory accounts, which exist for every year except FY2017)
#     but the other Pillar 3 metric sheets and RWA Breakdown are left
#     blank for FY2016 and FY2020.
YEARS = [
    "FY2025", "FY2024", "FY2023", "FY2022", "FY2021",
    "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014",
    "FY2013", "FY2012", "FY2011", "FY2010", "FY2009",
]

# HD-073 (2026-09-06): the statutory-statement sheets (Balance Sheet, P&L,
# Statement of Changes in Equity, Cash Flow Statement) use the full YEARS
# above, but Pillar 3 (all 11 metric sheets), Asset Quality, and RWA
# Breakdown are explicitly out of scope for that extension - they must keep
# FY2014 as their earliest column, same as before this ticket. Every call
# building one of those sheets passes years=PILLAR3_YEARS explicitly.
PILLAR3_YEARS = [y for y in YEARS if y not in (
    "FY2013", "FY2012", "FY2011", "FY2010", "FY2009",
)]

# FY2026 extension (2026-09-15): the Group's FY2026 Pillar 3 report (y/e 30 Jun
# 2026) is published and carries a full Bank-solo column, so the 11 metric
# sheets and RWA Breakdown gain an FY2026 column. The statutory sheets do NOT:
# Aldermore Bank PLC's own FY2026 accounts have not been filed at Companies
# House yet (latest filing is the year ended 30 June 2025, filed 03 Nov 2025),
# and the Group Annual Report's "Company" statements are Aldermore Group PLC
# the holding company (total assets £1,102.2m), not the Bank's ~£20bn balance
# sheet - so they cannot substitute under the entity-basis rule. Asset Quality
# is likewise statutory-sourced and stays on PILLAR3_YEARS. Hence a separate
# list rather than mutating YEARS or PILLAR3_YEARS, which would leak a blank
# FY2026 column into every statutory sheet.
# HISTORICAL PILLAR 3 EXTENSION (2026-09-15). Two pre-FY2014 Pillar 3 editions
# were recovered from the Internet Archive - 31 December 2011 and 31 December
# 2013 - so the 11 metric sheets and RWA Breakdown extend three columns further
# back than the FY2014 floor HD-073 set. FY2012 sits between them with no
# document located, and is carried as an explicit blank column rather than
# silently skipped, so the gap is visible instead of looking like a boundary.
#
# ENTITY CHECK - both recovered editions are ALDERMORE BANK PLC, the same legal
# entity this whole workbook is built on (Companies House 00947662, FRN 204503,
# named and registered on every page footer of both documents). They are not the
# Aldermore Group PLC holding company, which did not exist as a Pillar 3 reporting
# entity then. So there is NO entity-basis break at this end of the series: these
# are Bank-solo disclosures in their own right, whereas FY2014 onward are Bank
# columns lifted out of Group-level Pillar 3 reports. That direction of travel is
# recorded on the sheets, but it is a change in the reporting VEHICLE, not in the
# reporting entity, and the figures are Bank-solo throughout.
#
# FY2010 and FY2009 stay out: no Pillar 3 edition was located for either, and
# adding them would put two wholly blank columns on every metric sheet.
P3_DISCLOSURE_YEARS = ["FY2026"] + PILLAR3_YEARS + ["FY2013", "FY2012", "FY2011"]

YEAR_LABEL = {
    "FY2026": "FY2026 (y/e 30 Jun 26)",
    "FY2025": "FY2025 (y/e 30 Jun 25)",
    "FY2024": "FY2024 (y/e 30 Jun 24)",
    "FY2023": "FY2023 (y/e 30 Jun 23)",
    "FY2022": "FY2022 (y/e 30 Jun 22)",
    "FY2021": "FY2021 (y/e 30 Jun 21)",
    "FY2020": "FY2020 (y/e 30 Jun 20)",
    "FY2019": "FY2019 (y/e 30 Jun 19)",
    "FY2018": "FY2018 (18-month transition period, 1 Jan 17 - 30 Jun 18)",
    "FY2017": "FY2017 (no standalone 12-month period - see note)",
    "FY2016": "FY2016 (y/e 31 Dec 16)",
    "FY2015": "FY2015 (y/e 31 Dec 15)",
    "FY2014": "FY2014 (y/e 31 Dec 14)",
    "FY2013": "FY2013 (y/e 31 Dec 13)",
    "FY2012": "FY2012 (y/e 31 Dec 12)",
    "FY2011": "FY2011 (y/e 31 Dec 11)",
    "FY2010": "FY2010 (y/e 31 Dec 10)",
    "FY2009": "FY2009 (9-month stub, 1 Apr 09 - 31 Dec 09)",
}

CH_2013_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzA5ODk0MTEwOGFkaXF6a2N4/document?format=pdf&download=0"
CH_2011_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzA1NTc4MjIyNmFkaXF6a2N4/document?format=pdf&download=0"
CH_2010_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzAzNjIxMDA5N2FkaXF6a2N4/document?format=pdf&download=0"

CH_2025_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzQ4NzM5MDg2MWFkaXF6a2N4/document?format=pdf&download=0"
CH_2024_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzQ0MDgwMDc3OWFkaXF6a2N4/document?format=pdf&download=0"
CH_2023_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzM5ODA0OTgzOWFkaXF6a2N4/document?format=pdf&download=0"
CH_2022_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzM1NTc2ODMxMmFkaXF6a2N4/document?format=pdf&download=0"
CH_2021_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzMxODkyMzc2MWFkaXF6a2N4/document?format=pdf&download=0"
CH_2020_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzI4MzMzMzM4OGFkaXF6a2N4/document?format=pdf&download=0"
CH_2019_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzI0OTY0MTQwMWFkaXF6a2N4/document?format=pdf&download=0"
CH_2018_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzIxNzQ4NDUzNmFkaXF6a2N4/document?format=pdf&download=0"
CH_2016_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzE3NTQ0MTgwOGFkaXF6a2N4/document?format=pdf&download=0"
CH_2015_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzE0OTEzMjU1M2FkaXF6a2N4/document?format=pdf&download=0"

P3_2026_URL = "https://www.aldermore.co.uk/media/0wylhhas/pillar-3-fy-2026-aldermore-group.pdf"
ARA_2026_URL = "https://www.aldermore.co.uk/media/tsybnoau/ara-fy-2026-aldermore-group.pdf"
P3_2025_URL = "https://www.aldermore.co.uk/media/sgufisw5/aldermore-group-plc-2025-pillar-3-disclosures.pdf"
P3_2024_URL = "https://www.aldermore.co.uk/media/jkkdbgnu/aldermore-group-plc-2024-pillar-3-disclosures.pdf"
# FY2023's OWN edition, added 2026-09-16 (KM1-003). It was never cited by this project: found by
# diffing the Bank's own investor index against our citation list, which also turned up uncited
# FY2020 and FY2021 editions (neither prints a key-metrics table of any kind, so neither is wired).
# It matters because the Pillar 3 metric sheets above source FY2023 from the FY2024 edition's
# COMPARATIVE column, and the KM1 map's rule 1 is to use each year's own edition. The two agree
# here (Bank CET1 1,203.8 both ways), so this changes provenance, not figures.
P3_2023_URL = "https://www.aldermore.co.uk/media/ynohqczi/pillar-3-2023.pdf"
P3_2022_URL = "https://www.aldermore.co.uk/media/hnhpw03l/pillar-3-2022_0.pdf"
P3_2019_URL = "https://www.aldermore.co.uk/media/2prbumkj/aldermore-group-plc-pillar-3-disclosure-document-at-30-june-2019.pdf"
P3_2015_URL = "https://www.aldermore.co.uk/media/ot5axgnp/pillar-3-disclosure-dec-2015.pdf"
# ---------------------------------------------------------------
# 2026-09-18 INTERIOR-GAP PASS - THREE "MISSING" PILLAR 3 EDITIONS THAT WERE NEVER MISSING.
# Every version of this script before today asserted that no Pillar 3 document exists for
# FY2016, FY2020 or FY2012. All three exist and all three are below. See P3_RECOVERY_NOTE
# for how each was found and what it changed; the short version is that a gap in our
# citation list was being reported as a gap in the public record.
# ---------------------------------------------------------------
# FY2020 (y/e 30 June 2020): live on Aldermore's own investor index the whole time. A note
# added to this script on 2026-09-16 even recorded having FOUND it, and dismissed it as
# printing "no key-metrics table of any kind" - true of UK KM1, and irrelevant to the
# 10-page Bank-only Appendix 1 it does carry.
P3_2020_URL = "https://www.aldermore.co.uk/media/axcpvnoo/aldermore-group-plc-pillar-3-disclosures-year-ended-30-june-2020_1.pdf"
# FY2016 (31 December 2016): Aldermore Group PLC's own edition, whose filename carries NO
# year at all ("pillar_3_disclosures.pdf") - which is why every year-pattern search missed
# it. Recovered by enumerating the whole archived host with the Wayback CDX API rather than
# guessing filenames.
P3_2016_URL = "https://web.archive.org/web/2023id_/https://www.investors.aldermore.co.uk/system/files/uploads/financialdocs/pillar_3_disclosures.pdf"
# FY2012 (31 December 2012): sits under the identical /financialdocs/ path as the 2011 and
# 2013 editions this script has cited since 2026-09-15.
P3_2012_URL = "https://web.archive.org/web/2023id_/https://www.investors.aldermore.co.uk/system/files/uploads/financialdocs/pillar_3_disclosure_2012_0.pdf"
# Recovered from the Internet Archive 2026-09-15; both are Aldermore Bank PLC's own
# standalone Basel II-era Pillar 3 disclosures, no longer linked from any live page.
P3_2013_URL = "https://web.archive.org/web/20230811224731id_/https://www.investors.aldermore.co.uk/system/files/uploads/financialdocs/pillar_3_disclosure_2013_0.pdf"
P3_2011_URL = "https://web.archive.org/web/20230810043035id_/https://www.investors.aldermore.co.uk/system/files/uploads/financialdocs/pillar_3_disclosure_2011_0.pdf"
INTERIM_P3_2025_URL = "https://www.aldermore.co.uk/media/xx1fg0me/half-year-pillar-3-disclosures-31-dec-2025.pdf"

CASH_FLOW_SOURCES = (
    "Sources — Aldermore Bank PLC (company solo, not the Aldermore Group PLC holding company), "
    "Statement of cash flows from each year's full statutory accounts filed at Companies House "
    "(company no. 00947662), £m:\n"
    f"FY2025 & FY2024 (restated): Full accounts made up to 30 June 2025, filed 04 Nov 2025, p.55 — {CH_2025_URL}\n"
    f"FY2023: Full accounts made up to 30 June 2023, filed 27 Oct 2023, p.53 — {CH_2023_URL}\n"
    f"FY2022: Full accounts made up to 30 June 2022, filed 19 Oct 2022, p.60 — {CH_2022_URL}\n"
    f"FY2021: Full accounts made up to 30 June 2021, filed 04 Nov 2021, p.59 — {CH_2021_URL}\n"
    f"FY2020: Full accounts for the year ended 30 June 2020, filed 13 Nov 2020, p.62 — {CH_2020_URL}\n"
    f"FY2019 & FY2018 (18-month period ended 30 Jun 2018): Full accounts for the year ended 30 June 2019, "
    f"filed 22 Nov 2019, p.51 — {CH_2019_URL}\n"
    f"FY2016 & FY2015: Full accounts for the year ended 31 December 2016, filed 11 May 2017, p.28 — {CH_2016_URL}\n"
    f"FY2014: Full accounts for the year ended 31 December 2015, filed 23 May 2016, p.78 (FY2014 comparative) — {CH_2015_URL}\n"
    "(FY2024 accounts as originally filed are superseded by the FY2025 accounts' restated FY2024 comparative used here — "
    f"{CH_2024_URL})\n"
    "FY2017 has no standalone 12-month cash flow statement (see YEARS comment above); FY2018's column is an "
    "18-month period (1 Jan 2017 - 30 Jun 2018), not a 12-month year, so its flows are roughly 1.5x a normal "
    "year's and are not directly comparable to the years either side of it without adjusting for the extra "
    "6 months.\n"
    "Note: the Bank reclassified its FY2024 comparative cash flow statement (see FY2025 accounts, p.55) to move interest "
    "received/paid on the intercompany loan, interest paid on subordinated notes, and interest received on debt "
    "securities from investing/financing activities into operating activities, and to reclassify proceeds from disposal "
    "of a non-current asset held for sale into operating activities; amounts relating to intercompany loans are also now "
    "presented gross rather than net. FY2023/FY2022/FY2021 below are presented as originally filed under the older "
    "(pre-reclassification) basis. Blank cells indicate a line item was not part of that year's classification of cash "
    "flows; section totals (net cash from operating/investing/financing activities, net change, opening/closing cash) "
    "are directly as reported and comparable across all 5 years. Minor (≤£0.1m) differences between individual line "
    "items and their printed subtotals in the FY2023/FY2022 source documents are presented as disclosed, not adjusted.\n\n"
    "HD-073 (2026-09-06): checked for FY2009-FY2013 (the Balance Sheet/P&L/Equity sheets' new floor) - no Cash "
    "Flow Statement exists in the Bank's FY2009-FY2013 statutory accounts at all. UK banking companies were "
    "exempt from FRS 1 (Cash Flow Statements) under the old UK GAAP framework these years were prepared under "
    "(confirmed directly against the accounts' own contents pages and full text - no such statement is listed "
    "or present in any of the 5 years' filings). This sheet is left with no FY2009-FY2013 columns at all: a "
    "genuine whole-sheet, multi-year self-skip, not a missed document."
)

HIST_P3_NOTE = (
    "FY2013, FY2012 and FY2011 — HISTORICAL BASEL II EDITIONS, recovered from the Internet Archive on 15 "
    "September 2026 and previously outside this workbook's Pillar 3 coverage (HD-073 floored it at FY2014). "
    "Read the basis caveats before using these three columns.\n"
    f"FY2013 (year ended 31 DECEMBER 2013): Aldermore Bank PLC — Pillar 3 Disclosures 31 December 2013, "
    f"Section 4 'Capital Resources', p.9, and Section 5.1 'Credit Risk Exposure', p.11 — {P3_2013_URL}\n"
    "  - Capital, stated in narrative: 'As at 31 December 2013, the Bank's capital base was made up of £250.4 "
    "million of Tier 1 capital and £39.3 million of Tier 2 capital. Tier 1 capital consisted of fully issued "
    "ordinary shares ... and audited reserves. Tier 2 capital relates to issued subordinated loan notes and "
    "general provisions. The Bank does not hold any Tier 3 capital.'\n"
    "  - Pillar 1 CAPITAL requirement by exposure class (p.11, 'Exposure value / Pillar 1 Capital (8% x Risk "
    "Weight)'): total exposure value £4,746,619k against total credit-risk Pillar 1 capital of £165,031k. "
    "Operational risk Pillar 1 charge (Section 9, basic indicator approach): £6.5m.\n"
    f"FY2011 (year ended 31 DECEMBER 2011): Aldermore Bank Plc — Pillar 3 Disclosures December 31 2011, "
    f"Section 4 'Capital Resources', p.10, and Section 5.1 'Credit Risk Exposures', p.12 — {P3_2011_URL}\n"
    "  - Capital composition table (£'000): Share capital 3,300; Share premium 170,133; Profit and loss "
    "reserve (7,290); Total Core Tier 1 capital 166,143; Total Tier 2 capital 1,374; Total capital 167,517; "
    "less deductions — Intangible Assets (7,915); TOTAL CAPITAL LESS DEDUCTIONS 159,602. The narrative on the "
    "same page states the post-deduction split directly: '£158.2m of Tier 1 capital and £1.4m of Tier 2 "
    "capital', Tier 1 being ordinary shares and audited reserves only, Tier 2 general provisions only, and no "
    "Tier 3.\n"
    "  - Pillar 1 CAPITAL requirement by exposure class (p.12): total exposure value £1,647,406k against total "
    "credit-risk Pillar 1 capital of £68,091k. Operational risk Pillar 1 charge (basic indicator approach): "
    "£1.9m.\n"
    f"FY2012 (year ended 31 DECEMBER 2012): RECOVERED 2026-09-18 — Aldermore Bank PLC — Pillar 3 Disclosures "
    f"31 December 2012, Section 4 'Capital Resources', p.10, Section 5.1 'Credit Risk Exposures', p.11, and "
    f"Section 9 (operational risk), p.18 — {P3_2012_URL}\n"
    "  *** THE PREVIOUS VERSION OF THIS NOTE SAID 'NO PILLAR 3 EDITION LOCATED' AND WAS WRONG. *** It stated "
    "that neither the Internet Archive capture of the Bank's investor document library nor the live site "
    "carried a 2012 edition. The edition sits on that library's identical "
    "/system/files/uploads/financialdocs/ path, named pillar_3_disclosure_2012_0.pdf, one character different "
    "from the 2011 and 2013 filenames already cited above. See P3_RECOVERY_NOTE.\n"
    "  - Capital composition table (£'000): Share capital 3,300; Share premium 171,823; Profit and loss "
    "reserve (4,192); Total Core Tier 1 capital 170,931; Total Tier 2 capital 36,207; TOTAL CAPITAL 207,138; "
    "less deductions — Intangible Assets (7,467); TOTAL CAPITAL LESS DEDUCTIONS 199,671. The narrative on the "
    "same page states the post-deduction split directly: 'the Bank's capital base was made up of £163.5m of "
    "Tier 1 capital and £36.2m of Tier 2 capital', Tier 1 being ordinary shares and audited reserves only "
    "(GENPRU 2.2.83 R), Tier 2 subordinated loan notes and general provisions, and no Tier 3.\n"
    "  - Pillar 1 CAPITAL requirement by exposure class (p.11, 'Exposure value / Pillar 1 Capital (8% x Risk "
    "Weight)'): total exposure value £2,844,633k against total credit-risk Pillar 1 capital of £110,063k. "
    "Operational risk Pillar 1 charge (basic indicator approach, p.18): £3.8m.\n"
    "  *** THIS EDITION SETTLES WHAT BASIS THE BASEL II NARRATIVE SPLITS ARE ON, WHICH MATTERS FOR FY2013. *** "
    "The 2012 narrative's £163.5m + £36.2m sums to £199.7m, which is exactly that edition's printed 'Total "
    "capital less deductions' of £199,671k — so the narrative pair is stated AFTER deductions. The 2013 "
    "edition uses the identical sentence ('made up of £250.4 million of Tier 1 capital and £39.3 million of "
    "Tier 2 capital') and prints no table at all. That makes £289.7m the near-certain FY2013 total capital "
    "after deductions — but it is still an addition performed here rather than a figure the 2013 document "
    "prints, so it stays in this note and out of the Total Capital cell. Both FY2013 components are on their "
    "own rows of the Total Capital sheet instead, exactly as printed.\n"
    "BASIS CAVEATS FOR ALL THREE COLUMNS. (1) These are Basel II / CRD documents predating CRD IV, so the CET1 "
    "concept did not formally exist; the figures recorded on the CET1 sheets are each document's own Core "
    "Tier 1 / Tier 1 measure, which in both years comprised ordinary shares and audited reserves with no AT1 "
    "or hybrid instrument of any kind — a point each document states expressly. (2) NEITHER EDITION DISCLOSES "
    "A RISK-WEIGHTED-ASSET FIGURE OR ANY CAPITAL RATIO. They give the Pillar 1 CAPITAL requirement (8% x risk "
    "weight) instead. Total RWAs, CET1 Ratio, Tier 1 Ratio and Total Capital Ratio are therefore left blank "
    "for FY2013 and FY2011 and are NOT back-solved by grossing the capital requirement up by 12.5, and the "
    "capital figures that ARE disclosed are shown on the RWA Breakdown sheet as capital, on their own labelled "
    "rows, rather than converted. (3) Leverage ratio, LCR and NSFR are marked 'n/a': none existed as a UK "
    "disclosure requirement in 2011 or 2013 (the CRR leverage ratio, the LCR and the NSFR arrived with CRD "
    "IV/CRR in 2014, 2015 and 2022 respectively), and neither document contains any of them.\n"
    "VALIDATION GATE PASSED. FY2011's Total Core Tier 1 capital of £166,143k reproduces exactly the £166.1m "
    "Total equity already carried in this workbook's FY2011 Balance Sheet column from the Bank's own statutory "
    "accounts — an independent confirmation that the recovered document is the right entity and the right "
    "period. FY2013's £250.4m Tier 1 sits £7.0m below that year's £257.4m statutory Total equity, the same "
    "shape as FY2011's £7.9m intangible-asset deduction, and below the £280.7m CET1 already recorded for "
    "FY2014 — both consistent, neither forced. Nothing existing was overwritten: all three columns were "
    "entirely empty on these sheets before this pass."
)


P3_RECOVERY_NOTE = (
    "*** PILLAR 3 RECOVERY, 2026-09-18 — FY2016, FY2020 AND FY2012 WERE NEVER MISSING. READ THIS BEFORE "
    "TRUSTING ANY 'NO DOCUMENT EXISTS' CLAIM IN THIS WORKBOOK ***\n"
    "Until today this workbook stated, in five separate sheet notes, that no Pillar 3 disclosure document "
    "could be located for FY2016 or FY2020 'despite real effort (the Bank's own site, Wayback Machine CDX "
    "search, and web search)', and that FY2012 had 'NO PILLAR 3 EDITION LOCATED'. All three exist. All three "
    "were found on 2026-09-18 in under ten minutes, and the two reasons they had been missed are worth "
    "recording because they generalise:\n"
    "  (1) THE FY2016 EDITION'S FILENAME CONTAINS NO YEAR. It is 'pillar_3_disclosures.pdf' — every sibling "
    "edition is 'pillar_3_disclosure_2011_0.pdf', 'pillar-3-2022_0.pdf', "
    "'...-at-30-june-2019.pdf' and so on. Any search keyed on the year pattern skips straight past it. It was "
    "found by enumerating the ENTIRE archived host (Wayback CDX, url=investors.aldermore.co.uk/*, ~10,000 "
    "rows) and reading the 13 results whose path contained 'pillar' — not by guessing a URL. Opening it "
    "shows a cover page reading 'Aldermore Group PLC / Pillar 3 Disclosures / 31 December 2016'. The FY2012 "
    "edition turned up in the same listing, on the identical /financialdocs/ path as the 2011 and 2013 "
    "editions this script already cited.\n"
    "  (2) THE FY2020 EDITION WAS NEVER LOST AT ALL — it is linked from Aldermore's live investor index "
    "today. A comment added to this script on 2026-09-16 records having found it and set it aside because it "
    "'prints no key-metrics table of any kind'. That was true and beside the point: UK KM1 did not apply "
    "before 1 January 2022, but the edition carries a ten-page 'Appendix 1: Disclosures for Aldermore Bank "
    "PLC' with the Bank's full capital composition, RWA split and leverage tables. A document was judged on "
    "one absent template rather than opened.\n"
    "WHAT THIS CHANGED: FY2016 and FY2020 now have CET1/Tier 1/Total capital, all three capital ratios, total "
    "RWAs, an RWA split and a leverage ratio — on the Bank-solo basis every other column on these sheets uses "
    "— and FY2012 has its Basel II capital and Pillar 1 capital requirement. Nothing was estimated.\n"
    "VALIDATION, AND IT IS STRONG. Each recovered edition prints a prior-year comparative, and every one of "
    "those comparatives reproduces a column this workbook already held, to the £0.1m. The FY2016 edition's 31 "
    "December 2015 column: CET1 433.2, Tier 1 507.5, total capital 556.1, RWA 3,687.5 (credit 3,480.6 / "
    "market 0.1 / operational 205.5 / CVA 1.3), leverage exposure 7,095.9 and ratio 7.2% — identical to this "
    "workbook's existing FY2015 figures, which came from a different document. The FY2020 edition's 30 June "
    "2019 column: CET1 781.6, Tier 1 855.9, total capital 1,015.9, RWA 6,179.0 (credit 5,643.3 / market 0.3 / "
    "operational 533.3 / CVA 2.1) — again identical to the existing FY2019 column. And the FY2016 edition's "
    "own Bank CET1 ratio of 11.4% and the FY2020 edition's 13.4% are exactly the two figures this workbook "
    "had already taken from the Annual Report highlights, which is what confirms the highlight ratios were "
    "Bank-basis rather than Group (the same tables show Group at 11.5% and 13.3%).\n"
    "ONE FIGURE NOT REPRODUCED, RECORDED NOT RECONCILED: the FY2020 edition's 30 June 2019 leverage exposure "
    "is £12,582.8m, where the FY2019 edition itself printed £12,671.6m for that date. The FY2019 column here "
    "keeps its own edition's £12,671.6m, per this project's convention; the ratio is 6.8% on both."
)


def p3_sources(page_25="4", page_24="4", page_22="4", page_26="6"):
    return (
        "Sources — Aldermore Bank PLC solo figures from the 'Key metrics'/capital-composition tables (Bank "
        "columns), Aldermore Group PLC Pillar 3 Disclosures (and the Bank's own Annual Report highlights where "
        "noted):\n"
        f"FY2026: Pillar 3 Report for the year ended 30 June 2026, p.{page_26} (UK KM1 — Key metrics template, "
        f"Bank column a, 30-Jun-26) — {P3_2026_URL}\n"
        f"FY2025 & FY2024: Pillar 3 Disclosures for the year ended 30 June 2025, p.{page_25} (Key metrics) — {P3_2025_URL}\n"
        f"FY2023: Pillar 3 Disclosures for the year ended 30 June 2024, p.{page_24} (Key metrics, FY2023 comparative) — {P3_2024_URL}\n"
        f"FY2022 & FY2021: Pillar 3 Disclosures for the year ended 30 June 2022, p.{page_22} (Key metrics) — {P3_2022_URL}\n"
        f"FY2019 & FY2018: Pillar 3 Disclosures for the year ended 30 June 2019, p.57-61 (Appendix 1, Disclosures "
        f"for Aldermore Bank PLC — Total minimum Pillar 1 capital requirement, Capital composition, Leverage "
        f"ratio) — {P3_2019_URL}\n"
        f"FY2015 & FY2014: Pillar 3 Disclosures 31 December 2015, p.58-61 (Appendix 1, Disclosures for Aldermore "
        f"Bank PLC — Total minimum Pillar 1 capital requirement, Capital composition, Leverage ratio) — {P3_2015_URL}\n"
        f"FY2020: Aldermore Group PLC Pillar 3 Disclosures, year ended 30 June 2020, p.61-62 (Appendix 1, Table "
        f"34 Total minimum Pillar 1 capital requirement (Bank only) and Table 35 Capital composition (Bank "
        f"only)) and p.64-65 (Tables 38/39, Leverage ratio (Bank only)) — {P3_2020_URL}\n"
        f"FY2016: Aldermore Group PLC Pillar 3 Disclosures 31 December 2016, p.58-59 (Appendix 1, Table 34 Total "
        f"minimum Pillar 1 capital requirement (Bank only) and Table 35 Capital composition (Bank only)) and "
        f"p.61-62 (Tables 38/39, Leverage ratio (Bank only)) — {P3_2016_URL}\n"
        f"FY2012: Aldermore Bank PLC — Pillar 3 Disclosures 31 December 2012, p.10 (Capital Resources), p.11 "
        f"(Credit Risk Exposures) and p.18 (operational risk charge) — {P3_2012_URL}\n"
        "FY2017 has no standalone Pillar 3 disclosure at all, and this is STRUCTURAL rather than a sourcing "
        "failure: the FY2018 edition states that the Group moved to \"an 18 month reporting period to 30 June "
        "2018 for both the ARA and Pillar 3 documents\", so no 31 December 2017 reporting date exists to "
        "disclose against. Companies House shows the same shape on the statutory side — Aldermore Bank PLC "
        "accounts for the year ended 31 December 2016, then the 18-month period to 30 June 2018, with nothing "
        "in between (filing history enumerated in full on 2026-09-18). FY2018's column reflects that 18-month "
        "transition period. THE ONE 31 DECEMBER 2017 CAPITAL DATA POINT THAT DOES EXIST is deliberately not "
        "used: Aldermore Group PLC's unaudited interim results press release of 19 March 2018 gives a CET1 "
        "ratio of 12.2% and a total capital ratio of 15.2% at 31 December 2017 — but those are GROUP figures, "
        "unaudited, and every column on these sheets is Aldermore Bank PLC solo. Putting them here would break "
        "the entity basis silently. They are recorded in this note instead.\n"
        + HIST_P3_NOTE + "\n" + P3_RECOVERY_NOTE + "\n"
        "FY2026 columns cover the Pillar 3 metric sheets and RWA Breakdown only. The statutory sheets (Balance "
        "Sheet, Profit & Loss, Statement of Changes in Equity, Cash Flow Statement) and Asset Quality have no "
        "FY2026 column: Aldermore Bank PLC's own FY2026 statutory accounts have not been filed at Companies "
        "House yet (latest is the year ended 30 June 2025, filed 03 Nov 2025), and the Group's FY2026 Annual "
        "Report cannot substitute — its 'Company' statements are Aldermore Group PLC, the holding company "
        f"(total assets £1,102.2m, p.188), not Aldermore Bank PLC — {ARA_2026_URL}"
    )

bw = BankWorkbook(bank_name="Aldermore Bank PLC", years=YEARS, year_label=YEAR_LABEL, header_color="AD1457")

# ---------------------------------------------------------------
# Sheet: Balance Sheet (Statement of Financial Position)
# ---------------------------------------------------------------
BALANCE_SHEET_SOURCES = (
    "Sources — Aldermore Bank PLC (company solo, not the Aldermore Group PLC holding company), Statement of "
    "financial position from each year's full statutory accounts filed at Companies House (company no. 00947662), "
    "£m:\n"
    f"FY2025 & FY2024: Full accounts made up to 30 June 2025, filed 04 Nov 2025, p.54 — {CH_2025_URL}\n"
    f"FY2023 & FY2022: Full accounts made up to 30 June 2023, filed 27 Oct 2023, p.52 — {CH_2023_URL}\n"
    f"FY2021: Full accounts made up to 30 June 2021, filed 04 Nov 2021, p.58 — {CH_2021_URL}\n"
    f"FY2020: Full accounts for the year ended 30 June 2020, filed 13 Nov 2020, p.61 — {CH_2020_URL}\n"
    f"FY2019 & FY2018: Full accounts for the year ended 30 June 2019, filed 22 Nov 2019, p.49 — {CH_2019_URL}\n"
    f"FY2016 & FY2015: Full accounts for the year ended 31 December 2016, filed 11 May 2017, p.27 — {CH_2016_URL}\n"
    f"FY2014: Full accounts for the year ended 31 December 2015, filed 23 May 2016, p.77 (FY2014 comparative) — {CH_2015_URL}\n"
    "FY2017 has no standalone 12-month Statement of financial position: following the Bank's 2018 acquisition by "
    "FirstRand, its accounting reference date changed from 31 December to 30 June, producing one 18-month set of "
    "accounts (1 Jan 2017 - 30 Jun 2018, shown here as FY2018) instead of a normal FY2017 + FY2018 pair — FY2017 "
    "is left blank rather than estimated. FY2018's column is therefore an 18-month, not 12-month, snapshot; as a "
    "balance-sheet (point-in-time) statement this affects comparability less than the flow statements, but the "
    "period length difference should still be borne in mind when reading growth between FY2016 and FY2018.\n"
    "Note: minor (£0.1m) rounding differences appear between the Total equity figure on the face of the "
    "Statement of financial position and the Statement of Changes in Equity's closing balance in some years "
    "(e.g. FY2021: £987.1m here vs £987.2m per the FY2021 accounts' own Statement of Changes in Equity) — "
    "both are presented exactly as disclosed in their respective source tables, not reconciled.\n\n"
    "Debt securities breakdown (measurement basis + issuer type), added as sub-rows directly beneath the "
    "'Debt securities' line, sourced from the 'Debt securities' note of each year's own full statutory "
    "accounts (same Companies House filings/pages as above): FY2025/FY2024 — Note 12, p.79 of the FY2025 "
    f"filing ({CH_2025_URL}); FY2023/FY2022 — Note 11, p.78 of the FY2023 filing ({CH_2023_URL}); "
    f"FY2021/FY2020 — Note 16, p.86 of the FY2021 filing ({CH_2021_URL}). FY2020's 'UK Government gilts / "
    "treasury bills' sub-row (£235.0m) combines that year's own 'UK Government gilts and treasury bills' "
    "line (£188.9m) with a separate 'Treasury Bills' line (£46.1m) disclosed only as a FY2020 comparative in "
    "the FY2021 accounts. Sub-row sums reconcile to the 'Debt securities' total in every sourced year except "
    "FY2023 (£2,048.8m per the note vs £2,048.9m on the face of the Statement of financial position) and "
    "FY2022 (£2,339.3m vs £2,339.2m) — both are pre-existing £0.1m rounding artefacts in the Bank's own "
    "disclosures, not reconciled here. No equivalent note-level breakdown was sourced for FY2019 and earlier "
    "within this pass's scope (FY2020-FY2025 prioritised).\n\n"
    "HD-073 extension (FY2009-FY2013): sourced from the Bank's own full statutory accounts filed at Companies "
    "House, scanned/OCR'd (no text layer in the filed PDFs), prepared under old UK GAAP (not IFRS) as these "
    "pre-date the Bank's IFRS transition:\n"
    f"FY2013 & FY2012: Full accounts made up to 31 December 2013, filed 28 Apr 2014, p.38 — {CH_2013_URL}\n"
    f"FY2011 & FY2010: Full accounts made up to 31 December 2011, filed 13 Apr 2012, p.17 — {CH_2011_URL}\n"
    f"FY2010 & FY2009: Full accounts made up to 31 December 2010, filed 27 Apr 2011, p.17 — {CH_2010_URL}\n"
    "FY2009 is a 9-month stub period (1 Apr 2009 - 31 Dec 2009), not a full calendar year — see YEARS comment.\n"
    "Line-item mapping notes for these 5 years: 'Other liabilities, accruals and deferred income' is the sum "
    "of the old accounts' two separate 'Other liabilities' and 'Accruals and deferred income' lines (£69.5m/"
    "£56.3m/£40.5m/£26.0m/£12.0m for FY2013-FY2009 respectively) rather than a single disclosed figure, to "
    "match this row's combined modern-era presentation; 'Property, plant and equipment' maps to the old "
    "accounts' 'Tangible fixed assets' line; 'Deferred taxation' and 'Taxation liability' map to the old "
    "accounts' 'Deferred tax asset' and 'Taxation' lines respectively. Lines with no entry for FY2009-FY2013 "
    "(Amounts owed by/to other Group undertakings, Derivatives held for risk management, Fair value adjustment "
    "for portfolio hedged risk, Additional Tier 1 capital, FVOCI reserve, Debt securities in issue) did not "
    "exist on the Bank's balance sheet at all in this pre-IFRS/pre-Tier-1-issuance era — genuinely absent, not "
    "omitted. 'Amounts due to banks', 'Provisions', and 'Subordinated notes' are similarly blank for FY2011-"
    "FY2009 specifically (first appear as separate lines from FY2012); 'Capital contribution / redemption "
    "reserve' is blank before FY2012, the year the Bank's ultimate parent first made a non-returnable capital "
    "contribution (see the Statement of Changes in Equity sheet's source note)."
)

NO_FY2017 = "No 31 Dec 2017 period exists (18-month transition)"

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 1182.3, "FY2024": 2172.2, "FY2023": 1923.4, "FY2022": 838.3, "FY2021": 688.5, "FY2020": 542.4, "FY2019": 482.9, "FY2018": 508.8, "FY2016": 116.4, "FY2015": 105.3, "FY2014": 79.6, "FY2013": 192.8, "FY2012": 1.7, "FY2011": 0.1}),
    ("DATA", "Loans and advances to banks", {"FY2025": 183.6, "FY2024": 170.1, "FY2023": 206.5, "FY2022": 132.8, "FY2021": 106.4, "FY2020": 177.5, "FY2019": 110.6, "FY2018": 80.4, "FY2016": 43.4, "FY2015": 64.0, "FY2014": 86.8, "FY2013": 223.9, "FY2012": 83.1, "FY2011": 123.1, "FY2010": 219.3, "FY2009": 83.5}),
    ("DATA", "Amounts owed by / receivable from other Group undertakings", {"FY2025": 3779.6, "FY2024": 3720.5, "FY2023": 3525.1, "FY2022": 3072.5, "FY2021": 2303.8, "FY2020": 1615.2, "FY2019": 390.7, "FY2018": 20.7, "FY2016": 1.5, "FY2015": 0.9, "FY2014": 1.6}),
    ("DATA", "Total debt securities", {"FY2025": 2704.2, "FY2024": 2436.5, "FY2023": 2048.9, "FY2022": 2339.2, "FY2021": 1999.5, "FY2020": 1941.1, "FY2019": 1207.8, "FY2018": 829.9, "FY2016": 699.8, "FY2015": 640.1, "FY2014": 542.3, "FY2013": 339.4, "FY2012": 312.2, "FY2011": 228.0, "FY2010": 35.8, "FY2009": 37.4}),
    ("DATA", "Debt securities: FVOCI (fair value through other comprehensive income) — UK Government gilts / treasury bills", {"FY2025": 259.1, "FY2024": 187.2, "FY2023": 113.6, "FY2022": 156.8, "FY2021": 133.3, "FY2020": 235.0}),
    ("DATA", "Debt securities: FVOCI (fair value through other comprehensive income) — Supranational bonds", {"FY2025": 1188.8, "FY2024": 871.7, "FY2023": 742.0, "FY2022": 963.9, "FY2021": 1061.2, "FY2020": 990.7}),
    ("DATA", "Debt securities: FVOCI (fair value through other comprehensive income) — Asset-backed securities (other investment securities)", {"FY2025": 255.2, "FY2024": 200.7, "FY2023": 112.8, "FY2022": 146.0, "FY2021": 115.4, "FY2020": 114.4}),
    ("DATA", "Debt securities: FVOCI (fair value through other comprehensive income) — Covered bonds (other investment securities)", {"FY2025": 672.0, "FY2024": 802.0, "FY2023": 553.1, "FY2022": 681.2, "FY2021": 495.9, "FY2020": 529.7}),
    ("DATA", "Debt securities: amortised cost — UK Government gilts", {"FY2025": 256.8, "FY2024": 176.8, "FY2023": 270.8, "FY2022": 150.3, "FY2021": 107.3, "FY2020": 48.4}),
    ("DATA", "Debt securities: amortised cost — Supranational bonds (other investment securities)", {"FY2025": 72.3, "FY2024": 198.1, "FY2023": 256.5, "FY2022": 241.1, "FY2021": 86.4, "FY2020": 22.9}),
    ("DATA", "Derivatives held for risk management", {"FY2025": 170.1, "FY2024": 344.2, "FY2023": 666.3, "FY2022": 259.9, "FY2021": 18.9, "FY2020": 9.1, "FY2019": 9.1, "FY2018": 24.0, "FY2016": 17.5, "FY2015": 17.5, "FY2014": 25.6}),
    ("DATA", "Loans and advances to customers", {"FY2025": 12523.4, "FY2024": 11416.3, "FY2023": 10998.9, "FY2022": 10777.3, "FY2021": 10393.6, "FY2020": 10602.2, "FY2019": 10230.3, "FY2018": 8990.5, "FY2016": 7477.3, "FY2015": 6144.8, "FY2014": 4801.1, "FY2013": 3370.8, "FY2012": 2059.6, "FY2011": 1160.4, "FY2010": 475.0, "FY2009": 160.6}),
    ("DATA", "Fair value adjustment for portfolio hedged risk", {"FY2025": 18.8, "FY2024": -129.0, "FY2023": -400.1, "FY2022": -180.2, "FY2021": 15.2, "FY2020": 55.8, "FY2019": 17.9, "FY2018": -15.7, "FY2016": -3.5, "FY2015": 1.1}),
    ("DATA", "Non-current assets held for sale", {"FY2023": 32.8}),
    ("DATA", "Other assets", {"FY2025": 2.8, "FY2024": 9.2, "FY2023": 6.0, "FY2022": 1.6, "FY2021": 2.0, "FY2020": 0, "FY2019": 2.8, "FY2018": 6.4, "FY2016": 3.7, "FY2015": 2.5, "FY2014": 4.7, "FY2013": 11.5, "FY2012": 22.4, "FY2011": 14.3, "FY2010": 4.3, "FY2009": 1.2}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 23.6, "FY2024": 22.8, "FY2023": 17.8, "FY2022": 14.5, "FY2021": 13.3, "FY2020": 11.3, "FY2019": 5.3, "FY2018": 6.2, "FY2016": 3.4, "FY2015": 5.1, "FY2014": 6.7, "FY2013": 32.5, "FY2012": 21.8, "FY2011": 12.9, "FY2010": 5.8, "FY2009": 2.5}),
    ("DATA", "Taxation asset", {"FY2025": 2.9, "FY2024": 2.2, "FY2023": 0, "FY2022": 7.0, "FY2021": 0.7, "FY2020": 11.8}),
    ("DATA", "Deferred taxation", {"FY2025": 6.3, "FY2024": 5.7, "FY2023": 6.1, "FY2022": 2.6, "FY2021": 5.7, "FY2020": 3.4, "FY2019": 3.7, "FY2018": 2.3, "FY2016": 12.0, "FY2015": 16.9, "FY2014": 6.4, "FY2013": 3.5}),
    ("DATA", "Property, plant and equipment", {"FY2025": 16.3, "FY2024": 20.5, "FY2023": 15.7, "FY2022": 20.8, "FY2021": 25.8, "FY2020": 23.2, "FY2019": 3.8, "FY2018": 3.7, "FY2016": 3.1, "FY2015": 3.4, "FY2014": 2.8, "FY2013": 12.9, "FY2012": 11.4, "FY2011": 7.4, "FY2010": 3.8, "FY2009": 2.0}),
    ("DATA", "Intangible assets", {"FY2025": 4.3, "FY2024": 4.3, "FY2023": 4.3, "FY2022": 4.5, "FY2021": 9.6, "FY2020": 7.7, "FY2019": 7.0, "FY2018": 10.2, "FY2016": 21.9, "FY2015": 19.8, "FY2014": 18.4, "FY2013": 7.0, "FY2012": 7.5, "FY2011": 7.9, "FY2010": 8.4, "FY2009": 7.6}),
    ("TOTAL", "Total assets", {"FY2025": 20618.2, "FY2024": 20195.5, "FY2023": 19051.7, "FY2022": 17290.8, "FY2021": 15583.0, "FY2020": 15000.7, "FY2019": 12471.9, "FY2018": 10467.4, "FY2016": 8396.5, "FY2015": 7021.4, "FY2014": 5583.2, "FY2013": 4194.3, "FY2012": 2519.6, "FY2011": 1554.1, "FY2010": 752.3, "FY2009": 294.7}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Amounts due to banks", {"FY2025": 795.8, "FY2024": 1365.3, "FY2023": 1681.9, "FY2022": 1341.8, "FY2021": 1326.6, "FY2020": 2173.5, "FY2019": 1814.6, "FY2018": 1678.2, "FY2016": 753.8, "FY2015": 405.1, "FY2014": 305.9, "FY2013": 384.3, "FY2012": 115.1}),
    ("DATA", "Customers' accounts", {"FY2025": 17047.6, "FY2024": 16306.7, "FY2023": 15033.3, "FY2022": 14105.4, "FY2021": 12427.3, "FY2020": 10886.4, "FY2019": 8971.8, "FY2018": 7776.3, "FY2016": 6673.7, "FY2015": 5742.0, "FY2014": 4459.0, "FY2013": 3444.4, "FY2012": 2141.2, "FY2011": 1347.5, "FY2010": 634.7, "FY2009": 229.6}),
    ("DATA", "Derivatives held for risk management", {"FY2025": 94.1, "FY2024": 37.8, "FY2023": 62.5, "FY2022": 24.5, "FY2021": 40.0, "FY2020": 93.2, "FY2019": 36.6, "FY2018": 16.6, "FY2016": 35.3, "FY2015": 35.2, "FY2014": 53.5}),
    ("DATA", "Fair value adjustment for portfolio hedged risk", {"FY2025": 16.4, "FY2024": 6.5, "FY2023": -21.0, "FY2022": -12.7, "FY2021": 0, "FY2020": 2.1, "FY2019": 1.0, "FY2018": 0.2, "FY2016": -1.2, "FY2015": -0.8, "FY2014": 1.5}),
    ("DATA", "Amounts owed / payable to other Group undertakings", {"FY2025": 952.5, "FY2024": 909.2, "FY2023": 862.0, "FY2022": 531.5, "FY2021": 537.2, "FY2020": 714.4, "FY2019": 550.9, "FY2018": 104.5, "FY2016": 153.1, "FY2015": 213.4, "FY2014": 302.7}),
    ("DATA", "Other liabilities, accruals and deferred income", {"FY2025": 93.3, "FY2024": 96.7, "FY2023": 105.2, "FY2022": 97.9, "FY2021": 92.4, "FY2020": 71.2, "FY2019": 62.0, "FY2018": 57.6, "FY2016": 51.9, "FY2015": 47.5, "FY2014": 38.8, "FY2013": 69.5, "FY2012": 56.3, "FY2011": 40.5, "FY2010": 26.0, "FY2009": 12.0}),
    ("DATA", "Taxation liability", {"FY2023": 6.0, "FY2020": 0, "FY2019": 18.3, "FY2018": 5.8, "FY2016": 9.7, "FY2015": 12.5, "FY2014": 8.2, "FY2013": 2.5}),
    ("DATA", "Provisions", {"FY2025": 3.0, "FY2024": 0.6, "FY2023": 2.5, "FY2022": 3.8, "FY2021": 2.7, "FY2020": 2.5, "FY2019": 2.4, "FY2018": 1.0, "FY2016": 0.8, "FY2015": 1.1, "FY2014": 2.0, "FY2013": 1.2, "FY2012": 0.6}),
    ("DATA", "Debt securities in issue", {"FY2023": -0.2, "FY2022": -0.5}),
    ("DATA", "Subordinated notes", {"FY2025": 100.9, "FY2024": 100.9, "FY2023": 100.5, "FY2022": 100.5, "FY2021": 161.4, "FY2020": 161.2, "FY2019": 161.1, "FY2018": 60.5, "FY2016": 100.0, "FY2015": 38.1, "FY2014": 36.8, "FY2013": 35.1, "FY2012": 34.1}),
    ("TOTAL", "Total liabilities", {"FY2025": 17050.8, "FY2024": 18823.7, "FY2023": 17832.7, "FY2022": 16192.2, "FY2021": 14595.9, "FY2020": 14104.5, "FY2019": 11618.7, "FY2018": 9700.7, "FY2016": 7777.1, "FY2015": 6494.1, "FY2014": 5208.4, "FY2013": 3936.9, "FY2012": 2347.3, "FY2011": 1388.0, "FY2010": 660.7, "FY2009": 241.6}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 3.3, "FY2024": 3.3, "FY2023": 3.3, "FY2022": 3.3, "FY2021": 3.3, "FY2020": 3.3, "FY2019": 3.3, "FY2018": 3.3, "FY2016": 3.3, "FY2015": 3.3, "FY2014": 3.3, "FY2013": 3.3, "FY2012": 3.3, "FY2011": 3.3, "FY2010": 3.3, "FY2009": 3.3}),
    ("DATA", "Share premium account", {"FY2025": 307.5, "FY2024": 307.5, "FY2023": 307.5, "FY2022": 307.5, "FY2021": 307.5, "FY2020": 307.5, "FY2019": 307.6, "FY2018": 307.6, "FY2016": 307.6, "FY2015": 307.6, "FY2014": 233.4, "FY2013": 233.4, "FY2012": 171.8, "FY2011": 170.1, "FY2010": 94.7, "FY2009": 47.4}),
    ("DATA", "Additional Tier 1 capital", {"FY2025": 50.0, "FY2024": 61.0, "FY2023": 61.0, "FY2022": 61.0, "FY2021": 61.0, "FY2020": 61.0, "FY2019": 74.3, "FY2018": 74.3, "FY2016": 74.3, "FY2015": 74.3, "FY2014": 74.3}),
    ("DATA", "Capital contribution / redemption reserve", {"FY2018": 0, "FY2016": 6.9, "FY2015": 3.4, "FY2014": 3.1, "FY2013": 2.5, "FY2012": 2.3}),
    ("DATA", "FVOCI / fair value through other comprehensive income reserve", {"FY2025": -5.0, "FY2024": -0.7, "FY2023": 3.3, "FY2022": 6.9, "FY2021": 8.3, "FY2020": 1.5, "FY2019": 0.4, "FY2018": 1.1, "FY2016": 1.8, "FY2015": -1.0, "FY2014": 1.4}),
    ("DATA", "Retained earnings", {"FY2025": 1158.8, "FY2024": 1000.7, "FY2023": 843.9, "FY2022": 719.9, "FY2021": 607.0, "FY2020": 522.9, "FY2019": 467.6, "FY2018": 380.4, "FY2016": 225.5, "FY2015": 139.7, "FY2014": 59.3, "FY2013": 18.2, "FY2012": -5.2, "FY2011": -7.3, "FY2010": -6.4, "FY2009": 2.4}),
    ("TOTAL", "Total equity", {"FY2025": 1514.6, "FY2024": 1371.8, "FY2023": 1219.0, "FY2022": 1098.6, "FY2021": 987.1, "FY2020": 896.2, "FY2019": 853.2, "FY2018": 766.7, "FY2016": 619.4, "FY2015": 527.3, "FY2014": 374.8, "FY2013": 257.4, "FY2012": 172.3, "FY2011": 166.1, "FY2010": 91.6, "FY2009": 53.1}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 20618.2, "FY2024": 20195.5, "FY2023": 19051.7, "FY2022": 17290.8, "FY2021": 15583.0, "FY2020": 15000.7, "FY2019": 12471.9, "FY2018": 10467.4, "FY2016": 8396.5, "FY2015": 7021.4, "FY2014": 5583.2, "FY2013": 4194.3, "FY2012": 2519.6, "FY2011": 1554.1, "FY2010": 752.3, "FY2009": 294.7}),
    ("SECTION", "FY2017 - no 31 December 2017 reporting date exists. Aldermore changed its accounting reference date and ran an 18-month transition period from 1 January 2017 to 30 June 2018, reported in the FY2018 column. There is no FY2017 edition to open and no FY2017 figure that could be found; the Companies House filing history runs 31 Dec 2016 straight to 30 Jun 2018. Stated explicitly so the column does not read as an unclosed gap", {}),
    ("DATA", "Period covered by this column", {"FY2017": NO_FY2017}),
]

bw.add_balance_sheet_sheet(
    title="Aldermore Bank PLC — Statement of Financial Position",
    subtitle="Company (Bank solo) basis, £m, as at 30 June",
    rows=balance_sheet_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=72,
    source_height=150,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss (Income Statement + Statement of Comprehensive Income)
# ---------------------------------------------------------------
INCOME_STATEMENT_SOURCES = (
    "Sources — Aldermore Bank PLC (company solo, not the Aldermore Group PLC holding company), Income "
    "statement and Statement of comprehensive income from each year's full statutory accounts filed at "
    "Companies House (company no. 00947662), £m:\n"
    f"FY2025 & FY2024: Full accounts made up to 30 June 2025, filed 04 Nov 2025, p.53 — {CH_2025_URL}\n"
    f"FY2023 & FY2022: Full accounts made up to 30 June 2023, filed 27 Oct 2023, p.50-51 — {CH_2023_URL}\n"
    f"FY2021: Full accounts made up to 30 June 2021, filed 04 Nov 2021, p.56-57 — {CH_2021_URL}\n"
    f"FY2020: Full accounts for the year ended 30 June 2020, filed 13 Nov 2020, p.59-60 — {CH_2020_URL}\n"
    f"FY2019 & FY2018: Full accounts for the year ended 30 June 2019, filed 22 Nov 2019, p.47-48 — {CH_2019_URL}\n"
    f"FY2016 & FY2015: Full accounts for the year ended 31 December 2016, filed 11 May 2017, p.25-26 — {CH_2016_URL}\n"
    f"FY2014: Full accounts for the year ended 31 December 2015, filed 23 May 2016, p.75-76 (FY2014 comparative) — {CH_2015_URL}\n"
    "FY2019's interest income/expense and net gains from derivatives comparative for FY2018 (period ended 30 June "
    "2018) were restated to align with FirstRand Group policy (total operating income unaffected) — the FY2018 "
    "figures here are the restated ones as re-presented in the FY2019 accounts, not the FY2018 accounts' own "
    "as-originally-filed figures (which had interest income £607.4m, interest expense £(172.5)m).\n"
    "FY2017 has no standalone 12-month period (see YEARS comment above); FY2018's column is an 18-month period "
    "(1 Jan 2017 - 30 Jun 2018), not a 12-month year, so flow figures (income, expenses, profit) are not directly "
    "comparable to the 12-month years either side of it without adjusting for the extra 6 months.\n"
    "Note: each year's own presentation of 'below net-interest-income' income/expense line items differs "
    "(IPO preparation costs in FY2014-FY2016; goodwill impairment in FY2016; transaction/integration costs and "
    "intangible/goodwill impairment in FY2018-FY2019; a combined single 'Administrative expenses' line from "
    "FY2022) — all are transcribed as disclosed in their own year, not restated onto a common basis, and each "
    "year's own reported subtotals/totals are used directly rather than recomputed from the line items shown.\n\n"
    "HD-073 extension (FY2009-FY2013): sourced from the same old-UK-GAAP statutory accounts as the Balance "
    "Sheet sheet (see that sheet's source note for document/page references and the GAAP-basis caveat). "
    "FY2009 is a 9-month stub period (1 Apr 2009 - 31 Dec 2009), not a full year — its flow figures are not "
    "directly comparable to the 12-month years either side without adjusting for the shorter period.\n"
    "Line-item mapping: 'Other expenses and staff costs / other administrative expenses' maps to the old "
    "accounts' standalone 'Administrative expenses' line, shown separately from depreciation in this era (the "
    "modern combined 'Administrative expenses' TOTAL row sums the two, as it does for later years); 'Other "
    "operating income' for FY2013/FY2012 additionally folds in the old accounts' separate 'Gains on disposal "
    "of debt securities' line (£1.9m/£3.2m), which has no standalone row in the modern presentation. Every "
    "FY2009-FY2013 year had zero other comprehensive income — each year's own Statement of Total Recognised "
    "Gains and Losses confirms total recognised gains/losses equal the profit/(loss) for the year exactly — "
    "so the OCI section is shown as 0 rather than blank for these years, and 'Provisions' (liabilities) has no "
    "entry for FY2011-FY2009 specifically since the old accounts show no such separate line for those years."
)

income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 1240.5, "FY2024": 1234.8, "FY2023": 878.7, "FY2022": 533.4, "FY2021": 473.6, "FY2020": 513.5, "FY2019": 470.1, "FY2018": 599.6, "FY2016": 362.3, "FY2015": 306.2, "FY2014": 235.2, "FY2013": 156.0, "FY2012": 97.8, "FY2011": 53.2, "FY2010": 24.5, "FY2009": 6.0}),
    ("DATA", "Interest expense", {"FY2025": -828.0, "FY2024": -808.1, "FY2023": -433.6, "FY2022": -152.5, "FY2021": -157.3, "FY2020": -201.9, "FY2019": -150.3, "FY2018": -168.3, "FY2016": -119.4, "FY2015": -103.6, "FY2014": -92.7, "FY2013": -75.9, "FY2012": -63.3, "FY2011": -30.6, "FY2010": -12.5, "FY2009": -4.1}),
    ("TOTAL", "Net interest income", {"FY2025": 412.5, "FY2024": 426.7, "FY2023": 445.1, "FY2022": 380.9, "FY2021": 316.3, "FY2020": 311.6, "FY2019": 319.8, "FY2018": 431.3, "FY2016": 242.9, "FY2015": 202.6, "FY2014": 142.5, "FY2013": 80.1, "FY2012": 34.5, "FY2011": 22.6, "FY2010": 12.0, "FY2009": 1.9}),
    ("DATA", "Fee and commission income / fee and other income", {"FY2025": 7.5, "FY2024": 7.1, "FY2023": 11.7, "FY2022": 6.0, "FY2021": 6.5, "FY2020": 5.8, "FY2019": 7.4, "FY2018": 36.6, "FY2016": 30.0, "FY2015": 25.2, "FY2014": 26.4, "FY2013": 31.1, "FY2012": 24.2, "FY2011": 18.2, "FY2010": 12.3, "FY2009": 1.4}),
    ("DATA", "Fee and commission expense", {"FY2025": -9.5, "FY2024": -8.2, "FY2023": -5.4, "FY2022": -5.6, "FY2021": -5.4, "FY2020": -5.8, "FY2019": -5.4, "FY2018": -11.0, "FY2016": -7.5, "FY2015": -7.0, "FY2014": -7.8, "FY2013": -16.2, "FY2012": -10.2, "FY2011": -6.7, "FY2010": -3.1, "FY2009": -0.2}),
    ("DATA", "Net gains/(losses) from derivatives and other financial instruments at fair value through profit or loss", {"FY2025": 12.6, "FY2024": -3.0, "FY2023": 12.6, "FY2022": -5.3, "FY2021": -3.1, "FY2020": -5.2, "FY2019": 3.2, "FY2018": 1.2, "FY2016": -9.7, "FY2015": -9.1, "FY2014": -5.5}),
    ("DATA", "Net gains on disposal of financial assets at fair value through other comprehensive income", {"FY2025": 1.1, "FY2024": 2.0, "FY2023": 2.1, "FY2022": 0.2, "FY2021": 0.7, "FY2020": -0.1, "FY2019": 0.2, "FY2018": 1.2, "FY2016": 3.8, "FY2015": 2.3, "FY2014": 2.9}),
    ("DATA", "Net gains on financial assets at amortised cost", {"FY2024": 0.2}),
    ("DATA", "Other operating income", {"FY2025": 49.2, "FY2024": 38.1, "FY2023": 10.1, "FY2022": 13.6, "FY2021": 8.4, "FY2020": 6.8, "FY2019": 6.6, "FY2018": 9.2, "FY2016": 6.4, "FY2015": 7.6, "FY2014": 7.6, "FY2013": 8.8, "FY2012": 10.4, "FY2011": 8.5, "FY2010": 7.1, "FY2009": 0.9}),
    ("TOTAL", "Total operating income", {"FY2025": 473.4, "FY2024": 462.9, "FY2023": 476.2, "FY2022": 389.8, "FY2021": 323.4, "FY2020": 313.1, "FY2019": 331.8, "FY2018": 468.5, "FY2016": 265.9, "FY2015": 221.6, "FY2014": 166.1, "FY2013": 103.8, "FY2012": 58.8, "FY2011": 42.6, "FY2010": 28.2, "FY2009": 4.1}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Provisions", {"FY2025": -3.0, "FY2024": 1.2, "FY2023": -2.0, "FY2022": -2.1, "FY2021": -1.7, "FY2020": -0.5, "FY2019": -1.2, "FY2018": -1.2, "FY2016": -0.8, "FY2015": -2.3, "FY2014": -3.6, "FY2013": -2.1, "FY2012": -0.5}),
    ("DATA", "Costs in preparation for Aldermore Group PLC initial public offering", {"FY2015": -0.4, "FY2014": -5.9}),
    ("DATA", "Impairment of goodwill", {"FY2016": -4.1}),
    ("DATA", "Impairment of intangibles and goodwill", {"FY2019": -0.7, "FY2018": -14.2}),
    ("DATA", "Transaction costs", {"FY2018": -3.7}),
    ("DATA", "Integration costs", {"FY2019": -4.6, "FY2018": -2.4}),
    ("DATA", "Other expenses and staff costs / other administrative expenses", {"FY2025": -263.8, "FY2024": -265.0, "FY2023": -251.5, "FY2022": -221.9, "FY2021": -172.0, "FY2020": -148.1, "FY2019": -162.9, "FY2018": -206.3, "FY2016": -112.9, "FY2015": -107.4, "FY2014": -91.3, "FY2013": -65.2, "FY2012": -49.4, "FY2011": -40.7, "FY2010": -34.3, "FY2009": -11.9}),
    ("DATA", "Depreciation and amortisation", {"FY2021": -7.3, "FY2020": -6.7, "FY2019": -4.6, "FY2018": -8.4, "FY2016": -5.3, "FY2015": -5.3, "FY2014": -3.9, "FY2013": -4.3, "FY2012": -2.8, "FY2011": -1.9, "FY2010": -1.3, "FY2009": -0.5}),
    ("TOTAL", "Administrative expenses", {"FY2025": -266.8, "FY2024": -263.8, "FY2023": -253.5, "FY2022": -224.0, "FY2021": -173.7, "FY2020": -148.7, "FY2019": -169.4, "FY2018": -227.8, "FY2016": -117.8, "FY2015": -110.1, "FY2014": -100.8, "FY2013": -69.5, "FY2012": -52.2, "FY2011": -42.6, "FY2010": -35.6, "FY2009": -12.4}),
    ("TOTAL", "Operating profit before impairment losses", {"FY2025": 206.6, "FY2024": 199.1, "FY2023": 222.6, "FY2022": 165.8, "FY2021": 142.4, "FY2020": 157.7, "FY2019": 157.8, "FY2018": 232.3, "FY2016": 142.8, "FY2015": 106.2, "FY2014": 61.4, "FY2013": 34.3, "FY2012": 6.6, "FY2011": 0.1, "FY2010": -7.3, "FY2009": -8.3}),
    ("DATA", "Impairment releases/(losses) on loans and advances to customers", {"FY2025": 14.1, "FY2024": 19.1, "FY2023": -51.4, "FY2022": -5.1, "FY2021": -26.7, "FY2020": -65.1, "FY2019": -20.1, "FY2018": -19.5, "FY2016": -15.5, "FY2015": -10.4, "FY2014": -9.6, "FY2013": -9.8, "FY2012": -4.6, "FY2011": -1.0, "FY2010": -1.5, "FY2009": -4.6}),
    ("DATA", "Impairment losses on lease modifications", {"FY2021": 0, "FY2020": -11.0}),
    ("TOTAL", "Profit before taxation", {"FY2025": 220.7, "FY2024": 218.2, "FY2023": 171.2, "FY2022": 160.7, "FY2021": 115.7, "FY2020": 81.6, "FY2019": 137.7, "FY2018": 212.8, "FY2016": 127.3, "FY2015": 95.8, "FY2014": 51.8, "FY2013": 22.4, "FY2012": 1.5, "FY2011": -0.9, "FY2010": -8.8, "FY2009": -12.9}),
    ("DATA", "Taxation", {"FY2025": -57.5, "FY2024": -56.1, "FY2023": -42.0, "FY2022": -42.7, "FY2021": -26.4, "FY2020": -17.4, "FY2019": -35.5, "FY2018": -56.9, "FY2016": -35.0, "FY2015": -15.7, "FY2014": -12.1, "FY2013": 1.0, "FY2012": 0, "FY2011": 0.0, "FY2010": 0, "FY2009": -0.1}),
    ("TOTAL", "Profit after taxation — attributable to equity holders of the Company/Bank", {"FY2025": 163.2, "FY2024": 162.1, "FY2023": 129.2, "FY2022": 118.0, "FY2021": 89.3, "FY2020": 64.2, "FY2019": 102.2, "FY2018": 155.9, "FY2016": 92.3, "FY2015": 80.1, "FY2014": 39.7, "FY2013": 23.4, "FY2012": 1.5, "FY2011": -0.9, "FY2010": -8.8, "FY2009": -13.0}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "FVOCI debt securities: Fair value movements", {"FY2025": -4.6, "FY2024": -3.3, "FY2023": -2.7, "FY2022": -2.2, "FY2021": 10.3, "FY2020": 1.8, "FY2019": -0.2, "FY2018": 0.3, "FY2016": 7.6, "FY2015": -0.9, "FY2014": 3.5}),
    ("DATA", "FVOCI debt securities: Amounts transferred to the income statement", {"FY2025": -1.1, "FY2024": -2.0, "FY2023": -2.1, "FY2022": -0.2, "FY2021": -0.7, "FY2020": -0.5, "FY2019": -0.8, "FY2018": -1.2, "FY2016": -3.8, "FY2015": -2.1, "FY2014": -2.5}),
    ("DATA", "Taxation on other comprehensive income", {"FY2025": 1.4, "FY2024": 1.3, "FY2023": 1.3, "FY2022": 1.0, "FY2021": -2.8, "FY2020": -0.3, "FY2019": 0.3, "FY2018": None, "FY2016": -1.0, "FY2015": 0.6, "FY2014": -0.2}),
    ("TOTAL", "Total other comprehensive (expense)/income", {"FY2025": -4.3, "FY2024": -4.0, "FY2023": -3.6, "FY2022": -1.4, "FY2021": 6.8, "FY2020": 1.0, "FY2019": -0.7, "FY2018": -0.7, "FY2016": 2.8, "FY2015": -2.4, "FY2014": 0.8, "FY2013": 0, "FY2012": 0, "FY2011": 0, "FY2010": 0, "FY2009": 0}),
    ("TOTAL", "Total comprehensive income attributable to equity holders of the Bank", {"FY2025": 158.9, "FY2024": 158.1, "FY2023": 125.7, "FY2022": 116.6, "FY2021": 96.1, "FY2020": 65.2, "FY2019": 101.5, "FY2018": 155.2, "FY2016": 95.1, "FY2015": 77.7, "FY2014": 40.5, "FY2013": 23.4, "FY2012": 1.5, "FY2011": -0.9, "FY2010": -8.8, "FY2009": -13.0}),
    ("SECTION", "FY2017 - no 31 December 2017 reporting date exists. Aldermore changed its accounting reference date and ran an 18-month transition period from 1 January 2017 to 30 June 2018, reported in the FY2018 column. There is no FY2017 edition to open and no FY2017 figure that could be found; the Companies House filing history runs 31 Dec 2016 straight to 30 Jun 2018. Stated explicitly so the column does not read as an unclosed gap", {}),
    ("DATA", "Period covered by this column", {"FY2017": NO_FY2017}),
]

bw.add_income_statement_sheet(
    title="Aldermore Bank PLC — Income Statement and Statement of Comprehensive Income",
    subtitle="Company (Bank solo) basis, £m, year ended 30 June",
    rows=income_statement_rows,
    sources_text=INCOME_STATEMENT_SOURCES,
    first_col_width=78,
    source_height=150,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
EQUITY_CHANGES_SOURCES = (
    "Sources — Aldermore Bank PLC (company solo) Statement of changes in equity from each year's full "
    "statutory accounts filed at Companies House (company no. 00947662), £m:\n"
    f"FY2025 & FY2024: Full accounts made up to 30 June 2025, filed 04 Nov 2025, p.56 — {CH_2025_URL}\n"
    f"FY2023 & FY2022: Full accounts made up to 30 June 2023, filed 27 Oct 2023, p.54 — {CH_2023_URL}\n"
    f"FY2021 & FY2020: Full accounts made up to 30 June 2021, filed 04 Nov 2021, p.60 — {CH_2021_URL}\n"
    f"FY2019 & FY2018 (18-month period ended 30 Jun 2018): Full accounts for the year ended 30 June 2019, "
    f"filed 22 Nov 2019, p.52 — {CH_2019_URL}\n"
    f"FY2016 & FY2015: Full accounts for the year ended 31 December 2016, filed 11 May 2017, p.29 — {CH_2016_URL}\n"
    f"FY2014: Full accounts for the year ended 31 December 2015, filed 23 May 2016, p.79 (FY2014 comparative) — {CH_2015_URL}\n"
    "Chronological roll-forward, oldest to newest. 'As at 30 June 2021' shows £987.2m in the FY2021 accounts' "
    "own Statement of Changes in Equity vs £987.1m on the face of the FY2021 Statement of Financial Position "
    "— a £0.1m rounding difference in the Bank's own disclosures, both transcribed as reported. A similar sub-"
    "£0.1m rounding gap exists between the 'As at 30 June 2020' close (896.2, tying to the FY2020 accounts) and "
    "the 'As at 1 July 2020' opening carried over from the FY2022 accounts' own comparative roll-forward "
    "(FVOCI reserve 1.5 vs 1.4) — both reproduced exactly as each source states them, not reconciled.\n"
    "FY2017 has no standalone 12-month roll-forward: following the Bank's change of accounting reference date "
    "(see YEARS comment above), the roll-forward jumps directly from 'As at 31 December 2016' (year-end under "
    "the old Dec-FYE) to 'As at 1 January 2017' opening a single 18-month movement to 'As at 30 June 2018' — "
    "there is no 31 December 2017 balance in the Bank's own disclosures. The 'Capital contribution / redemption "
    "reserve' column is the same underlying reserve renamed across the Bank's own accounts over time ('Capital "
    "contribution reserve' in FY2014-FY2015 and again in the FY2018 18-month accounts; 'Capital redemption "
    "reserve' in FY2016 and FY2019 onward) — carried as one column for continuity; it is fully run down to nil "
    "by FY2019 and stays at nil (explicitly reported as '-') through FY2025, so is omitted from the FY2021-FY2025 "
    "rows below (shown as 0) exactly as the Bank's own more recent accounts no longer print it as a separate line.\n\n"
    "HD-073 extension (FY2009-FY2013): sourced from the same old-UK-GAAP statutory accounts as the Balance "
    "Sheet and Profit & Loss sheets (see the Balance Sheet sheet's source note for full document/page "
    "references), each year's own 'Reconciliation of movements in shareholders' funds'/'in reserves' note. "
    "FY2009 is a 9-month stub period (1 Apr 2009 - 31 Dec 2009): the Bank's very first roll-forward row, "
    "'As at 1 April 2009', is its true opening position (Share capital £2.5m, Retained earnings £15.4m), not "
    "a restated prior-year close. No Additional Tier 1 capital or FVOCI reserve existed yet in this period "
    "(both are genuinely absent, shown as blank rather than 0); the Capital contribution reserve did not "
    "exist before FY2012 either. The 'As at 31 December 2013' close (£257.4m, old UK GAAP basis) does NOT "
    "tie to the immediately following 'As at 1 January 2014' IFRS-basis opening (£259.4m) — a genuine ~£2.0m "
    "gap from the Bank's UK-GAAP-to-IFRS transition (which, among other things, created the FVOCI reserve "
    "column and restated retained earnings), not a data error. This is a real basis change, left as an "
    "unexplained gap here rather than bridged with a fabricated adjustment row, consistent with how a genuine "
    "reconciling difference elsewhere on this sheet (e.g. any other bank's real transition gaps) is handled.\n"
    "The FY2012 column throughout this sheet is presented on a restated basis: the Bank changed its accounting "
    "policy for IFRIC 21 Levies, which increased 1 January 2012 opening reserves by £662k and FY2012 retained "
    "profit by £707k versus the figures as originally reported in the Bank's own FY2012 accounts — both effects "
    "are included via the 'Prior year adjustment (IFRIC 21 restatement, FY2012)' row below, as disclosed in the "
    "FY2013 accounts' own comparative note (the FY2013 accounts, not the original FY2012 filing, are the source "
    "for the whole FY2012 column, consistent with the rest of this sheet using each year's latest filed figures)."
)

EQUITY_HEADERS = [
    "Share capital", "Share premium account", "Additional Tier 1 capital",
    "Capital contribution / redemption reserve", "FVOCI reserve", "Retained earnings", "Total",
]

equity_changes_rows = [
    ("TOTAL", "As at 1 April 2009 (opens the 9-month stub period to 31 Dec 2009)", (2.5, 0, None, None, None, 15.4, 17.9)),
    ("DATA", "Loss for the period (9 months to 31 Dec 2009)", (None, None, None, None, None, -13.0, -13.0)),
    ("DATA", "Shares issued during the period (FY2009 stub)", (0.8, None, None, None, None, None, 0.8)),
    ("DATA", "Premium on shares issued during the period (FY2009 stub)", (None, 47.4, None, None, None, None, 47.4)),
    ("TOTAL", "As at 31 December 2009", (3.3, 47.4, None, None, None, 2.4, 53.1)),
    ("TOTAL", "As at 1 January 2010", (3.3, 47.4, None, None, None, 2.4, 53.1)),
    ("DATA", "Loss for the year (FY2010)", (None, None, None, None, None, -8.8, -8.8)),
    ("DATA", "Premium on shares issued during the year (FY2010)", (None, 48.3, None, None, None, None, 48.3)),
    ("DATA", "Capital raising costs (FY2010)", (None, -1.0, None, None, None, None, -1.0)),
    ("TOTAL", "As at 31 December 2010", (3.3, 94.7, None, None, None, -6.4, 91.6)),
    ("TOTAL", "As at 1 January 2011", (3.3, 94.7, None, None, None, -6.4, 91.6)),
    ("DATA", "Loss for the year (FY2011)", (None, None, None, None, None, -0.9, -0.9)),
    ("DATA", "Premium on shares issued during the year (FY2011)", (None, 77.9, None, None, None, None, 77.9)),
    ("DATA", "Capital raising costs (FY2011)", (None, -2.5, None, None, None, None, -2.5)),
    ("TOTAL", "As at 31 December 2011", (3.3, 170.1, None, None, None, -7.3, 166.1)),
    ("TOTAL", "As at 1 January 2012", (3.3, 170.1, None, None, None, -7.3, 166.1)),
    ("DATA", "Prior year adjustment (IFRIC 21 restatement, FY2012)", (None, None, None, None, None, 0.7, 0.7)),
    ("TOTAL", "Restated balance as at 1 January 2012", (3.3, 170.1, None, None, None, -6.6, 166.8)),
    ("DATA", "Profit for the year (FY2012)", (None, None, None, None, None, 1.5, 1.5)),
    ("DATA", "Premium on shares issued during the year (FY2012)", (None, 1.7, None, None, None, None, 1.7)),
    ("DATA", "Capital raising costs (FY2012)", (None, 0, None, None, None, None, 0)),
    ("DATA", "Capital contribution (FY2012)", (None, None, None, 2.3, None, None, 2.3)),
    ("TOTAL", "As at 31 December 2012", (3.3, 171.8, None, 2.3, None, -5.2, 172.3)),
    ("TOTAL", "As at 1 January 2013", (3.3, 171.8, None, 2.3, None, -5.2, 172.3)),
    ("DATA", "Profit for the year (FY2013)", (None, None, None, None, None, 23.4, 23.4)),
    ("DATA", "Premium on shares issued during the year (FY2013)", (None, 61.6, None, None, None, None, 61.6)),
    ("DATA", "Capital contribution (FY2013)", (None, None, None, 0.2, None, None, 0.2)),
    ("TOTAL", "As at 31 December 2013 (old UK GAAP basis - see source note for the transition gap to 1 Jan 2014)", (3.3, 233.4, None, 2.5, None, 18.2, 257.4)),
    ("TOTAL", "As at 1 January 2014", (3.3, 233.4, None, 2.5, 0.6, 19.6, 259.4)),
    ("DATA", "Profit after taxation (FY2014)", (None, None, None, None, None, 39.7, 39.7)),
    ("DATA", "Other comprehensive income (FY2014)", (None, None, None, None, 0.8, None, 0.8)),
    ("DATA", "Additional Tier 1 perpetual loan issuance", (None, None, 74.3, None, None, None, 74.3)),
    ("DATA", "Share-based payments (FY2014)", (None, None, None, 0.6, None, None, 0.6)),
    ("TOTAL", "As at 31 December 2014", (3.3, 233.4, 74.3, 3.1, 1.4, 59.3, 374.8)),
    ("DATA", "Profit after taxation (FY2015)", (None, None, None, None, None, 80.1, 80.1)),
    ("DATA", "Other comprehensive loss (FY2015)", (None, None, None, None, -2.4, None, -2.4)),
    ("DATA", "Share issue proceeds — Aldermore Group PLC IPO", (None, 68.6, None, None, None, None, 68.6)),
    ("DATA", "Share issue proceeds — exercise of warrants in Aldermore Group PLC", (None, 5.6, None, -2.2, None, 2.2, 5.6)),
    ("DATA", "Coupon paid on Additional Tier 1 perpetual loan, net of tax relief (FY2015)", (None, None, None, None, None, -2.8, -2.8)),
    ("DATA", "Share-based payments, including tax reflected directly in retained earnings (FY2015)", (None, None, None, 3.4, None, None, 3.4)),
    ("DATA", "Transfer of capital contribution to retained earnings re vested share-based payments", (None, None, None, -0.9, None, 0.9, None)),
    ("TOTAL", "As at 31 December 2015", (3.3, 307.6, 74.3, 3.4, -1.0, 139.7, 527.3)),
    ("DATA", "Total comprehensive income (FY2016)", (None, None, None, None, 2.8, 92.3, 95.1)),
    ("DATA", "Share-based payments, including tax reflected directly in retained earnings (FY2016)", (None, None, None, 3.5, None, 0.1, 3.6)),
    ("DATA", "Coupon paid on contingent convertible securities, net of tax (FY2016)", (None, None, None, None, None, -6.6, -6.6)),
    ("TOTAL", "As at 31 December 2016", (3.3, 307.6, 74.3, 6.9, 1.8, 225.5, 619.4)),
    ("TOTAL", "As at 1 January 2017 (opens the 18-month transition period to 30 Jun 2018)", (3.3, 307.6, 74.3, 6.9, 1.8, 225.5, 619.4)),
    ("DATA", "Profit after taxation (18 months to 30 Jun 2018)", (None, None, None, None, None, 155.9, 155.9)),
    ("DATA", "Other comprehensive loss (18 months to 30 Jun 2018)", (None, None, None, None, -0.7, None, -0.7)),
    ("DATA", "Share-based payments, including tax reflected directly in retained earnings (18mo)", (None, None, None, 4.9, None, 1.4, 6.3)),
    ("DATA", "Coupon paid on contingent convertible securities, net of tax (18mo)", (None, None, None, None, None, -13.3, -13.3)),
    ("DATA", "Transfer of share based payment reserve to retained earnings (18mo)", (None, None, None, -11.8, None, 11.8, None)),
    ("DATA", "Release of Employee Benefit Trust loan (18mo)", (None, None, None, None, None, -0.9, -0.9)),
    ("TOTAL", "As at 30 June 2018", (3.3, 307.6, 74.3, 0, 1.1, 380.4, 766.7)),
    ("DATA", "Adjustment for adoption of IFRS 9", (None, None, None, None, None, -7.8, -7.8)),
    ("DATA", "Adjustment for adoption of IFRS 15", (None, None, None, None, None, -0.2, -0.2)),
    ("TOTAL", "Restated balance as at 1 July 2018", (3.3, 307.6, 74.3, 0, 1.1, 372.4, 758.7)),
    ("DATA", "Profit after taxation (FY2019)", (None, None, None, None, None, 102.2, 102.2)),
    ("DATA", "Other comprehensive loss (FY2019)", (None, None, None, None, -0.7, None, -0.7)),
    ("DATA", "Coupon paid on Additional Tier 1 capital securities, net of tax (FY2019)", (None, None, None, None, None, -7.0, -7.0)),
    ("TOTAL", "As at 30 June 2019", (3.3, 307.6, 74.3, 0, 0.4, 467.6, 853.2)),
    ("DATA", "Profit after taxation (FY2020)", (None, None, None, None, None, 64.2, 64.2)),
    ("DATA", "Other comprehensive income (FY2020)", (None, None, None, None, 1.0, None, 1.0)),
    ("DATA", "Issuance of Additional Tier 1 capital (FY2020)", (None, None, 61.0, None, None, None, 61.0)),
    ("DATA", "Redemption of Additional Tier 1 capital (FY2020)", (None, None, -74.3, None, None, None, -74.3)),
    ("DATA", "Coupon paid on Additional Tier 1 capital securities (FY2020)", (None, None, None, None, None, -8.9, -8.9)),
    ("TOTAL", "As at 30 June 2020", (3.3, 307.5, 61.0, 0, 1.4, 522.9, 896.2)),
    ("TOTAL", "As at 1 July 2020", (3.3, 307.6, 61.0, 0, 1.5, 522.9, 896.2)),
    ("DATA", "Profit after taxation (FY2021)", (None, None, None, None, None, 89.3, 89.3)),
    ("DATA", "Other comprehensive income (FY2021)", (None, None, None, None, 6.8, None, 6.9)),
    ("DATA", "Coupon paid on Additional Tier 1 capital securities (FY2021)", (None, None, None, None, None, -5.2, -5.2)),
    ("TOTAL", "As at 30 June 2021", (3.3, 307.6, 61.0, 0, 8.3, 607.0, 987.2)),
    ("DATA", "Profit after taxation (FY2022)", (None, None, None, None, None, 118.0, 118.0)),
    ("DATA", "Other comprehensive loss (FY2022)", (None, None, None, None, -1.4, None, -1.4)),
    ("DATA", "Coupon paid on Additional Tier 1 capital securities (FY2022)", (None, None, None, None, None, -5.2, -5.2)),
    ("TOTAL", "As at 30 June 2022", (3.3, 307.5, 61.0, 0, 6.9, 719.8, 1098.5)),
    ("DATA", "Profit after taxation (FY2023)", (None, None, None, None, None, 129.2, 129.2)),
    ("DATA", "Other comprehensive loss (FY2023)", (None, None, None, None, -3.6, None, -3.6)),
    ("DATA", "Coupon paid on Additional Tier 1 capital securities (FY2023)", (None, None, None, None, None, -5.2, -5.2)),
    ("TOTAL", "As at 30 June 2023", (3.3, 307.5, 61.0, 0, 3.3, 843.9, 1219.0)),
    ("DATA", "Profit after taxation (FY2024)", (None, None, None, None, None, 162.1, 162.1)),
    ("DATA", "Other comprehensive loss (FY2024)", (None, None, None, None, -4.0, None, -4.0)),
    ("DATA", "Coupon paid on Additional Tier 1 capital securities (FY2024)", (None, None, None, None, None, -5.3, -5.3)),
    ("TOTAL", "As at 30 June 2024", (3.3, 307.5, 61.0, 0, -0.7, 1000.7, 1371.8)),
    ("DATA", "Profit after taxation (FY2025)", (None, None, None, None, None, 163.2, 163.2)),
    ("DATA", "Other comprehensive loss (FY2025)", (None, None, None, None, -4.3, None, -4.3)),
    ("DATA", "Redemption of Additional Tier 1 capital", (None, None, -61.0, None, None, None, -61.0)),
    ("DATA", "Issuance of Additional Tier 1 capital", (None, None, 50.0, None, None, None, 50.0)),
    ("DATA", "Coupon paid on Additional Tier 1 capital securities (FY2025)", (None, None, None, None, None, -5.1, -5.1)),
    ("TOTAL", "As at 30 June 2025", (3.3, 307.5, 50.0, 0, -5.0, 1158.8, 1514.6)),
]

bw.add_equity_changes_sheet(
    title="Aldermore Bank PLC — Statement of Changes in Equity",
    subtitle="Company (Bank solo) basis, £m, chronological FY2009-FY2025 (FY2017 has no standalone period — see source notes)",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQUITY_CHANGES_SOURCES,
    first_col_width=54,
    source_height=150,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Reconciliation of profit before tax to net cash flows from operating activities", {}),
    ("DATA", "Profit before taxation", {"FY2025": 220.7, "FY2024": 218.2, "FY2023": 171.2, "FY2022": 160.7, "FY2021": 115.7, "FY2020": 81.6, "FY2019": 137.7, "FY2018": 212.8, "FY2016": 127.3, "FY2015": 95.8, "FY2014": 51.8}),
    ("DATA", "Adjustments for non-cash items and other adjustments included within the income statement", {"FY2025": -223.6, "FY2024": -188.9, "FY2023": -49.2, "FY2022": -22.3, "FY2021": 17.0, "FY2020": 58.1, "FY2019": 14.7, "FY2018": 26.4, "FY2016": 7.4, "FY2015": 4.3, "FY2014": -12.7}),
    ("DATA", "Change/(increase) in operating assets", {"FY2025": -1145.9, "FY2024": -439.9, "FY2023": -519.2, "FY2022": -389.0, "FY2021": 265.0, "FY2020": -584.8, "FY2019": -1327.7, "FY2018": -1528.8, "FY2016": -1327.1, "FY2015": -1310.3, "FY2014": -1499.8}),
    ("DATA", "Change/increase in operating liabilities", {"FY2025": 283.3, "FY2024": 992.8, "FY2023": 1539.6, "FY2022": 1526.0, "FY2021": 498.4, "FY2020": 2515.5, "FY2019": 1490.7, "FY2018": 1967.0, "FY2016": 1223.9, "FY2015": 1279.7, "FY2014": 1264.7}),
    ("DATA", "Interest received on intercompany loan (operating basis, FY2024-FY2025)", {"FY2025": 164.5, "FY2024": 135.8}),
    ("DATA", "Interest paid on intercompany loan (operating basis, FY2024-FY2025)", {"FY2025": -53.9, "FY2024": -38.0}),
    ("DATA", "Interest paid on subordinated notes (operating basis, FY2024-FY2025)", {"FY2025": -7.9, "FY2024": -6.4}),
    ("DATA", "Interest received on debt securities (operating basis, FY2024-FY2025)", {"FY2025": 95.2, "FY2024": 86.3}),
    ("DATA", "Proceeds from disposal of non-current assets held for sale (operating basis, FY2024-FY2025)", {"FY2025": 0, "FY2024": 32.8}),
    ("DATA", "Income tax paid", {"FY2025": -57.4, "FY2024": -62.6, "FY2023": -33.9, "FY2022": -59.7, "FY2021": -12.0, "FY2020": -39.7, "FY2019": -18.7, "FY2018": -44.8, "FY2016": -31.5, "FY2015": -20.2, "FY2014": -9.7}),
    ("TOTAL", "Net cash flows (used in)/generated from operating activities", {"FY2025": -725.0, "FY2024": 730.1, "FY2023": 1108.5, "FY2022": 1215.7, "FY2021": 884.1, "FY2020": 2030.7, "FY2019": 296.7, "FY2018": 632.6, "FY2016": 0, "FY2015": 49.3, "FY2014": -205.7}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of debt securities", {"FY2025": -1618.2, "FY2024": -1184.9, "FY2023": -358.2, "FY2022": -723.4, "FY2021": -444.6, "FY2020": -1085.2, "FY2019": -810.7, "FY2018": -703.7, "FY2016": -298.4, "FY2015": -414.0, "FY2014": -564.6}),
    ("DATA", "Proceeds from sale and/or maturity of debt securities", {"FY2025": 1278.3, "FY2024": 421.2, "FY2023": 299.3, "FY2022": 159.6, "FY2021": 333.1, "FY2020": 281.4, "FY2019": 386.5, "FY2018": 316.0, "FY2016": 161.7, "FY2015": 279.0, "FY2014": 346.2}),
    ("DATA", "Capital repayments of debt securities", {"FY2025": 81.4, "FY2024": 367.2, "FY2023": 351.3, "FY2022": 223.3, "FY2021": 61.4, "FY2020": 89.7, "FY2019": 53.8, "FY2018": 250.8, "FY2016": 87.5, "FY2015": 32.9, "FY2014": 48.2}),
    ("DATA", "Interest received on debt securities (investing basis, FY2021-FY2023)", {"FY2023": 15.2, "FY2022": 7.6, "FY2021": 6.8}),
    ("DATA", "Interest received on debt securities (investing basis, FY2014-FY2020)", {"FY2020": 8.5, "FY2019": 15.0, "FY2018": 15.5, "FY2016": 13.1, "FY2015": 10.5, "FY2014": 11.2}),
    ("DATA", "Purchase of property, plant and equipment and intangible assets", {"FY2025": -1.0, "FY2024": -5.1, "FY2023": -1.0, "FY2022": -1.9, "FY2021": -11.7, "FY2020": -6.0, "FY2019": -2.3, "FY2018": -11.6, "FY2016": -11.2, "FY2015": -7.3, "FY2014": -5.4}),
    ("TOTAL", "Net cash flows (used in)/generated from investing activities", {"FY2025": -259.5, "FY2024": -401.6, "FY2023": 306.5, "FY2022": -334.8, "FY2021": -55.0, "FY2020": -711.6, "FY2019": -357.7, "FY2018": -133.0, "FY2016": -47.3, "FY2015": -98.9, "FY2014": -164.4}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Repayment of subordinated debt", {"FY2024": -100.0, "FY2022": -60.0, "FY2018": -40.0}),
    ("DATA", "Proceeds from issue of subordinated debt", {"FY2024": 100.0, "FY2019": 100.0, "FY2016": 60.0}),
    ("DATA", "Issue costs of subordinated debt", {"FY2016": -0.6}),
    ("DATA", "Redemption of Additional Tier 1 Capital", {"FY2025": -61.0, "FY2020": -74.3}),
    ("DATA", "Issuance of Additional Tier 1 Capital", {"FY2025": 50.0, "FY2020": 61.0}),
    ("DATA", "Proceeds from Additional Tier 1 perpetual loan", {"FY2014": 74.3}),
    ("DATA", "Capital repayments on debt securities issued", {"FY2023": 0.4}),
    ("DATA", "Proceeds from issue of shares — Aldermore Group PLC initial public offering", {"FY2015": 68.6}),
    ("DATA", "Proceeds from shares issued — exercise of warrants in Aldermore Group PLC", {"FY2015": 5.6}),
    ("DATA", "Amounts paid on new intercompany loan", {"FY2023": -394.3, "FY2022": -694.4, "FY2021": -686.2, "FY2020": -1222.3, "FY2019": -369.2, "FY2018": -20.4}),
    ("DATA", "Interest received on intercompany loan (financing basis, FY2021-FY2023)", {"FY2023": 68.0, "FY2022": 30.3, "FY2021": 20.1}),
    ("DATA", "Interest received on intercompany loan (financing basis, FY2019-FY2020)", {"FY2020": 13.6, "FY2019": 0.1}),
    ("DATA", "Interest paid on intercompany deposit (FY2019-FY2020)", {"FY2020": -0.2, "FY2019": -0.1}),
    ("DATA", "Deposit placed by related Group companies", {"FY2021": -12.3, "FY2020": -37.4, "FY2019": 311.3}),
    ("DATA", "Coupons paid on Additional Tier 1 capital", {"FY2025": -5.1, "FY2024": -5.3, "FY2023": -5.2, "FY2022": -5.2, "FY2021": -5.2, "FY2020": -8.9, "FY2019": -8.9, "FY2018": -17.8, "FY2016": -8.9, "FY2015": -3.5}),
    ("DATA", "Interest paid on subordinated notes (financing basis)", {"FY2022": -7.4, "FY2021": -9.9, "FY2020": -9.9, "FY2019": -7.5, "FY2018": -10.2, "FY2016": -5.2, "FY2015": -5.2, "FY2014": -5.2}),
    ("DATA", "Repayment of lease liabilities - principal", {"FY2025": -2.3, "FY2024": -3.0, "FY2022": -2.8, "FY2021": -4.0, "FY2020": -1.9}),
    ("DATA", "Interest paid on lease liabilities", {"FY2023": -0.1, "FY2022": -0.1, "FY2021": -0.2, "FY2020": -0.2}),
    ("TOTAL", "Net cash generated/(used in) financing activities", {"FY2025": -18.4, "FY2024": -8.3, "FY2023": -331.2, "FY2022": -739.7, "FY2021": -697.7, "FY2020": -1280.5, "FY2019": 25.7, "FY2018": -88.4, "FY2016": 45.3, "FY2015": 65.5, "FY2014": 69.1}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -1002.9, "FY2024": 320.2, "FY2023": 1083.8, "FY2022": 141.2, "FY2021": 131.4, "FY2020": 38.6, "FY2019": -35.3, "FY2018": 411.2, "FY2016": -2.0, "FY2015": 15.9, "FY2014": -301.0}),
    ("DATA", "Cash and cash equivalents at start of the period", {"FY2025": 2219.6, "FY2024": 1899.4, "FY2023": 815.1, "FY2022": 674.0, "FY2021": 542.6, "FY2020": 504.0, "FY2019": 539.3, "FY2018": 128.1, "FY2016": 130.1, "FY2015": 114.2, "FY2014": 415.2}),
    ("TOTAL", "Cash and cash equivalents at end of the period", {"FY2025": 1216.7, "FY2024": 2219.6, "FY2023": 1899.4, "FY2022": 815.2, "FY2021": 674.0, "FY2020": 542.6, "FY2019": 504.0, "FY2018": 539.3, "FY2016": 128.1, "FY2015": 130.1, "FY2014": 114.2}),
    ("SECTION", "FY2017 - no 31 December 2017 reporting date exists. Aldermore changed its accounting reference date and ran an 18-month transition period from 1 January 2017 to 30 June 2018, reported in the FY2018 column. There is no FY2017 edition to open and no FY2017 figure that could be found; the Companies House filing history runs 31 Dec 2016 straight to 30 Jun 2018. Stated explicitly so the column does not read as an unclosed gap", {}),
    ("DATA", "Period covered by this column", {"FY2017": NO_FY2017}),
]

bw.add_cash_flow_sheet(
    title="Aldermore Bank PLC — Statement of Cash Flows",
    subtitle="Company (Bank solo) basis, £m, year ended 30 June",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=72,
    source_height=140,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality / Credit Risk Disclosures
# ---------------------------------------------------------------

ASSET_QUALITY_PRESENTATION_NOTE = (
    "PRESENTATION NOTE: figures are from each year's own full statutory accounts' 'Analysis of gross loans "
    "and advances' and 'Analysis of loss allowances' notes (IFRS 9 stage roll-forward tables), Bank solo "
    "basis. 'By product' figures (Business Finance / Property Finance) use the Bank's internal risk-category "
    "disclosure (excludes Property Development, which is separately disclosed only for irrevocable "
    "commitments, not drawn balances) and are only available at this granularity for FY2025/FY2024 in the "
    "documents reviewed; FY2023/FY2022/FY2021 are left blank for the by-product split rather than estimated. "
    "Stage totals (gross and ECL allowance) are available and tie out for all 5 years. FY2024's stage-total "
    "gross loans (11,549.3) differs by £0.1m from the FY2024 Balance Sheet's own 'Loans and advances to "
    "customers' figure (11,416.3 net + 133.0 allowance = 11,549.3) — consistent; both are transcribed as "
    "disclosed.\n\n"
    "HD-047 extension (FY2014-FY2020): IFRS 9 (the source of the Stage 1/2/3 framework above) only took "
    "effect for the Bank from 1 July 2018, so FY2014-FY2018 report credit quality on the older IAS 39 "
    "'individually impaired vs collectively assessed' basis instead, in the separate section below. The two "
    "bases are NOT mechanically comparable (different recognition trigger, and no forward-looking ECL overlay "
    "under IAS 39), so they are kept in separate sections and never merged into one series.\n\n"
    "GAP CLOSURE 2026-09-18 — the four interior blanks FY2016, FY2018, FY2019 and FY2020 are now FILLED. A "
    "previous session left them blank and recorded the reason as 'the Companies House filings for these years "
    "are scanned images with no text layer, so locating and transcribing note-level tables requires page-by-"
    "page visual review beyond this session's budget'. That was a statement about the effort available, not "
    "about the documents: all four filings were retrieved from Companies House, OCR'd at 200-300 dpi with "
    "ocrmypdf --force-ocr, and every figure below was then confirmed against the rendered page image before "
    "being transcribed. The OCR step is not optional and the visual check is not ceremony — FY2016's Asset "
    "Finance balance OCR'd as 1,873.4 and the page image reads 1,573.4; only 1,573.4 foots to the printed "
    "segment total of 7,477.3.\n\n"
    "SEGMENT TABLE IS NET, NOT GROSS. The 'by product' section was previously headed 'Gross loans and "
    "advances to customers, by product'. It is not gross: the Bank's own 'Credit concentration by segment' "
    "table is struck after impairment allowances. FY2016 proves it arithmetically — gross loans 7,504.7 less "
    "the 27.4 total allowance is 7,477.3, exactly the printed segment total — and FY2018 ties the same way "
    "(9,015.7 - 25.2 = 8,990.5). The section label has been corrected accordingly. The FY2015/FY2014 rows "
    "were already on this net basis and are unchanged in value; only the label they sit under is now "
    "accurate.\n\n"
    "FY2017 IS NOT A GAP. Aldermore changed its accounting reference date, running an 18-month transition "
    "period from 1 January 2017 to 30 June 2018. No 31 December 2017 reporting date exists, so there is no "
    "FY2017 edition to open and no FY2017 figure that could ever be found; the Companies House filing history "
    "runs 31 Dec 2016 straight to 30 Jun 2018. That year is marked with an explicit statement rather than "
    "left blank, because a blank would read as an unclosed gap.\n\n"
    "FY2020/FY2019 UNDRAWN-FACILITY MEMO ROWS. Those two editions' stage tables carry an 'undrawn loan "
    "facilities' column alongside drawn balances. It is reproduced as a memo row and deliberately excluded "
    "from the totals and from every ratio, so the stage series stays on one definition across all seven "
    "years. Two printed oddities in those tables are transcribed as printed and flagged, not corrected: the "
    "FY2019 edition prints a 10.0% coverage ratio against undrawn facilities where 0.8/687.5 is 0.1%, and the "
    "FY2020 Bank-only accounts head their coverage table 'Group impairment coverage ratio' although its 30 "
    "June 2019 comparative column reproduces the FY2019 Bank accounts' 'Bank impairment coverage ratio' "
    "figures exactly — an apparent heading error in the Bank's own document."
)

ASSET_QUALITY_SOURCES = (
    "Sources — Aldermore Bank PLC (company solo) 'Analysis of gross loans and advances' and 'Analysis of "
    "loss allowances' notes, £m:\n"
    f"FY2025 & FY2024 (by product, Business/Property Finance split): Full accounts made up to 30 June 2025, "
    f"filed 04 Nov 2025, p.24-26 (Credit quality and performance of loans) — {CH_2025_URL}\n"
    f"FY2025 & FY2024 (by IFRS 9 stage, gross and allowance): Full accounts made up to 30 June 2025, filed "
    f"04 Nov 2025, p.84-86 (Note 14, Analysis of gross loans and advances / Analysis of loss allowances) — {CH_2025_URL}\n"
    f"FY2023 & FY2022 (by IFRS 9 stage, gross and allowance): Full accounts made up to 30 June 2023, filed "
    f"27 Oct 2023, p.84 (Note 13, Analysis of gross loans and advances / Analysis of loss allowances) — {CH_2023_URL}\n"
    f"FY2021 (by IFRS 9 stage, gross and allowance): Full accounts made up to 30 June 2021, filed 04 Nov "
    f"2021, p.90-91 (Note 18, Analysis of gross loans and advances / Analysis of loss allowances) — {CH_2021_URL}\n"
    f"FY2020 (by IFRS 9 stage, gross and allowance): Full accounts made up to 30 June 2020, printed p.39 "
    f"(Analysis of gross loans and advances / loss allowances by stage) — {CH_2020_URL}\n"
    f"FY2020 (net lending by segment): same filing, printed p.35 (Credit concentration by segment) — {CH_2020_URL}\n"
    f"FY2019 (by IFRS 9 stage, gross and allowance): Full accounts made up to 30 June 2019, printed p.30 "
    f"(Analysis of gross loans and advances / loss allowances by stage) — {CH_2019_URL}\n"
    f"FY2019 (net lending by segment): same filing, printed p.26 (Credit concentration by segment) — {CH_2019_URL}\n"
    f"FY2018 (impaired loans and coverage, IAS 39 basis): Full accounts for the 18-month period ended 30 June "
    f"2018, printed p.92 (Impaired loan analysis / Impairment coverage ratio) — {CH_2018_URL}\n"
    f"FY2018 (net lending by segment): same filing, printed p.87 (Credit concentration by segment) — {CH_2018_URL}\n"
    f"FY2016 (impaired loans and coverage, IAS 39 basis): Full accounts for the year ended 31 December 2016, "
    f"printed p.79 (Impaired loan analysis / Impairment coverage ratio) — {CH_2016_URL}\n"
    f"FY2016 (net lending by segment): same filing, printed p.82 (Credit concentration by segment) — {CH_2016_URL}\n"
    f"FY2015 & FY2014 (by segment; impaired loans and coverage, IAS 39 basis): Full accounts for the year "
    f"ended 31 December 2015, filed 23 May 2016, p.55-58 (Risk Management — Impaired loan analysis, "
    f"Impairment coverage ratio, Credit concentration by product) — {CH_2015_URL}\n"
    f"FY2017: no such reporting date exists — see the presentation note below.\n\n"
    + ASSET_QUALITY_PRESENTATION_NOTE
)

asset_quality_rows = [
    ("SECTION", "Gross loans and advances to customers, by product (excl. Property Development commitments)", {}),
    ("DATA", "Business Finance", {"FY2025": 3903.8, "FY2024": 3716.7}),
    ("DATA", "Property Finance", {"FY2025": 8728.4, "FY2024": 7832.5}),
    ("TOTAL", "Total gross loans and advances (by product)", {"FY2025": 12632.2, "FY2024": 11549.2}),
    ("SECTION", "Gross loans and advances to customers, by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (performing)", {"FY2025": 11395.2, "FY2024": 10466.4, "FY2023": 10211.2, "FY2022": 9591.1, "FY2021": 9209.1, "FY2020": 9249.0, "FY2019": 9068.5}),
    ("DATA", "Stage 2 (underperforming)", {"FY2025": 814.8, "FY2024": 716.4, "FY2023": 664.9, "FY2022": 1026.0, "FY2021": 956.6, "FY2020": 1234.1, "FY2019": 1082.6}),
    ("DATA", "Stage 3 (credit-impaired)", {"FY2025": 422.2, "FY2024": 366.4, "FY2023": 287.3, "FY2022": 277.1, "FY2021": 343.9, "FY2020": 224.0, "FY2019": 128.6}),
    ("TOTAL", "Total gross loans and advances (by stage)", {"FY2025": 12632.2, "FY2024": 11549.3, "FY2023": 11163.4, "FY2022": 10894.2, "FY2021": 10509.6, "FY2020": 10707.1, "FY2019": 10279.7}),
    ("DATA", "Memo: undrawn loan facilities, gross carrying amount (FY2020/FY2019 source table only — NOT included in the total above)", {"FY2020": 301.7, "FY2019": 687.5}),
    ("SECTION", "Allowance for impairment losses, by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (performing)", {"FY2025": -34.2, "FY2024": -50.2, "FY2023": -91.4, "FY2022": -48.3, "FY2021": -32.8, "FY2020": -33.7, "FY2019": -16.8}),
    ("DATA", "Stage 2 (underperforming)", {"FY2025": -22.6, "FY2024": -25.6, "FY2023": -25.2, "FY2022": -19.8, "FY2021": -24.1, "FY2020": -29.6, "FY2019": -8.8}),
    ("DATA", "Stage 3 (credit-impaired)", {"FY2025": -52.0, "FY2024": -57.2, "FY2023": -48.0, "FY2022": -48.7, "FY2021": -59.1, "FY2020": -41.6, "FY2019": -23.8}),
    ("TOTAL", "Total allowance for impairment losses", {"FY2025": -108.8, "FY2024": -133.0, "FY2023": -164.6, "FY2022": -116.8, "FY2021": -116.0, "FY2020": -104.9, "FY2019": -49.4}),
    ("DATA", "Memo: provision against undrawn loan facilities (FY2020/FY2019 source table only — NOT included in the total above)", {"FY2020": -0.6, "FY2019": -0.8}),
    ("SECTION", "Asset quality ratios", {}),
    ("DATA", "ECL coverage ratio (Total allowance / Total gross loans)", {"FY2025": "0.86%", "FY2024": "1.15%", "FY2023": "1.47%", "FY2022": "1.07%", "FY2021": "1.10%", "FY2020": "0.98%", "FY2019": "0.48%"}),
    ("DATA", "Stage 3 (NPL) ratio (Stage 3 gross loans / Total gross loans)", {"FY2025": "3.34%", "FY2024": "3.17%", "FY2023": "2.57%", "FY2022": "2.54%", "FY2021": "3.27%", "FY2020": "2.09%", "FY2019": "1.25%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 allowance / Stage 3 gross loans)", {"FY2025": "12.32%", "FY2024": "15.61%", "FY2023": "16.71%", "FY2022": "17.58%", "FY2021": "17.18%", "FY2020": "18.57%", "FY2019": "18.51%"}),
    ("SECTION", "Net lending to customers, by product — the Bank's own 'Credit concentration by segment' table (IAS 39 basis to FY2018, IFRS 9 thereafter). NET of impairment allowances, NOT gross: FY2016 7,477.3 = gross 7,504.7 less the 27.4 allowance, and every other year ties the same way", {}),
    ("DATA", "Asset Finance", {"FY2020": 1857.9, "FY2019": 2017.7, "FY2018": 1841.7, "FY2016": 1573.4, "FY2015": 1346.7, "FY2014": 1044.3}),
    ("DATA", "Invoice Finance", {"FY2020": 278.7, "FY2019": 400.4, "FY2018": 265.2, "FY2016": 154.1, "FY2015": 160.8, "FY2014": 180.6}),
    ("DATA", "SME Commercial Mortgages", {"FY2020": 1139.1, "FY2019": 1020.6, "FY2018": 965.9, "FY2016": 929.9, "FY2015": 829.2, "FY2014": 552.4}),
    ("DATA", "Buy-to-Let", {"FY2020": 5246.9, "FY2019": 5043.7, "FY2018": 4436.8, "FY2016": 3326.0, "FY2015": 2417.9, "FY2014": 2044.1}),
    ("DATA", "Residential Mortgages", {"FY2020": 2079.6, "FY2019": 1747.9, "FY2018": 1480.9, "FY2016": 1493.9, "FY2015": 1390.2, "FY2014": 979.7}),
    ("TOTAL", "Total net lending to customers (by product)", {"FY2020": 10602.2, "FY2019": 10230.3, "FY2018": 8990.5, "FY2016": 7477.3, "FY2015": 6144.8, "FY2014": 4801.1}),
    ("SECTION", "Impaired loans and coverage (IAS 39 basis, pre-IFRS 9 — the Bank adopted IFRS 9 on 1 July 2018, so this basis runs to the 30 June 2018 period end and stops)", {}),
    ("DATA", "Gross loans and advances to customers", {"FY2018": 9015.7, "FY2016": 7504.7}),
    ("DATA", "Individually impaired loans (all products)", {"FY2018": 33.9, "FY2016": 35.6, "FY2015": 22.8, "FY2014": 20.8}),
    ("SECTION", "Impairment allowance components (IAS 39 basis)", {}),
    ("DATA", "Allowance for losses — individual provisions", {"FY2018": -7.8, "FY2016": -14.3, "FY2015": -10.2, "FY2014": -14.0}),
    ("DATA", "Allowance for losses — collective provisions", {"FY2018": -17.4, "FY2016": -13.1}),
    ("TOTAL", "Total impairment allowance (individual + collective)", {"FY2018": -25.2, "FY2016": -27.4}),
    ("DATA", "Individually impaired loans as a % of gross loans and advances", {"FY2018": "0.38%", "FY2016": "0.47%", "FY2015": "0.37%", "FY2014": "0.43%"}),
    ("DATA", "Coverage ratio (individual provisions / individually impaired loans)", {"FY2018": "23.09%", "FY2016": "40.17%", "FY2015": "44.74%", "FY2014": "67.40%"}),
    ("SECTION", "FY2017 — no 31 December 2017 reporting date exists (18-month transition period 1 Jan 2017 to 30 Jun 2018, reported in the FY2018 column)", {}),
    ("DATA", "Credit quality disclosures", {"FY2017": NO_FY2017}),
]

bw.add_asset_quality_sheet(
    title="Aldermore Bank PLC — Asset Quality / Credit Risk Disclosures",
    subtitle="Company (Bank solo) basis, £m",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=68,
    source_height=170,
    years=PILLAR3_YEARS,
)

# ---------------------------------------------------------------
# Sheet: KM1 Key Metrics (KM1-003)
# ---------------------------------------------------------------
# ENTITY: every column here is ALDERMORE BANK PLC ('Bank'), matching the rest of this workbook.
# Each edition prints the SAME rows twice - once for Aldermore Group PLC ('Group') and once for
# the Bank - so the entity-basis rule applies INSIDE a single table. FY2026 is six columns
# (Group a/b/c then Bank a/b/c over 30-Jun-26, 31-Dec-25, 30-Jun-25); FY2022-FY2025 are four
# (Group current, Group prior, Bank current, Bank prior). Taking the leftmost column because it
# comes first would silently put Group figures into a Bank series.
#
# TEMPLATE DRIFT WITHIN ONE BANK: only the FY2026 edition prints the template's row NUMBERS
# ("1", "UK 7a", "UK 16b"). The FY2022-FY2025 editions print the identical row set and labels
# with NO numbering at all. The numbers below are Aldermore's own, from FY2026, carried across
# the row because it is the same template row - not invented for the earlier years.
#
# EACH YEAR COMES FROM ITS OWN EDITION (map rule 1), never a later edition's comparative. That
# matters twice here:
#   * FY2023 uses the FY2023 edition, which this project had never cited (see P3_2023_URL).
#   * FY2025 leverage exposure is 15,674.3 in the FY2025 edition and RESTATED to 15,526.0 in the
#     FY2026 edition's comparative. The FY2025 figure stands here and the restatement is flagged
#     rather than reconciled. Every other FY2026 comparative agrees with the FY2025 edition.
km1_rows = [
    ("SECTION", "Available own funds (amounts)", {}),
    ("DATA", "1  Common Equity Tier 1 (CET1) capital (£m)",
     {"FY2026": 1450.9, "FY2025": 1337.8, "FY2024": 1321.5, "FY2023": 1203.8, "FY2022": 1065.9}),
    ("DATA", "2  Tier 1 capital (£m)",
     {"FY2026": 1500.9, "FY2025": 1387.8, "FY2024": 1382.5, "FY2023": 1264.8, "FY2022": 1126.6}),
    ("DATA", "3  Total capital (£m)",
     {"FY2026": 1800.9, "FY2025": 1487.8, "FY2024": 1482.5, "FY2023": 1364.8, "FY2022": 1226.6}),
    ("SECTION", "Risk-weighted exposure amounts", {}),
    ("DATA", "4  Total risk-weighted exposure amount (£m)",
     {"FY2026": 8203.7, "FY2025": 7271.6, "FY2024": 6875.6, "FY2023": 6504.9, "FY2022": 6260.1}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "5  Common Equity Tier 1 ratio (%)",
     {"FY2026": "17.7%", "FY2025": "18.4%", "FY2024": "19.2%", "FY2023": "18.5%", "FY2022": "17.0%"}),
    ("DATA", "6  Tier 1 ratio (%)",
     {"FY2026": "18.3%", "FY2025": "19.1%", "FY2024": "20.1%", "FY2023": "19.4%", "FY2022": "18.0%"}),
    ("DATA", "7  Total capital ratio (%)",
     {"FY2026": "22.0%", "FY2025": "20.5%", "FY2024": "21.6%", "FY2023": "21.0%", "FY2022": "19.6%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "UK 7a  Additional CET1 SREP requirements (%)",
     {"FY2026": "0.7%", "FY2025": "1.2%", "FY2024": "1.2%", "FY2023": "1.2%", "FY2022": "1.2%"}),
    ("DATA", "UK 7b  Additional AT1 SREP requirements (%)",
     {"FY2026": "0.2%", "FY2025": "0.4%", "FY2024": "0.4%", "FY2023": "0.4%", "FY2022": "0.4%"}),
    ("DATA", "UK 7c  Additional T2 SREP requirements (%)",
     {"FY2026": "0.4%", "FY2025": "0.5%", "FY2024": "0.5%", "FY2023": "0.5%", "FY2022": "0.5%"}),
    ("DATA", "UK 7d  Total SREP own funds requirements (%)",
     {"FY2026": "9.3%", "FY2025": "10.1%", "FY2024": "10.1%", "FY2023": "10.1%", "FY2022": "2.1%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "8  Capital conservation buffer (%)",
     {"FY2026": "2.5%", "FY2025": "2.5%", "FY2024": "2.5%", "FY2023": "2.5%", "FY2022": "2.5%"}),
    ("DATA", "9  Institution specific countercyclical capital buffer (%)",
     {"FY2026": "2.0%", "FY2025": "2.0%", "FY2024": "2.0%", "FY2023": "1.0%", "FY2022": "0.0%"}),
    ("DATA", "11  Combined buffer requirement (%)",
     {"FY2026": "4.5%", "FY2025": "4.5%", "FY2024": "4.5%", "FY2023": "3.5%", "FY2022": "2.5%"}),
    ("DATA", "UK 11a  Overall capital requirements (%)",
     {"FY2026": "13.8%", "FY2025": "14.6%", "FY2024": "14.6%", "FY2023": "13.6%", "FY2022": "12.6%"}),
    ("DATA", "12  CET1 available after meeting the total SREP own funds requirements (%)",
     {"FY2026": "12.5%", "FY2025": "12.8%", "FY2024": "12.8%", "FY2023": "12.8%", "FY2022": "7.0%"}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "13  Total exposure measure excluding claims on central banks (£m)",
     {"FY2026": 16715.1, "FY2025": 15674.3, "FY2024": 14337.2, "FY2023": 13609.6, "FY2022": 13850.3}),
    ("DATA", "14  Leverage ratio excluding claims on central banks (%)",
     {"FY2026": "9.0%", "FY2025": "8.9%", "FY2024": "9.6%", "FY2023": "9.3%", "FY2022": "8.1%"}),
    ("SECTION", "Liquidity Coverage Ratio", {}),
    ("DATA", "15  Total high-quality liquid assets (HQLA) (weighted value - average) (£m)",
     {"FY2026": 3725.9, "FY2025": 3723.1, "FY2024": 4208.6, "FY2023": 3280.6, "FY2022": 2838.5}),
    ("DATA", "UK 16a  Cash outflows - total weighted value (£m)",
     {"FY2026": 2554.3, "FY2025": 2194.3, "FY2024": 2206.4, "FY2023": 1951.0, "FY2022": 1012.1}),
    ("DATA", "UK 16b  Cash inflows - total weighted value (£m)",
     {"FY2026": 291.2, "FY2025": 226.0, "FY2024": 247.0, "FY2023": 264.6, "FY2022": 239.5}),
    ("DATA", "16  Total net cash outflows (adjusted value) (£m)",
     {"FY2026": 2263.1, "FY2025": 1968.3, "FY2024": 1959.4, "FY2023": 1686.4, "FY2022": 772.6}),
    ("DATA", "17  Liquidity coverage ratio (%)",
     {"FY2026": "164.6%", "FY2025": "189.2%", "FY2024": "214.8%", "FY2023": "194.5%", "FY2022": "367.4%"}),
    ("SECTION", "Net Stable Funding Ratio", {}),
    ("DATA", "18  Total available stable funding (£m)",
     {"FY2026": 16701.9, "FY2025": 15972.4, "FY2024": 16133.4, "FY2023": 15490.2, "FY2022": 15667.6}),
    ("DATA", "19  Total required stable funding (£m)",
     {"FY2026": 13318.4, "FY2025": 12166.9, "FY2024": 11778.0, "FY2023": 12161.3, "FY2022": 12169.6}),
    ("DATA", "20  NSFR ratio (%)",
     {"FY2026": "125.4%", "FY2025": "131.3%", "FY2024": "137.0%", "FY2023": "127.4%", "FY2022": "128.7%"}),
]

KM1_SOURCES = (
    "Sources — Aldermore Bank PLC ('Bank') columns of the key-metrics table in each year's OWN Pillar 3 "
    "edition. Every edition prints the same rows for both Aldermore Group PLC and the Bank; the Bank "
    "columns are taken here, matching the entity basis of every other sheet in this workbook.\n"
    f"FY2026: Pillar 3 Report for the year ended 30 June 2026, p.6 (UK KM1 — Key metrics template, Bank "
    f"column a, 30-Jun-26) — {P3_2026_URL}\n"
    f"FY2025: Pillar 3 Disclosures for the year ended 30 June 2025, pp.4-5 (Key metrics, Bank 30 June 2025 "
    f"column). This edition's table BREAKS ACROSS A PAGE: capital, SREP, buffers, leverage and LCR on p.4, "
    f"the three NSFR rows on p.5 under their own heading. The other editions print it whole on one page "
    f"— {P3_2025_URL}\n"
    f"FY2024: Pillar 3 Disclosures for the year ended 30 June 2024, p.4 (Key metrics, Bank 30 June 2024) "
    f"— {P3_2024_URL}\n"
    f"FY2023: Pillar 3 Disclosures for the year ended 30 June 2023, p.4 (Key metrics, Bank 30 June 2023) "
    f"— {P3_2023_URL}\n"
    f"FY2022: Pillar 3 Disclosures for the year ended 30 June 2022, p.4 (Key metrics, Bank 30 June 2022) "
    f"— {P3_2022_URL}\n"
    "FY2021 and earlier carry no column: the FY2021 and FY2020 editions (83 and 86 pages, both located on "
    "Aldermore's own investor index on 2026-09-16) print no key-metrics table of any kind, and the template "
    "post-dates them — the Disclosure (CRR) Part of the PRA Rulebook applied from 1 January 2022. Those "
    "years are blank because the FY2021 EDITION published no such table, not because it was not found. A "
    "FY2021 comparative does exist: the FY2022 edition prints a 30 June 2021 Bank column for the capital, "
    "ratio and SREP rows (CET1 £947.0m, CET1 ratio 15.9%, total SREP 1.1%) and 'n/a' for every leverage, "
    "LCR and NSFR row. It is deliberately not used — each column here comes from its own year's edition.\n"
    "LATEST-EDITION CHECK: Aldermore's own investor index "
    "(https://www.aldermore.co.uk/investors/results-and-presentations/) checked 2026-09-16 — newest Pillar 3 "
    "is FY2026 (year ended 30 June 2026), already carried here. None newer.\n"
    "\n"
    "FOUR SOURCE INCONSISTENCIES, REPRODUCED AS PUBLISHED AND NOT RECONCILED. All 25 rows of all five "
    "columns were read off that year's OWN edition and re-checked against the printed page on 2026-09-16. "
    "The items below are differences BETWEEN editions, found by comparing each edition against the next "
    "edition's comparative column for the same entity and date (FY2022 vs FY2023, FY2024 vs FY2025, FY2025 "
    "vs FY2026). Nothing below was adjusted, spliced or averaged.\n"
    "1. 'Total SREP own funds requirements' (UK 7d) is a BASIS BREAK, not a fall: the FY2022 edition prints "
    "2.1% for the Bank — the ADDITIONAL requirement only, and the three component rows immediately above it "
    "sum to exactly that (1.2 + 0.4 + 0.5) — while the FY2023 edition onward print 10.1% for the same "
    "measure, the TOTAL including the 8% Pillar 1 minimum. The Group column breaks identically in the same "
    "editions (1.6% to 9.6%), which is what confirms this is the bank's change of basis and not a row "
    "misread on our side. The series is deliberately not spliced.\n"
    "2. That basis change is applied RETROSPECTIVELY to the comparative: the FY2022 edition prints 7.0% for "
    "'CET1 available after meeting the total SREP own funds requirements' at 30 June 2022, while the FY2023 "
    "edition's comparative prints 11.3% for that identical row and identical date.\n"
    "3. The FY2023 edition also RESTATES the FY2022 NSFR rows: available stable funding £15,667.6m becomes "
    "£14,273.5m, required stable funding £12,169.6m becomes £10,867.2m, and the ratio 128.7% becomes 131.3%. "
    "Every LCR row for that same date agrees exactly between the two editions, so the restatement is "
    "confined to NSFR rather than being a general re-basing of the liquidity section.\n"
    "4. FY2025's leverage exposure measure is RESTATED: the FY2025 edition prints £15,674.3m for the Bank at "
    "30 June 2025, the FY2026 edition's comparative £15,526.0m for that same date. £15,674.3m stands here. "
    "24 of the 25 FY2026 comparative rows agree exactly with the FY2025 edition — that row-by-row check is "
    "how this was found. Separately, the FY2025 edition's own 30 June 2024 comparatives print CET1 "
    "£1,321.4m, Tier 1 £1,382.4m and total capital £1,482.4m where the FY2024 edition printed £1,321.5m, "
    "£1,382.5m and £1,482.5m: 0.1m of precision drift on three capital rows, carrying into no ratio.\n"
    "The FY2022 edition prints 'n/a' rather than a figure for the FY2021 comparatives of every leverage, LCR "
    "and NSFR row, footnoted 'these disclosures have been implemented from 1 January 2022 ... no comparatives "
    "are being provided' — the 1 January 2022 basis break in the bank's own words. Those comparatives are not "
    "used here in any case, since each column is taken from its own year's edition."
)

bw.add_km1_sheet(
    title="Aldermore Bank PLC — KM1 Key Metrics",
    subtitle="Aldermore Bank PLC (Bank solo) columns of the bank's own published key-metrics template, in its "
             "own row order, labels and precision. Amounts in £m, ratios as printed. Row numbers are "
             "Aldermore's own from the FY2026 edition; the FY2022–FY2025 editions print the identical rows "
             "with no numbering. FY2021 and earlier predate the template and are intentionally blank.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=62,
    source_height=210,
    years=P3_DISCLOSURE_YEARS,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Bank solo basis, {unit}" if unit else "Bank solo basis",
                         rows_data, sources_text, note=note, first_col_width=46, source_height=110,
                         years=P3_DISCLOSURE_YEARS)

# FY2017: no 31 December 2017 reporting date exists (18-month transition period, see YEARS
# comment and p3_sources). Marked explicitly on every Pillar 3 sheet rather than left blank,
# so the distinction between "structurally impossible" and "not yet researched" survives in
# the sheet itself.

metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2026": 1450.9, "FY2025": 1337.8, "FY2024": 1321.5, "FY2023": 1203.8, "FY2022": 1065.9, "FY2021": 947.0, "FY2020": 860.9, "FY2019": 781.6, "FY2018": 682.2, "FY2017": NO_FY2017, "FY2016": 522.2, "FY2015": 433.2, "FY2014": 280.7, "FY2013": 250.4, "FY2012": 163.5, "FY2011": 158.2})],
    p3_sources(),
    note="FY2020 (860.9) and FY2016 (522.2) ADDED 2026-09-18 from the Bank-only Appendix 1 capital-composition "
         "table of each year's own Pillar 3 edition — editions this workbook previously asserted did not "
         "exist. Both reconcile: 860.9 is the FY2020 edition's own build-up (share capital 3.3 + share premium "
         "307.5 + FVOCI 1.5 + retained earnings 522.9 + IFRS 9 transitional add back 33.4 − intangibles 7.7) "
         "and 522.2 the FY2016 edition's (3.3 + 307.6 + capital contribution reserve 6.9 + AFS reserve 1.8 + "
         "retained earnings 225.5 − intangibles 21.9 − indirect CET1 holding 0.9 − prudent valuation 0.1). See "
         "the Pillar 3 recovery note in the sources below.\n"
         "FY2012 163.5 ADDED 2026-09-18 and is Basel II Core Tier 1 after deductions, on the same basis and "
         "from the same kind of narrative statement as FY2013's 250.4 and FY2011's 158.2 — see the paragraph "
         "below and the historical-editions note in the sources.\n"
         "FY2013, FY2012 and FY2011 ARE BASEL II CORE TIER 1, NOT A CRD IV CET1 CALCULATION. CET1 as a defined measure "
         "did not exist before CRD IV took effect on 1 January 2014, and neither recovered edition uses the term. "
         "What each does state is that its Tier 1 capital consisted solely of fully issued ordinary shares and "
         "audited reserves, with no AT1, hybrid or Tier 3 instrument at all — so the Core Tier 1 measure is placed "
         "here on the same no-AT1 convention used elsewhere in this workbook, with the basis flagged rather than "
         "presented as a like-for-like CET1. FY2013 250.4 is the figure stated in that edition's own narrative; "
         "FY2011 158.2 is likewise stated in narrative and is the £166,143k Total Core Tier 1 capital of the same "
         "page's table less that table's own £7,915k intangible-assets deduction; FY2012 163.5 is stated in the "
         "recovered 2012 edition's narrative and is likewise that edition's table's £170,931k Total Core Tier 1 "
         "less its own £7,467k intangible-assets deduction. The prior version of this note said FY2012 was blank "
         "because no 2012 edition exists in the archive — it does; see the Pillar 3 recovery note in the sources.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 ratio", {"FY2026": "17.7%", "FY2025": "18.4%", "FY2024": "19.2%", "FY2023": "18.5%", "FY2022": "17.0%", "FY2021": "15.9%", "FY2020": "13.4%", "FY2019": "12.6%", "FY2018": "12.5%", "FY2017": NO_FY2017, "FY2016": "11.4%", "FY2015": "11.7%", "FY2014": "10.3%"})],
    p3_sources(),
    note="FY2020 (13.4%) and FY2016 (11.4%) WERE sourced from the Bank's own Annual Report 'Financial "
         "highlights' page on the stated grounds that no Pillar 3 document survived for those years. Both "
         "editions were recovered on 2026-09-18 and each prints exactly the same ratio in its Bank-only "
         "Appendix 1 capital-composition table, so the figures are unchanged and are now independently "
         "corroborated. That corroboration also settles a question the earlier sourcing left open: the same "
         "tables give the GROUP ratios as 11.5% (FY2016) and 13.3% (FY2020), so the Annual Report highlight "
         "figures were indeed Bank-basis and did not quietly mix an entity into this series. See the Pillar 3 "
         "recovery note in the sources below.\n"
         "FY2013, FY2012 and FY2011 are blank by design, not unresearched. The two recovered Basel II editions "
         "(31 Dec 2013 and 31 Dec 2011) disclose no risk-weighted-asset figure and no capital ratio of any kind — "
         "they publish the Pillar 1 CAPITAL requirement (8% x risk weight) instead — so there is no denominator to "
         "state and no ratio to transcribe. Deriving one by grossing the capital requirement up by 12.5 would be "
         "back-solving a figure neither document states, and is deliberately not done. The recovered FY2012 "
         "edition (see the Pillar 3 recovery note in the sources) behaves identically: capital requirement, no "
         "RWA, no ratio. The prior version of this note said FY2012 had no edition at all — it has one; what it "
         "does not have is a ratio.",
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2026": 1500.9, "FY2025": 1387.8, "FY2024": 1382.5, "FY2023": 1264.8, "FY2022": 1126.6, "FY2021": 1008.0, "FY2020": 921.9, "FY2019": 855.9, "FY2018": 756.5, "FY2017": NO_FY2017, "FY2016": 596.5, "FY2015": 507.5, "FY2014": 355.0, "FY2013": 250.4, "FY2012": 163.5, "FY2011": 158.2})],
    p3_sources(),
    note="FY2020 921.9 (CET1 860.9 + AT1 perpetual loan 61.0) and FY2016 596.5 (CET1 522.2 + AT1 perpetual loan "
         "74.3) ADDED 2026-09-18 from the recovered Bank-only Appendix 1 tables; both are printed totals, not "
         "sums computed here — the components are quoted only to show the shape. FY2012 163.5 is Basel II Core "
         "Tier 1 after deductions and equals this sheet's CET1 figure for the same reason FY2013 and FY2011 do. "
         "See the Pillar 3 recovery note in the sources.\n"
         "FY2013 250.4 and FY2011 158.2 are each recovered Basel II edition's own stated Tier 1 capital, after "
         "deductions, and are identical to the CET1 Capital sheet's figures for those years because neither year's "
         "Tier 1 contained any AT1 or hybrid instrument — each document states expressly that Tier 1 consisted of "
         "fully issued ordinary shares and audited reserves and that no Tier 3 capital was held. That is a real "
         "change of shape rather than a gap: from FY2014 the Bank's Tier 1 exceeds its CET1 (FY2014 355.0 vs 280.7) "
         "because AT1 had been issued by then. See sources.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2026": "18.3%", "FY2025": "19.1%", "FY2024": "20.1%", "FY2023": "19.4%", "FY2022": "18.0%", "FY2021": "16.9%", "FY2020": "14.4%", "FY2019": "13.9%", "FY2018": "13.9%", "FY2017": NO_FY2017, "FY2016": "13.0%", "FY2015": "13.8%", "FY2014": "13.1%"})],
    p3_sources(),
    note="FY2020 14.4% and FY2016 13.0% ADDED 2026-09-18, both printed in the 'Capital ratios' block of the "
         "recovered Bank-only Appendix 1 table for that year — not derived from the capital and RWA rows above "
         "them. (The FY2020 edition's own summary Table 1 prints 14.4% for the Bank too; note that its 30 June "
         "2019 comparative there reads 13.8% against the 13.9% printed in Appendix 1 and held on this sheet "
         "from the FY2019 edition — a 0.1pp rounding difference inside one document, recorded, not "
         "reconciled.)\n"
         "FY2013, FY2012 and FY2011 are blank by design: all three recovered Basel II editions publish a Pillar 1 "
         "capital requirement and no RWA figure and no capital ratio, so no ratio can be transcribed and none is "
         "derived. The prior version of this note said FY2012 had no edition at all; it does — see the Pillar 3 "
         "recovery note in the sources.",
)

metric(
    "Total Capital", "£m",
    [
        ("Total capital", {"FY2026": 1800.9, "FY2025": 1487.8, "FY2024": 1482.5, "FY2023": 1364.8, "FY2022": 1226.6, "FY2021": 1168.0, "FY2020": 1081.9, "FY2019": 1015.9, "FY2018": 833.9, "FY2017": NO_FY2017, "FY2016": 709.6, "FY2015": 556.1, "FY2014": 400.3, "FY2012": 199.7, "FY2011": 159.6}),
        ("Basel II editions' own narrative components, where the edition prints no total (FY2013 only): Tier 1 capital after deductions", {"FY2013": 250.4}),
        ("Basel II editions' own narrative components, where the edition prints no total (FY2013 only): Tier 2 capital", {"FY2013": 39.3}),
    ],
    p3_sources(),
    note="FY2020 1,081.9 and FY2016 709.6 ADDED 2026-09-18 — each is the printed 'Total regulatory capital "
         "resources' line of that year's recovered Bank-only Appendix 1 capital-composition table (FY2020: CET1 "
         "860.9 + AT1 61.0 + Tier 2 160.0; FY2016: CET1 522.2 + AT1 74.3 + Tier 2 113.1). FY2012 199.7 is the "
         "recovered 2012 edition's own printed 'Total capital less deductions' line (£199,671k). All three are "
         "stated totals, not sums computed here. See the Pillar 3 recovery note in the sources.\n"
         "FY2011 159.6 is the recovered 31 December 2011 edition's own printed 'Total capital less deductions' line "
         "(£159,602k) — likewise a stated total.\n"
         "FY2013 STILL HAS NO FIGURE ON THE TOTAL CAPITAL ROW, AND THE TWO ROWS BENEATH IT ARE WHY. That edition "
         "states £250.4m of Tier 1 capital and £39.3m of Tier 2 capital and never prints a total. The earlier "
         "reason for leaving it blank was that the edition does not say whether those components are before or "
         "after deductions. The recovered 2012 edition now answers that: its identical narrative sentence gives "
         "£163.5m + £36.2m = £199.7m, which is exactly its own printed post-deduction total — so the narrative "
         "pair is an after-deductions pair, and FY2013's total capital after deductions is almost certainly "
         "£289.7m. ALMOST CERTAINLY IS NOT DISCLOSED. The addition is still ours, not the document's, so the "
         "total row stays empty and the two components the 2013 edition does print sit on their own rows above, "
         "verbatim. A reader who wants the total can add them and will know exactly what they did.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2026": "22.0%", "FY2025": "20.5%", "FY2024": "21.6%", "FY2023": "21.0%", "FY2022": "19.6%", "FY2021": "19.6%", "FY2020": "16.9%", "FY2019": "16.4%", "FY2018": "15.3%", "FY2017": NO_FY2017, "FY2016": "15.5%", "FY2015": "15.1%", "FY2014": "14.7%"})],
    p3_sources(),
    note="FY2020 16.9% and FY2016 15.5% ADDED 2026-09-18, both printed in the 'Capital ratios' block of the "
         "recovered Bank-only Appendix 1 table for that year; nothing is derived. Note that FY2016's 15.5% is "
         "ABOVE FY2015's 15.1% while the CET1 ratio fell over the same year (11.7% to 11.4%) — that is the "
         "Bank's own disclosure, driven by a £60m subordinated loan from Aldermore Group PLC taking Tier 2 from "
         "£48.6m to £113.1m, and is not a transcription slip. See the Pillar 3 recovery note in the sources.\n"
         "FY2013, FY2012 and FY2011 are blank by design: no RWA denominator and no capital ratio is published in "
         "any of the three recovered Basel II editions, and none is derived. See the CET1 Ratio sheet's note and "
         "sources.",
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted assets (RWA)", {"FY2026": 8203.7, "FY2025": 7271.6, "FY2024": 6875.6, "FY2023": 6504.9, "FY2022": 6260.1, "FY2021": 5964.1, "FY2020": 6406.3, "FY2019": 6179.0, "FY2018": 5451.0, "FY2017": NO_FY2017, "FY2016": 4572.7, "FY2015": 3687.5, "FY2014": 2719.5})],
    p3_sources(),
    note="FY2020 6,406.3 and FY2016 4,572.7 ADDED 2026-09-18 from the recovered Bank-only 'Total minimum Pillar 1 "
         "capital requirement' table of each year's own Pillar 3 edition. Both foot exactly to their own "
         "components (FY2020: 5,818.3 + 0.2 + 586.7 + 1.1; FY2016: 4,264.1 + 0.2 + 307.2 + 1.2) and both "
         "reproduce the printed ratios against the capital figures on the neighbouring sheets. See the Pillar 3 "
         "recovery note in the sources.\n"
         "FY2013, FY2012 and FY2011 are blank by design, and this is the single most important gap to understand in "
         "the recovered historical columns. The 31 December 2013, 2012 and 2011 editions disclose the Pillar 1 "
         "CAPITAL requirement by exposure class (8% x risk weight) — £165,031k, £110,063k and £68,091k of "
         "credit-risk capital respectively, plus operational-risk charges of £6.5m, £3.8m and £1.9m — but no "
         "risk-weighted-asset amount "
         "anywhere, and no total against which a ratio could be quoted. Multiplying those capital requirements by "
         "12.5 would produce a plausible-looking RWA that no document states, so it is not done; the capital "
         "requirements are instead shown as capital, on clearly labelled rows of the RWA Breakdown sheet. The "
         "prior version of this note said FY2012 had no edition at all — it does; see the Pillar 3 recovery note "
         "in the sources.",
)

# ---------------------------------------------------------------
# Sheet: RWA Breakdown (Pillar 3's UK OV1 template - placed next to
# Total RWAs, since it's itself a Pillar 3 disclosure)
# ---------------------------------------------------------------
RWA_BREAKDOWN_PRESENTATION_NOTE = (
    "PRESENTATION NOTE: transcribed from each year's own Pillar 3 disclosures' 'Overview of RWA' table, Bank "
    "solo (not Group) column, where a full Pillar 3 document is available. FY2019/FY2018 and FY2015/FY2014 use "
    "the simpler 'Total minimum Pillar 1 capital requirement' table instead (credit risk / market risk / "
    "operational risk / CVA only — no separate counterparty-credit-risk or securitisation RWA line existed in "
    "that disclosure format). THE TWO TEMPLATES ARE SHOWN AS SEPARATE SECTIONS, each with its own rows and its "
    "own total, so no row carries figures from both: the category sets differ, and a row read straight across "
    "would change meaning partway along. Nothing is merged, re-labelled or estimated across the break — the "
    "'(excluding CCR)' qualifier in particular belongs only to the UK OV1 block, because the older table draws "
    "no such distinction. FY2016 AND FY2020 WERE ADDED TO THE OLDER TABLE'S SECTION ON 2026-09-18, replacing "
    "the previous claim that they 'have no RWA breakdown at all (no standalone Pillar 3 document survives)'. "
    "Both editions exist and both print the Bank-only version of exactly that table — see the Pillar 3 "
    "recovery note in the sources. FY2012 was added to the Basel II capital-requirement section for the same "
    "reason. This sheet's Total row ties out exactly to the Total RWAs sheet for every year with data.\n\n"
    "FY2026: the UK OV1 template in the FY2026 report has no market-risk row at all, so that row is left "
    "blank for FY2026 rather than written as zero. FY2026 rows sum exactly to the 8,203.7 total (7,291.1 + "
    "4.7 + 2.8 + 22.5 + 882.6), which ties to UK KM1 row 4. Note the FY2026 report re-presents the FY2025 "
    "comparative differently from the FY2025 report itself: it splits out CVA of 5.6 and shows credit risk "
    "(excluding CCR) of 6,405.2 and operational risk of 830.5, where the FY2025 own-year document reported "
    "credit risk of 6,410.7 with no separate Bank-solo CVA line and operational risk of 830.6. Both "
    "presentations total 7,271.6. The FY2025 column on this sheet is left as each year's own-year "
    "disclosure, consistent with every other year here, rather than restated to the later document's split. "
    "The FY2026 report also notes that IFRS 9 transitional arrangements under CRR Article 473a expired in "
    "June 2025, so FY2025 credit risk includes £11.3m of IFRS 9 transitional risk exposure that FY2026 does "
    "not.\n\n"
    "FY2013 AND FY2011 HAVE NO RWA ROWS AT ALL, AND THE BLOCK AT THE FOOT OF THIS SHEET IS NOT RWA. The two "
    "recovered Basel II editions (31 December 2013 and 31 December 2011) never disclose a risk-weighted-asset "
    "amount — not by category and not in total. What they publish is the Pillar 1 CAPITAL requirement by "
    "exposure class, headed 'Pillar 1 Capital (8% x Risk Weight)'. Those figures are transcribed exactly as "
    "disclosed, in £m of capital, on their own clearly labelled rows beneath the RWA block, and are NOT "
    "converted to RWA by the 12.5 scalar, because the resulting total would be a number neither document "
    "states. FY2013's credit-risk total of £165.0m is the sum printed at the foot of that table (£165,031k "
    "across government/central banks nil, regional governments 72, MDBs nil, institutions 3,582, corporates "
    "8,907, retail 50,354, secured on residential property 56,083, secured on commercial real estate 38,322, "
    "past due items 2,490, securitisation positions 1,224, other items 3,997); FY2011's is likewise the "
    "printed £68,091k total. The operational-risk rows are each document's own basic-indicator charge stated "
    "in its operational risk section (£6.5m for 2013, £1.9m for 2011). The memo exposure row is the printed "
    "total exposure value net of provisions including off-balance-sheet items, which is an exposure measure "
    "and emphatically not an RWA — for FY2013 it is £4,746.6m against a £4,194.3m statutory balance sheet, "
    "the difference being commitments and guarantees. FY2012 is blank throughout: no 2012 edition exists in "
    "the archive and neither adjacent edition carries a comparative column."
)

RWA_BREAKDOWN_SOURCES = (
    "Sources — Aldermore Bank PLC solo figures from the 'Overview of RWA' / 'Total minimum Pillar 1 capital "
    "requirement' table, Aldermore Group PLC Pillar 3 Disclosures:\n"
    f"FY2026: Pillar 3 Report for the year ended 30 June 2026, p.8 (UK OV1 — Overview of risk-weighted "
    f"exposure amounts, Bank column a, 30-Jun-26) — {P3_2026_URL}\n"
    f"FY2025 & FY2024: Pillar 3 Disclosures for the year ended 30 June 2025, p.9 (Overview Of RWA, Bank "
    f"column) — {P3_2025_URL}\n"
    f"FY2023: Pillar 3 Disclosures for the year ended 30 June 2024, p.8 (Overview Of RWA, Bank column, "
    f"FY2023 comparative) — {P3_2024_URL}\n"
    f"FY2022 & FY2021: Pillar 3 Disclosures for the year ended 30 June 2022, p.7 (Overview of RWA, Bank "
    f"column) — {P3_2022_URL}\n"
    f"FY2020: Pillar 3 Disclosures for the year ended 30 June 2020, p.61 (Appendix 1, Table 34 — Total minimum "
    f"Pillar 1 capital requirement, Bank only) — {P3_2020_URL}\n"
    f"FY2019 & FY2018: Pillar 3 Disclosures for the year ended 30 June 2019, p.57 (Appendix 1, Table 34 — "
    f"Total minimum Pillar 1 capital requirement, Bank only) — {P3_2019_URL}\n"
    f"FY2016: Pillar 3 Disclosures 31 December 2016, p.58 (Appendix 1, Table 34 — Total minimum Pillar 1 "
    f"capital requirement, Bank only) — {P3_2016_URL}\n"
    f"FY2015 & FY2014: Pillar 3 Disclosures 31 December 2015, p.58 (Appendix 1, Table 31 — Total minimum "
    f"Pillar 1 capital requirement, Bank only) — {P3_2015_URL}\n"
    f"FY2012 (CAPITAL requirement rows only, not RWA): Aldermore Bank PLC — Pillar 3 Disclosures 31 December "
    f"2012, p.11 (Credit Risk Exposures, 'Pillar 1 Capital (8% x Risk Weight)' column) and p.18 (operational "
    f"risk charge) — {P3_2012_URL}\n"
    f"FY2013 (CAPITAL requirement rows only, not RWA): Aldermore Bank PLC — Pillar 3 Disclosures 31 December "
    f"2013, p.11 (Credit risk exposure by exposure class, 'Pillar 1 Capital (8% x Risk Weight)' column) and "
    f"Section 9 (operational risk charge) — {P3_2013_URL}\n"
    f"FY2011 (CAPITAL requirement rows only, not RWA): Aldermore Bank Plc — Pillar 3 Disclosures December 31 "
    f"2011, p.12 (Credit risk exposure by exposure class) and Section 9 (operational risk charge) — "
    f"{P3_2011_URL}\n\n" + RWA_BREAKDOWN_PRESENTATION_NOTE
)

rwa_breakdown_rows = [
    ("SECTION", "UK OV1 / 'Overview of RWA' template — Aldermore Group PLC Pillar 3 Disclosures, Bank solo column (FY2026-FY2021)", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2026": 7291.1, "FY2025": 6410.7, "FY2024": 6071.2, "FY2023": 5802.1, "FY2022": 5624.9, "FY2021": 5338.2}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2026": 4.7, "FY2025": 4.8, "FY2024": 20.9, "FY2023": 37.1, "FY2022": 0.9, "FY2021": 0.9}),
    ("DATA", "Securitisation exposures in the non-trading book", {"FY2026": 22.5, "FY2025": 25.5, "FY2024": 40.0, "FY2023": 22.5, "FY2022": 29.2, "FY2021": 23.1}),
    ("DATA", "Position, foreign exchange and commodities risks (market risk)", {"FY2025": 0, "FY2024": 0.1, "FY2023": 1.8, "FY2022": 0.4, "FY2021": 0.1}),
    ("DATA", "Credit valuation adjustment (CVA)", {"FY2026": 2.8}),
    ("DATA", "Operational risk", {"FY2026": 882.6, "FY2025": 830.6, "FY2024": 743.4, "FY2023": 641.4, "FY2022": 604.7, "FY2021": 601.8}),
    ("TOTAL", "Total risk-weighted assets (RWA)", {"FY2026": 8203.7, "FY2025": 7271.6, "FY2024": 6875.6, "FY2023": 6504.9, "FY2022": 6260.1, "FY2021": 5964.1}),
    ("SECTION", "'Total minimum Pillar 1 capital requirement' table — Pillar 3 Disclosures y/e 30 Jun 2020 (Appendix 1, Table 34), y/e 30 Jun 2019 (Appendix 1, Table 34), 31 Dec 2016 (Appendix 1, Table 34) and 31 Dec 2015 (Appendix 1, Table 31), Bank only (FY2020, FY2019, FY2018, FY2016, FY2015, FY2014)", {}),
    ("DATA", "Credit risk", {"FY2020": 5818.3, "FY2019": 5643.3, "FY2018": 4950.6, "FY2016": 4264.1, "FY2015": 3480.6, "FY2014": 2592.5}),
    ("DATA", "Market risk", {"FY2020": 0.2, "FY2019": 0.3, "FY2018": 0.4, "FY2016": 0.2, "FY2015": 0.1, "FY2014": 0.3}),
    ("DATA", "Credit valuation adjustment (CVA)", {"FY2020": 1.1, "FY2019": 2.1, "FY2018": 1.0, "FY2016": 1.2, "FY2015": 1.3, "FY2014": 1.6}),
    ("DATA", "Operational risk", {"FY2020": 586.7, "FY2019": 533.3, "FY2018": 499.0, "FY2016": 307.2, "FY2015": 205.5, "FY2014": 125.1}),
    ("TOTAL", "Total risk-weighted assets (RWA)", {"FY2020": 6406.3, "FY2019": 6179.0, "FY2018": 5451.0, "FY2016": 4572.7, "FY2015": 3687.5, "FY2014": 2719.5}),
    ("SECTION", "Pillar 1 CAPITAL requirement, Basel II editions FY2013, FY2012 and FY2011 (£m of CAPITAL, not RWA — deliberately NOT multiplied by 12.5; do not read down the same column as the RWA rows above)", {}),
    ("DATA", "Capital requirement — credit risk (standardised, 8% x risk weight, all exposure classes)", {"FY2013": 165.0, "FY2012": 110.1, "FY2011": 68.1}),
    ("DATA", "Capital requirement — operational risk (basic indicator approach)", {"FY2013": 6.5, "FY2012": 3.8, "FY2011": 1.9}),
    ("DATA", "Memo: total credit risk exposure value after provisions, incl. off-balance-sheet (£m — an exposure measure, not an RWA)", {"FY2013": 4746.6, "FY2012": 2844.6, "FY2011": 1647.4}),
    ("SECTION", "FY2017 — no 31 December 2017 reporting date exists (18-month transition period to 30 June 2018); the FY2018 column covers 1 Jan 2017 to 30 Jun 2018", {}),
    ("DATA", "Total risk-weighted assets (RWA)", {"FY2017": NO_FY2017}),
]

bw.add_rwa_breakdown_sheet(
    title="Aldermore Bank PLC — RWA Breakdown (Overview of Risk Weighted Assets)",
    subtitle="Bank solo basis, £m",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=58,
    source_height=140,
    years=P3_DISCLOSURE_YEARS,
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total exposure measure excluding claims on central banks (£m)", {"FY2026": 16715.1, "FY2025": 15674.3, "FY2024": 14337.2, "FY2023": 13609.6, "FY2022": 13850.3, "FY2021": "n/a", "FY2020": 15132.5, "FY2019": 12671.6, "FY2018": 10585.1, "FY2017": NO_FY2017, "FY2016": 8562.9, "FY2015": 7095.9, "FY2014": 5630.4, "FY2013": "n/a", "FY2012": "n/a", "FY2011": "n/a"}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2026": "9.0%", "FY2025": "8.9%", "FY2024": "9.6%", "FY2023": "9.3%", "FY2022": "8.1%", "FY2021": "n/a", "FY2020": "6.1%", "FY2019": "6.8%", "FY2018": "7.1%", "FY2017": NO_FY2017, "FY2016": "7.0%", "FY2015": "7.2%", "FY2014": "6.3%", "FY2013": "n/a", "FY2012": "n/a", "FY2011": "n/a"}),
    ],
    p3_sources(),
    note="FY2020 (exposure 15,132.5, ratio 6.1%) and FY2016 (exposure 8,562.9, ratio 7.0%) ADDED 2026-09-18 from "
         "row 21/row 22 of the 'Leverage ratio common disclosure (Bank only)' table of each year's own recovered "
         "Pillar 3 edition (FY2020 p.65, FY2016 p.62). Both are on the same pre-2022 all-exposures basis as the "
         "FY2019/FY2018/FY2015/FY2014 figures beside them, not the 'excluding claims on central banks' variant "
         "the row label carries for FY2022 onward — see the basis paragraph below. Note that the summary "
         "reconciliation table on the facing page of each edition gives a slightly different exposure (FY2020 "
         "15,132.5 both ways; FY2016 8,591.4 on the reconciliation against 8,562.9 on the common-disclosure "
         "template, a £28.5m difference inside one document); the common-disclosure row 21 figure is used, being "
         "the one the printed ratio is struck on. See the Pillar 3 recovery note in the sources.\n"
         "FY2021 leverage ratio disclosure basis was introduced from 1 January 2022; the FY2022 Pillar 3 report explicitly "
         "marks FY2021 as 'n/a' with no comparative provided under the new template. FY2019/FY2018 and FY2015/FY2014 "
         "figures are each year's own pre-2022 leverage ratio disclosure basis (both are the CRR Part Eight / EBA "
         "Implementing Technical Standard leverage ratio, but the 'excluding claims on central banks' variant used from "
         "FY2022 onward did not exist as a separate disclosure before then, so these earlier figures are the Bank's "
         "then-current all-exposures leverage ratio, not a like-for-like restatement), and the same applies to the "
         "newly added FY2016 and FY2020 — the previous version of this note said those two years 'have no "
         "leverage ratio figure at all (no standalone Pillar 3 document survives for either year)', which was "
         "wrong on both counts. FY2013, FY2012 "
         "and FY2011 are 'n/a' for a structural reason rather than a sourcing one: no leverage ratio existed as a UK "
         "regulatory measure or disclosure at 31 December 2011 or 31 December 2013 (the CRR leverage ratio arrived "
         "with CRD IV from 2014), and neither recovered Basel II edition contains one in any form.\n"
         "RESTATEMENT: the FY2026 Pillar 3 report restates the Bank's 30-Jun-25 total exposure measure as "
         "£15,526.0m, where the FY2025 report itself disclosed £15,674.3m for that same period (a £148.3m "
         "reduction). The FY2025 column here is left at the £15,674.3m originally disclosed, consistent with "
         "how every other year on this sheet is presented on its own-year basis; the restated figure is "
         "recorded here rather than substituted. The leverage ratio rounds to 8.9% on either basis, so only "
         "the exposure-measure row is affected.",
)

metric(
    "LCR", "£m / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value average (£m)", {"FY2026": 3725.9, "FY2025": 3723.1, "FY2024": 4208.6, "FY2023": 3280.6, "FY2022": 2838.5, "FY2021": "n/a", "FY2020": "n/a", "FY2019": "n/a", "FY2018": "n/a", "FY2017": NO_FY2017, "FY2016": "n/a", "FY2015": "n/a", "FY2014": "n/a", "FY2013": "n/a", "FY2012": "n/a", "FY2011": "n/a"}),
        ("Total net cash outflows, adjusted value (£m)", {"FY2026": 2263.1, "FY2025": 1968.3, "FY2024": 1959.4, "FY2023": 1686.4, "FY2022": 772.6, "FY2021": "n/a", "FY2020": "n/a", "FY2019": "n/a", "FY2018": "n/a", "FY2017": NO_FY2017, "FY2016": "n/a", "FY2015": "n/a", "FY2014": "n/a", "FY2013": "n/a", "FY2012": "n/a", "FY2011": "n/a"}),
        ("Liquidity Coverage Ratio (%)", {"FY2026": "164.6%", "FY2025": "189.2%", "FY2024": "214.8%", "FY2023": "194.5%", "FY2022": "367.4%", "FY2021": "n/a", "FY2020": "n/a", "FY2019": "n/a", "FY2018": "n/a", "FY2017": NO_FY2017, "FY2016": "n/a", "FY2015": "n/a", "FY2014": "n/a", "FY2013": "n/a", "FY2012": "n/a", "FY2011": "n/a"}),
    ],
    p3_sources(),
    note="LCR is computed as a 12-month average to the period end. FY2021 and earlier are all 'n/a' — the Bank-solo "
         "LCR disclosure template used on this sheet was introduced from 1 January 2022 (see FY2022 Pillar 3 report); "
         "no comparable Bank-solo LCR figure was located for FY2014-FY2020 in the documents reviewed for this "
         "extension (the Basel LCR standard itself phased in nationally from 2015, but the Bank's own Pillar 3 "
         "reports for those years did not publish a Bank-solo LCR figure in the format used here — re-checked "
         "2026-09-18 against the FY2016 and FY2020 editions recovered that day, which is worth stating "
         "explicitly: those two documents DO exist and DO carry a full Bank-only appendix, and they still print "
         "no LCR, so 'n/a' for FY2016 and FY2020 is now a statement about the disclosure rather than about our "
         "reach). FY2017 reads 'No 31 Dec 2017 period exists' rather than 'n/a' because nothing could have been "
         "disclosed at that date at all. FY2013 and "
         "FY2011 are 'n/a' on firmer ground still: the LCR did not exist as a UK requirement or disclosure at "
         "either date (it was introduced by CRD IV/CRR and phased in from October 2015), and neither recovered "
         "Basel II edition contains any liquidity ratio - each describes liquidity risk narratively and by the "
         "then-applicable ILAA/liquid asset buffer framework instead. FY2012 has no edition at all.",
)

metric(
    "NSFR", "£m / %",
    [
        ("Total available stable funding (£m)", {"FY2026": 16701.9, "FY2025": 15972.4, "FY2024": 16133.4, "FY2023": 15490.2, "FY2022": 15667.6, "FY2021": "n/a", "FY2020": "n/a", "FY2019": "n/a", "FY2018": "n/a", "FY2017": NO_FY2017, "FY2016": "n/a", "FY2015": "n/a", "FY2014": "n/a", "FY2013": "n/a", "FY2012": "n/a", "FY2011": "n/a"}),
        ("Total required stable funding (£m)", {"FY2026": 13318.4, "FY2025": 12166.9, "FY2024": 11778.0, "FY2023": 12161.3, "FY2022": 12169.6, "FY2021": "n/a", "FY2020": "n/a", "FY2019": "n/a", "FY2018": "n/a", "FY2017": NO_FY2017, "FY2016": "n/a", "FY2015": "n/a", "FY2014": "n/a", "FY2013": "n/a", "FY2012": "n/a", "FY2011": "n/a"}),
        ("Net Stable Funding Ratio (%)", {"FY2026": "125.4%", "FY2025": "131.3%", "FY2024": "137.0%", "FY2023": "127.4%", "FY2022": "128.7%", "FY2021": "n/a", "FY2020": "n/a", "FY2019": "n/a", "FY2018": "n/a", "FY2017": NO_FY2017, "FY2016": "n/a", "FY2015": "n/a", "FY2014": "n/a", "FY2013": "n/a", "FY2012": "n/a", "FY2011": "n/a"}),
    ],
    p3_sources(),
    note="NSFR is computed as a 4-quarter average to the period end. FY2021 and earlier are all 'n/a' — the UK NSFR "
         "requirement did not take effect until 1 January 2022 (see FY2022 Pillar 3 report), so no NSFR figure exists "
         "for FY2014-FY2020 at all. This is the one metric on this workbook where recovering the FY2016 and "
         "FY2020 Pillar 3 editions (see the Pillar 3 recovery note in the sources) changed nothing and could not "
         "have: there was no NSFR to disclose in either year. The same applies with more force to FY2013, FY2012 "
         "and FY2011, which predate even the "
         "Basel III NSFR observation period; none of the three recovered Basel II editions contains an NSFR. "
         "FY2017 reads 'No 31 Dec 2017 period exists' rather than 'n/a' because no reporting date existed there "
         "at all.",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not publicly disclosed" for y in P3_DISCLOSURE_YEARS})],
    p3_sources(),
    note="MREL is not disclosed for Aldermore Bank PLC/Aldermore Group PLC in any Pillar 3 report reviewed — the Group "
         "sits below the balance-sheet threshold at which the Bank of England sets a bail-in MREL requirement above "
    "minimum capital requirements, so no separate MREL ratio is published.",
)

# ---------------------------------------------------------------
# Interim Pillar 3 disclosures
# ---------------------------------------------------------------
INTERIM_HEADERS = [
    "Period",
    "Disclosure type",
    "Metric",
    "Value",
    "Unit",
    "Basis",
    "Source document",
    "Page / table",
]

INTERIM_PERIODS = [
    ("31 Dec 2025", "H1 2025 interim (current period)"),
    ("30 Jun 2025", "H1 2025 interim (comparative)"),
    ("31 Dec 2024", "H1 2025 interim (comparative)"),
]

INTERIM_METRICS = [
    ("CET1 capital", [1342.5, 1337.8, 1306.1], "£m"),
    ("Tier 1 capital", [1392.5, 1387.8, 1367.1], "£m"),
    ("Total capital", [1692.5, 1487.8, 1467.1], "£m"),
    ("Total risk-weighted exposure amount", [7352.0, 7271.6, 6997.3], "£m"),
    ("CET1 ratio", ["18.3%", "18.4%", "18.7%"], "%"),
    ("Tier 1 ratio", ["18.9%", "19.1%", "19.5%"], "%"),
    ("Total capital ratio", ["23.0%", "20.5%", "21.0%"], "%"),
    ("Total exposure measure excluding claims on central banks", [15369.1, 15526.0, 14826.8], "£m"),
    ("Leverage ratio excluding claims on central banks", ["9.1%", "8.9%", "9.2%"], "%"),
    ("Total high-quality liquid assets (HQLA), weighted-value average", [3518.6, 3723.1, 4062.3], "£m"),
    ("Total net cash outflows (adjusted value)", [1964.8, 1968.3, 2047.1], "£m"),
    ("Liquidity coverage ratio", ["179.1%", "189.2%", "198.4%"], "%"),
    ("Total available stable funding", [16221.9, 15972.4, 16013.1], "£m"),
    ("Total required stable funding", [12699.7, 12166.9, 11856.4], "£m"),
    ("NSFR ratio", ["127.7%", "131.3%", "135.1%"], "%"),
    ("MREL ratio", ["Not disclosed", "Not disclosed", "Not disclosed"], "%"),
]

interim_rows = []
for period_index, (period, disclosure_type) in enumerate(INTERIM_PERIODS):
    for metric_name, values, unit in INTERIM_METRICS:
        interim_rows.append(
            [
                period,
                disclosure_type,
                metric_name,
                values[period_index],
                unit,
                "Aldermore Bank PLC (Bank solo)",
                "Aldermore Group PLC Interim Pillar 3 Disclosure — 31 December 2025",
                "p.4, Key Metrics (Bank column)",
            ]
        )

interim_hyperlinks = {(i, 6): INTERIM_P3_2025_URL for i in range(len(interim_rows))}
bw.add_wide_interim_sheet(
    "Interim Pillar 3",
    rows=interim_rows,
    hyperlink_cells=interim_hyperlinks,
    title="Aldermore Bank PLC — Interim Pillar 3",
    subtitle="Bank solo basis; amounts in £m and ratios in %, as disclosed in the official interim Key Metrics table",
    note=(
        "Source: Aldermore Group PLC Interim Pillar 3 Disclosure as at 31 December 2025, p.4, Key Metrics — Bank column. "
        f"Official PDF: {INTERIM_P3_2025_URL}\n"
        "The document reports 31 Dec 2025 and comparative 30 Jun 2025 and 31 Dec 2024 figures. No separate official "
        "half-year Pillar 3 document was located in the archive for 2021, 2022, 2023, or 2024; those periods are therefore "
        "not inferred or backfilled. MREL is not included in the Key Metrics table and is recorded as not disclosed."
    ),
)
# Keep the source register immediately after the matrix so the current
# verifier can discover it without changing the shared helper.
interim_ws = bw.wb["Interim Pillar 3"]
interim_ws.delete_rows(5 + len({row[2] for row in interim_rows}), 2)
for row_number in range(5, interim_ws.max_row + 1):
    if interim_ws.cell(row=row_number, column=1).value == "Source register":
        source_register_row = row_number
        break
    for column_number in range(4, interim_ws.max_column + 1):
        cell = interim_ws.cell(row=row_number, column=column_number)
        if cell.value not in (None, ""):
            cell.hyperlink = INTERIM_P3_2025_URL
            cell.style = "Hyperlink"
for row_number in range(source_register_row + 2, interim_ws.max_row + 1):
    if interim_ws.cell(row=row_number, column=1).value in (None, ""):
        break
    source_cell = interim_ws.cell(row=row_number, column=3)
    source_cell.hyperlink = INTERIM_P3_2025_URL
    source_cell.style = "Hyperlink"

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 20618.2, "FY2024": 20195.5, "FY2023": 19051.7, "FY2022": 17290.8, "FY2021": 15583.0, "FY2020": 15000.7, "FY2019": 12471.9, "FY2018": 10467.4, "FY2016": 8396.5, "FY2015": 7021.4, "FY2014": 5583.2}),
        ("Loans and advances to customers", {"FY2025": 12523.4, "FY2024": 11416.3, "FY2023": 10998.9, "FY2022": 10777.3, "FY2021": 10393.6, "FY2020": 10602.2, "FY2019": 10230.3, "FY2018": 8990.5, "FY2016": 7477.3, "FY2015": 6144.8, "FY2014": 4801.1}),
        ("Customers' accounts", {"FY2025": 17047.6, "FY2024": 16306.7, "FY2023": 15033.3, "FY2022": 14105.4, "FY2021": 12427.3, "FY2020": 10886.4, "FY2019": 8971.8, "FY2018": 7776.3, "FY2016": 6673.7, "FY2015": 5742.0, "FY2014": 4459.0}),
        ("Total equity", {"FY2025": 1514.6, "FY2024": 1371.8, "FY2023": 1219.0, "FY2022": 1098.6, "FY2021": 987.1, "FY2020": 896.2, "FY2019": 853.2, "FY2018": 766.7, "FY2016": 619.4, "FY2015": 527.3, "FY2014": 374.8}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total operating income", {"FY2025": 473.4, "FY2024": 462.9, "FY2023": 476.2, "FY2022": 389.8, "FY2021": 323.4, "FY2020": 313.1, "FY2019": 331.8, "FY2018": 468.5, "FY2016": 265.9, "FY2015": 221.6, "FY2014": 166.1}),
        ("Administrative expenses", {"FY2025": -266.8, "FY2024": -263.8, "FY2023": -253.5, "FY2022": -224.0, "FY2021": -173.7, "FY2020": -148.7, "FY2019": -169.4, "FY2018": -227.8, "FY2016": -117.8, "FY2015": -110.1, "FY2014": -100.8}),
        ("Profit after taxation", {"FY2025": 163.2, "FY2024": 162.1, "FY2023": 129.2, "FY2022": 118.0, "FY2021": 89.3, "FY2020": 64.2, "FY2019": 102.2, "FY2018": 155.9, "FY2016": 92.3, "FY2015": 80.1, "FY2014": 39.7}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 1371.8, "FY2024": 1219.0, "FY2023": 1098.5, "FY2022": 987.1, "FY2021": 896.2, "FY2020": 853.2, "FY2019": 766.7, "FY2018": 619.4, "FY2016": 527.3, "FY2015": 374.8, "FY2014": 259.4}),
        ("Total comprehensive income", {"FY2025": 158.9, "FY2024": 158.1, "FY2023": 125.7, "FY2022": 116.6, "FY2021": 96.1, "FY2020": 65.2, "FY2019": 101.5, "FY2018": 155.2, "FY2016": 95.1, "FY2015": 77.7, "FY2014": 40.5}),
        ("Other equity movements, net", {"FY2025": -16.1, "FY2024": -5.3, "FY2023": -5.2, "FY2022": -5.2, "FY2021": -5.2, "FY2020": -22.2, "FY2019": -15.0, "FY2018": -7.9, "FY2016": -3.0, "FY2015": 74.8, "FY2014": 74.9}),
        ("Closing equity", {"FY2025": 1514.6, "FY2024": 1371.8, "FY2023": 1219.0, "FY2022": 1098.6, "FY2021": 987.1, "FY2020": 896.2, "FY2019": 853.2, "FY2018": 766.7, "FY2016": 619.4, "FY2015": 527.3, "FY2014": 374.8}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash from operating activities", {"FY2025": -725.0, "FY2024": 730.1, "FY2023": 1108.5, "FY2022": 1215.7, "FY2021": 884.1, "FY2020": 2030.7, "FY2019": 296.7, "FY2018": 632.6, "FY2016": 0, "FY2015": 49.3, "FY2014": -205.7}),
        ("Net cash from investing activities", {"FY2025": -259.5, "FY2024": -401.6, "FY2023": 306.5, "FY2022": -334.8, "FY2021": -55.0, "FY2020": -711.6, "FY2019": -357.7, "FY2018": -133.0, "FY2016": -47.3, "FY2015": -98.9, "FY2014": -164.4}),
        ("Net cash from financing activities", {"FY2025": -18.4, "FY2024": -8.3, "FY2023": -331.2, "FY2022": -739.7, "FY2021": -697.7, "FY2020": -1280.5, "FY2019": 25.7, "FY2018": -88.4, "FY2016": 45.3, "FY2015": 65.5, "FY2014": 69.1}),
        ("Cash and cash equivalents at end of year", {"FY2025": 1216.7, "FY2024": 2219.6, "FY2023": 1899.4, "FY2022": 815.2, "FY2021": 674.0, "FY2020": 542.6, "FY2019": 504.0, "FY2018": 539.3, "FY2016": 128.1, "FY2015": 130.1, "FY2014": 114.2}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "18.4%", "FY2024": "19.2%", "FY2023": "18.5%", "FY2022": "17.0%", "FY2021": "15.9%", "FY2020": "13.4%", "FY2019": "12.6%", "FY2018": "12.5%", "FY2016": "11.4%", "FY2015": "11.7%", "FY2014": "10.3%"}),
        ("Tier 1 Ratio", {"FY2025": "19.1%", "FY2024": "20.1%", "FY2023": "19.4%", "FY2022": "18.0%", "FY2021": "16.9%", "FY2020": "14.4%", "FY2019": "13.9%", "FY2018": "13.9%", "FY2016": "13.0%", "FY2015": "13.8%", "FY2014": "13.1%"}),
        ("Total Capital Ratio", {"FY2025": "20.5%", "FY2024": "21.6%", "FY2023": "21.0%", "FY2022": "19.6%", "FY2021": "19.6%", "FY2020": "16.9%", "FY2019": "16.4%", "FY2018": "15.3%", "FY2016": "15.5%", "FY2015": "15.1%", "FY2014": "14.7%"}),
        ("Leverage Ratio", {"FY2025": "8.9%", "FY2024": "9.6%", "FY2023": "9.3%", "FY2022": "8.1%", "FY2020": "6.1%", "FY2019": "6.8%", "FY2018": "7.1%", "FY2016": "7.0%", "FY2015": "7.2%", "FY2014": "6.3%"}),
        ("LCR", {"FY2025": "189.2%", "FY2024": "214.8%", "FY2023": "194.5%", "FY2022": "367.4%"}),
        ("NSFR", {"FY2025": "131.3%", "FY2024": "137.0%", "FY2023": "127.4%", "FY2022": "128.7%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Fiscal year ends 30 June (31 December for FY2014-FY2016; the "
         "Bank's accounting reference date changed following its 2018 acquisition by FirstRand). Balance Sheet, "
         "Profit & Loss, Statement of Changes in Equity and Cash Flow figures are all Bank-solo; Pillar 3 ratios use "
         "the Bank-solo columns of Aldermore Group PLC's Pillar 3 disclosures (the only level at which Pillar 3 is "
         "published). "
         "FY2016 and FY2020 UPDATED 2026-09-18: this note previously said the FY2016/FY2020 CET1 Ratio came from "
         "the Bank's Annual Report highlights because 'no standalone Pillar 3 document survives for those two "
         "years', and Tier 1 Ratio, Total Capital Ratio and Leverage Ratio were blank in both years for the same "
         "stated reason. Both Pillar 3 editions were recovered on 2026-09-18 (FY2020 from Aldermore's own live "
         "investor index; FY2016 from the Wayback Machine, findable only by enumerating the whole host because its "
         "filename carries no year). Every ratio here for those two years is now the Bank-solo column of the "
         "recovered edition, and the two CET1 figures are unchanged from the Annual Report highlights — the "
         "documents corroborate each other. "
         "'Other equity movements, net' combines Additional Tier 1 capital issuance/redemption, AT1 coupon "
         "payments, and (FY2015/FY2014) the Aldermore Group PLC IPO share issue proceeds and warrant exercise. "
         "Leverage/LCR/NSFR have no FY2021 figure; LCR/NSFR have no figure at all before FY2022 (disclosure "
         "templates introduced from 1 Jan 2022) — see the Leverage Ratio/LCR/NSFR sheets for the "
         "disclosure-template basis note. FY2017 has no standalone 12-month period "
         "at all (see the Balance Sheet sheet's source note) and FY2018's column is an 18-month, not 12-month, "
         "period — both are omitted or flagged accordingly rather than estimated.",
)

bw.save("/Users/armaan/code/katalysis/banks/ALDERMORE FINANCIALS.xlsx")
