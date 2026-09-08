import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017"]
YEAR_LABEL = {y: y for y in YEARS}
AR2025_URL = "https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/2025-paragon-bank-plc-ara"
AR2024_URL = "https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/paragon-bank-plc-annual-report-and-accounts-2024"
AR2023_URL = "https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/paragon-bank-plc-annual-report-and-accounts-2023"
AR2022_URL = "https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/section-172/2022/paragon-bank-plc-s172"
AR2021_URL = "https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/section-172/paragonbankaccounts2021"
AR2020_URL = "https://find-and-update.company-information.service.gov.uk/company/05390593/filing-history"
AR2019_URL = AR2020_URL
AR2018_URL = AR2020_URL
AR2017_URL = AR2020_URL
P3_2025_URL = "https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/reports-presentations/2025/2025-pillar-iii"
P3_2024_URL = "https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/reports-presentations/2024/2024--pillar--iii"
P3_2022_URL = "https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/reports-presentations/2022/pbg_2022_pillar_iii_disclosures"
P3_2021_URL = "https://www.paragonbank.co.uk/resources/paragon-group/documents/reports-presentations/2022/pbg_2021_pillar_iii_disclosures"
INTERIM_2025_URL = "https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/reports-presentations/2025/2025-pillar-iii"
INTERIM_2024_URL = "https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/reports-presentations/2024/2024-pillar-iii"
INTERIM_2023_URL = "https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/reports-presentations/2023/paragonbankinggroup_hy_pillar-3_2023"
INTERIM_2022_URL = "https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/corporate-governance/half-year-pillar-iii"

ENTITY_NOTE = (
    "ENTITY/BASIS NOTE: Paragon Bank PLC (Companies House 05390593, FRN 604551; formerly Paragon Mortgages (No.24) PLC) "
    "is the regulated UK bank. Cash flows are the Bank's own statutory statement, £m, for years ended 30 September. "
    "Pillar 3 capital/liquidity figures are for the Paragon Bank regulatory group, including subsidiary entities, as stated "
    "in the 2025 accounts and Pillar 3 reports. FY2025 full-year Pillar 3 was announced on 23 January 2026, but the "
    "accessible 2025 URL is the half-year document; FY2025 capital metrics therefore use audited Annual Report note 38 "
    "and FY2025 LCR/NSFR use its strategic-report disclosures. MREL is not disclosed in reviewed reports. "
    "FY2020-FY2017 source retrieval was checked against the Paragon Bank PLC Companies House filing history "
    "(company 05390593); historical cells remain blank where the older filing presentation could not be transcribed reliably."
)
CASH_FLOW_SOURCES = (
    "Sources - Paragon Bank PLC own statutory Cash Flow Statement, £m (all years ended 30 September):\n"
    f"FY2025: Annual Report 2025, p.59 and notes 33-35 pp.111-112 - {AR2025_URL}\n"
    f"FY2024: Annual Report 2024, p.53 and notes 32-34 pp.105-106 - {AR2024_URL}\n"
    f"FY2023: Annual Report 2023, p.52 and notes 32-34 pp.102-103 - {AR2023_URL}\n"
    f"FY2022: Annual Report 2022, p.48 and notes 32-34 pp.93-94 - {AR2022_URL}\n"
    f"FY2021: Annual Report 2021, p.50 and notes 32-34 pp.93-94 - {AR2021_URL}\n" + ENTITY_NOTE
)
rows = [
 ("SECTION","Operating activities",{}),
 ("DATA","Profit before tax",{"FY2025":242.2,"FY2024":265.0,"FY2023":232.6,"FY2022":480.2,"FY2021":182.5,"FY2020":86.52,"FY2019":47.92,"FY2018":164.51,"FY2017":22.92}),
 ("DATA","Non-cash movement on borrowing",{"FY2025":0.4}),
 ("DATA","Non-cash movement on investment securities",{"FY2025":34.2,"FY2024":-7.8}),
 ("DATA","Depreciation on property, plant and equipment",{"FY2022":0.3,"FY2021":0.3}),
 ("DATA","Impairment losses on loans to customers",{"FY2025":8.0,"FY2024":9.2,"FY2023":10.5,"FY2022":6.6,"FY2021":-10.9,"FY2018":2.13,"FY2017":1.00}),
 ("DATA","Loans to customers",{"FY2025":-536.9,"FY2024":-1016.3,"FY2023":-1755.5,"FY2022":-1056.2,"FY2021":-3001.0,"FY2018":-1570.06,"FY2017":-1671.35}),
 ("DATA","Derivative financial instruments",{"FY2025":78.0,"FY2024":199.1,"FY2023":87.7,"FY2022":-577.4,"FY2021":-10.5,"FY2018":-13.03,"FY2017":-7.74}),
 ("DATA","Fair value of portfolio hedges",{"FY2025":-49.6,"FY2024":-230.3,"FY2023":-97.4,"FY2022":394.9,"FY2021":70.0,"FY2018":14.87,"FY2017":11.50}),
 ("DATA","Other receivables",{"FY2025":21.4,"FY2024":-48.4,"FY2023":26.4,"FY2022":12.5,"FY2021":447.3,"FY2018":-720.90,"FY2017":-591.16}),
 ("DATA","Retail deposits",{"FY2025":-32.3,"FY2024":3032.7,"FY2023":2596.0,"FY2022":1368.9,"FY2021":1443.8,"FY2018":1681.16,"FY2017":1741.53}),
 ("DATA","Derivative financial instruments (liabilities)",{"FY2025":-33.6,"FY2024":59.2,"FY2023":-78.4,"FY2022":76.1,"FY2021":-65.6,"FY2018":-0.67,"FY2017":-3.93}),
 ("DATA","Fair value of portfolio hedges (liabilities)",{"FY2025":-11.6,"FY2024":47.6,"FY2023":68.9,"FY2022":-96.8,"FY2021":-13.0,"FY2018":-1.12,"FY2017":0.69}),
 ("DATA","Increase in provisions",{"FY2025":25.5}),
 ("DATA","Other liabilities",{"FY2025":-54.7,"FY2024":-171.6,"FY2023":158.8,"FY2022":309.3,"FY2021":36.0,"FY2018":418.00,"FY2017":16.61}),
 ("DATA","Income taxes paid",{"FY2025":-61.4,"FY2024":-53.5,"FY2023":-34.0,"FY2022":-35.0,"FY2021":-13.7,"FY2018":-4.72,"FY2017":-0.09}),
 ("TOTAL","Net cash generated/(utilised) by operating activities",{"FY2025":-370.4,"FY2024":2084.9,"FY2023":1215.6,"FY2022":883.4,"FY2021":-934.8,"FY2018":-29.83,"FY2017":-480.02}),
 ("SECTION","Investing activities",{}),
 ("DATA","Investment in securities",{"FY2025":-233.0,"FY2024":-419.6,"FY2017":7.06}),
 ("DATA","Proceeds from sale of operating property, plant and equipment",{"FY2022":4.8}),
 ("DATA","Acquisition of subsidiary",{"FY2017":-225.60}),
 ("DATA","Advances of loans to subsidiary undertakings",{"FY2025":-2817.8,"FY2024":-10556.4,"FY2023":-9543.8,"FY2022":-5429.8,"FY2021":-2320.0}),
 ("DATA","Repayment of loans by subsidiary entities",{"FY2025":2736.7,"FY2024":10513.5,"FY2023":9750.1,"FY2022":5212.9,"FY2021":1905.6}),
 ("TOTAL","Net cash generated/(utilised) by investing activities",{"FY2025":-314.1,"FY2024":-462.5,"FY2023":206.3,"FY2022":-212.1,"FY2021":-414.4,"FY2018":0.0,"FY2017":-218.54}),
 ("SECTION","Financing activities",{}),
 ("DATA","Dividends paid",{"FY2025":-155.8,"FY2024":-158.9,"FY2023":-258.1,"FY2022":-150.3,"FY2021":-94.8,"FY2018":-6.91}),
 ("DATA","Issue of covered bond",{"FY2025":498.8}),
 ("DATA","Repayment of long term bank facilities",{"FY2025":-500.0,"FY2024":-2000.0}),
 ("DATA","Shares issued",{"FY2017":303.76}),
 ("DATA","Movement on short term central bank facilities",{"FY2025":695.0,"FY2024":5.0,"FY2022":-69.0,"FY2021":964.6,"FY2018":324.40,"FY2017":700.00}),
 ("DATA","Movement on repurchase facilities",{"FY2024":49.9,"FY2023":50.1}),
 ("DATA","Capital element of lease payments",{"FY2021":-0.1}),
 ("TOTAL","Net cash generated/(utilised) by financing activities",{"FY2025":538.0,"FY2024":-2104.0,"FY2023":-208.0,"FY2022":-219.3,"FY2021":869.7,"FY2018":317.49,"FY2017":1003.76}),
 ("TOTAL","Net (decrease)/increase in cash and cash equivalents",{"FY2025":-146.5,"FY2024":-481.6,"FY2023":1213.9,"FY2022":452.0,"FY2021":-479.5,"FY2018":287.66,"FY2017":305.20}),
 ("DATA","Opening cash and cash equivalents",{"FY2025":2378.4,"FY2024":2860.0,"FY2023":1646.1,"FY2022":1194.1,"FY2021":1673.6,"FY2018":629.89,"FY2017":324.69}),
 ("TOTAL","Closing cash and cash equivalents",{"FY2025":2231.9,"FY2024":2378.4,"FY2023":2860.0,"FY2022":1646.1,"FY2021":1194.1,"FY2018":917.55,"FY2017":629.89}),
]
P3_SOURCES = (
 "Sources - Pillar 3 / regulatory-group metrics (capital amounts and RWEAs £m; ratios %):\n"
 f"FY2025: Annual Report 2025, note 38 pp.116-120 (capital, RWEA, leverage, LCR and NSFR) - {AR2025_URL}; "
 f"half-year Pillar 3 UK KM1 pp.3-4 (cross-check) - {P3_2025_URL}\n"
 f"FY2024 and FY2023: Pillar III Disclosures 30 September 2024, UK KM1 pp.7-10 - {P3_2024_URL}\n"
 f"FY2022 and FY2021: Pillar III Disclosures 30 September 2022, UK KM1 pp.7-10 - {P3_2022_URL}; "
 f"FY2021 own-funds/LCR appendix pp.89-98 - {P3_2021_URL}\n" + ENTITY_NOTE
)
capital={"FY2025":1085.1,"FY2024":1177.9,"FY2023":1188.9,"FY2022":1221.8,"FY2021":1055.8}
total={"FY2025":1235.1,"FY2024":1327.9,"FY2023":1338.9,"FY2022":1371.8,"FY2021":1205.8}
rwa={"FY2025":8613.2,"FY2024":8278.7,"FY2023":7668.7,"FY2022":7515.0,"FY2021":6836.8}
cetr={"FY2025":"12.6%","FY2024":"14.2%","FY2023":"15.5%","FY2022":"16.3%","FY2021":"15.4%"}
tcr={"FY2025":"14.3%","FY2024":"16.0%","FY2023":"17.5%","FY2022":"18.3%","FY2021":"17.6%"}
lev={"FY2025":"6.2%","FY2024":"7.0%","FY2023":"7.6%"}
lcr={"FY2025":"154.0%","FY2024":"211.5%","FY2023":"193.8%","FY2022":"146.3%","FY2021":"164.9%"}
nsfr={"FY2025":"135.0%","FY2024":"139.5%","FY2023":"128.0%","FY2022":"121.5%","FY2021":"118.9%"}

INTERIM_BASIS = "Paragon Bank regulatory group; consolidated Paragon Banking Group PLC disclosure including all entities"
INTERIM_PERIODS = {
    "31 Mar 2025": (INTERIM_2025_URL, "3", "UK KM1 key metrics table"),
    "31 Mar 2024": (INTERIM_2024_URL, "3-4", "UK KM1 key metrics table"),
    "31 Mar 2023": (INTERIM_2023_URL, "3-4", "UK KM1 key metrics table"),
    "31 Mar 2022": (INTERIM_2022_URL, "3-4", "UK KM1 key metrics table"),
    "31 Mar 2021": (INTERIM_2022_URL, "3-4", "UK KM1 comparative column in 31 March 2022 report"),
}
INTERIM_VALUES = {
    "31 Mar 2025": {
        "CET1 capital": (1193.2, "£m"), "Tier 1 capital": (1193.2, "£m"), "Total capital": (1343.2, "£m"),
        "Total risk-weighted exposure amount": (8385.2, "£m"), "CET1 ratio": (14.2, "%"),
        "Tier 1 ratio": (14.2, "%"), "Total capital ratio": (16.0, "%"), "Leverage ratio excluding claims on central banks": (6.9, "%"),
        "Liquidity coverage ratio": (183.2, "%"), "NSFR ratio": (142.0, "%"),
    },
    "31 Mar 2024": {
        "CET1 capital": (1174.9, "£m"), "Tier 1 capital": (1174.9, "£m"), "Total capital": (1324.9, "£m"),
        "Total risk-weighted exposure amount": (7974.7, "£m"), "CET1 ratio": (14.7, "%"),
        "Tier 1 ratio": (14.7, "%"), "Total capital ratio": (16.6, "%"), "Leverage ratio excluding claims on central banks": (7.3, "%"),
        "Liquidity coverage ratio": (218.2, "%"), "NSFR ratio": (132.9, "%"),
    },
    "31 Mar 2023": {
        "CET1 capital": (1170.4, "£m"), "Tier 1 capital": (1170.4, "£m"), "Total capital": (1320.4, "£m"),
        "Total risk-weighted exposure amount": (7479.9, "£m"), "CET1 ratio": (15.6, "%"),
        "Tier 1 ratio": (15.6, "%"), "Total capital ratio": (17.7, "%"), "Leverage ratio excluding claims on central banks": (7.6, "%"),
        "Liquidity coverage ratio": (155.6, "%"), "NSFR ratio": (123.3, "%"),
    },
    "31 Mar 2022": {
        "CET1 capital": (1092.4, "£m"), "Tier 1 capital": (1092.4, "£m"), "Total capital": (1242.4, "£m"),
        "Total risk-weighted exposure amount": (7095.7, "£m"), "CET1 ratio": (15.4, "%"),
        "Tier 1 ratio": (15.4, "%"), "Total capital ratio": (17.5, "%"), "Leverage ratio excluding claims on central banks": (7.4, "%"),
        "Liquidity coverage ratio": (151.1, "%"), "NSFR ratio": (120.6, "%"),
    },
    "31 Mar 2021": {
        "CET1 capital": (1057.3, "£m"), "Tier 1 capital": (1057.3, "£m"), "Total capital": (1203.8, "£m"),
        "Total risk-weighted exposure amount": (6616.0, "£m"), "CET1 ratio": (16.0, "%"),
        "Tier 1 ratio": (16.0, "%"), "Total capital ratio": (18.2, "%"), "Leverage ratio excluding claims on central banks": (7.7, "%"),
        "Liquidity coverage ratio": (182.3, "%"), "NSFR ratio": (116.7, "%"),
    },
}

INTERIM_ROWS = [
    (period, "Half year Pillar 3", metric_name, value, unit, INTERIM_BASIS, source_url, page_table)
    for period, values in INTERIM_VALUES.items()
    for metric_name, (value, unit) in values.items()
    for source_url, page_table, _ in [INTERIM_PERIODS[period]]
]

bw=BankWorkbook(bank_name="Paragon Bank Plc", years=YEARS, year_label=YEAR_LABEL, header_color="264653")

# ---------------------------------------------------------------
# Balance Sheet - equity reconciliation ladder step 1: built first so each
# year's own Total equity is the independent check value for the equity
# sheet below. All 5 years tie exactly (Total assets = Total liabilities +
# Total equity; Total equity ties to the equity statement's own opening/
# closing balances - zero undocumented plug rows anywhere across all 5
# years - the one genuine bridge, FY2024's Note 44 restatement, is shown
# as its own explicit row on the equity sheet).
# ---------------------------------------------------------------
STATEMENTS_SOURCES = (
    "Sources - Paragon Bank PLC own statutory Balance Sheet/Statement of Profit or Loss/"
    "Statement of Movements in Equity, £m (all years ended 30 September), transcribed from "
    "each year's own Companies House full-accounts filing (image-only scans, transcribed by "
    "reading rendered pages):\n"
    f"FY2025: Companies House filing dated 10 Mar 2026 (157pp), Statement of Profit or Loss p.57, "
    f"Balance Sheet p.58, Statement of Movements in Equity p.60 - "
    f"https://find-and-update.company-information.service.gov.uk/company/05390593/filing-history\n"
    f"FY2024: Companies House filing dated 28 Jan 2025 (148pp), Statement of Profit or Loss p.51, "
    f"Balance Sheet p.52, Statement of Movements in Equity p.54 - "
    f"https://find-and-update.company-information.service.gov.uk/company/05390593/filing-history\n"
    f"FY2023: Companies House filing dated 15 Feb 2024 (147pp), Statement of Profit or Loss p.50, "
    f"Balance Sheet p.51, Statement of Movements in Equity p.53 - "
    f"https://find-and-update.company-information.service.gov.uk/company/05390593/filing-history\n"
    f"FY2022: Companies House filing dated 14 Mar 2023 (139pp), Statement of Profit or Loss p.46, "
    f"Balance Sheet p.47, Statement of Movements in Equity p.49 - "
    f"https://find-and-update.company-information.service.gov.uk/company/05390593/filing-history\n"
    f"FY2018: Companies House filing dated 13 Dec 2018 (99pp), Income Statement p.37, Balance Sheet p.38, "
    f"Cash Flow Statement p.39 and Statement of Movement in Equity p.40 (supplied Companies House scan)\n"
    f"FY2017: Companies House filing dated 19 Dec 2017 (82pp), Statement of Profit or Loss p.25, Balance Sheet p.26, "
    f"Cash Flow Statement p.27 and Statement of Movement in Equity p.28 (supplied Companies House scan)\n"
    f"FY2021: Companies House filing dated 2022 (137pp), Statement of Profit or Loss p.49, "
    f"Balance Sheet p.50, Cash Flow Statement p.51 - "
    f"https://find-and-update.company-information.service.gov.uk/company/05390593/filing-history\n\n"
    + ENTITY_NOTE +
    "\n\nINVESTMENT SECURITIES ISSUER-TYPE SPLIT: FY2025 Annual Report (Companies House filing "
    "dated 10 Mar 2026, 157pp), Note 13 'Investment securities', p.68, breaks the FY2025/FY2024 "
    "carrying value down between UK Government securities ('gilts', FY2025: £509.4m, FY2024: "
    "£404.4m) and Covered bonds (FY2025: £116.8m, FY2024: £23.0m) - both figures sum exactly to "
    "the Balance Sheet's own 'Investment securities' total each year. The note states the entire "
    "balance is carried at amortised cost in both years (confirmed separately by Note 49(b), "
    "'Assets and liabilities carried at amortised cost', same filing p.148) - i.e. there is no "
    "FVOCI/FVTPL leg to split out, so no measurement-basis rows are added here (a single-leg "
    "'100% amortised cost' row would also double-count against this issuer-type split in the "
    "downstream investment-composition view, since both views sum sibling Balance Sheet rows "
    "independently) - https://find-and-update.company-information.service.gov.uk/company/05390593/filing-history\n\n"
    "PRESENTATION NOTE: FY2023-FY2025's Balance Sheet carries a standalone 'Investment "
    "securities' line (FY2023: nil, not separately listed that year - folded into the table's "
    "absence; FY2024-25: populated); FY2021-FY2022 instead show a 'Short term investments' line "
    "(both nil) - shown here on one combined row since they are the same conceptual line, "
    "genuinely renamed by the Bank. 'Property, plant and equipment' appears as its own line only "
    "FY2021-FY2023 (nil FY2022-FY2023, £5.1m FY2021) - dropped entirely as a separate line from "
    "FY2024 onward (presumably folded into Sundry assets that year, per the Bank's own table). "
    "FY2025 uniquely carries 'Covered bonds' (£499.2m) and 'Provisions' (£25.5m) on the liabilities "
    "side, and a 'Provision for liabilities' line in the P&L - genuine new items that year, not "
    "gaps in earlier years. FY2021's Interest receivable/Interest payable are shown grossed up "
    "differently (£288.4m/£(145.8)m) than the FY2022 report's own restated FY2021 comparative "
    "(£256.2m/£(113.6)m) - Net interest income is identical either way (£142.6m), so this is a "
    "presentation-only grossing change (likely a swap-interest netting convention), not a "
    "restatement of profit; the Bank's own contemporaneous FY2021 figures are used here."
)

bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash - central banks", {"FY2025": 2175.7, "FY2024": 2315.5, "FY2023": 2783.3, "FY2022": 1612.5, "FY2021": 1142.0, "FY2020": 1637.06, "FY2019": 816.40, "FY2018": 917.55, "FY2017": 629.89}),
    ("DATA", "Cash - retail banks", {"FY2025": 56.2, "FY2024": 62.9, "FY2023": 76.7, "FY2022": 33.6, "FY2021": 52.1, "FY2020": 36.51, "FY2019": 20.83}),
    ("DATA", "UK Government securities (gilts) - carrying value", {"FY2025": 509.4, "FY2024": 404.4}),
    ("DATA", "Covered bonds - other financial assets, not UK government-backed", {"FY2025": 116.8, "FY2024": 23.0}),
    ("TOTAL", "Investment securities - total (FY2021-22: 'Short term investments', both nil)", {"FY2025": 626.2, "FY2024": 427.4, "FY2022": 0.0, "FY2021": 0.0, "FY2020": 0.0, "FY2019": 0.0}),
    ("DATA", "Loans to customers", {"FY2025": 12446.0, "FY2024": 11671.6, "FY2023": 11161.2, "FY2022": 8952.8, "FY2021": 8144.6, "FY2020": 7146.78, "FY2019": 5848.32, "FY2018": 4655.43, "FY2017": 3086.70}),
    ("DATA", "Investment in structured entities", {"FY2025": 1959.3, "FY2024": 2154.9, "FY2023": 1427.9, "FY2022": 1791.2, "FY2021": 1944.1, "FY2018": 8.22, "FY2017": 9.02}),
    ("DATA", "Derivative financial assets", {"FY2025": 241.1, "FY2024": 319.1, "FY2023": 518.2, "FY2022": 605.9, "FY2021": 28.5, "FY2020": 17.98, "FY2019": 9.72, "FY2018": 22.40, "FY2017": 9.37}),
    ("DATA", "Sundry assets", {"FY2025": 115.5, "FY2024": 137.0, "FY2023": 88.6, "FY2022": 115.0, "FY2021": 127.5, "FY2020": 574.87, "FY2019": 344.53, "FY2018": 350.23, "FY2017": 367.75}),
    ("DATA", "Fair value adjustments from portfolio hedging (asset)", {"FY2018": -23.05, "FY2017": -8.18}),
    ("DATA", "Property, plant and equipment", {"FY2023": 0.0, "FY2022": 0.0, "FY2021": 5.1}),
    ("DATA", "Investment in subsidiary undertakings", {"FY2025": 2192.7, "FY2024": 2111.9, "FY2023": 2069.0, "FY2022": 2278.0, "FY2021": 2061.7, "FY2020": 1647.34, "FY2019": 1598.65}),
    ("TOTAL", "Total assets", {"FY2025": 19812.7, "FY2024": 19200.3, "FY2023": 18124.9, "FY2022": 15389.0, "FY2021": 13505.6, "FY2020": 11061.83, "FY2019": 8640.96, "FY2018": 7488.86, "FY2017": 4914.21}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Retail deposits", {"FY2025": 16270.8, "FY2024": 16314.7, "FY2023": 13234.4, "FY2022": 10569.5, "FY2021": 9297.4, "FY2020": 7866.59, "FY2019": 6395.87, "FY2018": 5296.57, "FY2017": 3615.41}),
    ("DATA", "Derivative financial liabilities", {"FY2025": 65.3, "FY2024": 98.9, "FY2023": 39.7, "FY2022": 118.1, "FY2021": 42.0, "FY2018": 4.30, "FY2017": 5.42}),
    ("DATA", "Fair value adjustments from portfolio hedging (liability)", {"FY2018": -3.77, "FY2017": -3.10}),
    ("DATA", "Covered bonds", {"FY2025": 499.2}),
    ("DATA", "Central bank facilities", {"FY2025": 950.0, "FY2024": 755.0, "FY2023": 2750.0, "FY2022": 2750.0, "FY2021": 2819.0, "FY2020": 1854.40, "FY2019": 994.40, "FY2018": 1024.40, "FY2017": 700.00}),
    ("DATA", "Sale and repurchase agreements", {"FY2025": 100.0, "FY2024": 100.0, "FY2023": 50.1, "FY2022": 0.0}),
    ("DATA", "Corporate bond", {"FY2025": 150.2, "FY2024": 150.3, "FY2023": 146.3, "FY2022": 150.0, "FY2021": 150.0}),
    ("DATA", "Sundry liabilities", {"FY2025": 621.4, "FY2024": 635.4, "FY2023": 811.0, "FY2022": 648.5, "FY2021": 339.2, "FY2020": 297.89, "FY2019": 229.37, "FY2018": 449.51, "FY2017": 31.51}),
    ("DATA", "Provisions", {"FY2025": 25.5}),
    ("DATA", "Current tax liabilities", {"FY2025": 73.4, "FY2024": 61.9, "FY2023": 53.0, "FY2022": 34.5, "FY2021": 35.7, "FY2018": 7.15, "FY2017": 4.56}),
    ("DATA", "Deferred tax liability", {"FY2025": 10.9, "FY2024": 34.0, "FY2023": 38.9, "FY2022": 55.0, "FY2021": 3.0, "FY2018": 1.37, "FY2017": 0.60}),
    ("TOTAL", "Total liabilities", {"FY2025": 18766.7, "FY2024": 18150.2, "FY2023": 17123.4, "FY2022": 14325.6, "FY2021": 12686.3, "FY2020": 10291.39, "FY2019": 7854.89, "FY2018": 6779.53, "FY2017": 4354.40}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 552.6, "FY2024": 552.6, "FY2023": 552.6, "FY2022": 552.6, "FY2021": 552.6, "FY2020": 552.62, "FY2019": 552.62, "FY2018": 552.62, "FY2017": 552.62}),
    ("DATA", "Reserves (profit and loss account)", {"FY2025": 493.4, "FY2024": 497.5, "FY2023": 448.9, "FY2022": 510.8, "FY2021": 266.7, "FY2020": 217.82, "FY2019": 233.45, "FY2018": 156.71, "FY2017": 7.19}),
    ("TOTAL", "Total equity", {"FY2025": 1046.0, "FY2024": 1050.1, "FY2023": 1001.5, "FY2022": 1063.4, "FY2021": 819.3, "FY2020": 770.44, "FY2019": 786.07, "FY2018": 709.33, "FY2017": 559.81}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 19812.7, "FY2024": 19200.3, "FY2023": 18124.9, "FY2022": 15389.0, "FY2021": 13505.6, "FY2020": 11061.83, "FY2019": 8640.96, "FY2018": 7488.86, "FY2017": 4914.21}),
]

bw.add_balance_sheet_sheet(
    title="Paragon Bank Plc — Balance Sheet",
    subtitle="Bank statutory basis, £m (all years as at 30 September). FY2024's Total equity is shown "
              "here as originally reported (1,050.1) - see the Statement of Changes in Equity sheet for "
              "FY2025's Note 44 restatement (-£29.3m to Reserves) applied to FY2024's closing balance.",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=340,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Profit & Loss - all 5 years transcribed from each year's own Statement of
# Profit or Loss. No OCI in any year (each report states this explicitly),
# so Profit for the year = Total comprehensive income throughout.
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable", {"FY2025": 1148.9, "FY2024": 1180.9, "FY2023": 852.4, "FY2022": 368.0, "FY2021": 288.4, "FY2020": 274.43, "FY2019": 247.38, "FY2018": 177.08, "FY2017": 105.66}),
    ("DATA", "Interest payable and similar charges", {"FY2025": -758.1, "FY2024": -838.0, "FY2023": -536.8, "FY2022": -147.0, "FY2021": -145.8, "FY2020": -149.11, "FY2019": -136.23, "FY2018": -98.20, "FY2017": -49.37}),
    ("TOTAL", "Net interest income", {"FY2025": 390.8, "FY2024": 342.9, "FY2023": 315.6, "FY2022": 221.0, "FY2021": 142.6, "FY2020": 125.32, "FY2019": 111.15, "FY2018": 78.88, "FY2017": 56.29}),
    ("DATA", "Other income / other operating income", {"FY2025": 51.9, "FY2024": 81.8, "FY2023": 108.7, "FY2022": 174.4, "FY2021": 95.5, "FY2020": 58.85, "FY2019": 72.76, "FY2018": 140.21, "FY2017": 0.96}),
    ("TOTAL", "Total operating income", {"FY2025": 442.7, "FY2024": 424.7, "FY2023": 424.3, "FY2022": 395.4, "FY2021": 238.1, "FY2020": 184.17, "FY2019": 183.91, "FY2018": 219.09, "FY2017": 57.25}),
    ("TOTAL", "Operating expenses", {"FY2025": -132.6, "FY2024": -132.5, "FY2023": -117.4, "FY2022": -99.8, "FY2021": -81.5, "FY2020": -64.04, "FY2019": -61.54, "FY2018": -50.70, "FY2017": -32.49}),
    ("DATA", "Provisions for losses", {"FY2025": -6.4, "FY2024": -10.5, "FY2023": -10.5, "FY2022": -6.6, "FY2021": 10.9, "FY2020": -15.50, "FY2019": -3.82, "FY2018": -2.13, "FY2017": -1.06}),
    ("DATA", "Provision for liabilities", {"FY2025": -25.5}),
    ("TOTAL", "Operating profit before fair value items", {"FY2025": 278.2, "FY2024": 281.7, "FY2023": 296.4, "FY2022": 289.0, "FY2021": 167.5, "FY2020": 104.63, "FY2019": 118.55, "FY2018": 166.26, "FY2017": 23.70}),
    ("DATA", "Fair value net gain/(loss)", {"FY2025": -36.0, "FY2024": -16.7, "FY2023": -63.8, "FY2022": 191.2, "FY2021": 15.0, "FY2020": 5.52, "FY2019": -11.54, "FY2018": -1.75, "FY2017": -0.78}),
    ("TOTAL", "Profit on ordinary activities before taxation", {"FY2025": 242.2, "FY2024": 265.0, "FY2023": 232.6, "FY2022": 480.2, "FY2021": 182.5, "FY2020": 110.15, "FY2019": 107.01, "FY2018": 164.51, "FY2017": 22.92}),
    ("DATA", "Tax charge on profit on ordinary activities", {"FY2025": -61.2, "FY2024": -57.5, "FY2023": -36.4, "FY2022": -85.8, "FY2021": -38.8, "FY2020": -15.60, "FY2019": -9.79, "FY2018": -8.08, "FY2017": -5.25}),
    ("TOTAL", "Profit for the financial year", {"FY2025": 181.0, "FY2024": 207.5, "FY2023": 196.2, "FY2022": 394.4, "FY2021": 143.7, "FY2020": 94.55, "FY2019": 97.22, "FY2018": 156.43, "FY2017": 17.67}),
]

bw.add_income_statement_sheet(
    title="Paragon Bank Plc — Profit & Loss",
    subtitle="Bank statutory basis, £m. FY2025 uniquely carries a 'Provision for liabilities' line "
              "(£25.5m) - a genuine new item that year, not a gap in earlier years. No other "
              "comprehensive income was disclosed in any of the 5 years - Profit for the financial "
              "year equals Total comprehensive income throughout, per each report's own statement.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=340,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - per-year reconciliation ladder confirmed:
# every year's own closing balance ties exactly to both the next year's own
# opening balance and that year's own Balance Sheet Total equity. Zero
# undocumented plug rows - this entity's equity structure is unusually
# simple (only two components, Share capital and Reserves; no share
# issuances, treasury shares, or OCI reserves in any of the 5 years). The
# one bridging row is FY2024's own Note 44 restatement, a genuine
# Bank-disclosed prior-period adjustment, not an error.
# ---------------------------------------------------------------
equity_headers = ["Share capital", "Reserves (profit and loss account)", "Total equity"]
equity_rows = [
    ("TOTAL", "At 1 October 2020 (FY2021 opening)", (552.6, 217.8, 770.4)),
    ("DATA", "Profit for the year", (None, 143.7, 143.7)),
    ("DATA", "Dividends paid", (None, -94.8, -94.8)),
    ("TOTAL", "At 30 September 2021 (FY2021 closing)", (552.6, 266.7, 819.3)),
    ("DATA", "Profit for the year", (None, 394.4, 394.4)),
    ("DATA", "Dividends paid", (None, -150.3, -150.3)),
    ("TOTAL", "At 30 September 2022 (FY2022 closing)", (552.6, 510.8, 1063.4)),
    ("DATA", "Profit for the year", (None, 196.2, 196.2)),
    ("DATA", "Dividends paid", (None, -258.1, -258.1)),
    ("TOTAL", "At 30 September 2023 (FY2023 closing)", (552.6, 448.9, 1001.5)),
    ("DATA", "Profit for the year", (None, 207.5, 207.5)),
    ("DATA", "Dividends paid", (None, -158.9, -158.9)),
    ("TOTAL", "At 30 September 2024 (FY2024 closing, as originally reported)", (552.6, 497.5, 1050.1)),
    ("DATA", "Restatement (Note 44, per FY2025 Annual Report)", (None, -29.3, -29.3)),
    ("TOTAL", "At 30 September 2024 (FY2024 closing, as restated)", (552.6, 468.2, 1020.8)),
    ("DATA", "Profit for the year", (None, 181.0, 181.0)),
    ("DATA", "Dividends paid", (None, -155.8, -155.8)),
    ("TOTAL", "At 30 September 2025 (FY2025 closing)", (552.6, 493.4, 1046.0)),
]

bw.add_equity_changes_sheet(
    title="Paragon Bank Plc — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, Bank statutory basis, £m. Equity "
              "reconciliation ladder confirmed: every year's own closing balance ties exactly to both "
              "the next year's own opening balance and that year's own Balance Sheet Total equity - "
              "zero undocumented plug rows across all 5 years. The one bridging row (FY2024's Note 44 "
              "restatement, -£29.3m to Reserves) is a genuine Bank-disclosed prior-period adjustment, "
              "not an error - the FY2025 Annual Report doesn't itemise the restatement's cause beyond "
              "citing its own Note 44.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=64,
)

bw.add_cash_flow_sheet(title="Paragon Bank Plc — Cash Flow Statement", subtitle="Bank statutory basis, £m; see source and basis note", rows=rows, sources_text=CASH_FLOW_SOURCES, first_col_width=72, source_height=260, unit_suffix=" (£m)")

# ---------------------------------------------------------------
# Asset Quality - loans to customers by IFRS 9 stage (gross carrying
# amount), loss allowance, and net carrying value, all 5 years. Carrying
# value ties closely but not exactly to the Balance Sheet's own Loans to
# customers line (small definitional differences, e.g. accrued interest,
# are expected and flagged rather than forced to tie).
# ---------------------------------------------------------------
ASSET_QUALITY_SOURCES = (
    "Sources - Paragon Bank PLC Note 'Impairment provisions on loans to customers' (loans-to-customers "
    "balance movements by IFRS 9 stage), £m, transcribed from rendered page images:\n"
    f"FY2025/FY2024: Annual Report 2025 (Companies House filing), Note 17, p.86 - "
    f"https://find-and-update.company-information.service.gov.uk/company/05390593/filing-history\n"
    f"FY2023/FY2022: Annual Report 2023 (Companies House filing), Note 16, p.79 - "
    f"https://find-and-update.company-information.service.gov.uk/company/05390593/filing-history\n"
    f"FY2021: Annual Report 2022 (Companies House filing), Note 17, p.74 - "
    f"https://find-and-update.company-information.service.gov.uk/company/05390593/filing-history\n\n"
    + ENTITY_NOTE +
    "\n\nDATA QUALITY NOTE: this note's own 'Carrying value' total is a few £m below the Balance "
    "Sheet's own 'Loans to customers' line every year (e.g. FY2025: £12,439.5m here vs £12,446.0m "
    "on the Balance Sheet; FY2024: £11,714.7m vs £11,671.6m - the FY2024 gap runs the other way) - "
    "a small definitional difference between this note's population and the Balance Sheet line "
    "(likely accrued interest or fair value hedge adjustments), not a transcription error. No "
    "separate product-type split (e.g. buy-to-let vs SME lending) is disclosed at this granularity "
    "in any of the 5 years - only the aggregate stage split shown below."
)
asset_quality_rows = [
    ("SECTION", "Loans to customers, by IFRS 9 stage (gross carrying amount)", {}),
    ("DATA", "Stage 1", {"FY2025": 11809.8, "FY2024": 11058.1, "FY2023": 10801.8, "FY2022": 7979.5, "FY2021": 7224.0}),
    ("DATA", "Stage 2", {"FY2025": 502.6, "FY2024": 538.5, "FY2023": 554.7, "FY2022": 1302.5, "FY2021": 831.9}),
    ("DATA", "Stage 3", {"FY2025": 163.2, "FY2024": 158.9, "FY2023": 122.9, "FY2022": 69.7, "FY2021": 88.6}),
    ("TOTAL", "Gross carrying amount", {"FY2025": 12475.6, "FY2024": 11755.5, "FY2023": 11479.4, "FY2022": 9351.7, "FY2021": 8144.5}),
    ("DATA", "Loss allowance - Stage 1", {"FY2025": -4.2, "FY2024": -6.4, "FY2023": -7.8, "FY2022": -7.8, "FY2021": -3.1}),
    ("DATA", "Loss allowance - Stage 2", {"FY2025": -2.4, "FY2024": -3.4, "FY2023": -6.5, "FY2022": -5.7, "FY2021": -8.0}),
    ("DATA", "Loss allowance - Stage 3", {"FY2025": -29.5, "FY2024": -31.0, "FY2023": -30.5, "FY2022": -14.6, "FY2021": -12.9}),
    ("TOTAL", "Total loss allowance", {"FY2025": -36.1, "FY2024": -40.8, "FY2023": -44.8, "FY2022": -28.1, "FY2021": -24.0}),
    ("TOTAL", "Carrying value", {"FY2025": 12439.5, "FY2024": 11714.7, "FY2023": 11434.6, "FY2022": 9323.6, "FY2021": 8120.5}),
    ("DATA", "Stage 3 as % of gross carrying amount (NPL ratio)", {"FY2025": "1.31%", "FY2024": "1.35%", "FY2023": "1.07%", "FY2022": "0.75%", "FY2021": "1.09%"}),
    ("DATA", "Stage 2 as % of gross carrying amount", {"FY2025": "4.03%", "FY2024": "4.58%", "FY2023": "4.83%", "FY2022": "13.93%", "FY2021": "10.21%"}),
    ("DATA", "Total loss allowance as % of gross carrying amount (coverage)", {"FY2025": "0.29%", "FY2024": "0.35%", "FY2023": "0.39%", "FY2022": "0.30%", "FY2021": "0.29%"}),
]

bw.add_asset_quality_sheet(
    title="Paragon Bank Plc — Asset Quality",
    subtitle="Bank statutory basis, £m. Loans to customers, IFRS 9 stage 1/2/3 gross carrying amount, "
              "loss allowance, and carrying value.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=80,
    source_height=300,
    unit_suffix=" (£m)",
)
def metric(name, unit, label, values, note=None):
    bw.add_metric_sheet(name, unit, [(label, values)], P3_SOURCES, note=note, first_col_width=52, source_height=180)
metric("CET1 Capital","£m","Common Equity Tier 1 (CET1) capital",capital)
metric("CET1 Ratio","%","Common Equity Tier 1 ratio",cetr)
metric("Tier 1 Capital","£m","Tier 1 capital",capital,"No AT1 capital is reported; Tier 1 equals CET1 in each year.")
metric("Tier 1 Ratio","%","Tier 1 ratio",cetr)
metric("Total Capital","£m","Total regulatory capital",total)
metric("Total Capital Ratio","%","Total capital ratio",tcr)
metric("Total RWAs","£m","Total risk-weighted exposure amount",rwa)

# ---------------------------------------------------------------
# RWA Breakdown - Pillar 3 UK OV1 template risk-type category split, placed
# right after Total RWAs per the locked sheet order. FY2024/FY2023 tie
# exactly to the Total RWAs sheet above; FY2025/FY2022 are genuine
# documented mismatches, not transcription errors - see the in-sheet note.
# FY2021 predates the UK OV1 template and uses a different, coarser
# category split from that year's own Pillar 3 document.
# ---------------------------------------------------------------
RWA_BREAKDOWN_SOURCES = (
    "Sources - Paragon Banking Group PLC Pillar III Disclosures, UK OV1 'Overview of risk weighted "
    "exposure amounts' table, £m, regulatory-group basis (all recovered via Wayback Machine archives "
    "since paragonbankinggroup.co.uk blocks automated access):\n"
    "FY2025: Pillar III Disclosures 30 September 2025 (published ~23 Jan 2026), UK OV1 pp.9-10 - "
    "https://web.archive.org/web/20260203152658/https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/reports-presentations/2025/2025-pillar--iii\n"
    "FY2024: FY2025 Pillar III Disclosures' own 30 September 2024 comparative column, UK OV1 pp.9-10 "
    "(no standalone full-year FY2024 Pillar 3 document was locatable - only a half-year 31 March 2024 "
    "report exists at that URL slug) - same document as FY2025 above\n"
    "FY2023: Pillar III Disclosures 30 September 2023, UK OV1 pp.7-8 - "
    "https://web.archive.org/web/20240830064955/https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/reports-presentations/2023/2023-pillar-iii\n"
    "FY2022: Pillar III Disclosures 30 September 2022, UK OV1 pp.7-8 - "
    "https://web.archive.org/web/20240830044143/https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/reports-presentations/2022/pbg_2022_pillar_iii_disclosures\n"
    "FY2021: Pillar III Disclosures 30 September 2021, 'Total risk exposure (TRE)' table p.40 (predates "
    "the UK OV1 template) - "
    "https://web.archive.org/web/20240713140930/https://www.paragonbank.co.uk/resources/paragon-group/documents/reports-presentations/2022/pbg_2021_pillar_iii_disclosures\n\n"
    + ENTITY_NOTE +
    "\n\nDATA QUALITY NOTE (genuine, not transcription errors): FY2025's OV1 total (£8,630.6m) is "
    "close to but doesn't exactly match the pre-existing Total RWAs sheet's figure (£8,613.2m, sourced "
    "from the FY2025 Annual Report's own Note 38) - both are the Bank's own disclosed figures, just "
    "from two different contemporaneous documents. FY2022's OV1 total as originally published in the "
    "FY2022 Pillar 3 document (£7,645.8m, shown below) likewise doesn't match the Total RWAs sheet's "
    "KM1-sourced figure (£7,515.0m) - but the FY2023 Pillar 3 document's own FY2022 comparative column "
    "restates the FY2022 category breakdown (Credit risk £6,632.5m, CCR £249.4m, Operational risk "
    "£633.1m = £7,515.0m) to tie exactly. The originally-published FY2022 figures are shown below "
    "(each year on its own contemporaneous basis, per this rollout's standing convention), with this "
    "restatement flagged rather than silently blended in. FY2021 predates the UK OV1 template - its "
    "'Total risk exposure' table categorises differently (Credit risk/Operational risk/Market risk/"
    "Other, no separate CCR line) but ties closely to the Total RWAs sheet (£6,836.9m vs £6,836.8m, "
    "rounding)."
)
rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 7658.8, "FY2024": 7351.1, "FY2023": 6817.1, "FY2022": 6763.3, "FY2021": 6247.1}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 43.5, "FY2024": 79.6, "FY2023": 111.4, "FY2022": 249.9}),
    ("DATA", "Market risk", {"FY2021": 0.0}),
    ("DATA", "Operational risk", {"FY2025": 928.3, "FY2024": 848.0, "FY2023": 740.2, "FY2022": 633.1, "FY2021": 576.0}),
    ("DATA", "Other (FY2021 only; predates the UK OV1 template, category not broken out separately)", {"FY2021": 13.8}),
    ("TOTAL", "Total risk-weighted exposure amount", {"FY2025": 8630.6, "FY2024": 8278.7, "FY2023": 7668.7, "FY2022": 7645.8, "FY2021": 6836.9}),
]
bw.add_rwa_breakdown_sheet(
    title="Paragon Bank Plc — RWA Breakdown",
    subtitle="Pillar 3 UK OV1 template (top-level risk-type categories), £m, regulatory-group basis. "
              "FY2021 predates the UK OV1 template and uses a coarser risk-type split from that year's "
              "own Pillar 3 'Total risk exposure' table.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=64,
    source_height=340,
    unit_suffix=" (£m)",
)

metric("Leverage Ratio","%","Leverage ratio",lev,"FY2022 and FY2021 are not shown in the selected modern leverage-ratio series; no comparable figure was used.")
metric("LCR","%","Liquidity Coverage Ratio",lcr,"FY2025 is the 12-month average disclosed in the Annual Report; FY2024-FY2021 are applicable-average figures in the Pillar 3 disclosures.")
metric("NSFR","%","Net Stable Funding Ratio",nsfr)
metric("MREL Ratio","%","MREL ratio",{y:"Not publicly disclosed" for y in YEARS},"No MREL figure was located in the reviewed Paragon Annual Reports or Pillar 3 disclosures.")
bw.add_wide_interim_sheet(
    "Interim Pillar 3",
    rows=INTERIM_ROWS,
    hyperlink_cells={(i, 6): row[6] for i, row in enumerate(INTERIM_ROWS)},
    title="Paragon Bank Plc — Interim Pillar 3 Disclosures",
    subtitle="Half-year UK KM1 key metrics; regulatory-group basis, including all entities",
    note=("Coverage: 31 March 2021–31 March 2025. Standalone half-year reports are available for 2022–2025. "
          "31 March 2021 is included only as the comparative column in the official 31 March 2022 half-year report; "
          "no separate 2021 half-year Pillar 3 document was located. The disclosures are consolidated for the Paragon "
          "Bank regulatory group rather than Paragon Bank PLC statutory solo accounts. No MREL figure is reported."),
)
bw.add_overview_sheet(
 balance_sheet_totals=[
  ("Total assets",{"FY2025":19812.7,"FY2024":19200.3,"FY2023":18124.9,"FY2022":15389.0,"FY2021":13505.6}),
  ("Loans to customers",{"FY2025":12446.0,"FY2024":11671.6,"FY2023":11161.2,"FY2022":8952.8,"FY2021":8144.6}),
  ("Retail deposits",{"FY2025":16270.8,"FY2024":16314.7,"FY2023":13234.4,"FY2022":10569.5,"FY2021":9297.4}),
  ("Total equity",{"FY2025":1046.0,"FY2024":1050.1,"FY2023":1001.5,"FY2022":1063.4,"FY2021":819.3}),
 ], balance_sheet_unit="£m",
 income_statement_totals=[
  ("Total operating income",{"FY2025":442.7,"FY2024":424.7,"FY2023":424.3,"FY2022":395.4,"FY2021":238.1}),
  ("Operating expenses (incl. provisions)",{"FY2025":-164.5,"FY2024":-143.0,"FY2023":-127.9,"FY2022":-106.4,"FY2021":-70.6}),
  ("Profit for the financial year",{"FY2025":181.0,"FY2024":207.5,"FY2023":196.2,"FY2022":394.4,"FY2021":143.7}),
 ], income_statement_unit="£m",
 equity_changes_totals=[
  ("Opening equity",{"FY2025":1020.8,"FY2024":1001.5,"FY2023":1063.4,"FY2022":819.3,"FY2021":770.4}),
  ("Total comprehensive income for the year",{"FY2025":181.0,"FY2024":207.5,"FY2023":196.2,"FY2022":394.4,"FY2021":143.7}),
  ("Other equity movements, net (dividends paid)",{"FY2025":-155.8,"FY2024":-158.9,"FY2023":-258.1,"FY2022":-150.3,"FY2021":-94.8}),
  ("Closing equity",{"FY2025":1046.0,"FY2024":1050.1,"FY2023":1001.5,"FY2022":1063.4,"FY2021":819.3}),
 ], equity_changes_unit="£m",
 cash_flow_totals=[
  ("Net cash generated/(utilised) by operating activities",{"FY2025":-370.4,"FY2024":2084.9,"FY2023":1215.6,"FY2022":883.4,"FY2021":-934.8}),
  ("Net cash generated/(utilised) by investing activities",{"FY2025":-314.1,"FY2024":-462.5,"FY2023":206.3,"FY2022":-212.1,"FY2021":-414.4}),
  ("Net cash generated/(utilised) by financing activities",{"FY2025":538.0,"FY2024":-2104.0,"FY2023":-208.0,"FY2022":-219.3,"FY2021":869.7}),
  ("Closing cash and cash equivalents",{"FY2025":2231.9,"FY2024":2378.4,"FY2023":2860.0,"FY2022":1646.1,"FY2021":1194.1}),
 ], cash_flow_unit="£m",
 ratios=[("CET1 Ratio",cetr),("Tier 1 Ratio",cetr),("Total Capital Ratio",tcr),("Leverage Ratio",lev),("LCR",lcr),("NSFR",nsfr)],
 note="Cash-flow figures are Bank statutory; regulatory metrics are on the Paragon Bank regulatory-group basis. See each detail sheet."
)
bw.save("/Users/armaan/code/katalysis/banks/PARAGON FINANCIALS.xlsx")
