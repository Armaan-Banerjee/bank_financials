import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# PILLAR-3-ONLY WORKBOOK: The Bank of New York Mellon (International) Limited
# takes the FRS 101 cash-flow-statement disclosure exemption every year (its
# ultimate parent, The Bank of New York Mellon Corporation, publishes its own
# consolidated financial statements including a cash flow statement) - no
# Statement of Cash Flows exists in any year's accounts, confirmed directly in
# the FY2023 and FY2025 financial statements (identical wording) and
# previously also confirmed via 3 separate Companies House filings
# (FY2021/FY2023/FY2025). Pillar 3 disclosures, by contrast, are complete and
# strong for all 5 years, so this workbook keeps the standard 13-sheet
# structure but the "Cash Flow Statement" sheet documents the exemption
# instead of line items, and the Overview sheet omits the cash-flow chart.

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, calendar year-end (31 December)
YEAR_LABEL = {y: y for y in YEARS}

FS2025_URL = "https://www.bnymellon.com/content/dam/bnymellon/documents/pdf/investor-relations/Signed-2025-BNYMIL-Financial-Statements.pdf"
FS2023_URL = "https://www.bnymellon.com/content/dam/bnymellon/documents/pdf/investor-relations/bnymil-financial-statement-2023.pdf"
FS2021_URL = ("https://find-and-update.company-information.service.gov.uk/company/03236121/filing-history/"
              "MzMzNzcwMzgzM2FkaXF6a2N4/document?format=pdf&download=0")  # Companies House, filed 28 Apr 2022, scanned/image-only

P3_2021_URL = "https://www.bnymellon.com/content/dam/bnymellon/documents/pdf/investor-relations/the-bank-of-new-york-mellon-international-limited-2021-pillar-3-disclosure.pdf"
P3_2022_URL = "https://www.bnymellon.com/content/dam/bnymellon/documents/pdf/investor-relations/the-bank-of-new-york-mellon-international-limited-2022-pillar-3-disclosure.pdf"
P3_2023_URL = "https://www.bnymellon.com/content/dam/bnymellon/documents/pdf/investor-relations/the-bank-of-new-york-mellon-international-limited-2023-pillar-3-disclosure.pdf"
P3_2024_URL = "https://www.bnymellon.com/content/dam/bnymellon/documents/pdf/investor-relations/the-bank-of-new-york-mellon-international-limited-2024-pillar-3-disclosure.pdf"
P3_2025_URL = "https://www.bnymellon.com/content/dam/bnymellon/documents/pdf/investor-relations/the-bank-of-new-york-mellon-international-limited-2025-pillar-3-disclosure.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: The Bank of New York Mellon (International) Limited (company 03236121, FRN 183100) is a wholly-"
    "owned subsidiary of The Bank of New York Mellon Corporation (US). Figures are the Company's own entity-level "
    "disclosure throughout; the 2021 Pillar 3 report separately labelled 'Consolidated' and 'Solo' bases but both "
    "were identical every year shown (the Company has no material subsidiaries of its own), and from the 2022 "
    "report onward BNY Mellon International's Pillar 3 disclosures present a single, unified figure. Functional/"
    "presentational currency is GBP throughout - no FX conversion needed."
)

EXEMPTION_NOTE = (
    "FRS 101 CASH-FLOW EXEMPTION: this entity's Annual Report and Financial Statements state every year: \"The "
    "Company's ultimate parent undertaking, The Bank of New York Mellon Corporation includes the Company and all "
    "its subsidiary undertakings in its consolidated financial statements... Accordingly, the Company is a "
    "qualifying entity for the purpose of FRS 101 disclosure exemptions... the Company has applied the exemptions "
    "available under FRS 101 in respect of the following disclosures: A Statement of cash flows and related "
    f"notes...\" - FY2025 Financial Statements, note 1.1, p.29 - {FS2025_URL}; identical wording confirmed in the "
    f"FY2023 Financial Statements, note 1.1, p.41 - {FS2023_URL}. This has also been independently confirmed via "
    "Companies House filings for FY2021, FY2023 and FY2025 (OCR'd scanned filings, prior research pass). No "
    "Statement of Cash Flows or cash-flow notes exist in any of the entity's published accounts for any year - this "
    "is a standing structural feature of the entity, not a one-off or a data gap. Per the project's established "
    "policy for this exemption (see United Trust Bank Limited, self-skipped for the same reason), this workbook is "
    "built as a PILLAR-3-ONLY variant: all 11 Pillar 3 metric sheets are fully populated below, but no cash flow "
    "figures exist to show. See the Overview sheet for the equivalent treatment there."
)

CASH_FLOW_SOURCES = ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE

STATEMENTS_SOURCES = (
    "Sources - The Bank of New York Mellon (International) Limited's own audited financial statements:\n"
    f"FY2025/FY2024: Financial Statements, year ended 31 December 2025, Statement of profit and loss p.25, "
    f"Statement of comprehensive income p.26, Balance sheet p.27, Statement of changes in equity p.28 - {FS2025_URL}\n"
    f"FY2023/FY2022: Financial Statements, year ended 31 December 2023, Statement of profit and loss p.37, "
    f"Other comprehensive income p.38, Balance sheet p.39, Statement of changes in equity p.40 - {FS2023_URL}\n"
    f"FY2021 (and FY2020 comparative used for the opening equity roll-forward): Financial Statements, year ended 31 "
    f"December 2021, Statement of profit and loss p.35, Other comprehensive income p.36, Balance sheet p.37, "
    f"Statement of changes in equity p.38 - Companies House filing, 28 April 2022 (scanned/image-only, visually "
    f"transcribed) - {FS2021_URL}\n\n" + ENTITY_NOTE
)

PRESENTATION_NOTE = (
    "PRESENTATION NOTE: this entity's statement structure changed twice across the 5 years shown. (1) Income "
    "statement: FY2021-FY2023 place 'Income from investments in affiliates' before a combined 'Total income' "
    "subtotal; FY2024-FY2025 instead show a narrower 'Total operating income' (excluding investments-in-affiliates "
    "income) and add investments-in-affiliates income only after 'Total operating expenses', immediately before "
    "'Profit before taxation' - both years' own reported total is shown on the 'Total operating income / Total "
    "income' row below, not reconciled to a common basis. FY2024 also separately discloses 'Amounts written off "
    "investments in affiliates' (£57,148k), a line that doesn't exist in the other 4 years. (2) Other comprehensive "
    "income: FY2021-FY2023 split the FVOCI movement into 'Movement in financial assets measured at FVOCI' and a "
    "separate 'Change in ECL on financial assets measured at FVOCI' line; FY2024-FY2025 combine both into a single "
    "'Net movement in financial instruments measured at FVOCI' line - shown on the FVOCI-movement row with the ECL "
    "row left blank those 2 years, not split arbitrarily. (3) Balance sheet: FY2021's own statement uses the label "
    "'Cash in hand and on demand balances at central banks' (relabelled 'Cash and balances at central banks' from "
    "FY2022 onward - same line) and has no separate Intangible assets line (first appears FY2022); 'Deferred tax "
    "asset'/'Deferred tax liabilities' appear as explicit lines (value or nil) only in the years the Company had a "
    "recognised balance or an adjacent-year comparative required it - blank cells mean the year's own statement has "
    "no such line at all, not that the value is unknown. 'Loan due to fellow group undertakings' is a FY2025-only "
    "line (a new, discrete intercompany funding arrangement that year)."
)


def p3_sources(page):
    return (
        "Sources - The Bank of New York Mellon (International) Limited Pillar 3 Disclosure, Table 1: UK KM1 - Key "
        "metrics template (entity-level basis):\n"
        f"FY2025: Pillar 3 Disclosure, December 31, 2025, p.{page['FY2025']} - {P3_2025_URL}\n"
        f"FY2024: Pillar 3 Disclosure, December 31, 2024, p.{page['FY2024']} - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosure, December 31, 2023, p.{page['FY2023']} - {P3_2023_URL}\n"
        f"FY2022: Pillar 3 Disclosure, December 31, 2022, p.{page['FY2022']} - {P3_2022_URL}\n"
        f"FY2021: Pillar 3 Disclosure, December 31, 2021, p.{page['FY2021']} (\"1.8 Key metrics\") - {P3_2021_URL}\n"
        + ENTITY_NOTE
    )


KM1_PAGE = {"FY2025": "5", "FY2024": "6", "FY2023": "6", "FY2022": "8", "FY2021": "10-11"}

bw = BankWorkbook(bank_name="The Bank of New York Mellon (International) Limited", years=YEARS,
                   year_label=YEAR_LABEL, header_color="1F3B57")

# ---------------------------------------------------------------
# Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 2666888, "FY2024": 2687665, "FY2023": 3781275, "FY2022": 4706360, "FY2021": 4949582}),
    ("DATA", "Loans and advances to banks", {"FY2025": 2037724, "FY2024": 1891637, "FY2023": 1645021, "FY2022": 2520019, "FY2021": 1579113}),
    ("DATA", "Loans and advances to customers", {"FY2025": 28495, "FY2024": 173578, "FY2023": 108153, "FY2022": 138345, "FY2021": 104419}),
    ("DATA", "Investment securities", {"FY2025": 2969599, "FY2024": 2994460, "FY2023": 3072747, "FY2022": 4054942, "FY2021": 4357861}),
    ("DATA", "Investments in affiliates", {"FY2025": 118150, "FY2024": 127028, "FY2023": 181821, "FY2022": 188620, "FY2021": 174576}),
    ("DATA", "Intangible assets", {"FY2025": 2909, "FY2024": 156, "FY2023": 209, "FY2022": 12}),
    ("DATA", "Tangible fixed assets", {"FY2025": 31, "FY2024": 47, "FY2023": 65, "FY2022": 1, "FY2021": 1}),
    ("DATA", "Deferred tax asset", {"FY2024": 8926, "FY2023": 15014, "FY2022": 26967, "FY2021": 2150}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 65789, "FY2024": 58890, "FY2023": 58804, "FY2022": 44398, "FY2021": 27008}),
    ("DATA", "Other assets", {"FY2025": 29188, "FY2024": 65384, "FY2023": 33543, "FY2022": 22380, "FY2021": 32358}),
    ("TOTAL", "Total assets", {"FY2025": 7918773, "FY2024": 8007771, "FY2023": 8896652, "FY2022": 11702044, "FY2021": 11227068}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2025": 2240411, "FY2024": 2575276, "FY2023": 3297200, "FY2022": 4164947, "FY2021": 3152969}),
    ("DATA", "Customer accounts", {"FY2025": 4303354, "FY2024": 4316535, "FY2023": 4583519, "FY2022": 6631188, "FY2021": 7137353}),
    ("DATA", "Loan due to fellow group undertakings", {"FY2025": 118897}),
    ("DATA", "Other liabilities", {"FY2025": 31960, "FY2024": 20810, "FY2023": 30819, "FY2022": 28159, "FY2021": 50260}),
    ("DATA", "Deferred tax liabilities", {"FY2025": 288, "FY2024": 0, "FY2021": 0}),
    ("DATA", "Accruals and deferred income", {"FY2025": 7166, "FY2024": 6077, "FY2023": 26455, "FY2022": 9641, "FY2021": 4080}),
    ("DATA", "Provisions", {"FY2025": 1656, "FY2024": 4312, "FY2023": 4606, "FY2022": 4753, "FY2021": 4226}),
    ("TOTAL", "Total liabilities", {"FY2025": 6703732, "FY2024": 6923010, "FY2023": 7942599, "FY2022": 10838688, "FY2021": 10348888}),
    ("SECTION", "Capital and reserves", {}),
    ("DATA", "Called up share capital", {"FY2025": 519695, "FY2024": 519695, "FY2023": 519695, "FY2022": 519695, "FY2021": 519695}),
    ("DATA", "Fair value reserve", {"FY2025": 1758, "FY2024": -21742, "FY2023": -37213, "FY2022": -67625, "FY2021": -2488}),
    ("DATA", "Other reserves", {"FY2025": 7139, "FY2024": 7139, "FY2023": 7139, "FY2022": 7139, "FY2021": 7150}),
    ("DATA", "Profit and loss account", {"FY2025": 686449, "FY2024": 579669, "FY2023": 464432, "FY2022": 404147, "FY2021": 353823}),
    ("TOTAL", "Shareholder's funds", {"FY2025": 1215041, "FY2024": 1084761, "FY2023": 954053, "FY2022": 863356, "FY2021": 878180}),
    ("TOTAL", "Total liabilities and shareholder's funds", {"FY2025": 7918773, "FY2024": 8007771, "FY2023": 8896652, "FY2022": 11702044, "FY2021": 11227068}),
]

bw.add_balance_sheet_sheet(
    title="The Bank of New York Mellon (International) Limited — Balance Sheet",
    subtitle="Entity-level basis, £'000s.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + PRESENTATION_NOTE,
    first_col_width=64,
    source_height=440,
    unit_suffix=" (£'000s)",
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable and similar income", {"FY2025": 292194, "FY2024": 367509, "FY2023": 368769, "FY2022": 163522, "FY2021": 34976}),
    ("DATA", "Interest payable and similar charges", {"FY2025": -197224, "FY2024": -273351, "FY2023": -269549, "FY2022": -92414, "FY2021": -5231}),
    ("TOTAL", "Net interest income", {"FY2025": 94970, "FY2024": 94158, "FY2023": 99220, "FY2022": 71108, "FY2021": 29745}),
    ("DATA", "Fees and commissions receivable", {"FY2025": 145423, "FY2024": 147547, "FY2023": 139362, "FY2022": 133709, "FY2021": 140708}),
    ("DATA", "Net foreign exchange translation gain/(loss)", {"FY2025": 74, "FY2024": -315, "FY2023": -337, "FY2022": -1268, "FY2021": -468}),
    ("DATA", "Other operating income", {"FY2025": 8154, "FY2024": 6088, "FY2023": 10802, "FY2022": 14993, "FY2021": 11998}),
    ("TOTAL", "Non-interest income", {"FY2025": 153651, "FY2024": 153320, "FY2023": 149827, "FY2022": 147434, "FY2021": 152238}),
    ("TOTAL", "Total operating income (FY2024-25 basis, excl. investments-in-affiliates income)", {"FY2025": 248621, "FY2024": 247478}),
    ("TOTAL", "Total income (FY2021-23 basis, incl. investments-in-affiliates income)", {"FY2023": 266563, "FY2022": 240697, "FY2021": 210480}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Administration/administrative expenses", {"FY2025": -141192, "FY2024": -156924, "FY2023": -167758, "FY2022": -171390, "FY2021": -155502}),
    ("DATA", "Change in Expected Credit Loss (ECL) on financial assets", {"FY2025": 101, "FY2024": 451, "FY2023": -283, "FY2022": -124, "FY2021": 50}),
    ("TOTAL", "Total operating expenses", {"FY2025": -141091, "FY2024": -156473, "FY2023": -168041, "FY2022": -171514, "FY2021": -155452}),
    ("DATA", "Income from investments in affiliates", {"FY2025": 44810, "FY2024": 102898, "FY2023": 17516, "FY2022": 22155, "FY2021": 28497}),
    ("DATA", "Amounts written off investments in affiliates", {"FY2025": 0, "FY2024": -57148}),
    ("TOTAL", "Profit before taxation", {"FY2025": 152340, "FY2024": 136755, "FY2023": 98522, "FY2022": 69183, "FY2021": 55028}),
    ("DATA", "Taxation on profit", {"FY2025": -45560, "FY2024": -21518, "FY2023": -38209, "FY2022": -18870, "FY2021": -10102}),
    ("TOTAL", "Total profit for the financial year", {"FY2025": 106780, "FY2024": 115237, "FY2023": 60313, "FY2022": 50313, "FY2021": 44926}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Movement in financial assets measured at FVOCI", {"FY2025": 32634, "FY2024": 21463, "FY2023": 42230, "FY2022": -90166, "FY2021": -35721}),
    ("DATA", "Change in ECL on financial assets measured at FVOCI", {"FY2023": 15, "FY2022": -22, "FY2021": 1}),
    ("DATA", "Related tax", {"FY2025": -9134, "FY2024": -5992, "FY2023": -11833, "FY2022": 25051, "FY2021": 9867}),
    ("TOTAL", "Other comprehensive income/(loss), net of tax", {"FY2025": 23500, "FY2024": 15471, "FY2023": 30412, "FY2022": -65137, "FY2021": -25853}),
    ("TOTAL", "Total comprehensive income for the financial year", {"FY2025": 130280, "FY2024": 130708, "FY2023": 90725, "FY2022": -14824, "FY2021": 19073}),
]

bw.add_income_statement_sheet(
    title="The Bank of New York Mellon (International) Limited — Profit & Loss",
    subtitle="Entity-level basis, £'000s.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + PRESENTATION_NOTE,
    first_col_width=64,
    source_height=440,
    unit_suffix=" (£'000s)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity (chronological)
# ---------------------------------------------------------------
equity_changes_rows = [
    ("TOTAL", "At 1 January 2021", (519695, 23365, 7276, 308771, 859107)),
    ("DATA", "Movement in financial assets measured at FVOCI (FY2021)", (None, -35721, None, None, -35721)),
    ("DATA", "Change in ECL on financial assets measured at FVOCI (FY2021)", (None, 1, None, None, 1)),
    ("DATA", "Tax on other comprehensive income (FY2021)", (None, 9867, None, None, 9867)),
    ("DATA", "Profit for the financial year (FY2021)", (None, None, None, 44926, 44926)),
    ("TOTAL", "Total comprehensive income for the year (FY2021)", (None, -25853, None, 44926, 19073)),
    ("DATA", "Transfer between reserve accounts (FY2021)", (None, None, -126, 126, 0)),
    ("TOTAL", "At 31 December 2021", (519695, -2488, 7150, 353823, 878180)),
    ("DATA", "Profit for the financial year (FY2022)", (None, None, None, 50313, 50313)),
    ("DATA", "Movement in financial assets measured at FVOCI (FY2022)", (None, -90166, None, None, -90166)),
    ("DATA", "Change in ECL on financial assets measured at FVOCI (FY2022)", (None, -22, None, None, -22)),
    ("DATA", "Tax on other comprehensive income (FY2022)", (None, 25051, None, None, 25051)),
    ("TOTAL", "Total comprehensive income for the year (FY2022)", (None, -65137, None, 50313, -14824)),
    ("DATA", "Transfer between reserve accounts (FY2022)", (None, None, -11, 11, 0)),
    ("TOTAL", "At 31 December 2022", (519695, -67625, 7139, 404147, 863356)),
    ("DATA", "Profit for the financial year (FY2023)", (None, None, None, 60313, 60313)),
    ("DATA", "Movement in financial assets measured at FVOCI (FY2023)", (None, 42230, None, None, 42230)),
    ("DATA", "Change in ECL on financial assets measured at FVOCI (FY2023)", (None, 15, None, None, 15)),
    ("DATA", "Tax on other comprehensive income (FY2023)", (None, -11833, None, None, -11833)),
    ("TOTAL", "Total comprehensive income for the year (FY2023)", (None, 30412, None, 60313, 90725)),
    ("DATA", "Dividend in specie (FY2023)", (None, None, None, -28, -28)),
    ("TOTAL", "At 31 December 2023", (519695, -37213, 7139, 464432, 954053)),
    ("DATA", "Profit for the financial year (FY2024)", (None, None, None, 115237, 115237)),
    ("DATA", "Net movement in financial instruments measured at FVOCI (FY2024)", (None, 21463, None, None, 21463)),
    ("DATA", "Tax on other comprehensive income (FY2024)", (None, -5992, None, None, -5992)),
    ("TOTAL", "Total comprehensive income for the year (FY2024)", (None, 15471, None, 115237, 130708)),
    ("TOTAL", "At 31 December 2024", (519695, -21742, 7139, 579669, 1084761)),
    ("DATA", "Profit for the financial year (FY2025)", (None, None, None, 106780, 106780)),
    ("DATA", "Net movement in financial instruments measured at FVOCI (FY2025)", (None, 32634, None, None, 32634)),
    ("DATA", "Tax on other comprehensive income (FY2025)", (None, -9134, None, None, -9134)),
    ("TOTAL", "Total comprehensive income for the year (FY2025)", (None, 23500, None, 106780, 130280)),
    ("TOTAL", "At 31 December 2025", (519695, 1758, 7139, 686449, 1215041)),
]

bw.add_equity_changes_sheet(
    title="The Bank of New York Mellon (International) Limited — Statement of Changes in Equity",
    subtitle="Entity-level basis, £'000s. Chronological roll-forward, oldest to newest. No FX conversion (GBP functional currency throughout).",
    headers=["Called up share capital", "Fair value reserve", "Other reserves", "Profit and loss account", "Total equity"],
    rows=equity_changes_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + PRESENTATION_NOTE,
    first_col_width=54,
    source_height=440,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (exemption note in place of line items)
# ---------------------------------------------------------------
rows = [
    ("SECTION", "No Statement of Cash Flows is published by this entity in any year", {}),
    ("DATA", "See the note below for the FRS 101 exemption this entity relies on every year, and why this "
             "workbook is built as a Pillar-3-only variant.", {}),
]

bw.add_cash_flow_sheet(
    title="The Bank of New York Mellon (International) Limited — Cash Flow Statement",
    subtitle="Not applicable — this entity takes the FRS 101 cash-flow-statement disclosure exemption every year. See source note below.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=260,
    unit_suffix="",
)

# ---------------------------------------------------------------
# Asset Quality: this entity is a liability-driven custody bank, not a
# lender - "Loans and advances to customers" is a small, incidental line
# (£28m-£196m across the 5 years) next to a balance sheet dominated by
# central-bank cash, interbank placements and investment securities. The
# Company's own "Credit quality analysis" note covers ALL financial assets
# subject to IFRS 9 ECL (cash, loans to banks, loans to customers,
# investment securities) by internal credit grade and IFRS 9 stage - used
# here in full (mirroring the richer-than-customer-loans-alone treatment
# used for other placement-heavy banks in this project, e.g. Bank Sepah
# International in ST-013) rather than the narrower customer-loan book
# alone. Every year shown has 100% of exposure in Stage 1 (12-month ECL) -
# confirmed directly ("None of the loans and advances were past due or had
# a material ECL at the current or prior year-end", FY2025 statements) -
# no Stage 2/3 exposures in any of the 5 years.
# ---------------------------------------------------------------
AQ_GROSS = {"FY2025": 7702726, "FY2024": 7747362, "FY2023": 8607292, "FY2022": 11419812, "FY2021": 10991019}
AQ_ALLOWANCE = {"FY2025": -31, "FY2024": -34, "FY2023": -118, "FY2022": -183, "FY2021": -59}
AQ_NET = {y: AQ_GROSS[y] + AQ_ALLOWANCE[y] for y in YEARS}
AQ_STAGE3_RATIO = {y: "0.00%" for y in YEARS}
AQ_COVERAGE = {y: f"{-AQ_ALLOWANCE[y] / AQ_GROSS[y] * 100:.4f}%" for y in YEARS}

asset_quality_rows = [
    ("SECTION", "Gross exposure by IFRS 9 stage, across all ECL-bearing financial assets "
                "(cash at central banks, loans to banks, loans to customers, investment securities)", {}),
    ("DATA", "Stage 1 (12-month ECL) - gross exposure", AQ_GROSS),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired) - gross exposure", {y: 0 for y in YEARS}),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired) - gross exposure", {y: 0 for y in YEARS}),
    ("TOTAL", "Total gross exposure", AQ_GROSS),
    ("SECTION", "Expected credit loss (ECL) allowance", {}),
    ("DATA", "Loss allowance (all Stage 1; includes the FVOCI investment-securities ECL memo item)", AQ_ALLOWANCE),
    ("TOTAL", "Net carrying amount", AQ_NET),
    ("SECTION", "Ratios", {}),
    ("DATA", "Stage 3 exposure ratio (Stage 3 / total gross exposure)", AQ_STAGE3_RATIO),
    ("DATA", "Overall coverage ratio (loss allowance / total gross exposure)", AQ_COVERAGE),
]

bw.add_asset_quality_sheet(
    title="The Bank of New York Mellon (International) Limited — Asset Quality / Credit Risk Disclosures",
    subtitle="Credit quality analysis across all ECL-bearing financial assets, £'000s. Entity-level basis.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - the Company's own 'Credit quality analysis' note (Financial risk management, Note 2.1):\n"
        f"FY2025/FY2024: Financial Statements, year ended 31 December 2025, p.40 - {FS2025_URL}\n"
        f"FY2023/FY2022: Financial Statements, year ended 31 December 2023, p.54 - {FS2023_URL}\n"
        f"FY2021: Financial Statements, year ended 31 December 2021, p.50 (Companies House, scanned/image-only, "
        f"visually transcribed) - {FS2021_URL}\n\n"
        "Note: 100% of exposure sits in Stage 1 (12-month ECL) every year - no Stage 2 or Stage 3 exposures at all "
        "in any of the 5 years, and the entity's own note states none of the loans and advances were past due or "
        "had a material ECL at the current or prior year-end. This is a structural feature of a liability-driven "
        "custody bank (counterparties are almost entirely investment-grade banks/central banks/sovereign and "
        "supranational securities), not a data gap.\n\n" + ENTITY_NOTE
    ),
    first_col_width=76,
    source_height=340,
    unit_suffix=" (£'000s)",
)

# ---------------------------------------------------------------
# RWA Breakdown (UK OV1 / EU OV1 template)
# ---------------------------------------------------------------
RWA_SOURCES = (
    "Sources - The Bank of New York Mellon (International) Limited Pillar 3 Disclosures, Table 4 'UK OV1 - "
    "Overview of risk-weighted exposure amounts' (Table 7 'EU OV1 - Overview of RWAs' for FY2021, the older CRR "
    "template) - each year's own report, not a later restated comparative (see the CET1 Ratio sheet's note on the "
    "FY2025 report's restated FY2024 comparative):\n"
    f"FY2025: Pillar 3 Disclosure, December 31, 2025, p.10 - {P3_2025_URL}\n"
    f"FY2024: Pillar 3 Disclosure, December 31, 2024, p.10 - {P3_2024_URL}\n"
    f"FY2023: Pillar 3 Disclosure, December 31, 2023, p.11 - {P3_2023_URL}\n"
    f"FY2022: Pillar 3 Disclosure, December 31, 2022, p.14 - {P3_2022_URL}\n"
    f"FY2021: Pillar 3 Disclosure, December 31, 2021, p.25 - {P3_2021_URL}\n\n"
    "Note: FY2021's own report uses the older EU OV1 template, which separately discloses Credit Valuation "
    "Adjustment (CVA) as its own risk type; combined here into the 'Counterparty credit risk' row (£2m CCR + £2m "
    "CVA = £4m) to match the UK OV1 template's grouping used FY2022 onward - the combined figure ties to that "
    "year's own Total RWA (£838m). FY2021's securitisation exposure is a genuine disclosed zero ('the Company's "
    "securitisation portfolio was immaterial'), not a gap.\n\n" + ENTITY_NOTE
)

rwa_breakdown_rows = [
    ("SECTION", "RWA by risk category (£m)", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 435, "FY2024": 519, "FY2023": 539, "FY2022": 569, "FY2021": 466}),
    ("DATA", "Counterparty credit risk (incl. CVA where separately disclosed)", {"FY2025": 1, "FY2024": 1, "FY2023": 0, "FY2022": 0, "FY2021": 4}),
    ("DATA", "Securitisation exposures", {"FY2025": 7, "FY2024": 9, "FY2023": 9, "FY2022": 3, "FY2021": 0}),
    ("DATA", "Market risk (position, FX and commodities)", {"FY2025": 12, "FY2024": 12, "FY2023": 14, "FY2022": 12, "FY2021": 16}),
    ("DATA", "Operational risk", {"FY2025": 592, "FY2024": 577, "FY2023": 489, "FY2022": 415, "FY2021": 352}),
    ("TOTAL", "Total RWAs", {"FY2025": 1047, "FY2024": 1118, "FY2023": 1051, "FY2022": 999, "FY2021": 838}),
]

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=130)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 1091, "FY2024": 955, "FY2023": 833, "FY2022": 733, "FY2021": 761})],
    p3_sources(KM1_PAGE),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "104.22%", "FY2024": "85.41%", "FY2023": "79.26%", "FY2022": "73.35%", "FY2021": "90.8%"})],
    p3_sources(KM1_PAGE),
    note="The FY2025 Pillar 3 Disclosure's FY2024 comparative column restates RWA (1,118 -> 1,091) and this ratio "
         "(85.41% -> 87.54%) versus the FY2024 report's own originally-reported figures - the FY2024 column above "
         "uses that year's own report as originally published, not the later restated comparative (consistent with "
         "this project's convention of preserving each year's own as-reported figures).",
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 1091, "FY2024": 955, "FY2023": 833, "FY2022": 733, "FY2021": 761})],
    p3_sources(KM1_PAGE),
    note="Tier 1 = CET1 every year (no AT1 instruments in issue).",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "104.22%", "FY2024": "85.41%", "FY2023": "79.26%", "FY2022": "73.35%", "FY2021": "90.8%"})],
    p3_sources(KM1_PAGE),
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 1091, "FY2024": 955, "FY2023": 833, "FY2022": 733, "FY2021": 761})],
    p3_sources(KM1_PAGE),
    note="Total capital = CET1 = Tier 1 every year (no AT1 or Tier 2 instruments in issue).",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "104.22%", "FY2024": "85.41%", "FY2023": "79.26%", "FY2022": "73.35%", "FY2021": "90.8%"})],
    p3_sources(KM1_PAGE),
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted exposure amount", {"FY2025": 1047, "FY2024": 1118, "FY2023": 1051, "FY2022": 999, "FY2021": 838})],
    p3_sources(KM1_PAGE),
    note="FY2024 shown as originally reported (1,118); the FY2025 Pillar 3 Disclosure's comparative column restates "
         "this to 1,091 - see the CET1 Ratio sheet note.",
)

bw.add_rwa_breakdown_sheet(
    title="The Bank of New York Mellon (International) Limited — RWA Breakdown",
    subtitle="Entity-level basis, £m.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_SOURCES,
    first_col_width=64,
    source_height=280,
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total exposure measure excluding claims on central banks", {"FY2025": 6449, "FY2024": 6276, "FY2023": 5888, "FY2022": 7602}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "16.92%", "FY2024": "15.22%", "FY2023": "14.15%", "FY2022": "9.64%"}),
        ("Leverage ratio (as reported, basis not specified) (%)", {"FY2021": "6.1%"}),
    ],
    p3_sources(KM1_PAGE),
    note="The FY2021 Pillar 3 Disclosure's 'Key metrics' page discloses only a single Leverage ratio figure without "
         "specifying an excluding/including-central-bank-claims split (that split, and the exposure-measure £m "
         "figure, first appear in the FY2022 report's KM1 template) - shown on its own row rather than assumed "
         "comparable to the 'excluding' basis used FY2022 onward. The Company is not subject to a binding leverage "
         "ratio requirement (does not meet the LREQ firm thresholds under the PRA Rulebook).",
)

metric(
    "LCR", "£m / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value (average)", {"FY2025": 5184, "FY2024": 6021, "FY2023": 6887, "FY2022": 8876}),
        ("Total net cash outflows, adjusted value", {"FY2025": 1669, "FY2024": 2532, "FY2023": 3305, "FY2022": 4801}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "317.37%", "FY2024": "240.33%", "FY2023": "211.60%", "FY2022": "185.66%", "FY2021": "173%"}),
    ],
    p3_sources(KM1_PAGE),
    note="LCR is presented on a 12-month average basis (4-quarter average for FY2022, per that report's own note). "
         "FY2021's Pillar 3 report discloses only the headline ratio (173%, Solo basis) on its 'Key metrics' chart "
         "page, with no HQLA/outflow/inflow £m breakdown available that year and no FY2021 comparative shown in the "
         "FY2022 report (which explicitly states comparatives were not provided for LCR/NSFR due to a change in "
         "reporting instructions) - left blank rather than guessed.",
)

metric(
    "NSFR", "£m / %",
    [
        ("Total available stable funding", {"FY2025": 2561, "FY2024": 2474, "FY2023": 2386, "FY2022": 3210}),
        ("Total required stable funding", {"FY2025": 672, "FY2024": 675, "FY2023": 650, "FY2022": 680}),
        ("NSFR ratio (%)", {"FY2025": "381.21%", "FY2024": "366.64%", "FY2023": "368.06%", "FY2022": "472.37%", "FY2021": "446%"}),
    ],
    p3_sources(KM1_PAGE),
    note="NSFR is presented on a 4-quarter average basis. FY2021's Pillar 3 report discloses only the headline "
         "ratio (446%, Solo basis) with no £m breakdown, and no FY2021 comparative appears in the FY2022 report "
         "(same reporting-instruction change noted on the LCR sheet). The FY2025 Pillar 3 Disclosure's FY2024 "
         "comparative column also restates NSFR (ASF 2,474->2,481, RSF 675->664, ratio 366.64%->373.99%) versus "
         "the FY2024 report's own originally-reported figures - the FY2024 column above uses that year's own report "
         "as originally published, consistent with this project's convention.",
)

metric(
    "MREL Ratio", "£m / %",
    [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})],
    p3_sources(KM1_PAGE),
    note="No MREL figure (numeric or qualitative) appears anywhere in any of the 5 Pillar 3 Disclosures or the "
         "available Financial Statements for this entity - no reason is stated.",
)

# ---------------------------------------------------------------
# Overview sheet (Pillar-3-only: no cash-flow chart)
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 7918773, "FY2024": 8007771, "FY2023": 8896652, "FY2022": 11702044, "FY2021": 11227068}),
        ("Loans and advances to customers", {"FY2025": 28495, "FY2024": 173578, "FY2023": 108153, "FY2022": 138345, "FY2021": 104419}),
        ("Customer accounts", {"FY2025": 4303354, "FY2024": 4316535, "FY2023": 4583519, "FY2022": 6631188, "FY2021": 7137353}),
        ("Shareholder's funds", {"FY2025": 1215041, "FY2024": 1084761, "FY2023": 954053, "FY2022": 863356, "FY2021": 878180}),
    ],
    balance_sheet_unit="£'000s",
    income_statement_totals=[
        ("Non-interest income", {"FY2025": 153651, "FY2024": 153320, "FY2023": 149827, "FY2022": 147434, "FY2021": 152238}),
        ("Total operating expenses", {"FY2025": -141091, "FY2024": -156473, "FY2023": -168041, "FY2022": -171514, "FY2021": -155452}),
        ("Total profit for the financial year", {"FY2025": 106780, "FY2024": 115237, "FY2023": 60313, "FY2022": 50313, "FY2021": 44926}),
    ],
    income_statement_unit="£'000s",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 1084761, "FY2024": 954053, "FY2023": 863356, "FY2022": 878180, "FY2021": 859107}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": 130280, "FY2024": 130708, "FY2023": 90725, "FY2022": -14824, "FY2021": 19073}),
        ("Other movements, net", {"FY2025": 0, "FY2024": 0, "FY2023": -28, "FY2022": 0, "FY2021": 0}),
        ("Closing equity", {"FY2025": 1215041, "FY2024": 1084761, "FY2023": 954053, "FY2022": 863356, "FY2021": 878180}),
    ],
    equity_changes_unit="£'000s",
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("CET1 Ratio", {"FY2025": "104.22%", "FY2024": "85.41%", "FY2023": "79.26%", "FY2022": "73.35%", "FY2021": "90.8%"}),
        ("Tier 1 Ratio", {"FY2025": "104.22%", "FY2024": "85.41%", "FY2023": "79.26%", "FY2022": "73.35%", "FY2021": "90.8%"}),
        ("Total Capital Ratio", {"FY2025": "104.22%", "FY2024": "85.41%", "FY2023": "79.26%", "FY2022": "73.35%", "FY2021": "90.8%"}),
        ("Leverage Ratio (excl. central bank claims)", {"FY2025": "16.92%", "FY2024": "15.22%", "FY2023": "14.15%", "FY2022": "9.64%"}),
        ("LCR", {"FY2025": "317.37%", "FY2024": "240.33%", "FY2023": "211.60%", "FY2022": "185.66%", "FY2021": "173%"}),
        ("NSFR", {"FY2025": "381.21%", "FY2024": "366.64%", "FY2023": "368.06%", "FY2022": "472.37%", "FY2021": "446%"}),
    ],
    note="No cash flow summary or chart is shown here: The Bank of New York Mellon (International) Limited takes "
         "the FRS 101 cash-flow-statement exemption every year (see the Cash Flow Statement sheet). Balance Sheet, "
         "Profit & Loss, Statement of Changes in Equity and Pillar 3 Key Metrics are all fully populated below. See "
         "each sheet's own source citation for the underlying document/page.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BNY MELLON INTERNATIONAL FINANCIALS.xlsx")
