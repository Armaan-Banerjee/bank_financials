import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://redwoodbank.co.uk/media/howpdnen/2025-annual-report-and-accounts_redwood-bank-signed-150426.pdf"
AR2024_URL = "https://redwoodbank.co.uk/media/0h5hp3ku/2024-redwood-bank-annual-report-and-accounts.pdf"
AR2023_URL = "https://redwoodbank.co.uk/media/zrjnifqm/redwood-year-end-annual-report-and-accounts-2023-1.pdf"
CH_URL = "https://find-and-update.company-information.service.gov.uk/company/09872265/filing-history"
CH2022_URL = "https://find-and-update.company-information.service.gov.uk/company/09872265/filing-history/MzM4NjEzNjAwN2FkaXF6a2N4/document?download=0&format=pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Redwood Bank Limited (company 09872265, FRN 755924) is the exact legal entity in the bank list. "
    "It is a UK-authorised bank and a wholly owned subsidiary of Redwood Financial Partners Limited. The annual "
    "reports present the Bank on a Company-only basis; no Group cash-flow statement has been substituted. The "
    "company was previously named Acorn Financial Partners Limited, but the name change occurred before the years "
    "covered and does not create an entity ambiguity."
)

CASH_FLOW_SOURCES = (
    "Sources - Redwood Bank Limited Company-only statement of cash flows, £:\n"
    f"FY2025: Redwood Bank Annual Report and Accounts 2025, p.50 - {AR2025_URL}\n"
    f"FY2024: Redwood Bank Annual Report and Accounts 2024, p.47 - {AR2024_URL}\n"
    f"FY2023: Redwood Bank Annual Report and Accounts 2023, p.59 - {AR2023_URL}\n"
    f"FY2022: Redwood Bank Limited full accounts made up to 31 December 2022 filed at Companies House, p.33 "
    f"(comparative column) - {CH2022_URL}\n"
    f"FY2021: Redwood Bank Limited full accounts made up to 31 December 2022 filed at Companies House, p.33 "
    f"(comparative column for 2021), with the 2021 account used as a cross-check, p.28 - {CH2022_URL}\n\n"
    "The FY2022 and FY2021 columns use later-year comparative columns where available, following the project rule "
    "to inspect comparatives before seeking separate documents. The FY2021 comparative presents a small internal "
    "reclassification of TFSME interest and financing cash: its operating subtotal is £15,466,786 and financing "
    "subtotal £28,300,000, while the standalone 2021 report prints £15,456,792 and £28,309,994. Both produce the "
    "same reported net cash increase of £23,972,927 and the same closing cash of £105,308,945; the later comparative "
    "is used consistently here.\n\n" + ENTITY_NOTE
)

P3_SOURCES = (
    "Sources - Redwood Bank Limited regulatory capital and liquidity KPIs:\n"
    f"FY2025/FY2024: Redwood Bank Annual Report and Accounts 2025, pp.17 and 26, own-funds table p.26 - {AR2025_URL}\n"
    f"FY2024/FY2023: Redwood Bank Annual Report and Accounts 2024, pp.16 and 68 - {AR2024_URL}\n"
    f"FY2023/FY2022: Redwood Bank Annual Report and Accounts 2023, pp.22 and 81, own-funds table pp.81-82 - {AR2023_URL}\n"
    f"FY2021: Redwood Bank Limited full accounts made up to 31 December 2022 filed at Companies House, pp.6 and 60 "
    f"(comparative column), cross-checked against the 2021 accounts pp.6 and 53 - {CH2022_URL}\n\n"
    "Redwood's public reports do not provide separate entity-level numeric disclosures for Total RWAs, leverage "
    "ratio, NSFR, or MREL. Those fields remain explicitly undisclosed rather than being derived from other ratios."
)

bw = BankWorkbook("Redwood Bank Limited", YEARS, YEAR_LABEL, header_color="8B3A3A")

rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit for the year", {"FY2025": 602813, "FY2024": 1828088, "FY2023": 4204249, "FY2022": 1797614, "FY2021": 4084475}),
    ("DATA", "Amortisation of intangibles", {"FY2025": 359914, "FY2024": 336289, "FY2023": 216413, "FY2022": 133808, "FY2021": 85194}),
    ("DATA", "Depreciation of tangible assets", {"FY2025": 91501, "FY2024": 92566, "FY2023": 96581, "FY2022": 104682, "FY2021": 98689}),
    ("DATA", "Write off of fixed/intangible assets", {"FY2021": 0}),
    ("DATA", "Impairment charge on loans and advances to customers", {"FY2025": 756168, "FY2024": 1869546, "FY2023": 2782364, "FY2022": 2496977, "FY2021": 38873}),
    ("DATA", "Net increase in loans to banks", {"FY2025": -1870000}),
    ("DATA", "Net decrease/(increase) in loans to customers", {"FY2025": 1043154, "FY2024": -80130410}),
    ("DATA", "Net increase in customer deposits", {"FY2024": 53028098, "FY2023": 52794173, "FY2022": 9134687, "FY2021": 58428886}),
    ("DATA", "(Decrease)/increase in customer deposits", {"FY2025": -6233049}),
    ("DATA", "Increase in other liabilities", {"FY2024": 749378, "FY2023": 1346720, "FY2022": 1072022, "FY2021": 770530}),
    ("DATA", "(Decrease)/increase in other liabilities", {"FY2025": -1322763}),
    ("DATA", "Increase in other assets", {"FY2024": -194032, "FY2023": -183415, "FY2022": -201534, "FY2021": -112205}),
    ("DATA", "Increase in other assets", {"FY2025": -1390656}),
    ("DATA", "Net increase in loans to customers", {"FY2023": -13393698, "FY2022": -36070258, "FY2021": -45957889}),
    ("DATA", "Increase in accruals and deferred income", {"FY2025": -781191}),
    ("DATA", "Decrease/(increase) in payments and accrued income", {"FY2025": 49647}),
    ("DATA", "Increase in interest payable on TFSME", {"FY2023": 205532, "FY2022": 250709, "FY2021": 9994}),
    ("DATA", "(Decrease)/increase in interest payable on TFSME", {"FY2025": -226182, "FY2024": -241806}),
    ("DATA", "Redemption of TFSME", {"FY2025": -18500000, "FY2024": -19100000}),
    ("DATA", "Net increase in derivatives and hedged items", {"FY2025": -50510, "FY2024": -27459}),
    ("DATA", "Finance cost for subordinated debt", {"FY2025": 585000, "FY2024": 586603, "FY2023": 585000, "FY2022": 585000, "FY2021": 583397}),
    ("DATA", "Fair value change of treasury bills and gilts", {"FY2024": 0, "FY2023": 21961, "FY2022": 32241, "FY2021": -69078}),
    ("DATA", "Income tax", {"FY2025": -111603, "FY2024": 106161, "FY2023": 1332686, "FY2022": 468257, "FY2021": -1910683}),
    ("DATA", "Interest paid for subordinated debt", {"FY2025": -585000, "FY2024": -586603, "FY2023": -585000, "FY2022": -585000, "FY2021": -583397}),
    ("TOTAL", "Net cash from/(used in) operating activities", {"FY2025": -27582757, "FY2024": -41683581, "FY2023": 49423566, "FY2022": -20780795, "FY2021": 15466786}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchases of tangible fixed assets", {"FY2025": -44743, "FY2024": -69653, "FY2023": -104556, "FY2022": -88663, "FY2021": -22261}),
    ("DATA", "Purchases of intangible assets", {"FY2025": -481172, "FY2024": -563604, "FY2023": -551237, "FY2022": -400735, "FY2021": -87059}),
    ("DATA", "Acquisition of treasury bills and gilts", {"FY2024": -5053587, "FY2023": -44402384, "FY2022": -9165232, "FY2021": -19884208}),
    ("DATA", "Acquisition of gilts", {"FY2025": 0}),
    ("DATA", "Proceeds on sale/maturity of treasury bills and gilts", {"FY2025": 4998122, "FY2024": 53536391, "FY2023": 20866125, "FY2022": 9145225, "FY2021": 199669}),
    ("TOTAL", "Net cash generated/(used in) investing activities", {"FY2025": 4472207, "FY2024": 47849547, "FY2023": -24192052, "FY2022": -509405, "FY2021": -19793859}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Proceeds of issue of ordinary shares", {"FY2021": 9900000}),
    ("DATA", "Proceeds of TFSME", {"FY2021": 18400000}),
    ("TOTAL", "Net cash from financing activities", {"FY2021": 28300000}),
    ("TOTAL", "Net cash (decrease)/increase in cash and cash equivalents", {"FY2025": -23110550, "FY2024": 6165966, "FY2023": 25231514, "FY2022": -21290200, "FY2021": 23972927}),
    ("DATA", "Cash and cash equivalents at the beginning of year", {"FY2025": 113293493, "FY2024": 109250259, "FY2023": 84018745, "FY2022": 105308945, "FY2021": 81336018}),
    ("TOTAL", "Cash and cash equivalents at the end of year", {"FY2025": 90182943, "FY2024": 115416225, "FY2023": 109250259, "FY2022": 84018745, "FY2021": 105308945}),
]

bw.add_cash_flow_sheet("Redwood Bank Limited — Cash Flow Statement", "Company-only basis, £. FY2021 uses the later FY2022 comparative column; see source note.", rows, CASH_FLOW_SOURCES, first_col_width=68, source_height=300, unit_suffix=" (£)")

def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, P3_SOURCES, note=note, first_col_width=46, source_height=190)

metric("CET1 Capital", "£", [("Common Equity Tier 1 capital (rounded as reported)", {"FY2025": 48900000, "FY2024": 48400000, "FY2023": 46800000, "FY2022": 41400000, "FY2021": 39400000})], "The annual reports state CET1 capital rounded to £m; these values preserve that stated precision and are not presented as inferred exact amounts.")
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 ratio", {"FY2025": "16.6%", "FY2024": "15.1%", "FY2023": "16.0%", "FY2022": "15.4%", "FY2021": "16.9%"})])
metric("Tier 1 Capital", "£", [("Total Tier 1 capital", {"FY2025": 48846803, "FY2024": 48365248, "FY2023": 46764475, "FY2022": 41430663, "FY2021": 39399478})])
metric("Tier 1 Ratio", None, [("Tier 1 ratio", {y: "Not publicly disclosed" for y in YEARS})], "No separate Tier 1 ratio is stated in the public Redwood reports; it is not derived from CET1 or total-capital ratios.")
metric("Total Capital", "£", [("Total regulatory capital / own funds", {"FY2025": 58505932, "FY2024": 58431891, "FY2023": 56888551, "FY2022": 51320588, "FY2021": 49909754})])
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2025": "19.8%", "FY2024": "18.3%", "FY2023": "19.4%", "FY2022": "19.0%", "FY2021": "21.4%"})])
metric("Total RWAs", None, [("Total risk-weighted assets", {y: "Not publicly disclosed" for y in YEARS})])
metric("Leverage Ratio", None, [("Leverage ratio", {y: "Not publicly disclosed" for y in YEARS})])
metric("LCR", "%", [("Liquidity Coverage Ratio", {"FY2025": "362%", "FY2024": "284%", "FY2023": "481%", "FY2022": "352%", "FY2021": "970%"})])
metric("NSFR", None, [("NSFR", {y: "Not publicly disclosed" for y in YEARS})])
metric("MREL Ratio", None, [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})])

bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": -27582757, "FY2024": -41683581, "FY2023": 49423566, "FY2022": -20780795, "FY2021": 15466786}),
        ("Net cash generated/(used in) investing activities", {"FY2025": 4472207, "FY2024": 47849547, "FY2023": -24192052, "FY2022": -509405, "FY2021": -19793859}),
        ("Net cash from financing activities", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 28300000}),
        ("Cash and cash equivalents at end of year", {"FY2025": 90182943, "FY2024": 115416225, "FY2023": 109250259, "FY2022": 84018745, "FY2021": 105308945}),
    ],
    cash_flow_unit="£",
    ratios=[
        ("CET1 Ratio", {"FY2025": "16.6%", "FY2024": "15.1%", "FY2023": "16.0%", "FY2022": "15.4%", "FY2021": "16.9%"}),
        ("Total Capital Ratio", {"FY2025": "19.8%", "FY2024": "18.3%", "FY2023": "19.4%", "FY2022": "19.0%", "FY2021": "21.4%"}),
        ("LCR", {"FY2025": "362%", "FY2024": "284%", "FY2023": "481%", "FY2022": "352%", "FY2021": "970%"}),
    ],
    note="CET1 capital is rounded to the nearest £m as stated in Redwood's KPI narrative. Undisclosed regulatory metrics remain blank/not publicly disclosed on their detail sheets.",
)

bw.save("/Users/armaan/code/katalysis/banks/REDWOOD BANK FINANCIALS.xlsx")
