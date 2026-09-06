import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, all 12mo to 31 Dec
YEAR_LABEL = {y: y for y in YEARS}

# All 5 years sourced directly from Bank of Scotland plc's own Companies House
# full accounts filings (each year's own originally-filed document, not a
# later comparative) - the bank's own investor-relations site (lloydsbankinggroup.com)
# blocked automated fetches throughout this build.
AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/SC327000/filing-history/MzUxMDk3MTM2NGFkaXF6a2N4/document?format=pdf&download=0"
AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/SC327000/filing-history/MzQ2MDQ2MzkxNmFkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/SC327000/filing-history/MzQxNzI4ODY0NmFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/SC327000/filing-history/MzM3NTQ1ODI2M2FkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/SC327000/filing-history/MzMzNTAwMTQxNWFkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "ENTITY NOTE: Bank of Scotland plc (Companies House SC327000, FRN 169628) is a major UK high-street bank, "
    "wholly owned by Lloyds Banking Group plc - not to be confused with the separate PRA-authorised entity "
    "'Lloyds Bank plc' (FRN 119278), also part of the same group but not yet attempted in this project. All 5 "
    "Companies House filings for this entity are fully scanned/image-only (no text layer at all) despite being a "
    "major bank - every figure below was located by rendering pages and reading them visually, not OCR'd or "
    "text-searched. The bank's own website (lloydsbankinggroup.com) returned a Cloudflare block (error 1007) on "
    "every automated fetch attempt, so no alternative text-native source was available. Every Annual Report "
    "presents both 'The Group' (consolidated, including subsidiaries) and 'The Bank' (Bank of Scotland plc "
    "unconsolidated) columns for both the cash flow statement and, separately, an explicit unconsolidated capital "
    "position for 'the Bank' in the Strategic Report - THE BANK (unconsolidated) basis is used throughout this "
    "workbook for consistency between the cash flow and capital/Pillar 3 sheets."
)

CASH_FLOW_NOTE = (
    "CASH FLOW NOTE - genuine definitional break, not an error: the FY2022 Annual Report restates the FY2021 "
    "comparative cash-and-cash-equivalents balances (Bank: opening £2,208m / closing £2,165m) far above FY2021's "
    "own originally-published figures (Bank: opening £847m / closing £854m) - a ~2.6x jump most likely reflecting "
    "a broadened definition of 'cash and cash equivalents' (e.g. additional short-term interbank placements folded "
    "in) rather than a transcription issue, alongside a much smaller (£50m) revision to the FY2021 operating-"
    "activities total (£6,414m originally vs. £6,364m restated). Per this project's convention, each column below "
    "uses that year's own originally-published figures, so the FY2021 and FY2022 columns are NOT on a directly "
    "comparable cash-equivalents basis at the opening/closing balance level - the activity subtotals (operating/"
    "investing/financing) are only mildly affected. An 'Effect of exchange rate changes on cash and cash "
    "equivalents' line appears in FY2021 and FY2022 only (small, non-zero) and was dropped from the statement "
    "entirely from FY2023 onward - presentation change, not a gap."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Bank of Scotland plc's own unconsolidated ('The Bank') cash flow statement, £m, "
    "from each year's own Companies House full accounts filing:\n"
    f"FY2025: Bank of Scotland plc Annual Report and Accounts 2025, p.26 (Cash flow statements) - {AR2025_URL}\n"
    f"FY2024: Bank of Scotland plc Annual Report and Accounts 2024, p.28 (Cash flow statements) - {AR2024_URL}\n"
    f"FY2023: Bank of Scotland plc Annual Report and Accounts 2023, p.29 (Cash flow statements) - {AR2023_URL}\n"
    f"FY2022: Bank of Scotland plc Annual Report and Accounts 2022, p.29 (Cash flow statements) - {AR2022_URL}\n"
    f"FY2021: Bank of Scotland plc Annual Report and Accounts 2021, p.27 (Cash flow statements) - {AR2021_URL}\n"
    "Each year cross-checked against its own report only (not blended with later comparatives) - see the Cash "
    "Flow Note below.\n\n"
    + CASH_FLOW_NOTE + "\n\n" + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - Bank of Scotland plc's own unconsolidated ('The Bank') capital position, as stated in the "
        "'Capital position' section of the Strategic Report of each year's own Companies House full accounts "
        "filing (no standalone Pillar 3 document is published for this entity - see the Entity Note):\n"
        f"FY2025: Annual Report and Accounts 2025, p.2 - {AR2025_URL}\n"
        f"FY2024: Annual Report and Accounts 2024, p.2 - {AR2024_URL}\n"
        f"FY2023: Annual Report and Accounts 2023, p.2 - {AR2023_URL}\n"
        f"FY2022: Annual Report and Accounts 2022, p.2 - {AR2022_URL}\n"
        f"FY2021: Annual Report and Accounts 2021, p.2 - {AR2021_URL}\n\n"
        + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="Bank of Scotland plc", years=YEARS, year_label=YEAR_LABEL, header_color="003865")

STATEMENTS_SOURCES = (
    "Sources - Bank of Scotland plc's own unconsolidated ('The Bank') Balance sheet / Income statement / "
    "Statement of changes in equity, £m, from each year's own Companies House full accounts filing:\n"
    f"FY2025: Annual Report and Accounts 2025, pp.21-26 - {AR2025_URL}\n"
    f"FY2024: Annual Report and Accounts 2024, pp.21-26 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Accounts 2023, pp.26-29 - {AR2023_URL}\n"
    f"FY2022: Annual Report and Accounts 2023 (2022 comparative column) and Annual Report and Accounts 2022 own "
    f"equity statement - {AR2023_URL} / {AR2022_URL}\n"
    f"FY2021: Annual Report and Accounts 2021, pp.22-26 - {AR2021_URL}\n\n"
    + ENTITY_NOTE
)

PL_NOTE = (
    "PROFIT & LOSS NOTE - genuine disclosure gap, not an omission: from FY2023 back to FY2021, this entity's own "
    "Annual Report does NOT publish a full income statement for 'The Bank' (only for 'The Group'), permitted by "
    "section 408 of the Companies Act 2006 - only the Bank's bottom-line 'Profit for the year' (split between "
    "ordinary shareholders and other equity holders) is disclosed, in a footnote (FY2022/23) or the Statement of "
    "comprehensive income (FY2021). All other P&L line items (interest income, fee income, operating expenses, "
    "etc.) for those 3 years are therefore blank below - not missing data, genuinely not published at Bank level. "
    "Full line-by-line detail is disclosed for the Bank from FY2024 onward."
)

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 2767, "FY2024": 2853, "FY2023": 3009, "FY2022": 3004, "FY2021": 3201}),
    ("DATA", "Items in the course of collection from banks", {"FY2021": 47}),
    ("DATA", "Financial assets at fair value through profit or loss", {"FY2025": 123, "FY2024": 117, "FY2023": 111, "FY2022": 113, "FY2021": 152}),
    ("DATA", "Derivative financial instruments", {"FY2025": 2214, "FY2024": 3337, "FY2023": 2850, "FY2022": 3476, "FY2021": 4264}),
    ("DATA", "Loans and advances to banks", {"FY2025": 97, "FY2024": 78, "FY2023": 180, "FY2022": 171, "FY2021": 50}),
    ("DATA", "Loans and advances to customers", {"FY2025": 306405, "FY2024": 294782, "FY2023": 286187, "FY2022": 283621, "FY2021": 276005}),
    ("DATA", "Debt securities", {"FY2025": 1041, "FY2024": 1350, "FY2023": 1696}),
    ("DATA", "Due from fellow Lloyds Banking Group undertakings", {"FY2025": 18038, "FY2024": 18896, "FY2023": 20921, "FY2022": 22999, "FY2021": 23919}),
    ("TOTAL", "Financial assets at amortised cost", {"FY2025": 325581, "FY2024": 315106, "FY2023": 308984, "FY2022": 306791, "FY2021": 299974}),
    ("DATA", "Financial assets at fair value through other comprehensive income", {"FY2021": 2047}),
    ("DATA", "Goodwill", {"FY2025": 325, "FY2024": 325, "FY2023": 325, "FY2022": 325, "FY2021": 325}),
    ("DATA", "Current tax recoverable", {"FY2025": 450, "FY2024": 1354, "FY2023": 1096, "FY2022": 464, "FY2021": 293}),
    ("DATA", "Deferred tax assets", {"FY2025": 1768, "FY2024": 1886, "FY2023": 1932, "FY2022": 1979, "FY2021": 1991}),
    ("DATA", "Investment in subsidiary undertakings", {"FY2025": 1284, "FY2024": 1284, "FY2023": 1294, "FY2022": 1313, "FY2021": 84}),
    ("DATA", "Retirement benefit assets", {"FY2025": 39, "FY2024": 52, "FY2023": 49, "FY2022": 47, "FY2021": 58}),
    ("DATA", "Other assets", {"FY2025": 1566, "FY2024": 1554, "FY2023": 1459, "FY2022": 1640, "FY2021": 1476}),
    ("TOTAL", "Total assets", {"FY2025": 336117, "FY2024": 327868, "FY2023": 321109, "FY2022": 319152, "FY2021": 313912}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks", {"FY2025": 99, "FY2024": 179, "FY2023": 179, "FY2022": 195, "FY2021": 597}),
    ("DATA", "Customer deposits", {"FY2025": 167586, "FY2024": 165053, "FY2023": 161946, "FY2022": 166363, "FY2021": 170776}),
    ("DATA", "Repurchase agreements at amortised cost", {"FY2025": 10443, "FY2024": 22168, "FY2023": 30397, "FY2022": 30210, "FY2021": 30028}),
    ("DATA", "Due to fellow Lloyds Banking Group undertakings", {"FY2025": 124753, "FY2024": 107189, "FY2023": 94394, "FY2022": 91563, "FY2021": 83193}),
    ("DATA", "Items in the course of transmission to banks", {"FY2021": 98}),
    ("DATA", "Derivative financial instruments", {"FY2025": 2905, "FY2024": 3366, "FY2023": 4297, "FY2022": 4421, "FY2021": 4144}),
    ("DATA", "Notes in circulation", {"FY2025": 2118, "FY2024": 2121, "FY2023": 1392, "FY2022": 1280, "FY2021": 1321}),
    ("DATA", "Debt securities in issue at amortised cost", {"FY2025": 8342, "FY2024": 8077, "FY2023": 7992, "FY2022": 5376, "FY2021": 6140}),
    ("DATA", "Other liabilities", {"FY2025": 1008, "FY2024": 1031, "FY2023": 1290, "FY2022": 1345, "FY2021": 1288}),
    ("DATA", "Provisions", {"FY2025": 368, "FY2024": 464, "FY2023": 655, "FY2022": 897, "FY2021": 1057}),
    ("DATA", "Subordinated liabilities", {"FY2025": 1532, "FY2024": 1533, "FY2023": 1532, "FY2022": 1598, "FY2021": 1644}),
    ("TOTAL", "Total liabilities", {"FY2025": 319154, "FY2024": 311181, "FY2023": 304074, "FY2022": 303248, "FY2021": 300286}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 5847, "FY2024": 5847, "FY2023": 5847, "FY2022": 5847, "FY2021": 5847}),
    ("DATA", "Other reserves", {"FY2025": 3221, "FY2024": 3237, "FY2023": 3235, "FY2022": 3238, "FY2021": 2025}),
    ("DATA", "Retained profits", {"FY2025": 5295, "FY2024": 5003, "FY2023": 5403, "FY2022": 4619, "FY2021": 3554}),
    ("TOTAL", "Ordinary shareholders' equity", {"FY2025": 14363, "FY2024": 14087, "FY2023": 14485, "FY2022": 13704, "FY2021": 11426}),
    ("DATA", "Other equity instruments", {"FY2025": 2600, "FY2024": 2600, "FY2023": 2550, "FY2022": 2200, "FY2021": 2200}),
    ("TOTAL", "Total equity", {"FY2025": 16963, "FY2024": 16687, "FY2023": 17035, "FY2022": 15904, "FY2021": 13626}),
    ("TOTAL", "Total equity and liabilities", {"FY2025": 336117, "FY2024": 327868, "FY2023": 321109, "FY2022": 319152, "FY2021": 313912}),
]

income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 14929, "FY2024": 14569}),
    ("DATA", "Interest expense", {"FY2025": -10454, "FY2024": -10974}),
    ("TOTAL", "Net interest income", {"FY2025": 4475, "FY2024": 3595}),
    ("DATA", "Fee and commission income", {"FY2025": 625, "FY2024": 629}),
    ("DATA", "Fee and commission expense", {"FY2025": -295, "FY2024": -374}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 330, "FY2024": 255}),
    ("DATA", "Net trading income", {"FY2025": 187, "FY2024": 67}),
    ("DATA", "Dividends from subsidiaries", {"FY2025": 406, "FY2024": 184}),
    ("DATA", "Other operating income", {"FY2025": 224, "FY2024": 92}),
    ("TOTAL", "Other income", {"FY2025": 1147, "FY2024": 598}),
    ("TOTAL", "Total income", {"FY2025": 5622, "FY2024": 4193}),
    ("DATA", "Operating expenses", {"FY2025": -3637, "FY2024": -3202}),
    ("DATA", "Impairment (charge) credit", {"FY2025": -89, "FY2024": 24}),
    ("TOTAL", "Profit before tax", {"FY2025": 1896, "FY2024": 1015}),
    ("DATA", "Tax expense", {"FY2025": -385, "FY2024": -183}),
    ("TOTAL", "Profit for the year", {"FY2025": 1511, "FY2024": 832, "FY2023": 926, "FY2022": 1147, "FY2021": 1962}),
    ("DATA", "Profit attributable to ordinary shareholders", {"FY2025": 1274, "FY2024": 626, "FY2023": 740, "FY2022": 1025, "FY2021": 1853}),
    ("DATA", "Profit attributable to other equity holders", {"FY2025": 237, "FY2024": 206, "FY2023": 186, "FY2022": 122, "FY2021": 109}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Other comprehensive income (total), net of tax", {"FY2025": -27, "FY2024": 3, "FY2023": -2, "FY2022": -22, "FY2021": -33}),
    ("TOTAL", "Total comprehensive income for the year, net of tax", {"FY2025": 1484, "FY2024": 835, "FY2023": 924, "FY2022": 1125, "FY2021": 1929}),
]

EQUITY_HEADERS = ["Share capital", "Other reserves", "Retained profits", "Other equity instruments", "Total equity"]
equity_changes_rows = [
    ("TOTAL", "At 1 January 2021", (5847, 2046, 2877, 2200, 12970)),
    ("DATA", "Profit for the year", (None, None, 1853, 109, 1962)),
    ("DATA", "Other comprehensive income, net of tax", (None, -21, -12, None, -33)),
    ("DATA", "Dividends", (None, None, -1200, None, -1200)),
    ("DATA", "Distributions on other equity instruments", (None, None, None, -109, -109)),
    ("DATA", "Capital contributions received", (None, None, 36, None, 36)),
    ("TOTAL", "At 31 December 2021", (5847, 2025, 3554, 2200, 13626)),
    ("DATA", "Profit for the year", (None, None, 1025, 122, 1147)),
    ("DATA", "Other comprehensive income, net of tax", (None, -16, -6, None, -22)),
    ("DATA", "Distributions on other equity instruments", (None, None, None, -122, -122)),
    ("DATA", "Capital contributions received", (None, 1229, 46, None, 1275)),
    ("TOTAL", "At 31 December 2022", (5847, 3238, 4619, 2200, 15904)),
    ("DATA", "Profit for the year", (None, None, 740, 186, 926)),
    ("DATA", "Other comprehensive income, net of tax", (None, -3, 1, None, -2)),
    ("DATA", "Distributions on other equity instruments", (None, None, None, -186, -186)),
    ("DATA", "Issue of other equity instruments", (None, None, None, 350, 350)),
    ("DATA", "Capital contributions received", (None, None, 43, None, 43)),
    ("TOTAL", "At 31 December 2023", (5847, 3235, 5403, 2550, 17035)),
    ("DATA", "Profit for the year", (None, None, 626, 206, 832)),
    ("DATA", "Other comprehensive income, net of tax", (None, 2, 1, None, 3)),
    ("DATA", "Dividends", (None, None, -1050, None, -1050)),
    ("DATA", "Distributions on other equity instruments", (None, None, None, -206, -206)),
    ("DATA", "Issue of other equity instruments", (None, None, None, 1250, 1250)),
    ("DATA", "Repurchases and redemptions of other equity instruments", (None, None, None, -1200, -1200)),
    ("DATA", "Capital contributions received", (None, None, 23, None, 23)),
    ("TOTAL", "At 31 December 2024", (5847, 3237, 5003, 2600, 16687)),
    ("DATA", "Profit for the year", (None, None, 1274, 237, 1511)),
    ("DATA", "Other comprehensive income, net of tax", (None, -16, -11, None, -27)),
    ("DATA", "Dividends", (None, None, -980, None, -980)),
    ("DATA", "Distributions on other equity instruments", (None, None, None, -237, -237)),
    ("DATA", "Capital contributions received", (None, None, 9, None, 9)),
    ("TOTAL", "At 31 December 2025", (5847, 3221, 5295, 2600, 16963)),
]

ASSET_QUALITY_NOTE = (
    "ASSET QUALITY NOTE - IFRS 9 stage breakdown for 'The Bank' (Note 16/13/14 'Loans and advances to customers' "
    "(latterly 'Financial assets at amortised cost'), each year's own Companies House filing). FY2021's own Annual "
    "Report and Accounts 2021 (p.54, Note 13, 'Year ended 31 December 2021 / The Bank') DOES disclose a Bank-level "
    "Stage 1/2/3 movement table - corrected here from an earlier version of this workbook which wrongly treated it "
    "as undisclosed (having only checked the Group-level table); the FY2021 figures below reconcile exactly to the "
    "same Bank-level table repeated as FY2022's own comparative column in the Annual Report and Accounts 2022 (p.56, "
    "Note 13). No by-product loan-type split is separately disclosed for the Bank in any year - stage is the only "
    "breakdown available."
)

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, by IFRS 9 stage (gross carrying amount)", {}),
    ("DATA", "Stage 1", {"FY2025": 272640, "FY2024": 259025, "FY2023": 242505, "FY2022": 237443, "FY2021": 247854}),
    ("DATA", "Stage 2", {"FY2025": 29632, "FY2024": 31405, "FY2023": 38947, "FY2022": 42046, "FY2021": 25363}),
    ("DATA", "Stage 3", {"FY2025": 5377, "FY2024": 5887, "FY2023": 6711, "FY2022": 6946, "FY2021": 5251}),
    ("TOTAL", "Total gross carrying amount", {"FY2025": 307649, "FY2024": 296317, "FY2023": 288163, "FY2022": 286435, "FY2021": 278468}),
    ("SECTION", "Allowance for expected credit losses, by IFRS 9 stage", {}),
    ("DATA", "Stage 1", {"FY2025": 152, "FY2024": 175, "FY2023": 298, "FY2022": 216, "FY2021": 389}),
    ("DATA", "Stage 2", {"FY2025": 427, "FY2024": 514, "FY2023": 711, "FY2022": 935, "FY2021": 748}),
    ("DATA", "Stage 3", {"FY2025": 665, "FY2024": 846, "FY2023": 967, "FY2022": 1663, "FY2021": 1326}),
    ("TOTAL", "Total allowance for expected credit losses", {"FY2025": 1244, "FY2024": 1535, "FY2023": 1976, "FY2022": 2814, "FY2021": 2463}),
    ("TOTAL", "Net carrying amount", {"FY2025": 306405, "FY2024": 294782, "FY2023": 286187, "FY2022": 283621, "FY2021": 276005}),
    ("SECTION", "Asset quality ratios", {}),
    ("DATA", "Drawn ECL coverage (Total allowance / Total gross)", {"FY2025": "0.4%", "FY2024": "0.5%", "FY2023": "0.7%", "FY2022": "1.0%", "FY2021": "0.9%"}),
    ("DATA", "Stage 3 / NPL ratio (Stage 3 gross / Total gross)", {"FY2025": "1.7%", "FY2024": "2.0%", "FY2023": "2.3%", "FY2022": "2.4%", "FY2021": "1.9%"}),
    ("DATA", "Stage 3 coverage (Stage 3 allowance / Stage 3 gross)", {"FY2025": "12.4%", "FY2024": "14.4%", "FY2023": "14.4%", "FY2022": "23.9%", "FY2021": "25.3%"}),
]

RWA_BREAKDOWN_NOTE = (
    "CORRECTION: an earlier version of this workbook marked this sheet 'Not publicly disclosed', claiming the "
    "Strategic Report's Capital position section discloses only the single aggregate risk-weighted-assets total. "
    "That was wrong - immediately below the capital resources table, each year's own Strategic Report has its own "
    "'Risk-weighted assets of the Bank' table with a full breakdown by IRB/Standardised approach and by risk type "
    "(credit/counterparty credit/securitisation/market/operational), reconciling exactly to the Total RWAs sheet "
    "in every year. PRESENTATION NOTE: category labels and sub-splits shift slightly year to year, transcribed "
    "faithfully from each year's own report rather than restated: (1) FY2025's own report folds credit valuation "
    "adjustment (CVA) risk into 'Counterparty credit risk' (footnoted); FY2024-FY2021 show CVA risk as its own "
    "line. (2) FY2021's own report has no separate 'Securitisation' line (folded into Standardised Approach/Other "
    "IRB) and instead shows a 'Underlying risk-weighted assets' subtotal before adding back 'Threshold "
    "risk-weighted assets' to reach the Total - FY2022 onward drop that subtotal and show the threshold figure as "
    "a memo ('of which') line below an already-inclusive Total. The FY2022 report's own comparative column for "
    "FY2021 restates Other IRB Approach/Standardised Approach/Credit risk slightly differently (adding a separate "
    "Securitisation line) while the Total RWAs figure (60,807) is unchanged either way - this workbook uses "
    "FY2021's own report figures, per the per-year-own-source convention used throughout."
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - Bank of Scotland plc's own 'Risk-weighted assets of the Bank' table, in the 'Capital position' "
    "section of the Strategic Report, each year's own Companies House full accounts filing:\n"
    f"FY2025: Annual Report and Accounts 2025, p.2 - {AR2025_URL}\n"
    f"FY2024: Annual Report and Accounts 2024, p.2 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Accounts 2023, p.2 - {AR2023_URL}\n"
    f"FY2022: Annual Report and Accounts 2022, p.2 - {AR2022_URL}\n"
    f"FY2021: Annual Report and Accounts 2021, p.2 - {AR2021_URL}\n\n"
    + RWA_BREAKDOWN_NOTE + "\n\n" + ENTITY_NOTE
)
rwa_breakdown_rows = [
    ("SECTION", "Risk-weighted assets of the Bank, by approach", {}),
    ("DATA", "Foundation Internal Ratings Based (IRB) Approach", {"FY2025": 1942, "FY2024": 2159, "FY2023": 2492, "FY2022": 2605, "FY2021": 3476}),
    ("DATA", "Retail IRB Approach", {"FY2025": 63418, "FY2024": 65594, "FY2023": 61956, "FY2022": 53771, "FY2021": 41636}),
    ("DATA", "Other IRB Approach", {"FY2025": 3786, "FY2024": 3740, "FY2023": 3917, "FY2022": 3863, "FY2021": 1557}),
    ("TOTAL", "IRB Approach", {"FY2025": 69146, "FY2024": 71493, "FY2023": 68365, "FY2022": 60239, "FY2021": 46669}),
    ("DATA", "Standardised (STA) Approach", {"FY2025": 6196, "FY2024": 3136, "FY2023": 3457, "FY2022": 4307, "FY2021": 4389}),
    ("TOTAL", "Credit risk", {"FY2025": 75342, "FY2024": 74629, "FY2023": 71821, "FY2022": 64546, "FY2021": 51058}),
    ("SECTION", "Risk-weighted assets of the Bank, by risk type", {}),
    ("DATA", "Securitisation", {"FY2025": 722, "FY2024": 707, "FY2023": 931, "FY2022": 463}),
    ("DATA", "Counterparty credit risk", {"FY2025": 188, "FY2024": 136, "FY2023": 162, "FY2022": 191, "FY2021": 333}),
    ("DATA", "Credit valuation adjustment risk", {"FY2024": 51, "FY2023": 72, "FY2022": 77, "FY2021": 46}),
    ("DATA", "Operational risk", {"FY2025": 6051, "FY2024": 5909, "FY2023": 6799, "FY2022": 7751, "FY2021": 8488}),
    ("DATA", "Market risk", {"FY2025": 54, "FY2024": 61, "FY2023": 468, "FY2022": 56, "FY2021": 254}),
    ("TOTAL", "Underlying risk-weighted assets", {"FY2021": 60179}),
    ("DATA", "Threshold risk-weighted assets (of which, already included above)", {"FY2025": 2806, "FY2024": 2926, "FY2023": 3205, "FY2022": 3190, "FY2021": 628}),
    ("TOTAL", "Total risk-weighted assets", {"FY2025": 82357, "FY2024": 81493, "FY2023": 80254, "FY2022": 73084, "FY2021": 60807}),
]

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax", {"FY2025": 1896, "FY2024": 1015, "FY2023": 901, "FY2022": 1213, "FY2021": 2305}),
    ("DATA", "Change in operating assets", {"FY2025": -9007, "FY2024": -5430, "FY2023": -481, "FY2022": -6488, "FY2021": 2094}),
    ("DATA", "Change in operating liabilities", {"FY2025": 8052, "FY2024": 7275, "FY2023": 1135, "FY2022": 3169, "FY2021": 2275}),
    ("DATA", "Non-cash and other items", {"FY2025": -454, "FY2024": -346, "FY2023": -1434, "FY2022": 478, "FY2021": 251}),
    ("DATA", "Tax paid", {"FY2025": -296, "FY2024": -1364, "FY2023": -556, "FY2022": -208, "FY2021": -511}),
    ("DATA", "Tax refunded", {"FY2025": 942, "FY2024": 970}),
    ("TOTAL", "Net cash provided by/(used in) operating activities", {"FY2025": 1133, "FY2024": 2120, "FY2023": -435, "FY2022": -1836, "FY2021": 6414}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Dividends received from subsidiaries", {"FY2025": 406, "FY2024": 184, "FY2023": 719, "FY2022": 126, "FY2021": 49}),
    ("DATA", "Purchase of financial assets", {"FY2021": -107}),
    ("DATA", "Proceeds from sale and maturity of financial assets", {"FY2022": 1955, "FY2021": 399}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -172, "FY2024": -194, "FY2023": -219, "FY2022": -158, "FY2021": -171}),
    ("DATA", "Purchase of other intangible assets", {"FY2025": -114, "FY2024": -76}),
    ("DATA", "Proceeds from sale of property, plant and equipment", {"FY2025": 10, "FY2024": 36, "FY2023": 13, "FY2021": 41}),
    ("DATA", "Proceeds from goodwill and other intangible assets", {"FY2024": 1}),
    ("DATA", "Additional capital injections to subsidiaries", {"FY2025": -37}),
    ("TOTAL", "Net cash (used in)/provided by investing activities", {"FY2025": 93, "FY2024": -49, "FY2023": 513, "FY2022": 1923, "FY2021": 211}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividends paid to ordinary shareholders", {"FY2025": -980, "FY2024": -1050, "FY2021": -1200}),
    ("DATA", "Distributions on other equity instruments", {"FY2025": -237, "FY2024": -206, "FY2023": -186, "FY2022": -122, "FY2021": -109}),
    ("DATA", "Interest paid on subordinated liabilities", {"FY2025": -96, "FY2024": -108, "FY2023": -105, "FY2022": -58, "FY2021": -94}),
    ("DATA", "Proceeds from issue of subordinated liabilities", {"FY2021": 500}),
    ("DATA", "Proceeds from issue of other equity instruments", {"FY2024": 1250, "FY2023": 350}),
    ("DATA", "Repayment of subordinated liabilities", {"FY2023": -63, "FY2022": -44, "FY2021": -5714}),
    ("DATA", "Repurchases and redemptions of other equity instruments", {"FY2024": -1200}),
    ("TOTAL", "Net cash used in/(provided by) financing activities", {"FY2025": -1313, "FY2024": -1314, "FY2023": -4, "FY2022": -224, "FY2021": -6617}),
    ("DATA", "Effect of exchange rate changes on cash and cash equivalents", {"FY2022": -1, "FY2021": -1}),
    ("TOTAL", "Change in cash and cash equivalents", {"FY2025": -87, "FY2024": 757, "FY2023": 74, "FY2022": -138, "FY2021": 7}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 2858, "FY2024": 2101, "FY2023": 2027, "FY2022": 2165, "FY2021": 847}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 2771, "FY2024": 2858, "FY2023": 2101, "FY2022": 2027, "FY2021": 854}),
]

bw.add_balance_sheet_sheet(
    title="Bank of Scotland plc — Balance Sheet",
    subtitle="Unconsolidated ('The Bank') basis, £m. See source note at bottom.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=62,
    source_height=200,
    unit_suffix=" (£m)",
)

bw.add_income_statement_sheet(
    title="Bank of Scotland plc — Profit & Loss",
    subtitle="Unconsolidated ('The Bank') basis, £m. See source note at bottom.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + PL_NOTE,
    first_col_width=62,
    source_height=260,
    unit_suffix=" (£m)",
)

bw.add_equity_changes_sheet(
    title="Bank of Scotland plc — Statement of Changes in Equity",
    subtitle="Unconsolidated ('The Bank') basis, £m, chronological, 1 January 2021 - 31 December 2025",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=52,
    source_height=200,
)

bw.add_cash_flow_sheet(
    title="Bank of Scotland plc — Cash Flow Statement",
    subtitle="Unconsolidated ('The Bank') basis, £m. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=280,
    unit_suffix=" (£m)",
)

bw.add_asset_quality_sheet(
    title="Bank of Scotland plc — Asset Quality",
    subtitle="Unconsolidated ('The Bank') basis, £m. See source note at bottom.",
    rows=asset_quality_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + ASSET_QUALITY_NOTE,
    first_col_width=62,
    source_height=220,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 / capital metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, f"Unconsolidated ('The Bank') basis, {unit}" if unit else "Unconsolidated ('The Bank') basis",
                         rows_data, p3_sources(), note=note, first_col_width=48, source_height=180)


metric(
    "CET1 Capital", "£m",
    [("Common equity tier 1 capital", {"FY2025": 11083, "FY2024": 11028, "FY2023": 11966, "FY2022": 11284, "FY2021": 9540})],
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common equity tier 1 capital ratio", {"FY2025": "13.5%", "FY2024": "13.5%", "FY2023": "14.9%", "FY2022": "15.4%", "FY2021": "15.7%"})],
)

metric(
    "Tier 1 Capital", "£m",
    [("Total tier 1 capital", {"FY2025": 13683, "FY2024": 13628, "FY2023": 14516, "FY2022": 13484, "FY2021": 11762})],
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 capital ratio", {"FY2025": "16.6%", "FY2024": "16.7%", "FY2023": "18.1%", "FY2022": "18.5%", "FY2021": "19.3%"})],
)

metric(
    "Total Capital", "£m",
    [("Total capital resources", {"FY2025": 15183, "FY2024": 15402, "FY2023": 16410, "FY2022": 15330, "FY2021": 13259})],
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "18.4%", "FY2024": "18.9%", "FY2023": "20.4%", "FY2022": "21.0%", "FY2021": "21.8%"})],
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted assets", {"FY2025": 82357, "FY2024": 81493, "FY2023": 80254, "FY2022": 73084, "FY2021": 60807})],
)

bw.add_rwa_breakdown_sheet(
    title="Bank of Scotland plc — RWA Breakdown",
    subtitle="Unconsolidated ('The Bank') basis, £m. See source note at bottom.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=62,
    source_height=280,
    unit_suffix=" (£m)",
)

metric(
    "Leverage Ratio", "%",
    [("UK leverage ratio", {"FY2025": "4.3%", "FY2024": "4.4%", "FY2023": "4.8%", "FY2022": "4.5%"})],
    note="Not disclosed in FY2021's own Annual Report, nor in FY2022's own Annual Report (the FY2022 capital "
         "table has no leverage-ratio row at all) - the UK leverage ratio template was only introduced to this "
         "entity's own disclosure from the FY2023 Annual Report onward. The FY2022 figure (4.5%) shown here comes "
         "from FY2023's report, which is the first to show it as a prior-year comparative; FY2021 is left blank "
         "since no source (that year's own report or the following year's comparative) ever discloses it.",
)

bw.add_not_disclosed_metric_sheets(
    ["LCR", "NSFR", "MREL Ratio"],
    p3_sources(),
    per_note={
        "LCR": "Bank of Scotland plc's own Annual Report contains no dedicated risk-management/liquidity "
               "disclosure section and no standalone Pillar 3 document is published for this entity - LCR is "
               "disclosed only at the wider Lloyds Banking Group plc consolidated level, which is out of scope "
               "for this entity-level workbook.",
        "NSFR": "Same as the LCR note - not disclosed at this entity level.",
        "MREL Ratio": "Same as the LCR note - not disclosed at this entity level; MREL is set and disclosed at "
                      "the Lloyds Banking Group plc resolution-group level, not for Bank of Scotland plc solo.",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 336117, "FY2024": 327868, "FY2023": 321109, "FY2022": 319152, "FY2021": 313912}),
        ("Loans and advances to customers", {"FY2025": 306405, "FY2024": 294782, "FY2023": 286187, "FY2022": 283621, "FY2021": 276005}),
        ("Customer deposits", {"FY2025": 167586, "FY2024": 165053, "FY2023": 161946, "FY2022": 166363, "FY2021": 170776}),
        ("Total equity", {"FY2025": 16963, "FY2024": 16687, "FY2023": 17035, "FY2022": 15904, "FY2021": 13626}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total income", {"FY2025": 5622, "FY2024": 4193}),
        ("Operating expenses", {"FY2025": -3637, "FY2024": -3202}),
        ("Profit for the year", {"FY2025": 1511, "FY2024": 832, "FY2023": 926, "FY2022": 1147, "FY2021": 1962}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 16687, "FY2024": 17035, "FY2023": 15904, "FY2022": 13626, "FY2021": 12970}),
        ("Total comprehensive income", {"FY2025": 1484, "FY2024": 835, "FY2023": 924, "FY2022": 1125, "FY2021": 1929}),
        ("Other movements, net", {"FY2025": -1208, "FY2024": -1183, "FY2023": 207, "FY2022": 1153, "FY2021": -1273}),
        ("Closing equity", {"FY2025": 16963, "FY2024": 16687, "FY2023": 17035, "FY2022": 15904, "FY2021": 13626}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash provided by/(used in) operating activities", {"FY2025": 1133, "FY2024": 2120, "FY2023": -435, "FY2022": -1836, "FY2021": 6414}),
        ("Net cash (used in)/provided by investing activities", {"FY2025": 93, "FY2024": -49, "FY2023": 513, "FY2022": 1923, "FY2021": 211}),
        ("Net cash used in/(provided by) financing activities", {"FY2025": -1313, "FY2024": -1314, "FY2023": -4, "FY2022": -224, "FY2021": -6617}),
        ("Cash and cash equivalents at end of year", {"FY2025": 2771, "FY2024": 2858, "FY2023": 2101, "FY2022": 2027, "FY2021": 854}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "13.5%", "FY2024": "13.5%", "FY2023": "14.9%", "FY2022": "15.4%", "FY2021": "15.7%"}),
        ("Tier 1 Ratio", {"FY2025": "16.6%", "FY2024": "16.7%", "FY2023": "18.1%", "FY2022": "18.5%", "FY2021": "19.3%"}),
        ("Total Capital Ratio", {"FY2025": "18.4%", "FY2024": "18.9%", "FY2023": "20.4%", "FY2022": "21.0%", "FY2021": "21.8%"}),
        ("Leverage Ratio", {"FY2025": "4.3%", "FY2024": "4.4%", "FY2023": "4.8%", "FY2022": "4.5%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. LCR/NSFR/MREL are not shown here (not disclosed at "
         "this entity level - see those sheets). The FY2021-to-FY2022 cash-flow figures are not on a directly "
         "comparable cash-equivalents basis - see the Cash Flow Statement sheet's note.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BANK OF SCOTLAND FINANCIALS.xlsx")
