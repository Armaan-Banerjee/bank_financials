import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Cash flow statement only exists for FY2021-FY2022 (calendar year-end) - see
# ENTITY_NOTE / CASH_FLOW_EXEMPTION_NOTE below. Pillar 3 covers all 5 years.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/00955491/filing-history"
AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/00955491/filing-history"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/00955491/filing-history"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/00955491/filing-history"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/00955491/filing-history"

P3_2025_URL = "https://cdn.prod.website-files.com/62b1c54534b6a11713c35c02/6a1da906ea626c65de0ea1b6_TML_Pillar%203%202025%20Final.pdf"
P3_2024_URL = "https://cdn.prod.website-files.com/62b1c54534b6a11713c35c02/680f52c61791aa8addbecd66_TML_Pillar%203%202024%20Final.pdf"
P3_2023_URL = "https://cdn.prod.website-files.com/62b1c54534b6a11713c35c02/66a0e99ad693a6e63fe72544_TML_Pillar%203%202023%20Final.pdf"
P3_2021_URL = "https://assets.website-files.com/62a364a1705cce548303c9aa/6337028c7519c4c08e1b5d54_TML_Pillar%203%202021.12.31_Board.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: 'Tandem Bank Limited' (company number 00955491, FRN 204479) is the PRA-authorised entity built "
    "here. It is NOT the same company as 'Tandem Money Limited' (company number 08628614) - a related, similarly-"
    "named entity that briefly used the name 'Tandem Bank Limited' itself from Dec 2015-May 2017 before becoming "
    "Tandem Money Limited (TML), the non-bank holding company that today sits above Tandem Bank Limited (TBL) in "
    "the group structure. Company 00955491 was previously 'Harrods Bank Limited' (renamed 12 Jan 2018) - Tandem "
    "acquired Harrods Bank's banking licence in 2017 to become a PRA-authorised deposit-taker quickly; it traces "
    "further back to 'Harrods Trust Limited' and, before that, 'Harrods (Knightsbridge) Limited' (incorporated "
    "1969), which is why Companies House shows an incorporation date decades before Tandem's own 2013 founding. "
    "Confirmed via Companies House (previous-names history) and cross-checked against the FRN in Banks List 2608.xlsx."
)

CASH_FLOW_EXEMPTION_NOTE = (
    "CASH FLOW EXEMPTION NOTE: only FY2021 and FY2022 have a Statement of Cash Flows. From the FY2023 Annual Report "
    "onward (confirmed directly in the FY2023, FY2024, and FY2025 Annual Reports - all three fully scanned/image-"
    "only Companies House filings, OCR'd with tesseract and cross-verified against rendered page images), Tandem "
    "Bank Limited's accounting policies note states: 'The Bank is a qualifying entity as defined in FRS 102 and has "
    "therefore adopted the disclosure exemptions of FRS 102 Section 7 and paragraph 3.17(d) to not disclose a cash "
    "flow statement' - the same FRS 101/102 'qualifying entity' exemption that has blocked several other banks in "
    "this project (PNBE, ICICI, United Trust Bank, Union Bancaire Privée UK) entirely. Unlike those banks, Tandem "
    "took the exemption only recently (from FY2023) rather than throughout its history, so FY2021-FY2022 do have "
    "genuine, fully reconciling cash flow statements - both built here from the Bank's own Companies House filings "
    "(also fully scanned, OCR'd and cross-verified) rather than skipping the bank outright. FY2023-FY2025 are left "
    "blank on the Cash Flow Statement sheet rather than guessed."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Tandem Bank Limited's own (Company-only, not Group) Statement of Cash Flows, £'000:\n"
    f"FY2022: Tandem Bank Limited Annual Report and Accounts for the year ended 31 December 2022, p.45 (Statement "
    f"of Cash Flows) - {AR2022_URL}\n"
    f"FY2021: Tandem Bank Limited Annual Report and Accounts for the year ended 31 December 2021, p.48 (Statement "
    f"of Cash Flows) - {AR2021_URL}\n"
    "Both years' figures were independently cross-checked against their appearance as the following year's "
    "comparative column (FY2021 as reported in the FY2022 Annual Report) and matched exactly.\n\n"
    + ENTITY_NOTE + "\n\n" + CASH_FLOW_EXEMPTION_NOTE
)


def p3_sources(page_25="4", page_24="4", page_23="3", page_21="21"):
    return (
        "Sources - Tandem Money Limited (TML) Group consolidated basis (comprising TML, its wholly-owned "
        "subsidiary Tandem Bank Limited (TBL), and Allium Lending Group Limited) - NOT Tandem Bank Limited solo:\n"
        f"FY2025: TML Pillar 3 Disclosures, 31 December 2025, p.{page_25} (2. Key Metrics - UK KM1) - {P3_2025_URL}\n"
        f"FY2024: TML Pillar 3 Disclosures, 31 December 2024, p.{page_24} (2. Key Metrics - UK KM1) - {P3_2024_URL}\n"
        f"FY2023: TML Pillar 3 Disclosures, 31 December 2023, p.{page_23} (2. Key Metrics - UK KM1) - {P3_2023_URL}\n"
        "FY2022: no standalone Pillar 3 edition was found published or archived for 31 December 2022 (not on "
        "Tandem's newsroom page, not found via web search or Wayback Machine) - sourced instead from the FY2023 "
        f"Pillar 3 Disclosures' own '31 Dec '22' comparative column, p.{page_23} - {P3_2023_URL}\n"
        f"FY2021: TML Pillar 3 Disclosures, 31 December 2021, p.{page_21} (4. Capital Disclosures) and p.32-41 "
        f"(8. Leverage / Appendix 3: Liquidity Coverage Ratio) - {P3_2021_URL}\n"
        "PILLAR 3 BASIS NOTE: this is a genuine cash-flow-vs-Pillar-3 basis mismatch (Bank-only cash flow vs. "
        "Group-level Pillar 3), the same pattern seen with Vanquis Bank Limited elsewhere in this project - Tandem "
        "does not publish a Bank-only Pillar 3 breakout."
    )


bw = BankWorkbook(bank_name="Tandem Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="7C4A03")

RESTATEMENT_NOTE = (
    "RESTATEMENT NOTE: FY2022's Balance Sheet, Profit & Loss and Statement of Changes in Equity figures shown "
    "here are Tandem Bank Limited's own AS-ORIGINALLY-PUBLISHED figures (from the FY2022 Annual Report and "
    "Accounts), not the later FY2023 Annual Report's restated FY2022 comparative column (which reclassified "
    "certain effective interest rate balances and reflected motor finance hire purchase receivables as secured "
    "rather than unsecured lending - Note 2 of the FY2023 Annual Report). This creates a genuine, documented, "
    "non-plugged break at the FY2022/FY2023 boundary on the Statement of Changes in Equity sheet: FY2022's own "
    "closing Total equity (£115,178k) does not equal the FY2023 Annual Report's restated FY2023 opening balance "
    "(£115,535k, a £357k difference, itself split into a +£1,737k Other Reserves capital-contribution "
    "reclassification and a -£1,380k Retained earnings adjustment) - both figures are shown, connected by an "
    "explicit 'Restatement (per Note 2 of the FY2023 Annual Report)' row rather than silently smoothed over. The "
    "same restatement affects Loans and advances to customers on the Balance Sheet (FY2022 shown here as "
    "£1,078,369k as originally reported vs. £1,080,282k in the FY2023 Annual Report's restated comparative) and "
    "the FY2022 Profit & Loss (originally reported: Interest income £74,932k, Loss on operating activities before "
    "tax £(6,933)k, Loss for the year £(1,654)k; FY2023 Annual Report's restated comparative: Interest income "
    "£72,374k, Loss before tax £(9,491)k, Loss for the year £(4,212)k)."
)


def statement_sources(page_bs, page_pl, page_eq, note_extra=None):
    text = (
        "Sources - all figures are Tandem Bank Limited's own (Company-only, not TML Group) figures, £'000:\n"
        f"FY2025: Annual Report and Accounts for the year ended 31 December 2025, p.{page_bs} (Statement of "
        f"Financial Position), p.{page_pl} (Income Statement and Statement of Other Comprehensive Income), "
        f"p.{page_eq} (Statement of Changes in Equity) - {AR2025_URL}\n"
        "FY2024: as reported in the FY2025 Annual Report's own comparative column (no separate FY2024 filing "
        f"covers this line item set at this granularity) - {AR2025_URL}\n"
        "FY2023: Annual Report and Accounts for the year ended 31 December 2023, p.33 (Statement of Financial "
        f"Position), p.32 (Income Statement and Statement of Other Comprehensive Income), p.34 (Statement of "
        f"Changes in Equity) - {AR2023_URL}\n"
        "FY2022: Annual Report and Accounts for the year ended 31 December 2022, p.43 (Statement of Financial "
        f"Position), p.42 (Income Statement and Statement of Other Comprehensive Income), p.44 (Statement of "
        f"Changes in Equity) - as originally reported, NOT the FY2023 Annual Report's later restated comparative "
        f"- {AR2022_URL}\n"
        "FY2021: Annual Report and Accounts for the year ended 31 December 2021, p.46 (Income Statement and "
        f"Statement of Other Comprehensive Income), p.47 (Statement of Financial Position), p.48 (Statement of "
        f"Changes in Equity) - {AR2021_URL}\n\n"
        + ENTITY_NOTE + "\n\n" + RESTATEMENT_NOTE
    )
    if note_extra:
        text += "\n\n" + note_extra
    return text


# ---------------------------------------------------------------
# Balance Sheet
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 584887, "FY2024": 1497095, "FY2023": 2421938, "FY2022": 679659, "FY2021": 360378}),
    ("DATA", "Loans and advances to banks", {"FY2025": 35121, "FY2024": 33267, "FY2023": 34287, "FY2022": 21271, "FY2021": 16310}),
    ("DATA", "Loans and advances to customers", {"FY2025": 1284901, "FY2024": 1219256, "FY2023": 1280896, "FY2022": 1078369, "FY2021": 436845}),
    ("DATA", "Total debt securities", {"FY2025": 554658, "FY2024": 370151, "FY2023": 56609, "FY2022": 91210, "FY2021": 30215}),
    ("DATA", "Debt securities at amortised cost (Mortgage Backed Loan Notes Class A + Vertical Risk Retention Notes)", {"FY2025": 300970, "FY2024": 213670}),
    ("DATA", "Debt securities available-for-sale (at market value)", {"FY2025": 253688, "FY2024": 156481, "FY2023": 56609, "FY2022": 91210, "FY2021": 30215}),
    ("DATA", "UK Government securities (part of Debt securities)", {"FY2025": 31269, "FY2024": 0, "FY2023": 0, "FY2022": 19960, "FY2021": 5078}),
    ("DATA", "Other debt securities (supranational, European and UK financial institutions, mortgage-backed loan notes)", {"FY2025": 523389, "FY2024": 370151, "FY2023": 56609, "FY2022": 71250, "FY2021": 25137}),
    ("DATA", "Derivative financial instruments", {"FY2025": 6383, "FY2024": 11304, "FY2023": 24353, "FY2022": 29592, "FY2021": 2358}),
    ("DATA", "Equity shares", {"FY2025": 3667, "FY2024": 3533, "FY2023": 2758, "FY2022": 2309, "FY2021": 1970}),
    ("DATA", "Other assets", {"FY2025": 11395, "FY2024": 10296, "FY2023": 27830, "FY2022": 23287, "FY2021": 5639}),
    ("DATA", "Prepayments and accrued income", {"FY2023": 493, "FY2022": 500, "FY2021": 4}),
    ("DATA", "Deferred tax asset", {"FY2025": 8816, "FY2024": 10295, "FY2023": 10236}),
    ("TOTAL", "Total Assets", {"FY2025": 2489828, "FY2024": 3155197, "FY2023": 3859400, "FY2022": 1926197, "FY2021": 853719}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks / Borrowings from banks", {"FY2025": 10113, "FY2024": 23798, "FY2023": 30934, "FY2022": 43527, "FY2021": 40013}),
    ("DATA", "Customer accounts", {"FY2025": 2260738, "FY2024": 2916365, "FY2023": 3639407, "FY2022": 1754868, "FY2021": 771161}),
    ("DATA", "Derivative financial instruments", {"FY2025": 4988, "FY2024": 2503, "FY2023": 11197, "FY2022": 7057, "FY2021": 89}),
    ("DATA", "Other liabilities", {"FY2025": 6467, "FY2024": 15529, "FY2023": 1613, "FY2022": 5162, "FY2021": 522}),
    ("DATA", "Accruals and deferred income", {"FY2023": 735, "FY2022": 405, "FY2021": 314}),
    ("DATA", "Subordinated liabilities", {"FY2025": 19592, "FY2024": 19323, "FY2023": 18943}),
    ("TOTAL", "Total Liabilities", {"FY2025": 2301898, "FY2024": 2977518, "FY2023": 3702829, "FY2022": 1811019, "FY2021": 812099}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called-up share capital", {"FY2025": 200999, "FY2024": 192999, "FY2023": 187999, "FY2022": 152339, "FY2021": 75875}),
    ("DATA", "Other reserves", {"FY2025": 85444, "FY2024": 86998, "FY2023": 82924, "FY2022": 80051, "FY2021": 80051}),
    ("DATA", "Retained reserves (Available for sale reserve + Retained earnings/(losses))", {"FY2025": -98513, "FY2024": -102318, "FY2023": -114352, "FY2022": -117212, "FY2021": -114306}),
    ("TOTAL", "Total Equity", {"FY2025": 187930, "FY2024": 177679, "FY2023": 156571, "FY2022": 115178, "FY2021": 41620}),
    ("TOTAL", "Total Liabilities and Equity", {"FY2025": 2489828, "FY2024": 3155197, "FY2023": 3859400, "FY2022": 1926197, "FY2021": 853719}),
]

DEBT_SECURITIES_NOTE = (
    "DEBT SECURITIES BREAKDOWN NOTE: the amortised-cost/available-for-sale and UK Government/other sub-rows "
    "beneath 'Total debt securities' are drawn from the Bank's own 'Debt Securities' note, not estimated: "
    f"FY2025/FY2024 from Note 12 (Debt Securities), p.42 of the FY2025 Annual Report - {AR2025_URL}; FY2023/FY2022 "
    f"(as originally reported in that year's own filing) from Note 12, p.50 of the FY2023 Annual Report - "
    f"{AR2023_URL}; FY2021 from Note 15, p.61 of the FY2022 Annual Report (that filing's own '2021' comparative "
    f"column) - {AR2022_URL}. From FY2025, the note also splits out amortised-cost holdings (Mortgage Backed Loan "
    "Notes Class A and Vertical Risk Retention Notes issued by the Bank's own securitisation vehicles, Fylde "
    "Funding 2025-1 PLC and predecessors) that did not exist in FY2021-FY2023, when the entire debt securities "
    "book was held available-for-sale at market value for liquidity purposes; FY2024's 'UK Government' leg is a "
    "genuine disclosed nil (the note shows '-'), not a missing value."
)


bw.add_balance_sheet_sheet(
    title="Tandem Bank Limited — Statement of Financial Position",
    subtitle="Bank (Company-only) basis, £'000. FY2022 shown as originally reported - see source note at bottom (restatement).",
    rows=bs_rows,
    sources_text=statement_sources(
        "25 (2025)/26 (2024 comparative)", "24 (2025)/25 (2024 comparative)", "26 (2025)/27 (2024 comparative)",
        note_extra=DEBT_SECURITIES_NOTE,
    ),
    first_col_width=68,
    source_height=280,
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 200193, "FY2024": 239980, "FY2023": 203197, "FY2022": 74932, "FY2021": 21588}),
    ("DATA", "Interest expense", {"FY2025": -112547, "FY2024": -161034, "FY2023": -125307, "FY2022": -19522, "FY2021": -6453}),
    ("TOTAL", "Net Interest Income", {"FY2025": 87646, "FY2024": 78946, "FY2023": 77890, "FY2022": 55410, "FY2021": 15135}),
    ("DATA", "Fees and commissions income", {"FY2022": 0, "FY2021": 11}),
    ("DATA", "Fees and commissions expense", {"FY2025": -164, "FY2024": -98, "FY2023": -103, "FY2022": -163, "FY2021": -482}),
    ("DATA", "Net (loss)/gain in derivatives and hedge ineffectiveness", {"FY2025": -1426, "FY2024": 1542, "FY2023": -1890, "FY2022": 1954, "FY2021": 115}),
    ("DATA", "Other operating income", {"FY2025": 41, "FY2024": 20, "FY2023": 15, "FY2022": 26, "FY2021": 23}),
    ("TOTAL", "Total Income", {"FY2025": 86097, "FY2024": 80410, "FY2023": 75912, "FY2022": 57227, "FY2021": 14802}),
    ("DATA", "Administrative expenses (Operating Expenses)", {"FY2025": -64142, "FY2024": -62957, "FY2023": -62045, "FY2022": -52218, "FY2021": -30508}),
    ("DATA", "Provision for bad and doubtful debts", {"FY2025": -25410, "FY2024": -17053, "FY2023": -19415, "FY2022": -13412, "FY2021": -1705}),
    ("DATA", "Gain/(loss) on sale of financial assets/loan portfolios", {"FY2025": 8930, "FY2024": 11220, "FY2023": 2752, "FY2022": 1470, "FY2021": -569}),
    ("DATA", "Impairment of intercompany balances", {"FY2022": 0, "FY2021": -50}),
    ("TOTAL", "Profit/(Loss) on Operating Activities before Tax", {"FY2025": 5475, "FY2024": 11620, "FY2023": -2796, "FY2022": -6933, "FY2021": -18030}),
    ("DATA", "Tax charge/credit on profit/(loss)", {"FY2025": -2017, "FY2024": -108, "FY2023": 6396, "FY2022": 5279, "FY2021": 177}),
    ("TOTAL", "Profit/(Loss) for the Year", {"FY2025": 3458, "FY2024": 11512, "FY2023": 3600, "FY2022": -1654, "FY2021": -17853}),
    ("SECTION", "Other Comprehensive Income/(Expense)", {}),
    ("DATA", "Available for sale investments - fair value gain/(loss) on debt securities", {"FY2025": 246, "FY2024": -59, "FY2023": 303, "FY2022": -328, "FY2021": 52}),
    ("DATA", "Available for sale investments - fair value gain on equity shares", {"FY2025": 134, "FY2024": 775, "FY2023": 450, "FY2022": 339, "FY2021": 271}),
    ("DATA", "Deferred income tax on items of other comprehensive income", {"FY2025": -33, "FY2024": -194, "FY2023": -113, "FY2022": -85, "FY2021": -177}),
    ("TOTAL", "Other Comprehensive Income/(Expense) for the Year, net of tax", {"FY2025": 347, "FY2024": 522, "FY2023": 640, "FY2022": -74, "FY2021": 146}),
    ("TOTAL", "Total Comprehensive Profit/(Loss) for the Year", {"FY2025": 3805, "FY2024": 12034, "FY2023": 4240, "FY2022": -1728, "FY2021": -17707}),
]

bw.add_income_statement_sheet(
    title="Tandem Bank Limited — Income Statement and Statement of Other Comprehensive Income",
    subtitle="Bank (Company-only) basis, £'000. FY2022 shown as originally reported - see source note at bottom (restatement).",
    rows=pl_rows,
    sources_text=statement_sources(
        "25 (2025)/26 (2024 comparative)", "24 (2025)/25 (2024 comparative)", "26 (2025)/27 (2024 comparative)",
        note_extra=(
            "FY2022's Income Statement in its own Annual Report split figures into Continuing/Discontinued "
            "Operations columns (the Bank sold a loan portfolio and disposed of a business line that year); the "
            "'2022 Total' column shown here sums both. FY2021's Fees and commissions income (£11k) is a "
            "Discontinued Operations item; FY2022 had none in either column, shown as 0 rather than blank since "
            "the line is genuinely nil that year, not undisclosed."
        ),
    ),
    first_col_width=76,
    source_height=300,
)

# ---------------------------------------------------------------
# Statement of Changes in Equity
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Called-up Share Capital", "Available for Sale Reserve", "Other Reserves", "Retained earnings/(losses)", "Total equity"]

equity_rows = [
    ("TOTAL", "At 1 January 2021", (63566, 1207, 80051, -97806, 47018)),
    ("DATA", "Loss for the year", (None, None, None, -17853, -17853)),
    ("DATA", "Gain relating to available for sale investments", (None, 323, None, None, 323)),
    ("DATA", "Deferred tax on items of other comprehensive income", (None, -177, None, None, -177)),
    ("TOTAL", "Total comprehensive loss for the year", (None, 146, None, -17853, -17707)),
    ("DATA", "Shares issued, net of expenses", (12309, None, None, None, 12309)),
    ("TOTAL", "As at 31 December 2021", (75875, 1353, 80051, -115659, 41620)),
    ("DATA", "Loss for the year", (None, None, None, -1654, -1654)),
    ("DATA", "Gain relating to available for sale investments", (None, 11, None, None, 11)),
    ("DATA", "Deferred tax on items of other comprehensive income", (None, -85, None, None, -85)),
    ("TOTAL", "Total comprehensive loss for the year", (None, -74, None, -1654, -1728)),
    ("DATA", "Shares issued, net of expenses", (76464, None, None, None, 76464)),
    ("DATA", "Capital contribution", (None, None, None, -1178, -1178)),
    ("TOTAL", "As at 31 December 2022 (as originally reported)", (152339, 1279, 80051, -118491, 115178)),
    ("DATA", "Restatement (per Note 2 of the FY2023 Annual Report - reclassification of effective interest rate balances and motor finance hire purchase receivables)", (None, None, 1737, -1380, 357)),
    ("TOTAL", "At 1 January 2023 (restated)", (152339, 1279, 81788, -119871, 115535)),
    ("DATA", "Profit for the year", (None, None, None, 3600, 3600)),
    ("DATA", "Gain relating to available for sale investments", (None, 753, None, None, 753)),
    ("DATA", "Deferred tax on items of other comprehensive income", (None, -113, None, None, -113)),
    ("TOTAL", "Total comprehensive profit for the year", (None, 640, None, 3600, 4240)),
    ("DATA", "Shares issued, net of expenses", (35660, None, None, None, 35660)),
    ("DATA", "Capital contribution", (None, None, 1136, None, 1136)),
    ("TOTAL", "As at 31 December 2023", (187999, 1919, 82924, -116271, 156571)),
    ("DATA", "Profit for the year", (None, None, None, 11512, 11512)),
    ("DATA", "Gain relating to available for sale investments", (None, 716, None, None, 716)),
    ("DATA", "Deferred tax on items of other comprehensive income", (None, -194, None, None, -194)),
    ("TOTAL", "Total comprehensive profit for the year", (None, 522, None, 11512, 12034)),
    ("DATA", "Fair value adjustment of loans and advances to customers - on acquisition date", (None, None, 4287, None, 4287)),
    ("DATA", "Fair value adjustment of loans and advances to customers - amortisation", (None, None, -213, None, -213)),
    ("DATA", "Shares issued, net of expenses", (5000, None, None, None, 5000)),
    ("TOTAL", "As at 31 December 2024", (192999, 2441, 86998, -104759, 177679)),
    ("DATA", "Profit for the year", (None, None, None, 3458, 3458)),
    ("DATA", "Gain relating to available for sale investments", (None, 380, None, None, 380)),
    ("DATA", "Deferred tax on items of other comprehensive income", (None, -33, None, None, -33)),
    ("TOTAL", "Total comprehensive profit for the year", (None, 347, None, 3458, 3805)),
    ("DATA", "Fair value adjustment of loans and advances to customers - amortisation", (None, None, -1554, None, -1554)),
    ("DATA", "Shares issued, net of expenses", (8000, None, None, None, 8000)),
    ("TOTAL", "As at 31 December 2025", (200999, 2788, 85444, -101301, 187930)),
]

bw.add_equity_changes_sheet(
    title="Tandem Bank Limited — Statement of Changes in Equity",
    subtitle="Bank (Company-only) basis, £'000. Chronological, oldest to newest. See source note at bottom (FY2022/FY2023 restatement).",
    headers=EQUITY_HEADERS,
    rows=equity_rows,
    sources_text=statement_sources("25 (2025)/26 (2024 comparative)", "24 (2025)/25 (2024 comparative)", "26 (2025)/27 (2024 comparative)"),
    source_height=300,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Loss on operating activities before tax", {"FY2022": -6933, "FY2021": -18030}),
    ("DATA", "Non-cash items included in loss on operating activities before tax", {"FY2022": 11707, "FY2021": 2173}),
    ("DATA", "Change in operating assets and liabilities", {"FY2022": 304576, "FY2021": 217383}),
    ("TOTAL", "Net Cash Generated from Operating Activities", {"FY2022": 309350, "FY2021": 201526}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "(Purchase)/sale of debt securities", {"FY2022": -61572, "FY2021": -2075}),
    ("TOTAL", "Net Cash Used in Investing Activities", {"FY2022": -61572, "FY2021": -2075}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Proceeds from issuance of ordinary shares", {"FY2022": 76464, "FY2021": 12309}),
    ("TOTAL", "Net Cash Generated from Financing Activities", {"FY2022": 76464, "FY2021": 12309}),
    ("TOTAL", "Net Increase in Cash and Cash Equivalents", {"FY2022": 324242, "FY2021": 211760}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2022": 376688, "FY2021": 164928}),
    ("TOTAL", "Cash and Cash Equivalents at the end of the Year", {"FY2022": 700930, "FY2021": 376688}),
]

bw.add_cash_flow_sheet(
    title="Tandem Bank Limited — Statement of Cash Flows",
    subtitle="Bank (Company-only) basis, £'000. FY2023-FY2025 blank - see source note at bottom (FRS 102 cash-flow exemption).",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=72,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Asset Quality
# ---------------------------------------------------------------
aq_rows = [
    ("SECTION", "Gross Loans and Advances to Customers by Product", {}),
    ("DATA", "First charge mortgages", {"FY2025": 126826, "FY2024": 156342, "FY2023": 213554}),
    ("DATA", "Second charge mortgages", {"FY2025": 517524, "FY2024": 508609, "FY2023": 580850}),
    ("DATA", "Motor finance hire purchase receivables", {"FY2025": 323027, "FY2024": 223688, "FY2023": 115554}),
    ("DATA", "Secured lending (product-level split not disclosed pre-FY2023 - see source note)", {"FY2022": 692093, "FY2021": 262023}),
    ("DATA", "Unsecured lending", {"FY2025": 366008, "FY2024": 373406, "FY2023": 407597, "FY2022": 434784, "FY2021": 182894}),
    ("TOTAL", "Gross Loans and Advances to Customers", {"FY2025": 1333385, "FY2024": 1262045, "FY2023": 1317555, "FY2022": 1126877, "FY2021": 444917}),
    ("SECTION", "Credit Quality Analysis", {}),
    ("DATA", "Total gross impaired loans", {"FY2025": 135788, "FY2024": 109289, "FY2023": 71399, "FY2022": 47188, "FY2021": 8443}),
    ("DATA", "Past due but not impaired", {"FY2025": 1289, "FY2024": 16658, "FY2023": 17441, "FY2022": 11604, "FY2021": 13074}),
    ("DATA", "Neither past due nor impaired", {"FY2025": 1196308, "FY2024": 1136098, "FY2023": 1228715, "FY2022": 1068085, "FY2021": 423400}),
    ("TOTAL", "Total gross amount due", {"FY2025": 1333385, "FY2024": 1262045, "FY2023": 1317555, "FY2022": 1126877, "FY2021": 444917}),
    ("SECTION", "Impairment and Coverage", {}),
    ("DATA", "Provision for impairment", {"FY2025": -53848, "FY2024": -40875, "FY2023": -30460, "FY2022": -26381, "FY2021": -5834}),
    ("DATA", "Fair value adjustments (hedge accounting / acquisition of loan portfolio)", {"FY2025": 5364, "FY2024": -1914, "FY2023": -6199, "FY2022": -22127, "FY2021": -2238}),
    ("TOTAL", "Net Loans and Advances to Customers", {"FY2025": 1284901, "FY2024": 1219256, "FY2023": 1280896, "FY2022": 1078369, "FY2021": 436845}),
    ("DATA", "NPL ratio (impaired loans / gross loans)", {"FY2025": "10.18%", "FY2024": "8.66%", "FY2023": "5.42%", "FY2022": "4.19%", "FY2021": "1.90%"}),
    ("DATA", "Coverage ratio (provision / impaired loans)", {"FY2025": "39.65%", "FY2024": "37.40%", "FY2023": "42.66%", "FY2022": "55.90%", "FY2021": "69.10%"}),
]

bw.add_asset_quality_sheet(
    title="Tandem Bank Limited — Asset Quality",
    subtitle="Bank (Company-only) basis, £'000. NPL/coverage ratios derived from the figures above.",
    rows=aq_rows,
    sources_text=(
        "Sources - all figures are Tandem Bank Limited's own (Company-only, not TML Group) figures, £'000:\n"
        f"FY2025/FY2024: Annual Report and Accounts for the year ended 31 December 2025, Note 11 (Loans and "
        f"Advances to Customers) and Note 25.1(ii) (Credit Risk - Credit Quality Analysis) - {AR2025_URL}\n"
        f"FY2023: Annual Report and Accounts for the year ended 31 December 2023, Note 11 and Note 24.1(ii) - "
        f"{AR2023_URL}\n"
        f"FY2022: Annual Report and Accounts for the year ended 31 December 2022, Note 14 and Note 29.1(ii) - as "
        f"originally reported, NOT the FY2023 Annual Report's later restated comparative - {AR2022_URL}\n"
        f"FY2021: as reported in the FY2022 Annual Report's own comparative column, Note 14 and Note 29.1(ii); "
        f"cross-checked against the FY2021 Annual Report's own Note 11 and Note 25.1 figures and matched exactly "
        f"- {AR2021_URL}\n"
        "The product breakdown (First/Second charge mortgages, Motor finance hire purchase receivables, "
        "Unsecured lending) was only introduced from the FY2023 Annual Report onward; FY2022 and FY2021 are "
        "shown here on the Bank's own then-current Secured/Unsecured split (blank cells above indicate the "
        "sub-product breakdown did not exist that year, not a missing figure - the Unsecured lending row and "
        "product-level Secured total both tie to Gross Loans and Advances to Customers for those years). "
        "'Fair value adjustments' combines the hedge-accounting fair value adjustment and, from FY2021 onward, "
        "the acquisition-of-loan-portfolio fair value adjustment recognised on the Bank's 2024 repurchase of a "
        "mortgage portfolio from a related-party SPE (see Note 11 of the FY2025 Annual Report) - both are "
        "disclosed as a single combined 'Fair value adjustment for portfolio hedged risk' line pre-FY2025.\n\n"
        + ENTITY_NOTE
    ),
    first_col_width=68,
    source_height=300,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"TML Group basis, {unit}" if unit else "TML Group basis",
                         rows_data, sources_text, note=note, first_col_width=48, source_height=170)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 168224, "FY2024": 165574, "FY2023": 150158, "FY2022": 119883, "FY2021": 39742})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWEA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "15.53%", "FY2024": "17.40%", "FY2023": "16.1%", "FY2022": "15.2%", "FY2021": "14.2%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2025": 168224, "FY2024": 165574, "FY2023": 150158, "FY2022": 119883, "FY2021": 39742})],
    p3_sources(),
    note="Tier 1 Capital = CET1 Capital every year through FY2022 (no AT1 instruments); AT1 capital was first "
         "issued in FY2023 but is included within Total Capital, not Tier 1, per the Group's own KM1 template "
         "(rows 1 and 2 are identical every year) - Total Capital is the row where AT1/T2 shows up as a difference.",
)

metric(
    "Tier 1 Ratio", "% of RWEA",
    [("Tier 1 ratio", {"FY2025": "15.53%", "FY2024": "17.40%", "FY2023": "16.1%", "FY2022": "15.2%", "FY2021": "14.2%"})],
    p3_sources(),
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2025": 196155, "FY2024": 192343, "FY2023": 175438, "FY2022": 119883, "FY2021": 39742})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWEA",
    [("Total capital ratio", {"FY2025": "18.11%", "FY2024": "20.21%", "FY2023": "18.8%", "FY2022": "15.2%", "FY2021": "14.2%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted assets (RWEA)", {"FY2025": 1083333, "FY2024": 951607, "FY2023": 931650, "FY2022": 790158, "FY2021": 280843})],
    p3_sources(),
)

bw.add_not_disclosed_metric_sheets(
    ["RWA Breakdown"],
    p3_sources(),
    per_note={
        "RWA Breakdown": "TML's Pillar 3 Disclosures do not include a UK OV1-style RWA breakdown-by-risk-category "
                          "table in any year FY2021-FY2025 (all 4 available editions checked directly - each is a "
                          "short document, 9-15 pages, consistent with the Group's stated 'small, non-complex' "
                          "institution status under UK CRR Article 4(145) and the reduced Pillar 3 disclosure "
                          "regime of Article 433(b), the same basis already noted for MREL Ratio's non-disclosure).",
    },
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Total exposure measure excluding claims on central banks", {"FY2025": 1860727, "FY2024": 1652240, "FY2023": 1458860, "FY2022": 1401205, "FY2021": 859746}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "9.04%", "FY2024": "10.02%", "FY2023": "9.8%", "FY2022": "8.8%", "FY2021": "4.6%"}),
    ],
    p3_sources(),
    note="FY2021's Pillar 3 report predates the 'excluding claims on central banks' UK leverage framework "
         "(introduced Jan 2021 but not yet reflected in TML's own template that year) - its Table LRCom shows a "
         "single 'Total Leverage Ratio Exposures' / 'Leverage Ratio' figure (859,746 / 4.6%), shown here on the "
         "'excluding' row for comparability with later years, though it is not confirmed to be on an identical "
         "basis. The FY2024 Pillar 3 report's own comparative column restates FY2023's exposure measure to "
         "1,529,033 (footnoted 'Restated'); the figure shown here for FY2023 (1,458,860 / 9.8%) is as originally "
         "reported in the FY2023 Pillar 3 Disclosures itself, not the later restated comparative.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value (average)", {"FY2025": 1148813, "FY2024": 1927554, "FY2023": 1786879, "FY2022": 329806}),
        ("Total net cash outflows, adjusted value", {"FY2025": 258152, "FY2024": 359743, "FY2023": 281464, "FY2022": 103147}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "443.40%", "FY2024": "534.75%", "FY2023": "636.0%", "FY2022": "314.1%", "FY2021": "331%"}),
    ],
    p3_sources(),
    note="FY2022-FY2025 LCR is a simple average of monthly liquidity positions during the calendar year (per each "
         "report's own footnote). FY2021 used a different methodology (simple average of month-end observations "
         "over the trailing 12 months up to each quarter-end); the Group's FY2021 report only tabulates quarterly "
         "LCR values (31%: Dec '21 = 331%, Sep '21 = 394%, Jun '21 = 709%, Mar '21 = 1,832%) rather than one "
         "annual figure - the 31 Dec 2021 (year-end) value is shown here for comparability, but the two "
         "methodologies are not identical so a direct FY2021-to-FY2022 LCR comparison should be treated with "
         "caution. No HQLA/cash-outflow £ breakdown was found for FY2021 (only the % ratio was tabulated).",
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding", {"FY2025": 2560820, "FY2024": 3156347, "FY2023": 3142854, "FY2022": 1447618}),
        ("Total required stable funding", {"FY2025": 1320668, "FY2024": 1199958, "FY2023": 1156379, "FY2022": 922410}),
        ("NSFR ratio (%)", {"FY2025": "194.30%", "FY2024": "263.10%", "FY2023": "270.6%", "FY2022": "155.5%", "FY2021": "Not disclosed"}),
    ],
    p3_sources(),
    note="NSFR not disclosed for FY2021 - not yet part of TML's Pillar 3 template that year (consistent with the "
         "UK NSFR requirement not applying to reporting periods that early elsewhere in this project, e.g. Zopa).",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={
        "MREL Ratio": "MREL is not disclosed in any of TML's Pillar 3 Disclosures FY2021-FY2025. The Group states "
                       "(FY2023 Pillar 3 Disclosures, Overview) that it qualifies as a 'small, non-complex' "
                       "institution under UK CRR Article 4(145) and follows the reduced Pillar 3 disclosure regime "
                       "of Article 433(b) - consistent with, though not an explicit stated reason for, the absence "
                       "of any MREL figure.",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 2489828, "FY2024": 3155197, "FY2023": 3859400, "FY2022": 1926197, "FY2021": 853719}),
        ("Loans and advances to customers", {"FY2025": 1284901, "FY2024": 1219256, "FY2023": 1280896, "FY2022": 1078369, "FY2021": 436845}),
        ("Customer accounts", {"FY2025": 2260738, "FY2024": 2916365, "FY2023": 3639407, "FY2022": 1754868, "FY2021": 771161}),
        ("Total equity", {"FY2025": 187930, "FY2024": 177679, "FY2023": 156571, "FY2022": 115178, "FY2021": 41620}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total Income", {"FY2025": 86097, "FY2024": 80410, "FY2023": 75912, "FY2022": 57227, "FY2021": 14802}),
        ("Administrative expenses (Operating Expenses)", {"FY2025": -64142, "FY2024": -62957, "FY2023": -62045, "FY2022": -52218, "FY2021": -30508}),
        ("Profit/(Loss) for the Year", {"FY2025": 3458, "FY2024": 11512, "FY2023": 3600, "FY2022": -1654, "FY2021": -17853}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 177679, "FY2024": 156571, "FY2023": 115535, "FY2022": 41620, "FY2021": 47018}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": 3805, "FY2024": 12034, "FY2023": 4240, "FY2022": -1728, "FY2021": -17707}),
        ("Other equity movements, net", {"FY2025": 6446, "FY2024": 9074, "FY2023": 36796, "FY2022": 75286, "FY2021": 12309}),
        ("Closing equity", {"FY2025": 187930, "FY2024": 177679, "FY2023": 156571, "FY2022": 115178, "FY2021": 41620}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2022": 309350, "FY2021": 201526}),
        ("Net cash from/(used in) investing activities", {"FY2022": -61572, "FY2021": -2075}),
        ("Net cash from/(used in) financing activities", {"FY2022": 76464, "FY2021": 12309}),
        ("Cash and cash equivalents at end of year", {"FY2022": 700930, "FY2021": 376688}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "15.53%", "FY2024": "17.40%", "FY2023": "16.1%", "FY2022": "15.2%", "FY2021": "14.2%"}),
        ("Tier 1 Ratio", {"FY2025": "15.53%", "FY2024": "17.40%", "FY2023": "16.1%", "FY2022": "15.2%", "FY2021": "14.2%"}),
        ("Total Capital Ratio", {"FY2025": "18.11%", "FY2024": "20.21%", "FY2023": "18.8%", "FY2022": "15.2%", "FY2021": "14.2%"}),
        ("Leverage Ratio", {"FY2025": "9.04%", "FY2024": "10.02%", "FY2023": "9.8%", "FY2022": "8.8%", "FY2021": "4.6%"}),
        ("LCR", {"FY2025": "443.40%", "FY2024": "534.75%", "FY2023": "636.0%", "FY2022": "314.1%", "FY2021": "331%"}),
        ("NSFR", {"FY2025": "194.30%", "FY2024": "263.10%", "FY2023": "270.6%", "FY2022": "155.5%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Cash flow is blank for FY2023-FY2025 (FRS 102 qualifying-"
         "entity exemption took effect from FY2023 - see Cash Flow Statement sheet note) and ratios are on a wider "
         "TML Group basis, not Tandem Bank Limited solo (see each Pillar 3 sheet's source note) - two different, "
         "independently-documented basis differences within this single workbook.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/TANDEM FINANCIALS.xlsx")
