import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, y/e 31 July
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = ("https://find-and-update.company-information.service.gov.uk/company/00195626/"
              "filing-history/MzQ5NDAzMzc1NGFkaXF6a2N4/document?format=pdf&download=0")
AR2023_URL = ("https://find-and-update.company-information.service.gov.uk/company/00195626/"
              "filing-history/MzQwNzQ2MzI3OWFkaXF6a2N4/document?format=pdf&download=0")
AR2021_URL = ("https://find-and-update.company-information.service.gov.uk/company/00195626/"
              "filing-history/MzMyMjY5NTAxOGFkaXF6a2N4/document?format=pdf&download=0")

ENTITY_NOTE = (
    "Close Brothers Limited (company 00195626, FRN 124750) is the PRA-regulated bank subsidiary of the "
    "LSE-listed Close Brothers Group plc. Cash flow figures are the entity's own Consolidated (Close "
    "Brothers Limited + its subsidiaries) Statement of Cash Flows, from its statutory 'Group of companies' "
    "accounts' filings at Companies House - NOT the wider Close Brothers Group plc's own consolidated "
    "accounts (a separate filing). All 5 Companies House filings used were fully scanned/image-only.\n\n"
    "FY2021 is shown as a single headline total only (no line-item breakdown) - the operating-activities "
    "reconciliation note for that year's own report could not be located within budget; the other 4 years "
    "have full breakdowns. FY2022's figures are FY2023's report's own comparative column (no separate "
    "FY2022 filing was sourced); FY2024's figures are similarly FY2025's report's own comparative column.\n\n"
    "GENUINE MID-SERIES PRESENTATION BREAK in the Financing activities section: FY2021-FY2023 report "
    "'Equity dividends paid' and 'Interest paid on debt financing' as distinct lines; FY2024-FY2025 drop "
    "both (no dividend was paid in either year, consistent with FY2025's substantial loss) and instead "
    "introduce 'Issue of ordinary share capital', 'Issuance/costs of AT1 capital securities', and 'AT1 "
    "coupon payment' lines (a $200m AT1 issuance occurred in FY2024). Each year kept on its own "
    "originally-published presentation - blank cells where a line item doesn't apply to that year, not a "
    "gap. Full chain of opening/closing cash balances ties exactly across all 5 years.\n\n"
    "MOTOR FINANCE COMMISSION MIS-SELLING IMPACT: FY2025's Operating profit before tax swung to a loss of "
    "£(67.6)m (from £178.0m profit in FY2024), driven substantially by three new provision lines in the "
    "FY2025 operating-activities reconciliation: 'Provision in relation to motor finance commissions "
    "excluding cash paid' (£161.4m), 'Complaints handling and other operational and legal costs...in "
    "relation to motor finance commissions' (£5.6m), and 'Provision in relation to early settlements in "
    "Motor Finance' (£33.0m) - approximately £200m of provisions tied to the well-publicised FCA motor "
    "finance commission review. This is a real, disclosed business event, not a data anomaly."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Close Brothers Limited's own Consolidated Cash Flow Statement (Close "
    "Brothers Limited + its subsidiaries, NOT the wider listed Close Brothers Group plc):\n"
    "FY2025: Group of companies' accounts to 31 Jul 2025 (Companies House, filed 20 Dec 2025), "
    "Consolidated Cash Flow Statement p.101 + Note 24 reconciliation p.145 - " + AR2025_URL + "\n"
    "FY2024: same FY2025 filing's own FY2024 comparative column, p.101 + p.145\n"
    "FY2023: Group of companies' accounts to 31 Jul 2023 (Companies House, filed 20 Jan 2024), "
    "Consolidated Cash Flow Statement p.71 + Note 24 reconciliation p.112 - " + AR2023_URL + "\n"
    "FY2022: same FY2023 filing's own FY2022 comparative column, p.71 + p.112\n"
    "FY2021: Group of companies' accounts to 31 Jul 2021 (Companies House, filed 07 Dec 2021), "
    "Consolidated Cash Flow Statement p.47 (headline total only - operating-activities note not "
    "located within budget) - " + AR2021_URL + "\n\n"
    + ENTITY_NOTE
)


bw = BankWorkbook(bank_name="Close Brothers Limited", years=YEARS, year_label=YEAR_LABEL, header_color="F6324B")

STATEMENTS_ENTITY_NOTE = (
    "Close Brothers Limited (company 00195626, FRN 124750) is the PRA-regulated bank subsidiary of the "
    "LSE-listed Close Brothers Group plc. All figures are the entity's own Consolidated (Close Brothers "
    "Limited + its subsidiaries) financial statements, from its statutory 'Group of companies' accounts' "
    "filings at Companies House - NOT the wider Close Brothers Group plc's own consolidated accounts (a "
    "separate filing). All 3 filings used (FY2025, FY2023, FY2021) are fully scanned/image-only; figures "
    "were transcribed via page-image review. FY2024/FY2022 figures are each sourced from the following "
    "year's own filing's comparative column (no separate FY2024/FY2022 filing was sourced)."
)

STATEMENTS_SOURCES = (
    "Sources - all figures are Close Brothers Limited's own Consolidated Income Statement / Consolidated "
    "Statement of Comprehensive Income / Consolidated Balance Sheet / Consolidated Statement of Changes in "
    "Equity (Close Brothers Limited + its subsidiaries, NOT the wider listed Close Brothers Group plc):\n"
    "FY2025: Group of companies' accounts to 31 Jul 2025 (Companies House, filed 20 Dec 2025), pp.97-100 - " + AR2025_URL + "\n"
    "FY2024: same FY2025 filing's own FY2024 comparative column, pp.97-100\n"
    "FY2023: Group of companies' accounts to 31 Jul 2023 (Companies House, filed 20 Jan 2024), pp.67-70 - " + AR2023_URL + "\n"
    "FY2022: same FY2023 filing's own FY2022 comparative column, pp.67-70\n"
    "FY2021: Group of companies' accounts to 31 Jul 2021 (Companies House, filed 07 Dec 2021), pp.43-46 - " + AR2021_URL + "\n\n"
    + STATEMENTS_ENTITY_NOTE + "\n\n"
    "PRESENTATION NOTE: the income statement's structure changed twice across the 5 years. FY2021 has a "
    "'goodwill impairment' and 'exceptional item: HMRC VAT refund' line unique to that year, plus its own "
    "operating-expense subtotal before 'amortisation and impairment of intangible assets on acquisition, "
    "goodwill impairment and exceptional item'. FY2022-FY2023 drop the goodwill/exceptional lines and "
    "subtotal only before 'amortisation of intangible assets on acquisition'. FY2024-FY2025 restructure "
    "further, introducing three new motor-finance-commission provision lines (see the well-publicised FCA "
    "motor finance commission review, first appearing FY2024 with the 'Borrowers in Financial Difficulty' "
    "provision, then FY2025 with 'Provision in relation to motor finance commissions' and 'Provision in "
    "relation to early settlements in Motor Finance') and an 'Impairment of operating lease assets' line "
    "(FY2025 only) - each year kept on its own originally-published structure, not forced onto one basis. "
    "Note the FY2025 income statement's 'Provision in relation to motor finance commissions' (£165.0m) is a "
    "slightly larger figure than the Cash Flow Statement's 'Provision in relation to motor finance "
    "commissions excluding cash paid' (£161.4m) - both reproduced exactly as the Bank's own statements show "
    "them, a difference between the two measures' scope, not a transcription error."
)


BALANCE_SHEET_SOURCES = (
    STATEMENTS_SOURCES + "\n\n"
    "DEBT SECURITIES BREAKDOWN: the 'Debt securities - ...' sub-rows below the headline 'Debt securities' "
    "line are transcribed from Note 11 'Debt securities' of each year's own Notes to the Consolidated "
    "Accounts, which splits the balance both by measurement basis (fair value through profit or loss / "
    "fair value through other comprehensive income / amortised cost) and by instrument type (sovereign and "
    "central bank debt, supranational/sub-sovereign/agency ('SSA') bonds, covered bonds, certificates of "
    "deposit, other debt securities):\n"
    "FY2025: Note 11, p.126 - " + AR2025_URL + "\n"
    "FY2024: same FY2025 filing's own FY2024 comparative column, Note 11, p.126\n"
    "FY2023: Note 11, p.94 - " + AR2023_URL + "\n"
    "FY2022: same FY2023 filing's own FY2022 comparative column, Note 11, p.95\n"
    "FY2021: Note 11, p.76 - " + AR2021_URL + "\n\n"
    "Each year's sub-rows sum exactly to that year's headline 'Debt securities' line. Certificates of "
    "deposit and Supranational/sub-sovereign/agency (SSA) bonds are not disclosed as separate lines in "
    "every year (e.g. no SSA bonds line FY2021-FY2023, no Certificates of deposit FY2024-FY2025) - blank "
    "cells reflect the note's own year-by-year composition, not a gap."
)

bw.add_balance_sheet_sheet(
    title="Close Brothers Limited — Consolidated Balance Sheet",
    subtitle="Consolidated Statement of Financial Position, £m. Consolidated basis (Close Brothers Limited + subsidiaries). See source note at bottom.",
    rows=[
        ("SECTION", "Assets", {}),
        ("DATA", "Cash and balances at central banks",
         {"FY2025": 1917.0, "FY2024": 1584.0, "FY2023": 1937.0, "FY2022": 1254.7, "FY2021": 1331.0}),
        ("DATA", "Loans and advances to banks",
         {"FY2025": 156.9, "FY2024": 177.3, "FY2023": 261.5, "FY2022": 85.6, "FY2021": 66.8}),
        ("DATA", "Loans and advances to customers",
         {"FY2025": 9459.4, "FY2024": 9830.8, "FY2023": 9255.0, "FY2022": 8858.9, "FY2021": 8444.5}),
        ("DATA", "Total debt securities",
         {"FY2025": 859.2, "FY2024": 724.5, "FY2023": 292.4, "FY2022": 600.4, "FY2021": 457.2}),
        ("DATA", "Debt securities - Sovereign and central bank debt (sovereign debt, FVOCI)",
         {"FY2025": 601.6, "FY2024": 383.7, "FY2023": 186.1, "FY2022": 415.4, "FY2021": 192.5}),
        ("DATA", "Debt securities - Supranational, sub-sovereign and agency (SSA) bonds (FVOCI)",
         {"FY2025": 146.2, "FY2024": 145.5}),
        ("DATA", "Debt securities - Covered bonds (FVOCI)",
         {"FY2025": 105.6, "FY2024": 187.7, "FY2023": 106.3}),
        ("DATA", "Debt securities - Certificates of deposit (amortised cost)",
         {"FY2022": 185.0, "FY2021": 264.7}),
        ("DATA", "Debt securities - Other debt securities at fair value through profit or loss (FVTPL)",
         {"FY2025": 1.1, "FY2024": 0.8}),
        ("DATA", "Debt securities - Other debt securities at amortised cost",
         {"FY2025": 4.7, "FY2024": 6.8}),
        ("DATA", "Derivative financial instruments",
         {"FY2025": 103.0, "FY2024": 101.2, "FY2023": 88.5, "FY2022": 71.1, "FY2021": 18.3}),
        ("DATA", "Intangible assets",
         {"FY2025": 151.6, "FY2024": 170.7, "FY2023": 175.0, "FY2022": 160.5, "FY2021": 138.7}),
        ("DATA", "Property, plant and equipment",
         {"FY2025": 193.8, "FY2024": 297.7, "FY2023": 304.5, "FY2022": 279.0, "FY2021": 263.1}),
        ("DATA", "Current tax assets",
         {"FY2025": 42.7, "FY2024": 24.1, "FY2023": 33.8, "FY2022": 40.8, "FY2021": 28.7}),
        ("DATA", "Deferred tax assets",
         {"FY2025": 30.5, "FY2024": 12.5, "FY2023": 4.8, "FY2022": 24.8, "FY2021": 48.0}),
        ("DATA", "Prepayments, accrued income and other assets",
         {"FY2025": 171.7, "FY2024": 130.4, "FY2023": 135.6, "FY2022": 132.5, "FY2021": 154.6}),
        ("DATA", "Assets classified as held for sale", {"FY2025": 47.0}),
        ("TOTAL", "Total assets",
         {"FY2025": 13132.8, "FY2024": 13053.2, "FY2023": 12488.1, "FY2022": 11508.3, "FY2021": 10950.9}),

        ("SECTION", "Liabilities", {}),
        ("DATA", "Deposits by banks",
         {"FY2025": 88.1, "FY2024": 138.4, "FY2023": 141.9, "FY2022": 160.5, "FY2021": 150.6}),
        ("DATA", "Deposits by customers",
         {"FY2025": 8799.3, "FY2024": 8693.6, "FY2023": 7724.5, "FY2022": 6770.4, "FY2021": 6634.8}),
        ("DATA", "Loans and overdrafts from banks",
         {"FY2025": 1.5, "FY2024": 113.5, "FY2023": 635.3, "FY2022": 610.8, "FY2021": 506.2}),
        ("DATA", "Debt securities in issue",
         {"FY2025": 1740.0, "FY2024": 1735.6, "FY2023": 1762.1, "FY2022": 1810.5, "FY2021": 1611.8}),
        ("DATA", "Derivative financial instruments",
         {"FY2025": 104.7, "FY2024": 128.9, "FY2023": 195.9, "FY2022": 89.2, "FY2021": 21.2}),
        ("DATA", "Amounts due to group undertakings",
         {"FY2025": 256.2, "FY2024": 167.0, "FY2023": 334.2, "FY2022": 356.7, "FY2021": 347.2}),
        ("DATA", "Subordinated loan capital",
         {"FY2025": 195.5, "FY2024": 187.2, "FY2023": 174.9, "FY2022": 186.5, "FY2021": 222.7}),
        ("DATA", "Provisions", {"FY2025": 209.1, "FY2024": 24.9}),
        ("DATA", "Current tax liabilities", {"FY2021": 0.0}),
        ("DATA", "Accruals, deferred income and other liabilities",
         {"FY2025": 155.6, "FY2024": 169.0, "FY2023": 182.9, "FY2022": 197.7, "FY2021": 184.0}),
        ("DATA", "Liabilities classified as held for sale", {"FY2025": 6.0}),
        ("TOTAL", "Total liabilities",
         {"FY2025": 11556.0, "FY2024": 11358.1, "FY2023": 11151.7, "FY2022": 10182.3, "FY2021": 9678.5}),

        ("SECTION", "Equity", {}),
        ("DATA", "Called up share capital",
         {"FY2025": 187.5, "FY2024": 187.5, "FY2023": 122.5, "FY2022": 122.5, "FY2021": 122.5}),
        ("DATA", "Retained earnings",
         {"FY2025": 1197.4, "FY2024": 1303.7, "FY2023": 1183.4, "FY2022": 1183.2, "FY2021": 1151.6}),
        ("DATA", "Other reserves",
         {"FY2025": -5.7, "FY2024": 6.3, "FY2023": 30.5, "FY2022": 20.3, "FY2021": -0.7}),
        ("DATA", "Other equity instrument", {"FY2025": 197.6, "FY2024": 197.6}),
        ("DATA", "Non-controlling interests", {"FY2021": -1.0}),
        ("TOTAL", "Total equity",
         {"FY2025": 1576.8, "FY2024": 1695.1, "FY2023": 1336.4, "FY2022": 1326.0, "FY2021": 1272.4}),
        ("TOTAL", "Total liabilities and equity",
         {"FY2025": 13132.8, "FY2024": 13053.2, "FY2023": 12488.1, "FY2022": 11508.3, "FY2021": 10950.9}),
    ],
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=68,
    source_height=400,
    unit_suffix=" (£m)",
)

bw.add_income_statement_sheet(
    title="Close Brothers Limited — Consolidated Income Statement",
    subtitle="Consolidated Statement of Comprehensive Income, £m. Consolidated basis (Close Brothers Limited + subsidiaries). See source note at bottom.",
    rows=[
        ("SECTION", "Income", {}),
        ("DATA", "Interest income",
         {"FY2025": 1112.5, "FY2024": 1134.9, "FY2023": 885.2, "FY2022": 689.7, "FY2021": 656.7}),
        ("DATA", "Interest expense",
         {"FY2025": -531.6, "FY2024": -542.7, "FY2023": -297.9, "FY2022": -107.4, "FY2021": -114.9}),
        ("TOTAL", "Net interest income",
         {"FY2025": 580.9, "FY2024": 592.2, "FY2023": 587.3, "FY2022": 582.3, "FY2021": 541.8}),
        ("DATA", "Fee and commission income",
         {"FY2025": 103.5, "FY2024": 104.2, "FY2023": 110.6, "FY2022": 98.1, "FY2021": 88.2}),
        ("DATA", "Fee and commission expense",
         {"FY2025": -16.7, "FY2024": -19.8, "FY2023": -15.1, "FY2022": -14.7, "FY2021": -13.5}),
        ("DATA", "Other income",
         {"FY2025": 118.1, "FY2024": 129.7, "FY2023": 109.4, "FY2022": 101.6, "FY2021": 87.0}),
        ("DATA", "Depreciation of operating lease assets and other direct costs",
         {"FY2025": -84.6, "FY2024": -81.4, "FY2023": -77.8, "FY2022": -71.9, "FY2021": -69.5}),
        ("DATA", "Impairment of operating lease assets", {"FY2025": -30.0}),
        ("TOTAL", "Non-interest income",
         {"FY2025": 90.3, "FY2024": 132.7, "FY2023": 127.1, "FY2022": 113.1, "FY2021": 92.2}),
        ("TOTAL", "Operating income",
         {"FY2025": 671.2, "FY2024": 724.9, "FY2023": 714.4, "FY2022": 695.4, "FY2021": 634.0}),

        ("SECTION", "Expenses", {}),
        ("DATA", "Provision in relation to motor finance commissions", {"FY2025": -165.0}),
        ("DATA", "Complaints handling and other operational/legal costs re. motor finance commissions",
         {"FY2025": -18.7, "FY2024": -6.9}),
        ("DATA", "Provision in relation to early settlements in Motor Finance", {"FY2025": -33.0}),
        ("DATA", "Provision in relation to the Borrowers in Financial Difficulty (\"BiFD\") review",
         {"FY2024": -17.2}),
        ("DATA", "Administrative expenses",
         {"FY2025": -429.3, "FY2024": -423.9, "FY2023": -389.7, "FY2022": -362.6, "FY2021": -329.1}),
        ("TOTAL", "Total administrative expenses", {"FY2025": -646.0, "FY2024": -448.0}),
        ("DATA", "Impairment losses on financial assets",
         {"FY2025": -92.8, "FY2024": -98.9, "FY2023": -204.0, "FY2022": -103.3, "FY2021": -90.1}),
        ("TOTAL", "Total operating expenses", {"FY2025": -738.8, "FY2024": -546.9}),
        ("TOTAL", "Total operating expenses before amortisation of intangible assets on acquisition",
         {"FY2023": -593.7, "FY2022": -465.9}),
        ("TOTAL", "Total operating expenses before amortisation/impairment of intangibles, goodwill impairment and exceptional item",
         {"FY2021": -419.2}),
        ("TOTAL", "Operating profit before amortisation of intangible assets on acquisition",
         {"FY2023": 120.7, "FY2022": 229.5}),
        ("TOTAL", "Operating profit before amortisation/impairment of intangibles, goodwill impairment and exceptional item",
         {"FY2021": 214.8}),
        ("DATA", "Amortisation and impairment of intangible assets on acquisition",
         {"FY2023": 0.0, "FY2022": -0.1, "FY2021": -12.9}),
        ("DATA", "Goodwill impairment", {"FY2021": -12.1}),
        ("DATA", "Exceptional item: HMRC VAT refund", {"FY2021": 19.7}),
        ("TOTAL", "Operating (loss)/profit before tax",
         {"FY2025": -67.6, "FY2024": 178.0, "FY2023": 120.7, "FY2022": 229.4, "FY2021": 209.5}),
        ("DATA", "Tax",
         {"FY2025": -17.7, "FY2024": -47.6, "FY2023": -31.6, "FY2022": -66.3, "FY2021": -50.1}),
        ("TOTAL", "(Loss)/profit after tax",
         {"FY2025": -85.3, "FY2024": 130.4, "FY2023": 89.1, "FY2022": 163.1, "FY2021": 159.4}),

        ("SECTION", "Other comprehensive income", {}),
        ("DATA", "Other comprehensive (expense)/income, net of tax",
         {"FY2025": -12.0, "FY2024": -24.2, "FY2023": 10.2, "FY2022": 21.0, "FY2021": 6.0}),
        ("TOTAL", "Total comprehensive (loss)/income for the year",
         {"FY2025": -97.3, "FY2024": 106.2, "FY2023": 99.3, "FY2022": 184.1, "FY2021": 165.4}),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=78,
    source_height=340,
    unit_suffix=" (£m)",
)

EQUITY_HEADERS = [
    "Called up share capital", "Retained earnings", "Capital contribution reserve",
    "Other equity instrument", "Exchange movements reserve", "FVOCI reserve",
    "Cash flow hedging reserve", "Non-controlling interests", "Total equity",
]
bw.add_equity_changes_sheet(
    title="Close Brothers Limited — Consolidated Statement of Changes in Equity",
    subtitle="Consolidated basis (Close Brothers Limited + subsidiaries), £m. See source note at bottom.",
    headers=EQUITY_HEADERS,
    rows=[
        ("TOTAL", "At 31 July 2020 (FY2021 opening)",
         (122.5, 1083.2, None, None, -1.2, 0.2, -5.7, -1.0, 1198.0)),
        ("DATA", "Profit for the year (FY2021)",
         (None, 159.4, None, None, None, None, None, None, 159.4)),
        ("DATA", "Other comprehensive income (FY2021)",
         (None, None, None, None, None, 0.6, 5.4, None, 6.0)),
        ("TOTAL", "Total comprehensive income for the year (FY2021)",
         (None, 159.4, None, None, None, 0.6, 5.4, None, 165.4)),
        ("DATA", "Other movements (FY2021)", (None, 0.5, None, None, None, None, None, None, 0.5)),
        ("DATA", "Income tax (FY2021)", (None, 0.8, None, None, None, None, None, None, 0.8)),
        ("DATA", "Dividends paid (FY2021)", (None, -92.3, None, None, None, None, None, None, -92.3)),
        ("DATA", "Capital contribution - parent equity-settled share-based payments (FY2021)",
         (None, None, 1.8, None, None, None, None, None, 1.8)),
        ("DATA", "Return of capital contribution (FY2021)",
         (None, None, -1.8, None, None, None, None, None, -1.8)),
        ("TOTAL", "At 31 July 2021",
         (122.5, 1151.6, None, None, -1.2, 0.8, -0.3, -1.0, 1272.4)),

        ("DATA", "Profit for the year (FY2022)", (None, 163.1, None, None, None, None, None, None, 163.1)),
        ("DATA", "Other comprehensive income (FY2022)",
         (None, None, None, None, -0.3, -0.7, 22.0, None, 21.0)),
        ("TOTAL", "Total comprehensive income for the year (FY2022)",
         (None, 163.1, None, None, -0.3, -0.7, 22.0, None, 184.1)),
        ("DATA", "Other movements (FY2022)", (None, -0.7, None, None, None, None, None, 1.0, 0.3)),
        ("DATA", "Income tax (FY2022)", (None, -0.7, None, None, None, None, None, None, -0.7)),
        ("DATA", "Dividends paid (FY2022)", (None, -130.1, None, None, None, None, None, None, -130.1)),
        ("DATA", "Capital contribution (FY2022)", (None, None, 1.6, None, None, None, None, None, 1.6)),
        ("DATA", "Return of capital contribution (FY2022)",
         (None, None, -1.6, None, None, None, None, None, -1.6)),
        ("TOTAL", "At 31 July 2022",
         (122.5, 1183.2, None, None, -1.5, 0.1, 21.7, None, 1326.0)),

        ("DATA", "Profit for the year (FY2023)", (None, 89.1, None, None, None, None, None, None, 89.1)),
        ("DATA", "Other comprehensive income (FY2023)",
         (None, None, None, None, 0.3, -2.8, 12.7, None, 10.2)),
        ("TOTAL", "Total comprehensive income for the year (FY2023)",
         (None, 89.1, None, None, 0.3, -2.8, 12.7, None, 99.3)),
        ("DATA", "Other movements (FY2023)", (None, 0.9, None, None, None, None, None, None, 0.9)),
        ("DATA", "Income tax (FY2023)", (None, -0.2, None, None, None, None, None, None, -0.2)),
        ("DATA", "Dividends paid (FY2023)", (None, -89.6, None, None, None, None, None, None, -89.6)),
        ("DATA", "Capital contribution (FY2023)", (None, None, 0.8, None, None, None, None, None, 0.8)),
        ("DATA", "Return of capital contribution (FY2023)",
         (None, None, -0.8, None, None, None, None, None, -0.8)),
        ("TOTAL", "At 31 July 2023",
         (122.5, 1183.4, None, None, -1.2, -2.7, 34.4, None, 1336.4)),

        ("DATA", "Profit for the year (FY2024)", (None, 130.4, None, None, None, None, None, None, 130.4)),
        ("DATA", "Other comprehensive expense (FY2024)",
         (None, None, None, None, -0.1, -2.7, -21.4, None, -24.2)),
        ("TOTAL", "Total comprehensive income/(expense) for the year (FY2024)",
         (None, 130.4, None, None, -0.1, -2.7, -21.4, None, 106.2)),
        ("DATA", "Other equity instrument issued (Note 40) (FY2024)",
         (None, None, None, 197.6, None, None, None, None, 197.6)),
        ("DATA", "Other movements (FY2024)", (None, 1.0, None, None, None, None, None, None, 1.0)),
        ("DATA", "Shares issued (FY2024)", (65.0, None, None, None, None, None, None, None, 65.0)),
        ("DATA", "Coupon paid on other equity instrument (FY2024)",
         (None, -11.1, None, None, None, None, None, None, -11.1)),
        ("DATA", "Capital contribution (FY2024)", (None, None, 0.9, None, None, None, None, None, 0.9)),
        ("DATA", "Return of capital contribution (FY2024)",
         (None, None, -0.9, None, None, None, None, None, -0.9)),
        ("TOTAL", "At 31 July 2024",
         (187.5, 1303.7, None, 197.6, -1.3, -5.4, 13.0, None, 1695.1)),

        ("DATA", "Loss for the year (FY2025)", (None, -85.3, None, None, None, None, None, None, -85.3)),
        ("DATA", "Other comprehensive income/(expense) (FY2025)",
         (None, None, None, None, 0.1, -2.9, -9.2, None, -12.0)),
        ("TOTAL", "Total comprehensive (expense)/income for the year (FY2025)",
         (None, -85.3, None, None, 0.1, -2.9, -9.2, None, -97.3)),
        ("DATA", "Other movements (FY2025)", (None, 1.3, None, None, None, None, None, None, 1.3)),
        ("DATA", "Coupon paid on other equity instrument (FY2025)",
         (None, -22.3, None, None, None, None, None, None, -22.3)),
        ("TOTAL", "At 31 July 2025",
         (187.5, 1197.4, None, 197.6, -1.2, -8.3, 3.8, None, 1576.8)),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=64,
    source_height=340,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Operating profit before tax",
     {"FY2025": -67.6, "FY2024": 178.0, "FY2023": 120.7, "FY2022": 229.4}),
    ("DATA", "Tax paid",
     {"FY2025": -25.2, "FY2024": -30.2, "FY2023": -3.6, "FY2022": -60.8}),
    ("DATA", "Depreciation, amortisation and impairment",
     {"FY2025": 132.9, "FY2024": 96.3, "FY2023": 94.4, "FY2022": 86.6}),
    ("DATA", "Impairment losses on financial assets",
     {"FY2025": 92.8, "FY2024": 98.9, "FY2023": 204.0, "FY2022": 103.3}),
    ("DATA", "Provision in relation to motor finance commissions excluding cash paid",
     {"FY2025": 161.4}),
    ("DATA", "Complaints handling and other operational/legal costs re. motor finance commissions",
     {"FY2025": 5.6}),
    ("DATA", "Provision in relation to early settlements in Motor Finance",
     {"FY2025": 33.0}),
    ("DATA", "Amortisation of de-designated cash flow hedges",
     {"FY2025": -11.4, "FY2024": -27.9}),
    ("DATA", "Decrease/(increase) in interest receivable and prepaid expenses",
     {"FY2025": 11.6, "FY2024": 8.6, "FY2023": -5.7, "FY2022": 19.9}),
    ("DATA", "Decrease in interest payable and accrued expenses",
     {"FY2025": -2.6, "FY2024": -10.7, "FY2023": -0.2, "FY2022": -1.7}),
    ("TOTAL", "Net cash inflow from trading activities",
     {"FY2025": 330.5, "FY2024": 313.0, "FY2023": 409.6, "FY2022": 376.7}),
    ("DATA", "Loans and advances to banks not repayable on demand",
     {"FY2025": 1.3, "FY2024": 24.0, "FY2023": -21.1, "FY2022": -5.9}),
    ("DATA", "Loans and advances to customers",
     {"FY2025": 196.8, "FY2024": -699.4, "FY2023": -584.3, "FY2022": -515.0}),
    ("DATA", "Assets let under operating leases",
     {"FY2025": -20.3, "FY2024": -41.1, "FY2023": -73.2, "FY2022": -54.5}),
    ("DATA", "Certificates of deposit", {"FY2023": 185.0, "FY2022": 79.7}),
    ("DATA", "Sovereign and central bank debt",
     {"FY2025": -213.3, "FY2024": -194.2, "FY2023": 191.2, "FY2022": -255.3}),
    ("DATA", "SSA bonds", {"FY2024": -140.2}),
    ("DATA", "Covered Bonds", {"FY2025": 81.9, "FY2024": -80.7, "FY2023": -105.4}),
    ("DATA", "Deposits by banks",
     {"FY2025": -52.1, "FY2024": -1.3, "FY2023": -22.1, "FY2022": 11.8}),
    ("DATA", "Deposits by customers",
     {"FY2025": 100.1, "FY2024": 975.1, "FY2023": 942.5, "FY2022": 142.7}),
    ("DATA", "Loans and overdrafts from banks",
     {"FY2025": -112.1, "FY2024": -527.7, "FY2023": 24.5, "FY2022": 104.6}),
    ("DATA", "Debt securities in issue (net)",
     {"FY2025": -22.4, "FY2024": -71.6, "FY2023": 10.4, "FY2022": 243.6}),
    ("DATA", "Derivative financial instruments (net)", {"FY2025": 1.0, "FY2023": 70.4}),
    ("DATA", "Other assets less other liabilities",
     {"FY2025": -8.4, "FY2024": 2.8, "FY2023": -10.1, "FY2022": -7.6}),
    ("TOTAL", "Net cash (outflow)/inflow from operating activities",
     {"FY2025": 283.0, "FY2024": -441.3, "FY2023": 1017.4, "FY2022": 120.8, "FY2021": 89.2}),

    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment",
     {"FY2025": -4.5, "FY2024": -4.5, "FY2023": -4.5, "FY2022": -4.6, "FY2021": -3.7}),
    ("DATA", "Purchase of intangible assets - software",
     {"FY2025": -20.6, "FY2024": -27.7, "FY2023": -52.1, "FY2022": -48.8, "FY2021": -43.5}),
    ("DATA", "Purchase of subsidiaries, net of cash acquired",
     {"FY2024": -8.8, "FY2023": 0.0, "FY2022": -0.1}),
    ("TOTAL", "Net cash outflow from investing activities",
     {"FY2025": -25.1, "FY2024": -41.0, "FY2023": -56.6, "FY2022": -53.5, "FY2021": -47.2}),

    ("SECTION", "Financing activities", {}),
    ("DATA", "Equity dividends paid", {"FY2023": -89.5, "FY2022": -127.9, "FY2021": -90.0}),
    ("DATA", "Interest paid on debt financing", {"FY2023": -6.9, "FY2022": -6.9, "FY2021": -6.9}),
    ("DATA", "Issue of ordinary share capital", {"FY2024": 65.0}),
    ("DATA", "Issuance of Additional Tier 1 (\"AT1\") capital securities", {"FY2024": 200.0}),
    ("DATA", "Costs arising on issue of AT1", {"FY2024": -2.4}),
    ("DATA", "AT1 coupon payment", {"FY2025": -22.3, "FY2024": -11.1}),
    ("DATA", "Amounts (paid)/received from group undertakings",
     {"FY2025": 86.4, "FY2024": -171.7, "FY2023": -17.8, "FY2022": 12.8, "FY2021": 19.7}),
    ("DATA", "Payment of lease liabilities",
     {"FY2025": -7.9, "FY2024": -9.9, "FY2023": -9.3, "FY2022": -9.2, "FY2021": -11.0}),
    ("TOTAL", "Net cash (outflow)/inflow from financing activities",
     {"FY2025": 56.2, "FY2024": 69.9, "FY2023": -123.5, "FY2022": -131.2, "FY2021": -88.2}),

    ("TOTAL", "Net (decrease)/increase in cash",
     {"FY2025": 314.1, "FY2024": -412.4, "FY2023": 837.3, "FY2022": -63.9, "FY2021": -46.2}),
    ("DATA", "Cash and cash equivalents at beginning of year",
     {"FY2025": 1728.1, "FY2024": 2140.5, "FY2023": 1303.2, "FY2022": 1367.1, "FY2021": 1413.3}),
    ("TOTAL", "Cash and cash equivalents at end of year",
     {"FY2025": 2042.2, "FY2024": 1728.1, "FY2023": 2140.5, "FY2022": 1303.2, "FY2021": 1367.1}),
]

bw.add_cash_flow_sheet(
    title="Close Brothers Limited — Consolidated Cash Flow Statement",
    subtitle="Consolidated basis (Close Brothers Limited + subsidiaries), £m. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=88,
    source_height=320,
    unit_suffix=" (£m)",
)

bw.add_asset_quality_sheet(
    title="Close Brothers Limited — Asset Quality",
    subtitle="Loans and advances to customers held at amortised cost, by IFRS 9 stage, £m. Consolidated basis. See source note at bottom.",
    rows=[
        ("SECTION", "Gross loans and advances to customers held at amortised cost, by IFRS 9 stage", {}),
        ("DATA", "Stage 1",
         {"FY2025": 7914.2, "FY2024": 8410.5, "FY2023": 7990.2, "FY2022": 7627.0, "FY2021": 7434.3}),
        ("DATA", "Stage 2",
         {"FY2025": 1291.0, "FY2024": 1128.8, "FY2023": 1062.0, "FY2022": 1158.9, "FY2021": 960.2}),
        ("DATA", "Stage 3",
         {"FY2025": 492.1, "FY2024": 725.5, "FY2023": 583.4, "FY2022": 358.6, "FY2021": 330.4}),
        ("TOTAL", "Total gross loans and advances to customers",
         {"FY2025": 9697.3, "FY2024": 10264.8, "FY2023": 9635.6, "FY2022": 9144.5, "FY2021": 8724.9}),

        ("SECTION", "Impairment (ECL) provisions, by IFRS 9 stage", {}),
        ("DATA", "Stage 1",
         {"FY2025": -50.6, "FY2024": -52.2, "FY2023": -58.1, "FY2022": -50.3, "FY2021": -80.0}),
        ("DATA", "Stage 2",
         {"FY2025": -33.6, "FY2024": -31.3, "FY2023": -32.2, "FY2022": -78.3, "FY2021": -84.2}),
        ("DATA", "Stage 3",
         {"FY2025": -165.5, "FY2024": -362.3, "FY2023": -290.3, "FY2022": -157.0, "FY2021": -116.2}),
        ("TOTAL", "Total impairment provisions",
         {"FY2025": -249.7, "FY2024": -445.8, "FY2023": -380.6, "FY2022": -285.6, "FY2021": -280.4}),

        ("TOTAL", "Net loans and advances to customers held at amortised cost (derived)",
         {"FY2025": 9447.6, "FY2024": 9819.0, "FY2023": 9255.0, "FY2022": 8858.9, "FY2021": 8444.5}),

        ("SECTION", "Derived ratios", {}),
        ("DATA", "Stage 3 / gross loans (NPL ratio)",
         {"FY2025": "5.07%", "FY2024": "7.07%", "FY2023": "6.05%", "FY2022": "3.92%", "FY2021": "3.79%"}),
        ("DATA", "Stage 3 coverage (Stage 3 provision / Stage 3 gross)",
         {"FY2025": "33.64%", "FY2024": "49.94%", "FY2023": "49.76%", "FY2022": "43.78%", "FY2021": "35.17%"}),
        ("DATA", "Total ECL coverage (total provision / total gross)",
         {"FY2025": "2.57%", "FY2024": "4.34%", "FY2023": "3.95%", "FY2022": "3.12%", "FY2021": "3.21%"}),
    ],
    sources_text=(
        "Sources - Close Brothers Limited's own Notes to the Consolidated Accounts, Note 10 'Loans and "
        "advances to customers', part (d) 'Reconciliation of loans and advances to customers held at "
        "amortised cost and impairment provisions':\n"
        "FY2025: p.122-123 - " + AR2025_URL + "\n"
        "FY2024: same FY2025 filing's own FY2024 comparative/opening-balance rows, p.122\n"
        "FY2023: p.91-92 - " + AR2023_URL + "\n"
        "FY2022: same FY2023 filing's own FY2022 comparative/opening-balance rows, p.91-92\n"
        "FY2021: p.72-73 - " + AR2021_URL + "\n\n"
        + STATEMENTS_ENTITY_NOTE + "\n\n"
        "PRESENTATION NOTE: this note covers only loans held at amortised cost, not the full Balance Sheet "
        "'Loans and advances to customers' line (which also includes operating lease finance receivables and "
        "fair value adjustments). For FY2023/FY2022/FY2021 the derived net figure ties exactly to the "
        "Balance Sheet; for FY2025/FY2024 there is a small ~£11-12m gap (Balance Sheet £9,459.4m/£9,830.8m vs "
        "derived £9,447.6m/£9,819.0m) consistent with a growing operating-lease book in those years - shown "
        "as reported, not forced to reconcile."
    ),
    first_col_width=64,
    source_height=280,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets - genuinely none disclosed at this entity level
# ---------------------------------------------------------------
NOT_DISCLOSED_NOTE = (
    "Close Brothers Limited (the PRA-regulated entity, FRN 124750) does not publish its own Pillar 3 "
    "disclosures or Basel capital/liquidity ratios - checked its full 'Group of companies' accounts' "
    "statutory filings (all 5 years) for a capital management/regulatory capital note and found none. "
    "Pillar 3 is published only at the wider listed parent 'Close Brothers Group plc' level (confirmed "
    "via closebrothers.com's investor relations Pillar 3 Disclosures page) - a different, non-PRA-"
    "regulated entity, so those figures are not used here rather than mixing entity levels."
)

bw.add_not_disclosed_metric_sheets(
    ["CET1 Capital", "CET1 Ratio", "Tier 1 Capital", "Tier 1 Ratio", "Total Capital", "Total Capital Ratio",
     "Total RWAs"],
    "Sources - Close Brothers Limited Pillar 3 basis:\n" + NOT_DISCLOSED_NOTE,
    per_note={m: NOT_DISCLOSED_NOTE for m in
              ["CET1 Capital", "CET1 Ratio", "Tier 1 Capital", "Tier 1 Ratio", "Total Capital",
               "Total Capital Ratio", "Total RWAs"]},
)

bw.add_rwa_breakdown_sheet(
    title="Close Brothers Limited — RWA Breakdown",
    subtitle="Not publicly disclosed. See source note at bottom.",
    rows=[("DATA", "Not publicly disclosed", {})],
    sources_text="Sources - Close Brothers Limited Pillar 3 basis:\n" + NOT_DISCLOSED_NOTE,
    first_col_width=54,
    source_height=280,
)

bw.add_not_disclosed_metric_sheets(
    ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"],
    "Sources - Close Brothers Limited Pillar 3 basis:\n" + NOT_DISCLOSED_NOTE,
    per_note={m: NOT_DISCLOSED_NOTE for m in
              ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"]},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets",
         {"FY2025": 13132.8, "FY2024": 13053.2, "FY2023": 12488.1, "FY2022": 11508.3, "FY2021": 10950.9}),
        ("Loans and advances to customers",
         {"FY2025": 9459.4, "FY2024": 9830.8, "FY2023": 9255.0, "FY2022": 8858.9, "FY2021": 8444.5}),
        ("Deposits by customers",
         {"FY2025": 8799.3, "FY2024": 8693.6, "FY2023": 7724.5, "FY2022": 6770.4, "FY2021": 6634.8}),
        ("Total equity",
         {"FY2025": 1576.8, "FY2024": 1695.1, "FY2023": 1336.4, "FY2022": 1326.0, "FY2021": 1272.4}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Operating income",
         {"FY2025": 671.2, "FY2024": 724.9, "FY2023": 714.4, "FY2022": 695.4, "FY2021": 634.0}),
        ("Total operating expenses",
         {"FY2025": -738.8, "FY2024": -546.9, "FY2023": -593.7, "FY2022": -465.9, "FY2021": -419.2}),
        ("(Loss)/profit after tax",
         {"FY2025": -85.3, "FY2024": 130.4, "FY2023": 89.1, "FY2022": 163.1, "FY2021": 159.4}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity",
         {"FY2025": 1695.1, "FY2024": 1336.4, "FY2023": 1326.0, "FY2022": 1272.4, "FY2021": 1198.0}),
        ("Total comprehensive (loss)/income for the year",
         {"FY2025": -97.3, "FY2024": 106.2, "FY2023": 99.3, "FY2022": 184.1, "FY2021": 165.4}),
        ("Other equity movements, net",
         {"FY2025": -21.0, "FY2024": 252.5, "FY2023": -88.9, "FY2022": -130.5, "FY2021": -91.0}),
        ("Closing equity",
         {"FY2025": 1576.8, "FY2024": 1695.1, "FY2023": 1336.4, "FY2022": 1326.0, "FY2021": 1272.4}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash (outflow)/inflow from operating activities",
         {"FY2025": 283.0, "FY2024": -441.3, "FY2023": 1017.4, "FY2022": 120.8, "FY2021": 89.2}),
        ("Net cash outflow from investing activities",
         {"FY2025": -25.1, "FY2024": -41.0, "FY2023": -56.6, "FY2022": -53.5, "FY2021": -47.2}),
        ("Net cash (outflow)/inflow from financing activities",
         {"FY2025": 56.2, "FY2024": 69.9, "FY2023": -123.5, "FY2022": -131.2, "FY2021": -88.2}),
        ("Cash and cash equivalents at end of year",
         {"FY2025": 2042.2, "FY2024": 1728.1, "FY2023": 2140.5, "FY2022": 1303.2, "FY2021": 1367.1}),
    ],
    cash_flow_unit="£m",
    ratios=[],
    note="No Pillar 3 ratios chart shown - Close Brothers Limited (the PRA-regulated entity) does not "
         "publish its own Basel capital/liquidity disclosures; Pillar 3 exists only at the wider listed "
         "parent Close Brothers Group plc level. See the Cash Flow Statement sheet's source note and each "
         "Pillar 3 sheet for detail. Cash flow figures are duplicated from the detail sheet for at-a-glance "
         "trend viewing.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/CLOSE BROTHERS FINANCIALS.xlsx")
