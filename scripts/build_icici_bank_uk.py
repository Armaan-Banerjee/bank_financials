import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

P3_URLS = {
    "FY2025": "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/basel-pillar-3-disclosures-FY2024-25.pdf",
    "FY2024": "https://www.icicibank.co.uk/content/dam/icicibank/india/managed-assets/docs/pdf/basel-pillar-3-disclosures-FY2023-24.pdf",
    "FY2023": "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/icici-bank-uk-plc-pillar-3-disclosures-FY2022-23.pdf",
    "FY2022": "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/ICICI-Bank-UK-Plc-Pillar3-disclosures-FY2021-22.pdf",
}

AR2025_URL = "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/financial-report-uk-FY2025.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: ICICI Bank UK Plc (Companies House 04663024, FRN 223268, LEI "
    "2138002XB6T14IGKGU43) is the UK-incorporated PRA-authorised bank entity. "
    "Companies House confirms it is an active public limited company, incorporated "
    "11 February 2003, with accounts filed through 31 March 2025. The official Basel "
    "disclosures identify the reporting entity as ICICI Bank UK PLC and present the "
    "UK KM1 data on a standalone Bank basis in USD millions. No parent-group figures "
    "have been substituted."
)

EXEMPTION_NOTE = (
    "FRS 101 CASH-FLOW EXEMPTION: ICICI Bank UK Plc applies the FRS 101 reduced-"
    "disclosure framework and does not prepare a separate Statement of Cash Flows. "
    "This is therefore a Pillar-3-only workbook; the Cash Flow Statement sheet is "
    "retained to document the exemption rather than substituting parent-group cash flows. "
    f"Official supporting source: ICICI Bank UK PLC Strategic report, Directors' report "
    f"and financial statements for the year ended 31 March 2025, cash-flow exemptions "
    f"section (c) - {AR2025_URL}"
)


def p3_sources():
    lines = [
        "Sources - ICICI Bank UK Plc Basel III Pillar 3 disclosures, UK KM1 Key Metrics template (standalone Bank basis, USD million):"
    ]
    for year in YEARS:
        if year in P3_URLS:
            lines.append(f"{year}: official ICICI Bank UK Pillar 3 disclosure, pp.7–8 - {P3_URLS[year]}")
        else:
            lines.append(
                f"{year}: 31 March 2021 comparative in the official ICICI Bank UK Pillar 3 disclosure, pp.7–8 - {P3_URLS['FY2022']}"
            )
    lines.append(ENTITY_NOTE)
    return "\n".join(lines)


bw = BankWorkbook(bank_name="ICICI Bank UK Plc", years=YEARS, header_color="2A5D67")

bw.add_cash_flow_sheet(
    title="ICICI Bank UK Plc — Cash Flow Statement",
    subtitle="Not applicable — FRS 101 cash-flow-statement exemption applies for the periods covered.",
    rows=[("SECTION", "Not applicable", {}), ("DATA", EXEMPTION_NOTE, {})],
    sources_text=EXEMPTION_NOTE + "\n\n" + ENTITY_NOTE,
    first_col_width=105,
    source_height=180,
    unit_suffix="",
)


def metric(name, unit, rows, note=None):
    bw.add_metric_sheet(
        name, unit, rows, p3_sources(), note=note, first_col_width=58, source_height=155
    )


metric("CET1 Capital", "USD million", [("Common Equity Tier 1 (CET1) capital", {"FY2025": 322.9, "FY2024": 311.3, "FY2023": 295.4, "FY2022": 293.0, "FY2021": 493.9})])
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "19.57%", "FY2024": "20.14%", "FY2023": "21.54%", "FY2022": "17.79%", "FY2021": "23.80%"})])
metric("Tier 1 Capital", "USD million", [("Tier 1 capital", {"FY2025": 322.9, "FY2024": 311.3, "FY2023": 295.4, "FY2022": 293.0, "FY2021": 493.9})])
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {"FY2025": "19.57%", "FY2024": "20.14%", "FY2023": "21.54%", "FY2022": "17.79%", "FY2021": "23.80%"})])
metric("Total Capital", "USD million", [("Total capital", {"FY2025": 372.9, "FY2024": 361.3, "FY2023": 371.9, "FY2022": 378.0, "FY2021": 586.7})])
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2025": "22.60%", "FY2024": "23.37%", "FY2023": "27.12%", "FY2022": "22.96%", "FY2021": "28.27%"})])
metric("Total RWAs", "USD million", [("Total risk-weighted exposure amount", {"FY2025": 1649.7, "FY2024": 1546.2, "FY2023": 1371.5, "FY2022": 1646.7, "FY2021": 2075.1})])
metric(
    "Leverage Ratio",
    "USD million / %",
    [
        ("Total exposure measure excluding claims on central banks", {"FY2025": 2276.7, "FY2024": 2086.8, "FY2023": 1914.3, "FY2022": 2085.6}),
        ("Leverage ratio excluding claims on central banks", {"FY2025": "14.18%", "FY2024": "14.92%", "FY2023": "15.43%", "FY2022": "14.05%"}),
    ],
    note="The FY2021 comparative was not disclosed in the FY2022 UK KM1 leverage rows and is left blank rather than substituted.",
)
metric("LCR", "%", [("Liquidity coverage ratio", {"FY2025": "190.08%", "FY2024": "240.20%", "FY2023": "226.83%", "FY2022": "226.90%"})], note="The FY2021 comparative was not disclosed in the FY2022 UK KM1 LCR rows and is left blank rather than substituted.")
metric("NSFR", "%", [("Net stable funding ratio", {"FY2025": "151.03%", "FY2024": "159.20%", "FY2023": "147.72%", "FY2022": "141.69%"})], note="The FY2021 comparative was not disclosed in the FY2022 UK KM1 NSFR rows and is left blank rather than substituted.")
bw.add_not_disclosed_metric_sheets(["MREL Ratio"], p3_sources(), per_note={"MREL Ratio": "No MREL ratio appears in the official ICICI Bank UK Basel disclosures reviewed for FY2021–FY2025; no figure has been inferred."})

bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("CET1 Ratio", {"FY2025": "19.57%", "FY2024": "20.14%", "FY2023": "21.54%", "FY2022": "17.79%", "FY2021": "23.80%"}),
        ("Tier 1 Ratio", {"FY2025": "19.57%", "FY2024": "20.14%", "FY2023": "21.54%", "FY2022": "17.79%", "FY2021": "23.80%"}),
        ("Total Capital Ratio", {"FY2025": "22.60%", "FY2024": "23.37%", "FY2023": "27.12%", "FY2022": "22.96%", "FY2021": "28.27%"}),
        ("Leverage Ratio", {"FY2025": "14.18%", "FY2024": "14.92%", "FY2023": "15.43%", "FY2022": "14.05%"}),
        ("LCR", {"FY2025": "190.08%", "FY2024": "240.20%", "FY2023": "226.83%", "FY2022": "226.90%"}),
        ("NSFR", {"FY2025": "151.03%", "FY2024": "159.20%", "FY2023": "147.72%", "FY2022": "141.69%"}),
    ],
    note="Pillar-3-only workbook. ICICI Bank UK Plc's FRS 101 cash-flow exemption means no cash-flow summary or chart is shown. Regulatory figures are standalone Bank-basis USD millions or reported percentages; FY2026 is available from the official archive but excluded to retain the project's FY2021–FY2025 window.",
)

bw.save("/Users/armaan/code/katalysis/banks/ICICI BANK UK FINANCIALS.xlsx")
