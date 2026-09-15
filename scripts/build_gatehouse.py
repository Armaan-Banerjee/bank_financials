import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2017"]  # most recent first, y/e 31 Dec
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://assets.gatehousebank.com/production/downloads/Gatehouse-Bank-Annual-Report-2025.pdf"
AR2023_URL = "https://gatehousebank.com/downloads/gatehouse-bank-annual-report-2023"
AR2022_URL = "https://gatehousebank.com/downloads/gatehouse-bank-annual-report-2022"
AR2021_URL = "https://assets.gatehousebank.com/production/downloads/Gatehouse-Bank-Annual-Report-2021-FINAL-web.pdf"
AR2017_URL = "https://assets.gatehousebank.com/production/downloads/gatehousebankannualreport2017-wesbite2.pdf"
P3_2024_URL = "https://assets.gatehousebank.com/production/downloads/Gatehouse-Bank-Pillar-III-Disclosure-2024-FINAL.pdf"
P3_2023_URL = "https://assets.gatehousebank.com/production/downloads/Gatehouse-Bank-Pillar-III-Disclosure-2023-FINAL.pdf"
P3_2022_URL = "https://gatehousebank.com/downloads/gatehouse-bank-pillar-3-disclosure-2022"
P3_2021_URL = "https://assets.gatehousebank.com/production/downloads/Gatehouse-Bank-Pillar-III-Disclosure-2021-FINAL_2022-08-23-154942_nofu.pdf"
P3_2017_URL = "https://assets.gatehousebank.com/production/downloads/gatehousebankpillariiidisclosure2017.pdf"
PUBLICATIONS_INDEX_URL = "https://gatehousebank.com/about-us/corporate-governance"

ENTITY_NOTE = (
    "ENTITY NOTE: Gatehouse Bank Plc (FRN 475346, company 06260053) is a UK Shariah-compliant "
    "(Islamic) bank - 'profit paid/received' in the cash flow statement is the functional equivalent "
    "of conventional interest paid/received, and financing/advances line items are Shariah-compliant "
    "structures (Wakala, Murabaha, ijara) presented here as the standard cash flow line items they "
    "represent. Figures are the Bank's own Consolidated Statement of Cash Flows from its Companies "
    "House 'Group of companies' accounts' filings.\n\n"
    "GENUINE MID-SERIES PRESENTATION CHANGE across 3 distinct eras, each kept on its own "
    "originally-published line items (blank cells where a line doesn't apply that year, not a gap): "
    "FY2021 (single combined profit line, no separate cash-tax-paid line); FY2022-FY2023 (profit "
    "split continuing/discontinued, 'Share in profit of associate' adjustment, cash tax paid shown "
    "separately within the operating-liabilities block); FY2024-FY2025 (adds Held-For-Sale "
    "adjustment/asset lines and an 'Intercompany payable receivable' line reflecting a disclosed "
    "business restructuring, and introduces a 'Cash generated from operations' subtotal not shown in "
    "earlier years). The 'Fair value movement in financial instruments held at FVTIS (derivative "
    "financial instruments)' caption is used TWICE within the same year's own statement - once as a "
    "non-cash P&L adjustment, once under operating-asset movements - kept as two distinct rows per "
    "the source, not a duplicate.\n\n"
    "FY2021 RESTATEMENT: the FY2022 Annual Report's own FY2021 comparative column reclassifies "
    "several FY2021 operating/investing line items (e.g. splits continuing/discontinued profit "
    "differently, renames 'Net investment in financial assets held at FVTIS/FVTOCI' into the "
    "derivative-FVTIS captions used from FY2022 onward) versus FY2021's own originally-published "
    "Annual Report. The two vintages' Net cash flow from operating/investing activities totals differ "
    "(12,357/17,325 as originally published vs 12,643/17,039 restated) but their SUM and the overall "
    "net cash movement (28,958) are identical in both - a pure reclassification between sections, not "
    "a value correction (the same pattern seen at FCE Bank Plc in this project). FY2021's own "
    "originally-published Annual Report figures are used here, consistent with every other year using "
    "its own primary source rather than a later restated comparative.\n\n"
    f"FY2017: Annual Report and Financial Statements 2017, pp.33-36 - {AR2017_URL}\n"
    "FY2017 Pillar 3 key metrics are not in the 2017 annual report, but they ARE published - in the Bank's "
    "separate Pillar III Disclosure 2017, which was located and read on 2026-09-15 and now populates the "
    f"FY2017 column of every regulatory metric sheet except NSFR - {P3_2017_URL}\n"
    "(This supersedes an earlier note here which said FY2017 regulatory cells were 'left blank rather than "
    "inferred from the financial statements'. Nothing needed to be inferred: the wrong document had been "
    "checked. See the FY2017 note on the metric sheets for the full derivation and cross-checks.)\n\n"
    "Full opening-to-closing cash balance chain (including the separately-disclosed FX effect on cash) "
    "ties exactly across all available years."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Gatehouse Bank Plc's own Consolidated Statement of Cash Flows:\n"
    f"FY2025/FY2024: Annual Report and Financial Statements 2025, p.60-61 (Consolidated Statement of "
    f"Cash Flows) - {AR2025_URL}\n"
    f"FY2023/FY2022: Annual Report and Financial Statements 2023, p.64-65 (Consolidated Statement of "
    f"Cash Flows) - {AR2023_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021, p.52 (Consolidated Statement of Cash Flows, "
    f"own originally-published FY2021 column - see ENTITY NOTE on the later FY2022 report's restated "
    f"comparative) - {AR2021_URL}\n\n"
    + ENTITY_NOTE
)


def p3_sources(page, extra=""):
    return (
        f"Sources - Gatehouse Bank Plc Pillar 3 disclosures, Article 447 Key Metrics table, p.{page}:\n"
        f"FY2017: Pillar III Disclosure 2017 - Key Metrics table p.3, s.5 Capital Resources p.11, s.6 p.12, "
        f"s.9 p.19, Appendix 1 (Own Funds Disclosure) p.26 and Appendix II (Analysis of Leverage Ratio) p.27. "
        f"This is the CRD IV-era predecessor of the Article 447 template, not the template itself - "
        f"{P3_2017_URL}\n"
        f"FY2024: Pillar III Disclosure 2024 (Dec-24 column) - {P3_2024_URL}\n"
        f"FY2023: Pillar III Disclosure 2023 (Dec-23 column) - {P3_2023_URL}\n"
        f"FY2022: Pillar III Disclosure 2022 (Dec-22 column, own year's disclosure - see restatement "
        f"note) - {P3_2022_URL}\n"
        f"FY2021: Annual Report and Financial Statements 2021, s.5 Capital Resources, p.11 (own "
        f"year-end capital resources note, cross-validated against the 2022 Pillar 3 disclosure's "
        f"Dec-21 comparative column) - {AR2021_URL}\n"
        f"SDDT DATE TEST (checked 2026-09-15): the PRA's consolidated register of waivers and modifications "
        f"('Consolidated Waivers list for PRA-regulated firms - as of 1 July 2026', bankofengland.co.uk/"
        f"prudential-regulation/authorisations/waivers-and-modifications-of-rules) records that Gatehouse Bank "
        f"Plc (FRN 475346) holds a 'Modification by Consent - PRA Rulebook - CRR Firms - Rule 3.1 of the SDDT "
        f"Regime - General Application Part', sub-rule 'Ru 3.1', starting 08/01/2026 with no end date. That "
        f"modification removes the Pillar 3 disclosure obligation outright (a stronger relief than UK CRR "
        f"Article 433b, which only reduces frequency and content for small and non-complex institutions).\n"
        f"Crucially, 08/01/2026 falls EIGHT DAYS AFTER the FY2025 year-end of 31 December 2025 (year-end "
        f"confirmed 31 December throughout the Bank's Companies House accounts filing history, company "
        f"06260053). FY2025 therefore PREDATES the modification and is NOT structurally exempt - the Bank was "
        f"still subject to the disclosure obligation for that year. This is corroborated independently by the "
        f"fact that the FY2025 Pillar 3 document demonstrably EXISTS (the Annual Report says it is 'available "
        f"on request', see below): the obligation was live and was met, just not by general publication. The "
        f"FY2025 blanks below are therefore an ACCESS gap, not a structural one, and are recoverable by "
        f"requesting the document from the Bank.\n"
        f"Forward-looking: FY2026 (year ending 31 December 2026) is the first year that falls after the "
        f"modification took effect, so from FY2026 onward these blanks are expected to become structural.\n"
        f"FY2025: no FY2025 Pillar 3 disclosure has been published. The Bank's own Annual Report 2025 "
        f"confirms the document is not on general release - 'Pillar 3 disclosures are presented in the \"Pillar 3 "
        f"Disclosures\" document, available on request' (Notes to the Financial Statements, p.125) - and no "
        f"2025 file exists under the CDN naming pattern that serves every prior year, nor in the site's "
        f"downloads sitemap, nor in the Wayback CDX index for the domain (newest Pillar 3 capture is the "
        f"2024 report, 11 June 2026).\n"
        f"RE-VERIFIED 2026-09-15 against the Bank's own LIVE publications index rather than by URL guessing - "
        f"{PUBLICATIONS_INDEX_URL}. That page lists Pillar 3 disclosures for 2017, 2018, 2019, 2020, 2021, "
        f"2022, 2023 and 2024 and NO 2025 edition, while listing the Annual Report 2025 - i.e. the Bank has "
        f"published its FY2025 annual report but not its FY2025 Pillar 3, exactly as the annual report says "
        f"('published as soon as practicable AFTER the publication of the annual report'). An unfiltered "
        f"Wayback CDX sweep of the whole gatehousebank.com domain (6,938 captures) independently returns the "
        f"same eight Pillar 3 documents and no 2025 one. So FY2025 is a live access gap that may simply close "
        f"on its own when the Bank publishes; it is worth re-checking this index before requesting the "
        f"document. The same index is what exposed the FY2017 disclosure this project had been missing.\n"
        f"FY2025 is therefore populated ONLY where the Annual Report 2025 prints a figure that is provably "
        f"on the same basis as the Pillar 3 series. That is true of the capital AMOUNTS and false of the "
        f"RATIOS, so they are treated differently:\n"
        f"  - AMOUNTS (same basis, used): the regulatory capital note on p.126 gives Total regulatory "
        f"capital of GBP111,120k for 2025 and GBP127,083k for 2024. That 2024 comparative equals the "
        f"GBP127.1m this workbook already carries from the FY2024 Pillar 3 disclosure, so the note is "
        f"like-for-like and FY2025 Total Capital is taken from it - {AR2025_URL}\n"
        f"  - RATIOS (different basis, NOT used): the Annual Report's KPI table (p.21) gives a 2025 CET1 "
        f"ratio of 15.74% and leverage ratio of 6.53%, but its own 2024 comparatives (16.56% and 7.29%) do "
        f"NOT match the FY2024 Pillar 3 figures carried here (17.1% and 7.4%). The Annual Report defines "
        f"its CET1 ratio as 'Tier 1 common equity / risk weighted assets' and its leverage ratio as 'Tier 1 "
        f"Capital / Total exposures' on an accounting exposure measure, which is not the Article 447 "
        f"basis. Mixing the two would create a false break in the series, so the CET1 Ratio, Tier 1 Ratio, "
        f"Total Capital Ratio and Leverage Ratio sheets are left blank for FY2025 rather than blended.\n"
        f"  - NOT PRINTED AT ALL: the Annual Report gives no RWA total, no LCR and no NSFR for 2025, so "
        f"those sheets are blank too. Its capital note also stops at components - Core Tier 1 subtotal "
        f"GBP109,790k less Deductions from CET1 GBP(17,609)k, plus Tier 2 GBP18,939k, totalling "
        f"GBP111,120k - without printing CET1 net of deductions, so the CET1 Capital and Tier 1 Capital "
        f"sheets are blank for FY2025 rather than carrying a figure this project would have had to compute "
        f"itself. (For reference, that subtraction on the 2024 column reproduces GBP108.6m, exactly the "
        f"FY2024 Pillar 3 CET1 figure used here, so the missing FY2025 CET1 is recoverable the moment the "
        f"Pillar 3 document is obtained - it is requestable from the Bank.)\n"
        f"RESTATEMENT NOTE: the FY2023 Pillar 3 disclosure's own Dec-22 comparative column shows CET1 "
        f"capital of GBP98.0m / RWA of GBP579.1m / ratios of 16.9%/16.9%/18.5% / leverage 7.1% - "
        f"different from the FY2022 disclosure's own Dec-22 ('T') figures used here (GBP103.2m / "
        f"GBP594.7m / 17.4%/17.4%/18.9% / 7.5%). LCR and NSFR at Dec-22 match exactly between both "
        f"vintages (350.7% and 150.6%), so only the capital-side figures were later restated. Each "
        f"year's own primary disclosure is used throughout, consistent with the rest of this workbook."
        + extra
    )


bw = BankWorkbook(bank_name="Gatehouse Bank Plc", years=YEARS, year_label=YEAR_LABEL, header_color="76773E")

STATEMENTS_SOURCES = (
    "Sources - Gatehouse Bank Plc's own Consolidated Statement of Financial Position / Consolidated "
    "Income Statement / Consolidated Statement of Changes in Equity:\n"
    f"FY2025/FY2024: Annual Report and Financial Statements 2025, p.56-59 - {AR2025_URL}\n"
    f"FY2023/FY2022: Annual Report and Financial Statements 2023, p.59-63 - {AR2023_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021, p.46-50 - {AR2021_URL}\n"
    f"FY2017: Annual Report and Financial Statements 2017, pp.33-36 - {AR2017_URL}\n"
    "Each year's own originally-published figures used. The equity roll-forward ties exactly at every "
    "boundary EXCEPT one genuine, disclosed restatement: the FY2023 Annual Report's own FY2022 "
    "comparative equity statement opens at 'Balance at 1 January 2022 (restated)' of GBP92,816k "
    "(attributable GBP91,513k + NCI GBP1,303k) - GBP19,836k lower than FY2021's own originally-published "
    "closing Total Equity of GBP112,652k. The gap exactly matches a new 'Non-controlling interest "
    "acquisition reserve' column (GBP(19,836)k) introduced from FY2022 onward that wasn't present in "
    "FY2021's own equity statement - shown here as an explicit 'Prior period restatement' bridging row "
    "(reproducing the disclosed component, not force-reconciling it), consistent with FY2021 using its "
    "own originally-published figures throughout the rest of this workbook.\n"
    "PRESENTATION NOTE: FY2021 carries a Foreign currency translation reserve and Investment in "
    "associate/Investment Properties lines that later years don't (associate/investment property "
    "disposed); FY2022-FY2023 introduce a Non-controlling interest acquisition reserve (renamed "
    "'Reserve as a result of subsidiary acquisition' from FY2024) and a Goodwill balance sheet line "
    "(written off/absorbed by FY2024); FY2024-FY2025 introduce Assets/Liabilities in disposal groups "
    "classified as held for sale and a Deferred tax asset line not itemised in FY2021's own filing. The "
    "Non-controlling interest is fully bought out by FY2023 (nil from FY2023's own statement onward, not "
    "shown as a column at all from FY2024). Income statement structure also evolves: FY2021 shows "
    "Loss/Gain on property held for sale and Gain on investment properties (FY2021-only, associated with "
    "the investment property later disposed) and a below-the-line 'Net share of profit of associate' "
    "(FY2021-only); FY2022-FY2023 report Profit/(loss) for the year from continuing operations "
    "separately from Profit after tax from discontinued operations; FY2024-FY2025 relabel this split as "
    "Loss after tax from continuing operations / Discontinued operation. Each year's own line items are "
    "used unchanged, blank cells where a line genuinely doesn't apply that year.\n"
    + ENTITY_NOTE
)

bw.add_balance_sheet_sheet(
    title="Gatehouse Bank Plc — Consolidated Balance Sheet",
    subtitle="Consolidated basis, £'000. See source note at bottom.",
    rows=[
        ("SECTION", "Assets", {}),
        ("DATA", "Cash and balances with banks",
         {"FY2025": 24599, "FY2024": 27823, "FY2023": 24596, "FY2022": 22845, "FY2021": 41598}),
        ("DATA", "Financing and advances at amortised cost",
         {"FY2025": 1264559, "FY2024": 1315936, "FY2023": 1357803, "FY2022": 1227896, "FY2021": 901111}),
        ("DATA", "Derivative financial instruments (asset)",
         {"FY2025": 2348, "FY2024": 11337, "FY2023": 33032, "FY2022": 34138, "FY2021": 2619}),
        ("DATA", "Fair value of hedged assets in portfolio hedges of interest rate risk",
         {"FY2025": 2377, "FY2024": -371}),
        ("DATA", "Financial assets held at FVTOCI",
         {"FY2025": 38098, "FY2024": 28282, "FY2023": 19512, "FY2022": 19351, "FY2021": 22951}),
        ("DATA", "Financial assets held at FVTIS",
         {"FY2025": 2827, "FY2024": 8228, "FY2023": 18278, "FY2022": 17061, "FY2021": 26366}),
        ("DATA", "Investment in associate", {"FY2021": 14298}),
        ("DATA", "Goodwill", {"FY2023": 4242, "FY2022": 4242, "FY2021": 4242}),
        ("DATA", "Intangible assets",
         {"FY2025": 2849, "FY2024": 6644, "FY2023": 1879, "FY2022": 1812, "FY2021": 1389}),
        ("DATA", "Property, plant and equipment and right-of-use assets",
         {"FY2025": 1126, "FY2024": 945, "FY2023": 1155, "FY2022": 1486, "FY2021": 1714}),
        ("DATA", "Assets in disposal groups classified as held for sale", {"FY2025": 13551}),
        ("DATA", "Property held for sale", {"FY2021": 4537}),
        ("DATA", "Other assets",
         {"FY2025": 36503, "FY2024": 8857, "FY2023": 4016, "FY2022": 2571, "FY2021": 5533}),
        ("DATA", "Deferred tax assets",
         {"FY2025": 9374, "FY2024": 7427, "FY2023": 5260, "FY2022": 4525}),
        ("TOTAL", "Total assets",
         {"FY2025": 1398211, "FY2024": 1415108, "FY2023": 1469773, "FY2022": 1335927, "FY2021": 1026358}),

        ("SECTION", "Liabilities", {}),
        ("DATA", "Financial liabilities measured at amortised cost",
         {"FY2025": 1287404, "FY2024": 1288977, "FY2023": 1316609, "FY2022": 1168586, "FY2021": 895637}),
        ("DATA", "Financial liabilities held at FVTIS", {"FY2021": 1340}),
        ("DATA", "Derivative financial instruments (liability)",
         {"FY2025": 2736, "FY2024": 11110, "FY2023": 44010, "FY2022": 61224, "FY2021": 5033}),
        ("DATA", "Other liabilities",
         {"FY2025": 7562, "FY2024": 8649, "FY2023": 6926, "FY2022": 7333, "FY2021": 11696}),
        ("DATA", "Liabilities directly associated with assets in disposal groups classified as held for sale",
         {"FY2025": 4743}),
        ("TOTAL", "Total liabilities",
         {"FY2025": 1302445, "FY2024": 1308736, "FY2023": 1367545, "FY2022": 1237143, "FY2021": 913706}),

        ("SECTION", "Equity", {}),
        ("DATA", "Share capital",
         {"FY2025": 150049, "FY2024": 150049, "FY2023": 150049, "FY2022": 150049, "FY2021": 150049}),
        ("DATA", "Fair value through other comprehensive income reserve",
         {"FY2025": -3616, "FY2024": -4377, "FY2023": -4721, "FY2022": -5275, "FY2021": -3848}),
        ("DATA", "Foreign currency translation reserve", {"FY2021": 1792}),
        ("DATA", "Reserve as a result of subsidiary acquisition",
         {"FY2025": -15917, "FY2024": -15917, "FY2023": -15917, "FY2022": -15917}),
        ("DATA", "Retained earnings/(deficit)",
         {"FY2025": -34750, "FY2024": -23383, "FY2023": -27183, "FY2022": -30073, "FY2021": -36644}),
        ("TOTAL", "Equity attributable to owners of the company",
         {"FY2025": 95766, "FY2024": 106372, "FY2023": 102228, "FY2022": 98784, "FY2021": 111349}),
        ("DATA", "Non-controlling interest", {"FY2023": 0, "FY2022": 0, "FY2021": 1303}),
        ("TOTAL", "Total equity",
         {"FY2025": 95766, "FY2024": 106372, "FY2023": 102228, "FY2022": 98784, "FY2021": 112652}),
        ("TOTAL", "Total equity and liabilities",
         {"FY2025": 1398211, "FY2024": 1415108, "FY2023": 1469773, "FY2022": 1335927, "FY2021": 1026358}),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=380,
    unit_suffix=" (£'000)",
)

bw.add_income_statement_sheet(
    title="Gatehouse Bank Plc — Consolidated Income Statement",
    subtitle="Consolidated basis, £'000. See source note at bottom.",
    rows=[
        ("SECTION", "Income", {}),
        ("DATA", "Income from financial assets held at amortised cost",
         {"FY2025": 65700, "FY2024": 66694, "FY2023": 55745, "FY2022": 42738, "FY2021": 33889}),
        ("DATA", "Charges to financial institutions and customers",
         {"FY2025": -50933, "FY2024": -51092, "FY2023": -32736, "FY2022": -18604, "FY2021": -15332}),
        ("DATA", "Fees and commission income",
         {"FY2025": 2704, "FY2024": 917, "FY2023": 10130, "FY2022": 9078, "FY2021": 9954}),
        ("DATA", "Fees and commission expense", {"FY2023": -127, "FY2022": -167, "FY2021": -164}),
        ("DATA", "Foreign exchange gains/(losses)",
         {"FY2025": 211, "FY2024": 137, "FY2023": 19, "FY2022": -834, "FY2021": -516}),
        ("DATA", "Net (losses)/gains from financial assets at FVTIS",
         {"FY2025": -2052, "FY2024": 2287, "FY2023": 1952, "FY2022": 5676, "FY2021": 756}),
        ("DATA", "Net gains from financial assets at FVTOCI",
         {"FY2025": 885, "FY2024": 344, "FY2023": 197, "FY2022": 376, "FY2021": 335}),
        ("DATA", "Other income/(loss)", {"FY2023": -231, "FY2022": 335, "FY2021": 2178}),
        ("DATA", "(Loss)/gain on property held for sale", {"FY2021": -472}),
        ("DATA", "Gain on investment properties", {"FY2021": 1412}),
        ("DATA", "Impairment (charge)/release",
         {"FY2025": -2725, "FY2024": 192, "FY2023": -847, "FY2022": -5714, "FY2021": -806}),
        ("TOTAL", "Total operating income",
         {"FY2025": 13790, "FY2024": 19479, "FY2023": 34102, "FY2022": 32884, "FY2021": 31234}),

        ("SECTION", "Expenses", {}),
        ("DATA", "Staff costs",
         {"FY2025": -19031, "FY2024": -14881, "FY2023": -20643, "FY2022": -19889, "FY2021": -18126}),
        ("DATA", "Depreciation and amortisation",
         {"FY2025": -1043, "FY2024": -931, "FY2023": -1302, "FY2022": -1319, "FY2021": -1222}),
        ("DATA", "Other operating expenses",
         {"FY2025": -8954, "FY2024": -7081, "FY2023": -9004, "FY2022": -9121, "FY2021": -9173}),
        ("TOTAL", "Total operating expenses",
         {"FY2025": -29028, "FY2024": -22893, "FY2023": -30949, "FY2022": -30329, "FY2021": -28521}),

        ("TOTAL", "Operating profit/(loss)",
         {"FY2025": -15238, "FY2024": -3414, "FY2023": 3153, "FY2022": 2555, "FY2021": 2713}),
        ("DATA", "Net share of profit of associate", {"FY2021": 904}),
        ("TOTAL", "Profit/(loss) before tax",
         {"FY2025": -15238, "FY2024": -3414, "FY2023": 3153, "FY2022": 2555, "FY2021": 3617}),
        ("DATA", "Tax",
         {"FY2025": 1947, "FY2024": 2167, "FY2023": 4, "FY2022": 3933, "FY2021": -153}),
        ("TOTAL", "Profit/(loss) for the year from continuing operations",
         {"FY2025": -13291, "FY2024": -1247, "FY2023": 3157, "FY2022": 6488, "FY2021": 3464}),
        ("DATA", "Profit for the year from discontinued operations",
         {"FY2025": 1924, "FY2024": 5047, "FY2023": 0, "FY2022": 1640}),
        ("TOTAL", "(Loss)/profit for the year",
         {"FY2025": -11367, "FY2024": 3800, "FY2023": 3157, "FY2022": 8128, "FY2021": 3464}),

        ("SECTION", "Other comprehensive income", {}),
        ("DATA", "Net gain/(loss) on FVTOCI investments",
         {"FY2025": 761, "FY2024": 344, "FY2023": 554, "FY2022": -1539, "FY2021": -382}),
        ("DATA", "Foreign currency translation gains/(losses) from investment in associate (discontinued operation)",
         {"FY2022": -1792, "FY2021": 244}),
        ("TOTAL", "Other comprehensive income/(loss) for the year",
         {"FY2025": 761, "FY2024": 344, "FY2023": 554, "FY2022": -3331, "FY2021": -138}),
        ("TOTAL", "Total comprehensive (loss)/income for the year",
         {"FY2025": -10606, "FY2024": 4144, "FY2023": 3711, "FY2022": 4797, "FY2021": 3326}),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=88,
    source_height=380,
    unit_suffix=" (£'000)",
)

EQUITY_HEADERS = [
    "Share capital", "FVTOCI reserve", "Foreign currency translation reserve",
    "Reserve as a result of subsidiary acquisition", "Retained earnings/(deficit)",
    "Equity attributable to owners", "Non-controlling interest", "Total equity",
]
bw.add_equity_changes_sheet(
    title="Gatehouse Bank Plc — Consolidated Statement of Changes in Equity",
    subtitle="Consolidated basis, £'000, chronological. See source note at bottom.",
    headers=EQUITY_HEADERS,
    rows=[
        ("TOTAL", "At 1 January 2021", (150049, -3434, 1548, None, -39680, 108483, 843, 109326)),
        ("DATA", "Recycle of gain on sale of OCI investments (FY2021)",
         (None, -32, None, None, 32, 0, None, 0)),
        ("DATA", "Unrealised loss on instruments at FVTOCI (FY2021)",
         (None, -382, None, None, None, -382, None, -382)),
        ("DATA", "Foreign currency translation gains from associate investments (FY2021)",
         (None, None, 244, None, None, 244, None, 244)),
        ("TOTAL", "Subtotal after other comprehensive income (FY2021)",
         (150049, -3848, 1792, None, -39648, 108345, 843, 109188)),
        ("DATA", "Profit for the year (FY2021)", (None, None, None, None, 3004, 3004, 460, 3464)),
        ("TOTAL", "At 31 December 2021", (150049, -3848, 1792, None, -36644, 111349, 1303, 112652)),

        ("DATA", "Prior period restatement — introduction of Non-controlling interest acquisition reserve (FY2022 opening)",
         (None, None, None, -19836, None, -19836, None, -19836)),
        ("TOTAL", "At 1 January 2022 (restated)",
         (150049, -3848, 1792, -19836, -36644, 91513, 1303, 92816)),
        ("DATA", "Recycle of gain on sale of OCI investments (FY2022)",
         (None, 112, None, None, -112, 0, None, 0)),
        ("DATA", "Unrealised loss on instruments at FVTOCI (FY2022)",
         (None, -1539, None, None, None, -1539, None, -1539)),
        ("DATA", "Foreign currency translation losses from investment in associate — discontinued operation (FY2022)",
         (None, None, -1792, None, None, -1792, None, -1792)),
        ("TOTAL", "Subtotal after other comprehensive income (FY2022)",
         (150049, -5275, 0, -19836, -36756, 88182, 1303, 89485)),
        ("DATA", "Profit for the year — continuing operations (FY2022)",
         (None, None, None, 228, 5043, 5271, 1217, 6488)),
        ("DATA", "Profit for the year — discontinued operations (FY2022)",
         (None, None, None, None, 1640, 1640, None, 1640)),
        ("DATA", "Acquisition of a subsidiary (FY2022)",
         (None, None, None, 3691, None, 3691, -2520, 1171)),
        ("TOTAL", "At 31 December 2022", (150049, -5275, 0, -15917, -30073, 98784, 0, 98784)),

        ("TOTAL", "At 1 January 2023", (150049, -5275, None, -15917, -30073, 98784, None, 98784)),
        ("DATA", "Unrealised gain on instruments at FVTOCI (FY2023)",
         (None, 554, None, None, None, 554, None, 554)),
        ("TOTAL", "Subtotal after other comprehensive income (FY2023)",
         (150049, -4721, None, -15917, -30073, 99338, None, 99338)),
        ("DATA", "Profit for the year (FY2023)", (None, None, None, None, 3157, 3157, None, 3157)),
        ("DATA", "Recycling of reserve on liquidation of subsidiary (FY2023)",
         (None, None, None, None, -267, -267, None, -267)),
        ("TOTAL", "At 31 December 2023", (150049, -4721, None, -15917, -27183, 102228, None, 102228)),

        ("TOTAL", "At 1 January 2024", (150049, -4721, None, -15917, -27183, 102228, None, 102228)),
        ("DATA", "Loss for the year — continuing operations (FY2024)",
         (None, None, None, None, -1247, -1247, None, -1247)),
        ("DATA", "Profit for the year — discontinued operations (FY2024)",
         (None, None, None, None, 5047, 5047, None, 5047)),
        ("DATA", "Other comprehensive income (FY2024)", (None, 344, None, None, None, 344, None, 344)),
        ("TOTAL", "Total comprehensive income for the year (FY2024)",
         (None, 344, None, None, 3800, 4144, None, 4144)),
        ("TOTAL", "At 31 December 2024", (150049, -4377, None, -15917, -23383, 106372, None, 106372)),

        ("TOTAL", "At 1 January 2025", (150049, -4377, None, -15917, -23383, 106372, None, 106372)),
        ("DATA", "Loss for the year — continuing operations (FY2025)",
         (None, None, None, None, -13291, -13291, None, -13291)),
        ("DATA", "Profit for the year — discontinued operations (FY2025)",
         (None, None, None, None, 1924, 1924, None, 1924)),
        ("DATA", "Other comprehensive income (FY2025)", (None, 761, None, None, None, 761, None, 761)),
        ("TOTAL", "Total comprehensive (loss)/income for the year (FY2025)",
         (None, 761, None, None, -11367, -10606, None, -10606)),
        ("TOTAL", "At 31 December 2025", (150049, -3616, None, -15917, -34750, 95766, None, 95766)),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=380,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) after tax from continuing operations",
     {"FY2025": -13291, "FY2024": -1248, "FY2023": 3157, "FY2022": 6488}),
    ("DATA", "Profit after tax from discontinued operations",
     {"FY2025": 1924, "FY2024": 5048, "FY2023": 0, "FY2022": 1640}),
    ("DATA", "Operating profit on ordinary activities after tax (combined, not split this year)",
     {"FY2021": 3464}),
    ("TOTAL", "Profit/(loss) after tax for the year",
     {"FY2025": -11367, "FY2024": 3800, "FY2023": 3157, "FY2022": 8128, "FY2021": 3464}),
    ("DATA", "Depreciation and amortisation",
     {"FY2025": 1043, "FY2024": 930, "FY2023": 1302, "FY2022": 1319, "FY2021": 1222}),
    ("DATA", "Impairment charge/(release)",
     {"FY2025": 2725, "FY2024": -192, "FY2023": 847, "FY2022": 5714, "FY2021": 806}),
    ("DATA", "(Negative)/positive revaluation of financial instruments held at FVTIS (unquoted investments)",
     {"FY2025": 207, "FY2024": -1969, "FY2023": -22, "FY2022": -2904, "FY2021": 210}),
    ("DATA", "Positive revaluation on investment properties", {"FY2021": -1412}),
    ("DATA", "Loss/(gain) on sale of property held for sale", {"FY2021": 472}),
    ("DATA", "Share in profit of associate", {"FY2023": 0, "FY2022": -1640, "FY2021": -904}),
    ("DATA", "Fair value movement in derivative financial instruments (non-cash adjustment)",
     {"FY2025": 1844, "FY2024": 341, "FY2023": -1083, "FY2022": -1634, "FY2021": 160}),
    ("DATA", "Foreign exchange (gains)/losses",
     {"FY2025": -321, "FY2024": -120, "FY2023": 145, "FY2022": -264, "FY2021": 461}),
    ("DATA", "Taxation/income tax expense (non-cash adjustment)",
     {"FY2025": -1947, "FY2024": -2167, "FY2023": -4, "FY2022": -3933, "FY2021": 153}),
    ("DATA", "Adjustment for assets/liabilities held for sale", {"FY2025": 3134, "FY2024": 3148}),
    ("DATA", "Net (increase)/decrease in other assets",
     {"FY2025": -30867, "FY2024": -964, "FY2023": -1712, "FY2022": 3007, "FY2021": -1816}),
    ("DATA", "Changes in financing and advances at amortised cost",
     {"FY2025": 52974, "FY2024": 36152, "FY2023": -130754, "FY2022": -332498, "FY2021": -199760}),
    ("DATA", "Fair value movement in derivative financial instruments (operating assets)",
     {"FY2025": -8196, "FY2024": -4080, "FY2023": -14824, "FY2022": 26558}),
    ("DATA", "Net investment in financial assets held at FVTIS", {"FY2021": 8683}),
    ("DATA", "Net investment in financial assets held at FVTOCI", {"FY2021": -286}),
    ("DATA", "Changes in assets and liabilities held for sale", {"FY2025": -4183, "FY2024": -3876}),
    ("DATA", "Intercompany payable/receivable", {"FY2025": 51, "FY2024": 0}),
    ("DATA", "Changes in financial liabilities measured at amortised cost",
     {"FY2025": -2094, "FY2024": -27632, "FY2023": -148024, "FY2022": 263503, "FY2021": 196339}),
    ("DATA", "Net increase/(decrease) in other liabilities",
     {"FY2025": 2578, "FY2024": -534, "FY2023": 156, "FY2022": -3953, "FY2021": 4565}),
    ("TOTAL", "Cash generated from operations", {"FY2025": 5581, "FY2024": 2837}),
    ("DATA", "Income tax paid (cash)",
     {"FY2025": -1506, "FY2024": -850, "FY2023": -592, "FY2022": -330}),
    ("TOTAL", "Net cash flow from/(used in) operating activities",
     {"FY2025": 4075, "FY2024": 1987, "FY2023": 4640, "FY2022": -38927, "FY2021": 12357}),

    ("SECTION", "Investing activities", {}),
    ("DATA", "Acquisitions of property, plant and equipment",
     {"FY2025": -278, "FY2024": -150, "FY2023": -416, "FY2022": -637, "FY2021": -632}),
    ("DATA", "Proceeds from sale of property, plant and equipment", {"FY2025": 57, "FY2024": 30}),
    ("DATA", "Acquisition of intangible assets",
     {"FY2025": -1535, "FY2024": -1057, "FY2023": -623, "FY2022": -878, "FY2021": -320}),
    ("DATA", "Purchases of financial assets held at FVOCI",
     {"FY2025": -14050, "FY2024": -15693, "FY2021": -17000}),
    ("DATA", "Proceeds from sale of financial assets held at FVTOCI",
     {"FY2025": 5098, "FY2024": 7254, "FY2023": 0, "FY2022": 2061, "FY2021": 11617}),
    ("DATA", "Purchase of financial assets held at FVTIS (unquoted investments)",
     {"FY2025": -143, "FY2024": -1775, "FY2023": -1195, "FY2022": -600}),
    ("DATA", "Held for sale investing activities", {"FY2025": -647, "FY2024": -1391}),
    ("DATA", "Proceeds from sale of financial assets held at FVTIS (unquoted investments)",
     {"FY2025": 4394, "FY2024": 14735, "FY2023": 0, "FY2022": 11468, "FY2021": 23238}),
    ("DATA", "Cash flow received from discontinued operations", {"FY2023": 0, "FY2022": 14253}),
    ("DATA", "Dividend received from associate", {"FY2021": 859}),
    ("DATA", "Investments in subsidiaries", {"FY2021": -437}),
    ("DATA", "Net proceeds from disposal of property held for sale",
     {"FY2023": 0, "FY2022": 4537, "FY2021": 0}),
    ("TOTAL", "Net cash flow from/(used in) investing activities",
     {"FY2025": -7104, "FY2024": 1953, "FY2023": -2234, "FY2022": 30204, "FY2021": 17325}),

    ("SECTION", "Financing activities", {}),
    ("DATA", "Acquisition of subsidiaries", {"FY2023": 0, "FY2022": -9218}),
    ("DATA", "Cash outflow for lease liabilities",
     {"FY2025": -267, "FY2024": -401, "FY2023": -701, "FY2022": -672, "FY2021": -724}),
    ("DATA", "Held for sale financing activities", {"FY2025": -40, "FY2024": -296}),
    ("TOTAL", "Net cash flow from/(used in) financing activities",
     {"FY2025": -307, "FY2024": -697, "FY2023": -701, "FY2022": -9890, "FY2021": -724}),

    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents",
     {"FY2025": -3336, "FY2024": 3243, "FY2023": 1705, "FY2022": -18613, "FY2021": 28958}),
    ("DATA", "Cash and cash equivalents at beginning of year",
     {"FY2025": 27823, "FY2024": 24596, "FY2023": 22845, "FY2022": 41598, "FY2021": 12644}),
    ("DATA", "Effect of exchange rate fluctuations on cash held",
     {"FY2025": 112, "FY2024": -16, "FY2023": 46, "FY2022": -140, "FY2021": -4}),
    ("TOTAL", "Cash and cash equivalents at end of year",
     {"FY2025": 24599, "FY2024": 27823, "FY2023": 24596, "FY2022": 22845, "FY2021": 41598}),

    ("SECTION", "Additional information on operational cash flows from profit and dividends", {}),
    ("DATA", "Profit paid", {"FY2025": 48829, "FY2024": 53847, "FY2023": 23431, "FY2022": 14671}),
    ("DATA", "Profit received", {"FY2025": 65797, "FY2024": 65387, "FY2023": 55817, "FY2022": 43043}),
    ("DATA", "Dividend received", {"FY2025": 0, "FY2024": 659, "FY2023": 845, "FY2022": 844}),
]

bw.add_cash_flow_sheet(
    title="Gatehouse Bank Plc — Consolidated Cash Flow Statement",
    subtitle="Consolidated basis, £'000. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=88,
    source_height=340,
    unit_suffix=" (£'000)",
)

bw.add_asset_quality_sheet(
    title="Gatehouse Bank Plc — Asset Quality",
    subtitle="Financing and advances at amortised cost, by IFRS 9 stage, £'000. Consolidated basis. See source note at bottom.",
    rows=[
        ("SECTION", "Gross carrying value, by IFRS 9 stage", {}),
        ("DATA", "Stage 1 (12m ECL)",
         {"FY2025": 1098978, "FY2024": 1155258, "FY2023": 1193879, "FY2022": 1113761, "FY2021": 812023}),
        ("DATA", "Stage 2 (lifetime ECL)",
         {"FY2025": 94477, "FY2024": 91462, "FY2023": 116499, "FY2022": 106426, "FY2021": 79034}),
        ("DATA", "Stage 3 (lifetime ECL)",
         {"FY2025": 83611, "FY2024": 79036, "FY2023": 57596, "FY2022": 17035, "FY2021": 13666}),
        ("TOTAL", "Total gross carrying value",
         {"FY2025": 1277066, "FY2024": 1325756, "FY2023": 1367974, "FY2022": 1237222, "FY2021": 904723}),

        ("SECTION", "Loss allowance, by IFRS 9 stage", {}),
        ("DATA", "Stage 1 (12m ECL)",
         {"FY2025": -1363, "FY2024": -790, "FY2023": -1379, "FY2022": -3108, "FY2021": -413}),
        ("DATA", "Stage 2 (lifetime ECL)",
         {"FY2025": -512, "FY2024": -497, "FY2023": -1362, "FY2022": -5586, "FY2021": -2468}),
        ("DATA", "Stage 3 (lifetime ECL)",
         {"FY2025": -10632, "FY2024": -8533, "FY2023": -7430, "FY2022": -632, "FY2021": -731}),
        ("TOTAL", "Total loss allowance",
         {"FY2025": -12507, "FY2024": -9820, "FY2023": -10171, "FY2022": -9326, "FY2021": -3612}),

        ("SECTION", "Carrying value under IFRS 9, by stage", {}),
        ("DATA", "Stage 1", {"FY2025": 1097615, "FY2024": 1154468, "FY2023": 1192500, "FY2022": 1110653, "FY2021": 811610}),
        ("DATA", "Stage 2", {"FY2025": 93965, "FY2024": 90965, "FY2023": 115137, "FY2022": 100840, "FY2021": 76566}),
        ("DATA", "Stage 3", {"FY2025": 72979, "FY2024": 70503, "FY2023": 50166, "FY2022": 16403, "FY2021": 12935}),
        ("TOTAL", "Total carrying value (Financing and advances at amortised cost)",
         {"FY2025": 1264559, "FY2024": 1315936, "FY2023": 1357803, "FY2022": 1227896, "FY2021": 901111}),

        ("SECTION", "Derived ratios", {}),
        ("DATA", "Stage 3 / total gross carrying value (NPL ratio)",
         {"FY2025": "6.55%", "FY2024": "5.96%", "FY2023": "4.21%", "FY2022": "1.38%", "FY2021": "1.51%"}),
        ("DATA", "Total loss allowance coverage (total allowance / total gross)",
         {"FY2025": "0.98%", "FY2024": "0.74%", "FY2023": "0.74%", "FY2022": "0.75%", "FY2021": "0.40%"}),
        ("DATA", "Stage 3 coverage (Stage 3 loss allowance / Stage 3 gross)",
         {"FY2025": "12.72%", "FY2024": "10.80%", "FY2023": "12.90%", "FY2022": "3.71%", "FY2021": "5.35%"}),
    ],
    sources_text=(
        "Sources - Gatehouse Bank Plc's own 'Financing and advances at amortised cost' note "
        "(Group), IFRS 9 stage split:\n"
        f"FY2025/FY2024: Annual Report and Financial Statements 2025, p.89-90 - {AR2025_URL}\n"
        f"FY2023/FY2022: Annual Report and Financial Statements 2023, p.93 - {AR2023_URL}\n"
        f"FY2021: Annual Report and Financial Statements 2021, p.78 - {AR2021_URL}\n"
        "Each year's own originally-published figures used - every stage split ties exactly to that "
        "year's own Total gross carrying value/loss allowance/carrying value and to the Balance Sheet's "
        "own Financing and advances at amortised cost line. Derived ratios independently computed from "
        "the disclosed stage figures (not restated). Note the growing Stage 3 balance/NPL ratio across "
        "the series reflects a genuine, disclosed deterioration in the Bank's property finance book, not "
        "a presentation change.\n"
        + ENTITY_NOTE
    ),
    first_col_width=64,
    source_height=300,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, page, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(page), note=note, first_col_width=48, source_height=260)


CET1_CAPITAL = {"FY2024": 108.6, "FY2023": 108.2, "FY2022": 103.2, "FY2021": 94.5, "FY2017": 95.6}
CET1_CAPITAL_DERIVED = {"FY2025": 92.2}
TOTAL_CAPITAL = {"FY2025": 111.1, "FY2024": 127.1, "FY2023": 126.7, "FY2022": 112.2, "FY2021": 103.5, "FY2017": 95.6}
TOTAL_RWA = {"FY2024": 636.7, "FY2023": 644.8, "FY2022": 594.7, "FY2021": 523.0, "FY2017": 256.2}
CET1_RATIO = {"FY2024": "17.1%", "FY2023": "16.8%", "FY2022": "17.4%", "FY2021": "18.1%", "FY2017": "37.3%"}
TOTAL_CAPITAL_RATIO = {"FY2024": "20.0%", "FY2023": "19.6%", "FY2022": "18.9%", "FY2021": "19.8%", "FY2017": "37.3%"}
LEVERAGE_RATIO = {"FY2024": "7.4%", "FY2023": "7.3%", "FY2022": "7.5%", "FY2021": "9.2%", "FY2017": "37.8%"}
LEVERAGE_EXPOSURE = {"FY2017": 253.3}
LCR = {"FY2024": "447.6%", "FY2023": "691.6%", "FY2022": "350.7%", "FY2021": "365.4%", "FY2017": "641.3%"}
LCR_BUFFER = {"FY2017": 25.4}
LCR_OUTFLOWS = {"FY2017": 4.0}
NSFR = {"FY2024": "153.5%", "FY2023": "151.1%", "FY2022": "150.6%"}

FY2017_NOTE = (
    "FY2017 RECOVERED 2026-09-15. These cells were previously blank on the stated ground that 'FY2017 "
    "Pillar 3 key metrics were not published in the 2017 annual report'. That was true of the annual "
    "report but the wrong document was checked: Gatehouse Bank published a standalone 'Pillar III "
    "Disclosure 2017', and it is listed on the Bank's own live publications index to this day "
    "(gatehousebank.com/about-us/corporate-governance, link 'gatehouse-bank-pillar-3-disclosure-2017'). "
    "It was retrieved and read this session. Its Key Metrics table (p.3) prints CET1 ratio 37.3%, Tier 1 "
    "ratio 37.3%, Total Capital Ratio 37.3%, Leverage Ratio 37.8% and LCR 641.3% at 31-Dec-17; s.5 "
    "Capital Resources (p.11) and Appendix 1 (Own Funds Disclosure, p.26) give Total regulatory capital "
    "of GBP95.6m; s.6 (p.12) states 'Total Risk Weighted assets as at 31 December 2017 amount to "
    "GBP256.2m'; Appendix II (p.27) gives Total leverage ratio exposure of GBP253.3m; and s.9 (p.19) "
    "gives a liquidity buffer of GBP25.4m against total net cash outflows of GBP4.0m.\n"
    "All three ratios reconcile to the amounts: 95.6/256.2 = 37.3%, 95.6/253.3 = 37.7% and the LCR "
    "buffer/outflow pair is consistent with 641.3% at the disclosed rounding of the outflow figure. "
    "BASIS NOTE: FY2017 predates the Bank's Article 447/UK KM1 template series (which begins FY2021 "
    "here), so the FY2017 figures come from the equivalent CRD IV-era disclosure rather than the KM1 "
    "template. The capital stack also differs in shape - in FY2017 the Bank held no Tier 2 at all, so "
    "CET1, Tier 1 and Total capital are all GBP95.6m and all three ratios are identically 37.3%; the "
    "GBP(19.7)m deduction for the significant investment in Gatehouse Capital is a FY2017-specific item "
    "that does not recur in the later years."
)

NO_AT1_NOTE = ("No Additional Tier 1 instruments disclosed in any year, so Tier 1 capital equals CET1 capital "
               "throughout. (Correction, this pass: the earlier wording here also claimed no Tier 2 "
               "instruments. That was wrong - the Bank does hold Tier 2 capital, which is why Total capital "
               "exceeds CET1 capital every year. Its own Annual Report 2025 regulatory capital note states "
               "Tier 2 Capital of GBP18,939k at 31 December 2025 and GBP18,500k at 31 December 2024.)")
NSFR_NOTE = ("Not disclosed for FY2021 - the Article 447 Key Metrics NSFR rows first appear from the FY2022 "
             "Pillar 3 disclosure onward. CONFIRMED 2026-09-15 by reading the FY2022 edition directly: its NSFR "
             "section prints 150.6% at 31 December 2022 and a four-quarter table for 2022 alone (Q4 150.6%, Q3 "
             "144.0%, Q2 144.5%, Q1 137.6%, average 144.2%) with NO 2021 comparative column anywhere - so there "
             "is no back-route to FY2021 through the later edition, and the blank is structural rather than "
             "unsourced.")

CET1_DERIVED_LABEL = ("Common Equity Tier 1 (CET1) capital — derived from Annual Report 2025 capital note "
                      "components (memo, not Pillar 3)")
CET1_DERIVED_NOTE = (
    "FY2025 MEMO ROW (added 2026-09-15). The Pillar 3 row above is deliberately blank for FY2025 because no "
    "FY2025 Pillar 3 disclosure has been published (see the source note). The Annual Report 2025 regulatory "
    "capital note (p.126) does not print CET1 net of deductions either, but it does print every component of "
    "it: Core Tier 1 subtotal GBP109,790k less Deductions from CET1 GBP(17,609)k = GBP92,181k, which plus "
    "Tier 2 GBP18,939k gives the GBP111,120k Total regulatory capital the note states. The same subtraction "
    "on that note's 2024 column yields GBP108,583k = the GBP108.6m FY2024 Pillar 3 CET1 figure carried above, "
    "exactly - so the arithmetic is validated against a known year. It is shown as a separate, clearly "
    "labelled memo row rather than merged into the Pillar 3 series: this is a subtotal completed from "
    "disclosed components of a single table, NOT a figure back-solved from a ratio, but it is still not the "
    "Bank's own published Pillar 3 number.")

metric("CET1 Capital", "£m", [("Common Equity Tier 1 (CET1) capital", CET1_CAPITAL), (CET1_DERIVED_LABEL, CET1_CAPITAL_DERIVED)], "32", note=FY2017_NOTE + "\n\n" + CET1_DERIVED_NOTE)
metric("CET1 Ratio", "%", [("CET1 ratio", CET1_RATIO)], "32", note=FY2017_NOTE)
metric("Tier 1 Capital", "£m", [("Tier 1 capital", CET1_CAPITAL), (CET1_DERIVED_LABEL.replace("Common Equity Tier 1 (CET1)", "Tier 1"), CET1_CAPITAL_DERIVED)], "32", note=NO_AT1_NOTE + "\n\n" + FY2017_NOTE + "\n\n" + CET1_DERIVED_NOTE)
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", CET1_RATIO)], "32", note=NO_AT1_NOTE + "\n\n" + FY2017_NOTE)
metric("Total Capital", "£m", [("Total capital", TOTAL_CAPITAL)], "32", note=FY2017_NOTE)
metric("Total Capital Ratio", "%", [("Total capital ratio", TOTAL_CAPITAL_RATIO)], "32", note=FY2017_NOTE)
metric("Total RWAs", "£m", [("Total risk-weighted exposure amount", TOTAL_RWA)], "32", note=FY2017_NOTE)

bw.add_rwa_breakdown_sheet(
    title="Gatehouse Bank Plc — RWA Breakdown",
    subtitle="Consolidated basis, £m. Pillar 1 credit risk RWA by exposure class + derived operational risk RWA. See source note at bottom.",
    rows=[
        ("SECTION", "Credit risk RWA, by exposure class (Standardised approach)", {}),
        ("DATA", "Cash and balances with banks",
         {"FY2024": 4.8, "FY2023": 4.5, "FY2022": 3.5, "FY2021": 3.6}),
        ("DATA", "Financing and advances at amortised cost",
         {"FY2024": 498.8, "FY2023": 499.3, "FY2022": 446.7, "FY2021": 356.3}),
        ("DATA", "Financial assets held at fair value through the income statement",
         {"FY2024": 10.9, "FY2023": 27.4, "FY2022": 25.6, "FY2021": 55.7}),
        ("DATA", "Financial assets at fair value through other comprehensive income",
         {"FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
        ("DATA", "Derivative financial instruments",
         {"FY2024": 6.2, "FY2023": 6.6, "FY2022": 6.8, "FY2021": 0.5}),
        ("DATA", "Investment in subsidiaries",
         {"FY2024": 29.3, "FY2023": 29.2, "FY2022": 26.4, "FY2021": 6.5}),
        ("DATA", "Investment in associates", {"FY2021": 28.3}),
        ("DATA", "Other assets",
         {"FY2024": 7.6, "FY2023": 4.3, "FY2022": 4.4, "FY2021": 3.9}),
        ("DATA", "Off balance sheet assets",
         {"FY2024": 6.3, "FY2023": 3.8, "FY2022": 12.9, "FY2021": 8.2}),
        ("TOTAL", "Credit risk RWA, total",
         {"FY2024": 563.9, "FY2023": 575.1, "FY2022": 526.3, "FY2021": 463.0}),

        ("DATA", "Operational risk RWA (derived: disclosed Pillar 1 capital requirement ÷ 8%)",
         {"FY2024": 52.5, "FY2023": 60.0, "FY2022": 47.5, "FY2021": 35.0}),
        ("DATA", "Market risk, CVA and other Pillar 1 RWA (residual — Total RWA less disclosed Credit "
                 "Risk and derived Operational Risk RWA)",
         {"FY2024": 20.3, "FY2023": 9.7, "FY2022": 20.9, "FY2021": 25.0}),
        ("TOTAL", "Total RWAs", {"FY2024": 636.7, "FY2023": 644.8, "FY2022": 594.7, "FY2021": 523.0}),
    ],
    sources_text=(
        "Sources - Gatehouse Bank Plc Pillar 3 disclosures:\n"
        "Credit risk RWA by exposure class - 'The table below breaks out the Bank's Pillar 1 capital "
        "requirements for credit risk' table (an image-only table, visually transcribed):\n"
        f"FY2024: Pillar III Disclosure 2024, p.14 - {P3_2024_URL}\n"
        f"FY2023: Pillar III Disclosure 2023, p.14 - {P3_2023_URL}\n"
        f"FY2022: Pillar III Disclosure 2022, p.15 - {P3_2022_URL}\n"
        f"FY2021: Pillar III Disclosure 2021, p.14 - {P3_2021_URL}\n"
        "Operational risk RWA is NOT disclosed directly - each year's Pillar 3 document states only the "
        "Bank's 'Pillar 1 capital requirements to meet operational risks' in £m (FY2024: 4.2, FY2023: "
        "4.8, FY2022: 3.8, FY2021: 2.8, from the same 4 documents' s.9 Operational Risk sections) - "
        "derived to RWA here by dividing by the Pillar 1 minimum ratio of 8%, per the same documents' "
        "own stated methodology. The Market risk/CVA/other residual row is NOT independently disclosed "
        "anywhere - it is the arithmetic gap between the disclosed Total RWA (from the Total RWAs metric "
        "sheet's own Article 447 Key Metrics source) and the sum of disclosed Credit Risk RWA plus "
        "derived Operational Risk RWA, shown explicitly rather than silently absorbed, since the Bank's "
        "own Pillar 3 narrative states it has 'no material exposure to market risk.' FY2025 blank - "
        "Pillar 3 disclosures not yet published as at build date (same gap as the other Pillar 3 sheets "
        "in this workbook).\n"
        "FY2025 RE-CHECKED 2026-09-15 AND STILL GENUINELY UNPUBLISHED, not a sourcing gap: the Bank's own "
        f"publications index ({PUBLICATIONS_INDEX_URL}) was fetched live on that date and lists Pillar III "
        "editions for 2017, 2018, 2019, 2020, 2021, 2022, 2023 and 2024 - and no 2025. Gatehouse's pattern is "
        "to publish the Pillar 3 well AFTER the Annual Report (the 2024 edition's asset-server timestamp is "
        "August 2025, five months behind the 2024 Annual Report), so the FY2025 column is expected to fill on "
        "a later pass rather than to require a different search. The 2018, 2019 and 2020 editions listed on "
        "that index are outside this workbook's year columns (FY2025-FY2021 plus FY2017) and were not "
        "transcribed; the 2018 edition was read to check whether it carried a FY2017 RWA comparative for this "
        "sheet, and it does not - its exposure/RWA tables are 31 December 2018 only.\n"
        "FY2017 BLANK - EXPLAINED, NOT UNCHECKED (2026-09-15): the Pillar III Disclosure 2017 was located "
        "and read this session, and it did populate the FY2017 column of every other regulatory metric "
        f"sheet in this workbook ({P3_2017_URL}). It cannot populate THIS sheet because it contains no "
        "credit-risk-RWA-by-exposure-class table at all. What it does give is only a whole-Bank split: "
        "Total RWA GBP256.2m against a Pillar 1 capital requirement of GBP20.5m (s.6, p.12; 20.5/0.08 = "
        "256.25, consistent), operational risk capital of GBP5.8m (s.9, p.24, implying c.GBP72.5m of "
        "operational risk RWA on the 8% basis this sheet already uses) and a nil Pillar 1 market risk "
        "charge (s.8, p.22). Appendix II (p.27) does break exposures down by class - sovereigns GBP13.0m, "
        "regional govt/MDB/PSE GBP13.9m, institutions GBP59.2m, secured by immovable property GBP82.0m, "
        "other GBP109.1m - but those are LEVERAGE EXPOSURE amounts, not risk-weighted amounts, and must "
        "not be entered in an RWA sheet. So FY2017 is a genuine absence of this particular breakdown in "
        "an otherwise complete disclosure, and is left blank rather than assembled from mismatched "
        "measures.\n"
        + ENTITY_NOTE
    ),
    first_col_width=76,
    source_height=380,
    unit_suffix=" (£m)",
)

metric("Leverage Ratio", "%", [("Leverage ratio excluding claims on central banks", LEVERAGE_RATIO), ("Total leverage ratio exposure (£m)", LEVERAGE_EXPOSURE)], "32", note=FY2017_NOTE)
metric("LCR", "%", [("Liquidity coverage ratio", LCR), ("Liquidity buffer (£m)", LCR_BUFFER), ("Total net cash outflows (£m)", LCR_OUTFLOWS)], "32", note=FY2017_NOTE)
metric("NSFR", "%", [("Net Stable Funding Ratio", NSFR)], "32", note=NSFR_NOTE + " FY2017 likewise predates the UK NSFR regime entirely (the PRA's NSFR requirement and its disclosure template took effect 1 January 2022 under PS17/21 and PS22/21), so the FY2017 blank here is structural, not a sourcing gap - the 2017 Pillar 3 disclosure, which supplied every other FY2017 metric in this workbook, contains no NSFR because none was required.")

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources("n/a"),
    per_note={"MREL Ratio": "Not publicly disclosed any year, no exemption stated - consistent with a "
                             "small deposit taker below MREL-setting thresholds."},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets",
         {"FY2025": 1398211, "FY2024": 1415108, "FY2023": 1469773, "FY2022": 1335927, "FY2021": 1026358}),
        ("Financing and advances at amortised cost",
         {"FY2025": 1264559, "FY2024": 1315936, "FY2023": 1357803, "FY2022": 1227896, "FY2021": 901111}),
        ("Financial liabilities measured at amortised cost",
         {"FY2025": 1287404, "FY2024": 1288977, "FY2023": 1316609, "FY2022": 1168586, "FY2021": 895637}),
        ("Total equity",
         {"FY2025": 95766, "FY2024": 106372, "FY2023": 102228, "FY2022": 98784, "FY2021": 112652}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total operating income",
         {"FY2025": 13790, "FY2024": 19479, "FY2023": 34102, "FY2022": 32884, "FY2021": 31234}),
        ("Total operating expenses",
         {"FY2025": -29028, "FY2024": -22893, "FY2023": -30949, "FY2022": -30329, "FY2021": -28521}),
        ("(Loss)/profit for the year",
         {"FY2025": -11367, "FY2024": 3800, "FY2023": 3157, "FY2022": 8128, "FY2021": 3464}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity",
         {"FY2025": 106372, "FY2024": 102228, "FY2023": 98784, "FY2022": 92816, "FY2021": 109326}),
        ("Total comprehensive (loss)/income for the year",
         {"FY2025": -10606, "FY2024": 4144, "FY2023": 3711, "FY2022": 4797, "FY2021": 3326}),
        ("Other equity movements, net",
         {"FY2025": 0, "FY2024": 0, "FY2023": -267, "FY2022": 1171, "FY2021": 0}),
        ("Closing equity",
         {"FY2025": 95766, "FY2024": 106372, "FY2023": 102228, "FY2022": 98784, "FY2021": 112652}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash flow from/(used in) operating activities",
         {"FY2025": 4075, "FY2024": 1987, "FY2023": 4640, "FY2022": -38927, "FY2021": 12357}),
        ("Net cash flow from/(used in) investing activities",
         {"FY2025": -7104, "FY2024": 1953, "FY2023": -2234, "FY2022": 30204, "FY2021": 17325}),
        ("Net cash flow from/(used in) financing activities",
         {"FY2025": -307, "FY2024": -697, "FY2023": -701, "FY2022": -9890, "FY2021": -724}),
        ("Cash and cash equivalents at end of year",
         {"FY2025": 24599, "FY2024": 27823, "FY2023": 24596, "FY2022": 22845, "FY2021": 41598}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Total Capital Ratio", TOTAL_CAPITAL_RATIO),
        ("Leverage Ratio", LEVERAGE_RATIO),
        ("LCR", LCR),
        ("NSFR", NSFR),
    ],
    note="Gatehouse Bank Plc is a UK Shariah-compliant (Islamic) bank; 'profit paid/received' is the "
         "functional equivalent of interest paid/received. FY2025 Pillar 3 ratios and RWA Breakdown are "
         "blank - not yet published as at build date. Opening equity for FY2022 (GBP92,816k) is "
         "GBP19,836k lower than FY2021's own closing Total equity (GBP112,652k) - a genuine, disclosed "
         "restatement (a new Non-controlling interest acquisition reserve introduced from FY2022), see "
         "the Statement of Changes in Equity sheet's source note. See the Cash Flow Statement sheet's "
         "source note for the 3-era presentation change and the FY2021/FY2022 cash flow restatement "
         "notes. Figures are duplicated from the detail sheets for at-a-glance trend viewing.",
)

# FY2017 statement extension.  The 2017 report is the Bank's own consolidated
# report (pp.33-36); values are rounded to the workbook's £'000 convention.
# Pillar 3 metrics remain blank because this predates the Bank's published
# Article 447/KM1 disclosure series.
_FY2017 = {
    "Balance Sheet": {
        "Cash and balances with banks": 11900,
        "Financing and advances at amortised cost": 85903,
        "Financial assets held at FVTOCI": 72095,
        "Financial assets held at FVTIS": 0,
        "Investment in associate": 15379,
        "Derivative financial instruments (asset)": 0,
        "Intangible assets": 339,
        "Property, plant and equipment and right-of-use assets": 13031,
        "Other assets": 4627,
        "Total assets": 280526,
        "Financial liabilities measured at amortised cost": 150077,
        "Other liabilities": 2481,
        "Total liabilities": 153065,
        "Share capital": 150049,
        "Foreign currency translation reserve": 1571,
        "Fair value through other comprehensive income reserve": -394,
        "Retained earnings/(deficit)": -23764,
        "Equity attributable to owners of the company": 127462,
        "Total equity": 127462,
        "Total equity and liabilities": 280526,
    },
    "Profit & Loss": {
        "Income from financial assets held at amortised cost": 9072,
        "Charges to financial institutions and customers": -3425,
        "Fees and commission income": 4062,
        "Fees and commission expense": 0,
        "Foreign exchange gains/(losses)": -276,
        "Realised gains/(losses) on investments": 769,
        "Other income": 560,
        "Total operating income": 10762,
        "Staff costs": -6790,
        "Depreciation and amortisation": -583,
        "Other operating expenses": -4008,
        "Total operating expenses": -11381,
        "Operating profit/(loss)": -620,
        "Net share of profit of associate": 1946,
        "Impairment (charge)/release": -1671,
        "Profit/(loss) before tax": -345,
        "Tax": -7,
        "Profit/(loss) for the year from continuing operations": -351,
        "Other comprehensive income/(loss) for the year": -1032,
        "Total comprehensive (loss)/income for the year": -1383,
    },
    "Cash Flow Statement": {
        "Cash and cash equivalents at end of year": 11900,
        "Net cash flow from/(used in) operating activities": 30046,
        "Net cash flow from/(used in) investing activities": 10353,
        "Net cash flow from/(used in) financing activities": -36904,
        "Net (decrease)/increase in cash and cash equivalents": 3494,
        "Cash and cash equivalents at beginning of year": 8406,
    },
}
for _sheet, _rows in _FY2017.items():
    _ws = bw.wb[_sheet]
    _labels = {str(_ws.cell(r, 1).value).strip(): r for r in range(4, _ws.max_row + 1)}
    _col = 1 + YEARS.index("FY2017") + 1
    for _label, _value in _rows.items():
        if _label in _labels:
            _ws.cell(_labels[_label], _col, _value)

bw.save("/Users/armaan/code/katalysis/banks/GATEHOUSE BANK FINANCIALS.xlsx")
