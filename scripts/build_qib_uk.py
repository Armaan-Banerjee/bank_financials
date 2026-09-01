import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}
CH = "https://find-and-update.company-information.service.gov.uk/company/04656003/filing-history"
AR = {"FY2025": CH+"/MzUyNzI4MTM5OGFkaXF6a2N4/document?format=pdf&download=0", "FY2024": CH+"/MzQ2NzkwMzQ0MmFkaXF6a2N4/document?format=pdf&download=0", "FY2023": CH+"/MzQyNDU4NzQ0OGFkaXF6a2N4/document?format=pdf&download=0", "FY2022": CH+"/MzM4MDQ4MTUzN2FkaXF6a2N4/document?format=pdf&download=0", "FY2021": CH+"/MzMzOTk2ODIxNmFkaXF6a2N4/document?format=pdf&download=0"}
P3 = {"FY2025": "https://www.qib-uk.com/-/media/project/uk/files/finance-reports/pillar-3-disclosure-document--2025-approved.pdf", "FY2024": "https://www.qib-uk.com/-/media/project/uk/files/finance-reports/pillar-3-disclosure-document-31-december-2024.pdf", "FY2023": "https://www.qib-uk.com/-/media/project/uk/files/finance-reports/pillar-3-disclosure-document-31-december-2023.pdf", "FY2022": "https://www.qib-uk.com/-/media/project/uk/files/finance-reports/pillar-3-disclosure-document-2023.pdf", "FY2021": "https://www.qib-uk.com/-/media/project/uk/files/finance-reports/pillar-3-disclosure-document-2023.pdf"}

ENTITY = ("ENTITY NOTE: QIB (UK) plc (Companies House 04656003, FRN 466577) is the UK bank subsidiary of Qatar Islamic Bank S.A.Q. The Bank states that it had no active subsidiaries or joint ventures at 31 December 2023 and does not prepare group accounts; these are entity-only GBP accounts. Companies House shows the entity Active with accounts filed through FY2025.")
CASH_SOURCES = ("Sources - QIB (UK) plc's own entity Statement of Cash Flows, converted from £ to £m (divide by 1,000,000 and round to 2 decimals):\n" + "\n".join(f"{y}: Annual Report, p.{p} - {AR[y]}" for y,p in {"FY2025":24,"FY2024":25,"FY2023":24,"FY2022":25,"FY2021":22}.items()) + "\nFY2025/FY2024 reports label the FY2024 comparative restated and FY2023 labels the FY2022 comparative restated. Each year's own report column is used here, preserving the project convention and avoiding blended reclassifications. FY2024 and FY2023 each contain a source presentation difference between the printed operating line items and the printed operating subtotal; explicit reconciliation rows preserve both.\n\n" + ENTITY)
def p3_sources():
    return ("Sources - QIB (UK) plc's own Pillar 3 disclosures, UK KM1 Key Metrics template (amounts in £'000; ratios as reported):\n" + "\n".join(f"{y}: {('FY2022 comparative column of FY2022 disclosure' if y=='FY2021' else 'own-year disclosure')}, pp.6-7 - {P3[y]}" for y in YEARS) + "\nMREL is not disclosed in the reviewed QIB UK Pillar 3 documents.\n\n" + ENTITY)
def m(d): return {y: round(v/1_000_000, 2) for y,v in d.items()}

bw = BankWorkbook(bank_name="QIB (UK) plc", years=YEARS, year_label=YEAR_LABEL, header_color="0B4F6C")
rows = [
 ("SECTION", "Operating activities", {}),
 ("DATA", "Profit for the year", m({"FY2025":11731651,"FY2024":12602750,"FY2023":11949949,"FY2022":9692373,"FY2021":6855527})),
 ("DATA", "Depreciation", m({"FY2025":365521,"FY2024":545924,"FY2023":559334,"FY2022":533941,"FY2021":559611})),
 ("DATA", "Amortisation", m({"FY2025":11201,"FY2024":23300,"FY2023":48921,"FY2022":158848,"FY2021":135654})),
 ("DATA", "Taxation", m({"FY2025":4043683,"FY2024":4918194,"FY2023":4081371,"FY2022":1318592,"FY2021":375560})),
 ("DATA", "Fair value / impairment adjustments", m({"FY2025":1783183,"FY2024":898730,"FY2023":2383878,"FY2022":1490529,"FY2021":760690})),
 ("DATA", "Increase/(decrease) in financing arrangements", m({"FY2025":-72273531,"FY2024":-57921880,"FY2023":-44846764,"FY2022":-51177541,"FY2021":-133182070})),
 ("DATA", "Stage 3 ECL recoveries", m({"FY2024":0,"FY2023":-3750,"FY2022":-1223974,"FY2021":-3700})),
 ("DATA", "Increase/(decrease) in other assets", m({"FY2025":-1238998,"FY2024":-523919,"FY2023":-53161,"FY2022":-2981020,"FY2021":-183119})),
 ("DATA", "Increase/(decrease) in amounts due to banks", m({"FY2025":24774922,"FY2024":-20343376,"FY2023":-2185645,"FY2022":-14991188,"FY2021":-5075581})),
 ("DATA", "Increase/(decrease) in amounts due to customers", m({"FY2025":83009697,"FY2024":59016367,"FY2023":41134935,"FY2022":122440389,"FY2021":162594916})),
 ("DATA", "Increase/(decrease) in other liabilities", m({"FY2025":539841,"FY2024":458933,"FY2023":-2293547,"FY2022":5356669,"FY2021":3613140})),
 ("DATA", "Increase/(decrease) in financial assets at amortised cost", m({"FY2025":-3660555,"FY2024":-20589713,"FY2023":-21599498,"FY2022":-68236950,"FY2021":-14259831})),
 ("DATA", "Increase/(decrease) in derivative financial instruments", m({"FY2025":1265068,"FY2024":-1126779,"FY2023":-130255,"FY2022":388846,"FY2021":-5152783})),
 ("DATA", "Source operating subtotal reconciliation (see source note)", m({"FY2024":735088,"FY2023":1050000})),
 ("TOTAL", "Net cash inflow/(outflow) from operating activities", m({"FY2025":50351683,"FY2024":-21306381,"FY2023":-9904232,"FY2022":2769514,"FY2021":17038014})),
 ("SECTION", "Investing activities", {}),
 ("DATA", "Purchase of property, plant and equipment", m({"FY2025":-65532,"FY2024":-685282,"FY2023":-54715,"FY2022":-4369,"FY2021":-37762})),
 ("DATA", "Purchase of intangible assets", m({"FY2025":-103738,"FY2021":-116000})),
 ("TOTAL", "Net cash outflow from investing activities", m({"FY2025":-169270,"FY2024":-685282,"FY2023":-54715,"FY2022":-4369,"FY2021":-153762})),
 ("SECTION", "Financing activities", {}),
 ("DATA", "Repayment/(increase) of subordinated Wakala", m({"FY2025":-35344,"FY2024":-32973,"FY2023":100909,"FY2021":-2250000})),
 ("TOTAL", "Net cash (outflow)/inflow from financing activities", m({"FY2025":-35344,"FY2024":-32973,"FY2023":100909,"FY2022":0,"FY2021":-2250000})),
 ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", m({"FY2025":50147069,"FY2024":-22024636,"FY2023":-9858038,"FY2022":2765145,"FY2021":14634252})),
 ("DATA", "Cash and cash equivalents at start of year", m({"FY2025":82318198,"FY2024":49249786,"FY2023":59107824,"FY2022":56342679,"FY2021":41708427})),
 ("TOTAL", "Cash and cash equivalents at end of year", m({"FY2025":132465267,"FY2024":27225150,"FY2023":49249786,"FY2022":59107824,"FY2021":56342679})),
]
bw.add_cash_flow_sheet(title="QIB (UK) plc — Statement of Cash Flows", subtitle="Entity basis, £m, converted from the Bank's reported £ amounts; FY2021-FY2025.", rows=rows, sources_text=CASH_SOURCES, first_col_width=66, source_height=280, unit_suffix=" (£m)")
def metric(name, unit, data, note=None): bw.add_metric_sheet(name, unit, data, p3_sources(), note=note, first_col_width=50, source_height=220)
cap={"FY2025":124.259,"FY2024":113.099,"FY2023":98.878,"FY2022":86.739,"FY2021":78.028}; total={"FY2025":137.959,"FY2024":126.799,"FY2023":112.578,"FY2022":96.585,"FY2021":91.081}; rwa={"FY2025":693.154,"FY2024":601.928,"FY2023":543.184,"FY2022":499.121,"FY2021":462.020}
ratios={"CET1 Ratio":{"FY2025":"17.93%","FY2024":"18.79%","FY2023":"18.20%","FY2022":"17.38%","FY2021":"16.89%"},"Total Capital Ratio":{"FY2025":"19.90%","FY2024":"21.07%","FY2023":"20.73%","FY2022":"19.35%","FY2021":"19.71%"},"Leverage Ratio":{"FY2025":"10.67%","FY2024":"10.53%","FY2023":"9.61%","FY2022":"8.50%","FY2021":"8.75%"},"LCR":{"FY2025":"345.59%","FY2024":"322.05%","FY2023":"1153.62%","FY2022":"1236.14%","FY2021":"555.60%"},"NSFR":{"FY2025":"127.95%","FY2024":"128.20%","FY2023":"130.56%","FY2022":"129.18%","FY2021":"119.68%"}}
metric("CET1 Capital","£m",[("Common Equity Tier 1 (CET1) capital",cap)]); metric("CET1 Ratio","% of RWA",[("Common Equity Tier 1 ratio",ratios["CET1 Ratio"])]); metric("Tier 1 Capital","£m",[("Tier 1 capital",cap)],"KM1 reports Tier 1 equal to CET1; no AT1 capital is reported."); metric("Tier 1 Ratio","% of RWA",[("Tier 1 ratio",ratios["CET1 Ratio"])]); metric("Total Capital","£m",[("Total capital",total)]); metric("Total Capital Ratio","% of RWA",[("Total capital ratio",ratios["Total Capital Ratio"])]); metric("Total RWAs","£m",[("Total risk-weighted exposure amount",rwa)]); metric("Leverage Ratio","%",[("Leverage ratio excluding claims on central banks",ratios["Leverage Ratio"])]); metric("LCR","%",[("Liquidity coverage ratio",ratios["LCR"])]); metric("NSFR","%",[("Net stable funding ratio",ratios["NSFR"])]); metric("MREL Ratio","%",[("MREL ratio",{y:"Not publicly disclosed" for y in YEARS})],"No MREL ratio or requirement is disclosed in the reviewed QIB UK Pillar 3 documents.")
bw.add_overview_sheet(cash_flow_totals=[("Net cash inflow/(outflow) from operating activities",rows[15][2]),("Net cash outflow from investing activities",rows[18][2]),("Net cash (outflow)/inflow from financing activities",rows[21][2]),("Cash and cash equivalents at end of year",rows[24][2])], cash_flow_unit="£m", ratios=list(ratios.items()), note="Figures are duplicated from detail sheets; see each detail sheet's source citation.")
bw.save("/Users/armaan/code/katalysis/banks/QIB UK FINANCIALS.xlsx")
