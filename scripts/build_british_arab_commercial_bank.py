import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR_URL = {
    "FY2025": "https://files.bacb.co.uk/production/files/BACB_AnnualReportYE2025_WEB-Final.pdf",
    "FY2024": "https://files.bacb.co.uk/production/files/BACB_AnnualReportYE2024_WEB-Final.pdf",
    "FY2023": "https://files.bacb.co.uk/production/files/BACB_AnnualReportYE2023_WEB-06.pdf",
    "FY2022": "https://files.bacb.co.uk/production/files/BACB_AnnualReportYE2022_WEB-1proof-10.pdf",
    "FY2021": "https://files.bacb.co.uk/production/files/BACB_AnnualReportYE2021-1.pdf",
}
P3_URL = {
    "FY2025": "https://files.bacb.co.uk/production/files/BACB_Pillar3_YE2025web-03.pdf",
    "FY2024": "https://files.bacb.co.uk/production/files/BACB_Pillar3_YE2024web-05.pdf",
    "FY2023": "https://files.bacb.co.uk/production/files/BACB_Pillar3YE2023-03-002.pdf",
    "FY2022": "https://files.bacb.co.uk/production/files/BACB_Pillar3YE2022-1.pdf",
    "FY2021": "https://files.bacb.co.uk/production/files/BACB_Pillar3-2021_v3.pdf",
}

ENTITY_NOTE = (
    "British Arab Commercial Bank PLC (\"BACB\"), company 01047302 (incorporated 1972 as UBAF Limited, "
    "renamed British Arab Commercial Bank Limited 1996, re-registered as a public company 2009), FRN 204564. "
    "Owned by a consortium: Libyan Foreign Bank 85.95% (wholly owned by the Central Bank of Libya), Banque "
    "Exterieure d'Algerie 7.025%, Banque Centrale Populaire (Morocco) 7.025%. Single UK entity, no "
    "subsidiaries/associates, no prudential consolidation. Does NOT take the FRS 101/102 cash-flow exemption - "
    "full Statement of Cash Flow every year. GBP throughout, no FX conversion needed. Companies House status: "
    "Active, no going-concern issues found in any of the 5 Annual Reports (unqualified audits throughout).\n\n"
    "RESTATEMENTS: this bank's own cash flow comparatives shift modestly between report vintages (e.g. FY2021's "
    "\"Net cash gained from operating activities\" is 189,594 in the 2021 report's own figures vs 189,407 in "
    "2022's comparative; FY2024's is 227,828 in 2024's own report vs 227,636 in 2025's comparative) - each "
    "year's column here uses that year's own originally-published report, per project convention, not a later "
    "report's restated comparative."
)

CASH_FLOW_SOURCES = (
    "Sources - British Arab Commercial Bank PLC's own Statement of Cash Flow, each year from that year's own "
    "Annual Report (not a later report's restated comparative):\n"
    f"FY2025: Annual Report YE2025, pp.65-66 - {AR_URL['FY2025']}\n"
    f"FY2024: Annual Report YE2024, pp.59-60 - {AR_URL['FY2024']}\n"
    f"FY2023: Annual Report YE2023, p.60 - {AR_URL['FY2023']}\n"
    f"FY2022: Annual Report YE2022, p.56 - {AR_URL['FY2022']}\n"
    f"FY2021: Annual Report YE2021, p.48 - {AR_URL['FY2021']}\n\n"
    + ENTITY_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - British Arab Commercial Bank PLC Pillar 3 Disclosures, UK KM1 Key Metrics template:\n"
        f"FY2025: 2025 Pillar 3 Disclosures, p.6 (own year) - {P3_URL['FY2025']}\n"
        f"FY2024: 2024 Pillar 3 Disclosures, p.6 (own year) - {P3_URL['FY2024']}\n"
        f"FY2023: 2023 Pillar 3 Disclosures, p.6 (own year) - {P3_URL['FY2023']}\n"
        f"FY2022: 2022 Pillar 3 Disclosures, p.7 (own year) - {P3_URL['FY2022']}\n"
        f"FY2021: sourced from the 2022 Pillar 3 Disclosures' own FY2021 comparative column, p.7 - "
        f"{P3_URL['FY2022']} (the 2021 Pillar 3 document predates the modern UK KM1 template and has no "
        "equivalent single table - same approach as Aldermore/BLME/Bank of Ireland UK elsewhere in this project).\n"
        + (extra + "\n" if extra else "")
    )


bw = BankWorkbook(bank_name="British Arab Commercial Bank PLC", years=YEARS, year_label=YEAR_LABEL, header_color="0E7C9E")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit before taxation",
     {"FY2025": 31641, "FY2024": 38209, "FY2023": 36407, "FY2022": 13925, "FY2021": 14703}),
    ("DATA", "Allowance for credit losses",
     {"FY2025": 2313, "FY2024": 3992, "FY2023": 479, "FY2022": 3306, "FY2021": 1245}),
    ("DATA", "Recoveries of allowance for credit losses",
     {"FY2025": -5554, "FY2024": -5633, "FY2023": -2623, "FY2022": -1825, "FY2021": -12441}),
    ("DATA", "Depreciation and amortisation",
     {"FY2025": 3229, "FY2024": 3214, "FY2023": 2904, "FY2022": 2753, "FY2021": 2544}),
    ("DATA", "(Loss)/gain on sale or impairment of property, plant and equipment",
     {"FY2025": -6, "FY2024": 3, "FY2023": 518, "FY2022": 28, "FY2021": 9}),
    ("DATA", "Other non-cash items included in net profit",
     {"FY2025": -1275, "FY2024": -34, "FY2023": 115, "FY2022": 366, "FY2021": -3}),
    ("TOTAL", "Non-cash items included in net profit",
     {"FY2025": -1293, "FY2024": 1542, "FY2023": 1393, "FY2022": 4628, "FY2021": -8646}),
    ("DATA", "Reverse repurchase agreements",
     {"FY2024": 0, "FY2023": 149990, "FY2022": -21103, "FY2021": -36757}),
    ("DATA", "Loans, advances other than cash or cash equivalents",
     {"FY2025": -221607, "FY2024": -243014, "FY2023": -268285, "FY2022": -68881, "FY2021": -13840}),
    ("DATA", "Debt securities other than cash equivalents",
     {"FY2025": 250302, "FY2024": 164699, "FY2023": -108164, "FY2022": -221117, "FY2021": 7009}),
    ("DATA", "Derivatives",
     {"FY2025": -571, "FY2024": -1109, "FY2023": 683, "FY2022": -728, "FY2021": 465}),
    ("DATA", "Other debtors and prepayments",
     {"FY2025": -7064, "FY2024": 387, "FY2023": -9064, "FY2022": -1161, "FY2021": 1497}),
    ("TOTAL", "Change in operating assets",
     {"FY2025": 21060, "FY2024": -79037, "FY2023": -234840, "FY2022": -312990, "FY2021": -41626}),
    ("DATA", "Customer accounts and deposits by banks",
     {"FY2025": 78001, "FY2024": 277676, "FY2023": -94670, "FY2022": 165574, "FY2021": 238429}),
    ("DATA", "Other liabilities",
     {"FY2025": 2884, "FY2024": -2695, "FY2023": 10519, "FY2022": 9288, "FY2021": -12192}),
    ("TOTAL", "Change in operating liabilities",
     {"FY2025": 80885, "FY2024": 274981, "FY2023": -84151, "FY2022": 174862, "FY2021": 226237}),
    ("DATA", "Income tax paid",
     {"FY2025": -8155, "FY2024": -7867, "FY2023": -5220, "FY2022": -1169, "FY2021": -1074}),
    ("TOTAL", "Net cash generated from/(used in) operating activities",
     {"FY2025": 124138, "FY2024": 227828, "FY2023": -286411, "FY2022": -120744, "FY2021": 189594}),

    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment",
     {"FY2025": -409, "FY2024": -1590, "FY2023": -7683, "FY2022": -552, "FY2021": -274}),
    ("DATA", "Proceeds from sale of property, plant and equipment", {"FY2022": 42}),
    ("DATA", "Proceeds on sale of equity investments", {"FY2024": 1162}),
    ("DATA", "Purchase of intangible assets",
     {"FY2025": -1128, "FY2024": -392, "FY2023": -841, "FY2022": -853, "FY2021": -540}),
    ("DATA", "Proceeds from sale of intangible assets", {"FY2022": 269}),
    ("TOTAL", "Net cash used in investing activities",
     {"FY2025": -1537, "FY2024": -820, "FY2023": -8524, "FY2022": -1094, "FY2021": -814}),

    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Dividend paid", {"FY2025": -6228, "FY2024": -4780, "FY2023": -5215, "FY2022": -8765}),
    ("DATA", "Lease payments for Right of Use assets (principal)",
     {"FY2025": -249, "FY2024": -83, "FY2023": -202, "FY2022": -6, "FY2021": -191}),
    ("DATA", "Interest on lease payments", {"FY2024": -192}),
    ("DATA", "Subordinated debt issued", {"FY2024": 28185}),
    ("DATA", "Subordinated debt redeemed", {"FY2024": -28185}),
    ("TOTAL", "Net cash used in financing activities",
     {"FY2025": -6477, "FY2024": -5055, "FY2023": -5417, "FY2022": -8771, "FY2021": -191}),

    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents",
     {"FY2025": 116124, "FY2024": 221953, "FY2023": -300352, "FY2022": -130609, "FY2021": 188589}),
    ("DATA", "Cash and cash equivalents at the beginning of the year",
     {"FY2025": 604467, "FY2024": 372940, "FY2023": 700795, "FY2022": 766720, "FY2021": 586617}),
    ("DATA", "Effect of exchange rate change on cash and cash equivalents",
     {"FY2025": -2014, "FY2024": 9574, "FY2023": -27503, "FY2022": 64684, "FY2021": -8486}),
    ("TOTAL", "Cash and cash equivalents at the end of the year",
     {"FY2025": 718577, "FY2024": 604467, "FY2023": 372940, "FY2022": 700795, "FY2021": 766720}),

    ("SECTION", "Cash and cash equivalents comprise", {}),
    ("DATA", "Cash, notes and coin",
     {"FY2025": 0, "FY2024": 1, "FY2023": 1, "FY2022": 0, "FY2021": 218}),
    ("DATA", "Loans and advances to banks of original maturity three months or less",
     {"FY2025": 409309, "FY2024": 488558, "FY2023": 216705, "FY2022": 391580, "FY2021": 376162}),
    ("DATA", "Debt securities/certificates of deposit of three months original maturity or less",
     {"FY2025": 309268, "FY2024": 115908, "FY2023": 156234, "FY2022": 309215, "FY2021": 390340}),
    ("TOTAL", "Cash and cash equivalents",
     {"FY2025": 718577, "FY2024": 604467, "FY2023": 372940, "FY2022": 700795, "FY2021": 766720}),
]

bw.add_cash_flow_sheet(
    title="British Arab Commercial Bank PLC — Statement of Cash Flow",
    subtitle="Bank entity basis (single UK entity, no subsidiaries/associates). GBP throughout, no FX conversion.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=68,
    source_height=210,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=170)


CET1 = {"FY2025": 266352, "FY2024": 245034, "FY2023": 223772, "FY2022": 197516, "FY2021": 199873}
TOTAL_CAPITAL = {"FY2025": 334756, "FY2024": 318553, "FY2023": 276133, "FY2022": 267579, "FY2021": 270130}
RWA = {"FY2025": 1924184, "FY2024": 1571106, "FY2023": 1240666, "FY2022": 1231445, "FY2021": 1085219}
CET1_RATIO = {"FY2025": "13.8%", "FY2024": "15.6%", "FY2023": "18.0%", "FY2022": "16.0%", "FY2021": "18.4%"}
TCR = {"FY2025": "17.4%", "FY2024": "20.3%", "FY2023": "22.3%", "FY2022": "21.7%", "FY2021": "24.9%"}
LEVERAGE_RATIO = {"FY2025": "7.2%", "FY2024": "6.6%", "FY2023": "6.8%", "FY2022": "5.7%", "FY2021": "6.7%"}
LCR = {"FY2025": "234%", "FY2024": "327%", "FY2023": "271%", "FY2022": "254%", "FY2021": "276%"}
NSFR = {"FY2025": "166%", "FY2024": "160%", "FY2023": "151%", "FY2022": "130%"}

RWA_RESTATEMENT_NOTE = (
    "FY2022's Total RWA/CET1/Tier1/Total Capital ratios shown here are as originally published in the 2022 "
    "Pillar 3 Disclosures (RWA 1,231,445). The 2023 Pillar 3 Disclosures' own FY2022 comparative column restates "
    "this to 1,224,488 (footnoted 'amended for consistency of presentation') with correspondingly adjusted ratios "
    "(16.1% CET1/Tier1, 21.9% Total Capital) - the originally-published figure is used here, per project convention."
)

metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", CET1)], p3_sources())
metric("CET1 Ratio", "%", [("CET1 ratio", CET1_RATIO)], p3_sources(), note=RWA_RESTATEMENT_NOTE)
metric("Tier 1 Capital", "£'000 (= CET1 capital; no AT1 instruments)", [("Tier 1 capital", CET1)], p3_sources())
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", CET1_RATIO)], p3_sources())
metric("Total Capital", "£'000", [("Total capital", TOTAL_CAPITAL)], p3_sources())
metric("Total Capital Ratio", "%", [("Total capital ratio", TCR)], p3_sources(), note=RWA_RESTATEMENT_NOTE)
metric("Total RWAs", "£'000", [("Total risk-weighted exposure amount", RWA)], p3_sources(),
       note="See CET1 Ratio sheet for the FY2022 restatement note.")
metric("Leverage Ratio", "%", [("Leverage ratio", LEVERAGE_RATIO)], p3_sources())
metric("LCR", "%", [("Liquidity coverage ratio (12-month average)", LCR)], p3_sources())
metric("NSFR", "%", [("NSFR ratio (4-quarter average)", NSFR)], p3_sources(
    extra="NSFR not applicable/disclosed for FY2021 - the NSFR reporting requirement and KM1 template line were "
          "new from FY2022; the FY2021 comparative column in the 2022 Pillar 3 Disclosures itself states 'N/A'."))

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources(),
    per_note={"MREL Ratio": "Not found in any of the 5 Annual Reports or Pillar 3 Disclosures checked - not "
                             "asserted as an explicit exemption, just absent from every source."},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash generated from/(used in) operating activities",
         {"FY2025": 124138, "FY2024": 227828, "FY2023": -286411, "FY2022": -120744, "FY2021": 189594}),
        ("Net cash used in investing activities",
         {"FY2025": -1537, "FY2024": -820, "FY2023": -8524, "FY2022": -1094, "FY2021": -814}),
        ("Net cash used in financing activities",
         {"FY2025": -6477, "FY2024": -5055, "FY2023": -5417, "FY2022": -8771, "FY2021": -191}),
        ("Cash and cash equivalents at end of year",
         {"FY2025": 718577, "FY2024": 604467, "FY2023": 372940, "FY2022": 700795, "FY2021": 766720}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Total Capital Ratio", TCR),
        ("Leverage Ratio", LEVERAGE_RATIO),
        ("LCR", LCR),
        ("NSFR", NSFR),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BRITISH ARAB COMMERCIAL BANK FINANCIALS.xlsx")
