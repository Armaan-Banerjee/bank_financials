import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Cash flow statement exists for FY2016-FY2022 (31 March year-end) - see
# CASH_FLOW_EXEMPTION_NOTE below (only FY2023 onward is FRS 101-exempt). Pillar 3
# covers all 10 years, though FY2016/FY2017 have gaps (see p3_sources()).
YEARS = ["FY2026", "FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

CH_FILING_HISTORY_URL = "https://find-and-update.company-information.service.gov.uk/company/08632552/filing-history"
AR20_URL = "https://find-and-update.company-information.service.gov.uk/company/08632552/filing-history/MzI4MTUyNjc2OWFkaXF6a2N4/document?format=pdf&download=0"
AR19_URL = "https://find-and-update.company-information.service.gov.uk/company/08632552/filing-history/MzI0MTY5Njg4NGFkaXF6a2N4/document?format=pdf&download=0"
AR18_URL = "https://find-and-update.company-information.service.gov.uk/company/08632552/filing-history/MzIxNDUyMjk4M2FkaXF6a2N4/document?format=pdf&download=0"
AR17_URL = "https://find-and-update.company-information.service.gov.uk/company/08632552/filing-history/MzIxNDI0NDI5M2FkaXF6a2N4/document?format=pdf&download=0"
AR16_URL = "https://find-and-update.company-information.service.gov.uk/company/08632552/filing-history/MzE2MDEwMzEyNGFkaXF6a2N4/document?format=pdf&download=0"

P3_FY21_URL = "https://www.atombank.co.uk/~/docs/pillar-3-disclosures-20-21.pdf"
P3_FY22_URL = "https://www.atombank.co.uk/~/docs/pillar-3-disclosures-21-22.pdf"
P3_FY23_URL = "https://www.atombank.co.uk/~/docs/pillar-3-disclosures-22-23.pdf"
P3_FY24_URL = "https://www.atombank.co.uk/~/docs/atom-holdco-limited-pillar-3.pdf"
P3_FY25_URL = "https://www.atombank.co.uk/~/docs/pillar-3-disclosures-24-25.pdf"
P3_FY26_URL = "https://www.atombank.co.uk/~/docs/pillar-3-disclosures-25-26.pdf"
P3_FY20_URL = "http://web.archive.org/web/20221005223922id_/https://www.atombank.co.uk/~/docs/pillar-3-disclosures-19-20.pdf"
P3_FY19_URL = "http://web.archive.org/web/20221005205114id_/https://www.atombank.co.uk/~/docs/pillar-3-disclosures-18-19.pdf"
P3_FY18_URL = "http://web.archive.org/web/20221005211108id_/https://www.atombank.co.uk/~/docs/pillar-3-disclosures-17-18.pdf"
P3_FY17_URL = "http://web.archive.org/web/20221005211125id_/https://www.atombank.co.uk/~/docs/pillar-3-disclosures-16-17.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Atom Bank Plc (company 08632552, FRN 661960, matches Banks List 2608.xlsx exactly) is the "
    "PRA-authorised entity built here. During FY2023, a new non-trading holding company - Atom Holdco Limited "
    "(later re-registered Atom Holdco plc ahead of its 2025 IPO-track listing) - was inserted above Atom Bank "
    "Plc in the group structure. From that point, Atom Bank Plc became a wholly-owned subsidiary whose results "
    "are consolidated into Atom Holdco's own published financial statements, and Pillar 3 disclosures moved from "
    "being published at Bank level to being published at Holdco (Group) level, with a separate Bank-solo column "
    "shown alongside Group in the KM1 template from FY2023 onward. All Pillar 3 figures in this workbook use the "
    "Bank column (or, for FY2021-FY2022, the single pre-restructuring figure that IS the Bank, per each report's "
    "own note: 'the comparatives reflect the previous structure where Atom bank plc was the sole regulated "
    "entity') - so there is no cash-flow-vs-Pillar-3 basis mismatch here, unlike several other banks in this "
    "project."
)

CASH_FLOW_EXEMPTION_NOTE = (
    "CASH FLOW EXEMPTION NOTE (revised for HD-025): a Statement of Cash Flows exists for every year FY2016-FY2022 "
    "(called 'Cash flow statement(s)' in the source, Bank column used throughout) - the FY2016-FY2020 Companies "
    "House filings were fully scanned/image-only and read via page-render + visual reading (cross-verified "
    "against each later year's own comparative column, which in every case reproduced the prior year's figures "
    "exactly). Only from the FY2023 Annual Report onward (confirmed directly in the FY2023 and FY2025 filings) "
    "does Atom Bank Plc's accounting policies note state: 'The Bank is exempt by virtue of s400 of the Companies "
    "Act 2006 from the requirement to prepare group financial statements... The Bank is a qualifying entity as "
    "defined by Financial Reporting Standard 101... and therefore has adopted the reduced disclosure framework of "
    "FRS 101', explicitly listing 'IAS 7 Statement of cash flows' among the disclosures exempted - the same FRS "
    "101 'qualifying entity' exemption seen elsewhere in this project (ABC International Bank, BNY Mellon, United "
    "Trust Bank, ICICI, PNBE), but here - like Tandem Bank and AIB Group (UK) - taken only from a specific year "
    "onward rather than throughout the entity's whole history. FY2023-FY2025 are left blank on the Cash Flow "
    "Statement sheet rather than guessed."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Atom Bank Plc's own Bank-column 'Cash flow statement(s)', £'000, from its "
    "Companies House full accounts filings (Group of companies' accounts, which for FY2018-FY2022 present Group "
    "and Bank columns side by side):\n"
    f"FY2022: full accounts made up to 31 March 2022, filed 7 Sep 2022, p.65 (Cash flow statement, Bank column) - "
    f"{CH_FILING_HISTORY_URL}\n"
    f"FY2021: group of companies' accounts made up to 31 March 2021, filed 28 Sep 2021, p.48 (Cash flow "
    f"statements, Bank column) - {CH_FILING_HISTORY_URL}\n"
    f"FY2020: full accounts made up to 31 March 2020, filed 26 Jun 2020, p.46 (Cash flow statement, Bank column) - "
    f"{AR20_URL}\n"
    f"FY2019: full accounts made up to 31 March 2019, filed 22 Jul 2019, p.57 (Cash flow statement, Bank column) - "
    f"{AR19_URL}\n"
    f"FY2018: full accounts made up to 31 March 2018, filed 11 Jul 2018, p.45 (Cash flow statements, Bank column; "
    f"also gives the FY2017 comparative in full, used in preference to FY2017's own scan-degraded filing where "
    f"row labels were illegible) - {AR18_URL}\n"
    f"FY2016: full accounts made up to 31 March 2016, filed 22 Jul 2016, p.33 (Cash flow statement) - {AR16_URL}\n"
    "FY2021's own closing 'Cash and balances at central banks' (£316,827k) differs from FY2022's own opening "
    "figure for the same balance (£316,826k) by £1k - an immaterial rounding difference in the source documents "
    "themselves, kept as printed in each year's own report rather than force-corrected.\n\n"
    "FY2017 ROW-LABEL LEGIBILITY NOTE: FY2017's own Annual Report filing (an 11 Sep 2018 amended refiling) has a "
    "cash flow statement page with legible totals but illegible individual line-item labels/values (a scan "
    "artefact specific to that one page, confirmed by re-rendering at 200 DPI with no improvement) - so FY2017's "
    "detailed rows here are taken from FY2018's own report's FY2017 comparative column instead, which is fully "
    "legible and ties to the same totals printed (illegibly) in FY2017's own filing.\n\n"
    + ENTITY_NOTE + "\n\n" + CASH_FLOW_EXEMPTION_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - Atom Bank Plc (Bank-solo basis; Group basis where Bank=Group pre-restructuring, see ENTITY "
        "NOTE), Table UK KM1 - Key metrics (FY2021 onward) or each year's own 'Capital and leverage ratios' / "
        "'Own funds' / 'Summary of risk weighted assets' tables (FY2016-FY2020, pre-KM1 template), as at 31 March "
        "each year:\n"
        f"FY2026: Atom Holdco plc Pillar 3 Disclosures 2026, p.15 (4. Key metrics, '2026 Bank' column) - "
        f"{P3_FY26_URL}\n"
        f"FY2025: Atom Holdco plc Pillar 3 Disclosures 2025, p.13 (4. Key metrics, 'FY25 Bank' column) - "
        f"{P3_FY25_URL}\n"
        f"FY2024: Atom Holdco Limited Pillar 3 Disclosures 2024, p.13 (4. Key metrics, 'FY24 Bank' column) - "
        f"{P3_FY24_URL}\n"
        f"FY2023: Atom Holdco Limited Pillar 3 Disclosures 2023, p.12-13 (5. Key metrics) - {P3_FY23_URL}\n"
        f"FY2022: Atom Bank Plc Pillar 3 Disclosures 2021/22, p.17 (5. Key Metrics) - {P3_FY22_URL}\n"
        f"FY2021: Atom Bank Plc Pillar 3 Disclosures 2020/21, p.11 (3. Summary analysis) - {P3_FY21_URL}, "
        f"cross-checked against its identical appearance as the FY2021 comparative column in the FY2022 Pillar 3 "
        f"Disclosures above (both matched exactly).\n"
        f"FY2020: Atom Bank Plc Pillar 3 Disclosures 2019/20, Table 1/2/3 (Capital and leverage ratios / Own "
        f"funds / Summary of RWAs) - {P3_FY20_URL} (recovered via Wayback Machine, no longer live).\n"
        f"FY2019: Atom Bank Plc Pillar 3 Disclosures 2018/19, Table a/b/c, cross-checked against its identical "
        f"appearance as the FY2019 comparative in the FY2019/20 Pillar 3 Disclosures above - {P3_FY19_URL}.\n"
        f"FY2018: Atom Bank Plc Pillar 3 Disclosures 2017/18, Table a/b/c, cross-checked against its identical "
        f"appearance as the FY2018 comparative in the FY2018/19 Pillar 3 Disclosures above - {P3_FY18_URL}.\n"
        f"FY2017: Atom Bank Plc Pillar 3 Disclosures 2016/17 (Atom's first Pillar 3 disclosure, 'as at 31 March "
        f"2017'), Table 1/2/3 - {P3_FY17_URL}, cross-checked against its identical appearance as the FY2017 "
        f"comparative in the FY2017/18 Pillar 3 Disclosures above.\n"
        f"FY2016: the FY2016/17 Pillar 3 Disclosures' own FY2016 comparative column ({P3_FY17_URL}) - this is the "
        f"ONLY source for FY2016 Pillar 3 figures; no standalone FY2016 Pillar 3 document was ever published (the "
        f"FY2016/17 report explicitly states it is Atom's first Pillar 3 disclosure, prepared 'as at 31 March "
        f"2017' - FY2016 appears only as that report's own comparative).\n"
        "FY2024/FY2025/FY2026 figures were originally disclosed in £m and are shown here converted to £'000 "
        "(x1,000) for consistency with FY2021-FY2023's own £'000 presentation - ratios are unaffected by this "
        "unit change. The KM1 Key Metrics sheet does NOT apply that conversion: it reproduces each edition as "
        "printed, in two caption blocks (£m for FY2024-FY2026, £'000 for FY2022-FY2023), because a prescribed "
        "template must not be restated into a unit its own source never used."
        + extra
    )


bw = BankWorkbook(bank_name="Atom Bank Plc", years=YEARS, year_label=YEAR_LABEL, header_color="146C94")

AR26_URL = "https://find-and-update.company-information.service.gov.uk/company/08632552/filing-history/MzU0MDgxMjIwMGFkaXF6a2N4/document?format=pdf&download=0"
AR25_URL = "https://find-and-update.company-information.service.gov.uk/company/08632552/filing-history/MzQ3NzYwODYzOWFkaXF6a2N4/document?format=pdf&download=0"
AR24_URL = "https://find-and-update.company-information.service.gov.uk/company/08632552/filing-history/MzQzNDkxNDM0M2FkaXF6a2N4/document?format=pdf&download=0"
AR23_URL = "https://find-and-update.company-information.service.gov.uk/company/08632552/filing-history/MzM5ODE2MjM5N2FkaXF6a2N4/document?format=pdf&download=0"
AR21_URL = "https://find-and-update.company-information.service.gov.uk/company/08632552/filing-history/MzMxNDk5MDE0OWFkaXF6a2N4/document?format=pdf&download=0"

STATEMENT_ENTITY_NOTE = (
    "Bank (solo) basis throughout - the same basis as the pre-existing Cash Flow Statement and Pillar 3 sheets "
    "(see ENTITY NOTE below and on those sheets). FY2025/FY2024 come from the Atom Bank Plc full accounts filed "
    "with the FY2025 Companies House filing (Statement of financial position/Statement of comprehensive income/ "
    "Statement of changes in equity, pp.54-56), which is scanned/image-only - transcribed via page-render + "
    "visual reading rather than left blank, per the ABC International Bank precedent. FY2023/FY2022 come from "
    "the FY2023 filing (pp.52-54), also scanned/image-only. FY2021 comes from the FY2021 filing (pp.44-47, "
    "double-page-spread layout), Bank column (the Group column is not used, matching every other sheet's Bank "
    "basis). FY2016-FY2020 (added HD-025) are transcribed the same way from each year's own scanned/image-only "
    "Companies House filing - see each sheet's own source note for exact pages; FY2017's detail is sourced from "
    "FY2018's own comparative column instead of FY2017's own filing where the latter's scan quality makes row "
    "labels illegible (Cash Flow Statement only - Balance Sheet/P&L/Equity are legible in FY2017's own filing)."
    "\n\n" + ENTITY_NOTE
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents (FY2016 pre-product-launch presentation)", {"FY2016": 7240}),
    ("DATA", "Cash and balances at central banks", {"FY2026": 2619500, "FY2025": 1902200, "FY2024": 2405000, "FY2023": 4177488, "FY2022": 1453596, "FY2021": 316826, "FY2020": 269915, "FY2019": 225153, "FY2018": 364309, "FY2017": 419765}),
    ("DATA", "Financial investments - UK Treasury Bills and Gilts (FY2016 pre-IFRS 9 presentation)", {"FY2016": 6559}),
    ("DATA", "Debt instruments at fair value through other comprehensive income (total)", {"FY2026": 1245600, "FY2025": 1384500, "FY2024": 474700, "FY2023": 323978, "FY2022": 297334, "FY2021": 151052, "FY2020": 176733, "FY2019": 99072, "FY2018": 322361, "FY2017": 87249}),
    ("DATA", "Debt securities at FVOCI - UK Gilts & T-Bills", {"FY2026": 790600, "FY2025": 982600, "FY2024": 174600, "FY2023": 142297, "FY2022": 191363, "FY2021": 65036, "FY2020": 103717, "FY2019": 22032, "FY2018": 238136, "FY2017": 33970}),
    ("DATA", "Debt securities at FVOCI - Covered Bonds", {"FY2026": 349000, "FY2025": 351600, "FY2024": 290100, "FY2023": 142784, "FY2022": 70051, "FY2021": 79513, "FY2020": 54584, "FY2019": 49975, "FY2018": 20939, "FY2017": 20752}),
    ("DATA", "Debt securities at FVOCI - Residential Mortgage Backed Securities (RMBS)", {"FY2026": 76000, "FY2025": 50300, "FY2024": 7800, "FY2020": 1807, "FY2019": 10564, "FY2018": 11132, "FY2017": 10192}),
    ("DATA", "Debt securities at FVOCI - Multilateral Development Bank and Government Sponsored Debt", {"FY2026": 30000, "FY2024": 2200, "FY2023": 38897, "FY2022": 35920, "FY2021": 6503, "FY2020": 16625, "FY2019": 16501, "FY2018": 52154, "FY2017": 13295}),
    ("DATA", "Debt securities at FVOCI - Money Market Funds", {"FY2017": 9040}),
    ("DATA", "Debt instruments held at amortised cost", {"FY2026": 326800, "FY2025": 202500, "FY2024": 23000, "FY2023": 150273, "FY2022": 295103, "FY2021": 649503, "FY2020": 223311}),
    ("DATA", "Derivatives held for hedging purposes", {"FY2026": 47200, "FY2025": 55800, "FY2024": 62400, "FY2023": 76882, "FY2022": 36021, "FY2021": 4058, "FY2020": 736, "FY2018": 8008}),
    ("DATA", "Loans and advances to customers", {"FY2026": 5807500, "FY2025": 5301500, "FY2024": 4100900, "FY2023": 2958769, "FY2022": 2384066, "FY2021": 1638851, "FY2020": 1970818, "FY2019": 2399861, "FY2018": 1219356, "FY2017": 99209}),
    ("DATA", "Other assets", {"FY2026": 80100, "FY2025": 76700, "FY2024": 100100, "FY2023": 63182, "FY2022": 46845, "FY2021": 26077, "FY2020": 21634, "FY2019": 17931, "FY2018": 8649, "FY2017": 11482, "FY2016": 2445}),
    ("DATA", "Property, plant and equipment", {"FY2026": 12900, "FY2025": 600, "FY2024": 700, "FY2023": 3180, "FY2022": 4068, "FY2021": 4865, "FY2020": 5638, "FY2019": 562, "FY2018": 539, "FY2017": 722, "FY2016": 484}),
    ("DATA", "Intangible assets", {"FY2026": 37600, "FY2025": 38000, "FY2024": 41600, "FY2023": 37829, "FY2022": 36129, "FY2021": 35889, "FY2020": 36646, "FY2019": 29720, "FY2018": 34109, "FY2017": 30546, "FY2016": 19341}),
    ("DATA", "Current tax assets (FY2016 only; recognised as deferred thereafter)", {"FY2016": 1420}),
    ("DATA", "Deferred tax asset", {"FY2026": 49200, "FY2025": 29100, "FY2024": 16500, "FY2023": 9800, "FY2022": 5353}),
    ("TOTAL", "Total assets", {"FY2026": 10226400, "FY2025": 8990900, "FY2024": 7224900, "FY2023": 7801381, "FY2022": 4558515, "FY2021": 2827121, "FY2020": 2705431, "FY2019": 2772299, "FY2018": 1957331, "FY2017": 648973, "FY2016": 37489}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer deposits", {"FY2026": 8347600, "FY2025": 7538700, "FY2024": 5746200, "FY2023": 6551325, "FY2022": 3229796, "FY2021": 2154419, "FY2020": 1864812, "FY2019": 1771121, "FY2018": 1439793, "FY2017": 538060, "FY2016": 10}),
    ("DATA", "Borrowings from central banks", {"FY2026": 515900, "FY2025": 358200, "FY2024": 683800, "FY2023": 681403, "FY2022": 675749, "FY2021": 378093, "FY2020": 355481, "FY2019": 355437, "FY2018": 355215}),
    ("DATA", "Deemed loan", {"FY2026": 740700, "FY2025": 556100, "FY2024": 322400, "FY2023": 186864, "FY2022": 343856, "FY2021": 110700, "FY2020": 233091, "FY2019": 364204}),
    ("DATA", "Repurchase agreements", {"FY2019": 34851}),
    ("DATA", "Subordinated liabilities", {"FY2026": 50200, "FY2025": 50100, "FY2024": 0, "FY2023": 8201, "FY2022": 8192, "FY2021": 8180, "FY2020": 8166, "FY2019": 8149, "FY2018": 8134}),
    ("DATA", "Derivatives held for hedging purposes", {"FY2025": 200, "FY2024": 1100, "FY2023": 0, "FY2022": 108, "FY2021": 4422, "FY2020": 15113, "FY2019": 8628, "FY2017": 124}),
    ("DATA", "Provisions", {"FY2025": 900, "FY2024": 800, "FY2023": 425, "FY2022": 310, "FY2021": 197, "FY2020": 2752, "FY2019": 3585, "FY2018": 64, "FY2017": 132}),
    ("DATA", "Deferred tax liability", {"FY2026": 1500}),
    ("DATA", "Other liabilities", {"FY2026": 65900, "FY2025": 61500, "FY2024": 66800, "FY2023": 88532, "FY2022": 49410, "FY2021": 29780, "FY2020": 25513, "FY2019": 13620, "FY2018": 19154, "FY2017": 6575, "FY2016": 8183}),
    ("TOTAL", "Total liabilities", {"FY2026": 9721800, "FY2025": 8565700, "FY2024": 6821100, "FY2023": 7516750, "FY2022": 4307421, "FY2021": 2685791, "FY2020": 2504928, "FY2019": 2559595, "FY2018": 1822360, "FY2017": 544891, "FY2016": 8193}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital and share premium", {"FY2026": 144000, "FY2025": 128900, "FY2024": 128900, "FY2023": 29305, "FY2022": 566378, "FY2021": 448935, "FY2020": 448935, "FY2019": 399207, "FY2018": 246664, "FY2017": 167318, "FY2016": 54997}),
    ("DATA", "Other equity instruments (AT1)", {"FY2026": 49100}),
    ("DATA", "Other reserves", {"FY2026": 51700, "FY2025": 49200, "FY2024": 44700, "FY2023": 37379, "FY2022": 26875, "FY2021": 22627, "FY2020": 19421, "FY2019": 17405, "FY2018": 12358, "FY2017": 8135, "FY2016": 3501}),
    ("DATA", "Accumulated gains/(losses)", {"FY2026": 259800, "FY2025": 247100, "FY2024": 230200, "FY2023": 217947, "FY2022": -342159, "FY2021": -330232, "FY2020": -267853, "FY2019": -203908, "FY2018": -124051, "FY2017": -71371, "FY2016": -29202}),
    ("TOTAL", "Total equity", {"FY2026": 504600, "FY2025": 425200, "FY2024": 403800, "FY2023": 284631, "FY2022": 251094, "FY2021": 141330, "FY2020": 200503, "FY2019": 212704, "FY2018": 134971, "FY2017": 104082, "FY2016": 29296}),
    ("TOTAL", "Total liabilities and equity", {"FY2026": 10226400, "FY2025": 8990900, "FY2024": 7224900, "FY2023": 7801381, "FY2022": 4558515, "FY2021": 2827121, "FY2020": 2705431, "FY2019": 2772299, "FY2018": 1957331, "FY2017": 648973, "FY2016": 37489}),
]

BALANCE_SHEET_SOURCES = (
    "Sources - Statement of financial position, Bank basis, £'000:\n"
    f"FY2026: Atom bank plc Annual Report FY26 (full accounts made up to 31 March 2026, filed 25 Aug 2026), "
    f"p.58 (Statement of financial position); FVOCI issuer split from p.110 (Note 23, Assets held for liquidity "
    f"management) - {AR26_URL}\n"
    f"FY2025/FY2024: Atom Bank Plc full accounts made up to 31 March 2025, p.55 - {AR25_URL}\n"
    f"FY2023/FY2022: Atom Bank Plc full accounts made up to 31 March 2023, p.53 - {AR23_URL}\n"
    f"FY2021: Atom Bank Plc full accounts made up to 31 March 2021, p.45 (Bank column) - {AR21_URL}\n"
    f"FY2020/FY2019: Atom Bank Plc full accounts made up to 31 March 2020, p.43 (Bank column) - {AR20_URL}\n"
    f"FY2018/FY2017: Atom Bank Plc full accounts made up to 31 March 2018, p.43 (Bank column) - {AR18_URL}\n"
    f"FY2016: Atom Bank Plc full accounts made up to 31 March 2016, p.31 - {AR16_URL}\n"
    "FY2021's Bank statement carries no 'Deferred tax asset' line at all (Note 9 confirms no deferred tax asset "
    "was recognised that year - the Board only concluded it was appropriate to start recognising one from "
    "FY2022) - left blank rather than assumed zero. FY2021's Bank statement also carried a 'Debt securities in "
    "issue' line (£nil for Bank, £141,357k for Group) which no other year's statement shows - omitted as a "
    "row here since it is nil on the Bank basis used throughout, consistent with every other year."
    "\n\nHD-025 EXTENSION NOTES: FY2016 is Atom's first full-year balance sheet (the entity incorporated 31 July "
    "2014, prior period was an 8-month stub to 31 March 2015) - it predates any lending, debt-securities-at-FVOCI "
    "or IFRS 9 concept entirely (products only launched April-December 2016), so its own filing uses a materially "
    "simpler asset structure ('Cash and cash equivalents', 'Financial investments', 'Current tax assets' rather "
    "than 'Cash and balances at central banks', 'Debt instruments at FVOCI', 'Deferred tax asset') - kept as its "
    "own distinctly-named rows rather than force-mapped onto the later structure, since the underlying concepts "
    "genuinely differ (IFRS 9 was early-adopted only from FY2017). 'Deposits from banks' (FY2018's own label for "
    "the FY2018 figure) and 'Borrowings from central banks' (the same line's label from FY2019 onward, applied "
    "retrospectively to the FY2018 comparative in the FY2019 report) are the same underlying facility, shown "
    "under one row name. 'Repurchase agreements' first (and only) appears FY2019 - a real one-year financing "
    "instrument, not disclosed before or after."
    "\n\nINVESTMENT COMPOSITION EXTENSION NOTES: 'Financial investments' (FY2016) comprised entirely UK Treasury "
    "Bills and Gilts per Note 9 (Financial Investments), which states the balance 'comprise[s] UK Treasury Bills "
    "and Gilts and are valued by reference to a quoted market price, therefore included in IFRS13 Level 1' - "
    "Atom Bank Plc full accounts made up to 31 March 2016, p.44 - " + AR16_URL + ". Relabelled in place to name "
    "this single disclosed issuer type (100% one bucket, nothing to sub-split against) rather than left as a "
    "generic 'Financial investments' label that would otherwise fall into a default 'other' issuer-type bucket. "
    "The FY2016 filing predates IFRS 9/the FVOCI-vs-amortised-cost measurement-basis distinction entirely (see "
    "HD-025 note above) and doesn't use an AFS/trading/FVTPL label for this balance either, so no measurement-"
    "basis classification is asserted for this row - genuinely no further detail available on that dimension.\n\n"
    "'Debt instruments at fair value through other comprehensive income' is renamed to end '(total)' and split "
    "into disclosed issuer-type sub-rows for every year it has a value (FY2017-FY2025), each reconciling EXACTLY "
    "to the total - sourced from each report's own 'Assets held for liquidity management' note (or, for FY2023/"
    "FY2022, the equivalent Level 1 fair-value-hierarchy table in the fair values note, which breaks the same "
    "FVOCI total down by the same issuer categories): FY2025/FY2024 - Note 23, Atom Bank Plc full accounts made "
    "up to 31 March 2025, p.107 - " + AR25_URL + "; FY2023/FY2022 - Note 27 (Accounting for financial assets and "
    "liabilities - fair values), Atom Bank Plc full accounts made up to 31 March 2023, pp.118-119 - " + AR23_URL +
    "; FY2021 - Note 19, Atom Bank Plc full accounts made up to 31 March 2021, p.93 (Bank column) - " + AR21_URL +
    "; FY2020/FY2019 - Note 18, Atom Bank Plc full accounts made up to 31 March 2020, pp.85-86 (Bank column) - " +
    AR20_URL + "; FY2018/FY2017 - Note 18, Atom Bank Plc full accounts made up to 31 March 2018, p.81 - " +
    AR18_URL + ". 'Money Market Funds' appears as its own issuer-type sub-line in FY2017 only (£9,040k) - not "
    "disclosed in any other year. A 'Residential Mortgage Backed Securities (RMBS)' issuer-type sub-line is nil/"
    "not disclosed in FY2025/FY2023/FY2022/FY2021 (left blank rather than assumed zero, consistent with this "
    "workbook's convention); likewise 'Multilateral Development Bank and Government Sponsored Debt' is nil/not "
    "disclosed in FY2025. 'Debt instruments held at amortised cost' is NOT split - FY2020/FY2021's own note "
    "confirms this entire balance is retained RMBS notes from Atom's own Elvet mortgage securitisations (already "
    "correctly falling into the 'other' issuer-type bucket with no relabelling needed), and FY2022-FY2025's own "
    "notes disclose only the total with no further issuer-type breakdown - genuinely no further detail available "
    "for that row in those years."
    "\n\nFY2026 SOURCE AND PRESENTATION NOTES. (1) ENTITY: FY2026 is taken from ATOM BANK PLC's OWN Companies "
    "House filing, NOT from the Atom Holdco plc Annual Report published on atombank.co.uk. The Holdco report is "
    "consolidated group statements plus holding-company-only statements, and would be the wrong entity for these "
    "Bank-solo sheets however convenient it is to find. The Bank's own filing states the basis in terms: 'The "
    "Bank is therefore exempt by virtue of section 400 of the Companies Act 2006 from the requirement to prepare "
    "group financial statements. These financial statements present information about the Bank as an individual "
    "undertaking and not about its group' (p.60, Note 1b) - so it carries no Group column at all, unlike the "
    "FY2018-FY2022 filings. (2) UNIT: that filing is 'rounded to the nearest million (£'m)' (Note 1b), shown here "
    "x1,000 into £'000 on this sheet's stated unit, exactly as FY2024/FY2025 already were. (3) PRESENTATION "
    "CHANGE - two rows go blank for FY2026 rather than to zero: the FY2026 filing no longer shows 'Provisions' or "
    "the derivative LIABILITY as separate lines, folding both into 'Other liabilities'. Its own FY2025 "
    "comparative for that line is 62.6, which is this workbook's FY2025 Other liabilities 61,500 + Provisions 900 "
    "+ Derivatives 200 - so the balances did not disappear, the disclosure did. Those rows are left blank for "
    "FY2026 rather than forced to 0. (4) TWO NEW ROWS, both genuinely new instruments rather than relabelled "
    "ones: 'Other equity instruments (AT1)' 49,100 (AT1 capital issued in the year - it is also why KM1 row 2 "
    "Tier 1 exceeds row 1 CET1 for the first time) and 'Deferred tax liability' 1,500. (5) The FVOCI sub-rows "
    "reconcile EXACTLY to their own total for FY2026: 790,600 Gilts & T-Bills + 349,000 Covered Bonds + 76,000 "
    "RMBS + 30,000 Multilateral/Government Sponsored = 1,245,600. (6) THE FILING IS AN IMAGE-ONLY SCAN (144pp, "
    "~1 character of extractable text per page), so every FY2026 figure here was read by eye from 150 dpi page "
    "renders, not from text extraction; the primary statements were located from the document's own contents "
    "page (p.4, 'Financial statements 57') rather than by searching for digit-dense pages."
    "\n\n" + STATEMENT_ENTITY_NOTE
)

bw.add_balance_sheet_sheet(
    title="Atom Bank Plc - Statement of Financial Position",
    subtitle="Bank (solo) basis, £'000",
    rows=balance_sheet_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=62,
    source_height=430,
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2026": 510200, "FY2025": 441700, "FY2024": 440900, "FY2023": 208467, "FY2022": 76836, "FY2021": 42262, "FY2020": 46363, "FY2019": 37916, "FY2018": 13738, "FY2017": 725, "FY2016": 46}),
    ("DATA", "Interest expense", {"FY2026": -401300, "FY2025": -340400, "FY2024": -341800, "FY2023": -133218, "FY2022": -33566, "FY2021": -30199, "FY2020": -45135, "FY2019": -39800, "FY2018": -19367, "FY2017": -1601}),
    ("TOTAL", "Net interest income", {"FY2026": 108900, "FY2025": 101300, "FY2024": 99100, "FY2023": 75249, "FY2022": 43270, "FY2021": 12063, "FY2020": 1228, "FY2019": -1884, "FY2018": -5629, "FY2017": -876, "FY2016": 46}),
    ("DATA", "Net fee and commission expense", {"FY2021": -1072, "FY2020": -775, "FY2019": -1010, "FY2018": -264, "FY2017": -156, "FY2016": -28}),
    ("DATA", "Gain on disposal of assets held at amortised cost", {"FY2023": 0, "FY2022": 1749}),
    ("DATA", "Loss on disposal of assets held at amortised cost", {"FY2021": -9241, "FY2020": -9074}),
    ("DATA", "Other income", {"FY2023": 3083, "FY2022": 4099, "FY2018": 3573, "FY2017": 2}),
    ("DATA", "Other expense", {"FY2026": -200, "FY2025": -700, "FY2024": 0, "FY2020": -131, "FY2019": -1238}),
    ("DATA", "Other income/(expense)", {"FY2021": 188}),
    ("DATA", "Credit impairment charges", {"FY2026": -9400, "FY2025": -7100, "FY2024": -11000, "FY2023": -12768, "FY2022": -1100, "FY2021": -3652, "FY2020": -5783, "FY2019": -893, "FY2018": -256, "FY2017": -305}),
    ("TOTAL", "Net operating income/(expense)", {"FY2026": 99300, "FY2025": 93500, "FY2024": 88100, "FY2023": 65564, "FY2022": 48018, "FY2021": -1714, "FY2020": -14533, "FY2019": -5025, "FY2018": -2576, "FY2017": -1335, "FY2016": 18}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Staff costs", {"FY2026": -40100, "FY2025": -36900, "FY2024": -32700, "FY2023": -31347, "FY2022": -25882, "FY2021": -24183, "FY2020": -20554, "FY2019": -23026, "FY2018": -26707, "FY2017": -19321, "FY2016": -11580}),
    ("DATA", "Administrative and general expenses", {"FY2026": -33600, "FY2025": -31500, "FY2024": -28800, "FY2023": -27781, "FY2022": -24300, "FY2021": -22946, "FY2020": -19210, "FY2019": -20329, "FY2018": -17680, "FY2017": -18139, "FY2016": -11769}),
    ("TOTAL", "Staff and administrative expense", {"FY2026": -73700, "FY2025": -68400, "FY2024": -61500, "FY2023": -59128, "FY2022": -50182, "FY2021": -47129, "FY2020": -39764, "FY2019": -43355, "FY2018": -44387, "FY2017": -37460, "FY2016": -23349}),
    ("TOTAL", "Profit/(loss) before other charges", {"FY2026": 25600, "FY2025": 25100, "FY2024": 26600, "FY2023": 6436, "FY2022": -2164, "FY2021": -48843, "FY2020": -54297, "FY2019": -48380, "FY2018": -46963, "FY2017": -38795, "FY2016": -23331}),
    ("SECTION", "Other charges", {}),
    ("DATA", "Amortisation, depreciation and intangible impairment", {"FY2026": -13800, "FY2025": -13900, "FY2024": -12700, "FY2023": -11273, "FY2022": -10531, "FY2021": -10443, "FY2020": -7156, "FY2019": -23018, "FY2018": -5717, "FY2017": -3417, "FY2016": -604}),
    ("DATA", "Platform transformation costs", {"FY2021": -596, "FY2020": -300, "FY2019": -3500}),
    ("DATA", "Equity-settled share-based payments", {"FY2026": -2500, "FY2025": -6100, "FY2024": -7200, "FY2023": -5233, "FY2022": -4585, "FY2021": -2497, "FY2020": -2192, "FY2019": -4959}),
    ("TOTAL", "Other charges", {"FY2026": -16300, "FY2025": -20000, "FY2024": -19900, "FY2023": -16506, "FY2022": -15116, "FY2021": -13536, "FY2020": -9648, "FY2019": -31477, "FY2018": -5717, "FY2017": -3417, "FY2016": -604}),
    ("TOTAL", "Profit/(loss) before taxation", {"FY2026": 9300, "FY2025": 5100, "FY2024": 6700, "FY2023": -10070, "FY2022": -17280, "FY2020": -63945, "FY2019": -79857, "FY2018": -52680, "FY2017": -42212, "FY2016": -23935}),
    ("DATA", "Taxation credit/(expense)", {"FY2026": 18400, "FY2025": 11800, "FY2024": 5600, "FY2023": 4447, "FY2022": 5353, "FY2017": 43, "FY2016": 1420}),
    ("TOTAL", "Profit/(loss) for the year", {"FY2026": 27700, "FY2025": 16900, "FY2024": 12300, "FY2023": -5623, "FY2022": -11927, "FY2021": -62379, "FY2020": -63945, "FY2019": -79857, "FY2018": -52680, "FY2017": -42169, "FY2016": -22515}),
    ("SECTION", "Other comprehensive income/(expense), net of tax", {}),
    ("DATA", "Net (loss)/gain in fair value (fair value reserve)", {"FY2026": 1100, "FY2025": -400, "FY2024": 500, "FY2023": 117, "FY2022": -388, "FY2021": 725, "FY2020": -305, "FY2019": 171, "FY2018": -766, "FY2017": 317}),
    ("DATA", "Net amount transferred to profit or loss (fair value reserve)", {"FY2026": 0, "FY2025": 200, "FY2024": 100, "FY2023": -9, "FY2022": 51, "FY2021": -16, "FY2020": 129, "FY2019": -83, "FY2018": 95, "FY2017": 9}),
    ("DATA", "Net (losses)/gains from changes in fair value (cash flow hedge reserve)", {"FY2026": -1100, "FY2025": -1300, "FY2024": -400, "FY2023": 5163}),
    ("TOTAL", "Other comprehensive income/(expense), net of tax", {"FY2026": 0, "FY2025": -1500, "FY2024": 200, "FY2023": 5271, "FY2022": -337, "FY2021": 709, "FY2020": -176, "FY2019": 88, "FY2018": -671, "FY2017": 326}),
    ("TOTAL", "Total comprehensive income/(expense) for the year", {"FY2026": 27700, "FY2025": 15400, "FY2024": 12500, "FY2023": -352, "FY2022": -12264, "FY2021": -61670, "FY2020": -64121, "FY2019": -79769, "FY2018": -53351, "FY2017": -41843, "FY2016": -22515}),
]

INCOME_STATEMENT_SOURCES = (
    "Sources - Statement of comprehensive income, Bank basis, £'000:\n"
    f"FY2026: Atom bank plc Annual Report FY26 (full accounts made up to 31 March 2026, filed 25 Aug 2026), "
    f"p.57 (Statement of comprehensive income) - {AR26_URL}\n"
    f"FY2025/FY2024: Atom Bank Plc full accounts made up to 31 March 2025, p.54 - {AR25_URL}\n"
    f"FY2023/FY2022: Atom Bank Plc full accounts made up to 31 March 2023, p.52 - {AR23_URL}\n"
    f"FY2021: Atom Bank Plc full accounts made up to 31 March 2021, p.44 (Bank column) - {AR21_URL}\n"
    f"FY2020/FY2019: Atom Bank Plc full accounts made up to 31 March 2020, p.42 (Bank column) - {AR20_URL}\n"
    f"FY2018/FY2017: Atom Bank Plc full accounts made up to 31 March 2018, p.42 (Group and Bank identical both "
    f"years) - {AR18_URL}\n"
    f"FY2016: Atom Bank Plc full accounts made up to 31 March 2016, p.30 - {AR16_URL}\n"
    "HD-025 EXTENSION NOTE: FY2016-FY2018 predate the 'Net operating income/(expense)' and 'Profit/(loss) before "
    "other charges' subtotal labels used from FY2021 onward - their own reports use 'Net operating expense'/"
    "'Total expense' and 'Operating loss'/'Operating costs' for the same arithmetic positions (verified by "
    "reproducing each year's own running subtotals exactly). FY2016-FY2018 also predate the 'Platform "
    "transformation costs'/'Equity-settled share-based payments' split introduced from FY2019 - those years' "
    "share-based payment charges are folded into 'Staff costs' instead (not separately quantified in the source), "
    "and 'Amortisation, depreciation and intangible impairment' is labelled 'Amortisation and depreciation' before "
    "FY2019 - same concept, shown as a single line either way. FY2016 has no 'Other income'/'Credit impairment "
    "charges' lines at all (predates lending and had no non-interest income that year).\n"
    "PRESENTATION NOTE: the line-item structure changes materially across report vintages, kept as each year's "
    "own report presents it rather than forced into one shape - 'Net fee and commission expense' and 'Platform "
    "transformation costs' appear only in the FY2021 report; 'Loss on disposal of assets held at amortised "
    "cost' (FY2021, a genuine loss) is a different line from 'Gain on disposal of assets held at amortised "
    "cost' (FY2022/FY2023, a genuine gain, FY2023 nil); 'Other income' (FY2023/FY2022, a broader ~£3-4m income "
    "note aggregating fee income, hedge ineffectiveness and other items) is conceptually distinct from the "
    "small 'Other expense' line shown FY2025/FY2024 (-£0.7m/nil) and from FY2021's 'Other income/(expense)' "
    "(£0.19m) - all three are kept as separate rows rather than merged. FY2021's report shows 'Loss before and "
    "after taxation' as a single combined row with no separate pre-tax/taxation split (tax was nil that year) - "
    "'Profit/(loss) before taxation' and 'Taxation credit/(expense)' are left blank for FY2021 as a result, "
    "matching that report's own presentation. 'Total comprehensive income/(expense) for the year' is the one "
    "row genuinely comparable and populated across all 5 years."
    "\n\n" + STATEMENT_ENTITY_NOTE
)

bw.add_income_statement_sheet(
    title="Atom Bank Plc - Statement of Comprehensive Income",
    subtitle="Bank (solo) basis, £'000",
    rows=income_statement_rows,
    sources_text=INCOME_STATEMENT_SOURCES,
    first_col_width=68,
    source_height=260,
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
EQUITY_HEADERS = [
    "Share capital and share premium", "Other equity instruments", "Fair value reserve",
    "Cash flow hedge reserve", "Share-based payment reserve", "Accumulated gains/(losses)",
    "Total equity",
]

equity_changes_rows = [
    ("TOTAL", "Balance as at 1 April 2015 (opening FY2016)", (15607, None, None, None, 103, -6687, 9023)),
    ("DATA", "Issue of new ordinary shares, net of transaction costs (FY2016)", (39440, None, None, None, -103, None, 39337)),
    ("DATA", "Redemption of preference shares", (-50, None, None, None, None, None, -50)),
    ("DATA", "Share option scheme reserves (FY2016)", (None, None, None, None, 3501, None, 3501)),
    ("DATA", "Loss for the year (FY2016)", (None, None, None, None, None, -22515, -22515)),
    ("TOTAL", "Balance as at 31 March 2016", (54997, None, None, None, 3501, -29202, 29296)),
    ("DATA", "Loss for the year (FY2017)", (None, None, None, None, None, -42169, -42169)),
    ("DATA", "Net gain in fair value (FY2017)", (None, None, 317, None, None, None, 317)),
    ("DATA", "Net amount transferred to profit or loss (FY2017)", (None, None, 9, None, None, None, 9)),
    ("TOTAL", "Total comprehensive income/(expense) (FY2017)", (None, None, 326, None, None, -42169, -41843)),
    ("DATA", "Issue of new ordinary shares, net of transaction costs (FY2017)", (112321, None, None, None, None, None, 112321)),
    ("DATA", "Employee share schemes - value of services (FY2017)", (None, None, None, None, 4308, None, 4308)),
    ("TOTAL", "Balance as at 31 March 2017", (167318, None, 326, None, 7809, -71371, 104082)),
    ("DATA", "Loss for the year (FY2018)", (None, None, None, None, None, -52680, -52680)),
    ("DATA", "Net loss in fair value (FY2018)", (None, None, -766, None, None, None, -766)),
    ("DATA", "Net amount transferred to profit or loss (FY2018)", (None, None, 95, None, None, None, 95)),
    ("TOTAL", "Total comprehensive expense (FY2018)", (None, None, -671, None, None, -52680, -53351)),
    ("DATA", "Issue of new ordinary shares, net of transaction costs (FY2018)", (79346, None, None, None, None, None, 79346)),
    ("DATA", "Employee share schemes - value of services (FY2018)", (None, None, None, None, 4894, None, 4894)),
    ("TOTAL", "Balance as at 31 March 2018", (246664, None, -345, None, 12703, -124051, 134971)),
    ("DATA", "Loss for the year (FY2019)", (None, None, None, None, None, -79857, -79857)),
    ("DATA", "Net gain in fair value (FY2019)", (None, None, 171, None, None, None, 171)),
    ("DATA", "Net amount transferred to profit or loss (FY2019)", (None, None, -83, None, None, None, -83)),
    ("TOTAL", "Total comprehensive income/(expense) (FY2019)", (None, None, 88, None, None, -79857, -79769)),
    ("DATA", "Issue of new ordinary shares, net of transaction costs (FY2019)", (152543, None, None, None, None, None, 152543)),
    ("DATA", "Share schemes - value of services received (FY2019)", (None, None, None, None, 4959, None, 4959)),
    ("TOTAL", "Balance as at 31 March 2019", (399207, None, -257, None, 17662, -203908, 212704)),
    ("DATA", "Loss for the year (FY2020)", (None, None, None, None, None, -63945, -63945)),
    ("DATA", "Net loss in fair value (FY2020)", (None, None, -305, None, None, None, -305)),
    ("DATA", "Net amount transferred to profit or loss (FY2020)", (None, None, 129, None, None, None, 129)),
    ("TOTAL", "Total comprehensive income/(expense) (FY2020)", (None, None, -176, None, None, -63945, -64121)),
    ("DATA", "Issue of new ordinary shares, net of transaction costs (FY2020)", (49728, None, None, None, None, None, 49728)),
    ("DATA", "Share schemes - value of services received (FY2020)", (None, None, None, None, 2192, None, 2192)),
    ("TOTAL", "Balance as at 1 April 2020 (opening FY2021)", (448935, None, -433, None, 19854, -267853, 200503)),
    ("DATA", "Loss for the year (FY2021)", (None, None, None, None, None, -62379, -62379)),
    ("DATA", "Net gain in fair value", (None, None, 725, None, None, None, 725)),
    ("DATA", "Net amount transferred to profit or loss", (None, None, -16, None, None, None, -16)),
    ("TOTAL", "Total comprehensive income/(expense) (FY2021)", (None, None, 709, None, None, -62379, -61670)),
    ("DATA", "Share schemes - value of employee services", (None, None, None, None, 2497, None, 2497)),
    ("TOTAL", "Balance as at 31 March 2021", (448935, None, 276, None, 22351, -330232, 141330)),
    ("DATA", "Loss for the year (FY2022)", (None, None, None, None, None, -11927, -11927)),
    ("DATA", "Net loss in fair value", (None, None, -388, None, None, None, -388)),
    ("DATA", "Net amount transferred to profit or loss", (None, None, 51, None, None, None, 51)),
    ("TOTAL", "Total comprehensive expense (FY2022)", (None, None, -337, None, None, -11927, -12264)),
    ("DATA", "Issue of new ordinary shares, net of transaction costs", (117443, None, None, None, None, None, 117443)),
    ("DATA", "Share schemes - value of employee services", (None, None, None, None, 4585, None, 4585)),
    ("TOTAL", "Balance as at 31 March 2022", (566378, None, -61, None, 26936, -342159, 251094)),
    ("DATA", "Loss for the year (FY2023)", (None, None, None, None, None, -5623, -5623)),
    ("DATA", "Net gain in fair value", (None, None, 117, None, None, None, 117)),
    ("DATA", "Hedging adjustment (cash flow hedge reserve)", (None, None, None, 5163, None, None, 5163)),
    ("DATA", "Net amount transferred to profit or loss", (None, None, -9, None, None, None, -9)),
    ("TOTAL", "Total comprehensive income/(expense) (FY2023)", (None, None, 108, 5163, None, -5623, -352)),
    ("DATA", "Issue of new ordinary shares, net of transaction costs", (28656, None, None, None, None, None, 28656)),
    ("DATA", "Share premium reduction", (-565729, None, None, None, None, 565729, 0)),
    ("DATA", "Share schemes - value of employee services", (None, None, None, None, 5233, None, 5233)),
    ("TOTAL", "Balance as at 31 March 2023 (per FY2023 report)", (29305, None, 47, 5163, 32169, 217947, 284631)),
    ("TOTAL", "Balance as at 1 April 2023 (per FY2025 report - restated)", (29300, None, 0, 5200, 32100, 217900, 284500)),
    ("DATA", "Profit for the year (FY2024)", (None, None, None, None, None, 12300, 12300)),
    ("DATA", "Net gain in fair value", (None, None, 500, None, None, None, 500)),
    ("DATA", "Hedging adjustment (cash flow hedge reserve)", (None, None, None, -400, None, None, -400)),
    ("DATA", "Net amount transferred to profit or loss", (None, None, 100, None, None, None, 100)),
    ("TOTAL", "Total comprehensive income (FY2024)", (None, None, 600, -400, None, 12300, 12500)),
    ("DATA", "Issue of new ordinary shares, net of transaction costs", (99600, None, None, None, None, None, 99600)),
    ("DATA", "Share schemes - value of employee services", (None, None, None, None, 7200, None, 7200)),
    ("TOTAL", "Balance as at 31 March 2024", (128900, None, 600, 4800, 39300, 230200, 403800)),
    ("DATA", "Profit for the year (FY2025)", (None, None, None, None, None, 16900, 16900)),
    ("DATA", "Net loss in fair value", (None, None, -400, None, None, None, -400)),
    ("DATA", "Hedging adjustment (cash flow hedge reserve)", (None, None, None, -1300, None, None, -1300)),
    ("DATA", "Net amount transferred to profit or loss", (None, None, 200, None, None, None, 200)),
    ("TOTAL", "Total comprehensive income (FY2025)", (None, None, -200, -1300, None, 16900, 15400)),
    ("DATA", "Share schemes - value of employee services", (None, None, None, None, 6000, None, 6000)),
    ("TOTAL", "Balance as at 31 March 2025", (128900, None, 400, 3500, 45300, 247100, 425200)),
    ("DATA", "Profit for the year (FY2026)", (None, None, None, None, None, 27700, 27700)),
    ("DATA", "Net gain in fair value", (None, None, 1100, None, None, None, 1100)),
    ("DATA", "Hedging adjustment (cash flow hedge reserve)", (None, None, None, -1100, None, None, -1100)),
    ("TOTAL", "Total comprehensive income (FY2026)", (None, None, 1100, -1100, None, 27700, 27700)),
    ("DATA", "Issue of new ordinary shares, net of transaction costs", (15100, 49100, None, None, None, None, 64200)),
    ("DATA", "Dividend distribution", (None, None, None, None, None, -15000, -15000)),
    ("DATA", "Share schemes - value of employee services", (None, None, None, None, 2500, None, 2500)),
    ("TOTAL", "Balance as at 31 March 2026", (144000, 49100, 1500, 2400, 47800, 259800, 504600)),
]

EQUITY_CHANGES_SOURCES = (
    "Sources - Statement of changes in equity, Bank basis, £'000, read chronologically:\n"
    f"FY2026 movements: Atom bank plc Annual Report FY26 (full accounts made up to 31 March 2026, filed "
    f"25 Aug 2026), p.59 (Statement of changes in equity) - {AR26_URL}\n"
    "A NEW COLUMN WAS ADDED FOR FY2026: 'Other equity instruments'. Atom issued £49.1m of Additional Tier 1 "
    "(AT1) capital during FY2026 - an instrument it had never held before - and the closing balance cannot tie "
    "without it (144,000 + 49,100 + 1,500 + 2,400 + 47,800 + 259,800 = 504,600, which equals the Balance Sheet "
    "sheet's own Total equity for FY2026). Every pre-FY2026 row carries a blank in that column because the "
    "instrument did not exist, not because the figure is unknown. The same AT1 issue is why KM1 row 2 (Tier 1) "
    "exceeds row 1 (CET1) for the first time in Atom's history.\n"
    "The source prints the year's share issuance as a SINGLE row - 'Issue of new ordinary shares net of "
    "transaction costs', 15.1 into share capital and share premium and 49.1 into other equity instruments, "
    "64.2 in total - and it is reproduced here as one row on those two columns rather than split into two "
    "invented rows. FY2026 also carries the first dividend distribution (15,000) anywhere in this workbook's "
    "eleven-year history.\n"
    f"FY2016 movements: Atom Bank Plc full accounts made up to 31 March 2016, p.32 - {AR16_URL}\n"
    f"FY2017 movements: Atom Bank Plc full accounts made up to 31 March 2018, p.44 (Bank column - FY2017's own "
    f"filing is legible for this statement, but FY2018's report gives the same FY2017 movements with clearer "
    f"per-row detail) - {AR18_URL}\n"
    f"FY2018 movements: Atom Bank Plc full accounts made up to 31 March 2018, p.44 (Bank column) - {AR18_URL}\n"
    f"FY2019 movements: Atom Bank Plc full accounts made up to 31 March 2019, p.56 (Bank column) - {AR19_URL}\n"
    f"FY2020 movements: Atom Bank Plc full accounts made up to 31 March 2020, p.43 (Bank column) - {AR20_URL}\n"
    "The Bank-basis rollforward carries no treasury-shares column (treasury shares are a Group-only "
    "consolidation of the Employee Benefit Trust - see the pre-existing FY2021+ note on this) so none is added "
    "here either. FY2016's opening balance (1 April 2015) and its 'Issue of new ordinary shares' row combine "
    "the source's own separate 'Share capital' and 'Share premium account' columns into this sheet's single "
    "'Share capital and share premium' column, consistent with every later year; that same FY2016 row also shows "
    "a genuine £103k reversal in the 'Other reserves' (Share-based payment reserve) column, printed exactly as "
    "the source shows it, not smoothed away.\n"
    f"FY2021/FY2022 movements: Atom Bank Plc full accounts made up to 31 March 2021, p.46-47 (Bank balance rollforward, "
    f"1 April 2020 to 31 March 2021) - {AR21_URL}\n"
    f"FY2022/FY2023 movements: Atom Bank Plc full accounts made up to 31 March 2023, p.54 (1 April 2021 to 31 March 2023) - {AR23_URL}\n"
    f"FY2024/FY2025 movements: Atom Bank Plc full accounts made up to 31 March 2025, p.56 (1 April 2023 to 31 March 2025) - {AR25_URL}\n"
    "DISCREPANCY FLAGGED, not silently reconciled: the FY2023 report's own precise closing balance as at 31 "
    "March 2023 (£'000: 29,305 / 47 / 5,163 / 32,169 / 217,947 / 284,631) does not exactly match the FY2025 "
    "report's own restated opening balance as at 1 April 2023 (£m, converted to £'000: 29,300 / ~0 / 5,200 / "
    "32,100 / 217,900 / 284,500) for the same date - a ~£131k gap driven mainly by the FY2025 report disclosing "
    "in £m (1 decimal place) rather than FY2023's own £'000 precision, plus the fair value reserve rounding to "
    "nil. Both rows are shown rather than picking one, and all FY2024/FY2025 movements and closing balances are "
    "taken from the FY2025 report's own £m figures as printed (×1,000) so that report's own arithmetic ties out "
    "exactly (Balance as at 31 March 2025 = 425,200 = the Balance Sheet sheet's own Total equity for FY2025)."
    "\n\nThe 'Other reserves and treasury shares' column used in the FY2021 report's Bank statement (nil "
    "throughout FY2020-FY2021, no treasury shares held by the Bank) and the 'Cash flow hedge reserve' column "
    "(introduced only from FY2022's hedging activity onward) are genuine structural differences across report "
    "vintages, not errors - reflected here as blank cells rather than forced to zero or merged."
    "\n\n" + ENTITY_NOTE
)

bw.add_equity_changes_sheet(
    title="Atom Bank Plc - Statement of Changes in Equity",
    subtitle="Bank (solo) basis, £'000, read chronologically oldest to newest",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQUITY_CHANGES_SOURCES,
    source_height=280,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Loss for the year", {"FY2022": -11927, "FY2021": -62379, "FY2020": -63945, "FY2019": -79857, "FY2018": -52680, "FY2017": -42169, "FY2016": -22515}),
    ("DATA", "Depreciation and amortisation", {"FY2022": 10531, "FY2021": 10442, "FY2020": 7156, "FY2019": 12416, "FY2018": 5717, "FY2017": 3417, "FY2016": 604}),
    ("DATA", "Deferred tax asset recognised", {"FY2022": -5353}),
    ("DATA", "Impairment of intangible assets", {"FY2021": 0, "FY2019": 10602}),
    ("DATA", "Property, plant and equipment disposal (FY2018-FY2019 only)", {"FY2018": 16}),
    ("DATA", "Intangible assets adjustments and write-off (FY2016 only)", {"FY2016": 2295}),
    ("DATA", "Share option scheme reserves", {"FY2022": 4585, "FY2021": 2497, "FY2020": 2192, "FY2019": 4959, "FY2018": 4894, "FY2017": 4308, "FY2016": 3501}),
    ("DATA", "Other non cash movements", {"FY2022": -345, "FY2021": 1307, "FY2020": -1201, "FY2019": 3609, "FY2018": -85, "FY2017": 763}),
    ("DATA", "Loans and advances to customers", {"FY2022": -745215, "FY2021": 331967, "FY2020": 429043, "FY2019": -1180505, "FY2018": -1120403, "FY2017": -99514}),
    ("DATA", "Customer deposits", {"FY2022": 1075377, "FY2021": 289607, "FY2020": 93691, "FY2019": 331328, "FY2018": 901733, "FY2017": 538050, "FY2016": 10}),
    ("DATA", "Borrowing(s) from central banks", {"FY2022": 297656, "FY2021": 22612, "FY2020": 44, "FY2019": 222, "FY2018": 355215}),
    ("DATA", "Deemed loan", {"FY2022": 233156, "FY2021": -122391, "FY2020": -131113, "FY2019": 364204}),
    ("DATA", "Debt securities in issue", {"FY2022": 0, "FY2021": 0, "FY2020": 0}),
    ("DATA", "Debt instruments/securities held at amortised cost", {"FY2022": 354400, "FY2021": -426192, "FY2020": -223311}),
    ("DATA", "Repurchase agreements", {"FY2021": 0, "FY2020": -34851, "FY2019": 34851}),
    ("DATA", "Net increase in subordinated liabilities (FY2019 only)", {"FY2019": 15}),
    ("DATA", "Net decrease in tax asset (FY2017 only)", {"FY2017": 1420}),
    ("DATA", "Other assets", {"FY2022": -20768, "FY2021": -4443, "FY2020": -3703, "FY2019": -9282, "FY2018": 2833, "FY2017": -9037, "FY2016": -239}),
    ("DATA", "Other liabilities and provisions", {"FY2022": 20413, "FY2021": 1828, "FY2020": 7063, "FY2019": -5534, "FY2018": 12578, "FY2017": -1608}),
    ("DATA", "Derivatives held for hedging purposes", {"FY2022": -36277, "FY2021": -14013, "FY2020": 5749, "FY2019": 16636, "FY2018": -8132, "FY2017": 124}),
    ("DATA", "Net increase in financial investments (FY2016 only, pre-lending)", {"FY2016": -6559}),
    ("DATA", "Net decrease in trade receivables (FY2016 only)", {"FY2016": 37}),
    ("DATA", "Net increase in tax asset (FY2016 only)", {"FY2016": -806}),
    ("DATA", "Net increase in trade and other payables (FY2016 only)", {"FY2016": 5115}),
    ("TOTAL", "Net Cash Inflow/(Outflow) in Operating Activities", {"FY2022": 1176233, "FY2021": 30842, "FY2020": 86814, "FY2019": -496336, "FY2018": 101686, "FY2017": 395754, "FY2016": -18557}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Acquisition of intangible assets", {"FY2022": -9707, "FY2021": -8641, "FY2020": -13105, "FY2019": -18355, "FY2018": -8996, "FY2017": -14356}),
    ("DATA", "Payments for software (FY2016 only)", {"FY2016": -18417}),
    ("DATA", "Payments for banking licence (FY2016 only)", {"FY2016": -8}),
    ("DATA", "Acquisition of property, plant and equipment", {"FY2022": -267, "FY2021": -271, "FY2020": -297, "FY2019": -297, "FY2018": -117, "FY2017": -504, "FY2016": -247}),
    ("DATA", "Net (acquisition)/maturity of debt securities at FVOCI", {"FY2022": -146282, "FY2021": 25681, "FY2020": -77661, "FY2019": 223289, "FY2018": -244151, "FY2017": -71650}),
    ("TOTAL", "Net Cash (Outflow)/Inflow from Investing Activities", {"FY2022": -156256, "FY2021": 16769, "FY2020": -91063, "FY2019": 204637, "FY2018": -253264, "FY2017": -86510, "FY2016": -18672}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Proceeds from issuance of shares, net of expenses", {"FY2022": 117443, "FY2021": 0, "FY2020": 49728, "FY2019": 152543, "FY2018": 79346, "FY2017": 112321, "FY2016": 39337}),
    ("DATA", "Redemption of preference shares (FY2016 only)", {"FY2016": -50}),
    ("DATA", "Proceeds from issuance of subordinated debt (FY2018 only)", {"FY2018": 7935}),
    ("DATA", "Interest paid on subordinated debt (FY2018 only)", {"FY2018": -199}),
    ("DATA", "Purchase of treasury shares", {"FY2021": 0}),
    ("DATA", "Payment of principal portion of lease liabilities", {"FY2022": -650, "FY2021": -699, "FY2020": -717}),
    ("TOTAL", "Net Cash Inflow/(Outflow) from Financing Activities", {"FY2022": 116793, "FY2021": -699, "FY2020": 49011, "FY2019": 152543, "FY2018": 87082, "FY2017": 112321, "FY2016": 39287}),
    ("TOTAL", "Net Increase in Cash and Balances at Central Banks", {"FY2022": 1136770, "FY2021": 46912, "FY2020": 44762, "FY2019": -139156, "FY2018": -64496, "FY2017": 421565, "FY2016": 2058}),
    ("DATA", "Cash and balances at central banks at beginning of year", {"FY2022": 316826, "FY2021": 269915, "FY2020": 225153, "FY2019": 364309, "FY2018": 428805, "FY2017": 7240, "FY2016": 5182}),
    ("TOTAL", "Cash and Balances at Central Banks at the End of the Year", {"FY2022": 1453596, "FY2021": 316827, "FY2020": 269915, "FY2019": 225153, "FY2018": 364309, "FY2017": 428805, "FY2016": 7240}),
]

bw.add_cash_flow_sheet(
    title="Atom Bank Plc — Statement of Cash Flows",
    subtitle="Bank (solo) basis, £'000. FY2023-FY2026 blank - see source note at bottom (FRS 101 cash-flow exemption).",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=74,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Gross carrying amount by product", {}),
    ("DATA", "Mortgages", {"FY2026": 4597900, "FY2025": 4251500, "FY2024": 3242600, "FY2023": 2148481, "FY2022": 1487122, "FY2021": 976553, "FY2020": 1711375, "FY2019": 2194159, "FY2018": 1063880, "FY2017": 26627}),
    ("DATA", "BBSL (secured business lending)", {"FY2026": 1074700, "FY2025": 838700, "FY2024": 607900, "FY2023": 511831, "FY2022": 497305, "FY2021": 351978, "FY2020": 239953, "FY2019": 182526, "FY2018": 138391, "FY2017": 32880}),
    ("DATA", "BBUL (unsecured business lending)", {"FY2026": 188800, "FY2025": 256600, "FY2024": 307300, "FY2023": 389427, "FY2022": 439465, "FY2021": 310158}),
    ("DATA", "Structured/Unsecured funding loan note (FY2017-FY2019 predecessor product, matured by FY2020)", {"FY2019": 6967, "FY2018": 20743, "FY2017": 39865}),
    ("TOTAL", "Total gross carrying amount", {"FY2026": 5861400, "FY2025": 5346800, "FY2024": 4157800, "FY2023": 3049739, "FY2022": 2423892, "FY2021": 1638689, "FY2020": 1951328, "FY2019": 2383652, "FY2018": 1223014, "FY2017": 99372}),
    ("SECTION", "Gross carrying amount by IFRS 9 stage", {}),
    ("DATA", "Stage 1: 12 month expected loss", {"FY2026": 5509300, "FY2025": 5004400, "FY2024": 3881700, "FY2023": 2819585, "FY2022": 1970916, "FY2021": 1513908, "FY2020": 1782301, "FY2019": 2328035, "FY2018": 1191973, "FY2017": 99372}),
    ("DATA", "Stage 2: Lifetime - loans not credit impaired", {"FY2026": 280400, "FY2025": 292200, "FY2024": 239900, "FY2023": 195537, "FY2022": 428042, "FY2021": 117989, "FY2020": 164024, "FY2019": 51079, "FY2018": 31040}),
    ("DATA", "Stage 3: Lifetime - credit impaired loans", {"FY2026": 71700, "FY2025": 50200, "FY2024": 36200, "FY2023": 34617, "FY2022": 24934, "FY2021": 6792, "FY2020": 5003, "FY2019": 4538}),
    ("TOTAL", "Total gross carrying amount (by stage)", {"FY2026": 5861400, "FY2025": 5346800, "FY2024": 4157800, "FY2023": 3049739, "FY2022": 2423892, "FY2021": 1638689, "FY2020": 1951328, "FY2019": 2383652, "FY2018": 1223014, "FY2017": 99372}),
    ("SECTION", "Fair value / effective interest rate adjustments (pre-FY2021 presentation only)", {}),
    ("DATA", "Fair value adjustment", {"FY2020": 21254, "FY2019": 10300, "FY2018": -6714}),
    ("DATA", "Effective interest rate adjustment", {"FY2020": 4913, "FY2019": 7265, "FY2018": 3448}),
    ("TOTAL", "Total gross carrying amount including valuation adjustments", {"FY2020": 1977495, "FY2019": 2401217, "FY2018": 1219748, "FY2017": 99372}),
    ("SECTION", "Expected credit loss provision", {}),
    ("DATA", "Mortgages", {"FY2026": 7800, "FY2025": 5900, "FY2024": 5100, "FY2023": 3618, "FY2022": 1257, "FY2021": 577, "FY2020": 1891, "FY2019": 849, "FY2018": 299, "FY2017": 7}),
    ("DATA", "BBSL", {"FY2026": 2800, "FY2025": 3300, "FY2024": 3000, "FY2023": 2678, "FY2022": 2479, "FY2021": 4076, "FY2020": 3649, "FY2019": 279, "FY2018": 93, "FY2017": 156}),
    ("DATA", "BBUL", {"FY2026": 9600, "FY2025": 9200, "FY2024": 11900, "FY2023": 10042, "FY2022": 5751, "FY2021": 5086}),
    ("DATA", "Structured/Unsecured funding loan note", {"FY2019": 0, "FY2018": 0, "FY2017": 0}),
    ("TOTAL", "Total provision for on balance sheet impairment losses", {"FY2026": 20200, "FY2025": 18400, "FY2024": 20000, "FY2023": 16338, "FY2022": 9487, "FY2021": 9739, "FY2020": 6677, "FY2019": 1356, "FY2018": 392, "FY2017": 163}),
    ("SECTION", "Net balance sheet carrying value by product", {}),
    ("DATA", "Mortgages", {"FY2026": 4558600, "FY2025": 4219800, "FY2024": 3200400, "FY2023": 2070110, "FY2022": 1455268, "FY2021": 985758, "FY2020": 1736335, "FY2019": 2210717, "FY2018": 1060245, "FY2017": 26620}),
    ("DATA", "BBSL", {"FY2026": 1069600, "FY2025": 834300, "FY2024": 604900, "FY2023": 509153, "FY2022": 494826, "FY2021": 347902, "FY2020": 234483, "FY2019": 182176, "FY2018": 138354, "FY2017": 32724}),
    ("DATA", "BBUL", {"FY2026": 179300, "FY2025": 247400, "FY2024": 295600, "FY2023": 379506, "FY2022": 433972, "FY2021": 305191}),
    ("DATA", "Structured/Unsecured funding loan note", {"FY2019": 6968, "FY2018": 20757, "FY2017": 39865}),
    ("TOTAL", "Net balance sheet carrying value", {"FY2026": 5807500, "FY2025": 5301500, "FY2024": 4100900, "FY2023": 2958769, "FY2022": 2384066, "FY2021": 1638851, "FY2020": 1970818, "FY2019": 2399861, "FY2018": 1219356, "FY2017": 99209}),
    ("SECTION", "Asset quality ratios", {}),
    ("DATA", "Total coverage ratio (ECL provision / gross carrying amount)", {"FY2026": "0.33%", "FY2025": "0.33%", "FY2024": "0.44%", "FY2023": "0.48%", "FY2022": "0.36%", "FY2021": "0.53%", "FY2020": "0.34%", "FY2019": "0.06%", "FY2018": "0.03%", "FY2017": "0.16%"}),
    ("DATA", "Stage 3 / NPL ratio (Stage 3 gross / total gross carrying amount)", {"FY2026": "1.22%", "FY2025": "0.94%", "FY2024": "0.87%", "FY2023": "1.14%", "FY2022": "1.03%", "FY2021": "0.41%", "FY2020": "0.26%", "FY2019": "0.19%", "FY2018": "0.00%", "FY2017": "0.00%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 ECL provision / Stage 3 gross)", {"FY2026": "10.46%", "FY2025": "13.55%", "FY2024": "17.96%", "FY2023": "11.47%", "FY2022": "11.37%", "FY2021": "17.90%"}),
]

ASSET_QUALITY_SOURCES = (
    "Sources - Note 'Loans and advances to customers', Bank/Group basis (Atom's retail lending is on a single "
    "Bank basis for this note in every year, unlike the primary statements), £'000:\n"
    f"FY2026: Atom bank plc Annual Report FY26 (full accounts made up to 31 March 2026, filed 25 Aug 2026), "
    f"p.72 (Note 9, Loans and advances to customers) - {AR26_URL}\n"
    f"FY2025/FY2024: Atom Bank Plc full accounts made up to 31 March 2025, p.69 - {AR25_URL}\n"
    f"FY2023/FY2022: Atom Bank Plc full accounts made up to 31 March 2023, p.69-70 - {AR23_URL}\n"
    f"FY2021: Atom Bank Plc full accounts made up to 31 March 2021, p.72-73 (comparatives disclosed there for "
    f"FY2021/FY2020) - {AR21_URL}\n"
    f"FY2020: full accounts made up to 31 March 2020, p.34 (own year, not the FY2021 comparative) - {AR20_URL}\n"
    f"FY2019: full accounts made up to 31 March 2019, p.78 - {AR19_URL}\n"
    f"FY2018: full accounts made up to 31 March 2018, p.66 - {AR18_URL}\n"
    f"FY2017: same FY2018 filing, p.67 (a standalone FY2017-only table, not a side-by-side comparative column - "
    f"used because FY2017's own filing has this note on a scan-degraded page) - {AR18_URL}\n"
    "FY2026 NOTES. The FY2026 filing is an image-only scan, so Note 9 was read by eye from a 300/150 dpi render "
    "rather than extracted as text. Two independent checks passed on that reading: the net carrying value it "
    "gives (4,558.6 + 1,069.6 + 179.3 = 5,807.5) equals the Statement of financial position's own 'Loans and "
    "advances to customers' on p.58, and the same table's FY2025 comparative column reproduces THIS WORKBOOK'S "
    "existing FY2025 column exactly (5,004.4 / 292.2 / 50.2 gross by stage; 5.9 / 3.3 / 9.2 provision by "
    "product; 5,301.5 net) - transcribed here a year earlier from a different document.\n"
    "RATIOS: 'Total coverage ratio' 0.33% for FY2026 is PRINTED in Note 9 (as are the per-product 0.16% / 0.24% "
    "/ 5.08%), not calculated here. The 'Stage 3 / NPL ratio' and 'Stage 3 coverage ratio' rows are NOT printed "
    "by the bank in any year and are computed on this sheet's own long-standing stated formulas - FY2026: "
    "71,700 / 5,861,400 = 1.22%, and 7,500 / 71,700 = 10.46%, where 7,500 is Note 9's own Stage 3 line of the "
    "expected credit loss provision (3.4/1.9/2.5 by stage for mortgages etc. summing to 7.4 / 5.3 / 7.5 across "
    "the three products).\n"
    "KNOWN GAP, RECORDED RATHER THAN HALF-FIXED: Note 9 also prints a fair value adjustment of £(25.0)m and an "
    "effective interest rate adjustment of £(8.7)m for FY2026 (and £(19.8)m / £(7.1)m for FY2025), which would "
    "belong in the 'Fair value / effective interest rate adjustments' block above. That block is captioned "
    "'pre-FY2021 presentation only' and is blank for FY2021-FY2025, so filling FY2026 alone would create a "
    "one-year island and imply those adjustments did not exist in between, when in fact they were simply not "
    "carried. FY2026 is therefore left blank to match, and the whole block is flagged for a follow-up ticket to "
    "back-fill FY2021-FY2026 consistently from each year's own filing.\n"
    "'Total gross carrying amount' (by product) and 'Total gross carrying amount (by stage)' are the same "
    "underlying figure shown two ways (by product vs by IFRS 9 stage) and tie out exactly for every year "
    "(each product's own stage 1+2+3 gross carrying amounts sum to that product's own total row in the source "
    "table) - the by-stage total is what ties to the Balance Sheet's Loans and advances to customers line (net "
    "of the ECL provision below) for every year. Ratios are "
    "the Bank's own disclosed 'Total coverage ratio' row (FY2023-FY2021, FY2020, FY2019) or its FY2025/FY2024 "
    "equivalent, plus Stage 3/NPL and Stage 3 coverage ratios calculated here from the disclosed stage-level "
    "figures - FY2018/FY2017 don't disclose a 'Total coverage ratio' row at all, so it is calculated here "
    "throughout for consistency.\n\n"
    "HD-025 EXTENSION NOTES: FY2017-FY2020 use bank-specific 'Mortgages/BBSL/Structured Loan Note' (FY2017-2018) "
    "or 'Mortgages/BBSL/Unsecured funding loan note' (FY2019) product naming, pre-dating the 'BBUL' label used "
    "from FY2021 onward - kept as its own row rather than merged into BBUL, since it is a distinct, now-matured "
    "product line (fully wound down by FY2020, which shows only Mortgages/BBSL). FY2018-FY2020 also disclose "
    "separate 'Fair value adjustment' and 'Effective interest rate adjustment' lines reconciling the stage-based "
    "gross carrying amount to the balance-sheet carrying amount (a valuation-basis presentation dropped from "
    "FY2021 onward) - shown here as their own section. FY2016 has no Asset Quality data at all - the bank had "
    "not yet launched lending products that year (see STATEMENT_ENTITY_NOTE / balance sheet HD-025 notes), a "
    "genuine self-skip, not an omission."
    "\n\n" + STATEMENT_ENTITY_NOTE
)

bw.add_asset_quality_sheet(
    title="Atom Bank Plc - Asset Quality / Credit Risk Disclosures",
    subtitle="Bank basis, £'000 (ratios as stated/calculated)",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    source_height=260,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Bank basis, {unit}" if unit else "Bank basis",
                         rows_data, sources_text, note=note, first_col_width=52, source_height=180)


# ---------------------------------------------------------------
# Sheet: KM1 Key Metrics (the bank's own published UK KM1 template)
# ---------------------------------------------------------------
# TWO CAPTION BLOCKS, AND WHY. Atom's own presentation unit CHANGES between
# editions: FY2022 and FY2023 print the template in £'000, FY2024 onward in
# £m. One row cannot carry both without restating one edition's amounts into
# the other's unit - which is normalising a prescribed disclosure. So every
# AMOUNT row appears twice, each block labelled with the unit its own source
# printed; RATIO rows are unit-free and stay single. The single-metric sheets
# take the opposite approach by long-standing project convention (everything
# converted to £'000, stated in their source note) - that is a presentation
# choice available to a summary sheet, not to a reproduced template.
KM1_SOURCES = (
    "Sources - Table UK KM1 'Key metrics', ATOM BANK PLC ('Bank') column, as at 31 March each year. Each year is "
    "transcribed from ITS OWN edition, never from a later edition's comparative column:\n"
    f"FY2026: Atom Holdco plc Pillar 3 Disclosures 2026, p.15 (4. Key metrics) - {P3_FY26_URL}\n"
    f"FY2025: Atom Holdco plc Pillar 3 Disclosures 2025, p.13 (4. Key metrics) - {P3_FY25_URL}\n"
    f"FY2024: Atom Holdco Limited Pillar 3 Disclosures 2024, p.13 (4. Key metrics) - {P3_FY24_URL}\n"
    f"FY2023: Atom Holdco Limited Pillar 3 Disclosures 2023, pp.12-13 (5. Key metrics) - {P3_FY23_URL}\n"
    f"FY2022: Atom Bank Plc Pillar 3 Disclosures 2021/22, p.17 (5. Key Metrics) - {P3_FY22_URL}\n\n"
    "ENTITY (the single most important choice on this sheet). From FY2023 the template is published by the "
    "HOLDING COMPANY and prints Group and Bank side by side - FY2026 carries four columns (2026 Group, 2026 Bank, "
    "2025 Group, 2025 Bank). Every figure here is the BANK column, because this workbook is Atom Bank Plc "
    "(company 08632552, FRN 661960), the PRA-authorised entity. The Group column is a different entity and is "
    "never substituted, even where it is the only one discussed in the surrounding narrative. FY2022's edition "
    "predates the holding company and prints a single column that IS the Bank. The two differ materially and "
    "visibly: FY2026 CET1 is 363.6 Group against 365.2 Bank, and total RWAs 2,739.7 Group against 2,728.8 Bank.\n\n"
    "FY2021 AND EARLIER ARE DELIBERATELY BLANK - THE TEMPLATE IS NOT USED, which is a different finding from "
    "'no Pillar 3 exists'. The FY2020/21 edition publishes '3. Summary analysis': prose ratios plus two bespoke "
    "tables (an own-funds build-up and a 'Summary of risk weighted assets'). It carries no row numbers, no SREP "
    "rows, no buffer rows, no row 12, and no LCR or NSFR build-up - it fails the row-set test, so it is not an "
    "unnumbered KM1. The FY2022 edition DOES print a full FY2021 comparative column (CET1 114,012; RWAs 743,296; "
    "leverage 3.9%; LCR 241.8%; NSFR 125.0%) and it is deliberately unused here, because a comparative is not the "
    "year's own edition. Those FY2021 figures do appear on the single-metric sheets, which are sourced on a "
    "different basis and cite that comparative explicitly. Checked for a hidden image-only table before "
    "concluding: the FY2021 edition is text-native (32pp, ~8,800 chars/page), its summary page carries 342 digits "
    "of extractable text and no embedded image, and its only images sit on pages 3 and 5.\n\n"
    "ROWS THE SOURCE NEVER PRINTED STAY BLANK (and a later edition does not license filling them). The FY2022 "
    "edition prints no UK 16a and no UK 16b - it goes straight from row 15 to row 16 - so both are blank in that "
    "column here. The FY2023 edition's own 2022 comparative DOES print them (335,102 and 24,619), and those "
    "figures are deliberately not carried back: a row the year's own edition never printed is not disclosed for "
    "that year.\n\n"
    "NO RESTATEMENTS FOUND ACROSS EDITIONS - each overlapping year was cross-checked against the following "
    "edition's comparative and every figure matched exactly (FY2024 Bank in the FY2024 edition vs its FY24 Bank "
    "comparative in the FY2025 edition; FY2025 Bank in the FY2025 edition vs its 2025 Bank comparative in the "
    "FY2026 edition; FY2022 in its own edition vs the FY2023 edition's 2022 column apart from the two rows named "
    "above). Where a later edition rounds £'000 into £m the two agree to the rounding (FY2023 Bank CET1 241,213 "
    "appears as 241.3 in the FY2024 edition).\n\n"
    "LABEL DRIFT IS REPRODUCED, NOT HARMONISED: row 20 is printed 'NSFR ratio (%)' in FY2022/FY2023 and 'Net "
    "Stable Funding Ratio (%)' from FY2025; UK 16a is 'Cash outflows - Total weighted value' in FY2023 and "
    "'Outflows - Total weighted value' later. Each caption block carries the wording of the editions it covers; "
    "the single ratio rows carry the current wording.\n\n"
    "LATEST-EDITION CHECK (2026-09-16): atombank.co.uk/investor-information/ lists nine annual Pillar 3 editions "
    "(16-17 through 25-26, the FY2024 one filed under atom-holdco-limited-pillar-3.pdf rather than a year-named "
    "file). The newest is Pillar 3 Disclosures 2026 ('pillar-3-disclosures-25-26.pdf', verified by md5 against "
    "the copy read here), already carried above. NONE NEWER. The same page also publishes INTERIM (half-year) "
    "Pillar 3 disclosures - interim-pillar-3-disclosures-2026.pdf and interim-pillar-3-disclosures-hy2025.pdf - "
    "which this workbook does not currently carry an Interim Pillar 3 sheet for; recorded here as a known, "
    "deliberate gap rather than an absence.\n\n"
    + ENTITY_NOTE
)

km1_rows = [
    ("SECTION", "AVAILABLE OWN FUNDS (AMOUNTS)", {}),
    ("DATA", "1  Common Equity Tier 1 (CET1) capital (£m)",
     {"FY2026": 365.2, "FY2025": 356.4, "FY2024": 347.3}),
    ("DATA", "1  Common Equity Tier 1 (CET1) capital (£'000)",
     {"FY2023": 241213, "FY2022": 217158}),
    ("DATA", "2  Tier 1 capital (£m)",
     {"FY2026": 414.3, "FY2025": 356.4, "FY2024": 347.3}),
    ("DATA", "2  Tier 1 capital (£'000)",
     {"FY2023": 241213, "FY2022": 217158}),
    ("DATA", "3  Total capital (£m)",
     {"FY2026": 463.2, "FY2025": 406.4, "FY2024": 347.3}),
    ("DATA", "3  Total capital (£'000)",
     {"FY2023": 248418, "FY2022": 225151}),
    ("SECTION", "RISK-WEIGHTED EXPOSURE AMOUNTS", {}),
    ("DATA", "4  Total risk-weighted exposure amount (£m)",
     {"FY2026": 2728.8, "FY2025": 2379.3, "FY2024": 1828.0}),
    ("DATA", "4  Total risk-weighted exposure amount (£'000)",
     {"FY2023": 1271669, "FY2022": 1043001}),
    ("SECTION", "CAPITAL RATIOS (AS A PERCENTAGE OF RISK-WEIGHTED EXPOSURE AMOUNT)", {}),
    ("DATA", "5  Common Equity Tier 1 ratio (%)",
     {"FY2026": "13.4%", "FY2025": "15.0%", "FY2024": "19.0%", "FY2023": "19.0%", "FY2022": "20.8%"}),
    ("DATA", "6  Tier 1 ratio (%)",
     {"FY2026": "15.2%", "FY2025": "15.0%", "FY2024": "19.0%", "FY2023": "19.0%", "FY2022": "20.8%"}),
    ("DATA", "7  Total capital ratio (%)",
     {"FY2026": "17.0%", "FY2025": "17.1%", "FY2024": "19.0%", "FY2023": "19.5%", "FY2022": "21.6%"}),
    ("SECTION", "ADDITIONAL OWN FUNDS REQUIREMENTS BASED ON SREP (AS A PERCENTAGE OF RISK-WEIGHTED EXPOSURE AMOUNT)", {}),
    ("DATA", "UK 7a  Additional CET1 SREP requirements (%)",
     {"FY2026": "0.1%", "FY2025": "0.1%", "FY2024": "0.8%", "FY2023": "0.8%", "FY2022": "1.5%"}),
    ("DATA", "UK 7b  Additional AT1 SREP requirements (%)",
     {"FY2026": "0.0%", "FY2025": "0.0%", "FY2024": "0.3%", "FY2023": "0.3%", "FY2022": "0.9%"}),
    ("DATA", "UK 7c  Additional T2 SREP requirements (%)",
     {"FY2026": "0.1%", "FY2025": "0.1%", "FY2024": "0.3%", "FY2023": "0.3%", "FY2022": "1.1%"}),
    ("DATA", "UK 7d  Total SREP own funds requirements (%)",
     {"FY2026": "8.2%", "FY2025": "8.2%", "FY2024": "9.4%", "FY2023": "9.4%", "FY2022": "9.5%"}),
    ("SECTION", "COMBINED BUFFER REQUIREMENT (AS A PERCENTAGE OF RISK-WEIGHTED EXPOSURE AMOUNT)", {}),
    ("DATA", "8  Capital conservation buffer (%)",
     {"FY2026": "2.5%", "FY2025": "2.5%", "FY2024": "2.5%", "FY2023": "2.5%", "FY2022": "2.5%"}),
    ("DATA", "9  Institution specific countercyclical capital buffer (%)",
     {"FY2026": "2.0%", "FY2025": "2.0%", "FY2024": "2.0%", "FY2023": "1.0%", "FY2022": "0.0%"}),
    ("DATA", "11  Combined buffer requirement (%)",
     {"FY2026": "4.5%", "FY2025": "4.5%", "FY2024": "4.5%", "FY2023": "3.5%", "FY2022": "2.5%"}),
    ("DATA", "UK 11a  Overall capital requirements (%)",
     {"FY2026": "12.7%", "FY2025": "12.7%", "FY2024": "13.9%", "FY2023": "12.9%", "FY2022": "12.0%"}),
    ("DATA", "12  CET1 available after meeting the total SREP own funds requirements (%)",
     {"FY2026": "3.4%", "FY2025": "5.0%", "FY2024": "8.7%", "FY2023": "9.7%", "FY2022": "12.5%"}),
    ("SECTION", "LEVERAGE RATIO", {}),
    ("DATA", "13  Leverage ratio total exposure measure (£m)",
     {"FY2026": 7665.4, "FY2025": 7174.6, "FY2024": 5064.5}),
    ("DATA", "13  Leverage ratio total exposure measure (£'000)",
     {"FY2023": 3723901, "FY2022": 3313171}),
    ("DATA", "14  Leverage ratio (%)",
     {"FY2026": "5.4%", "FY2025": "5.0%", "FY2024": "6.9%", "FY2023": "6.5%", "FY2022": "6.6%"}),
    ("SECTION", "LIQUIDITY COVERAGE RATIO", {}),
    ("DATA", "15  Total high-quality liquid assets (HQLA) (Weighted value - average) (£m)",
     {"FY2026": 3756.0, "FY2025": 2333.1, "FY2024": 3849.0}),
    ("DATA", "15  Total high-quality liquid assets (HQLA) (Weighted value - average) (£'000)",
     {"FY2023": 2494398, "FY2022": 971602}),
    ("DATA", "UK 16a  Outflows - Total weighted value (£m)",
     {"FY2026": 1131.8, "FY2025": 594.7, "FY2024": 586.0}),
    ("DATA", "UK 16a  Cash outflows - Total weighted value (£'000)",
     {"FY2023": 495538}),
    ("DATA", "UK 16b  Cash inflows - Total weighted value (£m)",
     {"FY2026": 52.9, "FY2025": 44.3, "FY2024": 52.0}),
    ("DATA", "UK 16b  Cash inflows - Total weighted value (£'000)",
     {"FY2023": 49208}),
    ("DATA", "16  Total net cash outflows (adjusted value) (£m)",
     {"FY2026": 1078.9, "FY2025": 550.4, "FY2024": 534.0}),
    ("DATA", "16  Total net cash outflows (adjusted value) (£'000)",
     {"FY2023": 446330, "FY2022": 310483}),
    ("DATA", "17  Liquidity coverage ratio (%)",
     {"FY2026": "350.9%", "FY2025": "418.6%", "FY2024": "727.8%", "FY2023": "578.6%", "FY2022": "316.7%"}),
    ("SECTION", "NET STABLE FUNDING RATIO", {}),
    ("DATA", "18  Total available stable funding (£m)",
     {"FY2026": 8562.0, "FY2025": 6821.3, "FY2024": 6891.4}),
    ("DATA", "18  Total available stable funding (£'000)",
     {"FY2023": 5557689, "FY2022": 3492177}),
    ("DATA", "19  Total required stable funding (£m)",
     {"FY2026": 4378.4, "FY2025": 3987.7, "FY2024": 3146.1}),
    ("DATA", "19  Total required stable funding (£'000)",
     {"FY2023": 2615311, "FY2022": 2248265}),
    ("DATA", "20  Net Stable Funding Ratio (%)",
     {"FY2026": "196.0%", "FY2025": "171.2%", "FY2024": "221.8%", "FY2023": "211.8%", "FY2022": "154.9%"}),
]

bw.add_km1_sheet(
    title="Atom Bank Plc - KM1 Key Metrics",
    subtitle="Bank column, as published each year - amounts in two blocks because the source unit changes",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=76,
    source_height=460,
    years=["FY2026", "FY2025", "FY2024", "FY2023", "FY2022"],
)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2026": 365200, "FY2025": 356400, "FY2024": 347300, "FY2023": 241213, "FY2022": 217158, "FY2021": 114012, "FY2020": 168645, "FY2019": 184050, "FY2018": 100058, "FY2017": 73313, "FY2016": 9955})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWEA",
    [("Common Equity Tier 1 ratio (%)", {"FY2026": "13.4%", "FY2025": "15.0%", "FY2024": "19.0%", "FY2023": "19.0%", "FY2022": "20.8%", "FY2021": "15.3%", "FY2020": "18.6%", "FY2019": "17.9%", "FY2018": "17.5%", "FY2017": "43.9%", "FY2016": "25.2%"})],
    p3_sources(),
    note="Reported on a transitional (IFRS 9 relief) basis throughout, per project convention. The FY2025 Pillar 3 "
         "Disclosures state that without IFRS 9 transitional relief, FY2025's CET1 ratio would be 14.8% (Bank: "
         "14.8%) rather than the 15.0% shown - not substituted in, noted here for reference only.",
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2026": 414300, "FY2025": 356400, "FY2024": 347300, "FY2023": 241213, "FY2022": 217158, "FY2021": 114012, "FY2020": 168645, "FY2019": 184050, "FY2018": 100058, "FY2017": 73313, "FY2016": 9955})],
    p3_sources(),
    note="Tier 1 Capital = CET1 Capital every year - Atom has never held Additional Tier 1 (AT1) instruments (KM1 "
         "template shows an identical row 1/row 2 every year).",
)

metric(
    "Tier 1 Ratio", "% of RWEA",
    [("Tier 1 ratio (%)", {"FY2026": "15.2%", "FY2025": "15.0%", "FY2024": "19.0%", "FY2023": "19.0%", "FY2022": "20.8%", "FY2021": "15.3%", "FY2020": "18.6%", "FY2019": "17.9%", "FY2018": "17.5%", "FY2017": "43.9%", "FY2016": "25.2%"})],
    p3_sources(),
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2026": 463200, "FY2025": 406400, "FY2024": 347300, "FY2023": 248418, "FY2022": 225151, "FY2021": 121990, "FY2020": 176609, "FY2019": 191999, "FY2018": 107993, "FY2017": 73608, "FY2016": 9955})],
    p3_sources(),
    note="Total Capital exceeds Tier 1 Capital from FY2025 onward once Atom's £50m Fixed Rate Reset Callable "
         "Subordinated Tier 2 notes (issued October 2024) entered regulatory capital; FY2021-FY2023 also carry a "
         "smaller Tier 2 balance (British Business Bank instruments, ~£8m in FY2021) but FY2024's KM1 template "
         "shows Total Capital = Tier 1 exactly (no Tier 2 balance that year, per the source table). HD-025 "
         "EXTENSION: FY2017-FY2020 also carry their own real Tier 2 balances (general credit risk adjustments/"
         "issued Tier 2 instruments, £295k-£7,964k) - Total Capital exceeds Tier 1 in every one of those 4 years; "
         "FY2016 (pre-launch, no lending) has no Tier 2 balance at all, so Total Capital = CET1/Tier 1 exactly "
         "that year only.",
)

metric(
    "Total Capital Ratio", "% of RWEA",
    [("Total capital ratio (%)", {"FY2026": "17.0%", "FY2025": "17.1%", "FY2024": "19.0%", "FY2023": "19.5%", "FY2022": "21.6%", "FY2021": "16.4%", "FY2020": "19.5%", "FY2019": "18.7%", "FY2018": "18.9%", "FY2017": "44.1%", "FY2016": "25.2%"})],
    p3_sources(),
    note="The FY2025 Pillar 3 Disclosures state that without IFRS 9 transitional relief, FY2025's total capital "
         "ratio would be 16.9% (Bank: 16.9%) rather than the 17.1% shown - noted for reference only, not substituted.",
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted exposure amount", {"FY2026": 2728800, "FY2025": 2379300, "FY2024": 1828000, "FY2023": 1271669, "FY2022": 1043001, "FY2021": 743296, "FY2020": 907158, "FY2019": 1028247, "FY2018": 572566, "FY2017": 166888, "FY2016": 39541})],
    p3_sources(),
)

# ---------------------------------------------------------------
# Sheet: RWA Breakdown (placed immediately after Total RWAs, before Leverage Ratio)
# ---------------------------------------------------------------
rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding CCR)", {"FY2026": 2495600, "FY2025": 2171000, "FY2024": 1676100, "FY2023": 1161945, "FY2022": 951043, "FY2021": 658405, "FY2020": 872639, "FY2019": 1000236, "FY2018": 529996, "FY2017": 76974, "FY2016": 2677}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2026": 13300, "FY2025": 13400, "FY2024": 6000, "FY2023": 1903, "FY2022": 13238, "FY2021": 3677, "FY2020": 3052, "FY2019": 3105, "FY2018": 2928, "FY2017": 201}),
    ("DATA", "  of which credit valuation adjustment (CVA)", {"FY2026": 6600, "FY2025": 7100, "FY2024": 2700, "FY2023": 524, "FY2022": 4621, "FY2021": 560}),
    ("DATA", "Credit valuation adjustment (CVA) (FY2016-FY2020: own additive risk category, not a CCR sub-line)", {"FY2020": 2709, "FY2019": 2893, "FY2018": 3529, "FY2017": 1165}),
    ("DATA", "Securitisation exposures (non-trading book, after the cap)", {"FY2026": 26700, "FY2025": 20900, "FY2024": 4300, "FY2023": 21200, "FY2022": 40725, "FY2021": 81214, "FY2020": 28758, "FY2019": 9327, "FY2018": 23427, "FY2017": 41904}),
    ("DATA", "Market risk (position, FX and commodities risks)", {"FY2026": 0, "FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Operational risk", {"FY2026": 193200, "FY2025": 174000, "FY2024": 141600, "FY2023": 86621, "FY2022": 37995, "FY2021": 0, "FY2020": 0, "FY2019": 12686, "FY2018": 12686, "FY2017": 46644, "FY2016": 36864}),
    ("TOTAL", "Total risk-weighted exposure amount (RWEAs)", {"FY2026": 2728800, "FY2025": 2379300, "FY2024": 1828000, "FY2023": 1271669, "FY2022": 1043001, "FY2021": 743296, "FY2020": 907158, "FY2019": 1028247, "FY2018": 572566, "FY2017": 166888, "FY2016": 39541}),
]

RWA_BREAKDOWN_SOURCES = (
    "Sources - Table UK OV1 (Overview of risk weighted exposure amounts), Bank basis, £'000:\n"
    f"FY2026: Atom Holdco plc Pillar 3 Disclosures 2026, p.18 (Table UK OV1, '2026 Bank' column - the table "
    f"prints 2026 Group, 2026 Bank, 2025 Group and 2025 Bank side by side, and the Bank column is the one used "
    f"here; Group would have given 2,506.0 credit risk and a 2,739.7 total against the Bank's 2,495.6 and "
    f"2,728.8) - {P3_FY26_URL}\n"
    f"FY2025/FY2024: Atom Holdco plc Pillar 3 Disclosures 2025, p.16 (Bank column) - {P3_FY25_URL}\n"
    f"FY2023: Atom Holdco Limited Pillar 3 Disclosures 2023, p.16-17 (Bank column) - {P3_FY23_URL}\n"
    f"FY2022/FY2021: Atom Bank Plc Pillar 3 Disclosures 2021/22, p.20-21 - {P3_FY22_URL}\n"
    f"FY2020: Atom Bank Plc Pillar 3 Disclosures 2019/20 (each year's own 'Summary of risk weighted assets' "
    f"table, pre-UK OV1 template) - {P3_FY20_URL}\n"
    f"FY2019: Atom Bank Plc Pillar 3 Disclosures 2018/19, same table format - {P3_FY19_URL}\n"
    f"FY2018: Atom Bank Plc Pillar 3 Disclosures 2017/18, same table format - {P3_FY18_URL}\n"
    f"FY2017: Atom Bank Plc Pillar 3 Disclosures 2016/17 (Atom's first Pillar 3 disclosure, as at 31 March 2017) "
    f"- {P3_FY17_URL}\n"
    f"FY2016: sourced only from the FY2016/17 Pillar 3 Disclosures document's own FY2016 comparative column above "
    f"- no standalone FY2016 Pillar 3 document was ever published (the bank had no Pillar 3-relevant lending or "
    f"capital disclosure requirement in its own FY2016 Annual Report, which pre-dates product launch).\n"
    "Atom states it has no Pillar 1 market risk exposures in every year's Pillar 3 report - shown as £0 rather "
    "than blank/not-disclosed (FY2016-FY2017 don't disclose market risk as a line at all, but the bank had no "
    "trading book then either, consistent with £0). FY2025/FY2024 figures were originally disclosed in £m (1 "
    "decimal place) and are shown here converted to £'000 (x1,000), consistent with the FY2024/FY2025 Pillar 3 "
    "ratio sheets' own unit conversion note; FY2023-FY2016 are each source table's own £'000 figures. Total ties "
    "out exactly to the Total RWAs sheet for every year.\n\n"
    "HD-025 EXTENSION NOTE: FY2016-FY2020's pre-UK-OV1-template tables present Credit valuation adjustment (CVA) "
    "as its OWN additive risk category (a separate row, not a sub-line 'of which' underneath Counterparty credit "
    "risk as in FY2021 onward's UK OV1 template) - kept as a distinct row here for those years rather than force-"
    "fitted into the later 'of which' convention, since it is genuinely additive to the FY2016-FY2020 totals. "
    "FY2020's Pillar 3 report explains its Operational risk RWA fell to nil that year because the bank switched "
    "from a forecast-based to an actual-3-year-average-losses-based calculation, and three years of actual "
    "operational losses produced a nil capital requirement - a genuine documented methodology change, not a data "
    "gap. FY2016's own document discloses only Credit risk and Operational risk components (no CCR/CVA/"
    "Securitisation/Market risk lines at all, consistent with a bank that had not yet launched lending or trading) "
    "- its two disclosed components sum exactly to that year's Total RWA."
)

bw.add_rwa_breakdown_sheet(
    title="Atom Bank Plc - RWA Breakdown",
    subtitle="Bank basis, £'000",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Leverage ratio total exposure measure", {"FY2026": 7665400, "FY2025": 7174600, "FY2024": 5064500, "FY2023": 3723901, "FY2022": 3313171, "FY2021": 2914267, "FY2020": 2797736, "FY2019": 2846115, "FY2018": 2003497, "FY2017": 669927, "FY2016": 18148}),
        ("Leverage ratio (%)", {"FY2026": "5.4%", "FY2025": "5.0%", "FY2024": "6.9%", "FY2023": "6.5%", "FY2022": "6.6%", "FY2021": "3.9%", "FY2020": "6.0%", "FY2019": "6.5%", "FY2018": "5.0%", "FY2017": "10.9%", "FY2016": "54.9%"}),
    ],
    p3_sources(),
    note="Atom states it is 'out of scope of the leverage ratio requirements due to retail deposits falling below "
         "the threshold of £50bn' (FY2025 Pillar 3 Disclosures) - the ratio is voluntarily calculated and "
         "monitored against an internal 3.25% floor rather than a binding regulatory minimum. No 'excluding "
         "claims on central banks' basis break is shown in Atom's own KM1 templates (unlike several other banks "
         "in this project) - one consistent methodology is used throughout FY2016-FY2025. FY2016's very high 54.9% "
         "figure reflects the bank's pre-launch balance sheet (tiny exposure measure against already-raised "
         "capital), not a data error.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value (average)", {"FY2026": 3756000, "FY2025": 2333100, "FY2024": 3849000, "FY2023": 2494398, "FY2022": 971602, "FY2021": 415697, "FY2020": 290230, "FY2019": 216650, "FY2018": 643721, "FY2017": 481472}),
        ("Total net cash outflows, adjusted value", {"FY2026": 1078900, "FY2025": 550400, "FY2024": 534000, "FY2023": 446330, "FY2022": 310483, "FY2021": 185032, "FY2020": 38003, "FY2019": 66951, "FY2018": 132684, "FY2017": 74539}),
        ("Liquidity Coverage Ratio (%)", {"FY2026": "350.9%", "FY2025": "418.6%", "FY2024": "727.8%", "FY2023": "578.6%", "FY2022": "316.7%", "FY2021": "241.8%", "FY2020": "763.7%", "FY2019": "323.6%", "FY2018": "485.2%", "FY2017": "645.9%"}),
    ],
    p3_sources(),
    note="FY2016 has no LCR disclosure at all - genuinely absent from the FY2016/17 Pillar 3 Disclosures document "
         "(the only document covering that year), confirmed by directly searching its full text for 'liquidity "
         "coverage'/'LCR' rather than assuming absence from a section-heading scan. A real self-skip, not an "
         "omission.",
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding", {"FY2026": 8562000, "FY2025": 6821300, "FY2024": 6891400, "FY2023": 5557689, "FY2022": 3492177, "FY2021": 2536566}),
        ("Total required stable funding", {"FY2026": 4378400, "FY2025": 3987700, "FY2024": 3146100, "FY2023": 2615311, "FY2022": 2248265, "FY2021": 2029057}),
        ("Net Stable Funding Ratio (%)", {"FY2026": "196.0%", "FY2025": "171.2%", "FY2024": "221.8%", "FY2023": "211.8%", "FY2022": "154.9%", "FY2021": "125.0%"}),
    ],
    p3_sources(),
    note="FY2016-FY2020 have no numeric NSFR disclosure - each of those 5 Pillar 3 Disclosures only mentions the "
         "then-forthcoming CRR2 NSFR requirement in forward-looking terms, with no ratio ever actually reported "
         "(confirmed by directly searching each document's full text for 'NSFR'/'net stable funding' rather than "
         "assuming absence). A real self-skip across all 5 years, not an omission.",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={
        "MREL Ratio": "MREL is not mentioned anywhere in any of Atom's 6 Pillar 3 Disclosures (FY2021-FY2026) - "
                       "zero hits for 'MREL', 'minimum requirement for own funds' and 'resolution' in the FY2026 "
                       "edition, against rich neighbouring terms in the same document ('CET1' 26, 'own funds' 21, "
                       "'leverage' 17), so this is a real self-skip and not a failed search. It is also a FORMAL "
                       "EXCLUSION, not merely silence: the FY2026 edition's Appendix 1 CRR disclosure index states "
                       "'Article 437a Disclosure of Own Funds and Eligible Liabilities - Not Applicable - Due to "
                       "Article 433c (2)', i.e. Atom discloses as a small and non-complex institution and is not "
                       "required to publish own funds and eligible liabilities (MREL) disclosures.",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2026": 10226400, "FY2025": 8990900, "FY2024": 7224900, "FY2023": 7801381, "FY2022": 4558515, "FY2021": 2827121, "FY2020": 2705431, "FY2019": 2772299, "FY2018": 1957331, "FY2017": 648973, "FY2016": 37489}),
        ("Loans and advances to customers", {"FY2026": 5807500, "FY2025": 5301500, "FY2024": 4100900, "FY2023": 2958769, "FY2022": 2384066, "FY2021": 1638851, "FY2020": 1970818, "FY2019": 2399861, "FY2018": 1219356, "FY2017": 99209}),
        ("Customer deposits", {"FY2026": 8347600, "FY2025": 7538700, "FY2024": 5746200, "FY2023": 6551325, "FY2022": 3229796, "FY2021": 2154419, "FY2020": 1864812, "FY2019": 1771121, "FY2018": 1439793, "FY2017": 538060, "FY2016": 10}),
        ("Total equity", {"FY2026": 504600, "FY2025": 425200, "FY2024": 403800, "FY2023": 284631, "FY2022": 251094, "FY2021": 141330, "FY2020": 200503, "FY2019": 212704, "FY2018": 134971, "FY2017": 104082, "FY2016": 29296}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net operating income/(expense)", {"FY2026": 99300, "FY2025": 93500, "FY2024": 88100, "FY2023": 65564, "FY2022": 48018, "FY2021": -1714, "FY2020": -14533, "FY2019": -5025, "FY2018": -2576, "FY2017": -1335, "FY2016": 18}),
        ("Staff and administrative expense", {"FY2026": -73700, "FY2025": -68400, "FY2024": -61500, "FY2023": -59128, "FY2022": -50182, "FY2021": -47129, "FY2020": -39764, "FY2019": -43355, "FY2018": -44387, "FY2017": -37460, "FY2016": -23349}),
        ("Profit/(loss) for the year", {"FY2026": 27700, "FY2025": 16900, "FY2024": 12300, "FY2023": -5623, "FY2022": -11927, "FY2021": -62379, "FY2020": -63945, "FY2019": -79857, "FY2018": -52680, "FY2017": -42169, "FY2016": -22515}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2026": 425200, "FY2025": 403800, "FY2024": 284500, "FY2023": 251094, "FY2022": 141330, "FY2021": 200503, "FY2020": 212704, "FY2019": 134971, "FY2018": 104082, "FY2017": 29296, "FY2016": 9023}),
        ("Total comprehensive income/(expense) for the year", {"FY2026": 27700, "FY2025": 15400, "FY2024": 12500, "FY2023": -352, "FY2022": -12264, "FY2021": -61670, "FY2020": -64121, "FY2019": -79769, "FY2018": -53351, "FY2017": -41843, "FY2016": -22515}),
        ("Other equity movements, net", {"FY2026": 51700, "FY2025": 6000, "FY2024": 106800, "FY2023": 33889, "FY2022": 122028, "FY2021": 2497, "FY2020": 51920, "FY2019": 157502, "FY2018": 84240, "FY2017": 116629, "FY2016": 42788}),
        ("Closing equity", {"FY2026": 504600, "FY2025": 425200, "FY2024": 403800, "FY2023": 284631, "FY2022": 251094, "FY2021": 141330, "FY2020": 200503, "FY2019": 212704, "FY2018": 134971, "FY2017": 104082, "FY2016": 29296}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2022": 1176233, "FY2021": 30842, "FY2020": 86814, "FY2019": -496336, "FY2018": 101686, "FY2017": 395754, "FY2016": -18557}),
        ("Net cash from/(used in) investing activities", {"FY2022": -156256, "FY2021": 16769, "FY2020": -91063, "FY2019": 204637, "FY2018": -253264, "FY2017": -86510, "FY2016": -18672}),
        ("Net cash from/(used in) financing activities", {"FY2022": 116793, "FY2021": -699, "FY2020": 49011, "FY2019": 152543, "FY2018": 87082, "FY2017": 112321, "FY2016": 39287}),
        ("Cash and balances at central banks at end of year", {"FY2022": 1453596, "FY2021": 316827, "FY2020": 269915, "FY2019": 225153, "FY2018": 364309, "FY2017": 428805, "FY2016": 7240}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2026": "13.4%", "FY2025": "15.0%", "FY2024": "19.0%", "FY2023": "19.0%", "FY2022": "20.8%", "FY2021": "15.3%", "FY2020": "18.6%", "FY2019": "17.9%", "FY2018": "17.5%", "FY2017": "43.9%", "FY2016": "25.2%"}),
        ("Tier 1 Ratio", {"FY2026": "15.2%", "FY2025": "15.0%", "FY2024": "19.0%", "FY2023": "19.0%", "FY2022": "20.8%", "FY2021": "15.3%", "FY2020": "18.6%", "FY2019": "17.9%", "FY2018": "17.5%", "FY2017": "43.9%", "FY2016": "25.2%"}),
        ("Total Capital Ratio", {"FY2026": "17.0%", "FY2025": "17.1%", "FY2024": "19.0%", "FY2023": "19.5%", "FY2022": "21.6%", "FY2021": "16.4%", "FY2020": "19.5%", "FY2019": "18.7%", "FY2018": "18.9%", "FY2017": "44.1%", "FY2016": "25.2%"}),
        ("Leverage Ratio", {"FY2026": "5.4%", "FY2025": "5.0%", "FY2024": "6.9%", "FY2023": "6.5%", "FY2022": "6.6%", "FY2021": "3.9%", "FY2020": "6.0%", "FY2019": "6.5%", "FY2018": "5.0%", "FY2017": "10.9%", "FY2016": "54.9%"}),
        ("LCR", {"FY2026": "350.9%", "FY2025": "418.6%", "FY2024": "727.8%", "FY2023": "578.6%", "FY2022": "316.7%", "FY2021": "241.8%", "FY2020": "763.7%", "FY2019": "323.6%", "FY2018": "485.2%", "FY2017": "645.9%"}),
        ("NSFR", {"FY2026": "196.0%", "FY2025": "171.2%", "FY2024": "221.8%", "FY2023": "211.8%", "FY2022": "154.9%", "FY2021": "125.0%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Cash flow is blank for FY2023-FY2025 (FRS 101 qualifying-"
         "entity exemption took effect from FY2023, following the insertion of Atom Holdco above Atom Bank Plc - "
         "see Cash Flow Statement sheet note). Unlike several other banks in this project, all ratios here are on "
         "a consistent Bank-solo basis throughout - no cash-flow-vs-Pillar-3 basis mismatch. 'Net operating "
         "income/(expense)' and 'Staff and administrative expense' stand in for the usual 'Revenue'/'Total "
         "operating expense' headline pair - Atom's own P&L structure doesn't disclose a single top-line revenue "
         "figure (see the Profit & Loss sheet's presentation note). FY2024's 'Opening equity' (£284,500k) uses "
         "the FY2025 Annual Report's own restated 1 April 2023 balance rather than the FY2023 report's own "
         "(slightly different, £284,631k) closing balance for the same date - see the Statement of Changes in "
         "Equity sheet's flagged discrepancy note. HD-025: extended back to FY2016, the bank's first full year "
         "(licensed 2015, launched 2016) - Loans/advances, LCR and NSFR are blank for FY2016 (pre-launch/genuinely "
         "undisclosed that year, see the relevant detail sheets' notes).",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/ATOM BANK FINANCIALS.xlsx")
print("Saved ATOM BANK FINANCIALS.xlsx")
