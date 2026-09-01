import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# PILLAR-3-ONLY WORKBOOK: ABC International Bank plc (company 02564490, FRN 149025)
# is a qualifying entity under FRS 101 and takes the "requirements of IAS 7 Statement
# of Cash Flows" exemption every year - explicitly stated in note 1.2 of its FY2024
# Annual Report: "there is no requirement to prepare a statement of cash flows in
# accordance with Financial Reporting Standard 101." No Statement of Cash Flows
# exists in any year's accounts. Pillar 3 / capital disclosures are available for
# 4 of 5 years (not FY2025 - no year-end Pillar 3 report or Financial Highlights
# table for FY2025 could be located; the FY2025 Companies House filing is a fully
# scanned/image-only PDF), so this follows the BNY Mellon International precedent:
# standard 13-sheet structure, but the Cash Flow Statement sheet documents the
# exemption instead of line items, and the Overview sheet omits the cash-flow chart.

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, calendar year-end (31 December)
YEAR_LABEL = {y: y for y in YEARS}

AR2024_URL = "https://www.bank-abc.com/en/ShareholderRelations/Annual%20Reports/ABC%20IB%20Annual%20Report%202024%20_%20Spreads%20for%20web.pdf"
AR2022_URL = "https://www.bank-abc.com/en/ShareholderRelations/Annual%20Reports/ABCIB%20Annual%20Report%202022.pdf"
P3_2024_URL = "https://www.bank-abc.com/en/CountrySites/Europe/London/Financial-Info/Basel%20Pillars/ABCIB%20Pillar%203%20final%20Board%202024%20.pdf"
P3_2023_URL = "https://www.bank-abc.com/en/CountrySites/Europe/London/Financial-Info/Basel%20Pillars/BH2407109%20-%20Bank%20ABC%20Pillar%203%20Disclosures%202023%20-%20Final%20website%20version.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: ABC International Bank plc (company 02564490, FRN 149025, incorporated 3 December 1990) is a "
    "wholly-owned subsidiary within the Bank ABC (Arab Banking Corporation B.S.C., Bahrain) group. FY2023 and FY2024 "
    "figures are on a CONSOLIDATED basis (ABCIB's own subsidiaries, e.g. Alphabet Nominees Limited - a nominee "
    "company, not a trading entity), taken from ABCIB's own UK KM1 Pillar 3 template. FY2021 and FY2022 figures are "
    "on a SOLO (entity-only) basis, taken from the Annual Report's 'Financial Highlights' table - no consolidated "
    "Pillar 3 KM1-format disclosure could be located for those two years (only the modern KM1 template, introduced "
    "for the FY2023 report onward, publishes a full metrics breakdown; earlier years' Pillar 3 documents could not "
    "be located on the bank's website or via Wayback Machine). This is a genuine basis break within the series, not "
    "a data-entry choice - flagged on every affected sheet."
)

EXEMPTION_NOTE = (
    "FRS 101 CASH-FLOW EXEMPTION: ABCIB's FY2024 Annual Report states (Note 1.2, Basis of preparation): \"ABCIB is "
    "not required to prepare group accounts since it qualifies for the exemptions available under Section 401 of "
    "the Companies Act 2006. In addition, there is no requirement to prepare a statement of cash flows in "
    "accordance with Financial Reporting Standard 101,\" and lists among the FRS 101 exemptions taken: \"The "
    f"requirements of IAS 7 Statement of Cash Flows.\" - ABC International Bank plc Annual Report 2024, p.55 - "
    f"{AR2024_URL}. No Statement of Cash Flows exists in any of the entity's published accounts for any year - this "
    "is a standing structural feature of the entity, not a one-off or a data gap. Per the project's established "
    "policy for this exemption (see The Bank of New York Mellon (International) Limited), this workbook is built "
    "as a PILLAR-3-ONLY variant: all 11 Pillar 3 metric sheets are populated below (4 of 5 years - FY2025 Pillar 3 "
    "disclosure/highlights could not be located; the FY2025 Companies House filing is a scanned, image-only PDF), "
    "but no cash flow figures exist to show. See the Overview sheet for the equivalent treatment there."
)

CASH_FLOW_SOURCES = ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE

BASIS_NOTE = (
    "FY2023-FY2024 shown on a CONSOLIDATED basis (ABCIB Pillar 3 Disclosures, UK KM1 template); FY2021-FY2022 "
    "shown on a SOLO basis (Annual Report Financial Highlights table - no consolidated Pillar 3 disclosure located "
    "for those years). See the Cash Flow Statement sheet's entity note for detail. FY2025 not available - no "
    "Pillar 3 disclosure or Financial Highlights table for FY2025 could be located (the FY2025 Companies House "
    "filing is scanned/image-only)."
)


def p3_sources(extra=""):
    return (
        "Sources - ABC International Bank plc:\n"
        f"FY2024 & FY2023 (consolidated): ABC International Bank plc Pillar 3 Report 2024, Table \"UK KM1 - Key "
        f"metrics template\", p.14 - {P3_2024_URL}\n"
        f"FY2023 (consolidated, as originally reported): ABC International Bank plc Pillar 3 Disclosures 2023, "
        f"Table 3: Key Regulatory Metrics, p.13 - {P3_2023_URL}\n"
        f"FY2022 & FY2021 (solo): ABC International Bank plc Annual Report 2022, Financial Highlights, p.31 - "
        f"{AR2022_URL}\n"
        + (extra + "\n" if extra else "") + BASIS_NOTE
    )


bw = BankWorkbook(bank_name="ABC International Bank plc", years=YEARS, year_label=YEAR_LABEL, header_color="0D7377")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (exemption note in place of line items)
# ---------------------------------------------------------------
rows = [
    ("SECTION", "No Statement of Cash Flows is published by this entity in any year", {}),
    ("DATA", "See the note below for the FRS 101 exemption this entity relies on every year, and why this "
             "workbook is built as a Pillar-3-only variant.", {}),
]

bw.add_cash_flow_sheet(
    title="ABC International Bank plc — Cash Flow Statement",
    subtitle="Not applicable — this entity takes the FRS 101 cash-flow-statement disclosure exemption every year. See source note below.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=280,
    unit_suffix="",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=150)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2024": 564.579, "FY2023": 547.665, "FY2022": 416.5, "FY2021": 418.8})],
    p3_sources(),
    note="FY2022/FY2021 are calculated (RWA x Tier 1 ratio, both solo basis) - no separate CET1/Tier 1 £m figure is "
         "disclosed for those years, only the ratio and total 'Capital base'. Assumes CET1 = Tier 1 (no AT1 "
         "instruments in issue), consistent with the pattern directly confirmed in FY2023-FY2024.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2024": "16.2%", "FY2023": "17.6%", "FY2022": "17.0%", "FY2021": "16.7%"})],
    p3_sources(),
    note="FY2023 shown as originally reported (17.6%, consolidated); the FY2024 Pillar 3 Report's FY2023 "
         "comparative column restates this to 17.7% alongside a small RWA restatement (see Total RWAs sheet) - "
         "immaterial, but shown as originally reported per this project's convention. FY2022/FY2021 labelled "
         "'Tier 1 Capital Ratio' in the source (solo basis) - assumed equal to CET1 ratio, see CET1 Capital sheet note.",
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2024": 564.579, "FY2023": 547.665, "FY2022": 416.5, "FY2021": 418.8})],
    p3_sources(),
    note="Tier 1 = CET1 every year (no AT1 instruments in issue). FY2022/FY2021 calculated - see CET1 Capital sheet note.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2024": "16.2%", "FY2023": "17.6%", "FY2022": "17.0%", "FY2021": "16.7%"})],
    p3_sources(),
    note="FY2023 shown as originally reported (consolidated) - see CET1 Ratio sheet note.",
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2024": 616.448, "FY2023": 598.786, "FY2022": 447, "FY2021": 460})],
    p3_sources(),
    note="FY2022/FY2021 ('Capital base') and FY2023-FY2024 ('Total capital') are directly disclosed, not calculated.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2024": "17.7%", "FY2023": "19.3%", "FY2022": "18.2%", "FY2021": "18.3%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted exposure amount", {"FY2024": 3486.256, "FY2023": 3104.763, "FY2022": 2450, "FY2021": 2508})],
    p3_sources(),
    note="FY2023 shown as originally reported (consolidated, 3,104.763m); the FY2024 Pillar 3 Report's FY2023 "
         "comparative column restates this to 3,101.197m - immaterial (~0.1%), shown as originally reported per "
         "this project's convention.",
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total exposure measure excluding claims on central banks (£m)", {"FY2024": 5540.164, "FY2023": 5155.039}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2024": "10.2%", "FY2023": "10.62%"}),
    ],
    p3_sources(),
    note="FY2022/FY2021 not available - the Annual Report Financial Highlights table (the only source located for "
         "those years) does not include a leverage ratio.",
)

metric(
    "LCR", "£m / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value - average (£m)", {"FY2024": 854.893, "FY2023": 699.862}),
        ("Total net cash outflows, adjusted value (£m)", {"FY2024": 252.133, "FY2023": 189.675}),
        ("Liquidity Coverage Ratio (%)", {"FY2024": "339.1%", "FY2023": "369.0%"}),
    ],
    p3_sources(),
    note="FY2023 LCR is sourced from the FY2024 Pillar 3 Report's comparative column - ABCIB's own FY2023 Pillar 3 "
         "Disclosures document (Table 3) does not include LCR at all (only capital and leverage metrics). "
         "FY2022/FY2021 not available.",
)

metric(
    "NSFR", "£m / %",
    [
        ("Total available stable funding (£m)", {"FY2024": 2339.367, "FY2023": 2053.004}),
        ("Total required stable funding (£m)", {"FY2024": 1802.627, "FY2023": 1504.583}),
        ("Net Stable Funding Ratio (%)", {"FY2024": "129.8%", "FY2023": "136.4%"}),
    ],
    p3_sources(),
    note="FY2023 NSFR is sourced from the FY2024 Pillar 3 Report's comparative column - same reason as the LCR "
         "sheet. FY2022/FY2021 not available.",
)

metric(
    "MREL Ratio", "£m / %",
    [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})],
    p3_sources(),
    note="No MREL figure (numeric or qualitative) appears in either Pillar 3 Report reviewed for this entity - no "
         "reason is stated. ABCIB's balance sheet size (~£3.5-4.3bn) is well below the thresholds at which the "
         "Bank of England typically sets an independent MREL requirement, consistent with no disclosure existing.",
)

# ---------------------------------------------------------------
# Overview sheet (Pillar-3-only: no cash-flow chart)
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("CET1 Ratio", {"FY2024": "16.2%", "FY2023": "17.6%", "FY2022": "17.0%", "FY2021": "16.7%"}),
        ("Tier 1 Ratio", {"FY2024": "16.2%", "FY2023": "17.6%", "FY2022": "17.0%", "FY2021": "16.7%"}),
        ("Total Capital Ratio", {"FY2024": "17.7%", "FY2023": "19.3%", "FY2022": "18.2%", "FY2021": "18.3%"}),
        ("Leverage Ratio (excl. central bank claims)", {"FY2024": "10.2%", "FY2023": "10.62%"}),
        ("LCR", {"FY2024": "339.1%", "FY2023": "369.0%"}),
        ("NSFR", {"FY2024": "129.8%", "FY2023": "136.4%"}),
    ],
    note="This is a PILLAR-3-ONLY workbook: ABC International Bank plc takes the FRS 101 cash-flow-statement "
         "exemption every year (see the Cash Flow Statement sheet), so no cash flow summary or chart is shown here "
         "- only the Pillar 3 Key Metrics trend chart below. FY2023-FY2024 are consolidated basis, FY2021-FY2022 "
         "are solo basis, FY2025 not available - see each Pillar 3 sheet's own source citation for detail.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/ABC INTERNATIONAL BANK FINANCIALS.xlsx")
