import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# PILLAR-3-ONLY WORKBOOK: The Bank of New York Mellon (International) Limited
# takes the FRS 101 cash-flow-statement disclosure exemption every year (its
# ultimate parent, The Bank of New York Mellon Corporation, publishes its own
# consolidated financial statements including a cash flow statement) - no
# Statement of Cash Flows exists in any year's accounts, confirmed directly in
# the FY2023 and FY2025 financial statements (identical wording) and
# previously also confirmed via 3 separate Companies House filings
# (FY2021/FY2023/FY2025). Pillar 3 disclosures, by contrast, are complete and
# strong for all 5 years, so this workbook keeps the standard 13-sheet
# structure but the "Cash Flow Statement" sheet documents the exemption
# instead of line items, and the Overview sheet omits the cash-flow chart.

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, calendar year-end (31 December)
YEAR_LABEL = {y: y for y in YEARS}

FS2025_URL = "https://www.bnymellon.com/content/dam/bnymellon/documents/pdf/investor-relations/Signed-2025-BNYMIL-Financial-Statements.pdf"
FS2023_URL = "https://www.bnymellon.com/content/dam/bnymellon/documents/pdf/investor-relations/bnymil-financial-statement-2023.pdf"

P3_2021_URL = "https://www.bnymellon.com/content/dam/bnymellon/documents/pdf/investor-relations/the-bank-of-new-york-mellon-international-limited-2021-pillar-3-disclosure.pdf"
P3_2022_URL = "https://www.bnymellon.com/content/dam/bnymellon/documents/pdf/investor-relations/the-bank-of-new-york-mellon-international-limited-2022-pillar-3-disclosure.pdf"
P3_2023_URL = "https://www.bnymellon.com/content/dam/bnymellon/documents/pdf/investor-relations/the-bank-of-new-york-mellon-international-limited-2023-pillar-3-disclosure.pdf"
P3_2024_URL = "https://www.bnymellon.com/content/dam/bnymellon/documents/pdf/investor-relations/the-bank-of-new-york-mellon-international-limited-2024-pillar-3-disclosure.pdf"
P3_2025_URL = "https://www.bnymellon.com/content/dam/bnymellon/documents/pdf/investor-relations/the-bank-of-new-york-mellon-international-limited-2025-pillar-3-disclosure.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: The Bank of New York Mellon (International) Limited (company 03236121, FRN 183100) is a wholly-"
    "owned subsidiary of The Bank of New York Mellon Corporation (US). Figures are the Company's own entity-level "
    "disclosure throughout; the 2021 Pillar 3 report separately labelled 'Consolidated' and 'Solo' bases but both "
    "were identical every year shown (the Company has no material subsidiaries of its own), and from the 2022 "
    "report onward BNY Mellon International's Pillar 3 disclosures present a single, unified figure. Functional/"
    "presentational currency is GBP throughout - no FX conversion needed."
)

EXEMPTION_NOTE = (
    "FRS 101 CASH-FLOW EXEMPTION: this entity's Annual Report and Financial Statements state every year: \"The "
    "Company's ultimate parent undertaking, The Bank of New York Mellon Corporation includes the Company and all "
    "its subsidiary undertakings in its consolidated financial statements... Accordingly, the Company is a "
    "qualifying entity for the purpose of FRS 101 disclosure exemptions... the Company has applied the exemptions "
    "available under FRS 101 in respect of the following disclosures: A Statement of cash flows and related "
    f"notes...\" - FY2025 Financial Statements, note 1.1, p.29 - {FS2025_URL}; identical wording confirmed in the "
    f"FY2023 Financial Statements, note 1.1, p.41 - {FS2023_URL}. This has also been independently confirmed via "
    "Companies House filings for FY2021, FY2023 and FY2025 (OCR'd scanned filings, prior research pass). No "
    "Statement of Cash Flows or cash-flow notes exist in any of the entity's published accounts for any year - this "
    "is a standing structural feature of the entity, not a one-off or a data gap. Per the project's established "
    "policy for this exemption (see United Trust Bank Limited, self-skipped for the same reason), this workbook is "
    "built as a PILLAR-3-ONLY variant: all 11 Pillar 3 metric sheets are fully populated below, but no cash flow "
    "figures exist to show. See the Overview sheet for the equivalent treatment there."
)

CASH_FLOW_SOURCES = ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE


def p3_sources(page):
    return (
        "Sources - The Bank of New York Mellon (International) Limited Pillar 3 Disclosure, Table 1: UK KM1 - Key "
        "metrics template (entity-level basis):\n"
        f"FY2025: Pillar 3 Disclosure, December 31, 2025, p.{page['FY2025']} - {P3_2025_URL}\n"
        f"FY2024: Pillar 3 Disclosure, December 31, 2024, p.{page['FY2024']} - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosure, December 31, 2023, p.{page['FY2023']} - {P3_2023_URL}\n"
        f"FY2022: Pillar 3 Disclosure, December 31, 2022, p.{page['FY2022']} - {P3_2022_URL}\n"
        f"FY2021: Pillar 3 Disclosure, December 31, 2021, p.{page['FY2021']} (\"1.8 Key metrics\") - {P3_2021_URL}\n"
        + ENTITY_NOTE
    )


KM1_PAGE = {"FY2025": "5", "FY2024": "6", "FY2023": "6", "FY2022": "8", "FY2021": "10-11"}

bw = BankWorkbook(bank_name="The Bank of New York Mellon (International) Limited", years=YEARS,
                   year_label=YEAR_LABEL, header_color="1F3B57")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (exemption note in place of line items)
# ---------------------------------------------------------------
rows = [
    ("SECTION", "No Statement of Cash Flows is published by this entity in any year", {}),
    ("DATA", "See the note below for the FRS 101 exemption this entity relies on every year, and why this "
             "workbook is built as a Pillar-3-only variant.", {}),
]

bw.add_cash_flow_sheet(
    title="The Bank of New York Mellon (International) Limited — Cash Flow Statement",
    subtitle="Not applicable — this entity takes the FRS 101 cash-flow-statement disclosure exemption every year. See source note below.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=260,
    unit_suffix="",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=130)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 1091, "FY2024": 955, "FY2023": 833, "FY2022": 733, "FY2021": 761})],
    p3_sources(KM1_PAGE),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "104.22%", "FY2024": "85.41%", "FY2023": "79.26%", "FY2022": "73.35%", "FY2021": "90.8%"})],
    p3_sources(KM1_PAGE),
    note="The FY2025 Pillar 3 Disclosure's FY2024 comparative column restates RWA (1,118 -> 1,091) and this ratio "
         "(85.41% -> 87.54%) versus the FY2024 report's own originally-reported figures - the FY2024 column above "
         "uses that year's own report as originally published, not the later restated comparative (consistent with "
         "this project's convention of preserving each year's own as-reported figures).",
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 1091, "FY2024": 955, "FY2023": 833, "FY2022": 733, "FY2021": 761})],
    p3_sources(KM1_PAGE),
    note="Tier 1 = CET1 every year (no AT1 instruments in issue).",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "104.22%", "FY2024": "85.41%", "FY2023": "79.26%", "FY2022": "73.35%", "FY2021": "90.8%"})],
    p3_sources(KM1_PAGE),
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 1091, "FY2024": 955, "FY2023": 833, "FY2022": 733, "FY2021": 761})],
    p3_sources(KM1_PAGE),
    note="Total capital = CET1 = Tier 1 every year (no AT1 or Tier 2 instruments in issue).",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "104.22%", "FY2024": "85.41%", "FY2023": "79.26%", "FY2022": "73.35%", "FY2021": "90.8%"})],
    p3_sources(KM1_PAGE),
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted exposure amount", {"FY2025": 1047, "FY2024": 1118, "FY2023": 1051, "FY2022": 999, "FY2021": 838})],
    p3_sources(KM1_PAGE),
    note="FY2024 shown as originally reported (1,118); the FY2025 Pillar 3 Disclosure's comparative column restates "
         "this to 1,091 - see the CET1 Ratio sheet note.",
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total exposure measure excluding claims on central banks", {"FY2025": 6449, "FY2024": 6276, "FY2023": 5888, "FY2022": 7602}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "16.92%", "FY2024": "15.22%", "FY2023": "14.15%", "FY2022": "9.64%"}),
        ("Leverage ratio (as reported, basis not specified) (%)", {"FY2021": "6.1%"}),
    ],
    p3_sources(KM1_PAGE),
    note="The FY2021 Pillar 3 Disclosure's 'Key metrics' page discloses only a single Leverage ratio figure without "
         "specifying an excluding/including-central-bank-claims split (that split, and the exposure-measure £m "
         "figure, first appear in the FY2022 report's KM1 template) - shown on its own row rather than assumed "
         "comparable to the 'excluding' basis used FY2022 onward. The Company is not subject to a binding leverage "
         "ratio requirement (does not meet the LREQ firm thresholds under the PRA Rulebook).",
)

metric(
    "LCR", "£m / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value (average)", {"FY2025": 5184, "FY2024": 6021, "FY2023": 6887, "FY2022": 8876}),
        ("Total net cash outflows, adjusted value", {"FY2025": 1669, "FY2024": 2532, "FY2023": 3305, "FY2022": 4801}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "317.37%", "FY2024": "240.33%", "FY2023": "211.60%", "FY2022": "185.66%", "FY2021": "173%"}),
    ],
    p3_sources(KM1_PAGE),
    note="LCR is presented on a 12-month average basis (4-quarter average for FY2022, per that report's own note). "
         "FY2021's Pillar 3 report discloses only the headline ratio (173%, Solo basis) on its 'Key metrics' chart "
         "page, with no HQLA/outflow/inflow £m breakdown available that year and no FY2021 comparative shown in the "
         "FY2022 report (which explicitly states comparatives were not provided for LCR/NSFR due to a change in "
         "reporting instructions) - left blank rather than guessed.",
)

metric(
    "NSFR", "£m / %",
    [
        ("Total available stable funding", {"FY2025": 2561, "FY2024": 2474, "FY2023": 2386, "FY2022": 3210}),
        ("Total required stable funding", {"FY2025": 672, "FY2024": 675, "FY2023": 650, "FY2022": 680}),
        ("NSFR ratio (%)", {"FY2025": "381.21%", "FY2024": "366.64%", "FY2023": "368.06%", "FY2022": "472.37%", "FY2021": "446%"}),
    ],
    p3_sources(KM1_PAGE),
    note="NSFR is presented on a 4-quarter average basis. FY2021's Pillar 3 report discloses only the headline "
         "ratio (446%, Solo basis) with no £m breakdown, and no FY2021 comparative appears in the FY2022 report "
         "(same reporting-instruction change noted on the LCR sheet). The FY2025 Pillar 3 Disclosure's FY2024 "
         "comparative column also restates NSFR (ASF 2,474->2,481, RSF 675->664, ratio 366.64%->373.99%) versus "
         "the FY2024 report's own originally-reported figures - the FY2024 column above uses that year's own report "
         "as originally published, consistent with this project's convention.",
)

metric(
    "MREL Ratio", "£m / %",
    [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})],
    p3_sources(KM1_PAGE),
    note="No MREL figure (numeric or qualitative) appears anywhere in any of the 5 Pillar 3 Disclosures or the "
         "available Financial Statements for this entity - no reason is stated.",
)

# ---------------------------------------------------------------
# Overview sheet (Pillar-3-only: no cash-flow chart)
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("CET1 Ratio", {"FY2025": "104.22%", "FY2024": "85.41%", "FY2023": "79.26%", "FY2022": "73.35%", "FY2021": "90.8%"}),
        ("Tier 1 Ratio", {"FY2025": "104.22%", "FY2024": "85.41%", "FY2023": "79.26%", "FY2022": "73.35%", "FY2021": "90.8%"}),
        ("Total Capital Ratio", {"FY2025": "104.22%", "FY2024": "85.41%", "FY2023": "79.26%", "FY2022": "73.35%", "FY2021": "90.8%"}),
        ("Leverage Ratio (excl. central bank claims)", {"FY2025": "16.92%", "FY2024": "15.22%", "FY2023": "14.15%", "FY2022": "9.64%"}),
        ("LCR", {"FY2025": "317.37%", "FY2024": "240.33%", "FY2023": "211.60%", "FY2022": "185.66%", "FY2021": "173%"}),
        ("NSFR", {"FY2025": "381.21%", "FY2024": "366.64%", "FY2023": "368.06%", "FY2022": "472.37%", "FY2021": "446%"}),
    ],
    note="This is a PILLAR-3-ONLY workbook: The Bank of New York Mellon (International) Limited takes the FRS 101 "
         "cash-flow-statement exemption every year (see the Cash Flow Statement sheet), so no cash flow summary or "
         "chart is shown here - only the Pillar 3 Key Metrics trend chart below. See each Pillar 3 sheet's own "
         "source citation for the underlying document/page.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BNY MELLON INTERNATIONAL FINANCIALS.xlsx")
