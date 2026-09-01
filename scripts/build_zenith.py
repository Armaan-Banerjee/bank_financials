import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}
PREV_YEAR = {"FY2021": "FY2020", "FY2022": "FY2021", "FY2023": "FY2022", "FY2024": "FY2023", "FY2025": "FY2024"}

# ---------------------------------------------------------------
# FX conversion (Zenith Bank UK reports in USD; converting to £ per this
# project's established FX methodology - see build_smbc.py precedent).
# Rates are Bank of England GBP/USD spot/average via poundsterlinglive.com's
# published archive, £1 = $X.
# ---------------------------------------------------------------
FX_SPOT = {
    "FY2020": 1.3661,  # 31 Dec 2020 - only used for FY2021's opening cash balance
    "FY2021": 1.3521,  # 31 Dec 2021
    "FY2022": 1.2097,  # 30 Dec 2022 (31st was a Saturday)
    "FY2023": 1.2732,  # 29 Dec 2023 (31st was a Sunday)
    "FY2024": 1.2515,  # 31 Dec 2024
    "FY2025": 1.3448,  # 31 Dec 2025
}
FX_AVG = {
    "FY2021": 1.3752,
    "FY2022": 1.2362,
    "FY2023": 1.2439,
    "FY2024": 1.2782,
    "FY2025": 1.3193,
}


def flow(usd):
    """Flow (cash flow statement line item) figures, £'000, at that year's average rate."""
    return {y: round(v / FX_AVG[y] / 1000, 1) for y, v in usd.items()}


def stock(usd):
    """Point-in-time (balance/capital) figures, £'000, at that year's period-end spot rate."""
    return {y: round(v / FX_SPOT[y] / 1000, 1) for y, v in usd.items()}


def opening_cash(usd):
    """Opening cash balance, £'000 - uses the PRIOR year's period-end spot rate (it's the
    same balance as that prior year's closing figure, so must convert identically)."""
    return {y: round(v / FX_SPOT[PREV_YEAR[y]] / 1000, 1) for y, v in usd.items()}


def pct(usd_strings):
    """Ratios are NOT converted - dimensionless and currency-invariant."""
    return usd_strings

# ---------------------------------------------------------------
# Source documents
# ---------------------------------------------------------------
BASE = "https://www.zenith-bank.co.uk/media"
AR2024_URL = f"{BASE}/2273/2024-annual-report-and-financial-statements.pdf"
AR2023_URL = f"{BASE}/2253/2023-annual-report-and-financial-statements.pdf"
AR2022_URL = f"{BASE}/2237/2022-annual-report-and-financial-statements.pdf"
AR2021_URL = f"{BASE}/2205/2021-annual-report-and-financial-statements.pdf"

P3_2025_URL = f"{BASE}/2290/pillar-3-zbuk-31dec25.pdf"
P3_2024_URL = f"{BASE}/2274/31dec24-pillar-3-zbuk.pdf"
P3_2023_URL = f"{BASE}/2260/pillar-3-31dec23-final.pdf"
P3_2022_URL = f"{BASE}/2238/zbuk-31dec22-pillar-3-disclosures.pdf"
P3_2021_URL = f"{BASE}/2228/31dec21-pillar-3.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Zenith Bank (UK) Limited (FRN 451720) is a UK subsidiary of Zenith Bank Plc (Nigeria). Unlike "
    "several other foreign-subsidiary banks in this workbook series (ICICI Bank UK, Philippine National Bank "
    "Europe, Citibank UK, State Bank of India UK), it prepares full financial statements under UK-adopted "
    "International Accounting Standards (not FRS 101/102 reduced disclosure), including a genuine Statement of "
    "Cash Flows every year - no cash-flow exemption applies. The Bank's own capital structure is CET1-only (no "
    "AT1 or Tier 2 instruments), so CET1 capital = Tier 1 capital = Total capital in every year shown."
)

FX_NOTE = (
    "FX CONVERSION NOTE: Zenith Bank (UK) Limited reports in US Dollars. This workbook converts every $ amount to "
    "£ for consistency with the rest of this series, following the same methodology established for SMBC Bank "
    "International plc: point-in-time/balance figures (capital, RWA, leverage exposure, HQLA, cash balances) use "
    "the Bank of England GBP/USD SPOT rate as at that fiscal year-end (31 December); flow figures (every cash "
    "flow statement line item) use the AVERAGE of Bank of England rates over that calendar year - both via "
    "poundsterlinglive.com's published Bank of England archive. Rates used (£1 = $X): 31 Dec 2020 spot 1.3661 "
    "(FY2021 opening cash only); FY2021 spot 1.3521 / average 1.3752; FY2022 spot 1.2097 / average 1.2362; "
    "FY2023 spot 1.2732 / average 1.2439; FY2024 spot 1.2515 / average 1.2782; FY2025 spot 1.3448 / average "
    "1.3193. All % ratios (CET1/Tier 1/Total Capital/Leverage/LCR/NSFR ratios) are shown EXACTLY as reported in "
    "USD and were NOT converted - a ratio is dimensionless and currency-invariant. Because stocks and flows are "
    "converted at different rates, the cash flow statement includes an explicit 'Effect of GBP/USD translation' "
    "reconciling line so opening + all flows + this line = closing exactly in £ terms - this line is purely an "
    "artefact of £ translation and has no bearing on the Bank's underlying USD results. This conversion was not "
    "explicitly requested for this bank (unlike SMBC) - applied for consistency with the rest of the series; "
    "flag if £'000 rather than the Bank's native US$'000 presentation is not what's wanted here."
)

RESTATEMENT_NOTE = (
    "RESTATEMENT NOTE: FY2023's own Annual Report cash flow figures (used for FY2023's column here) differ "
    "slightly from the 'restated' FY2023 comparative shown in the FY2024 Annual Report (e.g. operating activities "
    "$(344,220,013) as originally reported vs $(346,336,139) restated) - both report the same $276,069,567 "
    "closing balance, so the restatement is a reclassification between line items, not a change to overall cash "
    "movement. FY2023's own as-originally-reported figures are used throughout, consistent with this project's "
    "convention of preferring each year's own report over a later restated comparative."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Zenith Bank (UK) Limited's own Statement of Cash Flows (converted from USD to £, "
    "see FX conversion note below):\n"
    f"FY2024: Annual Report and Financial Statements 2024, p.44-45 (Statement of Cash Flows) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.36 (Statement of Cash Flows) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2022, p.34 (Statement of Cash Flows) - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021, p.32 (Statement of Cash Flows) - {AR2021_URL}\n"
    "FY2025 cash flow is blank: no FY2025 Annual Report has been published yet (only the FY2025 Pillar 3 "
    "disclosure is out so far) - Pillar 3 sheets are fully populated for FY2025.\n"
    "Note: FY2021's own report presents operating cash flow more simply than later years - net interest is not "
    "separately reversed out of profit and re-added on a cash basis (no 'Interest income'/'Interest expense' "
    "adjustment lines, no 'Interest income received'/'Interest expense paid' cash lines); FY2022 onward introduced "
    "this more granular presentation. Blank cells for FY2021 on those rows reflect this, not missing data.\n"
    "Activity-total rows may be off by up to £0.2k from summing the visible line items above them, since each £ "
    "line is independently rounded to 1 decimal place before summing; the full statement ties exactly end-to-end "
    "via the net change, opening balance, exchange-rate-effect and translation-effect lines (verified to the "
    "penny in £'000 terms for all 4 populated years).\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE + "\n\n" + RESTATEMENT_NOTE
)


def p3_sources():
    return (
        "Sources - Zenith Bank (UK) Limited Pillar 3 Disclosures (UK KM1 - Key Metrics), converted from USD to £ "
        "where a $ amount (see FX conversion note on the Cash Flow Statement sheet; % ratios are unconverted):\n"
        f"FY2025: Pillar 3 Disclosures as at 31 Dec 2025, p.16 (Section 10, Key Metrics) - {P3_2025_URL}\n"
        f"FY2024: Pillar 3 Disclosures as at 31 Dec 2024, p.17 (Section 9, Key Metrics) - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures as at 31 Dec 2023, p.17 (Section 9, Key Metrics) - {P3_2023_URL}\n"
        f"FY2022: Pillar 3 Disclosures as at 31 Dec 2022, p.24 (Section 10, Key Metrics) - {P3_2022_URL}\n"
        f"FY2021: Pillar 3 Disclosures as at 31 Dec 2021, p.23 (Section 10, Key Metrics) - {P3_2021_URL}"
    )


bw = BankWorkbook(bank_name="Zenith Bank (UK) Limited", years=YEARS, year_label=YEAR_LABEL, header_color="2A3E5C")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (raw USD, then converted via flow()/stock()/opening_cash())
# ---------------------------------------------------------------
rows_usd = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit for the year", {"FY2024": 42223349, "FY2023": 54837411, "FY2022": 35200687, "FY2021": 11404135}),
    ("DATA", "Impairment provision charge/(reversal)", {"FY2024": -8225131, "FY2023": 771074, "FY2022": 5269233, "FY2021": 3692274}),
    ("DATA", "Depreciation of property and equipment", {"FY2024": 1184560, "FY2023": 1074768, "FY2022": 1131020, "FY2021": 1114950}),
    ("DATA", "Amortisation of intangible assets", {"FY2024": 499549, "FY2023": 550153, "FY2022": 543784, "FY2021": 662113}),
    ("DATA", "Interest expense on Right-of-use lease obligations", {"FY2024": 346769, "FY2023": 18326, "FY2021": 49200}),
    ("DATA", "Recoveries of bad debts written off", {"FY2022": -69063}),
    ("DATA", "Current income tax expense", {"FY2024": 13553590, "FY2023": 17745025, "FY2022": 9439732, "FY2021": 2232071}),
    ("DATA", "Deferred income tax expense", {"FY2024": 477928, "FY2023": 211215, "FY2022": 239806}),
    ("DATA", "Foreign currency translation gain - Right-of-use assets", {"FY2021": -211646}),
    ("DATA", "Foreign currency translation gain/(loss) - Lease obligation", {"FY2023": 110592, "FY2022": -317849, "FY2021": -307066}),
    ("DATA", "Foreign currency translation gain - Deferred tax assets", {"FY2022": 45}),
    ("DATA", "Foreign currency translation (gain)/loss - Corporation tax liability", {"FY2023": -123381, "FY2022": -43758, "FY2021": -2756}),
    ("DATA", "Deferred tax asset write-off (legacy)", {"FY2023": 1278}),
    ("DATA", "Impairment on equity investments", {"FY2021": 66644}),
    ("DATA", "Interest income", {"FY2024": -150477684, "FY2023": -148015884, "FY2022": -78988040}),
    ("DATA", "Interest expense", {"FY2024": 69789692, "FY2023": 51768873, "FY2022": 14995830}),
    ("DATA", "Fair value movement on securities measured at FVTPL", {"FY2024": 69201}),
    ("DATA", "Fair value movement on derivative contracts", {"FY2024": 3457754}),
    ("DATA", "Unrealised foreign exchange (gains)/losses", {"FY2024": -2466206}),
    ("DATA", "Loss on derecognition of assets", {"FY2024": 7486009}),
    ("DATA", "Decrease/(Increase) in loans and advances to banks", {"FY2024": 37241172, "FY2023": 17720794, "FY2022": -16995457, "FY2021": 29588441}),
    ("DATA", "(Increase)/Decrease in loans and advances to customers", {"FY2024": -92041493, "FY2023": -37968440, "FY2022": 39931143, "FY2021": -196507247}),
    ("DATA", "(Increase)/Decrease in securities measured at fair value through profit or loss", {"FY2024": -120096, "FY2023": -1751539, "FY2022": 6591830, "FY2021": 525737}),
    ("DATA", "Decrease/(Increase) in securities measured at FVOCI", {"FY2024": 314536239, "FY2023": 155867577, "FY2022": -568931339, "FY2021": -313837082}),
    ("DATA", "(Increase)/Decrease in other assets", {"FY2024": -4408211, "FY2023": -1265435, "FY2022": 135997, "FY2021": -577710}),
    ("DATA", "(Decrease)/Increase in deposits from banks", {"FY2024": -7577015, "FY2023": -688088465, "FY2022": 79243126, "FY2021": 600568191}),
    ("DATA", "(Decrease)/Increase in deposits from customers", {"FY2024": -104968633, "FY2023": 200100437, "FY2022": 123837261, "FY2021": -74898564}),
    ("DATA", "Increase/(Decrease) in repurchase agreements and other similar secured borrowing", {"FY2024": 43001229, "FY2023": -30579358, "FY2022": 30379006, "FY2021": 45573102}),
    ("DATA", "(Increase)/Decrease in derivative financial instruments (net)", {"FY2023": -118861, "FY2022": -389643, "FY2021": 5839211}),
    ("DATA", "Increase/(Decrease) in other liabilities", {"FY2024": 4871782, "FY2023": -9720985, "FY2022": 9795677, "FY2021": 2836076}),
    ("DATA", "Interest income received", {"FY2024": 104041078, "FY2023": 136365040, "FY2022": 86951488}),
    ("DATA", "Interest expense paid", {"FY2024": -53649527, "FY2023": -44315715, "FY2022": -12499405}),
    ("DATA", "Income tax paid", {"FY2024": -11483449, "FY2023": -19414513, "FY2022": -9210907, "FY2021": -1768909}),
    ("TOTAL", "Net cash generated from/(used in) operating activities", {"FY2024": 207362455, "FY2023": -344220013, "FY2022": -243759796, "FY2021": 116041165}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Acquisition of securities measured at amortised cost", {"FY2024": -81087234, "FY2023": -26729752, "FY2022": -47624983, "FY2021": -42913212}),
    ("DATA", "Proceeds from redemption of securities measured at amortised cost", {"FY2024": 69818444, "FY2023": 21071506, "FY2022": 27641163, "FY2021": 32279901}),
    ("DATA", "Interest income received (investing)", {"FY2024": 14053675, "FY2023": 15202064, "FY2022": 17837082}),
    ("DATA", "Acquisition of property and equipment", {"FY2024": -62128, "FY2023": -60188, "FY2022": -26331, "FY2021": -34354}),
    ("DATA", "Additions to Right-of-use assets", {"FY2021": -46639}),
    ("DATA", "Acquisition of intangible assets", {"FY2024": -2173626, "FY2023": -328438, "FY2022": -491577, "FY2021": -312642}),
    ("TOTAL", "Net cash generated from/(used in) investing activities", {"FY2024": 549131, "FY2023": 9155192, "FY2022": -2664646, "FY2021": -11026946}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Repayment of lease liability/obligation", {"FY2024": -672177, "FY2023": -926335, "FY2022": -824165, "FY2021": -1084238}),
    ("DATA", "Addition of new lease obligation", {"FY2021": 46639}),
    ("DATA", "Dividends paid to shareholders", {"FY2023": -17600000, "FY2022": -5700000, "FY2021": -8955674}),
    ("TOTAL", "Net cash generated from/(used in) financing activities", {"FY2024": -672177, "FY2023": -18526335, "FY2022": -6524165, "FY2021": -9993273}),
    ("TOTAL", "Net (decrease)/increase of cash and cash equivalents", {"FY2024": 207239409, "FY2023": -353591156, "FY2022": -252948607, "FY2021": 95020946}),
    ("DATA", "Cash and cash equivalents as at 1 January", {"FY2024": 276069567, "FY2023": 629660723, "FY2022": 882609330, "FY2021": 787588384}),
    ("DATA", "Effect of exchange rate changes on cash and cash equivalents (as reported, USD)", {"FY2024": -3075636}),
    ("TOTAL", "Cash and cash equivalents at 31 December", {"FY2024": 480233340, "FY2023": 276069567, "FY2022": 629660723, "FY2021": 882609330}),
]

# convert: SECTION rows pass through unchanged; opening-cash uses opening_cash()
# (prior year's spot rate); closing cash uses stock() (this year's spot rate) since
# it's a point-in-time balance, NOT a flow; everything else (DATA/TOTAL) uses flow().
_usd_by_label = {label: usd for _, label, usd in rows_usd}
rows = []
for kind, label, usd in rows_usd:
    if kind == "SECTION":
        rows.append((kind, label, {}))
    elif label == "Cash and cash equivalents as at 1 January":
        rows.append((kind, label, opening_cash(usd)))
    elif label == "Cash and cash equivalents at 31 December":
        rows.append((kind, label, stock(usd)))
    else:
        rows.append((kind, label, flow(usd)))
    if label == "Effect of exchange rate changes on cash and cash equivalents (as reported, USD)":
        # £ translation plug (see FX_NOTE): stocks (opening/closing) and flows
        # (everything else) are converted at different rates, so the £ statement
        # needs an explicit reconciling line to tie exactly. Computed programmatically
        # as closing(£) - opening(£) - net change(£) - reported FX-effect(£), per year,
        # rather than hardcoded, so it can never drift out of sync with the rates above.
        opening_gbp = opening_cash(_usd_by_label["Cash and cash equivalents as at 1 January"])
        closing_gbp = stock(_usd_by_label["Cash and cash equivalents at 31 December"])
        net_change_gbp = flow(_usd_by_label["Net (decrease)/increase of cash and cash equivalents"])
        fx_gbp = flow(usd)
        plug = {
            y: round(closing_gbp[y] - opening_gbp[y] - net_change_gbp[y] - fx_gbp.get(y, 0), 1)
            for y in closing_gbp
        }
        rows.append(("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", plug))

bw.add_cash_flow_sheet(
    title="Zenith Bank (UK) Limited — Statement of Cash Flows",
    subtitle="£'000, converted from USD - see source note at bottom for FX methodology and rates used. FY2025 blank (no FY2025 Annual Report yet).",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=76,
    source_height=320,
    unit_suffix=" (£'000, conv. from USD)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=48, source_height=120)


CET1_TIER1_TOTAL_USD = {"FY2025": 431376, "FY2024": 378325, "FY2023": 338086, "FY2022": 290721, "FY2021": 281088}
RWA_USD = {"FY2025": 1843312, "FY2024": 1475750, "FY2023": 1167888, "FY2022": 1125146, "FY2021": 1352803}

metric("CET1 Capital", "£'000 (conv. from USD)", [("Common Equity Tier 1 (CET1) capital", stock(CET1_TIER1_TOTAL_USD))], p3_sources())
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "23.40%", "FY2024": "25.64%", "FY2023": "28.95%", "FY2022": "25.84%", "FY2021": "20.78%"})], p3_sources())
metric("Tier 1 Capital", "£'000 (conv. from USD)", [("Tier 1 capital", stock(CET1_TIER1_TOTAL_USD))], p3_sources(),
       note="Equal to CET1 capital in every year - the Bank holds no Additional Tier 1 (AT1) instruments.")
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {"FY2025": "23.40%", "FY2024": "25.64%", "FY2023": "28.95%", "FY2022": "25.84%", "FY2021": "20.78%"})], p3_sources())
metric("Total Capital", "£'000 (conv. from USD)", [("Total capital", stock(CET1_TIER1_TOTAL_USD))], p3_sources(),
       note="Equal to CET1/Tier 1 capital in every year - the Bank holds no AT1 or Tier 2 instruments.")
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2025": "23.40%", "FY2024": "25.64%", "FY2023": "28.95%", "FY2022": "25.84%", "FY2021": "20.78%"})], p3_sources())
metric("Total RWAs", "£'000 (conv. from USD)", [("Total risk-weighted exposure amount", stock(RWA_USD))], p3_sources(),
       note="FY2023's figure (own report, £m equivalent of $1,167,888k) differs from the FY2024 report's restated FY2023 "
            "comparative ($1,203,364k) - a Basic Indicator Approach operational-risk methodology update. FY2023's own "
            "report figure is used, consistent with this project's convention of preferring each year's own report.")

metric(
    "Leverage Ratio", "£'000 / % (conv. from USD)",
    [
        ("Total exposure measure excluding claims on central banks", stock({"FY2025": 3171798, "FY2024": 2987483, "FY2023": 2872422, "FY2022": 3409175, "FY2021": 3219954})),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "12.08%", "FY2024": "11.25%", "FY2023": "9.76%", "FY2022": "7.32%", "FY2021": "8.36%"}),
    ],
    p3_sources(),
)

metric(
    "LCR", "£'000 / % (conv. from USD)",
    [
        ("Total high-quality liquid assets (HQLA), weighted value", stock({"FY2025": 952538, "FY2024": 1013789, "FY2023": 1147653, "FY2022": 1227530, "FY2021": 932821})),
        ("Total net cash outflows, adjusted value", stock({"FY2025": 352543, "FY2024": 306820, "FY2023": 369648, "FY2022": 374822, "FY2021": 337730})),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "270.19%", "FY2024": "330.42%", "FY2023": "310%", "FY2022": "343%", "FY2021": "276%"}),
    ],
    p3_sources(),
    note="LCR methodology changed across vintages: FY2021 is a point-in-time (year-end) figure as originally "
         "disclosed; FY2022 onward is a 12-month simple average, per each year's own report. FY2022's own report "
         "(374,822k/343%) differs from the FY2023 report's restated FY2022 comparative (348,210k/352%) - FY2022's "
         "own report figure is used, per this project's convention.",
)

metric(
    "NSFR", "£'000 / % (conv. from USD)",
    [
        ("Total available stable funding", stock({"FY2025": 1316936, "FY2024": 1136904, "FY2023": 1066880, "FY2022": 912816})),
        ("Total required stable funding", stock({"FY2025": 948441, "FY2024": 768308, "FY2023": 744377, "FY2022": 735763})),
        ("Net Stable Funding Ratio (%)", {"FY2025": "138.85%", "FY2024": "147.98%", "FY2023": "143%", "FY2022": "124%", "FY2021": "Not disclosed"}),
    ],
    p3_sources(),
    note="The UK NSFR was adopted from 1 January 2022 (per the FY2021 and FY2022 Pillar 3 reports), so no FY2021 "
         "figures exist.",
)

bw.add_not_disclosed_metric_sheets(["MREL Ratio"], p3_sources(),
    per_note={"MREL Ratio": "No MREL disclosure (numeric or qualitative) or UK KM2 template found in any year's "
                             "Pillar 3 report - not explicitly stated as an exemption, but consistent with the "
                             "Bank's small size relative to typical MREL-in-scope thresholds."})

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
cf_totals_usd = {
    "Net cash generated from/(used in) operating activities": {"FY2024": 207362455, "FY2023": -344220013, "FY2022": -243759796, "FY2021": 116041165},
    "Net cash generated from/(used in) investing activities": {"FY2024": 549131, "FY2023": 9155192, "FY2022": -2664646, "FY2021": -11026946},
    "Net cash generated from/(used in) financing activities": {"FY2024": -672177, "FY2023": -18526335, "FY2022": -6524165, "FY2021": -9993273},
}
cf_close_usd = {"FY2024": 480233340, "FY2023": 276069567, "FY2022": 629660723, "FY2021": 882609330}

bw.add_overview_sheet(
    cash_flow_totals=[(label, flow(vals)) for label, vals in cf_totals_usd.items()]
                      + [("Cash and cash equivalents at end of year", stock(cf_close_usd))],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "23.40%", "FY2024": "25.64%", "FY2023": "28.95%", "FY2022": "25.84%", "FY2021": "20.78%"}),
        ("Tier 1 Ratio", {"FY2025": "23.40%", "FY2024": "25.64%", "FY2023": "28.95%", "FY2022": "25.84%", "FY2021": "20.78%"}),
        ("Total Capital Ratio", {"FY2025": "23.40%", "FY2024": "25.64%", "FY2023": "28.95%", "FY2022": "25.84%", "FY2021": "20.78%"}),
        ("Leverage Ratio", {"FY2025": "12.08%", "FY2024": "11.25%", "FY2023": "9.76%", "FY2022": "7.32%", "FY2021": "8.36%"}),
        ("LCR", {"FY2025": "270.19%", "FY2024": "330.42%", "FY2023": "310%", "FY2022": "343%", "FY2021": "276%"}),
        ("NSFR", {"FY2025": "138.85%", "FY2024": "147.98%", "FY2023": "143%", "FY2022": "124%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation. All £ figures are converted from the Bank's native USD reporting (see Cash Flow Statement "
         "sheet's FX conversion note) - this conversion was not explicitly requested for this bank but applied for "
         "consistency with the rest of the series. FY2025 cash flow is blank (no FY2025 Annual Report published "
         "yet); Pillar 3 is fully populated for FY2025.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/ZENITH FINANCIALS.xlsx")
