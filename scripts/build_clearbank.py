import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://clear.bank/uploads/assets/ClearBank-Annual-Report-2025.pdf"
AR2023_URL = "https://clear.bank/uploads/assets/ClearBank-Annual-Report-and-Accounts-2023.pdf"
AR2022_URL = "https://clear.bank/uploads/assets/ClearBank-Annual-Report-and-Accounts_2022.pdf"
AR2021_URL = "https://clear.bank/uploads/assets/ClearBank-Annual-Report-2021.pdf"
P3_2025_URL = "https://clear.bank/uploads/assets/ClearBank-Pillar-3-2025.pdf"
P3_2023_URL = "https://clear.bank/uploads/assets/ClearBank-Pillar-3-Disclosure-2023.pdf"
P3_2022_URL = "https://clear.bank/uploads/assets/ClearBank-Pillar-3-2022.pdf"
P3_2021_URL = "https://clear.bank/uploads/assets/ClearBank-Pillar-3-disclosure-2021.pdf"
CBGH_FY2023_URL = "https://find-and-update.company-information.service.gov.uk/company/14254435/filing-history/MzQyMTUzMzg4NGFkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "ClearBank Limited (FRN 754568, company 09736376), a UK clearing/embedded-banking "
    "infrastructure bank. Group basis throughout (parent-only figures are not materially "
    "different - the Group is essentially the Bank plus dormant/minor subsidiaries). Does NOT "
    "take the FRS 101/102 cash-flow-statement exemption - full Consolidated Statement of Cash "
    "Flows every year.\n"
    "FY2022's own figures (from the FY2022 Annual Report itself) are used here rather than "
    "FY2023's report's restated FY2022 comparative (Note 32 of the FY2023 report flags a "
    "restatement, e.g. profit for the year after tax 6,818 as originally reported vs. 10,760 "
    "restated, and net cash from operating activities 413,627 vs. 416,088 restated) - each "
    "year's own originally-published figures are used throughout this workbook, per project "
    "convention.\n"
    "A genuine, small, undocumented cross-vintage gap exists between FY2023's own closing cash "
    "balance (£6,256,126k) and FY2024's own opening balance per the FY2025 Annual Report's "
    "comparative (£6,258,123k) - a ~£1,997k difference with no explanation found in either "
    "source; both figures are shown exactly as each report states them, not force-reconciled.\n"
    "\"Foreign currency differences\" appears twice with different values in the FY2025/FY2024 "
    "presentation - once within the non-cash adjustments (a small figure) and again within the "
    "working-capital-changes section (a much larger figure driven by FX movement on customer "
    "deposit balances) - both are genuine distinct line items in the source, not a duplicate."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are ClearBank Limited's own Consolidated Statement of Cash Flows:\n"
    "FY2025/FY2024: ClearBank Annual Report and Accounts 2025, p.71 - " + AR2025_URL + "\n"
    "FY2023: ClearBank Annual Report and Accounts 2023, p.73 - " + AR2023_URL + "\n"
    "FY2022: ClearBank Annual Report and Accounts 2022, p.43 (own originally-published figures, "
    "not FY2023's restated comparative) - " + AR2022_URL + "\n"
    "FY2021: ClearBank Annual Report and Accounts 2021, p.66 - " + AR2021_URL + "\n\n"
    + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - ClearBank Group Pillar 3 Key Metrics table:\n"
        "FY2025/FY2024: ClearBank Pillar 3 Disclosure 2025, p.15 - " + P3_2025_URL + "\n"
        "FY2023: ClearBank Pillar 3 Disclosure 2023, p.5-6 - " + P3_2023_URL + "\n"
        "FY2022/FY2021: ClearBank Pillar 3 Disclosure 2022, p.4-5 (FY2021 as the FY2022 "
        "document's own comparative column, cross-checked against ClearBank Pillar 3 Disclosure "
        "2021's own Table 1/Table 2 - CET1 140%/£36,739k there vs. 139.70%/£37m here, consistent "
        "to rounding) - " + P3_2022_URL + " and " + P3_2021_URL + "\n"
        "CET1 = Tier 1 = Total Capital every year (no AT1/Tier 2 instruments). MREL not "
        "disclosed anywhere in any Pillar 3 document reviewed, no reason given.\n"
        "LEVERAGE RATIO BASIS NOTE: FY2021's own Pillar 3 document (Table 1) discloses two "
        "different leverage figures with materially different values - a \"CRD leverage ratio\" "
        "of 1% and a \"UK leverage ratio\" of 39%, reflecting genuinely different exposure-measure "
        "definitions, not a typo. The 38.79% figure used here for FY2021 (from the FY2022 "
        "document's comparative, \"excluding claims on central banks\" basis) matches the UK "
        "leverage ratio figure, consistent with the basis used FY2022 onward."
    )


bw = BankWorkbook(bank_name="ClearBank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="E47F85")

# ---------------------------------------------------------------
# Statements sources / notes
# ---------------------------------------------------------------
STATEMENTS_ENTITY_NOTE = (
    "ENTITY-CHANGE NOTE (corrected on follow-up review against ClearBank Group Holdings "
    "Limited's own FY2023 Companies House filing, company 14254435): FY2021-FY2023 figures "
    "are ClearBank Limited's own statements (Companies House 09736376). FY2024/FY2025 "
    "figures are instead from the Annual Report and Accounts 2025, whose auditor's report "
    "and Statement of Financial Position are addressed to \"ClearBank Group Holdings "
    "Limited\" - a NEW intermediate holding entity (incorporated 25 July 2022) inserted "
    "above ClearBank Limited DURING FY2023, not between FY2023 and FY2024 as an earlier "
    "pass of this workbook stated. Per that entity's own first Group accounts (period ended "
    "31 December 2023, filed at Companies House 18 May 2024 - " + CBGH_FY2023_URL + "), its "
    "inaugural subsidiary ClearBank Europe N.V. was incorporated 6 March 2023; it acquired "
    "100% of ClearBank Limited on 8 December 2023 as a Business Combination Under Common "
    "Control, with ClearBank Limited's results consolidated from 1 May 2023 (the day after "
    "common control was established, 30 April 2023). \"CB Growth Holdings Limited\" (named "
    "in AR2023's own equity note 3, and confirmed in ClearBank Group Holdings Limited's own "
    "Note 1.4 as \"its parent\") is a GENUINELY SEPARATE, higher entity in the group chain - "
    "not an earlier name for ClearBank Group Holdings Limited (no Companies House "
    "previous-names record exists for company 14254435, and its own filing history shows no "
    "rename). The corrected chain, top to bottom, is: CB Growth Holdings Limited -> "
    "ClearBank Group Holdings Limited (14254435) -> ClearBank Limited. This is a genuine "
    "change of reporting entity, not a presentation choice: the Statement of Changes in "
    "Equity's FY2024 opening balance (£196,497k) does not equal FY2023's own closing balance "
    "(£129,526k) below, and the two entities' equity bases are not directly comparable, so no "
    "plug/bridging row is used across that boundary in this sheet. However, a genuine bridge "
    "DOES exist and is now cited for traceability: ClearBank Group Holdings Limited's own "
    "stub-period Consolidated statement of changes in equity (in the filing above) runs from "
    "£(812)k total equity at 1 March 2023 (its own first reporting date) to exactly £196,497k "
    "at 31 December 2023 - i.e. this workbook's existing FY2024 opening figure is that "
    "entity's own closing balance for its first, ~10-month accounting period, built mostly "
    "from a £179,405k share capital issuance (the mechanism for the ClearBank Limited "
    "acquisition) rather than organic trading profit. This bridging period is not added as "
    "its own column here since it doesn't align with this workbook's FY-year grid, but the "
    "£196,497k figure is now independently verified against its true source rather than only "
    "appearing as an unexplained opening balance. Balance Sheet and P&L totals for each year "
    "are still internally consistent (assets = liabilities + equity; income - expenses = "
    "profit/loss) since each is a same-entity, same-year snapshot - only the cross-year "
    "equity roll-forward is affected. FY2023's own Statement of Financial Position/"
    "Comprehensive Income are Company-only (ClearBank Limited did not publish Consolidated "
    "statements that year - see the Company vs Consolidated presentation note below); "
    "FY2021/FY2022/FY2024/FY2025 are Consolidated. Per project convention, each year's own "
    "originally-published figures are used throughout (FY2022's own AR2022 Consolidated "
    "figures, not AR2023's restated comparative - see CASH_FLOW_SOURCES' existing "
    "ENTITY_NOTE for the same convention applied to Cash Flow)."
)

PRESENTATION_NOTE = (
    "PRESENTATION NOTE: FY2021's own Statement of Comprehensive Income discloses only Net "
    "interest income and Net fee income (no separate Interest income/expense or Fee "
    "income/expense split) - per AR2022's own footnote, \"In 2021, only net interest income "
    "and net fee income were presented without splitting for gross amounts.\" FY2023's own "
    "Statement of Comprehensive Income additionally has an \"Expenses recharged\" line "
    "(income, not cost) not present in any other year, resulting in a positive \"Operating "
    "profit\" that year rather than the \"Operating loss\" label used elsewhere - both "
    "reproduced as reported. Balance Sheet: \"Loans and advances to banks\" (an interbank "
    "placement, not a customer loan) appears as its own line FY2021-FY2023 only - dropped "
    "from FY2024/FY2025's presentation (folded into Cash and cash equivalents per the "
    "Group's own accounting policy note). \"Due from UK tax authorities\" (FY2022/FY2023) "
    "and \"Current tax asset\" (FY2024/FY2025) are the same concept under different labels; "
    "FY2021 has neither line. Equity: \"Share-based payment reserve\" (FY2021/FY2022) was "
    "replaced by \"Capital contribution reserve\" from FY2023 onward (see the entity-change "
    "note above); \"Treasury shares\" and \"Translation reserve\" are absent from FY2023's "
    "Company-only presentation, present in every other year's Consolidated presentation."
)

STATEMENTS_SOURCES = (
    "Sources - ClearBank's own Statement of Comprehensive Income / Statement of Financial "
    "Position / Statement of Changes in Equity, transcribed from each year's own report:\n"
    "FY2025/FY2024: Consolidated statements, ClearBank Group Holdings Limited Annual Report "
    "and Accounts 2025, pp.68-70 - " + AR2025_URL + "\n"
    "FY2023: Company statements (no Consolidated statements published that year), ClearBank "
    "Annual Report and Accounts 2023, pp.69-72 - " + AR2023_URL + "\n"
    "FY2022: Consolidated statements, own originally-published figures (not FY2023's "
    "restated comparative - see Note 32 of the FY2023 report), ClearBank Annual Report and "
    "Accounts 2022, pp.80-83 - " + AR2022_URL + "\n"
    "FY2021: Consolidated statements, ClearBank Limited Annual Report and Accounts 2021, "
    "pp.60-63 - " + AR2021_URL + "\n\n"
    + STATEMENTS_ENTITY_NOTE + "\n\n" + PRESENTATION_NOTE
)

RWA_SOURCES = (
    "Sources - ClearBank Group Pillar 3 \"Overview of RWA\"/\"Overview of risk weighted "
    "exposure amounts\" table:\n"
    "FY2025/FY2024: ClearBank Pillar 3 Disclosure 2025, p.18 - " + P3_2025_URL + "\n"
    "FY2023: ClearBank Pillar 3 Disclosure 2023, p.11 (ClearBank Group column) - " + P3_2023_URL + "\n"
    "FY2022: ClearBank Pillar 3 disclosure 2022, p.15 (own originally-published figures, not "
    "FY2023's restated comparative - see note below) - " + P3_2022_URL + "\n"
    "FY2021: ClearBank Pillar 3 disclosure 2022, p.15 (FY2021 comparative column) - " + P3_2022_URL + "\n\n"
    "Only two risk categories are disclosed in any year: Credit risk (excluding CCR, "
    "Standardised Approach) and Operational risk (Basic Indicator Approach) - no market risk, "
    "CCR, or CVA charge in any year (consistent with a clearing/embedded-banking bank with no "
    "trading book).\n"
    "FY2024's Total here (£212m = £34m + £178m) is £1m higher than the FY2024 figure on this "
    "workbook's own Total RWAs sheet (£211m) - an immaterial rounding artifact in ClearBank's "
    "own Pillar 3 table, reproduced as disclosed rather than force-matched.\n"
    "RESTATEMENT NOTE: ClearBank's own FY2022 Pillar 3 disclosure (2022 edition) states "
    "Operational risk RWA of £22m (Total £38m), matching this workbook's existing Total RWAs "
    "sheet. The FY2023 Pillar 3 disclosure's own FY2022 comparative column instead shows "
    "Operational risk RWA of £55m (Total £71m) - a large restatement between Pillar 3 "
    "vintages with no explanation given. Per project convention, FY2022's own "
    "originally-published figures (£16m credit / £22m operational / £38m total) are used "
    "here, not the later restated comparative."
)

ASSET_QUALITY_SOURCES = (
    "Sources - ClearBank's own \"Credit risk\" and \"Impairment of financial assets\" notes "
    "(Note 21/2.6), read in full for all 5 years:\n"
    "FY2025/FY2024: ClearBank Group Holdings Limited Annual Report and Accounts 2025, pp.77,88 "
    "- " + AR2025_URL + "\n"
    "FY2023: ClearBank Annual Report and Accounts 2023, credit risk/impairment notes - " + AR2023_URL + "\n"
    "FY2022/FY2021: ClearBank Annual Report and Accounts 2022, credit risk/impairment notes - " + AR2022_URL + "\n\n"
    "GENUINE STRUCTURAL FINDING, NOT A DATA GAP: ClearBank does not lend to customers at "
    "all. Its own FY2025 Annual Report states plainly: \"The Group does not provide any "
    "credit facilities which are not fully collateralised to its customers and is therefore "
    "not exposed to associated credit risks\" and \"the Group's trade receivables and hence "
    "ECL are immaterial, with no further ECL-related disclosures considered necessary by "
    "management.\" This wording (or its equivalent) recurs across all 5 years reviewed. "
    "There is therefore no customer loan book, no IFRS 9 stage split, and no loss allowance "
    "of any kind recognised in any year - ClearBank's only credit exposure is to its treasury "
    "counterparties (predominantly the Bank of England) and to collateral it holds FROM "
    "clients (an asset-side benefit, not a risk), both deemed low/immaterial risk by the "
    "Group's own policy. \"Loans and advances to banks\" on the Balance Sheet (FY2021-FY2023 "
    "only, see Presentation Note on the Balance Sheet sheet) is an interbank treasury "
    "placement, not customer lending."
)


# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents",
     {"FY2025": 17956976, "FY2024": 10961293, "FY2023": 6256126, "FY2022": 3125862, "FY2021": 2720797}),
    ("DATA", "Loans and advances to banks",
     {"FY2023": 19525, "FY2022": 9156, "FY2021": 5962}),
    ("DATA", "Collateral placed",
     {"FY2025": 509, "FY2024": 1368, "FY2023": 1352, "FY2022": 433, "FY2021": 406}),
    ("DATA", "Receivables",
     {"FY2025": 17296, "FY2024": 10408, "FY2023": 9768, "FY2022": 6212, "FY2021": 4478}),
    ("DATA", "Current tax asset / due from UK tax authorities",
     {"FY2025": 1563, "FY2024": 753, "FY2023": 3542, "FY2022": 4363}),
    ("DATA", "Right-of-use asset",
     {"FY2025": 549, "FY2024": 2111, "FY2023": 952, "FY2022": 2677, "FY2021": 510}),
    ("DATA", "Property, plant and equipment",
     {"FY2025": 0, "FY2024": 34, "FY2023": 97, "FY2022": 566, "FY2021": 451}),
    ("DATA", "Intangible assets",
     {"FY2025": 51683, "FY2024": 52670, "FY2023": 41806, "FY2022": 29184, "FY2021": 27479}),
    ("DATA", "Deferred tax asset",
     {"FY2025": 39779, "FY2024": 35426, "FY2023": 33682, "FY2022": 25956, "FY2021": 12525}),
    ("TOTAL", "Total assets",
     {"FY2025": 18068355, "FY2024": 11064063, "FY2023": 6366850, "FY2022": 3204409, "FY2021": 2772608}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer deposits",
     {"FY2025": 17826803, "FY2024": 10818568, "FY2023": 6147363, "FY2022": 2982259, "FY2021": 2644756}),
    ("DATA", "Other payables",
     {"FY2025": 27067, "FY2024": 20708, "FY2023": 82372, "FY2022": 109307, "FY2021": 9897}),
    ("DATA", "Lease obligations",
     {"FY2025": 1256, "FY2024": 2219, "FY2023": 1003, "FY2022": 2789, "FY2021": 509}),
    ("DATA", "Deferred income",
     {"FY2025": 390, "FY2024": 277, "FY2023": 6444, "FY2022": 22742, "FY2021": 45229}),
    ("DATA", "Current tax liability", {"FY2023": 142}),
    ("TOTAL", "Total liabilities",
     {"FY2025": 17855516, "FY2024": 10841772, "FY2023": 6237324, "FY2022": 3117097, "FY2021": 2700391}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 2, "FY2024": 2}),
    ("DATA", "Share premium",
     {"FY2025": 224403, "FY2024": 224403, "FY2023": 203445, "FY2022": 192349, "FY2021": 191816}),
    ("DATA", "Treasury shares", {"FY2022": -204, "FY2021": -204}),
    ("DATA", "Capital contribution reserve", {"FY2025": 11942, "FY2024": 9188, "FY2023": 26805}),
    ("DATA", "Share-based payment reserve", {"FY2022": 24933, "FY2021": 17190}),
    ("DATA", "Retained earnings/(losses)",
     {"FY2025": -24512, "FY2024": -10518, "FY2023": -100724, "FY2022": -129650, "FY2021": -136468}),
    ("DATA", "Translation reserve",
     {"FY2025": 1004, "FY2024": -784, "FY2022": -116, "FY2021": -117}),
    ("TOTAL", "Total equity",
     {"FY2025": 212839, "FY2024": 222291, "FY2023": 129526, "FY2022": 87312, "FY2021": 72217}),
    ("TOTAL", "Total liabilities and equity",
     {"FY2025": 18068355, "FY2024": 11064063, "FY2023": 6366850, "FY2022": 3204409, "FY2021": 2772608}),
]

bw.add_balance_sheet_sheet(
    title="ClearBank — Consolidated Statement of Financial Position",
    subtitle="£'000. FY2023 is Company-only (no Consolidated statements published that year). See source note at bottom.",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=54,
    source_height=380,
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income",
     {"FY2025": 625779, "FY2024": 425289, "FY2023": 243956, "FY2022": 43774}),
    ("DATA", "Interest expense",
     {"FY2025": -554816, "FY2024": -358179, "FY2023": -162042, "FY2022": -9911}),
    ("TOTAL", "Net interest income",
     {"FY2025": 70963, "FY2024": 67110, "FY2023": 81914, "FY2022": 33863, "FY2021": 1842}),
    ("DATA", "Fee income",
     {"FY2025": 66183, "FY2024": 47141, "FY2023": 31390, "FY2022": 25455}),
    ("DATA", "Fee expenses",
     {"FY2025": -5268, "FY2024": -2952, "FY2023": -2620, "FY2022": -1047}),
    ("TOTAL", "Net fee income",
     {"FY2025": 60915, "FY2024": 44189, "FY2023": 28770, "FY2022": 24408, "FY2021": 18614}),
    ("DATA", "Other income",
     {"FY2025": 806, "FY2024": 787, "FY2023": 663, "FY2022": 13, "FY2021": 938}),
    ("TOTAL", "Total income",
     {"FY2025": 132684, "FY2024": 112086, "FY2023": 111347, "FY2022": 58284, "FY2021": 21394}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Staff costs",
     {"FY2025": -78740, "FY2024": -67335, "FY2023": -55318, "FY2022": -40095, "FY2021": -27719}),
    ("DATA", "Depreciation",
     {"FY2025": -2265, "FY2024": -1693, "FY2023": -2212, "FY2022": -1334, "FY2021": -2145}),
    ("DATA", "Amortisation of intangibles",
     {"FY2025": -15706, "FY2024": -11643, "FY2023": -8869, "FY2022": -7824, "FY2021": -5791}),
    ("DATA", "Impairment",
     {"FY2025": -936, "FY2024": -1584, "FY2023": -268, "FY2022": -675, "FY2021": -337}),
    ("DATA", "Other operating expenses",
     {"FY2025": -51287, "FY2024": -39780, "FY2023": -39116, "FY2022": -27710, "FY2021": -16447}),
    ("TOTAL", "Operating expenses",
     {"FY2025": -148934, "FY2024": -122035, "FY2023": -105783, "FY2022": -77638, "FY2021": -52439}),
    ("DATA", "Expenses recharged", {"FY2023": 13054, "FY2022": 8587}),
    ("TOTAL", "Operating profit/(loss)",
     {"FY2025": -16250, "FY2024": -9949, "FY2023": 18618, "FY2022": -10767, "FY2021": -31045}),
    ("DATA", "Other gains/(losses)",
     {"FY2025": -354, "FY2024": -165, "FY2023": -111, "FY2022": -181, "FY2021": 5}),
    ("DATA", "Finance costs",
     {"FY2025": -106, "FY2024": -130, "FY2023": -78, "FY2022": -55, "FY2021": -34}),
    ("TOTAL", "Profit/(loss) for the year before taxation",
     {"FY2025": -16710, "FY2024": -10244, "FY2023": 18429, "FY2022": -11003, "FY2021": -31074}),
    ("DATA", "Taxation",
     {"FY2025": 945, "FY2024": -74, "FY2023": 3967, "FY2022": 17821, "FY2021": 2874}),
    ("TOTAL", "Profit/(loss) for the year after taxation",
     {"FY2025": -15765, "FY2024": -10318, "FY2023": 22396, "FY2022": 6818, "FY2021": -28200}),
    ("SECTION", "Other comprehensive income/(loss)", {}),
    ("DATA", "Foreign currency translation differences",
     {"FY2025": 1788, "FY2024": -767, "FY2022": 1, "FY2021": -1}),
    ("TOTAL", "Total comprehensive income/(loss) for the year",
     {"FY2025": -13977, "FY2024": -11085, "FY2023": 22396, "FY2022": 6819, "FY2021": -28201}),
]

bw.add_income_statement_sheet(
    title="ClearBank — Consolidated Statement of Comprehensive Income",
    subtitle="£'000. FY2023 is Company-only (no Consolidated statements published that year). See source note at bottom.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=54,
    source_height=380,
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
EQ_HEADERS = ["Share capital", "Share premium", "Treasury shares", "Share-based payment reserve",
              "Capital contribution reserve", "Retained earnings/(losses)", "Translation reserve",
              "Total equity"]

eq_rows = [
    ("TOTAL", "At 1 January 2021", (None, 157316, -204, 9519, None, -108268, -116, 58247)),
    ("DATA", "Loss for the year (FY2021)", (None, None, None, None, None, -28200, None, -28200)),
    ("DATA", "Other comprehensive loss (FY2021)", (None, None, None, None, None, None, -1, -1)),
    ("DATA", "Issue of share capital (FY2021)", (None, 34500, None, None, None, None, None, 34500)),
    ("DATA", "Share-based payments (FY2021)", (None, None, None, 7671, None, None, None, 7671)),
    ("TOTAL", "At 31 December 2021", (None, 191816, -204, 17190, None, -136468, -117, 72217)),
    ("DATA", "Profit for the year (FY2022)", (None, None, None, None, None, 6818, None, 6818)),
    ("DATA", "Other comprehensive income (FY2022)", (None, None, None, None, None, None, 1, 1)),
    ("DATA", "Issue of share capital (FY2022)", (None, 533, None, None, None, None, None, 533)),
    ("DATA", "Share-based payments (FY2022)", (None, None, None, 7743, None, None, None, 7743)),
    ("TOTAL", "At 31 December 2022", (None, 192349, -204, 24933, None, -129650, -116, 87312)),
    ("DATA", "Note: FY2023's own report is Company-only - Treasury shares/Translation reserve "
             "columns are not disclosed that year (see Presentation Note); the FY2022 closing "
             "balance it re-presents (£87,312k Total) matches the Consolidated total above exactly.",
     (None, None, None, None, None, None, None, None)),
    ("DATA", "Profit for the year (FY2023)", (None, None, None, None, None, 22396, None, 22396)),
    ("DATA", "Issue of share capital (FY2023)", (None, 11300, None, None, None, None, None, 11300)),
    ("DATA", "Share-based payments and reserve transfer (FY2023)",
     (None, None, None, -21408, 26805, 1332, None, 6729)),
    ("DATA", "Tax on share-based payments (FY2023)", (None, None, None, None, None, 1789, None, 1789)),
    ("TOTAL", "At 31 December 2023", (None, 203445, None, None, 26805, -100724, None, 129526)),
    ("DATA", "ENTITY-CHANGE NOTE: a new intermediate parent, ClearBank Group Holdings Limited, "
             "was inserted above ClearBank Limited during FY2023 (business combination under "
             "common control, consolidated from 1 May 2023 - see Sources below) - the FY2024 "
             "opening balance is that new entity's own closing balance for its first reporting "
             "period (to 31 Dec 2023), not a continuation of the row above.",
     (None, None, None, None, None, None, None, None)),
    ("TOTAL", "At 1 January 2024", (2, 189403, None, None, 3511, 3598, -17, 196497)),
    ("DATA", "Loss for the year (FY2024)", (None, None, None, None, None, -10318, None, -10318)),
    ("DATA", "Other comprehensive loss (FY2024)", (None, None, None, None, None, None, -767, -767)),
    ("DATA", "Issue of share capital (FY2024)", (None, 35000, None, None, None, None, None, 35000)),
    ("DATA", "Share-based payments (FY2024)", (None, None, None, None, 5677, 76, None, 5753)),
    ("DATA", "Tax on share-based payments (FY2024)", (None, None, None, None, None, -3874, None, -3874)),
    ("TOTAL", "At 31 December 2024", (2, 224403, None, None, 9188, -10518, -784, 222291)),
    ("DATA", "Loss for the year (FY2025)", (None, None, None, None, None, -15765, None, -15765)),
    ("DATA", "Other comprehensive income (FY2025)", (None, None, None, None, None, None, 1788, 1788)),
    ("DATA", "Share-based payments (FY2025)", (None, None, None, None, 2754, -1187, None, 1567)),
    ("DATA", "Tax on share-based payments (FY2025)", (None, None, None, None, None, 2958, None, 2958)),
    ("TOTAL", "At 31 December 2025", (2, 224403, None, None, 11942, -24512, 1004, 212839)),
]

bw.add_equity_changes_sheet(
    title="ClearBank — Statement of Changes in Equity",
    subtitle="£'000, chronological. Contains a genuine entity-basis break at FY2023/FY2024 - see the notes rows and source note.",
    headers=EQ_HEADERS,
    rows=eq_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=52,
    source_height=380,
)

# ---------------------------------------------------------------
# Sheet: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) for the year after tax",
     {"FY2025": -15765, "FY2024": -10318, "FY2023": 22396, "FY2022": 6818, "FY2021": -28200}),
    ("DATA", "Depreciation of property, plant and equipment",
     {"FY2025": 63, "FY2024": 68, "FY2023": 510, "FY2022": 304, "FY2021": 475}),
    ("DATA", "(Profit)/loss on disposals of property, plant and equipment",
     {"FY2022": -13, "FY2021": 15}),
    ("DATA", "Depreciation of right-of-use assets",
     {"FY2025": 2202, "FY2024": 1624, "FY2023": 1702, "FY2022": 1030, "FY2021": 1670}),
    ("DATA", "Amortisation of intangible assets",
     {"FY2025": 15706, "FY2024": 11643, "FY2023": 8869, "FY2022": 7824, "FY2021": 5791}),
    ("DATA", "Impairment of intangible assets",
     {"FY2025": 936, "FY2024": 1584, "FY2023": 246, "FY2022": 676, "FY2021": 337}),
    ("DATA", "Share-based payment expense",
     {"FY2025": 1567, "FY2024": 5753, "FY2023": 6729, "FY2022": 7743, "FY2021": 7671}),
    ("DATA", "Recognition of right-of-use assets", {"FY2021": 34}),
    ("DATA", "Tax benefit/(charge)",
     {"FY2025": -945, "FY2024": 74, "FY2023": -3967, "FY2022": -17794, "FY2021": -2874}),
    ("DATA", "Finance costs", {"FY2022": 34, "FY2021": 10}),
    ("DATA", "Net interest income",
     {"FY2025": -70963, "FY2024": -67110, "FY2023": -81914, "FY2022": -33863, "FY2021": -1842}),
    ("DATA", "Other income", {"FY2025": -798, "FY2024": -678, "FY2023": -380}),
    ("DATA", "Foreign currency differences (non-cash items)",
     {"FY2025": 30, "FY2024": 18, "FY2023": 43, "FY2022": 1, "FY2021": -1}),
    ("TOTAL", "Operating cash flows before changes in working capital",
     {"FY2025": -67967, "FY2024": -57342, "FY2023": -45766, "FY2022": -27240, "FY2021": -16914}),
    ("DATA", "Increase/(decrease) in collateral",
     {"FY2025": 859, "FY2024": -16, "FY2023": -919, "FY2022": -27, "FY2021": -36}),
    ("DATA", "(Increase)/decrease in loans and advances to banks",
     {"FY2024": 19525, "FY2023": -10369, "FY2022": -3194, "FY2021": -5962}),
    ("DATA", "Increase in receivables",
     {"FY2025": -6288, "FY2024": -1877, "FY2023": -3547, "FY2022": -1734, "FY2021": -294}),
    ("DATA", "Increase/(decrease) in payables",
     {"FY2025": 6359, "FY2024": 46, "FY2023": -26935, "FY2022": 99410, "FY2021": 3306}),
    ("DATA", "Increase/(decrease) in deferred income",
     {"FY2025": 113, "FY2024": -6167, "FY2023": -16298, "FY2022": -24954, "FY2021": -17307}),
    ("DATA", "Increase in customer deposits/amounts due to customers",
     {"FY2025": 7006677, "FY2024": 4654971, "FY2023": 3152204, "FY2022": 335213, "FY2021": 1718866}),
    ("DATA", "Foreign currency differences (working capital)",
     {"FY2025": 5979, "FY2024": -3846}),
    ("TOTAL", "Cash generated by/from operations",
     {"FY2025": 6945732, "FY2024": 4605294, "FY2023": 3048370, "FY2022": 377474, "FY2021": 1681659}),
    ("DATA", "Interest received",
     {"FY2025": 625779, "FY2024": 425289, "FY2023": 243957, "FY2022": 43774, "FY2021": 2056}),
    ("DATA", "Interest paid",
     {"FY2025": -553258, "FY2024": -341945, "FY2023": -149139, "FY2022": -7621}),
    ("DATA", "Tax (paid)/received", {"FY2025": -1062, "FY2024": 2134, "FY2023": -640}),
    ("TOTAL", "Net cash generated from operating activities",
     {"FY2025": 7017191, "FY2024": 4690772, "FY2023": 3142548, "FY2022": 413627, "FY2021": 1683715}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment",
     {"FY2025": -29, "FY2024": -5, "FY2023": -41, "FY2022": -408, "FY2021": -268}),
    ("DATA", "Purchase of intangible assets",
     {"FY2025": -15655, "FY2024": -24091, "FY2023": -21737, "FY2022": -7736, "FY2021": -8356}),
    ("TOTAL", "Net cash used in investing activities",
     {"FY2025": -15684, "FY2024": -24096, "FY2023": -21778, "FY2022": -8144, "FY2021": -8624}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Proceeds from issue of Ordinary Shares",
     {"FY2024": 35000, "FY2023": 11300, "FY2022": 533, "FY2021": 34500}),
    ("DATA", "Direct costs paid for lease acquisition", {"FY2025": -24}),
    ("DATA", "Principal paid on lease liabilities",
     {"FY2025": -1579, "FY2024": -1567, "FY2023": -1763, "FY2022": -917, "FY2021": -1974}),
    ("DATA", "Interest paid on lease liabilities", {"FY2021": -34}),
    ("TOTAL", "Net cash generated from/(used in) financing activities",
     {"FY2025": -1603, "FY2024": 33433, "FY2023": 9537, "FY2022": -384, "FY2021": 32492}),
    ("TOTAL", "Net increase in cash and cash equivalents",
     {"FY2025": 6999904, "FY2024": 4700109, "FY2023": 3130307, "FY2022": 405099, "FY2021": 1707583}),
    ("DATA", "Cash and cash equivalents at the beginning of the year",
     {"FY2025": 10961293, "FY2024": 6258123, "FY2023": 3125862, "FY2022": 2720797, "FY2021": 1013224}),
    ("DATA", "Effect of foreign exchange rate changes",
     {"FY2025": -4221, "FY2024": 3061, "FY2023": -43, "FY2022": -34, "FY2021": -10}),
    ("TOTAL", "Cash and cash equivalents at the end of the year",
     {"FY2025": 17956976, "FY2024": 10961293, "FY2023": 6256126, "FY2022": 3125862, "FY2021": 2720797}),
]

bw.add_cash_flow_sheet(
    title="ClearBank Limited — Consolidated Cash Flow Statement",
    subtitle="Group basis, £'000. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
aq_rows = [
    ("SECTION", "Loan book", {}),
    ("DATA", "Customer loans and advances", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Loss allowance on customer loans", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("SECTION", "Interbank treasury placements ('Loans and advances to banks')", {}),
    ("DATA", "Carrying amount",
     {"FY2023": 19525, "FY2022": 9156, "FY2021": 5962}),
    ("DATA", "Loss allowance recognised", {"FY2023": 0, "FY2022": 0, "FY2021": 0}),
]

bw.add_asset_quality_sheet(
    title="ClearBank — Asset Quality / Credit Risk Disclosures",
    subtitle="£'000. ClearBank does not lend to customers - see the structural finding in the source note below.",
    rows=aq_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=64,
    source_height=280,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=44, source_height=190)


CET1_CAPITAL = {"FY2025": 132, "FY2024": 141, "FY2023": 126, "FY2022": 33, "FY2021": 36.7}
CET1_RATIO = {"FY2025": "49.75%", "FY2024": "67.02%", "FY2023": "77.45%", "FY2022": "87.66%", "FY2021": "139.70%"}
RWA = {"FY2025": 266, "FY2024": 211, "FY2023": 163, "FY2022": 38, "FY2021": 26}
LEVERAGE = {"FY2025": "20.05%", "FY2024": "26.07%", "FY2023": "43.51%", "FY2022": "13.87%", "FY2021": "38.79%"}
LCR = {"FY2025": "396.85%", "FY2024": "381.88%", "FY2023": "445.36%", "FY2022": "297.05%", "FY2021": "185.94%"}
NSFR = {"FY2025": "20366.50%", "FY2024": "15959.22%", "FY2023": "10153.88%", "FY2022": "5429.15%", "FY2021": "11701.32%"}

metric("CET1 Capital", "£m", [("Common Equity Tier 1 (CET1) capital", CET1_CAPITAL)])
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 ratio", CET1_RATIO)])
metric("Tier 1 Capital", "£m (= CET1 capital; no AT1 instruments)", [("Tier 1 capital", CET1_CAPITAL)])
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", CET1_RATIO)])
metric("Total Capital", "£m (= CET1 capital; no Tier 2 instruments)", [("Total capital", CET1_CAPITAL)])
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", CET1_RATIO)])
metric("Total RWAs", "£m", [("Total risk-weighted exposure amount", RWA)])

# ---------------------------------------------------------------
# Sheet: RWA Breakdown
# ---------------------------------------------------------------
rwa_rows = [
    ("SECTION", "RWA by risk category", {}),
    ("DATA", "Credit risk (excluding CCR), standardised approach",
     {"FY2025": 45000, "FY2024": 34000, "FY2023": 36000, "FY2022": 16000, "FY2021": 17000}),
    ("DATA", "Operational risk, basic indicator approach",
     {"FY2025": 221000, "FY2024": 178000, "FY2023": 127000, "FY2022": 22000, "FY2021": 9000}),
    ("TOTAL", "Total RWAs",
     {"FY2025": 266000, "FY2024": 212000, "FY2023": 163000, "FY2022": 38000, "FY2021": 26000}),
]

bw.add_rwa_breakdown_sheet(
    title="ClearBank — RWA Breakdown",
    subtitle="£'000 (source tables are in £m; converted x1000 for unit consistency with other sheets). See source note at bottom.",
    rows=rwa_rows,
    sources_text=RWA_SOURCES,
    first_col_width=54,
    source_height=340,
)
metric("Leverage Ratio", "%",
       [("Leverage ratio excluding claims on central banks", LEVERAGE)],
       note="FY2021 figure is on the \"UK leverage ratio\" basis (39% as originally disclosed in "
            "ClearBank's own FY2021 Pillar 3 document), consistent with the \"excluding claims on "
            "central banks\" basis used FY2022 onward - see the LEVERAGE RATIO BASIS NOTE in this "
            "sheet's source citation for the very different \"CRD leverage ratio\" (1%) also "
            "disclosed for FY2021 on a different exposure-measure definition.")
metric("LCR", "%", [("Liquidity Coverage Ratio", LCR)])
metric("NSFR", "%", [("Net Stable Funding Ratio", NSFR)],
       note="Extreme values (5,000%-20,000%+) are genuine, not a transcription error - ClearBank's "
            "clearing-bank business model holds very large customer deposit balances relative to a "
            "small lending book, so required stable funding is tiny relative to available stable "
            "funding.")

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={"MREL Ratio": "Not publicly disclosed - no MREL ratio or qualitative MREL statement "
                             "found in any Pillar 3 document reviewed (FY2021-FY2025), no reason given."},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets",
         {"FY2025": 18068355, "FY2024": 11064063, "FY2023": 6366850, "FY2022": 3204409, "FY2021": 2772608}),
        ("Customer deposits",
         {"FY2025": 17826803, "FY2024": 10818568, "FY2023": 6147363, "FY2022": 2982259, "FY2021": 2644756}),
        ("Total equity",
         {"FY2025": 212839, "FY2024": 222291, "FY2023": 129526, "FY2022": 87312, "FY2021": 72217}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total income",
         {"FY2025": 132684, "FY2024": 112086, "FY2023": 111347, "FY2022": 58284, "FY2021": 21394}),
        ("Operating expenses",
         {"FY2025": -148934, "FY2024": -122035, "FY2023": -105783, "FY2022": -77638, "FY2021": -52439}),
        ("Profit/(loss) for the year after taxation",
         {"FY2025": -15765, "FY2024": -10318, "FY2023": 22396, "FY2022": 6818, "FY2021": -28200}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 222291, "FY2024": 196497, "FY2023": 87312, "FY2022": 72217, "FY2021": 58247}),
        ("Total comprehensive income/(loss) for the year",
         {"FY2025": -13977, "FY2024": -11085, "FY2023": 22396, "FY2022": 6819, "FY2021": -28201}),
        ("Other equity movements, net",
         {"FY2025": 4525, "FY2024": 36879, "FY2023": 19818, "FY2022": 8276, "FY2021": 42171}),
        ("Closing equity", {"FY2025": 212839, "FY2024": 222291, "FY2023": 129526, "FY2022": 87312, "FY2021": 72217}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from operating activities",
         {"FY2025": 7017191, "FY2024": 4690772, "FY2023": 3142548, "FY2022": 413627, "FY2021": 1683715}),
        ("Net cash used in investing activities",
         {"FY2025": -15684, "FY2024": -24096, "FY2023": -21778, "FY2022": -8144, "FY2021": -8624}),
        ("Net cash from/(used in) financing activities",
         {"FY2025": -1603, "FY2024": 33433, "FY2023": 9537, "FY2022": -384, "FY2021": 32492}),
        ("Cash and cash equivalents at end of year",
         {"FY2025": 17956976, "FY2024": 10961293, "FY2023": 6256126, "FY2022": 3125862, "FY2021": 2720797}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Leverage Ratio", LEVERAGE),
        ("LCR", LCR),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. Statement of Changes in Equity Summary: FY2024's "
         "Opening equity is a new ultimate parent entity's own balance (ClearBank Group Holdings Limited, "
         "inserted above ClearBank Limited during FY2024), not a continuation of FY2023's Closing equity - "
         "see the Statement of Changes in Equity sheet for the full entity-change note. NSFR omitted from this chart (values in the "
         "thousands of percent would flatten every other series) - see the NSFR sheet directly.",
)

bw.save("/Users/armaan/code/katalysis/banks/CLEARBANK FINANCIALS.xlsx")
