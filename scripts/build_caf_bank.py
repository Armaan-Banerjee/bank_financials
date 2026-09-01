import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# CAF Bank Limited (Companies House 01837656, FRN 204451), owned by Charities
# Aid Foundation (CAF), serves charities/non-profits. Fiscal year-end 30 April.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/01837656/filing-history"
AR2025_URL = f"{CH_BASE}/MzUwNDA1NTExOGFkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = f"{CH_BASE}/MzM5MjYwNDE2NmFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = f"{CH_BASE}/MzMxMTMwNTcwNWFkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "ENTITY NOTE: CAF Bank Limited (Companies House 01837656, FRN 204451, formerly Cafcash Limited) is a UK bank "
    "wholly owned by the Charities Aid Foundation (CAF, registered charity 268369), serving charities/non-profits. "
    "It takes no FRS 101/102 cash-flow exemption - full Cash Flow Statement every year. All 3 source Companies "
    "House filings used (FY2025, FY2023-with-FY2022-comparative, FY2021) are fully scanned/image-only (0 text "
    "blocks/page) - every figure was transcribed via high-resolution page-image review, cross-checked against the "
    "following year's comparative column where available. FY2024's own standalone filing was not needed since "
    "FY2025's filing carries it as a comparative; FY2022's standalone filing was likewise not needed since FY2023's "
    "filing carries it as a comparative.\n\n"
    "DATA QUALITY NOTE: the FY2025 column's 'Net cash generated from operating activities' total (£20,729k) and "
    "'Net cash used in investing activities' total (£60,368k) are both independently corroborated - they sum "
    "exactly to the stated 'Change in cash and cash equivalents in the year' (£(39,639)k), and the closing balance "
    "these imply matches the 'Represented by' breakdown exactly. However, one underlying adjustment line "
    "('Amortisation of investments') is genuinely ambiguous in the source scan between the two plausible digit "
    "readings £(6,041)k and £(8,041)k - only the former makes the itemised adjustments sum exactly to the stated "
    "operating total, so £(6,041)k is used here as the internally-consistent figure (the same approach used "
    "elsewhere in this project for LHV/Zempler/Vanquis source-document ambiguities). The FY2024 comparative "
    "column's own itemised lines sum exactly to its own stated totals with no ambiguity.\n\n"
    "No Pillar 3 disclosure, standalone or embedded, was found anywhere for this entity: the Annual Report itself "
    "(Strategic Report, Risk management report, and all Notes to the Financial Statements) contains no CET1/"
    "Tier 1/Total Capital £ figures, no Total RWAs, no Leverage Ratio, no LCR/NSFR, and no MREL Ratio in any of "
    "the 5 years reviewed - only a passing reference to 'ICAAP and liquidity adequacy assessments' as a governance "
    "activity, with no figures given. No standalone Pillar 3 document exists on CAF Bank's own site or CAF's "
    "wider governance/regulatory-disclosures pages. All 11 Pillar 3 metrics are therefore 'Not publicly "
    "disclosed', consistent with a small, non-complex institution under simplified UK prudential disclosure rules."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are CAF Bank Limited's own Cash Flow Statement, transcribed from each year's own "
    "Companies House filing (or, for FY2024/FY2022, that year's own comparative column in the following year's "
    "filing):\n"
    f"FY2025/FY2024: Full accounts made up to 30 April 2025 (filed 10 Feb 2026), Cash Flow Statement - {AR2025_URL}\n"
    f"FY2023/FY2022: Full accounts made up to 30 April 2023 (filed 14 Sep 2023), Cash Flow Statement - {AR2023_URL}\n"
    f"FY2021: Full accounts made up to 30 April 2021 (filed 31 Aug 2021), Cash Flow Statement - {AR2021_URL}\n"
    + ENTITY_NOTE
)

bw = BankWorkbook(bank_name="CAF Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="2E7D32")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit on ordinary activities", {"FY2025": 14661, "FY2024": 18169, "FY2023": 8575, "FY2022": 1640, "FY2021": 929}),
    ("DATA", "Amortisation of investments", {"FY2025": -6041, "FY2024": -2450, "FY2023": 344, "FY2022": 1170, "FY2021": 21919}),
    ("DATA", "Corporation tax paid", {"FY2025": -1705, "FY2024": -5815, "FY2023": -830, "FY2021": None}),
    ("DATA", "(Increase)/decrease in prepayments and accrued income", {"FY2025": -1316, "FY2024": -1791, "FY2023": -4982, "FY2022": 275, "FY2021": 311}),
    ("DATA", "(Decrease)/increase in accruals and deferred income", {"FY2021": -98}),
    ("DATA", "Increase/(decrease) in Cash Ratio Deposit with the Bank of England", {"FY2024": 3582, "FY2023": -369, "FY2022": -918, "FY2021": -828}),
    ("DATA", "Decrease in loans and advances to banks", {"FY2021": 0}),
    ("DATA", "(Increase) in loans and advances to customers", {"FY2025": -21216, "FY2024": -20683, "FY2023": -17900, "FY2022": -34801, "FY2021": -21414}),
    ("DATA", "Increase/(decrease) in loan loss provision", {"FY2025": -184, "FY2024": 716, "FY2023": 573, "FY2022": -1100, "FY2021": 533}),
    ("DATA", "Increase/(decrease) in customer accounts", {"FY2025": 31493, "FY2024": -85992, "FY2023": -3512, "FY2022": 110791, "FY2021": 241151}),
    ("DATA", "Increase in other liabilities", {"FY2025": 5037, "FY2024": 3028, "FY2023": 2435, "FY2022": 2317, "FY2021": -2052}),
    ("TOTAL", "Net cash generated from/(used in) operating activities", {"FY2025": 20729, "FY2024": -91236, "FY2023": -15666, "FY2022": 79374, "FY2021": 240451}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Acquisitions of debt securities", {"FY2025": -156964, "FY2024": -254111, "FY2023": -88130, "FY2022": -228836, "FY2021": -293668}),
    ("DATA", "Redemptions of debt securities", {"FY2025": 115598, "FY2024": 371286, "FY2023": 112831, "FY2022": 336397, "FY2021": 156956}),
    ("DATA", "Disposals of debt securities", {"FY2021": 0}),
    ("DATA", "Net proceeds/(repayments) from repurchase agreements", {"FY2025": -13852, "FY2024": 5000, "FY2023": 8852, "FY2021": -10142}),
    ("DATA", "Acquisition of intangible assets", {"FY2025": -5150, "FY2024": -4425, "FY2023": -1657, "FY2022": -3482, "FY2021": -1194}),
    ("DATA", "Proceeds from subordinated debt", {"FY2024": 15000}),
    ("DATA", "Repayment of subordinated debt", {"FY2024": -10000}),
    ("TOTAL", "Net cash generated from/(used in) investing activities", {"FY2025": -60368, "FY2024": 122750, "FY2023": 31896, "FY2022": 104079, "FY2021": -148048}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Costs of redemption of additional tier 1 securities and exchange for ordinary share capital", {"FY2023": -31}),
    ("DATA", "Charitable donations paid", {"FY2021": -297}),
    ("DATA", "AT1 dividend paid", {"FY2021": -1126}),
    ("TOTAL", "Net cash used in financing activities", {"FY2025": 0, "FY2024": 0, "FY2023": -31, "FY2022": 0, "FY2021": -1423}),
    ("TOTAL", "Change in cash and cash equivalents in the year", {"FY2025": -39639, "FY2024": 31514, "FY2023": 16199, "FY2022": 183453, "FY2021": 90980}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 654524, "FY2024": 623010, "FY2023": 606811, "FY2022": 423358, "FY2021": 332378}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 614885, "FY2024": 654524, "FY2023": 623010, "FY2022": 606811, "FY2021": 423358}),
    ("SECTION", "Represented by:", {}),
    ("DATA", "Balances at Bank of England repayable on demand", {"FY2025": 610671, "FY2024": 630526, "FY2023": 616894, "FY2022": 599340, "FY2021": 415461}),
    ("DATA", "Loans and advances to banks repayable on demand", {"FY2025": 4214, "FY2024": 23998, "FY2023": 6116, "FY2022": 7471, "FY2021": 7897}),
]

bw.add_cash_flow_sheet(
    title="CAF Bank Limited — Cash Flow Statement",
    subtitle="CAF Bank Limited's own basis, £'000. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=88,
    source_height=320,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets — nothing publicly disclosed for this entity
# ---------------------------------------------------------------
NOT_DISCLOSED_NOTE = (
    "Not publicly disclosed by CAF Bank Limited in any year reviewed (FY2021-FY2025) - checked the Annual "
    "Report's Strategic Report, Risk management report, and full Notes to the Financial Statements, plus CAF "
    "Bank's own site and CAF's wider governance/regulatory-disclosures pages. No standalone Pillar 3 document "
    "exists; see ENTITY_NOTE on the Cash Flow Statement sheet."
)

bw.add_not_disclosed_metric_sheets(
    ["CET1 Capital", "CET1 Ratio", "Tier 1 Capital", "Tier 1 Ratio", "Total Capital", "Total Capital Ratio",
     "Total RWAs", "Leverage Ratio", "LCR", "NSFR", "MREL Ratio"],
    CASH_FLOW_SOURCES,
    per_note={m: NOT_DISCLOSED_NOTE for m in
              ["CET1 Capital", "CET1 Ratio", "Tier 1 Capital", "Tier 1 Ratio", "Total Capital", "Total Capital Ratio",
               "Total RWAs", "Leverage Ratio", "LCR", "NSFR", "MREL Ratio"]},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash generated from/(used in) operating activities", {"FY2025": 20729, "FY2024": -91236, "FY2023": -15666, "FY2022": 79374, "FY2021": 240451}),
        ("Net cash generated from/(used in) investing activities", {"FY2025": -60368, "FY2024": 122750, "FY2023": 31896, "FY2022": 104079, "FY2021": -148048}),
        ("Net cash used in financing activities", {"FY2025": 0, "FY2024": 0, "FY2023": -31, "FY2022": 0, "FY2021": -1423}),
        ("Cash and cash equivalents at end of year", {"FY2025": 614885, "FY2024": 654524, "FY2023": 623010, "FY2022": 606811, "FY2021": 423358}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {}),
        ("Tier 1 Ratio", {}),
        ("Total Capital Ratio", {}),
        ("Leverage Ratio", {}),
        ("LCR", {}),
        ("NSFR", {}),
    ],
    note="Full 5-year cash flow statement (FY2021-FY2025), no FRS 101/102 exemption. No Pillar 3 disclosure of "
         "any kind (CET1/Tier 1/Total Capital, RWAs, Leverage Ratio, LCR, NSFR, MREL) is published by this "
         "entity in any year - all 11 metric sheets are 'Not publicly disclosed'; see ENTITY_NOTE on the Cash "
         "Flow Statement sheet.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/CAF BANK FINANCIALS.xlsx")
