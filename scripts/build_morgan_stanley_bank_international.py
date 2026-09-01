import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


# Morgan Stanley Bank International Limited, company 03722571, FRN 195430.
# The legal entity and FRN are confirmed against Banks List 2608.xlsx,
# Companies House, and Morgan Stanley's UK office/FCA information.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

AR_URLS = {
    "FY2025": "https://find-and-update.company-information.service.gov.uk/company/03722571/filing-history/MzUxNTMzMjAyMmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2024": "https://find-and-update.company-information.service.gov.uk/company/03722571/filing-history/MzQ2MjkyNzg4N2FkaXF6a2N4/document?format=pdf&download=0",
    "FY2023": "https://find-and-update.company-information.service.gov.uk/company/03722571/filing-history/MzQyMDQ2MzQxOGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2022": "https://find-and-update.company-information.service.gov.uk/company/03722571/filing-history/MzM3ODM5NTg1NmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2021": "https://find-and-update.company-information.service.gov.uk/company/03722571/filing-history/MzMzODIzODA1MmFkaXF6a2N4/document?format=pdf&download=0",
}

ENTITY_NOTE = (
    "ENTITY NOTE: Morgan Stanley Bank International Limited (company 03722571, FRN 195430) is the legal entity "
    "listed in Banks List 2608.xlsx. Companies House confirms the active UK private limited company, incorporated "
    "23 February 1999, with registered office at 25 Cabot Square, London E14 4QA. The figures below are standalone "
    "Company figures from the entity's own annual reports, not Morgan Stanley International group figures."
)


def annual_sources():
    return (
        ENTITY_NOTE + "\n\n"
        "Sources — Morgan Stanley Bank International Limited Annual Reports and Financial Statements, "
        "Strategic Report capital/liquidity tables and financial statements:\n"
        f"FY2025: Annual Report and Financial Statements for year ended 31 December 2025, pp.5, 8-10, 47 — {AR_URLS['FY2025']}\n"
        f"FY2024: Annual Report and Financial Statements for year ended 31 December 2024, pp.5, 8-10 — {AR_URLS['FY2024']}\n"
        f"FY2023: Annual Report and Financial Statements for year ended 31 December 2023, pp.5, 8-10 — {AR_URLS['FY2023']}\n"
        f"FY2022: Annual Report and Financial Statements for year ended 31 December 2022, pp.5, 8-10 — {AR_URLS['FY2022']}\n"
        f"FY2021: Annual Report and Financial Statements for year ended 31 December 2021, pp.6, 9-10 — {AR_URLS['FY2021']}\n"
        "The annual reports state that the Company takes the FRS 101 reduced-disclosure exemption from presenting a "
        "cash-flow statement. Blank or non-disclosed entries are not estimates or zeros."
    )


bw = BankWorkbook("Morgan Stanley Bank International Limited", YEARS, header_color="1F4E79")

# The Company explicitly takes the FRS 101 exemption from presenting a cash-flow
# statement. Retain the standard tab and document the structural limitation.
bw.add_cash_flow_sheet(
    "Morgan Stanley Bank International Limited — Statement of Cash Flows",
    "Standalone Company basis; cash-flow statement not presented under the FRS 101 reduced-disclosure exemption",
    [("DATA", "Cash-flow statement not separately disclosed under FRS 101", {})],
    annual_sources(),
    first_col_width=72,
    source_height=220,
    unit_suffix=" (£'000)",
)


def metric(name, unit, rows, note=None):
    bw.add_metric_sheet(name, unit, rows, annual_sources(), note=note, first_col_width=54, source_height=220)


metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", {
    "FY2025": 676229, "FY2024": 709078, "FY2023": 685522, "FY2022": 702944, "FY2021": 717693,
})])
metric("CET1 Ratio", "% of RWA", [("CET1 capital ratio", {
    "FY2025": "42.6%", "FY2024": "46.7%", "FY2023": "31.7%", "FY2022": "34.0%", "FY2021": "34.4%",
})])
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", {
    "FY2025": 676229, "FY2024": 709078, "FY2023": 685522, "FY2022": 702944, "FY2021": 717693,
})])
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 capital ratio", {
    "FY2025": "42.6%", "FY2024": "46.7%", "FY2023": "31.7%", "FY2022": "34.0%", "FY2021": "34.4%",
})])
metric("Total Capital", "£'000", [("Total capital resources", {
    "FY2025": 934449, "FY2024": 908739, "FY2023": 935655, "FY2022": 1003410, "FY2021": 916488,
})])
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {
    "FY2025": "58.9%", "FY2024": "59.8%", "FY2023": "43.3%", "FY2022": "48.5%", "FY2021": "44.0%",
})])
metric("Total RWAs", "£'000", [("Total risk-weighted assets", {
    "FY2025": 1586014, "FY2024": 1519269, "FY2023": 2161713, "FY2022": 2068356, "FY2021": 2081783,
})])
metric("Leverage Ratio", "£'000 / %", [
    ("Leverage exposure", {"FY2025": 2233488, "FY2024": 2436257, "FY2023": 2874295, "FY2022": 3795132, "FY2021": 2384965}),
    ("Leverage ratio", {"FY2025": "30.3%", "FY2024": "29.1%", "FY2023": "23.9%", "FY2022": "18.5%", "FY2021": "30.1%"}),
])
metric("LCR", "£'000 / %", [
    ("Liquidity buffer — HQLA", {"FY2025": 1110032, "FY2024": 1825386, "FY2023": 1190200, "FY2022": 1230539, "FY2021": 1240953}),
    ("Liquidity coverage ratio", {"FY2025": "412%", "FY2024": "417%", "FY2023": "250%", "FY2022": "191%", "FY2021": "226%"}),
], note="The reports state that the HQLA amounts are reported to the regulator in USD and converted to GBP using an average annual exchange rate; the ratios are calculated using the preceding twelve months.")
metric("NSFR", "£'000 / %", [
    ("Available stable funding", {"FY2025": 1485790, "FY2024": 1597110, "FY2023": 2191000, "FY2022": 2344000, "FY2021": "Not disclosed"}),
    ("Required stable funding", {"FY2025": 574724, "FY2024": 716541, "FY2023": 1346000, "FY2022": 1417000, "FY2021": "Not disclosed"}),
    ("Net Stable Funding Ratio", {"FY2025": "263%", "FY2024": "223%", "FY2023": "163%", "FY2022": "165%", "FY2021": "Not disclosed"}),
], note="The Company states that NSFR became a PRA requirement from 1 January 2022; no FY2021 NSFR was disclosed.")
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    annual_sources() + "\nNo standalone MREL ratio was numerically disclosed in the five annual reports reviewed; group-level resolution disclosures were not substituted.",
)

bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "42.6%", "FY2024": "46.7%", "FY2023": "31.7%", "FY2022": "34.0%", "FY2021": "34.4%"}),
        ("Total Capital Ratio", {"FY2025": "58.9%", "FY2024": "59.8%", "FY2023": "43.3%", "FY2022": "48.5%", "FY2021": "44.0%"}),
        ("Leverage Ratio", {"FY2025": "30.3%", "FY2024": "29.1%", "FY2023": "23.9%", "FY2022": "18.5%", "FY2021": "30.1%"}),
        ("LCR", {"FY2025": "412%", "FY2024": "417%", "FY2023": "250%", "FY2022": "191%", "FY2021": "226%"}),
        ("NSFR", {"FY2025": "263%", "FY2024": "223%", "FY2023": "163%", "FY2022": "165%", "FY2021": "Not disclosed"}),
    ],
    note="The Company takes the FRS 101 exemption from presenting a cash-flow statement. Interim Morgan Stanley International Pillar 3 reports are group-level and do not provide defensible standalone MSBIL interim data, so this is a standard annual 13-sheet workbook.",
)

bw.save("/Users/armaan/code/katalysis/banks/MORGAN STANLEY BANK INTERNATIONAL FINANCIALS.xlsx")
