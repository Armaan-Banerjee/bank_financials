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


STATEMENTS_SOURCES = (
    "Sources - State Bank of India (UK) Limited Annual Report and Financial Statements, £'000:\n"
    f"FY2025/FY2024: Annual Report 2025, Income statement/Statement of comprehensive income/Statement of "
    f"financial position/Statement of changes in equity, pp. 33-36 - {FS2025}\n"
    f"FY2023/FY2022: Annual Report 2023, same statements, pp. 31-34 - {FS2023}\n"
    f"FY2021: Annual Report 2021 (also carries the FY2020 comparative and the FY2021 opening-equity bridge "
    f"used to build the FY2022 opening row below), same statements, pp. 25-28 - {FS2021}\n"
    "All 5 years independently cross-checked against the adjacent report's own comparative column (FY2024 "
    "vs FY2025's comparative; FY2022 vs FY2023's comparative) - exact match in every case bar one £1k "
    "rounding artifact noted below.\n\n"
    + ENTITY_NOTE
    + "\n\nPRESENTATION NOTES: (1) FY2025's Other assets (4,877) and Balance Sheet total tie exactly, but "
    "FY2024's own originally-published Other assets figure (5,269, from the FY2024 report) is £1k higher "
    "than the comparative FY2025's report shows for FY2024 (5,268) - FY2024's own originally-published "
    "figure is used here, per project convention, producing a £1k rounding gap against FY2024's reported "
    "Total assets of 1,842,936 that is not reproduced in the line items (1,842,937) - a source rounding "
    "artifact, not an error in this workbook. (2) FY2025 splits Fixed assets into Tangible (3,638) and "
    "Intangible (232) for the first time; all other years disclose only a single combined Fixed assets "
    "line - a single combined 'Fixed assets (tangible & intangible)' row is used throughout for "
    "comparability (FY2025: 3,870 = 3,638 + 232). (3) FY2021's Balance Sheet splits retained earnings "
    "into 'Retained earnings' (11,468) and 'Profit and loss account for the year' (7,423); these are "
    "combined into a single Retained earnings row (18,891) matching later years' presentation - this "
    "combined figure is confirmed by the FY2023 report's own equity statement, which shows the FY2021 "
    "closing Profit and loss balance as 18,891. (4) Income statement line-item wording shifts over time: "
    "FY2022-FY2025 report 'Net gains from derivative financial instruments' (FY2025/FY2024 relabelled "
    "'Net gains from Forex and derivative financial instruments') plus a separate 'Gain/(Loss) on sale of "
    "investments' line; FY2021's report instead splits this into 'Net income/(expense) on foreign "
    "exchange' and 'Net gain on realised financial instruments', with no separate sale-of-investments "
    "line - both FY2021-only rows are shown separately and left blank for other years, documented rather "
    "than forced into the later years' line labels."
)

EQUITY_SOURCES = (
    "Sources - State Bank of India (UK) Limited Statement of Changes in Equity, £'000, chronological "
    "(oldest to newest):\n"
    f"FY2021 movements (opening 1 April 2020 through 31 March 2021): Annual Report 2021, p.28 - {FS2021}\n"
    f"FY2022/FY2023 movements: Annual Report 2023, p.34 - {FS2023}\n"
    f"FY2024/FY2025 movements: Annual Report 2025, p.36 - {FS2025}\n"
    "Every closing balance ties exactly to the next year's own opening balance and to that year's own "
    "Balance Sheet Total equity - confirmed via a fifth independent source (the FY2023 report's own SOCE "
    "restates the FY2021 closing balance as its own 1 April 2021 opening row: 225,000 / 18,891 / (74) / "
    "18,817 / 243,817, an exact match to the figure derived from the FY2021 report's own 4-column SOCE). "
    "Zero undocumented plug rows across all 5 years.\n\n"
    + ENTITY_NOTE
    + "\n\nPRESENTATION NOTE: FY2023/FY2024/FY2025 reports use a 5-column SOCE (Share capital / Profit "
    "and loss / Other comprehensive income / Total comprehensive income / Total equity); FY2021's own "
    "report uses a simpler 4-column SOCE (Share capital / Retained earnings / Investment revaluation "
    "reserve / Total equity) with no separate 'Total comprehensive income' column and a single combined "
    "AFS-revaluation movement line (not split into a gross revaluation line and a deferred-tax line, as "
    "the later years' reports do). The FY2021 movement rows below are shown exactly as the FY2021 report "
    "presents them, with a derived Total comprehensive income figure (Profit + OCI movement) added for "
    "structural consistency with later years - not a re-presentation of any figure."
)

ASSET_QUALITY_SOURCES = (
    "Sources - State Bank of India (UK) Limited Pillar 3 credit risk exposures (loans and advances to "
    "customers, maximum exposure by degree of risk of financial loss), £m:\n"
    + "\n".join(f"{y}: SBI UK Pillar 3 disclosure, pp. {PAGES[y]} - {P3[y]}" for y in YEARS)
    + "\n\nEach year's Total maximum exposure figure reconciles to the source table's own total (FY2022's "
    "reconciles to within £0.01m of its own reported total - a source rounding artifact, not an error in "
    "this workbook). This Total does not tie to the Balance Sheet's narrower 'Loans and advances to "
    "customers' line (a net, on-balance-sheet figure), since it also includes off-balance-sheet "
    "unutilised overdraft commitments and pipeline loans - a genuine, documented scope difference, not "
    "forced to tie. Forbearance facility counts/exposures are drawn from each year's own Pillar 3 "
    "forbearance-policy paragraph.\n\n"
    + ENTITY_NOTE
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - State Bank of India (UK) Limited UK OV1 (Overview of risk-weighted exposure amounts), £m:\n"
    + "\n".join(f"{y}: SBI UK Pillar 3 disclosure, pp. {PAGES[y]} - {P3[y]}" for y in YEARS)
    + "\n\nEach year's 3 category rows sum to that year's own reported Total, except FY2025: 1,216.73 + "
    "7.60 + 95.33 = 1,319.66m against a reported Total of 1,320.25m, a genuine ~£0.59m gap present in the "
    "source document's own UK OV1 table (confirmed by direct visual inspection of the source PDF page, "
    "not a transcription error in this workbook) - the reported Total is used as the TOTAL row, and the "
    "gap is not silently plugged into any category."
)


bw = BankWorkbook("State Bank of India (UK) Limited", YEARS, YEAR_LABEL, header_color="1B4D6B")

bw.add_balance_sheet_sheet(
    title="State Bank of India (UK) Limited — Balance Sheet",
    subtitle="Entity basis, £'000. See source note at bottom.",
    rows=[
        ("SECTION", "Assets", {}),
        ("DATA", "Cash and balances with banks", {"FY2025": 70262, "FY2024": 90746, "FY2023": 144199, "FY2022": 86381, "FY2021": 113623}),
        ("DATA", "Loans and advances to banks", {"FY2025": 7752, "FY2024": 20607, "FY2023": 79912, "FY2022": 100000, "FY2021": 125000}),
        ("DATA", "Loans and advances to customers", {"FY2025": 1529812, "FY2024": 1415920, "FY2023": 1403369, "FY2022": 1201300, "FY2021": 1140238}),
        ("DATA", "Investment securities", {"FY2025": 329255, "FY2024": 292784, "FY2023": 323130, "FY2022": 367831, "FY2021": 339418}),
        ("DATA", "Derivative financial instruments", {"FY2025": 14341, "FY2024": 13186, "FY2023": 12060, "FY2022": 8430, "FY2021": 25114}),
        ("DATA", "Fixed assets (tangible & intangible)", {"FY2025": 3870, "FY2024": 4425, "FY2023": 3130, "FY2022": 3463, "FY2021": 2807}),
        ("DATA", "Other assets", {"FY2025": 4877, "FY2024": 5269, "FY2023": 11162, "FY2022": 8600, "FY2021": 9210}),
        ("TOTAL", "Total assets", {"FY2025": 1960169, "FY2024": 1842936, "FY2023": 1976962, "FY2022": 1776005, "FY2021": 1755410}),
        ("SECTION", "Liabilities", {}),
        ("DATA", "Borrowings from banks", {"FY2025": 0, "FY2024": 16199, "FY2023": 121408, "FY2022": 164120, "FY2021": 128696}),
        ("DATA", "Deposit from customers", {"FY2025": 1655992, "FY2024": 1530535, "FY2023": 1568185, "FY2022": 1339203, "FY2021": 1360344}),
        ("DATA", "Derivative financial instruments", {"FY2025": 654, "FY2024": 538, "FY2023": 0, "FY2022": 6061, "FY2021": 0}),
        ("DATA", "Other liabilities", {"FY2025": 26063, "FY2024": 23402, "FY2023": 27217, "FY2022": 17015, "FY2021": 22553}),
        ("TOTAL", "Total liabilities", {"FY2025": 1682709, "FY2024": 1570674, "FY2023": 1716810, "FY2022": 1526399, "FY2021": 1511593}),
        ("SECTION", "Shareholders' funds", {}),
        ("DATA", "Share capital", {"FY2025": 225000, "FY2024": 225000, "FY2023": 225000, "FY2022": 225000, "FY2021": 225000}),
        ("DATA", "Investment revaluation reserve", {"FY2025": -717, "FY2024": -2390, "FY2023": -5100, "FY2022": -2896, "FY2021": -74}),
        ("DATA", "Retained earnings", {"FY2025": 53177, "FY2024": 49652, "FY2023": 40252, "FY2022": 27502, "FY2021": 18891}),
        ("TOTAL", "Total equity", {"FY2025": 277460, "FY2024": 272262, "FY2023": 260152, "FY2022": 249606, "FY2021": 243817}),
        ("TOTAL", "Total liabilities and equity", {"FY2025": 1960169, "FY2024": 1842936, "FY2023": 1976962, "FY2022": 1776005, "FY2021": 1755410}),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=64,
    source_height=340,
)

bw.add_income_statement_sheet(
    title="State Bank of India (UK) Limited — Profit & Loss",
    subtitle="Entity basis, £'000. See source note at bottom.",
    rows=[
        ("SECTION", "Income", {}),
        ("DATA", "Interest receivable and similar income", {"FY2025": 101825, "FY2024": 98608, "FY2023": 71035, "FY2022": 43575, "FY2021": 40339}),
        ("DATA", "Interest payable and similar charges", {"FY2025": -56644, "FY2024": -47190, "FY2023": -23899, "FY2022": -8914, "FY2021": -16735}),
        ("TOTAL", "Net interest income", {"FY2025": 45181, "FY2024": 51418, "FY2023": 47136, "FY2022": 34661, "FY2021": 23604}),
        ("DATA", "Fees and commissions income", {"FY2025": 1772, "FY2024": 1486, "FY2023": 1543, "FY2022": 912, "FY2021": 1303}),
        ("DATA", "Net gains from Forex and derivative financial instruments", {"FY2025": 1615, "FY2024": 1607, "FY2023": 1652, "FY2022": 1484}),
        ("DATA", "Net income/(expense) on foreign exchange (FY2021 only, see note)", {"FY2021": 991}),
        ("DATA", "Net gain on realised financial instruments (FY2021 only, see note)", {"FY2021": 537}),
        ("DATA", "Gain/(Loss) on sale of investments", {"FY2025": 10, "FY2024": 51, "FY2023": -1314, "FY2022": 536}),
        ("DATA", "Other operating income", {"FY2025": 7, "FY2024": 37, "FY2023": 28, "FY2022": 30, "FY2021": 195}),
        ("TOTAL", "Operating income", {"FY2025": 48585, "FY2024": 54599, "FY2023": 49045, "FY2022": 37623, "FY2021": 26630}),
        ("SECTION", "Expenses", {}),
        ("DATA", "Administrative expenses", {"FY2025": -23568, "FY2024": -21916, "FY2023": -21791, "FY2022": -17610, "FY2021": -15515}),
        ("DATA", "Depreciation", {"FY2025": -856, "FY2024": -743, "FY2023": -731, "FY2022": -711, "FY2021": -695}),
        ("TOTAL", "Total operating expenses", {"FY2025": -24424, "FY2024": -22659, "FY2023": -22522, "FY2022": -18321, "FY2021": -16210}),
        ("TOTAL", "Operating profit before profit/(loss) on sale of loans, impairment and taxes", {"FY2025": 24161, "FY2024": 31940, "FY2023": 26523, "FY2022": 19302, "FY2021": 10420}),
        ("DATA", "Profit/(loss) on sale of loans", {"FY2025": -158, "FY2024": -194, "FY2023": 9, "FY2022": -44, "FY2021": 129}),
        ("DATA", "Impairment reversal/(charge) on loans", {"FY2025": 651, "FY2024": 106, "FY2023": -219, "FY2022": -1546, "FY2021": -1352}),
        ("TOTAL", "Profit on ordinary activities before tax", {"FY2025": 24654, "FY2024": 31852, "FY2023": 26313, "FY2022": 17712, "FY2021": 9197}),
        ("DATA", "Tax on profit of ordinary activities", {"FY2025": -6129, "FY2024": -8052, "FY2023": -5125, "FY2022": -3476, "FY2021": -1774}),
        ("TOTAL", "Profit on ordinary activities after tax", {"FY2025": 18525, "FY2024": 23800, "FY2023": 21188, "FY2022": 14236, "FY2021": 7423}),
        ("SECTION", "Other comprehensive income", {}),
        ("DATA", "Revaluation of available-for-sale investment/debt securities", {"FY2025": 2230, "FY2024": 3613, "FY2023": -2939, "FY2022": -3770, "FY2021": 870}),
        ("DATA", "Deferred tax adjustment on available-for-sale investment securities", {"FY2025": -557, "FY2024": -903, "FY2023": 735, "FY2022": 948, "FY2021": -165}),
        ("TOTAL", "Total other comprehensive income", {"FY2025": 1673, "FY2024": 2710, "FY2023": -2204, "FY2022": -2822, "FY2021": 705}),
        ("TOTAL", "Total comprehensive income for the year", {"FY2025": 20198, "FY2024": 26510, "FY2023": 18984, "FY2022": 11414, "FY2021": 8128}),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=340,
)

EQUITY_HEADERS = ["Share capital", "Profit and loss", "Other comprehensive income", "Total comprehensive income", "Total equity"]
bw.add_equity_changes_sheet(
    title="State Bank of India (UK) Limited — Statement of Changes in Equity",
    subtitle="Entity basis, £'000, chronological (oldest to newest). See source note at bottom.",
    headers=EQUITY_HEADERS,
    rows=[
        ("TOTAL", "As at 1 April 2020", (175000, 11468, -779, None, 185689)),
        ("DATA", "Conversion of subordinated debt to equity capital", (50000, 0, 0, 0, 50000)),
        ("DATA", "Profit on ordinary activities after tax", (0, 7423, 0, 7423, 7423)),
        ("DATA", "Movement in valuation of available-for-sale debt securities (net of deferred tax)", (0, 0, 705, 705, 705)),
        ("TOTAL", "As at 31 March 2021", (225000, 18891, -74, 18817, 243817)),
        ("DATA", "Profit on ordinary activities after tax", (0, 14236, 0, 14236, 14236)),
        ("DATA", "Interim dividends paid", (0, -5625, 0, -5625, -5625)),
        ("DATA", "Movement in valuation of available-for-sale debt securities", (0, 0, -3770, -3770, -3770)),
        ("DATA", "Deferred tax", (0, 0, 948, 948, 948)),
        ("TOTAL", "As at 31 March 2022", (225000, 27502, -2896, 24606, 249606)),
        ("DATA", "Profit on ordinary activities after tax", (0, 21188, 0, 21188, 21188)),
        ("DATA", "Interim dividends paid", (0, -8438, 0, -8438, -8438)),
        ("DATA", "Movement in valuation of available-for-sale debt securities", (0, 0, -2939, -2939, -2939)),
        ("DATA", "Deferred tax", (0, 0, 735, 735, 735)),
        ("TOTAL", "As at 31 March 2023", (225000, 40252, -5100, 35152, 260152)),
        ("DATA", "Interim dividends paid", (0, -14400, 0, -14400, -14400)),
        ("DATA", "Profit on ordinary activities after tax", (0, 23800, 0, 23800, 23800)),
        ("DATA", "Movement in valuation of available-for-sale debt securities", (0, 0, 3613, 3613, 3613)),
        ("DATA", "Deferred tax", (0, 0, -903, -903, -903)),
        ("TOTAL", "As at 31 March 2024", (225000, 49652, -2390, 47262, 272262)),
        ("DATA", "Interim dividends paid", (0, -15000, 0, -15000, -15000)),
        ("DATA", "Profit on ordinary activities after tax", (0, 18525, 0, 18525, 18525)),
        ("DATA", "Movement in valuation of available-for-sale debt securities", (0, 0, 2230, 2230, 2230)),
        ("DATA", "Deferred tax", (0, 0, -557, -557, -557)),
        ("TOTAL", "As at 31 March 2025", (225000, 53177, -717, 52460, 277460)),
    ],
    sources_text=EQUITY_SOURCES,
    source_height=340,
)

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

bw.add_asset_quality_sheet(
    title="State Bank of India (UK) Limited — Asset Quality",
    subtitle="Pillar 3 credit risk exposures, £m. Not IFRS 9-staged (FRS 102 entity) — categorised by degree "
              "of risk of financial loss. See source note at bottom.",
    rows=[
        ("SECTION", "Loan book by risk of financial loss (Pillar 3 credit risk exposures)", {}),
        ("DATA", "Neither past due beyond 90 days nor impaired", {"FY2025": 1537.46, "FY2024": 1420.37, "FY2023": 1408.07, "FY2022": 1205.40, "FY2021": 1142.58}),
        ("DATA", "Past due beyond 90 days, but not impaired", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
        ("DATA", "Impaired", {"FY2025": 0, "FY2024": 2.19, "FY2023": 5.32, "FY2022": 5.03, "FY2021": 4.61}),
        ("DATA", "Repossessions", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
        ("DATA", "Unutilised overdraft commitments", {"FY2025": 19.93, "FY2024": 34.79, "FY2023": 25.45, "FY2022": 6.52, "FY2021": 8.51}),
        ("DATA", "Pipeline loans", {"FY2025": 37.89, "FY2024": 10.67, "FY2023": 15.71, "FY2022": 69.29, "FY2021": 86.83}),
        ("TOTAL", "Total maximum exposure of loans and advances to customers", {"FY2025": 1595.28, "FY2024": 1468.02, "FY2023": 1454.55, "FY2022": 1286.23, "FY2021": 1242.53}),
        ("SECTION", "Collateral", {}),
        ("DATA", "Collateral value", {"FY2025": 1288.58, "FY2024": 1149.26, "FY2023": 1048.50, "FY2022": 770.94, "FY2021": 596.94}),
        ("DATA", "Gross loans and advances", {"FY2025": 1537.45, "FY2024": 1422.56, "FY2023": 1413.39, "FY2022": 1210.42, "FY2021": 1147.19}),
        ("DATA", "Collateral coverage (% of gross loans and advances)", {"FY2025": "83.81%", "FY2024": "80.79%", "FY2023": "74.18%", "FY2022": "63.69%", "FY2021": "52.03%"}),
        ("SECTION", "Forbearance", {}),
        ("DATA", "Business customers granted forbearance (count)", {"FY2025": 3, "FY2024": 4, "FY2023": 3, "FY2022": 7, "FY2021": 8}),
        ("DATA", "Total forbearance exposure, £m", {"FY2025": 4.60, "FY2024": 6.13, "FY2023": 6.71, "FY2022": 83, "FY2021": 82}),
    ],
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=66,
    source_height=260,
    unit_suffix=" (£m)",
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

bw.add_rwa_breakdown_sheet(
    title="State Bank of India (UK) Limited — RWA Breakdown",
    subtitle="UK OV1 - Overview of risk-weighted exposure amounts, £m. See source note at bottom.",
    rows=[
        ("SECTION", "UK OV1 — Overview of risk-weighted exposure amounts", {}),
        ("DATA", "Credit risk (excluding CCR)", {"FY2025": 1216.73, "FY2024": 1115.26, "FY2023": 1138.84, "FY2022": 1201.92, "FY2021": 1286.62}),
        ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 7.60, "FY2024": 9.05, "FY2023": 16.89, "FY2022": 17.00, "FY2021": 18.47}),
        ("DATA", "Operational risk", {"FY2025": 95.33, "FY2024": 88.71, "FY2023": 71.30, "FY2022": 57.76, "FY2021": 52.66}),
        ("TOTAL", "Total risk-weighted exposure amount", {"FY2025": 1320.25, "FY2024": 1213.02, "FY2023": 1227.04, "FY2022": 1276.68, "FY2021": 1357.75}),
    ],
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=54,
    source_height=200,
    unit_suffix=" (£m)",
)

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
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 1960169, "FY2024": 1842936, "FY2023": 1976962, "FY2022": 1776005, "FY2021": 1755410}),
        ("Loans and advances to customers", {"FY2025": 1529812, "FY2024": 1415920, "FY2023": 1403369, "FY2022": 1201300, "FY2021": 1140238}),
        ("Deposit from customers", {"FY2025": 1655992, "FY2024": 1530535, "FY2023": 1568185, "FY2022": 1339203, "FY2021": 1360344}),
        ("Total equity", {"FY2025": 277460, "FY2024": 272262, "FY2023": 260152, "FY2022": 249606, "FY2021": 243817}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Operating income", {"FY2025": 48585, "FY2024": 54599, "FY2023": 49045, "FY2022": 37623, "FY2021": 26630}),
        ("Total operating expenses", {"FY2025": -24424, "FY2024": -22659, "FY2023": -22522, "FY2022": -18321, "FY2021": -16210}),
        ("Profit on ordinary activities after tax", {"FY2025": 18525, "FY2024": 23800, "FY2023": 21188, "FY2022": 14236, "FY2021": 7423}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 272262, "FY2024": 260152, "FY2023": 249606, "FY2022": 243817, "FY2021": 185689}),
        ("Total comprehensive income for the year", {"FY2025": 20198, "FY2024": 26510, "FY2023": 18984, "FY2022": 11414, "FY2021": 8128}),
        ("Other equity movements, net", {"FY2025": -15000, "FY2024": -14400, "FY2023": -8438, "FY2022": -5625, "FY2021": 50000}),
        ("Closing equity", {"FY2025": 277460, "FY2024": 272262, "FY2023": 260152, "FY2022": 249606, "FY2021": 243817}),
    ],
    equity_changes_unit="£'000",
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
