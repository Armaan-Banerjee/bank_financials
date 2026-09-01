import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

AR2025 = "https://assets.santandermedia.com/adobe/assets/urn:aaid:aem:3af8ccd7-5ee0-4196-9577-83a30558e64c/original/as/02536CCAA25SantanderFinancialServicesPlc.pdf"
AR2023 = "https://assets.santandermedia.com/adobe/assets/urn:aaid:aem:8da5f087-d631-4188-9c9c-9671410070c5/original/as/sfs_annual_report_2023.pdf"
AR2022 = "https://assets.santandermedia.com/adobe/assets/urn:aaid:aem:f15fea69-5780-484a-bb22-ce42b29eeac3/original/as/santander_financial_services_plc_2022_annual_report.pdf"
AR2021 = "https://assets.santandermedia.com/adobe/assets/urn:aaid:aem:58592004-0ef9-4156-9df8-367908fc81a9/original/as/sfs_2021_annual_report.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Santander Financial Services plc (company 02338548, FRN 146003) is the legal entity covered. "
    "It operates in the UK, Jersey and the Isle of Man and is a subsidiary of Santander UK Group Holdings plc. "
    "The Company's accounts are prepared on an individual-company basis: SFS is exempt from preparing group accounts "
    "under section 400 of the Companies Act 2006. Figures below therefore use SFS standalone/company basis throughout; "
    "Santander UK plc, Santander UK Group Holdings plc and Banco Santander SA figures are not substituted."
)

CASH_SOURCES = (
    "Sources - Santander Financial Services plc own audited Cash Flow Statement, £m:\n"
    f"FY2025 and FY2024: SFS 2025 Annual Report, Cash Flow Statement (printed p.48/49) - {AR2025}\n"
    f"FY2023 and FY2022: SFS 2023 Annual Report, Cash Flow Statement (printed p.49) - {AR2023}\n"
    f"FY2022 and FY2021: SFS 2022 Annual Report, Cash Flow Statement (printed p.48) - {AR2022}\n"
    f"FY2021: SFS 2021 Annual Report, Cash Flow Statement (printed p.48) - {AR2021}\n\n"
    "The 2022 report's 2021 comparative agrees with the 2021 report. The 2023 report's 2022 comparative is used for "
    "the FY2022 column, and the 2025 report's 2024 comparative is used for FY2024. FY2025 accounting-policy change "
    "to IFRS 9 hedge accounting did not impact the statement of financial position or income statement and comparatives "
    "were not restated.\n\n" + ENTITY_NOTE
)

rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {"FY2025": 28, "FY2024": -23, "FY2023": -3, "FY2022": 36, "FY2021": 24}),
    ("SECTION", "Adjustments for non-cash items included in profit", {}),
    ("DATA", "Depreciation and amortisation", {"FY2025": 3, "FY2024": 3, "FY2023": 2, "FY2022": 1, "FY2021": 3}),
    ("DATA", "Provisions for other liabilities and charges", {"FY2025": 3, "FY2023": 2, "FY2022": 2, "FY2021": 2}),
    ("DATA", "Impairment losses", {"FY2024": 17, "FY2023": 1, "FY2022": 1}),
    ("DATA", "Corporation tax credit", {"FY2021": -2}),
    ("DATA", "Other non-cash items", {"FY2025": 2, "FY2024": 1, "FY2023": 3, "FY2022": 1}),
    ("TOTAL", "Non-cash items included in profit", {"FY2025": 8, "FY2024": 21, "FY2023": 8, "FY2022": 5, "FY2021": 3}),
    ("SECTION", "Net change in operating assets and liabilities", {}),
    ("DATA", "Cash and balances at central banks", {"FY2024": 17, "FY2023": 1, "FY2022": -1, "FY2021": 1}),
    ("DATA", "Derivative assets", {"FY2025": 3, "FY2024": -17, "FY2023": 2, "FY2022": 14, "FY2021": 12}),
    ("DATA", "Other financial assets at fair value through profit or loss", {"FY2025": -3, "FY2024": 30, "FY2023": -14, "FY2022": 146, "FY2021": 54}),
    ("DATA", "Loans and advances to banks and customers", {"FY2025": 165, "FY2024": 353, "FY2023": 307, "FY2022": -650, "FY2021": 40}),
    ("DATA", "Other assets", {"FY2024": -1, "FY2023": -2, "FY2022": -2}),
    ("DATA", "Deposits by banks and customers", {"FY2025": -103, "FY2024": 568, "FY2023": -443, "FY2022": 576, "FY2021": -40}),
    ("DATA", "Derivative liabilities", {"FY2025": 10, "FY2024": -56, "FY2023": 12, "FY2022": -181, "FY2021": -71}),
    ("DATA", "Other liabilities", {"FY2025": -21, "FY2024": -3, "FY2023": 16, "FY2022": 3, "FY2021": 1}),
    ("TOTAL", "Net change in operating assets and liabilities", {"FY2025": 51, "FY2024": 891, "FY2023": -121, "FY2022": -95, "FY2021": -3}),
    ("SECTION", "Corporation taxes", {}),
    ("DATA", "Corporation taxes (paid)/received", {"FY2025": -19, "FY2024": 9, "FY2023": -3, "FY2022": 7, "FY2021": -7}),
    ("TOTAL", "Net cash flows from operating activities", {"FY2025": 68, "FY2024": 898, "FY2023": -119, "FY2022": -47, "FY2021": 20}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Investments in other entities", {"FY2022": -3}),
    ("DATA", "Purchase of property, plant and equipment and intangible assets", {"FY2025": -5, "FY2024": -4, "FY2023": -13, "FY2022": -8, "FY2021": -3}),
    ("DATA", "Proceeds from sale of property, plant and equipment and intangible assets", {"FY2025": 1}),
    ("TOTAL", "Net cash flows from investing activities", {"FY2025": -4, "FY2024": -4, "FY2023": -13, "FY2022": -11, "FY2021": -3}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Issue of other equity instruments", {"FY2022": 50}),
    ("DATA", "Dividends paid on ordinary shares", {"FY2025": -12, "FY2024": -2, "FY2023": -4, "FY2022": -65, "FY2021": -8}),
    ("DATA", "Dividends paid on preference shares and other equity instruments", {"FY2025": -5, "FY2024": -4, "FY2023": -5}),
    ("DATA", "Principal elements of lease payments", {"FY2025": -1, "FY2024": -1, "FY2021": -1}),
    ("TOTAL", "Net cash flows from financing activities", {"FY2025": -18, "FY2024": -7, "FY2023": -9, "FY2022": -15, "FY2021": -9}),
    ("TOTAL", "Change in cash and cash equivalents", {"FY2025": 46, "FY2024": 887, "FY2023": -141, "FY2022": -73, "FY2021": 8}),
    ("DATA", "Cash and cash equivalents at beginning of the year", {"FY2025": 3204, "FY2024": 2318, "FY2023": 2460, "FY2022": 2532, "FY2021": 2524}),
    ("DATA", "Effects of exchange rate changes on cash and cash equivalents", {"FY2024": -1, "FY2023": -1, "FY2022": 1, "FY2021": 0}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2025": 3250, "FY2024": 3204, "FY2023": 2318, "FY2022": 2460, "FY2021": 2532}),
    ("SECTION", "Cash and cash equivalents consist of", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 3223, "FY2024": 3186, "FY2023": 2308, "FY2022": 2445, "FY2021": 2355}),
    ("DATA", "Less: restricted balances", {"FY2023": -17, "FY2022": -18, "FY2021": -17}),
    ("DATA", "Other cash equivalents", {"FY2025": 27, "FY2024": 18, "FY2023": 27, "FY2022": 33, "FY2021": 194}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2025": 3250, "FY2024": 3204, "FY2023": 2318, "FY2022": 2460, "FY2021": 2532}),
]

bw = BankWorkbook(bank_name="Santander Financial Services plc", years=YEARS, header_color="EC0000")
bw.add_cash_flow_sheet(
    title="Santander Financial Services plc — Cash Flow Statement",
    subtitle="Standalone company basis, £m. See source note for entity and comparative-column conventions.",
    rows=rows, sources_text=CASH_SOURCES, first_col_width=72, source_height=260, unit_suffix=" (£m)",
)

CAPITAL_SOURCES = (
    "Sources - Santander Financial Services plc own audited regulatory-capital tables in its Annual Reports, £m:\n"
    f"FY2025/FY2024: SFS 2025 Annual Report, Risk review p.39 - {AR2025}\n"
    f"FY2023/FY2022: SFS 2023 Annual Report, Risk review p.39 - {AR2023}\n"
    f"FY2022/FY2021: SFS 2022 Annual Report, Risk review p.39 - {AR2022}\n"
    f"FY2021: SFS 2021 Annual Report, Risk review p.39 - {AR2021}\n\n" + ENTITY_NOTE
)

def metric(name, unit, data, note=None):
    bw.add_metric_sheet(name, unit, data, CAPITAL_SOURCES, note=note, first_col_width=52, source_height=170)

metric("CET1 Capital", "£m", [("CET1 capital", {"FY2025": 249, "FY2024": 266, "FY2023": 288, "FY2022": 256, "FY2021": 293})])
metric("CET1 Ratio", "%", [("CET1 capital ratio", {y: "Not publicly disclosed" for y in YEARS})], "The SFS reports disclose CET1 capital amounts but do not disclose a standalone CET1 percentage or RWA in the reviewed reports. No ratio is inferred from other Santander entities.")
metric("Tier 1 Capital", "£m", [("Tier 1 capital", {"FY2025": 299, "FY2024": 316, "FY2023": 338, "FY2022": 306, "FY2021": 293})])
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", {y: "Not publicly disclosed" for y in YEARS})])
metric("Total Capital", "£m", [("Total regulatory capital", {"FY2025": 299, "FY2024": 316, "FY2023": 338, "FY2022": 306, "FY2021": 293})])
metric("Total Capital Ratio", "%", [("Total capital ratio", {y: "Not publicly disclosed" for y in YEARS})])
metric("Total RWAs", "£m", [("Total risk-weighted assets", {y: "Not publicly disclosed" for y in YEARS})])

UNAVAILABLE = "Not publicly disclosed at SFS standalone level"
bw.add_not_disclosed_metric_sheets(
    ["Leverage Ratio"], CAPITAL_SOURCES,
    per_note={"Leverage Ratio": "The reviewed SFS annual reports do not provide this metric for the SFS standalone/company basis. Santander UK Group Holdings disclosures are a different regulatory entity and were not substituted."},
)

LIQ_SOURCES = (
    "Sources - SFS own liquidity-risk review, £bn for LCR components and percentages for ratios:\n"
    f"FY2025/FY2024: SFS 2025 Annual Report, Risk review p.37 - {AR2025}\n"
    f"FY2023/FY2022: SFS 2023 Annual Report, Risk review p.37 - {AR2023}\n"
    f"FY2022/FY2021: SFS 2022 Annual Report, Risk review p.37 - {AR2022}\n"
    f"FY2021: SFS 2021 Annual Report, Risk review p.37 - {AR2021}\n\n" + ENTITY_NOTE
)
bw.add_metric_sheet("LCR", "£bn / %", [("Eligible liquidity pool", {"FY2025": 3.5, "FY2024": 3.5, "FY2023": 2.6, "FY2022": 2.7, "FY2021": 2.8}), ("Net stress outflows", {"FY2025": -1.5, "FY2024": -1.9, "FY2023": -1.1, "FY2022": -1.3, "FY2021": -1.4}), ("Eligible liquidity pool as percentage of anticipated net cash flows", {"FY2025": "227%", "FY2024": "186%", "FY2023": "240%", "FY2022": "218%", "FY2021": "206%"})], LIQ_SOURCES, note="LCR is presented in the SFS risk review as the eligible liquidity pool divided by anticipated/net stress cash outflows; the underlying table is in £bn and rounded.", first_col_width=58, source_height=180)
bw.add_metric_sheet("NSFR", "%", [("NSFR ratio", {"FY2025": "148%", "FY2024": "149%", "FY2023": "142%", "FY2022": "127%", "FY2021": "137%"})], LIQ_SOURCES, note="NSFR was described by SFS as implemented from 1 January 2022, but the 2021 report nevertheless states the SFS NSFR at 31 December 2021; values are reproduced as reported.", first_col_width=58, source_height=180)
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], CAPITAL_SOURCES,
    per_note={"MREL Ratio": "The reviewed SFS annual reports do not provide this metric for the SFS standalone/company basis. Santander UK Group Holdings disclosures are a different regulatory entity and were not substituted."},
)

bw.add_overview_sheet(
    cash_flow_totals=[("Net cash flows from operating activities", {"FY2025": 68, "FY2024": 898, "FY2023": -119, "FY2022": -47, "FY2021": 20}), ("Net cash flows from investing activities", {"FY2025": -4, "FY2024": -4, "FY2023": -13, "FY2022": -11, "FY2021": -3}), ("Net cash flows from financing activities", {"FY2025": -18, "FY2024": -7, "FY2023": -9, "FY2022": -15, "FY2021": -9}), ("Cash and cash equivalents at end of year", {"FY2025": 3250, "FY2024": 3204, "FY2023": 2318, "FY2022": 2460, "FY2021": 2532})],
    cash_flow_unit="£m", ratios=[("LCR", {"FY2025": "227%", "FY2024": "186%", "FY2023": "240%", "FY2022": "218%", "FY2021": "206%"}), ("NSFR", {"FY2025": "148%", "FY2024": "149%", "FY2023": "142%", "FY2022": "127%", "FY2021": "137%"})],
    note=ENTITY_NOTE + " All unavailable standalone regulatory ratios remain blank/not disclosed on their detail sheets."
)

bw.save("/Users/armaan/code/katalysis/banks/SANTANDER FINANCIAL SERVICES FINANCIALS.xlsx")
