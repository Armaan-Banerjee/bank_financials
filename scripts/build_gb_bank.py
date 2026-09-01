import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


# PILLAR-3-ONLY WORKBOOK: GB Bank Limited's current official annual Pillar 3
# archive provides sufficient entity-level regulatory data, while this build
# does not transcribe cash-flow statements from the Companies House accounts.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

CH_URL = "https://find-and-update.company-information.service.gov.uk/company/10702260"
P3_2022_URL = "https://www.gbbank.co.uk/download/4416/?tmstv=1760374739"
P3_2023_URL = "https://www.gbbank.co.uk/download/4420/?tmstv=1760374863"
P3_2024_URL = "https://www.gbbank.co.uk/download/4423/?tmstv=1760374514"
P3_2025_URL = "https://www.gbbank.co.uk/download/5065/?tmstv=1766062359"

ENTITY_NOTE = (
    "ENTITY AND REPORTING BASIS: GB Bank Limited (Companies House 10702260; PRA FRN 850286) "
    "is the matched UK legal entity. The 2022-2025 Pillar 3 reports state that the reported "
    "figures are prepared on a solo basis. The 2025 report additionally records PRA permission, "
    "backdated to 1 October 2025, for an individual-consolidation method including SilverRock "
    "Financial Services Ltd going forward; the main 30 September 2025 table remains solo and is "
    "used here. GB Bank states that it publishes Pillar 3 annually under CRR Article 433b as a "
    "small and non-complex bank. FY2024 is a shortened nine-month period ended 30 September 2024 "
    "after the accounting period end changed; FY2021-FY2023 end on 31 December and FY2025 ends "
    "30 September."
)


def p3_sources():
    return (
        "Sources - GB Bank Limited official annual Pillar 3 disclosures, solo basis:\n"
        f"FY2025: Pillar 3 Disclosures 2025, UK KM1 p.13 - {P3_2025_URL}\n"
        f"FY2024: Pillar 3 Disclosures 2024, UK KM1 p.12 - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures 2023, UK KM1 p.11 - {P3_2023_URL}\n"
        f"FY2022 and FY2021: Pillar 3 Disclosures 2022, UK KM1 p.11 - {P3_2022_URL}\n"
        f"Companies House entity record and filing history: {CH_URL}/filing-history\n\n"
        + ENTITY_NOTE
    )


CAPITAL = {"FY2025": 104969, "FY2024": 69270, "FY2023": 19299, "FY2022": 22096, "FY2021": 16586}
CAPITAL_RATIO = {"FY2025": "19.14%", "FY2024": "45.71%", "FY2023": "56.46%", "FY2022": "234.21%", "FY2021": "403.37%"}
RWA = {"FY2025": 548458, "FY2024": 151536, "FY2023": 34184, "FY2022": 9434, "FY2021": 4112}
LEVERAGE_EXPOSURE = {"FY2025": 2114122, "FY2024": 747677, "FY2023": 48734, "FY2022": 23445, "FY2021": 17606}
LEVERAGE_RATIO = {"FY2025": "4.97%", "FY2024": "9.26%", "FY2023": "39.60%", "FY2022": "94.25%", "FY2021": "94.21%"}
HQLA = {"FY2025": 1095636, "FY2024": 427498, "FY2023": 209812, "FY2022": 18436, "FY2021": 8698}
NET_OUTFLOWS = {"FY2025": 522180, "FY2024": 139823, "FY2023": 50415, "FY2022": 92, "FY2021": 0}
LCR = {"FY2025": "210%", "FY2024": "306%", "FY2023": "416%", "FY2022": "20,091%", "FY2021": "9,999.99%"}
ASF = {"FY2025": 2224154, "FY2024": 510589, "FY2023": 203914, "FY2022": 20742, "FY2021": 16546}
RSF = {"FY2025": 1162308, "FY2024": 94820, "FY2023": 6041, "FY2022": 1006, "FY2021": 1696}
NSFR = {"FY2025": "191%", "FY2024": "538%", "FY2023": "3,375%", "FY2022": "2,061.89%", "FY2021": "978.24%"}

bw = BankWorkbook(bank_name="GB Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="205072")

bw.add_cash_flow_sheet(
    title="GB Bank Limited — Cash Flow Statement",
    subtitle="Not populated in this Pillar-3-only build; see the exemption/access note below.",
    rows=[
        ("SECTION", "Cash-flow data not transcribed", {}),
        ("DATA", "This workbook is a Pillar-3-only variant. The official GB Bank Pillar 3 archive provides the regulatory data; no cash-flow figures are included here.", {}),
    ],
    sources_text=(
        "CASH-FLOW SCOPE NOTE: This build intentionally does not transcribe the Companies House account cash-flow statements. "
        "The current official annual Pillar 3 reports are sufficient for the 11 regulatory metric sheets. See the Companies House "
        f"filing history for the available accounts: {CH_URL}/filing-history\n\n{ENTITY_NOTE}"
    ),
    first_col_width=100,
    source_height=220,
    unit_suffix="",
)


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=58, source_height=210)


metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", CAPITAL)])
metric("CET1 Ratio", "%", [("Common Equity Tier 1 (CET1) ratio", CAPITAL_RATIO)])
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", CAPITAL)], note="No AT1 instruments are disclosed in the annual KM1 tables; Tier 1 equals CET1 throughout.")
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", CAPITAL_RATIO)])
metric("Total Capital", "£'000", [("Total capital", CAPITAL)], note="No AT1 or Tier 2 instruments are disclosed in the annual KM1 tables; total capital equals CET1 throughout.")
metric("Total Capital Ratio", "%", [("Total capital ratio", CAPITAL_RATIO)])
metric(
    "Total RWAs", "£'000", [("Total risk-weighted exposure amount", RWA)],
    note=(
        "The 2023 Pillar 3 report prints £2,735k for 2023 RWA, which is inconsistent with its own 56.46% capital ratio. "
        "The 2024 report's 2023 comparative prints £34,184k, which reconciles to the reported capital and ratio; £34,184k is used here."
    ),
)
metric("Leverage Ratio", "£'000 / %", [
    ("Total exposure measure excluding claims on central banks", LEVERAGE_EXPOSURE),
    ("Leverage ratio excluding claims on central banks (%)", LEVERAGE_RATIO),
])
metric("LCR", "£'000 / %", [
    ("Total high-quality liquid assets (HQLA), weighted value - average", HQLA),
    ("Total net cash outflows, adjusted value", NET_OUTFLOWS),
    ("Liquidity coverage ratio (%)", LCR),
])
metric("NSFR", "£'000 / %", [
    ("Total available stable funding", ASF),
    ("Total required stable funding", RSF),
    ("Net stable funding ratio (%)", NSFR),
])
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={"MREL Ratio": "No quantitative MREL figure was located in the official 2022-2025 Pillar 3 reports reviewed."},
)

bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("CET1 Ratio", CAPITAL_RATIO),
        ("Leverage Ratio", LEVERAGE_RATIO),
        ("LCR", LCR),
        ("NSFR", NSFR),
    ],
    note=(
        "PILLAR-3-ONLY WORKBOOK: no cash-flow figures are transcribed. Regulatory metrics are from GB Bank Limited's official "
        "annual solo-basis Pillar 3 disclosures. FY2024 covers nine months to 30 September 2024; FY2025 covers the year to "
        "30 September 2025. See each detail sheet for source pages and the documented 2023 RWA inconsistency."
    ),
)

bw.save("/Users/armaan/code/katalysis/banks/GB BANK FINANCIALS.xlsx")
