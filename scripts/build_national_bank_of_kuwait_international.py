import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


# Entity confirmed against Banks List 2608.xlsx and Companies House:
# National Bank of Kuwait (International) Plc, company 02773743, FRN 171532.
# The entity is a wholly-owned UK subsidiary of National Bank of Kuwait S.A.K.P.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

AR_URLS = {
    "FY2025": "https://www.nbk.com/dam/jcr:6d7dc8ff-20d6-4ba1-be40-03386a48becd/nbki-financial-statements-2025.pdf",
    "FY2024": "https://www.nbk.com/dam/jcr:04623e62-4149-4a86-99a6-989cd9285e7e/NBKI-Financial-Statement-2024.pdf",
    "FY2023": "https://www.nbk.com/dam/jcr:a2323d07-848e-4518-971d-8e24a3395ad0/NBKI-Financial-Statement-2023.pdf",
    "FY2022": "https://www.nbk.com/dam/jcr:d333e5bb-2545-40a2-90a6-59a827646b7b/NBKI-Financial-Statement-2022.pdf",
    "FY2021": "https://www.nbk.com/dam/jcr:c3c72c41-97cb-454c-b14e-2a77baf033ab/NBKI-Financial-Statement-2021.pdf",
}
PILLAR_URL = "https://www.nbk.com/dam/jcr:19757e7d-4d03-40f8-bf39-63c995186e39/Pillar_III_Disclosures.pdf"

ENTITY_NOTE = (
    "National Bank of Kuwait (International) Plc (company 02773743, FRN 171532, LEI "
    "213800OTQ2BHFRVL6A46) is the entity in Banks List 2608.xlsx. Companies House confirms "
    "the active public company, incorporated 9 December 1992, with accounts made up to 31 December. "
    "The Bank is a wholly-owned subsidiary of National Bank of Kuwait S.A.K.P. and is regulated by the PRA and FCA."
)

CF_NOTE = (
    "No Statement of Cash Flows is published for FY2021–FY2025. The audited reports are prepared under FRS 101 "
    "Reduced Disclosure Framework and the independent auditor's report identifies the financial statements as the "
    "statement of income, statement of comprehensive income, statement of financial position, statement of changes "
    "in equity, and related notes; a cash-flow statement is not included. This is therefore a Pillar-3-only workbook."
)


def annual_sources(extra=""):
    text = ENTITY_NOTE + "\n\nOfficial annual reports and financial statements:\n"
    capital_pages = {
        # Verified 2026-09-06 (HD-066): FY2021 AR's own Note 32 "Capital management
        # (unaudited)" is on p.72; FY2023 AR's own Note 31 (same title) is on p.72;
        # FY2022 AR's own Note 31 is actually on p.65, not p.64 (corrected here).
        # FY2024 and FY2025's own accounts contain no capital management note at all
        # (both end at Country by Country Reporting - Note 30 and Note 31
        # respectively; the FY2025 accounts' own going-concern section references a
        # non-existent "Note 32" - a dangling cross-reference in the Bank's own
        # document, not an error introduced here) - capital figures for these two
        # years come solely from the Pillar 3 disclosure cited below.
        "FY2025": "no capital management note published in the statutory accounts (see note)",
        "FY2024": "no capital management note published in the statutory accounts (see note)",
        "FY2023": "Note 31 \"Capital management (unaudited)\" p.72",
        "FY2022": "Note 31 \"Capital management (unaudited)\" p.65",
        "FY2021": "Note 32 \"Capital management (unaudited)\" p.72",
    }
    text += "\n".join(f"{y}: {capital_pages[y]}, {AR_URLS[y]}" for y in YEARS)
    if extra:
        text += "\n\n" + extra
    return text


def p3_sources(extra=""):
    return annual_sources(
        "Official NBKI Pillar 3 Disclosure 31 December 2025 (Table 3, Key Metrics, p.16; "
        f"includes 31 December 2024 comparative values): {PILLAR_URL}" + ("\n\n" + extra if extra else "")
    )


STATEMENTS_SOURCES = annual_sources(
    "Statement of Income, Statement of Financial Position, and Statement of Changes in Equity: "
    "FY2025 - AR2025 pp.28-31 (Statement of Income p.28, Statement of Comprehensive Income p.29, "
    "Statement of Financial Position p.30, Statement of Changes in Equity p.31), plus Notes 3-9 "
    "(interest/fee/expense detail, pp.43-45), all in £'000. FY2024 comparative from the same AR2025 "
    "pages. FY2023 - AR2023 pp.22, 24-25 (Statement of Income p.22, Statement of Financial Position "
    "p.24, Statement of Changes in Equity p.25), in US$'000. FY2022 - AR2022 pp.22, 24-25 (own "
    "contemporaneous filing, not AR2023's comparative), in US$'000. FY2021 - AR2021 pp.23-26 "
    "(Statement of Income p.23, Statement of Comprehensive Income p.24, Statement of Financial "
    "Position p.25, Statement of Changes in Equity p.26), in $'000 (the FY2021 filing labels its "
    "own currency column \"$000\" without the \"US\" prefix; treated as US$'000, consistent with "
    "later years' explicit US$ labelling and the unbroken equity roll-forward against FY2022's own "
    "restated FY2021 comparative).\n\n"
    "INVESTMENT SECURITIES BREAKDOWN: the 'Investment securities - ...' sub-rows below the renamed "
    "'Total investment securities' line are transcribed from each year's own Note 15 'Investment "
    "Securities' of the Notes to the Financial Statements, which splits the balance by measurement "
    "basis (equities at FVOCI / equities at FVPL / debt securities at FVOCI / debt securities at "
    "FVPL) plus a combined 'Less: ECL' line and (FY2022-FY2025 only) a combined interest-receivable "
    "line. No issuer-type split (e.g. UK government/gilts vs supranational/corporate) is disclosed "
    "anywhere in Note 15 or elsewhere in any year's report; the Bank's own repurchase-agreement note "
    "(Note 20, FY2025 AR p.50) states that Gilts pledged as repo collateral 'remain on the statement "
    "of financial position within investment securities' but gives no total gilts holding, so an "
    "issuer-type split cannot be derived:\n"
    "FY2025: Note 15, p.48 - " + AR_URLS["FY2025"] + "\n"
    "FY2024: same FY2025 filing's own FY2024 comparative column, Note 15, p.48\n"
    "FY2023: Note 15, p.43 - " + AR_URLS["FY2023"] + "\n"
    "FY2022: same FY2023 filing's own FY2022 comparative column, Note 15, p.43\n"
    "FY2021: Note 15, p.43 - " + AR_URLS["FY2021"] + "\n\n"
    "Each year's sub-rows sum exactly to that year's renamed 'Total investment securities' line. "
    "'Debt securities (FVPL)' is FY2021-only (reclassified out of the portfolio by FY2022); "
    "'Interest receivable (accrued)' is not disclosed as a separate line in the FY2021 note (folded "
    "into the FVOCI/FVPL debt balances that year) - blank cells reflect the note's own year-by-year "
    "composition, not a gap.\n\n"
    "CURRENCY NOTE: the Bank's presentation currency changed from USD to GBP between the FY2023 and "
    "FY2024 statutory accounts (matching the change already documented on the Pillar 3 sheets' "
    "CAPITAL_UNIT note). The FY2023 closing US$533,729k equity was retranslated to the FY2024 opening "
    "balance of £419,962k using the Bank's own year-end spot rate - this is a genuine currency "
    "redenomination, not a plug; the Statement of Changes in Equity sheet shows both figures as "
    "separate, clearly labelled rows rather than forcing a same-currency tie-out across the boundary. "
    "The Balance Sheet and Profit & Loss sheets are similarly presented on each year's own reported "
    "currency (US$'000 for FY2021-FY2023, £'000 for FY2024-FY2025) without an imposed conversion.\n\n"
    "ASSET QUALITY NOTE: FY2021 and FY2022's own-year loans-and-advances IFRS 9 stage split and "
    "impairment allowance are from each year's own Maximum Exposure to Credit Risk note (AR2022 "
    "Note 28.1.4 p.57-58 for FY2021/FY2022; AR2023 Note 28.1.4 p.63 for FY2022/FY2023 comparative "
    "used only to cross-check; AR2025 Note 29.1.4 pp.69-70 for FY2024/FY2025). Net carrying values "
    "tie exactly to each year's own Balance Sheet loans and advances to customers figure once the "
    "notes' own \"presented without accrued interest\" caveat is accounted for."
)


bw = BankWorkbook(
    bank_name="National Bank of Kuwait (International) Plc",
    years=YEARS,
    header_color="1F4E79",
)

bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at Central Bank / cash and cash equivalents", {"FY2025": 280213, "FY2024": 547502, "FY2023": 551396, "FY2022": 528440, "FY2021": 732863}),
    ("DATA", "Deposits with banks", {"FY2025": 666586, "FY2024": 840214, "FY2023": 1156167, "FY2022": 832185, "FY2021": 644300}),
    ("DATA", "Loans and advances to banks", {"FY2025": 156952, "FY2024": 96803, "FY2023": 104012, "FY2022": 78750, "FY2021": 26012}),
    ("DATA", "Loans and advances to customers", {"FY2025": 2205331, "FY2024": 1975643, "FY2023": 2028637, "FY2022": 1610422, "FY2021": 1585574}),
    ("DATA", "Total investment securities", {"FY2025": 550717, "FY2024": 398439, "FY2023": 357952, "FY2022": 264917, "FY2021": 213944}),
    ("DATA", "Investment securities - Equities (FVOCI)", {"FY2025": 2145, "FY2024": 2025, "FY2023": 1772, "FY2022": 1407, "FY2021": 1018}),
    ("DATA", "Investment securities - Equities (FVPL)", {"FY2025": 85, "FY2024": 46, "FY2023": 137, "FY2022": 11361, "FY2021": 252}),
    ("DATA", "Investment securities - Debt securities (FVOCI)", {"FY2025": 543552, "FY2024": 392799, "FY2023": 352409, "FY2022": 249601, "FY2021": 170839}),
    ("DATA", "Investment securities - Debt securities (FVPL)", {"FY2021": 41872}),
    ("DATA", "Investment securities - Interest receivable (accrued)", {"FY2025": 5039, "FY2024": 3634, "FY2023": 3691, "FY2022": 2577}),
    ("DATA", "Investment securities - Less: ECL allowance", {"FY2025": -104, "FY2024": -65, "FY2023": -57, "FY2022": -29, "FY2021": -37}),
    ("DATA", "Investment in group entity", {"FY2023": 0, "FY2022": 44000, "FY2021": 45792}),
    ("DATA", "Derivative assets", {"FY2025": 20557, "FY2024": 23453, "FY2023": 11890, "FY2022": 15296, "FY2021": 6401}),
    ("DATA", "Fixed assets", {"FY2025": 41862, "FY2024": 39969, "FY2023": 50764, "FY2022": 49253, "FY2021": 55230}),
    ("DATA", "Other assets", {"FY2025": 19645, "FY2024": 12547, "FY2023": 7177, "FY2022": 2423, "FY2021": 10231}),
    ("TOTAL", "Total assets", {"FY2025": 3941863, "FY2024": 3934570, "FY2023": 4267995, "FY2022": 3425686, "FY2021": 3320347}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Due to banks and other financial institutions", {"FY2025": 758900, "FY2024": 1020083, "FY2023": 1338382, "FY2022": 1078891, "FY2021": 863405}),
    ("DATA", "Customer deposits", {"FY2025": 2355436, "FY2024": 2126886, "FY2023": 1987234, "FY2022": 1611651, "FY2021": 1524917}),
    ("DATA", "Repurchase agreements", {"FY2025": 70065, "FY2024": 0}),
    ("DATA", "Certificates of deposit issued", {"FY2025": 185765, "FY2024": 257778, "FY2023": 345265, "FY2022": 213478, "FY2021": 441222}),
    ("DATA", "Derivative liabilities", {"FY2025": 13155, "FY2024": 3724, "FY2023": 18843, "FY2022": 18207, "FY2021": 32857}),
    ("DATA", "Other liabilities", {"FY2025": 21344, "FY2024": 24121, "FY2023": 44542, "FY2022": 29636, "FY2021": 10213}),
    ("TOTAL", "Total liabilities", {"FY2025": 3404665, "FY2024": 3432592, "FY2023": 3734266, "FY2022": 2951863, "FY2021": 2872614}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 283329, "FY2024": 283329, "FY2023": 289403, "FY2022": 289403, "FY2021": 235883}),
    ("DATA", "Retained earnings", {"FY2025": 251956, "FY2024": 217721, "FY2023": 244271, "FY2022": 211715, "FY2021": 225681}),
    ("DATA", "Cumulative changes in fair values", {"FY2025": 1913, "FY2024": 928, "FY2023": 1882, "FY2022": 1016, "FY2021": -2186}),
    ("DATA", "Translation / exchange reserve", {"FY2023": -1827, "FY2022": -28311, "FY2021": -11645}),
    ("TOTAL", "Total equity", {"FY2025": 537198, "FY2024": 501978, "FY2023": 533729, "FY2022": 473823, "FY2021": 447733}),
    ("TOTAL", "Total equity and liabilities", {"FY2025": 3941863, "FY2024": 3934570, "FY2023": 4267995, "FY2022": 3425686, "FY2021": 3320347}),
]

bw.add_balance_sheet_sheet(
    title="National Bank of Kuwait (International) Plc — Balance Sheet",
    subtitle="Entity basis. As reported: £'000 (FY2024-FY2025); US$'000 (FY2021-FY2023) - see Currency Note. "
              "The Bank sold its Investment in group entity (NBK France S.A.) in June 2023; the line is blank from "
              "FY2024 rather than zero. Repurchase agreements is a new FY2025 line (not previously used). "
              "'Investment securities - ...' sub-rows below the renamed 'Total investment securities' line are a "
              "measurement-basis breakdown per Note 15 - see Investment Securities Breakdown note; no issuer-type "
              "split is disclosed in any year's report.",
    rows=bs_rows, sources_text=STATEMENTS_SOURCES, first_col_width=68, source_height=460, unit_suffix="",
)

pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 221400, "FY2024": 225162, "FY2023": 227709, "FY2022": 88876, "FY2021": 52080}),
    ("DATA", "Interest expense", {"FY2025": -133279, "FY2024": -140090, "FY2023": -135198, "FY2022": -34660, "FY2021": -12443}),
    ("TOTAL", "Net interest income", {"FY2025": 88121, "FY2024": 85072, "FY2023": 92511, "FY2022": 54216, "FY2021": 39637}),
    ("DATA", "Net fees and commissions income", {"FY2025": 2677, "FY2024": 4032, "FY2023": 3431, "FY2022": 5916, "FY2021": 5539}),
    ("DATA", "Net gains from dealing in foreign currencies and derivative income", {"FY2025": 784, "FY2024": 227, "FY2023": 2211, "FY2022": 24428, "FY2021": 6047}),
    ("DATA", "Net investment income", {"FY2025": 112, "FY2024": 287, "FY2023": 587, "FY2022": 2627, "FY2021": 1069}),
    ("DATA", "Other operating income", {"FY2025": 108, "FY2024": 179, "FY2023": 396, "FY2022": 366, "FY2021": 387}),
    ("TOTAL", "Net operating income before ECL", {"FY2025": 91802, "FY2024": 89797, "FY2023": 99136, "FY2022": 87553, "FY2021": 52679}),
    ("DATA", "Charge/(release) on expected credit losses", {"FY2025": -3789, "FY2024": -1112, "FY2023": -1789, "FY2022": 665, "FY2021": 2004}),
    ("TOTAL", "Net operating income after ECL", {"FY2025": 88013, "FY2024": 88685, "FY2023": 97347, "FY2022": 88218, "FY2021": 54683}),
    ("DATA", "Administrative expenses", {"FY2025": -41151, "FY2024": -44114, "FY2023": -47648, "FY2022": -38714, "FY2021": -31911}),
    ("DATA", "Depreciation", {"FY2025": -1043, "FY2024": -863, "FY2023": -1061, "FY2022": -1136, "FY2021": -1597}),
    ("TOTAL", "Operating expenses", {"FY2025": -42194, "FY2024": -44977, "FY2023": -48709, "FY2022": -39850, "FY2021": -33508}),
    ("TOTAL", "Profit for the year before taxation", {"FY2025": 45819, "FY2024": 43708, "FY2023": 48638, "FY2022": 48368, "FY2021": 21175}),
    ("DATA", "Taxation", {"FY2025": -11584, "FY2024": -11139, "FY2023": -12761, "FY2022": -25945, "FY2021": -4099}),
    ("TOTAL", "Profit for the year", {"FY2025": 34235, "FY2024": 32569, "FY2023": 35877, "FY2022": 22423, "FY2021": 17076}),
    ("SECTION", "Other comprehensive income/(expense) for the year", {}),
    ("DATA", "Change in fair value of debt securities measured at FVOCI (net of tax)", {"FY2025": 894, "FY2024": -830, "FY2021": -124}),
    ("DATA", "Change in fair value of equity instruments measured at FVOCI (net of tax)", {"FY2025": 91, "FY2024": 277, "FY2021": -45}),
    ("DATA", "Change in fair value of investment in subsidiary measured at FVOCI (net of tax)", {"FY2021": -2759}),
    ("DATA", "Change in fair value of debt/equity securities and investment in subsidiary (combined, FY2022-FY2023)", {"FY2023": -2455, "FY2022": 3202}),
    ("DATA", "Net foreign currency translation effect / translation reserve movement", {"FY2023": 26484, "FY2022": -53055, "FY2021": -6296}),
    ("TOTAL", "Other comprehensive income/(expense) for the year", {"FY2025": 985, "FY2024": -553, "FY2023": 24029, "FY2022": -49853, "FY2021": -9224}),
    ("TOTAL", "Total comprehensive income/(expense) for the year", {"FY2025": 35220, "FY2024": 32016, "FY2023": 59906, "FY2022": -27430, "FY2021": 7852}),
]

bw.add_income_statement_sheet(
    title="National Bank of Kuwait (International) Plc — Profit & Loss",
    subtitle="Entity basis. As reported: £'000 (FY2024-FY2025); US$'000 (FY2021-FY2023) - see Currency Note. "
              "FY2023 Total comprehensive income is shown before a small FY2023-only fair-value/retained-earnings "
              "transfer (US$3,321k, net-zero within equity) disclosed on the Statement of Changes in Equity.",
    rows=pl_rows, sources_text=STATEMENTS_SOURCES, first_col_width=82, source_height=460, unit_suffix="",
)

equity_headers = ["Share capital", "Retained earnings", "Cumulative changes in fair values", "Translation / exchange reserve", "Total equity"]
equity_rows = [
    ("TOTAL", "At 1 January 2021 (FY2020 closing, restated, US$'000)", (235883, 208605, 742, -5349, 439881)),
    ("DATA", "Profit for the year", (None, 17076, None, None, 17076)),
    ("DATA", "Other comprehensive expense for the year", (None, None, -2928, -6296, -9224)),
    ("TOTAL", "At 31 December 2021 (FY2021 closing, US$'000)", (235883, 225681, -2186, -11645, 447733)),
    ("DATA", "New capital issuance", (53520, None, None, None, 53520)),
    ("DATA", "Transfer from translation reserve upon redenomination", (None, -36389, None, 36389, 0)),
    ("DATA", "Profit for the year", (None, 22423, None, None, 22423)),
    ("DATA", "Other comprehensive expense for the year", (None, None, 3202, -53055, -49853)),
    ("TOTAL", "At 31 December 2022 (FY2022 closing, US$'000)", (289403, 211715, 1016, -28311, 473823)),
    ("DATA", "Profit for the year", (None, 35877, None, None, 35877)),
    ("DATA", "Other comprehensive income for the year", (None, None, -2455, 26484, 24029)),
    ("DATA", "Transfer between fair value reserve and retained earnings", (None, -3321, 3321, None, 0)),
    ("TOTAL", "At 31 December 2023 (FY2023 closing, US$'000)", (289403, 244271, 1882, -1827, 533729)),
    ("TOTAL", "At 31 December 2023, retranslated as the FY2024 opening balance (GBP'000 - see Currency Note)", (233329, 185152, 1481, None, 419962)),
    ("DATA", "Profit for the year", (None, 32569, None, None, 32569)),
    ("DATA", "Other comprehensive expense for the year", (None, None, -553, None, -553)),
    ("DATA", "New share capital", (50000, None, None, None, 50000)),
    ("TOTAL", "At 31 December 2024 (FY2024 closing, £'000)", (283329, 217721, 928, None, 501978)),
    ("DATA", "Profit for the year", (None, 34235, None, None, 34235)),
    ("DATA", "Other comprehensive income for the year", (None, None, 985, None, 985)),
    ("TOTAL", "At 31 December 2025 (FY2025 closing, £'000)", (283329, 251956, 1913, None, 537198)),
]

bw.add_equity_changes_sheet(
    title="National Bank of Kuwait (International) Plc — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, entity basis. US$'000 through FY2023, £'000 from FY2024 "
              "onward - see Currency Note. Equity reconciliation ladder confirmed: every year's own closing balance "
              "ties exactly to both the next year's own opening balance and that year's own Balance Sheet Total "
              "equity, including across the FY2023-to-FY2024 currency-redenomination boundary (US$533,729k "
              "retranslated to £419,962k, shown as its own explicit row rather than forced to tie in the same "
              "currency). The ladder's mandated scan caught the FY2022 New Capital Issuance (US$53,520k), the "
              "same year's Transfer from Translation Reserve upon Redenomination (a genuine, net-zero internal "
              "reclassification - not related to the later FY2023/FY2024 currency change), the FY2023 fair-value/"
              "retained-earnings transfer (US$3,321k, net-zero), and the FY2025 New Share Capital issuance "
              "(£50,000k).",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=64,
)

# The entity takes the FRS 101 cash-flow disclosure exemption.
bw.add_cash_flow_sheet(
    title="National Bank of Kuwait (International) Plc — Cash Flow Statement",
    subtitle="Not applicable — FRS 101 cash-flow-statement disclosure exemption",
    rows=[
        ("SECTION", "No Statement of Cash Flows is published by this entity in any year", {}),
        ("DATA", CF_NOTE, {}),
    ],
    sources_text=annual_sources(CF_NOTE),
    first_col_width=100,
    source_height=280,
    unit_suffix="",
)

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers - gross carrying amount by IFRS 9 stage", {}),
    ("DATA", "Stage 1, gross carrying amount", {"FY2025": 2080805, "FY2024": 1817638, "FY2023": 1775545, "FY2022": 1310456, "FY2021": 1305813}),
    ("DATA", "Stage 2, gross carrying amount", {"FY2025": 79368, "FY2024": 103476, "FY2023": 223370, "FY2022": 199829, "FY2021": 266914}),
    ("DATA", "Stage 3, gross carrying amount", {"FY2025": 33666, "FY2024": 45284, "FY2023": 17683, "FY2022": 96744, "FY2021": 18025}),
    ("TOTAL", "Total gross carrying amount", {"FY2025": 2193839, "FY2024": 1966398, "FY2023": 2016598, "FY2022": 1607029, "FY2021": 1590752}),
    ("SECTION", "ECL allowance by stage", {}),
    ("DATA", "Stage 1 allowance", {"FY2025": -1770, "FY2024": -1652, "FY2023": -1871, "FY2022": -1310, "FY2021": -1712}),
    ("DATA", "Stage 2 allowance", {"FY2025": -731, "FY2024": -156, "FY2023": -639, "FY2022": -798, "FY2021": -1462}),
    ("DATA", "Stage 3 allowance", {"FY2025": -1713, "FY2024": -4761, "FY2023": -3507, "FY2022": -2503, "FY2021": -2243}),
    ("TOTAL", "Total ECL allowance", {"FY2025": -4214, "FY2024": -6569, "FY2023": -6017, "FY2022": -4611, "FY2021": -5417}),
    ("TOTAL", "Net carrying amount (excludes accrued interest - see source note)", {"FY2025": 2189625, "FY2024": 1959829, "FY2023": 2010581, "FY2022": 1602418, "FY2021": 1585335}),
    ("SECTION", "Derived ratios", {}),
    ("DATA", "Stage 3 (NPL) ratio - Stage 3 gross / total gross", {"FY2025": "1.53%", "FY2024": "2.30%", "FY2023": "0.88%", "FY2022": "6.02%", "FY2021": "1.13%"}),
    ("DATA", "Overall coverage ratio - total ECL allowance / total gross", {"FY2025": "0.19%", "FY2024": "0.33%", "FY2023": "0.30%", "FY2022": "0.29%", "FY2021": "0.34%"}),
    ("DATA", "Stage 3 coverage ratio - Stage 3 allowance / Stage 3 gross", {"FY2025": "5.09%", "FY2024": "10.51%", "FY2023": "19.83%", "FY2022": "2.59%", "FY2021": "12.44%"}),
]

bw.add_asset_quality_sheet(
    title="National Bank of Kuwait (International) Plc — Asset Quality",
    subtitle="Entity basis, loans and advances to customers only (the Bank's Maximum Exposure to Credit Risk note "
              "also covers cash, deposits with banks, credit institutions, and FVOCI debt securities, all Stage 1 "
              "with negligible impairment every year - omitted here as not customer lending risk). US$'000 through "
              "FY2023, £'000 from FY2024 - see Currency Note. Net carrying amount ties exactly to each year's own "
              "gross-minus-allowance arithmetic and closely to the Balance Sheet's loans and advances to customers "
              "line (small remaining gap is the note's own \"presented without accrued interest\" caveat).",
    rows=asset_quality_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=280,
    unit_suffix="",
)


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(
        name,
        unit,
        rows_data,
        p3_sources(),
        note=note,
        first_col_width=58,
        source_height=220,
    )


# FY2021–FY2023 capital figures are reported in US$000 in the statutory
# accounts; FY2024–FY2025 are reported in GBP£000 after the presentation-
# currency change. Values are kept as reported and the unit note is explicit.
CAPITAL = {"FY2025": 536637, "FY2024": 501570, "FY2023": 533272, "FY2022": 453162, "FY2021": 432220}
RWAS = {"FY2025": 2624404, "FY2024": 2503806, "FY2023": 2599821, "FY2022": 2131640, "FY2021": 2034858}
CAPITAL_RATIOS = {"FY2025": "20.45%", "FY2024": "20.03%", "FY2023": "20.51%", "FY2022": "21.26%", "FY2021": "21.24%"}

CAPITAL_UNIT = "As reported: £000 (FY2024–FY2025); US$000 (FY2021–FY2023)"
CAPITAL_NOTE = (
    "CET1, Tier 1, and Total Capital are equal in every year because the Bank reports no Tier 2 capital and its "
    "regulatory capital is comprised entirely of CET1. FY2021–FY2023 are reported in US$000; FY2024–FY2025 are "
    "reported in GBP£000 following the presentation-currency change. No conversion has been imposed.\n\n"
    "DATA QUALITY NOTE (FY2021/FY2022, verified 2026-09-06, HD-066): the FY2021 and FY2022 CET1/Total Capital and "
    "ratio figures here are taken from each year's own audited Annual Report Note 32/31 \"Capital management "
    "(unaudited)\" (US$432,220k/21.24% for FY2021; US$453,162k/21.26% for FY2022 - each self-consistent against "
    "the same year's own RWA of US$2,034,858k/US$2,131,640k to the basis point). Both years' archived Pillar 3 "
    "disclosures state different capital amounts against the identical RWA: the \"December 2021\"-dated document's "
    "own Table 1 states US$432,220k (matching the AR) but pairs it with a 21.81% ratio that is arithmetically "
    "inconsistent with that amount (432,220/2,034,858 = 21.24%, not 21.81% - an apparent error within that "
    "document); the \"December 2023\"-dated document's own Table 3/5 states a different, internally-consistent "
    "pair for both years (US$443,710k/21.81% FY2021; US$474,412k/22.26% FY2022 - each ties exactly to the same "
    "RWA). The two Pillar 3 documents' own RWA, Leverage Ratio, LCR, and NSFR agree with each other and are used "
    "on those sheets; only the CET1/Total Capital amount and ratio are disputed between the Bank's own statutory "
    "accounts and its own Pillar 3 disclosures for these two years, and the statutory accounts' figures are used "
    "here as the audited-adjacent, internally self-consistent source.\n\n"
    "RE-ESTABLISHED FIRST-HAND 2026-09-16 (KM1-022), from the documents rather than from this note: AR2022 "
    "Note 31 (printed p.65) and AR2021 Note 32 (printed p.73) were re-read and confirm 453,162/21.26% and "
    "432,220/21.24% against RWA of 2,131,640 and 2,034,858, with \"Tier 2 capital  -\" in every year; the "
    "\"December 2023\"-dated Pillar 3's p.16 was rendered at 300 dpi and confirms 474,412/22.26% and "
    "443,710/21.81%, corroborated by that same edition's Table 5 own-funds composition on p.18. Both sides "
    "are internally consistent; they differ only in the regulatory adjustments applied to the same audited "
    "equity. The KM1 Key Metrics sheet in this workbook carries the PILLAR 3 side, this sheet carries the "
    "AUDITED side, and the workbook verifier reports the resulting four-cell disagreement on every run - "
    "which is the intended outcome, not an open defect. See the KM1 sheet's source note for the full "
    "four-way test that ruled out a row-alignment slip."
)

# ---------------------------------------------------------------
# KM1 Key Metrics - NBKI's own "Table 3: Key metrics" (section 4.2 of its
# Pillar 3 Disclosure). Reproduced whole, in the Bank's own row order, with
# the Bank's own labels, section headings, glyphs and printed precision.
#
#   * NO ROW NUMBERS ARE PRINTED, so none are shown here. NBKI's table carries
#     the KM1 row set and the template's own section headings in the template's
#     own order (available own funds -> RWA -> capital ratios -> leverage ->
#     LCR -> NSFR, down to the "Total exposure measure excluding claims on
#     central banks" and the HQLA / net-cash-outflow LCR build-up), so it IS
#     the template, unnumbered. Attaching template row numbers to it would
#     invent a correspondence the Bank never published, so the rows are left
#     as the Bank labelled them.
#
#   * THE BANK PRINTS A SUBSET OF THE TEMPLATE'S ROWS. There is no Tier 1
#     ratio row (rows 1-3 and the Total Capital Ratio are printed, row 6 is
#     not), no SREP block (UK 7a-7d), no buffer block (8, 9, 11, UK 11a, 12),
#     and no NSFR build-up (available/required stable funding). Those cells are
#     absent from the source, not missing from this transcription.
#
#   * A SOURCE DEFECT, REPRODUCED NOT CORRECTED. The FY2022 edition prints the
#     "Common Equity Tier 1 (CET1) capital" row with BOTH cells empty, while
#     giving Tier 1 Capital and Total Capital. Those two cells are therefore
#     blank here. (Every other year the three amounts are identical, because
#     NBKI holds no AT1 and no Tier 2.) The same editions' standing lead-in
#     sentence also claims the table covers "buffer requirements and ratios",
#     which it does not print.
#
#   * THE UNIT CHANGES BETWEEN EDITIONS (map rule 17). FY2021 and FY2022 were
#     published in US$'000 ("In USD $"), FY2024 and FY2025 in £'000 ("In GBP
#     000's"), following the Bank's presentation-currency change. No single row
#     can express that, so - RESTRUCTURED 2026-09-16 under map rule 17 - every
#     AMOUNT row is split into two caption blocks, one per unit, the same shape
#     rule 5 uses for the leverage basis break. RATIO rows stay single, because
#     a percentage is unit-free. Nothing is converted and nothing is restated
#     into the other edition's unit; within each unit block the Bank's own row
#     order is preserved exactly.
#
#   * FY2023 IS BLANK BECAUSE NO FY2023 EDITION EXISTS TO TRANSCRIBE. NBKI
#     republishes at one stable URL rather than minting a per-year file, and
#     no FY2023 vintage was ever archived; the live FY2025 edition carries
#     only a single FY2024 comparative. See the RWA Breakdown sheet's
#     fourth-verification note - this gap is closed by enumeration.
#
#   * FY2021 COMES FROM THE FY2022 EDITION'S COMPARATIVE COLUMN, the one
#     departure from "each year from its own edition", because the FY2021
#     edition does not print this table at all: its "Table 1: Key metrics USD
#     000's as at 31.12.2021" is a different object, an eight-tile dashboard
#     (CET1 capital / Total Regulatory capital / CET1 ratio / Total Capital
#     ratio / Total RWAs / Leverage Ratio / LCR / NSFR) with no section
#     structure, no Tier 1 row and no LCR build-up. Same situation as Bank of
#     Scotland's FY2021. The divergence between the two is recorded in the
#     source note below rather than reconciled.
# ---------------------------------------------------------------
# Map rule 17: amount rows carry TWO caption blocks, one per unit. GBP first
# (FY2024-FY2025, the newer editions, and the leftmost columns), USD second
# (FY2021-FY2022). Ratio rows stay single.
GBP = "  [£'000, FY2024-FY2025 editions]"
USD = "  [US$'000, FY2021-FY2022 editions]"

km1_rows = [
    ("SECTION", "Available own funds (amounts)", {}),
    ("DATA", "Common Equity Tier 1 (CET1) capital *" + GBP,
     {"FY2025": 536637, "FY2024": 501570}),
    # Blank on purpose: the FY2022 edition prints this caption with BOTH cells
    # empty. Its own Table 5 (Capital movement, p.18) DOES give the figure -
    # 474,412 and 443,710 - but this sheet reproduces Table 3, so the blank
    # stands and the cross-reference is recorded in the source note.
    ("DATA", "Common Equity Tier 1 (CET1) capital" + USD, {}),
    ("DATA", "Tier 1 Capital" + GBP,
     {"FY2025": 536637, "FY2024": 501570}),
    ("DATA", "Tier 1 Capital" + USD,
     {"FY2022": 474412, "FY2021": 443710}),
    ("DATA", "Total Capital" + GBP,
     {"FY2025": 536637, "FY2024": 501570}),
    ("DATA", "Total Capital" + USD,
     {"FY2022": 474412, "FY2021": 443710}),
    ("SECTION", "Risk Weighted Assets", {}),
    ("DATA", "Total RWA" + GBP,
     {"FY2025": 2624404, "FY2024": 2503806}),
    ("DATA", "Total RWA" + USD,
     {"FY2022": 2131640, "FY2021": 2034858}),
    ("SECTION", "Capital Ratios (as percentage of RWA)", {}),
    ("DATA", "Common Equity Tier 1 Ratio",
     {"FY2025": "20.45%", "FY2024": "20.03%", "FY2022": "22.26%", "FY2021": "21.81%"}),
    ("DATA", "Total Capital Ratio",
     {"FY2025": "20.45%", "FY2024": "20.03%", "FY2022": "22.26%", "FY2021": "21.81%"}),
    ("SECTION", "Leverage Ratio", {}),
    ("DATA", "Total exposure measure excluding claims on central banks" + GBP,
     {"FY2025": 4062395, "FY2024": 4133905}),
    ("DATA", "Total exposure measure excluding claims on central banks" + USD,
     {"FY2022": 3625281, "FY2021": 3482137}),
    ("DATA", "Leverage ratio excluding claims on central banks (%)",
     {"FY2025": "13.21%", "FY2024": "12.13%", "FY2022": "13.09%", "FY2021": "12.74%"}),
    ("SECTION", "Liquidity Coverage Ratio ('LCR')", {}),
    ("DATA", "Total high-quality liquid assets (HQLA) (Weighted value average)" + GBP,
     {"FY2025": 731707, "FY2024": 925985}),
    ("DATA", "Total high-quality liquid assets (HQLA) (Weighted value average)" + USD,
     {"FY2022": 659703, "FY2021": 702588}),
    ("DATA", "Total net cash outflows (adjusted value)" + GBP,
     {"FY2025": 147299, "FY2024": 215454}),
    ("DATA", "Total net cash outflows (adjusted value)" + USD,
     {"FY2022": 220185, "FY2021": 209655}),
    ("DATA", "Liquidity coverage ratio (%) (adjusted value)",
     {"FY2025": "497%", "FY2024": "430%", "FY2022": "300%", "FY2021": "227%"}),
    ("SECTION", "Net Stable Funding Ratio ('NSFR')", {}),
    ("DATA", "NSFR ratio (%)   [FY2022 edition: \"NSFR ratio (%) (adjusted value)\"]",
     {"FY2025": "120%", "FY2024": "127%", "FY2022": "127%", "FY2021": "114%"}),
]

KM1_SOURCES = (
    "Sources - National Bank of Kuwait (International) Plc's own Pillar 3 Disclosure, section 4.2 \"Key "
    "Metrics\", Table 3 \"Key metrics\". Amounts and percentages exactly as printed; nothing converted, "
    "rounded or computed:\n"
    f"FY2025 and FY2024: Pillar 3 Disclosure 31 December 2025, Table 3, p.16, columns '31 Dec 2025' and "
    f"'31 Dec 2024', \"In GBP 000's\" - {PILLAR_URL}\n"
    "FY2022 and FY2021: the archived edition whose cover reads \"Pillar 3 Disclosure / December 2023\" but "
    "whose Table 3 columns read '31/12/22' and '31/12/21', \"In USD $\", p.16 - Wayback Machine capture of the "
    "same stable URL, 2024-02-17: https://web.archive.org/web/20240217111133/https://www.nbk.com/dam/"
    "jcr:19757e7d-4d03-40f8-bf39-63c995186e39/Pillar_III_Disclosures.pdf\n"
    "FY2023: no edition exists to transcribe (see below).\n\n"
    "LATEST-EDITION CHECK, 2026-09-16. The Bank's own live Pillar 3 URL was re-fetched directly (HTTP 200, "
    "Content-Type application/pdf, %PDF magic bytes verified) and serves the 31 December 2025 edition - the "
    "newest NBKI Pillar 3 published. NBK's group investor-relations page (https://www.nbk.com/nbk-group/"
    "investor-relations.html) was also read in full: the only NBKI-named Pillar 3 it links is a 2014 file. "
    "FY2025 is therefore the newest edition and this workbook already holds it; no year was added.\n\n"
    "TRANSCRIPTION NOTES:\n"
    "• NO ROW NUMBERS. NBKI prints this table unnumbered. It carries the KM1 row set and the template's own "
    "section headings in the template's own order, so it is the template - but the Bank's rows are reproduced "
    "under the Bank's own labels, with no template row numbers attached, because attaching them would assert "
    "a correspondence the Bank never published.\n"
    "• ROWS THE BANK DOES NOT PRINT ARE ABSENT FROM THE SOURCE, not missing from this sheet: no Tier 1 ratio "
    "row, no SREP block (UK 7a-7d), no buffer block (8, 9, 11, UK 11a, 12), and no NSFR stable-funding "
    "build-up. The lead-in sentence's claim that the table covers \"buffer requirements and ratios\" is the "
    "Bank's own; no buffer row is in fact printed. Recorded, not corrected.\n"
    "• A BLANK CET1 ROW IN THE FY2022 EDITION IS THE SOURCE'S OWN. That edition prints the \"Common Equity "
    "Tier 1 (CET1) capital\" caption with both value cells EMPTY, while printing Tier 1 Capital and Total "
    "Capital as 474,412 / 443,710. RE-VERIFIED 2026-09-16 by rendering p.16 at 300 dpi and looking: the table "
    "is fully ruled, every row sits in its own bordered cell, and the CET1 row's two cells are visibly empty. "
    "The two cells are therefore left blank here. In every year NBKI does print all three, they are "
    "identical, because the Bank holds no AT1 and no Tier 2. The SAME EDITION does supply the missing figure "
    "two pages later - its section 4.4 \"Composition of Regulatory Own Funds\", Table 5 \"Capital movement\" "
    "(p.18), prints \"Common Equity Tier 1 (CET1) capital after Regulatory adjustments\" as 474,412 and "
    "443,710 - but this sheet reproduces Table 3, and filling Table 3's blank from Table 4/5 would be "
    "normalising, so the blank stands and the cross-reference is recorded here instead.\n"
    "• THE UNIT CHANGES BETWEEN EDITIONS, so every AMOUNT row is split into two caption blocks (restructured "
    "2026-09-16 under map rule 17). FY2021-FY2022 are US$'000 - the FY2022 edition's stub column reads \"In "
    "USD $\" - while FY2024-FY2025 are £'000, the FY2025 edition's stub reading \"In GBP 000's\" with both "
    "column heads repeating \"GBP 000's\", after the Bank's presentation-currency change from USD to GBP. No "
    "single row can carry two units honestly, so each amount row appears twice, once per unit, the same shape "
    "map rule 5 uses for the leverage basis break. RATIO rows stay single, because a percentage is unit-free. "
    "Nothing is converted and neither edition's amounts are restated into the other's unit; within each unit "
    "block the Bank's own row order is preserved exactly.\n"
    "• The asterisk on the CET1 row is the Bank's own: the FY2025 edition footnotes it \"* Includes audited "
    "current year profits\". The FY2022 edition carries no such footnote.\n"
    "• LABEL DRIFT on the last row: the FY2025 edition prints \"NSFR ratio (%)\"; the FY2022 edition prints "
    "\"NSFR ratio (%) (adjusted value)\". Both are shown in the row label rather than one being chosen.\n"
    "• FY2021 IS THE FY2022 EDITION'S COMPARATIVE COLUMN, deliberately, because the FY2021 edition prints no "
    "such table. Its \"Table 1: Key metrics USD 000's as at 31.12.2021\" (p.3) is an eight-tile dashboard "
    "with no section structure, no Tier 1 row and no LCR build-up - a different object, not an unnumbered "
    "template - so it cannot supply these rows: https://web.archive.org/web/20231209144740/"
    "https://www.nbk.com/dam/jcr:19757e7d-4d03-40f8-bf39-63c995186e39/Pillar_III_Disclosures.pdf\n"
    "• AND THE TWO EDITIONS DISAGREE FOR FY2021, which is why the choice matters. The FY2021 edition's own "
    "dashboard gives CET1 capital and Total Regulatory capital as US$432,220k with a CET1/Total Capital "
    "ratio of 21.81%, against Total RWAs of US$2,034,858k - an internally impossible pair (432,220/2,034,858 "
    "= 21.24%). The FY2022 edition's comparative column gives US$443,710k with the same 21.81%, which does "
    "tie (443,710/2,034,858 = 21.81%). Its RWA, leverage ratio (12.74%), LCR (227%) and NSFR (114%) are "
    "identical in both editions. Both figures are recorded, neither is reconciled.\n\n"
    "WHY THIS SHEET AND THE CET1 RATIO / TOTAL CAPITAL RATIO SHEETS DISAGREE FOR FY2021 AND FY2022 - FOUR "
    "CELLS, EACH RE-ESTABLISHED FROM THE SOURCES ON 2026-09-16 AND EACH A GENUINE DIVERGENCE BETWEEN TWO OF "
    "THE BANK'S OWN DOCUMENTS, NOT A TRANSCRIPTION ERROR. The four are: CET1 Ratio FY2022 (this sheet 22.26% "
    "vs the CET1 Ratio sheet's 21.26%), CET1 Ratio FY2021 (21.81% vs 21.24%), and Total Capital Ratio for "
    "the same two years, which carry the identical pair of figures.\n"
    "  THE SUSPICION THAT HAD TO BE RULED OUT was a row-alignment slip: this table prints the SAME percentage "
    "for its CET1 Ratio row and its Total Capital Ratio row in both years, which is the classic signature of "
    "rows sliding by one during extraction. It was ruled out four ways, all first-hand:\n"
    "  (1) The FY2022 edition's p.16 was RENDERED AT 300 DPI AND LOOKED AT, not read from the text layer. The "
    "table is fully ruled; \"Common Equity Tier 1 Ratio 22.26% | 21.81%\" and \"Total Capital Ratio 22.26% | "
    "21.81%\" each sit in their own bordered row, one below the other. Nothing has slid.\n"
    "  (2) The ratios tie to the amounts printed in the same table, to the basis point: 474,412 / 2,131,640 = "
    "22.26% and 443,710 / 2,034,858 = 21.81%.\n"
    "  (3) The two ratios being equal is not an artefact but an arithmetic necessity for this bank. NBKI holds "
    "no AT1 and no Tier 2 - the audited accounts' own capital note prints \"Tier 2 capital  -\" for every year "
    "- so CET1 = Tier 1 = Total Capital, and all three ratios must coincide. The audited accounts print all "
    "three ratios as equal too (21.26% / 21.26% / 21.26% for FY2022), just at a different level.\n"
    "  (4) THE SAME EDITION CORROBORATES ITSELF ON A SECOND TABLE. Its section 4.4 Table 5 \"Capital "
    "movement\" (p.18), an own-funds composition table, builds CET1 up from components and then prints three "
    "separate ratio rows - \"Common Equity Tier 1 (as a percentage of total risk exposure amount)\", \"Tier 1 "
    "(...)\" and \"Total capital (...)\" - all three 22.26% for FY2022 and all three 21.81% for FY2021, "
    "against CET1 after regulatory adjustments of 474,412 / 443,710 and the same RWA. Two independent tables, "
    "same figures.\n"
    "  THE COLUMN HEADERS AND THE TABLE CAPTION WERE CHECKED TOO (map rules 18 and 19), because a "
    "misidentified entity block is the other way two adjacent figures come to look like two different ratios. "
    "They rule it out here. This table's two value columns are headed with DATES - \"31/12/22\" and "
    "\"31/12/21\" - not with entity names, so there is no Group-beside-Individual pair to confuse, and the CET1 "
    "Ratio and Total Capital Ratio figures sit on two separately captioned ROWS, not in two columns of one row. "
    "The document is NBKI's own, not a parent's with a subsidiary block in it: its section 1.1 says \"This "
    "document comprises the Pillar 3 disclosures on capital and risk management for NBKI Limited ('NBKI' or "
    "'the Bank') as of 31 December 2022\", section 1.2 identifies \"National Bank of Kuwait International "
    "('NBKI') PLC ... company number 02773743 ... Firm number on the FCA Register is 171532\" - the Banks List "
    "entity exactly - and section 1.1 states the document exists \"to meet the regulatory disclosure "
    "requirements under Part 8 of the UK Capital Requirements Regulation (CRR) ... including the Disclosure "
    "(CRR) part of the PRA Rulebook\". So NBKI discharges its own UK disclosure duty in its own document; the "
    "Kuwaiti parent National Bank of Kuwait S.A.K.P. reports under Central Bank of Kuwait Basel III rules and "
    "publishes no UK KM1 for this subsidiary. The edition's own list of tables runs Tables 1-6 with exactly one "
    "\"Key metrics\" entry, so there is no second, appendix-away printing of the template either (map rule 11).\n"
    "  THE OTHER SIDE WAS RE-READ TOO, from the Bank's own audited accounts rather than from this project's "
    "notes: AR2022 Note 31 \"Capital management (unaudited)\" (printed p.65) gives RWA 2,131,640 / 2,034,858 "
    "with CET1 = Tier 1 = Total capital of 453,162 / 432,220 and ratios 21.26% / 21.24%; AR2021 Note 32 (same "
    "title, printed p.73) gives 432,220 and 21.24% for FY2021 against the same RWA. Those also tie to the "
    "basis point. So BOTH SIDES ARE INTERNALLY CONSISTENT and they differ only in the capital numerator: "
    "US$21,250k for FY2022 and US$11,490k for FY2021.\n"
    "  WHAT THE GAP IS. The Pillar 3's Table 5 shows CET1 before regulatory adjustments of 473,823 (FY2022) "
    "and 447,733 (FY2021) - exactly the total equity on the Bank's own audited balance sheet for those two "
    "dates - and then takes it to 474,412 and 443,710 \"after Regulatory adjustments\". The audited capital "
    "note reaches 453,162 and 432,220 from the same starting equity. The two documents therefore apply "
    "DIFFERENT REGULATORY ADJUSTMENTS to the same audited equity, and the Bank does not reconcile them "
    "anywhere. This project does not reconcile them either, and no figure has been edited so that the two "
    "sides agree.\n"
    "  WHICH SHEET CARRIES WHICH, DELIBERATELY: this KM1 sheet reproduces the PILLAR 3 table, because that is "
    "what a KM1 sheet is for; the single-metric capital and ratio sheets carry the AUDITED ANNUAL REPORT "
    "figures, chosen there (HD-066, 2026-09-06) as audited-adjacent. The verifier reports the four "
    "disagreements every run, and that is the intended outcome - the workbook shows both of the Bank's own "
    "answers side by side rather than quietly picking one. RWA, leverage, LCR and NSFR agree across all "
    "sources for both years, which is itself evidence that only the own-funds definition is in dispute.\n"
    "  A SEPARATE SOURCE DEFECT IN THAT SAME TABLE 5, recorded and not corrected (map rule 7): its FY2022 "
    "column does not foot. 289,403 + 211,714 - 26,277 = 474,840, against a printed \"CET1 capital before "
    "regulatory adjustments\" of 473,823 (the AOCI figure would need to be -27,294 to foot, and -27,294 is "
    "what the audited balance sheet implies). The FY2021 column foots exactly (235,883 + 225,681 - 13,831 = "
    "447,733). Note also that FY2022's \"after regulatory adjustments\" figure is HIGHER than its \"before\" "
    "figure, while FY2021's is lower. None of this is on this sheet - Table 5 is not the KM1 - but it is "
    "recorded because it bears on how much weight the Pillar 3's own-funds numbers can carry.\n\n"
    "FY2023: no FY2023 Pillar 3 edition exists to transcribe. NBKI republishes at a single stable URL rather "
    "than minting a per-year file, the Wayback Machine holds only four captures of it (2023-12-09 = the "
    "FY2021 edition, 2024-02-17 = the FY2022 edition, and two 2025 captures that are text/html error pages), "
    "and the live FY2025 edition carries a single FY2024 comparative only. A domain-wide Wayback CDX "
    "enumeration of nbk.com surfaced two files called \"Pillar III Disclosures 2023.pdf\" and \"Pillar III "
    "Disclosres 2024.pdf\" [sic] - BOTH ARE NBK FRANCE SA, a different legal entity reporting in euros on the "
    "EU KM1 template, and neither may be used here. (Re-checked 2026-09-16: both of those French URLs now "
    "return HTTP 200 with Content-Type text/html - a soft-404 - so they are dead as well as wrong.) See the "
    "RWA Breakdown sheet for the full four-stage verification of this gap.\n\n"
    + ENTITY_NOTE
)

bw.add_km1_sheet(
    title="National Bank of Kuwait (International) Plc — KM1 Key Metrics",
    subtitle="The Bank's own \"Table 3: Key metrics\" from section 4.2 of its Pillar 3 Disclosure, reproduced in "
             "its own row order, labels and precision. The Bank prints this table UNNUMBERED, so no template "
             "row numbers are shown. THE UNIT CHANGES BETWEEN EDITIONS - US$'000 for FY2021-FY2022, £'000 for "
             "FY2024-FY2025 - so every amount row appears TWICE, once per unit, and nothing is converted; ratio "
             "rows stay single. FY2023 is blank because no FY2023 edition exists. The FY2022 edition's own CET1 "
             "capital cells are empty in the source and are left empty here. The CET1 and Total Capital ratios "
             "on this sheet differ from the single-metric ratio sheets for FY2021 and FY2022: that is a real "
             "conflict between the Bank's Pillar 3 and its audited accounts, established from both documents "
             "and explained in full in the source note - neither side has been edited to agree with the other.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=76,
    source_height=460,
)


metric("CET1 Capital", CAPITAL_UNIT, [("Common Equity Tier 1 (CET1) capital", CAPITAL)], CAPITAL_NOTE)
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 capital adequacy ratio", CAPITAL_RATIOS)])
metric("Tier 1 Capital", CAPITAL_UNIT, [("Tier 1 capital", CAPITAL)], CAPITAL_NOTE)
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 capital adequacy ratio", CAPITAL_RATIOS)])
metric("Total Capital", CAPITAL_UNIT, [("Total capital", CAPITAL)], CAPITAL_NOTE)
metric("Total Capital Ratio", "% of RWA", [("Total capital adequacy ratio", CAPITAL_RATIOS)])
metric("Total RWAs", CAPITAL_UNIT, [("Risk-weighted assets", RWAS)])

rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 2449107, "FY2024": 2342000, "FY2022": 2020121, "FY2021": 1929456}),
    ("DATA", "Counterparty credit risk - CCR", {"FY2025": 12096, "FY2024": 11448, "FY2022": 21783, "FY2021": 3162}),
    ("DATA", "Operational risk", {"FY2025": 163201, "FY2024": 150357, "FY2022": 89736, "FY2021": 102240}),
    ("TOTAL", "Total", {"FY2025": 2624404, "FY2024": 2503806, "FY2022": 2131640, "FY2021": 2034858}),
]

bw.add_rwa_breakdown_sheet(
    title="National Bank of Kuwait (International) Plc — RWA Breakdown",
    subtitle="Pillar 3 UK OV1 template. £'000 (FY2024-FY2025) / US$'000 (FY2021-FY2022) - see Currency Note. "
              "FY2023 not publicly disclosed - no FY2023 Pillar 3 document was located.",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources(
        "RWA Breakdown (Table 4: \"Pillar 1 RWA capital requirement\"): FY2025/FY2024 - official Pillar 3 Disclosure "
        "31 December 2025, Table 4, p.17 (same document as the Key Metrics table above). FY2022/FY2021 - the "
        "archived \"December 2023\"-dated document's own Table 4 (Wayback Machine snapshot captured 2024-02-17, "
        "https://web.archive.org/web/20240217111133/https://www.nbk.com/dam/jcr:19757e7d-4d03-40f8-bf39-63c995186e39/"
        "Pillar_III_Disclosures.pdf, p.17), cross-checked against the \"December 2021\"-dated document's own Table 8 "
        "operational risk figure (Wayback Machine snapshot captured 2023-12-09, https://web.archive.org/web/"
        "20231209144740/https://www.nbk.com/dam/jcr:19757e7d-4d03-40f8-bf39-63c995186e39/Pillar_III_Disclosures.pdf, "
        "p.17).\n\n"
        "DATA QUALITY NOTE: the archived document's own published \"Counterparty credit risk - CCR\" row is "
        "internally inconsistent with its own Total RWA figure for both FY2021 and FY2022 - the published figures "
        "($3,162,887k FY2021 [sic; likely a transcription error inserting extra digits into the \"of which "
        "standardised approach\" sub-line] and $14,466,197k FY2022) are 10-2,500x larger than the Bank's own "
        "reported Total RWA, an impossibility since CCR cannot exceed Total RWA. Credit risk and Operational risk "
        "are reproduced exactly as published (both tie consistently between the two archived documents and against "
        "the Key Metrics Total RWA). Counterparty credit risk - CCR is instead shown as the residual needed to "
        "reach the Bank's own disclosed Total RWA (Total RWA minus Credit risk minus Operational risk) rather than "
        "the source document's own unusable CCR figure - FY2021's residual (3,162) exactly matches the document's "
        "own separately-disclosed \"of which credit valuation adjustment - CVA\" sub-line, supporting this as the "
        "correct CCR figure with only the CVA component genuinely present that year; FY2022's residual (21,783) "
        "could not be similarly cross-checked against a clean sub-line and is flagged as a best-available derived "
        "figure, not an independently re-confirmed one.\n\n"
        "FY2023 RE-VERIFICATION (2026-09-12, independent re-check): confirmed still genuinely unobtainable. "
        "The Bank republishes its Pillar 3 PDF at the same stable URL each year rather than a new per-year URL, "
        "so a specific year's vintage survives only if the Wayback Machine happened to crawl it before it was "
        "overwritten - checked the full Wayback CDX capture history for this URL (only 4 captures exist: "
        "2023-12-09 = the FY2021-dated document; 2024-02-17 = the FY2022-dated document; two 2025 captures "
        "returned only a broken text/html page, not a PDF) - no FY2023-dated capture exists, and the live URL "
        "now serves the FY2025 document (confirmed by fetching it directly). Also checked NBKI-Financial-"
        "Statement-2023.pdf (the FY2023 Annual Report/statutory accounts, a separate stable document) Note 31 "
        "'Capital management' - it discloses only the aggregate Risk weighted assets figure ($2,599,821k, which "
        "ties exactly to this workbook's Total RWAs sheet), with no category-level credit/market/operational/"
        "CCR split. No other source was found.\n\n"
        "FY2023 THIRD VERIFICATION (2026-09-15) - AND A WARNING ABOUT THIS DOCUMENT'S COVER DATE. The archived "
        "document referenced above is titled, on its cover and in the running header of every page, 'Pillar 3 "
        "Disclosure / December 2023'. That title is misleading and has already caused this document to be "
        "described inconsistently in these very notes (as both 'the December 2023-dated document' and 'the "
        "FY2022-dated document'). It contains NO FY2023 data whatsoever. Re-downloaded and re-read in full on "
        "2026-09-15, it is a December 2022 disclosure throughout, on three independent pieces of internal "
        "evidence: (1) its Table 3 'Key metrics' column headers read '31/12/22' and '31/12/21' - Total RWA "
        "2,131,640 / 2,034,858, matching this workbook's FY2022/FY2021, not FY2023; (2) its Table 4 'Pillar 1 "
        "RWA capital requirement' column headers read '31 Dec 2022' and '31 Dec 2021'; and (3) its own section "
        "4.1 body text directs the reader to 'the 2022 Annual Report and Consolidated Financial Statements'. "
        "The 'December 2023' on the cover therefore reflects when the Bank posted the file, not the reporting "
        "date of its contents. A future pass finding this document must NOT read its figures as FY2023. FY2023 "
        "remains genuinely unobtainable: the Bank overwrites a single stable URL rather than publishing per-year "
        "files, the Wayback CDX history for that URL was re-queried on 2026-09-15 and still returns exactly four "
        "captures (2023-12-09 PDF, 2024-02-17 PDF = this document, and two 2025 captures that are text/html "
        "error pages, not PDFs), so no FY2023 vintage was ever archived.\n\n"
        "FY2023 FOURTH VERIFICATION (2026-09-15) - DOMAIN-WIDE ENUMERATION, AND A SECOND, MORE DANGEROUS TRAP. "
        "Every prior check queried only the single stable URL, which can fail to find a document but can never "
        "show one does not exist. This pass instead enumerated the WHOLE nbk.com domain via unfiltered Wayback "
        "CDX (40,000 captures), which does settle it. 39 captures match 'pillar'. That sweep DID surface two "
        "per-year Pillar 3 PDFs at previously-unknown AEM asset UUIDs - 'Pillar III Disclosures 2023.pdf' at "
        "jcr:6ed10da3-e2cf-4194-b3b2-eb19e0b4b447 and 'Pillar III Disclosres 2024.pdf' [sic] at "
        "jcr:7ba4c7e4-c705-4d5a-b6a6-2867045845bb - proving the Bank's group CDN does sometimes mint a new UUID "
        "per year rather than overwriting. BOTH WERE DOWNLOADED AND READ, AND NEITHER IS THIS ENTITY'S. They are "
        "NBK FRANCE SA ('NBKF', active in France since 1987, named as such in the 2024 document's Bank Overview), "
        "reported in euros on the EU KM1 template - the 2023 file's own Table EU KM1 shows CET1 220,981 and Total "
        "RWA 689,321 in euros against NBKI's US$533,272k and US$2,599,821k for the same year-end. DO NOT USE "
        "EITHER FILE FOR THIS WORKBOOK. The hazard is that their filenames are entirely generic and carry no hint "
        "of the French entity, so a future domain sweep will surface a file literally called 'Pillar III "
        "Disclosures 2023.pdf' precisely where this workbook's FY2023 hole is - it is the wrong bank. Of the 39 "
        "pillar-matching captures, the only NBKI (London) items are the stable URL cited above and a 2014 file "
        "('NBK-(International)-PLC-Pillar-3-Disclosures-2014.pdf'); every other per-year Pillar 3 on that CDN "
        "belongs to NBK France SA or NBK UAE. The stable URL's own entity was re-confirmed in the same pass by "
        "reading its section 1.2 directly: 'National Bank of Kuwait International (\"NBKI\") PLC, whose registered "
        "office is 13 George Street, London, W1U 3QJ ... company number 02773743 ... Firm number on the FCA "
        "Register is 171532', with Total RWA 2,131,640 / 2,034,858 tying to this workbook's FY2022/FY2021. So the "
        "existing figures are correctly sourced and correctly attributed, and FY2023 has now been shown absent by "
        "enumeration rather than merely not found by probing. Treat this gap as closed."
    ),
    first_col_width=64,
    source_height=340,
    unit_suffix="",
)

ARCHIVED_P3_NOTE = (
    "FY2021 and FY2022 figures on this sheet were recovered 2026-09-03 (ST-027) from two archived NBKI Pillar 3 "
    "disclosures no longer linked from the Bank's current disclosures page - a \"Pillar III Disclosures December "
    "2021\" document (Wayback Machine snapshot of https://www.nbk.com/dam/jcr:19757e7d-4d03-40f8-bf39-63c995186e39/"
    "Pillar_III_Disclosures.pdf captured 2023-12-09, https://web.archive.org/web/20231209144740/"
    "https://www.nbk.com/dam/jcr:19757e7d-4d03-40f8-bf39-63c995186e39/Pillar_III_Disclosures.pdf) and a \"December "
    "2023\"-dated document that (despite its filename) itself only discloses FY2022 with an FY2021 comparative "
    "(Wayback Machine snapshot captured 2024-02-17, https://web.archive.org/web/20240217111133/"
    "https://www.nbk.com/dam/jcr:19757e7d-4d03-40f8-bf39-63c995186e39/Pillar_III_Disclosures.pdf). Both were "
    "previously treated as \"not publicly disclosed\" for FY2021-FY2023 - FY2023 remains genuinely unrecoverable "
    "(no FY2023 Pillar 3 document was located via the live site or the Wayback Machine, and the only file with "
    "\"2023\" in its name resolved to an unrelated NBK entity's disclosure) and stays not publicly disclosed.\n\n"
    "FY2023 RE-VERIFIED AGAIN 2026-09-15 (independent interior-gap sweep; still genuinely not disclosed). Four "
    "checks, all negative:\n"
    "1. The live NBKI Pillar 3 document at the Bank's stable URL was re-downloaded and is the 31 December 2025 "
    "edition; its Table 3 'Key metrics' (p.16) has exactly TWO columns, 31 Dec 2025 and 31 Dec 2024. There is "
    "no FY2023 comparative to recover, so the usual \"read the next year's comparative column\" route is closed "
    "for this bank - NBKI's KM1-equivalent never carries more than one prior year.\n"
    "2. A Wayback CDX scan across the whole nbk.com domain for any URL containing \"pillar\" returned the same "
    "four captures of NBKI's own stable URL already documented above, and nothing else NBKI-related.\n"
    "3. That scan DID surface two nbk.com documents whose filenames look promising - "
    "https://www.nbk.com/dam/jcr:6ed10da3-e2cf-4194-b3b2-eb19e0b4b447/Pillar-III-Disclosures-2023.pdf and "
    "https://www.nbk.com/dam/jcr:7ba4c7e4-c705-4d5a-b6a6-2867045845bb/Pillar%20III%20Disclosres%202024.pdf "
    "(the second filename's typo is the Bank's own). Both were downloaded live and read: both are NBK FRANCE SA "
    "(\"NBKF\") reports, a different legal entity in a different jurisdiction (\"NBK France SA ('NBKF') has been "
    "active in France since 1987... the National Bank of Kuwait Group selected France as its preferred Member "
    "State\"). This pins down the earlier note's vague \"an unrelated NBK entity\" to the exact entity and the "
    "exact two URLs, so a future session does not have to re-open them. Using either would be a cross-entity "
    "substitution and is not done.\n"
    "4. The FY2023 statutory accounts (NBKI-Financial-Statement-2023.pdf) were re-read: Note 28.2 'Liquidity "
    "Risk' is a contractual-maturity table only, and neither the term LCR/NSFR nor any leverage ratio appears "
    "anywhere in that document (nor in the FY2024 accounts).\n"
    "Conclusion unchanged: NBKI's FY2023 Leverage Ratio, LCR and NSFR are genuinely not publicly disclosed."
)

metric(
    "Leverage Ratio",
    "£000 / $000 / %",
    [
        ("Total exposure measure excluding claims on central banks", {"FY2025": 4062395, "FY2024": 4133905, "FY2022": 3625281, "FY2021": 3482137}),
        ("Leverage ratio excluding claims on central banks", {"FY2025": "13.21%", "FY2024": "12.13%", "FY2022": "13.09%", "FY2021": "12.74%"}),
    ],
    "FY2023: not publicly disclosed - see note below. FY2024-FY2025 are £000, from the official Pillar 3 Table 3, "
    "p.16. FY2021-FY2022 are US$000, from archived Pillar 3 disclosures - see note below.\n\n" + ARCHIVED_P3_NOTE,
)

metric(
    "LCR",
    "£000 / $000 / %",
    [
        ("Total HQLA (weighted value average)", {"FY2025": 731707, "FY2024": 925985, "FY2022": 659703, "FY2021": 702588}),
        ("Total net cash outflows (adjusted value)", {"FY2025": 147299, "FY2024": 215454, "FY2022": 220185, "FY2021": 209655}),
        ("Liquidity Coverage Ratio (adjusted value)", {"FY2025": "497%", "FY2024": "430%", "FY2022": "300%", "FY2021": "227%"}),
    ],
    "FY2023: not publicly disclosed - see note below. FY2024-FY2025 are £000, from the official Pillar 3 Table 3, "
    "p.16. FY2021-FY2022 are US$000, from archived Pillar 3 disclosures - see note below.\n\n" + ARCHIVED_P3_NOTE,
)

metric(
    "NSFR",
    "%",
    [("Net Stable Funding Ratio", {"FY2025": "120%", "FY2024": "127%", "FY2022": "127%", "FY2021": "114%"})],
    "FY2023: not publicly disclosed - see note below. FY2024-FY2025 are from the official Pillar 3 Table 3, p.16. "
    "FY2021-FY2022 are from archived Pillar 3 disclosures - see note below. FY2022's NSFR (127%) and FY2024's "
    "NSFR (127%) are coincidentally identical values from two different years/documents.\n\n" + ARCHIVED_P3_NOTE,
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources("No MREL ratio or MREL requirement was numerically disclosed in the reviewed entity-level documents."),
    per_note={"MREL Ratio": "No MREL ratio or requirement was located in the FY2021–FY2025 annual reports or the official Pillar 3 disclosure."},
)

def bs_value(label):
    return next(v for kind, name, v in bs_rows if name == label)


def pl_value(label):
    return next(v for kind, name, v in pl_rows if name == label)


equity_summary = {
    "FY2025": {"Opening equity": 501978, "Total comprehensive income for the year": 35220, "Other equity movements, net": 0, "Closing equity": 537198},
    "FY2024": {"Opening equity": 419962, "Total comprehensive income for the year": 32016, "Other equity movements, net": 50000, "Closing equity": 501978},
    "FY2023": {"Opening equity": 473823, "Total comprehensive income for the year": 59906, "Other equity movements, net": 0, "Closing equity": 533729},
    "FY2022": {"Opening equity": 447733, "Total comprehensive income for the year": -27430, "Other equity movements, net": 53520, "Closing equity": 473823},
}

bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit=None,
    balance_sheet_totals=[(label, bs_value(label)) for label in [
        "Total assets",
        "Loans and advances to customers",
        "Customer deposits",
        "Total equity",
    ]],
    balance_sheet_unit="As reported: £'000 (FY2024-FY2025); US$'000 (FY2021-FY2023)",
    income_statement_totals=[(label, pl_value(label)) for label in [
        "Net operating income before ECL",
        "Operating expenses",
        "Profit for the year before taxation",
        "Profit for the year",
    ]],
    income_statement_unit="As reported: £'000 (FY2024-FY2025); US$'000 (FY2021-FY2023)",
    equity_changes_totals=[
        (label, {y: equity_summary[y].get(label) for y in ["FY2025", "FY2024", "FY2023", "FY2022"]})
        for label in ["Opening equity", "Total comprehensive income for the year", "Other equity movements, net", "Closing equity"]
    ],
    equity_changes_unit="As reported: £'000 (FY2024-FY2025); US$'000 (FY2022-FY2023) - FY2024's Opening equity is the "
                         "FY2023 closing balance retranslated to £'000, see Currency Note",
    ratios=[
        ("CET1 Ratio", CAPITAL_RATIOS),
        ("Tier 1 Ratio", CAPITAL_RATIOS),
        ("Total Capital Ratio", CAPITAL_RATIOS),
        ("Leverage Ratio", {"FY2025": "13.21%", "FY2024": "12.13%", "FY2022": "13.09%", "FY2021": "12.74%"}),
        ("LCR", {"FY2025": "497%", "FY2024": "430%", "FY2022": "300%", "FY2021": "227%"}),
        ("NSFR", {"FY2025": "120%", "FY2024": "127%", "FY2022": "127%", "FY2021": "114%"}),
    ],
    note=(
        "No Statement of Cash Flows is published (FRS 101 exemption) - cash-flow block omitted. Balance Sheet/"
        "Profit & Loss/Equity Changes cover FY2021-FY2025 (entity basis, currency changes from US$ to £ between "
        "FY2023 and FY2024 - see Currency Note on the statement sheets); the Equity Changes summary above starts "
        "at FY2022 to keep the chart's year-over-year figures in a consistent, comparable shape. Leverage, LCR, "
        "and NSFR now cover FY2021-FY2022 and FY2024-FY2025 (FY2021/FY2022 recovered 2026-09-03 (ST-027) from "
        "archived Pillar 3 disclosures - see the Leverage Ratio sheet's note); FY2023 remains not publicly "
        "disclosed for these three ratios and for RWA Breakdown."
    ),
)

bw.save("/Users/armaan/code/katalysis/banks/NATIONAL BANK OF KUWAIT INTERNATIONAL FINANCIALS.xlsx")
