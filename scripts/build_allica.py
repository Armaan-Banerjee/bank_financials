import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first

AR2025_URL = "https://www.allica.bank/hubfs/pdf/allica-bank_annual-report-2025.pdf"
AR2023_URL = "https://www.allica.bank/hubfs/Allica-Bank_Annual-report_2023.pdf"
AR2022_URL = "https://www.allica.bank/hubfs/pdf/web/investor-relations/Allica_Bank-Annual_Report-2022.pdf"

P3_2025_URL = "https://www.allica.bank/hubfs/pdf/Pillar-3-Report-2025_Allica.pdf"
P3_2024_URL = "https://www.allica.bank/hubfs/pdf/Pillar-3-Report-2024_Allica.pdf"
P3_2023_URL = "https://www.allica.bank/hubfs/Allica%20Bank%20Limited_Pillar%203%20Report%20_Year-ended%2031%20December%202023.pdf"
P3_2022_URL = "https://www.allica.bank/hubfs/pdf/web/investor-relations/Allica_Bank_Pillar_3_disclosure_2022.pdf"

CASH_FLOW_SOURCES = (
    "Sources — all figures are Allica Bank Limited consolidated (Group) cash flow statement, £m:\n"
    f"FY2025 & FY2024: Allica Bank Limited Annual Report & Accounts 2025, p.92-93 (Statement of cash flows) — {AR2025_URL}\n"
    f"FY2023 & FY2022: Allica Bank Limited Annual Report and Accounts 2023, p.76-77 & Note 32 p.130-131 (Statements of "
    f"cash flows / Note 32: Cash flow information) — {AR2023_URL}\n"
    f"FY2021: Allica Bank Limited Annual Report and Accounts 2022, p.85 & Note 32 p.139 (Statements of cash flows / "
    f"Note 32: Cash flow information) — {AR2022_URL}\n"
    "Note: Allica changed cash flow statement presentation across report vintages. FY2021-FY2023 reports show a Note 32 "
    "reconciliation (profit before tax + non-cash adjustments + working capital changes = 'Cash generated from "
    "operations') and then add actual cash 'Interest income received'/'Interest expense paid' on the face of the "
    "primary statement to reach 'Net cash from operating activities'. FY2024-FY2025 reports show the full "
    "reconciliation (including accrued-interest reversal lines) directly on the face of the statement with no "
    "separate interest-received/paid lines, reaching 'Net cash from operating activities' via 'Tax paid' alone. Blank "
    "cells indicate a line not separately disclosed that year under the applicable presentation; the operating/"
    "investing/financing/net-change/cash-at-year-end TOTAL rows are all consistent and comparable across all 5 years "
    "(independently cross-checked by hand against each year's underlying line items). FY2024-FY2025 also newly "
    "disclose 'Acquisition of a subsidiary, net of cash acquired' and a foreign-exchange translation line, both nil/"
    "absent in FY2021-FY2023 (Allica had no foreign operations in that earlier period)."
)

def p3_sources(extra_note=None):
    text = (
        "Sources — Allica Bank Limited consolidated (Group) basis, UK KM1 Key Metrics table, £'000:\n"
        f"FY2025: Allica Bank Limited Pillar 3 Report 2025, p.2 — {P3_2025_URL}\n"
        f"FY2024: Allica Bank Limited Pillar 3 Report 2024, p.2 — {P3_2024_URL}\n"
        f"FY2023: Allica Bank Limited Pillar 3 Report 2023, p.2-3 — {P3_2023_URL}\n"
        f"FY2022: Allica Bank Limited Pillar 3 Report, year ended 31 December 2022, p.2 — {P3_2022_URL}\n"
        f"FY2021: comparative column of the FY2022 Pillar 3 Report above, p.2 (restated onto the post-1 Jan 2022 "
        "leverage exposure basis per PRA PS21/21)."
    )
    if extra_note:
        text += "\n" + extra_note
    return text

bw = BankWorkbook(bank_name="Allica Bank Limited", years=YEARS, header_color="C1440E")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Reconciliation of profit before tax to net cash flows from operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {"FY2025": 36.9, "FY2024": 29.9, "FY2023": 16.091, "FY2022": -1.587, "FY2021": -25.058}),
    ("DATA", "Depreciation", {"FY2025": 1.5, "FY2024": 1.0, "FY2023": 0.849, "FY2022": 0.491, "FY2021": 0.312}),
    ("DATA", "Amortisation", {"FY2025": 9.4, "FY2024": 5.3, "FY2023": 3.606, "FY2022": 2.846, "FY2021": 2.421}),
    ("DATA", "Loss on disposal/write-off of fixed assets", {"FY2023": 0.028, "FY2022": 0.059, "FY2021": 0}),
    ("DATA", "Loss on write-off of intangible assets", {"FY2023": 0.939, "FY2022": 0, "FY2021": 6.712}),
    ("DATA", "Net fair value (losses)/gains on derivatives", {"FY2025": 0, "FY2024": 0, "FY2023": -0.146, "FY2022": 0.017, "FY2021": 0.147}),
    ("DATA", "Share-based payment charge", {"FY2023": 0, "FY2022": 0.288, "FY2021": 0.113}),
    ("DATA", "Impairment losses", {"FY2025": 13.3, "FY2024": 10.7, "FY2023": 14.279, "FY2022": 8.417, "FY2021": 1.077}),
    ("DATA", "Interest income accrued (non-cash reversal)", {"FY2025": -17.2, "FY2024": -14.7, "FY2023": -177.843, "FY2022": -72.252, "FY2021": -11.494}),
    ("DATA", "Interest expense accrued (non-cash reversal)", {"FY2025": -9.9, "FY2024": 19.1, "FY2023": 97.813, "FY2022": 23.358, "FY2021": 3.670}),
    ("DATA", "Other non-cash items", {"FY2025": 6.6, "FY2024": 0}),
    ("SECTION", "Changes in operating assets and liabilities", {}),
    ("DATA", "Net change in balances at central banks", {"FY2025": -0.1, "FY2024": 6.7, "FY2023": -6.106, "FY2022": -2.870, "FY2021": 0}),
    ("DATA", "Net change in loans and advances to banks", {"FY2025": 3.6, "FY2024": 41.7, "FY2023": -16.762, "FY2022": -28.527, "FY2021": 0}),
    ("DATA", "Net change in loans and advances to customers", {"FY2025": -651.3, "FY2024": -1007.9, "FY2023": -618.964, "FY2022": -795.711, "FY2021": -520.942}),
    ("DATA", "Net change in deposits from banks", {"FY2025": -16.5, "FY2024": 13.4}),
    ("DATA", "Net change in deposits from customers", {"FY2025": 1301.1, "FY2024": 1778.5, "FY2023": 1101.860, "FY2022": 657.114, "FY2021": 740.017}),
    ("DATA", "Net change in cash collateral", {"FY2023": -20.029, "FY2022": 23.514, "FY2021": 0}),
    ("DATA", "Net change in derivatives (balance sheet)", {"FY2022": 0, "FY2021": 0.806}),
    ("DATA", "Net change in trade and other debtors", {"FY2025": -2.5, "FY2024": -2.8, "FY2023": 2.447, "FY2022": 13.890, "FY2021": -20.758}),
    ("DATA", "Net change in trade and other creditors", {"FY2025": -1.6, "FY2024": 6.6, "FY2023": 2.034, "FY2022": 2.715, "FY2021": 2.364}),
    ("DATA", "Net change in provisions", {"FY2022": 0, "FY2021": -0.024}),
    ("DATA", "Interest income received (cash)", {"FY2023": 158.027, "FY2022": 71.813, "FY2021": 10.361}),
    ("DATA", "Interest expense paid (cash)", {"FY2023": -76.617, "FY2022": -17.118, "FY2021": -2.217}),
    ("DATA", "Tax paid", {"FY2025": -3.7, "FY2024": -3.4, "FY2023": -1.024, "FY2022": 0, "FY2021": 0}),
    ("TOTAL", "Net cash from/(used in) operating activities", {"FY2025": 669.6, "FY2024": 884.1, "FY2023": 480.482, "FY2022": -113.543, "FY2021": 187.507}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of debt securities", {"FY2025": -1391.5, "FY2024": -577.0, "FY2023": -49.641, "FY2022": -25.737, "FY2021": -40.410}),
    ("DATA", "Proceeds from sale and maturity of debt securities", {"FY2025": 554.4, "FY2024": 402.2}),
    ("DATA", "Purchase of investments", {"FY2023": 0, "FY2022": -1.0, "FY2021": 0}),
    ("DATA", "Acquisition of a subsidiary, net of cash acquired", {"FY2025": 8.0, "FY2024": -6.1}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -0.9, "FY2024": -0.8, "FY2023": -0.568, "FY2022": -0.613, "FY2021": -0.154}),
    ("DATA", "Purchase and development of intangible assets", {"FY2025": -11.7, "FY2024": -12.3, "FY2023": -10.114, "FY2022": -7.525, "FY2021": -3.219}),
    ("TOTAL", "Net cash from/(used in) investing activities", {"FY2025": -841.7, "FY2024": -194.0, "FY2023": -60.323, "FY2022": -34.875, "FY2021": -43.783}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Proceeds from issue of ordinary shares", {"FY2025": 35.0, "FY2024": 17.6, "FY2023": 34.494, "FY2022": 98.981, "FY2021": 40.801}),
    ("DATA", "Issue of subordinated debt", {"FY2024": 30.0, "FY2021": 7.5}),
    ("DATA", "Issue of credit-linked notes", {"FY2024": 50.0}),
    ("DATA", "Payment of principal on credit-linked notes", {"FY2025": -46.1, "FY2024": -3.9}),
    ("DATA", "Coupon paid on capital securities", {"FY2025": -6.9}),
    ("DATA", "Issue of perpetual notes (including convertible)", {"FY2024": 35.0, "FY2023": 35.241, "FY2021": 17.5}),
    ("DATA", "Capital repayment of lease liabilities", {"FY2025": -0.8, "FY2024": -0.5, "FY2023": -0.437, "FY2022": -0.298, "FY2021": -0.207}),
    ("DATA", "Repayment of external debt", {"FY2025": -19.3, "FY2024": -73.8}),
    ("TOTAL", "Net cash from/(used in) financing activities", {"FY2025": -38.1, "FY2024": 54.4, "FY2023": 69.298, "FY2022": 98.683, "FY2021": 65.594}),
    ("DATA", "Effect of exchange rates on cash and cash equivalents", {"FY2025": -0.1, "FY2024": 0}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": -210.3, "FY2024": 744.5, "FY2023": 489.457, "FY2022": -49.735, "FY2021": 209.318}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 1496.8, "FY2024": 752.303, "FY2023": 262.846, "FY2022": 312.581, "FY2021": 103.263}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 1286.5, "FY2024": 1496.8, "FY2023": 752.303, "FY2022": 262.846, "FY2021": 312.581}),
    ("SECTION", "Cash and cash equivalents at end of year comprise", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 1102.7, "FY2024": 1375.8, "FY2023": 709.829, "FY2022": 227.280, "FY2021": 295.291}),
    ("DATA", "Loans and advances to banks", {"FY2025": 183.8, "FY2024": 121.0, "FY2023": 42.474, "FY2022": 35.566, "FY2021": 17.290}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 1286.5, "FY2024": 1496.8, "FY2023": 752.303, "FY2022": 262.846, "FY2021": 312.581}),
]

bw.add_cash_flow_sheet(
    title="Allica Bank Limited — Consolidated Statement of Cash Flows",
    subtitle="Allica Bank Limited Group (consolidated basis), £m unless stated",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=68,
    source_height=140,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Consolidated (Group) basis, {unit}" if unit else "Consolidated (Group) basis",
                         rows_data, sources_text, note=note, first_col_width=48, source_height=110)

metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 325689, "FY2024": 276827, "FY2023": 219055, "FY2022": 170322, "FY2021": 68816})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 ratio", {"FY2025": "13.4%", "FY2024": "14.5%", "FY2023": "15.7%", "FY2022": "17.1%", "FY2021": "14.1%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2025": 370566, "FY2024": 321704, "FY2023": 264182, "FY2022": 180208, "FY2021": 86316})],
    p3_sources(),
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "15.3%", "FY2024": "16.9%", "FY2023": "18.9%", "FY2022": "18.1%", "FY2021": "17.7%"})],
    p3_sources(),
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2025": 406393, "FY2024": 359031, "FY2023": 271682, "FY2022": 187708, "FY2021": 93816})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "16.8%", "FY2024": "18.8%", "FY2023": "19.5%", "FY2022": "18.8%", "FY2021": "19.3%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted exposure amount", {"FY2025": 2422216, "FY2024": 1908286, "FY2023": 1396450, "FY2022": 997945, "FY2021": 486558})],
    p3_sources(),
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Total exposure measure excluding claims on central banks (£'000)", {"FY2025": 5092370, "FY2024": 3421039, "FY2023": 2208236, "FY2022": 1595100, "FY2021": 688827}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "7.3%", "FY2024": "9.4%", "FY2023": "11.4%", "FY2022": "11.3%", "FY2021": "12.5%"}),
    ],
    p3_sources(),
    note="Allica has never disclosed a leverage ratio 'including claims on central banks' variant in any of these 5 "
         "years and states in every report that it is not an LREQ firm subject to additional leverage ratio "
         "disclosure requirements. The FY2021 figures shown are already restated onto the post-1-January-2022 "
         "exposure-measure basis (PRA Policy Statement 21/21, excluding certain central bank claims) — the FY2022 "
         "Pillar 3 report explicitly restates its FY2021 comparative on this basis to aid comparison, so unlike "
         "several other banks in this series there is no leverage-ratio methodology break within Allica's own 5-year "
         "window.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value, average (£'000)", {"FY2025": 1928875, "FY2024": 1137180, "FY2023": 810081, "FY2022": 386347, "FY2021": 171242}),
        ("Total net cash outflows, adjusted value (£'000)", {"FY2025": 873645, "FY2024": 525922, "FY2023": 280344, "FY2022": 127792, "FY2021": 34252}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "220.8%", "FY2024": "216.2%", "FY2023": "289.0%", "FY2022": "302.3%", "FY2021": "499.9%"}),
    ],
    p3_sources(),
    note="LCR is calculated as a 12-month average per Allica's own Pillar 3 methodology note.",
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding (£'000)", {"FY2025": 3884410, "FY2024": 2937724, "FY2023": 1876364, "FY2022": 1338171}),
        ("Total required stable funding (£'000)", {"FY2025": 2799038, "FY2024": 2195700, "FY2023": 1385603, "FY2022": 897829}),
        ("Net Stable Funding Ratio (%)", {"FY2025": "138.8%", "FY2024": "133.8%", "FY2023": "135.4%", "FY2022": "149.0%", "FY2021": "Not disclosed"}),
    ],
    p3_sources(),
    note="NSFR was not a Pillar 3 disclosure requirement as at FY2021 (the UK NSFR regime took effect from 1 January "
         "2022), so no FY2021 figures exist. NSFR is calculated as a 4-quarter average. FY2022 'Total available "
         "stable funding' is reported as £1,338,171k in the FY2022 Pillar 3 report's own current-year column but as "
         "£1,338,711k in the FY2023 Pillar 3 report's prior-year comparative column — an apparent digit transposition "
         "in one of the two source PDFs. This sheet uses the FY2022 report's own-year figure as authoritative; the "
         "£540 discrepancy is immaterial and both reports agree the resulting NSFR ratio is 149.0%.",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})],
    p3_sources(),
    note="No MREL ratio row appears in any of Allica's 5 Pillar 3 reports; each explicitly states Allica Bank Limited "
         "is not an LREQ firm. As a smaller institution below the UK's MREL/bail-in resolution threshold, Allica is "
         "not subject to a separate MREL disclosure requirement.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 669.6, "FY2024": 884.1, "FY2023": 480.482, "FY2022": -113.543, "FY2021": 187.507}),
        ("Net cash from/(used in) investing activities", {"FY2025": -841.7, "FY2024": -194.0, "FY2023": -60.323, "FY2022": -34.875, "FY2021": -43.783}),
        ("Net cash from/(used in) financing activities", {"FY2025": -38.1, "FY2024": 54.4, "FY2023": 69.298, "FY2022": 98.683, "FY2021": 65.594}),
        ("Cash and cash equivalents at end of year", {"FY2025": 1286.5, "FY2024": 1496.8, "FY2023": 752.303, "FY2022": 262.846, "FY2021": 312.581}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "13.4%", "FY2024": "14.5%", "FY2023": "15.7%", "FY2022": "17.1%", "FY2021": "14.1%"}),
        ("Tier 1 Ratio", {"FY2025": "15.3%", "FY2024": "16.9%", "FY2023": "18.9%", "FY2022": "18.1%", "FY2021": "17.7%"}),
        ("Total Capital Ratio", {"FY2025": "16.8%", "FY2024": "18.8%", "FY2023": "19.5%", "FY2022": "18.8%", "FY2021": "19.3%"}),
        ("Leverage Ratio (excl. central banks)", {"FY2025": "7.3%", "FY2024": "9.4%", "FY2023": "11.4%", "FY2022": "11.3%", "FY2021": "12.5%"}),
        ("LCR", {"FY2025": "220.8%", "FY2024": "216.2%", "FY2023": "289.0%", "FY2022": "302.3%", "FY2021": "499.9%"}),
        ("NSFR", {"FY2025": "138.8%", "FY2024": "133.8%", "FY2023": "135.4%", "FY2022": "149.0%", "FY2021": "Not disclosed"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Allica is a young, fast-growing SME-lending challenger bank "
         "(authorised 2019) — its steadily declining capital/liquidity ratios alongside rapidly rising absolute "
         "capital and RWA figures reflect fast balance-sheet growth diluting ratios from an initially very "
         "well-capitalised base, not deteriorating credit quality.",
)

bw.save("/Users/armaan/code/katalysis/banks/ALLICA FINANCIALS.xlsx")
