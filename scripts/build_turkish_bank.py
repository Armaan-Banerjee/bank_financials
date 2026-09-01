import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://www.turkishbank.co.uk/wp-content/uploads/2026/04/Financial-Statements-TBUK-signed.pdf"
AR2024_URL = "https://www.turkishbank.co.uk/wp-content/uploads/2025/04/FINANCIAL-STATEMENTS-31122024-FINAL_SIGNED.pdf"
AR2023_URL = "https://www.turkishbank.co.uk/wp-content/uploads/2024/07/FY23TBUK-Financial-Statements-Signed.pdf"
AR2022_URL = "https://www.turkishbank.co.uk/wp-content/uploads/2023/05/FY22TBUK-Financial-Statements-Signed-for-AGM-signed.pdf"
AR2021_URL = "https://www.turkishbank.co.uk/wp-content/uploads/2022/07/21TBUK-Financial-Statements-reported-to-AGM-signed.pdf"
P3_2024_URL = "https://www.turkishbank.co.uk/wp-content/uploads/2026/02/PILLAR-3-DISCLOSURE.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Turkish Bank (UK) Limited (company number 02643004, FRN 204566), a UK-incorporated PRA-authorised "
    "bank majority-owned by Turkish Bank A.S. (Turkey/Northern Cyprus). Entity-level (unconsolidated) basis "
    "throughout - the Bank has no subsidiaries of its own. FY2021 and FY2025 Annual Reports were only available as "
    "fully scanned/image-only PDFs on the Bank's own site (no text layer) - both were OCR'd (tesseract) and every "
    "figure used below was cross-verified against the rendered page image, not trusted from OCR text alone."
)

PILLAR3_NOTE = (
    "PILLAR 3 COVERAGE NOTE: only one Pillar 3 Disclosure document is published on the Bank's site, covering "
    "31 Dec 2024 with a 31 Dec 2023 comparative (its 'Appendix 1: Key Metrics' UK KM1 template). No earlier Pillar 3 "
    "edition could be found (site search or Wayback Machine) and no FY2025 edition has been published yet - "
    "consistent with this being a very small bank that appears to have only recently begun formal Pillar 3 "
    "disclosure. FY2021/FY2022/FY2025 capital ratios (CET1/Tier 1/Total Capital/Leverage/LCR/NSFR) and the £ capital "
    "amounts behind them are therefore genuinely not publicly available and are left blank rather than estimated. "
    "Each Annual Report's own Note 37/38 'Capital risk management' does give a 'Total regulatory capital' figure for "
    "every year (FY2021-FY2025), but that figure is NOT on the same basis as CET1/Tier 1/Total Capital: it is an "
    "audited figure that includes fair value and revaluation reserve movements which the Bank's own notes state "
    "'would have [been] excluded... at the time of submission' of its actual regulatory return (confirmed by "
    "comparing the FY2024 AR's Total regulatory capital of £29,678k against the Pillar 3 KM1's CET1/Tier1/Total "
    "Capital of £28,884k for the same date). To avoid mixing bases under a single ratio/capital label, that broader "
    "AR figure is not substituted in here - see the Cash Flow Statement source note for where it can be found "
    "instead. Total RWAs is the one metric confirmed on a consistent, comparable basis across all 5 years (the "
    "Annual Reports' own RWA breakdown ties exactly to the Pillar 3 KM1 RWA figure for the years both exist)."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Turkish Bank (UK) Limited's own Statement of Cash Flows, £'000:\n"
    f"FY2025: Annual Report and Financial Statements for the year ended 31 December 2025, p.21 (Statement of Cash "
    f"Flows) - {AR2025_URL} (scanned filing, OCR'd and visually cross-verified)\n"
    f"FY2024: Annual Report and Financial Statements for the year ended 31 December 2024, p.22 (Statement of Cash "
    f"Flows) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.22 (Statement of Cash Flows) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2022, p.23 (Statement of Cash Flows) - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021, p.23 (Statement of Cash Flows) - {AR2021_URL} (scanned "
    f"filing, OCR'd and visually cross-verified)\n"
    "Note: each year's column uses that year's own Annual Report's own as-originally-reported comparative rather "
    "than a later report's restated comparative (e.g. the FY2023 report restated some FY2022 line items following a "
    "reclassification of accrued interest, and the FY2025 report similarly restated FY2024 - in both cases the "
    "originally-reported figures from that year's own report are used here, consistent with this project's usual "
    "convention). All 5 years reconcile exactly: opening cash equivalents in each year matches the prior year's own "
    "closing figure, and every activity subtotal sums correctly from its own line items. The FY2025 Statement's "
    "'Net decrease in cash and cash equivalents' row is labelled 'decrease' in the source but the figure itself is "
    "positive (+£1,217k, an increase) - the number is used as printed (it reconciles exactly with opening/closing "
    "balances); only the label appears to be a leftover from the prior year's (negative) presentation. FY2021's "
    "'profit and non-cash adjustments' subtotal is printed as £(3,466)k but the seven line items above it as printed "
    "sum to £(3,464)k - an immaterial £2k gap in the source itself; the printed subtotal is used as shown (not "
    "force-corrected) since it is what the statement's own downstream totals are built from, and the gap is too "
    "small to matter to any of this bank's other figures.\n\n"
    + ENTITY_NOTE + "\n\n"
    "Note 37/38 'Capital risk management' in each Annual Report separately discloses 'Total regulatory capital' "
    "(FY2021: £24,681k: FY2022: £26,022k; FY2023: £29,196k; FY2024: £29,678k; FY2025: £27,379k) and 'Total risk "
    "weighted assets' (used for the Total RWAs sheet) - see PILLAR3_NOTE on the Pillar 3 sheets for why the capital "
    "figure is not used as CET1/Tier1/Total Capital. Minor (<£100k) differences exist between a year's figure as "
    "originally reported and as shown as the following year's comparative (e.g. FY2022 retained earnings: £8,102k "
    "in the FY2022 report vs £8,019k in the FY2023 report's comparative) - not explained in either report; each "
    "year's own report's own figure is used for its own column."
)


def p3_sources():
    return (
        "Sources - Turkish Bank (UK) Limited, entity-level basis:\n"
        f"FY2024/FY2023: Pillar 3 Disclosure (published Feb 2026), p.31 (Appendix 1: Key Metrics - UK KM1 template, "
        f"columns '31 Dec 24' / '31 Dec 23') - {P3_2024_URL}\n"
        f"Total RWAs only, FY2022/FY2021: Annual Report and Financial Statements 2022, p.63 (Note 38 Capital risk "
        f"management, risk-weighted assets table) - {AR2022_URL}\n"
        f"Total RWAs only, FY2025: Annual Report and Financial Statements for the year ended 31 December 2025, p.61 "
        f"(Note 37 Capital risk management, risk-weighted assets table) - {AR2025_URL}\n\n"
        + PILLAR3_NOTE
    )


bw = BankWorkbook(bank_name="Turkish Bank (UK) Limited", years=YEARS, year_label=YEAR_LABEL, header_color="9C3D54")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) after taxation", {"FY2025": -576, "FY2024": 795, "FY2023": 2840, "FY2022": 1140, "FY2021": -29}),
    ("DATA", "Depreciation of property, plant and equipment", {"FY2025": 311, "FY2024": 255, "FY2023": 261, "FY2022": 316, "FY2021": 309}),
    ("DATA", "Amortisation of intangible assets", {"FY2025": 192, "FY2024": 200, "FY2023": 188, "FY2022": 210, "FY2021": 228}),
    ("DATA", "Non-cash stock dividends received from Visa", {"FY2022": -383, "FY2021": 0}),
    ("DATA", "Net interest income", {"FY2025": -7669, "FY2024": -9663, "FY2023": -9839, "FY2022": -5766, "FY2021": -4012}),
    ("DATA", "Interest paid on lease liabilities", {"FY2025": 0, "FY2024": 1, "FY2023": 1, "FY2022": 2, "FY2021": 2}),
    ("DATA", "Income tax expense/(credit)", {"FY2025": -366, "FY2024": 224, "FY2023": 881, "FY2022": 330, "FY2021": 38}),
    ("TOTAL", "Subtotal - profit and non-cash adjustments", {"FY2025": -8108, "FY2024": -8188, "FY2023": -5668, "FY2022": -4151, "FY2021": -3466}),
    ("SECTION", "Changes in operating assets and liabilities", {}),
    ("DATA", "Loans and advances to customers", {"FY2025": 3479, "FY2024": -7269, "FY2023": 5951, "FY2022": 2308, "FY2021": 3493}),
    ("DATA", "Loans and advances to banks", {"FY2025": 1871, "FY2024": -18801, "FY2023": -15876, "FY2022": 24461, "FY2021": -25858}),
    ("DATA", "Other assets", {"FY2025": -304, "FY2024": -540, "FY2023": -340, "FY2022": 1420, "FY2021": -1716}),
    ("DATA", "Deposits from banks", {"FY2025": -538, "FY2024": -4169, "FY2023": -2153, "FY2022": -2331, "FY2021": 5621}),
    ("DATA", "Deposits from customers", {"FY2025": -568, "FY2024": 1544, "FY2023": -12913, "FY2022": 6640, "FY2021": 2240}),
    ("DATA", "Other liabilities", {"FY2025": 173, "FY2024": -215, "FY2023": 1221, "FY2022": 112, "FY2021": 11}),
    ("TOTAL", "Subtotal - changes in operating assets and liabilities", {"FY2025": 4113, "FY2024": -29450, "FY2023": -24110, "FY2022": 32610, "FY2021": -16209}),
    ("SECTION", "Interest and tax", {}),
    ("DATA", "Interest received", {"FY2025": 10531, "FY2024": 12623, "FY2023": 12411, "FY2022": 6417, "FY2021": 4405}),
    ("DATA", "Interest paid", {"FY2025": -2862, "FY2024": -2960, "FY2023": -2572, "FY2022": -651, "FY2021": -393}),
    ("DATA", "Income tax recovered/(paid)", {"FY2025": 130, "FY2024": -374, "FY2023": -669}),
    ("TOTAL", "Net cash flows from/(used in) operating activities", {"FY2025": 3804, "FY2024": -28349, "FY2023": -20608, "FY2022": 34225, "FY2021": -15663}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Additions to/acquisition of property and equipment", {"FY2025": -2091, "FY2024": -61, "FY2023": -186, "FY2022": -97, "FY2021": -15}),
    ("DATA", "Additions to/acquisition of intangible assets", {"FY2025": -481, "FY2024": -35, "FY2023": -493, "FY2022": -43, "FY2021": -6}),
    ("TOTAL", "Net cash used in investing activities", {"FY2025": -2572, "FY2024": -96, "FY2023": -679, "FY2022": -140, "FY2021": -21}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Payment for lease liabilities", {"FY2025": -15, "FY2024": -38, "FY2023": -43, "FY2022": -98, "FY2021": -108}),
    ("DATA", "Interest paid on lease liabilities", {"FY2025": 0, "FY2024": -1, "FY2023": -1, "FY2022": -2, "FY2021": -2}),
    ("TOTAL", "Net cash used in financing activities", {"FY2025": -15, "FY2024": -39, "FY2023": -44, "FY2022": -100, "FY2021": -110}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 1217, "FY2024": -28484, "FY2023": -21331, "FY2022": 33985, "FY2021": -15794}),
    ("DATA", "Cash and cash equivalents as at 1 January", {"FY2025": 43449, "FY2024": 71933, "FY2023": 93264, "FY2022": 59279, "FY2021": 75073}),
    ("TOTAL", "Cash and cash equivalents as at 31 December", {"FY2025": 44666, "FY2024": 43449, "FY2023": 71933, "FY2022": 93264, "FY2021": 59279}),
]

bw.add_cash_flow_sheet(
    title="Turkish Bank (UK) Limited — Statement of Cash Flows",
    subtitle="Entity-level basis, £'000",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=70,
    source_height=310,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=140)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2024": 28884, "FY2023": 28099})],
    p3_sources(),
    note="Only FY2023/FY2024 are publicly disclosed - see PILLAR3_NOTE.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2024": "25.97%", "FY2023": "28.24%"})],
    p3_sources(),
    note="Only FY2023/FY2024 are publicly disclosed - see PILLAR3_NOTE.",
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2024": 28884, "FY2023": 28099})],
    p3_sources(),
    note="CET1 = Tier 1 = Total Capital in both disclosed years (no AT1 or Tier 2 instruments). Only FY2023/FY2024 "
         "are publicly disclosed - see PILLAR3_NOTE.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2024": "25.97%", "FY2023": "28.24%"})],
    p3_sources(),
    note="Only FY2023/FY2024 are publicly disclosed - see PILLAR3_NOTE.",
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2024": 28884, "FY2023": 28099})],
    p3_sources(),
    note="CET1 = Tier 1 = Total Capital in both disclosed years (no AT1 or Tier 2 instruments). Only FY2023/FY2024 "
         "are publicly disclosed - see PILLAR3_NOTE.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total Capital ratio", {"FY2024": "25.97%", "FY2023": "28.24%"})],
    p3_sources(),
    note="Only FY2023/FY2024 are publicly disclosed - see PILLAR3_NOTE.",
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted exposure amount", {"FY2025": 103473, "FY2024": 111235, "FY2023": 99516, "FY2022": 92487, "FY2021": 102064})],
    p3_sources(),
    note="The one metric available for all 5 years: each Annual Report's own Note 37/38 RWA breakdown (Credit + "
         "Operational + FX + CVA risk) ties exactly to the Pillar 3 KM1 RWA figure for the years both exist "
         "(FY2023/FY2024), confirming a consistent basis across all years.",
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Total exposure measure", {"FY2024": 181556, "FY2023": 185406}),
        ("Leverage ratio (including claims on central banks) (%)", {"FY2024": "15.9%", "FY2023": "15.2%"}),
    ],
    p3_sources(),
    note="Only FY2023/FY2024 are publicly disclosed - see PILLAR3_NOTE.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA)", {"FY2024": 30533, "FY2023": 45106}),
        ("Total net cash outflows (adjusted value)", {"FY2024": 5033, "FY2023": 6103}),
        ("Liquidity Coverage Ratio (%)", {"FY2024": "606%", "FY2023": "739%"}),
    ],
    p3_sources(),
    note="Only FY2023/FY2024 are publicly disclosed - see PILLAR3_NOTE.",
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding", {"FY2024": 158883, "FY2023": 147611}),
        ("Total required stable funding", {"FY2024": 81335, "FY2023": 76650}),
        ("NSFR ratio (%)", {"FY2024": "195.34%", "FY2023": "192.58%"}),
    ],
    p3_sources(),
    note="Only FY2023/FY2024 are publicly disclosed - see PILLAR3_NOTE.",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    sources_text=p3_sources(),
    per_note={"MREL Ratio": (
        "Not publicly disclosed for any year - no numeric or qualitative MREL disclosure was found in either the "
        "Pillar 3 Disclosure or any Annual Report. Consistent with a very small bank likely below the threshold at "
        "which the Bank of England sets an MREL requirement above minimum capital requirements (no explicit "
        "exemption is stated, it is simply absent)."
    )},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 3804, "FY2024": -28349, "FY2023": -20608, "FY2022": 34225, "FY2021": -15663}),
        ("Net cash from/(used in) investing activities", {"FY2025": -2572, "FY2024": -96, "FY2023": -679, "FY2022": -140, "FY2021": -21}),
        ("Net cash from/(used in) financing activities", {"FY2025": -15, "FY2024": -39, "FY2023": -44, "FY2022": -100, "FY2021": -110}),
        ("Cash and cash equivalents at end of year", {"FY2025": 44666, "FY2024": 43449, "FY2023": 71933, "FY2022": 93264, "FY2021": 59279}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2024": "25.97%", "FY2023": "28.24%"}),
        ("Tier 1 Ratio", {"FY2024": "25.97%", "FY2023": "28.24%"}),
        ("Total Capital Ratio", {"FY2024": "25.97%", "FY2023": "28.24%"}),
        ("Leverage Ratio", {"FY2024": "15.9%", "FY2023": "15.2%"}),
        ("LCR", {"FY2024": "606%", "FY2023": "739%"}),
        ("NSFR", {"FY2024": "195.34%", "FY2023": "192.58%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Pillar 3 ratios are only publicly disclosed for FY2023/FY2024 "
         "(the Bank has published only one Pillar 3 edition to date) - see the Pillar 3 sheets' PILLAR3_NOTE for "
         "detail on why FY2021/FY2022/FY2025 are blank rather than estimated.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/TURKISH BANK UK FINANCIALS.xlsx")
