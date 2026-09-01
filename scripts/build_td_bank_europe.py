import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

CH_FILINGS = "https://find-and-update.company-information.service.gov.uk/company/02734652/filing-history"
REGULATORY_PAGE = "https://www.tdsecurities.com/ca/en/legal"
P3_URL = {
    "FY2025": "https://www.tdsecurities.com/tds/document/Pillar-3-Disclosure-Oct-2025",
    "FY2024": "https://www.tdsecurities.com/tds/document/Pillar-3-Disclosure-Oct-2024",
    "FY2023": "https://www.tdsecurities.com/tds/document/Pillar-3-Disclosure-2023",
    "FY2022": "https://www.tdsecurities.com/tds/document/Pillar-3-Disclosure-2022",
    "FY2021": "https://www.tdsecurities.com/tds/document/Pillar-3-Disclosure-2022",
}

ENTITY_NOTE = (
    "TD Bank Europe Limited (TDBEL; Companies House company 02734652; FRN 165556) is the UK PRA/FCA-authorised "
    "banking entity covered by this workbook. Companies House filings show accounts through 31 October 2025. "
    "The 2023, 2024 and 2025 Pillar 3 reports state that TDBEL is the sole/single operating regulated UK subsidiary "
    "and present the current disclosure basis as solo. The TD regulatory page states that prior-year disclosures were "
    "included in Toronto-Dominion Investments B.V.'s Pillar 3 report at UK-consolidation level; this is a basis break, "
    "not a claim that the FY2021 comparative is directly comparable to the later solo series."
)


def p3_sources():
    return (
        "Sources - TD Bank Europe Limited annual Pillar 3 disclosures (amounts in CAD millions; ratios as reported):\n"
        "FY2025: TD Bank Europe Limited Pillar 3 Disclosure, year ended 31 October 2025, Appendix 1 Table 21 "
        "pp.34-35 and capital tables pp.13-14 - " + P3_URL["FY2025"] + "\n"
        "FY2024: TD Bank Europe Limited Pillar 3 Disclosure, year ended 31 October 2024, Appendix 1 Table 21 "
        "p.34 and capital tables p.13 - " + P3_URL["FY2024"] + "\n"
        "FY2023: TD Bank Europe Limited Pillar 3 Disclosure, year ended 31 October 2023, Appendix 1 Table 21 "
        "p.35 and capital tables p.13 - " + P3_URL["FY2023"] + "\n"
        "FY2022: TD Bank Europe Limited Pillar 3 Disclosure, year ended 31 October 2022, Appendix 1 Table 21 "
        "p.35 and capital tables p.13 - " + P3_URL["FY2022"] + "\n"
        "FY2021: 2021 comparative column in the 2022 TD Bank Europe Limited Pillar 3 Disclosure, Appendix 1 Table 21 "
        "p.35 and capital tables p.13 - " + P3_URL["FY2021"] + "\n"
        "Regulatory source index and basis-transition statement: " + REGULATORY_PAGE + "\n"
        + ENTITY_NOTE
    )


bw = BankWorkbook(
    bank_name="TD Bank Europe Limited",
    years=YEARS,
    year_label=YEAR_LABEL,
    header_color="2A3E5C",
)

# TDBEL's accounts use the applicable small-company/FRS exemption and do not
# publish a Statement of Cash Flows. Keep the standard sheet so the omission is
# explicit and the workbook retains the project's normal 13-sheet structure.
CASH_FLOW_SOURCES = (
    "No Statement of Cash Flows is included because TD Bank Europe Limited's published accounts take the applicable "
    "cash-flow-statement exemption. This workbook is therefore Pillar-3-only for quantitative purposes. Entity and "
    "filing identity: " + CH_FILINGS + "\n" + ENTITY_NOTE
)
bw.add_cash_flow_sheet(
    title="TD Bank Europe Limited — Cash Flow Statement",
    subtitle="Pillar-3-only build: no cash-flow statement published under the entity's applicable exemption.",
    rows=[("SECTION", "No Statement of Cash Flows is published by this entity", {})],
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=190,
    unit_suffix=" (not disclosed)",
)


def metric(name, unit, rows, note=None):
    bw.add_metric_sheet(
        name,
        unit,
        rows,
        p3_sources(),
        note=note,
        first_col_width=60,
        source_height=250,
    )


# All amounts are as reported in CAD MM. The 2021 values are the comparative
# column in the FY2022 report and are separately identified in the note below.
CET1 = {"FY2025": 1269, "FY2024": 1206, "FY2023": 1159, "FY2022": 1103, "FY2021": 1050}
RWA = {"FY2025": 801, "FY2024": 805, "FY2023": 1635, "FY2022": 1261, "FY2021": 1096}
CET1_RATIO = {"FY2025": "158%", "FY2024": "150%", "FY2023": "71%", "FY2022": "87%", "FY2021": "96%"}
LEVERAGE_EXPOSURE = {"FY2025": 25214, "FY2024": 23692, "FY2023": 23004, "FY2022": 23408, "FY2021": 20484}
LEVERAGE_RATIO = {"FY2025": "5.0%", "FY2024": "5.1%", "FY2023": "5.0%", "FY2022": "4.7%", "FY2021": "5.1%"}
LCR = {"FY2025": "4039%", "FY2024": "3170%", "FY2023": "2575%", "FY2022": "29989%", "FY2021": "18136%"}
NSFR = {"FY2025": "5467%", "FY2024": "5240%", "FY2023": "6804%", "FY2022": "8307%", "FY2021": "800%"}

TRANSITION_NOTE = (
    "FY2021 is taken from the 2021 comparative column in the FY2022 TDBEL Pillar 3 report. The TD regulatory page "
    "states that prior-year disclosures were previously included in the Toronto-Dominion Investments B.V. report at "
    "UK-consolidation level, while later reports are solo TDBEL. Treat FY2021 as a transition/comparative year and "
    "do not interpret the full series as basis-homogeneous."
)

metric("CET1 Capital", "CAD MM", [("Common Equity Tier 1 (CET1) capital", CET1)], TRANSITION_NOTE)
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 ratio", CET1_RATIO)], TRANSITION_NOTE)
metric("Tier 1 Capital", "CAD MM", [("Tier 1 capital", CET1)], "TDBEL reports no AT1 capital; Tier 1 equals CET1 in each disclosed year.\n" + TRANSITION_NOTE)
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", CET1_RATIO)], TRANSITION_NOTE)
metric("Total Capital", "CAD MM", [("Total capital", CET1)], "TDBEL reports no AT1 or Tier 2 capital; total capital equals CET1 in each disclosed year.\n" + TRANSITION_NOTE)
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", CET1_RATIO)], TRANSITION_NOTE)
metric("Total RWAs", "CAD MM", [("Total risk-weighted exposure amount", RWA)], TRANSITION_NOTE)
metric(
    "Leverage Ratio",
    "CAD MM / %",
    [
        ("Total exposure measure excluding claims on central banks", LEVERAGE_EXPOSURE),
        ("Leverage ratio excluding claims on central banks", LEVERAGE_RATIO),
    ],
    TRANSITION_NOTE,
)
metric("LCR", "%", [("Liquidity coverage ratio", LCR)], TRANSITION_NOTE)
metric(
    "NSFR",
    "%",
    [("Net stable funding ratio", NSFR)],
    "The FY2025 report's introductory key-metrics table states 5,820% for FY2025, while Appendix 1 Table 21 states "
    "5,467%; this workbook uses the Appendix 1 value and preserves the discrepancy in this note.\n" + TRANSITION_NOTE,
)
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={"MREL Ratio": "No numeric MREL ratio was identified in the reviewed 2021 comparative or FY2022-FY2025 TD Bank Europe Pillar 3 reports."},
)

bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit="CAD MM",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Tier 1 Ratio", CET1_RATIO),
        ("Total Capital Ratio", CET1_RATIO),
        ("Leverage Ratio", LEVERAGE_RATIO),
        ("LCR", LCR),
        ("NSFR", NSFR),
    ],
    note=(
        "Pillar-3-only workbook. No cash-flow totals are shown because the entity's accounts take the applicable "
        "cash-flow-statement exemption. All quantitative figures are reported in CAD MM or percentages. " + TRANSITION_NOTE
    ),
)

bw.save("/Users/armaan/code/katalysis/banks/TD BANK EUROPE FINANCIALS.xlsx")
