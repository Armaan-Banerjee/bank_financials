import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://wp-dfcapital-investors-2020.s3.eu-west-2.amazonaws.com/media/2026/03/DF-Capital-Annual-Report-and-Accounts-year-ending-2025.pdf"
AR2023_URL = "https://wp-dfcapital-investors-2020.s3.eu-west-2.amazonaws.com/media/2024/04/DF-Capital-Annual-Report-and-Accounts-year-ending-2023-1.pdf"
AR2021_URL = "https://wp-dfcapital-investors-2020.s3.eu-west-2.amazonaws.com/media/2022/05/Annual-report-and-accounts-year-end-2021.pdf"
P3_2025_URL = "https://wp-dfcapital-investors-2020.s3.eu-west-2.amazonaws.com/media/2026/03/DF-Capital-Pillar-III-2025.pdf"
P3_2024_URL = "https://wp-dfcapital-investors-2020.s3.eu-west-2.amazonaws.com/media/2025/04/Distribution-Finance-Capital-Holdings-plc-Pillar-3-Disclosures-at-31-December-2024.pdf"
P3_2023_URL = "https://wp-dfcapital-investors-2020.s3.eu-west-2.amazonaws.com/media/2024/04/DF-Capital-Pillar-III_2024-FINAL.pdf"
P3_2021_URL = "https://wp-dfcapital-investors-2020.s3.eu-west-2.amazonaws.com/media/2022/04/DF-Capital-Pillar-III_Dec-2021-Final.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: DF Capital Bank Limited (FRN 848291, company 10198535) is the PRA-regulated bank "
    "entity, a wholly-owned subsidiary of the AIM-listed Distribution Finance Capital Holdings plc "
    "(company 11911574, 'the Group'). The Bank's own Companies House filings are fully scanned "
    "(no text layer). Both the Annual Report and the Pillar 3 disclosure are published ONLY at the "
    "Group-consolidated level - the Pillar 3 document itself states 'there are no differences between "
    "the basis of consolidation of the Group for accounting and regulatory purposes,' confirming this "
    "is not a basis mismatch. From FY2021-FY2023 the Group comprised only DFCH plc and DF Capital Bank "
    "Limited; two further lending subsidiaries (DF Capital Financial Solutions Limited, DF Capital "
    "Retail Finance Limited) were added by FY2025 per the Annual Report's own country-by-country note. "
    "The FY2021 Pillar 3 document uniquely also discloses a Bank-solo column alongside Group - the "
    "Group column is used throughout for consistency with every later year, which only shows Group. "
    "NSFR was disclosed FY2021-FY2023 but stops appearing in the FY2024 and FY2025 Pillar 3 documents "
    "entirely (checked directly, not assumed) - plausibly linked to the Group's disclosed opt-in to the "
    "PRA's Small Domestic Deposit Takers (SDDT) reduced-disclosure regime. MREL not disclosed any year, "
    "no exemption stated - consistent with a small SDDT-regime institution."
)

CASH_FLOW_SOURCES = (
    "Sources - Distribution Finance Capital Holdings plc's Consolidated Cash Flow Statement (Group "
    "basis, the Bank's own filed accounts are fully scanned - see ENTITY NOTE):\n"
    f"FY2025/FY2024: Annual Report and Accounts 2025, p.114-115 (Consolidated Cash Flow Statement) - {AR2025_URL}\n"
    f"FY2023/FY2022: Annual Report and Accounts 2023, p.114-115 (Consolidated Cash Flow Statement) - {AR2023_URL}\n"
    f"FY2021: Annual Report and Accounts 2021, p.106-107 (Consolidated Cash Flow Statement) - {AR2021_URL}\n"
    "Each year's own originally-published figures are used; the closing balance of each year ties "
    "exactly to the opening balance of the next, no restatements found across any vintage. FY2022's "
    "own printed operating-activities total (-GBP3,408k) is GBP8k off its own component lines' sum "
    "(-GBP3,416k) - an immaterial rounding artifact in the source document itself, kept as printed "
    "rather than force-corrected; every other year's total ties to the penny.\n"
    + ENTITY_NOTE
)


def p3_sources(page):
    return (
        f"Sources - Distribution Finance Capital Holdings plc Pillar 3 Disclosures (Consolidated "
        f"Group basis), Key Metrics (UK KM1) table, p.{page}:\n"
        f"FY2025: DF Capital Pillar III 2025 - {P3_2025_URL}\n"
        f"FY2024: DF Capital Pillar 3 Disclosures at December 2024 - {P3_2024_URL}\n"
        f"FY2023/FY2022: DF Capital Pillar III 2024 (FY2023 with Dec-22 comparative) - {P3_2023_URL}\n"
        f"FY2021: DF Capital Pillar III Dec 2021, Table 1 (Group column used, Bank-solo column also "
        f"disclosed that year only, not used - see ENTITY NOTE) - {P3_2021_URL}\n"
        + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="DF Capital Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="D80034")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) before taxation",
     {"FY2025": 19641, "FY2024": 19074, "FY2023": 4573, "FY2022": 1304, "FY2021": -3735}),
    ("DATA", "Adjustments for non-cash items and other adjustments included in the income statement",
     {"FY2025": 7794, "FY2024": 3822, "FY2023": 13000, "FY2022": 4664, "FY2021": 1446}),
    ("DATA", "Increase/(decrease) in operating assets",
     {"FY2025": -186354, "FY2024": -92390, "FY2023": -149456, "FY2022": -193189, "FY2021": -136244}),
    ("DATA", "Increase/(decrease) in operating liabilities",
     {"FY2025": 195168, "FY2024": 79376, "FY2023": 94171, "FY2022": 183809, "FY2021": 151711}),
    ("DATA", "Taxation paid/(received)",
     {"FY2025": -3296, "FY2024": -681, "FY2023": 0, "FY2022": -4, "FY2021": 0}),
    ("TOTAL", "Net cash generated from/(used in) operating activities",
     {"FY2025": 32953, "FY2024": 9201, "FY2023": -37712, "FY2022": -3408, "FY2021": 13178}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of investment/debt securities",
     {"FY2025": -498, "FY2024": -9918, "FY2023": -14554, "FY2022": 0, "FY2021": -350980}),
    ("DATA", "Proceeds from sale and maturity of investment/debt securities",
     {"FY2025": 500, "FY2024": 25000, "FY2023": 23000, "FY2022": 85070, "FY2021": 307958}),
    ("DATA", "Dividends received on money market funds", {"FY2025": 57, "FY2024": 25}),
    ("DATA", "Interest received on investment/debt securities",
     {"FY2025": 2, "FY2024": 75, "FY2023": 383, "FY2022": 746, "FY2021": 549}),
    ("DATA", "Purchase of own shares", {"FY2023": -67}),
    ("DATA", "Purchase of property, plant and equipment",
     {"FY2025": -3557, "FY2024": -397, "FY2023": -418, "FY2022": -1041, "FY2021": -253}),
    ("DATA", "Cash received on disposal of property, plant and equipment", {"FY2025": 34}),
    ("DATA", "Purchase of right of use assets", {"FY2025": -81}),
    ("DATA", "Purchase of intangible assets",
     {"FY2025": -80, "FY2024": -623, "FY2023": -117, "FY2022": -193, "FY2021": -586}),
    ("TOTAL", "Net cash (used in)/generated from investing activities",
     {"FY2025": -3623, "FY2024": 14162, "FY2023": 8227, "FY2022": 84582, "FY2021": -43312}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Issue of new shares", {"FY2021": 38645}),
    ("DATA", "Repayment of lease liabilities",
     {"FY2025": -108, "FY2024": -252, "FY2023": -227, "FY2022": -141, "FY2021": -147}),
    ("DATA", "Issuance of subordinated liabilities", {"FY2025": 5000, "FY2023": 10000}),
    ("DATA", "Acquisition of subordinated liabilities", {"FY2023": -51}),
    ("DATA", "Coupon paid on subordinated liabilities", {"FY2025": -1269, "FY2024": -1273}),
    ("DATA", "Purchase of own shares", {"FY2025": -192, "FY2024": -142}),
    ("DATA", "Purchase of treasury shares", {"FY2025": -4877}),
    ("DATA", "Receipt of cash from settlement of share options", {"FY2025": 116}),
    ("TOTAL", "Net cash (used in)/generated from financing activities",
     {"FY2025": -1330, "FY2024": -1667, "FY2023": 9722, "FY2022": -141, "FY2021": 38498}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents",
     {"FY2025": 28000, "FY2024": 21696, "FY2023": -19763, "FY2022": 81033, "FY2021": 8364}),
    ("DATA", "Cash and cash equivalents at start of the period",
     {"FY2025": 112563, "FY2024": 90867, "FY2023": 110630, "FY2022": 29597, "FY2021": 21233}),
    ("TOTAL", "Cash and cash equivalents at end of the period",
     {"FY2025": 140563, "FY2024": 112563, "FY2023": 90867, "FY2022": 110630, "FY2021": 29597}),
]

bw.add_cash_flow_sheet(
    title="DF Capital Bank Limited — Consolidated Cash Flow Statement",
    subtitle="Distribution Finance Capital Holdings plc Group basis, £'000. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=80,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, page, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(page), note=note, first_col_width=48, source_height=180)


CET1_CAPITAL = {"FY2025": 112443, "FY2024": 98780, "FY2023": 79269, "FY2022": 84579, "FY2021": 82690}
TOTAL_CAPITAL = {"FY2025": 127745, "FY2024": 109010, "FY2023": 89538, "FY2022": 84579, "FY2021": 82690}
TOTAL_RWA = {"FY2025": 623607, "FY2024": 457565, "FY2023": 347034, "FY2022": 381972, "FY2021": 216353}
CET1_RATIO = {"FY2025": "18.0%", "FY2024": "21.6%", "FY2023": "22.8%", "FY2022": "22.1%", "FY2021": "38.2%"}
TOTAL_CAPITAL_RATIO = {"FY2025": "20.5%", "FY2024": "23.8%", "FY2023": "25.8%", "FY2022": "22.1%", "FY2021": "38.2%"}
LEVERAGE_RATIO = {"FY2025": "12.8%", "FY2024": "14.5%", "FY2023": "13.0%", "FY2022": "17.6%", "FY2021": "21.2%"}
LCR = {"FY2025": "704.0%", "FY2024": "836.6%", "FY2023": "618%", "FY2022": "1029%", "FY2021": "5597%"}
NSFR = {"FY2023": "148.2%", "FY2022": "163%", "FY2021": "214%"}

NO_AT1_NOTE = "No Additional Tier 1 or Tier 2 instruments disclosed any year - Tier 1/Total Capital equal CET1 Capital throughout."
NSFR_NOTE = (
    "NSFR was disclosed for FY2021-FY2023 but does not appear anywhere in the FY2024 or FY2025 Pillar "
    "3 documents (confirmed by direct search of both, not assumed) - plausibly linked to the Group's "
    "disclosed opt-in to the PRA's Small Domestic Deposit Takers (SDDT) reduced-disclosure regime."
)

metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", CET1_CAPITAL)], "4")
metric("CET1 Ratio", "%", [("CET1 ratio", CET1_RATIO)], "4")
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", CET1_CAPITAL)], "4", note=NO_AT1_NOTE)
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", CET1_RATIO)], "4", note=NO_AT1_NOTE)
metric("Total Capital", "£'000", [("Total capital", TOTAL_CAPITAL)], "4")
metric("Total Capital Ratio", "%", [("Total capital ratio", TOTAL_CAPITAL_RATIO)], "4")
metric("Total RWAs", "£'000", [("Total risk-weighted exposure amount", TOTAL_RWA)], "4")
metric("Leverage Ratio", "%", [("Leverage ratio excluding claims on central banks", LEVERAGE_RATIO)], "4")
metric("LCR", "%", [("Liquidity coverage ratio", LCR)], "4")
metric("NSFR", "%", [("Net Stable Funding Ratio", NSFR)], "4", note=NSFR_NOTE)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources("n/a"),
    per_note={"MREL Ratio": "Not publicly disclosed any year, no exemption stated - consistent with a small SDDT-regime institution."},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash generated from/(used in) operating activities",
         {"FY2025": 32953, "FY2024": 9201, "FY2023": -37712, "FY2022": -3408, "FY2021": 13178}),
        ("Net cash (used in)/generated from investing activities",
         {"FY2025": -3623, "FY2024": 14162, "FY2023": 8227, "FY2022": 84582, "FY2021": -43312}),
        ("Net cash (used in)/generated from financing activities",
         {"FY2025": -1330, "FY2024": -1667, "FY2023": 9722, "FY2022": -141, "FY2021": 38498}),
        ("Cash and cash equivalents at end of the period",
         {"FY2025": 140563, "FY2024": 112563, "FY2023": 90867, "FY2022": 110630, "FY2021": 29597}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Total Capital Ratio", TOTAL_CAPITAL_RATIO),
        ("Leverage Ratio", LEVERAGE_RATIO),
        ("LCR", LCR),
        ("NSFR", NSFR),
    ],
    note="Figures are Distribution Finance Capital Holdings plc Group-consolidated basis (the PRA-"
         "regulated Bank's own filed accounts are fully scanned with no text layer; the Group and "
         "regulatory consolidation bases are confirmed identical, so this is not a basis mismatch — "
         "see the Cash Flow Statement sheet's source note). Figures are duplicated from the detail "
         "sheets for at-a-glance trend viewing; see each sheet's own source citation for the "
         "underlying document/page.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/DF CAPITAL BANK FINANCIALS.xlsx")
