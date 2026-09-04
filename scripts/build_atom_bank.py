import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Cash flow statement only exists for FY2021-FY2022 (31 March year-end) - see
# CASH_FLOW_EXEMPTION_NOTE below. Pillar 3 covers all 5 years.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

CH_FILING_HISTORY_URL = "https://find-and-update.company-information.service.gov.uk/company/08632552/filing-history"

P3_FY21_URL = "https://www.atombank.co.uk/~/docs/pillar-3-disclosures-20-21.pdf"
P3_FY22_URL = "https://www.atombank.co.uk/~/docs/pillar-3-disclosures-21-22.pdf"
P3_FY23_URL = "https://www.atombank.co.uk/~/docs/pillar-3-disclosures-22-23.pdf"
P3_FY24_URL = "https://www.atombank.co.uk/~/docs/atom-holdco-limited-pillar-3.pdf"
P3_FY25_URL = "https://www.atombank.co.uk/~/docs/pillar-3-disclosures-24-25.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Atom Bank Plc (company 08632552, FRN 661960, matches Banks List 2608.xlsx exactly) is the "
    "PRA-authorised entity built here. During FY2023, a new non-trading holding company - Atom Holdco Limited "
    "(later re-registered Atom Holdco plc ahead of its 2025 IPO-track listing) - was inserted above Atom Bank "
    "Plc in the group structure. From that point, Atom Bank Plc became a wholly-owned subsidiary whose results "
    "are consolidated into Atom Holdco's own published financial statements, and Pillar 3 disclosures moved from "
    "being published at Bank level to being published at Holdco (Group) level, with a separate Bank-solo column "
    "shown alongside Group in the KM1 template from FY2023 onward. All Pillar 3 figures in this workbook use the "
    "Bank column (or, for FY2021-FY2022, the single pre-restructuring figure that IS the Bank, per each report's "
    "own note: 'the comparatives reflect the previous structure where Atom bank plc was the sole regulated "
    "entity') - so there is no cash-flow-vs-Pillar-3 basis mismatch here, unlike several other banks in this "
    "project."
)

CASH_FLOW_EXEMPTION_NOTE = (
    "CASH FLOW EXEMPTION NOTE: only FY2021 and FY2022 have a Statement of Cash Flows (called 'Cash flow "
    "statements' in the source, Bank column used throughout). Both Companies House filings for those years are "
    "fully scanned/image-only (0 text blocks/page), OCR'd with tesseract and cross-verified against rendered page "
    "images. From the FY2023 Annual Report onward (confirmed directly in the FY2023 and FY2025 filings - also "
    "fully scanned, OCR'd), Atom Bank Plc's accounting policies note states: 'The Bank is exempt by virtue of "
    "s400 of the Companies Act 2006 from the requirement to prepare group financial statements... The Bank is a "
    "qualifying entity as defined by Financial Reporting Standard 101... and therefore has adopted the reduced "
    "disclosure framework of FRS 101', explicitly listing 'IAS 7 Statement of cash flows' among the disclosures "
    "exempted - the same FRS 101 'qualifying entity' exemption seen elsewhere in this project (ABC International "
    "Bank, BNY Mellon, United Trust Bank, ICICI, PNBE), but here - like Tandem Bank and AIB Group (UK) - taken "
    "only from a specific year onward rather than throughout the entity's whole history. FY2023-FY2025 are left "
    "blank on the Cash Flow Statement sheet rather than guessed."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Atom Bank Plc's own Bank-column 'Cash flow statements', £'000, from its Companies "
    "House full accounts filings (Group of companies' accounts, which for FY2021/FY2022 present Group and Bank "
    "columns side by side):\n"
    f"FY2022: full accounts made up to 31 March 2022, filed 7 Sep 2022, p.65 (Cash flow statement, Bank column) - "
    f"{CH_FILING_HISTORY_URL}\n"
    f"FY2021: group of companies' accounts made up to 31 March 2021, filed 28 Sep 2021, p.48 (Cash flow "
    f"statements, Bank column) - {CH_FILING_HISTORY_URL}\n"
    "FY2021's own closing 'Cash and balances at central banks' (£316,827k) differs from FY2022's own opening "
    "figure for the same balance (£316,826k) by £1k - an immaterial rounding difference in the source documents "
    "themselves, kept as printed in each year's own report rather than force-corrected.\n\n"
    + ENTITY_NOTE + "\n\n" + CASH_FLOW_EXEMPTION_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - Atom Bank Plc (Bank-solo basis; Group basis where Bank=Group pre-restructuring, see ENTITY "
        "NOTE), Table UK KM1 - Key metrics, as at 31 March each year:\n"
        f"FY2025: Atom Holdco plc Pillar 3 Disclosures 2025, p.13 (4. Key metrics) - {P3_FY25_URL}\n"
        f"FY2024: comparative column within the FY2025 Pillar 3 Disclosures above (no separate FY2024 edition "
        f"fetched directly) - {P3_FY25_URL}\n"
        f"FY2023: Atom Holdco Limited Pillar 3 Disclosures 2023, p.12-13 (5. Key metrics) - {P3_FY23_URL}\n"
        f"FY2022: Atom Bank Plc Pillar 3 Disclosures 2021/22, p.17 (5. Key Metrics) - {P3_FY22_URL}\n"
        f"FY2021: Atom Bank Plc Pillar 3 Disclosures 2020/21, p.11 (3. Summary analysis) - {P3_FY21_URL}, "
        f"cross-checked against its identical appearance as the FY2021 comparative column in the FY2022 Pillar 3 "
        f"Disclosures above (both matched exactly).\n"
        "FY2024/FY2025 figures were originally disclosed in £m and are shown here converted to £'000 (x1,000) "
        "for consistency with FY2021-FY2023's own £'000 presentation - ratios are unaffected by this unit change."
        + extra
    )


bw = BankWorkbook(bank_name="Atom Bank Plc", years=YEARS, year_label=YEAR_LABEL, header_color="146C94")

AR25_URL = "https://find-and-update.company-information.service.gov.uk/company/08632552/filing-history/MzQ3NzYwODYzOWFkaXF6a2N4/document?format=pdf&download=0"
AR24_URL = "https://find-and-update.company-information.service.gov.uk/company/08632552/filing-history/MzQzNDkxNDM0M2FkaXF6a2N4/document?format=pdf&download=0"
AR23_URL = "https://find-and-update.company-information.service.gov.uk/company/08632552/filing-history/MzM5ODE2MjM5N2FkaXF6a2N4/document?format=pdf&download=0"
AR21_URL = "https://find-and-update.company-information.service.gov.uk/company/08632552/filing-history/MzMxNDk5MDE0OWFkaXF6a2N4/document?format=pdf&download=0"

STATEMENT_ENTITY_NOTE = (
    "Bank (solo) basis throughout - the same basis as the pre-existing Cash Flow Statement and Pillar 3 sheets "
    "(see ENTITY NOTE below and on those sheets). FY2025/FY2024 come from the Atom Bank Plc full accounts filed "
    "with the FY2025 Companies House filing (Statement of financial position/Statement of comprehensive income/ "
    "Statement of changes in equity, pp.54-56), which is scanned/image-only - transcribed via page-render + "
    "visual reading rather than left blank, per the ABC International Bank precedent. FY2023/FY2022 come from "
    "the FY2023 filing (pp.52-54), also scanned/image-only. FY2021 comes from the FY2021 filing (pp.44-47, "
    "double-page-spread layout), Bank column (the Group column is not used, matching every other sheet's Bank "
    "basis)."
    "\n\n" + ENTITY_NOTE
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 1902200, "FY2024": 2405000, "FY2023": 4177488, "FY2022": 1453596, "FY2021": 316826}),
    ("DATA", "Debt instruments at fair value through other comprehensive income", {"FY2025": 1384500, "FY2024": 474700, "FY2023": 323978, "FY2022": 297334, "FY2021": 151052}),
    ("DATA", "Debt instruments held at amortised cost", {"FY2025": 202500, "FY2024": 23000, "FY2023": 150273, "FY2022": 295103, "FY2021": 649503}),
    ("DATA", "Derivatives held for hedging purposes", {"FY2025": 55800, "FY2024": 62400, "FY2023": 76882, "FY2022": 36021, "FY2021": 4058}),
    ("DATA", "Loans and advances to customers", {"FY2025": 5301500, "FY2024": 4100900, "FY2023": 2958769, "FY2022": 2384066, "FY2021": 1638851}),
    ("DATA", "Other assets", {"FY2025": 76700, "FY2024": 100100, "FY2023": 63182, "FY2022": 46845, "FY2021": 26077}),
    ("DATA", "Property, plant and equipment", {"FY2025": 600, "FY2024": 700, "FY2023": 3180, "FY2022": 4068, "FY2021": 4865}),
    ("DATA", "Intangible assets", {"FY2025": 38000, "FY2024": 41600, "FY2023": 37829, "FY2022": 36129, "FY2021": 35889}),
    ("DATA", "Deferred tax asset", {"FY2025": 29100, "FY2024": 16500, "FY2023": 9800, "FY2022": 5353}),
    ("TOTAL", "Total assets", {"FY2025": 8990900, "FY2024": 7224900, "FY2023": 7801381, "FY2022": 4558515, "FY2021": 2827121}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer deposits", {"FY2025": 7538700, "FY2024": 5746200, "FY2023": 6551325, "FY2022": 3229796, "FY2021": 2154419}),
    ("DATA", "Borrowings from central banks", {"FY2025": 358200, "FY2024": 683800, "FY2023": 681403, "FY2022": 675749, "FY2021": 378093}),
    ("DATA", "Deemed loan", {"FY2025": 556100, "FY2024": 322400, "FY2023": 186864, "FY2022": 343856, "FY2021": 110700}),
    ("DATA", "Subordinated liabilities", {"FY2025": 50100, "FY2024": 0, "FY2023": 8201, "FY2022": 8192, "FY2021": 8180}),
    ("DATA", "Derivatives held for hedging purposes", {"FY2025": 200, "FY2024": 1100, "FY2023": 0, "FY2022": 108, "FY2021": 4422}),
    ("DATA", "Provisions", {"FY2025": 900, "FY2024": 800, "FY2023": 425, "FY2022": 310, "FY2021": 197}),
    ("DATA", "Other liabilities", {"FY2025": 61500, "FY2024": 66800, "FY2023": 88532, "FY2022": 49410, "FY2021": 29780}),
    ("TOTAL", "Total liabilities", {"FY2025": 8565700, "FY2024": 6821100, "FY2023": 7516750, "FY2022": 4307421, "FY2021": 2685791}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital and share premium", {"FY2025": 128900, "FY2024": 128900, "FY2023": 29305, "FY2022": 566378, "FY2021": 448935}),
    ("DATA", "Other reserves", {"FY2025": 49200, "FY2024": 44700, "FY2023": 37379, "FY2022": 26875, "FY2021": 22627}),
    ("DATA", "Accumulated gains/(losses)", {"FY2025": 247100, "FY2024": 230200, "FY2023": 217947, "FY2022": -342159, "FY2021": -330232}),
    ("TOTAL", "Total equity", {"FY2025": 425200, "FY2024": 403800, "FY2023": 284631, "FY2022": 251094, "FY2021": 141330}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 8990900, "FY2024": 7224900, "FY2023": 7801381, "FY2022": 4558515, "FY2021": 2827121}),
]

BALANCE_SHEET_SOURCES = (
    "Sources - Statement of financial position, Bank basis, £'000:\n"
    f"FY2025/FY2024: Atom Bank Plc full accounts made up to 31 March 2025, p.55 - {AR25_URL}\n"
    f"FY2023/FY2022: Atom Bank Plc full accounts made up to 31 March 2023, p.53 - {AR23_URL}\n"
    f"FY2021: Atom Bank Plc full accounts made up to 31 March 2021, p.45 (Bank column) - {AR21_URL}\n"
    "FY2021's Bank statement carries no 'Deferred tax asset' line at all (Note 9 confirms no deferred tax asset "
    "was recognised that year - the Board only concluded it was appropriate to start recognising one from "
    "FY2022) - left blank rather than assumed zero. FY2021's Bank statement also carried a 'Debt securities in "
    "issue' line (£nil for Bank, £141,357k for Group) which no other year's statement shows - omitted as a "
    "row here since it is nil on the Bank basis used throughout, consistent with every other year."
    "\n\n" + STATEMENT_ENTITY_NOTE
)

bw.add_balance_sheet_sheet(
    title="Atom Bank Plc - Statement of Financial Position",
    subtitle="Bank (solo) basis, £'000",
    rows=balance_sheet_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=62,
    source_height=220,
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 441700, "FY2024": 440900, "FY2023": 208467, "FY2022": 76836, "FY2021": 42262}),
    ("DATA", "Interest expense", {"FY2025": -340400, "FY2024": -341800, "FY2023": -133218, "FY2022": -33566, "FY2021": -30199}),
    ("TOTAL", "Net interest income", {"FY2025": 101300, "FY2024": 99100, "FY2023": 75249, "FY2022": 43270, "FY2021": 12063}),
    ("DATA", "Net fee and commission expense", {"FY2021": -1072}),
    ("DATA", "Gain on disposal of assets held at amortised cost", {"FY2023": 0, "FY2022": 1749}),
    ("DATA", "Loss on disposal of assets held at amortised cost", {"FY2021": -9241}),
    ("DATA", "Other income", {"FY2023": 3083, "FY2022": 4099}),
    ("DATA", "Other expense", {"FY2025": -700, "FY2024": 0}),
    ("DATA", "Other income/(expense)", {"FY2021": 188}),
    ("DATA", "Credit impairment charges", {"FY2025": -7100, "FY2024": -11000, "FY2023": -12768, "FY2022": -1100, "FY2021": -3652}),
    ("TOTAL", "Net operating income/(expense)", {"FY2025": 93500, "FY2024": 88100, "FY2023": 65564, "FY2022": 48018, "FY2021": -1714}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Staff costs", {"FY2025": -36900, "FY2024": -32700, "FY2023": -31347, "FY2022": -25882, "FY2021": -24183}),
    ("DATA", "Administrative and general expenses", {"FY2025": -31500, "FY2024": -28800, "FY2023": -27781, "FY2022": -24300, "FY2021": -22946}),
    ("TOTAL", "Staff and administrative expense", {"FY2025": -68400, "FY2024": -61500, "FY2023": -59128, "FY2022": -50182, "FY2021": -47129}),
    ("TOTAL", "Profit/(loss) before other charges", {"FY2025": 25100, "FY2024": 26600, "FY2023": 6436, "FY2022": -2164, "FY2021": -48843}),
    ("SECTION", "Other charges", {}),
    ("DATA", "Amortisation, depreciation and intangible impairment", {"FY2025": -13900, "FY2024": -12700, "FY2023": -11273, "FY2022": -10531, "FY2021": -10443}),
    ("DATA", "Platform transformation costs", {"FY2021": -596}),
    ("DATA", "Equity-settled share-based payments", {"FY2025": -6100, "FY2024": -7200, "FY2023": -5233, "FY2022": -4585, "FY2021": -2497}),
    ("TOTAL", "Other charges", {"FY2025": -20000, "FY2024": -19900, "FY2023": -16506, "FY2022": -15116, "FY2021": -13536}),
    ("TOTAL", "Profit/(loss) before taxation", {"FY2025": 5100, "FY2024": 6700, "FY2023": -10070, "FY2022": -17280}),
    ("DATA", "Taxation credit/(expense)", {"FY2025": 11800, "FY2024": 5600, "FY2023": 4447, "FY2022": 5353}),
    ("TOTAL", "Profit/(loss) for the year", {"FY2025": 16900, "FY2024": 12300, "FY2023": -5623, "FY2022": -11927, "FY2021": -62379}),
    ("SECTION", "Other comprehensive income/(expense), net of tax", {}),
    ("DATA", "Net (loss)/gain in fair value (fair value reserve)", {"FY2025": -400, "FY2024": 500, "FY2023": 117, "FY2022": -388, "FY2021": 725}),
    ("DATA", "Net amount transferred to profit or loss (fair value reserve)", {"FY2025": 200, "FY2024": 100, "FY2023": -9, "FY2022": 51, "FY2021": -16}),
    ("DATA", "Net (losses)/gains from changes in fair value (cash flow hedge reserve)", {"FY2025": -1300, "FY2024": -400, "FY2023": 5163}),
    ("TOTAL", "Other comprehensive income/(expense), net of tax", {"FY2025": -1500, "FY2024": 200, "FY2023": 5271, "FY2022": -337, "FY2021": 709}),
    ("TOTAL", "Total comprehensive income/(expense) for the year", {"FY2025": 15400, "FY2024": 12500, "FY2023": -352, "FY2022": -12264, "FY2021": -61670}),
]

INCOME_STATEMENT_SOURCES = (
    "Sources - Statement of comprehensive income, Bank basis, £'000:\n"
    f"FY2025/FY2024: Atom Bank Plc full accounts made up to 31 March 2025, p.54 - {AR25_URL}\n"
    f"FY2023/FY2022: Atom Bank Plc full accounts made up to 31 March 2023, p.52 - {AR23_URL}\n"
    f"FY2021: Atom Bank Plc full accounts made up to 31 March 2021, p.44 (Bank column) - {AR21_URL}\n"
    "PRESENTATION NOTE: the line-item structure changes materially across report vintages, kept as each year's "
    "own report presents it rather than forced into one shape - 'Net fee and commission expense' and 'Platform "
    "transformation costs' appear only in the FY2021 report; 'Loss on disposal of assets held at amortised "
    "cost' (FY2021, a genuine loss) is a different line from 'Gain on disposal of assets held at amortised "
    "cost' (FY2022/FY2023, a genuine gain, FY2023 nil); 'Other income' (FY2023/FY2022, a broader ~£3-4m income "
    "note aggregating fee income, hedge ineffectiveness and other items) is conceptually distinct from the "
    "small 'Other expense' line shown FY2025/FY2024 (-£0.7m/nil) and from FY2021's 'Other income/(expense)' "
    "(£0.19m) - all three are kept as separate rows rather than merged. FY2021's report shows 'Loss before and "
    "after taxation' as a single combined row with no separate pre-tax/taxation split (tax was nil that year) - "
    "'Profit/(loss) before taxation' and 'Taxation credit/(expense)' are left blank for FY2021 as a result, "
    "matching that report's own presentation. 'Total comprehensive income/(expense) for the year' is the one "
    "row genuinely comparable and populated across all 5 years."
    "\n\n" + STATEMENT_ENTITY_NOTE
)

bw.add_income_statement_sheet(
    title="Atom Bank Plc - Statement of Comprehensive Income",
    subtitle="Bank (solo) basis, £'000",
    rows=income_statement_rows,
    sources_text=INCOME_STATEMENT_SOURCES,
    first_col_width=68,
    source_height=260,
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
EQUITY_HEADERS = [
    "Share capital and share premium", "Fair value reserve", "Cash flow hedge reserve",
    "Share-based payment reserve", "Accumulated gains/(losses)", "Total equity",
]

equity_changes_rows = [
    ("TOTAL", "Balance as at 1 April 2020 (opening FY2021)", (448935, -433, None, 19854, -267853, 200503)),
    ("DATA", "Loss for the year (FY2021)", (None, None, None, None, -62379, -62379)),
    ("DATA", "Net gain in fair value", (None, 725, None, None, None, 725)),
    ("DATA", "Net amount transferred to profit or loss", (None, -16, None, None, None, -16)),
    ("TOTAL", "Total comprehensive income/(expense) (FY2021)", (None, 709, None, None, -62379, -61670)),
    ("DATA", "Share schemes - value of employee services", (None, None, None, 2497, None, 2497)),
    ("TOTAL", "Balance as at 31 March 2021", (448935, 276, None, 22351, -330232, 141330)),
    ("DATA", "Loss for the year (FY2022)", (None, None, None, None, -11927, -11927)),
    ("DATA", "Net loss in fair value", (None, -388, None, None, None, -388)),
    ("DATA", "Net amount transferred to profit or loss", (None, 51, None, None, None, 51)),
    ("TOTAL", "Total comprehensive expense (FY2022)", (None, -337, None, None, -11927, -12264)),
    ("DATA", "Issue of new ordinary shares, net of transaction costs", (117443, None, None, None, None, 117443)),
    ("DATA", "Share schemes - value of employee services", (None, None, None, 4585, None, 4585)),
    ("TOTAL", "Balance as at 31 March 2022", (566378, -61, None, 26936, -342159, 251094)),
    ("DATA", "Loss for the year (FY2023)", (None, None, None, None, -5623, -5623)),
    ("DATA", "Net gain in fair value", (None, 117, None, None, None, 117)),
    ("DATA", "Hedging adjustment (cash flow hedge reserve)", (None, None, 5163, None, None, 5163)),
    ("DATA", "Net amount transferred to profit or loss", (None, -9, None, None, None, -9)),
    ("TOTAL", "Total comprehensive income/(expense) (FY2023)", (None, 108, 5163, None, -5623, -352)),
    ("DATA", "Issue of new ordinary shares, net of transaction costs", (28656, None, None, None, None, 28656)),
    ("DATA", "Share premium reduction", (-565729, None, None, None, 565729, 0)),
    ("DATA", "Share schemes - value of employee services", (None, None, None, 5233, None, 5233)),
    ("TOTAL", "Balance as at 31 March 2023 (per FY2023 report)", (29305, 47, 5163, 32169, 217947, 284631)),
    ("TOTAL", "Balance as at 1 April 2023 (per FY2025 report - restated)", (29300, 0, 5200, 32100, 217900, 284500)),
    ("DATA", "Profit for the year (FY2024)", (None, None, None, None, 12300, 12300)),
    ("DATA", "Net gain in fair value", (None, 500, None, None, None, 500)),
    ("DATA", "Hedging adjustment (cash flow hedge reserve)", (None, None, -400, None, None, -400)),
    ("DATA", "Net amount transferred to profit or loss", (None, 100, None, None, None, 100)),
    ("TOTAL", "Total comprehensive income (FY2024)", (None, 600, -400, None, 12300, 12500)),
    ("DATA", "Issue of new ordinary shares, net of transaction costs", (99600, None, None, None, None, 99600)),
    ("DATA", "Share schemes - value of employee services", (None, None, None, 7200, None, 7200)),
    ("TOTAL", "Balance as at 31 March 2024", (128900, 600, 4800, 39300, 230200, 403800)),
    ("DATA", "Profit for the year (FY2025)", (None, None, None, None, 16900, 16900)),
    ("DATA", "Net loss in fair value", (None, -400, None, None, None, -400)),
    ("DATA", "Hedging adjustment (cash flow hedge reserve)", (None, None, -1300, None, None, -1300)),
    ("DATA", "Net amount transferred to profit or loss", (None, 200, None, None, None, 200)),
    ("TOTAL", "Total comprehensive income (FY2025)", (None, -200, -1300, None, 16900, 15400)),
    ("DATA", "Share schemes - value of employee services", (None, None, None, 6000, None, 6000)),
    ("TOTAL", "Balance as at 31 March 2025", (128900, 400, 3500, 45300, 247100, 425200)),
]

EQUITY_CHANGES_SOURCES = (
    "Sources - Statement of changes in equity, Bank basis, £'000, read chronologically:\n"
    f"FY2021/FY2022 movements: Atom Bank Plc full accounts made up to 31 March 2021, p.46-47 (Bank balance rollforward, "
    f"1 April 2020 to 31 March 2021) - {AR21_URL}\n"
    f"FY2022/FY2023 movements: Atom Bank Plc full accounts made up to 31 March 2023, p.54 (1 April 2021 to 31 March 2023) - {AR23_URL}\n"
    f"FY2024/FY2025 movements: Atom Bank Plc full accounts made up to 31 March 2025, p.56 (1 April 2023 to 31 March 2025) - {AR25_URL}\n"
    "DISCREPANCY FLAGGED, not silently reconciled: the FY2023 report's own precise closing balance as at 31 "
    "March 2023 (£'000: 29,305 / 47 / 5,163 / 32,169 / 217,947 / 284,631) does not exactly match the FY2025 "
    "report's own restated opening balance as at 1 April 2023 (£m, converted to £'000: 29,300 / ~0 / 5,200 / "
    "32,100 / 217,900 / 284,500) for the same date - a ~£131k gap driven mainly by the FY2025 report disclosing "
    "in £m (1 decimal place) rather than FY2023's own £'000 precision, plus the fair value reserve rounding to "
    "nil. Both rows are shown rather than picking one, and all FY2024/FY2025 movements and closing balances are "
    "taken from the FY2025 report's own £m figures as printed (×1,000) so that report's own arithmetic ties out "
    "exactly (Balance as at 31 March 2025 = 425,200 = the Balance Sheet sheet's own Total equity for FY2025)."
    "\n\nThe 'Other reserves and treasury shares' column used in the FY2021 report's Bank statement (nil "
    "throughout FY2020-FY2021, no treasury shares held by the Bank) and the 'Cash flow hedge reserve' column "
    "(introduced only from FY2022's hedging activity onward) are genuine structural differences across report "
    "vintages, not errors - reflected here as blank cells rather than forced to zero or merged."
    "\n\n" + ENTITY_NOTE
)

bw.add_equity_changes_sheet(
    title="Atom Bank Plc - Statement of Changes in Equity",
    subtitle="Bank (solo) basis, £'000, read chronologically oldest to newest",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQUITY_CHANGES_SOURCES,
    source_height=280,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Loss for the year", {"FY2022": -11927, "FY2021": -62379}),
    ("DATA", "Depreciation and amortisation", {"FY2022": 10531, "FY2021": 10442}),
    ("DATA", "Deferred tax asset recognised", {"FY2022": -5353}),
    ("DATA", "Impairment of intangible assets", {"FY2021": 0}),
    ("DATA", "Share option scheme reserves", {"FY2022": 4585, "FY2021": 2497}),
    ("DATA", "Other non cash movements", {"FY2022": -345, "FY2021": 1307}),
    ("DATA", "Loans and advances to customers", {"FY2022": -745215, "FY2021": 331967}),
    ("DATA", "Customer deposits", {"FY2022": 1075377, "FY2021": 289607}),
    ("DATA", "Borrowing(s) from central banks", {"FY2022": 297656, "FY2021": 22612}),
    ("DATA", "Deemed loan", {"FY2022": 233156, "FY2021": -122391}),
    ("DATA", "Debt securities in issue", {"FY2022": 0, "FY2021": 0}),
    ("DATA", "Debt instruments/securities held at amortised cost", {"FY2022": 354400, "FY2021": -426192}),
    ("DATA", "Repurchase agreements", {"FY2021": 0}),
    ("DATA", "Other assets", {"FY2022": -20768, "FY2021": -4443}),
    ("DATA", "Other liabilities and provisions", {"FY2022": 20413, "FY2021": 1828}),
    ("DATA", "Derivatives held for hedging purposes", {"FY2022": -36277, "FY2021": -14013}),
    ("TOTAL", "Net Cash Inflow/(Outflow) in Operating Activities", {"FY2022": 1176233, "FY2021": 30842}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Acquisition of intangible assets", {"FY2022": -9707, "FY2021": -8641}),
    ("DATA", "Acquisition of property, plant and equipment", {"FY2022": -267, "FY2021": -271}),
    ("DATA", "Net (acquisition)/maturity of debt securities at FVOCI", {"FY2022": -146282, "FY2021": 25681}),
    ("TOTAL", "Net Cash (Outflow)/Inflow from Investing Activities", {"FY2022": -156256, "FY2021": 16769}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Proceeds from issuance of shares, net of expenses", {"FY2022": 117443, "FY2021": 0}),
    ("DATA", "Purchase of treasury shares", {"FY2021": 0}),
    ("DATA", "Payment of principal portion of lease liabilities", {"FY2022": -650, "FY2021": -699}),
    ("TOTAL", "Net Cash Inflow/(Outflow) from Financing Activities", {"FY2022": 116793, "FY2021": -699}),
    ("TOTAL", "Net Increase in Cash and Balances at Central Banks", {"FY2022": 1136770, "FY2021": 46912}),
    ("DATA", "Cash and balances at central banks at beginning of year", {"FY2022": 316826, "FY2021": 269915}),
    ("TOTAL", "Cash and Balances at Central Banks at the End of the Year", {"FY2022": 1453596, "FY2021": 316827}),
]

bw.add_cash_flow_sheet(
    title="Atom Bank Plc — Statement of Cash Flows",
    subtitle="Bank (solo) basis, £'000. FY2023-FY2025 blank - see source note at bottom (FRS 101 cash-flow exemption).",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=74,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Gross carrying amount by product", {}),
    ("DATA", "Mortgages", {"FY2025": 4251500, "FY2024": 3242600, "FY2023": 2148481, "FY2022": 1487122, "FY2021": 976553}),
    ("DATA", "BBSL (secured business lending)", {"FY2025": 838700, "FY2024": 607900, "FY2023": 511831, "FY2022": 497305, "FY2021": 351978}),
    ("DATA", "BBUL (unsecured business lending)", {"FY2025": 256600, "FY2024": 307300, "FY2023": 389427, "FY2022": 439465, "FY2021": 310158}),
    ("TOTAL", "Total gross carrying amount", {"FY2025": 5346800, "FY2024": 4157800, "FY2023": 3049739, "FY2022": 2423892, "FY2021": 1638689}),
    ("SECTION", "Gross carrying amount by IFRS 9 stage", {}),
    ("DATA", "Stage 1: 12 month expected loss", {"FY2025": 5004400, "FY2024": 3881700, "FY2023": 2819585, "FY2022": 1970916, "FY2021": 1513908}),
    ("DATA", "Stage 2: Lifetime - loans not credit impaired", {"FY2025": 292200, "FY2024": 239900, "FY2023": 195537, "FY2022": 428042, "FY2021": 117989}),
    ("DATA", "Stage 3: Lifetime - credit impaired loans", {"FY2025": 50200, "FY2024": 36200, "FY2023": 34617, "FY2022": 24934, "FY2021": 6792}),
    ("TOTAL", "Total gross carrying amount (by stage)", {"FY2025": 5346800, "FY2024": 4157800, "FY2023": 3049739, "FY2022": 2423892, "FY2021": 1638689}),
    ("SECTION", "Expected credit loss provision", {}),
    ("DATA", "Mortgages", {"FY2025": 5900, "FY2024": 5100, "FY2023": 3618, "FY2022": 1257, "FY2021": 577}),
    ("DATA", "BBSL", {"FY2025": 3300, "FY2024": 3000, "FY2023": 2678, "FY2022": 2479, "FY2021": 4076}),
    ("DATA", "BBUL", {"FY2025": 9200, "FY2024": 11900, "FY2023": 10042, "FY2022": 5751, "FY2021": 5086}),
    ("TOTAL", "Total provision for on balance sheet impairment losses", {"FY2025": 18400, "FY2024": 20000, "FY2023": 16338, "FY2022": 9487, "FY2021": 9739}),
    ("SECTION", "Net balance sheet carrying value by product", {}),
    ("DATA", "Mortgages", {"FY2025": 4219800, "FY2024": 3200400, "FY2023": 2070110, "FY2022": 1455268, "FY2021": 985758}),
    ("DATA", "BBSL", {"FY2025": 834300, "FY2024": 604900, "FY2023": 509153, "FY2022": 494826, "FY2021": 347902}),
    ("DATA", "BBUL", {"FY2025": 247400, "FY2024": 295600, "FY2023": 379506, "FY2022": 433972, "FY2021": 305191}),
    ("TOTAL", "Net balance sheet carrying value", {"FY2025": 5301500, "FY2024": 4100900, "FY2023": 2958769, "FY2022": 2384066, "FY2021": 1638851}),
    ("SECTION", "Asset quality ratios", {}),
    ("DATA", "Total coverage ratio (ECL provision / gross carrying amount)", {"FY2025": "0.33%", "FY2024": "0.44%", "FY2023": "0.48%", "FY2022": "0.36%", "FY2021": "0.53%"}),
    ("DATA", "Stage 3 / NPL ratio (Stage 3 gross / total gross carrying amount)", {"FY2025": "0.94%", "FY2024": "0.87%", "FY2023": "1.14%", "FY2022": "1.03%", "FY2021": "0.41%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 ECL provision / Stage 3 gross)", {"FY2025": "13.55%", "FY2024": "17.96%", "FY2023": "11.47%", "FY2022": "11.37%", "FY2021": "17.90%"}),
]

ASSET_QUALITY_SOURCES = (
    "Sources - Note 'Loans and advances to customers', Bank/Group basis (Atom's retail lending is on a single "
    "Bank basis for this note in every year, unlike the primary statements), £'000:\n"
    f"FY2025/FY2024: Atom Bank Plc full accounts made up to 31 March 2025, p.69 - {AR25_URL}\n"
    f"FY2023/FY2022: Atom Bank Plc full accounts made up to 31 March 2023, p.69-70 - {AR23_URL}\n"
    f"FY2021: Atom Bank Plc full accounts made up to 31 March 2021, p.72-73 (comparatives disclosed there for "
    f"FY2021/FY2020) - {AR21_URL}\n"
    "'Total gross carrying amount' (by product) and 'Total gross carrying amount (by stage)' are the same "
    "underlying figure shown two ways (by product vs by IFRS 9 stage) and tie out exactly for every year "
    "(each product's own stage 1+2+3 gross carrying amounts sum to that product's own total row in the source "
    "table) - the by-stage total is what ties to the Balance Sheet's Loans and advances to customers line (net "
    "of the ECL provision below) for every year. Ratios are "
    "the Bank's own disclosed 'Total coverage ratio' row (FY2023-FY2021) or its FY2025/FY2024 equivalent, plus "
    "Stage 3/NPL and Stage 3 coverage ratios calculated here from the disclosed stage-level figures."
    "\n\n" + STATEMENT_ENTITY_NOTE
)

bw.add_asset_quality_sheet(
    title="Atom Bank Plc - Asset Quality / Credit Risk Disclosures",
    subtitle="Bank basis, £'000 (ratios as stated/calculated)",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    source_height=260,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Bank basis, {unit}" if unit else "Bank basis",
                         rows_data, sources_text, note=note, first_col_width=52, source_height=180)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 356400, "FY2024": 347300, "FY2023": 241213, "FY2022": 217158, "FY2021": 114012})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWEA",
    [("Common Equity Tier 1 ratio (%)", {"FY2025": "15.0%", "FY2024": "19.0%", "FY2023": "19.0%", "FY2022": "20.8%", "FY2021": "15.3%"})],
    p3_sources(),
    note="Reported on a transitional (IFRS 9 relief) basis throughout, per project convention. The FY2025 Pillar 3 "
         "Disclosures state that without IFRS 9 transitional relief, FY2025's CET1 ratio would be 14.8% (Bank: "
         "14.8%) rather than the 15.0% shown - not substituted in, noted here for reference only.",
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2025": 356400, "FY2024": 347300, "FY2023": 241213, "FY2022": 217158, "FY2021": 114012})],
    p3_sources(),
    note="Tier 1 Capital = CET1 Capital every year - Atom has never held Additional Tier 1 (AT1) instruments (KM1 "
         "template shows an identical row 1/row 2 every year).",
)

metric(
    "Tier 1 Ratio", "% of RWEA",
    [("Tier 1 ratio (%)", {"FY2025": "15.0%", "FY2024": "19.0%", "FY2023": "19.0%", "FY2022": "20.8%", "FY2021": "15.3%"})],
    p3_sources(),
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2025": 406400, "FY2024": 347300, "FY2023": 248418, "FY2022": 225151, "FY2021": 121990})],
    p3_sources(),
    note="Total Capital exceeds Tier 1 Capital from FY2025 onward once Atom's £50m Fixed Rate Reset Callable "
         "Subordinated Tier 2 notes (issued October 2024) entered regulatory capital; FY2021-FY2023 also carry a "
         "smaller Tier 2 balance (British Business Bank instruments, ~£8m in FY2021) but FY2024's KM1 template "
         "shows Total Capital = Tier 1 exactly (no Tier 2 balance that year, per the source table).",
)

metric(
    "Total Capital Ratio", "% of RWEA",
    [("Total capital ratio (%)", {"FY2025": "17.1%", "FY2024": "19.0%", "FY2023": "19.5%", "FY2022": "21.6%", "FY2021": "16.4%"})],
    p3_sources(),
    note="The FY2025 Pillar 3 Disclosures state that without IFRS 9 transitional relief, FY2025's total capital "
         "ratio would be 16.9% (Bank: 16.9%) rather than the 17.1% shown - noted for reference only, not substituted.",
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted exposure amount", {"FY2025": 2379300, "FY2024": 1828000, "FY2023": 1271669, "FY2022": 1043001, "FY2021": 743296})],
    p3_sources(),
)

# ---------------------------------------------------------------
# Sheet: RWA Breakdown (placed immediately after Total RWAs, before Leverage Ratio)
# ---------------------------------------------------------------
rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 2171000, "FY2024": 1676100, "FY2023": 1161945, "FY2022": 951043, "FY2021": 658405}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 13400, "FY2024": 6000, "FY2023": 1903, "FY2022": 13238, "FY2021": 3677}),
    ("DATA", "  of which credit valuation adjustment (CVA)", {"FY2025": 7100, "FY2024": 2700, "FY2023": 524, "FY2022": 4621, "FY2021": 560}),
    ("DATA", "Securitisation exposures (non-trading book, after the cap)", {"FY2025": 20900, "FY2024": 4300, "FY2023": 21200, "FY2022": 40725, "FY2021": 81214}),
    ("DATA", "Market risk (position, FX and commodities risks)", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Operational risk", {"FY2025": 174000, "FY2024": 141600, "FY2023": 86621, "FY2022": 37995, "FY2021": 0}),
    ("TOTAL", "Total risk-weighted exposure amount (RWEAs)", {"FY2025": 2379300, "FY2024": 1828000, "FY2023": 1271669, "FY2022": 1043001, "FY2021": 743296}),
]

RWA_BREAKDOWN_SOURCES = (
    "Sources - Table UK OV1 (Overview of risk weighted exposure amounts), Bank basis, £'000:\n"
    f"FY2025/FY2024: Atom Holdco plc Pillar 3 Disclosures 2025, p.16 (Bank column) - {P3_FY25_URL}\n"
    f"FY2023: Atom Holdco Limited Pillar 3 Disclosures 2023, p.16-17 (Bank column) - {P3_FY23_URL}\n"
    f"FY2022/FY2021: Atom Bank Plc Pillar 3 Disclosures 2021/22, p.20-21 - {P3_FY22_URL}\n"
    "Atom states it has no Pillar 1 market risk exposures in every year's Pillar 3 report - shown as £0 rather "
    "than blank/not-disclosed. FY2025/FY2024 figures were originally disclosed in £m (1 decimal place) and are "
    "shown here converted to £'000 (x1,000), consistent with the FY2024/FY2025 Pillar 3 ratio sheets' own unit "
    "conversion note; FY2023-FY2021 are the source table's own £'000 figures. Total ties out exactly to the "
    "Total RWAs sheet for every year."
)

bw.add_rwa_breakdown_sheet(
    title="Atom Bank Plc - RWA Breakdown",
    subtitle="Bank basis, £'000",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Leverage ratio total exposure measure", {"FY2025": 7174600, "FY2024": 5064500, "FY2023": 3723901, "FY2022": 3313171, "FY2021": 2914267}),
        ("Leverage ratio (%)", {"FY2025": "5.0%", "FY2024": "6.9%", "FY2023": "6.5%", "FY2022": "6.6%", "FY2021": "3.9%"}),
    ],
    p3_sources(),
    note="Atom states it is 'out of scope of the leverage ratio requirements due to retail deposits falling below "
         "the threshold of £50bn' (FY2025 Pillar 3 Disclosures) - the ratio is voluntarily calculated and "
         "monitored against an internal 3.25% floor rather than a binding regulatory minimum. No 'excluding "
         "claims on central banks' basis break is shown in Atom's own KM1 templates (unlike several other banks "
         "in this project) - one consistent methodology is used throughout FY2021-FY2025.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value (average)", {"FY2025": 2333100, "FY2024": 3849000, "FY2023": 2494398, "FY2022": 971602, "FY2021": 415697}),
        ("Total net cash outflows, adjusted value", {"FY2025": 550400, "FY2024": 534000, "FY2023": 446330, "FY2022": 310483, "FY2021": 185032}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "418.6%", "FY2024": "727.8%", "FY2023": "578.6%", "FY2022": "316.7%", "FY2021": "241.8%"}),
    ],
    p3_sources(),
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding", {"FY2025": 6821300, "FY2024": 6891400, "FY2023": 5557689, "FY2022": 3492177, "FY2021": 2536566}),
        ("Total required stable funding", {"FY2025": 3987700, "FY2024": 3146100, "FY2023": 2615311, "FY2022": 2248265, "FY2021": 2029057}),
        ("Net Stable Funding Ratio (%)", {"FY2025": "171.2%", "FY2024": "221.8%", "FY2023": "211.8%", "FY2022": "154.9%", "FY2021": "125.0%"}),
    ],
    p3_sources(),
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={
        "MREL Ratio": "MREL is not mentioned anywhere in any of Atom's 5 Pillar 3 Disclosures (FY2021-FY2025) - "
                       "no numeric ratio and no stated exemption, similar to several other smaller banks in this "
                       "project (e.g. Zopa, Zenith).",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 8990900, "FY2024": 7224900, "FY2023": 7801381, "FY2022": 4558515, "FY2021": 2827121}),
        ("Loans and advances to customers", {"FY2025": 5301500, "FY2024": 4100900, "FY2023": 2958769, "FY2022": 2384066, "FY2021": 1638851}),
        ("Customer deposits", {"FY2025": 7538700, "FY2024": 5746200, "FY2023": 6551325, "FY2022": 3229796, "FY2021": 2154419}),
        ("Total equity", {"FY2025": 425200, "FY2024": 403800, "FY2023": 284631, "FY2022": 251094, "FY2021": 141330}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net operating income/(expense)", {"FY2025": 93500, "FY2024": 88100, "FY2023": 65564, "FY2022": 48018, "FY2021": -1714}),
        ("Staff and administrative expense", {"FY2025": -68400, "FY2024": -61500, "FY2023": -59128, "FY2022": -50182, "FY2021": -47129}),
        ("Profit/(loss) for the year", {"FY2025": 16900, "FY2024": 12300, "FY2023": -5623, "FY2022": -11927, "FY2021": -62379}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 403800, "FY2024": 284500, "FY2023": 251094, "FY2022": 141330, "FY2021": 200503}),
        ("Total comprehensive income/(expense) for the year", {"FY2025": 15400, "FY2024": 12500, "FY2023": -352, "FY2022": -12264, "FY2021": -61670}),
        ("Other equity movements, net", {"FY2025": 6000, "FY2024": 106800, "FY2023": 33889, "FY2022": 122028, "FY2021": 2497}),
        ("Closing equity", {"FY2025": 425200, "FY2024": 403800, "FY2023": 284631, "FY2022": 251094, "FY2021": 141330}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2022": 1176233, "FY2021": 30842}),
        ("Net cash from/(used in) investing activities", {"FY2022": -156256, "FY2021": 16769}),
        ("Net cash from/(used in) financing activities", {"FY2022": 116793, "FY2021": -699}),
        ("Cash and balances at central banks at end of year", {"FY2022": 1453596, "FY2021": 316827}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "15.0%", "FY2024": "19.0%", "FY2023": "19.0%", "FY2022": "20.8%", "FY2021": "15.3%"}),
        ("Tier 1 Ratio", {"FY2025": "15.0%", "FY2024": "19.0%", "FY2023": "19.0%", "FY2022": "20.8%", "FY2021": "15.3%"}),
        ("Total Capital Ratio", {"FY2025": "17.1%", "FY2024": "19.0%", "FY2023": "19.5%", "FY2022": "21.6%", "FY2021": "16.4%"}),
        ("Leverage Ratio", {"FY2025": "5.0%", "FY2024": "6.9%", "FY2023": "6.5%", "FY2022": "6.6%", "FY2021": "3.9%"}),
        ("LCR", {"FY2025": "418.6%", "FY2024": "727.8%", "FY2023": "578.6%", "FY2022": "316.7%", "FY2021": "241.8%"}),
        ("NSFR", {"FY2025": "171.2%", "FY2024": "221.8%", "FY2023": "211.8%", "FY2022": "154.9%", "FY2021": "125.0%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Cash flow is blank for FY2023-FY2025 (FRS 101 qualifying-"
         "entity exemption took effect from FY2023, following the insertion of Atom Holdco above Atom Bank Plc - "
         "see Cash Flow Statement sheet note). Unlike several other banks in this project, all ratios here are on "
         "a consistent Bank-solo basis throughout - no cash-flow-vs-Pillar-3 basis mismatch. 'Net operating "
         "income/(expense)' and 'Staff and administrative expense' stand in for the usual 'Revenue'/'Total "
         "operating expense' headline pair - Atom's own P&L structure doesn't disclose a single top-line revenue "
         "figure (see the Profit & Loss sheet's presentation note). FY2024's 'Opening equity' (£284,500k) uses "
         "the FY2025 Annual Report's own restated 1 April 2023 balance rather than the FY2023 report's own "
         "(slightly different, £284,631k) closing balance for the same date - see the Statement of Changes in "
         "Equity sheet's flagged discrepancy note.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/ATOM BANK FINANCIALS.xlsx")
print("Saved ATOM BANK FINANCIALS.xlsx")
