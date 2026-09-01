import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2026", "FY2025", "FY2024", "FY2023", "FY2022"]
YEAR_LABEL = {y: y for y in YEARS}

BASE = "https://www.pnbint.com/PNBIL/pdf/Financial_Reports/"
AR_URL = {
    "FY2026": BASE + "PNBIL-Annual-Report-2026.pdf",
    "FY2025": BASE + "PNBIL%20Annual%20Report%202025.pdf",
    "FY2024": BASE + "Annual_Report_31-03-2024.pdf",
    "FY2023": BASE + "PNBIL_Annual_Report_2023.pdf",
    "FY2022": BASE + "AnnualReport20220331.pdf",
}
P3_URL = {
    "FY2026": BASE + "Basel-III-Pillar-3-Disclosure-31-03-2026.pdf",
    "FY2025": BASE + "Basel%20III%20Pillar%203%20Disclosures%2031-03-2025.pdf",
    "FY2024": BASE + "Basel_III_Pillar_3_Disclosures%2031-03-2024.pdf",
    "FY2023": BASE + "PNBIL%20Pillar%20III%20Disclosures%20Publish%20Version.pdf",
    "FY2022": BASE + "Basel%20III%20Pillar%203%20Disclosures%20%2031-03-2022.pdf",
}

# Rates are £1 = US$X from the Bank of England XUDLUSS series.  Flow rates are
# averages over each 1 April-31 March financial year; stocks use the final
# available business-day spot rate at 31 March.  FY2022 opening cash uses the
# 31 March 2021 spot rate because it is shown as a comparative in the FY2022
# accounts.
FX_SPOT = {"FY2026": 1.3188, "FY2025": 1.2910, "FY2024": 1.2632,
           "FY2023": 1.2364, "FY2022": 1.3162, "FY2021": 1.3796}
FX_AVG = {"FY2026": 1.3404, "FY2025": 1.2763, "FY2024": 1.2568,
          "FY2023": 1.2045, "FY2022": 1.3662}
PREVIOUS_SPOT = {"FY2022": "FY2021", "FY2023": "FY2022", "FY2024": "FY2023",
                 "FY2025": "FY2024", "FY2026": "FY2025"}


def flow(values):
    return {y: round(v / FX_AVG[y], 1) for y, v in values.items()}


def stock(values):
    return {y: round(v / FX_SPOT[y], 1) for y, v in values.items()}


ENTITY_NOTE = (
    "Punjab National Bank (International) Limited (Companies House company 05781326, FRN 459701) is an active UK "
    "private limited bank, incorporated in England and Wales and wholly owned by Punjab National Bank, India. The "
    "FY2026 annual report confirms the registered office at 1 Moorgate, London EC2R 6JH, no branches outside the UK, "
    "and UK-adopted International Accounting Standards. The financial statements are entity-level and presented in "
    "US Dollars because that is the Bank's functional currency. The Bank's own Pillar 3 disclosures are solo-basis; "
    "PNB India consolidates the group separately. The Bank has a genuine Statement of Cash Flows in every report used."
)

FX_NOTE = (
    "USD-to-GBP conversion: cash-flow flows use the Bank of England XUDLUSS average rate for the 1 April-31 March "
    "financial year, while cash balances and Pillar 3 dollar amounts use the final available Bank of England spot "
    "rate at 31 March. Rates (£1 = $X) were FY2022 1.3662 average/1.3162 spot, FY2023 1.2045/1.2364, FY2024 "
    "1.2568/1.2632, FY2025 1.2763/1.2910, and FY2026 1.3404/1.3188. The FY2022 opening balance uses the 31 March "
    "2021 spot rate of 1.3796. Ratios remain exactly as reported because they are dimensionless. A computed GBP "
    "translation line reconciles the use of different flow and stock rates; it is not a Bank-reported cash-flow line."
)

CASH_FLOW_SOURCES = (
    "Sources - Punjab National Bank (International) Limited entity-level Statement of Cash Flows (native unit $'000):\n"
    "FY2026: Annual Report and Accounts 2026, printed p.50 - " + AR_URL["FY2026"] + "\n"
    "FY2025: Annual Report and Accounts 2025, printed p.49 - " + AR_URL["FY2025"] + "\n"
    "FY2024: Annual Report and Accounts 2024, printed p.44 - " + AR_URL["FY2024"] + "\n"
    "FY2023: Annual Report and Accounts 2023, printed p.39 - " + AR_URL["FY2023"] + "\n"
    "FY2022: Annual Report and Accounts 2022, printed p.36; FY2021 comparative is not needed for this five-year window - " + AR_URL["FY2022"] + "\n\n"
    + ENTITY_NOTE + "\n" + FX_NOTE
)


def p3_sources():
    return (
        "Sources - Punjab National Bank (International) Limited solo-basis Pillar 3 UK KM1 key metrics table, "
        "native unit $ million:\n"
        + "\n".join([
            f"FY2026: {P3_URL['FY2026']}, printed p.6 (2026 KM1)",
            f"FY2025: {P3_URL['FY2025']}, printed p.6 (2025 KM1)",
            f"FY2024: {P3_URL['FY2024']}, printed p.6 (2024 KM1)",
            f"FY2023: {P3_URL['FY2023']}, printed p.6 (2023 KM1)",
            f"FY2022: {P3_URL['FY2023']}, printed p.6 (2022 comparative in 2023 KM1); the 2022 report's headline ratios are also confirmed at printed p.5 via {P3_URL['FY2022']}",
        ])
        + "\n\n" + ENTITY_NOTE
    )


# Native cash-flow figures, $'000.  Each report's own current-year column is
# used; later reports' comparative columns were checked for continuity.
OPERATING = {
    "FY2026": 63882, "FY2025": 3518, "FY2024": -29200,
    "FY2023": 7735, "FY2022": -20687,
}
INVESTING = {
    "FY2026": -28192, "FY2025": -7088, "FY2024": 22199,
    "FY2023": -9217, "FY2022": -48112,
}
FINANCING = {
    "FY2026": -15391, "FY2025": -15689, "FY2024": -5568,
    "FY2023": -4493, "FY2022": -3305,
}
NET_CHANGE = {
    "FY2026": 23169, "FY2025": -17279, "FY2024": -10789,
    "FY2023": -5975, "FY2022": -72104,
}
EXCHANGE = {"FY2026": 2870, "FY2025": 1980, "FY2024": 1780,
            "FY2023": 998, "FY2022": 582}
OPENING_USD = {"FY2026": 116753, "FY2025": 134032, "FY2024": 144821,
               "FY2023": 149798, "FY2022": 221320}
CLOSING_USD = {"FY2026": 139922, "FY2025": 116753, "FY2024": 134032,
               "FY2023": 144821, "FY2022": 149798}

opening = {
    y: round(OPENING_USD[y] / FX_SPOT[PREVIOUS_SPOT[y]], 1) for y in YEARS
}
closing = stock(CLOSING_USD)
translation = {
    y: round(closing[y] - opening[y] - flow(NET_CHANGE)[y] - flow(EXCHANGE)[y], 1)
    for y in YEARS
}

rows = [
    ("SECTION", "Operating activities", {}),
    ("TOTAL", "Net cash (used in)/generated from operating activities", flow(OPERATING)),
    ("SECTION", "Investing activities", {}),
    ("TOTAL", "Net cash (used in)/generated from investing activities", flow(INVESTING)),
    ("SECTION", "Financing activities", {}),
    ("TOTAL", "Net cash used in financing activities", flow(FINANCING)),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", flow(NET_CHANGE)),
    ("DATA", "Effects of exchange rate on cash and cash equivalents (Bank's own line)", flow(EXCHANGE)),
    ("DATA", "Effect of GBP/USD translation (this workbook's conversion line)", translation),
    ("DATA", "Cash and cash equivalents at beginning of year", opening),
    ("TOTAL", "Cash and cash equivalents at end of year", closing),
]

bw = BankWorkbook(bank_name="Punjab National Bank (International) Limited", years=YEARS,
                  year_label=YEAR_LABEL, header_color="5C2751")
bw.add_cash_flow_sheet(
    title="Punjab National Bank (International) Limited — Statement of Cash Flows",
    subtitle="Entity-level basis, £'000 converted from the Bank's native US$'000 presentation",
    rows=rows, sources_text=CASH_FLOW_SOURCES, first_col_width=92, source_height=260,
    unit_suffix=" (£'000, conv. from USD)",
)


def metric(name, unit, data, note=None):
    bw.add_metric_sheet(name, unit, data, p3_sources(), note=note,
                        first_col_width=54, source_height=180)


CAPITAL_NOTE = "Directly disclosed in the annual Pillar 3 UK KM1 table; figures are converted from $m to £m at the corresponding 31 March spot rate."
RWA_NOTE = "Directly disclosed total risk-weighted exposure amount in the annual Pillar 3 UK KM1 table; converted from $m to £m at the corresponding 31 March spot rate."
LCR_NOTE = (
    "The Bank's own report-year headline LCR is used. FY2025's report shows 201% for FY2025, while its FY2024 "
    "comparative shows 528%; the FY2024 report itself reported 647% for FY2024. This workbook preserves each year's "
    "own as-reported figure rather than replacing it with a later comparative restatement."
)

CET1 = {"FY2026": 138.2, "FY2025": 140.8, "FY2024": 144.1, "FY2023": 143.1, "FY2022": 137.9}
TIER1 = {"FY2026": 183.2, "FY2025": 185.8, "FY2024": 189.1, "FY2023": 188.1, "FY2022": 182.9}
TOTAL_CAPITAL = {"FY2026": 210.9, "FY2025": 216.1, "FY2024": 223.1, "FY2023": 226.4, "FY2022": 213.9}
RWA = {"FY2026": 894.9, "FY2025": 697.1, "FY2024": 701.0, "FY2023": 730.1, "FY2022": 802.6}
CET1_RATIO = {"FY2026": "15.4%", "FY2025": "20.2%", "FY2024": "20.6%", "FY2023": "19.6%", "FY2022": "17.2%"}
TIER1_RATIO = {"FY2026": "20.5%", "FY2025": "26.7%", "FY2024": "27.0%", "FY2023": "25.8%", "FY2022": "22.8%"}
TOTAL_RATIO = {"FY2026": "23.6%", "FY2025": "31.0%", "FY2024": "31.8%", "FY2023": "31.0%", "FY2022": "26.7%"}
LEVERAGE = {"FY2026": "13.6%", "FY2025": "16.7%", "FY2024": "19.1%", "FY2023": "19.9%", "FY2022": "19.3%"}
LCR = {"FY2026": "350%", "FY2025": "201%", "FY2024": "647%", "FY2023": "384%", "FY2022": "405%"}
NSFR = {"FY2026": "118%", "FY2025": "121%", "FY2024": "130%", "FY2023": "135%", "FY2022": "128%"}

metric("CET1 Capital", "£m (conv. from USD)", [("Common Equity Tier 1 (CET1) capital", stock(CET1))], CAPITAL_NOTE)
metric("CET1 Ratio", "%", [("Common Equity Tier 1 ratio", CET1_RATIO)])
metric("Tier 1 Capital", "£m (conv. from USD)", [("Tier 1 capital", stock(TIER1))], CAPITAL_NOTE)
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", TIER1_RATIO)])
metric("Total Capital", "£m (conv. from USD)", [("Total capital", stock(TOTAL_CAPITAL))], CAPITAL_NOTE)
metric("Total Capital Ratio", "%", [("Total capital ratio", TOTAL_RATIO)])
metric("Total RWAs", "£m (conv. from USD)", [("Total risk-weighted exposure amount", stock(RWA))], RWA_NOTE)
metric("Leverage Ratio", "%", [("Leverage ratio excluding claims on central banks", LEVERAGE)])
metric("LCR", "%", [("Liquidity Coverage Ratio", LCR)], LCR_NOTE)
metric("NSFR", "%", [("Net Stable Funding Ratio", NSFR)])
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources(),
    per_note={"MREL Ratio": "No MREL ratio or MREL target is disclosed in the FY2022-FY2026 Pillar 3 reports or annual reports reviewed; left explicitly undisclosed."},
)

bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash (used in)/generated from operating activities", flow(OPERATING)),
        ("Net cash (used in)/generated from investing activities", flow(INVESTING)),
        ("Net cash used in financing activities", flow(FINANCING)),
        ("Cash and cash equivalents at end of year", closing),
    ],
    cash_flow_unit="£'000 (conv. from USD)",
    ratios=[("CET1 Ratio", CET1_RATIO), ("Tier 1 Ratio", TIER1_RATIO),
            ("Total Capital Ratio", TOTAL_RATIO), ("Leverage Ratio", LEVERAGE),
            ("LCR", LCR), ("NSFR", NSFR)],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing. See each sheet's source citation. Dollar amounts are converted to GBP; ratios remain as reported.",
)

bw.save("/Users/armaan/code/katalysis/banks/PUNJAB NATIONAL BANK INTERNATIONAL FINANCIALS.xlsx")
