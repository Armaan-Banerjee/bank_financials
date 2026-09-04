import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, all 12mo to 31 Dec
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2025/annual/pdfs/hsbc-bank-plc/260225-annual-report-and-accounts-2025.pdf"
AR2024_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2024/annual/pdfs/hsbc-bank-plc/250219-annual-report-and-accounts-2024.pdf"
AR2023_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2023/annual/pdfs/hsbc-bank-plc/240221-annual-report-and-accounts-2023.pdf"
AR2022_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2022/annual/pdfs/hsbc-bank-plc/230221-annual-report-and-accounts-2022.pdf"
AR2021_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2021/annual/pdfs/hsbc-bank-plc/220222-annual-report-and-accounts-2021.pdf"

P32025_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2025/annual/pdfs/hsbc-bank-plc/260225-pillar-3-disclosures-at-31-december-2025.pdf"
P32024_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2024/annual/pdfs/hsbc-bank-plc/250219-pillar-3-disclosures-at-31-december-2024.pdf"
P32023_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2023/annual/pdfs/hsbc-bank-plc/240221-pillar-3-disclosures-31-december-2023.pdf"
P32022_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2022/annual/pdfs/hsbc-bank-plc/230221-pillar-3-disclosures-31-december-2022.pdf"
P32021_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2021/annual/pdfs/hsbc-bank-plc/220222-pillar-3-disclosures-at-31-december-2021.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: HSBC Bank plc (Companies House 00014259, FRN 114216) is HSBC's legacy UK/international "
    "non-ring-fenced banking entity - confirmed distinct from HSBC UK Bank plc (FRN 765112, the ring-fenced "
    "retail bank created 2018 under UK ring-fencing reform, not attempted in this project as of this build), "
    "HSBC Holdings plc (the ultimate listed parent, out of scope), and HSBC Innovation Bank Limited (FRN "
    "543146, the former Silicon Valley Bank UK, built separately in this same batch - see 'HSBC INNOVATION "
    "BANK FINANCIALS.xlsx'). All figures below are HSBC Bank plc's own entity-level Consolidated (i.e. HSBC "
    "Bank plc and its own subsidiaries, not the wider HSBC Holdings plc Group) statements, sourced directly "
    "from HSBC Bank plc's own Annual Report and Accounts and Pillar 3 Disclosures, published on hsbc.com's "
    "investor-relations 'Subsidiaries' reporting archive (a company-house style lookup was blocked at the DNS "
    "level in this session; hsbc.com itself was fully reachable). Both a 2023 IFRS 17 'Insurance Contracts' "
    "adoption and a late-2022 change to how non-financial-institution subsidiary investments are measured "
    "triggered real, source-disclosed restatements of prior-year comparatives - per this project's convention, "
    "every year below uses that year's own originally-published figures, not a later restated comparative; "
    "both restatements are individually noted where they bite."
)

CASH_FLOW_NOTE = (
    "CASH FLOW NOTE: figures are £m (this is one of the largest entities in this project by balance sheet "
    "size; £'000 would be unwieldy). The full opening-to-closing cash chain reconciles exactly year-to-year "
    "using each year's own originally-published figures (FY2021 closing £140,923m = FY2022 opening; FY2022 "
    "closing £189,907m = FY2023 opening; FY2023 closing £177,037m = FY2024 opening; FY2024 closing £162,928m "
    "= FY2025 opening) despite the IFRS 17 restatement below only affecting the 'Profit/(loss) before tax' "
    "and adjustment-line presentation for FY2022, not the underlying cash totals. One row's label was "
    "corrected between reports for the same figure: FY2022's own Annual Report labelled the £628m financing "
    "line 'redemption of preference shares and other equity instruments' (a positive value, inconsistent with "
    "'redemption'), which the FY2023 Annual Report's FY2022 comparative column relabels 'issue of ordinary "
    "share capital and other equity instruments' - matching the £628m 'Capital securities issued during the "
    "period' shown in FY2022's own statement of changes in equity. The corrected label and FY2022's own "
    "originally-published £628m value are both used here."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are HSBC Bank plc's own Consolidated Statement of Cash Flows, £m, from each year's "
    "own Annual Report and Accounts (each year's own originally-published figures, not a later restated "
    "comparative):\n"
    f"FY2025: HSBC Bank plc Annual Report and Accounts 2025, p.95 (Consolidated statement of cash flows) - {AR2025_URL}\n"
    f"FY2024: HSBC Bank plc Annual Report and Accounts 2024, p.121 (Consolidated statement of cash flows) - {AR2024_URL}\n"
    f"FY2023: HSBC Bank plc Annual Report and Accounts 2023, p.112-113 (Consolidated statement of cash flows) - {AR2023_URL}\n"
    f"FY2022: HSBC Bank plc Annual Report and Accounts 2022, p.117 (Consolidated statement of cash flows) - {AR2022_URL}\n"
    f"FY2021: HSBC Bank plc Annual Report and Accounts 2021, p.111 (Consolidated statement of cash flows) - {AR2021_URL}\n\n"
    + CASH_FLOW_NOTE + "\n\n" + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - HSBC Bank plc's own entity-level Pillar 3 Disclosures, Table 1 'Key metrics (KM1/IFRS9-FL)' "
        "(FY2022-FY2025) or the equivalent 'Comparison of own funds, capital and leverage ratios' / 'Overview "
        "of RWAs' tables (FY2021, which pre-dates the KM1 template), each year's own originally-published "
        "figures at 31 December:\n"
        f"FY2025: HSBC Bank plc Pillar 3 Disclosures at 31 December 2025, p.3 - {P32025_URL}\n"
        f"FY2024: HSBC Bank plc Pillar 3 Disclosures at 31 December 2024, p.3 - {P32024_URL}\n"
        f"FY2023: HSBC Bank plc Pillar 3 Disclosures at 31 December 2023, p.4 - {P32023_URL}\n"
        f"FY2022: HSBC Bank plc Pillar 3 Disclosures at 31 December 2022, p.2 - {P32022_URL}\n"
        f"FY2021: HSBC Bank plc Pillar 3 Disclosures at 31 December 2021, p.2-3 (Tables 1 and 2) - {P32021_URL}\n\n"
        + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="HSBC Bank plc", years=YEARS, year_label=YEAR_LABEL, header_color="8602AA")

IFRS17_NOTE = (
    "IFRS 17 NOTE: HSBC Bank plc adopted IFRS 17 'Insurance Contracts' (replacing IFRS 4) from 1 January 2023, "
    "and separately changed how non-financial-institution subsidiary investments are measured from 30 September "
    "2022. Both changes restated later-published comparatives for FY2022 and FY2021, but per this project's "
    "convention every year below uses that year's own originally-published figures (e.g. FY2022's own £(959)m "
    "Profit/(loss) before tax and £(398)m Profit/(loss) for the year, not the £(1,199)m/£(553)m later-restated "
    "IFRS 17 comparative shown in the FY2023 Annual Report). This creates one genuine, source-disclosed equity "
    "discontinuity between FY2022's own closing Total equity (£24,016m) and FY2023's own opening Total equity "
    "(£23,233m, on the restated basis) - bridged below with an explicit 'IFRS 17 transition restatement' row "
    "rather than force-reconciled, since it is a real basis change, not a transcription error."
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 101443, "FY2024": 119184, "FY2023": 110618, "FY2022": 131433, "FY2021": 108482}),
    ("DATA", "Items in the course of collection from other banks", {"FY2023": 2114, "FY2022": 2285, "FY2021": 346}),
    ("DATA", "Trading assets", {"FY2025": 131359, "FY2024": 116042, "FY2023": 100696, "FY2022": 79878, "FY2021": 83706}),
    ("DATA", "Financial assets designated and otherwise mandatorily measured at fair value through profit or loss", {"FY2025": 5752, "FY2024": 9417, "FY2023": 19068, "FY2022": 15881, "FY2021": 18649}),
    ("DATA", "Derivatives", {"FY2025": 168585, "FY2024": 198172, "FY2023": 174116, "FY2022": 225238, "FY2021": 141221}),
    ("DATA", "Loans and advances to banks", {"FY2025": 19349, "FY2024": 14521, "FY2023": 14371, "FY2022": 17109, "FY2021": 10784}),
    ("DATA", "Loans and advances to customers", {"FY2025": 79858, "FY2024": 82666, "FY2023": 75491, "FY2022": 72614, "FY2021": 91177}),
    ("DATA", "Reverse repurchase agreements - non-trading", {"FY2025": 68110, "FY2024": 53612, "FY2023": 73494, "FY2022": 53949, "FY2021": 54448}),
    ("DATA", "Financial investments", {"FY2025": 66614, "FY2024": 52216, "FY2023": 46368, "FY2022": 32604, "FY2021": 41300}),
    ("DATA", "Assets held for sale", {"FY2025": 5558, "FY2024": 21606, "FY2023": 20368, "FY2022": 21214}),
    ("DATA", "Prepayments, accrued income and other assets", {"FY2025": 58617, "FY2024": 56950, "FY2023": 63635, "FY2022": 61379, "FY2021": 43127}),
    ("DATA", "Current tax assets", {"FY2025": 463, "FY2024": 1043, "FY2023": 485, "FY2022": 595, "FY2021": 1135}),
    ("DATA", "Interests in associates and joint ventures", {"FY2025": 769, "FY2024": 703, "FY2023": 665, "FY2022": 728, "FY2021": 743}),
    ("DATA", "Goodwill and intangible assets", {"FY2025": 276, "FY2024": 303, "FY2023": 203, "FY2022": 1167, "FY2021": 894}),
    ("DATA", "Deferred tax assets", {"FY2025": 943, "FY2024": 895, "FY2023": 1278, "FY2022": 1279, "FY2021": 599}),
    ("TOTAL", "Total assets", {"FY2025": 707696, "FY2024": 727330, "FY2023": 702970, "FY2022": 717353, "FY2021": 596611}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2025": 39679, "FY2024": 26515, "FY2023": 22943, "FY2022": 20836, "FY2021": 32188}),
    ("DATA", "Customer accounts", {"FY2025": 244763, "FY2024": 242303, "FY2023": 222941, "FY2022": 215948, "FY2021": 205241}),
    ("DATA", "Repurchase agreements - non-trading", {"FY2025": 46758, "FY2024": 40384, "FY2023": 53416, "FY2022": 32901, "FY2021": 27259}),
    ("DATA", "Items in the course of transmission to other banks", {"FY2023": 2116, "FY2022": 2226, "FY2021": 489}),
    ("DATA", "Trading liabilities", {"FY2025": 41877, "FY2024": 42633, "FY2023": 42276, "FY2022": 41265, "FY2021": 46433}),
    ("DATA", "Financial liabilities designated at fair value", {"FY2025": 41842, "FY2024": 37443, "FY2023": 32545, "FY2022": 27287, "FY2021": 33608}),
    ("DATA", "Derivatives", {"FY2025": 166666, "FY2024": 197082, "FY2023": 171474, "FY2022": 218867, "FY2021": 139368}),
    ("DATA", "Debt securities in issue", {"FY2025": 12823, "FY2024": 19461, "FY2023": 13443, "FY2022": 7268, "FY2021": 9428}),
    ("DATA", "Liabilities of disposal groups held for sale", {"FY2025": 15711, "FY2024": 23110, "FY2023": 20684, "FY2022": 24711}),
    ("DATA", "Accruals, deferred income and other liabilities", {"FY2025": 50458, "FY2024": 50484, "FY2023": 60444, "FY2022": 66945, "FY2021": 43456}),
    ("DATA", "Current tax liabilities", {"FY2025": 266, "FY2024": 250, "FY2023": 272, "FY2022": 130, "FY2021": 97}),
    ("DATA", "Insurance contract liabilities", {"FY2025": 465, "FY2024": 3424, "FY2023": 20595, "FY2022": 19987, "FY2021": 22264}),
    ("DATA", "Provisions", {"FY2025": 1500, "FY2024": 275, "FY2023": 390, "FY2022": 424, "FY2021": 562}),
    ("DATA", "Deferred tax liabilities", {"FY2025": 5, "FY2024": 5, "FY2023": 6, "FY2022": 14, "FY2021": 15}),
    ("DATA", "Subordinated liabilities", {"FY2025": 18919, "FY2024": 16908, "FY2023": 14920, "FY2022": 14528, "FY2021": 12488}),
    ("TOTAL", "Total liabilities", {"FY2025": 681732, "FY2024": 700277, "FY2023": 678465, "FY2022": 693337, "FY2021": 572896}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 797, "FY2024": 797, "FY2023": 797, "FY2022": 797, "FY2021": 797}),
    ("DATA", "Share premium account", {"FY2025": 3582, "FY2024": 3582, "FY2023": 1004, "FY2022": 420}),
    ("DATA", "Other equity instruments", {"FY2025": 4197, "FY2024": 3921, "FY2023": 3930, "FY2022": 3930, "FY2021": 3722}),
    ("DATA", "Retained earnings", {"FY2025": 22376, "FY2024": 25040, "FY2023": 24724, "FY2022": 25096, "FY2021": 24735}),
    ("DATA", "Other reserves", {"FY2025": -5151, "FY2024": -6445, "FY2023": -6096, "FY2022": -6368, "FY2021": -5670}),
    ("TOTAL", "Total shareholders' equity", {"FY2025": 25801, "FY2024": 26895, "FY2023": 24359, "FY2022": 23875, "FY2021": 23584}),
    ("DATA", "Non-controlling interests", {"FY2025": 163, "FY2024": 158, "FY2023": 146, "FY2022": 141, "FY2021": 131}),
    ("TOTAL", "Total equity", {"FY2025": 25964, "FY2024": 27053, "FY2023": 24505, "FY2022": 24016, "FY2021": 23715}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 707696, "FY2024": 727330, "FY2023": 702970, "FY2022": 717353, "FY2021": 596611}),
]

BALANCE_SHEET_SOURCES = (
    "Sources - HSBC Bank plc's own Consolidated balance sheet, £m, from each year's own Annual Report and "
    "Accounts (each year's own originally-published figures, not a later restated comparative):\n"
    f"FY2025: HSBC Bank plc Annual Report and Accounts 2025, p.92-93 - {AR2025_URL}\n"
    f"FY2024: HSBC Bank plc Annual Report and Accounts 2024, p.117 - {AR2024_URL}\n"
    f"FY2023: HSBC Bank plc Annual Report and Accounts 2023, p.108 - {AR2023_URL}\n"
    f"FY2022: HSBC Bank plc Annual Report and Accounts 2022, p.116 - {AR2022_URL}\n"
    f"FY2021: HSBC Bank plc Annual Report and Accounts 2021, p.110 - {AR2021_URL}\n\n"
    "'Items in the course of collection/transmission from other banks' were reported as separate balance sheet "
    "lines through FY2023, then merged into 'Prepayments, accrued income and other assets' / 'Accruals, "
    "deferred income and other liabilities' from FY2024 onward per the Bank's own disclosed presentation "
    "change - left blank for FY2025/FY2024 rather than force-split. 'Share premium account' was not reported "
    "as a line separate from 'Called up share capital' until FY2022 - left blank for FY2021. 'Assets/Liabilities "
    "held for sale' did not exist as a line in FY2021 (introduced FY2022) - left blank. Goodwill and intangible "
    "assets shows a genuine large swing between FY2022's own figure (£1,167m) and the later IFRS 17-restated "
    "FY2022 comparative (£91m, shown in the FY2023 report) due to a VOBA/PVIF insurance intangible "
    "reclassification - FY2022's own originally-published figure is used here.\n\n"
    + ENTITY_NOTE + "\n\n" + IFRS17_NOTE
)

bw.add_balance_sheet_sheet(
    title="HSBC Bank plc — Consolidated Balance Sheet",
    subtitle="HSBC Bank plc consolidated (entity-level, not the wider HSBC Holdings plc Group), £m. See source note at bottom.",
    rows=balance_sheet_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=82,
    source_height=340,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Net interest income", {"FY2025": 1274, "FY2024": 985, "FY2023": 2151, "FY2022": 1904, "FY2021": 1754}),
    ("DATA", "- interest income", {"FY2025": 16081, "FY2024": 19414, "FY2023": 17782, "FY2022": 6535, "FY2021": 3149}),
    ("DATA", "- interest expense", {"FY2025": -14807, "FY2024": -18429, "FY2023": -15631, "FY2022": -4631, "FY2021": -1395}),
    ("DATA", "Net fee income", {"FY2025": 1227, "FY2024": 1275, "FY2023": 1229, "FY2022": 1261, "FY2021": 1413}),
    ("DATA", "- fee income", {"FY2025": 2921, "FY2024": 2758, "FY2023": 2594, "FY2022": 2606, "FY2021": 2706}),
    ("DATA", "- fee expense", {"FY2025": -1694, "FY2024": -1483, "FY2023": -1365, "FY2022": -1345, "FY2021": -1293}),
    ("DATA", "Net income from financial instruments held for trading or managed on a fair value basis", {"FY2025": 4938, "FY2024": 4726, "FY2023": 3395, "FY2022": 2875, "FY2021": 1733}),
    ("DATA", "Net income/(expense) from assets and liabilities of insurance businesses (IFRS 17, FY2023 on)", {"FY2025": 1017, "FY2024": 857, "FY2023": 1168, "FY2022": -1369}),
    ("DATA", "Changes in fair value of long-term debt and related derivatives", {"FY2025": -4, "FY2024": 2, "FY2023": -63, "FY2022": 102, "FY2021": -8}),
    ("DATA", "Changes in fair value of other financial instruments mandatorily measured at FVTPL", {"FY2025": 288, "FY2024": 413, "FY2023": 284, "FY2022": 143, "FY2021": 493}),
    ("DATA", "Net (losses)/gains from financial investments", {"FY2025": -1088, "FY2024": 22, "FY2023": -84, "FY2022": -60, "FY2021": 60}),
    ("DATA", "Net insurance premium income (IFRS 4, pre-FY2023)", {"FY2022": 1787, "FY2021": 1906}),
    ("DATA", "(Losses)/gains recognised on Assets held for sale", {"FY2025": -6, "FY2024": -100, "FY2023": 296, "FY2022": -1947}),
    ("DATA", "Insurance finance (expense)/income (IFRS 17, FY2023 on)", {"FY2025": -1090, "FY2024": -984, "FY2023": -1184}),
    ("DATA", "Insurance service result (IFRS 17, FY2023 on)", {"FY2025": 164, "FY2024": 171, "FY2023": 124}),
    ("DATA", "Other operating income", {"FY2025": 158, "FY2024": 106, "FY2023": 190, "FY2022": 356, "FY2021": 594}),
    ("TOTAL", "Total operating income (IFRS 4 presentation, pre-FY2023)", {"FY2022": 5052, "FY2021": 9159}),
    ("DATA", "Net insurance claims, benefits paid and movement in liabilities to policyholders (IFRS 4, pre-FY2023)", {"FY2022": -406, "FY2021": -3039}),
    ("TOTAL", "Net operating income before change in expected credit losses", {"FY2025": 6878, "FY2024": 7473, "FY2023": 7506, "FY2022": 4646, "FY2021": 6120}),
    ("DATA", "Change in expected credit losses and other credit impairment charges", {"FY2025": -154, "FY2024": -163, "FY2023": -169, "FY2022": -222, "FY2021": 174}),
    ("TOTAL", "Net operating income", {"FY2025": 6724, "FY2024": 7310, "FY2023": 7337, "FY2022": 4424, "FY2021": 6294}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Employee compensation and benefits", {"FY2025": -1983, "FY2024": -1672, "FY2023": -1706, "FY2022": -1762, "FY2021": -2023}),
    ("DATA", "General and administrative expenses", {"FY2025": -4363, "FY2024": -3440, "FY2023": -3375, "FY2022": -3463, "FY2021": -3265}),
    ("DATA", "Depreciation and impairment of PP&E and right-of-use assets", {"FY2025": -125, "FY2024": -71, "FY2023": -45, "FY2022": -103, "FY2021": -110}),
    ("DATA", "Amortisation and impairment of intangible assets", {"FY2025": -433, "FY2024": -77, "FY2023": -16, "FY2022": -25, "FY2021": -64}),
    ("TOTAL", "Total operating expenses", {"FY2025": -6904, "FY2024": -5260, "FY2023": -5142, "FY2022": -5353, "FY2021": -5462}),
    ("TOTAL", "Operating (loss)/profit", {"FY2025": -180, "FY2024": 2050, "FY2023": 2195, "FY2022": -929, "FY2021": 832}),
    ("DATA", "Share of profit/(loss) in associates and joint ventures", {"FY2025": 61, "FY2024": 18, "FY2023": -43, "FY2022": -30, "FY2021": 191}),
    ("TOTAL", "(Loss)/profit before tax", {"FY2025": -119, "FY2024": 2068, "FY2023": 2152, "FY2022": -959, "FY2021": 1023}),
    ("DATA", "Tax (charge)/credit", {"FY2025": -462, "FY2024": -785, "FY2023": -427, "FY2022": 561, "FY2021": 23}),
    ("TOTAL", "(Loss)/profit for the year", {"FY2025": -581, "FY2024": 1283, "FY2023": 1725, "FY2022": -398, "FY2021": 1046}),
    ("DATA", "- attributable to the parent company", {"FY2025": -591, "FY2024": 1253, "FY2023": 1703, "FY2022": -408, "FY2021": 1041}),
    ("DATA", "- attributable to non-controlling interests", {"FY2025": 10, "FY2024": 30, "FY2023": 22, "FY2022": 10, "FY2021": 5}),
    ("SECTION", "Other comprehensive income, net of tax", {}),
    ("DATA", "Debt instruments at fair value through other comprehensive income", {"FY2025": 830, "FY2024": 144, "FY2023": 439, "FY2022": -454, "FY2021": -237}),
    ("DATA", "Equity instruments designated at fair value through other comprehensive income", {"FY2025": 17, "FY2024": -2, "FY2023": -1, "FY2022": 0, "FY2021": 2}),
    ("DATA", "Cash flow hedges", {"FY2025": 209, "FY2024": 103, "FY2023": 663, "FY2022": -943, "FY2021": -165}),
    ("DATA", "Finance (expense)/income from insurance contracts (IFRS 17, FY2023 on)", {"FY2025": -510, "FY2024": -108, "FY2023": -298}),
    ("DATA", "Exchange differences", {"FY2025": 754, "FY2024": -491, "FY2023": -302, "FY2022": 701, "FY2021": -603}),
    ("DATA", "Remeasurement of defined benefit asset/liability", {"FY2025": 44, "FY2024": -2, "FY2023": -2, "FY2022": 38, "FY2021": 44}),
    ("DATA", "Changes in fair value of financial liabilities designated at FV due to own credit risk", {"FY2025": -127, "FY2024": -40, "FY2023": -132, "FY2022": 329, "FY2021": 2}),
    ("TOTAL", "Other comprehensive income/(expense) for the year, net of tax", {"FY2025": 1217, "FY2024": -396, "FY2023": 367, "FY2022": -329, "FY2021": -957}),
    ("TOTAL", "Total comprehensive income/(expense) for the year", {"FY2025": 636, "FY2024": 887, "FY2023": 2092, "FY2022": -727, "FY2021": 89}),
]

INCOME_STATEMENT_SOURCES = (
    "Sources - HSBC Bank plc's own Consolidated income statement and Consolidated statement of comprehensive "
    "income, £m, from each year's own Annual Report and Accounts (each year's own originally-published "
    "figures, not a later restated comparative):\n"
    f"FY2025: HSBC Bank plc Annual Report and Accounts 2025, p.90-91 - {AR2025_URL}\n"
    f"FY2024: HSBC Bank plc Annual Report and Accounts 2024, p.115-116 - {AR2024_URL}\n"
    f"FY2023: HSBC Bank plc Annual Report and Accounts 2023, p.106-107 - {AR2023_URL}\n"
    f"FY2022: HSBC Bank plc Annual Report and Accounts 2022, p.114-115 - {AR2022_URL}\n"
    f"FY2021: HSBC Bank plc Annual Report and Accounts 2021, p.108-109 - {AR2021_URL}\n\n"
    "HSBC Bank plc adopted IFRS 17 'Insurance Contracts' from 1 January 2023, replacing IFRS 4 - this is a "
    "genuine presentation-structure change, not a gap: FY2021/FY2022's own income statements use the IFRS 4 "
    "structure ('Net insurance premium income', 'Total operating income', 'Net insurance claims paid'), while "
    "FY2023-FY2025 use the IFRS 17 structure ('Insurance finance income/expense', 'Insurance service result') - "
    "both shown on their own basis rather than forced into one template. 'Net operating income before change in "
    "expected credit losses' is the one line comparable in substance across the whole transition ('total "
    "operating income' minus 'net insurance claims paid' under IFRS 4 equals this line's own value under IFRS 4, "
    "confirmed by cross-checking both years' totals).\n\n"
    + ENTITY_NOTE + "\n\n" + IFRS17_NOTE
)

bw.add_income_statement_sheet(
    title="HSBC Bank plc — Consolidated Income Statement",
    subtitle="HSBC Bank plc consolidated (entity-level, not the wider HSBC Holdings plc Group), £m. See source note at bottom.",
    rows=income_statement_rows,
    sources_text=INCOME_STATEMENT_SOURCES,
    first_col_width=90,
    source_height=340,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
# Combined-column presentation: "Other reserves" sums the Financial assets
# FVOCI / Cash flow hedging / Foreign exchange / Group reorganisation /
# Insurance finance reserve columns shown in HSBC Bank plc's own 11-column
# statement - verified this combined total ties exactly to the Balance
# Sheet's own "Other reserves" line for every year before finalizing.
EQUITY_HEADERS = ["Called-up share capital & premium", "Other equity instruments", "Retained earnings", "Other reserves", "Total shareholders' equity", "Non-controlling interests", "Total equity"]

equity_rows = [
    ("TOTAL", "Balance at 1 Jan 2021 (FY2020 closing, per FY2021's own statement)", (797, 3722, 23829, -4682, 23666, 183, 23849)),
    ("DATA", "Profit for the year", (None, None, 1041, None, 1041, 5, 1046)),
    ("DATA", "Other comprehensive income/(expense), net of tax", (None, None, 46, -994, -948, -9, -957)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, 1087, -994, 93, -4, 89)),
    ("DATA", "Dividends paid to the parent company", (None, None, -194, None, -194, -1, -195)),
    ("DATA", "Net impact of equity-settled share-based payments", (None, None, -10, None, -10, None, -10)),
    ("DATA", "Change in business combinations and other movements", (None, None, 23, 6, 29, -47, -18)),
    ("TOTAL", "Balance at 31 Dec 2021 (per FY2021's own statement)", (797, 3722, 24735, -5670, 23584, 131, 23715)),
    ("DATA", "Loss for the year", (None, None, -408, None, -408, 10, -398)),
    ("DATA", "Other comprehensive (expense)/income, net of tax", (None, None, 367, -698, -331, 2, -329)),
    ("TOTAL", "Total comprehensive (expense)/income for the year", (None, None, -41, -698, -739, 12, -727)),
    ("DATA", "Capital securities issued during the period", (420, 208, None, None, 628, None, 628)),
    ("DATA", "Dividends paid to the parent company", (None, None, -1052, None, -1052, -2, -1054)),
    ("DATA", "Net impact of equity-settled share-based payments", (None, None, 5, None, 5, None, 5)),
    ("DATA", "Capital contribution from the parent company", (None, None, 1465, None, 1465, None, 1465)),
    ("DATA", "Change in business combinations and other movements", (None, None, -16, None, -16, None, -16)),
    ("TOTAL", "Balance at 31 Dec 2022 (per FY2022's own statement, IFRS 4/pre-restatement basis)", (1217, 3930, 25096, -6368, 23875, 141, 24016)),
    ("DATA", "IFRS 17 transition restatement (change in opening balance, see source note)", (0, 0, -728, -45, -773, -10, -783)),
    ("TOTAL", "Balance at 1 Jan 2023 (restated, per FY2023's own statement)", (1217, 3930, 24368, -6413, 23102, 131, 23233)),
    ("DATA", "Profit for the year", (None, None, 1703, None, 1703, 22, 1725)),
    ("DATA", "Other comprehensive income/(expense), net of tax", (None, None, -134, 501, 367, None, 367)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, 1569, 501, 2070, 22, 2092)),
    ("DATA", "Capital securities issued during the period", (584, None, None, None, 584, None, 584)),
    ("DATA", "Dividends paid to the parent company", (None, None, -961, None, -961, -7, -968)),
    ("DATA", "Net impact of equity-settled share-based payments", (None, None, -18, None, -18, None, -18)),
    ("DATA", "Change in business combinations and other movements", (None, None, -234, -184, -418, None, -418)),
    ("TOTAL", "Balance at 31 Dec 2023 (per FY2023's own statement)", (1801, 3930, 24724, -6096, 24359, 146, 24505)),
    ("DATA", "Profit for the period", (None, None, 1253, None, 1253, 30, 1283)),
    ("DATA", "Other comprehensive (expense)/income, net of tax", (None, None, -40, -350, -390, -6, -396)),
    ("TOTAL", "Total comprehensive (expense)/income for the year", (None, None, 1213, -350, 863, 24, 887)),
    ("DATA", "Capital securities issued during the period", (2578, 204, None, None, 2782, None, 2782)),
    ("DATA", "Redemption of securities", (None, -213, None, None, -213, None, -213)),
    ("DATA", "Dividends paid to the parent company", (None, None, -535, None, -535, -11, -546)),
    ("DATA", "Net impact of equity-settled share-based payments", (None, None, -6, None, -6, None, -6)),
    ("DATA", "Change in business combinations and other movements", (None, None, -356, 1, -355, -1, -356)),
    ("TOTAL", "Balance at 31 Dec 2024 (per FY2024's own statement)", (4379, 3921, 25040, -6445, 26895, 158, 27053)),
    ("DATA", "(Loss)/profit for the period", (None, None, -591, None, -591, 10, -581)),
    ("DATA", "Other comprehensive (expense)/income, net of tax", (None, None, -81, 1287, 1206, 11, 1217)),
    ("TOTAL", "Total comprehensive (expense)/income for the year", (None, None, -672, 1287, 615, 21, 636)),
    ("DATA", "Capital securities issued during the period", (None, 276, None, None, 276, None, 276)),
    ("DATA", "Dividends paid to the parent company", (None, None, -1951, None, -1951, -16, -1967)),
    ("DATA", "Net impact of equity-settled share-based payments", (None, None, -24, None, -24, None, -24)),
    ("DATA", "Change in business combinations and other movements", (None, None, -17, 7, -10, None, -10)),
    ("TOTAL", "Balance at 31 Dec 2025 (per FY2025's own statement)", (4379, 4197, 22376, -5151, 25801, 163, 25964)),
]

EQUITY_SOURCES = (
    "Sources - HSBC Bank plc's own Consolidated statement of changes in equity, £m, from each year's own "
    "Annual Report and Accounts (each year's own originally-published figures for that year's own movements):\n"
    f"FY2021 movements: HSBC Bank plc Annual Report and Accounts 2022, p.118 (shows FY2021 as its prior-year "
    f"comparative column) - {AR2022_URL}\n"
    f"FY2022 movements: HSBC Bank plc Annual Report and Accounts 2022, p.118 - {AR2022_URL}\n"
    f"FY2023 movements: HSBC Bank plc Annual Report and Accounts 2023, p.109 - {AR2023_URL}\n"
    f"FY2024 movements: HSBC Bank plc Annual Report and Accounts 2024, p.118 - {AR2024_URL}\n"
    f"FY2025 movements: HSBC Bank plc Annual Report and Accounts 2025, p.93 - {AR2025_URL}\n\n"
    "'Other reserves' combines the Financial assets at FVOCI reserve, Cash flow hedging reserve, Foreign "
    "exchange reserve, Group reorganisation reserve, and (from FY2023) Insurance finance reserve columns shown "
    "separately in the Bank's own 11-column statement - verified this combined total ties exactly to the "
    "Balance Sheet's own 'Other reserves' line for every year before finalizing. Equity reconciliation ladder "
    "confirmed: each year's own closing balance ties exactly to the next year's own opening balance and to that "
    "year's own Balance Sheet Total equity, with the one exception below.\n\n"
    + ENTITY_NOTE + "\n\n" + IFRS17_NOTE
)

bw.add_equity_changes_sheet(
    title="HSBC Bank plc — Consolidated Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, £m. 'Other reserves' is a combined column - see source note. See source note at bottom.",
    headers=EQUITY_HEADERS,
    rows=equity_rows,
    sources_text=EQUITY_SOURCES,
    first_col_width=64,
    source_height=280,
    col_width=17,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {"FY2025": -119, "FY2024": 2068, "FY2023": 2152, "FY2022": -959, "FY2021": 1023}),
    ("DATA", "Depreciation, amortisation and impairment", {"FY2025": 558, "FY2024": 148, "FY2023": 61, "FY2022": 128, "FY2021": 174}),
    ("DATA", "Net loss/(gain) from investing activities", {"FY2025": 1098, "FY2024": 83, "FY2023": -66, "FY2022": 2002, "FY2021": -62}),
    ("DATA", "Share of (profit)/loss in associates and joint ventures", {"FY2025": -61, "FY2024": -18, "FY2023": 43, "FY2022": 30, "FY2021": -191}),
    ("DATA", "Change in expected credit losses gross of recoveries and other credit impairment charges", {"FY2025": 154, "FY2024": 165, "FY2023": 161, "FY2022": 253, "FY2021": -171}),
    ("DATA", "Provisions including pensions", {"FY2025": 1184, "FY2024": 78, "FY2023": 132, "FY2022": 192, "FY2021": 104}),
    ("DATA", "Share-based payment expense", {"FY2025": 81, "FY2024": 61, "FY2023": 58, "FY2022": 46, "FY2021": 96}),
    ("DATA", "Other non-cash items included in (loss)/profit before tax", {"FY2025": -155, "FY2024": -180, "FY2023": -165, "FY2022": -242, "FY2021": -198}),
    ("DATA", "Elimination of exchange differences", {"FY2025": -3416, "FY2024": 4883, "FY2023": 4426, "FY2022": -6714, "FY2021": 4926}),
    ("DATA", "- change in net trading securities and derivatives", {"FY2025": -16933, "FY2024": -13266, "FY2023": -15528, "FY2022": -6213, "FY2021": 8157}),
    ("DATA", "- change in loans and advances to banks and customers", {"FY2025": -3077, "FY2024": -455, "FY2023": 4245, "FY2022": -2717, "FY2021": 11149}),
    ("DATA", "- change in reverse repurchase agreements - non-trading", {"FY2025": -13896, "FY2024": 9341, "FY2023": -13531, "FY2022": 6251, "FY2021": 9538}),
    ("DATA", "- change in financial assets designated and otherwise mandatorily measured at fair value", {"FY2025": -3139, "FY2024": -1954, "FY2023": -3296, "FY2022": 2729, "FY2021": -2429}),
    ("DATA", "- change in other assets", {"FY2025": -3313, "FY2024": 4734, "FY2023": -5707, "FY2022": -7329, "FY2021": 10924}),
    ("DATA", "- change in deposits by banks and customer accounts", {"FY2025": 23219, "FY2024": 14113, "FY2023": 7548, "FY2022": 19835, "FY2021": 7940}),
    ("DATA", "- change in repurchase agreements - non-trading", {"FY2025": 6374, "FY2024": -13813, "FY2023": 20516, "FY2022": 5641, "FY2021": -7643}),
    ("DATA", "- change in debt securities in issue", {"FY2025": -6638, "FY2024": 6018, "FY2023": 6175, "FY2022": -1060, "FY2021": -7943}),
    ("DATA", "- change in financial liabilities designated at fair value", {"FY2025": 5234, "FY2024": 4937, "FY2023": 4042, "FY2022": -1822, "FY2021": -7191}),
    ("DATA", "- change in other liabilities", {"FY2025": 3534, "FY2024": -10026, "FY2023": -7506, "FY2022": 21297, "FY2021": -12295}),
    ("DATA", "- dividend received from associates", {"FY2025": 18, "FY2023": 15, "FY2022": 7}),
    ("DATA", "- contributions paid to defined benefit plans", {"FY2025": -28, "FY2024": -20, "FY2023": -5, "FY2022": -10, "FY2021": -24}),
    ("DATA", "- tax received/(paid)", {"FY2025": 92, "FY2024": -1088, "FY2023": -140, "FY2022": 845, "FY2021": -581}),
    ("TOTAL", "Changes in operating assets and liabilities - subtotal", {"FY2025": -8553, "FY2024": -1479, "FY2023": -3172, "FY2022": 37454, "FY2021": 9602}),
    ("TOTAL", "Net cash from operating activities", {"FY2025": -9229, "FY2024": 5809, "FY2023": 3630, "FY2022": 32190, "FY2021": 15303}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of financial investments", {"FY2025": -45055, "FY2024": -32587, "FY2023": -26586, "FY2022": -13227, "FY2021": -18890}),
    ("DATA", "Proceeds from the sale and maturity of financial investments", {"FY2025": 33969, "FY2024": 23272, "FY2023": 15497, "FY2022": 20490, "FY2021": 25027}),
    ("DATA", "Net cash flows from the purchase and sale of property, plant and equipment", {"FY2025": -18, "FY2024": -16, "FY2023": -31, "FY2022": -20, "FY2021": 52}),
    ("DATA", "Net investment in intangible assets", {"FY2025": -393, "FY2024": -149, "FY2023": -125, "FY2022": -28, "FY2021": -45}),
    ("DATA", "Net cash outflow from investment in associates and acquisition of businesses and subsidiaries", {"FY2025": -25, "FY2024": -955, "FY2023": -1161, "FY2022": -29, "FY2021": -85}),
    ("DATA", "Net cash flow on disposal of subsidiaries, businesses, associates and joint ventures", {"FY2025": 39, "FY2024": -8631, "FY2023": -394, "FY2021": 0}),
    ("TOTAL", "Net cash from investing activities", {"FY2025": -11483, "FY2024": -19066, "FY2023": -12800, "FY2022": 7186, "FY2021": 6059}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Issue of ordinary share capital and other equity instruments", {"FY2025": 276, "FY2024": 2782, "FY2023": 584, "FY2022": 628}),
    ("DATA", "Redemption of other equity instruments", {"FY2024": -213, "FY2021": 0}),
    ("DATA", "Subordinated loan capital issued", {"FY2025": 2702, "FY2024": 2777, "FY2023": 3246, "FY2022": 3111, "FY2021": 10466}),
    ("DATA", "Subordinated loan capital repaid", {"FY2025": -1277, "FY2024": -474, "FY2023": -2693, "FY2022": -2248, "FY2021": -10902}),
    ("DATA", "Dividends to the parent company", {"FY2025": -1951, "FY2024": -535, "FY2023": -961, "FY2022": -1052, "FY2021": -194}),
    ("DATA", "Funds received from the parent company", {"FY2022": 1465}),
    ("DATA", "Dividends paid to non-controlling interests", {"FY2025": -16, "FY2024": -11, "FY2023": -7, "FY2022": -2, "FY2021": -1}),
    ("TOTAL", "Net cash from financing activities", {"FY2025": -266, "FY2024": 4326, "FY2023": 169, "FY2022": 1902, "FY2021": -631}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": -20978, "FY2024": -8931, "FY2023": -9001, "FY2022": 41278, "FY2021": 20731}),
    ("DATA", "Cash and cash equivalents at 1 Jan", {"FY2025": 162928, "FY2024": 177037, "FY2023": 189907, "FY2022": 140923, "FY2021": 125304}),
    ("DATA", "Exchange difference in respect of cash and cash equivalents", {"FY2025": 4949, "FY2024": -5178, "FY2023": -3869, "FY2022": 7706, "FY2021": -5112}),
    ("TOTAL", "Cash and cash equivalents at 31 Dec", {"FY2025": 146899, "FY2024": 162928, "FY2023": 177037, "FY2022": 189907, "FY2021": 140923}),
]

bw.add_cash_flow_sheet(
    title="HSBC Bank plc — Consolidated Cash Flow Statement",
    subtitle="HSBC Bank plc consolidated (entity-level, not the wider HSBC Holdings plc Group), £m. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=82,
    source_height=280,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
LOANS_GROSS = {"FY2025": 80558, "FY2024": 83524, "FY2023": 76579, "FY2022": 73717, "FY2021": 92331}
LOANS_ECL = {"FY2025": -700, "FY2024": -858, "FY2023": -1088, "FY2022": -1103, "FY2021": -1154}
LOANS_NET = {y: LOANS_GROSS[y] + LOANS_ECL[y] for y in YEARS}
LOANS_COVERAGE = {y: f"{-LOANS_ECL[y] / LOANS_GROSS[y] * 100:.2f}%" for y in YEARS}

asset_quality_rows = [
    ("DATA", "Loans and advances to customers at amortised cost, gross carrying amount", LOANS_GROSS),
    ("DATA", "Allowance for expected credit losses", LOANS_ECL),
    ("TOTAL", "Loans and advances to customers at amortised cost, net", LOANS_NET),
    ("DATA", "ECL coverage ratio (allowance / gross carrying amount)", LOANS_COVERAGE),
]

ASSET_QUALITY_SOURCES = (
    "Sources - HSBC Bank plc's own 'Summary of financial instruments to which the impairment requirements in "
    "IFRS 9 are applied' table (the group basis), 'Loans and advances to customers at amortised cost' row, £m, "
    "from each year's own Annual Report and Accounts (each year's own originally-published figures):\n"
    f"FY2025: HSBC Bank plc Annual Report and Accounts 2025, p.25 - {AR2025_URL}\n"
    f"FY2024: HSBC Bank plc Annual Report and Accounts 2024, p.33 - {AR2024_URL}\n"
    f"FY2023: HSBC Bank plc Annual Report and Accounts 2023, p.33 - {AR2023_URL}\n"
    f"FY2022: HSBC Bank plc Annual Report and Accounts 2022, p.39 - {AR2022_URL}\n"
    f"FY2021: HSBC Bank plc Annual Report and Accounts 2021, p.34 - {AR2021_URL}\n\n"
    "Net figures tie exactly to this workbook's Balance Sheet 'Loans and advances to customers' line for every "
    "year. HSBC Bank plc's own IFRS 9 stage table further splits this by product (personal / corporate and "
    "commercial / non-bank financial institutions) and by Stage 1/2/3/POCI - not reproduced here at that "
    "granularity given the entity's scale, but the same gross/net/coverage totals shown above tie to that "
    "underlying stage table exactly.\n\n"
    + ENTITY_NOTE
)

bw.add_asset_quality_sheet(
    title="HSBC Bank plc — Asset Quality",
    subtitle="Loans and advances to customers at amortised cost, £m, group basis. See source note at bottom.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=80,
    source_height=250,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=48, source_height=190)


metric(
    "CET1 Capital", "£m",
    [("Common equity tier 1 (CET1) capital", {"FY2025": 20063, "FY2024": 21896, "FY2023": 19230, "FY2022": 19184, "FY2021": 18007})],
)

metric(
    "CET1 Ratio", "% of RWA",
    [("CET1 ratio", {"FY2025": "17.9%", "FY2024": "19.5%", "FY2023": "17.9%", "FY2022": "16.8%", "FY2021": "17.3%"})],
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 24272, "FY2024": 25828, "FY2023": 23124, "FY2022": 23077, "FY2021": 21869})],
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "21.6%", "FY2024": "23.0%", "FY2023": "21.5%", "FY2022": "20.2%", "FY2021": "21.0%"})],
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 41473, "FY2024": 41306, "FY2023": 37131, "FY2022": 36187, "FY2021": 33036})],
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "36.9%", "FY2024": "36.8%", "FY2023": "34.6%", "FY2022": "31.7%", "FY2021": "31.7%"})],
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted assets", {"FY2025": 112340, "FY2024": 112251, "FY2023": 107449, "FY2022": 114171, "FY2021": 104314})],
)

# ---------------------------------------------------------------
# Sheet: RWA Breakdown - HSBC Bank plc's own entity-level UK OV1 table
# ---------------------------------------------------------------
rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding counterparty credit risk)", {"FY2025": 56633, "FY2024": 57911, "FY2023": 58620, "FY2021": 60450}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 20958, "FY2024": 18201, "FY2023": 17037, "FY2021": 16389}),
    ("DATA", "Settlement risk", {"FY2025": 41, "FY2024": 27, "FY2023": 29, "FY2021": 45}),
    ("DATA", "Securitisation exposures in the non-trading book", {"FY2025": 2908, "FY2024": 3545, "FY2023": 3363, "FY2021": 3734}),
    ("DATA", "Market risk (position, FX and commodities)", {"FY2025": 16799, "FY2024": 18519, "FY2023": 15525, "FY2021": 9828}),
    ("DATA", "Operational risk", {"FY2025": 15001, "FY2024": 14048, "FY2023": 12875, "FY2021": 10512}),
    ("DATA", "Amounts below the thresholds for deduction (FY2021 own separate line only)", {"FY2021": 3356}),
    ("TOTAL", "Total RWAs", {"FY2025": 112340, "FY2024": 112251, "FY2023": 107449, "FY2022": 114171, "FY2021": 104314}),
]

RWA_BREAKDOWN_SOURCES = (
    "Sources - HSBC Bank plc's own entity-level 'Overview of risk-weighted exposure amounts' (UK OV1 template) "
    "from the official HSBC Bank plc Pillar 3 Disclosures, each year's own originally-published figures:\n"
    f"FY2025: HSBC Bank plc Pillar 3 Disclosures at 31 December 2025, Table 4, p.10 - {P32025_URL}\n"
    f"FY2024: HSBC Bank plc Pillar 3 Disclosures at 31 December 2024, Table 4, p.10 - {P32024_URL}\n"
    f"FY2023: HSBC Bank plc Pillar 3 Disclosures at 31 December 2023, Table 7, p.13 - {P32023_URL}\n"
    f"FY2022: genuinely not disclosed at category level - confirmed by reading the FY2022 Pillar 3 Disclosures "
    f"in full - only an aggregate Total RWAs figure appears in Table 1 (KM1), no RWA-by-risk-type breakdown "
    f"table exists in this vintage of the document - {P32022_URL}\n"
    f"FY2021: HSBC Bank plc Pillar 3 Disclosures at 31 December 2021, Table 2, p.3 - {P32021_URL}\n\n"
    "Each year's Total ties exactly to this workbook's Total RWAs metric sheet. FY2021's document (pre-dates "
    "the KM1/OV1 template used from FY2022 onward) shows 'Amounts below the thresholds for deduction' as its "
    "own explicit row; FY2023-FY2025's documents embed the equivalent amount inside the Credit risk row (as a "
    "footnoted 'of which' figure) rather than a separate addable row - left blank for those years rather than "
    "double-counted or force-matched to FY2021's structure.\n\n"
    + ENTITY_NOTE
)

bw.add_rwa_breakdown_sheet(
    title="HSBC Bank plc — RWA Breakdown",
    subtitle="£m, entity-level Pillar 3 UK OV1 template. FY2022 genuinely not disclosed at category level - see source note.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=88,
    source_height=310,
    unit_suffix=" (£m)",
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio", {"FY2025": "4.5%", "FY2024": "5.5%", "FY2023": "5.1%", "FY2022": "5.5%", "FY2021": "4.1%"})],
    note="A genuine basis change: FY2021 is disclosed on the Capital Requirements Regulation basis (total "
         "leverage ratio exposure £535,562m, ratio 4.1%). From FY2022 onward, HSBC Bank plc switched to the "
         "CRR II end-point basis 'excluding claims on central banks' (a narrower exposure measure) - FY2022's "
         "own report shows this new-basis figure (exposure £417,587m, ratio 5.5%) with no FY2021 comparative on "
         "the same basis, so FY2021 above is left on its own originally-disclosed (different) basis rather than "
         "forced onto the newer definition.",
)

metric(
    "LCR", "%, 12-month average",
    [("Liquidity coverage ratio", {"FY2025": "148%", "FY2024": "148%", "FY2023": "148%", "FY2022": "143.1%"})],
    note="Not disclosed for FY2021: HSBC Bank plc's own FY2021 Pillar 3 Disclosures pre-date the KM1 template "
         "and PRA's entity-level LCR/NSFR disclosure requirement, which 'came into effect on 1 January 2022' "
         "per the FY2022 Pillar 3 Disclosures' own footnote - confirmed genuinely absent, not an access gap. "
         "Reported on a 12-month rolling average basis (this project's standard convention).",
)

metric(
    "NSFR", "%, average of preceding 4 quarters",
    [("Net stable funding ratio", {"FY2025": "114%", "FY2024": "115%", "FY2023": "116%", "FY2022": "115.4%"})],
    note="Not disclosed for FY2021 - same reason as the LCR sheet (pre-dates the PRA's entity-level NSFR "
         "disclosure requirement, effective 1 January 2022).",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={
        "MREL Ratio": "No MREL figure or mention appears anywhere in any of HSBC Bank plc's own Pillar 3 "
                      "Disclosures FY2021-FY2025 - HSBC Bank plc is not itself a resolution entity under the "
                      "Bank of England's Single Point of Entry resolution strategy for the HSBC group (that "
                      "role sits with HSBC Holdings plc at the top of the group), so no entity-level MREL "
                      "requirement or ratio applies here - the same pattern as RBS plc/Coutts & Company's "
                      "relationship to the wider NatWest Group.",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 707696, "FY2024": 727330, "FY2023": 702970, "FY2022": 717353, "FY2021": 596611}),
        ("Loans and advances to customers", {"FY2025": 79858, "FY2024": 82666, "FY2023": 75491, "FY2022": 72614, "FY2021": 91177}),
        ("Total liabilities", {"FY2025": 681732, "FY2024": 700277, "FY2023": 678465, "FY2022": 693337, "FY2021": 572896}),
        ("Total equity", {"FY2025": 25964, "FY2024": 27053, "FY2023": 24505, "FY2022": 24016, "FY2021": 23715}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Net operating income", {"FY2025": 6724, "FY2024": 7310, "FY2023": 7337, "FY2022": 4424, "FY2021": 6294}),
        ("Total operating expenses", {"FY2025": -6904, "FY2024": -5260, "FY2023": -5142, "FY2022": -5353, "FY2021": -5462}),
        ("(Loss)/profit before tax", {"FY2025": -119, "FY2024": 2068, "FY2023": 2152, "FY2022": -959, "FY2021": 1023}),
        ("(Loss)/profit for the year", {"FY2025": -581, "FY2024": 1283, "FY2023": 1725, "FY2022": -398, "FY2021": 1046}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Total comprehensive income/(expense) for the year", {"FY2025": 636, "FY2024": 887, "FY2023": 2092, "FY2022": -727, "FY2021": 89}),
        ("Total equity (closing)", {"FY2025": 25964, "FY2024": 27053, "FY2023": 24505, "FY2022": 24016, "FY2021": 23715}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash from operating activities", {"FY2025": -9229, "FY2024": 5809, "FY2023": 3630, "FY2022": 32190, "FY2021": 15303}),
        ("Net cash from investing activities", {"FY2025": -11483, "FY2024": -19066, "FY2023": -12800, "FY2022": 7186, "FY2021": 6059}),
        ("Net cash from financing activities", {"FY2025": -266, "FY2024": 4326, "FY2023": 169, "FY2022": 1902, "FY2021": -631}),
        ("Cash and cash equivalents at 31 Dec", {"FY2025": 146899, "FY2024": 162928, "FY2023": 177037, "FY2022": 189907, "FY2021": 140923}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "17.9%", "FY2024": "19.5%", "FY2023": "17.9%", "FY2022": "16.8%", "FY2021": "17.3%"}),
        ("Tier 1 Ratio", {"FY2025": "21.6%", "FY2024": "23.0%", "FY2023": "21.5%", "FY2022": "20.2%", "FY2021": "21.0%"}),
        ("Total Capital Ratio", {"FY2025": "36.9%", "FY2024": "36.8%", "FY2023": "34.6%", "FY2022": "31.7%", "FY2021": "31.7%"}),
        ("Leverage Ratio", {"FY2025": "4.5%", "FY2024": "5.5%", "FY2023": "5.1%", "FY2022": "5.5%", "FY2021": "4.1%"}),
        ("LCR", {"FY2025": "148%", "FY2024": "148%", "FY2023": "148%", "FY2022": "143.1%"}),
        ("NSFR", {"FY2025": "114%", "FY2024": "115%", "FY2023": "116%", "FY2022": "115.4%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. MREL is not shown here (not disclosed at this "
         "entity level - see that sheet). The Leverage Ratio's FY2021 figure is on a different basis than "
         "FY2022-FY2025 - see the Leverage Ratio sheet's note.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/HSBC BANK PLC FINANCIALS.xlsx")
