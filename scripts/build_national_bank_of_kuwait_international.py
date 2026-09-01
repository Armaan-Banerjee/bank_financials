import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


# Entity confirmed against Banks List 2608.xlsx and Companies House:
# National Bank of Kuwait (International) Plc, company 02773743, FRN 171532.
# The entity is a wholly-owned UK subsidiary of National Bank of Kuwait S.A.K.P.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

AR_URLS = {
    "FY2025": "https://www.nbk.com/dam/jcr:6d7dc8ff-20d6-4ba1-be40-03386a48becd/nbki-financial-statements-2025.pdf",
    "FY2024": "https://www.nbk.com/dam/jcr:04623e62-4149-4a86-99a6-989cd9285e7e/NBKI-Financial-Statement-2024.pdf",
    "FY2023": "https://www.nbk.com/dam/jcr:a2323d07-848e-4518-971d-8e24a3395ad0/NBKI-Financial-Statement-2023.pdf",
    "FY2022": "https://www.nbk.com/dam/jcr:d333e5bb-2545-40a2-90a6-59a827646b7b/NBKI-Financial-Statement-2022.pdf",
    "FY2021": "https://www.nbk.com/dam/jcr:c3c72c41-97cb-454c-b14e-2a77baf033ab/NBKI-Financial-Statement-2021.pdf",
}
PILLAR_URL = "https://www.nbk.com/dam/jcr:19757e7d-4d03-40f8-bf39-63c995186e39/Pillar_III_Disclosures.pdf"

ENTITY_NOTE = (
    "National Bank of Kuwait (International) Plc (company 02773743, FRN 171532, LEI "
    "213800OTQ2BHFRVL6A46) is the entity in Banks List 2608.xlsx. Companies House confirms "
    "the active public company, incorporated 9 December 1992, with accounts made up to 31 December. "
    "The Bank is a wholly-owned subsidiary of National Bank of Kuwait S.A.K.P. and is regulated by the PRA and FCA."
)

CF_NOTE = (
    "No Statement of Cash Flows is published for FY2021–FY2025. The audited reports are prepared under FRS 101 "
    "Reduced Disclosure Framework and the independent auditor's report identifies the financial statements as the "
    "statement of income, statement of comprehensive income, statement of financial position, statement of changes "
    "in equity, and related notes; a cash-flow statement is not included. This is therefore a Pillar-3-only workbook."
)


def annual_sources(extra=""):
    text = ENTITY_NOTE + "\n\nOfficial annual reports and financial statements:\n"
    capital_pages = {
        "FY2025": "capital management p.75",
        "FY2024": "capital management p.76",
        "FY2023": "capital management p.72",
        "FY2022": "capital management p.64",
        "FY2021": "capital management p.72",
    }
    text += "\n".join(f"{y}: {capital_pages[y]}, {AR_URLS[y]}" for y in YEARS)
    if extra:
        text += "\n\n" + extra
    return text


def p3_sources(extra=""):
    return annual_sources(
        "Official NBKI Pillar 3 Disclosure 31 December 2025 (Table 3, Key Metrics, p.16; "
        f"includes 31 December 2024 comparative values): {PILLAR_URL}" + ("\n\n" + extra if extra else "")
    )


bw = BankWorkbook(
    bank_name="National Bank of Kuwait (International) Plc",
    years=YEARS,
    header_color="1F4E79",
)

# The entity takes the FRS 101 cash-flow disclosure exemption.
bw.add_cash_flow_sheet(
    title="National Bank of Kuwait (International) Plc — Cash Flow Statement",
    subtitle="Not applicable — FRS 101 cash-flow-statement disclosure exemption",
    rows=[
        ("SECTION", "No Statement of Cash Flows is published by this entity in any year", {}),
        ("DATA", CF_NOTE, {}),
    ],
    sources_text=annual_sources(CF_NOTE),
    first_col_width=100,
    source_height=280,
    unit_suffix="",
)


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(
        name,
        unit,
        rows_data,
        p3_sources(),
        note=note,
        first_col_width=58,
        source_height=220,
    )


# FY2021–FY2023 capital figures are reported in US$000 in the statutory
# accounts; FY2024–FY2025 are reported in GBP£000 after the presentation-
# currency change. Values are kept as reported and the unit note is explicit.
CAPITAL = {"FY2025": 536637, "FY2024": 501570, "FY2023": 533272, "FY2022": 453162, "FY2021": 432220}
RWAS = {"FY2025": 2624404, "FY2024": 2503806, "FY2023": 2599821, "FY2022": 2131640, "FY2021": 2034858}
CAPITAL_RATIOS = {"FY2025": "20.45%", "FY2024": "20.03%", "FY2023": "20.51%", "FY2022": "21.26%", "FY2021": "21.24%"}

CAPITAL_UNIT = "As reported: £000 (FY2024–FY2025); US$000 (FY2021–FY2023)"
CAPITAL_NOTE = (
    "CET1, Tier 1, and Total Capital are equal in every year because the Bank reports no Tier 2 capital and its "
    "regulatory capital is comprised entirely of CET1. FY2021–FY2023 are reported in US$000; FY2024–FY2025 are "
    "reported in GBP£000 following the presentation-currency change. No conversion has been imposed."
)

metric("CET1 Capital", CAPITAL_UNIT, [("Common Equity Tier 1 (CET1) capital", CAPITAL)], CAPITAL_NOTE)
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 capital adequacy ratio", CAPITAL_RATIOS)])
metric("Tier 1 Capital", CAPITAL_UNIT, [("Tier 1 capital", CAPITAL)], CAPITAL_NOTE)
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 capital adequacy ratio", CAPITAL_RATIOS)])
metric("Total Capital", CAPITAL_UNIT, [("Total capital", CAPITAL)], CAPITAL_NOTE)
metric("Total Capital Ratio", "% of RWA", [("Total capital adequacy ratio", CAPITAL_RATIOS)])
metric("Total RWAs", CAPITAL_UNIT, [("Risk-weighted assets", RWAS)])

metric(
    "Leverage Ratio",
    "£000 / %",
    [
        ("Total exposure measure excluding claims on central banks", {"FY2025": 4062395, "FY2024": 4133905}),
        ("Leverage ratio excluding claims on central banks", {"FY2025": "13.21%", "FY2024": "12.13%"}),
    ],
    "FY2021–FY2023: not publicly disclosed in the reviewed entity-level annual reports or available Pillar 3 source. "
    "FY2024–FY2025 are from the official Pillar 3 Table 3, p.16.",
)

metric(
    "LCR",
    "£000 / %",
    [
        ("Total HQLA (weighted value average)", {"FY2025": 731707, "FY2024": 925985}),
        ("Total net cash outflows (adjusted value)", {"FY2025": 147299, "FY2024": 215454}),
        ("Liquidity Coverage Ratio (adjusted value)", {"FY2025": "497%", "FY2024": "430%"}),
    ],
    "FY2021–FY2023: not publicly disclosed in the reviewed entity-level annual reports or available Pillar 3 source. "
    "FY2024–FY2025 are from the official Pillar 3 Table 3, p.16.",
)

metric(
    "NSFR",
    "%",
    [("Net Stable Funding Ratio", {"FY2025": "120%", "FY2024": "127%"})],
    "FY2021–FY2023: not publicly disclosed in the reviewed entity-level annual reports or available Pillar 3 source. "
    "FY2024–FY2025 are from the official Pillar 3 Table 3, p.16.",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources("No MREL ratio or MREL requirement was numerically disclosed in the reviewed entity-level documents."),
    per_note={"MREL Ratio": "No MREL ratio or requirement was located in the FY2021–FY2025 annual reports or the official Pillar 3 disclosure."},
)

bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("CET1 Ratio", CAPITAL_RATIOS),
        ("Tier 1 Ratio", CAPITAL_RATIOS),
        ("Total Capital Ratio", CAPITAL_RATIOS),
        ("Leverage Ratio", {"FY2025": "13.21%", "FY2024": "12.13%"}),
        ("LCR", {"FY2025": "497%", "FY2024": "430%"}),
        ("NSFR", {"FY2025": "120%", "FY2024": "127%"}),
    ],
    note=(
        "Pillar-3-only workbook: the Bank uses the FRS 101 cash-flow-statement exemption. "
        "Capital, RWA, and capital-ratio data covers FY2021–FY2025; leverage, LCR, and NSFR are available "
        "for FY2024–FY2025 only."
    ),
)

bw.save("/Users/armaan/code/katalysis/banks/NATIONAL BANK OF KUWAIT INTERNATIONAL FINANCIALS.xlsx")
