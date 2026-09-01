import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {year: year for year in YEARS}

CH_URL = "https://find-and-update.company-information.service.gov.uk/company/00938937/filing-history"
P3_ARCHIVE_URL = "https://jpmorganchaseco.gcs-web.com/ir/sec-other-filings/basel-pillar-and-lcr-disclosures/pillar-uk/"
P3_2025_URL = "https://jpmorganchaseco.gcs-web.com/static-files/a51475c0-d908-423e-b8de-6410d277a867"
P3_2024_URL = "https://jpmorganchaseco.gcs-web.com/static-files/a170e6df-d951-42fc-9897-2aa04d681885"
AR_2024_URL = "https://jpmorganchaseco.gcs-web.com/static-files/b200f4be-f143-4934-9589-9f44bcadd9be"

ENTITY_NOTE = (
    "ENTITY/BASIS NOTE: J.P. Morgan Europe Limited (Companies House 00938937; "
    "PRA FRN 124579) is the assigned UK legal entity. This workbook uses the "
    "JPMEL columns in JPMorgan's separate Annual Solo Pillar 3 disclosures, "
    "not JPMorgan Chase group, JPMorgan Chase Bank N.A., JPMorgan Securities "
    "plc, JPMorgan SE, or another JPMorgan subsidiary. The 2024 JPMEL annual "
    "accounts state that the financial statements are prepared under FRS 101 "
    "Reduced Disclosure Framework; no cash-flow statement is therefore filled "
    "from a different entity or group report."
)

P3_SOURCES = (
    "Sources - J.P. Morgan Europe Limited standalone Pillar 3 disclosures, "
    "GBP millions, UK KM1 Table 2 and related standalone tables:\n"
    f"FY2025: P3 Annual Solo 2025, Table 2 UK KM1 for JPMEL (and Tables 4, 9, "
    f"33, 36 and 38 where applicable) - {P3_2025_URL}\n"
    f"FY2024: P3 Annual Solo 2024, Table 2 UK KM1 for JPMEL (FY2024 current "
    f"and FY2023 comparative) - {P3_2024_URL}\n"
    "FY2023 is taken from the FY2024 disclosure's JPMEL comparative column. "
    "No JPMEL standalone annual-solo KM1 was located for FY2021 or FY2022; "
    "group and other-entity disclosures are deliberately not substituted.\n"
    f"Official JPMorgan UK Pillar 3 archive - {P3_ARCHIVE_URL}\n"
    + ENTITY_NOTE
)

CASH_FLOW_SOURCES = (
    "CASH-FLOW EXEMPTION: JPMEL's 2024 annual accounts state that the company "
    "uses FRS 101 Reduced Disclosure Framework. A statement of cash flows is "
    "not presented in the standalone accounts reviewed, so no group or other "
    "entity cash flows are substituted. Companies House filing history: "
    f"{CH_URL}\n"
    f"JPMEL 2024 annual accounts, accounting basis - {AR_2024_URL}\n"
    + ENTITY_NOTE
)

bw = BankWorkbook(
    bank_name="J.P. Morgan Europe Limited",
    years=YEARS,
    year_label=YEAR_LABEL,
    header_color="1F4E79",
)

bw.add_cash_flow_sheet(
    title="J.P. Morgan Europe Limited — Statement of Cash Flows",
    subtitle="Not presented: FRS 101 reduced-disclosure exemption; no substitute group/entity data used.",
    rows=[
        ("SECTION", "FRS 101 cash-flow presentation", {}),
        ("DATA", "Standalone statement of cash flows", {year: "Not presented under FRS 101" for year in YEARS}),
    ],
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=230,
    unit_suffix="",
)


def metric(name, unit, label, values, note=None):
    bw.add_metric_sheet(
        name,
        unit,
        [(label, values)],
        P3_SOURCES,
        note=note,
        first_col_width=58,
        source_height=230,
    )


CAPITAL = {"FY2025": 2594, "FY2024": 2327, "FY2023": 1429}
RWA = {"FY2025": 1041, "FY2024": 628, "FY2023": 440}
CAPITAL_RATIO = {"FY2025": "249.23%", "FY2024": "370.56%", "FY2023": "325.00%"}
LEVERAGE = {"FY2025": "94.12%", "FY2024": "98.73%", "FY2023": "65.05%"}
LCR = {"FY2025": "241.17%", "FY2024": "230.90%", "FY2023": "276.70%"}
NSFR = {"FY2025": "155.44%", "FY2024": "158.44%", "FY2023": "180.37%"}

GAP_NOTE = (
    "Only FY2023-FY2025 are populated: FY2023 is the FY2024 JPMEL KM1 "
    "comparative column. FY2021-FY2022 standalone JPMEL figures were not "
    "located, and consolidated or other-entity values are not substituted."
)

metric("CET1 Capital", "£m", "Common Equity Tier 1 (CET1) capital", CAPITAL, GAP_NOTE)
metric("CET1 Ratio", "%", "CET1 ratio", CAPITAL_RATIO, GAP_NOTE)
metric("Tier 1 Capital", "£m", "Tier 1 capital", CAPITAL, "JPMEL UK KM1 reports no separate AT1 amount; the disclosed capital total equals CET1/Tier 1 in each populated year.\n" + GAP_NOTE)
metric("Tier 1 Ratio", "%", "Tier 1 ratio", CAPITAL_RATIO, GAP_NOTE)
metric("Total Capital", "£m", "Total capital", CAPITAL, GAP_NOTE)
metric("Total Capital Ratio", "%", "Total capital ratio", CAPITAL_RATIO, GAP_NOTE)
metric("Total RWAs", "£m", "Total risk exposure amount / total RWAs", RWA, GAP_NOTE)
metric("Leverage Ratio", "%", "Leverage ratio", LEVERAGE, GAP_NOTE)
metric("LCR", "%", "Liquidity Coverage Ratio", LCR, GAP_NOTE)
metric("NSFR", "%", "Net Stable Funding Ratio", NSFR, GAP_NOTE)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    P3_SOURCES,
    per_note={
        "MREL Ratio": (
            "No standalone JPMEL MREL ratio was found in the annual solo "
            "tables reviewed; group or another JPMorgan entity's MREL is not "
            "substituted."
        )
    },
)

bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit="",
    ratios=[
        ("CET1 Ratio", CAPITAL_RATIO),
        ("Tier 1 Ratio", CAPITAL_RATIO),
        ("Total Capital Ratio", CAPITAL_RATIO),
        ("Leverage Ratio", LEVERAGE),
        ("LCR", LCR),
        ("NSFR", NSFR),
    ],
    note=(
        "Pillar 3-only workbook on JPMEL standalone basis. Annual solo "
        "quantitative coverage is FY2023-FY2025; FY2021-FY2022 are explicitly "
        "not separately disclosed. Cash flow is not presented under FRS 101."
    ),
)

bw.save("/Users/armaan/code/katalysis/banks/JP MORGAN EUROPE FINANCIALS.xlsx")
print("Saved.")
