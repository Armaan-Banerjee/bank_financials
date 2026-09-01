import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first

# Companies House annual accounts filings (company 05321714, formerly BMCE Bank
# International Plc / MediCapital Bank Plc). All filings are fully scanned
# (image-only) - every figure below was OCR'd/read visually and cross-checked
# against the adjoining year's own comparative column.
AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/05321714/filing-history/MzUxODk4NzcyM2FkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/05321714/filing-history/MzQzODczNDQ5OWFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/05321714/filing-history/MzM5NDE3NzEwN2FkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/05321714/filing-history/MzM1NDAwMjc2N2FkaXF6a2N4/document?format=pdf&download=0"

# Standalone Pillar 3 disclosures, found on the Bank's own site
# (bankofafricaunitedkingdom.co.uk/finances.html) - text-native PDFs, no OCR
# needed. No FY2021 or FY2025 edition exists (site's earliest is FY2022; FY2025
# not yet published).
P3_2022_URL = "https://www.bankofafricaunitedkingdom.co.uk/pdfs/finances/BOA_UK_Pillar_III_2022.pdf"
P3_2023_URL = "https://www.bankofafricaunitedkingdom.co.uk/pdfs/finances/Pillar3-Disclosures-2023.pdf"
P3_2024_URL = "https://www.bankofafricaunitedkingdom.co.uk/pdfs/finances/Pillar3-Disclosures-2024.pdf"
BOA_FINANCES_URL = "https://www.bankofafricaunitedkingdom.co.uk/finances.html"

ENTITY_NOTE = (
    "Entity: BANK OF AFRICA United Kingdom Plc (FRN 454750, company 05321714, formerly "
    "BMCE Bank International Plc / MediCapital Bank Plc), a UK-incorporated subsidiary of "
    "Bank of Africa S.A. (Morocco). Reports in GBP; no FX conversion needed. Does NOT take "
    "the FRS 101/102 cash-flow-statement exemption - a full Statement of Cash Flows exists "
    "every year. All 5 Companies House filings used are fully scanned/image-only; every "
    "figure was read from the rendered page image and cross-checked against the following "
    "year's own comparative column (all ties confirmed exact across the full 5-year chain: "
    "FY2021 closing = FY2022 opening = 87,968; FY2022 closing = FY2023 opening = 68,544; "
    "FY2023 closing = FY2024 opening = 54,575; FY2024 closing = FY2025 opening = 51,070).\n\n"
    "DATA QUALITY NOTE - genuine restatement, distinct from an arithmetic-error correction: "
    "the FY2023 Annual Report restates FY2022's comparative Statement of Changes in Equity "
    "(loss for the year (GBP3,839k) as originally reported in the FY2022 Annual Report vs. "
    "(GBP4,556k) restated; closing equity GBP75,751k vs. GBP75,034k restated) and, within the "
    "Cash Flow Statement itself, restates two line items within operating activities (Change "
    "in operating liabilities GBP(35,633)k original vs. GBP(35,509)k restated; Other non-cash "
    "items GBP(5,399)k vs. GBP(5,512)k restated) - the operating-activities TOTAL is "
    "unaffected (GBP(27,463)k both times) and the closing cash balance is unaffected. The "
    "FY2022 Independent Auditor's Report itself references 'prior year adjustments and "
    "ongoing regulatory investigation' as an audit risk factor, consistent with this being a "
    "genuine, disclosed restatement rather than a transcription error on our part. This "
    "workbook uses each year's own originally-reported cash flow figures as the primary "
    "column (project convention), with the restatement noted here rather than silently "
    "blended in."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Bank of Africa United Kingdom Plc's own Statement of Cash "
    "Flows, GBP'000:\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements 2025, p.42 (Statement of Cash Flows) - {AR2025_URL}\n"
    f"FY2023 (& FY2022 restated comparative, see note): Annual Report and Financial Statements 2023, p.43 (Statement of cash flows) - {AR2023_URL}\n"
    f"FY2022 (originally reported, used as primary column): Annual Report and Financial Statements 2022, p.42 (Statement of cash flows) - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2022, p.42 (Statement of cash flows, FY2021 comparative column) - {AR2022_URL}\n\n"
    + ENTITY_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - Bank of Africa United Kingdom Plc, own entity-level Pillar 3 disclosures "
        "(KM1 Key Metrics), GBP'000 unless stated:\n"
        f"FY2024: Pillar 3 Disclosures 2024, p.6 (Key Metrics) and p.20 (composition of capital resources table) - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures 2023, p.6 (Key Metrics) and p.20 (composition of capital resources table) - {P3_2023_URL}\n"
        f"FY2022: Pillar 3 Disclosures 2022, p.17 (composition of capital resources table, as originally published) - {P3_2022_URL}\n"
        f"FY2021: Pillar 3 Disclosures 2022, p.17 (composition of capital resources table, FY2021 comparative column) - {P3_2022_URL}\n"
        f"FY2025: no Pillar 3 edition published yet (as of this build) - Annual Report and Financial Statements 2025, p.23 (Capital Management) - {AR2025_URL}"
        + extra
    )


bw = BankWorkbook(bank_name="Bank of Africa United Kingdom Plc", years=YEARS, header_color="3D5A80")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from continuing operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {"FY2025": 3104, "FY2024": -2824, "FY2023": -13904, "FY2022": -5278, "FY2021": 5060}),
    ("DATA", "Net interest income", {"FY2025": -7089, "FY2024": -5674, "FY2023": -6774, "FY2022": -15070, "FY2021": -18581}),
    ("DATA", "Interest received", {"FY2025": 13028, "FY2024": 12048, "FY2023": 20919, "FY2022": 19859, "FY2021": 27104}),
    ("DATA", "Interest paid", {"FY2025": -6175, "FY2024": -6777, "FY2023": -10607, "FY2022": -7197, "FY2021": -4236}),
    ("DATA", "Change in operating assets", {"FY2025": -54573, "FY2024": -17912, "FY2023": 170939, "FY2022": 21084, "FY2021": 35264}),
    ("DATA", "Change in operating liabilities", {"FY2025": 34977, "FY2024": 33274, "FY2023": -189466, "FY2022": -35633, "FY2021": 14726}),
    ("DATA", "Other (non-cash) items included in profit before tax", {"FY2025": -7125, "FY2024": -1465, "FY2023": 18778, "FY2022": -5399, "FY2021": 1625}),
    ("DATA", "Corporation tax", {"FY2023": 0, "FY2022": 171, "FY2021": -868}),
    ("TOTAL", "Net cash flows from/(used in) operating activities", {"FY2025": -23853, "FY2024": 10670, "FY2023": -10115, "FY2022": -27463, "FY2021": 60094}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Purchase of financial investments", {"FY2025": -53189, "FY2024": -44212, "FY2023": -7685, "FY2022": -6272, "FY2021": -82228}),
    ("DATA", "Proceeds from sales of financial investments", {"FY2025": 64477, "FY2024": 32257, "FY2023": 8036, "FY2022": 17338, "FY2021": 39068}),
    ("DATA", "Purchase of Property, Plant and Equipment (and Right-of-use Assets)", {"FY2025": -22, "FY2024": -470, "FY2023": -1550, "FY2022": -233, "FY2021": -66}),
    ("DATA", "Purchase of intangible assets", {"FY2025": -877, "FY2024": -1569, "FY2023": -1858, "FY2022": -1744, "FY2021": -745}),
    ("TOTAL", "Net cash flows from/(used in) investing activities", {"FY2025": 10389, "FY2024": -13994, "FY2023": -3057, "FY2022": 9089, "FY2021": -43971}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Repayment of lease principal", {"FY2025": -89, "FY2024": -181, "FY2023": -797, "FY2022": -1050, "FY2021": -944}),
    ("TOTAL", "Net cash flows from/(used in) financing activities", {"FY2025": -89, "FY2024": -181, "FY2023": -797, "FY2022": -1050, "FY2021": -944}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": -13553, "FY2024": -3505, "FY2023": -13969, "FY2022": -19424, "FY2021": 15179}),
    ("DATA", "Cash and cash equivalents as at 1 January", {"FY2025": 51070, "FY2024": 54575, "FY2023": 68544, "FY2022": 87968, "FY2021": 72789}),
    ("TOTAL", "Cash and cash equivalents as at 31 December", {"FY2025": 37517, "FY2024": 51070, "FY2023": 54575, "FY2022": 68544, "FY2021": 87968}),
]

bw.add_cash_flow_sheet(
    title="Bank of Africa United Kingdom Plc — Statement of Cash Flows",
    subtitle="Entity-level (solo) basis, as reported in each year's own Annual Report",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=70,
    source_height=210,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=130)


RESTATEMENT_NOTE = (
    "FY2022 shown here as originally published in the Pillar 3 Disclosures 2022 (Tier 1 "
    "GBP55,465k, Own funds GBP71,130k, RWA GBP453,124k, Total Capital Ratio 15.70%). The "
    "Pillar 3 Disclosures 2023's FY2022 comparative restates this to Tier 1 GBP54,760k, Own "
    "funds GBP70,425k, RWA GBP453,125k, Total Capital Ratio 15.54% - the same restatement "
    "documented on the Cash Flow Statement sheet, consistent with the FY2022 Annual Report's "
    "own auditor's report flagging 'prior year adjustments and ongoing regulatory "
    "investigation'."
)

metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital (= Tier 1 capital; wholly CET1, no AT1 instruments)",
      {"FY2025": 41047, "FY2024": 45680, "FY2023": 44826, "FY2022": 55465, "FY2021": 59466})],
    p3_sources(), note=RESTATEMENT_NOTE,
)

metric(
    "CET1 Ratio", "%",
    [("CET1 Ratio (= Tier 1 Capital Ratio)",
      {"FY2025": "17.46%", "FY2024": "19.65%", "FY2023": "17.75%", "FY2022": "12.24%", "FY2021": "12.36%"})],
    p3_sources(), note=RESTATEMENT_NOTE,
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 Capital",
      {"FY2025": 41047, "FY2024": 45680, "FY2023": 44826, "FY2022": 55465, "FY2021": 59466})],
    p3_sources(), note=RESTATEMENT_NOTE,
)

metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 Capital Ratio",
      {"FY2025": "17.46%", "FY2024": "19.65%", "FY2023": "17.75%", "FY2022": "12.24%", "FY2021": "12.36%"})],
    p3_sources(), note=RESTATEMENT_NOTE,
)

metric(
    "Total Capital", "£'000",
    [("Total Capital / Own Funds (Tier 1 + Tier 2)",
      {"FY2025": 56485, "FY2024": 60323, "FY2023": 60197, "FY2022": 71130, "FY2021": 74498})],
    p3_sources(), note=RESTATEMENT_NOTE,
)

metric(
    "Total Capital Ratio", "%",
    [("Total Capital Ratio (Solvency Ratio)",
      {"FY2025": "24.03%", "FY2024": "25.95%", "FY2023": "23.83%", "FY2022": "15.70%", "FY2021": "15.49%"})],
    p3_sources(), note=RESTATEMENT_NOTE,
)

metric(
    "Total RWAs", "£'000",
    [("Total Risk Weighted Assets (Credit RWA)",
      {"FY2025": 235076, "FY2024": 232412, "FY2023": 252608, "FY2022": 453124, "FY2021": 480918})],
    p3_sources(),
)

metric(
    "Leverage Ratio", "%",
    [("Leverage Ratio",
      {"FY2024": "17.67%", "FY2023": "20.66%", "FY2022": "13.98%", "FY2021": "11.51%"})],
    p3_sources(
        "\n\nFY2025 leverage ratio not found - no Pillar 3 edition published yet and the "
        "FY2025 Annual Report's Strategic Report does not state a leverage ratio; left blank "
        "rather than guessed."
    ),
    note="No FY2025 figure - see source note.",
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio",
      {"FY2025": "212%", "FY2024": "207%", "FY2023": "351%", "FY2022": "207%", "FY2021": "203%"})],
    p3_sources(
        "\n\nBASIS NOTE: FY2021-FY2024 are point-in-time (31 December) LCR from each year's "
        "own Pillar 3 KM1 disclosure (FY2024's 207% independently verified by reconstructing "
        "the LCR composition table: HQLA GBP54,641k / net cash outflows GBP26,427k = 206.75% "
        "≈ 207%). FY2025 (212%) is instead the *average LCR throughout the year* as stated "
        "in the FY2025 Annual Report's 'Liquidity and funding' section (no Pillar 3 edition "
        "exists yet for FY2025) - the FY2025 Annual Report separately states FY2024's average "
        "LCR as 228%, a different basis to the 207% point-in-time figure used for FY2024 "
        "above, kept for consistency with every other year in this row. Same "
        "spot-vs-average distinction documented across this project (e.g. ALRAYAN Bank)."
    ),
    note="FY2025 is an average-throughout-year figure (Annual Report); all other years are "
         "point-in-time at 31 December (Pillar 3 KM1) - see source note.",
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio",
      {"FY2025": "173%", "FY2024": "146%"})],
    p3_sources(
        "\n\nNSFR is not quantified in any Pillar 3 KM1 disclosure found (FY2022-FY2024 "
        "editions mention only that the Bank 'monitors net stable funding ratio' "
        "qualitatively). FY2024 and FY2025 figures instead come from the FY2025 Annual "
        "Report's 'Liquidity and funding' narrative. FY2021-FY2023 not found anywhere - left "
        "blank rather than guessed (plausible given the UK NSFR requirement only took effect "
        "from 1 January 2022)."
    ),
    note="FY2021-FY2023 not publicly disclosed - see source note.",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    "No MREL disclosure found in any Annual Report or Pillar 3 document for any year - no "
    "numeric ratio and no qualitative exemption statement either. BOA UK is a small, "
    "non-systemic entity; plausibly below the Bank of England's MREL-setting threshold, but "
    "left as not disclosed rather than assumed. Official Bank of Africa UK financial reports "
    f"and Pillar 3 disclosures archive reviewed: {BOA_FINANCES_URL}. The available official "
    f"Pillar 3 reports are also cited directly above (2022: {P3_2022_URL}; 2023: "
    f"{P3_2023_URL}; 2024: {P3_2024_URL}).",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash flows from/(used in) operating activities", {"FY2025": -23853, "FY2024": 10670, "FY2023": -10115, "FY2022": -27463, "FY2021": 60094}),
        ("Net cash flows from/(used in) investing activities", {"FY2025": 10389, "FY2024": -13994, "FY2023": -3057, "FY2022": 9089, "FY2021": -43971}),
        ("Net cash flows from/(used in) financing activities", {"FY2025": -89, "FY2024": -181, "FY2023": -797, "FY2022": -1050, "FY2021": -944}),
        ("Cash and cash equivalents as at 31 December", {"FY2025": 37517, "FY2024": 51070, "FY2023": 54575, "FY2022": 68544, "FY2021": 87968}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "17.46%", "FY2024": "19.65%", "FY2023": "17.75%", "FY2022": "12.24%", "FY2021": "12.36%"}),
        ("Total Capital Ratio", {"FY2025": "24.03%", "FY2024": "25.95%", "FY2023": "23.83%", "FY2022": "15.70%", "FY2021": "15.49%"}),
        ("Leverage Ratio", {"FY2024": "17.67%", "FY2023": "20.66%", "FY2022": "13.98%", "FY2021": "11.51%"}),
        ("LCR", {"FY2025": "212%", "FY2024": "207%", "FY2023": "351%", "FY2022": "207%", "FY2021": "203%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page, and the Cash Flow Statement sheet's source note "
         "for a genuine FY2022 restatement affecting several sheets in this workbook.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BANK OF AFRICA UK FINANCIALS.xlsx")
print("Saved.")
