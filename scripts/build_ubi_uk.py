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


def _stock1(v, y):
    """Single-value point-in-time conversion (see stock() for the dict form) - used by the
    ST-035 Balance Sheet/Equity/Asset Quality/RWA Breakdown sheets, which build up their
    year-dicts from per-year USD dicts rather than one dict-per-line-item."""
    return round(v / FX_SPOT[y], 1)


def _flow1(v, y):
    """Single-value flow conversion (see flow() for the dict form) - used by the ST-035
    Income Statement/Equity sheets."""
    return round(v / FX_AVG[y], 1)


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
P3_2021_URL = f"{BASE}/Pillar_III_%20Disclosures_(2020-21).pdf"

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
# ST-035: Balance Sheet, Profit & Loss, Statement of Changes in Equity,
# Asset Quality, RWA Breakdown. All figures are Union Bank of India (UK)
# Limited's own reported USD'000 figures, converted to £ using the same
# stock()/flow() methodology as the Cash Flow Statement sheet - see
# FX_NOTE. Each year uses that year's own originally-published report
# (not a later restated comparative) except FY2021, which - consistent
# with the existing Cash Flow Statement/Pillar 3 sheets in this workbook
# - is sourced from the FY2022 Annual Report/Pillar 3 Disclosure's own
# comparative column (no dedicated FY2021 report exists).
# ---------------------------------------------------------------
STATEMENTS_RESTATEMENT_NOTE = (
    "RESTATEMENT NOTE: the FY2024 Annual Report's own FY2023 comparative Balance Sheet is labelled '(Restated)' and "
    "differs from FY2023's own originally-published figures (e.g. Total Assets $482,454k restated vs $483,606k as "
    "originally reported in the FY2023 Annual Report; Total Liabilities $368,617k restated vs $369,770k as "
    "originally reported) - the underlying reclassification is not explained in either report. Per this project's "
    "convention of preferring each year's own report over a later restated comparative, FY2023's Balance Sheet/"
    "Profit & Loss/Equity figures throughout this workbook use the FY2023 Annual Report's own originally-published "
    "figures, not the FY2024 report's restated comparative.\n\n"
    "ROUNDING NOTE: the Bank's own Statement of Changes in Equity closing balances for FY2022 and FY2023 differ from "
    "that same year's own Balance Sheet Total equity/Accumulated losses figures by exactly $1k (e.g. FY2022 ladder "
    "closing Accumulated losses $(33,446)k vs Balance Sheet $(33,447)k; FY2023 ladder closing Total equity $113,838k "
    "vs Balance Sheet $113,837k) - a genuine rounding artefact within the Bank's own source documents, not a "
    "transcription error here. The Balance Sheet's own figures are used as each year's authoritative Total equity; "
    "the equity ladder's own movement figures (profit/loss, OCI) are used for that year's movements; the resulting "
    "$1k gap is absorbed into the 'Effect of GBP/USD translation' reconciling row alongside the FX rate-differential "
    "effect (see FX_NOTE) rather than silently adjusted away."
)

BS_SOURCES = (
    "Sources - all figures are Union Bank of India (UK) Limited's own Statement of Financial Position (converted "
    "from USD to £, see FX conversion note below):\n"
    f"FY2025: Annual Report and Financial Statements, year ended 31 March 2025, p.32-33 (Statement of Financial Position) - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements, year ended 31 March 2024, p.25-26 (Statement of Financial Position) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements, year ended 31 March 2023, p.24-25 (Statement of Financial Position) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements, year ended 31 March 2022, p.32-33 (Statement of Financial Position) - {AR2022_URL}\n"
    f"FY2021: as presented in the FY2022 Annual Report's own comparative column (p.32-33) - {AR2022_URL}\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE + "\n\n" + STATEMENTS_RESTATEMENT_NOTE
)

IS_SOURCES = (
    "Sources - all figures are Union Bank of India (UK) Limited's own Income Statement / Statement of Other "
    "Comprehensive Income (converted from USD to £, see FX conversion note below):\n"
    f"FY2025: Annual Report and Financial Statements, year ended 31 March 2025, p.30-31 (Income Statement / Statement of Other Comprehensive Income) - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements, year ended 31 March 2024, p.23-24 (Income Statement / Statement of Other Comprehensive Income) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements, year ended 31 March 2023, p.22-23 (Income Statement / Statement of Other Comprehensive Income) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements, year ended 31 March 2022, p.30-31 (Income Statement / Statement of Other Comprehensive Income) - {AR2022_URL}\n"
    f"FY2021: as presented in the FY2022 Annual Report's own comparative column (p.30-31) - {AR2022_URL}\n"
    "Presentation note: a standalone 'Finance Cost' line only appears from FY2023 onward - FY2021/FY2022's own "
    "reports fold this into 'Other expenses' instead (both years' own 'Operating expenses before impairment loss "
    "allowances' subtotal is unaffected either way; the FY2021/FY2022 rows are left blank for the 'Finance Cost' "
    "line rather than estimating a split). No taxation was charged or credited in any year shown.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE
)

EQ_SOURCES = (
    "Sources - Union Bank of India (UK) Limited's own Statement of Changes in Equity (converted from USD to £; "
    "opening/closing balances at that year-end's SPOT rate, in-year movements at that year's AVERAGE rate - see FX "
    "conversion note on the Cash Flow Statement sheet):\n"
    f"FY2025: Annual Report and Financial Statements, year ended 31 March 2025, p.34 - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements, year ended 31 March 2024, p.27 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements, year ended 31 March 2023, p.26 - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements, year ended 31 March 2022, p.34 - {AR2022_URL}\n"
    f"FY2021: as presented in the FY2022 Annual Report's own comparative column (p.34) - {AR2022_URL}\n"
    f"Opening balance at 1 April 2020: as presented in the FY2022 Annual Report's own comparative column (p.34) - {AR2022_URL}\n\n"
    "'Effect of GBP/USD translation' rows are computed programmatically (closing balance at spot, less opening "
    "balance at prior year's spot, less that year's movements at average rate) - they absorb both the FX "
    "rate-differential (opening/closing use spot, movements use average - see FX_NOTE) and the Bank's own $1k "
    "source-document rounding artefacts in FY2022/FY2023 (see ROUNDING NOTE on the Balance Sheet sheet). This Bank "
    "has no share issuances, treasury shares, share-based payments, or FX/translation reserve movements in any year "
    "shown - the only two equity-component columns are Fair value reserves and Retained earnings (plus static "
    "Issued capital).\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE
)

AQ_SOURCES = (
    "Sources - Union Bank of India (UK) Limited's own IFRS 9 credit quality note for Loans and advances to "
    "customers (converted from USD to £ at each year-end's SPOT rate - a point-in-time balance, see FX conversion "
    "note on the Cash Flow Statement sheet):\n"
    f"FY2025: Annual Report and Financial Statements, year ended 31 March 2025, p.58 (IFRS 9 Credit Quality) - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements, year ended 31 March 2024, p.51 (IFRS 9 Credit Quality) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements, year ended 31 March 2023, p.51 (Credit Risk) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements, year ended 31 March 2022, p.64-65 (Credit Risk) - {AR2022_URL}\n"
    f"FY2021: as presented in the FY2022 Annual Report's own comparative column (p.65) - {AR2022_URL}\n\n"
    "'Net amounts receivable' (by stage) sums to a 'Loans and advances to customers (net of impairment, before "
    "unamortised processing fees)' subtotal, which is then bridged to the Balance Sheet's own 'Loans and advances "
    "to customers' line via a 'Less: unamortised portion of processing fees' row - reproducing the Bank's own note "
    "structure exactly (only FY2024/FY2025 disclose this fee bridge explicitly; earlier years' net-by-stage total "
    "ties to the Balance Sheet directly, within $1k rounding - see ROUNDING NOTE on the Balance Sheet sheet). NPL "
    "ratio = Stage 3 gross carrying amount / Total gross carrying amount; Stage 3 coverage ratio = Stage 3 "
    "impairment provision / Stage 3 gross carrying amount; overall ECL coverage ratio = Total impairment provision "
    "/ Total gross carrying amount - all derived, not separately disclosed by the Bank.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE
)

RWA_SOURCES = (
    "Sources - Union Bank of India (UK) Limited's own Pillar 3 UK OV1 (Overview of risk-weighted exposure amounts) "
    "disclosure, or its pre-UK-OV1-template equivalent for FY2022/FY2021 (converted from USD to £ at each "
    "year-end's SPOT rate; see FX conversion note on the Cash Flow Statement sheet):\n"
    f"FY2025: Pillar 3 Disclosure 2024-25, p.7-8 (UK OV1) - {P3_2025_URL}\n"
    f"FY2024: Pillar 3 Disclosure 2023-24, p.7-8 (UK OV1) - {P3_2024_URL}\n"
    f"FY2023: Pillar III Disclosure 2022-23, p.7-8 (UK OV1) - {P3_2023_URL}\n"
    f"FY2022: Pillar 3 Disclosure 2022, p.28 (3.5 Overview of total RWA) - {P3_2022_URL}\n"
    f"FY2021: Pillar 3 Disclosure 2021, p.26 (3.5 Overview of total RWA) - {P3_2021_URL}\n\n"
    "PRESENTATION NOTE: FY2021/FY2022's own Pillar 3 Disclosures predate the Bank's adoption of the UK OV1 template "
    "- both years' own '3.5 Overview of total RWA' table groups standardised credit risk together with counterparty "
    "credit risk (excluding CVA) into a single 'Credit risk: Standardised approach' line ($314,895k FY2021 / "
    "$330,859k FY2022), showing CVA separately ($1,018k FY2021 / $347k FY2022) but with no distinct 'Counterparty "
    "credit risk (CCR)' category of its own - reproduced here exactly as presented (the 'Counterparty credit risk "
    "(CCR)' row is left blank for FY2021/FY2022, not populated with an estimate). FY2023 onward uses the UK OV1 "
    "template, which separates 'Credit risk (excluding CCR)' from 'Counterparty credit risk (CCR)' (itself "
    "sub-showing CVA as one component of CCR) - both are populated from FY2023 onward. FY2021's category-level "
    "breakdown ($314,895k + $1,018k + $6,003k market risk + $21,231k operational risk) sums to exactly $343,147k, "
    "reconciling to the Total RWAs headline figure already on file for that year.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE
)

# --- Balance Sheet ---
BS_USD = {
    "FY2021": dict(cash=6150, lab=8000, lac=256757, fi_am=17329, fi_fvtpl=1316, deriv_a=1436, fi_fvoci=98207, ppe=978, intang=99, cwip=41, other_assets=902, total_assets=391215,
                   dep_banks=0, dep_cust=271130, repo=5223, deriv_l=0, provisions=114, other_liab=2930, total_liab=279397,
                   share_cap=150000, fv_res=537, acc_loss=-38719, total_equity=111818),
    "FY2022": dict(cash=5170, lab=19194, lac=286830, fi_am=11796, fi_fvtpl=1450, deriv_a=0, fi_fvoci=75923, ppe=644, intang=151, cwip=0, other_assets=1447, total_assets=402605,
                   dep_banks=6011, dep_cust=275587, repo=5149, deriv_l=586, provisions=113, other_liab=1915, total_liab=289361,
                   share_cap=150000, fv_res=-3309, acc_loss=-33447, total_equity=113244),
    "FY2023": dict(cash=18856, lab=57971, lac=318969, fi_am=6875, fi_fvtpl=2232, deriv_a=224, fi_fvoci=77408, ppe=239, intang=132, cwip=0, other_assets=700, total_assets=483606,
                   dep_banks=35826, dep_cust=332484, repo=0, deriv_l=0, provisions=113, other_liab=1347, total_liab=369770,
                   share_cap=150000, fv_res=-4582, acc_loss=-31581, total_equity=113837),
    "FY2024": dict(cash=8336, lab=43027, lac=339650, fi_am=4983, fi_fvtpl=3270, deriv_a=0, fi_fvoci=103558, ppe=5207, intang=71, cwip=0, other_assets=1402, total_assets=509504,
                   dep_banks=0, dep_cust=387541, repo=0, deriv_l=194, provisions=172, other_liab=4714, total_liab=392621,
                   share_cap=150000, fv_res=-3024, acc_loss=-30093, total_equity=116883),
    "FY2025": dict(cash=14195, lab=20202, lac=340434, fi_am=1997, fi_fvtpl=2761, deriv_a=0, fi_fvoci=94823, ppe=4586, intang=18, cwip=0, other_assets=2001, total_assets=481017,
                   dep_banks=0, dep_cust=348633, repo=15240, deriv_l=1436, provisions=184, other_liab=3924, total_liab=369417,
                   share_cap=150000, fv_res=-1699, acc_loss=-36701, total_equity=111600),
}


def bs_line(key):
    return {y: _stock1(d[key], y) for y, d in BS_USD.items() if d.get(key) is not None}


bw.add_balance_sheet_sheet(
    title="Union Bank of India (UK) Limited — Statement of Financial Position",
    subtitle="£'000, converted from USD - see source note at bottom for FX methodology and rates used.",
    rows=[
        ("SECTION", "Assets", {}),
        ("DATA", "Cash and cash equivalents", bs_line("cash")),
        ("DATA", "Loans and advances to Banks", bs_line("lab")),
        ("DATA", "Loans and advances to customers", bs_line("lac")),
        ("DATA", "Financial investments (amortised cost)", bs_line("fi_am")),
        ("DATA", "Financial investments (FVTPL)", bs_line("fi_fvtpl")),
        ("DATA", "Derivative financial instruments (assets)", bs_line("deriv_a")),
        ("DATA", "Financial investments (FVOCI)", bs_line("fi_fvoci")),
        ("DATA", "Property, plant and equipment", bs_line("ppe")),
        ("DATA", "Intangible assets", bs_line("intang")),
        ("DATA", "Capital work in progress", bs_line("cwip")),
        ("DATA", "Other assets", bs_line("other_assets")),
        ("TOTAL", "Total Assets", bs_line("total_assets")),
        ("SECTION", "Liabilities", {}),
        ("DATA", "Deposits from Banks", bs_line("dep_banks")),
        ("DATA", "Deposits from customers", bs_line("dep_cust")),
        ("DATA", "Repurchase agreements", bs_line("repo")),
        ("DATA", "Derivative financial instruments (liabilities)", bs_line("deriv_l")),
        ("DATA", "Provisions", bs_line("provisions")),
        ("DATA", "Other liabilities", bs_line("other_liab")),
        ("TOTAL", "Total Liabilities", bs_line("total_liab")),
        ("SECTION", "Equity", {}),
        ("DATA", "Share capital", bs_line("share_cap")),
        ("DATA", "Fair value reserves", bs_line("fv_res")),
        ("DATA", "Accumulated losses", bs_line("acc_loss")),
        ("TOTAL", "Total Shareholder's equity", bs_line("total_equity")),
    ],
    sources_text=BS_SOURCES,
    first_col_width=64,
    source_height=380,
    unit_suffix=" (£'000, conv. from USD)",
)

# --- Profit & Loss ---
IS_USD = {
    "FY2021": dict(int_inc=13690, int_exp=-4823, nii=8867, fee_inc=366, trading=30, other_inc=1026, derecog=237, total_op_inc=10526,
                   personnel=-3173, dep_amort=-528, finance_cost=None, other_exp=-3171, op_exp_before_impair=-6872, op_profit_before_impair=3654,
                   impair=-14789, fv_fx=197, pbt=-10939, tax=0, pat=-10939, oci=1749, tci=-9190),
    "FY2022": dict(int_inc=11415, int_exp=-3219, nii=8196, fee_inc=782, trading=18, other_inc=808, derecog=0, total_op_inc=9804,
                   personnel=-3809, dep_amort=-518, finance_cost=None, other_exp=-3424, op_exp_before_impair=-7751, op_profit_before_impair=2053,
                   impair=3129, fv_fx=91, pbt=5273, tax=0, pat=5273, oci=-3846, tci=1427),
    "FY2023": dict(int_inc=19884, int_exp=-6912, nii=12972, fee_inc=573, trading=-66, other_inc=882, derecog=None, total_op_inc=14361,
                   personnel=-3881, dep_amort=-514, finance_cost=-149, other_exp=-2818, op_exp_before_impair=-7362, op_profit_before_impair=6999,
                   impair=-5066, fv_fx=-67, pbt=1866, tax=0, pat=1866, oci=-1273, tci=593),
    "FY2024": dict(int_inc=31029, int_exp=-16852, nii=14177, fee_inc=712, trading=46, other_inc=1494, derecog=None, total_op_inc=16429,
                   personnel=-4456, dep_amort=-649, finance_cost=-304, other_exp=-4064, op_exp_before_impair=-9473, op_profit_before_impair=6956,
                   impair=-5593, fv_fx=125, pbt=1488, tax=0, pat=1488, oci=1558, tci=3046),
    "FY2025": dict(int_inc=32247, int_exp=-19934, nii=12313, fee_inc=583, trading=-204, other_inc=635, derecog=None, total_op_inc=13327,
                   personnel=-5063, dep_amort=-685, finance_cost=-466, other_exp=-3520, op_exp_before_impair=-9734, op_profit_before_impair=3593,
                   impair=-10245, fv_fx=44, pbt=-6608, tax=0, pat=-6608, oci=1325, tci=-5283),
}


def is_line(key):
    return {y: _flow1(d[key], y) for y, d in IS_USD.items() if d.get(key) is not None}


bw.add_income_statement_sheet(
    title="Union Bank of India (UK) Limited — Income Statement & Statement of Other Comprehensive Income",
    subtitle="£'000, converted from USD - see source note at bottom for FX methodology and rates used.",
    rows=[
        ("SECTION", "Income", {}),
        ("DATA", "Interest and similar income", is_line("int_inc")),
        ("DATA", "Interest and similar expense", is_line("int_exp")),
        ("TOTAL", "Net interest income", is_line("nii")),
        ("DATA", "Fees and commission income", is_line("fee_inc")),
        ("DATA", "Net trading income/(expense)", is_line("trading")),
        ("DATA", "Net other operating income", is_line("other_inc")),
        ("DATA", "Derecognition gain", is_line("derecog")),
        ("TOTAL", "Total Operating income", is_line("total_op_inc")),
        ("DATA", "Personnel costs", is_line("personnel")),
        ("DATA", "Depreciation and amortisation", is_line("dep_amort")),
        ("DATA", "Finance Cost", is_line("finance_cost")),
        ("DATA", "Other expenses", is_line("other_exp")),
        ("TOTAL", "Operating expenses before impairment loss allowances", is_line("op_exp_before_impair")),
        ("TOTAL", "Operating profit before impairment loss allowances", is_line("op_profit_before_impair")),
        ("DATA", "Impairment loss allowances/(reversal)", is_line("impair")),
        ("DATA", "Fair value gain/(loss) on Foreign Exchange Derivatives", is_line("fv_fx")),
        ("TOTAL", "Profit/(Loss) before tax", is_line("pbt")),
        ("DATA", "Corporation tax (charge)/credit", is_line("tax")),
        ("TOTAL", "Profit/(Loss) after tax", is_line("pat")),
        ("SECTION", "Other comprehensive income", {}),
        ("DATA", "Fair value gain/(loss) on FVTOCI debt instruments", is_line("oci")),
        ("TOTAL", "Total comprehensive income/(loss) for the year", is_line("tci")),
    ],
    sources_text=IS_SOURCES,
    first_col_width=64,
    source_height=340,
    unit_suffix=" (£'000, conv. from USD)",
)

# --- Statement of Changes in Equity ---
EQ_HEADERS = ["Issued capital", "Fair value reserves", "Retained earnings", "Total equity"]
EQ_BALANCES_USD = {
    "FY2020_open": (150000, -1211, -27781, 121008),
    "FY2021_close": (150000, 537, -38719, 111818),
    "FY2022_close": (150000, -3309, -33447, 113244),
    "FY2023_close": (150000, -4582, -31581, 113837),
    "FY2024_close": (150000, -3024, -30093, 116883),
    "FY2025_close": (150000, -1699, -36701, 111600),
}
EQ_MOVEMENTS_USD = {
    "FY2021": dict(profit=-10939, oci=1749, tci=-9190),
    "FY2022": dict(profit=5273, oci=-3846, tci=1427),
    "FY2023": dict(profit=1866, oci=-1273, tci=593),
    "FY2024": dict(profit=1488, oci=1558, tci=3046),
    "FY2025": dict(profit=-6608, oci=1325, tci=-5283),
}
EQ_OPEN_KEY = {"FY2021": "FY2020_open", "FY2022": "FY2021_close", "FY2023": "FY2022_close", "FY2024": "FY2023_close", "FY2025": "FY2024_close"}
EQ_OPEN_SPOT_YEAR = {"FY2021": "FY2020", "FY2022": "FY2021", "FY2023": "FY2022", "FY2024": "FY2023", "FY2025": "FY2024"}
EQ_CLOSE_KEY = {"FY2021": "FY2021_close", "FY2022": "FY2022_close", "FY2023": "FY2023_close", "FY2024": "FY2024_close", "FY2025": "FY2025_close"}
EQ_CLOSE_LABEL = {"FY2021": "31 March 2021", "FY2022": "31 March 2022", "FY2023": "31 March 2023", "FY2024": "31 March 2024", "FY2025": "31 March 2025"}
EQ_OPEN_LABEL = {"FY2021": "1 April 2020", "FY2022": "31 March 2021", "FY2023": "31 March 2022", "FY2024": "31 March 2023", "FY2025": "31 March 2024"}

EQ_ROWS = []
_eq_years_chrono = ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025"]
for i, y in enumerate(_eq_years_chrono):
    ob = EQ_BALANCES_USD[EQ_OPEN_KEY[y]]
    cb = EQ_BALANCES_USD[EQ_CLOSE_KEY[y]]
    oy = EQ_OPEN_SPOT_YEAR[y]
    ob_gbp = tuple(_stock1(v, oy) for v in ob)
    cb_gbp = tuple(_stock1(v, y) for v in cb)
    m = EQ_MOVEMENTS_USD[y]
    profit_gbp = _flow1(m["profit"], y)
    oci_gbp = _flow1(m["oci"], y)
    tci_gbp = _flow1(m["tci"], y)
    plug = (
        round(cb_gbp[0] - ob_gbp[0], 1),
        round(cb_gbp[1] - ob_gbp[1] - oci_gbp, 1),
        round(cb_gbp[2] - ob_gbp[2] - profit_gbp, 1),
        round(cb_gbp[3] - ob_gbp[3] - tci_gbp, 1),
    )
    if i == 0:
        EQ_ROWS.append(("TOTAL", f"Balance as at {EQ_OPEN_LABEL[y]}", ob_gbp))
    profit_label = "(Loss)/Profit for the year" if m["profit"] < 0 else "Profit for the year"
    EQ_ROWS.append(("DATA", profit_label, (None, None, profit_gbp, profit_gbp)))
    EQ_ROWS.append(("DATA", "Other comprehensive income/(expense) - FV movement on FVTOCI debt instruments", (None, oci_gbp, None, oci_gbp)))
    tci_label = "Total comprehensive (loss)/income for the year" if m["tci"] < 0 else "Total comprehensive income for the year"
    EQ_ROWS.append(("TOTAL", tci_label, (None, None, None, tci_gbp)))
    EQ_ROWS.append(("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", plug))
    EQ_ROWS.append(("TOTAL", f"Balance as at {EQ_CLOSE_LABEL[y]}", cb_gbp))

bw.add_equity_changes_sheet(
    title="Union Bank of India (UK) Limited — Statement of Changes in Equity",
    subtitle="£'000, converted from USD - chronological 1 April 2020 through 31 March 2025 - see source note for FX methodology.",
    headers=EQ_HEADERS,
    rows=EQ_ROWS,
    sources_text=EQ_SOURCES,
    first_col_width=70,
    source_height=380,
)

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
# Asset Quality (loan book by IFRS 9 stage, £'000 converted from USD at
# each year-end's spot rate) - placed after Cash Flow Statement, before
# the Pillar 3 sheets.
# ---------------------------------------------------------------
AQ_USD = {
    "FY2021": dict(s1_gross=208754, s2_gross=25739, s3_gross=83031, total_gross=317525,
                   s1_ecl=-2691, s2_ecl=-2212, s3_ecl=-55865, total_ecl=-60767,
                   s1_net=206064, s2_net=23528, s3_net=27166, total_net=256758, fee_bridge=None),
    "FY2022": dict(s1_gross=256441, s2_gross=6689, s3_gross=41018, total_gross=304148,
                   s1_ecl=-1892, s2_ecl=-611, s3_ecl=-14815, total_ecl=-17318,
                   s1_net=254549, s2_net=6078, s3_net=26203, total_net=286830, fee_bridge=None),
    "FY2023": dict(s1_gross=286278, s2_gross=8700, s3_gross=40298, total_gross=335276,
                   s1_ecl=-789, s2_ecl=-48, s3_ecl=-15470, total_ecl=-16307,
                   s1_net=285489, s2_net=8652, s3_net=24828, total_net=318969, fee_bridge=None),
    "FY2024": dict(s1_gross=290852, s2_gross=19502, s3_gross=51973, total_gross=362327,
                   s1_ecl=-1776, s2_ecl=-349, s3_ecl=-19682, total_ecl=-21807,
                   s1_net=289076, s2_net=19153, s3_net=32291, total_net=340520, fee_bridge=-870),
    "FY2025": dict(s1_gross=281344, s2_gross=38295, s3_gross=42424, total_gross=362063,
                   s1_ecl=-1598, s2_ecl=-4440, s3_ecl=-14805, total_ecl=-20843,
                   s1_net=279746, s2_net=33855, s3_net=27619, total_net=341220, fee_bridge=-786),
}


def aq_line(key):
    return {y: _stock1(d[key], y) for y, d in AQ_USD.items() if d.get(key) is not None}


def aq_ratio(numer_key, denom_key, sign=1):
    out = {}
    for y, d in AQ_USD.items():
        n, dn = d.get(numer_key), d.get(denom_key)
        if n is None or dn is None or dn == 0:
            continue
        out[y] = f"{sign * n / dn * 100:.2f}%"
    return out


bw.add_asset_quality_sheet(
    title="Union Bank of India (UK) Limited — Asset Quality (Loans and advances to customers, by IFRS 9 stage)",
    subtitle="£'000, converted from USD at each year-end's spot rate - see source note at bottom for FX methodology.",
    rows=[
        ("SECTION", "Gross carrying amount", {}),
        ("DATA", "Stage 1 (12-month ECL)", aq_line("s1_gross")),
        ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", aq_line("s2_gross")),
        ("DATA", "Stage 3 (credit-impaired)", aq_line("s3_gross")),
        ("TOTAL", "Total gross carrying amount", aq_line("total_gross")),
        ("SECTION", "Impairment provision (ECL)", {}),
        ("DATA", "Stage 1 impairment provision", aq_line("s1_ecl")),
        ("DATA", "Stage 2 impairment provision", aq_line("s2_ecl")),
        ("DATA", "Stage 3 impairment provision", aq_line("s3_ecl")),
        ("TOTAL", "Total impairment provision", aq_line("total_ecl")),
        ("SECTION", "Net amounts receivable", {}),
        ("DATA", "Stage 1 net amounts receivable", aq_line("s1_net")),
        ("DATA", "Stage 2 net amounts receivable", aq_line("s2_net")),
        ("DATA", "Stage 3 net amounts receivable", aq_line("s3_net")),
        ("TOTAL", "Total net amounts receivable (before processing-fee bridge)", aq_line("total_net")),
        ("DATA", "Less: unamortised portion of processing fees", aq_line("fee_bridge")),
        ("TOTAL", "Loans and advances to customers (per Balance Sheet)", {y: round(_stock1(d["total_net"], y) + (_stock1(d["fee_bridge"], y) if d.get("fee_bridge") else 0), 1) for y, d in AQ_USD.items()}),
        ("SECTION", "Derived ratios", {}),
        ("DATA", "NPL ratio (Stage 3 gross / Total gross)", aq_ratio("s3_gross", "total_gross")),
        ("DATA", "Stage 3 coverage ratio (Stage 3 ECL / Stage 3 gross)", aq_ratio("s3_ecl", "s3_gross", sign=-1)),
        ("DATA", "Overall ECL coverage ratio (Total ECL / Total gross)", aq_ratio("total_ecl", "total_gross", sign=-1)),
    ],
    sources_text=AQ_SOURCES,
    first_col_width=70,
    source_height=380,
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

# ---------------------------------------------------------------
# RWA Breakdown (placed right after Total RWAs, since it's itself a
# Pillar 3 disclosure) - £'000, converted from USD at each year-end's
# spot rate. See RWA_SOURCES for the FY2021/FY2022 presentation
# difference (pre-UK-OV1-template).
# ---------------------------------------------------------------
RWAB_USD = {
    "FY2021": dict(credit_std=314895, ccr=None, cva=1018, market=6003, op=21231, total=343147),
    "FY2022": dict(credit_std=330859, ccr=None, cva=347, market=1454, op=19990, total=352650),
    "FY2023": dict(credit_std=362454, ccr=1068, cva=334, market=587, op=21077, total=385186),
    "FY2024": dict(credit_std=391024, ccr=3199, cva=999, market=3774, op=23733, total=421729),
    "FY2025": dict(credit_std=375817, ccr=3925, cva=1213, market=2875, op=27304, total=409920),
}


def rwab_line(key):
    return {y: _stock1(d[key], y) for y, d in RWAB_USD.items() if d.get(key) is not None}


bw.add_rwa_breakdown_sheet(
    title="Union Bank of India (UK) Limited — RWA Breakdown (UK OV1 - Overview of risk-weighted exposure amounts)",
    subtitle="£'000, converted from USD - see source note for the FY2021/FY2022 presentation difference (pre-UK-OV1-template).",
    rows=[
        ("DATA", "Credit risk (excluding CCR) / Standardised approach", rwab_line("credit_std")),
        ("DATA", "Counterparty credit risk (CCR)", rwab_line("ccr")),
        ("DATA", "  of which: Credit valuation adjustment (CVA)", rwab_line("cva")),
        ("DATA", "Market risk", rwab_line("market")),
        ("DATA", "Operational risk", rwab_line("op")),
        ("TOTAL", "Total RWAs (risk-weighted exposure amount)", rwab_line("total")),
    ],
    sources_text=RWA_SOURCES,
    first_col_width=64,
    source_height=340,
    unit_suffix=" (£'000, conv. from USD)",
)

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

bs_overview_totals = [
    ("Total assets", bs_line("total_assets")),
    ("Loans and advances to customers", bs_line("lac")),
    ("Deposits from customers", bs_line("dep_cust")),
    ("Total Shareholder's equity", bs_line("total_equity")),
]
is_overview_totals = [
    ("Total Operating income", is_line("total_op_inc")),
    ("Operating expenses before impairment loss allowances", is_line("op_exp_before_impair")),
    ("Profit/(Loss) after tax", is_line("pat")),
]
eq_overview_open = {y: _stock1(EQ_BALANCES_USD[EQ_OPEN_KEY[y]][3], EQ_OPEN_SPOT_YEAR[y]) for y in YEARS if y != "FY2020"}
eq_overview_close = {y: _stock1(EQ_BALANCES_USD[EQ_CLOSE_KEY[y]][3], y) for y in YEARS}
eq_overview_tci = {y: _flow1(EQ_MOVEMENTS_USD[y]["tci"], y) for y in YEARS}
eq_overview_totals = [
    ("Opening equity", eq_overview_open),
    ("Total comprehensive income/(loss) for the year", eq_overview_tci),
    ("Closing equity", eq_overview_close),
]

bw.add_overview_sheet(
    balance_sheet_totals=bs_overview_totals,
    balance_sheet_unit="£'000 (conv. from USD)",
    income_statement_totals=is_overview_totals,
    income_statement_unit="£'000 (conv. from USD)",
    equity_changes_totals=eq_overview_totals,
    equity_changes_unit="£'000 (conv. from USD)",
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
