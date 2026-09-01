import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://www.crownagentsbank.com/wp-content/uploads/2026/04/Crown-Agents-Bank-2025-Annual-Report.pdf"
AR2023_URL = "http://www.crownagentsbank.com/wp-content/uploads/2025/09/cab_fs_ye_2023_signed_3_april_2024_audited.pdf"
AR2022_URL = "http://www.crownagentsbank.com/wp-content/uploads/2025/09/cab_financial_statements_2022_signed_19_april_formatted_version.pdf"
AR2021_URL = "http://www.crownagentsbank.com/wp-content/uploads/2025/09/cab_2021_financial_statements_1_apr.pdf"

P3_2025_URL = "https://www.crownagentsbank.com/wp-content/uploads/2026/04/CAB-Pillar-3-Document-2025-FINAL.pdf"
P3_2024_URL = "http://www.crownagentsbank.com/wp-content/uploads/2025/09/cab_pillar_3_-_document_2024_post_bac.pdf"
P3_2023_URL = "http://www.crownagentsbank.com/wp-content/uploads/2025/09/2023_cab_pillar_3_disclosures_final.pdf"
P3_2022_URL = "http://www.crownagentsbank.com/wp-content/uploads/2025/09/cab_pillar_3_disclosures_2022_v3.pdf"

ENTITY_NOTE = (
    "Crown Agents Bank Limited (FRN 204456, company 02334687) is the PRA-regulated bank entity - "
    "distinct from its LSE-listed ultimate parent CAB Payments Holdings plc (which IPO'd in 2023 and "
    "has faced separate, unrelated corporate-control events - a withdrawn possible offer from StoneX "
    "and an unrecommended offer from Helios - neither of which affects this Bank entity's own figures "
    "below). All figures are the Bank's OWN entity-level disclosures (Companies House filing history "
    "and the Bank's own Pillar 3 documents), not the wider listed Group's consolidated figures, which "
    "are published separately under the \"CAB Payments Holdings plc\" name and are NOT used here.\n\n"
    "RESTATEMENTS: two genuine cross-vintage restatements were found in the cash flow statement. "
    "FY2022's own originally-published net cash used in operating activities was £(252,244)k; the "
    "FY2023 Annual Report's own comparative column restates this to £(236,806)k (a £15,438k "
    "difference), with no explanation located for the change. FY2021's own originally-published net "
    "cash generated from operating activities was £318,950k; the FY2022 Annual Report's own "
    "comparative column restates this to £313,819k (a £5,131k difference). Per project convention, "
    "each year's own originally-published figures are used throughout (not later restated "
    "comparatives).\n\n"
    "Two minor, unexplained cross-vintage cash-bridge gaps also exist and are left as genuinely "
    "reported rather than forced to reconcile: FY2021's own closing balance (£1,118,821k) does not "
    "match FY2022's own opening balance (£1,113,467k), a £5,354k gap; FY2023's own closing balance "
    "(£1,179,607k) does not exactly match FY2024's own opening balance (£1,181,046k), a £1,439k gap."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Crown Agents Bank Limited's own Statement of Cash Flows (Bank-solo, "
    "no subsidiaries consolidated):\n"
    f"FY2025/FY2024: Annual Report and Financial Statements 2025, p.56-57 & p.105-106 (Statement of "
    f"Cash Flows + Note 28 reconciliation) - {AR2025_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.59 (Statement of cash flows) - {AR2023_URL}\n"
    f"FY2022/FY2021 (own originally-published figures, not FY2023's or FY2022's restated comparatives): "
    f"Annual Report and Financial Statements 2022, p.41 (Statement of Cash Flows) - {AR2022_URL}; "
    f"Annual Report and Financial Statements 2021, p.38 (Cash Flow Statement) - {AR2021_URL}\n\n"
    + ENTITY_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - Crown Agents Bank Limited Pillar 3 basis (Bank-solo, UK KM1 Key Metrics table unless noted):\n"
        f"FY2025: Pillar 3 Disclosures - 31 December 2025, p.9 (UK KM1) - {P3_2025_URL}\n"
        f"FY2024: Pillar 3 Disclosures - 31 December 2024, p.9 (UK KM1) - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures - 31 December 2023, p.9 (UK KM1) - {P3_2023_URL}\n"
        f"FY2022: Pillar 3 Disclosures - 31 December 2022, p.9 (Summary of Key Ratios - pre-KM1-template "
        f"format) - {P3_2022_URL}, cross-checked against FY2023's own KM1 comparative column where available\n"
        f"FY2021: sourced from the FY2022 document's own comparative column (p.9, Summary of Key Ratios) - "
        f"{P3_2022_URL} - no capital/liquidity summary table was located within budget in the FY2021 Pillar 3 "
        f"document itself.\n"
        "FY2021 predates the UK's post-Brexit CRR/KM1 regulatory regime, which UK banks became subject to "
        "from 1 January 2022 (per the FY2022 document's own Introduction) - FY2021 figures may not be "
        "directly comparable to FY2022 onward on a like-for-like basis.\n"
        + extra
    )


bw = BankWorkbook(bank_name="Crown Agents Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="A9152C")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Cash (outflow)/inflow from operating activities (before tax/lease interest)",
     {"FY2025": -614029, "FY2024": 99180, "FY2023": 308912, "FY2022": -242642, "FY2021": 321062}),
    ("DATA", "Tax paid",
     {"FY2025": -4687, "FY2024": -11766, "FY2023": -14084, "FY2022": -9583, "FY2021": -2112}),
    ("DATA", "Payments for interest on lease liabilities",
     {"FY2025": 0, "FY2024": -33, "FY2023": -65, "FY2022": -19}),
    ("TOTAL", "Net cash (used in)/generated from operating activities",
     {"FY2025": -618716, "FY2024": 87381, "FY2023": 294763, "FY2022": -252244, "FY2021": 318950}),

    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment",
     {"FY2025": -108, "FY2024": -2334, "FY2023": -416, "FY2022": -346, "FY2021": -302}),
    ("DATA", "Purchase/capitalisation of intangible assets",
     {"FY2025": -6778, "FY2024": -12141, "FY2023": -6642, "FY2022": -4375, "FY2021": -4313}),
    ("DATA", "Sale/(purchase) of equity investments/shares/exchange traded funds",
     {"FY2024": -53, "FY2021": -228}),
    ("DATA", "Purchase of investments in subsidiary undertakings",
     {"FY2025": -2577, "FY2024": -1269, "FY2023": -543}),
    ("TOTAL", "Net cash used in investing activities",
     {"FY2025": -9463, "FY2024": -15797, "FY2023": -7601, "FY2022": -4721, "FY2021": -4843}),

    ("SECTION", "Financing activities", {}),
    ("DATA", "Repayment of principal portion of lease liability", {"FY2024": -257, "FY2023": -462, "FY2022": -233}),
    ("DATA", "Reduction in overdraft", {}),
    ("TOTAL", "Net cash (used in)/generated from financing activities",
     {"FY2025": 0, "FY2024": -257, "FY2023": -462, "FY2022": -233, "FY2021": 0}),

    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents",
     {"FY2025": -628179, "FY2024": 71327, "FY2023": 286700, "FY2022": -257198, "FY2021": 314107}),
    ("DATA", "Cash and cash equivalents at the beginning of the year",
     {"FY2025": 1257559, "FY2024": 1181046, "FY2023": 906801, "FY2022": 1113467, "FY2021": 803412}),
    ("DATA", "Effect of exchange rate changes on cash and cash equivalents",
     {"FY2025": -26321, "FY2024": 5186, "FY2023": -13894, "FY2022": 50531, "FY2021": 1302}),
    ("TOTAL", "Cash and cash equivalents at the end of the year",
     {"FY2025": 603059, "FY2024": 1257559, "FY2023": 1179607, "FY2022": 906801, "FY2021": 1118821}),
]

bw.add_cash_flow_sheet(
    title="Crown Agents Bank Limited — Statement of Cash Flows",
    subtitle="Bank-solo basis, £'000. See source note at bottom (genuine restatements and cross-vintage gaps documented).",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=340,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=48, source_height=170)


CET1_CAPITAL = {"FY2025": 141776, "FY2024": 126265, "FY2023": 115358, "FY2022": 89871, "FY2021": 56661}
RWA = {"FY2025": 619414, "FY2024": 627016, "FY2023": 436220, "FY2022": 269258, "FY2021": 187000}
CET1_RATIO = {"FY2025": "22.9%", "FY2024": "20.1%", "FY2023": "26.4%", "FY2022": "33.4%", "FY2021": "30.3%"}
LEVERAGE_RATIO = {"FY2025": "9.5%", "FY2024": "7.4%", "FY2023": "7.3%", "FY2022": "6.9%", "FY2021": "5.0%"}
LCR = {"FY2025": "134.7%", "FY2024": "136.4%", "FY2023": "149.7%", "FY2022": "143.2%", "FY2021": "132%"}
NSFR = {"FY2025": "130.0%", "FY2024": "130.9%", "FY2023": "159.4%", "FY2022": "206.6%", "FY2021": "211%"}

RWA_NOTE = (
    "FY2021's RWA (£187m) is directly stated in the FY2022 document's own comparative column (rounded "
    "to the nearest £m, not disclosed to the £'000). All other years disclosed to the £'000 in their own "
    "KM1 tables."
)
CET1_CAPITAL_NOTE = (
    "FY2021's CET1/Tier1/Total Capital (£56,661k) is CALCULATED (RWA £187,000k x CET1 Ratio 30.3%) since "
    "no absolute capital figure was directly disclosed for FY2021, only the ratio and RWA - flagged, not "
    "guessed. All other years (FY2022 onward) are directly disclosed in the respective year's own KM1 table "
    "(FY2022's calculated cross-check: £269,258k x 33.4% = £89,933k vs the directly-disclosed £89,871k - "
    "matches closely, confirming the calculation method is sound)."
)
LIQUIDITY_BASIS_NOTE = (
    "LIQUIDITY RATIO BASIS CAVEAT: the FY2022 Pillar 3 document's own \"Summary of Key Ratios\" table shows "
    "LCR 158% and NSFR 213% for FY2022, and LCR 132%/NSFR 211% for FY2021 - but the FY2023 document's own "
    "KM1 table, which explicitly states its LCR is a \"12 month average\" and NSFR a \"4 quarter average\", "
    "gives a materially different Dec-2022 comparative (LCR 143.2%, NSFR 206.6%). This is the same "
    "spot-vs-average LCR/NSFR basis trap seen elsewhere in this project (e.g. ALRAYAN Bank, Bank of Africa "
    "UK) - the FY2022 document's own summary table doesn't state its methodology explicitly, but the gap "
    "strongly suggests a different (likely point-in-time/spot) basis. Used the KM1/average-basis figure for "
    "FY2022 (143.2%/206.6%) for consistency with every other bank in this project; the FY2022 document's own "
    "158%/213% figures are documented here for reference. FY2021 has no KM1-basis alternative available "
    "(predates the KM1 template rollout, per the FY2022 document's own note that UK banks became subject "
    "to the current regime from 1 January 2022) - FY2021's 132%/211% are used as the only figures found, "
    "flagged as likely not directly comparable to FY2022-onward's KM1-basis figures."
)

metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", CET1_CAPITAL)],
       p3_sources(), note=CET1_CAPITAL_NOTE)
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 (CET1) ratio", CET1_RATIO)], p3_sources())
metric("Tier 1 Capital", "£'000 (= CET1 Capital; no AT1 instruments)", [("Tier 1 capital", CET1_CAPITAL)],
       p3_sources(), note=CET1_CAPITAL_NOTE)
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", CET1_RATIO)], p3_sources())
metric("Total Capital", "£'000 (= CET1 Capital; no Tier 2 instruments)", [("Total capital", CET1_CAPITAL)],
       p3_sources(), note=CET1_CAPITAL_NOTE)
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", CET1_RATIO)], p3_sources())
metric("Total RWAs", "£'000", [("Total risk-weighted exposure amount", RWA)], p3_sources(), note=RWA_NOTE)
metric("Leverage Ratio", "%, excluding claims on central banks", [("Leverage ratio", LEVERAGE_RATIO)], p3_sources())
metric("LCR", "%", [("Liquidity Coverage Ratio", LCR)], p3_sources(), note=LIQUIDITY_BASIS_NOTE)
metric("NSFR", "%", [("Net Stable Funding Ratio", NSFR)], p3_sources(), note=LIQUIDITY_BASIS_NOTE)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources(),
    per_note={"MREL Ratio": "Not publicly disclosed - no MREL figure or exemption statement found in any "
                             "of the 5 years' Pillar 3 documents reviewed."},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash (used in)/generated from operating activities",
         {"FY2025": -618716, "FY2024": 87381, "FY2023": 294763, "FY2022": -252244, "FY2021": 318950}),
        ("Net cash used in investing activities",
         {"FY2025": -9463, "FY2024": -15797, "FY2023": -7601, "FY2022": -4721, "FY2021": -4843}),
        ("Net cash (used in)/generated from financing activities",
         {"FY2025": 0, "FY2024": -257, "FY2023": -462, "FY2022": -233, "FY2021": 0}),
        ("Cash and cash equivalents at end of year",
         {"FY2025": 603059, "FY2024": 1257559, "FY2023": 1179607, "FY2022": 906801, "FY2021": 1118821}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Total Capital Ratio", CET1_RATIO),
        ("Leverage Ratio", LEVERAGE_RATIO),
        ("LCR", LCR),
        ("NSFR", NSFR),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. LCR/NSFR shown here use the KM1/average basis "
         "from FY2022 onward - see the LCR/NSFR sheets' own CAVEAT note for FY2021/FY2022 basis ambiguity.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/CROWN AGENTS BANK FINANCIALS.xlsx")
