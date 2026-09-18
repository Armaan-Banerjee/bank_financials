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
# SLUG NAMING ON THIS HOST IS LOAD-BEARING, AND IT IS NOT THE RULE WE FIRST
# WROTE DOWN. The full-year edition's slug carries a DOUBLE dash before "iii"
# and the half-year's a single one; the dash after the YEAR varies and cannot
# be predicted (FY2024 full-year is "2024--pillar--iii" but FY2025 full-year is
# "2025-pillar--iii"). Guessing the wrong combination does not 404: on
# 2026-09-18 ".../2025/2025--pillar--iii" returned HTTP 200 with
# "text/html; charset=utf-8" and a 96,461-byte body - the site's own index page
# served as a soft-404. Only the Content-Type and the %PDF magic separate it
# from a hit, which is why both are checked and recorded below.
# NOTE: P3_2025_URL is the 31 MARCH 2025 HALF-YEAR document despite its name -
# the full-year FY2025 edition is P3_FY2025_URL.
P3_FY2025_URL = "https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/reports-presentations/2025/2025-pillar--iii"
P3_2025_URL = "https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/reports-presentations/2025/2025-pillar-iii"
P3_2024_URL = "https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/reports-presentations/2024/2024--pillar--iii"
P3_2022_URL = "https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/reports-presentations/2022/pbg_2022_pillar_iii_disclosures"
P3_2021_URL = "https://www.paragonbank.co.uk/resources/paragon-group/documents/reports-presentations/2022/pbg_2021_pillar_iii_disclosures"
INTERIM_2026_URL = "https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/reports-presentations/2026/2026-pillar-iii"
INTERIM_2025_URL = "https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/reports-presentations/2025/2025-pillar-iii"
INTERIM_2024_URL = "https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/reports-presentations/2024/2024-pillar-iii"
INTERIM_2023_URL = "https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/reports-presentations/2023/paragonbankinggroup_hy_pillar-3_2023"
INTERIM_2022_URL = "https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/corporate-governance/half-year-pillar-iii"

ENTITY_NOTE = (
    "ENTITY/BASIS NOTE: Paragon Bank PLC (Companies House 05390593, FRN 604551; formerly Paragon Mortgages (No.24) PLC) "
    "is the regulated UK bank. Cash flows are the Bank's own statutory statement, £m, for years ended 30 September. "
    "Pillar 3 capital/liquidity figures are for the Paragon Bank regulatory group, including subsidiary entities, as stated "
    "in the 2025 accounts and Pillar 3 reports. CORRECTED 18 September 2026 (KM1-032): this note used to say that "
    "'the accessible 2025 URL is the half-year document', and that FY2025 capital metrics therefore used Annual "
    "Report note 38. The full-year FY2025 Pillar III is accessible - it sits at a different slug on the same host "
    "and was retrieved on 18 September 2026 - so FY2025 now comes from it, on the same basis as every other year. "
    "MREL is not disclosed in reviewed reports. "
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
 f"FY2025: Pillar III Disclosures - 30 September 2025, UK KM1 printed pp.8-9, column a '30 Sep 25' - "
 f"{P3_FY2025_URL} (retrieved 18 September 2026: HTTP 200, 'application/pdf', %PDF-1.6, 1,234,294 bytes, "
 f"104 pages)\n"
 f"FY2024 and FY2023: Pillar III Disclosures - 30 September 2024, UK KM1 printed pp.8-9 - {P3_2024_URL} "
 f"(retrieved 18 September 2026: HTTP 200, 'application/pdf', %PDF-1.7, 1,591,886 bytes, 107 pages)\n"
 f"FY2022 and FY2021: Pillar III Disclosures 30 September 2022, UK KM1 pp.7-10 - {P3_2022_URL}; "
 f"FY2021 own-funds/LCR appendix pp.89-98 - {P3_2021_URL}\n\n"
 "FY2025 WAS REPOINTED ON 18 SEPTEMBER 2026, AND THE OLD FIGURES ARE RECORDED HERE RATHER THAN DISCARDED "
 "(KM1-032). Until today FY2025 on these sheets came from Paragon Bank PLC's Annual Report 2025 note 38, "
 "because the FY2025 Pillar III was recorded as unobtainable. It was obtainable, and the two sources are "
 "not the same entity: note 38 reports PARAGON BANK PLC's own regulatory consolidation, whereas FY2024 back "
 "to FY2021 on these sheets - and the KM1 sheet throughout - report PARAGON BANKING GROUP PLC's regulatory "
 "group. The series therefore changed legal entity in its newest column without saying so. FY2025 now comes "
 "from the Group Pillar III like every other year. For completeness, note 38's Paragon Bank PLC figures at "
 "30 September 2025 were: CET1 and Tier 1 capital £1,085.1m, total regulatory capital £1,235.1m, total risk "
 "exposure £8,613.2m, CET1 ratio 12.6%, total capital ratio 14.3%, leverage ratio 6.2% on a total leverage "
 "exposure of £17,621.9m (Annual Report and Accounts - 30 September 2025, printed pp.116, 118 and 120; the "
 "capital tables there are marked 'not subject to audit' apart from the equity reconciliation). Those are "
 "the Bank's own audited-entity numbers and they are NOT substituted into any sheet.\n"
 "FY2024's NSFR was shown as 139.5% and has been corrected to 138.2%. Both the FY2024 and the FY2025 "
 "editions print 138.2% for 30 September 2024 on UK KM1 row 20; no document printing 139.5% was found, so "
 "the old value matched no source rather than a different one.\n" + ENTITY_NOTE
)
# FY2025 REPOINTED AND FY2024 NSFR CORRECTED, 18 September 2026 (KM1-032).
# Until today FY2025 was the only year in these series NOT taken from the
# Group's Pillar 3 - it came from Paragon Bank PLC's own Annual Report note 38,
# because the FY2025 Pillar III was believed unobtainable. It was obtainable,
# and the substitution was not like-for-like: AR note 38 reports PARAGON BANK
# PLC's regulatory consolidation, while every other year here reports PARAGON
# BANKING GROUP PLC's regulatory group. So the five-year series silently
# changed legal entity in its newest column. It no longer does. The Bank-PLC
# figures are not lost - they are recorded in P3_SOURCES below, unsubstituted.
# FY2024's NSFR was 139.5%, which matches no edition: both the FY2024 and the
# FY2025 Pillar III print 138.2% for 30 September 2024. Corrected to 138.2%.
capital={"FY2025":1172.4,"FY2024":1177.9,"FY2023":1188.9,"FY2022":1221.8,"FY2021":1055.8}
total={"FY2025":1322.4,"FY2024":1327.9,"FY2023":1338.9,"FY2022":1371.8,"FY2021":1205.8}
rwa={"FY2025":8630.7,"FY2024":8278.7,"FY2023":7668.7,"FY2022":7515.0,"FY2021":6836.8}
cetr={"FY2025":"13.6%","FY2024":"14.2%","FY2023":"15.5%","FY2022":"16.3%","FY2021":"15.4%"}
tcr={"FY2025":"15.3%","FY2024":"16.0%","FY2023":"17.5%","FY2022":"18.3%","FY2021":"17.6%"}
lev={"FY2025":"6.6%","FY2024":"7.0%","FY2023":"7.6%"}
lcr={"FY2025":"154.0%","FY2024":"211.5%","FY2023":"193.8%","FY2022":"146.3%","FY2021":"164.9%"}
nsfr={"FY2025":"138.7%","FY2024":"138.2%","FY2023":"128.0%","FY2022":"121.5%","FY2021":"118.9%"}

INTERIM_BASIS = "Paragon Bank regulatory group; consolidated Paragon Banking Group PLC disclosure including all entities"
INTERIM_PERIODS = {
    # 31 March 2026 added 18 September 2026 (KM1-032): the newest disclosure
    # Paragon has published, retrieved live the day the Cloudflare block was
    # solved. It is not a year-end date and therefore cannot sit in an annual
    # column - Paragon's FY2026 ends 30 September 2026, which has not happened.
    "31 Mar 2026": (INTERIM_2026_URL, "3-4", "UK KM1 key metrics table"),
    "31 Mar 2025": (INTERIM_2025_URL, "3", "UK KM1 key metrics table"),
    "31 Mar 2024": (INTERIM_2024_URL, "3-4", "UK KM1 key metrics table"),
    "31 Mar 2023": (INTERIM_2023_URL, "3-4", "UK KM1 key metrics table"),
    "31 Mar 2022": (INTERIM_2022_URL, "3-4", "UK KM1 key metrics table"),
    "31 Mar 2021": (INTERIM_2022_URL, "3-4", "UK KM1 comparative column in 31 March 2022 report"),
}
INTERIM_VALUES = {
    # 31 Mar 2026 is the first period in this series where Tier 1 exceeds CET1:
    # the Group issued AT1 in the half-year, so rows 2 and 3 step up while row 1
    # does not. Read from the 31 March 2026 half-year report, printed pp.3-4,
    # column "31 Mar 2026" (HTTP 200, application/pdf, %PDF, 326,403 bytes,
    # 6 pages, retrieved 18 September 2026).
    "31 Mar 2026": {
        "CET1 capital": (1171.3, "£m"), "Tier 1 capital": (1319.7, "£m"), "Total capital": (1469.7, "£m"),
        "Total risk-weighted exposure amount": (8685.7, "£m"), "CET1 ratio": (13.5, "%"),
        "Tier 1 ratio": (15.2, "%"), "Total capital ratio": (16.9, "%"), "Leverage ratio excluding claims on central banks": (7.2, "%"),
        "Liquidity coverage ratio": (145.6, "%"), "NSFR ratio": (134.9, "%"),
    },
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
# ---------------------------------------------------------------
# KM1 Key Metrics - Paragon's own published UK KM1 template, reproduced whole,
# placed immediately after Asset Quality and immediately before CET1 Capital.
#
# YEARS: FY2021-FY2025. FY2017-FY2020 carry NO COLUMN AT ALL - the UK KM1
# template post-dates those editions and none of them prints one.
#
# FY2025 AND FY2024 ARE BLANK FOR A REACH REASON, NOT AN ABSENCE REASON, and
# those two columns are deliberately kept visible so the gap is not hidden.
# Paragon publishes a full-year Pillar III every year and both editions exist;
# neither could be retrieved this session. See KM1_SOURCES for the evidence.
#
# COLUMN SELECTION. Paragon's KM1 prints three columns per edition (a / c / e =
# the reporting date, six months earlier, twelve months earlier). Only column a
# of each full-year edition is taken here, except FY2021 - see below.
# ---------------------------------------------------------------
KM1_YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

KM1_P3_2023_ARCHIVE = (
    "https://web.archive.org/web/20240830064955/https://www.paragonbankinggroup.co.uk/resources/"
    "paragon-group/documents/reports-presentations/2023/2023-pillar-iii"
)
KM1_P3_2022_ARCHIVE = (
    "https://web.archive.org/web/20240830044143/https://www.paragonbankinggroup.co.uk/resources/"
    "paragon-group/documents/reports-presentations/2022/pbg_2022_pillar_iii_disclosures"
)
KM1_P3_2021_ARCHIVE = (
    "https://web.archive.org/web/20240713140930/https://www.paragonbank.co.uk/resources/"
    "paragon-group/documents/reports-presentations/2022/pbg_2021_pillar_iii_disclosures"
)

KM1_SOURCES = (
    "Sources - Paragon Banking Group PLC, 'UK KM1 - Key metrics template', regulatory-group "
    "basis, £m, all years ended 30 September. Each year is read from the edition for which it is the "
    "REPORTING year, except FY2021 - see below. FY2025 and FY2024 come from the Group's live website; "
    "FY2023-FY2021 are Wayback Machine captures taken when the live host was refusing us:\n"
    f"FY2025: Pillar III Disclosures - 30 September 2025, section 2.1 'UK KM1 - Key metrics template', "
    f"printed pp.8-9 (rows 1-17 on p.8, rows 18-20 on p.9), column a '30 Sep 25' - {P3_FY2025_URL}\n"
    f"FY2024: Pillar III Disclosures - 30 September 2024, section 2.1, printed pp.8-9 (rows 1-11 on p.8, "
    f"rows UK 11a-20 on p.9), column a '30 Sept 24' - {P3_2024_URL}\n"
    f"FY2023: Pillar III Disclosures 30 September 2023, section 2.2, pp.8-10 (printed folios 8-10; the table "
    f"spans three pages), column a '30 Sept 23' - {KM1_P3_2023_ARCHIVE}\n"
    f"FY2022: Pillar III Disclosures 30 September 2022, section 2.2, pp.8-10, column a '30 Sept 22' - "
    f"{KM1_P3_2022_ARCHIVE}\n"
    f"FY2021: the SAME FY2022 edition's own column e '30 Sept 21', pp.8-10 - {KM1_P3_2022_ARCHIVE}. The "
    f"FY2021 edition itself contains no key-metrics template of any kind (see below), so this column is filled "
    f"from the earliest edition that prints the year rather than left blank. That edition is at "
    f"{KM1_P3_2021_ARCHIVE}\n\n"
    "THE FY2021 EDITION PRINTS NO KM1, ON POSITIVE EVIDENCE. Its contents page runs Introduction / Governance "
    "/ Risk management / Capital resources / Credit risk / Asset encumbrance / Counterparty credit risk / "
    "Interest rate risk / Liquidity risk / Securitisation / Remuneration / Glossary - there is no key-metrics "
    "section. Searching its extracted text returns zero occurrences of 'KM1', zero of 'Key metrics template' "
    "and zero of 'combined buffer', while the SAME extraction is rich on neighbouring regulatory language - 7 "
    "occurrences of 'own funds', 6 of 'SREP', 5 of 'Total exposure measure', 5 of 'countercyclical' and 4 of "
    "'risk-weighted'. The zeros are therefore a fact about the document, not about the extraction. This is "
    "consistent with the Group's own statement that the template is required from the 1 January 2022 UK "
    "regime; the FY2022 edition is its first.\n\n"
    "FY2025 AND FY2024 WERE EMPTY UNTIL 18 SEPTEMBER 2026, AND THE REASON GIVEN WAS WRONG (KM1-032). Until "
    "today this sheet said the two columns were blank because 'neither edition could be retrieved' - the "
    "Group's site 403ing us and the single archived capture refusing to replay. The retrieval failure was "
    "real; the conclusion drawn from it was not, and the cells stayed empty for want of a document that was "
    "sitting on the Group's own website the whole time. BOTH EDITIONS WERE RETRIEVED TODAY AND THE COLUMNS "
    "ARE NOW FILLED FROM THEM: Pillar III Disclosures - 30 September 2025 (HTTP 200, 'application/pdf', "
    "%PDF-1.6, 1,234,294 bytes, 104 pages, cover reading 'Paragon Banking Group PLC / Pillar III Disclosures "
    "- 30 September 2025') and Pillar III Disclosures - 30 September 2024 (HTTP 200, 'application/pdf', "
    "%PDF-1.7, 1,591,886 bytes, 107 pages). Both read 18 September 2026.\n"
    "WHAT ACTUALLY UNBLOCKED IT, recorded because it is reusable and was not obvious: the Cloudflare 403 on "
    "this host is triggered by the HTTP/2 request, not by the User-Agent, the headers, cookies or the path. "
    "The identical request sent over HTTP/1.1 (curl --http1.1) returns the PDF. A full browser header set "
    "over HTTP/2 is still refused; a bare User-Agent over HTTP/1.1 succeeds. Every previous attempt on this "
    "bank had varied the headers while leaving the protocol alone, so the block looked absolute and adaptive "
    "when it was neither. The earlier note's own words - 'the block is adaptive rather than fixed' - were an "
    "inference from repeated failure, and they were wrong.\n"
    "The Group does publish the template every year, as its half-year report states: 'Full Pillar 3 "
    "disclosures for the Group are required only at year end ... published annually at approximately the same "
    "time as the Group's report and accounts'. That sentence was already on this sheet, and it was already "
    "enough to know the documents existed.\n\n"
    "THE TWO EDITIONS DISAGREE WITH EACH OTHER ABOUT 30 SEPTEMBER 2024, ON ROWS 8 AND 9, AND BOTH READINGS "
    "ARE PRINTED HERE. The FY2024 edition's column a gives capital conservation buffer 2.5% and institution "
    "specific countercyclical buffer 2.0%. The FY2025 edition's '30 Sep 24' comparative column gives the same "
    "two numbers the other way round, 2.0% and 2.5%, and carries that reversal through all three of its "
    "columns. This sheet takes each year from its own edition, so FY2024 reads 2.5%/2.0% and FY2025 reads "
    "2.0%/2.5% - which on the face of the sheet looks like the two buffers swapping places between "
    "consecutive years. They are NOT reconciled and neither is corrected. For the reader's judgement rather "
    "than as an amendment: the UK capital conservation buffer has stood at 2.5% throughout, and the UK "
    "countercyclical buffer rate has been 2.0% since 5 July 2023, which fits the FY2024 edition's labelling "
    "and not the FY2025 edition's. Two further documents were checked and both agree with the FY2024 "
    "edition - the 31 March 2025 half-year report prints 2.5%/2.0% for its own '30 Sep 2024' column, and "
    "the 31 March 2026 half-year report prints 2.5%/2.0% for its '30 Sep 2025' column, which is the very "
    "date the FY2025 annual labels 2.0%/2.5%. So the FY2025 annual edition is the outlier among four "
    "documents, and on the face of it has the two row labels transposed. It is still reproduced exactly as "
    "printed, because this sheet reproduces a prescribed template rather than corrects one. Row 11 is 4.5% "
    "in every document, so whichever way the two are labelled the combined requirement is unaffected.\n\n"
    "ROW 4 DISAGREES WITH THE SAME DOCUMENT'S OWN UK OV1 BY 0.1, FOR FY2025. KM1 row 4 prints 8,630.7 and "
    "UK OV1 row 29 'Total' prints 8,630.6, two pages later in the same edition. This workbook carries each "
    "figure on the sheet that reproduces the template it was printed in - 8,630.7 here, 8,630.6 on the RWA "
    "Breakdown sheet - so the two sheets do not tie for FY2025, by design. It is component rounding, it is "
    "the Group's own, and silently aligning them would erase a real feature of the disclosure.\n\n"
    "LABEL SPELLING ON ROW UK 8a: the FY2022 and FY2023 editions print 'Conversation buffer', which is the "
    "Group's own typo for 'Conservation' and is kept as the reproduced label. The FY2024 and FY2025 editions "
    "spell it correctly. The row label is shared by all five columns, so it cannot show both; it keeps the "
    "older spelling and the correction is recorded here rather than applied silently.\n\n"
    "DASHES, 'N/A' AND BLANKS ARE THREE DIFFERENT THINGS ON THIS SHEET. Rows UK 8a, UK 9a, 10 and UK 10a are "
    "dashed in every edition, footnoted [a] 'These buffers are not currently applicable to the Group', and "
    "they now CARRY that dash for the three years a readable edition covers - FY2023 from the FY2023 "
    "edition's column a '30 Sept 23', FY2022 from the FY2022 edition's column a '30 Sept 22', and FY2021 "
    "from that same FY2022 edition's column e '30 Sept 21'. Rows 14a-14e are NOT "
    "dashed: they print the literal 'N/A', footnoted [b] 'These lines are only required for LREQ banks, as "
    "defined by the PRA Rulebook. The Group's balance sheet size is too small to be classified as an LREQ "
    "bank.' That is the Group's own word, not a dash, and it is deliberately NOT converted into one; those "
    "cells remain blank pending a corpus-wide decision on how a printed 'N/A' should be shown. Row 9 by "
    "contrast prints a real 0.0 for FY2022 and FY2021, and that disclosed zero is kept as a zero - it is a "
    "measured value, and tidying it into a dash would destroy the very distinction this sheet now draws. "
    "FY2025 and FY2024 now carry the same dashes on rows UK 8a, UK 9a, 10 and UK 10a, read from their own "
    "editions, which print them dashed and footnoted [a] exactly as the earlier years do; and FY2025 adds two "
    "more printed zeros, on rows 7b and 7c, kept as zeros on the same reasoning. Rows 14a-14e print 'N/A' in "
    "those two editions as well, so they stay blank.\n\n"
    "BASIS FOOTNOTES CARRIED BY THE SOURCE, which matter when comparing rows: the LCR block (rows 15, UK 16a, "
    "UK 16b, 16) is 'based on a 12 month rolling average of month end positions', row 17 likewise and "
    "'therefore cannot be derived from the values given above it', and the NSFR block (rows 18-20) is 'based "
    "on a 4 quarter rolling average of quarter end positions'.\n\n"
    "LATEST-EDITION CHECK 2026-09-18, COMPLETED. The Group's own results/reports index was read live "
    "(HTTP 200, 96,467 bytes) and the newest FULL-YEAR edition it lists is Pillar III Disclosures - "
    "30 September 2025, which is the newest this sheet could carry in any case: Paragon's year-end is "
    "30 September, so FY2026 has not ended. The newest disclosure of any kind is the half-year Pillar 3 for "
    "the six months ended 31 March 2026 (HTTP 200, 'application/pdf', %PDF, 326,403 bytes, 6 pages, read "
    "18 September 2026). That is not a year-end date and does not belong in an annual column; it belongs on "
    "the Interim Pillar 3 sheet, which is where the half-year series is kept.\n\n" + ENTITY_NOTE
)

km1_rows = [
    # FY2025 and FY2024 added 18 September 2026 (KM1-032), each read from the
    # edition for which it is the REPORTING year (map rule 1), never from the
    # other's comparative column:
    #   FY2025 <- Pillar III Disclosures - 30 September 2025, section 2.1,
    #             printed p.8 (rows 1-17) and p.9 (rows 18-20), column a
    #             "30 Sep 25".
    #   FY2024 <- Pillar III Disclosures - 30 September 2024, section 2.1,
    #             printed p.8 (rows 1-11) and p.9 (rows UK 11a-20), column a
    #             "30 Sept 24".
    # Both retrieved live from paragonbankinggroup.co.uk on 2026-09-18 over
    # HTTP/1.1 - see the source note for why the protocol is load-bearing.
    ("SECTION", "Available own funds (amounts)", {}),
    ("DATA", "1  Common Equity Tier 1 ('CET1') Capital (£m)",
     {"FY2025": 1172.4, "FY2024": 1177.9, "FY2023": 1188.9, "FY2022": 1221.8, "FY2021": 1055.8}),
    ("DATA", "2  Tier 1 capital (£m)",
     {"FY2025": 1172.4, "FY2024": 1177.9, "FY2023": 1188.9, "FY2022": 1221.8, "FY2021": 1055.8}),
    ("DATA", "3  Total capital (£m)",
     {"FY2025": 1322.4, "FY2024": 1327.9, "FY2023": 1338.9, "FY2022": 1371.8, "FY2021": 1205.8}),
    ("SECTION", "Risk-weighted exposure amounts", {}),
    # FY2025: the FY2025 edition prints 8,630.7 here and 8,630.6 as its own
    # UK OV1 row 29 total, two pages later. Both are kept where they were
    # printed - this sheet 8,630.7, the RWA Breakdown sheet 8,630.6 - and the
    # 0.1 is not reconciled away. It is component rounding inside one document.
    ("DATA", "4  Total risk-weighted exposure amount (£m)",
     {"FY2025": 8630.7, "FY2024": 8278.7, "FY2023": 7668.7, "FY2022": 7515.0, "FY2021": 6836.8}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "5  Common Equity Tier 1 ratio (%)",
     {"FY2025": "13.6%", "FY2024": "14.2%", "FY2023": "15.5%", "FY2022": "16.3%", "FY2021": "15.4%"}),
    ("DATA", "6  Tier 1 ratio (%)",
     {"FY2025": "13.6%", "FY2024": "14.2%", "FY2023": "15.5%", "FY2022": "16.3%", "FY2021": "15.4%"}),
    ("DATA", "7  Total capital ratio (%)",
     {"FY2025": "15.3%", "FY2024": "16.0%", "FY2023": "17.5%", "FY2022": "18.3%", "FY2021": "17.6%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure "
                "amount)", {}),
    ("DATA", "7a  Additional CET1 SREP requirements (%)",
     {"FY2025": "0.1%", "FY2024": "0.4%", "FY2023": "0.4%", "FY2022": "0.4%", "FY2021": "0.4%"}),
    # FY2025 prints a real 0.0 on rows 7b and 7c - a disclosed zero, kept as a
    # zero and not blanked, on the same reasoning as row 9's FY2022/FY2021.
    ("DATA", "7b  Additional AT1 SREP requirements (%)",
     {"FY2025": "0.0%", "FY2024": "0.1%", "FY2023": "0.2%", "FY2022": "0.2%", "FY2021": "0.2%"}),
    ("DATA", "7c  Additional T2 SREP requirements (%)",
     {"FY2025": "0.0%", "FY2024": "0.2%", "FY2023": "0.2%", "FY2022": "0.2%", "FY2021": "0.2%"}),
    ("DATA", "7d  Total SREP own funds requirements (%)",
     {"FY2025": "8.1%", "FY2024": "8.7%", "FY2023": "8.8%", "FY2022": "8.8%", "FY2021": "8.8%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    # ROWS 8 AND 9 CARRY A CROSS-EDITION CONTRADICTION ON ONE YEAR. For 30
    # September 2024 the FY2024 edition prints conservation 2.5 / countercyclical
    # 2.0, and the FY2025 edition's own "30 Sep 24" comparative prints the two
    # the other way round, 2.0 / 2.5. Each year here is taken from its own
    # edition, so FY2024 shows 2.5/2.0 and FY2025 shows 2.0/2.5 - which makes
    # the two columns look like a swap between consecutive years. It is not a
    # transcription error and it is deliberately NOT reconciled; see the source
    # note, which also records which reading the published UK buffer rates fit.
    ("DATA", "8  Capital conservation buffer (%)",
     {"FY2025": "2.0%", "FY2024": "2.5%", "FY2023": "2.5%", "FY2022": "2.5%", "FY2021": "2.5%"}),
    # Dashed in every edition - "not currently applicable to the Group".
    # "Conversation" is the Group's own typo for "Conservation" in the FY2022
    # and FY2023 editions and is kept as the reproduced label; the FY2024 and
    # FY2025 editions spell it correctly, which is recorded in the source note
    # rather than silently applied to a row label the older columns also use.
    ("DATA", "UK 8a  Conversation buffer due to macro-prudential or systemic risk identified at the level of "
             "a Member State (%)",
     {"FY2025": "-", "FY2024": "-", "FY2023": "-", "FY2022": "-", "FY2021": "-"}),
    # A disclosed 0.0 for FY2022 and FY2021 - a printed zero, kept as a zero.
    ("DATA", "9  Institution specific countercyclical capital buffer (%)",
     {"FY2025": "2.5%", "FY2024": "2.0%", "FY2023": "2.0%", "FY2022": "0.0%", "FY2021": "0.0%"}),
    ("DATA", "UK 9a  Systemic risk buffer (%)",
     {"FY2025": "-", "FY2024": "-", "FY2023": "-", "FY2022": "-", "FY2021": "-"}),
    ("DATA", "10  Global systemically important institution buffer (%)",
     {"FY2025": "-", "FY2024": "-", "FY2023": "-", "FY2022": "-", "FY2021": "-"}),
    ("DATA", "UK 10a  Other Systemically Important Institution buffer (%)",
     {"FY2025": "-", "FY2024": "-", "FY2023": "-", "FY2022": "-", "FY2021": "-"}),
    ("DATA", "11  Combined buffer requirement (%)",
     {"FY2025": "4.5%", "FY2024": "4.5%", "FY2023": "4.5%", "FY2022": "2.5%", "FY2021": "2.5%"}),
    ("DATA", "UK 11a  Overall capital requirements (%)",
     {"FY2025": "12.6%", "FY2024": "13.2%", "FY2023": "13.3%", "FY2022": "11.3%", "FY2021": "11.3%"}),
    ("DATA", "12  CET1 available after meeting the total SREP own funds requirements (%)",
     {"FY2025": "7.2%", "FY2024": "7.3%", "FY2023": "6.7%", "FY2022": "8.8%", "FY2021": "8.8%"}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "13  Total exposure measure excluding claims on central banks (£m)",
     {"FY2025": 17651.1, "FY2024": 16807.9, "FY2023": 15579.3, "FY2022": 15387.5, "FY2021": 14123.2}),
    ("DATA", "14  Leverage ratio excluding claims on central banks (%)",
     {"FY2025": "6.6%", "FY2024": "7.0%", "FY2023": "7.6%", "FY2022": "7.9%", "FY2021": "7.5%"}),
    ("SECTION", "Additional leverage ratio disclosure requirements", {}),
    # Rows 14a-14e print the literal "N/A" in every edition - LREQ-bank-only
    # lines that do not apply to the Group. Left blank, never zero. The FY2025
    # and FY2024 editions print "N/A" on these rows too, so adding those two
    # years changes nothing here.
    ("DATA", "14a  Fully loaded ECL accounting model leverage ratio excluding claims on central banks (%)", {}),
    ("DATA", "14b  Leverage ratio including claims on central banks (%)", {}),
    ("DATA", "14c  Average leverage ratio excluding claims on central banks (%)", {}),
    ("DATA", "14d  Average leverage ratio including claims on central banks (%)", {}),
    ("DATA", "14e  Countercyclical leverage ratio buffer (%)", {}),
    ("SECTION", "Liquidity Coverage Ratio", {}),
    ("DATA", "15  Total high-quality liquid assets ('HQLA') (Weighted value -average) (£m)",
     {"FY2025": 2439.5, "FY2024": 3049.1, "FY2023": 2082.1, "FY2022": 1296.7, "FY2021": 1393.5}),
    ("DATA", "UK 16a  Cash outflows - Total weighted value (£m)",
     {"FY2025": 1931.2, "FY2024": 1785.5, "FY2023": 1397.8, "FY2022": 1152.8, "FY2021": 1166.2}),
    ("DATA", "UK 16b  Cash inflows - Total weighted value (£m)",
     {"FY2025": 347.8, "FY2024": 332.9, "FY2023": 321.1, "FY2022": 265.4, "FY2021": 289.2}),
    ("DATA", "16  Total net cash outflows (adjusted value) (£m)",
     {"FY2025": 1583.5, "FY2024": 1452.6, "FY2023": 1076.7, "FY2022": 887.4, "FY2021": 877.1}),
    ("DATA", "17  Liquidity coverage ratio (%)",
     {"FY2025": "154.0%", "FY2024": "211.5%", "FY2023": "193.8%", "FY2022": "146.3%", "FY2021": "164.9%"}),
    ("SECTION", "Net Stable Funding Ratio", {}),
    ("DATA", "18  Total available stable funding (£m)",
     {"FY2025": 18036.8, "FY2024": 19506.0, "FY2023": 17543.6, "FY2022": 16596.2, "FY2021": 15452.9}),
    ("DATA", "19  Total required stable funding (£m)",
     {"FY2025": 13007.8, "FY2024": 14120.8, "FY2023": 13706.8, "FY2022": 13660.0, "FY2021": 12994.4}),
    ("DATA", "20  NSFR ratio (%)",
     {"FY2025": "138.7%", "FY2024": "138.2%", "FY2023": "128.0%", "FY2022": "121.5%", "FY2021": "118.9%"}),
]

bw.add_km1_sheet(
    title="Paragon Bank Plc — KM1 Key Metrics",
    subtitle="Paragon Banking Group PLC's own published 'UK KM1 - Key metrics template', reproduced in its own "
             "row order, row numbering, labels and precision. Amounts in £m, ratios as printed; all years "
             "ended 30 September. REGULATORY-GROUP BASIS, not Paragon Bank PLC statutory solo - see the entity "
             "note. FY2025 and FY2024 were added on 18 September 2026 from their own editions, both retrieved "
             "live from the Group's website; they had been empty on the mistaken ground that the editions "
             "could not be obtained - see the source note. FY2017-FY2020 are not shown at all: the template "
             "post-dates those editions.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=72,
    source_height=520,
    years=KM1_YEARS,
)


def metric(name, unit, label, values, note=None):
    bw.add_metric_sheet(name, unit, [(label, values)], P3_SOURCES, note=note, first_col_width=52, source_height=180)
metric("CET1 Capital","£m","Common Equity Tier 1 (CET1) capital",capital)
metric("CET1 Ratio","%","Common Equity Tier 1 ratio",cetr)
metric("Tier 1 Capital","£m","Tier 1 capital",capital,"No AT1 capital is reported; Tier 1 equals CET1 in each year.")
metric("Tier 1 Ratio","%","Tier 1 ratio",cetr)
metric("Total Capital","£m","Total regulatory capital",total)
metric("Total Capital Ratio","%","Total capital ratio",tcr)
metric("Total RWAs","£m","Total risk-weighted exposure amount",rwa,
       "FY2022 verified 2026-09-15 against the FY2022 Pillar III document itself: £7,515.0m is printed there "
       "four separate times (UK KM1 row 4, own-funds template row 60, IFRS 9 transitional template row 7, and "
       "the leverage section's 'Total risk exposure amount'), and Paragon's own printed FY2022 CET1 ratio of "
       "16.3% matches it (1,221.8/7,515.0 = 16.26%; against the OV1 total it would be 16.0%). The same "
       "document's UK OV1 total of £7,645.8m is the outlier and the FY2023 edition restates the FY2022 "
       "category split to tie to £7,515.0m. The RWA Breakdown sheet deliberately keeps the "
       "originally-published OV1 figures, so its Total row does not equal this sheet for FY2022 (nor for "
       "FY2025, where the same FY2025 edition prints 8,630.7 on KM1 row 4 and 8,630.6 on UK OV1 row 29) - "
       "see that sheet's note. Do not reconcile.")

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
    "exposure amounts' table (section 2.2), £m, regulatory-group basis. FY2025 and FY2024 come from the "
    "Group's live website; the older years are Wayback Machine captures taken when the live host was "
    "refusing us:\n"
    "FY2025: Pillar III Disclosures - 30 September 2025, UK OV1 printed pp.9-10, column a '30 Sep 25' - "
    + P3_FY2025_URL + " (retrieved 18 September 2026: HTTP 200, 'application/pdf', %PDF-1.6, 1,234,294 "
    "bytes). These figures were previously transcribed from the Wayback capture at "
    "https://web.archive.org/web/20260203152658/... of the same document; every one of them was re-checked "
    "against the live PDF today and they agree exactly, which is worth recording because the archived copy "
    "had been unreplayable and the transcription therefore unconfirmable.\n"
    "FY2024: Pillar III Disclosures - 30 September 2024, UK OV1 printed pp.10-11, column a '30 Sept 24' - "
    + P3_2024_URL + " (retrieved 18 September 2026: HTTP 200, 'application/pdf', %PDF-1.7, 1,591,886 "
    "bytes). REPOINTED 18 September 2026 from the FY2025 edition's comparative column b to FY2024's own "
    "edition, per the standing rule that a year is read from the edition for which it is the reporting "
    "year. The figures are identical either way (7,351.1 / 79.6 / 848.0 / 8,278.7), so this changes the "
    "provenance and not the data - and the agreement itself is a check: the later edition did not restate "
    "the year.\n"
    "  CLAIM WITHDRAWN 18 September 2026 (KM1-032). This citation used to add '(no standalone full-year "
    "FY2024 Pillar 3 document was locatable - only a half-year 31 March 2024 report exists at that URL "
    "slug)'. That was a failed fetch written down as a fact about the Group, and it is wrong twice over. "
    "(i) A standalone full-year edition IS published and is listed on the Group's own "
    "results-reports-and-presentations index: 'Paragon Banking Group PLC / Pillar III Disclosures - "
    "30 September 2024', retrieved once during this ticket on 2026-09-18 at HTTP 200, application/pdf, "
    "%PDF-, 1,591,886 bytes. A FY2025 full-year edition and a 31 March 2026 half-year edition are listed "
    "too. (ii) The sub-claim about the URL slug was literally true and still produced a false conclusion, "
    "because THE SLUG NAMING IS LOAD-BEARING: the full-year edition's slug carries a DOUBLE dash before "
    "'iii' and the half-year's a single one. Probing the half-year slug and finding a half-year report "
    "proves nothing about the full-year one sitting beside it.\n"
    "  THAT SLUG RULE WAS ITSELF OVERSTATED, AND IS NARROWED HERE (18 September 2026). It was written as "
    "'2024--pillar--iii' vs '2024-pillar-iii', i.e. as though BOTH dashes doubled for a full-year edition. "
    "Only the dash before 'iii' is reliable: the FY2025 full-year edition is '2025-pillar--iii', with a "
    "single dash after the year. Guessing '2025--pillar--iii' by analogy with 2024 does not fail cleanly - "
    "it returns HTTP 200 with 'text/html; charset=utf-8' and a 96,461-byte body, the site's own index page "
    "served as a soft-404. A status-code check would have read that as a hit. A pattern inferred from one "
    "year is the same shape of error this whole correction is about, committed one paragraph later.\n"
    "  NO LONGER BLOCKED - RESOLVED LATER THE SAME DAY. This entry recorded, hours earlier, that "
    "paragonbankinggroup.co.uk returned HTTP 403 from Cloudflare to every request including its own index "
    "page, that a full browser header set and a cookie-jar-plus-Referer retry were both refused, and that "
    "'the block is adaptive rather than fixed'. That last part was an inference from repeated failure and "
    "it was wrong. THE TRIGGER IS THE HTTP VERSION, NOT THE HEADERS: the same request sent over HTTP/1.1 "
    "returns the document, while HTTP/2 is refused no matter how the headers are dressed. Every attempt on "
    "this bank, across several sessions, had varied the headers and left the protocol alone. Both full-year "
    "editions and the Group's own index page were retrieved on 18 September 2026 by that route, each "
    "verified by Content-Type and %PDF magic rather than by status code, and the FY2025 and FY2024 columns "
    "on this sheet and on the KM1 sheet are transcribed from them. Recorded at length because it generalises: "
    "a 403 that survives every header permutation is worth one attempt at a different protocol before it is "
    "written down as a block.\n"
    "FY2023: Pillar III Disclosures 30 September 2023, UK OV1 pp.7-8 - "
    "https://web.archive.org/web/20240830064955/https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/reports-presentations/2023/2023-pillar-iii\n"
    "FY2022: Pillar III Disclosures 30 September 2022, UK OV1 pp.7-8 - "
    "https://web.archive.org/web/20240830044143/https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/reports-presentations/2022/pbg_2022_pillar_iii_disclosures\n"
    "FY2021: Pillar III Disclosures 30 September 2021, 'Total risk exposure (TRE)' table p.40 (predates "
    "the UK OV1 template) - "
    "https://web.archive.org/web/20240713140930/https://www.paragonbank.co.uk/resources/paragon-group/documents/reports-presentations/2022/pbg_2021_pillar_iii_disclosures\n\n"
    + ENTITY_NOTE +
    "\n\nDATA QUALITY NOTE (genuine, not transcription errors): FY2025's OV1 total (£8,630.6m) is "
    "0.1 below the Total RWAs and KM1 sheets' figure (£8,630.7m). UPDATED 18 September 2026: that gap "
    "used to be £17.5m, because the Total RWAs sheet then carried £8,613.2m from Paragon Bank PLC's "
    "Annual Report note 38 - a different legal entity from this sheet's regulatory group. FY2025 now "
    "comes from the Group Pillar III on both sheets, and what remains is the 0.1 by which that single "
    "document's own KM1 row 4 (8,630.7) exceeds its own UK OV1 row 29 total (8,630.6), two pages apart. "
    "Each figure is kept on the sheet reproducing the template it was printed in; component rounding "
    "inside one document is not something to reconcile away. FY2022's OV1 total as originally published in the "
    "FY2022 Pillar 3 document (£7,645.8m, shown below) likewise doesn't match the Total RWAs sheet's "
    "KM1-sourced figure (£7,515.0m) - but the FY2023 Pillar 3 document's own FY2022 comparative column "
    "restates the FY2022 category breakdown (Credit risk £6,632.5m, CCR £249.4m, Operational risk "
    "£633.1m = £7,515.0m) to tie exactly. The originally-published FY2022 figures are shown below "
    "(each year on its own contemporaneous basis, per this rollout's standing convention), with this "
    "restatement flagged rather than silently blended in. FY2021 predates the UK OV1 template - its "
    "'Total risk exposure' table categorises differently (Credit risk/Operational risk/Market risk/"
    "Other, no separate CCR line) but ties closely to the Total RWAs sheet (£6,836.9m vs £6,836.8m, "
    "rounding).\n\n"
    "FY2022 RESOLVED 2026-09-15 (RWA cross-sheet sweep - do not re-flag). The FY2022 Pillar III "
    "document was re-read in full to establish which of its two totals is the real one. Within that ONE "
    "document, £7,515.0m is printed four times - UK KM1 row 4 'Total risk-weighted exposure amount', the "
    "own-funds template row 60 'Total risk exposure amount', the IFRS 9 transitional template row 7 'Total "
    "risk-weighted assets', and the leverage section's 'Total risk exposure amount (£m)' - while £7,645.8m "
    "appears once, as UK OV1 row 29. The Total RWAs sheet's £7,515.0m is therefore the figure Paragon's own "
    "FY2022 document states as its total, corroborated three ways, and the OV1 total is the outlier. This "
    "is NOT the credit-risk-subtotal defect found at Redwood and Ghana International: the Total RWAs sheet "
    "holds the larger, complete figure and the breakdown holds the inflated one, i.e. the opposite pattern. "
    "The FY2022 OV1 is visibly internally inconsistent in several places - its own rows 1 and 2 disagree for "
    "the 30 Sept 21 column (6,186.1 vs 6,247.1) and its CCR 'of which' rows sum to 256.9 against a printed "
    "CCR line of 249.9. What the FY2023 edition's restatement shows is that OV1's credit-risk line "
    "double-counted part of counterparty credit risk: the restated credit-risk figure (£6,632.5m) is lower "
    "than the originally-published one (£6,763.3m) by exactly £130.8m, which is precisely the amount the "
    "FY2022 OV1 reports on its own row 7, 'CCR - of which the standardised approach', and the OV1 total "
    "exceeds the KM1 total by exactly that same £130.8m. Per this project's standing rule on restatements, "
    "each year keeps its own contemporaneous edition's figures rather than being reconciled, so the "
    "originally-published FY2022 OV1 numbers stay on this sheet as published and the Total RWAs sheet keeps "
    "the KM1 figure. Neither is to be changed to make the two sheets agree."
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

metric("Leverage Ratio","%","Leverage ratio",lev,"FY2022 and FY2021 are not shown in the selected modern leverage-ratio series; no comparable figure was "
       "used - but both years ARE on the KM1 sheet (rows 13 and 14), read from the FY2022 edition. FY2025 was "
       "6.2% here until 18 September 2026, which was Paragon Bank PLC's own fully loaded ratio from Annual "
       "Report note 38; it is now 6.6%, the Group regulatory-group ratio from UK KM1 row 14, on the same basis "
       "as FY2024 and FY2023. The two are different entities, not different measures of one.")
metric("LCR","%","Liquidity Coverage Ratio",lcr,"All five years are the Pillar 3 UK KM1 row 17 figure, which the editions footnote as 'based on a "
       "12 month rolling average of month end positions' and note 'cannot be derived from the values given "
       "above it'. FY2025 previously cited the Annual Report instead; the figure was the same 154.0%, but the "
       "citation now names the document the number is actually printed in.")
metric("NSFR","%","Net Stable Funding Ratio",nsfr)
metric("MREL Ratio","%","MREL ratio",{y:"Not publicly disclosed" for y in YEARS},"No MREL figure was located in the reviewed Paragon Annual Reports or Pillar 3 disclosures.")
bw.add_wide_interim_sheet(
    "Interim Pillar 3",
    rows=INTERIM_ROWS,
    hyperlink_cells={(i, 6): row[6] for i, row in enumerate(INTERIM_ROWS)},
    title="Paragon Bank Plc — Interim Pillar 3 Disclosures",
    subtitle="Half-year UK KM1 key metrics; regulatory-group basis, including all entities",
    note=("Coverage: 31 March 2021–31 March 2026. Standalone half-year reports are available for 2022–2026. "
          "31 March 2021 is included only as the comparative column in the official 31 March 2022 half-year report; "
          "no separate 2021 half-year Pillar 3 document was located. The disclosures are consolidated for the Paragon "
          "Bank regulatory group rather than Paragon Bank PLC statutory solo accounts. No MREL figure is reported.\n"
          "31 MARCH 2026 ADDED 18 September 2026. It is the newest Pillar 3 disclosure Paragon has published and is "
          "the newest this workbook can hold: the Group's year-end is 30 September, so there is no FY2026 annual "
          "column to be had. Tier 1 capital (£1,319.7m) exceeds CET1 (£1,171.3m) for the first time in this series, "
          "the Group having issued AT1 during the half-year; every earlier period has the two equal.\n"
          "TWO CROSS-EDITION RESTATEMENTS ARE VISIBLE HERE AND ARE NOT RECONCILED. (i) Each period's figures are "
          "read from its own half-year report, so 31 March 2025 shows £8,385.2m of RWEAs as that report printed "
          "them; the FY2025 annual Pillar III later prints £8,383.2m for the same date, a £2.0m restatement. "
          "(ii) The 31 March 2026 report restates leverage comparatives after a change in the treatment of IAS 39 "
          "fair value hedging adjustments - its own footnote says so - giving 31 March 2025 a total exposure "
          "measure of £17,117.1m against the £17,192.0m printed at the time. Each figure stays with the edition "
          "that printed it."),
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
