import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first

CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/07425398/filing-history"
AR25_URL = f"{CH_BASE}/MzUyNjQ0MDA3MmFkaXF6a2N4/document?format=pdf&download=0"
AR23_URL = f"{CH_BASE}/MzQyMDE3MTk5NWFkaXF6a2N4/document?format=pdf&download=0"
AR21_URL = f"{CH_BASE}/MzMzODgwNTQxMWFkaXF6a2N4/document?format=pdf&download=0"

CASH_FLOW_SOURCES = (
    "Sources — all figures are Itau BBA International plc (\"IBBAInt\"/\"the Bank\") solo-entity (Bank, not Group) "
    "Statement of Cash Flows, USD'000:\n"
    f"FY2025 & FY2024: 2025 Annual Report, p.65 (Statements of Cash Flows) — {AR25_URL}\n"
    f"FY2023 & FY2022: 2023 Annual Report, p.57 (Statement of Cash Flows) — {AR23_URL}\n"
    f"FY2021: 2021 Annual Report, p.56 (Statement of Cash Flows) — {AR21_URL}\n"
    "Note: these are Companies House filing copies (fully scanned/image-only PDFs, no text layer — transcribed via "
    "page-render + manual reading). The bank's own site (itau.co.uk) returned HTTP 403 to every fetch, and the "
    "domain referenced throughout the Annual Report for further disclosures (www.itaubba.co.uk) was unreachable "
    "this session (connection refused/timed out, and no usable Wayback Machine snapshot was found — a genuine "
    "Internet Archive-side outage, not bank-specific), so Companies House was the only available source. The source "
    "labels 'Derivatives designated as hedging instruments' twice per year (once within operating assets, once "
    "within operating liabilities) — disambiguated here as '(assets)' / '(liabilities)' for clarity; this is a "
    "labeling change only, not a data change. 'Purchases of financial assets measured at fair value through OCI' "
    "is printed with an inconsistent sign convention across report vintages (positive in the FY2025 report's own "
    "FY2025/FY2024 columns, negative in the FY2023 report's own FY2023/FY2022 columns) — transcribed exactly as "
    "each source year printed it, not normalized. Blank cells indicate that year's report did not disclose that "
    "specific line; a dash ('-') in the source is shown as 0. All 5 years' opening cash balances tie exactly to "
    "the prior year's closing balance. DATA QUALITY NOTE: summing FY2024's own individually-transcribed line "
    "items gives USD 233,960k for 'Net cash flow from operating activities before payment of income tax', a USD "
    "7k gap against the figure the source itself prints for that subtotal (USD 233,967k, used here) — an "
    "immaterial rounding artifact within the source document, not a transcription error (every individual line "
    "item ties exactly to the source page); flagged rather than silently adjusted, per this project's convention."
)

def p3_sources(page, doc_label, url, note_extra=""):
    return (
        f"Source — Itau BBA International plc Group (consolidated) regulatory capital summary, {doc_label} "
        f"Annual Report, p.{page} ('Capital' section of the Strategic Report) — {url}\n"
        "The Annual Report states in full that additional Pillar 3 Disclosures (capital detail, LCR, NSFR, MREL) "
        "are published as a separate, standalone unaudited document on www.itaubba.co.uk — that site was "
        "unreachable this session (connection refused/timed out; no usable Wayback Machine snapshot found), so "
        "only the summary figures printed directly in the Annual Report's own 'Capital' section are used here. "
        "Figures are Group/consolidated basis (the Annual Report's Capital section is presented at Group level "
        "only, not solo Bank level, throughout all 5 years)." + (" " + note_extra if note_extra else "")
    )

bw = BankWorkbook(bank_name="Itau BBA International plc", years=YEARS, header_color="F58220")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit before tax and dividends", {"FY2025": 120167, "FY2024": 131803, "FY2023": 83525, "FY2022": 68873, "FY2021": 23680}),
    ("DATA", "Credit impairment charges and other provisions", {"FY2025": -64, "FY2024": -306, "FY2023": 6669, "FY2022": -4188, "FY2021": -9753}),
    ("DATA", "Depreciation, amortisation and impairment of property, plant, equipment and intangibles", {"FY2025": 831, "FY2024": 852, "FY2023": 999, "FY2022": 1280, "FY2021": 1276}),
    ("DATA", "Other non-cash movements", {"FY2025": -104138, "FY2024": 31363, "FY2023": -33091, "FY2022": 9264, "FY2021": 1017}),
    ("DATA", "Trading assets and financial assets designated at fair value", {"FY2025": 124541, "FY2024": -213757, "FY2023": 501113, "FY2022": 629204, "FY2021": 156038}),
    ("DATA", "Loans and advances to banks", {"FY2025": 135096, "FY2024": -240931, "FY2023": 23043, "FY2022": -200127, "FY2021": 37815}),
    ("DATA", "Balances at central banks (mandatory reserves)", {"FY2021": 0}),
    ("DATA", "Loans and advances to customers", {"FY2025": 60053, "FY2024": -235192, "FY2023": -263283, "FY2022": -378299, "FY2021": -32696}),
    ("DATA", "Derivatives designated as hedging instruments (assets)", {"FY2025": 3103, "FY2024": -1190, "FY2023": 38012, "FY2022": -48100, "FY2021": -1705}),
    ("DATA", "Other operating assets", {"FY2025": 17431, "FY2024": 12645, "FY2023": 22312, "FY2022": -33257, "FY2021": 3638}),
    ("DATA", "Trading liabilities", {"FY2025": 71537, "FY2024": 178116, "FY2023": -113085, "FY2022": -37506, "FY2021": 56410}),
    ("DATA", "Financial liabilities designated at fair value", {"FY2025": -44456, "FY2024": -4802, "FY2023": 49259, "FY2022": -410, "FY2021": -1396}),
    ("DATA", "Deposits from banks", {"FY2025": 127432, "FY2024": -432800, "FY2023": 521131, "FY2022": -13577, "FY2021": -545052}),
    ("DATA", "Customer accounts", {"FY2025": -994100, "FY2024": 1035388, "FY2023": -204474, "FY2022": 162167, "FY2021": 509622}),
    ("DATA", "Debt securities in issue", {"FY2025": -259630, "FY2024": -75268, "FY2023": 314516, "FY2022": 802330, "FY2021": -8907}),
    ("DATA", "Derivatives designated as hedging instruments (liabilities)", {"FY2025": -4690, "FY2024": 1337, "FY2023": -10618, "FY2022": 27046, "FY2021": -8097}),
    ("DATA", "Other operating liabilities", {"FY2025": -45452, "FY2024": 46702, "FY2023": -16839, "FY2022": 8370, "FY2021": 4105}),
    ("TOTAL", "Net cash flow from operating activities before payment of income tax", {"FY2025": -792339, "FY2024": 233967, "FY2023": 919189, "FY2022": 993070, "FY2021": 185995}),
    ("DATA", "Income tax paid", {"FY2025": -30862, "FY2024": -31922, "FY2023": -22344, "FY2022": -15859, "FY2021": -2809}),
    ("TOTAL", "Net cash flow from operating activities", {"FY2025": -823201, "FY2024": 202045, "FY2023": 896845, "FY2022": 977211, "FY2021": 183186}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Sales/(Purchases) of debt investments at amortised cost", {"FY2022": 2192, "FY2021": -2192}),
    ("DATA", "Purchases of financial assets measured at fair value through OCI", {"FY2025": 90366, "FY2024": 206101, "FY2023": -851115, "FY2022": -1180856}),
    ("DATA", "Sales/(Purchases) of subsidiaries", {"FY2025": -550, "FY2024": -55880, "FY2023": -65061, "FY2022": -10670, "FY2021": -45297}),
    ("DATA", "Dividends received", {"FY2024": 1, "FY2022": 20004, "FY2021": 8888}),
    ("DATA", "Purchases of intangible assets", {"FY2021": -61}),
    ("DATA", "Sales/(Purchases) of fixed assets", {"FY2025": -33, "FY2024": -33, "FY2023": -2406, "FY2022": -33, "FY2021": -2155}),
    ("TOTAL", "Net cash flow from investing activities", {"FY2025": 89783, "FY2024": 150189, "FY2023": -918582, "FY2022": -1169363, "FY2021": -40817}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Leasing Contracts", {"FY2025": -862, "FY2024": -838, "FY2023": 1619, "FY2022": -926, "FY2021": 948}),
    ("DATA", "Share Capital Increase", {"FY2023": 500000}),
    ("TOTAL", "Net cash flow from financing activities", {"FY2025": -862, "FY2024": -838, "FY2023": 501619, "FY2022": -926, "FY2021": 948}),
    ("TOTAL", "Increase/(decrease) in cash and cash equivalents", {"FY2025": -734280, "FY2024": 351396, "FY2023": 479882, "FY2022": -193078, "FY2021": 143317}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 1149307, "FY2024": 797911, "FY2023": 318029, "FY2022": 511107, "FY2021": 367790}),
    ("DATA", "Effects of exchange rate change on cash and cash equivalents", {"FY2025": 45560, "FY2024": 0, "FY2021": 0}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 460587, "FY2024": 1149307, "FY2023": 797911, "FY2022": 318029, "FY2021": 511107}),
    ("SECTION", "Cash and cash equivalents comprise", {}),
    ("DATA", "Cash and balances at Central Banks", {"FY2025": 17, "FY2024": 16, "FY2023": 16, "FY2022": 15, "FY2021": 16}),
    ("DATA", "Loans and advances to banks with original maturity less than three months", {"FY2025": 460570, "FY2024": 1149291, "FY2023": 797895, "FY2022": 318014, "FY2021": 511091}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 460587, "FY2024": 1149307, "FY2023": 797911, "FY2022": 318029, "FY2021": 511107}),
]

bw.add_cash_flow_sheet(
    title="Itau BBA International plc — Statement of Cash Flows (Bank, solo)",
    subtitle="Itau BBA International plc (Bank/solo basis, not Group), USD'000 unless stated",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=76,
    source_height=170,
    unit_suffix=" (USD'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Group/consolidated basis, {unit}" if unit else "Group/consolidated basis",
                         rows_data, sources_text, note=note, first_col_width=48, source_height=150)

metric(
    "CET1 Capital", "USD m",
    [("Common equity tier 1 (CET1) capital", {"FY2025": 2276, "FY2024": 2073, "FY2023": 1939, "FY2022": 1334, "FY2021": 1318})],
    p3_sources(21, "2025", AR25_URL),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common equity tier 1 ratio", {"FY2025": "29.0%", "FY2024": "23.9%", "FY2023": "27.0%", "FY2022": "19.6%", "FY2021": "22.6%"})],
    p3_sources(21, "2025", AR25_URL),
)

metric(
    "Tier 1 Capital", None,
    [("Tier 1 capital", {y: "Not publicly disclosed" for y in YEARS})],
    p3_sources(21, "2025", AR25_URL),
    note="No distinct Tier 1 capital figure is broken out in the Annual Report's 'Capital' section in any of the "
         "5 years — only 'Common equity tier 1 capital' and 'Total regulatory capital' are shown, and those two "
         "figures are identical (or within USD 1m) in every year sourced, implying negligible AT1 instruments, "
         "but no separate Tier 1 line exists to transcribe. See the CET1 Capital and Total Capital sheets.",
)

metric(
    "Tier 1 Ratio", None,
    [("Tier 1 ratio", {y: "Not publicly disclosed" for y in YEARS})],
    p3_sources(21, "2025", AR25_URL),
    note="Same basis as the Tier 1 Capital sheet — no distinct Tier 1 ratio is broken out; CET1 ratio and Total "
         "capital ratio are identical in every year sourced. See the CET1 Ratio and Total Capital Ratio sheets.",
)

metric(
    "Total Capital", "USD m",
    [("Total regulatory capital", {"FY2025": 2276, "FY2024": 2073, "FY2023": 1940, "FY2022": 1334, "FY2021": 1318})],
    p3_sources(21, "2025", AR25_URL),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "29.0%", "FY2024": "23.9%", "FY2023": "27.1%", "FY2022": "19.6%", "FY2021": "22.6%"})],
    p3_sources(21, "2025", AR25_URL),
)

metric(
    "Total RWAs", "USD m",
    [("Risk-weighted assets (RWA)", {"FY2025": 7855, "FY2024": 8660, "FY2023": 7170, "FY2022": 6812, "FY2021": 5836})],
    p3_sources(21, "2025", AR25_URL),
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio", {"FY2025": "19.1%", "FY2024": "16.4%", "FY2023": "16.7%", "FY2022": "11.9%", "FY2021": "14.6%"})],
    p3_sources(21, "2025", AR25_URL, "The Leverage Ratio is quoted in the Capital section's narrative text (not the composition table) each year."),
)

metric(
    "LCR", None,
    [("Liquidity Coverage Ratio", {y: "Not publicly disclosed" for y in YEARS})],
    p3_sources(21, "2025", AR25_URL),
    note="Not found anywhere in the Annual Report's own pages (Strategic Report or Notes) — the Annual Report "
         "defers all liquidity Pillar 3 detail to the standalone Pillar 3 Disclosures document referenced above, "
         "which was unreachable this session.",
)

metric(
    "NSFR", None,
    [("Net Stable Funding Ratio", {y: "Not publicly disclosed" for y in YEARS})],
    p3_sources(21, "2025", AR25_URL),
    note="Same availability constraint as the LCR sheet — deferred to the unreachable standalone Pillar 3 report.",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})],
    p3_sources(21, "2025", AR25_URL),
    note="No MREL ratio or resolution-strategy discussion was found in the Annual Report's own pages; deferred to "
         "the unreachable standalone Pillar 3 report, same as LCR/NSFR.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash flow from operating activities", {"FY2025": -823201, "FY2024": 202045, "FY2023": 896845, "FY2022": 977211, "FY2021": 183186}),
        ("Net cash flow from investing activities", {"FY2025": 89783, "FY2024": 150189, "FY2023": -918582, "FY2022": -1169363, "FY2021": -40817}),
        ("Net cash flow from financing activities", {"FY2025": -862, "FY2024": -838, "FY2023": 501619, "FY2022": -926, "FY2021": 948}),
        ("Cash and cash equivalents at end of year", {"FY2025": 460587, "FY2024": 1149307, "FY2023": 797911, "FY2022": 318029, "FY2021": 511107}),
    ],
    cash_flow_unit="USD'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "29.0%", "FY2024": "23.9%", "FY2023": "27.0%", "FY2022": "19.6%", "FY2021": "22.6%"}),
        ("Total Capital Ratio", {"FY2025": "29.0%", "FY2024": "23.9%", "FY2023": "27.1%", "FY2022": "19.6%", "FY2021": "22.6%"}),
        ("Leverage Ratio", {"FY2025": "19.1%", "FY2024": "16.4%", "FY2023": "16.7%", "FY2022": "11.9%", "FY2021": "14.6%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Cash flow figures are Bank/solo basis; capital ratios are "
         "Group/consolidated basis (the only basis the Annual Report discloses for capital). Tier 1 Ratio, LCR and "
         "NSFR are omitted from this chart — not separately disclosed/not publicly disclosed in the sourced pages; "
         "see each metric's own sheet for detail.",
)

bw.save("/Users/armaan/code/katalysis/banks/ITAU BBA INTERNATIONAL FINANCIALS.xlsx")
