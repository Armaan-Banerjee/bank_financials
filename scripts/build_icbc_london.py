import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first

AR25_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/ICBCLondon/download/2025/ICBCReport2025.pdf"
AR24_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/ICBCLondon/download/2024/ICBCReport2024.pdf"
AR23_URL = "https://find-and-update.company-information.service.gov.uk/company/04552753/filing-history/MzQyNDQ0NTU5OWFkaXF6a2N4/document?format=pdf&download=0"
AR22_URL = "https://find-and-update.company-information.service.gov.uk/company/04552753/filing-history/MzM4MTkxOTA4OGFkaXF6a2N4/document?format=pdf&download=0"
AR21_URL = "https://find-and-update.company-information.service.gov.uk/company/04552753/filing-history/MzM0MDgwMDM4MGFkaXF6a2N4/document?format=pdf&download=0"

P3_25_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/ICBCLondon/download/2025/2025_pillar_3_disclosure.pdf"
P3_24_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/ICBCLondon/download/2024/2024_pillar_3_disclosure.pdf"

CASH_FLOW_SOURCES = (
    "Sources — all figures are ICBC (London) plc Statement of Cash Flows, $'000:\n"
    f"FY2025 & FY2024: ICBC (London) plc Annual Report and Financial Statements 2025, p.27 (Statement of Cash Flows) — {AR25_URL}\n"
    f"FY2024 comparative cross-checked against ICBC (London) plc Annual Report 2024, p.29 (Statement of Cash flows) — {AR24_URL}\n"
    f"FY2023: ICBC (London) plc Annual Report and Financial Statements 2023 (Companies House filing, full accounts), p.30 (Statement of Cash flows) — {AR23_URL}\n"
    f"FY2022: ICBC (London) plc Annual Report and Financial Statements 2022 (Companies House filing, full accounts), p.28 (Statement of Cash flows) — {AR22_URL}\n"
    f"FY2021: ICBC (London) plc Annual Report and Financial Statements 2021 (Companies House filing, full accounts), p.30 (Statement of Cash flows) — {AR21_URL}\n"
    "Note: the FY2021-2023 Companies House filings are scanned (image-only) documents; those years' figures were "
    "transcribed from page renders. All five years cross-reconcile exactly year-on-year (each year's closing cash and "
    "cash equivalents equals the following year's opening balance). 'Gain on sale of financial investments at FVOCI' "
    "was not a separate line in the FY2022/FY2023 statements (folded into the exchange gain/amortisation line); blank "
    "cells indicate that year's statement did not disclose that specific line. The source document's own labels "
    "('Net decrease in cash and cash equivalents', 'Net cash used in operating activities') are reproduced verbatim "
    "even in years where the reported figure is positive."
)

def p3_sources(note_disclosure_start=True):
    text = (
        "Sources — ICBC (London) plc (solo basis), Annex 2 — UK KM1 - Key metric template:\n"
        f"FY2025: ICBC (London) plc Pillar 3 Disclosures 2025, p.13-14 (31/12/2025 column) — {P3_25_URL}\n"
        f"FY2024: ICBC (London) plc Pillar 3 Disclosures 2024, p.12-13 (31/12/2024 column) — {P3_24_URL}\n"
        f"FY2023: ICBC (London) plc Pillar 3 Disclosures 2024, p.12-13 (31/12/2023 comparative column, the only "
        f"public source for this year) — {P3_24_URL}"
    )
    if note_disclosure_start:
        text += (
            "\nNote: ICBC (London) plc's Pillar 3 disclosures are only publicly available from FY2024 onward (the "
            "2025 document's own comparative columns reach back to 31/12/2024; the 2024 document's comparative "
            "columns reach back to 31/12/2023). No FY2022 or FY2021 Pillar 3 disclosure document exists on the "
            "bank's site. The FY2024 RWA/ratio figures used here are taken from the FY2024 disclosure's own current-"
            "period column rather than the FY2025 disclosure's restated comparative column, which shows a slightly "
            "different RWA (715,739.38 vs. 719,040.48) and CET1/Tier1/Total capital ratio (70.48% vs. 70.16%) for "
            "the same date despite an identical capital figure — both are the bank's own official disclosures."
        )
    return text

bw = BankWorkbook(bank_name="ICBC (London) plc", years=YEARS, header_color="2E5395")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Reconciliation of profit for the year to net cash flows from operating activities", {}),
    ("DATA", "Profit for the year", {"FY2025": 42880, "FY2024": 39663, "FY2023": 26135, "FY2022": 11367, "FY2021": 15516}),
    ("DATA", "Depreciation of tangible fixed assets", {"FY2025": 1106, "FY2024": 1073, "FY2023": 1070, "FY2022": 1301, "FY2021": 1819}),
    ("DATA", "Amortisation of intangible assets", {"FY2025": 102, "FY2024": 81, "FY2023": 164, "FY2022": 162, "FY2021": 143}),
    ("DATA", "Impairment losses", {"FY2025": 52, "FY2024": -312, "FY2023": -1180, "FY2022": 1052, "FY2021": -6532}),
    ("DATA", "Interest income", {"FY2025": -73022, "FY2024": -80464, "FY2023": -64844, "FY2022": -27188, "FY2021": -19740}),
    ("DATA", "Interest expense", {"FY2025": 17005, "FY2024": 24461, "FY2023": 28971, "FY2022": 8992, "FY2021": 4294}),
    ("DATA", "Gain on sale of financial investments at FVOCI", {"FY2025": -139, "FY2024": 0, "FY2021": 0}),
    ("DATA", "Exchange gain and accretion of discounts and amortisation of premiums on financial investments", {"FY2025": 4619, "FY2024": 7528, "FY2023": -4149, "FY2022": 21189, "FY2021": 555}),
    ("DATA", "Revaluation (gain)/loss on financial derivatives", {"FY2025": 2500, "FY2024": -189, "FY2023": -66, "FY2022": -96, "FY2021": -497}),
    ("DATA", "Tax on profit on ordinary activities", {"FY2025": 14375, "FY2024": 15178, "FY2023": 8432, "FY2022": 3303, "FY2021": 4280}),
    ("SECTION", "Changes in operating assets and liabilities", {}),
    ("DATA", "Loans to banks", {"FY2025": 764198, "FY2024": -436287, "FY2023": 136996, "FY2022": -160146, "FY2021": 149827}),
    ("DATA", "Loans and advances to customers", {"FY2025": -77176, "FY2024": 93250, "FY2023": -97842, "FY2022": -203380, "FY2021": 305578}),
    ("DATA", "Financial investments at FVOCI", {"FY2025": 408, "FY2024": -60711, "FY2023": 17973, "FY2022": 66827, "FY2021": 46073}),
    ("DATA", "Financial investments at amortised cost", {"FY2025": -9488, "FY2024": 41729, "FY2023": 106936, "FY2022": 35881, "FY2021": -13036}),
    ("DATA", "Other assets", {"FY2025": -3319, "FY2024": -957, "FY2023": 1104, "FY2022": -720, "FY2021": 1762}),
    ("DATA", "Deposits by banks", {"FY2025": 647415, "FY2024": 223171, "FY2023": -59118, "FY2022": 399437, "FY2021": -699204}),
    ("DATA", "Deposits from customers", {"FY2025": -4714, "FY2024": -78671, "FY2023": -3639, "FY2022": -282533, "FY2021": 143585}),
    ("DATA", "Other liabilities", {"FY2025": 1613, "FY2024": -1030, "FY2023": 3697, "FY2022": -1865, "FY2021": 1733}),
    ("DATA", "Interest received", {"FY2025": 72209, "FY2024": 79076, "FY2023": 63856, "FY2022": 27330, "FY2021": 20462}),
    ("DATA", "Interest paid", {"FY2025": -18202, "FY2024": -26683, "FY2023": -26378, "FY2022": -6721, "FY2021": -5095}),
    ("DATA", "Income tax paid", {"FY2025": -15945, "FY2024": -14140, "FY2023": -8715, "FY2022": -2607, "FY2021": -3266}),
    ("TOTAL", "Net cash used in operating activities", {"FY2025": 1366477, "FY2024": -174234, "FY2023": 129403, "FY2022": -108415, "FY2021": -51743}),
    ("SECTION", "Cash flow from investing activities", {}),
    ("DATA", "Acquisition of tangible fixed assets", {"FY2025": -638, "FY2024": -332, "FY2023": -87, "FY2022": -367, "FY2021": -660}),
    ("DATA", "Acquisition of intangible assets", {"FY2025": -126, "FY2024": -115, "FY2023": -188, "FY2022": -158, "FY2021": -133}),
    ("TOTAL", "Net cash used in investing activities", {"FY2025": -764, "FY2024": -447, "FY2023": -275, "FY2022": -525, "FY2021": -793}),
    ("TOTAL", "Net cash from financing activities", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("TOTAL", "Net decrease in cash and cash equivalents", {"FY2025": 1365713, "FY2024": -174681, "FY2023": 129128, "FY2022": -108940, "FY2021": -52536}),
    ("DATA", "Cash and cash equivalents at 1 January", {"FY2025": 139627, "FY2024": 316971, "FY2023": 180382, "FY2022": 307556, "FY2021": 361540}),
    ("DATA", "Effects of exchange rates on cash and cash equivalents", {"FY2025": -6647, "FY2024": -2663, "FY2023": 7461, "FY2022": -18234, "FY2021": -1448}),
    ("TOTAL", "Cash and cash equivalents at 31 December", {"FY2025": 1498693, "FY2024": 139627, "FY2023": 316971, "FY2022": 180382, "FY2021": 307556}),
]

bw.add_cash_flow_sheet(
    title="ICBC (London) plc — Statement of Cash Flows",
    subtitle="Solo basis, $'000 unless stated",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=75,
    source_height=140,
    unit_suffix=" ($'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Solo basis, {unit}" if unit else "Solo basis",
                         rows_data, sources_text, note=note, first_col_width=48, source_height=140)

metric(
    "CET1 Capital", "$'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 547878, "FY2024": 504454, "FY2023": 474459})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 ratio", {"FY2025": "81.09%", "FY2024": "70.16%", "FY2023": "56.30%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "$'000",
    [("Tier 1 capital", {"FY2025": 547878, "FY2024": 504454, "FY2023": 474459})],
    p3_sources(),
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "81.09%", "FY2024": "70.16%", "FY2023": "56.30%"})],
    p3_sources(),
)

metric(
    "Total Capital", "$'000",
    [("Total capital", {"FY2025": 547878, "FY2024": 504454, "FY2023": 474459})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "81.09%", "FY2024": "70.16%", "FY2023": "56.30%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "$'000",
    [("Total risk-weighted exposure amount", {"FY2025": 675668, "FY2024": 719040, "FY2023": 842738})],
    p3_sources(),
)

metric(
    "Leverage Ratio", "$'000 / %",
    [
        ("Leverage ratio total exposure measure ($'000)", {"FY2025": 1153889, "FY2024": 1493767, "FY2023": 1339718}),
        ("Leverage ratio (%)", {"FY2025": "47.48%", "FY2024": "33.77%", "FY2023": "35.41%"}),
    ],
    p3_sources(),
)

metric(
    "LCR", "$'000 / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value ($'000)", {"FY2025": 1374779, "FY2024": 328482, "FY2023": 384069}),
        ("Total net cash outflows, adjusted value ($'000)", {"FY2025": 956680, "FY2024": 187564, "FY2023": 136060}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "143.70%", "FY2024": "175.13%", "FY2023": "282.28%"}),
    ],
    p3_sources(),
    note="LCR figures are single month-end (31 December) spot observations as disclosed in the KM1 template, not a "
         "12-month trailing average.",
)

metric(
    "NSFR", "$'000 / %",
    [
        ("Total available stable funding ($'000)", {"FY2025": 581574, "FY2024": 608924, "FY2023": 694607}),
        ("Total required stable funding ($'000)", {"FY2025": 335509, "FY2024": 407762, "FY2023": 511527}),
        ("Net Stable Funding Ratio (%)", {"FY2025": "173.34%", "FY2024": "149.33%", "FY2023": "135.79%"}),
    ],
    p3_sources(),
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(note_disclosure_start=False) + "\nMREL is not referenced anywhere in either available Pillar 3 disclosure document; "
    "ICBC (London) plc does not appear to be subject to a separate MREL requirement.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash used in operating activities", {"FY2025": 1366477, "FY2024": -174234, "FY2023": 129403, "FY2022": -108415, "FY2021": -51743}),
        ("Net cash used in investing activities", {"FY2025": -764, "FY2024": -447, "FY2023": -275, "FY2022": -525, "FY2021": -793}),
        ("Net cash from financing activities", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
        ("Cash and cash equivalents at 31 December", {"FY2025": 1498693, "FY2024": 139627, "FY2023": 316971, "FY2022": 180382, "FY2021": 307556}),
    ],
    cash_flow_unit="$'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "81.09%", "FY2024": "70.16%", "FY2023": "56.30%"}),
        ("Tier 1 Ratio", {"FY2025": "81.09%", "FY2024": "70.16%", "FY2023": "56.30%"}),
        ("Total Capital Ratio", {"FY2025": "81.09%", "FY2024": "70.16%", "FY2023": "56.30%"}),
        ("Leverage Ratio", {"FY2025": "47.48%", "FY2024": "33.77%", "FY2023": "35.41%"}),
        ("LCR", {"FY2025": "143.70%", "FY2024": "175.13%", "FY2023": "282.28%"}),
        ("NSFR", {"FY2025": "173.34%", "FY2024": "149.33%", "FY2023": "135.79%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Pillar 3 ratios are only publicly disclosed from FY2023 onward "
         "(no FY2022/FY2021 Pillar 3 document exists); blank cells for those years are intentional, not zeros.",
)

bw.save("/Users/armaan/code/katalysis/banks/ICBC (LONDON) PLC FINANCIALS.xlsx")
