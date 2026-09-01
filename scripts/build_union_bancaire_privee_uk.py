import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {year: year for year in YEARS}

CH_URL = "https://find-and-update.company-information.service.gov.uk/company/00964058/filing-history"
P3_ARCHIVE_URL = "https://www.ubp.com/en/legal-aspects/union-bancaire-privee-uk-limited/pillar-3-disclosure"
P3_2024_URL = "https://www.ubp.com/files/live/sites/ubp/files/documents/legal/ubp-uk/SGKH_2024-P3-disclosures.pdf"
P3_2023_URL = "https://www.ubp.com/files/live/sites/ubp/files/documents/legal/ubp-uk/UBP_2023_P3_disclosures.pdf"
P3_2022_URL = "https://www.ubp.com/files/live/sites/ubp/files/documents/legal/ubp-uk/UBP_2022_P3_disclosures.pdf"

ENTITY_NOTE = (
    "ENTITY/BASIS NOTE: Union Bancaire Privée (UK) Limited (Companies House "
    "00964058; FRN 119250) was formerly SG Kleinwort Hambros Bank Limited. "
    "The 2022-2024 Pillar 3 reports retain the SGKH name because they cover "
    "pre-acquisition periods. All figures use the reports' UK Consolidation "
    "Group basis, incorporating SGKH Bank Ltd, its branches, and the trust "
    "entity; they are not bank-solo figures. The reports state that the "
    "published financial statements use FRS 101 and differ from the prudential "
    "scope of consolidation."
)

P3_SOURCES = (
    "Sources - UK Consolidation Group Pillar 3 disclosures, amounts converted "
    "from £'000 to £m; ratios retained as reported:\n"
    f"FY2024: SGKH Pillar 3 Disclosure 31 December 2024, UK KM1 p.10 (FY2024 "
    f"current and FY2023 comparative) - {P3_2024_URL}\n"
    f"FY2023: SGKH Pillar 3 Disclosure 31 December 2023, UK KM1 p.10 (FY2023 "
    f"current and FY2022 comparative) - {P3_2023_URL}\n"
    f"FY2022: SGKH Pillar 3 Disclosure 31 December 2022, UK KM1 p.10 (FY2022 "
    f"current and FY2021 comparative) - {P3_2022_URL}\n"
    f"Official UBP UK disclosure archive - {P3_ARCHIVE_URL}\n"
    "FY2025: no defensible UK Consolidation Group Pillar 3 disclosure found; "
    "left blank rather than substituted. Amounts are shown in £m for "
    "consistency with this project.\n"
    + ENTITY_NOTE
)

CASH_FLOW_SOURCES = (
    "CASH-FLOW EXEMPTION: the SGKH disclosures explain that the published "
    "financial statements use FRS 101 Reduced Disclosure Framework and do not "
    "consolidate the relevant subsidiaries, while prudential reporting uses "
    "the UK Consolidation Group scope. No standalone cash-flow statement is "
    "used in this Pillar-3-only workbook; no group or other-entity cash flows "
    f"are substituted. Companies House filing history: {CH_URL}\n"
    f"SGKH 2024 Pillar 3 disclosure, scope/basis discussion - {P3_2024_URL}\n"
    + ENTITY_NOTE
)

bw = BankWorkbook(
    bank_name="Union Bancaire Privée (UK) Limited",
    years=YEARS,
    year_label=YEAR_LABEL,
    header_color="355C7D",
)

bw.add_cash_flow_sheet(
    title="Union Bancaire Privée (UK) Limited — Statement of Cash Flows",
    subtitle="Not applicable: Pillar-3-only build; FRS 101 accounting/reporting basis does not provide a defensible cash-flow series.",
    rows=[
        ("SECTION", "FRS 101 / Pillar-3-only treatment", {}),
        ("DATA", "Standalone cash-flow statement", {year: "Not presented" for year in YEARS}),
    ],
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=82,
    source_height=250,
    unit_suffix="",
)


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(
        name,
        unit,
        rows_data,
        P3_SOURCES,
        note=note,
        first_col_width=65,
        source_height=240,
    )


CAPITAL = {"FY2024": 291.256, "FY2023": 356.795, "FY2022": 426.529, "FY2021": 461.392}
RWA = {"FY2024": 1373.096, "FY2023": 1450.014, "FY2022": 1830.761, "FY2021": 1951.543}
CAPITAL_RATIO = {"FY2024": "21.2%", "FY2023": "24.6%", "FY2022": "23.3%", "FY2021": "23.6%"}
LEVERAGE_EXPOSURE = {"FY2024": 4407.957, "FY2023": 4161.978, "FY2022": 4707.494, "FY2021": 5203.049}
LEVERAGE = {"FY2024": "6.6%", "FY2023": "8.6%", "FY2022": "9.1%", "FY2021": "8.9%"}
HQLA = {"FY2024": 2565.121, "FY2023": 2191.986, "FY2022": 2372.431, "FY2021": 2319.358}
LCR_OUTFLOWS = {"FY2024": 1167.142, "FY2023": 971.156, "FY2022": 1029.869, "FY2021": 1079.986}
LCR_INflows = {"FY2024": 135.972, "FY2023": 103.495, "FY2022": 208.111, "FY2021": 301.570}
LCR_NET = {"FY2024": 1031.169, "FY2023": 867.661, "FY2022": 821.759, "FY2021": 778.416}
LCR = {"FY2024": "248.8%", "FY2023": "252.6%", "FY2022": "288.7%", "FY2021": "298.0%"}
ASF = {"FY2024": 3202.089, "FY2023": 3140.112, "FY2022": 3765.621, "FY2021": 3792.308}
RSF = {"FY2024": 1265.791, "FY2023": 1441.162, "FY2022": 1698.754, "FY2021": 2108.413}
NSFR = {"FY2024": "253.0%", "FY2023": "217.9%", "FY2022": "221.7%", "FY2021": "179.9%"}

GAP_NOTE = (
    "FY2025 is blank because the official UBP UK archive currently provides "
    "SGKH UK Consolidation Group disclosures through 31 December 2024 only. "
    "FY2021-FY2024 are populated from the 2022-2024 reports. Amounts are "
    "converted from £'000 to £m; ratios remain as reported."
)

metric("CET1 Capital", "£m", [("Common Equity Tier 1 (CET1) capital", CAPITAL)], GAP_NOTE)
metric("CET1 Ratio", "%", [("Common Equity Tier 1 ratio", CAPITAL_RATIO)], GAP_NOTE)
metric("Tier 1 Capital", "£m", [("Tier 1 capital", CAPITAL)], "Tier 1 capital equals CET1 capital in every populated year; the UK KM1 tables report the same amount.\n" + GAP_NOTE)
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", CAPITAL_RATIO)], GAP_NOTE)
metric("Total Capital", "£m", [("Total capital", CAPITAL)], "Total capital equals CET1 and Tier 1 capital in every populated year in the UK KM1 tables.\n" + GAP_NOTE)
metric("Total Capital Ratio", "%", [("Total capital ratio", CAPITAL_RATIO)], GAP_NOTE)
metric("Total RWAs", "£m", [("Total risk-weighted exposure amounts", RWA)], GAP_NOTE)
metric(
    "Leverage Ratio",
    "£m / %",
    [
        ("Total exposure measure excluding claims on central banks", LEVERAGE_EXPOSURE),
        ("Leverage ratio excluding claims on central banks", LEVERAGE),
    ],
    "SGKH states that it is outside the binding LREQ framework but continues to monitor leverage. The reported ratio uses the excluding-central-bank-claims basis.\n" + GAP_NOTE,
)
metric(
    "LCR",
    "£m / %",
    [
        ("Total HQLA, weighted value average", HQLA),
        ("Cash outflows, total weighted value", LCR_OUTFLOWS),
        ("Cash inflows, total weighted value", LCR_INflows),
        ("Total net cash outflows, adjusted value", LCR_NET),
        ("Liquidity Coverage Ratio", LCR),
    ],
    "LCR is presented on the reports' weighted-average basis. FY2021 component values are taken from the FY2022 report's comparative column.\n" + GAP_NOTE,
)
metric(
    "NSFR",
    "£m / %",
    [
        ("Total available stable funding", ASF),
        ("Total required stable funding", RSF),
        ("NSFR ratio", NSFR),
    ],
    "NSFR is presented on the reports' four-quarter average basis. FY2021 component values are taken from the FY2022 report's comparative column.\n" + GAP_NOTE,
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    P3_SOURCES,
    per_note={
        "MREL Ratio": "No numeric MREL ratio was found in the 2022-2024 UK Consolidation Group disclosures reviewed. FY2025 is also outside the located disclosure coverage.",
    },
)

bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("CET1 Ratio", CAPITAL_RATIO),
        ("Tier 1 Ratio", CAPITAL_RATIO),
        ("Total Capital Ratio", CAPITAL_RATIO),
        ("Leverage Ratio", LEVERAGE),
        ("LCR", LCR),
        ("NSFR", NSFR),
    ],
    note=(
        "Pillar-3-only workbook on the UK Consolidation Group basis. FY2021-FY2024 "
        "are populated from official SGKH disclosures; FY2025 is blank because "
        "no current UK Consolidation Group disclosure was located. Cash flow is "
        "not substituted because the published accounts use the FRS 101 reduced "
        "disclosure framework."
    ),
)

bw.save("/Users/armaan/code/katalysis/banks/UNION BANCAIRE PRIVEE UK FINANCIALS.xlsx")
print("Saved.")
