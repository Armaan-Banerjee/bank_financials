import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016",
         "FY2015", "FY2014", "FY2013"]
Y_CORE = YEARS[:YEARS.index('FY2014') + 1]  # HD-072/075/079: FY2014-floor default for Pillar 3/Asset Quality/RWA Breakdown/Overview
  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR_URL = {
    "FY2025": "https://files.bacb.co.uk/production/files/BACB_AnnualReportYE2025_WEB-Final.pdf",
    "FY2024": "https://files.bacb.co.uk/production/files/BACB_AnnualReportYE2024_WEB-Final.pdf",
    "FY2023": "https://files.bacb.co.uk/production/files/BACB_AnnualReportYE2023_WEB-06.pdf",
    "FY2022": "https://files.bacb.co.uk/production/files/BACB_AnnualReportYE2022_WEB-1proof-10.pdf",
    "FY2021": "https://files.bacb.co.uk/production/files/BACB_AnnualReportYE2021-1.pdf",
    "FY2020": "https://files.bacb.co.uk/production/files/BACB-Annual-Report-2020.pdf",
    "FY2019": "https://files.bacb.co.uk/production/files/BACB_AnnualReportYE2019-print-3-opt.pdf",
    "FY2018": "https://files.bacb.co.uk/production/files/BACB_AnnualReportYE2018-complete-6.pdf",
    "FY2017": "https://files.bacb.co.uk/production/files/BACB_AnnualReport_online-2018-v4.pdf",
    "FY2016": "https://files.bacb.co.uk/production/files/BACB_AnnualReport_online-2017.pdf",
    "FY2015": "https://files.bacb.co.uk/production/files/Report-Financials-2015-FINAL-18032016.pdf",
    "FY2014": "https://files.bacb.co.uk/production/files/Annual-Report-2014-Final.pdf",
    # FY2013: no longer hosted on bacb.co.uk's own file server (confirmed 404 on the same filename pattern as
    # FY2014's "Annual-Report-2014-Final.pdf") - sourced instead from Companies House's filing history, the
    # Bank's own statutory accounts filing made up to 31 December 2013 (filed 18 Mar 2014, company 01047302).
    "FY2013": "https://find-and-update.company-information.service.gov.uk/company/01047302/filing-history/"
              "MzA5NjQ2MjMzMmFkaXF6a2N4/document?format=pdf&download=0",
}
P3_URL = {
    "FY2025": "https://files.bacb.co.uk/production/files/BACB_Pillar3_YE2025web-03.pdf",
    "FY2024": "https://files.bacb.co.uk/production/files/BACB_Pillar3_YE2024web-05.pdf",
    "FY2023": "https://files.bacb.co.uk/production/files/BACB_Pillar3YE2023-03-002.pdf",
    "FY2022": "https://files.bacb.co.uk/production/files/BACB_Pillar3YE2022-1.pdf",
    "FY2021": "https://files.bacb.co.uk/production/files/BACB_Pillar3-2021_v3.pdf",
    "FY2019": "https://files.bacb.co.uk/production/files/2019-Pillar-3.pdf",
    "FY2018": "https://files.bacb.co.uk/production/files/Pillar-3-2018_Final-secured.pdf",
    "FY2017": "https://files.bacb.co.uk/production/files/Pillar-3-2017-FINAL-24-May-2018.pdf",
    "FY2016": "https://files.bacb.co.uk/production/files/Pillar-3-2016-FINAL-June17.pdf",
    "FY2015": "https://files.bacb.co.uk/production/files/2015-Pillar-3-secured.pdf",
    "FY2014": "https://files.bacb.co.uk/production/files/2014-Pillar-3-secured.pdf",
    # FY2020 has no standalone Pillar 3 document (confirmed via full Wayback Machine domain-wide CDX search -
    # no 2020-labelled Pillar 3 PDF was ever published); sourced from FY2021's own comparative column instead.
}

ENTITY_NOTE = (
    "British Arab Commercial Bank PLC (\"BACB\"), company 01047302 (incorporated 1972 as UBAF Limited, "
    "renamed British Arab Commercial Bank Limited 1996, re-registered as a public company 2009), FRN 204564. "
    "Owned by a consortium: Libyan Foreign Bank 85.95% (wholly owned by the Central Bank of Libya), Banque "
    "Exterieure d'Algerie 7.025%, Banque Centrale Populaire (Morocco) 7.025%. Single UK entity, no "
    "subsidiaries/associates, no prudential consolidation. Does NOT take the FRS 101/102 cash-flow exemption - "
    "full Statement of Cash Flow every year. GBP throughout, no FX conversion needed. Companies House status: "
    "Active, no going-concern issues found in any of the 5 Annual Reports (unqualified audits throughout).\n\n"
    "RESTATEMENTS: this bank's own cash flow comparatives shift modestly between report vintages (e.g. FY2021's "
    "\"Net cash gained from operating activities\" is 189,594 in the 2021 report's own figures vs 189,407 in "
    "2022's comparative; FY2024's is 227,828 in 2024's own report vs 227,636 in 2025's comparative) - each "
    "year's column here uses that year's own originally-published report, per project convention, not a later "
    "report's restated comparative.\n\n"
    "HISTORICAL DEPTH (FY2014-FY2020, added under HD-051, capped at FY2014 project-wide by 2026-09-05 user "
    "decision - the Bank's own archive goes back further but pre-CRD IV/Basel III Pillar 3 data isn't "
    "comparable and 2008-2012 crisis-era data is out of scope): FY2014's own report states Net pension "
    "liability GBP2,614k; FY2015's own report's FY2014 comparative restates this to GBP3,268k, with an exactly "
    "offsetting GBP654k reduction in FY2014's 'Deferred taxation' comparative (GBP1,183k in FY2014's own report "
    "vs GBP529k in FY2015's FY2014 comparative) - Total liabilities/equity unaffected either way, a reclass "
    "between two liability lines, not a genuine balance change - FY2014's own figures for both lines are used "
    "here, per this same convention. A similar small GBP38k reclass between Retained earnings and the Fair "
    "Value reserve exists between FY2020's own closing equity balance and FY2021's own opening balance (Total "
    "equity unaffected), shown as an explicit reclassification row at that transition, same as the other such "
    "reclasses already noted below. IFRS 9 replaced IAS 39 from 1 "
    "January 2018: FY2014-FY2017's own Balance Sheets have no 'Fair Value reserve' line (an 'AFS reserve' "
    "instead, renamed at IFRS 9 transition); FY2018's own report shows the transition adjustment "
    "(GBP7,447k impairment reclass + GBP1,288k DTA impact) as an explicit restated-opening-balance line "
    "between the FY2017 closing and FY2018 opening equity balances, shown as such below. FY2018 was a "
    "large loss year (GBP35,308k loss) driven by the IFRS 9 day-1 impairment build and a GBP59,043k "
    "allowance for credit losses charge - a genuine result, not a data error.\n\n"
    "HISTORICAL DEPTH FY2013 (added under HD-072, statutory statements only - Pillar 3/Asset Quality/RWA "
    "Breakdown untouched, per that ticket's scope): sourced from Companies House, not bacb.co.uk (no FY2013 "
    "Annual Report PDF found on the Bank's own file server - only FY2014 onward). FY2013's own filed accounts "
    "state Loans and advances to customers GBP456,896k and a combined Debt securities/Equity shares/Shares in "
    "bank undertakings total of GBP760,316k (GBP746,475k + GBP13,841k + GBP0k, shown here as 'Financial "
    "investments' to match later years' single-line presentation); FY2014's own report's FY2013 comparative "
    "column restates these to GBP450,839k and GBP766,373k respectively - an exact GBP6,057k reclass between the "
    "two lines, Total assets unaffected (GBP2,402,148k either way). FY2013's own originally-filed figures are "
    "used here, per this same convention."
)

CASH_FLOW_SOURCES = (
    "Sources - British Arab Commercial Bank PLC's own Statement of Cash Flow, each year from that year's own "
    "Annual Report (not a later report's restated comparative):\n"
    f"FY2025: Annual Report YE2025, pp.65-66 - {AR_URL['FY2025']}\n"
    f"FY2024: Annual Report YE2024, pp.59-60 - {AR_URL['FY2024']}\n"
    f"FY2023: Annual Report YE2023, p.60 - {AR_URL['FY2023']}\n"
    f"FY2022: Annual Report YE2022, p.56 - {AR_URL['FY2022']}\n"
    f"FY2021: Annual Report YE2021, p.48 - {AR_URL['FY2021']}\n"
    f"FY2020: Annual Report YE2020, p.2.4 - {AR_URL['FY2020']}\n"
    f"FY2019: Annual Report YE2019, p.2.4 - {AR_URL['FY2019']}\n"
    f"FY2018: Annual Report YE2018, p.2.4 - {AR_URL['FY2018']}\n"
    f"FY2017: Annual Report (filename says 2018, cover confirms FY2017), p.31 - {AR_URL['FY2017']}\n"
    f"FY2016: Annual Report (filename says 2017, cover confirms FY2016), p.30 - {AR_URL['FY2016']}\n"
    f"FY2015: Annual Report YE2015, p.31 - {AR_URL['FY2015']}\n"
    f"FY2014: Annual Report YE2014, p.30 - {AR_URL['FY2014']}\n"
    f"FY2013: Full accounts made up to 31 December 2013, filed with Companies House 18 Mar 2014, p.25 (Statement "
    f"of Cash Flow) - {AR_URL['FY2013']}\n\n"
    + ENTITY_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - British Arab Commercial Bank PLC Pillar 3 Disclosures, UK KM1 Key Metrics template:\n"
        f"FY2025: 2025 Pillar 3 Disclosures, p.6 (own year) - {P3_URL['FY2025']}\n"
        f"FY2024: 2024 Pillar 3 Disclosures, p.6 (own year) - {P3_URL['FY2024']}\n"
        f"FY2023: 2023 Pillar 3 Disclosures, p.6 (own year) - {P3_URL['FY2023']}\n"
        f"FY2022: 2022 Pillar 3 Disclosures, p.7 (own year) - {P3_URL['FY2022']}\n"
        f"FY2021: sourced from the 2022 Pillar 3 Disclosures' own FY2021 comparative column, p.7 - "
        f"{P3_URL['FY2022']} (the 2021 Pillar 3 document predates the modern UK KM1 template and has no "
        "equivalent single table - same approach as Aldermore/BLME/Bank of Ireland UK elsewhere in this project).\n"
        f"FY2020: sourced from the 2021 Pillar 3 Disclosures' own FY2020 comparative column (Table 9/10/25) - "
        f"{P3_URL['FY2021']} (no standalone FY2020 Pillar 3 document exists - confirmed via a full "
        "Wayback Machine CDX domain search for bacb.co.uk, which shows FY2019- and FY2021-labelled documents "
        "but no FY2020 one).\n"
        f"FY2019: 2019 Pillar 3 Disclosures (own year), Table 9 (LCR)/Table 10 (capital)/p.33 (leverage) - "
        f"{P3_URL['FY2019']}\n"
        f"FY2018: 2018 Pillar 3 Disclosures (own year), Table 10 (capital)/p.31 (leverage) - {P3_URL['FY2018']}\n"
        f"FY2017: 2017 Pillar 3 Disclosures (own year), Table 10 (capital)/p.31 (leverage) - {P3_URL['FY2017']}\n"
        f"FY2016: 2016 Pillar 3 Disclosures (own year), Table 7 (capital)/p.30 (leverage) - {P3_URL['FY2016']}\n"
        f"FY2015: 2015 Pillar 3 Disclosures (own year), Table 8 (capital)/Table 12 (leverage exposure) - "
        f"{P3_URL['FY2015']}\n"
        f"FY2014: 2014 Pillar 3 Disclosures (own year), Table 8 (capital) - {P3_URL['FY2014']} (no leverage "
        "ratio disclosed - the leverage ratio requirement first appears in BACB's own Pillar 3 Disclosures "
        "from FY2015; no LCR % disclosed - LCR appears only as an undisclosed chart image in FY2014-FY2018's "
        "own documents, with a first extractable numeric value from FY2019's own report).\n"
        + (extra + "\n" if extra else "")
    )


bw = BankWorkbook(bank_name="British Arab Commercial Bank PLC", years=Y_CORE, year_label=YEAR_LABEL, header_color="0E7C9E")

STATEMENTS_NOTE = (
    "Each year's Balance Sheet/P&L/Equity column uses that year's own originally-published Annual Report, not a "
    "later report's restated comparative (same convention as the Cash Flow Statement - see its own note). This "
    "surfaces several genuine, small restatements between vintages, all left as originally reported and flagged "
    "here rather than silently blended:\n"
    "- FY2023's own report (AR2023) states Profit for the year GBP27,875k / Total comprehensive income GBP30,511k; "
    "the FY2024 report's FY2023 comparative restates these to GBP29,044k / GBP30,527k (AR2024 Note 2 states this "
    "reclassification affected both the 2023 SOCI and SOFP - not detailed further in that report).\n"
    "- FY2023's own report's closing equity is Retained earnings GBP120,650k / Fair value reserve -GBP1,921k; the "
    "FY2024 report's own 1 January 2024 opening balance is GBP121,819k / -GBP3,090k for the same two lines (Total "
    "equity and Other reserves total unaffected - a GBP1,169k reclass between the two reserve lines only). Shown "
    "here as an explicit 'Reclassification between reserves (per FY2024 report)' row at FY2024's opening.\n"
    "- A smaller, similar GBP42k reclass between Retained earnings and Fair value reserve exists between FY2021's "
    "own closing balance and FY2022's own opening balance (Total equity unaffected); shown the same way.\n"
    "- FY2021's own report's Net operating income (GBP53,466k) and Other operating income (GBP1,519k) differ "
    "immaterially (GBP21k) from the FY2022 report's own FY2021 comparative (GBP53,487k / GBP1,540k); FY2021's own "
    "figures are used here.\n"
    "- FY2021's own report's Total assets (GBP2,782,543k, incl. Net pension asset GBP5,480k and Deferred tax "
    "liabilities GBP539k) differs from the FY2022 report's own FY2021 comparative (GBP2,782,004k) by the same "
    "amount - FY2021's own figures are used here.\n"
    "- Within FY2023's own equity statement, an 'Other Fair Value adjustments' GBP16k line pushes the equity "
    "statement's own Total comprehensive income for FY2023 (GBP30,527k) GBP16k above the P&L's own Total "
    "comprehensive income for FY2023 (GBP30,511k) - a small internal inconsistency present in the Bank's own "
    "audited report, not introduced here.\n\n"
    "Presentation changes: FY2025/FY2024's P&L splits interest income/expense into 'calculated under the "
    "effective interest method' vs 'other method'; FY2023/FY2022/FY2021 report single combined interest income/"
    "expense lines. FY2021's P&L has no 'Revaluation of property, plant & equipment' OCI line (adopted from "
    "FY2022). Balance sheet: 'Deferred tax assets' appears as its own line only FY2023 (nil) and FY2022 "
    "(GBP3,561k); 'Corporation tax receivable/payable' and 'Deferred tax liabilities' lines appear inconsistently "
    "across years depending on the sign of that year's balance - left blank where a report has no equivalent line "
    "that year, not assumed zero."
)

STATEMENTS_SOURCES = (
    "Sources - British Arab Commercial Bank PLC's own Statement of Comprehensive Income / Statement of Financial "
    "Position / Statement of Changes in Equity, each year from that year's own Annual Report:\n"
    f"FY2025: Annual Report YE2025, pp.62-64 - {AR_URL['FY2025']}\n"
    f"FY2024: Annual Report YE2024, pp.56-58 - {AR_URL['FY2024']}\n"
    f"FY2023: Annual Report YE2023, pp.57-59 - {AR_URL['FY2023']}\n"
    f"FY2022: Annual Report YE2022, pp.2.2-2.4 - {AR_URL['FY2022']}\n"
    f"FY2021: Annual Report YE2021, pp.2.2-2.4 - {AR_URL['FY2021']}\n"
    f"FY2020: Annual Report YE2020, pp.2.2-2.3 - {AR_URL['FY2020']}\n"
    f"FY2019: Annual Report YE2019, pp.2.2-2.3 - {AR_URL['FY2019']}\n"
    f"FY2018: Annual Report YE2018, pp.2.2-2.3 - {AR_URL['FY2018']}\n"
    f"FY2017: Annual Report (filename says 2018, cover/profit figures confirm FY2017), pp.28-30 - {AR_URL['FY2017']}\n"
    f"FY2016: Annual Report (filename says 2017, cover confirms FY2016), pp.27-29 - {AR_URL['FY2016']}\n"
    f"FY2015: Annual Report YE2015, pp.28-30 - {AR_URL['FY2015']}\n"
    f"FY2014: Annual Report YE2014, pp.27-29 - {AR_URL['FY2014']}\n"
    f"FY2013: Full accounts made up to 31 December 2013, filed with Companies House 18 Mar 2014, pp.22-24 "
    f"(Statement of Comprehensive Income / Statement of Financial Position / Statement of Changes in Equity) - "
    f"{AR_URL['FY2013']}\n\n"
    + STATEMENTS_NOTE
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet (Statement of Financial Position)
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash, notes and coins",
     {"FY2025": 0, "FY2024": 1, "FY2023": 1, "FY2022": 0, "FY2021": 218, "FY2020": 219, "FY2019": 89, "FY2018": 110,
      "FY2017": 143, "FY2016": 87, "FY2015": 323, "FY2014": 633, "FY2013": 223}),
    ("DATA", "Derivatives",
     {"FY2025": 2008, "FY2024": 1770, "FY2023": 661, "FY2022": 1344, "FY2021": 616, "FY2020": 1081, "FY2019": 751,
      "FY2018": 1249, "FY2017": 547, "FY2016": 769, "FY2015": 181, "FY2014": 567, "FY2013": 1271}),
    ("DATA", "Reverse repurchase agreements",
     {"FY2025": 25147, "FY2024": 210601, "FY2023": 86937, "FY2022": 236927, "FY2021": 215824}),
    ("DATA", "Loans and advances to banks",
     {"FY2025": 1570302, "FY2024": 1271347, "FY2023": 855620, "FY2022": 755184, "FY2021": 588843,
      "FY2020": 616563, "FY2019": 1189720, "FY2018": 997428, "FY2017": 1017510, "FY2016": 759716,
      "FY2015": 910561, "FY2014": 1293790, "FY2013": 1156909}),
    ("DATA", "Loans and advances to customers",
     {"FY2025": 353562, "FY2024": 387260, "FY2023": 388567, "FY2022": 463780, "FY2021": 484536,
      "FY2020": 582529, "FY2019": 651514, "FY2018": 1081161, "FY2017": 1068589, "FY2016": 864311,
      "FY2015": 685680, "FY2014": 471375, "FY2013": 456896}),
    ("DATA", "Financial investments",
     {"FY2025": 1317406, "FY2024": 1427440, "FY2023": 1621748, "FY2022": 1695000, "FY2021": 1456288,
      "FY2020": 1306280, "FY2019": 891682, "FY2018": 1774166, "FY2017": 788066, "FY2016": 1288442,
      "FY2015": 1399383, "FY2014": 1122262,
      # FY2013's own report: Debt securities 746,475 + Equity shares and investments 13,841 + Shares in bank
      # undertakings 0 = 760,316 (FY2014's own restated FY2013 comparative shows 766,373 with an offsetting
      # -6,057 shift in Loans and advances to customers - FY2013's own originally-filed figures used, see note).
      "FY2013": 760316}),
    ("DATA", "Prepayments, accrued income and other debtors",
     {"FY2025": 14721, "FY2024": 8497, "FY2023": 10424, "FY2022": 3014, "FY2021": 3437, "FY2020": 14370,
      "FY2019": 22181, "FY2018": 16815, "FY2017": 62573, "FY2016": 11016, "FY2015": 10562, "FY2014": 13877,
      "FY2013": 15627}),
    ("DATA", "Corporation tax receivable",
     {"FY2023": 947, "FY2022": 223, "FY2019": 214, "FY2018": 677, "FY2016": 1358, "FY2015": 4030, "FY2014": 2610}),
    ("DATA", "Deferred tax assets", {"FY2023": 0, "FY2022": 3561, "FY2019": 994, "FY2018": 2914, "FY2016": 1069}),
    ("DATA", "Property, plant and equipment",
     {"FY2025": 30946, "FY2024": 31014, "FY2023": 29839, "FY2022": 27271, "FY2021": 19719, "FY2020": 12120,
      "FY2019": 11682, "FY2018": 8378, "FY2017": 8291, "FY2016": 8488, "FY2015": 8678, "FY2014": 8993,
      "FY2013": 8875}),
    ("DATA", "Intangible assets",
     {"FY2025": 2305, "FY2024": 2937, "FY2023": 4566, "FY2022": 6222, "FY2021": 7582, "FY2020": 8980,
      "FY2019": 10491, "FY2018": 10954, "FY2017": 6796, "FY2016": 4008, "FY2015": 1897, "FY2014": 2310,
      "FY2013": 2031}),
    ("DATA", "Net pension asset", {"FY2025": 2353, "FY2024": 2599, "FY2023": 2617, "FY2022": 2219, "FY2021": 5480,
                                    "FY2020": 756}),
    ("TOTAL", "Total assets",
     {"FY2025": 3318750, "FY2024": 3343466, "FY2023": 3001927, "FY2022": 3194745, "FY2021": 2782543,
      "FY2020": 2542898, "FY2019": 2779318, "FY2018": 3893852, "FY2017": 2952856, "FY2016": 2939264,
      "FY2015": 3021295, "FY2014": 2916417, "FY2013": 2402148}),

    ("SECTION", "Liabilities", {}),
    ("DATA", "Derivatives",
     {"FY2025": 728, "FY2024": 1056, "FY2023": 46, "FY2022": 507, "FY2021": 1268, "FY2020": 5582, "FY2019": 3093,
      "FY2018": 1119, "FY2017": 1271, "FY2016": 1960, "FY2015": 806, "FY2014": 1342, "FY2013": 1014}),
    ("DATA", "Deposits from banks",
     {"FY2025": 2110653, "FY2024": 2218623, "FY2023": 1960559, "FY2022": 2144470, "FY2021": 1876756,
      "FY2020": 1691853, "FY2019": 1836945, "FY2018": 3047548, "FY2017": 2095638, "FY2016": 2019036,
      "FY2015": 2107305, "FY2014": 1938136, "FY2013": 1452278}),
    ("DATA", "Other deposits",
     {"FY2025": 828120, "FY2024": 758949, "FY2023": 699119, "FY2022": 737763, "FY2021": 604750, "FY2020": 549829,
      "FY2019": 674607, "FY2018": 585058, "FY2017": 555556, "FY2016": 622896, "FY2015": 627581, "FY2014": 686071,
      "FY2013": 674490}),
    ("DATA", "Other liabilities, accruals and deferred income",
     {"FY2025": 29930, "FY2024": 29369, "FY2023": 33274, "FY2022": 27080, "FY2021": 17530, "FY2020": 25582,
      "FY2019": 14168, "FY2018": 16044, "FY2017": 10019, "FY2016": 7959, "FY2015": 10295, "FY2014": 24383,
      "FY2013": 16281}),
    ("DATA", "Corporation tax payable",
     {"FY2025": 327, "FY2024": 810, "FY2021": 900, "FY2020": 794, "FY2017": 339, "FY2013": 1264}),
    ("DATA", "Deferred tax liabilities",
     {"FY2025": 1646, "FY2024": 2821, "FY2023": 1797, "FY2021": 539, "FY2020": 15, "FY2014": 1183, "FY2013": 179}),
    ("DATA", "Net pension liability",
     {"FY2019": 741, "FY2018": 584, "FY2017": 898, "FY2016": 3607, "FY2015": 1831, "FY2014": 2614, "FY2013": 2673}),
    ("DATA", "Subordinated liabilities",
     {"FY2025": 69006, "FY2024": 74226, "FY2023": 74554, "FY2022": 77659, "FY2021": 70514, "FY2020": 72036,
      "FY2019": 71870, "FY2018": 75321, "FY2017": 72302, "FY2016": 75413, "FY2015": 63307, "FY2014": 60519,
      "FY2013": 57141}),
    ("TOTAL", "Total liabilities",
     {"FY2025": 3040410, "FY2024": 3085854, "FY2023": 2769349, "FY2022": 2987479, "FY2021": 2572257,
      "FY2020": 2345691, "FY2019": 2601424, "FY2018": 3725674, "FY2017": 2736023, "FY2016": 2730871,
      "FY2015": 2811125, "FY2014": 2714248, "FY2013": 2205320}),

    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital",
     {"FY2025": 108069, "FY2024": 107097, "FY2023": 106377, "FY2022": 105592, "FY2021": 104357, "FY2020": 104357,
      "FY2019": 104357, "FY2018": 104357, "FY2017": 104149, "FY2016": 104149, "FY2015": 104149, "FY2014": 79453,
      "FY2013": 79453}),
    ("DATA", "Capital redemption reserve",
     {"FY2025": 4104, "FY2024": 4104, "FY2023": 4104, "FY2022": 4104, "FY2021": 4104, "FY2020": 4104,
      "FY2019": 4104, "FY2018": 4104, "FY2017": 4104, "FY2016": 4104, "FY2015": 4104, "FY2014": 4104,
      "FY2013": 4104}),
    ("DATA", "Other reserves",
     {"FY2025": 166167, "FY2024": 146411, "FY2023": 122097, "FY2022": 97570, "FY2021": 101825, "FY2020": 88746,
      "FY2019": 69433, "FY2018": 59717, "FY2017": 108580, "FY2016": 100140, "FY2015": 101917, "FY2014": 118612,
      "FY2013": 113271}),
    ("TOTAL", "Total equity",
     {"FY2025": 278340, "FY2024": 257612, "FY2023": 232578, "FY2022": 207266, "FY2021": 210286, "FY2020": 197207,
      "FY2019": 177894, "FY2018": 168178, "FY2017": 216833, "FY2016": 208393, "FY2015": 210170, "FY2014": 202169,
      "FY2013": 196828}),
    ("TOTAL", "Total liabilities and equity",
     {"FY2025": 3318750, "FY2024": 3343466, "FY2023": 3001927, "FY2022": 3194745, "FY2021": 2782543,
      "FY2020": 2542898, "FY2019": 2779318, "FY2018": 3893852, "FY2017": 2952856, "FY2016": 2939264,
      "FY2015": 3021295, "FY2014": 2916417, "FY2013": 2402148}),
]

bw.add_balance_sheet_sheet(
    title="British Arab Commercial Bank PLC — Statement of Financial Position",
    subtitle="Bank entity basis (single UK entity, no subsidiaries/associates). GBP throughout, no FX conversion.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=460,
    unit_suffix=" (£'000)",
    years=YEARS,
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss (Statement of Comprehensive Income)
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest and similar income (or: calculated under effective interest method)",
     {"FY2025": 130031, "FY2024": 144622, "FY2023": 168035, "FY2022": 71950, "FY2021": 33156, "FY2020": 47746,
      "FY2019": 77416, "FY2018": 81564, "FY2017": 61614, "FY2016": 47872, "FY2015": 36234, "FY2014": 35464,
      "FY2013": 32643}),
    ("DATA", "Interest income calculated using other method", {"FY2025": 34805, "FY2024": 38274}),
    ("DATA", "Interest expense and similar charges (or: calculated under effective interest method)",
     {"FY2025": -101087, "FY2024": -112061, "FY2023": -103747, "FY2022": -38301, "FY2021": -12248, "FY2020": -24196,
      "FY2019": -47067, "FY2018": -44358, "FY2017": -33196, "FY2016": -25397, "FY2015": -18362, "FY2014": -14195,
      "FY2013": -17379}),
    ("DATA", "Interest expense calculated using other method", {"FY2025": -325, "FY2024": -192}),
    ("TOTAL", "Net interest income",
     {"FY2025": 63424, "FY2024": 70643, "FY2023": 64288, "FY2022": 33649, "FY2021": 20908, "FY2020": 23550,
      "FY2019": 30349, "FY2018": 37206, "FY2017": 28418, "FY2016": 22475, "FY2015": 17872, "FY2014": 21269,
      "FY2013": 15264}),
    ("DATA", "Fee and commission income",
     {"FY2025": 25974, "FY2024": 26821, "FY2023": 24098, "FY2022": 21653, "FY2021": 17502, "FY2020": 16971,
      "FY2019": 19488, "FY2018": 22667, "FY2017": 15609, "FY2016": 12335, "FY2015": 13658, "FY2014": 18880,
      "FY2013": 21084}),
    ("DATA", "Fee and commission expense",
     {"FY2025": -7360, "FY2024": -6431, "FY2023": -6977, "FY2022": -4035, "FY2021": -1599, "FY2020": -1269,
      "FY2019": -1098, "FY2018": -372, "FY2017": -325, "FY2016": -357, "FY2015": -443, "FY2014": -643,
      "FY2013": -652}),
    ("TOTAL", "Net fee and commission income",
     {"FY2025": 18614, "FY2024": 20390, "FY2023": 17121, "FY2022": 17618, "FY2021": 15903, "FY2020": 15702,
      "FY2019": 18390, "FY2018": 22295, "FY2017": 15284, "FY2016": 11978, "FY2015": 13215, "FY2014": 18237,
      "FY2013": 20432}),
    ("DATA", "Net trading (and other) income",
     {"FY2025": 9424, "FY2024": 6549, "FY2023": 5546, "FY2022": 6522, "FY2021": 3393, "FY2020": 2797,
      "FY2019": 13870, "FY2018": 5358, "FY2017": 4730, "FY2016": 6157, "FY2015": 6226, "FY2014": 6958,
      "FY2013": 7875}),
    ("DATA", "Other operating income/(expense)",
     {"FY2025": 1301, "FY2024": 1068, "FY2023": 901, "FY2022": -356, "FY2021": 1519, "FY2020": 2742,
      "FY2019": 1415, "FY2018": -23, "FY2017": 4964, "FY2016": 2129, "FY2015": 1197, "FY2014": 1612,
      "FY2013": 596}),
    ("TOTAL", "Operating income before allowance for credit losses",
     {"FY2025": 92763, "FY2024": 98650, "FY2023": 87856, "FY2022": 57433, "FY2021": 41723, "FY2020": 44791,
      "FY2019": 64024, "FY2018": 64836, "FY2017": 53396, "FY2016": 42739, "FY2015": 38510, "FY2014": 48076,
      "FY2013": 44167}),
    ("DATA", "Allowance for credit losses (pre-2018: 'Loan impairments', single net figure)",
     {"FY2025": -2313, "FY2024": -3992, "FY2023": -479, "FY2022": -3306, "FY2021": -1245, "FY2020": -6902,
      "FY2019": -18558, "FY2018": -59043, "FY2017": -10131, "FY2016": -7122, "FY2015": -18804, "FY2014": -4962,
      "FY2013": -2482}),
    ("DATA", "Reversal of allowances booked in previous periods",
     {"FY2025": 5554, "FY2024": 5633, "FY2023": 2623, "FY2022": 1825, "FY2021": 12441, "FY2020": 13754}),
    ("DATA", "Recoveries of amounts written off in previous periods",
     {"FY2024": 0, "FY2023": 1, "FY2022": 4, "FY2021": 547, "FY2020": 1293}),
    ("TOTAL", "Net reversals/(allowances) for credit losses",
     {"FY2025": 3241, "FY2024": 1641, "FY2023": 2145, "FY2022": -1477, "FY2021": 11743, "FY2020": 8145,
      "FY2019": -18558, "FY2018": -59043, "FY2017": -10131, "FY2016": -7122, "FY2015": -18804, "FY2014": -4962,
      "FY2013": -2482}),
    ("TOTAL", "Net operating income",
     {"FY2025": 96004, "FY2024": 100291, "FY2023": 90001, "FY2022": 55956, "FY2021": 53466, "FY2020": 52936,
      "FY2019": 45466, "FY2018": 5793, "FY2017": 43265, "FY2016": 35617, "FY2015": 19706, "FY2014": 43114,
      "FY2013": 41685}),
    ("DATA", "Administrative expenses",
     {"FY2025": -64363, "FY2024": -62082, "FY2023": -53594, "FY2022": -42031, "FY2021": -38763, "FY2020": -37014,
      "FY2019": -37388, "FY2018": -38018, "FY2017": -36000, "FY2016": -33038, "FY2015": -34777, "FY2014": -37603,
      "FY2013": -23837}),
    ("DATA", "Regulatory charge", {"FY2018": -3141}),
    ("TOTAL", "Profit before income tax",
     {"FY2025": 31641, "FY2024": 38209, "FY2023": 36407, "FY2022": 13925, "FY2021": 14703, "FY2020": 15922,
      "FY2019": 8078, "FY2018": -35366, "FY2017": 7265, "FY2016": 2579, "FY2015": -15071, "FY2014": 5511,
      "FY2013": 17848}),
    ("DATA", "Income tax credit/(charge)",
     {"FY2025": -7514, "FY2024": -9454, "FY2023": -8532, "FY2022": 1175, "FY2021": -1668, "FY2020": -1494,
      "FY2019": -450, "FY2018": 58, "FY2017": -440, "FY2016": 140, "FY2015": 566, "FY2014": -782,
      "FY2013": -4081}),
    ("TOTAL", "Profit for the year",
     {"FY2025": 24127, "FY2024": 28755, "FY2023": 27875, "FY2022": 15100, "FY2021": 13035, "FY2020": 14428,
      "FY2019": 7628, "FY2018": -35308, "FY2017": 6825, "FY2016": 2719, "FY2015": -14505, "FY2014": 4729,
      "FY2013": 13767}),

    ("SECTION", "Other comprehensive income/(expense), net of tax", {}),
    ("DATA", "Remeasurement of defined benefit liability",
     {"FY2025": -219, "FY2024": -1558, "FY2023": -1257, "FY2022": -4161, "FY2021": 3231, "FY2020": 298,
      "FY2019": -1633, "FY2018": -1075, "FY2017": 1277, "FY2016": -3250, "FY2015": 141, "FY2014": -1060,
      "FY2013": 299}),
    ("DATA", "Revaluation gain/(loss) on equity investments designated at FVOCI",
     {"FY2025": -244, "FY2024": 61, "FY2023": -1048, "FY2022": -376, "FY2021": -138, "FY2020": -48, "FY2019": -139,
      "FY2018": -928}),
    ("DATA", "Disposal of equity investment designated at FVOCI", {"FY2024": -161}),
    ("DATA", "Revaluation gain/(loss) on property, plant & equipment",
     {"FY2025": 871, "FY2024": 778, "FY2023": -3359, "FY2022": 7851}),
    ("DATA", "Related tax (items not reclassified to P&L)",
     {"FY2025": 1379, "FY2024": -420, "FY2023": 1109, "FY2022": -1153, "FY2021": -588, "FY2020": -34, "FY2019": 303,
      "FY2018": 360, "FY2017": -217, "FY2016": 494, "FY2015": -28, "FY2014": -14, "FY2013": -166}),
    ("DATA", "Change in fair value for debt securities designated at FVOCI",
     {"FY2025": 786, "FY2024": 2662, "FY2023": 9036, "FY2022": -14178, "FY2021": -3924, "FY2020": 2575,
      "FY2019": 4094, "FY2018": -5950}),
    ("DATA", "Other Fair value adjustments", {"FY2023": 16}),
    ("DATA", "Credit loss on debt securities at FVOCI transferred to P&L",
     {"FY2025": -128, "FY2024": -18, "FY2023": -79, "FY2022": -57, "FY2021": -218, "FY2020": 251, "FY2019": -177,
      "FY2018": 445}),
    ("DATA", "FV gains on debt securities at FVOCI transferred to income upon derecognition",
     {"FY2025": 775, "FY2024": 508, "FY2023": 397, "FY2022": -646, "FY2021": 1130, "FY2020": 2117, "FY2019": 1156,
      "FY2018": 373}),
    ("DATA", "Related tax (items that may be reclassified to P&L)",
     {"FY2025": -391, "FY2024": -793, "FY2023": -2163, "FY2022": 3349, "FY2021": 551, "FY2020": -274,
      "FY2019": -1516, "FY2018": 1085}),
    ("DATA", "Change in fair value of available for sale financial assets (pre-2018, AFS reserve)",
     {"FY2017": 5137, "FY2016": 3522, "FY2015": -3571, "FY2014": -358, "FY2013": 976}),
    ("DATA", "Fair value (losses)/gains on AFS assets transferred to income (pre-2018, AFS reserve)",
     {"FY2017": -4587, "FY2016": -5279, "FY2015": 690, "FY2014": 2461, "FY2013": -588}),
    ("DATA", "Related tax (pre-2018, AFS reserve items)",
     {"FY2017": 5, "FY2016": 17, "FY2015": 578, "FY2014": -417, "FY2013": -30}),
    ("TOTAL", "Other comprehensive income/(expense) for the year, net of tax",
     {"FY2025": 2829, "FY2024": 1059, "FY2023": 2636, "FY2022": -9371, "FY2021": 44, "FY2020": 4885, "FY2019": 2088,
      "FY2018": -5690, "FY2017": 1615, "FY2016": -4496, "FY2015": -2190, "FY2014": 612, "FY2013": 491}),
    ("TOTAL", "Total comprehensive income for the year",
     {"FY2025": 26956, "FY2024": 29814, "FY2023": 30511, "FY2022": 5729, "FY2021": 13079, "FY2020": 19313,
      "FY2019": 9716, "FY2018": -40998, "FY2017": 8440, "FY2016": -1777, "FY2015": -16695, "FY2014": 5341,
      "FY2013": 14258}),
]

bw.add_income_statement_sheet(
    title="British Arab Commercial Bank PLC — Statement of Comprehensive Income",
    subtitle="Bank entity basis (single UK entity, no subsidiaries/associates). GBP throughout, no FX conversion.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=460,
    unit_suffix=" (£'000)",
    years=YEARS,
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity (chronological, oldest to newest)
# ---------------------------------------------------------------
equity_changes_rows = [
    ("TOTAL", "Balance at 31 December 2012 (per FY2013's own report)",
     (79453, 4104, 103050, None, 3163, 189770)),
    ("DATA", "Profit for the year (FY2013)", (None, None, 13767, None, None, 13767)),
    ("DATA", "Other comprehensive income (FY2013)", (None, None, 133, None, 358, 491)),
    ("DATA", "Dividend relating to 2012, paid in FY2013", (None, None, -7200, None, None, -7200)),
    ("TOTAL", "Balance at 1 January 2014 (= 31 December 2013, per FY2014's own report)",
     (79453, 4104, 109750, None, 3521, 196828)),
    ("DATA", "Profit for the year (FY2014)", (None, None, 4729, None, None, 4729)),
    ("DATA", "Other comprehensive income/(expense) (FY2014)", (None, None, -1074, None, 1686, 612)),
    ("TOTAL", "Balance at 31 December 2014", (79453, 4104, 113405, None, 5207, 202169)),
    ("DATA", "Loss for the year (FY2015)", (None, None, -14505, None, None, -14505)),
    ("DATA", "Other comprehensive income/(expense) (FY2015)", (None, None, 113, None, -2303, -2190)),
    ("DATA", "Issue of ordinary shares (FY2015)", (24696, None, None, None, None, 24696)),
    ("TOTAL", "Balance at 31 December 2015", (104149, 4104, 99013, None, 2904, 210170)),
    ("DATA", "Profit for the year (FY2016)", (None, None, 2719, None, None, 2719)),
    ("DATA", "Other comprehensive (loss) (FY2016)", (None, None, -2756, None, -1740, -4496)),
    ("TOTAL", "Balance at 31 December 2016", (104149, 4104, 98976, None, 1164, 208393)),
    ("DATA", "Profit for the year (FY2017)", (None, None, 6825, None, None, 6825)),
    ("DATA", "Other comprehensive income (FY2017)", (None, None, 1060, None, 555, 1615)),
    ("TOTAL", "Balance at 31 December 2017", (104149, 4104, 106861, None, 1719, 216833)),
    ("DATA", "IFRS 9 initial application - impairment adjustment (1 Jan 2018)", (None, None, -7447, None, None, -7447)),
    ("DATA", "IFRS 9 initial application - DTA impact (1 Jan 2018)", (None, None, 1288, None, None, 1288)),
    ("TOTAL", "Restated balance at 1 January 2018", (104149, 4104, 100702, None, 1719, 210674)),
    ("DATA", "Loss for the year (FY2018)", (None, None, -35308, None, None, -35308)),
    ("DATA", "Other comprehensive income/(expense) (FY2018)", (None, None, -892, None, -4798, -5690)),
    ("DATA", "Issue of ordinary shares (FY2018)", (208, None, -208, None, None, 0)),
    ("DATA", "Dividends (FY2018)", (None, None, -1498, None, None, -1498)),
    ("TOTAL", "Balance at 31 December 2018", (104357, 4104, 62796, None, -3079, 168178)),
    ("DATA", "Profit for the year (FY2019)", (None, None, 7628, None, None, 7628)),
    ("DATA", "Other comprehensive (loss)/income (FY2019)", (None, None, -1355, None, 3443, 2088)),
    ("TOTAL", "Balance at 31 December 2019", (104357, 4104, 69069, None, 364, 177894)),
    ("DATA", "Profit for the year (FY2020)", (None, None, 14428, None, None, 14428)),
    ("DATA", "Other comprehensive income (FY2020)", (None, None, 254, None, 4631, 4885)),
    ("TOTAL", "Balance at 31 December 2020", (104357, 4104, 83751, None, 4995, 197207)),
    ("DATA", "Reclassification between reserves (per FY2021 report's own opening balance)",
     (None, None, -38, None, 38, 0)),
    ("TOTAL", "Balance at 1 January 2021", (104357, 4104, 83713, 0, 5033, 197207)),
    ("DATA", "Profit for the year (FY2021)", (None, None, 13035, None, None, 13035)),
    ("DATA", "Other comprehensive income (FY2021)", (None, None, 2505, None, -2461, 44)),
    ("TOTAL", "Balance at 31 December 2021 (per FY2021's own report)", (104357, 4104, 99253, 0, 2572, 210286)),
    ("DATA", "Reclassification between reserves (per FY2022 report's own opening balance)",
     (None, None, 42, None, -42, 0)),
    ("TOTAL", "Balance at 1 January 2022 (per FY2022's own report)", (104357, 4104, 99295, 0, 2530, 210286)),
    ("DATA", "Profit for the year (FY2022)", (None, None, 15100, None, None, 15100)),
    ("DATA", "Reclassification between FV reserve and retained earnings", (None, None, 126, None, -110, 16)),
    ("DATA", "Other comprehensive (expense)/income (FY2022)", (None, None, -3727, 5888, -11532, -9371)),
    ("DATA", "Issue of share capital (FY2022)", (1235, None, None, None, None, 1235)),
    ("DATA", "Dividend paid (FY2022)", (None, None, -10000, None, None, -10000)),
    ("TOTAL", "Balance at 31 December 2022", (105592, 4104, 100794, 5888, -9112, 207266)),
    ("DATA", "Profit for the year (FY2023)", (None, None, 27875, None, None, 27875)),
    ("DATA", "Other Fair Value adjustments (FY2023)", (None, None, 16, None, None, 16)),
    ("DATA", "Other comprehensive (expense)/income (FY2023)", (None, None, -2035, -2520, 7191, 2636)),
    ("DATA", "Issue of share capital (FY2023)", (785, None, None, None, None, 785)),
    ("DATA", "Dividend paid (FY2023)", (None, None, -6000, None, None, -6000)),
    ("TOTAL", "Balance at 31 December 2023 (per FY2023's own report)", (106377, 4104, 120650, 3368, -1921, 232578)),
    ("DATA", "Reclassification between reserves (per FY2024 report's own opening balance)",
     (None, None, 1169, None, -1169, 0)),
    ("TOTAL", "Balance at 1 January 2024 (per FY2024's own report)", (106377, 4104, 121819, 3368, -3090, 232578)),
    ("DATA", "Profit for the year (FY2024)", (None, None, 28755, None, None, 28755)),
    ("DATA", "Other comprehensive (expense)/income (FY2024)", (None, None, -1883, 583, 2359, 1059)),
    ("DATA", "Issue of share capital (FY2024)", (720, None, None, None, None, 720)),
    ("DATA", "Dividend paid (FY2024)", (None, None, -5500, None, None, -5500)),
    ("TOTAL", "Balance at 31 December 2024", (107097, 4104, 143191, 3951, -731, 257612)),
    ("DATA", "Profit for the year (FY2025)", (None, None, 24127, None, None, 24127)),
    ("DATA", "Other comprehensive (expense)/income (FY2025)", (None, None, -402, 2189, 1042, 2829)),
    ("DATA", "Issue of share capital (FY2025)", (972, None, None, None, None, 972)),
    ("DATA", "Dividend paid (FY2025)", (None, None, -7200, None, None, -7200)),
    ("TOTAL", "Balance at 31 December 2025", (108069, 4104, 159716, 6140, 311, 278340)),
]

bw.add_equity_changes_sheet(
    title="British Arab Commercial Bank PLC — Statement of Changes in Equity",
    subtitle="Bank entity basis, £'000. Chronological roll-forward, oldest to newest. GBP throughout, no FX conversion.",
    headers=["Share capital", "Capital redemption reserve", "Retained earnings", "Revaluation reserve",
             "Fair Value reserve", "Total equity"],
    rows=equity_changes_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=64,
    source_height=460,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit before taxation",
     {"FY2025": 31641, "FY2024": 38209, "FY2023": 36407, "FY2022": 13925, "FY2021": 14703, "FY2020": 15922,
      "FY2019": 8078, "FY2018": -35366, "FY2017": 7265, "FY2016": 2579, "FY2015": -15071, "FY2014": 5511,
      "FY2013": 17848}),
    ("DATA", "Allowance for credit losses",
     {"FY2025": 2313, "FY2024": 3992, "FY2023": 479, "FY2022": 3306, "FY2021": 1245, "FY2020": 6902, "FY2019": 18558,
      "FY2018": 59043, "FY2017": 10131, "FY2016": 7122, "FY2015": 18804, "FY2014": 4962, "FY2013": 2482}),
    ("DATA", "Recoveries of allowance for credit losses",
     {"FY2025": -5554, "FY2024": -5633, "FY2023": -2623, "FY2022": -1825, "FY2021": -12441, "FY2020": -13754}),
    ("DATA", "Profit on realisation of equity shares and investments", {"FY2016": -3822, "FY2013": -309}),
    ("DATA", "Depreciation and amortisation",
     {"FY2025": 3229, "FY2024": 3214, "FY2023": 2904, "FY2022": 2753, "FY2021": 2544, "FY2020": 2444,
      "FY2019": 2519, "FY2018": 1024, "FY2017": 1401, "FY2016": 1694, "FY2015": 1477, "FY2014": 1355,
      "FY2013": 1128}),
    ("DATA", "(Loss)/gain on sale or impairment of property, plant and equipment",
     {"FY2025": -6, "FY2024": 3, "FY2023": 518, "FY2022": 28, "FY2021": 9, "FY2020": 81, "FY2018": 1101,
      "FY2017": 665, "FY2016": -50, "FY2015": 95, "FY2014": 676, "FY2013": 141}),
    ("DATA", "Other non-cash items included in net profit",
     {"FY2025": -1275, "FY2024": -34, "FY2023": 115, "FY2022": 366, "FY2021": -3, "FY2020": -151, "FY2019": -1035,
      "FY2018": 1731, "FY2017": -748, "FY2016": -332}),
    ("TOTAL", "Non-cash items included in net profit",
     {"FY2025": -1293, "FY2024": 1542, "FY2023": 1393, "FY2022": 4628, "FY2021": -8646, "FY2020": -4478,
      "FY2019": 20042, "FY2018": 62899, "FY2017": 11449, "FY2016": 4612, "FY2015": 20376, "FY2014": 6993,
      "FY2013": 3442}),
    ("DATA", "Reverse repurchase agreements",
     {"FY2024": 0, "FY2023": 149990, "FY2022": -21103, "FY2021": -36757}),
    ("DATA", "Loans, advances other than cash or cash equivalents",
     {"FY2025": -221607, "FY2024": -243014, "FY2023": -268285, "FY2022": -68881, "FY2021": -13840, "FY2020": 234049,
      "FY2017": -672228, "FY2016": -129256, "FY2015": 9045, "FY2014": 2673}),
    ("DATA", "Debt securities other than cash equivalents",
     {"FY2025": 250302, "FY2024": 164699, "FY2023": -108164, "FY2022": -221117, "FY2021": 7009, "FY2020": -329589}),
    ("DATA", "Loans, advances and debt securities other than cash equivalents (combined - see note)",
     {"FY2019": 125407, "FY2018": 263435,
      # FY2013's own report combines these into a single "Loans, advances and other debt securities other than
      # cash and cash equivalents" line too (same combined presentation as FY2018/FY2019's own reports) -
      # confirmed against FY2014's own report's FY2013 comparative, which shows the identical combined figure.
      "FY2013": -200768}),
    ("DATA", "Derivatives",
     {"FY2025": -571, "FY2024": -1109, "FY2023": 683, "FY2022": -728, "FY2021": 465}),
    ("DATA", "Other debtors and prepayments",
     {"FY2025": -7064, "FY2024": 387, "FY2023": -9064, "FY2022": -1161, "FY2021": 1497, "FY2020": 6427,
      "FY2019": -2485, "FY2018": 41805, "FY2017": -51334, "FY2016": -1042, "FY2015": 3701, "FY2014": 4335,
      "FY2013": -606}),
    ("TOTAL", "Change in operating assets",
     {"FY2025": 21060, "FY2024": -79037, "FY2023": -234840, "FY2022": -312990, "FY2021": -41626, "FY2020": -89113,
      "FY2019": 122922, "FY2018": 305240, "FY2017": -723562, "FY2016": -130298, "FY2015": 12746, "FY2014": 7008,
      "FY2013": -201374}),
    ("DATA", "Customer accounts and deposits by banks",
     {"FY2025": 78001, "FY2024": 277676, "FY2023": -94670, "FY2022": 165574, "FY2021": 238429, "FY2020": -254610,
      "FY2019": -1022442, "FY2018": 839143, "FY2017": 144902, "FY2016": -483032, "FY2015": 64151,
      "FY2014": 418975, "FY2013": 225768}),
    ("DATA", "Other liabilities",
     {"FY2025": 2884, "FY2024": -2695, "FY2023": 10519, "FY2022": 9288, "FY2021": -12192, "FY2020": 10181,
      "FY2019": -3196, "FY2018": 8238, "FY2017": -1338, "FY2016": 595, "FY2015": -16061, "FY2014": 5487,
      "FY2013": -1491}),
    ("TOTAL", "Change in operating liabilities",
     {"FY2025": 80885, "FY2024": 274981, "FY2023": -84151, "FY2022": 174862, "FY2021": 226237, "FY2020": -244429,
      "FY2019": -1025638, "FY2018": 847381, "FY2017": 143564, "FY2016": -482437, "FY2015": 48090,
      "FY2014": 424462, "FY2013": 224277}),
    ("DATA", "Income tax paid",
     {"FY2025": -8155, "FY2024": -7867, "FY2023": -5220, "FY2022": -1169, "FY2021": -1074, "FY2020": 214,
      "FY2019": 724, "FY2018": -782, "FY2017": 1774, "FY2016": 2256, "FY2015": -796, "FY2014": -4065,
      "FY2013": -2515}),
    ("TOTAL", "Net cash generated from/(used in) operating activities",
     {"FY2025": 124138, "FY2024": 227828, "FY2023": -286411, "FY2022": -120744, "FY2021": 189594,
      "FY2020": -321884, "FY2019": -873872, "FY2018": 1179372, "FY2017": -559510, "FY2016": -603288,
      "FY2015": 65345, "FY2014": 439909, "FY2013": 41678}),

    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment",
     {"FY2025": -409, "FY2024": -1590, "FY2023": -7683, "FY2022": -552, "FY2021": -274, "FY2020": -1096,
      "FY2019": -3994, "FY2018": -644, "FY2017": -472, "FY2016": -493, "FY2015": -451, "FY2014": -691,
      "FY2013": -491}),
    ("DATA", "Proceeds from sale of property, plant and equipment", {"FY2022": 42, "FY2013": 18}),
    ("DATA", "Purchases of equity shares and investments (pre-2018)", {"FY2014": -555, "FY2013": -1691}),
    ("DATA", "Proceeds on sale of equity investments",
     {"FY2024": 1162, "FY2017": 206, "FY2016": 4058, "FY2015": 515, "FY2014": 513, "FY2013": 629}),
    ("DATA", "Purchase of intangible assets",
     {"FY2025": -1128, "FY2024": -392, "FY2023": -841, "FY2022": -853, "FY2021": -540, "FY2020": -356,
      "FY2019": -1369, "FY2018": -5744, "FY2017": -3477, "FY2016": -3014, "FY2015": -510, "FY2014": -1737,
      "FY2013": -894}),
    ("DATA", "Proceeds from sale of intangible assets", {"FY2022": 269}),
    ("TOTAL", "Net cash used in investing activities",
     {"FY2025": -1537, "FY2024": -820, "FY2023": -8524, "FY2022": -1094, "FY2021": -814, "FY2020": -1452,
      "FY2019": -5363, "FY2018": -6388, "FY2017": -3743, "FY2016": 551, "FY2015": -446, "FY2014": -2470,
      "FY2013": -2429}),

    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Dividend paid",
     {"FY2025": -6228, "FY2024": -4780, "FY2023": -5215, "FY2022": -8765, "FY2018": -1498, "FY2013": -7200}),
    ("DATA", "Lease payments for Right of Use assets (principal)",
     {"FY2025": -249, "FY2024": -83, "FY2023": -202, "FY2022": -6, "FY2021": -191, "FY2020": -156}),
    ("DATA", "Interest on lease payments", {"FY2024": -192}),
    ("DATA", "Subordinated debt issued", {"FY2024": 28185}),
    ("DATA", "Subordinated debt redeemed", {"FY2024": -28185}),
    ("DATA", "Non-cash effect of share capital issuance (FY2015)", {"FY2015": 24697}),
    ("DATA", "Net subordinated debt issued/(redeemed) (FY2015)", {"FY2015": -408}),
    ("TOTAL", "Net cash used in financing activities",
     {"FY2025": -6477, "FY2024": -5055, "FY2023": -5417, "FY2022": -8771, "FY2021": -191, "FY2020": -156,
      "FY2019": 0, "FY2018": -1498, "FY2017": 0, "FY2016": 0, "FY2015": 24289, "FY2014": 0, "FY2013": -7200}),

    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents",
     {"FY2025": 116124, "FY2024": 221953, "FY2023": -300352, "FY2022": -130609, "FY2021": 188589, "FY2020": -323492,
      "FY2019": -879235, "FY2018": 1171486, "FY2017": -563253, "FY2016": -602737, "FY2015": 89188,
      "FY2014": 437439, "FY2013": 32049}),
    ("DATA", "Cash and cash equivalents at the beginning of the year",
     {"FY2025": 604467, "FY2024": 372940, "FY2023": 700795, "FY2022": 766720, "FY2021": 586617, "FY2020": 897237,
      "FY2019": 1821651, "FY2018": 625253, "FY2017": 1226225, "FY2016": 1623993, "FY2015": 1514842,
      "FY2014": 1041466, "FY2013": 1014858}),
    ("DATA", "Effect of exchange rate change on cash and cash equivalents",
     {"FY2025": -2014, "FY2024": 9574, "FY2023": -27503, "FY2022": 64684, "FY2021": -8486, "FY2020": 12872,
      "FY2019": -45179, "FY2018": 24912, "FY2017": -37719, "FY2016": 204969, "FY2015": 19963, "FY2014": 35937,
      "FY2013": -5441}),
    ("TOTAL", "Cash and cash equivalents at the end of the year",
     {"FY2025": 718577, "FY2024": 604467, "FY2023": 372940, "FY2022": 700795, "FY2021": 766720, "FY2020": 586617,
      "FY2019": 897237, "FY2018": 1821651, "FY2017": 625253, "FY2016": 1226225, "FY2015": 1623993,
      "FY2014": 1514842, "FY2013": 1041466}),

    ("SECTION", "Cash and cash equivalents comprise", {}),
    ("DATA", "Cash, notes and coin",
     {"FY2025": 0, "FY2024": 1, "FY2023": 1, "FY2022": 0, "FY2021": 218, "FY2020": 219, "FY2019": 89, "FY2018": 110,
      "FY2017": 143, "FY2016": 87, "FY2015": 323, "FY2014": 633, "FY2013": 223}),
    ("DATA", "Loans and advances to banks of original maturity three months or less",
     {"FY2025": 409309, "FY2024": 488558, "FY2023": 216705, "FY2022": 391580, "FY2021": 376162, "FY2020": 350549,
      "FY2019": 768892, "FY2018": 627016, "FY2017": 588102, "FY2016": 427449, "FY2015": 767850,
      "FY2014": 1058934, "FY2013": 1031243}),
    ("DATA", "Loans and advances to non-banks of original maturity three months or less (from FY2019 onwards)",
     {"FY2020": 0, "FY2019": 3786, "FY2018": 191951}),
    ("DATA", "Debt securities/certificates of deposit of three months original maturity or less",
     {"FY2025": 309268, "FY2024": 115908, "FY2023": 156234, "FY2022": 309215, "FY2021": 390340, "FY2020": 235849,
      "FY2019": 124470, "FY2018": 1002574, "FY2017": 37008, "FY2016": 798689, "FY2015": 855820,
      "FY2014": 455275, "FY2013": 10000}),
    ("TOTAL", "Cash and cash equivalents",
     {"FY2025": 718577, "FY2024": 604467, "FY2023": 372940, "FY2022": 700795, "FY2021": 766720, "FY2020": 586617,
      "FY2019": 897237, "FY2018": 1821651, "FY2017": 625253, "FY2016": 1226225, "FY2015": 1623993,
      "FY2014": 1514842, "FY2013": 1041466}),
]

bw.add_cash_flow_sheet(
    title="British Arab Commercial Bank PLC — Statement of Cash Flow",
    subtitle="Bank entity basis (single UK entity, no subsidiaries/associates). GBP throughout, no FX conversion.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=68,
    source_height=210,
    unit_suffix=" (£'000)",
    years=YEARS,
)

# ---------------------------------------------------------------
# Asset Quality: Loans and advances to customers by IFRS 9 stage, from the
# Bank's own "Credit quality analysis" note each year (own report). FY2024
# and FY2022's own reports present credit quality only via a combined
# grade-based table across all financial assets (no customer-loan-specific
# stage split that year) - confirmed by reading each report in full, left
# blank rather than assumed or backfilled from a different year's document.
# ---------------------------------------------------------------
AQ_S1 = {"FY2025": 270253, "FY2023": 254360, "FY2021": 417375, "FY2020": 360471, "FY2019": 480522, "FY2018": 826480}
AQ_S2 = {"FY2025": 36036, "FY2023": 102165, "FY2021": 69314, "FY2020": 222279, "FY2019": 151173, "FY2018": 130467}
AQ_S3 = {"FY2025": 49098, "FY2023": 43879, "FY2021": 11038, "FY2020": 58099, "FY2019": 84760, "FY2018": 211138}
AQ_GROSS_TOTAL = {"FY2025": 355387, "FY2023": 400404, "FY2021": 497727, "FY2020": 640849, "FY2019": 716455,
                  "FY2018": 1168085}
AQ_ALLOW_S1 = {"FY2025": -266, "FY2023": -229, "FY2021": -632, "FY2020": -1342, "FY2019": -1063, "FY2018": -1840}
AQ_ALLOW_S2 = {"FY2025": -628, "FY2023": -2442, "FY2021": -4388, "FY2020": -5764, "FY2019": -3700, "FY2018": -3371}
AQ_ALLOW_S3 = {"FY2025": -931, "FY2023": -9166, "FY2021": -8171, "FY2020": -51214, "FY2019": -60178,
               "FY2018": -81713}
AQ_ALLOW_TOTAL = {"FY2025": -1825, "FY2023": -11837, "FY2021": -13191, "FY2020": -58320, "FY2019": -64941,
                  "FY2018": -86924}
AQ_CARRYING = {"FY2025": 353562, "FY2024": 387260, "FY2023": 388567, "FY2022": 463780, "FY2021": 484536,
               "FY2020": 582529, "FY2019": 651514, "FY2018": 1081161}
AQ_STAGE3_RATIO = {y: f"{AQ_S3[y] / AQ_GROSS_TOTAL[y] * 100:.2f}%" for y in AQ_S3}
AQ_STAGE3_COVERAGE = {y: f"{-AQ_ALLOW_S3[y] / AQ_S3[y] * 100:.2f}%" for y in AQ_S3}
AQ_OVERALL_COVERAGE = {y: f"{-AQ_ALLOW_TOTAL[y] / AQ_GROSS_TOTAL[y] * 100:.2f}%" for y in AQ_S3}

# Pre-IFRS 9 (FY2014-FY2017) years use IAS 39's individual/collective impairment model, with no Stage 1/2/3
# equivalent - the Bank's own 'Net charge for impairment losses on loans and advances' note (movements in the
# impairment provision balance) is used as a like-for-like proxy instead, each year from that year's own report.
AQ_IND_IMPAIRMENT = {"FY2017": -47994, "FY2016": -40719, "FY2015": -26360, "FY2014": -23331}
AQ_COLL_IMPAIRMENT = {"FY2017": -809, "FY2016": -250, "FY2015": -1431, "FY2014": -784}
AQ_TOTAL_IMPAIRMENT_PROVISION = {"FY2017": -48803, "FY2016": -40969, "FY2015": -27791, "FY2014": -24115}
AQ_GROSS_CUSTOMER_LOANS_PRE = {"FY2017": 1117392, "FY2016": 905280, "FY2015": 713471, "FY2014": 495490}
AQ_OVERALL_COVERAGE_PRE = {y: f"{-AQ_TOTAL_IMPAIRMENT_PROVISION[y] / AQ_GROSS_CUSTOMER_LOANS_PRE[y] * 100:.2f}%"
                           for y in AQ_TOTAL_IMPAIRMENT_PROVISION}

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, by IFRS 9 stage (gross exposure)", {}),
    ("DATA", "Stage 1 (12-month ECL)", AQ_S1),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", AQ_S2),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired / default)", AQ_S3),
    ("TOTAL", "Total gross exposure", AQ_GROSS_TOTAL),
    ("SECTION", "Loss allowance, by stage", {}),
    ("DATA", "Stage 1 allowance", AQ_ALLOW_S1),
    ("DATA", "Stage 2 allowance", AQ_ALLOW_S2),
    ("DATA", "Stage 3 allowance", AQ_ALLOW_S3),
    ("TOTAL", "Total loss allowance", AQ_ALLOW_TOTAL),
    ("TOTAL", "Carrying amount (= Balance Sheet's Loans and advances to customers)", AQ_CARRYING),
    ("SECTION", "Ratios (FY2024/FY2022 not computable - see note)", {}),
    ("DATA", "Stage 3 exposure ratio (Stage 3 / total gross exposure)", AQ_STAGE3_RATIO),
    ("DATA", "Stage 3 coverage ratio (Stage 3 allowance / Stage 3 exposure)", AQ_STAGE3_COVERAGE),
    ("DATA", "Overall coverage ratio (total allowance / total gross exposure)", AQ_OVERALL_COVERAGE),
    ("SECTION", "Pre-IFRS 9 (FY2014-FY2017): impairment provision against Loans and advances to customers "
                "(IAS 39 individual/collective model - not a Stage 1/2/3 equivalent, see note)", {}),
    ("DATA", "Individual impairment provision", AQ_IND_IMPAIRMENT),
    ("DATA", "Collective impairment provision", AQ_COLL_IMPAIRMENT),
    ("TOTAL", "Total impairment provision", AQ_TOTAL_IMPAIRMENT_PROVISION),
    ("DATA", "Estimated gross Loans and advances to customers (carrying amount + impairment provision)",
     AQ_GROSS_CUSTOMER_LOANS_PRE),
    ("DATA", "Overall coverage ratio (total provision / estimated gross loans)", AQ_OVERALL_COVERAGE_PRE),
]

bw.add_asset_quality_sheet(
    title="British Arab Commercial Bank PLC — Asset Quality / Credit Risk Disclosures",
    subtitle="Loans and advances to customers by IFRS 9 stage, £'000. Bank entity basis.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - British Arab Commercial Bank PLC's own 'Credit quality analysis' note (Loans and advances to "
        "customers only, £'000), each year from that year's own Annual Report:\n"
        f"FY2025: Annual Report YE2025, p.95 - {AR_URL['FY2025']}\n"
        f"FY2023: Annual Report YE2023, p.83 - {AR_URL['FY2023']}\n"
        f"FY2021: Annual Report YE2021, p.72 - {AR_URL['FY2021']}\n"
        f"FY2020: Annual Report YE2020, p.2.34 - {AR_URL['FY2020']}\n"
        f"FY2019: Annual Report YE2019, p.2.35 - {AR_URL['FY2019']}\n"
        f"FY2018: Annual Report YE2018, p.2.29 - {AR_URL['FY2018']}\n\n"
        "FY2024 and FY2022's own Annual Reports (checked in full) present credit quality only via a single "
        "grade-based table spanning all financial assets combined (cash, loans, debt securities, derivatives) - "
        "no customer-loan-specific Stage 1/2/3 split that year, unlike FY2025/FY2023/FY2021's own reports. "
        "Genuine finding: the Stage 3 exposure ratio rose sharply (2.22% FY2021 -> 13.82% FY2025) while the Stage "
        "3 coverage ratio fell sharply (74.03% FY2021 -> 1.90% FY2025) - consistent with the Bank's own disclosed "
        "credit-grade migration and write-off activity, not a data error.\n\n"
        "Pre-IFRS 9 (FY2014-FY2017) impairment provision figures - British Arab Commercial Bank PLC's own 'Net "
        "charge for impairment losses on loans and advances' note, each year from that year's own Annual Report:\n"
        f"FY2017: Annual Report (filename says 2018, confirmed FY2017), p.55 - {AR_URL['FY2017']}\n"
        f"FY2016: Annual Report (filename says 2017, confirmed FY2016), p.53 - {AR_URL['FY2016']}\n"
        f"FY2015: Annual Report YE2015, p.48 - {AR_URL['FY2015']}\n"
        f"FY2014: Annual Report YE2014, p.59 - {AR_URL['FY2014']}\n"
        "IFRS 9 (adopted 1 January 2018) replaced IAS 39's individual/collective impairment model with the "
        "forward-looking Stage 1/2/3 ECL model used from FY2018 onwards - these two blocks are not directly "
        "comparable and are shown as separate sections rather than forced into a single set of columns. Genuine "
        "restatement: FY2014's own report states its impairment provision split as Individual GBP23,331k / "
        "Collective GBP784k; FY2015's own report's FY2014 comparative restates this split to GBP22,755k / "
        "GBP1,360k (the total, GBP24,115k, is identical either way) - FY2014's own split is used here, per "
        "project convention."
    ),
    first_col_width=68,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=170)


CET1 = {"FY2025": 266352, "FY2024": 245034, "FY2023": 223772, "FY2022": 197516, "FY2021": 199873, "FY2020": 192041,
        "FY2019": 170824, "FY2018": 161218, "FY2017": 209247, "FY2016": 203089, "FY2015": 208273, "FY2014": 194652}
TOTAL_CAPITAL = {"FY2025": 334756, "FY2024": 318553, "FY2023": 276133, "FY2022": 267579, "FY2021": 270130,
                 "FY2020": 263826, "FY2019": 236050, "FY2018": 233482, "FY2017": 281209, "FY2016": 278176,
                 "FY2015": 271337, "FY2014": 255171}
RWA = {"FY2025": 1924184, "FY2024": 1571106, "FY2023": 1240666, "FY2022": 1231445, "FY2021": 1085219,
       "FY2020": 1101165, "FY2019": 1207405, "FY2018": 1635966, "FY2017": 1723409, "FY2016": 1418241,
       "FY2015": 1361260, "FY2014": 1067344}
CET1_RATIO = {"FY2025": "13.8%", "FY2024": "15.6%", "FY2023": "18.0%", "FY2022": "16.0%", "FY2021": "18.4%",
              "FY2020": "17.4%", "FY2019": "14.1%", "FY2018": "9.9%", "FY2017": "12.1%", "FY2016": "14.3%",
              "FY2015": "15.3%", "FY2014": "18.2%"}
TCR = {"FY2025": "17.4%", "FY2024": "20.3%", "FY2023": "22.3%", "FY2022": "21.7%", "FY2021": "24.9%",
       "FY2020": "24.0%", "FY2019": "19.6%", "FY2018": "14.3%", "FY2017": "16.3%", "FY2016": "19.6%",
       "FY2015": "19.9%", "FY2014": "23.9%"}
LEVERAGE_RATIO = {"FY2025": "7.2%", "FY2024": "6.6%", "FY2023": "6.8%", "FY2022": "5.7%", "FY2021": "6.7%",
                  "FY2020": "7.09%", "FY2019": "5.69%", "FY2018": "3.83%", "FY2017": "6.53%", "FY2016": "6.56%",
                  "FY2015": "6.55%"}
LCR = {"FY2025": "234%", "FY2024": "327%", "FY2023": "271%", "FY2022": "254%", "FY2021": "276%", "FY2020": "215%",
       "FY2019": "222%"}
NSFR = {"FY2025": "166%", "FY2024": "160%", "FY2023": "151%", "FY2022": "130%"}

RWA_RESTATEMENT_NOTE = (
    "FY2022's Total RWA/CET1/Tier1/Total Capital ratios shown here are as originally published in the 2022 "
    "Pillar 3 Disclosures (RWA 1,231,445). The 2023 Pillar 3 Disclosures' own FY2022 comparative column restates "
    "this to 1,224,488 (footnoted 'amended for consistency of presentation') with correspondingly adjusted ratios "
    "(16.1% CET1/Tier1, 21.9% Total Capital) - the originally-published figure is used here, per project convention."
)

metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", CET1)], p3_sources())
metric("CET1 Ratio", "%", [("CET1 ratio", CET1_RATIO)], p3_sources(), note=RWA_RESTATEMENT_NOTE)
metric("Tier 1 Capital", "£'000 (= CET1 capital; no AT1 instruments)", [("Tier 1 capital", CET1)], p3_sources())
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", CET1_RATIO)], p3_sources())
metric("Total Capital", "£'000", [("Total capital", TOTAL_CAPITAL)], p3_sources())
metric("Total Capital Ratio", "%", [("Total capital ratio", TCR)], p3_sources(), note=RWA_RESTATEMENT_NOTE)
metric("Total RWAs", "£'000", [("Total risk-weighted exposure amount", RWA)], p3_sources(),
       note="See CET1 Ratio sheet for the FY2022 restatement note.")

# ---------------------------------------------------------------
# RWA Breakdown. GENUINE CORRECTNESS FINDING (out of this fork's HD-051 scope to
# fix, flagged for follow-up): the FY2021-FY2025 note below claims none of those
# 5 years' own Pillar 3 Disclosures contain an RWA-by-risk-category table - but
# BACB_Pillar3-2021_v3.pdf (already cited elsewhere in this script for FY2021)
# DOES contain exactly such a table (its own "Table 12: Overview of RWAs..."),
# and the same table appears consistently in every one of FY2014-FY2019's own
# Pillar 3 Disclosures, each verified to foot to that year's own Total RWA
# figure within GBP1k. Populated below for FY2014-FY2019; FY2020 has no
# standalone Pillar 3 document (see p3_sources()) and back-deriving RWA-by-
# category from the FY2021 comparative's capital-requirement-only figures via
# /8% would introduce ~GBP250k of rounding error against the known FY2020
# Total RWA, so FY2020 is left "Not publicly disclosed" rather than estimated.
# ---------------------------------------------------------------
RWA_BD_YEARS = ["FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014"]


def bd(**vals):
    return {y: vals[y] for y in RWA_BD_YEARS if y in vals}


rwa_breakdown_rows = [
    # Modern UK OV1 disclosures report aggregate risk-type rows rather than
    # the older exposure-class table. Keep them separate and non-additive.
    ("SECTION", "Modern UK OV1 aggregate risk types (not additive to legacy rows)", {}),
    ("DATA", "Credit risk (excluding counterparty credit risk) — UK OV1 aggregate",
     {"FY2023": 1128031, "FY2022": 1147518, "FY2021": 976627}),
    ("DATA", "Counterparty credit risk — UK OV1 aggregate",
     {"FY2023": 318, "FY2022": 2127, "FY2021": 1986}),
    ("DATA", "Market risk — UK OV1 aggregate",
     {"FY2023": 1651, "FY2022": 3163, "FY2021": 13550}),
    ("DATA", "Operational risk — UK OV1 aggregate",
     {"FY2023": 110666, "FY2022": 78637, "FY2021": 93056}),
    ("DATA", "Amounts below deduction thresholds — UK OV1 memo",
     {"FY2023": 0, "FY2022": 2681, "FY2021": 0}),
    ("TOTAL", "Total risk-weighted exposure amount — UK OV1",
     {"FY2023": 1240666, "FY2022": 1231445, "FY2021": 1085220}),
    ("SECTION", "Legacy Table 12 risk categories", {}),
    ("SECTION", "Credit and Counterparty Credit Risk", {}),
    ("DATA", "Central governments/central banks",
     bd(FY2019=38728, FY2018=64505, FY2017=69107, FY2016=11443, FY2015=3643, FY2014=9041)),
    ("DATA", "Multilateral development banks", bd(FY2015=0, FY2014=11944)),
    ("DATA", "Institutions",
     bd(FY2019=125785, FY2018=185570, FY2017=200843, FY2016=92288, FY2015=254240, FY2014=507871)),
    ("DATA", "Corporates",
     bd(FY2019=509680, FY2018=714874, FY2017=978424, FY2016=987560, FY2015=824756, FY2014=379442)),
    ("DATA", "Covered bonds", bd(FY2019=8435, FY2018=10594, FY2017=2717)),
    ("DATA", "Secured by mortgages on immovable property",
     bd(FY2019=290316, FY2018=316818, FY2017=276665, FY2016=178008, FY2015=86488, FY2014=17519)),
    ("DATA", "Exposures in default",
     bd(FY2019=38647, FY2018=130368, FY2017=69839, FY2016=27128, FY2015=39084, FY2014=23153)),
    ("DATA", "Equity exposures",
     bd(FY2019=2374, FY2018=1964, FY2017=1868, FY2016=1807, FY2015=8248, FY2014=8080)),
    ("DATA", "Items associated with particularly high risk", bd(FY2019=38964, FY2018=29829, FY2017=16203,
                                                                 FY2016=10325, FY2015=20291)),
    ("DATA", "Other items",
     bd(FY2019=28371, FY2018=32391, FY2017=19991, FY2016=25248, FY2015=20954, FY2014=19331)),
    ("TOTAL", "Total Credit and Counterparty Credit Risk",
     bd(FY2019=1081300, FY2018=1486913, FY2017=1635656, FY2016=1333807, FY2015=1257703, FY2014=976383)),
    ("SECTION", "Market Risk", {}),
    ("DATA", "Interest Rate PRR", bd(FY2019=20283, FY2018=8129, FY2017=5451, FY2015=16259, FY2014=12516)),
    ("DATA", "Foreign Exchange PRR", bd(FY2019=8500, FY2018=54567, FY2017=2692, FY2016=2425, FY2015=1537,
                                        FY2014=1146)),
    ("DATA", "Operational Risk (Basic Indicator Approach)",
     bd(FY2019=96637, FY2018=85268, FY2017=79242, FY2016=81480, FY2015=85615, FY2014=76686)),
    ("DATA", "Credit Valuation Adjustment", bd(FY2019=684, FY2018=1090, FY2017=369, FY2016=529, FY2015=146,
                                               FY2014=613)),
    ("TOTAL", "Total Pillar 1 RWA (= Total RWAs sheet)",
     bd(FY2019=1207405, FY2018=1635966, FY2017=1723409, FY2016=1418241, FY2015=1361260, FY2014=1067344)),
]

bw.add_rwa_breakdown_sheet(
    title="British Arab Commercial Bank PLC — RWA Breakdown",
    subtitle="Pillar 1 RWA by risk category, £'000. FY2021-FY2023 UK OV1 aggregates are shown separately from "
             "the legacy exposure-class rows; FY2024-FY2025 are not disclosed at this granularity (see note); "
             "FY2020 not disclosed (no standalone document); FY2019-FY2014 populated from each year's own Table 12.",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources(
        extra="FY2024-FY2025: no exposure-class breakdown was found in the own-year Pillar 3 documents. FY2021-FY2023 "
              "do contain UK OV1 aggregate risk-type rows, reproduced above; these are not the older exposure-class "
              "rows and are not additive to them. GENUINE FINDING (2026-09-05, HD-051): this appears to be incorrect - "
              "BACB_Pillar3-2021_v3.pdf (cited above for FY2021) itself contains 'Table 12: Overview of RWAs and "
              "the Bank's minimum capital requirement...under Pillar 1', with the same table present in every one "
              "of FY2014-FY2019's own Pillar 3 Disclosures (see below) - flagged here for a follow-up fix by "
              "whoever next touches this bank; out of scope to correct under HD-051 (years FY2014-FY2020 only).\n\n"
              "FY2019: 2019 Pillar 3 Disclosures, Table 12 (own year) - " + P3_URL["FY2019"] + "\n"
              "FY2018: 2018 Pillar 3 Disclosures, Table 12 (own year) - " + P3_URL["FY2018"] + "\n"
              "FY2017: 2017 Pillar 3 Disclosures, Table 12 (own year) - " + P3_URL["FY2017"] + "\n"
              "FY2016: 2016 Pillar 3 Disclosures, Table 7 (own year) - " + P3_URL["FY2016"] + "\n"
              "FY2015: 2015 Pillar 3 Disclosures, Table 9 (own year) - " + P3_URL["FY2015"] + "\n"
              "FY2014: 2014 Pillar 3 Disclosures, Table 9 (own year) - " + P3_URL["FY2014"] + "\n"
              "FY2020: no standalone Pillar 3 document exists (see main sources above) and the FY2021 document's "
              "FY2020 comparative only discloses capital-requirement figures (not RWA) at category level; "
              "back-deriving RWA via /8% would introduce ~GBP250k of rounding error against the independently-"
              "known FY2020 Total RWA of 1,101,165 - left 'Not publicly disclosed' rather than estimated."
    ),
    first_col_width=54,
    source_height=340,
    unit_suffix=" (£'000)",
)
metric("Leverage Ratio", "%", [("Leverage ratio", LEVERAGE_RATIO)], p3_sources(
    extra="Leverage ratio not disclosed for FY2014 - the leverage ratio disclosure first appears in BACB's own "
          "Pillar 3 Disclosures from FY2015 onwards."))
metric("LCR", "%", [("Liquidity coverage ratio (12-month average)", LCR)], p3_sources(
    extra="LCR % not disclosed for FY2014-FY2018 - each of those years' own Pillar 3 Disclosures shows an LCR "
          "chart but no extractable numeric table; the first extractable LCR % is FY2019's own report."))
metric("NSFR", "%", [("NSFR ratio (4-quarter average)", NSFR)], p3_sources(
    extra="NSFR not applicable/disclosed for FY2021 - the NSFR reporting requirement and KM1 template line were "
          "new from FY2022; the FY2021 comparative column in the 2022 Pillar 3 Disclosures itself states 'N/A'. "
          "Not disclosed for FY2014-FY2020 either - the requirement did not exist yet."))

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources(),
    per_note={"MREL Ratio": "Not found in any of the 5 Annual Reports or Pillar 3 Disclosures checked - not "
                             "asserted as an explicit exemption, just absent from every source."},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 3318750, "FY2024": 3343466, "FY2023": 3001927, "FY2022": 3194745,
                          "FY2021": 2782543, "FY2020": 2542898, "FY2019": 2779318, "FY2018": 3893852,
                          "FY2017": 2952856, "FY2016": 2939264, "FY2015": 3021295, "FY2014": 2916417}),
        ("Loans and advances to customers", {"FY2025": 353562, "FY2024": 387260, "FY2023": 388567, "FY2022": 463780,
                                             "FY2021": 484536, "FY2020": 582529, "FY2019": 651514, "FY2018": 1081161,
                                             "FY2017": 1068589, "FY2016": 864311, "FY2015": 685680,
                                             "FY2014": 471375}),
        ("Deposits from banks + other deposits",
         {"FY2025": 2938773, "FY2024": 2977572, "FY2023": 2659678, "FY2022": 2882233, "FY2021": 2481506,
          "FY2020": 2241682, "FY2019": 2511552, "FY2018": 3632606, "FY2017": 2651194, "FY2016": 2641932,
          "FY2015": 2734886, "FY2014": 2624207}),
        ("Total equity", {"FY2025": 278340, "FY2024": 257612, "FY2023": 232578, "FY2022": 207266, "FY2021": 210286,
                          "FY2020": 197207, "FY2019": 177894, "FY2018": 168178, "FY2017": 216833, "FY2016": 208393,
                          "FY2015": 210170, "FY2014": 202169}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Operating income before allowance for credit losses",
         {"FY2025": 92763, "FY2024": 98650, "FY2023": 87856, "FY2022": 57433, "FY2021": 41723, "FY2020": 44791,
          "FY2019": 64024, "FY2018": 64836, "FY2017": 53396, "FY2016": 42739, "FY2015": 38510, "FY2014": 48076}),
        ("Administrative expenses",
         {"FY2025": -64363, "FY2024": -62082, "FY2023": -53594, "FY2022": -42031, "FY2021": -38763,
          "FY2020": -37014, "FY2019": -37388, "FY2018": -38018, "FY2017": -36000, "FY2016": -33038,
          "FY2015": -34777, "FY2014": -37603}),
        ("Profit for the year",
         {"FY2025": 24127, "FY2024": 28755, "FY2023": 27875, "FY2022": 15100, "FY2021": 13035, "FY2020": 14428,
          "FY2019": 7628, "FY2018": -35308, "FY2017": 6825, "FY2016": 2719, "FY2015": -14505, "FY2014": 4729}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Total equity", {"FY2025": 278340, "FY2024": 257612, "FY2023": 232578, "FY2022": 207266, "FY2021": 210286,
                          "FY2020": 197207, "FY2019": 177894, "FY2018": 168178, "FY2017": 216833, "FY2016": 208393,
                          "FY2015": 210170, "FY2014": 202169}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash generated from/(used in) operating activities",
         {"FY2025": 124138, "FY2024": 227828, "FY2023": -286411, "FY2022": -120744, "FY2021": 189594,
          "FY2020": -321884, "FY2019": -873872, "FY2018": 1179372, "FY2017": -559510, "FY2016": -603288,
          "FY2015": 65345, "FY2014": 439909}),
        ("Net cash used in investing activities",
         {"FY2025": -1537, "FY2024": -820, "FY2023": -8524, "FY2022": -1094, "FY2021": -814, "FY2020": -1452,
          "FY2019": -5363, "FY2018": -6388, "FY2017": -3743, "FY2016": 551, "FY2015": -446, "FY2014": -2470}),
        ("Net cash used in financing activities",
         {"FY2025": -6477, "FY2024": -5055, "FY2023": -5417, "FY2022": -8771, "FY2021": -191, "FY2020": -156,
          "FY2019": 0, "FY2018": -1498, "FY2017": 0, "FY2016": 0, "FY2015": 24289, "FY2014": 0}),
        ("Cash and cash equivalents at end of year",
         {"FY2025": 718577, "FY2024": 604467, "FY2023": 372940, "FY2022": 700795, "FY2021": 766720,
          "FY2020": 586617, "FY2019": 897237, "FY2018": 1821651, "FY2017": 625253, "FY2016": 1226225,
          "FY2015": 1623993, "FY2014": 1514842}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Total Capital Ratio", TCR),
        ("Leverage Ratio", LEVERAGE_RATIO),
        ("LCR", LCR),
        ("NSFR", NSFR),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BRITISH ARAB COMMERCIAL BANK FINANCIALS.xlsx")
