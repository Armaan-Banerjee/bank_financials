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
        "FY2025": "capital management p.75",
        "FY2024": "capital management p.76",
        "FY2023": "capital management p.72",
        "FY2022": "capital management p.64",
        "FY2021": "capital management p.72",
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
    ("DATA", "Investment securities", {"FY2025": 550717, "FY2024": 398439, "FY2023": 357952, "FY2022": 264917, "FY2021": 213944}),
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
              "FY2024 rather than zero. Repurchase agreements is a new FY2025 line (not previously used).",
    rows=bs_rows, sources_text=STATEMENTS_SOURCES, first_col_width=68, source_height=340, unit_suffix="",
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
    ("DATA", "Change in fair value of debt securities measured at FVOCI (net of tax)", {"FY2025": 894, "FY2024": -830}),
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
    rows=pl_rows, sources_text=STATEMENTS_SOURCES, first_col_width=82, source_height=340, unit_suffix="",
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
    "reported in GBP£000 following the presentation-currency change. No conversion has been imposed."
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
        "figure, not an independently re-confirmed one."
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
    "\"2023\" in its name resolved to an unrelated NBK entity's disclosure) and stays not publicly disclosed."
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
