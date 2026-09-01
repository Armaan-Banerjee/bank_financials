import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}
AR2025_URL = "https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/2025-paragon-bank-plc-ara"
AR2024_URL = "https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/paragon-bank-plc-annual-report-and-accounts-2024"
AR2023_URL = "https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/paragon-bank-plc-annual-report-and-accounts-2023"
AR2022_URL = "https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/section-172/2022/paragon-bank-plc-s172"
AR2021_URL = "https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/section-172/paragonbankaccounts2021"
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
    "and FY2025 LCR/NSFR use its strategic-report disclosures. MREL is not disclosed in reviewed reports."
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
 ("DATA","Profit before tax",{"FY2025":242.2,"FY2024":265.0,"FY2023":232.6,"FY2022":480.2,"FY2021":182.5}),
 ("DATA","Non-cash movement on borrowing",{"FY2025":0.4}),
 ("DATA","Non-cash movement on investment securities",{"FY2025":34.2,"FY2024":-7.8}),
 ("DATA","Depreciation on property, plant and equipment",{"FY2022":0.3,"FY2021":0.3}),
 ("DATA","Impairment losses on loans to customers",{"FY2025":8.0,"FY2024":9.2,"FY2023":10.5,"FY2022":6.6,"FY2021":-10.9}),
 ("DATA","Loans to customers",{"FY2025":-536.9,"FY2024":-1016.3,"FY2023":-1755.5,"FY2022":-1056.2,"FY2021":-3001.0}),
 ("DATA","Derivative financial instruments",{"FY2025":78.0,"FY2024":199.1,"FY2023":87.7,"FY2022":-577.4,"FY2021":-10.5}),
 ("DATA","Fair value of portfolio hedges",{"FY2025":-49.6,"FY2024":-230.3,"FY2023":-97.4,"FY2022":394.9,"FY2021":70.0}),
 ("DATA","Other receivables",{"FY2025":21.4,"FY2024":-48.4,"FY2023":26.4,"FY2022":12.5,"FY2021":447.3}),
 ("DATA","Retail deposits",{"FY2025":-32.3,"FY2024":3032.7,"FY2023":2596.0,"FY2022":1368.9,"FY2021":1443.8}),
 ("DATA","Derivative financial instruments (liabilities)",{"FY2025":-33.6,"FY2024":59.2,"FY2023":-78.4,"FY2022":76.1,"FY2021":-65.6}),
 ("DATA","Fair value of portfolio hedges (liabilities)",{"FY2025":-11.6,"FY2024":47.6,"FY2023":68.9,"FY2022":-96.8,"FY2021":-13.0}),
 ("DATA","Increase in provisions",{"FY2025":25.5}),
 ("DATA","Other liabilities",{"FY2025":-54.7,"FY2024":-171.6,"FY2023":158.8,"FY2022":309.3,"FY2021":36.0}),
 ("DATA","Income taxes paid",{"FY2025":-61.4,"FY2024":-53.5,"FY2023":-34.0,"FY2022":-35.0,"FY2021":-13.7}),
 ("TOTAL","Net cash generated/(utilised) by operating activities",{"FY2025":-370.4,"FY2024":2084.9,"FY2023":1215.6,"FY2022":883.4,"FY2021":-934.8}),
 ("SECTION","Investing activities",{}),
 ("DATA","Investment in securities",{"FY2025":-233.0,"FY2024":-419.6}),
 ("DATA","Proceeds from sale of operating property, plant and equipment",{"FY2022":4.8}),
 ("DATA","Advances of loans to subsidiary undertakings",{"FY2025":-2817.8,"FY2024":-10556.4,"FY2023":-9543.8,"FY2022":-5429.8,"FY2021":-2320.0}),
 ("DATA","Repayment of loans by subsidiary entities",{"FY2025":2736.7,"FY2024":10513.5,"FY2023":9750.1,"FY2022":5212.9,"FY2021":1905.6}),
 ("TOTAL","Net cash generated/(utilised) by investing activities",{"FY2025":-314.1,"FY2024":-462.5,"FY2023":206.3,"FY2022":-212.1,"FY2021":-414.4}),
 ("SECTION","Financing activities",{}),
 ("DATA","Dividends paid",{"FY2025":-155.8,"FY2024":-158.9,"FY2023":-258.1,"FY2022":-150.3,"FY2021":-94.8}),
 ("DATA","Issue of covered bond",{"FY2025":498.8}),
 ("DATA","Repayment of long term bank facilities",{"FY2025":-500.0,"FY2024":-2000.0}),
 ("DATA","Movement on short term central bank facilities",{"FY2025":695.0,"FY2024":5.0,"FY2022":-69.0,"FY2021":964.6}),
 ("DATA","Movement on repurchase facilities",{"FY2024":49.9,"FY2023":50.1}),
 ("DATA","Capital element of lease payments",{"FY2021":-0.1}),
 ("TOTAL","Net cash generated/(utilised) by financing activities",{"FY2025":538.0,"FY2024":-2104.0,"FY2023":-208.0,"FY2022":-219.3,"FY2021":869.7}),
 ("TOTAL","Net (decrease)/increase in cash and cash equivalents",{"FY2025":-146.5,"FY2024":-481.6,"FY2023":1213.9,"FY2022":452.0,"FY2021":-479.5}),
 ("DATA","Opening cash and cash equivalents",{"FY2025":2378.4,"FY2024":2860.0,"FY2023":1646.1,"FY2022":1194.1,"FY2021":1673.6}),
 ("TOTAL","Closing cash and cash equivalents",{"FY2025":2231.9,"FY2024":2378.4,"FY2023":2860.0,"FY2022":1646.1,"FY2021":1194.1}),
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
bw.add_cash_flow_sheet(title="Paragon Bank Plc — Cash Flow Statement", subtitle="Bank statutory basis, £m; see source and basis note", rows=rows, sources_text=CASH_FLOW_SOURCES, first_col_width=72, source_height=260, unit_suffix=" (£m)")
def metric(name, unit, label, values, note=None):
    bw.add_metric_sheet(name, unit, [(label, values)], P3_SOURCES, note=note, first_col_width=52, source_height=180)
metric("CET1 Capital","£m","Common Equity Tier 1 (CET1) capital",capital)
metric("CET1 Ratio","%","Common Equity Tier 1 ratio",cetr)
metric("Tier 1 Capital","£m","Tier 1 capital",capital,"No AT1 capital is reported; Tier 1 equals CET1 in each year.")
metric("Tier 1 Ratio","%","Tier 1 ratio",cetr)
metric("Total Capital","£m","Total regulatory capital",total)
metric("Total Capital Ratio","%","Total capital ratio",tcr)
metric("Total RWAs","£m","Total risk-weighted exposure amount",rwa)
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
