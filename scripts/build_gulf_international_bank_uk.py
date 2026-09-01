import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}
PREV_YEAR = {"FY2021": "FY2020", "FY2022": "FY2021", "FY2023": "FY2022", "FY2024": "FY2023", "FY2025": "FY2024"}

# ---------------------------------------------------------------
# FX conversion (GIB UK reports in USD; converting to £ per this project's
# established FX methodology - same public Bank of England GBP/USD spot/
# average rates already used for Zenith Bank UK / Union Bank of India UK /
# Credit Suisse International, reused here rather than re-derived).
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


def flow(usd):
    """Flow (cash flow statement line item) figures, £'000, at that year's average rate."""
    return {y: round(v / FX_AVG[y] / 1000, 1) for y, v in usd.items() if y in FX_AVG}


def stock(usd):
    """Point-in-time (balance/capital) figures, £'000, at that year's period-end spot rate."""
    return {y: round(v / FX_SPOT[y] / 1000, 1) for y, v in usd.items() if y in FX_SPOT}


def opening_cash(usd):
    """Opening cash balance, £'000 - uses the PRIOR year's period-end spot rate (it's the
    same balance as that prior year's closing figure, so must convert identically)."""
    return {y: round(v / FX_SPOT[PREV_YEAR[y]] / 1000, 1) for y, v in usd.items() if PREV_YEAR.get(y) in FX_SPOT}


# ---------------------------------------------------------------
# Source documents
# ---------------------------------------------------------------
CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/01223938/filing-history"
AR2024_URL = f"{CH_BASE}/MzQ2MTE4ODYxN2FkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = f"{CH_BASE}/MzQxNzM5ODc0MWFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = f"{CH_BASE}/MzM3NTI0MDA2MmFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = f"{CH_BASE}/MzM1NTYyODEwMGFkaXF6a2N4/document?format=pdf&download=0"

P3_2024_URL = "https://gib-am.files.svdcdn.com/production/documents/2024-GIBUK-Pillar-3-disclosures-Board-approved.pdf"
P3_2023_URL = "https://gib-am.files.svdcdn.com/production/documents/Fund-sustainability-related-documents/2023-GIBUK-Pillar-3-disclosures.pdf"
P3_2022_URL = "https://web.archive.org/web/20230927145657/https://gibam.com/assets/2022-GIBUK-Pillar-3-disclosures_VF.pdf"
P3_2021_URL = "https://web.archive.org/web/20230329132856/https://gibam.com/assets/2021-GIBUK-Pillar-3_Final.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Gulf International Bank (UK) Limited (\"GIB UK\", FRN 124772, company 01223938) is a wholly "
    "owned subsidiary of Gulf International Bank B.S.C. (Bahrain, sovereign-backed by several Gulf Cooperation "
    "Council states), trading as \"GIB Asset Management\" (GIB AM) for its investment-management business, with a "
    "branch in New York. It prepares standalone (non-consolidated) financial statements under UK-adopted "
    "international accounting standards, exempt from producing group accounts under Companies Act 2006 s.401 and "
    "IFRS 10 (its parent's consolidated accounts are filed in Bahrain). No cash-flow exemption applies - a full "
    "Statement of Cash Flow is presented every year. FY2025 accounts had not yet been filed with Companies House "
    "and no FY2025 Pillar 3 disclosure had been published as at the time of this workbook's research (accounts "
    "for this entity have historically been filed 3-4 months after the 31 December year-end, so this is normal "
    "lag, not a gap)."
)

FX_NOTE = (
    "FX CONVERSION NOTE: GIB UK reports in US Dollars (its functional and presentation currency per its own "
    "accounting policy note). This workbook converts every $ amount to £ for consistency with the rest of this "
    "series, following the same methodology established for Zenith Bank UK/Union Bank of India UK/Credit Suisse "
    "International: point-in-time/balance figures (capital, RWA, leverage exposure, HQLA/stable-funding amounts, "
    "cash balances) use the Bank of England GBP/USD SPOT rate as at that fiscal year-end; flow figures (every "
    "cash flow statement line item) use the AVERAGE of Bank of England rates over that calendar year. Rates used "
    "(£1 = $X, reused from this project's existing FX rate table): 31 Dec 2020 spot 1.3661 (FY2021 opening cash "
    "only); FY2021 spot 1.3521 / average 1.3752; FY2022 spot 1.2097 / average 1.2362; FY2023 spot 1.2732 / "
    "average 1.2439; FY2024 spot 1.2515 / average 1.2782. All % ratios are shown exactly as reported in USD and "
    "were NOT converted - a ratio is dimensionless and currency-invariant. Because stocks and flows are converted "
    "at different rates, the cash flow statement includes an explicit 'Effect of GBP/USD translation' reconciling "
    "line, computed programmatically so it can never drift out of sync with the rates above, so that opening + "
    "all flows + this line = closing exactly in £ terms - this line is purely an artefact of £ translation and "
    "has no bearing on the Bank's underlying USD results. This conversion was not explicitly requested for this "
    "bank - applied for consistency with the rest of the series; flag if £'000 rather than the Bank's native "
    "US$'000 presentation is not what's wanted here."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Gulf International Bank (UK) Limited's own Statement of Cash Flow (converted from "
    "USD to £, see FX conversion note below), transcribed from scanned/image-only Companies House filings (no "
    "text layer in any of the 4 filings):\n"
    f"FY2024: Annual Report and Financial Statements 2024, p.109 (Statement of Cash Flow) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.71 (Statement of Cash Flow, incl. FY2022 comparative) - {AR2023_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021, p.52 (Statement of Cash Flow) - {AR2021_URL}\n"
    "FY2022's own column is sourced from the FY2023 Annual Report's comparative column (p.71 above) rather than "
    "the FY2022 Annual Report directly - both would show the same figures for FY2022 (a bank's own prior-year "
    "comparative is not normally restated absent a disclosed reason, and none is disclosed here); the FY2022 "
    "filing itself is also fully scanned - see AR2022_URL for reference: " + AR2022_URL + ".\n"
    "FY2025 is blank: no FY2025 Annual Report has been filed with Companies House yet.\n"
    "All 4 years' opening-to-closing cash bridges reconcile exactly in USD as originally reported; the £ "
    "conversion is exact by construction (translation-effect line computed programmatically, see FX note). "
    "FY2021/FY2023/FY2024's operating-activities line items also sum exactly (in USD) to each year's own printed "
    "subtotal. FY2022's do not: summing FY2022's own line items above gives $285,026k vs the source's own printed "
    "$287,025k subtotal - a $1,999k (~0.7%) gap within the source document's own comparative column, not traceable "
    "to a specific mis-cast line (each line was independently re-checked against the source image). Flagged rather "
    "than forced to reconcile, per this project's convention for unexplained source-side gaps.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE
)


def p3_sources():
    return (
        "Sources - Gulf International Bank (UK) Limited Pillar 3 Disclosures (UK KM1 - Key Metrics table), "
        "converted from USD to £ where a $ amount (see FX conversion note on the Cash Flow Statement sheet; % "
        "ratios are unconverted):\n"
        f"FY2024: Pillar 3 Disclosures as at 31 December 2024 (Board-approved), p.6 (UK KM1) - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures as at 31 December 2023, p.6 (UK KM1) - {P3_2023_URL}\n"
        f"FY2022: sourced from the FY2023 Pillar 3 Disclosures' own T-4/prior-year comparative column (p.6 above), "
        "which matches the FY2022 Pillar 3 Disclosures document exactly where both are legible - "
        f"{P3_2022_URL}\n"
        f"FY2021: Pillar 3 Disclosures as at 31 December 2021, p.6 (Key ratios summary) and p.7 (Liquidity, "
        f"Q4 2021 quarter-end figures) - {P3_2021_URL}\n"
        "FY2025: not yet published as at the time of this workbook's research."
    )


bw = BankWorkbook(bank_name="Gulf International Bank (UK) Limited", years=YEARS, year_label=YEAR_LABEL, header_color="38AD47")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (raw USD, then converted via flow()/stock()/opening_cash())
# ---------------------------------------------------------------
rows_usd = [
    ("SECTION", "Operating cash flows from operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {"FY2024": 32104, "FY2023": 52494, "FY2022": 9146, "FY2021": -13571}),
    ("DATA", "Income tax (paid)/received", {"FY2024": -6050, "FY2023": -3870, "FY2022": 0, "FY2021": 2400}),
    ("DATA", "Depreciation of property and equipment", {"FY2024": 902, "FY2023": 1060, "FY2022": 1211, "FY2021": 1270}),
    ("DATA", "Depreciation of ROU assets", {"FY2024": 2358, "FY2023": 1883, "FY2022": 2520, "FY2021": 2247}),
    ("DATA", "Change in accrued interest receivable", {"FY2024": -4050, "FY2023": -90461, "FY2022": -47278, "FY2021": 10789}),
    ("DATA", "Change in accrued interest payable", {"FY2024": -4230, "FY2023": 7017, "FY2022": 45097, "FY2021": -649}),
    ("DATA", "Change in other net assets (incl. movements to pension reserve)", {"FY2023": 11798, "FY2022": -68074, "FY2021": -7360}),
    ("DATA", "Change in other operating assets and liabilities", {"FY2024": -56920}),
    ("DATA", "Change in trading securities", {"FY2024": -30056, "FY2023": -38262, "FY2022": -17018, "FY2021": -23066}),
    ("DATA", "Change in placements with banks", {"FY2024": -376341, "FY2023": -1629689, "FY2022": 144535, "FY2021": 994557}),
    ("DATA", "Change in debt securities at amortised cost/investment securities net", {"FY2023": 13993, "FY2022": 18566, "FY2021": -724622}),
    ("DATA", "Change in debt securities at amortised cost", {"FY2024": -46010}),
    ("DATA", "Change in deposits from banks", {"FY2024": 1179214, "FY2023": -536019, "FY2022": 893757, "FY2021": -144626}),
    ("DATA", "Change in deposits from customers", {"FY2024": -8096261, "FY2023": 11528272, "FY2022": -698680, "FY2021": 247815}),
    ("DATA", "Finance costs (lease liability)", {"FY2024": 1058, "FY2023": 1093, "FY2022": 1125}),
    ("DATA", "Finance costs (lease liability) and FX loss on reval of lease liability", {"FY2021": 940}),
    ("DATA", "Impairment", {"FY2024": -166, "FY2023": 199, "FY2022": 119, "FY2021": 1199}),
    ("TOTAL", "Net cash (outflow)/inflow from operating activities", {"FY2024": -7404448, "FY2023": 9319508, "FY2022": 287025, "FY2021": 347323}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Net purchase of property and equipment", {"FY2024": -302, "FY2023": -508, "FY2022": -39, "FY2021": -4966}),
    ("TOTAL", "Net cash used in investing activities", {"FY2024": -302, "FY2023": -508, "FY2022": -39, "FY2021": -4966}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Payment of principal portion of lease liabilities", {"FY2024": -3186, "FY2023": -3249, "FY2022": -2115, "FY2021": -108}),
    ("TOTAL", "Net cash used in financing activities", {"FY2024": -3186, "FY2023": -3249, "FY2022": -2115, "FY2021": -108}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2024": -7407936, "FY2023": 9315751, "FY2022": 284871, "FY2021": 342249}),
    ("DATA", "Net foreign exchange difference (as reported, USD)", {"FY2024": -96612, "FY2023": 241455, "FY2022": -558230}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2024": 14883184, "FY2023": 5325978, "FY2022": 5599337, "FY2021": 5257088}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2024": 7378636, "FY2023": 14883184, "FY2022": 5325978, "FY2021": 5599337}),
]

_usd_by_label = {label: usd for _, label, usd in rows_usd}
rows = []
for kind, label, usd in rows_usd:
    if kind == "SECTION":
        rows.append((kind, label, {}))
    elif label == "Cash and cash equivalents at beginning of year":
        rows.append((kind, label, opening_cash(usd)))
    elif label == "Cash and cash equivalents at end of year":
        rows.append((kind, label, stock(usd)))
    else:
        rows.append((kind, label, flow(usd)))
    if label == "Net foreign exchange difference (as reported, USD)":
        # £ translation plug (see FX_NOTE): stocks (opening/closing) and flows
        # (everything else) are converted at different rates, so the £ statement
        # needs an explicit reconciling line to tie exactly. Computed programmatically
        # from the actual converted figures, per year, so it can never drift out of
        # sync with the rates above.
        opening_gbp = opening_cash(_usd_by_label["Cash and cash equivalents at beginning of year"])
        closing_gbp = stock(_usd_by_label["Cash and cash equivalents at end of year"])
        net_change_gbp = flow(_usd_by_label["Net (decrease)/increase in cash and cash equivalents"])
        fx_gbp = flow(usd)
        plug = {
            y: round(closing_gbp[y] - opening_gbp[y] - net_change_gbp[y] - fx_gbp.get(y, 0), 1)
            for y in closing_gbp
        }
        rows.append(("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", plug))

bw.add_cash_flow_sheet(
    title="Gulf International Bank (UK) Limited — Statement of Cash Flow",
    subtitle="£'000, converted from USD - see source note at bottom for FX methodology and rates used. FY2025 blank (no FY2025 Annual Report filed yet).",
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
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=140)


CAPITAL_USD = {"FY2024": 435465, "FY2023": 411658, "FY2022": 368416, "FY2021": 371866}
RWA_USD = {"FY2024": 1963743, "FY2023": 1809984, "FY2022": 1557567, "FY2021": 1932234}
CAPITAL_RATIO = {"FY2024": "22.18%", "FY2023": "22.74%", "FY2022": "23.65%", "FY2021": "19.22%"}

metric("CET1 Capital", "£'000 (conv. from USD)", [("Common Equity Tier 1 (CET1) capital", stock(CAPITAL_USD))], p3_sources(),
       note="GIB UK's regulatory capital consists entirely of CET1 (fully paid-up ordinary shares, capital contribution, and audited retained earnings/reserves) - no AT1 or Tier 2 instruments in any year.")
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 (CET1) ratio", CAPITAL_RATIO)], p3_sources())
metric("Tier 1 Capital", "£'000 (conv. from USD)", [("Tier 1 capital", stock(CAPITAL_USD))], p3_sources(),
       note="Equal to CET1 capital in every year - the Bank holds no Additional Tier 1 (AT1) instruments.")
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", CAPITAL_RATIO)], p3_sources())
metric("Total Capital", "£'000 (conv. from USD)", [("Total capital", stock(CAPITAL_USD))], p3_sources(),
       note="Equal to CET1/Tier 1 capital in every year - the Bank holds no AT1 or Tier 2 instruments.")
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", CAPITAL_RATIO)], p3_sources())
metric("Total RWAs", "£'000 (conv. from USD)", [("Total risk-weighted exposure amount", stock(RWA_USD))], p3_sources())

metric(
    "Leverage Ratio", "£'000 / % (conv. from USD)",
    [
        ("Total exposure measure", stock({
            "FY2024": 8682283, "FY2023": 7795728, "FY2022": 5136739, "FY2021": 10573209,
        })),
        ("Leverage ratio (%)", {"FY2024": "5.02%", "FY2023": "5.28%", "FY2022": "7.17%", "FY2021": "3.52%"}),
    ],
    p3_sources(),
    note="Basis change: FY2022 onward reports 'Total exposure measure EXCLUDING claims on central banks' (the "
         "Bank's own FY2021 report states it was 'not, currently, in scope of the UK Leverage Framework' that "
         "introduced this exclusion, effective 1 January 2022); FY2021's figure is the single (unqualified) "
         "leverage ratio/exposure measure as originally reported that year, likely on an including-central-bank-"
         "claims basis. Each year's own as-reported figure is used rather than forcing a common basis.",
)

metric(
    "LCR", "£'000 / % (conv. from USD)",
    [
        ("Total high-quality liquid assets (HQLA / average liquid assets buffer)", stock({
            "FY2024": 8650825, "FY2023": 15980246, "FY2022": 9198733, "FY2021": 6737809,
        })),
        ("Total net cash outflows, adjusted value", stock({
            "FY2024": 3021360, "FY2023": 5579776, "FY2022": 2597379,
        })),
        ("Liquidity Coverage Ratio (%)", {"FY2024": "286.32%", "FY2023": "286.40%", "FY2022": "354.15%", "FY2021": "480.13%"}),
    ],
    p3_sources(),
    note="Methodology differs for FY2021: that year's Pillar 3 report discloses LCR as a quarterly (not annual) "
         "average - Q4 2021 is used here as the closest analogue to later years' 12-month-average KM1 figure. "
         "FY2021's own 'Average net flows' figure is not directly comparable to later years' 'Total net cash "
         "outflows (adjusted value)' definition, so that cell is left blank for FY2021 rather than approximated; "
         "the ratio and HQLA-equivalent buffer are shown as reported.",
)

metric(
    "NSFR", "£'000 / % (conv. from USD)",
    [
        ("Total available stable funding", stock({
            "FY2024": 5139351, "FY2023": 4607371, "FY2022": 4297495, "FY2021": 10511066,
        })),
        ("Total required stable funding", stock({
            "FY2024": 2225713, "FY2023": 1822687, "FY2022": 1031978, "FY2021": 9455958,
        })),
        ("Net Stable Funding Ratio (%)", {"FY2024": "230.91%", "FY2023": "252.78%", "FY2022": "416.49%", "FY2021": "111.16%"}),
    ],
    p3_sources(),
    note="FY2021 is that year's Q4 (year-end) quarterly figure, as originally disclosed in quarterly form; "
         "FY2022 onward is each year's single annual KM1 figure.",
)

bw.add_not_disclosed_metric_sheets(["MREL Ratio"], p3_sources(),
    per_note={"MREL Ratio": "No separate MREL ratio or instruments disclosed in any year. The Bank's own FY2021 "
                             "Pillar 3 report explains why: following the Bank of England's 3 December 2021 "
                             "Statement of Policy on MREL, 'GIB (UK)'s MREL requirement is equal to its CRD V "
                             "requirement under Pillar 1 and Pillar 2A. Consequently, the Bank does not need to "
                             "hold any MREL compliant instruments in addition to those needed to satisfy its CRD "
                             "V requirement' - i.e. MREL is fully satisfied by ordinary capital, with no "
                             "incremental MREL-specific ratio or instrument stock to disclose."})

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
cf_totals_usd = {
    "Net cash (outflow)/inflow from operating activities": {"FY2024": -7404448, "FY2023": 9319508, "FY2022": 287025, "FY2021": 347323},
    "Net cash used in investing activities": {"FY2024": -302, "FY2023": -508, "FY2022": -39, "FY2021": -4966},
    "Net cash used in financing activities": {"FY2024": -3186, "FY2023": -3249, "FY2022": -2115, "FY2021": -108},
}
cf_close_usd = {"FY2024": 7378636, "FY2023": 14883184, "FY2022": 5325978, "FY2021": 5599337}

bw.add_overview_sheet(
    cash_flow_totals=[(label, flow(vals)) for label, vals in cf_totals_usd.items()]
                      + [("Cash and cash equivalents at end of year", stock(cf_close_usd))],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", CAPITAL_RATIO),
        ("Tier 1 Ratio", CAPITAL_RATIO),
        ("Total Capital Ratio", CAPITAL_RATIO),
        ("Leverage Ratio", {"FY2024": "5.02%", "FY2023": "5.28%", "FY2022": "7.17%", "FY2021": "3.52%"}),
        ("LCR", {"FY2024": "286.32%", "FY2023": "286.40%", "FY2022": "354.15%", "FY2021": "480.13%"}),
        ("NSFR", {"FY2024": "230.91%", "FY2023": "252.78%", "FY2022": "416.49%", "FY2021": "111.16%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation. All £ figures are converted from the Bank's native USD reporting (see Cash Flow Statement "
         "sheet's FX conversion note) - this conversion was not explicitly requested for this bank but applied "
         "for consistency with the rest of the series. FY2025 is blank throughout (no FY2025 Annual Report or "
         "Pillar 3 Disclosure published yet).",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/GULF INTERNATIONAL BANK UK FINANCIALS.xlsx")
