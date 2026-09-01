import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

Y=["FY2025","FY2024","FY2023","FY2022","FY2021"]
AR={"FY2025":"https://www.shawbrook.co.uk/media/vkkpos4a/shawbrook-bank-limited-2025-annual-report-accounts.pdf","FY2024":"https://www.shawbrook.co.uk/media/jhujcnzh/shawbrook-bank-limited-2024-annual-report-accounts.pdf","FY2023":"https://www.shawbrook.co.uk/media/iflapcxl/shawbrook-bank-ltd-annual-report-and-accounts-2023.pdf","FY2022":"https://www.shawbrook.co.uk/media/wttf0kdt/2022-shawbrook-bank-limited-annual-report-and-accounts.pdf","FY2021":"https://www.shawbrook.co.uk/media/ft4eulfp/shawbrook-bank-ara-2021.pdf"}
P3={"FY2025":"https://www.shawbrook.co.uk/media/w5chxn4q/shawbrook-pillar-3-disclosures-2025.pdf","FY2024":"https://www.shawbrook.co.uk/media/rzpdavyj/shawbrook-2024-pillar-3-disclosures.pdf","FY2023":"https://www.shawbrook.co.uk/media/wrpglj2h/shawbrook-pillar-3-disclosures-2023.pdf","FY2022":"https://www.shawbrook.co.uk/media/pljhf2fo/2022-shawbrook-pillar-3-disclosures.pdf","FY2021":"https://www.shawbrook.co.uk/media/hlbpmnjm/pillar-3-2021.pdf"}
def d(vals): return dict(zip(Y,vals))
note=("Shawbrook Bank Limited (Companies House 00388466; FRN 204574; LEI 213800XSHRKUIZK86B68) is the matched legal entity. "
"Cash flows use the Company column, £m, from the Bank's consolidated-and-company accounts. Bank-specific Pillar 3 metrics are used for FY2021-FY2024. "
"The FY2025 Pillar 3 publication is Group-only after the listing and is not substituted for Bank data. FY2022 RWA/capital comparatives use the restatement in the 2023 Pillar 3 disclosure; FY2021 and FY2022 leverage bases differ.")
cf="Sources - Shawbrook Bank Limited Company cash flows (£m):\n"+"\n".join(f"{y}: Annual Report and Accounts cash-flow statement, p.{({'FY2021':106,'FY2022':98,'FY2023':111,'FY2024':107,'FY2025':114}[y])}, {AR[y]}" for y in Y)+"\n\n"+note
b=BankWorkbook(bank_name="Shawbrook Bank Limited",years=Y,header_color="FE1270")
r=[("SECTION","Cash flows from operating activities",{}),
("DATA","Profit before tax",d([252.7,271.6,333.8,284.6,203.8])),
("DATA","Adjustments for non-cash items and other adjustments",d([182.2,52.4,63.2,67.4,2.6])),
("DATA","(Increase)/decrease in operating assets",d([-2597.8,-1906.0,-2632.5,-2234.4,-1526.5])),
("DATA","Increase in operating liabilities",d([2590.0,2209.7,2775.8,2627.5,1449.6])),
("DATA","Tax (paid)/recovered",d([-56.5,-85.1,-88.5,-61.9,-48.4])),
("TOTAL","Net cash generated from operating activities",d([370.6,542.6,451.8,683.2,81.1])),
("SECTION","Cash flows from investing activities",{}),
("DATA","Purchase of investment securities",d([-1254.0,-691.3,-308.4,-204.8,-231.9])),
("DATA","Disposals and maturities of investment securities",d([441.1,60.7,194.8,92.9,37.7])),
("DATA","Purchase of property, plant and equipment",d([-0.3,-2.3,-0.7,-0.4,-0.7])),
("DATA","Purchase and development of intangible assets",d([-17.2,-13.3,-13.4,-9.1,-7.1])),
("DATA","Investment in right-of-use asset",d([0,-6.9,0,0,0])),
("DATA","Purchase of subsidiary",d([-64.8,-22.0,-44.7,0,-5.5])),
("TOTAL","Net cash (used by)/generated from investing activities",d([-895.2,-675.1,-172.4,-121.4,-207.5])),
("SECTION","Cash flows from financing activities",{}),
("DATA","Increase/(decrease) in amounts due to banks",d([58.5,-25.5,-101.1,298.0,385.2])),
("DATA","Issue of debt securities",d([0,0,0,0,0])),
("DATA","Repurchase and redemption of debt securities",d([0,0,0,0,0])),
("DATA","Costs arising on issue of debt securities",d([0,0,0,0,0])),
("DATA","Payment of principal portion of lease liabilities",d([-0.6,-1.5,-1.9,-2.1,-1.8])),
("DATA","Issue of subordinated debt",d([75.0,0,90.0,0,0])),
("DATA","Redemption of subordinated debt",d([-76.5,-20.0,0,0,0])),
("DATA","Costs arising on issue of subordinated debt",d([-0.9,0,-1.0,0,0])),
("DATA","Net proceeds from issue of share capital",d([50.0,0,0,0,0])),
("DATA","Decrease/(increase) in deemed loan due from structured entities",d([78.2,83.1,-120.7,0,0])),
("DATA","(Decrease)/increase in deemed loan due to structured entities",d([-12.8,119.3,136.2,-269.8,134.6])),
("DATA","Increase in deemed loan due from structured entities",d([0,0,0,-93.4,0])),
("DATA","Capital contribution",d([0,0,14.3,0,0])),
("DATA","Coupon paid to holders of capital securities",d([-15.1,-15.1,-16.9,-8.8,-9.8])),
("TOTAL","Net cash (used by)/generated from financing activities",d([155.8,140.3,-1.1,-76.1,508.2])),
("TOTAL","Net (decrease)/increase in cash and cash equivalents",d([-368.8,7.8,278.3,485.7,381.8])),
("DATA","Cash and cash equivalents as at 1 January",d([2493.5,2485.7,2207.4,1721.7,1339.9])),
("TOTAL","Cash and cash equivalents as at 31 December",d([2124.7,2493.5,2485.7,2207.4,1721.7]))]
b.add_cash_flow_sheet(title="Shawbrook Bank Limited — Company Cash Flow Statement",subtitle="Company/entity basis, £m; FY2021-FY2025 calendar year-ends.",rows=r,sources_text=cf,first_col_width=70,source_height=230,unit_suffix=" (£m)")
ps="Sources - Bank-specific Pillar 3: FY2021 Appendix 4 pp.54-58; FY2022 Bank tables 17 and KM1 pp.18-21; FY2023 Bank tables 14-15 pp.19-22; FY2024 Bank tables 11-12 pp.16-19.\n"+"\n".join(f"{y}: {P3[y]}" for y in Y)+"\nBlank cells mean not publicly disclosed/not applicable; FY2025 Group-only data is not used as a Bank proxy."
def m(name,unit,data,n=None): b.add_metric_sheet(name,unit,[(name,data)],ps,note=n,first_col_width=54,source_height=180)
m("CET1 Capital","£m",d([None,1297.0,1122.7,951.5,775.7]));m("CET1 Ratio","%",d([None,"13.0%","12.9%","12.7%","12.6%"]));m("Tier 1 Capital","£m",d([None,1422.0,1247.7,1076.5,900.7]));m("Tier 1 Ratio","%",d([None,"14.3%","14.3%","14.6%","14.7%"]));m("Total Capital","£m",d([None,1586.2,1431.7,1171.5,995.7]));m("Total Capital Ratio","%",d([None,"15.9%","16.4%","15.9%","16.2%"]));m("Total RWAs","£m",d([None,9952.2,8707.3,7466.4,6134.0]));m("Leverage Ratio","%",d([None,"8.1%","8.2%","8.8%","8.0%"]),"FY2022 uses the UK leverage framework effective 1 January 2022; FY2021 uses the prior basis and comparatives were not restated.");m("LCR","%",d([None,"265.0%","310.9%","290.3%",None]),"Bank-specific FY2021 LCR was not provided; Group data was not substituted.");m("NSFR","%",d([None,"134.5%","145.8%",None,None]),"NSFR was not applicable in the FY2022 disclosure and FY2025 Bank data is unavailable.");m("MREL Ratio","%",d([None,None,None,None,None]),"No Bank-specific quantitative MREL ratio was disclosed.")
b.add_overview_sheet(cash_flow_totals=[("Net cash generated from operating activities",d([370.6,542.6,451.8,683.2,81.1])),("Net cash (used by)/generated from investing activities",d([-895.2,-675.1,-172.4,-121.4,-207.5])),("Net cash (used by)/generated from financing activities",d([155.8,140.3,-1.1,-76.1,508.2])),("Cash and cash equivalents as at 31 December",d([2124.7,2493.5,2485.7,2207.4,1721.7]))],cash_flow_unit="£m",ratios=[("CET1 Ratio",d([None,"13.0%","12.9%","12.7%","12.6%"])),("Tier 1 Ratio",d([None,"14.3%","14.3%","14.6%","14.7%"])),("Total Capital Ratio",d([None,"15.9%","16.4%","15.9%","16.2%"])),("Leverage Ratio",d([None,"8.1%","8.2%","8.8%","8.0%"])),("LCR",d([None,"265.0%","310.9%","290.3%",None])),("NSFR",d([None,"134.5%","145.8%",None,None]))],note="Company-only cash flows and Bank-specific regulatory metrics; FY2025 Bank regulatory metrics are blank because the available Pillar 3 document is Group-only.")
b.save("/Users/armaan/code/katalysis/banks/SHAWBROOK FINANCIALS.xlsx")
