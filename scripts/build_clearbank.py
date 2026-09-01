import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://clear.bank/uploads/assets/ClearBank-Annual-Report-2025.pdf"
AR2023_URL = "https://clear.bank/uploads/assets/ClearBank-Annual-Report-and-Accounts-2023.pdf"
AR2022_URL = "https://clear.bank/uploads/assets/ClearBank-Annual-Report-and-Accounts_2022.pdf"
AR2021_URL = "https://clear.bank/uploads/assets/ClearBank-Annual-Report-2021.pdf"
P3_2025_URL = "https://clear.bank/uploads/assets/ClearBank-Pillar-3-2025.pdf"
P3_2023_URL = "https://clear.bank/uploads/assets/ClearBank-Pillar-3-Disclosure-2023.pdf"
P3_2022_URL = "https://clear.bank/uploads/assets/ClearBank-Pillar-3-2022.pdf"
P3_2021_URL = "https://clear.bank/uploads/assets/ClearBank-Pillar-3-disclosure-2021.pdf"

ENTITY_NOTE = (
    "ClearBank Limited (FRN 754568, company 09736376), a UK clearing/embedded-banking "
    "infrastructure bank. Group basis throughout (parent-only figures are not materially "
    "different - the Group is essentially the Bank plus dormant/minor subsidiaries). Does NOT "
    "take the FRS 101/102 cash-flow-statement exemption - full Consolidated Statement of Cash "
    "Flows every year.\n"
    "FY2022's own figures (from the FY2022 Annual Report itself) are used here rather than "
    "FY2023's report's restated FY2022 comparative (Note 32 of the FY2023 report flags a "
    "restatement, e.g. profit for the year after tax 6,818 as originally reported vs. 10,760 "
    "restated, and net cash from operating activities 413,627 vs. 416,088 restated) - each "
    "year's own originally-published figures are used throughout this workbook, per project "
    "convention.\n"
    "A genuine, small, undocumented cross-vintage gap exists between FY2023's own closing cash "
    "balance (£6,256,126k) and FY2024's own opening balance per the FY2025 Annual Report's "
    "comparative (£6,258,123k) - a ~£1,997k difference with no explanation found in either "
    "source; both figures are shown exactly as each report states them, not force-reconciled.\n"
    "\"Foreign currency differences\" appears twice with different values in the FY2025/FY2024 "
    "presentation - once within the non-cash adjustments (a small figure) and again within the "
    "working-capital-changes section (a much larger figure driven by FX movement on customer "
    "deposit balances) - both are genuine distinct line items in the source, not a duplicate."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are ClearBank Limited's own Consolidated Statement of Cash Flows:\n"
    "FY2025/FY2024: ClearBank Annual Report and Accounts 2025, p.71 - " + AR2025_URL + "\n"
    "FY2023: ClearBank Annual Report and Accounts 2023, p.73 - " + AR2023_URL + "\n"
    "FY2022: ClearBank Annual Report and Accounts 2022, p.43 (own originally-published figures, "
    "not FY2023's restated comparative) - " + AR2022_URL + "\n"
    "FY2021: ClearBank Annual Report and Accounts 2021, p.66 - " + AR2021_URL + "\n\n"
    + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - ClearBank Group Pillar 3 Key Metrics table:\n"
        "FY2025/FY2024: ClearBank Pillar 3 Disclosure 2025, p.15 - " + P3_2025_URL + "\n"
        "FY2023: ClearBank Pillar 3 Disclosure 2023, p.5-6 - " + P3_2023_URL + "\n"
        "FY2022/FY2021: ClearBank Pillar 3 Disclosure 2022, p.4-5 (FY2021 as the FY2022 "
        "document's own comparative column, cross-checked against ClearBank Pillar 3 Disclosure "
        "2021's own Table 1/Table 2 - CET1 140%/£36,739k there vs. 139.70%/£37m here, consistent "
        "to rounding) - " + P3_2022_URL + " and " + P3_2021_URL + "\n"
        "CET1 = Tier 1 = Total Capital every year (no AT1/Tier 2 instruments). MREL not "
        "disclosed anywhere in any Pillar 3 document reviewed, no reason given.\n"
        "LEVERAGE RATIO BASIS NOTE: FY2021's own Pillar 3 document (Table 1) discloses two "
        "different leverage figures with materially different values - a \"CRD leverage ratio\" "
        "of 1% and a \"UK leverage ratio\" of 39%, reflecting genuinely different exposure-measure "
        "definitions, not a typo. The 38.79% figure used here for FY2021 (from the FY2022 "
        "document's comparative, \"excluding claims on central banks\" basis) matches the UK "
        "leverage ratio figure, consistent with the basis used FY2022 onward."
    )


bw = BankWorkbook(bank_name="ClearBank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="E47F85")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) for the year after tax",
     {"FY2025": -15765, "FY2024": -10318, "FY2023": 22396, "FY2022": 6818, "FY2021": -28200}),
    ("DATA", "Depreciation of property, plant and equipment",
     {"FY2025": 63, "FY2024": 68, "FY2023": 510, "FY2022": 304, "FY2021": 475}),
    ("DATA", "(Profit)/loss on disposals of property, plant and equipment",
     {"FY2022": -13, "FY2021": 15}),
    ("DATA", "Depreciation of right-of-use assets",
     {"FY2025": 2202, "FY2024": 1624, "FY2023": 1702, "FY2022": 1030, "FY2021": 1670}),
    ("DATA", "Amortisation of intangible assets",
     {"FY2025": 15706, "FY2024": 11643, "FY2023": 8869, "FY2022": 7824, "FY2021": 5791}),
    ("DATA", "Impairment of intangible assets",
     {"FY2025": 936, "FY2024": 1584, "FY2023": 246, "FY2022": 676, "FY2021": 337}),
    ("DATA", "Share-based payment expense",
     {"FY2025": 1567, "FY2024": 5753, "FY2023": 6729, "FY2022": 7743, "FY2021": 7671}),
    ("DATA", "Recognition of right-of-use assets", {"FY2021": 34}),
    ("DATA", "Tax benefit/(charge)",
     {"FY2025": -945, "FY2024": 74, "FY2023": -3967, "FY2022": -17794, "FY2021": -2874}),
    ("DATA", "Finance costs", {"FY2022": 34, "FY2021": 10}),
    ("DATA", "Net interest income",
     {"FY2025": -70963, "FY2024": -67110, "FY2023": -81914, "FY2022": -33863, "FY2021": -1842}),
    ("DATA", "Other income", {"FY2025": -798, "FY2024": -678, "FY2023": -380}),
    ("DATA", "Foreign currency differences (non-cash items)",
     {"FY2025": 30, "FY2024": 18, "FY2023": 43, "FY2022": 1, "FY2021": -1}),
    ("TOTAL", "Operating cash flows before changes in working capital",
     {"FY2025": -67967, "FY2024": -57342, "FY2023": -45766, "FY2022": -27240, "FY2021": -16914}),
    ("DATA", "Increase/(decrease) in collateral",
     {"FY2025": 859, "FY2024": -16, "FY2023": -919, "FY2022": -27, "FY2021": -36}),
    ("DATA", "(Increase)/decrease in loans and advances to banks",
     {"FY2024": 19525, "FY2023": -10369, "FY2022": -3194, "FY2021": -5962}),
    ("DATA", "Increase in receivables",
     {"FY2025": -6288, "FY2024": -1877, "FY2023": -3547, "FY2022": -1734, "FY2021": -294}),
    ("DATA", "Increase/(decrease) in payables",
     {"FY2025": 6359, "FY2024": 46, "FY2023": -26935, "FY2022": 99410, "FY2021": 3306}),
    ("DATA", "Increase/(decrease) in deferred income",
     {"FY2025": 113, "FY2024": -6167, "FY2023": -16298, "FY2022": -24954, "FY2021": -17307}),
    ("DATA", "Increase in customer deposits/amounts due to customers",
     {"FY2025": 7006677, "FY2024": 4654971, "FY2023": 3152204, "FY2022": 335213, "FY2021": 1718866}),
    ("DATA", "Foreign currency differences (working capital)",
     {"FY2025": 5979, "FY2024": -3846}),
    ("TOTAL", "Cash generated by/from operations",
     {"FY2025": 6945732, "FY2024": 4605294, "FY2023": 3048370, "FY2022": 377474, "FY2021": 1681659}),
    ("DATA", "Interest received",
     {"FY2025": 625779, "FY2024": 425289, "FY2023": 243957, "FY2022": 43774, "FY2021": 2056}),
    ("DATA", "Interest paid",
     {"FY2025": -553258, "FY2024": -341945, "FY2023": -149139, "FY2022": -7621}),
    ("DATA", "Tax (paid)/received", {"FY2025": -1062, "FY2024": 2134, "FY2023": -640}),
    ("TOTAL", "Net cash generated from operating activities",
     {"FY2025": 7017191, "FY2024": 4690772, "FY2023": 3142548, "FY2022": 413627, "FY2021": 1683715}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment",
     {"FY2025": -29, "FY2024": -5, "FY2023": -41, "FY2022": -408, "FY2021": -268}),
    ("DATA", "Purchase of intangible assets",
     {"FY2025": -15655, "FY2024": -24091, "FY2023": -21737, "FY2022": -7736, "FY2021": -8356}),
    ("TOTAL", "Net cash used in investing activities",
     {"FY2025": -15684, "FY2024": -24096, "FY2023": -21778, "FY2022": -8144, "FY2021": -8624}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Proceeds from issue of Ordinary Shares",
     {"FY2024": 35000, "FY2023": 11300, "FY2022": 533, "FY2021": 34500}),
    ("DATA", "Direct costs paid for lease acquisition", {"FY2025": -24}),
    ("DATA", "Principal paid on lease liabilities",
     {"FY2025": -1579, "FY2024": -1567, "FY2023": -1763, "FY2022": -917, "FY2021": -1974}),
    ("DATA", "Interest paid on lease liabilities", {"FY2021": -34}),
    ("TOTAL", "Net cash generated from/(used in) financing activities",
     {"FY2025": -1603, "FY2024": 33433, "FY2023": 9537, "FY2022": -384, "FY2021": 32492}),
    ("TOTAL", "Net increase in cash and cash equivalents",
     {"FY2025": 6999904, "FY2024": 4700109, "FY2023": 3130307, "FY2022": 405099, "FY2021": 1707583}),
    ("DATA", "Cash and cash equivalents at the beginning of the year",
     {"FY2025": 10961293, "FY2024": 6258123, "FY2023": 3125862, "FY2022": 2720797, "FY2021": 1013224}),
    ("DATA", "Effect of foreign exchange rate changes",
     {"FY2025": -4221, "FY2024": 3061, "FY2023": -43, "FY2022": -34, "FY2021": -10}),
    ("TOTAL", "Cash and cash equivalents at the end of the year",
     {"FY2025": 17956976, "FY2024": 10961293, "FY2023": 6256126, "FY2022": 3125862, "FY2021": 2720797}),
]

bw.add_cash_flow_sheet(
    title="ClearBank Limited — Consolidated Cash Flow Statement",
    subtitle="Group basis, £'000. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=44, source_height=190)


CET1_CAPITAL = {"FY2025": 132, "FY2024": 141, "FY2023": 126, "FY2022": 33, "FY2021": 36.7}
CET1_RATIO = {"FY2025": "49.75%", "FY2024": "67.02%", "FY2023": "77.45%", "FY2022": "87.66%", "FY2021": "139.70%"}
RWA = {"FY2025": 266, "FY2024": 211, "FY2023": 163, "FY2022": 38, "FY2021": 26}
LEVERAGE = {"FY2025": "20.05%", "FY2024": "26.07%", "FY2023": "43.51%", "FY2022": "13.87%", "FY2021": "38.79%"}
LCR = {"FY2025": "396.85%", "FY2024": "381.88%", "FY2023": "445.36%", "FY2022": "297.05%", "FY2021": "185.94%"}
NSFR = {"FY2025": "20366.50%", "FY2024": "15959.22%", "FY2023": "10153.88%", "FY2022": "5429.15%", "FY2021": "11701.32%"}

metric("CET1 Capital", "£m", [("Common Equity Tier 1 (CET1) capital", CET1_CAPITAL)])
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 ratio", CET1_RATIO)])
metric("Tier 1 Capital", "£m (= CET1 capital; no AT1 instruments)", [("Tier 1 capital", CET1_CAPITAL)])
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", CET1_RATIO)])
metric("Total Capital", "£m (= CET1 capital; no Tier 2 instruments)", [("Total capital", CET1_CAPITAL)])
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", CET1_RATIO)])
metric("Total RWAs", "£m", [("Total risk-weighted exposure amount", RWA)])
metric("Leverage Ratio", "%",
       [("Leverage ratio excluding claims on central banks", LEVERAGE)],
       note="FY2021 figure is on the \"UK leverage ratio\" basis (39% as originally disclosed in "
            "ClearBank's own FY2021 Pillar 3 document), consistent with the \"excluding claims on "
            "central banks\" basis used FY2022 onward - see the LEVERAGE RATIO BASIS NOTE in this "
            "sheet's source citation for the very different \"CRD leverage ratio\" (1%) also "
            "disclosed for FY2021 on a different exposure-measure definition.")
metric("LCR", "%", [("Liquidity Coverage Ratio", LCR)])
metric("NSFR", "%", [("Net Stable Funding Ratio", NSFR)],
       note="Extreme values (5,000%-20,000%+) are genuine, not a transcription error - ClearBank's "
            "clearing-bank business model holds very large customer deposit balances relative to a "
            "small lending book, so required stable funding is tiny relative to available stable "
            "funding.")

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={"MREL Ratio": "Not publicly disclosed - no MREL ratio or qualitative MREL statement "
                             "found in any Pillar 3 document reviewed (FY2021-FY2025), no reason given."},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from operating activities",
         {"FY2025": 7017191, "FY2024": 4690772, "FY2023": 3142548, "FY2022": 413627, "FY2021": 1683715}),
        ("Net cash used in investing activities",
         {"FY2025": -15684, "FY2024": -24096, "FY2023": -21778, "FY2022": -8144, "FY2021": -8624}),
        ("Net cash from/(used in) financing activities",
         {"FY2025": -1603, "FY2024": 33433, "FY2023": 9537, "FY2022": -384, "FY2021": 32492}),
        ("Cash and cash equivalents at end of year",
         {"FY2025": 17956976, "FY2024": 10961293, "FY2023": 6256126, "FY2022": 3125862, "FY2021": 2720797}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Leverage Ratio", LEVERAGE),
        ("LCR", LCR),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. NSFR omitted from this chart (values in the "
         "thousands of percent would flatten every other series) - see the NSFR sheet directly.",
)

bw.save("/Users/armaan/code/katalysis/banks/CLEARBANK FINANCIALS.xlsx")
