import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}
PREV_YEAR = {"FY2021": "FY2020", "FY2022": "FY2021", "FY2023": "FY2022", "FY2024": "FY2023", "FY2025": "FY2024"}

# ---------------------------------------------------------------
# FX conversion (FCMB Bank (UK) Limited reports in USD; converting to £ per
# this project's established FX methodology). Same 31 December year-end as
# Zenith Bank UK / Union Bank of India UK - reusing that exact rate table
# rather than re-deriving it. Rates are Bank of England GBP/USD spot/average
# via poundsterlinglive.com's published archive, £1 = $X.
# ---------------------------------------------------------------
FX_SPOT = {
    "FY2020": 1.3661,  # 31 Dec 2020 - only used for FY2021's opening cash balance
    "FY2021": 1.3521,
    "FY2022": 1.2097,
    "FY2023": 1.2732,
    "FY2024": 1.2515,
    "FY2025": 1.3448,
}
FX_AVG = {
    "FY2021": 1.3752,
    "FY2022": 1.2362,
    "FY2023": 1.2439,
    "FY2024": 1.2782,
    "FY2025": 1.3193,
}


def flow(usd):
    return {y: round(v / FX_AVG[y] / 1000, 1) for y, v in usd.items()}


def stock(usd):
    return {y: round(v / FX_SPOT[y] / 1000, 1) for y, v in usd.items()}


def opening_cash(usd):
    return {y: round(v / FX_SPOT[PREV_YEAR[y]] / 1000, 1) for y, v in usd.items()}


AR2025_URL = "https://fcmbuk.com/wp-content/uploads/2026/08/SIGNED-FCMB-Bank-UK-Limited-Audited-Accounts-2025.pdf"
AR2024_URL = "https://fcmbuk.com/wp-content/uploads/2025/09/FCMB-Bank-UK-Limited-Audited-Accounts-2024-Signed.pdf"
AR2023_URL = "https://fcmbuk.com/wp-content/uploads/2024/07/FCMB-Bank-UK-Limited-Audited-Accounts-2023.pdf"
AR2022_URL = "https://fcmbuk.com/wp-content/uploads/2023/09/FCMB-Bank-UK-Limited-Signed-Annual-Report-Financial-Statements-2022.pdf"
AR2021_URL = "https://fcmbuk.com/wp-content/uploads/2023/09/FCMB-Bank-UK-Limited-Signed-Audited-Accounts-2021.pdf"
P3_2025_URL = "https://fcmbuk.com/wp-content/uploads/2026/08/5.-Pillar-III-Disclosures-FYE-2025-30-June-2026.pdf"
P3_2024_URL = "https://fcmbuk.com/wp-content/uploads/2025/09/Pillar-III-Disclosures-FYE-2024.pdf"
P3_2023_URL = "https://fcmbuk.com/wp-content/uploads/2024/08/Pillar-III-Disclosures-FYE-2023.pdf"
P3_2022_URL = "https://fcmbuk.com/wp-content/uploads/2023/09/Pillar-III-Disclosures-FYE-2022.pdf"
P3_2021_URL = "https://fcmbuk.com/wp-content/uploads/2022/07/Pillar-III-Disclosures-FYE-2021-002.pdf"

ENTITY_NOTE = (
    "FCMB Bank (UK) Limited (company 06621225, FRN 502704) is a UK subsidiary of First City Monument "
    "Bank (Nigeria). Does NOT take the FRS 101/102 cash-flow exemption - a full Statement of Cash Flows "
    "exists every year. Each year's own originally-published figures used throughout - the closing "
    "balance of each year ties exactly to the following year's own opening balance across all 5 years.\n"
    "DATA QUALITY NOTE (FY2024): the FY2025 Annual Report's own FY2024 comparative column shows "
    "materially different 'Changes in operating assets and liabilities' line items (and a different "
    "Operating/Investing split) than FY2024's own originally-published Annual Report - e.g. 'Net "
    "(increase) in loans and advances to banks' is $(42,672,236) in the FY2025 report's comparative "
    "vs. $(35,611,527) in FY2024's own report. FY2024's own figures are used throughout (per project "
    "convention), and independently confirmed internally consistent (adjustments subtotal $2,243,237 + "
    "changes subtotal $4,830,112 = $7,073,349, matching FY2024's own printed operating total exactly). "
    "Net cash flow for the year, opening balance, and closing balance are IDENTICAL between both "
    "vintages ($(239,325) net change, both years) - only the Operating/Investing section split differs, "
    "consistent with a presentational reclassification rather than a change in the Bank's actual cash "
    "position. Similarly, FY2021's own report classifies 'Issuance of subordinated liabilities' "
    "($2,000,000) within Operating activities, while later reports' FY2021 comparative reclassifies it "
    "into Financing activities - the FY2022 report's own footnote explicitly confirms this deliberate "
    "reclassification ('Subordinated liabilities were classified under operating activities in 2021. In "
    "2022, subordinated liabilities have been classified under financing activities for the current "
    "year and in the prior year comparatives.'). FY2021's own original classification is used here, per "
    "convention.\n"
    "FX CONVERSION: the Bank's functional and presentational currency is USD. Converted to £ per this "
    "project's established methodology: point-in-time/balance figures (capital, RWA, leverage exposure, "
    "HQLA, cash balances) use the Bank of England GBP/USD SPOT rate as at that fiscal year-end (31 "
    "December); flow figures (every cash flow statement line item) use the AVERAGE of Bank of England "
    "rates over that calendar year. Rate table reused from Zenith Bank UK/Union Bank of India UK "
    "(same 31 Dec year-end): 31 Dec 2020 spot 1.3661 (FY2021 opening cash only); FY2021 spot 1.3521 / "
    "average 1.3752; FY2022 spot 1.2097 / average 1.2362; FY2023 spot 1.2732 / average 1.2439; FY2024 "
    "spot 1.2515 / average 1.2782; FY2025 spot 1.3448 / average 1.3193. All % ratios are shown exactly "
    "as reported in USD, not converted (dimensionless, currency-invariant). An explicit 'Effect of "
    "GBP/USD translation' line reconciles the stock/flow rate mismatch so opening + flows + this line = "
    "closing exactly in £ terms; computed programmatically from the actual converted figures, not "
    "hardcoded."
)

CASH_FLOW_SOURCES = (
    "Sources - FCMB Bank (UK) Limited's own Statement of Cash Flows, from its Companies House-filed "
    "Annual Report and Accounts (also published on the Bank's own site):\n"
    f"FY2025: Audited Accounts 2025, p.42-43 - {AR2025_URL}\n"
    f"FY2024: Audited Accounts 2024, p.31 (own-year figures; FY2024 comparative in the FY2025 report cross-checked and matched exactly) - {AR2024_URL}\n"
    f"FY2023: Audited Accounts 2023, p.33 - {AR2023_URL}\n"
    f"FY2022: Annual Report & Financial Statements 2022, p.31 (own-year figures; FY2022 comparative in the FY2023 report cross-checked and matched exactly) - {AR2022_URL}\n"
    f"FY2021: Audited Accounts 2021, p.28 - {AR2021_URL}\n"
    + ENTITY_NOTE
)


def p3_sources(page_2025="3", page_2024="2", page_2023="19", page_2022="19"):
    return (
        "Sources - FCMB Bank (UK) Limited Pillar 3 Disclosures ('Key Regulatory Metrics' table):\n"
        f"FY2025: Pillar III Disclosures FYE 2025, p.{page_2025} - {P3_2025_URL}\n"
        f"FY2024: Pillar III Disclosures FYE 2024, p.{page_2024} (own-year; also cross-checked against FY2025's comparative column, matched exactly) - {P3_2024_URL}\n"
        f"FY2023: Pillar III Disclosures FYE 2023, p.{page_2023} (own-year; also cross-checked against FY2024's comparative column, matched exactly) - {P3_2023_URL}\n"
        f"FY2022: Pillar III Disclosures FYE 2022, p.{page_2022} (own-year; also cross-checked against FY2023's comparative column, matched exactly) - {P3_2022_URL}\n"
        f"FY2021: sourced from FY2022's Pillar III Disclosures own comparative column - the FY2021 document itself "
        f"(Pillar III Disclosures FYE 2021, {P3_2021_URL}) pre-dates this 'Key Regulatory Metrics'/KM1-style table "
        "and only discloses a 'Minimum Capital Requirements' breakdown with no CET1/Total Capital/RWA/Leverage/"
        "LCR/NSFR figures - same pattern as Aldermore/BLME/Bank of Ireland UK/British Arab Commercial Bank "
        "elsewhere in this project.\n"
        "LCR/NSFR methodology note (per the Bank's own documents, CRR Article 447): each LCR component is "
        "calculated as a 12-month average, and NSFR components as the average of the last 4 quarters - i.e. the "
        "LCR%/NSFR% shown are themselves already period averages, not point-in-time spot ratios."
    )


bw = BankWorkbook(bank_name="FCMB Bank (UK) Limited", years=YEARS, year_label=YEAR_LABEL, header_color="A90D9C")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows_usd = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(Loss) before tax for the year",
     {"FY2025": -4899200, "FY2024": 3301017, "FY2023": 5642919, "FY2022": 2953126, "FY2021": 1124026}),
    ("DATA", "Depreciation and amortisation",
     {"FY2025": 797249, "FY2024": 804587, "FY2023": 672685, "FY2022": 579990, "FY2021": 603791}),
    ("DATA", "Non-cash PPE movements", {"FY2023": 1010191}),
    ("DATA", "Changes to ROU asset, Interest & lease liability", {"FY2025": 3130, "FY2024": -831690}),
    ("DATA", "Provision/impairment charge for loan losses (label varies by year - see source note)",
     {"FY2025": 5384068, "FY2024": -1023267, "FY2023": 1795645, "FY2022": 2508414, "FY2021": 77775}),
    ("DATA", "(Net gain)/Loss on investment activities", {"FY2025": 898826}),
    ("DATA", "Effect of currency translation on cash and cash equivalents (operating adjustment)",
     {"FY2025": -670243, "FY2024": -7410, "FY2023": -8096, "FY2022": 66367, "FY2021": 11947}),
    ("TOTAL", "Cash flows from operating activities before changes in operating assets and liabilities",
     {"FY2025": 1513830, "FY2024": 2243237, "FY2023": 9113344, "FY2022": 6107897, "FY2021": 1817539}),
    ("DATA", "Net (increase) in loans and advances to banks",
     {"FY2025": -49909448, "FY2024": -35611527, "FY2023": -40236174, "FY2022": -7790893, "FY2021": -14354382}),
    ("DATA", "Net (increase)/decrease in loans and advances to customers",
     {"FY2025": -33865933, "FY2024": -11601238, "FY2023": -3765576, "FY2022": 6754576, "FY2021": -27914986}),
    ("DATA", "Net decrease/(increase) in derivative FIs",
     {"FY2025": -3293894, "FY2024": 1295271, "FY2023": -2384003, "FY2022": 492972, "FY2021": 5058288}),
    ("DATA", "Net (increase)/decrease in other assets",
     {"FY2025": 40077, "FY2024": -4047332, "FY2023": -1039844, "FY2022": -979246, "FY2021": -3061931}),
    ("DATA", "Net increase/(decrease) in deposits from banks",
     {"FY2025": 27094889, "FY2024": 48429573, "FY2023": -6029796, "FY2022": 91435975, "FY2021": -15995514}),
    ("DATA", "Net increase/(decrease) in deposits from customers",
     {"FY2025": 62092889, "FY2024": 5009718, "FY2023": -57791638, "FY2022": 15652787, "FY2021": 29913143}),
    ("DATA", "Net increase in subordinated liabilities", {"FY2021": 2000000}),
    ("DATA", "Net increase/(decrease) in other liabilities",
     {"FY2025": 2191933, "FY2024": 1964709, "FY2023": 1934898, "FY2022": 707738, "FY2021": 911716}),
    ("DATA", "Taxation Paid", {"FY2025": -282719, "FY2024": -609062, "FY2023": -1689353}),
    ("TOTAL", "Net cash flows from operating activities",
     {"FY2025": 5581624, "FY2024": 7073349, "FY2023": -101888142, "FY2022": 112381806, "FY2021": -21626127}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Acquisition of investment securities",
     {"FY2025": -1781759737, "FY2024": -1560609502, "FY2023": -1910769930, "FY2022": -773481181, "FY2021": -640171183}),
    ("DATA", "Disposal of investment securities",
     {"FY2025": 1779031267, "FY2024": 1554220291, "FY2023": 2008897440, "FY2022": 658367424, "FY2021": 655246302}),
    ("DATA", "Purchases of property and equipment",
     {"FY2025": -102864, "FY2024": -201207, "FY2023": -101367, "FY2022": -29323, "FY2021": -31689}),
    ("DATA", "Purchases of intangible assets",
     {"FY2025": -167364, "FY2024": -321532, "FY2023": -357134, "FY2022": -274691, "FY2021": -46850}),
    ("TOTAL", "Net cash flows from investing activities",
     {"FY2025": -2998699, "FY2024": -6911950, "FY2023": 97669009, "FY2022": -115417771, "FY2021": 14996580}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Issuance of own shares", {"FY2023": 5000000}),
    ("DATA", "Issuance of subordinated liabilities", {"FY2022": 4600000}),
    ("DATA", "Payments made for lease liability",
     {"FY2025": -452280, "FY2024": -400724, "FY2023": -408491, "FY2022": -359478, "FY2021": -402811}),
    ("TOTAL", "Net cash flows from financing activities",
     {"FY2025": -452280, "FY2024": -400724, "FY2023": 4591509, "FY2022": 4240522, "FY2021": -402811}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents",
     {"FY2025": 2130645, "FY2024": -239325, "FY2023": 372376, "FY2022": 1204557, "FY2021": -7032358}),
    ("DATA", "Cash and cash equivalents at 1 January",
     {"FY2025": 7266626, "FY2024": 7498541, "FY2023": 7118069, "FY2022": 5979879, "FY2021": 13024184}),
    ("DATA", "Effect of currency translation on cash and cash equivalents (closing bridge)",
     {"FY2025": 670243, "FY2024": 7410, "FY2023": 8096, "FY2022": -66367, "FY2021": -11947}),
    ("TOTAL", "Cash and cash equivalents at 31 December",
     {"FY2025": 10067514, "FY2024": 7266626, "FY2023": 7498541, "FY2022": 7118069, "FY2021": 5979879}),
]

_usd_by_label = {label: usd for _, label, usd in rows_usd}
rows = []
for kind, label, usd in rows_usd:
    if kind == "SECTION":
        rows.append((kind, label, {}))
    elif label == "Cash and cash equivalents at 1 January":
        rows.append((kind, label, opening_cash(usd)))
    elif label == "Cash and cash equivalents at 31 December":
        rows.append((kind, label, stock(usd)))
    else:
        rows.append((kind, label, flow(usd)))
    if label == "Effect of currency translation on cash and cash equivalents (closing bridge)":
        opening_gbp = opening_cash(_usd_by_label["Cash and cash equivalents at 1 January"])
        closing_gbp = stock(_usd_by_label["Cash and cash equivalents at 31 December"])
        net_change_gbp = flow(_usd_by_label["Net (decrease)/increase in cash and cash equivalents"])
        fx_gbp = flow(usd)
        plug = {
            y: round(closing_gbp[y] - opening_gbp[y] - net_change_gbp[y] - fx_gbp.get(y, 0), 1)
            for y in closing_gbp
        }
        rows.append(("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", plug))

bw.add_cash_flow_sheet(
    title="FCMB Bank (UK) Limited — Statement of Cash Flows",
    subtitle="£'000, converted from USD - see source note at bottom for FX methodology and rates used.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=95,
    source_height=280,
    unit_suffix="",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=170)


CET1_USD = {"FY2025": 54656000, "FY2024": 57951000, "FY2023": 50032000, "FY2022": 40321000, "FY2021": 42915000}
TOTALCAP_USD = {"FY2025": 64256000, "FY2024": 67551000, "FY2023": 59632000, "FY2022": 48310000, "FY2021": 47915000}
TREA_USD = {"FY2025": 368569000, "FY2024": 350177000, "FY2023": 287662000, "FY2022": 237643000, "FY2021": 248258000}
LEV_EXP_USD = {"FY2025": 620401000, "FY2024": 376611000, "FY2023": 486253000, "FY2022": 543896000, "FY2021": 424021000}
HQLA_USD = {"FY2025": 149895000, "FY2024": 159598000, "FY2023": 194868000, "FY2022": 194898000, "FY2021": 127551000}
NSFR_AVAIL_USD = {"FY2025": 293158000, "FY2024": 264324000, "FY2023": 185387000, "FY2022": 225966000, "FY2021": 191843000}
NSFR_REQ_USD = {"FY2025": 187805000, "FY2024": 159601000, "FY2023": 106823000, "FY2022": 131535000, "FY2021": 93529000}

CET1_RATIO = {y: f"{CET1_USD[y] / TREA_USD[y] * 100:.2f}%" for y in YEARS}
TOTALCAP_RATIO = {y: f"{TOTALCAP_USD[y] / TREA_USD[y] * 100:.2f}%" for y in YEARS}
LEVERAGE_RATIO = {"FY2025": "8.81%", "FY2024": "14.73%", "FY2023": "10.29%", "FY2022": "7.41%", "FY2021": "10.12%"}
LCR_RATIO = {"FY2025": "273%", "FY2024": "333%", "FY2023": "729%", "FY2022": "513%", "FY2021": "371%"}
NSFR_RATIO = {"FY2025": "157%", "FY2024": "166%", "FY2023": "174%", "FY2022": "179%", "FY2021": "206%"}

TIER1_NOTE = (
    "Not publicly disclosed as a separate line - the Bank's 'Key Regulatory Metrics' table only gives "
    "Common Equity Tier 1 (CET1) Capital and Total Capital, with no separate Tier 1 breakdown. Total "
    "Capital exceeds CET1 in every year shown (e.g. FY2025: $64,256k vs $54,656k), confirming some "
    "Additional Tier 1 and/or Tier 2 capital exists, but it isn't broken out - NOT assumed equal to CET1."
)
MREL_NOTE = (
    "Not publicly disclosed in any of the 5 years' Pillar 3 Disclosures reviewed - no MREL figure or "
    "exemption statement found."
)

metric("CET1 Capital", "£'000 (conv. from USD)", [("Common Equity Tier 1 (CET1) Capital", stock(CET1_USD))], p3_sources())
metric("CET1 Ratio", "% of TREA (calculated - see note)", [("CET1 Ratio", CET1_RATIO)], p3_sources(),
       note="CALCULATED as CET1 Capital / Total Risk-Weighted exposure amount (TREA) for each year - "
            "neither the Bank's Annual Report nor its Pillar 3 Disclosures state a CET1 ratio % directly, "
            "only the underlying £/$ amounts (see CET1 Capital and Total RWAs sheets).")
bw.add_not_disclosed_metric_sheets(["Tier 1 Capital", "Tier 1 Ratio"], p3_sources(), per_note={"Tier 1 Capital": TIER1_NOTE, "Tier 1 Ratio": TIER1_NOTE})
metric("Total Capital", "£'000 (conv. from USD)", [("Total Capital", stock(TOTALCAP_USD))], p3_sources())
metric("Total Capital Ratio", "% of TREA (calculated - see note)", [("Total Capital Ratio", TOTALCAP_RATIO)], p3_sources(),
       note="CALCULATED as Total Capital / Total Risk-Weighted exposure amount (TREA) for each year - "
            "not directly stated as a percentage in the source (see CET1 Ratio sheet for the same caveat).")
metric("Total RWAs", "£'000 (conv. from USD)", [("Total Risk-Weighted exposure amount (TREA)", stock(TREA_USD))], p3_sources())
metric("Leverage Ratio", "%", [("Leverage Ratio", LEVERAGE_RATIO)], p3_sources())
metric("LCR", "% (12-month average - see methodology note)", [("Liquidity Coverage Ratio", LCR_RATIO)], p3_sources())
metric("NSFR", "% (4-quarter average - see methodology note)", [("Net Stable Funding Ratio", NSFR_RATIO)], p3_sources())
bw.add_not_disclosed_metric_sheets(["MREL Ratio"], p3_sources(), per_note={"MREL Ratio": MREL_NOTE})

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash flows from operating activities", flow(_usd_by_label["Net cash flows from operating activities"])),
        ("Net cash flows from investing activities", flow(_usd_by_label["Net cash flows from investing activities"])),
        ("Net cash flows from financing activities", flow(_usd_by_label["Net cash flows from financing activities"])),
        ("Cash and cash equivalents at 31 December", stock(_usd_by_label["Cash and cash equivalents at 31 December"])),
    ],
    cash_flow_unit="£'000 (conv. from USD)",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Total Capital Ratio", TOTALCAP_RATIO),
        ("Leverage Ratio", LEVERAGE_RATIO),
        ("LCR", LCR_RATIO),
        ("NSFR", NSFR_RATIO),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. Cash flow and capital figures converted from USD - "
         "see the Cash Flow Statement sheet's source note for the FX methodology and exact rates used.",
)

bw.save("/Users/armaan/code/katalysis/banks/FCMB UK FINANCIALS.xlsx")
