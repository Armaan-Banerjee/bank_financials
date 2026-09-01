import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}
PREV_YEAR = {"FY2021": "FY2020", "FY2022": "FY2021", "FY2023": "FY2022", "FY2024": "FY2023"}

# ---------------------------------------------------------------
# FX conversion (United Bank for Africa (UK) Limited reports in USD; converting
# to £ per this project's established FX methodology - see build_smbc.py /
# build_zenith.py precedent). Same calendar years as Zenith Bank UK, so the
# same Bank of England GBP/USD spot/average rates apply (£1 = $X, via
# poundsterlinglive.com's published BoE archive).
# ---------------------------------------------------------------
FX_SPOT = {
    "FY2020": 1.3661,  # 31 Dec 2020 - only used for FY2021's opening cash balance
    "FY2021": 1.3521,  # 31 Dec 2021
    "FY2022": 1.2097,  # 30 Dec 2022 (31st was a Saturday)
    "FY2023": 1.2732,  # 29 Dec 2023 (31st was a Sunday)
    "FY2024": 1.2515,  # 31 Dec 2024
}
FX_AVG = {
    "FY2021": 1.3752,
    "FY2022": 1.2362,
    "FY2023": 1.2439,
    "FY2024": 1.2782,
}


def flow(usd_000s):
    """Flow (cash flow statement line item) figures, £'000, at that year's
    average rate. UBA UK's own source already prints figures in US$'000, so
    (unlike build_zenith.py, whose source printed whole dollars) there's no
    extra /1000 here - dividing US$'000 by the rate gives £'000 directly."""
    return {y: round(v / FX_AVG[y], 1) for y, v in usd_000s.items()}


def stock(usd_000s):
    """Point-in-time (balance/capital) figures, £'000, at that year's period-end spot rate."""
    return {y: round(v / FX_SPOT[y], 1) for y, v in usd_000s.items()}


def opening_cash(usd_000s):
    """Opening cash balance, £'000 - uses the PRIOR year's period-end spot rate (it's the
    same balance as that prior year's closing figure, so must convert identically)."""
    return {y: round(v / FX_SPOT[PREV_YEAR[y]], 1) for y, v in usd_000s.items()}

# ---------------------------------------------------------------
# Source documents
# ---------------------------------------------------------------
AR2024_URL = "https://www.ubauk.com/wp-content/uploads/sites/29/2025/07/UBA-UK-2024-AR-1.pdf"
AR2022_URL = "https://www.ubauk.com/wp-content/uploads/sites/29/2023/09/UBA-UK-FIN-A-Ann-Rpt-and-Accts-31-Dec-2022.pdf"

P3_2024_URL = "https://www.ubauk.com/wp-content/uploads/sites/29/2026/05/UBA-UK-Pillar-3-Disclosures-31-Dec-2024.pdf"
P3_2022_URL = "https://www.ubauk.com/wp-content/uploads/sites/29/2023/08/UBA-UK-Pillar-3-Disclosures-31-Dec-2022_final-clean-trotter-comments.1-1.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: United Bank for Africa (UK) Limited (Companies House 03104974, FRN 695048) is a UK subsidiary of "
    "United Bank for Africa Plc (Nigeria). Unlike several other foreign-subsidiary banks in this workbook series "
    "(ICICI Bank UK, Philippine National Bank Europe, Citibank UK, State Bank of India UK), it prepares full IFRS "
    "financial statements with a genuine Statement of Cash Flows every year - no FRS 101/102 cash-flow exemption "
    "applies. The Bank's Own Funds consist entirely of Common Equity Tier 1 (CET1) capital (no AT1 or Tier 2 "
    "instruments), so CET1 capital = Tier 1 capital = Total capital in every year shown. No FY2025 Annual Report or "
    "Pillar 3 disclosure has been published yet (as of this workbook's build date), so this workbook covers "
    "FY2021-FY2024 only (4 years) rather than the usual 5."
)

FX_NOTE = (
    "FX CONVERSION NOTE: United Bank for Africa (UK) Limited reports in US Dollars (its functional currency, per "
    "its own foreign currency risk note - 'Revenues, assets and liabilities are primarily in the functional "
    "currency US dollar'). This workbook converts every $ amount to £ for consistency with the rest of this "
    "series, following the same methodology established for SMBC Bank International plc and Zenith Bank (UK) "
    "Limited: point-in-time/balance figures (capital, RWA, leverage exposure, HQLA, cash balances) use the Bank "
    "of England GBP/USD SPOT rate as at that fiscal year-end (31 December); flow figures (every cash flow "
    "statement line item) use the AVERAGE of Bank of England rates over that calendar year - both via "
    "poundsterlinglive.com's published Bank of England archive, and identical to the rates used for Zenith Bank "
    "UK since both banks share the same 31 December fiscal year-end. Rates used (£1 = $X): 31 Dec 2020 spot "
    "1.3661 (FY2021 opening cash only); FY2021 spot 1.3521 / average 1.3752; FY2022 spot 1.2097 / average "
    "1.2362; FY2023 spot 1.2732 / average 1.2439; FY2024 spot 1.2515 / average 1.2782. All % ratios (CET1/Tier "
    "1/Total Capital/Leverage/LCR/NSFR ratios) are shown EXACTLY as reported in USD and were NOT converted - a "
    "ratio is dimensionless and currency-invariant. Because stocks and flows are converted at different rates, "
    "the cash flow statement includes an explicit 'Effect of GBP/USD translation' reconciling line so opening + "
    "all flows + this line = closing exactly in £ terms - this line is purely an artefact of £ translation and "
    "has no bearing on the Bank's underlying USD results. This conversion was not explicitly requested for this "
    "bank (unlike SMBC) - applied for consistency with the rest of the series, following the same call already "
    "confirmed for Zenith Bank UK; flag if £'000 rather than the Bank's native US$'000 presentation is not what's "
    "wanted here."
)

RECONCILIATION_NOTE = (
    "RECONCILIATION NOTE: the FY2022 Annual Report's Statement of Cash Flows shows the FY2022 closing balance as "
    "US$31,392k, but a supplementary 'cash and cash equivalent reconciliation' note in that same report nets this "
    "down to US$31,354k (deducting a US$38k expected credit loss allowance) - and it is this US$31,354k figure "
    "that the FY2023 Annual Report actually carries forward as its own FY2023 opening balance. Both figures are "
    "used exactly as each report presents them (FY2022's own closing balance from its primary statement; FY2023's "
    "own opening balance from its primary statement) rather than forcing them to match, so there is a small "
    "(~£31k) presentational discontinuity between the FY2022 closing and FY2023 opening £ balances shown here - "
    "not a data error, the underlying US$38k difference is fully explained by the source reconciliation note."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are United Bank for Africa (UK) Limited's own Statement of Cash Flows (converted from "
    "USD to £, see FX conversion note below):\n"
    f"FY2024 & FY2023: Annual Report and Accounts 2024, p.50 (Statements of Cash Flows) - {AR2024_URL}\n"
    f"FY2022 & FY2021: Annual Report and Accounts 2022, p.39 (Statement of Cash Flows) - {AR2022_URL}\n"
    "Note: presentation differs between report vintages - FY2024/FY2023 separately disclose 'Change in due from "
    "banks', a combined FVTPL subscription/redemption line, and split FVOCI/amortised-cost gain-on-derecognition "
    "lines; FY2022/FY2021 instead show a single combined 'Loss on disposal of investments at FVOCI' line and "
    "separate FVTPL/amortised-cost purchase and proceeds lines. Each year's own as-reported line items and labels "
    "are preserved rather than forced into a common shape; blank cells indicate that year's report did not "
    "disclose that specific split.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE + "\n\n" + RECONCILIATION_NOTE
)


def p3_sources(page_24="10", page_22="9"):
    return (
        "Sources - United Bank for Africa (UK) Limited Pillar 3 Disclosures (Key Metrics table), converted from "
        "USD to £ where a $ amount (see FX conversion note on the Cash Flow Statement sheet; % ratios are "
        "unconverted):\n"
        f"FY2024 & FY2023: Pillar 3 Disclosures - 31 Dec 2024, p.{page_24} (Section 4, Key Metrics) - {P3_2024_URL}\n"
        f"FY2022 & FY2021: Pillar 3 Disclosures - 31 Dec 2022, p.{page_22} (Section 4, Key Metrics) - {P3_2022_URL}"
    )


bw = BankWorkbook(bank_name="United Bank for Africa (UK) Limited", years=YEARS, year_label=YEAR_LABEL, header_color="805B10")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (raw USD '000, then converted via flow()/stock()/opening_cash())
# ---------------------------------------------------------------
rows_usd = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {"FY2024": 12919, "FY2023": 17895, "FY2022": 12053, "FY2021": -1047}),
    ("DATA", "Depreciation and amortisation", {"FY2024": 780, "FY2023": 783, "FY2022": 756, "FY2021": 765}),
    ("DATA", "Net gain/(loss) on derecognition of debt instruments measured at amortised cost", {"FY2024": -1047, "FY2023": 124}),
    ("DATA", "Net gain/(loss) on derecognition of debt instruments measured at FVOCI", {"FY2024": -204, "FY2023": -12}),
    ("DATA", "Loss on disposal of investments at FVOCI", {"FY2022": 343, "FY2021": 18}),
    ("DATA", "Other non-cash items included in profit before tax", {"FY2024": 93, "FY2023": -1366}),
    ("DATA", "Increase in other non-cash movements", {"FY2022": 4583, "FY2021": -201}),
    ("DATA", "Change in due from banks", {"FY2024": -86309}),
    ("DATA", "Change in loans and advances to banks", {"FY2024": 274189, "FY2023": 56239, "FY2022": -92501, "FY2021": -249404}),
    ("DATA", "Change in loans and advances to customers", {"FY2024": 2561, "FY2023": -2561}),
    ("DATA", "Change in other assets", {"FY2024": -2122, "FY2023": -1552, "FY2022": 737, "FY2021": -1228}),
    ("DATA", "Change in deposit from banks", {"FY2024": -119812, "FY2023": -45796, "FY2022": 62562, "FY2021": 287902}),
    ("DATA", "Change in deposit from customers", {"FY2024": -27544, "FY2023": 32565, "FY2022": 4798, "FY2021": -13452}),
    ("DATA", "Change/increase in other liabilities", {"FY2024": 1841, "FY2023": 973, "FY2022": -1251, "FY2021": 3115}),
    ("DATA", "Tax paid", {"FY2024": -3217, "FY2023": -4064}),
    ("TOTAL", "Net cash flows from/(used in) operating activities", {"FY2024": 52128, "FY2023": 53228, "FY2022": -7920, "FY2021": 26468}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2024": -546, "FY2023": -67}),
    ("DATA", "Purchase and sale of property, plant and equipment (net)", {"FY2022": -24}),
    ("DATA", "Purchase of intangible assets", {"FY2024": -207, "FY2023": -95, "FY2022": -229, "FY2021": -122}),
    ("DATA", "Payments for investment securities at FVOCI", {"FY2024": -75117, "FY2023": -9857, "FY2022": -4988, "FY2021": -86474}),
    ("DATA", "Net payment for subscription/redemption of investment securities at FVTPL", {"FY2024": -5961, "FY2023": -15621}),
    ("DATA", "Payments for investment securities at FVTPL", {"FY2022": -27044, "FY2021": -12502}),
    ("DATA", "Payments for investment securities at amortised cost", {"FY2022": -13533, "FY2021": -33135}),
    ("DATA", "Proceeds from sale of investment securities at FVOCI", {"FY2024": 32328, "FY2023": 17627, "FY2022": 17438, "FY2021": 73743}),
    ("DATA", "Proceeds from sale of investment securities at amortised cost", {"FY2024": 18662, "FY2023": 2038}),
    ("DATA", "Proceeds from sale of investment securities at FVTPL", {"FY2022": 12502, "FY2021": 2000}),
    ("DATA", "Proceeds from maturity of investment securities at amortised cost", {"FY2021": 41008}),
    ("TOTAL", "Net cash flows from/(used in) investing activities", {"FY2024": -30841, "FY2023": -5975, "FY2022": -15878, "FY2021": -15482}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Payments of lease liabilities", {"FY2024": -255, "FY2023": -235, "FY2022": -235, "FY2021": -283}),
    ("DATA", "Payments of interest on leases", {"FY2024": -9, "FY2023": -11}),
    ("DATA", "Dividend paid", {"FY2024": -10000}),
    ("DATA", "Proceeds from issuance of share capital", {"FY2023": 12000}),
    ("TOTAL", "Net cash flow (used in)/from financing activities", {"FY2024": -10264, "FY2023": 11754, "FY2022": -235, "FY2021": -283}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2024": 11023, "FY2023": 59007, "FY2022": -24033, "FY2021": 10703}),
    ("DATA", "Net foreign exchange difference", {"FY2024": 55, "FY2023": 889}),
    ("DATA", "Cash and cash equivalents at beginning of period", {"FY2024": 91250, "FY2023": 31354, "FY2022": 55425, "FY2021": 44722}),
    ("TOTAL", "Cash and cash equivalents at end of period", {"FY2024": 102328, "FY2023": 91250, "FY2022": 31392, "FY2021": 55425}),
]

# £ translation plug (see FX_NOTE): stocks (opening/closing) and flows (everything
# else) are converted at different rates, so the £ statement needs an explicit
# reconciling line to tie exactly. Computed as closing(£) - opening(£) - net
# change(£) - reported FX-effect line(£), per year (verified independently).
TRANSLATION_PLUG_GBP = {"FY2024": 1427.6, "FY2023": -2400.8, "FY2022": 4399.5, "FY2021": 471.9}

# convert: SECTION rows pass through unchanged; opening-cash row uses opening_cash();
# everything else (DATA/TOTAL) uses flow() - all cash flow statement figures are
# period flows/movements except the opening balance, which is a point-in-time carry-forward.
rows = []
for kind, label, usd in rows_usd:
    if kind == "SECTION":
        rows.append((kind, label, {}))
    elif label == "Cash and cash equivalents at beginning of period":
        rows.append((kind, label, opening_cash(usd)))
    elif label == "Cash and cash equivalents at end of period":
        # point-in-time balance, like the opening row - spot rate, not average
        rows.append((kind, label, stock(usd)))
    else:
        rows.append((kind, label, flow(usd)))
    if label == "Net foreign exchange difference":
        rows.append(("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", TRANSLATION_PLUG_GBP))

bw.add_cash_flow_sheet(
    title="United Bank for Africa (UK) Limited — Statement of Cash Flows",
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
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=48, source_height=120)


CET1_TIER1_TOTAL_USD = {"FY2024": 78168.563, "FY2023": 60900.368, "FY2022": 36513.246, "FY2021": 38317.917}
RWA_USD = {"FY2024": 159390.258, "FY2023": 127932.133, "FY2022": 137833.765, "FY2021": 93272.286}
LEVERAGE_EXPOSURE_USD = {"FY2024": 483630.135, "FY2023": 626525.876, "FY2022": 613889.918, "FY2021": 573663.805}
HQLA_USD = {"FY2024": 110851.365, "FY2023": 100502.936, "FY2022": 91179.217, "FY2021": 92773.320}
NET_CASH_OUTFLOWS_USD = {"FY2024": 31422.835, "FY2023": 43919.581, "FY2022": 40678.515, "FY2021": 25667.620}
NSFR_ASF_USD = {"FY2024": 122954.356, "FY2023": 138256.344, "FY2022": 167040.341, "FY2021": 152043.116}
NSFR_RSF_USD = {"FY2024": 67305.335, "FY2023": 90321.851, "FY2022": 92117.147, "FY2021": 102891.413}

metric("CET1 Capital", "£'000 (conv. from USD)", [("Common Equity Tier 1 (CET1) capital", stock(CET1_TIER1_TOTAL_USD))], p3_sources())
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 (CET1) ratio", {"FY2024": "49.04%", "FY2023": "47.60%", "FY2022": "23.27%", "FY2021": "33.56%"})], p3_sources())
metric("Tier 1 Capital", "£'000 (conv. from USD)", [("Tier 1 capital", stock(CET1_TIER1_TOTAL_USD))], p3_sources(),
       note="Equal to CET1 capital in every year - the Bank holds no Additional Tier 1 (AT1) instruments.")
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {"FY2024": "49.04%", "FY2023": "47.60%", "FY2022": "23.27%", "FY2021": "33.56%"})], p3_sources())
metric("Total Capital", "£'000 (conv. from USD)", [("Total capital", stock(CET1_TIER1_TOTAL_USD))], p3_sources(),
       note="Equal to CET1/Tier 1 capital in every year - the Bank holds no AT1 or Tier 2 instruments.")
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2024": "49.04%", "FY2023": "47.60%", "FY2022": "23.27%", "FY2021": "33.56%"})], p3_sources())
metric("Total RWAs", "£'000 (conv. from USD)", [("Total risk-weighted exposure amount", stock(RWA_USD))], p3_sources())

metric(
    "Leverage Ratio", "£'000 / % (conv. from USD)",
    [
        ("Total exposure measure excluding claims on central banks", stock(LEVERAGE_EXPOSURE_USD)),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2024": "16.16%", "FY2023": "9.72%", "FY2022": "6%", "FY2021": "7%"}),
    ],
    p3_sources(),
    note="FY2022/FY2021 leverage ratios are printed to whole-percent precision only in the source document "
         "(6% and 7%), unlike FY2024/FY2023's two-decimal precision - transcribed exactly as shown, not rounded "
         "further or given false precision.",
)

metric(
    "LCR", "£'000 / % (conv. from USD)",
    [
        ("Total high-quality liquid assets (HQLA), weighted value (average)", stock(HQLA_USD)),
        ("Total net cash outflows, adjusted value", stock(NET_CASH_OUTFLOWS_USD)),
        ("Liquidity Coverage Ratio (%)", {"FY2024": "352.77%", "FY2023": "228.83%", "FY2022": "224.15%", "FY2021": "361.44%"}),
    ],
    p3_sources(),
)

metric(
    "NSFR", "£'000 / % (conv. from USD)",
    [
        ("Total available stable funding", stock(NSFR_ASF_USD)),
        ("Total required stable funding", stock(NSFR_RSF_USD)),
        ("NSFR ratio (%)", {"FY2024": "182.68%", "FY2023": "153.07%", "FY2022": "181.33%", "FY2021": "147.77%"}),
    ],
    p3_sources(),
)

bw.add_not_disclosed_metric_sheets(["MREL Ratio"], p3_sources(),
    per_note={"MREL Ratio": "No MREL disclosure (numeric or qualitative) or UK KM2 template found anywhere in any "
                             "year's Pillar 3 report - not explicitly stated as an exemption, but consistent with "
                             "the Bank's small size relative to typical MREL-in-scope thresholds."})

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
cf_totals_usd = {
    "Net cash flows from/(used in) operating activities": {"FY2024": 52128, "FY2023": 53228, "FY2022": -7920, "FY2021": 26468},
    "Net cash flows from/(used in) investing activities": {"FY2024": -30841, "FY2023": -5975, "FY2022": -15878, "FY2021": -15482},
    "Net cash flow (used in)/from financing activities": {"FY2024": -10264, "FY2023": 11754, "FY2022": -235, "FY2021": -283},
}
cf_close_usd = {"FY2024": 102328, "FY2023": 91250, "FY2022": 31392, "FY2021": 55425}

bw.add_overview_sheet(
    cash_flow_totals=[(label, flow(vals)) for label, vals in cf_totals_usd.items()]
                      + [("Cash and cash equivalents at end of period", stock(cf_close_usd))],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2024": "49.04%", "FY2023": "47.60%", "FY2022": "23.27%", "FY2021": "33.56%"}),
        ("Tier 1 Ratio", {"FY2024": "49.04%", "FY2023": "47.60%", "FY2022": "23.27%", "FY2021": "33.56%"}),
        ("Total Capital Ratio", {"FY2024": "49.04%", "FY2023": "47.60%", "FY2022": "23.27%", "FY2021": "33.56%"}),
        ("Leverage Ratio", {"FY2024": "16.16%", "FY2023": "9.72%", "FY2022": "6%", "FY2021": "7%"}),
        ("LCR", {"FY2024": "352.77%", "FY2023": "228.83%", "FY2022": "224.15%", "FY2021": "361.44%"}),
        ("NSFR", {"FY2024": "182.68%", "FY2023": "153.07%", "FY2022": "181.33%", "FY2021": "147.77%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation. All £ figures are converted from the Bank's native USD reporting (see Cash Flow Statement "
         "sheet's FX conversion note) - this conversion was not explicitly requested for this bank but applied for "
         "consistency with the rest of the series, following the same call already confirmed for Zenith Bank UK. "
         "No FY2025 Annual Report or Pillar 3 disclosure has been published yet, so this workbook covers "
         "FY2021-FY2024 (4 years) rather than the usual 5.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/UBA UK FINANCIALS.xlsx")
