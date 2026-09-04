import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/01311315/filing-history/MzUyMTMxMjk3OWFkaXF6a2N4/document?format=pdf&download=0"
AR2025_WEBSITE_URL = "https://www.htb.co.uk/htbcontent/uploads/2026/04/HTB_Annual_Report_2025.pdf"
AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/01311315/filing-history/MzQ2NTc0NTU3N2FkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/01311315/filing-history/MzQyNDU2MzAzMmFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/01311315/filing-history/MzM4ODU3ODUzOWFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/01311315/filing-history/MzM0MjI1MzEyMmFkaXF6a2N4/document?format=pdf&download=0"

P3_2025_URL = "https://www.htb.co.uk/htbcontent/uploads/2026/04/HTB_Pillar_3_Disclosures_2025.pdf"
P3_2024_URL = "https://www.htb.co.uk/htbcontent/uploads/2025/07/HTB_Pillar_3_Disclosures_2024.pdf"
P3_2023_URL = "https://www.htb.co.uk/htbcontent/uploads/2024/06/HTB_Pillar_3_Disclosures_2023.pdf"
P3_2022_URL = "https://www.htb.co.uk/htbcontent/uploads/2023/08/Hampshire-Trust-Bank-HTB-2022-Pillar-3-Disclosures.pdf"
P3_2021_URL = "https://www.htb.co.uk/htbcontent/uploads/2022/07/Hampshire-Trust-Bank-HTB-2021-Pillar-3-Disclosures.pdf"

STATEMENTS_ENTITY_NOTE = (
    "Balance Sheet, Profit & Loss and Statement of Changes in Equity all use the Bank (parent-entity, "
    "non-consolidated) column, matching the entity-level basis used throughout this workbook. Every "
    "year's own originally-published figures are used (e.g. FY2023 comes from HTB's own FY2023 Annual "
    "Report, FY2024 from its own FY2024 report), not a later restated comparative column - confirmed "
    "identical between each year's own report and the next year's comparative column in every case "
    "checked. FY2021 predates any Group consolidation (first subsidiary acquired during FY2022) and "
    "predates HTB's use of cash-flow hedge accounting - no Cash flow hedge reserve, Investment in "
    "subsidiaries, or Other equity instruments (non-controlling interest) balance exists that year. "
    "Corporation tax asset is only broken out as its own Balance Sheet line from FY2025 onward - FY2024 "
    "and earlier years fold it into Other assets (confirmed: FY2024's Other assets of 227,921 = the "
    "226,100 shown in the FY2025 report's restated FY2024 comparative plus that year's 1,821 Corporation "
    "tax asset, transcribed here on each year's own originally-disclosed basis, i.e. undivided)."
)

ENTITY_NOTE = (
    "All Cash Flow Statement figures use the Bank (parent-entity, non-consolidated) column, matching the "
    "entity-level basis of the Pillar 3 disclosures below. HTB's FY2021 Annual Report predates any Group "
    "consolidation (its first subsidiary was acquired during FY2022, see the Investing Activities section), "
    "so FY2021 presents a single unified Company statement rather than separate Group/Bank columns - that "
    "single column is used here. The FY2025 Companies House filing (the source used for every other year) is "
    "missing page 64 of its own PDF (the Statement of Cash Flows' operating-activities page - printed page "
    "numbers jump 63 to 65 with no page 64 present in the scan); the operating-activities detail for FY2025 "
    "was instead sourced from the identical statement in HTB's own website copy of the same Annual Report, "
    "which is text-native and paginates differently. Every other line item and every other year comes from "
    "the Companies House filings."
)

CASH_FLOW_SOURCES = (
    "Sources - Hampshire Trust Bank Plc's own Consolidated and Bank Statement of Cash Flows (Bank column):\n"
    f"FY2025: Group Annual Report and Accounts 2025 (Companies House, filed 13 May 2026), p.64-65 - {AR2025_URL}\n"
    f"  (operating-activities section from HTB's own website copy of the same report, p.32 - {AR2025_WEBSITE_URL})\n"
    f"FY2024: Annual Report and Accounts for the year ended 31 December 2024 (Companies House, filed 13 May 2025), p.74-75 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Accounts for the year ended 31 December 2023 (Companies House, filed 11 Jun 2024), p.74-75 (FY2023 comparative column) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Accounts for the year ended 31 December 2022 (Companies House, filed 07 Aug 2023), p.61-62 - {AR2022_URL}\n"
    f"FY2021: Annual Report and Accounts for the year ended 31 December 2021 (Companies House, filed 14 Jun 2022), p.54, Statement of Cash flows - {AR2021_URL}\n"
    + ENTITY_NOTE
)


def p3_sources(km1_page="10-11"):
    return (
        "Sources - Hampshire Trust Bank Plc Pillar 3 Disclosures, 'Key Metrics' (KM1) table, Bank column "
        "(Group column used only for LCR/NSFR, which HTB discloses only at consolidated/Group level - 'Liquidity "
        "is managed on a consolidated basis hence only Group metrics are reported'; FY2021's Pillar 3 report "
        "predates the Group/Bank split entirely and shows a single value used for every metric that year):\n"
        f"FY2025: Pillar 3 Disclosures | 31 December 2025, p.{km1_page} - {P3_2025_URL}\n"
        f"FY2024: Pillar 3 Disclosures | 31 December 2024, p.9-10 - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures | 31 December 2023, p.10-11 - {P3_2023_URL}\n"
        f"FY2022: Pillar 3 Disclosures | 31 December 2022, p.10-11 - {P3_2022_URL}\n"
        f"FY2021: Pillar 3 Disclosures | 31 December 2021, Key Metrics table - {P3_2021_URL}\n"
        "MREL is not mentioned anywhere in any year's Pillar 3 disclosure - not publicly disclosed."
    )


bw = BankWorkbook(bank_name="Hampshire Trust Bank Plc", years=YEARS, year_label=YEAR_LABEL, header_color="DD741F")

# ---------------------------------------------------------------
# Sheet: Balance Sheet (Bank / entity-level column)
# ---------------------------------------------------------------
BS_SOURCES = (
    "Sources - Hampshire Trust Bank Plc's own Consolidated and Bank Statement of Financial Position "
    "(Bank column), each year's own originally-published report:\n"
    f"FY2025: Group Annual Report and Accounts 2025 (Companies House, filed 13 May 2026), p.59 - {AR2025_URL}\n"
    f"FY2024: Annual Report and Accounts for the year ended 31 December 2024 (Companies House, filed 13 May 2025), p.69 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Accounts for the year ended 31 December 2023 (Companies House, filed 04 Jun 2024) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Accounts for the year ended 31 December 2022 (Companies House, filed 07 Aug 2023), p.56 - {AR2022_URL}\n"
    f"FY2021: Annual Report and Accounts for the year ended 31 December 2021 (Companies House, filed 14 Jun 2022), p.51, Statement of Financial Position - {AR2021_URL}\n"
    + STATEMENTS_ENTITY_NOTE
)

bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Loans and advances to banks", {
        "FY2025": 679085, "FY2024": 1435307, "FY2023": 476806, "FY2022": 458974, "FY2021": 242323,
    }),
    ("DATA", "Derivative assets held for risk management", {
        "FY2025": 13326, "FY2024": 51588, "FY2023": 75076, "FY2022": 113319, "FY2021": 19458,
    }),
    ("DATA", "Investment securities", {
        "FY2025": 693673, "FY2024": 219980, "FY2023": 234509, "FY2022": 217722, "FY2021": 196712,
    }),
    ("DATA", "Loans and advances to customers - FVTPL", {
        "FY2025": 0, "FY2024": 260, "FY2023": 3305, "FY2022": 4294, "FY2021": 10025,
    }),
    ("DATA", "Loans and advances to customers - at amortised cost", {
        "FY2025": 4540376, "FY2024": 3391908, "FY2023": 2967326, "FY2022": 2243123, "FY2021": 1704683,
    }),
    ("DATA", "Investment in subsidiaries", {
        "FY2025": 11703, "FY2024": 38203, "FY2023": 49422, "FY2022": 49422,
    }),
    ("DATA", "Property, plant and equipment", {
        "FY2025": 2969, "FY2024": 3961, "FY2023": 4969, "FY2022": 1443, "FY2021": 1471,
    }),
    ("DATA", "Right-of-use assets", {
        "FY2025": 1940, "FY2024": 2711, "FY2023": 3602, "FY2022": 685, "FY2021": 1608,
    }),
    ("DATA", "Intangible assets", {
        "FY2025": 13949, "FY2024": 14712, "FY2023": 11732, "FY2022": 9464, "FY2021": 7606,
    }),
    ("DATA", "Corporation tax asset", {
        "FY2025": 4416,
    }),
    ("DATA", "Deferred tax asset", {
        "FY2025": 468, "FY2024": 978, "FY2023": 1414, "FY2022": 2538, "FY2021": 1925,
    }),
    ("DATA", "Other assets", {
        "FY2025": 164494, "FY2024": 227921, "FY2023": 235646, "FY2022": 99498, "FY2021": 4720,
    }),
    ("TOTAL", "Total assets", {
        "FY2025": 6126399, "FY2024": 5387529, "FY2023": 4063807, "FY2022": 3200482, "FY2021": 2190531,
    }),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Derivative liabilities held for risk management", {
        "FY2025": 18715, "FY2024": 22569, "FY2023": 25456, "FY2022": 19136, "FY2021": 4413,
    }),
    ("DATA", "Customer deposits", {
        "FY2025": 5232516, "FY2024": 4526003, "FY2023": 3205681, "FY2022": 2420694, "FY2021": 1633046,
    }),
    ("DATA", "Lease liabilities", {
        "FY2025": 2900, "FY2024": 3409, "FY2023": 3974, "FY2022": 647, "FY2021": 1895,
    }),
    ("DATA", "Central bank facilities", {
        "FY2025": 290000, "FY2024": 295000, "FY2023": 300000, "FY2022": 295000, "FY2021": 295000,
    }),
    ("DATA", "Subordinated liabilities", {
        "FY2025": 81669, "FY2024": 56085, "FY2023": 57768, "FY2022": 30336, "FY2021": 30202,
    }),
    ("DATA", "Provisions", {
        "FY2025": 2150,
    }),
    ("DATA", "Other liabilities", {
        "FY2025": 64082, "FY2024": 109904, "FY2023": 148127, "FY2022": 175805, "FY2021": 37139,
    }),
    ("TOTAL", "Total liabilities", {
        "FY2025": 5692032, "FY2024": 5012970, "FY2023": 3741006, "FY2022": 2941618, "FY2021": 2001695,
    }),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {
        "FY2025": 139828, "FY2024": 139828, "FY2023": 139828, "FY2022": 139828, "FY2021": 139828,
    }),
    ("DATA", "Share premium", {
        "FY2025": 196, "FY2024": 196, "FY2023": 196, "FY2022": 196, "FY2021": 196,
    }),
    ("DATA", "Cash flow hedge reserve", {
        "FY2025": -2182, "FY2024": -2674, "FY2023": -3099, "FY2022": 129,
    }),
    ("DATA", "Retained earnings", {
        "FY2025": 279495, "FY2024": 220179, "FY2023": 168846, "FY2022": 101681, "FY2021": 48812,
    }),
    ("TOTAL", "Total equity, excluding non-controlling interest", {
        "FY2025": 417337, "FY2024": 357529, "FY2023": 305771, "FY2022": 241834, "FY2021": 188836,
    }),
    ("DATA", "Other equity instruments (non-controlling interests)", {
        "FY2025": 17030, "FY2024": 17030, "FY2023": 17030, "FY2022": 17030,
    }),
    ("TOTAL", "Total equity", {
        "FY2025": 434367, "FY2024": 374559, "FY2023": 322801, "FY2022": 258864, "FY2021": 188836,
    }),
    ("TOTAL", "Total liabilities and equity", {
        "FY2025": 6126399, "FY2024": 5387529, "FY2023": 4063807, "FY2022": 3200482, "FY2021": 2190531,
    }),
]

bw.add_balance_sheet_sheet(
    title="Hampshire Trust Bank Plc — Bank Statement of Financial Position",
    subtitle="Bank (parent-entity) column; FY2021 predates Group consolidation - see source note",
    rows=bs_rows,
    sources_text=BS_SOURCES,
    first_col_width=74,
    source_height=190,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss (Bank / entity-level column)
# ---------------------------------------------------------------
PL_SOURCES = (
    "Sources - Hampshire Trust Bank Plc's own Consolidated and Bank Statement of Comprehensive Income "
    "(Bank column), each year's own originally-published report:\n"
    f"FY2025: Group Annual Report and Accounts 2025 (Companies House, filed 13 May 2026), p.58 - {AR2025_URL}\n"
    f"FY2024: Annual Report and Accounts for the year ended 31 December 2024 (Companies House, filed 13 May 2025), p.68 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Accounts for the year ended 31 December 2023 (Companies House, filed 04 Jun 2024), p.59 - {AR2023_URL}\n"
    f"FY2022: Annual Report and Accounts for the year ended 31 December 2022 (Companies House, filed 07 Aug 2023), p.55 - {AR2022_URL}\n"
    f"FY2021: Annual Report and Accounts for the year ended 31 December 2021 (Companies House, filed 14 Jun 2022), p.50, Statement of Comprehensive Income - {AR2021_URL}\n"
    + STATEMENTS_ENTITY_NOTE +
    "\nNet (loss)/gain arising from derecognition of financial assets at amortised cost and Impairment "
    "loss on investments in subsidiaries are only disclosed as separate lines from FY2024 onward - not "
    "applicable/nil in earlier years' own disclosures, left blank rather than assumed zero."
)

pl_rows = [
    ("DATA", "Interest and similar income", {
        "FY2025": 396890, "FY2024": 352194, "FY2023": 245613, "FY2022": 131839, "FY2021": 88508,
    }),
    ("DATA", "Interest expense and similar charges", {
        "FY2025": -229271, "FY2024": -206852, "FY2023": -114551, "FY2022": -33255, "FY2021": -19351,
    }),
    ("TOTAL", "Net interest income", {
        "FY2025": 167619, "FY2024": 145342, "FY2023": 131062, "FY2022": 98584, "FY2021": 69157,
    }),
    ("SECTION", "Other operating income", {}),
    ("DATA", "Fees and commissions income", {
        "FY2025": 3006, "FY2024": 3172, "FY2023": 1459, "FY2022": 2078, "FY2021": 1533,
    }),
    ("DATA", "Fees and commissions payable", {
        "FY2025": -1110, "FY2024": -1406, "FY2023": -1375, "FY2022": -1637, "FY2021": -805,
    }),
    ("DATA", "Net (loss)/gain on loans and other financial assets at fair value through profit or loss", {
        "FY2025": -1010, "FY2024": -315, "FY2023": -2495, "FY2022": 3276, "FY2021": 3175,
    }),
    ("DATA", "Net (loss)/gain arising from derecognition of financial assets at amortised cost", {
        "FY2025": -769, "FY2024": 7275,
    }),
    ("DATA", "Other income", {
        "FY2025": 2887, "FY2024": 3927, "FY2023": 5991, "FY2022": 6512, "FY2021": 9,
    }),
    ("TOTAL", "Operating income", {
        "FY2025": 170623, "FY2024": 157995, "FY2023": 134642, "FY2022": 108813, "FY2021": 73069,
    }),
    ("DATA", "Administrative expenses", {
        "FY2025": -83039, "FY2024": -75545, "FY2023": -69237, "FY2022": -56984, "FY2021": -46313,
    }),
    ("DATA", "Impairment loss on investments in subsidiaries", {
        "FY2025": -26500, "FY2024": -11219,
    }),
    ("DATA", "Impairment gains/(losses) on loans and advances to customers", {
        "FY2025": -9063, "FY2024": -9770, "FY2023": -12498, "FY2022": -7308, "FY2021": 590,
    }),
    ("TOTAL", "Profit before tax and dividends", {
        "FY2025": 52021, "FY2024": 61461, "FY2023": 52907, "FY2022": 44521, "FY2021": 27346,
    }),
    ("DATA", "Interim dividends received", {
        "FY2025": 26500, "FY2024": 11000, "FY2023": 27500, "FY2022": 20000,
    }),
    ("TOTAL", "Profit before tax", {
        "FY2025": 78521, "FY2024": 72461, "FY2023": 80407, "FY2022": 64521, "FY2021": 27346,
    }),
    ("DATA", "Tax expense", {
        "FY2025": -18405, "FY2024": -19407, "FY2023": -13134, "FY2022": -10488, "FY2021": -6784,
    }),
    ("TOTAL", "Profit after tax for the year", {
        "FY2025": 60116, "FY2024": 53054, "FY2023": 67273, "FY2022": 54033, "FY2021": 20562,
    }),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Cash flow hedges - effective portion of changes in fair value", {
        "FY2025": -184, "FY2024": -724, "FY2023": -3394, "FY2022": 125,
    }),
    ("DATA", "Cash flow hedges - recycled to profit or loss", {
        "FY2025": 676, "FY2024": 1149, "FY2023": 166, "FY2022": 4,
    }),
    ("TOTAL", "Total comprehensive income for the year, net of tax", {
        "FY2025": 60608, "FY2024": 53479, "FY2023": 64045, "FY2022": 54162, "FY2021": 20562,
    }),
]

bw.add_income_statement_sheet(
    title="Hampshire Trust Bank Plc — Bank Statement of Comprehensive Income",
    subtitle="Bank (parent-entity) column; FY2021 predates Group consolidation and cash flow hedge accounting - see source note",
    rows=pl_rows,
    sources_text=PL_SOURCES,
    first_col_width=88,
    source_height=190,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity (Bank / entity-level column)
# ---------------------------------------------------------------
EQ_SOURCES = (
    "Sources - Hampshire Trust Bank Plc's own Bank Statement of Changes in Equity, each year's own "
    "originally-published report (page as cited on the Balance Sheet/P&L sheets' source notes for that "
    "year - the equity statement sits on the immediately adjacent page in every filing):\n"
    f"FY2025: {AR2025_URL} (p.62)\nFY2024: {AR2024_URL} (p.72)\nFY2023: {AR2023_URL} (p.60ish, Bank statement)\n"
    f"FY2022: {AR2022_URL} (p.59)\nFY2021: {AR2021_URL} (p.52, single Company statement)\n"
    + STATEMENTS_ENTITY_NOTE +
    "\nBuilt using the per-year reconciliation ladder: every year's closing balance ties exactly to both "
    "the next year's own opening balance and that year's own Balance Sheet Total equity - zero plug rows "
    "needed anywhere in this roll-forward."
)

EQ_HEADERS = [
    "Share capital", "Share premium", "Cash flow hedge reserve", "Retained earnings",
    "Attributable to ordinary shareholders", "Other equity reserves (NCI)", "Total equity",
]

eq_rows = [
    ("DATA", "Balance at 1 January 2021", (126288, 196, None, 27574, 154058, None, 154058)),
    ("DATA", "Profit for the year", (None, None, None, 20562, 20562, None, 20562)),
    ("DATA", "Equity settled share-based payment", (None, None, None, 676, 676, None, 676)),
    ("DATA", "Issue of share capital", (13540, None, None, None, 13540, None, 13540)),
    ("TOTAL", "Balance at 31 December 2021", (139828, 196, None, 48812, 188836, None, 188836)),

    ("DATA", "Balance at 1 January 2022", (139828, 196, None, 48812, 188836, None, 188836)),
    ("DATA", "Profit for the year", (None, None, None, 54033, 54033, None, 54033)),
    ("DATA", "Cash flow hedges - effective portion of changes in fair value", (None, None, 125, None, 125, None, 125)),
    ("DATA", "Cash-flow hedges - recycled to profit or loss", (None, None, 4, None, 4, None, 4)),
    ("DATA", "Equity settled share-based payment", (None, None, None, 240, 240, None, 240)),
    ("DATA", "Issue of other equity instruments", (None, None, None, None, None, 17030, 17030)),
    ("DATA", "Coupon paid on other equity instruments", (None, None, None, -1404, -1404, None, -1404)),
    ("TOTAL", "Balance at 31 December 2022", (139828, 196, 129, 101681, 241834, 17030, 258864)),

    ("DATA", "Balance at 1 January 2023", (139828, 196, 129, 101681, 241834, 17030, 258864)),
    ("DATA", "Profit for the year", (None, None, None, 67273, 67273, None, 67273)),
    ("DATA", "Cash flow hedges - effective portion of changes in fair value", (None, None, -3394, None, -3394, None, -3394)),
    ("DATA", "Cash-flow hedges - recycled to profit or loss", (None, None, 166, None, 166, None, 166)),
    ("DATA", "Equity settled share-based payment", (None, None, None, 1399, 1399, None, 1399)),
    ("DATA", "Coupon paid on other equity instruments", (None, None, None, -1507, -1507, None, -1507)),
    ("TOTAL", "Balance at 31 December 2023", (139828, 196, -3099, 168846, 305771, 17030, 322801)),

    ("DATA", "Balance at 1 January 2024", (139828, 196, -3099, 168846, 305771, 17030, 322801)),
    ("DATA", "Profit for the year", (None, None, None, 53054, 53054, None, 53054)),
    ("DATA", "Cash flow hedges - effective portion of changes in fair value", (None, None, -724, None, -724, None, -724)),
    ("DATA", "Cash-flow hedges - recycled to profit or loss", (None, None, 1149, None, 1149, None, 1149)),
    ("DATA", "Equity settled share-based payment", (None, None, None, -204, -204, None, -204)),
    ("DATA", "Coupon paid on other equity instruments", (None, None, None, -1517, -1517, None, -1517)),
    ("TOTAL", "Balance at 31 December 2024", (139828, 196, -2674, 220179, 357529, 17030, 374559)),

    ("DATA", "Balance at 1 January 2025", (139828, 196, -2674, 220179, 357529, 17030, 374559)),
    ("DATA", "Profit for the year", (None, None, None, 60116, 60116, None, 60116)),
    ("DATA", "Cash flow hedges - effective portion of changes in fair value", (None, None, -184, None, -184, None, -184)),
    ("DATA", "Cash-flow hedges - recycled to profit or loss", (None, None, 676, None, 676, None, 676)),
    ("DATA", "Equity settled share-based payment", (None, None, None, 718, 718, None, 718)),
    ("DATA", "Coupon paid on other equity instruments", (None, None, None, -1518, -1518, None, -1518)),
    ("TOTAL", "Balance at 31 December 2025", (139828, 196, -2182, 279495, 417337, 17030, 434367)),
]

bw.add_equity_changes_sheet(
    title="Hampshire Trust Bank Plc — Bank Statement of Changes in Equity",
    subtitle="Bank (parent-entity) column, chronological; FY2021 predates Group consolidation - see source note",
    headers=EQ_HEADERS,
    rows=eq_rows,
    sources_text=EQ_SOURCES,
    source_height=210,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (Bank / entity-level column)
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax for the year", {
        "FY2025": 78521, "FY2024": 72461, "FY2023": 80407, "FY2022": 64521, "FY2021": 27346,
    }),
    ("DATA", "Depreciation and amortisation", {
        "FY2025": 6963, "FY2024": 5800, "FY2023": 4936, "FY2022": 4411, "FY2021": 3936,
    }),
    ("DATA", "Loss on disposal of fixed assets", {
        "FY2023": 503,
    }),
    ("DATA", "Impairment loss on investment in subsidiaries", {
        "FY2025": 26500, "FY2024": 11219,
    }),
    ("DATA", "Foreign exchange gains/(losses)", {
        "FY2025": -29, "FY2022": -2, "FY2021": 9,
    }),
    ("DATA", "Gain on securitisation", {
        "FY2024": -10414,
    }),
    ("DATA", "Increase in impairment of loans and advances", {
        "FY2025": 10147, "FY2024": 8939, "FY2023": 7183, "FY2022": 11995, "FY2021": 6362,
    }),
    ("DATA", "Increase/(decrease) in provisions", {
        "FY2025": 1831, "FY2024": 1364, "FY2023": 6036, "FY2022": 3215, "FY2021": -4206,
    }),
    ("DATA", "Equity-settled share-based payment transactions", {
        "FY2025": 718, "FY2024": -204, "FY2023": 1399, "FY2022": 240, "FY2021": 676,
    }),
    ("DATA", "Bond premium/discount amortisation", {
        "FY2025": 157, "FY2024": -1943, "FY2023": -4943, "FY2022": -335, "FY2021": 1275,
    }),
    ("DATA", "Decrease/(increase) in fair value of derivative assets", {
        "FY2025": 30481, "FY2024": 18609, "FY2023": 41007, "FY2022": -76695, "FY2021": -28408,
    }),
    ("DATA", "Increase/(decrease) in fair value of loans and advances designated as hedged items", {
        "FY2025": -32163, "FY2024": -19784, "FY2023": -39698, "FY2022": 73530, "FY2021": 25595,
    }),
    ("DATA", "Decrease/(increase) in fair value of loans and advances held at FVTPL", {
        "FY2025": 188, "FY2024": -53, "FY2023": 1436, "FY2022": -6981, "FY2021": -749,
    }),
    ("DATA", "Repayment of the interest accrued on lease liabilities", {
        "FY2025": 228, "FY2024": 258, "FY2023": 142, "FY2022": 70, "FY2021": -129,
    }),
    ("DATA", "Dividends received", {
        "FY2025": -26500, "FY2024": -11000, "FY2023": -27500, "FY2022": -20000,
    }),
    ("DATA", "Other acquisition costs recognised through equity", {
        "FY2022": -392,
    }),
    ("DATA", "Corporation tax paid", {
        "FY2025": -21655, "FY2024": -18086, "FY2023": -15835, "FY2022": -14257, "FY2021": -3709,
    }),
    ("DATA", "Corporation tax received", {
        "FY2025": 1166,
    }),
    ("DATA", "(Increase) in loans and advances to customers", {
        "FY2025": -1121847, "FY2024": -717726, "FY2023": -675670, "FY2022": -625569, "FY2021": -419379,
    }),
    ("DATA", "(Increase)/decrease in other assets", {
        "FY2025": 61605, "FY2024": 6841, "FY2023": -169564, "FY2022": -94775, "FY2021": -508,
    }),
    ("DATA", "(Decrease)/increase in central bank facilities", {
        "FY2025": -5000, "FY2024": -5000, "FY2023": 5000, "FY2021": 115000,
    }),
    ("DATA", "(Increase)/decrease in collateral held with banks", {
        "FY2025": -30078, "FY2024": -25256, "FY2023": -33646, "FY2022": 73421, "FY2021": 27594,
    }),
    ("DATA", "Increase in customer deposits", {
        "FY2025": 702733, "FY2024": 1324101, "FY2023": 765355, "FY2022": 798748, "FY2021": 512682,
    }),
    ("DATA", "Increase/(decrease) in subordinated and other liabilities", {
        "FY2025": -12373, "FY2024": -20701, "FY2023": 6564, "FY2022": 68205, "FY2021": 3637,
    }),
    ("TOTAL", "Net cash from/(used in) operating activities", {
        "FY2025": -328407, "FY2024": 619425, "FY2023": -46888, "FY2022": 259350, "FY2021": 267024,
    }),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Acquisition of subsidiary, net of cash acquired", {
        "FY2022": -32000,
    }),
    ("DATA", "Dividends received from subsidiary undertakings", {
        "FY2025": 26500, "FY2024": 11000, "FY2023": 27500, "FY2022": 20000,
    }),
    ("DATA", "Purchase of property, plant and equipment", {
        "FY2025": -300, "FY2024": -298, "FY2023": -4742, "FY2022": -543, "FY2021": -231,
    }),
    ("DATA", "Disposal of property, plant and equipment", {
        "FY2024": 51,
    }),
    ("DATA", "Purchase of intangible assets", {
        "FY2025": -4612, "FY2024": -6814, "FY2023": -5424, "FY2022": -4777, "FY2021": -3355,
    }),
    ("DATA", "Disposal of intangible assets", {
        "FY2025": 477, "FY2024": 67,
    }),
    ("DATA", "Purchase of right of use asset", {
        "FY2023": -3982,
    }),
    ("DATA", "Disposal of right of use asset", {
        "FY2024": -113,
    }),
    ("DATA", "Purchase of investment securities", {
        "FY2025": -500773, "FY2024": -135668, "FY2023": -415054, "FY2022": -424657, "FY2021": -178144,
    }),
    ("DATA", "Settlement/sale of investment securities", {
        "FY2025": 28148, "FY2024": 162520, "FY2023": 439744, "FY2022": 402000,
    }),
    ("TOTAL", "Net cash from/(used in) investing activities", {
        "FY2025": -450560, "FY2024": 30745, "FY2023": 38042, "FY2022": -39977, "FY2021": -181730,
    }),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Repayments of the principal portion of finance lease liabilities", {
        "FY2025": -737, "FY2024": -710, "FY2023": -797, "FY2022": -1318, "FY2021": -1183,
    }),
    ("DATA", "Inception of finance lease liability", {
        "FY2023": 3982,
    }),
    ("DATA", "Coupon paid to other equity instrument holders", {
        "FY2025": -1518, "FY2024": -1517, "FY2023": -1507, "FY2022": -1404,
    }),
    ("DATA", "Proceeds from the issuance of subordinated debt", {
        "FY2025": 55000, "FY2023": 25000,
    }),
    ("DATA", "Repayment of subordinated debt", {
        "FY2025": -30000,
    }),
    ("DATA", "Proceeds from securitisation", {
        "FY2024": 310558,
    }),
    ("DATA", "Proceeds from the issue of share capital", {
        "FY2021": 13540,
    }),
    ("TOTAL", "Net cash from/(used in) financing activities", {
        "FY2025": 22745, "FY2024": 308331, "FY2023": 26678, "FY2022": -2722, "FY2021": 12357,
    }),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {
        "FY2025": -756222, "FY2024": 958501, "FY2023": 17832, "FY2022": 216651, "FY2021": 97651,
    }),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {
        "FY2025": 1435307, "FY2024": 476806, "FY2023": 458974, "FY2022": 242323, "FY2021": 144672,
    }),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {
        "FY2025": 679085, "FY2024": 1435307, "FY2023": 476806, "FY2022": 458974, "FY2021": 242323,
    }),
]

bw.add_cash_flow_sheet(
    title="Hampshire Trust Bank Plc — Bank Statement of Cash Flows",
    subtitle="Bank (parent-entity) column; FY2021 predates Group consolidation and uses the single Company "
              "statement — see source note",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=74,
    source_height=170,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality (Bank / entity-level column)
# ---------------------------------------------------------------
AQ_SOURCES = (
    "Sources - Hampshire Trust Bank Plc's own Note 30 'Allowance for credit impairment losses on "
    "financial assets at amortised cost', Bank Total Gross Carrying Value and Bank Total Loss allowance "
    "tables (summed across the Bank's disclosed product lines: Development Finance, Specialist "
    "Mortgages, Asset and Wholesale Finance):\n"
    f"FY2025: Group Annual Report and Accounts 2025 (Companies House, filed 13 May 2026), p.18-25 - {AR2025_URL}\n"
    f"FY2024: same document's FY2024 comparative columns, p.18-25 - {AR2025_URL}\n"
    f"FY2023: Annual Report and Accounts for the year ended 31 December 2024 (Companies House, filed 13 May 2025), FY2023 comparative columns, p.126-136 - {AR2024_URL}\n"
    f"FY2022: same document's FY2022 comparative columns (from the FY2023 GCV/loss allowance tables), p.126-136 - {AR2024_URL}\n"
    f"FY2021: Annual Report and Accounts for the year ended 31 December 2021 (Companies House, filed 14 Jun 2022), single Company basis (pre-Group; only Development Finance + Specialist Mortgages + Asset and Wholesale Finance product lines existed), p.93-97 - {AR2021_URL}\n"
    "Note's own product-level tables are labelled 'Bank' for Development Finance and Specialist "
    "Mortgages in every year checked (identical to the 'Group' tables for those two products - both "
    "are 100% Bank-originated) and separately labelled 'Bank' vs 'Group' for Asset and Wholesale "
    "Finance/Commercial and Retail Finance once the Group had subsidiary-originated lending (from "
    "FY2022) - the Bank Total used here sums only the Bank-basis product lines, consistent with the "
    "Bank basis used throughout this workbook. Commercial and Retail Finance has no Bank-basis line "
    "at all in any year (subsidiary-only origination) - correctly excluded from the Bank Total. FY2024's "
    "Bank Total loss allowance is disclosed as £21,715k in AR2024's own FY2024 closing balance but as "
    "£21,787k in AR2025's FY2024 opening comparative (a £72k gap, both companies' own filings, not "
    "reconciled here - reproduced as each document discloses it). Net carrying value (Gross carrying "
    "value less Loss allowance) does not tie exactly to the Balance Sheet's 'Loans and advances to "
    "customers - at amortised cost' line (e.g. FY2025: £4,528,886k here vs £4,540,376k on the Balance "
    "Sheet) - Note 30's 'financial assets at amortised cost' scope is evidently broader than customer "
    "loans alone (likely also captures loans to banks and/or investment securities held at amortised "
    "cost), not confirmed further from the disclosure alone - not force-reconciled."
)

aq_rows = [
    ("SECTION", "Gross carrying value by IFRS 9 stage (Bank basis)", {}),
    ("DATA", "Stage 1 (12-month ECL)", {
        "FY2025": 3911362, "FY2024": 2958747, "FY2023": 2512679, "FY2022": 1896973, "FY2021": 1565803,
    }),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {
        "FY2025": 471501, "FY2024": 388068, "FY2023": 443933, "FY2022": 407977, "FY2021": 127790,
    }),
    ("DATA", "Stage 3 (credit-impaired)", {
        "FY2025": 167492, "FY2024": 91739, "FY2023": 70199, "FY2022": 53821, "FY2021": 38893,
    }),
    ("TOTAL", "Total gross carrying value", {
        "FY2025": 4550355, "FY2024": 3438552, "FY2023": 3026811, "FY2022": 2358771, "FY2021": 1732486,
    }),
    ("SECTION", "Loss allowance (ECL) by IFRS 9 stage (Bank basis)", {}),
    ("DATA", "Stage 1", {
        "FY2025": 4573, "FY2024": 4436, "FY2023": 5307, "FY2022": 3099, "FY2021": 1431,
    }),
    ("DATA", "Stage 2", {
        "FY2025": 3429, "FY2024": 3998, "FY2023": 6038, "FY2022": 4752, "FY2021": 1475,
    }),
    ("DATA", "Stage 3", {
        "FY2025": 13467, "FY2024": 13281, "FY2023": 9078, "FY2022": 6535, "FY2021": 8265,
    }),
    ("TOTAL", "Total loss allowance", {
        "FY2025": 21469, "FY2024": 21715, "FY2023": 20423, "FY2022": 14386, "FY2021": 11171,
    }),
    ("TOTAL", "Net carrying value (Gross carrying value less Loss allowance)", {
        "FY2025": 4528886, "FY2024": 3416837, "FY2023": 3006388, "FY2022": 2344385, "FY2021": 1721315,
    }),
    ("SECTION", "Derived ratios", {}),
    ("DATA", "Stage 3 (NPL) ratio (Stage 3 / Total gross carrying value)", {
        "FY2025": "3.68%", "FY2024": "2.67%", "FY2023": "2.32%", "FY2022": "2.28%", "FY2021": "2.25%",
    }),
    ("DATA", "ECL coverage ratio (Total loss allowance / Total gross carrying value)", {
        "FY2025": "0.47%", "FY2024": "0.63%", "FY2023": "0.67%", "FY2022": "0.61%", "FY2021": "0.64%",
    }),
    ("DATA", "Stage 3 coverage ratio (Stage 3 loss allowance / Stage 3 gross carrying value)", {
        "FY2025": "8.04%", "FY2024": "14.48%", "FY2023": "12.93%", "FY2022": "12.14%", "FY2021": "21.25%",
    }),
]

bw.add_asset_quality_sheet(
    title="Hampshire Trust Bank Plc — Asset Quality",
    subtitle="Bank basis, Note 30's financial-assets-at-amortised-cost scope - see source note for the resulting Balance Sheet gap",
    rows=aq_rows,
    sources_text=AQ_SOURCES,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=130)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {
        "FY2025": 397694, "FY2024": 300589, "FY2023": 243719, "FY2022": 180193, "FY2021": 174913,
    })],
    p3_sources(),
)

metric(
    "CET1 Ratio", "%",
    [("Common Equity Tier 1 (CET1) ratio", {
        "FY2025": "13.5%", "FY2024": "13.6%", "FY2023": "13.3%", "FY2022": "13.8%", "FY2021": "18.9%",
    })],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {
        "FY2025": 414725, "FY2024": 317619, "FY2023": 260749, "FY2022": 197223, "FY2021": 174913,
    })],
    p3_sources(),
    note="No Additional Tier 1 instruments are disclosed for FY2021 — Tier 1 capital equals CET1 capital that year.",
)

metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 ratio", {
        "FY2025": "14.1%", "FY2024": "14.4%", "FY2023": "14.2%", "FY2022": "15.1%", "FY2021": "18.9%",
    })],
    p3_sources(),
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {
        "FY2025": 494725, "FY2024": 362750, "FY2023": 311890, "FY2022": 227223, "FY2021": 204913,
    })],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "%",
    [("Total capital ratio", {
        "FY2025": "16.8%", "FY2024": "16.4%", "FY2023": "17.0%", "FY2022": "17.4%", "FY2021": "22.2%",
    })],
    p3_sources(),
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted exposure amount", {
        "FY2025": 2949233, "FY2024": 2207947, "FY2023": 1830864, "FY2022": 1310125, "FY2021": 922921,
    })],
    p3_sources(),
)

# ---------------------------------------------------------------
# Sheet: RWA Breakdown (placed right after Total RWAs, Bank basis)
# ---------------------------------------------------------------
RWA_BREAKDOWN_SOURCES = (
    "Sources - Hampshire Trust Bank Plc Pillar 3 Disclosures, 'Minimum capital requirement' RWEA table "
    "(UK OV1-style breakdown by risk category), Bank column:\n"
    f"FY2025: Pillar 3 Disclosures | 31 December 2025, p.12 - {P3_2025_URL}\n"
    f"FY2024: same table's Bank 2024 comparative column, p.12 - {P3_2025_URL}\n"
    f"FY2023: Pillar 3 Disclosures | 31 December 2023, p.12, Bank 2023 column - {P3_2023_URL}\n"
    f"FY2022: same table's Bank 2022 comparative column, p.12 - {P3_2023_URL}\n"
    f"FY2021: Pillar 3 Disclosures | 31 December 2021, p.17, Bank's 'Capital resources requirement - "
    f"Pillar 1' table (only Credit risk and Operational risk capital requirements disclosed that year, "
    f"no Counterparty credit risk/Securitisation breakout) - {P3_2021_URL}\n"
    "FY2021's Credit risk and Operational risk RWA figures are derived from that year's disclosed "
    "capital requirements (requirement / 8%), since no direct RWEA table was published that year - "
    "the derived Total (£921,488k) sits ~£1,433k (0.16%) below the disclosed Total RWAs sheet figure "
    "(£922,921k), likely reflecting a small Counterparty credit risk or other category not captured in "
    "the simplified 2-line disclosure - not force-reconciled. Securitisation exposures are a new "
    "category from FY2025 (HTB's first securitisation) - genuinely nil (not merely undisclosed) in "
    "FY2024-FY2022, confirmed since the Total ties exactly without a Securitisation line those years."
)

rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding CCR)", {
        "FY2025": 2627722, "FY2024": 1952854, "FY2023": 1623626, "FY2022": 1151820, "FY2021": 816163,
    }),
    ("DATA", "Counterparty credit risk (CCR)", {
        "FY2025": 1435, "FY2024": 8733, "FY2023": 9410, "FY2022": 13524,
    }),
    ("DATA", "Securitisation exposures", {
        "FY2025": 35085, "FY2024": 0, "FY2023": 0, "FY2022": 0,
    }),
    ("DATA", "Operational risk", {
        "FY2025": 284991, "FY2024": 246360, "FY2023": 197828, "FY2022": 144781, "FY2021": 105325,
    }),
    ("TOTAL", "Total RWAs", {
        "FY2025": 2949233, "FY2024": 2207947, "FY2023": 1830864, "FY2022": 1310125, "FY2021": 921488,
    }),
]

bw.add_rwa_breakdown_sheet(
    title="Hampshire Trust Bank Plc — RWA Breakdown",
    subtitle="Bank basis; FY2021 derived from the disclosed capital requirement (÷8%) - see source note",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    source_height=230,
    unit_suffix=" (£'000)",
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio", {
        "FY2025": "7.5%", "FY2024": "8.1%", "FY2023": "7.5%", "FY2022": "9.2%", "FY2021": "8.0%",
    })],
    p3_sources(),
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio", {
        "FY2025": "346.9%", "FY2024": "391.1%", "FY2023": "388.6%", "FY2022": "386.9%", "FY2021": "314.8%",
    })],
    p3_sources(),
    note="Disclosed only at consolidated Group level from FY2022 onward ('Liquidity is managed on a "
         "consolidated basis hence only Group metrics are reported') — no separate Bank-solo LCR exists to "
         "report for those years. FY2021 predates the Group/Bank split; its single reported value is used.",
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio", {
        "FY2025": "158.9%", "FY2024": "163.3%", "FY2023": "147.7%", "FY2022": "152.5%", "FY2021": "120.5%",
    })],
    p3_sources(),
    note="Disclosed only at consolidated Group level from FY2022 onward, same basis as LCR above. FY2021 "
         "predates the Group/Bank split; its single reported value is used.",
)

bw.add_not_disclosed_metric_sheets(["MREL Ratio"], p3_sources())

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {
            "FY2025": 6126399, "FY2024": 5387529, "FY2023": 4063807, "FY2022": 3200482, "FY2021": 2190531,
        }),
        ("Loans and advances to customers - at amortised cost", {
            "FY2025": 4540376, "FY2024": 3391908, "FY2023": 2967326, "FY2022": 2243123, "FY2021": 1704683,
        }),
        ("Customer deposits", {
            "FY2025": 5232516, "FY2024": 4526003, "FY2023": 3205681, "FY2022": 2420694, "FY2021": 1633046,
        }),
        ("Total equity", {
            "FY2025": 434367, "FY2024": 374559, "FY2023": 322801, "FY2022": 258864, "FY2021": 188836,
        }),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net interest income", {
            "FY2025": 167619, "FY2024": 145342, "FY2023": 131062, "FY2022": 98584, "FY2021": 69157,
        }),
        ("Administrative expenses", {
            "FY2025": -83039, "FY2024": -75545, "FY2023": -69237, "FY2022": -56984, "FY2021": -46313,
        }),
        ("Profit after tax for the year", {
            "FY2025": 60116, "FY2024": 53054, "FY2023": 67273, "FY2022": 54033, "FY2021": 20562,
        }),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {
            "FY2025": 374559, "FY2024": 322801, "FY2023": 258864, "FY2022": 188836, "FY2021": 154058,
        }),
        ("Total comprehensive income for the year", {
            "FY2025": 60608, "FY2024": 53479, "FY2023": 64045, "FY2022": 54162, "FY2021": 20562,
        }),
        ("Closing equity", {
            "FY2025": 434367, "FY2024": 374559, "FY2023": 322801, "FY2022": 258864, "FY2021": 188836,
        }),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {
            "FY2025": -328407, "FY2024": 619425, "FY2023": -46888, "FY2022": 259350, "FY2021": 267024,
        }),
        ("Net cash from/(used in) investing activities", {
            "FY2025": -450560, "FY2024": 30745, "FY2023": 38042, "FY2022": -39977, "FY2021": -181730,
        }),
        ("Net cash from/(used in) financing activities", {
            "FY2025": 22745, "FY2024": 308331, "FY2023": 26678, "FY2022": -2722, "FY2021": 12357,
        }),
        ("Cash and cash equivalents at end of year", {
            "FY2025": 679085, "FY2024": 1435307, "FY2023": 476806, "FY2022": 458974, "FY2021": 242323,
        }),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {
            "FY2025": "13.5%", "FY2024": "13.6%", "FY2023": "13.3%", "FY2022": "13.8%", "FY2021": "18.9%",
        }),
        ("Tier 1 Ratio", {
            "FY2025": "14.1%", "FY2024": "14.4%", "FY2023": "14.2%", "FY2022": "15.1%", "FY2021": "18.9%",
        }),
        ("Total Capital Ratio", {
            "FY2025": "16.8%", "FY2024": "16.4%", "FY2023": "17.0%", "FY2022": "17.4%", "FY2021": "22.2%",
        }),
        ("Leverage Ratio", {
            "FY2025": "7.5%", "FY2024": "8.1%", "FY2023": "7.5%", "FY2022": "9.2%", "FY2021": "8.0%",
        }),
        ("LCR", {
            "FY2025": "346.9%", "FY2024": "391.1%", "FY2023": "388.6%", "FY2022": "386.9%", "FY2021": "314.8%",
        }),
        ("NSFR", {
            "FY2025": "158.9%", "FY2024": "163.3%", "FY2023": "147.7%", "FY2022": "152.5%", "FY2021": "120.5%",
        }),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. All Cash Flow figures are the Bank (entity-level) "
         "column; LCR/NSFR are Group-level from FY2022 onward (see the LCR/NSFR sheets' notes).",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/HAMPSHIRE TRUST BANK FINANCIALS.xlsx")
