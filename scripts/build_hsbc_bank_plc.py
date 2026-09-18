import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018"]  # most recent first, all 12mo to 31 Dec
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2025/annual/pdfs/hsbc-bank-plc/260225-annual-report-and-accounts-2025.pdf"
AR2024_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2024/annual/pdfs/hsbc-bank-plc/250219-annual-report-and-accounts-2024.pdf"
AR2023_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2023/annual/pdfs/hsbc-bank-plc/240221-annual-report-and-accounts-2023.pdf"
AR2022_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2022/annual/pdfs/hsbc-bank-plc/230221-annual-report-and-accounts-2022.pdf"
AR2021_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2021/annual/pdfs/hsbc-bank-plc/220222-annual-report-and-accounts-2021.pdf"
AR2020_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2020/annual/pdfs/hsbc-bank-plc/210223-annual-report-and-accounts-2020.pdf"
AR2019_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2019/annual/pdfs/hsbc-bank-plc/200218-annual-report-and-accounts-2019.pdf"
AR2018_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2018/annual/hsbc-bank-plc/190219-annual-report-and-accounts-2018.pdf"

P32025_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2025/annual/pdfs/hsbc-bank-plc/260225-pillar-3-disclosures-at-31-december-2025.pdf"
P32024_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2024/annual/pdfs/hsbc-bank-plc/250219-pillar-3-disclosures-at-31-december-2024.pdf"
P32023_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2023/annual/pdfs/hsbc-bank-plc/240221-pillar-3-disclosures-31-december-2023.pdf"
P32022_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2022/annual/pdfs/hsbc-bank-plc/230221-pillar-3-disclosures-31-december-2022.pdf"
P32021_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2021/annual/pdfs/hsbc-bank-plc/220222-pillar-3-disclosures-at-31-december-2021.pdf"
P32020_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2020/annual/pdfs/hsbc-bank-plc/210223-pillar-3-disclosures-31-december-2020.pdf"
P32019_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2019/annual/pdfs/hsbc-bank-plc/200218-pillar-3-disclosures-31-december-2019.pdf"
P32018_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2018/annual/hsbc-bank-plc/190219-pillar-3-disclosures-31-december-2018.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: HSBC Bank plc (Companies House 00014259, FRN 114216) is HSBC's legacy UK/international "
    "non-ring-fenced banking entity - confirmed distinct from HSBC UK Bank plc (FRN 765112, the ring-fenced "
    "retail bank created 2018 under UK ring-fencing reform, not attempted in this project as of this build), "
    "HSBC Holdings plc (the ultimate listed parent, out of scope), and HSBC Innovation Bank Limited (FRN "
    "543146, the former Silicon Valley Bank UK, built separately in this same batch - see 'HSBC INNOVATION "
    "BANK FINANCIALS.xlsx'). All figures below are HSBC Bank plc's own entity-level Consolidated (i.e. HSBC "
    "Bank plc and its own subsidiaries, not the wider HSBC Holdings plc Group) statements, sourced directly "
    "from HSBC Bank plc's own Annual Report and Accounts and Pillar 3 Disclosures, published on hsbc.com's "
    "investor-relations 'Subsidiaries' reporting archive, found via that archive's own '/api/tables/archive' "
    "document-filter endpoint (query params company-new=hsbc-bank-plc&years=<YYYY> against "
    "hsbc.com/investors/results-and-announcements/all-reporting/subsidiaries) - re-confirmed working in the "
    "FY2018-FY2020 extension session, where Companies House was, this time, fully reachable (re-tested via "
    "nslookup and a direct filing-history fetch), so the technique was reused only because it was already "
    "documented, not because it was still needed for access. Both a 2023 IFRS 17 'Insurance Contracts' "
    "adoption and a late-2022 change to how non-financial-institution subsidiary investments are measured "
    "triggered real, source-disclosed restatements of prior-year comparatives - per this project's convention, "
    "every year below uses that year's own originally-published figures, not a later restated comparative; "
    "both restatements are individually noted where they bite. A separate, much larger structural event bites "
    "at the FY2018 floor: HSBC completed UK ring-fencing on 1 July 2018, transferring qualifying RBWM/CMB/GPB "
    "retail and commercial customers out of HSBC Bank plc into the newly created HSBC UK Bank plc - this alone "
    "roughly halves HSBC Bank plc's own balance sheet within FY2018 (Total assets £818,868m at 31 Dec 2017 to "
    "£604,958m at 31 Dec 2018, per FY2018's own Annual Report) and introduces a 'Group reorganisation reserve' "
    "(GRR) of £(7,692)m as a one-off FY2018 equity movement - a genuine one-off business separation, not a "
    "transcription error, and not restated in any later year's figures."
)

CASH_FLOW_NOTE = (
    "CASH FLOW NOTE: figures are £m (this is one of the largest entities in this project by balance sheet "
    "size; £'000 would be unwieldy). The full opening-to-closing cash chain reconciles exactly year-to-year "
    "using each year's own originally-published figures (FY2018 closing £89,002m; FY2019 closing £92,338m = "
    "FY2020 opening £92,338m; FY2020 closing £125,304m; FY2021 closing £140,923m = FY2022 opening; FY2022 "
    "closing £189,907m = FY2023 opening; FY2023 closing £177,037m = FY2024 opening; FY2024 closing £162,928m "
    "= FY2025 opening) despite the IFRS 17 restatement below only affecting the 'Profit/(loss) before tax' "
    "and adjustment-line presentation for FY2022, not the underlying cash totals. One row's label was "
    "corrected between reports for the same figure: FY2022's own Annual Report labelled the £628m financing "
    "line 'redemption of preference shares and other equity instruments' (a positive value, inconsistent with "
    "'redemption'), which the FY2023 Annual Report's FY2022 comparative column relabels 'issue of ordinary "
    "share capital and other equity instruments' - matching the £628m 'Capital securities issued during the "
    "period' shown in FY2022's own statement of changes in equity. The corrected label and FY2022's own "
    "originally-published £628m value are both used here. A second, genuine cash-definition break bites "
    "between FY2018 and FY2019: FY2018's own Annual Report shows closing cash and cash equivalents of "
    "£89,002m, but FY2019's own Annual Report footnotes that 'HSBC included settlement accounts with bank "
    "counterparties of one month or less on a net basis' from 2019, re-presenting the FY2018 comparative "
    "opening figure upward by approximately £8.1bn to £97,058m - FY2018's own originally-published £89,002m "
    "closing figure is used here rather than that later re-presented comparative, so the FY2018-to-FY2019 "
    "opening/closing pair does not tie exactly (a real disclosed definitional change, not a transcription "
    "error). Separately, FY2018's own 'change in other liabilities' operating-activities line (£5,394m) "
    "differs slightly from the £5,171m shown as FY2019's FY2018 comparative in the FY2019 Annual Report - "
    "attributable to the same settlement-account netting re-presentation; FY2018's own originally-published "
    "figure is used, and it is what its own year's 'Changes in operating assets and liabilities' subtotal "
    "(£(670)m) and 'Net cash from operating activities' (£(161)m) are actually built from."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are HSBC Bank plc's own Consolidated Statement of Cash Flows, £m, from each year's "
    "own Annual Report and Accounts (each year's own originally-published figures, not a later restated "
    "comparative):\n"
    f"FY2025: HSBC Bank plc Annual Report and Accounts 2025, p.95 (Consolidated statement of cash flows) - {AR2025_URL}\n"
    f"FY2024: HSBC Bank plc Annual Report and Accounts 2024, p.121 (Consolidated statement of cash flows) - {AR2024_URL}\n"
    f"FY2023: HSBC Bank plc Annual Report and Accounts 2023, p.112-113 (Consolidated statement of cash flows) - {AR2023_URL}\n"
    f"FY2022: HSBC Bank plc Annual Report and Accounts 2022, p.117 (Consolidated statement of cash flows) - {AR2022_URL}\n"
    f"FY2021: HSBC Bank plc Annual Report and Accounts 2021, p.111 (Consolidated statement of cash flows) - {AR2021_URL}\n"
    f"FY2020: HSBC Bank plc Annual Report and Accounts 2020, p.111 (Consolidated statement of cash flows) - {AR2020_URL}\n"
    f"FY2019: HSBC Bank plc Annual Report and Accounts 2019, p.98 (Consolidated statement of cash flows) - {AR2019_URL}\n"
    f"FY2018: HSBC Bank plc Annual Report and Accounts 2018, p.90 (Consolidated statement of cash flows) - {AR2018_URL}\n\n"
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
        f"FY2021: HSBC Bank plc Pillar 3 Disclosures at 31 December 2021, p.2-3 (Tables 1 and 2) - {P32021_URL}\n"
        f"FY2020: HSBC Bank plc Pillar 3 Disclosures at 31 December 2020, p.8 (Table 4, own funds disclosure) - {P32020_URL}\n"
        f"FY2019: HSBC Bank plc Pillar 3 Disclosures at 31 December 2019, p.6-7 (Table 4, own funds disclosure) - {P32019_URL}\n"
        f"FY2018: HSBC Bank plc Pillar 3 Disclosures at 31 December 2018, p.2-3 (Tables 1-3) - {P32018_URL}\n\n"
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
    ("DATA", "Cash and balances at central banks", {"FY2025": 101443, "FY2024": 119184, "FY2023": 110618, "FY2022": 131433, "FY2021": 108482, "FY2020": 85092, "FY2019": 51816, "FY2018": 52013}),
    ("DATA", "Items in the course of collection from other banks", {"FY2023": 2114, "FY2022": 2285, "FY2021": 346, "FY2020": 243, "FY2019": 707, "FY2018": 839}),
    ("DATA", "Trading assets", {"FY2025": 131359, "FY2024": 116042, "FY2023": 100696, "FY2022": 79878, "FY2021": 83706, "FY2020": 86976, "FY2019": 98249, "FY2018": 95420}),
    ("DATA", "Financial assets designated and otherwise mandatorily measured at fair value through profit or loss", {"FY2025": 5752, "FY2024": 9417, "FY2023": 19068, "FY2022": 15881, "FY2021": 18649, "FY2020": 16220, "FY2019": 17012, "FY2018": 17799}),
    ("DATA", "Derivatives", {"FY2025": 168585, "FY2024": 198172, "FY2023": 174116, "FY2022": 225238, "FY2021": 141221, "FY2020": 201210, "FY2019": 164538, "FY2018": 144522}),
    ("DATA", "Loans and advances to banks", {"FY2025": 19349, "FY2024": 14521, "FY2023": 14371, "FY2022": 17109, "FY2021": 10784, "FY2020": 12646, "FY2019": 11467, "FY2018": 13628}),
    ("DATA", "Loans and advances to customers", {"FY2025": 79858, "FY2024": 82666, "FY2023": 75491, "FY2022": 72614, "FY2021": 91177, "FY2020": 101491, "FY2019": 108391, "FY2018": 111964}),
    ("DATA", "Reverse repurchase agreements - non-trading", {"FY2025": 68110, "FY2024": 53612, "FY2023": 73494, "FY2022": 53949, "FY2021": 54448, "FY2020": 67577, "FY2019": 85756, "FY2018": 80102}),
    ("DATA", "Financial investments", {"FY2025": 66614, "FY2024": 52216, "FY2023": 46368, "FY2022": 32604, "FY2021": 41300, "FY2020": 51826, "FY2019": 46464, "FY2018": 47272}),
    ("DATA", "Assets held for sale", {"FY2025": 5558, "FY2024": 21606, "FY2023": 20368, "FY2022": 21214}),
    ("DATA", "Prepayments, accrued income and other assets", {"FY2025": 58617, "FY2024": 56950, "FY2023": 63635, "FY2022": 61379, "FY2021": 43127, "FY2020": 55565, "FY2019": 48939, "FY2018": 37497}),
    ("DATA", "Current tax assets", {"FY2025": 463, "FY2024": 1043, "FY2023": 485, "FY2022": 595, "FY2021": 1135, "FY2020": 444, "FY2019": 725, "FY2018": 337}),
    ("DATA", "Interests in associates and joint ventures", {"FY2025": 769, "FY2024": 703, "FY2023": 665, "FY2022": 728, "FY2021": 743, "FY2020": 497, "FY2019": 437, "FY2018": 399}),
    ("DATA", "Goodwill and intangible assets", {"FY2025": 276, "FY2024": 303, "FY2023": 203, "FY2022": 1167, "FY2021": 894, "FY2020": 766, "FY2019": 1582, "FY2018": 2626}),
    ("DATA", "Deferred tax assets", {"FY2025": 943, "FY2024": 895, "FY2023": 1278, "FY2022": 1279, "FY2021": 599, "FY2020": 597, "FY2019": 408, "FY2018": 540}),
    ("TOTAL", "Total assets", {"FY2025": 707696, "FY2024": 727330, "FY2023": 702970, "FY2022": 717353, "FY2021": 596611, "FY2020": 681150, "FY2019": 636491, "FY2018": 604958}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2025": 39679, "FY2024": 26515, "FY2023": 22943, "FY2022": 20836, "FY2021": 32188, "FY2020": 34305, "FY2019": 23991, "FY2018": 24532}),
    ("DATA", "Customer accounts", {"FY2025": 244763, "FY2024": 242303, "FY2023": 222941, "FY2022": 215948, "FY2021": 205241, "FY2020": 195184, "FY2019": 177236, "FY2018": 180836}),
    ("DATA", "Repurchase agreements - non-trading", {"FY2025": 46758, "FY2024": 40384, "FY2023": 53416, "FY2022": 32901, "FY2021": 27259, "FY2020": 34903, "FY2019": 49385, "FY2018": 46583}),
    ("DATA", "Items in the course of transmission to other banks", {"FY2023": 2116, "FY2022": 2226, "FY2021": 489, "FY2020": 290, "FY2019": 403, "FY2018": 351}),
    ("DATA", "Trading liabilities", {"FY2025": 41877, "FY2024": 42633, "FY2023": 42276, "FY2022": 41265, "FY2021": 46433, "FY2020": 44229, "FY2019": 48026, "FY2018": 49514}),
    ("DATA", "Financial liabilities designated at fair value", {"FY2025": 41842, "FY2024": 37443, "FY2023": 32545, "FY2022": 27287, "FY2021": 33608, "FY2020": 40792, "FY2019": 41642, "FY2018": 36922}),
    ("DATA", "Derivatives", {"FY2025": 166666, "FY2024": 197082, "FY2023": 171474, "FY2022": 218867, "FY2021": 139368, "FY2020": 199232, "FY2019": 161083, "FY2018": 139932}),
    ("DATA", "Debt securities in issue", {"FY2025": 12823, "FY2024": 19461, "FY2023": 13443, "FY2022": 7268, "FY2021": 9428, "FY2020": 17371, "FY2019": 25039, "FY2018": 22721}),
    ("DATA", "Liabilities of disposal groups held for sale", {"FY2025": 15711, "FY2024": 23110, "FY2023": 20684, "FY2022": 24711}),
    ("DATA", "Accruals, deferred income and other liabilities", {"FY2025": 50458, "FY2024": 50484, "FY2023": 60444, "FY2022": 66945, "FY2021": 43456, "FY2020": 53395, "FY2019": 50315, "FY2018": 41036}),
    ("DATA", "Current tax liabilities", {"FY2025": 266, "FY2024": 250, "FY2023": 272, "FY2022": 130, "FY2021": 97, "FY2020": 139, "FY2019": 106, "FY2018": 128}),
    ("DATA", "Insurance contract liabilities", {"FY2025": 465, "FY2024": 3424, "FY2023": 20595, "FY2022": 19987, "FY2021": 22264, "FY2020": 22816, "FY2019": 21509, "FY2018": 20657}),
    ("DATA", "Provisions", {"FY2025": 1500, "FY2024": 275, "FY2023": 390, "FY2022": 424, "FY2021": 562, "FY2020": 861, "FY2019": 540, "FY2018": 538}),
    ("DATA", "Deferred tax liabilities", {"FY2025": 5, "FY2024": 5, "FY2023": 6, "FY2022": 14, "FY2021": 15, "FY2020": 20, "FY2019": 22, "FY2018": 29}),
    ("DATA", "Subordinated liabilities", {"FY2025": 18919, "FY2024": 16908, "FY2023": 14920, "FY2022": 14528, "FY2021": 12488, "FY2020": 13764, "FY2019": 13182, "FY2018": 13770}),
    ("TOTAL", "Total liabilities", {"FY2025": 681732, "FY2024": 700277, "FY2023": 678465, "FY2022": 693337, "FY2021": 572896, "FY2020": 657301, "FY2019": 612479, "FY2018": 577549}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 797, "FY2024": 797, "FY2023": 797, "FY2022": 797, "FY2021": 797, "FY2020": 797, "FY2019": 797, "FY2018": 797}),
    ("DATA", "Share premium account", {"FY2025": 3582, "FY2024": 3582, "FY2023": 1004, "FY2022": 420}),
    ("DATA", "Other equity instruments", {"FY2025": 4197, "FY2024": 3921, "FY2023": 3930, "FY2022": 3930, "FY2021": 3722, "FY2020": 3722, "FY2019": 3722, "FY2018": 2403}),
    ("DATA", "Retained earnings", {"FY2025": 22376, "FY2024": 25040, "FY2023": 24724, "FY2022": 25096, "FY2021": 24735, "FY2020": 23829, "FY2019": 24449, "FY2018": 28649}),
    ("DATA", "Other reserves", {"FY2025": -5151, "FY2024": -6445, "FY2023": -6096, "FY2022": -6368, "FY2021": -5670, "FY2020": -4682, "FY2019": -5465, "FY2018": -4971}),
    ("TOTAL", "Total shareholders' equity", {"FY2025": 25801, "FY2024": 26895, "FY2023": 24359, "FY2022": 23875, "FY2021": 23584, "FY2020": 23666, "FY2019": 23503, "FY2018": 26878}),
    ("DATA", "Non-controlling interests", {"FY2025": 163, "FY2024": 158, "FY2023": 146, "FY2022": 141, "FY2021": 131, "FY2020": 183, "FY2019": 509, "FY2018": 531}),
    ("TOTAL", "Total equity", {"FY2025": 25964, "FY2024": 27053, "FY2023": 24505, "FY2022": 24016, "FY2021": 23715, "FY2020": 23849, "FY2019": 24012, "FY2018": 27409}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 707696, "FY2024": 727330, "FY2023": 702970, "FY2022": 717353, "FY2021": 596611, "FY2020": 681150, "FY2019": 636491, "FY2018": 604958}),
]

BALANCE_SHEET_SOURCES = (
    "Sources - HSBC Bank plc's own Consolidated balance sheet, £m, from each year's own Annual Report and "
    "Accounts (each year's own originally-published figures, not a later restated comparative):\n"
    f"FY2025: HSBC Bank plc Annual Report and Accounts 2025, p.92-93 - {AR2025_URL}\n"
    f"FY2024: HSBC Bank plc Annual Report and Accounts 2024, p.117 - {AR2024_URL}\n"
    f"FY2023: HSBC Bank plc Annual Report and Accounts 2023, p.108 - {AR2023_URL}\n"
    f"FY2022: HSBC Bank plc Annual Report and Accounts 2022, p.116 - {AR2022_URL}\n"
    f"FY2021: HSBC Bank plc Annual Report and Accounts 2021, p.110 - {AR2021_URL}\n"
    f"FY2020: HSBC Bank plc Annual Report and Accounts 2020, p.109-110 - {AR2020_URL}\n"
    f"FY2019: HSBC Bank plc Annual Report and Accounts 2019, p.97 - {AR2019_URL}\n"
    f"FY2018: HSBC Bank plc Annual Report and Accounts 2018, p.89 - {AR2018_URL}\n\n"
    "'Items in the course of collection/transmission from other banks' were reported as separate balance sheet "
    "lines through FY2023, then merged into 'Prepayments, accrued income and other assets' / 'Accruals, "
    "deferred income and other liabilities' from FY2024 onward per the Bank's own disclosed presentation "
    "change - left blank for FY2025/FY2024 rather than force-split. 'Share premium account' was not reported "
    "as a line separate from 'Called up share capital' until FY2022 - left blank for FY2018-FY2021. 'Assets/Liabilities "
    "held for sale' did not exist as a line before FY2022 - left blank for FY2018-FY2021. Goodwill and intangible "
    "assets shows a genuine large swing between FY2022's own figure (£1,167m) and the later IFRS 17-restated "
    "FY2022 comparative (£91m, shown in the FY2023 report) due to a VOBA/PVIF insurance intangible "
    "reclassification - FY2022's own originally-published figure is used here. FY2018's own Total assets "
    "(£604,958m) is roughly half FY2017's (£818,868m, not itself shown in this workbook, whose floor is "
    "FY2018) - a genuine one-off effect of the 1 July 2018 UK ring-fencing transfer of retail/commercial "
    "customers to the newly created HSBC UK Bank plc, not a transcription error (see entity note).\n\n"
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
    ("DATA", "Net interest income", {"FY2025": 1274, "FY2024": 985, "FY2023": 2151, "FY2022": 1904, "FY2021": 1754, "FY2020": 1898, "FY2019": 1483, "FY2018": 3660}),
    ("DATA", "- interest income", {"FY2025": 16081, "FY2024": 19414, "FY2023": 17782, "FY2022": 6535, "FY2021": 3149, "FY2020": 4086, "FY2019": 5504, "FY2018": 7422}),
    ("DATA", "- interest expense", {"FY2025": -14807, "FY2024": -18429, "FY2023": -15631, "FY2022": -4631, "FY2021": -1395, "FY2020": -2188, "FY2019": -4021, "FY2018": -3762}),
    ("DATA", "Net fee income", {"FY2025": 1227, "FY2024": 1275, "FY2023": 1229, "FY2022": 1261, "FY2021": 1413, "FY2020": 1400, "FY2019": 1344, "FY2018": 2044}),
    ("DATA", "- fee income", {"FY2025": 2921, "FY2024": 2758, "FY2023": 2594, "FY2022": 2606, "FY2021": 2706, "FY2020": 2674, "FY2019": 2590, "FY2018": 3402}),
    ("DATA", "- fee expense", {"FY2025": -1694, "FY2024": -1483, "FY2023": -1365, "FY2022": -1345, "FY2021": -1293, "FY2020": -1274, "FY2019": -1246, "FY2018": -1358}),
    ("DATA", "Net income from financial instruments held for trading or managed on a fair value basis", {"FY2025": 4938, "FY2024": 4726, "FY2023": 3395, "FY2022": 2875, "FY2021": 1733, "FY2020": 1758, "FY2019": 2055, "FY2018": 2733}),
    ("DATA", "Net income/(expense) from assets and liabilities of insurance businesses (IFRS 17, FY2023 on)", {"FY2025": 1017, "FY2024": 857, "FY2023": 1168, "FY2022": -1369, "FY2020": 254, "FY2019": 1288, "FY2018": -604}),
    ("DATA", "Changes in fair value of long-term debt and related derivatives", {"FY2025": -4, "FY2024": 2, "FY2023": -63, "FY2022": 102, "FY2021": -8, "FY2020": 17, "FY2019": -8, "FY2018": 5}),
    ("DATA", "Changes in fair value of other financial instruments mandatorily measured at FVTPL", {"FY2025": 288, "FY2024": 413, "FY2023": 284, "FY2022": 143, "FY2021": 493, "FY2020": 285, "FY2019": 547, "FY2018": 511}),
    ("DATA", "Net (losses)/gains from financial investments", {"FY2025": -1088, "FY2024": 22, "FY2023": -84, "FY2022": -60, "FY2021": 60, "FY2020": 95, "FY2019": 38, "FY2018": 12}),
    ("DATA", "Net insurance premium income (IFRS 4, pre-FY2023)", {"FY2022": 1787, "FY2021": 1906, "FY2020": 1559, "FY2019": 2147, "FY2018": 2005}),
    ("DATA", "(Losses)/gains recognised on Assets held for sale", {"FY2025": -6, "FY2024": -100, "FY2023": 296, "FY2022": -1947}),
    ("DATA", "Insurance finance (expense)/income (IFRS 17, FY2023 on)", {"FY2025": -1090, "FY2024": -984, "FY2023": -1184}),
    ("DATA", "Insurance service result (IFRS 17, FY2023 on)", {"FY2025": 164, "FY2024": 171, "FY2023": 124}),
    ("DATA", "Other operating income", {"FY2025": 158, "FY2024": 106, "FY2023": 190, "FY2022": 356, "FY2021": 594, "FY2020": 417, "FY2019": 516, "FY2018": 580}),
    ("TOTAL", "Total operating income (IFRS 4 presentation, pre-FY2023)", {"FY2022": 5052, "FY2021": 9159, "FY2020": 7683, "FY2019": 9410, "FY2018": 10946}),
    ("DATA", "Net insurance claims, benefits paid and movement in liabilities to policyholders (IFRS 4, pre-FY2023)", {"FY2022": -406, "FY2021": -3039, "FY2020": -1783, "FY2019": -3366, "FY2018": -1478}),
    ("TOTAL", "Net operating income before change in expected credit losses", {"FY2025": 6878, "FY2024": 7473, "FY2023": 7506, "FY2022": 4646, "FY2021": 6120, "FY2020": 5900, "FY2019": 6044, "FY2018": 9468}),
    ("DATA", "Change in expected credit losses and other credit impairment charges", {"FY2025": -154, "FY2024": -163, "FY2023": -169, "FY2022": -222, "FY2021": 174, "FY2020": -808, "FY2019": -124, "FY2018": -159}),
    ("TOTAL", "Net operating income", {"FY2025": 6724, "FY2024": 7310, "FY2023": 7337, "FY2022": 4424, "FY2021": 6294, "FY2020": 5092, "FY2019": 5920, "FY2018": 9309}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Employee compensation and benefits", {"FY2025": -1983, "FY2024": -1672, "FY2023": -1706, "FY2022": -1762, "FY2021": -2023, "FY2020": -2340, "FY2019": -2225, "FY2018": -2529}),
    ("DATA", "General and administrative expenses", {"FY2025": -4363, "FY2024": -3440, "FY2023": -3375, "FY2022": -3463, "FY2021": -3265, "FY2020": -3092, "FY2019": -3034, "FY2018": -4501}),
    ("DATA", "Depreciation and impairment of PP&E and right-of-use assets", {"FY2025": -125, "FY2024": -71, "FY2023": -45, "FY2022": -103, "FY2021": -110, "FY2020": -372, "FY2019": -210, "FY2018": -150}),
    ("DATA", "Amortisation and impairment of intangible assets", {"FY2025": -433, "FY2024": -77, "FY2023": -16, "FY2022": -25, "FY2021": -64, "FY2020": -901, "FY2019": -161, "FY2018": -171}),
    ("DATA", "Goodwill impairment", {"FY2019": -1152}),
    ("TOTAL", "Total operating expenses", {"FY2025": -6904, "FY2024": -5260, "FY2023": -5142, "FY2022": -5353, "FY2021": -5462, "FY2020": -6705, "FY2019": -6782, "FY2018": -7351}),
    ("TOTAL", "Operating (loss)/profit", {"FY2025": -180, "FY2024": 2050, "FY2023": 2195, "FY2022": -929, "FY2021": 832, "FY2020": -1613, "FY2019": -862, "FY2018": 1958}),
    ("DATA", "Share of profit/(loss) in associates and joint ventures", {"FY2025": 61, "FY2024": 18, "FY2023": -43, "FY2022": -30, "FY2021": 191, "FY2020": -1, "FY2019": -10, "FY2018": 16}),
    ("TOTAL", "(Loss)/profit before tax", {"FY2025": -119, "FY2024": 2068, "FY2023": 2152, "FY2022": -959, "FY2021": 1023, "FY2020": -1614, "FY2019": -872, "FY2018": 1974}),
    ("DATA", "Tax (charge)/credit", {"FY2025": -462, "FY2024": -785, "FY2023": -427, "FY2022": 561, "FY2021": 23, "FY2020": 136, "FY2019": -119, "FY2018": -442}),
    ("TOTAL", "(Loss)/profit for the year", {"FY2025": -581, "FY2024": 1283, "FY2023": 1725, "FY2022": -398, "FY2021": 1046, "FY2020": -1478, "FY2019": -991, "FY2018": 1532}),
    ("DATA", "- attributable to the parent company", {"FY2025": -591, "FY2024": 1253, "FY2023": 1703, "FY2022": -408, "FY2021": 1041, "FY2020": -1488, "FY2019": -1013, "FY2018": 1506}),
    ("DATA", "- attributable to non-controlling interests", {"FY2025": 10, "FY2024": 30, "FY2023": 22, "FY2022": 10, "FY2021": 5, "FY2020": 10, "FY2019": 22, "FY2018": 26}),
    ("SECTION", "Other comprehensive income, net of tax", {}),
    ("DATA", "Debt instruments at fair value through other comprehensive income", {"FY2025": 830, "FY2024": 144, "FY2023": 439, "FY2022": -454, "FY2021": -237, "FY2020": 213, "FY2019": 121, "FY2018": 83}),
    ("DATA", "Equity instruments designated at fair value through other comprehensive income", {"FY2025": 17, "FY2024": -2, "FY2023": -1, "FY2022": 0, "FY2021": 2, "FY2020": 2, "FY2019": 2, "FY2018": 36}),
    ("DATA", "Cash flow hedges", {"FY2025": 209, "FY2024": 103, "FY2023": 663, "FY2022": -943, "FY2021": -165, "FY2020": 118, "FY2019": 65, "FY2018": -16}),
    ("DATA", "Finance (expense)/income from insurance contracts (IFRS 17, FY2023 on)", {"FY2025": -510, "FY2024": -108, "FY2023": -298}),
    ("DATA", "Exchange differences", {"FY2025": 754, "FY2024": -491, "FY2023": -302, "FY2022": 701, "FY2021": -603, "FY2020": 467, "FY2019": -707, "FY2018": 100}),
    ("DATA", "Remeasurement of defined benefit asset/liability", {"FY2025": 44, "FY2024": -2, "FY2023": -2, "FY2022": 38, "FY2021": 44, "FY2020": -8, "FY2019": 12, "FY2018": 171}),
    ("DATA", "Changes in fair value of financial liabilities designated at FV due to own credit risk", {"FY2025": -127, "FY2024": -40, "FY2023": -132, "FY2022": 329, "FY2021": 2, "FY2020": 67, "FY2019": -251, "FY2018": 504}),
    ("TOTAL", "Other comprehensive income/(expense) for the year, net of tax", {"FY2025": 1217, "FY2024": -396, "FY2023": 367, "FY2022": -329, "FY2021": -957, "FY2020": 859, "FY2019": -758, "FY2018": 878}),
    ("TOTAL", "Total comprehensive income/(expense) for the year", {"FY2025": 636, "FY2024": 887, "FY2023": 2092, "FY2022": -727, "FY2021": 89, "FY2020": -619, "FY2019": -1749, "FY2018": 2410}),
]

INCOME_STATEMENT_SOURCES = (
    "Sources - HSBC Bank plc's own Consolidated income statement and Consolidated statement of comprehensive "
    "income, £m, from each year's own Annual Report and Accounts (each year's own originally-published "
    "figures, not a later restated comparative):\n"
    f"FY2025: HSBC Bank plc Annual Report and Accounts 2025, p.90-91 - {AR2025_URL}\n"
    f"FY2024: HSBC Bank plc Annual Report and Accounts 2024, p.115-116 - {AR2024_URL}\n"
    f"FY2023: HSBC Bank plc Annual Report and Accounts 2023, p.106-107 - {AR2023_URL}\n"
    f"FY2022: HSBC Bank plc Annual Report and Accounts 2022, p.114-115 - {AR2022_URL}\n"
    f"FY2021: HSBC Bank plc Annual Report and Accounts 2021, p.108-109 - {AR2021_URL}\n"
    f"FY2020: HSBC Bank plc Annual Report and Accounts 2020, p.108-109 - {AR2020_URL}\n"
    f"FY2019: HSBC Bank plc Annual Report and Accounts 2019, p.95-96 - {AR2019_URL}\n"
    f"FY2018: HSBC Bank plc Annual Report and Accounts 2018, p.87-88 - {AR2018_URL}\n\n"
    "HSBC Bank plc adopted IFRS 17 'Insurance Contracts' from 1 January 2023, replacing IFRS 4 - this is a "
    "genuine presentation-structure change, not a gap: FY2018-FY2022's own income statements use the IFRS 4 "
    "structure ('Net insurance premium income', 'Total operating income', 'Net insurance claims paid'), while "
    "FY2023-FY2025 use the IFRS 17 structure ('Insurance finance income/expense', 'Insurance service result') - "
    "both shown on their own basis rather than forced into one template. 'Net operating income before change in "
    "expected credit losses' is the one line comparable in substance across the whole transition ('total "
    "operating income' minus 'net insurance claims paid' under IFRS 4 equals this line's own value under IFRS 4, "
    "confirmed by cross-checking both years' totals). A one-off £1,152m goodwill impairment charge appears only "
    "in FY2019's own operating expenses (a dedicated 'Goodwill impairment' row not present in any other year) - "
    "confirmed against FY2019's own Annual Report, not a recurring item.\n\n"
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
    ("TOTAL", "Balance at 31 Dec 2017 (per FY2018's own statement, pre-IFRS 9 transition)", (797, 3781, 36140, 2744, 43462, 587, 44049)),
    ("DATA", "IFRS 9 transition impact (1 Jan 2018)", (0, 0, -283, -249, -532, 0, -532)),
    ("TOTAL", "Balance at 1 Jan 2018 (restated for IFRS 9, per FY2018's own statement)", (797, 3781, 35857, 2495, 42930, 587, 43517)),
    ("DATA", "Profit for the period", (None, None, 1506, None, 1506, 26, 1532)),
    ("DATA", "Other comprehensive income, net of tax", (None, None, 677, 204, 881, -3, 878)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, 2183, 204, 2387, 23, 2410)),
    ("DATA", "Capital securities issued during the period", (None, 818, None, None, 818, None, 818)),
    ("DATA", "Dividends paid to shareholders", (None, None, -13044, None, -13044, -28, -13072)),
    ("DATA", "Transfer", (None, -2196, None, None, -2196, None, -2196)),
    ("DATA", "Net impact of equity-settled share-based payments", (None, None, 17, None, 17, None, 17)),
    ("DATA", "Capital contribution from the parent company", (None, None, 3377, None, 3377, None, 3377)),
    ("DATA", "Change in business combinations and other movements", (None, None, 218, -3, 215, -51, 164)),
    ("DATA", "Tax on items taken directly to equity", (None, None, 41, None, 41, None, 41)),
    ("DATA", "Group reorganisation reserve (GRR) recognised on ring-fencing (see source note)", (None, None, None, -7667, -7667, None, -7667)),
    ("TOTAL", "Balance at 31 Dec 2018 (per FY2018's own statement)", (797, 2403, 28649, -4971, 26878, 531, 27409)),
    ("DATA", "Loss for the period", (None, None, -1013, None, -1013, 22, -991)),
    ("DATA", "Other comprehensive (expense)/income, net of tax", (None, None, -238, -494, -732, -26, -758)),
    ("TOTAL", "Total comprehensive (expense)/income for the year", (None, None, -1251, -494, -1745, -4, -1749)),
    ("DATA", "Capital securities issued during the period", (None, 1319, None, None, 1319, None, 1319)),
    ("DATA", "Dividends to the parent company", (None, None, -2985, None, -2985, -17, -3002)),
    ("DATA", "Net impact of equity-settled share-based payments", (None, None, 16, None, 16, None, 16)),
    ("DATA", "Change in business combinations and other movements", (None, None, 20, None, 20, -1, 19)),
    ("TOTAL", "Balance at 31 Dec 2019 (per FY2019's own statement)", (797, 3722, 24449, -5465, 23503, 509, 24012)),
    ("DATA", "Loss for the year", (None, None, -1488, None, -1488, 10, -1478)),
    ("DATA", "Other comprehensive income, net of tax", (None, None, 56, 779, 835, 24, 859)),
    ("TOTAL", "Total comprehensive income/(loss) for the year", (None, None, -1432, 779, -653, 34, -619)),
    ("DATA", "Dividends to the parent company", (None, None, -263, None, -263, None, -263)),
    ("DATA", "Net impact of equity-settled share-based payments", (None, None, 11, None, 11, None, 11)),
    ("DATA", "Capital contribution from the parent company", (None, None, 1000, None, 1000, None, 1000)),
    ("DATA", "Change in business combinations and other movements", (None, None, 64, 4, 68, -360, -292)),
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
    f"FY2025 movements: HSBC Bank plc Annual Report and Accounts 2025, p.93 - {AR2025_URL}\n"
    f"FY2020 movements: HSBC Bank plc Annual Report and Accounts 2020, p.112 - {AR2020_URL}\n"
    f"FY2019 movements: HSBC Bank plc Annual Report and Accounts 2019, p.98-99 - {AR2019_URL}\n"
    f"FY2018 movements (including the 1 Jan 2018 IFRS 9 transition impact and the FY2018 Group reorganisation "
    f"reserve recognition): HSBC Bank plc Annual Report and Accounts 2018, p.91 - {AR2018_URL}\n\n"
    "'Other reserves' combines the Financial assets at FVOCI reserve, Cash flow hedging reserve, Foreign "
    "exchange reserve, Group reorganisation reserve, and (from FY2023) Insurance finance reserve columns shown "
    "separately in the Bank's own 11-column statement - verified this combined total ties exactly to the "
    "Balance Sheet's own 'Other reserves' line for every year before finalizing. Equity reconciliation ladder "
    "confirmed: each year's own closing balance ties exactly to the next year's own opening balance and to that "
    "year's own Balance Sheet Total equity, with the one exception below. The FY2018 floor bridges a genuine, "
    "source-disclosed IFRS 9 transition impact at 1 Jan 2018 (£(532)m) and a genuine, much larger one-off 'Group "
    "reorganisation reserve' recognition of £(7,667)m during FY2018 itself, arising from the 1 July 2018 UK "
    "ring-fencing transfer of retail/commercial customers to the newly created HSBC UK Bank plc - both shown as "
    "their own explicit rows rather than absorbed into 'other movements'.\n\n"
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
    ("DATA", "Profit/(loss) before tax", {"FY2025": -119, "FY2024": 2068, "FY2023": 2152, "FY2022": -959, "FY2021": 1023, "FY2020": -1614, "FY2019": -872, "FY2018": 1974}),
    ("DATA", "Depreciation, amortisation and impairment", {"FY2025": 558, "FY2024": 148, "FY2023": 61, "FY2022": 128, "FY2021": 174, "FY2020": 1273, "FY2019": 1523, "FY2018": 321}),
    ("DATA", "Net loss/(gain) from investing activities", {"FY2025": 1098, "FY2024": 83, "FY2023": -66, "FY2022": 2002, "FY2021": -62, "FY2020": -99, "FY2019": -59, "FY2018": -14}),
    ("DATA", "Share of (profit)/loss in associates and joint ventures", {"FY2025": -61, "FY2024": -18, "FY2023": 43, "FY2022": 30, "FY2021": -191, "FY2020": 1, "FY2019": 10, "FY2018": -16}),
    ("DATA", "Change in expected credit losses gross of recoveries and other credit impairment charges", {"FY2025": 154, "FY2024": 165, "FY2023": 161, "FY2022": 253, "FY2021": -171, "FY2020": 810, "FY2019": 130, "FY2018": 220}),
    ("DATA", "Provisions including pensions", {"FY2025": 1184, "FY2024": 78, "FY2023": 132, "FY2022": 192, "FY2021": 104, "FY2020": 424, "FY2019": 231, "FY2018": -41}),
    ("DATA", "Share-based payment expense", {"FY2025": 81, "FY2024": 61, "FY2023": 58, "FY2022": 46, "FY2021": 96, "FY2020": 78, "FY2019": 88, "FY2018": 99}),
    ("DATA", "Other non-cash items included in (loss)/profit before tax", {"FY2025": -155, "FY2024": -180, "FY2023": -165, "FY2022": -242, "FY2021": -198, "FY2020": 135, "FY2019": -19, "FY2018": 40}),
    ("DATA", "Elimination of exchange differences", {"FY2025": -3416, "FY2024": 4883, "FY2023": 4426, "FY2022": -6714, "FY2021": 4926, "FY2020": -2527, "FY2019": 4001, "FY2018": -2074}),
    ("DATA", "- change in net trading securities and derivatives", {"FY2025": -16933, "FY2024": -13266, "FY2023": -15528, "FY2022": -6213, "FY2021": 8157, "FY2020": 8070, "FY2019": -1310, "FY2018": 7837}),
    ("DATA", "- change in loans and advances to banks and customers", {"FY2025": -3077, "FY2024": -455, "FY2023": 4245, "FY2022": -2717, "FY2021": 11149, "FY2020": 6780, "FY2019": 3441, "FY2018": -6377}),
    ("DATA", "- change in reverse repurchase agreements - non-trading", {"FY2025": -13896, "FY2024": 9341, "FY2023": -13531, "FY2022": 6251, "FY2021": 9538, "FY2020": 16084, "FY2019": -7293, "FY2018": -22893}),
    ("DATA", "- change in financial assets designated and otherwise mandatorily measured at fair value", {"FY2025": -3139, "FY2024": -1954, "FY2023": -3296, "FY2022": 2729, "FY2021": -2429, "FY2020": 735, "FY2019": 787, "FY2018": -2246}),
    ("DATA", "- change in other assets", {"FY2025": -3313, "FY2024": 4734, "FY2023": -5707, "FY2022": -7329, "FY2021": 10924, "FY2020": -7513, "FY2019": -12074, "FY2018": -1769}),
    ("DATA", "- change in deposits by banks and customer accounts", {"FY2025": 23219, "FY2024": 14113, "FY2023": 7548, "FY2022": 19835, "FY2021": 7940, "FY2020": 28262, "FY2019": -4141, "FY2018": -347}),
    ("DATA", "- change in repurchase agreements - non-trading", {"FY2025": 6374, "FY2024": -13813, "FY2023": 20516, "FY2022": 5641, "FY2021": -7643, "FY2020": -14482, "FY2019": 2803, "FY2018": 8807}),
    ("DATA", "- change in debt securities in issue", {"FY2025": -6638, "FY2024": 6018, "FY2023": 6175, "FY2022": -1060, "FY2021": -7943, "FY2020": -7668, "FY2019": 2318, "FY2018": 9435}),
    ("DATA", "- change in financial liabilities designated at fair value", {"FY2025": 5234, "FY2024": 4937, "FY2023": 4042, "FY2022": -1822, "FY2021": -7191, "FY2020": -402, "FY2019": 4390, "FY2018": 1982}),
    ("DATA", "- change in other liabilities", {"FY2025": 3534, "FY2024": -10026, "FY2023": -7506, "FY2022": 21297, "FY2021": -12295, "FY2020": 5432, "FY2019": 9539, "FY2018": 5394}),
    ("DATA", "- dividend received from associates", {"FY2025": 18, "FY2023": 15, "FY2022": 7}),
    ("DATA", "- contributions paid to defined benefit plans", {"FY2025": -28, "FY2024": -20, "FY2023": -5, "FY2022": -10, "FY2021": -24, "FY2020": -22, "FY2019": -13, "FY2018": -20}),
    ("DATA", "- tax received/(paid)", {"FY2025": 92, "FY2024": -1088, "FY2023": -140, "FY2022": 845, "FY2021": -581, "FY2020": 142, "FY2019": -287, "FY2018": -473}),
    ("TOTAL", "Changes in operating assets and liabilities - subtotal", {"FY2025": -8553, "FY2024": -1479, "FY2023": -3172, "FY2022": 37454, "FY2021": 9602, "FY2020": 35418, "FY2019": -1840, "FY2018": -670}),
    ("TOTAL", "Net cash from operating activities", {"FY2025": -9229, "FY2024": 5809, "FY2023": 3630, "FY2022": 32190, "FY2021": 15303, "FY2020": 33899, "FY2019": 3193, "FY2018": -161}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of financial investments", {"FY2025": -45055, "FY2024": -32587, "FY2023": -26586, "FY2022": -13227, "FY2021": -18890, "FY2020": -21037, "FY2019": -26200, "FY2018": -29235}),
    ("DATA", "Proceeds from the sale and maturity of financial investments", {"FY2025": 33969, "FY2024": 23272, "FY2023": 15497, "FY2022": 20490, "FY2021": 25027, "FY2020": 17417, "FY2019": 24304, "FY2018": 26888}),
    ("DATA", "Net cash flows from the purchase and sale of property, plant and equipment", {"FY2025": -18, "FY2024": -16, "FY2023": -31, "FY2022": -20, "FY2021": 52, "FY2020": -70, "FY2019": -58, "FY2018": -111}),
    ("DATA", "Net investment in intangible assets", {"FY2025": -393, "FY2024": -149, "FY2023": -125, "FY2022": -28, "FY2021": -45, "FY2020": -150, "FY2019": -385, "FY2018": -433}),
    ("DATA", "Net cash outflow from investment in associates and acquisition of businesses and subsidiaries", {"FY2025": -25, "FY2024": -955, "FY2023": -1161, "FY2022": -29, "FY2021": -85, "FY2020": -371, "FY2019": -49, "FY2018": -227}),
    ("DATA", "Net cash flow on disposal of subsidiaries, businesses, associates and joint ventures", {"FY2025": 39, "FY2024": -8631, "FY2023": -394, "FY2021": 0, "FY2020": 57, "FY2019": 0, "FY2018": -29371}),
    ("TOTAL", "Net cash from investing activities", {"FY2025": -11483, "FY2024": -19066, "FY2023": -12800, "FY2022": 7186, "FY2021": 6059, "FY2020": -4154, "FY2019": -2388, "FY2018": -32489}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Issue of ordinary share capital and other equity instruments", {"FY2025": 276, "FY2024": 2782, "FY2023": 584, "FY2022": 628, "FY2020": 0, "FY2019": 1319, "FY2018": 818}),
    ("DATA", "Redemption of other equity instruments", {"FY2024": -213, "FY2021": 0, "FY2020": -318}),
    ("DATA", "Subordinated loan capital issued", {"FY2025": 2702, "FY2024": 2777, "FY2023": 3246, "FY2022": 3111, "FY2021": 10466, "FY2020": 0, "FY2019": 6736, "FY2018": 12274}),
    ("DATA", "Subordinated loan capital repaid", {"FY2025": -1277, "FY2024": -474, "FY2023": -2693, "FY2022": -2248, "FY2021": -10902, "FY2020": -18, "FY2019": -7100, "FY2018": -12765}),
    ("DATA", "Dividends to the parent company", {"FY2025": -1951, "FY2024": -535, "FY2023": -961, "FY2022": -1052, "FY2021": -194, "FY2020": -263, "FY2019": -2985, "FY2018": -13044}),
    ("DATA", "Funds received from the parent company", {"FY2022": 1465, "FY2020": 1000, "FY2018": 3512}),
    ("DATA", "Dividends paid to non-controlling interests", {"FY2025": -16, "FY2024": -11, "FY2023": -7, "FY2022": -2, "FY2021": -1, "FY2020": 0, "FY2019": -17, "FY2018": -28}),
    ("TOTAL", "Net cash from financing activities", {"FY2025": -266, "FY2024": 4326, "FY2023": 169, "FY2022": 1902, "FY2021": -631, "FY2020": 401, "FY2019": -2047, "FY2018": -9233}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": -20978, "FY2024": -8931, "FY2023": -9001, "FY2022": 41278, "FY2021": 20731, "FY2020": 30146, "FY2019": -1242, "FY2018": -41883}),
    ("DATA", "Cash and cash equivalents at 1 Jan", {"FY2025": 162928, "FY2024": 177037, "FY2023": 189907, "FY2022": 140923, "FY2021": 125304, "FY2020": 92338, "FY2019": 97058, "FY2018": 129737}),
    ("DATA", "Exchange difference in respect of cash and cash equivalents", {"FY2025": 4949, "FY2024": -5178, "FY2023": -3869, "FY2022": 7706, "FY2021": -5112, "FY2020": 2820, "FY2019": -3478, "FY2018": 1148}),
    ("TOTAL", "Cash and cash equivalents at 31 Dec", {"FY2025": 146899, "FY2024": 162928, "FY2023": 177037, "FY2022": 189907, "FY2021": 140923, "FY2020": 125304, "FY2019": 92338, "FY2018": 89002}),
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
LOANS_GROSS = {"FY2025": 80558, "FY2024": 83524, "FY2023": 76579, "FY2022": 73717, "FY2021": 92331, "FY2020": 102960, "FY2019": 109428, "FY2018": 113306}
LOANS_ECL = {"FY2025": -700, "FY2024": -858, "FY2023": -1088, "FY2022": -1103, "FY2021": -1154, "FY2020": -1469, "FY2019": -1037, "FY2018": -1342}
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
    f"FY2021: HSBC Bank plc Annual Report and Accounts 2021, p.34 - {AR2021_URL}\n"
    f"FY2020: HSBC Bank plc Annual Report and Accounts 2020, p.34 - {AR2020_URL}\n"
    f"FY2019: HSBC Bank plc Annual Report and Accounts 2019, p.30 - {AR2019_URL}\n"
    f"FY2018: HSBC Bank plc Annual Report and Accounts 2018, p.36 - {AR2018_URL}\n\n"
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
# Sheet: KM1 Key Metrics (KM1-016)
#
# HSBC Bank plc prints the template as "Table 1: Key metrics (KM1/IFRS9-FL)" in
# its FY2022-FY2025 Pillar 3 Disclosures. Four points that shaped this
# transcription, each verified against the PDFs themselves:
#
# (a) ENTITY. HSBC Holdings plc, HSBC Bank plc and HSBC UK Bank plc each publish
#     their OWN Pillar 3 Disclosures, and HSBC Innovation Bank Limited is a
#     fourth entity again. Every figure below comes from a document whose own
#     running header reads "HSBC Bank plc Pillar 3 Disclosures at 31 December
#     <year>" and whose table preamble names HSBC Bank plc - not the Holdings
#     group document and not the ring-fenced bank's.
#
# (b) THE COLUMN SET IS FIVE DATES, ONLY ONE OF WHICH IS THIS YEAR-END. Each
#     annual edition prints 31 Dec / 30 Sep / 30 Jun / 31 Mar of its own year and
#     then the prior 31 Dec. Only the leftmost (31 December of the edition's own
#     reporting year) column is taken. The three intra-year quarter-ends are not
#     year-ends at all, and the prior-31-Dec column is a comparative, which
#     HSBC restates: the FY2023 edition shows 31 Dec 2022 CET1 as £18,411m where
#     the FY2022 edition's own reporting column shows £19,184m (IFRS 17 adoption
#     and the equity-accounting change for non-financial-institution
#     subsidiaries). FY2022 here is £19,184m, its own edition's figure.
#
# (c) THE BASIS SPLITS *WITHIN* A COLUMN. Rows 1-14e are on the regulatory scope
#     of consolidation, but every edition footnotes rows 15-20 with "These LCR
#     and NSFR amounts relate to HSBC Bank plc as a single entity and are not
#     produced on a consolidated basis" (FY2022 fn 7, FY2023 fn 7, and in the
#     table preamble itself for FY2024 and FY2025). So one column carries a
#     consolidated capital/leverage block above a SOLO liquidity block. Both are
#     reproduced where the bank printed them; neither is relabelled.
#
# (d) ROW SET DRIFT, and one real basis break.
#     * HSBC prints only the template rows that carry a value - its own footnote
#       says the references "identify lines prescribed in the relevant PRA
#       template where applicable and where there is a value". So rows UK-7a,
#       UK-7b, UK-7c, UK-8a, UK-9a, 10 and UK-10a never appear in any edition.
#       They are shown blank here: not printed by the bank, not values we failed
#       to find.
#     * The unnumbered "...as if IFRS 9 transitional arrangements had not been
#       applied" rows (the IFRS9-FL half of the combined template) appear in the
#       FY2022-FY2024 editions and are dropped from the FY2025 edition, because
#       the IFRS 9 transitional arrangements ended on 1 January 2025 and the
#       transitional and end-point figures became identical.
#     * Rows 14a-14e and EU-14d/EU-14e first appear in the FY2023 edition (HSBC
#       Bank plc became an LREQ firm on 1 January 2023, per that edition's own
#       footnote 5), so they are blank for FY2022.
#     * THE 1 JANUARY 2022 LEVERAGE BASIS BREAK is visible inside the FY2022
#       edition itself: rows 13/14 ("excluding claims on central banks") print
#       "N/A" for the 31 Dec 2021 comparative, and the old CRR measure is given
#       instead on two separate unnumbered rows under their own heading
#       "Leverage ratio (under Capital Requirements Regulation)", which in turn
#       print "N/A" for 31 Dec 2022. Both captions are kept as separate rows and
#       the two series are never merged. The old-basis rows carry no value in any
#       column of this sheet: their only figures (£536,518m and 4.2%) belong to
#       that edition's 31 Dec 2021 COMPARATIVE column, which rule 1 forbids using.
#
# (e) FY2021-FY2018 ARE BLANK, and this is "the template is not used", not "no
#     Pillar 3 is published" and not an access failure. All four of those
#     editions were downloaded (HTTP 200, application/pdf, %PDF magic bytes) and
#     read: each leads with "Table 1: Comparison of own funds, capital and
#     leverage ratios, with and without the application of transitional
#     arrangements for IFRS 9 (IFRS9-FL)", a DIFFERENT and shorter template with
#     its own row numbering 1-17. It looks KM1-adjacent - it carries CET1/Tier
#     1/Total capital, Total RWAs, the three capital ratios and a leverage ratio
#     - but it has no SREP row, no buffer block, no LCR and no NSFR, and its
#     numbers 1-17 are IFRS9-FL's own, not KM1's. Mapping it onto KM1 row numbers
#     would invent a correspondence HSBC never published, so it is not used here.
#     The FY2022 edition's own footnote 3 says the SREP and buffer disclosures
#     "have been implemented from 1 January 2022 and are based on the PRA's
#     disclosure templates and instructions which came into force at that time",
#     which is the positive reason the template is absent before then.
# ---------------------------------------------------------------
km1_rows = [
    ("SECTION", "Available capital (£m)", {}),
    ("DATA", "1    Common equity tier 1 ('CET1') capital",
     {"FY2025": 20063, "FY2024": 21896, "FY2023": 19230, "FY2022": 19184}),
    ("DATA", "     CET1 capital as if IFRS 9 transitional arrangements had not been applied",
     {"FY2024": 21896, "FY2023": 19230, "FY2022": 19165}),
    ("DATA", "2    Tier 1 capital",
     {"FY2025": 24272, "FY2024": 25828, "FY2023": 23124, "FY2022": 23077}),
    ("DATA", "     Tier 1 capital as if IFRS 9 transitional arrangements had not been applied",
     {"FY2024": 25828, "FY2023": 23124, "FY2022": 23057}),
    ("DATA", "3    Total capital",
     {"FY2025": 41473, "FY2024": 41306, "FY2023": 37131, "FY2022": 36187}),
    ("DATA", "     Total capital as if IFRS 9 transitional arrangements had not been applied",
     {"FY2024": 41306, "FY2023": 37131, "FY2022": 36167}),
    ("SECTION", "Risk-weighted assets ('RWAs') (£m)", {}),
    ("DATA", "4    Total RWAs",
     {"FY2025": 112340, "FY2024": 112251, "FY2023": 107449, "FY2022": 114171}),
    ("DATA", "     Total RWAs as if IFRS 9 transitional arrangements had not been applied",
     {"FY2024": 112251, "FY2023": 107449, "FY2022": 114154}),
    ("SECTION", "Capital ratios (%)", {}),
    ("DATA", "5    CET1",
     {"FY2025": "17.9", "FY2024": "19.5", "FY2023": "17.9", "FY2022": "16.8"}),
    ("DATA", "     CET1 as if IFRS 9 transitional arrangements had not been applied",
     {"FY2024": "19.5", "FY2023": "17.9", "FY2022": "16.8"}),
    ("DATA", "6    Tier 1",
     {"FY2025": "21.6", "FY2024": "23.0", "FY2023": "21.5", "FY2022": "20.2"}),
    ("DATA", "     Tier 1 as if IFRS 9 transitional arrangements had not been applied",
     {"FY2024": "23.0", "FY2023": "21.5", "FY2022": "20.2"}),
    ("DATA", "7    Total capital",
     {"FY2025": "36.9", "FY2024": "36.8", "FY2023": "34.6", "FY2022": "31.7"}),
    ("DATA", "     Total capital as if IFRS 9 transitional arrangements had not been applied",
     {"FY2024": "36.8", "FY2023": "34.6", "FY2022": "31.7"}),
    ("SECTION", "Additional own funds requirements based on Supervisory Review and Evaluation Process ('SREP') as a percentage of RWAs (%)", {}),
    ("DATA", "UK-7a    Additional CET1 SREP requirements", {}),
    ("DATA", "UK-7b    Additional AT1 SREP requirements", {}),
    ("DATA", "UK-7c    Additional T2 SREP requirements", {}),
    ("DATA", "UK-7d    Total SREP own funds requirements",
     {"FY2025": "8.0", "FY2024": "8.0", "FY2023": "8.0", "FY2022": "8.0"}),
    ("SECTION", "Combined buffer requirement as a percentage of RWAs (%)", {}),
    ("DATA", "8    Capital conservation buffer requirement",
     {"FY2025": "2.5", "FY2024": "2.5", "FY2023": "2.5", "FY2022": "2.5"}),
    ("DATA", "UK-8a    Conservation buffer due to macro-prudential or systemic risk identified at the level of a Member State", {}),
    ("DATA", "9    Institution specific countercyclical capital buffer",
     {"FY2025": "1.0", "FY2024": "1.1", "FY2023": "0.9", "FY2022": "0.3"}),
    ("DATA", "UK-9a    Systemic risk buffer", {}),
    ("DATA", "10    Global Systemically Important Institution buffer", {}),
    ("DATA", "UK-10a    Other Systemically Important Institution buffer", {}),
    ("DATA", "11    Combined buffer requirement",
     {"FY2025": "3.5", "FY2024": "3.6", "FY2023": "3.4", "FY2022": "2.8"}),
    ("DATA", "UK-11a    Overall capital requirements",
     {"FY2025": "11.5", "FY2024": "11.6", "FY2023": "11.4", "FY2022": "10.8"}),
    ("DATA", "12    CET1 available after meeting the total SREP own funds requirements",
     {"FY2025": "13.4", "FY2024": "15.0", "FY2023": "13.4", "FY2022": "12.3"}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "13    Total exposure measure excluding claims on central banks (£m)",
     {"FY2025": 534474, "FY2024": 468557, "FY2023": 455852, "FY2022": 417587}),
    ("DATA", "14    Leverage ratio excluding claims on central banks (%)",
     {"FY2025": "4.5", "FY2024": "5.5", "FY2023": "5.1", "FY2022": "5.5"}),
    ("SECTION", "Leverage ratio (under Capital Requirements Regulation) — pre-1 January 2022 basis, FY2022 edition only", {}),
    ("DATA", "     Total leverage ratio exposure measure (£m)", {"FY2022": "N/A"}),
    ("DATA", "     Leverage ratio (%)", {"FY2022": "N/A"}),
    ("SECTION", "Additional own funds requirements to address risks of excessive leverage (as a percentage of leverage ratio total exposure amount)", {}),
    ("DATA", "     Average exposure measure excluding claims on central banks (£m)",
     {"FY2023": 449733}),
    ("DATA", "14a    Fully loaded expected credit losses ('ECL') accounting model leverage ratio excluding claims on central banks (%)",
     {"FY2025": "4.5", "FY2024": "5.5", "FY2023": "5.1"}),
    ("DATA", "14b    Leverage ratio including claims on central banks (%)",
     {"FY2025": "3.7", "FY2024": "4.3", "FY2023": "4.0"}),
    ("DATA", "14c    Average leverage ratio excluding claims on central banks (%)",
     {"FY2025": "4.5", "FY2024": "5.1", "FY2023": "5.3"}),
    ("DATA", "14d    Average leverage ratio including claims on central banks (%)",
     {"FY2025": "3.7", "FY2024": "4.1", "FY2023": "4.1"}),
    ("DATA", "14e    Countercyclical leverage ratio buffer (%)",
     {"FY2025": "0.4", "FY2024": "0.4", "FY2023": "0.3"}),
    ("DATA", "EU-14d    Leverage ratio buffer requirement (%)",
     {"FY2025": "0.4", "FY2024": "0.4", "FY2023": "0.3"}),
    ("DATA", "EU-14e    Overall leverage ratio requirements (%)",
     {"FY2025": "3.7", "FY2024": "3.7", "FY2023": "3.6"}),
    ("SECTION", "Liquidity coverage ratio ('LCR') — HSBC Bank plc as a single entity, NOT consolidated", {}),
    ("DATA", "15    Total high-quality liquid assets (£m)",
     {"FY2025": 110242, "FY2024": 107749, "FY2023": 105524, "FY2022": 104491}),
    ("DATA", "UK-16a    Cash outflows – total weighted value (£m)",
     {"FY2025": 117263, "FY2024": 116388, "FY2023": 120627, "FY2022": 122833}),
    ("DATA", "UK-16b    Cash inflows – total weighted value (£m)",
     {"FY2025": 42617, "FY2024": 43615, "FY2023": 49517, "FY2022": 49831}),
    ("DATA", "16    Total net cash outflow (£m)",
     {"FY2025": 74646, "FY2024": 72773, "FY2023": 71110, "FY2022": 73002}),
    ("DATA", "17    LCR ratio (%)",
     {"FY2025": "148", "FY2024": "148", "FY2023": "148", "FY2022": "143.1"}),
    ("SECTION", "Net stable funding ratio ('NSFR') — HSBC Bank plc as a single entity, NOT consolidated", {}),
    ("DATA", "18    Total available stable funding (£m)",
     {"FY2025": 131347, "FY2024": 131324, "FY2023": 116303, "FY2022": 107679}),
    ("DATA", "19    Total required stable funding (£m)",
     {"FY2025": 114788, "FY2024": 114149, "FY2023": 100094, "FY2022": 93310}),
    ("DATA", "20    NSFR ratio (%)",
     {"FY2025": "114", "FY2024": "115", "FY2023": "116", "FY2022": "115.4"}),
]

KM1_SOURCES = (
    "Sources - HSBC Bank plc's OWN entity-level Pillar 3 Disclosures, Table 1 'Key metrics "
    "(KM1/IFRS9-FL)'. Each year is taken from the 31 December column of the edition in which "
    "that year is the reporting year - never from a later edition's comparative. Every PDF was "
    "re-downloaded for this ticket and verified by HTTP 200, Content-Type application/pdf and "
    "%PDF magic bytes:\n"
    f"FY2025: Pillar 3 Disclosures at 31 December 2025, Table 1, p.3 (PDF p.4) - {P32025_URL}\n"
    f"FY2024: Pillar 3 Disclosures at 31 December 2024, Table 1, p.3 (PDF p.4) - {P32024_URL}\n"
    f"FY2023: Pillar 3 Disclosures at 31 December 2023, Table 1, p.4 (PDF p.5) - {P32023_URL}\n"
    f"FY2022: Pillar 3 Disclosures at 31 December 2022, Table 1, p.2 (PDF p.3) - {P32022_URL}\n"
    f"FY2021: no KM1 - Pillar 3 Disclosures at 31 December 2021 - {P32021_URL}\n"
    f"FY2020: no KM1 - Pillar 3 Disclosures at 31 December 2020 - {P32020_URL}\n"
    f"FY2019: no KM1 - Pillar 3 Disclosures at 31 December 2019 - {P32019_URL}\n"
    f"FY2018: no KM1 - Pillar 3 Disclosures at 31 December 2018 - {P32018_URL}\n\n"
    "LATEST-EDITION CHECK, 2026-09-16: checked HSBC's own investor-relations subsidiaries "
    "reporting page (hsbc.com/investors/results-and-announcements/all-reporting/subsidiaries), "
    "not this project's cited URLs and not Wayback. The newest HSBC Bank plc documents listed "
    "there are the Pillar 3 Disclosures at 31 March 2026 (a Q1 disclosure) and at 30 June 2026 "
    "(an interim disclosure), plus the Interim Report 2026. The newest ANNUAL edition remains "
    "the Pillar 3 Disclosures at 31 December 2025 and the Annual Report and Accounts 2025, both "
    "published 25 February 2026 - which this workbook already holds. FY2026 is not a complete "
    "financial year, so no new year column is added. Checked, none newer.\n\n"
    "ENTITY, and why it matters here: HSBC publishes SEPARATE Pillar 3 Disclosures for HSBC "
    "Holdings plc (the listed group, out of scope), HSBC Bank plc (this entity, FRN 114216), "
    "HSBC UK Bank plc (FRN 765112, the ring-fenced bank) and HSBC Innovation Bank Limited (FRN "
    "543146). All four appear on the same hsbc.com downloads page. Every figure on this sheet "
    "comes from a document whose own running header reads 'HSBC Bank plc Pillar 3 Disclosures "
    "at 31 December <year>' and whose table preamble names HSBC Bank plc.\n\n"
    "COLUMN SELECTION: each annual edition's Table 1 prints FIVE dated columns - 31 Dec, 30 Sep, "
    "30 Jun and 31 Mar of its own year, then the prior 31 Dec. Only the leftmost 31 December "
    "column is taken. The three intra-year columns are quarter-ends, not year-ends, and the "
    "prior-31-Dec column is a comparative that HSBC restates: the FY2023 edition shows 31 Dec "
    "2022 CET1 capital as GBP18,411m where the FY2022 edition's own reporting column shows "
    "GBP19,184m (IFRS 17 adoption from 1 January 2023, and the September 2022 move to equity "
    "accounting for investments in non-financial-institution subsidiaries). The FY2022 column "
    "here is GBP19,184m, from FY2022's own edition, which is also what the CET1 Capital metric "
    "sheet in this workbook carries.\n\n"
    "BASIS SPLITS WITHIN EACH COLUMN - read this before comparing rows: the capital, RWA, buffer "
    "and leverage rows (1-14e) are on HSBC Bank plc's regulatory scope of consolidation, but the "
    "liquidity rows (15-20) are HSBC Bank plc SOLO. Every edition says so in terms - 'These LCR "
    "and NSFR amounts relate to HSBC Bank plc as a single entity and are not produced on a "
    "consolidated basis' (FY2022 footnote 7; FY2023 footnote 7; stated in the table preamble "
    "itself in FY2024 and FY2025). So a single column of this sheet is consolidated above the "
    "LCR heading and solo below it. Both are reproduced where the bank printed them.\n\n"
    "ROW SET DRIFT (map rule 4 - a row the bank did not print is blank, which is not zero and "
    "not a row we failed to find):\n"
    "  * HSBC prints only template rows that carry a value. Its own asterisk footnote reads "
    "'The references in this and subsequent tables identify lines prescribed in the relevant PRA "
    "template where applicable and where there is a value.' Rows UK-7a, UK-7b, UK-7c, UK-8a, "
    "UK-9a, 10 and UK-10a therefore appear in NO edition. They are kept as blank rows here so "
    "the sheet matches the template a reader would cross-refer to.\n"
    "  * The unnumbered '...as if IFRS 9 transitional arrangements had not been applied' rows - "
    "the IFRS9-FL half of the combined KM1/IFRS9-FL template, which HSBC prints without row "
    "numbers - appear in the FY2022, FY2023 and FY2024 editions and are DROPPED from the FY2025 "
    "edition, because the IFRS 9 transitional arrangements ended on 1 January 2025 (and CRR II "
    "grandfathering on 28 June 2025), making the transitional and end-point figures identical. "
    "FY2025 blanks on those rows mean 'not printed', not 'nil'.\n"
    "  * Rows 14a-14e, EU-14d and EU-14e first appear in the FY2023 edition: 'From 1 January "
    "2023 HSBC Bank plc became an LREQ firm subject to Average leverage ratio requirement' "
    "(FY2023 footnote 5). They are blank for FY2022.\n"
    "  * The unnumbered 'Average exposure measure excluding claims on central banks' row is "
    "printed in the FY2023 edition only (GBP449,733m) and not in FY2024 or FY2025.\n\n"
    "THE 1 JANUARY 2022 LEVERAGE BASIS BREAK is visible inside the FY2022 edition itself and is "
    "NOT merged here. Rows 13 and 14 ('...excluding claims on central banks') print 'N/A' in "
    "that edition's 31 Dec 2021 comparative column, and the pre-2022 measure is given instead on "
    "two separate unnumbered rows under their own heading 'Leverage ratio (under Capital "
    "Requirements Regulation)' - which in turn print 'N/A' in the 31 Dec 2022 column, reproduced "
    "as 'N/A' above. Those old-basis rows carry no figure anywhere on this sheet because their "
    "only values (GBP536,518m and 4.2%) sit in that edition's 31 Dec 2021 COMPARATIVE column, "
    "and FY2021's own edition has no KM1 to take them from.\n\n"
    "WHY FY2021-FY2018 ARE BLANK - 'the template is not used', NOT 'no Pillar 3 is published', "
    "and NOT a blocked fetch. All four editions were downloaded and read in full for this ticket "
    "(each HTTP 200, application/pdf, %PDF verified). Each of them leads with 'Table 1: "
    "Comparison of own funds, capital and leverage ratios, with and without the application of "
    "transitional arrangements for IFRS 9 (IFRS9-FL)' - a DIFFERENT, shorter template carrying "
    "its own row numbering 1-17. It is deceptively KM1-like (CET1/Tier 1/Total capital, Total "
    "RWAs, the three capital ratios, a leverage ratio) but has NO SREP row, NO buffer block, NO "
    "LCR and NO NSFR, and its numbers 1-17 are IFRS9-FL's, not KM1's. Re-labelling it onto KM1 "
    "row numbers would invent a correspondence HSBC never published, so it is not used. The "
    "positive reason for the absence is in the FY2022 edition's own footnote 3: the SREP and "
    "buffer disclosures 'have been implemented from 1 January 2022 and are based on the PRA's "
    "disclosure templates and instructions which came into force at that time'. The FY2018-FY2021 "
    "figures on the single-metric sheets in this workbook come from those years' IFRS9-FL, OV1 "
    "and own-funds tables, not from a KM1.\n\n"
    "PRECISION AS PRINTED (map rule 3): the FY2022 edition prints LCR as 143.1 and NSFR as 115.4 "
    "to one decimal place; the FY2023-FY2025 editions print both as whole numbers. That is the "
    "bank's own house style changing, and is left as published. Ratio rows are stored as the "
    "digits HSBC printed, without a percent sign, because HSBC carries the unit in the section "
    "heading rather than on the row.\n\n"
    "A SOURCE DEFECT, RECORDED NOT CORRECTED (map rule 7) - and the explanation for the three "
    "cross-check warnings this sheet raises. HSBC's IFRS9-FL rows are unnumbered, and in the "
    "'Available capital' block they read 'CET1 capital as if...', 'Tier 1 capital as if...' and "
    "'Total capital as if...', while in the 'Capital ratios' block they read 'CET1 as if...', "
    "'Tier 1 as if...' and 'Total capital as if...'. The CET1 and Tier 1 pairs are distinguishable "
    "by their wording; THE TWO 'Total capital as if IFRS 9 transitional arrangements had not been "
    "applied' ROWS ARE WORD-FOR-WORD IDENTICAL, and are told apart only by which section heading "
    "they sit under - one is a GBP m amount, the other a percentage. Both are reproduced verbatim "
    "here rather than disambiguated, because inventing distinguishing wording would be this "
    "project editing a prescribed template. The consequence is that verify_workbook.py's "
    "check_km1_against_metric_sheets(), which falls back to matching an unnumbered row by its "
    "label prefix, maps BOTH of them to the 'Total Capital' (GBP m) metric sheet and reports the "
    "ratio one as disagreeing for FY2024 (36.8 vs 41,306), FY2023 (34.6 vs 37,131) and FY2022 "
    "(31.7 vs 36,187). Those three warnings are expected and are not transcription errors: 36.8, "
    "34.6 and 31.7 are the fully-loaded TOTAL CAPITAL RATIOS, and they tie exactly to the Total "
    "Capital Ratio metric sheet; 41,306, 37,131 and 36,187 are the fully-loaded total capital "
    "AMOUNTS, and the amount row above ties exactly to the Total Capital metric sheet. No figure "
    "has been changed to silence the warning.\n\n"
    "LABEL DRIFT, recorded not normalised: the FY2025 edition writes row 9 as 'Institution "
    "specific countercyclical capital buffer (‘CCyB’)' where FY2022-FY2024 write it "
    "without the abbreviation; the FY2025 edition moves the '(£m)' unit from the individual row "
    "labels up into its section headings. The row labels above follow the FY2022-FY2024 form.\n\n"
    + ENTITY_NOTE
)

bw.add_km1_sheet(
    title="HSBC Bank plc — KM1 Key Metrics",
    subtitle="HSBC Bank plc's own published UK KM1 template ('Table 1: Key metrics (KM1/IFRS9-FL)'), "
             "reproduced in the bank's row order with its own row references, labels and printed "
             "precision. Amounts £m, ratios as printed (%). Rows 1-14e are on the regulatory scope of "
             "consolidation; rows 15-20 are HSBC Bank plc SOLO, per the bank's own footnote. FY2021 and "
             "earlier are blank because HSBC Bank plc's Pillar 3 Disclosures for those years do not use "
             "the KM1 template - see the source note.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    source_height=420,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=48, source_height=190)


metric(
    "CET1 Capital", "£m",
    [("Common equity tier 1 (CET1) capital", {"FY2025": 20063, "FY2024": 21896, "FY2023": 19230, "FY2022": 19184, "FY2021": 18007, "FY2020": 18042, "FY2019": 17791, "FY2018": 19831})],
)

metric(
    "CET1 Ratio", "% of RWA",
    [("CET1 ratio", {"FY2025": "17.9%", "FY2024": "19.5%", "FY2023": "17.9%", "FY2022": "16.8%", "FY2021": "17.3%", "FY2020": "14.7%", "FY2019": "14.2%", "FY2018": "13.8%"})],
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 24272, "FY2024": 25828, "FY2023": 23124, "FY2022": 23077, "FY2021": 21869, "FY2020": 22165, "FY2019": 22130, "FY2018": 23079})],
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "21.6%", "FY2024": "23.0%", "FY2023": "21.5%", "FY2022": "20.2%", "FY2021": "21.0%", "FY2020": "18.1%", "FY2019": "17.6%", "FY2018": "16.0%"})],
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 41473, "FY2024": 41306, "FY2023": 37131, "FY2022": 36187, "FY2021": 33036, "FY2020": 33438, "FY2019": 34929, "FY2018": 37671})],
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "36.9%", "FY2024": "36.8%", "FY2023": "34.6%", "FY2022": "31.7%", "FY2021": "31.7%", "FY2020": "27.3%", "FY2019": "27.9%", "FY2018": "26.2%"})],
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted assets", {"FY2025": 112340, "FY2024": 112251, "FY2023": 107449, "FY2022": 114171, "FY2021": 104314, "FY2020": 122392, "FY2019": 125413, "FY2018": 143875})],
)

# ---------------------------------------------------------------
# Sheet: RWA Breakdown - HSBC Bank plc's own entity-level UK OV1 table
# ---------------------------------------------------------------
rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding counterparty credit risk)", {"FY2025": 56633, "FY2024": 57911, "FY2023": 58620, "FY2022": 65365, "FY2021": 60450, "FY2020": 69671, "FY2019": 75389, "FY2018": 88822}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 20958, "FY2024": 18201, "FY2023": 17037, "FY2022": 17834, "FY2021": 16389, "FY2020": 19342, "FY2019": 21173, "FY2018": 24669}),
    ("DATA", "Settlement risk", {"FY2025": 41, "FY2024": 27, "FY2023": 29, "FY2022": 147, "FY2021": 45, "FY2020": 2, "FY2019": 113}),
    ("DATA", "Securitisation exposures in the non-trading book", {"FY2025": 2908, "FY2024": 3545, "FY2023": 3363, "FY2022": 3456, "FY2021": 3734, "FY2020": 4744, "FY2019": 3819}),
    ("DATA", "Market risk (position, FX and commodities)", {"FY2025": 16799, "FY2024": 18519, "FY2023": 15525, "FY2022": 15822, "FY2021": 9828, "FY2020": 14589, "FY2019": 13107, "FY2018": 17534}),
    ("DATA", "Operational risk", {"FY2025": 15001, "FY2024": 14048, "FY2023": 12875, "FY2022": 11547, "FY2021": 10512, "FY2020": 11245, "FY2019": 11812, "FY2018": 12850}),
    ("DATA", "Amounts below the thresholds for deduction (FY2020/FY2021 own separate line only)", {"FY2021": 3356, "FY2020": 2799}),
    ("TOTAL", "Total RWAs", {"FY2025": 112340, "FY2024": 112251, "FY2023": 107449, "FY2022": 114171, "FY2021": 104314, "FY2020": 122392, "FY2019": 125413, "FY2018": 143875}),
]

RWA_BREAKDOWN_SOURCES = (
    "Sources - HSBC Bank plc's own entity-level 'Overview of risk-weighted exposure amounts' (UK OV1 template) "
    "from the official HSBC Bank plc Pillar 3 Disclosures, each year's own originally-published figures:\n"
    f"FY2025: HSBC Bank plc Pillar 3 Disclosures at 31 December 2025, Table 4, p.10 - {P32025_URL}\n"
    f"FY2024: HSBC Bank plc Pillar 3 Disclosures at 31 December 2024, Table 4, p.10 - {P32024_URL}\n"
    f"FY2023: HSBC Bank plc Pillar 3 Disclosures at 31 December 2023, Table 7, p.13 - {P32023_URL}\n"
    f"FY2022: HSBC Bank plc Pillar 3 Disclosures at 31 December 2022, Table 2 'Overview of risk-weighted "
    f"exposure amounts (OV1)', p.3 - {P32022_URL}. CORRECTION (2026-09-12 independent re-verification): this "
    f"sheet previously stated FY2022's category breakdown was 'genuinely not disclosed' and that 'no RWA-by-"
    f"risk-type breakdown table exists in this vintage of the document' - that claim was factually wrong; "
    f"Table 2 (OV1) is present on p.3 of the same document already cited elsewhere on this sheet and gives "
    f"the full category split. Figures used here: Credit risk (excl. CCR) 65,365; CCR 17,834; Settlement risk "
    f"147; Securitisation 3,456; Market risk 15,822; Operational risk 11,547 - these sum exactly to the "
    f"document's own printed Total of 114,171, which also ties to this workbook's Total RWAs sheet. The "
    f"document's own line 24 ('of which: Amounts below the thresholds for deduction', £6,025m) is a footnoted "
    f"memo item nested inside the Credit risk row (as in FY2023-FY2025), not a separately-addable component - "
    f"left blank for FY2022 for the same reason it's blank FY2023-FY2025.\n"
    f"FY2021: HSBC Bank plc Pillar 3 Disclosures at 31 December 2021, Table 2, p.3 - {P32021_URL}\n"
    f"FY2020: HSBC Bank plc Pillar 3 Disclosures at 31 December 2020, Table 2 'Overview of RWAs', p.9 - {P32020_URL}\n"
    f"FY2019: HSBC Bank plc Pillar 3 Disclosures at 31 December 2019, Table 2 'Overview of RWAs (OV1)', p.3 - {P32019_URL}\n"
    f"FY2018: HSBC Bank plc Pillar 3 Disclosures at 31 December 2018, Table 3 'Pillar 1 overview', p.3 - {P32018_URL}\n\n"
    "Each year's Total ties exactly to this workbook's Total RWAs metric sheet. FY2021's document (pre-dates "
    "the KM1/OV1 template used from FY2022 onward) shows 'Amounts below the thresholds for deduction' as its "
    "own explicit row; FY2023-FY2025's documents embed the equivalent amount inside the Credit risk row (as a "
    "footnoted 'of which' figure) rather than a separate addable row - left blank for those years rather than "
    "double-counted or force-matched to FY2021's structure. FY2020's own document (already on the OV1 "
    "template) also shows this row explicitly. FY2018's own document pre-dates the OV1 template entirely and "
    "uses a coarser 4-category 'Pillar 1 overview' table: its own 'Credit risk' figure (£88,822m) folds in "
    "what FY2019 onward's OV1 template breaks out separately as 'Securitisation exposures' (confirmed by "
    "cross-checking FY2019's own FY2018 comparative OV1 column: £84,135m credit risk + £4,687m securitisation "
    "= £88,822m), and its own 'Counterparty credit risk' figure (£24,669m) folds in what later templates show "
    "as 'Settlement risk' (£24,620m + £49m = £24,669m) - FY2018's own combined figures are used here rather "
    "than force-split using a later year's finer categories, with Settlement risk and Securitisation left "
    "blank for FY2018 only. The Total (£143,875m) is identical either way.\n\n"
    + ENTITY_NOTE
)

bw.add_rwa_breakdown_sheet(
    title="HSBC Bank plc — RWA Breakdown",
    subtitle="£m, entity-level Pillar 3 UK OV1 template (or FY2018's coarser pre-OV1 equivalent).",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=88,
    source_height=310,
    unit_suffix=" (£m)",
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio", {"FY2025": "4.5%", "FY2024": "5.5%", "FY2023": "5.1%", "FY2022": "5.5%", "FY2021": "4.1%", "FY2020": "3.8%", "FY2019": "3.8%", "FY2018": "3.9%"})],
    note="Two genuine basis changes bite across this range. First: FY2021 is disclosed on the Capital "
         "Requirements Regulation basis (total leverage ratio exposure £535,562m, ratio 4.1%). From FY2022 "
         "onward, HSBC Bank plc switched to the CRR II end-point basis 'excluding claims on central banks' (a "
         "narrower exposure measure) - FY2022's own report shows this new-basis figure (exposure £417,587m, "
         "ratio 5.5%) with no FY2021 comparative on the same basis, so FY2021 above is left on its own "
         "originally-disclosed (different) basis rather than forced onto the newer definition. Second, further "
         "back: FY2018's own Pillar 3 Disclosures state the leverage ratio 'is calculated using the CRD IV "
         "end-point basis for additional tier 1 capital' (exposure £570.0bn, ratio 3.9%), while FY2019's own "
         "document states that 'effective 30 June 2019, the leverage ratio is calculated using the CRR II end "
         "point basis for capital' (exposure £571.3bn, ratio 3.8%) - FY2019 and FY2020 (exposure £565.0bn, "
         "ratio 3.8%) share this CRR II end-point basis with FY2021, so the only leverage-basis break in the "
         "FY2018-FY2021 span is at the FY2018/FY2019 boundary; each year's own originally-disclosed figure is "
         "used throughout rather than restated onto a single common basis.",
)

metric(
    "LCR", "%, 12-month average",
    [("Liquidity coverage ratio", {"FY2025": "148%", "FY2024": "148%", "FY2023": "148%", "FY2022": "143.1%"})],
    note="Not disclosed for FY2018-FY2021: HSBC Bank plc's own Pillar 3 Disclosures for these years pre-date "
         "the KM1 template and PRA's entity-level LCR/NSFR disclosure requirement, which 'came into effect on "
         "1 January 2022' per the FY2022 Pillar 3 Disclosures' own footnote - confirmed genuinely absent (each "
         "of the FY2018/FY2019/FY2020 documents was read in full and discusses LCR/NSFR only qualitatively, "
         "with no numeric ratio), not an access gap. Reported on a 12-month rolling average basis (this "
         "project's standard convention).",
)

metric(
    "NSFR", "%, average of preceding 4 quarters",
    [("Net stable funding ratio", {"FY2025": "114%", "FY2024": "115%", "FY2023": "116%", "FY2022": "115.4%"})],
    note="Not disclosed for FY2018-FY2021 - same reason as the LCR sheet (pre-dates the PRA's entity-level "
         "NSFR disclosure requirement, effective 1 January 2022).",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={
        "MREL Ratio": "No MREL figure or mention appears anywhere in any of HSBC Bank plc's own Pillar 3 "
                      "Disclosures FY2018-FY2025 - HSBC Bank plc is not itself a resolution entity under the "
                      "Bank of England's Single Point of Entry resolution strategy for the HSBC group (that "
                      "role sits with HSBC Holdings plc at the top of the group), so no entity-level MREL "
                      "requirement or ratio applies here - the same pattern as RBS plc/Coutts & Company's "
                      "relationship to the wider NatWest Group.",
    },
)

# ---------------------------------------------------------------
# Additional interim Pillar 3 disclosures
# ---------------------------------------------------------------
# The standard metric sheets above intentionally remain ANNUAL - one fixed
# column per 31 December year-end.  HSBC Bank plc also publishes quarterly
# Pillar 3 disclosures under Article 433a, each carrying a full UK KM1 at a
# non-year-end reporting date.  Those observations are kept here, in a separate
# wide matrix with periods across the columns, so that a half-year or quarterly
# reporting date is never mixed into a year-end column.
P3_2026_Q1_URL = ("https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2026/1q/pdfs/"
                  "hsbc-bank-plc/260508-hsbc-bank-plc-pillar-3-disclosures-at-31-march-2026.pdf")
P3_2026_H1_URL = ("https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2026/interim/pdfs/"
                  "hsbc-bank-plc/260810-hsbc-bank-plc-pillar-3-disclosures-at-30-june-2026.pdf")

INTERIM_PERIODS = [
    ("2026 H1", "H1", "HSBC Bank plc Pillar 3 Disclosures at 30 June 2026", "p.3, Table 1", P3_2026_H1_URL),
    ("2026 Q1", "Q1", "HSBC Bank plc Pillar 3 Disclosures at 31 March 2026", "p.3, Table 1", P3_2026_Q1_URL),
]

# Order of each list matches INTERIM_PERIODS above (30 Jun 2026, then 31 Mar 2026).
INTERIM_VALUES = {
    "CET1 Capital": [19180, 19113],
    "Tier 1 Capital": [23783, 23321],
    "Total Capital": [41356, 41581],
    "Total RWAs": [112200, 109459],
    "CET1 Ratio": ["17.1%", "17.5%"],
    "Tier 1 Ratio": ["21.2%", "21.3%"],
    "Total Capital Ratio": ["36.9%", "38.0%"],
    "Leverage Ratio": ["4.1%", "4.2%"],
    "LCR": ["139%", "142%"],
    "NSFR": ["112%", "112%"],
}

interim_rows = []
_interim_basis = "HSBC Bank plc consolidated entity-level"
for _metric_name, _values in INTERIM_VALUES.items():
    _unit = "%" if _metric_name in {"CET1 Ratio", "Tier 1 Ratio", "Total Capital Ratio",
                                    "Leverage Ratio", "LCR", "NSFR"} else "£m"
    for _idx, (_period, _dtype, _document, _page, _url) in enumerate(INTERIM_PERIODS):
        interim_rows.append(
            (_period, _dtype, _metric_name, _values[_idx], _unit, _interim_basis, _url, _page)
        )

bw.add_wide_interim_sheet(
    "Interim Pillar 3",
    rows=interim_rows,
    hyperlink_cells={(i, 6): row[6] for i, row in enumerate(interim_rows)},
    title="HSBC Bank plc — Interim Pillar 3",
    subtitle="Entity-level quarterly/half-year KM1 observations at 31 March 2026 and 30 June 2026; "
             "annual year-end values remain on the standard metric sheets.",
    note=(
        "Why this sheet exists, and why there is no FY2026 annual column anywhere in this workbook. "
        "HSBC Bank plc has a 31 DECEMBER year-end, so the FY2026 reporting date (31 December 2026) had not "
        "been reached when this workbook was built (18 September 2026) and no FY2026 Annual Report or annual "
        "Pillar 3 exists. What the bank HAS published for 2026 is its quarterly Pillar 3 disclosures under "
        "Article 433a: at 31 March 2026 (published 8 May 2026) and at 30 June 2026 (published 10 August "
        "2026). Those are HALF-YEAR and FIRST-QUARTER reporting dates, not year-end ones, so they are "
        "recorded here with their dates stated rather than placed in an annual column - a 30 June figure and "
        "a 31 December figure are not the same measurement and must not share a column. The 30 September "
        "2026 quarter had not ended, so no Q3 2026 disclosure exists yet; that is an absence in the "
        "publication calendar, not a document we were unable to obtain.\n\n"
        "Each period is taken from the edition in which that date is the REPORTING date, not from the other "
        "edition's comparative column. Both editions agree digit-for-digit on 31 March 2026.\n\n"
        "Scope. This sheet deliberately covers 2026 only. HSBC Bank plc has published quarterly Pillar 3 "
        "disclosures for earlier years too, and the 2026 editions reprint 31 Mar / 30 Jun / 30 Sep 2025 as "
        "comparatives, but those earlier periods are NOT backfilled here from a later edition's comparative "
        "column. A backfill would need each period's own edition; it was not in scope for this pass and its "
        "absence is a scope boundary, not a finding that the bank did not publish.\n\n"
        "Restatement check. Both 2026 editions reprint 31 December 2025 as a comparative and print it "
        "identically to the FY2025 figures already held on this workbook's annual metric sheets: CET1 "
        "£20,063m, tier 1 £24,272m, total capital £41,473m, RWAs £112,340m, ratios 17.9% / 21.6% / 36.9%, "
        "leverage ratio 4.5%, LCR 148%, NSFR 114%. No restatement of any previously held figure was found, "
        "so no annual figure was changed. The 31 March 2026 edition's footnote 1 records that from 30 June "
        "2025 the regulatory valuation of tier 2 capital includes accrued interest and that prior periods "
        "have NOT been restated - a prospective change, affecting no figure already in this workbook.\n\n"
        "Basis. Capital, RWA and ratio rows are KM1 rows 1-7. The leverage ratio row is KM1 row 14, "
        "'Leverage ratio excluding claims on central banks', the same basis as the annual Leverage Ratio "
        "sheet for FY2022 onwards. LCR is the average of the preceding 12 months and NSFR the average of "
        "the preceding four quarter-ends, as the bank states above its own table. MREL is not disclosed at "
        "this entity level in any edition - see the MREL Ratio sheet."
    ),
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 707696, "FY2024": 727330, "FY2023": 702970, "FY2022": 717353, "FY2021": 596611, "FY2020": 681150, "FY2019": 636491, "FY2018": 604958}),
        ("Loans and advances to customers", {"FY2025": 79858, "FY2024": 82666, "FY2023": 75491, "FY2022": 72614, "FY2021": 91177, "FY2020": 101491, "FY2019": 108391, "FY2018": 111964}),
        ("Total liabilities", {"FY2025": 681732, "FY2024": 700277, "FY2023": 678465, "FY2022": 693337, "FY2021": 572896, "FY2020": 657301, "FY2019": 612479, "FY2018": 577549}),
        ("Total equity", {"FY2025": 25964, "FY2024": 27053, "FY2023": 24505, "FY2022": 24016, "FY2021": 23715, "FY2020": 23849, "FY2019": 24012, "FY2018": 27409}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Net operating income", {"FY2025": 6724, "FY2024": 7310, "FY2023": 7337, "FY2022": 4424, "FY2021": 6294, "FY2020": 5092, "FY2019": 5920, "FY2018": 9309}),
        ("Total operating expenses", {"FY2025": -6904, "FY2024": -5260, "FY2023": -5142, "FY2022": -5353, "FY2021": -5462, "FY2020": -6705, "FY2019": -6782, "FY2018": -7351}),
        ("(Loss)/profit before tax", {"FY2025": -119, "FY2024": 2068, "FY2023": 2152, "FY2022": -959, "FY2021": 1023, "FY2020": -1614, "FY2019": -872, "FY2018": 1974}),
        ("(Loss)/profit for the year", {"FY2025": -581, "FY2024": 1283, "FY2023": 1725, "FY2022": -398, "FY2021": 1046, "FY2020": -1478, "FY2019": -991, "FY2018": 1532}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Total comprehensive income/(expense) for the year", {"FY2025": 636, "FY2024": 887, "FY2023": 2092, "FY2022": -727, "FY2021": 89, "FY2020": -619, "FY2019": -1749, "FY2018": 2410}),
        ("Total equity (closing)", {"FY2025": 25964, "FY2024": 27053, "FY2023": 24505, "FY2022": 24016, "FY2021": 23715, "FY2020": 23849, "FY2019": 24012, "FY2018": 27409}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash from operating activities", {"FY2025": -9229, "FY2024": 5809, "FY2023": 3630, "FY2022": 32190, "FY2021": 15303, "FY2020": 33899, "FY2019": 3193, "FY2018": -161}),
        ("Net cash from investing activities", {"FY2025": -11483, "FY2024": -19066, "FY2023": -12800, "FY2022": 7186, "FY2021": 6059, "FY2020": -4154, "FY2019": -2388, "FY2018": -32489}),
        ("Net cash from financing activities", {"FY2025": -266, "FY2024": 4326, "FY2023": 169, "FY2022": 1902, "FY2021": -631, "FY2020": 401, "FY2019": -2047, "FY2018": -9233}),
        ("Cash and cash equivalents at 31 Dec", {"FY2025": 146899, "FY2024": 162928, "FY2023": 177037, "FY2022": 189907, "FY2021": 140923, "FY2020": 125304, "FY2019": 92338, "FY2018": 89002}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "17.9%", "FY2024": "19.5%", "FY2023": "17.9%", "FY2022": "16.8%", "FY2021": "17.3%", "FY2020": "14.7%", "FY2019": "14.2%", "FY2018": "13.8%"}),
        ("Tier 1 Ratio", {"FY2025": "21.6%", "FY2024": "23.0%", "FY2023": "21.5%", "FY2022": "20.2%", "FY2021": "21.0%", "FY2020": "18.1%", "FY2019": "17.6%", "FY2018": "16.0%"}),
        ("Total Capital Ratio", {"FY2025": "36.9%", "FY2024": "36.8%", "FY2023": "34.6%", "FY2022": "31.7%", "FY2021": "31.7%", "FY2020": "27.3%", "FY2019": "27.9%", "FY2018": "26.2%"}),
        ("Leverage Ratio", {"FY2025": "4.5%", "FY2024": "5.5%", "FY2023": "5.1%", "FY2022": "5.5%", "FY2021": "4.1%", "FY2020": "3.8%", "FY2019": "3.8%", "FY2018": "3.9%"}),
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
