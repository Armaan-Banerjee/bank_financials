import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019"]  # most recent first, all 12mo to 31 Dec

AR2025_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2025/annual/pdfs/hsbc-uk-bank-plc/260225-annual-report-and-accounts-2025.pdf"
AR2024_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2024/annual/pdfs/hsbc-uk-bank-plc/250219-annual-report-and-accounts-2024.pdf"
AR2023_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2023/annual/pdfs/hsbc-uk-bank-plc/240221-annual-report-and-accounts-2023.pdf"
AR2022_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2022/annual/pdfs/hsbc-uk-bank-plc/230221-annual-report-and-accounts-2022.pdf"
AR2021_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2021/annual/pdfs/hsbc-uk-bank-plc/220222-annual-report-and-accounts-2021.pdf"
AR2020_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2020/annual/pdfs/hsbc-uk-bank-plc/210223-annual-report-and-accounts-2020.pdf"
AR2019_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2019/annual/pdfs/hsbc-uk-bank-plc/200218-annual-report-and-accounts-2019.pdf"

P32025_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2025/annual/pdfs/hsbc-uk-bank-plc/260225-pillar-3-disclosures-at-31-december-2025.pdf"
P32024_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2024/annual/pdfs/hsbc-uk-bank-plc/250219-pillar-3-disclosures-at-31-december-2024.pdf"
P32023_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2023/annual/pdfs/hsbc-uk-bank-plc/240221-pillar-3-disclosures-at-31-december-2023.pdf"
P32022_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2022/annual/pdfs/hsbc-uk-bank-plc/230221-pillar-3-disclosures-at-31-december-2022.pdf"
P32021_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2021/annual/pdfs/hsbc-uk-bank-plc/220222-pillar-3-disclosures-at-31-december-2021.pdf"
# FY2020 and FY2019 Pillar 3 documents are no longer live on hsbc.com; sourced via Wayback Machine snapshots
# of the original hsbc.com URLs (same filename pattern as the live AR/Pillar 3 pairs above).
P32020_URL = "https://web.archive.org/web/20240527084156id_/https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2020/annual/pdfs/hsbc-uk-bank-plc/210223-pillar-3-disclosures-at-31-december-2020.pdf"
P32019_URL = "https://web.archive.org/web/20221014171921id_/https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2019/annual/pdfs/hsbc-uk-bank-plc/200218-pillar-3-disclosures-31-december-2019.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: HSBC UK Bank plc (Companies House 09928412, FRN 765112) is the ring-fenced retail/SME "
    "banking entity created in 2018 under UK ring-fencing reform - confirmed distinct from HSBC Bank plc "
    "(FRN 114216, the legacy non-ring-fenced entity, built separately in WF-012) and HSBC Innovation Bank "
    "Limited (FRN 543146, the former Silicon Valley Bank UK, also built in WF-012). All figures below are "
    "HSBC UK Bank plc's own entity-level Consolidated statements, sourced directly from HSBC UK Bank plc's "
    "own Annual Report and Accounts and Pillar 3 Disclosures on hsbc.com's investor-relations subsidiaries "
    "reporting archive.\n\n"
    "HISTORICAL FLOOR (HD-019, independently verified - not assumed from GLEIF entity-creation date): HSBC UK "
    "Bank plc's legal entity was incorporated 23 December 2015 as a dormant shelf company ('HSBC UK RFB "
    "Limited'), but it did not begin real banking operations until the UK ring-fencing transfer on 1 July "
    "2018 (confirmed directly against the entity's own Annual Report and Accounts 2017, which states the "
    "company 'made a pre-tax profit of £16,000... representing interest earned on UK treasury gilts' with "
    "'no relevant audit information' and total equity of £15.01m - i.e. a genuine shell, not a trading bank; "
    "and against the entity's own Annual Report and Accounts 2018, whose audited financial statements cover "
    "only the six months to 31 December 2018, since 'HSBC UK's banking operations commenced on 1 July "
    "2018'). This is the same UK ring-fencing gating event, under the same Financial Services (Banking "
    "Reform) Act 2013 regime, found for Barclays Bank UK PLC in HD-001. FY2018 itself is therefore NOT usable "
    "as a year column in this workbook: its own audited income statement, statement of comprehensive income, "
    "cash flow statement and equity roll-forward all cover only a 6-month stub period (1 July-31 December "
    "2018), not comparable to the full 12-month columns used everywhere else in this workbook. The floor used "
    "here is FY2019 - the entity's own first genuine full 12-month audited reporting year - confirmed directly "
    "against HSBC UK Bank plc's own Annual Report and Accounts 2019, whose Consolidated income statement is "
    "explicitly 'for the year ended 31 December 2019' with the note 'the period from 1 January 2019 to 31 "
    "December 2019'. FY2019 and FY2020 Pillar 3 Disclosures documents are no longer live on hsbc.com and were "
    "retrieved via Wayback Machine snapshots of their original hsbc.com URLs."
)

CASH_FLOW_NOTE = (
    "CASH FLOW NOTE: figures are £m. Presentation granularity changed across report vintages: FY2025/FY2024 "
    "and FY2023/FY2022 both itemise 'Purchase of property, plant and equipment' / 'Proceeds from sale of "
    "property, plant and equipment' as separate lines, while FY2021's own report combines them into a single "
    "'Net cash flows from the purchase and sale of property, plant and equipment' line; similarly FY2025/2024 "
    "itemise 'Purchase of intangible assets' / 'Proceeds from sale of intangible assets' separately, FY2023/"
    "2022 report only a net purchase line, and FY2021 combines both into 'Net investment in intangible "
    "assets'. FY2023/FY2022 include two SVB UK-acquisition-specific lines (HSBC UK Bank plc acquired Silicon "
    "Valley Bank UK in March 2023) not present in other years. FY2025 introduces two new financing lines "
    "('Issue of ordinary share capital and other equity instruments', 'Repayment of other equity instruments "
    "to non-controlling interests') not present in earlier years. FY2020's own report has no Subordinated "
    "loan capital issued/repaid line (nil that year) and no 'Issue of ordinary share capital' line (only "
    "issued in 2018, a one-off). FY2019's own report has a unique 'Funds received from the shareholder of the "
    "parent company' line (£nil in all other years shown here). Blank cells indicate that year's own report "
    "did not disclose that specific line; section totals (net cash from operating/investing/financing "
    "activities, cash and cash equivalents) are consistent and comparable across all 7 years."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are HSBC UK Bank plc's own Consolidated statement of cash flows, £m, from each "
    "year's own Annual Report and Accounts:\n"
    f"FY2025 & FY2024: HSBC UK Bank plc Annual Report and Accounts 2025, p.79 (Consolidated statement of cash flows) - {AR2025_URL}\n"
    f"FY2023 & FY2022: HSBC UK Bank plc Annual Report and Accounts 2023, p.81 (Consolidated statement of cash flows) - {AR2023_URL}\n"
    f"FY2021: HSBC UK Bank plc Annual Report and Accounts 2021, p.75 (Consolidated statement of cash flows) - {AR2021_URL}\n"
    f"FY2020: HSBC UK Bank plc Annual Report and Accounts 2020, p.83 (Consolidated statement of cash flows) - {AR2020_URL}\n"
    f"FY2019: HSBC UK Bank plc Annual Report and Accounts 2019, p.73 (Consolidated statement of cash flows) - {AR2019_URL}\n\n"
    + CASH_FLOW_NOTE + "\n\n" + ENTITY_NOTE
)


def p3_sources(page="5"):
    return (
        "Sources - HSBC UK Bank plc's own entity-level Pillar 3 Disclosures, Table 1 'Key metrics "
        "(KM1/IFRS9-FL)' (Table 1 titled 'Comparison of own funds, capital and leverage ratios...(IFRS9-FL)' "
        "for FY2019), each year's own originally-published figures at 31 December:\n"
        f"FY2025: HSBC UK Bank plc Pillar 3 Disclosures at 31 December 2025, p.5 - {P32025_URL}\n"
        f"FY2024: HSBC UK Bank plc Pillar 3 Disclosures at 31 December 2024, p.5 - {P32024_URL}\n"
        f"FY2023: HSBC UK Bank plc Pillar 3 Disclosures at 31 December 2023, p.5 - {P32023_URL}\n"
        f"FY2022: HSBC UK Bank plc Pillar 3 Disclosures at 31 December 2022, p.5 - {P32022_URL}\n"
        f"FY2021: HSBC UK Bank plc Pillar 3 Disclosures at 31 December 2021, p.4 - {P32021_URL}\n"
        f"FY2020: HSBC UK Bank plc Pillar 3 Disclosures at 31 December 2020, p.4 (Table 1: Key metrics "
        f"(KM1/IFRS9-FL)) - {P32020_URL} (retrieved via Wayback Machine, no longer live on hsbc.com)\n"
        f"FY2019: HSBC UK Bank plc Pillar 3 Disclosures at 31 December 2019, p.3 (Table 1: Comparison of own "
        f"funds, capital and leverage ratios, with and without the application of transitional arrangements "
        f"for IFRS 9 (IFRS9-FL)) - {P32019_URL} (retrieved via Wayback Machine, no longer live on hsbc.com)\n\n"
        + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="HSBC UK Bank plc", years=YEARS, header_color="DB0011")

STATEMENTS_ENTITY_NOTE = (
    "ENTITY NOTE: figures are HSBC UK Bank plc's own Consolidated statements (the ring-fenced retail/SME "
    "banking entity, distinct from HSBC Bank plc and HSBC Innovation Bank - see the entity note on the "
    "Cash Flow Statement sheet), £m, each year's own originally-published figures (not later restated "
    "comparatives). Sourced from each year's own Annual Report and Accounts:\n"
    f"FY2025 & FY2024: HSBC UK Bank plc Annual Report and Accounts 2025 - {AR2025_URL}\n"
    f"FY2023 & FY2022: HSBC UK Bank plc Annual Report and Accounts 2023 - {AR2023_URL}\n"
    f"FY2021: HSBC UK Bank plc Annual Report and Accounts 2021 - {AR2021_URL}\n"
    f"FY2020: HSBC UK Bank plc Annual Report and Accounts 2020 - {AR2020_URL}\n"
    f"FY2019: HSBC UK Bank plc Annual Report and Accounts 2019 - {AR2019_URL}\n\n"
    + ENTITY_NOTE
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 40369, "FY2024": 52276, "FY2023": 65719, "FY2022": 94407, "FY2021": 112478, "FY2020": 76429, "FY2019": 37030}),
    ("DATA", "Items in the course of collection from other banks", {"FY2023": 284, "FY2022": 353, "FY2021": 299, "FY2020": 253, "FY2019": 504}),
    ("DATA", "Financial assets mandatorily measured at fair value through profit or loss", {"FY2025": 175, "FY2024": 174, "FY2023": 135, "FY2022": 108, "FY2021": 79, "FY2020": 26, "FY2019": 66}),
    ("DATA", "Derivatives", {"FY2025": 167, "FY2024": 298, "FY2023": 178, "FY2022": 546, "FY2021": 64, "FY2020": 155, "FY2019": 121}),
    ("DATA", "Loans and advances to banks", {"FY2025": 6636, "FY2024": 7263, "FY2023": 7980, "FY2022": 6357, "FY2021": 1914, "FY2020": 1514, "FY2019": 1389}),
    ("DATA", "Loans and advances to customers", {"FY2025": 231223, "FY2024": 217604, "FY2023": 211887, "FY2022": 204143, "FY2021": 195526, "FY2020": 191233, "FY2019": 183056}),
    ("DATA", "Reverse repurchase agreements - non-trading", {"FY2025": 21560, "FY2024": 11776, "FY2023": 7686, "FY2022": 7406, "FY2021": 7988, "FY2020": 2485, "FY2019": 3014}),
    ("DATA", "Financial investments", {"FY2025": 41638, "FY2024": 37801, "FY2023": 26315, "FY2022": 16092, "FY2021": 14377, "FY2020": 19309, "FY2019": 19737}),
    ("DATA", "Prepayments, accrued income and other assets", {"FY2025": 9736, "FY2024": 9303, "FY2023": 8321, "FY2022": 8762, "FY2021": 9136, "FY2020": 9310, "FY2019": 8203}),
    ("DATA", "Current tax assets", {"FY2025": 3, "FY2020": 49}),
    ("DATA", "Interests in joint ventures", {"FY2025": 10, "FY2024": 9, "FY2023": 8, "FY2022": 9, "FY2021": 9, "FY2020": 8, "FY2019": 9}),
    ("DATA", "Goodwill and intangible assets", {"FY2025": 4413, "FY2024": 4373, "FY2023": 4363, "FY2022": 4258, "FY2021": 4193, "FY2020": 4093, "FY2019": 3973}),
    ("TOTAL", "Total assets", {"FY2025": 355930, "FY2024": 340877, "FY2023": 332876, "FY2022": 342441, "FY2021": 346063, "FY2020": 304864, "FY2019": 257102}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2025": 7709, "FY2024": 11144, "FY2023": 10843, "FY2022": 10721, "FY2021": 11180, "FY2020": 540, "FY2019": 529}),
    ("DATA", "Customer accounts", {"FY2025": 288756, "FY2024": 280366, "FY2023": 268345, "FY2022": 281095, "FY2021": 281870, "FY2020": 259341, "FY2019": 216214}),
    ("DATA", "Repurchase agreements - non-trading", {"FY2025": 6276, "FY2024": 420, "FY2023": 4652, "FY2022": 9333, "FY2021": 10438, "FY2020": 6150, "FY2019": 98}),
    ("DATA", "Items in the course of transmission to other banks", {"FY2023": 411, "FY2022": 308, "FY2021": 151, "FY2020": 132, "FY2019": 343}),
    ("DATA", "Derivatives", {"FY2025": 162, "FY2024": 107, "FY2023": 108, "FY2022": 304, "FY2021": 292, "FY2020": 365, "FY2019": 201}),
    ("DATA", "Debt securities in issue", {"FY2025": 3019, "FY2024": 2044, "FY2023": 1988, "FY2022": 1299, "FY2021": 900, "FY2020": 866, "FY2019": 3142}),
    ("DATA", "Accruals, deferred income and other liabilities", {"FY2025": 3524, "FY2024": 3476, "FY2023": 4124, "FY2022": 3543, "FY2021": 1674, "FY2020": 1941, "FY2019": 1834}),
    ("DATA", "Current tax liabilities", {"FY2025": 218, "FY2024": 449, "FY2023": 276, "FY2022": 173, "FY2021": 802, "FY2019": 409}),
    ("DATA", "Provisions", {"FY2025": 264, "FY2024": 265, "FY2023": 350, "FY2022": 424, "FY2021": 495, "FY2020": 979, "FY2019": 1325}),
    ("DATA", "Deferred tax liabilities", {"FY2025": 1318, "FY2024": 949, "FY2023": 1111, "FY2022": 666, "FY2021": 1969, "FY2020": 1677, "FY2019": 1223}),
    ("DATA", "Subordinated liabilities", {"FY2025": 16423, "FY2024": 15686, "FY2023": 14598, "FY2022": 12349, "FY2021": 12487, "FY2020": 10015, "FY2019": 9533}),
    ("TOTAL", "Total liabilities", {"FY2025": 327669, "FY2024": 314906, "FY2023": 306806, "FY2022": 320215, "FY2021": 322258, "FY2020": 282006, "FY2019": 234851}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {}),
    ("DATA", "Share premium account", {"FY2023": 9015, "FY2022": 9015, "FY2021": 9015, "FY2020": 9015, "FY2019": 9015}),
    ("DATA", "Other equity instruments", {"FY2025": 2691, "FY2024": 2196, "FY2023": 2196, "FY2022": 2196, "FY2021": 2196, "FY2020": 2196, "FY2019": 2196}),
    ("DATA", "Other reserves", {"FY2025": 2387, "FY2024": 1579, "FY2023": 7226, "FY2022": 6121, "FY2021": 7657, "FY2020": 7838, "FY2019": 7688}),
    ("DATA", "Retained earnings", {"FY2025": 23163, "FY2024": 22136, "FY2023": 7573, "FY2022": 4834, "FY2021": 4877, "FY2020": 3749, "FY2019": 3292}),
    ("TOTAL", "Total shareholders' equity", {"FY2025": 28241, "FY2024": 25911, "FY2023": 26010, "FY2022": 22166, "FY2021": 23745, "FY2020": 22798, "FY2019": 22191}),
    ("DATA", "Non-controlling interests", {"FY2025": 20, "FY2024": 60, "FY2023": 60, "FY2022": 60, "FY2021": 60, "FY2020": 60, "FY2019": 60}),
    ("TOTAL", "Total equity", {"FY2025": 28261, "FY2024": 25971, "FY2023": 26070, "FY2022": 22226, "FY2021": 23805, "FY2020": 22858, "FY2019": 22251}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 355930, "FY2024": 340877, "FY2023": 332876, "FY2022": 342441, "FY2021": 346063, "FY2020": 304864, "FY2019": 257102}),
]

bw.add_balance_sheet_sheet(
    title="HSBC UK Bank plc — Consolidated Balance Sheet",
    subtitle="HSBC UK Bank plc consolidated, £m. Called up share capital is nil/negligible throughout (rounds to £0m). See source note at bottom.",
    rows=bs_rows,
    sources_text=(
        "Sources - HSBC UK Bank plc's own Consolidated balance sheet, £m:\n"
        f"FY2025 & FY2024: Annual Report and Accounts 2025, p.78 - {AR2025_URL}\n"
        f"FY2023 & FY2022: Annual Report and Accounts 2023, p.80 - {AR2023_URL}\n"
        f"FY2021: Annual Report and Accounts 2021, p.75 - {AR2021_URL}\n"
        f"FY2020: Annual Report and Accounts 2020, p.82 - {AR2020_URL}\n"
        f"FY2019: Annual Report and Accounts 2019, p.72 - {AR2019_URL}\n\n"
        "Presentation note: 'Items in the course of collection from other banks' and 'Items in the course of "
        "transmission to other banks' appear as separate lines FY2023/FY2022/FY2021/FY2020/FY2019 - removed "
        "from the balance sheet's own presentation from FY2024 onward. 'Current tax assets' only appears "
        "FY2025 and FY2020 (nil in other years, per each year's own report). All Total rows reconcile exactly "
        "(Total assets = Total liabilities + Total equity for every year)."
        + "\n\n" + STATEMENTS_ENTITY_NOTE
    ),
    first_col_width=68,
    source_height=200,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 14860, "FY2024": 14789, "FY2023": 12915, "FY2022": 7592, "FY2021": 5072, "FY2020": 5197, "FY2019": 5696}),
    ("DATA", "Interest expense", {"FY2025": -6210, "FY2024": -6705, "FY2023": -5128, "FY2022": -1389, "FY2021": -422, "FY2020": -646, "FY2019": -944}),
    ("TOTAL", "Net interest income", {"FY2025": 8650, "FY2024": 8084, "FY2023": 7787, "FY2022": 6203, "FY2021": 4650, "FY2020": 4551, "FY2019": 4752}),
    ("DATA", "Fee income", {"FY2025": 1621, "FY2024": 1605, "FY2023": 1554, "FY2022": 1493, "FY2021": 1329, "FY2020": 1191, "FY2019": 1456}),
    ("DATA", "Fee expense", {"FY2025": -335, "FY2024": -297, "FY2023": -270, "FY2022": -248, "FY2021": -249, "FY2020": -175, "FY2019": -226}),
    ("TOTAL", "Net fee income", {"FY2025": 1286, "FY2024": 1308, "FY2023": 1284, "FY2022": 1245, "FY2021": 1080, "FY2020": 1016, "FY2019": 1230}),
    ("DATA", "Net income from financial instruments held for trading or managed on a fair value basis", {"FY2025": 430, "FY2024": 454, "FY2023": 414, "FY2022": 384, "FY2021": 318, "FY2020": 357, "FY2019": 400}),
    ("DATA", "Changes in fair value of other financial instruments mandatorily measured at FVTPL", {"FY2021": 15, "FY2020": -1, "FY2019": 2}),
    ("DATA", "Gains less losses from financial investments", {"FY2021": 101, "FY2020": 73, "FY2019": 48}),
    ("DATA", "Gain on acquisition of subsidiary (SVB UK)", {"FY2023": 1307}),
    ("DATA", "Other operating income", {"FY2025": 102, "FY2024": 133, "FY2023": 15, "FY2022": 120, "FY2021": 86, "FY2020": 35, "FY2019": 52}),
    ("TOTAL", "Net operating income before change in expected credit losses", {"FY2025": 10468, "FY2024": 9979, "FY2023": 10807, "FY2022": 7952, "FY2021": 6250, "FY2020": 6031, "FY2019": 6484}),
    ("DATA", "Change in expected credit losses and other credit impairment charges", {"FY2025": -539, "FY2024": -315, "FY2023": -421, "FY2022": -482, "FY2021": 989, "FY2020": -2115, "FY2019": -613}),
    ("TOTAL", "Net operating income", {"FY2025": 9929, "FY2024": 9664, "FY2023": 10386, "FY2022": 7470, "FY2021": 7239, "FY2020": 3916, "FY2019": 5871}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Employee compensation and benefits", {"FY2025": -1205, "FY2024": -1128, "FY2023": -1007, "FY2022": -1079, "FY2021": -1022, "FY2020": -985, "FY2019": -934}),
    ("DATA", "General and administrative expenses", {"FY2025": -2610, "FY2024": -2442, "FY2023": -2265, "FY2022": -2271, "FY2021": -2316, "FY2020": -2404, "FY2019": -3601}),
    ("DATA", "Depreciation and impairment of PP&E and right-of-use assets", {"FY2025": -105, "FY2024": -99, "FY2023": -116, "FY2022": -164, "FY2021": -174, "FY2020": -181, "FY2019": -170}),
    ("DATA", "Amortisation and impairment of intangible assets", {"FY2025": -390, "FY2024": -348, "FY2023": -319, "FY2022": -318, "FY2021": -247, "FY2020": -183, "FY2019": -156}),
    ("TOTAL", "Total operating expenses", {"FY2025": -4310, "FY2024": -4017, "FY2023": -3707, "FY2022": -3832, "FY2021": -3759, "FY2020": -3753, "FY2019": -4861}),
    ("TOTAL", "Profit before tax", {"FY2025": 5619, "FY2024": 5647, "FY2023": 6679, "FY2022": 3638, "FY2021": 3480, "FY2020": 163, "FY2019": 1010}),
    ("DATA", "Tax expense", {"FY2025": -1517, "FY2024": -1508, "FY2023": -1425, "FY2022": -762, "FY2021": -1112, "FY2020": -83, "FY2019": -494}),
    ("TOTAL", "Profit for the year", {"FY2025": 4102, "FY2024": 4139, "FY2023": 5254, "FY2022": 2876, "FY2021": 2368, "FY2020": 80, "FY2019": 516}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Debt instruments at fair value through OCI", {"FY2025": 73, "FY2024": -35, "FY2023": 66, "FY2022": -300, "FY2021": -89, "FY2020": 142, "FY2019": -4}),
    ("DATA", "Cash flow hedges", {"FY2025": 734, "FY2024": -365, "FY2023": 1031, "FY2022": -1234, "FY2021": -91, "FY2020": 13, "FY2019": 34}),
    ("DATA", "Remeasurement of defined benefit asset/liability", {"FY2025": -80, "FY2024": -285, "FY2023": -128, "FY2022": -1023, "FY2021": -510, "FY2020": 553, "FY2019": -207}),
    ("DATA", "Exchange differences", {"FY2025": 1, "FY2024": 1, "FY2023": 8, "FY2022": -2, "FY2021": -1, "FY2020": -5, "FY2019": 1}),
    ("TOTAL", "Other comprehensive income/(expense) for the year, net of tax", {"FY2025": 728, "FY2024": -684, "FY2023": 977, "FY2022": -2559, "FY2021": -691, "FY2020": 703, "FY2019": -176}),
    ("TOTAL", "Total comprehensive income for the year", {"FY2025": 4830, "FY2024": 3455, "FY2023": 6231, "FY2022": 317, "FY2021": 1677, "FY2020": 783, "FY2019": 340}),
]

bw.add_income_statement_sheet(
    title="HSBC UK Bank plc — Consolidated Income Statement & Statement of Comprehensive Income",
    subtitle="HSBC UK Bank plc consolidated, £m. See source note at bottom.",
    rows=pl_rows,
    sources_text=(
        "Sources - HSBC UK Bank plc's own Consolidated income statement / statement of comprehensive income, £m:\n"
        f"FY2025 & FY2024: Annual Report and Accounts 2025, p.76-77 - {AR2025_URL}\n"
        f"FY2023 & FY2022: Annual Report and Accounts 2023, p.78 - {AR2023_URL}\n"
        f"FY2021: Annual Report and Accounts 2021, p.73 - {AR2021_URL}\n"
        f"FY2020: Annual Report and Accounts 2020, p.80-81 - {AR2020_URL}\n"
        f"FY2019: Annual Report and Accounts 2019, p.70-71 - {AR2019_URL}\n\n"
        "Presentation note: FY2023's 'Gain on acquisition of subsidiary' (£1,307m, provisional gain on the "
        "acquisition of Silicon Valley Bank UK, March 2023) is unique to that year. FY2021's, FY2020's and "
        "FY2019's 'Changes in fair value of other financial instruments mandatorily measured at FVTPL' and "
        "'Gains less losses from financial investments' lines were folded into other income lines from FY2022 "
        "onward and don't appear as separate lines in later years. OCI detail is disclosed in-table for all 7 "
        "years; Total comprehensive income for the year is comparable across all years and ties exactly to "
        "Profit for the year + OCI total."
        + "\n\n" + STATEMENTS_ENTITY_NOTE
    ),
    first_col_width=80,
    source_height=210,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
EQ_HEADERS = ["Called up share capital and share premium", "Other equity instruments", "Retained earnings",
              "Financial assets at FVOCI reserve", "Cash flow hedging reserve", "Group reorganisation reserve",
              "Total shareholders' equity", "Non-controlling interests", "Total equity"]

eq_rows = [
    ("TOTAL", "At 1 Jan 2019 (FY2019's own opening)", (9015, 2196, 3405, 14, -46, 7689, 22273, 60, 22333)),
    ("DATA", "Profit for the year", (None, None, 512, None, None, None, 512, 4, 516)),
    ("DATA", "Other comprehensive income (net of tax)", (None, None, -207, -5, 34, 2, -176, None, -176)),
    ("DATA", "Total comprehensive income for the year", (None, None, 305, -5, 34, 2, 336, 4, 340)),
    ("DATA", "Dividends to shareholders", (None, None, -451, None, None, None, -451, -4, -455)),
    ("DATA", "Other movements (pension asset transfer, share-based payments)", (None, None, 33, None, None, None, 33, None, 33)),
    ("TOTAL", "At 31 Dec 2019 / 1 Jan 2020", (9015, 2196, 3292, 9, -12, 7691, 22191, 60, 22251)),
    ("DATA", "Profit for the year", (None, None, 76, None, None, None, 76, 4, 80)),
    ("DATA", "Other comprehensive income (net of tax)", (None, None, 553, 137, 13, None, 703, None, 703)),
    ("DATA", "Total comprehensive income for the year", (None, None, 629, 137, 13, None, 779, 4, 783)),
    ("DATA", "Dividends to shareholders", (None, None, -222, None, None, None, -222, -4, -226)),
    ("DATA", "Other movements (pension asset transfer, share-based payments)", (None, None, 50, None, None, None, 50, None, 50)),
    ("TOTAL", "At 1 Jan 2021 (FY2021's own opening)", (9015, 2196, 3749, 146, 1, 7691, 22798, 60, 22858)),
    ("DATA", "Profit for the year", (None, None, 2363, None, None, None, 2363, 5, 2368)),
    ("DATA", "Other comprehensive income (net of tax)", (None, None, -510, -90, -91, None, -691, None, -691)),
    ("DATA", "Total comprehensive income for the year", (None, None, 1853, -90, -91, None, 1672, 5, 1677)),
    ("DATA", "Dividends to shareholders", (None, None, -747, None, None, None, -747, -5, -752)),
    ("DATA", "Other movements (pension asset transfers, share-based payments)", (None, None, 22, None, None, None, 22, None, 22)),
    ("TOTAL", "At 31 Dec 2021 / 1 Jan 2022", (9015, 2196, 4877, 56, -90, 7691, 23745, 60, 23805)),
    ("DATA", "Profit for the year", (None, None, 2871, None, None, None, 2871, 5, 2876)),
    ("DATA", "Other comprehensive income (net of tax)", (None, None, -1023, -302, -1234, None, -2559, None, -2559)),
    ("DATA", "Total comprehensive income for the year", (None, None, 1848, -302, -1234, None, 312, 5, 317)),
    ("DATA", "Dividends to shareholders", (None, None, -1929, None, None, None, -1929, -5, -1934)),
    ("DATA", "Other movements (pension asset transfers, share-based payments)", (None, None, 38, None, None, None, 38, None, 38)),
    ("TOTAL", "At 31 Dec 2022 / 1 Jan 2023", (9015, 2196, 4834, -246, -1324, 7691, 22166, 60, 22226)),
    ("DATA", "Profit for the year", (None, None, 5249, None, None, None, 5249, 5, 5254)),
    ("DATA", "Other comprehensive income (net of tax)", (None, None, -128, 74, 1031, None, 977, None, 977)),
    ("DATA", "Total comprehensive income for the year", (None, None, 5121, 74, 1031, None, 6226, 5, 6231)),
    ("DATA", "Dividends to shareholders", (None, None, -2411, None, None, None, -2411, -5, -2416)),
    ("DATA", "Other movements (pension asset transfers, share-based payments)", (None, None, 29, None, None, None, 29, None, 29)),
    ("TOTAL", "At 31 Dec 2023 / 1 Jan 2024", (9015, 2196, 7573, -172, -293, 7691, 26010, 60, 26070)),
    ("DATA", "Profit for the year", (None, None, 4134, None, None, None, 4134, 5, 4139)),
    ("DATA", "Other comprehensive income (net of tax)", (None, None, -285, -34, -365, None, -684, None, -684)),
    ("DATA", "Total comprehensive income for the year", (None, None, 3849, -34, -365, None, 3450, 5, 3455)),
    ("DATA", "Dividends to shareholders", (None, None, -3564, None, None, None, -3564, -5, -3569)),
    ("DATA", "Share premium reclassification to retained earnings", (-9015, None, 9015, None, None, None, 0, None, 0)),
    ("DATA", "Capitalisation of Group reorganisation reserve through bonus share issuance", (5248, None, None, None, None, -5248, 0, None, 0)),
    ("DATA", "Cancellation of bonus shares", (-5248, None, 5248, None, None, None, 0, None, 0)),
    ("DATA", "Other movements (tax credit on share-based payments, pension asset transfers)", (None, None, 15, None, None, None, 15, None, 15)),
    ("TOTAL", "At 31 Dec 2024 / 1 Jan 2025", (0, 2196, 22136, -206, -658, 2443, 25911, 60, 25971)),
    ("DATA", "Profit for the year", (None, None, 4097, None, None, None, 4097, 5, 4102)),
    ("DATA", "Other comprehensive income (net of tax)", (None, None, -80, 74, 734, None, 728, None, 728)),
    ("DATA", "Total comprehensive income for the year", (None, None, 4017, 74, 734, None, 4825, 5, 4830)),
    ("DATA", "Issue of other equity instruments", (None, 495, None, None, None, None, 495, None, 495)),
    ("DATA", "Dividends to shareholders", (None, None, -3023, None, None, None, -3023, -5, -3028)),
    ("DATA", "Other movements (tax credit on share-based payments, repayment of other equity instruments to NCI)", (None, None, 33, None, None, None, 33, -40, -7)),
    ("TOTAL", "At 31 Dec 2025", (0, 2691, 23163, -132, 76, 2443, 28241, 20, 28261)),
]

bw.add_equity_changes_sheet(
    title="HSBC UK Bank plc — Consolidated Statement of Changes in Equity",
    subtitle=(
        "Chronological roll-forward, oldest to newest, £m. Equity reconciliation ladder confirmed: each year's "
        "own closing balance ties exactly to the next year's own opening balance and to that year's own Balance "
        "Sheet Total equity - zero plug rows needed anywhere across all 7 years. During Q4 2024, HSBC UK Bank "
        "plc converted £5.2bn of its Group reorganisation reserve and £9.0bn of its share premium account into "
        "retained earnings via a bonus share issuance and cancellation (Note 23) - a real, disclosed internal "
        "restructuring, not an error. See source note at bottom."
    ),
    headers=EQ_HEADERS,
    rows=eq_rows,
    sources_text=(
        "Sources - HSBC UK Bank plc's own Consolidated statement of changes in equity, £m:\n"
        f"FY2025 & FY2024: Annual Report and Accounts 2025, p.79 - {AR2025_URL}\n"
        f"FY2023 & FY2022: Annual Report and Accounts 2023, p.81 - {AR2023_URL}\n"
        f"FY2021: Annual Report and Accounts 2021, p.77 - {AR2021_URL}\n"
        f"FY2020 & FY2019: Annual Report and Accounts 2020, p.84 - {AR2020_URL}\n\n"
        "Presentation note (FY2019/FY2020 only): HSBC UK Bank plc's own equity statement for these two years "
        "carries an extra 'Foreign exchange reserve' column not present in the FY2021-2025 vintages (fully run "
        "down to nil by 31 December 2019 and not disclosed as a separate column thereafter). It is folded into "
        "the 'Group reorganisation reserve' column above rather than given its own column, to keep this sheet's "
        "column structure identical across all 7 years - this changes presentation only, not any total: "
        "FY2019's own opening Group reorganisation reserve balance of £7,691m plus the then-existing £(2)m "
        "Foreign exchange reserve balance is shown as £7,689m at 1 Jan 2019, and the +£2m FY2019 exchange-"
        "difference movement (reported in HSBC UK Bank plc's own Foreign exchange reserve column, distinct "
        "from the -£1m/-£5m exchange-difference amounts that are reported within the Financial assets at "
        "FVOCI reserve column in the original report and are left there unchanged) is folded into the same "
        "merged Group reorganisation reserve column, bringing it back to £7,691m at 31 Dec 2019 - which is "
        "exactly the Group reorganisation reserve balance already used, unchanged, for FY2020 and FY2021-2025."
        + "\n\n" + STATEMENTS_ENTITY_NOTE
    ),
    first_col_width=58,
    source_height=180,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax", {"FY2025": 5619, "FY2024": 5647, "FY2023": 6679, "FY2022": 3638, "FY2021": 3480, "FY2020": 163, "FY2019": 1010}),
    ("DATA", "Depreciation, amortisation and impairment", {"FY2025": 495, "FY2024": 447, "FY2023": 435, "FY2022": 482, "FY2021": 421, "FY2020": 364, "FY2019": 326}),
    ("DATA", "Net gain from investing activities", {"FY2025": -20, "FY2024": -38, "FY2023": 79, "FY2022": -37, "FY2021": -101, "FY2020": -73, "FY2019": -49}),
    ("DATA", "Provisional gain on acquisition of SVB UK", {"FY2023": -1307}),
    ("DATA", "Change in expected credit losses gross of recoveries and other credit impairment charges", {"FY2025": 616, "FY2024": 386, "FY2023": 472, "FY2022": 575, "FY2021": -911, "FY2020": 2180, "FY2019": 697}),
    ("DATA", "Provisions including pensions", {"FY2025": -181, "FY2024": -198, "FY2023": -233, "FY2022": -78, "FY2021": 123, "FY2020": 28, "FY2019": 1248}),
    ("DATA", "Share-based payment expense", {"FY2025": 30, "FY2024": 28, "FY2023": 19, "FY2022": 17, "FY2021": 16, "FY2020": 22, "FY2019": 17}),
    ("DATA", "Other non-cash items included in profit before tax", {"FY2025": -249, "FY2024": -249, "FY2023": -149, "FY2022": -204, "FY2021": -30}),
    ("DATA", "Elimination of exchange differences", {"FY2025": 143, "FY2024": 142, "FY2023": 332, "FY2022": 1032, "FY2021": -33, "FY2020": -85, "FY2019": 255}),
    ("SECTION", "Changes in operating assets and liabilities", {}),
    ("DATA", "Change in net trading securities and derivatives", {"FY2025": 1208, "FY2024": -626, "FY2023": 1615, "FY2022": -2174, "FY2021": -97, "FY2020": 133, "FY2019": -161}),
    ("DATA", "Change in loans and advances to banks and customers", {"FY2025": -14483, "FY2024": -5073, "FY2023": -2773, "FY2022": -9182, "FY2021": -3717, "FY2020": -10353, "FY2019": -8306}),
    ("DATA", "Change in reverse repurchase agreements - non-trading", {"FY2025": -4764, "FY2024": -1952, "FY2023": -264, "FY2022": 894, "FY2021": -5503, "FY2020": 529, "FY2019": 408}),
    ("DATA", "Change in financial assets mandatorily measured at fair value", {"FY2025": -1, "FY2024": -39, "FY2023": -27, "FY2022": -29, "FY2021": -53, "FY2020": 40, "FY2019": -31}),
    ("DATA", "Change in other assets", {"FY2025": -730, "FY2024": -748, "FY2023": 114, "FY2022": -2219, "FY2021": 728, "FY2020": -773, "FY2019": 511}),
    ("DATA", "Change in deposits by banks and customer accounts", {"FY2025": 4956, "FY2024": 12322, "FY2023": -20028, "FY2022": -1234, "FY2021": 33169, "FY2020": 43138, "FY2019": 10879}),
    ("DATA", "Change in repurchase agreements - non-trading", {"FY2025": 5856, "FY2024": -4231, "FY2023": -5086, "FY2022": -1104, "FY2021": 4288, "FY2020": 6052, "FY2019": -541}),
    ("DATA", "Change in debt securities in issue", {"FY2025": 975, "FY2024": 56, "FY2023": 689, "FY2022": 399, "FY2021": 34, "FY2020": -2276, "FY2019": 3142}),
    ("DATA", "Change in other liabilities", {"FY2025": -113, "FY2024": -900, "FY2023": 605, "FY2022": 1052, "FY2021": -1233, "FY2020": 93, "FY2019": -1621}),
    ("DATA", "Contributions paid to defined benefit plans", {"FY2025": 0, "FY2024": -1, "FY2023": -17, "FY2022": -21, "FY2021": -195, "FY2020": -202, "FY2019": -115}),
    ("DATA", "Tax paid", {"FY2025": -1632, "FY2024": -1209, "FY2023": -1182, "FY2022": -1499, "FY2021": 53, "FY2020": -404, "FY2019": -360}),
    ("TOTAL", "Net cash from operating activities", {"FY2025": -2275, "FY2024": 3764, "FY2023": -20027, "FY2022": -9692, "FY2021": 30439, "FY2020": 38576, "FY2019": 7309}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of financial investments", {"FY2025": -26063, "FY2024": -33396, "FY2023": -17640, "FY2022": -10386, "FY2021": -12468, "FY2020": -27644, "FY2019": -19300}),
    ("DATA", "Proceeds from the sale and maturity of financial investments", {"FY2025": 22519, "FY2024": 22617, "FY2023": 10222, "FY2022": 8571, "FY2021": 17000, "FY2020": 28848, "FY2019": 12629}),
    ("DATA", "Proceeds from sale of property, plant and equipment", {"FY2025": 0, "FY2024": 27, "FY2023": 67, "FY2022": 39}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -73, "FY2024": -71, "FY2023": -45, "FY2022": -80}),
    ("DATA", "Net cash flows from the purchase and sale of property, plant and equipment", {"FY2021": -53, "FY2020": -58, "FY2019": -69}),
    ("DATA", "Purchase of intangible assets", {"FY2025": -438, "FY2024": -363, "FY2023": -325, "FY2022": -382}),
    ("DATA", "Proceeds from sale of intangible assets", {"FY2025": 10, "FY2024": 1}),
    ("DATA", "Net investment in intangible assets", {"FY2021": -347, "FY2020": -303, "FY2019": -319}),
    ("DATA", "Net cash flow on acquisition of subsidiaries, businesses and joint venture", {"FY2025": 1, "FY2024": 0, "FY2019": 0}),
    ("DATA", "Net cash flow from acquisition of SVB UK", {"FY2023": 1023}),
    ("TOTAL", "Net cash from investing activities", {"FY2025": -4044, "FY2024": -11185, "FY2023": -6698, "FY2022": -2238, "FY2021": 4132, "FY2020": 843, "FY2019": -7059}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Issue of ordinary share capital and other equity instruments", {"FY2025": 495, "FY2024": 0, "FY2019": 0}),
    ("DATA", "Subordinated loan capital issued", {"FY2025": 3194, "FY2024": 3259, "FY2023": 2250, "FY2021": 4978, "FY2020": 0, "FY2019": 4619}),
    ("DATA", "Subordinated loan capital repaid", {"FY2025": -2414, "FY2024": -2194, "FY2021": -2079}),
    ("DATA", "Dividends paid to shareholders of the parent company and non-controlling interests", {"FY2025": -3028, "FY2024": -3569, "FY2023": -2416, "FY2022": -1934, "FY2021": -752, "FY2020": -226, "FY2019": -455}),
    ("DATA", "Repayment of other equity instruments to non-controlling interests", {"FY2025": -40, "FY2024": 0}),
    ("TOTAL", "Net cash from financing activities", {"FY2025": -1793, "FY2024": -2504, "FY2023": -166, "FY2022": -1934, "FY2021": 2147, "FY2020": -226, "FY2019": 4164}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": -8112, "FY2024": -9925, "FY2023": -26891, "FY2022": -13864, "FY2021": 36718, "FY2020": 39193, "FY2019": 4414}),
    ("DATA", "Cash and cash equivalents at 1 Jan", {"FY2025": 63366, "FY2024": 73381, "FY2023": 100319, "FY2022": 114134, "FY2021": 77422, "FY2020": 38086, "FY2019": 33817}),
    ("DATA", "Exchange differences in respect of cash and cash equivalents", {"FY2025": 45, "FY2024": -90, "FY2023": -47, "FY2022": 49, "FY2021": -6, "FY2020": 143, "FY2019": -145}),
    ("TOTAL", "Cash and cash equivalents at 31 Dec", {"FY2025": 55299, "FY2024": 63366, "FY2023": 73381, "FY2022": 100319, "FY2021": 114134, "FY2020": 77422, "FY2019": 38086}),
]

bw.add_cash_flow_sheet(
    title="HSBC UK Bank plc — Consolidated Cash Flow Statement",
    subtitle="HSBC UK Bank plc consolidated, £m. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=82,
    source_height=260,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
aq_rows = [
    ("SECTION", "Loans and advances to customers at amortised cost, by IFRS 9 stage", {}),
    ("DATA", "Stage 1 - gross carrying amount", {"FY2025": 210641, "FY2024": 180408, "FY2023": 167396, "FY2022": 154818, "FY2021": 174917, "FY2020": 162033, "FY2019": 168351}),
    ("DATA", "Stage 2 - gross carrying amount", {"FY2025": 18642, "FY2024": 35152, "FY2023": 42286, "FY2022": 46693, "FY2021": 18436, "FY2020": 28802, "FY2019": 13177}),
    ("DATA", "Stage 3 - gross carrying amount", {"FY2025": 3453, "FY2024": 3532, "FY2023": 3909, "FY2022": 4521, "FY2021": 4008, "FY2020": 3555, "FY2019": 3179}),
    ("DATA", "POCI - gross carrying amount", {"FY2023": 0, "FY2022": 23, "FY2021": 20, "FY2020": 36, "FY2019": 27}),
    ("TOTAL", "Total gross carrying amount", {"FY2025": 232736, "FY2024": 219092, "FY2023": 213591, "FY2022": 206055, "FY2021": 197381, "FY2020": 194426, "FY2019": 184734}),
    ("DATA", "Stage 1 - allowance for ECL", {"FY2025": -284, "FY2024": -275, "FY2023": -286, "FY2022": -248, "FY2021": -315, "FY2020": -467, "FY2019": -214}),
    ("DATA", "Stage 2 - allowance for ECL", {"FY2025": -477, "FY2024": -565, "FY2023": -755, "FY2022": -941, "FY2021": -692, "FY2020": -1651, "FY2019": -626}),
    ("DATA", "Stage 3 - allowance for ECL", {"FY2025": -752, "FY2024": -648, "FY2023": -663, "FY2022": -722, "FY2021": -843, "FY2020": -1053, "FY2019": -838}),
    ("DATA", "POCI - allowance for ECL", {"FY2023": 0, "FY2022": -1, "FY2021": -5, "FY2020": -22, "FY2019": 0}),
    ("TOTAL", "Total allowance for ECL", {"FY2025": -1513, "FY2024": -1488, "FY2023": -1704, "FY2022": -1912, "FY2021": -1855, "FY2020": -3193, "FY2019": -1678}),
    ("TOTAL", "Net loans and advances to customers", {"FY2025": 231223, "FY2024": 217604, "FY2023": 211887, "FY2022": 204143, "FY2021": 195526, "FY2020": 191233, "FY2019": 183056}),
    ("SECTION", "Derived ratios", {}),
    ("DATA", "Stage 3 as % of total gross carrying amount", {"FY2025": "1.5%", "FY2024": "1.6%", "FY2023": "1.8%", "FY2022": "2.2%", "FY2021": "2.0%", "FY2020": "1.8%", "FY2019": "1.7%"}),
    ("DATA", "ECL coverage - overall (total allowance / total gross)", {"FY2025": "0.7%", "FY2024": "0.7%", "FY2023": "0.8%", "FY2022": "0.9%", "FY2021": "0.9%", "FY2020": "1.6%", "FY2019": "0.9%"}),
    ("DATA", "ECL coverage - Stage 3 (Stage 3 allowance / Stage 3 gross)", {"FY2025": "21.8%", "FY2024": "18.3%", "FY2023": "17.0%", "FY2022": "16.0%", "FY2021": "21.0%", "FY2020": "29.6%", "FY2019": "26.4%"}),
]

bw.add_asset_quality_sheet(
    title="HSBC UK Bank plc — Asset Quality",
    subtitle="Loans and advances to customers at amortised cost, by IFRS 9 stage, £m. Net figures tie exactly to the Balance Sheet's own 'Loans and advances to customers' line every year. See source note at bottom.",
    rows=aq_rows,
    sources_text=(
        "Sources - HSBC UK Bank plc's own 'Summary of credit risk by stage distribution and ECL coverage by "
        "industry sector' table (Risk review section), £m:\n"
        f"FY2025: Annual Report and Accounts 2025, p.26 - {AR2025_URL}\n"
        f"FY2024: Annual Report and Accounts 2024, p.30 - {AR2024_URL}\n"
        f"FY2023: Annual Report and Accounts 2023, p.29 - {AR2023_URL}\n"
        f"FY2022: Annual Report and Accounts 2023, p.30 (FY2022 comparative column, no separate FY2022-vintage "
        f"report needed - same table format) - {AR2023_URL}\n"
        f"FY2021: Annual Report and Accounts 2021, p.32 - {AR2021_URL}\n"
        f"FY2020: Annual Report and Accounts 2020, p.34 - {AR2020_URL}\n"
        f"FY2019: Annual Report and Accounts 2019, p.28 (table titled 'Summary of credit risk (excluding debt "
        f"instruments measured at FVOCI) by stage distribution and ECL coverage by industry sector') - {AR2019_URL}\n\n"
        "ECL coverage % figures are the bank's own disclosed coverage percentages from this same table (not "
        "self-calculated); 'Stage 3 as % of total gross carrying amount' is the one ratio calculated here from "
        "the disclosed gross figures, as it is not itself a column in the source table. POCI (purchased or "
        "originated credit-impaired) appears as its own category FY2019-FY2022; nil/not applicable from "
        "FY2023 onward."
        + "\n\n" + STATEMENTS_ENTITY_NOTE
    ),
    first_col_width=64,
    source_height=200,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=48, source_height=170)


metric(
    "CET1 Capital", "£m",
    [("Common equity tier 1 (CET1) capital", {"FY2025": 15509, "FY2024": 15059, "FY2023": 14224, "FY2022": 12519, "FY2021": 12813, "FY2020": 12963, "FY2019": 11202})],
)

metric(
    "CET1 Ratio", "% of RWA",
    [("CET1 ratio", {"FY2025": "13.2%", "FY2024": "13.6%", "FY2023": "14.0%", "FY2022": "13.5%", "FY2021": "15.3%", "FY2020": "15.2%", "FY2019": "13.0%"})],
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 18218, "FY2024": 17307, "FY2023": 16479, "FY2022": 14771, "FY2021": 15067, "FY2020": 15197, "FY2019": 13453})],
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "15.5%", "FY2024": "15.7%", "FY2023": "16.2%", "FY2022": "16.0%", "FY2021": "18.0%", "FY2020": "17.8%", "FY2019": "15.7%"})],
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 21888, "FY2024": 20500, "FY2023": 19772, "FY2022": 17847, "FY2021": 18067, "FY2020": 18171, "FY2019": 16462})],
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "18.6%", "FY2024": "18.6%", "FY2023": "19.5%", "FY2022": "19.3%", "FY2021": "21.6%", "FY2020": "21.3%", "FY2019": "19.2%"})],
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted assets", {"FY2025": 117463, "FY2024": 110423, "FY2023": 101478, "FY2022": 92413, "FY2021": 83723, "FY2020": 85477, "FY2019": 85881})],
)

rwa_rows = [
    ("SECTION", "Credit risk (excluding counterparty credit risk)", {}),
    ("DATA", "Standardised approach", {"FY2025": 12796, "FY2024": 11067, "FY2023": 10918, "FY2022": 3990, "FY2021": 1715, "FY2020": 1461, "FY2019": 1376}),
    ("DATA", "Foundation IRB approach", {"FY2025": 45233, "FY2024": 45143, "FY2023": 40034, "FY2022": 41270, "FY2021": 41811, "FY2020": 43389, "FY2019": 5665}),
    ("DATA", "Slotting approach", {"FY2025": 6074, "FY2024": 5012, "FY2023": 5146, "FY2022": 5469}),
    ("DATA", "Advanced IRB approach", {"FY2025": 34602, "FY2024": 32297, "FY2023": 30680, "FY2022": 29361, "FY2021": 27904, "FY2020": 28437, "FY2019": 67179}),
    ("TOTAL", "Credit risk (excluding counterparty credit risk) - total", {"FY2025": 98705, "FY2024": 93519, "FY2023": 86778, "FY2022": 80090, "FY2021": 71430, "FY2020": 73287, "FY2019": 74220}),
    ("SECTION", "Other risk categories", {}),
    ("DATA", "Counterparty credit risk", {"FY2025": 255, "FY2024": 243, "FY2023": 236, "FY2022": 204, "FY2021": 129, "FY2020": 122, "FY2019": 198}),
    ("DATA", "Securitisation exposures in the non-trading book", {"FY2025": 1592, "FY2024": 899, "FY2023": 725, "FY2022": 650, "FY2021": 859, "FY2020": 904, "FY2019": 596}),
    ("DATA", "Position, foreign exchange and commodities risks (Market risk)", {"FY2025": 97, "FY2024": 173, "FY2023": 132, "FY2022": 101, "FY2021": 170, "FY2020": 156, "FY2019": 27}),
    ("DATA", "Operational risk", {"FY2025": 16814, "FY2024": 15589, "FY2023": 13607, "FY2022": 11368, "FY2021": 10607, "FY2020": 10509, "FY2019": 10303}),
    ("DATA", "Amounts below thresholds for deduction (FY2021 only: additive to Total; FY2022-FY2025: memo, already included within Credit risk above)", {"FY2025": 457, "FY2024": 574, "FY2023": 652, "FY2022": 724, "FY2021": 528, "FY2020": 499, "FY2019": 537}),
    ("TOTAL", "Total RWAs", {"FY2025": 117463, "FY2024": 110423, "FY2023": 101478, "FY2022": 92413, "FY2021": 83723, "FY2020": 85477, "FY2019": 85881}),
]

bw.add_rwa_breakdown_sheet(
    title="HSBC UK Bank plc — RWA Breakdown",
    subtitle="Pillar 3 UK OV1 template, £m. Ties exactly to the Total RWAs sheet for all 7 years. See source note at bottom.",
    rows=rwa_rows,
    sources_text=(
        "Sources - HSBC UK Bank plc's own entity-level Pillar 3 Disclosures, Table 'Overview of risk-weighted "
        "exposure amounts (OV1)' (Table 12 in the FY2019/FY2020 vintages):\n"
        f"FY2025 & FY2024: Pillar 3 Disclosures at 31 December 2025, p.15 - {P32025_URL}\n"
        f"FY2023: Pillar 3 Disclosures at 31 December 2023, p.17 - {P32023_URL}\n"
        f"FY2022: Pillar 3 Disclosures at 31 December 2022, p.16 - {P32022_URL}\n"
        f"FY2021: Pillar 3 Disclosures at 31 December 2021, p.15 - {P32021_URL}\n"
        f"FY2020: Pillar 3 Disclosures at 31 December 2020, p.16 (Table 12) - {P32020_URL} (retrieved via "
        f"Wayback Machine, no longer live on hsbc.com)\n"
        f"FY2019: Pillar 3 Disclosures at 31 December 2019, p.14 (Table 12) - {P32019_URL} (retrieved via "
        f"Wayback Machine, no longer live on hsbc.com)\n\n"
        "Template note: FY2021's, FY2020's and FY2019's OV1 tables use an older presentation (no separate "
        "'slotting approach' row - folded within foundation/advanced IRB, no separate SEC-ERBA row, includes a "
        "'Settlement risk' row showing nil throughout, and a 'Floor adjustment' row showing nil throughout, "
        "both omitted here since always zero) and, unlike FY2022-FY2025 where 'Amounts below thresholds for "
        "deduction' is a memo already embedded within Credit risk row 2, FY2021's/FY2020's/FY2019's own "
        "disclosures keep it as a genuinely separate, additive row before the Total - reproduced as disclosed "
        "in each year's own format rather than forced onto a single template. FY2019's own foundation-IRB/"
        "advanced-IRB split is markedly different from later years' (almost all on advanced IRB, £67,179m vs "
        "only £5,665m foundation IRB - the opposite emphasis to FY2021-2025) - reproduced exactly as "
        "originally disclosed, not a transcription error. All 7 years' category "
        "breakdowns sum exactly to that year's own disclosed Total RWAs figure, cross-checked before "
        "finalizing."
        + "\n\n" + ENTITY_NOTE
    ),
    first_col_width=76,
    source_height=230,
    unit_suffix=" (£m)",
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio", {"FY2025": "5.6%", "FY2024": "5.8%", "FY2023": "6.1%", "FY2022": "5.9%", "FY2021": "4.2%", "FY2020": "4.8%", "FY2019": "5.0%"})],
    note="A genuine basis change: FY2022-FY2025 are disclosed 'excluding claims on central banks' under the "
         "CRR II end-point basis (the new PRA disclosure template effective 1 January 2022), while FY2021's, "
         "FY2020's and FY2019's own reports pre-date that template and disclose a single leverage ratio "
         "(total exposure £358,237m/£317,196m/£268,271m respectively) that includes claims on central banks - "
         "a narrower/different exposure measure. FY2019-FY2021 are left on their own originally-disclosed "
         "basis rather than forced onto the newer definition.",
)

metric(
    "LCR", "%, 12-month average",
    [("Liquidity coverage ratio", {"FY2025": "175%", "FY2024": "190%", "FY2023": "201%", "FY2022": "226%"})],
    note="Not disclosed for FY2019-FY2021: HSBC UK Bank plc's own FY2019/FY2020/FY2021 Pillar 3 Disclosures "
         "pre-date the PRA's entity-level LCR quantitative-disclosure requirement (effective 1 January 2022, "
         "per the FY2022 Pillar 3 Disclosures' own footnote) - each of those years' own reports only describes "
         "the LCR qualitatively, with no numeric value given. Confirmed genuinely absent, not an access gap. "
         "Reported on a 12-month rolling average basis (this project's standard convention).",
)

metric(
    "NSFR", "%, average of preceding 4 quarters",
    [("Net stable funding ratio", {"FY2025": "146%", "FY2024": "154%", "FY2023": "158%", "FY2022": "164%"})],
    note="Not disclosed for FY2019-FY2021 - same reason as the LCR sheet (pre-dates the PRA's entity-level "
         "NSFR quantitative-disclosure requirement, effective 1 January 2022).",
)

# ---------------------------------------------------------------
# Additional interim Pillar 3 disclosures
# ---------------------------------------------------------------
# The standard metric sheets intentionally remain annual (one fixed column per
# year). HSBC UK publishes additional Q1/H1/Q3 disclosures, so these are kept
# in a separate wide matrix with periods across the columns.
INTERIM_PERIODS = [
    ("2025 Q3", "Q3", "2025-09-30"),
    ("2025 H1", "H1", "2025-06-30"),
    ("2025 Q1", "Q1", "2025-03-31"),
    ("2024 Q3", "Q3", "2024-09-30"),
    ("2024 H1", "H1", "2024-06-30"),
    ("2024 Q1", "Q1", "2024-03-31"),
    ("2023 Q3", "Q3", "2023-09-30"),
    ("2023 H1", "H1", "2023-06-30"),
    ("2023 Q1", "Q1", "2023-03-31"),
    ("2022 Q3", "Q3", "2022-09-30"),
    ("2022 H1", "H1", "2022-06-30"),
    ("2022 Q1", "Q1", "2022-03-31"),
    ("2021 H1", "H1", "2021-06-30"),
]

INTERIM_VALUES = {
    "CET1 Capital": [
        15626, 15255, 15211, 14966, 14550, 14611, 14818, 14382, 14317,
        12338, 12346, 12244, 13219,
    ],
    "Tier 1 Capital": [
        18334, 17963, 17423, 17220, 16802, 16864, 17072, 16632, 16567,
        14586, 14599, 14490, 15467,
    ],
    "Total Capital": [
        21978, 21632, 20598, 20375, 19990, 20053, 20140, 19671, 19625,
        17721, 17668, 17509, 18454,
    ],
    "Total RWAs": [
        117852, 115402, 112221, 105494, 104352, 102218, 100563, 99098, 99930,
        91917, 90209, 89803, 84555,
    ],
    "CET1 Ratio": [
        "13.3%", "13.2%", "13.6%", "14.2%", "13.9%", "14.3%", "14.7%", "14.5%", "14.3%",
        "13.4%", "13.7%", "13.6%", "15.6%",
    ],
    "Tier 1 Ratio": [
        "15.6%", "15.6%", "15.5%", "16.3%", "16.1%", "16.5%", "17.0%", "16.8%", "16.6%",
        "15.9%", "16.2%", "16.1%", "18.3%",
    ],
    "Total Capital Ratio": [
        "18.6%", "18.7%", "18.4%", "19.3%", "19.2%", "19.6%", "20.0%", "19.9%", "19.6%",
        "19.3%", "19.6%", "19.5%", "21.8%",
    ],
    "Leverage Ratio": [
        "5.7%", "5.7%", "5.8%", "5.8%", "5.9%", "6.1%", "6.4%", "6.3%", "6.3%",
        "5.6%", "5.8%", "5.8%", "4.6%",
    ],
    "LCR": [
        "181%", "186%", "189%", "192%", "193%", "196%", "206%", "213%", "220%",
        "232%", "232%", "230%", None,
    ],
    "NSFR": [
        "148%", "151%", "154%", "155%", "155%", "156%", "160%", "162%", "163%",
        "165%", "166%", "167%", None,
    ],
}

INTERIM_SOURCES = {
    "2025 Q3": ("HSBC UK Bank plc Pillar 3 Disclosures at 30 September 2025", "Table 1", "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2025/3q/pdfs/hsbc-uk-bank-plc-ring-fenced-bank/251106-hsbc-uk-bank-plc-pillar-3-disclosures-at-30-september-2025.pdf"),
    "2025 H1": ("HSBC UK Bank plc Pillar 3 Disclosures at 30 June 2025", "Table 1", "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2025/interim/pdfs/hsbc-uk-bank-plc/250806-pillar-3-disclosures-at-30-june-2025.pdf"),
    "2025 Q1": ("HSBC UK Bank plc Pillar 3 Disclosures at 31 March 2025", "Table 1", "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2025/1q/pdfs/hsbc-uk-bank-plc/250507-hbuk-pillar-3-disclosures-at-31-march-2025.pdf"),
    "2024 Q3": ("HSBC UK Bank plc Pillar 3 Disclosures at 30 September 2024", "p.3, Table 1", "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2024/3q/pdfs/hsbc-uk-bank-plc-ring-fenced-bank/241105-hsbc-uk-bank-plc-pillar-3-disclosures-at-30-september-2024.pdf"),
    "2024 H1": ("HSBC UK Bank plc Pillar 3 Disclosures at 30 June 2024", "p.4, Table 1", "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2024/interim/pdfs/hsbc-uk-bank-plc/240806-pillar-3-disclosures-at-30-june-2024.pdf"),
    "2024 Q1": ("HSBC UK Bank plc Pillar 3 Disclosures at 30 June 2024", "p.4, Table 1 comparative", "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2024/interim/pdfs/hsbc-uk-bank-plc/240806-pillar-3-disclosures-at-30-june-2024.pdf"),
    "2023 Q3": ("HSBC UK Bank plc Pillar 3 Disclosures at 30 September 2023", "p.3, Table 1", "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2023/3q/pdfs/hsbc-bank-plc/231106-hsbc-uk-bank-plc-pillar-3-disclosures-at-30-september-2023.pdf"),
    "2023 H1": ("HSBC UK Bank plc Pillar 3 Disclosures at 30 September 2023", "p.3, Table 1 comparative", "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2023/3q/pdfs/hsbc-bank-plc/231106-hsbc-uk-bank-plc-pillar-3-disclosures-at-30-september-2023.pdf"),
    "2023 Q1": ("HSBC UK Bank plc Pillar 3 Disclosures at 30 September 2023", "p.3, Table 1 comparative", "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2023/3q/pdfs/hsbc-bank-plc/231106-hsbc-uk-bank-plc-pillar-3-disclosures-at-30-september-2023.pdf"),
    "2022 Q3": ("HSBC UK Bank plc Pillar 3 Disclosures at 30 September 2022", "p.3, Table 1", "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2022/3q/pdfs/hsbc-uk-bank-plc/221102-pillar-3-disclosures-at-30-september-2022.pdf"),
    "2022 H1": ("HSBC UK Bank plc Pillar 3 Disclosures at 30 September 2022", "p.3, Table 1 comparative", "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2022/3q/pdfs/hsbc-uk-bank-plc/221102-pillar-3-disclosures-at-30-september-2022.pdf"),
    "2022 Q1": ("HSBC UK Bank plc Pillar 3 Disclosures at 30 September 2022", "p.3, Table 1 comparative", "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2022/3q/pdfs/hsbc-uk-bank-plc/221102-pillar-3-disclosures-at-30-september-2022.pdf"),
    "2021 H1": ("HSBC UK Bank plc Pillar 3 Disclosures at 30 September 2022", "p.3, Table 1 comparative", "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2022/3q/pdfs/hsbc-uk-bank-plc/221102-pillar-3-disclosures-at-30-september-2022.pdf"),
}

def add_interim_pillar3_sheet():
    interim_rows = []
    basis = "HSBC UK Bank plc consolidated entity-level"
    for metric_name, values in INTERIM_VALUES.items():
        unit = "%" if "Ratio" in metric_name or metric_name in {"Leverage Ratio", "LCR", "NSFR"} else "£m"
        for idx, (period, disclosure_type, as_of) in enumerate(INTERIM_PERIODS):
            document, page, url = INTERIM_SOURCES[period]
            interim_rows.append(
                (period, disclosure_type, metric_name, values[idx], unit, basis, url, page)
            )

    note = (
        "Scope note: 2022–2025 Q1/H1/Q3 observations are taken from HSBC UK Bank plc's own entity-level "
        "Pillar 3 Table 1 disclosures or their comparative columns. The only 2021 interim observation found "
        "was 30 June 2021; LCR and NSFR were not disclosed for that period. MREL was not disclosed in the "
        "entity-level reports. Blank values are source gaps, not calculated estimates. HSBC UK Bank plc is "
        "distinct from HSBC Bank plc and HSBC Group."
    )
    bw.add_wide_interim_sheet(
        "Interim Pillar 3",
        rows=interim_rows,
        hyperlink_cells={(i, 6): row[6] for i, row in enumerate(interim_rows)},
        title="HSBC UK Bank plc — Interim Pillar 3",
        subtitle="Additional entity-level Q1/H1/Q3 observations; annual values remain on the standard metric sheets.",
        note=note,
    )


bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={
        "MREL Ratio": "No MREL figure or mention appears anywhere in any of HSBC UK Bank plc's own Pillar 3 "
                      "Disclosures FY2019-FY2025 - HSBC UK Bank plc is not itself a resolution entity under "
                      "the Bank of England's Single Point of Entry resolution strategy for the HSBC group "
                      "(that role sits with HSBC Holdings plc at the top of the group), so no entity-level "
                      "MREL requirement or ratio applies here - the same pattern as HSBC Bank plc's "
                      "relationship to the wider group (see that workbook).",
    },
)

add_interim_pillar3_sheet()

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from operating activities", {"FY2025": -2275, "FY2024": 3764, "FY2023": -20027, "FY2022": -9692, "FY2021": 30439, "FY2020": 38576, "FY2019": 7309}),
        ("Net cash from investing activities", {"FY2025": -4044, "FY2024": -11185, "FY2023": -6698, "FY2022": -2238, "FY2021": 4132, "FY2020": 843, "FY2019": -7059}),
        ("Net cash from financing activities", {"FY2025": -1793, "FY2024": -2504, "FY2023": -166, "FY2022": -1934, "FY2021": 2147, "FY2020": -226, "FY2019": 4164}),
        ("Cash and cash equivalents at 31 Dec", {"FY2025": 55299, "FY2024": 63366, "FY2023": 73381, "FY2022": 100319, "FY2021": 114134, "FY2020": 77422, "FY2019": 38086}),
    ],
    cash_flow_unit="£m",
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 355930, "FY2024": 340877, "FY2023": 332876, "FY2022": 342441, "FY2021": 346063, "FY2020": 304864, "FY2019": 257102}),
        ("Loans and advances to customers", {"FY2025": 231223, "FY2024": 217604, "FY2023": 211887, "FY2022": 204143, "FY2021": 195526, "FY2020": 191233, "FY2019": 183056}),
        ("Total liabilities", {"FY2025": 327669, "FY2024": 314906, "FY2023": 306806, "FY2022": 320215, "FY2021": 322258, "FY2020": 282006, "FY2019": 234851}),
        ("Total equity", {"FY2025": 28261, "FY2024": 25971, "FY2023": 26070, "FY2022": 22226, "FY2021": 23805, "FY2020": 22858, "FY2019": 22251}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Net interest income", {"FY2025": 8650, "FY2024": 8084, "FY2023": 7787, "FY2022": 6203, "FY2021": 4650, "FY2020": 4551, "FY2019": 4752}),
        ("Total operating expenses", {"FY2025": -4310, "FY2024": -4017, "FY2023": -3707, "FY2022": -3832, "FY2021": -3759, "FY2020": -3753, "FY2019": -4861}),
        ("Profit for the year", {"FY2025": 4102, "FY2024": 4139, "FY2023": 5254, "FY2022": 2876, "FY2021": 2368, "FY2020": 80, "FY2019": 516}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Total comprehensive income for the year", {"FY2025": 4830, "FY2024": 3455, "FY2023": 6231, "FY2022": 317, "FY2021": 1677, "FY2020": 783, "FY2019": 340}),
        ("Dividends to shareholders", {"FY2025": -3028, "FY2024": -3569, "FY2023": -2416, "FY2022": -1934, "FY2021": -752, "FY2020": -226, "FY2019": -455}),
    ],
    equity_changes_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "13.2%", "FY2024": "13.6%", "FY2023": "14.0%", "FY2022": "13.5%", "FY2021": "15.3%", "FY2020": "15.2%", "FY2019": "13.0%"}),
        ("Tier 1 Ratio", {"FY2025": "15.5%", "FY2024": "15.7%", "FY2023": "16.2%", "FY2022": "16.0%", "FY2021": "18.0%", "FY2020": "17.8%", "FY2019": "15.7%"}),
        ("Total Capital Ratio", {"FY2025": "18.6%", "FY2024": "18.6%", "FY2023": "19.5%", "FY2022": "19.3%", "FY2021": "21.6%", "FY2020": "21.3%", "FY2019": "19.2%"}),
        ("Leverage Ratio", {"FY2025": "5.6%", "FY2024": "5.8%", "FY2023": "6.1%", "FY2022": "5.9%", "FY2021": "4.2%", "FY2020": "4.8%", "FY2019": "5.0%"}),
        ("LCR", {"FY2025": "175%", "FY2024": "190%", "FY2023": "201%", "FY2022": "226%"}),
        ("NSFR", {"FY2025": "146%", "FY2024": "154%", "FY2023": "158%", "FY2022": "164%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. MREL is not shown here (not disclosed at this "
         "entity level - see that sheet). The Leverage Ratio's FY2019/FY2020/FY2021 figures are on a "
         "different basis than FY2022-FY2025 - see the Leverage Ratio sheet's note. FY2019 was a period of "
         "unusually low profitability (Profit for the year £516m, then £80m in FY2020) driven by elevated "
         "expected credit loss charges and Covid-19-era provisioning, not a data error - see the Profit & "
         "Loss sheet.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/HSBC UK BANK PLC FINANCIALS.xlsx")
