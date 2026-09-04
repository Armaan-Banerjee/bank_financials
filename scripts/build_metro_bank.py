import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

AR_2021 = "https://www.metrobankonline.co.uk/globalassets/documents/customer_documents/intermediaries/metro-bank-annual-report-2021.pdf"
AR_2022 = "https://www.metrobankonline.co.uk/globalassets/documents/customer_documents/business-and-commercial/metro-bank-annual-report-and-accounts-2022.pdf.pdf"
AR_2023 = "https://www.metrobankonline.co.uk/globalassets/documents/customer_documents/business-and-commercial/metro-bank-plc-annual-report-2023.pdf"
AR_2024 = "https://www.metrobankonline.co.uk/globalassets/documents/customer_documents/personal/metro-bank-annual-report-2024.pdf"
AR_2025 = "https://www.metrobankonline.co.uk/globalassets/documents/investor_documents/metro-bank---annual-report-2025.pdf"
P3_2021 = "https://www.metrobankonline.co.uk/globalassets/documents/customer_documents/intermediaries/metro-bank-pillar-3-disclosure-2021.pdf"
P3_H1_2022 = "https://www.metrobankonline.co.uk/globalassets/documents/customer_documents/business-and-commercial/pillar-3-disclosure---h1-2022.pdf"
P3_H1_2023 = "https://www.metrobankonline.co.uk/globalassets/documents/customer_documents/personal/pillar-3-disclosure-h1-2023.pdf"
P3_H1_2024 = "https://www.metrobankonline.co.uk/globalassets/documents/customer_documents/intermediaries/pillar-3-disclosure-h1-2024.pdf"
P3_H1_2025 = "https://www.metrobankonline.co.uk/globalassets/h1-2025-pillar-3-final.pdf"
P3_2022 = "https://www.metrobankonline.co.uk/globalassets/documents/customer_documents/business-and-commercial/pillar-3-disclosure-2022.pdf"
P3_2023 = "https://www.metrobankonline.co.uk/globalassets/pillar-3-disclosure-2023.pdf"
P3_2024 = "https://www.metrobankonline.co.uk/globalassets/pillar-3-2024.pdf"
P3_2025 = "https://www.metrobankonline.co.uk/globalassets/documents/investor_documents/pillar-3---2025-final.pdf"

ENTITY_NOTE = (
    "ENTITY/BASIS NOTE: Metro Bank PLC (Companies House 06419578; FRN 488982; LEI "
    "213800X5WU57YL9GPK89) is the matched legal entity in Banks List 2608.xlsx. "
    "FY2021-FY2023 cash flows are the Company/standalone figures from Metro Bank PLC "
    "accounts. Metro Bank PLC used an individual consolidation method for prudential "
    "reporting in 2021-2022. On 19 May 2023 Metro Bank Holdings PLC became the ultimate "
    "holding company; FY2023-FY2025 Pillar 3 disclosures are subsequently for Holdings "
    "and its subsidiaries, not standalone Metro Bank PLC. FY2024-FY2025 standalone Metro "
    "Bank PLC accounts/cash flows were not located in the reviewed official archive and "
    "are left blank rather than substituted with Holdings figures."
)

CASH_SOURCES = (
    "Sources - Metro Bank PLC Company/standalone cash flows, £m:\n"
    f"FY2023 & FY2022: Metro Bank PLC Annual Report 2023, p.147 (Company cash flow statement) - {AR_2023}\n"
    f"FY2022 & FY2021: Metro Bank PLC Annual Report and Accounts 2022, p.185 (Company column) - {AR_2022}\n"
    f"FY2021: Metro Bank PLC Annual Report and Accounts 2021, p.165 (Company column) - {AR_2021}\n\n"
    + ENTITY_NOTE
)

P3_SOURCES = (
    "Sources - Metro Bank regulatory key metrics:\n"
    f"FY2025: Metro Bank Holdings PLC Pillar 3 Disclosure 2025, p.10 - {P3_2025}\n"
    f"FY2024: Metro Bank Holdings PLC Pillar 3 Disclosure 2024, p.12 - {P3_2024}\n"
    f"FY2023: Metro Bank Holdings PLC Pillar 3 Disclosure 2023, p.12 - {P3_2023}\n"
    f"FY2022: Metro Bank PLC Pillar 3 Disclosure 2022, p.10 - {P3_2022}\n"
    f"FY2021: Metro Bank PLC Pillar 3 Disclosure 2021, p.4 - {P3_2021}\n\n"
    + ENTITY_NOTE
)

bw = BankWorkbook(bank_name="Metro Bank PLC", years=YEARS, year_label=YEAR_LABEL, header_color="00695C")

STATEMENTS_SOURCES = (
    "Sources - Metro Bank PLC statements, £m:\n"
    f"FY2025: Metro Bank Holdings PLC Annual Report and Accounts 2025, Consolidated income statement/balance sheet/statement of changes in equity, p.147-151 - {AR_2025}\n"
    f"FY2024: Metro Bank Holdings PLC Annual Report and Accounts 2024, Consolidated statement of comprehensive income/balance sheet/statement of changes in equity, p.161-164 - {AR_2024}\n"
    f"FY2023: Metro Bank PLC Annual Report 2023, Consolidated and Company statement of comprehensive income/balance sheet/statement of changes in equity, p.92-95 and p.144-146 - {AR_2023}\n"
    f"FY2022: Metro Bank PLC Annual Report and Accounts 2022, Consolidated and company statement of comprehensive income/balance sheets/statements of changes in equity, p.181-184 - {AR_2022}\n"
    f"FY2021: Metro Bank PLC Annual Report & Accounts 2021, Consolidated statement of comprehensive income/Consolidated and company balance sheets/statements of changes in equity, p.162-165 - {AR_2021}\n\n"
    + ENTITY_NOTE
    + "\n\nBASIS NOTE: Balance Sheet and Statement of Changes in Equity are shown on the same Company/standalone Metro "
    "Bank PLC basis as the Cash Flow Statement for FY2021-FY2023, and left blank for FY2024-FY2025 for the same reason "
    "(no standalone Metro Bank PLC accounts were located for those years - the 'Company' balance sheet published in the "
    "FY2024/FY2025 Annual Reports is Metro Bank Holdings PLC's own shell-company balance sheet, an investment-holding "
    "entity with ~£1.8bn/£1.9bn total assets dominated by 'Investment in subsidiaries', a fundamentally different entity "
    "from the ~£17-22bn banking entity Metro Bank PLC and not a defensible substitute; confirmed via Companies House "
    "filing history for Metro Bank PLC (06419578), which lists only 'Group of companies' accounts' for FY2024/FY2025, "
    "no standalone individual accounts). Profit & Loss is shown on a Group/consolidated basis for all 5 years, because "
    "Metro Bank PLC does not publish its own standalone income statement in any year reviewed (s.408 Companies Act 2006 "
    "exemption, available where consolidated accounts are also presented) - only a Company balance sheet, statement of "
    "changes in equity, and cash flow statement.\n\n"
    "DATA QUALITY FLAG: the FY2024 Annual Report's own FY2023 comparative column restates several FY2023 P&L and "
    "Balance Sheet figures from what AR2023 itself originally reported (e.g. Total operating expenses (585.2) vs "
    "AR2023's own (566.4); Total assets 22,245 vs AR2023's own 22,267; Total equity 1,134 vs AR2023's own 1,153) - this "
    "workbook uses each year's own contemporaneous figures (as AR2023 itself reported FY2023) rather than the later "
    "restated comparative, consistent with this project's standing convention."
)

cash_rows = [
    ("SECTION", "Reconciliation of profit/(loss) before tax to net cash flows from operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {"FY2023": 46, "FY2022": -71, "FY2021": -245}),
    ("DATA", "Adjustments for non-cash items", {"FY2023": -376, "FY2022": -259, "FY2021": -132}),
    ("DATA", "Interest received", {"FY2023": 834, "FY2022": 538, "FY2021": 394}),
    ("DATA", "Interest paid", {"FY2023": -370, "FY2022": -124, "FY2021": -126}),
    ("DATA", "Changes in other operating assets", {"FY2023": 729, "FY2022": -842, "FY2021": 2613}),
    ("DATA", "Changes in other operating liabilities", {"FY2023": -251, "FY2022": -409, "FY2021": 370}),
    ("TOTAL", "Net cash inflows/(outflows) from operating activities", {"FY2023": 612, "FY2022": -1167, "FY2021": 2874}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Sales of investment securities", {"FY2023": 1870, "FY2022": 857, "FY2021": 1269}),
    ("DATA", "Purchase of investment securities", {"FY2023": -816, "FY2022": -1206, "FY2021": -3438}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2023": -12, "FY2022": -29, "FY2021": -41}),
    ("DATA", "Purchase and development of intangible assets", {"FY2023": -26, "FY2022": -24, "FY2021": -64}),
    ("DATA", "Dividends received from subsidiaries", {"FY2023": 12}),
    ("TOTAL", "Net cash inflows/(outflows) from investing activities", {"FY2023": 1028, "FY2022": -402, "FY2021": -2274}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Repayment of capital elements of leases", {"FY2023": -23, "FY2022": -25, "FY2021": -27}),
    ("DATA", "Issuance of new shares", {"FY2023": 144}),
    ("DATA", "Issuance of medium-term notes/subordinated debt (net of costs)", {"FY2023": 175}),
    ("TOTAL", "Net cash inflows/(outflows) from financing activities", {"FY2023": 296, "FY2022": -25, "FY2021": -27}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2023": 1936, "FY2022": -1594, "FY2021": 573}),
    ("DATA", "Cash and cash equivalents at start of year", {"FY2023": 1953, "FY2022": 3547, "FY2021": 2974}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2023": 3889, "FY2022": 1953, "FY2021": 3547}),
]

bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances with the Bank of England", {"FY2023": 3889, "FY2022": 1953, "FY2021": 3547}),
    ("DATA", "Loans and advances to customers", {"FY2023": 11844, "FY2022": 12698, "FY2021": 11976}),
    ("DATA", "Investment securities held at FVOCI", {"FY2023": 476, "FY2022": 571, "FY2021": 798}),
    ("DATA", "Investment securities held at amortised cost", {"FY2023": 4403, "FY2022": 5343, "FY2021": 4776}),
    ("DATA", "Financial assets held at fair value through profit and loss", {"FY2022": 1, "FY2021": 3}),
    ("DATA", "Derivative financial assets", {"FY2023": 36, "FY2022": 23}),
    ("DATA", "Property, plant and equipment", {"FY2023": 723, "FY2022": 748, "FY2021": 765}),
    ("DATA", "Investment in subsidiaries", {"FY2023": 15, "FY2022": 31, "FY2021": 31}),
    ("DATA", "Intangible assets", {"FY2023": 188, "FY2022": 204, "FY2021": 231}),
    ("DATA", "Prepayments and accrued income", {"FY2023": 111, "FY2022": 80, "FY2021": 64}),
    ("DATA", "Assets classified as held for sale", {"FY2022": 1}),
    ("DATA", "Other assets", {"FY2023": 572, "FY2022": 473, "FY2021": 392}),
    ("TOTAL", "Total assets", {"FY2023": 22257, "FY2022": 22126, "FY2021": 22583}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from customers", {"FY2023": 15623, "FY2022": 16014, "FY2021": 16448}),
    ("DATA", "Deposits from central banks", {"FY2023": 3050, "FY2022": 3800, "FY2021": 3800}),
    ("DATA", "Debt securities", {"FY2023": 699, "FY2022": 571, "FY2021": 588}),
    ("DATA", "Repurchase agreements", {"FY2023": 1191, "FY2022": 238, "FY2021": 169}),
    ("DATA", "Derivative financial liabilities", {"FY2022": 26, "FY2021": 10}),
    ("DATA", "Lease liabilities", {"FY2023": 234, "FY2022": 248, "FY2021": 269}),
    ("DATA", "Deferred grants", {"FY2023": 16, "FY2022": 17, "FY2021": 19}),
    ("DATA", "Provisions", {"FY2023": 23, "FY2022": 7, "FY2021": 15}),
    ("DATA", "Deferred tax liability", {"FY2023": 13, "FY2022": 12, "FY2021": 12}),
    ("DATA", "Other liabilities", {"FY2023": 256, "FY2022": 236, "FY2021": 217}),
    ("TOTAL", "Total liabilities", {"FY2023": 21105, "FY2022": 21169, "FY2021": 21547}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called-up share capital", {}),
    ("DATA", "Share premium", {"FY2023": 144, "FY2022": 1964, "FY2021": 1964}),
    ("DATA", "Retained earnings/(losses)", {"FY2023": 996, "FY2022": -1014, "FY2021": -941}),
    ("DATA", "Other reserves", {"FY2023": 12, "FY2022": 7, "FY2021": 13}),
    ("TOTAL", "Total equity", {"FY2023": 1152, "FY2022": 957, "FY2021": 1036}),
    ("TOTAL", "Total equity and liabilities", {"FY2023": 22257, "FY2022": 22126, "FY2021": 22583}),
]

bw.add_balance_sheet_sheet(
    title="Metro Bank PLC - Balance Sheet",
    subtitle="Company/standalone basis, £m; 31 December year-end. FY2024-FY2025 not located (see source note) - "
              "same basis and gap as the Cash Flow Statement.",
    rows=bs_rows, sources_text=STATEMENTS_SOURCES, first_col_width=72, source_height=340, unit_suffix=" (£m)",
)

pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 725.4, "FY2024": 935.4, "FY2023": 855.7, "FY2022": 563.7, "FY2021": 405.7}),
    ("DATA", "Interest expense", {"FY2025": -265.1, "FY2024": -557.5, "FY2023": -443.8, "FY2022": -159.6, "FY2021": -110.4}),
    ("TOTAL", "Net interest income", {"FY2025": 460.3, "FY2024": 377.9, "FY2023": 411.9, "FY2022": 404.1, "FY2021": 295.3}),
    ("DATA", "Fee and commission income", {"FY2025": 96.7, "FY2024": 98.0, "FY2023": 95.0, "FY2022": 84.4, "FY2021": 71.2}),
    ("DATA", "Fee and commission expense", {"FY2025": -5.6, "FY2024": -4.8, "FY2023": -4.6, "FY2022": -2.6, "FY2021": -1.6}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 91.1, "FY2024": 93.2, "FY2023": 90.4, "FY2022": 81.8, "FY2021": 69.6}),
    ("DATA", "Net gain/(loss) on sale of assets", {"FY2025": 5.2, "FY2024": -101.4, "FY2023": 2.7, "FY2021": 9.4}),
    ("DATA", "Other income", {"FY2025": 36.7, "FY2024": 35.6, "FY2023": 143.9, "FY2022": 37.6, "FY2021": 44.2}),
    ("TOTAL", "Total income", {"FY2025": 593.3, "FY2024": 405.3, "FY2023": 648.9, "FY2022": 523.5, "FY2021": 418.5}),
    ("DATA", "General operating expenses", {"FY2025": -429.4, "FY2024": -489.0, "FY2023": -484.1, "FY2022": -467.6, "FY2021": -536.1}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -61.7, "FY2024": -77.3, "FY2023": -77.7, "FY2022": -77.0, "FY2021": -80.2}),
    ("DATA", "Impairment and write-offs of property, plant, equipment and intangible assets", {"FY2025": -0.7, "FY2024": -44.0, "FY2023": -4.6, "FY2022": -9.7, "FY2021": -24.9}),
    ("TOTAL", "Total operating expenses", {"FY2025": -491.8, "FY2024": -610.3, "FY2023": -566.4, "FY2022": -554.3, "FY2021": -641.2}),
    ("DATA", "Expected credit loss expense", {"FY2025": -14.3, "FY2024": -7.1, "FY2023": -33.2, "FY2022": -39.9, "FY2021": -22.4}),
    ("TOTAL", "Profit/(loss) before tax", {"FY2025": 87.2, "FY2024": -212.1, "FY2023": 49.3, "FY2022": -70.7, "FY2021": -245.1}),
    ("DATA", "Taxation credit/(expense)", {"FY2025": -17.5, "FY2024": 254.6, "FY2023": -1.0, "FY2022": -2.0, "FY2021": -3.1}),
    ("TOTAL", "Profit/(loss) for the year", {"FY2025": 69.7, "FY2024": 42.5, "FY2023": 48.3, "FY2022": -72.7, "FY2021": -248.2}),
    ("SECTION", "Other comprehensive income/(expense) for the year", {}),
    ("DATA", "Movement in investment securities held at FVOCI - changes in fair value (net of tax)", {"FY2025": 4.2, "FY2024": 3.4, "FY2023": 2.4, "FY2022": -7.6, "FY2021": -8.1}),
    ("DATA", "FV changes transferred to the income statement on disposal (net of tax)", {"FY2021": -0.3}),
    ("TOTAL", "Total other comprehensive income/(expense)", {"FY2025": 4.2, "FY2024": 3.4, "FY2023": 2.4, "FY2022": -7.6, "FY2021": -8.4}),
    ("TOTAL", "Total comprehensive income/(loss) for the year", {"FY2025": 73.9, "FY2024": 45.9, "FY2023": 50.7, "FY2022": -80.3, "FY2021": -256.6}),
]

bw.add_income_statement_sheet(
    title="Metro Bank PLC - Profit & Loss",
    subtitle="Group/consolidated basis, £m (Metro Bank PLC does not publish its own standalone income statement in "
              "any year reviewed - see source note).",
    rows=pl_rows, sources_text=STATEMENTS_SOURCES, first_col_width=78, source_height=340, unit_suffix=" (£m)",
)

equity_headers = ["Called-up share capital", "Share premium", "Retained earnings/(losses)", "FVOCI reserve",
                   "Share option reserve", "Deemed capital contribution", "Total equity"]
equity_rows = [
    ("TOTAL", "At 1 January 2021 (FY2021 opening)", (0, 1964, -689, 3, 16, None, 1294)),
    ("DATA", "Loss for the year", (None, None, -252, None, None, None, -252)),
    ("DATA", "Other comprehensive expense relating to investment securities designated at FVOCI, net of tax", (None, None, None, -8, None, None, -8)),
    ("DATA", "Net share option movements", (None, None, None, None, 2, None, 2)),
    ("TOTAL", "At 31 December 2021 (FY2021 closing)", (0, 1964, -941, -5, 18, None, 1036)),
    ("DATA", "Loss for the year", (None, None, -73, None, None, None, -73)),
    ("DATA", "Other comprehensive expense relating to investment securities designated at FVOCI, net of tax", (None, None, None, -8, None, None, -8)),
    ("DATA", "Net share option movements", (None, None, None, None, 2, None, 2)),
    ("TOTAL", "At 31 December 2022 (FY2022 closing)", (0, 1964, -1014, -13, 20, None, 957)),
    ("DATA", "Profit for the year", (None, None, 46, None, None, None, 46)),
    ("DATA", "Other comprehensive income relating to investment securities designated at FVOCI, net of tax", (None, None, None, 2, None, None, 2)),
    ("DATA", "Net share option movements", (None, None, None, None, 3, None, 3)),
    ("DATA", "Transfer of share option reserve upon insertion of new holding company", (None, None, None, None, -23, 23, 0)),
    ("DATA", "Cancellation of Metro Bank PLC share capital and share premium", (None, -1964, 1964, None, None, None, 0)),
    ("DATA", "Shares issued", (None, 144, None, None, None, None, 144)),
    ("TOTAL", "At 31 December 2023 (FY2023 closing)", (0, 144, 996, -11, 0, 23, 1152)),
]

bw.add_equity_changes_sheet(
    title="Metro Bank PLC - Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, Company/standalone basis, £m. FY2024-FY2025 not "
              "located - same basis and gap as the Balance Sheet and Cash Flow Statement. Equity reconciliation "
              "ladder confirmed: each year's own closing balance ties exactly to both the next year's own opening "
              "balance and that year's own Balance Sheet Total equity. The ladder's mandated scan caught the "
              "insertion of Metro Bank Holdings PLC as new ultimate parent in 2023 - a genuine cancellation of "
              "Metro Bank PLC's £1,964m share capital/premium (offset into retained earnings) and £144m of new "
              "shares issued, not a plug.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=46,
)

bw.add_cash_flow_sheet(
    title="Metro Bank PLC - Company Cash Flow Statement",
    subtitle="Company/standalone basis, £m; 31 December year-end. FY2024-FY2025 standalone accounts not located.",
    rows=cash_rows, sources_text=CASH_SOURCES, first_col_width=72, source_height=220, unit_suffix=" (£m)",
)

asset_quality_rows = [
    ("SECTION", "Gross carrying amount by portfolio, Group basis", {}),
    ("DATA", "Retail mortgages", {"FY2025": 4940, "FY2024": 5145, "FY2023": 7817, "FY2022": 7649, "FY2021": 6723}),
    ("DATA", "Consumer lending", {"FY2025": 114, "FY2024": 745, "FY2023": 1297, "FY2022": 1480, "FY2021": 890}),
    ("DATA", "Commercial / corporate and commercial lending", {"FY2025": 3939, "FY2024": 3314, "FY2023": 3382, "FY2022": 4160, "FY2021": 4846}),
    ("TOTAL", "Total loans and advances to customers, gross", {"FY2025": 8993, "FY2024": 9204, "FY2023": 12496, "FY2022": 13289, "FY2021": 12459}),
    ("DATA", "ECL allowance - retail mortgages", {"FY2025": -16, "FY2024": -15, "FY2023": -19, "FY2022": -20, "FY2021": -19}),
    ("DATA", "ECL allowance - consumer lending", {"FY2025": -67, "FY2024": -108, "FY2023": -108, "FY2022": -75, "FY2021": -42}),
    ("DATA", "ECL allowance - commercial / corporate and commercial lending", {"FY2025": -87, "FY2024": -68, "FY2023": -72, "FY2022": -92, "FY2021": -108}),
    ("TOTAL", "Total ECL allowance", {"FY2025": -170, "FY2024": -191, "FY2023": -199, "FY2022": -187, "FY2021": -169}),
    ("TOTAL", "Total loans and advances to customers, net", {"FY2025": 8823, "FY2024": 9013, "FY2023": 12297, "FY2022": 13102, "FY2021": 12290}),
    ("SECTION", "IFRS 9 stage split and coverage, portfolio-total level", {}),
    ("DATA", "Stage 1, gross carrying amount", {"FY2025": 7819, "FY2024": 7723}),
    ("DATA", "Stage 2, gross carrying amount", {"FY2025": 713, "FY2024": 978}),
    ("DATA", "Stage 3, gross carrying amount", {"FY2025": 462, "FY2024": 504}),
    ("DATA", "% loans in Stage 2", {"FY2025": "7.9%", "FY2024": "11%", "FY2023": "12%", "FY2022": "16%", "FY2021": "15%"}),
    ("DATA", "% loans in Stage 3", {"FY2025": "5.1%", "FY2024": "5%", "FY2023": "3%", "FY2022": "3%", "FY2021": "4%"}),
    ("DATA", "Coverage ratio (ECL allowance / gross lending, including Stage 3)", {"FY2025": "1.89%", "FY2024": "2.07%", "FY2023": "1.59%", "FY2022": "1.41%", "FY2021": "1.36%"}),
    ("DATA", "90+ days past due", {"FY2024": "3%", "FY2023": "2%", "FY2022": "1%", "FY2021": "2%"}),
    ("SECTION", "Non-performing loans (NPLs) by portfolio", {}),
    ("DATA", "Retail mortgages NPLs", {"FY2025": 220, "FY2024": 203, "FY2023": 146, "FY2022": 111, "FY2021": 114}),
    ("DATA", "Consumer NPLs", {"FY2025": 74, "FY2024": 97, "FY2023": 77, "FY2022": 50, "FY2021": 21}),
    ("DATA", "Commercial / corporate and commercial NPLs", {"FY2025": 168, "FY2024": 204, "FY2023": 166, "FY2022": 191, "FY2021": 327}),
    ("TOTAL", "Total NPLs", {"FY2025": 462, "FY2024": 504, "FY2023": 389, "FY2022": 352, "FY2021": 462}),
    ("DATA", "Total NPL ratio", {"FY2025": "5.14%", "FY2024": "5.48%", "FY2023": "3.11%", "FY2022": "2.65%", "FY2021": "3.71%"}),
]

bw.add_asset_quality_sheet(
    title="Metro Bank PLC - Asset Quality",
    subtitle="Group/consolidated basis, £m (Group loans and advances to customers ties exactly to the Consolidated "
              "Balance Sheet, not the Company balance sheet above - see source note).",
    rows=asset_quality_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nAsset Quality tables: FY2025 - AR2025 'Table 1' (Financial review, p.17) and Note 30 Expected credit "
        "loss (p.185-186); FY2024 - AR2024 'Table 1'/'Table 2'/'Table 3' (Financial risks, p.126-127) and Note 30; "
        "FY2023 - AR2023 'Table 1'/'Table 2'/'Table 3' (Financial risks, p.62-63); FY2022 - AR2022 'Table 1'/'Table "
        "2' (Risk report, p.72-74) and AR2023's FY2022 comparative for 'Table 3' NPLs by portfolio; FY2021 - AR2022's "
        "FY2021 comparative for 'Table 1'/'Table 2', and AR2021's own 'Table 1: Non-performing loans' (p.69).\n\n"
        "DATA QUALITY NOTE: FY2025's % Stage 2/% Stage 3 are computed here from Note 30's absolute Stage 1/2/3 gross "
        "carrying amounts (713/8,993 and 462/8,993) rather than a disclosed percentage - AR2025 stopped disclosing "
        "the FY2021-FY2024 'Table 2: Total portfolio credit performance' percentage table in that exact form. FY2025's "
        "90+ days past due percentage was not located in the reviewed disclosure and is left blank rather than "
        "estimated. 'Commercial lending' (FY2021-FY2024 label) and 'Corporate and commercial' (FY2025 label) are the "
        "same portfolio, simply relabelled between years."
    ),
    first_col_width=76,
    source_height=340,
    unit_suffix=" (£m)",
)


def vals(data):
    return {y: data.get(y) for y in YEARS}


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, P3_SOURCES, note=note, first_col_width=56, source_height=190)


metric("CET1 Capital", "£m", [("Common Equity Tier 1 (CET1) capital", vals({"FY2025": 840, "FY2024": 808, "FY2023": 985, "FY2022": 819, "FY2021": 936}))],
       "FY2023-FY2025 are Holdings Group figures following the May 2023 holding-company insertion; FY2021-FY2022 are Metro Bank PLC consolidated prudential figures. CORRECTED 2026-09-03 (ST-026): FY2023-FY2025 previously showed the 30 June interim KM1 column instead of the 31 December year-end column (e.g. FY2024 was 937, the 30 June 2024 figure - the year-end figure is 808); found while cross-checking against the RWA Breakdown sheet's own OV1/KM1 source tables. FY2021-FY2022 were already correct.")
metric("CET1 Ratio", "%", [("Common Equity Tier 1 ratio", vals({"FY2025": "12.5%", "FY2024": "12.5%", "FY2023": "13.1%", "FY2022": "10.3%", "FY2021": "12.6%"}))],
       "CORRECTED 2026-09-03 (ST-026): FY2023-FY2025 previously showed the 30 June interim column instead of 31 December year-end (see CET1 Capital sheet's note).")
metric("Tier 1 Capital", "£m", [("Tier 1 capital", vals({"FY2025": 1082, "FY2024": 808, "FY2023": 985, "FY2022": 819, "FY2021": 936}))],
       "CORRECTED 2026-09-03 (ST-026): FY2023-FY2025 previously showed the 30 June interim column instead of 31 December year-end (see CET1 Capital sheet's note).")
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", vals({"FY2025": "16.1%", "FY2024": "12.5%", "FY2023": "13.1%", "FY2022": "10.3%", "FY2021": "12.6%"}))],
       "CORRECTED 2026-09-03 (ST-026): FY2023-FY2025 previously showed the 30 June interim column instead of 31 December year-end (see CET1 Capital sheet's note).")
metric("Total Capital", "£m", [("Total capital", vals({"FY2025": 1232, "FY2024": 958, "FY2023": 1135, "FY2022": 1069, "FY2021": 1184}))],
       "CORRECTED 2026-09-03 (ST-026): FY2023-FY2025 previously showed the 30 June interim column instead of 31 December year-end (see CET1 Capital sheet's note).")
metric("Total Capital Ratio", "%", [("Total capital ratio", vals({"FY2025": "18.4%", "FY2024": "14.9%", "FY2023": "15.1%", "FY2022": "13.4%", "FY2021": "15.9%"}))],
       "CORRECTED 2026-09-03 (ST-026): FY2023-FY2025 previously showed the 30 June interim column instead of 31 December year-end (see CET1 Capital sheet's note).")
metric("Total RWAs", "£m", [("Total risk-weighted exposure amount", vals({"FY2025": 6711, "FY2024": 6442, "FY2023": 7533, "FY2022": 7990, "FY2021": 7454}))],
       "CORRECTED 2026-09-03 (ST-026): FY2023-FY2025 previously showed the 30 June interim column instead of 31 December year-end (e.g. FY2024 was 7239, the 30 June 2024 figure - the year-end figure is 6442, confirmed against both the KM1 Key metrics table and the OV1 RWA-by-risk-type table, and against the RWA Breakdown sheet's own total). FY2021-FY2022 were already correct.")

rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding counterparty credit risk)", vals({"FY2025": 5793, "FY2024": 5572, "FY2023": 6667, "FY2022": 7071, "FY2021": 6444})),
    ("DATA", "Counterparty credit risk", vals({"FY2025": 5, "FY2024": 19, "FY2023": 26, "FY2022": 9, "FY2021": 6})),
    ("DATA", "Securitisation exposures in the banking book (after the cap)", vals({"FY2025": 138, "FY2024": 124, "FY2023": 129, "FY2022": 166, "FY2021": 261})),
    ("DATA", "Market risk", vals({"FY2022": 0, "FY2021": 9})),
    ("DATA", "Operational risk", vals({"FY2025": 759, "FY2024": 720, "FY2023": 703, "FY2022": 739, "FY2021": 729})),
    ("DATA", "Amounts below the thresholds for deduction (subject to 250% risk weight)", vals({"FY2025": 16, "FY2024": 7, "FY2023": 8, "FY2022": 5, "FY2021": 5})),
    ("TOTAL", "Total", vals({"FY2025": 6711, "FY2024": 6442, "FY2023": 7533, "FY2022": 7990, "FY2021": 7454})),
]
bw.add_rwa_breakdown_sheet(
    title="Metro Bank PLC - RWA Breakdown",
    subtitle="Pillar 3 UK/EU OV1 template. FY2023-FY2025 are Holdings Group figures; FY2021-FY2022 are the Metro "
              "Bank PLC prudential perimeter (same basis split as the other Pillar 3 sheets).",
    rows=rwa_breakdown_rows,
    sources_text=P3_SOURCES + (
        "\n\nRWA Breakdown table: FY2025 - Pillar 3 Disclosure 2025, Table 6 UK OV1, p.12. FY2024 - Pillar 3 "
        "Disclosure 2024, Table 6 UK OV1, p.14. FY2023 - Pillar 3 Disclosure 2023, Table 6 UK OV1, p.14. FY2022 - "
        "Pillar 3 Disclosure 2022, Table 5 UK OV1, p.12. FY2021 - Pillar 3 Disclosure 2021, Table 10 EU OV1, p.52. "
        "All 5 years' totals tie exactly to the (corrected) Total RWAs sheet."
    ),
    first_col_width=68,
    source_height=250,
    unit_suffix=" (£m)",
)

metric("Leverage Ratio", "£m / %", [
    ("Total exposure measure excluding claims on central banks", vals({"FY2025": 13837, "FY2024": 14417, "FY2023": 18420, "FY2022": 19348, "FY2021": 17869})),
    ("Leverage ratio excluding claims on central banks", vals({"FY2025": "7.8%", "FY2024": "5.6%", "FY2023": "5.3%", "FY2022": "4.2%", "FY2021": "5.2%"})),
], note="The 2023-2025 figures are Holdings Group figures; 2021-2022 are the Metro Bank PLC prudential perimeter. The 2021-2022 disclosures restate the leverage measure to exclude central-bank claims for comparability. CORRECTED 2026-09-03 (ST-026): FY2023-FY2025 previously showed the 30 June interim column instead of 31 December year-end.")
metric("LCR", "£m / %", [
    ("Total high-quality liquid assets (HQLA), weighted value - average", vals({"FY2025": 5552, "FY2024": 7189, "FY2023": 5056, "FY2022": 6051, "FY2021": 6900})),
    ("Total net cash outflows, adjusted value", vals({"FY2025": 1773, "FY2024": 1854, "FY2023": 2079, "FY2022": 2465, "FY2021": 2169})),
    ("Liquidity Coverage Ratio", vals({"FY2025": "314%", "FY2024": "444%", "FY2023": "244%", "FY2022": "246%", "FY2021": "281%"})),
], note="The source tables disclose HQLA/net outflow components on different reporting bases across years; the headline ratios are reproduced as reported. Basis changes after the holding-company insertion are described on the Cash Flow Statement and source note. CORRECTED 2026-09-03 (ST-026): FY2023-FY2025 previously showed the 30 June interim column instead of 31 December year-end.")
metric("NSFR", "£m / %", [
    ("Total available stable funding", vals({"FY2025": 13965, "FY2024": 16676, "FY2023": 18277, "FY2022": 18903})),
    ("Total required stable funding", vals({"FY2025": 8448, "FY2024": 10475, "FY2023": 13442, "FY2022": 13225})),
    ("Net stable funding ratio", vals({"FY2025": "165%", "FY2024": "160%", "FY2023": "136%", "FY2022": "143%"})),
], note="NSFR disclosures were required from 1 January 2023; FY2021 is blank. FY2023-FY2025 are Holdings Group figures after the restructure. CORRECTED 2026-09-03 (ST-026): FY2023-FY2025 previously showed the 30 June interim column instead of 31 December year-end.")
metric("MREL Ratio", "%", [("MREL ratio", vals({"FY2021": "20.5%", "FY2022": "Not disclosed", "FY2023": "Not disclosed", "FY2024": "Not disclosed", "FY2025": "Not disclosed"}))],
       "The 2021 Pillar 3 report discloses 20.5%. No quantitative MREL ratio was located in the later KM1 tables reviewed; the 2022-2025 cells are therefore not publicly disclosed rather than zero.")


INTERIM_HEADERS = ["Period", "Disclosure type", "Metric", "Value", "Unit", "Basis", "Source document", "Page / table"]
INTERIM_METRICS = [
    ("CET1 capital", [1052, 816], "£m"),
    ("Tier 1 capital", [1052, 816], "£m"),
    ("Total capital", [1301, 1065], "£m"),
    ("Total risk-weighted exposure amount", [7563, 7702], "£m"),
    ("CET1 ratio", ["13.9%", "10.6%"], "%"),
    ("Tier 1 ratio", ["13.9%", "10.6%"], "%"),
    ("Total capital ratio", ["17.2%", "13.8%"], "%"),
    ("Total exposure measure excluding claims on central banks", [16909, 18809], "£m"),
    ("Leverage ratio excluding claims on central banks", ["6.2%", "4.3%"], "%"),
    ("Total HQLA, weighted value - average", [None, 6687], "£m"),
    ("Total net cash outflows, adjusted value", [None, 2374], "£m"),
    ("Liquidity coverage ratio", [None, "282%"], "%"),
    ("Total available stable funding", ["Not yet required", "Not disclosed"], "£m"),
    ("Total required stable funding", ["Not yet required", "Not disclosed"], "£m"),
    ("NSFR ratio", ["Not yet required", "Not disclosed"], "%"),
    ("MREL ratio", ["Not disclosed", "Not disclosed"], "%"),
]
interim_rows = []
for period, values, source, page in [
    ("30 Jun 2021", 0, P3_H1_2022, "3, UK KM1"),
    ("30 Jun 2022", 1, P3_H1_2022, "3, UK KM1"),
]:
    for metric_name, metric_values, unit in INTERIM_METRICS:
        interim_rows.append([period, "H1 Pillar 3 disclosure", metric_name, metric_values[values], unit, "Metro Bank PLC consolidated basis", source, page])
for period, source in [("30 Jun 2023", P3_H1_2023), ("30 Jun 2024", P3_H1_2024), ("30 Jun 2025", P3_H1_2025)]:
    interim_rows.append([period, "H1 Pillar 3 disclosure", "All Metro Bank PLC entity-level interim metrics", "Not separately disclosed", "n/a", "Metro Bank Holdings PLC group disclosure after 19 May 2023 restructure", source, "Basis note"])

bw.add_wide_interim_sheet(
    "Interim Pillar 3", rows=interim_rows,
    hyperlink_cells={(i, 6): row[6] for i, row in enumerate(interim_rows)},
    title="Metro Bank PLC - Interim Pillar 3 Disclosures",
    subtitle="Entity-level Metro Bank PLC basis where available; later Holdings Group disclosures are not substituted.",
    note="H1 2021 and H1 2022 use the official Metro Bank PLC consolidated UK KM1 table. From 19 May 2023 the ultimate holding company changed to Metro Bank Holdings PLC; H1 2023-H1 2025 official disclosures are Holdings Group figures and do not provide a defensible standalone Metro Bank PLC series, so those periods are explicitly recorded as not separately disclosed.",
)


def cash_value(label):
    return next(v for kind, name, v in cash_rows if name == label)


def bs_value(label):
    return next(v for kind, name, v in bs_rows if name == label)


def pl_value(label):
    return next(v for kind, name, v in pl_rows if name == label)


equity_summary = {
    "FY2021": {"Opening equity": 1294, "Total comprehensive loss for the year": -260, "Other equity movements, net": 2, "Closing equity": 1036},
    "FY2022": {"Opening equity": 1036, "Total comprehensive loss for the year": -81, "Other equity movements, net": 2, "Closing equity": 957},
    "FY2023": {"Opening equity": 957, "Total comprehensive income for the year": 48, "Other equity movements, net": 147, "Closing equity": 1152},
}

bw.add_overview_sheet(
    cash_flow_totals=[(label, cash_value(label)) for label in [
        "Net cash inflows/(outflows) from operating activities",
        "Net cash inflows/(outflows) from investing activities",
        "Net cash inflows/(outflows) from financing activities",
        "Cash and cash equivalents at end of year",
    ]],
    cash_flow_unit="£m",
    balance_sheet_totals=[(label, bs_value(label)) for label in [
        "Total assets",
        "Loans and advances to customers",
        "Deposits from customers",
        "Total equity",
    ]],
    balance_sheet_unit="£m",
    income_statement_totals=[(label, pl_value(label)) for label in [
        "Total income",
        "Total operating expenses",
        "Profit/(loss) before tax",
        "Profit/(loss) for the year",
    ]],
    income_statement_unit="£m",
    equity_changes_totals=[
        (label, {y: equity_summary[y].get(label) for y in ["FY2023", "FY2022", "FY2021"]})
        for label in ["Opening equity", "Total comprehensive income for the year", "Total comprehensive loss for the year", "Other equity movements, net", "Closing equity"]
    ],
    equity_changes_unit="£m",
    ratios=[
        ("CET1 Ratio", vals({"FY2025": "12.5%", "FY2024": "12.5%", "FY2023": "13.1%", "FY2022": "10.3%", "FY2021": "12.6%"})),
        ("Total Capital Ratio", vals({"FY2025": "18.4%", "FY2024": "14.9%", "FY2023": "15.1%", "FY2022": "13.4%", "FY2021": "15.9%"})),
        ("Leverage Ratio", vals({"FY2025": "7.8%", "FY2024": "5.6%", "FY2023": "5.3%", "FY2022": "4.2%", "FY2021": "5.2%"})),
        ("LCR", vals({"FY2025": "314%", "FY2024": "444%", "FY2023": "244%", "FY2022": "246%", "FY2021": "281%"})),
        ("NSFR", vals({"FY2025": "165%", "FY2024": "160%", "FY2023": "136%", "FY2022": "143%"})),
    ],
    note="Metro Bank PLC entity basis. Balance Sheet/Equity Changes summaries are Company/standalone (FY2024-FY2025 "
         "blank - no standalone Metro Bank PLC accounts located); Profit & Loss summary is Group/consolidated "
         "(Metro Bank PLC does not publish its own income statement); cash-flow is Company/standalone with the same "
         "FY2024-FY2025 gap. Regulatory ratios change from Metro Bank PLC consolidated basis to Holdings Group basis "
         "after the 19 May 2023 restructure; see the metric and interim-sheet notes. Regulatory figures for "
         "FY2023-FY2025 were corrected 2026-09-03 (ST-026) - see the Total RWAs sheet's note.",
)

bw.save("/Users/armaan/code/katalysis/banks/METRO BANK FINANCIALS.xlsx")
