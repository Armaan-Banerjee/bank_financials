import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


# PILLAR-3-ONLY WORKBOOK: Citibank UK Limited (CUKL), company 11283101,
# FRN 124579.  The company applies the FRS 101 IAS 7 exemption, so no
# statutory cash-flow statement is available.  The defensible quantitative
# scope is FY2021-FY2023: the official 2021 and 2023 standalone Pillar 3
# reports are available, and the 2023 report includes FY2022 comparatives.
YEARS = ["FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

P3_2021_URL = "https://www.citigroup.com/rcs/citigpa/akpublic/storage/public/b3p3d211231_uk.pdf"
P3_2023_URL = "https://www.citigroup.com/rcs/citigpa/storage/public/b3p3d231231_uk.pdf"
FS_2024_URL = "https://www.citigroup.com/rcs/citigpa/storage/public/citibank-uk-limited-annual-fs-2024.pdf"
CH_URL = "https://find-and-update.company-information.service.gov.uk/company/11283101/filing-history"
REG_URL = "https://www.citigroup.com/global/investors/other-regulatory-filings"

ENTITY_NOTE = (
    "ENTITY NOTE: Citibank UK Limited (CUKL), Companies House company 11283101 and FRN 124579, is the UK legal "
    "entity covered here. CUKL's official Pillar 3 disclosures state that it has no subsidiaries and that the "
    "disclosures are prepared on a stand-alone basis. This is not Citibank N.A. London Branch or Citibank Europe plc."
)

P3_SOURCES = (
    "Sources - official Citibank UK Limited standalone Pillar 3 disclosures, UK KM1 and related tables:\n"
    f"FY2023: CUKL Pillar 3 Disclosures December 2023, pp. 3-5 and 8 - {P3_2023_URL}\n"
    f"FY2022: FY2022 comparative column in the CUKL Pillar 3 Disclosures December 2023, p. 5 - {P3_2023_URL}\n"
    f"FY2021: CUKL Pillar 3 Disclosures December 2021, pp. 6 and 15 - {P3_2021_URL}\n"
    f"Regulatory filing index: {REG_URL}\n"
    + ENTITY_NOTE
)

EXEMPTION_NOTE = (
    "FRS 101 CASH-FLOW EXEMPTION: CUKL's 2024 audited financial statements state that the Company has taken the "
    "FRS 101 exemption from the requirements of IAS 7 Statement of cash flows (note 1, p. 25). The same reduced-"
    "disclosure basis is consistent with the standalone Pillar 3 reports. The 2024 accounts also state that capital "
    f"management is explained in CUKL's Basel Pillar 3 disclosures. Source: {FS_2024_URL}. Companies House filing "
    f"history for company 11283101 confirms the 2024 accounts were filed on 30 May 2025: {CH_URL}."
)

bw = BankWorkbook(
    bank_name="Citibank UK Limited",
    years=YEARS,
    year_label=YEAR_LABEL,
    header_color="1F3B57",
)

bw.add_cash_flow_sheet(
    title="Citibank UK Limited — Cash Flow Statement",
    subtitle="Not applicable — CUKL applies the FRS 101 IAS 7 cash-flow disclosure exemption.",
    rows=[
        ("SECTION", "No Statement of Cash Flows is published for the covered entity", {}),
        ("DATA", "Pillar-3-only scope used because the statutory cash-flow statement is exempted and unavailable.", {}),
    ],
    sources_text=ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE,
    first_col_width=90,
    source_height=230,
    unit_suffix="",
)


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, P3_SOURCES, note=note, first_col_width=56, source_height=145)


metric("CET1 Capital", "£m", [
    ("Common Equity Tier 1 (CET1) capital", {"FY2023": 418.0, "FY2022": 417.0, "FY2021": 304.2}),
])
metric("CET1 Ratio", "% of RWA", [
    ("Common Equity Tier 1 (CET1) ratio", {"FY2023": "72.7%", "FY2022": "59.1%", "FY2021": "37.8%"}),
])
metric("Tier 1 Capital", "£m", [
    ("Tier 1 capital", {"FY2023": 470.0, "FY2022": 469.0, "FY2021": 356.2}),
])
metric("Tier 1 Ratio", "% of RWA", [
    ("Tier 1 ratio", {"FY2023": "81.8%", "FY2022": "66.4%", "FY2021": "44.2%"}),
])
metric("Total Capital", "£m", [
    ("Total capital", {"FY2023": 522.0, "FY2022": 521.0, "FY2021": 408.2}),
])
metric("Total Capital Ratio", "% of RWA", [
    ("Total capital ratio", {"FY2023": "90.8%", "FY2022": "73.8%", "FY2021": "50.7%"}),
])
metric("Total RWAs", "£m", [
    ("Total risk-weighted exposure amount", {"FY2023": 574.7, "FY2022": 706.1, "FY2021": 805.3}),
])
metric("Leverage Ratio", "£m / %", [
    ("Total exposure measure", {"FY2023": 2812.0, "FY2022": 4733.0, "FY2021": 6818.1}),
    ("Leverage ratio", {"FY2023": "16.7%", "FY2022": "9.9%", "FY2021": "5.2%"}),
], note="FY2021 is reported on the pre-2022 Basel III basis; FY2022-FY2023 use the UK KM1 leverage measure excluding claims on central banks.")
metric("LCR", "£m / %", [
    ("Total HQLA (weighted value / average)", {"FY2023": 2988.6, "FY2022": 4476.6, "FY2021": 4219.7}),
    ("Total net cash outflows (adjusted value)", {"FY2023": 357.5, "FY2022": 687.1, "FY2021": 639.8}),
    ("Liquidity coverage ratio", {"FY2023": "836.0%", "FY2022": "654.5%", "FY2021": "659%"}),
], note="FY2021 is based on daily averages; FY2022-FY2023 use the revised UK KM1 weighted-average presentation.")
metric("NSFR", "£m / %", [
    ("Total available stable funding", {"FY2023": 4091.4, "FY2022": 6249.1}),
    ("Total required stable funding", {"FY2023": 1018.8, "FY2022": 1839.5}),
    ("NSFR ratio", {"FY2023": "401.6%", "FY2022": "342.2%"}),
], note="NSFR was implemented in the UK reporting framework from 2022; no FY2021 NSFR figure is populated.")
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    P3_SOURCES,
    per_note={"MREL Ratio": "The 2021 report states that no MREL eligible debt had been issued. The 2023 report states that the BoE set CUKL's MREL requirement equal to its minimum capital requirement and that no MREL eligible debt had been issued as at 31 December 2023; no numeric MREL ratio is disclosed."},
)

bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("CET1 Ratio", {"FY2023": "72.7%", "FY2022": "59.1%", "FY2021": "37.8%"}),
        ("Tier 1 Ratio", {"FY2023": "81.8%", "FY2022": "66.4%", "FY2021": "44.2%"}),
        ("Total Capital Ratio", {"FY2023": "90.8%", "FY2022": "73.8%", "FY2021": "50.7%"}),
        ("Leverage Ratio", {"FY2023": "16.7%", "FY2022": "9.9%", "FY2021": "5.2%"}),
        ("LCR", {"FY2023": "836.0%", "FY2022": "654.5%", "FY2021": "659%"}),
        ("NSFR", {"FY2023": "401.6%", "FY2022": "342.2%"}),
    ],
    note="PILLAR-3-ONLY scope. FY2024 and FY2025 are intentionally omitted: no official standalone CUKL Pillar 3 report was located for FY2024, and Companies House shows FY2025 accounts are not yet filed as at 29 August 2026. See source notes for the FRS 101 IAS 7 exemption and the 2021-2023 source coverage.",
)

bw.save("/Users/armaan/code/katalysis/banks/CITIBANK UK FINANCIALS.xlsx")
