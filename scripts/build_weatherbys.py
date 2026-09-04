import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
COMPANY = "Weatherbys Bank Limited"
COMPANY_NO = "02943300"
FRN = "204571"
LEI = "549300OF84KDPIFN4M17"

AR_URLS = {
    "FY2025": "https://www.weatherbys.bank/weatherbys-banking-group-annual-report-2025/",
    "FY2024": "https://www.weatherbys.bank/app/uploads/2025/04/Weatherbys-Banking-Group-Annual-Report-2024.pdf",
    "FY2023": "https://www.weatherbys.bank/app/uploads/2024/05/Weatherbys-Banking-Group-Annual-Report-2023.pdf",
    "FY2022": "https://www.weatherbys.bank/app/uploads/2023/05/Weatherbys-Banking-Group-Annual_Report-2022.pdf",
}
P3_URLS = {
    "FY2024": "https://www.weatherbys.bank/app/uploads/2025/04/Weatherbys-Bank-Pillar-3-Disclosures-2024.pdf",
    "FY2023": "https://weatherbys.bank/app/uploads/2024/05/Weatherbys-Bank-Pillar-3-Dislcosures-2023.pdf",
    "FY2022": "https://weatherbys.bank/app/uploads/2023/05/Weatherbys-Bank-Pillar-3-Dislcosures-2022.pdf",
    "FY2021": "https://www.weatherbys.bank/app/uploads/2022/05/Pillar-3-2021-v2.0-Weatherbys-Bank.pdf",
}
CH_URL = f"https://find-and-update.company-information.service.gov.uk/company/{COMPANY_NO}"
PRA_URL = "https://www.bankofengland.co.uk/prudential-regulation/authorisations/which-firms-does-the-pra-regulate"

ENTITY_NOTE = (
    f"Entity verification: {COMPANY}, Companies House {COMPANY_NO}, FRN {FRN}, LEI {LEI}; "
    "the supplied Banks List 2608.xlsx, the Weatherbys corporate-information page, the PRA register, "
    "and Companies House identify the same legal bank. The workbook uses Weatherbys Banking Group's "
    "consolidated cash-flow statement because that is the audited cash-flow presentation in the annual "
    "reports. The official Pillar 3 disclosures are consolidated Group/Solo disclosures: the documents "
    "state that the solo-consolidated group includes Weatherbys Bank Limited and its subsidiaries and that "
    "there are no differences between accounting and prudential consolidation for the Group. Group figures "
    "are therefore used only where the source explicitly labels them Group and Solo; unrelated wider-group "
    "figures are not substituted. Amounts are GBP'000 unless stated otherwise."
)

CASH_SOURCES = (
    "Sources - Weatherbys Banking Group consolidated statement of cash flows, GBP'000: "
    f"FY2025/FY2024: Annual Report and Financial Accounts 2025, p.64 - {AR_URLS['FY2025']}; "
    f"FY2024/FY2023: Annual Report & Accounts 2024, p.45 - {AR_URLS['FY2024']}; "
    f"FY2023/FY2022: Annual Report & Accounts 2023, p.50 - {AR_URLS['FY2023']}; "
    f"FY2022/FY2021: Annual Report & Accounts 2022, p.46 - {AR_URLS['FY2022']}.\n\n"
    + ENTITY_NOTE
    + " The 2024 statement labels the financing section's subtotal as investing activities, but its placement and figures are the financing cash flows; the source presentation is retained with a corrected descriptive label."
)

rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit for the financial year before exceptional items", {"FY2025": 19244, "FY2024": 18270, "FY2023": 24735, "FY2022": 11909, "FY2021": 5206}),
    ("DATA", "Depreciation, impairment and amortisation of fixed assets", {"FY2025": 7065, "FY2024": 4506, "FY2023": 2758, "FY2022": 2786, "FY2021": 2402}),
    ("DATA", "Amortisation of debt securities", {"FY2025": -1870, "FY2024": -1138, "FY2023": 413, "FY2022": 443, "FY2021": 133}),
    ("DATA", "Taxation expense", {"FY2025": 3830, "FY2024": 6306, "FY2023": 8348, "FY2022": 3504, "FY2021": 1596}),
    ("DATA", "Increase in prepayments and accrued income", {"FY2025": -1508, "FY2024": -4032, "FY2023": -4930, "FY2022": -6282, "FY2021": -1055}),
    ("DATA", "Decrease/(increase) in trade and other debtors", {"FY2025": -678, "FY2024": 38, "FY2023": -201, "FY2022": -364, "FY2021": 20}),
    ("DATA", "Change in fair value of financial instruments", {"FY2025": 6430, "FY2024": -1624, "FY2023": 7216, "FY2022": -8619, "FY2021": -3069}),
    ("DATA", "Movement in margin call", {"FY2025": -6550}),
    ("DATA", "Loss/(gain) on investments", {"FY2025": 20, "FY2024": 71, "FY2023": -17, "FY2022": 104, "FY2021": 3}),
    ("DATA", "Loss/(gain) on disposal of subsidiary/tangible fixed assets", {"FY2025": -10235}),
    ("DATA", "Change in trade and other creditors", {"FY2025": 2299, "FY2024": -2982, "FY2023": 11753, "FY2022": 2607, "FY2021": -496}),
    ("DATA", "Net decrease/(increase) in provisions", {"FY2025": -64, "FY2024": -1366, "FY2023": 5968, "FY2022": 2623, "FY2021": 1123}),
    ("DATA", "Increase/(decrease) in provision for bad and doubtful debts", {"FY2025": 1074, "FY2024": 46, "FY2023": 184, "FY2022": -25, "FY2021": -518}),
    ("DATA", "Net increase/(decrease) in deposits from customers", {"FY2025": 193121, "FY2024": 203231, "FY2023": -16626, "FY2022": 116590, "FY2021": 315834}),
    ("DATA", "Net increase in loans and advances to customers", {"FY2025": -138623, "FY2024": -38018, "FY2023": -46309, "FY2022": -30957, "FY2021": -65508}),
    ("TOTAL", "Cash from operations", {"FY2025": 73555, "FY2024": 183308, "FY2023": -6708, "FY2022": 94319, "FY2021": 255671}),
    ("DATA", "Taxation paid", {"FY2025": -4301, "FY2024": -5721, "FY2023": -5421, "FY2022": -2320, "FY2021": -678}),
    ("TOTAL", "Net cash generated/(used) from operating activities", {"FY2025": 69254, "FY2024": 177587, "FY2023": -12129, "FY2022": 91999, "FY2021": 254993}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Sale of subsidiary undertaking", {"FY2025": 10552}),
    ("DATA", "Income from joint venture", {"FY2025": 400}),
    ("DATA", "Investment in joint venture", {"FY2023": -60, "FY2022": -280, "FY2021": -12}),
    ("DATA", "Purchase of investment securities", {"FY2025": -361092, "FY2024": -173844, "FY2023": -66857, "FY2022": -136837, "FY2021": -22148}),
    ("DATA", "Sale and maturities of investment securities", {"FY2025": 190722, "FY2024": 72330, "FY2023": 127951, "FY2022": 46415, "FY2021": 38649}),
    ("DATA", "Purchase of tangible fixed assets", {"FY2025": -4139, "FY2024": -2103, "FY2021": -3939}),
    ("DATA", "Purchase of intangible fixed assets", {"FY2025": -13123, "FY2024": -6502}),
    ("DATA", "Purchase of intangible/tangible fixed assets", {"FY2023": -7251, "FY2022": -6456}),
    ("TOTAL", "Net cash (used)/generated from investing activities", {"FY2025": -176680, "FY2024": -110119, "FY2023": 53783, "FY2022": -97158, "FY2021": 12550}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Issue of contingent convertible securities", {"FY2023": 3000}),
    ("DATA", "Equity dividends paid", {"FY2025": -11100, "FY2024": -5000, "FY2023": -5000, "FY2022": -2000, "FY2021": -1250}),
    ("TOTAL", "Net cash (used)/generated from financing activities", {"FY2025": -11100, "FY2024": -5000, "FY2023": -2000, "FY2022": -2000, "FY2021": -1250}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": -118526, "FY2024": 62468, "FY2023": 39654, "FY2022": -7159, "FY2021": 266293}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 687343, "FY2024": 624875, "FY2023": 585221, "FY2022": 592380, "FY2021": 326087}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 568817, "FY2024": 687343, "FY2023": 624875, "FY2022": 585221, "FY2021": 592380}),
]

AR2024_OWN_URL = AR_URLS["FY2024"]

BS_RESTATEMENT_NOTE = (
    "AR2025's own restated FY2024 comparative balance sheet (note 36, 'Statement of financial position "
    "reclassification') moves broker commissions and interest receivable/payable between prepayments, loans "
    "and advances to customers, other liabilities and customer accounts, with no impact on profit or net "
    "assets - AR2025's FY2024 Total assets is £1,847,554k against AR2024's own originally published "
    "£1,848,494k, a further ~£940k gap beyond what note 36 explains. Per project convention, FY2024 uses "
    "AR2024's own originally published figures throughout (Total assets £1,848,494k), not the later restated "
    "comparative; the two years' FY2024 Total equity figures agree exactly (£100,043k) and the Profit & Loss/ "
    "Statement of Changes in Equity figures for FY2024 are unaffected by the reclassification. Prior to 2024 "
    "the liquid-balances line is labelled 'Loans and advances to banks' (FY2021-FY2023); from 2024 it is "
    "labelled 'Cash at banks' - the same underlying balance, relabelled, not a new line."
)
BS_SOURCES = (
    "Sources - Weatherbys Banking Group consolidated statement of financial position, GBP'000: "
    f"FY2025: Annual Report and Financial Accounts 2025, p.60 - {AR_URLS['FY2025']}; "
    f"FY2024: Annual Report & Accounts 2024, p.41 - {AR2024_OWN_URL}; "
    f"FY2023: Annual Report & Accounts 2023, p.46 - {AR_URLS['FY2023']}; "
    f"FY2022/FY2021: Annual Report & Accounts 2022, p.42 - {AR_URLS['FY2022']}.\n\n"
    + ENTITY_NOTE
    + " " + BS_RESTATEMENT_NOTE
)

bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash at banks / Loans and advances to banks", {"FY2025": 575367, "FY2024": 687343, "FY2023": 624875, "FY2022": 585221, "FY2021": 592380}),
    ("DATA", "Derivative financial assets", {"FY2025": 1394, "FY2024": 5018, "FY2023": 5194, "FY2022": 9813, "FY2021": 961}),
    ("DATA", "Loans and advances to customers", {"FY2025": 1006160, "FY2024": 859672, "FY2023": 821700, "FY2022": 775573, "FY2021": 744591}),
    ("DATA", "Debt securities", {"FY2025": 420989, "FY2024": 248749, "FY2023": 146097, "FY2022": 207605, "FY2021": 117625}),
    ("DATA", "Investment in joint venture", {"FY2024": 670, "FY2023": 670, "FY2022": 610, "FY2021": 330}),
    ("DATA", "Investments", {"FY2025": 364, "FY2024": 384, "FY2023": 455, "FY2022": 438, "FY2021": 542}),
    ("DATA", "Intangible fixed assets", {"FY2025": 24676, "FY2024": 16194, "FY2023": 12327, "FY2022": 6145, "FY2021": 3154}),
    ("DATA", "Tangible fixed assets", {"FY2025": 10936, "FY2024": 9397, "FY2023": 9283, "FY2022": 11216, "FY2021": 10747}),
    ("DATA", "Other assets", {"FY2025": 2753, "FY2024": 1875, "FY2023": 1913, "FY2022": 1711, "FY2021": 1803}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 10808, "FY2024": 19192, "FY2023": 15160, "FY2022": 10232, "FY2021": 3950}),
    ("TOTAL", "Total assets", {"FY2025": 2053447, "FY2024": 1848494, "FY2023": 1637674, "FY2022": 1608564, "FY2021": 1476083}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Derivative financial liabilities", {"FY2025": 4075, "FY2024": 1269, "FY2023": 3069, "FY2022": 472, "FY2021": 238}),
    ("DATA", "Customer accounts", {"FY2025": 1905431, "FY2024": 1707796, "FY2023": 1504566, "FY2022": 1521191, "FY2021": 1404601}),
    ("DATA", "Other liabilities", {"FY2025": 12734, "FY2024": 18287, "FY2023": 22583, "FY2022": 7903, "FY2021": 4568}),
    ("DATA", "Accruals and deferred income", {"FY2025": 10093, "FY2024": 11099, "FY2023": 12465, "FY2022": 6498, "FY2021": 3876}),
    ("DATA", "Subordinated loan", {"FY2025": 10000, "FY2024": 10000, "FY2023": 10000, "FY2022": 10000, "FY2021": 10000}),
    ("TOTAL", "Total liabilities", {"FY2025": 1942333, "FY2024": 1748451, "FY2023": 1552683, "FY2022": 1546064, "FY2021": 1423283}),
    ("SECTION", "Shareholders' funds", {}),
    ("DATA", "Called up share capital", {"FY2025": 7000, "FY2024": 7000, "FY2023": 7000, "FY2022": 7000, "FY2021": 7000}),
    ("DATA", "Contingent convertible securities", {"FY2025": 3000, "FY2024": 3000, "FY2023": 3000}),
    ("DATA", "Revaluation reserve", {"FY2025": 231, "FY2024": 404, "FY2023": 522, "FY2022": 766, "FY2021": 975}),
    ("DATA", "Profit and loss account", {"FY2025": 100883, "FY2024": 89639, "FY2023": 74469, "FY2022": 54734, "FY2021": 44825}),
    ("TOTAL", "Total equity", {"FY2025": 111114, "FY2024": 100043, "FY2023": 84991, "FY2022": 62500, "FY2021": 52800}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 2053447, "FY2024": 1848494, "FY2023": 1637674, "FY2022": 1608564, "FY2021": 1476083}),
]

PL_SOURCES = (
    "Sources - Weatherbys Banking Group consolidated income statement, GBP'000: "
    f"FY2025: Annual Report and Financial Accounts 2025, p.58 - {AR_URLS['FY2025']}; "
    f"FY2024: Annual Report & Accounts 2024, p.39 - {AR2024_OWN_URL}; "
    f"FY2023: Annual Report & Accounts 2023, pp.44-45 - {AR_URLS['FY2023']}; "
    f"FY2022/FY2021: Annual Report & Accounts 2022, p.40 - {AR_URLS['FY2022']}.\n\n"
    + ENTITY_NOTE
    + " FY2025's exceptional item is a £10,238k gain (sale of subsidiary/tangible fixed assets, matching the "
    "Cash Flow Statement's disposal line); FY2024's exceptional item is a £2,128k charge; FY2023/FY2022/FY2021 "
    "had no exceptional item line. FY2023 additionally discloses a small Rent Receivable line (£84k) not "
    "present in other years."
)

pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable - arising from debt securities", {"FY2025": 12442, "FY2024": 12235, "FY2023": 8846, "FY2022": 2642, "FY2021": 655}),
    ("DATA", "Interest receivable - other interest and similar income", {"FY2025": 102751, "FY2024": 104058, "FY2023": 93591, "FY2022": 51278, "FY2021": 35361}),
    ("DATA", "Interest payable", {"FY2025": -36240, "FY2024": -37279, "FY2023": -24283, "FY2022": -4733, "FY2021": -3996}),
    ("TOTAL", "Net interest income", {"FY2025": 78953, "FY2024": 79014, "FY2023": 78154, "FY2022": 49187, "FY2021": 32020}),
    ("DATA", "Fees and commissions receivable", {"FY2025": 8973, "FY2024": 7852, "FY2023": 6796, "FY2022": 5862, "FY2021": 5118}),
    ("DATA", "Fees and commissions payable", {"FY2025": -1130, "FY2024": -942, "FY2023": -615, "FY2022": -546, "FY2021": -493}),
    ("DATA", "Rent receivable", {"FY2023": 84}),
    ("DATA", "Other operating income", {"FY2025": 4299, "FY2024": 4502, "FY2023": 4007, "FY2022": 3526, "FY2021": 3130}),
    ("TOTAL", "Operating income", {"FY2025": 91095, "FY2024": 90426, "FY2023": 88426, "FY2022": 58029, "FY2021": 39775}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "(Loss)/gain on value of derivatives", {"FY2025": -673, "FY2024": 117, "FY2023": 75, "FY2022": 76, "FY2021": 2362}),
    ("DATA", "Administrative expenses", {"FY2025": -65873, "FY2024": -55163, "FY2023": -50274, "FY2022": -39014, "FY2021": -31654}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -7065, "FY2024": -4505, "FY2023": -2758, "FY2022": -2786, "FY2021": -2402}),
    ("DATA", "Impairment charge on loans and advances", {"FY2025": -4648, "FY2024": -4571, "FY2023": -2784, "FY2022": -1400, "FY2021": -1559}),
    ("DATA", "Share of operating profit in joint venture", {"FY2024": 400, "FY2023": 400, "FY2022": 340, "FY2021": 280}),
    ("TOTAL", "Operating profit before exceptional items and tax", {"FY2025": 12836, "FY2024": 26704, "FY2023": 33085, "FY2022": 15245, "FY2021": 6802}),
    ("DATA", "Exceptional item", {"FY2025": 10238, "FY2024": -2128}),
    ("TOTAL", "Operating profit before tax", {"FY2025": 23074, "FY2024": 24576, "FY2023": 33085, "FY2022": 15245, "FY2021": 6802}),
    ("DATA", "Taxation on profit", {"FY2025": -3830, "FY2024": -6306, "FY2023": -8350, "FY2022": -3336, "FY2021": -1596}),
    ("TOTAL", "Profit for the financial year", {"FY2025": 19244, "FY2024": 18270, "FY2023": 24735, "FY2022": 11909, "FY2021": 5206}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Revaluation of tangible fixed assets", {"FY2025": -173, "FY2024": -118, "FY2023": -244, "FY2022": -209, "FY2021": 458}),
    ("TOTAL", "Total comprehensive income for the year", {"FY2025": 19071, "FY2024": 18152, "FY2023": 24491, "FY2022": 11700, "FY2021": 5664}),
]

EQ_SOURCES = (
    "Sources - Weatherbys Banking Group consolidated statement of changes in equity, GBP'000: "
    f"AR2025, p.62 - {AR_URLS['FY2025']}; AR2024, p.43 - {AR2024_OWN_URL}; AR2023, p.48 - {AR_URLS['FY2023']}; "
    f"AR2022, p.44 - {AR_URLS['FY2022']}.\n\n"
    + ENTITY_NOTE
    + " Every year's closing balance ties exactly to the next year's opening balance and to that year's own "
    "Balance Sheet Total equity - zero undocumented plug rows. Contingent Convertible Securities first appear "
    "in FY2023 (a £3,000k issuance)."
)

eq_headers = ["Share capital", "Contingent Convertible Securities", "Revaluation reserve", "Profit & loss account", "Total equity"]
eq_rows = [
    ("DATA", "1 January 2021", (7000, None, 517, 40869, 48386)),
    ("DATA", "Profit for the year", (None, None, None, 5206, 5206)),
    ("DATA", "Revaluation of tangible fixed assets", (None, None, 458, None, 458)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, 458, 5206, 5664)),
    ("DATA", "Dividends", (None, None, None, -1250, -1250)),
    ("TOTAL", "31 December 2021", (7000, None, 975, 44825, 52800)),
    ("DATA", "Profit for the year", (None, None, None, 11909, 11909)),
    ("DATA", "Revaluation of tangible fixed assets", (None, None, -209, None, -209)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, -209, 11909, 11700)),
    ("DATA", "Dividends", (None, None, None, -2000, -2000)),
    ("TOTAL", "31 December 2022", (7000, None, 766, 54734, 62500)),
    ("DATA", "Profit for the year", (None, None, None, 24735, 24735)),
    ("DATA", "Revaluation of tangible fixed assets", (None, None, -244, None, -244)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, -244, 24735, 24491)),
    ("DATA", "Dividends", (None, None, None, -5000, -5000)),
    ("DATA", "Issue of contingent convertible securities", (None, 3000, None, None, 3000)),
    ("TOTAL", "31 December 2023", (7000, 3000, 522, 74469, 84991)),
    ("DATA", "Profit for the year", (None, None, None, 18270, 18270)),
    ("DATA", "Revaluation of tangible fixed assets", (None, None, -118, None, -118)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, -118, 18270, 18152)),
    ("DATA", "Dividends", (None, None, None, -3100, -3100)),
    ("TOTAL", "31 December 2024", (7000, 3000, 404, 89639, 100043)),
    ("DATA", "Profit for the year", (None, None, None, 19244, 19244)),
    ("DATA", "Revaluation of tangible fixed assets", (None, None, -173, None, -173)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, -173, 19244, 19071)),
    ("DATA", "Dividends", (None, None, None, -8000, -8000)),
    ("TOTAL", "31 December 2025", (7000, 3000, 231, 100883, 111114)),
]

AQ_SOURCES = (
    "Sources - Weatherbys Bank Limited Pillar 3 Disclosures, Group and Solo (identical, Table 5/Table 6), "
    f"GBP'000: FY2025 impairment/NPL data from Annual Report and Financial Accounts 2025, pp.79-80 (Banking "
    f"Group basis) - {AR_URLS['FY2025']}; FY2024 from Annual Report & Accounts 2024, p.60 and Pillar 3 "
    f"Disclosures 2024, pp.7-8 - {AR2024_OWN_URL} and {P3_URLS['FY2024']}; FY2023 from Annual Report & "
    f"Accounts 2023, p.65 and Pillar 3 Disclosures 2023, pp.6-7 - {AR_URLS['FY2023']} and {P3_URLS['FY2023']}; "
    f"FY2022 from Annual Report & Accounts 2022, p.62 and Pillar 3 Disclosures 2022, pp.8-9 - {AR_URLS['FY2022']} "
    f"and {P3_URLS['FY2022']}; FY2021 from Annual Report & Accounts 2022, p.62 (2021 comparative) and Pillar 3 "
    f"Disclosures 2021, pp.7-8 - {AR_URLS['FY2022']} and {P3_URLS['FY2021']}.\n\n"
    + ENTITY_NOTE
    + " Gross loans and advances to customers is derived as the Balance Sheet's net Loans and advances to "
    "customers plus the Loan loss provision balance from each year's own Note 15/16 (Banking Group basis); "
    "this ties exactly to the Balance Sheet's net figure every year. FY2025's Note 15 Balance Sheet loan loss "
    "provision (£5,333k) differs by £5k from Note 16's cumulative provision total (£5,338k) - a small internal "
    "document discrepancy, reproduced as-stated rather than forced to tie; both figures are shown. The "
    "regulatory credit risk exposure table (Pillar 3 Table 6) is a broader Pillar 1 exposure-class measure "
    "before credit risk mitigation (includes central bank/financial institution/covered bond exposures, not "
    "just customer loans) and does not tie to the narrower Balance Sheet loans line - shown as supplementary "
    "risk categorisation, not forced to reconcile."
)

def npl_ratio(npl, gross):
    return f"{npl / gross * 100:.2f}%"

def coverage_ratio(prov, npl):
    return f"{prov / npl * 100:.2f}%"

aq_gross = {"FY2025": 1011493, "FY2024": 863936, "FY2023": 825925, "FY2022": 779193, "FY2021": 748236}
aq_prov_bs = {"FY2025": -5333, "FY2024": -4264, "FY2023": -4225, "FY2022": -3620, "FY2021": -3645}
aq_prov_total = {"FY2025": 5338, "FY2024": 4264, "FY2023": 4225, "FY2022": 3620, "FY2021": 3645}
aq_npl = {"FY2025": 11193, "FY2024": 10452, "FY2023": 9628, "FY2022": 6847, "FY2021": 6372}

aq_rows = [
    ("SECTION", "Loans and advances to customers - credit quality (Banking Group)", {}),
    ("DATA", "Gross loans and advances to customers", aq_gross),
    ("DATA", "Loan loss provision (Balance Sheet, Note 15)", aq_prov_bs),
    ("TOTAL", "Net loans and advances to customers", {"FY2025": 1006160, "FY2024": 859672, "FY2023": 821700, "FY2022": 775573, "FY2021": 744591}),
    ("DATA", "Total provisions for bad and doubtful debts (Note 16 cumulative)", aq_prov_total),
    ("DATA", "Non-performing loans and advances to customers (before provisions)", aq_npl),
    ("DATA", "NPL ratio (non-performing loans / gross loans)", {y: npl_ratio(aq_npl[y], aq_gross[y]) for y in YEARS}),
    ("DATA", "Coverage ratio (total provisions / non-performing loans)", {y: coverage_ratio(aq_prov_total[y], aq_npl[y]) for y in YEARS}),
    ("SECTION", "Regulatory credit risk exposure by class (Pillar 3 Table 6, before credit risk mitigation)", {}),
    ("DATA", "Central Government and Central Banks", {"FY2025": None, "FY2024": 760594, "FY2023": 645464, "FY2022": 646149, "FY2021": 577637}),
    ("DATA", "Financial institutions", {"FY2024": 65986, "FY2023": 40329, "FY2022": 48477, "FY2021": 38362}),
    ("DATA", "Covered Bonds", {"FY2024": 86742, "FY2023": 60875, "FY2022": 67566, "FY2021": 51916}),
    ("DATA", "Multilateral Development Banks", {"FY2024": 38424, "FY2023": 29455, "FY2022": 37092, "FY2021": 43634}),
    ("DATA", "Corporates", {"FY2024": 0, "FY2023": 0, "FY2022": 15, "FY2021": 99}),
    ("DATA", "Retail", {"FY2024": 273745, "FY2023": 239489, "FY2022": 196497, "FY2021": 131874}),
    ("DATA", "CBILs - Government Guaranteed", {"FY2024": 15644, "FY2023": 10628, "FY2022": 12793, "FY2021": 13240}),
    ("DATA", "Secured on real estate property", {"FY2024": 578244, "FY2023": 571853, "FY2022": 568369, "FY2021": 581162}),
    ("DATA", "Other items", {"FY2024": 42329, "FY2023": 35556, "FY2022": 22514, "FY2021": 34363}),
    ("DATA", "Exposures In Default", {"FY2024": 12703, "FY2023": 14760, "FY2022": 9269, "FY2021": 7139}),
    ("DATA", "Credit Value Adjustment", {"FY2024": 6164, "FY2023": 1784, "FY2021": 1549}),
    ("TOTAL", "Total regulatory credit risk exposure", {"FY2024": 1880575, "FY2023": 1650193, "FY2022": 1608741, "FY2021": 1480975}),
]

RWA_SOURCES = (
    "Sources - Weatherbys Bank Limited Pillar 3 Disclosures, Group/Solo (identical), Tables 3-4, GBP'000: "
    f"FY2024, pp.6-7 - {P3_URLS['FY2024']}; FY2023, p.7 - {P3_URLS['FY2023']}; FY2022, pp.7-8 - {P3_URLS['FY2022']}; "
    f"FY2021, pp.5-7 - {P3_URLS['FY2021']}.\n\n"
    + ENTITY_NOTE
    + " Weatherbys does not publish a UK OV1-style risk-weighted-exposure-amount table by category - instead "
    "each Pillar 3 disclosure gives the minimum capital requirement per credit risk exposure class (Table 3) "
    "and per Pillar 1 risk type (Table 4). This RWA Breakdown derives each category's risk-weighted-asset "
    "equivalent by dividing its capital requirement by the disclosed conversion rate: FY2021's Table 3 header "
    "explicitly states 'Minimum Capital Requirement 8%' (the standard CRR Pillar 1 rate, confirmed in the "
    "accompanying text - 'a factor of 8% is applied to the risk weighted exposure amounts'), so FY2021 uses "
    "8%. From FY2022 onward, the PRA set the Bank's own Total Capital Requirement (TCR) at 9% of RWAs (per "
    "the FY2022 disclosure's own text: 'In September 2022 the PRA set the Bank's TCR at 9% of RWAs plus a "
    "static add-on of £4.4m'), and Table 3/4's own 'minimum capital requirement' figures for FY2022-FY2024 "
    "are computed at this firm-specific 9% rate rather than the generic 8% - confirmed by summing each year's "
    "credit-risk and operational-risk capital requirement components and dividing by 9%, which reconciles to "
    "the separately and directly disclosed Total RWAs figure (see the Total RWAs sheet) to within 0.3% every "
    "year, versus a >10% mismatch at 8%. This is therefore a derived breakdown, not a directly published "
    "RWEA/OV1 table - the small remaining gap to the disclosed Total RWAs headline (FY2021: £5k/0.001%; "
    "FY2022: £1,349k/0.28%; FY2023: £199k/0.04%; FY2024: £1,113k/0.18%) reflects rounding in the underlying, "
    "more precise Bank calculation. The Static Pension add-on (a Pillar 2 item, not RWA-based) is excluded "
    "from this breakdown. FY2025 is blank because no FY2025 Pillar 3 disclosure was located (same access gap "
    "already noted on the other Pillar 3 sheets)."
)

rwa_rows = [
    ("SECTION", "Credit risk, by exposure class (derived, see sources)", {}),
    ("DATA", "Financial institutions", {"FY2024": 14667, "FY2023": 8811, "FY2022": 10256, "FY2021": 8450}),
    ("DATA", "Covered bonds", {"FY2024": 8678, "FY2023": 6089, "FY2022": 6756, "FY2021": 5188}),
    ("DATA", "Corporates", {"FY2024": 0, "FY2023": 0, "FY2022": 11, "FY2021": 100}),
    ("DATA", "Retail", {"FY2024": 149878, "FY2023": 131600, "FY2022": 106233, "FY2021": 81438}),
    ("DATA", "Secured by mortgages on immovable property", {"FY2024": 216322, "FY2023": 213678, "FY2022": 212289, "FY2021": 218838}),
    ("DATA", "Exposures in default", {"FY2024": 16278, "FY2023": 18400, "FY2022": 12456, "FY2021": 8888}),
    ("DATA", "Other items", {"FY2024": 52400, "FY2023": 46544, "FY2022": 43689, "FY2021": 32050}),
    ("DATA", "Credit Value Adjustment", {"FY2024": 6167, "FY2023": 1778}),
    ("TOTAL", "Credit risk (subtotal)", {"FY2024": 464390, "FY2023": 426900, "FY2022": 391690, "FY2021": 354952}),
    ("SECTION", "Other risk categories", {}),
    ("DATA", "Market risk", {"FY2021": 975}),
    ("DATA", "Operational risk", {"FY2024": 148056, "FY2023": 116389, "FY2022": 83433, "FY2021": 69650}),
    ("TOTAL", "Total RWAs (derived - see sources for reconciliation to the directly disclosed Total RWAs sheet)", {"FY2024": 612446, "FY2023": 543289, "FY2022": 475123, "FY2021": 425577}),
]

bw = BankWorkbook(bank_name=COMPANY, years=YEARS, year_label=None, header_color="7030A0")
bw.add_balance_sheet_sheet(
    title=f"{COMPANY} — Balance Sheet",
    subtitle="Weatherbys Banking Group consolidated statement of financial position, GBP'000. Five latest available financial years.",
    rows=bs_rows,
    sources_text=BS_SOURCES,
    first_col_width=64,
    source_height=280,
    unit_suffix=" (GBP'000)",
)
bw.add_income_statement_sheet(
    title=f"{COMPANY} — Profit & Loss",
    subtitle="Weatherbys Banking Group consolidated income statement, GBP'000. Five latest available financial years.",
    rows=pl_rows,
    sources_text=PL_SOURCES,
    first_col_width=68,
    source_height=220,
    unit_suffix=" (GBP'000)",
)
bw.add_equity_changes_sheet(
    title=f"{COMPANY} — Statement of Changes in Equity",
    subtitle="Weatherbys Banking Group consolidated statement of changes in equity, GBP'000. Chronological, oldest to newest.",
    headers=eq_headers,
    rows=eq_rows,
    sources_text=EQ_SOURCES,
    first_col_width=46,
    source_height=180,
)
bw.add_cash_flow_sheet(
    title=f"{COMPANY} — Cash Flow Statement",
    subtitle="Weatherbys Banking Group consolidated basis, GBP'000. Five latest available financial years.",
    rows=rows,
    sources_text=CASH_SOURCES,
    first_col_width=78,
    source_height=360,
    unit_suffix=" (GBP'000)",
)
bw.add_asset_quality_sheet(
    title=f"{COMPANY} — Asset Quality",
    subtitle="Weatherbys Banking Group loan book credit quality and regulatory credit risk exposure, GBP'000.",
    rows=aq_rows,
    sources_text=AQ_SOURCES,
    first_col_width=68,
    source_height=260,
    unit_suffix=" (GBP'000)",
)

P3_SOURCES = (
    "Sources - Weatherbys Bank 3 Pillar Disclosures, Group/Solo columns, GBP'000 except ratios: "
    f"FY2024, pp.5-6 and 20-26 - {P3_URLS['FY2024']}; "
    f"FY2023, pp.5-6 and 20-27 - {P3_URLS['FY2023']}; "
    f"FY2022, pp.6-7 and 21-27 - {P3_URLS['FY2022']}; "
    f"FY2021, pp.5-6 and 14, 18-22 - {P3_URLS['FY2021']}.\n\n"
    + ENTITY_NOTE
    + " FY2025 is blank for regulatory metrics because the 2025 annual report does not reproduce the requested Pillar 3 capital/liquidity tables and no 2025 Pillar 3 disclosure was located in the official archive."
)

capital = {
    "FY2024": {"cet1": 84898, "tier1": 87898, "total": 99753, "rwa": 613559, "cet1r": "13.84%", "tier1r": "14.33%", "totalr": "16.26%", "lev": "7.08%", "lcr": "1017%", "nsfr": "266%"},
    "FY2023": {"cet1": 73192, "tier1": 76192, "total": 87815, "rwa": 543090, "cet1r": "13.48%", "tier1r": "14.03%", "totalr": "16.17%", "lev": "7.13%", "lcr": "896%", "nsfr": "254%"},
    "FY2022": {"cet1": 57524, "tier1": 57524, "total": 69108, "rwa": 476472, "cet1r": "12.07%", "tier1r": "12.07%", "totalr": "14.50%", "lev": "5.30%", "lcr": "650%", "nsfr": "259.7%"},
    "FY2021": {"cet1": 50247, "tier1": 50247, "total": 61634, "rwa": 425582, "cet1r": "11.81%", "tier1r": "11.81%", "totalr": "14.48%", "lev": "3.37%", "lcr": "531%", "nsfr": "268.2%"},
}

def series(key):
    return {y: capital[y][key] for y in capital}

def metric(name, unit, label, key):
    bw.add_metric_sheet(name, unit, [(label, series(key))], P3_SOURCES, first_col_width=58, source_height=320)

metric("CET1 Capital", "£'000", "CET1 capital", "cet1")
metric("CET1 Ratio", "%", "CET1 ratio", "cet1r")
metric("Tier 1 Capital", "£'000", "Tier 1 capital", "tier1")
metric("Tier 1 Ratio", "%", "Tier 1 ratio", "tier1r")
metric("Total Capital", "£'000", "Total capital", "total")
metric("Total Capital Ratio", "%", "Total capital ratio", "totalr")
metric("Total RWAs", "£'000", "Total risk weighted assets", "rwa")
bw.add_rwa_breakdown_sheet(
    title=f"{COMPANY} — RWA Breakdown",
    subtitle="Weatherbys Bank risk-weighted assets by category, GBP'000 — derived from Pillar 3 capital requirement tables (see sources).",
    rows=rwa_rows,
    sources_text=RWA_SOURCES,
    first_col_width=58,
    source_height=340,
    unit_suffix=" (GBP'000)",
)
metric("Leverage Ratio", "%", "Leverage ratio", "lev")
metric("LCR", "%", "Liquidity coverage ratio", "lcr")
metric("NSFR", "%", "Net stable funding ratio", "nsfr")
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], P3_SOURCES,
    per_note={"MREL Ratio": "MREL was not separately disclosed in the Weatherbys 2021-2024 Pillar 3 documents reviewed; FY2025 has no official Pillar 3 document located. This is an explicit non-disclosure, not a zero."},
)

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {y: dict((r[1], r[2].get(y)) for r in bs_rows).get("Total assets") for y in YEARS}),
        ("Total liabilities", {y: dict((r[1], r[2].get(y)) for r in bs_rows).get("Total liabilities") for y in YEARS}),
        ("Total equity", {y: dict((r[1], r[2].get(y)) for r in bs_rows).get("Total equity") for y in YEARS}),
    ],
    balance_sheet_unit="GBP'000",
    income_statement_totals=[
        ("Operating income", {y: dict((r[1], r[2].get(y)) for r in pl_rows).get("Operating income") for y in YEARS}),
        ("Profit for the financial year", {y: dict((r[1], r[2].get(y)) for r in pl_rows).get("Profit for the financial year") for y in YEARS}),
    ],
    income_statement_unit="GBP'000",
    equity_changes_totals=[
        ("Total equity (year-end)", {"FY2021": 52800, "FY2022": 62500, "FY2023": 84991, "FY2024": 100043, "FY2025": 111114}),
    ],
    equity_changes_unit="GBP'000",
    cash_flow_totals=[
        ("Net cash generated/(used) from operating activities", {y: dict((r[1], r[2].get(y)) for r in rows).get("Net cash generated/(used) from operating activities") for y in YEARS}),
        ("Net cash (used)/generated from investing activities", {y: dict((r[1], r[2].get(y)) for r in rows).get("Net cash (used)/generated from investing activities") for y in YEARS}),
        ("Net cash (used)/generated from financing activities", {y: dict((r[1], r[2].get(y)) for r in rows).get("Net cash (used)/generated from financing activities") for y in YEARS}),
        ("Cash and cash equivalents at end of year", {y: dict((r[1], r[2].get(y)) for r in rows).get("Cash and cash equivalents at end of year") for y in YEARS}),
    ],
    cash_flow_unit="GBP'000",
    ratios=[("CET1 Ratio", series("cet1r")), ("Total Capital Ratio", series("totalr"))],
    note="FY2025 Pillar 3 metrics are blank because no 2025 official disclosure was located; FY2021-FY2024 values are the official Weatherbys Group/Solo disclosures.",
)

bw.save("/Users/armaan/code/katalysis/banks/WEATHERBYS FINANCIALS.xlsx")
