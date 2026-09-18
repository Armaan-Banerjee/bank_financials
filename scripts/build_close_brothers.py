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

# ---------------------------------------------------------------------------
# CORRECTION FOUND 2026-09-16 (KM1-010): Close Brothers Limited's regulatory
# metrics ARE published in a Pillar 3 document, not only inside the statutory
# filings. Close Brothers Group plc's annual Pillar 3 prints UK KM1 with SIX
# columns - three for "Group" (CBG plc) and three for "Individual", the latter
# being CBL on the CRR article 9 individual-consolidation basis. Every prior
# session searched only the Companies House filings and the group narrative,
# so the CBL half of that table was never seen. Its capital, RWA, ratio, LCR
# and NSFR figures agree cell-for-cell with the Strategic Report table this
# workbook already used, which is what confirms the two are the same basis.
# It also discloses a CBL LEVERAGE RATIO, which this workbook previously
# asserted was "genuinely not disclosed at this entity level" - see the
# Leverage Ratio sheet for the retraction.
#
# The documents are reached from closebrothers.com's own "Results, reports and
# presentations" page; the visible links are Pardot redirectors on
# files.closebrothers.com which serve an HTML <embed> wrapper, and the PDF
# itself lives on storage.pardot.com. Both are recorded so a later session can
# verify either. All five verified 2026-09-16 by HTTP 200 + Content-Type
# application/pdf + %PDF magic bytes.
CBG_REPORTS_INDEX = ("https://www.closebrothers.com/s/investor-relations/investor-information/"
                     "results-reports-and-presentations")
CBG_P3_2025_URL = "https://storage.pardot.com/186742/1779102089T5UqOZ2F/Pillar3Disclosures2025.pdf"
CBG_P3_2024_URL = "https://storage.pardot.com/186742/177910260307OnlFA4/Pillar_3_Disclosures_2024.pdf"
CBG_P3_2023_URL = "https://storage.pardot.com/186742/17791028104aOkhZu0/Pillar_3_Disclosures_2023.pdf"
CBG_P3_2022_URL = "https://storage.pardot.com/186742/17791029759gmHVOKT/Pillar_3_2022___Doc__14__0.pdf"
CBG_P3_2021_URL = "https://storage.pardot.com/186742/1781775148kmJ2jvY6/CBG_Pillar_3_disclosures_2021.pdf"
CBG_P3_HY2026_URL = ("https://storage.pardot.com/186742/1778671946zDhym2UD/"
                     "CBG_Half_Year_Pillar_3_disclosures_January_2026.pdf")

LATEST_EDITION_NOTE = (
    "LATEST-EDITION CHECK, 2026-09-16: read off closebrothers.com's own 'Results, reports and "
    f"presentations' page ({CBG_REPORTS_INDEX}), not from the URLs previously cited in this script. "
    "The newest ANNUAL documents published are the Annual Report 2025 and Pillar 3 Disclosures 2025, "
    "both dated 3 October 2025 and both for the year ended 31 July 2025 - the year this workbook already "
    "ends on. The newest Pillar 3 of any kind is the half-year edition for the six months ended 31 "
    f"January 2026, published 17 March 2026 ({CBG_P3_HY2026_URL}); it is an interim period, not a "
    "financial year, so no column is taken from it, but its 31 Jul 2025 comparative column reproduces "
    "every FY2025 individual-basis figure used here identically, which is a useful independent check. "
    "Close Brothers Group plc's own financial calendar puts the '2026 Preliminary Results' (year ended "
    "31 July 2026) on 29 September 2026, i.e. AFTER the date of this check, and Close Brothers Limited's "
    "own statutory filing for that year would not reach Companies House until around December 2026. "
    "Checked, none newer. YEARS unchanged."
)

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
# Pillar 3 metric sheets
# ---------------------------------------------------------------
# CORRECTION (re-verified 2026-09-12): this workbook previously marked every
# Pillar 3 metric "not publicly disclosed", on the stated basis that the
# entity's own statutory filings carry no capital note. That was WRONG. All
# five Companies House filings are scanned/image-only PDFs with no text
# layer, so the original text-only search found nothing - OCR of the same
# filings (pdftoppm + tesseract) finds a full regulatory-capital disclosure
# in every year:
#   - FY2025/FY2024: Strategic Report "Composition of regulatory capital and
#     Pillar 1 risk weighted assets", AR2025 printed p.38 (PDF p.39), plus the
#     narrative capital section on printed p.37; Note 40 "Capital" (PDF p.173)
#     cross-refers to it ("The capital position for the group is disclosed in
#     pages 36 to 39 of the Strategic Report").
#   - FY2023/FY2022: same table, AR2023 printed p.27 (PDF p.28).
#   - FY2021: Note 21 "Capital", AR2021 printed p.92 (PDF p.93).
# BASIS: these are the "group" figures as that term is defined inside these
# filings - Close Brothers Limited AND its subsidiaries - i.e. the same
# CBL-consolidated entity basis this workbook's statement sheets use, NOT the
# wider listed Close Brothers Group plc. The filings are explicit that CBG plc
# publishes its own separate Pillar 3; those figures are still not used here.
P3_SOURCES = (
    "Sources - Close Brothers Limited's own Companies House 'Group of companies' accounts' filings "
    "(Close Brothers Limited + its subsidiaries - NOT the listed Close Brothers Group plc). All five "
    "filings are scanned/image-only PDFs with no text layer; figures below were read by OCR of the "
    "rendered pages and each year's RWA components were checked to foot to that year's own disclosed "
    "total.\n"
    "FY2025 & FY2024: Annual Report 2025, Strategic Report 'Composition of regulatory capital and "
    "Pillar 1 risk weighted assets', printed p.38 (PDF p.39), with supporting narrative p.37; audited "
    "Note 40 'Capital' (PDF p.173) cross-refers to it - " + AR2025_URL + "\n"
    "FY2023 & FY2022: Annual Report 2023, same Strategic Report table, printed p.27 (PDF p.28) - "
    + AR2023_URL + "\n"
    "FY2021: Annual Report 2021, Note 21 'Capital' to the Consolidated Accounts, printed p.92 "
    "(PDF p.93) - " + AR2021_URL + "\n\n"
    "The FY2025 and FY2023 tables are labelled unaudited except where stated (FY2025's 'Total "
    "regulatory capital' line is marked audited); FY2021's is inside an audited note but its RWA and "
    "ratio rows are themselves marked unaudited. Ratios are as each report states them, not recomputed.\n\n"
    "SECOND, INDEPENDENT SOURCE FOUND 2026-09-16 (KM1-010), and it corroborates every figure above. "
    "Close Brothers Group plc's annual Pillar 3 prints template UK KM1 with an 'Individual' block "
    "beside its 'Group' block, the Individual block being CBL on the CRR article 9 individual-"
    "consolidation basis. For FY2022-FY2025 its CET1 capital, Tier 1 capital, total capital, total "
    "risk-weighted exposure amount and all three capital ratios match the Companies House Strategic "
    "Report figures on this sheet cell-for-cell, which is what establishes that the two are the same "
    "basis rather than merely similar. That document is cited in full on the KM1 Key Metrics sheet, and "
    "it is also where this workbook's leverage-ratio retraction comes from - see the Leverage Ratio "
    f"sheet. Index page: {CBG_REPORTS_INDEX}\n\n"
    "WHY THAT SECOND SOURCE STOPS AT KM1, IN THE PUBLISHER'S OWN WORDS (added 2026-09-18, KM1-032). "
    "The parent's Pillar 3 states the limit of its CBL-level disclosure explicitly: 'The only "
    "quantitative disclosures for the individual consolidation basis included within this document are "
    "UK KM1 and the IFRS 9 transitional arrangements template. In line with CRR article 432, other "
    "templates are not disclosed on an individual consolidation basis as they are consistent with group "
    "disclosures or are not deemed materially different.' (Pillar 3 Disclosures 2025, printed p.2 / PDF "
    "p.6; re-read 18 September 2026.) This is a formal Article 432 exclusion, and it settles a question "
    "that would otherwise stay open across EVERY sheet in this workbook rather than one metric: where a "
    "CBL-level template is absent here, the reason of record is that Close Brothers chose not to publish "
    "it on that basis - not that it was published somewhere this project failed to reach. It is also why "
    "the Companies House filings above remain the primary source for the metric sheets: outside UK KM1 "
    "there is no CBL-level Pillar 3 template to read, in any edition."
    + "\n\n"
    + LATEST_EDITION_NOTE
)

TIER1_DERIVATION_NOTE = (
    "FY2025/FY2024 are directly disclosed (the £200.0m AT1 contingent convertible securities issued "
    "29 November 2023 give a Tier 1 figure distinct from CET1). FY2023/FY2022/FY2021 are not separately "
    "labelled 'Tier 1' in the source tables because no AT1 instrument was in issue in those years - each "
    "table runs CET1 capital -> Tier 2 subordinated debt -> Total regulatory capital with no AT1 line, "
    "and CET1 + Tier 2 equals the disclosed Total exactly (FY2023: 1,139.6 + 200.0 = 1,339.6; FY2022: "
    "1,194.4 + 200.0 = 1,394.4; FY2021: 1,224.9 + 223.4 = 1,448.3). Tier 1 therefore equals CET1 in "
    "those three years as a matter of the source table's own arithmetic, not an estimate."
)


def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit or "", rows_data, sources_text,
                        note=note, first_col_width=54, source_height=310)


# ---------------------------------------------------------------
# Sheet: KM1 Key Metrics
# ---------------------------------------------------------------
# Every figure below is the "Individual" half of Close Brothers Group plc's
# UK KM1 - i.e. Close Brothers Limited on the CRR article 9 individual-
# consolidation basis - never the "Group" half. Rule 11 in the KM1 map (one
# document printing the template twice, once per entity basis) applies here in
# its sharper form: ONE table, six columns, two entities side by side, and the
# wrong three columns look entirely plausible (FY2025 CET1 is 1,348.1 on the
# group side against 1,229.2 on CBL's, a 10% error).
KM1_SOURCES = (
    "Sources - Close Brothers Limited ('CBL') on the CRR article 9 individual-consolidation basis, read "
    "from the 'Individual' columns of Close Brothers Group plc's own annual Pillar 3 UK KM1. Each year "
    "comes from the edition in which it is the REPORTING year, except FY2022 - see below. Amounts £m.\n"
    f"FY2025: Pillar 3 Disclosures 2025 (year ended 31 July 2025), 'Annex I: Key metrics and overview of "
    f"risk-weighted exposure amounts / UK KM1 - Key metrics', printed pp.3-4, column a under 'Individual' "
    f"(31 Jul 2025) - {CBG_P3_2025_URL}\n"
    f"FY2024: Pillar 3 Disclosures 2024, same template, printed pp.3-4, 'Individual' column a "
    f"(31 Jul 2024) - {CBG_P3_2024_URL}\n"
    f"FY2023: Pillar 3 Disclosures 2023, same template, printed pp.3-4, 'Individual' column a "
    f"(31 Jul 2023) - {CBG_P3_2023_URL}\n"
    f"FY2022: Pillar 3 Disclosures 2023, 'Individual' column e (31 Jul 2022) - {CBG_P3_2023_URL}. This is "
    "the one column taken from a later edition's comparative, and it is not a choice: FY2022's OWN edition "
    f"({CBG_P3_2022_URL}) prints UK KM1 for the GROUP ONLY - three columns, no 'Individual' block at all - "
    "so no CBL KM1 exists in the document for which FY2022 is the reporting year. Cross-checked against "
    "this workbook's own metric sheets, which take FY2022 independently from the FY2023 Annual Report's "
    "Strategic Report table: CET1 1,194.4, total capital 1,394.4, RWAs 8,847.6 and the three ratios all "
    "agree, so the comparative is not a restatement of anything.\n"
    "FY2021: BLANK, on two independent grounds. (a) FY2021's own edition (Pillar 3 disclosures for the "
    f"year ended 31 July 2021 - {CBG_P3_2021_URL}) contains no UK KM1: the template arrived with the "
    "Disclosure (CRR) Part of the PRA Rulebook and post-dates a 31 July 2021 year end. What it prints "
    "instead, at section 3 'Key Regulatory Metrics' (printed p.15), is a ten-row unnumbered summary - "
    "capital, RWAs, three ratios, leverage, LCR - with no SREP rows, no buffer rows, no HQLA/outflow "
    "build-up and no NSFR. Under the row-set test that is a different and shorter table, not an "
    "unnumbered KM1, and mapping it onto template row numbers would invent a correspondence Close "
    "Brothers never published. (b) That table is GROUP-basis in any case; the FY2021 edition carries no "
    "quantitative CBL individual-consolidation disclosure at all, only the qualitative 'Individual "
    "Consolidation' paragraph on printed p.2. This workbook's FY2021 capital figures come instead from "
    f"CBL's own Annual Report 2021, Note 21 'Capital' - {AR2021_URL}.\n\n"
    "WHICH THREE COLUMNS. Each edition's KM1 is one table with six columns: columns a/c/e under a 'Group' "
    "heading (Close Brothers Group plc) and columns a/c/e under an 'Individual' heading (CBL). Only the "
    "'Individual' block is used here, because this is a Close Brothers Limited workbook. The editions "
    "footnote the basis themselves: 'For capital and leverage, the PRA supervises CBL on an individual "
    "consolidation basis as permitted under CRR article 9. For liquidity and funding, the PRA supervises "
    "CBL on an individual basis, excluding all subsidiary undertakings.' Columns c (the 31 January "
    "half-year) are not carried - only the column whose date is the financial year end.\n\n"
    "ROWS THE TEMPLATE OMITS, AND WHY. Rows 14a-14e are absent from every edition, and that is a stated "
    "exclusion rather than a gap: each edition footnotes 'Rows 14a-14e have been removed as only LREQ "
    "firms are required to disclose this information.' Columns b and d are removed on the same footing "
    "('only required to disclose information on a semi-annual basis'). Rows 10 and UK 10a (G-SII / O-SII "
    "buffers) and UK 8a / UK 9a (systemic risk buffers) are not printed in any edition. Row 11 appears "
    "without a row 10 above it, exactly as published.\n\n"
    "FY2022 NSFR ROWS ARE BLANK BECAUSE THE TEMPLATE LEAVES THEM BLANK, and the reason is footnoted. The "
    "FY2023 edition's footnote 3 reads: 'NSFR was implemented under CRR on 1 January 2022 and as such no "
    "comparative has been provided for the four-quarter average to 31 July 2022. The point in time NSFR "
    "at 31 July 2022 was 118.3% for the CBG group and 133.6% for CBL.' The 133.6% that this workbook's "
    "NSFR sheet carries for FY2022 is therefore a POINT-IN-TIME figure sitting in a column of "
    "four-quarter averages - a real basis difference, recorded on both sheets rather than reconciled. "
    "Rows 18 and 19 have no FY2022 figure on any basis.\n\n"
    "LEVERAGE. Rows 13/14 are captioned 'excluding claims on central banks' in every edition that prints "
    "them, all of which report periods ending after the 1 January 2022 basis change, so there is no "
    "basis break inside this sheet and a single caption block is correct. These rows are the source of "
    "the correction recorded on the Leverage Ratio sheet.\n\n"
    "PRECISION IS AS PRINTED: one decimal place throughout, including '0.0' for the FY2022 "
    "countercyclical buffer, which is a printed zero and is kept as a zero rather than blanked.\n\n"
    + LATEST_EDITION_NOTE
)

km1_rows = [
    ("SECTION", "Available own funds (amounts) — £m", {}),
    ("DATA", "1    Common equity tier 1 (\"CET1\") capital",
     {"FY2025": 1229.2, "FY2024": 1326.4, "FY2023": 1139.6, "FY2022": 1194.4}),
    ("DATA", "2    Tier 1 capital",
     {"FY2025": 1429.2, "FY2024": 1526.4, "FY2023": 1139.6, "FY2022": 1194.4}),
    ("DATA", "3    Total capital",
     {"FY2025": 1629.2, "FY2024": 1726.4, "FY2023": 1339.6, "FY2022": 1394.4}),
    ("SECTION", "Risk-weighted exposure amounts — £m", {}),
    ("DATA", "4    Total risk-weighted exposure amount",
     {"FY2025": 9534.2, "FY2024": 10033.9, "FY2023": 9159.2, "FY2022": 8847.6}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "5    Common equity tier 1 ratio (%)",
     {"FY2025": "12.9%", "FY2024": "13.2%", "FY2023": "12.4%", "FY2022": "13.5%"}),
    ("DATA", "6    Tier 1 ratio (%)",
     {"FY2025": "15.0%", "FY2024": "15.2%", "FY2023": "12.4%", "FY2022": "13.5%"}),
    ("DATA", "7    Total capital ratio (%)",
     {"FY2025": "17.1%", "FY2024": "17.2%", "FY2023": "14.6%", "FY2022": "15.8%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "UK 7a    Additional CET1 SREP requirements (%)",
     {"FY2025": "1.0%", "FY2024": "1.0%", "FY2023": "0.8%", "FY2022": "0.8%"}),
    ("DATA", "UK 7b    Additional AT1 SREP requirements (%)",
     {"FY2025": "0.3%", "FY2024": "0.3%", "FY2023": "0.3%", "FY2022": "0.3%"}),
    ("DATA", "UK 7c    Additional T2 SREP requirements (%)",
     {"FY2025": "0.4%", "FY2024": "0.4%", "FY2023": "0.3%", "FY2022": "0.3%"}),
    ("DATA", "UK 7d    Total SREP own funds requirements (%)",
     {"FY2025": "9.8%", "FY2024": "9.8%", "FY2023": "9.4%", "FY2022": "9.4%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "8    Capital conservation buffer (%)",
     {"FY2025": "2.5%", "FY2024": "2.5%", "FY2023": "2.5%", "FY2022": "2.5%"}),
    ("DATA", "9    Institution specific countercyclical capital buffer (%)",
     {"FY2025": "1.9%", "FY2024": "1.9%", "FY2023": "1.9%", "FY2022": "0.0%"}),
    ("DATA", "11    Combined buffer requirement (%)",
     {"FY2025": "4.4%", "FY2024": "4.4%", "FY2023": "4.4%", "FY2022": "2.5%"}),
    ("DATA", "UK 11a    Overall capital requirements (%)",
     {"FY2025": "14.2%", "FY2024": "14.2%", "FY2023": "13.8%", "FY2022": "11.9%"}),
    ("DATA", "12    CET1 available after meeting total SREP own funds requirements (%)",
     {"FY2025": "7.3%", "FY2024": "7.4%", "FY2023": "5.3%", "FY2022": "6.4%"}),
    ("SECTION", "Leverage ratio — amounts £m (rows 14a-14e removed by the bank: LREQ firms only)", {}),
    ("DATA", "13    Total exposure measure excluding claims on central banks",
     {"FY2025": 11323.0, "FY2024": 11399.2, "FY2023": 10540.3, "FY2022": 10546.9}),
    ("DATA", "14    Leverage ratio excluding claims on central banks (%)",
     {"FY2025": "12.6%", "FY2024": "13.4%", "FY2023": "10.8%", "FY2022": "11.3%"}),
    ("SECTION", "Liquidity coverage ratio — amounts £m, 12-month average to the period end", {}),
    ("DATA", "15    Total high-quality liquid assets (\"HQLA\") (Weighted value - average)",
     {"FY2025": 2477.8, "FY2024": 2197.8, "FY2023": 1931.8, "FY2022": 1259.9}),
    ("DATA", "UK 16a    Cash outflows - Total weighted value",
     {"FY2025": 1050.8, "FY2024": 945.2, "FY2023": 698.4, "FY2022": 569.7}),
    ("DATA", "UK 16b    Cash inflows - Total weighted value",
     {"FY2025": 2145.8, "FY2024": 2206.1, "FY2023": 2036.1, "FY2022": 1778.9}),
    ("DATA", "16    Total net cash outflows (adjusted value)",
     {"FY2025": 262.7, "FY2024": 236.3, "FY2023": 174.6, "FY2022": 142.4}),
    ("DATA", "17    Liquidity coverage ratio (%)",
     {"FY2025": "943.2%", "FY2024": "930.1%", "FY2023": "1,106.4%", "FY2022": "884.7%"}),
    ("SECTION", "Net stable funding ratio — amounts £m, four-quarter average to the period end", {}),
    ("DATA", "18    Total available stable funding",
     {"FY2025": 10563.6, "FY2024": 10139.2, "FY2023": 9139.8}),
    ("DATA", "19    Total required stable funding",
     {"FY2025": 6479.7, "FY2024": 6839.1, "FY2023": 6505.1}),
    ("DATA", "20    Net stable funding ratio (%)",
     {"FY2025": "163.0%", "FY2024": "148.3%", "FY2023": "140.5%"}),
]

bw.add_km1_sheet(
    title="Close Brothers Limited — KM1 Key Metrics",
    subtitle="UK KM1 as published, Close Brothers Limited on the CRR article 9 individual-consolidation "
             "basis (the 'Individual' columns of Close Brothers Group plc's Pillar 3 UK KM1, never the "
             "'Group' columns). Amounts £m, ratios as printed. FY2021 is blank: that year's edition "
             "pre-dates the template and carries no CBL figures - see source note at bottom.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=72,
    source_height=560,
)

metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital",
      {"FY2025": 1229.2, "FY2024": 1326.4, "FY2023": 1139.6, "FY2022": 1194.4, "FY2021": 1224.9})],
    P3_SOURCES,
    note="Shown after applying IFRS 9 transitional arrangements and the CRR transitional/qualifying own "
         "funds arrangements in force at the time, as each source table states.",
)

metric(
    "CET1 Ratio", "%",
    [("CET1 capital ratio",
      {"FY2025": "12.9%", "FY2024": "13.2%", "FY2023": "12.4%", "FY2022": "13.5%", "FY2021": "14.6%"})],
    P3_SOURCES,
    note="Transitional basis, as disclosed. On a fully-loaded basis (without IFRS 9 transitional and CRR "
         "qualifying own funds arrangements) the source reports state 12.8% for FY2025, 13.1% for FY2024, "
         "12.1% for FY2023, 12.7% for FY2022 and 12.9% for FY2021.",
)

metric(
    "Tier 1 Capital", "£m",
    [("Total Tier 1 capital",
      {"FY2025": 1429.2, "FY2024": 1526.4, "FY2023": 1139.6, "FY2022": 1194.4, "FY2021": 1224.9}),
     ("of which: Additional Tier 1 capital",
      {"FY2025": 200.0, "FY2024": 200.0})],
    P3_SOURCES,
    note=TIER1_DERIVATION_NOTE,
)

metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 capital ratio",
      {"FY2025": "15.0%", "FY2024": "15.2%", "FY2023": "12.4%", "FY2022": "13.5%", "FY2021": "14.6%"})],
    P3_SOURCES,
    note="FY2025/FY2024 directly disclosed. FY2023-FY2021 equal the disclosed CET1 capital ratio because "
         "no AT1 was in issue in those years - see the Tier 1 Capital sheet's note. Fully-loaded FY2025 "
         "14.9%, FY2024 15.1% per the FY2025 report.",
)

metric(
    "Total Capital", "£m",
    [("Total regulatory capital",
      {"FY2025": 1629.2, "FY2024": 1726.4, "FY2023": 1339.6, "FY2022": 1394.4, "FY2021": 1448.3}),
     ("of which: Tier 2 capital - subordinated debt",
      {"FY2025": 200.0, "FY2024": 200.0, "FY2023": 200.0, "FY2022": 200.0, "FY2021": 223.4})],
    P3_SOURCES,
)

metric(
    "Total Capital Ratio", "%",
    [("Total capital ratio",
      {"FY2025": "17.1%", "FY2024": "17.2%", "FY2023": "14.6%", "FY2022": "15.8%", "FY2021": "17.3%"})],
    P3_SOURCES,
    note="Transitional basis, as disclosed. Fully-loaded equivalents stated in the source reports: FY2025 "
         "17.0%, FY2024 17.1%, FY2023 14.3%, FY2022 14.9%, FY2021 15.6%.",
)

metric(
    "Total RWAs", "£m",
    [("Total Pillar 1 risk weighted assets",
      {"FY2025": 9534.2, "FY2024": 10033.9, "FY2023": 9159.2, "FY2022": 8847.6, "FY2021": 8387.4})],
    P3_SOURCES,
    note="FY2021's table labels these 'risk weighted assets (notional)'. In every year the disclosed "
         "credit/operational/market components foot exactly to this total - see the RWA Breakdown sheet.",
)

bw.add_rwa_breakdown_sheet(
    title="Close Brothers Limited — RWA Breakdown",
    subtitle="Pillar 1 RWAs by risk category, CBL-consolidated basis, £m. All 5 years disclosed.",
    rows=[
        ("DATA", "Credit and counterparty credit risk",
         {"FY2025": 8841.5, "FY2024": 9370.8, "FY2023": 8544.7, "FY2022": 8263.0, "FY2021": 7840.9}),
        ("DATA", "Operational risk",
         {"FY2025": 673.9, "FY2024": 643.0, "FY2023": 602.4, "FY2022": 561.1, "FY2021": 533.0}),
        ("DATA", "Market risk",
         {"FY2025": 18.8, "FY2024": 20.1, "FY2023": 12.1, "FY2022": 23.5, "FY2021": 13.5}),
        ("TOTAL", "Total risk weighted assets",
         {"FY2025": 9534.2, "FY2024": 10033.9, "FY2023": 9159.2, "FY2022": 8847.6, "FY2021": 8387.4}),
    ],
    sources_text=P3_SOURCES + (
        "\n\nEach year's three components foot exactly to that year's own disclosed total (FY2025 "
        "8,841.5 + 673.9 + 18.8 = 9,534.2; FY2024 9,370.8 + 643.0 + 20.1 = 10,033.9; FY2023 8,544.7 + "
        "602.4 + 12.1 = 9,159.2; FY2022 8,263.0 + 561.1 + 23.5 = 8,847.6; FY2021 7,840.9 + 533.0 + 13.5 "
        "= 8,387.4). FY2025's Market risk figure was initially mis-OCR'd as 13.8 at 250 dpi, which broke "
        "the footing by 5.0; re-rendering that page at 450 dpi resolved it to 18.8, which foots exactly - "
        "recorded here because the same failure mode could recur on these scanned filings.\n"
        "FY2023/FY2022/FY2021 note that operational and market risk include an adjustment at 8% in order "
        "to determine notional RWAs. No finer sub-split (e.g. standardised vs IRB, or a UK OV1 template) "
        "is published at this entity level in any year - and that is now a documented exclusion rather "
        "than the outcome of a search: the parent's Pillar 3 states that UK KM1 and the IFRS 9 "
        "transitional template are the ONLY quantitative disclosures it gives on the individual "
        "consolidation basis, other templates being withheld under CRR article 432 (quoted in full in "
        "the source note above). UK OV1 is printed in those documents on the GROUP basis only, and group "
        "RWAs are not substituted here."
    ),
    first_col_width=54,
    source_height=380,
    unit_suffix=" (£m)",
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio excluding claims on central banks",
      {"FY2025": "12.6%", "FY2024": "13.4%", "FY2023": "10.8%", "FY2022": "11.3%",
       "FY2021": "Not publicly disclosed"}),
     ("Leverage ratio total exposure measure excluding claims on central banks (£m)",
      {"FY2025": 11323.0, "FY2024": 11399.2, "FY2023": 10540.3, "FY2022": 10546.9})],
    KM1_SOURCES,
    note="RETRACTION, 2026-09-16. Until today this sheet read 'Not publicly disclosed' for all five "
         "years, on the stated basis that the leverage ratio is 'genuinely not disclosed at this entity "
         "level in any of the five years'. THAT WAS WRONG, and the error was one of scope rather than of "
         "extraction: the earlier sweep OCR'd Close Brothers Limited's Companies House filings in full "
         "and correctly found no leverage figure there, then wrote that finding down as a fact about the "
         "BANK. Close Brothers Group plc's annual Pillar 3 prints UK KM1 with an 'Individual' block "
         "alongside the 'Group' block, and that Individual block IS Close Brothers Limited on the CRR "
         "article 9 individual-consolidation basis - the same basis as this workbook's other capital "
         "sheets, which is confirmed by its CET1, RWA and ratio rows agreeing cell-for-cell with the "
         "Strategic Report table those sheets already used. Rows 13 and 14 of that block give CBL's own "
         "leverage exposure measure and ratio for FY2022-FY2025. The old note's one true statement - "
         "that CBG plc also publishes a leverage ratio and that it is a different entity level - still "
         "holds, and the group figures (12.9% FY2025, 12.7% FY2024, 11.4% FY2023, 12.0% FY2022) are "
         "still NOT substituted here.\n"
         "FY2021 remains 'Not publicly disclosed' for CBL specifically: that year's Pillar 3 pre-dates "
         "the UK KM1 template, its section 3 'Key Regulatory Metrics' table is group-basis only (11.8% "
         "at 31 July 2021), and the FY2021 Annual Report's Note 21 'Capital' has no leverage row.\n"
         "BASIS: 'excluding claims on central banks' in every year printed. All four dates fall after "
         "the 1 January 2022 change that introduced that basis, so no basis break sits inside this "
         "series and no series has been merged across one.",
)

metric(
    "LCR", "%",
    [("Liquidity coverage ratio (12-month average)",
      {"FY2025": "943.2%", "FY2024": "930.1%", "FY2023": "1,106%", "FY2022": "885%",
       "FY2021": "Not publicly disclosed"})],
    P3_SOURCES + (
        "\n\nLCR is disclosed as a 12-MONTH AVERAGE in the Strategic Report's liquidity/funding risk "
        "section, not as a point-in-time year-end figure:\n"
        "FY2025 & FY2024: Annual Report 2025, Strategic Report liquidity section - " + AR2025_URL + "\n"
        "FY2023 & FY2022: Annual Report 2023, Strategic Report liquidity section - " + AR2023_URL + "\n"
        "FY2021: no LCR figure appears anywhere in the FY2021 filing - confirmed by OCR'ing all 147 "
        "pages and finding no occurrence of 'LCR' or 'liquidity coverage'.\n"
        "The FY2023 report states that for liquidity and funding ratios CBL is regulated by the PRA on "
        "an individual basis EXCLUDING subsidiary undertakings - a solo basis, narrower than the "
        "CBL-consolidated basis used for the capital figures above.\n\n"
        "PRECISION DIFFERS BETWEEN THE TWO DOCUMENTS THAT CARRY THESE SAME FIGURES, noted 2026-09-16 "
        "(KM1-010). The Annual Report rounds FY2023 to '1,106%' and FY2022 to '885%'; the corresponding "
        "Pillar 3 UK KM1 'Individual' column prints them to one decimal, 1,106.4% and 884.7%. The KM1 "
        "Key Metrics sheet carries the Pillar 3 printing and this sheet carries the Annual Report's, "
        "each as its own document has it; neither has been re-rounded to match the other. FY2025 and "
        "FY2024 are printed identically in both (943.2%, 930.1%).\n"
        "FY2021 stays 'Not publicly disclosed' for CBL specifically. Close Brothers Group plc's FY2021 "
        f"Pillar 3 does print a 12-month average LCR of 1,003% at section 3 ({CBG_P3_2021_URL}), but "
        "that is the CBG group figure; that edition carries no CBL-level liquidity disclosure, and the "
        "group figure is not substituted here."
    ),
    note="12-month average, not a year-end point-in-time figure. Solo (CBL individual) basis, which "
         "differs from the CBL-consolidated basis of the capital/RWA sheets. FY2023/FY2022 are the "
         "Annual Report's rounded printing; the Pillar 3 prints 1,106.4% and 884.7% - see source note.",
)

metric(
    "NSFR", "%",
    [("Net stable funding ratio (four-quarter average, except FY2022 - see note)",
      {"FY2025": "163.0%", "FY2024": "148.3%", "FY2023": "140.5%", "FY2022": "133.6%",
       "FY2021": "Not applicable"})],
    P3_SOURCES + (
        "\n\nNSFR is disclosed as a FOUR-QUARTER AVERAGE in the Strategic Report's funding risk section:\n"
        "FY2025 & FY2024: Annual Report 2025, Strategic Report funding section - " + AR2025_URL + "\n"
        "FY2023 & FY2022: Annual Report 2023, Strategic Report funding section - " + AR2023_URL + "\n"
        "FY2021: shown as 'Not applicable' rather than 'Not publicly disclosed' - the NSFR was only "
        "implemented by the PRA on 1 January 2022 (stated in both the FY2023 and FY2025 reports), which "
        "is after this bank's 31 July 2021 year end, so no NSFR existed to disclose for FY2021.\n"
        "Same solo (CBL individual, excluding subsidiaries) basis as the LCR - see that sheet.\n\n"
        "FY2022 IS A POINT-IN-TIME FIGURE IN A COLUMN OF AVERAGES, found 2026-09-16 (KM1-010) and "
        "recorded rather than reconciled. FY2023-FY2025 are four-quarter averages to the period end. "
        "FY2022 cannot be: Close Brothers Group plc's Pillar 3 Disclosures 2023 leaves KM1 rows 18, 19 "
        "and 20 EMPTY in its 31 July 2022 column and footnotes why - 'NSFR was implemented under CRR on "
        "1 January 2022 and as such no comparative has been provided for the four-quarter average to 31 "
        "July 2022. The point in time NSFR at 31 July 2022 was 118.3% for the CBG group and 133.6% for "
        f"CBL.' - {CBG_P3_2023_URL}. The 133.6% shown here is that footnoted CBL point-in-time figure, "
        "which is also what the FY2023 Annual Report prints as its FY2022 comparative. The KM1 Key "
        "Metrics sheet leaves FY2022 blank on rows 18-20, because that is what the template itself "
        "prints; the two sheets differ deliberately and neither has been changed to match the other."
    ),
    note="Four-quarter average for FY2023-FY2025, solo (CBL individual) basis. FY2022 is a POINT-IN-TIME "
         "NSFR, not a four-quarter average - no average was published for that date because the regime "
         "began part-way through the year; see the source note. FY2021 predates the PRA's 1 January 2022 "
         "implementation of the NSFR.",
)

metric(
    "MREL Ratio", "%",
    [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})],
    P3_SOURCES + (
        "\n\nMREL: no MREL figure or requirement is mentioned anywhere in any of the three filings - "
        "re-verified 2026-09-12 by full-document OCR search for 'MREL' and 'minimum requirement for own "
        "funds', zero hits across all 487 pages. MREL is set at the resolution-entity level, which for "
        "this group is the listed parent Close Brothers Group plc, not Close Brothers Limited.\n\n"
        "STRENGTHENED 2026-09-16 (KM1-010) from an absence to a positive statement by the bank itself. "
        "Close Brothers Group plc's Pillar 3 reaches template UK KM2 - 'Key metrics - MREL' - and "
        "declines to fill it in, in terms: 'The group does not have any additional MREL requirements "
        "Section 3A(4B) of the Banking Act 2009 so this template has not been presented' (Pillar 3 "
        "Disclosures 2025, printed p.6; the FY2022 edition words it 'Close Brothers does not have any "
        "additional MREL requirements as laid down in CRR articles 92a or 92b'). So the reason no MREL "
        "ratio appears for Close Brothers Limited is not that it is withheld or that we failed to find "
        "it: no additional MREL requirement is set above the group's own funds requirements, and the "
        "template is therefore omitted with the omission explained. Unlike the leverage ratio, UK KM2 "
        "has no 'Individual' block to read, because it has no columns at all in any edition. - "
        f"{CBG_P3_2025_URL}"
    ),
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
    note="Capital and liquidity ratios are disclosed at this entity level (Close Brothers Limited and its "
         "subsidiaries) in its own Annual Report's Strategic Report / Capital note - see the CET1 Ratio, "
         "Total Capital Ratio, LCR and NSFR sheets. The LEVERAGE RATIO is disclosed at this level too, for "
         "FY2022-FY2025 - correcting a statement that stood on this sheet until 2026-09-16 that it was not; "
         "it is published in the 'Individual' (CBL, CRR article 9) columns of Close Brothers Group plc's "
         "Pillar 3 UK KM1, which the earlier sweeps never read because they searched only the Companies "
         "House filings. See the Leverage Ratio and KM1 Key Metrics sheets. MREL is the one metric with no "
         "figure at this level, and for a stated reason: the group's Pillar 3 declines to present template "
         "UK KM2 because it has no additional MREL requirements under section 3A(4B) of the Banking Act "
         "2009 - see the MREL Ratio sheet. Cash flow figures are duplicated from the detail sheet for "
         "at-a-glance trend viewing.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/CLOSE BROTHERS FINANCIALS.xlsx")
