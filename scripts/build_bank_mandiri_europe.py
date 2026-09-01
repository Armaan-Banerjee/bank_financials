import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# PILLAR-3-ONLY WORKBOOK: Bank Mandiri (Europe) Limited (company 03793679, FRN 204424)
# is a qualifying entity under FRS 101 and takes the "presentation of a cash-flow
# statement" (IAS 7) disclosure exemption every year - explicitly stated in Note 1.4
# "Disclosure Exemptions" of its FY2025 Annual Report, deferring to the accounts of
# its parent, PT Bank Mandiri (Persero) Tbk. Confirmed as a standing feature by
# checking both the FY2020 filing (earliest available, filed 2021) and the FY2025
# filing (most recent) - no Contents-page entry for a cash flow statement in either,
# 5 years apart. Follows the BNY Mellon International / ABC International Bank
# precedent: 13-sheet structure, Cash Flow Statement sheet documents the exemption
# instead of line items, Overview sheet omits the cash-flow chart.
#
# The Bank's functional currency is US Dollars (Note 1.2). No dedicated Pillar 3
# document exists - the only capital/liquidity disclosures found are a narrative
# paragraph + "Key Performance Indicator" table in the Strategic Report of each
# Annual Report, giving only a combined Total Capital Ratio (labelled "Capital
# Adequacy Ratio", Own Funds / Total RWA - no separate CET1/Tier 1 breakdown exists
# anywhere), LCR, NSFR, and total "regulatory capital resources" (Own Funds, $m).
# This KPI table format was only introduced from the FY2023 Annual Report onward
# (FY2022's own report has a KPI table with no capital/liquidity rows, and no
# capital/liquidity narrative was found in its Strategic Report or Directors'
# Report) - FY2022's figures come from FY2023's own comparative column instead.
# FY2021 could not be found in any source checked (FY2022 filing has no numeric
# capital/liquidity disclosure at all) - left blank, not estimated.

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, calendar year-end (31 December)
YEAR_LABEL = {y: y for y in YEARS}

# ---------------------------------------------------------------
# FX conversion (functional currency USD; converting to £ per this project's
# established FX methodology - see build_zenith.py / build_smbc.py precedent).
# Only point-in-time (stock) figures need conversion here - there's no cash flow
# statement, so no average/flow rate is needed.
# Rates are Bank of England GBP/USD spot via poundsterlinglive.com's published
# archive, £1 = $X, same table used throughout this project's USD-reporting banks.
# ---------------------------------------------------------------
FX_SPOT = {
    "FY2022": 1.2097,  # 30 Dec 2022 (31st was a Saturday)
    "FY2023": 1.2732,  # 29 Dec 2023 (31st was a Sunday)
    "FY2024": 1.2515,  # 31 Dec 2024
    "FY2025": 1.3448,  # 31 Dec 2025
}


def stock(usd):
    """Point-in-time (capital/RWA) figures, £'000, at that year's period-end spot rate."""
    return {y: round(v / FX_SPOT[y] / 1000, 0) for y, v in usd.items()}


FY2025_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/03793679/filing-history/MzUyODU0NjIyMmFkaXF6a2N4/document?format=pdf&download=0"
FY2024_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/03793679/filing-history/MzQ2ODc4NDgyMGFkaXF6a2N4/document?format=pdf&download=0"
FY2023_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/03793679/filing-history/MzQyNjk5Njk1M2FkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "ENTITY NOTE: Bank Mandiri (Europe) Limited (company 03793679, FRN 204424, incorporated 22 June 1999 as "
    "'Exitmode Limited', renamed 26 July 1999) is a wholly-owned UK subsidiary of PT Bank Mandiri (Persero) Tbk, "
    "Indonesia's largest bank by assets. All figures below are on the Bank's own entity-level basis - it has no "
    "subsidiaries of its own."
)

EXEMPTION_NOTE = (
    "FRS 101 CASH-FLOW EXEMPTION: the FY2025 Annual Report states (Note 1.4, Disclosure Exemptions): \"As permitted "
    "by FRS 101, the Company has taken advantage of the disclosure exemptions available under that standard "
    "concerning the presentation of comparative information in respect of certain assets, presentation of a "
    "cash-flow statement, standards not yet effective, impairment of assets and related party transactions between "
    "two or more wholly owned members of the group. Where required, equivalent disclosures are given in the "
    "accounts of PT Bank Mandiri (Persero) Tbk\", and explicitly lists 'IAS 7 Statement of Cash Flows and related "
    f"notes' among the exemptions applied - Bank Mandiri (Europe) Limited Annual Report FY2025, p.24-25 - "
    f"{FY2025_AR_URL}. No Statement of Cash Flows appears in the Contents page of either the FY2020 (earliest "
    "available Companies House filing) or FY2025 (most recent) accounts, confirming this is a standing structural "
    "feature across the entity's history, not a one-off. Per the project's established policy for this exemption "
    "(see The Bank of New York Mellon (International) Limited / ABC International Bank plc), this workbook is "
    "built as a PILLAR-3-ONLY variant: the capital/liquidity metrics that are disclosed are populated below, but no "
    "cash flow figures exist to show. See the Overview sheet for the equivalent treatment there."
)

CASH_FLOW_SOURCES = ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE

NOT_DISCLOSED_NOTE = (
    "No dedicated Pillar 3 document is published by this entity - the only capital/liquidity disclosures found are "
    "a narrative paragraph and Key Performance Indicator table in each Annual Report's Strategic Report, which give "
    "only a single combined Total Capital Ratio (no CET1/Tier 1 breakdown), LCR, and NSFR. This metric is not "
    "disclosed in any form found in any of the 4 Annual Reports (FY2022-FY2025) or the FY2020 filing checked."
)


def p3_sources(extra=""):
    return (
        "Sources - Bank Mandiri (Europe) Limited (figures reported in US Dollars, converted to £ at the Bank of "
        "England GBP/USD spot rate as at each fiscal year-end - see FX conversion note below; % ratios shown "
        "exactly as reported, not converted):\n"
        f"FY2025 & FY2024: Bank Mandiri (Europe) Limited Annual Report FY2025, Strategic Report \"Key Performance "
        f"Indicator\" table, p.6 - {FY2025_AR_URL}\n"
        f"FY2024 (as originally reported) & FY2023: Bank Mandiri (Europe) Limited Annual Report FY2024, Strategic "
        f"Report \"Key Performance Indicator\" table, p.6 - {FY2024_AR_URL}\n"
        f"FY2023 (as originally reported) & FY2022: Bank Mandiri (Europe) Limited Annual Report FY2023, Strategic "
        f"Report \"Key Performance Indicator\" table, p.6 - {FY2023_AR_URL}\n"
        "FX rates (£1 = $X, Bank of England spot via poundsterlinglive.com): 31 Dec 2022 1.2097; 29 Dec 2023 "
        "1.2732 (31st was a Sunday); 31 Dec 2024 1.2515; 31 Dec 2025 1.3448.\n"
        + (extra + "\n" if extra else "")
        + "FY2022's Total Capital Ratio/LCR/NSFR are sourced from the FY2023 Annual Report's own comparative column "
          "- the FY2022 Annual Report's own KPI table and Strategic Report do not include these figures at all "
          "(this KPI format was only introduced from the FY2023 report onward). FY2021 could not be found in any "
          "form (numeric or narrative) in the FY2022 Annual Report - left blank, not estimated."
    )


bw = BankWorkbook(bank_name="Bank Mandiri (Europe) Limited", years=YEARS, year_label=YEAR_LABEL, header_color="8B0000")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (exemption note in place of line items)
# ---------------------------------------------------------------
rows = [
    ("SECTION", "No Statement of Cash Flows is published by this entity in any year", {}),
    ("DATA", "See the note below for the FRS 101 exemption this entity relies on every year, and why this "
             "workbook is built as a Pillar-3-only variant.", {}),
]

bw.add_cash_flow_sheet(
    title="Bank Mandiri (Europe) Limited — Cash Flow Statement",
    subtitle="Not applicable — this entity takes the FRS 101 cash-flow-statement disclosure exemption every year. See source note below.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=300,
    unit_suffix="",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=170)


TOTAL_CAPITAL_USD = {"FY2025": 56_400_000, "FY2024": 54_300_000, "FY2023": 52_300_000, "FY2022": 49_710_000}
CAR = {"FY2025": "33.59%", "FY2024": "42.90%", "FY2023": "34.30%", "FY2022": "34.09%"}
# Calculated: Own Funds / CAR - no separate RWA figure is directly disclosed anywhere.
RWA_USD = {"FY2025": 167_907_000, "FY2024": 126_573_000, "FY2023": 152_478_000, "FY2022": 145_820_000}

# Sheet order matches the project-wide standard (CET1 Capital/Ratio, Tier 1 Capital/Ratio,
# Total Capital/Ratio, Total RWAs, Leverage Ratio, LCR, NSFR, MREL Ratio) even though this
# entity only discloses the Total Capital/RWA/LCR/NSFR metrics.
bw.add_not_disclosed_metric_sheets(
    ["CET1 Capital", "CET1 Ratio", "Tier 1 Capital", "Tier 1 Ratio"],
    p3_sources(),
    per_note={m: NOT_DISCLOSED_NOTE for m in ["CET1 Capital", "CET1 Ratio", "Tier 1 Capital", "Tier 1 Ratio"]},
)

metric(
    "Total Capital", "£'000 (conv. from USD)",
    [("Regulatory capital resources (\"Own Funds\")", stock(TOTAL_CAPITAL_USD))],
    p3_sources(),
    note="No CET1/Tier 1 breakdown is disclosed anywhere in the source - only this single combined 'regulatory "
         "capital resources' figure. See CET1 Capital / Tier 1 Capital sheets.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Capital Adequacy Ratio / Total Capital Ratio (Own Funds / Total Risk Weighted Asset)", CAR)],
    p3_sources(),
)

metric(
    "Total RWAs", "£'000 (conv. from USD)",
    [("Total risk-weighted assets", stock(RWA_USD))],
    p3_sources(),
    note="CALCULATED, not directly disclosed - derived as regulatory capital resources ÷ Total Capital Ratio for "
         "each year. No RWA figure appears in any source checked.",
)

bw.add_not_disclosed_metric_sheets(
    ["Leverage Ratio"], p3_sources(), per_note={"Leverage Ratio": NOT_DISCLOSED_NOTE},
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio (%)", {"FY2025": "446.89%", "FY2024": "382%", "FY2023": "264.29%", "FY2022": "147.59%"})],
    p3_sources(),
    note="No £/$ breakdown (HQLA, net cash outflows) is disclosed anywhere - only the ratio itself. FY2025 shown to "
         "2 d.p. as stated in the Strategic Report narrative (446.89%); the report's own KPI table rounds this to 447%.",
)

metric(
    "NSFR", "%",
    [("Net Stable Fund Ratio (%)", {"FY2025": "121.85%", "FY2024": "142%", "FY2023": "131.85%", "FY2022": "143.26%"})],
    p3_sources(),
    note="No £/$ breakdown (available/required stable funding) is disclosed anywhere - only the ratio itself. "
         "FY2025 shown to 2 d.p. as stated in the Strategic Report narrative (121.85%); the report's own KPI table "
         "rounds this to 122%.",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources(), per_note={"MREL Ratio": NOT_DISCLOSED_NOTE},
)

# ---------------------------------------------------------------
# Overview sheet (Pillar-3-only: no cash-flow chart)
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("Total Capital Ratio", CAR),
        ("LCR", {"FY2025": "446.89%", "FY2024": "382%", "FY2023": "264.29%", "FY2022": "147.59%"}),
        ("NSFR", {"FY2025": "121.85%", "FY2024": "142%", "FY2023": "131.85%", "FY2022": "143.26%"}),
    ],
    note="This is a PILLAR-3-ONLY workbook: Bank Mandiri (Europe) Limited takes the FRS 101 cash-flow-statement "
         "exemption every year (see the Cash Flow Statement sheet), so no cash flow summary or chart is shown here "
         "- only the capital/liquidity ratio trend chart below. No dedicated Pillar 3 document is published by this "
         "entity; only a combined Total Capital Ratio (no CET1/Tier 1 breakdown), LCR, and NSFR are disclosed, in "
         "each Annual Report's Strategic Report. FY2021 not available - see each sheet's own source citation.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BANK MANDIRI EUROPE FINANCIALS.xlsx")
