import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

P3 = {
    "FY2025": "https://sbiuk.statebank/documents/274771/0/PILLAR+3+DISCLOSURE+FINAL310325_241225_Clean.pdf/276091ea-d916-6dca-edea-e443f2360cc9?t=1767022122544",
    "FY2024": "https://sbiuk.statebank/documents/274771/0/Pillar+3+Disclosures+March+24.pdf/91bf9318-a453-5bc7-f2ae-434bdbe0371c?t=1730125188784",
    "FY2023": "https://sbiuk.statebank/documents/274771/0/Disclosure+Statement+Basel+3+FY+22+23.pdf/f068336d-c894-0e35-49b6-a3bb372791ae?t=1699459644582",
    "FY2022": "https://sbiuk.statebank/documents/274771/0/SBI+UK+Limited+Pillar+3+Disclosures_2022_Final.pdf/f3ecb40e-bb6a-2a6b-52b6-44c00b93dc8b?t=1671208953569",
    "FY2021": "https://sbiuk.statebank/documents/274771/0/SBI+UK+Limited+Pillar+3_2021_FINAL.pdf/cea4191a-a7ee-17ef-df42-ee5d2d21f73f?t=1635936666779",
}
PAGES = {"FY2025": "6-7", "FY2024": "7-8", "FY2023": "7-8", "FY2022": "7-8", "FY2021": "4"}
FS2025 = "https://sbiuk.statebank/documents/274771/0/SBIUK%2B-%2BAnnual%2BReport%2B2025%2Bapproved.pdf/4d165f25-8596-0935-9c39-80cf4c7202b8?t=1767022144810"
FS2024 = "http://sbiuk.statebank/documents/274771/0/SBIUK+Ltd+-+Annual+Report+++2024.pdf/80699e7d-ba2e-8cc6-6726-f8bc7058261f?t=1730125796286"
FS2023 = "https://sbiuk.statebank/documents/274771/0/Annual+Financial+22+23.pdf/77b485b2-332e-c7b0-63bf-30991ce5238b?t=1699459677034"
FS2022 = "https://sbiuk.statebank/documents/274771/0/SBIUK+Annual+Financial+Statement+2022.pdf/e333fa11-f77e-d3ab-b179-010d91c38b92?t=1671208995591"
FS2021 = "https://sbiuk.statebank/documents/274771/0/SBI+UK+Annual+Report+-+Final.pdf/d188a204-db49-de8e-9662-5fece3c6f364?t=1635936642226"

ENTITY_NOTE = (
    "ENTITY NOTE: State Bank of India (UK) Limited (Companies House 10436460, FRN 757156, LEI "
    "213800LOV39TJH6YQY23) is the UK legal entity named in the Banks List 2608.xlsx and the PRA register. "
    "It is a wholly owned subsidiary of State Bank of India and has no subsidiaries. The Pillar 3 figures below "
    "are SBI UK standalone/entity figures; parent State Bank of India figures have not been substituted."
)
EXEMPTION_NOTE = (
    "FRS 102 CASH-FLOW EXEMPTION: SBI UK’s annual accounts explicitly state that it takes the FRS 102 disclosure "
    "exemption from preparation of a cash flow statement because it is a qualifying entity and its ultimate parent, "
    "State Bank of India, includes the bank’s cash flows in consolidated financial statements. This wording is in "
    f"the FY2025 accounts, accounting policies (p.29) - {FS2025}, and the corresponding FY2024, FY2023, FY2022 "
    f"and FY2021 accounts. No entity cash-flow statement is therefore presented. This is a PILLAR-3-ONLY workbook."
)


def sources():
    return (
        "Sources - State Bank of India (UK) Limited standalone UK KM1 / Key Metrics disclosures, £m and %:\n"
        + "\n".join(f"{y}: SBI UK Pillar 3 disclosure, pp. {PAGES[y]} - {P3[y]}" for y in YEARS)
        + "\n\n"
        + ENTITY_NOTE
    )


bw = BankWorkbook("State Bank of India (UK) Limited", YEARS, YEAR_LABEL, header_color="1B4D6B")
bw.add_cash_flow_sheet(
    title="State Bank of India (UK) Limited — Cash Flow Statement",
    subtitle="Not applicable — the entity takes the FRS 102 cash-flow-statement exemption. See source note below.",
    rows=[
        ("SECTION", "No Statement of Cash Flows is published by this entity", {}),
        ("DATA", "This workbook is the Pillar-3-only variant; the exemption and source evidence are documented below.", {}),
    ],
    sources_text=ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE,
    first_col_width=92,
    source_height=280,
    unit_suffix="",
)


def metric(name, unit, rows, note=None):
    bw.add_metric_sheet(name, unit, rows, sources(), note=note, first_col_width=52, source_height=150)


metric("CET1 Capital", "£m", [("Common Equity Tier 1 (CET1) capital", {"FY2025": 277.00, "FY2024": 271.82, "FY2023": 259.67, "FY2022": 249.19, "FY2021": 243.50})])
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 ratio", {"FY2025": "20.98%", "FY2024": "22.41%", "FY2023": "21.16%", "FY2022": "19.52%", "FY2021": "17.93%"})])
metric("Tier 1 Capital", "£m", [("Tier 1 capital", {"FY2025": 277.00, "FY2024": 271.82, "FY2023": 259.67, "FY2022": 249.19, "FY2021": 243.50})], "Tier 1 equals CET1 in every year shown; no AT1 capital is reported.")
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {"FY2025": "20.98%", "FY2024": "22.41%", "FY2023": "21.16%", "FY2022": "19.52%", "FY2021": "17.93%"})])
metric("Total Capital", "£m", [("Total capital", {"FY2025": 277.00, "FY2024": 271.82, "FY2023": 259.67, "FY2022": 249.19, "FY2021": 247.76})], "FY2021 total capital exceeds CET1/Tier 1 because the source reports £4.26m of Tier 2 capital; from FY2022 onward total capital equals CET1/Tier 1.")
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2025": "20.98%", "FY2024": "22.41%", "FY2023": "21.16%", "FY2022": "19.52%", "FY2021": "18.25%"})])
metric("Total RWAs", "£m", [("Total risk-weighted exposure amount", {"FY2025": 1320.25, "FY2024": 1213.02, "FY2023": 1227.04, "FY2022": 1276.68, "FY2021": 1357.75})])
metric("Leverage Ratio", "£m / %", [
    ("Total exposure measure excluding claims on central banks", {"FY2025": 1919.23, "FY2024": 1774.80, "FY2023": 1864.49, "FY2022": 1749.04}),
    ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "14.43%", "FY2024": "15.32%", "FY2023": "13.93%", "FY2022": "14.25%"}),
    ("Leverage ratio (financial-ratios presentation; basis not specified)", {"FY2021": "13.5%"}),
], "The FY2021 report presents only a headline leverage ratio in its financial-ratios section. The excluding-central-bank-claims exposure measure and ratio first appear in the FY2022 UK KM1 table; FY2021 is not relabelled or inferred.")
metric("LCR", "£m / %", [
    ("Total high-quality liquid assets (HQLA), weighted value - average", {"FY2025": 183.96, "FY2024": 184.64, "FY2023": 188.83, "FY2022": 142.01}),
    ("Cash outflows - total weighted value", {"FY2025": 80.05, "FY2024": 105.33, "FY2023": 135.01, "FY2022": 124.25}),
    ("Cash inflows - total weighted value", {"FY2025": 48.09, "FY2024": 49.57, "FY2023": 43.28, "FY2022": 37.66}),
    ("Total net cash outflows (adjusted value)", {"FY2025": 36.64, "FY2024": 55.75, "FY2023": 91.72, "FY2022": 86.59}),
    ("Liquidity coverage ratio (%)", {"FY2025": "572.38%", "FY2024": "331.15%", "FY2023": "205.87%", "FY2022": "164.00%", "FY2021": "156%"}),
], "FY2021's Pillar 3 report discloses only the headline LCR ratio in its financial-ratios presentation; no FY2021 KM1 liquidity component amounts were found, so they remain blank.")
metric("NSFR", "£m / %", [
    ("Total available stable funding", {"FY2025": 1782.87, "FY2024": 1687.00, "FY2023": 1765.00, "FY2022": 1571.94}),
    ("Total required stable funding", {"FY2025": 1311.47, "FY2024": 1200.00, "FY2023": 1231.00, "FY2022": 1209.80}),
    ("NSFR ratio (%)", {"FY2025": "135.94%", "FY2024": "140.48%", "FY2023": "143.36%", "FY2022": "129.93%", "FY2021": "124%"}),
], "FY2021's Pillar 3 report discloses only the headline NSFR ratio; no FY2021 ASF/RSF component amounts were found, so they remain blank.")
metric("MREL Ratio", "£m / %", [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})], "No numeric MREL ratio was disclosed in the five SBI UK Pillar 3 documents reviewed; it is not inferred from capital or liquidity metrics.")

bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("CET1 Ratio", {"FY2025": "20.98%", "FY2024": "22.41%", "FY2023": "21.16%", "FY2022": "19.52%", "FY2021": "17.93%"}),
        ("Tier 1 Ratio", {"FY2025": "20.98%", "FY2024": "22.41%", "FY2023": "21.16%", "FY2022": "19.52%", "FY2021": "17.93%"}),
        ("Total Capital Ratio", {"FY2025": "20.98%", "FY2024": "22.41%", "FY2023": "21.16%", "FY2022": "19.52%", "FY2021": "18.25%"}),
        ("Leverage Ratio (excl. central bank claims)", {"FY2025": "14.43%", "FY2024": "15.32%", "FY2023": "13.93%", "FY2022": "14.25%"}),
        ("LCR", {"FY2025": "572.38%", "FY2024": "331.15%", "FY2023": "205.87%", "FY2022": "164.00%", "FY2021": "156%"}),
        ("NSFR", {"FY2025": "135.94%", "FY2024": "140.48%", "FY2023": "143.36%", "FY2022": "129.93%", "FY2021": "124%"}),
    ],
    note="PILLAR-3-ONLY WORKBOOK: SBI UK takes the FRS 102 cash-flow-statement exemption, so the cash-flow sheet documents the exemption and the Overview contains the Pillar 3 trend chart only.",
)

bw.save("/Users/armaan/code/katalysis/banks/STATE BANK OF INDIA UK FINANCIALS.xlsx")
