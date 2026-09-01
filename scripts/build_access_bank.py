import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2024", "FY2023", "FY2022", "FY2021", "FY2020"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}
PREV_YEAR = {"FY2021": "FY2020", "FY2022": "FY2021", "FY2023": "FY2022", "FY2024": "FY2023"}

# ---------------------------------------------------------------
# FX conversion (The Access Bank UK Limited reports in USD; converting to £
# per this project's established FX methodology - see build_smbc.py /
# build_zenith.py / build_uba_uk.py precedent). Same 31 December fiscal
# year-end as Zenith/UBA UK, so the same Bank of England GBP/USD spot/average
# rates apply for the overlapping years (£1 = $X, via poundsterlinglive.com's
# published BoE archive); FY2020 average is new to this workbook (no earlier
# bank in this series needed a full FY2020 column).
# ---------------------------------------------------------------
FX_SPOT = {
    "FY2020": 1.3661,  # 31 Dec 2020
    "FY2021": 1.3521,  # 31 Dec 2021
    "FY2022": 1.2097,  # 30 Dec 2022 (31st was a Saturday)
    "FY2023": 1.2732,  # 29 Dec 2023 (31st was a Sunday)
    "FY2024": 1.2515,  # 31 Dec 2024
}
FX_AVG = {
    "FY2020": 1.2837,
    "FY2021": 1.3752,
    "FY2022": 1.2362,
    "FY2023": 1.2439,
    "FY2024": 1.2782,
}


def cf_flow(usd):
    """Cash flow statement line items, £'000, at that year's average rate.
    The Bank's own Statement of Cash Flows is presented in whole US$ (not
    $'000), so - like build_zenith.py - dividing by the rate then by 1000
    gives £'000."""
    return {y: round(v / FX_AVG[y] / 1000, 1) for y, v in usd.items()}


def cf_stock(usd):
    """Point-in-time cash balance, £'000, at that year's period-end spot rate."""
    return {y: round(v / FX_SPOT[y] / 1000, 1) for y, v in usd.items()}


def cf_opening(usd):
    """Opening cash balance, £'000 - uses the PRIOR year's period-end spot rate
    (same balance as that prior year's closing figure). No FY2020 entry: that
    would require a FY2019 spot rate, which hasn't been sourced for this
    project - left blank rather than guessed (see entity note)."""
    return {y: round(v / FX_SPOT[PREV_YEAR[y]] / 1000, 1) for y, v in usd.items() if y in PREV_YEAR}


def p3_stock(usd_000):
    """Pillar 3 point-in-time figures, £'000 - the Bank's own Pillar 3 tables are
    already in $'000, so (unlike the cash flow statement) no extra /1000 here."""
    return {y: round(v / FX_SPOT[y], 1) for y, v in usd_000.items()}

# ---------------------------------------------------------------
# Source documents
# ---------------------------------------------------------------
BASE = "https://www.theaccessbankukltd.co.uk/wp-content/uploads"
AR2024_URL = f"{BASE}/2025/06/AccessBank_AR2024_Financials-AW.pdf"
AR2023_URL = f"{BASE}/2024/07/ACCESS_BANK_AR_2023_Financial-statements.pdf"
AR2022_URL = f"{BASE}/2023/07/ACCESS_BANK_AR22_Accs.pdf"
AR2021_URL = f"{BASE}/2022/06/ACCESS_BANK_AR_2021_Accounts.pdf"

P3_2023_URL = f"{BASE}/2025/06/PIllar-3-2023.pdf"
P3_2022_URL = f"{BASE}/2024/01/PILLAR-3-DISCLOSURES-2022-Final.pdf"
P3_2021_URL = f"{BASE}/2022/10/PILLAR-3-DISCLOSURES-2021-Final.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: The Access Bank UK Limited (Companies House 06365062, FRN 478415) is a UK subsidiary of Access "
    "Bank Plc (Nigeria); ultimate parent is Access Holdings Plc (Nigeria). Like Zenith Bank (UK) Limited and "
    "United Bank for Africa (UK) Limited elsewhere in this workbook series, it prepares full IFRS financial "
    "statements with a genuine Statement of Cash Flows every year - no FRS 101/102 cash-flow exemption applies. "
    "The Bank's Own Funds consist entirely of Common Equity Tier 1 (CET1) capital (no AT1 or Tier 2 instruments), "
    "so CET1 capital = Tier 1 capital = Total capital in every year shown. The Bank's own website blocks "
    "automated page fetches (Cloudflare bot protection on its HTML pages, though direct PDF links work); its "
    "'Our Reports' page was instead reconstructed via multiple Wayback Machine snapshots (2022-2025) to locate "
    "every year's Annual Report and Pillar 3 Disclosures PDF. Companies House filing history confirms the latest "
    "filed accounts are 'Group of companies' accounts made up to 31 December 2024' (filed 22 Sep 2025) - no "
    "FY2025 Annual Report or Pillar 3 disclosure has been published yet, and no later Pillar 3 edition than the "
    "2023 one has been found (the Bank's Reports page showed only the 2023 edition as of a 16 Nov 2025 Wayback "
    "snapshot, the most recent snapshot available). This workbook therefore covers FY2020-FY2024 (shifted one "
    "year earlier than most other banks in this series, which run FY2021-FY2025) - 5 years of cash flow, but "
    "Pillar 3 metrics only to FY2023 (4 years); FY2024 Pillar 3 cells are blank rather than guessed. From FY2024 "
    "the Bank's own Statement of Cash Flows is presented on both 'Bank' and 'Group' bases (following the "
    "acquisition of an interest in a subsidiary during 2024 - see 'Purchase of share in subsidiary' below); the "
    "Bank (entity-level) column is used throughout this workbook for consistency with every earlier year, when "
    "Bank and Group were identical since no subsidiary existed."
)

FX_NOTE = (
    "FX CONVERSION NOTE: The Access Bank UK Limited reports in US Dollars. This workbook converts every $ amount "
    "to £ for consistency with the rest of this series, following the same methodology established for SMBC Bank "
    "International plc, Zenith Bank (UK) Limited and United Bank for Africa (UK) Limited: point-in-time/balance "
    "figures (capital, RWA, leverage exposure, HQLA, cash balances) use the Bank of England GBP/USD SPOT rate as "
    "at that fiscal year-end (31 December); flow figures (every cash flow statement line item) use the AVERAGE "
    "of Bank of England rates over that calendar year - both via poundsterlinglive.com's published Bank of "
    "England archive. Rates used (£1 = $X): FY2020 spot 1.3661 / average 1.2837; FY2021 spot 1.3521 / average "
    "1.3752; FY2022 spot 1.2097 / average 1.2362; FY2023 spot 1.2732 / average 1.2439; FY2024 spot 1.2515 / "
    "average 1.2782 - identical to the FY2021-FY2024 rates already used for Zenith Bank UK and UBA UK, since all "
    "three share the same 31 December fiscal year-end; FY2020 average is newly sourced for this workbook (no "
    "earlier bank in this series needed a full FY2020 column). All % ratios (CET1/Tier 1/Total Capital/Leverage/"
    "LCR/NSFR ratios) are shown EXACTLY as reported in USD and were NOT converted - a ratio is dimensionless and "
    "currency-invariant. Because stocks and flows are converted at different rates, the cash flow statement "
    "includes an explicit 'Effect of GBP/USD translation' reconciling line (FY2021-FY2024 only, computed "
    "programmatically from the actual converted figures) so opening + all flows + this line = closing exactly in "
    "£ terms for those years - this line is purely an artefact of £ translation and has no bearing on the Bank's "
    "underlying USD results. FY2020's opening cash balance is left blank (not converted) since it would require "
    "a 31 December 2019 spot rate, which hasn't been sourced for this project - FY2020's closing balance and "
    "flow lines ARE populated, just not its opening balance or a translation plug. This conversion was not "
    "explicitly requested for this bank - applied for consistency with the rest of the series, following the "
    "same call already confirmed for Zenith Bank UK and UBA UK; flag if £'000 rather than the Bank's native "
    "US$'000 presentation is not what's wanted here."
)

PRESENTATION_NOTE = (
    "PRESENTATION NOTE: presentation differs slightly between report vintages, each year's own as-reported line "
    "items/labels are preserved rather than forced into a common shape. FY2023/FY2024 split lease payments into "
    "separate 'Lease payments principal' and 'Lease payments interest' rows; FY2020-FY2022 instead show a single "
    "combined 'Lease payments' row (FY2022's own report keeps the combined presentation even though FY2023's "
    "report restates FY2022 as a split comparative - FY2022's own report's combined figure is used here, per "
    "this project's convention of preferring each year's own report). A handful of line items differ by $1-$3 "
    "between a year's own primary statement and its appearance as the following year's comparative column "
    "(immaterial rounding, e.g. FY2021 'Operating cash flows before movements in working capital' is $86,336,098 "
    "in AR2021's own statement vs $86,336,099 in AR2022's comparative) - each year's own primary statement figure "
    "is used throughout."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are The Access Bank UK Limited's own Statement of Cash Flows (converted from USD to "
    "£, see FX conversion note below):\n"
    f"FY2024: Report & Financial Statements 2024, p.23 (Statement of Cash Flows, Bank column) - {AR2024_URL}\n"
    f"FY2023: Report and Financial Statements 2023, p.21 (Statement of Cash Flows) - {AR2023_URL}\n"
    f"FY2022: Report and Statutory Accounts 2022, p.19 (Statement of Cash Flows) - {AR2022_URL}\n"
    f"FY2021 & FY2020: Report and Statutory Accounts 2021, p.17 (Statement of Cash Flows) - {AR2021_URL}\n"
    "Activity-total rows may be off by up to £0.1k from summing the visible line items above them, since each £ "
    "line is independently rounded to 1 decimal place before summing; the full statement ties exactly end-to-end "
    "via the net change, opening balance, exchange-rate-effect and translation-effect lines (verified to the "
    "penny in £'000 terms for FY2021-FY2024; FY2020 has no opening balance, see FX note).\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE + "\n\n" + PRESENTATION_NOTE
)


def p3_sources():
    return (
        "Sources - The Access Bank UK Limited Pillar 3 Disclosures (UK KM1 - Key Metrics template, or the "
        "equivalent UK CC1/LR2 tables for FY2020/FY2021 which pre-date the Bank's KM1 template), converted from "
        "USD to £ where a $ amount (see FX conversion note on the Cash Flow Statement sheet; % ratios are "
        "unconverted):\n"
        f"FY2023 & FY2022: Pillar 3 Disclosures 2023, p.6 (Section 1.7, Key Metrics) - {P3_2023_URL}\n"
        f"FY2021 (capital/leverage): Pillar 3 Disclosures 2021, p.15 (UK CC1) & p.21 (LR2) - {P3_2021_URL}\n"
        f"FY2021 (LCR/NSFR) & FY2020 (capital/leverage): Pillar 3 Disclosures 2022, p.6-7 (Section 1.7 comparative "
        f"column) & Pillar 3 Disclosures 2021, p.15 (UK CC1) & p.21 (LR2) - {P3_2022_URL}\n"
        "No FY2024 Pillar 3 Disclosures document has been found (the Bank's Reports page showed only the 2023 "
        "edition as of the most recent available Wayback Machine snapshot, 16 Nov 2025) - FY2024 cells are blank "
        "rather than guessed. FY2020 LCR/NSFR were not found in any source (narrative-only LCR in the FY2021 "
        "Pillar 3 report gives a single FY2021 point figure, no FY2020 comparative; the UK NSFR framework may not "
        "yet have covered FY2020) - left blank."
    )


bw = BankWorkbook(bank_name="The Access Bank UK Limited", years=YEARS, year_label=YEAR_LABEL, header_color="4B2E39")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (raw USD, then converted via cf_flow()/cf_stock()/cf_opening())
# ---------------------------------------------------------------
rows_usd = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax (expense) for the year", {"FY2024": 173388564, "FY2023": 151529997, "FY2022": 58700008, "FY2021": 51859841, "FY2020": 16828643}),
    ("DATA", "Depreciation", {"FY2024": 3212001, "FY2023": 1800071, "FY2022": 1722134, "FY2021": 1478136, "FY2020": 1742769}),
    ("DATA", "Amortisation", {"FY2024": 952546, "FY2023": 759048, "FY2022": 565746, "FY2021": 429620, "FY2020": 566163}),
    ("DATA", "Impairment charge on financial assets", {"FY2024": 10834839, "FY2023": 8229710, "FY2022": 37271365, "FY2021": 32468250, "FY2020": 58636697}),
    ("DATA", "Interest expense on Lease", {"FY2024": 401164, "FY2023": 65940, "FY2022": 91170, "FY2021": 100251}),
    ("DATA", "Write off of property, plant and equipment", {"FY2023": 13554}),
    ("DATA", "Changes in money market placements", {"FY2024": -6093971, "FY2023": -3558109, "FY2022": 328434, "FY2021": 2582519, "FY2020": 16731994}),
    ("DATA", "Changes in loans and advances to banks and customers", {"FY2024": -555699709, "FY2023": -522765009, "FY2022": -517702261, "FY2021": -102082702, "FY2020": -344428871}),
    ("DATA", "Changes in other assets", {"FY2024": -8665619, "FY2023": 1637826, "FY2022": -6430632, "FY2021": 5945581, "FY2020": -12184644}),
    ("DATA", "Changes in deposits from banks", {"FY2024": 1464499879, "FY2023": 254139555, "FY2022": 259431167, "FY2021": 591802878, "FY2020": -207254914}),
    ("DATA", "Changes in deposits from customers", {"FY2024": 98308227, "FY2023": 199431981, "FY2022": 316415170, "FY2021": 59301364, "FY2020": 95537237}),
    ("DATA", "Changes in other liabilities", {"FY2024": 32975340, "FY2023": 8011361, "FY2022": -786452, "FY2021": -3512265, "FY2020": -297793}),
    ("DATA", "Taxation paid", {"FY2024": -44924329, "FY2023": -38160082, "FY2022": -3757046, "FY2021": -13689454, "FY2020": -21162550}),
    ("TOTAL", "Net cash from/(used in) operating activities", {"FY2024": 1169188932, "FY2023": 61135843, "FY2022": 145848803, "FY2021": 626684019, "FY2020": -395285269}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Net purchase of investment securities", {"FY2024": -1272811576, "FY2023": -309430328, "FY2022": -103968389, "FY2021": -253303827, "FY2020": 60223424}),
    ("DATA", "Purchase of share in subsidiary", {"FY2024": -22224000}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2024": -1364149, "FY2023": -484795, "FY2022": -527124, "FY2021": -145204, "FY2020": -743680}),
    ("DATA", "Purchase of intangible assets", {"FY2024": -4890547, "FY2023": -1641145, "FY2022": -1739101, "FY2021": -740453, "FY2020": -373996}),
    ("TOTAL", "Net cash from/(used in) investing activities", {"FY2024": -1301290272, "FY2023": -311556268, "FY2022": -106234614, "FY2021": -254189484, "FY2020": 59105748}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Issuance of own shares", {"FY2023": 100000000, "FY2022": 65000000}),
    ("DATA", "Lease payments (combined principal & interest)", {"FY2022": -1351378, "FY2021": -1156685, "FY2020": -1331105}),
    ("DATA", "Lease payments principal", {"FY2024": -2771957, "FY2023": -1362355}),
    ("DATA", "Lease payments interest", {"FY2024": -89465, "FY2023": -25495}),
    ("DATA", "Dividends paid", {"FY2024": -26458740, "FY2023": -19793000}),
    ("TOTAL", "Net cash from/(used in) financing activities", {"FY2024": -29320162, "FY2023": 78819150, "FY2022": 63648622, "FY2021": -1156685, "FY2020": -1331105}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2024": -161421502, "FY2023": -171601275, "FY2022": 103262811, "FY2021": 371337850, "FY2020": -337510626}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {"FY2024": 463780357, "FY2023": 634602649, "FY2022": 531094912, "FY2021": 160274778}),
    ("DATA", "Effect of exchange rate fluctuations on cash held", {"FY2024": 257548, "FY2023": 778983, "FY2022": 244926, "FY2021": -517716, "FY2020": 226620}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2024": 302616403, "FY2023": 463780357, "FY2022": 634602649, "FY2021": 531094912, "FY2020": 160274778}),
]

_usd_by_label = {label: usd for _, label, usd in rows_usd}
rows = []
for kind, label, usd in rows_usd:
    if kind == "SECTION":
        rows.append((kind, label, {}))
    elif label == "Cash and cash equivalents at the beginning of the year":
        rows.append((kind, label, cf_opening(usd)))
    elif label == "Cash and cash equivalents at the end of the year":
        rows.append((kind, label, cf_stock(usd)))
    else:
        rows.append((kind, label, cf_flow(usd)))
    if label == "Effect of exchange rate fluctuations on cash held":
        # £ translation plug (see FX_NOTE): stocks (opening/closing) and flows
        # (everything else) are converted at different rates, so the £ statement
        # needs an explicit reconciling line to tie exactly. Computed programmatically
        # from the actual converted figures - only for years with an opening balance
        # in £ (FY2021-FY2024; FY2020 has none, see FX_NOTE).
        opening_gbp = cf_opening(_usd_by_label["Cash and cash equivalents at the beginning of the year"])
        closing_gbp = cf_stock(_usd_by_label["Cash and cash equivalents at the end of the year"])
        net_change_gbp = cf_flow(_usd_by_label["Net increase/(decrease) in cash and cash equivalents"])
        fx_gbp = cf_flow(usd)
        plug = {
            y: round(closing_gbp[y] - opening_gbp[y] - net_change_gbp[y] - fx_gbp.get(y, 0), 1)
            for y in opening_gbp
        }
        rows.append(("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", plug))

bw.add_cash_flow_sheet(
    title="The Access Bank UK Limited — Statement of Cash Flows",
    subtitle="£'000, converted from USD - see source note at bottom for FX methodology and rates used. Bank (entity-level) basis throughout.",
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


CET1_TIER1_TOTAL_USD = {"FY2023": 676944, "FY2022": 486842, "FY2021": 377827, "FY2020": 338920}
RWA_USD = {"FY2023": 3024867, "FY2022": 2459345, "FY2021": 1726764, "FY2020": 1841957}
LEVERAGE_EXPOSURE_USD = {"FY2023": 4246733, "FY2022": 4061990, "FY2021": 3379955, "FY2020": 2595307}
HQLA_USD = {"FY2023": 902038, "FY2022": 1053232, "FY2021": 807121}
NET_CASH_OUTFLOWS_USD = {"FY2023": 246754, "FY2022": 233797, "FY2021": 217760}
NSFR_ASF_USD = {"FY2023": 1878935, "FY2022": 1467825, "FY2021": 1783197}
NSFR_RSF_USD = {"FY2023": 1114383, "FY2022": 992570, "FY2021": 906296}

CET1_RATIO = {"FY2023": "22.4%", "FY2022": "19.8%", "FY2021": "21.88%", "FY2020": "18.40%"}
LEVERAGE_RATIO = {"FY2023": "15.9%", "FY2022": "12.0%", "FY2021": "11.18%", "FY2020": "13.07%"}
LCR_RATIO = {"FY2023": "365.6%", "FY2022": "450.5%", "FY2021": "370.6%"}
NSFR_RATIO = {"FY2023": "168.6%", "FY2022": "147.9%", "FY2021": "196.8%"}

metric("CET1 Capital", "£'000 (conv. from USD)", [("Common Equity Tier 1 (CET1) capital", p3_stock(CET1_TIER1_TOTAL_USD))], p3_sources())
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 (CET1) ratio", CET1_RATIO)], p3_sources())
metric("Tier 1 Capital", "£'000 (conv. from USD)", [("Tier 1 capital", p3_stock(CET1_TIER1_TOTAL_USD))], p3_sources(),
       note="Equal to CET1 capital in every year - the Bank holds no Additional Tier 1 (AT1) instruments.")
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", CET1_RATIO)], p3_sources())
metric("Total Capital", "£'000 (conv. from USD)", [("Total capital", p3_stock(CET1_TIER1_TOTAL_USD))], p3_sources(),
       note="Equal to CET1/Tier 1 capital in every year - the Bank holds no AT1 or Tier 2 instruments.")
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", CET1_RATIO)], p3_sources())
metric("Total RWAs", "£'000 (conv. from USD)", [("Total risk-weighted exposure amount", p3_stock(RWA_USD))], p3_sources())

metric(
    "Leverage Ratio", "£'000 / % (conv. from USD)",
    [
        ("Total exposure measure", p3_stock(LEVERAGE_EXPOSURE_USD)),
        ("Leverage ratio (%)", LEVERAGE_RATIO),
    ],
    p3_sources(),
    note="FY2020/FY2021 source tables (UK LR2, in the FY2021 Pillar 3 report) label this 'including claims on "
         "central banks'; FY2022 onward (UK KM1 template) labels it 'excluding claims on central banks'. Despite "
         "the differing labels, the FY2021 figure is identical (3,379,955) in both the FY2021 report's own table "
         "and the FY2022 report's comparative column, so this appears to be inconsistent wording by the Bank "
         "rather than a genuine methodology change - shown here as a single continuous row, flagged for visibility.",
)

metric(
    "LCR", "£'000 / % (conv. from USD)",
    [
        ("Total high-quality liquid assets (HQLA), weighted value", p3_stock(HQLA_USD)),
        ("Total net cash outflows, adjusted value", p3_stock(NET_CASH_OUTFLOWS_USD)),
        ("Liquidity Coverage Ratio (%)", LCR_RATIO),
    ],
    p3_sources(),
    note="FY2021's $ breakdown (HQLA/net cash outflows) is sourced from the FY2022 Pillar 3 report's comparative "
         "column - the FY2021 Pillar 3 report itself only states a single narrative LCR percentage (343.9%, "
         "a slightly different figure from the 370.6% shown here), not a KM1-style table with a $ breakdown. The "
         "two FY2021 percentages differ slightly, most likely because the narrative figure is a different point-"
         "in-time/averaging convention than the KM1 template's 'average of preceding twelve months' basis used "
         "here - both are the Bank's own disclosures, this workbook uses the KM1-consistent figure. FY2020 not "
         "found in any source.",
)

metric(
    "NSFR", "£'000 / % (conv. from USD)",
    [
        ("Total available stable funding", p3_stock(NSFR_ASF_USD)),
        ("Total required stable funding", p3_stock(NSFR_RSF_USD)),
        ("Net Stable Funding Ratio (%)", NSFR_RATIO),
    ],
    p3_sources(),
    note="FY2021's $ breakdown is sourced from the FY2022 Pillar 3 report's comparative column (the FY2021 "
         "report itself does not tabulate NSFR). FY2020 not found in any source.",
)

bw.add_not_disclosed_metric_sheets(["MREL Ratio"], p3_sources(),
    per_note={"MREL Ratio": "No MREL disclosure (numeric or qualitative) or UK KM2 template found in any year's "
                             "Pillar 3 report - not explicitly stated as an exemption, but consistent with the "
                             "Bank's small size relative to typical MREL-in-scope thresholds."})

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
cf_totals_usd = {
    "Net cash from/(used in) operating activities": {"FY2024": 1169188932, "FY2023": 61135843, "FY2022": 145848803, "FY2021": 626684019, "FY2020": -395285269},
    "Net cash from/(used in) investing activities": {"FY2024": -1301290272, "FY2023": -311556268, "FY2022": -106234614, "FY2021": -254189484, "FY2020": 59105748},
    "Net cash from/(used in) financing activities": {"FY2024": -29320162, "FY2023": 78819150, "FY2022": 63648622, "FY2021": -1156685, "FY2020": -1331105},
}
cf_close_usd = {"FY2024": 302616403, "FY2023": 463780357, "FY2022": 634602649, "FY2021": 531094912, "FY2020": 160274778}

bw.add_overview_sheet(
    cash_flow_totals=[(label, cf_flow(vals)) for label, vals in cf_totals_usd.items()]
                      + [("Cash and cash equivalents at end of year", cf_stock(cf_close_usd))],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Tier 1 Ratio", CET1_RATIO),
        ("Total Capital Ratio", CET1_RATIO),
        ("Leverage Ratio", LEVERAGE_RATIO),
        ("LCR", LCR_RATIO),
        ("NSFR", NSFR_RATIO),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation. All £ figures are converted from the Bank's native USD reporting (see Cash Flow Statement "
         "sheet's FX conversion note) - this conversion was not explicitly requested for this bank but applied for "
         "consistency with the rest of the series. This workbook covers FY2020-FY2024 (shifted one year earlier "
         "than most other banks in this series) since no FY2025 Annual Report has been published yet; Pillar 3 "
         "cells are blank for FY2024 (no edition found) and FY2020 LCR/NSFR (not found in any source).",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/ACCESS BANK UK FINANCIALS.xlsx")
