import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018"]  # most recent first

AR2025_URL = "https://www.handelsbanken.co.uk/tron/gbpu/info/contents/v1/document/52-278301"
AR2024_URL = "https://www.handelsbanken.co.uk/tron/gbpu/info/contents/v1/document/52-265184"
AR2023_URL = "https://www.handelsbanken.co.uk/tron/gbpu/info/contents/v1/document/52-223741"
AR2022_URL = "https://www.handelsbanken.co.uk/tron/gbpu/info/contents/v1/document/52-175531"
AR2021_URL = "https://www.handelsbanken.co.uk/tron/gbpu/info/contents/v1/document/52-141596"

P3_2025_URL = "https://www.handelsbanken.co.uk/tron/gbpu/info/contents/v1/document/52-278302"
P3_2023_URL = "https://www.handelsbanken.co.uk/tron/gbpu/info/contents/v1/document/52-223742"
P3_2022_URL = "https://www.handelsbanken.co.uk/tron/gbpu/info/contents/v1/document/52-175532"

# FY2018-FY2020 pre-date what is hosted on handelsbanken.co.uk's investor relations pages (the earliest AR
# published there is FY2021's); these three years' statutory accounts were instead sourced from Companies House
# (company number 11305395), which is the primary and only surviving public source for them.
AA2020_URL = "https://find-and-update.company-information.service.gov.uk/company/11305395/filing-history/MzI5NzQzMjk0N2FkaXF6a2N4/document?format=pdf&download=0"
AA2019_URL = "https://find-and-update.company-information.service.gov.uk/company/11305395/filing-history/MzI2NzEzNzY5N2FkaXF6a2N4/document?format=pdf&download=0"
AA2018_URL = "https://find-and-update.company-information.service.gov.uk/company/11305395/filing-history/MzIzMTA0NzkzMWFkaXF6a2N4/document?format=pdf&download=0"

HISTORICAL_BASIS_NOTE = (
    "HISTORICAL BASIS NOTE (FY2018-FY2020): these three years pre-date Handelsbanken plc's UK Group consolidated "
    "financial statements entirely (not just the Cash Flow Statement's Group/Bank split noted above) - no UK Group "
    "consolidated accounts were prepared until FY2021. FY2018-FY2020 figures below are instead Handelsbanken plc's "
    "own standalone ('solo') statutory accounts as filed with Companies House, since the Bank met the Companies "
    "Act's exemption from preparing consolidated financial statements for its 2-3 wholly-owned subsidiaries "
    "(carried at cost via an 'Investments in subsidiaries' balance sheet line, absent from the UK Group "
    "consolidated basis used from FY2021 onward). There is a genuine basis discontinuity at the FY2020/FY2021 "
    "boundary, not a restatement error: solo Total equity at 31 December 2020 was £2,392,453k per Handelsbanken "
    "plc's own FY2020 accounts, but the FY2021 Annual Report's own 'At 1 January 2021' UK Group consolidated "
    "opening balance is £2,387,716k (retained earnings £312,047k) - a £4,737k difference from consolidating the "
    "subsidiaries previously held at cost. FY2018 additionally covers a stub 9-month period (11 April 2018 "
    "incorporation to 31 December 2018); its income statement and cash flow reflect only 1 month of actual "
    "banking activity, following the 1 December 2018 transfer of trade and assets from the UK branch of Svenska "
    "Handelsbanken AB - see the Overview sheet note. The balance sheet, by contrast, is a genuine point-in-time "
    "snapshot as at 31 December 2018."
)

ENTITY_NOTE = (
    "ENTITY NOTE: Handelsbanken plc (company number 11305395, FRN 806852) was incorporated 11 April 2018 as the "
    "UK-incorporated subsidiary that Handelsbanken's (Svenska Handelsbanken AB) UK business restructured into from "
    "a branch. Because of that youth, FY2021 (its third full year) is the earliest year for which the annual report "
    "distinguishes a consolidated 'UK Group' cash flow statement from the standalone parent-only 'Bank' one - the "
    "FY2021 Annual Report itself presents only a single, undifferentiated 'Cash Flow Statement' (i.e. Bank and "
    "Group were not yet reported separately). To keep this sheet on a consistent Group/consolidated basis "
    "throughout, FY2021 cash flow figures below are the Group-restated comparative column as re-presented in the "
    "FY2022 Annual Report (which differs modestly, line by line, from the FY2021 report's own originally-reported "
    "figures - net cash flow totals below are internally consistent with this restated basis)."
)

CASH_FLOW_SOURCES = (
    "Sources - Handelsbanken plc cash flow statement, £'000 (UK Group consolidated FY2021-FY2025; Bank-only/solo "
    "FY2018-FY2020, see HISTORICAL BASIS NOTE below):\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements 2025, p.83 (Consolidated cash flow statement, UK "
    f"Group) - {AR2025_URL}\n"
    f"FY2023: Annual Report 2023, p.87 (Cash flow statement, UK Group) - {AR2023_URL}\n"
    f"FY2022: Annual Report 2022, p.90 (Consolidated cash flow statement, UK Group) - {AR2022_URL}\n"
    f"FY2021: Annual Report 2022, p.90 (2021 comparative column, UK Group, restated) - {AR2022_URL}\n"
    f"FY2020: Report and Financial Statements for the year ended 31 December 2020, p.61 (Cash flow statement) - {AA2020_URL}\n"
    f"FY2019: Report and Financial Statements for the year ended 31 December 2020, p.61 (2019 comparative column, "
    f"restated - see PRESENTATION NOTE) - {AA2020_URL}\n"
    f"FY2018: Report and Financial Statements for the 9 month period ended 31 December 2018, p.30 (Cash flow "
    f"statement) - {AA2018_URL}\n\n"
    + ENTITY_NOTE + "\n\n"
    + HISTORICAL_BASIS_NOTE + "\n\n"
    "PRESENTATION NOTE: line items shift modestly across vintages (e.g. 'Acquisition of right of use asset' moved "
    "from the Investing section in the FY2021 report to an Operating-activities adjustment from FY2022 onward; "
    "FY2020's own report still shows this line within Investing - kept there below as its own separate row, rather "
    "than merged into the shared 'Acquisition of right of use asset' Operating row used from FY2021 onward, so "
    "each year's Operating and Investing subtotals both still tie exactly to their own disclosed figures; an "
    "'Accrued interest' line appears only in the FY2025 report). Blank cells indicate that year's statement did not "
    "show that specific line (pre-IFRS 16 lines are blank for FY2018; the one-off incorporation-year lines "
    "'Investment in subsidiary', 'Cash transferred from branch' and 'Capital contribution from parent' are FY2018 "
    "only). FY2019 figures below are the restated comparative column as re-presented in the FY2020 Annual Report, "
    "not FY2019's own originally-published cash flow statement, for the same reason as the FY2021 restatement "
    "described above: FY2019's own report classified 'Payments made for lease liabilities' (£10,006k) within "
    "Operating activities (giving operating cash inflow of £489,829k and nil net financing cash flow), whereas the "
    "FY2020 Annual Report's 2019 comparative reclassifies that same £10,006k into Financing activities (operating "
    "cash inflow £499,835k, financing cash outflow £10,006k) - both are Handelsbanken plc's own figures, just "
    "presented on two different section bases a year apart; the restated basis is used here to keep this sheet's "
    "row/section structure consistent with FY2020 onward. Operating/investing/financing subtotals and the net cash "
    "movement for the year are internally consistent and reconcile exactly in every year shown; the "
    "opening-plus-movement-plus-FX bridge to the closing cash balance is exact for FY2018-FY2024, and within an "
    "immaterial £13k rounding difference (on a balance of £7.76bn) for FY2025, as published."
)


def p3_sources(source_doc="Risk and Capital Information according to Pillar 3 - 2025", page="8-9", url=P3_2025_URL):
    return (
        "Sources - Handelsbanken plc UK Group consolidated basis (UK KM1 Key metrics template):\n"
        f"{source_doc}, p.{page} - {url}"
    )


bw = BankWorkbook(bank_name="Handelsbanken plc", years=YEARS, header_color="003D6B")

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
BS_SOURCES = (
    "Sources - Handelsbanken plc balance sheet, £'000 (UK Group consolidated FY2021-FY2025; Bank-only/solo "
    "FY2018-FY2020, see HISTORICAL BASIS NOTE below):\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements 2025, p.81 (Consolidated balance sheet, UK Group) - {AR2025_URL}\n"
    f"FY2023 & FY2022: Annual Report 2023, p.85 (Balance sheet, UK Group) - {AR2023_URL}\n"
    f"FY2021: Annual Report 2022, p.89 (2021 comparative column, Consolidated balance sheet, UK Group) - {AR2022_URL}\n"
    f"FY2020 & FY2019: Report and Financial Statements for the year ended 31 December 2020, p.59 (Balance sheet) - {AA2020_URL}\n"
    f"FY2018: Report and Financial Statements for the 9 month period ended 31 December 2018, p.28 (Balance sheet) - {AA2018_URL}\n\n"
    + ENTITY_NOTE + "\n\n"
    + HISTORICAL_BASIS_NOTE + "\n\n"
    "PRESENTATION NOTE: 'Other loans to central banks' is shown as its own balance sheet line FY2018-FY2023 but is "
    "absorbed elsewhere (not separately disclosed) from FY2024 onward - blank where not shown that year. 'Retained "
    "earnings' is shown as a single combined line FY2025/FY2024, but the FY2023 Annual Report's own balance sheet "
    "splits 'Retained earnings' and 'Profit for the year' as two separate equity lines for its FY2023/FY2022 columns "
    "(and the FY2022 Annual Report's FY2021 comparative does the same, as do the Bank's own FY2018-FY2020 accounts) "
    "- these are combined into one 'Retained earnings' figure below for consistency across all years (e.g. FY2023: "
    "£398,276k + £415,740k = £814,016k), which ties to the Statement of Changes in Equity sheet's own 'Retained "
    "earnings' column. 'Investments in subsidiaries' (£44,119k, unchanged FY2018-FY2020) is a Bank-only/solo-basis "
    "line with no FY2021+ equivalent (see HISTORICAL BASIS NOTE) - the Bank's 2-3 subsidiaries are immaterial and "
    "carried at cost rather than consolidated in these years. 'Right-of-use assets' and 'Lease liabilities' are "
    "blank for FY2018 (pre-IFRS 16; adopted 1 January 2019). All Total assets / Total liabilities / Total equity / "
    "Total liabilities and equity rows reconcile exactly in every year shown."
)

bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances with central banks", {"FY2025": 7743225, "FY2024": 9084816, "FY2023": 8878735, "FY2022": 7944713, "FY2021": 8284357, "FY2020": 9024036, "FY2019": 6948123, "FY2018": 6462632}),
    ("DATA", "Other loans to central banks", {"FY2023": 88371, "FY2022": 99900, "FY2021": 102779, "FY2020": 98393, "FY2019": 81671, "FY2018": 74489}),
    ("DATA", "Loans to other credit institutions", {"FY2025": 3476885, "FY2024": 3562720, "FY2023": 5230310, "FY2022": 5523785, "FY2021": 3944381, "FY2020": 3649977, "FY2019": 2944509, "FY2018": 3973416}),
    ("DATA", "Loans to the public", {"FY2025": 18414143, "FY2024": 17826369, "FY2023": 18023996, "FY2022": 19028715, "FY2021": 20177506, "FY2020": 20858150, "FY2019": 21403516, "FY2018": 20604034}),
    ("DATA", "Investments in subsidiaries (Bank-only/solo basis, see note)", {"FY2020": 44119, "FY2019": 44119, "FY2018": 44119}),
    ("DATA", "Intangible assets", {"FY2025": 41802, "FY2024": 50057, "FY2023": 51005, "FY2022": 47844, "FY2021": 49420, "FY2020": 26042, "FY2019": 23396, "FY2018": 18285}),
    ("DATA", "Property and equipment", {"FY2025": 26817, "FY2024": 21635, "FY2023": 19892, "FY2022": 18435, "FY2021": 18917, "FY2020": 22103, "FY2019": 24620, "FY2018": 22364}),
    ("DATA", "Right-of-use assets", {"FY2025": 74181, "FY2024": 50509, "FY2023": 50720, "FY2022": 51454, "FY2021": 58053, "FY2020": 66212, "FY2019": 68286}),
    ("DATA", "Current tax assets", {"FY2025": 3581, "FY2024": 2431, "FY2023": 396, "FY2020": 2944}),
    ("DATA", "Deferred tax assets", {"FY2025": 801, "FY2024": 1071, "FY2023": 2098, "FY2022": 3869, "FY2021": 2150, "FY2020": 1549, "FY2019": 1068, "FY2018": 1320}),
    ("DATA", "Assets held for sale", {"FY2022": 0, "FY2021": 145, "FY2020": 210, "FY2019": 88, "FY2018": 1709}),
    ("DATA", "Prepaid expenses and accrued income", {"FY2025": 18669, "FY2024": 18641, "FY2023": 16385, "FY2022": 14187, "FY2021": 14112, "FY2020": 7876, "FY2019": 6427, "FY2018": 15550}),
    ("DATA", "Other assets", {"FY2025": 4508, "FY2024": 95608, "FY2023": 6033, "FY2022": 31723, "FY2021": 6431, "FY2020": 12314, "FY2019": 15911, "FY2018": 43658}),
    ("TOTAL", "Total assets", {"FY2025": 29804612, "FY2024": 30713857, "FY2023": 32367941, "FY2022": 32764625, "FY2021": 32658251, "FY2020": 33813925, "FY2019": 31561734, "FY2018": 31261576}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Due to credit institutions", {"FY2025": 4015067, "FY2024": 4979153, "FY2023": 6886954, "FY2022": 7239434, "FY2021": 7875770, "FY2020": 9234311, "FY2019": 9724277, "FY2018": 9364695}),
    ("DATA", "Deposits from the public", {"FY2025": 21467902, "FY2024": 20880491, "FY2023": 20359402, "FY2022": 20486618, "FY2021": 19201850, "FY2020": 19090724, "FY2019": 16456660, "FY2018": 14976954}),
    ("DATA", "Issued securities", {"FY2025": 1753210, "FY2024": 2136439, "FY2023": 2134871, "FY2022": 2190225, "FY2021": 2976981, "FY2020": 2980128, "FY2019": 2958620, "FY2018": 4736028}),
    ("DATA", "Current tax liabilities", {"FY2023": 108, "FY2022": 3916, "FY2021": 1514, "FY2019": 32805, "FY2018": 22804}),
    ("DATA", "Deferred tax liabilities", {"FY2025": 1920, "FY2024": 2179, "FY2023": 2730, "FY2022": 3020, "FY2021": 2719}),
    ("DATA", "Provisions", {"FY2025": 14275, "FY2024": 14350, "FY2023": 16731, "FY2022": 22843, "FY2021": 18189, "FY2020": 14638, "FY2019": 5644, "FY2018": 5550}),
    ("DATA", "Lease liabilities", {"FY2025": 78993, "FY2024": 52397, "FY2023": 51290, "FY2022": 52611, "FY2021": 61633, "FY2020": 65013, "FY2019": 70355}),
    ("DATA", "Accrued expenses and deferred income", {"FY2025": 10381, "FY2024": 9686, "FY2023": 11300, "FY2022": 10203, "FY2021": 13436, "FY2020": 18050, "FY2019": 19036, "FY2018": 38226}),
    ("DATA", "Other liabilities", {"FY2025": 20056, "FY2024": 15528, "FY2023": 14870, "FY2022": 16294, "FY2021": 19330, "FY2020": 18608, "FY2019": 21493, "FY2018": 28017}),
    ("TOTAL", "Total liabilities", {"FY2025": 27361804, "FY2024": 28090223, "FY2023": 29478256, "FY2022": 30025164, "FY2021": 30171422, "FY2020": 31421472, "FY2019": 29288890, "FY2018": 29172274}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 5050, "FY2024": 5050, "FY2023": 5050, "FY2022": 5050, "FY2021": 5050, "FY2020": 5050, "FY2019": 5050, "FY2018": 5050}),
    ("DATA", "Share premium", {"FY2025": 2070619, "FY2024": 2070619, "FY2023": 2070619, "FY2022": 2070619, "FY2021": 2070619, "FY2020": 2070619, "FY2019": 2070619, "FY2018": 2070619}),
    ("DATA", "Retained earnings", {"FY2025": 367139, "FY2024": 547965, "FY2023": 814016, "FY2022": 663792, "FY2021": 411160, "FY2020": 316784, "FY2019": 197175, "FY2018": 13633}),
    ("TOTAL", "Total equity", {"FY2025": 2442808, "FY2024": 2623634, "FY2023": 2889685, "FY2022": 2739461, "FY2021": 2486829, "FY2020": 2392453, "FY2019": 2272844, "FY2018": 2089302}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 29804612, "FY2024": 30713857, "FY2023": 32367941, "FY2022": 32764625, "FY2021": 32658251, "FY2020": 33813925, "FY2019": 31561734, "FY2018": 31261576}),
]

bw.add_balance_sheet_sheet(
    title="Handelsbanken plc — Consolidated Balance Sheet",
    subtitle="Handelsbanken plc UK Group (consolidated basis), £'000 unless stated. See source note at bottom.",
    rows=bs_rows,
    sources_text=BS_SOURCES,
    first_col_width=60,
    source_height=200,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
IS_SOURCES = (
    "Sources - Handelsbanken plc statement of profit or loss, £'000 (UK Group consolidated FY2021-FY2025; "
    "Bank-only/solo FY2018-FY2020, see HISTORICAL BASIS NOTE below):\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements 2025, p.80 (Consolidated statement of profit or loss "
    f"and other comprehensive income, UK Group) - {AR2025_URL}\n"
    f"FY2023: Annual Report 2023, p.84 (Consolidated statement of profit and loss and comprehensive income, UK "
    f"Group) - {AR2023_URL}\n"
    f"FY2022 & FY2021: Annual Report 2022, p.88 (each year's own originally-published figures, UK Group) - {AR2022_URL}\n"
    f"FY2020 & FY2019: Report and Financial Statements for the year ended 31 December 2020, p.58 (Income statement) - {AA2020_URL}\n"
    f"FY2018: Report and Financial Statements for the 9 month period ended 31 December 2018, p.27 (Income statement) - {AA2018_URL}\n\n"
    + ENTITY_NOTE + "\n\n"
    + HISTORICAL_BASIS_NOTE + "\n\n"
    "PRESENTATION NOTE: in 2023, breakage fees previously reported under 'Net gains on financial transactions and "
    "other income' began to be presented within 'Interest income' - the FY2023 Annual Report's own restated 2022 "
    "comparative column shows Interest income £923,790k (vs FY2022's own originally-published £912,438k) and Net "
    "gains on financial transactions and other income £12,729k (vs FY2022's own originally-published £24,081k), a "
    "difference of £11,352k (~£11m) in both directions - matching the disclosed reclassification exactly. FY2022 "
    "figures below use FY2022's own originally-published presentation (per project convention), not the later "
    "restated comparative. FY2018's own income statement itemised 'Professional fees' (£2,435k) and 'IT costs' "
    "(£1,634k) separately from 'Other expenses' (£8,315k); these three lines are combined into the single 'Other "
    "operating expenses' cell below (£12,384k) for consistency with later years' presentation - this is exactly "
    "how the FY2019 Annual Report's own 2018 comparative column re-presents the same figures. No other "
    "comprehensive income was recognised in any year shown. Total income / Total expenses / Profit before tax / "
    "Profit for the year / Total comprehensive income rows all reconcile exactly and tie to the Cash Flow "
    "Statement sheet's own 'Profit before tax' row in every year."
)

is_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 1574025, "FY2024": 1866849, "FY2023": 1802094, "FY2022": 912438, "FY2021": 571072, "FY2020": 655358, "FY2019": 774106, "FY2018": 64953}),
    ("DATA", "Interest expense", {"FY2025": -784441, "FY2024": -1005107, "FY2023": -875598, "FY2022": -271326, "FY2021": -128033, "FY2020": -203834, "FY2019": -270473, "FY2018": -22106}),
    ("TOTAL", "Net interest income", {"FY2025": 789584, "FY2024": 861742, "FY2023": 926496, "FY2022": 641112, "FY2021": 443039, "FY2020": 451524, "FY2019": 503633, "FY2018": 42847}),
    ("DATA", "Fee and commission income", {"FY2025": 72570, "FY2024": 71197, "FY2023": 71497, "FY2022": 72357, "FY2021": 71651, "FY2020": 38425, "FY2019": 43302, "FY2018": 4415}),
    ("DATA", "Fee and commission expense", {"FY2025": -2912, "FY2024": -3074, "FY2023": -3624, "FY2022": -3656, "FY2021": -3301, "FY2020": -3250, "FY2019": -3383, "FY2018": -376}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 69658, "FY2024": 68123, "FY2023": 67873, "FY2022": 68701, "FY2021": 68350, "FY2020": 35175, "FY2019": 39919, "FY2018": 4039}),
    ("DATA", "Net gains on financial transactions and other income", {"FY2025": 12327, "FY2024": 12311, "FY2023": 11987, "FY2022": 24081, "FY2021": 21464, "FY2020": 19411, "FY2019": 22729, "FY2018": 2276}),
    ("TOTAL", "Total income", {"FY2025": 871569, "FY2024": 942176, "FY2023": 1006356, "FY2022": 733894, "FY2021": 532853, "FY2020": 506110, "FY2019": 566281, "FY2018": 49162}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Personnel costs", {"FY2025": -298247, "FY2024": -296153, "FY2023": -262399, "FY2022": -240280, "FY2021": -232331, "FY2020": -207178, "FY2019": -177199, "FY2018": -16578}),
    ("DATA", "Depreciation, amortisation and impairment", {"FY2025": -36386, "FY2024": -28159, "FY2023": -25183, "FY2022": -23420, "FY2021": -32815, "FY2020": -21498, "FY2019": -19199, "FY2018": -412}),
    ("DATA", "Other operating expenses", {"FY2025": -122165, "FY2024": -129993, "FY2023": -140157, "FY2022": -122681, "FY2021": -141061, "FY2020": -106203, "FY2019": -119539, "FY2018": -12384}),
    ("TOTAL", "Total expenses", {"FY2025": -456798, "FY2024": -454305, "FY2023": -427739, "FY2022": -386381, "FY2021": -406207, "FY2020": -334879, "FY2019": -315937, "FY2018": -29374}),
    ("DATA", "Profit before credit gains/(losses) and net losses/(gains) from disposal", {"FY2025": 414771, "FY2024": 487871, "FY2023": 578617, "FY2022": 347513, "FY2021": 126646, "FY2020": 171231, "FY2019": 250344, "FY2018": 19788}),
    ("DATA", "Net credit gains/(losses)", {"FY2025": 7162, "FY2024": 10164, "FY2023": -3788, "FY2022": -4415, "FY2021": 7945, "FY2020": -10046, "FY2019": 1255, "FY2018": -1051}),
    ("DATA", "Net (losses)/gains on disposal of property, equipment and intangible assets", {"FY2025": -101, "FY2024": -13, "FY2023": -65, "FY2022": 818, "FY2021": 775, "FY2020": -585, "FY2019": 81}),
    ("TOTAL", "Profit before tax", {"FY2025": 421832, "FY2024": 498022, "FY2023": 574764, "FY2022": 343916, "FY2021": 135366, "FY2020": 160600, "FY2019": 251680, "FY2018": 18737}),
    ("DATA", "Taxes", {"FY2025": -117971, "FY2024": -138732, "FY2023": -159024, "FY2022": -91284, "FY2021": -36253, "FY2020": -40991, "FY2019": -68138, "FY2018": -5104}),
    ("TOTAL", "Profit for the year", {"FY2025": 303861, "FY2024": 359290, "FY2023": 415740, "FY2022": 252632, "FY2021": 99113, "FY2020": 119609, "FY2019": 183542, "FY2018": 13633}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Other comprehensive income, net of tax", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0, "FY2020": 0, "FY2019": 0, "FY2018": 0}),
    ("TOTAL", "Total comprehensive income for the year", {"FY2025": 303861, "FY2024": 359290, "FY2023": 415740, "FY2022": 252632, "FY2021": 99113, "FY2020": 119609, "FY2019": 183542, "FY2018": 13633}),
]

bw.add_income_statement_sheet(
    title="Handelsbanken plc — Consolidated Statement of Profit or Loss and Other Comprehensive Income",
    subtitle="Handelsbanken plc UK Group (consolidated basis), £'000 unless stated. See source note at bottom.",
    rows=is_rows,
    sources_text=IS_SOURCES,
    first_col_width=68,
    source_height=220,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
EQUITY_SOURCES = (
    "Sources - Handelsbanken plc statement of changes in equity, £'000 (UK Group consolidated FY2021-FY2025; "
    "Bank-only/solo FY2018-FY2020, see HISTORICAL BASIS NOTE below):\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements 2025, p.82 (Consolidated statement of changes in "
    f"equity, UK Group) - {AR2025_URL}\n"
    f"FY2023 & FY2022: Annual Report 2023, p.86 (Statement of changes in equity, UK Group) - {AR2023_URL}\n"
    f"FY2021: Annual Report 2022, p.90 (2021 section, Consolidated statement of changes in equity, UK Group) - {AR2022_URL}\n"
    f"FY2020 & FY2019: Report and Financial Statements for the year ended 31 December 2020, p.60 (Statement of "
    f"changes in equity) - {AA2020_URL}\n"
    f"FY2018: Report and Financial Statements for the 9 month period ended 31 December 2018, p.29 (Statement of "
    f"changes in equity) - {AA2018_URL}\n\n"
    + ENTITY_NOTE + "\n\n"
    + HISTORICAL_BASIS_NOTE + "\n\n"
    "PRESENTATION NOTE: no plug rows were needed anywhere in this roll-forward within either the FY2018-FY2020 "
    "(Bank-only) run or the FY2021-FY2025 (UK Group) run considered separately - each year's closing balance ties "
    "exactly to both the next year's own opening balance and that year's own Balance Sheet Total equity, within "
    "each of those two runs. The one break in the chain is exactly at the FY2020/FY2021 boundary itself (see "
    "HISTORICAL BASIS NOTE) - a basis change, not a plug. No share issuances, treasury shares, share-based "
    "payments, or FX/translation reserve movements exist for this entity in any year shown; the only equity "
    "movements are dividends (first paid in FY2023) and total comprehensive income (profit for the year, since no "
    "OCI was recognised in any year)."
)

equity_rows = [
    ("TOTAL", "At 11 April 2018 (incorporation)", (0, 0, 0, 0)),
    ("DATA", "Issuance of shares", (5050, 2070619, None, 2075669)),
    ("DATA", "Total comprehensive income for the period", (None, None, 13633, 13633)),
    ("TOTAL", "At 31 December 2018 / At 1 January 2019", (5050, 2070619, 13633, 2089302)),
    ("DATA", "Total comprehensive income for the year", (None, None, 183542, 183542)),
    ("TOTAL", "At 31 December 2019 / At 1 January 2020", (5050, 2070619, 197175, 2272844)),
    ("DATA", "Total comprehensive income for the year", (None, None, 119609, 119609)),
    ("TOTAL", "At 31 December 2020 (Bank-only/solo basis - see note)", (5050, 2070619, 316784, 2392453)),
    ("TOTAL", "At 1 January 2021 (UK Group consolidated basis - see note)", (5050, 2070619, 312047, 2387716)),
    ("DATA", "Total comprehensive income for the year", (None, None, 99113, 99113)),
    ("TOTAL", "At 31 December 2021 / At 1 January 2022", (5050, 2070619, 411160, 2486829)),
    ("DATA", "Total comprehensive income for the year", (None, None, 252632, 252632)),
    ("TOTAL", "At 31 December 2022 / At 1 January 2023", (5050, 2070619, 663792, 2739461)),
    ("DATA", "Dividend paid", (None, None, -265516, -265516)),
    ("DATA", "Total comprehensive income for the year", (None, None, 415740, 415740)),
    ("TOTAL", "At 31 December 2023 / At 1 January 2024", (5050, 2070619, 814016, 2889685)),
    ("DATA", "Dividend paid", (None, None, -625341, -625341)),
    ("DATA", "Total comprehensive income for the year", (None, None, 359290, 359290)),
    ("TOTAL", "At 31 December 2024 / At 1 January 2025", (5050, 2070619, 547965, 2623634)),
    ("DATA", "Dividend paid", (None, None, -484687, -484687)),
    ("DATA", "Total comprehensive income for the year", (None, None, 303861, 303861)),
    ("TOTAL", "At 31 December 2025", (5050, 2070619, 367139, 2442808)),
]

bw.add_equity_changes_sheet(
    title="Handelsbanken plc — Consolidated Statement of Changes in Equity",
    subtitle="Handelsbanken plc UK Group (consolidated basis), £'000, chronological (oldest to newest). See source note at bottom.",
    headers=["Share capital", "Share premium", "Retained earnings", "Total equity"],
    rows=equity_rows,
    sources_text=EQUITY_SOURCES,
    first_col_width=46,
    source_height=170,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax", {"FY2025": 421832, "FY2024": 498022, "FY2023": 574764, "FY2022": 343916, "FY2021": 135366, "FY2020": 160600, "FY2019": 251680, "FY2018": 18737}),
    ("DATA", "Net credit (gains)/losses", {"FY2025": -7162, "FY2024": -10164, "FY2023": 3788, "FY2022": 4415, "FY2021": -7945, "FY2020": 10046, "FY2019": -1255, "FY2018": 1051}),
    ("DATA", "(Gain)/loss on financial transactions", {"FY2020": 1134, "FY2019": -228, "FY2018": 96}),
    ("DATA", "Net losses/(gains) on disposal of property, equipment and intangible assets", {"FY2025": 101, "FY2024": 13, "FY2023": 65, "FY2022": -818, "FY2021": -775, "FY2020": 585, "FY2019": -81}),
    ("DATA", "Depreciation, amortisation and impairment", {"FY2025": 36386, "FY2024": 28159, "FY2023": 25129, "FY2022": 23420, "FY2021": 32815, "FY2020": 21498, "FY2019": 19199, "FY2018": 412}),
    ("DATA", "Lease liability interest expense", {"FY2025": 3222, "FY2024": 1734, "FY2023": 1535, "FY2022": 1328, "FY2021": 1555, "FY2020": 1625, "FY2019": 1711}),
    ("DATA", "Acquisition of right of use asset", {"FY2025": -40681, "FY2024": -8854, "FY2023": -8866, "FY2022": -7388, "FY2021": -3100}),
    ("DATA", "Provisions", {"FY2025": -75, "FY2024": -2381, "FY2023": -6112, "FY2022": 4654, "FY2021": 3526, "FY2020": 8994, "FY2019": -4296, "FY2018": 4639}),
    ("DATA", "Other loans to central banks", {"FY2024": 88371, "FY2023": 11529, "FY2022": 2879, "FY2021": -4386, "FY2020": -16722, "FY2019": -7182, "FY2018": -5639}),
    ("DATA", "Loans to other credit institutions", {"FY2025": 87866, "FY2024": 1634611, "FY2023": 289812, "FY2022": -1598199, "FY2021": -241068, "FY2020": -700058, "FY2019": 1019067, "FY2018": -600068}),
    ("DATA", "Loans to the public", {"FY2025": -580612, "FY2024": 207791, "FY2023": 1000930, "FY2022": 1144359, "FY2021": 688529, "FY2020": 538820, "FY2019": -808214, "FY2018": 190867}),
    ("DATA", "Due to credit institutions", {"FY2025": -964086, "FY2024": -1907801, "FY2023": -352481, "FY2022": -636336, "FY2021": -1358541, "FY2020": -489966, "FY2019": 359582, "FY2018": -175409}),
    ("DATA", "Deposits from the public", {"FY2025": 587411, "FY2024": 521089, "FY2023": -127216, "FY2022": 1284768, "FY2021": 122809, "FY2020": 2634064, "FY2019": 1479706, "FY2018": -312492}),
    ("DATA", "Issued securities", {"FY2025": -383229, "FY2024": 1568, "FY2023": -55354, "FY2022": -786756, "FY2021": -3147, "FY2020": 21508, "FY2019": -1777408, "FY2018": -207899}),
    ("DATA", "Lease liabilities (change)", {"FY2025": 38681, "FY2024": 9469, "FY2023": 7327, "FY2022": 4549, "FY2021": 2589}),
    ("DATA", "Payments made for variable/short-term/low-value leases", {"FY2020": -4796, "FY2019": -5472}),
    ("DATA", "Income tax paid", {"FY2025": -119110, "FY2024": -140399, "FY2023": -161747, "FY2022": -90301, "FY2021": -32713, "FY2020": -77220, "FY2019": -57884, "FY2018": 84}),
    ("DATA", "Other assets", {"FY2025": 91100, "FY2024": -89575, "FY2023": 25690, "FY2022": -25292, "FY2021": 5058, "FY2020": 3597, "FY2019": 27747, "FY2018": 105525}),
    ("DATA", "Prepaid expenses and accrued income", {"FY2025": -28, "FY2024": -2256, "FY2023": -2198, "FY2022": -75, "FY2021": -1632, "FY2020": -1449, "FY2019": 9123, "FY2018": -4990}),
    ("DATA", "Other liabilities", {"FY2025": 4528, "FY2024": 658, "FY2023": -1424, "FY2022": -3036, "FY2021": -711, "FY2020": 2033, "FY2019": 9114, "FY2018": -109043}),
    ("DATA", "Accrued expenses and deferred income", {"FY2025": 695, "FY2024": -1614, "FY2023": 1097, "FY2022": -3233, "FY2021": -5470, "FY2020": -986, "FY2019": -14800, "FY2018": -1552}),
    ("DATA", "Accrued interest", {"FY2025": 3884, "FY2024": 7868}),
    ("DATA", "Other operating items", {"FY2022": -11971, "FY2021": -369, "FY2020": -210, "FY2019": -274, "FY2018": -798}),
    ("TOTAL", "Cash (outflow)/inflow from operating activities", {"FY2025": -819277, "FY2024": 836309, "FY2023": 1215640, "FY2022": -351346, "FY2021": -670515, "FY2020": 2113097, "FY2019": 499835, "FY2018": -1096479}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Assets held for sale", {"FY2022": 963, "FY2021": 65, "FY2020": -122, "FY2019": 2138}),
    ("DATA", "Acquisitions of property and equipment", {"FY2025": -14385, "FY2024": -7728, "FY2023": -7000, "FY2022": -4714, "FY2021": -3323, "FY2020": -3491, "FY2019": -7814, "FY2018": -270}),
    ("DATA", "Disposal of property and equipment", {"FY2025": 100, "FY2024": 277, "FY2023": 166, "FY2022": 1216, "FY2021": 996, "FY2020": 275, "FY2019": 390}),
    ("DATA", "Acquisitions/development of intangible assets", {"FY2025": -5526, "FY2024": -10663, "FY2023": -11138, "FY2022": -6635, "FY2021": -3463, "FY2020": -6704, "FY2019": -8892, "FY2018": -651}),
    ("DATA", "Acquisition and remeasurement of right-of-use asset (FY2020 only - disclosed within Investing that year, unlike FY2021+)", {"FY2020": -9633}),
    ("DATA", "Investment in subsidiary (incorporation year only)", {"FY2018": -44119}),
    ("DATA", "Cash transferred from branch (incorporation year only)", {"FY2018": 7199101}),
    ("TOTAL", "Cash outflow from investing activities", {"FY2025": -19811, "FY2024": -18114, "FY2023": -17972, "FY2022": -9170, "FY2021": -5725, "FY2020": -19675, "FY2019": -14178, "FY2018": 7154061}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividends paid to company's shareholders", {"FY2025": -484687, "FY2024": -625341, "FY2023": -265516}),
    ("DATA", "Payments made for lease liabilities", {"FY2025": -11901, "FY2024": -11884, "FY2023": -12424, "FY2022": -12141, "FY2021": -13551, "FY2020": -12099, "FY2019": -10006}),
    ("DATA", "Capital contribution from parent (incorporation year only)", {"FY2018": 405050}),
    ("TOTAL", "Cash outflow from financing activities", {"FY2025": -496588, "FY2024": -637225, "FY2023": -277940, "FY2022": -12141, "FY2021": -13551, "FY2020": -12099, "FY2019": -10006, "FY2018": 405050}),
    ("TOTAL", "Cash (outflow)/inflow for the year", {"FY2025": -1335676, "FY2024": 180970, "FY2023": 919728, "FY2022": -372657, "FY2021": -689791, "FY2020": 2081323, "FY2019": 475651, "FY2018": 6462632}),
    ("DATA", "Cash balance at beginning of year", {"FY2025": 9097190, "FY2024": 8916214, "FY2023": 7996622, "FY2022": 8368955, "FY2021": 9058894, "FY2020": 6977760, "FY2019": 6502109, "FY2018": 0}),
    ("DATA", "Net foreign exchange differences", {"FY2024": 6, "FY2023": -136, "FY2022": 324, "FY2021": -148}),
    ("TOTAL", "Cash balance at end of year", {"FY2025": 7761527, "FY2024": 9097190, "FY2023": 8916214, "FY2022": 7996622, "FY2021": 8368955, "FY2020": 9059083, "FY2019": 6977760, "FY2018": 6462632}),
]

bw.add_cash_flow_sheet(
    title="Handelsbanken plc — Consolidated Cash Flow Statement",
    subtitle="Handelsbanken plc UK Group (consolidated basis), £'000 unless stated. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=68,
    source_height=220,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
ASSET_QUALITY_SOURCES = (
    "Sources - Handelsbanken plc, Note 9 Credit losses (Note 10 from FY2022 onward), 'Balance sheet and "
    "off-balance sheet items that are subject to impairment testing' table (Loans to the public only), £'000 "
    "(UK Group consolidated FY2021-FY2025; Bank-only/solo FY2018-FY2020, see HISTORICAL BASIS NOTE below):\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements 2025, p.110 - {AR2025_URL}\n"
    f"FY2023 & FY2022: Annual Report 2023, p.110-111 - {AR2023_URL}\n"
    f"FY2021: Annual Report 2022, p.112-113 (2021 comparative) - {AR2022_URL}\n"
    f"FY2020 & FY2019: Report and Financial Statements for the year ended 31 December 2020, p.83, Note 9 (2020 "
    f"primary column and 2019 comparative) - {AA2020_URL}\n"
    f"FY2018: Report and Financial Statements for the 9 month period ended 31 December 2018, p.45, Note 9 - {AA2018_URL}\n\n"
    + ENTITY_NOTE + "\n\n"
    + HISTORICAL_BASIS_NOTE + "\n\n"
    "PRESENTATION NOTE: 'Total gross exposure' minus 'Total provisions' ties exactly to the Balance Sheet sheet's "
    "own 'Loans to the public' figure in every year shown (e.g. FY2025: £18,425,775k gross - £11,632k provisions = "
    "£18,414,143k, matching the Balance Sheet exactly; FY2018: £20,638,193k gross - £34,159k provisions = "
    "£20,604,034k). Credit loss reserve ratios and the Stage 3 proportion are each bank-disclosed figures (the "
    "note's own 'Key figures, credit losses' table), not derived by us; FY2018's ratios are the only ones labelled "
    "'Credit loss ratio' rather than 'Credit gain/(loss) ratio' since the Bank had a net credit loss (not a net "
    "credit gain) that year."
)

asset_quality_rows = [
    ("SECTION", "Loans to the public — IFRS 9 stage analysis", {}),
    ("DATA", "Stage 1 gross exposure", {"FY2025": 17640737, "FY2024": 16705882, "FY2023": 16176948, "FY2022": 17688338, "FY2021": 19059761, "FY2020": 19195537, "FY2019": 20269709, "FY2018": 19516661}),
    ("DATA", "Stage 2 gross exposure", {"FY2025": 626364, "FY2024": 926032, "FY2023": 1708802, "FY2022": 1270780, "FY2021": 1037782, "FY2020": 1616230, "FY2019": 1076111, "FY2018": 1029080}),
    ("DATA", "Stage 3 gross exposure", {"FY2025": 158674, "FY2024": 212397, "FY2023": 167023, "FY2022": 94450, "FY2021": 102175, "FY2020": 81300, "FY2019": 84882, "FY2018": 92452}),
    ("TOTAL", "Total gross exposure", {"FY2025": 18425775, "FY2024": 17844311, "FY2023": 18052773, "FY2022": 19053568, "FY2021": 20199718, "FY2020": 20893067, "FY2019": 21430702, "FY2018": 20638193}),
    ("DATA", "Stage 1 provision", {"FY2025": -5130, "FY2024": -6445, "FY2023": -10391, "FY2022": -9445, "FY2021": -4737, "FY2020": -5271, "FY2019": -6402, "FY2018": -4222}),
    ("DATA", "Stage 2 provision", {"FY2025": -3303, "FY2024": -6603, "FY2023": -15234, "FY2022": -11432, "FY2021": -9534, "FY2020": -16373, "FY2019": -6746, "FY2018": -9980}),
    ("DATA", "Stage 3 provision", {"FY2025": -3199, "FY2024": -4894, "FY2023": -3152, "FY2022": -3976, "FY2021": -7941, "FY2020": -13273, "FY2019": -14038, "FY2018": -19957}),
    ("TOTAL", "Total provisions", {"FY2025": -11632, "FY2024": -17942, "FY2023": -28777, "FY2022": -24853, "FY2021": -22212, "FY2020": -34917, "FY2019": -27186, "FY2018": -34159}),
    ("TOTAL", "Net loans to the public (ties to Balance Sheet)", {"FY2025": 18414143, "FY2024": 17826369, "FY2023": 18023996, "FY2022": 19028715, "FY2021": 20177506, "FY2020": 20858150, "FY2019": 21403516, "FY2018": 20604034}),
    ("SECTION", "Key ratios (as disclosed)", {}),
    ("DATA", "Credit loss reserve ratio, Stage 1 (%)", {"FY2025": "0.03%", "FY2024": "0.04%", "FY2023": "0.06%", "FY2022": "0.05%", "FY2021": "0.02%", "FY2020": "0.03%", "FY2019": "0.03%", "FY2018": "0.02%"}),
    ("DATA", "Credit loss reserve ratio, Stage 2 (%)", {"FY2025": "0.53%", "FY2024": "0.71%", "FY2023": "0.89%", "FY2022": "0.90%", "FY2021": "0.92%", "FY2020": "1.01%", "FY2019": "0.63%", "FY2018": "0.97%"}),
    ("DATA", "Credit loss reserve ratio, Stage 3 (%)", {"FY2025": "2.02%", "FY2024": "2.30%", "FY2023": "1.89%", "FY2022": "4.21%", "FY2021": "7.77%", "FY2020": "16.33%", "FY2019": "16.54%", "FY2018": "21.59%"}),
    ("DATA", "Total credit loss reserve ratio (%)", {"FY2025": "0.06%", "FY2024": "0.10%", "FY2023": "0.16%", "FY2022": "0.13%", "FY2021": "0.11%", "FY2020": "0.17%", "FY2019": "0.13%", "FY2018": "0.17%"}),
    ("DATA", "Proportion of loans in Stage 3 (%)", {"FY2025": "0.84%", "FY2024": "1.16%", "FY2023": "0.91%", "FY2022": "0.47%", "FY2021": "0.47%", "FY2020": "0.33%", "FY2019": "0.33%", "FY2018": "0.35%"}),
    ("DATA", "Credit loss/(gain) ratio, % of loans to the public (annualised)", {"FY2020": "0.04%", "FY2019": "-0.01%", "FY2018": "0.06%"}),
]

bw.add_asset_quality_sheet(
    title="Handelsbanken plc — Asset Quality (Loans to the Public)",
    subtitle="Handelsbanken plc UK Group (consolidated basis), £'000 unless stated. See source note at bottom.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=58,
    source_height=170,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"UK Group consolidated basis, {unit}" if unit else "UK Group consolidated basis",
                         rows_data, sources_text, note=note, first_col_width=44, source_height=100)


FY2021_BASIS_NOTE = (
    "No Pillar 3 / UK KM1 report was published for FY2021 (the earliest found on Handelsbanken plc's own site is "
    "2022). FY2021 figures instead come from the 'Capital adequacy ratios'/'Capital resources' sections of the "
    f"FY2021 Annual Report ({AR2021_URL}), which pre-date the Group/Bank split noted on the Cash Flow Statement "
    "sheet - treat FY2021 as the entity's own (Bank=Group) basis at that time, not a formal KM1 disclosure."
)

HISTORICAL_P3_NOTE = (
    "FY2018-FY2020 similarly pre-date any Pillar 3/UK KM1 report, and are additionally on the Bank-only/solo basis "
    "described in the Balance Sheet sheet's HISTORICAL BASIS NOTE (not the UK Group consolidated basis used from "
    "FY2021 onward). These three years' figures instead come from the 'Risk and Capital Management' section's own "
    "'Capital resources'/'Capital requirements'/'Capital adequacy ratios'/'Leverage ratio'/'Liquidity coverage "
    f"ratio' tables of each year's own Report and Financial Statements: FY2018 ({AA2018_URL}); FY2019 and FY2020 "
    f"(both from the FY2020 report, which shows FY2019 as its own clean comparative column) ({AA2020_URL})."
)

metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 2155, "FY2024": 2089, "FY2023": 2214, "FY2022": 2426, "FY2021": 2464, "FY2020": 2366, "FY2019": 2250, "FY2018": 2071})],
    p3_sources(),
    note=FY2021_BASIS_NOTE + " " + HISTORICAL_P3_NOTE,
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "17.5%", "FY2024": "18.0%", "FY2023": "20.0%", "FY2022": "21.3%", "FY2021": "20.2%", "FY2020": "17.6%", "FY2019": "14.8%", "FY2018": "15.8%"})],
    p3_sources(),
    note=FY2021_BASIS_NOTE + " " + HISTORICAL_P3_NOTE + " FY2025/FY2023 ratios are shown after deduction of that "
         "year's recommended dividend (the Board's stated practice - e.g. the FY2025 dividend recommendation "
         "reduced the CET1 ratio from 19.5% to the 17.5% shown here).",
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 2155, "FY2024": 2089, "FY2023": 2214, "FY2022": 2426, "FY2021": 2464, "FY2020": 2366, "FY2019": 2250, "FY2018": 2071})],
    p3_sources(),
    note=FY2021_BASIS_NOTE + " " + HISTORICAL_P3_NOTE + " Equal to CET1 capital in every year shown - the Bank has "
         "not issued any Additional Tier 1 (AT1) capital.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "17.5%", "FY2024": "18.0%", "FY2023": "20.0%", "FY2022": "21.3%", "FY2021": "20.2%", "FY2020": "17.6%", "FY2019": "14.8%", "FY2018": "15.8%"})],
    p3_sources(),
    note=FY2021_BASIS_NOTE + " " + HISTORICAL_P3_NOTE,
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 2456, "FY2024": 2389, "FY2023": 2614, "FY2022": 2826, "FY2021": 2864, "FY2020": 2766, "FY2019": 2650, "FY2018": 2071})],
    p3_sources(),
    note=FY2021_BASIS_NOTE + " " + HISTORICAL_P3_NOTE + " FY2018 total capital equals CET1 capital exactly - the "
         "Bank had not yet raised any Tier 2 capital (the first £400m Tier 2 subordinated debt was raised in May "
         "2019).",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "20.0%", "FY2024": "20.6%", "FY2023": "23.6%", "FY2022": "24.8%", "FY2021": "23.5%", "FY2020": "20.6%", "FY2019": "17.5%", "FY2018": "15.8%"})],
    p3_sources(),
    note=FY2021_BASIS_NOTE + " " + HISTORICAL_P3_NOTE,
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted exposure amount", {"FY2025": 12309, "FY2024": 11605, "FY2023": 11066, "FY2022": 11404, "FY2021": 12176, "FY2020": 13448, "FY2019": 15187, "FY2018": 13123})],
    p3_sources(),
    note=FY2021_BASIS_NOTE + " " + HISTORICAL_P3_NOTE,
)

# ---------------------------------------------------------------
# Sheet: RWA Breakdown
# ---------------------------------------------------------------
RWA_BREAKDOWN_SOURCES = (
    "Sources - Handelsbanken plc UK Group, UK OV1 'Overview of risk weighted exposure amounts' table, £m "
    "(FY2022-FY2025); Bank-only/solo 'RWAs' table, £m (FY2018-FY2020, see HISTORICAL BASIS NOTE on the Balance "
    "Sheet sheet):\n"
    f"FY2025 & FY2024: Risk and Capital Information according to Pillar 3 - 2025, p.9 - {P3_2025_URL}\n"
    f"FY2023 & FY2022: Pillar 3 Disclosure 2023, p.7 - {P3_2023_URL}\n"
    f"FY2020 & FY2019: Report and Financial Statements for the year ended 31 December 2020, p.50 - {AA2020_URL}\n"
    f"FY2018: Report and Financial Statements for the 9 month period ended 31 December 2018, p.21 - {AA2018_URL}\n"
    f"FY2021: Report and Financial Statements for the year ended 31 December 2021, 'Capital requirements' section, "
    f"the table introduced 'The following table summarises the Bank's RWAs', p.36 - {AR2021_URL}. This table breaks "
    f"RWA into exactly the same 3 categories as the FY2018-FY2020 tables below (Credit risk according to "
    f"standardised approach / Operational risk according to BIA / Market risks, explicitly nil), on the same "
    f"entity-own (Bank=Group) basis per FY2021_BASIS_NOTE - directly disclosed, not derived. Total ties exactly to "
    f"the Total RWAs sheet's own FY2021 figure (12,176).\n\n"
    + ENTITY_NOTE + "\n\n"
    + FY2021_BASIS_NOTE + " FY2018-FY2020's own tables only ever break RWA into 'Credit risk according to standardised "
    "approach' and 'Operational risk according to BIA' (Market risk RWA is explicitly nil in all three years - the "
    "Bank holds no trading book - and no 'Amounts below thresholds for deduction' line existed yet); mapped to the "
    "'Credit risk (excluding CCR)' and 'Operational risk' rows below respectively. Totals reconcile exactly to the "
    "Total RWAs sheet in every year shown."
)

rwa_breakdown_rows = [
    ("SECTION", "Risk weighted exposure amounts (UK OV1)", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 10634, "FY2024": 10184, "FY2023": 9940, "FY2022": 10364, "FY2021": 11181, "FY2020": 12483, "FY2019": 14320, "FY2018": 12337}),
    ("DATA", "Operational risk", {"FY2025": 1675, "FY2024": 1421, "FY2023": 1126, "FY2022": 1040, "FY2021": 995, "FY2020": 965, "FY2019": 867, "FY2018": 786}),
    ("DATA", "Amounts below thresholds for deduction (subject to 250% risk weight)", {"FY2025": 2, "FY2024": 2, "FY2023": 4, "FY2022": 10}),
    ("TOTAL", "Total RWA", {"FY2025": 12309, "FY2024": 11605, "FY2023": 11066, "FY2022": 11404, "FY2021": 12176, "FY2020": 13448, "FY2019": 15187, "FY2018": 13123}),
]

bw.add_rwa_breakdown_sheet(
    title="Handelsbanken plc — RWA Breakdown",
    subtitle="Handelsbanken plc UK Group (consolidated basis), £m. See source note at bottom.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=54,
    source_height=180,
    unit_suffix=" (£m)",
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total exposure measure excluding claims on central banks", {"FY2025": 23011, "FY2024": 22473, "FY2023": 24356, "FY2022": 25680}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "9.4%", "FY2024": "9.3%", "FY2023": "9.1%", "FY2022": "9.4%"}),
        ("Leverage ratio - CRR2 total exposure basis, £m (FY2018-FY2021, pre-KM1 methodology)", {"FY2021": 33635, "FY2020": 35325, "FY2019": 33323, "FY2018": 33290}),
        ("Leverage ratio - CRR2 basis (%) (FY2018-FY2021, pre-KM1 methodology)", {"FY2021": "7.3%", "FY2020": "6.7%", "FY2019": "6.8%", "FY2018": "6.2%"}),
    ],
    p3_sources(),
    note=FY2021_BASIS_NOTE + " " + HISTORICAL_P3_NOTE + " The UK Group is not in scope of the binding UK leverage "
         "ratio minimum requirement (below the size threshold) but the PRA expects a ratio above 3.25%, which it "
         "has maintained throughout. FY2018-FY2021's figures use a different, larger exposure measure (Tier 1 "
         "capital / total CRR2 exposure, including claims on central banks) than the 'excluding claims on central "
         "banks' KM1 basis used from FY2022 onward - the two are not directly comparable, hence the separate rows. "
         "The FY2018 Annual Report separately states that applying the (then-new) UK leverage ratio definition, "
         "which excludes the Bank of England deposit from the exposure measure, would increase FY2018's ratio to "
         "7.8% - not shown as its own row since no equivalent alternative figure was found for FY2019-FY2021.",
)

metric(
    "LCR", "£m / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value (average)", {"FY2025": 8039, "FY2024": 8853, "FY2023": 7946, "FY2022": 7904}),
        ("Total net cash outflows (adjusted value)", {"FY2025": 4572, "FY2024": 5400, "FY2023": 5220, "FY2022": 5377}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "180%", "FY2024": "165%", "FY2023": "153%", "FY2022": "147%", "FY2021": "Not disclosed (KM1 basis)"}),
        ("High-quality liquid assets, spot value as at year-end, £m (FY2018-FY2020, pre-KM1 methodology)", {"FY2020": 9023.7, "FY2019": 6946.4, "FY2018": 6535.6}),
        ("Net cash outflows, spot value as at year-end, £m (FY2018-FY2020, pre-KM1 methodology)", {"FY2020": 2746.7, "FY2019": 2057.5, "FY2018": 1413.7}),
        ("Liquidity Coverage Ratio (%) - spot, as at year-end (FY2018-FY2020, pre-KM1 methodology)", {"FY2020": "329%", "FY2019": "338%", "FY2018": "462%"}),
    ],
    p3_sources(),
    note=FY2021_BASIS_NOTE + " " + HISTORICAL_P3_NOTE + " LCR is a 12-month average of month-end observations from "
         "FY2022 onward. The FY2023 and FY2024 Annual Reports separately quote a narrower, single-point 'as at "
         "year end' LCR narrative (147% and 180% respectively) that happens to coincide with the average-basis KM1 "
         "figures shown here for those two years, but the FY2022 narrative figure (147%) differs from an earlier "
         "average-basis disclosure; treat the KM1 table above as the primary source. The FY2021 Annual Report "
         "separately states a spot LCR of 475% at 31 December 2021 - not on the same (averaged, KM1) basis as the "
         "figures above, so not included as a comparable data point. FY2018-FY2020's own LCR disclosures are, like "
         "FY2021's, single-point spot values as at year-end (not 12-month averages) - shown in their own separate "
         "rows above for the same reason FY2021's spot figure is excluded from the primary row, rather than left "
         "out entirely; HQLA/net cash outflow £'000 figures as disclosed were divided by 1,000 to convert to £m "
         "for consistency with this sheet's unit (e.g. FY2018: HQLA £6,535,601k / outflows £5,232,181k less "
         "inflows £3,818,447k = £1,413,734k net, giving 6535.6/1413.7 = 462%, matching the Bank's own disclosed "
         "462% exactly).",
)

metric(
    "NSFR", "£m / %",
    [
        ("Total available stable funding", {"FY2025": 19047, "FY2024": 19210, "FY2023": 19525, "FY2022": 20678}),
        ("Total required stable funding", {"FY2025": 14676, "FY2024": 14166, "FY2023": 14950, "FY2022": 15953}),
        ("NSFR ratio (%)", {"FY2025": "130%", "FY2024": "136%", "FY2023": "131%", "FY2022": "130%", "FY2021": "Not disclosed", "FY2020": "Not disclosed", "FY2019": "Not disclosed", "FY2018": "105% (internal interpretation of Basel NSFR rules, pre-UK NSFR regulation)"}),
    ],
    p3_sources(),
    note=FY2021_BASIS_NOTE + " " + HISTORICAL_P3_NOTE + " FY2018's Annual Report states the Bank operated with an "
         "NSFR of 105% 'at all times' during the period, based on its own internal interpretation of the (not yet "
         "UK-implemented) Basel NSFR rules - not a formal regulatory ratio. FY2019 and FY2020's Annual Reports "
         "name the NSFR as one of the Bank's monitored liquidity metrics but do not state a numeric value for "
         "either year.",
)

metric(
    "MREL Ratio", "£m / %",
    [
        ("MREL-eligible senior non-preferred debt issued", {"FY2025": 450, "FY2024": 200, "FY2023": 50, "FY2022": 150, "FY2021": 200, "FY2020": 200, "FY2019": 200}),
        ("Total capital resources (Total capital, see Total Capital sheet)", {"FY2025": 2456, "FY2024": 2389, "FY2023": 2614, "FY2022": 2826, "FY2021": 2864, "FY2020": 2766, "FY2019": 2650, "FY2018": 2071}),
        ("Total MREL ratio (% of RWA)", {"FY2025": "23.6%", "FY2020": "22.1%"}),
    ],
    (
        "Sources - Handelsbanken plc UK Group, Risk and Capital Management section of each Annual Report "
        "(Bank-only/solo basis FY2018-FY2020, see HISTORICAL BASIS NOTE on the Balance Sheet sheet):\n"
        f"FY2025: Annual Report 2025, p.67 - {AR2025_URL}\n"
        f"FY2024: Annual Report 2024, p.65 - {AR2024_URL}\n"
        f"FY2023: Annual Report 2023, p.70 - {AR2023_URL}\n"
        f"FY2022: Annual Report 2022, p.79 - {AR2022_URL}\n"
        f"FY2021: Annual Report 2021, p.63 - {AR2021_URL}\n"
        f"FY2020 & FY2019: Report and Financial Statements for the year ended 31 December 2020, p.51 - {AA2020_URL}"
    ),
    note="Handelsbanken plc, as a material subsidiary of a foreign-owned group, is subject to MREL (21.2% of RWA "
         "as at FY2025, reduced by any applicable Bank of England scalar; the end-state 21.6%-of-RWA requirement "
         "took effect 1 January 2023, following an 18%-of-RWA interim requirement from 1 January 2020 - FY2018 "
         "entirely pre-dates MREL applying to the Bank at all, hence its blank cells in this sheet, and FY2019's "
         "£200m of MREL-eligible debt was only issued in December 2019, in preparation for that interim "
         "requirement). No Pillar 3/KM1-format numeric MREL resources or ratio was found for FY2021-FY2024, where "
         "the ratio cell is left blank rather than computed by us from the two rows above, since the Bank did not "
         "itself state a ratio for those years (a reader can derive an approximate figure from the two rows shown, "
         "but we have not presented it as a disclosed fact). FY2025 and FY2020 are the two years where the Bank's "
         "own Annual Report directly states a combined ratio: FY2025's 'total capital and MREL ratio of 23.6% of "
         "RWA' (£450m MREL-eligible debt plus £2,456m of capital resources), and FY2020's 'total capital and MREL "
         "ratio of 22.1% of RWA' (£200m MREL-eligible debt plus £2.8bn of capital resources, i.e. the £2,766m "
         "Total capital resources row above, rounded).",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 29804612, "FY2024": 30713857, "FY2023": 32367941, "FY2022": 32764625, "FY2021": 32658251, "FY2020": 33813925, "FY2019": 31561734, "FY2018": 31261576}),
        ("Loans to the public", {"FY2025": 18414143, "FY2024": 17826369, "FY2023": 18023996, "FY2022": 19028715, "FY2021": 20177506, "FY2020": 20858150, "FY2019": 21403516, "FY2018": 20604034}),
        ("Deposits from the public", {"FY2025": 21467902, "FY2024": 20880491, "FY2023": 20359402, "FY2022": 20486618, "FY2021": 19201850, "FY2020": 19090724, "FY2019": 16456660, "FY2018": 14976954}),
        ("Total equity", {"FY2025": 2442808, "FY2024": 2623634, "FY2023": 2889685, "FY2022": 2739461, "FY2021": 2486829, "FY2020": 2392453, "FY2019": 2272844, "FY2018": 2089302}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total income", {"FY2025": 871569, "FY2024": 942176, "FY2023": 1006356, "FY2022": 733894, "FY2021": 532853, "FY2020": 506110, "FY2019": 566281, "FY2018": 49162}),
        ("Total expenses", {"FY2025": -456798, "FY2024": -454305, "FY2023": -427739, "FY2022": -386381, "FY2021": -406207, "FY2020": -334879, "FY2019": -315937, "FY2018": -29374}),
        ("Profit for the year", {"FY2025": 303861, "FY2024": 359290, "FY2023": 415740, "FY2022": 252632, "FY2021": 99113, "FY2020": 119609, "FY2019": 183542, "FY2018": 13633}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Dividend paid", {"FY2025": -484687, "FY2024": -625341, "FY2023": -265516, "FY2022": 0, "FY2021": 0, "FY2020": 0, "FY2019": 0, "FY2018": 0}),
        ("Total comprehensive income for the year", {"FY2025": 303861, "FY2024": 359290, "FY2023": 415740, "FY2022": 252632, "FY2021": 99113, "FY2020": 119609, "FY2019": 183542, "FY2018": 13633}),
        ("Closing Total equity", {"FY2025": 2442808, "FY2024": 2623634, "FY2023": 2889685, "FY2022": 2739461, "FY2021": 2486829, "FY2020": 2392453, "FY2019": 2272844, "FY2018": 2089302}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": -819277, "FY2024": 836309, "FY2023": 1215640, "FY2022": -351346, "FY2021": -670515, "FY2020": 2113097, "FY2019": 499835, "FY2018": -1096479}),
        ("Net cash from/(used in) investing activities", {"FY2025": -19811, "FY2024": -18114, "FY2023": -17972, "FY2022": -9170, "FY2021": -5725, "FY2020": -19675, "FY2019": -14178, "FY2018": 7154061}),
        ("Net cash from/(used in) financing activities", {"FY2025": -496588, "FY2024": -637225, "FY2023": -277940, "FY2022": -12141, "FY2021": -13551, "FY2020": -12099, "FY2019": -10006, "FY2018": 405050}),
        ("Cash balance at end of year", {"FY2025": 7761527, "FY2024": 9097190, "FY2023": 8916214, "FY2022": 7996622, "FY2021": 8368955, "FY2020": 9059083, "FY2019": 6977760, "FY2018": 6462632}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "17.5%", "FY2024": "18.0%", "FY2023": "20.0%", "FY2022": "21.3%", "FY2021": "20.2%", "FY2020": "17.6%", "FY2019": "14.8%", "FY2018": "15.8%"}),
        ("Tier 1 Ratio", {"FY2025": "17.5%", "FY2024": "18.0%", "FY2023": "20.0%", "FY2022": "21.3%", "FY2021": "20.2%", "FY2020": "17.6%", "FY2019": "14.8%", "FY2018": "15.8%"}),
        ("Total Capital Ratio", {"FY2025": "20.0%", "FY2024": "20.6%", "FY2023": "23.6%", "FY2022": "24.8%", "FY2021": "23.5%", "FY2020": "20.6%", "FY2019": "17.5%", "FY2018": "15.8%"}),
        ("Leverage Ratio", {"FY2025": "9.4%", "FY2024": "9.3%", "FY2023": "9.1%", "FY2022": "9.4%", "FY2021": "7.3%", "FY2020": "6.7%", "FY2019": "6.8%", "FY2018": "6.2%"}),
        ("LCR", {"FY2025": "180%", "FY2024": "165%", "FY2023": "153%", "FY2022": "147%", "FY2020": "329%", "FY2019": "338%", "FY2018": "462%"}),
        ("NSFR", {"FY2025": "130%", "FY2024": "136%", "FY2023": "131%", "FY2022": "130%", "FY2018": "105%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Handelsbanken plc is a young UK-incorporated entity "
         "(2018) - FY2021 pre-dates its Group/Bank consolidated-reporting split and its first formal Pillar 3/KM1 "
         "disclosure (first published for FY2022), so FY2021's leverage ratio uses a different, non-comparable "
         "methodology (see Leverage Ratio sheet) and has no LCR/NSFR figure at all. FY2018-FY2020 are on a "
         "further different basis still (Bank-only/solo, not UK Group consolidated - see the Balance Sheet sheet's "
         "HISTORICAL BASIS NOTE): their Leverage Ratio and LCR figures use the same pre-KM1/pre-averaged "
         "methodologies as FY2021's, and their NSFR is blank except FY2018's 105% (an internal, pre-regulation "
         "estimate, not directly comparable to the FY2022+ KM1 figures). FY2018 itself covers only a 9-month stub "
         "period (11 April - 31 December 2018) in which the Bank only actually traded for the final month, "
         "following the transfer of trade and assets from Svenska Handelsbanken AB's UK branch on 1 December 2018 "
         "- its Income Statement and Cash Flow Statement totals reflect that one month of trading, not a full "
         "year, while its Balance Sheet is a genuine 31 December 2018 snapshot.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/HANDELSBANKEN FINANCIALS.xlsx")
