import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

# ---------------------------------------------------------------
# FX conversion (FidBank UK reports in USD; converting to £ per this
# project's established FX methodology - see build_zenith.py precedent).
# Unlike other banks in this series, rates are NOT sourced from the Bank of
# England independently - FidBank UK's own Annual Report discloses its own
# Dollar/Sterling exchange rate (year-end and average) for each year in its
# 5-year Financial Highlights table, so those entity-disclosed rates are used
# directly (£1 = $X), avoiding any independent-source mismatch.
# ---------------------------------------------------------------
FX_SPOT = {  # "Year End" rate, £1 = $X
    "FY2025": 1.35,
    "FY2024": 1.25,
    "FY2023": 1.27,
    "FY2022": 1.20,
    "FY2021": 1.35,  # from the FY2025 AR's own 5-year Financial Highlights table (p.6) -
                      # needed only to convert FY2022's opening balance (= FY2021's closing
                      # balance) at the correct spot rate; no FY2021 cash flow statement exists.
}
FX_AVG = {  # "Average" rate, £1 = $X
    "FY2025": 1.32,
    "FY2024": 1.28,
    "FY2023": 1.25,
    "FY2022": 1.23,
}
PREV_YEAR = {"FY2023": "FY2022", "FY2024": "FY2023", "FY2025": "FY2024", "FY2022": "FY2021"}


def flow(usd):
    """Flow (cash flow statement line item) figures, £'000, at that year's average rate."""
    return {y: round(v / FX_AVG[y], 1) for y, v in usd.items() if y in FX_AVG}


def stock(usd):
    """Point-in-time (balance) figures, £'000, at that year's period-end spot rate."""
    return {y: round(v / FX_SPOT[y], 1) for y, v in usd.items() if y in FX_SPOT}


def opening_cash(usd):
    """Opening cash balance, £'000 - uses the PRIOR year's period-end spot rate."""
    return {y: round(v / FX_SPOT[PREV_YEAR[y]], 1) for y, v in usd.items() if y in PREV_YEAR}


# ---------------------------------------------------------------
# Source documents (all via Companies House - FidBank UK's own site has no
# investor-relations/regulatory-disclosures section; only 3 Annual Report
# filings exist at Companies House at all, none earlier - see ENTITY_NOTE)
# ---------------------------------------------------------------
CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/04661188/filing-history"
AR2025_URL = f"{CH_BASE}/MzUzMzg1ODU2NWFkaXF6a2N4/document?format=pdf&download=0"  # filed 25 Jul 2026, covers FY2025+FY2024
AR2023_URL = f"{CH_BASE}/MzQxOTU1NjA5M2FkaXF6a2N4/document?format=pdf&download=0"  # filed 26 Apr 2024, covers FY2023+FY2022

ENTITY_NOTE = (
    "FidBank UK Limited (company 04661188, FRN 400712) is a wholly-owned subsidiary of Fidelity Bank Plc, "
    "Nigeria (listed on the Nigerian Stock Exchange). The company has changed name twice: incorporated 2003 "
    "as \"Union Bank UK PLC\", later became \"Fidelity Bank UK Limited\", then renamed \"FidBank UK Limited\" "
    "on 13/14 March 2024 (per Companies House and the FY2023 Annual Report's own Subsequent Events note). "
    "Only 3 Annual Report filings exist at Companies House at all (FY2023, FY2024, FY2025) - no earlier "
    "filings were found, consistent with this being a young/thin filer at Companies House even though the "
    "company itself is over 20 years old; FY2021's cash flow could not be sourced from any document and is "
    "left blank rather than estimated (the FY2025 Annual Report's own 5-year \"Financial Highlights\" table "
    "gives only headline P&L/balance-sheet figures for FY2021, not a line-item cash flow statement).\n\n"
    "PRESENTATION CHANGE: the FY2023 Annual Report's cash flow statement (covering FY2023/FY2022) and the "
    "FY2025 Annual Report's cash flow statement (covering FY2025/FY2024) use different line-item structures "
    "and different terminology for the closing cash balance (\"Cash and cash equivalents\" in the FY2023 "
    "vintage vs. \"Cash and cash equivalents (including bank placements)\" in the FY2025 vintage) - each "
    "year's own line items and labels are preserved as printed rather than forced into a common format, per "
    "project convention.\n\n"
    "UNEXPLAINED CASH-BRIDGE GAP: FY2023's own statement shows closing cash and cash equivalents of "
    "US$7,127k. The FY2025 Annual Report's own comparative shows the FY2024 column's OPENING balance as "
    "US$115,901k - a US$108,774k gap between the two filings' figures for what should be the same balance "
    "sheet date (31 Dec 2023). This is plausibly explained by the broadened \"(including bank placements)\" "
    "definition introduced in the newer presentation, but this could not be confirmed from the source "
    "documents available - left unreconciled and flagged here rather than forced to match, per project "
    "convention (compare Arab Bank Europe's/Bank of China UK's similar unreconciled gaps elsewhere in this "
    "project).\n\n"
    "SOURCE-LABEL NOTE: the FY2025 Annual Report's cash flow statement labels BOTH columns' opening-balance "
    "row \"at 31 December 2024\" - this is a source-document label copy-paste artifact (the FY2024 column's "
    "opening balance is actually as at 31 December 2023); the VALUES are used exactly as printed, only the "
    "shared row label is affected.\n\n"
    "FX METHODOLOGY NOTE, FY2023/FY2022: the opening cash balance for these two years is converted at the "
    "correct PRIOR-year spot rate (FY2022's opening uses FY2021's own year-end $/£ rate of 1.35, sourced from "
    "the FY2025 Annual Report's 5-year Financial Highlights table, p.6 - no FY2021 cash flow statement exists "
    "for this entity, but its exchange rate is separately disclosed there). Because the FY2023 Annual Report's "
    "own USD figures tie exactly with no FX line (single-currency presentation), converting opening/flow/"
    "closing at three different correct rates (prior-year spot / this year's average / this year's spot) "
    "necessarily creates a translation gap in GBP terms - a genuine 'Exchange difference / effect of GBP-USD "
    "translation' line for FY2023/FY2022 is computed programmatically from the actual converted figures (see "
    "_FY2023_FY2022_TRANSLATION_PLUG in the build script) and shown alongside FY2025/FY2024's real disclosed "
    "exchange-difference line, per this project's established FX conversion methodology."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are FidBank UK Limited's own Statement of Cash Flows (Bank-only, GBP figures "
    "converted from the source's own USD figures at FidBank UK's own disclosed Dollar/Sterling exchange "
    "rates - see FX methodology note below):\n"
    f"FY2025, FY2024: Annual Report and Financial Statements for the year ended 31 December 2025, p.37 "
    f"(Statement of Cash Flows) - {AR2025_URL}\n"
    f"FY2023, FY2022: Annual Report & Financial Statements for the year ended 31 December 2023, p.26 "
    f"(Statement of Cash Flows) - {AR2023_URL}\n"
    "FY2021: not available - no source document with line-item cash flow detail was found (see entity note).\n\n"
    "FX conversion methodology: this project converts flow (cash flow statement) figures at each year's "
    "average GBP/USD rate and point-in-time (balance) figures at that year's period-end spot rate. FidBank "
    "UK's own Annual Report discloses its own Dollar/Sterling exchange rates (year-end and average) directly "
    "in its 5-year Financial Highlights table each year - those entity-disclosed rates are used here rather "
    "than an independently-sourced Bank of England rate, since they are explicitly stated as the rates the "
    "entity itself used to prepare its accounts. Ratios are never converted (dimensionless, currency-"
    "invariant).\n\n"
    + ENTITY_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - FidBank UK Limited Pillar 3/capital basis:\n"
        f"FY2025, FY2024: Annual Report and Financial Statements for the year ended 31 December 2025 - "
        f"\"Financial Highlights\" (p.6) and \"Performance Metrics\" (p.7) - {AR2025_URL}\n"
        f"FY2023, FY2022, FY2021: Annual Report and Financial Statements for the year ended 31 December "
        f"2025's own 5-year \"Financial Highlights\" comparative table (p.6), cross-checked against the "
        f"FY2023 Annual Report's own 5-year Financial Highlights table (p.3), which independently confirms "
        f"the same FY2023/FY2022/FY2021 figures - {AR2025_URL} ; {AR2023_URL}\n\n"
        "No standalone Pillar 3 document exists for this entity - no capital/liquidity-specific "
        "investor-relations or regulatory-disclosures page was found on FidBank UK's own site, and the "
        "Annual Report itself contains no dedicated Pillar 3/KM1-style table. All capital/liquidity figures "
        "come from the Annual Report's own Financial Highlights and Performance Metrics pages, which give "
        "only a single combined \"Capital Ratio\" (defined explicitly in the source as Shareholders' Funds "
        "÷ Risk Weighted Assets - not necessarily identical to a standard regulatory Total Capital "
        "Ratio calculation, since the numerator is an accounting rather than a regulatory-capital figure; "
        "used here as the closest available proxy, same treatment as Bank Saderat's \"Capital Cover\" "
        "elsewhere in this project) and, from FY2024 only, an LCR percentage. No CET1/Tier 1 breakdown, no "
        "RWA amount, no Leverage Ratio %, no NSFR, and no MREL figure were found anywhere in any of the 3 "
        "Annual Reports reviewed, despite the Strategic Report's Capital Risk section confirming a Leverage "
        "Ratio is tracked internally (\"tracked daily...reported quarterly to the Board\") - its actual value "
        "is never disclosed.\n"
        + extra
    )


CAPITAL_RATIO_NOTE = (
    "CAUTION: this is FidBank UK's own headline \"Capital Ratio\" (Shareholders' Funds ÷ Risk Weighted "
    "Assets, per the source's own stated formula), NOT necessarily a standard regulatory Total Capital Ratio "
    "(CET1+AT1+T2 ÷ RWA) since the numerator is an accounting equity figure, not a confirmed regulatory-"
    "capital figure. Used as the best available proxy since no other capital ratio breakdown is disclosed. "
    "FY2025's Performance Metrics infographic (p.7) separately states this same ratio as 21.64%, a minor "
    "internal inconsistency with the Financial Highlights table's own 21.46% - the Financial Highlights "
    "table figure is used here as the formal 5-year comparative disclosure."
)

NOT_DISCLOSED_NOTE = (
    "Not publicly disclosed - no standalone Pillar 3 document exists for this entity, and this metric does "
    "not appear anywhere in any of the 3 Annual Report filings reviewed (FY2023, FY2024, FY2025 - the only "
    "filings that exist at Companies House for this entity). See the Cash Flow Statement sheet's entity note."
)


bw = BankWorkbook(bank_name="FidBank UK Limited", years=YEARS, year_label=YEAR_LABEL, header_color="AD7B7E")

# ---------------------------------------------------------------
# FY2023/FY2022 GBP-translation plug (computed programmatically from the
# actual converted opening/net-change/closing figures, never hardcoded - see
# the Zenith Bank UK fix elsewhere in this project for why this matters).
# The FY2023 Annual Report's own USD statement ties exactly with no FX line
# (single currency, no conversion in the source) - the gap only appears once
# each of opening/flow/closing is converted at ITS OWN correct rate (prior-
# year spot / this year's average / this year's spot respectively), so a
# genuine translation-effect line is needed here even though the FY2023
# vintage's own presentation has no equivalent disclosed line (unlike
# FY2025/FY2024, which use a real disclosed "Exchange difference" figure).
# ---------------------------------------------------------------
_FY2023_FY2022_OPENING_USD = {"FY2023": 5431, "FY2022": 8999}
_FY2023_FY2022_NET_CHANGE_USD = {"FY2023": 1696, "FY2022": -3568}
_FY2023_FY2022_CLOSING_USD = {"FY2023": 7127, "FY2022": 5431}
_FY2023_FY2022_TRANSLATION_PLUG = {
    y: round(
        _FY2023_FY2022_CLOSING_USD[y] / FX_SPOT[y]
        - _FY2023_FY2022_OPENING_USD[y] / FX_SPOT[PREV_YEAR[y]]
        - _FY2023_FY2022_NET_CHANGE_USD[y] / FX_AVG[y],
        1,
    )
    for y in ("FY2023", "FY2022")
}

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    # --- FY2025/FY2024 basis (from the FY2025 Annual Report) ---
    ("DATA", "Profit/(loss) before tax", flow({"FY2025": 920, "FY2024": -2151, "FY2023": -3023, "FY2022": -5382})),
    ("DATA", "Depreciation and amortisation", flow({"FY2025": 164, "FY2024": 156, "FY2023": 193, "FY2022": 185})),
    ("DATA", "Amortisation of rights of use assets", flow({"FY2025": 380, "FY2024": 381, "FY2023": 379, "FY2022": 378})),
    ("DATA", "Adjustment to right of use asset - rent increase", flow({"FY2025": 0, "FY2024": -8})),
    ("DATA", "Amortisation of discounts received/premiums paid", flow({"FY2025": -2245, "FY2024": -2080, "FY2023": -1648, "FY2022": -245})),
    ("DATA", "Net exchange differences", flow({"FY2025": -335, "FY2024": 150})),
    ("DATA", "Profit on sale of amortised cost bonds", flow({"FY2025": -1502, "FY2024": 0})),
    # --- FY2023/FY2022 basis (from the FY2023 Annual Report) ---
    ("DATA", "Loss on disposal of tangible/intangible assets", flow({"FY2025": 0, "FY2024": 0, "FY2023": 1, "FY2022": 1})),
    ("DATA", "Bad debt recovered", flow({"FY2023": 0, "FY2022": 23})),
    ("DATA", "Exchange differences - finance lease liability", flow({"FY2023": 120, "FY2022": -292})),
    ("DATA", "Interest on finance lease liability", flow({"FY2025": 121, "FY2024": 192, "FY2023": 90, "FY2022": 102})),
    ("DATA", "Impairment of loans and advances", flow({"FY2025": 71, "FY2024": 445, "FY2023": -133, "FY2022": 144})),
    ("TOTAL", "Non-cash and other adjustments (subtotal; unlabeled in source)",
     flow({"FY2025": -2426, "FY2024": -2915, "FY2023": -4021, "FY2022": -5086})),
    ("DATA", "Change in loans and advances to banks", flow({"FY2025": -57963, "FY2024": -46794, "FY2023": -62422, "FY2022": 45036})),
    ("DATA", "Change in loans and advances to customers", flow({"FY2025": -91665, "FY2024": -46779, "FY2023": -5052, "FY2022": 12591})),
    ("DATA", "Change in short-term investments", flow({"FY2025": -11074, "FY2024": 0})),
    ("DATA", "Change in other assets", flow({"FY2025": -481, "FY2024": -287, "FY2023": -89, "FY2022": -12})),
    ("DATA", "Change in prepayments", flow({"FY2025": -121, "FY2024": -227, "FY2023": -92, "FY2022": -27})),
    ("DATA", "Change in deposits by banks", flow({"FY2025": 87927, "FY2024": 27557, "FY2023": 58695, "FY2022": -49159})),
    ("DATA", "Change in customer accounts", flow({"FY2025": 89485, "FY2024": 57086, "FY2023": 12335, "FY2022": -19026})),
    ("DATA", "Change in derivatives", flow({"FY2025": -285, "FY2024": 0})),
    ("DATA", "Change in other liabilities", flow({"FY2025": 20, "FY2024": 271, "FY2023": 64, "FY2022": 12})),
    ("DATA", "Change in accruals and deferred income", flow({"FY2025": -312, "FY2024": 318, "FY2023": -32, "FY2022": -47})),
    ("TOTAL", "Cash (used in)/from operations", flow({"FY2025": 13105, "FY2024": -11770, "FY2023": -614, "FY2022": -15718})),
    ("DATA", "Acquisition of financial assets", flow({"FY2025": -117331, "FY2024": -72386, "FY2023": -78132, "FY2022": -40469})),
    ("DATA", "Disposal of financial assets", flow({"FY2025": 126614, "FY2024": 68941, "FY2023": 55879, "FY2022": 52877})),
    ("DATA", "Income tax received", flow({"FY2023": 0, "FY2022": 253})),
    ("TOTAL", "Net cash (used in)/from operating activities", flow({"FY2025": 22388, "FY2024": -15215, "FY2023": -22867, "FY2022": -3057})),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Acquisition of tangible and intangible assets", flow({"FY2025": -394, "FY2024": -61, "FY2023": -163, "FY2022": -38})),
    ("TOTAL", "Net cash flow used in investing activities", flow({"FY2025": -394, "FY2024": -61, "FY2023": -163, "FY2022": -38})),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Increase in share capital", flow({"FY2025": 0, "FY2024": 0, "FY2023": 25000, "FY2022": 0})),
    ("DATA", "Leasehold property repayments", flow({"FY2025": -606, "FY2024": -564, "FY2023": -274, "FY2022": -473})),
    ("TOTAL", "Net cash generated from/(used in) financing activities", flow({"FY2025": -606, "FY2024": -564, "FY2023": 24726, "FY2022": -473})),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", flow({"FY2025": 21388, "FY2024": -15840, "FY2023": 1696, "FY2022": -3568})),
    ("DATA", "Cash and cash equivalents at the beginning of the year",
     opening_cash({"FY2025": 99914, "FY2024": 115901, "FY2023": 5431, "FY2022": 8999})),
    ("DATA", "Exchange difference in respect of cash and cash equivalents / effect of GBP-USD translation",
     {**flow({"FY2025": 454, "FY2024": -147}), **_FY2023_FY2022_TRANSLATION_PLUG}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", stock({"FY2025": 121756, "FY2024": 99914, "FY2023": 7127, "FY2022": 5431})),
]

bw.add_cash_flow_sheet(
    title="FidBank UK Limited — Statement of Cash Flows",
    subtitle="Bank-only basis, £'000 (conv. from USD). FY2021 not available - see source note below.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=340,
    unit_suffix=" (£'000, conv. from USD)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=48, source_height=220)


CAPITAL_RATIO = {"FY2025": "21.46%", "FY2024": "43%", "FY2023": "98%", "FY2022": "54%", "FY2021": "40%"}
LCR = {"FY2025": "178%", "FY2024": "243%"}

bw.add_not_disclosed_metric_sheets(
    ["CET1 Capital", "CET1 Ratio", "Tier 1 Capital", "Tier 1 Ratio"],
    p3_sources(),
    per_note={m: NOT_DISCLOSED_NOTE for m in ["CET1 Capital", "CET1 Ratio", "Tier 1 Capital", "Tier 1 Ratio"]},
)

bw.add_not_disclosed_metric_sheets(["Total Capital"], p3_sources(), per_note={"Total Capital": NOT_DISCLOSED_NOTE})

metric("Total Capital Ratio", "%", [("Capital Ratio (Shareholders' Funds ÷ RWA)", CAPITAL_RATIO)],
       p3_sources(), note=CAPITAL_RATIO_NOTE)

bw.add_not_disclosed_metric_sheets(
    ["Total RWAs", "Leverage Ratio"], p3_sources(),
    per_note={"Total RWAs": NOT_DISCLOSED_NOTE,
              "Leverage Ratio": NOT_DISCLOSED_NOTE + " The Strategic Report's Capital Risk section confirms "
                                "a Leverage Ratio IS tracked internally (\"tracked daily...reported quarterly "
                                "to the Board\"), but its actual value is never stated in any filing reviewed."},
)

metric("LCR", "%", [("Liquidity Coverage Ratio", LCR)], p3_sources(),
       note="Only disclosed for FY2025 and FY2024 (Performance Metrics page, p.7 of the FY2025 Annual "
            "Report) - not found in the FY2023 Annual Report or anywhere else for FY2023/FY2022/FY2021.")

bw.add_not_disclosed_metric_sheets(
    ["NSFR", "MREL Ratio"], p3_sources(), per_note={m: NOT_DISCLOSED_NOTE for m in ["NSFR", "MREL Ratio"]},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash (used in)/from operating activities", flow({"FY2025": 22388, "FY2024": -15215, "FY2023": -22867, "FY2022": -3057})),
        ("Net cash flow used in investing activities", flow({"FY2025": -394, "FY2024": -61, "FY2023": -163, "FY2022": -38})),
        ("Net cash generated from/(used in) financing activities", flow({"FY2025": -606, "FY2024": -564, "FY2023": 24726, "FY2022": -473})),
        ("Cash and cash equivalents at end of year", stock({"FY2025": 121756, "FY2024": 99914, "FY2023": 7127, "FY2022": 5431})),
    ],
    cash_flow_unit="£'000 (conv. from USD)",
    ratios=[
        ("Total Capital Ratio", CAPITAL_RATIO),
        ("LCR", LCR),
    ],
    note="FY2021 cash flow not available (see Cash Flow Statement sheet's source note). Pillar 3 coverage is "
         "very thin - only a combined Capital Ratio (all 5 years) and LCR (FY2025/FY2024 only) are disclosed "
         "anywhere; every other Pillar 3 metric is Not publicly disclosed. Figures are duplicated from the "
         "detail sheets for at-a-glance trend viewing; see each sheet's own source citation.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/FIDBANK UK FINANCIALS.xlsx")
