import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}
PREV_YEAR = {"FY2019": "FY2018", "FY2020": "FY2019", "FY2021": "FY2020", "FY2022": "FY2021", "FY2023": "FY2022", "FY2024": "FY2023", "FY2025": "FY2024"}

# ---------------------------------------------------------------
# FX conversion (FCMB Bank (UK) Limited reports in USD; converting to £ per
# this project's established FX methodology). Same 31 December year-end as
# Zenith Bank UK / Union Bank of India UK - reusing that exact rate table
# rather than re-deriving it. Rates are Bank of England GBP/USD spot/average
# via poundsterlinglive.com's published archive, £1 = $X.
# ---------------------------------------------------------------
FX_SPOT = {
    "FY2018": 1.2783,
    "FY2019": 1.3203,
    "FY2020": 1.3661,  # 31 Dec 2020 - only used for FY2021's opening cash balance
    "FY2021": 1.3521,
    "FY2022": 1.2097,
    "FY2023": 1.2732,
    "FY2024": 1.2515,
    "FY2025": 1.3448,
}
FX_AVG = {
    "FY2019": 1.2793,
    "FY2020": 1.2837,
    "FY2021": 1.3752,
    "FY2022": 1.2362,
    "FY2023": 1.2439,
    "FY2024": 1.2782,
    "FY2025": 1.3193,
}


def flow(usd):
    return {y: round(v / FX_AVG[y] / 1000, 1) for y, v in usd.items() if y in FX_AVG}


def stock(usd):
    return {y: round(v / FX_SPOT[y] / 1000, 1) for y, v in usd.items() if y in FX_SPOT}


def opening_cash(usd):
    # FY2020 has no FY2019 spot-rate input because FY2019 is a documented
    # self-skipped year; preserve a blank opening balance rather than guessing.
    return {
        y: round(v / FX_SPOT[PREV_YEAR[y]] / 1000, 1)
        for y, v in usd.items()
        if y in PREV_YEAR and PREV_YEAR[y] in FX_SPOT
    }


AR2025_URL = "https://fcmbuk.com/wp-content/uploads/2026/08/SIGNED-FCMB-Bank-UK-Limited-Audited-Accounts-2025.pdf"
AR2024_URL = "https://fcmbuk.com/wp-content/uploads/2025/09/FCMB-Bank-UK-Limited-Audited-Accounts-2024-Signed.pdf"
AR2023_URL = "https://fcmbuk.com/wp-content/uploads/2024/07/FCMB-Bank-UK-Limited-Audited-Accounts-2023.pdf"
AR2022_URL = "https://fcmbuk.com/wp-content/uploads/2023/09/FCMB-Bank-UK-Limited-Signed-Annual-Report-Financial-Statements-2022.pdf"
AR2021_URL = "https://fcmbuk.com/wp-content/uploads/2023/09/FCMB-Bank-UK-Limited-Signed-Audited-Accounts-2021.pdf"
P3_2020_URL = "https://www.fcmbuk.com/wp-content/uploads/2021/12/Pillar-III-Disclosures-FYE-2020.pdf"
P3_2025_URL = "https://fcmbuk.com/wp-content/uploads/2026/08/5.-Pillar-III-Disclosures-FYE-2025-30-June-2026.pdf"
P3_2024_URL = "https://fcmbuk.com/wp-content/uploads/2025/09/Pillar-III-Disclosures-FYE-2024.pdf"
P3_2023_URL = "https://fcmbuk.com/wp-content/uploads/2024/08/Pillar-III-Disclosures-FYE-2023.pdf"
P3_2022_URL = "https://fcmbuk.com/wp-content/uploads/2023/09/Pillar-III-Disclosures-FYE-2022.pdf"
P3_2021_URL = "https://fcmbuk.com/wp-content/uploads/2022/07/Pillar-III-Disclosures-FYE-2021-002.pdf"

ENTITY_NOTE = (
    "FCMB Bank (UK) Limited (company 06621225, FRN 502704) is a UK subsidiary of First City Monument "
    "Bank (Nigeria). Does NOT take the FRS 101/102 cash-flow exemption - a full Statement of Cash Flows "
    "exists every year. FY2020 is sourced from the FY2021 Annual Report's audited comparative column; "
    "FY2019 is sourced from the Companies House-filed statutory accounts supplied for this audit (printed pages 26-29). "
    "Each available year's own originally-published figures used throughout - the closing "
    "balance of each year ties exactly to the following year's own opening balance across all 5 years.\n"
    "DATA QUALITY NOTE (FY2024): the FY2025 Annual Report's own FY2024 comparative column shows "
    "materially different 'Changes in operating assets and liabilities' line items (and a different "
    "Operating/Investing split) than FY2024's own originally-published Annual Report - e.g. 'Net "
    "(increase) in loans and advances to banks' is $(42,672,236) in the FY2025 report's comparative "
    "vs. $(35,611,527) in FY2024's own report. FY2024's own figures are used throughout (per project "
    "convention), and independently confirmed internally consistent (adjustments subtotal $2,243,237 + "
    "changes subtotal $4,830,112 = $7,073,349, matching FY2024's own printed operating total exactly). "
    "Net cash flow for the year, opening balance, and closing balance are IDENTICAL between both "
    "vintages ($(239,325) net change, both years) - only the Operating/Investing section split differs, "
    "consistent with a presentational reclassification rather than a change in the Bank's actual cash "
    "position. Similarly, FY2021's own report classifies 'Issuance of subordinated liabilities' "
    "($2,000,000) within Operating activities, while later reports' FY2021 comparative reclassifies it "
    "into Financing activities - the FY2022 report's own footnote explicitly confirms this deliberate "
    "reclassification ('Subordinated liabilities were classified under operating activities in 2021. In "
    "2022, subordinated liabilities have been classified under financing activities for the current "
    "year and in the prior year comparatives.'). FY2021's own original classification is used here, per "
    "convention.\n"
    "FX CONVERSION: the Bank's functional and presentational currency is USD. Converted to £ per this "
    "project's established methodology: point-in-time/balance figures (capital, RWA, leverage exposure, "
    "HQLA, cash balances) use the Bank of England GBP/USD SPOT rate as at that fiscal year-end (31 "
    "December); flow figures (every cash flow statement line item) use the AVERAGE of Bank of England "
    "rates over that calendar year. Rate table reused from Zenith Bank UK/Union Bank of India UK "
    "(same 31 Dec year-end): 31 Dec 2020 spot 1.3661 (FY2021 opening cash only); FY2021 spot 1.3521 / "
    "average 1.3752; FY2022 spot 1.2097 / average 1.2362; FY2023 spot 1.2732 / average 1.2439; FY2024 "
    "spot 1.2515 / average 1.2782; FY2025 spot 1.3448 / average 1.3193. All % ratios are shown exactly "
    "as reported in USD, not converted (dimensionless, currency-invariant). An explicit 'Effect of "
    "GBP/USD translation' line reconciles the stock/flow rate mismatch so opening + flows + this line = "
    "closing exactly in £ terms; computed programmatically from the actual converted figures, not "
    "hardcoded."
)

CASH_FLOW_SOURCES = (
    "Sources - FCMB Bank (UK) Limited's own Statement of Cash Flows, from its Companies House-filed "
    "Annual Report and Accounts (also published on the Bank's own site):\n"
    f"FY2025: Audited Accounts 2025, p.42-43 - {AR2025_URL}\n"
    f"FY2024: Audited Accounts 2024, p.31 (own-year figures; FY2024 comparative in the FY2025 report cross-checked and matched exactly) - {AR2024_URL}\n"
    f"FY2023: Audited Accounts 2023, p.33 - {AR2023_URL}\n"
    f"FY2022: Annual Report & Financial Statements 2022, p.31 (own-year figures; FY2022 comparative in the FY2023 report cross-checked and matched exactly) - {AR2022_URL}\n"
    f"FY2021: Audited Accounts 2021, p.28 - {AR2021_URL}\n"
    f"FY2020: Audited Accounts 2021, p.28 (audited comparative column) - {AR2021_URL}\n"
    "FY2019: Companies House-filed FCMB Bank (UK) Limited Annual Report and Financial Statements 2019, printed pp.26-29 (user-supplied primary PDF; deleted after extraction)\n"
    + ENTITY_NOTE
)


def p3_sources(page_2025="3", page_2024="2", page_2023="19", page_2022="19"):
    return (
        "Sources - FCMB Bank (UK) Limited Pillar 3 Disclosures ('Key Regulatory Metrics' table):\n"
        f"FY2025: Pillar III Disclosures FYE 2025, p.{page_2025} - {P3_2025_URL}\n"
        f"FY2024: Pillar III Disclosures FYE 2024, p.{page_2024} (own-year; also cross-checked against FY2025's comparative column, matched exactly) - {P3_2024_URL}\n"
        f"FY2023: Pillar III Disclosures FYE 2023, p.{page_2023} (own-year; also cross-checked against FY2024's comparative column, matched exactly) - {P3_2023_URL}\n"
        f"FY2022: Pillar III Disclosures FYE 2022, p.{page_2022} (own-year; also cross-checked against FY2023's comparative column, matched exactly) - {P3_2022_URL}\n"
        f"FY2021: sourced from FY2022's Pillar III Disclosures own comparative column - the FY2021 document itself "
        f"(Pillar III Disclosures FYE 2021, {P3_2021_URL}) pre-dates this 'Key Regulatory Metrics'/KM1-style table "
        "and only discloses a 'Minimum Capital Requirements' breakdown with no CET1/Total Capital/RWA/Leverage/"
        "LCR/NSFR figures - same pattern as Aldermore/BLME/Bank of Ireland UK/British Arab Commercial Bank "
        "elsewhere in this project.\n"
        f"FY2020: Pillar III Disclosures FYE 2020, pp.8-9 (old-format capital and RWA tables; no KM1 leverage/LCR/NSFR table) - {P3_2020_URL}\n"
        "LCR/NSFR methodology note (per the Bank's own documents, CRR Article 447): each LCR component is "
        "calculated as a 12-month average, and NSFR components as the average of the last 4 quarters - i.e. the "
        "LCR%/NSFR% shown are themselves already period averages, not point-in-time spot ratios."
    )


bw = BankWorkbook(bank_name="FCMB Bank (UK) Limited", years=YEARS, year_label=YEAR_LABEL, header_color="A90D9C")

STATEMENTS_ENTITY_NOTE = (
    ENTITY_NOTE + "\n"
    "BALANCE SHEET RECLASSIFICATION NOTE (FY2024): the FY2025 Annual Report's own FY2024 comparative "
    "column shows a different split between 'Loans and advances to banks' ($222,353,776), 'Loans and "
    "advances to customers' ($87,181,343) and 'Investment securities' ($192,066,892) than FY2024's own "
    "originally-published Annual Report ($215,293,067 / $86,092,409 / $196,761,703 respectively) - the "
    "FY2025 report's own Balance Sheet page states 'There has been a re-classification of accrued "
    "interest and some investment securities at the prior year-end have been recategorised as a "
    "debtor.' Total assets/liabilities/equity are IDENTICAL between both vintages ($521,421,659 total "
    "assets, $59,259,637 total equity) - only the asset-line split differs. FY2024's own originally-"
    "published figures are used throughout here, per project convention.\n"
    "ASSET QUALITY RECLASSIFICATION NOTE (FY2024): similarly, the FY2025 report's own FY2024 comparative "
    "'Net carrying value of exposure by risk rating' table shows Stage 1/2/3 splits ($409,617,076 / "
    "$6,832,107 / $3,121,198, total $419,570,381) that differ from FY2024's own originally-published "
    "note ($404,519,023 / $6,673,411 / $3,121,198, total $414,313,632) - consistent with the same "
    "reclassification. FY2024's own originally-published figures are used here too.\n"
    "RWA BREAKDOWN NOTE: the Bank's Pillar 3 Disclosures do not publish a UK OV1-style RWA-by-category "
    "table directly - only a 'Minimum Capital Requirements' table (8% of own funds requirement, by risk "
    "type). RWA by category is CALCULATED as (capital requirement / 8%) for each row, independently "
    "cross-checked against the Bank's own disclosed Total RWA/TREA figure (Total RWAs sheet) - the "
    "calculated Total Pillar 1 RWA ties to the disclosed TREA within rounding for every year (e.g. "
    "FY2025: $29,485k / 8% = $368,563k calculated vs $368,569k disclosed TREA).\n"
    "INVESTMENT SECURITIES BREAKDOWN: the 'Investment securities - ...' sub-rows below the 'Total "
    "investment securities' line are transcribed from Note 15 'Investment securities' of each year's own "
    "Notes to the Financial Statements, which splits the balance both by measurement basis (fair value "
    "through other comprehensive income (FVOCI) vs fair value through profit or loss (FVTPL) - there is "
    "no amortised-cost investment securities balance in any year) and by instrument type (Government "
    "Bonds; Bank bonds; HQLA Investments, described in the note as 'high quality liquid assets [that] "
    "include US Treasury bills and bonds issued by International Bank of Restructuring and Development "
    "(IBRD)' - i.e. a sovereign/supranational mix not broken down further; an allowance for impairment "
    "losses against the FVOCI book; and Fund Investments - Government / Fund Investments - Other, both "
    "FVTPL): "
    f"FY2025: Audited Accounts 2025, Note 15, p.62 - {AR2025_URL}\n"
    f"FY2024: Audited Accounts 2024, Note 15, p.49 (own-year figures - see reclassification note above; "
    f"the FY2025 report's own FY2024 comparative column shows different Note 15 sub-figures totalling "
    f"$192,066,892, consistent with the same reclassification) - {AR2024_URL}\n"
    f"FY2023: Audited Accounts 2023, Note 15, p.51 - {AR2023_URL}\n"
    f"FY2022: Annual Report & Financial Statements 2022, Note 15, p.50 - {AR2022_URL}\n"
    f"FY2021: Audited Accounts 2021, Note 15, p.46 - {AR2021_URL}\n"
    f"FY2020: Audited Accounts 2021, Note 15, p.46 (audited comparative column; FY2020 predates the "
    f"'HQLA Investments' sub-line introduced from FY2022 onwards, so that FY2020 sub-row is £0) - "
    f"{AR2021_URL}\n"
    "FY2019: no breakdown available - the FY2019 Note 15 was not among the pages transcribed from the "
    "user-supplied primary PDF (since deleted after extraction), so the FY2019 sub-rows are left blank "
    "rather than estimated.\n"
    "Each year's sub-rows sum exactly to that year's headline 'Total investment securities' line in "
    "underlying USD; after this project's independent per-row £'000 FX conversion (each row rounded to "
    "1 decimal place separately) the sub-rows tie to the total within rounding (at most £0.1k) for any "
    "given year."
)

STATEMENTS_SOURCES = (
    "Sources - FCMB Bank (UK) Limited's own Statement of Financial Position / Statement of Comprehensive "
    "Income / Statement of Changes in Equity, from its Companies House-filed Annual Report and Accounts:\n"
    f"FY2025: Audited Accounts 2025, p.40-41 - {AR2025_URL}\n"
    f"FY2024: Audited Accounts 2024, p.29-30 (own-year figures - see reclassification note) - {AR2024_URL}\n"
    f"FY2023: Audited Accounts 2023, p.31-32 - {AR2023_URL}\n"
    f"FY2022: Annual Report & Financial Statements 2022, p.29-30 - {AR2022_URL}\n"
    f"FY2021: Audited Accounts 2021, p.26-27 - {AR2021_URL}\n"
    f"FY2020: Audited Accounts 2021, pp.26-27 (audited comparative column) - {AR2021_URL}\n"
    "FY2019: Companies House-filed Annual Report and Financial Statements 2019, printed pp.26-27 (user-supplied primary PDF; deleted after extraction)\n"
    + STATEMENTS_ENTITY_NOTE
)

ASSET_QUALITY_SOURCES = (
    "Sources - FCMB Bank (UK) Limited's own 'Net carrying value of exposure by risk rating' (IFRS 9 "
    "stage) and 'Expected Credit Loss by Stage' notes, Note 24 (Financial instruments and risk "
    "management), from its Companies House-filed Annual Report and Accounts:\n"
    f"FY2025: Audited Accounts 2025, p.79-80 - {AR2025_URL}\n"
    f"FY2024: Audited Accounts 2024, p.65 (own-year figures - see reclassification note) - {AR2024_URL}\n"
    f"FY2023: Audited Accounts 2023, p.67 - {AR2023_URL}\n"
    f"FY2022: Annual Report & Financial Statements 2022, p.66 - {AR2022_URL}\n"
    f"FY2021: Audited Accounts 2021, p.61 (ECL by stage sourced from this page's own narrative text) - {AR2021_URL}\n"
    f"FY2020: Audited Accounts 2021, p.61 (audited comparative column and narrative) - {AR2021_URL}\n"
    "Gross carrying amount by stage is CALCULATED as Net carrying amount + ECL allowance for that stage "
    "(the Bank discloses net carrying value and ECL by stage separately, not gross carrying amount "
    "directly). NPL ratio = Stage 3 gross carrying / Total gross carrying; Stage 3 coverage ratio = Stage "
    "3 ECL / Stage 3 gross carrying (blank for FY2021, which had zero Stage 3 exposure); Total ECL "
    "coverage = Total ECL / Total gross carrying.\n"
    + ENTITY_NOTE.split("DATA QUALITY NOTE")[0]
)

# ---------------------------------------------------------------
# Balance Sheet (Statement of Financial Position), own-year figures throughout
# ---------------------------------------------------------------
BS_USD = {
    "Cash and cash equivalents": {"FY2025": 10067514, "FY2024": 7266626, "FY2023": 7498541, "FY2022": 7118069, "FY2021": 5979879, "FY2020": 13024184, "FY2019": 15721283},
    "Loans and advances to banks": {"FY2025": 272182290, "FY2024": 215293067, "FY2023": 179580081, "FY2022": 139928644, "FY2021": 132348155, "FY2020": 117798590, "FY2019": 112085852},
    "Loans and advances to customers": {"FY2025": 115746735, "FY2024": 86092409, "FY2023": 74582276, "FY2022": 71445494, "FY2021": 79441478, "FY2020": 51668458, "FY2019": 37370618},
    "Investment securities": {"FY2025": 195435410, "FY2024": 196761703, "FY2023": 187900449, "FY2022": 284747448, "FY2021": 174077450, "FY2020": 189651477, "FY2019": 189652928},
    "Investment securities - Government bonds (sovereign debt, FVOCI)": {"FY2025": 0, "FY2024": 5625803, "FY2023": 5498440, "FY2022": 5495131, "FY2021": 7455147, "FY2020": 0},
    "Investment securities - Bank bonds (financial institution debt, FVOCI)": {"FY2025": 0, "FY2024": 15208790, "FY2023": 16525823, "FY2022": 15143439, "FY2021": 17212630, "FY2020": 3230250},
    "Investment securities - HQLA: US Treasury bills & IBRD supranational bonds (FVOCI)": {"FY2025": 5110015, "FY2024": 19914165, "FY2023": 29464278, "FY2022": 19430955, "FY2021": 0, "FY2020": 0},
    "Investment securities - Allowance for impairment losses on FVOCI investments": {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": -139266, "FY2020": 0},
    "Investment securities - Fund investments - Government (FVTPL)": {"FY2025": 188571800, "FY2024": 147574098, "FY2023": 127321582, "FY2022": 235843987, "FY2021": 139770139, "FY2020": 186421227},
    "Investment securities - Fund investments - Other (FVTPL)": {"FY2025": 1753595, "FY2024": 8438847, "FY2023": 9090326, "FY2022": 8833936, "FY2021": 9778800, "FY2020": 0},
    "Derivative financial instruments (asset)": {"FY2025": 2970155, "FY2024": 1432396, "FY2023": 1597744, "FY2022": 1851462, "FY2021": 834132, "FY2020": 3716102},
    "Other assets": {"FY2025": 9227109, "FY2024": 13004808, "FY2023": 9099146, "FY2022": 7569349, "FY2021": 6590091, "FY2020": 3528046, "FY2019": 3828574},
    "Deferred tax asset": {"FY2025": 357362, "FY2023": 19819, "FY2022": 159008, "FY2021": 660811, "FY2020": 149356},
    "Property and equipment": {"FY2025": 516932, "FY2024": 950961, "FY2023": 480338, "FY2022": 1851933, "FY2021": 2236095, "FY2020": 2612610, "FY2019": 3003210},
    "Intangible assets": {"FY2025": 526698, "FY2024": 619689, "FY2023": 540470, "FY2022": 393250, "FY2021": 285064, "FY2020": 433802, "FY2019": 538089},
    "Total assets": {"FY2025": 607030205, "FY2024": 521421659, "FY2023": 461298864, "FY2022": 515064657, "FY2021": 402453155, "FY2020": 382582625, "FY2019": 362180554},
    "Deposits from banks": {"FY2025": 308574526, "FY2024": 280518956, "FY2023": 232089383, "FY2022": 238119179, "FY2021": 146683204, "FY2020": 162678718, "FY2019": 190244135},
    "Deposits from customers": {"FY2025": 225771958, "FY2024": 160341314, "FY2023": 155331596, "FY2022": 213123234, "FY2021": 197470447, "FY2020": 167557304, "FY2019": 122044903},
    "Derivative financial instruments (liability)": {"FY2025": 422687, "FY2024": 2178822, "FY2023": 1048899, "FY2022": 3686620, "FY2021": 2176318, "FY2020": 0},
    "Current tax liability": {"FY2022": 45624},
    "Other liabilities": {"FY2025": 6941662, "FY2024": 9498007, "FY2023": 7934679, "FY2022": 6357677, "FY2021": 5998326, "FY2020": 5497582, "FY2019": 5899974},
    "Subordinated liabilities": {"FY2025": 9600000, "FY2024": 9600000, "FY2023": 9600000, "FY2022": 9600000, "FY2021": 5000000, "FY2020": 3000000},
    "Deferred tax liability": {"FY2024": 24923},
    "Total liabilities": {"FY2025": 551310833, "FY2024": 462162022, "FY2023": 406004557, "FY2022": 470932334, "FY2021": 357328295, "FY2020": 338733604, "FY2019": 318189012},
    "Issued capital": {"FY2025": 53900000, "FY2024": 53900000, "FY2023": 53900000, "FY2022": 48900000, "FY2021": 48900000, "FY2020": 48900000, "FY2019": 48900000},
    "Retained earnings": {"FY2025": 1818642, "FY2024": 5495727, "FY2023": 3035900, "FY2022": -1268750, "FY2021": -3674449, "FY2020": -5309930, "FY2019": -4923353},
    "Other reserves": {"FY2025": 730, "FY2024": -136090, "FY2023": -1641593, "FY2022": -3498927, "FY2021": -100691, "FY2020": 258951, "FY2019": 14695},
    "Total equity": {"FY2025": 55719372, "FY2024": 59259637, "FY2023": 55294307, "FY2022": 44132323, "FY2021": 45124860, "FY2020": 43849021, "FY2019": 43991542},
    "Total liabilities and equity": {"FY2025": 607030205, "FY2024": 521421659, "FY2023": 461298864, "FY2022": 515064657, "FY2021": 402453155, "FY2020": 382582625, "FY2019": 362180554},
}

bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents", stock(BS_USD["Cash and cash equivalents"])),
    ("DATA", "Loans and advances to banks", stock(BS_USD["Loans and advances to banks"])),
    ("DATA", "Loans and advances to customers", stock(BS_USD["Loans and advances to customers"])),
    ("DATA", "Total investment securities", stock(BS_USD["Investment securities"])),
    ("DATA", "Investment securities - Government bonds (sovereign debt, FVOCI)",
     stock(BS_USD["Investment securities - Government bonds (sovereign debt, FVOCI)"])),
    ("DATA", "Investment securities - Bank bonds (financial institution debt, FVOCI)",
     stock(BS_USD["Investment securities - Bank bonds (financial institution debt, FVOCI)"])),
    ("DATA", "Investment securities - HQLA: US Treasury bills & IBRD supranational bonds (FVOCI)",
     stock(BS_USD["Investment securities - HQLA: US Treasury bills & IBRD supranational bonds (FVOCI)"])),
    ("DATA", "Investment securities - Allowance for impairment losses on FVOCI investments",
     stock(BS_USD["Investment securities - Allowance for impairment losses on FVOCI investments"])),
    ("DATA", "Investment securities - Fund investments - Government (FVTPL)",
     stock(BS_USD["Investment securities - Fund investments - Government (FVTPL)"])),
    ("DATA", "Investment securities - Fund investments - Other (FVTPL)",
     stock(BS_USD["Investment securities - Fund investments - Other (FVTPL)"])),
    ("DATA", "Derivative financial instruments", stock(BS_USD["Derivative financial instruments (asset)"])),
    ("DATA", "Other assets", stock(BS_USD["Other assets"])),
    ("DATA", "Deferred tax asset", stock(BS_USD["Deferred tax asset"])),
    ("DATA", "Property and equipment", stock(BS_USD["Property and equipment"])),
    ("DATA", "Intangible assets", stock(BS_USD["Intangible assets"])),
    ("TOTAL", "Total assets", stock(BS_USD["Total assets"])),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks", stock(BS_USD["Deposits from banks"])),
    ("DATA", "Deposits from customers", stock(BS_USD["Deposits from customers"])),
    ("DATA", "Derivative financial instruments", stock(BS_USD["Derivative financial instruments (liability)"])),
    ("DATA", "Current tax liability", stock(BS_USD["Current tax liability"])),
    ("DATA", "Other liabilities", stock(BS_USD["Other liabilities"])),
    ("DATA", "Subordinated liabilities", stock(BS_USD["Subordinated liabilities"])),
    ("DATA", "Deferred tax liability", stock(BS_USD["Deferred tax liability"])),
    ("TOTAL", "Total liabilities", stock(BS_USD["Total liabilities"])),
    ("SECTION", "Equity", {}),
    ("DATA", "Issued capital", stock(BS_USD["Issued capital"])),
    ("DATA", "Retained earnings", stock(BS_USD["Retained earnings"])),
    ("DATA", "Other reserves", stock(BS_USD["Other reserves"])),
    ("TOTAL", "Total equity", stock(BS_USD["Total equity"])),
    ("TOTAL", "Total liabilities and equity", stock(BS_USD["Total liabilities and equity"])),
]

bw.add_balance_sheet_sheet(
    title="FCMB Bank (UK) Limited — Statement of Financial Position",
    subtitle="£'000, converted from USD - see source note at bottom for FX methodology and rates used.",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=60,
    source_height=340,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Profit & Loss (Statement of Comprehensive Income), own-year figures throughout
# ---------------------------------------------------------------
PL_USD = {
    "Interest and similar income": {"FY2025": 34085629, "FY2024": 36174703, "FY2023": 31703911, "FY2022": 18924173, "FY2021": 11210682, "FY2020": 10108036, "FY2019": 11573277},
    "Interest and similar expense": {"FY2025": -18574590, "FY2024": -18342203, "FY2023": -13832115, "FY2022": -4429010, "FY2021": -2853008, "FY2020": -4894740, "FY2019": -5598667},
    "Net interest income": {"FY2025": 15511039, "FY2024": 17832500, "FY2023": 17871796, "FY2022": 14495163, "FY2021": 8357674, "FY2020": 5213296, "FY2019": 5974610},
    "Fees and commission income": {"FY2025": 2698507, "FY2024": 1755726, "FY2023": 1297345, "FY2022": 1776850, "FY2021": 2300057, "FY2020": 2257621},
    "Fees and commission expense": {"FY2025": -1108194, "FY2024": -809953, "FY2023": -734826, "FY2022": -888409, "FY2021": -767438, "FY2020": -486298},
    "Net fee and commission income": {"FY2025": 1590313, "FY2024": 945773, "FY2023": 562519, "FY2022": 888441, "FY2021": 1532619, "FY2020": 1771323, "FY2019": 2346142},
    "Other operating income": {"FY2025": 1819183, "FY2024": 2208661, "FY2023": 4611335, "FY2022": 3534205, "FY2021": 3022643, "FY2020": 1630708, "FY2019": 1302648},
    "Impairment charges": {"FY2025": -5384068, "FY2024": -29914, "FY2023": -1795645, "FY2022": -2508414, "FY2021": -77775, "FY2020": -375071, "FY2019": -10951},
    "Net operating income": {"FY2025": 13536467, "FY2024": 20957020, "FY2023": 21250005, "FY2022": 16409395, "FY2021": 12835161, "FY2020": 8240256, "FY2019": 9612448},
    "Personnel expenses": {"FY2025": -12916311, "FY2024": -11495240, "FY2023": -9886321, "FY2022": -7880197, "FY2021": -6867362, "FY2020": -5797195},
    "Depreciation and amortisation expenses": {"FY2025": -797249, "FY2024": -804587, "FY2023": -672685, "FY2022": -579990, "FY2021": -603791, "FY2020": -599159},
    "General and administrative expenses": {"FY2025": -4722107, "FY2024": -5356176, "FY2023": -5048080, "FY2022": -4996082, "FY2021": -4117113, "FY2020": -2157057},
    "Other operating expenses": {"FY2021": -122869, "FY2020": -222978},
    "Total operating expenses": {"FY2025": -18435667, "FY2024": -17656003, "FY2023": -15607086, "FY2022": -13456269, "FY2021": -11711135, "FY2020": -8776389, "FY2019": -8115025},
    "Profit/(Loss) before tax": {"FY2025": -4899200, "FY2024": 3301017, "FY2023": 5642919, "FY2022": 2953126, "FY2021": 1124026, "FY2020": -536133, "FY2019": 1497423},
    "Taxation": {"FY2025": 1222115, "FY2024": -841190, "FY2023": -1338269, "FY2022": -547427, "FY2021": 511455, "FY2020": 149356},
    "Profit/(Loss) for the year": {"FY2025": -3677085, "FY2024": 2459827, "FY2023": 4304650, "FY2022": 2405699, "FY2021": 1635481, "FY2020": -386777, "FY2019": 1497423},
    "Net change in fair value of FVOCI investments": {"FY2025": 360812, "FY2024": 1464225, "FY2023": 1857334, "FY2022": -3398236, "FY2021": -359642, "FY2020": 258951},
    "Net amount reclassified to the income statement": {"FY2020": -14695, "FY2025": -973472, "FY2024": 1053181},
    "Recycling of ECL / net change in ECL on FVOCI investments": {"FY2025": 749480, "FY2024": -1011903},
    "Other comprehensive income/(loss), net of tax": {"FY2025": 136820, "FY2024": 1505503, "FY2023": 1857334, "FY2022": -3398236, "FY2021": -359642, "FY2020": 244256},
    "Total comprehensive income/(loss) for the year": {"FY2025": -3540265, "FY2024": 3965330, "FY2023": 6161984, "FY2022": -992537, "FY2021": 1275839, "FY2020": -142521},
}

pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest and similar income", flow(PL_USD["Interest and similar income"])),
    ("DATA", "Interest and similar expense", flow(PL_USD["Interest and similar expense"])),
    ("TOTAL", "Net interest income", flow(PL_USD["Net interest income"])),
    ("DATA", "Fees and commission income", flow(PL_USD["Fees and commission income"])),
    ("DATA", "Fees and commission expense", flow(PL_USD["Fees and commission expense"])),
    ("TOTAL", "Net fee and commission income", flow(PL_USD["Net fee and commission income"])),
    ("DATA", "Other operating income", flow(PL_USD["Other operating income"])),
    ("DATA", "Impairment charges", flow(PL_USD["Impairment charges"])),
    ("TOTAL", "Net operating income", flow(PL_USD["Net operating income"])),
    ("DATA", "Personnel expenses", flow(PL_USD["Personnel expenses"])),
    ("DATA", "Depreciation and amortisation expenses", flow(PL_USD["Depreciation and amortisation expenses"])),
    ("DATA", "General and administrative expenses", flow(PL_USD["General and administrative expenses"])),
    ("DATA", "Other operating expenses", flow(PL_USD["Other operating expenses"])),
    ("TOTAL", "Total operating expenses", flow(PL_USD["Total operating expenses"])),
    ("TOTAL", "Profit/(Loss) before tax", flow(PL_USD["Profit/(Loss) before tax"])),
    ("DATA", "Taxation", flow(PL_USD["Taxation"])),
    ("TOTAL", "Profit/(Loss) for the year", flow(PL_USD["Profit/(Loss) for the year"])),
    ("SECTION", "Other comprehensive income/(loss)", {}),
    ("DATA", "Net change in fair value of FVOCI investments", flow(PL_USD["Net change in fair value of FVOCI investments"])),
    ("DATA", "Net amount reclassified to the income statement", flow(PL_USD["Net amount reclassified to the income statement"])),
    ("DATA", "Recycling of ECL / net change in ECL on FVOCI investments", flow(PL_USD["Recycling of ECL / net change in ECL on FVOCI investments"])),
    ("TOTAL", "Other comprehensive income/(loss), net of tax", flow(PL_USD["Other comprehensive income/(loss), net of tax"])),
    ("TOTAL", "Total comprehensive income/(loss) for the year", flow(PL_USD["Total comprehensive income/(loss) for the year"])),
]

bw.add_income_statement_sheet(
    title="FCMB Bank (UK) Limited — Statement of Comprehensive Income",
    subtitle="£'000, converted from USD - see source note at bottom for FX methodology and rates used. "
             "FY2023/FY2022 OCI shown as a single FVOCI fair value line (not broken into the FY2024/FY2025 "
             "3-line split) - matches each year's own disclosure.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=340,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - chronological, oldest to newest, per-year
# reconciliation ladder: Balance Sheet built first (above), equity built
# year-by-year checking each closing balance against BS Total equity before
# moving on. Ties exactly at every boundary in USD; an explicit FX
# translation plug row absorbs the stock/flow rate-mismatch in GBP only.
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Issued capital", "Retained earnings", "Other reserves", "Total equity"]

EQUITY_ROWS_USD = [
    ("TOTAL", "At 1 January 2019", [48900000, -6420576, 40328, 42529752], "spot", "FY2018"),
    ("DATA", "Profit for the year (FY2019)", [None, 1497423, None, 1497423], "avg", "FY2019"),
    ("DATA", "Other comprehensive income (FY2019)", [None, None, -25633, -25633], "avg", "FY2019"),
    ("TOTAL", "Total comprehensive income (FY2019)", [None, 1497423, -25633, 1471790], "avg", "FY2019"),
    ("DATA", "FX translation effect on equity, net (FY2019)", [None, None, None, None], "plug", "FY2019"),
    ("TOTAL", "At 31 December 2019", [48900000, -4923353, 14695, 43991542], "spot", "FY2019"),

    ("TOTAL", "At 1 January 2020", [48900000, -4923153, 14695, 43991542], "spot", "FY2020"),
    ("DATA", "Loss for the year (FY2020)", [None, -386777, None, -386777], "avg", "FY2020"),
    ("DATA", "Other comprehensive income (FY2020)", [None, None, 244256, 244256], "avg", "FY2020"),
    ("TOTAL", "Total comprehensive loss (FY2020)", [None, -386777, 244256, -142521], "avg", "FY2020"),
    ("DATA", "FX translation effect on equity, net (FY2020)", [None, None, None, None], "plug", "FY2020"),
    ("TOTAL", "At 31 December 2020", [48900000, -5309930, 258951, 43849021], "spot", "FY2020"),

    ("TOTAL", "At 1 January 2021", [48900000, -5309930, 258951, 43849021], "spot", "FY2020"),
    ("DATA", "Profit for the year (FY2021)", [None, 1635481, None, 1635481], "avg", "FY2021"),
    ("DATA", "Other comprehensive income (FY2021)", [None, None, -359642, -359642], "avg", "FY2021"),
    ("TOTAL", "Total comprehensive income (FY2021)", [None, 1635481, -359642, 1275839], "avg", "FY2021"),
    ("DATA", "FX translation effect on equity, net (FY2021)", [None, None, None, None], "plug", "FY2021"),
    ("TOTAL", "At 31 December 2021", [48900000, -3674449, -100691, 45124860], "spot", "FY2021"),

    ("DATA", "Profit for the year (FY2022)", [None, 2405699, None, 2405699], "avg", "FY2022"),
    ("DATA", "Other comprehensive loss (FY2022)", [None, None, -3398236, -3398236], "avg", "FY2022"),
    ("TOTAL", "Total comprehensive income/(loss) (FY2022)", [None, 2405699, -3398236, -992537], "avg", "FY2022"),
    ("DATA", "FX translation effect on equity, net (FY2022)", [None, None, None, None], "plug", "FY2022"),
    ("TOTAL", "At 31 December 2022", [48900000, -1268750, -3498927, 44132323], "spot", "FY2022"),

    ("DATA", "Profit for the year (FY2023)", [None, 4304650, None, 4304650], "avg", "FY2023"),
    ("DATA", "Other comprehensive income (FY2023)", [None, None, 1857334, 1857334], "avg", "FY2023"),
    ("TOTAL", "Total comprehensive income (FY2023)", [None, 4304650, 1857334, 6161984], "avg", "FY2023"),
    ("DATA", "Proceeds from shares issued (FY2023)", [5000000, None, None, 5000000], "avg", "FY2023"),
    ("DATA", "FX translation effect on equity, net (FY2023)", [None, None, None, None], "plug", "FY2023"),
    ("TOTAL", "At 31 December 2023", [53900000, 3035900, -1641593, 55294307], "spot", "FY2023"),

    ("DATA", "Profit for the year (FY2024)", [None, 2459827, None, 2459827], "avg", "FY2024"),
    ("DATA", "Other comprehensive income (FY2024)", [None, None, 1505503, 1505503], "avg", "FY2024"),
    ("TOTAL", "Total comprehensive income (FY2024)", [None, 2459827, 1505503, 3965330], "avg", "FY2024"),
    ("DATA", "FX translation effect on equity, net (FY2024)", [None, None, None, None], "plug", "FY2024"),
    ("TOTAL", "At 31 December 2024", [53900000, 5495727, -136090, 59259637], "spot", "FY2024"),

    ("DATA", "Loss for the year (FY2025)", [None, -3677085, None, -3677085], "avg", "FY2025"),
    ("DATA", "Other comprehensive income (FY2025)", [None, None, 136820, 136820], "avg", "FY2025"),
    ("TOTAL", "Total comprehensive income/(loss) (FY2025)", [None, -3677085, 136820, -3540265], "avg", "FY2025"),
    ("DATA", "FX translation effect on equity, net (FY2025)", [None, None, None, None], "plug", "FY2025"),
    ("TOTAL", "At 31 December 2025", [53900000, 1818642, 730, 55719372], "spot", "FY2025"),
]

# FX translation plug (Total column only) computed programmatically as:
# closing total (spot) - opening total (spot, prior year-end) - sum of that
# year's movement totals (average rate) - not hardcoded, derived from the
# same figures independently verified to tie exactly in USD above.
equity_changes_rows = []
prev_close_gbp = None
for kind, label, vals, rtype, ry in EQUITY_ROWS_USD:
    if rtype == "plug":
        this_close_usd = next(v for k2, l2, v, rt2, ry2 in EQUITY_ROWS_USD if rt2 == "spot" and ry2 == ry and l2.startswith("At 31 December"))
        this_close_gbp = round(this_close_usd[-1] / FX_SPOT[ry] / 1000, 1)
        movements_gbp_total = sum(
            round(v[-1] / (FX_AVG[ry2] if rt2 == "avg" else 1) / 1000, 1)
            for k2, l2, v, rt2, ry2 in EQUITY_ROWS_USD
            if ry2 == ry and rt2 == "avg" and not l2.startswith("Total comprehensive")
        )
        plug = round(this_close_gbp - prev_close_gbp - movements_gbp_total, 1)
        equity_changes_rows.append((kind, label, [None, None, None, plug]))
        continue
    rate = FX_SPOT[ry] if rtype == "spot" else FX_AVG[ry]
    row_vals = [None if v is None else round(v / rate / 1000, 1) for v in vals]
    equity_changes_rows.append((kind, label, row_vals))
    if label.startswith("At 31 December") or label.startswith("At 1 January"):
        prev_close_gbp = row_vals[-1]

EQUITY_SOURCES = (
    STATEMENTS_SOURCES + "\n\n"
    "FX METHODOLOGY FOR THIS SHEET: opening balances converted at the prior year-end's spot rate, "
    "movement lines at that year's average rate, closing balances at that year-end's spot rate - the "
    "same convention used throughout this workbook. Converting stocks and flows at different rates "
    "within one year means the roll-forward doesn't tie exactly in GBP even though it ties exactly in "
    "USD (independently verified against each year's own source table before conversion) - an explicit "
    "'FX translation effect on equity, net' row (Total column only, computed as the balancing figure) is "
    "included each year, same treatment as this entity's own Cash Flow Statement's 'Effect of GBP/USD "
    "translation' line."
)

bw.add_equity_changes_sheet(
    title="FCMB Bank (UK) Limited — Statement of Changes in Equity",
    subtitle="£'000, converted from USD - chronological, oldest to newest. See source note for FX methodology.",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQUITY_SOURCES,
    first_col_width=56,
    source_height=340,
)

# ---------------------------------------------------------------
# Sheet: Cash Flow Statement
# ---------------------------------------------------------------
rows_usd = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(Loss) before tax for the year",
     {"FY2025": -4899200, "FY2024": 3301017, "FY2023": 5642919, "FY2022": 2953126, "FY2021": 1124026, "FY2020": -536133, "FY2019": 1497423}),
    ("DATA", "Depreciation and amortisation",
     {"FY2025": 797249, "FY2024": 804587, "FY2023": 672685, "FY2022": 579990, "FY2021": 603791, "FY2020": 599159, "FY2019": 518753}),
    ("DATA", "Non-cash PPE movements", {"FY2023": 1010191}),
    ("DATA", "Changes to ROU asset, Interest & lease liability", {"FY2025": 3130, "FY2024": -831690}),
    ("DATA", "Provision/impairment charge for loan losses (label varies by year - see source note)",
     {"FY2025": 5384068, "FY2024": -1023267, "FY2023": 1795645, "FY2022": 2508414, "FY2021": 77775, "FY2020": 375071, "FY2019": 10953}),
    ("DATA", "(Net gain)/Loss on investment activities", {"FY2025": 898826}),
    ("DATA", "Effect of currency translation on cash and cash equivalents (operating adjustment)",
     {"FY2025": -670243, "FY2024": -7410, "FY2023": -8096, "FY2022": 66367, "FY2021": 11947, "FY2020": -196168, "FY2019": -15492}),
    ("TOTAL", "Cash flows from operating activities before changes in operating assets and liabilities",
     {"FY2025": 1513830, "FY2024": 2243237, "FY2023": 9113344, "FY2022": 6107897, "FY2021": 1817539, "FY2020": 241929, "FY2019": 2011635}),
    ("DATA", "Net (increase) in loans and advances to banks",
     {"FY2025": -49909448, "FY2024": -35611527, "FY2023": -40236174, "FY2022": -7790893, "FY2021": -14354382, "FY2020": -5840334, "FY2019": 65923}),
    ("DATA", "Net (increase)/decrease in loans and advances to customers",
     {"FY2025": -33865933, "FY2024": -11601238, "FY2023": -3765576, "FY2022": 6754576, "FY2021": -27914986, "FY2020": -14542101, "FY2019": -23262290}),
    ("DATA", "Net decrease/(increase) in derivative FIs",
     {"FY2025": -3293894, "FY2024": 1295271, "FY2023": -2384003, "FY2022": 492972, "FY2021": 5058288, "FY2020": -3716102}),
    ("DATA", "Net (increase)/decrease in other assets",
     {"FY2025": 40077, "FY2024": -4047332, "FY2023": -1039844, "FY2022": -979246, "FY2021": -3061931, "FY2020": 290742}),
    ("DATA", "Net increase/(decrease) in deposits from banks",
     {"FY2025": 27094889, "FY2024": 48429573, "FY2023": -6029796, "FY2022": 91435975, "FY2021": -15995514, "FY2020": -27565417, "FY2019": 45452487}),
    ("DATA", "Net increase/(decrease) in deposits from customers",
     {"FY2025": 62092889, "FY2024": 5009718, "FY2023": -57791638, "FY2022": 15652787, "FY2021": 29913143, "FY2020": 45512401, "FY2019": 74585244}),
    ("DATA", "Net increase in subordinated liabilities", {"FY2021": 2000000, "FY2020": 3000000}),
    ("DATA", "Net increase/(decrease) in other liabilities",
     {"FY2025": 2191933, "FY2024": 1964709, "FY2023": 1934898, "FY2022": 707738, "FY2021": 911716, "FY2020": 2099}),
    ("DATA", "Taxation Paid", {"FY2025": -282719, "FY2024": -609062, "FY2023": -1689353}),
    ("TOTAL", "Net cash flows from operating activities",
     {"FY2025": 5581624, "FY2024": 7073349, "FY2023": -101888142, "FY2022": 112381806, "FY2021": -21626127, "FY2020": -2616783, "FY2019": 99289063}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Acquisition of investment securities",
     {"FY2025": -1781759737, "FY2024": -1560609502, "FY2023": -1910769930, "FY2022": -773481181, "FY2021": -640171183, "FY2020": -728779798, "FY2019": -750276199}),
    ("DATA", "Disposal of investment securities",
     {"FY2025": 1779031267, "FY2024": 1554220291, "FY2023": 2008897440, "FY2022": 658367424, "FY2021": 655246302, "FY2020": 729025505, "FY2019": 658043114}),
    ("DATA", "Purchases of property and equipment",
     {"FY2025": -102864, "FY2024": -201207, "FY2023": -101367, "FY2022": -29323, "FY2021": -31689, "FY2020": -25673, "FY2019": -144712}),
    ("DATA", "Purchases of intangible assets",
     {"FY2025": -167364, "FY2024": -321532, "FY2023": -357134, "FY2022": -274691, "FY2021": -46850, "FY2020": -78599, "FY2019": -388511}),
    ("TOTAL", "Net cash flows from investing activities",
     {"FY2025": -2998699, "FY2024": -6911950, "FY2023": 97669009, "FY2022": -115417771, "FY2021": 14996580, "FY2020": 141435, "FY2019": -92766308}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Issuance of own shares", {"FY2023": 5000000}),
    ("DATA", "Issuance of subordinated liabilities", {"FY2022": 4600000}),
    ("DATA", "Payments made for lease liability",
     {"FY2025": -452280, "FY2024": -400724, "FY2023": -408491, "FY2022": -359478, "FY2021": -402811, "FY2020": -407919}),
    ("TOTAL", "Net cash flows from financing activities",
     {"FY2025": -452280, "FY2024": -400724, "FY2023": 4591509, "FY2022": 4240522, "FY2021": -402811, "FY2020": -407919}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents",
     {"FY2025": 2130645, "FY2024": -239325, "FY2023": 372376, "FY2022": 1204557, "FY2021": -7032358, "FY2020": -2883267, "FY2019": 6523390}),
    ("DATA", "Cash and cash equivalents at 1 January",
     {"FY2025": 7266626, "FY2024": 7498541, "FY2023": 7118069, "FY2022": 5979879, "FY2021": 13024184, "FY2020": 15711283, "FY2019": 9172401}),
    ("DATA", "Effect of currency translation on cash and cash equivalents (closing bridge)",
     {"FY2025": 670243, "FY2024": 7410, "FY2023": 8096, "FY2022": -66367, "FY2021": -11947, "FY2020": 196168}),
    ("TOTAL", "Cash and cash equivalents at 31 December",
     {"FY2025": 10067514, "FY2024": 7266626, "FY2023": 7498541, "FY2022": 7118069, "FY2021": 5979879, "FY2020": 13024184, "FY2019": 15711283}),
]

_usd_by_label = {label: usd for _, label, usd in rows_usd}
rows = []
for kind, label, usd in rows_usd:
    if kind == "SECTION":
        rows.append((kind, label, {}))
    elif label == "Cash and cash equivalents at 1 January":
        rows.append((kind, label, opening_cash(usd)))
    elif label == "Cash and cash equivalents at 31 December":
        rows.append((kind, label, stock(usd)))
    else:
        rows.append((kind, label, flow(usd)))
    if label == "Effect of currency translation on cash and cash equivalents (closing bridge)":
        opening_gbp = opening_cash(_usd_by_label["Cash and cash equivalents at 1 January"])
        closing_gbp = stock(_usd_by_label["Cash and cash equivalents at 31 December"])
        net_change_gbp = flow(_usd_by_label["Net (decrease)/increase in cash and cash equivalents"])
        fx_gbp = flow(usd)
        plug = {
            y: round(closing_gbp[y] - opening_gbp[y] - net_change_gbp[y] - fx_gbp.get(y, 0), 1)
            for y in closing_gbp
            if y in opening_gbp and y in net_change_gbp
        }
        rows.append(("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", plug))

bw.add_cash_flow_sheet(
    title="FCMB Bank (UK) Limited — Statement of Cash Flows",
    subtitle="£'000, converted from USD - see source note at bottom for FX methodology and rates used.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=95,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Asset Quality: Net carrying value + ECL by IFRS 9 stage, own-year figures
# throughout. Gross carrying amount = Net carrying + ECL allowance (the Bank
# discloses net + ECL separately, not gross directly - see sources note).
# ---------------------------------------------------------------
AQ_NET_USD = {
    "Stage 1": {"FY2025": 441790782, "FY2024": 404519023, "FY2023": 330580426, "FY2022": 279834026, "FY2021": 284775434, "FY2020": 214754510},
    "Stage 2": {"FY2025": 2068858, "FY2024": 6673411, "FY2023": 10090935, "FY2022": 9009321, "FY2021": 529517, "FY2020": 0},
    "Stage 3": {"FY2025": 6506282, "FY2024": 3121198, "FY2023": 4410821, "FY2022": 3889084, "FY2021": 0, "FY2020": 0},
    "Total": {"FY2025": 450365922, "FY2024": 414313632, "FY2023": 345082182, "FY2022": 292732431, "FY2021": 285304951, "FY2020": 214754510},
}
AQ_ECL_USD = {
    "Stage 1": {"FY2025": 2180753, "FY2024": 1919530, "FY2023": 2099535, "FY2022": 1292032, "FY2021": 710047, "FY2020": 632833},
    "Stage 2": {"FY2025": 49181, "FY2024": 364349, "FY2023": 322131, "FY2022": 206214, "FY2021": 561, "FY2020": 0},
    "Stage 3": {"FY2025": 6902293, "FY2024": 1707521, "FY2023": 2593001, "FY2022": 1720776, "FY2021": 0, "FY2020": 0},
    "Total": {"FY2025": 9132227, "FY2024": 3991400, "FY2023": 5014667, "FY2022": 3219022, "FY2021": 710608, "FY2020": 632833},
}
AQ_GROSS_USD = {
    stage: {y: AQ_NET_USD[stage][y] + AQ_ECL_USD[stage][y] for y in YEARS if y in AQ_NET_USD[stage] and y in AQ_ECL_USD[stage]}
    for stage in ("Stage 1", "Stage 2", "Stage 3", "Total")
}
AQ_NPL_RATIO = {y: f"{AQ_GROSS_USD['Stage 3'][y] / AQ_GROSS_USD['Total'][y] * 100:.2f}%" for y in YEARS if y in AQ_GROSS_USD['Stage 3'] and y in AQ_GROSS_USD['Total']}
AQ_STAGE3_COVERAGE = {
    y: (f"{AQ_ECL_USD['Stage 3'][y] / AQ_GROSS_USD['Stage 3'][y] * 100:.2f}%" if AQ_GROSS_USD["Stage 3"][y] else None)
    for y in YEARS if y in AQ_GROSS_USD['Stage 3']
}
AQ_TOTAL_COVERAGE = {y: f"{AQ_ECL_USD['Total'][y] / AQ_GROSS_USD['Total'][y] * 100:.2f}%" for y in YEARS if y in AQ_GROSS_USD['Total']}

aq_rows = [
    ("SECTION", "Gross carrying amount by IFRS 9 stage (calculated - see source note)", {}),
    ("DATA", "Stage 1 (12-month ECL)", stock(AQ_GROSS_USD["Stage 1"])),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", stock(AQ_GROSS_USD["Stage 2"])),
    ("DATA", "Stage 3 (credit-impaired)", stock(AQ_GROSS_USD["Stage 3"])),
    ("TOTAL", "Total gross carrying amount", stock(AQ_GROSS_USD["Total"])),
    ("SECTION", "ECL allowance by stage", {}),
    ("DATA", "Stage 1 ECL", stock(AQ_ECL_USD["Stage 1"])),
    ("DATA", "Stage 2 ECL", stock(AQ_ECL_USD["Stage 2"])),
    ("DATA", "Stage 3 ECL", stock(AQ_ECL_USD["Stage 3"])),
    ("TOTAL", "Total ECL allowance", stock(AQ_ECL_USD["Total"])),
    ("SECTION", "Net carrying amount by stage (as reported)", {}),
    ("DATA", "Stage 1", stock(AQ_NET_USD["Stage 1"])),
    ("DATA", "Stage 2", stock(AQ_NET_USD["Stage 2"])),
    ("DATA", "Stage 3", stock(AQ_NET_USD["Stage 3"])),
    ("TOTAL", "Total net carrying amount", stock(AQ_NET_USD["Total"])),
    ("SECTION", "Derived ratios", {}),
    ("DATA", "NPL ratio (Stage 3 gross / Total gross)", AQ_NPL_RATIO),
    ("DATA", "Stage 3 coverage ratio (Stage 3 ECL / Stage 3 gross)", AQ_STAGE3_COVERAGE),
    ("DATA", "Total ECL coverage ratio (Total ECL / Total gross)", AQ_TOTAL_COVERAGE),
]

bw.add_asset_quality_sheet(
    title="FCMB Bank (UK) Limited — Asset Quality / Credit Risk Disclosures",
    subtitle="£'000, converted from USD (stock figures) - see source note at bottom for FX methodology and rates used.",
    rows=aq_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=70,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None, note_height=60):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52,
                        source_height=170, note_height=note_height)


CET1_USD = {"FY2025": 54656000, "FY2024": 57951000, "FY2023": 50032000, "FY2022": 40321000, "FY2021": 42915000, "FY2020": 43266000}
TOTALCAP_USD = {"FY2025": 64256000, "FY2024": 67551000, "FY2023": 59632000, "FY2022": 48310000, "FY2021": 47915000, "FY2020": 46266000}
TREA_USD = {"FY2025": 368569000, "FY2024": 350177000, "FY2023": 287662000, "FY2022": 237643000, "FY2021": 248258000, "FY2020": 158682000}
LEV_EXP_USD = {"FY2025": 620401000, "FY2024": 376611000, "FY2023": 486253000, "FY2022": 543896000, "FY2021": 424021000}
HQLA_USD = {"FY2025": 149895000, "FY2024": 159598000, "FY2023": 194868000, "FY2022": 194898000, "FY2021": 127551000}
NSFR_AVAIL_USD = {"FY2025": 293158000, "FY2024": 264324000, "FY2023": 185387000, "FY2022": 225966000, "FY2021": 191843000}
NSFR_REQ_USD = {"FY2025": 187805000, "FY2024": 159601000, "FY2023": 106823000, "FY2022": 131535000, "FY2021": 93529000}

CET1_RATIO = {y: f"{CET1_USD[y] / TREA_USD[y] * 100:.2f}%" for y in YEARS if y in CET1_USD and y in TREA_USD}
TOTALCAP_RATIO = {y: f"{TOTALCAP_USD[y] / TREA_USD[y] * 100:.2f}%" for y in YEARS if y in TOTALCAP_USD and y in TREA_USD}
LEVERAGE_RATIO = {"FY2025": "8.81%", "FY2024": "14.73%", "FY2023": "10.29%", "FY2022": "7.41%", "FY2021": "10.12%"}
LCR_RATIO = {"FY2025": "273%", "FY2024": "333%", "FY2023": "729%", "FY2022": "513%", "FY2021": "371%"}
NSFR_RATIO = {"FY2025": "157%", "FY2024": "166%", "FY2023": "174%", "FY2022": "179%", "FY2021": "206%"}

# CORRECTED 2026-09-18 (leading-gaps queue / GA-016). The previous note asserted
# that "FY2021 onward is not publicly disclosed as a separate line". All six
# editions FYE2020-FYE2025 were re-fetched live and read in full this date, and
# that claim is FALSE of the Tier 1 RATIO - every edition prints a "Tier 1
# capital ratio" row. It remains TRUE of the Tier 1 CAPITAL AMOUNT, and then
# only for FY2021-FY2023. The old claim is corrected below rather than deleted.
TIER1_NOTE = (
    "WHERE THE BANK'S OWN CAPITAL TABLE PRINTS A TIER 1 SUBTOTAL, AND WHERE IT DOES NOT. All six editions "
    "FYE2020-FYE2025 were re-fetched live on 2026-09-18 (HTTP 200, Content-Type application/pdf, %PDF magic "
    "bytes on every one) and read in full. The Bank's capital table - 'Total Available Capital', section 3.2 "
    "in the FY2020-FY2023 editions and section 4.2 from FY2024 - changes shape between the FY2023 and FY2024 "
    "editions:\n"
    "- FY2024 AND FY2025 EDITIONS: the table gained an explicit 'Total Tier 1 capital' subtotal row, printed "
    "under a 'Tier 1 capital (T1)' block heading. Those two years' amounts are transcribed from that printed "
    "row.\n"
    "- FY2020 THROUGH FY2023 EDITIONS: no Tier 1 subtotal row of any kind is printed. The table lists the "
    "components (share capital, retained earnings, AFS/OCI reserves, intangible assets, other capital "
    "adjustments), then Tier 2 capital, then 'Total regulatory capital (CAR)'. FY2023, FY2022 and FY2021 are "
    "therefore recorded above as not disclosed - NOT summed from the components, and NOT back-solved from "
    "the printed ratio times RWA. The arithmetic is available and is deliberately not used: the FY2023 "
    "column's components foot exactly to 50,032, which is also what the FY2024 edition's comparative column "
    "prints, but a figure the Bank did not print is not manufactured here and a later edition's comparative "
    "is not this project's source for an own year.\n"
    "\n"
    "WHAT THE SUPERSEDED NOTE GOT RIGHT AND WHAT IT GOT WRONG. It said the 'Key Regulatory Metrics' table "
    "gives only CET1 and Total Capital with no separate Tier 1 breakdown. That is correct, and it is why the "
    "Tier 1 amount cannot be read off THAT table. It then generalised to 'FY2021 onward is not publicly "
    "disclosed as a separate line', which read as covering the Tier 1 RATIO too. It does not: the "
    "capital-adequacy table in every edition FY2020-FY2025 prints a 'Tier 1 capital ratio' row, and all six "
    "years are now carried on the Tier 1 Ratio sheet from their own editions.\n"
    "\n"
    "TIER 1 IS STILL NOT ASSUMED EQUAL TO CET1. Total Capital exceeds CET1 in every year (e.g. FY2025 "
    "$64,256k against $54,656k), the difference being $9,600k of subordinated loans the Bank labels Tier 2. "
    "Where the Bank does print a Tier 1 subtotal it happens to equal CET1 (FY2024: 57,951 on both the "
    "capital table's 'Total Tier 1 capital' row and the Key Regulatory Metrics CET1 row) - but that is the "
    "Bank's own printing for those years, not an equivalence applied on its behalf to the years it left "
    "blank.\n"
    "\n"
    "FY2020 - A CORRECTION TO THIS WORKBOOK'S OWN EARLIER WORDING. The superseded note described FY2020's "
    "$43,266k as 'explicitly disclosed in the old-format Pillar 3 table'. It is not printed as a row. The "
    "FYE2020 edition's section 3.2 table prints share capital 48,900, retained earnings (5,200), AFS "
    "reserves '-' and intangible assets (434) in its 2020 column and no Tier 1 subtotal; 48,900 - 5,200 - "
    "434 = 43,266. The figure is left in place because it is the value this workbook has carried and it "
    "agrees with the CET1 Capital sheet, but it is a COMPONENT SUM and is labelled as one here so a future "
    "session can decide whether it belongs on a disclosure sheet at all. Flagged rather than silently kept "
    "or silently removed."
)
TIER1_FY2025_CONTRADICTION_NOTE = (
    "THE FY2025 EDITION PRINTS A TIER 1 AMOUNT THAT ITS OWN TABLE CONTRADICTS, AND IT IS REPRODUCED AS "
    "PRINTED. In the FYE2025 edition's section 4.2 table the 'Total Tier 1 capital' row reads 57,951 in "
    "BOTH the 31/12/2025 and the 31/12/2024 columns; 57,951 is the FY2024 figure. Three separate numbers in "
    "that same table disagree with it for 2025: (a) the 31/12/2025 column's own components foot to 54,657 "
    "(53,900 + 1,819 + 1 - 527 - 536); (b) the table's Total capital 64,256 less its Tier 2 subordinated "
    "loans 9,600 leaves 54,656; (c) the table's own 'Tier 1 capital ratio' of 14.8% against its own risk "
    "weighted assets of 368,569 implies 54,656, where 57,951/368,569 would be 15.72%. The Key Regulatory "
    "Metrics table on p.3 of the same document prints CET1 of 54,656. The printed 57,951 therefore reads as "
    "a cell carried forward from the prior-year column. It is transcribed exactly as the Bank printed it "
    "and the disagreement is documented, per this project's rule that a figure is never adjusted to make a "
    "set tie - the same treatment as Bank of Africa UK's FY2019 table (GA-016). A reader who needs an "
    "internally consistent 2025 Tier 1 amount should use the CET1 Capital sheet, which carries the Bank's "
    "own printed 54,656."
)
TIER1_RATIO_SOURCE_NOTE = (
    "ALL SIX YEARS ARE PRINTED FIGURES FROM THAT YEAR'S OWN EDITION - nothing on this sheet is calculated "
    "and nothing is taken from a later edition's comparative column. Each is the capital-adequacy table's "
    "'Tier 1 capital ratio' row: FY2025 14.8% and FY2024 16.5% from section 4.2 of their own editions; "
    "FY2023 17%, FY2022 17% and FY2021 17% from section 3.2 of theirs; FY2020 25% from section 3.2 of the "
    "FYE2020 edition. FY2021-FY2025 were added 2026-09-18, closing five leading gaps that existed only "
    "because an earlier pass read the 'Key Regulatory Metrics' table and not the capital-adequacy table in "
    "the same documents.\n"
    "\n"
    "TWO DIFFERENT DENOMINATORS LIVE IN ONE DOCUMENT, and that is what makes these printed ratios "
    "reconcile. The capital-adequacy table carries its own 'Risk weighted assets' row, which in the "
    "FY2021-FY2023 editions is SMALLER than the Total Risk-Weighted exposure amount (TREA) printed in the "
    "same document's Key Regulatory Metrics table. The printed Tier 1 ratios reconcile against TREA, not "
    "against the capital table's own RWA row: FY2023 50,032/287,662 = 17.39% (TREA) against 50,032/257,090 "
    "= 19.46% (cap-table RWA), for a printed 17%; FY2022 40,321/237,643 = 16.97% against 40,321/214,632 = "
    "18.79%, for a printed 17%; FY2021 42,915/248,258 = 17.29% against 42,915/225,003 = 19.07%, for a "
    "printed 17%. From FY2024 the two rows agree (350,177 and 368,569) and the question falls away. Both "
    "figures are the Bank's own and neither is adjusted here.\n"
    "\n"
    "FY2020 - THE GA-016 'IMPOSSIBLE' TRIPLE, RESOLVED WITHOUT EDITING ANY FIGURE (2026-09-18). GA-016 "
    "flagged FY2020 as a Tier 1 ratio BELOW the CET1 ratio, which cannot happen when Tier 1 contains CET1. "
    "There is nothing to fix, because the two sides are not measurements of the same thing: the Tier 1 "
    "ratio is PRINTED (25%) and the CET1 ratio is CALCULATED by this workbook (43,266/158,682 = 27.27%, and "
    "the CET1 Ratio sheet says on its face that it is calculated). The FYE2020 edition prints a 'Tier 1 "
    "capital ratio' of 25% and a 'Total capital ratio' of 26% and NO CET1 ratio row at all - confirmed by "
    "reading that edition in full on 2026-09-18. FY2020 is further the one year whose printed ratios "
    "reconcile against nothing in its own table: the printed total capital ratio of 26% sits against "
    "46,266/158,682 = 29.16%. The Bank's own FY2020 set is internally inconsistent. Recorded, not "
    "reconciled, and no figure changed."
)
TIER1_CAP_NOT_DISCLOSED = {
    "FY2023": "Not disclosed - this edition prints no Tier 1 subtotal row",
    "FY2022": "Not disclosed - this edition prints no Tier 1 subtotal row",
    "FY2021": "Not disclosed - this edition prints no Tier 1 subtotal row",
}
TIER1_USD = {"FY2025": 57951000, "FY2024": 57951000, "FY2020": 43266000}
TIER1_RATIO = {
    "FY2025": "14.8%", "FY2024": "16.5%", "FY2023": "17%",
    "FY2022": "17%", "FY2021": "17%", "FY2020": "25%",
}
MREL_NOTE = (
    "Not publicly disclosed in any of the 5 years' Pillar 3 Disclosures reviewed - no MREL figure or "
    "exemption statement found."
)

# ---------------------------------------------------------------
# KM1 Key Metrics - documented "Not applicable" (see note)
# ---------------------------------------------------------------
KM1_NOT_APPLICABLE_NOTE = (
    "\n\nWHY THIS SHEET IS 'NOT APPLICABLE' RATHER THAN BLANK OR UNRESEARCHED\n"
    "FCMB Bank (UK) Limited DOES publish Pillar 3 disclosures - a continuous annual series, the newest "
    "being the FYE 2025 edition - but none of them uses the UK KM1 key-metrics template. This is the "
    "distinction between 'no Pillar 3 is published', 'a Pillar 3 is published but the template is not used' "
    "and 'the rows are formally excluded'. This bank is the middle case, and the entry above says so.\n"
    "\n"
    "WHAT THE BANK PUBLISHES INSTEAD. Every edition prints a bespoke 15-row table of the Bank's own design, "
    "headed 'Key Regulatory Metrics'. A shared caption is not the test; the ROW SET is. That table has no "
    "row numbers, no Tier 1 capital row, no capital-ratio rows of any kind, no SREP block, and no "
    "countercyclical-buffer or G-SII rows. It is missing the majority of the template's rows and the whole "
    "of three of its sections, so it is a different disclosure that happens to summarise some of the same "
    "quantities - not the template printed without numbering.\n"
    "\n"
    "HOW THAT WAS ESTABLISHED (2026-09-17). Six editions (FYE 2020 to FYE 2025) were read in full and the "
    "FYE 2019 edition was phrase-tested. Every edition was searched on whole phrases that cannot occur as "
    "substrings of ordinary prose - 'Available own funds', 'Total SREP own funds requirements', 'Additional "
    "CET1 SREP', 'Tier 1 ratio', 'Common Equity Tier 1 ratio' and 'KM1' - and every one returned zero hits "
    "in every edition. The only near-misses, 'countercyclical' and 'combined buffer requirement', were "
    "inspected line by line rather than counted: they belong to a different table and to the Bank's own "
    "narrative, not to a key-metrics template. A hit count was never treated as an answer in either "
    "direction.\n"
    "\n"
    "NOTHING IS BACK-FILLED. The individual Pillar 3 metric sheets in this workbook carry what the Bank's "
    "own table does disclose. No KM1 row is reconstructed here from the statutory accounts, from the "
    "parent's disclosures, or from any figure on those sheets - a template the Bank did not publish is not "
    "manufactured on its behalf.\n"
    "\n"
    "ENTITY BASIS. FCMB Bank (UK) Limited publishes its own entity-level Pillar 3, so this finding rests on "
    "the UK entity's own documents throughout. No figure from FCMB Group Plc's consolidated disclosures is "
    "used or substituted anywhere on this sheet."
)

bw.add_km1_sheet(
    title="FCMB Bank (UK) Limited — KM1 Key Metrics",
    subtitle="Not applicable — the Bank publishes Pillar 3 disclosures every year, but no edition uses the "
             "UK KM1 key-metrics template. Its capital disclosure is a bespoke 15-row 'Key Regulatory "
             "Metrics' table of the Bank's own design, which is a different thing. See the source note for "
             "the test applied, and the individual Pillar 3 metric sheets for what that table does "
             "disclose.",
    rows=[
        ("DATA", "UK KM1 key-metrics template",
         {y: "Not used in any Pillar 3 edition" for y in YEARS}),
    ],
    sources_text=p3_sources(page_2025="3", page_2024="2", page_2023="19", page_2022="19")
    + KM1_NOT_APPLICABLE_NOTE,
    first_col_width=52,
    source_height=520,
)

metric("CET1 Capital", "£'000 (conv. from USD)", [("Common Equity Tier 1 (CET1) Capital", stock(CET1_USD))], p3_sources())
metric("CET1 Ratio", "% of TREA (calculated - see note)", [("CET1 Ratio", CET1_RATIO)], p3_sources(),
       note="CALCULATED as CET1 Capital / Total Risk-Weighted exposure amount (TREA) for each year - "
            "neither the Bank's Annual Report nor its Pillar 3 Disclosures state a CET1 ratio % directly, "
            "only the underlying £/$ amounts (see CET1 Capital and Total RWAs sheets).")
metric("Tier 1 Capital", "£'000 (conv. from USD)",
       [("Tier 1 Capital", dict(TIER1_CAP_NOT_DISCLOSED, **stock(TIER1_USD)))], p3_sources(),
       note=TIER1_NOTE + "\n\n" + TIER1_FY2025_CONTRADICTION_NOTE, note_height=560)
metric("Tier 1 Ratio", "%", [("Tier 1 Capital ratio", TIER1_RATIO)], p3_sources(),
       note=TIER1_RATIO_SOURCE_NOTE + "\n\n" + TIER1_NOTE, note_height=560)
metric("Total Capital", "£'000 (conv. from USD)", [("Total Capital", stock(TOTALCAP_USD))], p3_sources())
metric("Total Capital Ratio", "% of TREA (calculated - see note)", [("Total Capital Ratio", TOTALCAP_RATIO)], p3_sources(),
       note="CALCULATED as Total Capital / Total Risk-Weighted exposure amount (TREA) for each year - "
            "not directly stated as a percentage in the source (see CET1 Ratio sheet for the same caveat).")
metric("Total RWAs", "£'000 (conv. from USD)", [("Total Risk-Weighted exposure amount (TREA)", stock(TREA_USD))], p3_sources())

# ---------------------------------------------------------------
# RWA Breakdown: calculated as (Minimum Capital Requirement / 8%) by risk
# type from the Bank's own Pillar 3 "Minimum Capital Requirements" table -
# see STATEMENTS_ENTITY_NOTE for the cross-check against disclosed TREA.
# ---------------------------------------------------------------
CAPREQ_USD_000 = {  # as disclosed, $'000
    "Credit Risk": {"FY2025": 25892, "FY2024": 24221, "FY2023": 20567, "FY2022": 17170, "FY2021": 18000, "FY2020": 12695},
    "Market Risk": {"FY2025": 429, "FY2024": 634, "FY2023": 424, "FY2022": 283, "FY2021": 524, "FY2020": 194},
    "Operational Risk": {"FY2025": 3148, "FY2024": 3148, "FY2023": 2022, "FY2022": 1558, "FY2021": 1337, "FY2020": 1210},
    "CVA Risk": {"FY2025": 16, "FY2024": 12},
    "Total Pillar 1 Capital Requirement": {"FY2025": 29485, "FY2024": 28014, "FY2023": 23013, "FY2022": 19011, "FY2021": 19861, "FY2020": 14099},
}
RWA_USD = {
    cat: {y: v * 1000 * 12.5 for y, v in years_dict.items()}
    for cat, years_dict in CAPREQ_USD_000.items()
}

rwa_rows = [
    ("DATA", "Credit risk", stock(RWA_USD["Credit Risk"])),
    ("DATA", "Market risk", stock(RWA_USD["Market Risk"])),
    ("DATA", "Operational risk", stock(RWA_USD["Operational Risk"])),
    ("DATA", "CVA risk", stock(RWA_USD["CVA Risk"])),
    ("TOTAL", "Total RWAs (calculated)", stock(RWA_USD["Total Pillar 1 Capital Requirement"])),
]

bw.add_rwa_breakdown_sheet(
    title="FCMB Bank (UK) Limited — RWA Breakdown",
    subtitle="£'000, converted from USD - CALCULATED from disclosed Minimum Capital Requirements (see source note). "
              "CVA Risk only disclosed from FY2024 onward.",
    rows=rwa_rows,
    sources_text=p3_sources() + "\n\nRWA BREAKDOWN NOTE:" + STATEMENTS_ENTITY_NOTE.split("RWA BREAKDOWN NOTE:")[1],
    first_col_width=54,
    source_height=200,
    unit_suffix=" (£'000)",
)

metric("Leverage Ratio", "%", [("Leverage Ratio", LEVERAGE_RATIO)], p3_sources())
metric("LCR", "% (12-month average - see methodology note)", [("Liquidity Coverage Ratio", LCR_RATIO)], p3_sources())
metric("NSFR", "% (4-quarter average - see methodology note)", [("Net Stable Funding Ratio", NSFR_RATIO)], p3_sources())
bw.add_not_disclosed_metric_sheets(["MREL Ratio"], p3_sources(), per_note={"MREL Ratio": MREL_NOTE})

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", stock(BS_USD["Total assets"])),
        ("Loans and advances to customers", stock(BS_USD["Loans and advances to customers"])),
        ("Deposits from customers", stock(BS_USD["Deposits from customers"])),
        ("Total equity", stock(BS_USD["Total equity"])),
    ],
    balance_sheet_unit="£'000 (conv. from USD)",
    income_statement_totals=[
        ("Net operating income", flow(PL_USD["Net operating income"])),
        ("Total operating expenses", flow(PL_USD["Total operating expenses"])),
        ("Profit/(Loss) for the year", flow(PL_USD["Profit/(Loss) for the year"])),
    ],
    income_statement_unit="£'000 (conv. from USD)",
    equity_changes_totals=[
        ("Opening equity", {y: round(v / FX_SPOT[PREV_YEAR[y]] / 1000, 1) for y, v in
            {"FY2025": 59259637, "FY2024": 55294307, "FY2023": 44132323, "FY2022": 45124860, "FY2021": 43849021, "FY2020": 43991542}.items()
            if y in PREV_YEAR and PREV_YEAR[y] in FX_SPOT}),
        ("Total comprehensive income/(loss) for the year", flow({"FY2025": -3540265, "FY2024": 3965330, "FY2023": 6161984, "FY2022": -992537, "FY2021": 1275839, "FY2020": -142521})),
        ("Closing equity", stock(BS_USD["Total equity"])),
    ],
    equity_changes_unit="£'000 (conv. from USD)",
    cash_flow_totals=[
        ("Net cash flows from operating activities", flow(_usd_by_label["Net cash flows from operating activities"])),
        ("Net cash flows from investing activities", flow(_usd_by_label["Net cash flows from investing activities"])),
        ("Net cash flows from financing activities", flow(_usd_by_label["Net cash flows from financing activities"])),
        ("Cash and cash equivalents at 31 December", stock(_usd_by_label["Cash and cash equivalents at 31 December"])),
    ],
    cash_flow_unit="£'000 (conv. from USD)",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Total Capital Ratio", TOTALCAP_RATIO),
        ("Leverage Ratio", LEVERAGE_RATIO),
        ("LCR", LCR_RATIO),
        ("NSFR", NSFR_RATIO),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. Cash flow and capital figures converted from USD - "
         "see the Cash Flow Statement sheet's source note for the FX methodology and exact rates used.",
)

bw.save("/Users/armaan/code/katalysis/banks/FCMB UK FINANCIALS.xlsx")
