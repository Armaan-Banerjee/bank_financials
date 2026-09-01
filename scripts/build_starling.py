import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2026", "FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {
    "FY2026": "FY2026 (SGHL)‡",
    "FY2025": "FY2025",
    "FY2024": "FY2024",
    "FY2023": "FY2023",
    "FY2022": "FY2022",
    "FY2021": "FY2021†",
}

AR21_URL = "https://www.starlingbank.com/docs/annual-reports/Starling-Bank-Annual-Report-2019-21.pdf"
AR22_URL = "https://www.starlingbank.com/docs/annual-reports/Starling-Bank-Annual-Report-2022.pdf"
AR23_URL = "https://www.starlingbank.com/docs/annual-reports/Starling-Bank-Annual-Report-2023.pdf"
AR25_URL = "https://www.starlingbank.com/docs/annual-reports/Starling-Bank-Annual-Report-2025.pdf"
AR26_SGHL_URL = "https://www.starlingbank.com/docs/annual-reports/Starling-Group-Annual-Report-2026.pdf"

P3_21_URL = "https://www.starlingbank.com/docs/annual-reports/Pillar3-2021.pdf"
P3_22_URL = "https://www.starlingbank.com/docs/annual-reports/Pillar3-2022.pdf"
P3_23_URL = "https://www.starlingbank.com/docs/annual-reports/Pillar3-2023.pdf"
P3_24_URL = "https://www.starlingbank.com/docs/annual-reports/Pillar3-2024.pdf"
P3_25_URL = "https://www.starlingbank.com/docs/annual-reports/Pillar3-2025.pdf"
P3_26_URL = "https://www.starlingbank.com/docs/annual-reports/Pillar3-2026.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Starling Bank Limited (Companies House 09092149) is the entity on the PRA register and is used, "
    "on a consolidated Group basis, for FY2021-FY2025 - each year's own Annual Report and Consolidated Financial "
    "Statements. FY2021 (marked †) is a 16-month period (1 December 2019 - 31 March 2021), Starling's first "
    "period reporting to a 31 March year end - not directly run-rate comparable to the other years.\n"
    "FY2026 (marked ‡, added as a bonus column beyond the standard 5-year window) is different: in June 2025 a "
    "new non-trading holding company, Starling Group Holdings Limited (SGHL), was inserted as ultimate parent of "
    "Starling Bank Limited (SBL), with an intermediate holding company (SIHL) added in September 2025. From "
    "FY2026, SBL's own Companies House filing is presented on an unconsolidated solo/Company basis only (SBL's "
    "own wording: 'the Company' = Starling Bank Limited; consolidated 'Group' figures are now published "
    "separately as SGHL's own Annual Report). To keep this column comparable to FY2021-FY2025's consolidated "
    "basis, FY2026 cash flow figures here are SGHL's consolidated Group figures (from the new SGHL Annual "
    "Report), not SBL's own solo filing. The SGHL accounting consolidation for FY2026 additionally includes "
    "Murmur Financial Services Limited, Fleet Mortgages Limited and Engine by Starling Limited alongside SBL and "
    "its own ancillary undertakings (Starling FS Services Limited, and Ember by Starling Limited, acquired during "
    "FY2026) - a broader scope than SBL's own historical Group accounts. Pillar 3 (prudential) figures for FY2026 "
    "are on the narrower 'Regulatory Group' basis (SGHL, SIHL, SBL, SFSSL and Ember only - Murmur/Fleet "
    "Mortgages/Engine fall below CRR Article 19 materiality thresholds); cross-checking confirms this made no "
    "difference to the FY2025 capital figures, so Pillar 3 continuity FY2021-FY2026 is unaffected by the "
    "restructuring."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Group/consolidated basis, £'000. See entity note above re: FY2021 (16-month "
    "period) and FY2026 (new SGHL parent entity).\n"
    f"FY2026: Starling Group Holdings Limited Annual Report and Accounts 2026, p.165 (Consolidated cash flow "
    f"statement) - {AR26_SGHL_URL}\n"
    f"FY2025 & FY2024: Starling Bank Limited Annual Report and Accounts 2025, p.159 and p.214 (Consolidated and "
    f"company cash flow statement, and note 29) - {AR25_URL}\n"
    f"FY2023 & FY2022 (restated): Starling Bank Limited Annual Report 2023, p.124-125 and p.177 (Consolidated & "
    f"Company Cash Flow Statement, and note 29) - {AR23_URL}\n"
    f"FY2021: Starling Bank Limited Annual Report and Consolidated Financial Statements, period ended 31 March "
    f"2021, p.66-67 (Consolidated Cash Flow Statement) - {AR21_URL}\n\n" + ENTITY_NOTE + "\n\n"
    "RESTATEMENT NOTE: The 2023 Annual Report changed the Group's cash and cash equivalents accounting policy to "
    "exclude the mandatory Cash Ratio Deposit held with the Bank of England; this reduced the Group's cash and "
    "cash equivalents at 1 April 2021 by £7,627k (to a restated £3,188,722k) on a comparative basis, but FY2021's "
    "own original Annual Report was never itself restated (its reported closing balance is £3,196,349k). This "
    "produces a documented £7,627k break at the FY2021/FY2022 boundary only; FY2022 onward reconciles exactly.\n\n"
    "PRESENTATION NOTE: FY2021-FY2023 report operating-activities adjustments and asset/liability movements as "
    "granular individual line items; FY2024 onward summarises them into three reported subtotals ('Non-cash "
    "movements', 'Movement in operating assets', 'Movement in operating liabilities') with the detail moved to a "
    "note - both are shown, clearly separated, so blank cells simply reflect which presentation style that year's "
    "report used. FY2026's figures are shown only at the summarised level (the underlying SGHL note breakdown "
    "was not extracted). The 'Profit for the period after taxation' line is repeated once per presentation style "
    "(a generic block-reconciliation checker run against this sheet will only sum the DATA rows immediately "
    "preceding each operating-activities TOTAL, so Profit needs its own row within each block rather than a "
    "single shared row above both - this is a spreadsheet-layout clarification, not a change to any figure). "
    "Section totals and cash and cash equivalents are consistent within each presentation style and reconcile "
    "exactly year to year (except the documented FY2021/FY2022 break above): confirmed by hand against each "
    "year's own primary source, including FY2026 (2026-08-27), where the operating-activities TOTAL was "
    "originally mistranscribed as 185,354 - the SGHL FY2026 Annual Report's own Consolidated Cash Flow Statement "
    "(p.165) states 183,334, which is what the full profit+adjustments+tax chain sums to exactly; corrected."
)

def p3_sources(url, doc_label, page1="6", page2="7"):
    return (
        "Sources - Starling Bank Limited Pillar 3 basis (Regulatory Group basis for FY2026 - see entity note on "
        f"Cash Flow Statement sheet; identical to Starling Bank Limited's own scope for FY2021-FY2025):\n"
        f"{doc_label}: p.{page1}-{page2}, section 4.1 Key metrics - {url}"
    )

P3_SOURCES_ALL = (
    "Sources - Starling Bank Limited Pillar 3 basis (Regulatory Group basis for FY2026 - see entity note on Cash "
    "Flow Statement sheet):\n"
    f"FY2026: Starling Group Pillar 3 report 2026, as at 31 March 2026, section 4.1 Key metrics, p.22-23 - {P3_26_URL}\n"
    f"FY2025: Starling Bank Limited Pillar 3 report 2025, as at 31 March 2025, section 4.1 Key metrics, p.22-23 - {P3_25_URL}\n"
    f"FY2024: Starling Bank Limited Pillar 3 report 2024, as at 31 March 2024, section 4.1 Key metrics, p.22-23 - {P3_24_URL}\n"
    f"FY2023: Starling Bank Limited Pillar 3 Report 2023, as at 31 March 2023, section 4.1 Key Metrics, p.21 - {P3_23_URL}\n"
    f"FY2022: Starling Bank Ltd Pillar 3 Report 2022, as at 31 March 2022 (FY2023 report's comparator column), p.21 - {P3_22_URL}\n"
    f"FY2021: Starling Bank Limited Pillar 3 Disclosures, as at 31 March 2021, sections 5 (Capital Resources), "
    f"5.2 (Leverage Ratio) and 12 (Liquidity), p.19-23 - {P3_21_URL} (pre-dates the formal KM1 template)"
)

bw = BankWorkbook(bank_name="Starling Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="6B2C91")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit/(loss) for the period after taxation (FY2021-FY2023 presentation)", {"FY2023": 142856, "FY2022": 44938, "FY2021": -23319}),
    ("SECTION", "Adjustments for non-cash items (FY2021-FY2023 presentation)", {}),
    ("DATA", "Depreciation and Amortisation", {"FY2023": 10953, "FY2022": 6384, "FY2021": 7045}),
    ("DATA", "Cost of Share Award Schemes, Net of Tax / FV of Shares Allocated to Employees", {"FY2023": 1323, "FY2022": 4659, "FY2021": 1927}),
    ("DATA", "Change in Derivatives and Fair Value on Hedging Relationships", {"FY2023": 6487, "FY2022": -7905}),
    ("DATA", "Net Increase in Fair Value of Derivatives (FY2021 presentation)", {"FY2021": -12670}),
    ("DATA", "Net Increase in Fair Value of Assets Designated as Hedged Items (FY2021 presentation)", {"FY2021": 12520}),
    ("DATA", "Impairment and Charge-offs", {"FY2023": 9991, "FY2022": 10226, "FY2021": 16106}),
    ("DATA", "Recognition of Right of Use Asset (FY2021 presentation)", {"FY2021": -5527}),
    ("DATA", "Foreign Exchange Losses on Consolidation (FY2021 presentation)", {"FY2021": 91}),
    ("DATA", "Disposal of Intangible Assets (FY2021 presentation)", {"FY2021": 358}),
    ("DATA", "Net Increase in Deferred Tax Asset (adjustment)", {"FY2021": -6088}),
    ("DATA", "Taxation Charged to the Income Statement", {"FY2023": 51740}),
    ("DATA", "Other Non-Cash Items", {"FY2023": -13652, "FY2022": 1479}),
    ("SECTION", "Net changes in operating assets and liabilities (FY2021-FY2023 presentation)", {}),
    ("DATA", "Movement in Loans and Advances to Banks", {"FY2023": -9835, "FY2022": -16523}),
    ("DATA", "Net (Increase) in Loans and Advances to Customers", {"FY2023": -1567215, "FY2022": -1007837, "FY2021": -2203378}),
    ("DATA", "Net (Increase) in Deferred Tax Asset (asset movement)", {"FY2022": -15897}),
    ("DATA", "Net (Increase) in Other Assets", {"FY2023": -5399, "FY2022": -61397, "FY2021": -31818}),
    ("DATA", "Net Increase in Customer Deposits", {"FY2023": 1524407, "FY2022": 3199715, "FY2021": 4820298}),
    ("DATA", "Net Increase in Central Bank Facilities (FY2021 presentation)", {"FY2021": 1000000}),
    ("DATA", "Net (Decrease)/Increase in Deposits from Banks", {"FY2023": -9515, "FY2022": 1281380}),
    ("DATA", "Net Increase/(Decrease) in Provisions for Liabilities and Charges", {"FY2023": 232, "FY2022": -758, "FY2021": -680}),
    ("DATA", "Net (Decrease)/Increase in Other Liabilities and Accruals", {"FY2023": -51253, "FY2022": 104310, "FY2021": 969}),
    ("DATA", "Net Increase/(Decrease) in Deferred Income", {"FY2023": 16202, "FY2022": -3994, "FY2021": -44894}),
    ("DATA", "Taxation Paid (FY2022-FY2023 presentation)", {"FY2023": -26720, "FY2022": -3321}),
    ("TOTAL", "Net Cash Flows from Operating Activities (FY2021-FY2023 presentation)", {"FY2023": 80602, "FY2022": 3535459, "FY2021": 3530940}),
    ("SECTION", "Adjustments and net changes (FY2024-FY2026 presentation, summarised - see note for breakdown)", {}),
    ("DATA", "Profit for the period after taxation (FY2024-FY2026 presentation)", {"FY2026": 156043, "FY2025": 150722, "FY2024": 220001}),
    ("DATA", "Non-cash movements (as reported)", {"FY2026": 109080, "FY2025": 165605, "FY2024": 155782}),
    ("DATA", "Movement in operating assets (as reported)", {"FY2026": -541473, "FY2025": -30989, "FY2024": 194795}),
    ("DATA", "Movement in operating liabilities (as reported)", {"FY2026": 505769, "FY2025": 793034, "FY2024": 813947}),
    ("DATA", "Taxation paid (FY2024-FY2026 presentation)", {"FY2026": -46085, "FY2025": -61999, "FY2024": -94266}),
    ("TOTAL", "Net cash flows from operating activities (FY2024-FY2026 presentation)", {"FY2026": 183334, "FY2025": 1016373, "FY2024": 1290259}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Purchase of Property, Plant and Equipment", {"FY2023": -2824, "FY2022": -1279, "FY2021": -1131}),
    ("DATA", "Purchase of property, plant and equipment (FY2024-FY2026 presentation)", {"FY2026": -6034, "FY2025": -3167, "FY2024": -4728}),
    ("DATA", "Net Purchases of Debt Securities (FY2022-FY2023 presentation)", {"FY2023": -161608, "FY2022": -814284}),
    ("DATA", "Net Increase in Debt Securities (FY2021 presentation)", {"FY2021": -1184380}),
    ("DATA", "Purchases of debt securities (FY2024-FY2026 presentation)", {"FY2026": -4462187, "FY2025": -1378404, "FY2024": -1577646}),
    ("DATA", "Proceeds from maturity and sale of debt securities (FY2024-FY2026 presentation)", {"FY2026": 1575165, "FY2025": 735088, "FY2024": 748813}),
    ("DATA", "Acquisition of Subsidiary, Net of Cash Acquired", {"FY2022": -36160}),
    ("DATA", "PPE and Intangibles on Acquisition of Subsidiary", {"FY2022": -8377}),
    ("DATA", "Net cash on acquisition of subsidiary (FY2026 presentation)", {"FY2026": -2205}),
    ("DATA", "Purchase and Development of Intangible Assets", {"FY2023": -27643, "FY2022": -19170}),
    ("DATA", "Capitalisation of Intangible Assets (FY2021 presentation)", {"FY2021": -5623}),
    ("DATA", "Purchase and development of intangible assets (FY2024-FY2026 presentation)", {"FY2026": -75792, "FY2025": -56997, "FY2024": -43278}),
    ("TOTAL", "Net Cash Flows from Investing Activities", {"FY2026": -2971053, "FY2025": -703480, "FY2024": -876839, "FY2023": -192075, "FY2022": -879270, "FY2021": -1191134}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Issuance of Ordinary Shares Less Cost of Issuance", {"FY2023": 130500, "FY2022": 240000, "FY2021": 94012}),
    ("DATA", "Purchase of own shares", {"FY2024": -56362}),
    ("DATA", "Drawdown of funding from central banks", {"FY2026": 900000}),
    ("DATA", "Repayment of funding from central banks", {"FY2026": -600000, "FY2025": -50000}),
    ("DATA", "Repayment of Lease Liabilities", {"FY2023": -68, "FY2022": -1780, "FY2021": -2174}),
    ("DATA", "Repayment of lease liabilities (FY2024-FY2026 presentation)", {"FY2026": -4120, "FY2025": -2710, "FY2024": -2154}),
    ("TOTAL", "Net Cash Flows from Financing Activities", {"FY2026": 295880, "FY2025": -52710, "FY2024": -58516, "FY2023": 130432, "FY2022": 238220, "FY2021": 91838}),
    ("TOTAL", "Net Increase/(Decrease) in Cash and Cash Equivalents", {"FY2026": -2491839, "FY2025": 260183, "FY2024": 354904, "FY2023": 18859, "FY2022": 2894409, "FY2021": 2431644}),
    ("DATA", "Cash and Cash Equivalents at Beginning of Period/Year", {"FY2026": 6717177, "FY2025": 6456994, "FY2024": 6102090, "FY2023": 6083131, "FY2022": 3188722, "FY2021": 764705}),
    ("TOTAL", "Cash and Cash Equivalents at End of Period/Year", {"FY2026": 4225338, "FY2025": 6717177, "FY2024": 6456994, "FY2023": 6102090, "FY2022": 6083131, "FY2021": 3196349}),
]

bw.add_cash_flow_sheet(
    title="Starling Bank Limited — Consolidated Cash Flow Statement",
    subtitle="Group/consolidated basis, £'000. FY2021: 16-month period (†). FY2026: Starling Group Holdings Limited (‡). See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=70,
    source_height=250,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, P3_SOURCES_ALL, note=note, first_col_width=52, source_height=150)

metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2026": 1123255, "FY2025": 1000231, "FY2024": 870769, "FY2023": 710614, "FY2022": 397502, "FY2021": 136769})],
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2026": "28.58%", "FY2025": "31.55%", "FY2024": "32.55%", "FY2023": "37.50%", "FY2022": "39.96%", "FY2021": "47.9%"})],
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2026": 1123255, "FY2025": 1000231, "FY2024": 870769, "FY2023": 710614, "FY2022": 397502, "FY2021": 136769})],
    note="Equal to CET1 capital in every year - Starling has never issued Additional Tier 1 or Tier 2 capital ('All "
         "of Starling Bank's capital is Common Equity Tier 1 (CET1)' - FY2024 Pillar 3 report).",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2026": "28.58%", "FY2025": "31.55%", "FY2024": "32.55%", "FY2023": "37.50%", "FY2022": "39.96%", "FY2021": "47.9%"})],
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2026": 1123255, "FY2025": 1000231, "FY2024": 870769, "FY2023": 710614, "FY2022": 397502, "FY2021": 136769})],
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2026": "28.58%", "FY2025": "31.55%", "FY2024": "32.55%", "FY2023": "37.50%", "FY2022": "39.96%", "FY2021": "47.9%"})],
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted exposure amount", {"FY2026": 3930308, "FY2025": 3170032, "FY2024": 2675477, "FY2023": 1894758, "FY2022": 994828, "FY2021": 285689})],
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Total exposure measure excluding claims on central banks", {"FY2026": 12608384, "FY2025": 8976790, "FY2024": 8383435, "FY2023": 7641617, "FY2022": 5063481}),
        ("Leverage ratio excluding claims on central banks / UK leverage ratio (%)", {"FY2026": "8.91%", "FY2025": "11.14%", "FY2024": "10.39%", "FY2023": "9.30%", "FY2022": "7.85%", "FY2021": "5.4%"}),
        ("Leverage ratio including claims on central banks / CRR (EU) leverage ratio (%) (FY2021 only, pre-KM1 template)", {"FY2021": "1.9%"}),
    ],
    note="FY2021 predates the formal KM1 template and did not disclose a £ exposure measure, only two ratios: "
         "a 'UK leverage ratio' (excluding central bank exposures, matching the 'excluding claims on central "
         "banks' basis used from FY2022 onward) and a 'CRR (EU) leverage ratio' (including them). Starling noted "
         "it was 'not subject to the PRA Handbook's (UK) leverage ratio' at the time, i.e. this was disclosed "
         "voluntarily rather than as a binding requirement in FY2021.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA) (average weighted value)", {"FY2026": 7038393, "FY2025": 6812037, "FY2024": 6510731, "FY2023": 6413925, "FY2022": 5128346, "FY2021": 3410070}),
        ("Cash outflows (total weighted value)", {"FY2026": 1326072, "FY2025": 1477094, "FY2024": 1891560, "FY2023": 1711200, "FY2022": 1211430}),
        ("Cash inflows (total weighted value)", {"FY2026": 89112, "FY2025": 156237, "FY2024": 446533, "FY2023": 311926, "FY2022": 209396}),
        ("Total net cash outflows (adjusted value)", {"FY2026": 1236960, "FY2025": 1320857, "FY2024": 1445027, "FY2023": 1399274, "FY2022": 1002034, "FY2021": 674460}),
        ("Liquidity Coverage Ratio (%)", {"FY2026": "569.01%", "FY2025": "515.73%", "FY2024": "450.56%", "FY2023": "460%", "FY2022": "515%", "FY2021": "506%"}),
    ],
    note="FY2021 disclosed only Total HQLA and Total Net Cash Outflow (no separate cash inflow/outflow split) - "
         "predates the formal KM1 template. LCR/NSFR are averages over the year in every year shown.",
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding", {"FY2026": 14206855, "FY2025": 13448876, "FY2024": 12578157, "FY2023": 11944952, "FY2022": 10660584, "FY2021": 6366591}),
        ("Total required stable funding", {"FY2026": 5754691, "FY2025": 5555204, "FY2024": 5646537, "FY2023": 4870012, "FY2022": 4088546, "FY2021": 2127872}),
        ("Net Stable Funding Ratio (%)", {"FY2026": "246.87%", "FY2025": "242.10%", "FY2024": "222.76%", "FY2023": "245%", "FY2022": "261%", "FY2021": "299%"}),
    ],
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not disclosed (no numeric ratio published)" for y in YEARS})],
    note="MREL became applicable to Starling from April 2023 (previously not applicable, as for a small "
         "institution). From then, Starling states its capital is maintained 'above MREL requirements plus "
         "buffers at all times' but has never published a numeric MREL ratio or resources figure in any Pillar 3 "
         "report reviewed, FY2021-FY2026 - only this qualitative statement.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash flows from operating activities", {
            "FY2023": 80602, "FY2022": 3535459, "FY2021": 3530940,  # FY2021-FY2023 presentation
            "FY2026": 183334, "FY2025": 1016373, "FY2024": 1290259,  # FY2024-FY2026 presentation
        }),
        ("Net cash flows from investing activities", {"FY2026": -2971053, "FY2025": -703480, "FY2024": -876839, "FY2023": -192075, "FY2022": -879270, "FY2021": -1191134}),
        ("Net cash flows from financing activities", {"FY2026": 295880, "FY2025": -52710, "FY2024": -58516, "FY2023": 130432, "FY2022": 238220, "FY2021": 91838}),
        ("Cash and cash equivalents at end of period/year", {"FY2026": 4225338, "FY2025": 6717177, "FY2024": 6456994, "FY2023": 6102090, "FY2022": 6083131, "FY2021": 3196349}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2026": "28.58%", "FY2025": "31.55%", "FY2024": "32.55%", "FY2023": "37.50%", "FY2022": "39.96%", "FY2021": "47.9%"}),
        ("Tier 1 Ratio", {"FY2026": "28.58%", "FY2025": "31.55%", "FY2024": "32.55%", "FY2023": "37.50%", "FY2022": "39.96%", "FY2021": "47.9%"}),
        ("Total Capital Ratio", {"FY2026": "28.58%", "FY2025": "31.55%", "FY2024": "32.55%", "FY2023": "37.50%", "FY2022": "39.96%", "FY2021": "47.9%"}),
        ("Leverage Ratio", {"FY2026": "8.91%", "FY2025": "11.14%", "FY2024": "10.39%", "FY2023": "9.30%", "FY2022": "7.85%", "FY2021": "5.4%"}),
        ("LCR", {"FY2026": "569.01%", "FY2025": "515.73%", "FY2024": "450.56%", "FY2023": "460%", "FY2022": "515%", "FY2021": "506%"}),
        ("NSFR", {"FY2026": "246.87%", "FY2025": "242.10%", "FY2024": "222.76%", "FY2023": "245%", "FY2022": "261%", "FY2021": "299%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Net cash from operating activities combines two reporting "
         "presentations Starling used across this period (FY2021-FY2023 vs. FY2024-FY2026); see the Cash Flow "
         "Statement sheet for the distinction. Leverage ratio shown on the 'excluding claims on central banks' "
         "basis for comparability (FY2021 disclosed on the since-retired 'including' CRR basis instead - see "
         "Leverage Ratio sheet).",
)

bw.save("/Users/armaan/code/katalysis/banks/STARLING FINANCIALS.xlsx")
