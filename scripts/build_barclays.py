import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first

AR25_URL = "https://home.barclays/content/dam/home-barclays/documents/investor-relations/reports-and-events/annual-reports/2025/Barclays-Bank-UK-PLC-Annual-Report-2025.pdf"
AR23_URL = "https://home.barclays/content/dam/home-barclays/documents/investor-relations/reports-and-events/annual-reports/2023/Barclays-Bank-UK-Annual-Report-2023-Results-committee.pdf"
AR21_URL = "https://home.barclays/content/dam/home-barclays/documents/investor-relations/reports-and-events/annual-reports/2021/Barclays-Bank-UK-PLC-2021-Annual-Report.pdf"

P3_25_URL = "https://home.barclays/content/dam/home-barclays/documents/investor-relations/ResultAnnouncements/FullYear2025Results/FY25-BBUKPLC-Pillar-3.pdf"
P3_23_URL = "https://home.barclays/content/dam/home-barclays/documents/investor-relations/reports-and-events/annual-reports/2023/BB-UK-Pillar-3-Report-2023.pdf"
P3_21_URL = "https://home.barclays/content/dam/home-barclays/documents/investor-relations/reports-and-events/annual-reports/2021/Barclays-Bank-UK-PLC-Pillar-3-Report-2021.pdf"

CASH_FLOW_SOURCES = (
    "Sources — all figures are Barclays Bank UK Group consolidated cash flow statement, £m:\n"
    f"FY2025 & FY2024: Barclays Bank UK PLC Annual Report 2025, p.201 (Consolidated cash flow statement) — {AR25_URL}\n"
    f"FY2023 & FY2022: Barclays Bank UK PLC Annual Report 2023, p.166 (Consolidated cash flow statement) — {AR23_URL}\n"
    f"FY2021: Barclays Bank UK PLC Annual Report 2021, p.138 (Consolidated cash flow statement) — {AR21_URL}\n"
    "Note: Barclays changed cash flow statement presentation granularity across these report vintages "
    "(e.g. FY2025/FY2024 split some line items — such as repurchase/reverse repurchase agreements and trading "
    "portfolio assets/liabilities — that FY2023/FY2022/FY2021 report on a combined basis). Blank cells indicate "
    "that year's report did not disclose that specific split; where a coarser combined figure was reported instead, "
    "it appears on its own row. Section totals (net cash from operating/investing/financing activities, "
    "cash and cash equivalents) are consistent and comparable across all 5 years."
)

def p3_sources(part_label_25="Table 6: KM1 - Key metrics - Part 1", page_25="11",
               part_label_23="Table 6: UK KM1 - Key metrics - Part 1", page_23="11",
               part_label_21="Table 4: Key Metrics (KM1 / IFRS 9-FL)", page_21="9"):
    return (
        "Sources — Barclays Bank UK Group consolidated (Pillar 3) basis:\n"
        f"FY2025 & FY2024: Barclays Bank UK PLC Pillar 3 Report 2025, p.{page_25} ({part_label_25}) — {P3_25_URL}\n"
        f"FY2023 & FY2022: Barclays Bank UK PLC Pillar 3 Report 2023, p.{page_23} ({part_label_23}) — {P3_23_URL}\n"
        f"FY2021: Barclays Bank UK PLC Pillar 3 Report 2021, p.{page_21} ({part_label_21}) — {P3_21_URL}"
    )

bw = BankWorkbook(bank_name="Barclays Bank UK Group", years=YEARS, header_color="1F3864")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Reconciliation of profit before tax to net cash flows from operating activities", {}),
    ("DATA", "Profit before tax", {"FY2025": 3325, "FY2024": 3560, "FY2023": 2671, "FY2022": 2552, "FY2021": 2163}),
    ("DATA", "Credit impairment charges/(releases)", {"FY2025": 393, "FY2024": 352, "FY2023": 308, "FY2022": 268, "FY2021": -371}),
    ("DATA", "Depreciation, amortisation and impairment of property, plant, equipment and intangibles", {"FY2025": 97, "FY2024": 95, "FY2023": 146, "FY2022": 187, "FY2021": 169}),
    ("DATA", "Loss on disposal of subsidiaries", {"FY2023": 124, "FY2022": 0}),
    ("DATA", "Other provisions (including pensions where noted)", {"FY2025": 144, "FY2024": 68, "FY2023": 69, "FY2022": 47, "FY2021": 25}),
    ("DATA", "Other non-cash items / exchange rate movements", {"FY2025": 375, "FY2024": 228, "FY2023": 2401, "FY2022": -878, "FY2021": -480}),
    ("SECTION", "Changes in operating assets and liabilities", {}),
    ("DATA", "Net (increase)/decrease in cash collateral and settlement balances", {"FY2025": -944, "FY2024": 414, "FY2023": 1108, "FY2022": 335, "FY2021": 322}),
    ("DATA", "Net (increase)/decrease in loans and advances at amortised cost", {"FY2025": -9592, "FY2024": 3023, "FY2023": 4402, "FY2022": 2893, "FY2021": -4591}),
    ("DATA", "Net (increase) in reverse repurchase agreements and other similar secured lending", {"FY2025": -107, "FY2024": -2327}),
    ("DATA", "Net (decrease)/increase in repurchase agreements and other similar secured borrowing", {"FY2025": -1906, "FY2024": 241}),
    ("DATA", "Repurchase and reverse repurchase agreements (combined, as reported)", {"FY2023": -5527, "FY2022": -870, "FY2021": 11050}),
    ("DATA", "Net increase/(decrease) in deposits at amortised cost", {"FY2025": 330, "FY2024": -3686, "FY2023": -17016, "FY2022": -2615, "FY2021": 20197}),
    ("DATA", "Net increase/(decrease) in debt securities in issue", {"FY2025": 2084, "FY2024": -1242, "FY2023": -4702, "FY2022": -675, "FY2021": 1181}),
    ("DATA", "Net decrease/(increase) in derivative financial instruments", {"FY2025": 906, "FY2024": -413, "FY2023": -1519, "FY2022": 427, "FY2021": -406}),
    ("DATA", "Net (increase) in trading portfolio assets", {"FY2025": -143, "FY2024": -199}),
    ("DATA", "Net increase/(decrease) in trading portfolio liabilities", {"FY2025": 182, "FY2024": -182}),
    ("DATA", "Trading assets and liabilities (combined, as reported)", {"FY2023": 455, "FY2022": -299, "FY2021": -258}),
    ("DATA", "Net decrease in financial assets at fair value through the income statement", {"FY2025": 130, "FY2024": 173}),
    ("DATA", "Net (decrease)/increase in financial liabilities designated at fair value", {"FY2025": -1845, "FY2024": 2652}),
    ("DATA", "Financial assets and liabilities at fair value through the income statement (combined, as reported)", {"FY2023": 264, "FY2022": 787, "FY2021": 665}),
    ("DATA", "Net (increase) in other assets and liabilities", {"FY2025": -215, "FY2024": -276, "FY2023": -52, "FY2022": -298, "FY2021": -299}),
    ("DATA", "Corporate income tax paid", {"FY2025": -1074, "FY2024": -522, "FY2023": -583, "FY2022": -395, "FY2021": -53}),
    ("TOTAL", "Net cash from operating activities", {"FY2025": -7860, "FY2024": 1959, "FY2023": -17451, "FY2022": 1466, "FY2021": 29314}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of debt securities at amortised cost", {"FY2025": -3727, "FY2024": -4615}),
    ("DATA", "Proceeds from redemption or sale of debt securities at amortised cost", {"FY2025": 8061, "FY2024": 3932}),
    ("DATA", "Debt securities at amortised cost (net, as reported)", {"FY2023": -178, "FY2022": -5796, "FY2021": -3695}),
    ("DATA", "Purchase of financial assets at fair value through other comprehensive income", {"FY2025": -20764, "FY2024": -21343}),
    ("DATA", "Proceeds from sale or redemption of financial assets at fair value through other comprehensive income", {"FY2025": 16812, "FY2024": 14959}),
    ("DATA", "Financial assets at fair value through other comprehensive income (net, as reported)", {"FY2023": -304, "FY2022": -6792, "FY2021": 10125}),
    ("DATA", "Financial liabilities designated at fair value (net, as reported)", {"FY2023": 196, "FY2022": 0}),
    ("DATA", "Purchase of property, plant and equipment and investment in intangibles", {"FY2025": -52, "FY2024": -13, "FY2023": -25, "FY2022": -13, "FY2021": 0}),
    ("DATA", "Acquisition of business, net of cash acquired", {"FY2025": 0, "FY2024": -228}),
    ("DATA", "Acquisition of subsidiaries, net of cash acquired", {"FY2023": -2378, "FY2022": 0}),
    ("DATA", "Disposal of subsidiaries, net of cash disposed", {"FY2023": -141, "FY2022": 0}),
    ("TOTAL", "Net cash from investing activities", {"FY2025": 330, "FY2024": -7308, "FY2023": -2830, "FY2022": -12601, "FY2021": 6430}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividends paid and other coupon payments on equity instruments", {"FY2025": -1639, "FY2024": -1173, "FY2023": -1482, "FY2022": -1888, "FY2021": -683}),
    ("DATA", "Capital contribution from Barclays PLC", {"FY2021": 0}),
    ("DATA", "Issuance of subordinated liabilities/debt", {"FY2025": 3600, "FY2024": 2277, "FY2023": 4393, "FY2022": 829, "FY2021": 1025}),
    ("DATA", "Redemption of subordinated liabilities/debt", {"FY2025": -2703, "FY2024": -372, "FY2023": -1136, "FY2022": -2017, "FY2021": -1116}),
    ("DATA", "Issue of shares and other equity instruments", {"FY2025": 990, "FY2024": 618, "FY2023": 619, "FY2022": 0}),
    ("DATA", "Repurchase/redemption of shares and other equity instruments", {"FY2025": -1188, "FY2024": -622, "FY2023": -750, "FY2022": 0}),
    ("DATA", "Lease liability payments", {"FY2025": -41, "FY2024": -53, "FY2023": -63, "FY2022": -71}),
    ("DATA", "Vesting of employee share schemes", {"FY2025": -28, "FY2024": -15, "FY2023": -16, "FY2022": -14, "FY2021": -11}),
    ("DATA", "Effect of exchange rates on cash and cash equivalents", {"FY2021": 0}),
    ("TOTAL", "Net cash from financing activities", {"FY2025": -1009, "FY2024": 660, "FY2023": 1565, "FY2022": -3161, "FY2021": -785}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -8539, "FY2024": -4689, "FY2023": -18716, "FY2022": -14296, "FY2021": 34959}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 35675, "FY2024": 40364, "FY2023": 59080, "FY2022": 73376, "FY2021": 38417}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 27136, "FY2024": 35675, "FY2023": 40364, "FY2022": 59080, "FY2021": 73376}),
    ("SECTION", "Cash and cash equivalents at end of year comprise", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 21208, "FY2024": 29819, "FY2023": 34948, "FY2022": 54208, "FY2021": 69488}),
    ("DATA", "Loans and advances to banks with original maturity less than three months", {"FY2025": 178, "FY2024": 231, "FY2023": 291, "FY2022": 347, "FY2021": 46}),
    ("DATA", "Cash collateral balances with central banks with original maturity less than three months", {"FY2025": 5750, "FY2024": 5625, "FY2023": 5125, "FY2022": 4525, "FY2021": 3842}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 27136, "FY2024": 35675, "FY2023": 40364, "FY2022": 59080, "FY2021": 73376}),
]

bw.add_cash_flow_sheet(
    title="Barclays Bank UK PLC — Consolidated Cash Flow Statement",
    subtitle="Barclays Bank UK Group (consolidated basis), £m unless stated",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=70,
    source_height=90,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Consolidated basis, {unit}" if unit else "Consolidated basis",
                         rows_data, sources_text, note=note, first_col_width=42, source_height=90)

metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 12331, "FY2024": 11895, "FY2023": 10638, "FY2022": 10701, "FY2021": 10828})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "14.5%", "FY2024": "14.2%", "FY2023": "14.8%", "FY2022": "14.7%", "FY2021": "15.2%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 14558, "FY2024": 14320, "FY2023": 13067, "FY2022": 13261, "FY2021": 13388})],
    p3_sources(),
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "17.1%", "FY2024": "17.1%", "FY2023": "18.1%", "FY2022": "18.2%", "FY2021": "18.8%"})],
    p3_sources(),
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 16996, "FY2024": 17155, "FY2023": 15596, "FY2022": 15828, "FY2021": 16442})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "20.0%", "FY2024": "20.5%", "FY2023": "21.6%", "FY2022": "21.8%", "FY2021": "23.1%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted exposure amount", {"FY2025": 85065, "FY2024": 83639, "FY2023": 72102, "FY2022": 72719, "FY2021": 71213})],
    p3_sources(),
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total exposure measure excluding claims on central banks (£m)", {"FY2025": 277958, "FY2024": 268452, "FY2023": 250163, "FY2022": 250092, "FY2021": 241173}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "5.2%", "FY2024": "5.3%", "FY2023": "5.2%", "FY2022": "5.3%", "FY2021": "5.6%"}),
        ("Leverage ratio including claims on central banks (%)", {"FY2025": "4.8%", "FY2024": "4.7%", "FY2023": "4.5%", "FY2022": "4.3%", "FY2021": "4.1%"}),
    ],
    p3_sources(part_label_25="Table 6: KM1 - Key metrics - Part 2", page_25="12",
               part_label_23="Table 6: KM1 - Key metrics - Part 2", page_23="12",
               part_label_21="Table 4: Key Metrics (KM1 / IFRS 9-FL)", page_21="9"),
    note="FY2021 exposure/ratios use the 'UK leverage ratio (Transitional)' and 'CRR leverage ratio (Transitional)' rows "
         "from the 2021 Pillar 3 report as the closest equivalents to the 'excluding'/'including claims on central banks' "
         "framing introduced in later reports.",
)

metric(
    "LCR", "£m / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value (£m)", {"FY2025": 64552, "FY2024": 68446, "FY2023": 68533, "FY2022": 81791, "FY2021": 85092}),
        ("Total net cash outflows, adjusted value (£m)", {"FY2025": 34613, "FY2024": 33879, "FY2023": 38057, "FY2022": 43966, "FY2021": 41690}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "186.6%", "FY2024": "202.0%", "FY2023": "180%", "FY2022": "186%", "FY2021": "204%"}),
    ],
    p3_sources(part_label_25="Table 6: KM1 - Key metrics - Part 2", page_25="12",
               part_label_23="Table 6: KM1 - Key metrics - Part 2", page_23="12",
               part_label_21="Table 4: Key Metrics (KM1 / IFRS 9-FL)", page_21="9"),
    note="LCR is computed as a trailing average of the last 12 month-end observations.",
)

metric(
    "NSFR", "£m / %",
    [
        ("Total available stable funding (£m)", {"FY2025": 257230, "FY2024": 254755, "FY2023": 258620, "FY2022": 266421}),
        ("Total required stable funding (£m)", {"FY2025": 168761, "FY2024": 160041, "FY2023": 156588, "FY2022": 158156}),
        ("Net Stable Funding Ratio (%)", {"FY2025": "152.4%", "FY2024": "159.3%", "FY2023": "165%", "FY2022": "168%", "FY2021": "Not disclosed"}),
    ],
    p3_sources(part_label_25="Table 6: KM1 - Key metrics - Part 2", page_25="12",
               part_label_23="Table 6: KM1 - Key metrics - Part 2", page_23="12",
               part_label_21="Table 4: Key Metrics (KM1 / IFRS 9-FL)", page_21="9"),
    note="NSFR is computed as a trailing average of the last four spot quarter-end positions. It was not a Pillar 3 "
         "disclosure requirement as at FY2021 (the UK NSFR regime took effect from 1 January 2022), so no FY2021 figures "
         "are available.",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not disclosed at this level" for y in YEARS})],
    p3_sources(),
    note="MREL disclosures are not applicable for Barclays Bank UK Group (the ring-fenced entity) in any of the five "
         "years reviewed; MREL is disclosed at the Barclays PLC group level instead (see Barclays PLC Pillar 3 Report, "
         "Table 21: TLAC2).",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from operating activities", {"FY2025": -7860, "FY2024": 1959, "FY2023": -17451, "FY2022": 1466, "FY2021": 29314}),
        ("Net cash from investing activities", {"FY2025": 330, "FY2024": -7308, "FY2023": -2830, "FY2022": -12601, "FY2021": 6430}),
        ("Net cash from financing activities", {"FY2025": -1009, "FY2024": 660, "FY2023": 1565, "FY2022": -3161, "FY2021": -785}),
        ("Cash and cash equivalents at end of year", {"FY2025": 27136, "FY2024": 35675, "FY2023": 40364, "FY2022": 59080, "FY2021": 73376}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "14.5%", "FY2024": "14.2%", "FY2023": "14.8%", "FY2022": "14.7%", "FY2021": "15.2%"}),
        ("Tier 1 Ratio", {"FY2025": "17.1%", "FY2024": "17.1%", "FY2023": "18.1%", "FY2022": "18.2%", "FY2021": "18.8%"}),
        ("Total Capital Ratio", {"FY2025": "20.0%", "FY2024": "20.5%", "FY2023": "21.6%", "FY2022": "21.8%", "FY2021": "23.1%"}),
        ("Leverage Ratio", {"FY2025": "5.2%", "FY2024": "5.3%", "FY2023": "5.2%", "FY2022": "5.3%", "FY2021": "5.6%"}),
        ("LCR", {"FY2025": "186.6%", "FY2024": "202.0%", "FY2023": "180%", "FY2022": "186%", "FY2021": "204%"}),
        ("NSFR", {"FY2025": "152.4%", "FY2024": "159.3%", "FY2023": "165%", "FY2022": "168%", "FY2021": "Not disclosed"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. Leverage ratio shown on the 'excluding claims on "
         "central banks' basis for comparability across years (see Leverage Ratio sheet for the 'including' "
         "variant and FY2021 basis note).",
)

bw.save("/Users/armaan/code/katalysis/banks/BARCLAYS FINANCIALS.xlsx")
