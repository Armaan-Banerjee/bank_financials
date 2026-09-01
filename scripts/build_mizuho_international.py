import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


# Mizuho International plc (company 01203696, FRN 119256), confirmed against
# Banks List 2608.xlsx and Companies House.  The reports present consolidated
# Mizuho International plc Group figures in GBP millions.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

AR = {
    "FY2025": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/6949753a5e4af5e79887a666_MIzuho_MHI_Annual_Report_2025.pdf",
    "FY2024": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/686301edbbd3ea24c5c8059f_mizuho_annual_report_2024_final_v02.pdf",
    "FY2023": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/6863021624e9468651ae2fbd_mizuho_annual_report_2023_final_02.pdf",
    "FY2022": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/686302389cf6e01446043fd2_2022-mizuho-international-plc-annual-report.pdf",
    "FY2021": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/686302637f7fc2c72f2e2f59_2021-mizuho-international-plc-annual-report.pdf",
}
P3 = {
    "FY2024": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/6864747a2fb833ca68387b1e_mhi-consolidated-pillar-3-disclosure-2024-final.pdf",
    "FY2023": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/68647496be5f9b72fe43c3f9_mhi-consolidated-pillar-3-disclosure-2023-final.pdf",
    "FY2022": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/686474abd90349ac917e208a_2022-mhi-consolidated-pillar-3-disclosure.pdf",
    "FY2021": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/6864754eb71eb72dcfb8ec06_2021-mizuho-international-plc-pillar-3-disclosure.pdf",
}

ENTITY_NOTE = (
    "ENTITY NOTE: Mizuho International plc (company 01203696, FRN 119256; LEI "
    "213800HZ54TG54H2KV03) is the legal entity in Banks List 2608.xlsx. "
    "Companies House confirms the active UK public company. Figures are the "
    "consolidated Mizuho International plc Group basis used in the official reports, "
    "in £ millions. The company accounts use the FRS 102 exemption from preparing a "
    "separate company cash-flow statement."
)

CF = {
    "Profit / (loss) before tax": {"FY2025": 5.8, "FY2024": 15.0, "FY2023": -10.4, "FY2022": -37.6, "FY2021": 43.8},
    "Non-cash items included in profit / (loss) before tax": {"FY2025": -30.0, "FY2024": -23.0, "FY2023": -6.3, "FY2022": 12.6, "FY2021": 23.3},
    "Provision for liabilities": {"FY2025": 0.1, "FY2024": -0.9, "FY2023": 0.9, "FY2022": -0.2, "FY2021": -0.4},
    "Movement in Other Comprehensive Income": {"FY2025": -0.5, "FY2024": -0.4, "FY2023": -0.1, "FY2022": -0.4, "FY2021": -0.5},
    "Change in operating assets": {"FY2025": 846.1, "FY2024": 2479.7, "FY2023": -5424.2, "FY2022": -3613.0, "FY2021": 6374.7},
    "Change in operating liabilities": {"FY2025": -938.8, "FY2024": -2313.4, "FY2023": 5456.5, "FY2022": 4012.7, "FY2021": -6952.2},
    "Interest paid": {"FY2025": -93.3, "FY2024": -92.7, "FY2023": -0.1, "FY2022": -0.2, "FY2021": -1.3},
    "Interest received": {"FY2025": 124.2, "FY2024": 139.8, "FY2023": 11.0, "FY2022": 14.4, "FY2021": 16.4},
    "Tax (paid) / received": {"FY2025": -6.1, "FY2024": 12.6, "FY2023": -2.0, "FY2022": -3.4, "FY2021": 10.5},
    "Net cash flows from operating activities": {"FY2025": -92.5, "FY2024": 216.7, "FY2023": 25.3, "FY2022": 384.9, "FY2021": -485.7},
    "Net investment in shares in group undertakings": {"FY2025": -1.4, "FY2024": -0.1, "FY2023": -0.5, "FY2022": -2.0, "FY2021": -0.1},
    "Dividends from investment in shares in group undertakings": {"FY2025": 0.4, "FY2024": 0.2, "FY2023": 0.3, "FY2022": 0.7, "FY2021": 0.4},
    "Purchase of intangible assets": {"FY2025": -43.8, "FY2024": -27.2, "FY2023": -28.7, "FY2022": -25.3, "FY2021": -21.8},
    "Purchase of tangible assets": {"FY2025": -5.2, "FY2024": -5.8, "FY2023": -2.7, "FY2022": -6.4, "FY2021": -3.6},
    "Net cash flows used in investing activities": {"FY2025": -50.0, "FY2024": -32.9, "FY2023": -31.6, "FY2022": -33.0, "FY2021": -25.1},
    "Net repayment from debt securities in issue": {"FY2025": -101.5, "FY2024": -221.2, "FY2023": -139.6, "FY2022": -87.8, "FY2021": 75.6},
    "Net repayment of subordinated liabilities": {"FY2022": -45.0},
    "Proceeds from the issuance of equity": {"FY2025": 45.0},
    "Net cash flows from / (used in) financing activities": {"FY2025": -56.5, "FY2024": -221.2, "FY2023": -139.6, "FY2022": -132.8, "FY2021": 75.6},
    "Net (decrease) / increase in cash and cash equivalents": {"FY2025": -199.0, "FY2024": -37.4, "FY2023": -145.9, "FY2022": 219.1, "FY2021": -435.2},
    "Effects of exchange rates on cash and cash equivalents": {"FY2025": -0.9, "FY2024": -4.2, "FY2023": 4.3, "FY2022": 2.2, "FY2021": -6.6},
    "Cash and cash equivalents at beginning of the period": {"FY2025": 375.6, "FY2024": 417.2, "FY2023": 558.8, "FY2022": 337.5, "FY2021": 779.3},
    "Cash and cash equivalents at the end of the period": {"FY2025": 175.7, "FY2024": 375.6, "FY2023": 417.2, "FY2022": 558.8, "FY2021": 337.5},
}

ROWS = [("SECTION", "Operating activities", {})]
for label in list(CF)[:10]:
    ROWS.append(("TOTAL" if label == "Net cash flows from operating activities" else "DATA", label, CF[label]))
ROWS.append(("SECTION", "Investing activities", {}))
for label in list(CF)[10:15]:
    ROWS.append(("TOTAL" if label == "Net cash flows used in investing activities" else "DATA", label, CF[label]))
ROWS.append(("SECTION", "Financing activities", {}))
for label in list(CF)[15:19]:
    ROWS.append(("TOTAL" if label == "Net cash flows from / (used in) financing activities" else "DATA", label, CF[label]))
for label in list(CF)[19:]:
    ROWS.append(("TOTAL" if "cash equivalents" in label else "DATA", label, CF[label]))

def sources():
    return ENTITY_NOTE + "\n\nOfficial sources — Mizuho International plc Annual Reports: " + "; ".join(f"{y}: {u}" for y, u in AR.items())

def p3_sources():
    return ENTITY_NOTE + "\n\nOfficial Mizuho International plc Pillar 3 disclosures: " + "; ".join(f"{y}: {u}" for y, u in P3.items()) + "\nFY2025 Pillar 3 PDF was not available at the official archive URL checked; 2025 values are included only where disclosed in the Annual Report KPI/regulatory-capital sections."

bw = BankWorkbook("Mizuho International plc", YEARS, header_color="7A3E9D")
bw.add_cash_flow_sheet("Mizuho International plc — Consolidated Statement of Cash Flows", "Consolidated Group basis, £ millions", ROWS, sources(), first_col_width=66, source_height=220, unit_suffix=" (£m)")

def metric(name, unit, values, note=None):
    bw.add_metric_sheet(name, unit, [(name, values)], p3_sources(), note=note, first_col_width=48, source_height=220)

metric("CET1 Capital", "£ millions", {"FY2025": 670.5, "FY2024": 637.4, "FY2023": 627.7, "FY2022": 640.8, "FY2021": 675.6}, "FY2025 Annual Report states regulatory capital consists solely of Tier 1 capital; treated as CET1 for this metric because no Tier 2 capital is reported.")
metric("CET1 Ratio", "%", {"FY2025": "20.0%", "FY2024": "22.8%", "FY2023": "28.0%", "FY2022": "31.14%", "FY2021": "31.12%"})
metric("Tier 1 Capital", "£ millions", {"FY2025": 670.5, "FY2024": 637.4, "FY2023": 627.7, "FY2022": 640.8, "FY2021": 675.6})
metric("Tier 1 Ratio", "%", {"FY2025": "20.0%", "FY2024": "22.84%", "FY2023": "28.00%", "FY2022": "31.14%", "FY2021": "31.12%"})
metric("Total Capital", "£ millions", {"FY2025": 670.5, "FY2024": 637.4, "FY2023": 627.7, "FY2022": 640.8, "FY2021": 711.6})
metric("Total Capital Ratio", "%", {"FY2025": "20.0%", "FY2024": "22.84%", "FY2023": "28.00%", "FY2022": "31.14%", "FY2021": "32.78%"})
metric("Total RWAs", "£ millions", {"FY2024": 2790.7, "FY2023": 2241.7, "FY2022": 2057.9, "FY2021": 2171.0}, "FY2025 standalone RWA was not numerically disclosed in the Annual Report sections checked; no ratio-based estimate is made.")
metric("Leverage Ratio", "%", {"FY2025": "4.2%", "FY2024": "4.07%", "FY2023": "4.24%", "FY2022": "4.07%", "FY2021": "4.75%"})
metric("LCR", "%", {"FY2025": "268.7%", "FY2024": "250.39%", "FY2023": "302.67%", "FY2022": "364.04%", "FY2021": "303.00%"})
metric("NSFR", "%", {"FY2025": "122.5%", "FY2024": "128.67%", "FY2023": "140.66%", "FY2022": "177.71%"}, "NSFR was not disclosed in the 2021 report; 2025 is from the Annual Report KPI section.")
metric("MREL Ratio", "%", {}, "MREL ratio was not numerically disclosed in the official annual/Pillar 3 reports checked.")

bw.add_overview_sheet(
    cash_flow_totals=[("Net cash flow from operating activities", CF["Net cash flows from operating activities"]), ("Net cash flows used in investing activities", CF["Net cash flows used in investing activities"]), ("Cash and cash equivalents at end of period", CF["Cash and cash equivalents at the end of the period"])],
    cash_flow_unit="£m",
    ratios=[("CET1 Ratio", {"FY2025": "20.0%", "FY2024": "22.8%", "FY2023": "28.0%", "FY2022": "31.14%", "FY2021": "31.12%"}), ("Leverage Ratio", {"FY2025": "4.2%", "FY2024": "4.07%", "FY2023": "4.24%", "FY2022": "4.07%", "FY2021": "4.75%"})],
    note="Annual consolidated Group data. 2025 Pillar 3 source was unavailable at the official archive URL checked, so latest-year values use the 2025 Annual Report KPI and regulatory-capital disclosures.",
)

bw.save("/Users/armaan/code/katalysis/banks/MIZUHO INTERNATIONAL FINANCIALS.xlsx")
