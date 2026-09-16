import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}
PREV_YEAR = {"FY2020": "FY2019", "FY2021": "FY2020", "FY2022": "FY2021", "FY2023": "FY2022", "FY2024": "FY2023"}

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
    "FY2019": 1.3210,  # 31 Dec 2019, Bank of England XUDLUSS
    "FY2020": 1.3661,  # 31 Dec 2020
    "FY2021": 1.3521,  # 31 Dec 2021
    "FY2022": 1.2097,  # 30 Dec 2022 (31st was a Saturday)
    "FY2023": 1.2732,  # 29 Dec 2023 (31st was a Sunday)
    "FY2024": 1.2515,  # 31 Dec 2024
}
FX_AVG = {
    "FY2019": 1.2767,  # calendar-year average (published BoE-rate archive)
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
AR2019_URL = f"{BASE}/2020/07/ACCE3269_ACCESS_BANK_AR_2019_WEB.pdf"

P3_2020_URL = f"{BASE}/2022/06/PILLAR-3-DISCLOSURES-2020-Clean.pdf"
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
    "snapshot, the most recent snapshot available). This workbook therefore covers FY2019-FY2024 (shifted one "
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
    "three share the same 31 December fiscal year-end; FY2019 spot 1.3210 / average 1.2767 (Bank of England "
    "series XUDLUSS, 31 December 2019; its published calendar-year GBP/USD average). All % ratios (CET1/Tier 1/Total Capital/Leverage/"
    "LCR/NSFR ratios) are shown EXACTLY as reported in USD and were NOT converted - a ratio is dimensionless and "
    "currency-invariant. Because stocks and flows are converted at different rates, the cash flow statement "
    "includes an explicit 'Effect of GBP/USD translation' reconciling line (FY2021-FY2024 only, computed "
    "programmatically from the actual converted figures) so opening + all flows + this line = closing exactly in "
    "£ terms for those years - this line is purely an artefact of £ translation and has no bearing on the Bank's "
    "underlying USD results. This conversion was not "
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
    f"FY2019: Report and Statutory Accounts 2019, p.14 (Statement of Cash Flows) - {AR2019_URL}\n"
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
        f"FY2019: Pillar 3 Disclosures 2020, p.6 (Section 1.7 FY2019 comparative) and p.17/p.20 (Pillar 1 / leverage "
        f"comparatives) - {P3_2020_URL}\n"
        f"FY2024 (capital amounts): Report & Financial Statements 2024, p.59, Note 27g 'Capital management "
        f"(Bank)', 'Capital Resources' table - Total tier 1 capital / Total regulatory capital $750,775,693 "
        f"(shown here as 750,776 $'000 before conversion) - {AR2024_URL}\n"
        "No FY2024 Pillar 3 Disclosures document exists. Re-verified 15 September 2026: nine filename "
        "permutations under the Bank's /wp-content/uploads/ CDN (2025/06, 2025/09, 2025/12, 2026/01, 2026/06, "
        "2026/07 folders) all return the site's 404 page, and a Wayback CDX sweep of the whole domain filtered "
        "on 'pillar' returns exactly five documents, the newest being the 2023 edition. The Bank's HTML pages "
        "return HTTP 403 to both curl and automated fetchers (Cloudflare), so the CDN and Wayback are the only "
        "routes; both agree. The Bank publishes its Pillar 3 roughly 18 months after year-end (the 2023 edition "
        "was uploaded in the 2025/06 folder), so a FY2024 edition would be expected around mid-to-late 2026.\n"
        "For FY2024 the Annual Report substitutes ONLY where the basis is verified identical. The AR's Note 27g "
        "capital table is the same basis as the Pillar 3: its FY2023 comparative of $676,943,850 reproduces the "
        "FY2023 Pillar 3 CET1/Tier 1/Total capital figure of 676,944 $'000 EXACTLY, and the note confirms "
        "'the Bank's regulatory capital consists only of Tier 1 capital', matching the CET1 = Tier 1 = Total "
        "capital treatment used in every other year. The AR's Tier 1 Capital Ratio (20.18%) likewise ties to the "
        "Pillar 3 basis (its FY2023 figure, 22.38%, matches the workbook's 22.4%).\n"
        "NOT substituted for FY2024, and left blank rather than derived: Total RWAs (the AR gives no RWA figure; "
        "back-solving $750,775,693 / 20.18% is refused because the ratio is rounded to 2dp, which spans an RWA "
        "range of roughly $3,719.5m-$3,721.3m); Leverage Ratio (the AR discloses no leverage ratio and no "
        "leverage exposure measure - total assets of $6,125.4m is NOT the exposure measure, which includes "
        "off-balance-sheet items); and NSFR (the AR contains no NSFR or stable-funding disclosure at all - "
        "'stable funding' returns zero hits in the document). FY2020 LCR/NSFR were not found in any source "
        "(narrative-only LCR in the FY2021 Pillar 3 report gives a single FY2021 point figure, no FY2020 "
        "comparative; the UK NSFR framework may not yet have covered FY2020) - left blank."
    )


bw = BankWorkbook(bank_name="The Access Bank UK Limited", years=YEARS, year_label=YEAR_LABEL, header_color="4B2E39")

# ---------------------------------------------------------------
# ST- rollout: shared entity/FX notes reused across the new sheets
# ---------------------------------------------------------------
STATEMENTS_PRESENTATION_NOTE = (
    "PRESENTATION NOTE: The Bank column (entity-level) is used throughout for consistency with the Cash Flow "
    "Statement sheet - Bank and Group are identical for FY2020-FY2023 (no subsidiary existed) and differ only "
    "immaterially for FY2024 (following the Access Bank Malta investment - see Investment in Subsidiary note). "
    "The Balance Sheet's line-item structure changed between report vintages: FY2024/FY2023 (AR2024) present "
    "'Money market placements', 'Investment in subsidiary', 'Deferred tax liability' and a 'Prepaid corporation "
    "tax' asset as separate lines not present in earlier years; FY2022 (AR2022)/FY2021/FY2020 group these "
    "differently (e.g. a single 'Cash at bank' line, no separate money-market-placements or investment-securities "
    "split visible pre-FY2021 in the same granularity). Each year's own as-reported labels/granularity are "
    "preserved rather than forced into a common shape - blank cells indicate that year's report did not disclose "
    "that specific line. The P&L's structure also changed: FY2024/FY2023 use a 'Total operating income' / "
    "'Net operating income' (after ECL) structure; FY2022/FY2021/FY2020 use a similar shape but without the "
    "'Total operating income' subtotal line (ECL is deducted one step later, after 'Other income', directly into "
    "'Net operating income')."
)


def convert_bs_rows(rows_usd):
    """Balance sheet / P&L line items in whole $ -> £'000 at point-in-time
    (BS, spot) or average (P&L, flow) rate - same FX methodology as the
    existing Cash Flow Statement (cf_stock/cf_flow), applied here for
    consistency across the new sheets. Values are already whole $, so this
    additionally divides by 1000 to reach £'000 (matching cf_flow/cf_stock's
    own /1000 step for the Bank's whole-$ cash flow statement)."""
    return rows_usd


def bs_stock(usd):
    return {y: round(v / FX_SPOT[y] / 1000, 1) for y, v in usd.items()}


def bs_flow(usd):
    return {y: round(v / FX_AVG[y] / 1000, 1) for y, v in usd.items()}


# ---------------------------------------------------------------
# Sheet: Balance Sheet (Consolidated Statement of Financial Position)
# ---------------------------------------------------------------
BALANCE_SHEET_SOURCES = (
    "Sources - The Access Bank UK Limited's own Statement of Financial Position (Bank column), converted from "
    "USD to £ per the FX conversion note on the Cash Flow Statement sheet:\n"
    f"FY2024 & FY2023: Report & Financial Statements 2024, p.21 - {AR2024_URL}\n"
    f"FY2022 & FY2021: Report and Statutory Accounts 2022, p.17 - {AR2022_URL}\n"
    f"FY2020: Report and Statutory Accounts 2021, p.15 (comparative column) - {AR2021_URL}\n"
    f"FY2019: Report and Statutory Accounts 2019, p.12 - {AR2019_URL}\n\n"
    "Investment securities breakdown (Bank column) - by issuer type in all years, plus measurement basis "
    "(FVPL/FVOCI) where the Bank separately discloses it:\n"
    f"FY2024 & FY2023: Report & Financial Statements 2024, Note 16 'Investment securities', p.36 - {AR2024_URL}\n"
    f"FY2022 & FY2021: Report and Statutory Accounts 2022, Note 13 'Investment securities', p.30 - {AR2022_URL}\n"
    f"FY2020: Report and Statutory Accounts 2021, Note 13 'Investment securities' (comparative column) - {AR2021_URL}\n"
    f"FY2019: Report and Statutory Accounts 2019, Note 12 'Investment securities', p.27 - {AR2019_URL}\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE + "\n\n" + STATEMENTS_PRESENTATION_NOTE
)

balance_sheet_rows_usd = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents / Cash at bank", {"FY2024": 302616403, "FY2023": 463780357, "FY2022": 634602649, "FY2021": 531094912, "FY2020": 160274778, "FY2019": 497558784}),
    ("DATA", "Money market placements", {"FY2024": 13252505, "FY2023": 7158534, "FY2022": 3600384, "FY2021": 3928474, "FY2020": 6510993, "FY2019": 23239663}),
    ("DATA", "Investment securities - US Treasury bills and government bonds, at FVPL", {"FY2024": 1971422489, "FY2023": 1018686084}),
    ("DATA", "Investment securities - US Treasury bills, at FVOCI", {"FY2024": 319419125, "FY2023": 0}),
    ("DATA", "Investment securities - US Treasury bills and government bonds (measurement basis not separately disclosed pre-FY2023)", {"FY2022": 711513304, "FY2021": 607500000, "FY2020": 355007353, "FY2019": 415118236}),
    ("DATA", "Investment securities - Listed equity securities in financial institutions", {"FY2024": 4095335, "FY2023": 4759367, "FY2022": 2497339, "FY2021": 2546734, "FY2020": 1649819, "FY2019": 2004320}),
    ("TOTAL", "Total investment securities", {"FY2024": 2294936949, "FY2023": 1023445451, "FY2022": 714010643, "FY2021": 610046734, "FY2020": 356657172, "FY2019": 417122556}),
    ("DATA", "Investment in subsidiary", {"FY2024": 22224000}),
    ("DATA", "Loans and advances to banks", {"FY2024": 1774689997, "FY2023": 1376219992, "FY2022": 1269502028, "FY2021": 849457860, "FY2020": 943688846, "FY2019": 674309238}),
    ("DATA", "Loans and advances to customers", {"FY2024": 1669793574, "FY2023": 1523143929, "FY2022": 1114878580, "FY2021": 1054399028, "FY2020": 890496159, "FY2019": 874086599}),
    ("DATA", "Property, plant and equipment", {"FY2024": 2032215, "FY2023": 1138435, "FY2022": 1094451, "FY2021": 944155, "FY2020": 1234891, "FY2019": 2768462}),
    ("DATA", "Right-of-use assets", {"FY2024": 7297760, "FY2023": 2467870, "FY2022": 3832014, "FY2021": 5191262, "FY2020": 4851412}),
    ("DATA", "Intangible assets", {"FY2024": 8596031, "FY2023": 4658030, "FY2022": 3851278, "FY2021": 2677923, "FY2020": 2376663, "FY2019": 2509537}),
    ("DATA", "Other financial/non-financial assets", {"FY2024": 25972576, "FY2023": 19370331, "FY2022": 22937417, "FY2021": 27013191, "FY2020": 31461526, "FY2019": 8004578}),
    ("DATA", "Prepaid corporation tax", {"FY2024": 486548, "FY2023": 186777}),
    ("DATA", "Derivative financial instruments", {"FY2024": 3506088, "FY2023": 1742483}),
    ("TOTAL", "Total assets", {"FY2024": 6125404646, "FY2023": 4423312189, "FY2022": 3768309444, "FY2021": 3084753539, "FY2020": 2397552440, "FY2019": 2499599417}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks", {"FY2024": 3720229334, "FY2023": 2255729461, "FY2022": 2001589908, "FY2021": 1742158743, "FY2020": 1150355865, "FY2019": 1357610779}),
    ("DATA", "Deposits from customers", {"FY2024": 1549953453, "FY2023": 1451645528, "FY2022": 1252213546, "FY2021": 935798374, "FY2020": 876497010, "FY2019": 780959773}),
    ("DATA", "Lease liabilities", {"FY2024": 7268531, "FY2023": 2194027}),
    ("DATA", "Other financial/non-financial liabilities", {"FY2024": 50824896, "FY2023": 28487357, "FY2022": 22937811, "FY2021": 25483781, "FY2020": 30083087, "FY2019": 33836818}),
    ("DATA", "Deferred tax liability", {"FY2024": 2228603, "FY2023": 1202528, "FY2022": 484114, "FY2021": 509917, "FY2020": 395016, "FY2019": 233658}),
    ("DATA", "Derivative financial instruments", {"FY2024": 9995259, "FY2023": 1749163}),
    ("TOTAL", "Total liabilities", {"FY2024": 5340500076, "FY2023": 3741008064, "FY2022": 3277225379, "FY2021": 2703950815, "FY2020": 2057330978, "FY2019": 2172641028}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2024": 372380250, "FY2023": 372380250, "FY2022": 272380250, "FY2021": 207380250, "FY2020": 207380250, "FY2019": 207380250}),
    ("DATA", "Retained earnings", {"FY2024": 417623754, "FY2023": 313703236, "FY2022": 223921592, "FY2021": 178591301, "FY2020": 138095774, "FY2019": 124590741}),
    ("DATA", "Other reserves", {"FY2024": -85871, "FY2023": 1234202, "FY2022": -204214, "FY2021": -155264, "FY2020": -240999, "FY2019": 961}),
    ("DATA", "Currency translation reserve", {"FY2024": -5013563, "FY2023": -5013563, "FY2022": -5013563, "FY2021": -5013563, "FY2020": -5013563, "FY2019": -5013563}),
    ("TOTAL", "Total equity", {"FY2024": 784904570, "FY2023": 682304125, "FY2022": 491084065, "FY2021": 380802724, "FY2020": 340221462, "FY2019": 326958389}),
    ("TOTAL", "Total liabilities and equity", {"FY2024": 6125404646, "FY2023": 4423312189, "FY2022": 3768309444, "FY2021": 3084753539, "FY2020": 2397552440, "FY2019": 2499599417}),
]

balance_sheet_rows = []
for kind, label, usd in balance_sheet_rows_usd:
    balance_sheet_rows.append((kind, label, bs_stock(usd) if kind != "SECTION" else {}))

bw.add_balance_sheet_sheet(
    title="The Access Bank UK Limited — Statement of Financial Position",
    subtitle="£'000, converted from USD, Bank basis - see source note at bottom for FX methodology and rates used.",
    rows=balance_sheet_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=60,
    source_height=260,
    unit_suffix=" (£'000, conv. from USD)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss (Consolidated Statement of Comprehensive Income)
# ---------------------------------------------------------------
INCOME_STATEMENT_SOURCES = (
    "Sources - The Access Bank UK Limited's own Statement of Comprehensive Income (Bank column), converted from "
    "USD to £ per the FX conversion note on the Cash Flow Statement sheet:\n"
    f"FY2024 & FY2023: Report & Financial Statements 2024, p.20 - {AR2024_URL}\n"
    f"FY2022 & FY2021: Report and Statutory Accounts 2022, p.16 - {AR2022_URL}\n"
    f"FY2020: Report and Statutory Accounts 2021, p.14 (comparative column) - {AR2021_URL}\n"
    f"FY2019: Report and Statutory Accounts 2019, p.11 - {AR2019_URL}\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE + "\n\n" + STATEMENTS_PRESENTATION_NOTE
)

income_statement_rows_usd = [
    ("SECTION", "Operating income", {}),
    ("DATA", "Interest income", {"FY2024": 362390387, "FY2023": 274162094, "FY2022": 129813100, "FY2021": 101091990, "FY2020": 98075794, "FY2019": 89865476}),
    ("DATA", "Interest expense", {"FY2024": -154070948, "FY2023": -100413489, "FY2022": -30327185, "FY2021": -17585729, "FY2020": -24571141, "FY2019": -27900771}),
    ("TOTAL", "Net interest income", {"FY2024": 208319439, "FY2023": 173748605, "FY2022": 99485915, "FY2021": 83506261, "FY2020": 73504653, "FY2019": 61964705}),
    ("DATA", "Fee and commission income", {"FY2024": 32739640, "FY2023": 30614509, "FY2022": 29973424, "FY2021": 27143190, "FY2020": 26743396, "FY2019": 22270590}),
    ("DATA", "Fee and commission expense", {"FY2024": -2891533, "FY2023": -1802245, "FY2022": -1995602, "FY2021": -1850925, "FY2020": -1221054, "FY2019": -236711}),
    ("TOTAL", "Net fee and commission income", {"FY2024": 29848107, "FY2023": 28812264, "FY2022": 27977822, "FY2021": 25292265, "FY2020": 25522342, "FY2019": 22033879}),
    ("DATA", "Other income", {"FY2024": 6179206, "FY2023": 5046212, "FY2022": 4019405, "FY2021": 2373856, "FY2020": 1805722, "FY2019": 1435142}),
    ("DATA", "Other operating income", {"FY2021": 8072122}),
    ("TOTAL", "Total operating income", {"FY2024": 244346752, "FY2023": 207607081, "FY2019": 85175567}),
    ("DATA", "Expected credit loss (ECL) allowance / Provision for expected credit losses", {"FY2024": -10834839, "FY2023": -8229710, "FY2022": -37271365, "FY2021": -32468250, "FY2020": -58636697, "FY2019": -258159}),
    ("TOTAL", "Net operating income", {"FY2024": 233511913, "FY2023": 199377371, "FY2022": 94211777, "FY2021": 86776254, "FY2020": 42196020, "FY2019": 85175567}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Personnel expenses", {"FY2024": -38755452, "FY2023": -31872155, "FY2022": -22478062, "FY2021": -22375495, "FY2020": -17055499, "FY2019": -19520635}),
    ("DATA", "Depreciation and amortisation", {"FY2024": -4164547, "FY2023": -2559119, "FY2022": -2287880, "FY2021": -1907756, "FY2020": -2308932, "FY2019": -1762990}),
    ("DATA", "Other expenses", {"FY2024": -17203350, "FY2023": -13416100, "FY2022": -10745827, "FY2021": -10633162, "FY2020": -6002946, "FY2019": -6741801}),
    ("TOTAL", "Total operating expenses", {"FY2024": -60123349, "FY2023": -47847374, "FY2022": -35511769, "FY2021": -34916413, "FY2020": -25367377, "FY2019": -28025426}),
    ("TOTAL", "Profit before tax expense", {"FY2024": 173388564, "FY2023": 151529997, "FY2022": 58700008, "FY2021": 51859841, "FY2020": 16828643, "FY2019": 57150141}),
    ("DATA", "Tax expense / Taxation", {"FY2024": -45661717, "FY2023": -39302942, "FY2022": -13369717, "FY2021": -11364314, "FY2020": -3323610, "FY2019": -12855786}),
    ("TOTAL", "Profit after tax expense for the year", {"FY2024": 127726847, "FY2023": 112227055, "FY2022": 45330291, "FY2021": 40495527, "FY2020": 13505033, "FY2019": 44294355}),
    ("SECTION", "Other comprehensive income/(expense)", {}),
    ("DATA", "Other comprehensive income on investment securities / net profit on FVOCI securities", {"FY2024": -1320073, "FY2023": 1438416, "FY2022": -48950, "FY2021": 85735, "FY2020": -241960, "FY2019": 219314}),
    ("TOTAL", "Total comprehensive income for the year, net of tax", {"FY2024": 126406774, "FY2023": 113665471, "FY2022": 45281341, "FY2021": 40581262, "FY2020": 13263073, "FY2019": 44513669}),
]

income_statement_rows = []
for kind, label, usd in income_statement_rows_usd:
    income_statement_rows.append((kind, label, bs_flow(usd) if kind != "SECTION" else {}))

bw.add_income_statement_sheet(
    title="The Access Bank UK Limited — Statement of Comprehensive Income",
    subtitle="£'000, converted from USD, Bank basis - see source note at bottom for FX methodology and rates used.",
    rows=income_statement_rows,
    sources_text=INCOME_STATEMENT_SOURCES,
    first_col_width=76,
    source_height=260,
    unit_suffix=" (£'000, conv. from USD)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Share capital", "Retained earnings", "Other reserves", "Currency translation reserve", "Total equity"]

EQUITY_CHANGES_SOURCES = (
    "Sources - The Access Bank UK Limited's own Statement of Changes in Equity (Bank basis), converted from USD "
    "to £ (Balance rows at that date's BoE spot rate; movement rows at that calendar year's BoE average rate - "
    "same FX methodology as the Cash Flow Statement sheet):\n"
    f"2024 & 2023 movements: Report & Financial Statements 2024, p.22 - {AR2024_URL}\n"
    f"2022 & 2021 movements: Report and Statutory Accounts 2022, p.18 - {AR2022_URL}\n"
    f"2020 movements: Report and Statutory Accounts 2021, p.16 (comparative column) - {AR2021_URL}\n"
    f"2019 movements: Report and Statutory Accounts 2019, p.13 - {AR2019_URL}\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE + "\n\n"
    "EQUITY SHEET FX CAVEAT: because this roll-forward mixes point-in-time Balance rows (spot rate) with "
    "in-year movement rows (average rate) - the same two-rate approach used for the Cash Flow Statement - each "
    "period's £ closing balance will differ very slightly from £ opening balance + £ movements (unlike the Cash "
    "Flow Statement, this sheet has no natural 'FX translation' line to absorb the difference, so no plug row is "
    "shown here). The underlying USD figures (see rows above) tie out exactly in every period; this is purely a "
    "£ presentation artefact of using two different conversion rates, not a data quality issue.\n\n"
    "PRESENTATION NOTE: FY2022's own statement labels "
    "its 'Proceeds from shares issued' row as part of a combined 'Total comprehensive income for the year' total "
    "(which would overstate that label); this workbook instead reports 'Total comprehensive income for the "
    "year (2022)' as profit + OCI only (excluding the share issuance), with 'Proceeds from shares issued' shown "
    "as its own separate row immediately after - the Balance at 31 December 2022 row still ties to the sum of "
    "all rows in between, this is a relabeling for clarity only, not a change to any figure."
)

equity_changes_rows_usd = [
    ("TOTAL", "Balance as at 1 January 2019", (176653800, 80296386, -218353, -3812620, 252919213)),
    ("DATA", "Profit after tax for the year (2019)", (0, 44294355, 0, 0, 44294355)),
    ("DATA", "Other comprehensive income for the year (2019)", (0, 0, 219314, 0, 219314)),
    ("DATA", "Translation impact on SOCI (2019)", (0, 0, 0, -1200943, -1200943)),
    ("TOTAL", "Total comprehensive income for the year (2019)", (0, 44294355, 219314, -1200943, 43312726)),
    ("DATA", "Proceeds from shares issued (2019)", (33500250, 0, 0, 0, 33500250)),
    ("DATA", "Translation impact on share capital (2019)", (-2773800, 0, 0, 0, -2773800)),
    ("TOTAL", "Balance as at 31 December 2019", (207380250, 124590741, 961, -5013563, 326958389)),
    ("TOTAL", "Balance as at 1 January 2020", (207380250, 124590741, 961, -5013563, 326958389)),
    ("DATA", "Profit after tax for the year (2020)", (0, 13505033, 0, 0, 13505033)),
    ("DATA", "Other comprehensive expense for the year (2020)", (0, 0, -241960, 0, -241960)),
    ("TOTAL", "Total comprehensive income for the year (2020)", (0, 13505033, -241960, 0, 13263073)),
    ("TOTAL", "Balance as at 31 December 2020", (207380250, 138095774, -240999, -5013563, 340221462)),
    ("DATA", "Profit after tax for the year (2021)", (0, 40495527, 0, 0, 40495527)),
    ("DATA", "Other comprehensive income for the year (2021)", (0, 0, 85735, 0, 85735)),
    ("TOTAL", "Total comprehensive income for the year (2021)", (0, 40495527, 85735, 0, 40581262)),
    ("TOTAL", "Balance as at 31 December 2021", (207380250, 178591301, -155264, -5013563, 380802724)),
    ("DATA", "Profit after tax for the year (2022)", (0, 45330291, 0, 0, 45330291)),
    ("DATA", "Other comprehensive expense for the year (2022)", (0, 0, -48950, 0, -48950)),
    ("TOTAL", "Total comprehensive income for the year (2022)", (0, 45330291, -48950, 0, 45281341)),
    ("DATA", "Proceeds from shares issued (2022)", (65000000, 0, 0, 0, 65000000)),
    ("TOTAL", "Balance as at 31 December 2022", (272380250, 223921592, -204214, -5013563, 491084065)),
    ("DATA", "Profit after tax for the year (2023)", (0, 112227055, 0, 0, 112227055)),
    ("DATA", "Other comprehensive income for the year (2023)", (0, 0, 1438416, 0, 1438416)),
    ("TOTAL", "Total comprehensive income for the year (2023)", (0, 112227055, 1438416, 0, 113665471)),
    ("DATA", "Proceeds from shares issued (2023)", (100000000, 0, 0, 0, 100000000)),
    ("DATA", "Dividends declared (2023)", (0, -22445411, 0, 0, -22445411)),
    ("TOTAL", "Balance as at 31 December 2023", (372380250, 313703236, 1234202, -5013563, 682304125)),
    ("DATA", "Profit after tax for the year (2024)", (0, 127726847, 0, 0, 127726847)),
    ("DATA", "Other comprehensive expense for the year (2024)", (0, 0, -1320073, 0, -1320073)),
    ("TOTAL", "Total comprehensive income for the year (2024)", (0, 127726847, -1320073, 0, 126406774)),
    ("DATA", "Dividends declared (2024)", (0, -23806329, 0, 0, -23806329)),
    ("TOTAL", "Balance as at 31 December 2024", (372380250, 417623754, -85871, -5013563, 784904570)),
]

_BALANCE_YEAR = {
    "Balance as at 31 December 2019": "FY2019",
    "Balance as at 31 December 2020": "FY2020", "Balance as at 31 December 2021": "FY2021",
    "Balance as at 31 December 2022": "FY2022", "Balance as at 31 December 2023": "FY2023",
    "Balance as at 31 December 2024": "FY2024",
}
_MOVEMENT_YEAR = {"(2019)": "FY2019", "(2020)": "FY2020", "(2021)": "FY2021", "(2022)": "FY2022", "(2023)": "FY2023", "(2024)": "FY2024"}


def _convert_equity_row(label, values):
    if label == "Balance as at 1 January 2019":
        return tuple(None for _ in values)
    if label == "Balance as at 1 January 2020":
        rate = FX_SPOT["FY2019"]
    elif label in _BALANCE_YEAR:
        rate = FX_SPOT[_BALANCE_YEAR[label]]
    else:
        year = next(y for tag, y in _MOVEMENT_YEAR.items() if tag in label)
        rate = FX_AVG[year]
    return tuple(round(v / rate / 1000, 1) if v is not None else None for v in values)


equity_changes_rows = [
    (kind, label, _convert_equity_row(label, values))
    for kind, label, values in equity_changes_rows_usd
]

bw.add_equity_changes_sheet(
    title="The Access Bank UK Limited — Statement of Changes in Equity",
    subtitle="£'000, converted from USD, Bank basis - chronological, oldest to newest. See source note for FX methodology/caveat.",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQUITY_CHANGES_SOURCES,
    first_col_width=48,
    source_height=280,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (raw USD, then converted via cf_flow()/cf_stock()/cf_opening())
# ---------------------------------------------------------------
rows_usd = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax (expense) for the year", {"FY2024": 173388564, "FY2023": 151529997, "FY2022": 58700008, "FY2021": 51859841, "FY2020": 16828643, "FY2019": 57150141}),
    ("DATA", "Depreciation", {"FY2024": 3212001, "FY2023": 1800071, "FY2022": 1722134, "FY2021": 1478136, "FY2020": 1742769, "FY2019": 304713}),
    ("DATA", "Amortisation", {"FY2024": 952546, "FY2023": 759048, "FY2022": 565746, "FY2021": 429620, "FY2020": 566163, "FY2019": 459017}),
    ("DATA", "Impairment charge on financial assets", {"FY2024": 10834839, "FY2023": 8229710, "FY2022": 37271365, "FY2021": 32468250, "FY2020": 58636697, "FY2019": 282959}),
    ("DATA", "Interest expense on Lease", {"FY2024": 401164, "FY2023": 65940, "FY2022": 91170, "FY2021": 100251}),
    ("DATA", "Write off of property, plant and equipment", {"FY2023": 13554}),
    ("DATA", "Changes in money market placements", {"FY2024": -6093971, "FY2023": -3558109, "FY2022": 328434, "FY2021": 2582519, "FY2020": 16731994, "FY2019": 181311272}),
    ("DATA", "Changes in loans and advances to banks and customers", {"FY2024": -555699709, "FY2023": -522765009, "FY2022": -517702261, "FY2021": -102082702, "FY2020": -344428871, "FY2019": -425790470}),
    ("DATA", "Changes in other assets", {"FY2024": -8665619, "FY2023": 1637826, "FY2022": -6430632, "FY2021": 5945581, "FY2020": -12184644, "FY2019": -572171}),
    ("DATA", "Changes in deposits from banks", {"FY2024": 1464499879, "FY2023": 254139555, "FY2022": 259431167, "FY2021": 591802878, "FY2020": -207254914, "FY2019": -194998930}),
    ("DATA", "Changes in deposits from customers", {"FY2024": 98308227, "FY2023": 199431981, "FY2022": 316415170, "FY2021": 59301364, "FY2020": 95537237, "FY2019": 164335225}),
    ("DATA", "Changes in other liabilities", {"FY2024": 32975340, "FY2023": 8011361, "FY2022": -786452, "FY2021": -3512265, "FY2020": -297793, "FY2019": 7101084}),
    ("DATA", "Taxation paid", {"FY2024": -44924329, "FY2023": -38160082, "FY2022": -3757046, "FY2021": -13689454, "FY2020": -21162550, "FY2019": -11008913}),
    ("TOTAL", "Net cash from/(used in) operating activities", {"FY2024": 1169188932, "FY2023": 61135843, "FY2022": 145848803, "FY2021": 626684019, "FY2020": -395285269, "FY2019": -221426073}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Net purchase of investment securities", {"FY2024": -1272811576, "FY2023": -309430328, "FY2022": -103968389, "FY2021": -253303827, "FY2020": 60223424, "FY2019": -20878365}),
    ("DATA", "Purchase of share in subsidiary", {"FY2024": -22224000}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2024": -1364149, "FY2023": -484795, "FY2022": -527124, "FY2021": -145204, "FY2020": -743680, "FY2019": -400732}),
    ("DATA", "Purchase of intangible assets", {"FY2024": -4890547, "FY2023": -1641145, "FY2022": -1739101, "FY2021": -740453, "FY2020": -373996, "FY2019": -782582}),
    ("TOTAL", "Net cash from/(used in) investing activities", {"FY2024": -1301290272, "FY2023": -311556268, "FY2022": -106234614, "FY2021": -254189484, "FY2020": 59105748, "FY2019": -22061679}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Issuance of own shares", {"FY2023": 100000000, "FY2022": 65000000, "FY2019": 33500250}),
    ("DATA", "Lease payments (combined principal & interest)", {"FY2022": -1351378, "FY2021": -1156685, "FY2020": -1331105}),
    ("DATA", "Lease payments principal", {"FY2024": -2771957, "FY2023": -1362355}),
    ("DATA", "Lease payments interest", {"FY2024": -89465, "FY2023": -25495}),
    ("DATA", "Dividends paid", {"FY2024": -26458740, "FY2023": -19793000}),
    ("TOTAL", "Net cash from/(used in) financing activities", {"FY2024": -29320162, "FY2023": 78819150, "FY2022": 63648622, "FY2021": -1156685, "FY2020": -1331105, "FY2019": 33500250}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2024": -161421502, "FY2023": -171601275, "FY2022": 103262811, "FY2021": 371337850, "FY2020": -337510626, "FY2019": -209987502}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {"FY2024": 463780357, "FY2023": 634602649, "FY2022": 531094912, "FY2021": 160274778, "FY2020": 497558784, "FY2019": 711079568}),
    ("DATA", "Effect of exchange rate fluctuations on cash held", {"FY2024": 257548, "FY2023": 778983, "FY2022": 244926, "FY2021": -517716, "FY2020": 226620, "FY2019": -3533282}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2024": 302616403, "FY2023": 463780357, "FY2022": 634602649, "FY2021": 531094912, "FY2020": 160274778, "FY2019": 497558784}),
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
# Sheet: Asset Quality / Credit Risk Disclosures
# ---------------------------------------------------------------
ASSET_QUALITY_SOURCES = (
    "Sources - The Access Bank UK Limited's own Note 27/24 'Financial instruments - Credit risk' (Group basis; "
    "immaterially different from Bank basis in every year - see entity note), converted from USD to £ at that "
    "year's BoE spot rate (point-in-time balances, same as the Balance Sheet sheet's convention):\n"
    f"FY2024 & FY2023: Report & Financial Statements 2024, p.51-52 (Note 27d, Loans to customers ECL staging table) - {AR2024_URL}\n"
    f"FY2022 & FY2021: Report and Statutory Accounts 2022, p.43 (Note 24d) - {AR2022_URL}\n"
    f"FY2020: Report and Statutory Accounts 2021, p.42 (Note 24d, comparative column) - {AR2021_URL}\n"
    f"FY2019: Report and Statutory Accounts 2019, p.37 (Note 23d) - {AR2019_URL}\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE + "\n\n"
    "PRESENTATION NOTE: the loan-book-by-product split is NOT presented on a consistent basis across all 5 years "
    "- FY2024/FY2023 disclose a GROSS product split (Loans to corporates / secured on property / other secured "
    "personal loans, from Note 18/17); FY2022/FY2021/FY2020 only disclose a NET-of-allowance Retail/Corporate "
    "split (from the credit risk exposure table), not a gross one at that granularity - each row is labelled to "
    "make this explicit, and the 'Total loans and advances to customers' row for each year sums exactly to "
    "whichever rows are populated for that year (gross FY2023-24, net FY2020-22) - do not compare that total "
    "row directly across the gross/net boundary. The by-IFRS-9-stage breakdown below IS on a consistent gross "
    "basis for all 5 years and ties to each year's own Balance Sheet 'Loans and advances to customers' gross "
    "figure. FY2024's Stage 3 loss allowance coverage (0.3%) is much lower than FY2023's (28.7%) - both figures "
    "are as directly reported; the Bank's own notes attribute this to a large trade-finance Stage 3 exposure "
    "($49.9m) that is substantially collateralised by credit insurance, so most of its gross balance is not "
    "provisioned for - flagged here for visibility rather than smoothed over."
)

asset_quality_rows_usd = [
    ("SECTION", "Loan book by product/segment (basis differs by year - see presentation note)", {}),
    ("DATA", "Loans to corporates (gross)", {"FY2024": 1487628136, "FY2023": 1386572738}),
    ("DATA", "Loans secured on property (gross)", {"FY2024": 128950353, "FY2023": 120538545}),
    ("DATA", "Other secured personal loans (gross)", {"FY2024": 80281571, "FY2023": 42417147}),
    ("DATA", "Retail loans, incl. mortgages (net of allowance)", {"FY2022": 151522375, "FY2021": 147076616, "FY2020": 109784290, "FY2019": 110686719}),
    ("DATA", "Corporate loans, incl. mortgages (net of allowance)", {"FY2022": 963356205, "FY2021": 907322412, "FY2020": 780711869, "FY2019": 763399880}),
    ("TOTAL", "Total loans and advances to customers (gross FY2023-24 / net FY2019-22)", {"FY2024": 1696860060, "FY2023": 1549528430, "FY2022": 1114878580, "FY2021": 1054399028, "FY2020": 890496159, "FY2019": 874086599}),
    ("SECTION", "Loan book by IFRS 9 stage (gross carrying amount)", {}),
    ("DATA", "Stage 1 (12-month ECL)", {"FY2024": 1551240901, "FY2023": 1449313581, "FY2022": 1035081471, "FY2021": 927874029, "FY2020": 739050772, "FY2019": 820606770}),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {"FY2024": 57549029, "FY2023": 12145764, "FY2022": 10751443, "FY2021": 16075352, "FY2020": 96821620, "FY2019": 38030710}),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired)", {"FY2024": 88070130, "FY2023": 88069085, "FY2022": 112727842, "FY2021": 185298016, "FY2020": 113059835, "FY2019": 16001216}),
    ("TOTAL", "Total gross carrying amount", {"FY2024": 1696860060, "FY2023": 1549528430, "FY2022": 1158560756, "FY2021": 1129247397, "FY2020": 948932227, "FY2019": 874638696}),
    ("SECTION", "Loss allowance by IFRS 9 stage", {}),
    ("DATA", "Stage 1 loss allowance", {"FY2024": -1362900, "FY2023": -1073251, "FY2022": -775788, "FY2021": -486733, "FY2020": -736544, "FY2019": -151066}),
    ("DATA", "Stage 2 loss allowance", {"FY2024": -25413612, "FY2023": 0, "FY2022": -18442, "FY2021": -44074, "FY2020": -8722790, "FY2019": -401031}),
    ("DATA", "Stage 3 loss allowance", {"FY2024": -289974, "FY2023": -25311250, "FY2022": -42887946, "FY2021": -74317562, "FY2020": -48976734, "FY2019": 0}),
    ("TOTAL", "Total loss allowance", {"FY2024": -27066486, "FY2023": -26384501, "FY2022": -43682176, "FY2021": -74848369, "FY2020": -58436068, "FY2019": -552097}),
]

asset_quality_rows = []
for kind, label, usd in asset_quality_rows_usd:
    asset_quality_rows.append((kind, label, bs_stock(usd) if kind != "SECTION" else {}))

asset_quality_rows.append(("SECTION", "Asset quality ratios (computed from the £-converted figures above)", {}))
asset_quality_rows.append(("DATA", "ECL coverage ratio (total loss allowance / total gross carrying amount)",
    {"FY2024": "1.6%", "FY2023": "1.7%", "FY2022": "3.8%", "FY2021": "6.6%", "FY2020": "6.2%", "FY2019": "0.1%"}))
asset_quality_rows.append(("DATA", "Stage 3 / NPL ratio (Stage 3 gross / total gross carrying amount)",
    {"FY2024": "5.2%", "FY2023": "5.7%", "FY2022": "9.7%", "FY2021": "16.4%", "FY2020": "11.9%", "FY2019": "1.8%"}))
asset_quality_rows.append(("DATA", "Stage 3 coverage ratio (Stage 3 loss allowance / Stage 3 gross)",
    {"FY2024": "0.3%", "FY2023": "28.7%", "FY2022": "38.0%", "FY2021": "40.1%", "FY2020": "43.3%", "FY2019": "0.0%"}))

bw.add_asset_quality_sheet(
    title="The Access Bank UK Limited — Asset Quality / Credit Risk Disclosures",
    subtitle="£'000, converted from USD, Group basis - see source note for FX methodology and product/stage basis caveats.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=78,
    source_height=300,
    unit_suffix=" (£'000, conv. from USD)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=48, source_height=130)


CET1_TIER1_TOTAL_USD = {"FY2024": 750776, "FY2023": 676944, "FY2022": 486842, "FY2021": 377827, "FY2020": 338920}
RWA_USD = {"FY2023": 3024867, "FY2022": 2459345, "FY2021": 1726764, "FY2020": 1841957}
LEVERAGE_EXPOSURE_USD = {"FY2023": 4246733, "FY2022": 4061990, "FY2021": 3379955, "FY2020": 2595307}
HQLA_USD = {"FY2023": 902038, "FY2022": 1053232, "FY2021": 807121}
NET_CASH_OUTFLOWS_USD = {"FY2023": 246754, "FY2022": 233797, "FY2021": 217760}
NSFR_ASF_USD = {"FY2023": 1878935, "FY2022": 1467825, "FY2021": 1783197}
NSFR_RSF_USD = {"FY2023": 1114383, "FY2022": 992570, "FY2021": 906296}

CET1_RATIO = {"FY2024": "20.18%", "FY2023": "22.4%", "FY2022": "19.8%", "FY2021": "21.88%", "FY2020": "18.40%"}
LEVERAGE_RATIO = {"FY2023": "15.9%", "FY2022": "12.0%", "FY2021": "11.18%", "FY2020": "13.07%"}
LCR_RATIO = {"FY2023": "365.6%", "FY2022": "450.5%", "FY2021": "370.6%"}
# Point-in-time year-end LCR - a DIFFERENT basis from the KM1 12-month-average row
# above, kept as its own row rather than blended into it. See the LCR sheet note.
LCR_POINT_IN_TIME = {"FY2024": "176.65%", "FY2023": "275.47%"}
NSFR_RATIO = {"FY2023": "168.6%", "FY2022": "147.9%", "FY2021": "196.8%"}

# ---------------------------------------------------------------
# Sheet: KM1 Key Metrics (KM1-003)
# ---------------------------------------------------------------
# CURRENCY: this sheet stays in US DOLLARS ($'000), exactly as the Bank
# publishes it, while every other Pillar 3 sheet in this workbook is converted
# to £'000 at the Bank of England spot rate. That is map rule KM1-004(d) - a
# KM1 is a reproduction of a published template, so it keeps the published
# currency. verify_workbook.py's _currency() detects the mismatch and skips
# cross-currency amount comparisons while still checking the ratio rows.
#
# ENTITY: one basis only, stated by the Bank in every edition - "These
# disclosures relate only to The Access Bank UK Limited, which has no trading
# subsidiaries, and therefore does not report on a consolidated basis." No
# Nigerian-parent figure appears anywhere on this sheet.
#
# FY2021 WAS RECOVERED FROM AN IMAGE. research/km1_inventory.jsonl records the
# FY2021 edition as NO_KM1_FOUND. That is WRONG and the row should be
# corrected: page 7 prints the heading "KM1 - Key metrics template" and, below
# the table, "It should be noted that the above ratios..." - but the table
# itself is an 861x637 embedded IMAGE with no text layer, so both pdftotext
# modes return the heading and the note with nothing between them. The same
# edition's CC1 and LR2 tables extract as text, which is why this went unseen.
# The page was rendered at 300dpi and read directly, and the figures below were
# transcribed from two independent renderings (the full page and the embedded
# bitmap at native resolution) that agree digit for digit. "Our text extractor
# cannot see it" is not "the bank did not publish it" (map rule 9).
#
# WHY EACH YEAR COMES FROM ITS OWN EDITION - THIS BANK IS THE PROOF (rule 1).
# The FY2022 edition's 2021 comparative column disagrees with the FY2021
# edition's own Dec-21 column on SIX rows, while capital, RWAs, ratios and
# leverage agree exactly:
#     UK 7a   7.69% (own)  vs  6.1%   (comparative)
#     UK 7d  15.69%        vs 14.1%
#     UK 11a 18.21%        vs 16.6%
#     12      6.19%        vs  7.8%
#     17    343.85%        vs 370.6%
#     20    213.70%        vs 196.8%
# Each edition is internally consistent under the Bank's own printed definition
# ("Row 12 represents the difference between the Total Capital Ratio and the
# Total SREP own funds requirements"): 21.88 - 15.69 = 6.19 in the FY2021
# edition, 21.9 - 14.1 = 7.8 in the FY2022 one. So the SREP requirement for
# FY2021 was genuinely restated between editions. Worse, the FY2022 edition's
# 2021 SREP figures coincide with the FY2021 edition's Dec-20 column
# (6.11/14.11/16.63), which is exactly the kind of near-match that makes a
# wrong column look correct. Every column below is its own edition's own year.
#
# ROW SETS DRIFT HARD ACROSS THESE FOUR EDITIONS (rule 4). Rows 15, UK 16a,
# UK 16b, 16, 18 and 19 are printed only in the FY2022 and FY2023 editions;
# the FY2021 and FY2020 editions print LCR and NSFR as a single ratio row each.
# The FY2020 edition prints no UK 7a/UK 7d/UK 11a/row 12 at all. Those cells
# are blank because the Bank did not print them, not because they were not
# found.
km1_rows = [
    ("SECTION", "Available own funds (amounts)", {}),
    ("DATA", "1  Common Equity Tier 1 (CET1) capital ($'000)",
     {"FY2023": 676944, "FY2022": 486842, "FY2021": 377827, "FY2020": 338920}),
    ("DATA", "2  Tier 1 capital ($'000)",
     {"FY2023": 676944, "FY2022": 486842, "FY2021": 377827, "FY2020": 338920}),
    ("DATA", "3  Total capital ($'000)",
     {"FY2023": 676944, "FY2022": 486842, "FY2021": 377827, "FY2020": 338920}),
    ("SECTION", "Risk-weighted exposure amounts", {}),
    ("DATA", "4  Total risk-weighted exposure amount ($'000)",
     {"FY2023": 3024867, "FY2022": 2459345, "FY2021": 1726764, "FY2020": 1841957}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "5  Common Equity Tier 1 ratio (%)",
     {"FY2023": "22.4%", "FY2022": "19.8%", "FY2021": "21.88%", "FY2020": "18.40%"}),
    ("DATA", "6  Tier 1 ratio (%)",
     {"FY2023": "22.4%", "FY2022": "19.8%", "FY2021": "21.88%", "FY2020": "18.40%"}),
    ("DATA", "7  Total capital ratio (%)",
     {"FY2023": "22.4%", "FY2022": "19.8%", "FY2021": "21.88%", "FY2020": "18.40%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "UK 7a  Additional CET1 SREP requirements (%)",
     {"FY2023": "5.2%", "FY2022": "5.2%", "FY2021": "7.69%"}),
    ("DATA", "UK 7d  Total SREP own funds requirements (%)",
     {"FY2023": "13.2%", "FY2022": "13.2%", "FY2021": "15.69%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "8  Capital conservation buffer (%)",
     {"FY2023": "2.5%", "FY2022": "2.5%", "FY2021": "2.50%", "FY2020": "2.50%"}),
    ("DATA", "9  Institution specific countercyclical capital buffer (%)",
     {"FY2023": "0.1%", "FY2022": "0.0%", "FY2021": "0.02%", "FY2020": "0.02%"}),
    ("DATA", "11  Combined buffer requirement (%)",
     {"FY2023": "2.6%", "FY2022": "2.5%", "FY2021": "2.52%", "FY2020": "2.52%"}),
    ("DATA", "UK 11a  Overall capital requirements (%)",
     {"FY2023": "15.8%", "FY2022": "15.7%", "FY2021": "18.21%"}),
    ("DATA", "12  CET1 available after meeting the total SREP own funds requirements (%)",
     {"FY2023": "9.2%", "FY2022": "6.6%", "FY2021": "6.19%"}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "13  Total exposure measure excluding claims on central banks ($'000)",
     {"FY2023": 4246733}),
    ("DATA", "14  Leverage ratio excluding claims on central banks (%)",
     {"FY2023": "15.9%"}),
    ("DATA", "13  Total Basel III Leverage Ratio exposure method ($'000)",
     {"FY2022": 4061990, "FY2021": 3379955, "FY2020": 2595307}),
    ("DATA", "14  Basel III Leverage ratio (%)",
     {"FY2022": "12.0%", "FY2021": "11.18%", "FY2020": "13.07%"}),
    ("SECTION", "Liquidity Coverage Ratio", {}),
    ("DATA", "15  Total high-quality liquid assets (HQLA) (Weighted value - average) ($'000)",
     {"FY2023": 902038, "FY2022": 1053232}),
    ("DATA", "UK 16a  Cash outflows - Total weighted value ($'000)",
     {"FY2023": 987015, "FY2022": 935189}),
    ("DATA", "UK 16b  Cash inflows - Total weighted value ($'000)",
     {"FY2023": 896548, "FY2022": 732155}),
    ("DATA", "16  Total net cash outflows (adjusted value) ($'000)",
     {"FY2023": 246754, "FY2022": 233797}),
    ("DATA", "17  Liquidity coverage ratio (%) (average of preceding twelve months)",
     {"FY2023": "365.6%", "FY2022": "450.5%", "FY2021": "343.85%", "FY2020": "346.76%"}),
    ("SECTION", "Net Stable Funding Ratio", {}),
    ("DATA", "18  Total available stable funding ($'000)",
     {"FY2023": 1878935, "FY2022": 1467825}),
    ("DATA", "19  Total required stable funding ($'000)",
     {"FY2023": 1114383, "FY2022": 992570}),
    ("DATA", "20  NSFR ratio (%) (average of preceding four quarters)",
     {"FY2023": "168.6%", "FY2022": "147.9%", "FY2021": "213.70%", "FY2020": "173.76%"}),
]

KM1_SOURCES = (
    "Sources - The Access Bank UK Limited's own KM1 key-metrics template in EACH YEAR'S OWN Pillar 3 edition. "
    "Figures are in US DOLLARS ($'000) exactly as published and are NOT converted to sterling, unlike every "
    "other Pillar 3 sheet in this workbook - a KM1 reproduces a published template, so it keeps the published "
    "currency. All ratios are as printed, including the Bank's own precision (two decimals in the FY2020/FY2021 "
    "editions, one decimal from FY2022).\n"
    "ENTITY: a single basis in every year. Each edition states: \"These disclosures relate only to The Access "
    "Bank UK Limited, which has no trading subsidiaries, and therefore does not report on a consolidated "
    "basis.\" No figure of the Nigerian parent (Access Bank Plc) or of Access Holdings Plc appears here.\n"
    f"FY2023: Pillar 3 Disclosures 2023, p.6, Section 1.7 'UK KM1 - Key metrics template', column a "
    f"(31-Dec-23) - {P3_2023_URL}\n"
    f"FY2022: Pillar 3 Disclosures 2022, pp.6-7, Section 1.7 'KM1 - Key metrics template', 2022 column "
    f"- {P3_2022_URL}\n"
    f"FY2021: Pillar 3 Disclosures 2021, p.7, Section 1.7 'KM1 - Key metrics template', Dec-21 column "
    f"- {P3_2021_URL}\n"
    f"FY2020: Pillar 3 Disclosures 2020, p.7, Section 1.7 'Key Metrics', Dec-20 column - {P3_2020_URL}\n"
    "\n"
    "FY2021 WAS READ FROM AN IMAGE, NOT FROM TEXT. The FY2021 edition embeds its KM1 as a picture (an 861x637 "
    "bitmap) rather than as text, so every text extraction of that page returns the heading 'KM1 - Key metrics "
    "template' and the trailing note about 'the above ratios' with nothing in between. The page was rendered at "
    "300dpi and read directly, and each figure was transcribed twice from two independent renderings - the full "
    "page and the embedded bitmap at its native resolution - which agree digit for digit. The same edition's "
    "CC1 and LR2 tables are ordinary text, which is why this table's absence from our extracts looked like an "
    "absence of disclosure. research/km1_inventory.jsonl currently records this document as NO_KM1_FOUND and is "
    "wrong on that point.\n"
    "\n"
    "WHY NO COLUMN IS TAKEN FROM A LATER EDITION'S COMPARATIVE - THIS BANK IS THE DEMONSTRATION.\n"
    "The FY2022 edition's 2021 comparative disagrees with the FY2021 edition's own Dec-21 column on six rows, "
    "while capital, RWAs, capital ratios and leverage agree exactly: UK 7a 7.69% against 6.1%, UK 7d 15.69% "
    "against 14.1%, UK 11a 18.21% against 16.6%, row 12 6.19% against 7.8%, row 17 343.85% against 370.6%, and "
    "row 20 213.70% against 196.8%. Both editions are internally consistent under the Bank's own printed "
    "definition that row 12 is the difference between the total capital ratio and the total SREP own funds "
    "requirement (21.88 - 15.69 = 6.19; 21.9 - 14.1 = 7.8), so the FY2021 SREP requirement was genuinely "
    "restated between editions rather than mistyped. Note also that the FY2022 edition's 2021 SREP figures "
    "coincide with the FY2021 edition's Dec-20 column (6.11 / 14.11 / 16.63) - a near-match of the kind that "
    "makes a wrongly-read column look entirely plausible. The figures above are each edition's own year.\n"
    "\n"
    "THE LEVERAGE ROWS CARRY TWO DIFFERENT CAPTIONS AND ARE NOT MERGED (the 1 January 2022 basis break).\n"
    "The FY2020, FY2021 and FY2022 editions caption rows 13 and 14 'Total Basel III Leverage Ratio exposure "
    "method' and 'Basel III Leverage ratio (%)'. The FY2023 edition captions the same row numbers 'Total "
    "exposure measure excluding claims on central banks' and 'Leverage ratio excluding claims on central "
    "banks'. Both captions are kept as separate rows above rather than run together as one series. The FY2022 "
    "figure is identical under either caption (4,061,990), which is precisely why merging them would look safe.\n"
    "\n"
    "ROW SETS DIFFER BY EDITION - THESE BLANKS ARE NOT-PRINTED, NOT NOT-FOUND.\n"
    "Rows 15, UK 16a, UK 16b, 16, 18 and 19 appear only in the FY2022 and FY2023 editions; the FY2021 and "
    "FY2020 editions disclose liquidity as a single LCR ratio row and a single NSFR ratio row. The FY2020 "
    "edition additionally prints no UK 7a, UK 7d, UK 11a or row 12. Neither edition prints UK 7b or UK 7c in "
    "any year - this Bank discloses only the CET1 and total SREP requirements.\n"
    "\n"
    "SOURCE DEFECTS, REPRODUCED AND FLAGGED (rule 7).\n"
    "1. The FY2020 edition captions its risk-weighted assets section '($m)' while the figures printed under it "
    "are plainly $'000 (1,841,957 is $1.84bn, not $1.84 trillion); its leverage row is captioned '($m)' the "
    "same way. The figures are carried as $'000, the unit the magnitudes and every adjacent edition confirm, "
    "and the caption defect is recorded rather than silently corrected.\n"
    "2. The FY2020 edition's row labels are its own and differ from the template's: 'Common Equity Tier "
    "(CET 1)', 'TIer 1 Ratio (%)' (with that capitalisation), and row 11 as 'Total of bank CET1 specific buffer "
    "requirement'. Its section headings likewise read 'Available capital' and 'Additional CET 1 buffer "
    "requirement as a percentage of RWA'. The template's canonical labels are used for the sheet's rows because "
    "the row NUMBERS and measures are the Bank's own; the label variants are recorded here.\n"
    "3. The FY2023 edition prints the five-column template's column letters as 'a' and 'e' over 31-Dec-23 and "
    "31-Dec-22 - two populated columns of a five-column template, not a two-column table.\n"
    "\n"
    "FY2024 AND FY2019 ARE BLANK, FOR DIFFERENT REASONS.\n"
    "FY2024: no FY2024 Pillar 3 edition exists. That finding is this script's own, recorded 2026-09-15 on "
    "positive evidence - nine filename permutations across six CDN upload folders, plus a Wayback CDX sweep of "
    "the whole domain filtered on 'pillar' returning exactly five documents, the newest being the 2023 edition "
    "- and it is retained here rather than re-derived. See p3_sources() for the detail and for what the Annual "
    "Report does and does not substitute.\n"
    "FY2019: the Bank's FY2019 Pillar 3 edition has not been located. The FY2020 edition prints a Dec-19 "
    "comparative column, and it is deliberately NOT used here for the reason demonstrated above. FY2019 "
    "therefore carries no column on this sheet, while the single-metric sheets continue to show that "
    "comparative under their own citation.\n"
    "\n"
    "EXPECTED VERIFIER OUTPUT - TWO DISAGREEMENTS THAT ARE CORRECT AND MUST NOT BE 'FIXED'.\n"
    "scripts/verify_workbook.py reports KM1 row 17 FY2021 (343.85%) and row 20 FY2021 (213.70%) as disagreeing "
    "with the LCR and NSFR sheets (370.6% and 196.8%). Both sides are deliberate and both are right for what "
    "they are: this sheet takes FY2021 from the FY2021 edition's own Dec-21 column, while those metric sheets "
    "cite the FY2022 edition's 2021 comparative, as their own source notes say. The gap IS the restatement "
    "documented above - the checker found it independently, from the other direction. Everything else "
    "reconciles, and the amount rows are skipped by design because this sheet is in USD and the metric sheets "
    "are in converted sterling.\n"
    "\n"
    "LATEST-EDITION CHECK, 2026-09-16 - BLOCKED, WHICH IS NOT THE SAME AS 'NONE NEWER' (map rule 9).\n"
    "The Bank's own website could not be read at all today. The homepage, the investor-relations page, "
    "sitemaps.xml (the filename robots.txt itself names) and every wp-json endpoint each returned HTTP 403 "
    "carrying a Cloudflare 'Just a moment...' JavaScript interstitial, including with a full desktop browser "
    "User-Agent - the technique that did defeat the Lloyds Banking Group block for Bank of Scotland does NOT "
    "work on this host. Static files are served normally (robots.txt 200 text/plain, and every cited PDF 200 "
    "application/pdf), so the block is on the HTML surface only. web.archive.org returned 'Temporarily "
    "Offline' throughout, so the archive route was unavailable rather than empty. 96 plausible 2024/2025 "
    "filenames under /wp-content/uploads/ returned nothing, which proves little given this Bank's filename "
    "variance (PILLAR-3-DISCLOSURES-2020-Clean, -2021-Final, -2022-Final, then PIllar-3-2023.pdf with a "
    "capital-I typo). CONCLUSION: the index could not be read, so no claim is made here about whether a newer "
    "edition exists. The 2026-09-15 evidence above remains the best available and should be re-run once the "
    "site or the archive is reachable."
)

bw.add_km1_sheet(
    title="The Access Bank UK Limited - KM1 Key Metrics",
    subtitle="The Bank's own published KM1 key-metrics template, in its own row order, row numbers, labels and "
             "precision. Amounts in US DOLLARS ($'000) as published - this sheet is NOT converted to sterling, "
             "unlike the other Pillar 3 sheets in this workbook. Each column is taken from that year's own "
             "edition; FY2021 was recovered from an image. See the sources note for the six rows on which a "
             "later edition's comparative disagrees with the year's own edition.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=66,
    source_height=340,
    years=YEARS,
)

metric("CET1 Capital", "£'000 (conv. from USD)", [("Common Equity Tier 1 (CET1) capital", p3_stock(CET1_TIER1_TOTAL_USD))], p3_sources())
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 (CET1) ratio", CET1_RATIO)], p3_sources())
metric("Tier 1 Capital", "£'000 (conv. from USD)", [("Tier 1 capital", p3_stock(CET1_TIER1_TOTAL_USD))], p3_sources(),
       note="Equal to CET1 capital in every year - the Bank holds no Additional Tier 1 (AT1) instruments.")
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", CET1_RATIO)], p3_sources())
metric("Total Capital", "£'000 (conv. from USD)", [("Total capital", p3_stock(CET1_TIER1_TOTAL_USD))], p3_sources(),
       note="Equal to CET1/Tier 1 capital in every year - the Bank holds no AT1 or Tier 2 instruments.")
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", CET1_RATIO)], p3_sources())
metric("Total RWAs", "£'000 (conv. from USD)", [("Total risk-weighted exposure amount", p3_stock(RWA_USD))], p3_sources())

# ---------------------------------------------------------------
# Sheet: RWA Breakdown (UK OV1 - Overview of risk weighted exposure amounts)
# ---------------------------------------------------------------
RWA_BREAKDOWN_SOURCES = (
    "Sources - The Access Bank UK Limited's own OV1 (Overview of risk weighted exposure amounts) table, "
    "converted from USD to £ at that year's BoE spot rate:\n"
    f"FY2023 & FY2022: Pillar 3 Disclosures 2023, p.6 (Section 4.3, OV1) - {P3_2023_URL}\n"
    f"FY2021 & FY2020: Pillar 3 Disclosures 2022, p.15 (Section 4.3, OV1) - {P3_2022_URL}\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE + "\n\n"
    "No FY2024 Pillar 3 Disclosures document has been found (same gap already noted on the Pillar 3 metric "
    "sheets) - FY2024 cells are blank rather than guessed. The Bank has no market risk RWA requirement in any "
    "year shown (its own Pillar 3 reports state market risk is below the CRR de minimis threshold - it holds no "
    "trading book) - not a missing-disclosure gap, a genuine nil. 'Of which: credit valuation adjustment (CVA)' "
    "is a memo sub-item already included WITHIN 'Counterparty credit risk (CCR)' above it (per the OV1 template's "
    "own structure), not an additional component - it will appear to double-count against the Total row in a "
    "naive DATA-sum reconciliation check; this is expected and matches the Bank's own table structure."
)

rwa_breakdown_rows_usd = [
    ("SECTION", "Risk-weighted exposure amounts (RWEAs)", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2023": 2731456, "FY2022": 2238225, "FY2021": 1540125, "FY2020": 1671502}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2023": 9799, "FY2022": 6598, "FY2021": 838, "FY2020": 9552}),
    ("DATA", "Of which: credit valuation adjustment (CVA)", {"FY2023": 2199, "FY2022": 828, "FY2021": 200, "FY2020": 3507}),
    ("DATA", "Operational risk (basic indicator approach)", {"FY2023": 281414, "FY2022": 214522, "FY2021": 185601, "FY2020": 157396}),
    ("TOTAL", "Total risk-weighted exposure amount", {"FY2023": 3024867, "FY2022": 2459345, "FY2021": 1726764, "FY2020": 1841957}),
]
rwa_breakdown_rows = []
for kind, label, usd in rwa_breakdown_rows_usd:
    rwa_breakdown_rows.append((kind, label, p3_stock(usd) if kind != "SECTION" else {}))

bw.add_rwa_breakdown_sheet(
    title="The Access Bank UK Limited — RWA Breakdown (UK OV1)",
    subtitle="£'000, converted from USD - see source note for FX methodology.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=54,
    source_height=170,
    unit_suffix=" (£'000, conv. from USD)",
)

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
        ("Liquidity Coverage Ratio (%) (KM1, average of preceding 12 months)", LCR_RATIO),
        ("Liquidity Coverage Ratio (%) (point-in-time at 31 December)", LCR_POINT_IN_TIME),
    ],
    p3_sources(),
    note="TWO DIFFERENT BASES, deliberately kept on separate rows. The KM1 row is the Bank's 'average of "
         "preceding twelve months' figure and is the basis used for FY2021-FY2023. The point-in-time row is the "
         "Bank's year-end spot LCR. They are NOT comparable: for FY2023 the Bank discloses BOTH - 365.6% on the "
         "KM1 average basis (Pillar 3 Disclosures 2023, p.6 row 17) and 275.5% at 31 December 2023 (same "
         "document, Section 8 narrative), a 90-point gap. FY2024 has no Pillar 3 report, so only the "
         "point-in-time figure (176.65%, per the Annual Report 2024 KPI table) exists; it is shown on the "
         "point-in-time row and the KM1 average row is left BLANK for FY2024 rather than continued with a "
         "different-basis number. An earlier revision of this workbook placed 176.65% directly in the KM1 "
         "average row, which made the ratio appear to fall 365.6% -> 176.65%; the like-for-like point-in-time "
         "move is 275.47% -> 176.65%. FY2021's $ breakdown (HQLA/net cash outflows) is sourced from the FY2022 "
         "Pillar 3 report's comparative column - the FY2021 Pillar 3 report itself only states a single "
         "narrative LCR percentage (343.9%), not a KM1-style table with a $ breakdown; that narrative figure is "
         "again a different convention from the 370.6% KM1 figure shown here. FY2020 not found in any source.",
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

overview_bs_totals_usd = {
    "Total assets": {"FY2024": 6125404646, "FY2023": 4423312189, "FY2022": 3768309444, "FY2021": 3084753539, "FY2020": 2397552440},
    "Loans and advances to customers": {"FY2024": 1669793574, "FY2023": 1523143929, "FY2022": 1114878580, "FY2021": 1054399028, "FY2020": 890496159},
    "Customer deposits": {"FY2024": 1549953453, "FY2023": 1451645528, "FY2022": 1252213546, "FY2021": 935798374, "FY2020": 876497010},
    "Total equity": {"FY2024": 784904570, "FY2023": 682304125, "FY2022": 491084065, "FY2021": 380802724, "FY2020": 340221462},
}
overview_is_totals_usd = {
    "Total operating income / Net operating income": {"FY2024": 233511913, "FY2023": 199377371, "FY2022": 94211777, "FY2021": 86776254, "FY2020": 42196020},
    "Total operating expense": {"FY2024": -60123349, "FY2023": -47847374, "FY2022": -35511769, "FY2021": -34916413, "FY2020": -25367377},
    "Profit for the year": {"FY2024": 127726847, "FY2023": 112227055, "FY2022": 45330291, "FY2021": 40495527, "FY2020": 13505033},
}
overview_eq_flow_usd = {
    "Total comprehensive income for the year": {"FY2024": 126406774, "FY2023": 113665471, "FY2022": 45281341, "FY2021": 40581262, "FY2020": 13263073},
    "Other equity movements, net (share issuance/dividends)": {"FY2024": -23806329, "FY2023": 77554589, "FY2022": 65000000, "FY2021": 0, "FY2020": 0},
}
overview_eq_opening_usd = {"FY2024": 682304125, "FY2023": 491084065, "FY2022": 380802724, "FY2021": 340221462}  # FY2020 opening not converted, see equity sheet's FX caveat
_eq_opening_rate = {"FY2024": FX_SPOT["FY2023"], "FY2023": FX_SPOT["FY2022"], "FY2022": FX_SPOT["FY2021"], "FY2021": FX_SPOT["FY2020"]}
overview_eq_opening_gbp = {y: round(v / _eq_opening_rate[y] / 1000, 1) for y, v in overview_eq_opening_usd.items()}
overview_eq_closing_usd = {"FY2024": 784904570, "FY2023": 682304125, "FY2022": 491084065, "FY2021": 380802724, "FY2020": 340221462}

bw.add_overview_sheet(
    cash_flow_totals=[(label, cf_flow(vals)) for label, vals in cf_totals_usd.items()]
                      + [("Cash and cash equivalents at end of year", cf_stock(cf_close_usd))],
    cash_flow_unit="£'000",
    balance_sheet_totals=[(label, bs_stock(vals)) for label, vals in overview_bs_totals_usd.items()],
    balance_sheet_unit="£'000",
    income_statement_totals=[(label, bs_flow(vals)) for label, vals in overview_is_totals_usd.items()],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", overview_eq_opening_gbp),
        ("Total comprehensive income for the year", bs_flow(overview_eq_flow_usd["Total comprehensive income for the year"])),
        ("Other equity movements, net", bs_flow(overview_eq_flow_usd["Other equity movements, net (share issuance/dividends)"])),
        ("Closing equity", bs_stock(overview_eq_closing_usd)),
    ],
    equity_changes_unit="£'000",
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
         "cells are blank for FY2024 (no edition found) and FY2020 LCR/NSFR (not found in any source). "
         "'Total operating income / Net operating income' uses each year's Net operating income (after ECL), the "
         "one operating-income-level figure disclosed consistently across all 5 years (see Asset Quality sheet's "
         "presentation note on the P&L structure change). Opening equity for FY2020 is not shown (no 31 December "
         "2019 GBP/USD rate sourced) - see the Statement of Changes in Equity sheet's FX caveat.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/ACCESS BANK UK FINANCIALS.xlsx")
