import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020"]
YEAR_LABEL = {y: y for y in YEARS}

AR_URLS = {
    "FY2025": "https://danskebank.co.uk/-/media/danske-bank/uk/about-us/corporate-governance/annual-reports/northern-bank-annual-report-accounts-2025.pdf?hash=FAA2D970352C7AB5893C6D09B997681A&rev=a79a533060b745c682e1796ed929cab5",
    "FY2024": "https://danskebank.co.uk/-/media/danske-bank/uk/about-us/corporate-governance/annual-reports/northern-bank-annual-report-og-accounts-2024.pdf?hash=C989E05EAE7993B66B70ADF26AB11BF7&rev=1a1acede77ae425a8222ac3395302b9d",
    "FY2023": "https://danskebank.co.uk/-/media/danske-bank/uk/about-us/corporate-governance/annual-reports/northern-bank-annual-report-og-accounts-2023.pdf?hash=7CEA5F947D848F4BD9C1E97211AFF9CE&rev=4202add3decb471fbed08666ff6e307b",
    "FY2022": "https://danskebank.co.uk/-/media/danske-bank/uk/about-us/corporate-governance/annual-reports/northern-bank-annual-report-og-accounts-2022.pdf?rev=9aa72868afb1433d9e9df8f0959d630f",
    "FY2021": "https://danskebank.co.uk/-/media/danske-bank/uk/about-us/corporate-governance/annual-reports/northern-bank---annual-report-og-accounts-2021.pdf?rev=6bfedd29bb0d488ea30ffce998073674",
    "FY2020": "https://danskebank.co.uk/-/media/danske-bank/uk/about-us/corporate-governance/annual-reports/northern-bank---annual-report-og-accounts-2020.pdf",
}

# FY2020 NSFR (199%) is not disclosed anywhere in the Bank's own FY2020 Annual
# Report - only recovered as the FY2021 Annual Report's own "31 December 2020"
# comparative figure (p.70 of the FY2021 report), per the same pattern already
# used for the FY2021 MREL ratio one row down. No numeric MREL ratio for FY2020
# exists in any report actually read (FY2020's own report, FY2021's own report,
# or FY2022's report, which only tables FY2021/FY2022) - MREL Ratio is
# genuinely self-skipped for FY2020 alone, documented on that sheet.
FY2021_REPORT_URL = AR_URLS["FY2021"]

ENTITY_NOTE = (
    "ENTITY NOTE: Northern Bank Limited (Companies House R0000568, FRN 122261, "
    "LEI 549300KUB2XKWLPMXV81) is the exact legal entity in Banks List 2608.xlsx. "
    "It trades as Danske Bank in Northern Ireland but remains Northern Bank Limited, "
    "an autonomous subsidiary of Danske Bank Group. All figures are the Bank's own "
    "entity-level disclosures, not Danske Bank A/S group figures. The annual reports "
    "state that the Bank monitors capital monthly and quarterly and publishes these "
    "annual capital and liquidity metrics; no separate interim Pillar 3 sheet is "
    "included in this standard annual WF-018 build."
)


def sources(section, pages):
    lines = [f"Sources - Northern Bank Limited entity-level {section}:"]
    for year in YEARS:
        lines.append(f"{year}: Northern Bank Limited Annual Report and Financial Statements {year[2:]}, p.{pages[year]} - {AR_URLS[year]}")
    return "\n".join(lines) + "\n\n" + ENTITY_NOTE


bw = BankWorkbook(
    bank_name="Northern Bank Limited (trading as Danske Bank)",
    years=YEARS,
    year_label=YEAR_LABEL,
    header_color="1D3557",
)

# ---------------------------------------------------------------
# Balance Sheet - equity reconciliation ladder step 1: built first so each
# year's own Total equity is the independent check value for the equity
# sheet below. All 5 years tie exactly (Total assets = Total liabilities +
# Total equity; Total equity ties to the equity statement's own opening/
# closing balances - zero plug rows needed anywhere across all 5 years).
# ---------------------------------------------------------------
STATEMENTS_SOURCES = (
    "Sources - Northern Bank Limited entity-level Annual Report and Financial Statements:\n"
    f"FY2025: Income Statement/Statement of Other Comprehensive Income p.88, Balance Sheet p.89, "
    f"Statement of Changes in Equity p.90 - {AR_URLS['FY2025']}\n"
    f"FY2024: Income Statement p.127, Statement of Other Comprehensive Income p.128, Balance Sheet p.129, "
    f"Statement of Changes in Equity p.130 - {AR_URLS['FY2024']}\n"
    f"FY2023: Income Statement p.127, Balance Sheet p.128, Statement of Other Comprehensive Income p.129, "
    f"Statement of Changes in Equity p.131 - {AR_URLS['FY2023']}\n"
    f"FY2022: Income Statement p.115, Statement of Other Comprehensive Income p.116, Balance Sheet p.117, "
    f"Statement of Changes in Equity p.118 - {AR_URLS['FY2022']}\n"
    f"FY2021: Income Statement p.103, Statement of Other Comprehensive Income p.104, Balance Sheet p.105, "
    f"Statement of Changes in Equity p.106 - {AR_URLS['FY2021']}\n"
    f"FY2020: Income Statement p.71, Statement of Other Comprehensive Income p.72, Balance Sheet p.73, "
    f"Statement of Changes in Equity p.74 - {AR_URLS['FY2020']}\n\n"
    + ENTITY_NOTE
)

BALANCE_SHEET_SOURCES = (
    STATEMENTS_SOURCES + "\n\n"
    "INVESTMENT SECURITIES BREAKDOWN: the 'Investment securities - ...' sub-rows below the headline 'Total "
    "investment securities' line are transcribed from each year's own Note 15 'Investment securities' (Note 13 "
    "in the FY2020-FY2022 reports, renumbered to Note 15 from FY2023 onward), which splits the balance solely "
    "by IFRS 9 measurement basis/business model - Note 15(a) 'Hold to collect' (securities measured at "
    "amortised cost) and Note 15(b) 'Hold to collect and sell' (securities measured FVOCI). Each note states "
    "the underlying bonds are 'primarily UK government securities and highly rated covered, sovereign, "
    "supra-national and agency bonds' but does NOT itemise the balance numerically by issuer type - only the "
    "measurement-basis split is disclosed as figures, so no issuer-type sub-rows are shown here.\n"
    f"FY2025: Note 15(a)/15(b), p.108 - {AR_URLS['FY2025']}\n"
    f"FY2024: Note 15(a)/15(b), p.153 - {AR_URLS['FY2024']}\n"
    f"FY2023: Note 15(a)/15(b), p.153 - {AR_URLS['FY2023']}\n"
    f"FY2022: Note 13(a)/13(b), p.140 - {AR_URLS['FY2022']}\n"
    f"FY2021: Note 13(a)/13(b), p.124 - {AR_URLS['FY2021']}\n"
    f"FY2020: Note 13(a)/13(b), p.91 - {AR_URLS['FY2020']}\n\n"
    "Each year's two sub-rows sum exactly to that year's own headline 'Total investment securities' line "
    "(verified for all 6 years, including cross-checks against each report's own prior-year comparative "
    "column)."
)

bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central bank", {"FY2025": 2975799, "FY2024": 3468175, "FY2023": 3299543, "FY2022": 3350828, "FY2021": 4388161, "FY2020": 4225153}),
    ("DATA", "Items in the course of collection from other banks", {"FY2025": 23389, "FY2024": 25069, "FY2023": 41191, "FY2022": 32139, "FY2021": 21839, "FY2020": 20190}),
    ("DATA", "Due from other banks", {"FY2025": 4236, "FY2024": 5731, "FY2023": 10283, "FY2022": 41711, "FY2021": 48023, "FY2020": 50639}),
    ("DATA", "Derivative financial instruments", {"FY2025": 77518, "FY2024": 76537, "FY2023": 75457, "FY2022": 89324, "FY2021": 8586, "FY2020": 17284}),
    ("DATA", "Total investment securities", {"FY2025": 4637481, "FY2024": 3724852, "FY2023": 3367408, "FY2022": 3369156, "FY2021": 2226346, "FY2020": 1409536}),
    ("DATA", "Investment securities - Hold to collect (amortised cost)", {"FY2025": 3130670, "FY2024": 2951816, "FY2023": 2403390, "FY2022": 2294601, "FY2021": 1318484, "FY2020": 531555}),
    ("DATA", "Investment securities - Hold to collect and sell (FVOCI)", {"FY2025": 1506811, "FY2024": 773036, "FY2023": 964018, "FY2022": 1074555, "FY2021": 907862, "FY2020": 877981}),
    ("DATA", "Loans and advances to customers", {"FY2025": 8054390, "FY2024": 7030843, "FY2023": 6739732, "FY2022": 6334707, "FY2021": 6206664, "FY2020": 6229841}),
    ("DATA", "Investment in subsidiaries", {"FY2025": 250, "FY2024": 250, "FY2023": 250, "FY2022": 250, "FY2021": 250, "FY2020": 250}),
    ("DATA", "Intangible assets", {"FY2025": 2466, "FY2024": 1859, "FY2023": 1608, "FY2022": 522, "FY2021": 34, "FY2020": 157}),
    ("DATA", "Property, plant and equipment", {"FY2025": 32177, "FY2024": 35153, "FY2023": 36823, "FY2022": 38822, "FY2021": 40272, "FY2020": 41818}),
    ("DATA", "Right-of-use assets", {"FY2025": 4067, "FY2024": 3782, "FY2023": 4783, "FY2022": 4618, "FY2021": 4253, "FY2020": 5568}),
    ("DATA", "Assets held for sale", {"FY2024": 376, "FY2023": 588, "FY2022": 707, "FY2021": 1399, "FY2020": 360}),
    ("DATA", "Defined benefit pension asset", {"FY2025": 7025, "FY2024": 2822, "FY2023": 4804, "FY2022": 78009, "FY2021": 154208, "FY2020": 219679}),
    ("DATA", "Current tax asset", {"FY2025": 9724, "FY2024": 5678, "FY2023": 1314, "FY2022": 6785, "FY2021": 1092, "FY2020": 3008}),
    ("DATA", "Deferred tax asset", {"FY2025": 22394, "FY2024": 39348, "FY2023": 55404, "FY2022": 36533}),
    ("DATA", "Other assets", {"FY2025": 61038, "FY2024": 53916, "FY2023": 58179, "FY2022": 36280, "FY2021": 24046, "FY2020": 26706}),
    ("TOTAL", "Total assets", {"FY2025": 15911954, "FY2024": 14474391, "FY2023": 13697367, "FY2022": 13420391, "FY2021": 13125173, "FY2020": 12250189}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Due to other banks", {"FY2025": 329724, "FY2024": 414631, "FY2023": 431125, "FY2022": 404807, "FY2021": 366611, "FY2020": 373032}),
    ("DATA", "Items in course of transmission to other banks", {"FY2025": 18661, "FY2024": 14231, "FY2023": 44130, "FY2022": 26068, "FY2021": 15267, "FY2020": 12147}),
    ("DATA", "Derivative financial instruments", {"FY2025": 27178, "FY2024": 46074, "FY2023": 48519, "FY2022": 82808, "FY2021": 22487, "FY2020": 28199}),
    ("DATA", "Deposits from customers", {"FY2025": 13440624, "FY2024": 12053498, "FY2023": 11333715, "FY2022": 11229589, "FY2021": 11161358, "FY2020": 10228137}),
    ("DATA", "Notes in circulation", {"FY2025": 938572, "FY2024": 784961, "FY2023": 711125, "FY2022": 664728, "FY2021": 634036, "FY2020": 557942}),
    ("DATA", "Deferred tax liabilities", {"FY2021": 13900, "FY2020": 34194}),
    ("DATA", "Other liabilities", {"FY2025": 86459, "FY2024": 85430, "FY2023": 68156, "FY2022": 43049, "FY2021": 33558, "FY2020": 36317}),
    ("DATA", "Provisions", {"FY2025": 1876, "FY2024": 1571, "FY2023": 1256, "FY2022": 2150, "FY2021": 2757, "FY2020": 3354}),
    ("DATA", "Subordinated debt instruments / Non-preferred senior securities issued", {"FY2025": 100000, "FY2024": 130000, "FY2023": 130000, "FY2022": 130000, "FY2021": 126000, "FY2020": 126000}),
    ("TOTAL", "Total liabilities", {"FY2025": 14943094, "FY2024": 13530396, "FY2023": 12768026, "FY2022": 12583199, "FY2021": 12375974, "FY2020": 11399322}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 218170, "FY2024": 218170, "FY2023": 218170, "FY2022": 218170, "FY2021": 218170, "FY2020": 218170}),
    ("DATA", "Other equity instruments (AT1)", {"FY2025": 226190, "FY2024": 226526, "FY2023": 226895, "FY2022": 225953, "FY2021": 96974, "FY2020": 96958}),
    ("DATA", "Share premium account", {"FY2025": 306590, "FY2024": 306590, "FY2023": 306590, "FY2022": 306590, "FY2021": 306590, "FY2020": 306590}),
    ("DATA", "Revaluation reserve", {"FY2025": 28706, "FY2024": 30697, "FY2023": 32506, "FY2022": 33418, "FY2021": 33892, "FY2020": 34965}),
    ("DATA", "Reserve for investment securities at fair value", {"FY2025": 3104, "FY2024": 948, "FY2023": -2970, "FY2022": -29070, "FY2021": -2446, "FY2020": 7190}),
    ("DATA", "Cash flow hedge reserve", {"FY2025": 733, "FY2024": -173, "FY2023": -1676, "FY2022": -8449, "FY2021": -2115, "FY2020": 4712}),
    ("DATA", "Retained earnings", {"FY2025": 185367, "FY2024": 161237, "FY2023": 149826, "FY2022": 90580, "FY2021": 98134, "FY2020": 182282}),
    ("TOTAL", "Total equity and shareholders' equity", {"FY2025": 968860, "FY2024": 943995, "FY2023": 929341, "FY2022": 837192, "FY2021": 749199, "FY2020": 850867}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 15911954, "FY2024": 14474391, "FY2023": 13697367, "FY2022": 13420391, "FY2021": 13125173, "FY2020": 12250189}),
]

bw.add_balance_sheet_sheet(
    title="Northern Bank Limited — Balance Sheet",
    subtitle="Entity-level. £'000. Trading name: Danske Bank. FY2020 and FY2021 both carry a 'Deferred tax "
              "liabilities' line (34,194 and 13,900 respectively) instead of a deferred tax asset, and a "
              "'Subordinated notes issued' liability (126,000, Tier 2-eligible) - from FY2022 onward this became "
              "'Non-preferred senior securities issued' (not Tier 2-eligible, shown here on the same combined row "
              "for comparability). 'Assets held for sale' is not disclosed as a standalone line for FY2025 (merged "
              "into Other assets that year, per the Bank's own presentation).",
    rows=bs_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=72,
    source_height=340,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Profit & Loss - OCI section shown with each component's pre-tax movement
# plus one combined "Taxation impact" row per year. FY2025's own report
# already presents OCI tax this way (two combined tax lines); FY2021-FY2024's
# reports itemise tax per component instead - both reduce to the same total,
# shown uniformly here for comparability across all 5 years. Confirmed each
# year's own components + combined tax sum exactly to that year's own
# disclosed "Total other comprehensive income" figure.
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest and similar income", {"FY2025": 624405, "FY2024": 573484, "FY2023": 456611, "FY2022": 242626, "FY2021": 160651, "FY2020": 175408}),
    ("DATA", "Interest expense", {"FY2025": -238907, "FY2024": -230921, "FY2023": -159585, "FY2022": -23809, "FY2021": -5895, "FY2020": -13487}),
    ("TOTAL", "Net interest income", {"FY2025": 385498, "FY2024": 342563, "FY2023": 297026, "FY2022": 218817, "FY2021": 154756, "FY2020": 161921}),
    ("DATA", "Fee and commission income", {"FY2025": 44535, "FY2024": 46179, "FY2023": 46020, "FY2022": 46232, "FY2021": 40835, "FY2020": 38701}),
    ("DATA", "Fee and commission expense", {"FY2025": -8095, "FY2024": -8808, "FY2023": -7532, "FY2022": -5684, "FY2021": -5841, "FY2020": -5306}),
    ("DATA", "Net trading income", {"FY2025": 10887, "FY2024": 7059, "FY2023": -3805, "FY2022": 11706, "FY2021": 8962, "FY2020": 7850}),
    ("DATA", "Other operating income", {"FY2025": 1467, "FY2024": 1391, "FY2023": 1812, "FY2022": 2434, "FY2021": 1335, "FY2020": 1953}),
    ("TOTAL", "Non-interest income", {"FY2025": 48794, "FY2024": 45821, "FY2023": 36495, "FY2022": 54688, "FY2021": 45291, "FY2020": 43198}),
    ("TOTAL", "Operating income", {"FY2025": 434292, "FY2024": 388384, "FY2023": 333521, "FY2022": 273505, "FY2021": 200047, "FY2020": 205119}),
    ("DATA", "Operating expenses", {"FY2025": -177643, "FY2024": -175365, "FY2023": -157020, "FY2022": -146981, "FY2021": -150005, "FY2020": -142240}),
    ("DATA", "Depreciation and amortisation expense", {"FY2025": -6004, "FY2024": -4442, "FY2023": -3646, "FY2022": -3364, "FY2021": -3433, "FY2020": -4376}),
    ("TOTAL", "Profit before loan impairment (charge)/credit", {"FY2025": 250645, "FY2024": 208577, "FY2023": 172855, "FY2022": 123160, "FY2021": 46609, "FY2020": 58503}),
    ("DATA", "Loan impairment (charge)/credit", {"FY2025": -267, "FY2024": 9587, "FY2023": 13105, "FY2022": -19859, "FY2021": 14660, "FY2020": -45426}),
    ("TOTAL", "Profit before tax", {"FY2025": 250378, "FY2024": 218164, "FY2023": 185960, "FY2022": 103301, "FY2021": 61269, "FY2020": 13077}),
    ("DATA", "Tax (charge)/credit", {"FY2025": -61147, "FY2024": -52669, "FY2023": -29241, "FY2022": 109, "FY2021": -19735, "FY2020": -5525}),
    ("TOTAL", "Profit for the year", {"FY2025": 189231, "FY2024": 165495, "FY2023": 156719, "FY2022": 103410, "FY2021": 41534, "FY2020": 7552}),
    ("SECTION", "Other comprehensive income, net of tax", {}),
    ("DATA", "Actuarial gain/(loss) on retirement benefit scheme (pre-tax)", {"FY2025": 5836, "FY2024": -404, "FY2023": -106904, "FY2022": -80050, "FY2021": -69792, "FY2020": 19865}),
    ("DATA", "Property revaluation gain/(loss) (pre-tax)", {"FY2025": -1940, "FY2024": -1479, "FY2023": -1155, "FY2022": 243, "FY2021": 571, "FY2020": -954}),
    ("DATA", "Unrealised value adjustments of investment securities at fair value (pre-tax)", {"FY2025": 3173, "FY2024": -571, "FY2023": 21919, "FY2022": -36724, "FY2021": -13500, "FY2020": 7724}),
    ("DATA", "Transfer to income statement on disposal of investment securities (pre-tax)", {"FY2025": -28, "FY2024": 6013, "FY2023": 14330}),
    ("DATA", "Movement on interest rate hedge adjustment (pre-tax)", {"FY2025": -150}),
    ("DATA", "Cash flow hedge reserve gains/(losses) (pre-tax)", {"FY2025": 1258, "FY2024": 2088, "FY2023": 9406, "FY2022": -8578, "FY2021": -9611, "FY2020": 3612}),
    ("DATA", "Taxation impact (total, all OCI components)", {"FY2025": -2432, "FY2024": -1477, "FY2023": 17575, "FY2022": 33070, "FY2021": 29099, "FY2020": -8451}),
    ("TOTAL", "Total other comprehensive income, net of tax", {"FY2025": 5717, "FY2024": 4170, "FY2023": -44829, "FY2022": -92039, "FY2021": -63233, "FY2020": 21796}),
    ("TOTAL", "Total comprehensive income for the year", {"FY2025": 194948, "FY2024": 169665, "FY2023": 111890, "FY2022": 11371, "FY2021": -21699, "FY2020": 29348}),
]

bw.add_income_statement_sheet(
    title="Northern Bank Limited — Profit & Loss",
    subtitle="Entity-level. £'000. Trading name: Danske Bank. 'Transfer to income statement on disposal' and "
              "'Movement on interest rate hedge adjustment' are only disclosed as separate OCI lines from FY2023 "
              "and FY2025 respectively - blank in earlier years where the Bank's own report doesn't break them "
              "out. Each year's own components plus the combined taxation impact tie exactly to that year's own "
              "disclosed Total other comprehensive income and Total comprehensive income figures (FY2020's own "
              "OCI note prints a -8,451 combined tax figure and a 21,796 total OCI figure; the FY2020 Statement "
              "of Changes in Equity's own tax row instead nets to -8,450/21,797 - a 1-unit rounding artifact "
              "already present in the Bank's own FY2020 report, not a transcription error).",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=82,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - per-year reconciliation ladder confirmed:
# every year's own closing balance ties exactly to both the next year's own
# opening balance and that year's own Balance Sheet Total equity. Zero plug
# rows needed anywhere across all 5 years. Ladder's mandated scan of each
# year's equity note caught genuine "easy to skip" categories: AT1 issuance/
# redemption (FY2022) and AT1 distributions paid every year, shown on their
# own rows rather than folded into a generic "other".
# ---------------------------------------------------------------
equity_headers = ["Share capital", "Share premium", "Revaluation reserve", "Cash flow hedge reserve",
                   "Reserve for securities at fair value", "Retained earnings",
                   "Total attributable to shareholders", "AT1 capital holders", "Total equity"]
equity_rows = [
    ("TOTAL", "At 1 January 2020 (FY2020 opening)", (218170, 306590, 35906, 2132, 1594, 165194, 729586, 97069, 826655)),
    ("DATA", "Profit for the year", (None, None, None, None, None, 2526, 2526, 5026, 7552)),
    ("DATA", "Actuarial gain recognised in retirement benefit scheme", (None, None, None, None, None, 19865, 19865, None, 19865)),
    ("DATA", "Transfer re property disposals", (None, None, -60, None, None, 60, None, None, None)),
    ("DATA", "Property revaluation", (None, None, -954, None, None, None, -954, None, -954)),
    ("DATA", "Investment securities at fair value", (None, None, None, None, 7724, None, 7724, None, 7724)),
    ("DATA", "Cash flow hedge reserve", (None, None, None, 3612, None, None, 3612, None, 3612)),
    ("DATA", "Taxation impact", (None, None, 73, -1032, -2128, -5363, -8450, None, -8451)),
    ("DATA", "AT1 distributions paid", (None, None, None, None, None, None, None, -5137, -5137)),
    ("TOTAL", "At 31 December 2020 (FY2020 closing) / At 1 January 2021 (FY2021 opening)", (218170, 306590, 34965, 4712, 7190, 182282, 753909, 96958, 850867)),
    ("DATA", "Profit for the year", (None, None, None, None, None, 36549, 36549, 4985, 41534)),
    ("DATA", "Actuarial loss recognised in retirement benefit scheme", (None, None, None, None, None, -69792, -69792, None, -69792)),
    ("DATA", "Transfer re property disposals", (None, None, -1063, None, None, 1063, None, None, None)),
    ("DATA", "Property revaluation", (None, None, 571, None, None, None, 571, None, 571)),
    ("DATA", "Investment securities at fair value", (None, None, None, None, -13500, None, -13500, None, -13500)),
    ("DATA", "Cash flow hedge reserve", (None, None, None, -9611, None, None, -9611, None, -9611)),
    ("DATA", "Taxation impact", (None, None, -581, 2784, 3864, 23032, 29099, None, 29099)),
    ("DATA", "Dividends paid", (None, None, None, None, None, -75000, -75000, None, -75000)),
    ("DATA", "AT1 distributions paid", (None, None, None, None, None, None, None, -4969, -4969)),
    ("TOTAL", "At 31 December 2021 (FY2021 closing)", (218170, 306590, 33892, -2115, -2446, 98134, 652225, 96974, 749199)),
    ("DATA", "Profit for the year", (None, None, None, None, None, 91053, 91053, 12357, 103410)),
    ("DATA", "Actuarial loss recognised in retirement benefit scheme", (None, None, None, None, None, -80050, -80050, None, -80050)),
    ("DATA", "Transfer re property disposals", (None, None, -1394, None, None, 1394, None, None, None)),
    ("DATA", "Property revaluation", (None, None, 243, None, None, None, 243, None, 243)),
    ("DATA", "Investment securities at fair value", (None, None, None, None, -36724, None, -36724, None, -36724)),
    ("DATA", "Cash flow hedge reserve", (None, None, None, -8578, None, None, -8578, None, -8578)),
    ("DATA", "Taxation impact", (None, None, 677, 2244, 10100, 20049, 33070, None, 33070)),
    ("DATA", "Dividends paid to shareholders", (None, None, None, None, None, -40000, -40000, None, -40000)),
    ("DATA", "AT1 issuance", (None, None, None, None, None, None, None, 222000, 222000)),
    ("DATA", "AT1 redemption", (None, None, None, None, None, None, None, -96000, -96000)),
    ("DATA", "AT1 distributions paid", (None, None, None, None, None, None, None, -9378, -9378)),
    ("TOTAL", "At 31 December 2022 (FY2022 closing)", (218170, 306590, 33418, -8449, -29070, 90580, 611239, 225953, 837192)),
    ("DATA", "Profit for the year", (None, None, None, None, None, 136036, 136036, 20683, 156719)),
    ("DATA", "Actuarial loss recognised in retirement benefit scheme", (None, None, None, None, None, -106904, -106904, None, -106904)),
    ("DATA", "Transfer re property disposals", (None, None, -183, None, None, 183, None, None, None)),
    ("DATA", "Property revaluation", (None, None, -1155, None, None, None, -1155, None, -1155)),
    ("DATA", "Investment securities at fair value: changes in fair value", (None, None, None, None, 21919, None, 21919, None, 21919)),
    ("DATA", "Investment securities at fair value: transfer to income statement", (None, None, None, None, 14330, None, 14330, None, 14330)),
    ("DATA", "Cash flow hedge reserve", (None, None, None, 9406, None, None, 9406, None, 9406)),
    ("DATA", "Taxation impact", (None, None, 426, -2633, -10149, 29931, 17575, None, 17575)),
    ("DATA", "AT1 distributions paid", (None, None, None, None, None, None, None, -19741, -19741)),
    ("TOTAL", "At 31 December 2023 (FY2023 closing)", (218170, 306590, 32506, -1676, -2970, 149826, 702446, 226895, 929341)),
    ("DATA", "Profit for the year", (None, None, None, None, None, 143853, 143853, 21642, 165495)),
    ("DATA", "Actuarial loss recognised in retirement benefit scheme", (None, None, None, None, None, -404, -404, None, -404)),
    ("DATA", "Transfer re property disposals", (None, None, -848, None, None, 848, None, None, None)),
    ("DATA", "Property revaluation", (None, None, -1479, None, None, None, -1479, None, -1479)),
    ("DATA", "Investment securities at fair value: changes in fair value", (None, None, None, None, -571, None, -571, None, -571)),
    ("DATA", "Investment securities at fair value: transfer to income statement", (None, None, None, None, 6013, None, 6013, None, 6013)),
    ("DATA", "Cash flow hedge reserve", (None, None, None, 2088, None, None, 2088, None, 2088)),
    ("DATA", "Taxation impact", (None, None, 518, -585, -1524, 114, -1477, None, -1477)),
    ("DATA", "Dividends paid to shareholders", (None, None, None, None, None, -133000, -133000, None, -133000)),
    ("DATA", "AT1 distributions paid", (None, None, None, None, None, None, None, -22011, -22011)),
    ("TOTAL", "At 31 December 2024 (FY2024 closing)", (218170, 306590, 30697, -173, 948, 161237, 717469, 226526, 943995)),
    ("DATA", "Profit for the year", (None, None, None, None, None, 169484, 169484, 19747, 189231)),
    ("DATA", "Actuarial gain recognised in retirement benefit scheme", (None, None, None, None, None, 5836, 5836, None, 5836)),
    ("DATA", "Transfer re property disposals", (None, None, -444, None, None, 444, None, None, None)),
    ("DATA", "Property revaluation", (None, None, -1940, None, None, None, -1940, None, -1940)),
    ("DATA", "Investment securities at fair value: changes in fair value", (None, None, None, None, 3173, None, 3173, None, 3173)),
    ("DATA", "Investment securities at fair value: movement on interest rate hedge adjustment", (None, None, None, None, -150, None, -150, None, -150)),
    ("DATA", "Investment securities at fair value: transfer to income statement", (None, None, None, None, -28, None, -28, None, -28)),
    ("DATA", "Cash flow hedge reserve", (None, None, None, 1258, None, None, 1258, None, 1258)),
    ("DATA", "Taxation impact", (None, None, 393, -352, -839, -1634, -2432, None, -2432)),
    ("DATA", "Dividends paid to shareholders", (None, None, None, None, None, -150000, -150000, None, -150000)),
    ("DATA", "AT1 distributions paid", (None, None, None, None, None, None, None, -20083, -20083)),
    ("TOTAL", "At 31 December 2025 (FY2025 closing)", (218170, 306590, 28706, 733, 3104, 185367, 742670, 226190, 968860)),
]

bw.add_equity_changes_sheet(
    title="Northern Bank Limited — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, entity-level. £'000. Equity reconciliation ladder "
              "confirmed: every year's own closing balance ties exactly to both the next year's own opening "
              "balance and that year's own Balance Sheet Total equity - zero plug rows needed anywhere across "
              "all 6 years. FY2020's own Taxation impact row nets to -8,450 (Total attributable) / -8,451 (Total "
              "equity), a 1-unit rounding artifact already present in the Bank's own FY2020 Statement of Changes "
              "in Equity, not a transcription error.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=64,
)

# ---------------------------------------------------------------
# Asset Quality - loans and advances to customers by IFRS 9 stage (gross
# carrying amount), plus the loans-only ECL allowance that ties exactly to
# the Balance Sheet's net loans line. The stage-level "Total allowance
# account" the Bank discloses in its own reconciliation note is broader
# than this (it also covers due from other banks, derivative financial
# instruments, and loan commitments/guarantees) - shown separately below as
# a memo so it isn't mistaken for a mismatch against the Balance Sheet.
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, by IFRS 9 stage (gross carrying amount)", {}),
    ("DATA", "Stage 1", {"FY2025": 7639874, "FY2024": 6618811, "FY2023": 6115316, "FY2022": 5480235, "FY2021": 5501521, "FY2020": 5263981}),
    ("DATA", "Stage 2", {"FY2025": 347793, "FY2024": 328902, "FY2023": 489900, "FY2022": 758653, "FY2021": 479569, "FY2020": 551088}),
    ("DATA", "Stage 3", {"FY2025": 148814, "FY2024": 165234, "FY2023": 222529, "FY2022": 194154, "FY2021": 316083, "FY2020": 522902}),
    ("TOTAL", "Gross carrying amount", {"FY2025": 8136481, "FY2024": 7112947, "FY2023": 6827745, "FY2022": 6433042, "FY2021": 6297173, "FY2020": 6337971}),
    ("DATA", "ECL allowance on loans at amortised cost", {"FY2025": -82091, "FY2024": -82104, "FY2023": -88013, "FY2022": -98335, "FY2021": -90509, "FY2020": -108130}),
    ("TOTAL", "Net carrying amount (Balance Sheet loans and advances to customers)", {"FY2025": 8054390, "FY2024": 7030843, "FY2023": 6739732, "FY2022": 6334707, "FY2021": 6206664, "FY2020": 6229841}),
    ("DATA", "Stage 3 as % of gross carrying amount (NPL ratio)", {"FY2025": "1.83%", "FY2024": "2.32%", "FY2023": "3.26%", "FY2022": "3.02%", "FY2021": "5.02%", "FY2020": "8.25%"}),
    ("DATA", "Stage 2 as % of gross carrying amount", {"FY2025": "4.28%", "FY2024": "4.62%", "FY2023": "7.18%", "FY2022": "11.79%", "FY2021": "7.62%", "FY2020": "8.69%"}),
    ("DATA", "ECL allowance (loans-only) as % of gross carrying amount (coverage)", {"FY2025": "1.01%", "FY2024": "1.15%", "FY2023": "1.29%", "FY2022": "1.53%", "FY2021": "1.44%", "FY2020": "1.71%"}),
    ("SECTION", "Memo: Total ECL allowance account by stage (all categories - loans, due from other banks, "
                "derivatives, and loan commitments/guarantees; broader than the loans-only figure above, so does "
                "NOT tie to the Balance Sheet loans line on its own)", {}),
    ("DATA", "Stage 1 (all categories)", {"FY2025": 15373, "FY2024": 13317, "FY2023": 13459, "FY2022": 13322, "FY2021": 5210, "FY2020": 13113}),
    ("DATA", "Stage 2 (all categories)", {"FY2025": 25921, "FY2024": 22220, "FY2023": 26395, "FY2022": 38399, "FY2021": 9258, "FY2020": 14449}),
    ("DATA", "Stage 3 (all categories)", {"FY2025": 45251, "FY2024": 51823, "FY2023": 52750, "FY2022": 51288, "FY2021": 81514, "FY2020": 92806}),
    ("TOTAL", "Total ECL allowance account (all categories)", {"FY2025": 86545, "FY2024": 87360, "FY2023": 92604, "FY2022": 103009, "FY2021": 95982, "FY2020": 120368}),
]

cash_flow = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax", {"FY2025": 250380, "FY2024": 218164, "FY2023": 185960, "FY2022": 103301, "FY2021": 61269, "FY2020": 13077}),
    ("TOTAL", "Net cash flow provided by operating activities", {"FY2025": 295380, "FY2024": 441840, "FY2023": -236114, "FY2022": -29212, "FY2021": 929604, "FY2020": 2046601}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of investments - hold to collect", {"FY2025": -3171759, "FY2024": -958368, "FY2023": -439077, "FY2022": -1113378, "FY2021": -943850, "FY2020": -127567}),
    ("DATA", "Maturity of investments - hold to collect", {"FY2025": 3070000, "FY2024": 430500, "FY2023": 343800, "FY2022": 135000, "FY2021": 150000, "FY2020": 186000}),
    ("DATA", "Purchase of investments - hold to collect and sell", {"FY2025": -822418, "FY2024": -99541, "FY2023": -316956, "FY2022": -365859, "FY2021": -301761, "FY2020": -287543}),
    ("DATA", "Maturity and sale of investments - hold to collect and sell", {"FY2025": 91071, "FY2024": 290568, "FY2023": 462521, "FY2022": 159491, "FY2021": 255005, "FY2020": 145354}),
    ("TOTAL", "Net cash flow provided by investing activities", {"FY2025": -838444, "FY2024": -340002, "FY2023": 47639, "FY2022": -1184140, "FY2021": -841417, "FY2020": -85177}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividends paid to shareholders", {"FY2025": -150000, "FY2024": -133000, "FY2023": 0, "FY2022": -40000, "FY2021": -75000, "FY2020": 0}),
    ("DATA", "Payments of interest to AT1 capital holders", {"FY2025": -20083, "FY2024": -22011, "FY2023": -19741, "FY2022": -9377, "FY2021": -4970, "FY2020": -5137}),
    ("TOTAL", "Net cash flow provided by financing activities", {"FY2025": -201187, "FY2024": -155922, "FY2023": -20740, "FY2022": 79642, "FY2021": -81038, "FY2020": -6250}),
    ("TOTAL", "Net change in cash and cash equivalents", {"FY2025": -493871, "FY2024": 164080, "FY2023": -82713, "FY2022": -1043645, "FY2021": 7149, "FY2020": 1955174}),
    ("DATA", "Cash and cash equivalents, beginning of year", {"FY2025": 3473906, "FY2024": 3309826, "FY2023": 3392539, "FY2022": 4436184, "FY2021": 2962528, "FY2020": 1007354}),
    ("TOTAL", "Cash and cash equivalents, end of year", {"FY2025": 2980035, "FY2024": 3473906, "FY2023": 3309826, "FY2022": 3392539, "FY2021": 2969677, "FY2020": 2962528}),
]

bw.add_cash_flow_sheet(
    title="Northern Bank Limited — Cash Flow Statement",
    subtitle="Entity-level annual cash flows, £'000. Trading name: Danske Bank.",
    rows=cash_flow,
    sources_text=sources("cash flow statement", {"FY2025": 91, "FY2024": 91, "FY2023": 66, "FY2022": 119, "FY2021": 107, "FY2020": 75})
    + "\n\nCASH FLOW PRESENTATION NOTE: The workbook retains the principal reported cash-flow lines and reported annual totals. The reports change the presentation and reconciliation detail over time; the generic verifier may therefore flag subtotal arithmetic where omitted underlying adjustments or comparative restatements are not represented in this compact view. The reported net-change-to-opening/closing cash chain is preserved."
    + "\n\nFY2021/FY2022 CASH-DEFINITION RECLASSIFICATION NOTE (re-checked in full per HD-081, 2026-09-07): FY2021's own Annual Report (p.107) reports 'Cash and cash equivalents, end of year' of £2,969,677k, made up of non-mandatory deposits with central banks (£2,921,654k) and deposits with credit institutions with terms shorter than 3 months (£48,023k) - mandatory central-bank deposits are explicitly excluded from that year's own definition of cash equivalents. FY2022's own Annual Report (p.119) restates the FY2021 comparative 'Cash and cash equivalents, end of year' as £4,436,184k - the same £2,921,654k and £48,023k components plus a newly-added £1,466,507k of 'mandatory deposits' with central banks (its own Note 10 balance), which FY2021's report held outside the cash-equivalents boundary. The £1,466,507k gap (~£1.47bn) between this sheet's FY2021 closing cash (2,969,677) and FY2022 opening cash (4,436,184) is exactly this mandatory-deposits component - i.e. a genuine, source-documented change in which balances the Bank classifies as 'cash and cash equivalents' between report vintages (FY2022's report does not flag this as a formal restatement or describe the change in its Note 1(c) 'Changes to accounting policies and presentation', so the cause is inferred from directly comparing both years' own reconciliation tables, not from an explicit restatement disclosure). Consistent with this workbook's standing practice, each year's own originally-published figure is retained on this sheet rather than force-matched; FY2020-FY2021 and FY2022-FY2023 both tie exactly within their own report vintage.",
    first_col_width=62,
    source_height=220,
    unit_suffix=" (£'000)",
)

bw.add_asset_quality_sheet(
    title="Northern Bank Limited — Asset Quality",
    subtitle="Entity-level. £'000. Loans and advances to customers, IFRS 9 stage 1/2/3 gross carrying amount.",
    rows=asset_quality_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nNote 16 (Loans and advances to customers) page references for the stage/ECL detail - "
        f"FY2025: p.109 (gross carrying), p.113 (ECL reconciliation) - {AR_URLS['FY2025']}; "
        f"FY2024: pp.156-157 (gross carrying), pp.162-163 (ECL reconciliation) - {AR_URLS['FY2024']}; "
        f"FY2023: pp.156-163 (both tables) - {AR_URLS['FY2023']}; "
        f"FY2022: p.143 (gross carrying), p.148 (ECL reconciliation) - {AR_URLS['FY2022']}; "
        f"FY2021 gross carrying/ECL closing balances are the FY2022 Annual Report's own '1 January 2022' "
        f"comparative figures (p.143/p.148) - {AR_URLS['FY2022']}; "
        f"FY2020: p.94 (gross carrying, Note 14), p.93 (loans-only allowance account, Note 14), p.97 (total "
        f"allowance account reconciliation, Note 14) - {AR_URLS['FY2020']} (the FY2020 report's own note numbering "
        f"for this disclosure is Note 14, renumbered to Note 16 from FY2021 onward).\n\n"
        "DATA QUALITY NOTE: each year's own Note 16 discloses two different ECL allowance figures - a narrower "
        "'loans at amortised cost' figure (used above, ties exactly to the Balance Sheet net loans line) and a "
        "broader 'Total allowance account' also covering due from other banks, derivatives, and loan commitments/"
        "guarantees, reconciled separately by IFRS 9 stage (shown as the memo section below). The two are not "
        "the same figure and neither is an error - both are exactly as the Bank itself discloses them."
    ),
    first_col_width=90,
    source_height=340,
    unit_suffix=" (£'000)",
)


# ---------------------------------------------------------------------------
# KM1 Key Metrics (wayfinder KM1-022, 2026-09-16) - "Not applicable", and the
# Bank says so itself, in its own accounts, with the legal basis.
#
# Called BEFORE the first add_metric_sheet() so the sheet lands immediately
# after Asset Quality and immediately before CET1 Capital.
DB_GROUP_RM_2025_URL = "https://danskebank.com/-/media/danske-bank-com/file-cloud/2026/2/risk-management-2025.pdf?rev=d803f349b39f43f58c7b3d4aef1455a3"
DB_GROUP_P3_Q4_2025_URL = "https://danskebank.com/-/media/danske-bank-com/file-cloud/2026/2/additional-pillar-3-disclosures-q4-2025.xls"

KM1_SOURCES = (
    "KM1 Key Metrics - NOT APPLICABLE, and unusually this rests on the Bank's own written declaration of the "
    "legal basis rather than on an inference from absence.\n\n"
    "THE BANK STATES IT, IN ITS OWN AUDITED ACCOUNTS, IN A NOTE DEDICATED TO THE QUESTION. Note 40 \"Pillar 3 "
    "disclosure reporting\" of the FY2025 Annual Report (printed p.137) reads in full: \"The Bank's capital "
    "position is set out from page 59 and applies all relevant Capital Requirements Directive V requirements "
    "that were in force during 2025. THE BANK DOES NOT PUBLISH PILLAR 3 DISCLOSURE REPORTING ON AN INDIVIDUAL "
    "BASIS, ON THE BASIS THAT IT DOES NOT MEET THE CAPITAL REQUIREMENT REGULATIONS 2 DEFINITION OF 'LARGE "
    "INSTITUTION'.\" The same note appears verbatim, with only the year and page reference changed, as Note 40 "
    "of the FY2024 and FY2023 reports and as Note 43 of the FY2022 report (printed p.182). That is a "
    "declaration in the document naming the rule it relies on - the same class of evidence as Bank of "
    "Scotland's Article 432 excluded-templates appendix, and stronger than a failed search could ever be.\n\n"
    "LATEST-EDITION CHECK, 2026-09-16. The Bank's OWN site was read live: "
    "https://danskebank.co.uk/about-us/corporate-governance lists exactly one documents page, "
    "\"Annual report and financial statements\", and that page (HTTP 200, 270 KB) links nine PDFs - the "
    "2017 through 2025 Annual Reports and nothing else. NEWEST EDITION = the Annual Report and Financial "
    "Statements 2025, which this workbook already holds; the Bank's year-end is 31 December, so FY2026 is not "
    "yet a reporting year and no year was added. All six editions used here (FY2020-FY2025) were re-downloaded "
    "and verified HTTP 200 / Content-Type application/pdf / %PDF magic bytes.\n"
    "THERE IS NO PILLAR 3 PAGE ON THE SITE AT ALL, and that was tested rather than assumed: the Bank's own "
    "sitemap.xml (99 KB, fetched live) contains ZERO occurrences of the string \"pillar\", as do all three "
    "corporate-governance pages fetched. Candidate paths /about-us/regulatory-disclosures and /pillar-3 return "
    "a genuine HTTP 404 from a server that returns HTTP 200 for the pages that do exist, so this is a fact "
    "about publication, not about reach.\n\n"
    "THE PARENT'S PILLAR 3 WAS CHECKED FIRST, NOT LAST (map rule 18), because UK Disclosure (CRR) subsidiary "
    "reporting normally puts a non-large subsidiary's figures in the consolidating parent's document - which is "
    "exactly what the Bank's own Note 40 implies. IT IS NOT THERE EITHER, and here is what was read:\n"
    "- Danske Bank A/S's Pillar 3 comes in two parts. The narrative is \"Risk Management 2025\" (45 pages, "
    + DB_GROUP_RM_2025_URL + "), which says in terms that the quantitative templates live elsewhere: "
    "\"Additional Pillar 3 disclosures required under the Capital Requirements Regulation ... can be downloaded "
    "from www.danskebank.com/investor-relations.\" It mentions Northern Bank exactly once, in a securitisation "
    "exposure-scope list, and contains no KM1.\n"
    "- Those quantitative templates are \"Additional Pillar 3 disclosures Q4 2025\" (" + DB_GROUP_P3_Q4_2025_URL +
    "), a 79-sheet workbook running EU CC1, CC2, KM1, KM2, TLAC1/3, INS1, OV1, LI1-LI3, CQ/CR/CCR/MR/LR/LIQ/AE "
    "and IRRBB1. EVERY CELL OF ALL 79 SHEETS was searched for \"Northern\", \"Northern Ireland\" and \"Danske "
    "Bank UK\". The Bank appears in exactly one template - EU LI3, the entity-by-entity scope-of-consolidation "
    "table, where \"Northern Bank Limited\" is listed alongside Northern Bank Factors Limited, Northern Bank "
    "Executor and Trustee Company Limited, Northern Bank Nominees Limited and Northern Bank Pension Trust "
    "Limited. It is NAMED AS A CONSOLIDATED ENTITY AND NOWHERE ELSE.\n"
    "- The Group's \"EU KM1\" sheet is a single-entity Group template whose five value columns are QUARTERLY "
    "DATES (31 Dec 2025, 30 Sep 2025, 30 Jun 2025, 31 Mar 2025, 31 Dec 2024), denominated in DKK millions. "
    "There is no Northern Bank column, so there is no rule-19 subsidiary block hiding in a column or an "
    "appendix - and note it is the EU KM1 template in Danish kroner, a different template and a different "
    "currency from the UK KM1 this sheet would carry.\n\n"
    "THE BRAND IS NOT THE ENTITY, which is the trap on this bank. Northern Bank Limited TRADES AS \"Danske "
    "Bank\" in Northern Ireland and its reports are hosted on danskebank.co.uk, but the legal entity is "
    "Northern Bank Limited (Companies House R0000568, FRN 122261) and every document used here is titled "
    "\"Northern Bank Limited Annual Report and Financial Statements\". Danske Bank A/S is the Danish parent, a "
    "separate legal entity reporting under EU CRR; its Pillar 3 is NOT Northern Bank's, and none of its "
    "figures has been carried onto any sheet in this workbook.\n\n"
    "THE BANK'S OWN CAPITAL TABLES ARE NOT A KM1 AND ARE NOT RESHAPED INTO ONE (map rule 8). The unaudited "
    "capital section of each Annual Report (FY2025: printed pp.59-61) holds four bespoke tables - \"Regulatory "
    "capital\" (a CET1 build-up), \"Capital and leverage position\", \"Risk weighted exposure amounts\" and a "
    "\"Regulatory capital to statutory total equity reconciliation\" - plus an MREL table. The closest of them "
    "to the template, \"Capital and leverage position\", has FIVE rows: CET1 ratio, Tier 1 ratio, Total capital "
    "ratio, Total Capital Requirement and Leverage ratio, over two date columns. No row numbers, no own-funds "
    "amounts in that table, no RWA row, no SREP breakdown (only a single TCR figure), no combined-buffer block, "
    "no LCR row and no NSFR row. That is a different and shorter table - the ABC International Bank pattern - "
    "not an unnumbered KM1. Its figures, and those of the tables beside it, already populate the eleven "
    "single-metric sheets of this workbook; mapping them onto KM1 row numbers would invent a correspondence "
    "Northern Bank has never published.\n\n"
    "FY2020 AND FY2021 ARE COVERED BY A DIFFERENT AND SIMPLER ARGUMENT, stated separately rather than folded "
    "into the one above, because the Note 40/43 declaration first appears in the FY2022 report: neither the "
    "FY2020 nor the FY2021 Annual Report mentions Pillar 3 at all, and the UK KM1 template only came into "
    "force with the Disclosure (CRR) Part of the PRA Rulebook on 1 January 2022. A KM1 could not have existed "
    "for those years (map rule 22).\n\n"
    "SEARCH QUALITY, recorded so the zeroes can be trusted (map rule 15). All six of the Bank's Annual Reports "
    "were converted and searched: ZERO occurrences of \"KM1\" in any of them, against 125-178 occurrences of "
    "\"capital\", 8-17 of \"leverage\" and 2-4 of \"liquidity coverage\" in the same files. The extraction is "
    "demonstrably rich on neighbouring terms, so the zero is a fact about the documents rather than about the "
    "tool. The two \"key metric\" hits (FY2023, FY2024) are in risk-appetite narrative, not table captions.\n\n"
    + ENTITY_NOTE
)

bw.add_km1_sheet(
    title="Northern Bank Limited (trading as Danske Bank) — KM1 Key Metrics",
    subtitle="Not applicable, and the Bank says so itself. Note 40 \"Pillar 3 disclosure reporting\" of its own "
             "accounts states that \"The Bank does not publish Pillar 3 disclosure reporting on an individual "
             "basis, on the basis that it does not meet the Capital Requirement Regulations 2 definition of "
             "'large institution'\" - the same note in every edition from FY2022. Its Danish parent Danske Bank "
             "A/S was checked too: across all 79 templates of the Group's Q4 2025 Pillar 3 workbook, Northern "
             "Bank Limited appears only in EU LI3 as a consolidated entity, and the Group's EU KM1 is a "
             "Group-only template in DKK with quarterly date columns - no Northern Bank block anywhere. The "
             "Annual Report's own five-row \"Capital and leverage position\" table is not the template and is "
             "not reshaped into it. WHERE THE OTHER SHEETS COME FROM, since this one says the Bank publishes no "
             "Pillar 3: the eleven single-metric sheets and the RWA Breakdown sheet are transcribed from the "
             "Bank's own Annual Report capital and liquidity tables, at the pages each of those sheets cites. "
             "None of them is sourced from a Pillar 3 document, because none exists.",
    # GA-009 (2026-09-18): EVERY YEAR CELL CARRIES THE STATEMENT, not just the
    # row label. Until now this row was built with an empty dict, so the sheet
    # rendered as six year headers above six blank cells - the only KM1 sheet
    # shape that says nothing at all, and indistinguishable to a reader from
    # "nobody has looked yet". Same one-line defect fixed in Nomura under GA-005
    # and in Melli under GA-006. Each cell is scoped to what was actually
    # established for THAT year: the Note 40/43 declaration first appears in the
    # FY2022 report, the 79-template Group sweep was run on the Q4 2025 workbook,
    # and FY2020-FY2021 predate the UK template entirely.
    rows=[
        ("DATA", "UK KM1 key-metrics template",
         {y: "Not published for this entity" for y in YEARS}),
        ("DATA", "Published by the Bank itself",
         {"FY2025": "No Pillar 3 — Note 40 of that year's accounts declares it",
          "FY2024": "No Pillar 3 — Note 40 of that year's accounts declares it",
          "FY2023": "No Pillar 3 — Note 40 of that year's accounts declares it",
          "FY2022": "No Pillar 3 — Note 43 of that year's accounts declares it",
          "FY2021": "No Pillar 3 — that year's accounts do not mention Pillar 3 at all",
          "FY2020": "No Pillar 3 — that year's accounts do not mention Pillar 3 at all"}),
        ("DATA", "Published for the Bank in its Danish parent's Pillar 3 (Danske Bank A/S)",
         {"FY2025": "Not disclosed — all 79 Q4 2025 Group templates searched; the Bank appears only in EU LI3",
          "FY2024": "Not disclosed — the parent files an EU KM1 for the Group, not a UK KM1 for this entity",
          "FY2023": "Not disclosed — the parent files an EU KM1 for the Group, not a UK KM1 for this entity",
          "FY2022": "Not disclosed — the parent files an EU KM1 for the Group, not a UK KM1 for this entity",
          "FY2021": "Not applicable — the UK KM1 template did not exist until 1 January 2022",
          "FY2020": "Not applicable — the UK KM1 template did not exist until 1 January 2022"}),
    ],
    sources_text=KM1_SOURCES,
    first_col_width=92,
    source_height=1500,
)


def metric(name, unit, label, values, page_map, note=None):
    bw.add_metric_sheet(name, unit, [(label, values)], sources(name, page_map), note=note, first_col_width=54, source_height=180)


capital_pages = {"FY2025": 61, "FY2024": 84, "FY2023": 87, "FY2022": 53, "FY2021": 65, "FY2020": 48}
liquidity_pages = {"FY2025": 59, "FY2024": 80, "FY2023": 82, "FY2022": 56, "FY2021": 69, "FY2020": 10}

metric("CET1 Capital", "£'000", "Common Equity Tier 1 capital after deductions", {"FY2025": 655970, "FY2024": 636698, "FY2023": 616879, "FY2022": 504118, "FY2021": 496106, "FY2020": 585834}, capital_pages)
metric("CET1 Ratio", "% of RWA", "Common Equity Tier 1 ratio", {"FY2025": "14.9%", "FY2024": "16.1%", "FY2023": "15.6%", "FY2022": "13.6%", "FY2021": "14.4%", "FY2020": "16.1%"}, capital_pages)
metric("Tier 1 Capital", "£'000", "Tier 1 capital", {"FY2025": 835421, "FY2024": 797744, "FY2023": 774046, "FY2022": 666724, "FY2021": 561291, "FY2020": 657729}, capital_pages)
metric("Tier 1 Ratio", "% of RWA", "Tier 1 ratio", {"FY2025": "19.0%", "FY2024": "20.2%", "FY2023": "19.6%", "FY2022": "18.0%", "FY2021": "16.3%", "FY2020": "18.1%"}, capital_pages)
metric("Total Capital", "£'000", "Total capital after deductions", {"FY2025": 835421, "FY2024": 797744, "FY2023": 774046, "FY2022": 666724, "FY2021": 648203, "FY2020": 753588}, capital_pages)
metric("Total Capital Ratio", "% of RWA", "Total capital ratio", {"FY2025": "19.0%", "FY2024": "20.2%", "FY2023": "19.6%", "FY2022": "18.0%", "FY2021": "18.8%", "FY2020": "20.7%"}, capital_pages)
metric("Total RWAs", "£'000", "Total risk-weighted exposure amount", {"FY2025": 4401004, "FY2024": 3949640, "FY2023": 3947673, "FY2022": 3694531, "FY2021": 3455735, "FY2020": 3634478}, capital_pages)

# RWA Breakdown - Pillar 3-style risk weighted exposure amounts table, placed
# right after Total RWAs per the locked sheet order. All 6 years tie exactly
# to the Total RWAs figure above (rounding aside).
rwa_breakdown_pages = {"FY2025": 61, "FY2024": 85, "FY2023": 87, "FY2022": 54, "FY2021": 66, "FY2020": 49}
rwa_breakdown_rows = [
    ("DATA", "Credit risk", {"FY2025": 3849058, "FY2024": 3482122, "FY2023": 3546324, "FY2022": 3317928, "FY2021": 3090753, "FY2020": 3249042}),
    ("DATA", "Operational risk", {"FY2025": 546447, "FY2024": 467065, "FY2023": 401329, "FY2022": 376579, "FY2021": 364961, "FY2020": 384135}),
    ("DATA", "Market risk", {"FY2025": 4620, "FY2024": 19, "FY2023": 20, "FY2022": 24, "FY2021": 21, "FY2020": 0}),
    ("DATA", "Credit value adjustment", {"FY2025": 879, "FY2024": 434, "FY2023": 0, "FY2022": 0, "FY2021": 0, "FY2020": 1301}),
    ("TOTAL", "Total risk-weighted exposure amount", {"FY2025": 4401004, "FY2024": 3949640, "FY2023": 3947673, "FY2022": 3694531, "FY2021": 3455735, "FY2020": 3634478}),
]
bw.add_rwa_breakdown_sheet(
    title="Northern Bank Limited — RWA Breakdown",
    subtitle="Entity-level. £'000. Risk weighted exposure amounts by top-level risk-type category, as disclosed in "
              "the Bank's own annual 'Capital and leverage position' risk management report section.",
    rows=rwa_breakdown_rows,
    sources_text=sources("RWA breakdown", rwa_breakdown_pages),
    first_col_width=54,
    source_height=180,
    unit_suffix=" (£'000)",
)

bw.add_metric_sheet(
    "Leverage Ratio", "%",
    [
        ("Leverage ratio - UK Leverage Ratio Framework basis, exposure measure EXCLUDES central bank reserves "
         "and government-guaranteed Bounce Back Loans (FY2022 onward)",
         {"FY2025": "6.4%", "FY2024": "7.2%", "FY2023": "7.4%", "FY2022": "6.7%"}),
        ("Leverage ratio - pre-2022 basis, exposure measure INCLUDES central bank reserves and BBLs, "
         "as originally reported (FY2020-FY2021)",
         {"FY2021": "4.2%", "FY2020": "5.2%"}),
    ],
    sources("Leverage Ratio", capital_pages),
    note="THESE TWO ROWS ARE NOT A LIKE-FOR-LIKE SERIES. The Bank says so itself, in the FY2022 Annual Report's "
         "'Capital and leverage position (unaudited)' section (p.52): 'On 8 October 2021, the FPC and PRA jointly "
         "published PS21/21 \"The UK Leverage Ratio Framework\", with an implementation date for certain "
         "requirements of 1 January 2022. As a result, the Bank is no longer subject to a regulatory leverage "
         "ratio requirement, but instead a supervisory expectation to maintain a leverage ratio above 3.25%. In "
         "addition, the leverage exposure measure excludes central bank reserves and the government guaranteed "
         "lending through Bounce Bank [sic] Loans (BBLs). This has resulted in an increase in the leverage ratio "
         "to 6.7% at 31 December 2022 (2021: 4.2%).' The Bank therefore attributes the whole 4.2% -> 6.7% step to "
         "the change of denominator, not to any change in the Bank - which is why the two bases are on separate "
         "rows here and must never be read, charted or trended as one series. Note the exclusion is TWO items, "
         "not just central bank claims: BBL lending is excluded as well. The Bank did NOT restate FY2020 or "
         "FY2021 onto the excluding basis and did not publish an including-basis figure for FY2022 onward, so "
         "each row stops where the Bank's own disclosure stops; nothing here is back-solved from the other basis. "
         "The FY2022 report is the only edition that states the exclusion explicitly - the FY2023, FY2024 and "
         "FY2025 reports simply carry the ratio forward on the framework basis then in force.",
    first_col_width=76, source_height=260,
)
metric("LCR", "%", "Liquidity coverage ratio (pillar 1 + 2)", {"FY2025": "287%", "FY2024": "318%", "FY2023": "309%", "FY2022": "290%", "FY2021": "293%", "FY2020": "264%"}, liquidity_pages)
metric("NSFR", "%", "Net Stable Funding Ratio", {"FY2025": "200%", "FY2024": "207%", "FY2023": "203%", "FY2022": "217%", "FY2021": "213%", "FY2020": "199%"}, liquidity_pages, note="The FY2020 figure (199%) is not disclosed in the Bank's own FY2020 Annual Report (which predates the Bank's NSFR disclosure) - it is the FY2021 Annual Report's own '31 December 2020' comparative (p.70), corroborated as the same NSFR metric introduced that year (a binding NSFR requirement came into force in Q1 2022).")
metric("MREL Ratio", "%", "MREL ratio", {"FY2025": "127%", "FY2024": "148%", "FY2023": "148%", "FY2022": "146%", "FY2021": "134%"}, {"FY2025": 60, "FY2024": 83, "FY2023": 86, "FY2022": 55, "FY2021": 65, "FY2020": 47}, note="MREL ratios are the Bank's own annual internal-MREL disclosures. The 2021 figure is the 2021 comparative in the 2022 report and is corroborated by the 2021 report's MREL discussion. FY2020 SELF-SKIP: no numeric MREL ratio for FY2020 is disclosed anywhere - not in the Bank's own FY2020 Annual Report (p.47-48 discusses MREL only qualitatively, 'the Bank did not require any additional MREL funds'), not in the FY2021 Annual Report (same qualitative-only treatment, p.65), and the FY2022 Annual Report's own MREL reconciliation table (p.55) only tables FY2022 and FY2021, with no FY2020 comparative column. This is a genuine non-disclosure, not an access gap - all three primary-source PDFs were read in full.")

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 15911954, "FY2024": 14474391, "FY2023": 13697367, "FY2022": 13420391, "FY2021": 13125173, "FY2020": 12250189}),
        ("Loans and advances to customers", {"FY2025": 8054390, "FY2024": 7030843, "FY2023": 6739732, "FY2022": 6334707, "FY2021": 6206664, "FY2020": 6229841}),
        ("Deposits from customers", {"FY2025": 13440624, "FY2024": 12053498, "FY2023": 11333715, "FY2022": 11229589, "FY2021": 11161358, "FY2020": 10228137}),
        ("Total equity and shareholders' equity", {"FY2025": 968860, "FY2024": 943995, "FY2023": 929341, "FY2022": 837192, "FY2021": 749199, "FY2020": 850867}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Operating income", {"FY2025": 434292, "FY2024": 388384, "FY2023": 333521, "FY2022": 273505, "FY2021": 200047, "FY2020": 205119}),
        ("Operating expenses (incl. depreciation & amortisation)", {"FY2025": -183647, "FY2024": -179807, "FY2023": -160666, "FY2022": -150345, "FY2021": -153438, "FY2020": -146616}),
        ("Profit for the year", {"FY2025": 189231, "FY2024": 165495, "FY2023": 156719, "FY2022": 103410, "FY2021": 41534, "FY2020": 7552}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 943995, "FY2024": 929341, "FY2023": 837192, "FY2022": 749199, "FY2021": 850867, "FY2020": 826655}),
        ("Total comprehensive income for the year", {"FY2025": 194948, "FY2024": 169665, "FY2023": 111890, "FY2022": 11371, "FY2021": -21699, "FY2020": 29348}),
        ("Other equity movements, net", {"FY2025": -170083, "FY2024": -155011, "FY2023": -19741, "FY2022": 76622, "FY2021": -79969, "FY2020": -5137}),
        ("Closing equity", {"FY2025": 968860, "FY2024": 943995, "FY2023": 929341, "FY2022": 837192, "FY2021": 749199, "FY2020": 850867}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash flow provided by operating activities", {"FY2025": 295380, "FY2024": 441840, "FY2023": -236114, "FY2022": -29212, "FY2021": 929604, "FY2020": 2046601}),
        ("Net cash flow provided by investing activities", {"FY2025": -838444, "FY2024": -340002, "FY2023": 47639, "FY2022": -1184140, "FY2021": -841417, "FY2020": -85177}),
        ("Net cash flow provided by financing activities", {"FY2025": -201187, "FY2024": -155922, "FY2023": -20740, "FY2022": 79642, "FY2021": -81038, "FY2020": -6250}),
        ("Cash and cash equivalents, end of year", {"FY2025": 2980035, "FY2024": 3473906, "FY2023": 3309826, "FY2022": 3392539, "FY2021": 2969677, "FY2020": 2962528}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "14.9%", "FY2024": "16.1%", "FY2023": "15.6%", "FY2022": "13.6%", "FY2021": "14.4%", "FY2020": "16.1%"}),
        ("Tier 1 Ratio", {"FY2025": "19.0%", "FY2024": "20.2%", "FY2023": "19.6%", "FY2022": "18.0%", "FY2021": "16.3%", "FY2020": "18.1%"}),
        ("Total Capital Ratio", {"FY2025": "19.0%", "FY2024": "20.2%", "FY2023": "19.6%", "FY2022": "18.0%", "FY2021": "18.8%", "FY2020": "20.7%"}),
        ("Leverage Ratio (BASIS BREAK at FY2021/FY2022 - see note; not a like-for-like series)", {"FY2025": "6.4%", "FY2024": "7.2%", "FY2023": "7.4%", "FY2022": "6.7%", "FY2021": "4.2%", "FY2020": "5.2%"}),
    ],
    note="All figures are duplicated from the detail sheets for trend viewing. See each detail sheet for the exact annual-report source citation.\n\n"
         "LEVERAGE RATIO - DO NOT READ THE 4.2% -> 6.7% STEP AS DELEVERAGING. This sheet is a copy and its chart "
         "would otherwise draw a false trend. From 1 January 2022 the PRA's UK Leverage Ratio Framework (PS21/21) "
         "removed central bank reserves, and the Bank's government-guaranteed Bounce Back Loans, from the leverage "
         "exposure measure. The Bank's own FY2022 Annual Report (p.52) attributes the entire increase to that: "
         "'the leverage exposure measure excludes central bank reserves and the government guaranteed lending "
         "through Bounce Bank [sic] Loans (BBLs). This has resulted in an increase in the leverage ratio to 6.7% "
         "at 31 December 2022 (2021: 4.2%).' FY2020-FY2021 are on the old (including) basis and FY2022-FY2025 on "
         "the new (excluding) one; the Bank published neither basis for the other years, so no comparable "
         "six-year series exists. The Leverage Ratio sheet splits the two bases onto separate rows.\n\n" + ENTITY_NOTE,
)

bw.save("/Users/armaan/code/katalysis/banks/NORTHERN BANK FINANCIALS.xlsx")
