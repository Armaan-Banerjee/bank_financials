import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2026", "FY2025", "FY2024", "FY2023", "FY2022"]
AR26_URL = "https://recognisebank.co.uk/wp-content/uploads/274107-Recognise-Bank-Annual-Report-WEB.pdf"
AR24_URL = "https://recognisebank.co.uk/wp-content/uploads/2024-Annual-Report-Accounts.pdf"
AR23_URL = "https://recognisebank.co.uk/wp-content/uploads/2023/10/230821-Recognise-Bank-2023-Annual-Report-WEB.pdf"
AR22_URL = "https://recognisebank.co.uk/wp-content/uploads/2023/10/2022-Annual-Report-Recognise-Bank-Limited.pdf"
P3_26_URL = "https://recognisebank.co.uk/wp-content/uploads/Pillar-3-disclosure-March-2026-RBL-v1.1-To-BAC-updated_-1-1.pdf"

ENTITY_NOTE = (
    "ENTITY/BASIS NOTE: Recognise Bank Limited (Companies House 10603119; FRN 849404; LEI "
    "213800ZFTXJC7RV9UQ92) is the matched authorised bank entity. Cash flows are presented on "
    "the Company/standalone basis in £'000 throughout. The 2022-2024 reports also show Group "
    "columns, but the Company column is used consistently here. Recognise's sole remaining "
    "subsidiary, Credit Asset Management Limited (CAML), entered members' voluntary liquidation "
    "on 24 March 2025; the 2025 accounts therefore were not consolidated, and the 2026 report is "
    "standalone. FY2025 is taken from the clean comparative in the 2026 report because the bank's "
    "published 2025 PDF has an extraction/encoding problem; no figure is inferred. Blank cells "
    "mean not publicly disclosed, not zero."
)
CASH_SOURCES = (
    "Sources - Recognise Bank Limited Company/standalone cash flows, £'000:\n"
    f"FY2026 & FY2025: Annual Report 2026, printed p.52 - {AR26_URL}\n"
    f"FY2024 & FY2023: Annual Report 2024, printed p.46 (Company statement) - {AR24_URL}\n"
    f"FY2023 & FY2022: Annual Report 2023, printed p.42 (Company statement) - {AR23_URL}\n"
    f"FY2022 & FY2021 comparative: Annual Report 2022, printed p.44 (Company statement) - {AR22_URL}\n\n"
    + ENTITY_NOTE
)
P3_SOURCES = (
    f"Source - Recognise Bank Limited Pillar 3 Disclosure 2026, Table 1 UK KM1, printed p.3 "
    f"(Mar-26 through Mar-22 comparatives) - {P3_26_URL}\n"
    "The 2026 KM1 table supplies all five requested year-ends on a bank/entity basis."
)

bw = BankWorkbook(bank_name="Recognise Bank Limited", years=YEARS, header_color="51158C")
rows = [
    ("SECTION", "Cash flow from operating activities", {}),
    ("DATA", "Profit/(loss) for the year", {"FY2026": 8856, "FY2025": -5332, "FY2024": -9259, "FY2023": -12783, "FY2022": -12444}),
    ("DATA", "Depreciation and amortisation", {"FY2026": 559, "FY2025": 699, "FY2024": 635, "FY2023": 789, "FY2022": 305}),
    ("DATA", "Intangible assets impairment", {"FY2026": 928}),
    ("DATA", "Recognition of deferred tax asset", {"FY2026": -7060}),
    ("DATA", "Interest earned during the year", {"FY2026": -42754, "FY2025": -36294, "FY2024": -25487, "FY2023": -9112, "FY2022": -2136}),
    ("DATA", "Interest expense during the year", {"FY2026": 22398, "FY2025": 20832, "FY2024": 13153, "FY2023": 2970, "FY2022": 803}),
    ("DATA", "Interest expense on leases", {"FY2026": 5, "FY2025": 10, "FY2024": 22, "FY2023": 29}),
    ("DATA", "Impairment (gain)/loss", {"FY2026": -46, "FY2025": 2311, "FY2024": 3339, "FY2023": 76, "FY2022": 148}),
    ("DATA", "Share-based incentive plan", {"FY2022": 171}),
    ("DATA", "Dividend income from CAML", {"FY2025": -400, "FY2024": 0, "FY2023": -468}),
    ("DATA", "Other income", {"FY2026": -431}),
    ("DATA", "Interest received", {"FY2026": 41682, "FY2025": 36170, "FY2024": 24429, "FY2023": 9210, "FY2022": 3608}),
    ("DATA", "Interest paid", {"FY2026": -11971, "FY2025": -11997, "FY2024": -4824, "FY2023": -2245, "FY2022": -457}),
    ("DATA", "Increase in debt securities", {"FY2026": -19928, "FY2025": -9656}),
    ("DATA", "Decrease/(increase) in debt securities", {"FY2022": 6500}),
    ("DATA", "Increase in loans and advances", {"FY2026": -155239, "FY2025": -5307, "FY2024": -183505, "FY2023": -22804, "FY2022": -93780}),
    ("DATA", "Increase in deposits from customers", {"FY2026": 80807, "FY2025": 63808, "FY2024": 203087, "FY2023": 104533, "FY2022": 94646}),
    ("DATA", "Increase/(decrease) in other assets", {"FY2026": -271, "FY2025": -78, "FY2024": -77, "FY2023": -248, "FY2022": -276}),
    ("DATA", "Increase/(decrease) in other liabilities", {"FY2026": 368, "FY2025": -60, "FY2024": -22, "FY2023": 745, "FY2022": 492}),
    ("TOTAL", "Net cash (used in)/generated from operating activities", {"FY2026": -82097, "FY2025": 54706, "FY2024": 21491, "FY2023": 70692, "FY2022": -2420}),
    ("SECTION", "Cash flow from investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2026": -90, "FY2025": -7, "FY2024": -52, "FY2023": -259, "FY2022": -53}),
    ("DATA", "Disposal of property, plant and equipment", {"FY2022": 1}),
    ("DATA", "Distribution/dividend received from CAML", {"FY2026": 11, "FY2025": 60}),
    ("DATA", "Surplus funds sent from CAML", {"FY2025": 280, "FY2024": 800, "FY2023": 1000}),
    ("DATA", "Loans repaid by group companies", {"FY2022": 5017}),
    ("DATA", "Loans advanced to group companies", {"FY2022": -271}),
    ("DATA", "Purchase of intangible assets", {"FY2026": -562, "FY2025": -402, "FY2024": -1054, "FY2023": -571, "FY2022": -156}),
    ("TOTAL", "Net cash (used in)/generated from investing activities", {"FY2026": -641, "FY2025": -69, "FY2024": -306, "FY2023": 170, "FY2022": 4538}),
    ("SECTION", "Cash flow from financing activities", {}),
    ("DATA", "Interest paid on customer deposits", {"FY2022": 6}),
    ("DATA", "Finance lease payments", {"FY2026": -45, "FY2025": -198, "FY2024": -247, "FY2023": -225, "FY2022": -66}),
    ("DATA", "Gross proceeds from the issue of ordinary shares", {"FY2026": 5000, "FY2025": 20001, "FY2024": 5000, "FY2023": 31504, "FY2022": 22950}),
    ("DATA", "Costs of share issue", {"FY2023": -20}),
    ("TOTAL", "Net cash generated from financing activities", {"FY2026": 4955, "FY2025": 19803, "FY2024": 4753, "FY2023": 31259, "FY2022": 22890}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2026": -77783, "FY2025": 74440, "FY2024": 25938, "FY2023": 102121, "FY2022": 25008}),
    ("DATA", "Cash and cash equivalents brought forward", {"FY2026": 238732, "FY2025": 164292, "FY2024": 138354, "FY2023": 36233, "FY2022": 11225}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2026": 160949, "FY2025": 238732, "FY2024": 164292, "FY2023": 138354, "FY2022": 36233}),
]
bw.add_cash_flow_sheet(title="Recognise Bank Limited - Company Cash Flow Statement", subtitle="Company/standalone basis, £'000; FY2022-FY2026 (31 March year-end).", rows=rows, sources_text=CASH_SOURCES, first_col_width=66, source_height=230, unit_suffix=" (£'000)")

def metric(name, unit, data, note=None):
    bw.add_metric_sheet(name, unit, data, P3_SOURCES, note=note, first_col_width=54, source_height=130)

km1 = {
    "FY2026": (74617, 356376, "20.9%", 509006, "14.7%", 220955, 82309, 8630, 73679, "299.9%", 520393, 295089, "176.4%"),
    "FY2025": (66988, 220421, "30.4%", 329206, "20.3%", 212180, 44148, 5456, 38692, "548.4%", 480437, 211608, "227.0%"),
    "FY2024": (52617, 200213, "26.3%", 316246, "16.6%", 149255, 39271, 10380, 28891, "516.6%", 440424, 213351, "206.4%"),
    "FY2023": (57482, 88249, "65.1%", 134402, "42.8%", 71930, 18358, 9363, 8996, "799.6%", 247010, 93289, "264.8%"),
    "FY2022": (37411, 87216, "42.9%", 109158, "34.3%", 20648, 13379, 8079, 5300, "389.6%", 128630, 78103, "164.7%"),
}
def col(i): return {y: km1[y][i] for y in YEARS}
metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", col(0))])
metric("CET1 Ratio", "%", [("Common Equity Tier 1 (CET1) ratio", col(2))])
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", col(0))])
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", col(2))])
metric("Total Capital", "£'000", [("Total capital", col(0))])
metric("Total Capital Ratio", "%", [("Total capital ratio", col(2))])
metric("Total RWAs", "£'000", [("Total risk-weighted exposure amount", col(1))])
metric("Leverage Ratio", "£'000 / %", [("Total exposure measure excluding claims on central banks", col(3)), ("Leverage ratio excluding claims on central banks", col(4))])
metric("LCR", "£'000 / %", [("Total high-quality liquid assets (HQLA), weighted value - average", col(5)), ("Cash outflows - total weighted value", col(6)), ("Cash inflows - total weighted value", col(7)), ("Total net cash outflows (adjusted value)", col(8)), ("Liquidity coverage ratio", col(9))])
metric("NSFR", "£'000 / %", [("Total available stable funding", col(10)), ("Total required stable funding", col(11)), ("NSFR ratio", col(12))])
metric("MREL Ratio", None, [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})], "No quantitative MREL ratio was located in the official Recognise Bank annual reports or Pillar 3 disclosures reviewed.")

def row_values(label):
    return next(values for kind, name, values in rows if name == label)
bw.add_overview_sheet(
    cash_flow_totals=[(label, row_values(label)) for label in ["Net cash (used in)/generated from operating activities", "Net cash (used in)/generated from investing activities", "Net cash generated from financing activities", "Cash and cash equivalents at end of year"]],
    cash_flow_unit="£'000",
    ratios=[("CET1 Ratio", col(2)), ("Total Capital Ratio", col(2)), ("Leverage Ratio", col(4)), ("LCR", col(9)), ("NSFR", col(12))],
    note="Cash flows are Company/standalone figures. Pillar 3 metrics are Recognise Bank Limited UK KM1 figures. FY2025 accounts were not consolidated after CAML entered liquidation; the 2026 report supplies the FY2025 comparative. Blank cells mean not disclosed, not zero.",
)
bw.save("/Users/armaan/code/katalysis/banks/RECOGNISE BANK FINANCIALS.xlsx")
