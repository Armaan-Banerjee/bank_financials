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
# SLUG TRAP (verified 2026-09-15): the document-library slugs change suffix by vintage -
# FY2015-FY2019 editions end "-annual"; FY2020 onward end "-final". Every "-final"
# permutation for 2015-2019 404s, which is why earlier passes recorded those years as
# unsourced. The slugs are not HTML landing pages: they 302 straight to the PDF bytes.
P3_ANNUAL_SUFFIX_YEARS = {"FY2019", "FY2018", "FY2017"}
P3_URLS = {
    y: (
        "https://www.securetrustbank.com/investor-relations/document-library/"
        f"pillar-3-disclosure-{y[-4:]}-{'annual' if y in P3_ANNUAL_SUFFIX_YEARS else 'final'}"
    )
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

# PAGE NUMBERS ARE THE PRINTED FOLIO, not the PDF sheet index, and the two differ by
# one in every Secure Trust Bank Pillar 3 edition (the cover carries no printed number).
# Corrected 2026-09-16 after re-reading each page's own footer: the FY2025-FY2022 KM1
# citations read "p. 5" (the PDF sheet) where every one of those pages is footed 4, and
# the FY2020 CC1 citation read "Section 4.4 ... p. 13" where the table is section 4.1 on
# a page footed 12. A folio is a promise about where a reader should look and an
# off-by-one one cannot be detected from inside the spreadsheet.
P3_PAGE_TABLE = {
    "FY2025": "Key metrics table (UK KM1), p. 4",
    "FY2024": "Key metrics table (UK KM1), p. 4",
    "FY2023": "Key metrics table (UK KM1), rows 1-17 on p. 4 and rows 18-20 continued on p. 5",
    "FY2022": "Key metrics table (UK KM1), p. 4",
    "FY2021": "Key metrics table, p. 4; Total RWA from Section 4.1 table CC1 row 60, p. 12",
    "FY2020": "Section 2 'Key Prudential Metrics and Risk Weighted Assets', p. 4 ('Including IFRS 9 Transitional Arrangement' column); "
              "Total RWA from Section 4.1 table CC1 row 60, p. 12; leverage ratio from Appendix B table LRCom row 22, p. 32",
    "FY2019": "Section 2 'Key Prudential Metrics and Risk Weighted Assets', p. 5 (31 Dec 2019 column); "
              "Total RWA from Section 4.1 table CC1 row 60, p. 7; leverage ratio from Appendix B table LRCom row 22, p. 22",
    "FY2018": "Section 2.2 'Key Metrics (at consolidated group level)', p. 4, column a (31-Dec-18)",
    "FY2017": "Section 2.2 'Key Metrics (at consolidated group level)', p. 5, column a (31-Dec-17)",
}

P3_BASIS_NOTE = (
    "HISTORICAL EDITIONS (FY2017-FY2020), added 2026-09-15. Each year's figures are taken from that year's OWN Pillar 3 edition, "
    "consistent with the convention already used for this bank's Balance Sheet and Profit & Loss sheets. Two subsequent restatements "
    "are therefore NOT written over the own-year columns, but are recorded here so the break is auditable:\n"
    "(a) FY2018 - the FY2019 edition restates its 31 December 2018 comparative column to CET1/Tier 1 capital 240.0 (own-year 251.8), "
    "Total capital 285.7 (own-year 297.5), CET1 and Tier 1 ratios 13.2% (own-year 13.8%), Total capital ratio 15.7% (own-year 16.3%), "
    "and Basel III leverage ratio 9.5% on an exposure measure of 2,539.0 (own-year 10.4% on 2,432.8). Total RWA of 1,824.6 is identical "
    "in both editions.\n"
    "(b) FY2019 - the FY2020 edition footnotes the FY2019 leverage ratio as 9.7%, 'Previously disclosed as 9.8%, which has been restated' "
    "(exposure measure 2,772.7 restated from 2,740.8). The own-year 9.8% is kept above.\n"
    "The FY2017 and FY2018 editions both footnote their RWA row: 'Total Risk Exposure (TRE) has been reported in row 4 rather than Risk "
    "Weighted Assets (RWA). TRE represents RWA plus the Operational Risk component.' The figure is transcribed exactly as the document "
    "states it; nothing is recomputed.\n"
    "FY2017-FY2020 are pre-UK-CRR Basel III/CRR IV editions, so the leverage ratio and LCR they disclose are on different bases from the "
    "UK KM1 series that begins in FY2021 - see the notes on those two sheets. No figure from one basis is carried into the other's row."
)

P3_SOURCES = "Sources - Secure Trust Bank PLC Group regulatory disclosures:\n" + "\n".join(
    f"{y}: Secure Trust Bank PLC Pillar 3 disclosures for the year ended 31 December {y[-4:]}, "
    f"{P3_PAGE_TABLE[y]} - {P3_URLS[y]}"
    for y in YEARS
) + "\n\n" + P3_BASIS_NOTE + "\n\n" + ENTITY_NOTE + " Regulatory figures are Group figures and are not substituted into Company cash flows."

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
    f"FY2021: Annual Report & Accounts 2021, Consolidated statement of comprehensive income, p.108 - {AR2021_URL}\n"
    f"FY2020: Annual Report & Accounts 2020, Consolidated statement of comprehensive income, p.113 - {AR_URLS['FY2020']}\n"
    f"FY2019: Annual Report & Accounts 2019, Consolidated statement of comprehensive income, p.120 - {AR_URLS['FY2019']}\n"
    f"FY2018: Annual Report & Accounts 2018, Consolidated statement of comprehensive income, p.128 - {AR_URLS['FY2018']}\n"
    f"FY2017: Annual Report & Accounts 2017, Consolidated statement of comprehensive income, p.110, 'Total' column - {AR_URLS['FY2017']}\n\n"
    "THREE CORRECTIONS MADE 2026-09-16, each traced back to the year's own annual report after the operating-income-to-"
    "profit-before-tax chain was found not to foot in three years. (a) FY2020 was missing a line: AR2020 p.113 prints "
    "'Losses on modification of financial assets (3.1)' between the impairment charge and operating expenses, and the row here "
    "carried FY2023/FY2022/FY2021 gains only. The row is now captioned 'Gains/(losses) on modification of financial assets', "
    "which is AR2021's own caption for the line across both signs. (b) FY2021 carried the same 0.1 loss twice. AR2021 p.108 "
    "prints one such line, 'Losses from derivatives and hedge accounting (0.1)'; the FY2022 report's restated 2021 comparative "
    "renames it 'Fair value losses on financial instruments (0.1)'. Both captions existed here with a value against FY2021, so "
    "the 0.1 was counted twice. The own-edition caption is kept and the restated one is now blank for FY2021. (c) FY2017 was "
    "missing 'Profit on sale of equity instruments available-for-sale 0.3', which AR2017 p.110 prints immediately before profit "
    "before income tax. It is shown here among the other non-interest items rather than in that printed position, because this "
    "sheet merges nine editions into one row set; AR2018 p.128 prints the same row with a dash for 2018, so FY2018 is left "
    "blank rather than zero. After all three, operating income less every intervening line equals the published profit before "
    "income tax in all nine years.\n\n"
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
    ("DATA", "Gains/(losses) on modification of financial assets", {"FY2023": 0.3, "FY2022": 1.1, "FY2021": 1.5, "FY2020": -3.1}),
    ("DATA", "Other gains/(losses)", {"FY2025": 0.1, "FY2024": -0.3}),
    ("DATA", "Fair value gains/(losses) on financial instruments", {"FY2025": 0.1, "FY2024": 1.2, "FY2023": 0.5, "FY2022": -0.3}),
    ("DATA", "Loss on disposal of loan books", {"FY2021": -1.4}),
    ("DATA", "Losses from derivatives and hedge accounting", {"FY2021": -0.1}),
    ("DATA", "Profit on sale of equity instruments available-for-sale", {"FY2017": 0.3}),
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
    IS_ROWS, IS_SOURCES, first_col_width=68, source_height=430, unit_suffix=" (£m)",
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

# ---------------------------------------------------------------------------
# KM1 Key Metrics
#
# FOUR REGIMES, NEVER MERGED. Secure Trust Bank's nine Pillar 3 editions do not
# all print the same table, and three of them print no key-metrics template at
# all. The sheet below therefore carries TWO separate template blocks and leaves
# a deliberate three-year hole between them:
#
#   FY2025-FY2022  UK KM1 (rows 1-20, UK-prefixed rows UK 7a-7d, UK 11a, UK 16a,
#                  UK 16b). The Bank omits the rows it has nothing to report in
#                  - UK 8a, UK 9a, 10, UK 10a and 14a-14e never appear - and its
#                  own p.3 says so: "where specific rows and columns in the
#                  tables prescribed by the PRA are not applicable, these are
#                  omitted". Those rows are therefore absent here too rather
#                  than printed empty, because reproducing the table means
#                  reproducing which rows it has.
#   FY2021-FY2019  NO KM1 AT ALL. Those three editions replace the template with
#                  a short unnumbered "Key Prudential Metrics" summary: capital
#                  amounts, a capital-ratio block, and (FY2019 only) a two-line
#                  Basel III leverage block. No SREP block, no buffer block, no
#                  row 12, no LCR rows, no NSFR rows; FY2020 and FY2021 do not
#                  even carry an RWA amount in that table. It fails the row-set
#                  test, so those columns are left blank rather than filled from
#                  a table that is not the template. This is a POSITIVE finding,
#                  not a retrieval failure: the FY2021 extraction returns 120
#                  occurrences of "capital" and 118 of "ratio" against 0 of
#                  "km1", and pdfimages reports one image in the file (the
#                  logo), so there is no scanned table hiding from the text
#                  layer either.
#   FY2018-FY2017  The EARLIER EU/Basel KM1, "Key Metrics (at consolidated group
#                  level)", rows 1-20 with the "fully loaded ECL accounting
#                  model" twins 1a/2a/3a/5a/6a/7a/14a and FIVE QUARTERLY columns
#                  (a = year end, b-e = the preceding quarters and the prior
#                  year end). Only column a is taken, because only column a is
#                  that edition's reporting date. This is a genuinely different
#                  template from the UK KM1 above - its row 13/14 leverage is
#                  Basel III (exposure measure INCLUDING claims on central
#                  banks), its rows 15-17 are a period observation rather than a
#                  twelve-month average, and its row 4 is footnoted as Total
#                  Risk Exposure rather than RWA - so it is kept in its own
#                  block and no figure is carried across the break.
#
# IFRS 9-FL twins appear only in the FY2024 and FY2023 editions. The FY2025
# edition states its figures are "reported without the application of Article
# 473a IFRS 9 transitional arrangements", so there is no twin to print; the
# FY2022 edition prints only the transitional figures. Rows 18-20 exist only in
# the FY2023 and FY2022 editions (the SDDT reduced template drops NSFR from
# FY2024 onward, and the FY2017 edition predates the requirement).
#
# Each year comes from the edition in which that year is the REPORTING year, so
# the FY2022 column is the FY2022 edition's own 31 December 2022 figures, NOT
# the "Restated" 31 December 2022 comparative column the FY2023 edition prints.
KM1_ROWS = [
    # Gap-fill round 2026-09-18: FY2021/FY2020/FY2019 held no cell at all, so a
    # reader saw three blank year columns and the census scored them as untouched
    # gaps - even though the negative was already sourced in KM1_SOURCES below.
    # It now appears IN the columns. A statement row, not a template row: nothing
    # from those editions' short unnumbered 'Key Prudential Metrics' summary, nor
    # from their CC1/OV1/LRCom tables, is written into a KM1 row here.
    # Re-confirmed at source 2026-09-18: all three PDFs fetched on rung 2
    # (curl -L), 200 application/pdf, %PDF magic, 512KB/596KB/760KB; text layer
    # returns 960/975/583 hits on 'the' (richness control) and ZERO on 'KM1'.
    ("DATA", "[No key-metrics template published for this year - see note below]",
     {"FY2021": "Not published - this edition prints only a short unnumbered summary",
      "FY2020": "Not published - this edition prints only a short unnumbered summary",
      "FY2019": "Not published - this edition prints only a short unnumbered summary"}),
    ("SECTION", "UK KM1 (FY2025-FY2022 editions) - Available own funds (amounts) (£m)", {}),
    ("DATA", "1    Common Equity Tier 1 (CET 1) capital",
     {"FY2025": 364.8, "FY2024": 351.4, "FY2023": 337.9, "FY2022": 327.4}),
    ("DATA", "     CET 1 capital as if IFRS 9 transitional arrangements had not been applied",
     {"FY2024": 351.3, "FY2023": 335.8}),
    ("DATA", "2    Tier 1 capital",
     {"FY2025": 364.8, "FY2024": 351.4, "FY2023": 337.9, "FY2022": 327.4}),
    ("DATA", "     Tier 1 capital as if IFRS 9 transitional arrangements had not been applied",
     {"FY2024": 351.3, "FY2023": 335.8}),
    ("DATA", "3    Total capital",
     {"FY2025": 428.4, "FY2024": 415.7, "FY2023": 397.6, "FY2022": 377.3}),
    ("DATA", "     Total capital as if IFRS 9 transitional arrangements had not been applied",
     {"FY2024": 415.6, "FY2023": 395.5}),
    ("SECTION", "Risk weighted exposure amounts (£m)", {}),
    ("DATA", "4    Total RWEAs",
     {"FY2025": 2827.5, "FY2024": 2855.7, "FY2023": 2653.4, "FY2022": 2335.0}),
    ("DATA", "     Total RWEAs as if IFRS 9 transitional arrangements had not been applied",
     {"FY2024": 2853.6, "FY2023": 2651.7}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "5    CET 1 ratio (%)",
     {"FY2025": "12.9%", "FY2024": "12.3%", "FY2023": "12.7%", "FY2022": "14.0%"}),
    ("DATA", "     CET 1 as if IFRS 9 transitional arrangements had not been applied",
     {"FY2024": "12.3%", "FY2023": "12.7%"}),
    ("DATA", "6    Tier 1 ratio (%)",
     {"FY2025": "12.9%", "FY2024": "12.3%", "FY2023": "12.7%", "FY2022": "14.0%"}),
    ("DATA", "     Tier 1 as if IFRS 9 transitional arrangements had not been applied",
     {"FY2024": "12.3%", "FY2023": "12.7%"}),
    ("DATA", "7    Total capital ratio (%)",
     {"FY2025": "15.2%", "FY2024": "14.6%", "FY2023": "15.0%", "FY2022": "16.2%"}),
    ("DATA", "     Total Capital as if IFRS 9 transitional arrangements had not been applied",
     {"FY2024": "14.6%", "FY2023": "14.9%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "UK 7a    Additional CET1 SREP requirements (%)",
     {"FY2025": "0.6%", "FY2024": "0.6%", "FY2023": "0.6%", "FY2022": "0.6%"}),
    ("DATA", "UK 7b    Additional AT1 SREP requirements (%)",
     {"FY2025": "0.2%", "FY2024": "0.2%", "FY2023": "0.2%", "FY2022": "0.2%"}),
    ("DATA", "UK 7c    Additional T2 SREP requirements (%)",
     {"FY2025": "0.3%", "FY2024": "0.3%", "FY2023": "0.3%", "FY2022": "0.3%"}),
    ("DATA", "UK 7d    Total SREP own funds requirements (%)",
     {"FY2025": "9.0%", "FY2024": "9.0%", "FY2023": "9.0%", "FY2022": "9.0%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "8    Capital conservation buffer (%)",
     {"FY2025": "2.5%", "FY2024": "2.5%", "FY2023": "2.5%", "FY2022": "2.5%"}),
    ("DATA", "9    Institution specific countercyclical capital buffer (%)",
     {"FY2025": "2.0%", "FY2024": "2.0%", "FY2023": "2.0%", "FY2022": "1.0%"}),
    ("DATA", "11    Combined buffer requirement (%)",
     {"FY2025": "4.5%", "FY2024": "4.5%", "FY2023": "4.5%", "FY2022": "3.5%"}),
    ("DATA", "UK 11a    Overall capital requirements (%)",
     {"FY2025": "13.5%", "FY2024": "13.5%", "FY2023": "13.5%", "FY2022": "12.5%"}),
    ("DATA", "12    CET1 available after meeting the total SREP own funds requirements (%)",
     {"FY2025": "7.8%", "FY2024": "7.2%", "FY2023": "7.7%", "FY2022": "8.95%"}),
    ("SECTION", "Leverage ratio (£m / %)", {}),
    ("DATA", "13    Total exposure measure excluding claims on central banks",
     {"FY2025": 3861.6, "FY2024": 3717.7, "FY2023": 3472.8, "FY2022": 3049.9}),
    ("DATA", "14    Leverage ratio excluding claims on central banks (%)",
     {"FY2025": "9.4%", "FY2024": "9.5%", "FY2023": "9.7%", "FY2022": "10.7%"}),
    ("DATA", "     Leverage ratio excluding claims on central banks (%) as if IFRS 9 transitional arrangements had not been applied",
     {"FY2024": "9.5%", "FY2023": "9.7%"}),
    ("SECTION", "Liquidity Coverage Ratio (£m / %)", {}),
    ("DATA", "15    Total high-quality liquid assets (HQLA) (Weighted value -average)",
     {"FY2025": 443.2, "FY2024": 427.2, "FY2023": 358.0, "FY2022": 283.6}),
    ("DATA", "UK 16a    Cash outflows - Total weighted value",
     {"FY2025": 416.4, "FY2024": 383.3, "FY2023": 355.1, "FY2022": 298.3}),
    ("DATA", "UK 16b    Cash inflows - Total weighted value",
     {"FY2025": 182.7, "FY2024": 184.4, "FY2023": 181.1, "FY2022": 187.3}),
    ("DATA", "16    Total net cash outflows (adjusted value)",
     {"FY2025": 233.7, "FY2024": 198.9, "FY2023": 174.0, "FY2022": 112.6}),
    ("DATA", "17    Liquidity coverage ratio (%)",
     {"FY2025": "190.4%", "FY2024": "219.6%", "FY2023": "208.0%", "FY2022": "270.1%"}),
    ("SECTION", "Net Stable Funding Ratio (£m / %)", {}),
    ("DATA", "18    Total available stable funding", {"FY2023": 3255.4, "FY2022": 2820.5}),
    ("DATA", "19    Total required stable funding", {"FY2023": 2266.1, "FY2022": 1846.3}),
    ("DATA", "20    NSFR ratio (%)", {"FY2023": "143.6%", "FY2022": "152.8%"}),
    ("SECTION",
     "FY2021, FY2020 AND FY2019: NO KM1 TEMPLATE PUBLISHED - those editions print a short unnumbered "
     "'Key Prudential Metrics' summary that fails the row-set test (see the source note below). Left blank, "
     "never back-filled from that summary or from the statutory accounts.", {}),
    ("SECTION", "EARLIER EU/BASEL KM1 (FY2018 and FY2017 editions, column a = year end) - Available capital (amounts) (£m)", {}),
    ("DATA", "1    Common Equity Tier 1 (CET1)", {"FY2018": 251.8, "FY2017": 238.9}),
    # FY2017 prints a literal "-" on every fully-loaded twin (1a/2a/3a/5a/6a/7a/14a):
    # the Group had not yet made the IFRS 9 transitional election, so the fully-loaded
    # measure did not apply to it. Read 2026-09-18 from the FY2017 edition's own
    # section 2.2 "Key Metrics", printed page 5, column a (31-Dec-17). Note the
    # contrast in that SAME table: rows 9 and 10 print "0.0%", a measured zero, and
    # they stay numeric. One table, both glyphs - do not tidy either into the other.
    ("DATA", "1a    Fully loaded ECL accounting model CET1", {"FY2018": 227.3, "FY2017": "-"}),
    ("DATA", "2    Tier 1 capital", {"FY2018": 251.8, "FY2017": 238.9}),
    ("DATA", "2a    Fully loaded ECL accounting model Tier 1", {"FY2018": 227.3, "FY2017": "-"}),
    ("DATA", "3    Total capital", {"FY2018": 297.5, "FY2017": 243.3}),
    ("DATA", "3a    Fully loaded ECL accounting model total capital", {"FY2018": 273.0, "FY2017": "-"}),
    ("SECTION", "Risk weighted assets (amount) (£m)", {}),
    ("DATA", "4    Total risk weighted assets (RWA)", {"FY2018": 1824.6, "FY2017": 1446.1}),
    ("SECTION", "Risk based capital ratios as a percentage of RWA", {}),
    ("DATA", "5    Common Equity Tier 1 (CET1) ratio (%)", {"FY2018": "13.8%", "FY2017": "16.5%"}),
    ("DATA", "5a    Fully loaded ECL accounting model CET1 (%)", {"FY2018": "12.5%", "FY2017": "-"}),
    ("DATA", "6    Tier 1 ratio (%)", {"FY2018": "13.8%", "FY2017": "16.5%"}),
    ("DATA", "6a    Fully loaded ECL accounting model Tier 1 ratio (%)", {"FY2018": "12.5%", "FY2017": "-"}),
    ("DATA", "7    Total capital ratio (%)", {"FY2018": "16.3%", "FY2017": "16.8%"}),
    ("DATA", "7a    Fully loaded ECL accounting model total capital ratio (%)", {"FY2018": "15.0%", "FY2017": "-"}),
    ("SECTION", "Additional CET1 buffer requirements as a percentage of RWA", {}),
    ("DATA", "8    Capital conservation buffer requirement (2.5% from 2019) (%)", {"FY2018": "1.9%", "FY2017": "1.3%"}),
    ("DATA", "9    Countercyclical buffer requirement (%)", {"FY2018": "1.0%", "FY2017": "0.0%"}),
    ("DATA", "10    Bank G-SIB and/or D-SIB additional requirements (%)", {"FY2018": "0.0%", "FY2017": "0.0%"}),
    ("DATA", "11    Total of bank CET1 specific buffer requirements (rows 8-10) (%)", {"FY2018": "2.9%", "FY2017": "1.3%"}),
    ("DATA", "12    CET1 available after meeting the bank's specific buffer requirements (%)", {"FY2018": "10.9%", "FY2017": "15.3%"}),
    ("SECTION", "Basel III leverage ratio (£m / %)", {}),
    ("DATA", "13    Total Basel III leverage ratio exposure measure", {"FY2018": 2432.8, "FY2017": 1942.7}),
    ("DATA", "14    Basel III leverage ratio (%) (row 2/row 13)", {"FY2018": "10.4%", "FY2017": "12.3%"}),
    ("DATA", "14a    Fully loaded ECL accounting model Basel III leverage ratio (%) (row 2a/row 13)", {"FY2018": "9.3%", "FY2017": "-"}),
    ("SECTION", "Liquidity Coverage Ratio (£m / %)", {}),
    ("DATA", "15    Total HQLA", {"FY2018": 211.2, "FY2017": 218.7}),
    ("DATA", "16    Total net cash outflow", {"FY2018": 33.9, "FY2017": 29.7}),
    ("DATA", "17    LCR ratio (%)", {"FY2018": "623.2%", "FY2017": "736.4%"}),
    ("SECTION", "Net Stable Funding Ratio (£m / %)", {}),
    ("DATA", "18    Total available stable funding", {"FY2018": 2245.8}),
    ("DATA", "19    Total required stable funding", {"FY2018": 1523.1}),
    ("DATA", "20    NSFR ratio", {"FY2018": "147.4%"}),
]

KM1_SOURCES = (
    "Sources - Secure Trust Bank PLC Group key metrics templates, taken from each year's OWN Pillar 3 edition:\n"
    f"FY2025: Pillar 3 Disclosures for the year ended 31 December 2025, section 2 'Key metrics', table headed 'The table below "
    f"UK KM1/International Financial Reporting Standard ('IFRS') 9-FL presents key metrics...', printed p.4 (PDF p.5), column "
    f"'31 Dec 2025 / £million' - {P3_URLS['FY2025']}\n"
    f"FY2024: Pillar 3 Disclosures for the year ended 31 December 2024, section 2 'Key metrics', printed p.4 (PDF p.5), column "
    f"'31 Dec 2024 / £million' - {P3_URLS['FY2024']}\n"
    f"FY2023: Pillar 3 Disclosures for the year ended 31 December 2023, section 2 'Key metrics', rows 1-17 on printed p.4 (PDF "
    f"p.5) and rows 18-20 continued onto printed p.5 (PDF p.6) under a repeated column header, column '31 Dec 2023 / £million' "
    f"- {P3_URLS['FY2023']}\n"
    f"FY2022: Pillar 3 Disclosures for the year ended 31 December 2022, section 2 'Key metrics', table introduced 'The table "
    f"below UK KM1 presents key metrics...', printed p.4 (PDF p.5), column '31 Dec 2022 / £million' - {P3_URLS['FY2022']}\n"
    f"FY2018: Pillar 3 disclosures for the year ended 31 December 2018, section 2.2 'Key Metrics (at consolidated group level)', "
    f"printed p.4 (PDF p.5), column a '31-Dec-18 / £'m' - {P3_URLS['FY2018']}\n"
    f"FY2017: Pillar 3 disclosures for the year ended 31 December 2017, section 2.2 'Key Metrics (at consolidated group level)', "
    f"printed p.5 (PDF p.6), column a '31-Dec-17 / £'m' - {P3_URLS['FY2017']}\n\n"
    "FY2021, FY2020 AND FY2019 PUBLISH NO KM1 - A SOURCED NEGATIVE, NOT A GAP IN THE SEARCH. All three editions were downloaded "
    "in full (HTTP 200, Content-Type application/pdf, %PDF magic bytes confirmed) and read, not merely searched. Each prints a "
    "section headed 'Key Prudential Metrics' (FY2019/FY2020: 'Key Prudential Metrics and Risk Weighted Assets'; FY2021: 'Key "
    "metrics') whose table is SHORT AND UNNUMBERED: an 'Available capital (amounts)' block of three lines, a 'Risk based capital "
    "ratios' block of three lines, and - in FY2019 only - a two-line 'Basel III leverage ratio' block. There is no SREP block, "
    "no combined-buffer block, no row 12, no LCR rows and no NSFR rows in any of the three; FY2020 and FY2021 carry no "
    "risk-weighted-assets amount in that table at all. On the row-set test that table is a summary, not the template, so those "
    "three columns are left blank above. The extraction is demonstrably working rather than silently empty: the FY2021 text "
    "layer returns 120 occurrences of 'capital' and 118 of 'ratio' against 0 of 'km1', and pdfimages reports a single image in "
    "the file (the corporate logo), so no key-metrics table is hiding in a bitmap. Nothing has been back-filled into those years "
    "from the summary table, from the CC1/OV1 tables elsewhere in those documents, or from the statutory accounts - the "
    "individual Pillar 3 metric sheets in this workbook do source those years from CC1/OV1/LRCom, but that is a different "
    "disclosure and is not represented here as a KM1 row.\n\n"
    "TWO TEMPLATES, ONE SHEET, NO MERGING. The FY2018 and FY2017 block is the earlier EU/Basel 'Key Metrics' template, not the "
    "UK KM1. Its row numbering is the same for rows 1-20 but its content is not comparable at three points: (a) rows 13/14 are "
    "the Basel III leverage ratio, whose exposure measure INCLUDES claims on central banks, against the UK basis above which "
    "excludes them from 1 January 2022; (b) rows 15-17 are a period observation of HQLA over net cash outflow, against the "
    "twelve-month average of month-end observations the UK KM1 requires; (c) both editions footnote row 4 - 'Total Risk Exposure "
    "(TRE) has been reported in row 4 rather than Risk Weighted Assets (RWA). TRE represents RWA plus the Operational Risk "
    "component.' The figure is reproduced exactly as printed under the label the document uses. That older table also prints "
    "FIVE QUARTERLY COLUMNS (a = the year end, b-d = the preceding quarter ends, e = the prior year end); only column a is "
    "transcribed, because only column a is that edition's reporting date. The FY2018 edition's column e therefore repeats "
    "31-Dec-17 and the FY2017 edition's column e carries 31-Dec-16, and neither is used.\n\n"
    "DASHES AND ABSENT ROWS. In the FY2017 edition the fully-loaded twins 1a/2a/3a/5a/6a/7a/14a are printed as '-' (the Group "
    "had not yet made the IFRS 9 transitional election), and those cells CARRY that dash rather than being blanked: the Group "
    "printed something there, and what it printed means 'this does not apply to us', which is a different statement from never "
    "having disclosed the row at all. A dash is still never turned into a zero, and - just as importantly - a zero is never "
    "turned into a dash: rows 9 and 10 of that same FY2017 table print '0.0%' and are kept as the measured zeros they are. "
    "Re-read at source 2026-09-18, section 2.2 'Key Metrics', printed page 5, column a. Rows 18-20 are "
    "not printed at all in the FY2017 edition - the FY2018 edition explains why: 'The Net Stable Funding Ratio (NSFR) is "
    "required to be disclosed from 30 June 2018 onwards.' The FY2024 and FY2025 editions likewise print no rows 18-20, because "
    "the Group joined the SDDT regime in H2 2024 and moved to the reduced SDDT template (FRN 204550 holds PRA Disclosure (CRR) "
    "Rule 3.1 and 3.2 permissions, both dated 09/07/2024); it nonetheless continued to publish full annual and half-year Pillar "
    "3 editions. The FY2025 edition also prints no IFRS 9-FL twin rows, stating its figures are 'reported without the "
    "application of Article 473a IFRS 9 transitional arrangements'. Secure Trust Bank omits UK 8a, UK 9a, 10, UK 10a and "
    "14a-14e from the UK KM1 entirely, as its own p.3 says it will: 'where specific rows and columns in the tables prescribed "
    "by the PRA are not applicable, these are omitted'. Those rows are absent above rather than shown empty, so the sheet "
    "reproduces which rows the Bank printed.\n\n"
    "OWN-EDITION FIGURES, NOT LATER COMPARATIVES - AND THE FY2022 DIVERGENCE IS REAL. The FY2022 column above is the FY2022 "
    "edition's own 31 December 2022 figures. The FY2023 edition reprints that date as a column headed 'Restated1' with "
    "different numbers, following a change in accounting policy for Group land and buildings (now at historical cost; see its "
    "footnote 1 and note 1.3 of the 2023 Annual Report). Both are correct on their own basis; the divergences are CET1 and Tier "
    "1 capital 327.4 own-edition against 326.9 restated, Total capital 377.3 against 376.8, Total RWEAs 2,335.0 against "
    "2,334.6, Total capital ratio 16.2% against 16.1%, row 13 total exposure measure 3,049.9 against 3,049.4, and row 12 8.95% "
    "against 8.9%. Every other row of that date agrees digit-for-digit between the two editions. The own-edition figure is kept "
    "above and the restated one is recorded here rather than written over it.\n\n"
    "THE FY2021 COLUMN IS BLANK EVEN THOUGH A LATER EDITION PRINTS ONE - AND HERE IS WHAT IT PRINTS. The FY2022 edition's UK "
    "KM1 carries a third column headed '31 Dec 2021', populated for rows 1-12 only: CET 1 capital 303.6, Tier 1 capital 303.6, "
    "Total capital 350.6, Total RWEAs 2,087.4, CET 1 ratio 14.5%, Tier 1 ratio 14.5%, Total capital ratio 16.8%, UK 7a 0.6%, UK "
    "7b 0.2%, UK 7c 0.3%, UK 7d 9.0%, row 8 2.5%, row 9 0.0%, row 11 2.5%, UK 11a 12.0%, row 12 9.48%; rows 13-20 are empty "
    "there, because that edition's footnote 1 says 'Ratios and figures requiring disclosure for the first time under new PS22/21 "
    "guidance from 1 January 2022 do not include comparatives', and its footnote 2 says the 2021 figures 'are based on rules "
    "applicable prior to 1 January 2022 (CRR regulation no 575/2013)'. Those values are recorded here and NOT written into the "
    "FY2021 column above, because a KM1 column on this sheet asserts what the Bank published as its own key-metrics template for "
    "that year, and for 2021 it published none. The comparative is quoted so the choice is visible and reversible rather than "
    "silent.\n\n"
    "SOURCE ARITHMETIC IN THE FY2022 LCR BLOCK. That edition's UK 16a (298.3) less UK 16b (187.3) is 111.0, against the 112.6 "
    "it prints on row 16. The published figures are reproduced unchanged; the LCR cap on inflows (75% of outflows) does not "
    "explain the difference at these values, so this is recorded as a defect in the source, not reconciled.\n\n"
    "HALF-YEAR EDITIONS AS A SECOND OPINION, CHECKED 2026-09-16. Secure Trust Bank publishes an interim Pillar 3 each year "
    "carrying the same template with a 30 June column, and every annual edition above reprints that same 30 June date as its "
    "middle column. The two document families were compared cell by cell: all 37 populated values on this workbook's 'Interim "
    "Pillar 3' sheet (H1 2025 through H1 2022, ten metrics) agree digit-for-digit with the 30 June columns of the FY2025, "
    "FY2024, FY2023 and FY2022 annual editions - CET 1 and Tier 1 367.1 / 348.2 / 326.8 / 313.8, Total capital 432.7 / 409.7 / "
    "383.5 / 363.6, Total RWEAs 2,916.8 / 2,735.3 / 2,518.5 / 2,237.1, and the leverage and LCR rows likewise. That is an "
    "independent confirmation of a whole column of each annual edition at no extra transcription cost.\n\n"
    + ENTITY_NOTE
    + " KM1 is a Group-level template throughout; no Company-only column exists in any edition."
)

bw.add_km1_sheet(
    "Secure Trust Bank PLC - UK KM1 Key Metrics",
    "Consolidated Group basis. Two different templates, kept in separate blocks: UK KM1 (FY2025-FY2022) and the earlier "
    "EU/Basel 'Key Metrics' table (FY2018-FY2017). FY2021-FY2019 publish no template. Amounts £million; ratios per cent, "
    "as printed.",
    KM1_ROWS, KM1_SOURCES, first_col_width=86, source_height=520,
)


def metric(name, unit, data, note=None):
    bw.add_metric_sheet(name, unit, data, P3_SOURCES, note=note, first_col_width=52, source_height=230)

IFRS9_TRANSITIONAL_NOTE = (
    "FY2018-FY2020 figures are the 'including IFRS 9 transitional arrangement' basis, which is the headline basis each edition reports "
    "and the basis its own ratios are struck on. Each of those editions also discloses a 'fully loaded ECL accounting model' / 'excluding "
    "IFRS 9 transitional arrangement' variant (FY2020: CET1 and Tier 1 256.8, Total capital 301.4; FY2018: CET1 and Tier 1 227.3, Total "
    "capital 273.0); those are a parallel series and are not mixed into the row above. FY2017 predates the IFRS 9 transitional election "
    "(its 31-Dec-17 'fully loaded' column is shown as '-')."
)

metric("CET1 Capital", "£m", [("Common Equity Tier 1 capital", {"FY2025": 364.8, "FY2024": 351.4, "FY2023": 337.9, "FY2022": 327.4, "FY2021": 303.6, "FY2020": 283.7, "FY2019": 268.0, "FY2018": 251.8, "FY2017": 238.9})], IFRS9_TRANSITIONAL_NOTE)
metric("CET1 Ratio", "% of RWEA", [("CET1 ratio", {"FY2025": "12.9%", "FY2024": "12.3%", "FY2023": "12.7%", "FY2022": "14.0%", "FY2021": "14.5%", "FY2020": "14.2%", "FY2019": "12.7%", "FY2018": "13.8%", "FY2017": "16.5%"})], IFRS9_TRANSITIONAL_NOTE)
metric("Tier 1 Capital", "£m", [("Tier 1 capital", {"FY2025": 364.8, "FY2024": 351.4, "FY2023": 337.9, "FY2022": 327.4, "FY2021": 303.6, "FY2020": 283.7, "FY2019": 268.0, "FY2018": 251.8, "FY2017": 238.9})], "Secure Trust Bank has no Additional Tier 1 instruments in any disclosed year, so each edition reports Tier 1 capital equal to CET1 capital; both rows are transcribed from their own separately-stated lines (CC1 rows 29 and 45 in the FY2019/FY2020 editions, KM1 rows 1 and 2 in the FY2017/FY2018 editions), not derived from one another. " + IFRS9_TRANSITIONAL_NOTE)
metric("Tier 1 Ratio", "% of RWEA", [("Tier 1 ratio", {"FY2025": "12.9%", "FY2024": "12.3%", "FY2023": "12.7%", "FY2022": "14.0%", "FY2021": "14.5%", "FY2020": "14.2%", "FY2019": "12.7%", "FY2018": "13.8%", "FY2017": "16.5%"})], IFRS9_TRANSITIONAL_NOTE)
metric("Total Capital", "£m", [("Total capital", {"FY2025": 428.4, "FY2024": 415.7, "FY2023": 397.6, "FY2022": 377.3, "FY2021": 350.6, "FY2020": 328.8, "FY2019": 318.0, "FY2018": 297.5, "FY2017": 243.3})], IFRS9_TRANSITIONAL_NOTE)
metric("Total Capital Ratio", "% of RWEA", [("Total capital ratio", {"FY2025": "15.2%", "FY2024": "14.6%", "FY2023": "15.0%", "FY2022": "16.2%", "FY2021": "16.8%", "FY2020": "16.4%", "FY2019": "15.0%", "FY2018": "16.3%", "FY2017": "16.8%"})], IFRS9_TRANSITIONAL_NOTE)
metric("Total RWAs", "£m", [("Total RWEAs", {"FY2025": 2827.5, "FY2024": 2855.7, "FY2023": 2653.4, "FY2022": 2335.0, "FY2021": 2087.4, "FY2020": 2001.5, "FY2019": 2118.1, "FY2018": 1824.6, "FY2017": 1446.1})], "FY2017 and FY2018 are labelled 'Total risk weighted assets (RWA)' in their own KM1 tables, but both editions footnote that row: 'Total Risk Exposure (TRE) has been reported in row 4 rather than Risk Weighted Assets (RWA). TRE represents RWA plus the Operational Risk component.' The figure is transcribed exactly as published; the FY2017/FY2018 OV1 tables on the following page reach the same total (1,446.1 and 1,824.6) by summing credit and operational risk, so the label differs but the quantity is the comparable one.")

RWA_SOURCES = (
    "Sources - Secure Trust Bank PLC Group UK OV1 Overview of risk weighted exposure amounts:\n"
    f"FY2025: Pillar 3 Disclosures for the year ended 31 December 2025, Section 3, p.6 - {P3_URLS['FY2025']}\n"
    f"FY2024: Pillar 3 Disclosures for the year ended 31 December 2024, Section 3, p.6 - {P3_URLS['FY2024']}\n"
    f"FY2023: Pillar 3 Disclosures for the year ended 31 December 2023, Section 3, p.6 - {P3_URLS['FY2023']}\n"
    f"FY2022: Pillar 3 Disclosures for the year ended 31 December 2022, Section 3, p.6 - {P3_URLS['FY2022']}\n"
    f"FY2021: Pillar 3 disclosures for the year ended 31 December 2021, Section 4.5 Pillar 1 Capital Requirements table, p.14 - {P3_URLS['FY2021']}\n"
    f"FY2020: Pillar 3 disclosures for the year ended 31 December 2020, Section 4.5 Pillar 1 Capital Requirements table, p.14 - {P3_URLS['FY2020']}\n"
    f"FY2019: Pillar 3 disclosures for the year ended 31 December 2019, Section 4.4 Pillar 1 Capital Requirements table, p.10 - {P3_URLS['FY2019']}\n"
    f"FY2018: Pillar 3 disclosures for the year ended 31 December 2018, Section 2.5 table OV1 'Overview of Risk Weighted Assets', p.7, column a (31/12/18) - {P3_URLS['FY2018']}\n"
    f"FY2017: Pillar 3 disclosures for the year ended 31 December 2017, Section 2.7 table OV1 'Overview of Risk Weighted Assets', p.10, column a (31/12/17) - {P3_URLS['FY2017']}\n\n"
    + ENTITY_NOTE
    + " FY2017 and FY2018 use the pre-UK (EU) OV1 template, whose line 1 is 'Credit Risk (excluding counterparty credit risk) CCR' and line 19 'Operational "
    "risk'; both years print a literal '-' against counterparty credit risk, market risk, securitisation and the 250%-risk-weight threshold line, and the "
    "CCR and threshold cells on this sheet now REPRODUCE that dash. They previously held 0.0, which was wrong in a way worth naming: a zero asserts the Group "
    "measured those exposures and found none, whereas the dash the documents actually print says the line did not apply to it. Corrected 2026-09-18 with both "
    "editions open, each year taken from its own edition (FY2018 section 2.5, printed page 7; FY2017 section 2.7, printed page 10). Market risk and "
    "securitisation have no rows on this sheet at all, so nothing is asserted about them either way. FY2018's operational risk moved from the Basic Indicator Approach (FY2017, OV1 row 20) to the Standardised "
    "Approach (FY2018, OV1 row 21); the total is unaffected. FY2019 and FY2020 disclose the same information as an exposure-class table (Institutions, "
    "Corporates, Retail, Secured on Immovable Property, Exposures in default, Other) that already carries its own 'Credit Risk (Standardised Approach)' "
    "subtotal alongside separate counterparty credit risk and operational risk lines; those published subtotals are used directly and nothing is re-added. "
    "FY2021 predates Secure Trust Bank's adoption of the UK OV1 template - it discloses RWAs by exposure class (Central governments, Institutions, "
    "Corporates, Retail, Secured on Immovable Property, Exposures in default, Other, Items associated with a particular high risk) rather than by risk type; "
    "these have been mapped to a single 'Credit Risk (Standardised Approach)' line for comparability with FY2022 onward, matching the Pillar 3 document's own "
    "subtotal. 'Amounts below the thresholds for deduction' (FY2022-25) is a memo/information line excluded from the Total per the source template's own "
    "footnote, not summed into RWAs."
)

RWA_ROWS = [
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 2521.0, "FY2024": 2561.0, "FY2023": 2368.8, "FY2022": 2062.4, "FY2021": 1826.6, "FY2020": 1758.1, "FY2019": 1905.0, "FY2018": 1653.5, "FY2017": 1278.6}),
    # FY2018 and FY2017 previously carried 0.0 here, but neither document prints a
    # zero: both print a literal "-" on OV1 row 4. Corrected 2026-09-18 with both
    # editions in hand, each year read from its OWN edition - FY2018 from the FY2018
    # edition's section 2.5 "Overview of Risk Weighted Assets", printed page 7, and
    # FY2017 from the FY2017 edition's section 2.7 OV1, printed page 10, column a in
    # each case. A fabricated zero asserts the Group measured counterparty credit
    # risk and found none; the dash says the line did not apply to it. The footing
    # still reconciles because a lone dash reads as nil to the checker.
    ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 0.8, "FY2024": 10.7, "FY2023": 12.1, "FY2022": 8.1, "FY2021": 2.3, "FY2020": 2.6, "FY2019": 1.7, "FY2018": "-", "FY2017": "-"}),
    ("DATA", "Operational risk", {"FY2025": 305.7, "FY2024": 284.0, "FY2023": 272.5, "FY2022": 264.5, "FY2021": 258.5, "FY2020": 240.8, "FY2019": 211.4, "FY2018": 171.1, "FY2017": 167.5}),
    ("TOTAL", "Total RWEAs", {"FY2025": 2827.5, "FY2024": 2855.7, "FY2023": 2653.4, "FY2022": 2335.0, "FY2021": 2087.4, "FY2020": 2001.5, "FY2019": 2118.1, "FY2018": 1824.6, "FY2017": 1446.1}),
    # FY2018 and FY2017 carry a printed "-" on OV1 row 23 in their own editions
    # (pp.7 and 10 respectively), so those two cells hold the dash. FY2021-FY2019
    # stay BLANK: those editions were not read for this, and an unread year is not
    # evidence of a dash. The row's position is unchanged - see the GA-012 note.
    ("DATA", "Memo: amounts below thresholds for deduction (not summed into Total)", {"FY2025": 8.9, "FY2024": 8.3, "FY2023": 10.7, "FY2022": 4.0, "FY2018": "-", "FY2017": "-"}),
]

bw.add_rwa_breakdown_sheet(
    "Secure Trust Bank PLC - Group RWA Breakdown",
    "Consolidated Group basis, £million; UK OV1 Overview of risk weighted exposure amounts (FY2021 uses the pre-OV1 exposure-class table).",
    RWA_ROWS, RWA_SOURCES, first_col_width=64, source_height=260, unit_suffix=" (£m)",
)

LEVERAGE_BASIS_NOTE = (
    "TWO DIFFERENT SERIES, DELIBERATELY KEPT ON SEPARATE ROWS - do not merge them into one line and do not read a trend across the break. "
    "FY2021-FY2025 are the UK leverage ratio, whose exposure measure EXCLUDES qualifying claims on central banks (the UK leverage framework "
    "exemption). FY2017-FY2020 predate that framework: those editions disclose the Basel III / CRR leverage ratio, whose exposure measure "
    "INCLUDES central bank claims, computed as Tier 1 capital divided by the total leverage ratio exposure (FY2020 2,733.5; FY2019 2,740.8; "
    "FY2018 2,432.8; FY2017 1,942.7). Because Secure Trust holds a large Bank of England reserve account, the two bases are not comparable: "
    "the older basis is structurally the more conservative of the two, so the apparent step between FY2020 and FY2021 is a definitional "
    "change, not a movement in leverage.\n"
    "RESTATEMENT NOTED, NOT OVERWRITTEN: the FY2020 edition footnotes FY2019's leverage ratio as 9.7%, 'Previously disclosed as 9.8%, which "
    "has been restated' (exposure measure restated 2,740.8 -> 2,772.7). The FY2019 cell above keeps that year's own published 9.8%. The "
    "FY2019 edition likewise restates FY2018 to 9.5% on an exposure measure of 2,539.0, against the 10.4% on 2,432.8 that FY2018's own "
    "edition published and that is used above."
)

metric("Leverage Ratio", "%", [
    ("Leverage ratio excluding claims on central banks (UK leverage framework)", {"FY2025": "9.4%", "FY2024": "9.5%", "FY2023": "9.7%", "FY2022": "10.7%", "FY2021": "10.3%"}),
    ("Basel III / CRR leverage ratio, exposure measure including claims on central banks", {"FY2020": "10.4%", "FY2019": "9.8%", "FY2018": "10.4%", "FY2017": "12.3%"}),
], LEVERAGE_BASIS_NOTE)

LCR_BASIS_NOTE = (
    "TWO DIFFERENT SERIES, DELIBERATELY KEPT ON SEPARATE ROWS. FY2022-FY2025 are the UK KM1 Liquidity Coverage Ratio, which is a TWELVE-MONTH "
    "AVERAGE of month-end observations, as the UK KM1 template requires. FY2017 and FY2018 come from the pre-UK Basel III KM1 'Liquidity "
    "Coverage Ratio' block (rows 15-17) of those years' own editions, which reports a period observation of total HQLA over total net cash "
    "outflow (FY2018: HQLA 211.2 / net outflow 33.9; FY2017: HQLA 218.7 / net outflow 29.7) rather than a twelve-month average. Averaging a "
    "point observation against an average series would be a false comparison, so the two are never placed on one row and the fall from 736.4% "
    "to 270.1% across the gap must not be read as a trend.\n"
    "FY2019, FY2020 AND FY2021 ARE A GENUINE DISCLOSURE GAP, NOT A RETRIEVAL FAILURE (checked 2026-09-15). The FY2019, FY2020 and FY2021 "
    "Pillar 3 editions were downloaded in full and searched: the strings 'LCR', 'Liquidity Coverage', 'HQLA' and 'Net Stable Funding' return "
    "no liquidity metric table in FY2019 or FY2020 at all, and FY2021's key-metrics table carries no LCR line. The FY2020 edition's Section 10 "
    "'Liquidity and Funding Risk' contains only narrative and cross-refers the reader to note 37 of the 2020 Annual Report and Accounts instead. "
    "No annual-report point-in-time proxy has been substituted for any of those three years."
)

metric("LCR", "%", [
    ("Liquidity Coverage Ratio - UK KM1 twelve-month average", {"FY2025": "190.4%", "FY2024": "219.6%", "FY2023": "208.0%", "FY2022": "270.1%", "FY2021": "Not publicly disclosed", "FY2020": "Not publicly disclosed", "FY2019": "Not publicly disclosed"}),
    ("Liquidity Coverage Ratio - Basel III KM1 period observation", {"FY2018": "623.2%", "FY2017": "736.4%"}),
], LCR_BASIS_NOTE)
SDDT_NSFR_NOTE = (
    "FY2024 and FY2025 are STRUCTURALLY EXEMPT, not a sourcing failure (established 2026-09-15, cross-bank "
    "SDDT pass). Secure Trust Bank is a Small Domestic Deposit Taker ('SDDT') and its Pillar 3 disclosures "
    "are now produced on the reduced SDDT template, which drops the NSFR; the SDDT regime also replaces the "
    "full NSFR with a Simplified Retail Deposit Ratio. NSFR does not appear anywhere in either the FY2024 or "
    "the FY2025 Pillar 3 disclosure (both downloaded and searched in full - readable text layers, 12 pages "
    "each, zero occurrences of 'NSFR' or 'Net Stable Funding'), so there is no figure to find.\n"
    "The Group says all of this in its own words. Pillar 3 Disclosure 2024, p.3: 'In H2 2024 the Group "
    "received confirmation of its successful application to join the SDDT regime with immediate effect.' Same "
    "page, on the mechanism: 'Pillar 3 disclosure requirements under the SDDT regime were confirmed in "
    "December 2023 through PS15/23 \"The Strong and Simple Framework: Scope Criteria, Liquidity and "
    "Disclosure Requirements\", which became effective from 1 July 2024.' And p.4: 'The Group's disclosures "
    "are produced in accordance with the requirements as set out in Article 433b Disclosures by Small "
    "Domestic Deposit Takers, SDDT Consolidation Entities and Small and Non-Complex Institutions of the PRA "
    "Rulebook.' The FY2025 edition carries the same CFO attestation at p.4 - disclosures prepared 'in "
    "accordance with the Disclosure (CRR) part of the PRA Rulebook, as applicable for SDDTs'.\n"
    "Corroborated by the PRA's own firm-level register - Bank of England consolidated list of waivers and "
    "modifications granted to PRA-authorised firms (downloaded 2026-09-15, "
    "https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/authorisations/"
    "waivers-and-modifications-of-rules/consolidated-waivers-pra-firms.csv) - which carries two rows for FRN "
    "204550, 'SECURE TRUST BANK PUBLIC LIMITED COMPANY': Rule 3.1 of the SDDT Regime - General Application "
    "Part (ref 'A00008217P.pdf') and Rule 3.2 (ref 'A00008218P.pdf'), BOTH with start date '09/07/2024' and "
    "no end date. That 9 July 2024 date sits immediately after PS15/23's 1 July 2024 effective date and "
    "inside the 'H2 2024' the Group describes, so register and narrative agree.\n"
    "DATE FIT: the modification took effect 9 July 2024, so it covers FY2024 and FY2025 and NOTHING earlier. "
    "FY2022 and FY2023 NSFR are disclosed above in the normal way. FY2021's blank has a completely separate "
    "and earlier cause - the UK NSFR requirement only became binding from 1 January 2022, so no FY2021 figure "
    "was ever required. Do not read the SDDT exemption back onto FY2021. The Group discloses no Simplified "
    "Retail Deposit Ratio value, so nothing is added in the NSFR's place.\n"
    "FY2018 IS NOT A BLANK EITHER (added 2026-09-15): the FY2018 Pillar 3 discloses an NSFR of 147.4% in its own key-metrics table "
    "(rows 18-20: total available stable funding 2,245.8, total required stable funding 1,523.1), and explains why FY2017 has none - "
    "'The Net Stable Funding Ratio (NSFR) is required to be disclosed from 30 June 2018 onwards.' FY2017 is therefore marked structurally "
    "not applicable rather than left blank. This 2018-vintage NSFR is the Basel III / CRR II definition disclosed voluntarily ahead of the "
    "UK binding requirement; it is a point observation, not the four-quarter average of the later UK KM1 series, so it should not be read "
    "as continuous with FY2022/FY2023. FY2019, FY2020 and FY2021 disclose no NSFR at all - those editions were downloaded and searched in "
    "full and contain no occurrence of 'NSFR' or 'Net Stable Funding' - so the UK requirement's 1 January 2022 start date is not the only "
    "reason for those blanks; the Group simply stopped publishing the metric after FY2018 and resumed under UK KM1 in FY2022."
)

metric("NSFR", "%", [("Net Stable Funding Ratio", {"FY2025": "Not required (SDDT)", "FY2024": "Not required (SDDT)", "FY2023": "143.6%", "FY2022": "152.8%", "FY2021": "Not publicly disclosed", "FY2020": "Not publicly disclosed", "FY2019": "Not publicly disclosed", "FY2018": "147.4%", "FY2017": "Not applicable"})], SDDT_NSFR_NOTE)
metric("MREL Ratio", "%", [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})], (
    "No quantitative MREL ratio was located in the reviewed annual reports or Pillar 3 disclosures. This is a SOURCED negative for "
    "FY2017-FY2020, not merely an unsearched gap: each of those four Pillar 3 editions addresses MREL directly and in the same terms - "
    "the Group's Total Loss Absorbing Capacity equals its Pillar 1 + Pillar 2A capital requirement, and 'The Group is not required by the "
    "PRA to hold a MREL recapitalisation reserve' (FY2017 Section 4 p.13; FY2018 p.10; FY2019 Section 4.1 p.7; FY2020 Section 4 p.15, which "
    "spells out 'Minimum Requirement for own funds and Eligible Liabilities'). A firm with no recapitalisation-reserve requirement has no "
    "MREL ratio in excess of its capital ratios to report, so the absence is a regulatory fact about the firm rather than a disclosure gap."
))

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
        ("Total assets", {"FY2025": 4316.0, "FY2024": 4116.7, "FY2023": 3778.0, "FY2022": 3380.3, "FY2021": 2885.9, "FY2020": 2664.1, "FY2019": 2682.8, "FY2018": 2444.3, "FY2017": 1891.6}),
        ("Loans and advances to customers", {"FY2025": 3295.8, "FY2024": 3608.5, "FY2023": 3315.3, "FY2022": 2919.5, "FY2021": 2530.6, "FY2020": 2358.9, "FY2019": 2450.1, "FY2018": 2028.9, "FY2017": 1598.3}),
        ("Deposits from customers", {"FY2025": 3509.6, "FY2024": 3244.9, "FY2023": 2871.8, "FY2022": 2514.6, "FY2021": 2103.2, "FY2020": 1992.5, "FY2019": 2020.3, "FY2018": 1847.7, "FY2017": 1483.2}),
        ("Total equity", {"FY2025": 374.3, "FY2024": 360.5, "FY2023": 344.5, "FY2022": 326.9, "FY2021": 302.4, "FY2020": 270.5, "FY2019": 254.1, "FY2018": 237.1, "FY2017": 249.1}),
    ], balance_sheet_unit="£m",
    income_statement_totals=[
        ("Operating income", {"FY2025": 165.2, "FY2024": 203.9, "FY2023": 184.7, "FY2022": 169.6, "FY2021": 164.5, "FY2020": 166.1, "FY2019": 165.5, "FY2018": 151.6, "FY2017": 137.5}),
        ("Operating expenses", {"FY2025": -74.7, "FY2024": -103.8, "FY2023": -99.7, "FY2022": -93.2, "FY2021": -104.0, "FY2020": -91.6, "FY2019": -94.2, "FY2018": -84.5, "FY2017": -71.6}),
        ("Net impairment charge on loans and advances", {"FY2025": -31.4, "FY2024": -61.9, "FY2023": -43.2, "FY2022": -38.2, "FY2021": -4.5, "FY2020": -51.3, "FY2019": -32.6, "FY2018": -32.4, "FY2017": -36.9}),
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
        ("CET1 Ratio", {"FY2025": "12.9%", "FY2024": "12.3%", "FY2023": "12.7%", "FY2022": "14.0%", "FY2021": "14.5%", "FY2020": "14.2%", "FY2019": "12.7%", "FY2018": "13.8%", "FY2017": "16.5%"}),
        ("Total Capital Ratio", {"FY2025": "15.2%", "FY2024": "14.6%", "FY2023": "15.0%", "FY2022": "16.2%", "FY2021": "16.8%", "FY2020": "16.4%", "FY2019": "15.0%", "FY2018": "16.3%", "FY2017": "16.8%"}),
        ("Leverage Ratio (UK basis, excl. central bank claims)", {"FY2025": "9.4%", "FY2024": "9.5%", "FY2023": "9.7%", "FY2022": "10.7%", "FY2021": "10.3%"}),
        ("Leverage Ratio (Basel III/CRR basis, incl. central bank claims)", {"FY2020": "10.4%", "FY2019": "9.8%", "FY2018": "10.4%", "FY2017": "12.3%"}),
        ("LCR (UK KM1 twelve-month average)", {"FY2025": "190.4%", "FY2024": "219.6%", "FY2023": "208.0%", "FY2022": "270.1%"}),
        ("LCR (Basel III KM1 period observation)", {"FY2018": "623.2%", "FY2017": "736.4%"}),
        ("NSFR", {"FY2023": "143.6%", "FY2022": "152.8%", "FY2018": "147.4%"}),
    ],
    note=(
        "Group cash flows and Group Pillar 3 metrics are deliberately kept on their respective disclosed bases. FY2021 cash uses the FY2022 restated "
        "comparative; blank regulatory cells mean not disclosed, not zero. FY2017-FY2020 regulatory figures were added 2026-09-15 from those years' own "
        "Pillar 3 editions (whose document-library slugs end '-annual', not '-final'). The leverage ratio and LCR are shown on two rows each because the "
        "FY2017-FY2020 editions predate the UK leverage framework and the UK KM1 template: the older leverage denominator INCLUDES claims on central banks "
        "and the older LCR is a period observation rather than a twelve-month average. Read each row on its own; the step between the two rows is a "
        "definitional change, not a movement in the underlying position. Balance-sheet and income-statement totals for FY2017-FY2020 are each year's own "
        "originally-published figures, matching the detail sheets; equity roll-forward and cash-flow totals remain FY2021-FY2025 only because the detail "
        "sheets do not carry the earlier years."
    ),
)

bw.save("/Users/armaan/code/katalysis/banks/SECURE TRUST BANK FINANCIALS.xlsx")
