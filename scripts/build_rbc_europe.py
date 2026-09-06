import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014"]
YEAR_LABEL = {y: y for y in YEARS}
AR_URL = {
    "FY2025": "https://find-and-update.company-information.service.gov.uk/company/00995939/filing-history/MzUxNjA1NTA3MGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2024": "https://find-and-update.company-information.service.gov.uk/company/00995939/filing-history/MzQ3MTY0MzU5OWFkaXF6a2N4/document?format=pdf&download=0",
    "FY2023": "https://find-and-update.company-information.service.gov.uk/company/00995939/filing-history/MzQxNjYxMzY5MmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2022": "https://find-and-update.company-information.service.gov.uk/company/00995939/filing-history/MzM3Mzk1MDQ0MWFkaXF6a2N4/document?format=pdf&download=0",
    "FY2021": "https://find-and-update.company-information.service.gov.uk/company/00995939/filing-history/MzMzNjkyMjU2MGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2020": "https://find-and-update.company-information.service.gov.uk/company/00995939/filing-history/MzI5NzU5NDkyMWFkaXF6a2N4/document?format=pdf&download=0",
    "FY2019": "https://find-and-update.company-information.service.gov.uk/company/00995939/filing-history/MzI2MDE2OTMwNGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2018": "https://find-and-update.company-information.service.gov.uk/company/00995939/filing-history/MzIzMTI1OTE5MWFkaXF6a2N4/document?format=pdf&download=0",
    "FY2017": "https://find-and-update.company-information.service.gov.uk/company/00995939/filing-history/MzIwMjY0NzYzMWFkaXF6a2N4/document?format=pdf&download=0",
    "FY2016": "https://find-and-update.company-information.service.gov.uk/company/00995939/filing-history/MzE3MjQyMzYwNmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2015": "https://find-and-update.company-information.service.gov.uk/company/00995939/filing-history/MzE0NTQzNjM1MWFkaXF6a2N4/document?format=pdf&download=0",
    "FY2014": "https://find-and-update.company-information.service.gov.uk/company/00995939/filing-history/MzEyMDE3MjI1NWFkaXF6a2N4/document?format=pdf&download=0",
}
P3_URL = {
    "FY2025": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/rbcel-pillar-3-oct-25-final.pdf",
    "FY2024": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/rbcel-pillar-3-oct-24-final.pdf",
    "FY2023": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/RBCEL-Pillar-3-Oct-23_Final_v2.pdf",
    "FY2022": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/RBCEL-Annual-Pillar-3-2022.pdf",
    "FY2021": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/RBCEL-Annual-Pillar-3-2021.pdf",
    "FY2020": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/2020-Pillar-III-Disclosure.pdf",
    "FY2019": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/2019-Pillar-III-Disclosure.pdf",
    "FY2018": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/2018-Pillar-III-Disclosure.pdf",
    "FY2017": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/2017_Pillar_III_Disclosure.pdf",
    "FY2016": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/Pillar-Disclosure-2016.pdf",
    "FY2015": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/Pillar-Disclosure-2015.pdf",
    "FY2014": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/Pillar-Disclosure-2014.pdf",
}
HISTORICAL_SOURCES = (
    "HD-018 (FY2014-FY2020 extension) - RBC Europe Limited's own Annual Report and Accounts filed with Companies "
    "House (company 00995939) and its own annual Pillar III disclosures published at rbc.com/regulatory-information "
    "were used for every added year; all seven Companies House filings are image-only scans, OCR'd with tesseract "
    "(150-300dpi) and cross-checked for internal arithmetic consistency (each year's closing balances tie to the "
    "next year's opening balances and to that year's own Pillar III own-funds table) before transcription. FY2018 "
    "was the first year RBC Europe adopted IFRS 9 (effective 1 November 2017); FY2014-FY2017 Pillar III disclosures "
    "predate the UK's post-Brexit CRR/KM1 templates and use the EU CRR transitional-provisions presentation "
    "(Common Equity Tier 1 = Tier 1 throughout, since no AT1 existed until the FY2018 issuance). LCR and NSFR were "
    "not yet disclosed metrics in any FY2014-FY2020 Pillar III filing (NSFR's UK application date was January 2022 "
    "per the FY2020 disclosure's own text) - shown as 'Not publicly disclosed' for those years, consistent with the "
    "existing FY2021 treatment."
)
ENTITY_NOTE = ("RBC Europe Limited (company 00995939, FRN 124543) is a UK authorised bank and wholly owned "
               "subsidiary of Royal Bank of Canada. The financial statements and cash flows are the Company's own "
               "entity-level figures in GBP, with October 31 year-end. The Pillar 3 disclosures are also RBC Europe "
               "Limited (RBCEL) Company-level disclosures, not consolidated Royal Bank of Canada group figures.")
CASH_FLOW_SOURCES = (
    "Sources - RBC Europe Limited's own Statement of Cash Flows, £'000 (all five filings were image-only scans; "
    "OCR'd with tesseract and cross-checked against rendered pages):\n"
    f"FY2025/FY2024: Full accounts made up to 31 October 2025, p.41 - {AR_URL['FY2025']}\n"
    f"FY2024/FY2023: Full accounts made up to 31 October 2024, p.39 - {AR_URL['FY2024']}\n"
    f"FY2023/FY2022: Full accounts made up to 31 October 2023, p.36 - {AR_URL['FY2023']}\n"
    f"FY2022/FY2021: Full accounts made up to 31 October 2022, p.34; FY2021 is the restated comparative - {AR_URL['FY2022']}\n"
    "The 2022 accounts label the FY2021 comparative as restated following an error; that restated comparative is used.\n" + ENTITY_NOTE)
def p3_sources():
    return ("Sources - RBC Europe Limited annual Pillar III disclosures, UK KM1 Key Metrics (Company basis), "
            "p.11 of the 2025/2024 disclosures, p.12 of 2023, p.13 of 2022, and FY2021 own-funds/leverage tables pp.16/21. "
            "FY2014-FY2020 (HD-018): EU CRR transitional own-funds disclosure tables, own-year filing in each case - "
            "FY2020 p.16 ('Table 4'), FY2019 p.10, FY2018 p.21 ('Table 4'), FY2017 p.13/16 ('Table 4'), FY2016 p.17 "
            "('Table 1'/'Table 4'), FY2015 p.15 ('Table 4'), FY2014 pp.13-14 ('Table 4'/'Table 5'). Leverage ratio "
            "table (own-year filing, 'Table 7' pre-FY2018 / 'Table 8' from FY2018): FY2020 p.22, FY2019 p.19, FY2018 "
            "p.33 ('own leverage ratio common disclosure' sub-table; the following page shows FY2017's comparative), "
            "FY2017 p.27, FY2016 p.27, FY2015 p.25. FY2014 had no leverage ratio table (see note below) - not an "
            "omission.\n" +
            "\n".join(f"{y}: {P3_URL[y]}" for y in YEARS) + "\n" + ENTITY_NOTE + "\n" + HISTORICAL_SOURCES)

bw = BankWorkbook(bank_name="RBC Europe Limited", years=YEARS, year_label=YEAR_LABEL, header_color="0B4F6C")

STATEMENTS_SOURCES = (
    "Sources - RBC Europe Limited's own Balance Sheet / Income Statement / Statement of Comprehensive Income "
    "/ Statement of Changes in Equity, £'000, all image-only scans, transcribed via rendered pages:\n"
    f"FY2025/FY2024: Full accounts made up to 31 October 2025, Income Statement p.36, Statement of "
    f"Comprehensive Income p.37, Statement of Changes in Equity p.38, Balance Sheet pp.39-40 - {AR_URL['FY2025']}\n"
    f"FY2023: Full accounts made up to 31 October 2024, Income Statement p.34, Balance Sheet pp.37-38, "
    f"Statement of Changes in Equity p.36 (FY2023 own-year figures) - {AR_URL['FY2024']}\n"
    f"FY2022: Full accounts made up to 31 October 2023, Income Statement p.31, Balance Sheet pp.33-34, "
    f"Statement of Changes in Equity p.32 (FY2022 own-year figures) - {AR_URL['FY2023']}\n"
    f"FY2021 (restated): Full accounts made up to 31 October 2022, Income Statement p.28, Balance Sheet "
    f"pp.31-32, Statement of Changes in Equity p.30 (FY2021 own-year figures, and comprehensive income p.29) "
    f"- {AR_URL['FY2022']}. The 2022 accounts label the FY2021 comparative as restated following an error "
    f"(note 1(f) of that filing) - that restated comparative is used, consistent with the existing Cash Flow "
    f"Statement's convention.\n" + ENTITY_NOTE
)
HISTORICAL_STATEMENTS_SOURCES = (
    "Sources - RBC Europe Limited's own Income Statement / Statement of Comprehensive Income / Statement of "
    "Changes in Equity / Balance Sheet, all image-only Companies House scans, OCR'd from rendered pages (HD-018):\n"
    f"FY2020: Full accounts made up to 31 October 2020, Income Statement p.25, Statement of Comprehensive Income "
    f"and Statement of Changes in Equity p.26, Balance Sheet pp.27-28 - {AR_URL['FY2020']}\n"
    f"FY2019: Full accounts made up to 31 October 2019, Income Statement p.16, Statement of Comprehensive Income "
    f"and Statement of Changes in Equity p.17, Balance Sheet pp.18-19 - {AR_URL['FY2019']}\n"
    f"FY2018: Full accounts made up to 31 October 2018 (own-year, unrestated figures), Income Statement p.16, "
    f"Statement of Comprehensive Income and Statement of Changes in Equity p.17, Balance Sheet pp.18-19 "
    f"- {AR_URL['FY2018']}\n"
    f"FY2017: Full accounts made up to 31 October 2017, Income Statement p.12, Statement of Comprehensive Income "
    f"and Statement of Changes in Equity p.13, Balance Sheet pp.14-15 - {AR_URL['FY2017']}\n"
    f"FY2016: Full accounts made up to 31 October 2017, p.12 (2016 comparative column) for Income Statement, "
    f"p.13 for Statement of Changes in Equity, pp.14-15 (2016 comparative column) for Balance Sheet "
    f"- {AR_URL['FY2017']}\n"
    f"FY2015: Full accounts made up to 31 October 2015, Income Statement (titled 'Statement of Income') p.9, "
    f"Statement of Comprehensive Income and Statement of Changes in Equity p.10, Balance Sheet pp.11-12 "
    f"- {AR_URL['FY2015']}\n"
    f"FY2014: Full accounts made up to 31 October 2015, p.9 (2014 comparative column) for Income Statement, "
    f"p.10 for Statement of Changes in Equity, pp.11-12 (2014 comparative column) for Balance Sheet "
    f"- {AR_URL['FY2015']}\n"
    "IFRS 9 was first adopted for the year beginning 1 November 2017 (FY2018); FY2014-FY2017 use the IAS 39 "
    "available-for-sale ('AFS') regime, so the 'Securities - Investments, net of applicable allowance' row and the "
    "OCI 'debt securities at FVOCI' row hold that period's AFS balances/movements under the same row for "
    "comparability across the full FY2014-FY2025 window - genuine terminology change, not a transcription error. "
    "No Additional Tier 1 capital existed before the FY2018 AT1 issuance, so 'Other equity' is a genuine blank for "
    "FY2014-FY2017, not a gap. FY2016 disclosed a small net pension LIABILITY (not asset) of £1,170k, shown on its "
    "own row. Small residual 'Goodwill and other intangibles' balances (FY2014 £572k amortising to nil by FY2019) "
    "predate and are unrelated to the FY2025 Client Relationships/Goodwill intangibles from the Brewin Dolphin "
    "acquisition.\n" + ENTITY_NOTE
)

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and due from banks", {"FY2025": 2534127, "FY2024": 4455652, "FY2023": 9347772, "FY2022": 10594230, "FY2021": 5171908, "FY2020": 1288018, "FY2019": 3241628, "FY2018": 4516303, "FY2017": 5266890, "FY2016": 2920665, "FY2015": 1983813, "FY2014": 2800600}),
    ("DATA", "Securities - Trading", {"FY2025": 7858143, "FY2024": 7715026, "FY2023": 4769474, "FY2022": 3929825, "FY2021": 4359481, "FY2020": 3917974, "FY2019": 3999396, "FY2018": 4108669, "FY2017": 3418862, "FY2016": 2443939, "FY2015": 3196218, "FY2014": 6800779}),
    ("DATA", "Securities - Investments, net of applicable allowance", {"FY2025": 2279559, "FY2024": 83182, "FY2023": 203710, "FY2022": 625402, "FY2021": 1498709, "FY2020": 2818906, "FY2019": 1228171, "FY2018": 769790, "FY2017": 259115, "FY2016": 28031, "FY2015": 21880, "FY2014": 23829}),
    ("DATA", "Assets purchased under reverse repurchase agreements and securities borrowed", {"FY2025": 21774851, "FY2024": 22497453, "FY2023": 23063695, "FY2022": 23177413, "FY2021": 23666084, "FY2020": 25027609, "FY2019": 23344949, "FY2018": 25037452, "FY2017": 20599676, "FY2016": 19762676, "FY2015": 15537374, "FY2014": 12553224}),
    ("DATA", "Loans and advances", {"FY2025": 8781847, "FY2024": 7810517, "FY2023": 7905674, "FY2022": 8022378, "FY2021": 7034028, "FY2020": 6835562, "FY2019": 6031374, "FY2018": 4779895, "FY2017": 4890103, "FY2016": 3488542, "FY2015": 2948501, "FY2014": 2803899}),
    ("DATA", "Derivative assets", {"FY2025": 1783249, "FY2024": 1329215, "FY2023": 1256698, "FY2022": 1701873, "FY2021": 1524466, "FY2020": 2085908, "FY2019": 2289790, "FY2018": 2518720, "FY2017": 2222269, "FY2016": 1618887, "FY2015": 410554, "FY2014": 425817}),
    ("DATA", "Intangible assets - Client Relationships", {"FY2025": 652709}),
    ("DATA", "Intangible assets - Goodwill", {"FY2025": 576640}),
    ("DATA", "Goodwill and other intangibles (legacy, unrelated to the FY2025 Client Relationships/Goodwill above - amortised to nil by FY2019)", {"FY2017": 74, "FY2016": 242, "FY2015": 407, "FY2014": 572}),
    ("DATA", "Post employment benefit asset", {"FY2025": 12066, "FY2024": 13537, "FY2023": 12800, "FY2022": 18492, "FY2021": 26364, "FY2020": 20000, "FY2019": 19700, "FY2018": 19400, "FY2017": 600, "FY2015": 12100, "FY2014": 8200}),
    ("DATA", "Post employment benefit liability (FY2016 only - net position was a liability, not an asset, that year)", {"FY2016": 1170}),
    ("DATA", "Other assets", {"FY2025": 7004809, "FY2024": 8125846, "FY2023": 7453983, "FY2022": 5243854, "FY2021": 5892136, "FY2020": 5769355, "FY2019": 4733968, "FY2018": 6768045, "FY2017": 3377356, "FY2016": 4163652, "FY2015": 3678469, "FY2014": 2546660}),
    ("TOTAL", "Total assets", {"FY2025": 53258000, "FY2024": 52030428, "FY2023": 54013806, "FY2022": 53313467, "FY2021": 49173176, "FY2020": 47763332, "FY2019": 44888976, "FY2018": 48518274, "FY2017": 40034945, "FY2016": 34426634, "FY2015": 27789316, "FY2014": 27963580}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2025": 7474953, "FY2024": 7051961, "FY2023": 6811297, "FY2022": 8540162, "FY2021": 9026838, "FY2020": 10099652, "FY2019": 8870352, "FY2018": 1579937, "FY2017": 6926710, "FY2016": 4252545, "FY2015": 2063803, "FY2014": 2674108}),
    ("DATA", "Deposits by customers", {"FY2025": 12589815, "FY2024": 12134787, "FY2023": 11557114, "FY2022": 11060215, "FY2021": 5600093, "FY2020": 4586747, "FY2019": 4089777, "FY2018": 4228034, "FY2017": 4853591, "FY2016": 5148013, "FY2015": 4862234, "FY2014": 5841020}),
    ("DATA", "Obligations related to securities sold short", {"FY2025": 3790621, "FY2024": 3939291, "FY2023": 3787173, "FY2022": 2395694, "FY2021": 4034321, "FY2020": 3276454, "FY2019": 2347350, "FY2018": 3046104, "FY2017": 2049584, "FY2016": 2014067, "FY2015": 8454298, "FY2014": 10403695}),
    ("DATA", "Obligations related to assets sold under repurchase agreements and securities loaned", {"FY2025": 17048308, "FY2024": 17716798, "FY2023": 21267109, "FY2022": 22634814, "FY2021": 22236346, "FY2020": 21169408, "FY2019": 21385270, "FY2018": 23061001, "FY2017": 19410167, "FY2016": 16473299, "FY2015": 7475631, "FY2014": 5455869}),
    ("DATA", "Derivative liabilities", {"FY2025": 1729879, "FY2024": 1148496, "FY2023": 1148184, "FY2022": 1636975, "FY2021": 1409860, "FY2020": 2023029, "FY2019": 2225511, "FY2018": 2227123, "FY2017": 2187658, "FY2016": 1611367, "FY2015": 1058963, "FY2014": 374665}),
    ("DATA", "Other liabilities", {"FY2025": 7182262, "FY2024": 8179593, "FY2023": 7596980, "FY2022": 5251277, "FY2021": 5145470, "FY2020": 4945378, "FY2019": 4387202, "FY2018": 6833678, "FY2017": 3248857, "FY2016": 3635778, "FY2015": 2697360, "FY2014": 2053099}),
    ("DATA", "Subordinated liabilities", {"FY2025": 285540, "FY2024": 77658, "FY2023": 82447, "FY2022": 86947, "FY2021": 72951, "FY2020": 77268, "FY2019": 77322, "FY2018": 235091, "FY2017": 301409, "FY2016": 327466, "FY2015": 258849, "FY2014": 250078}),
    ("TOTAL", "Total liabilities", {"FY2025": 50101378, "FY2024": 50248584, "FY2023": 52250304, "FY2022": 51606084, "FY2021": 47525879, "FY2020": 46177936, "FY2019": 43382784, "FY2018": 47210968, "FY2017": 38977976, "FY2016": 33463705, "FY2015": 26871138, "FY2014": 27052534}),
    ("SECTION", "Equity", {}),
    ("DATA", "Common shares", {"FY2025": 2047996, "FY2024": 497996, "FY2023": 497996, "FY2022": 497996, "FY2021": 497996, "FY2020": 497996, "FY2019": 497996, "FY2018": 497996, "FY2017": 497996, "FY2016": 497996, "FY2015": 497996, "FY2014": 497996}),
    ("DATA", "Other equity", {"FY2025": 299694, "FY2024": 299694, "FY2023": 299694, "FY2022": 299694, "FY2021": 299694, "FY2020": 299694, "FY2019": 299694, "FY2018": 141953}),
    ("DATA", "Retained earnings", {"FY2025": 704929, "FY2024": 885513, "FY2023": 870178, "FY2022": 814442, "FY2021": 751213, "FY2020": 694019, "FY2019": 627278, "FY2018": 587423, "FY2017": 493712, "FY2016": 413640, "FY2015": 361089, "FY2014": 354075}),
    ("DATA", "Other reserves", {"FY2025": 104003, "FY2024": 98641, "FY2023": 95634, "FY2022": 95251, "FY2021": 98394, "FY2020": 93687, "FY2019": 81224, "FY2018": 79934, "FY2017": 65261, "FY2016": 51293, "FY2015": 59093, "FY2014": 58975}),
    ("TOTAL", "Total equity", {"FY2025": 3156622, "FY2024": 1781844, "FY2023": 1763502, "FY2022": 1707383, "FY2021": 1647297, "FY2020": 1585396, "FY2019": 1506192, "FY2018": 1307306, "FY2017": 1056969, "FY2016": 962929, "FY2015": 918178, "FY2014": 911046}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 53258000, "FY2024": 52030428, "FY2023": 54013806, "FY2022": 53313467, "FY2021": 49173176, "FY2020": 47763332, "FY2019": 44888976, "FY2018": 48518274, "FY2017": 40034945, "FY2016": 34426634, "FY2015": 27789316, "FY2014": 27963580}),
]
bw.add_balance_sheet_sheet(
    title="RBC Europe Limited — Balance Sheet",
    subtitle="RBC Europe Limited own entity basis, £'000. FY2021 restated per the 2022 accounts' own note 1(f) "
              "(consistent with the existing Cash Flow Statement's convention). Client Relationships/Goodwill "
              "intangibles first appear in FY2025 following the acquisition of Brewin Dolphin Limited's wealth "
              "management business (see note 38 of the FY2025 filing) - genuinely absent in earlier years, not a gap. "
              "FY2014-FY2020 added under HD-018: no Other equity (AT1) existed before FY2018; FY2016 had a small net "
              "pension liability instead of an asset (own row); small legacy 'Goodwill and other intangibles' "
              "balances predate and are unrelated to the FY2025 intangibles.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + HISTORICAL_STATEMENTS_SOURCES,
    first_col_width=90,
    source_height=420,
    unit_suffix=" (£'000)",
)

income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 2110523, "FY2024": 2672691, "FY2023": 2438356, "FY2022": 782506, "FY2021": 336869, "FY2020": 498156, "FY2019": 739016, "FY2018": 581731, "FY2017": 395233, "FY2016": 307165, "FY2015": 308436, "FY2014": 299146}),
    ("DATA", "Interest expense", {"FY2025": -2060032, "FY2024": -2621243, "FY2023": -2389970, "FY2022": -688112, "FY2021": -159612, "FY2020": -386896, "FY2019": -645594, "FY2018": -521109, "FY2017": -297769, "FY2016": -255013, "FY2015": -462860, "FY2014": -444705}),
    ("TOTAL", "Net interest income", {"FY2025": 50491, "FY2024": 51448, "FY2023": 48386, "FY2022": 94394, "FY2021": 177257, "FY2020": 111260, "FY2019": 93422, "FY2018": 60622, "FY2017": 97464, "FY2016": 52152, "FY2015": -154424, "FY2014": -145559}),
    ("DATA", "Fees and commission income", {"FY2025": 714140, "FY2024": 312383, "FY2023": 275441, "FY2022": 278815, "FY2021": 251058, "FY2020": 237200, "FY2019": 194899, "FY2018": 262799, "FY2017": 237767, "FY2016": 202869, "FY2015": 207488, "FY2014": 174809}),
    ("DATA", "Fees and commission expense", {"FY2025": -85814, "FY2024": -80055, "FY2023": -88513, "FY2022": -79824, "FY2021": -46225, "FY2020": -10878, "FY2019": -21937, "FY2018": -22547, "FY2017": -31436, "FY2016": -29081, "FY2015": -21690, "FY2014": -21130}),
    ("TOTAL", "Net fees and commission income", {"FY2025": 628326, "FY2024": 232328, "FY2023": 186928, "FY2022": 198991, "FY2021": 204833, "FY2020": 226322, "FY2019": 172962, "FY2018": 240252, "FY2017": 206331, "FY2016": 173788, "FY2015": 185798, "FY2014": 153679}),
    ("DATA", "Net trading income", {"FY2025": 250197, "FY2024": 199297, "FY2023": 263103, "FY2022": 172722, "FY2021": 67720, "FY2020": 194113, "FY2019": 142677, "FY2018": 166019, "FY2017": 127482, "FY2016": 147294, "FY2015": 277203, "FY2014": 249952}),
    ("TOTAL", "Total operating income", {"FY2025": 929014, "FY2024": 483073, "FY2023": 498417, "FY2022": 466107, "FY2021": 449810, "FY2020": 531695, "FY2019": 409061, "FY2018": 466893, "FY2017": 431277, "FY2016": 373234, "FY2015": 308577, "FY2014": 258072}),
    ("DATA", "Provision for credit losses: (charge)/credit", {"FY2025": -50253, "FY2024": 1208, "FY2023": -4361, "FY2022": 3878, "FY2021": 7435, "FY2020": -14457, "FY2019": -6678, "FY2018": -1601, "FY2017": -88, "FY2016": -3814, "FY2015": 0, "FY2014": 129}),
    ("TOTAL", "Net operating income", {"FY2025": 878761, "FY2024": 484281, "FY2023": 494056, "FY2022": 469985, "FY2021": 457245, "FY2020": 517238, "FY2019": 402383, "FY2018": 465292, "FY2017": 431189, "FY2016": 369420, "FY2015": 308577, "FY2014": 258201}),
    ("DATA", "Human resources", {"FY2025": -381054, "FY2024": -176324, "FY2023": -182971, "FY2022": -175504, "FY2021": -171245, "FY2020": -184190, "FY2019": -177084, "FY2018": -178245, "FY2017": -177300, "FY2016": -163665, "FY2015": -172393, "FY2014": -162193}),
    ("DATA", "Related party charges & recoveries", {"FY2025": -321055, "FY2024": -128194, "FY2023": -129311, "FY2022": -121211, "FY2021": -103641, "FY2020": -100806, "FY2019": -96002, "FY2018": -97431, "FY2017": -83373, "FY2016": -80984, "FY2015": -70062, "FY2014": -58813}),
    ("DATA", "Other operating expenses", {"FY2025": -209812, "FY2024": -120796, "FY2023": -84918, "FY2022": -83603, "FY2021": -72250, "FY2020": -67426, "FY2019": -64454, "FY2018": -57937, "FY2017": -61203, "FY2016": -58594, "FY2015": -56548, "FY2014": -47429}),
    ("TOTAL", "Total operating expenses", {"FY2025": -911921, "FY2024": -425314, "FY2023": -397200, "FY2022": -380318, "FY2021": -347136, "FY2020": -352422, "FY2019": -337540, "FY2018": -333613, "FY2017": -321876, "FY2016": -303243, "FY2015": -299003, "FY2014": -268435}),
    ("TOTAL", "(Loss)/Profit before income tax", {"FY2025": -33160, "FY2024": 58967, "FY2023": 96856, "FY2022": 89667, "FY2021": 110109, "FY2020": 164816, "FY2019": 64843, "FY2018": 131679, "FY2017": 109313, "FY2016": 66177, "FY2015": 9574, "FY2014": -10234}),
    ("DATA", "Income tax", {"FY2025": -11163, "FY2024": -12355, "FY2023": -10993, "FY2022": -8789, "FY2021": -20179, "FY2020": -39079, "FY2019": -14193, "FY2018": -32995, "FY2017": -29241, "FY2016": -13626, "FY2015": -2560, "FY2014": 3085}),
    ("TOTAL", "Net (loss)/profit", {"FY2025": -44323, "FY2024": 46612, "FY2023": 85863, "FY2022": 80878, "FY2021": 89930, "FY2020": 125737, "FY2019": 50650, "FY2018": 98684, "FY2017": 80072, "FY2016": 52551, "FY2015": 7014, "FY2014": -7149}),
    ("SECTION", "Other comprehensive income / (loss), net of tax", {}),
    ("DATA", "Unrealised gains/(losses) on debt securities at FVOCI", {"FY2025": 1302, "FY2024": 7, "FY2023": 512, "FY2022": -551, "FY2021": 1697, "FY2020": 6250, "FY2019": 1226, "FY2018": 1302, "FY2017": 13228, "FY2016": 3721, "FY2015": -1562, "FY2014": -1386}),
    ("DATA", "Provision for credit losses recognised in OCI", {"FY2025": -22, "FY2024": 1, "FY2023": 8, "FY2022": -2, "FY2021": 160, "FY2020": -135}),
    ("DATA", "Deferred tax on debt securities FVOCI", {"FY2025": -335, "FY2024": -2, "FY2023": -97, "FY2022": 311, "FY2021": 276, "FY2020": -581}),
    ("DATA", "Reclassification of net gains on FVOCI debt securities to income", {"FY2023": -45, "FY2022": -859, "FY2021": -3305, "FY2020": -3340}),
    ("DATA", "Net gains on derivatives designated as cash flow hedges", {"FY2025": 1967, "FY2024": 76}),
    ("DATA", "Deferred tax on cash flow hedges", {"FY2025": -395, "FY2024": -12}),
    ("DATA", "Reclassification of gains on cash flow hedges to income", {"FY2025": -460, "FY2024": -31}),
    ("DATA", "Unrealised gains on FVOCI equity instruments", {"FY2025": 5959, "FY2024": 3908, "FY2023": 13289, "FY2022": 2423, "FY2021": 3692, "FY2020": 11460}),
    ("DATA", "Deferred tax on FVOCI equity instruments", {"FY2025": -1315, "FY2024": -1114, "FY2023": -7922, "FY2022": 1714, "FY2021": -2266, "FY2020": -1332}),
    ("DATA", "Changes in valuation of post employment benefit assets", {"FY2025": -1816, "FY2024": 225, "FY2023": -6599, "FY2022": -8374, "FY2021": 5960, "FY2020": -94, "FY2019": 64, "FY2018": 13371, "FY2017": 740, "FY2016": -11521, "FY2015": 1680, "FY2014": -807}),
    ("DATA", "Deferred tax on post employment benefit assets", {"FY2025": 477, "FY2024": -51, "FY2023": 1237, "FY2022": 2194, "FY2021": -1506, "FY2020": 238}),
    ("TOTAL", "Total other comprehensive income/(loss), net of tax", {"FY2025": 5362, "FY2024": 3007, "FY2023": 383, "FY2022": -3144, "FY2021": 4708, "FY2020": 12463, "FY2019": 1290, "FY2018": 14676, "FY2017": 13968, "FY2016": -7800, "FY2015": 118, "FY2014": -2193}),
    ("TOTAL", "Total comprehensive (loss)/income attributable to shareholder", {"FY2025": -38961, "FY2024": 49619, "FY2023": 86246, "FY2022": 77734, "FY2021": 94638, "FY2020": 138200, "FY2019": 51940, "FY2018": 113360, "FY2017": 94040, "FY2016": 44751, "FY2015": 7132, "FY2014": -9342}),
]
bw.add_income_statement_sheet(
    title="RBC Europe Limited — Profit & Loss",
    subtitle="RBC Europe Limited own entity basis, £'000. FY2021 restated per the 2022 accounts' own note 1(f) "
              "- restated Net profit 89,930 (originally 103,702) and restated Total comprehensive income 94,638 - "
              "consistent with the existing Cash Flow Statement's convention. FY2014-FY2020 added under HD-018: "
              "FY2014/FY2015 genuinely disclosed a net interest EXPENSE (funding/repo costs exceeded interest "
              "income those years) - reproduced as negative 'Net interest income' exactly as disclosed, not an "
              "error. Pre-FY2020 OCI is shown at the same net-of-tax granularity actually disclosed each year "
              "(fewer line items existed before cash flow hedges and cost-of-hedging reclassifications were "
              "introduced); every year's own Total OCI and Total comprehensive income ties to the source exactly.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + HISTORICAL_STATEMENTS_SOURCES,
    first_col_width=90,
    source_height=400,
    unit_suffix=" (£'000)",
)

equity_headers = ["Common shares", "Other equities", "Capital contribution", "Share premium", "FVOCI securities", "Cash Flow Hedges", "Post employment benefits", "Other Reserves", "Retained earnings", "Total equity"]
equity_rows = [
    ("TOTAL", "Balance at 31 October 2013", (497996, None, 36619, 803, 19712, None, 4034, 61168, 361224, 920388)),
    ("DATA", "Net loss", (None, None, None, None, None, None, None, None, -7149, -7149)),
    ("DATA", "Net change in gains on available-for-sale securities", (None, None, None, None, -1386, None, None, -1386, None, -1386)),
    ("DATA", "Changes in valuation of post employment benefit assets", (None, None, None, None, None, None, -807, -807, None, -807)),
    ("TOTAL", "Balance at 31 October 2014", (497996, None, 36619, 803, 18326, None, 3227, 58975, 354075, 911046)),
    ("DATA", "Net profit", (None, None, None, None, None, None, None, None, 7014, 7014)),
    ("DATA", "Net change in gains on available-for-sale securities", (None, None, None, None, -1562, None, None, -1562, None, -1562)),
    ("DATA", "Changes in valuation of post employment benefit assets", (None, None, None, None, None, None, 1680, 1680, None, 1680)),
    ("TOTAL", "Balance at 31 October 2015", (497996, None, 36619, 803, 16764, None, 4907, 59093, 361089, 918178)),
    ("DATA", "Net profit", (None, None, None, None, None, None, None, None, 52551, 52551)),
    ("DATA", "Net change in gains on available-for-sale securities", (None, None, None, None, 3721, None, None, 3721, None, 3721)),
    ("DATA", "Changes in valuation of post employment benefit assets", (None, None, None, None, None, None, -11521, -11521, None, -11521)),
    ("TOTAL", "Balance at 31 October 2016", (497996, None, 36619, 803, 20485, None, -6614, 51293, 413640, 962929)),
    ("DATA", "Net profit", (None, None, None, None, None, None, None, None, 80072, 80072)),
    ("DATA", "Net change in gains on available-for-sale securities", (None, None, None, None, 13228, None, None, 13228, None, 13228)),
    ("DATA", "Changes in valuation of post employment benefit assets", (None, None, None, None, None, None, 740, 740, None, 740)),
    ("TOTAL", "Balance at 31 October 2017", (497996, None, 36619, 803, 33713, None, -5874, 65261, 493712, 1056969)),
    ("DATA", "Issuance of Additional Tier 1 other equity", (None, 141953, None, None, None, None, None, None, None, 141953)),
    ("DATA", "Net profit", (None, None, None, None, None, None, None, None, 98684, 98684)),
    ("DATA", "Net change in gains on FVOCI securities (renamed from available-for-sale on IFRS 9 adoption)", (None, None, None, None, 1302, None, None, 1302, None, 1302)),
    ("DATA", "Changes in valuation of post employment benefit assets", (None, None, None, None, None, None, 13371, 13371, None, 13371)),
    ("DATA", "Transition adjustment to retained earnings (IFRS 9 initial application, note 2)", (None, None, None, None, None, None, None, None, -880, -880)),
    ("DATA", "Dividends on other equities", (None, None, None, None, None, None, None, None, -4093, -4093)),
    ("TOTAL", "Balance at 31 October 2018 and 1 November 2018", (497996, 141953, 36619, 803, 35015, None, 7497, 79934, 587423, 1307306)),
    ("DATA", "Issuance of Additional Tier 1 other equity", (None, 157741, None, None, None, None, None, None, None, 157741)),
    ("DATA", "Net profit", (None, None, None, None, None, None, None, None, 50650, 50650)),
    ("DATA", "Net change in gains on FVOCI securities", (None, None, None, None, 1226, None, None, 1226, None, 1226)),
    ("DATA", "Changes in valuation of post employment benefit assets", (None, None, None, None, None, None, 64, 64, None, 64)),
    ("DATA", "Dividends on other equities", (None, None, None, None, None, None, None, None, -10795, -10795)),
    ("TOTAL", "Balance at 31 October 2019 and 1 November 2019", (497996, 299694, 36619, 803, 36241, None, 7561, 81224, 627278, 1506192)),
    ("DATA", "Net profit", (None, None, None, None, None, None, None, None, 125737, 125737)),
    ("DATA", "Net change in gains on FVOCI securities", (None, None, None, None, 12322, None, None, 12322, None, 12322)),
    ("DATA", "Changes in valuation of post employment benefit assets", (None, None, None, None, None, None, 141, 141, None, 141)),
    ("DATA", "Consideration for transfer of Investment Management business", (None, None, None, None, None, None, None, None, -42000, -42000)),
    ("DATA", "Dividends on other equities", (None, None, None, None, None, None, None, None, -16996, -16996)),
    ("TOTAL", "Balance at 31 October 2020 (as originally reported)", (497996, 299694, 36619, 803, 48563, None, 7702, 93687, 694019, 1585396)),
    ("DATA", "Correction of error (FY2021 restatement, note 1(f) of the FY2022 filing) - applied retrospectively to this opening balance", (None, None, None, None, None, None, None, None, -19810, -19810)),
    ("TOTAL", "Restated balance at 1 November 2020", (497996, 299694, 36619, 803, 48563, None, 7702, 93687, 674209, 1565586)),
    ("DATA", "Net profit (prior to restatement)", (None, None, None, None, None, None, None, None, 103702, 103702)),
    ("DATA", "Net change in gains on FVOCI securities", (None, None, None, None, 254, None, None, 254, None, 254)),
    ("DATA", "Changes in valuation of post employment benefit assets", (None, None, None, None, None, None, 4454, 4454, None, 4454)),
    ("DATA", "Dividends on other equities", (None, None, None, None, None, None, None, None, -12927, -12927)),
    ("DATA", "Correction of error (FY2021 restatement, note 1(f))", (None, None, None, None, None, None, None, None, -13772, -13772)),
    ("TOTAL", "Restated balance at 31 October 2021 and 1 November 2021", (497996, 299694, 36619, 803, 48817, None, 12156, 98395, 751212, 1647297)),
    ("DATA", "Net profit", (None, None, None, None, None, None, None, None, 80878, 80878)),
    ("DATA", "Net change in gains on FVOCI securities", (None, None, None, None, 3036, None, None, 3036, None, 3036)),
    ("DATA", "Changes in valuation of post employment benefit assets", (None, None, None, None, None, None, -6180, -6180, None, -6180)),
    ("DATA", "Dividends on other equities", (None, None, None, None, None, None, None, None, -17648, -17648)),
    ("TOTAL", "Balance at 31 October 2022 and 1 November 2022", (497996, 299694, 36619, 803, 51853, None, 5976, 95251, 814442, 1707383)),
    ("DATA", "Net profit", (None, None, None, None, None, None, None, None, 85863, 85863)),
    ("DATA", "Net change in gains on FVOCI securities", (None, None, None, None, 5745, None, None, 5745, None, 5745)),
    ("DATA", "Changes in valuation of post employment benefit assets", (None, None, None, None, None, None, -5362, -5362, None, -5362)),
    ("DATA", "Dividends on other equities", (None, None, None, None, None, None, None, None, -30127, -30127)),
    ("TOTAL", "Balance at 31 October 2023 and 1 November 2023", (497996, 299694, 36619, 803, 57598, 0, 614, 95634, 870178, 1763502)),
    ("DATA", "Net profit", (None, None, None, None, None, None, None, None, 46612, 46612)),
    ("DATA", "Net change in gains on FVOCI securities", (None, None, None, None, 2800, None, None, 2800, None, 2800)),
    ("DATA", "Net change in gains on Cash Flow Hedges", (None, None, None, None, None, 33, None, 33, None, 33)),
    ("DATA", "Changes in valuation of post employment benefit assets", (None, None, None, None, None, None, 174, 174, None, 174)),
    ("DATA", "Dividends on other equities", (None, None, None, None, None, None, None, None, -31277, -31277)),
    ("TOTAL", "Balance at 31 October 2024 and 1 November 2024", (497996, 299694, 36619, 803, 60398, 33, 788, 98641, 885513, 1781844)),
    ("DATA", "Issuance of common shares", (1550000, None, None, None, None, None, None, None, None, 1550000)),
    ("DATA", "Net loss", (None, None, None, None, None, None, None, None, -44323, -44323)),
    ("DATA", "Net change in gains on FVOCI securities", (None, None, None, None, 5589, None, None, 5589, None, 5589)),
    ("DATA", "Net change in gains on Cash Flow Hedges", (None, None, None, None, None, 1112, None, 1112, None, 1112)),
    ("DATA", "Contributions to the transfer of a business under common control", (None, None, None, None, None, None, None, None, -108589, -108589)),
    ("DATA", "Changes in valuation of post employment benefit assets", (None, None, None, None, None, None, -1339, -1339, None, -1339)),
    ("DATA", "Dividends on other equities", (None, None, None, None, None, None, None, None, -27672, -27672)),
    ("TOTAL", "Balance at 31 October 2025", (2047996, 299694, 36619, 803, 65987, 1145, -551, 104003, 704929, 3156622)),
]
bw.add_equity_changes_sheet(
    title="RBC Europe Limited — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, RBC Europe Limited own entity basis, £'000. Equity "
              "reconciliation ladder confirmed: every year's own closing balance ties exactly to both the next "
              "year's own opening balance and that year's own Balance Sheet Total equity - zero undocumented "
              "plug rows anywhere across all 12 years (FY2013 opening through FY2025 closing). The FY2021 "
              "'Correction of error' row is a genuine, bank-disclosed restatement (note 1(f) of the FY2022 "
              "filing), not an error introduced here - it is applied here at the FY2020/FY2021 boundary since "
              "that is where the FY2020 own-year filing (as extended under HD-018) and the FY2022 filing's "
              "restated comparative diverge by exactly £19,810k. A £1 rounding artifact exists between this "
              "statement's own Retained earnings/Other Reserves split for the FY2021 restated closing balance "
              "(751,212 / 98,395) and the Balance Sheet's own split for the same date (751,213 / 98,394) - the "
              "two sub-lines differ by £1 in opposite directions and net to the identical Total equity figure, "
              "so both are reproduced exactly as each source states them. FY2014-FY2020 added under HD-018: no "
              "Additional Tier 1 'other equity' existed before the FY2018 issuance (blank, not zero); the FY2018 "
              "IFRS 9 transition adjustment and the FY2020 Investment Management business transfer are genuine, "
              "one-off, bank-disclosed items.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + HISTORICAL_STATEMENTS_SOURCES,
    first_col_width=70,
    source_height=420,
)

rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("TOTAL", "Net cash (outflow)/inflow from operating activities", {"FY2025": -2827725, "FY2024": -4638153, "FY2023": -1165304, "FY2022": 5441607, "FY2021": 3898171, "FY2020": -1894560, "FY2019": -1263852, "FY2018": -822129, "FY2017": 2372282, "FY2016": 868235, "FY2015": -825558, "FY2014": -656223}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("TOTAL", "Net cash from investing activities", {"FY2025": -1153173, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0, "FY2020": -42000, "FY2019": 0, "FY2018": 0, "FY2017": 0, "FY2016": 0, "FY2015": 0, "FY2014": 0}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Interest on subordinated liabilities", {"FY2025": -16674, "FY2024": -5638, "FY2023": -4890, "FY2022": -1637, "FY2021": -1354}),
    ("DATA", "Dividends on other equity", {"FY2025": -27672, "FY2024": -31277, "FY2023": -30127, "FY2022": -17648, "FY2021": -12927, "FY2020": -16996, "FY2019": -10795, "FY2018": -4093}),
    ("DATA", "Issue of subordinated liabilities", {"FY2025": 209396}),
    ("DATA", "Issue of common shares", {"FY2025": 1550000}),
    ("DATA", "Issue/repayment of subordinated liabilities and FX (pre-FY2021 years, combined as disclosed)", {"FY2017": -26057, "FY2016": 68617, "FY2015": 8771, "FY2014": -67560}),
    ("DATA", "Issue of other equity (Additional Tier 1)", {"FY2019": 157741, "FY2018": 141953}),
    ("TOTAL", "Net cash inflow/(outflow) from financing activities", {"FY2025": 1715050, "FY2024": -36915, "FY2023": -35017, "FY2022": -19285, "FY2021": -14281, "FY2020": -17050, "FY2019": -10823, "FY2018": 71542, "FY2017": -26057, "FY2016": 68617, "FY2015": 8771, "FY2014": -67560}),
    ("DATA", "Effect of exchange rate changes on cash and due from banks (added to reach closing cash)", {"FY2025": 344323, "FY2024": -217052, "FY2023": -46137, "FY2022": 0, "FY2021": 0}),
    ("TOTAL", "Net decrease/increase in cash and cash equivalents before exchange-rate effect", {"FY2025": -2265848, "FY2024": -4675068, "FY2023": -1200321, "FY2022": 5422322, "FY2021": 3883890, "FY2020": -1953610, "FY2019": -1274675, "FY2018": -750587, "FY2017": 2346225, "FY2016": 936852, "FY2015": -816787, "FY2014": -723783}),
    ("DATA", "Cash and cash equivalents at the beginning of the financial year", {"FY2025": 4455652, "FY2024": 9347772, "FY2023": 10594230, "FY2022": 5171908, "FY2021": 1288018, "FY2020": 3241628, "FY2019": 4516303, "FY2018": 5266890, "FY2017": 2920665, "FY2016": 1983813, "FY2015": 2800600, "FY2014": 3524383}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 2534127, "FY2024": 4455652, "FY2023": 9347772, "FY2022": 10594230, "FY2021": 5171908, "FY2020": 1288018, "FY2019": 3241628, "FY2018": 4516303, "FY2017": 5266890, "FY2016": 2920665, "FY2015": 1983813, "FY2014": 2800600}),
]
HISTORICAL_CASH_FLOW_SOURCES = (
    "Sources - RBC Europe Limited's own Statement of Cash Flows, £'000, image-only Companies House scans, OCR'd "
    "(HD-018):\n"
    f"FY2020: Full accounts made up to 31 October 2020, p.29 - {AR_URL['FY2020']}\n"
    f"FY2019: Full accounts made up to 31 October 2019, p.20 - {AR_URL['FY2019']}\n"
    f"FY2018: Full accounts made up to 31 October 2018 (own-year figures), p.20 - {AR_URL['FY2018']}\n"
    f"FY2017: Full accounts made up to 31 October 2017, p.16 - {AR_URL['FY2017']}\n"
    f"FY2016: Full accounts made up to 31 October 2017, p.16 (2016 comparative column) - {AR_URL['FY2017']}\n"
    f"FY2015: Full accounts made up to 31 October 2015, p.13 - {AR_URL['FY2015']}\n"
    f"FY2014: Full accounts made up to 31 October 2015, p.13 (2014 comparative column) - {AR_URL['FY2015']}\n"
    "FY2014-FY2020 did not separately present an exchange-rate effect line (FX is embedded within the operating "
    "activities detail) - the 'Net decrease/increase' line for those years already reconciles opening to closing "
    "cash directly, verified for all seven years. Closing cash in each of these years ties exactly to the next "
    "year's own opening cash, and FY2020's closing cash (£1,288,018k) ties exactly to the existing FY2021 sheet's "
    "own opening-cash figure."
)
bw.add_cash_flow_sheet(title="RBC Europe Limited — Statement of Cash Flows", subtitle="RBC Europe Limited own entity basis, £'000; source net-change line is before separately reported exchange-rate effect (FY2021-FY2025 only; FY2014-FY2020 reconcile directly with no separate FX line)", rows=rows, sources_text=CASH_FLOW_SOURCES + "\nRECONCILIATION NOTE: In each year, the source's reported net decrease/increase equals operating + investing + financing cash flows before the separately presented exchange-rate effect. Closing cash equals opening cash + that net-change line + the exchange-rate effect.\n\n" + HISTORICAL_CASH_FLOW_SOURCES, first_col_width=78, source_height=340, unit_suffix=" (£'000)")

asset_quality_rows = [
    ("SECTION", "Loans and advances, loan commitments and financial guarantees issued, IFRS 9 stage gross carrying amount", {}),
    ("DATA", "Stage 1 (performing)", {"FY2025": 6996170, "FY2024": 6887944, "FY2023": 7571126, "FY2022": 7623302, "FY2021": 6320002}),
    ("DATA", "Stage 2 (performing)", {"FY2025": 1095341, "FY2024": 456335, "FY2023": 1802, "FY2022": 15858, "FY2021": 28989}),
    ("DATA", "Stage 3 (impaired)", {"FY2025": 89817, "FY2024": 35799, "FY2023": 44262, "FY2022": 0, "FY2021": 14669}),
    ("TOTAL", "Total gross carrying amount", {"FY2025": 8181328, "FY2024": 7380078, "FY2023": 7617190, "FY2022": 7639160, "FY2021": 6363660}),
    ("SECTION", "Allowance for credit losses - loans and advances to customers only", {}),
    ("DATA", "Opening balance", {"FY2025": 4386, "FY2024": 8543, "FY2023": 4097, "FY2022": 8150, "FY2021": 17194}),
    ("DATA", "Provision for credit losses / net movement", {"FY2025": 49163, "FY2024": -3019, "FY2023": -3981, "FY2022": -7056}),
    ("DATA", "Net write-offs", {"FY2025": -30000, "FY2024": -868, "FY2022": -1469}),
    ("DATA", "Exchange rate and other", {"FY2025": 128, "FY2024": -86, "FY2023": -72, "FY2022": -519}),
    ("TOTAL", "Closing balance", {"FY2025": 23677, "FY2024": 4386, "FY2023": 8543, "FY2022": 4097, "FY2021": 8150}),
    ("SECTION", "Asset quality ratios (derived)", {}),
    ("DATA", "Stage 2+3 as % of total gross carrying amount", {"FY2025": "14.5%", "FY2024": "6.7%", "FY2023": "0.6%", "FY2022": "0.2%", "FY2021": "0.7%"}),
    ("DATA", "Stage 3 as % of total gross carrying amount", {"FY2025": "1.1%", "FY2024": "0.5%", "FY2023": "0.6%", "FY2022": "0.0%", "FY2021": "0.2%"}),
    ("SECTION", "FY2014-FY2020 (pre-IFRS 9 stage disclosure / simplified banking-book note structure - see note below)", {}),
    ("DATA", "Neither past due nor individually impaired (banking book loans)", {"FY2020": 6014831, "FY2019": 5297265, "FY2018": 4186128, "FY2017": 4745168, "FY2016": 3326372, "FY2015": 2506832}),
    ("DATA", "Individually impaired", {"FY2017": -88}),
    ("DATA", "Less: allowance/collective provision for credit losses", {"FY2020": -17194, "FY2019": -10956, "FY2018": -4202, "FY2017": -3814, "FY2016": -3814}),
    ("TOTAL", "Net loans and advances, banking book (per Note 9/Note 24 of each filing)", {"FY2020": 5997637, "FY2019": 5286309, "FY2018": 4181926, "FY2017": 4741266, "FY2016": 3322558, "FY2015": 2506832}),
]
bw.add_asset_quality_sheet(
    title="RBC Europe Limited — Asset Quality",
    subtitle="IFRS 9 stage gross carrying amount for Loans and advances, Loan commitments and Financial "
              "guarantees issued combined (the scope subject to IFRS 9 impairment requirements per the Company's "
              "own Note 24) - broader than the Balance Sheet's own 'Loans and advances' line alone, so does NOT "
              "tie to that line directly. £'000. FY2014-FY2020 (added under HD-018) predate this IFRS 9 stage "
              "table and are shown in their own section using the bank's actual pre-2021 disclosure structure "
              "(a simpler 'neither past due nor individually impaired' banking-book note, scoped to on-balance-"
              "sheet loans and advances only, not the wider commitments/guarantees scope above) - not forced "
              "into the later template's categories, consistent with how the RWA Breakdown sheet treats FY2021's "
              "older CRR-era table.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - RBC Europe Limited's own Note 24 (Allowance for credit losses), all image-only scans:\n"
        f"FY2025/FY2024: Full accounts made up to 31 October 2025, pp.94-96 - {AR_URL['FY2025']}\n"
        f"FY2023: Full accounts made up to 31 October 2023 (FY2023's own comparative), pp.85-86 - {AR_URL['FY2023']}\n"
        f"FY2022: Full accounts made up to 31 October 2022 (FY2022's own comparative), pp.83-85 - {AR_URL['FY2022']}\n"
        f"FY2021: Full accounts made up to 31 October 2022, p.85 (FY2021's own closing balance, "
        f"the earliest year with a full IFRS 9 stage split table) - {AR_URL['FY2022']}\n\n"
        + ENTITY_NOTE + "\n\nDATA QUALITY NOTE: FY2022's Stage 3 gross carrying amount is genuinely nil "
        "(Balance at 31 October 2022 in the Company's own Note 24 table shows a dash for Stage 3), while the "
        "allowance for credit losses that year still carries a small Stage 3 balance from FY2021 - both figures "
        "reproduced exactly as disclosed, not reconciled to force a tie.\n\n"
        "Sources (HD-018 extension) - RBC Europe Limited's own Note 9 (Credit risk), 'loans and advances in the "
        "banking book' table, image-only Companies House scans, OCR'd:\n"
        f"FY2020: Full accounts made up to 31 October 2020, p.52 - {AR_URL['FY2020']}\n"
        f"FY2019: Full accounts made up to 31 October 2019, p.46 - {AR_URL['FY2019']}\n"
        f"FY2018: Full accounts made up to 31 October 2018, p.50 - {AR_URL['FY2018']}\n"
        f"FY2017: Full accounts made up to 31 October 2017, p.40 - {AR_URL['FY2017']}\n"
        f"FY2016: Full accounts made up to 31 October 2017, p.40 (2016 comparative column) - {AR_URL['FY2017']}\n"
        f"FY2015: Full accounts made up to 31 October 2016, p.38 (2015 comparative column) - {AR_URL['FY2016']}\n"
        "FY2014's own equivalent note table could not be located within a reasonable search of the FY2014/FY2015 "
        "filings (both accessible pages covered policy text, not the numeric table) - self-skipped for this one "
        "row/year per project convention; FY2014's Balance Sheet 'Loans and advances' (£2,803,899k) and Profit & "
        "Loss 'Provision for credit losses' (a £129k credit) remain available on their own sheets."
    ),
    first_col_width=90,
    source_height=460,
    unit_suffix=" (£'000)",
)

def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=52, source_height=150)


INTERIM_SOURCES = {
    "2021 H1": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/2021-Interim-Pillar-III-Disclosure.pdf",
    "2022 H1": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/2022-Interim-Pillar-III-Disclosure.pdf",
    "2023 Q1": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/RBCEL-Jan-2023-Pillar3-Disclosures.pdf",
    "2023 H1": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/RBCEL-April-2023-Semi-Annual-Pillar3-Disclosures.pdf",
    "2023 Q3": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/RBCEL-July2023-Pillar3-Disclosures.pdf",
    "2024 Q1": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/RBCEL-Pillar-3-Jan-24.pdf",
    "2024 H1": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/RBCEL-Pillar-3-Apr-24.pdf",
    "2024 Q3": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/2024-Q3-Pillar-III-Diclosure.pdf",
    "2025 Q1": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/2025-q1-pillar-iii-disclosure.pdf",
    "2025 H1": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/2025-semi-annual-pillar-iii-disclosure.pdf",
    "2025 Q3": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/2025-Q3-Pillar-III-Disclosure.pdf",
}


def add_interim_pillar3_sheet():
    """Add entity-level RBCEL interim observations from official disclosures."""
    headers = ["Period", "Disclosure type", "Metric", "Value", "Unit", "Basis", "Source document", "Page / table"]
    rows = []

    def add(period, disclosure_type, metric_name, value, unit, basis, page):
        rows.append((period, disclosure_type, metric_name, value, unit, basis,
                     f"RBC Europe Limited {period} Pillar III disclosure", page))

    # The 2021 and 2022 reports use the transitional/CRR-era presentation;
    # values below are the headline figures reported in their own tables.
    add("Apr-21", "Semi-annual", "Common Equity Tier 1 (CET1) capital", 1257, "£m", "Company / transitional own-funds table", "p.4, Table 2")
    add("Apr-21", "Semi-annual", "Tier 1 capital", 1557, "£m", "Company / transitional own-funds table", "p.4, Table 2")
    add("Apr-21", "Semi-annual", "Total capital", 1629, "£m", "Company / transitional own-funds table", "p.4, Table 2")
    add("Apr-21", "Semi-annual", "Total risk-weighted exposures", 8642, "£m", "Company / transitional own-funds table", "p.4, Table 2")
    add("Apr-21", "Semi-annual", "Common Equity Tier 1 ratio", "14.5%", "%", "Company / transitional own-funds table", "p.4, Table 2")
    add("Apr-21", "Semi-annual", "Tier 1 ratio", "18.0%", "%", "Company / transitional own-funds table", "p.4, Table 2")
    add("Apr-21", "Semi-annual", "Total capital ratio", "18.9%", "%", "Company / transitional own-funds table", "p.4, Table 2")
    add("Apr-21", "Semi-annual", "Total leverage ratio exposure", 47141, "£m", "Company / CRR leverage ratio disclosure", "p.5, Table 3")
    add("Apr-21", "Semi-annual", "Leverage ratio", "3.30%", "%", "Company / CRR leverage ratio disclosure", "p.5, Table 3")

    add("Apr-22", "Semi-annual", "Common Equity Tier 1 (CET1) capital", 1344, "£m", "Company / UK KM1", "p.4, Table 1")
    add("Apr-22", "Semi-annual", "Tier 1 capital", 1644, "£m", "Company / UK KM1", "p.4, Table 1")
    add("Apr-22", "Semi-annual", "Total capital", 1724, "£m", "Company / UK KM1", "p.4, Table 1")
    add("Apr-22", "Semi-annual", "Total risk-weighted exposure amount", 9759, "£m", "Company / UK KM1", "p.4, Table 1")
    add("Apr-22", "Semi-annual", "Common Equity Tier 1 ratio", "13.77%", "%", "Company / UK KM1", "p.4, Table 1")
    add("Apr-22", "Semi-annual", "Tier 1 ratio", "16.85%", "%", "Company / UK KM1", "p.4, Table 1")
    add("Apr-22", "Semi-annual", "Total capital ratio", "17.66%", "%", "Company / UK KM1", "p.4, Table 1")
    add("Apr-22", "Semi-annual", "Leverage ratio total exposure measure", 45175, "£m", "Company / UK leverage ratio key metrics", "p.4, Table 2")
    add("Apr-22", "Semi-annual", "Leverage ratio", "3.63%", "%", "Company / UK leverage ratio key metrics", "p.4, Table 2")
    add("Apr-22", "Semi-annual", "Total high-quality liquid assets (HQLA), weighted value-average", 8757, "£m", "Company / UK liquidity key metrics", "p.5, Table 3")
    add("Apr-22", "Semi-annual", "Total net cash outflows, adjusted value", 6881, "£m", "Company / UK liquidity key metrics", "p.5, Table 3")
    add("Apr-22", "Semi-annual", "Liquidity coverage ratio", "127%", "%", "Company / UK liquidity key metrics", "p.5, Table 3")
    add("Apr-22", "Semi-annual", "Total available stable funding", 16464, "£m", "Company / UK liquidity key metrics", "p.5, Table 3")
    add("Apr-22", "Semi-annual", "Total required stable funding", 16249, "£m", "Company / UK liquidity key metrics", "p.5, Table 3")
    add("Apr-22", "Semi-annual", "NSFR ratio", "101%", "%", "Company / UK liquidity key metrics", "p.5, Table 3")

    # From 2023 onward the semi-annual reports use the UK KM1 template;
    # quarterly reports publish only the leverage section.
    h1_metrics = {
        "Apr-23": ("2023 H1", 1362, 1662, 1742, 9222, "14.77%", "18.02%", "18.89%", 42658, "3.90%", 11968, 9515, "126%", 18196, 15752, "116%", "p.2, UK KM1"),
        "Apr-24": ("2024 H1", 1423, 1723, 1803, 10873, "13.09%", "15.85%", "16.85%", 42706, "4.03%", 11174, 8891, "126%", 17116, 14616, "117%", "p.2, UK KM1"),
        "Apr-25": ("2025 H1", 1810, 2110, 2185, 12120, "14.94%", "17.41%", "18.03%", 42018, "5.02%", 11462, 8198, "140%", 18113, 15959, "114%", "p.2, UK KM1"),
    }
    for period, (source_period, cet1, tier1, total, rwa, cet1r, tier1r, totalr, lev_exp, levr, hqla, net_out, lcr, asf, rsf, nsfr, page) in h1_metrics.items():
        for name, value, unit in [
            ("Common Equity Tier 1 (CET1) capital", cet1, "£m"), ("Tier 1 capital", tier1, "£m"),
            ("Total capital", total, "£m"), ("Total risk-weighted exposure amount", rwa, "£m"),
            ("Common Equity Tier 1 ratio", cet1r, "%"), ("Tier 1 ratio", tier1r, "%"),
            ("Total capital ratio", totalr, "%"), ("Leverage ratio total exposure measure excluding claims on central banks", lev_exp, "£m"),
            ("Leverage ratio excluding claims on central banks", levr, "%"),
            ("Total high-quality liquid assets (HQLA), weighted value-average", hqla, "£m"),
            ("Total net cash outflows, adjusted value", net_out, "£m"), ("Liquidity coverage ratio", lcr, "%"),
            ("Total available stable funding", asf, "£m"), ("Total required stable funding", rsf, "£m"),
            ("NSFR ratio", nsfr, "%"),
        ]:
            add(period, "Semi-annual", name, value, unit, "Company / UK KM1", page)

    quarterly = {
        "Jan-23": ("2023 Q1", "4.13%", "3.36%", "0.08%", 50486, 41191, "p.2"),
        "Jul-23": ("2023 Q3", "4.38%", "3.46%", "0.30%", 48617, 39003, "p.2"),
        "Jan-24": ("2024 Q1", "4.24%", "3.59%", "0.28%", 48253, 40359, "p.2"),
        "Jul-24": ("2024 Q3", "4.25%", "3.63%", "0.34%", 46331, 41636, "p.2"),
        "Jan-25": ("2025 Q1", "4.91%", "4.24%", "0.32%", 45272, None, "p.2"),
        "Jul-25": ("2025 Q3", "4.60%", "4.24%", "0.33%", 44665, None, "p.2"),
    }
    for period, (source_period, excl, incl, buffer, avg_incl, avg_excl, page) in quarterly.items():
        add(period, "Quarterly", "Leverage ratio excluding claims on central banks", excl, "%", "Company / leverage ratio disclosure", page)
        add(period, "Quarterly", "Leverage ratio including claims on central banks", incl, "%", "Company / leverage ratio disclosure", page)
        add(period, "Quarterly", "Leverage ratio buffer", buffer, "%", "Company / leverage ratio disclosure", page)
        add(period, "Quarterly", "Average exposure measure including claims on central banks", avg_incl, "£m", "Company / leverage ratio disclosure", page)
        if avg_excl is not None:
            add(period, "Quarterly", "Average exposure measure excluding claims on central banks", avg_excl, "£m", "Company / leverage ratio disclosure", page)

    source_period = {
        "Apr-21": "2021 H1", "Apr-22": "2022 H1",
        "Jan-23": "2023 Q1", "Apr-23": "2023 H1", "Jul-23": "2023 Q3",
        "Jan-24": "2024 Q1", "Apr-24": "2024 H1", "Jul-24": "2024 Q3",
        "Jan-25": "2025 Q1", "Apr-25": "2025 H1", "Jul-25": "2025 Q3",
    }
    hyperlinks = {
        (i, 6): INTERIM_SOURCES[source_period[rows[i][0]]]
        for i in range(len(rows))
    }
    bw.add_wide_interim_sheet(
        "Interim Pillar 3", headers, rows,
        title="RBC Europe Limited — Interim Pillar 3",
        subtitle="Entity-level interim observations from official RBC Europe Limited disclosures, April 2021 to July 2025",
        note="Annual Pillar 3 disclosures remain in the existing annual metric sheets. Quarterly RBCEL reports are limited disclosures focused on leverage; semi-annual reports provide the broader UK KM1 and liquidity metrics shown here. All amounts are £m unless stated otherwise.",
        widths=[16, 16, 58, 16, 12, 38, 48, 18],
        hyperlink_cells=hyperlinks,
    )


CET1 = {"FY2025": 1773, "FY2024": 1454, "FY2023": 1439, "FY2022": 1377, "FY2021": 1348, "FY2020": 1266, "FY2019": 1178, "FY2018": 1140, "FY2017": 1030, "FY2016": 954, "FY2015": 903, "FY2014": 879}
T1 = {"FY2025": 2072, "FY2024": 1754, "FY2023": 1738, "FY2022": 1677, "FY2021": 1649, "FY2020": 1566, "FY2019": 1478, "FY2018": 1282, "FY2017": 1030, "FY2016": 954, "FY2015": 903, "FY2014": 879}
TC = {"FY2025": 2358, "FY2024": 1832, "FY2023": 1821, "FY2022": 1764, "FY2021": 1721, "FY2020": 1643, "FY2019": 1555, "FY2018": 1517, "FY2017": 1242, "FY2016": 1236, "FY2015": 1142, "FY2014": 1122}
RWA = {"FY2025": 12834, "FY2024": 12049, "FY2023": 9579, "FY2022": 8911, "FY2021": 8961, "FY2020": 7810, "FY2019": 8209, "FY2018": 7978, "FY2017": 7157, "FY2016": 5610, "FY2015": 4374, "FY2014": 5105}
CET1R = {"FY2025": "13.81%", "FY2024": "12.07%", "FY2023": "15.02%", "FY2022": "15.46%", "FY2021": "15.05%", "FY2020": "16.2%", "FY2019": "14.4%", "FY2018": "14.3%", "FY2017": "14.4%", "FY2016": "17.0%", "FY2015": "20.6%", "FY2014": "17.2%"}
T1R = {"FY2025": "16.15%", "FY2024": "14.56%", "FY2023": "18.15%", "FY2022": "18.82%", "FY2021": "18.40%", "FY2020": "20.0%", "FY2019": "18.0%", "FY2018": "16.1%", "FY2017": "14.4%", "FY2016": "17.0%", "FY2015": "20.6%", "FY2014": "17.2%"}
TCR = {"FY2025": "18.37%", "FY2024": "15.20%", "FY2023": "19.01%", "FY2022": "19.80%", "FY2021": "19.21%", "FY2020": "21.0%", "FY2019": "18.9%", "FY2018": "19.0%", "FY2017": "17.3%", "FY2016": "22.0%", "FY2015": "26.1%", "FY2014": "22.0%"}
HISTORICAL_CAPITAL_NOTE = ("FY2014-FY2020 (HD-018): EU CRR transitional-provisions basis, own-year filing in each case. "
    "No Additional Tier 1 capital existed before the FY2018 AT1 issuance, so CET1 = Tier 1 exactly for FY2014-FY2017 "
    "- not a data-entry duplication. FY2014's leverage ratio was not yet a disclosure requirement (RBC Europe's own "
    "FY2014 filing states its first published leverage ratio would be for the year ending 31 October 2015).")
metric("CET1 Capital", "£m", [("Common Equity Tier 1 (CET1) capital", CET1)], note=HISTORICAL_CAPITAL_NOTE)
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 (CET1) ratio", CET1R)], note=HISTORICAL_CAPITAL_NOTE)
metric("Tier 1 Capital", "£m", [("Tier 1 capital", T1)], note=HISTORICAL_CAPITAL_NOTE)
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", T1R)], note=HISTORICAL_CAPITAL_NOTE)
metric("Total Capital", "£m", [("Total capital", TC)], note=HISTORICAL_CAPITAL_NOTE)
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", TCR)], note=HISTORICAL_CAPITAL_NOTE)
metric("Total RWAs", "£m", [("Total risk-weighted exposure amount", RWA)], note=HISTORICAL_CAPITAL_NOTE)

rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 4362, "FY2024": 3702, "FY2023": 3673, "FY2022": 3061}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 3671, "FY2024": 3757, "FY2023": 1895, "FY2022": 1954}),
    ("DATA", "Settlement risk", {"FY2025": 0, "FY2024": 1, "FY2023": 1, "FY2022": 8}),
    ("DATA", "Securitisation exposures in the non-trading book (after the cap)", {"FY2025": 44, "FY2024": 61, "FY2023": 30, "FY2022": 133}),
    ("DATA", "Position, foreign exchange and commodities risks (Market risk)", {"FY2025": 3563, "FY2024": 3624, "FY2023": 3095, "FY2022": 2856}),
    ("DATA", "Operational risk", {"FY2025": 1194, "FY2024": 905, "FY2023": 884, "FY2022": 900}),
    ("TOTAL", "Total risk-weighted exposure amount", {"FY2025": 12834, "FY2024": 12049, "FY2023": 9579, "FY2022": 8911}),
    ("SECTION", "FY2016-FY2021 (older CRR-era table, different category structure - see note below)", {}),
    ("DATA", "Banking book credit risk", {"FY2021": 2993, "FY2020": 2822, "FY2019": 2860, "FY2018": 2753, "FY2017": 2657, "FY2016": 2346}),
    ("DATA", "Counterparty credit risk", {"FY2021": 1904, "FY2020": 1368, "FY2019": 2142, "FY2018": 1903, "FY2017": 1553, "FY2016": 1117}),
    ("DATA", "Default fund contributions to a CCP", {"FY2021": 46, "FY2020": 24, "FY2019": 11, "FY2018": 36, "FY2017": 57, "FY2016": 53}),
    ("DATA", "Settlement/delivery risk (Trading book)", {"FY2021": 3, "FY2020": 1, "FY2019": 3, "FY2018": 2, "FY2017": 0, "FY2016": 0}),
    ("DATA", "Position, foreign exchange and commodities risks (Market risk)", {"FY2021": 3130, "FY2020": 2708, "FY2019": 2369, "FY2018": 2484, "FY2017": 2188, "FY2016": 1491}),
    ("DATA", "Operational risk", {"FY2021": 881, "FY2020": 880, "FY2019": 817, "FY2018": 795, "FY2017": 696, "FY2016": 587}),
    ("DATA", "Credit valuation adjustment (CVA)", {"FY2021": 4, "FY2020": 7, "FY2019": 8, "FY2018": 7, "FY2017": 7, "FY2016": 15}),
    ("TOTAL", "Total risk-weighted exposure amount (FY2016-FY2021 own tables)", {"FY2021": 8961, "FY2020": 7810, "FY2019": 8209, "FY2018": 7978, "FY2017": 7157, "FY2016": 5610}),
    ("SECTION", "FY2014-FY2015 (earliest available Pillar 3 disclosures - combined credit/counterparty structure)", {}),
    ("DATA", "Credit and counterparty credit risk (combined, standardised approach)", {"FY2015": 2699, "FY2014": 2324}),
    ("DATA", "Default fund contributions to a CCP (FY2014/FY2015)", {"FY2015": 7, "FY2014": 5}),
    ("DATA", "Settlement/delivery risk, Trading book (FY2014/FY2015)", {"FY2015": 1, "FY2014": 7}),
    ("DATA", "Position, foreign exchange and commodities risks, Market risk (FY2014/FY2015)", {"FY2015": 1146, "FY2014": 2289}),
    ("DATA", "Operational risk (FY2014/FY2015)", {"FY2015": 496, "FY2014": 417}),
    ("DATA", "Credit valuation adjustment, CVA (FY2014/FY2015)", {"FY2015": 26, "FY2014": 63}),
    ("TOTAL", "Total risk-weighted exposure amount (FY2014/FY2015 own tables)", {"FY2015": 4374, "FY2014": 5105}),
]
bw.add_rwa_breakdown_sheet(
    title="RBC Europe Limited — RWA Breakdown",
    subtitle="Company-level (RBCEL), £m for FY2022-FY2025 and FY2021; £'000 for FY2014-FY2020 (unit differs by "
              "section, see row labels). FY2022-FY2025 from Pillar 3 UK OV1 tables. FY2021's own Pillar 3 "
              "disclosure predates the UK OV1 template and uses an older CRR-era risk-category structure - shown "
              "as its own separate section rather than forced into the later template's categories (both totals "
              "tie exactly to the Total RWAs sheet). FY2016-FY2020 (added under HD-018) use the same older "
              "category structure as FY2021's section and are grouped with it; FY2014-FY2015 predate even that "
              "structure (no separate Banking book/Counterparty credit risk split was disclosed) and get their "
              "own section.",
    rows=rwa_breakdown_rows,
    sources_text=(
        "Sources - RBC Europe Limited annual Pillar III disclosures, UK OV1 - Overview of Risk Weighted "
        "Exposure Amounts (FY2022-FY2025) / Table 1: Distribution of Risk-weighted amount (FY2021):\n"
        f"FY2025: p.17 - {P3_URL['FY2025']}\n"
        f"FY2024: p.17 (FY2025 document's own FY2024 comparative column) - {P3_URL['FY2025']}\n"
        f"FY2023: p.18 - {P3_URL['FY2023']}\n"
        f"FY2022: p.18 (FY2023 document's own FY2022 comparative column) - {P3_URL['FY2023']}\n"
        f"FY2021: p.6 - {P3_URL['FY2021']}\n" + ENTITY_NOTE + "\n\n"
        "Sources (HD-018 extension) - RBC Europe Limited annual Pillar III disclosures, 'Table 1: Distribution of "
        "Risk-weighted amount' (FY2016-FY2020) / 'Table 7/Table 8: Risk exposure amount by risk type' (FY2014/FY2015):\n"
        f"FY2020: p.3 - {P3_URL['FY2020']}\n"
        f"FY2019: p.3 (FY2020 document's own FY2019 comparative column) - {P3_URL['FY2020']}\n"
        f"FY2018: p.3 (FY2019 document's own FY2018 comparative column) - {P3_URL['FY2019']}\n"
        f"FY2017: p.3 (FY2018 document's own FY2017 comparative column) - {P3_URL['FY2018']}\n"
        f"FY2016: p.3 - {P3_URL['FY2016']}\n"
        f"FY2015: p.23 (with-transitional-provisions table) - {P3_URL['FY2015']}\n"
        f"FY2014: pp.18-19 (with-transitional-provisions table) - {P3_URL['FY2014']}\n"
        "FY2014/FY2015 units are £'000 (not £m, unlike every other section on this sheet) - reproduced exactly as "
        "each source discloses; see the row labels for the £'000 vs £m distinction."
    ),
    first_col_width=76,
    source_height=420,
    unit_suffix="",
)

metric("Leverage Ratio", "£m / %", [("Total exposure measure excluding claims on central banks", {"FY2025": 45993, "FY2024": 42872, "FY2023": 40693, "FY2022": 40753}), ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "4.51%", "FY2024": "4.09%", "FY2023": "4.27%", "FY2022": "4.12%"}), ("Total leverage ratio exposure (older CRR leverage table, FY2015-FY2021)", {"FY2021": 46925, "FY2020": 44648.596, "FY2019": 46933.644, "FY2018": 46509.827, "FY2017": 43328.495, "FY2016": 38502.673, "FY2015": 30412.357}), ("Leverage ratio (older CRR leverage table, FY2015-FY2021)", {"FY2021": "3.51%", "FY2020": "3.51%", "FY2019": "3.15%", "FY2018": "2.76%", "FY2017": "2.38%", "FY2016": "2.48%", "FY2015": "2.97%"})], note="FY2015-FY2021 (FY2015-FY2020 added under HD-018) all use the same older, single 'Total leverage ratio exposure' CRR table (total exposure £46,924.653m; ratio 3.51% for FY2021, own-year filing for each earlier year) - each year's own narrative text corroborates the prior year's own figure (e.g. the FY2020 filing states '3.51% (2019: 3.15%)', which matches FY2019's own-year table exactly), so all six years are cross-checked, not just transcribed once. From FY2022, KM1 reports the excluding-central-bank basis; the FY2022 report shows FY2021 as N/A under that revised presentation. FY2014 is a genuine blank: RBC Europe's own FY2014 Pillar III disclosure states the Delegated Act required it to first publish a Leverage Ratio for the year ending 31 October 2015, and no numeric ratio appears anywhere in that filing.")
metric("LCR", "£m / %", [("Total high-quality liquid assets (HQLA), weighted value (average)", {"FY2025": 12642, "FY2024": 10688, "FY2023": 11490, "FY2022": 10868}), ("Total net cash outflows, adjusted value", {"FY2025": 9632, "FY2024": 8036, "FY2023": 9031, "FY2022": 8696}), ("Liquidity coverage ratio (%)", {"FY2025": "132%", "FY2024": "134%", "FY2023": "127%", "FY2022": "125%", "FY2021": "Not publicly disclosed", "FY2020": "Not publicly disclosed", "FY2019": "Not publicly disclosed", "FY2018": "Not publicly disclosed", "FY2017": "Not publicly disclosed", "FY2016": "Not publicly disclosed", "FY2015": "Not publicly disclosed", "FY2014": "Not publicly disclosed"})], note="The FY2021 standalone Pillar 3 disclosure contains no LCR table or headline ratio. FY2014-FY2020 (checked under HD-018) are the same: none of the seven annual Pillar III filings contains an LCR table, headline ratio, or HQLA/net-cash-outflow figures - the only 'HQLA' tables present in the FY2019/FY2020 filings are Template A/B Asset Encumbrance disclosures (a different regulatory template, EU 2017/2295), not a liquidity coverage ratio table, and pre-FY2019 filings have no such table at all. Genuinely not disclosed, not unfound.")
metric("NSFR", "£m / %", [("Total available stable funding", {"FY2025": 18791, "FY2024": 17010, "FY2023": 16879, "FY2022": 18964}), ("Total required stable funding", {"FY2025": 16780, "FY2024": 15158, "FY2023": 13654, "FY2022": 17081}), ("NSFR ratio (%)", {"FY2025": "112%", "FY2024": "112%", "FY2023": "124%", "FY2022": "111%", "FY2021": "Not publicly disclosed", "FY2020": "Not publicly disclosed", "FY2019": "Not publicly disclosed", "FY2018": "Not publicly disclosed", "FY2017": "Not publicly disclosed", "FY2016": "Not publicly disclosed", "FY2015": "Not publicly disclosed", "FY2014": "Not publicly disclosed"})], note="The FY2021 standalone Pillar 3 disclosure contains no NSFR table or headline ratio. FY2014-FY2020 (checked under HD-018) are the same: NSFR is only ever discussed as a forthcoming CRR2 requirement ('It is proposed to be applied from January 2022 in the UK', per the FY2020 filing's own text) - no numeric available/required stable funding figures or ratio appear in any of the seven filings. Genuinely not disclosed, not unfound.")
metric("MREL Ratio", "£m / %", [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})], note="No numeric MREL ratio was identified in the five annual RBCEL Pillar 3 disclosures reviewed.")
add_interim_pillar3_sheet()
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 53258000, "FY2024": 52030428, "FY2023": 54013806, "FY2022": 53313467, "FY2021": 49173176}),
        ("Loans and advances", {"FY2025": 8781847, "FY2024": 7810517, "FY2023": 7905674, "FY2022": 8022378, "FY2021": 7034028}),
        ("Deposits by customers", {"FY2025": 12589815, "FY2024": 12134787, "FY2023": 11557114, "FY2022": 11060215, "FY2021": 5600093}),
        ("Total equity", {"FY2025": 3156622, "FY2024": 1781844, "FY2023": 1763502, "FY2022": 1707383, "FY2021": 1647297}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total operating income", {"FY2025": 929014, "FY2024": 483073, "FY2023": 498417, "FY2022": 466107, "FY2021": 449810}),
        ("Total operating expenses", {"FY2025": -911921, "FY2024": -425314, "FY2023": -397200, "FY2022": -380318, "FY2021": -347136}),
        ("Net (loss)/profit", {"FY2025": -44323, "FY2024": 46612, "FY2023": 85863, "FY2022": 80878, "FY2021": 89930}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 1781844, "FY2024": 1763502, "FY2023": 1707383, "FY2022": 1647297, "FY2021": 1565586}),
        ("Total comprehensive (loss)/income for the year", {"FY2025": -38961, "FY2024": 49619, "FY2023": 86246, "FY2022": 77734, "FY2021": 94638}),
        ("Other equity movements, net", {"FY2025": 1413739, "FY2024": -31277, "FY2023": -30127, "FY2022": -17648, "FY2021": -12927}),
        ("Closing equity", {"FY2025": 3156622, "FY2024": 1781844, "FY2023": 1763502, "FY2022": 1707383, "FY2021": 1647297}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[("Net cash (outflow)/inflow from operating activities", {"FY2025": -2827725, "FY2024": -4638153, "FY2023": -1165304, "FY2022": 5441607, "FY2021": 3898171}), ("Net cash from investing activities", {"FY2025": -1153173, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}), ("Net cash inflow/(outflow) from financing activities", {"FY2025": 1715050, "FY2024": -36915, "FY2023": -35017, "FY2022": -19285, "FY2021": -14281}), ("Cash and cash equivalents at end of year", {"FY2025": 2534127, "FY2024": 4455652, "FY2023": 9347772, "FY2022": 10594230, "FY2021": 5171908})], cash_flow_unit="£'000", ratios=[("CET1 Ratio", CET1R), ("Tier 1 Ratio", T1R), ("Total Capital Ratio", TCR), ("Leverage Ratio", {"FY2025": "4.51%", "FY2024": "4.09%", "FY2023": "4.27%", "FY2022": "4.12%", "FY2021": "3.51%"}), ("LCR", {"FY2025": "132%", "FY2024": "134%", "FY2023": "127%", "FY2022": "125%"}), ("NSFR", {"FY2025": "112%", "FY2024": "112%", "FY2023": "124%", "FY2022": "111%"})], note="Figures are duplicated from the detail sheets; see those sheets for source pages, basis notes, and disclosure gaps.")
bw.save("/Users/armaan/code/katalysis/banks/RBC EUROPE FINANCIALS.xlsx")
