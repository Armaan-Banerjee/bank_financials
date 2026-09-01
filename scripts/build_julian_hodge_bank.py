import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# PILLAR-3-ONLY WORKBOOK: Julian Hodge Bank Limited (company 00743437, FRN 204439)
# takes the FRS 101 cash-flow-statement disclosure exemption in every one of its FY2021-FY2025
# Annual Reports - explicitly stated each year in Note 1 (Basis of preparation): "the Bank has
# applied the exemptions available under FRS 101 in respect of the following disclosures: A Cash
# Flow Statement and related notes; ..." No Statement of Cash Flows exists in any year's accounts.
# Pillar 3 / capital disclosures are rich for FY2021-FY2023 (full UK KM1-format Key Regulatory
# Metrics tables, standalone Pillar 3 documents), but FY2024-FY2025 have no standalone Pillar 3
# document published - only a brief unaudited "Capital risk management" note inside each year's
# own Annual Report giving CET1/RWA/ratios (no Leverage/LCR/NSFR for those two years). Follows the
# BNY Mellon International / ABC International Bank precedent: standard 13-sheet structure, but
# the Cash Flow Statement sheet documents the exemption instead of line items, and the Overview
# sheet omits the cash-flow chart.

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, fiscal year-end 30 September
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://hodgebank.co.uk/wp-content/uploads/2026/02/Hodge-AR-28.01.26.pdf"
AR2024_URL = "https://hodgebank.co.uk/wp-content/uploads/2025/02/Hodge-annual-report-21.02.25.pdf"
AR2023_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/Annual-report-Jan-25.01.24.pdf"
AR2022_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/Hodge-Annual-Report-April-04.04.23-optimised.pdf"
AR2021_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/Hodge-Annual-Report-2020_2021.pdf"
P3_2023_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/Hodge-pillar-3-11.03.24.pdf"
P3_2022_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/Hodge-pillar-3-19.06.23.pdf"
P3_2021_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/Hodge-Pillar-3-Document-2020_2021.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Julian Hodge Bank Limited (company 00743437, FRN 204439, incorporated 1962) is a "
    "privately-owned Cardiff-based bank; immediate parent Hodge Limited, ultimate parent The Carlyle Trust "
    "(Jersey) Limited. Fiscal year-end is 30 September. All 5 years text-native PDFs, no OCR required."
)

EXEMPTION_NOTE = (
    "FRS 101 CASH-FLOW EXEMPTION: every Annual Report FY2021-FY2025 states in Note 1 (Basis of preparation) that "
    "the Bank \"has applied the exemptions available under FRS 101 in respect of the following disclosures: A Cash "
    "Flow Statement and related notes; ...\" - e.g. Julian Hodge Bank Limited Annual Report 2025, Note 1.1, p.42 - "
    f"{AR2025_URL}. No Statement of Cash Flows exists in any of the entity's published accounts for any year in "
    "this window - a standing structural feature, not a one-off or data gap. Per the project's established policy "
    "for this exemption (see The Bank of New York Mellon (International) Limited / ABC International Bank plc), "
    "this workbook is built as a PILLAR-3-ONLY variant: all 11 Pillar 3 metric sheets are populated below, but no "
    "cash flow figures exist to show. See the Overview sheet for the equivalent treatment there."
)

CASH_FLOW_SOURCES = ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE

BASIS_NOTE = (
    "FY2021-FY2023: full UK KM1-format 'Key Regulatory Metrics' table from each year's own standalone Pillar 3 "
    "Disclosures document. FY2024-FY2025: no standalone Pillar 3 document was located on the bank's site (financial "
    "information page lists a Pillar 3 disclosure link for FY2018-FY2023 only) - CET1/RWA/ratio figures instead "
    "come from each year's own Annual Report 'Capital risk management (unaudited)' note, which does not include "
    "Leverage Ratio, LCR, or NSFR - those 3 metrics are genuinely unavailable for FY2024/FY2025 this session, not "
    "assumed absent."
)


def p3_sources(extra=""):
    return (
        "Sources - Julian Hodge Bank Limited:\n"
        f"FY2023: Hodge Bank Pillar 3 Disclosures - Period ended 30 September 2023, Table \"3 Key Regulatory "
        f"Metrics\", p.9 - {P3_2023_URL}\n"
        f"FY2022: Hodge Bank Pillar 3 Disclosures - Period ended 30 September 2022, Table \"3 Key Regulatory "
        f"Metrics\", p.12 - {P3_2022_URL}\n"
        f"FY2021: Hodge Bank Pillar 3 Disclosures - Period ended 30 September 2021, Table \"Key Metrics\", p.16 - "
        f"{P3_2021_URL}\n"
        f"FY2024: Julian Hodge Bank Limited Annual Report 2024, Note 32 'Capital risk management (unaudited)', "
        f"p.73 - {AR2024_URL}\n"
        f"FY2025: Julian Hodge Bank Limited Annual Report 2025, Note 34 'Capital risk management (unaudited)', "
        f"p.76 - {AR2025_URL}\n"
        + (extra + "\n" if extra else "") + BASIS_NOTE
    )


bw = BankWorkbook(bank_name="Julian Hodge Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="8B4513")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (exemption note in place of line items)
# ---------------------------------------------------------------
rows = [
    ("SECTION", "No Statement of Cash Flows is published by this entity in any year", {}),
    ("DATA", "See the note below for the FRS 101 exemption this entity relies on every year, and why this "
             "workbook is built as a Pillar-3-only variant.", {}),
]

bw.add_cash_flow_sheet(
    title="Julian Hodge Bank Limited — Cash Flow Statement",
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
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=170)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 162.8, "FY2024": 166.2, "FY2023": 172.9, "FY2022": 177, "FY2021": 143.8})],
    p3_sources(),
    note="FY2021's own report (P3 2021) shows CET1 = 143.8; the following year's Pillar 3 document (P3 2022) "
         "restates the FY2021 comparative to 144 (rounding to whole £m from that document's own precision) - "
         "each year's own originally-published figure is used per this project's convention.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "17.5%", "FY2024": "19.8%", "FY2023": "24.5%", "FY2022": "25.2%", "FY2021": "20.2%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 162.8, "FY2024": 166.2, "FY2023": 172.9, "FY2022": 177, "FY2021": 143.8})],
    p3_sources(),
    note="Tier 1 = CET1 every year (no AT1 instruments in issue - 'Hold all its capital in the form of Common "
         "Equity Tier 1 and Tier 2 capital', and Tier 2 = nil every year per the Pillar 3 documents). FY2024/FY2025 "
         "not separately labelled 'Tier 1' in the Annual Report's brief capital note but equal to CET1 by the same "
         "pattern confirmed directly in FY2021-FY2023.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "17.5%", "FY2024": "19.8%", "FY2023": "24.5%", "FY2022": "25.2%", "FY2021": "20.2%"})],
    p3_sources(),
    note="Equal to CET1 ratio every year - see Tier 1 Capital sheet note.",
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 162.8, "FY2024": 166.2, "FY2023": 172.9, "FY2022": 177, "FY2021": 143.8})],
    p3_sources(),
    note="Equal to CET1/Tier 1 every year - the Bank holds no Tier 2 capital in any year covered.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "17.5%", "FY2024": "19.8%", "FY2023": "24.5%", "FY2022": "25.2%", "FY2021": "20.2%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted assets / exposure amount", {"FY2025": 930.2, "FY2024": 841.1, "FY2023": 704.7, "FY2022": 705, "FY2021": 711.0})],
    p3_sources(),
    note="FY2021's own report (P3 2021) shows RWA = 711.0; the FY2022 Pillar 3 document's FY2021 comparative "
         "restates this to 711 (rounding only, immaterial) - each year's own originally-published figure is used.",
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total Basel III/leverage ratio exposure measure (£m)", {"FY2023": 1649.9, "FY2022": 1624, "FY2021": 1732.2}),
        ("Leverage Ratio (%)", {"FY2023": "10.5%", "FY2022": "10.9%", "FY2021": "8.3%"}),
    ],
    p3_sources(),
    note="FY2024/FY2025 not available - no standalone Pillar 3 document exists for those years and the Annual "
         "Report's brief 'Capital risk management' note does not include a leverage ratio. DATA QUALITY FLAG: the "
         "FY2022 Pillar 3 document's own FY2021 comparative column shows a materially different leverage exposure "
         "(£1,320m) and ratio (10.9%) than FY2021's own contemporaneous report (£1,732.2m / 8.3%) - a genuine "
         "cross-vintage restatement in the bank's own documents, not a transcription error. Per this project's "
         "convention, each year's own originally-published figure is used (FY2021 = 8.3%, not the later-restated "
         "10.9%) - worth double-checking if this workbook is relied on for leverage-ratio trend analysis.",
)

metric(
    "LCR", "£m / %",
    [
        ("Total HQLA after haircuts (£m)", {"FY2023": 230.4, "FY2022": 334, "FY2021": 479.5}),
        ("Total net cash outflow, adjusted value (£m)", {"FY2023": 130.2, "FY2022": 133, "FY2021": 137.1}),
        ("Liquidity Coverage Ratio (%)", {"FY2023": "176.9%", "FY2022": "252%", "FY2021": "349.6%"}),
    ],
    p3_sources(),
    note="FY2024/FY2025 not available - see Leverage Ratio sheet note. Year-end (point-in-time) values shown, "
         "per each source document's own basis ('year end value for LCR related metrics').",
)

metric(
    "NSFR", "£m / %",
    [
        ("Total available stable funding (£m)", {"FY2023": 1721.9, "FY2022": 1549, "FY2021": 1551.0}),
        ("Total required stable funding (£m)", {"FY2023": 1144.2, "FY2022": 1085, "FY2021": 922.7}),
        ("Net Stable Funding Ratio (%)", {"FY2023": "150.5%", "FY2022": "143%", "FY2021": "168.1%"}),
    ],
    p3_sources(),
    note="FY2024/FY2025 not available - see Leverage Ratio sheet note.",
)

metric(
    "MREL Ratio", "£m / %",
    [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})],
    p3_sources(),
    note="No MREL figure (numeric or qualitative) appears in any of the 3 standalone Pillar 3 documents reviewed, "
         "nor in either Annual Report's brief capital note - no reason is stated. Consistent with this small "
         "private bank not being set an independent MREL requirement by the Bank of England, the same pattern "
         "seen at other small UK banks in this project (e.g. Cynergy Bank, DF Capital Bank).",
)

# ---------------------------------------------------------------
# Overview sheet (Pillar-3-only: no cash-flow chart)
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("CET1 Ratio", {"FY2025": "17.5%", "FY2024": "19.8%", "FY2023": "24.5%", "FY2022": "25.2%", "FY2021": "20.2%"}),
        ("Tier 1 Ratio", {"FY2025": "17.5%", "FY2024": "19.8%", "FY2023": "24.5%", "FY2022": "25.2%", "FY2021": "20.2%"}),
        ("Total Capital Ratio", {"FY2025": "17.5%", "FY2024": "19.8%", "FY2023": "24.5%", "FY2022": "25.2%", "FY2021": "20.2%"}),
        ("Leverage Ratio", {"FY2023": "10.5%", "FY2022": "10.9%", "FY2021": "8.3%"}),
        ("LCR", {"FY2023": "176.9%", "FY2022": "252%", "FY2021": "349.6%"}),
        ("NSFR", {"FY2023": "150.5%", "FY2022": "143%", "FY2021": "168.1%"}),
    ],
    note="This is a PILLAR-3-ONLY workbook: Julian Hodge Bank Limited takes the FRS 101 cash-flow-statement "
         "exemption every year (see the Cash Flow Statement sheet), so no cash flow summary or chart is shown here "
         "- only the Pillar 3 Key Metrics trend chart below. Leverage/LCR/NSFR are only available FY2021-FY2023 - "
         "see each Pillar 3 sheet's own source citation for detail.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/JULIAN HODGE BANK FINANCIALS.xlsx")
