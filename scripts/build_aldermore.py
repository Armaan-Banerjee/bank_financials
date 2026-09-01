import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Aldermore Bank PLC (Companies House 00947662, FRN 204503) reports to a
# 30 June fiscal year end - "FY2025" below means the year ended 30 June 2025.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {
    "FY2025": "FY2025 (y/e 30 Jun 25)",
    "FY2024": "FY2024 (y/e 30 Jun 24)",
    "FY2023": "FY2023 (y/e 30 Jun 23)",
    "FY2022": "FY2022 (y/e 30 Jun 22)",
    "FY2021": "FY2021 (y/e 30 Jun 21)",
}

CH_2025_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzQ4NzM5MDg2MWFkaXF6a2N4/document?format=pdf&download=0"
CH_2024_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzQ0MDgwMDc3OWFkaXF6a2N4/document?format=pdf&download=0"
CH_2023_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzM5ODA0OTgzOWFkaXF6a2N4/document?format=pdf&download=0"
CH_2022_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzM1NTc2ODMxMmFkaXF6a2N4/document?format=pdf&download=0"
CH_2021_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzMxODkyMzc2MWFkaXF6a2N4/document?format=pdf&download=0"

P3_2025_URL = "https://www.aldermore.co.uk/media/sgufisw5/aldermore-group-plc-2025-pillar-3-disclosures.pdf"
P3_2024_URL = "https://www.aldermore.co.uk/media/jkkdbgnu/aldermore-group-plc-2024-pillar-3-disclosures.pdf"
P3_2022_URL = "https://www.aldermore.co.uk/media/hnhpw03l/pillar-3-2022_0.pdf"
INTERIM_P3_2025_URL = "https://www.aldermore.co.uk/media/xx1fg0me/half-year-pillar-3-disclosures-31-dec-2025.pdf"

CASH_FLOW_SOURCES = (
    "Sources — Aldermore Bank PLC (company solo, not the Aldermore Group PLC holding company), "
    "Statement of cash flows from each year's full statutory accounts filed at Companies House "
    "(company no. 00947662), £m:\n"
    f"FY2025 & FY2024 (restated): Full accounts made up to 30 June 2025, filed 04 Nov 2025, p.55 — {CH_2025_URL}\n"
    f"FY2023: Full accounts made up to 30 June 2023, filed 27 Oct 2023, p.53 — {CH_2023_URL}\n"
    f"FY2022: Full accounts made up to 30 June 2022, filed 19 Oct 2022, p.60 — {CH_2022_URL}\n"
    f"FY2021: Full accounts made up to 30 June 2021, filed 04 Nov 2021, p.59 — {CH_2021_URL}\n"
    "(FY2024 accounts as originally filed are superseded by the FY2025 accounts' restated FY2024 comparative used here — "
    f"{CH_2024_URL})\n"
    "Note: the Bank reclassified its FY2024 comparative cash flow statement (see FY2025 accounts, p.55) to move interest "
    "received/paid on the intercompany loan, interest paid on subordinated notes, and interest received on debt "
    "securities from investing/financing activities into operating activities, and to reclassify proceeds from disposal "
    "of a non-current asset held for sale into operating activities; amounts relating to intercompany loans are also now "
    "presented gross rather than net. FY2023/FY2022/FY2021 below are presented as originally filed under the older "
    "(pre-reclassification) basis. Blank cells indicate a line item was not part of that year's classification of cash "
    "flows; section totals (net cash from operating/investing/financing activities, net change, opening/closing cash) "
    "are directly as reported and comparable across all 5 years. Minor (≤£0.1m) differences between individual line "
    "items and their printed subtotals in the FY2023/FY2022 source documents are presented as disclosed, not adjusted."
)

def p3_sources(page_25="4", page_24="4", page_22="4"):
    return (
        "Sources — Aldermore Bank PLC solo figures from the 'Key metrics' table (Bank columns), Aldermore Group PLC "
        "Pillar 3 Disclosures:\n"
        f"FY2025 & FY2024: Pillar 3 Disclosures for the year ended 30 June 2025, p.{page_25} (Key metrics) — {P3_2025_URL}\n"
        f"FY2023: Pillar 3 Disclosures for the year ended 30 June 2024, p.{page_24} (Key metrics, FY2023 comparative) — {P3_2024_URL}\n"
        f"FY2022 & FY2021: Pillar 3 Disclosures for the year ended 30 June 2022, p.{page_22} (Key metrics) — {P3_2022_URL}"
    )

bw = BankWorkbook(bank_name="Aldermore Bank PLC", years=YEARS, year_label=YEAR_LABEL, header_color="AD1457")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Reconciliation of profit before tax to net cash flows from operating activities", {}),
    ("DATA", "Profit before taxation", {"FY2025": 220.7, "FY2024": 218.2, "FY2023": 171.2, "FY2022": 160.7, "FY2021": 115.7}),
    ("DATA", "Adjustments for non-cash items and other adjustments included within the income statement", {"FY2025": -223.6, "FY2024": -188.9, "FY2023": -49.2, "FY2022": -22.3, "FY2021": 17.0}),
    ("DATA", "Change/(increase) in operating assets", {"FY2025": -1145.9, "FY2024": -439.9, "FY2023": -519.2, "FY2022": -389.0, "FY2021": 265.0}),
    ("DATA", "Change/increase in operating liabilities", {"FY2025": 283.3, "FY2024": 992.8, "FY2023": 1539.6, "FY2022": 1526.0, "FY2021": 498.4}),
    ("DATA", "Interest received on intercompany loan (operating basis, FY2024-FY2025)", {"FY2025": 164.5, "FY2024": 135.8}),
    ("DATA", "Interest paid on intercompany loan (operating basis, FY2024-FY2025)", {"FY2025": -53.9, "FY2024": -38.0}),
    ("DATA", "Interest paid on subordinated notes (operating basis, FY2024-FY2025)", {"FY2025": -7.9, "FY2024": -6.4}),
    ("DATA", "Interest received on debt securities (operating basis, FY2024-FY2025)", {"FY2025": 95.2, "FY2024": 86.3}),
    ("DATA", "Proceeds from disposal of non-current assets held for sale (operating basis, FY2024-FY2025)", {"FY2025": 0, "FY2024": 32.8}),
    ("DATA", "Income tax paid", {"FY2025": -57.4, "FY2024": -62.6, "FY2023": -33.9, "FY2022": -59.7, "FY2021": -12.0}),
    ("TOTAL", "Net cash flows (used in)/generated from operating activities", {"FY2025": -725.0, "FY2024": 730.1, "FY2023": 1108.5, "FY2022": 1215.7, "FY2021": 884.1}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of debt securities", {"FY2025": -1618.2, "FY2024": -1184.9, "FY2023": -358.2, "FY2022": -723.4, "FY2021": -444.6}),
    ("DATA", "Proceeds from sale and/or maturity of debt securities", {"FY2025": 1278.3, "FY2024": 421.2, "FY2023": 299.3, "FY2022": 159.6, "FY2021": 333.1}),
    ("DATA", "Capital repayments of debt securities", {"FY2025": 81.4, "FY2024": 367.2, "FY2023": 351.3, "FY2022": 223.3, "FY2021": 61.4}),
    ("DATA", "Interest received on debt securities (investing basis, FY2021-FY2023)", {"FY2023": 15.2, "FY2022": 7.6, "FY2021": 6.8}),
    ("DATA", "Purchase of property, plant and equipment and intangible assets", {"FY2025": -1.0, "FY2024": -5.1, "FY2023": -1.0, "FY2022": -1.9, "FY2021": -11.7}),
    ("TOTAL", "Net cash flows (used in)/generated from investing activities", {"FY2025": -259.5, "FY2024": -401.6, "FY2023": 306.5, "FY2022": -334.8, "FY2021": -55.0}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Repayment of subordinated debt", {"FY2024": -100.0, "FY2022": -60.0}),
    ("DATA", "Proceeds from issue of subordinated debt", {"FY2024": 100.0}),
    ("DATA", "Redemption of Additional Tier 1 Capital", {"FY2025": -61.0}),
    ("DATA", "Issuance of Additional Tier 1 Capital", {"FY2025": 50.0}),
    ("DATA", "Capital repayments on debt securities issued", {"FY2023": 0.4}),
    ("DATA", "Amounts paid on new intercompany loan", {"FY2023": -394.3, "FY2022": -694.4, "FY2021": -686.2}),
    ("DATA", "Interest received on intercompany loan (financing basis, FY2021-FY2023)", {"FY2023": 68.0, "FY2022": 30.3, "FY2021": 20.1}),
    ("DATA", "Deposit placed by related Group companies", {"FY2021": -12.3}),
    ("DATA", "Coupons paid on Additional Tier 1 capital", {"FY2025": -5.1, "FY2024": -5.3, "FY2023": -5.2, "FY2022": -5.2, "FY2021": -5.2}),
    ("DATA", "Interest paid on subordinated notes (financing basis, FY2021-FY2023)", {"FY2022": -7.4, "FY2021": -9.9}),
    ("DATA", "Repayment of lease liabilities - principal", {"FY2025": -2.3, "FY2024": -3.0, "FY2022": -2.8, "FY2021": -4.0}),
    ("DATA", "Interest paid on lease liabilities", {"FY2023": -0.1, "FY2022": -0.1, "FY2021": -0.2}),
    ("TOTAL", "Net cash generated/(used in) financing activities", {"FY2025": -18.4, "FY2024": -8.3, "FY2023": -331.2, "FY2022": -739.7, "FY2021": -697.7}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -1002.9, "FY2024": 320.2, "FY2023": 1083.8, "FY2022": 141.2, "FY2021": 131.4}),
    ("DATA", "Cash and cash equivalents at start of the period", {"FY2025": 2219.6, "FY2024": 1899.4, "FY2023": 815.1, "FY2022": 674.0, "FY2021": 542.6}),
    ("TOTAL", "Cash and cash equivalents at end of the period", {"FY2025": 1216.7, "FY2024": 2219.6, "FY2023": 1899.4, "FY2022": 815.2, "FY2021": 674.0}),
]

bw.add_cash_flow_sheet(
    title="Aldermore Bank PLC — Statement of Cash Flows",
    subtitle="Company (Bank solo) basis, £m, year ended 30 June",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=72,
    source_height=140,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Bank solo basis, {unit}" if unit else "Bank solo basis",
                         rows_data, sources_text, note=note, first_col_width=46, source_height=110)

metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 1337.8, "FY2024": 1321.5, "FY2023": 1203.8, "FY2022": 1065.9, "FY2021": 947.0})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 ratio", {"FY2025": "18.4%", "FY2024": "19.2%", "FY2023": "18.5%", "FY2022": "17.0%", "FY2021": "15.9%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 1387.8, "FY2024": 1382.5, "FY2023": 1264.8, "FY2022": 1126.6, "FY2021": 1008.0})],
    p3_sources(),
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "19.1%", "FY2024": "20.1%", "FY2023": "19.4%", "FY2022": "18.0%", "FY2021": "16.9%"})],
    p3_sources(),
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 1487.8, "FY2024": 1482.5, "FY2023": 1364.8, "FY2022": 1226.6, "FY2021": 1168.0})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "20.5%", "FY2024": "21.6%", "FY2023": "21.0%", "FY2022": "19.6%", "FY2021": "19.6%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted assets (RWA)", {"FY2025": 7271.6, "FY2024": 6875.6, "FY2023": 6504.9, "FY2022": 6260.1, "FY2021": 5964.1})],
    p3_sources(),
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total exposure measure excluding claims on central banks (£m)", {"FY2025": 15674.3, "FY2024": 14337.2, "FY2023": 13609.6, "FY2022": 13850.3, "FY2021": "n/a"}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "8.9%", "FY2024": "9.6%", "FY2023": "9.3%", "FY2022": "8.1%", "FY2021": "n/a"}),
    ],
    p3_sources(),
    note="FY2021 leverage ratio disclosure basis was introduced from 1 January 2022; the FY2022 Pillar 3 report explicitly "
         "marks FY2021 as 'n/a' with no comparative provided under the new template.",
)

metric(
    "LCR", "£m / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value average (£m)", {"FY2025": 3723.1, "FY2024": 4208.6, "FY2023": 3280.6, "FY2022": 2838.5, "FY2021": "n/a"}),
        ("Total net cash outflows, adjusted value (£m)", {"FY2025": 1968.3, "FY2024": 1959.4, "FY2023": 1686.4, "FY2022": 772.6, "FY2021": "n/a"}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "189.2%", "FY2024": "214.8%", "FY2023": "194.5%", "FY2022": "367.4%", "FY2021": "n/a"}),
    ],
    p3_sources(),
    note="LCR is computed as a 12-month average to the period end. FY2021 is 'n/a' — no comparative was provided under "
         "the disclosure template introduced from 1 January 2022 (see FY2022 Pillar 3 report).",
)

metric(
    "NSFR", "£m / %",
    [
        ("Total available stable funding (£m)", {"FY2025": 15972.4, "FY2024": 16133.4, "FY2023": 15490.2, "FY2022": 15667.6, "FY2021": "n/a"}),
        ("Total required stable funding (£m)", {"FY2025": 12166.9, "FY2024": 11778.0, "FY2023": 12161.3, "FY2022": 12169.6, "FY2021": "n/a"}),
        ("Net Stable Funding Ratio (%)", {"FY2025": "131.3%", "FY2024": "137.0%", "FY2023": "127.4%", "FY2022": "128.7%", "FY2021": "n/a"}),
    ],
    p3_sources(),
    note="NSFR is computed as a 4-quarter average to the period end. FY2021 is 'n/a' — no comparative was provided under "
         "the disclosure template introduced from 1 January 2022 (see FY2022 Pillar 3 report).",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})],
    p3_sources(),
    note="MREL is not disclosed for Aldermore Bank PLC/Aldermore Group PLC in any Pillar 3 report reviewed — the Group "
         "sits below the balance-sheet threshold at which the Bank of England sets a bail-in MREL requirement above "
    "minimum capital requirements, so no separate MREL ratio is published.",
)

# ---------------------------------------------------------------
# Interim Pillar 3 disclosures
# ---------------------------------------------------------------
INTERIM_HEADERS = [
    "Period",
    "Disclosure type",
    "Metric",
    "Value",
    "Unit",
    "Basis",
    "Source document",
    "Page / table",
]

INTERIM_PERIODS = [
    ("31 Dec 2025", "H1 2025 interim (current period)"),
    ("30 Jun 2025", "H1 2025 interim (comparative)"),
    ("31 Dec 2024", "H1 2025 interim (comparative)"),
]

INTERIM_METRICS = [
    ("CET1 capital", [1342.5, 1337.8, 1306.1], "£m"),
    ("Tier 1 capital", [1392.5, 1387.8, 1367.1], "£m"),
    ("Total capital", [1692.5, 1487.8, 1467.1], "£m"),
    ("Total risk-weighted exposure amount", [7352.0, 7271.6, 6997.3], "£m"),
    ("CET1 ratio", ["18.3%", "18.4%", "18.7%"], "%"),
    ("Tier 1 ratio", ["18.9%", "19.1%", "19.5%"], "%"),
    ("Total capital ratio", ["23.0%", "20.5%", "21.0%"], "%"),
    ("Total exposure measure excluding claims on central banks", [15369.1, 15526.0, 14826.8], "£m"),
    ("Leverage ratio excluding claims on central banks", ["9.1%", "8.9%", "9.2%"], "%"),
    ("Total high-quality liquid assets (HQLA), weighted-value average", [3518.6, 3723.1, 4062.3], "£m"),
    ("Total net cash outflows (adjusted value)", [1964.8, 1968.3, 2047.1], "£m"),
    ("Liquidity coverage ratio", ["179.1%", "189.2%", "198.4%"], "%"),
    ("Total available stable funding", [16221.9, 15972.4, 16013.1], "£m"),
    ("Total required stable funding", [12699.7, 12166.9, 11856.4], "£m"),
    ("NSFR ratio", ["127.7%", "131.3%", "135.1%"], "%"),
    ("MREL ratio", ["Not disclosed", "Not disclosed", "Not disclosed"], "%"),
]

interim_rows = []
for period_index, (period, disclosure_type) in enumerate(INTERIM_PERIODS):
    for metric_name, values, unit in INTERIM_METRICS:
        interim_rows.append(
            [
                period,
                disclosure_type,
                metric_name,
                values[period_index],
                unit,
                "Aldermore Bank PLC (Bank solo)",
                "Aldermore Group PLC Interim Pillar 3 Disclosure — 31 December 2025",
                "p.4, Key Metrics (Bank column)",
            ]
        )

interim_hyperlinks = {(i, 6): INTERIM_P3_2025_URL for i in range(len(interim_rows))}
bw.add_wide_interim_sheet(
    "Interim Pillar 3",
    rows=interim_rows,
    hyperlink_cells=interim_hyperlinks,
    title="Aldermore Bank PLC — Interim Pillar 3",
    subtitle="Bank solo basis; amounts in £m and ratios in %, as disclosed in the official interim Key Metrics table",
    note=(
        "Source: Aldermore Group PLC Interim Pillar 3 Disclosure as at 31 December 2025, p.4, Key Metrics — Bank column. "
        f"Official PDF: {INTERIM_P3_2025_URL}\n"
        "The document reports 31 Dec 2025 and comparative 30 Jun 2025 and 31 Dec 2024 figures. No separate official "
        "half-year Pillar 3 document was located in the archive for 2021, 2022, 2023, or 2024; those periods are therefore "
        "not inferred or backfilled. MREL is not included in the Key Metrics table and is recorded as not disclosed."
    ),
)
# Keep the source register immediately after the matrix so the current
# verifier can discover it without changing the shared helper.
interim_ws = bw.wb["Interim Pillar 3"]
interim_ws.delete_rows(5 + len({row[2] for row in interim_rows}), 2)
for row_number in range(5, interim_ws.max_row + 1):
    if interim_ws.cell(row=row_number, column=1).value == "Source register":
        source_register_row = row_number
        break
    for column_number in range(4, interim_ws.max_column + 1):
        cell = interim_ws.cell(row=row_number, column=column_number)
        if cell.value not in (None, ""):
            cell.hyperlink = INTERIM_P3_2025_URL
            cell.style = "Hyperlink"
for row_number in range(source_register_row + 2, interim_ws.max_row + 1):
    if interim_ws.cell(row=row_number, column=1).value in (None, ""):
        break
    source_cell = interim_ws.cell(row=row_number, column=3)
    source_cell.hyperlink = INTERIM_P3_2025_URL
    source_cell.style = "Hyperlink"

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from operating activities", {"FY2025": -725.0, "FY2024": 730.1, "FY2023": 1108.5, "FY2022": 1215.7, "FY2021": 884.1}),
        ("Net cash from investing activities", {"FY2025": -259.5, "FY2024": -401.6, "FY2023": 306.5, "FY2022": -334.8, "FY2021": -55.0}),
        ("Net cash from financing activities", {"FY2025": -18.4, "FY2024": -8.3, "FY2023": -331.2, "FY2022": -739.7, "FY2021": -697.7}),
        ("Cash and cash equivalents at end of year", {"FY2025": 1216.7, "FY2024": 2219.6, "FY2023": 1899.4, "FY2022": 815.2, "FY2021": 674.0}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "18.4%", "FY2024": "19.2%", "FY2023": "18.5%", "FY2022": "17.0%", "FY2021": "15.9%"}),
        ("Tier 1 Ratio", {"FY2025": "19.1%", "FY2024": "20.1%", "FY2023": "19.4%", "FY2022": "18.0%", "FY2021": "16.9%"}),
        ("Total Capital Ratio", {"FY2025": "20.5%", "FY2024": "21.6%", "FY2023": "21.0%", "FY2022": "19.6%", "FY2021": "19.6%"}),
        ("Leverage Ratio", {"FY2025": "8.9%", "FY2024": "9.6%", "FY2023": "9.3%", "FY2022": "8.1%"}),
        ("LCR", {"FY2025": "189.2%", "FY2024": "214.8%", "FY2023": "194.5%", "FY2022": "367.4%"}),
        ("NSFR", {"FY2025": "131.3%", "FY2024": "137.0%", "FY2023": "127.4%", "FY2022": "128.7%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Fiscal year ends 30 June. Cash flow statement uses Bank-solo "
         "figures; Pillar 3 ratios use the Bank-solo columns of Aldermore Group PLC's Pillar 3 disclosures (the only "
         "level at which Pillar 3 is published). Leverage/LCR/NSFR have no FY2021 figure — see the Leverage Ratio/LCR/"
         "NSFR sheets for the disclosure-template basis note.",
)

bw.save("/Users/armaan/code/katalysis/banks/ALDERMORE FINANCIALS.xlsx")
