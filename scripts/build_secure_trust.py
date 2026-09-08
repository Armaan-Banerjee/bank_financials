import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017"]
AR_URLS = {
    "FY2025": "https://www.securetrustbank.com/investor-relations/document-library/reports-and-accounts-2025-final-483796420288",
    "FY2024": "https://www.securetrustbank.com/investor-relations/document-library/reports-and-accounts-2024-final",
    "FY2023": "https://www.securetrustbank.com/investor-relations/document-library/reports-and-accounts-2023-final",
    "FY2022": "https://www.securetrustbank.com/investor-relations/document-library/reports-and-accounts-2022-final",
    "FY2021": "https://www.securetrustbank.com/investor-relations/document-library/reports-and-accounts-2021-final",
    "FY2020": "https://www.securetrustbank.com/investor-relations/document-library/reports-and-accounts-2020-final",
    "FY2019": "https://www.securetrustbank.com/investor-relations/document-library/reports-and-accounts-2019-final",
    "FY2018": "https://www.securetrustbank.com/investor-relations/document-library/reports-and-accounts-2018-final",
    "FY2017": "https://www.securetrustbank.com/investor-relations/document-library/reports-and-accounts-2017-final",
}
P3_URLS = {
    y: f"https://www.securetrustbank.com/investor-relations/document-library/pillar-3-disclosure-{y[-4:]}-final"
    for y in YEARS
}
INTERIM_URLS = {
    "H1 2025": "https://www.securetrustbank.com/investor-relations/document-library/pillar-3-disclosure-2025-interim",
    "H1 2024": "https://www.securetrustbank.com/investor-relations/document-library/pillar-3-disclosure-2024-interim",
    "H1 2023": "https://www.securetrustbank.com/investor-relations/document-library/pillar-3-disclosure-2023-interim",
    "H1 2022": "https://www.securetrustbank.com/investor-relations/document-library/pillar-3-disclosure-2022-interim",
}

ENTITY_NOTE = (
    "ENTITY / BASIS NOTE: Secure Trust Bank Public Limited Company (Companies House 00541132; FRN 204550; "
    "LEI 213800CXIBLC2TMIGI76) is the exact legal entity in the supplied bank list and the PRA register. "
    "The cash-flow statement uses the consolidated Group column, matching the Group-basis Pillar 3 disclosures; "
    "the annual reports also contain Company statements, but Company cash flows are not substituted. Secure Trust "
    "Bank PLC is the current legal name. FY2021 is taken from the restated comparative column in the FY2022 report, "
    "which restates prior-year cash and cash equivalents from £303.0m to £306.7m. Figures are £million as reported. "
    "FY2020-FY2017 historical statements are available in the Bank's official archive (the 2020 report includes a "
    "five-year summary for 2020-2016); blank cells are retained where a line was not separately presented."
)

CASH_SOURCES = "Sources - Secure Trust Bank PLC consolidated Group cash flows, £million:\n" + "\n".join(
    f"{y}: Secure Trust Bank PLC Annual Report & Accounts {y[-4:]}, consolidated statement of cash flows, "
    f"official report - {AR_URLS[y]}"
    for y in YEARS
) + "\n\n" + ENTITY_NOTE

P3_SOURCES = "Sources - Secure Trust Bank PLC Group regulatory disclosures:\n" + "\n".join(
    f"{y}: Secure Trust Bank PLC Pillar 3 disclosure for the year ended 31 December {y[-4:]}, Key metrics table, "
    f"p. 5 (2021 p. 4) - {P3_URLS[y]}"
    for y in YEARS
) + "\n\n" + ENTITY_NOTE + " Regulatory figures are Group figures and are not substituted into Company cash flows."

bw = BankWorkbook("Secure Trust Bank Public Limited Company", YEARS, header_color="1F4E79")

AR2025_URL = AR_URLS["FY2025"]
AR2024_URL = AR_URLS["FY2024"]
AR2023_URL = AR_URLS["FY2023"]
AR2022_URL = AR_URLS["FY2022"]
AR2021_URL = AR_URLS["FY2021"]

BS_SOURCES = (
    "Sources - Secure Trust Bank PLC consolidated Group statement of financial position, £million:\n"
    f"FY2025: Annual Report & Accounts 2025, Consolidated and Company statement of financial position, p.147 - {AR2025_URL}\n"
    f"FY2024: Annual Report & Accounts 2024, Consolidated and Company statement of financial position, p.131 - {AR2024_URL}\n"
    f"FY2023: Annual Report & Accounts 2023, Consolidated statement of financial position, p.115 - {AR2023_URL}\n"
    f"FY2022: Annual Report & Accounts 2022, Consolidated statement of financial position, p.121 (each year's own originally-published figures, not later restated comparatives) - {AR2022_URL}\n"
    f"FY2021: Annual Report & Accounts 2021, Consolidated statement of financial position, p.109 - {AR2021_URL}\n\n"
    + ENTITY_NOTE
    + " Group basis throughout (Company figures are near-identical but not substituted). FY2023's own report restated the FY2022 comparative for a land & buildings "
    "accounting policy change (historical cost, not revaluation); the FY2022 column above uses AR2022's own originally-published figures, not that restated "
    "comparative - see the Statement of Changes in Equity sheet for the resulting 0.5m reconciling break. FY2025's Balance Sheet reflects the Consumer Finance "
    "business (Vehicle Finance) being reclassified to \"Assets held for sale\" - not present as a separate held-for-sale line in earlier years. "
    "Debt securities' composition comes from each year's own Note 14 'Debt securities': FY2025 (p.211, note 14) states the balance \"consisted "
    "solely of sterling UK Government securities ('gilts')\", held at amortised cost with intent to hold to collect; FY2021 (p.169, note 14), "
    "FY2018 (p.115, note 14) and FY2020's report (p.169, note 13, giving the FY2019 comparative) each state the balance \"consist(s) solely of "
    "sterling UK Government Treasury Bills ('T-Bills')\", also held to collect at amortised cost. Every disclosed year is thus 100% UK Government "
    "paper at amortised cost, with no FVOCI/FVTPL leg (\"The Group currently has no financial instruments classified as FVOCI\" per each year's "
    "own Note 1/2 accounting policy) - not a genuine two-way split, so no separate 'other'/mark-to-market row is added alongside it."
)

BS_ROWS = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and Bank of England reserve account", {"FY2025": 528.1, "FY2024": 445.0, "FY2023": 351.6, "FY2022": 370.1, "FY2021": 235.7, "FY2020": 181.5, "FY2019": 105.8, "FY2018": 169.7, "FY2017": 226.1}),
    ("DATA", "Loans and advances to banks", {"FY2025": 36.8, "FY2024": 24.0, "FY2023": 53.7, "FY2022": 50.5, "FY2021": 50.3, "FY2020": 63.3, "FY2019": 48.4, "FY2018": 44.8, "FY2017": 34.3}),
    ("DATA", "Debt securities - UK Government Treasury Bills/gilts (amortised cost)", {"FY2025": 1.0, "FY2021": 25.0, "FY2020": 0.0, "FY2019": 25.0, "FY2018": 149.7, "FY2017": 5.0}),
    ("DATA", "Loans and advances to customers", {"FY2025": 3295.8, "FY2024": 3608.5, "FY2023": 3315.3, "FY2022": 2919.5, "FY2021": 2530.6, "FY2020": 2358.9, "FY2019": 2450.1, "FY2018": 2028.9, "FY2017": 1598.3}),
    ("DATA", "Fair value adjustment for portfolio hedged risk", {"FY2025": 7.3, "FY2024": -6.8, "FY2023": -3.9, "FY2022": -32.0, "FY2021": -3.5, "FY2020": 5.7, "FY2019": -0.9, "FY2018": 0.0, "FY2017": 0.0}),
    ("DATA", "Derivative financial instruments", {"FY2025": 0.2, "FY2024": 14.3, "FY2023": 25.5, "FY2022": 34.9, "FY2021": 3.8, "FY2020": 4.8, "FY2019": 0.9, "FY2018": 0.0, "FY2017": 0.0}),
    ("DATA", "Assets held for sale", {"FY2025": 390.8, "FY2021": 1.3}),
    ("DATA", "Investment property", {"FY2025": 24.1, "FY2021": 4.7}),
    ("DATA", "Property, plant and equipment", {"FY2025": 7.4, "FY2024": 9.9, "FY2023": 10.8, "FY2022": 10.3, "FY2021": 9.3}),
    ("DATA", "Right-of-use assets", {"FY2025": 4.4, "FY2024": 1.6, "FY2023": 1.8, "FY2022": 1.5, "FY2021": 2.2}),
    ("DATA", "Intangible assets", {"FY2025": 5.1, "FY2024": 5.0, "FY2023": 5.9, "FY2022": 6.6, "FY2021": 6.9}),
    ("DATA", "Current tax assets", {"FY2025": 2.6, "FY2024": 0.2, "FY2023": 0.1, "FY2022": None, "FY2021": 0.8}),
    ("DATA", "Deferred tax assets", {"FY2025": 3.6, "FY2024": 3.3, "FY2023": 4.3, "FY2022": 5.5, "FY2021": 6.9}),
    ("DATA", "Other assets", {"FY2025": 8.8, "FY2024": 11.7, "FY2023": 12.9, "FY2022": 13.4, "FY2021": 11.9, "FY2020": 49.9, "FY2019": 53.5, "FY2018": 51.2, "FY2017": 27.9}),
    ("TOTAL", "Total assets", {"FY2025": 4316.0, "FY2024": 4116.7, "FY2023": 3778.0, "FY2022": 3380.3, "FY2021": 2885.9, "FY2020": 2664.1, "FY2019": 2682.8, "FY2018": 2444.3, "FY2017": 1891.6}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Due to banks", {"FY2025": 205.9, "FY2024": 365.8, "FY2023": 402.0, "FY2022": 400.5, "FY2021": 390.8, "FY2020": 276.4, "FY2019": 308.5, "FY2018": 263.5, "FY2017": 113.0}),
    ("DATA", "Deposits from customers", {"FY2025": 3509.6, "FY2024": 3244.9, "FY2023": 2871.8, "FY2022": 2514.6, "FY2021": 2103.2, "FY2020": 1992.5, "FY2019": 2020.3, "FY2018": 1847.7, "FY2017": 1483.2}),
    ("DATA", "Fair value adjustment for portfolio hedged risk", {"FY2025": 4.7, "FY2024": -3.4, "FY2023": -1.4, "FY2022": -23.0, "FY2021": -5.3, "FY2020": 4.7, "FY2019": -0.7, "FY2018": 0.0, "FY2017": 0.0}),
    ("DATA", "Derivative financial instruments", {"FY2025": 0.1, "FY2024": 10.0, "FY2023": 22.0, "FY2022": 26.7, "FY2021": 6.2, "FY2020": 6.1, "FY2019": 0.6, "FY2018": 0.0, "FY2017": 0.0}),
    ("DATA", "Liabilities directly associated with assets held for sale", {"FY2021": 2.0}),
    ("DATA", "Current tax liabilities", {"FY2022": 0.8}),
    ("DATA", "Lease liabilities", {"FY2025": 4.4, "FY2024": 1.8, "FY2023": 2.3, "FY2022": 2.1, "FY2021": 3.1}),
    ("DATA", "Other liabilities", {"FY2025": 98.0, "FY2024": 32.5, "FY2023": 37.7, "FY2022": 78.1, "FY2021": 31.3, "FY2020": 63.1, "FY2019": 49.4, "FY2018": 45.6, "FY2017": 46.3}),
    ("DATA", "Provisions for liabilities and charges", {"FY2025": 25.5, "FY2024": 11.3, "FY2023": 6.0, "FY2022": 2.5, "FY2021": 1.3}),
    ("DATA", "Subordinated liabilities", {"FY2025": 93.5, "FY2024": 93.3, "FY2023": 93.1, "FY2022": 51.1, "FY2021": 50.9, "FY2020": 50.8, "FY2019": 50.6, "FY2018": 50.4, "FY2017": 0.0}),
    ("TOTAL", "Total liabilities", {"FY2025": 3941.7, "FY2024": 3756.2, "FY2023": 3433.5, "FY2022": 3053.4, "FY2021": 2583.5, "FY2020": 2393.6, "FY2019": 2428.7, "FY2018": 2207.2, "FY2017": 1642.5}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 7.6, "FY2024": 7.6, "FY2023": 7.6, "FY2022": 7.5, "FY2021": 7.5}),
    ("DATA", "Share premium", {"FY2025": 84.2, "FY2024": 84.0, "FY2023": 83.8, "FY2022": 82.2, "FY2021": 82.2}),
    ("DATA", "Other reserves", {"FY2025": -1.9, "FY2024": -2.2, "FY2023": -1.7, "FY2022": -0.3, "FY2021": 1.0}),
    ("DATA", "Retained earnings", {"FY2025": 284.4, "FY2024": 271.1, "FY2023": 254.8, "FY2022": 237.5, "FY2021": 211.7}),
    ("TOTAL", "Total equity", {"FY2025": 374.3, "FY2024": 360.5, "FY2023": 344.5, "FY2022": 326.9, "FY2021": 302.4, "FY2020": 270.5, "FY2019": 254.1, "FY2018": 237.1, "FY2017": 249.1}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 4316.0, "FY2024": 4116.7, "FY2023": 3778.0, "FY2022": 3380.3, "FY2021": 2885.9, "FY2020": 2664.1, "FY2019": 2682.8, "FY2018": 2444.3, "FY2017": 1891.6}),
]

bw.add_balance_sheet_sheet(
    "Secure Trust Bank PLC - Group Balance Sheet",
    "Consolidated Group basis, £million; each year uses that year's own originally-published figures, not later restated comparatives.",
    BS_ROWS, BS_SOURCES, first_col_width=62, source_height=340, unit_suffix=" (£m)",
)

IS_SOURCES = (
    "Sources - Secure Trust Bank PLC consolidated Group statement of comprehensive income, £million:\n"
    f"FY2025: Annual Report & Accounts 2025, Consolidated statement of comprehensive income, p.146 - {AR2025_URL}\n"
    f"FY2024: Annual Report & Accounts 2024, Consolidated statement of comprehensive income, p.130 - {AR2024_URL}\n"
    f"FY2023: Annual Report & Accounts 2023, Consolidated statement of comprehensive income, p.114 - {AR2023_URL}\n"
    f"FY2022: Annual Report & Accounts 2022, Consolidated statement of comprehensive income, p.120 - {AR2022_URL}\n"
    f"FY2021: Annual Report & Accounts 2021, Consolidated statement of comprehensive income, p.108 - {AR2021_URL}\n\n"
    + ENTITY_NOTE
    + " Each year uses that year's own originally-published continuing/discontinued split, not a later restated comparative. FY2022's Consumer Finance "
    "(Debt Managers) business and FY2023's Vehicle Finance disposal each produced small discontinued-operations results in their own year; FY2025's own report "
    "shows a much larger discontinued-operations loss as the Vehicle Finance book was reclassified as held for sale. AR2025's own restated FY2024 comparative "
    "splits FY2024 into continuing/discontinued to match, but AR2024's own originally-published FY2024 figures (used here) show no discontinued operations at "
    "all for that year - both report the same £19.7m profit for the year, only the continuing/discontinued split differs. FY2021 has no discontinued operations "
    "at all (\"All comprehensive income relates to continuing operations\")."
)

IS_ROWS = [
    ("SECTION", "Income - continuing operations", {}),
    ("DATA", "Interest income and similar income", {"FY2025": 301.8, "FY2024": 366.0, "FY2023": 304.0, "FY2022": 203.0, "FY2021": 180.0, "FY2020": 192.5, "FY2019": 191.4, "FY2018": 169.2, "FY2017": 149.3}),
    ("DATA", "Interest expense and similar charges", {"FY2025": -150.7, "FY2024": -181.1, "FY2023": -136.5, "FY2022": -50.4, "FY2021": -29.2, "FY2020": -41.6, "FY2019": -46.0, "FY2018": -35.5, "FY2017": -26.7}),
    ("TOTAL", "Net interest income", {"FY2025": 151.1, "FY2024": 184.9, "FY2023": 167.5, "FY2022": 152.6, "FY2021": 150.8, "FY2020": 150.9, "FY2019": 145.4, "FY2018": 133.7, "FY2017": 122.6}),
    ("DATA", "Fee and commission income", {"FY2025": 14.1, "FY2024": 19.2, "FY2023": 17.3, "FY2022": 17.4, "FY2021": 14.3}),
    ("DATA", "Fee and commission expense", {"FY2025": 0.0, "FY2024": -0.2, "FY2023": -0.1, "FY2022": -0.4, "FY2021": -0.6}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 14.1, "FY2024": 19.0, "FY2023": 17.2, "FY2022": 17.0, "FY2021": 13.7, "FY2020": 15.2, "FY2019": 20.1, "FY2018": 17.9, "FY2017": 14.9}),
    ("TOTAL", "Operating income", {"FY2025": 165.2, "FY2024": 203.9, "FY2023": 184.7, "FY2022": 169.6, "FY2021": 164.5, "FY2020": 166.1, "FY2019": 165.5, "FY2018": 151.6, "FY2017": 137.5}),
    ("DATA", "Net impairment charge on loans and advances to customers", {"FY2025": -31.4, "FY2024": -61.9, "FY2023": -43.2, "FY2022": -38.2, "FY2021": -4.5, "FY2020": -51.3, "FY2019": -32.6, "FY2018": -32.4, "FY2017": -36.9}),
    ("DATA", "Gains on modification of financial assets", {"FY2023": 0.3, "FY2022": 1.1, "FY2021": 1.5}),
    ("DATA", "Other gains/(losses)", {"FY2025": 0.1, "FY2024": -0.3}),
    ("DATA", "Fair value gains/(losses) on financial instruments", {"FY2025": 0.1, "FY2024": 1.2, "FY2023": 0.5, "FY2022": -0.3, "FY2021": -0.1}),
    ("DATA", "Loss on disposal of loan books", {"FY2021": -1.4}),
    ("DATA", "Losses from derivatives and hedge accounting", {"FY2021": -0.1}),
    ("TOTAL", "Operating expenses", {"FY2025": -74.7, "FY2024": -103.8, "FY2023": -99.7, "FY2022": -93.2, "FY2021": -104.0, "FY2020": -91.6, "FY2019": -94.2, "FY2018": -84.5, "FY2017": -71.6}),
    ("TOTAL", "Profit before income tax from continuing operations before exceptional items", {"FY2025": 59.3, "FY2024": 39.1, "FY2023": 42.6, "FY2022": 39.0, "FY2021": 56.0, "FY2020": 20.1, "FY2019": 38.7, "FY2018": 34.7, "FY2017": 29.3}),
    ("DATA", "Exceptional items", {"FY2025": 0.0, "FY2024": -9.9, "FY2023": -6.5}),
    ("TOTAL", "Profit before income tax from continuing operations", {"FY2025": 59.3, "FY2024": 29.2, "FY2023": 36.1, "FY2022": 39.0, "FY2021": 56.0, "FY2020": 20.1, "FY2019": 38.7, "FY2018": 34.7, "FY2017": 29.3}),
    ("DATA", "Income tax (expense)/credit", {"FY2025": -14.7, "FY2024": -9.5, "FY2023": -9.7, "FY2022": -9.4, "FY2021": -10.4}),
    ("TOTAL", "Profit for the year from continuing operations", {"FY2025": 44.6, "FY2024": 19.7, "FY2023": 26.4, "FY2022": 29.6, "FY2021": 45.6}),
    ("SECTION", "Discontinued operations", {}),
    ("DATA", "Profit/(loss) before income tax from discontinued operations", {"FY2025": -31.8, "FY2023": -2.7, "FY2022": 5.0}),
    ("DATA", "Income tax (expense)/credit from discontinued operations", {"FY2025": 4.8, "FY2023": 0.6, "FY2022": -0.9}),
    ("TOTAL", "Profit/(loss) for the year from discontinued operations", {"FY2025": -27.0, "FY2023": -2.1, "FY2022": 4.1}),
    ("TOTAL", "Profit for the year", {"FY2025": 17.6, "FY2024": 19.7, "FY2023": 24.3, "FY2022": 33.7, "FY2021": 45.6}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Cash flow hedge reserve movements, net of tax", {"FY2025": 0.0, "FY2024": 0.3, "FY2023": 0.5, "FY2022": -0.5, "FY2021": -0.3}),
    ("DATA", "Revaluation reserve movements, net of tax", {"FY2022": 0.3, "FY2021": 0.4}),
    ("TOTAL", "Other comprehensive income for the year, net of income tax", {"FY2025": 0.0, "FY2024": 0.3, "FY2023": 0.5, "FY2022": -0.2, "FY2021": 0.1}),
    ("TOTAL", "Total comprehensive income for the year", {"FY2025": 17.6, "FY2024": 20.0, "FY2023": 24.8, "FY2022": 33.5, "FY2021": 45.7}),
]

bw.add_income_statement_sheet(
    "Secure Trust Bank PLC - Group Profit & Loss",
    "Consolidated Group basis, £million; each year uses that year's own originally-published continuing/discontinued split.",
    IS_ROWS, IS_SOURCES, first_col_width=68, source_height=280, unit_suffix=" (£m)",
)

EQ_SOURCES = (
    "Sources - Secure Trust Bank PLC consolidated Group statement of changes in equity, £million:\n"
    f"1 Jan 2021 opening & FY2021 movements: Annual Report & Accounts 2021, Consolidated statement of changes in equity, p.111 - {AR2021_URL}\n"
    f"FY2022 movements (own, unrestated): Annual Report & Accounts 2022, Consolidated statement of changes in equity, p.123 - {AR2022_URL}\n"
    f"FY2023 movements: Annual Report & Accounts 2023, Consolidated statement of changes in equity, p.117 - {AR2023_URL}\n"
    f"FY2024 movements: Annual Report & Accounts 2024, Consolidated and Company statement of changes in equity, p.132 - {AR2024_URL}\n"
    f"FY2025 movements: Annual Report & Accounts 2025, Consolidated and Company statement of changes in equity, p.148 - {AR2025_URL}\n\n"
    + ENTITY_NOTE
    + " GENUINE RECONCILING BREAK, NOT A PLUG ROW: AR2023's own report restated the 1 January 2022 opening balance for a change in accounting policy (land & "
    "buildings now held at historical cost rather than revalued - see Note 1.3 of the 2023 Annual Report), which also eliminates the Revaluation reserve from "
    "31 December 2022 onward. FY2022's closing balance shown below (£326.9m) is AR2022's own originally-published figure; a labelled 'Restatement' row then "
    "bridges to AR2023's own restated 1 January 2023 opening (£326.4m) that FY2023's own movements roll forward from - both figures are transcribed exactly as "
    "each report presented them, not blended or forced to tie. The 'Own shares' reserve column was introduced from the FY2022 statement onward (no equivalent "
    "in the FY2021 statement); the 'Revaluation reserve' column was eliminated by the same FY2023 restatement and does not reappear in the FY2024/FY2025 "
    "statements, which show only a Cash flow hedge reserve and Own shares under 'Other reserves'."
)

EQ_HEADERS = ["Share capital", "Share premium", "Cash flow hedge reserve", "Revaluation reserve", "Own shares", "Retained earnings", "Total equity"]

EQ_ROWS = [
    ("TOTAL", "Balance at 1 January 2021", (7.5, 82.2, 0.0, 0.9, None, 177.0, 267.6)),
    ("DATA", "Profit for 2021", (None, None, None, None, None, 45.6, 45.6)),
    ("DATA", "Cash flow hedge reserve movements", (None, None, -0.4, None, None, None, -0.4)),
    ("DATA", "Tax on cash flow hedge reserve movements", (None, None, 0.1, None, None, None, 0.1)),
    ("DATA", "Revaluation reserve movements", (None, None, None, 0.5, None, None, 0.5)),
    ("DATA", "Tax on revaluation reserve movements", (None, None, None, -0.1, None, None, -0.1)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, -0.3, 0.4, None, 45.6, 45.7)),
    ("DATA", "Dividends", (None, None, None, None, None, -11.9, -11.9)),
    ("DATA", "Share-based payments", (None, None, None, None, None, 1.0, 1.0)),
    ("TOTAL", "Balance at 31 December 2021", (7.5, 82.2, -0.3, 1.3, None, 211.7, 302.4)),
    ("DATA", "Profit for 2022", (None, None, None, None, None, 33.7, 33.7)),
    ("DATA", "Cash flow hedge reserve movements", (None, None, -0.7, None, None, None, -0.7)),
    ("DATA", "Tax on cash flow hedge reserve movements", (None, None, 0.2, None, None, None, 0.2)),
    ("DATA", "Revaluation during the year", (None, None, None, 0.1, None, None, 0.1)),
    ("DATA", "Revaluation transfer to retained earnings", (None, None, None, -0.8, None, 0.8, 0.0)),
    ("DATA", "Tax on revaluation reserve movements", (None, None, None, 0.2, None, None, 0.2)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, -0.5, -0.5, None, 34.5, 33.5)),
    ("DATA", "Purchase of own shares", (None, None, None, None, -0.3, None, -0.3)),
    ("DATA", "Dividends", (None, None, None, None, None, -10.7, -10.7)),
    ("DATA", "Share-based payments", (None, None, None, None, None, 2.0, 2.0)),
    ("TOTAL", "Balance at 31 December 2022 (own, AR2022, unrestated)", (7.5, 82.2, -0.8, 0.8, -0.3, 237.5, 326.9)),
    ("DATA", "Restatement: land & buildings accounting policy change, net of tax (per AR2023 Note 1.3)", (None, None, None, -0.8, None, 0.3, -0.5)),
    ("TOTAL", "Balance at 1 January 2023 (restated, per AR2023)", (7.5, 82.2, -0.8, 0.0, -0.3, 237.8, 326.4)),
    ("DATA", "Profit for 2023", (None, None, None, None, None, 24.3, 24.3)),
    ("DATA", "Cash flow hedge reserve movements", (None, None, 0.6, None, None, None, 0.6)),
    ("DATA", "Tax on cash flow hedge reserve movements", (None, None, -0.1, None, None, None, -0.1)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, 0.5, None, None, 24.3, 24.8)),
    ("DATA", "Purchase of own shares", (None, None, None, None, -1.2, None, -1.2)),
    ("DATA", "Sale of own shares", (None, None, None, None, 0.1, None, 0.1)),
    ("DATA", "Issue of shares", (0.1, 1.6, None, None, None, None, 1.7)),
    ("DATA", "Dividends", (None, None, None, None, None, -8.4, -8.4)),
    ("DATA", "Share-based payments", (None, None, None, None, None, 1.1, 1.1)),
    ("TOTAL", "Balance at 31 December 2023", (7.6, 83.8, -0.3, 0.0, -1.4, 254.8, 344.5)),
    ("DATA", "Profit for 2024", (None, None, None, None, None, 19.7, 19.7)),
    ("DATA", "Other comprehensive income, net of income tax", (None, None, 0.3, None, None, None, 0.3)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, 0.3, None, None, 19.7, 20.0)),
    ("DATA", "Purchase of own shares", (None, None, None, None, -1.4, None, -1.4)),
    ("DATA", "Sale of own shares", (None, None, None, None, 0.6, None, 0.6)),
    ("DATA", "Loss on sale of own shares", (None, None, None, None, None, -0.5, -0.5)),
    ("DATA", "Issue of shares", (None, 0.2, None, None, None, None, 0.2)),
    ("DATA", "Dividends paid", (None, None, None, None, None, -5.2, -5.2)),
    ("DATA", "Share-based payments", (None, None, None, None, None, 2.3, 2.3)),
    ("TOTAL", "Balance at 31 December 2024", (7.6, 84.0, 0.0, None, -2.2, 271.1, 360.5)),
    ("DATA", "Profit for 2025", (None, None, None, None, None, 17.6, 17.6)),
    ("DATA", "Other comprehensive income, net of income tax", (None, None, 0.0, None, None, None, 0.0)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, 0.0, None, None, 17.6, 17.6)),
    ("DATA", "Purchase of own shares", (None, None, None, None, -0.2, None, -0.2)),
    ("DATA", "Sale of own shares", (None, None, None, None, 0.5, None, 0.5)),
    ("DATA", "Loss on sale of own shares", (None, None, None, None, None, -0.5, -0.5)),
    ("DATA", "Issue of shares", (None, 0.2, None, None, None, None, 0.2)),
    ("DATA", "Dividends", (None, None, None, None, None, -6.4, -6.4)),
    ("DATA", "Share-based payments", (None, None, None, None, None, 2.6, 2.6)),
    ("TOTAL", "Balance at 31 December 2025", (7.6, 84.2, 0.0, None, -1.9, 284.4, 374.3)),
]

bw.add_equity_changes_sheet(
    "Secure Trust Bank PLC - Group Statement of Changes in Equity",
    "Consolidated Group basis, £million; chronological 1 January 2021 through 31 December 2025.",
    EQ_HEADERS, EQ_ROWS, EQ_SOURCES, first_col_width=58, source_height=280,
)

rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit for the year", {"FY2025": 17.6, "FY2024": 19.7, "FY2023": 24.3, "FY2022": 33.7, "FY2021": 45.6}),
    ("DATA", "Income tax expense", {"FY2025": 9.9, "FY2024": 9.5, "FY2023": 9.1, "FY2022": 10.3, "FY2021": 10.4}),
    ("DATA", "Depreciation of property, plant and equipment", {"FY2025": .8, "FY2024": 1.0, "FY2023": .9, "FY2022": 1.2, "FY2021": 1.3}),
    ("DATA", "Depreciation of right-of-use assets", {"FY2025": 1.1, "FY2024": 1.0, "FY2023": .7, "FY2022": .7, "FY2021": .7}),
    ("DATA", "Amortisation of intangible assets", {"FY2025": 1.2, "FY2024": 1.4, "FY2023": 1.2, "FY2022": 1.4, "FY2021": 1.5}),
    ("DATA", "Loss/(gain) on disposals and modifications", {"FY2024": 0.0, "FY2023": .2, "FY2022": -7.5, "FY2021": -.5}),
    ("DATA", "Impairment charge on loans and advances", {"FY2025": 58.0, "FY2024": 61.9, "FY2023": 43.2, "FY2022": 39.0, "FY2021": 4.5}),
    ("DATA", "Share-based compensation", {"FY2025": 2.0, "FY2024": 2.3, "FY2023": 1.1, "FY2022": 2.0, "FY2021": 1.0}),
    ("DATA", "Provisions for liabilities and charges", {"FY2025": 21.7, "FY2024": 9.8, "FY2023": 8.5}),
    ("DATA", "Other non-cash items included in profit before tax", {"FY2025": .2, "FY2024": -.6, "FY2023": -.8, "FY2022": 1.0, "FY2021": .4}),
    ("DATA", "Loans and advances to customers", {"FY2025": -159.0, "FY2024": -354.8, "FY2023": -439.0, "FY2022": -497.1, "FY2021": -238.4}),
    ("DATA", "Loans and advances to banks and central banks", {"FY2025": -5.1, "FY2024": 5.0, "FY2023": -1.3, "FY2022": .6, "FY2021": -1.9}),
    ("DATA", "Other assets", {"FY2025": 2.8, "FY2024": 1.4, "FY2023": .4, "FY2022": -1.5, "FY2021": 6.0}),
    ("DATA", "Deposits from customers", {"FY2025": 264.7, "FY2024": 373.1, "FY2023": 357.2, "FY2022": 411.4, "FY2021": 110.7}),
    ("DATA", "Provisions for liabilities and charges utilisation", {"FY2025": -7.6, "FY2024": -4.7, "FY2023": -4.7, "FY2022": -1.1, "FY2021": -.7}),
    ("DATA", "Other liabilities", {"FY2025": 60.7, "FY2024": -5.5, "FY2023": -37.8, "FY2022": 45.6, "FY2021": -24.4}),
    ("DATA", "Income tax paid", {"FY2025": -12.0, "FY2024": -8.8, "FY2023": -8.6, "FY2022": -7.0, "FY2021": -12.6}),
    ("TOTAL", "Net cash inflow/(outflow) from operating activities", {"FY2025": 257.0, "FY2024": 111.7, "FY2023": -45.4, "FY2022": 32.7, "FY2021": -96.4}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Consideration on sale of loan books", {"FY2023": 0.0, "FY2022": 81.9, "FY2021": 60.4}),
    ("DATA", "Sale of investment property", {"FY2022": 3.3}),
    ("DATA", "Maturity and sales of debt securities", {"FY2022": 80.0, "FY2021": 90.0}),
    ("DATA", "Purchase of debt securities", {"FY2022": -80.0, "FY2021": -90.0}),
    ("DATA", "Purchase of property, plant and equipment and intangible assets", {"FY2025": -1.6, "FY2024": -1.0, "FY2023": -2.7, "FY2022": -2.7, "FY2021": -1.3}),
    ("DATA", "Purchase of investment property", {"FY2025": -1.1}),
    ("DATA", "Purchase of debt securities", {"FY2025": -1.0}),
    ("DATA", "Sale of property, plant and equipment", {"FY2025": 1.9}),
    ("TOTAL", "Net cash inflow/(outflow) from investing activities", {"FY2025": -1.8, "FY2024": -1.0, "FY2023": -2.7, "FY2022": 82.5, "FY2021": 59.1}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Issue of subordinated debt", {"FY2023": 70.0}),
    ("DATA", "Redemption of subordinated debt", {"FY2023": -28.8}),
    ("DATA", "Drawdown/(repayment) of amounts due to banks", {"FY2025": -1.7, "FY2024": .8, "FY2023": -.9, "FY2022": 7.0, "FY2021": 114.4}),
    ("DATA", "Drawdown of sale and repurchase agreements", {"FY2025": 250.0, "FY2024": 125.0}),
    ("DATA", "Repayment of sale and repurchase agreements", {"FY2025": -175.0}),
    ("DATA", "Repayment of Term Funding Scheme", {"FY2025": -230.0, "FY2024": -160.0}),
    ("DATA", "Purchase of own shares", {"FY2025": -.2, "FY2024": -1.4, "FY2023": -1.2, "FY2022": -.3}),
    ("DATA", "Issue of shares", {"FY2025": .2, "FY2024": .2, "FY2023": 1.7}),
    ("DATA", "Dividends paid", {"FY2025": -6.4, "FY2024": -5.2, "FY2023": -8.4, "FY2022": -10.7, "FY2021": -11.9}),
    ("DATA", "Repayment of lease liabilities", {"FY2025": -1.3, "FY2024": -1.4, "FY2023": -.9, "FY2022": -1.0, "FY2021": -.9}),
    ("DATA", "Issue of ordinary shares", {"FY2021": 0.0}),
    ("TOTAL", "Net cash (outflow)/inflow from financing activities", {"FY2025": -164.4, "FY2024": -42.0, "FY2023": 31.5, "FY2022": -5.0, "FY2021": 101.6}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 90.8, "FY2024": 68.7, "FY2023": -16.6, "FY2022": 110.2, "FY2021": 64.3}),
    ("DATA", "Cash and cash equivalents at 1 January", {"FY2025": 469.0, "FY2024": 400.3, "FY2023": 416.9, "FY2022": 306.7, "FY2021": 242.4}),
    ("TOTAL", "Cash and cash equivalents at 31 December", {"FY2025": 559.8, "FY2024": 469.0, "FY2023": 400.3, "FY2022": 416.9, "FY2021": 306.7}),
]

bw.add_cash_flow_sheet(
    "Secure Trust Bank PLC - Group Cash Flow Statement",
    "Consolidated Group basis, £million; FY2021 uses the restated comparative presented in the FY2022 report.",
    rows, CASH_SOURCES, first_col_width=68, source_height=250, unit_suffix=" (£m)",
)

AQ_SOURCES = (
    "Sources - Secure Trust Bank PLC consolidated Group loan book by product and IFRS 9 stage, £million:\n"
    f"FY2025: Annual Report & Accounts 2025, Note 17 Allowances for impairment of loans and advances, p.163 - {AR2025_URL}\n"
    f"FY2024: Annual Report & Accounts 2025, Note 17 (FY2024 comparative column), p.164 - {AR2025_URL}\n"
    f"FY2023: Annual Report & Accounts 2023, Note 16 Allowances for impairment of loans and advances, p.136 - {AR2023_URL}\n"
    f"FY2022: Annual Report & Accounts 2022, Note 17 Allowances for impairment of loans and advances, p.142 - {AR2022_URL}\n"
    f"FY2021: Annual Report & Accounts 2021, Note 17 Allowances for impairment of loans and advances, p.130 - {AR2021_URL}\n\n"
    + ENTITY_NOTE
    + " Every year's Total gross loans and advances to customers less Total impairment allowance ties exactly to the Balance Sheet's own 'Loans and advances to "
    "customers' line - for FY2025, this means excluding the Vehicle Finance book reclassified as 'Assets held for sale' (£434.8m gross, £44.0m provision), which "
    "the Balance Sheet reports separately, not within Loans and advances to customers. Debt Management was a distinct product line only in FY2021, sold during "
    "2022. 'Stage 3 as % of gross loans' is a derived credit-quality proxy (Stage 3 provision-eligible balances / Total gross loans), not a Pillar 3-defined ratio."
)

AQ_ROWS = [
    ("SECTION", "Loan book by product - gross loans and advances to customers", {}),
    ("DATA", "Retail Finance", {"FY2025": 1499.6, "FY2024": 1387.9, "FY2023": 1255.3, "FY2022": 1082.7, "FY2021": 786.5}),
    ("DATA", "Real Estate Finance", {"FY2025": 1475.3, "FY2024": 1353.9, "FY2023": 1251.8, "FY2022": 1118.9, "FY2021": 1112.8}),
    ("DATA", "Commercial Finance", {"FY2025": 366.4, "FY2024": 351.8, "FY2023": 383.2, "FY2022": 378.4, "FY2021": 314.4}),
    ("DATA", "Vehicle Finance", {"FY2025": 434.8, "FY2024": 626.7, "FY2023": 513.1, "FY2022": 417.5, "FY2021": 297.5}),
    ("DATA", "Debt Management", {"FY2021": 86.9}),
    ("TOTAL", "Total gross loans and advances to customers", {"FY2025": 3776.1, "FY2024": 3720.3, "FY2023": 3403.4, "FY2022": 2997.5, "FY2021": 2598.1}),
    ("SECTION", "Impairment allowance by IFRS 9 stage", {}),
    ("DATA", "Stage 1: subject to 12-month ECL", {"FY2025": 25.2, "FY2024": 29.6, "FY2023": 29.5, "FY2022": 24.3, "FY2021": 18.5}),
    ("DATA", "Stage 2: subject to lifetime ECL, not credit-impaired", {"FY2025": 21.3, "FY2024": 15.9, "FY2023": 18.2, "FY2022": 28.6, "FY2021": 20.0}),
    ("DATA", "Stage 3: subject to lifetime ECL, credit-impaired", {"FY2025": 43.0, "FY2024": 66.3, "FY2023": 40.4, "FY2022": 25.1, "FY2021": 29.0}),
    ("TOTAL", "Total impairment allowance", {"FY2025": 89.5, "FY2024": 111.8, "FY2023": 88.1, "FY2022": 78.0, "FY2021": 67.5}),
    ("DATA", "Provision coverage ratio", {"FY2025": "2.4%", "FY2024": "3.0%", "FY2023": "2.6%", "FY2022": "2.6%", "FY2021": "2.6%"}),
    ("DATA", "Stage 3 as % of gross loans (derived)", {"FY2025": "1.14%", "FY2024": "1.78%", "FY2023": "1.19%", "FY2022": "0.84%", "FY2021": "1.12%"}),
]

bw.add_asset_quality_sheet(
    "Secure Trust Bank PLC - Group Asset Quality",
    "Consolidated Group basis, £million; loan book by product and IFRS 9 impairment stage.",
    AQ_ROWS, AQ_SOURCES, first_col_width=60, source_height=260, unit_suffix=" (£m)",
)

def metric(name, unit, data, note=None):
    bw.add_metric_sheet(name, unit, data, P3_SOURCES, note=note, first_col_width=52, source_height=230)

metric("CET1 Capital", "£m", [("Common Equity Tier 1 capital", {"FY2025": 364.8, "FY2024": 351.4, "FY2023": 337.9, "FY2022": 327.4, "FY2021": 303.6})])
metric("CET1 Ratio", "% of RWEA", [("CET1 ratio", {"FY2025": "12.9%", "FY2024": "12.3%", "FY2023": "12.7%", "FY2022": "14.0%", "FY2021": "14.5%"})])
metric("Tier 1 Capital", "£m", [("Tier 1 capital", {"FY2025": 364.8, "FY2024": 351.4, "FY2023": 337.9, "FY2022": 327.4, "FY2021": 303.6})])
metric("Tier 1 Ratio", "% of RWEA", [("Tier 1 ratio", {"FY2025": "12.9%", "FY2024": "12.3%", "FY2023": "12.7%", "FY2022": "14.0%", "FY2021": "14.5%"})])
metric("Total Capital", "£m", [("Total capital", {"FY2025": 428.4, "FY2024": 415.7, "FY2023": 397.6, "FY2022": 377.3, "FY2021": 350.6})])
metric("Total Capital Ratio", "% of RWEA", [("Total capital ratio", {"FY2025": "15.2%", "FY2024": "14.6%", "FY2023": "15.0%", "FY2022": "16.2%", "FY2021": "16.8%"})])
metric("Total RWAs", "£m", [("Total RWEAs", {"FY2025": 2827.5, "FY2024": 2855.7, "FY2023": 2653.4, "FY2022": 2335.0, "FY2021": 2087.4})])

RWA_SOURCES = (
    "Sources - Secure Trust Bank PLC Group UK OV1 Overview of risk weighted exposure amounts:\n"
    f"FY2025: Pillar 3 Disclosures for the year ended 31 December 2025, Section 3, p.6 - {P3_URLS['FY2025']}\n"
    f"FY2024: Pillar 3 Disclosures for the year ended 31 December 2024, Section 3, p.6 - {P3_URLS['FY2024']}\n"
    f"FY2023: Pillar 3 Disclosures for the year ended 31 December 2023, Section 3, p.6 - {P3_URLS['FY2023']}\n"
    f"FY2022: Pillar 3 Disclosures for the year ended 31 December 2022, Section 3, p.6 - {P3_URLS['FY2022']}\n"
    f"FY2021: Pillar 3 disclosures for the year ended 31 December 2021, Section 4.5 Pillar 1 Capital Requirements table, p.14 - {P3_URLS['FY2021']}\n\n"
    + ENTITY_NOTE
    + " FY2021 predates Secure Trust Bank's adoption of the UK OV1 template - it discloses RWAs by exposure class (Central governments, Institutions, "
    "Corporates, Retail, Secured on Immovable Property, Exposures in default, Other, Items associated with a particular high risk) rather than by risk type; "
    "these have been mapped to a single 'Credit Risk (Standardised Approach)' line for comparability with FY2022 onward, matching the Pillar 3 document's own "
    "subtotal. 'Amounts below the thresholds for deduction' (FY2022-25) is a memo/information line excluded from the Total per the source template's own "
    "footnote, not summed into RWAs."
)

RWA_ROWS = [
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 2521.0, "FY2024": 2561.0, "FY2023": 2368.8, "FY2022": 2062.4, "FY2021": 1826.6}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 0.8, "FY2024": 10.7, "FY2023": 12.1, "FY2022": 8.1, "FY2021": 2.3}),
    ("DATA", "Operational risk", {"FY2025": 305.7, "FY2024": 284.0, "FY2023": 272.5, "FY2022": 264.5, "FY2021": 258.5}),
    ("TOTAL", "Total RWEAs", {"FY2025": 2827.5, "FY2024": 2855.7, "FY2023": 2653.4, "FY2022": 2335.0, "FY2021": 2087.4}),
    ("DATA", "Memo: amounts below thresholds for deduction (not summed into Total)", {"FY2025": 8.9, "FY2024": 8.3, "FY2023": 10.7, "FY2022": 4.0}),
]

bw.add_rwa_breakdown_sheet(
    "Secure Trust Bank PLC - Group RWA Breakdown",
    "Consolidated Group basis, £million; UK OV1 Overview of risk weighted exposure amounts (FY2021 uses the pre-OV1 exposure-class table).",
    RWA_ROWS, RWA_SOURCES, first_col_width=64, source_height=260, unit_suffix=" (£m)",
)

metric("Leverage Ratio", "%", [("Leverage ratio excluding claims on central banks", {"FY2025": "9.4%", "FY2024": "9.5%", "FY2023": "9.7%", "FY2022": "10.7%", "FY2021": "10.3%"})])
metric("LCR", "%", [("Liquidity Coverage Ratio", {"FY2025": "190.4%", "FY2024": "219.6%", "FY2023": "208.0%", "FY2022": "270.1%", "FY2021": "Not publicly disclosed"})], "The 2021 Pillar 3 key-metrics table does not disclose an LCR figure; no annual-report proxy is substituted.")
metric("NSFR", "%", [("Net Stable Funding Ratio", {"FY2025": "Not publicly disclosed", "FY2024": "Not publicly disclosed", "FY2023": "143.6%", "FY2022": "152.8%", "FY2021": "Not publicly disclosed"})])
metric("MREL Ratio", "%", [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})], "No quantitative MREL ratio was located in the reviewed annual reports or Pillar 3 disclosures.")

INTERIM_VALUES = {
    "H1 2025": {
        "CET1 capital": (367.1, "£m"),
        "Tier 1 capital": (367.1, "£m"),
        "Total capital": (432.7, "£m"),
        "Total RWEAs": (2916.8, "£m"),
        "CET1 ratio": ("12.6%", "% of RWEA"),
        "Tier 1 ratio": ("12.6%", "% of RWEA"),
        "Total capital ratio": ("14.8%", "% of RWEA"),
        "Leverage ratio excluding claims on central banks": ("9.3%", "%"),
        "Liquidity Coverage Ratio": ("193.5%", "%"),
    },
    "H1 2024": {
        "CET1 capital": (348.2, "£m"),
        "Tier 1 capital": (348.2, "£m"),
        "Total capital": (409.7, "£m"),
        "Total RWEAs": (2735.3, "£m"),
        "CET1 ratio": ("12.7%", "% of RWEA"),
        "Tier 1 ratio": ("12.7%", "% of RWEA"),
        "Total capital ratio": ("15.0%", "% of RWEA"),
        "Leverage ratio excluding claims on central banks": ("9.9%", "%"),
        "Liquidity Coverage Ratio": ("216.3%", "%"),
    },
    "H1 2023": {
        "CET1 capital": (326.8, "£m"),
        "Tier 1 capital": (326.8, "£m"),
        "Total capital": (383.5, "£m"),
        "Total RWEAs": (2518.5, "£m"),
        "CET1 ratio": ("13.0%", "% of RWEA"),
        "Tier 1 ratio": ("13.0%", "% of RWEA"),
        "Total capital ratio": ("15.2%", "% of RWEA"),
        "Leverage ratio excluding claims on central banks": ("10.1%", "%"),
        "Liquidity Coverage Ratio": ("217.0%", "%"),
        "NSFR ratio": ("150.9%", "%"),
    },
    "H1 2022": {
        "CET1 capital": (313.8, "£m"),
        "Tier 1 capital": (313.8, "£m"),
        "Total capital": (363.6, "£m"),
        "Total RWEAs": (2237.1, "£m"),
        "CET1 ratio": ("14.0%", "% of RWEA"),
        "Tier 1 ratio": ("14.0%", "% of RWEA"),
        "Total capital ratio": ("16.3%", "% of RWEA"),
        "Leverage ratio excluding claims on central banks": ("10.6%", "%"),
        "Liquidity Coverage Ratio": ("363.0%", "%"),
    },
}

INTERIM_PAGE_TABLE = {
    "H1 2025": "PDF p. 5, UK KM1 / IFRS 9-FL",
    "H1 2024": "PDF p. 5, UK KM1 / IFRS 9-FL",
    "H1 2023": "PDF p. 5, UK KM1",
    "H1 2022": "PDF p. 3, UK KM1",
}

interim_rows = []
interim_links = {}
for period, metrics in INTERIM_VALUES.items():
    for metric_name, (value, unit) in metrics.items():
        interim_rows.append(
            (period, "Interim Pillar 3", metric_name, value, unit, "Group", period, INTERIM_PAGE_TABLE[period])
        )
        interim_links[(len(interim_rows) - 1, 6)] = INTERIM_URLS[period]

bw.add_wide_interim_sheet(
    "Interim Pillar 3",
    headers=["Period", "Disclosure type", "Metric", "Value", "Unit", "Basis", "Source document", "Page / table"],
    rows=interim_rows,
    subtitle="Secure Trust Bank PLC Group basis; H1 observations from official interim UK KM1 disclosures.",
    note=(
        "Coverage: H1 2022 through H1 2025, covering the four official interim disclosures located. "
        "Each disclosure states that Secure Trust Bank PLC and its subsidiaries (the Group) are covered and "
        "that Pillar 3 disclosures are issued every six months. No separate H1 2021 Pillar 3 disclosure was "
        "located in the official archive; no 2021 interim values are inferred from annual or comparative data. "
        "NSFR was not disclosed in the H1 2022, H1 2024, or H1 2025 KM1 tables; those gaps are omitted rather "
        "than represented as zero. H1 2023 NSFR is reported. All source-document cells link to the official "
        "Secure Trust Bank document-library page for the relevant disclosure."
    ),
    widths=[14, 20, 46, 14, 16, 14, 42, 30],
    hyperlink_cells=interim_links,
)

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 4316.0, "FY2024": 4116.7, "FY2023": 3778.0, "FY2022": 3380.3, "FY2021": 2885.9}),
        ("Loans and advances to customers", {"FY2025": 3295.8, "FY2024": 3608.5, "FY2023": 3315.3, "FY2022": 2919.5, "FY2021": 2530.6}),
        ("Deposits from customers", {"FY2025": 3509.6, "FY2024": 3244.9, "FY2023": 2871.8, "FY2022": 2514.6, "FY2021": 2103.2}),
        ("Total equity", {"FY2025": 374.3, "FY2024": 360.5, "FY2023": 344.5, "FY2022": 326.9, "FY2021": 302.4}),
    ], balance_sheet_unit="£m",
    income_statement_totals=[
        ("Operating income", {"FY2025": 165.2, "FY2024": 203.9, "FY2023": 184.7, "FY2022": 169.6, "FY2021": 164.5}),
        ("Operating expenses", {"FY2025": -74.7, "FY2024": -103.8, "FY2023": -99.7, "FY2022": -93.2, "FY2021": -104.0}),
        ("Net impairment charge on loans and advances", {"FY2025": -31.4, "FY2024": -61.9, "FY2023": -43.2, "FY2022": -38.2, "FY2021": -4.5}),
        ("Profit for the year", {"FY2025": 17.6, "FY2024": 19.7, "FY2023": 24.3, "FY2022": 33.7, "FY2021": 45.6}),
    ], income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 360.5, "FY2024": 344.5, "FY2023": 326.4, "FY2022": 302.4, "FY2021": 267.6}),
        ("Total comprehensive income for the year", {"FY2025": 17.6, "FY2024": 20.0, "FY2023": 24.8, "FY2022": 33.5, "FY2021": 45.7}),
        ("Other equity movements, net", {"FY2025": -3.8, "FY2024": -4.0, "FY2023": -6.7, "FY2022": -9.0, "FY2021": -10.9}),
        ("Closing equity", {"FY2025": 374.3, "FY2024": 360.5, "FY2023": 344.5, "FY2022": 326.9, "FY2021": 302.4}),
    ], equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 257.0, "FY2024": 111.7, "FY2023": -45.4, "FY2022": 32.7, "FY2021": -96.4}),
        ("Net cash from/(used in) investing activities", {"FY2025": -1.8, "FY2024": -1.0, "FY2023": -2.7, "FY2022": 82.5, "FY2021": 59.1}),
        ("Net cash from/(used in) financing activities", {"FY2025": -164.4, "FY2024": -42.0, "FY2023": 31.5, "FY2022": -5.0, "FY2021": 101.6}),
        ("Cash and cash equivalents at end of year", {"FY2025": 559.8, "FY2024": 469.0, "FY2023": 400.3, "FY2022": 416.9, "FY2021": 306.7}),
    ], cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "12.9%", "FY2024": "12.3%", "FY2023": "12.7%", "FY2022": "14.0%", "FY2021": "14.5%"}),
        ("Total Capital Ratio", {"FY2025": "15.2%", "FY2024": "14.6%", "FY2023": "15.0%", "FY2022": "16.2%", "FY2021": "16.8%"}),
        ("Leverage Ratio", {"FY2025": "9.4%", "FY2024": "9.5%", "FY2023": "9.7%", "FY2022": "10.7%", "FY2021": "10.3%"}),
        ("LCR", {"FY2025": "190.4%", "FY2024": "219.6%", "FY2023": "208.0%", "FY2022": "270.1%"}),
        ("NSFR", {"FY2023": "143.6%", "FY2022": "152.8%"}),
    ],
    note="Group cash flows and Group Pillar 3 metrics are deliberately kept on their respective disclosed bases. FY2021 cash uses the FY2022 restated comparative; blank regulatory cells mean not disclosed, not zero.",
)

bw.save("/Users/armaan/code/katalysis/banks/SECURE TRUST BANK FINANCIALS.xlsx")
