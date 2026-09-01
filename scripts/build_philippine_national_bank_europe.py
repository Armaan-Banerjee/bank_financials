import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024"]
YEAR_LABEL = {y: y for y in YEARS}

P3_2025_URL = "https://www.pnb.com.ph/storage/asset-libraries/Me1hxgtaSlrRs32Dvl6SIB1qgOfY1WbTDfGv2ZzQ.pdf"
P3_2024_URL = "https://pnb-website.s3-ap-southeast-1.amazonaws.com/uploads/docs/Pillar3_Disclosures.pdf"
CH_PROFILE_URL = "https://find-and-update.company-information.service.gov.uk/company/02939223"
CH_ACCOUNTS_URL = CH_PROFILE_URL + "/filing-history?category=accounts"

ENTITY_NOTE = (
    "ENTITY/BASIS: Philippine National Bank (Europe) Plc (Companies House 02939223; FRN 204532; "
    "LEI 8945002FWV05NGBXJJ26) is the UK-registered bank, wholly owned by Philippine National Bank "
    "(Manila). The official FY2024 and FY2025 Pillar 3 documents state that PNBE has no subsidiaries "
    "and disclose on an un-consolidated basis. Parent PNB Manila figures and parent-group disclosures "
    "are expressly excluded. Companies House confirms the entity and annual 31 December accounts history."
)

P3_SOURCES = (
    "Sources - PNBE's own standalone Pillar 3 disclosures (GBP '000 unless stated):\n"
    f"FY2025: Pillar 3 Disclosures for 31 December 2025, pp.3, 5-8 - {P3_2025_URL}\n"
    f"FY2024: Pillar 3 Disclosures for 31 December 2024, pp.3, 5-8 - {P3_2024_URL}\n"
    f"Entity identity and accounts filing history: Companies House - {CH_PROFILE_URL}; {CH_ACCOUNTS_URL}\n"
    + ENTITY_NOTE
)

EXEMPTION_NOTE = (
    "PILLAR-3-ONLY: the prior project screening identified PNBE's qualifying-entity cash-flow disclosure "
    "exemption in its UK accounts, so no audited cash-flow statement is populated here. The current build "
    "does not infer cash flows from parent PNB disclosures. The two official standalone Pillar 3 documents "
    "located provide quantitative capital/RWA data for FY2024-FY2025 only; no defensible standalone PNBE "
    "Pillar 3 quantitative documents were located for FY2021-FY2023, so those years are intentionally outside "
    "this workbook's scope."
)

bw = BankWorkbook(bank_name="Philippine National Bank (Europe) Plc", years=YEARS,
                  year_label=YEAR_LABEL, header_color="007A33")

bw.add_cash_flow_sheet(
    title="Philippine National Bank (Europe) Plc — Cash Flow Statement",
    subtitle="Not applicable — Pillar-3-only scope; see the exemption and coverage note below.",
    rows=[
        ("SECTION", "No standalone Statement of Cash Flows populated", {}),
        ("DATA", "PNBE cash-flow disclosure exemption; parent-group cash flows are not substituted.", {}),
    ],
    sources_text=ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE + "\n\n" + P3_SOURCES,
    first_col_width=78, source_height=260, unit_suffix="",
)


def metric(name, unit, rows, note=None):
    bw.add_metric_sheet(name, unit, rows, P3_SOURCES, note=note,
                        first_col_width=48, source_height=220)


OWN_FUNDS = {"FY2025": 10344, "FY2024": 10467}
CAPITAL_RATIO = {"FY2025": "127.55%", "FY2024": "136.95%"}
TOTAL_RWA = {"FY2025": 8110, "FY2024": 7643}

metric("CET1 Capital", "GBP '000", [("Common Equity Tier 1 (CET1) capital", OWN_FUNDS)])
metric("CET1 Ratio", "%", [("CET1 capital ratio", CAPITAL_RATIO)],
       note="CET1 = Tier 1 = total capital in both reported years; PNBE states it holds no Tier 2 capital.")
metric("Tier 1 Capital", "GBP '000", [("Tier 1 capital", OWN_FUNDS)])
metric("Tier 1 Ratio", "%", [("Tier 1 capital ratio", CAPITAL_RATIO)])
metric("Total Capital", "GBP '000", [("Own funds / total capital", OWN_FUNDS)])
metric("Total Capital Ratio", "%", [("Total capital ratio", CAPITAL_RATIO)])
metric("Total RWAs", "GBP '000", [("Total risk-weighted assets", TOTAL_RWA)],
       note="Total is the sum of credit/counterparty, market and operational RWA components in each source table.")

UNDISCLOSED = ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"]
bw.add_not_disclosed_metric_sheets(
    UNDISCLOSED, P3_SOURCES,
    per_note={name: "No quantitative standalone PNBE disclosure was located in the FY2024 or FY2025 "
                    "Pillar 3 documents; left blank rather than estimated." for name in UNDISCLOSED},
)

bw.add_overview_sheet(
    cash_flow_totals=[], cash_flow_unit=None,
    ratios=[("CET1 Ratio", CAPITAL_RATIO), ("Tier 1 Ratio", CAPITAL_RATIO),
            ("Total Capital Ratio", CAPITAL_RATIO)],
    note=("PILLAR-3-ONLY, two-year scope (FY2024-FY2025). FY2021-FY2023 are excluded because no defensible "
          "standalone PNBE Pillar 3 quantitative disclosures were located. No parent-group data is used."),
)

bw.save("/Users/armaan/code/katalysis/banks/PHILIPPINE NATIONAL BANK EUROPE FINANCIALS.xlsx")
