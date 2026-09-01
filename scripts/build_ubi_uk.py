import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, year ended 31 March
YEAR_LABEL = {y: y for y in YEARS}
PREV_YEAR = {"FY2021": "FY2020", "FY2022": "FY2021", "FY2023": "FY2022", "FY2024": "FY2023", "FY2025": "FY2024"}

# ---------------------------------------------------------------
# FX conversion (Union Bank of India (UK) Limited reports in USD; converting
# to £ per this project's established methodology - see build_smbc.py/
# build_zenith.py precedent). Same 31 March year-ends as SMBC Bank
# International, so the same Bank of England GBP/USD spot/average rates
# apply (via poundsterlinglive.com's published archive), £1 = $X.
# ---------------------------------------------------------------
FX_SPOT = {
    "FY2020": 1.2403,  # 31 Mar 2020 - only used for FY2021's opening cash balance
    "FY2021": 1.3796,
    "FY2022": 1.3162,
    "FY2023": 1.2364,
    "FY2024": 1.2632,
    "FY2025": 1.2910,
}
FX_AVG = {
    "FY2021": 1.3193,
    "FY2022": 1.3617,
    "FY2023": 1.2043,
    "FY2024": 1.2581,
    "FY2025": 1.2775,
}


def flow(usd):
    """Flow (cash flow statement line item) figures, £'000, at that year's average rate.
    Input values are already in USD '000 (per the source documents), so no /1000 here."""
    return {y: round(v / FX_AVG[y], 1) for y, v in usd.items()}


def stock(usd):
    """Point-in-time (balance/capital) figures, £'000, at that year's period-end spot rate.
    Input values are already in USD '000 (per the source documents), so no /1000 here."""
    return {y: round(v / FX_SPOT[y], 1) for y, v in usd.items()}


def opening_cash(usd):
    """Opening cash balance, £'000 - uses the PRIOR year's period-end spot rate (it's
    the same balance as that prior year's closing figure, so must convert identically).
    Input values are already in USD '000, so no /1000 here."""
    return {y: round(v / FX_SPOT[PREV_YEAR[y]], 1) for y, v in usd.items()}


# ---------------------------------------------------------------
# Source documents
# ---------------------------------------------------------------
BASE = "https://www.unionbankofindiauk.co.uk/Portals/0/pdf"
AR2025_URL = f"{BASE}/Annual_report_UBI_UK_signed_31-03-2025.pdf"
AR2024_URL = f"{BASE}/Signed_UBI_UK_Annual_Report_28_05.pdf"
AR2023_URL = f"{BASE}/Annual_Report_March_2023_with_Final_Audit_report_24052023-signed.pdf"
AR2022_URL = f"{BASE}/Financial_Statements%20_31-03-2022.pdf"

P3_2025_URL = f"{BASE}/Final_Pillar_3_Disclosure-31-03-2025.pdf"
P3_2024_URL = f"{BASE}/Pillar_3_Disclosures_2024.pdf"
P3_2023_URL = f"{BASE}/Pillar_3_Disclosure_2023.pdf"
P3_2022_URL = f"{BASE}/Pillar_III%20_Disclosures_2021_22.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Union Bank of India (UK) Limited (FRN 601551, Companies House 07653660) is an Indian-owned UK "
    "subsidiary bank (parent: Union Bank of India). Unlike other single-country Indian-subsidiary banks in this "
    "workbook series (ICICI Bank UK, State Bank of India UK - both skipped), this Bank does NOT take the FRS 101/102 "
    "cash-flow-statement exemption - it publishes a genuine Statement of Cash Flows every year. CET1 capital = "
    "Tier 1 capital in every year shown (no AT1 instruments); Total capital also equals CET1/Tier 1 from FY2022 "
    "onward (no Tier 2 instruments), but FY2021 Total capital ($115,017k) exceeds CET1/Tier 1 ($111,081k), implying "
    "the Bank held Tier 2 capital that year which had run off by FY2022. FY2021 cash flow figures are sourced from "
    "the FY2022 Annual Report's own comparative column (no dedicated FY2021 report was fetched), consistent with "
    "this project's practice of using the earliest practically available presentation of a year's figures."
)

FX_NOTE = (
    "FX CONVERSION NOTE: Union Bank of India (UK) Limited reports in US Dollars. This workbook converts every $ "
    "amount to £, following the same methodology established for SMBC Bank International plc and Zenith Bank (UK) "
    "Limited: point-in-time/balance figures (capital, RWA, leverage exposure, HQLA, cash balances) use the Bank of "
    "England GBP/USD SPOT rate as at that fiscal year-end (31 March); flow figures (every cash flow statement line "
    "item) use the AVERAGE Bank of England rate over that fiscal year - both via poundsterlinglive.com's published "
    "Bank of England archive (same rate table as SMBC Bank International plc, which shares the same 31 March "
    "year-end). Rates used (£1 = $X): 31 Mar 2020 spot 1.2403 (FY2021 opening cash only); FY2021 spot 1.3796 / "
    "average 1.3193; FY2022 spot 1.3162 / average 1.3617; FY2023 spot 1.2364 / average 1.2043; FY2024 spot 1.2632 / "
    "average 1.2581; FY2025 spot 1.2910 / average 1.2775. All % ratios (CET1/Tier 1/Total Capital/Leverage/LCR/NSFR "
    "ratios) are shown EXACTLY as reported in USD and were NOT converted - a ratio is dimensionless and "
    "currency-invariant. This conversion was not explicitly requested for this specific bank but applied for "
    "consistency with the rest of the series (per the user's standing instruction on this batch of banks); flag if "
    "£'000 rather than the Bank's native US$'000 presentation is not what's wanted here."
)

PRESENTATION_NOTE = (
    "PRESENTATION NOTE: this Bank's own statement presents 'Cash flows before changes in working capital' (or "
    "'...operating activities' in FY2021/FY2022) as the sum of the adjustment lines ONLY - it deliberately excludes "
    "'(Loss)/profit before tax for the year', which is carried forward separately and only folded in at the final "
    "'Net cash flows from/(used in) operating activities' total (verified: profit before tax + adjustments subtotal "
    "+ working capital change + loans/deposits movements = the operating total, exactly, in every year). A generic "
    "block-sum check that includes the profit-before-tax line together with the adjustment lines above that "
    "subtotal will therefore show an apparent mismatch equal to the profit/(loss) before tax figure - this is a "
    "structural feature of the source document's own layout, not a data error."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Union Bank of India (UK) Limited's own Statement of Cash Flows (converted from USD "
    "to £, see FX conversion note below):\n"
    f"FY2025: Annual Report and Financial Statements, year ended 31 March 2025, p.35 (Statement of Cash Flows) - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements, year ended 31 March 2024, p.28 (Statement of Cash Flows) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements, year ended 31 March 2023, p.27 (Statement of Cash Flows) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements, year ended 31 March 2022, p.35 (Statement of Cash Flows) - {AR2022_URL}\n"
    f"FY2021: as presented in the FY2022 Annual Report's own comparative column (p.35) - {AR2022_URL}\n"
    "Note: FY2023's own report's FY2022 comparative figures for the operating/investing/financing subtotals differ "
    "from FY2022's own report (e.g. operating activities $(31,909)k restated vs $(30,053)k as originally reported) "
    "- a reclassification between activity categories, not a change to the overall cash movement (both agree the "
    "year-end balance was $5,170k). FY2022's own as-originally-reported figures are used throughout, per this "
    "project's convention of preferring each year's own report over a later restated comparative.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE + "\n\n" + PRESENTATION_NOTE
)


def p3_sources():
    return (
        "Sources - Union Bank of India (UK) Limited Pillar 3 Disclosures (UK KM1 - Key metrics / prudential "
        "regulatory metrics table), converted from USD to £ where a $ amount (see FX conversion note on the Cash "
        "Flow Statement sheet; % ratios are unconverted):\n"
        f"FY2025: Pillar 3 Disclosure 2024-25, p.9 (UK KM1 - Key metrics) - {P3_2025_URL}\n"
        f"FY2024: Pillar 3 Disclosure 2023-24, p.9 (UK KM1 - Key metrics) - {P3_2024_URL}\n"
        f"FY2023: Pillar III Disclosure 2022-23, p.9 (UK KM1 - Key metrics) - {P3_2023_URL}\n"
        f"FY2022: Pillar 3 Disclosure 2022, p.28 (3.4 Bank's prudential regulatory metrics) - {P3_2022_URL}\n"
        f"FY2021: as presented in the FY2022 Pillar 3 Disclosure's own comparative column (p.28) - {P3_2022_URL}"
    )


bw = BankWorkbook(bank_name="Union Bank of India (UK) Limited", years=YEARS, year_label=YEAR_LABEL, header_color="0F5B78")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (raw USD, converted via flow()/stock()/opening_cash())
# ---------------------------------------------------------------
rows_usd = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "(Loss)/profit before tax for the year", {"FY2025": -6608, "FY2024": 1488, "FY2023": 1866, "FY2022": 5273, "FY2021": -10939}),
    ("DATA", "Interest Income", {"FY2025": -32247, "FY2024": -31029, "FY2023": -19884}),
    ("DATA", "Interest Expense", {"FY2025": 19934, "FY2024": 16852, "FY2023": 6912}),
    ("DATA", "Impairment loss allowances", {"FY2025": 10245, "FY2024": 5593, "FY2023": 5066}),
    ("DATA", "Amortisation of intangible non-current asset", {"FY2025": 57, "FY2024": 62, "FY2023": 83, "FY2022": 99, "FY2021": 131}),
    ("DATA", "Depreciation for property, plant and equipment", {"FY2025": 628, "FY2024": 587, "FY2023": 431, "FY2022": 420, "FY2021": 421}),
    ("DATA", "FV movement in derivatives", {"FY2025": -44, "FY2024": -125, "FY2023": 67, "FY2022": -92, "FY2021": -197}),
    ("DATA", "Effects of exchange rate changes on cash and cash equivalents (operating adjustment)", {"FY2025": 126, "FY2024": 122, "FY2023": 148, "FY2022": 33, "FY2021": -5}),
    ("DATA", "FV movement of investments at FVTPL", {"FY2025": 509, "FY2024": -1038}),
    ("DATA", "Finance Charge on Lease", {"FY2025": 247, "FY2024": 166, "FY2023": 10, "FY2022": 24, "FY2021": 38}),
    ("TOTAL", "Cash flows before changes in working capital (excl. profit before tax - see presentation note)", {"FY2025": -545, "FY2024": -8811, "FY2023": -7167, "FY2022": 484, "FY2021": 388}),
    ("DATA", "(Increase)/Decrease in receivables & prepayments", {"FY2025": -599, "FY2024": -702, "FY2023": 747, "FY2022": -545, "FY2021": 4123}),
    ("DATA", "Tax paid", {"FY2022": 0, "FY2021": 0}),
    ("DATA", "(Decrease)/Increase in other liabilities", {"FY2025": -584, "FY2024": 794, "FY2023": -146, "FY2022": -568, "FY2021": 1775}),
    ("TOTAL", "Net change in working capital", {"FY2025": -1183, "FY2024": 92, "FY2023": 601, "FY2022": -1113, "FY2021": 5898}),
    ("DATA", "(Decrease)/Increase in loans and advances to customers", {"FY2025": -8058, "FY2024": -24458, "FY2023": -34904, "FY2022": -30074, "FY2021": -485}),
    ("DATA", "Interest received on loans and advances to customers", {"FY2025": 22391, "FY2024": 22218, "FY2023": 14354}),
    ("DATA", "Decrease/(Increase) in loans and advances to banks", {"FY2025": 22748, "FY2024": 15018, "FY2023": -38776, "FY2022": -11194, "FY2021": 36054}),
    ("DATA", "Interest received on loans and advances to banks", {"FY2025": 3769, "FY2024": 3509, "FY2023": 1464}),
    ("DATA", "Decrease in deposits from Banks", {"FY2022": 0, "FY2021": -21256}),
    ("DATA", "(Decrease)/Increase in deposits from customers", {"FY2025": -37899, "FY2024": 47737, "FY2023": 53780, "FY2022": 4457, "FY2021": 29212}),
    ("DATA", "Interest paid on deposits from customers", {"FY2025": -20076, "FY2024": -8478, "FY2023": -2832}),
    ("DATA", "Decrease/(Increase) in derivative financial instruments - Assets", {"FY2025": 0, "FY2024": 224, "FY2023": -224, "FY2022": 1436, "FY2021": -1436}),
    ("DATA", "Increase/(Decrease) in derivative financial instruments - Liabilities", {"FY2025": 1286, "FY2024": 316, "FY2023": -654, "FY2022": 678, "FY2021": -3013}),
    ("TOTAL", "Net cash generated from/(used in) operating activities", {"FY2025": -24175, "FY2024": 48856, "FY2023": -12492, "FY2022": -30053, "FY2021": 34423}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Disposal/(Acquisition) of Investments - FVOCI", {"FY2022": 18437, "FY2021": -23895}),
    ("DATA", "Acquisition of Investments - FVOCI", {"FY2025": -15132, "FY2024": -24308, "FY2023": -2692}),
    ("DATA", "Proceeds from Investments", {"FY2025": 28142}),
    ("DATA", "Disposal/(Acquisition) of Investments - Amortised cost", {"FY2022": 5533, "FY2021": -5266}),
    ("DATA", "Proceeds from Investments - Amortised cost", {"FY2024": 1892, "FY2023": 4921}),
    ("DATA", "(Acquisition) of Investments - FVTPL", {"FY2023": -782, "FY2022": -133, "FY2021": -1316}),
    ("DATA", "Interest received on Investments", {"FY2025": 3228, "FY2024": 1980, "FY2023": 1698}),
    ("DATA", "Disposal of property, plant and equipment", {"FY2022": 3, "FY2021": 2}),
    ("DATA", "Acquisition of property, plant and equipment", {"FY2025": -12, "FY2024": -1745, "FY2023": -25, "FY2022": -48, "FY2021": -54}),
    ("DATA", "Acquisition of intangible assets", {"FY2025": -4, "FY2023": -64, "FY2022": -151}),
    ("TOTAL", "Net cash generated from/(used in) investing activities", {"FY2025": 16222, "FY2024": -22181, "FY2023": 3056, "FY2022": 23641, "FY2021": -30530}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Proceeds from Intra-group/Inter Bank borrowings", {"FY2023": 35000, "FY2022": 6011}),
    ("DATA", "Repayment of Inter Bank borrowings", {"FY2024": -35000, "FY2023": -6000}),
    ("DATA", "Interest Paid on Inter bank borrowings", {"FY2025": -23, "FY2024": -1880, "FY2023": -124}),
    ("DATA", "Decrease in repurchase agreements", {"FY2022": -74, "FY2021": -3718}),
    ("DATA", "Proceeds from Repurchase agreements", {"FY2025": 15052}),
    ("DATA", "Repayment of Repurchase agreements", {"FY2023": -5145}),
    ("DATA", "Interest Paid on Repurchase agreements", {"FY2025": -656, "FY2023": -29}),
    ("DATA", "Repayment of Lease (Principal amt)", {"FY2025": -435, "FY2024": -193, "FY2023": -432, "FY2022": -448, "FY2021": -402}),
    ("DATA", "Payment of Interest on Lease", {"FY2022": -24, "FY2021": -38}),
    ("TOTAL", "Net cash generated from/(used in) financing activities", {"FY2025": 13938, "FY2024": -37073, "FY2023": 23270, "FY2022": 5465, "FY2021": -4158}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 5985, "FY2024": -10399, "FY2023": 13834, "FY2022": -947, "FY2021": -265}),
    ("DATA", "Cash and cash equivalents at beginning of the year", {"FY2025": 8336, "FY2024": 18856, "FY2023": 5170, "FY2022": 6150, "FY2021": 6410}),
    ("DATA", "Effects of exchange rate changes on cash and cash equivalents (closing bridge)", {"FY2025": -126, "FY2024": -122, "FY2023": -148, "FY2022": -33, "FY2021": 5}),
    ("TOTAL", "Cash and cash equivalents at close of the year", {"FY2025": 14195, "FY2024": 8336, "FY2023": 18856, "FY2022": 5170, "FY2021": 6150}),
]

# £ translation plug (see FX_NOTE): the closing cash balance is a point-in-time
# stock figure, converted at that year-end's own SPOT rate (like the opening
# balance), while everything above it (net change, reported FX-effect line) is
# a flow converted at the AVERAGE rate - so the statement needs an explicit
# reconciling line to tie exactly, per the SMBC/Zenith precedent. Computed
# programmatically (not hand-derived) as closing(spot) - opening(spot) -
# net_change(avg) - reported_FX_effect(avg), per year.
_usd_by_label = {label: usd for _, label, usd in rows_usd}
_closing_spot = stock(_usd_by_label["Cash and cash equivalents at close of the year"])
_opening_spot = opening_cash(_usd_by_label["Cash and cash equivalents at beginning of the year"])
_net_change_avg = flow(_usd_by_label["Net increase/(decrease) in cash and cash equivalents"])
_fx_effect_avg = flow(_usd_by_label["Effects of exchange rate changes on cash and cash equivalents (closing bridge)"])
TRANSLATION_PLUG_GBP = {
    y: round(_closing_spot[y] - _opening_spot[y] - _net_change_avg[y] - _fx_effect_avg[y], 1)
    for y in YEARS
}

rows = []
for kind, label, usd in rows_usd:
    if kind == "SECTION":
        rows.append((kind, label, {}))
    elif label == "Cash and cash equivalents at beginning of the year":
        rows.append((kind, label, opening_cash(usd)))
    elif label == "Cash and cash equivalents at close of the year":
        rows.append(("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", TRANSLATION_PLUG_GBP))
        rows.append((kind, label, stock(usd)))
    else:
        rows.append((kind, label, flow(usd)))

bw.add_cash_flow_sheet(
    title="Union Bank of India (UK) Limited — Statement of Cash Flows",
    subtitle="£'000, converted from USD - see source note at bottom for FX methodology and rates used.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=340,
    unit_suffix=" (£'000, conv. from USD)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=48, source_height=130)


CET1_TIER1_USD = {"FY2025": 111479, "FY2024": 116706, "FY2023": 113622, "FY2022": 113013, "FY2021": 111081}
TOTAL_CAP_USD = {"FY2025": 111479, "FY2024": 116706, "FY2023": 113622, "FY2022": 113013, "FY2021": 115017}
RWA_USD = {"FY2025": 409920, "FY2024": 421729, "FY2023": 385186, "FY2022": 352650, "FY2021": 343147}

metric("CET1 Capital", "£'000 (conv. from USD)", [("Common Equity Tier 1 (CET1) capital", stock(CET1_TIER1_USD))], p3_sources())
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "27.20%", "FY2024": "27.67%", "FY2023": "29.50%", "FY2022": "32.05%", "FY2021": "32.37%"})], p3_sources())
metric("Tier 1 Capital", "£'000 (conv. from USD)", [("Tier 1 capital", stock(CET1_TIER1_USD))], p3_sources(),
       note="Equal to CET1 capital in every year - the Bank holds no Additional Tier 1 (AT1) instruments.")
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {"FY2025": "27.20%", "FY2024": "27.67%", "FY2023": "29.50%", "FY2022": "32.05%", "FY2021": "32.37%"})], p3_sources())
metric("Total Capital", "£'000 (conv. from USD)", [("Total capital", stock(TOTAL_CAP_USD))], p3_sources(),
       note="Equal to CET1/Tier 1 capital from FY2022 onward (no Tier 2 instruments); FY2021 Total capital "
            "($115,017k) exceeds CET1/Tier 1 ($111,081k), implying Tier 2 capital held that year which had run "
            "off by FY2022 (not explicitly explained in the source).")
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2025": "27.20%", "FY2024": "27.67%", "FY2023": "29.50%", "FY2022": "32.05%", "FY2021": "33.52%"})], p3_sources())
metric("Total RWAs", "£'000 (conv. from USD)", [("Total risk-weighted exposure amount", stock(RWA_USD))], p3_sources())

metric(
    "Leverage Ratio", "£'000 / % (conv. from USD)",
    [
        ("Leverage ratio total exposure measure", stock({"FY2025": 496976, "FY2024": 511751, "FY2023": 475110, "FY2022": 411084, "FY2021": 402973})),
        ("Leverage ratio (%)", {"FY2025": "22.43%", "FY2024": "22.81%", "FY2023": "23.92%", "FY2022": "27.49%", "FY2021": "27.57%"}),
    ],
    p3_sources(),
    note="FY2021/FY2022 disclosed on the 'Basel III leverage ratio' basis (per that era's Pillar 3 template); "
         "FY2023 onward uses the 'UK KM1' leverage ratio template. Both are shown on the same row for continuity "
         "since the Bank's own reports do not draw an excluding/including-central-banks distinction in any year.",
)

metric(
    "LCR", "£'000 / % (conv. from USD)",
    [
        ("Total high-quality liquid assets (HQLA), weighted value", stock({"FY2025": 43965, "FY2024": 43840, "FY2023": 48637, "FY2022": 36977, "FY2021": 64886})),
        ("Total net cash outflows, adjusted value", stock({"FY2025": 3017, "FY2024": 4815, "FY2023": 1637, "FY2022": 3888, "FY2021": 4486})),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "1457%", "FY2024": "910%", "FY2023": "2971%", "FY2022": "951%", "FY2021": "1446%"}),
    ],
    p3_sources(),
)

metric(
    "NSFR", "£'000 / % (conv. from USD)",
    [
        ("Total available stable funding", stock({"FY2025": 431914, "FY2024": 412656, "FY2023": 408381, "FY2022": 346323})),
        ("Total required stable funding", stock({"FY2025": 318358, "FY2024": 314809, "FY2023": 282448, "FY2022": 247487})),
        ("Net Stable Funding Ratio (%)", {"FY2025": "136%", "FY2024": "131%", "FY2023": "145%", "FY2022": "140%", "FY2021": "Not disclosed"}),
    ],
    p3_sources(),
    note="The UK NSFR regime took effect from 1 January 2022, so no FY2021 figures exist (consistent with other "
         "banks in this series). FY2022 figures are as presented in the FY2023 Pillar 3 report's own comparative "
         "column (FY2022's own Pillar 3 report predates NSFR disclosure for this Bank).",
)

bw.add_not_disclosed_metric_sheets(["MREL Ratio"], p3_sources(),
    per_note={"MREL Ratio": "No MREL disclosure (numeric or qualitative) or UK KM2 template found in any year's "
                             "Pillar 3 report - consistent with the Bank's small size relative to typical "
                             "MREL-in-scope thresholds."})

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
cf_totals_usd = {
    "Net cash generated from/(used in) operating activities": {"FY2025": -24175, "FY2024": 48856, "FY2023": -12492, "FY2022": -30053, "FY2021": 34423},
    "Net cash generated from/(used in) investing activities": {"FY2025": 16222, "FY2024": -22181, "FY2023": 3056, "FY2022": 23641, "FY2021": -30530},
    "Net cash generated from/(used in) financing activities": {"FY2025": 13938, "FY2024": -37073, "FY2023": 23270, "FY2022": 5465, "FY2021": -4158},
}
cf_close_usd = {"FY2025": 14195, "FY2024": 8336, "FY2023": 18856, "FY2022": 5170, "FY2021": 6150}

bw.add_overview_sheet(
    cash_flow_totals=[(label, flow(vals)) for label, vals in cf_totals_usd.items()]
                      + [("Cash and cash equivalents at end of year", flow(cf_close_usd))],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "27.20%", "FY2024": "27.67%", "FY2023": "29.50%", "FY2022": "32.05%", "FY2021": "32.37%"}),
        ("Tier 1 Ratio", {"FY2025": "27.20%", "FY2024": "27.67%", "FY2023": "29.50%", "FY2022": "32.05%", "FY2021": "32.37%"}),
        ("Total Capital Ratio", {"FY2025": "27.20%", "FY2024": "27.67%", "FY2023": "29.50%", "FY2022": "32.05%", "FY2021": "33.52%"}),
        ("Leverage Ratio", {"FY2025": "22.43%", "FY2024": "22.81%", "FY2023": "23.92%", "FY2022": "27.49%", "FY2021": "27.57%"}),
        ("LCR", {"FY2025": "1457%", "FY2024": "910%", "FY2023": "2971%", "FY2022": "951%", "FY2021": "1446%"}),
        ("NSFR", {"FY2025": "136%", "FY2024": "131%", "FY2023": "145%", "FY2022": "140%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation. All £ figures are converted from the Bank's native USD reporting (see Cash Flow Statement "
         "sheet's FX conversion note) - this conversion was not explicitly requested for this bank but applied for "
         "consistency with the rest of the series.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/UNION BANK OF INDIA UK FINANCIALS.xlsx")
