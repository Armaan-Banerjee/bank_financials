import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

AR_URLS = {
    "FY2025": "https://oaknorth.co.uk/wp-content/uploads/2026/03/Annual_Report_2025.pdf",
    "FY2024": "https://oaknorth.co.uk/wp-content/uploads/2025/03/Annual_Report_2024.pdf",
    "FY2023": "https://oaknorth.co.uk/wp-content/uploads/2024/03/OakNorth_Annual_Report_2023.pdf",
    "FY2022": "https://oaknorth.co.uk/wp-content/uploads/2023/03/OakNorth-Annual-Report-2022.pdf",
    "FY2021": "https://www.oaknorth.co.uk/wp-content/uploads/2022/03/OakNorth-Bank-Annual-Report-2021.pdf",
}
P3_URLS = {
    "FY2025": "https://oaknorth.co.uk/wp-content/uploads/2026/04/Pillar-3-Disclosures-OakNorth-Bank-Plc-2025-1.pdf",
    "FY2024": "https://oaknorth.co.uk/wp-content/uploads/2025/05/Pillar-3-Disclosures-OakNorth-Bank-Plc-2024.pdf",
    "FY2023": "https://oaknorth.co.uk/wp-content/uploads/2024/05/Pillar-3-Disclosure-OakNorth-Bank-Plc-2023.pdf",
    "FY2022": "https://oaknorth.co.uk/wp-content/uploads/2023/05/Pillar-3-disclosures-2022_Final.pdf",
    "FY2021": "https://oaknorth.co.uk/wp-content/uploads/2022/07/OakNorth_Pillar-3_2021.pdf",
}


def cash_flow_sources():
    return (
        "Sources — OakNorth Bank plc cash flows, £'000. FY2025: OakNorth Bank Plc Annual Report 2025, "
        f"pp.102-103 (Statement of cash flows) — {AR_URLS['FY2025']}\n"
        f"FY2024: Annual Report 2024, pp.94-95 — {AR_URLS['FY2024']}\n"
        f"FY2023: Annual Report 2023, pp.87-88 — {AR_URLS['FY2023']}\n"
        f"FY2022: Annual Report 2022, pp.106-107 — {AR_URLS['FY2022']}\n"
        f"FY2021: Annual Report 2021, p.87 — {AR_URLS['FY2021']}\n"
        "The 2022–2025 reports present both Bank Group and standalone Bank columns; this sheet uses the Bank Group "
        "column for those years. The 2021 report predates the ASK Partners consolidation and presents OakNorth Bank "
        "plc standalone figures, which are used for FY2021. Blank cells mean the line was not separately disclosed "
        "under that year's presentation; they are not zeros."
    )


def p3_sources():
    return (
        "Sources — OakNorth Bank Pillar 3 disclosures, £'000 unless percentages are shown. FY2025: UK KM1 p.14 "
        f"and OV1 p.15 — {P3_URLS['FY2025']}\n"
        f"FY2024: UK KM1 pp.16-17 — {P3_URLS['FY2024']}\n"
        f"FY2023: UK KM1 p.6 and capital adequacy p.10 — {P3_URLS['FY2023']}\n"
        f"FY2022: capital metrics pp.19-23 — {P3_URLS['FY2022']}\n"
        f"FY2021: regulatory capital and leverage pp.11-15 — {P3_URLS['FY2021']}\n"
        "The 2025 disclosure states that the prudential disclosures are on a consolidated Bank Group basis, while "
        "the 2022–2024 reports describe the relevant regulatory templates as solo/Bank basis. The 2021 figures are "
        "the standalone Bank figures."
    )


bw = BankWorkbook("OakNorth Bank plc", YEARS, header_color="6B8E23")

cash_rows = [
    ("SECTION", "Reconciliation of profit before tax to operating cash flows", {}),
    ("DATA", "Profit before tax", {"FY2025": 222529, "FY2024": 214794, "FY2023": 187333, "FY2022": 152336, "FY2021": 134540}),
    ("DATA", "Adjustments for non-cash items", {"FY2025": 20707, "FY2024": 11139, "FY2023": 30215, "FY2022": 7056, "FY2021": 646}),
    ("DATA", "Net change in other assets and liabilities", {"FY2025": 41185, "FY2024": 4665, "FY2023": -30857, "FY2022": -14137, "FY2021": -2050}),
    ("DATA", "Increase in loan receivables", {"FY2025": -496341, "FY2024": -573437, "FY2023": -714507, "FY2022": -251805, "FY2021": -390362}),
    ("DATA", "Increase in customer deposits", {"FY2025": 408891, "FY2024": 1463663, "FY2023": 1026092, "FY2022": 969657, "FY2021": 329975}),
    ("DATA", "(Increase)/decrease in derivatives held for risk management", {"FY2025": -29903, "FY2024": 7655, "FY2023": -2530}),
    ("DATA", "Income taxes paid", {"FY2025": -49351, "FY2024": -57333, "FY2023": -52840, "FY2022": -39766, "FY2021": -31850}),
    ("DATA", "Other operating adjustments not separately shown", {"FY2023": 531, "FY2022": 9880, "FY2021": 710}),
    ("TOTAL", "Net cash flows generated from operating activities", {"FY2025": 117717, "FY2024": 1071146, "FY2023": 443437, "FY2022": 833221, "FY2021": 41609}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of intangible assets", {"FY2025": -7832, "FY2024": -5279, "FY2023": -2961, "FY2022": -4358}),
    ("DATA", "Purchase of tangible assets", {"FY2025": -299, "FY2024": -75, "FY2023": -18, "FY2022": -19, "FY2021": -57}),
    ("DATA", "Acquisition of subsidiary, net of cash acquired", {"FY2022": -10475}),
    ("DATA", "Purchase of investment securities", {"FY2025": -621941, "FY2024": -820024, "FY2023": -897488, "FY2022": -202501, "FY2021": -191086}),
    ("DATA", "Proceeds from sale/maturity of investment securities", {"FY2025": 409522, "FY2024": 830700, "FY2023": 905244, "FY2022": 191000, "FY2021": 126771}),
    ("DATA", "Interest received on investment securities", {"FY2025": 21152, "FY2023": 623, "FY2022": 1076, "FY2021": 4029}),
    ("DATA", "Other investing cash flows and classification differences", {"FY2025": 90, "FY2024": 19, "FY2023": 18}),
    ("TOTAL", "Net cash flows from/(used in) investing activities", {"FY2025": -199308, "FY2024": 5341, "FY2023": 5418, "FY2022": -25277, "FY2021": -60343}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Increase in borrowings from Bank of England facilities", {"FY2025": 15000}),
    ("DATA", "Repayment of borrowings from Bank of England facilities", {"FY2025": -210000}),
    ("DATA", "Increase in subordinated debt", {"FY2024": 150000, "FY2023": 30000}),
    ("DATA", "Increase in intercompany borrowings", {"FY2025": 4541, "FY2024": 6326, "FY2023": 11660}),
    ("DATA", "Repayment/decrease of intercompany borrowings", {"FY2025": -7041, "FY2024": -9772}),
    ("DATA", "Interest paid on borrowings and subordinated debt", {"FY2025": -24084, "FY2024": -15538, "FY2023": -10073, "FY2022": -5449, "FY2021": -3964}),
    ("DATA", "Cash outflow on lease liabilities", {"FY2025": -1456, "FY2024": -1408, "FY2023": -686, "FY2022": -1050}),
    ("DATA", "Payment of dividend to parent", {"FY2025": -120000, "FY2024": -20000}),
    ("DATA", "Repayment of subordinated debt", {"FY2023": -50000}),
    ("DATA", "Other financing cash flows and classification differences", {"FY2025": -199}),
    ("DATA", "Increase in TFS borrowings", {"FY2021": 18100}),
    ("TOTAL", "Net cash flows from/(used in) financing activities", {"FY2025": -343239, "FY2024": 109608, "FY2023": -19099, "FY2022": -6499, "FY2021": 14136}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": -424920, "FY2024": 1186076, "FY2023": 429738, "FY2022": 801445, "FY2021": -4598}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 2893652, "FY2024": 1707576, "FY2023": 1277838, "FY2022": 476393, "FY2021": 480991}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 2468732, "FY2024": 2893652, "FY2023": 1707576, "FY2022": 1277838, "FY2021": 476393}),
    ("SECTION", "Reconciliation to cash at banks", {}),
    ("DATA", "Cash and balances at central bank", {"FY2025": 2199053, "FY2024": 2689013, "FY2023": 1637314, "FY2022": 1235711, "FY2021": 446374}),
    ("DATA", "Loans and advances to banks", {"FY2025": 77587, "FY2024": 75477, "FY2023": 33458, "FY2022": 37507, "FY2021": 30019}),
    ("DATA", "Investment securities (US money market funds)", {"FY2025": 192092, "FY2024": 124007, "FY2023": 31788}),
    ("TOTAL", "Total cash and cash equivalents", {"FY2025": 2468732, "FY2024": 2888497, "FY2023": 1702560, "FY2022": 1273218, "FY2021": 476393}),
]
bw.add_cash_flow_sheet(
    "OakNorth Bank plc — Consolidated Statement of Cash Flows",
    "Bank Group basis for FY2022–FY2025; standalone Bank basis for FY2021, £'000",
    cash_rows, cash_flow_sources(), first_col_width=62, source_height=155, unit_suffix=" (£'000)"
)


def metric(name, unit, rows, note=None):
    bw.add_metric_sheet(name, unit, rows, p3_sources(), note=note, first_col_width=52, source_height=155)


metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", {"FY2025": 988868, "FY2024": 952901, "FY2023": 853523, "FY2022": 719977, "FY2021": 628446})])
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 ratio", {"FY2025": "15.5%", "FY2024": "17.3%", "FY2023": "18.6%", "FY2022": "18.7%", "FY2021": "20.5%"})])
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", {"FY2025": 988868, "FY2024": 952901, "FY2023": 853523, "FY2022": 719977, "FY2021": 628446})])
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {"FY2025": "15.5%", "FY2024": "17.3%", "FY2023": "18.6%", "FY2022": "18.7%", "FY2021": "20.5%"})])
metric("Total Capital", "£'000", [("Total capital", {"FY2025": 1168868, "FY2024": 1132901, "FY2023": 883523, "FY2022": 769977, "FY2021": 678446})])
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2025": "18.4%", "FY2024": "20.5%", "FY2023": "19.3%", "FY2022": "20.1%", "FY2021": "22.1%"})])
metric("Total RWAs", "£'000", [("Total risk-weighted exposure amount", {"FY2025": 6363514, "FY2024": 5517819, "FY2023": 4577382, "FY2022": 3840274, "FY2021": 3065585})])
metric("Leverage Ratio", "£'000 / %", [
    ("Leverage ratio exposure measure excluding central banks", {"FY2025": 6177019, "FY2024": 5262074, "FY2023": 4463419, "FY2022": 4954910, "FY2021": 3855405}),
    ("Leverage ratio excluding central banks", {"FY2025": "16.0%", "FY2024": "18.1%", "FY2023": "19.1%", "FY2022": "14.5%", "FY2021": "21.4%"}),
    ("Leverage ratio exposure measure including central banks", {"FY2025": 8361483, "FY2024": 7951087, "FY2023": 6100733}),
    ("Leverage ratio including central banks", {"FY2025": "11.8%", "FY2024": "12.0%", "FY2023": "14.0%"}),
], note="The FY2021 disclosure labels its 21.4% figure as the UK leverage-ratio-framework calculation excluding claims on central banks; FY2022–FY2025 use the corresponding KM1 excluding-central-bank measure. FY2022–FY2025 do not disclose the including-central-bank variant in the same way until FY2023.")
metric("LCR", "£'000 / %", [
    ("Total high-quality liquid assets (HQLA), weighted value-average", {"FY2025": 2609639, "FY2024": 1876341, "FY2023": 1441255, "FY2022": 556199, "FY2021": "Not disclosed"}),
    ("Total net cash outflows, adjusted value", {"FY2025": 555901, "FY2024": 384055, "FY2023": 374177, "FY2022": 158569, "FY2021": "Not disclosed"}),
    ("Liquidity Coverage Ratio", {"FY2025": "478%", "FY2024": "489%", "FY2023": "385%", "FY2022": "351%", "FY2021": "Not publicly disclosed"}),
], note="The 2022–2025 LCR figures are the reported average/weighted-value disclosures. The FY2021 Pillar 3 report does not contain a comparable LCR key-metrics disclosure.")
metric("NSFR", "£'000 / %", [
    ("Total available stable funding", {"FY2025": 6855628, "FY2024": 6303663, "FY2023": 4831446, "FY2022": 3748427, "FY2021": "Not disclosed"}),
    ("Total required stable funding", {"FY2025": 3608230, "FY2024": 3324269, "FY2023": 2993447, "FY2022": 2436946, "FY2021": "Not disclosed"}),
    ("Net Stable Funding Ratio", {"FY2025": "190%", "FY2024": "190%", "FY2023": "161%", "FY2022": "154%", "FY2021": "Not publicly disclosed"}),
], note="UK NSFR disclosures began from 1 January 2022; no FY2021 NSFR disclosure exists in OakNorth's official Pillar 3 report.")
metric("MREL Ratio", None, [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})], note="No MREL ratio is presented in OakNorth's five annual Pillar 3 disclosures. This is a documented non-disclosure, not a zero.")

bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash flows generated from operating activities", {"FY2025": 117717, "FY2024": 1071146, "FY2023": 443437, "FY2022": 833221, "FY2021": 41609}),
        ("Net cash flows from/(used in) investing activities", {"FY2025": -199308, "FY2024": 5341, "FY2023": 5418, "FY2022": -25277, "FY2021": -60343}),
        ("Net cash flows from/(used in) financing activities", {"FY2025": -343239, "FY2024": 109608, "FY2023": -19099, "FY2022": -6499, "FY2021": 14136}),
        ("Cash and cash equivalents at end of year", {"FY2025": 2468732, "FY2024": 2888497, "FY2023": 1702560, "FY2022": 1273218, "FY2021": 476393}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "15.5%", "FY2024": "17.3%", "FY2023": "18.6%", "FY2022": "18.7%", "FY2021": "20.5%"}),
        ("Tier 1 Ratio", {"FY2025": "15.5%", "FY2024": "17.3%", "FY2023": "18.6%", "FY2022": "18.7%", "FY2021": "20.5%"}),
        ("Total Capital Ratio", {"FY2025": "18.4%", "FY2024": "20.5%", "FY2023": "19.3%", "FY2022": "20.1%", "FY2021": "22.1%"}),
        ("Leverage Ratio", {"FY2025": "16.0%", "FY2024": "18.1%", "FY2023": "19.1%", "FY2022": "14.5%", "FY2021": "21.4%"}),
        ("LCR", {"FY2025": "478%", "FY2024": "489%", "FY2023": "385%", "FY2022": "351%", "FY2021": "Not disclosed"}),
        ("NSFR", {"FY2025": "190%", "FY2024": "190%", "FY2023": "161%", "FY2022": "154%", "FY2021": "Not disclosed"}),
    ],
    note="OakNorth's official Pillar 3 archive is annual. This WF-018 workbook therefore contains the standard annual 13-sheet structure; no interim/14th worksheet is added in this pass.",
)

bw.save("/Users/armaan/code/katalysis/banks/OAKNORTH BANK FINANCIALS.xlsx")
